"""The one forwarding facade of the package: makes a file that was cut into part modules keep its meaning.

A large script is cut into part modules; the original file stays as the entry point and as an import
FACADE. Before the cut one module global was seen by all the file's code and by every reader through
`<stem>.<name>`; after it each part has its own globals. `install(__name__, [<parts, low rank first>])`
is the single place that gives `<stem>.<name>` its old meaning back (AR-15, one survivor for every
cut file):

    import part_a
    import part_b
    import module_facade
    module_facade.install(__name__, [part_a, part_b])       # parts may also be given by module name

MIRROR. At install every name a part binds is copied into the facade's own dict (the first part in the
given order wins, a name the facade binds itself stays), so a reader sees it as a plain module attribute
(`vars`, `import *`, `mock.patch.object` treat it as local). Not mirrored: the names the module machinery
owns (`__spec__`, `__file__`, `__all__`, ...) and every name that ANY part's bytecode rebinds through
`global` (STORE_GLOBAL / DELETE_GLOBAL): those stay forwarded, so a cache a part refills is read live.

READS. `facade.x`, for a name the facade's own dict does not bind, returns the value bound in the part that
bound it at install if it still binds it, else in the FIRST part (the given order) that binds it, LIVE:
no cache. A name bound nowhere raises `AttributeError` exactly as a module does. A module-level
`__getattr__` the facade defined BEFORE install is chained AFTER the parts (it is taken out of the
module dict at install, because the interpreter would otherwise call it before the parts).

WRITES. At install the facade records, per part, the names the part binds at module level and the GLOBAL
names its code accesses (`dis` over the module code and every nested code object: LOAD/STORE/DELETE of
GLOBAL or NAME, builtin names such as `open` included; a name only used as an attribute, `o.x`, is not
recorded; the code comes from the part's loader, so a cached bytecode file makes it cheap), and the
same for the facade's own code (the frame that calls `install`). `facade.n = v`, `setattr`, and
`mock.patch.object(facade, n, v)` write `n` into the facade's dict when the facade binds it or its own
code accesses it, into every part whose recorded set holds `n`; a name bound nowhere at all is created
in the facade's dict. `del facade.n` removes `n` from the same places where it is present and raises
`AttributeError` only if it was bound nowhere. `mock.patch.object` round-trips: the first write or
delete of a name remembers the original of each place (or that the place did not bind it, as with a
builtin a part only reads); the write of the object the patch had read, back, or a restoring `del`
followed by that write, puts every place back to ITS original and removes the binding from a place that
had none, provided no other code rebound the name in between; a `patch.object(..., create=True)` of an
absent name leaves no trace.

REFUSED at install: a name a part rebinds through `global` that the facade binds (`from part import n` in
the facade's code) or another part binds: that copy would read stale; the code that rebinds it and
every bare reader of it must live in one part, outsiders read it through the facade.

NOT COVERED, the same as for one plain module today: `from facade import x` taken by an outside module is a
COPY of the value at that moment, not reached by a later patch. Not reached either: a name a part reads or
binds only through a string (`globals()["x"]`, `getattr(module, "x")`), a part imported after install, and
a builtin read as a free name by code that is neither a part nor the facade's own module code. A direct
write into a part module (`part.x = v`, or its own non-`global` rebinding) bypasses the facade: the mirrored
copy in the facade is then stale. `importlib.reload` of a facade is not supported. The module object stays
the same object in `sys.modules`: only its `__class__` is swapped for a `ModuleType` subclass; `__name__`,
`__file__`, `__doc__`, `__spec__` are untouched, so it works when the facade is `__main__` (directly, or
through `run_py_entry.run_as_main`).

THREADS. Writes (and deletes) take a re-entrant lock; reads take none and walk the part dicts in a plain loop.
"""
import dis
import sys
import threading
import types

_MISSING = object()

# What the import system and the module object own: never forwarded to a part, never written to one.
_MACHINERY = frozenset({
    "__builtins__", "__cached__", "__doc__", "__file__", "__loader__", "__name__", "__package__",
    "__path__", "__spec__", "__all__", "__getattr__", "__dir__", "__annotations__",
})
_GLOBAL_OPS = frozenset({"LOAD_GLOBAL", "STORE_GLOBAL", "DELETE_GLOBAL", "LOAD_NAME", "STORE_NAME",
                         "DELETE_NAME", "LOAD_FROM_DICT_OR_GLOBALS"} & set(dis.opmap))
_REBIND_OPS = frozenset({"STORE_GLOBAL", "DELETE_GLOBAL"})


def _scan(code: types.CodeType):
    """(names `code` and its nested code objects access as globals, names they rebind through `global`)."""
    access: set = set()
    rebound: set = set()
    stack = [code]
    while stack:
        current = stack.pop()
        for ins in dis.get_instructions(current):
            if ins.opname in _GLOBAL_OPS:
                access.add(ins.argval)
                if ins.opname in _REBIND_OPS:
                    rebound.add(ins.argval)
        stack.extend(const for const in current.co_consts if isinstance(const, types.CodeType))
    return access - _MACHINERY, rebound - _MACHINERY


def _code_of(part: types.ModuleType):
    """The module code of `part` from its loader, or None when it has no source loader."""
    spec = getattr(part, "__spec__", None)
    get_code = getattr(getattr(spec, "loader", None), "get_code", None)
    return get_code(spec.name) if get_code is not None else None


def _prepare(name: str, parts, own_code: types.CodeType):
    """Validate the call and scan the code; nothing is changed. Returns (facade, parts, recorded, rebound, own)."""
    facade = sys.modules.get(name)
    if not isinstance(facade, types.ModuleType):
        raise ValueError(f"module_facade.install: {name!r} is not an imported module")
    if getattr(type(facade), "__module_facade__", False):
        raise ValueError(f"module_facade.install: {name!r} already has a facade installed "
                         "(reload of a facade is not supported)")
    mods = []
    for part in parts:
        mod = sys.modules.get(part) if isinstance(part, str) else part
        if not isinstance(mod, types.ModuleType):
            raise ValueError(f"module_facade.install: part {part!r} is not an imported module")
        if mod is facade:
            raise ValueError(f"module_facade.install: part {part!r} is the facade {name!r} itself")
        if any(mod is other for other in mods):
            raise ValueError(f"module_facade.install: part {part!r} is given twice")
        mods.append(mod)
    recorded, rebound = [], []
    for mod in mods:
        code = _code_of(mod)
        if code is None:
            raise ValueError(f"module_facade.install: cannot read the code of part {mod.__name__!r} "
                             "(it has no source loader); a part is an imported module of a file")
        access, stored = _scan(code)
        recorded.append(frozenset((set(mod.__dict__) | access) - _MACHINERY))
        rebound.append(stored)
    for i, stored in enumerate(rebound):
        for attr in sorted(stored):
            copies = [f"facade {name!r}"] if attr in facade.__dict__ else []
            copies += [f"part {m.__name__!r}" for j, m in enumerate(mods) if j != i and attr in m.__dict__]
            if copies:
                raise ValueError(f"module_facade.install: {attr!r} is rebound through `global` in part "
                                 f"{mods[i].__name__!r} and also bound in {copies[0]}: that copy would read stale; "
                                 "keep the rebinding code and every bare reader in one part")
    return facade, mods, recorded, set().union(*rebound), _scan(own_code)[0]


class _Shadow:
    """What one name looked like before the first write or delete through the facade."""
    __slots__ = ("read", "facade", "parts", "last", "places")

    def __init__(self, read, facade, parts):
        self.read = read          # what getattr(facade, name) returned (_MISSING: nothing)
        self.facade = facade      # the facade dict's own binding, or _MISSING
        self.parts = parts        # {part index: that part's binding or _MISSING}
        self.last = _MISSING      # the value written last
        self.places = ()          # where it went: -1 is the facade, i >= 0 is part i


class _State:
    """Everything one installed facade knows; the facade class only forwards to it."""

    def __init__(self, name, ns, dicts, recorded, own, home, chained):
        self.name, self.ns, self.dicts = name, ns, dicts
        self.recorded, self.own, self.home, self.chained = recorded, own, home, chained
        self.lock = threading.RLock()       # a value's __del__ may write through the facade while we hold it
        self.shadows: dict = {}

    def part_value(self, attr):
        if attr in _MACHINERY:
            return _MISSING
        i = self.home.get(attr)
        if i is not None:
            found = self.dicts[i].get(attr, _MISSING)
            if found is not _MISSING:
                return found
        for d in self.dicts:
            found = d.get(attr, _MISSING)
            if found is not _MISSING:
                return found
        return _MISSING

    def forward(self, attr):
        found = self.part_value(attr)
        if found is not _MISSING:
            return found
        if self.chained is not None:
            return self.chained(attr)
        raise AttributeError(f"module {self.name!r} has no attribute {attr!r}")

    def read_now(self, attr):
        return self.ns[attr] if attr in self.ns else self.part_value(attr)

    def place_dict(self, place):
        return self.ns if place < 0 else self.dicts[place]

    def new_shadow(self, attr, holders):
        return _Shadow(self.read_now(attr), self.ns.get(attr, _MISSING),
                       {i: self.dicts[i].get(attr, _MISSING) for i in holders})

    def still_ours(self, shadow, attr):
        for place in shadow.places:
            current = self.place_dict(place).get(attr, _MISSING)
            if current is not shadow.last and current is not _MISSING:
                return False
        return True

    def restore(self, shadow, attr):
        for place, original in [(-1, shadow.facade), *shadow.parts.items()]:
            d = self.place_dict(place)
            if original is _MISSING:
                d.pop(attr, None)
            else:
                d[attr] = original

    def write(self, attr, value):
        if attr in _MACHINERY:
            self.ns[attr] = value
            return
        with self.lock:
            shadow = self.shadows.get(attr)
            if shadow is not None and not self.still_ours(shadow, attr):
                shadow = None                           # someone else rebound it: the old originals are stale
            if shadow is not None and value is shadow.read:
                self.restore(shadow, attr)              # the patch hands the original back
                del self.shadows[attr]
                return
            holders = [i for i, names in enumerate(self.recorded) if attr in names]
            if shadow is None:
                shadow = self.shadows[attr] = self.new_shadow(attr, holders)
            places = list(holders)
            if attr in self.ns or attr in self.own or not holders:
                places.append(-1)
            for place in places:
                self.place_dict(place)[attr] = value
            shadow.last = value
            shadow.places = tuple(places)

    def delete(self, attr):
        if attr in _MACHINERY:
            try:
                del self.ns[attr]
            except KeyError:
                raise AttributeError(f"module {self.name!r} has no attribute {attr!r}") from None
            return
        with self.lock:
            holders = [i for i, names in enumerate(self.recorded) if attr in names]
            present = [i for i in holders if attr in self.dicts[i]]
            if attr not in self.ns and not present:
                raise AttributeError(f"module {self.name!r} has no attribute {attr!r}")
            shadow = self.shadows.get(attr)
            if shadow is None:
                shadow = self.shadows[attr] = self.new_shadow(attr, holders)   # a restoring write needs it
            self.ns.pop(attr, None)
            for i in present:
                del self.dicts[i][attr]
            if shadow.read is _MISSING:
                del self.shadows[attr]                  # a created name: nothing to put back


class _Facade(types.ModuleType):
    """The class a facade module is switched to; install makes one subclass per facade carrying the state."""
    __module_facade__ = True

    def __getattr__(self, attr):
        return type(self).__module_facade_state__.forward(attr)

    def __setattr__(self, attr, value):
        type(self).__module_facade_state__.write(attr, value)

    def __delattr__(self, attr):
        type(self).__module_facade_state__.delete(attr)

    def __dir__(self):
        state = type(self).__module_facade_state__
        out = set(state.ns)
        for d in state.dicts:
            out.update(key for key in d if key not in _MACHINERY)
        return sorted(out)


def install(name: str, parts) -> None:
    """Turn the imported module `name` (its `__name__`; `"__main__"` works) into a facade over `parts`
    (imported module objects or their names, LOW rank first). Call it from the facade's module code: that
    code is the facade's own place for writes. ValueError names the problem (a part that is not an
    imported module, the facade itself as a part, a part twice, a second install, a name that would read
    stale) and leaves the module a plain module."""
    facade, mods, recorded, rebound, own = _prepare(name, parts, sys._getframe(1).f_code)
    ns = facade.__dict__
    dicts = tuple(mod.__dict__ for mod in mods)
    chained = ns.pop("__getattr__", None)
    home: dict = {}
    for i, d in enumerate(dicts):
        for key in d:
            if key not in _MACHINERY:
                home.setdefault(key, i)
    for key, i in home.items():
        if key not in rebound and key not in ns:
            ns[key] = dicts[i][key]
    state = _State(name, ns, dicts, tuple(recorded), own, home, chained)
    facade.__class__ = type("_Facade", (_Facade,), {"__module_facade_state__": state})

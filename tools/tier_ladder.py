"""The ladder home: ONE module that holds the model-family order, the function
ranks, the default bindings and the one reader of delegation.config.yaml's
`roles.<function>` bindings. Every reader of "who outranks whom" -- the tier gate
(tools/mechanism_gate.py), the savings counterfactual (tools/savings_report.py)
and, in later streams, the journal matrix, the MODEL line and the echo/dispatch
gates -- goes through the functions below (spec 20261116-architect-tier-spec, S2;
SIBLING_MAP axis 34).

A LEAF, not a gate: it imports the standard library only. `yaml` is imported
lazily INSIDE bindings(), so a hook that needs only FAMILIES / family_of takes no
pyyaml dependency on its path.

Error direction (a resolver that feeds a GATE): rank_of_model may err only
DOWNWARD (a lower rank -> a basis is needed / the tier line is refused); it never
invents a rank above what the bindings or the family order give.
"""
from __future__ import annotations

# The model-family vocabulary in ONE order, weakest -> strongest. A reader that
# needs strongest-first reverses it; no reader keeps its own tuple.
FAMILIES = ("haiku", "sonnet", "opus", "fable")
ALIASES = {"mythos": "fable"}

# Function ranks (critic = designer). designer is an EXECUTOR rank only: it is
# not a coordination rung and the config is never read for it.
FUNCTION_RANKS = {"scout": 0, "builder": 1, "critic": 2, "designer": 2, "lead": 3, "architect": 4}
COORDINATION_FUNCTIONS = ("scout", "builder", "critic", "lead", "architect")

# The bindings used when the config yields none (absent, unparsable, oversize,
# aliased, no pyyaml, no lead model). It equals the live config by family, so a
# config-less clone behaves as the repository always did.
DEFAULT_BINDINGS = {"lead": "fable", "critic": "opus", "builder": "sonnet", "scout": "sonnet"}

MAX_CONFIG_BYTES = 64 * 1024
_RESERVE_NOTE = "roles.reserve is not read: rename it to roles.architect"


def family_of(model_id) -> str | None:
    """The family of a model id or word (lowercase substring match on FAMILIES and
    ALIASES); None for a non-Claude id, an empty or non-string input."""
    if not isinstance(model_id, str) or not model_id.strip():
        return None
    low = model_id.lower()
    for fam in FAMILIES:
        if fam in low:
            return fam
    for alias, fam in ALIASES.items():
        if alias in low:
            return fam
    return None


def rank_of_function(name) -> int | None:
    """FUNCTION_RANKS; an unknown (or non-string) name -> None."""
    if not isinstance(name, str):
        return None
    return FUNCTION_RANKS.get(name)


def _role_model(role_data):
    if not isinstance(role_data, dict):
        return None
    for key in ("subscription", "api"):
        block = role_data.get(key)
        model = block.get("model") if isinstance(block, dict) else None
        if isinstance(model, str) and model.strip():
            return model.strip()
    return None


def bindings(config_text) -> tuple[dict, str | None]:
    """(function -> model id for the coordination functions that have a model, a
    problem note). Absent text, text over 64 KB, any YAML alias or anchor, a parse
    error, no `roles` mapping or pyyaml missing -> ({}, "<reason>"). An uncommented
    `roles.reserve` is NOT read; the note names the rename door."""
    if not isinstance(config_text, str) or not config_text.strip():
        return {}, "config absent"
    if len(config_text.encode("utf-8", errors="replace")) > MAX_CONFIG_BYTES:
        return {}, "config is over 64 KB"
    try:
        import yaml
    except ImportError:
        return {}, "pyyaml is not installed"

    class _NoAliasLoader(yaml.SafeLoader):
        def compose_node(self, parent, index):
            event = self.peek_event()
            if isinstance(event, yaml.AliasEvent) or getattr(event, "anchor", None):
                raise yaml.YAMLError("a YAML alias or anchor is not allowed")
            return super().compose_node(parent, index)

    try:
        data = yaml.load(config_text, Loader=_NoAliasLoader)  # noqa: S506 -- SafeLoader subclass
    except (yaml.YAMLError, ValueError, RecursionError) as exc:
        first = next(iter(str(exc).strip().splitlines()), "") or type(exc).__name__
        return {}, f"config is not readable YAML ({first})"
    roles = data.get("roles") if isinstance(data, dict) else None
    if not isinstance(roles, dict):
        return {}, "config has no roles mapping"
    found = {}
    for function in COORDINATION_FUNCTIONS:
        model = _role_model(roles.get(function))
        if model:
            found[function] = model
    note = _RESERVE_NOTE if roles.get("reserve") is not None else None
    if not found:
        return {}, "; ".join(filter(None, ["no coordination function has a model", note]))
    return found, note


def _effective(config_text) -> tuple[dict, str | None, bool]:
    found, note = bindings(config_text)
    if "lead" not in found:
        if found:  # a config that binds other functions but names no lead model
            note = "; ".join(filter(None, ["roles.lead names no model", note]))
        return dict(DEFAULT_BINDINGS), note, True
    return found, note, False


def effective_bindings(config_text) -> tuple[dict, str | None]:
    """bindings() or, when it yields none (or no lead), DEFAULT_BINDINGS with the
    note. EVERY reader goes through this one function."""
    found, note, _ = _effective(config_text)
    return found, note


def _idx(family):
    return FAMILIES.index(family)


def _usable(function, model, lead_family):
    """A rung bound to a family WEAKER than lead's never inherits a rank >= lead."""
    if FUNCTION_RANKS[function] <= FUNCTION_RANKS["lead"]:
        return True
    fam = family_of(model)
    return lead_family is None or fam is None or _idx(fam) >= _idx(lead_family)


def _resolve(model, found):
    """(rank | None, road, bound id of the top matching function) -- the ONE
    matcher; rank_of_model and function_of_session both read it."""
    if not isinstance(model, str) or not model.strip():
        return None, "", ""
    lead_fam = family_of(found.get("lead"))
    rungs = {f: m for f, m in found.items() if _usable(f, m, lead_fam)}
    exact = [f for f, m in rungs.items() if m == model]
    if exact:
        top = max(exact, key=FUNCTION_RANKS.__getitem__)
        return FUNCTION_RANKS[top], "exact", rungs[top]
    fam = family_of(model)
    if fam is None:
        return None, "", ""
    same = [f for f, m in rungs.items() if family_of(m) == fam]
    if same:
        top = max(same, key=FUNCTION_RANKS.__getitem__)
        return FUNCTION_RANKS[top], "family", rungs[top]
    if lead_fam is None:
        return None, "", ""  # nothing to place a family against
    if _idx(fam) > _idx(lead_fam):
        return FUNCTION_RANKS["architect"], "above", ""
    weaker = [(_idx(family_of(m)), f) for f, m in rungs.items()
              if family_of(m) is not None and _idx(family_of(m)) < _idx(fam)]
    if not weaker:
        return -1, "below", ""
    nearest = max(i for i, _ in weaker)
    top = max((f for i, f in weaker if i == nearest), key=FUNCTION_RANKS.__getitem__)
    return FUNCTION_RANKS[top], "between", ""


def rank_of_model(model_word_or_id, config_text) -> int | None:
    """THE rank function the matrix, the tier gate and the MODEL line share:
    (a) an exact id match on a bound rung -> the max rank among matches;
    (b) else the FAMILY: the max rank of the functions bound to that family;
    (c) a known family bound to nothing: stronger than lead's family -> architect
        rank; weaker than every bound family -> -1 (below scout, the floor); in
        between -> the rank of the nearest WEAKER bound family's top function;
    (d) unknown family, non-Claude id with no exact match, empty, non-string -> None."""
    return _resolve(model_word_or_id, effective_bindings(config_text)[0])[0]


def lead_binding(config_text) -> str | None:
    return effective_bindings(config_text)[0].get("lead")


def architect_binding(config_text) -> str | None:
    return effective_bindings(config_text)[0].get("architect")


def function_of_session(model_id, config_text) -> tuple[str | None, str]:
    """(coordination function of the session's rank, a note naming the road taken).
    Derived from the one matcher, never a matcher of its own; designer is never a
    session function."""
    found, _note, defaulted = _effective(config_text)
    rank, road, bound = _resolve(model_id, found)
    if rank is None:
        return None, "matches no binding"
    if rank < 0:
        return None, "below builder"
    function = next(f for f in COORDINATION_FUNCTIONS if FUNCTION_RANKS[f] == rank)
    if defaulted:
        return function, "config unreadable: default bindings"
    if road == "exact":
        return function, ""
    if road == "family":
        return function, f"family match: {bound}"
    if road == "above":
        return function, "no architect binding"
    return function, "unbound family"

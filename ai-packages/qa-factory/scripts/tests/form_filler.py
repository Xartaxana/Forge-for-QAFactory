"""The form filler (P1-a spec 3.5): fills a handoff form the way its own hints say, for the writer-reader round.

A helper next to the tests, not a test. It reads the contract ONLY through the module that owns it (`handoff`: `index`, `template`,
`spec`, `is_placeholder`, `set_value`, and the reader functions `relaxed_sections`, `rows_owed`, `null_outcomes`,
`owned_by_contract`, so no rule of a reader is copied here) and never opens a reader's regular expression. Which generator fills
which kind of hint is a table in `fixtures/form-fill-rules.json`. A hint no rule fits is NOT guessed: it comes back as an
`Unfillable`, and the caller turns it into a red row (or `require()` raises `NotFillable`).

Pure: only the form text is produced, `write_dispatch_form` is the one function that writes, and only under the task root it is given.
Deterministic: the same contract, context, verdict, variant and overrides give the same bytes (no time, no randomness; the order of
the keys is the template's).

Fields code fills (`handoff_check._code_fills`) stay as the template wrote them and are named in `left_for_code`.
"""
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import handoff  # noqa: E402
import handoff_check  # noqa: E402

RULES_PATH = HERE / "fixtures" / "form-fill-rules.json"
VARIANT_BASE, OMIT_OPTIONAL, EMPTY_LISTS = "base", "omit_optional", "empty_lists"
AT_LIMIT, BEYOND_LIMIT = "at_limit", "beyond_limit"
ALT = re.compile(r"alt:(\d+)")
DISPATCH_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
ROW_INDEX = re.compile(r"\[(\d+)\]")
ID_TOKEN = re.compile(r"([A-Z]{1,4})-(?:n|m|ID)\b")
ID_NUMBER = re.compile(r"-n(?![A-Za-z])")
ALT_SPLIT = re.compile(r",\s+or\s+|,\s+|\s+or\s+")


class _Absent:
    """The one marker object: "remove this field" (in `overrides`), and the value of a field that was left out."""
    __slots__ = ()

    def __repr__(self) -> str:
        return "ABSENT"


ABSENT = _Absent()


@dataclass(frozen=True)
class FillContext:
    """What the world knows. A token of a contract with no key here is unfillable, never a guess (E12)."""
    task_key: str = "TP1-1"
    case_id_form: str | None = None
    dispatches: dict = field(default_factory=dict)
    author_dispatch: str = ""
    minted: dict = field(default_factory=dict)
    files: dict = field(default_factory=dict)
    cases: list = field(default_factory=list)
    bugs: list = field(default_factory=list)
    requirements: list = field(default_factory=list)


@dataclass(frozen=True)
class Fill:
    path: str
    hint: str          # the template's own text of the field (the angle brackets included)
    value: object      # what was written; ABSENT when the field was left out
    rule: str          # the id of the rule (form-fill-rules.json), "override", "token", "verdict" or "omit-optional"


@dataclass(frozen=True)
class Unfillable:
    path: str
    hint: str
    why: str


class NotFillable(Exception):
    """A form that cannot be filled: the contract (or output), the field and the hint, and why."""

    def __init__(self, where: str, path: str, hint: str, why: str):
        super().__init__(f"{where}: cannot fill {path} «{hint}»: {why}")
        self.where, self.path, self.hint, self.why = where, path, hint, why


@dataclass
class Filled:
    contract: str
    verdict: str | None
    variant: str
    text: str
    data: dict
    fills: list
    unfillable: list
    left_for_code: list

    def require(self) -> "Filled":
        """The form itself, or `NotFillable` naming the first field it could not fill (and how many more)."""
        if self.unfillable:
            first = self.unfillable[0]
            more = f" (and {len(self.unfillable) - 1} more)" if len(self.unfillable) > 1 else ""
            raise NotFillable(self.contract, first.path, first.hint, first.why + more)
        return self


# ------------------------------------------------------------------------------------------------ the rules
@dataclass
class _Gen:
    values: list                 # values[0] is the base; the rest are the alternatives the hint offers (E1, E2)
    rule: str
    at: object = None            # the value of exactly N characters, for a `<= N characters` limit (E13)
    beyond: object = None        # N + 1 characters
    empty: bool = False          # the hint says the empty list is a legal answer (E6)


def _leaf(path: str) -> str:
    name = ROW_INDEX.sub("", path.rsplit(".", 1)[-1])
    return name or "value"


def _row_number(path: str) -> int:
    found = ROW_INDEX.findall(path)
    return int(found[-1]) + 1 if found else 1


def _gen_limit(rule, match, hint, fspec, path):
    size = fspec.max_len
    base = f"filled {_leaf(path)}"[:size]
    at = (f"filled {_leaf(path)} " + "x" * size)[:size]
    return _Gen([base], rule["id"], at=at, beyond=at + "x")


def _gen_first_option(rule, match, hint, fspec, path):
    return _Gen([fspec.options[0]], rule["id"]) if fspec.options else None


def _gen_values(rule, match, hint, fspec, path):
    return _Gen(list(rule["values"]), rule["id"])


def _gen_literal(rule, match, hint, fspec, path):
    return _Gen([rule["value"]], rule["id"])


def _gen_hint_number(rule, match, hint, fspec, path):
    return _Gen([int(hint)], rule["id"])


def _gen_free_text(rule, match, hint, fspec, path):
    return _Gen([f"filled {_leaf(path)}"], rule["id"], empty=bool(rule.get("empty")))


def _id_value(token: str, path: str) -> str:
    prefix = ID_TOKEN.match(token).group(1)
    return f"{prefix}-{_row_number(path)}"


def _gen_id_prefix(rule, match, hint, fspec, path):
    values = [_id_value(hint, path)]
    if rule.get("word_alternative"):
        values.append(rule["word_alternative"])
    return _Gen(values, rule["id"], empty=bool(rule.get("empty")))


def _gen_alternatives(rule, match, hint, fspec, path):
    values = [_id_value(item, path) if ID_TOKEN.match(item) else f"filled {_leaf(path)}" for item in ALT_SPLIT.split(hint)]
    return _Gen(values, rule["id"])


def _gen_id_in_path(rule, match, hint, fspec, path):
    return _Gen([ID_NUMBER.sub(f"-{_row_number(path)}", hint)], rule["id"])


GENERATORS = {"limit": _gen_limit, "first_option": _gen_first_option, "values": _gen_values, "literal": _gen_literal,
              "hint_number": _gen_hint_number, "free_text": _gen_free_text, "id_prefix": _gen_id_prefix,
              "alternatives": _gen_alternatives, "id_in_path": _gen_id_in_path}
_RULES: dict = {}


def rules() -> dict:
    """form-fill-rules.json, read once; a rule with a generator the code does not name, or a pattern that does not compile, raises."""
    if not _RULES:
        data = json.loads(RULES_PATH.read_text(encoding="utf-8"))
        for row in data["rules"]:
            if row["gen"] not in GENERATORS:
                raise ValueError(f"{RULES_PATH.name}: rule {row['id']!r} names the generator {row['gen']!r}, which is not one of {sorted(GENERATORS)}")
            row["_re"] = re.compile(row["pattern"], re.S) if "pattern" in row else None
        _RULES.update(data)
    return _RULES


def _hint_of(raw: str) -> str:
    text = raw.strip()
    return text[1:-1].strip()           # `handoff.is_placeholder` has said it is `<...>` (or empty)


def _generate(raw: str, fspec, path: str):
    """(_Gen | None, why): the first rule that fits the hint, or None and the reason (E10)."""
    hint = _hint_of(raw)
    if not hint:
        return None, "the template holds no hint for this field"
    for rule in rules()["rules"]:
        when = rule.get("when", "")
        if when == "max_len" and not fspec.max_len:
            continue
        if when.startswith("kind:") and fspec.kind != when[5:]:
            continue
        match = None
        if rule["_re"] is not None:
            match = rule["_re"].fullmatch(hint)
            if not match:
                continue
        got = GENERATORS[rule["gen"]](rule, match, hint, fspec, path)
        if got is None:
            return None, f"rule `{rule['id']}` found no value to write (the hint names a closed list the contract cannot read)"
        return got, ""
    return None, "no rule of form-fill-rules.json fits this hint"


# ------------------------------------------------------------------------------------------------ the survey
@dataclass
class _Item:
    path: str
    generic: str
    raw: str
    node: object
    fspec: object
    kind: str                    # keep | token | code | verdict | gen | nogen
    gen: object = None
    why: str = ""


class _Survey:
    def __init__(self, contract: str):
        self.contract = contract
        self.tmpl = handoff.template(contract)
        self.spec = handoff.spec(contract)
        verdict = self.spec.get("header.verdict")
        self.has_verdict = verdict is not None
        self.words = list(verdict.options) if verdict is not None and verdict.options else None
        self.items = []
        for path, node in sorted(self.tmpl.nodes.items(), key=lambda kv: kv[1].line):
            if handoff.owned_by_contract(path):
                continue
            generic = ROW_INDEX.sub("[]", path)
            fspec = self.spec[generic]
            raw = "" if node.value is None else str(node.value)
            if not handoff.is_placeholder(node.value):
                if any(tok in raw for tok in rules()["context_tokens"]):
                    kind = "code" if handoff_check._code_fills(path) else "token"      # a value code fills is code's, token or not
                else:
                    kind = "keep"
                self.items.append(_Item(path, generic, raw, node, fspec, kind))
            elif path == "header.verdict":
                self.items.append(_Item(path, generic, raw, node, fspec, "verdict"))
            elif handoff_check._code_fills(path):
                self.items.append(_Item(path, generic, raw, node, fspec, "code"))
            elif raw.strip() in rules()["context_tokens"]:
                self.items.append(_Item(path, generic, raw, node, fspec, "token"))
            else:
                gen, why = _generate(raw, fspec, path)
                self.items.append(_Item(path, generic, raw, node, fspec, "gen" if gen else "nogen", gen, why))
        gens = [i.gen for i in self.items if i.kind == "gen"]
        self.max_alts = max([len(g.values) for g in gens] + [1])
        self.has_limits = any(g.at is not None for g in gens)
        self.has_optional = any(i.kind in ("gen", "code") and i.fspec.optional for i in self.items)
        self.list_sections = [name for name, value in self.tmpl.data.items()
                              if isinstance(value, list) and not handoff.owned_by_contract(name)]
        self.has_empty_field = any(g.empty for g in gens)

    def emptiable(self, word) -> list:
        """The list sections a role may legally leave empty under `word`: not the one list every form owes (unless the form
        declares a null outcome for it, E6) and not a list the verdict owes rows of (E5)."""
        owed = handoff.rows_owed(self.contract, word) if word else set()
        required = set(handoff.REQUIRED_LISTS) - set(handoff.null_outcomes(self.contract))
        return [name for name in self.list_sections if name not in owed and name not in required]

    def names(self) -> list:
        out = [VARIANT_BASE]
        if self.has_optional:
            out.append(OMIT_OPTIONAL)
        if self.emptiable(None) or self.has_empty_field:
            out.append(EMPTY_LISTS)
        out += [f"alt:{k}" for k in range(1, self.max_alts)]
        if self.has_limits:
            out += [AT_LIMIT, BEYOND_LIMIT]
        return out


def variants(contract: str) -> list:
    """`[(verdict word | None, variant)]` for the form: every word of `header.verdict` (None for a form with no such field) times the
    variants the form's hints call for (base always; the others only where the form has something for them to change)."""
    survey = _Survey(contract)
    words = survey.words if survey.words else [None]
    return [(word, name) for word in words for name in survey.names()]


# ------------------------------------------------------------------------------------------------ the filling
def _override_for(path: str, generic: str, overrides: dict):
    """(found, value): the most specific override of this field: `section[0].key` over `section[].key`."""
    if path in overrides:
        return True, overrides[path]
    if generic in overrides:
        return True, overrides[generic]
    return False, None


def _delete_leaf(lines: list, node) -> None:
    """Remove the scalar's lines. A row's first key carries the row's dash: the dash moves to the row's next key, or the row goes."""
    first, last = node.line, node.end_line
    dash = re.match(r"^(\s*)-\s+", lines[first])
    if dash and node.key:
        j = last + 1
        while j < len(lines) and (not lines[j].strip() or lines[j].lstrip().startswith("#")):
            j += 1
        if j < len(lines) and len(lines[j]) - len(lines[j].lstrip()) == len(dash.group(1)) + 2 \
                and not lines[j].lstrip().startswith("- "):
            lines[j] = " " * len(dash.group(1)) + "- " + lines[j].lstrip()
    del lines[first:last + 1]


def _section_span(lines: list, name: str):
    start = next((i for i, text in enumerate(lines) if re.match(r"^" + re.escape(name) + r"\s*:", text)), None)
    if start is None:
        return None
    last = start
    for j in range(start + 1, len(lines)):
        text = lines[j]
        if not text.strip() or text.lstrip().startswith("#"):
            continue
        if len(text) - len(text.lstrip()) == 0 and not text.startswith("-"):
            break
        last = j
    return start, last


def fill_form(contract: str, ctx: FillContext, *, verdict=None, variant: str = VARIANT_BASE, overrides=None) -> Filled:
    """The form of `contract` filled from its own hints: every field the role fills gets the value its hint says (the first
    alternative in the base variant), a field code fills stays as written, and a hint nothing fits is listed in `unfillable`.

    `verdict`: the word of `header.verdict` (None: the first word). `variant`: one of `variants(contract)`; any other name
    raises ValueError. `overrides`: `{path: value | ABSENT}` in the grammar of the paths of the forms (`section[].key` every row,
    `section[0].key` one row; a top-level section name only with ABSENT or, for a list, `[]`); the value goes in as given, and an
    override that names no field is an `Unfillable`, never a quiet no-op (E20)."""
    overrides = dict(overrides or {})
    survey = _Survey(contract)
    names = survey.names()
    if variant not in names:
        raise ValueError(f"{contract}: {variant!r} is not a variant of this form; its variants are {names}")
    unfillable, fills, left = [], [], []
    word = verdict
    if survey.has_verdict:
        if word is None:
            word = survey.words[0] if survey.words else None
        elif survey.words and word not in survey.words:
            unfillable.append(Unfillable("header.verdict", "", f"`{word}` is not a word of vocabulary.header_verdicts: {survey.words}"))
    elif verdict is not None:
        unfillable.append(Unfillable("header.verdict", "", f"the form has no header.verdict, and the verdict `{verdict}` was asked for"))
        word = None
    word_text = word if isinstance(word, str) else None
    dropped = set(handoff.relaxed_sections(contract, word_text)) & set(survey.tmpl.data) if word_text else set()
    emptied = set()
    if variant == EMPTY_LISTS:
        emptied = set(survey.emptiable(word_text)) - dropped
    # section-level overrides: ABSENT drops a section, [] empties a list section; anything else names no field
    sections = survey.tmpl.data
    for key in list(overrides):
        if key in sections and not handoff.owned_by_contract(key):
            value = overrides[key]
            if value is ABSENT:
                dropped.add(key)
                fills.append(Fill(key, "", ABSENT, "override"))
                emptied.discard(key)
            elif value == [] and isinstance(sections[key], list):
                emptied.add(key)
                fills.append(Fill(key, "", [], "override"))
            else:
                unfillable.append(Unfillable(key, "", f"override names no field of {contract}: `{key}` is a section, and a section takes only ABSENT or []"))
            del overrides[key]
    # every other override must name a field of the form
    matched = set()
    for item in survey.items:
        if item.path in overrides:
            matched.add(item.path)
        if item.generic in overrides and item.generic != item.path:
            matched.add(item.generic)
    for key in overrides:
        if key not in matched:
            unfillable.append(Unfillable(key, "", f"override names no field of {contract}"))
    ops = []                                          # (node, "set" | "delete", value, path)
    for item in survey.items:
        head = item.path.split(".")[0].split("[")[0]
        found, value = _override_for(item.path, item.generic, overrides)
        if head in dropped or head in emptied:
            if found:
                unfillable.append(Unfillable(item.path, item.raw, f"the override cannot land: the section `{head}` is left out or emptied in this variant"))
            continue
        if found:
            if value is ABSENT:
                ops.append((item.node, "delete", None, item.path))
            else:
                ops.append((item.node, "set", value, item.path))
            fills.append(Fill(item.path, item.raw, value, "override"))
            continue
        if item.kind == "keep":
            continue
        if item.kind == "token":
            text, missing = item.raw, []
            for token, key in rules()["context_tokens"].items():
                if token in text:
                    given = getattr(ctx, key, "")
                    if given:
                        text = text.replace(token, str(given))
                    else:
                        missing.append((token, key))
            if missing:
                unfillable.append(Unfillable(item.path, item.raw, "; ".join(f"the contract's token {t} has no key `{k}` in the context" for t, k in missing)))
            else:
                ops.append((item.node, "set", text, item.path))
                fills.append(Fill(item.path, item.raw, text, "token"))
            continue
        if item.kind == "code":
            if variant == OMIT_OPTIONAL and item.fspec.optional:
                ops.append((item.node, "delete", None, item.path))
                fills.append(Fill(item.path, item.raw, ABSENT, "omit-optional"))
            else:
                left.append(item.path)
            continue
        if item.kind == "verdict":
            if word_text is None:
                unfillable.append(Unfillable(item.path, item.raw, "the form's `header.verdict` has no word to write (vocabulary.header_verdicts is empty)"))
            else:
                ops.append((item.node, "set", word_text, item.path))
                fills.append(Fill(item.path, item.raw, word_text, "verdict"))
            continue
        if item.kind == "nogen":
            unfillable.append(Unfillable(item.path, item.raw, item.why))
            continue
        gen = item.gen
        if variant == OMIT_OPTIONAL and item.fspec.optional:
            ops.append((item.node, "delete", None, item.path))
            fills.append(Fill(item.path, item.raw, ABSENT, "omit-optional"))
            continue
        value = gen.values[0]
        alt = ALT.fullmatch(variant)
        if variant == EMPTY_LISTS and gen.empty:
            value = []
        elif alt and int(alt.group(1)) < len(gen.values):
            value = gen.values[int(alt.group(1))]
        elif variant == AT_LIMIT and gen.at is not None:
            value = gen.at
        elif variant == BEYOND_LIMIT and gen.beyond is not None:
            value = gen.beyond
        ops.append((item.node, "set", value, item.path))
        fills.append(Fill(item.path, item.raw, value, gen.rule))
    doc = survey.tmpl
    for node, action, value, path in sorted(ops, key=lambda op: op[0].line, reverse=True):
        if action == "delete":
            _delete_leaf(doc.lines, node)
        elif not handoff.set_value(doc, path, value):
            unfillable.append(Unfillable(path, "", "handoff.set_value refused to write the field"))
    spans = [(name, _section_span(doc.lines, name), name in dropped) for name in sorted(dropped | emptied)]
    for name, span, drop in sorted((s for s in spans if s[1]), key=lambda s: s[1][0], reverse=True):
        doc.lines[span[0]:span[1] + 1] = [] if drop else [f"{name}: []"]
    text = doc.text()
    return Filled(contract, word_text, variant, text, handoff.parse(text).data, fills, unfillable, left)


def write_dispatch_form(task_root, dispatch_id: str, contract: str, ctx: FillContext, verdict, *, overrides=None) -> Path:
    """`<task_root>/work/handoffs/<dispatch_id>.yaml`: the form of `contract` filled in its base variant, the file a dispatch's role would
    leave. Raises NotFillable (never writes a half-filled form) and ValueError for a dispatch id that is not one plain file name."""
    if not DISPATCH_ID.fullmatch(str(dispatch_id)):
        raise ValueError(f"dispatch id {dispatch_id!r} is not one plain file name (letters, digits, `.`, `_`, `-`)")
    filled = fill_form(contract, ctx, verdict=verdict, overrides=overrides).require()
    path = Path(task_root) / "work" / "handoffs" / f"{dispatch_id}.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(filled.text.encode("utf-8"))
    return path

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
import importlib
import json
import re
import sys
from dataclasses import dataclass, field, replace
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import grammar  # noqa: E402
import handoff  # noqa: E402
import handoff_check  # noqa: E402

RULES_PATH = HERE / "fixtures" / "form-fill-rules.json"
ROOT = HERE.parents[1]               # the package root: a template row names its contract file from here (`references/...`)
REFERENCES = ROOT / "references"
ROLE_WRITER = " (the role)"          # the predicate of driver_runner (`writer == "<role> (the role)"`): a role writes the output
HINT = re.compile(r"<(?!!--)[^<>\n]+>")      # a hint, never the `<!-- ... -->` marker line of a report block
FRONT_KEY = re.compile(r"^([A-Za-z_][\w-]*):\s?(.*)$")
BODY = "body:"
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
    dispatch_id: str = ""        # what the token `<dispatch>` reads; empty keeps the token unfillable (the caller names it)
    case_id: str = ""            # what the artifact token `<case id>` reads: set by `fill_artifact` for each id of `cases` (forms never read it)
    bug_id: str = ""             # what the artifact token `<bug id>` reads: set by `fill_artifact` for each id of `bugs`
    area: str = "general"        # what the token `<area>` reads: the area the artifact templates put their cases in
    impl_diff: str = ""          # what the artifact token `<the diff text>` reads: the text of the merge request's diff the world holds (the story kit's
                                 # input, no product writer); empty keeps the token unfillable (the caller names it, nothing is written)
    cases_root: str = ""         # what the token `<cases_root>` reads when the form has no plain `cases_root` field: the world's own case store, as the
                                 # product's reader (`contract.cases_root`) resolves it there; empty keeps the token unfillable (the caller names it)

    channels: dict = field(default_factory=dict)   # case id -> `auto` | `manual`: the story kit's channel of each case (the one source in a dry world)

    @property
    def case_channel(self) -> str:
        """What the artifact token `<channel>` reads: the kit's channel of the case being written; a case the kit gives none (or no kit at all) is `auto`."""
        given = self.channels.get(self.case_id) if isinstance(self.channels, dict) else None
        return given if isinstance(given, str) and given.strip() else "auto"

    @property
    def first_case(self) -> str:
        """What the token `<case>` reads: the case `fill_artifact` is writing, else the first case of the world; empty when there is none."""
        return self.case_id or next((c for c in self.cases if isinstance(c, str) and c.strip()), "")


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
    literal_text: list = field(default_factory=list)       # paths whose value is text a `literal_text` row names (an angle bracket that is no hint)
    kept_in_contract: list = field(default_factory=list)   # (path, hint text): contract-owned values with a hint no token names, kept as the contract wrote them

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
    world: str = ""              # the key of the context whose list holds the ids this field names (`cases`); the row's own number picks one


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


PLAIN_ID = re.compile(r"([A-Z]{1,4})-(\d+)")


def _issued(value, ctx):
    """An id the hint gave (`TC-1`, row n of its prefix) becomes the n-th id the WORLD issued for that prefix (`ctx.minted`, e.g. the case
    `TC-001`) when the context holds one; with none it stays as the hint gave it. The world's ids are the ones its readers know."""
    found = PLAIN_ID.fullmatch(value) if isinstance(value, str) else None
    ids = ctx.minted.get(found.group(1)) if found else None
    at = int(found.group(2)) - 1 if found else -1
    return ids[at] if isinstance(ids, list) and 0 <= at < len(ids) and isinstance(ids[at], str) and ids[at].strip() else value


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


def _gen_world_ids(rule, match, hint, fspec, path):
    return _Gen([f"filled {_leaf(path)}"], rule["id"], world=rule["from"])


GENERATORS = {"world_ids": _gen_world_ids, "limit": _gen_limit, "first_option": _gen_first_option, "values": _gen_values, "literal": _gen_literal,
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
        for row in data.get("literal_text", []):
            row["_re"] = re.compile(row["pattern"], re.S)
        _RULES.update(data)
    return _RULES


def _hint_of(raw: str) -> str:
    text = raw.strip()
    return text[1:-1].strip()           # `handoff.is_placeholder` has said it is `<...>` (or empty)


def _hint_list(value) -> bool:
    """Is `value` a non-empty list whose every element is a whole hint (`["<reason>"]`)? Such a list is filled element by element."""
    return isinstance(value, list) and bool(value) and all(isinstance(e, str) and e.strip() and handoff.is_placeholder(e) for e in value)


def _literal_text(raw: str):
    """The id of the `literal_text` row of form-fill-rules.json that says `raw` is text, not a hint (a command template a role copies
    as it stands), or None. A row is named data: the filler holds no list of such texts."""
    return next((row["id"] for row in rules().get("literal_text", []) if row["_re"].search(raw)), None)


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
        self.kept = []                      # (path, raw): contract-owned values that carry a hint no token names - the contract's, kept as written
        tokens = {**rules()["context_tokens"], **rules().get("form_field_tokens", {})}
        for path, node in sorted(self.tmpl.nodes.items(), key=lambda kv: kv[1].line):
            generic = ROW_INDEX.sub("[]", path)
            raw = "" if node.value is None else str(node.value)
            if handoff.owned_by_contract(path):
                # the contract writes these itself; only a token inside one (`inputs[0].path`) is the filler's to substitute
                if isinstance(node.value, str) and any(tok in raw for tok in tokens):
                    self.items.append(_Item(path, generic, raw, node, self.spec.get(generic), "token"))
                elif isinstance(node.value, str) and HINT.search(raw) and _literal_text(raw) is None:
                    self.kept.append((path, raw))
                continue
            fspec = self.spec[generic]
            if _hint_list(node.value):                      # `["<reason>"]`: every element is a hint of its own, filled by the same rules
                firsts, why = [], ""
                for at, element in enumerate(node.value):
                    one, why = _generate(str(element), fspec, f"{path}[{at}]")
                    if one is None:
                        break
                    firsts.append(one.values[0])
                gen = _Gen([firsts], "hint-list") if len(firsts) == len(node.value) else None
                self.items.append(_Item(path, generic, raw, node, fspec, "gen" if gen else "nogen", gen, why))
            elif not handoff.is_placeholder(node.value):
                if any(tok in raw for tok in tokens):
                    kind = "code" if handoff_check._code_fills(path, self.contract) else "token"      # a value code fills is code's, token or not
                elif HINT.search(raw) and _literal_text(raw) is None:
                    kind = "code" if handoff_check._code_fills(path, self.contract) else "embedded"   # a hint inside a value, named by no token and no literal-text row
                elif HINT.search(raw):
                    kind = "literal"                                                   # text that carries an angle bracket, named by a literal-text row
                else:
                    kind = "keep"
                self.items.append(_Item(path, generic, raw, node, fspec, kind))
            elif path == "header.verdict":
                self.items.append(_Item(path, generic, raw, node, fspec, "verdict"))
            elif handoff_check._code_fills(path, self.contract):
                self.items.append(_Item(path, generic, raw, node, fspec, "code"))
            elif raw.strip() in tokens:
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


def _finish_token(item, text: str, missing: list, ops: list, fills: list, unfillable: list) -> None:
    """Close a value whose tokens were substituted: a token with no value, or a hint STILL left in the text (a hint that is no token), is an
    `Unfillable` - never a value that leaves the filler carrying a hint (AR-28) - unless a `literal_text` row names the text."""
    if missing:
        unfillable.append(Unfillable(item.path, item.raw, "; ".join(missing)))
        return
    left = HINT.findall(text)
    if left and _literal_text(text) is None:
        unfillable.append(Unfillable(item.path, item.raw, f"after the tokens were filled the value still carries {left}: a hint that no context token "
                                                          "names and no `literal_text` row of form-fill-rules.json covers (E10)"))
        return
    ops.append((item.node, "set", text, item.path))
    fills.append(Fill(item.path, item.raw, text, "token"))


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
    literal, deferred = [], []
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
        if item.kind == "literal":
            literal.append(item.path)
            continue
        if item.kind == "token":
            text, missing = item.raw, []
            for token, key in rules()["context_tokens"].items():
                if token in text:
                    given = getattr(ctx, key, "")
                    if given:
                        text = text.replace(token, str(given))
                    else:
                        missing.append(f"the contract's token {token} has no key `{key}` in the context")
            if any(token in text for token in rules().get("form_field_tokens", {})):
                deferred.append((item, text, missing))      # a token the form's own field gives: known once every field has its value
                continue
            _finish_token(item, text, missing, ops, fills, unfillable)
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
        if item.kind == "embedded":
            unfillable.append(Unfillable(item.path, item.raw, "a hint inside a value that no context token names and no `literal_text` row of "
                                                              "form-fill-rules.json covers: the filler writes no value it cannot fill (E10)"))
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
        if gen.world:                                  # a field that names an id of the world (`case id`): the world's own, when it holds one
            ids = getattr(ctx, gen.world, [])
            at = _row_number(item.path) - 1
            if isinstance(ids, list) and 0 <= at < len(ids) and isinstance(ids[at], str) and ids[at].strip():
                value = ids[at]
        value = _issued(value, ctx)
        ops.append((item.node, "set", value, item.path))
        fills.append(Fill(item.path, item.raw, value, gen.rule))
    for item, text, missing in deferred:
        given_by = {path: value for _node, action, value, path in ops if action == "set"}
        for token, field_path in rules()["form_field_tokens"].items():
            if token not in text:
                continue
            value = given_by.get(field_path)
            fallback_key = rules().get("context_fallback_tokens", {}).get(token)       # the form has no plain value: the world's own, when a row names its key
            fallback = getattr(ctx, fallback_key, "") if fallback_key else ""
            if isinstance(value, str) and value.strip() and not HINT.search(value):
                text = text.replace(token, value)
            elif isinstance(fallback, str) and fallback.strip():
                text = text.replace(token, fallback)
            else:
                known = f"; and the context has no key `{fallback_key}` value for it" if fallback_key else ""
                missing.append(f"the contract's token {token} reads the field `{field_path}` of this form, which gives no plain value (it was {value!r}){known}")
        _finish_token(item, text, missing, ops, fills, unfillable)
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
    return Filled(contract, word_text, variant, text, handoff.parse(text).data, fills, unfillable, left, literal, list(survey.kept))


def write_dispatch_form(task_root, dispatch_id: str, contract: str, ctx: FillContext, verdict, *, overrides=None) -> Path:
    """`<task_root>/work/handoffs/<dispatch_id>.yaml`: the form of `contract` filled in its base variant, the file a dispatch's role would
    leave. Raises NotFillable (never writes a half-filled form) and ValueError for a dispatch id that is not one plain file name."""
    if not DISPATCH_ID.fullmatch(str(dispatch_id)):
        raise ValueError(f"dispatch id {dispatch_id!r} is not one plain file name (letters, digits, `.`, `_`, `-`)")
    filled = fill_form(contract, replace(ctx, dispatch_id=str(dispatch_id)), verdict=verdict, overrides=overrides).require()
    path = Path(task_root) / "work" / "handoffs" / f"{dispatch_id}.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(filled.text.encode("utf-8"))
    return path


# ------------------------------------------------------------------------------------------------ the outputs of the stages
@dataclass
class FilledArtifact:
    output: str
    files: dict            # path inside the world -> text; `project:<rel>` for a project-level file
    fills: list
    unfillable: list
    left_for_code: list

    def require(self) -> "FilledArtifact":
        """The output itself, or `NotFillable` naming the first field it could not fill (and how many more)."""
        if self.unfillable:
            first = self.unfillable[0]
            more = f" (and {len(self.unfillable) - 1} more)" if len(self.unfillable) > 1 else ""
            raise NotFillable(self.output, first.path, first.hint, first.why + more)
        return self


@dataclass(frozen=True)
class ByCode:
    output: str
    writer: str            # artifact-writers.json: the code that writes it; the filler does not


@dataclass(frozen=True)
class NotCovered:
    output: str
    why: str               # the row of `not_covered` in form-fill-rules.json


class Unclassified(Exception):
    """An output the table cannot place (E23): no writer, or a role-written output with no template and no `not_covered` row."""

    def __init__(self, output: str, why: str):
        super().__init__(f"output {output}: {why}")
        self.output, self.why = output, why


_REFERENCE_CACHE: dict = {}


def _reference(name: str) -> dict:
    """A reference table of the package, read loud (a missing or broken file raises: an empty table must never read as "no outputs")."""
    if name not in _REFERENCE_CACHE:
        _REFERENCE_CACHE[name] = json.loads((REFERENCES / name).read_text(encoding="utf-8"))
    return _REFERENCE_CACHE[name]


def stage_outputs() -> list:
    """`[(stage id, output name)]` read out of references/stages.json: every `outputs` entry and every `optional_dispatches[].output`, in the
    file's order, a pair once. Never a literal list."""
    pairs = []
    for stage in _reference("stages.json")["stages"]:
        names = list(stage.get("outputs") or []) + [d["output"] for d in stage.get("optional_dispatches") or []
                                                    if isinstance(d, dict) and d.get("output")]
        for name in names:
            if (stage["id"], name) not in pairs:
                pairs.append((stage["id"], name))
    return pairs


def writer_of(output: str) -> str:
    """The `writer` artifact-writers.json names for the output; `Unclassified` when it names none (never a default)."""
    entry = (_reference("artifact-writers.json").get("artifacts") or {}).get(output)
    writer = entry.get("writer") if isinstance(entry, dict) else None
    if not isinstance(writer, str) or not writer.strip():
        raise Unclassified(output, "no writer in artifact-writers.json")
    return writer


LANG = "<lang>"


def _key_of(output: str):
    """The key of `artifact_templates` that shapes the output: its own name, or the one row that names a family (`test_file:<lang>`:
    the text after the head and before the tail is the language). None when no row shapes it."""
    templates = rules()["artifact_templates"]
    if output in templates:
        return output
    for key in templates:
        if LANG in key:
            head, tail = key.split(LANG, 1)
            if output.startswith(head) and output.endswith(tail) and len(output) > len(head) + len(tail):
                return key
    return None


def _lang_of(output: str) -> str:
    key = _key_of(output)
    if not key or LANG not in key:
        return ""
    head, tail = key.split(LANG, 1)
    return output[len(head):len(output) - len(tail)]


def test_file_languages(source: dict) -> list:
    """THE ONE reader of the languages `test_file:<lang>` is walked for (F5, axis 34: the stage-output walk and the reverse walk of
    test_field_producers.py both call it). `source` is the `languages_source` row of `fixtures/form-rounds.json`: `file` and `sections`
    name the table of languages the package already holds (`references/detectors.json`: `assertion_probes`, `assertion_probes_ast`),
    `runner_keys` names the file whose object entries are runner keys (`references/case-markers.json`). A language with no marker form
    is walked too: it comes back `Unfillable` (E9), never skipped. An unreadable language file raises, never "no languages"."""
    names = []
    table = _reference(Path(source["file"]).name)
    for section in source["sections"]:
        names += list(table.get(section) or {})
    names += _runner_keys(source)
    return sorted(dict.fromkeys(names))


def _runner_keys(source: dict) -> list:
    """The runner keys the `runner_keys` file of `source` names (object entries); none when the row names no file or the file cannot be read."""
    if not source.get("runner_keys"):
        return []
    try:
        markers = json.loads((REFERENCES / Path(source["runner_keys"]).name).read_text(encoding="utf-8"))
        return [k for k, v in markers.items() if isinstance(v, dict)]
    except Exception:                                   # said by every row of the family: `marker_form` names the file
        return []


def reverse_walk_languages(source: dict) -> tuple:
    """`(names, notes)` for the reverse walk: `test_file_languages` with every runner key collapsed onto the language the data already links
    it to - a `languages` row `{"like": <language>}` of a `test_file:<lang>` template row - so one file and one refusal is ONE ledger row
    (`@pytest` is the Python file). A runner key with no such link, or one whose language is not walked, is walked as before and `notes`
    (name -> why) says so: the row prints it. No pair is written in this code."""
    names = test_file_languages(source)
    links = {}
    for key, row in rules()["artifact_templates"].items():
        table = row.get("languages") if LANG in key and isinstance(row.get("languages"), dict) else {}
        for lang, entry in table.items():
            if isinstance(entry, dict) and isinstance(entry.get("like"), str) and entry["like"].strip():
                links[lang] = entry["like"]
    runner = set(_runner_keys(source))
    out, notes = [], {}
    for name in names:
        target = links.get(name)
        if target and target != name and target in names:
            continue                                    # the runner key of a language that is walked: the same file
        out.append(name)
        if name in runner:
            notes[name] = (f"runner key `{name}` has no `like` link to a walked language in the template rows, so it is walked on its own"
                           if not target else f"runner key `{name}` links to `{target}`, which is not a walked language, so it is walked on its own")
    return out, notes


def marker_form(lang: str, row: dict) -> tuple:
    """`(the decorator that binds a test to its case, "")` read out of `references/case-markers.json`, or `(None, why)` naming the file and
    the language: the file missing, not JSON, no entry for the language (`row["marker_key"]` maps a language to the runner key the
    file names it by), an entry with an empty marker form, or an empty decorator prefix. Never a default marker (E9)."""
    name = row.get("markers", "references/case-markers.json")
    try:
        data = json.loads((REFERENCES / Path(name).name).read_text(encoding="utf-8"))
    except Exception as exc:
        return None, f"{name} cannot be read ({type(exc).__name__}: {exc}): no marker form for the language {lang}"
    if not isinstance(data, dict):
        return None, f"{name} is not a JSON object: no marker form for the language {lang}"
    key = (row.get("marker_key") or {}).get(lang, lang)
    entry = data.get(key)
    if not isinstance(entry, dict):
        return None, f"{name} has no marker form for the language {lang} (no entry `{key}`)"
    case, prefix = entry.get("case"), data.get("decorator_prefix")
    if not isinstance(case, str) or not case.strip():
        return None, f"{name}: the entry `{key}` has an empty marker form for the language {lang} (no `case` name)"
    if not isinstance(prefix, str) or not prefix.strip():
        return None, f"{name}: `decorator_prefix` is empty, so the language {lang} has no marker form"
    return prefix + case, ""


def language_body(lang: str, row: dict) -> tuple:
    """`({"file_name", "template"}, "")` for the language from the `languages` rows of the template row (a row `{"like": <language>}` is
    that language's, one hop), or `(None, why)` naming the language: a language no row writes a body for is never given another
    language's file (F1, axis 34: no hidden road for Python)."""
    table = row.get("languages") if isinstance(row.get("languages"), dict) else {}
    entry = table.get(lang)
    if isinstance(entry, dict) and entry.get("like"):
        entry = table.get(entry["like"])
    if not isinstance(entry, dict) or not str(entry.get("file_name") or "").strip() or not str(entry.get("template") or "").strip():
        return None, f"form-fill-rules.json has no body row for the language {lang} (`languages.{lang}`): the filler writes no test file it has no row for"
    return {"file_name": entry["file_name"], "template": entry["template"]}, ""


def row_fields(spec: dict) -> tuple:
    """`({field: RowField}, "")` read at the call from the module the row names (`from: <module>.<attribute>`), or `(None, why)` naming
    the module: not importable, no such attribute, not a mapping, or empty. Never a copied list (AR-13, axis 34)."""
    module, _, attr = spec["from"].rpartition(".")
    try:
        found = getattr(importlib.import_module(module), attr)
    except Exception as exc:
        return None, f"module {module} cannot supply {spec['from']} ({type(exc).__name__}: {exc})"
    if not isinstance(found, dict) or not found:
        return None, f"module {module}: {spec['from']} is empty or not a mapping, so the row has no field to fill"
    return found, ""


def _add_row_fields(output: str, spec: dict, tree: dict, unfillable: list) -> None:
    """Put every field of the module's list into the first row of `tree[spec["at"]]`: the value from `spec["shapes"]` for a field whose
    shape the module cannot give (a list of objects), the first of its closed `values`, else its own `what` as a hint the rules fill.
    A `shapes` key naming a field the module no longer has is an `Unfillable` (the table never outlives the list)."""
    found, why = row_fields(spec)
    if found is None:
        unfillable.append(Unfillable(spec["from"], "", why))
        return
    shapes = spec.get("shapes") or {}
    for name in shapes:
        if name not in found:
            unfillable.append(Unfillable(f"{spec['at']}[0].{name}", "", f"the rules give a shape for `{name}`, which {spec['from']} does not list"))
    rows = tree.get(spec["at"])
    if not isinstance(rows, list) or not rows or not isinstance(rows[0], dict):
        unfillable.append(Unfillable(spec["at"], "", f"the template of {output} has no row at `{spec['at']}[0]` to put the fields in"))
        return
    for name, field_spec in found.items():
        values = getattr(field_spec, "values", ())
        if name in shapes:
            rows[0][name] = json.loads(json.dumps(shapes[name]))
        elif values:
            rows[0][name] = values[0]
        else:
            rows[0][name] = f"<{getattr(field_spec, 'what', name)}>"


def required_of(output: str) -> list:
    """The paths the broken variant may remove, in order: the fields of the module a row names (read at the call), then the row's own
    `required`. The first one is what the table removes (E7)."""
    row = _row_of(output)
    spec = row.get("row_fields")
    found = row_fields(spec)[0] if spec else None
    return [f"{spec['at']}[0].{name}" for name in (found or {})] + list(row.get("required") or [])


def classify(output: str) -> str:
    """`"code"` (the writer is code), `"role"` (a role writes it and a row of `artifact_templates` shapes it) or `"not_covered"` (a role
    writes it and a row of `not_covered` says why the filler cannot); anything else raises `Unclassified`.

    A sub-kind (a template row with `subkind_of`: the plan row, the case, the rows a walker sends) is a thing a role writes by
    definition, whoever writes the file it lands in: it needs no writer row of its own, and its parent must be an output of the stages."""
    key = _key_of(output)
    if key and rules()["artifact_templates"][key].get("subkind_of"):
        if output in rules()["not_covered"]:
            raise Unclassified(output, "a sub-kind, and a not_covered row names it too")
        return "role"
    writer = writer_of(output)
    if not writer.endswith(ROLE_WRITER):
        return "code"
    templated = output in rules()["artifact_templates"]
    named = output in rules()["not_covered"]
    if templated and named:
        raise Unclassified(output, "role-written, and both a template and a not_covered row name it")
    if templated:
        return "role"
    if named:
        return "not_covered"
    raise Unclassified(output, "role-written, neither template nor not_covered")


def _text_of(raw: str, path: str, generic: str, ctx: FillContext, fills: list, unfillable: list):
    """The value of one text of a template: a token from the context, a hint filled by the rules (the SAME rules as forms), or the text
    itself. `raw` is the whole hint (angle brackets included) or a text; an unfillable hint is listed and the text stays as written."""
    tokens = {**rules()["context_tokens"], **rules().get("artifact_tokens", {})}
    if raw.strip() in tokens or (not handoff.is_placeholder(raw) and any(t in raw for t in tokens)):
        text, missing = raw, []
        for token, key in tokens.items():
            if token in text:
                given = getattr(ctx, key, "")
                if given:
                    text = text.replace(token, str(given))
                else:
                    missing.append((token, key))
        if missing:
            unfillable.append(Unfillable(path, raw, "; ".join(f"the contract's token {t} has no key `{k}` in the context" for t, k in missing)))
            return raw
        fills.append(Fill(path, raw, text, "token"))
        return text
    if handoff.is_placeholder(raw) and raw.strip():
        gen, why = _generate(raw, handoff._spec_of_value(generic, raw), path)
        if gen is None:
            unfillable.append(Unfillable(path, raw, why))
            return raw
        fills.append(Fill(path, raw, gen.values[0], gen.rule))
        return gen.values[0]
    return raw


def _json_nodes(node, path: str = "", generic: str = "") -> list:
    """`[(path, generic path, parent, key)]` of every node under `node`, parents first (`a.b[0].c`, generic `a.b[].c`)."""
    out = []
    if isinstance(node, dict):
        for key, value in node.items():
            here = f"{path}.{key}" if path else str(key)
            gen = f"{generic}.{key}" if generic else str(key)
            out.append((here, gen, node, key))
            out += _json_nodes(value, here, gen)
    elif isinstance(node, list):
        for i, value in enumerate(node):
            out.append((f"{path}[{i}]", f"{generic}[]", node, i))
            out += _json_nodes(value, f"{path}[{i}]", f"{generic}[]")
    return out


def _fill_json(output: str, row: dict, ctx: FillContext, overrides: dict, fills: list, unfillable: list) -> str:
    tree = json.loads(json.dumps(row["template"]))
    if row.get("row_fields"):                                 # the fields of a row come from the module that owns the list
        _add_row_fields(output, row["row_fields"], tree, unfillable)
    nodes = _json_nodes(tree)
    known = {n[0] for n in nodes} | {n[1] for n in nodes}
    for key in overrides:
        if key not in known:
            unfillable.append(Unfillable(key, "", f"override names no field of {output}"))
    ops, covered = [], []
    for position, (path, generic, parent, key) in enumerate(nodes):
        found, value = _override_for(path, generic, overrides)
        if any(path.startswith(c + ".") or path.startswith(c + "[") for c in covered):
            if found:
                unfillable.append(Unfillable(path, "", "the override cannot land: an override on a section above it already replaces or removes it"))
            continue
        if found:
            ops.append((position, parent, key, value))
            fills.append(Fill(path, parent[key] if isinstance(parent[key], str) else "", value, "override"))
            covered.append(path)
        elif isinstance(parent[key], str):
            cited = (row.get("cites") or {}).get(path) or (row.get("cites") or {}).get(generic)
            if cited and handoff.is_placeholder(parent[key]) and ID_TOKEN.match(_hint_of(parent[key])):
                issued = (ctx.minted.get(cited) or [""])[0]          # the id another form issued (3.5): never an invented one
                if not issued:
                    unfillable.append(Unfillable(path, parent[key], f"the field cites an id another form issued, and ctx.minted holds no `{cited}` id"))
                else:
                    fills.append(Fill(path, parent[key], issued, "minted"))
                    parent[key] = issued
            else:
                parent[key] = _text_of(parent[key], path, generic, ctx, fills, unfillable)
    for _position, parent, key, value in sorted(ops, key=lambda op: op[0], reverse=True):
        if value is ABSENT:
            del parent[key]
        else:
            parent[key] = value
    return json.dumps(tree, indent=2, ensure_ascii=False) + "\n"


def _cite_variants(output: str, ctx: FillContext) -> list:
    """`cite_hint:<path>` for every field the template says CITES an id another form issued (`cites`: path -> the key of `ctx.minted`),
    where the id the context holds has another prefix than the template's own hint (`P-1` against `TS-n`): the base takes the issued id,
    the variant the hint's own prefix (3.5, the priority of issue and citation). No issued id, or the same prefix: no variant."""
    out = []
    row = _row_of(output)
    lines = row["template"].split("\n") if isinstance(row.get("template"), str) else []
    for path, key in (row.get("cites") or {}).items():
        issued = (ctx.minted.get(key) or [""])[0]
        hints = [_hint_of(m.group(0)) for text in lines if (BODY + text.strip()).startswith(path) for m in HINT.finditer(text)]
        mine = next((ID_TOKEN.match(h).group(1) for h in hints if ID_TOKEN.match(h)), "")
        if issued and mine and issued.split("-")[0] != mine:
            out.append(f"cite_hint:{path}")
    return out


def _fill_md(output: str, row: dict, ctx: FillContext, overrides: dict, fills: list, unfillable: list, variant: str = VARIANT_BASE) -> str:
    """A markdown template: front matter keys (`key: <hint>`) and body lines. A hint in a table row goes through `grammar.escape_cell`.
    Override keys: a front matter key, or `body:<label>` — the FIRST template line (outside the front matter) whose text starts with the
    label; ABSENT removes the line, any other value replaces the whole line."""
    lines = row["template"].split("\n")
    each = row.get("per_case")                          # a line holding this token is written once per id of `ctx.cases` (a report's rows)
    if each and ctx.cases:
        spread = []
        for at, one in enumerate(ctx.cases):             # one row per id: an empty or repeated id is no row (as a directory output)
            if not isinstance(one, str) or not one.strip() or one in ctx.cases[:at]:
                unfillable.append(Unfillable(output, str(one), "an id of the context that is empty or repeated: one row per id"))
        for text in lines:
            if each in text:
                for one in dict.fromkeys(c for c in ctx.cases if isinstance(c, str) and c.strip()):
                    spread.append(text.replace(each, grammar.escape_cell(one) if text.lstrip().startswith("|") else one))   # axis 21
                    fills.append(Fill(text.strip()[:40], each, one, "token"))
            else:
                spread.append(text)
        lines = spread
    front_end = 0
    if lines and lines[0].strip() == "---":
        front_end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), 0)
    labels = {}                                         # line index -> label of the line
    for i, text in enumerate(lines):
        in_front = front_end and i <= front_end
        found = FRONT_KEY.match(text) if in_front and 0 < i < front_end else None
        if found:
            labels[i] = found.group(1)
        elif text.strip() and not in_front:
            labels[i] = BODY + text.strip()
    chosen = {}                                         # line index -> override value
    for key, value in overrides.items():
        if key.startswith(BODY):
            at = next((i for i, label in labels.items() if label.startswith(BODY) and label[len(BODY):].startswith(key[len(BODY):])), None)
        else:
            at = next((i for i, label in labels.items() if label == key), None)
        if at is None:
            unfillable.append(Unfillable(key, "", f"override names no field of {output}"))
        else:
            chosen[at] = value
    out = []
    for i, text in enumerate(lines):
        label = labels.get(i)
        if i in chosen:
            fills.append(Fill(label, text, chosen[i], "override"))
            if chosen[i] is not ABSENT:
                out.append(str(chosen[i]) if label.startswith(BODY) else f"{label}: {chosen[i]}")
            continue
        if label is None or not HINT.search(text):
            out.append(text)
            continue
        table = text.lstrip().startswith("|")
        gen_path = label if not label.startswith(BODY) else f"line{i + 1}"

        def swap(match, label=label, gen_path=gen_path, table=table):
            logged, problems = [], []
            key = next((k for p, k in (row.get("cites") or {}).items() if label.startswith(p)), None)
            as_hint = any(variant == f"cite_hint:{p}" and label.startswith(p) for p in (row.get("cites") or {}))
            if key and not as_hint and ID_TOKEN.match(_hint_of(match.group(0))):
                issued = (ctx.minted.get(key) or [""])[0]
                if not issued:
                    unfillable.append(Unfillable(label, match.group(0), f"the field cites an id another form issued, and ctx.minted holds no `{key}` id"))
                    return match.group(0)
                fills.append(Fill(label, match.group(0), issued, "minted"))
                return grammar.escape_cell(issued) if table else issued
            value = _text_of(match.group(0), gen_path, gen_path, ctx, logged, problems)
            fills.extend(Fill(label, f.hint, f.value, f.rule) for f in logged)
            unfillable.extend(Unfillable(label, u.hint, u.why) for u in problems)
            return grammar.escape_cell(value) if table else str(value)
        out.append(HINT.sub(swap, text))
    return "\n".join(out).rstrip("\n") + "\n"


def fill_artifact(output: str, ctx: FillContext, *, variant: str = VARIANT_BASE, overrides=None):
    """`FilledArtifact` for a role-written output with a template row, `ByCode` for an output code writes, `NotCovered` for one the filler
    does not do (the row says why); `Unclassified` for an output the tables cannot place. Only `base` is a variant of an output in this
    group; any other name raises ValueError. `overrides`: `{path: value | ABSENT}`, the grammar of 3.5 (a JSON path `a.b[0].c` /
    `a.b[].c`; a front matter key or `body:<label>` for markdown); an override that names no field is an `Unfillable` (E20)."""
    kind = classify(output)
    if kind == "code":
        _check_variant(output, variant, [VARIANT_BASE])
        return ByCode(output, writer_of(output))
    if kind == "not_covered":
        _check_variant(output, variant, [VARIANT_BASE])
        return NotCovered(output, rules()["not_covered"][output])
    _check_variant(output, variant, artifact_variants(output, ctx))
    row = _row_of(output)
    overrides = dict(overrides or {})
    fills, unfillable = [], []
    problem = _anchor_problem(row)
    if problem is not None:                                   # the contract line the template stands on is gone: no shape is guessed
        return FilledArtifact(output, {}, fills, [problem], [])
    if row.get("markers"):                                    # a test file: its case marker is the form `case-markers.json` holds (E9)
        marker, why = marker_form(_lang_of(output), row)
        if marker is None:
            return FilledArtifact(output, {}, fills, [Unfillable("marker", _lang_of(output), why)], [])
        body, why = language_body(_lang_of(output), row)
        if body is None:
            return FilledArtifact(output, {}, fills, [Unfillable("body", _lang_of(output), why)], [])
        row = {**row, **body, "template": body["template"].replace("{marker}", marker)}
    if row.get("file_name"):                                  # a directory output (E24): one file per id of the context
        ids = list(getattr(ctx, row.get("ids", "cases")))[:1 if row.get("one") else None]
        if not ids:
            unfillable.append(Unfillable(output, "", f"no ids in ctx for a directory output (ctx.{row.get('ids', 'cases')} is empty)"))
            return FilledArtifact(output, {}, fills, unfillable, [])
        files, seen = {}, set()
        for one in ids:
            if not isinstance(one, str) or not one.strip() or one in seen:
                unfillable.append(Unfillable(output, str(one), "an id of the context that is empty or repeated: one file per id"))
                continue
            seen.add(one)
            at = replace(ctx, **{row.get("id_field", "case_id"): one})
            text = _fill_text(output, row, at, overrides, fills, unfillable, variant)
            files[(row.get("dir") or output) + row["file_name"].replace(row.get("id_token", "<case id>"), one)] = text
        return FilledArtifact(output, files, fills, unfillable, [])
    text = _fill_text(output, row, ctx, overrides, fills, unfillable, variant)
    return FilledArtifact(output, {row.get("path") or output: text}, fills, unfillable, list(row.get("left_for_code") or []))


def _anchor_problem(row: dict):
    """None when the line of the contract the template stands on (`anchor`, a whole line, compared as the heading is written, never by its
    line number) is in the contract file; otherwise the `Unfillable` naming the file and the line (the heading moved or went)."""
    contract, anchor = row.get("contract"), row.get("anchor")
    if not contract or not anchor:
        return None
    try:
        lines = [ln.rstrip() for ln in (ROOT / contract).read_text(encoding="utf-8").splitlines()]
    except Exception as exc:
        return Unfillable("anchor", anchor, f"{contract} cannot be read ({type(exc).__name__}: {exc}): there is no shape to fill from")
    if anchor not in lines:
        return Unfillable("anchor", anchor, f"{contract} has no line {anchor!r}: the heading was renamed or removed, so the template row has no "
                                            "shape to stand on; the filler does not guess one")
    return None


def _row_of(output: str) -> dict:
    """The template row of the output; a row with `row_of` takes every key it does not write from the row it names."""
    row = rules()["artifact_templates"][_key_of(output)]
    return {**rules()["artifact_templates"][row["row_of"]], **row} if row.get("row_of") else row


def _check_variant(output: str, variant: str, names: list) -> None:
    if variant not in names:
        raise ValueError(f"{output}: {variant!r} is not a variant of this output; its variants are {names}")


def artifact_variants(output: str, ctx: FillContext) -> list:
    """`[base]` and, for a template that CITES an id another form issued, `cite_hint:<path>` where the issued id's prefix is not the
    hint's (3.5). The other kinds of output have the base variant only."""
    if classify(output) != "role":
        return [VARIANT_BASE]
    return [VARIANT_BASE] + _cite_variants(output, ctx)


def _fill_text(output: str, row: dict, ctx: FillContext, overrides: dict, fills: list, unfillable: list, variant: str) -> str:
    if row["format"] == "json":
        return _fill_json(output, row, ctx, overrides, fills, unfillable)
    if row["format"] in ("md", "yaml", "text"):               # a yaml or text template is read as lines of text, with no front matter
        return _fill_md(output, row, ctx, overrides, fills, unfillable, variant)
    raise ValueError(f"{output}: the template format {row['format']!r} is not one the filler writes (`json`, `md`, `yaml`)")


def write_outputs(task_root, project_root, result: FilledArtifact) -> list:
    """Write the files of a filled output into the world: a story file under `task_root`, a `project:<rel>` file under
    `<project_root>/qa-factory/<rel>`. Raises NotFillable for a half-filled output (nothing is written) and ValueError for a path that
    would leave its root (E22: the filler writes only inside the world it is given); every file is checked BEFORE the first is written."""
    result.require()
    plan = []
    for rel, text in result.files.items():
        project = rel.startswith("project:")
        base = (Path(project_root) / "qa-factory") if project else Path(task_root)
        inner = rel[len("project:"):] if project else rel
        target = (base / inner).resolve()
        parts = re.split(r"[\\/]", inner)
        if not inner or Path(inner).is_absolute() or inner.startswith(("/", "\\")) or ".." in parts \
                or not target.is_relative_to(base.resolve()) or target == base.resolve():
            raise ValueError(f"{result.output}: the path {rel!r} does not stay inside {base} - the filler writes only inside the world it is given")
        plan.append((target, text))
    written = []
    for target, text in plan:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(text.encode("utf-8"))
        written.append(target)
    return written

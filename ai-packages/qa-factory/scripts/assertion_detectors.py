"""assertion_detectors.py - the ONE reader of `references/detectors.json` `assertion_probes` (B-373).

A library module: no CLI, writes nothing, standard library only, and no import of any runtime of
`probe_by_code` / `red_sandbox` / `validate_artifacts` (they import THIS - FR-17: one reader of one table).

The table says how a test in a language other than Python is probed live: how its declaration, its body
and its assertion forms look, which one-for-one inversion each form has and the failure message that
inversion must fire, and how the runner's stack frames name the test file. It is closed variety, so it
is data (FR-13); the code here only validates it and hands it out.

The reader is STRICT. An unreadable file, an absent key and a malformed entry are three different
refusals (`DetectorsUnreadable`, `DetectorsKeyAbsent`, `DetectorEntryMalformed`), because an unknown is
never reported as "no entry" (FR-41): a probe that read a half-valid table as "this language has no
entry" would send a role to add a row that is already there. Every message names the field and what was
expected (FR-1). Anything that fails is a gap of the factory's data, never a verdict on a test.

  assertion_detectors(path=None) -> {language id: entry}   (validated; regexes are still strings)
  assertion_heads(table=None)    -> [head regex, ...]       (the accessor the other readers use, A11; `table` is
                                                               the validated table, never the raw document)
  assert_line_patterns(path=None) -> [regex, ...]           the `assert_lines` key: which lines of a self-fix
                                                               count as an assertion (B-407 C); a typed error when it
                                                               cannot be read, and ASSERT_LINE_FLOOR is the caller's
  shape_patterns(key, path=None) -> [regex, ...]            a key of plain regexes (`sleep`, `locator`,
                                                               `locator_words`, `negative_code`; B-407 C), same errors
  entry_for_suffix(doc, suffix)  -> (language id, entry) | (None, None)
  grammar_of(entry)              -> (frames, skip_frames, frame_path)   for `reporters.assertion_site`
  declaration_regex(entry, name, helper=False) -> compiled declaration pattern for one name
  fires_matches(fires_as, subject) -> bool          `re.search(fires_as, subject)`, no added flags (L7)
  fires_in(fires_as, text, by_line=True) -> bool    THE one "does this failure text fire" reader: the whole text, and
                                                    (by default) each non-blank line with its leading blanks cut
"""
import json
import os
import re
from pathlib import Path

REL = "references/detectors.json"
KEY = "assertion_probes"
# Tests point the reader at a broken copy through this variable (the way `PROBE_RUN_SUITE` replaces the
# runner); a path given as an argument wins over it.
ENV_FILE = "ASSERTION_DETECTORS_FILE"
DETECTORS_FILE = Path(__file__).resolve().parents[1] / "references" / "detectors.json"
ASSERT_LINES_KEY = "assert_lines"
# What counts as an assertion line when `assert_lines` cannot be read (an older copy of the references next to a
# newer script, a broken file): the same six patterns the shipped key holds. A check on a role's work may only
# over-refuse, never go quiet because a table was missing (B-407 C, E-C4), so the caller falls back to these.
ASSERT_LINE_FLOOR = (r"(?i)assert", r"\bexpect\s*\(", r"(?i)\bshould\b", r"\bverify\s*\(", r"\brequire\.\w+\(",
                     r"\bt\.(Error|Errorf|Fatal|Fatalf|Fail|FailNow)\(")

DECLARATION_STYLES = ("method", "call")
STATEMENT_ENDS = ("semicolon", "semicolon_or_newline")
MATCHER_AT = ("head", "after_args", "second_arg")
FRAME_PATHS = ("path", "basename")
ESCAPES = ("backslash", "double", "none")
NAME = "{name}"

ENTRY_FIELDS = {
    "required": ("suffixes", "lexer", "declaration_style", "test_declaration", "body_open",
                 "helper_declaration", "name_separators", "tail_join", "statement_end", "assertions",
                 "frames", "skip_frames", "frame_path", "compiled", "builds_by_default",
                 "no_rebuild_flags"),
    "optional": ("helper_body_open", "report_separators", "display_name", "conditional_directive",
                 "soft_assert_patterns", "soft_report", "title_tag", "title_template", "title_placeholders",
                 "group_declaration", "group_each_declaration", "each_declaration", "loop_heads"),
}
# EP1-37: the optional fields `test_source.read_file` reads a test file by. A regex field must compile; a field that
# is present and broken is a gap of the data, never "the language has none". Plain regexes (no {name}):
TEST_SOURCE_REGEX_FIELDS = ("title_tag", "group_declaration", "group_each_declaration", "each_declaration", "loop_heads")
# What a refusal shows when a language has no entry: the shape of the row to add (FR-1, FR-2: the door).
ENTRY_SHAPE = (
    '"' + KEY + '": {"<language id>": {"suffixes": [".ext"], "lexer": {"line_comments": ["//"], '
    '"block_comments": [["/*", "*/"]], "strings": [{"open": "\\"", "close": "\\"", "escape": "backslash"}]}, '
    '"declaration_style": "method|call", "test_declaration": "<regex with one {name}>", "body_open": "<regex>", '
    '"helper_declaration": "<regex with one {name}>", "name_separators": ["::"], "tail_join": ".", '
    '"statement_end": "semicolon|semicolon_or_newline", "assertions": [{"head": "<regex>", '
    '"matcher_at": "head|after_args|second_arg", "invert": [{"find": "<regex>", "replace": "<text>", '
    '"fires_as": "<regex of the failure the inverted form must show>"}]}], "frames": ["<regex with groups '
    'path and line>"], "skip_frames": ["<regex>"], "frame_path": "path|basename", "compiled": false, '
    '"builds_by_default": [], "no_rebuild_flags": []}} (optional, for a call-style language whose files are read '
    'to list their tests: "title_tag", "title_template": {"open", "close"}, "title_placeholders": [<regex>], '
    '"group_declaration", "group_each_declaration", "each_declaration", "loop_heads")')


class DetectorsError(ValueError):
    """The assertion-probe table cannot be used. `kind` says which of the three it is."""
    kind = ""


class DetectorsUnreadable(DetectorsError):
    kind = "unreadable"


class DetectorsKeyAbsent(DetectorsError):
    kind = "absent"


class DetectorEntryMalformed(DetectorsError):
    kind = "malformed"

    def __init__(self, field: str, message: str):
        super().__init__(message)
        self.field = field


# --- reading ----------------------------------------------------------------------------------------

def detectors_path(path=None) -> Path:
    return Path(path or os.environ.get(ENV_FILE) or DETECTORS_FILE)


def _document(where: Path, expected: str = KEY):
    """The parsed detectors file, or DetectorsUnreadable (the one place the file is opened)."""
    try:
        return json.loads(where.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as exc:
        raise DetectorsUnreadable(
            f"{REL} cannot be read ({type(exc).__name__}: {str(exc)[:120]}): this is a gap of the factory's data "
            f"({where}), not of the test. Expected: a JSON object with the key `{expected}`") from exc


def assertion_detectors(path=None) -> dict:
    """{language id: entry}, every entry validated. Raises one of the three typed errors."""
    doc = _document(detectors_path(path))
    if not isinstance(doc, dict) or KEY not in doc:
        raise DetectorsKeyAbsent(
            f"{REL} has no `{KEY}` key (found: {', '.join(sorted(doc)[:8]) if isinstance(doc, dict) else 'not an object'}):"
            f" a gap of the factory's data, not of the test. The key holds one entry per language: {ENTRY_SHAPE}")
    table = doc[KEY]
    if not isinstance(table, dict) or not table:
        raise DetectorEntryMalformed(KEY, f"{REL} `{KEY}` must be a non-empty object with one entry per language id, "
                                          f"got {type(table).__name__}")
    entries, seen = {}, {}
    for language, entry in table.items():
        entries[language] = _entry(language, entry)
        for suffix in entries[language]["suffixes"]:
            if suffix in seen:
                raise DetectorEntryMalformed(
                    f"{KEY}.{language}.suffixes",
                    f"{KEY}.{language}.suffixes: {suffix!r} is also claimed by {seen[suffix]!r}; a suffix belongs to "
                    "exactly one entry (which grammar reads a file must never be a guess). Fix the rows in "
                    f"{REL}; this is a gap of the factory's data, not of the test")
            seen[suffix] = language
    return entries


def assertion_heads(table=None) -> list:
    """The head regex of every assertion form of every entry, in table order, without repeats: what
    another reader counts as "this line is an assertion" (B-407's `assert_lines` is unioned with it).

    `table` is the VALIDATED table `assertion_detectors()` returns - `{language id: entry}` - or nothing (the
    shipped table is read). It is NOT the raw `detectors.json` document (the one that holds the key
    `assertion_probes` beside `retry_markers` and the rest): that is refused with a ValueError that says so."""
    table = assertion_detectors() if table is None else table
    if not isinstance(table, dict) or KEY in table or not all(
            isinstance(entry, dict) and isinstance(entry.get("assertions"), list) for entry in table.values()):
        raise ValueError(
            "assertion_heads takes the validated table `{language id: entry}` that `assertion_detectors()` "
            f"returns (every entry holding `assertions`), not the raw {REL} document (the one with the key "
            f"`{KEY}`): call `assertion_heads(assertion_detectors())`, or `assertion_heads()`")
    out = []
    for entry in table.values():
        for form in entry["assertions"]:
            if form["head"] not in out:
                out.append(form["head"])
    return out


def shape_patterns(key: str, path=None) -> list:
    """The regexes of one plain-list key of `detectors.json` (`sleep`, `locator`, `locator_words`, `negative_code`,
    `assert_lines`), validated: a non-empty list of non-empty strings that each compile. The same three refusals
    as `assertion_detectors` (unreadable file, absent key, malformed key), and a partly valid list is malformed as
    a whole - an unknown is never a shorter list (FR-41). Each reader decides what its failure means (the
    direction in which it may err): arch_check keeps today's regex, judge_code asks the question of every test,
    check_self_fixes keeps ASSERT_LINE_FLOOR."""
    doc = _document(detectors_path(path), key)
    if not isinstance(doc, dict) or key not in doc:
        raise DetectorsKeyAbsent(
            f"{REL} has no `{key}` key (found: {', '.join(sorted(doc)[:8]) if isinstance(doc, dict) else 'not an object'}):"
            f" a gap of the factory's data (an older copy of the references?). Expected: a non-empty list of regex strings")
    value = doc[key]
    if not isinstance(value, list) or not value or not all(isinstance(p, str) and p for p in value):
        raise DetectorEntryMalformed(key, f"{REL} `{key}` must be a non-empty list of non-empty regex strings, "
                                          f"got {type(value).__name__}: a gap of the factory's data")
    for pattern in value:
        try:
            re.compile(pattern)
        except re.error as exc:
            raise DetectorEntryMalformed(key, f"{REL} `{key}`: {pattern!r} does not compile ({exc}): a gap of the "
                                              "factory's data") from exc
    return list(value)


def assert_line_patterns(path=None) -> list:
    """The `assert_lines` key: the patterns that make a line of a self-fix's `before`/`after` an assertion line
    (B-407 C). Loads the document itself, the way `assertion_detectors(path)` does; raises the typed error when the
    key cannot be read, and the caller falls back to ASSERT_LINE_FLOOR with a note. Not unioned with
    `assertion_heads()` here: the union is the caller's, because `assertion_heads` has its own failure."""
    return shape_patterns(ASSERT_LINES_KEY, path)


def entry_for_suffix(table, suffix: str) -> tuple:
    suffix = str(suffix or "").lower()
    for language, entry in table.items():
        if suffix and suffix in entry["suffixes"]:
            return language, entry
    return None, None


# --- one entry's use ----------------------------------------------------------------------------------

def _list_of(value) -> list:
    return [value] if isinstance(value, str) else list(value or [])


def grammar_of(entry: dict) -> tuple:
    """(frames, skip_frames, frame_path) as `reporters.assertion_site` takes them. A fresh list each call:
    the caller owns what it gets."""
    return _list_of(entry["frames"]), _list_of(entry["skip_frames"]), entry["frame_path"]


def soft_patterns(entry: dict) -> list:
    """The entry's `soft_assert_patterns` (the assertion forms that record a failure and let the test go on); `[]` when the
    language declares none. A fresh list each call."""
    return _list_of((entry or {}).get("soft_assert_patterns"))


def soft_report_of(entry: dict) -> tuple:
    """(error_head, after_frame_ok) of the entry's `soft_report`, or (None, []) when the language declares none."""
    report = (entry or {}).get("soft_report")
    if not isinstance(report, dict) or not isinstance(report.get("error_head"), str):
        return None, []
    return report["error_head"], _list_of(report.get("after_frame_ok"))


def declaration_regex(entry: dict, name: str, helper: bool = False):
    """The compiled declaration pattern with `name` escaped in: the data names the shape, `re.escape` keeps
    the title of a test from being read as regex syntax."""
    pattern = entry["helper_declaration" if helper else "test_declaration"]
    return re.compile(pattern.replace(NAME, re.escape(name)))


def fires_matches(fires_as: str, subject: str) -> bool:
    """`re.search(fires_as, subject)` and nothing added: no flags, so an anchor means the start of the
    subject (L7). A row that cannot be compiled is a gap, so it never matches."""
    try:
        return re.search(fires_as, subject or "") is not None
    except re.error:
        return False


def fires_in(fires_as: str, text: str, by_line: bool = True) -> bool:
    """THE one definition of "the failure text fires `fires_as`" (AR-13): `fires_matches` on the whole text, and with
    `by_line` also on each non-blank line, leading whitespace cut, so a `^` binds to the start of a LINE (a Playwright
    report opens with a header and its own `Error: <msg>` line; the library's `expect(received)...` line is indented after
    them). A code frame echo stays out by its `> 12 |` prefix, not by the anchor. `by_line=False` is the whole text only: the
    caller passes it for the AUTHOR's own message, whose lines must not be able to fire a detector (AR-28)."""
    text = str(text or "")
    if fires_matches(fires_as, text):
        return True
    return by_line and any(fires_matches(fires_as, line.lstrip()) for line in text.splitlines() if line.strip())


def top_level_alternatives(pattern: str) -> list:
    """The alternatives of `pattern` split at the `|` that sit outside any group, class or escape."""
    parts, depth, in_class, start, index = [], 0, False, 0, 0
    while index < len(pattern):
        char = pattern[index]
        if char == "\\":
            index += 2
            continue
        if in_class:
            in_class = char != "]"
        elif char == "[":
            in_class = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "|" and depth == 0:
            parts.append(pattern[start:index])
            start = index + 1
        index += 1
    parts.append(pattern[start:])
    return parts


def anchored(pattern: str) -> bool:
    """Every top-level alternative starts with `^` (after the global flags group, if there is one), and `^`
    means the start of the SUBJECT: a global `m` flag makes it match at every line, which is exactly the
    code-frame echo an anchor exists to keep out (L7), so such a pattern is not anchored."""
    flags = re.match(r"^\(\?([aiLmsux]+)\)", pattern)
    if flags and "m" in flags.group(1):
        return False
    body = pattern[flags.end():] if flags else pattern
    return all(alt.startswith("^") for alt in top_level_alternatives(body))


# --- validation ---------------------------------------------------------------------------------------

def _bad(language: str, path: str, message: str, row_id: str = ""):
    field = f"{KEY}.{language}.{path}"
    where = f"{field} ({row_id})" if row_id else field
    return DetectorEntryMalformed(field, f"{where}: {message}. Fix the row in {REL}; this is a gap of the "
                                         "factory's data, not of the test")


def _regex(language: str, path: str, pattern, row_id: str = "", with_name: bool = False):
    if not isinstance(pattern, str) or not pattern:
        raise _bad(language, path, f"must be a non-empty regex string, got {pattern!r}", row_id)
    probe = pattern
    if with_name:
        if pattern.count(NAME) != 1:
            raise _bad(language, path, f"must hold exactly one {NAME} (got {pattern.count(NAME)})", row_id)
        probe = pattern.replace(NAME, re.escape("x"))
    try:
        return re.compile(probe)
    except re.error as exc:
        raise _bad(language, path, f"does not compile ({exc})", row_id) from exc


def _strings(language: str, path: str, value, *, allow_empty: bool = True) -> list:
    if not isinstance(value, list) or not all(isinstance(v, str) and v for v in value) or \
            (not allow_empty and not value):
        raise _bad(language, path, "must be a list of non-empty strings" + ("" if allow_empty else " (not empty)"))
    return value


def _lexer(language: str, value) -> dict:
    if not isinstance(value, dict):
        raise _bad(language, "lexer", "must be an object {line_comments, block_comments, strings}")
    extra = sorted(set(value) - {"line_comments", "block_comments", "strings", "regex_literal"})
    if extra:
        raise _bad(language, "lexer", f"unknown field(s) {', '.join(extra)}")
    _strings(language, "lexer.line_comments", value.get("line_comments", []))
    blocks = value.get("block_comments", [])
    if not isinstance(blocks, list) or not all(isinstance(b, list) and len(b) == 2 and all(
            isinstance(x, str) and x for x in b) for b in blocks):
        raise _bad(language, "lexer.block_comments", "must be a list of [open, close] pairs of non-empty strings")
    strings = value.get("strings")
    if not isinstance(strings, list) or not strings:
        raise _bad(language, "lexer.strings", "must be a non-empty list of {open, close, escape}")
    for index, item in enumerate(strings):
        if not isinstance(item, dict) or not {"open", "close", "escape"} <= set(item) \
                or set(item) - {"open", "close", "escape", "multiline"} or not (
                isinstance(item["open"], str) and item["open"] and isinstance(item["close"], str) and item["close"]):
            raise _bad(language, f"lexer.strings[{index}]",
                       "must be {open, close, escape[, multiline]} with non-empty delimiters")
        if item["escape"] not in ESCAPES:
            raise _bad(language, f"lexer.strings[{index}].escape", f"must be one of {', '.join(ESCAPES)}")
        if "multiline" in item and not isinstance(item["multiline"], bool):
            raise _bad(language, f"lexer.strings[{index}].multiline", "must be true or false")
    if "regex_literal" in value:
        _regex_literal(language, value["regex_literal"])
    return value


def _regex_literal(language: str, spec) -> None:
    """The optional `lexer.regex_literal`: a `/`-style literal that is told from a division by what comes before it."""
    path = "lexer.regex_literal"
    keys = {"open", "close", "escape", "class_open", "class_close", "multiline", "after"}
    if not isinstance(spec, dict) or not keys - {"multiline"} <= set(spec) or set(spec) - keys:
        raise _bad(language, path, "must be {open, close, escape, class_open, class_close, after[, multiline]}")
    for key in ("open", "close", "escape", "class_open", "class_close"):
        if not (isinstance(spec[key], str) and len(spec[key]) == 1):
            raise _bad(language, f"{path}.{key}", "must be exactly one character")
    if "multiline" in spec and not isinstance(spec["multiline"], bool):
        raise _bad(language, f"{path}.multiline", "must be true or false")
    after = spec["after"]
    if not isinstance(after, dict) or set(after) != {"chars", "words"} or not isinstance(after["chars"], str) \
            or not isinstance(after["words"], list) or not all(isinstance(w, str) and w for w in after["words"]) \
            or not (after["chars"] or after["words"]):
        raise _bad(language, f"{path}.after", "must be {chars: a string, words: a list of words}, not both empty "
                   "(what makes a `/` open the literal instead of divide)")


def _pair(language: str, base: str, index: int, pair, call_style: bool) -> None:
    path = f"{base}.invert[{index}]"
    row_id = str(pair.get("id") or "") if isinstance(pair, dict) else ""
    if not isinstance(pair, dict) or not {"find", "replace", "fires_as"} <= set(pair) \
            or set(pair) - {"id", "find", "replace", "fires_as"}:
        raise _bad(language, path, "must be {find, replace, fires_as} (and optionally an id), nothing else", row_id)
    if "id" in pair and not (isinstance(pair["id"], str) and pair["id"]):
        raise _bad(language, path + ".id", "must be a non-empty string", row_id)
    find = _regex(language, path + ".find", pair["find"], row_id)
    if not isinstance(pair["replace"], str):
        raise _bad(language, path + ".replace", "must be a string (group references as \\1)", row_id)
    for ref in re.findall(r"\\(\d+)", pair["replace"]):
        if int(ref) > find.groups:
            raise _bad(language, path + ".replace", f"names group {ref}, and `find` has {find.groups}", row_id)
    fires = pair["fires_as"]
    _regex(language, path + ".fires_as", fires, row_id)
    if call_style and not anchored(fires):
        # A jest-style failure text carries a code frame that echoes the mutated statement; only an
        # alternative that is anchored to the start of the subject keeps that echo out (L7).
        raise _bad(language, path + ".fires_as", "every alternative of a call-style row must start with `^`, "
                   "so a code frame echoing the mutated statement can never fire it", row_id)


def _form(language: str, index: int, form, call_style: bool) -> None:
    base = f"assertions[{index}]"
    if not isinstance(form, dict) or set(form) != {"head", "matcher_at", "invert"}:
        raise _bad(language, base, "must be {head, matcher_at, invert}")
    _regex(language, base + ".head", form["head"])
    if form["matcher_at"] not in MATCHER_AT:
        raise _bad(language, base + ".matcher_at", f"must be one of {', '.join(MATCHER_AT)}")
    pairs = form["invert"]
    if pairs is None:
        return
    if not isinstance(pairs, list) or not pairs:
        raise _bad(language, base + ".invert", "must be null (no inversion) or a non-empty list of pairs")
    for position, pair in enumerate(pairs):
        _pair(language, base, position, pair, call_style)


def _frames(language: str, entry: dict) -> None:
    frames = _list_of(entry["frames"]) if isinstance(entry["frames"], (str, list)) else None
    if not frames or not all(isinstance(f, str) for f in frames):
        raise _bad(language, "frames", "must be a regex or a non-empty list of regexes")
    for position, pattern in enumerate(frames):
        rx = _regex(language, f"frames[{position}]", pattern)
        if not {"path", "line"} <= set(rx.groupindex):
            raise _bad(language, f"frames[{position}]", "must name the groups `path` and `line`")
        if entry["frame_path"] == "basename" and "qual" not in rx.groupindex:
            raise _bad(language, f"frames[{position}]", "a frame_path `basename` grammar must name the group `qual` "
                       "(the qualified method name: its package decides which same-named file it is)")
    skip = entry["skip_frames"]
    if not isinstance(skip, (str, list)) or not all(isinstance(s, str) for s in _list_of(skip)):
        raise _bad(language, "skip_frames", "must be a regex or a list of regexes")
    for position, pattern in enumerate(_list_of(skip)):
        _regex(language, f"skip_frames[{position}]", pattern)


def _suffixes(language: str, value) -> list:
    _strings(language, "suffixes", value, allow_empty=False)
    out = []
    for suffix in value:
        low = suffix.lower()
        if not low.startswith(".") or len(low) < 2 or "/" in low or "\\" in low:
            raise _bad(language, "suffixes", f"{suffix!r} must be a file suffix like `.cs`")
        if low == ".py":
            raise _bad(language, "suffixes", "`.py` is never an entry: a Python test is probed by the AST path")
        if low in out:
            raise _bad(language, "suffixes", f"{suffix!r} is listed twice")
        out.append(low)
    return out


def _entry(language: str, entry) -> dict:
    if not isinstance(entry, dict):
        raise _bad(language, "", f"must be an object, got {type(entry).__name__}")
    missing = [k for k in ENTRY_FIELDS["required"] if k not in entry]
    if missing:
        raise _bad(language, missing[0], f"is missing (the entry also lacks: {', '.join(missing[1:]) or 'nothing else'})")
    extra = sorted(set(entry) - set(ENTRY_FIELDS["required"]) - set(ENTRY_FIELDS["optional"]))
    if extra:
        raise _bad(language, extra[0], f"is not a field of an entry (unknown: {', '.join(extra)})")
    out = dict(entry)
    out["suffixes"] = _suffixes(language, entry["suffixes"])
    _lexer(language, entry["lexer"])
    if entry["declaration_style"] not in DECLARATION_STYLES:
        raise _bad(language, "declaration_style", f"must be one of {', '.join(DECLARATION_STYLES)}")
    for key in ("test_declaration", "helper_declaration"):
        _regex(language, key, entry[key], with_name=True)
    for key in ("body_open", "helper_body_open", "display_name", "conditional_directive"):
        if key in entry:
            _regex(language, key, entry[key])
    for key in ("name_separators", "report_separators", "builds_by_default", "no_rebuild_flags"):
        if key in entry:
            _strings(language, key, entry[key])
    if "soft_assert_patterns" in entry:
        # EP1-38: the assertion forms that do not stop a test when they fail (Playwright `expect.soft`). A language that
        # has none leaves the key out; a list that does not compile is a gap of the data, never "no soft form".
        for position, pattern in enumerate(_strings(language, "soft_assert_patterns", entry["soft_assert_patterns"])):
            _regex(language, f"soft_assert_patterns[{position}]", pattern)
    if "soft_report" in entry:
        # EP1-38 F-2: how a soft test's failure text is built (the integrity check of `reporters.failure_frames`)
        report = entry["soft_report"]
        if not isinstance(report, dict) or set(report) - {"error_head", "after_frame_ok"} or not isinstance(report.get("error_head"), str):
            raise _bad(language, "soft_report", "must be an object {error_head: regex, after_frame_ok: [regex]}")
        _regex(language, "soft_report.error_head", report["error_head"])
        for position, pattern in enumerate(_strings(language, "soft_report.after_frame_ok", report.get("after_frame_ok", []))):
            _regex(language, f"soft_report.after_frame_ok[{position}]", pattern)
    for key in TEST_SOURCE_REGEX_FIELDS:
        if key in entry:
            _regex(language, key, entry[key])
    if "title_template" in entry:
        template = entry["title_template"]
        if not isinstance(template, dict) or set(template) != {"open", "close"} or not all(
                isinstance(template[k], str) and template[k] for k in template):
            raise _bad(language, "title_template", "must be an object {open, close} of two non-empty strings")
    if "title_placeholders" in entry:
        for position, pattern in enumerate(_strings(language, "title_placeholders", entry["title_placeholders"])):
            _regex(language, f"title_placeholders[{position}]", pattern)
    if not isinstance(entry["tail_join"], str) or not entry["tail_join"]:
        raise _bad(language, "tail_join", "must be a non-empty string (one space is legal)")
    if entry["statement_end"] not in STATEMENT_ENDS:
        raise _bad(language, "statement_end", f"must be one of {', '.join(STATEMENT_ENDS)}")
    if not isinstance(entry["compiled"], bool):
        raise _bad(language, "compiled", "must be true or false")
    if entry["frame_path"] not in FRAME_PATHS:
        raise _bad(language, "frame_path", f"must be one of {', '.join(FRAME_PATHS)}")
    forms = entry["assertions"]
    if not isinstance(forms, list) or not forms:
        raise _bad(language, "assertions", "must be a non-empty list of {head, matcher_at, invert}")
    for index, form in enumerate(forms):
        _form(language, index, form, entry["declaration_style"] == "call")
    _frames(language, entry)
    return out

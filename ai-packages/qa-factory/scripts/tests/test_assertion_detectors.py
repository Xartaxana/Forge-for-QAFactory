"""assertion_detectors.py: the ONE strict reader of `references/detectors.json` `assertion_probes` (B-373 R2).

What these pin: the shipped table reads; an unreadable file, an absent key and a malformed entry are three
DIFFERENT refusals and a malformed one names its field (and its row); every regex compiles and every rule of
R1 is validated; every `fires_as` matches the message of the inverted form it is for and none of the original
form's own red (the seed table's "must NOT match" column, as a test); `P` - the spec-only shorthand - is
expanded in the data; `assertion_heads` is the accessor the other readers use, and importing the module pulls
in no runtime of the probe. The messages are estimates (measurement M2 replaces them), kept in
fixtures/probe-languages/samples.json.
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from harness import FIXTURES, check, check_eq, check_in, check_not_in, cleanup, finish, temp_dir  # noqa: E402

import assertion_detectors as AD  # noqa: E402

SHIPPED = Path(AD.DETECTORS_FILE)
SAMPLES = json.loads((FIXTURES / "probe-languages" / "samples.json").read_text(encoding="utf-8"))["pairs"]
PY = sys.executable


def shipped_doc() -> dict:
    return json.loads(SHIPPED.read_text(encoding="utf-8"))


def pairs_of(doc: dict):
    """(language, form index, pair index, pair) of every pair of every form."""
    for language, entry in doc["assertion_probes"].items():
        for fi, form in enumerate(entry["assertions"]):
            for pi, pair in enumerate(form["invert"] or []):
                yield language, fi, pi, pair


def reading(directory: Path, doc, name: str = "d.json"):
    """What `assertion_detectors(path)` raises (the class) or returns, for `doc` written to `directory`."""
    path = directory / name
    path.write_text(doc if isinstance(doc, str) else json.dumps(doc), encoding="utf-8")
    try:
        return AD.assertion_detectors(path)
    except AD.DetectorsError as exc:
        return exc


def the_shipped_table(tmp: Path) -> None:
    doc = AD.assertion_detectors()
    check_eq("the shipped table: three languages", sorted(doc), ["csharp", "java", "typescript"])
    check_eq("csharp owns .cs", doc["csharp"]["suffixes"], [".cs"])
    check_eq("java owns .java", doc["java"]["suffixes"], [".java"])
    check_eq("typescript owns the eight JS/TS suffixes",
             doc["typescript"]["suffixes"], [".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".mts", ".cts"])
    # F1: a single-line string that crosses a line break is a lexer error - set on the quote strings of every entry
    for language, entry in doc.items():
        single = {s["open"]: s.get("multiline", True) for s in entry["lexer"]["strings"]}
        check_eq(f"F1: {language}: the `'` and `\"` strings are single-line", (single.get("'", None), single.get('"', None)),
                 (False, False) if "'" in single else (None, False))
    check_eq("F1: the verbatim, raw and template strings stay multi-line",
             [s.get("multiline", True) for e in doc.values() for s in e["lexer"]["strings"] if s["open"] in ('@"', '"""', "`")],
             [True, True, True, True])
    check_in("F1: csharp has a conditional_directive that matches #if/#else and not #region",
             "#", doc["csharp"]["conditional_directive"])
    rx = re.compile(doc["csharp"]["conditional_directive"], re.M)
    check("F1: ...it matches `#if NET6` and `  # else` at the start of a line, not `#region` or a `#if` mid-line",
          bool(rx.search("a\n#if NET6\n")) and bool(rx.search("  # else\n")) and not rx.search("#region x\n") and not rx.search("x #if y"))
    every = [s for entry in doc.values() for s in entry["suffixes"]]
    check("a suffix belongs to exactly one entry, and `.py` to none", len(every) == len(set(every)) and ".py" not in every)
    check_eq("schema_version stays 1", shipped_doc()["schema_version"], 1)
    check("the note is there (assertion_probes_note) and names the estimates", "ESTIMATE" in shipped_doc()["assertion_probes_note"])
    check_eq("the styles: method for C# and Java, call for TypeScript",
             [doc[k]["declaration_style"] for k in ("csharp", "java", "typescript")], ["method", "method", "call"])
    check_eq("compiled: true, true, false", [doc[k]["compiled"] for k in ("csharp", "java", "typescript")], [True, True, False])
    # the other families of the file are untouched (validate_artifacts reads only its own keys)
    for key in ("retry_markers", "broad_status", "broad_status_context", "broad_status_doors", "sleep", "dead_code",
                "skip_markers", "plan_antipatterns"):
        check(f"the family `{key}` is still a list of strings", all(isinstance(x, str) for x in shipped_doc()[key]))
    # every regex of the table really compiles (the reader validated it; here by hand, as a control)
    for language, fi, pi, pair in pairs_of(shipped_doc()):
        for field in ("find", "fires_as"):
            try:
                re.compile(pair[field])
                ok = True
            except re.error:
                ok = False
            check(f"{language} form {fi} pair {pair.get('id')}: {field} compiles", ok)
    # L9: the Java frames carry a `qual` group; L1/L8: the TS grammar
    check_in("java: the frames regex names `qual`", "(?P<qual>", doc["java"]["frames"][0])
    check_eq("java resolves frames by basename", doc["java"]["frame_path"], "basename")
    skip = doc["typescript"]["skip_frames"][0]
    check_in("L1: the Jest frame `(<anonymous>)` is skipped only at the end of the line", "\\(<anonymous>\\)\\s*$", skip)
    check_not_in("L1: the bare `<anonymous>` alternative of the draft is gone", "|<anonymous>", skip.replace("\\(<anonymous>\\)", "").replace("at\\s+<anonymous>", ""))
    jest_frame = "      at Object.<anonymous> (/clone/src/sum.test.ts:11:20)"
    check("L1: a Jest test frame is NOT skipped", re.search(skip, jest_frame) is None)
    check("L1: ... and is read by the first TS frame regex",
          re.search(doc["typescript"]["frames"][0], jest_frame) is not None)
    check("L1: `at new Promise (<anonymous>)` IS skipped", re.search(skip, "      at new Promise (<anonymous>)") is not None)
    check("L1: a bare `at <anonymous>` line IS skipped", re.search(skip, "    at <anonymous>") is not None)
    vitest = " " + chr(0x276F) + " src/sum.test.ts:11:20"  # U+276F built by chr(): only ASCII in the file
    check("L8: a Vitest arrow frame is read by the second TS frame regex",
          re.search(doc["typescript"]["frames"][1], vitest) is not None)
    check_eq("L8: Vitest row names `Calc > adds` are a report separator", doc["typescript"]["report_separators"], [" > "])
    # L6: NUnit alternatives carry (?m); X3's NUnit alternative is scoped
    by_id = {pair["id"]: pair for _l, _f, _p, pair in pairs_of(shipped_doc())}
    for pid in ("N1", "N2", "N3", "N4"):
        check(f"L6: {pid} starts with (?m)", by_id[pid]["fires_as"].startswith("(?m)"), by_id[pid]["fires_as"])
    check_in("L6: X3's NUnit alternative is (?m:...)", "(?m:^\\s*Expected: False", by_id["X3"]["fires_as"])
    # L8: J1/J2 allow a user message; A2 allows `.as()`
    check_in("L8: J1 allows `msg ==> `", "(?:.*? ==> )?", by_id["J1"]["fires_as"])
    check_in("L8: J2 allows `msg ==> `", "(?:.*? ==> )?", by_id["J2"]["fires_as"])
    check_in("L8: A2 allows a bracketed description", "(?:\\[.*?\\]\\s*)?", by_id["A2"]["fires_as"])
    # `P` is a spec-only shorthand: expanded in the data, none left over
    expanded = "(?:org\\.opentest4j\\.AssertionFailedError: |java\\.lang\\.AssertionError: )?"
    for pid in ("J1", "J2", "J3", "J4", "J5", "J6"):
        text = by_id[pid]["fires_as"]
        check(f"{pid}: `P` is expanded (the shorthand's body is there)", text.startswith("^" + expanded), text)
        check(f"{pid}: and no literal `^P` is left in the data", re.search(r"\^P(?![A-Za-z]*\()", text.replace(expanded, "")) is None
              and "^P" not in text.replace("^" + expanded, ""), text)
    check("no `fires_as` anywhere starts with a literal P shorthand",
          not any(re.match(r"\^P[^\w(]|\^P[a-z]|\^P\(\?:\.", p["fires_as"]) for _l, _f, _p, p in pairs_of(shipped_doc())))


def three_distinct_refusals(tmp: Path) -> None:
    """K4: unreadable file / absent key / malformed entry are three different typed refusals (FR-41)."""
    gone = reading(tmp, "{}", "x.json")  # a real file with no key
    check_eq("an absent key is DetectorsKeyAbsent", (type(gone).__name__, getattr(gone, "kind", "")), ("DetectorsKeyAbsent", "absent"))
    check_in("...and says which key, and where the row goes", "`assertion_probes`", str(gone))
    check_in("...and shows the entry shape (the door)", "suffixes", str(gone))
    check_in("...and says it is the factory's data, not the test's", "not of the test", str(gone))
    try:
        AD.assertion_detectors(tmp / "no-such-file.json")
        got = None
    except AD.DetectorsError as exc:
        got = exc
    check_eq("an unreadable file is DetectorsUnreadable", (type(got).__name__, getattr(got, "kind", "")), ("DetectorsUnreadable", "unreadable"))
    check_in("...naming the file", "cannot be read", str(got))
    got = reading(tmp, "{not json", "bad.json")
    check_eq("a file that is not JSON is DetectorsUnreadable too", type(got).__name__, "DetectorsUnreadable")
    got = reading(tmp, ["a", "list"], "list.json")
    check_eq("a JSON file that is not an object is an absent key, not a crash", type(got).__name__, "DetectorsKeyAbsent")
    doc = shipped_doc()
    del doc["assertion_probes"]["csharp"]["frames"]
    got = reading(tmp, doc)
    check_eq("a malformed entry is DetectorEntryMalformed", (type(got).__name__, getattr(got, "kind", "")),
             ("DetectorEntryMalformed", "malformed"))
    check_eq("...naming the field", getattr(got, "field", ""), "assertion_probes.csharp.frames")
    check("the three are different classes",
          len({AD.DetectorsUnreadable, AD.DetectorsKeyAbsent, AD.DetectorEntryMalformed}) == 3
          and issubclass(AD.DetectorsUnreadable, AD.DetectorsError) and issubclass(AD.DetectorEntryMalformed, ValueError))
    doc = shipped_doc()
    doc["assertion_probes"] = {}
    check_eq("an empty table is malformed, not 'no entry'", type(reading(tmp, doc)).__name__, "DetectorEntryMalformed")
    doc["assertion_probes"] = ["x"]
    check_eq("a table that is not an object is malformed", type(reading(tmp, doc)).__name__, "DetectorEntryMalformed")


def malformed_entries(tmp: Path) -> None:
    """Every rule of R1/R2 refuses, naming the field; a row with an id names it too."""
    def corrupt(label: str, fn, field: str, hint: str = "", row: str = "") -> None:
        doc = shipped_doc()
        fn(doc["assertion_probes"])
        got = reading(tmp, doc)
        check_eq(f"{label}: malformed", type(got).__name__, "DetectorEntryMalformed")
        check_eq(f"{label}: names the field", getattr(got, "field", ""), field)
        if hint:
            check_in(f"{label}: says what is wrong", hint, str(got))
        if row:
            check_in(f"{label}: names the row", f"({row})", str(got))
        check_in(f"{label}: and that it is the factory's data", "factory's data", str(got))

    cs = lambda p: p["csharp"]  # noqa: E731
    for key in ("suffixes", "lexer", "declaration_style", "test_declaration", "body_open", "helper_declaration",
                "name_separators", "tail_join", "statement_end", "assertions", "frames", "skip_frames", "frame_path",
                "compiled", "builds_by_default", "no_rebuild_flags"):
        corrupt(f"missing {key}", lambda p, k=key: cs(p).pop(k), f"assertion_probes.csharp.{key}", "is missing")
    corrupt("an unknown field", lambda p: cs(p).update(frames_typo=1), "assertion_probes.csharp.frames_typo", "not a field")
    corrupt("an entry that is not an object", lambda p: p.update(csharp=[1]), "assertion_probes.csharp.", "must be an object")
    corrupt(".py as a suffix", lambda p: cs(p).update(suffixes=[".cs", ".py"]), "assertion_probes.csharp.suffixes", "Python")
    corrupt("a suffix with no dot", lambda p: cs(p).update(suffixes=["cs"]), "assertion_probes.csharp.suffixes", "like `.cs`")
    corrupt("a suffix listed twice", lambda p: cs(p).update(suffixes=[".cs", ".CS"]), "assertion_probes.csharp.suffixes", "twice")
    corrupt("a suffix of two entries", lambda p: p["java"].update(suffixes=[".java", ".cs"]),
            "assertion_probes.java.suffixes", "exactly one entry")
    corrupt("an empty suffix list", lambda p: cs(p).update(suffixes=[]), "assertion_probes.csharp.suffixes", "not empty")
    corrupt("a bad declaration_style", lambda p: cs(p).update(declaration_style="block"),
            "assertion_probes.csharp.declaration_style", "method, call")
    corrupt("test_declaration without {name}", lambda p: cs(p).update(test_declaration="void\\s+x\\s*\\("),
            "assertion_probes.csharp.test_declaration", "exactly one {name} (got 0)")
    corrupt("test_declaration with two {name}", lambda p: cs(p).update(test_declaration="{name}{name}"),
            "assertion_probes.csharp.test_declaration", "(got 2)")
    corrupt("helper_declaration that does not compile", lambda p: cs(p).update(helper_declaration="(void{name}"),
            "assertion_probes.csharp.helper_declaration", "does not compile")
    corrupt("body_open that does not compile", lambda p: cs(p).update(body_open="("), "assertion_probes.csharp.body_open",
            "does not compile")
    corrupt("an optional display_name that does not compile", lambda p: p["java"].update(display_name="@Display("),
            "assertion_probes.java.display_name", "does not compile")
    corrupt("an empty tail_join", lambda p: cs(p).update(tail_join=""), "assertion_probes.csharp.tail_join", "non-empty")
    corrupt("a bad statement_end", lambda p: cs(p).update(statement_end="newline"),
            "assertion_probes.csharp.statement_end", "semicolon")
    corrupt("compiled that is not a boolean", lambda p: cs(p).update(compiled="yes"), "assertion_probes.csharp.compiled",
            "true or false")
    corrupt("name_separators that is not a list of strings", lambda p: cs(p).update(name_separators="::"),
            "assertion_probes.csharp.name_separators", "list of non-empty strings")
    corrupt("builds_by_default with a non-string", lambda p: cs(p).update(builds_by_default=[1]),
            "assertion_probes.csharp.builds_by_default", "list of non-empty strings")
    corrupt("a bad frame_path", lambda p: cs(p).update(frame_path="glob"), "assertion_probes.csharp.frame_path", "path, basename")
    corrupt("no assertions", lambda p: cs(p).update(assertions=[]), "assertion_probes.csharp.assertions", "non-empty list")
    corrupt("a lexer that is not an object", lambda p: cs(p).update(lexer=[]), "assertion_probes.csharp.lexer", "must be an object")
    corrupt("a lexer with no strings", lambda p: cs(p)["lexer"].update(strings=[]), "assertion_probes.csharp.lexer.strings",
            "non-empty list")
    corrupt("a lexer string with a bad escape", lambda p: cs(p)["lexer"]["strings"][0].update(escape="caret"),
            "assertion_probes.csharp.lexer.strings[0].escape", "backslash, double, none")
    corrupt("a lexer string with an empty delimiter", lambda p: cs(p)["lexer"]["strings"][0].update(open=""),
            "assertion_probes.csharp.lexer.strings[0]", "non-empty delimiters")
    corrupt("block comments that are not pairs", lambda p: cs(p)["lexer"].update(block_comments=[["/*"]]),
            "assertion_probes.csharp.lexer.block_comments", "pairs")
    corrupt("an unknown lexer field", lambda p: cs(p)["lexer"].update(raw=1), "assertion_probes.csharp.lexer", "unknown")
    # forms and pairs
    corrupt("a form with no head", lambda p: cs(p)["assertions"][0].pop("head"), "assertion_probes.csharp.assertions[0]",
            "{head, matcher_at, invert}")
    corrupt("a head that does not compile", lambda p: cs(p)["assertions"][0].update(head="Assert("),
            "assertion_probes.csharp.assertions[0].head", "does not compile")
    corrupt("a bad matcher_at", lambda p: cs(p)["assertions"][0].update(matcher_at="tail"),
            "assertion_probes.csharp.assertions[0].matcher_at", "head, after_args, second_arg")
    corrupt("an invert that is an empty list", lambda p: cs(p)["assertions"][0].update(invert=[]),
            "assertion_probes.csharp.assertions[0].invert", "null (no inversion) or a non-empty list")
    corrupt("a find that does not compile", lambda p: cs(p)["assertions"][0]["invert"][0].update(find="^(Assert"),
            "assertion_probes.csharp.assertions[0].invert[0].find", "does not compile", "X1")
    corrupt("a fires_as that does not compile", lambda p: cs(p)["assertions"][0]["invert"][0].update(fires_as="[x"),
            "assertion_probes.csharp.assertions[0].invert[0].fires_as", "does not compile", "X1")
    corrupt("a replace naming a group `find` lacks", lambda p: cs(p)["assertions"][0]["invert"][0].update(replace="\\1x"),
            "assertion_probes.csharp.assertions[0].invert[0].replace", "names group 1", "X1")
    corrupt("a replace that is not a string", lambda p: cs(p)["assertions"][0]["invert"][0].update(replace=None),
            "assertion_probes.csharp.assertions[0].invert[0].replace", "must be a string", "X1")
    corrupt("a pair with an extra key", lambda p: cs(p)["assertions"][0]["invert"][0].update(why="x"),
            "assertion_probes.csharp.assertions[0].invert[0]", "nothing else", "X1")
    corrupt("a pair with no fires_as", lambda p: cs(p)["assertions"][0]["invert"][0].pop("fires_as"),
            "assertion_probes.csharp.assertions[0].invert[0]", "{find, replace, fires_as}", "X1")
    # frames
    corrupt("frames that is empty", lambda p: cs(p).update(frames=[]), "assertion_probes.csharp.frames", "non-empty")
    corrupt("frames with no `line` group", lambda p: cs(p).update(frames=["at (?P<path>.+)"]),
            "assertion_probes.csharp.frames[0]", "`path` and `line`")
    corrupt("frames that do not compile", lambda p: cs(p).update(frames=["(?P<path>"]), "assertion_probes.csharp.frames[0]",
            "does not compile")
    corrupt("a basename grammar without `qual`", lambda p: p["java"].update(
        frames=["^\\s*at\\s+x\\((?P<path>[\\w$]+\\.java):(?P<line>\\d+)\\)"]), "assertion_probes.java.frames[0]", "`qual`")
    corrupt("skip_frames that do not compile", lambda p: cs(p).update(skip_frames=["(x"]),
            "assertion_probes.csharp.skip_frames[0]", "does not compile")
    corrupt("skip_frames that is a number", lambda p: cs(p).update(skip_frames=5), "assertion_probes.csharp.skip_frames",
            "regex or a list")
    # L7: a call-style row must be anchored
    def unanchor(p):
        p["typescript"]["assertions"][0]["invert"][0]["fires_as"] = "expect\\(received\\)\\.to|^Error: x"
    corrupt("L7: a TS alternative without a leading ^", unanchor,
            "assertion_probes.typescript.assertions[0].invert[0].fires_as", "start with `^`", "T1")
    def flagged(p):
        p["typescript"]["assertions"][0]["invert"][0]["fires_as"] = "(?s)^a|b"
    corrupt("L7: the second alternative of (?s)^a|b is not anchored", flagged,
            "assertion_probes.typescript.assertions[0].invert[0].fires_as", "start with `^`", "T1")
    # F3: a global `m` flag makes `^` match at every line - the very echo L7 keeps out - so it is not an anchor
    for flagged in ("(?m)^a|^b", "(?ms)^a|^b", "(?im)^a"):
        def multiline_flag(p, text=flagged):
            p["typescript"]["assertions"][0]["invert"][0]["fires_as"] = text
        corrupt(f"F3: a call-style row with the global flags {flagged[:5]}", multiline_flag,
                "assertion_probes.typescript.assertions[0].invert[0].fires_as", "start with `^`", "T1")
    # F1 (data): the new lexer and entry keys are validated
    corrupt("F1: a lexer string whose `multiline` is not a boolean", lambda p: cs(p)["lexer"]["strings"][2].update(multiline="no"),
            "assertion_probes.csharp.lexer.strings[2].multiline", "true or false")
    # F1b: the optional regex-literal spec of a lexer is validated
    ts = lambda p: p["typescript"]["lexer"]["regex_literal"]  # noqa: E731
    corrupt("F1b: a regex_literal that is not an object", lambda p: p["typescript"]["lexer"].update(regex_literal="/"),
            "assertion_probes.typescript.lexer.regex_literal", "must be {open")
    corrupt("F1b: a regex_literal missing `after`", lambda p: ts(p).pop("after"), "assertion_probes.typescript.lexer.regex_literal", "after")
    corrupt("F1b: a regex_literal with an unknown key", lambda p: ts(p).update(flags="g"), "assertion_probes.typescript.lexer.regex_literal",
            "must be {open")
    for key in ("open", "close", "escape", "class_open", "class_close"):
        corrupt(f"F1b: a regex_literal `{key}` of two characters", lambda p, k=key: ts(p).update({k: "//"}),
                f"assertion_probes.typescript.lexer.regex_literal.{key}", "exactly one character")
    corrupt("F1b: a regex_literal `multiline` that is not a boolean", lambda p: ts(p).update(multiline="no"),
            "assertion_probes.typescript.lexer.regex_literal.multiline", "true or false")
    corrupt("F1b: an `after` set that is empty", lambda p: ts(p).update(after={"chars": "", "words": []}),
            "assertion_probes.typescript.lexer.regex_literal.after", "not both empty")
    corrupt("F1b: an `after` with a non-string word", lambda p: ts(p).update(after={"chars": "(", "words": [1]}),
            "assertion_probes.typescript.lexer.regex_literal.after", "chars")
    doc = shipped_doc()
    del doc["assertion_probes"]["typescript"]["lexer"]["regex_literal"]
    check_eq("F1b: the regex_literal is optional (Java and C# have none)", type(reading(tmp, doc)).__name__, "dict")
    shipped = AD.assertion_detectors()
    check_eq("F1b: only the typescript entry has a regex_literal", {k: "regex_literal" in e["lexer"] for k, e in shipped.items()},
             {"csharp": False, "java": False, "typescript": True})
    spec = shipped["typescript"]["lexer"]["regex_literal"]
    check_eq("F1b: the shipped spec: `/`, escape `\\`, class [ ], single-line", (spec["open"], spec["close"], spec["escape"],
                                                                                spec["class_open"], spec["class_close"], spec["multiline"]),
             ("/", "/", "\\", "[", "]", False))
    check_eq("F1b: the shipped `after` chars are the operator and punctuation set",
             sorted(spec["after"]["chars"]), sorted("(,=:[!&|?{};+-*%<>~^"))
    check_eq("F1b: ...and the words", sorted(spec["after"]["words"]),
             sorted("return typeof instanceof in of new delete void throw case do else yield await".split()))
    check_eq("F1b: entry_for_suffix takes the table by that name", AD.entry_for_suffix(table=shipped, suffix=".cs")[0], "csharp")
    corrupt("F1: a conditional_directive that does not compile", lambda p: cs(p).update(conditional_directive="(#if"),
            "assertion_probes.csharp.conditional_directive", "does not compile")
    doc = shipped_doc()
    doc["assertion_probes"]["csharp"]["assertions"][0]["invert"][0]["fires_as"] = "Assert\\.NotEqual"  # method style: no anchor demanded
    check_eq("an unanchored fires_as is legal for a method-style entry", type(reading(tmp, doc)).__name__, "dict")
    doc = shipped_doc()
    doc["assertion_probes"]["typescript"]["frames"] = doc["assertion_probes"]["typescript"]["frames"][0]  # one regex as a string
    check_eq("frames as one regex string is legal", type(reading(tmp, doc)).__name__, "dict")
    doc = shipped_doc()
    del doc["assertion_probes"]["typescript"]["helper_body_open"]
    del doc["assertion_probes"]["typescript"]["report_separators"]
    check_eq("the optional fields may be absent", type(reading(tmp, doc)).__name__, "dict")
    # EP1-38: `soft_assert_patterns`, the optional list of forms that record a failure and let the test go on
    check_eq("EP1-38: the shipped typescript entry names its soft form as data, the others have none",
             (shipped["typescript"].get("soft_assert_patterns"), "soft_assert_patterns" in shipped["csharp"],
              AD.soft_patterns(shipped["typescript"]), AD.soft_patterns(shipped["java"])),
             (["\\bexpect\\.soft\\s*\\("], False, ["\\bexpect\\.soft\\s*\\("], []))
    check_eq("EP1-38: a copy of the entry without the key is legal (the key is optional)",
             type(reading(tmp, {"assertion_probes": {"typescript": {k: v for k, v in shipped_doc()["assertion_probes"]["typescript"].items()
                                                                     if k != "soft_assert_patterns"}}})).__name__, "dict")
    corrupt("EP1-38: soft_assert_patterns that is not a list", lambda p: p["typescript"].update(soft_assert_patterns="expect"),
            "assertion_probes.typescript.soft_assert_patterns", "list of non-empty strings")
    corrupt("EP1-38: a soft_assert_patterns regex that does not compile",
            lambda p: p["typescript"].update(soft_assert_patterns=["(expect"]),
            "assertion_probes.typescript.soft_assert_patterns[0]", "does not compile")


def fires_as_against_the_samples() -> None:
    """R2 / the seed table: every `fires_as` matches the message of ITS inverted form and none of the original
    form's own red, read by `AD.fires_in` (`re.search`, no flags, on the whole text and on each line - L7). A pair with
    no sample, or a sample for no pair, is a defect of this test's data."""
    table = list(pairs_of(shipped_doc()))
    ids = [pair["id"] for _l, _f, _p, pair in table]
    check_eq("every pair has an id", len(ids), len(set(ids)))
    check_eq("every pair has samples, and every sample belongs to a pair", sorted(ids), sorted(SAMPLES))
    for language, _fi, _pi, pair in table:
        sample = SAMPLES[pair["id"]]
        for text in sample["fires"]:
            check(f"{pair['id']}: fires_as matches its own inverted form's message {text[:40]!r}",
                  AD.fires_in(pair["fires_as"], text), pair["fires_as"])
        for text in sample["not"]:
            check(f"{pair['id']}: fires_as does NOT match the original form's red {text[:40]!r}",
                  not AD.fires_in(pair["fires_as"], text), pair["fires_as"])
        check(f"{pair['id']}: an empty message matches nothing", not AD.fires_in(pair["fires_as"], ""))
    # L7: no flags are added - `^` means the start of the text or of a line; a code frame echo is kept out by its
    # `> 11 |` prefix (the line does not start with the head), not by the anchor
    t1 = next(p for _l, _f, _p, p in table if p["id"] == "T1")
    echo = "Error: boom\n  > 11 |   expect(received).toBe(expected)\n"
    check("L7: a code frame echo line does not fire (its prefix, not the anchor, keeps it out)", not AD.fires_in(t1["fires_as"], echo))
    check("L7: the same statement on a line of its own DOES fire by line",
          AD.fires_in(t1["fires_as"], "boom\n  expect(received).toBe(expected)\n"))
    check("L7: ...and by the whole text only it does not (by_line=False is the whole text)",
          not AD.fires_in(t1["fires_as"], "boom\n  expect(received).toBe(expected)\n", by_line=False))
    check("L7: whole-text first line fires with by_line=False too",
          AD.fires_in(t1["fires_as"], "expect(received).toBe(expected)\n  > 11 |   x", by_line=False))
    check("a pattern that cannot compile never matches (a gap is not a verdict)", not AD.fires_matches("(", "x"))


def the_helpers() -> None:
    check_eq("top-level alternatives respect groups, classes and escapes",
             AD.top_level_alternatives("a|(b|c)|[|]|d\\|e"), ["a", "(b|c)", "[|]", "d\\|e"])
    check("anchored: every alternative starts with ^", AD.anchored("^a|^b"))
    check("anchored: a global flags group is skipped", AD.anchored("(?s)^a|^b"))
    check("anchored: one bare alternative fails", not AD.anchored("^a|b"))
    check("F3: a global m flag is not an anchor, whatever the alternatives", not any(
        AD.anchored(p) for p in ("(?m)^x|^y", "(?ms)^x|^y", "(?mi)^x")))
    check("F3 control: other global flags keep the anchor", AD.anchored("(?s)^x|^y") and AD.anchored("(?i)^x"))
    check("F3 control: a scoped (?m:...) group inside an anchored alternative is not a global flag",
          AD.anchored("^(?m:a|b)"))
    check("anchored: a group's own bar is not an alternative", AD.anchored("^(?:a|b)c"))
    doc = AD.assertion_detectors()
    check_eq("entry_for_suffix: .cs", AD.entry_for_suffix(doc, ".cs")[0], "csharp")
    check_eq("entry_for_suffix: case-insensitive", AD.entry_for_suffix(doc, ".TSX")[0], "typescript")
    check_eq("entry_for_suffix: .py has none", AD.entry_for_suffix(doc, ".py"), (None, None))
    check_eq("entry_for_suffix: no suffix has none", AD.entry_for_suffix(doc, ""), (None, None))
    check_eq("entry_for_suffix: .kt has none", AD.entry_for_suffix(doc, ".kt"), (None, None))
    frames, skip, how = AD.grammar_of(doc["typescript"])
    frames.append("mutated by the caller")
    check_eq("grammar_of hands out a fresh list (the table cannot be changed through it)",
             len(AD.grammar_of(doc["typescript"])[0]), 2)
    check_eq("grammar_of: the path mode", how, "path")
    one = dict(doc["csharp"], frames="^(?P<path>x):(?P<line>1)$")
    check_eq("grammar_of: a single regex string is one pattern, not a list of letters", len(AD.grammar_of(one)[0]), 1)
    rx = AD.declaration_regex(doc["csharp"], "A.b(c)")
    check("declaration_regex: the name is escaped (regex syntax in a name is literal)",
          rx.search("public void A.b(c) (") is not None and rx.search("public void AXb(c) (") is None)
    rx = AD.declaration_regex(doc["typescript"], "adds two numbers")
    check("declaration_regex: a TS title with spaces matches its own quote kinds",
          all(rx.search(f"test({q}adds two numbers{q}, () => {{") for q in ("'", '"', "`")))
    check("declaration_regex: and not another title", rx.search("test('adds', () => {") is None)
    heads = AD.assertion_heads(doc)
    check("assertion_heads: a list of strings", isinstance(heads, list) and all(isinstance(h, str) for h in heads))
    check_in("assertion_heads: carries the TS expect head", "\\bexpect(?:\\.soft)?\\s*\\(", heads)
    check_in("assertion_heads: carries the xUnit head", "\\bAssert\\.Equal\\b", heads)
    check_eq("assertion_heads: no repeats", len(heads), len(set(heads)))
    check_eq("assertion_heads: the same with no argument", AD.assertion_heads(), heads)
    check_eq("assertion_heads: the parameter is the validated `table`", AD.assertion_heads(table=doc), heads)
    # F6: B-407's reader takes the RAW detectors.json document; handing it here is a named refusal, not a crash
    for label, wrong in (("the raw detectors.json document", shipped_doc()), ("a list", ["x"]), ("an entry that is no object", {"csharp": 1}),
                         ("an entry with no assertions", {"csharp": {"suffixes": [".cs"]}})):
        try:
            AD.assertion_heads(wrong)
            got = None
        except ValueError as exc:
            got = str(exc)
        except Exception as exc:  # a crash is what F6 forbids
            got = "CRASH " + type(exc).__name__
        check(f"F6: {label} is a ValueError that names the expected shape",
              bool(got) and not got.startswith("CRASH") and "validated table" in got and "assertion_detectors()" in got, str(got))
    try:
        AD.assertion_heads(shipped_doc())
    except ValueError as exc:
        check_in("F6: the refusal says the raw document is the one that holds the key", "`assertion_probes`", str(exc))
    check_eq("F6: an empty table is a table with no heads", AD.assertion_heads({}), [])
    check_eq("assertion_heads: one per assertion form, in table order",
             heads, [f["head"] for entry in doc.values() for f in entry["assertions"]])


def the_path_and_the_environment(tmp: Path) -> None:
    broken = tmp / "broken.json"
    broken.write_text("{}", encoding="utf-8")
    saved = os.environ.get(AD.ENV_FILE)
    os.environ[AD.ENV_FILE] = str(broken)
    try:
        try:
            AD.assertion_detectors()
            got = None
        except AD.DetectorsKeyAbsent as exc:
            got = exc
        check("the environment variable points the reader at another file", got is not None)
        check_eq("a path given as an argument wins over it", sorted(AD.assertion_detectors(SHIPPED)), ["csharp", "java", "typescript"])
    finally:
        if saved is None:
            os.environ.pop(AD.ENV_FILE, None)
        else:
            os.environ[AD.ENV_FILE] = saved
    check_eq("without it the shipped file is read", AD.detectors_path(), SHIPPED)


def one_reader_no_runtime() -> None:
    """L10: a small stdlib module; importing it pulls in no runtime of probe_by_code, red_sandbox or
    validate_artifacts (B-407 imports it from validate_artifacts: a cycle would break the gate)."""
    code = ("import sys; sys.path.insert(0, %r); import assertion_detectors; "
            "print(sorted(m for m in ('probe_by_code', 'red_sandbox', 'validate_artifacts', 'reporters', 'contract') "
            "if m in sys.modules))" % str(Path(AD.__file__).parent))
    proc = subprocess.run([PY, "-B", "-c", code], capture_output=True, text=True, timeout=60,
                          env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    check_eq("importing assertion_detectors imports none of the probe's runtimes", proc.stdout.strip(), "[]")
    source = Path(AD.__file__).read_text(encoding="utf-8")
    imports = re.findall(r"^(?:import|from)\s+(\w+)", source, re.M)
    check_eq("its imports are the standard library's",
             sorted(set(imports)), ["json", "os", "pathlib", "re"])
    # FR-17: nobody else parses the table's key - the probe and the sandbox read it through this module
    scripts = Path(AD.__file__).parent
    readers = sorted(p.name for p in scripts.glob("*.py") if p.name != "assertion_detectors.py"
                     and "assertion_probes" in p.read_text(encoding="utf-8")
                     and ('["assertion_probes"]' in p.read_text(encoding="utf-8")
                          or ".get(\"assertion_probes\")" in p.read_text(encoding="utf-8")))
    check_eq("no second reader of the key `assertion_probes` in the package's scripts", readers, [])


def ep1_37_the_reading_fields(tmp: Path) -> None:
    """EP1-37: the optional fields `test_source.read_file` reads a file by are validated like the rest: the shipped entry of the
    call-style language carries all six, a field that is there and broken is a gap of the data (malformed, naming the field), and
    an entry without them reads as before (no field is required)."""
    doc = shipped_doc()
    entry = doc["assertion_probes"]["typescript"]
    for field in ("title_tag", "title_template", "title_placeholders", "group_declaration", "each_declaration", "loop_heads"):
        check(f"the shipped call-style entry carries {field}", field in entry)
        check(f"{field} is an optional field of the reader", field in AD.ENTRY_FIELDS["optional"])
    check_in("the test_declaration takes the skip form", "skip", entry["test_declaration"])
    for field, bad in (("title_tag", "@("), ("group_declaration", "["), ("each_declaration", "(("), ("loop_heads", "*"),
                       ("title_template", {"open": "${"}), ("title_template", "${"), ("title_placeholders", ["%s", "("]),
                       ("title_placeholders", "%s")):
        broken = shipped_doc()
        broken["assertion_probes"]["typescript"][field] = bad
        got = reading(tmp, broken, f"broken-{field}.json")
        check(f"a broken {field} ({bad!r}) is refused as malformed", isinstance(got, AD.DetectorEntryMalformed), repr(got)[:120])
        if isinstance(got, AD.DetectorEntryMalformed):
            check_in(f"a broken {field} names the field", f"typescript.{field}", got.field)
    for field in ("title_tag", "title_template", "title_placeholders", "group_declaration", "each_declaration", "loop_heads"):
        plain = shipped_doc()
        del plain["assertion_probes"]["typescript"][field]
        check(f"an entry without {field} still reads", isinstance(reading(tmp, plain, f"plain-{field}.json"), dict))


def main() -> None:
    tmp = temp_dir("qa-detectors-")
    try:
        the_shipped_table(tmp)
        three_distinct_refusals(tmp)
        malformed_entries(tmp)
        fires_as_against_the_samples()
        the_helpers()
        the_path_and_the_environment(tmp)
        one_reader_no_runtime()
        ep1_37_the_reading_fields(tmp)
    finally:
        cleanup(tmp)
    finish("test_assertion_detectors")


if __name__ == "__main__":
    main()

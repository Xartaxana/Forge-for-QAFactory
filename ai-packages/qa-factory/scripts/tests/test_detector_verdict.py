#!/usr/bin/env python3
"""C2-1: `detector_verdict` - the contract of a detector's output, its one reader, its one renderer.

cmp3 (S5): `exit_gate.detector_errors` took the last three lines of a detector's output, and `s5_precheck` printed two
lines per finding plus a marker line, so a role refused for four findings was shown one and came back four times.
Here: `parse` over every shape an output can take (by the contract, cut off at its end, broken, nothing at all, in
the old form), the tags of the refusal at the source, `Record`, the controller's combined refusal (`split_items`,
`refusal_text`), `render` in BYTES with its pointer to the whole list, and the contract test over the six producers:
statically (the AST of every `print` that starts a REJECT) and by running each on its own refusal.
"""
import ast
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import (SCRIPTS, check, check_eq, check_in, check_not_in, cleanup, finish,  # noqa: E402
                     run_script, temp_project)

sys.path.insert(0, str(SCRIPTS))
import detector_verdict as DV  # noqa: E402
from role_cli import PERSON_MARKER, REPAIR_MARKER  # noqa: E402

HEAD = "REJECT — {n} finding(s):"


def block(n: int, label: str = "") -> str:
    head = HEAD.format(n=n)
    return "\n".join([head[:-1] + (" " + label if label else "") + ":"] + [f"- finding {i}" for i in range(1, n + 1)])


def parse_cases() -> None:
    check_eq("exit 0 is no findings", DV.parse(0, "REJECT — 2 stray\n- a\n- b", "")["findings"], [])
    for n in (1, 4, 1000):
        v = DV.parse(1, block(n) + "\n" + REPAIR_MARKER, "")
        check_eq(f"a block of {n}: n findings, whole, no defect, no unmigrated, the marker of the tail",
                 (len(v["findings"]), v["defects"], v["unmigrated"], v["marker"]), (n, [], "", "repair"))
    check_eq("the findings come without their `- `", DV.parse(1, block(2), "")["findings"], ["finding 1", "finding 2"])
    v = DV.parse(1, block(2) + "\nsome tail\n" + block(3) + "\n" + PERSON_MARKER, "")
    check_eq("two blocks: the sum, the marker of the tail after the LAST block", (len(v["findings"]), v["marker"]),
             (5, "person"))
    check_eq("the marker in the context above the header is not the tail's",
             DV.parse(1, REPAIR_MARKER + "\n" + block(1), "")["marker"], "")
    # cut off at its end: what was printed, and the shortfall said
    v = DV.parse(1, block(5).rsplit("\n", 2)[0], "")
    check_eq("a block cut off at the end of the output: the 3 lines printed and one defect", (len(v["findings"]), v["defects"]),
             (3, ["declared 5 finding(s) and printed 3"]))
    v = DV.parse(1, "REJECT — 4 finding(s):", "")
    check_eq("a header with nothing after it: 0 printed, one defect", (v["findings"], v["defects"]),
             ([], ["declared 4 finding(s) and printed 0"]))
    # broken: one unmigrated text, no finding invented, no defect (no label)
    for name, text in (("a block interrupted by a line that is not `- `", "REJECT — 4 finding(s):\n- a\n- b\nfix: x\n- c"),
                       ("an overrun: one more `- ` line after the n-th", "REJECT — 2 finding(s):\n- a\n- b\n- c"),
                       ("a `- ` line after the tail", "REJECT — 1 finding(s):\n- a\ntail\n- c"),
                       ("a REJECT line with no count", "REJECT — 1 finding(s):\n- a\nREJECT: no count here")):
        v = DV.parse(1, text, "")
        check_eq(f"{name}: one unmigrated text, no finding, no defect",
                 (v["findings"], v["defects"], bool(v["unmigrated"]), "\n" in v["unmigrated"]), ([], [], True, False))
    old = "REJECT — 4 finding(s) for the author:\n" + "".join(f"- [c] message {i}\n  fix: do {i}\n" for i in range(4))
    v = DV.parse(1, old, "")
    check_eq("the old S5 form (a `  fix:` line under each finding), 4 findings: ONE unmigrated text holding all four, "
             "not 'declared 4 printed 1'", (v["findings"], v["defects"], all(f"message {i}" in v["unmigrated"] for i in range(4))),
             ([], [], True))
    v = DV.parse(2, "", "usage: x <file>")
    check_eq("exit 2 (outside the contract) with a free text: unreadable with the stderr tail (RH1-5), no finding",
             (v["findings"], v["unmigrated"], v["unreadable"]),
             ([], "", "exit 2, outside the detector contract: usage: x <file>"))
    v = DV.parse(1, "", "")
    check_eq("refused and printed nothing: unreadable, never a pass", (v["findings"], v["defects"], v["unmigrated"], v["unreadable"]),
             ([], [], "", "exit 1, printed nothing"))
    v = DV.parse(1, "REJECT — 0 finding(s):\ntail", "")
    check_eq("a refusal that declares zero findings is a defect, not a pass", (v["findings"], len(v["defects"])), ([], 1))
    v = DV.parse(1, "", block(2))
    check_eq("the header only in stderr: read by the same rules", len(v["findings"]), 2)
    v = DV.parse(1, block(1), "REJECT — 5 finding(s):\n- x")
    check_eq("headers in stdout: stderr is not read", v["findings"], ["finding 1"])
    v = DV.parse(1, "WARN:\n- w1\n- w2\n" + block(2), "")
    check_eq("`- ` lines of a WARN list above the header are context, not findings", v["findings"],
             ["finding 1", "finding 2"])
    # the label of a producer that judged the words at its source
    v = DV.parse(1, block(2, DV.WORDS_AT_SOURCE), "")
    check_eq("the label in the header: words judged at the source", (v["words"], len(v["findings"])), ("source", 2))
    check_eq("no label: the gate judges the words", DV.parse(1, block(2), "")["words"], "gate")
    for name, text, why in (("interrupted", block(4, DV.WORDS_AT_SOURCE).replace("- finding 3", "tail line").replace("- finding 4", ""),
                             "interrupted after 2"),
                            ("overrun", block(2, DV.WORDS_AT_SOURCE) + "\n- finding 3", "followed by one more '- ' line")):
        v = DV.parse(1, text, "")
        check_eq(f"a labelled header and a block {name}: one unmigrated text and one defect that names the block",
                 (v["findings"], bool(v["unmigrated"]), v["words"], len(v["defects"])), ([], True, "source", 1))
        check("...the defect names the head line, where it stands and why", v["defects"][0].startswith(
            "the block 'REJECT — ") and "at line 1 is malformed: declared " in v["defects"][0]
            and v["defects"][0].endswith(why), v["defects"][0])


def tag_cases() -> None:
    """§L-4/§L-5: `WORDS_REFUSED_AT_SOURCE: <id> <cause>` lines ABOVE the header, tied to the finding by the id in its label."""
    lines = ["- [manifest manifest:TC-1:a] one", "- [smell smell:TC-1:b] two", "- [oracle oracle:TC-1:c] three"]
    tag = lambda fid, cause: f"{DV.WORDS_REFUSED_AT_SOURCE} {fid} {cause}"  # noqa: E731
    head = "REJECT — 3 finding(s) " + DV.WORDS_AT_SOURCE + ":"
    v = DV.parse(1, "\n".join([tag("manifest:TC-1:a", "family"), tag("oracle:TC-1:c", "predating"), head] + lines), "")
    check_eq("a family line and a predating line: the named findings are refused, the other is not",
             v["refused"], ["family", "", "predating"])
    check_eq("...and nothing else is reported", (v["defects"], v["unmigrated"], len(v["findings"])), ([], "", 3))
    for name, line in (("no cause", f"{DV.WORDS_REFUSED_AT_SOURCE} smell:TC-1:b"),
                       ("an unknown cause", tag("smell:TC-1:b", "other"))):
        v = DV.parse(1, "\n".join([line, head] + lines), "")
        check_eq(f"a refusal line with {name}: the finding stays refused and one defect says so",
                 (v["refused"], len(v["defects"])), (["", "unreadable", ""], 1))
        check_in(f"...the defect names the line ({name}) and the three known causes",
                 "gives no known cause (family or predating or awaits_answer)", v["defects"][0])
    v = DV.parse(1, "\n".join([tag("oracle:TC-1:c", "awaits_answer"), head] + lines), "")
    check_eq("d1: a refusal line with the cause awaits_answer: that finding is refused with it, no defect",
             (v["refused"], v["defects"]), (["", "", "awaits_answer"], []))
    v = DV.parse(1, "\n".join([tag("nothing:here", "family"), head] + lines), "")
    check_eq("a refusal line naming an id that is not printed: a defect, no finding refused",
             (v["refused"], len(v["defects"])), (["", "", ""], 1))
    check_in("...which says so", "which is not among the findings printed", v["defects"][0])
    # a broken block with a refusal line: the line is read all the same
    v = DV.parse(1, "\n".join([tag("manifest:TC-1:a", "family"), head] + lines + ["- one too many"]), "")
    check_eq("a block broken under a refusal line: one unmigrated text that is refused", (v["findings"], v["unmigrated_refused"]),
             ([], "family"))
    v = DV.parse(1, "\n".join([tag("x:y:z", "predating"), "free text, no header"]), "")
    check_eq("no header at all and a refusal line: unmigrated and refused", (bool(v["unmigrated"]), v["unmigrated_refused"]),
             (True, "predating"))
    check_eq("no refusal line: not refused", DV.parse(1, head + "\n" + "\n".join(lines), "")["refused"], ["", "", ""])
    check_eq("`id_token` leaves an id without whitespace or `]` as it is", DV.id_token("oracle:TC-1:f.py:79"),
             "oracle:TC-1:f.py:79")
    check_eq("...and makes one of those a token", DV.id_token("smell:TC-1:env-assert-a b]c"), "smell:TC-1:env-assert-a_b_c")


def record_cases() -> None:
    r = DV.Record("x: y", script="x", words="source", kind="unmigrated", refused="family")
    check_eq("a Record is a str for printing, JSON and substring matching",
             (isinstance(r, str), json.dumps([r]), "y" in r), (True, '["x: y"]', True))
    check_eq("...and carries its attributes", (r.script, r.words, r.kind, r.refused), ("x", "source", "unmigrated", "family"))
    plain = "plain"
    check_eq("a plain str is read as a finding the gate judges", (getattr(plain, "kind", "finding"), getattr(plain, "words", "gate"),
             getattr(plain, "refused", "")), ("finding", "gate", ""))
    check_eq("one_line makes a finding one physical line", DV.one_line("a\n  b\r\nc "), "a b c")
    v = DV.parse(1, block(2), "")
    check_eq("flatten: findings first", DV.flatten(v), ["finding 1", "finding 2"])
    check_in("flatten: the unmigrated text whole", "unmigrated detector output", DV.flatten(DV.parse(1, "free", ""))[0])


def check_id_cases() -> None:
    """P1-v N0 (spec 20261113-p1v-run-scoreboard-spec.md §2 W0): every record of the exit gate carries the id of the check that produced it,
    in a FIELD (`check`, `tag`), read from the contract's own parse (`labels`), never from the text. Text of every record unchanged."""
    import exit_gate as EG
    import contract as C
    findings = ["[manifest manifest:TC-1:row-fields-missing] one — fix: a", "plain finding, no label",
                "a finding that quotes [grounding R3] in its middle", "[smell smell-id] an id with no colon",
                "[a a:b:c] has [grounding R3] inside"]
    v = DV.parse(1, "REJECT — 5 finding(s):\n" + "\n".join("- " + f for f in findings), "")
    check_eq("(a) parse: `labels` runs parallel to `findings`; a mid-line `[x y]` is no label, an id with no `:` keeps its family",
             (len(v["labels"]) == len(v["findings"]), v["labels"]),
             (True, [("manifest", "manifest:TC-1:row-fields-missing"), None, None, ("smell", "smell-id"), ("a", "a:b:c")]))
    check_eq("(a) parse: no findings (exit 0, unreadable, unmigrated) -> no labels",
             [DV.parse(0, "x", "")["labels"], DV.parse(3, "UNREADABLE: why", "")["labels"], DV.parse(1, "free text", "")["labels"]], [[], [], []])
    recs = EG.detector_records("s5_precheck.py", 1, v, words="gate")
    check_eq("(a) a finding's check is `<producer stem>:<label check>`, `:unlabelled` without a label",
             [r.check for r in recs], ["s5_precheck:manifest", "s5_precheck:unlabelled", "s5_precheck:unlabelled", "s5_precheck:smell", "s5_precheck:a"])
    check_eq("(a) its tag is the third `:`-part of the label's id, `\"\"` for an id with fewer parts or no label",
             [r.tag for r in recs], ["row-fields-missing", "", "", "", "c"])
    check_eq("(b) the TEXT of every record is today's: the producer's prefix and the line, byte for byte",
             [str(r) for r in recs], ["s5_precheck.py: " + f for f in findings])
    broken = DV.parse(1, "REJECT — 1 finding(s) " + DV.WORDS_AT_SOURCE + ":\n- a\n- b\n- c", "")
    zero = DV.parse(1, "REJECT — 0 finding(s):", "")
    check_eq("(a) the unmigrated record, the defect record and the unreadable record name their family",
             [EG.detector_records("x.py", 1, broken, words="source")[-1].check, EG.detector_records("x.py", 1, zero, words="gate")[-1].check,
              EG.detector_records("x.py", 3, DV.parse(3, "UNREADABLE: why", ""), words="gate")[0].check],
             ["x:unmigrated", "x:defect", "x:unreadable"])
    wit = EG.detector_records("work/art.json", 1, v, words="gate", producer="check_witness.py")
    check_eq("(a) check_witness: the check is the producer's (`check_witness:<family>`), `script` stays the artifact (the person's word)",
             (wit[0].check, wit[0].script, wit[1].check), ("check_witness:manifest", "work/art.json", "check_witness:unlabelled"))
    check_eq("(a) `unreadable_record` is `<script stem>:unreadable`, owner file or not",
             [EG.unreadable_record("check_witness.py", "r").check, EG.unreadable_record("s2_check.py", "r", "register.json").check],
             ["check_witness:unreadable", "s2_check:unreadable"])
    # check_id / with_check
    plain, bare, named = "plain", DV.Record("x", script="p/q.py"), DV.Record("x", check="k:v")
    check_eq("check_id: the field, else `<script stem>:unlabelled`, else `unknown` (a plain str, a record built by hand)",
             [DV.check_id(named), DV.check_id(bare), DV.check_id(plain), DV.check_id(DV.Record("x"))], ["k:v", "q:unlabelled", "unknown", "unknown"])
    copy = DV.with_check(DV.Record("t", script="s.py", words="source", kind="unmigrated", refused="family", tag="g"), "exit_gate:scoped")
    check_eq("with_check keeps script, words, kind, refused, tag and the text", (str(copy), copy.script, copy.words, copy.kind, copy.refused, copy.tag, copy.check),
             ("t", "s.py", "source", "unmigrated", "family", "g", "exit_gate:scoped"))
    check_eq("with_check: a record that already has a check keeps it (the same object); a plain str becomes a Record with the defaults",
             (DV.with_check(named, "other:x") is named, DV.with_check("s", "exit_gate:digest").check, DV.with_check("s", "e:d").kind), (True, "exit_gate:digest", "finding"))
    # (c) the tag is a field: the waiting class is today's on a producer record, and a hand-built record with the label in its TEXT has no tag
    waiting = f"[bindings bindings:TC-700:{C.THEN_REMAINDER_WAITS}4] one remainder"
    src = EG.detector_records("s5_precheck.py", 1, DV.parse(1, "REJECT — 1 finding(s) " + DV.WORDS_AT_SOURCE + ":\n- " + waiting, ""), words="source")[0]
    hand = DV.Record("s5_precheck.py: " + waiting, script="s5_precheck.py", words="source")
    check_eq("(c) `_finding_tag_of` reads the field; `word_class` is `refused` for a source-judged waiting Then and `star` for a hand-built text",
             (EG._finding_tag_of(src), EG.word_class(src), EG._finding_tag_of(hand), EG.word_class(hand), EG._finding_tag_of("plain str")),
             (f"{C.THEN_REMAINDER_WAITS}4", "refused", "", "star", ""))
    # (a) one row per family of `all_errors`: its own producers are named right after the call, the detectors name theirs
    names = ("scoped_errors", "detector_errors", "witness_errors", "grounding_errors", "case_identity_errors", "digest_errors",
             "required_outputs_errors", "run_advisers", "_task_pipeline", "_stage_id", "is_halting_handoff")
    saved = {n: getattr(EG, n) for n in names}
    try:
        EG.scoped_errors = lambda *a, **k: ["scoped plain", DV.Record("scoped rec", script="x.py", check="keep:me")]
        EG.detector_errors = lambda *a, **k: [DV.Record("det", script="s5_precheck.py", check="s5_precheck:manifest")]
        EG.witness_errors = lambda *a, **k: [DV.Record("wit", script="a.json", check="check_witness:manifest")]
        EG.grounding_errors = lambda *a, **k: ["grounding plain"]
        EG.case_identity_errors = lambda *a, **k: ["case plain"]
        EG.digest_errors = lambda *a, **k: [DV.Record("digest rec", script="role_digest")]
        EG.required_outputs_errors = lambda *a, **k: ["required plain"]
        EG.run_advisers = lambda *a, **k: []
        EG._task_pipeline, EG._stage_id, EG.is_halting_handoff = (lambda *a: {}), (lambda *a: "S5"), (lambda digest: False)
        blocking, _passed = EG.all_errors("r", "T-1", "digest")
        check_eq("(a) all_errors: scoped / detector / witness / grounding / case_identity / digest / required_outputs each carry their family",
                 [(str(r), r.check) for r in blocking],
                 [("scoped plain", "exit_gate:scoped"), ("scoped rec", "keep:me"), ("det", "s5_precheck:manifest"), ("wit", "check_witness:manifest"),
                  ("grounding plain", "exit_gate:grounding"), ("case plain", "exit_gate:case_identity"), ("digest rec", "exit_gate:digest"),
                  ("required plain", "exit_gate:required_outputs")])
        for name in names[:7]:
            setattr(EG, name, lambda *a, **k: [])
        EG.run_advisers = lambda *a, **k: ["adviser plain"]
        blocking, _passed = EG.all_errors("r", "T-1", "digest")
        check_eq("(a) all_errors: an adviser's refusal carries `exit_gate:adviser`, its text untouched", [(str(r), r.check) for r in blocking],
                 [("adviser plain", "exit_gate:adviser")])
    finally:
        for name, fn in saved.items():
            setattr(EG, name, fn)


def _reader(rows: dict, seen: list = None):
    """A stand-in for `stage_joints.row_for`: `{check id: (row | None, why)}`; an id it does not know is `(None, "no row for <id>")`."""
    def row_for(check, data=None):
        if seen is not None:
            seen.append(check)
        return rows.get(check, (None, f"no row for {check}"))
    return row_for


class _Rows:
    """`with _Rows(rows) as seen:` - `stage_joints.row_for` is replaced by the stand-in (and `rows_for` by a trap: the constructor
    must never use it, C-10), then put back."""
    def __init__(self, rows, reader=None):
        self.rows, self.reader = rows, reader

    def __enter__(self):
        import stage_joints as SJ
        self.sj, self.seen = SJ, []
        self.saved = (SJ.row_for, SJ.rows_for)
        SJ.row_for = self.reader or _reader(self.rows, self.seen)

        def trap(*a, **k):
            raise AssertionError("rows_for must not be read by refusal()")
        SJ.rows_for = trap
        return self.seen

    def __exit__(self, *exc):
        self.sj.row_for, self.sj.rows_for = self.saved


def _stderr_of(fn, *args) -> tuple:
    """`(result or exit code, the stderr text as UTF-8 bytes)` of a call that prints to stderr and may exit."""
    import contextlib
    import io
    buf = io.StringIO()
    with contextlib.redirect_stderr(buf):
        try:
            got = fn(*args)
        except SystemExit as exc:
            got = exc.code
    return got, buf.getvalue().encode("utf-8")


ROW_ONE = {"check": "t:one", "requirement": "Write <T> before you end the dispatch.", "door": "run <ID> now"}


def told_cases() -> None:
    """told-before-work T2 (rows a-f, i of the dispatch spec): `Record.expected` / `.door`, the constructor `refusal`, the renderer
    `spoken`, and the two in-process sinks `hooklib.block` and `stage_guard.deny` (the third, `role_cli.refuse`, is in
    test_role_commands rows g, h). The rows are injected by replacing the reader; no test reads the real stage-joints.json."""
    import hooklib
    import stage_guard
    # (a) T2-1: the two new fields default to "", old constructors are unchanged, `str` is the problem only
    old = DV.Record("x: y", script="x", words="source", kind="unmigrated", refused="family", check="k:v", tag="t")
    new = DV.Record("p", check="k:v", expected="E", door="D")
    check_eq("(a) Record: expected and door default to empty; the old constructor keywords are unchanged",
             (old.expected, old.door, old.check, old.tag, old.kind, str(old)), ("", "", "k:v", "t", "unmigrated", "x: y"))
    check_eq("(a) Record: expected and door are fields; `str` is the problem only, JSON too",
             (new.expected, new.door, str(new), json.dumps([new])), ("E", "D", "p", '["p"]'))
    copy = DV.with_check(DV.Record("p", expected="E", door="D"), "a:b")
    check_eq("(a) with_check keeps expected and door on a copy", (copy.expected, copy.door, copy.check), ("E", "D", "a:b"))
    # (b) T2-2 and T2-3
    with _Rows({"t:one": (ROW_ONE, "")}) as seen:
        got = DV.refusal("t:one", "the plan is missing", fill={"T": "QA-7", "ID": "G-3"})
        check_eq("(b) refusal: the problem is the text, the check is set, expected and door are the row's, filled",
                 (str(got), got.check, got.expected, got.door),
                 ("the plan is missing", "t:one", "Write QA-7 before you end the dispatch.", "run G-3 now"))
        check_eq("(b) refusal reads only through row_for (the rows_for trap was not hit; the reader saw the id once)", seen, ["t:one"])
        got = DV.refusal("t:one", "p")
        check_eq("(b) fill=None leaves the placeholders as written", (got.expected, got.door),
                 ("Write <T> before you end the dispatch.", "run <ID> now"))
        got = DV.refusal("t:one", "p", fill={"T": "", "ID": None, "home": "H"})
        check_eq("(b) a placeholder with no value (empty, None, absent) stays literal, no KeyError", (got.expected, got.door),
                 ("Write <T> before you end the dispatch.", "run <ID> now"))
        check_eq("(b) a non-text problem is its text, never an exception", str(DV.refusal("t:one", 42)), "42")
    # (c) T2 behaviour table: absent row, broken file, a reader that raises, two rows, a sentence-less row
    absent = "(the factory's requirement row t:none could not be read: no row for t:none; this is a factory defect)"
    with _Rows({}):
        got = DV.refusal("t:none", "p")
        check_eq("(c) absent row: the problem, the check, the `could not be read` sentence, no door",
                 (str(got), got.check, got.expected, got.door), ("p", "t:none", absent, ""))
        check_eq("(c) absent row: spoken is the problem, the expected line and the check line, no door line",
                 DV.spoken(got), f"p\n  expected: {absent}\n  check: t:none")
    import stage_joints as SJ
    tmp = Path(tempfile.mkdtemp(prefix="qa-factory-told-"))
    saved = SJ.DATA
    try:
        for label, body in (("absent file", None), ("unparsable file", "{not json"), ("not a v2 file", '{"schema_version": 1}')):
            SJ.DATA = tmp / "stage-joints.json"
            if body is not None:
                SJ.DATA.write_text(body, encoding="utf-8")
            got = DV.refusal("t:none", "p")
            check_eq(f"(c) broken rows file ({label}): no crash, no pass - the I-P text, no door",
                     (str(got), got.check, got.door, got.expected.startswith("(the factory's requirement row t:none could not be read: "),
                      got.expected.endswith("; this is a factory defect)")), ("p", "t:none", "", True, True))
    finally:
        SJ.DATA = saved
        cleanup(tmp)
    def boom(check, data=None):
        raise RuntimeError("x")
    with _Rows({}, reader=boom):
        check_eq("(c) a reader that raises: the I-P text with the exception class, never a crash",
                 DV.refusal("t:none", "p").expected,
                 "(the factory's requirement row t:none could not be read: RuntimeError; this is a factory defect)")
    with _Rows({"t:one": (ROW_ONE, "two rows")}):
        got = DV.refusal("t:one", "p")
        check_eq("(c) two rows (row_for returns the first and a why): the first row's expected and door; the why is not shown",
                 (got.expected, got.door, "two rows" in DV.spoken(got)),
                 ("Write <T> before you end the dispatch.", "run <ID> now", False))
    with _Rows({"t:agg": ({"check": "t:agg", "door": "look at <T>"}, ""), "t:bare": ({"check": "t:bare"}, "")}):
        got = DV.refusal("t:agg", "p", fill={"T": "QA-1"})
        check_eq("(c) a sentence-less row (an aggregator key): expected empty, its own door; this is not the absent case",
                 (got.expected, got.door, DV.spoken(got)), ("", "look at QA-1", "p\n  door: look at QA-1\n  check: t:agg"))
        got = DV.refusal("t:bare", "p")
        check_eq("(c) a row with neither sentence nor door: only the problem and the check", DV.spoken(got), "p\n  check: t:bare")
    with _Rows({"t:one": ({"check": "t:one", "requirement": "see <missing>", "door": ""}, "")}):
        check_eq("(c) an unknown placeholder token stays literal", DV.refusal("t:one", "p", fill={"T": "x"}).expected, "see <missing>")
    # (d) T2-4: spoken
    text = "plain — text\n"
    check_eq("(d) spoken: a plain str is returned unchanged, byte for byte (a trailing newline, a dash)", DV.spoken(text).encode("utf-8"),
             text.encode("utf-8"))
    check_eq("(d) spoken: a Record with no check and nothing to tell is its text unchanged", DV.spoken(DV.Record("only")), "only")
    check_eq("(d) spoken: problem, expected, door, check - in that order, the check line last",
             DV.spoken(DV.Record("p", check="a:b", expected="E", door="D")), "p\n  expected: E\n  door: D\n  check: a:b")
    check_eq("(d) spoken: an empty expected or door line is omitted, not printed blank (S-6)",
             (DV.spoken(DV.Record("p", check="a:b", expected="E")), DV.spoken(DV.Record("p", check="a:b", door="D"))),
             ("p\n  expected: E\n  check: a:b", "p\n  door: D\n  check: a:b"))
    long = "w" * 20000
    check_eq("(d) spoken never truncates", len(DV.spoken(DV.Record("p", check="a:b", expected=long))), len("p\n  expected: \n  check: a:b") + 20000)
    check_eq("(d) spoken: a non-str is its text", DV.spoken(7), "7")
    from driver_machine import match_known
    with _Rows({"t:one": (ROW_ONE, "")}):
        for problem in ("required stages are not done", "a sentence nobody matches", "the plan is missing"):
            got = DV.refusal("t:one", problem)
            check_eq(f"(d) I-R: match_known of spoken equals match_known of the problem ({problem[:20]}...)",
                     match_known(DV.spoken(got)), match_known(str(got)))
        shown = DV.spoken(DV.refusal("t:one", "p", fill={"T": "x", "ID": "y"}))
        check_eq("(d) I-R: no marker is added by refusal or spoken", (REPAIR_MARKER in shown, PERSON_MARKER in shown), (False, False))
    # (e) T2-5: block
    for label, message in (("ascii", "a refusal"), ("dash and a trailing newline", "a — refusal\n\n"), ("empty", "")):
        code, got = _stderr_of(hooklib.block, message)
        check_eq(f"(e) block(str) [{label}]: exit 2 and the stderr bytes are today's, `message.rstrip() + newline + TRAPPED`",
                 (code, got), (2, (message.rstrip() + "\n" + hooklib.TRAPPED + "\n").encode("utf-8")))
    record = DV.Record("p", check="a:b", expected="E", door="D")
    code, got = _stderr_of(hooklib.block, record)
    lines = got.decode("utf-8").splitlines()
    check_eq("(e) block(Record): the spoken text, then TRAPPED as the last line", (code, lines[:-1], lines[-1]),
             (2, ["p", "  expected: E", "  door: D", "  check: a:b"], hooklib.TRAPPED))
    # (f) T2-6: deny
    for label, message in (("ascii", "a refusal"), ("dash", "a — refusal"), ("trailing newline", "x\n")):
        code, got = _stderr_of(stage_guard.deny, message)
        check_eq(f"(f) deny(str) [{label}]: DENY, the stderr bytes are today's `STAGE GUARD: ` + message, LAST_DENIAL is the message",
                 (code, got, stage_guard.LAST_DENIAL["message"]), (stage_guard.DENY, ("STAGE GUARD: " + message + "\n").encode("utf-8"), message))
    record = DV.Record("the dispatch is stopped", check="a:b", expected="the item is absent and could not be written", door="D")
    code, got = _stderr_of(stage_guard.deny, record)
    check_eq("(f) deny(Record): the printed text is spoken, LAST_DENIAL holds the problem only (an exact str)",
             (code, got.decode("utf-8"), type(stage_guard.LAST_DENIAL["message"]) is str, stage_guard.LAST_DENIAL["message"]),
             (stage_guard.DENY, "STAGE GUARD: the dispatch is stopped\n  expected: the item is absent and could not be written\n  door: D\n  check: a:b\n",
              True, "the dispatch is stopped"))
    check_eq("(f) deny(Record): block_match reads the problem, never the expected or door text (`is absent` is in expected only)",
             (stage_guard.block_match(stage_guard.LAST_DENIAL["message"]), stage_guard.block_match(str(record))), ("*", "*"))


COMPOUND = ("3 problems - the request is refused whole, every one is listed:\n"
            "1) decision references stale source revision\n"
            "2) gate before prerequisite completion: already accepted\n   (the second line of item 2)\n"
            "3) author and critic are one identity")


def refusal_cases() -> None:
    items = DV.split_items(COMPOUND)
    check_eq("split_items: the head with 3 items, a continuation line joined to its item", (len(items), "second line" in items[1]),
             (3, True))
    check_eq("split_items: a text with no head is None (a single refusal)", DV.split_items("decision references stale source revision"),
             None)
    check_eq("split_items: a head that declares 3 and 2 items is [] (the head was there: the route is the conductor's)",
             DV.split_items(COMPOUND.rsplit("\n", 1)[0].replace("   (the second line of item 2)\n", "")), [])
    check_eq("refusal_text: the controller's bare text comes back unchanged (the positive control)",
             DV.refusal_text(COMPOUND), COMPOUND)
    check_eq("...and the bare text splits to 3", len(DV.split_items(DV.refusal_text(COMPOUND))), 3)
    wrapped = "story_step finish d1 (exit 2):\nstory_step: refused - " + COMPOUND
    check_eq("refusal_text: the story_step prefix is taken off, the head stands at the start of its line",
             len(DV.split_items(DV.refusal_text(wrapped)) or []), 3)
    check_eq("...and without the normaliser the head is not found at the start of a line, the wrapped text is no compound",
             DV.split_items(wrapped), None)
    cli = "controller decision (exit 2):\n" + json.dumps({"error": COMPOUND})
    check_eq("refusal_text: the JSON `error` of --operation decision gets its real newlines back",
             len(DV.split_items(DV.refusal_text(cli)) or []), 3)
    check_eq("...a line with a `{` that is not JSON stays as it is", DV.refusal_text("a\n{not json\nb"), "a\n{not json\nb")
    check_eq("...and a JSON line without a string `error` stays as it is", DV.refusal_text('{"x": 1}'), '{"x": 1}')


def render_cases() -> None:
    check_eq("render: everything fits - no pointer, no file", DV.render(["a", "b"]), "- a\n- b")
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "findings" / "all.txt"
        lines = ["x" * 98] * 10                         # a block of 10 lines is 10 * 100 + 9 = 1009 bytes
        at = DV.render(lines, max_bytes=1009, full_path=path)
        check_eq("render: exactly max_bytes is not a cut (no pointer, no file)", (at.count("\n") + 1, path.exists()), (10, False))
        over = DV.render(lines, max_bytes=1008, full_path=path)
        check_eq("render: max_bytes - 1: a cut - 9 lines and the pointer, the file holds all 10",
                 (len(over.splitlines()), path.exists() and path.read_text(encoding="utf-8").count("\n- ")), (10, 10))
        check_in("render: the pointer counts what is left and names the file", f"- (+1 more finding(s) — the whole list: {path})", over)
        check("render: the file starts with the count of the list", path.read_text(encoding="utf-8").startswith("# 10 finding(s), "))
        # the ceiling is BYTES, not characters: 8 lines of 400 two-byte characters are 3200 characters, 6400 bytes
        two_bytes = chr(0x44F)      # a letter of two UTF-8 bytes, made by code: the package carries no Cyrillic (FR-30)
        wide = [two_bytes * 400] * 8
        shown = DV.render(wide, full_path=path)
        check_eq("render: a ceiling in bytes (the default 6000): 8 lines of 800 bytes do not fit, 7 do, plus the pointer",
                 (len(shown.splitlines()), "(+1 more" in shown), (8, True))
        check("...and the text without the pointer stays within the ceiling",
              len("\n".join(shown.splitlines()[:-1]).encode("utf-8")) <= DV.FINDINGS_MAX_BYTES, shown[-200:])
        # one line longer than the ceiling, a two-byte character at the border
        long_line = DV.render([two_bytes * 100], max_bytes=51, full_path=path)
        body = long_line.splitlines()[0]
        check("render: a first line longer than the ceiling is cut at a character boundary, marked `…`, valid UTF-8",
              body.startswith("- " + two_bytes) and body.endswith("…") and len(body.encode("utf-8")) <= 51 and "�" not in body, body)
        check_in("...and the pointer says a line was cut", "… marks a line cut here", long_line)
    nopath = DV.render(["a"] * 3, max_bytes=5)
    check_in("render: no path (the story is not known): said in words, nothing written", "the whole list could not be saved: "
             "the story is not known", nopath)
    check_not_in("...and no path is invented", "the whole list:", nopath)
    check_eq("render: nothing to show is an empty text", DV.render([]), "")
    check_eq("render: the word of the pointer is a parameter", "(+1 more line(s)" in DV.render(["a", "b"], max_bytes=4, noun="line"), True)


def joined_cases() -> None:
    """C3-8/9: `joined`, the one-line twin of `render`: AT and BEYOND the ceiling, the edges, the adversarial items."""
    five = ["x" * 10] * 5                                    # 5 * 10 + 4 * 2 = 58 characters joined
    check_eq("joined: exactly the ceiling is not a cut (no pointer, no file)", DV.joined(five, noun="item", where="w", max_chars=58),
             "; ".join(five))
    over = DV.joined(five, noun="item", where="the plan file", max_chars=57)
    check_eq("joined: the ceiling - 1 is a cut: 4 items and ONE trailing part that names the place",
             over, "; ".join(five[:4]) + "; (+1 more item(s) — the whole list: the plan file)")
    check_eq("joined: the pointer is its own `; ` part, so a reader that splits at `; ` never glues it to an item",
             over.split("; ")[-1].startswith("(+1 more"), True)
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "state" / "findings" / "all.txt"
        fits = DV.joined(five, noun="item", full_path=path, max_chars=58)
        check_eq("joined: at the ceiling with a full_path nothing is written (no pointer without a cut)", (path.exists(), "(+" in fits),
                 (False, False))
        cut = DV.joined(five, noun="item", full_path=path, max_chars=57)
        check_eq("joined: past the ceiling the file written by this call holds all 5 and the pointer names it",
                 (path.read_text(encoding="utf-8").count("\n- "), cut.endswith(f"(+1 more item(s) — the whole list: {path})")), (5, True))
        blocked = Path(tmp) / "plain-file"
        blocked.write_text("x", encoding="utf-8")
        bad = DV.joined(five, noun="item", full_path=blocked / "all.txt", max_chars=57)
        check_in("joined: a path that cannot be written: said in words, the shown items stay (FR-41)",
                 "; (+1 more item(s); the whole list could not be saved: ", bad)
        check_eq("...and the shown items are the same 4", bad.startswith("; ".join(five[:4])), True)
        sur = DV.joined(["a" * 30, "b" + chr(0xD800) + "c"], noun="item", full_path=path, max_chars=31)
        check_in("joined: a lone surrogate in an item does not crash the refusal", "(+1 more item(s)", sur)
    check_eq("joined: no items is `none`, with or without a ceiling", (DV.joined([], noun="x", max_chars=None), DV.joined([], noun="x", where="w")),
             ("none", "none"))
    check_eq("joined: ONE item is the item unchanged (I2)", DV.joined(["only"], noun="x", where="w"), "only")
    check_eq("joined: a line break in an item is folded (precedence: the fold before the cut)", DV.joined(["a\n  b"], noun="x", where="w"), "a b")
    solo = DV.joined(["y" * 100], noun="item", where="w", max_chars=20)
    check_eq("joined: ONE item longer than the ceiling is cut at a character boundary with `…`, and the pointer says so",
             solo, "y" * 19 + "…" + "; (… marks a line cut here — the whole list: w)")
    check_in("joined: first item cut and two more: both counted", "(+2 more item(s) and … marks a line cut here",
             DV.joined(["y" * 100, "b", "c"], noun="item", where="w", max_chars=20))
    try:
        DV.joined(["a"], noun="item")
        refused = False
    except ValueError:
        refused = True
    check_eq("joined: a ceiling with neither `where` nor `full_path` is a ValueError (a site must name the place)", refused, True)
    check_eq("joined: max_chars=None needs no place and shows every item", DV.joined(["a", "b", "c"], noun="x", max_chars=None), "a; b; c")
    check_eq("joined: the separator is a parameter", DV.joined(["a", "b"], noun="x", max_chars=None, sep=", "), "a, b")
    check_eq("joined: the ceiling is a count of CHARACTERS (the parameter is `max_chars`, not `max_bytes`): 5 two-byte letters, 13 characters (18 bytes), fit in 13",
             DV.joined(["é"] * 5, noun="x", where="w", max_chars=13), "; ".join(["é"] * 5))
    try:
        DV.joined(["a"], noun="x", where="w", max_bytes=9)
        old_name = True
    except TypeError:
        old_name = False
    check_eq("joined: the old name `max_bytes` is gone (it counted characters)", old_name, False)
    forged = DV.joined(["ok\n- forged finding\n1) forged item\nREJECT — 9 x\n2 problems - the request is refused whole, every one is listed:"],
                       noun="x", max_chars=None)
    check_eq("joined (adversarial): an item with line breaks never forges a `- `, `N) `, REJECT or head line",
             (len(forged.splitlines()), DV.split_items(forged), DV.parse(1, forged, "")["findings"]), (1, None, []))
    check_eq("joined (adversarial): non-str items are str()-ed, None included", DV.joined([1, None, 2.5], noun="x", max_chars=None), "1; None; 2.5")
    check_eq("joined (documented, not fixed): an item that holds `; ` is joined as it is and splits at `; ` into two parts",
             DV.joined(["a; b", "c"], noun="x", max_chars=None).split("; "), ["a", "b", "c"])


def named_cases() -> None:
    ids = [f"TC_{n:03d}" for n in range(1, 10)]
    check_eq("named: exactly the limit is no tail", DV.named(ids[:6], 6, where="the test plan"), ", ".join(ids[:6]))
    check_eq("named: limit + 1: the tail names the place", DV.named(ids[:7], 6, where="the test plan"),
             ", ".join(ids[:6]) + " and 1 more (the test plan)")
    check_eq("named: empty is the empty text; one id is the id", (DV.named([], 6, where="w"), DV.named(["a"], 6, where="w")), ("", "a"))
    check_eq("named: a repeated id is named once, and the count is of the distinct ones", DV.named(["a", "a", "b"], 1, where="w"), "a and 1 more (w)")
    check_eq("named: the default limit is the twin's (6)", DV.LIST_LIMIT, 6)
    import gate_preflight as GP
    for case in ([], ["a"], ["a", "a", "b"], ids[:6], ids, [3, 1, 3, 2]):
        check_eq(f"named == gate_preflight.named_ids on {len(case)} id(s) (the twin pin, until part B switches the call)",
                 DV.named(case), GP.named_ids(case))
    check_eq("...at another limit too", DV.named(ids, 3), GP.named_ids(ids, 3))
    check_eq("named: `sep` joins the shown ids (the default `, ` is the twin's)", (DV.named(ids[:3], 6, where="w", sep="; "), DV.named(ids[:3])),
             ("TC_001; TC_002; TC_003", "TC_001, TC_002, TC_003"))
    check_eq("named: `sep` with a tail: the tail is not joined, it stays the same sentence",
             DV.named(ids[:7], 6, where="w", sep="; "), "; ".join(ids[:6]) + " and 1 more (w)")


def compound_cases() -> None:
    import controller
    twin = controller.Controller._raise_all

    def raised(messages):
        try:
            twin([(ValueError, m) for m in messages])
        except ValueError as exc:
            return str(exc)
        return ""
    for name, messages in (("none", []), ("one", ["a"]), ("two", ["a", "b"]), ("equal ones folded", ["a", "b", "a", "a"]),
                           ("a multi-line one", ["a\nb\n2) c", "d"]), ("all equal", ["x", "x"])):
        check_eq(f"compound == the controller's _raise_all on {name} (the second builder's detector)", DV.compound(messages), raised(messages))
    check_eq("compound: the head constant is the one COMPOUND_HEAD_RE reads",
             DV.COMPOUND_HEAD_RE.match(DV.COMPOUND_HEAD.format(n=2)) is not None, True)
    text = DV.compound(["first", "second"], prefix="T-1:")
    check_eq("compound: with a prefix the head stands FIRST on a line and split_items reads both items",
             (text.splitlines()[:2], DV.split_items(text)), (["T-1:", DV.COMPOUND_HEAD.format(n=2)], ["first", "second"]))
    check_eq("compound: ONE message with a prefix is `<prefix> <message>`, the sentence as before", DV.compound(["m"], prefix="T-1:"), "T-1: m")


def m2_m4_cases() -> None:
    """m2: a LABELLED producer's stray uncounted REJECT is a defect; m4: one builder of the unmigrated sentence."""
    labelled = "REJECT — 1 finding(s) " + DV.WORDS_AT_SOURCE + ":\n- a\nREJECT: no count here"
    v = DV.parse(1, labelled, "")
    check_eq("m2: a labelled output with a stray REJECT: no finding invented, one defect that names the line",
             (v["findings"], v["defects"], bool(v["unmigrated"])), ([], ["the line 3 'REJECT: no count here' has no count"], True))
    v = DV.parse(1, "REJECT — 1 finding(s):\n- a\nREJECT: no count here", "")
    check_eq("m2 (positive control): the same output UNLABELLED: no defect, unmigrated as before", (v["defects"], bool(v["unmigrated"])), ([], True))
    check_eq("m4: the unmigrated sentence of a reader with no records and of the gate (with its exit) come from one builder",
             (DV.flatten(DV.parse(1, "free", ""))[0], DV.unmigrated_text("free", 1)),
             ("unmigrated detector output (it is not in the one-line-per-finding form, so it is shown whole): free",
              "unmigrated detector output (exit 1; it is not in the one-line-per-finding form, so it is shown whole): free"))
    reason = DV.parse(1, "", "")["unreadable"]
    check_eq("m4: the reason of a refusal that printed nothing ends with the one constant", (reason, reason.endswith(DV.PRINTED_NOTHING)),
             ("exit 1, printed nothing", True))


# --- the contract of the six producers --------------------------------------------------------------------------

PRODUCERS = ("sizing.py", "planning_contract.py", "critic_rollcall.py", "s5_precheck.py", "check_coverage.py", "check_witness.py",
             "grounding_table.py", "claim_projector.py", "branch_accounting.py", "stage_joints.py")


def leading_literal(node):
    """`(the first Constant of the expression, the node right after it)` for a str, an f-string or a `+` chain."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value, None
    if isinstance(node, ast.JoinedStr):
        values = node.values
        if values and isinstance(values[0], ast.Constant):
            return values[0].value, (values[1] if len(values) > 1 else None)
        return "", None
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        return leading_literal(node.left)
    return "", None


def static_findings(source: str) -> list:
    """The contract's violations in the REJECT prints of one source: [(line, what)]."""
    bad = []
    for node in ast.walk(ast.parse(source)):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "print" and node.args):
            continue
        text, after = leading_literal(node.args[0])
        if not text.startswith("REJECT"):
            continue
        if any(kw.arg == "file" for kw in node.keywords):
            bad.append((node.lineno, "a REJECT print with file=: the verdict is on stdout"))
        rest = text[len("REJECT — "):] if text.startswith("REJECT — ") else None
        if rest is None:
            bad.append((node.lineno, "a REJECT print that does not start with `REJECT — `"))
        elif not ((rest == "" and isinstance(after, ast.FormattedValue)) or rest[:1].isdigit()):
            bad.append((node.lineno, "a REJECT header with no count"))
    return bad


def contract_static() -> None:
    for name in PRODUCERS:
        found = static_findings((SCRIPTS / name).read_text(encoding="utf-8"))
        check_eq(f"static: {name} has no REJECT print against the contract", found, [])
    check_eq("static: the checker sees a print to stderr", len(static_findings('print("REJECT — 1 x", file=sys.stderr)')), 1)
    check_eq("static: ...a header with a value after the dash passes statically, whatever the value is (the plan name is "
             "told from a count only by the RUN, below)", static_findings('print(f"REJECT — {plan.name} is bad")'), [])
    check_eq("static: ...an old `REJECT: ` header", len(static_findings('print("REJECT: x")')), 1)
    check_eq("static: ...a header joined with `+` that has a count passes, one that has none does not",
             (static_findings('print("REJECT — 2 x" + y)'), len(static_findings('print("REJECT — " + y)'))), ([], 1))
    check_eq("static: ...a counted f-string passes", static_findings('print(f"REJECT — {len(e)} x")'), [])


def run_checks(label: str, script: str, *args, cwd=None, env=None, code: int = 1) -> dict:
    done = run_script(script, *args, cwd=cwd, env=env)
    heads = [line for line in done.stdout.splitlines() if line.startswith("REJECT")]
    check_eq(f"run: {label} exits {code}", done.returncode, code)
    check(f"run: {label}: every REJECT line is `REJECT — <n>`, and there is none on stderr",
          bool(heads) and all(re.match(r"^REJECT — \d+", line) for line in heads) and "REJECT" not in done.stderr,
          done.stdout[:300] + done.stderr[:200])
    verdict = DV.parse(done.returncode, done.stdout, done.stderr)
    declared = sum(int(re.match(r"^REJECT — (\d+)", line).group(1)) for line in heads)
    check_eq(f"run: {label}: parse reads as many findings as the headers declare, none unmigrated, no defect",
             (len(verdict["findings"]), verdict["unmigrated"], verdict["defects"]), (declared, "", []))
    return {"verdict": verdict, "out": done.stdout}


def contract_run() -> None:
    import test_words_doors as WD
    for label, script, make in (("critic_rollcall", "critic_rollcall.py", WD.critic_story),
                                ("planning_contract", "planning_contract.py", WD.plan_story),
                                ("s5_precheck", "s5_precheck.py", WD.s5_story)):
        root = temp_project("qa-verdict-")
        try:
            WD.use_project(root)
            make(root)
            ran = run_checks(label, script, cwd=root, env=WD.project_env(root))
            if script == "s5_precheck.py":
                v = ran["verdict"]
                causes = [line.rsplit(" ", 1)[1] for line in ran["out"].splitlines()
                          if line.startswith(DV.WORDS_REFUSED_AT_SOURCE)]
                check("run: s5_precheck: the header carries the label, every refusal line has family or predating",
                      v["words"] == "source" and all(c in DV.REFUSAL_CAUSES for c in causes), str(causes))
            else:
                check_not_in(f"run: {label}: no refusal line (it judges no words at its source)", DV.WORDS_REFUSED_AT_SOURCE,
                             ran["out"])
                check_eq(f"run: {label}: the gate judges its words", ran["verdict"]["words"], "gate")
        finally:
            cleanup(root)
    root = temp_project("qa-verdict-plan-")
    try:
        WD.use_project(root)
        task = WD.story_with(root, "QA-1", {"S3": {"status": "running"}})
        (task / "work").mkdir()
        (task / "work" / "test-plan.json").write_text("{not json", encoding="utf-8")
        run_checks("planning_contract on a plan that is not JSON", "planning_contract.py", cwd=root, env=WD.project_env(root))
    finally:
        cleanup(root)
    root = temp_project("qa-verdict-cov-")
    try:
        case = root / "qa-factory" / "artifacts" / "T-1" / "test-cases" / "area-a" / "TC-1.md"
        case.parent.mkdir(parents=True)
        case.write_text("---\nid: TC-1\narea: area-a\nstatus: Draft\nupdated: 2026-01-01\n---\nbody\n", encoding="utf-8")
        run_checks("check_coverage with no map", "check_coverage.py", "--root", root, cwd=root)
        run_script("check_coverage.py", "--root", root, "--write", cwd=root)
        for rel in ("records", "state"):
            mp = root / "qa-factory" / rel / "coverage-map.md"
            if mp.exists():
                mp.write_text(mp.read_text(encoding="utf-8").replace("| Cases created | 1 |", "| Cases created | 9 |"),
                              encoding="utf-8")
        run_checks("check_coverage with a diverged map", "check_coverage.py", "--root", root, cwd=root)
    finally:
        cleanup(root)
    with tempfile.TemporaryDirectory() as tmp:
        review = Path(tmp) / "code-review.md"
        review.write_text("nothing here\n", encoding="utf-8")
        two = run_checks("check_witness with 2 errors", "check_witness.py", review)
        check_eq("run: check_witness: the 2 errors are 2 findings", len(two["verdict"]["findings"]), 2)
        run_checks("check_witness on a path that does not exist", "check_witness.py", Path(tmp) / "absent.json")
        broken = Path(tmp) / "automation-manifest.json"
        broken.write_text("{not json", encoding="utf-8")
        run_checks("check_witness on broken JSON", "check_witness.py", broken)
    done = run_script("sizing.py")
    check_eq("run: sizing without arguments never refuses (exit 0): no findings to read", done.returncode, 0)


def one_of_cases() -> None:
    """t-1355 N2 (S-5, AR-15): the ONE closed-list renderer. A set is printed sorted, a tuple in its own order, an empty
    list says it is empty (an empty closed list accepts nothing, and never prints as a bare "one of ")."""
    check_eq("one_of: a set is printed sorted", DV.one_of({"ui", "api", "cli"}), "api, cli, ui")
    check_eq("one_of: a frozenset is printed sorted too", DV.one_of(frozenset({"b", "a"})), "a, b")
    check_eq("one_of: a tuple keeps its own order", DV.one_of(("low", "normal", "critical")), "low, normal, critical")
    check_eq("one_of: a list keeps its own order", DV.one_of(["z", "a"]), "z, a")
    check_eq("one_of: an empty list says the list is empty", DV.one_of([]), "(none: the list is empty)")
    check_eq("one_of: an empty set says so too", DV.one_of(set()), "(none: the list is empty)")
    check_eq("one_of: a non-string item is JSON", DV.one_of([1, None, "a"]), "1, null, a")
    check_eq("one_of: a mixed set sorts by text, never raises", DV.one_of({2, "a", 1}), "1, 2, a")


def unreadable_cases() -> None:
    """RH1-5: the third state of the contract (K4, E4-E8, E22, section 7 of the spec)."""
    check_eq("the line a producer prints", DV.unreadable_line("boom\nsecond"), "UNREADABLE: boom second")
    v = DV.parse(3, DV.unreadable_line("running_story raised OSError"), "")
    check_eq("exit 3 with the marker: the reason, no finding", (v["unreadable"], v["findings"]),
             ("running_story raised OSError", []))
    check_eq("exit 3 with nothing printed", DV.parse(3, "", "")["unreadable"], "exit 3, no reason printed")
    v = DV.parse(3, block(2), "")
    check_eq("exit 3 with a REJECT block: unreadable, the findings are not read", (v["unreadable"], v["findings"]),
             ("exit 3, no reason printed", []))
    for code in (2, 4, 9, 127):
        v = DV.parse(code, "", "Traceback x\nBoom")
        check_eq(f"exit {code}: outside the contract, the stderr tail", (v["unreadable"], v["findings"]),
                 (f"exit {code}, outside the detector contract: Traceback x; Boom", []))
    check_eq("E22: exit 2, empty stdout, a refusal in stderr", DV.parse(2, "", "<refusal>")["unreadable"],
             "exit 2, outside the detector contract: <refusal>")
    check_eq("exit 2 with nothing printed", DV.parse(2, "", "")["unreadable"], "exit 2, outside the detector contract")
    check_eq("E6: exit 1, empty stdout, no head, a stderr (an import crash)", DV.parse(1, "", "ImportError: x")["unreadable"],
             "exit 1, no verdict printed: ImportError: x")
    check_eq("E6: whitespace stdout is empty", DV.parse(1, " \n\r\n", "")["unreadable"], "exit 1, printed nothing")
    v = DV.parse(1, "", "noise\n" + block(2))
    check_eq("E6 control: the head only in stderr: findings, nothing unreadable", (len(v["findings"]), v["unreadable"]), (2, ""))
    check_eq("E4: a block with a wrong count stays unmigrated, not unreadable", (bool(DV.parse(1, "REJECT — 2 f\n- a\n- b\n- c", "")["unmigrated"]),
             DV.parse(1, "REJECT — 2 f\n- a\n- b\n- c", "")["unreadable"]), (True, ""))
    check_eq("E4: free stdout at exit 1 stays unmigrated", (bool(DV.parse(1, "free", "")["unmigrated"]), DV.parse(1, "free", "")["unreadable"]),
             (True, ""))
    check_eq("E8: exit 0 with the marker at the start of a line is unreadable", DV.parse(0, "ok\nUNREADABLE: late", "")["unreadable"], "late")
    check_eq("E8: a BOM before the marker", DV.parse(0, "﻿UNREADABLE: bom", "")["unreadable"], "bom")
    check_eq("E8: the word not at the start of a line is no marker (FR-12)", DV.parse(0, "an UNREADABLE: x\nnote UNREADABLE", "")["unreadable"], "")
    check_eq("E8: CRLF lines", DV.parse(0, "a\r\nUNREADABLE: crlf\r\n", "")["unreadable"], "crlf")
    check_eq("exit 0 clean: nothing unreadable", DV.parse(0, "fine", "")["unreadable"], "")
    check_in("flatten says it, never empty", "unreadable: exit 1, printed nothing", DV.flatten(DV.parse(1, "", ""))[0])
    check_eq("E25: the cause `unreadable` of a refused line is not the new state",
             (DV.parse(1, "WORDS_REFUSED_AT_SOURCE: x\nfree", "")["unreadable"], DV.UNREADABLE, DV.EXIT_UNREADABLE), ("", "unreadable", 3))


def _raised(fn):
    """The exception `fn()` raises (None when it does not raise)."""
    try:
        fn()
    except Exception as exc:  # noqa: BLE001 - the row asserts its class
        return exc
    return None


def t1rs_world(root: Path) -> dict:
    """The valid request `validate_request` is provoked over, and the files it reads, under `root`."""
    import execution_request as ER
    from execution_fingerprint import file_hash
    (root / "qa-factory" / "state").mkdir(parents=True)
    (root / "qa-factory" / "config.json").write_text("{}", encoding="utf-8")
    (root / "dummy_runner.py").write_text("print('x')\n", encoding="utf-8")
    (root / "qa-factory" / "artifacts" / "REQ-1").mkdir(parents=True)
    ids = ["case-0", "case-1"]
    request = {
        "task": "REQ-1", "revision": "plan-1", "dispatch_id": "dispatch-1", "profile_id": "api", "purpose": "initial",
        "selected_instance_ids": ids, "current_scope_instance_ids": ids, "input_fingerprint": "sha256:inputs-1",
        "fingerprint_files": [{"path": str(root / "dummy_runner.py"), "sha256": file_hash(root / "dummy_runner.py"), "kind": "test_files"},
                              {"path": str(root / "qa-factory" / "config.json"),
                               "sha256": file_hash(root / "qa-factory" / "config.json"), "kind": "config_files"}],
        "fingerprint_components": {"source_sha": "a" * 40, "test_content_sha": "b" * 64, "config_sha": "c" * 64},
        "runtime_provenance": {"profile_id": "api", "timestamp": "2026-09-17T12:00:00Z", "environment_id": "qa",
                               "expected_source_revision": "source-1", "observed_runtime_identity": "build-1",
                               "evidence_refs": ["deploy/1"],
                               "provenance": {"technical_verification": True, "source_linkage": "exact",
                                              "deployed_source_revision": "source-1"}, "result": "matched"},
        "runtime_required": True, "runtime_probe": {"argv": [sys.executable, "probe.py"], "cwd": ".", "timeout_s": 5},
        "instance_contracts": {i: {"report_test_id": f"x::{i}", "parameters": {}} for i in ids},
        "reason": "t1rs", "remaining_budget": 100, "idempotency_key": "k-1", "freshness": "fresh",
        "command": {"argv": [sys.executable, "dummy_runner.py", "{report_path}"], "cwd": ".", "scope": "selected",
                    "reporter": "junit-xml", "report_path": "{report_path}", "selector_args": {i: [i] for i in ids}}}
    assert ER.validate_request(request, root)["selected_instance_ids"] == ids     # the control: the base request is valid
    return request


def t1rs_sites() -> None:
    """told-before-work T1r-sites S-1a: every refusal of `execution_request.py` that maps to a row id is `refusal("<id>", <text>)`
    and its text is the one it always was. ONE table, a row per id: the refusal is provoked in-process, `str(exc)` is the old
    text (a literal of `T1RS_OLD`), the Record of the row rides on the exception (`records` of a `validate_request` error,
    else `args[0]`) with `check == <id>`, and the row of that id states a sentence the refusal prints. Ids that need the
    stand's collect (`window_first`, `selector_args`) are not provoked here: they are written in test_execution_request.py."""
    import contextlib
    import execution_request as ER
    import stage_joints as SJ
    from contract import entries_for_case, manifest_test_keys, split_case_key
    tmp = Path(tempfile.mkdtemp(prefix="t1rs-"))
    saved = os.environ.get("CLAUDE_PROJECT_DIR")
    try:
        root = tmp / "validate"
        request = t1rs_world(root)

        def broken(**over):
            changed = json.loads(json.dumps(request))
            for key, value in over.items():
                if value is None:
                    changed.pop(key, None)
                else:
                    changed[key] = value
            return changed
        validate = lambda data: _raised(lambda: ER.validate_request(data, root))  # noqa: E731
        pipeline = root / "qa-factory" / "artifacts" / "REQ-1" / "pipeline.json"

        def reference_contradiction():
            pipeline.write_text(json.dumps({"ticket": "REQ-1", "environment": "qa", "sides": {
                "ui": {"reality": "real", "deliverable": True, "reference": "qa", "source": "person"}}}), encoding="utf-8")
            try:
                return validate(broken())
            finally:
                pipeline.write_text(json.dumps({"ticket": "REQ-1"}), encoding="utf-8")
        no_selector = json.loads(json.dumps(request["command"]))
        no_selector.pop("selector_args")
        bogus_reporter = {**request["command"], "reporter": "bogus"}

        # the `--mine` world: a story K-1 with a running dispatch (scope TC-002, TC-777) and a manifest row for TC-002
        mine = tmp / "mine"
        (mine / "qa-factory" / "state").mkdir(parents=True)
        (mine / "tests").mkdir()
        (mine / "tests" / "a.spec.ts").write_text("test('TC-002 adds one', async () => {});\n", encoding="utf-8")
        task = mine / "qa-factory" / "artifacts" / "K-1"
        task.mkdir(parents=True)
        spec = {"argv": [sys.executable, "probe.py"], "cwd": ".", "timeout_s": 30}
        profile = {"profile_id": "web", "selected": True, "roots": {"test": "tests"},
                   "commands": {"one_test": {"argv": ["npx", "playwright", "test", "<test-file>"], "cwd": "."}},
                   "reporter": {"kind": "junit-xml"}, "selectors": {"verified": True}}
        cfg = {"profiles": [profile], "execution": {"runtime_probes": {"web": spec}}}
        no_command = {**cfg, "profiles": [{**profile, "commands": {}}]}

        def put(name, value):
            (task / name).parent.mkdir(parents=True, exist_ok=True)
            (task / name).write_text(json.dumps(value), encoding="utf-8")

        def story(dispatches):
            put("work/automation-manifest.json", {"tests": [{"case": "TC-002", "file": "tests/a.spec.ts",
                                                            "selector": "tests/a.spec.ts::TC-002 adds one",
                                                            "instance_id": "TC-002 adds one", "test": "TC-002 adds one"}]})
            put("state/controller.json", {"schema_version": "2", "revision": "1", "source_revision": "s", "dispatches": dispatches})
            put("pipeline.json", {"stages": {"S5": {"status": "running"}}})
        running = {"S5-qa-automator-1": {"id": "S5-qa-automator-1", "stage": "S5", "role": "qa-automator", "status": "running",
                                         "scope": ["TC-002", "TC-777"], "budget": {"requests": 150}}}
        os.environ["CLAUDE_PROJECT_DIR"] = str(mine)

        def build(cases, config=cfg, **kw):
            return _raised(lambda: ER.build_mine_request(mine, cases, cfg=config, task="K-1", **kw))

        def with_story(dispatches, cases, config=cfg, **kw):
            story(dispatches)
            return build(cases, config, **kw)

        def refused_probe(_spec):
            raise ER.ProvenanceRefused({"result": "unknown", "environment_id": "qa"})
        stand = lambda probe=None: _raised(lambda: ER._observe_stand(  # noqa: E731
            cfg if probe else {}, "web", None, "run", probe, {}, mine, None, False, []))
        entries = [{"case": "TC-1", "file": "t.py"}]
        readers = (manifest_test_keys, split_case_key, entries_for_case)
        store = ER.JobStore(tmp / "jobs")
        store.directory.mkdir()
        (store.directory / (ER.hashlib.sha256(b"bad").hexdigest() + ".json")).write_text("{not json", encoding="utf-8")
        rows = [
            ("execution_request:purpose", lambda: validate(broken(purpose="impact_regression"))),
            ("execution_request:selection", lambda: validate(broken(selected_instance_ids=[]))),
            ("execution_request:budget", lambda: validate(broken(remaining_budget=0))),
            ("execution_request:freshness", lambda: validate(broken(freshness="stale"))),
            ("execution_request:runtime", lambda: validate(broken(runtime_provenance=None))),
            ("execution_request:fingerprint", lambda: validate(broken(fingerprint_components={}))),
            ("execution_request:command", lambda: validate(broken(command=bogus_reporter))),
            ("execution_request:execution", lambda: validate(broken(execution={"schema_version": 2}))),
            ("execution_request:selector", lambda: validate(broken(command=no_selector))),
            ("execution_request:instance_contracts", lambda: validate(broken(instance_contracts=None))),
            ("execution_request:stand.reference", reference_contradiction),
            ("execution_request:mine_call", lambda: build([])),
            ("execution_request:active_dispatch", lambda: with_story({}, ["TC-002"])),
            ("execution_request:scope", lambda: with_story(running, ["TC-009"])),
            ("execution_request:no_test", lambda: with_story(running, ["TC-777"])),
            ("execution_request:profile", lambda: with_story(running, ["TC-002"], profile_id="nope")),
            ("execution_request:profile_command", lambda: with_story(running, ["TC-002"], no_command)),
            ("execution_request:stand.probe", lambda: stand()),
            ("execution_request:stand", lambda: stand(refused_probe)),
            ("execution_request:place_rows", lambda: _raised(lambda: ER._place_rows(
                [{"node": "tests/none.py::t", "case": "TC-1"}], mine, mine))),
            ("execution_request:case_entries", lambda: _raised(lambda: ER._entries_of_case(
                entries, "TC-1", readers, True, None, lambda number: ["api", "ui"]))),
            ("execution_request:sandbox", lambda: _raised(lambda: ER.sandbox_run_directory(
                mine, tmp / "no-clone", profile, None))),
            ("run_suite:begin", lambda: _raised(lambda: store.begin({"idempotency_key": "bad"}))),
            ("run_suite:recover", lambda: _raised(lambda: store.recover("bad", lambda *a: False))),
        ]
        for rid, provoke in rows:
            exc = provoke()
            ok = isinstance(exc, ER.RequestError)
            check(f"t1rs {rid}: the refusal is raised", ok, repr(exc))
            if not ok:
                continue
            carried = [r for r in (exc.records or exc.args[:1]) if getattr(r, "check", "") == rid]
            check_eq(f"t1rs {rid}: the Record of the row rides on the exception", len(carried) >= 1, True)
            old = (T1RS_OLD.get(rid) or "").replace("<MINE>", str(mine)).replace("<NOCLONE>", str(tmp / "no-clone"))
            check_eq(f"t1rs {rid}: the message is the old text, byte for byte", str(exc), old)
            row, why = SJ.row_for(rid)
            told = SJ.told_text(row)[0] if row else ""
            check(f"t1rs {rid}: its row states a sentence the refusal can print", bool(told), why)
            if carried:
                check_eq(f"t1rs {rid}: the Record carries that sentence", carried[0].expected, told)
        t1rs_roads(tmp, root, mine, request, broken, story, running, pipeline, cfg, profile, store)
        # B3: a helper with several callers stays bare - `read` (begin / recover name their own row; last_run_of stays bare, E6)
        # and `find_active_dispatch` (build_mine_request names its row)
        for label, exc in (("JobStore.read", _raised(lambda: store.read("bad"))),
                           ("JobStore.last_run_of", _raised(lambda: store.last_run_of({"idempotency_key": "bad"}))),
                           ("find_active_dispatch", (story({}), _raised(lambda: ER.find_active_dispatch(
                               mine / "qa-factory" / "artifacts", "K-1", "", ["TC-002"], None)))[1])):
            check_eq(f"t1rs {label}: the raise stays a bare string", (isinstance(exc, ER.RequestError), isinstance(exc.args[0], DV.Record)),
                     (True, False))
        many = validate(broken(selected_instance_ids=["case-outside"]))
        check_eq("t1rs several problems: the join is the unchanged `; ` join", str(many), T1RS_OLD.get("many"))
        check_eq("t1rs several problems: one Record per sited problem, in order", [r.check for r in many.records],
                 ["execution_request:selection", "execution_request:selection", "execution_request:selector",
                  "execution_request:instance_contracts"])
        check_eq("t1rs an error nobody sited carries no records", ER.RequestError("x").records, ())
        saved_row_for = SJ.row_for
        SJ.row_for = lambda check, data=None: (None, "x")
        try:
            unread = validate(broken(freshness="stale"))
        finally:
            SJ.row_for = saved_row_for
        check_eq("t1rs unreadable row: the message is unchanged, the sentence says so",
                 (str(unread), "could not be read" in unread.records[0].expected),
                 (T1RS_OLD.get("execution_request:freshness"), True))
    finally:
        if saved is None:
            os.environ.pop("CLAUDE_PROJECT_DIR", None)
        else:
            os.environ["CLAUDE_PROJECT_DIR"] = saved
        shutil.rmtree(tmp, ignore_errors=True)


def t1rs_roads(tmp, root, mine, request, broken, story, running, pipeline, cfg, profile, store) -> None:
    """told-before-work T1r-sites S-1b: the ROAD column of the `t1rs_sites` table. Each row calls a printer or handler IN-PROCESS (or
    `run_suite.py` itself as the child it is) and asserts: `error` / the message is the old text, exactly ONE line starting with `{`
    (the JSON roads), `told` the LAST key, and `told[0]` is `{check: <id>, expected: told_text(row)[0]}`. `road` is one of run_suite,
    red_sandbox, probe_by_code, import_test_receipt, schedule. A road not provoked here is named in the S-1b report (judged by the batch canon)."""
    import contextlib
    import hashlib
    import io
    import subprocess
    import execution_request as ER
    import execution_scheduler as SCH
    import import_test_receipt as ITR
    import probe_by_code as PBC
    import red_sandbox as RSB
    import role_cli
    import run_suite as RS
    import stage_joints as SJ

    def sentence(rid):
        return SJ.told_text(SJ.row_for(rid)[0])[0]

    def at(project):
        from harness import use_project         # hooklib caches the project root per process: moved with the env, as every test does
        use_project(project)

    def call(fn, *argv):
        out, err, code, saved = io.StringIO(), io.StringIO(), None, sys.argv
        sys.argv = ["run_suite.py", *[str(a) for a in argv]]
        try:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                try:
                    fn()
                except SystemExit as stop:
                    code = stop.code
        finally:
            sys.argv = saved
        return code, out.getvalue(), err.getvalue()

    def write(path, value):
        Path(path).write_text(value if isinstance(value, str) else json.dumps(value), encoding="utf-8")

    def row(road, rid, stream, old, code, want_code, extra_first=()):
        """One JSON refusal: ONE `{` line on `stream`, `error` is `old`, `told` is last and holds the row's sentence."""
        tag = f"t1rs road {road} {rid}"
        lines = [ln for ln in stream.splitlines() if ln.startswith("{")]
        check_eq(f"{tag}: exactly one JSON line, the exit code unchanged", (len(lines), code), (1, want_code))
        if len(lines) != 1:
            return
        got = json.loads(lines[0])
        check_eq(f"{tag}: `error` is the old text, `told` the last key, no `execution_status`",
                 (got.get("error"), list(got)[-1], "execution_status" in got), (old, "told", False))
        entry = (got.get("told") or [{}])[0]
        check_eq(f"{tag}: the told entry is the row's", (entry.get("check"), entry.get("expected")), (rid, sentence(rid)))

    # --- the projection every road above uses: `told_fields` (rows of the same table; edges 2 and 7 of the node)
    first = DV.refusal("execution_request:freshness", "a")
    second = DV.refusal("run_suite:begin", "b")
    holder = ER.RequestError("a; b")
    holder.records = (first, second, DV.refusal("execution_request:freshness", "c"), "x")
    shapes = {
        "record": (first, ["execution_request:freshness"]),
        "exception-records (dedupe by check, first-seen order, a str item skipped)": (holder, ["execution_request:freshness", "run_suite:begin"]),
        "exception-arg0 (no records, a Record first)": (ER.RequestError(second), ["run_suite:begin"]),
        "exception-str-arg0 (records == ())": (ER.RequestError("text"), []),
        "exception-no-args": (ER.RequestError(), []),
        "list of items": ([second, first, ValueError(first)], ["run_suite:begin", "execution_request:freshness"]),
        "record with no check": (DV.Record("plain"), []),
        "plain str": ("text", []),
        "odd source (None, an int, a dict)": ([None, 3, {"told": []}], []),
    }
    for name, (source, want) in shapes.items():
        got = DV.told_fields(source)
        check_eq(f"t1rs told_fields {name}", [e["check"] for e in got.get("told", [])], want)
        check_eq(f"t1rs told_fields {name}: no key when nothing is told", ("told" in got), bool(want))
    check_eq("t1rs told_fields: an empty value's key is left out (a row with no door)",
             "door" in DV.told_fields(DV.Record("p", check="x:y", expected="e"))["told"][0], False)
    # --- road run_suite: main() and the refusers, in-process
    at(root)
    req_file = tmp / "req.json"
    write(req_file, broken(freshness="stale"))
    code, out, err = call(RS.main, "--request", req_file)
    row("run_suite", "execution_request:freshness", err, T1RS_OLD["execution_request:freshness"], code, 2)
    write(pipeline, {"ticket": "REQ-1", "environment": "qa", "sides": {
        "ui": {"reality": "real", "deliverable": True, "reference": "qa", "source": "person"}}})
    write(req_file, request)
    code, out, err = call(RS.main, "--request", req_file)
    row("run_suite", "execution_request:stand.reference", out, T1RS_OLD["execution_request:stand.reference"], code, 2)
    write(pipeline, {"ticket": "REQ-1"})
    jobs = root / "qa-factory" / "artifacts" / "REQ-1" / "state" / "execution-jobs"
    jobs.mkdir(parents=True, exist_ok=True)
    claim = jobs / (hashlib.sha256(b"k-1").hexdigest() + ".json")
    write(claim, "{not json")
    code, out, err = call(RS.main, "--request", req_file)
    claim.unlink()
    row("run_suite", "run_suite:begin", err, _CORRUPT, code, 2)
    code, out, err = call(RS.main, "--recover", "nokey", "--task", "REQ-1")
    row("run_suite", "run_suite:recover", err, "unknown execution job", code, 2)
    code, out, err = call(RS.main, "--detail", "t", "--task", "NOPE", "--label", "x")
    try:
        RS.story_root("NOPE", "run_suite --task")
    except ValueError as exc:
        phantom = str(exc)
    row("run_suite", "run_suite:phantom_story", err, phantom, code, 2)
    missing = tmp / "missing-request.json"
    try:
        missing.read_text(encoding="utf-8")
    except OSError as exc:
        absent = f"{type(exc).__name__}: {exc}"
    code, out, err = call(RS.main, "--detail", "t", "--request", missing)
    row("run_suite", "run_suite:detail_target", out, absent, code, 2)
    code, out, err = call(lambda: RS.refuse_missing_executor("web", "npx", ["TC-002"]))
    lines = [ln for ln in out.splitlines() if ln.startswith("{")]
    got = json.loads(lines[0]) if len(lines) == 1 else {}
    check_eq("t1rs road run_suite run_suite:missing_executor: one JSON line, exit 3, the question first, `told` last",
             (len(lines), code, "question" in got, list(got)[-1:], (got.get("told") or [{}])[0].get("check"),
              (got.get("told") or [{}])[0].get("expected")),
             (1, 3, True, ["told"], "run_suite:missing_executor", sentence("run_suite:missing_executor")))
    block_missing = root / "qa-factory" / "artifacts" / "REQ-1" / "work" / "none.json"
    mapping = tmp / "mapping.json"
    write(mapping, {})
    code, out, err = call(RS.main, "--reparse-block", block_missing, "--task", "REQ-1", "--mapping", mapping)
    row("run_suite", "run_suite:reparse", err, "reparse block must be an existing task-local run block", code, 2)
    schedule = tmp / "schedule.json"
    write(schedule, {"requests": [broken(freshness="stale")]})
    code, out, err = call(RS.main, "--schedule", schedule)
    row("run_suite", "execution_request:freshness", err, T1RS_OLD["execution_request:freshness"], code, 2)
    write(pipeline, {"stages": {"S5": {"status": "running"}}})
    code, out, err = call(RS.main, "--task", "REQ-1", "--label", "x")
    write(pipeline, {"ticket": "REQ-1"})
    spoken_ok = (RS.UNTYPED_STORY_RUN.format(stage="S5") in err and f"  expected: {sentence('run_suite:untyped_story_run')}" in err
                 and not [ln for ln in err.splitlines() if ln.startswith("{")])
    check_eq("t1rs road run_suite run_suite:untyped_story_run: ap.error prints the old problem, then the row's `expected:` line",
             (code, spoken_ok), (2, True))
    at(mine)
    write(mine / "qa-factory" / "config.json", {})
    story({})
    code, out, err = call(RS.main, "--mine", "TC-002", "--task", "K-1")
    row("run_suite", "execution_request:active_dispatch", out, str(_raised(lambda: ER.build_mine_request(
        mine, ["TC-002"], cfg={}, task="K-1"))), code, 2)
    code, out, err = call(RS.main, "--mine", "TC-002", "--detail", "x")
    lines = [ln for ln in out.splitlines() if ln.startswith("{")]
    got = json.loads(lines[0]) if len(lines) == 1 else {}
    check_eq("t1rs road run_suite active_dispatch (--mine --detail): one JSON line, `hint` kept, `told` last",
             (len(lines), code, "hint" in got, list(got)[-1:], (got.get("told") or [{}])[0].get("check")),
             (1, 2, True, ["told"], "execution_request:active_dispatch"))
    # --- road schedule: a child of `execution_scheduler` is `run_suite.py --request`; its `run_refused` line becomes a group row
    at(root)
    write(pipeline, {"ticket": "REQ-1", "environment": "qa", "sides": {
        "ui": {"reality": "real", "deliverable": True, "reference": "qa", "source": "person"}}})
    child = subprocess.run([sys.executable, "-B", str(Path(RS.__file__).resolve()), "--request", str(req_file)], cwd=str(root),
                           capture_output=True, text=True, encoding="utf-8", timeout=120)
    write(pipeline, {"ticket": "REQ-1"})

    class Pipe:
        def text(self, name):
            return child.stdout if name == "stdout" else ""

        def lines(self, name, count):
            return []
    group = SCH._child_row({"request": request, "job_id": "j-1", "workers": 1, "resources": set(), "reason": "t1rs"},
                           Pipe(), child.returncode, None)
    entry = (group.get("told") or [{}])[0]
    check_eq("t1rs road schedule execution_request:stand.reference: the group row keeps `error` and carries `told`",
             (group.get("status"), group.get("error") == T1RS_OLD["execution_request:stand.reference"], entry.get("check"),
              entry.get("expected")), ("run_refused", True, "execution_request:stand.reference", sentence("execution_request:stand.reference")))
    # --- road import_test_receipt: the text road of `run_guarded`: the old message, then the row's `expected:` / `door:` lines
    stream = io.StringIO()
    code = role_cli.run_guarded("import_test_receipt.py", lambda: ITR.import_receipt(broken(freshness="stale"), {}, root, tmp / "out"), stream)
    printed = stream.getvalue().splitlines()
    check_eq("t1rs road import_test_receipt execution_request:freshness: old message, `expected:` line, `check:` last",
             (code, printed[0], f"  expected: {sentence('execution_request:freshness')}" in printed, printed[-1]),
             (2, "import_test_receipt.py: " + T1RS_OLD["execution_request:freshness"], True, "  check: execution_request:freshness"))
    # --- road red_sandbox: the reader of `_run_mine` is the existing one; `_carry_told` copies the child's own `told`
    at(mine)
    proc, summary = RSB._run_mine(Path(RS.__file__).resolve(), mine, ["TC-002"], dispatch="", sandbox_root=tmp / "sandbox",
                                  reason="t1rs", again=False, timeout=120)
    carried: list = []
    RSB._carry_told(carried, summary)
    check_eq("t1rs road red_sandbox execution_request:active_dispatch: `_run_mine` reads the one line, `told` is carried",
             (summary.get("status"), bool(summary.get("error")), [e.get("check") for e in carried],
              [e.get("expected") for e in carried]), ("mine_refused", True, ["execution_request:active_dispatch"],
                                                      [sentence("execution_request:active_dispatch")]))
    refused = ER.MineRefusal(DV.refusal("execution_request:profile", "no profile"))
    saved_fresh, saved_budget = RSB._fresh_instances, ER.load_run_budget
    RSB._fresh_instances = lambda *a, **k: (_ for _ in ()).throw(refused)
    ER.load_run_budget = lambda *a, **k: ({}, "")
    try:
        told, notes = [], []
        mode = RSB._author_baseline(mine, mine / "qa-factory" / "artifacts" / "K-1", ["TC-002"], [], {}, notes, told)[0]
        check_eq("t1rs road red_sandbox execution_request:profile (in-process fresh_evidence handler, probe): the note, then `told`",
                 (mode, notes[0].startswith("the author's result could not be read (MineRefusal: no profile)"),
                  [e.get("check") for e in told], [e.get("expected") for e in told]),
                 ("own", True, ["execution_request:profile"], [sentence("execution_request:profile")]))
        told, notes = [], []
        RSB._diagnostic_red(mine, mine / "qa-factory" / "artifacts" / "K-1", "TC-002", "i", notes, told)
        check_eq("t1rs road red_sandbox execution_request:profile (in-process fresh_evidence handler, diagnostic): the note, then `told`",
                 (notes[0].startswith("the newest result of i could not be read (MineRefusal: no profile)"),
                  [e.get("check") for e in told]), (True, ["execution_request:profile"]))
    finally:
        RSB._fresh_instances, ER.load_run_budget = saved_fresh, saved_budget
    # --- road probe_by_code: the call sites of `_profile_for` / `find_active_dispatch` name their row on the Refusal they raise
    rows_of = [{"node": "tests/a.spec.ts::TC-002 adds one", "entry": {"profile_id": "nope"}}]
    story(running)
    for label, fn, rid in (
            ("_profile_of", lambda: PBC._profile_of(cfg, rows_of, "TC-002"), "execution_request:profile"),
            ("_profile_cwd", lambda: PBC._profile_cwd(cfg, "tests/a.spec.ts", "nope"), "execution_request:profile"),
            ("_dispatch_context", lambda: (story({}), PBC._dispatch_context(mine, "K-1", mine / "qa-factory" / "artifacts" / "K-1",
                                                                         "gone", "TC-002", False))[1], "execution_request:active_dispatch")):
        exc = _raised(fn)
        sent = DV.told_fields(exc).get("told", [{}])[0]
        check_eq(f"t1rs road probe_by_code {rid} ({label}): a Refusal that keeps its text and carries the row",
                 (isinstance(exc, PBC.Refusal), str(exc).startswith("probe_by_code: "), sent.get("check"), sent.get("expected")),
                 (True, True, rid, sentence(rid)))


_CORRUPT = "corrupt persisted job for idempotency key: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)"
_STAND_PROBE = (
    "this is the story's first typed run on profile web, and the factory does not know how to identify what the stand runs: "
    "there is no earlier request to copy the runtime probe from, and no `execution.runtime_probes` entry in qa-factory/config.json. "
    "That is the factory's gap, not your test's. No probe can be registered for profile web from here: qa-factory/config.json "
    "records no checkout for it (`implementation_repos[].local_path`), so there is no code to compare the stand with. Write this "
    "one request from `run_suite.py --template request`; every later `--mine` copies its probe and provenance.")
# the text each T1rs refusal had before it was sited: read from the pre-change `execution_request.py` (git HEAD 1db4ec9) by running
# the same provocations over it; `<MINE>` and `<NOCLONE>` stand for the two temporary paths the rows build
T1RS_OLD: dict = {
    "execution_request:purpose": "impact_regression is recommendation-only and cannot be executed",
    "execution_request:selection": "behavioral request must select at least one approved instance",
    "execution_request:budget": "new behavioral execution requires remaining_budget greater than zero",
    "execution_request:freshness": "freshness must be explicitly fresh; unknown/stale evidence cannot match",
    "execution_request:runtime": "runtime_provenance is required",
    "execution_request:fingerprint": "fingerprint_components requires immutable source_sha, test_content_sha, and config_sha",
    "execution_request:command": "command.reporter must be one of ['junit-xml', 'none', 'pytest', 'trx']",
    "execution_request:execution": "execution.schema_version must equal integer 1",
    "execution_request:selector": "behavioral command requires framework-specific selector_args mapping",
    "execution_request:instance_contracts": "behavioral request requires instance_contracts",
    "execution_request:stand.reference": (
        "the story's record names the stand `qa` both as its own stand (`pipeline.json` `environment`) and as the reference (the OLD "
        "version) of the `ui` side, so the factory cannot tell which version a run there would show. Door: correct the record - "
        "`stage_done.py --task REQ-1 --set sides.ui.reference=<the stand that runs the old version>` (or clear it), or tell the "
        "conductor which stand runs the new version"),
    "execution_request:mine_call": "--mine needs at least one case id: --mine TC-001[,TC-002]",
    "execution_request:active_dispatch": (
        "no active dispatch in story K-1: `--mine` builds the run of the dispatch the controller has open, and none is open. Inside "
        "a story the orchestrator opens one (controller.py --operation prepare); outside a story run tests with --task/--label."),
    "execution_request:scope": (
        "TC-009 is outside its scope: dispatch S5-qa-automator-1 was given TC-002, TC-777. A dispatch runs only the cases it was "
        "given; nothing is wrong with your test. Hand the case back in your digest — the orchestrator dispatches it, or "
        "records the person's word for it (waiver.py, stage S5, block \"outside its scope\")."),
    "execution_request:no_test": (
        "the manifest names no test for TC-777 yet. Put the test there through manifest_put.py (file + selector), or name it for "
        "this run: --mine TC-777 --node-id <file>::<test function>"),
    "execution_request:profile": (
        "--profile names the execution profile `nope`, which qa-factory/config.json does not hold (profile_id there: web); pass "
        "one of them with --profile ID"),
    "execution_request:profile_command": (
        "profile web has no commands.one_test.argv in qa-factory/config.json, and this story has no earlier typed run to copy the "
        "command from. That is a gap of the onboarding, not of your test: report it in your digest, and write this one run with "
        "--template request. To record the command once and for all: `/qa-factory:qa-onboarding` (execution batch)."),
    "execution_request:stand.probe": _STAND_PROBE,
    "execution_request:stand": "runtime probe returned unknown: the probe gave no reason",
    "execution_request:place_rows": (
        "TC-1: the manifest names tests/none.py, and no such file is under <MINE>. Correct `file` through manifest_put.py (a path "
        "relative to the project root), or pass --cwd when the test lives in a sandbox."),
    "execution_request:case_entries": (
        "TC-1 is held under more than one area (api/TC-1, ui/TC-1); name the one you mean: --mine api/TC-1 (if your dispatch was "
        "given the bare id, hand it back in your digest)"),
    "execution_request:sandbox": (
        "the sandbox root <NOCLONE> is not a directory. `red_sandbox.py --probe` prepares a clone that holds it and passes "
        "--sandbox-root itself; or name the one directory to run in with --cwd <directory>"),
    "run_suite:begin": _CORRUPT,
    "run_suite:recover": _CORRUPT,
    "many": ("selected instances outside approved current scope: case-outside; unsupported selector for instances: case-outside; "
             "command.selector_args.case-outside must be a non-empty string array; "
             "instance_contracts.case-outside.report_test_id is required"),
}


def main() -> None:
    unreadable_cases()
    one_of_cases()
    parse_cases()
    tag_cases()
    record_cases()
    check_id_cases()
    told_cases()
    refusal_cases()
    render_cases()
    joined_cases()
    named_cases()
    compound_cases()
    m2_m4_cases()
    contract_static()
    contract_run()
    t1rs_sites()
    finish("test_detector_verdict")


if __name__ == "__main__":
    main()

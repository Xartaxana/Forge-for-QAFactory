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


def refuse_cases() -> None:
    """K10p/refuse-*: `role_cli.refuse` prints every further refused check of an error (`records`) through the one line renderer, after
    `how to prove it` and before `if you cannot`; the LAST line stays `  check: <first check>`. Rows are injected by `_Rows`."""
    import io
    import branch_accounting
    import role_cli
    command = "import_test_receipt.py"
    rows = {f"t:{n}": ({"check": f"t:{n}", "requirement": f"Sentence {n}.", "door": f"door {n}"}, "") for n in "abcde"}

    def rec(n: str) -> DV.Record:
        return DV.Record(f"problem {n}", check=f"t:{n}", expected=f"Sentence {n}.", door=f"door {n}")

    def run(problem, **kw) -> list:
        stream = io.StringIO()
        code = role_cli.refuse(command, problem, stream, **kw)
        check_eq("K10p/refuse: the exit code is the refused one", code, role_cli.EXIT_REFUSED)
        return stream.getvalue().splitlines()

    def extras(lines) -> list:
        return [x for x in lines if x.startswith("  - [") or "more refused checks" in x]

    def line(n: str) -> str:
        return f"  - [t:{n}] Sentence {n}. Door: door {n}."

    def limited(n):
        saved = branch_accounting.limit
        branch_accounting.limit = lambda name: n
        return saved

    with _Rows(rows):
        base = run(rec("a"))
        for label, kw in (("no-records", {}), ("records-empty", {"records": ()}), ("records-not-a-list",
                          {"records": "t:b"}), ("records-a-dict", {"records": {"t:b": rec("b")}}), ("records-none", {"records": None})):
            check_eq(f"K10p/refuse-{label}/no-records: output byte-equal to today", run(rec("a"), **kw), base)
        check_eq("K10p/refuse-no-records: a plain str problem with no records is its own lines, the check last",
                 run("plain", check="x:y")[-1], "  check: x:y")
        lines = run(rec("a"), records=(rec("a"), rec("b"), rec("c")))
        check_eq("K10p/refuse-records-printed: every further check once, after `how to prove it`, before `if you cannot`",
                 (extras(lines), [i for i, x in enumerate(lines) if x.startswith("  how to prove it")] < [i for i, x in enumerate(lines)
                  if x == line("b")], lines.index(line("c")) < next(i for i, x in enumerate(lines) if x.startswith("  if you cannot"))),
                 ([line("b"), line("c")], True, True))
        check_eq("K10p/refuse-last-line-is-check: the last line is the first record's check", lines[-1], "  check: t:a")
        check_eq("K10p/refuse-first-repeated: the first record in `records` is not printed twice; a repeat of another is printed once",
                 extras(run(rec("a"), records=(rec("a"), rec("b"), rec("b"), rec("a")))), [line("b")])
        check_eq("K10p/refuse-non-record-item: a non-Record item is skipped, no exception",
                 extras(run(rec("a"), records=("t:b", 7, None, {"check": "t:c"}, rec("d")))), [line("d")])
        check_eq("K10p/refuse-own-command-check: a record of this command's own row is skipped",
                 extras(run(rec("a"), records=(DV.Record("p", check=f"role_cli:{command}", expected="E", door="D"), rec("b")))), [line("b")])
        check_eq("K10p/refuse-unreadable-row: an id with no row prints the `could not be read` sentence",
                 extras(run(rec("a"), records=(rec("a"), DV.Record("p", check="t:none")))),
                 ["  - [t:none] (the factory's requirement row t:none could not be read: the row states no requirement; this is a factory defect). Door: ."])
        saved = limited(2)
        try:
            at = run(rec("a"), records=(rec("a"), rec("b"), rec("c")))
            beyond = run(rec("a"), records=(rec("a"), rec("b"), rec("c"), rec("d")))
            beyond_many = run(rec("a"), records=(rec("a"), rec("b"), rec("c"), rec("d"), rec("e")))
        finally:
            branch_accounting.limit = saved
        tail = "  {} more refused checks are not shown: fix these and run the command again; it names the rest"
        check_eq("K10p/refuse-at-limit: AT the limit every line prints, no tail line", extras(at), [line("b"), line("c")])
        check_eq("K10p/refuse-beyond-limit: one beyond prints the limit and a tail line naming 1",
                 (extras(beyond), beyond[-1]), ([line("b"), line("c"), tail.format(1)], "  check: t:a"))
        check_eq("K10p/refuse-beyond-limit: three beyond name 2", extras(beyond_many)[-1], tail.format(2))

        def broken_limit(name):
            raise branch_accounting.Unreadable("x")
        saved, branch_accounting.limit = branch_accounting.limit, broken_limit
        try:
            check_eq("K10p/refuse-limit-unreadable: no cap, every line prints",
                     len(extras(run(rec("a"), records=tuple(rec(n) for n in "abcde")))), 4)
        finally:
            branch_accounting.limit = saved
    check_eq("K10p/refuse-no-literal-line: role_cli renders no `- [` line of its own (the one renderer is stage_joints.told_line)",
             "- [" in Path(role_cli.__file__).read_text(encoding="utf-8"), False)


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


def _t7c_row(obligations, **over) -> dict:
    return {"id": "TS-1", "schema_version": 2, "coverage_obligations": obligations, **over}


def _t7c_ob(**over) -> dict:
    ob = {"obligation_id": "O-1", "behavior": "b", "observation_boundary": "api", "completion_condition": "done",
          "requirement_refs": [{"ref": "R-1", "revision": "r"}], "applicable_scenarios": ["positive"],
          "oracle_status": "resolved", "oracle_source_ref": "spec", "decision": "reuse", "execution_scope": "current_task",
          "sufficiency_review": {"author_dispatch_id": "d", "input_hash": "h", "rationale": "r"},
          "coverage_links": [{"candidate_id": "c", "assessment": "sufficient", "assessment_reason": "r",
                              "assertion_refs": ["a"], "proves": ["b"], "does_not_prove": []}], "planned_check_refs": ["x"]}
    ob.update(over)
    return ob


# the lists `validate_obligations` returned before it was sited: read from the pre-change `coverage_contract.py` by running the same
# inputs over a byte copy of it (E-T7c-1: the function is also a projection filter, so the whole LIST is the old value)
T7C_OLD: dict = {
    "valid": [],
    "version": ["TS-1: coverage schema version 2 required: the row key is exactly `schema_version`, written as the number 2 "
                "(`schema_version: 2`) (this row has `coverage_schema_version`, which is not the key)"],
    "no_behavior": ["O-1: missing behavior: behavior needs a non-empty sentence"],
    "no_obligations": ["TS-1: coverage_obligations required"],
    "oracle": ["O-1: oracle_status: not filled. One of: resolved | unresolved"],
    "observation": ["O-1: observation_contract required by coverage contract revision"],
    "two": ["O-1: missing behavior: behavior needs a non-empty sentence", "obligation IDs must be nonempty and unique",
            "O-1: oracle_status: not filled. One of: resolved | unresolved"],
}


def tbw_t7c_sites() -> None:
    """told-before-work T7c: `coverage_contract.validate_obligations` writes `coverage_contract:obligations` on every problem line it
    makes and `coverage_contract:obligations.observation` on the lines of `validate_observation_contract`. One table, a row per
    input: the returned list equals the OLD list (E-T7c-1, the same function is a projection filter: `==`, `json.dumps`, and the
    valid row gives `[]`), each item is a `Record` with the row's id and the row's sentence."""
    import coverage_contract as CC
    import stage_joints as SJ

    def sentence(rid):
        return SJ.told_text(SJ.row_for(rid)[0])[0]
    obligations, observation = "coverage_contract:obligations", "coverage_contract:obligations.observation"
    inputs = {
        "valid": ([_t7c_row([_t7c_ob()])], None),
        "version": ([{"id": "TS-1", "coverage_schema_version": 2, "coverage_obligations": [_t7c_ob()]}], obligations),
        "no_behavior": ([_t7c_row([_t7c_ob(behavior="")])], obligations),
        "no_obligations": ([_t7c_row([])], obligations),
        "oracle": ([_t7c_row([_t7c_ob(oracle_status="maybe")])], obligations),
        "observation": ([_t7c_row([_t7c_ob()], coverage_contract_revision=CC.COVERAGE_CONTRACT_REVISION)], observation),
        "two": ([_t7c_row([_t7c_ob(behavior=""), _t7c_ob(oracle_status="maybe")])], obligations),
    }
    for name, (rows, rid) in inputs.items():
        got = CC.validate_obligations(rows, True)
        check_eq(f"t7c {name}: the returned list is the old list (a projection filter sees the same value)",
                 (got == T7C_OLD[name], json.dumps(got) == json.dumps(T7C_OLD[name]), isinstance(got, list)), (True, True, True))
        check_eq(f"t7c {name}: every item is a Record of its row, with the row's sentence",
                 [(isinstance(e, DV.Record), getattr(e, "check", None), getattr(e, "expected", None)) for e in got],
                 [(True, rid, sentence(rid))] * len(got))
    check_eq("t7c obligations: the row states a sentence the refusal prints (a row nobody can read gives the factory-defect text)",
             (bool(sentence(obligations)), bool(sentence(observation))), (True, True))


# told-before-work T6: the sha256[:16] of the text the OLD `handoff_check.py` printed for each provocation of `tbw_t6_sites` (captured from a
# byte copy of the file before the siting edit; a path is `<ROOT>` / `<PKG>`, a backslash folded to `/`)
T6_OLD = {
    'field.blank / fresh form, header.verdict': '316827b3057015e3',
    'required_rows / fresh form, scope': '2aacb18285053e98',
    'field.value / closed list, bogus word': 'd32e1ba7378d22c4',
    'required_rows.owed_by_verdict / concerns owes findings': '5ee8a34a35a0d267',
    'findings_tooling / tooling finding not repeated': '96a349b9717df61b',
    'field.value / open list, `new:` without a reason': '515f115e87617c95',
    'tried / fresh S2 form': '7c483d84567c9e2b',
    'blocked_problem / a blocked row, blocked.problem empty': 'f400591efd3c5ffe',
    'field.max_len / a reason of 90': 'ed605c3ddb7dbd95',
    'field.value / row state bogus': '39ad2113f0644a71',
    'required_rows.null_word / window none beside a row': 'a626be7fa8e21883',
    'null_outcome.repairs / a TEST_BUG row': '6d2894cb59a86b27',
    'null_outcome.verdict / a verdict nobody knows': 'e7b372af87a70593',
    'null_outcome.names / a row with no instance': 'f1487fcc2ad932d8',
    'null_outcome.report / no run report': 'db8dca98c5281d69',
    'null_outcome.failures / no row, report shows a failure': 'e666b5d0d1cd3646',
    'null_outcome.failures / a failure with no row among rows': '2ad69ca10eb73b89',
    'null_outcome.listing / a triage row not listed': '10e29ffe4e6996aa',
    'null_outcome.listing / an id listed nobody triaged': '24187593815ecf5b',
    'binding / non-empty scope, a row names two failures': '9d45df4f31d94fda',
    'null_outcome.failures / empty scope, ambiguous rows': 'a53a53319ae4f9b4',
    'investigation / scope not empty': 'd4cebebd1e33db83',
    'investigation / scope not a list': '60a051ac25c00d9d',
    'claims / _check_claims, claimed true and false on disk': 'f8877a8cc91074c8',
    'claims / _fill_claims, measured false': '6520dad9c12aba69',
    'claims / _fill_claims, could not measure': '45ff1775d2712a4f',
    'values_file / not a path line': '4c23b82a7490e15f',
    'values_file / invalid JSON': '4ad5c2ad421e626f',
    'values_file / a JSON list': '7975cb1ac3302610',
    'values_file / given twice': 'd9eb0d09f0dcf663',
    'values_file / nested': 'c77f5585660c7737',
    'values_apply / not a field': 'fba9f456f57e9c98',
    "values_apply / a list row's end": '24433d1e66ce75ad',
    'values_apply / contract-owned': '35e23da64af5a868',
    'values_apply / a list for one value': 'df9202230c7ab8f0',
    'values_apply / a row out of order': '33e64f8d9396afba',
    'values_apply / _text_of, not UTF-8': '2ce7a1b828bfb5c5',
    'cli / --shorten without --fix': '5fa94ae13215a545',
    'cli / no such file': '74a692e1910cc058',
    'cli / not UTF-8': '1264eb6f8686bff7',
    'cli / no contract line': 'ba75c5b63e193591',
    'cli / unknown contract': '6d1b6caab72bfc8d',
    'cli / no such values file': '8eda50354c04ec33',
}


def tbw_t6_sites() -> None:
    """told-before-work T6: every refusal of `handoff_check.py` that maps to one of the 21 rows is `refusal("handoff_check:<id>", <text>)`
    and its text is the one it always was. ONE table, a row per (id, provocation): the problem builder is called in-process (`check`,
    `parse_values`, `apply_values`, `_text_of`, `_fill_claims`, `_check_claims`, `main`), the text hashes to the OLD file's text (`T6_OLD`),
    the Problem's text is a Record with `check == <id>` and the row's sentence as `expected` (the `cli` prints are bare text: the last
    stdout line is the reason a caller reads), and the scanner reads exactly the 21 ids in `handoff_check.py`. `refusal_text`, `--json` and
    the exit codes are not touched (K11 and K12 of test_handoff_values_main_block pin them)."""
    import contextlib
    import hashlib
    import io
    import handoff
    import handoff_check as H
    import handoff_init
    import refusal_registry
    import stage_joints as SJ
    s7c, s5c, s2c, ticket = "s7-analyst-to-automator", "s5-critic-to-automator", "s2-tester-to-strategist", "QA-9"
    tmp = Path(tempfile.mkdtemp(prefix="t6-"))
    got, saved_argv = {}, sys.argv

    def head(contract, role, stage, disp):
        text = (handoff.CONTRACTS / f"{contract}.yaml").read_text(encoding="utf-8")
        return handoff_init.fill_head(text, task=ticket, dispatch=disp, role=role, stage=stage, scope="")

    def section(text, name, body):
        return re.sub(r"(?ms)^" + re.escape(name) + r":.*?(?=^\S)", body.rstrip("\n") + "\n\n", text, count=1)

    def s7_form(scope=(), nfr=(), window="none", reason="the test waits for a race"):
        doc = handoff.parse(head(s7c, "qa-failure-analyst", "S7", "S7-qa-failure-analyst-1"))
        for path, value in (("inputs_read[0].version", "v1"), ("inputs_read[0].failures", 7), ("inputs_read[1].path", "work/triage.json"),
                            ("inputs_read[1].version", "v2"), ("header.verdict", "concerns"), ("header.window", window),
                            ("claims.every_repair_names_evidence_expected_and_check", True),
                            ("claims.no_app_bug_expectation_was_handed_for_repair", True),
                            ("claims.every_flaky_verdict_carries_three_isolated_reruns_and_a_mechanism", True)):
            handoff.set_value(doc, path, value)
            doc = handoff.parse(doc.text())
        rows = ["scope:"] + [x for i, st in scope for x in (f"  - id: {i}", f"    state: {st}", f"    reason: {reason}",
                                                           f"    case: {ticket}_TC_001", "    round: 1 of 2")]
        text = section(doc.text(), "scope", "\n".join(rows) if scope else "scope: []")
        text = section(section(text, "repairs", "repairs: []"), "unresolved", "unresolved: []")
        kept = ["not_for_repair:"] + [x for i, v in nfr for x in (f"  - id: {i}", f"    verdict: {v}", "    where_it_went: x/y.json")]
        return section(text, "not_for_repair", "\n".join(kept) if nfr else "not_for_repair: []")

    def task(triage, report="clean"):
        root = Path(tempfile.mkdtemp(prefix="t6w-", dir=tmp))
        (root / "work").mkdir()
        if triage is not None:
            (root / "work" / "triage.json").write_text(json.dumps({"triage": triage}), encoding="utf-8")
        if report == "clean":
            report = {"execution_status": "passed", "current_results": [], "current_totals": {"passed": 1}, "current_manual_checks": []}
        if report is not None:
            (root / "work" / "run-report.json").write_text(json.dumps(report), encoding="utf-8")
        return root

    def row(i, verdict):
        return {"test": "tests/t.py::" + i, "instance_id": i, "verdict": verdict, "evidence": "e.json", "attempt_id": "a1"}

    def problems(text, contract, root, dispatch="S7-qa-failure-analyst-1"):
        return H.check(handoff.parse(text), contract, H.Artifacts(root, dispatch=dispatch), use_judge=False)[2]

    def add(key, source, path=None, kind=None, has=None):
        if isinstance(source, list):
            source = next((p for p in source if path in (None, p.path) and kind in (None, p.kind) and (has or "") in str(p.text)), None)
            check(f"tbw-t6 {key}: the provocation raised its problem", source is not None)
            if source is None:
                return
        got[key] = (str(getattr(source, "text", source)), getattr(source, "text", source), isinstance(source, str))

    def with_triage(rows, report="clean", form=None):
        names = [(r.get("instance_id"), r["verdict"] if r["verdict"] in ("APP_BUG", "ENV_ISSUE") else "ENV_ISSUE")
                 for r in rows if r.get("instance_id")]
        return problems(form or s7_form(nfr=names), s7c, task(rows, report))

    def edited(text, contract, root, dispatch, **sets):
        doc = handoff.parse(text)
        for path, value in sets.items():
            handoff.set_value(doc, re.sub(r"__(\d+)__", r"[\1].", path).replace("__", "."), value)
            doc = handoff.parse(doc.text())
        return problems(doc.text(), contract, root, dispatch)

    def digest(text):
        return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]

    failing = {"execution_status": "failed", "current_manual_checks": [], "current_totals": {"failed": 1},
               "current_results": [{"instance_id": "z[1]", "status": "failed"}]}
    ambiguous = {"execution_status": "failed", "current_manual_checks": [], "current_totals": {"failed": 2},
                 "current_results": [{"instance_id": "s[json]", "status": "failed"}, {"instance_id": "s[multi]", "status": "failed"}]}
    try:
        s5, s2 = head(s5c, "qa-code-critic", "S5", "S5-qa-code-critic-1"), head(s2c, "qa-requirements-tester", "S2", "S2-qa-requirements-tester-1")
        t5, t7, s5d, s2d = task(None, report=None), task([]), "S5-qa-code-critic-1", "S2-qa-requirements-tester-1"
        fresh5 = problems(s5, s5c, t5, s5d)
        add("field.blank / fresh form, header.verdict", fresh5, "header.verdict", "blank")
        add("required_rows / fresh form, scope", fresh5, "scope")
        add("field.value / closed list, bogus word", edited(s5, s5c, t5, s5d, header__verdict="bogus"), "header.verdict")
        add("required_rows.owed_by_verdict / concerns owes findings", edited(s5, s5c, t5, s5d, header__verdict="concerns"), "findings")
        add("findings_tooling / tooling finding not repeated",
            edited(s5, s5c, t5, s5d, findings__0__id="F-1", findings__0__cause="tooling"), "findings[0].cause")
        add("field.value / open list, `new:` without a reason", edited(s2, s2c, t5, s2d, header__verdict="new: x"), "header.verdict")
        add("tried / fresh S2 form", problems(s2, s2c, t5, s2d), "tried")
        add("blocked_problem / a blocked row, blocked.problem empty", edited(s2, s2c, t5, s2d, scope__0__state="blocked"), "scope[0].state")
        add("field.max_len / a reason of 90", problems(s7_form(scope=[("a[1]", "red")], window=ticket, reason="x" * 90), s7c, t7), "scope[0].reason")
        add("field.value / row state bogus", problems(s7_form(scope=[("a[1]", "bogus")], window=ticket), s7c, t7), "scope[0].state")
        add("required_rows.null_word / window none beside a row", problems(s7_form(scope=[("a[1]", "red")]), s7c, t7), "header.window")
        add("null_outcome.repairs / a TEST_BUG row", with_triage([row("a[1]", "TEST_BUG")]), "scope")
        add("null_outcome.verdict / a verdict nobody knows", with_triage([row("a[1]", "WHATEVER")]), "scope")
        add("null_outcome.names / a row with no instance", with_triage([{"verdict": "ENV_ISSUE"}]), "scope")
        add("null_outcome.report / no run report", with_triage([row("a[1]", "ENV_ISSUE")], report=None), "scope")
        add("null_outcome.failures / no row, report shows a failure", with_triage([], failing, s7_form()), "scope")
        add("null_outcome.failures / a failure with no row among rows", with_triage([row("a[1]", "ENV_ISSUE")], failing), "scope")
        add("null_outcome.failures / empty scope, ambiguous rows", with_triage([row("s", "TEST_BUG")], ambiguous, s7_form(nfr=[("s", "ENV_ISSUE")])),
            "scope", has="so a failure has no verdict")
        pair = [row("a[1]", "ENV_ISSUE"), row("b[1]", "ENV_ISSUE")]
        add("null_outcome.listing / a triage row not listed", with_triage(pair, form=s7_form(nfr=[("a[1]", "ENV_ISSUE")])), "not_for_repair")
        add("null_outcome.listing / an id listed nobody triaged",
            with_triage(pair, form=s7_form(nfr=[("a[1]", "ENV_ISSUE"), ("b[1]", "ENV_ISSUE"), ("ghost[1]", "ENV_ISSUE")])), "not_for_repair")
        add("binding / non-empty scope, a row names two failures",
            with_triage([row("s", "TEST_BUG")], ambiguous, s7_form(scope=[("s[json]", "red")], window=ticket)), "scope")
        entry = handoff.null_outcomes(s7c)["scope"]
        loaded = handoff.parse(s7_form(scope=[("a[1]", "red")], window=ticket))
        add("investigation / scope not empty", H._investigation_view(loaded, "scope", entry, s7c, H.Artifacts(t7))[0], "scope")
        loaded = handoff.parse(s7_form())
        loaded.data["scope"] = "x"
        add("investigation / scope not a list", H._investigation_view(loaded, "scope", entry, s7c, H.Artifacts(t7))[0], "scope")
        kept_claims = dict(H.CLAIMS)
        H.CLAIMS["t6_false"], H.CLAIMS["t6_none"] = (lambda art: (False, "the table is not on disk")), (lambda art: (None, "no way to measure"))
        try:
            add("claims / _check_claims, claimed true and false on disk",
                H._check_claims(handoff.parse("claims:\n  t6_false: true\n"), H.Artifacts(t7)), "claims.t6_false")
            filled = H._fill_claims(handoff.parse("claims:\n  t6_false: <true|false>\n  t6_none: <true|false>\n"), H.Artifacts(t7))[3]
            add("claims / _fill_claims, measured false", filled, "claims.t6_false")
            add("claims / _fill_claims, could not measure", filled, "claims.t6_none")
        finally:
            H.CLAIMS.clear()
            H.CLAIMS.update(kept_claims)
        for label, text in (("not a path line", "just words\n"), ("invalid JSON", "{nope"), ("a JSON list", "[1]"),
                            ("given twice", "a.b: 1\na.b: 2\n"), ("nested", "scope: {a: 1}\n")):
            add(f"values_file / {label}", H.parse_values(text, "v.yaml", contract=s5c)[1])
        for label, one in (("not a field", ("nosuch.field", "x", 1, "")), ("a list row's end", ("scope[0]", "x", 1, "")),
                           ("contract-owned", ("contract", "x", 1, "")), ("a list for one value", ("header.verdict", ["a"], 1, "")),
                           ("a row out of order", ("scope[7].id", "x", 1, ""))):
            add(f"values_apply / {label}", H.apply_values(handoff.parse(s5), s5c, [one])[2])
        add("values_apply / _text_of, not UTF-8", H._text_of("v.yaml", lambda: b"\xff\xfe\x00bad\x80")[1])

        def folded(text):
            text = text.replace(str(SCRIPTS.parent), "<PKG>").replace(SCRIPTS.parent.as_posix(), "<PKG>")
            text = text.replace(str(tmp), "<ROOT>").replace(tmp.as_posix(), "<ROOT>")
            return re.sub(r"<(ROOT|PKG)>\S*", lambda m: m.group(0).replace("\\", "/"), text)
        good = tmp / "work" / "handoffs" / "S5-qa-code-critic-1.yaml"
        good.parent.mkdir(parents=True)
        good.write_text(s5, encoding="utf-8")
        for name, content in (("bad8.yaml", b"contract: x\n\xff\n"), ("nc.yaml", b"a: 1\n"), ("unk.yaml", b"contract: no-such-contract\n")):
            (tmp / name).write_bytes(content)
        for label, argv in (("--shorten without --fix", ("--file", str(good), "--shorten")), ("no such file", ("--file", str(tmp / "none.yaml"))),
                            ("not UTF-8", ("--file", str(tmp / "bad8.yaml"))), ("no contract line", ("--file", str(tmp / "nc.yaml"))),
                            ("unknown contract", ("--file", str(tmp / "unk.yaml"))),
                            ("no such values file", ("--file", str(good), "--values", str(tmp / "nv.yaml"), "--task-root", str(tmp)))):
            buf = io.StringIO()
            sys.argv = ["handoff_check.py", *argv]
            try:
                with contextlib.redirect_stdout(buf):
                    code = H.main()
            finally:
                sys.argv = saved_argv
            check_eq(f"tbw-t6 cli / {label}: exit 2", code, 2)
            add(f"cli / {label}", folded(buf.getvalue().strip()))
        for key, (text, record, bare) in got.items():
            rid = "handoff_check:" + key.split(" / ")[0]
            if digest(text) != T6_OLD.get(key):
                print(f"T6 {key}: the text is now\n{text}")
            check_eq(f"tbw-t6 {key}: the text is the old file's, byte for byte", digest(text), T6_OLD.get(key))
            if not bare:
                check_eq(f"tbw-t6 {key}: the Record carries the id and the row's sentence",
                         (getattr(record, "check", ""), getattr(record, "expected", "")), (rid, SJ.told_text(SJ.row_for(rid)[0])[0]))
        check_eq("tbw-t6 every provocation has an old text", sorted(set(T6_OLD) - set(got)), [])
        # one Record per problem, in order (EC-5): a fresh critic form says two `required_rows` (`scope`, `inputs_read`) and five blank fields
        check_eq("tbw-t6 several problems: one Record per problem, in order", [getattr(p.text, "check", "") for p in fresh5],
                 ["handoff_check:required_rows"] * 2 + ["handoff_check:field.blank"] * 5)
        check_eq("tbw-t6 no problem: a clean triage and an empty scope say nothing of the null outcome",
                 [p.path for p in problems(s7_form(), s7c, t7) if p.path in ("scope", "not_for_repair")], [])
        # an unreadable row: the text is unchanged, the sentence says the factory could not read it (EC-4, FR-59)
        real_row_for = SJ.row_for
        SJ.row_for = lambda check_id, data=None: (None, "x")
        try:
            mark = next(p for p in problems(s2, s2c, t5, s2d) if p.path == "tried")
        finally:
            SJ.row_for = real_row_for
        check_eq("tbw-t6 unreadable row: the text is unchanged, the sentence says so",
                 (digest(str(mark.text)), "could not be read" in getattr(mark.text, "expected", "")), (T6_OLD["tried / fresh S2 form"], True))
        # the scanner: the 21 ids of the rows are the literals of `handoff_check.py`, and no other id is there (E1)
        names = ["handoff_check.py"]
        records = refusal_registry.sites(SCRIPTS.parent, names, raises=refusal_registry.raise_family(SCRIPTS.parent, names, wide=True))
        wanted = sorted("handoff_check:" + i for i in (
            "field.blank field.value field.max_len required_rows required_rows.owed_by_verdict required_rows.null_word tried blocked_problem "
            "findings_tooling claims null_outcome.repairs null_outcome.verdict null_outcome.names null_outcome.report null_outcome.failures "
            "null_outcome.listing values_file values_apply cli binding investigation").split())
        check_eq("tbw-t6 the scanner reads the 21 ids as literals of handoff_check.py",
                 sorted({r["check"] for r in records if r.get("check")}), wanted)
    finally:
        sys.argv = saved_argv
        shutil.rmtree(tmp, ignore_errors=True)


def t4a_provoke(G, HA, tmp: Path) -> dict:
    """told-before-work T4a: every refusal of the `guard_pre_tool` / `host_adapter.role_policy` sites provoked in-process through the
    REAL `hooklib.block`. `{row: (id, stderr)}`; the temporary root and the plugin root are written `<ROOT>` / `<PLUGIN>`. `G` and
    `HA` are the modules under test (the pin below was captured by running the same provocations over the pre-change files).
    The project root, `CLAUDE_PROJECT_DIR` and `hooklib._PROJECT_ROOT_CACHE` are put back, and the root removed, whatever happens."""
    import hooklib
    saved_env, saved_cache = os.environ.get("CLAUDE_PROJECT_DIR"), hooklib._PROJECT_ROOT_CACHE
    root = temp_project("t4a-")
    try:
        return t4a_provoke_in(G, HA, root)
    finally:
        if saved_env is None:
            os.environ.pop("CLAUDE_PROJECT_DIR", None)
        else:
            os.environ["CLAUDE_PROJECT_DIR"] = saved_env
        hooklib._PROJECT_ROOT_CACHE = saved_cache
        cleanup(root)


def t4a_provoke_in(G, HA, root: Path) -> dict:
    """The body of `t4a_provoke`, inside the project `root` it made."""
    import contextlib
    import hooklib
    import io
    from types import SimpleNamespace
    from unittest import mock
    from harness import use_project
    import dispatch_identity as DI
    import planning_contract as PC
    import handoff_check
    use_project(root)
    cfg = json.loads((root / "qa-factory" / "config.json").read_text(encoding="utf-8"))
    task = root / "qa-factory" / "artifacts" / "T-1"
    (task / "state").mkdir(parents=True)
    (task / "work" / "handoffs").mkdir(parents=True)
    (root / "evidence").mkdir()
    for rel, text in (("work/handoffs/D-1.yaml", "a: 1\n"), ("work/handoffs/D-1.values.yaml", "a: 2\n"), ("work/test-plan.md", "# plan\n"),
                      ("work/test-plan.json", '[{"id": "TS-1"}]'), ("work/context-manifest.json", "{}"),
                      ("work/automation-manifest.json", '{"tests": [{"case": "TC-1"}]}'), ("state/controller.json", '{"dispatches": {}}'),
                      ("pipeline.json", '{"ticket": "T-1", "stages": {}}')):
        (task / rel).write_text(text, encoding="utf-8")
    (root / "evidence" / "a.log").write_text("x" * 9000, encoding="utf-8")
    (root / "big.txt").write_text("y" * 100000, encoding="utf-8")
    (root / "tests" / "api").mkdir(parents=True, exist_ok=True)
    out: dict = {}

    def err_of(fn, *args) -> str:
        buf = io.StringIO()
        with contextlib.redirect_stderr(buf):
            try:
                fn(*args)
            except SystemExit as exc:
                if exc.code != 2:
                    return f"exit {exc.code}"
        text = buf.getvalue()
        for path, tag in ((root, "<ROOT>"), (hooklib.PLUGIN_ROOT, "<PLUGIN>")):
            for spelling in (str(path), str(path).replace("\\", "/")):
                text = text.replace(spelling, tag)
        return text

    def put(row, cid, fn, *args):
        out[row] = (cid, err_of(fn, *args))

    def at(rel):
        return str(task / rel)

    def ev(tool, path="", role="", **tool_input):
        event = {"tool_name": tool, "tool_input": dict({"file_path": path} if path else {}, **tool_input), "cwd": str(root)}
        return dict(event, agent_type=role) if role else event
    sh = lambda command, role="": ev("Bash", command=command, role=role)  # noqa: E731
    p = "guard_pre_tool:PT-"
    put("size", p + "command-size", G.size_check, sh("x" * 70000), cfg)
    put("direct run", p + "direct-test-run", G.runs_check, sh("pytest -q"), cfg)
    put("playwright test", p + "direct-test-run", G.runs_check, sh("npx playwright test"), cfg)
    put("git config", p + "git-config", G.git_config_check, sh("git config --global user.name x"), cfg)
    put("logs Read", p + "logs", G.logs_check, ev("Read", str(root / "evidence" / "a.log")), cfg)
    put("logs shell", p + "logs", G.logs_check, sh(f"cat {root / 'evidence' / 'a.log'}"), cfg)
    put("plugin read", p + "plugin-read", G.plugin_read_check, ev("Read", (hooklib.PLUGIN_ROOT / "scripts" / "hooklib.py").as_posix(), role="qa-scout"), cfg)
    put("big read", p + "big-read", G.big_read_check, {"file_path": str(root / "big.txt")}, cfg, ev("Read", str(root / "big.txt")))
    put("case store", p + "case-store", G.case_store_check, ev("Write", at("work/TC-001.md")), {**cfg, "cases_root": "cases"})
    put("handoff rewrite", p + "handoff-rewrite", G.handoff_write_check, ev("Write", at("work/handoffs/D-1.yaml")), cfg)
    put("handoff edit pending", p + "handoff-edit-pending", G.handoff_write_check, ev("Edit", at("work/handoffs/D-1.yaml")), cfg)
    put("handoff code file", p + "handoff-code-file", G.handoff_write_check, ev("Write", at("work/handoffs/D-1.values.applied.yaml")), cfg)
    report = SimpleNamespace(problems=["p"], blocked_said=False, contract=None, role="", kept=[])
    with mock.patch.object(handoff_check, "values_report", return_value=report), \
            mock.patch.object(handoff_check, "refusal_text", return_value="the lines to fix"):
        put("handoff values", p + "handoff-values", G.handoff_values_check, ev("Write", at("work/handoffs/D-1.values.yaml"), content="a: 3\n"))
    put("artifact rewrite", p + "artifact-rewrite", G.artifact_rewrite_check, ev("Write", at("work/context-manifest.json")), cfg)
    put("plan rewrite", p + "plan-rewrite", G.plan_write_check, ev("Write", at("work/test-plan.json")), cfg)
    put("plan md rewrite", p + "plan-md-rewrite", G.plan_write_check, ev("Write", at("work/test-plan.md")), cfg)
    put("manifest shrink", p + "manifest-shrink", G.manifest_write_check, ev("Write", at("work/automation-manifest.json")), cfg)
    put("owner story", p + "owner", G.owner_check, ev("Write", at("work/automation-manifest.json"), role="qa-scout"), cfg)
    put("owner ledger", p + "owner", G.owner_check, ev("Write", str(root / "qa-factory" / "factory-backlog.md"), role="qa-scout"), cfg)
    controller = {"dispatches": {i: {"id": i, "stage": "S5", "role": "qa-automator", "status": "running", "scope": [c]}
                                 for i, c in (("S5-qa-automator-1", "TC-1"), ("S5-qa-automator-2", "TC-2"))}, "stages": {}}
    (task / "state" / "controller.json").write_text(json.dumps(controller), encoding="utf-8")
    saved = {k: os.environ.get(k) for k in (PC.DETECTOR_DISPATCH_ENV, DI.DRIVER_RUN_ENV)}
    os.environ.pop(PC.DETECTOR_DISPATCH_ENV, None)
    try:
        test_file = ev("Write", str(root / "tests" / "api" / "test_orders.py"))
        os.environ[DI.DRIVER_RUN_ENV] = "S5-qa-automator-1"      # the first window claims the file and passes
        err_of(G.window_file_check, test_file, cfg)
        os.environ[DI.DRIVER_RUN_ENV] = "S5-qa-automator-2"      # the second is refused (one refusal: no 'in a row' text)
        put("window file", p + "window-file", G.window_file_check, test_file, cfg)
    finally:
        for key, value in saved.items():
            os.environ.pop(key, None) if value is None else os.environ.__setitem__(key, value)
    put("external writes", p + "external-writes", G.writes_check, sh("glab issue create --title x"), cfg)
    put("human word", p + "human-word", G.human_word_check, sh("python waiver.py --stage S9 --block x", role="qa-scout"), cfg)
    put("config write", p + "config-write", G.config_write_check, ev("Write", str(root / "qa-factory" / "config.json"), role="qa-automator"), cfg)
    put("stand record", p + "stand-record-write",
        G.stand_record_write_check, ev("Write", str(root / "qa-factory" / "records" / "stand-identity.json"), role="qa-scout"), cfg)
    put("walker", p + "walker-error", G.walker_refusal, sh("x"), hooklib.WalkerError("boom"))
    put("patch unchecked", p + "patch-unchecked", G._guard, ev("apply_patch", command="not a patch"))
    with mock.patch.object(G, "read_event", return_value=None):
        put("unparsed event", p + "unparsed-event", G.main)
    h = "host_adapter:HA-"
    codex = {"turn_id": "t-1"}
    hcfg = {"host_tools": {}}
    put("call shape", h + "call-shape", HA.role_policy, {"_qa_host": {"refusal": {"what": "w", "expected": "e", "door": "d"}}}, {})
    put("no command text", h + "no-command-text", HA.role_policy,
        dict(codex, tool_name="shell", tool_input={}, _qa_host={"name": "shell"}), hcfg)
    put("nested delegation", h + "role-nested-delegation", HA.role_policy, dict(codex, agent_type="qa-automator", tool_name="Agent"), hcfg)
    put("role read only", h + "role-read-only", HA.role_policy,
        dict(codex, agent_type="qa-test-strategist", tool_name="Bash", tool_input={"command": "python x.py"}), hcfg)
    put("stdin chars", h + "stdin-chars", HA.role_policy,
        dict(codex, tool_name="Bash", tool_input={"chars": "x"}, _qa_host={"name": "write_stdin"}), hcfg)
    put("exec tty", h + "exec-tty", HA.role_policy,
        dict(codex, tool_name="Bash", tool_input={"tty": True}, _qa_host={"name": "exec_command"}), hcfg)
    tool = {"tool_name": "mcp__x__create_thing", "_qa_host": {"name": "mcp__x__create_thing"}}
    put("connector no shell", h + "connector-unclassified", HA.role_policy, dict(codex, agent_type="qa-test-strategist", **tool), hcfg)
    put("connector orchestrator", h + "connector-orchestrator", HA.role_policy, dict(codex, **tool), hcfg)
    return out


def t4a_digest(err: str) -> str:
    """The first 16 hex digits of the sha256 of the refusal's own text: stderr without the closing TRAPPED line and without the
    row's lines that follow the problem (`expected:` / `door:` / `check:`), trailing white space cut as `block` cuts it."""
    import hashlib
    from hooklib import TRAPPED
    err = err[:-1] if err.endswith("\n") else err        # the newline `print` ends the last line with
    body = err[:-len("\n" + TRAPPED)] if err.endswith("\n" + TRAPPED) else err
    return hashlib.sha256(body.split("\n  expected: ")[0].split("\n  check: ")[0].rstrip().encode("utf-8")).hexdigest()[:16]


T4A_OLD: dict = {   # row -> t4a_digest of the pre-change file's stderr (byte copy of guard_pre_tool.py / host_adapter.py taken before the edit)
    'size': 'f60c2116d5ea0e9b',
    'direct run': '504d8a343ec1dd7d',
    'playwright test': '19ad5ce85fd9a420',
    'git config': '0b7737239f468b11',
    'logs Read': 'd3dcdca4b6849d83',
    'logs shell': 'd3dcdca4b6849d83',
    'plugin read': '577c1db84a62bfdb',   # the POSIX spelling on every OS (was c8455f9f..., the Windows spelling); PLUGIN_READ_MSG unchanged since 9ac00f09
    'big read': '8cb6f7047b49f287',
    'case store': '3b95d98a22c0bbe5',
    'handoff rewrite': '9e174afe126371ee',
    'handoff edit pending': 'd9bdb494031a8c18',
    'handoff code file': '022e7a003d498b7d',
    'handoff values': '552764b4205bd4d0',
    'artifact rewrite': '477ec5b1f34fb8f3',
    'plan rewrite': '4e7edca5f5dd7ec1',
    'plan md rewrite': '0c1633372b6225d4',
    'manifest shrink': '170520564db6c6f1',
    'owner story': '7d93f26a8ae64faf',
    'owner ledger': '9944a5a6f8378e14',
    'window file': '4868f8c01058fd0b',
    'external writes': '6bbb874a5adb79fa',
    'human word': '4da061f97df6c201',
    'config write': '55d7e335e2690053',
    'stand record': 'd578f4dc0afd5204',
    'walker': 'fbd8e127dc49e34c',
    'patch unchecked': '43ee82ddb514fd27',
    'unparsed event': '2c77e19e3d5de451',
    'call shape': '5da2572131407510',
    'no command text': '2a16c97a325a52d5',
    'nested delegation': 'a9f8cc04fffca795',
    'role read only': '3d145d994a502a02',
    'stdin chars': '5b33bf4592a6a966',
    'exec tty': '460a32af2059611b',
    'connector no shell': '2b458f52b2437f60',
    'connector orchestrator': '5957e371a6fde6fb',
}


def tbw_t4a_sites() -> None:
    """told-before-work T4a: each role-facing refusal of `guard_pre_tool.py` and `host_adapter.role_policy` is `refusal("<row id>", <the
    text it always had>)`. ONE table, a row per site: the stderr is the old text byte for byte (digest `T4A_OLD`, captured over the pre-change
    files), then `  expected:` / `  door:` of the row of that id and `  check: <id>` last, then the closing TRAPPED line, exit code 2."""
    import stage_joints as SJ
    from hooklib import TRAPPED
    import guard_pre_tool as G
    import host_adapter as HA
    tmp = Path(tempfile.mkdtemp(prefix="tbw-t4a-"))
    try:
        got = t4a_provoke(G, HA, tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    check_eq("t4a: every site is provoked", sorted(got), sorted(T4A_OLD))
    for name, (cid, err) in got.items():
        row, why = SJ.row_for(cid)
        expected, door = SJ.told_text(row) if row else ("", "")
        tail = "\n  expected: " + expected + ("\n  door: " + door if door else "") + "\n  check: " + cid
        check(f"t4a {name} {cid}: the row states a sentence", bool(expected), str(why))
        check(f"t4a {name} {cid}: the row's lines follow the problem, `check:` last, TRAPPED closes", err.endswith(tail + "\n" + TRAPPED + "\n"), err[-300:])
        check_eq(f"t4a {name} {cid}: the problem text is the old one", t4a_digest(err), T4A_OLD.get(name))


def tbw_siting_command_sites() -> None:
    """told-before-work siting A (t-1108): the command and plan refusals of `controller.py`, `waiver.py`, `source_exclusions.py`,
    `stage_done.py` and `planning_contract.py` carry their row id on the Record, with the text they always had (EC-1; the one named
    exception is the unmarked-revision door of key 4, whose expected sentence is the card's). ONE table of driven sites (a refusal is
    provoked, the Record's `check` and `str` are read), and the `_raise_all` rows (E7: one keeps its Record, several set `exc.records`, a folded `(xK)` has no id)."""
    import argparse
    import contextlib
    import io
    import controller as CTL
    import planning_contract as PC
    import source_exclusions as SE
    import stage_done as SD
    import waiver as WV
    import person_words
    from harness import use_project
    import test_controller_release as REL

    def refused(fn):
        try:
            fn()
        except (ValueError, SystemExit) as exc:
            return exc
        return None

    def first(exc):
        return exc.args[0] if exc is not None and exc.args else None

    def id_text(record):
        return (getattr(record, "check", ""), str(record) if record is not None else None)

    root = temp_project()
    saved = os.environ.get("CLAUDE_PROJECT_DIR")
    try:
        use_project(root)
        controller = REL.at_s3_rework(root)
        # --- build_rework_request: row 2 (`rework.args`); one problem keeps its Record, two set `exc.records` (E7) ---
        purposes = ", ".join(sorted(CTL.PURPOSES))
        bad_purpose = f"purpose 'nope' must be one of: {purposes}"
        one = refused(lambda: controller.build_rework_request("S3", "qa-test-strategist", [], "mend it", purpose="nope"))
        check_eq("siting rework.args: one problem keeps its Record, the text is the old text",
                 id_text(first(one)), ("controller:rework.args", bad_purpose))
        two = refused(lambda: controller.build_rework_request("S3", "qa-test-strategist", [], "  ", purpose="nope"))
        blank = "--reason must say what this round repairs; it is what the role reads"
        check_eq("siting rework.args: several problems: the text is the compound text, `exc.records` carry the ids",
                 (str(two).split("\n"), [(r.check, str(r)) for r in two.records]),
                 ([CTL.Controller.COMPOUND_HEAD.format(n=2), f"1) {bad_purpose}", f"2) {blank}"],
                  [("controller:rework.args", bad_purpose), ("controller:rework.args", blank)]))
        # --- release_dispatch: row 5 (c), the unknown-dispatch caller included ---
        unknown = refused(lambda: controller.release_dispatch("ZZ-9", "it is dead"))
        check_eq("siting release.call: the unknown dispatch is wrapped at its caller, the text is `_unknown_dispatch`'s",
                 id_text(first(unknown)),
                 ("controller:release.call", CTL.Controller._unknown_dispatch("ZZ-9", controller.state()["dispatches"])[1]))
        nowords = refused(lambda: controller.release_dispatch("ZZ-9", ""))
        check_eq("siting release.call: blank words and the unknown dispatch are two Records of the one row",
                 [r.check for r in nowords.records], ["controller:release.call"] * 2)
        # --- _raise_all (E7) ---
        rec = lambda text: DV.refusal("controller:rework.args", text)           # noqa: E731
        once = refused(lambda: CTL.Controller._raise_all([(ValueError, rec("alone"))]))
        check_eq("siting _raise_all: one problem keeps the Record", id_text(first(once)), ("controller:rework.args", "alone"))
        folded = refused(lambda: CTL.Controller._raise_all([(ValueError, rec("same")), (ValueError, rec("same"))]))
        check_eq("siting _raise_all: a folded `(xK)` problem has the text and no id",
                 (id_text(first(folded)), getattr(folded, "records", "absent")), (("", "same (×2)"), "absent"))
        plain = refused(lambda: CTL.Controller._raise_all([(ValueError, "bare one"), (ValueError, "bare two")]))
        check_eq("siting _raise_all: plain strings set no records", getattr(plain, "records", None), [])
        # --- controller.main: rows 1 and 5 (a) and (b); the id rides only on its own operation (E11) ---
        story = root / "qa-factory" / "stories" / "T-1"
        (story / "state").mkdir(parents=True)
        (story / "state" / "events.jsonl").write_text("", encoding="utf-8")

        def main_with(*argv):
            old = sys.argv
            sys.argv = ["controller.py", *argv]
            try:
                return refused(CTL.main)
            finally:
                sys.argv = old
        missing = str(root / "nowhere")
        for operation, expected in (("rework", "controller:rework.call"), ("release", "controller:release.call"), ("next", "")):
            got = main_with("--operation", operation, "--task-root", missing)
            check_eq(f"siting main {operation}: the story-root refusal carries {expected or 'no id'}", getattr(first(got), "check", ""), expected)
        for operation, extra, expected in (("release", ("--words", "w"), "controller:release.call"), ("reopen_story", ("--words", "w"), ""),
                                           ("rework", ("--reason", "r"), "controller:rework.call")):
            got = main_with("--operation", operation, "--task-root", str(story), "--words-file", str(root / "w.txt"), *extra)
            check(f"siting main {operation}: both options of the words refuse (WordsRefused), id {expected or 'none'}",
                  isinstance(got, person_words.WordsRefused) and getattr(first(got), "check", "") == expected, repr(got))
        # --- waiver: rows 6 (i) in the dispatch order of the forms, 6 (ii), 11, and `record_refusals` rows 7-9 ---
        seen = []

        def waiver_error(self, message):
            seen.append(message)
            raise SystemExit(2)
        real_error, old_argv = argparse.ArgumentParser.error, sys.argv
        argparse.ArgumentParser.error = waiver_error
        try:
            for name, argv, expected in (
                    ("block words", ["--task", "T", "--stage", "S1", "--block", "b", "--decision", "d", "--words-file", "f"], "waiver:block.call"),
                    ("remark words", ["--remark", "--task", "T", "--stage", "S1", "--text", "d", "--words-file", "f"], "waiver:remark.call"),
                    ("revoke words", ["--revoke", "--task", "T", "--stage", "S1", "--block", "b", "--decision", "d", "--words-file", "f"], ""),
                    ("gate words", ["--task", "T", "--gate", "A", "--requirement", "r", "--decision", "d", "--words-file", "f"], ""),
                    ("block required", ["--task", "T", "--stage", "S1", "--block", "b"], "waiver:block.call"),
                    ("remark required", ["--remark", "--task", "T"], "waiver:remark.call")):
                del seen[:]
                sys.argv = ["waiver.py", *argv]
                refused(WV.main)
                check_eq(f"siting waiver {name}: id {expected or 'none'}", [getattr(m, "check", "") for m in seen], [expected])
        finally:
            argparse.ArgumentParser.error, sys.argv = real_error, old_argv
        gap = WV.record_refusals("stand gap:")
        check_eq("siting waiver stand_gap_id: the text is NO_GAP_ID, the id its row",
                 [id_text(r) for r in gap], [("waiver:block.stand_gap_id", WV.NO_GAP_ID)])
        holder = WV.record_refusals("probe gap: <case key>")
        check_eq("siting waiver WV-placeholder-block: one Record of the A24 id, text starts as before",
                 [(r.check, str(r).startswith('waiver: the block "probe gap: <case key>" still holds the placeholder <case key>, which names nothing'),
                   str(r).endswith("Nothing was recorded.")) for r in holder], [("waiver:WV-placeholder-block", True, True)])
        grant = WV.record_refusals("protected test path: **")
        check("siting waiver grant_pattern: every pattern error is a Record of the row (and the pattern is refused)",
              bool(grant) and all(getattr(r, "check", "") == "waiver:block.grant_pattern" for r in grant), repr(grant)[:200])
        # --- source_exclusions: the `main` prints are Records of `revoke.call` ---
        asked, real_refusal = [], DV.refusal
        DV.refusal = lambda cid, text, **kw: (asked.append((cid, str(text))), real_refusal(cid, text, **kw))[1]
        try:
            with contextlib.redirect_stderr(io.StringIO()) as err:
                SE.main(["--task", "T-1"])
            check_eq("siting source_exclusions: no form -> revoke.call, the old line on stderr",
                     (asked, err.getvalue()),
                     ([("source_exclusions:revoke.call", 'source_exclusions: give exactly one of --load FILE, --show, --revoke <id> --words "..."')],
                      'source_exclusions: give exactly one of --load FILE, --show, --revoke <id> --words "..."\n'))
        finally:
            DV.refusal = real_refusal
        # --- stage_done: row 14 ---
        for name, items, text in (("no =", ["novalue"], "--set takes key=value, not `novalue`"),
                                  ("coerced", ["size=bogus"], None)):
            got = refused(lambda: SD.parse_sets(items))
            check_eq(f"siting stage_done {name}: a ValueError carrying the Record of stage_done:set",
                     (getattr(first(got), "check", ""), text is None or str(first(got)) == text), ("stage_done:set", True))
        import contract as CONTRACT
        real_reader = CONTRACT.side_realities
        CONTRACT.side_realities = lambda: {}
        try:
            got = refused(lambda: SD.parse_sets(["sides.api.reality=absent"]))
        finally:
            CONTRACT.side_realities = real_reader
        check_eq("siting stage_done: an unreadable reference file stays bare (no id), the old text, selected by type",
                 (type(got).__name__, getattr(first(got), "check", ""), str(got).startswith("`sides.api.reality`: the words a reality may take cannot be read from references/side-realities.json - repair that file")),
                 ("UnreadableReference", "", True))
        # --- planning_contract: the unmarked line (E17, E26) with the door of key 4 ---
        line = PC.gate_plan_errors([{"id": "TS-1"}], "new", 1)
        tail = "did not run for this plan: a strategist rework of S3 writes it when that rework completes"
        check_eq("siting planning_contract: the unmarked line is a Record of its id, the prefix and the new door stand",
                 [(r.check, str(r).startswith("TS-1: missing coverage_contract_revision"), str(r).endswith(tail))
                  for r in line if "missing coverage_contract_revision" in str(r)],
                 [("planning_contract:plan.unmarked_revision", True, True)])
    finally:
        if saved is None:
            os.environ.pop("CLAUDE_PROJECT_DIR", None)
        else:
            os.environ["CLAUDE_PROJECT_DIR"] = saved
        cleanup(root)


def main() -> None:
    unreadable_cases()
    one_of_cases()
    parse_cases()
    tag_cases()
    record_cases()
    check_id_cases()
    told_cases()
    refusal_cases()
    refuse_cases()
    render_cases()
    joined_cases()
    named_cases()
    compound_cases()
    m2_m4_cases()
    contract_static()
    contract_run()
    t1rs_sites()
    tbw_t7c_sites()
    tbw_t6_sites()
    tbw_t7b_sites()
    tbw_t4a_sites()
    tbw_t4b_sites()
    tbw_siting_command_sites()
    finish("test_detector_verdict")


def tbw_t7b_sites() -> None:
    """told-before-work T7b: the twelve refusals of the S3 plan contract (`planning_contract.py`) that map to a row id write it as
    `refusal("<id>", <text>)`. ONE table, a row per id (`regression_scope.problems` is another module's: the id is on its caller
    `_regression_findings`, E-T7b-1). Each row provokes the function that returns the refusal lines, asserts the text is the one the
    pre-change file printed (`old`, read from a byte copy of that file before the edit; EC-1), that each line is a Record with
    `check == <id>` and the row's own sentence and door, and that no problem means no line (EC-5). `plan_json` is a print in the
    detector body: the row runs the body and spies on `refusal`. `unmarked_revision_errors` carries `planning_contract:plan.unmarked_revision` (t-1108: its row E17)."""
    import contextlib
    import io
    import planning_contract as PC
    import stage_joints as SJ
    from harness import use_project
    row = {"id": "TS-1", "schema_version": 1, "impact": "moderate", "likelihood": "medium", "confidence": "medium",
           "risk_rationale": "shared component", "risk_source_refs": ["R-1"], "risk_policy_revision": "factory-starter-v1",
           "coverage_refs": [], "unknowns": [], "verification_depth": "normal", "required_scenarios": ["opens"],
           "test_level_rationale": "user path", "design_review_required": False}
    register = ("## Register\n\n| R | Requirement | source | derived_from | verifiable | ac_ref | observable | impact |\n"
                "|---|---|---|---|---|---|---|---|\n| R-1 | a denied caller gets 403 | ac | - | yes | AC-1 | diff:src/api.py:10 | access |\n\n"
                "## Contradiction matrix\n\n| R | parent story/feature | area cases (TC-*) | area open bugs |\n|---|---|---|---|\n"
                "| R-1 | contradicts:\"the parent feature says 401\" (feature 3) | silent | silent |\n")
    fence = {"missing": [{"id": "R-9", "where": "plan"}, {"id": "R-8", "where": "md"}], "candidates": [{"r": "R-7"}],
             "waiting": [{"id": "R-6", "question": "Q2"}], "by_reference": []}
    found = {"word": "extend", "target": "tests/x.py", "state": "absent", "file": "tests/x.py", "why": ""}
    problem = ("new_questions[0] has key 'x'. Expected: \"new:<n>\" with n from 1 to 99")
    old: dict = {   # the text each refusal printed before the file was sited: a byte copy of the pre-change planning_contract.py, same provocations
        'plan depth': [
            'TS-1: invalid verification depth (one of low, normal, critical)',
        ],
        'plan revision': [
            "TS-1: coverage_contract_revision is 'v0'; this factory plans against 'coverage-observation-v1' and writes the mark itself - remove the field from the row (a row planned against another revision is re-planned, not relabelled)",
        ],
        'plan obligation': [
            'TS-1: coverage_obligations required',
        ],
        'contradictions none': [
            'R-1: the register\'s matrix records contradicts:"the parent feature says 401" (feature 3), and no plan row covers R-1 — a contradiction cannot be closed by leaving it out of the plan',
        ],
        'contradictions unflagged': [
            'R-1: the register\'s matrix records contradicts:"the parent feature says 401" (feature 3); the plan row(s) TS-1 carry neither `source_conflict: true` nor `oracle_unknown: true`, so the reading you chose reaches gate A as a settled fact and nobody reviews it',
        ],
        'branches': [
            'REJECT — 2 question-branch problem(s) of the plan rows; at gate A an answer would not move the plan as written. Repair them now, while S3 still holds the context:',
            '- TS-2: Q9 is not in the register',
            '- TS-1: no branch for Q1',
        ],
        'branches new_questions': [
            'REJECT — 1 question-branch problem(s) of the plan rows; at gate A an answer would not move the plan as written. Repair them now, while S3 still holds the context:',
            '- TS-1: new_questions[0] has key \'x\'. Expected: "new:<n>" with n from 1 to 99 - the strategist\'s rework repairs this row',
        ],
        'fence plan_row': [
            'R-9: this requirement of the register has no row in the test plan. Expected: a row that names R-9 in `requirements` in work/test-plan.json and in the `R` column of test-plan.md. If it waits for a gate A question: `disposition: unverifiable`, `question_refs: ["Q2"]` and `if_answered["Q2"]` with a key for every reading letter (or `*`) and `not_needed`; the reading that keeps it in scope sets a disposition that gets a case. If it should not be checked: `disposition: skip` with the reason, and the person sees that row at gate A. A `not_planned` entry does not stand in for a row.',
        ],
        'fence r_column': [
            'R-8: this requirement of the register is named in work/test-plan.json but not in the `R` column of test-plan.md; the person reads and the delivery trace follows that table. Expected: the same id in the `R` cell of the row.',
        ],
        'fence candidate_defects': [
            'R-7: the register marks this requirement `bug:candidate-defect`, and no row plans a test for it. Expected: a row naming R-7 with `disposition: automate` or `manual-agent`; or, while a gate A question decides it, `unverifiable` with `question_refs` and an `if_answered` reading that sets `automate` or `manual-agent`. When the requirements do not state the expected result: `oracle_unknown: true` and a question; the current code is never the expected result.',
        ],
        'fence waiting_branch': [
            'R-6 waits for Q2, and no row of it has a non-empty branch for Q2. Expected: `if_answered["Q2"]` on the row with a patch for at least one reading; or, if no answer changes the row, a person\'s word: the waiver line below.',
        ],
        'regression': [
            'no `## Recommended regression` in test-plan.md: write the list, or `No regression: <reason>`',
        ],
        'targets': [
            "REJECT — 1 plan target(s) name a test the project's working tree does not have; S4 would search for it:",
            '- TS-1: `extend tests/x.py` - no file at tests/x.py under the project root or the run folder of its profile. Expected: the test as it is in the working tree, `extend <path from the project root>[::<name>]`, or a candidate id of work/context-bundle.json; when the test exists only in the change under test, `fit: new` with `fit_absent: "tests/x.py"` - the new test then writes the page objects and helpers it needs.',
        ],
        'requests': [
            'TS-1: requests[0] has no `failures` (a non-empty list of strings) - fix: {"request": "<key>", "failures": ["500", "timeout"]}',
            'TS-1: has `requests` and no `requirements` - fix: name in `requirements` the register R whose flow sends the request (the red violates that R); a request that serves no R of the story goes to top-level `request_homes` with that reason',
            'GET /api/books (src/a.js:3): no plan row fails it with 500, timeout - fix: add {"request": "GET /api/books", "failures": ["500", "timeout"]} to `requests` of the row that checks it, or {"request": "GET /api/books", "failure": "500|timeout|*", "reason": "<why>"} to top-level `request_homes`',
        ],
        'requests capped': [
            'TS-1: requests[0] has no `failures` (a non-empty list of strings) - fix: {"request": "<key>", "failures": ["500", "timeout"]}',
            '2 more problems (3 in all); fix these first, the check runs again',
        ],
        'plan_json': [
            'REJECT — 1 problem(s): the structured test plan cannot be read:',
            '- test-plan.json is not readable JSON (Expecting property name enclosed in double quotes: line 1 column 2 (char 1)); Gate A reads this file, so it cannot stay broken',
        ],
    }
    tmp = Path(tempfile.mkdtemp(prefix="tbw-t7b-"))
    saved = os.environ.get("CLAUDE_PROJECT_DIR")
    root = temp_project("tbw-t7b-")
    try:
        use_project(root)
        task = root / "qa-factory" / "artifacts" / "QA-1"
        (task / "work").mkdir(parents=True)
        (task / "test-plan.md").write_text("# Plan\n", encoding="utf-8")
        (task / "work" / "flow-requests.json").write_text(json.dumps({"requests": [
            {"method": "GET", "url_template": "/api/books", "source": "code", "path": "src/a.js", "line": 3}]}), encoding="utf-8")
        bad_requests = {"rows": [{"id": "TS-1", "requests": [{"request": "GET /api/books"}]}]}

        def told(cid):
            return SJ.told_text(SJ.row_for(cid)[0])

        def capped(limit):
            import branch_accounting as BA
            real = BA.limit
            BA.limit = lambda name, *a, **k: limit if name == "refusal_units_shown" else real(name, *a, **k)
            try:
                return PC._request_findings(task, bad_requests)
            finally:
                BA.limit = real

        # (key, the id its lines carry, the lines the function returns, how many leading lines are headers, not findings)
        rows = (
            ("plan depth", "planning_contract:plan", lambda: PC.gate_plan_errors([dict(row, verification_depth="deep")], "legacy", 1), 0),
            ("plan revision", "planning_contract:plan", lambda: PC.gate_plan_errors([dict(row, coverage_contract_revision="v0")], "legacy", 1), 0),
            # F3: an obligation line that came out of `validate_plan` as a `coverage_contract:obligations` Record keeps its own row
            ("plan obligation", "coverage_contract:obligations", lambda: [e for e in PC.gate_plan_errors(
                [dict(row, schema_version=2, coverage_obligations=[])], "legacy", 2) if "coverage_obligations required" in e], 0),
            ("contradictions none", "planning_contract:contradictions", lambda: PC.contradiction_errors([], register), 0),
            ("contradictions unflagged", "planning_contract:contradictions", lambda: PC.contradiction_errors([dict(row, requirement_refs=["R-1"])], register), 0),
            ("branches", "planning_contract:branches", lambda: PC._branch_block_lines([
                {"kind": "missing_branch", "message": "TS-1: no branch for Q1"}, {"kind": "unresolved_ref", "message": "TS-2: Q9 is not in the register"}]), 1),
            ("branches new_questions", "planning_contract:branches.new_questions", lambda: PC._branch_block_lines(
                PC.s3_branch_refusals(task, [], view=([], [], [("TS-1", "new:1", f"TS-1: {problem}")]))[0]), 1),
            ("fence plan_row", "planning_contract:fence.plan_row", lambda: PC.fence_lines(dict(fence, candidates=[], waiting=[], missing=fence["missing"][:1]))[0][1], 0),
            ("fence r_column", "planning_contract:fence.r_column", lambda: PC.fence_lines(dict(fence, candidates=[], waiting=[], missing=fence["missing"][1:]))[0][1], 0),
            ("fence candidate_defects", "planning_contract:fence.candidate_defects", lambda: PC.fence_lines(dict(fence, missing=[], waiting=[]))[0][1], 0),
            ("fence waiting_branch", "planning_contract:fence.waiting_branch", lambda: PC.fence_lines(dict(fence, missing=[], candidates=[]))[0][1], 0),
            ("regression", "planning_contract:regression", lambda: PC._regression_findings(task), 0),
            ("targets", "planning_contract:targets", lambda: PC.fit_target_block([{"where": "TS-1", "state": "absent", "line": PC._target_line("TS-1", found)}]), 1),
            ("requests", "planning_contract:requests", lambda: PC._request_findings(task, bad_requests), 0),
            ("requests capped", "planning_contract:requests", lambda: capped(1), 0),
        )
        for key, cid, produce, headers in rows:
            lines = list(produce())
            expected, door = told(cid)
            check_eq(f"t7b {cid} ({key}): the printed text is the old text", [str(x) for x in lines], old.get(key))
            check_eq(f"t7b {cid} ({key}): every finding is a Record of the row, with its sentence and door; a header stays plain",
                     [(getattr(x, "check", ""), getattr(x, "expected", ""), getattr(x, "door", "")) for x in lines],
                     [("", "", "")] * headers + [(cid, expected, door)] * (len(lines) - headers))
        # EC-5: nothing wrong, nothing returned
        check_eq("t7b no problem, no line (plan, contradictions, branches, targets, requests, regression)",
                 (PC.gate_plan_errors([row], "legacy", 1), PC.contradiction_errors([dict(row, requirement_refs=["R-1"], source_conflict=True)], register),
                  PC._branch_block_lines([]), PC.fit_target_block([]), PC.fence_lines(dict(fence, missing=[], candidates=[], waiting=[])),
                  PC._request_findings(task, {"rows": [dict(row, requests=[{"request": "GET /api/books", "failures": ["500", "timeout"]}],
                                                            requirements=["R-1"])]}),
                  PC._regression_findings(tmp)), ([], [], [], [], [], [], []))
        # the unmarked revision lines carry the id `planning_contract:plan.unmarked_revision` (t-1108 E17); their text is pinned by `tbw_siting_command_sites`
        bare = PC.gate_plan_errors([row], "new", 1)
        check_eq("t7b plan: the unmarked-revision line carries its own id", (len(bare), [getattr(x, "check", "") for x in bare]),
                 (1, ["planning_contract:plan.unmarked_revision"]))
        # plan_json: a print of the detector body; the row runs the body and watches the constructor
        (task / "work" / "test-plan.json").write_text("{not json", encoding="utf-8")
        asked, real_refusal, real_story = [], PC.refusal, PC.detector_story
        PC.refusal = lambda cid, text, **kw: (asked.append(cid), real_refusal(cid, text, **kw))[1]
        PC.detector_story = lambda *a, **k: task
        out = io.StringIO()
        try:
            with contextlib.redirect_stdout(out):
                code = PC._detector_body(None)
        finally:
            PC.refusal, PC.detector_story = real_refusal, real_story
        check_eq("t7b planning_contract:plan_json: the body prints the old two lines, exits 1, and asks the constructor for the row",
                 (out.getvalue().splitlines(), code, asked), (old.get("plan_json"), 1, ["planning_contract:plan_json"]))
    finally:
        if saved is None:
            os.environ.pop("CLAUDE_PROJECT_DIR", None)
        else:
            os.environ["CLAUDE_PROJECT_DIR"] = saved
        cleanup(root)
        shutil.rmtree(tmp, ignore_errors=True)


def tbw_t4b_sites(sg=None, capture: bool = False):
    """told-before-work T4b: each role-facing refusal of `stage_guard.check_command` that maps to a row of `stage-joints.json` (rows 25-30 of
    mech 5.3, row 28 as two sub-ids) is `refusal("<id>", <the text it always had>)`: the runner's three (`opaque`, `typed_runner`,
    `request`, written where the rule knows the requirement, carried through the ticket prefix) and the commit / stash / delivery ones
    (written in `check_command`, the caller: `rule_pathspec`, `rule_manifest`, `rule_stash` and `rule_delivery` have other callers, EC-2).
    ONE table, a row per site, driven through the REAL `check_command` and its `deny`: the stderr is `STAGE GUARD: ` + the old text byte for
    byte (the digest in `old`, captured by running the same rows over a byte copy of the file taken before the edit; EC-1), then the
    row's `  expected:` / `  door:` and `  check: <id>` last (EC-6); the code is DENY. Controls: a command nothing refuses prints nothing
    and allows (EC-5). `sg` is the module under test (the scratch capture of `old` passes the byte copy and `capture=True`: `{row: digest}`).
    The walker's door (`SG-walker-error`) is the last row, driven through the real `check` with the walker raising; every dispatch-time refusal stays bare: a refusal with no row prints no `check:` line."""
    import contextlib
    import hashlib
    import io
    from unittest import mock
    import hooklib
    import stage_joints as SJ
    from harness import reader_patched, use_project
    if sg is None:
        import stage_guard as sg
    old = {   # row -> sha256[:16] of the problem text the pre-change file printed (a byte copy of stage_guard.py, same rows)
        "opaque": "13194e9a98d58b21",
        "typed_runner no path": "a6332152cf00feea",
        "typed_runner region": "0656d3600256ff56",
        "request missing file": "45fb2f1593e58732",
        "request unreadable": "f188b6c039344c52",
        "request no requests": "5b2c099e9922b22e",
        "request other dispatch": "52a392fac1c0e2e0",
        "request selection not a list": "8c31c182696ee4aa",
        "request outside scope": "a392b839c038f258",
        "commit pathspec": "de89fde49f65e866",
        "commit manifest": "3e92949a32bb21fd",
        "stash": "94d0fa72ac580e08",
        "delivery": "e364cb85432891cb",
    }
    saved_env, saved_cache = os.environ.get("CLAUDE_PROJECT_DIR"), hooklib._PROJECT_ROOT_CACHE
    from harness import cleanup, temp_project
    root = temp_project("tbw-t4b-")
    try:
        use_project(root)
        task = root / "qa-factory" / "artifacts" / "QA-3"
        (task / "work").mkdir(parents=True)
        (task / "state").mkdir()
        (task / "pipeline.json").write_text(json.dumps({"ticket": "QA-3", "stages": {"S1": {"status": "running"}}}), encoding="utf-8")
        (task / "work" / "ledger.json").write_text(json.dumps(
            {"delivery_verdict": "no", "delivery_ready": False, "rows": [], "reasons": ["x"]}), encoding="utf-8")
        (task / "state" / "controller.json").write_text(json.dumps({"dispatches": {"d-1": {
            "id": "d-1", "stage": "S5", "role": "qa-automator", "status": "running", "scope": ["TC-012"]}}}), encoding="utf-8")

        def request(name, body):
            path = root / name
            path.write_text(body if isinstance(body, str) else json.dumps(body), encoding="utf-8")
            return path.as_posix()

        bad_json = request("bad.json", "{not json")
        empty = request("empty.json", {"requests": []})
        other = request("other.json", {"dispatch_id": "zz", "selected_instance_ids": ["TC-012"]})
        notlist = request("notlist.json", {"dispatch_id": "d-1", "selected_instance_ids": "TC-012"})
        outside = request("outside.json", {"dispatch_id": "d-1", "selected_instance_ids": ["TC-099::t[x]"]})
        inside = request("inside.json", {"dispatch_id": "d-1", "selected_instance_ids": ["TC-012::t[x]"]})
        p = "stage_guard:SG-command."
        # (row, the id its refusal carries, the command, a stub of `rule_manifest` or None)
        rows = (
            ("opaque", p + "opaque", "echo a\\(b; python run_suite.py --mine TC-012", None),
            ("typed_runner no path", p + "typed_runner", "python run_suite.py --task X --label all", None),
            ("typed_runner region", p + "typed_runner", "python run_suite.py --request $(echo f.json)", None),
            ("request missing file", p + "request", "python run_suite.py --request work/requests/nothing.json", None),
            ("request unreadable", p + "request", f"python run_suite.py --request {bad_json}", None),
            ("request no requests", p + "request", f"python run_suite.py --request {empty}", None),
            ("request other dispatch", p + "request", f"python run_suite.py --request {other}", None),
            ("request selection not a list", p + "request", f"python run_suite.py --request {notlist}", None),
            ("request outside scope", p + "request", f"python run_suite.py --request {outside}", None),
            ("commit pathspec", p + "commit.pathspec", "git commit -a -m x tests/t.py", None),
            ("commit manifest", p + "commit.manifest", "git commit -m x -- tests/t.py", "committing test code: unresolved cases without a reason"),
            ("stash", p + "stash", "git stash push -u", None),
            ("delivery", p + "delivery", "gh pr create --fill", None),
        )
        digests = {}

        def run(command, stub=None):
            event = {"tool_name": "Bash", "cwd": str(root), "task_id": "QA-3", "tool_input": {"command": command}}
            buf = io.StringIO()
            patch = mock.patch.object(sg, "rule_manifest", return_value=stub) if stub is not None else contextlib.nullcontext()
            with contextlib.redirect_stderr(buf), patch:
                code = sg.check_command(event)
            text = buf.getvalue()
            for spelling in (str(root), str(root).replace("\\", "/")):
                text = text.replace(spelling, "<ROOT>")
            return code, text

        for name, cid, command, stub in rows:
            code, err = run(command, stub)
            problem = err[:-1] if err.endswith("\n") else err
            problem = problem.split("\n  expected: ")[0].split("\n  check: ")[0]
            assert problem.startswith("STAGE GUARD: "), (name, err)
            digests[name] = hashlib.sha256(problem[len("STAGE GUARD: "):].rstrip().encode("utf-8")).hexdigest()[:16]
            if capture:
                continue
            row, why = SJ.row_for(cid)
            expected, door = SJ.told_text(row) if row else ("", "")
            tail = "\n  expected: " + expected + ("\n  door: " + door if door else "") + "\n  check: " + cid + "\n"
            check_eq(f"t4b {name} {cid}: the guard denies", code, sg.DENY)
            check(f"t4b {name} {cid}: the row states a sentence", bool(expected), str(why))
            check(f"t4b {name} {cid}: the row's lines follow the problem, `check:` last", err.endswith(tail), err[-300:])
            check_eq(f"t4b {name} {cid}: the problem text is the old one", digests[name], old.get(name))
        if capture:
            return digests
        # EC-5: nothing refused, nothing printed
        for command in ("python run_suite.py --mine TC-012", f"python run_suite.py --request {inside}", "git stash push -u -- src/a.py"):
            check_eq(f"t4b control {command[:44]!r}: allowed, nothing printed", run(command), (sg.ALLOW, ""))
        # the walker's door (`SG-walker-error`, F3 of the topic critic): the REAL `check` with the walker made to raise - a deny whose
        # problem is `WALKER_DOOR` filled with the walker's own failure, then the row's lines from stage-joints.json, `check:` last
        wid = "stage_guard:SG-walker-error"
        wrow, wwhy = SJ.row_for(wid)
        wexpected, wdoor = SJ.told_text(wrow) if wrow else ("", "")

        def boom(self, *args, **kwargs):
            raise IndexError("synthetic walker failure")
        with reader_patched("_code", lambda real: boom):
            with contextlib.redirect_stderr(io.StringIO()) as buf:
                wcode = sg.check({"tool_name": "Bash", "cwd": str(root), "tool_input": {"command": "git commit -m x tests/t.py"}})
        wtail = ("\n  expected: " + wexpected + ("\n  door: " + wdoor if wdoor else "") + "\n  check: " + wid + "\n")
        wproblem = "STAGE GUARD: " + hooklib.WALKER_DOOR.format(reason="IndexError: synthetic walker failure")
        check_eq(f"t4b the walker's door {wid}: the guard denies", wcode, sg.DENY)
        check(f"t4b the walker's door {wid}: the row states a sentence", bool(wexpected), str(wwhy))
        check(f"t4b the walker's door {wid}: the old problem text, then the row's lines, `check:` last",
              buf.getvalue() == wproblem + wtail, buf.getvalue()[-300:])
        check_eq("t4b every id of the table is a row of stage-joints.json",
                 sorted({cid for _name, cid, _c, _s in rows if SJ.row_for(cid)[0] is None}), [])
    finally:
        if saved_env is None:
            os.environ.pop("CLAUDE_PROJECT_DIR", None)
        else:
            os.environ["CLAUDE_PROJECT_DIR"] = saved_env
        hooklib._PROJECT_ROOT_CACHE = saved_cache
        cleanup(root)


if __name__ == "__main__":
    main()

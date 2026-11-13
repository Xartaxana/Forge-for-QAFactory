#!/usr/bin/env python3
"""TR3-10 E: the S3 plan row's optional `walk_data` / `walk_global` - checked by SHAPE only, carried whole into request.json, and the
strategist is told they exist (FR-38, AR-10; AR-29: nothing here judges whether what the strategist wrote is RIGHT).
KEYS: walk_data_shape_each_bad_refused, walk_global_blank_refused, absent_field_no_constraint, prepare_request_carries_both_whole,
strategist_line_present, release_note_names_raise, unprepared_request_carries_walk_fields, walk_line_in_s3_head_once,
shape_check_any_disposition.
Mutations (each killed by THIS file): `exclusive` accepted as text -> walk_data_shape_each_bad_refused; a blank `walk_global`
accepted -> walk_global_blank_refused; an absent field refused -> absent_field_no_constraint; the request built without the fields or
with reworded text -> prepare_request_carries_both_whole; the brief line dropped -> strategist_line_present; the release note without the raise
named -> release_note_names_raise; `_unprepared_document` without `_walk_fields` ->
unprepared_request_carries_walk_fields; the line back inside `request_lines` or dropped from the S3 head ->
walk_line_in_s3_head_once; the shape check back on `manual-agent` rows only -> shape_check_any_disposition."""
import copy
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "fixtures" / "manual-evidence"))
import harness  # noqa: E402
from harness import SCRIPTS, check, check_eq, check_in, finish  # noqa: E402
import scaffold as S  # noqa: E402

sys.path.insert(0, str(SCRIPTS))
import brief_pack as BP  # noqa: E402
import manual_evidence as M  # noqa: E402
import planning_contract as PC  # noqa: E402

PACKAGE = SCRIPTS.parent
GOOD_ENTRY = {"kind": "book", "exclusive": True, "changes": "deletes one book"}


def manual_row(**fields):
    """The plan's manual-agent row of the api case (TS-12) with `fields` added, and the plan the check reads."""
    t = S.make_task(manual=("api",))
    try:
        row = copy.deepcopy(t.row("TS-12"))
    finally:
        S.cleanup(t)
    row.update(fields)
    return row


def problems(row) -> list:
    """The walk-field problems of the plan check on this one row (the shape check lives inside `validate_plan`)."""
    return [e for e in PC.validate_plan([row]) if "walk_data" in e or "walk_global" in e]


def walk_data_shape_each_bad_refused():
    check_eq("good walk_data: no problem", problems(manual_row(walk_data=[GOOD_ENTRY])), [])
    check_eq("good walk_data with `exclusive: false` and an empty `changes`: no problem",
             problems(manual_row(walk_data=[{"kind": "x", "exclusive": False, "changes": ""}])), [])
    bad = {
        "a non-list walk_data (object)": ({"walk_data": GOOD_ENTRY}, "walk_data must be a list"),
        "a non-list walk_data (text)": ({"walk_data": "book"}, "walk_data must be a list"),
        "a null walk_data": ({"walk_data": None}, "walk_data must be a list"),
        "an entry that is not an object": ({"walk_data": ["book"]}, "walk_data[0] must be an object"),
        "a blank kind": ({"walk_data": [dict(GOOD_ENTRY, kind="  ")]}, "walk_data[0].kind"),
        "a missing kind": ({"walk_data": [{"exclusive": True, "changes": "x"}]}, "walk_data[0].kind"),
        "a kind that is not text": ({"walk_data": [dict(GOOD_ENTRY, kind=3)]}, "walk_data[0].kind"),
        "an exclusive given as text": ({"walk_data": [dict(GOOD_ENTRY, exclusive="true")]}, "walk_data[0].exclusive"),
        "an exclusive given as a number": ({"walk_data": [dict(GOOD_ENTRY, exclusive=1)]}, "walk_data[0].exclusive"),
        "a missing exclusive": ({"walk_data": [{"kind": "book", "changes": "x"}]}, "walk_data[0].exclusive"),
        "a changes that is not text": ({"walk_data": [dict(GOOD_ENTRY, changes=["x"])]}, "walk_data[0].changes"),
        "a missing changes": ({"walk_data": [{"kind": "book", "exclusive": True}]}, "walk_data[0].changes"),
        "the second entry bad": ({"walk_data": [GOOD_ENTRY, dict(GOOD_ENTRY, exclusive="yes")]}, "walk_data[1].exclusive"),
    }
    for label, (fields, needle) in bad.items():
        row = manual_row(**fields)
        found = problems(row)
        check(f"{label}: refused", bool(found), str(found))
        check_in(f"{label}: names the field", needle, " ".join(found))
        check_in(f"{label}: names the row", row["id"] + ":", " ".join(found))
        check(f"{label}: gives the right shape (an example)", "e.g." in " ".join(found), str(found))
        check_in(f"{label}: refused by the plan check as a whole", needle, " ".join(PC.validate_plan([row])))
    # E.4: a kind of 200+ characters, with `/` or quotes, is kept as given: the shape check does not touch it
    for kind in ("k" * 250, "a/b", 'say "hi"', "it's"):
        check_eq(f"E.4 kind {kind[:12]!r}: well-formed, no problem", problems(manual_row(walk_data=[dict(GOOD_ENTRY, kind=kind)])), [])


def shape_check_any_disposition():
    """F12: the carrier takes the fields from every row that owns the case's obligations, so the shape check runs on every row that
    carries them, whatever its disposition."""
    other = manual_row(disposition="automate", walk_data="nonsense")
    found = problems(other)
    check("a non-manual-agent row with a malformed walk_data is refused", bool(found), str(found))
    check_in("... naming the row and the field", other["id"] + ": walk_data must be a list", " ".join(found))
    blank = problems(manual_row(disposition="automate", walk_global=""))
    check("`walk_global: \"\"` on a non-manual-agent row is refused by shape", bool(blank), str(blank))
    check_eq("a good field on a non-manual-agent row: no problem",
             problems(manual_row(disposition="automate", walk_data=[GOOD_ENTRY], walk_global="x")), [])
    check_eq("absent fields on a non-manual-agent row: no constraint", problems(manual_row(disposition="automate")), [])


def walk_global_blank_refused():
    check_eq("a reason: no problem", problems(manual_row(walk_global="the Then counts every book")), [])
    for label, value in (("empty", ""), ("blanks", "   "), ("null", None), ("a number", 3), ("a list", ["x"])):
        row = manual_row(walk_global=value)
        found = problems(row)
        check(f"walk_global {label}: refused", bool(found), str(found))
        check_in(f"walk_global {label}: names the field", "walk_global must be non-blank text", " ".join(found))
        check(f"walk_global {label}: gives an example", "e.g." in " ".join(found), str(found))
        check_in(f"walk_global {label}: refused by the plan check as a whole", "walk_global", " ".join(PC.validate_plan([row])))


def absent_field_no_constraint():
    row = manual_row()
    check("the scaffold row names neither field", "walk_data" not in row and "walk_global" not in row)
    check_eq("E.1 absent fields: no problem", problems(row), [])
    check_eq("E.3 `walk_data: []` is not said: no problem", problems(manual_row(walk_data=[])), [])
    check("absent fields add nothing to the plan check", not any("walk_" in e for e in PC.validate_plan([row])))
    t = S.make_task(manual=("api",))
    try:
        with t.patched():
            request = M.prepare_request(t.task, S.CASES["api"], ["OB-12"])
        check("the request of a plan with no field carries neither key (no constraint)", "walk_data" not in request and "walk_global" not in request,
              str(sorted(request)))
        t.row("TS-12")["walk_data"] = []
        t.write_plan()
        with t.patched():
            request = M.prepare_request(t.task, S.CASES["api"], ["OB-12"])
        check("E.3 `walk_data: []` carries no key either", "walk_data" not in request)
    finally:
        S.cleanup(t)


def prepare_request_carries_both_whole():
    data = [dict(GOOD_ENTRY, kind="Book / \"odd\" " + "k" * 250, changes="removes it; the count drops"),
            {"kind": "cart", "exclusive": False, "changes": "adds a line"}]
    reason = "the Then counts every book, in every lane"
    t = S.make_task(manual=("api",))
    try:
        row = t.row("TS-12")
        row["walk_data"], row["walk_global"] = copy.deepcopy(data), reason
        t.write_plan()
        with t.patched():
            request = M.prepare_request(t.task, S.CASES["api"], ["OB-12"])
        check_eq("walk_data travels whole (no rewording, no cut, no reorder)", request.get("walk_data"), data)
        check_eq("walk_global travels whole", request.get("walk_global"), reason)
        row["walk_data"] = [{"kind": "x", "exclusive": "yes", "changes": "y"}]
        t.write_plan()
        try:
            with t.patched():
                M.prepare_request(t.task, S.CASES["api"], ["OB-12"])
            check("a malformed field is refused with the plan's own check, never carried", False)
        except M.Refused as exc:
            check_in("a malformed field: the refusal names the field and the shape", "walk_data[0].exclusive", exc.args[2] if len(exc.args) > 2 else str(exc))
    finally:
        S.cleanup(t)


def unprepared_request_carries_walk_fields():
    """F10 (AR-21, FR-49, AR-28): a case through the unprepared (walkable) door carries walk_data / walk_global whole, so it is never
    walked with 'no constraint' when its row said `exclusive: true`."""
    data = [dict(GOOD_ENTRY, kind="Book / \"odd\"", changes="removes it; the count drops")]
    reason = "the Then counts every book"
    t = S.make_task(manual=("ui",))
    try:
        row = t.row("TS-7")
        policy = {"not": "one word"}
        row["evidence_policy"] = policy
        for ob in row["coverage_obligations"]:
            ob["evidence_policy"] = policy
        row["walk_data"], row["walk_global"] = copy.deepcopy(data), reason
        t.write_plan()
        case = S.CASES["ui"]
        with t.patched():
            try:
                M.prepare_to_file(t.task, case, ["OB-7"])
                check("the dict policy leaves the case unprepared (the walkable door)", False)
            except M.Refused as exc:
                check("the refusal is the walkable one", exc.walkable is True)
        doc = json.loads(M.request_path(t.task, case).read_text(encoding="utf-8"))
        check("the document is the unprepared one", "unprepared" in doc and "refused" not in doc, str(sorted(doc)))
        check_eq("unprepared: walk_data kept whole (with `exclusive: true`)", doc.get("walk_data"), data)
        check_eq("unprepared: walk_global kept whole", doc.get("walk_global"), reason)
        row.pop("walk_data"), row.pop("walk_global")
        t.write_plan()
        with t.patched():
            try:
                M.prepare_to_file(t.task, case, ["OB-7"])
            except M.Refused:
                pass
        doc = json.loads(M.request_path(t.task, case).read_text(encoding="utf-8"))
        check("unprepared with no field said: neither key (no constraint)", "walk_data" not in doc and "walk_global" not in doc, str(sorted(doc)))
    finally:
        S.cleanup(t)


def s3_head(flow_raises: bool) -> list:
    """The S3 brief of the strategist as `brief_pack.build` makes it, with the flow requests working or raising."""
    import judge
    from unittest.mock import patch
    import user_path_failures as UPF
    root = harness.temp_project("walk-line-")
    try:
        harness.use_project(root)
        task = root / "qa-factory" / "artifacts" / "QA-9"
        (task / "work").mkdir(parents=True)
        (task / "pipeline.json").write_text(json.dumps(
            {"ticket": "QA-9", "size": "S", "environment": "local", "implementation_source": "diff",
             "stages": {"S0": {"status": "pending"}}, "gates": {}, "halts": []}), encoding="utf-8")
        with patch.object(judge, "active", return_value=False):
            if flow_raises:
                with patch.object(UPF, "flow_requests", side_effect=RuntimeError("boom")):
                    built = BP.build("QA-9", "S3", "qa-test-strategist", "S3-qa-test-strategist-1", write=False)
            else:
                built = BP.build("QA-9", "S3", "qa-test-strategist", "S3-qa-test-strategist-1", write=False)
        return built["markdown"].splitlines()
    finally:
        harness.cleanup(root)


def walk_line_in_s3_head_once():
    """F11: the strategist line is emitted ONCE in the S3 head (so it shows when the flow requests fail), and is no part of
    `request_lines` (so `user_path_failures` does not print it)."""
    for flow_raises in (False, True):
        lines = s3_head(flow_raises)
        mine = [x for x in lines if x.startswith("Walk data: ")]
        label = "flow requests failing" if flow_raises else "flow requests working"
        check_eq(f"{label}: the S3 brief carries the line exactly once", len(mine), 1)
        check_eq(f"{label}: and it is the constant", mine[:1], [BP.WALK_DATA_LINE])
        if flow_raises:
            check("flow requests failing: their own `not measured` line is there too",
                  any(x.startswith("Flow requests: not measured") for x in lines))
    req = {"key": "GET /api/r1", "method": "GET", "url_template": "/api/r1", "path": "App/src/a.ts", "line": 1}
    story_base = harness.mark_project(harness.temp_dir("qa-walk-fields-"))
    story = story_base / "qa-factory" / "artifacts" / "QA-9"
    for found in ({"requests": [], "unmeasured": []}, {"requests": [req], "unmeasured": []}):
        check("request_lines carries no walk line", not any(x.startswith("Walk data: ") for x in BP.request_lines(found, story)))
    harness.cleanup(story_base)
    src = (SCRIPTS / "user_path_failures.py").read_text(encoding="utf-8")
    check("user_path_failures carries no walk line of its own", "Walk data" not in src)


def strategist_line_present():
    check("the line names both fields and the shape",
          all(s in BP.WALK_DATA_LINE for s in ("`walk_data`", "`walk_global`", "kind", "exclusive", "changes")), BP.WALK_DATA_LINE)
    req = {"key": "GET /api/r1", "method": "GET", "url_template": "/api/r1", "path": "App/src/a.ts", "line": 1}
    story_base = harness.mark_project(harness.temp_dir("qa-walk-fields-"))
    with_requests = BP.request_lines({"requests": [req], "unmeasured": []}, story_base / "qa-factory" / "artifacts" / "QA-9")
    harness.cleanup(story_base)
    check("the closing line of the flow requests stays last", "each one gets a plan row" in with_requests[-1], with_requests[-1][:60])
    charter = (PACKAGE / "agents" / "qa-test-strategist.md").read_text(encoding="utf-8")
    check_in("the charter carries the experience sentence, exactly",
             "a manual check that changes a record other checks read says which kind and whether it must be its own.", charter)


def release_note_names_raise():
    """AR-20: the release note of this change names the strategist's raise as `old -> new` (the numbers themselves are the
    ratchet's business: `role-load.json` is judged by `role_load.py::process_ratchet_problems` (test_role_load.py test_process_ratchet)
    and by audit A22; no number of it is pinned here)."""
    # A release folds the fragment into CHANGELOG.md, so the note is read through the one reader that follows it there.
    note = harness.release_note(PACKAGE / "changelog.d" / "tr3-10e-walk-data-field.md", "an optional `walk_data` (a list of")
    check("the release note names the raise as old -> new", re.search(r"rises \d+ -> \d+ tokens", note) is not None, note[-200:])


def main():
    walk_data_shape_each_bad_refused()
    walk_global_blank_refused()
    absent_field_no_constraint()
    shape_check_any_disposition()
    prepare_request_carries_both_whole()
    unprepared_request_carries_walk_fields()
    walk_line_in_s3_head_once()
    strategist_line_present()
    release_note_names_raise()
    finish("test_walk_plan_fields")


if __name__ == "__main__":
    main()

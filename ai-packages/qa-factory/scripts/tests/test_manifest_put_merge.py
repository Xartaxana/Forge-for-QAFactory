#!/usr/bin/env python3
"""`manifest_put`: the door that takes an `unresolved[]` row away, the replacement of a re-sent row's slice, and the refusal
of two reasons for one case (HF2-3, GW1-22, FB-5; spec t-085 rev. 3, part 3b).

TP1-12586 (22-24.10.2026): the author recorded the Thens behind TC-004's red one by one (`blocked_by_check`), and the
`contradicts_requirement` row of TC-004 (and the stale partition row of TC-005) stood on, because `unresolved[]` had no way
out for a row that names a slice: a green `tests[]` entry does not take it, and a re-sent row kept the old `partitions`
beside the new `instance_ids`.

Keys: K1 the retraction, K2 send-and-retract refused, K3 a key that names no row / an already gone one, K2b the replay,
K4 two reasons refused in `run` before the commit, K4b the fold of an old event with two reasons, K8 the replacement of a
slice in two independent groups, K8b `_partition_scoped` reads the one constant. The fixtures are `test_mixed_then_outcomes`'.

HF2-5 (spec t-085 rev. 3, part 5a, K1 / K5): `then_bindings` is merged by unit and no longer replaced whole. Keys: 5a-K1 (a) the
writer's fragment replaces the array, (b) a hand fragment of blocked rows leaves the covered rows of another test of the same
case, (c) a hand fragment of one case leaves the other cases, (d) a fragment without `then_bindings` leaves the array, (e)
two handed Thens of one case (null `instance_id`): the one the hand fragment does not send is taken out and named, and with
both sent nothing is; and the replay of an old journal that holds such a hand fragment folds by the new rule.

HF3-2 (spec t-1248 part B): a retracted instance takes the `then_bindings` rows of its spelling with it, while no remaining
row wears that spelling. Keys: B-K1 the retirement and its print, B-K4 a spelling a live row still wears keeps its rows,
B-K5 a fragment that binds a Then to the id it retracts (refused by `run`, kept by `merge` on replay), B-K7 the empties.
"""
import copy
import inspect
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import check, check_eq, check_in, check_not_in, finish  # noqa: E402

sys.path.insert(0, str(harness.SCRIPTS))
import acceptance as AC  # noqa: E402
import contract as C  # noqa: E402
import manifest_put as MP  # noqa: E402
from test_manifest_projection import Stand  # noqa: E402
from test_mixed_then_outcomes import G5, MS, RED_ROW, items, shape_a, shape_b, with_stale_rows  # noqa: E402

CONTRADICTS, BLOCKED = "contradicts_requirement", "blocked_by_env"
GREEN_TC9 = {"instance_id": "test_nine[x]", "file": "tests/test_nine.py", "covers": ["TC-009"], "status": "green"}


def stale_story() -> dict:
    """TC-004's row (`instance_ids: [MS]`, `thens: [2]`) and the live stale form for TC-005 (`partitions`, no `thens`)."""
    return with_stale_rows(shape_b(), ["TC-005"])["manifest"]


def cases(manifest: dict) -> list:
    return [MP._case(r) for r in manifest.get("unresolved") or []]


def row_of(manifest: dict, case: str) -> dict:
    return next(r for r in manifest.get("unresolved") or [] if MP._case(r) == case)


def refusal(fn, *args) -> str:
    try:
        fn(*args)
    except ValueError as exc:
        return str(exc)
    return ""


def journal(*fragments, seed=None) -> list:
    events = [{"type": "manifest_seed", "sequence": 1, "idempotency_key": "s", "payload": {"manifest": seed}}] if seed else []
    return events + [{"type": "manifest_patch", "sequence": len(events) + n, "idempotency_key": f"k{n}",
                      "payload": {"fragment": f}} for n, f in enumerate(fragments, 1)]


# --- K1: the retraction ----------------------------------------------------------------------------------------------

def k1_retraction() -> None:
    story = stale_story()
    merged, summary = MP.merge(copy.deepcopy(story), {"retracted_unresolved": ["TC-005"]})
    check_eq("K1: the stale partition row of TC-005 is dropped, the red one of TC-004 stays", cases(merged), ["TC-004"])
    check_eq("K1: the key joins the manifest's history", merged.get("retracted_unresolved"), ["TC-005"])
    check_eq("K1: the summary counts the rows dropped", summary.get("retracted_unresolved"), 1)
    check_eq("K1: nothing else of the manifest moved", (merged["tests"], merged["then_bindings"]),
             (story["tests"], story["then_bindings"]))
    again, _ = MP.merge(merged, {"retracted_unresolved": ["TC-004"], "run_witness": "w.json"})
    check_eq("K1: a second retraction appends to the history, and the key is not copied as a scalar",
             (cases(again), again.get("retracted_unresolved"), again.get("run_witness")), ([], ["TC-005", "TC-004"], "w.json"))
    check_eq("K1: the row went WHOLE - the red instance of TC-004 is no longer explained by any row",
             (AC.red_by_requirement(story, items(), AC.story_scope(story), strict=False) != {},
              AC.red_by_requirement(again, items(), AC.story_scope(again), strict=False)), (True, {}))

    empty, summary0 = MP.merge(copy.deepcopy(story), {"retracted_unresolved": []})
    check_eq("K1: `retracted_unresolved: []` retracts nothing", (empty, summary0.get("retracted_unresolved")), (story, None))

    both = {"unresolved": [{"case": "speakers/TC-001", "reason": CONTRADICTS, "partitions": ["P-a"]},
                           {"case": "venues/TC-001", "reason": BLOCKED, "instance_ids": ["t[a]"]},
                           {"case": "venues/TC-002", "reason": "impossible"}]}
    bare, summary2 = MP.merge(copy.deepcopy(both), {"retracted_unresolved": ["TC-001"]})
    check_eq("K1: a bare key finds the row of every area and says so in the count", (cases(bare), summary2["retracted_unresolved"]),
             (["venues/TC-002"], 2))
    named, _ = MP.merge(copy.deepcopy(both), {"retracted_unresolved": ["venues/TC-001"]})
    check_eq("K1: an area-qualified key finds that area's row only", cases(named), ["speakers/TC-001", "venues/TC-002"])
    lines = MP.retracted_unresolved_lines(both, {"retracted_unresolved": ["TC-001"]})
    check_eq("K1: `run` names each row of a bare key with its slice", len(lines), 2)
    check_in("K1: the print carries the slice and the reason", 'partitions ["P-a"]', lines)
    check_in("K1: and the other area's instance row", 'instance_ids ["t[a]"]', lines)
    check_in("K1: the print carries the Thens of the dropped row",
             "thens [2]", MP.retracted_unresolved_lines(story, {"retracted_unresolved": ["TC-004"]}))
    check_in("K1: a whole-case row is said to be whole",
             "the whole case", MP.retracted_unresolved_lines(both, {"retracted_unresolved": ["venues/TC-002"]}))
    check_eq("K1: a fragment that retracts nothing prints nothing", MP.retracted_unresolved_lines(story, {"tests": []}), [])


# --- K2, K3: what the retraction refuses -------------------------------------------------------------------------------

def k2_k3_refusals() -> None:
    story = stale_story()
    text = refusal(MP.merge, copy.deepcopy(story),
                   {"retracted_unresolved": ["TC-005"], "unresolved": [{"case": "TC-005", "reason": CONTRADICTS}]})
    check_eq("K2: send and retract the row of one case in one fragment -> the refusal",
             text, "one fragment cannot both send and retract the unresolved row of TC-005 - send the new row, or retract the old one")
    check_in("K2: an area-qualified row is the same case as a bare key",
             "cannot both send and retract", refusal(MP.merge, copy.deepcopy(story),
                                                     {"retracted_unresolved": ["TC-005"],
                                                      "unresolved": [{"case": "area/TC-005", "reason": BLOCKED}]}))
    check_eq("K2: the neighbour (another case sent, this one retracted) is no clash", refusal(
        MP.merge, copy.deepcopy(story), {"retracted_unresolved": ["TC-005"], "unresolved": [{"case": "TC-006", "reason": BLOCKED}]}), "")

    text = refusal(MP.merge, copy.deepcopy(story), {"retracted_unresolved": ["TC-099"]})
    check_in("K3: a key that names no row and no history is refused", "names no unresolved[] row this manifest holds: TC-099", text)
    check_in("K3: and the door is the view", "manifest_view.py --task <T>", text)
    gone, _ = MP.merge(copy.deepcopy(story), {"retracted_unresolved": ["TC-005"]})
    text = refusal(MP.merge, gone, {"retracted_unresolved": ["TC-005"]})
    check_in("K3: a key an earlier revision already dropped -> already gone", "TC-005 is already gone", text)
    check_not_in("K3: and it is not told apart as 'names no row'", "names no unresolved[] row", text)
    check_in("K3: one bad key among good ones refuses the whole fragment (nothing half-dropped)", "TC-099",
             refusal(MP.merge, copy.deepcopy(story), {"retracted_unresolved": ["TC-005", "TC-099"]}))
    check_in("K3: a value that is no list is refused, not read letter by letter", "is a list of case keys",
             refusal(MP.merge, copy.deepcopy(story), {"retracted_unresolved": "TC-005"}))

    # The rename rule of `_retract_instances`: this fragment's own green test already moved the case out - satisfied.
    held = {"unresolved": [{"case": "TC-009", "reason": "impossible"}]}
    moved, summary = MP.merge(held, {"tests": [GREEN_TC9], "retracted_unresolved": ["TC-009"]})
    check_eq("K3: a retraction the merge itself already satisfied is recorded, counted as nothing, not refused",
             (cases(moved), moved.get("retracted_unresolved"), summary.get("retracted_unresolved")), ([], ["TC-009"], None))


# --- K2b: the replay ----------------------------------------------------------------------------------------------------

def k2b_replay() -> None:
    story = stale_story()
    fragment = {"retracted_unresolved": ["TC-005"], "run_witness": "w.json"}
    direct, _ = MP.merge(copy.deepcopy(story), fragment)
    direct["revision"] = 1
    folded = MP.fold(journal(fragment, seed=copy.deepcopy(story)))
    check_eq("K2b: the fold of a committed retraction is the merge's manifest, nothing unprojected",
             ({k: v for k, v in folded.items() if k != "revision"}, "unprojected_events" in folded),
             ({k: v for k, v in direct.items() if k != "revision"}, False))
    check_eq("K2b: the fold is deterministic - replayed twice, the same manifest",
             MP.fold(journal(fragment, seed=copy.deepcopy(story))), folded)


# --- K4, K4b: two reasons for one case ---------------------------------------------------------------------------------

def k4_two_reasons() -> None:
    both = {"unresolved": [{"case": "TC-005", "reason": CONTRADICTS, "detail": "d"},
                           {"case": "TC-005", "reason": BLOCKED, "instance_ids": ["t[a]"]}]}
    problems = MP.unresolved_reason_conflicts(both)
    check_eq("K4: two reasons of one case -> one problem", len(problems), 1)
    check_in("K4: it names the case, both reasons and the door", "TC-005", problems)
    check_in("K4: both reasons", f"{CONTRADICTS} and {BLOCKED}", problems)
    check_in("K4: the door", "send one row per case: the stand row OR the requirement row; `retracted_unresolved` drops the old one", problems)
    check_eq("K4: two `blocked_by_env` rows are united, not refused", MP.unresolved_reason_conflicts(
        {"unresolved": [{"case": "TC-5", "reason": BLOCKED, "instance_id": "a"}, {"case": "TC-5", "reason": BLOCKED, "instance_id": "b"}]}), [])
    check_eq("K4: two rows of one reason - the later wins as always, no refusal", MP.unresolved_reason_conflicts(
        {"unresolved": [{"case": "TC-5", "reason": CONTRADICTS, "thens": [1]}, {"case": "TC-5", "reason": CONTRADICTS, "thens": [2]}]}), [])
    check_eq("K4: two reasons of two DIFFERENT cases are no conflict", MP.unresolved_reason_conflicts(
        {"unresolved": [{"case": "TC-5", "reason": CONTRADICTS}, {"case": "TC-6", "reason": BLOCKED}]}), [])
    check_eq("K4: three reasons of one case are still one problem naming all three", len(MP.unresolved_reason_conflicts(
        {"unresolved": [{"case": "TC-5", "reason": r} for r in (CONTRADICTS, BLOCKED, "impossible")]})), 1)
    check_in("K4: a row with no reason differs from a named one (refused, not guessed at)", "(none)", MP.unresolved_reason_conflicts(
        {"unresolved": [{"case": "TC-5", "reason": CONTRADICTS}, {"case": "TC-5"}]}))
    for odd in ({}, {"unresolved": None}, {"unresolved": "TC-5"}, {"unresolved": [None, 3, {"reason": BLOCKED}]}, None):
        check_eq(f"K4: an unreadable `unresolved` ({odd!r}) conflicts with nothing", MP.unresolved_reason_conflicts(odd), [])

    with Stand() as stand:
        first = stand.put({"unresolved": [{"case": "TC-001", "reason": "impossible", "detail": "d"}]})
        before = (stand.journal(), stand.tree())
        code, out, err = stand.put(both)
        check_eq("K4: `run` refuses the fragment with EXIT_BAD_FRAGMENT", (first[0], code), (0, MP.EXIT_BAD_FRAGMENT))
        check_in("K4: the refusal names the case, the reasons and the door", "TC-005 with different reasons (contradicts_requirement and "
                 "blocked_by_env)", err)
        check_in("K4: and the repair marker", MP.REPAIR_MARKER, err)
        check_eq("K4: BEFORE the commit - the journal and the tree are exactly as they were", (stand.journal(), stand.tree()), before)
        united = {"unresolved": [{"case": "TC-005", "reason": BLOCKED, "instance_id": "t[a]"},
                                 {"case": "TC-005", "reason": BLOCKED, "instance_id": "t[b]"}]}
        check_eq("K4: two `blocked_by_env` rows of one case still commit", stand.put(united)[0], 0)
        check_eq("K4: and their instances are united", row_of(stand.manifest(), "TC-005").get("instance_ids"), ["t[a]", "t[b]"])


def k4b_old_events_fold() -> None:
    """An event committed before the rule (two reasons of one case) folds as it always did: the later wins, nothing unprojected."""
    patch = {"unresolved": [{"case": "TC-5", "reason": CONTRADICTS, "detail": "d"}, {"case": "TC-5", "reason": BLOCKED, "instance_ids": ["t[a]"]}]}
    seed = {"unresolved": [{"case": "TC-1", "reason": "impossible"}], "revision": 0}
    folded = MP.fold(journal(patch, seed=seed))
    check_eq("K4b: fold([seed, patch with two reasons]) -> the later wins", row_of(folded, "TC-5").get("reason"), BLOCKED)
    check_eq("K4b: no unprojected_events", "unprojected_events" in folded, False)
    check_eq("K4b: and the merge itself raises nothing", refusal(MP.merge, copy.deepcopy(seed), patch), "")
    reversed_patch = {"unresolved": list(reversed(patch["unresolved"]))}
    check_eq("K4b: the order decides, as before (the requirement row last -> it wins)",
             row_of(MP.fold(journal(reversed_patch, seed=seed)), "TC-5").get("reason"), CONTRADICTS)


# --- K8: the slice of a re-sent row ------------------------------------------------------------------------------------

def resend(old: dict, patch: dict) -> dict:
    """The `contradicts_requirement` row of TC-004 after `patch` is sent over `old` (both through the merge)."""
    standing = {"unresolved": [dict({"case": "TC-004", "reason": CONTRADICTS, "detail": "d"}, **old)]}
    merged, _ = MP.merge(standing, {"unresolved": [dict({"case": "TC-004"}, **patch)]})
    return row_of(merged, "TC-004")


def k8_slice_replacement() -> None:
    row = resend({"partitions": ["P-msteams"]}, {"instance_ids": ["x"]})
    check_eq("K8: a patch with instances replaces the partitions", (row.get("instance_ids"), "partitions" in row), (["x"], False))
    row = resend({"instance_ids": [MS]}, {"thens": [2]})
    check_eq("K8: a `thens`-only patch keeps `instance_ids` (the two groups are independent)",
             (row.get("instance_ids"), row.get("thens")), ([MS], [2]))
    row = resend({"instance_ids": [MS], "thens": [2]}, {"instance_ids": ["MS2"]})
    check_eq("K8: new instances keep the Thens", (row.get("instance_ids"), row.get("thens")), (["MS2"], [2]))
    row = resend({"instance_ids": [MS], "thens": [2]}, {"detail": "new words"})
    check_eq("K8: a `detail`-only patch leaves the slice and the Thens", (row.get("instance_ids"), row.get("thens"), row["detail"]),
             ([MS], [2], "new words"))
    check_eq("K8: and changes no byte of the row's key order", list(row), ["case", "reason", "detail", "instance_ids", "thens"])
    row = resend({"instance_ids": [MS], "thens": [2]}, {"thens": []})
    check_eq("K8: `thens: []` leaves the old Thens (an empty group is not carried)", row.get("thens"), [2])
    row = resend({"instance_ids": [MS], "thens": [2]}, {"instance_ids": [], "partitions": ""})
    check_eq("K8: an empty slice group leaves the old slice", (row.get("instance_ids"), "partitions" in row), ([MS], False))
    row = resend({"instance_ids": [MS]}, {"thens": []})
    check_eq("K8: an empty `thens` on a row that had none does not plant the key", "thens" in row, False)
    row = resend({"instance_ids": [MS], "thens": [2]}, {"thens": [1, 2]})
    check_eq("K8: new Thens replace the old (not united), the instances stay", (row.get("thens"), row.get("instance_ids")), ([1, 2], [MS]))
    row = resend({"instance_id": "old[a]"}, {"instance_ids": ["new[b]"]})
    check_eq("K8: the singular and the plural spelling are ONE group", (row.get("instance_ids"), "instance_id" in row), (["new[b]"], False))
    row = resend({"partitions": ["P-a"]}, {"instance_ids": ["x"], "partitions": ["P-b"]})
    check_eq("K8: a patch naming both keys of the group sends both", (row.get("instance_ids"), row.get("partitions")), (["x"], ["P-b"]))

    # other reasons are not this function's: today's merge (update) stays for them
    other = {"unresolved": [{"case": "TC-004", "reason": "handed_to_person", "partitions": ["P-a"]}]}
    merged, _ = MP.merge(other, {"unresolved": [{"case": "TC-004", "instance_ids": ["x"]}]})
    check_eq("K8: a row of another reason keeps the plain update (partitions beside instance_ids)",
             (row_of(merged, "TC-004").get("partitions"), row_of(merged, "TC-004").get("instance_ids")), (["P-a"], ["x"]))
    stand = {"unresolved": [{"case": "TC-004", "reason": BLOCKED, "instance_ids": ["a"]}]}
    merged, _ = MP.merge(stand, {"unresolved": [{"case": "TC-004", "instance_ids": ["b"]}]})
    check_eq("K8: and a `blocked_by_env` row keeps its own rule (`_replace_blocked_naming`)", row_of(merged, "TC-004").get("instance_ids"), ["b"])
    # the function itself, on its edge inputs
    check_eq("K8: a patch that changes the reason to contradicts_requirement is judged by the MERGED reason",
             MP._replace_contradicts_slice({"instance_ids": ["x"]}, {"reason": CONTRADICTS, "partitions": ["P-a"], "instance_ids": ["x"]},
                                           {"reason": BLOCKED, "partitions": ["P-a"]}), {"reason": CONTRADICTS, "instance_ids": ["x"]})
    handed = {"reason": CONTRADICTS, "partitions": ["P-a"], "instance_ids": ["x"]}
    snapshot = copy.deepcopy(handed)
    MP._replace_contradicts_slice({"instance_ids": ["x"]}, handed, {})
    check_eq("K8: the row handed in is not edited in place (the manifest shares its rows with the caller's)", handed, snapshot)


def k8b_one_constant() -> None:
    inputs = [{key: "x"} for key in C.UNRESOLVED_SLICE_KEYS] + [{key: [1]} for key in C.UNRESOLVED_SLICE_KEYS] + [
        {"thens": [2]}, {}, {"instance_ids": []}, {"partitions": ""}, None, "TC-1", []]
    check_eq("K8b: `_partition_scoped` and `contract._slice_scoped` agree on every input of the contract's key test",
             [MP._partition_scoped(e) for e in inputs], [C._slice_scoped(e) for e in inputs])
    check_eq("K8b: every slice key makes a row slice-scoped (the loop is over the constant)",
             [MP._partition_scoped({key: "x"}) for key in C.UNRESOLVED_SLICE_KEYS], [True] * len(C.UNRESOLVED_SLICE_KEYS))
    check_eq("K8b: `thens` is not a slice key", (MP._partition_scoped({"thens": [2]}), C.UNRESOLVED_THENS_KEY in C.UNRESOLVED_SLICE_KEYS), (False, False))
    scoped, replaced = inspect.getsource(MP._partition_scoped), inspect.getsource(MP._replace_contradicts_slice)
    # the census (AR-13): the readers carry no key list of their own; the control is a function that does (the stand's naming)
    own = inspect.getsource(MP._with_naming)
    check("K8b: control - the same literal-key search finds a private list where there is one", '"instance_ids"' in own, own[:80])
    for name, source in (("_partition_scoped", scoped), ("_replace_contradicts_slice", replaced)):
        check(f"K8b: {name} names no slice key of its own", not any(f'"{key}"' in source for key in C.UNRESOLVED_SLICE_KEYS + (C.UNRESOLVED_THENS_KEY,)), source[:60])
        check(f"K8b: {name} reads the contract's constants", "C.UNRESOLVED_" in source, source[:60])


# --- through `run` (the journal, the print, the replay) ---------------------------------------------------------------

def run_end_to_end() -> None:
    with Stand() as stand:
        seeded = {"tests": [{"instance_id": MS, "file": "tests/test_move.py", "covers": ["TC-004", "TC-005"], "status": "red",
                             "partitions": ["P-msteams"]}],
                  "unresolved": [dict(RED_ROW), {"case": "TC-005", "reason": CONTRADICTS, "partitions": ["P-msteams"], "detail": "stale"}]}
        check_eq("run: the rows are sent", stand.put(seeded)[0], 0)
        both = stand.put({"unresolved": [{"case": "TC-005", "instance_ids": [MS], "thens": [1]}]})
        check_eq("run: a re-sent row replaces its slice in the projection", both[0], 0)
        check_eq("run: ... partitions gone, instances and Thens as sent", (row_of(stand.manifest(), "TC-005").get("instance_ids"),
                                                                          "partitions" in row_of(stand.manifest(), "TC-005")), ([MS], False))

        before = (stand.journal(), stand.tree())
        code, _out, err = stand.put({"retracted_unresolved": ["TC-099"]})
        check_eq("run K3: a key naming no row is refused before the commit", (code, (stand.journal(), stand.tree())), (MP.EXIT_BAD_FRAGMENT, before))
        check_in("run K3: nothing was committed, and the door is the view", "manifest_view.py --task <T>", err)
        code, _out, err = stand.put({"retracted_unresolved": ["TC-005"], "unresolved": [{"case": "TC-005", "reason": BLOCKED}]})
        check_eq("run K2: send-and-retract is refused before the commit", (code, (stand.journal(), stand.tree())), (MP.EXIT_BAD_FRAGMENT, before))

        code, out, err = stand.put({"retracted_unresolved": ["TC-005"]})
        check_eq("run K1: the retraction commits", code, 0)
        check_in("run K1: and says what it dropped, slice and Thens", f'unresolved row of TC-005 retracted: reason {CONTRADICTS}, '
                 f'instance_ids ["{MS}"], thens [1]', out)
        manifest = stand.manifest()
        check_eq("run K1: the projection holds TC-004's row only, and the history", (cases(manifest), manifest.get("retracted_unresolved")),
                 (["TC-004"], ["TC-005"]))
        code, _out, err = stand.put({"retracted_unresolved": ["TC-005"], "run_witness": "w2.json"})
        check_eq("run K3: the same key again is refused as already gone", (code, "is already gone" in err), (MP.EXIT_BAD_FRAGMENT, True))
        count = stand.journal()
        code, out, _err = stand.recover()
        check_eq("run K2b: the replay of the journal is the projection already standing", (code, "already current" in out, stand.journal()),
                 (0, True, count))
        check_eq("run K2b: ... and the manifest is the same", stand.manifest(), manifest)


# --- 5a-K1: `then_bindings` by unit (HF2-5) -----------------------------------------------------------------------------

def bound(case: str, then: int, iid, ref="tests/t.py:1-5") -> dict:
    return {"case": case, "then": then, "instance_id": iid, "assertion_ref": ref, "status": "covered"}


def handed(case: str, then: int, detail: str = "the steps") -> dict:
    return {"case": case, "then": then, "instance_id": None, "assertion_ref": None, "status": "unresolved",
            "reason": "handed_to_person", "detail": detail}


def writer_test(iid: str, case: str) -> dict:
    return {"instance_id": iid, "file": "tests/t.py", "covers": [case], "status": "green", "generated_from": ["tests/t.py"]}


def k5a_k1_a_writer_replaces() -> None:
    current = {"tests": [writer_test("t7", "TC-007"), writer_test("t1", "TC-001")],
               "then_bindings": [bound("TC-007", 1, "t7"), bound("TC-001", 1, "t1")]}
    # RN1-22: the writer's array replaces the rows of what it WROTE ABOUT (the instances of its `tests[]`, the cases of its own
    # rows), so the moved test (t7) is in its `tests[]`; before, any writer fragment replaced the whole array.
    sent = [bound("TC-001", 1, "t1"), bound("TC-008", 1, "t7")]
    merged, _ = MP.merge(copy.deepcopy(current), {"tests": [writer_test("t7", "TC-008")], "then_bindings": sent})
    check_eq("5a-K1 (a): the writer's array replaces the old one: the test moved TC-007 -> TC-008, the covered TC-007 row is gone",
             merged["then_bindings"], sent)
    check_eq("5a-K1 (a): ... and the run prints the row it took out",
             MP.removed_then_lines(current, {"tests": [writer_test("t7", "TC-008")], "then_bindings": sent}),
             ["TC-007 Then 1 on t7"])
    hand_merged, _ = MP.merge(copy.deepcopy(current), {"then_bindings": sent})
    check_eq("5a-K1 (a) CONTROL: the same rows from a hand fragment (no `generated_from`) leave the unit they do not name",
             [(r["case"], r["then"]) for r in hand_merged["then_bindings"]], [("TC-007", 1), ("TC-001", 1), ("TC-008", 1)])
    only_unresolved = {"unresolved": [{"case": "TC-009", "reason": "impossible", "detail": "d"}], "then_bindings": sent}
    merged, _ = MP.merge(copy.deepcopy(current), only_unresolved)
    check_eq("5a-K1 (a): a fragment with no `tests[]` (only `qa_unresolved` rows) is a hand fragment: TC-007 stays",
             [(r["case"], r["then"]) for r in merged["then_bindings"]], [("TC-007", 1), ("TC-001", 1), ("TC-008", 1)])


def k5a_k1_b_c_d_hand_units() -> None:
    story = shape_a()["manifest"]
    rows = story["then_bindings"]
    blocked_ms = [dict(r, detail="check once TC-004 is fixed (sent again)") for r in rows
                  if r["case"] == "TC-005" and r["instance_id"] == MS]
    check_eq("5a-K1 (b) fixture: TC-005 has two blocked rows on MS and two covered rows on G5",
             (len(blocked_ms), len([r for r in rows if r["case"] == "TC-005" and r["instance_id"] == G5])), (2, 2))
    merged, _ = MP.merge(copy.deepcopy(story), {"then_bindings": blocked_ms})
    check_eq("5a-K1 (b): a hand fragment of the blocked rows of TC-005 on MS leaves the covered TC-005 rows on G5 as they were",
             [r for r in merged["then_bindings"] if r["case"] == "TC-005" and r["instance_id"] == G5],
             [r for r in rows if r["case"] == "TC-005" and r["instance_id"] == G5])
    check_eq("5a-K1 (b): ... the blocked rows are the ones sent, each where it stood, and nothing else moved",
             (len(merged["then_bindings"]), [r for r in merged["then_bindings"] if r["instance_id"] == MS and r["case"] == "TC-005"]),
             (len(rows), blocked_ms))
    check_eq("5a-K1 (b): ... every row of the other units is the row it was",
             [r for r in merged["then_bindings"] if r not in blocked_ms], [r for r in rows if r["case"] != "TC-005" or r["instance_id"] != MS])
    check_eq("5a-K1 (b): ... and nothing is printed as taken out",
             MP.removed_then_lines(story, {"then_bindings": blocked_ms}), [])

    own = [dict(r, assertion_ref="tests/test_generic.py:1-2") for r in rows if r["case"] == "TC-005" and r["instance_id"] == G5]
    merged, _ = MP.merge(copy.deepcopy(story), {"then_bindings": own})
    check_eq("5a-K1 (c): a hand fragment for TC-005 leaves the TC-004 and TC-006 rows as they were",
             [r for r in merged["then_bindings"] if r["case"] in ("TC-004", "TC-006")],
             [r for r in rows if r["case"] in ("TC-004", "TC-006")])
    check_eq("5a-K1 (c): ... and the TC-005 rows of the unit are the ones sent", [r for r in merged["then_bindings"] if r in own], own)
    check_eq("5a-K1 (c): ... TC-005's other unit (MS) is untouched too",
             [r for r in merged["then_bindings"] if r["case"] == "TC-005" and r["instance_id"] == MS],
             [r for r in rows if r["case"] == "TC-005" and r["instance_id"] == MS])

    merged, _ = MP.merge(copy.deepcopy(story), {"run_witness": "w.json"})
    check_eq("5a-K1 (d): a fragment without `then_bindings` leaves the array as it was", merged["then_bindings"], rows)
    merged, _ = MP.merge(copy.deepcopy(story), {"then_bindings": []})
    check_eq("5a-K1 (d): ... and `then_bindings: []` names no unit, so it takes nothing out", merged["then_bindings"], rows)
    sent = dict(own[1], then="2", assertion_ref="x")
    merged, _ = MP.merge(copy.deepcopy(story), {"then_bindings": [sent]})
    g5_rows = [r for r in rows if r["case"] == "TC-005" and r["instance_id"] == G5]
    check_eq("5a-K1 (d): ... a `then` written as \"2\" is the Then 2 of the row it replaces (one row, not two); Then 1 of the unit "
             "was not sent and STAYS (RN1-22: only `retract` takes it out)",
             [r for r in merged["then_bindings"] if r["case"] == "TC-005" and r["instance_id"] == G5], [g5_rows[0], sent])
    merged, _ = MP.merge(copy.deepcopy(story), {"then_bindings": [sent], "retract": ["then_bindings"]})
    check_eq("5a-K1 (d): ... and with `retract: [then_bindings]` Then 1 of the unit is out, as before RN1-22",
             [r for r in merged["then_bindings"] if r["case"] == "TC-005" and r["instance_id"] == G5], [sent])
    merged, _ = MP.merge(copy.deepcopy(story), {"then_bindings": "not an array"})
    check_eq("5a-K1: a value that is no array is carried as before, never raised (an old journal replays)",
             merged["then_bindings"], "not an array")


def k5a_k1_e_two_handed_thens() -> None:
    current = {"tests": [writer_test("t1", "TC-001")],
               "then_bindings": [bound("TC-001", 1, "t1"), handed("TC-001", 3), handed("TC-001", 4), bound("TC-002", 1, "t1")]}
    # RN1-22 (FK-1 a): a Then of a named unit the fragment did not send is taken out only by `retract: [then_bindings]`
    retracting = {"then_bindings": [handed("TC-001", 4, "new steps")], "retract": ["then_bindings"]}
    merged, _ = MP.merge(copy.deepcopy(current), retracting)
    check_eq("5a-K1 (e): two handed Thens of TC-001 (null instance), the hand fragment sends Then 4 with `retract`: Then 3 is taken out",
             [(r["case"], r["then"], r.get("detail")) for r in merged["then_bindings"]],
             [("TC-001", 1, None), ("TC-001", 4, "new steps"), ("TC-002", 1, None)])
    check_eq("5a-K1 (e): ... and the summary names it", MP.removed_then_lines(current, retracting), ["TC-001 Then 3 on none"])
    both = [handed("TC-001", 3), handed("TC-001", 4, "new steps")]
    merged, _ = MP.merge(copy.deepcopy(current), {"then_bindings": both})
    check_eq("5a-K1 (e) CONTROL: the fragment sends both: both stand", [(r["then"], r.get("detail")) for r in merged["then_bindings"]
                                                                    if r["case"] == "TC-001" and r["instance_id"] is None],
             [(3, "the steps"), (4, "new steps")])
    check_eq("5a-K1 (e) CONTROL: ... and nothing is printed", MP.removed_then_lines(current, {"then_bindings": both}), [])
    check_eq("5a-K1 (e): a null instance is a unit of its own: the covered TC-001 row on t1 is not the handed unit",
             [r for r in merged["then_bindings"] if r["instance_id"] == "t1" and r["case"] == "TC-001"], [bound("TC-001", 1, "t1")])


def k5a_k1_replay() -> None:
    seed = {"tests": [writer_test("t1", "TC-001")], "then_bindings": [bound("TC-001", 1, "t1"), handed("TC-001", 3), handed("TC-001", 4)]}
    old_hand_fragment = {"then_bindings": [handed("TC-001", 4, "new steps")]}
    folded = MP.fold(journal(old_hand_fragment, seed=seed))
    check_eq("5a-K1 replay: an old journal with a hand `then_bindings` fragment folds by the new rule (RN1-22, E12: Then 3 is kept, "
             "no `retract` was sent; the covered row stays)",
             [(r["then"], r["instance_id"]) for r in folded["then_bindings"]], [(1, "t1"), (3, None), (4, None)])
    check_not_in("5a-K1 replay: ... and nothing is reported as unprojected", "unprojected_events", " ".join(folded))
    check_eq("5a-K1 replay: ... the fold is deterministic (folding the journal twice is the same manifest)",
             MP.fold(journal(old_hand_fragment, seed=seed)), folded)


def k5a_k1_run_prints() -> None:
    with Stand() as stand:
        check_eq("5a-K1 run: the handed Thens are sent", stand.put({"then_bindings": [handed("TC-001", 3), handed("TC-001", 4)]})[0], 0)
        code, out, _err = stand.put({"then_bindings": [handed("TC-001", 3), handed("TC-001", 4, "again")]})
        check_eq("5a-K1 (e) run CONTROL: both sent: it commits and says nothing of rows taken out",
                 (code, "taken out" in out), (0, False))
        code, out, _err = stand.put({"then_bindings": [handed("TC-001", 4, "only this one")], "retract": ["then_bindings"]})
        check_eq("5a-K1 (e) run: only Then 4 sent, with `retract`: it commits", code, 0)
        check_in("5a-K1 (e) run: ... and prints the row it took out in the words `<case> Then <n> on <instance|none>`",
                 "TC-001 Then 3 on none", out)
        check_eq("5a-K1 (e) run: ... the projection holds Then 4 only",
                 [(r["then"], r["detail"]) for r in stand.manifest()["then_bindings"]], [(4, "only this one")])
        count = stand.journal()
        code, out, _err = stand.put({"then_bindings": [handed("TC-001", 4, "only this one")], "retract": ["then_bindings"]})
        check_eq("5a-K1 (e) run: the same fragment sent again takes nothing out (the replay prints nothing)",
                 (code, "taken out" in out, stand.journal()), (0, False, count))


# --- HF3-2: a retracted instance takes its Then rows with it (B-K1, B-K4, B-K5, B-K7) ------------------------------------

OLD_I, NEW_I, OTHER_I = "t_old[a]", "t_new[a]", "t_other[a]"


def test_row(iid: str, covered: str = "TC-020", **extra) -> dict:
    return dict({"instance_id": iid, "file": "tests/a.py", "covers": [covered], "status": "green"}, **extra)


def retire_story() -> dict:
    """TC-020 is proved by two tests; the Thens of OLD_I (two) and of OTHER_I (one) are bound."""
    return {"tests": [test_row(OLD_I), test_row(OTHER_I)],
            "then_bindings": [bound("TC-020", 1, OLD_I), bound("TC-020", 2, OLD_I), bound("TC-020", 1, OTHER_I)]}


def hf3_2_b_k1_retraction_takes_the_rows() -> None:
    story = retire_story()
    rename = {"retracted_instances": [OLD_I], "tests": [test_row(NEW_I)]}
    merged, summary = MP.merge(copy.deepcopy(story), rename)
    check_eq("B-K1: a rename (old retracted, new sent) takes the two Thens bound to the retired spelling and leaves the rest",
             [(r["then"], r["instance_id"]) for r in merged["then_bindings"]], [(1, OTHER_I)])
    check_eq("B-K1: ... the summary counts them, and the retraction is recorded as before",
             (summary.get("then_rows_retired"), summary.get("retracted_instances"), merged.get("retracted_instances")),
             (2, 1, [OLD_I]))
    check_eq("B-K1: ... `run` prints exactly those rows, in the words of the other block",
             MP.removed_then_lines(story, rename), [f"TC-020 Then 1 on {OLD_I}", f"TC-020 Then 2 on {OLD_I}"])
    _, summary = MP.merge(copy.deepcopy(story), {"tests": [test_row(NEW_I)]})
    check_eq("B-K1 CONTROL: the same new row WITHOUT the retraction takes nothing (and the summary has no such key)",
             ("then_rows_retired" in summary, MP.removed_then_lines(story, {"tests": [test_row(NEW_I)]})), (False, []))

    # the door of a ghost (A19): retracting the id AGAIN takes the Thens that still stand on it (m10 - "asked", not "first written")
    ghosted = copy.deepcopy(story)
    ghosted["retracted_instances"] = [OLD_I]
    ghosted["tests"] = [t for t in ghosted["tests"] if t["instance_id"] != OLD_I] + [{"instance_id": OLD_I, "status": "red"}]
    merged, summary = MP.merge(copy.deepcopy(ghosted), {"retracted_instances": [OLD_I]})
    check_eq("B-K1 door: retracting a ghost's id again drops the ghost AND the Thens still bound to it",
             ([t["instance_id"] for t in merged["tests"]], [(r["then"], r["instance_id"]) for r in merged["then_bindings"]],
              merged["retracted_instances"]), ([OTHER_I], [(1, OTHER_I)], [OLD_I]))

    with Stand() as stand:
        check_eq("B-K1 run: the story is sent", stand.put(story)[0], 0)
        code, out, _err = stand.put(rename)
        check_eq("B-K1 run: the rename commits", code, 0)
        check_in("B-K1 run: ... prints the block and the first row", "then_bindings rows taken out by this send", out)
        check_in("B-K1 run: ... and the rows by their words", f"TC-020 Then 2 on {OLD_I}", out)
        check_eq("B-K1 run: ... the projection holds the one row that stood on the other test",
                 [(r["then"], r["instance_id"]) for r in stand.manifest()["then_bindings"]], [(1, OTHER_I)])
        count = stand.journal()
        code, out, _err = stand.put(rename)
        check_eq("B-K1 run: the same fragment sent again is the store's reuse path (nothing new, nothing re-printed as taken)",
                 (code, stand.journal()), (0, count))


def hf3_2_b_k4_a_spelling_a_row_still_wears() -> None:
    prefixed, bare = "TC-012::test_x[eu]", "test_x[eu]"
    old = {"tests": [test_row(bare, "TC-012", case="TC-012")], "then_bindings": [bound("TC-012", 1, prefixed), bound("TC-012", 2, bare)]}
    # `_current_spelling`: a 0.7.7 fragment sends the prefixed spelling of the row that stands bare; the prefixed one is
    # retired - and the surviving row still answers to it (`_identity`), so its Thens stay
    patch = {"tests": [test_row(prefixed, "TC-012", case="TC-012")]}
    merged, summary = MP.merge(copy.deepcopy(old), patch)
    check_eq("B-K4: the 0.7.7 spelling retired by `_current_spelling` (the rename of one live row) keeps its Thens",
             ([r["instance_id"] for r in merged["then_bindings"]], merged.get("retracted_instances"), "then_rows_retired" in summary),
             ([prefixed, bare], [prefixed], False))
    check_eq("B-K4: ... and `run` prints nothing taken", MP.removed_then_lines(old, patch), [])
    # `_retract_aliases`: two rows that are two spellings of one test collapse; the survivor wears both
    twin = {"tests": [test_row(prefixed, "TC-012", case="TC-012"), test_row(bare, "TC-012", case="TC-012")],
            "then_bindings": old["then_bindings"]}
    merged, summary = MP.merge(copy.deepcopy(twin), {"runs": [{"label": "w"}]})
    check_eq("B-K4: the collapse of two spellings of one test (`_retract_aliases`) keeps the Thens of both",
             ([t["instance_id"] for t in merged["tests"]], [r["instance_id"] for r in merged["then_bindings"]],
              "then_rows_retired" in summary), ([bare], [prefixed, bare], False))
    # CONTROL: an explicit retraction of that very alias with the row dropped by it is a retirement (nobody wears it after).
    # FLIPPED by the Lead's decision on HF3-2 Q2 (critic t-1276): the Then rows bound to ANY alias of the dropped row go with
    # it - the bare spelling too, not only the one that was named (was: `[bare], 1`)
    merged, summary = MP.merge(copy.deepcopy(old), {"retracted_instances": [prefixed]})
    check_eq("B-K4 CONTROL (Q2): retracting the prefixed id with no row left to wear it takes the Thens bound to it AND to its bare alias",
             ([t["instance_id"] for t in merged["tests"]], [r["instance_id"] for r in merged["then_bindings"]],
              summary.get("then_rows_retired")), ([], [], 2))


def hf3_2_b_k8_aliases_of_a_dropped_row() -> None:
    """Q2 (critic t-1276, the Lead's decision): a Then row bound to ANY spelling a dropped row answered to is retired with it
    (`contract.instance_id_aliases`: the canonical id, the 0.7.7 case-prefixed id, the bare id, the selector hash)."""
    prefixed, bare = "TC-012::test_x[eu]", "test_x[eu]"
    other = "test_y[eu]"
    row = test_row(prefixed, "TC-012", case="TC-012")
    thens = [bound("TC-012", 1, prefixed), bound("TC-012", 2, bare), bound("TC-012", 3, other)]
    story = {"tests": [row, test_row(other, "TC-012", case="TC-012")], "then_bindings": thens}
    aliases = MP._spellings(row)
    check_eq("B-K8: the alias set of the row holds the prefixed and the bare spelling", {prefixed, bare} <= aliases, True)
    for asked in (prefixed, bare):
        merged, summary = MP.merge(copy.deepcopy(story), {"retracted_instances": [asked]})
        check_eq(f"B-K8: retracting `{asked}` takes the Thens of EVERY alias of the dropped row and leaves the other test's",
                 ([t["instance_id"] for t in merged["tests"]], [(r["then"], r["instance_id"]) for r in merged["then_bindings"]],
                  summary.get("then_rows_retired")), ([other], [(3, other)], 2))
        check_eq(f"B-K8: ... and `run` prints the rows of both spellings (`{asked}`)",
                 MP.removed_then_lines(story, {"retracted_instances": [asked]}),
                 [f"TC-012 Then 1 on {prefixed}", f"TC-012 Then 2 on {bare}"])
    check_eq("B-K8 CONTROL: a row that survives keeps every Then of its aliases (nothing dropped, nothing retired)",
             MP._dropped_spellings(story, []), set())
    check_eq("B-K8: `_dropped_spellings` adds the aliases of the row that answers to a named spelling, and nothing for an unknown one",
             (MP._dropped_spellings(story, [prefixed]) >= {prefixed, bare}, MP._dropped_spellings(story, ["nobody"]),
              MP._dropped_spellings(None, [prefixed])), (True, {"nobody"}, {prefixed}))
    check_eq("B-K8: spelled in a rename (the new row wears the aliases): the rows of the spelling the new row answers to stay",
             MP._retire_then_rows({"tests": [row], "then_bindings": thens}, MP._dropped_spellings(story, [prefixed]), {}), [])


def hf3_2_b_k5_send_and_retract() -> None:
    story = retire_story()
    sent = {"retracted_instances": [OLD_I], "tests": [test_row(NEW_I)], "then_bindings": [bound("TC-020", 3, OLD_I)]}
    merged, summary = MP.merge(copy.deepcopy(story), sent)
    check_eq("B-K5 replay: `merge` never raises on a fragment that binds a Then to the id it retracts, and the sent row STAYS "
             "(the retirement runs before the merge of the fragment's own rows); the older rows of the id went",
             ([(r["then"], r["instance_id"]) for r in merged["then_bindings"]], summary.get("then_rows_retired")),
             ([(1, OTHER_I), (3, OLD_I)], 2))
    check_eq("B-K5 replay: ... and the old journal folds without a gap",
             "unprojected_events" in MP.fold(journal(sent, seed=story)), False)
    with Stand() as stand:
        stand.put(story)
        before = (stand.journal(), stand.tree())
        code, _out, err = stand.put(sent)
        check_eq("B-K5 run: the same fragment is refused BEFORE the commit and nothing changes",
                 (code, (stand.journal(), stand.tree())), (MP.EXIT_BAD_FRAGMENT, before))
        check_in("B-K5 run: ... with the rule's words", "one fragment cannot both bind a Then to and retract an instance", err)
        check_in("B-K5 run: ... the id", OLD_I, err)
        check_in("B-K5 run: ... and the door", "retract the old spelling, not the same id twice", err)
        control = dict(sent, then_bindings=[bound("TC-020", 3, NEW_I)])
        code, _out, err = stand.put(control)
        check_eq("B-K5 run CONTROL: the Then row on the NEW id commits", (code, err), (0, ""))


def hf3_2_b_k7_empties() -> None:
    story = retire_story()
    for label, fragment in (("an empty retraction", {"retracted_instances": [], "runs": [{"label": "w"}]}),
                            ("a null retraction", {"retracted_instances": None, "runs": [{"label": "w"}]}),
                            ("no then_bindings in the manifest", {"retracted_instances": [OLD_I]})):
        base = copy.deepcopy(story)
        if label.startswith("no then"):
            base.pop("then_bindings")
        try:
            merged, summary = MP.merge(base, fragment)
            raised = ""
        except Exception as exc:
            merged, summary, raised = {}, {}, f"{type(exc).__name__}: {exc}"
        check_eq(f"B-K7: {label} does not raise", raised, "")
        if label.startswith("no then"):
            check_eq("B-K7: ... and invents no array", ("then_bindings" in merged, "then_rows_retired" in summary), (False, False))
        else:
            check_eq(f"B-K7: ... {label} takes nothing", (merged["then_bindings"], "then_rows_retired" in summary),
                     (story["then_bindings"], False))
    base = copy.deepcopy(story)
    base["then_bindings"] = "not an array"
    merged, summary = MP.merge(base, {"retracted_instances": [OLD_I]})
    check_eq("B-K7: a `then_bindings` that is no array (an old journal) is carried as it was, never raised",
             (merged["then_bindings"], "then_rows_retired" in summary), ("not an array", False))
    check_eq("B-K7: `_retire_then_rows` with nothing to retire or nothing to read returns [] and touches nothing",
             [MP._retire_then_rows({"then_bindings": [bound("TC-020", 1, OLD_I)], "tests": []}, [], {}),
              MP._retire_then_rows({"then_bindings": [bound("TC-020", 1, OLD_I)], "tests": []}, [None, "", "  "], {}),
              MP._retire_then_rows({"then_bindings": None}, [OLD_I], {}), MP._retire_then_rows({}, [OLD_I], {})], [[]] * 4)
    garbage = {"then_bindings": [None, "x", 3, bound("TC-020", 1, OLD_I)], "tests": []}
    check_eq("B-K7: rows that are no objects are kept, the object row of the retired spelling goes",
             (MP._retire_then_rows(garbage, [OLD_I], {}), garbage["then_bindings"]), ([bound("TC-020", 1, OLD_I)], [None, "x", 3]))


# --- TQ1-7: introduced_helpers[] by (file, name) -------------------------------------------------------------------------

def helper(file: str, name: str, novelty=None, **role) -> dict:
    row = {"file": file, "name": name, **role}
    if novelty:
        row["novelty"] = novelty
    return row


def tq1_7_helpers() -> None:
    """D1-K4/K6, D1-3: two writers, one row. The writer's row (it carries `novelty`) replaces; the files it read lose the
    rows of functions it did not send; a role row changes the role fields of a row that stands and creates none; a field
    that is none of the seven is refused with the fields named, before the commit. Killing test of M-D1-4 (merge not by pair)."""
    a, b = "tests/a.py", "tests/b.py"
    writer = {"introduced_helpers": [helper(a, "PO.read", "new", purpose="", searched="", similar_found="", keep=""),
                                     helper(a, "make", "changed", purpose="", searched="", similar_found="", keep=""),
                                     helper(b, "other", "new", purpose="", searched="", similar_found="", keep="")]}
    merged, summary = MP.merge({}, writer)
    check_eq("K4: the writer's rows are added, keyed by the pair", sorted((r["file"], r["name"]) for r in merged["introduced_helpers"]),
             [(a, "PO.read"), (a, "make"), (b, "other")])
    check_eq("K4: three added", summary["added"], 3)
    role = {"introduced_helpers": [{"file": a, "name": "make", "purpose": "builds", "searched": "tests/", "similar_found": "none"}]}
    merged2, _ = MP.merge(merged, role)
    row = next(r for r in merged2["introduced_helpers"] if r["name"] == "make")
    check_eq("K4: a role row sets the role fields and keeps the scaffold", (row["purpose"], row["searched"], row["novelty"], row["keep"]),
             ("builds", "tests/", "changed", ""))
    check_eq("K4: the other rows stand as they were", [r for r in merged2["introduced_helpers"] if r["name"] != "make"],
             [r for r in merged["introduced_helpers"] if r["name"] != "make"])
    # the writer again: the role's words survive an EMPTY role field of the writer, the function that is gone loses its row,
    # the row of the other file stays
    rewrite = {"introduced_helpers": [helper(a, "make", "changed", purpose="", searched="", similar_found="", keep="")],
               "tests": [{"instance_id": "t_one", "file": a, "generated_from": [a], "case": "TC-1", "covers": ["TC-1"]}]}
    merged3, _ = MP.merge(merged2, rewrite)
    check_eq("D1-3: a writer run over a.py drops the vanished PO.read, keeps b.py's row",
             sorted((r["file"], r["name"]) for r in merged3["introduced_helpers"]), [(a, "make"), (b, "other")])
    check_eq("K3: an empty role field of the writer does not wipe what the role wrote",
             next(r for r in merged3["introduced_helpers"] if r["name"] == "make")["purpose"], "builds")
    merged4, _ = MP.merge(merged2, {"introduced_helpers": [], "tests": rewrite["tests"]})
    check_eq("K4: an empty list with a writer-marked test row of the file takes every row of that file",
             sorted((r["file"], r["name"]) for r in merged4["introduced_helpers"]), [(b, "other")])
    merged5, _ = MP.merge(merged2, {"introduced_helpers": [], "tests": [{"instance_id": "t_one", "file": a}]})
    check_eq("D1-3: a test row without the writer's mark takes nothing", len(merged5["introduced_helpers"]), 3)
    check_eq("D1-2: an old manifest without the key stays without it under a fragment without it",
             "introduced_helpers" in MP.merge({"tests": []}, {"run_witness": "w"})[0], False)
    check_eq("K6 (merge): a role row for a pair nobody wrote creates nothing at replay",
             MP.merge({}, {"introduced_helpers": [{"file": a, "name": "ghost", "purpose": "x"}]})[0].get("introduced_helpers"), [])

    problems = MP.helper_row_problems(merged, {"introduced_helpers": [{"file": a, "name": "make", "colour": "red", "scope": 1}]})
    check("K6: a field that is none of the seven is refused and the fields are named",
          len(problems) == 1 and "colour, scope" in problems[0] and "purpose" in problems[0] and "novelty" in problems[0], str(problems))
    check_eq("K6: a role row for a pair the manifest holds no row for is refused with the door",
             ["manifest_from_tests.py" in p for p in MP.helper_row_problems(merged, {"introduced_helpers": [
                 {"file": a, "name": "ghost", "purpose": "x"}]})], [True])
    check_eq("K6: ... but not when the same fragment brings the writer's row of it",
             MP.helper_row_problems({}, {"introduced_helpers": [helper(a, "n", "new"), {"file": a, "name": "n", "purpose": "p"}]}), [])
    check("K6: a role field that is not text, and a `novelty` that is not one of the three, are named",
          len(MP.helper_row_problems(merged, {"introduced_helpers": [{"file": a, "name": "make", "purpose": 3},
                                                                       helper(a, "make", "maybe")]})) == 2)
    check_eq("K6: the key is a list", len(MP.helper_row_problems({}, {"introduced_helpers": "x"})), 1)
    check_eq("D1-2: a fragment without the key has no problem to name", MP.helper_row_problems({}, {"tests": []}), [])
    check("BY_HELPER is also in SCALAR_EXEMPT: the trailing scalar loop never copies the key whole",
          MP.BY_HELPER[0] in MP.SCALAR_EXEMPT, str(MP.SCALAR_EXEMPT))

    with Stand() as stand:
        check_eq("run: the writer's rows are committed", stand.put(writer)[0], 0)
        before = (stand.journal(), stand.tree())
        code, _out, err = stand.put({"introduced_helpers": [{"file": a, "name": "make", "colour": "red"}]})
        check_eq("K6 run: a row with a foreign field is refused before the commit, the journal unchanged",
                 (code, (stand.journal(), stand.tree())), (MP.EXIT_BAD_FRAGMENT, before))
        check_in("K6 run: the refusal names the field and the fields it takes", "colour", err)
        check_in("K6 run: ... and the repair marker", "repair", err.lower())
        code, _out, err = stand.put({"introduced_helpers": [{"file": a, "name": "ghost", "purpose": "x"}]})
        check_eq("K6 run: a role row for a helper nobody wrote is refused", (code, "manifest_from_tests.py" in err), (MP.EXIT_BAD_FRAGMENT, True))
        check_eq("run: the role's four fields go in", stand.put(role)[0], 0)
        check_eq("run: the projection holds them beside the scaffold",
                 [(r["purpose"], r["novelty"]) for r in stand.manifest()["introduced_helpers"] if r["name"] == "make"], [("builds", "changed")])


def tq1_18_base_outcome() -> None:
    """TQ1-18 (D3-K19, D3-K20, D3-2; kills M-D3-8 on the writer's side): `manifest_put` refuses a `base_outcome` whose word is not one of
    the two and one with no run, before the commit; and the value a REAL `manifest_put` wrote reaches `ledger.test_state` (the proof
    that the field has a producer and a reader: `test_field_producers.py` does not walk manifest-row fields, S-7)."""
    import ledger as L
    check("the ledger's word is the writer's", L.BASE_REFUSED in MP.BASE_OUTCOMES, str(MP.BASE_OUTCOMES))
    row = {"instance_id": "test_move", "file": "tests/t.py", "covers": ["TC-018"], "case": "TC-018", "critic_verdict": "approved"}
    with Stand() as stand:
        check_eq("the row is sent", stand.put({"tests": [row]})[0], 0)
        for name, block in (("an unknown outcome", {"outcome": "refusde", "run": "A1"}), ("no run", {"outcome": "refused"}),
                            ("an empty run", {"outcome": "working", "run": " "}), ("not an object", "refused")):
            before = (stand.journal(), stand.tree())
            code, _out, err = stand.put({"tests": [dict(row, base_outcome=block)]})
            check_eq(f"K19: {name} is refused before the commit", (code, (stand.journal(), stand.tree())), (MP.EXIT_BAD_FRAGMENT, before))
            check_in(f"K19: {name}: the refusal names the field and what it expects", "`base_outcome`", err)
        check_in("K19: ... and the two words", '"refused" | "working"', err)
        check_eq("a good record is committed", stand.put({"tests": [dict(row, base_outcome={"outcome": "refused", "run": "A1"})]})[0], 0)
        entry = C.manifest_tests(stand.manifest())[0]
        check_eq("the record is on the row", entry.get("base_outcome"), {"outcome": "refused", "run": "A1"})
        report = {"current_results": [{"instance_id": "test_move", "case": "TC-018", "status": "passed", "attempt_id": "A1"}]}
        check_eq("D3-K20: the value the real writer stored reaches the ledger", L.test_state(entry, report, {"triage": []}, None,
                                                                                         stand.manifest())[0], L.NOT_VERIFIED_REFUSED_BASE)


def ep1_38_obligation_hash() -> None:
    """EP1-38 item 5 (AR-14): a `tests[]` row that SENDS an `obligation_hash` is checked against `content_hash(obligation_refs)`
    BEFORE the commit; the refs are the patch's, else the stored row's of the same instance (M-7). No hash -> not looked at."""
    from event_store import content_hash
    refs = [{"obligation_id": "OB-1", "obligation_hash": "h1"}, {"obligation_id": "OB-2", "obligation_hash": "h2"}]
    built = content_hash(refs)
    row = {"instance_id": "test_move", "file": "tests/t.py", "covers": ["TC-018"], "case": "TC-018", "status": "green"}
    check_eq("pure: a row with no hash is not looked at", MP.obligation_hash_problems({"tests": [dict(row, obligation_refs=refs)]}, []), [])
    check_eq("pure: the right hash of the patch's refs is accepted",
             MP.obligation_hash_problems({"tests": [dict(row, obligation_refs=refs, obligation_hash=built)]}, []), [])
    check_eq("pure: a null / empty hash is 'no hash'",
             MP.obligation_hash_problems({"tests": [dict(row, obligation_hash=None), dict(row, obligation_hash="")]}, []), [])
    check_eq("pure: no tests key, a non-dict row and a non-list stored are no problem",
             MP.obligation_hash_problems({}, None) + MP.obligation_hash_problems({"tests": ["x"]}, "y"), [])
    with Stand() as stand:
        check_eq("the row with its refs is sent (no hand hash)", stand.put({"tests": [dict(row, obligation_refs=refs)]})[0], 0)
        before = (stand.journal(), stand.tree())
        code, _out, err = stand.put({"tests": [dict(row, obligation_refs=refs, obligation_hash="zzz")]})
        check_eq("a wrong hash beside its refs is refused before the commit", (code, (stand.journal(), stand.tree())),
                 (MP.EXIT_BAD_FRAGMENT, before))
        check_in("... and says what the code builds", f"is not the hash of its obligation_refs ({built}); leave it out, the code builds it", err)
        check_in("... naming the row and the hash sent", "tests[0].obligation_hash zzz", err)
        code, _out, err = stand.put({"tests": [{"instance_id": "test_move", "obligation_hash": "zzz"}]})
        check_eq("M-7: a patch with no refs of its own is checked against the STORED refs of that instance",
                 (code, f"({built})" in err), (MP.EXIT_BAD_FRAGMENT, True))
        check_eq("M-7: ... and the right hash of the stored refs is accepted",
                 stand.put({"tests": [{"instance_id": "test_move", "obligation_hash": built}]})[0], 0)
        code, _out, err = stand.put({"tests": [dict(row, obligation_refs=[], obligation_hash=built)]})
        check_eq("empty refs in the patch + a hash: nothing to check it against -> refused",
                 (code, "cannot be checked: the row names no obligation_refs; leave it out, the code builds it" in err),
                 (MP.EXIT_BAD_FRAGMENT, True))
        code, _out, err = stand.put({"tests": [{"instance_id": "test_other", "file": "tests/t.py", "covers": ["TC-019"],
                                                "case": "TC-019", "obligation_hash": built}]})
        check_eq("a hash for an instance that holds no refs anywhere -> refused as unverifiable",
                 (code, "cannot be checked" in err), (MP.EXIT_BAD_FRAGMENT, True))
        check_eq("a patch that leaves the hash out is taken", stand.put({"tests": [dict(row, critic_verdict="approved")]})[0], 0)


def _plan_file(stand, ids=("OB-1", "OB-2"), text=None) -> dict:
    """The story's plan on disk: one schema-2 row naming `ids`; `{id: obligation}` of what it wrote. `text` writes that instead."""
    rows = [{"id": "TS-1", "schema_version": 2, "coverage_obligations": [{"obligation_id": i, "decision": "automate"} for i in ids]}]
    (stand.task / "work" / "test-plan.json").write_text(text if text is not None else json.dumps({"rows": rows}), encoding="utf-8")
    return {ob["obligation_id"]: ob for ob in rows[0]["coverage_obligations"]}


def _row_of(stand, iid="test_ob") -> dict:
    return next(t for t in stand.manifest()["tests"] if t["instance_id"] == iid)


def _ob_row(**extra) -> dict:
    return dict({"instance_id": "test_ob", "file": "tests/t.py", "covers": ["TC-018"], "case": "TC-018", "status": "green"}, **extra)


def fv1_19_predicate() -> None:
    """FV1-19 N1: the ONE reader of a valid obligation reference and the one stamp, pure (`contract`)."""
    from event_store import content_hash
    plan = {"OB-1": {"obligation_id": "OB-1", "decision": "a"}, "OB-2": {"obligation_id": "OB-2", "decision": "b"}}
    good = lambda oid: {"obligation_id": oid, "obligation_hash": content_hash(plan[oid])}   # noqa: E731
    check_eq("map: last occurrence wins; non-dict rows, non-list obligations, non-dict and id-less items are skipped",
             C.obligation_map([{"coverage_obligations": [{"obligation_id": "A", "v": 1}, "x", {"v": 2}]}, "row", {"coverage_obligations": "no"},
                               {"schema_version": 1, "coverage_obligations": [{"obligation_id": "A", "v": 3}]}]), {"A": {"obligation_id": "A", "v": 3}})
    check_eq("map: a non-list of rows is an empty map", (C.obligation_map(None), C.obligation_map("x")), ({}, {}))
    check_eq("predicate: valid refs and an empty list are no problem",
             (C.obligation_ref_problems([good("OB-1"), good("OB-2")], plan, strict=True), C.obligation_ref_problems([], plan, strict=True)), ([], []))
    kinds = lambda refs, m=plan, strict=False: [k for k, _t in C.obligation_ref_problems(refs, m, strict)]   # noqa: E731
    bad_hashes = ["h", good("OB-1")["obligation_hash"] + " ", good("OB-1")["obligation_hash"].upper(), content_hash(plan["OB-2"])]
    check_eq("predicate E19: a hash of another obligation, a trailing space, uppercase hex, a wrong hash are all stale",
             [kinds([{"obligation_id": "OB-1", "obligation_hash": h}]) for h in bad_hashes], [["stale"]] * 4)
    check_eq("predicate: an id of another case is unknown, naming the plan's ids",
             (kinds([good("OB-1") | {"obligation_id": "ob-1"}]), C.obligation_ref_problems([good("OB-1") | {"obligation_id": "ob-1"}], plan)[0][1]
              .endswith("(the plan names OB-1, OB-2)")), (["unknown"], True))
    check_eq("predicate: shape problems come ALONE (a broken list never reaches the hash comparison)",
             kinds([{"obligation_id": "OB-1", "obligation_hash": "stale"}, "junk", good("OB-2") | {"obligation_hash": None}]), ["shape", "shape"])
    check_eq("predicate: not a list / non-dict item / non-string id or hash / twice / missing hash are shape",
             [kinds(r) for r in ("OB-1", {"obligation_id": "OB-1"}, [1], [{"obligation_id": 7, "obligation_hash": "h"}],
                                 [{"obligation_id": "OB-1", "obligation_hash": 123}], [good("OB-1"), good("OB-1")],
                                 [{"obligation_id": "OB-1"}], [{"obligation_id": "OB-1", "obligation_hash": ""}])], [["shape"]] * 8)
    check_eq("predicate: strict with an empty or missing map makes EVERY ref unknown, as the finish reads it today",
             (kinds([good("OB-1"), good("OB-2")], {}, True), kinds([good("OB-1")], None, True)), (["unknown", "unknown"], ["unknown"]))
    check_eq("predicate: not strict with an empty or missing map judges shape only",
             (kinds([good("OB-1")], {}), kinds([good("OB-1")], None), kinds([{"obligation_id": "OB-1"}], None)), ([], [], ["shape"]))
    check_eq("predicate: strict with an empty map still returns shape alone when the list is broken", kinds(["x"], {}, True), ["shape"])
    sent = {"tests": [_ob_row(obligation_refs=[{"obligation_id": "OB-1"}])], "obligation_bindings": [{"obligation_id": "OB-1"}]}
    frozen = copy.deepcopy(sent)
    stamped, problems = C.stamp_obligation_refs(sent, plan)
    check_eq("stamp: pure - the input is never edited", sent, frozen)
    check_eq("stamp: the ref, the derived ids, the row hash and the binding hash are the code's",
             (problems, stamped["tests"][0]["obligation_refs"], stamped["tests"][0].get("obligation_ids"), stamped["tests"][0].get("obligation_hash"),
              stamped["obligation_bindings"]), ([], [good("OB-1")], ["OB-1"], content_hash([good("OB-1")]),
                                                [dict(good("OB-1"), judged_on={})]))
    check_eq("stamp: idempotent - the stamped rows stamp to themselves (a binding carrying the code's `judged_on` is refused, FV1-19e)",
             (C.stamp_obligation_refs({"tests": stamped["tests"]}, plan), len(C.stamp_obligation_refs(stamped, plan)[1])),
             (({"tests": stamped["tests"]}, []), 1))
    check_eq("(k) stamp: a binding with an id the plan does not name gets no stamp and no `judged_on` (a sent hash is dropped, F8 (a))",
             C.stamp_obligation_refs({"obligation_bindings": [{"obligation_id": "OB-9", "obligation_hash": "x"}, {"obligation_id": "OB-8"}]}, plan),
             ({"obligation_bindings": [{"obligation_id": "OB-9"}, {"obligation_id": "OB-8"}]}, []))
    check_eq("stamp: a non-string hash on a ref or a non-string id is refused as shape, never coerced",
             [len(C.stamp_obligation_refs({"tests": [_ob_row(obligation_refs=[r])]}, plan)[1]) for r in
              ({"obligation_id": "OB-1", "obligation_hash": 123}, {"obligation_id": 1}, {"obligation_id": ""})], [1, 1, 1])
    check_eq("stamp: a fragment with no tests and no bindings passes through (a non-dict too)",
             (C.stamp_obligation_refs({"unresolved": []}, plan), C.stamp_obligation_refs("x", plan)), (({"unresolved": []}, []), ("x", [])))
    want = content_hash(plan["OB-1"])
    hashed = lambda b, stored: C.stamp_obligation_refs({"obligation_bindings": [b]}, plan, stored)   # noqa: E731
    receipt = {"obligation_id": "OB-1", "review_receipt_ref": "r"}
    check_eq("B1 stamp: no stored binding (absent, None, not a list, non-dict items, another id), a stored one with no or an "
             "empty hash, a stored hash equal to the plan's -> stamped",
             [hashed(receipt, s)[0]["obligation_bindings"][0].get("obligation_hash") for s in
              (None, "x", {"obligation_id": "OB-1"}, [1, "x", None], [{"obligation_id": "OB-2", "obligation_hash": "old"}],
               [{"obligation_id": "OB-1"}], [{"obligation_id": "OB-1", "obligation_hash": ""}], [{"obligation_id": "OB-1", "obligation_hash": want}])],
             [want] * 8)
    stale = [{"obligation_id": "OB-1", "obligation_hash": "old", "design_assessment": "sufficient"}]
    check_eq("B1 stamp: a STALE stored binding + a hash-less patch (a receipt, a null hash, an empty hash, a null design_assessment) "
             "-> no hash key, no problem",
             [hashed(dict(receipt, **extra), stale) for extra in ({}, {"obligation_hash": None}, {"obligation_hash": ""}, {"design_assessment": None})],
             [({"obligation_bindings": [dict(receipt, judged_on={}, **({"design_assessment": None} if "design_assessment" in extra else {}))]}, [])
              for extra in ({}, {"obligation_hash": None}, {"obligation_hash": ""}, {"design_assessment": None})])
    check_eq("B1 stamp: a STALE stored binding + a re-sent design_assessment -> stamped (a re-judgment); the last stored row of an id is read",
             (hashed(dict(receipt, design_assessment="insufficient"), stale)[0]["obligation_bindings"][0]["obligation_hash"],
              hashed(receipt, [{"obligation_id": "OB-1", "obligation_hash": "old"}, {"obligation_id": "OB-1", "obligation_hash": want}])[0]
              ["obligation_bindings"][0].get("obligation_hash")), (want, want))
    check_eq("B1 stamp POSITIONAL: over a stale stored binding a wrong sent hash is still a problem, an unknown id still left alone",
             (len(hashed({"obligation_id": "OB-1", "obligation_hash": "zzz"}, stale)[1]),
              hashed({"obligation_id": "OB-9"}, [{"obligation_id": "OB-9", "obligation_hash": "old"}])), (1, ({"obligation_bindings": [{"obligation_id": "OB-9"}]}, [])))
    check_eq("F2 one shape wording: every shape text of the reader is the stamp's, but for the missing hash only the reader refuses",
             [(len(C.stamp_obligation_refs({"tests": [_ob_row(obligation_refs=r)]}, plan)[1]),
               [t for _k, t in C.obligation_ref_problems(r, plan)]
               == [t.replace("tests[0].obligation_refs", "obligation_refs") for t in C.stamp_obligation_refs({"tests": [_ob_row(obligation_refs=r)]}, plan)[1]])
              for r in ("OB-1", [1], [{"obligation_id": 7}], [{"obligation_id": "OB-1", "obligation_hash": 123}], [good("OB-1"), good("OB-1")])],
             [(1, True)] * 5)
    check_eq("F2 ... the missing hash: the reader says shape, the stamp writes the hash",
             ([k for k, _t in C.obligation_ref_problems([{"obligation_id": "OB-1"}], plan)],
              C.stamp_obligation_refs({"tests": [_ob_row(obligation_refs=[{"obligation_id": "OB-1"}])]}, plan)[1]), (["shape"], []))


def fv1_19_obligation_stamp() -> None:
    """FV1-19 N1 rows (a)-(g), (j), (k), (l), (m), (n), (q): `manifest_put.run` stamps the hashes; a role sends ids."""
    from event_store import content_hash
    ref = lambda plan, oid: {"obligation_id": oid, "obligation_hash": content_hash(plan[oid])}   # noqa: E731
    with Stand() as stand:
        plan = _plan_file(stand)
        code, _out, err = stand.put({"tests": [_ob_row(obligation_refs=[{"obligation_id": "OB-1"}])]})
        stored = _row_of(stand)
        check_eq("(a) ids only: the stored ref carries the plan's hash, the row its ids and the hash of the stored refs",
                 (code, err, stored["obligation_refs"], stored.get("obligation_ids"), stored.get("obligation_hash")),
                 (0, "", [ref(plan, "OB-1")], ["OB-1"], content_hash(stored["obligation_refs"])))
        before = (stand.journal(), stand.tree())
        code, _out, err = stand.put({"tests": [_ob_row(obligation_refs=[{"obligation_id": "OB-2", "obligation_hash": "zzz"}])]})
        check_eq("(b) a wrong hash is refused before the commit: exit, journal and tree unchanged", (code, (stand.journal(), stand.tree())),
                 (MP.EXIT_BAD_FRAGMENT, before))
        for what, needle in (("the id", "OB-2"), ("the hash sent", "zzz"), ("the plan's hash", content_hash(plan["OB-2"])),
                             ("the door", "leave `obligation_hash` out"), ("the repair marker", MP.REPAIR_MARKER)):
            check_in(f"(b) ... the refusal names {what}", needle, err)
        code, _out, err = stand.put({"tests": [_ob_row(obligation_refs=[{"obligation_id": "OB-2", "obligation_hash": content_hash(plan["OB-2"])}])]})
        check_eq("(b) the hash the code would write is accepted", (code, _row_of(stand)["obligation_refs"]), (0, [ref(plan, "OB-2")]))
        before = (stand.journal(), stand.tree())
        code, _out, err = stand.put({"tests": [_ob_row(obligation_refs=[{"obligation_id": "OB-9"}])]})
        check_eq("(c) an id the plan does not name is refused, naming the plan's ids", (code, (stand.journal(), stand.tree()), "the plan names OB-1, OB-2" in err),
                 (MP.EXIT_BAD_FRAGMENT, before, True))
        for what, refs in (("a string", "OB-1"), ("a dict", {"obligation_id": "OB-1"}), ("a list holding a non-dict", [1])):
            code, _out, err = stand.put({"tests": [_ob_row(obligation_refs=refs)]})
            check_eq(f"(e) refs that are {what} are refused (shape, with the expected shape)", (code, "obligation_refs" in err and '"obligation_id": "<plan obligation id>"' in err),
                     (MP.EXIT_BAD_FRAGMENT, True))
        code, _out, err = stand.put({"tests": [_ob_row(obligation_refs=[{"obligation_id": "OB-1"}, {"obligation_id": "OB-1"}])]})
        check_eq("(g) a duplicate id in one row is refused", (code, "OB-1 appears twice" in err), (MP.EXIT_BAD_FRAGMENT, True))
        check_eq("(g)+(e) a non-string id is refused as shape, never coerced",
                 stand.put({"tests": [_ob_row(obligation_refs=[{"obligation_id": 1}])]})[0], MP.EXIT_BAD_FRAGMENT)

        print("-- (f) null = not sent; [] clears")
        stand.put({"tests": [_ob_row(obligation_refs=[{"obligation_id": "OB-1"}, {"obligation_id": "OB-2"}])],
                   "obligation_bindings": [{"obligation_id": "OB-1", "instance_ids": ["test_ob"]}]})
        held = copy.deepcopy(_row_of(stand))
        binding = copy.deepcopy(stand.manifest()["obligation_bindings"][0])
        check_eq("(f) the binding was stamped", binding.get("obligation_hash"), content_hash(plan["OB-1"]))
        # Re-seeded (FV1-19 B1): the plan's OB-1 changes, so the stored binding hash is STALE - a null must keep it, not restamp it.
        replanned = {"obligation_id": "OB-1", "decision": "manual"}
        _plan_file(stand, text=json.dumps({"rows": [{"id": "TS-1", "schema_version": 2, "coverage_obligations": [
            replanned, {"obligation_id": "OB-2", "decision": "automate"}]}]}))
        code, _out, err = stand.put({"tests": [_ob_row(obligation_refs=None, obligation_ids=None, obligation_hash=None, status="red")],
                                     "obligation_bindings": [{"obligation_id": "OB-1", "obligation_hash": None, "sensitivity": "proven"}]})
        now = _row_of(stand)
        check_eq("(f) nulls keep the stored refs, ids and row hash (the key is dropped before the merge)",
                 (code, now["status"], {k: now[k] for k in ("obligation_refs", "obligation_ids", "obligation_hash")}),
                 (0, "red", {k: held[k] for k in ("obligation_refs", "obligation_ids", "obligation_hash")}))
        check_eq("(f) a binding `obligation_hash: null` keeps the stored (STALE) binding hash, not the re-planned one",
                 (stand.manifest()["obligation_bindings"][0], binding["obligation_hash"] != content_hash(replanned)),
                 (binding | {"sensitivity": "proven"}, True))
        _plan_file(stand)
        code, _out, err = stand.put({"tests": [_ob_row(obligation_refs=[])]})
        now = _row_of(stand)
        check_eq("(f) [] clears refs, ids and the row hash", (code, now["obligation_refs"], now["obligation_ids"], now["obligation_hash"]), (0, [], [], ""))

        print("-- (m) the ids the role sends")
        two = [{"obligation_id": "OB-1"}, {"obligation_id": "OB-2"}]
        code, _out, err = stand.put({"tests": [_ob_row(obligation_refs=two, obligation_ids=["OB-1"])]})
        check_eq("(m) obligation_ids that differ as a set from the refs are refused", (code, "leave it out, the code writes it" in err),
                 (MP.EXIT_BAD_FRAGMENT, True))
        code, _out, err = stand.put({"tests": [_ob_row(obligation_refs=two, obligation_ids=["OB-2", "OB-1"])]})
        check_eq("(m) the same set in another order is accepted, stored in refs order", (code, _row_of(stand)["obligation_ids"]), (0, ["OB-1", "OB-2"]))
        code, _out, err = stand.put({"tests": [_ob_row(instance_id="test_ids_only", obligation_ids=["OB-2"])]})
        check_eq("(m) a row sending only obligation_ids is stored as sent (today's behaviour)",
                 (code, _row_of(stand, "test_ids_only")["obligation_ids"]), (0, ["OB-2"]))

        print("-- (n) the row hash never outlives its refs")
        h_old = _row_of(stand)["obligation_hash"]
        code, _out, err = stand.put({"tests": [_ob_row(obligation_refs=[{"obligation_id": "OB-2"}], fit_note="n")]})
        now = _row_of(stand)
        check_eq("(n) an ids-only fragment over a stored row: the row hash is the hash of the NEW stamped refs",
                 (code, now["obligation_hash"] == content_hash(now["obligation_refs"]), now["obligation_hash"] != h_old), (0, True, True))

        print("-- (k) bindings")
        code, _out, err = stand.put({"obligation_bindings": [{"obligation_id": "OB-2", "instance_ids": ["test_ob"]}]})
        check_eq("(k) a binding without a hash is stamped", (code, next(b for b in stand.manifest()["obligation_bindings"] if b["obligation_id"] == "OB-2")
                                                              .get("obligation_hash")), (0, content_hash(plan["OB-2"])))
        before = (stand.journal(), stand.tree())
        code, _out, err = stand.put({"obligation_bindings": [{"obligation_id": "OB-2", "obligation_hash": "zzz"}]})
        check_eq("(k) a binding with a wrong hash is refused", (code, (stand.journal(), stand.tree()), "leave `obligation_hash` out" in err),
                 (MP.EXIT_BAD_FRAGMENT, before, True))
        code, _out, err = stand.put({"obligation_bindings": [{"obligation_id": "OB-9"}]})
        check_eq("(k) a binding with an id the plan does not name keeps the `obligation-id` refusal and its word road",
                 (code, "obligation ids not in the plan: OB-9" in err, 'waiver.py --task <TICKET> --stage S5 --block "obligation-id"' in err),
                 (MP.EXIT_BAD_FRAGMENT, True, True))

    print("-- B1: a hash-less binding patch never refreshes a STALE stored binding hash; a re-sent design_assessment does")
    with Stand() as stand:
        _plan_file(stand)
        stand.put({"obligation_bindings": [{"obligation_id": "OB-1", "instance_ids": ["test_ob"], "design_assessment": "sufficient"}]})
        old_hash = stand.manifest()["obligation_bindings"][0]["obligation_hash"]
        replanned = {"obligation_id": "OB-1", "decision": "manual"}
        _plan_file(stand, text=json.dumps({"rows": [{"id": "TS-1", "schema_version": 2, "coverage_obligations": [
            replanned, {"obligation_id": "OB-2", "decision": "automate"}]}]}))
        stored_b = lambda: stand.manifest()["obligation_bindings"][0]   # noqa: E731
        for what, patch in (("review-receipt", {"review_receipt_ref": "state/r.json"}), ("sensitivity-only", {"sensitivity": "proven"})):
            code, _out, err = stand.put({"obligation_bindings": [dict({"obligation_id": "OB-1"}, **patch)]})
            check_eq(f"B1 a stale stored binding + a hash-less {what} patch: stored, the stored hash unchanged, still not current",
                     (code, {k: stored_b().get(k) for k in patch}, stored_b()["obligation_hash"], stored_b()["obligation_hash"] == content_hash(replanned)),
                     (0, patch, old_hash, False))
        before = (stand.journal(), stand.tree())
        code, _out, err = stand.put({"obligation_bindings": [{"obligation_id": "OB-1", "obligation_hash": "zzz", "review_receipt_ref": "x"}]})
        check_eq("B1 POSITIONAL: over a stale stored binding a caller-sent wrong hash is still refused, nothing written",
                 (code, (stand.journal(), stand.tree())), (MP.EXIT_BAD_FRAGMENT, before))
        code, _out, err = stand.put({"obligation_bindings": [{"obligation_id": "OB-9", "review_receipt_ref": "x"}]})
        check_eq("B1 POSITIONAL: an id the plan does not name is still refused", (code, (stand.journal(), stand.tree())), (MP.EXIT_BAD_FRAGMENT, before))
        code, _out, err = stand.put({"obligation_bindings": [{"obligation_id": "OB-1", "design_assessment": "sufficient"}]})
        check_eq("B1 a stale stored binding + a hash-less patch re-sending design_assessment is a re-judgment: stamped with the current plan hash",
                 (code, stored_b()["obligation_hash"]), (0, content_hash(replanned)))

    print("-- (d) an empty plan and no plan: the refs are stored as sent")
    for what, write in (("no plan file", None), ("a plan naming no obligation", {"rows": [{"id": "TS-1", "schema_version": 2}]})):
        with Stand() as stand:
            if write is not None:
                _plan_file(stand, text=json.dumps(write))
            code, _out, err = stand.put({"tests": [_ob_row(obligation_refs=[{"obligation_id": "OB-1"}, {"obligation_id": "OB-2", "obligation_hash": "typed"}])]})
            now = _row_of(stand)
            check_eq(f"(d) {what}: exit 0, no note, no hash added, ids and row hash derived",
                     (code, err, now["obligation_refs"], now["obligation_ids"], now["obligation_hash"] == content_hash(now["obligation_refs"])),
                     (0, "", [{"obligation_id": "OB-1"}, {"obligation_id": "OB-2", "obligation_hash": "typed"}], ["OB-1", "OB-2"], True))

    print("-- (q) a plan that is not JSON")
    with Stand() as stand:
        _plan_file(stand, text="{not json")
        code, _out, err = stand.put({"tests": [_ob_row(obligation_refs=[{"obligation_id": "OB-1"}])]})
        notes = [line for line in err.splitlines() if line.startswith("manifest_put: note: the plan")]
        check_eq("(q) exit 0, ONE note line naming what the finish will do, the refs stored as sent",
                 (code, len(err.splitlines()), len(notes), "without hashes, and the window finish refuses them until the plan reads" in err,
                  _row_of(stand)["obligation_refs"]), (0, 1, 1, True, [{"obligation_id": "OB-1"}]))

    print("-- (l) magnitude")
    with Stand() as stand:
        many = {f"O-{n}": {"obligation_id": f"O-{n}"} for n in range(1000)}
        rows = [{"id": "TS-1", "schema_version": 2, "coverage_obligations": list(many.values())}]
        (stand.task / "work" / "test-plan.json").write_text(json.dumps({"rows": rows}), encoding="utf-8")
        refs = [{"obligation_id": oid} for oid in many]
        for at in (3, 500, 999):
            refs[at]["obligation_hash"] = "typo"
        code, _out, err = stand.put({"tests": [_ob_row(obligation_refs=refs)]})
        check_eq("(l) 1000 refs, 3 bad: ONE refusal line naming the 3 and no more",
                 (code, len(err.strip().splitlines()), [f"O-{n} carries hash typo" in err for n in (3, 500, 999)], err.count("carries hash")),
                 (MP.EXIT_BAD_FRAGMENT, 1, [True] * 3, 3))
        check_eq("(l) 1000 refs, 0 bad: one write", stand.put({"tests": [_ob_row(obligation_refs=[{"obligation_id": oid} for oid in many])]})[0], 0)
    ceiling = 6000
    for beyond in (0, 1):
        with Stand() as stand:
            def two_problems(pad):
                ids = ["A" * 40, "B" * pad]
                plan = _plan_file(stand, ids=ids)
                frag = {"tests": [_ob_row(obligation_refs=[{"obligation_id": i, "obligation_hash": "zz"} for i in ids])]}
                return frag, C.stamp_obligation_refs(frag, plan)[1]
            pad = 40
            while len("; ".join(two_problems(pad)[1])) < ceiling + beyond:
                pad += 1
            frag, problems = two_problems(pad)
            joined = "; ".join(problems)
            before = stand.tree()
            code, _out, err = stand.put(frag)
            spill = stand.task / "state" / "findings" / "manifest-put-obligation-refs.txt"
            if not beyond:
                check_eq("(l) AT the ceiling (joined text exactly 6000 characters): the whole list in the line, no pointer, no file",
                         (len(joined), code, joined in err, "more problem" in err, spill.exists()), (6000, MP.EXIT_BAD_FRAGMENT, True, False, False))
            else:
                spilled = spill.read_text(encoding="utf-8") if spill.exists() else ""
                check_eq("(l) BEYOND (6001): the items that fit, the pointer, and the file holding every problem",
                         (len(joined), code, "(+1 more problem(s) — the whole list: " in err, "manifest-put-obligation-refs.txt)" in err,
                          problems[0] in err, problems[1] in err, all(p in spilled for p in problems)),
                         (6001, MP.EXIT_BAD_FRAGMENT, True, True, True, False, True))
                (stand.task / "state" / "findings" / "manifest-put-obligation-refs.txt").unlink()
                (stand.task / "state" / "findings").rmdir()
                (stand.task / "state" / "findings").write_text("a file where the folder should be", encoding="utf-8")
                code, _out, err = stand.put(frag)
                check_eq("(l) the spill file that cannot be written: the refusal still prints, saying so, no crash",
                         (code, "the whole list could not be saved" in err), (MP.EXIT_BAD_FRAGMENT, True))

    print("-- (j) a journal holding old unstamped events folds unchanged; merge stays pure")
    old = {"tests": [_ob_row(obligation_refs=[{"obligation_id": "OB-1", "obligation_hash": "stale"}, {"obligation_id": "OB-7"}],
                             obligation_ids=["OB-1"], obligation_hash="whatever")]}
    folded = MP.fold(journal(old))
    check_eq("(j) the replay stores the old event as it was written: no stamp, no refusal", folded["tests"][0],
             {**old["tests"][0], "obligation_refs": old["tests"][0]["obligation_refs"]})
    check_eq("(j) merge itself never stamps", MP.merge({}, old)[0]["tests"][0]["obligation_refs"], old["tests"][0]["obligation_refs"])


def fv1_19e_binding_currency() -> None:
    """FV1-19e table T1 "binding currency" (rows r1-r17): a judgment field counts only when the plan hash it was stamped with
    equals the current obligation's; the stamp (`stamp_obligation_refs`) and the per-key fold (`merge`) are the only writers."""
    from event_store import content_hash
    import migrate_artifacts as MA
    ob = lambda d: {"obligation_id": "OB-1", "decision": d}   # noqa: E731
    h = lambda d: content_hash(ob(d))   # noqa: E731
    both = lambda a, c: {"design_assessment": a, "code_validity": c}   # noqa: E731
    TT, FF, TF, FT = both(True, True), both(False, False), both(True, False), both(False, True)
    plan_of = lambda d: {"rows": [{"id": "TS-1", "schema_version": 2, "coverage_obligations": [ob(d)]}]}   # noqa: E731
    judged = {"obligation_id": "OB-1", "design_assessment": "sufficient", "code_validity": "valid"}
    w1 = lambda d, **extra: dict(judged, obligation_hash=h(d), **extra)   # noqa: E731  # a binding as it was written before C1

    def bound(stand):
        return next((b for b in stand.manifest().get("obligation_bindings") or [] if b["obligation_id"] == "OB-1"), None)

    def run_steps(stand, steps):
        codes = []
        for kind, what in steps:
            if kind == "plan":
                _plan_file(stand, text=json.dumps(plan_of(what)))
            elif kind == "noplan":
                (stand.task / "work" / "test-plan.json").unlink()
            elif kind == "world1":
                stand.append_projected({"fragment": {"obligation_bindings": [what]}}, f"w1-{len(codes)}")
            else:
                codes.append(stand.put({"obligation_bindings": [what]})[0])
        return codes

    step1 = [("plan", "P1"), ("put", judged)]
    redesign = ("put", {"obligation_id": "OB-1", "design_assessment": "sufficient"})
    for name, steps, final, currency, stamps in (
            ("r1 world 2: both judgments stamped with P1's hash", step1, "P1", TT, {"code_validity": h("P1")}),
            ("r2 (the defect) re-plan, re-send ONLY design_assessment: validity stops counting", step1 + [("plan", "P2"), redesign],
             "P2", TF, {"code_validity": h("P1")}),
            ("r3 ... then re-send code_validity: it counts again", step1 + [("plan", "P2"), redesign, ("put", {"obligation_id": "OB-1", "code_validity": "valid"})],
             "P2", TT, {"code_validity": h("P2")}),
            ("r4 receipt-only and sensitivity-only patches over a stale binding make nothing current",
             step1 + [("plan", "P2"), ("put", {"obligation_id": "OB-1", "review_receipt_ref": "r"}),
                      ("put", {"obligation_id": "OB-1", "sensitivity": "proven"})], "P2", FF, {"code_validity": h("P1")}),
            ("r6 world 1 + a design-only re-send under P2: the legacy currency is materialized from the STORED hash",
             [("plan", "P1"), ("world1", w1("P1")), ("plan", "P2"), redesign], "P2", TF, {"code_validity": h("P1")}),
            ("r7 ... and the plan back to P1: the old text counts again, the re-judged design does not",
             [("plan", "P1"), ("world1", w1("P1")), ("plan", "P2"), redesign, ("plan", "P1")], "P1", FT, {"code_validity": h("P1")})):
        with Stand() as stand:
            codes = run_steps(stand, steps)
            b = bound(stand)
            check_eq(name, (codes, C.binding_currency(b, h(final)), b.get("judged_on")), ([0] * len(codes), currency, stamps))

    print("-- r5 world 1: an old-shape event (no judged_on) folded through merge keeps today's reading")
    folded = MP.fold(journal({"obligation_bindings": [w1("P1")]}))["obligation_bindings"][0]
    check_eq("r5 under P1 every field is current, under P2 none; no judged_on invented by the fold",
             (C.binding_currency(folded, h("P1")), C.binding_currency(folded, h("P2")), "judged_on" in folded), (TT, FF, False))

    print("-- r8 a sent judged_on is refused with a door; null is dropped")
    with Stand() as stand:
        _plan_file(stand, text=json.dumps(plan_of("P1")))
        before = (stand.journal(), stand.tree())
        for what in ({}, {"code_validity": h("P1")}, "x", [], {"a": {"b": 1}}, {f"k{n}": n for n in range(10000)}):
            code, _out, err = stand.put({"obligation_bindings": [dict(judged, judged_on=what)]})
            check_eq(f"r8 judged_on {str(what)[:30]!r}: refused, journal and tree unchanged, the stderr names the field and the door",
                     (code, (stand.journal(), stand.tree()), "judged_on" in err, "leave it out, the code writes it" in err),
                     (MP.EXIT_BAD_FRAGMENT, before, True, True))
        check_eq("r8 judged_on null: exit 0, the key is the code's (never null)",
                 (stand.put({"obligation_bindings": [dict(judged, judged_on=None)]})[0], bound(stand)["judged_on"]),
                 (0, {"code_validity": h("P1")}))

    print("-- r9, r10 a sent hash never refreshes; with no plan nothing is stamped and the stored stamps stand")
    with Stand() as stand:
        run_steps(stand, step1 + [("plan", "P2")])
        code, _out, _err = stand.put({"obligation_bindings": [{"obligation_id": "OB-1", "obligation_hash": h("P2"), "review_receipt_ref": "r"}]})
        check_eq("r9 a sent hash EQUAL to the plan's over a stale binding without design_assessment: stored hash unchanged",
                 (code, bound(stand)["obligation_hash"]), (0, h("P1")))
    with Stand() as stand:
        code, _out, _err = stand.put({"obligation_bindings": [{"obligation_id": "OB-1", "code_validity": "valid", "obligation_hash": "zzz"}]})
        check_eq("r10 no plan file: exit 0, no judged_on written, the sent hash not stored",
                 (code, "judged_on" in bound(stand), "obligation_hash" in bound(stand)), (0, False, False))
    with Stand() as stand:
        run_steps(stand, step1 + [("noplan", None)])
        code, _out, _err = stand.put({"obligation_bindings": [{"obligation_id": "OB-1", "code_validity": "valid", "obligation_hash": "zzz"}]})
        check_eq("r10 over a stored world-2 binding the stamps are unchanged (the new value inherits h(P1))",
                 (code, bound(stand)["judged_on"], bound(stand)["obligation_hash"]), (0, {"code_validity": h("P1")}, h("P1")))
    with Stand() as stand:
        run_steps(stand, [("plan", "P1"), ("world1", w1("P1")), ("noplan", None)])
        code, _out, _err = stand.put({"obligation_bindings": [{"obligation_id": "OB-1", "code_validity": "valid", "obligation_hash": "zzz"}]})
        check_eq("r10 over a stored world-1 binding the stored hash is unchanged and no judged_on appears",
                 (code, bound(stand)["obligation_hash"], "judged_on" in bound(stand)), (0, h("P1"), False))

    print("-- r11 old events fold unchanged, a world-2 journal folds the same twice")
    old_events = journal({"obligation_bindings": [w1("P1")]}, {"obligation_bindings": [{"obligation_id": "OB-1", "sensitivity": "proven"}]})
    check_eq("r11 old events fold to exactly what dict(old, **new) says, no judged_on",
             MP.fold(old_events)["obligation_bindings"], [dict(w1("P1"), sensitivity="proven")])
    new_events = journal({"obligation_bindings": [dict(w1("P1"), judged_on={"code_validity": h("P1")})]},
                         {"obligation_bindings": [{"obligation_id": "OB-1", "design_assessment": "partial", "judged_on": {}}]})
    check_eq("r11 a world-2 journal folded twice gives equal results", MP.fold(new_events), MP.fold(copy.deepcopy(new_events)))

    print("-- r12 race shape: two stamps computed from one snapshot, applied in both orders")
    plan2 = {"OB-1": ob("P2")}
    snapshot = [dict(w1("P1"), judged_on={"code_validity": h("P1")})]
    frag_a = C.stamp_obligation_refs({"obligation_bindings": [{"obligation_id": "OB-1", "design_assessment": "sufficient"}]}, plan2, snapshot)[0]
    frag_b = C.stamp_obligation_refs({"obligation_bindings": [{"obligation_id": "OB-1", "code_validity": "valid"}]}, plan2, snapshot)[0]
    frag_c = C.stamp_obligation_refs({"obligation_bindings": [{"obligation_id": "OB-1", "review_receipt_ref": "r"}]}, plan2, snapshot)[0]
    for label, second, expect_validity in (("validity re-send", frag_b, True), ("receipt only", frag_c, False)):
        for order in ((frag_a, second), (second, frag_a)):
            state = {"obligation_bindings": copy.deepcopy(snapshot)}
            for frag in order:
                state, _s = MP.merge(state, copy.deepcopy(frag))
            check_eq(f"r12 {label}: validity counts iff its own fragment stamped it with the current hash",
                     C.binding_currency(state["obligation_bindings"][0], h("P2"))["code_validity"], expect_validity)

    print("-- r13 the code writers forward no judged_on")
    row = dict(judged, judged_on={"code_validity": "x"}, obligation_hash="hb")
    check_eq("r13 _forwardable drops judged_on on both branches",
             ["judged_on" in MA._forwardable(row, refs) for refs in (True, False)], [False, False])

    print("-- r14 binding_currency errs only toward not current")
    hp = h("P1")
    bad = [("judged_on []", dict(judged, obligation_hash="o", judged_on=[]), hp), ("judged_on 'x'", dict(judged, obligation_hash="o", judged_on="x"), hp),
           ("judged_on None", dict(judged, obligation_hash="o", judged_on=None), hp),
           ("trailing space", dict(judged, obligation_hash="o", judged_on={"code_validity": hp + " "}), hp),
           ("uppercase hex", dict(judged, obligation_hash="o", judged_on={"code_validity": hp.upper()}), hp),
           ("int stamp", dict(judged, obligation_hash="o", judged_on={"code_validity": 123}), hp),
           ("empty stamp, empty plan hash", dict(judged, obligation_hash="o", judged_on={"code_validity": ""}), ""),
           ("hash None, judged_on absent", dict(judged, obligation_hash=None), hp), ("hash absent, judged_on absent", dict(judged), hp),
           ("not a dict", "x", hp), ("None", None, hp), ("plan hash None", dict(judged, obligation_hash=hp, judged_on={"code_validity": hp}), None),
           ("plan hash int", dict(judged, obligation_hash=5, judged_on={"code_validity": 5}), 5)]
    check_eq("r14 every adversarial input reads not current", [(n, C.binding_currency(b, p)) for n, b, p in bad], [(n, FF) for n, _b, _p in bad])

    print("-- r16 F5 (b): a stored binding with no hash and a COUNTING design is not stamped by a receipt")
    plan1 = {"OB-1": ob("P1")}
    want = h("P1")
    stamp = lambda b, stored=None, **frag: C.stamp_obligation_refs({"obligation_bindings": [b], **frag}, plan1, stored)   # noqa: E731
    receipt = {"obligation_id": "OB-1", "review_receipt_ref": "r"}
    out_hash = lambda b, stored: stamp(b, stored)[0]["obligation_bindings"][0].get("obligation_hash")   # noqa: E731
    check_eq("r16 counting design, no hash: no hash key; `unknown`: stamped; counting + a re-sent design: stamped; no design: stamped",
             [out_hash(receipt, [{"obligation_id": "OB-1", "design_assessment": "sufficient"}]),
              out_hash(receipt, [{"obligation_id": "OB-1", "design_assessment": "unknown"}]),
              out_hash(dict(receipt, design_assessment="sufficient"), [{"obligation_id": "OB-1", "design_assessment": "sufficient"}]),
              out_hash(receipt, [{"obligation_id": "OB-1"}])], [None, want, want, want])

    print("-- r17 B-1, B26: a rename carries the OLD stamps, never the plan's hash, and renamed_from is never stored")
    renamed = {"obligation_id": "OB-1", "renamed_from": "X", "design_assessment": "sufficient", "code_validity": "valid"}
    gone = {"retracted_obligations": ["X"]}
    pull = lambda stored, b=renamed, **frag: stamp(b, stored, **(frag or gone))   # noqa: E731
    out_b = lambda stored, b=renamed: pull(stored, b)[0]["obligation_bindings"][0]   # noqa: E731
    stale_x = out_b([{"obligation_id": "X", "obligation_hash": "old"}])
    check_eq("r17 X hash old: the hash and the validity stamp are old, no renamed_from, nothing current",
             (stale_x["obligation_hash"], stale_x["judged_on"], "renamed_from" in stale_x, C.binding_currency(stale_x, want)),
             ("old", {"code_validity": "old"}, False, FF))
    fresh_x = out_b([{"obligation_id": "X", "obligation_hash": want}])
    check_eq("r17 X hash == the plan's: carried and current", (fresh_x["obligation_hash"], fresh_x["judged_on"], C.binding_currency(fresh_x, want)),
             (want, {"code_validity": want}, TT))
    bare_x = out_b([{"obligation_id": "X"}])
    check_eq("r17 X with no hash and no judged_on: no hash key, judged_on {}", ("obligation_hash" in bare_x, bare_x["judged_on"]), (False, {}))
    check_eq("r17 X with its own judged_on: that stamp is carried",
             out_b([{"obligation_id": "X", "obligation_hash": "old", "judged_on": {"code_validity": "jv"}}])["judged_on"], {"code_validity": "jv"})
    check_eq("r17 a binding with no design_assessment (only sensitivity) over X hash old: the plan's hash, as a row (o)",
             out_b([{"obligation_id": "X", "obligation_hash": "old"}], {"obligation_id": "OB-1", "renamed_from": "X", "sensitivity": "proven"})["obligation_hash"],
             want)
    stored_x = [{"obligation_id": "X", "obligation_hash": "old"}]
    for what, value, stored, frag in (("5", 5, stored_x, gone), ("empty", "", stored_x, gone), ("a list", [], stored_x, gone),
                                      ("an id the fragment does not retract", "Y", stored_x + [{"obligation_id": "Y"}], gone),
                                      ("retracted_obligations not a list", "X", stored_x, {"retracted_obligations": "X"}),
                                      ("retracted but no stored binding", "X", [], gone),
                                      ("the binding's own id", "OB-1", [{"obligation_id": "OB-1"}], {"retracted_obligations": ["OB-1"]})):
        problems = pull(stored, dict(renamed, renamed_from=value), **frag)[1]
        check_eq(f"r17 renamed_from {what}: exactly one problem naming the key and the migration",
                 (len(problems), "renamed_from" in "".join(problems), "it is the migration's" in "".join(problems)), (1, True, True))
    null_out, null_problems = pull(stored_x, dict(renamed, renamed_from=None))
    check_eq("r17 renamed_from null: dropped, no problem, the normal stamp", (null_problems, null_out["obligation_bindings"][0]["obligation_hash"],
             "renamed_from" in null_out["obligation_bindings"][0]), ([], want, False))

    print("-- r15 a judged field sent as null is not stamped and never counts")
    with Stand() as stand:
        run_steps(stand, [("plan", "P1"), ("put", dict(judged, code_validity=None))])
        b = bound(stand)
        check_eq("r15 stored null, judged_on {}, not counting", (b.get("code_validity"), b["judged_on"], C.counting_value(b, "code_validity")),
                 (None, {}, False))


def t9(iid: str = "test_nine[a]", **extra) -> dict:
    return dict({"instance_id": iid, "file": "tests/test_nine.py", "case": "TC-009", "covers": ["TC-009"]}, **extra)


THEN_ROW = {"case": "TC-009", "reason": CONTRADICTS, "thens": [2], "detail": "Then 2 contradicts the requirement"}


def tests_of(manifest: dict) -> list:
    return sorted(MP._instance(e) for e in manifest.get("tests") or [])


def ep1_39_then_row_keeps_tests() -> None:
    """EP1-39 (AR-14, AR-23, AR-25, AR-27): a `contradicts_requirement` row that names only Thens of a case that RAN does not
    take the case's `tests[]` rows with it; the rows that were taken are named. Table `edges` of the spec, one line per row."""
    # the tests are STORED and the fragment sends the row alone: only a stored row can be moved out by it
    send = lambda tests, row: MP.merge({"tests": copy.deepcopy(tests)}, {"unresolved": [row]})[0]
    # the predicate: one home (AR-13), and the forms that do NOT widen the protection
    check_eq("pred: the Then row is `contradicts_requirement` + non-empty `thens` list + no slice",
             (C.then_scoped_row(THEN_ROW), MP._then_row(THEN_ROW)), (True, True))
    for label, odd in (("thens []", dict(THEN_ROW, thens=[])), ("thens ''", dict(THEN_ROW, thens="")),
                       ("no thens", {k: v for k, v in THEN_ROW.items() if k != "thens"}), ("thens '2'", dict(THEN_ROW, thens="2")),
                       ("another reason", dict(THEN_ROW, reason="impossible")), ("blocked_by_env", dict(THEN_ROW, reason=BLOCKED)),
                       ("a slice", dict(THEN_ROW, instance_ids=["x"])), ("partitions", dict(THEN_ROW, partitions=["P-a"])),
                       ("not a dict", "x")):
        check_eq(f"pred: {label} is not the Then row", (C.then_scoped_row(odd), MP._then_row(odd)), (False, False))

    # a test that ran stands, and so does the row
    for label, status in (("a handwritten row with NO status (M-2)", {}), ("status ''", {"status": ""}), ("green", {"status": "green"}),
                          ("red", {"status": "red"})):
        merged = send([t9(**status)], THEN_ROW)
        check_eq(f"E-then-row: {label} + thens [2] with no slice -> the test stays and the row stays",
                 (tests_of(merged), cases(merged)), (["test_nine[a]"], ["TC-009"]))
    # a test that did not run is wholly unresolved, and the loss is named
    for status in ("pending_run", "not_run", "blocked_by_env"):
        merged = send([t9(status=status)], THEN_ROW)
        check_eq(f"M-2: status {status} is not a run -> the case is wholly unresolved", (tests_of(merged), cases(merged)), ([], ["TC-009"]))
    # the row without Thens, or with an unreadable `thens`, keeps its whole-case meaning
    for label, row in (("thens []", dict(THEN_ROW, thens=[])), ("thens ''", dict(THEN_ROW, thens="")),
                       ("no thens", {k: v for k, v in THEN_ROW.items() if k != "thens"}), ("thens '2'", dict(THEN_ROW, thens="2")),
                       ("another reason + thens", dict(THEN_ROW, reason="impossible")),
                       ("blocked_by_env + thens", dict(THEN_ROW, reason=BLOCKED))):
        check_eq(f"E-then-row: {label} -> the whole case, the test row goes", tests_of(send([t9(status="red")], row)), [])
    check_eq("slice: thens + instance_ids stays a slice, as today (the tests stay)",
             tests_of(send([t9(status="red")], dict(THEN_ROW, instance_ids=["test_nine[a]"]))), ["test_nine[a]"])
    # no instance that ran
    stored = {"tests": [t9(status="pending_run")]}
    merged = MP.merge(copy.deepcopy(stored), {"unresolved": [THEN_ROW]})[0]
    check_eq("no ran instance (only a pending one stored): the whole case, the row goes", (tests_of(merged), cases(merged)), ([], ["TC-009"]))
    merged = MP.merge({"tests": [t9(status="red")]}, {"unresolved": [THEN_ROW]})[0]
    check_eq("a ran instance STORED (the fragment sends none): the row stands", (tests_of(merged), cases(merged)), (["test_nine[a]"], ["TC-009"]))
    # a ran row of the FRAGMENT protects a stored pending sibling (the incoming side of `_ran_rows`)
    merged = MP.merge({"tests": [t9("test_nine[b]", status="pending_run")]},
                      {"tests": [t9("test_nine[a]", status="red")], "unresolved": [THEN_ROW]})[0]
    check_eq("_ran_rows reads the fragment's rows too: red a keeps pending b", (tests_of(merged), cases(merged)),
             (["test_nine[a]", "test_nine[b]"], ["TC-009"]))
    # the consolidated instance
    consolidated = {"instance_id": "t[all]", "file": "t.py", "case": "TC-003", "covers": ["TC-003", "TC-004", "TC-005"], "status": "red"}
    check_eq("`_moved_out:433`: a consolidated TC-003/004/005 with one Then row on TC-003 stays",
             tests_of(send([consolidated], dict(THEN_ROW, case="TC-003"))), ["t[all]"])

    # M-1: the stored Then row is taken by an explicit green only, and not beside a red instance
    base9 = {"unresolved": [dict(THEN_ROW)]}
    gone, _ = MP.merge(copy.deepcopy(base9), {"tests": [GREEN_TC9]})
    check_eq("pin GREEN_TC9: the only green instance, explicit -> the Then row is taken", cases(gone), [])
    red_b = t9("test_nine[b]", status="red")
    kept, _ = MP.merge({"unresolved": [dict(THEN_ROW)], "tests": [red_b]}, {"tests": [t9("test_nine[a]", status="green")]})
    check_eq("M-1: green a beside the STORED red b -> the row stands", (cases(kept), tests_of(kept)), (["TC-009"], ["test_nine[a]", "test_nine[b]"]))
    kept, _ = MP.merge({"unresolved": [dict(THEN_ROW)]}, {"tests": [t9("test_nine[a]", status="green"), t9("test_nine[b]", status="red")]})
    check_eq("M-1: green a and red b in ONE fragment -> the row stands", cases(kept), ["TC-009"])
    for label, status in (("no status (a critic patch)", {}), ("status ''", {"status": ""})):
        kept, _ = MP.merge({"unresolved": [dict(THEN_ROW)]}, {"tests": [t9(**status)]})
        check_eq(f"reverse hole: {label} is no explicit green -> the Then row stands", cases(kept), ["TC-009"])
    kept, _ = MP.merge({"unresolved": [dict(THEN_ROW)], "tests": [t9(status="red")]},
                       {"tests": [{"instance_id": "test_nine[a]", "critic_verdict": "approved", "critic_note": "re-read"}]})
    check_eq("reverse hole: a critic patch with no `status` over a stored row -> the Then row stands", (cases(kept), tests_of(kept)),
             (["TC-009"], ["test_nine[a]"]))

    # F-3 (t-555): a patch that names only the instance is read OVER its stored row, so it cannot hide a stored red
    a_green = t9("test_nine[a]", status="green")
    stored_ab = {"tests": [a_green, red_b], "unresolved": [dict(THEN_ROW)]}
    patch_b = {"instance_id": "test_nine[b]", "critic_verdict": "unverified"}
    kept, _ = MP.merge(copy.deepcopy(stored_ab), {"tests": [dict(a_green), patch_b]})
    check_eq("F-3: stored green a + red b, a fragment of green a and a bare patch of b -> the Then row stands",
             (cases(kept), tests_of(kept)), (["TC-009"], ["test_nine[a]", "test_nine[b]"]))
    p_pending = t9("test_nine[p]", status="pending_run")
    q_red = t9("test_nine[q]", status="red")
    patch_q = {"instance_id": "test_nine[q]", "critic_verdict": "unverified"}
    stored_pq = {"tests": [p_pending, q_red]}
    kept, _ = MP.merge(copy.deepcopy(stored_pq), {"tests": [patch_q], "unresolved": [dict(THEN_ROW)]})
    check_eq("F-3: stored pending p + red q, a bare patch of q and the Then row -> p stays (q is red and stands)",
             (tests_of(kept), cases(kept)), (["test_nine[p]", "test_nine[q]"], ["TC-009"]))
    check_eq("F-3: ... and the print names no moved row", MP.moved_out_lines(copy.deepcopy(stored_pq),
             {"tests": [patch_q], "unresolved": [dict(THEN_ROW)]}), [])
    kept, _ = MP.merge({"unresolved": [dict(THEN_ROW)]}, {"tests": [dict(a_green)]})
    check_eq("F-3 control: the only green instance, nothing else stored -> the Then row is taken", cases(kept), [])

    # idempotency and order
    fragment = {"tests": [t9(status="red")], "unresolved": [dict(THEN_ROW)]}
    once, _ = MP.merge({}, fragment)
    twice, _ = MP.merge(copy.deepcopy(once), fragment)
    check_eq("the same fragment twice -> the manifest byte for byte", twice, once)

    def normal(m):
        return {k: sorted(m.get(k) or [], key=lambda r: repr(sorted(r.items()))) for k in ("tests", "unresolved")}
    first, _ = MP.merge(MP.merge({}, {"tests": [t9(status="red")]})[0], {"unresolved": [dict(THEN_ROW)]})
    second, _ = MP.merge(MP.merge({}, {"unresolved": [dict(THEN_ROW)]})[0], {"tests": [t9(status="red")]})
    check_eq("{red tests, Then row} in both orders -> equal manifests (arrays normalised HERE, not in the code)", normal(first), normal(second))
    check_eq("... and both hold the test and the row", (tests_of(first), cases(first)), (["test_nine[a]"], ["TC-009"]))
    # the replay: a journal of the old order folds, and does not raise
    check_eq("replay: two fragments of the old order fold without an unprojected event",
             "unprojected_events" in MP.fold(journal({"unresolved": [dict(THEN_ROW)]}, {"tests": [t9(status="red")]})), False)

    # the print: lines come from the trail, one per moved row, and add up to `moved` of tests[]
    two = {"tests": [t9("test_nine[a]", status="pending_run"), t9("test_nine[b]", status="pending_run")], "unresolved": [THEN_ROW]}
    lines = MP.moved_out_lines({}, two)
    merged, summary = MP.merge({}, two)
    check_eq("print: one line per moved row, the sum is `moved` of tests[] (both rows were only in the fragment: none moved)",
             (len(lines), summary["moved"]), (0, 0))
    stored = {"tests": [t9("test_nine[a]", status="pending_run"), t9("test_nine[b]", status="pending_run")]}
    lines = MP.moved_out_lines(stored, {"unresolved": [THEN_ROW]})
    merged, summary = MP.merge(copy.deepcopy(stored), {"unresolved": [THEN_ROW]})
    check_eq("print: the lines add up to the rows moved out of tests[]", (len(lines), summary["moved"], tests_of(merged)), (2, 2, []))
    check_in("print: a line names the instance, the case and the door", "moved out of tests[]: test_nine[a] (case TC-009 is now wholly "
             "unresolved because the row names no instance_ids/partitions; if it is about particular Thens, name the instances: "
             "instance_ids: [...])", lines[0])
    check_eq("print: nothing moved -> no lines", MP.moved_out_lines({"tests": [t9(status="red")]}, {"unresolved": [THEN_ROW]}), [])
    check_eq("print: a before that cannot merge is no failure", MP.moved_out_lines("x", {"unresolved": [THEN_ROW]}), [])


def ep1_39_critic_approval() -> None:
    """EP1-39 item 7 (F-11 a): `approved` over a stored `unverified` needs a note; a note passes (legality is not judged)."""
    stored = [t9(critic_verdict="unverified", critic_note="no probe")]
    patch = lambda **kw: {"tests": [dict({"instance_id": "test_nine[a]", "critic_verdict": "approved"}, **kw)]}
    check_in("pure: approved over unverified with no note -> refused, naming the row",
             "tests[0] approves over a stored unverified verdict with no critic_note: say what changed (a probe result, a re-read); a "
             "receipt that lacks a probe is a tooling gap, not an approval", MP.critic_approval_problems(patch(), stored)[0])
    for label, kw in (("whitespace note", {"critic_note": "  "}), ("empty note", {"critic_note": ""})):
        check_eq(f"pure: {label} is no note", len(MP.critic_approval_problems(patch(**kw), stored)), 1)
    check_eq("pure: a non-empty note passes (no judgement of it)", MP.critic_approval_problems(patch(critic_note="probe read"), stored), [])
    check_eq("pure: over an approved / absent verdict -> nothing", MP.critic_approval_problems(patch(), [t9(critic_verdict="approved")])
             + MP.critic_approval_problems(patch(), [t9()]) + MP.critic_approval_problems(patch(), []), [])
    check_eq("pure: another row's unverified verdict is not this row's",
             MP.critic_approval_problems(patch(), [t9("test_other[x]", critic_verdict="unverified")]), [])
    check_eq("pure: odd inputs read as nothing", MP.critic_approval_problems({}, None) + MP.critic_approval_problems({"tests": ["x"]}, ["y"]), [])
    with Stand() as stand:
        check_eq("run: the unverified row is stored", stand.put({"tests": [t9(status="green", critic_verdict="unverified", critic_note="no probe")]})[0], 0)
        before = (stand.journal(), stand.tree())
        code, _out, err = stand.put(patch())
        check_eq("run: an `approved` with no note is refused before the commit", (code, (stand.journal(), stand.tree())), (MP.EXIT_BAD_FRAGMENT, before))
        check_in("run: ... and says what to do", "approves over a stored unverified verdict with no critic_note", err)
        check_eq("run: a note passes", stand.put(patch(critic_note="probe result read"))[0], 0)

        # the print through `run`: a pending test is moved out by a row with no slice
        stand.put({"tests": [t9("test_ten[a]", status="pending_run", case="TC-010", covers=["TC-010"])]})
        code, out, _err = stand.put({"unresolved": [{"case": "TC-010", "reason": CONTRADICTS, "thens": [1], "detail": "d"}]})
        check_eq("run: the move commits", code, 0)
        check_in("run: and `run` prints the moved row", "moved out of tests[]: test_ten[a] (case TC-010 is now wholly unresolved", out)


def pc3_provisional_beside_the_other_lists() -> None:
    """t-2181 PC-3: `provisional[]` is merged by `id` beside the other lists and folds like them. A fragment that also carries
    `tests[]`, `unresolved[]` and `then_bindings` leaves them as the merge always left them; the journal replays to the same
    manifest; a retraction naming a row nobody sent is NOT raised on replay (it is named in `unprojected_events`)."""
    prov = {"id": "P-1", "kind": "side_substitute", "what": "a mock of the payments side", "status": "open"}
    together = {"tests": [t9("test_pay[a]", provisional=["P-1"])], "provisional": [prov],
                "unresolved": [{"case": "TC-004", "reason": "pending_implementation", "instance_ids": ["test_pay[b]"]}]}
    merged, _ = MP.merge({}, together)
    check_eq("the lists of one fragment each land in their own key",
             (sorted(merged), [t["instance_id"] for t in merged["tests"]], merged["provisional"][0]["id"]),
             (["provisional", "tests", "unresolved"], ["test_pay[a]"], "P-1"))
    folded = MP.fold(journal(together, {"provisional": [{"id": "P-1", "status": "kept_by_decision"}]},
                             {"retracted_provisional": ["P-1"]}))
    check_eq("the journal replays to one row, retracted, with its first fields",
             [(r["id"], r["kind"], r["status"]) for r in folded["provisional"]], [("P-1", "side_substitute", "retracted")])
    check_eq("and the replay reports nothing unprojected", "unprojected_events" in folded, False)
    bad = MP.fold(journal({"retracted_provisional": ["P-5"]}, together))
    check_eq("a retraction of an id nobody sent is never raised on replay (the door refuses it before the commit) and retracts nothing",
             ("unprojected_events" in bad, [(r["id"], r["status"]) for r in bad["provisional"]]), (False, [("P-1", "open")]))


def fv1_19e_projection_reads_the_currency() -> None:
    """FV1-19e table T2 row p-proj: the coverage projection reads a binding through `contract.binding_currency` - after the
    r2 steps (re-plan, ONLY design_assessment re-sent) the design counts and the code validity does not."""
    import coverage_contract as CC
    ob = lambda d: {"obligation_id": "OB-1", "decision": d, "execution_scope": "current_task"}   # noqa: E731
    plan_of = lambda d: json.dumps({"rows": [{"id": "TS-1", "schema_version": 2, "coverage_obligations": [ob(d)]}]})   # noqa: E731
    judged = {"obligation_id": "OB-1", "design_assessment": "sufficient", "code_validity": "valid"}
    with Stand() as stand:
        _plan_file(stand, text=plan_of("automate"))
        check_eq("p-proj setup: the first write lands", stand.put({"obligation_bindings": [judged]})[0], 0)
        item = CC.coverage_projection(stand.task, {"current_results": []}, stand.manifest())["obligations"][0]
        check_eq("p-proj before the re-plan: both judgments count", (item["design_assessment"], item["code_validity"]),
                 ("sufficient", "valid"))
        _plan_file(stand, text=plan_of("new"))
        check_eq("p-proj re-plan: the design re-send lands",
                 stand.put({"obligation_bindings": [{"obligation_id": "OB-1", "design_assessment": "sufficient"}]})[0], 0)
        item = CC.coverage_projection(stand.task, {"current_results": []}, stand.manifest())["obligations"][0]
        check_eq("p-proj (r2): the design counts, the validity judged on the old text reads unverified",
                 (item["design_assessment"], item["code_validity"]), ("sufficient", "unverified"))


def main() -> None:
    fv1_19e_projection_reads_the_currency()
    pc3_provisional_beside_the_other_lists()
    ep1_39_then_row_keeps_tests()
    ep1_39_critic_approval()
    ep1_38_obligation_hash()
    fv1_19_predicate()
    fv1_19_obligation_stamp()
    fv1_19e_binding_currency()
    tq1_18_base_outcome()
    tq1_7_helpers()
    hf3_2_b_k1_retraction_takes_the_rows()
    hf3_2_b_k4_a_spelling_a_row_still_wears()
    hf3_2_b_k8_aliases_of_a_dropped_row()
    hf3_2_b_k5_send_and_retract()
    hf3_2_b_k7_empties()
    k5a_k1_a_writer_replaces()
    k5a_k1_b_c_d_hand_units()
    k5a_k1_e_two_handed_thens()
    k5a_k1_replay()
    k5a_k1_run_prints()
    k1_retraction()
    k2_k3_refusals()
    k2b_replay()
    k4_two_reasons()
    k4b_old_events_fold()
    k8_slice_replacement()
    k8b_one_constant()
    run_end_to_end()
    finish("test_manifest_put_merge")


if __name__ == "__main__":
    main()

# t-968 — critic: rules debt, phase 2, wave 1 (S7 t-950, S8 t-951, C1 t-959, C2 t-960)

One review for the topic (R13-g). Specs: `docs/tasks/specs/20261117-rules-debt-fix-spec.md` (S7, S8, F-O3, F-O6) and
`docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md` (C1, C2, §0, Lead decisions D-1 (ii), D-3 (a), B-2 (a)).
Brief: `docs/tasks/critic-diff-brief.md` (questions 1-12). Severity words used here: **blocks** (the merge waits), **fix
before merge**, **low** (still fixed in this round, as the Lead asked). Nothing is proposed for the queue. Where a fix
falls outside a node's owns, it says so, and widening the owns is the Lead's call.

## Verdicts

| diff | verdict | blocking | fix before merge | low |
|---|---|---|---|---|
| S7 t-950 `091a0fa5` | fit_with_fixes | 0 | S7-1, S7-2 | — |
| S8 t-951 `25e0764e` | fit_with_fixes | 0 | S8-1, S8-2 | S8-3, S8-4, S8-5 |
| C1 t-959 `74ab9646` | fit_with_fixes | 0 | C1-1, C1-2, C1-3, C1-4, C1-7 | C1-5, C1-6, C1-8 |
| C2 t-960 `753bffec` | fit_with_fixes | 0 | C2-1, C2-2, C2-3, C2-6 | C2-4, C2-5 |

None of the four is not fit. Every finding below has a concrete input or a line plus a failure scenario. The
mechanical layer the Lead attached is consistent with the diffs. I re-ran one item myself (S7, 34/34) and ran three
probes (S8 refusal, C1 K4 control values, pyflakes on the touched files). The details are in the Trail.

---

## S7 — t-950: "no rule" is not "OK"

Fit to spec (q1): `check_witness.main` prints `ADVICE — 1` / `- not checked: no evidence contract for <name>` at exit 0.
`parse` reads it as one advice with no defect (the test row, and I re-ran it). `exit_gate.witness_errors` stashes the advice
under source `"witness"` and `run_advisers` pops it (exit_gate.py:117,159,696). E1-E4 hold. The registry `exempt_reason` was edited.

**S7-1 (fix before merge) — the consumer recognises the advice by re-spelling the producer's text.**
`exit_gate.py:161` checks `str(r).startswith("not checked: no evidence contract")`. The producer has the constant
`NOT_CHECKED_NO_CONTRACT = "not checked: no evidence contract for {name}"` (check_witness.py:280). This breaks the closing
rule of SIBLING_MAP axis 17: no second parser of a detector's text. Failure scenario: someone rewords the constant (for
example "not checked - no evidence contract …"). `parse` still files the advice, but the prefix test is False, so the gate
prints `witness OK (re-run by the exit gate)` again. That is exactly the defect S7 exists for, and no test catches it (S7-2).
Minimal fix: compare with the producer's own constant, `str(r) == CW.NOT_CHECKED_NO_CONTRACT.format(name=art.name)` (import
it the way `artifact_producer.py:79` imports `RULES`). A cleaner variant: one predicate `check_witness.has_contract(name)`
(`name == "code-review.md" or name in RULES`), read by `main` and by `witness_errors`. Then the decision is a data fact and
no text is matched at all.

**S7-2 (fix before merge) — the test docstring promises more than the test checks, and the reader half never runs.**
The docstring at `test_check_witness.py:143-144` says "the exit gate's reader files it as advice and prints the 'not checked'
line, not 'OK'". The row only calls `EG.advice_records`, a one-line mapper. Three things never run: `witness_errors`'
printed line, its `_stash_advice(..., "witness", ...)`, and the new `"witness"` element of the `run_advisers` tuple. Delete
`"witness"` from exit_gate.py:696, or revert line :161 to always print OK, and the test stays green. Minimal fix: call
`witness_errors` in a world that already drives it (`test_exit_gate_unreadable.py` does). Assert two things: stdout carries
`witness not checked: test-plan.md has no evidence contract` and not `witness OK`; `exit_gate._STASH[(agent, task,
"witness")]` holds one record of kind `advice`. If that is not done, the docstring must be cut down to what is checked
(brief q7: an annotation that is not true).

K6 (readers of the literal "witness OK"): verified. A case-insensitive grep over `ai-packages/`, `tools/`, `.claude/agents`
and `.githooks` finds four places. `check_witness.py:329` and `exit_gate.py:165` are the producers' prints for the RULED
path. `driver_dispatch.py:136` is a history comment. `test_check_witness.py` holds the new negative check. Positive control,
same tool and case profile: the pattern `witness ok (re-run` finds `exit_gate.py:165`. `check_delivery.py:716` runs
check_witness only on the manifest, which has a rule, and reads it through `detector_verdict`. No reader depends on the
literal for a no-rule artifact. The old text `OK (no rule …)` still stands in `design/factory-rules-debt.md:62`. That file
belongs to S1b, which is planned, so it is not a finding.

Tests (q5): one row, and `tests-over:` is given with a reason that holds. Duplication (q6): S7-1. Code quality (q7): S7-2.
AR-18 and AR-28 are named and held, except for the second text parse (S7-1). JUDGMENT (q11): none, because presence of a
contract is a data fact. ONE ROAD (q12): none found (no language, project or case branch in the diff).

---

## S8 — t-951: the finding scopes as one data file

Fit (q1): `references/finding-scopes.json` holds the three words. `FINDING_SCOPES` reads it lazily: import does not read the
file (probe: after import `_rows` is `None`), so E2 holds. A missing file gives a refusal that names the path, the expected
shape and the door "restore it from the plugin" (probe output in the Trail), so E1 holds. `_scope_arg` and `_build_parser`
degrade with that door. The dashboard keys on `.urgent`, and no literal `local-urgent` is left. E3 rows already exist
(`test_project_decisions_refs.py:147-169`, `test_project_decisions_change_request.py:165-172`). E5: `--homes` passes.

**S8-1 (fix before merge) — a private JSON read of a package file.** `project_decisions._ScopeTable._load` does
`json.loads(path.read_text(encoding="utf-8"))`. The closing rule of SIBLING_MAP axis 16 says "a new JSON read of a package
file calls `hooklib.read_json`", which also tolerates a BOM. Minimal fix: `raw = hooklib.read_json(path, None)`, and `None`
gives the same refusal, worded "missing or not JSON".

**S8-2 (fix before merge) — K5 (FR-1, P1): an unreadable data file takes the whole dashboard down.** `tab_factory` iterates
`FINDING_SCOPES` (factory_dashboard.py:3647, :3655, :3664). The call site in the `tabs` list (:4054) has no `try`. So a
missing or broken `finding-scopes.json` raises `ValueError` out of the render, and no page is written. The builder states
this in the report ("raises the ValueError refusal at render"). It was the builder's own choice on a point the spec left
open, and it went in the unsafe direction: P1 says code reports, it does not stop. The same widget already has the
safe form for a missing `factory-backlog.md` (:3667-3668, "Unavailable: …"). Minimal fix: in `tab_factory`, wrap the reads
in `try: … except ValueError as exc:`. Draw `w1` as `Unavailable: <esc(str(exc))>`. Let `scope_span` fall back to
`esc(scope)`. The CLI refusal (E1) stays as it is.

**S8-3 (low) — K5: the "no urgent row" grey slice has no label.** With no urgent row, render findings get a grey slice
(:3659-3660) that no legend item explains. The count is in the total, but a reader cannot tell what it is. The scope cell
shows "—", which is an honest unknown (FR-41 holds there). Fix: when that slice is added, add a legend item such as
`unclassified (this render)`. Today the branch cannot be reached in the package, because the data file is pinned with an
urgent row, so this is presentation only.

**S8-4 (low) — the test checks the same junction twice.** The new lines `test_conductor_doors.py:125-134` pin the three
words in order. `test_project_decisions_refs.py:121` already pins that (`tuple(PD.FINDING_SCOPES) == WORDS`). The new
template-words check overlaps `:131-136`, which checks each word plus the lead of its meaning in the template. TESTING.md:
one test per behaviour. Fix: keep the junction `PD.FINDING_SCOPES == data` and the "template line holds the whole meaning"
check in one place. Delete the weaker loop at refs:131-136 and the new word-order pin. refs is outside S8's owns, so the
Lead widens the owns by one path.

**S8-5 (low) — the FR walk answer for B is not accurate.** The report says "B: text to a person unchanged". The template
line `factory-backlog.md:15`, which people and roles read, was reworded, and the legend changed colour for
`local-calibration`. Fix the line: "B: one template line reworded with the same meaning; no question text". The spec §7
already queues it for live-runs.

Duplication (q6): S8-1 and S8-4. Code quality (q7): S8-2, the unsafe direction. AR-1, AR-13 and AR-3 are named. AR-13 holds:
`FINDING_SCOPES` is the one reader, and the dashboard imports it (factory_dashboard.py:27). JUDGMENT: none. ONE ROAD: none
found, because F-O3 (a) is the owner's word, quoted from the spec's closing section «The owner's word 17.11.2026 (second
portion)».

---

## C1 — t-959: bug file homes, writer <-> readers

Fit (q1): items 1-6 are present. D-1 (ii) works: `resolve_bug_file` tries the task root first and then the state directory,
both at `process_bug_proposal` and in `record_result` for kind bug. Slices are regenerated with no K10 raise. The texts are
aligned. E1, E2, E4, E6 and E8 hold.

**K4 (E5), checked with control values, not by reading.** My probe (Trail, `c1probe.py`) builds a real layout:
`<proj>/qa-factory/artifacts/T-1/{work/proposals,proposals}`, plus a custom `qa-artifacts/T-2/work/proposals`. Results:
`bugs/BUG-5.md`, which exists only in the state directory, resolves to `qa-factory/bugs/BUG-5.md` from both proposal folders,
so older proposals still resolve. `bugs/BUG-1.md` with both files present resolves to the story's own file (E6). The D-1 (i)
form `artifacts/T-1/bugs/BUG-1.md` resolves through the fallback. `bugs/NOPE.md` falls through to a state-directory path that
does not exist, so the T6 text is unchanged. A custom artifact root resolves to the story's file. **E5 holds.**

**C1-1 (fix before merge) — E3's invariant is broken, and what the cap cuts is not reported.** `judge_results.py:344-353`
applies one cap across all drafts (`pairs_used`, `MAX_BUG_PAIRS = 200`, :54). The outer loop runs over drafts and the inner
loop over the item-1 order. Concrete input: 3 drafts, this story has `BUG-1`, other stories have 199 bugs. Draft 1 uses all
200 pairs (its own BUG-1 and then 199 others). Drafts 2 and 3 are never compared with their own story's `BUG-1`, while draft
1's pairs with other stories' bugs are kept. That breaks the card's E3 invariant ("it never drops the current story's own
bugs before others'"). The cut is not written in `judge-bugs.json` either (FR-59). Before C1 the input was only the project
home. D-3 (a) makes the input grow with every story, so this becomes likely. Minimal fix: have `filed_bug_listing` return
the home label with each path (or the paths grouped by tier). Build the pairs tier by tier: every draft × the story's bugs,
then every draft × the project home, then every draft × other stories. Write `report["pairs_dropped"] = <n>` when the cap
cuts. To test it, take the pair order out into a pure helper (`_bug_pairs(drafts, tiers, cap)`) and add one table row:
expected from E3, not from the code.

**C1-2 (fix before merge) — K1: keeping `_project_bugs_dir` leaves a second home for the fact.**
`judge_results._project_bugs_dir` (:273-279) still derives `<project>/qa-factory/bugs` next to `bug_records._project_home`
(:131-138), and the two disagree. For a story under no project, `_project_bugs_dir` returns "two levels up" + `/bugs`, while
`_project_home` returns `None`. Its name is now untrue: the only product caller is `_state_relative` (:283-290), which uses
`.parent` to get the state directory. This breaks AR-13/AR-15 (one fact, one reader) and axis 8's one project-marker walk.
Minimal fix: delete `_project_bugs_dir`. Have `_state_relative` take the state directory from
`runtime_paths.nearest_project(task_root)`, and return the absolute posix path when that is `None`. In
`tests/test_task_root_project_door.py`, drop the SITES row `judge_results._project_bugs_dir:275` (:35) and the bare-root
check (:67): that derivation no longer exists, and the walk stays covered by the other rows and by
`test_bug_records.py:1415-1417`. The test file is outside C1's owns, so the Lead adds it to the owns.

**C1-3 (fix before merge) — K2: any sibling folder is taken as a story, without the module's own story rule.**
`filed_bug_listing` (bug_records.py:170-177) lists every directory next to the task root. The module already has the
story rule, `_story_exists` → `hooklib.is_story_with_pipeline` (bug_records.py:1461-1465; SIBLING_MAP axis 8, "the ONE key
-> story-folder rule"). AR-4 holds: `task.parent` is the artifact root in every layout `artifacts_dir` builds, and a custom
`artifact_root` is followed. What breaks is the story rule (AR-13 for the fact "is a story"). **The layout that fails:**
`artifact_root: "."` is legal, because `hooklib.artifact_root` (hooklib.py:803-828) accepts any non-empty path. There the
siblings are every top-level folder of the project. A product file `docs/bugs/BUG-12.md` would then go to the judge as a
filed bug. `qa-factory/` itself also becomes a "story"; dedup absorbs that one. The same happens with any artifact root that
also holds folders that are not stories. Minimal fix: add `and _story_exists(task.parent, p.name)` to the sibling filter.
Add one check to the existing row: a non-story folder with `bugs/BUG-9.md` is not listed.

**C1-4 (fix before merge) — K3: the unknown is written, but the text a role or person sees stays silent.**
`unreadable` has one caller, `run_bugs`, which writes `report["unreadable_bug_homes"]` to the JSON file only (:372-373).
Two texts never mention it. `render_bugs` (:379-385) is the line printed at the reporter's `start`, and it still says "N
possible duplicate(s) flagged". The reporter's brief (`story_step.py:223-225`) does not name the key either. So FR-59/AR-28
holds in the file but not in the text anyone reads (AR-22: a field is produced, and its reader is unnamed). Minimal fix:
`render_bugs` adds `; <n> bug folder(s) could not be listed (unreadable_bug_homes in work/judge-bugs.json)` when the key is
present. Use the same clause for C1-1's `pairs_dropped`.

**C1-5 (low) — the T6b world does not use the factory's own layout.** In `test_external_writes_bug_refusals.py:127-141`
the Rig's proposal sits at `<project>/proposals/` (Rig :45), so the "task root" is the project root itself. The primary
location `<task root>/work/proposals/` (external_writes.py:6; the `folder.parent.name == "work"` branch of
`resolve_bug_file`) never runs. A defect that always took `folder.parent` would pass. My K4 probe shows the code is right
today. Fix: one check `EW.resolve_bug_file(<root>/qa-factory/artifacts/T/work/proposals/bug-1.json, "bugs/BUG-1.md") ==
<T>/bugs/BUG-1.md`.

**C1-6 (low; the card's choice, so the Lead decides) — "file" uses a different frame from `bug_file`.** A duplicate entry's
`"file"` is relative to the state directory (`_state_relative`, as the card prescribes). After this diff, `common-rules.md`
says `bug_file` is relative to the task root. So the string `bugs/BUG-1.md` means the PROJECT-home file in
`judge-bugs.json` and THIS story's file in a proposal. A reporter that copies a duplicate's `"file"` into a proposal's
`bug_file` would point at the wrong file. Fix: make `"file"` relative to the project root, with the `qa-factory/` prefix
(`qa-factory/bugs/BUG-1.md`, `qa-factory/artifacts/T/bugs/BUG-1.md`), following the `journal_path` precedent in the same
frame table. Then it cannot be read in the bug_file frame. This amends the card.

**C1-7 (fix before merge) — class completeness and an AR-13 claim that is too broad.** The commit says "AR-13 -- the bug
folders are read only through bug_records". That is false for three readers, and none of them is in the card's siblings or
in D-2's carrier list (cards spec :248-252):
- `factory_dashboard.load_bugs` (:1222-1255) walks the artifact root with its own `iterdir`. That is a second implementation
  of "other stories' bug folders", with the same no-story-rule gap as C1-3.
- `exit_gate.bug_audit_errors` (:1395) and `audit_factory.a3_a4_artifacts` (:457) list only `state_dir()/bugs`. A bug the
  reporter writes under the task root, which is the home after F-O6 (a), is never checked by `check_bug`. A case's
  `red_lock: BUG-n` that names a task-root bug gets a false "file bugs/BUG-n.md does not exist" (:465-466).
Minimal fix this round: narrow the architecture line to "the duplicate check's bug folders are read through bug_records".
Name the three readers in the axis 38 text (the Lead's commit) and in the D-2 node's scout question and owns, which the Lead
already decided to open. `factory_dashboard.py` belongs to S8's owns in this wave, which is why it is not changed here.

**C1-8 (low) — the FR walk answer for B.** "B: no text shown to a person added". The test report's Notation line
(`templates/test-report.md:35`), which a person reads, changed. Fix the line: "B: one notation phrase changed; no question
text".

Tests (q5): `tests-over:` is given, and the reason holds for edge rows. The new rows' expected values are quoted from
F-O6 (a) and D-1/D-3, not taken from the code. `test_bug_records.py` is slow and its new function ran alone, which is
legitimate. Ratchets (q9): `role-load.json` K10 was not raised; the builder trimmed bytes instead. No census row was added.
JUDGMENT: none; the duplicate decision stays the advisory judge's. ONE ROAD: none found. The `bug` and `case` kinds are
resolved in different frames, but that is a frame declared per field, not a language, project or case exception.

---

## C2 — t-960: the four command-door families as one table

Fit (q1): `DOOR_FAMILIES` has the four rows, named by family. Each walk row is found by block text (E2). A missing family
fails by name (E3). E4 counts events. E5 holds. E6: `main` before the old :93 is unchanged. B-2 (a): `cart-1` is used for
semantic_reopen, and BASE is named for the rest.

**C2-1 (fix before merge) — unused import, so a new lint-ratchet finding.** pyflakes:
`test_controller_doors.py:30:1: 'harness.check_not_in' imported but unused`. `forge-check`'s `lint_ratchet --check` turns red
on a new identity. Fix: drop `check_not_in`.

**C2-2 (fix before merge) — the gate-decision row does not run the door the walk names.** The walk's way-through cell for
both rows (controller-blocks.md:65 and :128) is `gate-decision`. That operation is `_gate_decision_call` →
`_gate_decision_run`, "THE ONE road of a gate decision" (controller.py:9622-9650): it pins the project, lays the answers
over the plan, writes the question register, and does the manifest put of `accept as blocked`. The row instead calls
`controller.build_gate_decision(...)` and then `apply("decision", …)`, which is only part of that road. The commit's "AR-9
-- … proven by executing the door" therefore says more than the test does for this family. The checkpoint row (`--operation
checkpoint` has its own branch at :10040) is a milder case of the same. `recover` is exact: `c.recover()` is the body of
`--operation recover`, :10024-10025. Minimal fix: run the gate-decision door through
`harness.run_controller_inprocess([... "--operation", "gate-decision", "--gate", "A", "--words-file", <file>], root)`
(DC1-27, the one in-process controller run of the tests). If BASE cannot carry the door, that is the card's E1: the row
comes back as a question, it is not weakened. For the other rows, either use the CLI too or have the docstring say "the
operation's body".

**C2-3 (fix before merge) — `pinned` duplicates an existing helper.** `pinned` (:62-74) re-implements
`hooklib.selftest_root_restored()` + `hooklib.pin_project_root()` (hooklib.py:130-160, "one method for every selftest that
builds a throwaway project"). `scenario_walk._pinned` (:126-134) already uses exactly that pair. Fix:
`with hooklib.selftest_root_restored(): hooklib.pin_project_root(project); yield`.

**C2-4 (low) — a hand-written project marker in the new helper.** `synthetic_world` writes `config.json` as `"{}"` (:85).
The text was carried over from the old block, but it now sits in a new helper. `harness.mark_project` is "THE one place a
test fixture gets its marker" (SIBLING_MAP axis 8, row "fixture marker writer"; census F6-17). Fix: `harness.mark_project(root)`.
If the template keys change the BASE world's behaviour, the builder reports that instead.

**C2-5 (low) — `row_checkpoint` ignores `needle`.** It checks the literal `"checkpoint active work"` (:144), while the
other three rows use the block text from the walk. E2 asks for the walk's text. Fix: `check_in(..., needle, str(refusal))`.

**C2-6 (fix this round, outside C2's owns) — K7: the refusal is a dead block in controller.py, and the walk is correct.**
Evidence, traced: `deployment_inputs` (controller.py:2252-2267) reads `state = self.state()` once and calls
`self._validate_gate_a_content_current(state)` (:2261). That function (:4747-4753) calls `_raise_all` with "current Gate A
decision required" whenever `_current_gate_a(state)` is `None`. `_raise_all` (:6154-6167) raises for any non-empty list.
`_current_gate_a` (:4741-4745) is exactly "gate A, status approved, `source_revision == state.source_revision`". The check at
:2262-2264 is that same predicate over the same `state` object, and nothing writes in between. So whenever execution gets
past :2261, `any(...)` is True, and `raise StateConflict("approved Gate A required before deployment")` (:2265) can never
fire. The walk row `controller-blocks.md:55` is generated from the source (`tools/controller-blocks-gen.py`), so the walk
reports the source correctly, and the source has a dead block. **Class:** a shadowed refusal, meaning a block whose
predicate an earlier check already implies, so no caller can ever see it. It is a dead branch (q7). The builder's
reachability measurement was correct, and the cause is in the product. I checked the neighbours: the other two callers of
`_validate_gate_a_content_current` (:2242 baseline, :5584 scope) are not followed by a re-check of the same predicate.
Minimal fix: delete controller.py:2262-2265 and regenerate `design/controller-blocks.md`, which drops row 55; the door stays
on row 128. controller.py is a HOT file and a non-goal of C2, so the Lead gives this its own owns.

Tests (q5): `tests-over: F-O5 (b), the owner's word` holds; the owner chose the option that adds test lines. The volume is
in one file and no new test file was added. Expected values come from each walk row's way-through cell. JUDGMENT: none.
ONE ROAD: none found. Ratchets: none touched.

---

## Seams (q3)

S8 owns `factory_dashboard.py` in this wave. C1-7's dashboard reader is therefore named, not edited. C2-6 needs
`controller.py` (HOT). C1-2 needs `tests/test_task_root_project_door.py`. S8-4 needs `tests/test_project_decisions_refs.py`.
All four are owns the Lead has to add. No two diffs touch the same file. S7's `exit_gate.py` and C1's readers do not
overlap: `bug_audit_errors` is only named.

## Class-wide completeness (K8, SIBLING_MAP)

- **S7:** axis 17 (detector verdict shape): S7-1. Axis 5 (stage twins): not applicable, because the change is a detector
  wording with no twin. Axis 18: the census test was run by the builder; no row changed.
- **S8:** axis 16 (one JSON reader): S8-1. Axis 18: no ratchet. AR-1 change check, a grep for a tuple or dict of the three
  words in `scripts/`: the builder's claim holds. My grep for `FINDING_SCOPES|scope_refusal` lists only project_decisions
  and the dashboard.
- **C1:** axis 8 (where the story is on disk): C1-2 (the project walk) and C1-3 (the story rule). The new axis 38 (the Lead's
  commit): C1-7 names three readers that the axis text and D-2 must take. Axis 18: role-load not raised.
- **C2:** axis 8 (the fixture marker writer): C2-4. The shadowed-refusal class: one instance (C2-6), and the neighbours were
  walked as described above.

## Spot-checks (negative claims, each with a positive control)

- S7 "no reader depends on `witness OK`": confirmed (K6 above). The control `witness ok (re-run` found exit_gate.py:165.
- S8 "lazy, never at import": confirmed by the probe (`_rows` is `None` after import).
- S8 "missing file → refusal naming file and door": confirmed by the probe.
- C1 "every older proposal resolves (E5)": confirmed by control values (K4).
- C1 "no keep row drives run_bugs": true. `test_judge_results.py` is quarantined (cards spec §0.3), so C1-1's pure helper
  is the way to test it.
- C2 "approved Gate A required … unreachable in both worlds": confirmed by tracing; it is unreachable in every world (C2-6).
- C2 "no red rows": I did not re-run; the Lead's acceptance run holds 31/31. pyflakes found C2-1, which the run does not show.

## Trail

Read: `docs/tasks/critic-diff-brief.md` (whole); the fix spec S7, S8, §6 forks, owner-word sections (:314-378, :500-654);
the cards spec §0-§2 C1/C2, §6, Lead decisions (:1-230, :706-834); the four `git show HEAD` diffs and the four reports;
`exit_gate.py` :112-170, :400-470, :605-760, :1375-1440, :1880-1925; `detector_verdict.py` :95-107 (Record is a str);
`hooklib.py` :130-160, :246, :282-307, :370-412, :803-900; `bug_records.py` :120-190, :1450-1480, :1570-1600;
`judge_results.py` :270-390; `external_writes.py` :160-175, :626-680; `story_step.py` :218-250;
`factory_dashboard.py` :27-32, :478-490, :1222-1255, :3619-3700, :3757-3830, :4048-4058; `audit_factory.py` :450-470;
`project_decisions.py` :36-115, :355-375, :915-1000; `controller.py` :2240-2275, :3441-3470, :4740-4800, :6154-6201,
:9622-9662, :10020-10040; `controller-blocks.md` rows 55, 65, 128; `harness.py` :255-400; `scenario_walk.py` :80-200;
`tests/test_task_root_project_door.py` (whole); `test_project_decisions_refs.py` :90-170; `test_external_writes_bug_refusals.py`
Rig :37-70; `docs/SIBLING_MAP.md` headings and axes 8, 16, 17; `tools/critic_verdict.schema.json`.

Commands (verbatim tails):
- `python -B <wt-S7>/scripts/tests/test_check_witness.py` → `=== check witness: 34/34 ok ===`
- S8 probe `s8probe.py` → `import ok, rows loaded: None` / `urgent: ('local-urgent',) len 3` / `REFUSAL: the finding scopes
  cannot be read (FileNotFoundError): …\references\nope.json must be a JSON object of {word: {"meaning": text, "urgent":
  true|false}} with at least one word; restore it from the plugin (update or reinstall qa-factory) - nothing was recorded`
  (the probe's own third call was a miscall, `main()` takes no argv, and is not used as evidence)
- C1 probe `c1probe.py` → `…/T-1/work/proposals/bug-1.json bugs/BUG-1.md -> qa-factory/artifacts/T-1/bugs/BUG-1.md
  exists=True`; `… bugs/BUG-5.md -> qa-factory/bugs/BUG-5.md exists=True`; `… artifacts/T-1/bugs/BUG-1.md ->
  qa-factory/artifacts/T-1/bugs/BUG-1.md exists=True`; `… bugs/NOPE.md -> qa-factory/bugs/NOPE.md exists=False`; the same
  four for `/proposals/`; `qa-artifacts/T-2/work/proposals/bug-1.json bugs/BUG-3.md -> qa-artifacts/T-2/bugs/BUG-3.md
  exists=True`
- `python -m pyflakes` over the touched files → `test_controller_doors.py:30:1: 'harness.check_not_in' imported but unused`.
  The three `factory_dashboard.py:2148` lines already exist on main and are not in this diff. Nothing else.
- Greps: `witness OK` (-i) and `no rule for|OK (no rule|contract undefined` over the package/tools; `check_witness`
  callers; `FINDING_SCOPES|scope_refusal`; `SCOPE_SHOWN` in tests; `judge-bugs|unreadable_bug_homes|filed_bug_listing`;
  readers of `qa-factory/bugs|state_dir()/"bugs"`; `_project_bugs_dir|_project_home`; `is_story_folder|is_story_with_pipeline`;
  `_validate_gate_a_content_current(` callers; `_PROJECT_ROOT_CACHE` in harness.

Final decision on acceptance rests with the Lead; these verdicts are input to that acceptance (rule 6).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "S7: axis 17 second text parse of check_witness advice (S7-1). S8: axis 16 private JSON read (S8-1). C1: axis 8 project walk duplicated by _project_bugs_dir (C1-2) and story predicate bypassed in filed_bug_listing (C1-3); axis 38 readers not in card or D-2: factory_dashboard.load_bugs, exit_gate.bug_audit_errors, audit_factory.a3_a4_artifacts (C1-7). C2: axis 8 fixture marker writer (C2-4); shadowed-refusal class one instance controller.py:2262-2265, neighbours at :2242 and :5584 walked, clean (C2-6).",
  "fixes": [
    "S7-1 exit_gate.py:161 compare with check_witness.NOT_CHECKED_NO_CONTRACT (or one has_contract predicate) instead of a re-spelled prefix",
    "S7-2 test_check_witness.py:142-165 drive witness_errors: stdout 'witness not checked' and not 'witness OK', and the witness stash holds one advice; or cut the docstring",
    "S8-1 project_decisions._ScopeTable._load read through hooklib.read_json",
    "S8-2 factory_dashboard.tab_factory: an unreadable finding-scopes.json gives an Unavailable card with the refusal, not a crashed page",
    "S8-3 legend item for the grey no-urgent-row slice",
    "S8-4 one junction test: drop refs:131-136 and the new word-order pin, keep PD==data and the whole-meaning template check",
    "S8-5 correct the FR walk line B in the report",
    "C1-1 judge_results.run_bugs: pairs tier by tier across drafts, report pairs_dropped, pure helper plus one row",
    "C1-2 delete judge_results._project_bugs_dir; _state_relative via runtime_paths.nearest_project; drop test_task_root_project_door rows :35 and :67",
    "C1-3 bug_records.filed_bug_listing: filter siblings by _story_exists; add a non-story folder check to the row",
    "C1-4 render_bugs names unreadable_bug_homes and pairs_dropped",
    "C1-5 T6b check in the real layout work/proposals",
    "C1-6 duplicate entry file relative to the project root with the qa-factory prefix (card amendment, Lead's call)",
    "C1-7 narrow the AR-13 line; name load_bugs, bug_audit_errors, a3_a4_artifacts in axis 38 and the D-2 node",
    "C1-8 correct the FR walk line B in the report",
    "C2-1 drop unused import check_not_in",
    "C2-2 gate-decision row through run_controller_inprocess --operation gate-decision, or the docstring says the operation body",
    "C2-3 pinned uses hooklib.selftest_root_restored plus pin_project_root",
    "C2-4 synthetic_world uses harness.mark_project",
    "C2-5 row_checkpoint checks needle",
    "C2-6 delete dead raise controller.py:2262-2265 and regenerate controller-blocks.md (row 55)"
  ],
  "trail": {
    "read": [
      "docs/tasks/critic-diff-brief.md",
      "docs/tasks/specs/20261117-rules-debt-fix-spec.md",
      "docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md",
      "four worktree HEAD diffs and handoff reports t-950, t-951, t-959, t-960",
      "ai-packages/qa-factory/scripts/exit_gate.py",
      "ai-packages/qa-factory/scripts/check_witness.py",
      "ai-packages/qa-factory/scripts/detector_verdict.py",
      "ai-packages/qa-factory/scripts/hooklib.py",
      "ai-packages/qa-factory/scripts/project_decisions.py",
      "ai-packages/qa-factory/scripts/factory_dashboard.py",
      "ai-packages/qa-factory/scripts/bug_records.py",
      "ai-packages/qa-factory/scripts/judge_results.py",
      "ai-packages/qa-factory/scripts/external_writes.py",
      "ai-packages/qa-factory/scripts/audit_factory.py",
      "ai-packages/qa-factory/scripts/story_step.py",
      "ai-packages/qa-factory/scripts/controller.py",
      "ai-packages/qa-factory/design/controller-blocks.md",
      "ai-packages/qa-factory/scripts/tests/harness.py",
      "ai-packages/qa-factory/scripts/tests/scenario_walk.py",
      "ai-packages/qa-factory/scripts/tests/test_task_root_project_door.py",
      "ai-packages/qa-factory/scripts/tests/test_project_decisions_refs.py",
      "ai-packages/qa-factory/scripts/tests/test_external_writes_bug_refusals.py",
      "docs/SIBLING_MAP.md",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "python -B <wt-S7>/ai-packages/qa-factory/scripts/tests/test_check_witness.py", "result": "=== check witness: 34/34 ok ==="},
      {"command": "python -B scratchpad/s8probe.py <wt-S8>/scripts", "result": "lazy (rows None after import); refusal names references/nope.json, the shape and the restore door"},
      {"command": "python -B scratchpad/c1probe.py <wt-C1>/scripts", "result": "state-dir-only bug resolves from work/proposals and proposals; task root wins on a same name; NOPE falls through to a missing state-dir path; custom artifact root resolves"},
      {"command": "python -m pyflakes on touched files of the four worktrees", "result": "test_controller_doors.py:30:1 'harness.check_not_in' imported but unused; factory_dashboard.py:2148 lines pre-existing"}
    ]
  }
}
```

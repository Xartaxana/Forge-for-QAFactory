# t-152 — critic, batch onboarding-forge/1: Part A re-review of the hooklib fix round (b1875b4), Part B first diff gate of stream "doctor" (9a97901)

Reviewer: critic (Opus), 12.11.2026. One pass, two topics (R13-g). The verdicts are inputs to acceptance. The decision stays
with the coordinator of the proper tier.

**PART A verdict: ACCEPT WITH FIXES. 1 blocking (A0: B1's second half is not closed; `tools/test_quarantine.py check` reports 5 violations). B2, B3, F4, F6, F8 and F9 are closed. A1-A3 are queue and node actions.**
**PART B verdict: ACCEPT WITH FIXES (NEEDS WORK). 3 blocking (D1-D3), 4 more fixes (D4-D7).**

---

## PART A — hooklib fix round (b1875b4)

### Closure of the t-141 findings

| finding | closed? | evidence |
|---|---|---|
| B1 | **half** (A0) | The edits to both quarantined files are reverted (net branch diff on both files: empty), and the commit carries two `quarantine-edit:` lines, but in the wrong form (A0). The cases now live in `test_cost_capture_settled.py`, which is a `keep` row (layer `detector`, `named_by docs/SIBLING_MAP.md:339`, covers cost_capture.py, factory_dashboard.py and hooklib.py). I checked this by reading `test-layers.json`. There is no source pin. Re-run: 159/159 ok. The tree-diff cases run subprocesses and compare trees. `tools/test_quarantine.py check` result: see Trail. |
| B2 + F9 | yes | `activity_capture.is_factory_activity` (dict entry, `isinstance(type, str)`, member of REAL_FACTORY_TYPES) is the only reader at all four sites: hooklib:2212, cost_capture:1942/2234, factory_dashboard:1973, metrics_projection:460. `_has_factory_type` is gone. Both "identical rule" docstrings are corrected, and so are the changelog and the AR-1 line. The test feeds unhashable types (`[]`, `{}`, `["story"]`, `{"story":1}`) to all five readers and expects False from each. My grep found no other `'doctor','onboarding','story'`-style "is factory" predicate, with one sibling outside the question (A1). |
| B3 | yes | `READER_STAMP = "capture-0.10.8"`. The new K2 row pins that a `capture-0.10.7` file classifies as `logic` (stale), with a current-stamp control. The changelog states the recapture price. |
| F4 | yes | `cost_capture.main`: `if not _carries_project(project_root(event)): return` sits after `read_event` and before `_choose_subagent_transcript`, `_mark_started`, the debounce `stat` and `_capture_with_wait`. So nothing under `qa-factory/` is created, and the exit is 0. `project_root` is cached per process and is first called here with the event, so the later `state_dir(event)` reads the same root. The `--recapture/--all-stale` CLI branch runs before the check and is unaffected. Pinned: hook plain and `--debounced` on a bare root give exit 0, empty stderr and an identical tree. Control: a project root still captures `s1.json`. |
| F6 | yes | `run_suite.refresh_dashboard` goes through `dashboard_refresh.refresh_project(project_root())`. On a root without config.json that returns `not_configured` before any write, so `require_project_at`'s SystemExit is never reached. `refresh_project` re-raises a non-SystemExit error after writing `stale`, and `except Exception` catches it. Pinned: the B-suite subprocess on a bare cwd prints `returned`, exit 0, identical tree. Side effects of the chokepoint: stdout is now redirected, renders coalesce by input hash, and the writer lock applies. Those are the chokepoint's declared behaviour (AR-15), not a regression. |
| F8 | yes | `cost_capture.py:1940` and `:2232` now say "a factory activity type". The mangled test line left with the B1 revert. |

New defects introduced by the fix: none found. I traced `is_factory_activity(items or ())` for the inputs `None`, `[]`, `{}.values()`, junk entries and non-str types: all give False and nothing raises. The import chain `factory_dashboard`/`metrics_projection` -> `activity_capture` -> `event_store, hooklib, session_identity` forms no cycle; the test imports D and MP at module level and passed.

### Fixes (Part A)

- **A0 (blocks merge; t-141 B1 consequence 2 not closed): `tools/test_quarantine.py check` is still red, now with 5 violations instead of 3.** Re-run: `python -B tools/test_quarantine.py check --root <of-hooklib>` printed b8989353 twice, f99b9f37 once and b1875b4b twice, then "quarantine check: 5 violation(s)", rc=1. There are two causes, both traced in `tools/test_quarantine.py`:
  - (1) `check_history` judges every commit on its own (`:1689-1693`). The two original commits keep their violation unless a LATER commit carries `quarantine-accept: <sha> -- <reason>` (`:1520`, `:1729`). b1875b4 carries no accept line.
  - (2) b1875b4's own door lines name the full path (`quarantine-edit: ai-packages/qa-factory/scripts/tests/test_cost_capture_nonfactory_summary.py -- ...`). The check compares the captured token with the bare quarantine key (`n in _DOORS["edit"].findall(msg)`, where `n` is `test_cost_capture_nonfactory_summary.py`), so the full path never matches, and the fix commit flags itself.
  - Fix: one follow-up commit with `quarantine-accept: b898935 -- <reason>`, `quarantine-accept: f99b9f3 -- <reason>` and `quarantine-accept: b1875b4 -- <reason>` (reason: node tests moved out, net change zero). The alternative is squashing the branch to one commit with no net touch of either file. Witness: the same check printing 0 violations.
  - Defect class for the record: the builder's report says B1 was closed but attached no run of the checker that B1 named. Under rule 7 that claim had no witness.

- **A1 (class completeness, CD1-11 closed set): `scripts/recover_codex_usage.py:32`.** The code is `if kind not in {'doctor','onboarding','story'} ... raise ValueError('Unsupported activity boundary')`. Recovery of a Codex session's boundaries therefore refuses `collect` and `environment-maintenance` boundaries, and their spend stays `unclassified`. That contradicts the owner's word on CD1-11 ("collect and environment-maintenance now count"). The question here differs slightly ("which boundary types can be recovered", not "is this factory work"), but it is the same closed set held as a third literal copy (AR-1). My t-141 grep used a double-quoted pattern and missed this single-quoted set. That is my own miss, disclosed here. Fix now (one line: `kind not in REAL_FACTORY_TYPES`; the regex on the next line already takes any `--type`), or queue with a node id. The file is outside these owns.
- **A2 (t-141 F5, second half): the `docs/SIBLING_MAP.md` axis 10 row is still stale.** The worktree's row :256 is unchanged. It still says OH3-37 is queued and does not record that the dashboard and the cost_capture hook are now done. Update it in the same move that opens the F5 node.
- **A3 (F5 / F7 node proposals): not judgeable as nodes. Only one-line titles reached this review.** The only carrier I found is the narrative snapshot `docs/tasks/compact-snapshots/2026-11-12-1932-narrative.md:27`, which says "узлы F5 (install_smoke --report на голом корне) и F7 (один текст отказа not_a_project) — завести в невзятой пачке onboarding-forge". As titles they are not well-formed nodes under PROJECT.md «Командная работа» p. 11 (file, function, behaviour, test, chosen direction). What each node must carry:
  - **F5:** owns `scripts/install_smoke.py` (`main` ~:573-586, `run_report` ~:518-560) and its test row. The direction must be chosen, and **refusal is the wrong direction**: the doctor's step 1 runs the smoke before onboarding, so an exit-3 refusal would turn every pre-onboarding doctor run into verdict row 1 ("fix the install"), which violates FR-5. Dropping `--report` is also out (t-146 F5-B: loses the reuse window and the receipt that survives a lost shell handle). The node should pick a write location for a root without config (for example the host-local spool that activity boundaries already use before config.json exists) and state how the doctor's step 1 finds the report (the path the script prints). It needs a test row: bare root gives exit 0, identical tree, report readable at the printed path, `--reuse-within` still reuses. It must also carry the axis 10 row and the queue order against the doctor stream and OF1-4, because step 1's text in SKILL.md may change.
  - **F7:** one builder in hooklib (for example `not_a_project_text(root, given, extra_door="")`) that carries host_probe's ancestor hint ("Re-run with --root {above}"). `require_project_at` prints it, `host_probe._not_a_project` returns it, and the dashboard passes the `--read-only --out <file outside the root>` door. `dashboard_refresh.refresh_project:25` switches to `_carries_project`. The docstring "The ONE refusal every writer ... uses (AR-15)" becomes true or is reworded. The node must name the text pins to keep: `test_story_root_class.py:602` "refusing to create one", plus the host_probe pins in `test_host_probe_shapes.py`, which is quarantined, so the node must say how those pins are handled. It needs a table test: bare root, ancestor carries the marker, extra door. FR-6 applies because the text is person-facing.

### Standing lines (Part A)
- DUPLICATION AND CONSISTENCY: the four copies of the predicate are now one (B2 closed). Remaining items: A1 (a third literal copy of the set, in recovery) and F7 (two refusal builders, queued). Grepped: `['"]doctor['"], ?['"]onboarding['"]|['"]onboarding['"], ?['"]story['"]|REAL_FACTORY_TYPES|is_factory_activity|_has_factory_type` over `scripts/*.py` excluding tests. The positive control is the 4 known readers, which it found.
- CODE QUALITY: no new function over 60 lines or deeper than 3 levels. The docstrings now tell the truth, except `require_project_at`'s "ONE refusal", which waits on F7. The test helper `one_predicate_for_factory_activity` uses an `entry_type = next(... repr(j) == kind ...)` lookup that is clumsy but correct (traced for the non-str keys None, 5 and ()).
- ONE ROAD: run_suite now uses the one refresh chokepoint, which removes a second road. No language, project or case exclusion.

---

## PART B — stream "doctor" (9a97901; OH3-6, OH3-12, OH3-7)

### Q1. Items and binding fixes applied as written

| item / fix | applied? | note |
|---|---|---|
| 1 `Write` in allowed-tools | yes | the scope question is Q4 / D5 |
| 2 step 1b + repair.md guard section | text yes, **pointer broken** | D1 |
| 3 printing bullet 1 (no factory script) | text yes, **the same-artifact sweep missed rows** | D2 |
| 4 step 3 gate | yes, as the spec wrote it | D6 (positional invariant) |
| 5 FACTORY NOTES + READINESS | yes | contradicts an existing bullet: D3 |
| 6 writes sentence, never-list, README | yes | the sample-ticket question is lost: D4 |
| 7 cuts (a)-(d) | yes; 18,995 -> 18,817 B (my control: 18817/18817) | cut (c) is the cause of D4 |
| 8 evals | yes: ids 1-15 unique; id 12/13 names unchanged; 14/15 present | |
| 9 changelog fragment | yes; `--lang` PASS | |
| t-146 fix 1 (bytes) | yes | headroom after: 183 B |
| fix 3 (artifacts bullet, README:61) | yes | |
| fix 4 (plain-words notes; mixed precedence) | yes ("A `remedy.owner: user` row keeps READINESS at 'your help is needed'") | |
| fix 5 (no post-write `--check`) | yes, in SKILL.md and eval 14 | |
| fix 6 (refused Write -> unverified) | yes (repair.md: "A refusal of your own throwaway write is that evidence too") | |
| fix 8 (spec wording) | not in the diff (spec-only) | D7 |
| fix 9 (repair.md:42-45, SKILL.md never-list) | yes | |
| Codex paragraph move (coordinator decision) | moved verbatim | broke item 2's pointer (D1); duplicated words (D7) |

### Blocking findings

**D1 (blocks): SKILL.md:99 sends the doctor to the wrong section.**
The text reads "`guard_parse` not `verified`: make the missing call yourself (`phases/repair.md`, last section), then `--check` once." After this diff the last section of `phases/repair.md` is `## Codex code mode` (appended at the end), not "Does the pre-tool guard still parse this host's events?". Failure scenario: the doctor follows item 2's core instruction, opens the last section, and reads instructions for waiting on a Codex smoke. It finds no throwaway-write recipe, no "once" limit and no rule that the `reason` is never shown to the person. The OH3-6 behaviour then rests on luck. Cause: the coordinator's decision to append the Codex paragraph combined with an item-2 pointer that names a position, not a section. Fix: move `## Codex code mode` above the guard section in repair.md (costs 0 bytes in SKILL.md), or name the section in SKILL.md:99. Naming it is position-proof but costs bytes.

**D2 (blocks Q2): the next-action table still hands the person a factory script.**
- Verdict row 6a (SKILL.md:243): its next action is "`controller.py --task-root <T> --operation recover` (owner: factory)". "Next action: <exactly one line>" is addressed to the person. That violates the new printing rule 1 (":278 never a factory script, flag or plugin path"), spec item 3's invariant, P3, P9, FR-6 and AR-9. It also contradicts row 5a's principle that a factory-owned item is never the person's errand.
- Step 4 (:189, "Print the lines"): the STALE line is printed to the person verbatim, including its tail `controller.py … --operation recover`.
- This is the class item 3 introduces, inside the same artifact (sweep-the-artifact-first). The spec's §6 sweep enumerated the printing bullets and verdict row 8, but not rows 6/6a or step 4. I missed it in t-146 as well.
- Fix: row 6a's action becomes the repair the doctor itself runs under `phases/repair.md`, including its "is anybody working on `<T>`?" question, for example "the stale tail of `<T>`: the doctor repairs it (`phases/repair.md`)". Step 4 prints the STALE line without its command tail.
- Also check row 6 ("that halt's own instruction"): a halt instruction that names a script is the same class (the doctor runs it or names the owning skill). I did not establish whether halts carry script text, so this one is a question, not a finding.

**D3 (blocks Q2 / AR-28, FR-10): "No third bucket ... reads as 'all is well', and that is true" now contradicts FACTORY NOTES.**
SKILL.md:287-289 keeps the bullet: "No third bucket: everything outside 'here is what to do' reads as 'all is well', and that is true." FACTORY NOTES is a block outside "here is what to do" (its header says "nothing for you to do"), and it holds non-`ok` rows that READINESS must count as not ok. A doctor reading the two rules together gets two answers. Under the bullet, a factory-owned `unknown` reads as "all is well". Under :254/:279 it is "<k> of <n>, the rest in FACTORY NOTES". This is exactly the AR-28 failure the coordinator's Q2 asks about. The anchor "no third bucket" is a must-keep `role-rules.json:433` carrier, so it stays. Fix: one clause after it, for example "(FACTORY NOTES is not 'all is well': READINESS counts its rows)". About 60 B.

### Further fixes (this round)

**D4: cut (c) removed the only carrier of the step-2b question.** Step 2b (:149-150) still says "... else ask once" for a Jira sample ticket, and that question comes BEFORE the report. The removed never-list text was the one place that named it ("plus the sample ticket in step 2b when no story supplies one"). Now four carriers say otherwise: the opening "Three questions, all after the report" (:36), the never-list "its questions are those of the opening section" (:307), README "Asks only after the report: ... " (:63-64) and eval 4 ("the questions named are the three after the report"). The doctor's text contradicts itself about its own questions (FR-10), and eval 4 would grade a correct answer as wrong. Fix: name the 2b question once in the opening (about 50 B), and bring README and eval 4 into line. (Cut (c) came from the spec and passed my t-146. The defect is spec-side.)

**D5 (Q4, P14 / AR-11): Write is not bounded to its two targets by any sentence.** The writes sentence (:39-41) names "the guard-probe file". The words file appears only as an exception in the never-list (:309) and in repair.md:39. No sentence says Write serves only these two files: nothing stops the doctor from Writing, say, a `.claude/settings.json` (permissions.md says "the human writes that file", but that file is read only when asked) or a project file. F2-A accepted that the limit rests on the text, which is why the text must state it. Fix: in the writes sentence, "the guard-probe file and a release's words file (Write serves only these two)". About 45 B. Detector: eval 11/14 as in F2.

**D6 (spec defect; positional invariant of item 4): the step-3 gate sits after the fence it gates.** The fence (:169-173) still lists `project_gitignore.py --root . --check` unconditionally, under a heading that says "each one Bash call". The gate sentence comes after it. Failure scenario: before onboarding, the doctor pastes the three-line fence as one call, which produces exactly the `--check` listing that spec item 4's positional invariant says "must never even produce". The builder followed the spec, which said "the code fence keeps its `--check` line" (my t-146 passed it). Fix: put the third command in its own fence behind the gating sentence, in step 2's form "If `qa-factory/config.json` exists in the current directory, run:". That is the T6-protected phrase, so it also helps one-road consistency. Roughly byte-neutral.

**D7 (quality / carriers):**
- (a) repair.md "Codex code mode" opens "Step 1's smoke, on Codex in code mode: In Codex code mode print ...". The added intro duplicates the paragraph's own first words; drop one.
- (b) The persisted spec `t-144-doctor-oh3-6-12-7.md` still carries the pre-fix text (§0.5 estimate, item 4 "then `--check`", §3 `guard_defect` row, §0.3 wording). The binding fixes live only in the dispatch, so the `designer:` carrier disagrees with what was built. Record the fixes in the spec or in the node rows.
- (c) A smoke-wait recipe inside `phases/repair.md` ("Repairing the factory's own state") is an odd home. It is acceptable as the coordinator's decision, and D1's fix (move it above, or into its own phase file) can settle the placement.

**Byte budget for D1-D6:** headroom is 183 B. My estimate (not measured) is D3 about 60, D4 about 50, D5 about 45, D6 about 0-10, D1 0 if repair.md is reordered, D2 about 0 or negative. Total about 155-165 B, which fits but leaves the follow-up nodes OF1-4 and OH1-9 almost no room. t-146 already recommended that the Lead pre-approve relocating the stray `# Evidence capability checks` H1 (:316-319, about 174 B) into step 2. That remains open and is now needed.

### Q2-Q5 answers

- **Q2 (no factory script; no factory unknown shown as ok):** **not held.** D2: row 6a and the STALE line still give the person `controller.py`. D3: the "all is well" bullet contradicts the READINESS count. The rest holds. The format's READINESS alternatives, the mixed-precedence clause, and eval 15 `readiness-not-green` keep the count non-green. repair.md never relays `reason`. Eval 13 puts the pre-onboarding `host_hooks unknown` in FACTORY NOTES, which is not a demand.
- **Q3 (no .gitignore demand before onboarding):** **held in meaning.** Step 3's third command is gated on config.json in the cwd, the same predicate as steps 2 and 7 and row 3. Eval 1 carries `no-gitignore-demand-before-onboarding`. permissions.md is corrected. Row 8 does not fire on gitignore output. Weak spot: the placement (D6). The receipts the smoke writes before onboarding are the F5 root, outside this stream (Part A, A3).
- **Q4 (P14, Write scoped):** the tool is needed, and no narrower tool exists (t-146 F2: GUARD_FAMILIES keys on the tool name). I verified the guard lets the probe Write through: `test_claude_host_probe.py:473-484` puts a real `Write` to `qa-factory/state/doctor-guard-probe.txt` through the guard (exit 0, family verified). **The scope is not stated as a limit: D5.**
- **Q5 DUPLICATION AND CONSISTENCY:** inconsistencies D1, D3 and D4. The cut list of questions removed a duplicate but lost a member (D4). The `.gitignore` write reuses the one writer `project_gitignore.write_block`, so no duplicate mechanism. Grepped: `last section|repair.md` over the package (`*.md`, `*.json`, `*.py`): SKILL.md:37/41/57/99/194/309/312, test_person_words.py:641 (pin `FLAG`, `state/words/` still present), test_controller_task_flag.py:209. Also grepped `write_stdin|functions\.wait|text\(r\)|human writes that file|sample ticket|third bucket|Never asks a question|only file this skill writes|dropped VPN|green lines are worth` over scripts/design/references: no test pins the moved or cut text (hits are unrelated code and the role-rules:433 anchor, which is kept).
- **Q5 CODE QUALITY (text):** D7 (a) duplicated words, D7 (c) placement, and the stray H1 at the end of SKILL.md (pre-existing, t-146).
- **ONE ROAD (P31):** the onboarded branch is the task's own condition with one predicate. D6 would align step 3 with step 2's form. No language, project or case exclusion; the guard-probe uses "the host's file tool" on every host.
- **FR / AR walk spot-check:** AR-9 is claimed but not held while D2 stands. AR-28 is claimed, "READINESS never reads ok while FACTORY NOTES holds a non-ok row", and is contradicted by :287-289 (D3). AR-11 is claimed with "two targets", which the text does not state as a limit (D5). AR-14, AR-17, AR-25 and AR-29 hold. Fix 7 (role-rules rows) is queued to the full Lead. Until it lands, the step-3 gate and rule 1 have no CI guard: evals do not run in CI, and the key script is not committed.

### Class completeness (Part B)
Same artifact: the printing bullets were swept. The verdict rows 6/6a and step 4's printed STALE line were not (D2). The bullet "no third bucket" was judged "not applicable" by spec §6, but it is affected (D3). Axis 5 sibling skills (onboarding, qa-story): queued per spec §6. The coordinator must confirm a carrier exists (t-146 F4 note). Axis 10: the install_smoke root is the F5 node (Part A, A3).

---

## Trail

Read: t-141 verdict (whole); `git show b1875b4` (whole diff); worktree of-hooklib: `cost_capture.py main` (whole), `hooklib.py` 35-60, 54-80, 169-200, `dashboard_refresh.py` 1-80, `run_suite.py` 890-915 and the `refresh_dashboard()` call sites, `activity_capture.py` 1-28, `recover_codex_usage.py` 15-50, `test-layers.json` keep row of test_cost_capture_settled.py, `docs/SIBLING_MAP.md:256`; the narrative snapshot 2026-11-12-1932 line 27; journal grep for F5 and install_smoke. Part B: spec t-144 (whole), verdict t-146 (whole), `git show 9a97901 -s`, `git diff origin/main...wip/of-doctor` (all 6 files), SKILL.md after the change (whole, 319 lines), repair.md after the change 1-45 plus the diff, `role-rules.json:433` and the doctor row ids, `test_claude_host_probe.py:465-500`.

Re-runs (verbatim tails):
- `python -B <of-hooklib>/ai-packages/qa-factory/scripts/tests/test_cost_capture_settled.py` -> "PASS B-hook control: a project root captures as before / PASS B-suite run_suite.refresh_dashboard on a bare cwd returns, escapes no SystemExit, writes nothing / === test_cost_capture_settled: 159/159 ok ===" (real 12.5 s).
- `python -B tools/test_quarantine.py check --root <of-hooklib>` -> five lines "quarantine check: b8989353 (x2) / f99b9f37 (x1) / b1875b4b (x2): quarantined file ... expected a line 'quarantine-edit: <bare name> -- <reason>' ... or a later commit line quarantine-accept", then "quarantine check: 5 violation(s)", rc=1. Also `git diff --stat origin/main...wip/of-hooklib -- <both quarantined files>` -> empty (net zero).
- SKILL.md bytes at 9a97901 (raw / CRLF->LF): "18817 18817".
- `( cd <of-doctor>/ai-packages/qa-factory && python -B scripts/selftest.py --limits --lang )` -> "PASS limits: SKILL.md / agents / references within size caps / PASS limits: every mandatory role rule of design/role-rules.json holds in its carrier / === qa-factory selftest: 4/4 ok ===".
- evals.json at 9a97901: "[1..15] True" (ids unique); id 12/13 assertion names unchanged (listed).
- I did not re-run the builder's 98-file union run or the doctor key script. They are consistent with the diff: the key list matches the shipped text, and the negative control is described. I ran no slow or quarantined file (non-goal).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "A0: tools/test_quarantine.py check on of-hooklib reports 5 violations, rc=1 (b8989353 x2, f99b9f37 x1, b1875b4b x2): no quarantine-accept lines for the earlier commits, and b1875b4 quarantine-edit lines use full paths where the check matches bare names; t-141 B1 consequence 2 not closed",
    "B-D1: SKILL.md:99 points to phases/repair.md 'last section', which after the Codex move is 'Codex code mode', not the guard-parse section: item 2's core instruction misroutes",
    "B-D2: verdict row 6a (SKILL.md:243) and step 4's printed STALE line still hand the person controller.py --operation recover, against new printing rule 1 (P3, P9, FR-6, AR-9); same-artifact sweep missed",
    "B-D3: SKILL.md:287-289 'No third bucket: everything outside here-is-what-to-do reads as all is well, and that is true' contradicts FACTORY NOTES holding non-ok rows that READINESS counts (AR-28, FR-10)"
  ],
  "fixes": [
    "A0: add a later commit with quarantine-accept: b898935, f99b9f3 and b1875b4 (reason: node tests moved out, net zero), or squash the branch; witness the check at 0 violations",
    "A1: recover_codex_usage.py:32 holds the literal set doctor/onboarding/story and refuses collect and environment-maintenance boundaries; use REAL_FACTORY_TYPES or queue with a node id (CD1-11 class, AR-1)",
    "A2: update docs/SIBLING_MAP.md axis 10 row (dashboard and cost_capture hook done) in the move that opens the F5 node",
    "A3: F5/F7 proposals reached review as titles only; F5 must choose a non-refusal direction (spool or printed path; refusal breaks the doctor's pre-onboarding smoke, FR-5), name install_smoke main/run_report, a bare-root test row and the axis 10 row; F7 must name the hooklib builder with the ancestor hint and extra door, the host_probe and require_project_at callers, the dashboard_refresh marker check, the docstring, the kept pins (quarantined test_host_probe_shapes handled) and a table test",
    "D1: reorder repair.md so the guard section is last, or name the section at SKILL.md:99",
    "D2: row 6a action becomes the doctor's own repair per phases/repair.md (with its question); step 4 prints the STALE line without the command tail; check row 6 halt instructions for script text",
    "D3: add one clause after 'no third bucket' (anchor kept): FACTORY NOTES is not all-is-well, READINESS counts its rows",
    "D4: restore the step-2b sample-ticket question in the opening question list; align README:63-64 and eval 4",
    "D5: bound Write in the writes sentence: the guard-probe file and a release's words file, nothing else",
    "D6: put project_gitignore --check in its own fence behind 'If qa-factory/config.json exists in the current directory, run:' so a not-onboarded run never produces its output",
    "D7: drop the duplicated 'In Codex code mode' words in repair.md; record the binding t-146 fixes in spec t-144 or the node rows; Lead to pre-approve relocating the stray Evidence H1 (about 174 B) since D1-D6 consume most of the 183 B headroom"
  ],
  "class_completeness": "Part A: CD1-11 predicate unified at all four readers; one sibling holding the same closed set left in recover_codex_usage.py:32 (A1). OH3-37 axis 10: dashboard, cost_capture hook and run_suite refresh closed; install_smoke --report and the second refusal builder in host_probe go to F5/F7 nodes whose texts are not yet well-formed (A3); axis 10 row stale (A2). Part B: printing bullets swept, but verdict rows 6/6a and the printed STALE line not (D2); the 'no third bucket' neighbour judged n/a but affected (D3); cut (c) dropped a question carrier (D4); axis 5 sibling skills queued per spec; fix 7 role-rules rows queued to full Lead, so no CI guard yet.",
  "trail": {
    "read": [
      "docs/tasks/specs/reviews/t-141-of1-hooklib-critic.md",
      "git show b1875b4 (whole)",
      "of-hooklib ai-packages/qa-factory/scripts/cost_capture.py main",
      "of-hooklib scripts/hooklib.py 35-80, 169-200",
      "of-hooklib scripts/dashboard_refresh.py 1-80",
      "of-hooklib scripts/run_suite.py 890-915 and refresh_dashboard call sites",
      "of-hooklib scripts/activity_capture.py 1-28",
      "of-hooklib scripts/recover_codex_usage.py 15-50",
      "of-hooklib scripts/tests/test-layers.json keep row test_cost_capture_settled.py",
      "docs/SIBLING_MAP.md:256 (main and worktree)",
      "docs/tasks/compact-snapshots/2026-11-12-1932-narrative.md:27",
      "docs/tasks/specs/t-144-doctor-oh3-6-12-7.md",
      "docs/tasks/specs/reviews/t-146-doctor-plan-critic.md",
      "git diff origin/main...wip/of-doctor (6 files)",
      "of-doctor skills/qa-doctor/SKILL.md (whole, after)",
      "of-doctor skills/qa-doctor/phases/repair.md 1-45 and diff",
      "of-doctor design/role-rules.json:433 and doctor rows",
      "of-doctor scripts/tests/test_claude_host_probe.py 465-500"
    ],
    "reruns": [
      {"command": "python -B of-hooklib scripts/tests/test_cost_capture_settled.py", "result": "159/159 ok, real 12.5 s"},
      {"command": "python -B tools/test_quarantine.py check --root of-hooklib", "result": "5 violations, rc=1: b8989353 x2, f99b9f37 x1, b1875b4b x2 (full-path quarantine-edit lines do not match the bare key; no quarantine-accept for earlier commits)"},
      {"command": "byte count SKILL.md at 9a97901", "result": "18817 raw / 18817 LF"},
      {"command": "selftest.py --limits --lang (of-doctor package cwd)", "result": "4/4 ok; size caps PASS; role-rules anchors PASS"},
      {"command": "evals.json at 9a97901 ids and id 12/13 names", "result": "ids 1-15 unique; names unchanged"}
    ]
  }
}
```

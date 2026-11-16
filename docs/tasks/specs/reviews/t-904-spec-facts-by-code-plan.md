# t-904 — plan review: "Spec facts by code, spec judgment by the plan critic" (spec t-897, with the Lead's fork decisions)

Reviewed: `docs/tasks/specs/20261116-spec-facts-by-code-spec.md` (583 lines, read whole, including "Lead decisions on the forks").
Base searched: `origin/main` = `0d6f61b1`. Every grep below is `git -C C:/QAFactory/forge-repo grep ... origin/main`. The scope array
I used is the spec's §2.3 scope with `:(glob)` magic and two `:(exclude,glob)` items. My own script, kept in the session scratchpad
and not committed.

## Verdict: GO WITH FIXES (6 blocking, 11 minor)

The direction holds. Code gathers facts and the critic gets a judgment question. C3 is a note only, the promotion path is written,
and no code refuses on a judgment (item 4 holds). But the main piece of the plan, the reader list by literal file-name mention,
has no firm hit in the replay once the replay is checked against the journal. Under the specified cap it also hides the readers
that matter. Two more problems block: one premise does not reproduce (the slow-list reader), and two places let an unknown read as
a pass. All six blockers can be fixed in the spec text before S1 starts. No rework of the direction is needed.

---

## BLOCKERS

### B1 — §2.4 cap + §2.3 error direction: with the cap, "over-report is safe" stops being true, and the load-bearing readers end up in the overflow
- **What.** The spec lets the search over-report (§2.5: "may err toward OVER-reporting"). It also caps the output at 12 `outside` lines and does not define the ORDER. So the noise pushes the real readers into the overflow. Over-reporting plus a cap gives under-reporting of the listed set.
- **Evidence (hand run, the spec's own S2 owns).** Owned: `tools/dispatch_manifest.py` + `tools/test_dispatch_manifest.py`. Readers outside owns: 20. Sorted the way a natural implementation would sort them, lines 1-12 are `agent_budget.py … test_dispatch_cut.py`. Line 13 is `tools/test_dispatch_gate.py` and line 15 is `tools/test_dispatch_new.py`. Those are exactly the two tests that S2's own DoD names, and both land in `unsearched: 8 more`. For `selftest.py` (S1's DoD run): 106 files. The two tests from journal line 829, `test_selftest_shard.py` and `test_selftest_slow_tests.py`, sit at positions 77-78.
- **Fix.** Define the order and the grouping. TEST readers first, all of them up to a test cap (e.g. 25). Code readers as one count line, `+N code readers (--all)`. Data carriers listed. Quarantined readers as one count line unless they are owned (see M10). When the test readers pass the test cap, the header says `hot file: pass --names <changed functions>` instead of listing them.

### B2 — §2.1/§2.3/F-4: `--names` HITS have no output shape (only `absent`), and a name the spec introduces reads `absent`
- **What.** Names that are found are never printed, so the name-level readers that the replay itself offers as the fix are never shown. And a function the dispatch asks the builder to CREATE has zero hits on the base, so it gets `- absent: name …`. That is a false alarm on every dispatch that introduces a name: the temporal edge of CLAUDE.md rule 11 (i).
- **Evidence.** Journal 1395 (t-559). The commit `3e8a085d` touched `driver_s0.py`, `ticket_adapter.py` and `test_story_run_s0.py`. At `3e8a085d~1`, `test_conductor_doors.py` does NOT name `driver_s0` or `ticket_adapter` (grep: empty. Positive control, same shape: `driver_s0` is named by 8 files). It names the METHOD: `test_conductor_doors.py:760 raised(driver.s0_criteria, …`. Only a `--names s0_criteria` hit line would have shown it. Line 1117 (the `qa-retro-analyst` pin) is the same class.
- **Fix.** Add `- names: <reader> (test|code|data) names <n>`, tests first, under the B1 caps. Add a ` (new)` marker for names, the same as for paths: a `(new)` name that is absent prints nothing, and a `(new)` name that is present prints `exists`.

### B3 — §2.5 E-2/E-3/E-14: an unknown can still read as a pass (FR-59)
- **What and evidence.**
  1. `git grep` exits 1 when nothing matches. Any other rc is an error (128). `gitcmd.git` returns -1 on a timeout (`tools/gitcmd.py:15-17`). The spec never maps rc to meaning, so "the grep failed" can be rendered `readers: ok -- 0 readers`.
  2. E-2's order ("resolve first") only covers a base that does not resolve. `_blob_sections` runs its OWN `_git` (`tools/test_quarantine.py:116-122`, timeout 120, `except → 128`). When `git show` fails AFTER `rev-parse` succeeded (timeout, I/O, the file absent), it returns empty sections (`:210-211`). That reads as "not quarantined", and the tool cannot tell it apart from E-3 "absent".
  3. Malformed `test-layers.json`: `_blob_sections` raises `test_quarantine.Unknown` (`:215`). E-3 covers only "absent". The exception would climb to `dispatch_new` and turn the WHOLE block into `readers: unknown`, losing every other fact.
- **Fix.** State the rc mapping: 0 = hits, 1 = none, anything else = `unknown`. Get the registry's presence from the tool's own `ls-tree` (the same call as (iv)). If the file is present and the sections come back empty or raise `Unknown`, print `quarantine: unknown (<why>)` in the header and keep the rest of the block. Add T1 rows for: grep rc 128, `git show` failing after the base resolved, and malformed JSON.

### B4 — §3.1 × §3.2: C3's note fires inside `dispatch_new` on the headers it is about to extend
- **What.** `dispatch_new.main` calls `dispatch_gate.decide_full` on the header text WITHOUT the block. It prints `decision.notes` to stderr (`tools/dispatch_new.py` main: `note = "\n".join(... decision.notes ...)` → `print(note, file=sys.stderr)`). `decide_full` calls `dm.check_cut` (`tools/dispatch_gate.py:798-800`), which is exactly where C3 adds `READERS NOTE: this writing dispatch carries no readers: line -- run … (dispatch_new.py prints it)`. After S2, every run of the generator would print a note telling the Lead to run what it is printing. These are two requirements of the spec's own that conflict (rule 11), and the spec says nothing about it.
- **Fix.** In S1, `dispatch_new` builds the block FIRST and passes headers + blank line + block to `decide_full`, so the hook checks the text it prints (it then works as a live check of §3.1's "the block never enters a section" invariant). Add a T2 row: no `READERS NOTE` on stderr when the block is present.

### B5 — §1, §2.3 (ii), premise P7, F-7: the slow-list reader exists, and the spec's "slow" means something else
- **What.** P7 says `slow_tests.json` "has no reader function". It does: `selftest.slow_tests(path)`, docstring "The one reader of scripts/slow_tests.json" (`ai-packages/qa-factory/scripts/selftest.py:1000`), with a shape validator `_slow_tests_problem` (`:975`). P7 grepped `SLOW_TESTS\b`, but the names are `SLOW_TESTS_FILE` (`:103`) and `slow_tests()`. The meaning differs too. In the one reader, "slow" is MEMBERSHIP: `fast=True skips the files scripts/slow_tests.json names` (`:868`), "between the two thresholds it keeps whatever it has". The spec's rule "seconds over `slow_over_s`" is a different predicate.
- **Evidence (empirical, CLAUDE.md critic rule 13).** On origin/main: 145 files listed, of which 6 are listed with ≤ 10 s or null: `test_audit_rules.py, test_codex_host.py, test_controller_release.py, test_controller_rework_scope.py, test_s5_plan.py, test_test_locations.py`. The canon skips them in the fast tier. The spec's tool would call them not slow. Two of them are `test_controller_*`, which PROJECT.md names as files the builder must not run locally. The spec's own §4.1 (c) says "one [premise] that does not reproduce blocks".
- **Fix (F-7 should change).** Read through the one reader. Validate the blob text at the base with `selftest._slow_tests_problem(raw)` and use membership in `files` as "slow", reached the way `test_quarantine._pkg_module` already loads selftest. Or write the blob to a temp file and call `slow_tests(path)`. Drop the threshold rule, and correct P7.

### B6 — §R replay: the hit rate is overstated, and it is never measured against the 30 code-fact rejects
Re-check of rows (journal `logs/journal/dev1.jsonl` + origin/main and historical revisions):

| Line | Spec says | Re-check | Evidence |
|---|---|---|---|
| 1395 (t-559) | likely yes | **no** (yes only with B2's names hits) | owned `driver_s0.py`/`ticket_adapter.py`. At `3e8a085d~1` the test names neither (control: 8 readers of `driver_s0`). It names the method `s0_criteria` (:760). `s0.md`/`driver.md` were stale docs, not owns |
| 1181 (t-462) | likely yes | **no for t-462** | t-462 was an integration of branches. The ratchet red came from t-437's earlier merge (journal 1180: "TR4-15 slice text put qa-failure-analyst over its role-load ratchets … Merged in wave 21 without canon"). The tool on t-462's owns does not see someone else's merged change. It could have helped t-437, if t-437 owned the role file |
| 294 / 307 (t-113) | yes as tests / partial | **no new information** | line 294 says "the DoD run is 100 failed": the reader tests were already in the DoD run. What was missed is what a new mandatory key does to 99 existing fixture inputs. That is a temporal edge (PART 2 (a)), not a missing reader |
| 829 (t-325) | partial | **no under the cap** | positions 77-78 of 106 (B1). The cause it names (selftest.py:93 rule) is a2 |
| 1115 (t-439) | yes | **yes** | `test_import_test_receipt.py` is in `quarantine` at origin/main (checked in the parsed blob: True) |
| 1117 (t-442) | probably no | **agree: no** (yes with B2) | `test_walk_plan_fields.py` names `role-load` once. The pin is gone today (grep `qa-retro-analyst`/`14075` → empty, control `role-load` → 1) |
| 384, 397, 1060 | yes | **accepted as likely** | notes say the builder wrote into or was sent to quarantined files. I did not rebuild the owns of each |

Firm catches of PART 1 as specified: the 4 quarantine lines (384, 397, 1060, 1115), plus 541 through F-4. The literal reader list, which is most of the machinery, has **zero** firm catches among the replayed reader rows. The denominator question stays open. The 30 code-fact rejects have no carrier: the t-896 digest is not persisted, and journal 2196 says "classes are the scout's reading of journal notes". So "what share of the 30 stays uncaught" cannot be computed and the spec does not state it. **Fix:** restate §R with the corrected rows and say plainly that the reader list's yield is unproven. Either persist the scout's per-line classification, so the denominator has a carrier, or state the share as an estimate. Size the plan to the replay (item 8 below).

---

## Minor findings (fix in this round, in the spec text)

- **M1 — §2.3 scope: pathspec semantics are not stated.** In git's default pathspec, `*` crosses `/`. Measured: `.../tests/fixtures/*.json` matches 584 files with the default (depths 7-14), but 13 with `:(glob)`. The spec's "top level only" is therefore false unless glob magic is used. `git ls-tree` refuses `:(glob)` ("pathspec magic not supported by this command: 'glob'"). Fix: state `:(glob)` for every scope row and `:(exclude,glob)` for the excluded rows. Say that the `ls-tree` calls take literal paths only.
- **M2 — §2.2 header wording carries a verdict.** `readers: ok` and `N to act on` judge the facts (P27): an imported code reader is not automatically something to act on, and `ok` on a file whose real readers are name-level (1395) is false comfort. Fix: `readers: 0 outside owns (literal mention; known misses in docstring)` and `readers: N listed`. Update C3's regex to match.
- **M3 — E-4 vs §3.1.** E-4 prints `<path> is outside the repo`, which can be absolute (`C:/elsewhere/x.py`). That breaks the §3.1 invariant "no absolute path", and `dispatch_gate.given_path_warn` reads paths on any line. Fix: print the base name plus `(outside the repo)`, or restate the invariant.
- **M4 — §6 axes and S-5.** Lead edits name axes 13, 18, 31 and 34. They miss: **axis 9** ("is this a test file"; the forge precedent `tools/test_volume.py` got its own line, `docs/SIBLING_MAP.md` axis 9 last paragraph, and this tool's `test_*` glob reader with the over-report direction needs the same line); **axis 10** (the gitcmd caller enumeration gets `owns_readers`); **axis 2** (exam instruments, for the critic.md edit). S-5 "the tool reaches git only through gitcmd.git" is false while `_blob_sections` runs `test_quarantine._git`. Name it.
- **M5 — F-6 exam deviation: one road.** The precedent exists. Commit `1f165a38` (critic.md, t-847) recorded "Deviation (F-A1-2) … exam was not run; the debt stands in plans/piles/forge/batch-3-exam-debts.md" (node F3-1 there). Use the same road: name F3-1 and add to its debt row. Do not invent a new "recorded as not runnable" form.
- **M6 — §6 detector L7 / the promotion rule of §3.2.** Both count "class a1/e rejects", but the class lives nowhere in machine form. Fix: a bare notes token on `rejected` lines (e.g. `spec-class:a1`, read like `closes:`), or define the detector on what IS countable: `failure_class: spec` rejects whose dispatch did or did not carry a `readers:` line.
- **M7 — §4.1 text.** (i) The home file is titled "Standing brief for the critic gate on a builder diff". Retitle it, or add a first-paragraph line that it also holds the plan gate. (ii) (c) re-states critic.md rule 12. Cite it, and keep only the "one or two" bound. (iii) (d) "its KNOWN MISSES are yours to judge" has no stated answer form. Make it concrete: miss 3 → "does the plan change a VALUE (a count, a key) pinned elsewhere: name the value and grep it"; miss 1 → "for a package path, `--witness-for` is the transitive list"; misses 2 and 5 → "answered 'not applicable — why' or one grep".
- **M8 — §3.1.** `dispatch_new.py`'s docstring says "NO grammar of its own … Pure output: stdout only … these are the only rules of the generator's own". S1 changes that contract, so the docstring edit belongs in S1's DoD.
- **M9 — One road (P31/AR-15, critic rule 19).** For package paths, a builder now gets two answers to "which tests concern this path": `scenario_walk.py --witness-for` (keep `covers` + import closure) and this tool (literal mention). §N.5's "possible later convergence, not in this spec" is the kind of residual rule 19 forbids. Fix: state the split in both docstrings (witness-for = what to RUN; owns_readers = what must not break or be edited, plus layer status), and open a node with an owner for the later convergence.
- **M10 — §2.4/§6 (a) cost claim "1-15 block lines".** Caps are defined for `outside` only. Owned `story_run.py`: 253 readers outside, of which **81 are quarantined** and 55 slow by the spec's predicate, plus 12 `data` carriers. If `quarantined` reader lines and `data` lines are not capped, the block is about 107 lines. State caps or aggregation for every kind (B1's fix covers it).
- **M11 (side observation, outside this spec).** `docs/tasks/critic-diff-brief.md:11-12` still says "until `scripts/tests/test-layers.json` holds quarantine rows". The quarantine section holds 431 rows. A stale clause for the Lead to queue.

## Item 2 — the two hand runs (noise, caps, wall time)

Command shape (spec §2.3 (i), file name + stem `-w`, the scope with `:(glob)`/excludes):
`git -C <repo> grep -I -l -w -F -e <stem>.py -e <stem> origin/main -- "${SCOPE[@]}"`

`tools/dispatch_manifest.py`: **22 files, 138 hit lines (-o), real 0m0.200s**. Head:
```
origin/main:tools/agent_budget.py
origin/main:tools/dispatch_gate.py
origin/main:tools/dispatch_manifest.py
origin/main:tools/dispatch_new.py
origin/main:tools/dod_gate.py
```
Outside an S2 owns: 20 (9 tests, 10 code, 1 data `tools/warn_layers.json`), 0 quarantined, 0 slow. Cap 12 → S2's own DoD tests are hidden (B1).

`ai-packages/qa-factory/scripts/story_run.py` (hot file): **254 files, 1942 hit lines, real 0m0.190s**. Classes: tests 173, data 12, code 69. 81 quarantined. Head:
```
origin/main:ai-packages/qa-factory/references/collect-loops.json:story_run.py
origin/main:ai-packages/qa-factory/references/conductor-actions.json:story_run.py
origin/main:ai-packages/qa-factory/references/driver-infra.json:story_run.py
origin/main:ai-packages/qa-factory/references/field-producers.json:story_run
```
Under the cap: 12 lines + `241 more`. Nothing actionable gets through for a function-level change. Only `--names` (B2) makes a hot-file block useful.

Wall time: ~0.2 s per grep, so the spec's "under 5 s, estimate" is safe by a wide margin. The cost is context paid by every worker, not time (P11/FR-55). Common-word stem noise, measured: stem `contract` (a real `scripts/contract.py`) is a whole word in 537 scope files against 96 that name `contract.py`. This feeds B1.

## Item 3 — one road (answer)
- test-layers.json: read through `_blob_sections`. Correct reuse, apart from the unsafe error direction (B3).
- slow_tests.json: the spec makes itself a second reader even though the one reader exists (B5). That is a finding.
- `scenario_walk --witness-for`: a parallel answer for package paths, with no node (M9).
- `dispatch_gate` path check: the block's paths flow into `given_path_warn`. The spec accepts that knowingly (§3.1). OK, except M3.
- `test_role_carriers_one_owner.py`: the L4 pointer row is planned. OK.
- critic-diff-brief item 9 / `source-split-carriers.json`: covered by the data globs, no second list (F-3 a). OK.
- Duplication check, empty answers: none found beyond the above. Grepped `quarantine` over `dispatch_gate.py dispatch_manifest.py dispatch_new.py owns_gate.py dod_gate.py handoff_gate.py`: 0 hits. Positive control, same call: `test_quarantine.py:141`. So no existing dispatch-time quarantine reader exists. The canon's `quarantine-edit` check runs only nightly (`.github/workflows/nightly.yml:240`) plus in canon.

## Item 4 — judgment vs data
Kept. C1 prints facts. C3 is a note with a hand-typed door. Promotion only on log evidence and as a new node (rule 10 (d)). Remaining nits: the header words (M2), and the detector carrier (M6).

## Item 5 — PART 2 rule
Executable for (a)-(c). (d) needs answer forms for the known misses (M7). It tells the critic not to re-grep what the block lists, which is good. It lives in critic-diff-brief with a critic.md rule 21 pointer and an L4 pin, so it is on the critic's path. It overlaps lightly with brief item 1 (diff gate) and critic rule 12; cite them, do not restate (M7).

## Item 6 — edges of the tool
Stated: no ref (E-2), `(new)` (E-5), directory (E-6), spaces (E-8), short stem (E-10/S-3), binary (E-11), git timeout (E-2, but only for rev-parse: B3). Missing or wrong: grep rc semantics (B3), registry failure after resolution (B3), malformed test-layers (B3), a common-word stem ≥ 4 characters (E-10 cites `config`, which is 6 characters and so is NOT skipped; measured noise is ~5×: B1), `(new)` names (B2), absolute path in E-4 (M3), pathspec magic (M1). Detached worktree: not stated, but behaviour is identical (refs are shared). One line in E-13 is enough. An unknown stays an unknown only after B3's fixes.

## Item 7 — four questions
(a) Cost: the stated "1-15 lines" is contradicted by measurement (M10). Time is cheap (~0.2 s). (b) Axes: incomplete (M4). (c) Detector L7: has no machine carrier for its class (M6). (d) On the path: dispatch_new prints the block and C3 is a note. Fine once B4 is fixed.

## Item 8 — the cheapest version that catches the named repeats
The repeats named in the dispatch, and what catches each:
- quarantine not named: (ii) on owned and given paths, no grep needed;
- a test outside owns pins the old behaviour: name-level hits, B2;
- a reader of the owned file not named: the literal list, useful only for small, non-hot files;
- unmerged code: (iv) plus F-4.

The minimal tool is (ii) + (iv) + `--names` presence and hits (tests first), with the literal file-name reader list as a tests-only section behind a count. That catches every firm replay hit (384, 397, 1060, 1115, 541) plus 1395 and 1117 with names. The plan as written is bigger mainly in the uncapped kinds and the code-reader listing, and smaller where it matters (no names hits).

## Forks where the Lead's decision should change
- **F-7**: (a) → read through `selftest.slow_tests` / `_slow_tests_problem`, membership semantics (B5).
- **F-4**: (a) stands, but add hits and a `(new)` marker (B2).
- **F-10**: replace the flat 12/40 with tests-first ordering and per-class aggregation (B1, M10). 40 per directory is fine.
- **F-6**: (b) stands. Record the exam on the existing F3-1 debt road (M5).
- **F-1, F-2, F-3, F-5, F-8, F-9**: agree. For F-2, add the hot-file header that asks for `--names`.

## What I did not check
- I did not rebuild the owns of t-133/t-134/t-420, so 384/397/1060 are taken from their notes.
- I did not classify the other 51 spec rejects, and the scout's per-line classes have no carrier.
- I did not read SIBLING_MAP axes 13/18/31/34 bodies, beyond their titles and axes 9-10.
- I did not read `dispatch_manifest.py` beyond `check_cut`'s head, so the §3.1 position invariant (sections end at a blank line) is taken from P2.
- No tests were run (non-goal).

## Trail
Read: the spec (whole); `docs/tasks/critic-diff-brief.md` (whole); `tools/dispatch_new.py` 1-40, 60-80, 120-170; `tools/gitcmd.py` 1-60; `tools/test_quarantine.py` 108-140, 205-270 (origin/main); `selftest.py` 99-112, 960-1025 (origin/main); `scenario_walk.py` 887-927; `docs/SIBLING_MAP.md` axis list + 232-273; `tools/critic_verdict.schema.json`; journal lines 294, 307, 384, 397, 541, 829, 1060, 1115, 1117, 1138-1182, 1383, 1395, 1972, 2188-2196; `PROCESS/README.md` 18-26; `docs/TESTING.md` grep for «Файлы».

Commands (verbatim results):
- `git rev-parse --short=8 origin/main` → `0d6f61b1`
- `grep -c '"failure_class":"spec"' logs/journal/dev1.jsonl` → `65` (by day: 11.11 1, 12.11 29, 13.11 29, 14.11 6)
- fixtures pathspec: default `*.json` → 584 files at depths 7-14; `:(glob)` → `13`; `git ls-tree … ':(glob)…'` → `fatal: … pathspec magic not supported by this command: 'glob'`
- hand runs: see item 2 (22 files/0.200 s; 254 files/0.190 s; selftest 106 files, shard/slow tests at 77-78)
- quarantine/slow on story_run readers (parsed origin/main blobs): `story_run quarantined readers 81 … slow 55`; `dispatch_manifest quarantined readers 0 … slow 0`
- `test_import_test_receipt.py True` (in quarantine); `test_walk_plan_fields.py/test_conductor_doors.py/test_selftest_shard.py False`
- `git show --stat 3e8a085d` → `driver_s0.py, test_story_run_s0.py, ticket_adapter.py, changelog, report`; grep at `3e8a085d~1`: test_conductor_doors names neither stem; `s0_criteria` at test_conductor_doors.py:760; control `driver_s0` readers → `8`
- slow list: `listed 145 listed but <=10s or null 6 ['test_audit_rules.py', 'test_codex_host.py', 'test_controller_release.py', 'test_controller_rework_scope.py', 'test_s5_plan.py', 'test_test_locations.py']`
- stem noise: `contract: word-files 537 name-files 96`; `report: 646/27`; `state: 927/6`; `paths: 379/20`
- `git grep -c -i quarantine origin/main -- tools/dispatch_gate.py tools/test_quarantine.py` → only `tools/test_quarantine.py:141`
- `git log origin/main -- .claude/agents/critic.md` → `1f165a38 … (t-847)`, message: `Deviation (F-A1-2): … PROCESS/CRITIC_EXAM.md is absent … debt … batch-3-exam-debts.md`
- duplicate .py basenames across tools/ and scripts/ → `sitecustomize.py` only (same-basename attribution is not a practical risk)

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1 s2.4/s2.3: a flat 12 cap with no defined order plus an over-reporting search hides the load-bearing readers; S2's own DoD tests test_dispatch_gate.py and test_dispatch_new.py land at positions 13 and 15 of 20, and the line-829 tests at 77-78 of 106 for selftest.py",
    "B2 s2.1/s2.3/F-4: --names hits have no output shape (only absent), so name-level readers like s0_criteria in test_conductor_doors.py:760 (line 1395) are never printed; a name the spec introduces reads absent (temporal edge)",
    "B3 s2.5 E-2/E-3/E-14: git grep rc semantics are not mapped; _blob_sections returns empty sections on a git show failure after rev-parse, which reads as not quarantined; malformed test-layers raises Unknown and wipes the whole block",
    "B4 s3.1 x s3.2: dispatch_new calls decide_full on headers without the block, so C3's READERS NOTE fires on every generator run",
    "B5 s2.3(ii)/P7/F-7: selftest.slow_tests (selftest.py:1000) is the one reader and its meaning is list membership (fast tier skips the listed files); the spec's threshold rule misreports 6 listed files and P7 does not reproduce",
    "B6 sR: replay overstated; 1395 is no (verified at 3e8a085d~1), 1181 is no for t-462, 294/307 add no information, 829 is hidden by the cap; firm catches are the 4 quarantine rows plus 541 via F-4; the share of the 30 code-fact rejects has no carrier and is not stated"
  ],
  "class_completeness": "SIBLING_MAP: the spec names axes 13, 18, 31, 34; missing axis 9 (forge test-file recognizer, precedent tools/test_volume.py), axis 10 (gitcmd callers; _blob_sections uses its own _git, so S-5 is false), axis 2 (exam instruments for the critic.md edit). One road: second slow_tests reader (B5); parallel witness-for answer with no node (M9).",
  "trail": {
    "read": [
      "docs/tasks/specs/20261116-spec-facts-by-code-spec.md",
      "docs/tasks/critic-diff-brief.md",
      "tools/dispatch_new.py",
      "tools/gitcmd.py",
      "tools/test_quarantine.py@origin/main:108-140,205-270",
      "ai-packages/qa-factory/scripts/selftest.py@origin/main:99-112,960-1025",
      "ai-packages/qa-factory/scripts/tests/scenario_walk.py@origin/main:887-927",
      "docs/SIBLING_MAP.md axis list and 232-273",
      "tools/critic_verdict.schema.json",
      "logs/journal/dev1.jsonl lines 294,307,384,397,541,829,1060,1115,1117,1138-1182,1383,1395,1972,2188-2196",
      "PROCESS/README.md@origin/main:18-26"
    ],
    "reruns": [
      {"command": "git grep -I -l -w -F -e dispatch_manifest.py -e dispatch_manifest origin/main -- <spec scope with :(glob)>", "result": "22 files, 138 hit lines, real 0.200s; 20 outside an S2 owns; DoD tests at positions 13 and 15"},
      {"command": "git grep -I -l -w -F -e story_run.py -e story_run origin/main -- <spec scope>", "result": "254 files, 1942 hit lines, real 0.190s; tests 173, data 12, code 69; 81 quarantined"},
      {"command": "git grep -l -w -F -e selftest.py -e selftest origin/main -- <spec scope>", "result": "106 files; test_selftest_shard.py and test_selftest_slow_tests.py at 77-78"},
      {"command": "git grep -w -F driver_s0/ticket_adapter/s0_criteria 3e8a085d~1 -- test_conductor_doors.py", "result": "no stem hits (control: driver_s0 named by 8 files); s0_criteria at :760"},
      {"command": "python parse slow_tests.json@origin/main", "result": "145 listed, 6 listed at <=10s or null"},
      {"command": "git grep -l '\"' origin/main -- fixtures/*.json default vs :(glob)", "result": "584 vs 13 files"},
      {"command": "grep -c failure_class spec logs/journal/dev1.jsonl", "result": "65"}
    ]
  },
  "fixes": [
    "B1: tests-first order, all test readers up to a test cap, code readers as a count, quarantined non-owned readers as a count, hot-file header asking for --names",
    "B2: print --names hits as '- names:' lines under the same caps; add a (new) marker for names",
    "B3: rc map 0/1/other; registry presence from the tool's own ls-tree; quarantine: unknown on empty or Unknown after presence; T1 rows for grep rc 128, git show failure, malformed JSON",
    "B4: dispatch_new passes headers + block to decide_full; T2 row: no READERS NOTE when the block is printed",
    "B5: read slow status through selftest.slow_tests or _slow_tests_problem with membership semantics; correct P7; change F-7",
    "B6: restate sR with the corrected rows and state that the reader list's yield is unproven; persist the scout classes or label the share an estimate",
    "M1: :(glob) and :(exclude,glob) pathspecs stated; ls-tree takes literal paths only",
    "M2: neutral header words (counts and method), C3 regex updated",
    "M3: E-4 prints no absolute path",
    "M4: axes 9, 10, 2 in the commit block; S-5 corrected for _blob_sections' own _git",
    "M5: exam deviation on the existing F3-1 debt road",
    "M6: a machine carrier for the detector class or a detector on readers-line presence",
    "M7: brief retitle, cite critic rule 12, concrete answer forms for known misses",
    "M8: dispatch_new docstring contract edit in S1's DoD",
    "M9: state the witness-for / owns_readers split in both docstrings and open a convergence node with an owner",
    "M10: caps or aggregation for every kind; correct the 1-15 line cost claim"
  ]
}
```

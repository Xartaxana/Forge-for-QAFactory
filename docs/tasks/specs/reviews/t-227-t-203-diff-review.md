# t-227 — critic on the DIFFS of t-203, Part A (OH3-36) and Part B (OH5-11)

Reviewer: critic (Opus), 13.11.2026. One pass for one topic (R13-g). Subject: `origin/wip/oh3-36` @037ad2f and
`origin/wip/oh5-11` @56679c3, both from `origin/main` 00f0193. Spec: `docs/tasks/specs/t-203-native-context-long-root.md`.
Plan review: `docs/tasks/specs/reviews/t-212-t-203-plan-review.md`. Rule text: `docs/tasks/critic-diff-brief.md`.

## Verdicts (input to the Lead's acceptance; the decision is the Lead's)

- **Part A (OH3-36): ACCEPT WITH FIXES.** Fix A-1 blocks the merge, A-2 goes with it, A-3 is a request for the mechanical layer.
- **Part B (OH5-11): ACCEPT WITH FIXES.** Nothing in the code blocks. B-1 (the AR line) is fixed before the merge.
  B-2/B-3 are Lead queue work that the spec makes a precondition of acceptance.
- **Ratchet (AR-20, `blocking_per_role` +1 x13): ACCEPT the raise.** Details in Q2.

## Findings

### A-1 — BLOCKS (Part A). The pass door tells the orchestrator to record `--block "*"`, which waives every dispatch block of that stage

`inject_context.py:487-488`: `PASS_DOOR.format(hint=waiver_hint(ticket, stage, NATIVE_PACKET_PASS_MATCH))`.
`stage_guard.waiver_hint` (`stage_guard.py:792-798`) does not quote the message it gets. It calls `block_match(message)`
(`:782-786`), which returns a phrase from `BLOCK_MATCHES` (`:778-779`) or `"*"`. `"could not be written"` is not in
`BLOCK_MATCHES`. I ran this against the branch code (oh3-36 worktree):

```
Your word passes this: `waiver.py --task T --stage S1 --block "*" --words-file <file>`.
*
```

Failure scenario: a native launch at stage S5 is refused with this line. The orchestrator follows the door as printed, so
the record is `stage_overrides[] {stage: S5, match: "*"}`. `split_overridden` passes every line on a `*`
(`waiver.py:217`). From then on, while the record stands, it also passes every stage_guard dispatch block on S5:
"required stages are not done", "gate A is not approved", the tracker route, and so on. The person agreed to "start
without the factory context" and ends up waiving every block of the stage. This breaks invariant I-C ("a person's word
passes only the line it names", spec A.6), the registry row's own text (`refusal_registry.py`, row
`IC-native-packet-unwritten`: `--block "could not be written"`) and D2a. The error is toward a silent over-pass. A second
effect: the driver copies `--block` names from a refusal's door into `standing-refusal.json` `doors`
(`driver_conductor.py:586`, `waiver.door_blocks`), so the line's own name never reaches waiver's check. With other lines
standing at the stage, `waiver.py --block "could not be written"` then reads `unmatched` and refuses (`waiver.py:716-724`),
which pushes the orchestrator toward `*` again.

Origin: the spec. A.2.1 prescribes `stage_guard.waiver_hint(ticket, stage, "could not be written")`, and t-212 missed that
`block_match` returns `*`. The builder followed the spec. The test did not catch it: A5b checks only the prefix
`'waiver.py --task T --stage S1'` (`test_doctor_context.py:330`).

Fix (the Lead widens the owns by one data row in a hot file, the function list being `BLOCK_MATCHES` only):
add `"could not be written"` to `stage_guard.BLOCK_MATCHES` (`stage_guard.py:778-779`). This is the one road for a
dispatch block's door name, and it is a data row. Nothing in `stage_guard.py` contains "could not be written", so no
existing message changes its match (Grep over `scripts/*.py`, -i: the hits are in `bug_records`, `claim_projector`,
`controller`, `cost_capture` and `delivery_summary`, none in `stage_guard`). In A5b, assert
`'--block "could not be written"'` in stderr for the `revoked`/`other_stage`/`no_pipeline` rows, so the test can catch this
defect. Rejected alternative: building the hint in `inject_context` with `person_words.door` would add a second hint
builder (item 6).

### A-2 — fix before merge (Part A, tests). A5b cannot catch A-1 as written. It is covered by the A-1 fix above, and listed separately so it is not dropped.

### A-3 — request (Part A, mechanical layer, rule 7). No Part A witness was attached

The dispatch says the layer is "in the commit and its report". The commit message carries the AR, judgment and census
lines but no run output, and no report was given to me. Missing: the `scenario_walk.py --witness-for <Part A owns>` runs,
`test_judgment_census.py` (which proves +1 x13 is what the test computes and that `unwritten_facts`,
`_said_write_failure` and `ambiguous_once_key` are not uncounted units), `test_codex_host.py`, `refusal_registry.py
--check` with its exit code, `selftest --lang`, and the `151` grep with its positive control. My one control re-run
covers `test_doctor_context.py` (green, below). It does not replace the rest. The coordinator should attach the builder's
verbatim tails or the branch's `forge-check` before accepting.

### B-1 — fix before merge (Part B). The `architecture:` line drops AR-15

The spec's acceptance key is `architecture: AR-15, AR-13 -- worker_lifecycle calls hooklib.artifacts_dir(root=) at all
three sites`. The commit (56679c3) has `architecture: AR-13 -- one artifacts_dir reader`, and AR-15 (one survivor wired
everywhere) is the invariant the node exists for. Amend the message at merge time. Also: the commit says `tier: sonnet`
but its trailer is `Co-Authored-By: Claude Opus 5.5`. The coordinator should reconcile this (calibration check 4); it is
not a code finding.

### B-2 — Lead queue, a precondition of acceptance (spec §4 "Copies"). The new onboarding-hooks node is not opened

The spec says "The Lead opens that node (finding + batch row) before Part B is accepted." On `origin/main`,
`plans/piles/onboarding-hooks/` has batches 1-5 and its last node is OH5-15. Grep `is_one_component|one-component|one path
component` -i over that pile returned nothing. Positive control: the same Grep shape over the pile finds `OH5-11`
(`batch-5-...md:39`). Until the node exists, the eight copies are "queued" only on paper.

### B-3 — Lead queue (class). Two copies the spec's grep could not see (see Q3, "missed")

## Questions

**Q1. Fit to the spec, edges included.**
Part A:
- Root limit: `NAME_HEX` 32, `PACKET_ROOT_LIMIT` 119 and `SUPPORTED_ROOT` 119 are unchanged or added as specified. A1
  pins 119→259 and 120→260; unnamed 152→259.
- F-1 informed pass: implemented through `waiver.split_overridden`, `journal_override`, a stderr line, `return`, and no
  denial row. A launch with no carrier (no ticket, no stage, no pipeline) has no pass. The door text is wrong (A-1).
- F-7/F-9: each guard wraps ONE call and sits before `context_output`. The context goes out in every case. One stderr
  line plus a `person_signal(kind inject)` with no once_key. Both-fail gives two lines and two signals. A8/A8b assert all
  of this.
- F-4: once per role per name set; A9 asserts it, with the flag unlinked before and after.
- Q-2: the only reader is the run report. No doctor reader was added (Grep of the diff: no `doctor` hunk).
- `except OSError` sits before `except ValueError` inside `dispatch`. A passed refusal returns to `sys.exit(0)` and a
  refused one exits 2 inside `block` (traced at `inject_context.py:702-710`).
- `unwritten_facts` reads the normalised slot, so `\\?\`, `\\?\UNC\` and `//?/` are covered, and POSIX has no limit.
- A6/A7 open the door end to end.
- Builder decisions the spec left silent: the `NATIVE_PACKET_PASS_MATCH` constant (fine, but see A-1) and a try/except
  around `print` in `_said_write_failure` (safe).

Part B:
- `artifacts_dir(ticket, event=None, root=None)`: the body and the component check are as the spec gives them.
- All four `worker_lifecycle` sites now call it with `root=root`: the copy in `binding_is_active` and the call sites at
  `:115`, `:156` and `:210`.
- Each edge keeps its error direction: in `binding_is_active` a bad ticket is a `ValueError` and returns True. In the stop
  branch the existing handler sets `allowed=None`, so the stop is denied.
- `covers` gains `worker_lifecycle.py`.
- B1-B5 kill the defect: B3 fails on the old code (event None resolves under cwd), and the B4/B5 spies record the `root`
  kwarg.
- Test doubles: I re-grepped the doubles of `artifacts_dir` under `scripts/tests/`. All of them rebind a module-local
  name (`SG.`, `SJ.`, `PBC.`, `RS.`, `run_suite.`, `E.`, `GB.`, `guard_app_under_test.`), except
  `test_read_json.py:624`, which rebinds `hooklib.artifacts_dir` for `environment_record._story_context`, a path that does
  not reach `worker_lifecycle`. So no double without `root` runs where `worker_lifecycle` calls the survivor. The
  builder's claim holds.

**Q2. Ratchet raise (AR-20): ACCEPT.**
- One new blocking unit, `inject_context.refuse_native_packet`. It is class `shape`, owner `data`, and has the same 13
  roles as the `collect_blocks` row it sits beside.
- Each key goes up by exactly +1: qa-automator 167→168, qa-bug-reporter 133→134, qa-case-critic 158→159,
  qa-case-designer 133→134, qa-code-critic 132→133, qa-doc-scribe 133→134, qa-failure-analyst 134→135,
  qa-requirements-tester 151→152, qa-retro-analyst 133→134, qa-runner 134→135, qa-scout 133→134,
  qa-test-strategist 165→166, conductor 472→473.
- The commit message names every key old→new with the reason "silent pass made a refusal (t-203)". The diff matches it
  digit for digit.
- Justified: it turns a silent no-context launch into a refusal with a door and a pass (FR-4, AR-28). No class was lowered
  and no `blocks_override` was added.
- Not yet witnessed: that `test_judgment_census.py` computes this and nothing else (A-3).

**Q3. Class-wide completeness (SIBLING_MAP; my Grep `c in \w+ for c in|"/\\\\:"` -i over `scripts/*.py`, oh5-11 tree;
positive control: the survivor `hooklib.py:236` is found).**
- Covered: `worker_lifecycle` (the copy plus three call sites, the stop branch included). Native delivery chain: packet
  stage → refusal; binding `record` and packet rewrite → guarded (F-7/F-9); ambiguity → signal.
- Queued in the spec, but the carrier is not written yet (B-2):
  - one-component copies: `host_dispatch.py:21`, `exit_gate.py:209`, `stage_guard.py:436/643/717`,
    `activity_capture.py:44`, `cost_capture.py:1907/3800`;
  - F-2 (the shared `_publish` temp suffix), F-6 (the unregistered native `ValueError` refusals), and the "uncapped path
    components" finding;
  - the axis 8 row for `artifacts_dir(root=)`, which the spec assigns to the Lead.
  - A Grep for `uncapped|F-2|temp suffix|_publish|unregistered native` over `plans/piles/onboarding-hooks` on origin/main
    found nothing. Positive control: `OH5-11` is found in the same pile.
- Missed:
  - `recover_codex_usage.py:16`: `any(c in session for c in '/\\:')`. It is single-quoted, so the spec's double-quoted
    grep (`"/\\\\:"`) could not see it. It also lacks the `.`/`..` guard, so a session id of `..` passes it. It belongs in
    the new node.
  - `hooklib.py:282` `is_story_folder`: a stricter twin (`"/\\:\0"`, a strip check) inside the survivor's own file. Give it
    a verdict in that node: either it calls `is_one_component` plus its own extras, or it is documented as the axis 8 leaf.
  - Surface walk (rule 14), encoding/quoting class: the grep's quote form was the blind spot. The node's detector should
    match both quote forms.

**Q4. Duplication and consistency (item 6).**
- `_said_write_failure` is one handler for both deliver writes (C-12), so there is no copy.
- The pass reuses the existing readers: `waiver.split_overridden`, `stage_guard.journal_override` and `waiver_hint`.
- Part B removes a copy.
- `NATIVE_PACKET_UNWRITTEN.format(**parts)` is evaluated three times (`inject_context.py` split/note/block). The A24 key
  needs only the `block(` form, so `note_denial` and `split_overridden` could take one local `message`. Severity: queue
  (cosmetic; the spec prescribed this form).
- Otherwise none found: I grepped `def .*unwritten|write_path_length|TEMP_NAME_EXTRA|PATH_LIMITS` over `scripts/` (only
  the new definitions) and the `artifacts_dir` doubles listed above.

**Q5. Code quality (item 7).**
- No new function is over about 60 lines. `refuse_native_packet` is about 32 lines with nesting ≤2. `deliver` grows to
  about 58 lines (it was already about 45). That is acceptable; it could be split when OH5-10 touches it (queue).
- No dead branches. `facts["packet_limit"]` is read by no text, only by A4; the spec requires it (it stays).
- `DELIVER_WRITE_FAILED`'s tail, "a shorter folder or long paths fix it", is printed for the F-9 rewrite too, which the
  spec says is never a length failure. The text is the spec's own; queue a wording tweak.
- Severity of all three: queue.

**Q6. Architecture and judgment.**
- AR-13: kept. Part B goes through the one reader. Part A reads overrides only through `split_overridden`.
- AR-9: kept. The refusal names its cause, its door and its owner, and the A24 row is in the same commit. The door's pass
  text is wrong (A-1).
- AR-28: kept. An `OSError` can no longer reach `main`'s fail-open handler. `refuse_native_packet`'s own calls
  (`live_stage_overrides`, `names_whole`, `journal_override`) are documented never-raise or best-effort.
- AR-20: named (Q2).
- AR-15: kept, but not named in Part B's commit (B-1).
- P27 / AR-29: no meaning is judged. The new unit judges the presence of a write failure and of a recorded word. The
  match is the existing `names_whole` predicate. The census class `shape` is honest.
- ONE ROAD (P31, item 12): no exclusion. `PATH_LIMITS` is a platform row with a default that only chooses the text, and
  every OS takes the same refusal road. Grep of the diff for language or project names: none.

**Q7. Merges.**
- `git merge-tree --write-tree` gives a clean tree for oh3-36 × oh5-11 (`29c8967`), main × oh3-36 (`2541259`) and
  main × oh5-11 (`6d36be6`).
- `git diff --stat 00f0193 origin/main -- ai-packages/` is empty, so main has not moved under the package.
- Semantic seam: Part A's `refuse_native_packet` calls `artifacts_dir(ticket, event)` with no `root` (event project =
  root here), which is compatible with Part B's signature. The A-1 fix touches `stage_guard.py`, which neither branch owns.

## Trail

Read:
- the spec (whole) and t-212 (whole);
- `critic-diff-brief.md`;
- both diffs in full (`git diff 00f0193 origin/wip/oh3-36`, `.../oh5-11`) and both commit messages;
- branch files:
  - `inject_context.py` 640-720;
  - `native_context.py` 36-230;
  - `stage_guard.py` 778-804 and 935-947;
  - `waiver.py` 202-222, 355-420 and 690-735;
  - `contract.py` 132-171;
  - `test_read_json.py` 605-650;
  - `hooklib.py` 268-290;
  - `recover_codex_usage.py` 10-22;
- `docs/SIBLING_MAP.md` axis list and axis 8;
- `tools/critic_verdict.schema.json`.

Reruns:
- `python -B -c` probe of `stage_guard.waiver_hint('T','S1', NATIVE_PACKET_PASS_MATCH)` and
  `block_match('could not be written')` in the oh3-36 worktree. Output quoted in A-1.
- `python -B -m pytest .claude/worktrees/oh3-36/.../tests/test_doctor_context.py -q` → `27 passed, 32 subtests passed in
  220.16s`.
- `refusal_registry.py --check` (oh3-36). The tail printed the registry listing with no failure line. Its exit code was
  masked by the pipe, so this is not proof of exit 0 (A-3).
- `scenario_walk.py --witness-for <Part B owns>` → 85 lines (keep rows of every hooklib reader). The builder ran 6 files
  plus selftest. Per PROJECT.md p.2 the remainder is CI's, so the branch's CI result belongs with the acceptance.
- `git merge-tree` ×3 (above).
- Greps with controls are as cited in Q3, B-2 and Q4.

Not done: no re-run of `test_resolver.py` (Part B's tails were attached and are consistent with the diff: B1-B5 are the
new rows and the red-first `TypeError ... 'root'` matches the old signature).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "A-1 (Part A): inject_context.py:487-488 builds the pass door with stage_guard.waiver_hint, whose block_match returns '*' for 'could not be written' (not in BLOCK_MATCHES, stage_guard.py:778-779); measured: the door prints waiver.py --task T --stage S1 --block \"*\". Following it records a * override that waives every stage_guard dispatch block of that stage (breaks I-C, contradicts the A24 row and D2a); A5b only checks the prefix (test_doctor_context.py:330)."
  ],
  "class_completeness": "Covered: worker_lifecycle copy + 3 call sites incl. the stop branch; the native chain (stage refusal, binding and rewrite guarded, ambiguity signalled). Queued in the spec but not yet carried: the new onboarding-hooks node for host_dispatch:21, exit_gate:209, stage_guard:436/643/717, activity_capture:44, cost_capture:1907/3800 (no node on origin/main; control OH5-11 found), F-2, F-6, the uncapped-path finding, and the axis 8 row. Missed by the spec's double-quoted grep: recover_codex_usage.py:16 (single-quoted, no ./.. guard) and hooklib.py:282 is_story_folder (stricter twin); both go to the new node.",
  "fixes": [
    "A-1: add 'could not be written' to stage_guard.BLOCK_MATCHES (stage_guard.py:778-779; the Lead widens Part A owns by this data row) so waiver_hint names the line, not '*'",
    "A-2: test_doctor_context.py:330 also asserts '--block \"could not be written\"' in stderr for the refused rows that print the pass door",
    "A-3: attach Part A's verbatim mechanical layer (scenario_walk --witness-for runs, test_judgment_census.py, test_codex_host.py, refusal_registry.py --check exit code, selftest --lang, the 151 grep with control) or the branch forge-check",
    "B-1: Part B commit message: architecture line becomes 'AR-15, AR-13 -- worker_lifecycle calls hooklib.artifacts_dir(root=) at all three sites' (spec key)",
    "B-2: the Lead opens the onboarding-hooks node for the one-component copies (spec precondition of Part B acceptance) and adds recover_codex_usage.py:16 and hooklib.py:282 to it; files F-2, F-6 and the uncapped-path finding; adds the axis 8 row",
    "Queue: format NATIVE_PACKET_UNWRITTEN once into a local message for note_denial and split_overridden; DELIVER_WRITE_FAILED tail wording for the F-9 case"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/t-203-native-context-long-root.md",
      "docs/tasks/specs/reviews/t-212-t-203-plan-review.md",
      "docs/tasks/critic-diff-brief.md",
      "git diff 00f0193 origin/wip/oh3-36 (all 7 files)",
      "git diff 00f0193 origin/wip/oh5-11 (all 5 files)",
      "ai-packages/qa-factory/scripts/inject_context.py 640-720 (oh3-36)",
      "ai-packages/qa-factory/scripts/native_context.py 36-230 (oh3-36)",
      "ai-packages/qa-factory/scripts/stage_guard.py 778-804, 935-947",
      "ai-packages/qa-factory/scripts/waiver.py 202-222, 355-420, 690-735",
      "ai-packages/qa-factory/scripts/contract.py 132-171",
      "ai-packages/qa-factory/scripts/hooklib.py 268-290 (oh5-11)",
      "ai-packages/qa-factory/scripts/recover_codex_usage.py 10-22",
      "ai-packages/qa-factory/scripts/tests/test_read_json.py 605-650",
      "docs/SIBLING_MAP.md axis list and axis 8",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "python -B -c (oh3-36) stage_guard.waiver_hint('T','S1',inject_context.NATIVE_PACKET_PASS_MATCH); stage_guard.block_match('could not be written')", "result": "Your word passes this: `waiver.py --task T --stage S1 --block \"*\" --words-file <file>`. / *"},
      {"command": "python -B -m pytest .claude/worktrees/oh3-36/ai-packages/qa-factory/scripts/tests/test_doctor_context.py -q", "result": "27 passed, 32 subtests passed in 220.16s"},
      {"command": "python -B refusal_registry.py --check (oh3-36), piped to tail", "result": "registry listing, no failure line; exit code masked by the pipe"},
      {"command": "python -B scenario_walk.py --witness-for <Part B owns> | wc -l", "result": "85"},
      {"command": "git merge-tree --write-tree oh3-36 x oh5-11; main x oh3-36; main x oh5-11", "result": "clean: 29c8967, 2541259, 6d36be6; main has no ai-packages change since 00f0193"}
    ]
  }
}
```

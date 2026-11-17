# t-946 — topic critic: Architect streams B, C, D, E, F (spec 20261116-architect-tier)

Critic (Opus), 17.11.2026. One topic gate (R13-g) over five STAGED diffs (`git -C <wt> diff --cached`), all on base
169f4046. Main has moved since (cfe418b6), but none of the files owned by B-F changed there (checked with
`git log 169f4046..HEAD --name-only`). Worktree paths below are shortened: `wt-B` = `.claude/worktrees/agent-af32948f64703e15e`,
`wt-C` = `agent-a45e4804c9d4e3e05`, `wt-D` = `agent-a405ea232608187a5`, `wt-E` = `agent-a2c103ab55cd4d3df`, `wt-F` =
`agent-a27e965d90cc34002`.

## Verdicts

| stream | verdict | blocking |
|---|---|---|
| B (t-935) | fix | B-1, B-2 |
| C (t-936) | accept with minor fixes | — |
| D (t-937) | fix | D-1 |
| E (t-938) | accept with minor fixes | — |
| F (t-939) | fix (one text depends on B-2; one small divergence) | — (F-1 is resolved by B-2) |
| **topic** | **NEEDS WORK (fit_with_fixes)** | B-1, B-2, D-1 |

Whether to accept is the Lead's call (rule 6). This file proposes; it does not decide.

## Findings

### Blocking

**B-1. Two old matrix tests read the live config and turn RED when stream L flips it** (TEMPORAL; spec 3.4, rule 11 (i)).
`wt-B/tools/test_journal_validator.py:799-809` (`test_matrix_designer_accepted_by_opus_without_basis_fails_equal_tier`) and
`:848-861` (`test_matrix_designer_by_opus_critic_basis_fails`) call `jv.decide(staged, HEAD_TEXT, NOW)` without `config_text`.
The new default `_CONFIG_UNSET` reads `delegation.config.yaml` at the git root of the cwd, which is the live config. After L,
lead is opus, so opus ranks 3, which is above designer's 2, and the expected FAIL becomes a pass.
Proof: a scratch git repo holding the post-L config, then `( cd <scratch> && python -m pytest <wt-B>/tools/test_journal_validator.py -q )`
→ `2 failed, 330 passed` (exactly those two tests). On today's config the builder's witness is green. Stream L's own
witness ("the narrow sets of A-E re-run on the merged tree") would go red, and L owns no test files to fix it with.
The class: an in-process test that depends on whatever config the developer's tree holds. Fix: both cases are already rows
of `MATRIX_ROWS` (`today-designer-opus-bare`, and `*-designer-sonnet-critic-basis`). Delete the two functions and add the one
missing row `today-designer-opus-critic-basis`. Every remaining legacy test that calls `decide` without `config_text` needs
either `config_text=CFG_TODAY` or deletion (see N-B1). Severity: blocks merge.

**B-2. The INDEPENDENT CONTEXT detector is registered by a command that can never print it** (rule 10 (c); B4 (ii); check 6 (i)).
F writes check 6 (i) as "`python -B tools/journal_validator.py --all --base <sha>`" (`wt-F/PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:133`,
taken verbatim from spec 5.5). In B, `_run_all` → `_developer_file_result(..., drift=False)` →
`wt-B/tools/journal_validator.py:2369-2370` takes the branch `(*decide(..., drift=False), [])`: the warnings list is hard-coded
empty, and `matrix_warnings` is wired only into `decide_with_warnings` (the commit and write path) and `decide_merge`. So the one
calibration reader of the WARN gets nothing, and the detector check 6 (i) registers is dead.
The defect starts in the spec text and lands in B (the code) plus F (the command). Fix (B): in the `drift=False` branch also
collect `matrix_warnings(new_lines, head_lines, seed_lines=split_lines(seed_text))`. The WARNs do not depend on the clock, so
`--all` prints them through `_emit`. Add one row proving that `--all --base` prints an INDEPENDENT CONTEXT line. F's text can
then stay as it is. Severity: blocks merge (a mechanism with no live detector).

**D-1. A hook-copy list missed by D: `test_transcripts.py` goes red; `test_critic_snapshot.py` passes without testing what it claims** (Q6).
`dispatch_gate.py` now does a hard `import tier_ladder` (`wt-D/tools/dispatch_gate.py:1039-1044`).
`tools/test_transcripts.py:1360-1388` (`_alone(tmp, "dispatch_gate.py")`) copies dispatch_gate on its own and imports it.
In wt-D: `python -m pytest tools/test_transcripts.py -q -k alone` → `1 failed, 1 passed`
(`ModuleNotFoundError: No module named 'tier_ladder'`). Control on main, same command → `2 passed`.
`tools/test_critic_snapshot.py:476-484` (`_write_isolated_copy(with_dispatch_gate=True, broken_decide=True)`) still passes, but
the copied dispatch_gate now fails at import before `decide()` is ever reached. So
`test_dispatch_gate_decide_raises_fail_open_snapshot_written` silently became a second copy of the "missing sibling" case.
Fix: copy `tier_ladder.py` in both places, as D did in its three copy lists. Neither file is in any stream's owns: the Lead
adds them to D's fix-round owns. Severity: blocks merge (red CI on main).

### Fix this round, not merge-blocking

**B-3. The generated AGENTS.md "Journal note" is stale and no one owns it** (`wt-B/tools/agents_md.py:260-267`).
After B, it still says "`TIER_ORDER` of `tools/journal_validator.py`" (that name is deleted), "for a leaf, `judge`" (the
validator now refuses that basis), and "the tier word of the FUNCTION level your model serves" (wrong under F4-A: `by` is the
session's model-family word). The builder left it so that `--check` stays clean. Stream L only REGENERATES AGENTS.md; it does
not edit `agents_md.py`. So the stale text survives L. Fix: B's fix round edits the text (`FAMILIES` of `tools/tier_ladder.py`,
no judge, "the model-family word of the accepting session") and regenerates AGENTS.md in the same commit (AGENTS.md goes into
B's owns). The other option is to add this one line to L's edit list explicitly. Either way it must not stay unowned.

**N-B1. Duplication: about 22 per-cell legacy matrix tests are already covered by the new table** (brief items 6 and 5; TESTING.md: one parameterised test per behaviour).
`wt-B/tools/test_journal_validator.py:499-861` (`test_matrix_*`, `test_pair_*`, `test_unknown_by_*`): each one repeats a
`MATRIX_ROWS` cell (`:880-940`). Removing them fixes B-1's class and B's volume (V-B).

**V-B, V-C, V-E. Test volume (rule 20).** Added lines (staged numstat, the `tools/test_volume.py` classes):
B has 256 test lines against 253 product lines, C has 163 against 138, E has 50 against 27. No handoff names a `tests-over:`
reason. Fix: for B, N-B1 brings it well under. For C and E, either a `tests-over:` line in the Lead's commit with a reason that
holds (E: the spec itself demanded an 11-row adversarial table; C: four item tables plus the 25-line-cut test), or a trim.

**Q7 / N-D2. Dead code in `journal_echo`: the `basis == "judge"` silencing** (confirmed).
`tools/journal_echo.py:2201-2202` (`if basis == "judge": return None  # S4`), comment block `:1994`, tests
`tools/test_journal_echo_r3.py:175-185` and `:555`. The writer refuses judge before the write (B, `journal_write` validates).
A hand-written judge line is also reported by `journal_echo`'s own `decide` call at `:2547`. So S4 only silences an echo on a
line that is already FAILing. No stream owns `journal_echo.py` (D's non-goals exclude it). Proposal: D's fix round (axis 14
neighbour of `tier_echo`), with owns += `tools/journal_echo.py` (S4 branch and comment) and `tools/test_journal_echo_r3.py` (two
rows deleted). If the Lead prefers, it can be a node row in the untaken batch 7 instead.

**N-E1. Neighbouring case class: a case-variant path bypasses E's refusal** (rule 14; surface: E's python-program recogniser).
Probe in wt-E/tools: `_worker_verdict_call("python TOOLS/journal_write.py accept --task t-1")` → `False`, and
`"python tools/Journal_Write.py accept"` → `False`. On Windows (a case-insensitive filesystem) both invoke the real writer.
`wt-E/tools/hygiene_gate.py:1493` compares the program path case-sensitively. Fix: `.lower()` the program before comparing,
plus one row. Error direction: the spec allows false refusals and forbids passes. Other neighbours walked: backslash, `./`,
quoting, `cmd /c "..."`, a second segment, and an upper-case verb all refuse (`ACCEPT` is a harmless false refusal). Indirect
forms (`python -c`, script files) are the spec's stated residual.

**Q4 / N-E2. The private import `dod_track._PYTHON_PROGRAM_RE`** (`wt-E/tools/hygiene_gate.py:1491`).
The spec's edge allowed "a scan of ALL matches with the same regex", and the builder stated its choice. So this is within the
spec. Breakage is not silent: a rename raises AttributeError, `decide` fails open with a visible message, and the 11 deny rows
of `test_hygiene_gate.py` go red. Also, lines `:1492-1493` repeat the body of `dod_track._is_journal_writer_call` (`dod_track.py:238-242`).
Recommendation (not blocking): give `dod_track` a public `python_programs(command)` generator that yields normalised program
paths, and have both callers read it. That is one edit in `dod_track.py`, outside every owns, so it goes into the small-work
batch with the Lead as owner. Until then, the private import is acceptable.

**F-1 (= B-2).** The check 6 (i) command is correct once B-2 lands; no edit to F is needed then.

**F-2. ARCHITECT_START step 5 uses the wrong start date** (`wt-F/PROCESS/ARCHITECT_START.md:28-29`).
F says "none yet means the date of the commit that landed this checklist". That is F's own commit. Spec 4.5 step 5 says
"the date of stream L's commit", and F's own check 49 leak line says "after the Architect landing". Depending on merge order,
F's wording pulls B-E (already reviewed by this gate) into the first review, or drops them from it. Fix: "the date of the
stream-L commit (the Architect landing)".

**F-3. `D-nnnn` placeholders** in `wt-F/docs/ADOPTION_LEDGER.md:4,23,52,77,144`. Stream L must fill them. L's edit list (spec §7 L)
does not name ADOPTION_LEDGER. Add it to L's list.

### Minor (queue or this round, Lead's choice)

- `wt-B/tools/journal_validator.py:268`: `JOURNAL_PATH ="logs/routing-log.jsonl"`, a whitespace edit on a line the stream had
  no reason to touch.
- B: stale prose saying `TIER_ORDER`, `AGENT_TIER` or judge-for-leaf in validator rule-2 text and in test comments (the
  builder listed them).
- C: `wt-C/tools/session_context.py:1024` re-derives the 64 KB cap (`cap: int = 65536`). The home has `tier_ladder.MAX_CONFIG_BYTES`.
  Read it from there (AR-13).
- C: no TODAY-world row. Add `claude-fable-5-2` against today's config → `function lead (family match: claude-fable-5-1) ...
  architect = unbound`. The between-families render `<f> (unbound family)` has no row either.
- C: before L (no architect bound), a Lead session whose calibration is overdue is told to call an Architect that does not
  exist (`:611` suffix). The spec does not cover this world. Today's last `calibrated` is 2026-11-12, so the suffix appears from
  2026-11-20 if L has not landed by then. Low severity. One possible fix: when `architect_binding` is None, use a "run the
  calibration" suffix.
- C: in the "above lead, no architect binding" case, the ARCHITECT line is suppressed but the calibration suffix is still the
  Architect variant (`session_function` returns `architect`). Small inconsistency.
- D: `family_of` scans weakest-first, while the old `dispatch_gate._model_family` scanned strongest-first. An id holding two
  family words now resolves differently, and `mythos` is now recognised in dispatch_gate. Neither case is realistic, and
  neither feeds a rank gate. Recorded, no fix.

## Answers to the dispatch questions

1. **Fit.** B: B1-B7 done, with the order of 3.1 kept (enum → judge → ok_rank → floor → critic → queued band → generic).
   Traced `_matrix_d0058_violation`, and probed `tier_ladder` on the live config: haiku -1, sonnet 1, opus 2, fable 3,
   `claude-fable-5-2` → lead (family match). This matches spec 3.4. The builder's four choices:
   (1) the `_warn_line` shape: ACCEPT (AR-18, one WARN shape). F's check 6 searches for `INDEPENDENT CONTEXT`, which matches.
   The Lead should amend the spec literal.
   (2) `reviewed_through: null` counts as absent: ACCEPT (the `via`/`session` convention). The writer drops None
   (`journal_write._lead_obj:754`).
   (3) An absent config is silent: ACCEPT. It is safe: after L, the defaults make acceptance stricter, never looser. Temporary
   test repos would otherwise WARN on every write. The spec's 2.4 wording needs a line from the Lead.
   (4) The agents_md text left untouched: NOT acceptable as a silent residual, see B-3.
   C: C1-C4 done. The ASCII deviation is justified (pinned cp1252 tests). D: D1-D4 done. It deviates from "no test edit" out of
   necessity, but is incomplete (D-1). E: every DoD row is present. F: F1-F6 done, apart from F-2.
2. **TEMPORAL.** On live hooks between each merge and L: `tier_ladder.py` is already on main (stream A), so no self-activating
   file breaks the live session. Live config and settings are equal (`claude-fable-5-1` in both), so no pin WARN fires today.
   The breakages are in CI and tests: B-1 (red after L); D-1 (red at D's merge); and **B merged without D breaks 11 tests of
   `tools/test_journal_echo.py`**. Proof: in wt-B, `python -m pytest tools/test_journal_echo.py -q` → `11 failed, 113 passed`,
   with `journal_validator.py line 266: import tier_ladder ... ModuleNotFoundError` inside the hook copy. D's added copy entry
   fixes it, so the merge order matters.
3. **One reader of the ladder.** No stream re-derives ranks or bindings, apart from C's 64 KB cap (minor). The function names
   agree across B (`FUNCTION_RANKS`, `QUEUED_TO_LEAD_AGENTS`), C (`function_of_session`) and D (`FAMILIES`/`family_of`). F22 holds:
   B's ok_rank passes any higher-ranked acceptor (row `after-no-architect-key-fable-critic`). D and E carry no ranks. F's texts
   add no rule against F22 (the outage text belongs to L).
4. See N-E2: acceptable for now. A public helper is recommended. Its owner is the Lead, through the small-work batch, since
   `dod_track.py` is outside every owns.
5. C's ASCII line deviates from the literal of 4.6. The deviation is justified and stated (question 1 of C's handoff). F's texts
   do not quote the Russian phrase, and L's CLAUDE.md move says "tell the owner". Suggestion: drop the quotes, so that no session
   repeats an English literal to the owner, for example `-- overdue: suggest calling the Architect to the owner (...)`.
6. D's test edits are only the three copy lists (verified in its diff). Grep of the copy-list shape across `tools/test_*.py`
   (`"(journal_validator|tier_echo|dispatch_gate|journal_hooks|token_usage_stats|session_context|hygiene_gate|journal_echo|journal_write|mechanism_gate|savings_report)\.py"`)
   finds the missed copies: `test_transcripts.py:1386` and `test_critic_snapshot.py:484` (D-1). The positive control is the same
   grep finding D's own `test_journal_echo.py:1236`. No miss for journal_validator beyond `test_journal_echo.py`.
   `test_permission_audit.py:732` copies hygiene_gate, but E imports dod_track lazily, only inside `decide`, so that copy is safe.
7. Confirmed dead; see N-D2. Proposed: D's fix round.
8. Readers of deleted or renamed names, from `git grep -n -i -I` on the F tree and on main (excluding logs, specs, handoffs and
   snapshots). The positive control `session-handoff` gets hits in CLAUDE.md and SIBLING_MAP with the same shape.
   - `lead-queue-fable`: on the F tree, only `docs/tasks/lead-queue.md:7` (the rename note itself). Live specs: 
     `docs/tasks/specs/20261117-everything-in-piles-spec.md:44,46,362,702`, which already knows about the rename (its P16).
     No code reads the name.
   - `skills/onboarding`: `delegation.config.yaml:34,39,95-96` (L's list), `tools/test_wiring_check.py:487-526` (synthetic,
     unchanged by the spec), `plans/piles/forge/batch-3-exam-debts.md:17`, `plans/piles/forge/batch-7-vhodyashchie-4.md:73`
     (FG7-50) and `plans/piles/forge/findings/20261116-but-odna-tema-v-mnogih-mestah-kopii-pravil-ustareli.md:37`. The pile
     items that ask to edit the deleted skill are now moot; the Lead adds a line to L's batch-7 rows.
   - `next-task`: 0 hits on the F tree (control above).
   - Bare "onboarding" in `PROCESS/README.md:22,24` and similar places names the process, not the skill. Left as is.
9. Duplication: N-B1, N-E2 (body clone of 3 lines), C's cap. Code quality: B-1's class, the `JOURNAL_PATH` whitespace, and the
   C row expected value built through `.replace("claude-fable", "fable")` (`wt-C/tools/test_session_context.py` row
   `config-unreadable`), which is obscure but correct. No new function is over 60 lines. No expected value copied from the
   code's output was found: B's matrix rows, E's rows and C's rows come from spec 3.1, 2.4 and 5.4.
10. Axis blocks (the Lead writes them):
    - B: axis 1 (journal ↔ policy) and axis 34 (one road for the ladder). Axis 17 n/a (forge tool, not a package detector).
      Detector: check 6 (i)-(iii) and check 20 (b). Check 6 (i) is live only after B-2.
    - C: axis 1 and axis 34. Detector: check 49 (b) and check 5.
    - D: axis 14 (transcript readers `tier_echo`/`journal_echo`) and axis 34. No behaviour change. Detector: the existing test
      tables plus `test_tier_ladder.py`.
    - E: axis 1 and **axis 11** (a new shell-command recogniser in `hygiene_gate`, which the map already lists as queued for the
      walker; extend that queue line by this recogniser). Detector: check 49 (d).
    - F: axis 1, axis 2 (the Lead-exam row), axis 31 (two skill rows removed). Detector: check 49's own-leak line. critic.md:
      "exam not re-run: wording only" in the commit (critic.md rule 10).

## Merge order (recommendation)

**D → B → C → E → F → L.** D first: B's validator imports `tier_ladder`, and the `test_journal_echo.py` hook copy needs D's
entry. Without it, B alone leaves main with 11 red tests. B after its fix round (B-1, B-2, B-3). C and E are independent. F after
B, because F's check 6 (i) command is live only with B-2. F before L, because L fills F's `D-nnnn`. Each fix round runs in a
fresh worker (Cost gates). A re-review of B-2 only needs the fix diff and this verdict.

## Duplication and consistency (rule 18)
Findings: N-B1 (legacy per-cell tests repeat `MATRIX_ROWS`), N-E2 (`dod_track` program extraction repeated, private import),
C's 64 KB cap re-derived. Searched: the copy-list grep above; `TIER_ORDER|AGENT_TIER|LEAF_CATEGORIES|_matrix_d0058_violation|_line_form_violations`
over `tools/ ai-packages/ experiments/` (only agents_md stale text and the package's own unrelated `sizing.TIER_ORDER`);
`Lead tier = fable|Lead(top)|critic-tier|model_tier|-> tier ` across `tools/ PROCESS/ docs/ .claude/`, where only the files C
replaced matched.

## Code quality (rule 18)
Findings: the B-1 class, the `JOURNAL_PATH` whitespace, the obscure C expected value, the duplicated helper body (N-E2). No new
function is over 60 lines or nested more than 3 levels. Dead code: `journal_echo` S4 (N-D2).

## One road (rule 19)
None found. Searched for exclusions of a language, project or case in the five diffs: B/C/D/E branch only on function and
family names, which are data in `tier_ladder`. E adds a second python-invocation recogniser inside `hygiene_gate`
(axis 11). The spec chose it and the map already queues it, so it is not an exclusion. Axis-block line: see Q10, E.

## Tests (rule 20)
V-B, V-C, V-E (no `tests-over:` reason named). D is within budget. Killing power: B's rows would catch a wrong branch order
(the judge-at-fable and by-function-word rows). E's rows would catch a first-segment-only scan (the second-segment rows). C's
cut test would catch an ARCHITECT line placed after the cut.

## Not checked
- Stream A (on main; reviewed in t-922). Stream L (after this gate).
- Full sets, ratchets (`dup_ratchet`, `lint_ratchet`) and the BATCH CANON (CI's).
- `test_warn_messages.py` and `test_permission_audit.py` were not re-run (E's attached witness counts them).
- Spec premise 1: whether a subagent's Bash PreToolUse payload carries `agent_id` is still unmeasured. If it does not, E never
  fires: no false refusals, but no protection either. Check 49 (d) is the only net.
- `tools/test_mechanism_gate.py` closure tests are RED ON MAIN already (`usage_report.py` outside `MECHANISM_PREFIXES`; control
  run on main → 2 failed). This existed before these streams and is not caused by them. It needs its own node.
- Whether F's deleted skill texts held procedures still needed elsewhere. That was decided by F14; not re-judged.
- `PROCESS/CRITIC_EXAM.md` re-run for the critic.md wording edit.

## Trail

Read: the spec `docs/tasks/specs/20261116-architect-tier-spec.md` §2-§7 and the forks/decisions; `docs/tasks/critic-diff-brief.md`;
`docs/SIBLING_MAP.md` axis list and axis 11; the handoffs of t-935..t-939; the full staged diffs of all five worktrees;
`tools/tier_ladder.py` (`family_of`, `_effective`, `_resolve`, `function_of_session`); `wt-B/tools/journal_validator.py`
`_run_all` and `_developer_file_result` (2352-2546); `tools/journal_echo.py:2190-2210` plus the grep for judge;
`tools/dod_track.py:226-242`; `tools/hygiene_gate.py` (grep for recognisers); `tools/test_transcripts.py:1360-1388`;
`tools/test_critic_snapshot.py:470-570`; `tools/test_volume.py:1-40`; `.claude/settings.json:1-5`; journal grep of
`worker_ref` forms (1117 `agent:`, 1 `cli:`).

Reruns (verbatim tails):
- post-L config probe, B: `( cd <scratch repo with post-L config> && python -m pytest <wt-B>/tools/test_journal_validator.py -q -p no:cacheprovider )` → `2 failed, 330 passed in 6.95s`
- same probe, merge and node: `... test_journal_validator_merge.py test_journal_validator_node.py` → `211 passed in 22.97s`
- `( cd wt-B && python -m pytest tools/test_journal_echo.py -q -p no:cacheprovider )` → `11 failed, 113 passed in 21.79s` (`No module named 'tier_ladder'`)
- `( cd wt-D && python -m pytest tools/test_transcripts.py -q -p no:cacheprovider -k alone )` → `1 failed, 1 passed`; control on main → `2 passed`
- `( cd wt-D && python -m pytest tools/test_critic_snapshot.py -q -p no:cacheprovider )` → `26 passed` (one test now vacuous, D-1)
- `( cd wt-E && python -m pytest tools/test_mechanism_gate.py tools/test_streams.py -q -k "closure or import" )` → `2 failed, 12 passed`; control on main → the same 2 closure tests fail (`usage_report.py`), pre-existing
- E recogniser probe (python -c in wt-E/tools): `TOOLS/journal_write.py accept` → False, `Journal_Write.py` → False, `./tools/...` → True, `cmd /c "..."` → True
- `tier_ladder` on the live config: `bindings` = scout/builder sonnet-5-5, critic opus-5-5, lead fable-5-1; ranks haiku -1, sonnet 1, opus 2, fable 3

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B-1: wt-B tools/test_journal_validator.py:799-809 and :848-861 call decide() without config_text, read the live config, and fail after stream L flips lead to opus (proved: 2 failed under a post-L config)",
    "B-2: wt-B tools/journal_validator.py:2369-2370 --all --base path returns no warnings, so check 6 (i) (wt-F WEEKLY_CALIBRATION_PROTOCOL.md:133) can never list INDEPENDENT CONTEXT WARNs: a dead registered detector",
    "D-1: tools/test_transcripts.py:1360-1388 copies dispatch_gate.py without tier_ladder.py and goes red after D (control green on main); tools/test_critic_snapshot.py:476-484 now passes without testing the decide-raises case"
  ],
  "fixes": [
    "B-1: delete the two legacy tests (covered by MATRIX_ROWS), add the row today-designer-opus-critic-basis, pin or delete every other decide() call that depends on the config (N-B1)",
    "B-2: collect matrix_warnings in the drift=False branch of _developer_file_result and add one row that --all prints INDEPENDENT CONTEXT",
    "B-3: agents_md.py:260-267 Journal note text (FAMILIES of tier_ladder, no judge, model-family word) plus AGENTS.md regen in B's fix round, or an explicit line in L's list",
    "D-1: copy tier_ladder.py in test_transcripts.py _alone call and in test_critic_snapshot.py _write_isolated_copy (owns extended by the Lead)",
    "N-D2: delete journal_echo.py S4 judge silencing (:1994, :2201-2202) and test_journal_echo_r3.py rows :175, :555 in D's fix round, or open a batch-7 node",
    "N-E1: lower-case the program path in hygiene_gate.py:1493 plus one row (TOOLS/journal_write.py accept from a worker must be refused)",
    "V-B/V-C/V-E: tests-over reason in the commit or trim (B is resolved by N-B1)",
    "F-2: ARCHITECT_START.md:28-29 start date = the stream-L commit, not the checklist's own commit",
    "F-3: add docs/ADOPTION_LEDGER.md D-nnnn placeholders to stream L's edit list",
    "Merge order D, B, C, E, F, then L"
  ],
  "class_completeness": "Hook-copy class (axis: a tool gaining a hard import): D covered 3 of 5 copy lists, missing test_transcripts.py:1386 and test_critic_snapshot.py:484 (D-1); journal_validator copy only in test_journal_echo (D covered). Config-dependent in-process tests (B-1 class): 2 found by the post-L probe, merge and node files clean. Judge-basis class: validator refuses, journal_echo S4 dead (N-D2), agents_md text stale (B-3), check 20 updated by F. Shell recogniser (axis 11): E adds one more recogniser to the already-queued hygiene_gate line; case-variant neighbour open (N-E1). Deleted-name readers (F): only L-listed config comments, a synthetic test, and pile history remain.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261116-architect-tier-spec.md",
      "docs/tasks/critic-diff-brief.md",
      "docs/SIBLING_MAP.md",
      "docs/tasks/handoffs/t-935..t-939 (in the worktrees)",
      "staged diffs of wt-B, wt-C, wt-D, wt-E, wt-F",
      "tools/tier_ladder.py",
      "wt-B tools/journal_validator.py:2352-2546",
      "tools/journal_echo.py:2190-2210",
      "tools/dod_track.py:226-242",
      "tools/test_transcripts.py:1360-1388",
      "tools/test_critic_snapshot.py:470-570",
      "tools/test_volume.py:1-40",
      ".claude/settings.json"
    ],
    "reruns": [
      {"command": "post-L config scratch repo: pytest wt-B tools/test_journal_validator.py", "result": "2 failed, 330 passed"},
      {"command": "post-L config scratch repo: pytest wt-B test_journal_validator_merge.py test_journal_validator_node.py", "result": "211 passed"},
      {"command": "wt-B: pytest tools/test_journal_echo.py", "result": "11 failed, 113 passed (No module named tier_ladder)"},
      {"command": "wt-D: pytest tools/test_transcripts.py -k alone", "result": "1 failed, 1 passed; main control 2 passed"},
      {"command": "wt-D: pytest tools/test_critic_snapshot.py", "result": "26 passed (one now vacuous)"},
      {"command": "wt-E and main: pytest tools/test_mechanism_gate.py -k closure", "result": "2 failed in both (usage_report.py, pre-existing)"},
      {"command": "wt-E: _worker_verdict_call probes", "result": "case-variant program path not refused"}
    ]
  }
}
```

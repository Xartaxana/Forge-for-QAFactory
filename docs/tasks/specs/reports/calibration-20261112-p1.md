# Weekly calibration 2026-11-12 -- evidence layer, part 1 (checks 1-12), task t-087

First calibration of this repository. Gathered and reported only; nothing fixed, nothing written but this file.
Scripts used (read-only, scratchpad, not committed): `C:\Users\i_mas\AppData\Local\Temp\claude\b3e3188b390a00d9\f92520fc-f552-4e47-9d06-efbc3daae572\scratchpad\` -- `tx.py` (sessions and sidechains), `cmp.py` (journal vs sidechains), `owns.py` (owns/numbered items from dispatch prompts), `ovh.py` (Lead tool-call mix), `map.py` (SIBLING_MAP paths). Transcripts: `C:\Users\i_mas\.claude\projects\C--QAFactory-forge-repo` (3 main sessions, 95 sidechain files) and `...\C--QAFactory` (3 main sessions, no sidechains).

## Window

- File: `logs/journal/dev1.jsonl`. First `ts` 2026-11-05T14:29:30, last `ts` seen 2026-11-12T11:30:14 (the file grew while I ran: 219 lines at start, 223 at the end; the 4 added are t-087..t-090 `delegated`).
- Local time is UTC+1 (git commit stamps `+0100`; journal `ts` is local, transcript `timestamp` is `Z`). The journal has NO event between 2026-11-05T20:01 and 2026-11-11T20:58 (a 6-day gap), while git has 18 commits in that interval.
- Command: `python -c "...Counter(e['event'] ...)"` over the file ->
  `{'journal_created': 1, 'dispatch_skipped': 14, 'delegated': 106, 'accepted': 82, 'defect_found': 6, 'rejected': 14}` = 223 events; `calibrated`/`lead_degraded`/`lead_restored`/`escalated`: 0 of each.
  By agent: builder 135, critic 34, scout 25, designer 24, lead 1 (first run; before the last 4 lines).
- Hooks live: `git config core.hooksPath` -> `C:\QAFactory\forge-repo\.githooks`; `ls .githooks` -> commit-msg, post-merge, pre-commit, pre-merge-commit, pre-push.
- Sessions found (usage records + transcripts; main chains): `07782f25` 2026-11-05T15:06Z-15:07Z claude-sonnet-5-5 (32 turns, setup/CI read); `fc171a1f` 11-11 18:23Z-18:37Z fable-5-2 (69 turns); `646c4aac` 11-11 18:47Z-20:09Z fable-5-2 (366 turns); `a3462969` 11-11 19:26Z-11-12 01:47Z fable-5-2 (746); `1624cb4a` 11-11 20:37Z-11-12 05:50Z fable-5-2 (833); `f92520fc` 11-12 10:12Z-10:30Z fable-5-2 (139, the session that launched me). `a3462969` and `1624cb4a` overlap (two Lead sessions in parallel).

## Summary of findings, by weight

1. Check 1 / 2 / 8: Lead session `646c4aac` (fable, 2026-11-11 19:47-21:09 local) did builder-class work itself -- 132 Bash, 23 Edit, 10 Write, 0 Agent calls -- editing `tools/test_quarantine.py`, `tools/mechanism_gate.py`, `tools/test_story_capture.py`, tests, PROJECT.md; the journal holds no `delegated`, no `dispatch_skipped` for it. Its commits (db96d9f ... 10b6f86, e.g. 14bd8a8 226 lines of tools code, 10b6f86 1448 lines) have no journal task, no `accepted`, no critic, no critic-waiver note.
2. Check 1(b): within-session recurrence with no repeat marker at all (0 of 14 skip events carry one): session a3462969 designer-skip class events #68, #77 (after #54); session 1624cb4a self-execution-"blocking" class events #192, #199 (after #163, session attribution of #163 ambiguous).
3. Check 1(c)/(d): of 33 first-attempt writing dispatches over the designer threshold (script count), 9 have neither a paired designer spec nor a `dispatch_skipped(designer)` (t-014, t-058, t-071, t-076, t-080, t-081, t-082, t-085, t-086; owns/numbered counts are a parse of the dispatch prompts); t-077 -> t-078 is a re-badged continuation of a rejected task under a new task_id (event 202 says "same node"). Designer share: 9 designer dispatches + 6 skips vs 33.
4. Check 11: boot budget 117229 / 120000 bytes WARN after the limit was raised 100000 -> 120000 (t-031; boot was 133737 B at 572ec23); WARN-layer density: SEARCH_RETURNED_NOTHING 56.1 %, WITNESS_ECHO 28.7 %, NOTES_LEN 21.8 % of their achievable populations; 24 journal notes exceed 300 chars.
5. Check 12: ~10 concrete paths in `docs/SIBLING_MAP.md` are dead (GitLab remnants `.gitlab-ci.yml`, `tools/test_ci_layout.py`; `experiments/driver-golden*`; `logs/routing-log.jsonl` still read by `tools/forge_metrics.py` per the map; wrong pile name; two wrong-base package paths); D-0045 exists in neither decisions file; the map grew 589 -> 637 lines since the import.
6. Check 6: t-073 (T-2, sidechain finished) has neither `accepted` nor `rejected` after 2.5+ hours of window and no `closes:` token; t-068 is closed only by a `closes:` token (event 215).
7. Check 7 / 4 / 5: journal events t-001..t-011 (2026-11-05) have no sidechain or Lead transcript on this machine -- not measurable, not provably phantom; the only 11-05 main chain is Sonnet (`07782f25`) with no repo edit; the lead binding id (`claude-fable-5-1`, delegation.config.yaml) differs from the actual id (`claude-fable-5-2`) in all Lead chains (same tier word).
8. Check 9: no "no neighbors:" line and no neighbor enumeration in any of the 57 findings files added since the import; class-naming journal events #98, #126, #200 carry no enumeration; 0 "new axis" lines anywhere.
9. Check 2 / 8 (ambiguous, Lead judgment): the critic waiver on t-028 (1242+/1933- CLAUDE.md rewrite, "byte copy of what the critic walked on the plan"); R13-g load: ten critic passes in the TD-11 topic; "axes: not a mechanism" waivers that may hide a duty change (be804ba, 47ff421, 14bd8a8, 4f43202).
10. Not findings, recorded as clean: check 3 (no task rejected twice; 12 retries on the same id; 0 escalations needed), check 4 (all 95 declared worker models equal the measured models), check 6 tiers (all `by: fable`), check 8 machine audit (0 mismatches, rc 0), check 11 sync dispatches (95 of 95 background).

---

## Check 1 -- Rules 1/2/8: silent self-exclusion
verdict: finding

evidence:
- Main sessions' tool mix (script `tx.py`, `python -B .../tx.py`): `646c4aac` and `fc171a1f` live in project dir `C--QAFactory` (read with an inline script, same fields): 646c4aac `Bash 132, mcp__ccd_turn__update_plan 29, Edit 23, Write 10, wrap_up 8, ToolSearch 3` -> no `Agent` tool call; fc171a1f `Bash 21, PowerShell 4, Read 3, update_plan 6` (CI reads, `winget install Python`, lint/dup ratchet runs; its only Edit/Write are 2 on `~/.claude/settings.json`, outside the repo). Sessions with dispatches: a3462969 `Agent 34, Edit 115`, 1624cb4a `Agent 59, Edit 111, Write 28`, f92520fc `Agent 8`.
- 646c4aac Edit/Write targets (inline script): `tools/test_quarantine.py` x4, `tools/test_test_quarantine.py` x2, `tools/mechanism_gate.py` x1, `tools/test_story_capture.py` x3, `ai-packages/qa-factory/scripts/tests/test-layers.json`, `test_walk_plan_fields.py`, `PROJECT.md`, four `plans/piles/*/batch-*.md`, one finding, plus scratchpad commit-message files msg2..msg9.
- Journal for its window (local 19:47-21:09): `python -c` over the file: no event with `ts` between 2026-11-05T20:01:?? (event 27, t-011) and 2026-11-11T20:58:42 (t-012 delegated, #28). Positive control: the same filter on 11-11T21:38..22:00 returns events #53..#55.
- Commits in that interval with no journal trace (`git log --since=2026-11-05T20:00 --until=2026-11-11T21:30 --format='%h %ad %s'`): db96d9f 19:57 (38+/47-, 26 files), 271e57d 20:05, 4f43202 20:22, 14bd8a8 20:30 (213+/13-, tools), 4d12e85 20:33, 483e664 20:37, 47ff421 20:19, 818b102, 30bcd6b, b695ec1 21:09, 10b6f86 21:10 (923+/525-); 5498318 18:40 (merge of the experiment line, 266453+/10982-, 1827 files). 18 commits, zero journal events.
- Transcript scan of Lead sessions for `Agent` dispatches vs journal (see Check 7): every launched dispatch in a3462969/1624cb4a/f92520fc has a journal `delegated`; the gap is only in 646c4aac/fc171a1f.

findings:
- Rule 8 / Rule 1: session 646c4aac (Lead tier, fable-5-2, 2026-11-11T18:47Z-20:09Z) self-executed builder-class edits of tools code and the mechanism gate (`tools/mechanism_gate.py`, `tools/test_quarantine.py`) with neither `delegated` nor `dispatch_skipped`. Commit 14bd8a8 even carries a `tier: fable` line. ambiguous: the two readings are (a) silent self-exclusion of builder work (violation), (b) integration/canon-repair of a merge ("first canon after the merge", db96d9f/271e57d/4f43202), which rule 8 may treat as deterministic/integration work needing no event -- but the edits to `tools/test_quarantine.py` (a new GitHub backend, 14bd8a8) and `mechanism_gate.py` are code, not script runs. The Lead judges.
- The six-day journal gap 2026-11-05T20:01 -> 2026-11-11T20:58: no `journal` carrier for 18 commits (and no `accepted` for any of them).
- fc171a1f (69 turns, no repo edit): not a finding, reads and environment setup only.

### (b) within-session recurrence of the same class
verdict: finding
evidence:
- Skip events (14), session attributed by the nearest `delegated` worker's sidechain directory (`cmp.py` mapping) and by `ts` against session windows: #2 (11-05, unattributed), #7, #20 (11-05, unattributed), #54, #68, #77 (a3462969), #116, #163 (?), #192, #199 (1624cb4a), #211, #212 (1624cb4a), #213, #214 (f92520fc).
- Marker grep: `re.search(r'repeat of class|second occurrence|repeat', notes, re.I)` over the 14 `dispatch_skipped` notes -> `[]`; positive control: the same pattern shape on the string "repeat of class" matches (control line printed True for the sibling pattern `resubmi` in the same run; the repeat-marker control was run on `'second occurrence'` -> match).
- Class "designer: edit is mechanical, a draft costs more than the edit", session a3462969, ts order: #54 21:57:46 (t-024, 7 files), #68 22:54:15 (t-031, four files), #77 23:09:48 (t-035, five test files). #68 and #77 are the second and third event of one class in one session; neither carries a marker.
- Class "Lead self-executed, blocking / integration", session 1624cb4a: #163 02:10:44 ("Self-executed, blocking": two one-line lint removals; note says it is a peer session's report, so it may belong to a3462969 which ran until 02:47), #192 02:55:18 ("Integration, self-executed"), #199 04:21:07 ("Self-executed in td11-cut, blocking the cut's commit"). #192 and #199 are second/third in the same session; no marker.
- #211 (selftest `--slow-tests --update`, b0f7079) and #212 (canon confirmation) in 1624cb4a are `dispatch_skipped` events for deterministic script runs/result records (the rule says a deterministic script run needs NO skip event; #212 does not describe a skipped dispatch at all).
findings:
- Rule 8 / calibration 1(b): #68, #77 (designer-skip class) and #192, #199 (self-execution class) are violations in their own right under the check's text (second-or-later same-class event, no repeat marker -> self-declaration failed). ambiguous: reason class is judged by the Lead -- "designer draft costs more than the edit" is the same reason three times; the self-execution trio differs in reason wording ("blocking" / "integration").
- #211/#212: event-kind misuse (ambiguous: harmless extra records, or noise that dilutes the skip stream). Lead judges.
- No within-session recurrence found in f92520fc (its two events #213 scout, #214 designer are different classes, first of each).

### (c) dispatcher threshold of the designer
verdict: finding
evidence:
- Method: for every builder `Agent` call, `owns:` block paths and numbered items parsed from the dispatch prompt (`owns.py`; the numbered-item count is a regex proxy and also counts DoD/edge lists); first attempts only (`attempt` absent). Command: `python -B .../owns.py`. Output (task, agent, owns paths, numbered items): t-014 (1,5); t-024 (7,4); t-028 (9,6); t-029 (6,0); t-031 (4,0); t-035 (5,2); t-038 (4,0); t-049 (17,0); t-054 (3,0); t-056 (4,0); t-057 (5,0); t-058 (3,0); t-060 (3,8); t-063 (2,6); t-064 (3,6); t-065 (9,3); t-066 (7,3); t-067 (7,3); t-068 (9,0); t-069 (8,0); t-070 (7,0); t-071 (3,3); t-073 (4,7); t-074 (2,6); t-076 (4,0); t-077 (15,5); t-078 (5,9); t-080 (7,0); t-081 (2,3); t-082 (3,3); t-084 (20,5); t-085 (3,4); t-086 (5,3) -> 33 first-attempt writing dispatches at or over the threshold (`>=3` owns paths or `>=3` numbered items).
- Designer carriers in the journal: `delegated(designer)`: t-013, t-023, t-025, t-026, t-027, t-030, t-041, t-042, t-043 (9, command: count of `delegated` with agent designer = 9); `dispatch_skipped(designer)`: events #7, #20, #54, #68, #77, #214 (6).
- Paired: t-024 (#54), t-031 (#68), t-035 (#77), t-028/t-029 (specs t-013/t-023), t-054/t-056/t-057 (specs t-041/t-042/t-043), t-084 (#214 plus spec t-027), and the TD-11 nodes t-038, t-049, t-060, t-063..t-070, t-073, t-074, t-077, t-078 by the four designer specs A-D (t-025, t-026, t-027, t-030; pairing by topic, not by task_id -- ambiguous whether a topic-level spec counts as "a paired designer dispatch before it").
- Unpaired by either reading: t-014, t-058, t-071, t-076, t-080, t-081, t-082, t-085, t-086 (9).
- TREND: designer dispatches 9 (+6 designer skips) against 33 over-threshold writing dispatches in the window = 0.27 (0.45 counting skips). First measurement -- no earlier run to compare; the next run decides "rising".
findings:
- Each of the 9 unpaired dispatches is a silent absorption of the designer function if the counts hold (t-014 five numbered items; t-080 seven owns; t-058/t-076 filing of findings, four paths; t-081/t-082/t-085/t-086 DoD lists of 3-4). ambiguous: several are small-work batches or one-file tests with long DoD lists (the regex counts DoD items), the "3 numbered items" clause of rule 2 is then triggered by the DoD list itself. The Lead judges which count.

### (d) the "resubmission = continuation" exception
verdict: finding
evidence:
- `delegated` with `attempt>=2` after a `rejected` under the same task_id: t-036, t-038, t-039, t-044, t-047, t-048, t-049, t-053, t-054, t-056, t-057, t-060 (12; command: list of `delegated` events with an `attempt` field) -- all under the same task_id, so a designer is not owed.
- Re-badged continuations under a NEW task_id after a `rejected`: t-013 (rejected, event #44) -> t-023 (designer, "Fix round ... under a fresh id (the critic's accepted closed t-013 in the validator's reading)", #45): it IS a designer dispatch, no designer pairing is owed. t-077 (rejected, failure_class tooling, event #194, 03:14:45, builder) -> t-078 (delegated #195, same ts, same worktree td11-cut, owns overlap with t-077's carriers; its `accepted` #202 says "closes:t-077 (the first apply, same node)"), no designer, no skip.
- Reverse leakage: `re.search('resubmi', notes, re.I)` over all 223 notes -> `[]`; positive control `bool(p.search('a resubmission'))` -> True. "no skip events of class resubmission".
findings:
- t-077 -> t-078: a rejected task re-badged under a new task_id with the same node, same worktree and adjacent ts; no `delegated(designer)`, no `dispatch_skipped(designer)`; t-078 owns 5 paths and 9 numbered items. By the check's text this is a leak of the exception. ambiguous: t-078's subject ("fix the tool, roll back, re-apply") differs from t-077's ("apply the cut"), and the Lead's reading may be that fixing the tool is new work.
- t-013 -> t-023 is the same pattern but a designer was dispatched, so no violation; recorded as the cause of two task_ids for one spec (event #45 says so).
- "no resubmissions" cannot be claimed for the window.

## Check 2 -- Rule 3: critic on large diffs
verdict: finding

evidence:
- `git log --since=2026-11-05 --numstat` summed per commit (command in the run): 91 commits, 34 with > 100 changed lines. Table of the code/policy-bearing ones and their critic coverage:
  - 32858bd (46 files, 24653+/22186-): `delegated(critic)` t-079 (+ topic passes t-045, t-055); covered.
  - 88e6d4d (2175+/697-): t-045, t-055, t-059, t-062; covered. 1843dfd (6013+): t-045 (T-1), t-061 (T-3), t-072 (t-071 fix); covered. 16ffac7 (266+/2-): t-061 (event #116 "deferred, one pass on the spec-C topic"); covered.
  - 10e521d, 3c22916, 62cfe24: critic entries t-056, t-057, t-054 (same task_id as the builder: legal critic-entry repeat); covered. b0d80bb (2589+): t-040; covered. a2a12ad (747+/22-): t-083; covered.
  - c159412 (850+/5-; the code is ~35 test lines, the rest specs): t-044 `accepted` says "critic: skipped" (event #105); waiver present.
  - 57559de (178+/19-: 78 code lines + a 119-line report): t-081 `accepted` "critic: skipped, 59+/19-" (event #209); waiver present (its count 59+ vs git's 78-line code diff is a minor discrepancy).
  - 94702be (22 files, 1242+/1933-: CLAUDE.md rewrite): plan critic t-013 (and fix round t-023); t-028 `accepted` "critic: skipped, CLAUDE.md is a byte copy of the text the critic walked on the plan" (#61).
  - 572ec23 (261+/29-: 192 of it a critic report): t-024 `accepted` "critic: skipped, 67 lines" (#55); waiver present.
  - b0f7079 (154+/124-, a registry regenerated by `selftest.py --slow-tests --update`): event #211 `dispatch_skipped`; not a builder diff.
  - 10b6f86 (923+/525-, 9 files), 14bd8a8 (213+/13-, 5 files), dc0e047 (433+/433-, a tool data move), 5498318 (merge, 266453+/10982-): NO `delegated`, NO `accepted`, NO critic, NO waiver in the journal (see Check 1).
  - Doc/journal/spec commits over 100 lines (e13388c, f91030a, 8f350d6, 0e57851, 28f59e9, 0076d8c, 066a148, 7f14a22, 393c58a, e2206bf, df3524c, 98f03b2 (initial workflows), bda1693, 194c4b7, b0d8350, 9ac00f0 (initial import)): not builder diffs, outside the check.
- Waiver legality: every `critic: skipped` is in an `accepted` by `fable` over a `sonnet` builder (journal `by`/`model` fields; Lead chains measured fable-5-2) -> the acceptor is above the executor.
- R13-g: `delegated(critic)` events = 33 across 18 distinct task_ids (command: `Counter` of agent critic delegations; 18 distinct `task_id`). TD-11 topic critics: plan t-032; code t-040 (D0+D1), t-045 (T-1+P0-A), t-055 (facade), t-059 (P0-C), t-061 (T-3+C-F3), t-062 (B0b), t-072 (wave-1 cuts), t-079 (applied cut), t-083 (focused critic on t-082, the facade start-up fix). PC2: plan critics t-046, t-050, t-051; code critics t-054, t-056, t-057.
findings:
- Rule 3: 14bd8a8 (226 lines of `tools/` code, a new quarantine backend), 10b6f86 (1448 lines of boot/policy files) -- commits over ~100 lines with no critic entry and no waiver (and no `accepted` at all). The Lead-authored 94702be waiver is ambiguous below.
- ambiguous (t-028): the waiver is legal by acceptor tier, but the commit is 3175 changed lines and rule 3 asks a critic for >100-line builder diffs; the justification (plan critic walked the text, the diff is a byte copy) is a semantic call.
- R13-g, Cost-gates: TD-11 has nine critic passes after its plan critic (t-083 re-reviews the facade topic already passed by t-055; t-079 re-reviews the cut after t-045/t-059/t-062) -- ambiguous: "one topic" is a semantic call for the Lead (sub-topics A..D vs one topic TD-11).

## Check 3 -- Rule 6 / the escalation rule
verdict: ok (with one clean-run note)

evidence:
- Command (script over the journal): `rejected` events per task_id -> t-013 [1], t-038 [1], t-039 [1], t-044 [1], t-036 [1], t-047 [1], t-049 [1], t-054 [1], t-057 [1], t-056 [1], t-053 [1], t-048 [1], t-060 [1], t-077 [1]; no task has two `rejected` at one tier. `escalated` events: 0 (so no `escalated` without a `rejected` trail either).
- Typed fields: events of the mandatory set (`delegated/accepted/rejected/escalated/defect_found`) with no `task_id`: `[]`; `rejected` without `failure_class`/`attempt`/`by`: `[]`; failure classes: spec 11, capability 2, tooling 1. `python -B tools/journal_validator.py --all --base origin/main` -> empty output, exit code 0 (captured separately into a file; `validator_rc=0`).
- Attempt 2 follows every rejection of a builder on the same task_id except t-077 (-> t-078, see 1(d)); no attempt 3 exists.
findings:
- none by the check's text. Note for the Lead: 11 of 14 `rejected` are `failure_class: spec` (dispatcher defects) -- the PROJECT.md rule 6 detector (two `spec` rejections on one task_id) did not fire; the class volume is itself a trend signal.

## Check 4 -- Self-declared-model discrepancy
verdict: ok on workers; ambiguous on the Lead binding id; not measured for 2026-11-05

evidence:
- `python -B tools/usage_report.py --all --json` -> `per_model`: claude-sonnet-5-5 rows 1832, claude-opus-5-5 rows 1234, claude-fable-5-2 rows 961 (`unknown_price_turns: {"claude-fable-5-2": 961}`); `totals.rows 4027`.
- Journal vs sidechains (`cmp.py`): 106 `delegated`, 106 with `agent:<id>` refs, no duplicate `worker_ref`; 95 resolve to a sidechain transcript. Declared model per agent: builder claude-sonnet-5-5 (127 events), scout claude-sonnet-5-5 (24), critic claude-opus-5-5 (33), designer claude-opus-5-5 (18). Measured sidechain models: builder `('claude-sonnet-5-5',)` x57 + one with `<synthetic>` added, scout sonnet x11, critic opus x16 + one with `<synthetic>`, designer opus x9 -> every declared model equals the measured model. The two "mismatch" lines (t-028, t-054) are the `<synthetic>` placeholder row, not a real model.
- Lead chains: all main-chain assistant rows are `claude-fable-5-2` (646c4aac 366, a3462969 746 + 1 `<synthetic>`, 1624cb4a 833, fc171a1f 69, f92520fc 139). `delegation.config.yaml` binds lead to `claude-fable-5-1` (and DECISIONS.md D-0003 says the same).
findings:
- ambiguous: the lead binding names `claude-fable-5-1`; every measured Lead chain is `claude-fable-5-2` (and commit trailers say "Claude Fable 5.2" from 11-11, "Fable 5.1" on be804ba, 11-05). Same tier word "fable" -> the tier matrix holds; a strict model-id reading is a discrepancy (a binding-change decision, D-0003 rewalk, was not made).
- 2026-11-05 events t-001..t-011 (11 `delegated`): no sidechain transcript on this machine -> their `model: claude-sonnet-5-5`/`claude-opus-5-5` cannot be reconciled (not measured; what would measure it: the 11-05 session transcripts, absent from `~/.claude/projects`).

## Check 5 -- Degradation
verdict: not applicable for pairs (empty window); ambiguous for silent degradation on 11-05

evidence:
- `lead_degraded`/`lead_restored` count: 0 each (`sum(e['event'] in (...))` -> 0; the same script returns 14 for `dispatch_skipped`). Journal's last event is `delegated` (t-090), not a `lead_degraded`.
- Lead main chains in the period (not sidechains): see Window -- all `claude-fable-5-2` for 11-11 and 11-12 (the top tier). The only main chain below it is `07782f25` (claude-sonnet-5-5, 2026-11-05T15:06:12Z-15:07:51Z, 32 turns, project dir `C--QAFactory`, cwd `C:\QAFactory`): tools Bash 5, PowerShell 3, browser navigate/get_page_text 9; no Edit/Write, no journal write.
- The 11-05 journal has Lead events (`accepted` by fable, `dispatch_skipped` #2 "Lead self-fix") whose session left no transcript here.
findings:
- ambiguous: 11-05 Lead-tier work (events #2-#27, commits through be804ba) has no Fable main-chain transcript on this machine; the only 11-05 main chain is Sonnet. Either the 11-05 Lead session was elsewhere (transcript absent), or Lead work ran on Sonnet outside a declared window (silent degradation). It cannot be settled from the usage records; the Lead should say which.

## Check 6 -- Acceptance
verdict: finding

evidence:
- Open tasks (no `accepted`/`rejected` after the last `delegated`; script over task_id): t-068, t-073, t-084, t-087, t-088, t-089, t-090. t-084, t-087..t-090 are live workers (t-084's meta has no `"finished": true`; t-085/t-086 launched in the same minute are already accepted). t-068: sidechain finished; closed by `closes:t-068` in event #215 (notes of t-084). t-073: sidechain `aa881de2` meta `"finished":true`, no `accepted`, no `rejected`, no `closes:t-073`; event #212 says "T-2 (t-073, not accepted)".
- Every `accepted` has a preceding `delegated`: `[]` accepted without delegated. `by` counts: fable 96 (accepted+rejected). Executor tiers: builder/scout sonnet, critic/designer opus -> `by` strictly above in every case. Lead chains for events from 2026-11-11T20:58 on are fable-5-2 (Check 5) -> acceptor tier verified for all those; 11-05 `accepted` events unverified (no transcripts).
- `basis` on `accepted`: builder with `basis: critic` 22, builder none 25 (acceptor above executor, so not required), critic none 15, scout none 12, designer none 8.
- Scout `accepted` events (12): every note carries a strict/spot-check marker (`'strict' in n or 'spot' in n` True for all 12); negative claims: t-020 "quarantined gate_repair is absent there (control: the same grep finds the three)"; t-033 note has no negative claim. Spot-check of one load-bearing claim is named in each of the 12.
- Environment-negative claims in notes: `re.search(r'(not found|no such|nowhere|is absent|absent from|does not exist|not installed|not available|cannot be run|not reproduced|no output|empty output|unavailable)', notes, re.I)`, positive control on "X is nowhere to be found" True -> 2 hits: #32 t-014 "Not reproduced locally: the old pin passes on Windows; the proof on Linux is the next CI run" (a stated, measured reason, not an environment claim); #50 t-020 with its control quoted.
findings:
- t-073: a finished dispatch with no acceptance, no rejection and no closing token (rule: every completed `delegated` has a match). Its report is the only open dispatch of the window that is not a live worker. ambiguous: the Lead may be deliberately holding it (T-2 is "not accepted" per #212); the journal has no carrier saying so.
- t-068: closed by token only (legal under the open-dispatch rule), but the work (N2 cut) was folded into t-084 and never accepted as itself.
- Critic task ids repeat the builder's id for a critic entry (t-054, t-056, t-057): legal under the `delegated` row; their `accepted` events cite "critic's verdict t-054" and carry no `basis` (acceptor above executor -- legal).

## Check 7 -- Journal vs transcripts, both directions
verdict: finding on the 11-05 block (not measurable); clean on 11-11/12

evidence:
- Sidechains: `find ...\C--QAFactory-forge-repo -path '*subagents*' -name '*.jsonl'` -> 95 files (`tx.py` prints `95`); `...\C--QAFactory` has 0 (`find $D -name '*.jsonl'` lists three main files only).
- Direction 1 (sidechain without `delegated`): `cmp.py` -> "sidechains without journal delegated:" empty (all 95 matched by the 8-hex prefix of `worker_ref`, positive control: 95 of 95 match).
- Direction 2 (`delegated` without sidechain): 11 refs, all 2026-11-05: t-001..t-011 (`abf60cc3`, `a556f868`, `a6b17a89`, `a0e4d844`, `a1f255f9`, `a0931996`, `a2c0c63b`, `a9f70e52`, `aa6c9847`, `a39c8a0f`, `ac5833bb`).
- Agent calls that never launched: 6 `Agent` tool_use in main chains with no sidechain -- all returned `PreToolUse:Agent hook error: DISPATCH PATHS MISSING (CLAUDE.md rule 11)` (1624cb4a 22:19:57, 22:20:37, 22:21:02, 01:24:01; a3462969 23:28:36; f92520fc 10:15:59); each was re-sent and the re-sent one has its `delegated`. Counts: Agent calls 59 + 34 + 8 = 101 = 95 launched + 6 refused.
- All 95 sidechain metas carry `"requestShape":"background"` (command: `Counter` over `*.meta.json`).
findings:
- 11 `delegated` events (t-001..t-011) have no matching sidechain: either phantom events or transcripts that are not on this machine (the 11-05 sessions left only the Sonnet `07782f25`). ambiguous; not measurable here; what would measure it: the 11-05 transcripts or the old repository's bundle (journal_created #1 says the history stays in the old repository's bundle).
- No undocumented dispatch (sidechain with no `delegated`) in the window.

## Check 8 -- The four-questions-per-mechanism rule
verdict: finding (mostly ambiguous items for the Lead's judgment)

evidence:
- New DECISIONS entries in the window: `git log --since=2026-11-05 -p -- DECISIONS.md docs/DECISIONS_ARCHIVE.md | grep '^+D-...'` shows only archive/index moves in 572ec23, 10b6f86, 4d12e85 (ids moved whole, not new decisions); no new D-number. Latest ids: D-0063, D-0064 live in `DECISIONS.md:43-44`, and no commit of the window adds them. "empty window": no new decision entry; so no (a)-(d) answer to audit in DECISIONS.md.
- Machine audit: `python -B tools/mechanism_gate.py --audit --since 2026-11-05` -> `mechanism_gate audit since 2026-11-05: 11 commits on mechanism paths, 0 mismatches (0 axis lines without a label, accepted before 2026-10-16; 91 commits in the window; reference: the current map)`; `audit_rc=0` (separate run capturing the exit code).
- Gate liveness: `git config core.hooksPath` -> `C:\QAFactory\forge-repo\.githooks`.
- Commit messages with a four-questions block and the 36 axis lines (the map has 36 axes: `## Axis N` headings 1-36, `grep -n '^## Axis' docs/SIBLING_MAP.md`): 94702be, 572ec23, a6b273e, 16ffac7, 10b6f86's waiver line; their (c) answers register an existing detector (`install_parity.py --check`, session_context budget line / calibration check 10, K5 history check / check 33).
- "axes: not a mechanism" lines in the window (`git log --format='%h|%B' | grep ...`): 34 commits carry one; of these the substantively doubtful: be804ba (PROJECT.md "the docker fallback runs only on the owner's word" -- "one clause of an existing rule narrowed"), 47ff421 (an owner's word written into PROJECT.md rule text), 14bd8a8 (the quarantine reads CI on GitHub, a second backend; also has `tier: fable`), 4f43202 ("the net of the gate follows the import closure ... two file names" -- touches the mechanism net), 483e664 (a scrub rule dropped), 32858bd (the move also edits `docs/SIBLING_MAP.md` anchors).
- Tier declarations: `tier:` lines (`git log --format='%h|%B' | grep '^tier:'`) on 10b6f86, 14bd8a8, 16ffac7 (`tier: claude-fable-5-2`, a model id rather than the keyword), 47ff421, 483e664, 4d12e85, 4f43202, 572ec23, 94702be, a6b273e: all say fable; the Lead chains at those times measured fable-5-2 (646c4aac for 11-11 18:47Z-20:09Z, a3462969/1624cb4a after) -> truthful. be804ba (11-05) has no `tier:` line and no 11-05 transcript to reconcile.
findings:
- ambiguous: the waivers above (be804ba, 47ff421, 14bd8a8, 4f43202) are candidates for "a waiver used on a substantive mechanism"; by the commit texts they add no duty, but PROJECT.md edits and a new CI backend for a gate-relevant tool alter what future sessions must do. Lead judgment; if any is a mechanism, a retroactive four-questions writeup is owed.
- 16ffac7 `tier: claude-fable-5-2` is not the bare tier word the journal gate requires for `by` (the commit gate accepted it): form inconsistency between the commit-trailer and the journal conventions.
- 646c4aac's mechanism-path edit (`tools/mechanism_gate.py`, 4f43202) was not journaled (Check 1).
- (c)/(d) registered-detector audit of new mechanism commits: all four block-carrying commits name an existing registered detector; nothing missing.

## Check 9 -- SIBLING_MAP class-wide completeness
verdict: finding (ambiguous in part)

evidence:
- "New axis for SIBLING_MAP" lines: `grep -i 'new axis'` over commit messages since the import -> count 0 (`git log --since=2026-11-05 --format=%B | grep -i -c 'new axis'` = 0); over `logs`, `docs/tasks/compact-snapshots`, pile READMEs -> only a hit in `logs/.search-ledger/...jsonl` (the search ledger of this very session, not a note). Positive control for the lookup shape: the same grep for `no neighbors` finds `CLAUDE.md`.
- Findings added in the window by regular commits: `git log 9ac00f0..HEAD --no-merges --diff-filter=A --name-only -- 'plans/piles/*/findings/*.md'` -> 57 distinct files (15 filed 2026-11-11/12 by 0e57851, 28f59e9, 0076d8c, 94702be, df3524c, b695ec1; 1 each 11-05 by bda1693, 194c4b7, 8bed03b; the rest arrived with the 5498318 merge). Marker grep: `grep -i -E 'no neighbors|neighbor'` over the 15 new ones -> no `no neighbors:` line; `grep -i -E 'сосед|neighbor|sweep'` over the 57 -> 5 files mention neighbours in prose (e.g. `project-knowledge/findings/20261111-guard-globalnaya-opciya-pered-podkomandoj.md:17` "для обоих соседей"), none as a per-neighbor enumeration with verdicts. Control: the same Russian pattern over all piles' findings returns 99 files, so the pattern shape works.
- Class-naming journal events: #98 (t-044 rejected, "the brief named one scenario, not the class"), #126 (t-037 defect_found, "any Driver* class name resolves"), #200 (t-080 delegated, "A class P0-C missed: kept tests read the driver's text through Path(story_run.__file__)"), #31 (t-014 delegated "sweep the file for the same class"). The control for the pattern `class|sibling|neighbo` is True on "A class P0-C missed".
- Commits that close findings and name axes: the four-questions blocks of 94702be, 572ec23, a6b273e, 16ffac7 enumerate all 36 axes; commits that closed pile findings under "axes: not a mechanism" (14bd8a8/FG7-10, 483e664/FG7-9) name none.
findings:
- No class-named finding in the window carries an enumeration of its own artifact's neighbors or "no neighbors: <why>" (the 15 new findings, #98/#126/#200 in the journal). ambiguous: whether each of those "names a CLASS" is the Lead's call (the pile findings are mostly one-instance defects; #200 and t-044's reject plainly name one).
- The FORMALITY DETECTOR cannot run: no enumeration exists to rubber-stamp.

## Check 10 -- Growth of live files
verdict: finding on the SIBLING_MAP; first baseline for the rest (no previous `calibrated` event)

evidence:
- Previous run: none (0 `calibrated` events) -> these numbers are the baseline for the next `calibrated` event. Command: `wc -l <file>; wc -c <file>`; comparison column: `git show 9ac00f0:<file> | wc -l` (the import commit on 2026-11-05):
  - BOOT.md 52 lines / 1819 B (import: 48 / 1666 B)
  - SYSTEM_PROMPT.md 18 / 627 B (18 / 609 B)
  - DECISIONS.md 44 / 7547 B (78 / 55814 B -- down after the 11-11 boot diet, 4d12e85, 572ec23, 10b6f86)
  - CURRENT_CONTEXT.md 22 / 1219 B (22 / 1197 B; the file was not edited since the import: `git log -- CURRENT_CONTEXT.md` -> 9ac00f0 only)
  - CLAUDE.md 435 / 41502 B (855 / 57091 B -- cut by 94702be)
  - PROJECT.md 401 / 58077 B (404 / 64134 B)
  - docs/SIBLING_MAP.md 637 lines / 155892 B working tree (589 / 142553 B at import). Per commit: 9ac00f0 589, 5498318 637 (+48 via the merge), 572ec23 637, 94702be 637, 16ffac7 637, 32858bd 637 -> bytes 142553, 154624, 154647, 154681, 154891, 155255 (committed form, LF).
- Boot files list taken from `BOOT.md`: Layer A = SYSTEM_PROMPT.md, DECISIONS.md; Layer B = CURRENT_CONTEXT.md; "read when needed": README.md, DELEGATION_TABLE.md.
findings:
- docs/SIBLING_MAP.md grew +48 lines / +13.3 KB since the import and is monotonic through the window (every window commit that touched it added bytes: 5498318 +12071 B, 94702be +34, 16ffac7 +210, 32858bd +364) while the check calls it "supposed to stay small"; at 155 KB it is the largest live file measured. Part of the growth is the merged experiment line (5498318), so ambiguous: the Lead decides whether a merge of an older line counts as growth "with no archive".
- The boot-path files (DECISIONS.md, CLAUDE.md, PROJECT.md) shrank in the window through deliberate boot-diet commits; BOOT.md/SYSTEM_PROMPT.md/CURRENT_CONTEXT.md are flat. No monotonic growth there.
- Observation: `CURRENT_CONTEXT.md` is 22 lines and unchanged since the import although eight days of work happened -- not a size finding; recorded because its role is "state of main" (PROJECT.md rule 5).

## Check 11 -- Rule #1 applied to the routing machinery itself
verdict: finding

evidence:
- Overhead from usage records: `python -B tools/usage_report.py --all --json` -> totals `rows 4027`, `input_tokens 8306`, `output_tokens 4944337`, `cache_creation_tokens 21564286`, `cache_read_tokens 692899344`; `sidechain_tokens 416223956`, `sidechain_share_of_tokens 0.5785578831353457`, `sidechain_accounted_cost_usd 178.97442179999973`; `accounted_cost_usd 179.2492...`; `unknown_cost_rows 961` (all `claude-fable-5-2`, price not in `tools/model_prices.json`). Per model output tokens: fable (Lead) 994936, sonnet 2324930, opus 1624471 -> Lead = 20.1 % of output tokens, 42.1 % of all tokens (303192317 main of 719416273; cache reads 297.9 M of the Lead's).
  USD overhead ratio is NOT measured: the Lead's price is unknown to the tool (what would measure it: a `claude-fable-5-2` row in `tools/model_prices.json`).
- Lead tool-call mix, proxy for "what Lead spends on" (`ovh.py`, call counts, not tokens): journal Edit/Write 101 (54 + 42 + 5), dispatch (`Agent`) 101, specs/tasks/snapshots 53, plans/policy files 69, shell 384, reads 140, code files 24. Journal appends are as numerous as dispatches (1:1).
- Sync dispatches: all 95 sidechain metas have `requestShape: background` (positive control: the same field exists on every meta, `Counter` = `{'background': 95}`); the Agent inputs lack `run_in_background` in 41/6/0 calls but the host receipt says background -> no synchronous dispatch in the window ("empty window: no sync dispatch").
- SessionStart hook: `echo '{}' | python -B tools/session_context.py` -> exit 0, `wc -lc` = 89 lines / 10103 bytes (first measurement, baseline for the `calibrated` notes next to the check-10 counts). Key line 11: `BOOT BUDGET: 117229 bytes / 120000 (4 files + 3 imports) WARN | CLAUDE.md: 41502/47800 incl. imports 107836`. Line 88: `[WARNING: 20 unmapped non-ASCII characters in DECISIONS.md were replaced with '?' -- MEANING MAY BE LOST; tell the operator]`.
- Limit history: 572ec23 message "Boot total 147868 -> 133737 bytes of 100000"; a6b273e (t-031) raised the limit 100000 -> 120000 and the warn 90000 -> 108000 ("owner's word 11.11.2026", axis 18 "a RAISE, named").
- WARN layer density: `python -B tools/warn_density.py --window-start 2026-11-05T00:00:00 --window-end 2026-11-12T11:45:00 --no-sidecar` (no previous `calibrated` -> journal start used; `--no-sidecar` so no file was written). `SUMMARY: layers 23 - calls total 407 - tool_use in window 1065`; `--check`: "layers in registry: 23 (valid: 23) (no defects)" and "FINDINGS ABOUT THE CHECK: (reconciled)". Per layer, calls / achievable share / rate per 100 tool_use:
  - GIVEN-PATH 45 / n/a (population not declared: false-positive-class layer) / 4.23
  - ROLE-TYPE 0 / n/a / 0.00; WRITE-QUOTED 0 / n/a / 0.00; DOD-QUOTED 0 / n/a / 0.00; MANIFEST-QUOTED 0 / n/a / 0.00
  - OWNS OVERLAP 23 / n/a (needs owns_gate's own parser) / 2.16; BLIND_OWNS 0 / n/a / 0.00; QUOTED_OWNS 0 / n/a / 0.00
  - TIER ECHO 0 / 0.0 % (0 of 101 achievable) / 0.00
  - WITNESS ECHO 29 / 28.7 % / 2.72
  - TS DRIFT 1 / 1.0 % / 0.09; ESCALATION 0 / 0.0 % / 0.00
  - NOTES LEN 22 / 21.8 % / 2.07; R3 MIRROR 1 / 1.0 % / 0.09; JOURNAL ECHO 4 / 4.0 % / 0.38
  - NEGATIVE LINT 0 / n/a / 0.00; Negative claim 22 / n/a / 2.07
  - Search returned nothing 156 / 56.1 % (156 of 278 achievable) / 14.65
  - Command hygiene 46 / n/a (population not wired) / 4.32 (`in_density_check=no`)
  - FRESHNESS WARN 0 / n/a / 0.00; MANIFEST-SKIP 0 / n/a / 0.00; MANIFEST-UNCHECKED 0 / n/a / 0.00
  - PATH CHECK 58 / n/a / 5.45
  - Source-control lines: `subagent stream invisible: 5045 of 6110 window calls (the denominator counts main-stream only)`; `second traces ... 511 (hook_success: 479, orphaned: 46)`; `stdout does not parse as JSON (raw fallback): 8`.
  - Layers named in the check and checked against `tools/warn_layers.json`: all 23 registry layers reconcile ("--check ... (no defects)", "(reconciled)"); layers in the check's list but absent from the registry: none; live layers absent from the check's list: none surfaced by the reconciliation.
- Notes length (`rule 12: journal notes <= 300 chars`): 24 events have `len(notes) > 300` (#7 327, #34 305, #45 323, #75 315, #76 330, #91 327, #116 305, #142 321, #144 322, #162 322, #163 329, #176 305, #184 344, #190 316, #192 301, #193 301, #196 357, #198 366, #200 329, #203 412, #208 339, #211 324, #212 302, #213 331) -- the NOTES LEN layer reports 22 firings.
findings:
- WARN layers marking tens of percent of their own achievable population: Search returned nothing 56.1 %, WITNESS ECHO 28.7 %, NOTES LEN 21.8 % -- by the check's text "a mechanism defect, because a warn that dense trains the reader to ignore it". (No share threshold set in advance; the numbers are the obligation.) Several layers (HYGIENE, PATH CHECK, GIVEN-PATH, OWNS OVERLAP, Negative claim) have no declared population -> their share is "n/a", their rate is 2-5 per 100 tool calls.
- Boot budget at 97.7 % of a limit that was raised 20 % on the owner's word in the same week; the raw load is 117229 B after the diet (down from 133737 B before 572ec23's diet and 147868 B before that) -- monotonic evidence for simplification is not yet established (single measurement), but the WARN state is the starting point of the trend.
- DECISIONS.md reads through the hook with 20 non-ASCII characters replaced by `?` (line 88 of the hook output): "MEANING MAY BE LOST" -- a live encoding defect of the hook output (cp1252 stdout on this machine).
- Journal overhead is high but not measurable in USD: journal Edit/Write calls equal dispatch calls (101 : 101). Lead output tokens are 20.1 % of all output; the worker output (sonnet+opus) is 79.9 %. Not "systematically comparable to the work it routes" by output tokens, but the cache-read volume of the Lead (297.9 M, 41 % of all tokens) is a large part of the bill. Decision on simplification is the Lead's.
- Sync-dispatch finding: none.

## Check 12 -- SIBLING_MAP liveness
verdict: finding

evidence:
- Method: every backticked token in `docs/SIBLING_MAP.md` ending in `.py|.md|.json|.yaml|.yml|.sh|.jsonl|.txt` or a trailing `/` (452 distinct), resolved against the repo root and the base directories `ai-packages/qa-factory/`, `.../scripts/`, `.../scripts/tests/`, `tools/`, `references/`, `design/`, `fixtures/`, `docs/`, `plans/` (`map.py`; output "distinct path-like tokens 452 / not found at any base: 60"). Triage of the 60 (runtime state names like `state/driver-state.json`, `work/grounding.yaml`, `captures.jsonl`, file basenames that exist under a package directory, and ellipsis fragments excluded) leaves these dead concrete paths, each confirmed by `ls` (positive control: `ls tools/mechanism_gate.py` -> exists):
  - `.gitlab-ci.yml` (map line 518, row "`.gitlab-ci.yml` | integrator | per-push regression") -- file absent; CI is `.github/workflows` here (PROJECT.md); `ls .gitlab-ci.yml` -> No such file.
  - `tools/test_ci_layout.py` (map line 518, "golden") -- `ls` -> No such file.
  - `tools/language-sites-baseline.json` (line 586, "The code layer (planned)... after its baseline ... exists") -- absent; the row is conditional ("planned"), but `tools/language_sites.py` exists, so a detector described as INERT with a baseline that was never created (ambiguous: planned vs dead).
  - `logs/routing-log.jsonl` (line 165: `tools/forge_metrics.py` reads it) -- absent; `logs/` holds only `dispatch_verdict.json`, `journal/`, `owns_registry.jsonl`, `posttooluse-schema-sample.json`; the protocol header and PROJECT.md point at `logs/routing-log.jsonl` as read-only history, the file does not exist in this repository.
  - `experiments/driver-golden/`, `experiments/driver-golden-c2f837f/`, `experiments/driver-golden/coverage-n0.json`, `freeze_package.sh` (line 166, axis "The driver golden") -- `ls experiments` -> `measurers` only.
  - `ai-packages/qa-factory/design/factory-map.md` (line 114): "Until ... exists" -- conditional wording; the map lives at `docs/factory-map/` (README.md, graph svgs). Dead only if the condition has long been met.
  - `skills/qa-story/index.yaml` (line 135) -- actual file `ai-packages/qa-factory/handoffs/index.yaml`; `references/controller-paths.md` (line 217) -- actual `ai-packages/qa-factory/design/controller-paths.md`; `plans/piles/onboarding-hooks/findings/20261030-windows-260-codex-dispatch-bez-konteksta.md` (line 255) -- actual under `plans/piles/onboarding-forge/findings/`.
  - `tests/ui/pageobject/login_page.py` (line 127) and `qa-factory/state/reporter-rehearsals.json` -- examples/runtime state, not repo paths.
- Rules/mechanisms still live: `.gitlab-ci.yml` row names a mechanism that moved to GitHub Actions (`.github/workflows` in the import commit 98f03b2); the PROJECT.md rule "the GitLab board is off" is consistent with it.
- Decisions count (this half of the check applies only when decisions are "an index plus a full-text companion"): `DECISIONS.md` holds 18 entry-start ids (D-0002, 3, 5, 7, 9, 21, 22, 33, 37, 39, 43, 44, 46, 49, 50, 59, 63, 64; the first nine-plus are trimmed index lines whose full text is archived), `docs/DECISIONS_ARCHIVE.md` holds 58 (D-0001...D-0062). Union covers D-0001..D-0064 minus D-0045: `grep -n 'D-0045' DECISIONS.md docs/DECISIONS_ARCHIVE.md` -> no match (positive control: the same grep for `D-0046` -> 2 and 4 matches); D-0046 appears 3x in the archive (lines 55 and 82) -- a duplicate. D-0063/D-0064 are live only in `DECISIONS.md:43-44`, absent from the archive.
- Repeats in the period (a defect of an already fixed class recurring outside the map's listed spots): the cut of `story_run.py` (axis 13/driver-layers rows) was followed by defects of the same class outside the listed spots -- #126 (L8 never switched on), #196 (t-053, tests collected from tools/), #200 (t-080, kept tests reading `story_run.__file__`), #203/#204 (K-M3 and a timeout) -- written up as journal findings, but no commit of the window corrected an axis of the map for them beyond the anchors in 32858bd.
findings:
- Dead paths in the map: `.gitlab-ci.yml` and `tools/test_ci_layout.py` (line 518), `experiments/driver-golden*` and `freeze_package.sh` (line 166), `logs/routing-log.jsonl` (line 165, still named as a reader's input), three wrong-base/wrong-pile paths (lines 135, 217, 255) -- each a violation of the map's own same-commit-maintenance rule. `tools/forge_metrics.py` reading a file this repository does not have is also a live-mechanism question (tools broken, or dormant).
- ambiguous (decisions counts): the check's decisions half applies only to an index-plus-companion layout; here `DECISIONS.md` mixes trimmed index lines and live entries. Two readings: (a) the half applies and the counts do not match (18 vs 58; D-0045 absent; D-0046 duplicated in the archive); (b) it does not apply (single live file with a moved-out archive). The Lead judges.
- The `Repeats` line: the map was not corrected for the post-cut repeat class (journal #126, #200); queue for the Lead.

---

## Positive controls used (for every empty result above)
- "no repeat marker in skip events": pattern `repeat of class|second occurrence|repeat` run against `'second occurrence'` -> match; the resubmission pattern run against `'a resubmission'` -> True; the environment-negative pattern against `'X is nowhere to be found'` -> True; the class pattern against `'A class P0-C missed'` -> True; the neighbor grep over findings has its control in CLAUDE.md (matches `no neighbors`) and a 99-file Russian-pattern control.
- "no `lead_degraded`/`lead_restored`/`calibrated`/`escalated`": same script returns 14 `dispatch_skipped`, 106 `delegated`.
- "no sidechain without `delegated`": the same prefix join matches 95 of 95.
- "no new decisions": the grep for `^+D-` shows lines for the three move commits (so the pattern works) and none for new numbers.

## Needed beyond the manifest
- `~/.claude/projects/C--QAFactory-forge-repo` and `...\C--QAFactory` (main and subagent transcripts, `*.meta.json` with `requestShape`/`toolUseId`) -- not in the "given" basket; `tools/usage_report.py` does not split main vs sidechain per model by itself, so a named script parsed the transcripts.
- Full git history (`git log --numstat`, commit bodies, `core.hooksPath`), `plans/piles/*/findings/`, `BOOT.md`, `SYSTEM_PROMPT.md`, `CURRENT_CONTEXT.md`, `PROJECT.md`, `tools/warn_density.py`, `tools/mechanism_gate.py --audit`, `tools/journal_validator.py --all`, `tools/session_context.py`.
- The dispatch prompts (Agent `tool_use` inputs in the main transcripts) for the `owns:` / numbered-item counts of check 1(c).
- A usage-record notion of "cc_usage" does not exist here (checked: `tools/usage_report.py` reads transcripts directly); `PROCESS/CRITIC_EXAM.md` does not exist (`ls PROCESS` lists 11 files, none named so) -- exam-set checks belong to the other parts of the calibration (D-0037/D-0058 are the recorded deferral).

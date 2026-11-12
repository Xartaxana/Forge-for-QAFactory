# Weekly calibration 12.11.2026 -- evidence layer p2, checks 13-18 (task t-088, feature F19)

Gatherer: builder (sonnet), read-only. Nothing fixed, committed or edited except this file. The verdicts are the Lead's.

## Window

- Journal: `logs/journal/dev1.jsonl`, the whole file is the window (first calibration of this repository; `Last calibration: NONE` is in the SessionStart line of all three transcripts).
- First `ts` 2026-11-05T14:29:30, last `ts` 2026-11-12T11:30:14 (t-090) at the moment of the run. Command: `python -B tools/journal_keys.py where` -> `last ts: 2026-11-12T11:30:14`; first by `python -B -c "...L[0]['ts']..."` -> `2026-11-05T14:29:30`.
- Events by type, command `python -B tools/calibration_counts.py` (223 lines parsed, 223 in window, 0 unparsable):
  `accepted: 82, defect_found: 6, delegated: 106, dispatch_skipped: 14, journal_created: 1, rejected: 14`.
- By tier x event (same command): builder accepted=47 defect_found=6 delegated=67 dispatch_skipped=6 rejected=13; critic accepted=15 delegated=18 dispatch_skipped=1; designer accepted=8 delegated=9 dispatch_skipped=6 rejected=1; scout accepted=12 delegated=12 dispatch_skipped=1; lead journal_created=1.
- The journal grew while I worked (219 -> 223 lines, t-087..t-090 are live workers, one of them is this task).
- Transcripts on this machine: 3 sessions of this project (`~/.claude/projects/C--QAFactory-forge-repo/{1624cb4a,a3462969,f92520fc}`) with 95 agent transcripts, plus 3 sessions of the parent folder project `C--QAFactory` (one of them, fc171a1f, ran in the same clone, 11.11 18:23Z-18:37Z). There is NO transcript for the 05.11 block (t-001..t-011): the earliest transcript on disk starts 2026-11-11T19:26Z (positive control: 95 of 106 `delegated` worker_refs resolve to a transcript with the same lookup).

### Summary of findings, by weight

1. Check 17(d): the Lead session 1624cb4a has a median context of 361,780 per turn (target <= 350K) and 109 turns over 600K (max 679,370; 11.12 04:26-06:08 local); its only two compactions are at 11.11 21:08Z and 23:35Z. A compaction was skipped. No worker passed 400K (17(a) ok).
2. Checks 13(d)/15: 10 of the 14 `rejected` events are dispatcher-side (spec/DoD/owns narrower than the failing class or the sibling surface, or the spec's own design/premise wrong); 13 of 14 are `failure_class=spec|capability` on builder-class work, 10 of 13 builder rejections are `spec`. Cluster A (the DoD/owns did not carry the sibling class) recurs 6 times (t-044, t-049, t-054, t-056, t-057, t-060) although rules 9 and 11 already encode it: a repeat of a codified class = the codification leaked. No `calibrated` event exists yet, so the cluster count (check 15 iii/vi) is owed.
3. Check 13(j)/rule 4: no `witness` field carries a "BATCH CANON" label (0 of 47); every canon result of the window sits in `notes` of `defect_found`/`dispatch_skipped` lines (179, 203, 211, 212) and two `accepted` lines say "BATCH CANON to be appended when read" (202, 210) with nothing appended afterwards. Second signature on a 2-node sample: t-085 and t-086 witnesses are narrower than `scenario_walk.py --witness-for <owns>` prints.
4. Check 17(b): one fix round by a RESUMED builder after a critic verdict: t-082, `SendMessage` to a7794056795e8efa6 at 2026-11-12T04:28:36Z "t-082: three fixes from the critic, then done"; the journal line 208 says so ("Fixes sent back to the same builder"). Expected 0.
5. Check 17(e): per session the writer count peaked at 6 (1624cb4a), 5 (f92520fc), 3 (a3462969) -- inside the gate's cap of 6 (`PARALLEL_CAP = 6`, D-0054), but the two parallel sessions of 11-12 01:00Z carried 8 builder-type workers at once (the cap counts one session's subagents folder only); and the protocol text of 17(e) still says "more than 4" (stale against CLAUDE.md/D-0054).
6. Check 13(i): t-073 (T-2, delegated 11.12 02:26) is still open: its worker finished and handed back at 02:48 (transcript `agent-aa881de274d1ace2d`, `finished: true`), no `accepted`/`rejected`/`closes:` in 9 hours and across 2 session boundaries. t-068 stayed open the same way until `closes:t-068` at 11:16 (line 215).
7. Check 13(f): t-057 `accepted` (line 159, 02:05) is 416 s BEFORE its worker's last transcript line (02:12:19); t-045 `delegated` (line 96) is 39 s BEFORE the worker's first line; t-036 attempt-2 `delegated` (line 125) is written 3364 s AFTER its worker started; line 211 carries a ts 14 s before the commit (b0f7079) its notes name; in the 05.11 block 25 of 27 `ts` have seconds divisible by 5 (26 of 196 in the rest).
8. Check 13(b): false-accept rate builder 6/47 = 12.77% (critic, designer, scout 0). 4 of the 6 defects sit in work accepted with `basis: critic` (t-005, t-053, t-060, t-047); one `defect_found` (line 196, ref t-053) names a cause that belongs to t-047 in its own notes.
9. Check 17(d): 24 of 223 journal notes are over 300 chars (max 412); 2 CI-log reads through the browser in session fc171a1f (same clone, 11.11 18:2xZ).
10. Check 13(e): 4 id collisions with the parallel session in the same minute (dispatch text and report file say t-046, t-050, t-054, t-058; journal ids t-049, t-053, t-055, t-059), i.e. the "re-read the journal tail before issuing" rule leaked 4 times; also the protocol text of 13(l) names `logs/routing-log.jsonl`, which does not exist here (stale carrier).
- Not measured here: 14(b) (no exam set), 17(d) stage commits per merge (no mechanical definition), 18(d) API rollup (no `requests` table) and the previous data point of check 18 (none).

## Check 13 -- Evidence-based acceptance, typed fields

False-accept rate by tier (13(b)), command `python -B tools/calibration_counts.py`:
```
=== False-accept rate by tier ===
  builder: defect_found=6 / accepted=47 = 0.1277
  critic: defect_found=0 / accepted=15 = 0.0000
  designer: defect_found=0 / accepted=8 = 0.0000
  scout: defect_found=0 / accepted=12 = 0.0000
```
The 6 `defect_found` (refs t-005, t-037, t-054, t-053, t-060, t-047; lines 22, 126, 179, 196, 203, 204) all point to an `accepted` builder task of this journal (check: `all defect refs accepted builder: True`, a python scan of the journal). Of the 47 builder acceptances, 22 carry `basis: critic` (no other `basis` value exists).

verdict: finding (see the lettered lines)

### 13(a) witness on every builder `accepted`
verdict: ok
evidence: `python -B -c` scan over the journal printing `witness` of every `event==accepted and agent==builder`: 47 lines printed, none `<<NONE>>`; `witness` on non-builder accepts: `[]`. `python -B tools/calibration_counts.py` -> `=== Missing typed fields (candidate violation, post-legacy) ===  (none)`; `python -B tools/journal_validator.py --all --base HEAD` -> no output, rc=0.
findings: none. Adjacent (not 13(a)): lines 218/219 (t-086, t-085, ts 11:22:47 / 11:24:29, after 11:20) are the ones the coordinator said carry a WITNESS ECHO note. The echo text is hook output (`tools/journal_echo.py` lines 127, 313) and is not stored in the journal (`grep WITNESS ECHO` over the journal -> no match; positive control: the same grep over `tools/journal_echo.py` hits lines 127/172/313). What the carrier shows: `.claude/dod_track/f92520fc-....json` records the run behind t-086's witness at 11:22:40 with `outcome: red` and the run behind t-085 at 11:24:29 with `outcome: green`. I cannot reproduce the echo text itself ("not measured"); the Lead has it from its own turn.

### 13(b) defect_found ref + false-accept rate
verdict: finding
evidence: see the table above; refs resolve (above).
findings:
- Builder 6/47 = 12.77% in the first window (a rate that is "systematic" or not is for the Lead; the other tiers are 0).
- 4 of 6 defects are in work accepted with `basis: critic` (t-005 line 17, t-053 line 168, t-060 line 177, t-047 line 135), i.e. the critic gate did not stop them: causes were canon-only (Linux CI) reds and a scope miss (t-005: "the node's narrowed witness did not include test_audit_rules (dispatcher's scope miss)", line 22).
- ambiguous: line 196 `defect_found` ref=t-053 lists three causes (pytest collecting tools/test_split.py = t-053; audit rule A1 on module_facade.py = "ref t-047" in its own notes; test_walk_lanes_parallel = t-014's class) under ONE ref. Reading 1: one event per ref is the rule, the Lead chose the main cause; reading 2: t-047 and t-014 each needed their own `defect_found`. t-047 did get its own line later (204, a different cause).

### 13(c) `failure_class` on every `rejected`
verdict: ok
evidence: `python -B tools/calibration_counts.py` -> `Rejected by failure_class x agent x model: capability / builder: 2; spec / builder: 10; spec / designer: 1; tooling / builder: 1` = 14 = the 14 `rejected` events; `Escalation-pairing candidates: (no candidates)`.
findings: none.

### 13(d) systematic spec class; manifest completeness; recon
verdict: finding
evidence:
- `failure_class=spec`: builder 10 of 13 rejections, designer 1 of 1. `failure_class=recon`: 0 (count above; the table lists every class present, `recon` is absent -- positive control: the same table lists `spec`).
- Dispatch header form (rule 11 R11-f): `python -B <scratchpad>/manifest.py` over the first user line of the 58 builder transcripts (`transcripts.first_user_text`, `agentType: builder`): `builder transcripts 58 ... with manifest-skip line 3; missing header key counts {'DoD:': 3}; all six present: 55 of 58`. The three that lack a `DoD:` header line (agents a18313c6=t-078, ae955ade=t-080, aecd9be3=t-077) are the three that carry `manifest-skip: owns -- ...` (control: the `manifest-skip:` regex found those 3). `budget-skip:` lines: 0 of 95 dispatch texts (same loop, control = the 3 manifest-skip lines).
- "needed beyond the manifest" telemetry: `python -B -c ... glob docs/tasks/specs/reports/*.md` -> `reports with the line 42 of which none/empty 6 naming files 36` (of 62 files in the folder).
findings:
- MANIFEST-SKIP density 3 of 58 builder dispatches (5%), all on `owns` for the tool-written part files of the TD-11 cut (t-077, t-078, t-080); each has its reason inline. The gate is walked around by an informed pass, not silently.
- 36 of 42 reports that carry the line name files read beyond the basket: the "given" baskets are systematically thin for TD-11 nodes (check text: "piling up -> the Lead's baskets are systematically thin").
- ambiguous: t-056 (line 146: "a check outside the owns I gave") and t-057 (line 144: "R1 t-2181 lines 48/769 ... not in the owns I gave") are `failure_class=spec` for an INCOMPLETE `owns` -- the header gate checks the presence of `owns:` but not its sufficiency. Reading 1: a leak of the gate itself (check text: "a rejected spec for a MISSING manifest item after 2026-09-30"); reading 2: not a missing item, an incomplete one, outside the gate's reach (a dispatcher defect, check 15 cluster A).

### 13(e) task_id integrity
verdict: finding
evidence: `python -B -c` over the journal -> `90 1 90 missing []` (t-001..t-090 all present once as first delegation); delegated more than once: `{t-013:2, t-036:2, t-038:2, t-039:2, t-044:2, t-047:2, t-048:2, t-049:2, t-053:2, t-054:3, t-056:3, t-057:3, t-060:2}`; `python -B tools/calibration_counts.py` classifies all 16 repeats `critic-entry` or `continuation` (attempt=2 after `rejected`), none a collision. `logs/journal-segments.json` does not exist (`ls` -> No such file; one journal, one clone: no segments to declare). `python -B tools/journal_keys.py where` -> `next free id: t-091`.
findings:
- No duplicate id between unrelated tasks inside the journal.
- Id collisions with the parallel session caught only in the text: line 104 (t-049: "dispatch text and report file say t-046 ... taken by the parallel session in the same minute"), line 112 (t-053 says t-050), line 115 (t-055 says t-054), line 128 (t-059 says t-058). Four workers' dispatch texts and report files carry an id that the journal assigns to other tasks (report files `t-046-td11-P0-C.md`, `t-054...`, `t-050...`, `t-058...`; `ls docs/tasks/specs/reports | grep t-0` lists them). CLAUDE.md "Issuing a task_id means re-reading the tail of the journal right before writing `delegated`" is the codified rule; 4 repeats in one window = the rule leaked (class: dispatch text composed before the id is issued). The journal itself kept both sets distinct, the collision is between text and journal.

### 13(f) timestamp honesty
verdict: finding
evidence: monotonic: `python -B -c` -> `nonmono 0`; `calibration_counts.py` `=== ts anomalies ===  (none)`. External clock = the agent transcripts' own timestamps (UTC, local = +1 h; SessionStart `NOW: 2026-11-11 21:37:52` vs first transcript line 20:37:57Z) via `python -B <scratchpad>/clock.py` over all 95 resolvable workers:
```
delegated journal ts minus worker first ts (s): n 95 min -38.986 max 3364.484
journal delegated BEFORE worker start by >5 s: [(96, 't-045', -38.986)]
journal delegated > 120 s AFTER worker start: [(125, 't-036', 3364.484), (128, 't-059', 177.994), (149, 't-062', 122.879), (150, 't-063', 122.866), (151, 't-064', 122.667), (182, 't-076', 203.101)]
accepted/rejected ts earlier than worker last transcript line by >30 s: [(159, 'accepted', 't-057', -416)]
```
git: `git log -1 --format='%ad' b0f7079` -> `11-12T05:52:22`; journal line 211 ts `2026-11-12T05:52:08` names b0f7079 in its notes. Commits named in other lines are all before their journal line (8ae68ce 15:32:28 < line 4 15:35:40; 701c09a 02:52:50 < line 192 02:55:18; 32858bd 04:26:27, f6c8d95 04:26:44 < line 202 04:26:52; 57559de 05:29:31 < line 209 05:29:36; a2a12ad 05:33:12 < line 210 05:33:20). dod_track runs vs journal: t-086 run 11:22:40.9 / line 218 11:22:47; t-085 run 11:24:29.6 / line 219 11:24:29 (consistent).
Seconds-divisible-by-5 test (`python -B -c`): `lines1-27 sec%5==0 (25, 27)  lines28-223 (26, 196)`.
findings:
- t-057 `accepted` (line 159, 02:05) precedes its worker's SubagentHandback (transcript 01:12:16Z = 02:12:16 local) by 416 s. Reading 1: the ts was not read from the clock; reading 2: the Lead accepted from the worktree before the worker delivered (then the acceptance preceded the handback it rests on). Either is a `ts`/witness-order defect.
- t-045 `delegated` (line 96, 00:01) is 39 s before the worker's first line; the rule writes `delegated` AFTER the dispatch returns.
- t-036 attempt-2 `delegated` (line 125, ts 01:35:xx) was written 56 min after its worker started (the worker file begins ~00:39): batch writing of `delegated`, not "same turn". Five more are 2-3 min late (t-059, t-062, t-063, t-064, t-076).
- Line 211 (b0f7079) ts is 14 s before the author/commit date of the commit it records.
- ambiguous: the 05.11 block (lines 1-27) has 25 of 27 `ts` on a 5-second grid (e.g. t-003..t-007 delegated 16:51:40/45/50/55/16:52:00, accepts 18:44:20..40) against 26 of 196 elsewhere (13% vs 93%); git does not contradict them (commits 76b99b8 15:36:05 after line 4 15:35:40), the transcripts of that day are not on this machine, and no line carries a `retroactive` mark. Reading 1: written by hand from narrative (a retro block unmarked); reading 2: five sequential Edit writes by one session. Cannot be settled without the 05.11 transcripts ("not measured").
- Known past ts errors: none recorded in the journal (`grep -ci "ts drift\|wrong ts"` not run: no `calibrated` event, no correcting event exists).

### 13(g) SessionStart hook liveness
verdict: ok for liveness; ambiguous for the marker
evidence (`grep -o` over the three transcripts of this project):
- `NOW: 2026-11-11 20:26:18 Wednesday (local system clock)` (a3462969), `NOW: 2026-11-11 21:37:52 Wednesday (local system clock)` (1624cb4a), `NOW: 2026-11-12 11:12:08 Thursday (local system clock)` (f92520fc).
- Closing literal: `BOOT LAYER A INJECTED -- 4 files, 40094 bytes on disk ---` (a3462969), `-- 4 files, 22305 bytes ---` (1624cb4a), `-- 2 files, 8174 bytes ---` (f92520fc).
- The MODEL line in all three: `MODEL: not provided by hook input -- verify tier yourself`. Marker "declared by harness, not measured": present in `tools/session_context.py:1012` as `(declared by harness, not measured; Lead tier = fable)`, absent from the three emitted MODEL lines (the hook input carried no model).
- Preflight/tooling: the one `rejected failure_class=tooling` is t-077 (line 194: a defect of the split tool, not a provider quota error); `tools/preflight_quota.py` exists (Glob).
findings:
- ambiguous: the marker "declared by harness, not measured" does not appear on any emitted MODEL line of the window. Reading 1: the marker disappeared (regression, per the check text); reading 2: it is printed only when the harness supplies a model, and the honest alternative wording "not provided by hook input -- verify tier yourself" took its place here. The code at session_context.py:1012 should be read to settle it.

### 13(h) traffic_kind honesty
verdict: not applicable (no gateway `requests` table; the cc_usage track has one traffic kind)
evidence: `python -B -c` on `gateway/requests.db` (opened read-only): tables `[('cc_usage',), ('sqlite_sequence',)]` -- no `requests` table (positive control: the same query lists cc_usage). cc_usage `group by traffic_kind` -> `[('real', 4136, 181.67)]`. Signature scan on cc_usage: rows with total tokens < 100: 0 (the smallest row has 45,588 tokens; the same query with `< 50000` would return rows); ts groups with several models: 1 (`2026-11-11T23:23:23.172Z`, 2 models; control: the same grouping with `count(*) > 1` returns 1 group), i.e. no multi-alias batch.
findings: none. Side effect to know: `usage_report.py` imports transcripts into the git-ignored `gateway/requests.db` (`.gitignore:2 gateway/*.db`); the file already existed (4027 rows before; my first run printed `109 new row(s) imported`; now 4136 rows, ts 2026-11-05T15:06 .. 2026-11-12T10:34Z).

### 13(i) phantom dispatches
verdict: finding
evidence: `python -B tools/calibration_counts.py` -> `Unclosed tasks: t-073@dev1, t-084@dev1, t-087@dev1, t-088@dev1, t-089@dev1, t-090@dev1`. `delegated` without `worker_ref`: 0 (`Missing typed fields: (none)`). worker_ref -> transcript lookup (`python -B -c`, glob `agent-*.jsonl`): `106 delegated; no transcript: 11` -- the 11 are all 05.11 (t-001..t-011), whose transcripts are not on this machine. Worker states (`.meta.json finished`): t-073 `aa881de274d1ace2d` finished, last line 01:48:34Z "Report delivered to your caller"; t-084 `a96c92208c5880c7` finished 11:36:57; t-087 finished 11:42:56; t-089 finished 11:42:00; t-090 `ae2965cf326015f0` live at 11:43; t-088 is this worker.
Spot-check of 2 worker_refs against transcripts: `agent-aa881de274d1ace2d` (t-073, agentType builder, description "T-2 ... source_split.py") and `agent-a3bef32be9d80b992` (t-086, owns lines match the journal's dispatch) exist and match their task.
findings:
- t-073 is a delivered result with no disposition after 9 h and two session changes (opened by 1624cb4a; the SessionStart line of f92520fc lists `OPEN DISPATCH: t-068 ... t-073`). Journal line 212 says "T-2 (t-073, not accepted)". Not a phantom (the worker existed and delivered): an unaccepted result left open.
- t-068 (line 170, 02:17) was open the same way until `closes:t-068` in line 215 (11:16): a worker that handed back PARTIAL at ~02:3x (line 172 notes) closed 9 h later by a token in another task's notes.
- t-084, t-087, t-089 are live-session results awaiting acceptance (not phantoms; the coordinator said so).
- 05.11 workers (t-001..t-011): worker_ref reality NOT MEASURED (no transcripts). What would measure it: the 05.11 sessions' transcripts (project dir `C--QAFactory` holds 3 sessions, none with `subagents/`).

### 13(j) narrowed witness scope of a parallel node
verdict: finding
evidence:
- Concurrent groups (`python -B <scratchpad>/groups.py`, builder `delegated`->`accepted|rejected` windows): `builder attempts 67 overlap clusters 3`: `11-05T16:51 -> 18:44 size 5 (t-003..t-007)`, `11-05T18:45 -> 19:59 size 2 (t-009,t-010)`, and one cluster from 11-11T23:22 of 52 attempts, chained into one by the never-closed t-073 window (true overlaps inside it are bounded by the writer count in 17(e): peak 6 per session).
- DATA SIGNATURE (full canonical run): `python -B -c` over witnesses: witness with `pytest tools/ ` or bare `selftest.py`: `[]`; witnesses with `selftest.py --lang|--limits`: 7 (narrow flags). No witness carries a full run.
- BATCH CANON carrier: `witness with BATCH CANON: []`; `notes with BATCH CANON: [(179, 'defect_found'), (202, 'accepted'), (203, 'defect_found'), (210, 'accepted'), (211, 'dispatch_skipped'), (212, 'dispatch_skipped')]`.
- THIRD SIGNATURE (`test_story_step.py`, every `test_story_run_*.py`, full selftest, docker, mutation RUN): hits only the word `mutation`: lines 177 (t-060: "builder's mutation probes on byte copies") and 209 (t-081: "three mutation probes red"); `test_story_step.py`, docker: none. t-003 (line 15) lists the story_run family tests individually (s7 live 44/44, controller_rework, ...), not all at once.
- SECOND SIGNATURE, sample of 2 nodes (`python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>`, 12 s each): t-085 owns `test_brief_pack.py` -> prints `keep test_codex_tool_guidance.py (layer detector, covers it)` and `keep test_fit_targets.py (layer gate_named, covers it)`; t-085's witness (line 219) ran `test_brief_pack.py` only. t-086 owns `harness.py` -> prints `keep` rows for every test file (hundreds; first `test_adapter_forms.py`, `test_ahead_cards.py`...); for `test_codex_tool_guidance.py` and `test_role_policy_reads.py` it prints `no scenario or keep row covers ...: run the whole scenario layer`; t-086's witness (line 218) ran those two files only. The other ~36 post-11.11 builder acceptances were not walked ("not measured": 12 s per path, owns taken from each dispatch text).
findings:
- No second full canonical run (the one-per-window rule is not breached on the DATA SIGNATURE).
- Rule 4 carrier: the canon output is never in a `witness` field; it lives in `notes` (179/203 are defects found by the canon; 211/212 are a self-executed `dispatch_skipped` carrying the green canon 43157607270 on b0f7079). Lines 202 and 210 promise "BATCH CANON to be appended when read" and no later `accepted` carries it (the last accepted of the batch was line 210; the canon was read at 05:52-06:07 and written into 211/212 as `dispatch_skipped`). A canon outside the `witness` field is not the carrier the check reads.
- ambiguous (second signature): CLAUDE.md rule 4 says the witness is "what `scenario_walk.py --witness-for <owns>` prints"; PROJECT.md item 2 and builder-rules 7b let the builder run only fast narrow witnesses ("up to a minute each"). For t-085/t-086 the printed list is far larger (hundreds of files, or "the whole scenario layer") than anything a builder can run. Reading 1: both nodes' DoDs are a dispatcher defect (second signature); reading 2: the printed list is the BATCH CANON's scope and the builder's witness is the own test (the rule 4 text is then unreachable for `harness.py`-owning nodes).
- THIRD signature word `mutation` (lines 177, 209): the builder ran "mutation probes on byte copies" (red probes), not a mutation-testing RUN; ambiguous whether the check's "mutation RUN" covers them. Plans/builder-rules 7b was not read for this; flagged to the Lead.

### 13(k) doc-dispatch witness
verdict: ok on the sample, (i) not verifiable
evidence: acceptances whose witness is not pytest but a key-presence script over markdown/config owns: t-029 (line 64) and t-024 (line 55, `verify_move.py`). t-029: `keys.py ... 11 of 11 PRESENT, OK, exit=0; --neg: MISSING docs/SIBLING_MAP.md :: THIS KEY IS DELIBERATELY ABSENT, FAIL, exit=1` -- (iii) negative control present. (ii) the journal says "source in the worker's report"; there is NO report file for t-029 (`ls docs/tasks/specs/reports | grep t-03` lists t-036..t-039 reports, control; nothing for t-024..t-031), but the worker's transcript `agent-ada148a765a33eea8.jsonl` holds the full `KEYS = [...]` source and 8 occurrences of the negative-control marker. t-024: `verify_move.py: 16 of 16 in HEAD 1 / now 0 / archive 1, control D-0002 1 / 1 / 0` -- a control row present. Other doc-only acceptances (t-058 line 133, t-076 line 183) run `piles.py check --all`, `board --check` and `pytest tools/test_pile_cards_contents.py`: committed deterministic gates, not key-presence scripts.
findings:
- ambiguous: t-029 (ii): source attached in the handback message (visible in the transcript), not in a committed or reported file; (i) keys quoted from the DoD before the run cannot be compared from the journal (the DoD text is in the dispatch only). t-024 names `verify_move.py` but `find . -name verify_move.py` (outside .claude/worktrees) returns nothing: the script is not in the repository and no report carries its source (not checked in the t-024 transcript), so its (ii) is not established either; its witness does show a control row (D-0002).

### 13(l) merge acknowledgements
verdict: no merge acknowledgements
evidence: `git log --merges --full-history --since=2026-11-05 --oneline -- logs/routing-log.jsonl | wc -l` -> `0`; `ls logs/routing-log.jsonl` -> No such file (the check names a file that does not exist here). Same shape on the live journal: `git log --merges --full-history --since=2026-11-05 --oneline -- logs/journal/dev1.jsonl` -> 8 merges (`4400381`, `f9c8a22`, `fd87296`, `26ba10c`, `e67e6d6`, `1bdf26b`, `9c1cf04`, `574d29e`). `grep -ci "merge-accepts:" logs/journal/dev1.jsonl` -> `0`; control, same grep shape: `grep -ci "closes:t-" logs/journal/dev1.jsonl` -> `2`.
findings:
- 0 `merge-accepts:` tokens for 8 merges that touched the journal file; the protocol text of 13(l) names `logs/routing-log.jsonl` (stale carrier in this repository: the journal is `logs/journal/<dev>.jsonl`).
- Adjacent, outside the check text: line 61 (t-028 accepted) is a builder diff of "108 lines of anchors, constants and pointers" plus the 41.5 KB CLAUDE.md copy accepted with "critic: skipped"; CLAUDE.md rule 3 makes the critic gate MANDATORY over roughly 100 lines or on core (the plan critic t-013 had walked the text). ambiguous: Reading 1: over 100 lines of the diff = a missed mandatory gate; Reading 2: the critic on the PLAN already gated it and the waiver is available to a Fable acceptor.

## Check 14 -- Golden set for recon, regression rule for prompt edits

verdict: not applicable for (a),(b),(e) (no exam set, no non-Claude run); (c) ok; (d) note owed; recorded pass for critic.md is D-0037/D-0063

### 14(a) role-file edits with an exam set
verdict: not applicable (the exam sets do not exist; the pass is the decision line)
evidence: `ls PROCESS/SCOUT_GOLDEN_SET.md PROCESS/CRITIC_EXAM.md` -> `No such file` for both (positive control: `ls PROCESS` lists 11 other files). `DECISIONS.md:33` D-0037: "Exams are deferred ... this line is the recorded pass of that gate (P13) ... Detector: calibration check 14(a) reads this decision as the pass"; `DECISIONS.md:43` D-0063 repeats it for critic rule 19 ("`PROCESS/CRITIC_EXAM.md` does not exist ... this line is the recorded pass"). `git log --since=2026-11-05 --format='%h %ad %s' -- .claude/agents` -> `94702be 11-11T22:46 policy: CLAUDE.md is rewritten ...`, `5498318 11-11T18:40 Merge the experiment line into main ...`, `9ac00f0 11-05T14:04 Initial import`. `git diff 9ac00f0 HEAD -- .claude/agents` -> `builder.md 5 +-, critic.md 9 +, designer.md 25 +-`; `git diff 9ac00f0 HEAD -- .claude/agents | grep '^[+-]model:'` -> empty (no `model:` change; frontmatter now: builder claude-sonnet-5-5, critic claude-opus-5-5, designer claude-opus-5-5, scout claude-sonnet-5-5, judge `sonnet`). `scout.md`: no edit in the window.
findings: none against the check's own text: critic.md edited (+9 lines, merge 5498318) with no Runs-log line because no exam file exists; D-0037/D-0063 are the recorded pass. ambiguous: the 5498318 edit date (11.11 18:40) precedes the first journal event of the 11.11 session but is after the journal's start (05.11), so it is in the window; whether D-0063 (06.11) covers the +9 lines of 5498318 specifically cannot be read from the carriers (no diff-to-rule map).

### 14(b) key liveness
verdict: not applicable (no set; `not measured`: the exam sets are deferred by D-0037)
evidence: no `PROCESS/SCOUT_GOLDEN_SET.md` (above). Scout acceptances ran under "the strict form R1 b" per D-0037: e.g. line 29 (t-012) `Strict form (R1 b): checked the anchors ... negatives ... with a positive control`, lines 46-52 (t-016..t-022) each name an own grep/read of the digest's claim.
findings: none.

### 14(c) rise in `failure_class=recon`
verdict: ok (no rise: 0)
evidence: `Rejected by failure_class` table above: no `recon` row; `python -B tools/calibration_counts.py` (control: the table does list `spec` and `tooling`). No previous window to compare (first calibration).
findings: none.

### 14(d) edits to role files with no exam set
verdict: note owed in the `calibrated` event
evidence: builder.md (+4/-1) and designer.md (+20/-?, 5 lines more in 94702be) edited in commits 5498318 and 94702be (above); both have no exam set by design (execution-based acceptance).
findings: the `calibrated` event notes must carry: "builder.md edited in 5498318, designer.md in 5498318 and 94702be, no exam set (D-0037)" -- no `calibrated` event exists yet.

### 14(e) fabrication guard for non-Claude runs
verdict: ok (no such runs; guard live)
evidence: `grep -ci "pi_run_guard" logs/journal/dev1.jsonl` -> `0` (control, same shape: `grep -ci "dispatch_skipped" logs/journal/dev1.jsonl` -> `14`); the models in the journal are only `claude-sonnet-5-5` and `claude-opus-5-5` (`python -B -c` Counter over `model`). Guard liveness: `python -B tools/pi_run_guard.py --json <scratchpad>/badreplay.jsonl` (a stream with 0 `tool_execution_start` events and a confident final answer with a "Trail") -> `verdict: REJECTED` / `reason: zero structural tool calls with a substantive final answer`, rc=1; control `goodreplay.jsonl` (1 tool call) -> `verdict: PASS`, rc=0.
findings: none.

## Check 15 -- Repeated critic findings -> codification, attribution

verdict: finding
Evidence base and its limit: the 17 verdict files of the window total 448 KB; I did not read them end to end. Classes and attributions below are taken from (1) the Lead's own `rejected`/`accepted` notes (lines cited), (2) the verdict headers/blocking sections I read (t-040, t-041, t-042, t-045, t-054 x2, t-056, t-061, t-062, t-072, t-079), and (3) `python -B tools/calibration_counts.py`. Acceptance of this check's output is textual (check text).

### 15(ii) attribution of the 14 `rejected` events (primary cause = earliest in the chain)
| line | task | tier / class | primary | second | basis |
|---|---|---|---|---|---|
| 44 | t-013 | designer / spec | performer (the draft: size cut left to the builder, N2 witness on N1's files, checks 2 and 20 cite removed text) | -- | critic verdict t-013 (B1-B3, F1-F6, Q1-Q3); ambiguous: the intent brief is not in the journal, so a brief gap cannot be excluded |
| 92 | t-039 | builder / spec | DISPATCHER (world key by qualname, unguarded delete "come from the spec's own text") | performer (a reset that swallows a failure) | line 92 |
| 93 | t-038 | builder / spec | DISPATCHER (builds counted from tempdir events, builder seconds from intervals: "the spec's design") | -- | line 93 |
| 98 | t-044 | builder / spec | DISPATCHER (the brief named one scenario, not the class) | -- | line 98 |
| 124 | t-036 | builder / capability | DISPATCHER for B4 ("partly a spec defect of the Lead") | performer (B1-B3: four inputs move code wrongly under green proofs) | line 124 |
| 130 | t-047 | builder / spec | DISPATCHER ("Mostly spec: the brief said co_names and was silent on mock's create exit") | performer (M1-M4) | line 130 |
| 137 | t-049 | builder / spec | DISPATCHER (F1 left to node P0-D, which the brief had dropped) | -- | line 137 |
| 139 | t-054 | builder / spec | DISPATCHER ("The spec let the builder skip" the E5 pin) | -- | line 139 |
| 144 | t-057 | builder / spec | DISPATCHER (R1 "not in the owns I gave") | -- | line 144 |
| 146 | t-056 | builder / spec | DISPATCHER (K6 control "outside the owns I gave") | -- | line 146 |
| 153 | t-053 | builder / capability | performer (runner shapes refused though reported handled; PROOF ok on seven lossy classes) | -- | line 153 |
| 155 | t-048 | builder / spec | unattributed (the note names C-B1, C-B2 findings but not whose gap; ambiguous: spec of the K5 door or builder) | -- | line 155 |
| 165 | t-060 | builder / spec | DISPATCHER ("DoD items 4 and 6 were narrower than spec B 2.6") | -- | line 165 |
| 194 | t-077 | builder / tooling | an earlier node's tool defect (the T-1/T-1b split tool wrote mixin class names into NO_MOVE_BASELINE rows); the builder "edited nothing by hand: correct" | -- | line 194 |

### 15(iii) cluster count (to go into the `calibrated` event notes)
Dispatcher 10 (t-039, t-038, t-044, t-036, t-047, t-049, t-054, t-057, t-056, t-060); performer 2 (t-013, t-053); earlier-node tooling 1 (t-077); unattributed 1 (t-048) = 14. Dispatcher causes split into two clusters:
- Cluster A, "the DoD/owns did not carry the sibling class or the surface the change touches": t-044, t-049, t-054, t-056, t-057, t-060 = 6; the same class in `defect_found`: t-005 (line 22: "narrowed witness did not include test_audit_rules (dispatcher's scope miss)") = 7. Also in `accepted` notes: line 164 (t-062: "Both blockers come from the Lead's dispatch narrowing the spec") and line 123 (t-045: "Spec defect noted: fix item 4 named the stored ratchet") belong to the same class.
- Cluster B, "the spec's own design/premise wrong or silent on an edge of the mechanism": t-038, t-039, t-047, t-036 (B4) = 4.
- Cluster C (id issue, 13(e)): 4 events of dispatch texts carrying ids issued before the journal tail was re-read.
- Verdict-level classes that recur in the critic reports (not only rejects), by journal notes and headers: (V1) a check/proof that cannot fail or a pin that is vacuous: t-045 (P7 cannot fail, P2/P3/P5 cannot pass on the real tree), t-054 (E5 unpinned), t-056 (K6 control measures length), t-061 (PROOF ok on 7 lossy classes, K5 door too wide), t-062 (equal-rank import passes; the exception pin 14 rows against 8) = 5; (V2) readers of moved or changed code not swept after a cut: t-079 B1 (test_silent_passes:547), t-080 (kept tests read `story_run.__file__`: "A class P0-C missed"), t-049 F1 (words_doors inventory keyed by one path), t-072 Q5 (four carriers turn the canon red if the closing commit misses them), plus `defect_found` t-054 (probe_walk_edges call-count pin), t-060 (test_exploratory_findings K-M3 reader moved), t-053 (audit A1) = 7; (V3) a tool/proof green on synthetic input but wrong on the real tree: t-045 B2/B3, t-061 (tool refuses 3 of 6 wave-1 files), t-077 (mixin names into baseline rows), t-071 (two defects the N2 cut exposed) = 4.
- Codified already? CLAUDE.md rule 11 (edges named; POSITIONAL invariant), rule 9 (class, siblings by the map) and the five-point checklist (3) "given enumerated AND sufficient", (4) owns. Cluster A and V2 are repeats of those: "a repeat of an ALREADY-codified class is itself a finding -- the codification leaked". Whether a line "the DoD names the readers/pins of what the cut moves" exists in `docs/SIBLING_MAP.md` was not read by me (not measured).
- (v) next-window goal: none to compare (first run).
- (vi) the window has 14 rejects and NO `calibrated` event: the cluster count is not yet recorded -- visible leak until the Lead writes it.
findings:
- Cluster A (6 rejects + t-005) and V2 (7 events) exceed the landing threshold (2): landing into the pre-dispatch checklist is mandatory (Lead-tier edit of CLAUDE.md), or an explicit line `not codified: <why>`. Not for me to decide.
- t-048 is `unattributed` (cause not named in the note).

## Check 16 -- Two-pass external recon

verdict: not applicable (no new RELATED_WORK entry or external survey in the window)
evidence: `git log --since=2026-11-05 --format='%h %ad %s' --date=format:%m-%dT%H:%M -- docs/RELATED_WORK.md` -> only `9ac00f0 11-05T14:04 Initial import` (the file's last change; it holds sections 1 DMtools 01.10.2026 and 2 Testing Factory 21.10.2026, i.e. entries from before the window; `wc -l` 219). The window's scout surveys t-012, t-015, t-016..t-022, t-033, t-034 are all internal recon (journal lines 28-52, 73-76); `python -B -c` over the journal for `external|RELATED_WORK|survey|dmtools|testing-factory` in `notes` -> `[]` (control: the same regex over `notes` finds nothing else to compare, so I also ran the case-insensitive Grep of `docs/RELATED_WORK.md` for `проход` which matched lines 4, 5, 14, 25, 81, 93).
For the two pre-window entries (outside the check's period, for the Lead's information): section 1 has `Первый проход (скауты, Sonnet)` (line 14) and `Второй проход Lead (18:05-18:25, сырые файлы через WebFetch, замер в копии через PowerShell, только чтение)` (line 25); section 2 has `Первый проход` (line 81) and `Второй проход Lead (13:2x-14:0x, чтение копии, только чтение)` (line 93): both carry the second-pass trail.
findings: none. Empty window: "no new RELATED_WORK entries in the window".

## Check 17 -- Cost gates

verdict: finding (d: Lead context; b: resumed fix round; e: cross-session count; stale protocol text)
Method: `python -B <scratchpad>/c17.py` (max context per assistant turn = input + cache_creation + cache_read, the definition of `tools/agent_budget.py`/`transcripts.usage_total`) over 95 subagent transcripts and 3 main transcripts of this project. `tools/agent_budget.py` is a PreToolUse hook (no reporting command; `python -B tools/agent_budget.py --help` prints nothing, rc=0); the weights are `tools/hop_metrics.py:80` `UNIT_WEIGHTS = {"input": 1, "cache_write": 2, "cache_read": 0.1, "output": 5}`. D-0035/D-0038/D-0040/D-0054 were not re-read in full; the cap value comes from `tools/dispatch_gate.py:1482,1512` (`PARALLEL_CAP = 6`, "the owner's word 20.10.2026, D-0054; was 4").

### 17(a) workers over 400K
verdict: ok
evidence: `c17.py` -> `workers 95`; `workers with MAX ctx > 400000 : []`; control, the same code with 250000: 11 workers (`a45e1429b80322c7a` designer 303130, `a110ec62b87cd5a38` designer 301382, `aa881de274d1ace2d` builder 297479, `a6f226faee4f8c95c` designer 294631, `a72b9f65526f4b5b4` builder 293011, ...). Max in the window: 303,130.
findings: none.

### 17(b) fix rounds by a RESUMED worker
verdict: finding (1)
evidence: `python -B -c` over the three main transcripts, every `tool_use` of `SendMessage` with its target's `agentType`:
```
1624cb4a 2026-11-11T21:39:55 to a110ec62b87cd5a38 designer | resume stalled designer C
1624cb4a 2026-11-12T01:35:16 to a9019c715d47bb888 builder | P1-1b: take alternative (b), finish the node
1624cb4a 2026-11-12T02:35:50 to a18313c63c78040c6 builder | P1-2b: answers Q1-Q3, finish the apply
1624cb4a 2026-11-12T04:28:36 to a7794056795e8efa6 builder | t-082: three fixes from the critic, then done
a3462969 2026-11-11T23:32:16 to a5654076c5623b2dd critic | Owner answered F-2 (b); judge it too
f92520fc 2026-11-12T10:21:38 to a21cff40bd05f5bfc builder | PC2-1 fork answered: option (a), value pin
```
(plus 3 SendMessage calls to peer-session/pipe targets, not workers).
findings:
- t-082 (worker a7794056795e8efa6; journal lines 207-210): the critic's verdict t-083 (F1, F2, F4) was sent as a message to the SAME builder (line 208: "Fixes sent back to the same builder (t-082)") -- a fix round by a RESUMED worker after a critic verdict; expected 0; the fresh-worker rule (rule 12 Cost gates) is the codified class.
- Not fix rounds but resumed builders: t-074 (a9019c715d47bb888) and t-078 (a18313c63c78040c6) were messaged with answers to forks/questions (not after a critic verdict); t-085 (a21cff40bd05f5bfc) with a Lead fork answer. Designer t-027 resumed after a 600 s stall; critic t-050 got an addition. Ambiguous: the check names only "a SendMessage to a builder after a critic verdict"; a fork answer is not that, but it keeps one builder context alive across a decision (Reading 1: legitimate; Reading 2: the same class of context re-reading).

### 17(c) critic entries per task_id, re-review scope, critic-on-plan
verdict: ok on counts; ambiguous on the topic reading
evidence: `python -B tools/calibration_counts.py` repeat table: `critic-entry` repeats: t-013 (line 35), t-054 (122), t-057 (141), t-056 (142). Critic `delegated` events: 18; max per task_id: 1 critic dispatch (the repeats are on the builder task's own id: builder + 1 critic + builder attempt 2). Critic dispatches: plan: t-013, t-032, t-046, t-050, t-051 (each spec carries forks per the notes: F1-F9, F1-F3, F-2, F1-F7); code: t-008, t-040, t-045, t-054, t-055, t-056, t-057, t-059, t-061, t-062, t-072, t-079, t-083. Re-review: t-083 is "Focused critic on t-082" (a fix-diff-sized question), the fix rounds of t-009, t-036, t-047, t-048, t-049, t-053, t-054, t-056, t-057, t-060 were accepted "no second pass" or on the verdict (e.g. line 135 "no second pass").
findings: none by the counts. ambiguous: R13-g "ONE critic pass per TOPIC": TD-11 got one plan pass (t-032) and nine code passes (t-040, t-045, t-055, t-059, t-061, t-062, t-072, t-079, t-083), each on a distinct node's diff. Reading 1: the node is the topic (ok); Reading 2: TD-11 is one topic (9 passes).

### 17(d) Lead context, stage commits, note length, CI reads
verdict: finding
evidence:
```
MAIN 1624cb4a turns 833 median 361780 max 679370 turns>600K 109 turns>350K 441 2026-11-11T20:37:57Z .. 2026-11-12T05:50:06Z
MAIN a3462969 turns 746 median 270423 max 429359 turns>600K 0 turns>350K 157 2026-11-11T19:26:23Z .. 2026-11-12T01:47:01Z
MAIN f92520fc turns 139 median 209188 max 292138 turns>600K 0 turns>350K 0 2026-11-12T10:12:13Z .. 2026-11-12T10:32:08Z
```
(`c17.py`). The 109 turns over 600K are all in 1624cb4a between 03:26:33Z and 05:08:22Z. Compaction events in 1624cb4a (`"subtype":"compact_boundary"|isCompactSummary`): 21:08:13Z and 23:35:53Z (2 events, each twice in the file); none after 23:35Z. Journal notes over 300 chars: `python -B -c` -> `notes>300 24 of 223 max 412` (lines 7, 34, 45, 75, 76, 91, 116, 142, 144, 162, 163, 176, 184, 190, 192, 193, 196, 198, 200, 203, 208, 211, 212, 213; all of them are after 07.10.2026 23:00). Stage commits per merge: `git log --since=2026-11-05 --merges --oneline | wc -l` -> 9; `--format=%s | grep -ci stage` -> 4 (all four are ordinary commits whose subject contains the word, none is a "stage commit" label). CI reads: `grep -c '"type":"tool_use","id":"[^"]*","name":"mcp__[^"]*[Bb]rowser'` -> 0, 0, 0 in the three transcripts of this project; same-shape control on parent-folder session fc171a1f -> 2: `mcp__Claude_Browser__browser_batch` navigate `https://github.com/Xartaxana/Forge-for-QAFactory/actions/runs/43074944592/job/130712203271` and `.../commit/5498318.../checks/130712203271/logs` (11.11 18:23-18:37Z, cwd `/c/QAFactory/forge-repo`). `ci_read.py` usage in the Lead's sessions: not counted.
findings:
- 1624cb4a: median 361,780 > the 350K target; 109 turns over 600K ("a turn over 600K means a compaction was skipped"): from 04:26 to 06:08 local, 1 h 42 min with no compaction. (Owner's line "context ~NNNK, snapshot ready" is PROJECT.md's duty at ~300K: the snapshots of 11.12 are `docs/tasks/compact-snapshots/2026-11-12-0018|0021|0034-manual.md` and `2026-11-11-2204|2207`; I did not check whether a snapshot was announced at the 600K crossing.)
- 24 of 223 notes (10.8%) exceed 300 chars (`journal_echo` warns).
- Two CI-log reads through the browser in session fc171a1f (a parallel session of the same clone, outside this project's transcript folder); the check says "CI reads through the browser instead of `tools/ci_read.py`".
- Stage commits per merge: not measured (no mechanical definition of "stage commit"; the journal line 192 names one: "TD-11 stage committed on td-11-integration (1843dfd tools, 88e6d4d package, 16ffac7 split-keep...)"; 9 merges in the window).

### 17(e) writing workers alive at once
verdict: finding (cross-session sum; stale protocol text)
evidence: `python -B <scratchpad>/conc.py` (workers with `agentType: builder`, first->last transcript timestamp): per session `1624cb4a builder-type workers 33 max concurrent 6 2026-11-12T01:00:19Z`, `a3462969 ... 18 ... 3 ...`, `f92520fc ... 7 ... 5 2026-11-12T10:30:05Z`; all sessions together: 58 builder-type workers, max 8 at 2026-11-12T01:00:19Z-01:06:03Z (>= 5 for 5,520 s, >= 6 for 724 s, >= 7 for 449 s, >= 8 for 351 s; 21 segments over 4). `grep -c budget-skip` in the journal: 0; in the 95 dispatch texts: 0 (control: 3 `manifest-skip:` lines in the same loop). `.claude/dispatch_claims/` holds `*.owns_gate` claim files (listed, not counted).
findings:
- The protocol text says "more than 4 WRITING workers alive at once (`dispatch_gate.py` blocks; D-0040 ...)"; CLAUDE.md rule 12 and `dispatch_gate.py:1512` say 6 (D-0054). By the protocol's literal 4: sessions 1624cb4a (6) and f92520fc (5) exceeded it; by the live cap (6) no session exceeded it. The protocol text is stale (protocol/CLAUDE.md pair divergence).
- 8 builder-type workers at once at 01:00Z: the two parallel sessions of 11-12 (1624cb4a and a3462969) each stayed within its cap (the gate counts the current session's subagents folder, `dispatch_gate.py:1483`), their sum is 8. The cap invariant ("at most six writing workers, each re-reading ...") is per session; two sessions in one clone double it.
- Estimate label: worker alive = first->last transcript line (not `finished`/mtime window), "estimate, not verified" against the gate's own live test.

### 17(f) effective units per merged node vs the 0.9 baseline
verdict: not measured as "per merged node" (definition absent); a window figure is given
evidence: `python -B tools/usage_report.py --days 7` totals: `4136 turns, 8524+5006823 tok (+21807955 cache-write, +704774568 cache-read)`. Units by `UNIT_WEIGHTS` (python arithmetic): `8524*1 + 5006823*5 + 21807955*2 + 704774568*0.1 = 139,136,006` (139.1M). Per distinct builder-accepted task (47): 2.96M; per accepted event (82): 1.70M. Baseline for comparison (check text): 48M per node, 1113M for 23 nodes; "working" = under half (24M per node).
findings: the journal has no definition of "merged node"; per accepted unit the window is at about 6% (builder) / 4% (all) of the baseline per node, an order of magnitude, with these caveats: the totals include the parent-folder project (202 turns of the `C--QAFactory` sessions), the 05.11 sidechains are absent (no transcripts: 11 of the 82 acceptances have no cost in the numerator), and the input weight 1 is an assumption (hop_metrics.py:22-23).

## Check 18 -- Economic trend

verdict: baseline recorded with caveats; no previous data point exists (first calibration; `Last calibration: NONE` in all three SessionStart lines, no `calibrated` event in the journal: `python -B tools/calibration_counts.py` event table has none)
Commands: `python -B tools/usage_report.py --days 7`; `python -B tools/savings_report.py --routed-start 2026-11-05 --until 2026-11-13`; SQL on the read-only `gateway/requests.db` (`cc_usage`). `--routed-start 2026-11-05` is my choice (the first journal date; pre-routing: 0 turns, `$0.00`); `--until` is EXCLUSIVE: the run with `--until 2026-11-12` (the literal "end of window" date) drops 11.12 (2162 turns, `$109.35`, `2 days, $54.67/day`, `gross savings=$190.96 (64%)`) -- the trap is that 11.12 is a $72.32 day; the figures below use `--until 2026-11-13`.
```
===== ROUTED (>= 2026-11-05 .. 2026-11-13) =====
  claude-opus-5-5   side turns= 1234 sess= 2 cost=$ 108.10 $/turn=0.0876
  claude-sonnet-5-5 side turns= 1924 sess= 3 cost=$  73.29 $/turn=0.0381
  claude-sonnet-5-5 main turns=   17 sess= 1 cost=$   0.27 $/turn=0.0162
  claude-fable-5-2  main turns=  961 sess= 5 cost=$   0.00 $/turn=0.0000
  TOTAL: 4136 turns, $181.67, 3 days, $60.56/day (partial: 961 turn(s) without a price -- claude-fable-5-2)
===== COUNTERFACTUAL: routed sidechains at the top-tier model's rates =====
  top-tier model: claude-fable-5-1 (roles.lead in delegation.config.yaml)
  builder claude-sonnet-5-5 turns=1648 actual=$ 62.12 as-top-tier=$ 261.17
  critic  claude-opus-5-5   turns= 732 actual=$ 58.27 as-top-tier=$ 120.24
  designer claude-opus-5-5  turns= 502 actual=$ 49.83 as-top-tier=$ 105.44
  scout   claude-sonnet-5-5 turns= 276 actual=$ 11.17 as-top-tier=$  48.45
  TOTAL: actual=$181.40  as-top-tier=$535.29  gross savings=$353.90 (66%)
===== API CONTOUR (requests.db, full history) ===== not measured (no `requests` table)
```
`usage_report` per day: `2026-11-05: 17 turns, $0.2748; 2026-11-11: 2145 turns, $109.0740; 2026-11-12: 1974 turns, $72.3224` (11.12 ends at 11:30 local, a partial day).

### 18(a) $/day, routed window
verdict: measured, a floor
evidence: `$60.56/day` over 3 calendar days (4136 turns, `$181.67`); the daily rows above.
findings: the number EXCLUDES the Lead's own main-session cost: 961 `claude-fable-5-2` turns carry no price (`unknown price: claude-fable-5-2: 961 turn(s)`, `tools/model_prices.json` has rows `claude-fable-5` and `claude-fable-5-1` only, grep control: `claude-opus-5-5` found), 297.9M cache-read tokens among them (the largest consumer). Also the "3 days" divisor counts 05.11 ($0.27, 17 turns of a parent-folder session) as a full day: the active days are 2 (11.11, 11.12, the latter partial).

### 18(b) gross savings vs delegation counterfactual
verdict: measured
evidence: `$353.90 (66%)` (actual sidechains $181.40 priced as top-tier $535.29 at claude-fable-5-1 rates, `delegation.config.yaml` roles.lead). `delegation.config.yaml`: lead `claude-fable-5-1`, critic `claude-opus-5-5`; actual main sessions run `claude-fable-5-2` (the usage rows), the counterfactual rates are those of fable-5-1 (the table has no fable-5-2 row).
findings: none beyond the caveat: the counterfactual prices the same token profile; coordination premium not separable.

### 18(c) cost per accepted unit
verdict: measured with two denominators
evidence: sidechain actual `$181.40` (SQL: `select is_sidechain, count(*), round(sum(accounted_cost_usd),2) from cc_usage group by 1` -> `(1, 3158, 181.4)`); accepted count `python -B -c` -> `accepted 82 on 11-05 11 distinct task ids 82`; builder `47 distinct 47 11-05 9`. `$181.40 / 82 = $2.21`; the 05.11 acceptances have no transcripts, so the like-for-like figure is `$181.40 / 71 = $2.55`; builder only `$62.12 / 38 = $1.63` (38 = builder acceptances after 05.11).
findings: none; a number is not a trend (one point).

### 18(d) API-track accounting and real-traffic share
verdict: not measured for the API contour; cc_usage rollup given
evidence: `python -B tools/savings_report.py ...` -> `API CONTOUR ... not measured (no requests table)`; the contour is `subscription` (`delegation.config.yaml`). Literal for the `calibrated` event notes where it applies: `n/a: no usage DB` for the API track (a `gateway/requests.db` exists but holds only `cc_usage`). cc_usage rollup by traffic_kind: `[('real', 4136, 181.67)]` = real share 100% of rows and of cost (SQL above).
findings: none (no leak line: `savings report: n/a` did not appear and no traceback).

Caveats to carry alongside the baseline (check text): taken while mechanisms are still being built (TD-11, the policy rewrite, the test split), so censored; the coordination premium is not separable from non-delegable Lead work; the Lead tier is unpriced (floor); two calendar days of real activity.

## Needed beyond the manifest

- `tools/journal_echo.py` (WITNESS ECHO text), `.claude/dod_track/*.json` (runs behind lines 218/219), `tools/transcripts.py`, `tools/hop_metrics.py:80`, `tools/dispatch_gate.py:1477-1515` (cap), `tools/session_context.py:993-1012` (MODEL marker), `tools/pi_run_guard.py`, `gateway/requests.db` (read-only), `tools/model_prices.json` (grep), `ai-packages/qa-factory/scripts/tests/scenario_walk.py` (run), `.claude/agents/*.md` frontmatter, `DECISIONS.md:33,43`, `docs/tasks/specs/reports/` (listing and 42-report scan), `~/.claude/projects/C--QAFactory-forge-repo/**` (3 main + 95 agent transcripts, meta files), `~/.claude/projects/C--QAFactory/**` (parent project sessions, one browser CI read), `git log/diff` for `.claude/agents`, `docs/RELATED_WORK.md`, merges.
- Not available / not read: `plans/builder-rules.md` 7b (cited indirectly), `docs/SIBLING_MAP.md` (whether the class of V2 has an axis), the dispatch texts beyond header-line regexes, 12 of the 17 critic verdicts end to end, `D-0035/38/40/54` text.

## Notes on my own run

- Side effects: (1) `usage_report.py` (named by check 18) imports transcripts into the git-ignored `gateway/requests.db` (`cc_usage`, 4136 rows after the run); (2) several of my Bash calls began with `cd` (the PreToolUse hook answered WARN, never blocked); the shell's cwd changes do not persist across calls and I changed no file outside this report and the scratchpad (`git status --porcelain` at the end: only the live journal tail is tracked-modified; the two td-11 spec files that were modified at session start are no longer, so another session committed them meanwhile, not me).
- Scripts run (scratchpad `C:\Users\i_mas\AppData\Local\Temp\claude\b3e3188b390a00d9\f92520fc-f552-4e47-9d06-efbc3daae572\scratchpad\`): `c17.py`, `conc.py`, `groups.py`, `clock.py`, `manifest.py`, `ov.txt`/`notes.txt` (journal views), `badreplay.jsonl`, `goodreplay.jsonl`. All read-only on the repository.

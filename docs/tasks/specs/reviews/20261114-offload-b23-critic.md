# t-871 — critic on offload B23 (t-869): dispatch-record hooks, journal Edit/Write gate, dod_track

Reviewer: critic (Opus). Scope: the verdict layer on the staged B23 tree in `.claude/worktrees/offload-b23` (patch
`docs/tasks/handoffs/t-869-B23.patch`), against spec r2 §3 B23 (lines 446-543) and §7. Out of scope: B0/B1 (t-865), topic C, CI.

**Verdict: GO WITH FIXES** — 1 blocking finding (F1), 2 major (F2, F3), 4 minor (F4-F7). The decision to accept belongs to the
Lead (Fable). This review does not accept anything.

## Findings

### F1 (BLOCKER) — a stop whose cwd is a linked worktree with no `tools/dev.config.yaml` loses `returned` silently
`tools/journal_hooks.py:339`: `if _journal_file(root) is None: return []`. Here `root` is the STOP payload's cwd. This check
runs BEFORE `_locate`. The index (`<common>/forge-journal/open/<id>`) and the scan over all worktrees are never reached, no
pending marker is created, and no WARN is printed. Two facts make this a live case:
- `tools/dev.config.yaml` is untracked, so no linked worktree has it. Measured: every `.claude/worktrees/*` folder printed
  `NO` (a3-fix, agent-a02f…, … 20 of 20 listed, offload-b23 too); only the root has it.
- Step 0 (d), the cwd of the SubagentStop payload for a worktree-isolated worker, was NOT measured. The builder's report says
  "the design does not depend on it". That is false at this line. If the host sends the worker's own worktree as cwd, every
  isolated builder's `returned` is lost, with no marker, so the 24 h "returned lost" WARN never fires either. Only the weekly
  check 48(c) would see it.

Probe, run by me (`scratchpad/probe_f1b.py`: a temp repo with dev.config in the root, a linked worktree without it, the B23
modules imported from the worktree). Verbatim:
```
linked worktree has dev.config: False
post-agent: ['JOURNAL: delegated t-001 written (logs/journal/probe.jsonl:2); task id issued by the hook: t-001 (the dispatch named none)', ...]
index exists: True
record_returned (stop cwd = linked worktree): []
events after stop from worktree cwd: ['journal_created', 'delegated']
pending marker: []
record_returned (stop cwd = main): ['JOURNAL: returned t-001 written (logs/journal/probe.jsonl:3)']
```
The index was there, and nothing used it. This breaks the E-B23-10 invariant ("a `returned` is written into the same copy as
its `delegated`, or a loud WARN says it was lost"). The tests miss it because the E-B23-10 rows seed a dev.config in the
linked worktree.

Fix: drop the guard at :339, or move it after `_locate` and judge it over `jw.worktrees_of(root)`. The index and markers live
in the common dir, so they work from any worktree. Return early only when no worktree of the clone has a journal. Add a row:
the stop comes from a linked worktree with no dev.config, and `returned` is written into the root copy through the index, and
through the scan when the index is gone.
Spec side (the dispatcher's): §3 B23 step 0 lets the design go ahead on an unmeasured (d) while claiming the design does not
depend on it. Item 2 says what to do when there is no index (the scan) but says nothing about a stop root that has no journal.

### F2 (MAJOR) — the WARN lines on the stop side go to a channel nobody reads
`tools/dod_gate.py:571-572` writes `record_returned`'s lines to stderr, and dod_gate exits 0. Under the host's hook semantics
(documented behaviour, not measured here), stderr on exit 0 is not delivered to the model. So these lines are invisible:
- `JOURNAL: returned NOT written for agent:… write it: …` (`journal_hooks.py:313-314`), for example after a 5 s lock timeout;
- the prune WARNs printed from the stop path (`returned lost …`, `index entry … pruned`).

On the not-written path no marker is left, because `_write_returned` gets the PENDING path and the marker may not exist. So
nothing retries. Spec item 3 says these WARNs are "read by check 48(c)", and §6.4 (b) reads `NOT written` lines through
`warn_density.py`. If the stop-side lines never reach a transcript, the only detector left is 48(c)'s coverage count.
Fix, one of: (a) on a not-written `returned`, create the pending marker anyway, so the next post-agent or prune surfaces it on
the PostToolUse channel; or (b) also append these WARN lines to a file under `<common>/forge-journal/warn.log` that check 48(c)
reads. Also name the channel in the spec. Spec side (the dispatcher's): item 2/3 names no output channel for the SubagentStop
path. Its "Output channel: additionalContext" line covers only the PostToolUse/PreToolUse hooks.

### F3 (MAJOR) — `journal_hooks.py` reads stdin with no deadline, unlike every other live hook
`tools/journal_hooks.py:419-427` calls `sys.stdin.buffer.read()` with no bound. Every other live hook in tools/ carries the
stdin deadline (`OSLLM_STDIN_TIMEOUT`, P4 class): claim_control_gate, dispatch_gate, dod_gate, dod_track, handoff_gate,
hygiene_gate, journal_echo, main_gate, negative_lint, owns_gate, search_control_gate, session_context, tier_echo
(grep `stdin_deadline|OSLLM_STDIN_TIMEOUT` over `tools/*.py`, non-test, 15 files). Once L places the settings, `pre-edit` runs
on EVERY Edit/Write and `post-agent` on every launch. A stdin with no EOF then stalls the tool until the host timeout (60 s
default; the settings set none). This is a second road for one action (P31; rule 18 consistency). Fix: the local deadline
copy (the negative_lint.py:533-603 form). On a timeout, post-agent prints the door line
(`JOURNAL: delegated NOT written -- stdin deadline exceeded; write it: …`) and pre-edit stays silent. Add one test row per
mode. This must land before L. It is inert until then, because the dod_gate path does not use `_read_payload`.

### F4 (minor) — a lost race prints a door for a line that already exists
`journal_hooks.py:290-314` with `:344-361`. The marker check, the `_locate` re-look and the idempotence read are all outside
the lock. Interleaving: record_returned creates the marker, post-agent writes `delegated` and sees the marker, and
record_returned's re-look finds the `delegated`. Both then write `returned`. Validator rule 9f (one `returned` per
(task, worker_ref), judged under the lock, `journal_validator.py:1178`) refuses the second. Nothing is doubled. But post-agent
then shows `JOURNAL: returned NOT written … write it: …` on additionalContext, which invites a pointless CLI call. Fix: when
the write is refused, re-read `_find_delegated(copy)`; if `done`, say nothing.

### F5 (minor) — `record_returned` swallows its own exceptions with no line
`journal_hooks.py:324-325` (`except Exception: return []`), and `:336-338` (`repo_root` refused → `[]`). For example,
`_forge_dir` raising LockError inside `_locate` (`:370`) loses `returned` silently, before any marker exists. This is not
dod_gate's business: its exit code is correctly untouched. But it is a silent drop against the module's own docstring
(":11 never left unrecorded SILENTLY"). Fix: return one line, `JOURNAL: returned NOT recorded for agent:<id> -- the hook
failed (<Type>)`. It goes to the same channel as F2, so fix F2 first.

### F6 (minor) — the dod_track writer exclusion misses three non-canonical command forms
Surface: `dod_track._PYTHON_PROGRAM_RE` (`tools/dod_track.py:229`), the command parser. I ran the neighbouring forms against
`is_verification_command`. Verbatim:
```
False | python -B tools/journal_write.py accept --run "python -m pytest tools/x.py -q"
True  | python -X utf8 tools/journal_write.py accept --run "python -m pytest tools/x.py -q"
True  | python -B "C:/my dir/tools/journal_write.py" accept --run "python -m pytest tools/x.py -q"
True  | py -3 tools/journal_write.py accept --run "python -m pytest tools/x.py -q"
```
- A flag that takes a value (`-X utf8`, `-W ignore`) is read as the program.
- A quoted path with a space is cut at the space.
- The `py` launcher is not matched.

In each case the inner `--run` pytest counts as a verification run, against the S-12 invariant. The canonical form
(`python -B tools/journal_write.py`) works, so this is minor. Fix: skip `-X/-W/-c?/-m?` together with their value, take a
quoted program whole, and allow `py(\s+-\d[\d.]*)?`. Add the three rows.

### F7 (minor) — duplication (rule 18)
- `journal_hooks.py:46` `AGENT_ID_RE` repeats `transcripts.py:44` byte for byte. The agent-id grammar has one owner. Fix:
  `AGENT_ID_RE = transcripts.AGENT_ID_RE` (or use `transcripts.agent_file_name`).
- `journal_hooks.py:88-97` `_objs(text)` is `journal_write.py:288-297` `_objs(lines)` with a split in front. Fix: call
  `jw._objs(text.splitlines())`.
- `_find_delegated` (`:123-133`) is a third copy of the "the `delegated` with this (task, worker_ref)" match, next to
  `journal_write._fill_returned` (`:423-438`) and the validator's open-pair state. It is acceptable as a reader. Note it; no fix
  is needed now.

## Answers

**Q1 (a hook never blocks by error).** Held for the exit code, with one formal exception. `main()` (`journal_hooks.py:430-447`)
wraps the payload read and both modes in `except Exception`, and returns 0. `post_agent` and `record_returned` each have their
own catch-all. `write_event` never raises (`journal_write.py:388-400`, read). The imported modules have no top-level
`sys.exit`: grep of journal_write/keys/lock, transcripts, dispatch_gate/manifest, journal_validator/echo, streams and
dev_config shows only `if __name__` exits. In dod_gate, `_record_returned` (`dod_gate.py:562-574`) is inside try/except. It is
called only when `exit_code == 0` (`:624-625`), after the gate's message. A blocked stop (exit 2) never reaches it, and its
failure cannot change the exit code or the message.
The exception: `import streams` (`journal_hooks.py:33`) and `streams.utf8_stdio()` (`:431`) sit outside the try. `utf8_stdio`
itself never raises (`streams.py:39-44`, read). A missing `streams.py` (a partial merge) would give a traceback and exit 1.
That does not block (only exit 2 blocks), but it breaks "exit 0 always". Low. Optional fix: move the import into `main`'s try.
pre-edit warn mode: one `additionalContext`, exit 0. The PreToolUse `additionalContext` channel is real: this session got
`PreToolUse:Bash hook additional context` lines. Refuse mode: the deny shape, exit 0. Also F3: a hang is not an exception, but
it does block the tool, until the timeout.

**Q2 (never unrecorded silently; `returned` never before `delegated`).**
- Ordering: HELD. `returned` is written only when `_find_delegated` has found the `delegated` in that copy (`:343-361`), or
  right after post-agent's own successful write (`:273`). A doubled `returned` from the race is refused by rule 9f (F4).
- "Never silently": NOT held on two roads:
  - F1: a stop cwd in a linked worktree with no dev.config gives no write, no marker and no WARN. Probe above.
  - F2/F5: the stop-side failures go to an unread channel, or produce no line at all.
- The post-agent side IS loud: every no-write road returns `_door(...)` on additionalContext (`:206-263`).
- Linked worktree as the DELEGATING session (E-B23-10): works through the index and through the scan when that worktree has
  a dev.config (rows exist). In this deployment no linked worktree has one. So post-agent from such a session gets a loud
  door ("no journal file"), never a silent loss.
- Two sessions on one machine: each write takes the machine lock inside `write_event`. The idempotence read (`:243-245`) is
  outside the lock. Two PostToolUse events for one agent id at the same instant with no task id would issue two ids. This is
  the builder's deviation 3, an estimate. I accept it as low, because the completion event comes minutes later.
- Measured by me for the order question: in the 11 session transcripts, the 76 Agent/Task launches WITHOUT
  `run_in_background` also returned `Async agent launched … agentId:` (fg/field/text 56, fg/nofield/text 18). No synchronous
  foreground result form occurs, so E-B23-8 is a tolerant branch, not the common one. All 1,295 launches that did go out
  carry `agentId: ` in the text; only the 192 PreToolUse-refused ones do not (scratchpad `fg.py`).

**Q3 (streams.py in MECHANISM_PREFIXES).** The list change is complete for the code readers:
- `mechanism_gate.mechanism_paths` (`mechanism_gate.py:386-388`);
- `test_mechanism_gate` closure (both worlds now, the builder's new `[live|proposed]` rows);
- `test_streams` S3 (exemption by `mechanism_paths`; streams.py is harmlessly exempt twice) and S4 (now `SANCTIONED_STREAMS_ROAD`
  = journal_write, journal_hooks, dod_gate);
- `test_worktree_sweep:1025-1030` (unaffected).

Every module journal_hooks imports lazily (dispatch_gate, dispatch_manifest, journal_validator, journal_echo, transcripts,
journal_keys, dev_config) was already in the list (`mechanism_gate.py:232-271`, read).

The rule TEXT is not complete. It is stale in two carriers:
- `tools/streams.py:14-17`: "a mechanism-chain link NEVER imports this module … S4 (no link reaches this file)";
- `docs/SIBLING_MAP.md:355`: "a link NEVER imports `streams`"; the call-site list also lacks journal_hooks. And `:357`:
  "S4 … the closure from EVERY link", which is now "every link except the sanctioned road".

The axis-15 closing rule (`SIBLING_MAP.md:359`) itself is consistent: "the Lead brings `streams.py` into `MECHANISM_PREFIXES`
with a mechanism commit". But that commit must carry the text change, and neither file is in the builder's owns. So this is a
NEEDS-WORK item for the Fable commit, not for a builder round. Rewrite the three passages to: "links never import streams
except the road named in `test_streams.SANCTIONED_STREAMS_ROAD`".

**Q4 (deferring the hook_liveness_probe cases to stream L).** Cases 17 (post-agent) and 19 (pre-edit): safe to defer. Their
hooks are not on any live path until L places the settings, so there is nothing live to probe.
Case 18 (passing stop writes `returned`): NOT a deferral to L in effect. `dod_gate.py` is ALREADY on the live SubagentStop
path, so `record_returned` goes live the moment B23 lands. From then until L:
- (i) `returned` lines start appearing in the live journal for every hand-written `delegated` whose worker_ref is
  `agent:<id>`. This is a behaviour change at landing that the spec does not state for the two worlds (rule 11 (i), the
  dispatcher's side).
- (ii) Every stop with no matching `delegated` (a dispatch the Lead journals after its stop, or with another worker_ref form)
  leaves a pending marker. No post-agent will consume it. It is pruned after 24 h with a WARN on the invisible channel (F2).
- (iii) A runtime import failure of journal_hooks or journal_write inside dod_gate is swallowed (`dod_gate.py:573-574`). With
  case 18 deferred, nothing live detects it. `test_dod_gate`'s B23 rows cover only the logic in CI.
- (iv) The Lead's own by-hand journal Edits can now hit the Edit tool's stale-read refusal after a hook append, and the
  pre-edit WARN that explains it is not live yet. This is friction, not loss.

Recommendation: land case 18 WITH B23 (the probe count goes 20 → 21), or state the two worlds in the spec and accept (i)-(iv)
explicitly. Which one is the Lead's decision.

## DUPLICATION AND CONSISTENCY (rule 18, brief item 6)
Findings F3 (a second stdin road), F7 (AGENT_ID_RE, `_objs`), F6 (one more command parser: the S-12 regex sits next to
`VERIFICATION_COMMAND_RE`; acceptable, but its holes are listed). What was grepped: `AGENT_ID_RE = ` over tools (2 hits),
`^def _objs`, `stdin_deadline|OSLLM_STDIN_TIMEOUT` (15 hooks), `agentId` readers (`hop_metrics` now imports
`transcripts.LAUNCH_RE`, so a single pattern is confirmed).

## CODE QUALITY (rule 18, brief item 7)
journal_hooks.py is readable and fail-soft, and every no-write road names its door. Points:
- `journal_echo._journal_rel` is used across modules as a private name. It is the one reader, by spec, so this is acceptable,
  but it should be made public at the next touch.
- Post-agent reads the whole journal twice per launch (`:243`, and `:280` with a designer skip), on top of the writer's own
  read. The live file is 2,137 lines and 0.93 MB (`wc -l`, `ls -la logs/journal/`), so this is fine now and worth a note.

## ONE ACTION, ONE ROAD (rule 19, brief item 12)
F3 is the instance: the stdin read of a hook. The pre-edit WARN road for by-hand journal edits is a named transitional
exception that closes at node B23-S (§2 row B23-S), with an owner and a trigger, so it does not block. There is no exclusion
of a language, project or case.

## SIBLING_MAP axes touched
- axis 13 (one cut): covered. The `section_cut` fallback for a scout/critic prompt is the same one cut (deviation 1). It is
  correct, and it is a spec gap on the dispatcher's side.
- axis 14 (one reader of a shared fact): covered for the launch id (`transcripts.launch_agent_id`, hop_metrics imports
  `LAUNCH_RE`). NOT covered for the agent-id grammar (F7).
- axis 15 (the stream/stdin helpers of chain links): partly covered. streams enters the chain correctly, but the rule text is
  stale (Q3), and the stdin deadline copy is missing (F3).
- axis 4 (settings → AGENTS.md): covered at L (the proposed file differs from the live one by exactly the two entries;
  verified by a sorted-JSON diff).
- axis 22 (host forms read at one place): covered. Step 0 (c)/(f) was re-measured by me from transcripts (above).
- axis 34 (one road): covered by the B23-S transitional; F3 as above.
- All other axes: n/a for this diff. I agree with the builder's §7 lines, except axis 15 ("covered"), which I narrow as above.

## Trail
Read:
- the spec r2 §3 B23 (446-543) and §6.4 check 48 (786-793);
- the builder report t-869-B23.md;
- the t-865 seam notes (F3, the notes cap);
- `tools/journal_hooks.py` (whole);
- the staged diffs of dod_gate, dod_track, mechanism_gate, transcripts, dispatch_gate, hop_metrics and hook_liveness_probe;
- `dod_gate.py:530-640`;
- `journal_write.py:150-210, 386-510`;
- `journal_keys.py:778-833`, `journal_lock.lock_dir`;
- `streams.utf8_stdio`;
- `SIBLING_MAP.md:334-359`;
- the settings.json vs .proposed sorted diff.

Re-runs and probes:
- `pytest tools/test_journal_hooks.py tools/test_dod_track.py -q` → 156 passed (a control subset of the attached 1569);
- probe F1 (above);
- the dod_track forms (F6);
- the transcript launch-form survey (Q2);
- the dev.config presence check over the worktrees.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "F1 journal_hooks.py:339 -- the guard on the STOP root's journal returns [] before the index/scan: a stop whose cwd is a linked worktree without tools/dev.config.yaml (every linked worktree here) loses returned with no marker and no WARN; probe: index exists, record_returned -> [], events stay [journal_created, delegated]"
  ],
  "class_completeness": "Axis 15: streams.py brought into the chain correctly in code (mechanism_paths, closure test both worlds, test_streams S3/S4), but the rule text is stale in tools/streams.py:14-17 and SIBLING_MAP.md:355,357 (Fable commit), and journal_hooks lacks the stdin deadline every other live hook carries (F3). Axis 14: launch id one reader yes; agent-id grammar duplicated (F7). Axis 13 covered via the section_cut fallback.",
  "fixes": [
    "F1: drop or move the journal_hooks.py:339 guard after _locate (judge over jw.worktrees_of); add a row: stop from a linked worktree without dev.config writes returned into the root copy via the index and via the scan",
    "F2: stop-side WARN/NOT-written lines go to stderr on exit 0 (unread): leave the pending marker on a refused returned, or log WARNs under <common>/forge-journal for check 48(c); name the channel in the spec",
    "F3: add the local stdin-deadline copy (negative_lint.py:533-603 form) to journal_hooks._read_payload; timeout -> post-agent door line, pre-edit silent; one row per mode; before L",
    "F4: on a refused returned re-check _find_delegated and stay silent when already done",
    "F5: record_returned exception path returns one NOT recorded line instead of []",
    "F6: dod_track._PYTHON_PROGRAM_RE: skip -X/-W with their value, take a quoted program whole, allow the py launcher; three rows",
    "F7: AGENT_ID_RE = transcripts.AGENT_ID_RE; _objs via journal_write._objs",
    "Q3 (Fable commit): rewrite streams.py:14-17 and SIBLING_MAP.md:355,357 to name the sanctioned road (test_streams.SANCTIONED_STREAMS_ROAD) and list journal_hooks as a streams caller",
    "Q4: land hook_liveness_probe case 18 with B23 (dod_gate path is live at landing) or state the two worlds in the spec"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/20261114-coordinator-offload-spec-r2.md:446-543,786-793",
      "docs/tasks/handoffs/t-869-B23.md",
      "docs/tasks/specs/reviews/20261114-offload-topic-b-critic.md:36-60",
      ".claude/worktrees/offload-b23/tools/journal_hooks.py",
      ".claude/worktrees/offload-b23/tools/dod_gate.py:530-640",
      ".claude/worktrees/offload-b23/tools/journal_write.py:150-210,386-510",
      ".claude/worktrees/offload-b23/tools/journal_keys.py:778-833",
      "staged diffs: dod_gate, dod_track, mechanism_gate, transcripts, dispatch_gate, hop_metrics, hook_liveness_probe",
      "docs/SIBLING_MAP.md:334-359",
      ".claude/settings.json vs .claude/settings.json.proposed (sorted JSON diff)"
    ],
    "reruns": [
      {"command": "python -m pytest tools/test_journal_hooks.py tools/test_dod_track.py -q (in the worktree)", "result": "156 passed in 29.53s"},
      {"command": "python -B scratchpad/probe_f1b.py (temp repo, linked worktree without dev.config, stop cwd = worktree)", "result": "index exists: True; record_returned -> []; events [journal_created, delegated]; from main cwd -> returned written"},
      {"command": "dod_track.is_verification_command on 4 writer forms", "result": "canonical False; -X utf8, quoted path with space, py -3 -> True"},
      {"command": "python -B scratchpad/fg.py (Agent launch result forms over 11 transcripts)", "result": "all launched results carry agentId text; non-background launches also async (74); 192 refused have none"},
      {"command": "test -f tools/dev.config.yaml over .claude/worktrees/*", "result": "NO for every linked worktree listed; root has it"}
    ]
  }
}
```

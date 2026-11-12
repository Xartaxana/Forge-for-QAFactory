# t-116 code review — spec fg-context-and-hygiene B1 + B2 (critic, opus)

Under review: the uncommitted diff of worktree `C:\QAFactory\forge-repo\.claude\worktrees\agent-ac59fdf8d182e6ef9`
(`.claude/agents/builder.md`, `critic.md`, `designer.md`, `tools/test_handoff_rule_anchors.py`, `tools/dod_gate.py`,
`tools/test_dod_gate.py`). What the work had to meet: spec §3 B whole + the Lead acceptance sections (F-B1..F-B4).
Line numbers below refer to the worktree files.

**Verdict: NEEDS WORK — 2 blocking (B-1, B-2), 9 non-blocking (F-1..F-9).** Accepting the diff is the Lead's call (rule 6).

## Control runs (verbatim)

1. The witness re-run, same command as the builder's:
   `python -m pytest <wt>/tools/test_handoff_rule_anchors.py <wt>/tools/test_dod_gate.py <wt>/tools/test_handoff_gate.py -q -p no:cacheprovider`
   ```
   ........................................................................ [ 45%]
   ........................................................................ [ 91%]
   ..............                                                           [100%]
   158 passed in 6.88s
   ```
   Same as the builder's witness (158 passed).
2. The clone ratchet: `python -B <wt>/tools/dup_ratchet.py --check --repo <wt>`
   ```
   dup ratchet: scripts 278 files in 26.3s, tools 72 files in 3.5s
   dup ratchet: scripts: 9 groups, 9 known, 0 new, 0 grown, 0 carried, 0 shrunk/gone (0 diverged)
   dup ratchet: tools: 16 groups, 16 known, 0 new, 0 grown, 0 carried, 0 shrunk/gone (0 diverged)
   exit=0
   ```
3. A replay against real data (rule 13): the new `named_handoffs` + `handoff_written` run over all 38 subagents of session
   f92520fc (their real dispatches from `~/.claude/projects/C--QAFactory-forge-repo/<session>/subagents/`, their real
   tracks; a worktree agent's track is the one in its worktree). What came out:
   - import of the readers 0.052 s; each check took 0.000-0.053 s.
   - every critic and designer that wrote its report -> `written True` (8 of them: t-094, t-096, t-098, t-105, t-109 and three designers).
   - `written False` only for agents still running at replay time (a08344 t-114, af100c t-113, aa8a70 = this review, a98c3c designer):
     their files do not exist yet (`ls`: "No such file or directory").
   - **every builder: `cand []`**. Builder dispatches today carry a prose `handoff:` line ("the report at the owns path: ..."):
     `handoff_paths` -> `[]` for ac59fdf8d182e6ef9, a0534aa1e15afd92c and afe747bf910867c04 (cut not degraded). So the check
     never fires for builders today.
4. Path-match probe (`handoff_written`, candidate `C:/My Repo/docs/tasks/specs/reviews/r 1.md`): lower-case + forward slashes
   -> True; backslashes -> True; worktree copy `...\.claude\worktrees\agent-x\docs\...\r 1.md` -> True; `r 2.md` -> False.
   A backticked path with spaces on `handoff:` is read by `handoff_paths` and `_in_folder` -> True.
5. The worktree probe (for B-1):
   ```
   dod_track.build_fact({'tool_name':'Write','agent_id':'w1','cwd':'C:/QAFactory/forge-repo/.claude/worktrees/agent-x',
                         'tool_input':{'file_path':'C:/QAFactory/forge-repo/docs/tasks/handoffs/r.md'}})
   fact: None
   dod_gate.decide({'edits':[],'runs':[]},'w1',[(that path,'docs/tasks/handoffs')], worktree) -> 2
   ```

## Blocking

**B-1. A worktree worker that writes the dispatch's literal main-clone path is blocked as "you did not write it".**
`tools/dod_gate.py:358-366` (`_handoff_block`) checks only the track. But `tools/dod_track.py:191-214`
(`_is_scratchpad_path`, applied at `:340`) drops from the track every edit outside the payload `cwd`. For a
worktree agent, `cwd` is the worktree. Evidence: the ac59 builder's edits and the gate_state of 22 other worktree agents
live in `<worktree>/.claude/dod_track/<session>.json`, not in the main track. So a worker that follows builder rule 7
word for word ("write ... to that one path") and writes `C:\QAFactory\forge-repo\docs\tasks\handoffs\r.md` from a
worktree leaves no edit record. The SubagentStop then exits 2 with HANDOFF MISSING (control run 5).

Why it blocks. It is a false block on a worker that did its job, the direction the spec rules out ("may err toward
PASS"). It also writes a false `handoff_missing` entry into the very detector check 28 (b) will count. Today it is
dormant: builder handoffs are prose (control run 3). But B1 itself teaches builders the form `report: <path>` and
"when the dispatch names an absolute path on its `handoff:` line". The first Lead dispatch that follows that form for a
worktree builder triggers it. The spec's edge list covered only the reverse case (a worktree copy of the path), so this
is partly a spec gap. The fix still belongs to this round.

Fix, in the pass direction and inside `owns`: before returning the path in `_handoff_block`, pass when the candidate
file exists on disk and its mtime is not earlier than the worker's dispatch. Take the dispatch time from the timestamp
of the first record of the worker transcript, which `named_handoffs` already resolves. Return it with the candidate,
e.g. `(path, folder, dispatch_ts)`. A file older than the dispatch, or a missing one, still blocks once. Add one test
row: "written to the main-clone path from a worktree cwd (no track edit, file mtime after dispatch) -> pass". The
alternative of recording out-of-cwd handoff writes in `dod_track` changes the doc-only and green invariants of a file
the node does not own, so it goes to the queue, not this round.

**B-2. At N = 0 the line cap contradicts the form in all three rules, and the text departs from the spec's edge.**
`builder.md:73-74`, `critic.md:120-121`, `designer.md:58` say "(N = the numbered spec items; 0 items: 3 lines; ...)".
Each then lists FOUR lines as the form: `report:`, "one status line", `questions:`, `needed beyond the manifest:`. The
spec edge (§3 B1) says "0 numbered items -> cap 3 lines **+ the path**", which is 4 lines. The builder dropped
"+ the path".

For a critic, N = 0 is the normal case: a critic dispatch carries lettered questions, not numbered spec items. This
dispatch is an example. Critic 16 makes the status line (verdict + number of blockers) mandatory. So a weaker model
cannot obey both clauses: it will break the cap or drop the verdict line.

Fix: in all three, "0 items: 3 lines plus the `report:` line" (the spec's wording). Optionally say what N is for a
critic, see F-3. The anchor test needs no change, since K2 is the character key.

## Non-blocking (fix before merge unless marked queue)

- **F-1 (B1 edges missing from the text).** Two spec edges are not in any of the three rules: "a dispatch whose spec is a
  pointer (R11-m) -> N is counted in the persisted spec it points to", and "the N statuses may share one line, so the
  character cap usually decides". A weaker model computing N for a pointer dispatch has nothing to go on. Fix: one
  clause in each rule, e.g. "(a pointer dispatch: N from the spec it points to)".
- **F-2 (vocabulary vs builder-rules 11).** `plans/builder-rules.md:77` keeps DONE/PARTIAL/NOT DONE per item for the
  report file. The new builder 7 status line has `done | not done -- <clause> | question`, with no `partial`. This is
  not a contradiction (file vs message), but a partial item has to be squeezed into "not done". Fix: allow
  `partial -- <clause>` in the status-line example, or leave as is with a Lead note.
- **F-3 (what N is for critic/designer).** "N = the numbered spec items" fits a builder. For a critic it is the items of
  the reviewed spec? the dispatch's questions? For a designer, the items of the brief or of its own draft? The rule text
  does not say, and the same text drives the line cap. The fork is the Lead's (F-B2 extended the form to these roles).
  Recommendation: for critic and designer, N = the numbered or lettered questions of the dispatch.
- **F-4 (the safety-valve interaction has no test).** The builder's decision (1) is correct (answer c), but no row pins
  it. The spec edge "the existing safety valve (2 blocks) counts this block too" is a behaviour with a branch
  (`dod_gate.py:362`). Add one row: a builder with no green run and its handoff unwritten. Expected stops:
  [2 handoff, 2 no-green, 0 valve], with `gate_log` actions `handoff_missing, blocked, skipped_after_2_blocks`.
- **F-5 (anchor test: scout must not carry the new cap).** `test_handoff_rule_anchors.py:129` and `:159` still check only
  that `"25 lines"` is absent from scout.md. F-B2 keeps scout unchanged, so the pin should also assert K2 is absent.
  `RESTATED` (`:29`) keeps the old Russian key `"не длиннее 25 строк"`. A Russian restatement of the NEW cap in the brief
  or in builder-rules 11 would not be caught. Fix: add `"2 000 символов"` / `"2000 символов"`, or queue it with F-B4's
  registry.
- **F-6 (duplication, brief item 6).** `dod_gate._segments` (`:275-276`) repeats the split+normcase of
  `handoff_gate._in_folder` (`handoff_gate.py:94`, `SEGMENT_SPLIT_RE`). The realpath+normcase in `_written_paths`
  (`:286`) and in `handoff_written` (`:298`) repeats `handoff_gate._real` (`:100-101`). The spec said "one reader, no
  copy". They are small (2 lines each), and the clone ratchet is green (control run 2). Fix: pass the imported
  `handoff_gate` down, or import `_real`/`SEGMENT_SPLIT_RE` lazily in `handoff_written`. Severity: fix before merge,
  cheap.
- **F-7 (SIBLING_MAP rows not updated; class completeness).** Row `docs/SIBLING_MAP.md:316` lists `HANDOFF_DIRS`
  readers as `handoff_gate` and `agent_budget.ALLOWED_DIRS`. `dod_gate.named_handoffs` is now a third consumer.
  Row `:333` ("Consumers and their error direction") does not list dod_gate's fail-OPEN direction, the opposite of
  handoff_gate's fail-closed. Not in the builder's owns: a Lead line of the same merge (node P or the merge commit),
  `<what> | узел: P`.
- **F-8 (concurrency, pre-existing race, queue).** `dod_gate.main` loads, decides and saves with no lock
  (`dod_track.py:61` documents the race). A `dod_track` PostToolUse save of a parallel worker in the same cwd can land
  between this stop's load and save, or after it from a stale load. The once-key is then lost and a second
  HANDOFF MISSING follows. Rare: it needs two critics in main cwd and a stop within ms of a sibling's Write. This is the
  same class as the lost `consecutive_blocks`. Queue: `перенос: forge findings | обоснование: pre-existing race of the
  track file, not introduced here | подтвердил: —`.
- **F-9 (unverified live premise).** `named_handoffs` reads `payload["transcript_path"]` as the MAIN session transcript
  and derives `subagents/agent-<id>.jsonl` from it. That is what PreToolUse gives `handoff_gate`. For SubagentStop the
  host also sends `agent_transcript_path`. If `transcript_path` ever pointed to the agent file, the check would pass
  silently forever (stderr "dispatch unreadable"). My replay used the main path, so it proves the reader, not the
  payload. Fix: prefer `agent_transcript_path` when present, otherwise the current derivation. Put a live-proof line in
  the batch's evidence ("one critic that skips its Write gets exactly one HANDOFF MISSING").

## Answers a-f

**a. B1.** Same form in all three: `report:`, a status line, `questions:`, `needed beyond the manifest:`. Same caps:
2,000 characters and 3 + N lines, "the stricter cap decides". Rule numbers kept: builder 7, critic 16, designer 5
(`test_role_rule_carries_file_rule` green). The anchors are all present in all three: "never lost, never shortened",
"names no such path", "the Write is refused", `ceil(len/200)`, "the file at `handoff:`". "the closing lines of the
witness" left builder 7 in both places. Contradictions:
- B-2 (N = 0, against the four-line form and the spec edge);
- F-1 (pointer N);
- F-3 (N for critic/designer).

No contradiction with critic 17 ("the chat digest carries no block" is kept). `critic-diff-brief.md` and
builder-rules 11 still only point: grep "25 lines|final message|closing lines|digest" -> no hit in either, with the
positive control on builder.md hitting; `test_brief_what_comes_back` and `test_builder_rules_p11` are green.
Builder-rules 11 vocabulary: F-2. Executable for a weaker model: yes once B-2 and F-1 are fixed.

**b. Error direction.**
- Double block for this reason: only via the race of F-8 (pre-existing class, queue). Otherwise the once-key persists,
  including on a track that did not exist (row `no-edit-critic-no-track-file`, which runs the real hook).
- A worker that did write gets blocked in one case: a worktree worker writing the main-clone path, B-1.
- Case, slash direction, worktree copy and a path with spaces all match (control run 4).
- Unreadable dispatch, broken import, degraded cut, two or more candidates, no `agent_id`, no `transcript_path`: all
  pass (the try at `:333-355` wraps everything up to the candidate list).
- Exception roads: `decide`/`handoff_written` sit outside that try, and `main` has no try. A corrupt track (a non-dict
  edit entry) raises AttributeError there, so Python exits 1, which the host treats as non-blocking. That is a pass,
  the same as the pre-existing `evaluate()` behaviour on such a track. `realpath` with a NUL character does not raise
  (probed). No road to exit 2 from an exception.

**c. The builder's two decisions.**
- (1) Counting the block in `consecutive_blocks`, and skipping the check when it is already at 2, is right. The spec
  says the valve counts this block. Firing at 2 would be a third block, past the valve. Skipping errs toward pass.
  Consequence to note (spec-consistent, not a defect): a builder that gets one handoff block and then one no-green
  block now passes the valve WITHOUT a green run, after one fewer no-green block than before. That is a one-attempt
  weakening of the green invariant for builders with an absolute handoff path, and it shows up as `unsafe_completions`
  at the next SessionStart. Untested: F-4.
- (2) No `transcript_path` -> silent no-check: right. Nothing was named, so nothing failed, which matches "a stderr line
  where something failed". It also keeps the old empty-stderr pins green. Premise caveat: F-9.

**d. The save condition** (`main`, `dod_gate.py:569-572`). `once_fired` is True only when the key is set: on the block
itself, or on any later stop of that agent, when the file then exists anyway. With no track, no edits and no block, the
key is absent, so nothing is written. This is pinned by `test_no_handoff_no_track_file_still_writes_nothing` and by the
old no-edit tests, still green. `decide` does create an empty `per_agent[<key>]` dict in memory on every stop, but the
save gate ignores it. Kept.

**e. Siblings still saying "25 lines"** (my grep `25 lines|25-line` over the protocol, tools and docs; positive control:
hits in the anchor test):
- `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:828` **and `:860`** ("hand-back messages over 25 lines"; the builder reported
  only 828): SAME merge, node P (spec §8, "B1 and B2 land in ONE merge with check 28's edit").
- `tools/handback_extract.py:31,158` are docstrings naming how lines are counted, and the counting (ceil(len/200))
  stays valid. Only the label is stale: queue, or a one-word edit in the same merge by whoever owns the file. The
  substantive sibling is the reader itself: it prints `bytes=`, while the cap is in CHARACTERS (Cyrillic counts 2 bytes
  per character). Check 28 (b) "messages over the cap counted by `handback_extract`" would over-count non-ASCII
  hand-backs. That belongs to node P / B0's outcome: `<characters, not bytes, in the over-cap count> | узел: P`.
- `tools/hop_metrics.py:209` is a docstring only: queue.
- `tools/session_context.py:58,99,1700` (its own MAX_LINES budget): unrelated, n/a.

Duplication: F-6. Code quality (item 7): the new functions are each under 40 lines with at most 3 nesting levels:
`named_handoffs` `:322-355`, `handoff_written` `:291-305`, `_handoff_block` `:358-366`. No dead branches. Two redundant
checks: `len(handoffs) != 1` in `_handoff_block` (`named_handoffs` already returns 0 or 1 entries) and the
`isinstance(tp, str)` duplication. Harmless, no finding. Names do not lie. The docstring of `decide` matches the code.

**f. Live path.**
- Import cost: 0.052 s for the readers (including `dispatch_manifest`'s lazy imports). Each check takes milliseconds,
  and runs only for stops with an `agent_id` and a `transcript_path`. The main session's Stop is untouched.
- Agents launched before the merge: their tracks lack nothing (`dod_track` has recorded `file_path` per `agent_id`
  since before B2, which the replay confirms). An old critic that wrote its report passes. An old critic that did not
  write gets the single block, which is the intended behaviour.
- The hook command is `python tools/dod_gate.py`, relative. So a worktree agent probably runs its own tree's copy, and
  agents in worktrees cut before the merge would not get the check at all. Estimate, not verified: which copy runs
  depends on the host's process cwd for subagent hooks. Harmless either way.
- E1 changing `dispatch_manifest`'s shape: an AttributeError or TypeError is caught, giving pass + stderr. New header
  keys that the cut does not recognise could fold extra paths into the `handoff` section, giving two candidates and so a
  pass. Every road errs toward pass. The node is still a reader of `section_cut`/`handoff_paths`/`HANDOFF_DIRS` and
  must be named in E1's consumer list (F-7).

## Standing questions

- **DUPLICATION AND CONSISTENCY:** F-6 (two small copies of handoff_gate's `_real` and segment split). Clone ratchet
  green.
- **CODE QUALITY:** none found beyond F-6. Function sizes and nesting were checked on the new code (ranges above).
- **ONE ROAD (item 12):**
  - none found in the code: grepped the diff for language, project or role names. `named_handoffs` deliberately checks
    every `HANDOFF_DIRS` folder whatever the agent's kind, the same for every role.
  - The scout exclusion of the form (F-B2 "scout unchanged") is the Lead's decision quoted in the acceptance section.
    It is not a shared-mechanism exclusion: scout has no Write (`scout.md:5 tools: Read, Glob, Grep`).
- **ARCHITECTURE:** AR-13 is kept (the dispatch is read through `transcripts`/`dispatch_manifest`/`handoff_gate`, with
  no second parser). AR-22: the new `handoff_missing` producer has its reader in check 28, node P, same merge. AR-25:
  the block names its door, "put the full report in your final message". AR-28: unknowns pass, by the spec's chosen
  direction (an advisory-class block, not a gate on an unknown).
- **JUDGMENT:** none. It is a data check (file written yes or no), with no role content judged.

## Trail

Read:
- the full diff;
- the spec, lines 8-37 and 152-197;
- the builder report `docs/tasks/specs/reports/t-116-b1-b2-handback.md`;
- `tools/handoff_gate.py:1-185`;
- `tools/dod_track.py:185-561`;
- `tools/dod_gate.py`: `main` and `decide` `:398-437`;
- `tools/dispatch_manifest.py:138-143`;
- `tools/test_handoff_rule_anchors.py:24-165`;
- `plans/builder-rules.md:77`;
- `docs/tasks/critic-diff-brief.md:27-90`;
- `docs/SIBLING_MAP.md` (rows 316-352 by grep);
- `.claude/settings.json` hooks;
- `tools/critic_verdict.schema.json`;
- the real tracks of session f92520fc (main and 24 worktrees) and the 38 subagent transcripts (replay).

Needed beyond the manifest: the transcripts directory and the dod_track files (for the empirical replay), and
`docs/SIBLING_MAP.md`.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B-1 tools/dod_gate.py:358-366 with tools/dod_track.py:191-214,340 -- a worktree worker that writes the dispatch's literal main-clone handoff path leaves no track edit (out-of-cwd edits are dropped) and is blocked as HANDOFF MISSING; probe: build_fact -> None, decide -> 2",
    "B-2 builder.md:73-74, critic.md:120-121, designer.md:58 -- '0 items: 3 lines' contradicts the four-line form each rule lists and drops the spec edge's '+ the path'; N = 0 is the normal critic case"
  ],
  "fixes": [
    "B-1: in _handoff_block pass when the candidate file exists with mtime not earlier than the worker transcript's first-record timestamp; add the test row 'main-clone path written from a worktree cwd -> pass'",
    "B-2: write '0 items: 3 lines plus the report: line' in all three rules",
    "F-1: add the pointer-dispatch N clause (R11-m) to the three rules",
    "F-4: add the safety-valve row (stops 2/2/0, gate_log handoff_missing, blocked, skipped_after_2_blocks)",
    "F-5: scout pins also assert K2 absent; a Russian key for the new cap in RESTATED or queue it",
    "F-6: reuse handoff_gate._real and SEGMENT_SPLIT_RE instead of the two local copies",
    "F-9: prefer payload agent_transcript_path when present; a live-proof line in the batch evidence",
    "Lead/node P: SIBLING_MAP rows 316 and 333 name dod_gate; protocol :828 and :860; handback_extract counts characters not bytes for the cap"
  ],
  "class_completeness": "Path-match surface walked: case, slash direction, spaces, worktree copy (all match), plus the reverse worktree case (main-clone path written from a worktree cwd: B-1). Error-direction surface walked: unreadable, import failure, degraded cut, 2+ candidates, no agent_id, no transcript_path, corrupt track (exit 1 = pass), race (F-8 queue). 25-line siblings: protocol :828/:860 node P same merge; handback_extract :31/:158 and hop_metrics :209 docstrings queue; handback_extract bytes vs characters to node P. SIBLING_MAP rows 316/333 need dod_gate named (F-7, Lead line).",
  "trail": {
    "read": [
      "git diff HEAD of worktree agent-ac59fdf8d182e6ef9",
      "docs/tasks/specs/fg-context-and-hygiene.md:8-37,152-197",
      "docs/tasks/specs/reports/t-116-b1-b2-handback.md",
      "tools/handoff_gate.py:1-185",
      "tools/dod_track.py:185-561",
      "tools/dod_gate.py:270-440,520-590",
      "tools/dispatch_manifest.py:138-143",
      "tools/test_handoff_rule_anchors.py:24-165",
      "plans/builder-rules.md:77",
      "docs/tasks/critic-diff-brief.md:27-90",
      "docs/SIBLING_MAP.md rows 316-352",
      ".claude/settings.json hooks",
      "real dod_track files of session f92520fc and its 38 subagent transcripts"
    ],
    "reruns": [
      {
        "command": "python -m pytest tools/test_handoff_rule_anchors.py tools/test_dod_gate.py tools/test_handoff_gate.py -q (worktree)",
        "result": "158 passed in 6.88s"
      },
      {
        "command": "python -B tools/dup_ratchet.py --check --repo <worktree>",
        "result": "0 new, 0 grown in both scopes, exit=0"
      },
      {
        "command": "replay named_handoffs + handoff_written over 38 real subagents of session f92520fc",
        "result": "every finished critic/designer written True; False only for still-running agents; every builder cand [] (prose handoff lines); import 0.052s"
      },
      {
        "command": "dod_track.build_fact(Write of main-clone handoff path, cwd = worktree); dod_gate.decide(empty track)",
        "result": "fact None; decide exit 2 HANDOFF MISSING"
      }
    ]
  }
}
```

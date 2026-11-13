# Critic: P1-v N4b code review (bookkeeping and refused calls per role session)

Diff: worktree `C:\QAFactory\forge-repo\.claude\worktrees\p1v-n4b`, branch `wip/p1v-n4b`, `71d7ca8..d8b86a6` (commits 26d987f + d8b86a6),
one pass for the node. Spec: `docs/tasks/specs/20261113-p1v-run-scoreboard-spec.md` rows T9/T10 (`:243-244`), §2.1 (`:276-292`),
§7.14 (`:430-432`), node N4b (`:449`), forks F15/F16 (`:560-561`); the Lead's six answers as given in the dispatch; the builder's two reports.

**Verdict: fit_with_fixes (NEEDS WORK).** 3 blocking findings (B1-B3), 5 non-blocking (N1-N5). Accepting the work is the Lead's decision. B2 also
needs one Lead decision before the fix round: answer 4's row 2 premise does not hold on the real data.

## Control runs (verbatim)

Mechanical layer, re-run from the package dir in a subshell:

```
( cd .../p1v-n4b/ai-packages/qa-factory && python -B scripts/tests/test_friction.py | tail -3; python -B scripts/tests/test_judgment_census.py | tail -1; python -B scripts/selftest.py --lang | tail -1 )
PASS and prints no 0.0%

=== test_friction: 196/196 ok ===
=== judgment_census: 24/24 ok ===
=== qa-factory selftest: 2/2 ok ===
```

Empirics first (numeric diff). `friction.call_spans` from the worktree on the three automator transcripts
(`~/.claude/projects/C--QAFactory-mybooks-stand-arm-factory-test-automation-framework/{db9a9038,8325ed4c,5a86e7e9}-*.jsonl`), read-only probe
(Bash heredoc, nothing written):

```
{'bookkeeping': [42, 164.4, 375.7], 'fragment_writes': [2, 4.4, 19.8], 'refused': [13, 32.4, 128.9], 'named_by_marker': [9, 25.9, 59.0], 'refused_total': [22, 58.3, 187.9]}
```

That reproduces the builder's row (e), with last-digit rounding differences (164.3/164.4, 128.8/128.9, 58.4/58.3). Invocations per script over the
same three sessions (distinct per command): `run_suite.py 33, manifest_put.py 17, manifest_from_tests.py 12, s5_precheck.py 9, handoff_check.py 6,
manifest_view.py 4, mk2.py 2, traceability.py 2, stand_health.py 1, mk3.py 1, mk4.py 1, execution_fingerprint.py 1`. Attributed calls
17+11+5+5+4 = 42, and listed invocations minus attributed calls = 6. That confirms the builder's "six commands invoke two signed scripts".
`plan_row.py` and the other unsigned scripts are invoked 0 times, which confirms the builder's negative claim.

Hand count on the fixture `timed_transcript()` (test_friction.py): bookkeeping k1, k3, k9, k10, k11 = 5 calls. Execution k1 4->7 = 3 s and
k3 14->16 = 2 s, so 5.0 s with 3 unmeasured. Turn k1 0->7 = 7 s; message t3 has its window 12->20 split over 2 calls = 4 s; total 11.0 s with
3 unmeasured. Refused: k2 3 s, k4 5 s, k5 3 s = 11 s execution; turn 5 + 4 + 5 = 14 s. Every figure matches the test row.

## Blocking findings

**B1. Surface: the shell-command reader `friction._segments` / `invoked_scripts` (`scripts/friction.py:282-350`). It is a new private
tokenizer on SIBLING_MAP axis 11, and it misreads heredoc bodies.** Axis 11 (`docs/SIBLING_MAP.md:283-285`) says a new reader of a command's words
takes its segments from `hooklib.walk` / `hooklib.command_segments`, not from a private tokenizer. Heredoc and here-string bodies already have the
ONE scan, `hooklib.scan_bodies` + `hooklib.cut_bodies` (`hooklib.py:1874-1970`, OH3-22, AR-15). The private tokenizer does not know about bodies.
Two failures follow, both measured:
- A body line is read as a command: `cat > notes.md <<'E'\nrun manifest_put.py later\npython s5_precheck.py was refused\nE` gives
  `['s5_precheck.py']`. That is a mention counted as an invocation, the class answer 2 closed.
- A quote inside a body flips the quote state for everything after it. `cat > n.md <<'E'\nthe guard didn't run\nE\npython scripts/manifest_put.py --fragment f.json`
  gives `[]`, so a real bookkeeping call is lost and nothing marks it unmeasured.
On real data (all 82 stand transcripts, 170 Bash commands that python-invoke a listed script), **4 commands lose a real invocation that follows a
heredoc**. Examples: `b74ea62c` ends `python .../handoff_check.py --file ... --fix`; `c830c46c` ends `python ".../manifest_put.py" --task LOCAL-1 --fragment ...`.
All 4 are code-critic sessions, so row (e) of the three automator sessions is unaffected. The counter still prints `measured` for an undercount.
Control: `hooklib.cut_bodies(c, hooklib.scan_bodies(c))` followed by `hooklib.command_segments(text, "bash")` reads the same failing command as
`[['cat','>','n.md','<<E'], ['python','scripts/manifest_put.py','--fragment','f.json']]`, which is correct.
Neighbouring classes of the same surface, each probed:
- Wrappers `timeout 120 python x.py`, `env X=1 python x.py`, `sudo python x.py`: all give `[]`. `references/launch-causes.json` `wrappers` /
  `launchers` (read by `hooklib._launcher_subs`, `:2078`) is the existing data for this.
- Nesting: `bash -c 'python x.py'` gives `[]`. `walk(payloads=...)` already reads payload hops.
- A program held in a variable: `$PY x.py` gives `[]`. Axis 11 names this indirection class.
- Encoding/case: `MANIFEST_PUT.py` is lower-cased and counted; `2>&1 | tail` is fine; `-X utf8` and `-Bu` are fine.
- Empty input gives `[]`, which is fine.
**Fix:** build `invoked_scripts` on `hooklib.scan_bodies`/`cut_bodies` + `hooklib.command_segments` (cleaned words through `hooklib.cleaned_word`).
Keep only the program-position rule (interpreter -> first non-flag word; `-c`/`-m` run no file) in friction. Take wrappers from the launch-causes
data, or name the wrapper/variable/`-c` payload classes as `unknown` in `CALL_TIME_METHOD`. Add `INVOCATION_SHAPES` rows: a heredoc body naming a
script (not counted), an apostrophe in a body followed by a real invocation (counted), and a wrapper.

**B2. Surface: refused row 2 `named_by_marker` and `refused_total` (`friction.py:437-440, 451-465, 469-479`). On the real data, row 2 is 9 of
9 non-refusals. The report's reconciliation reads them as missed refusals, and the total prints them as refusals with `state: measured`
(FR-41, AR-28).** Every row-2 call in the three sessions, with its result head:
- 7 x `usage`: all are voluntary `--help` calls (`manifest_from_tests.py --help`, `run_suite.py --help`, `manifest_put.py --help` (x2),
  `manifest_from_tests.py --help` (x2), `execution_fingerprint.py --help`). The role asked for the usage text. Nothing refused it.
- 1 x `validator`: `tail -5 tests/api/cart/cart_add.spec.ts`. The result is the role's OWN test title, "invalid input **is refused** with one
  error class", matching `validator_head_phrases` "is refused".
- 1 x `validator`: `manifest_from_tests.py ... --dry-run | tail -15`. The result is dry-run JSON echoing the role's instance id "stock-0 add
  **is refused**".
So the report's statements "The host flag alone misses 9 of 22 (41 %)" (round-2 report `:98`) and "22 calls ... against the hand 20: two calls
MORE" (`:95`) are false. The measured refusals are the 13 host-flagged calls, 7 UNDER the hand 20, so the gap changes direction. The DoD for row (e)
("every difference explained") is therefore not met: the explanation offered is wrong. The spec ties the T10 norm to this reconciliation
(`:244`, `:356`), so the error would carry into a norm.
On FR-12 (question 6): the markers file is a closed data list of OUR refusal spellings (AR-1), which is legitimate when applied to a result the
host flagged. Applied to UNflagged results, it matched the role's own wording (a test title and an instance id). That is the FR-12 class in
practice, and the commit line `judgment: none -- ... no word list over a role's text` does not hold for row 2.
**Fix (the Lead decides the shape; answer 4 is the Lead's):**
- (a) `refused_total` must not present row 2 as refusals: either drop the total, or make it the flagged row plus row 2 labelled
  `candidates, not confirmed` with its own state (not `measured`).
- (b) Recommended narrowing of row 2, structural only: a call counts in row 2 only when the command invokes a factory script (`invoked_scripts`),
  and a `usage` result of a command that passed `-h`/`--help` to that script is not a refusal. This measures 0 of 9 on these sessions, which is
  the true figure.
- (c) The builder corrects the report's refused paragraph: 13 measured refusals vs the hand 20; row 2 is 9 non-refusals listed by call; the hand
  basis for the 7-call difference is unknown.

**B3. Surface: `story_calls` role rows (`friction.py:773-779`, `_empty_rows`). A role with no reachable session prints `refused: {calls: 0}`
and `calls: 0` with no state.** That violates the function's own docstring ("never 0 calls, never 0 seconds", `:735`) and spec §7.14 ("an
unmeasured call is never 0 seconds"). Probe: a task root whose journal names `qa-automator` (transcript present) and `qa-code-critic`
(transcript absent) gives:
`qa-code-critic reachable 0 calls 0 {'bookkeeping': (0,'unknown'), 'fragment_writes': (0,'unknown'), 'refused': (0, None), 'named_by_marker': (0,'unknown'), 'refused_total': (0,'unknown')}`.
`refused` is the only one of the five rows with no state. It is T10 row 1 itself. A reader that prints `refused.calls` shows 0 for a role nobody
measured.
**Fix:** `_empty_rows` gives `refused` `state="unknown", reason="unknown: no session could be read"`. `call_spans` gives `refused`
`state="measured"`, and `_fold` already flips the state. The role-level `calls` becomes None, or gains a state, when `reachable == 0`. Add one
row to `story_call_time_rows`.

## Non-blocking findings

**N1. AR-22, and a false architecture line.** Commit 26d987f says `AR-22 -- new keys have a reader (call_spans/story_calls, N4 reads them)`. In
the base, `run_counters.py:636-638` sets T9/T10 to `unknown` with "bookkeeping and refused-call time come from the roles' transcripts
(friction.call_spans, node N4b), not read here". No package code calls `story_calls`, `call_spans` or `seconds_text` (grep `story_calls|call_spans`
over the worktree `*.py`: only friction.py and tests; the same grep finds `story_friction` in run_counters.py:493, positive control). The spec
assigns no node to wire them (`story_calls` appears only in row T9, `:243`). **Fix:** the Lead opens a node, "run_counters T9/T10 read
`friction.story_calls` (n/a for SIMULATED as today)" (owns `run_counters.py`, `test_retro_numbers.py`; after N4b merges). The fix round puts one
line in the report correcting the AR-22 claim.

**N2. Fragment writes by Bash are not counted.** The row counts only Write/Edit (stated in `CALL_TIME_METHOD`, so it is labelled, not hidden). On
all stand transcripts, `*.values.yaml` is written 28 times by Write/Edit/MultiEdit and **11 times by a Bash redirect/heredoc**, so 28 % of
fragment writes fall outside the row. The automator's three sessions have 0. **Fix:** the Lead decides whether to count Bash redirect targets
(after B1 the shared walker exposes them; `guard_pre_tool.config_write_check` is the existing shell-write recognizer) or keep the scope as labelled.
Either way, the report says so.

**N3. Code quality.** `call_spans` (`friction.py:396-466`) is about 70 lines, over the roughly 60-line bar. Pull the per-call classification
(`script`/`fragment`/`kind`/`named`) out into a helper. `call_spans:446-452` and `_empty_rows:773-779` build the same five row shapes twice with
different states. One constructor taking a state removes the duplication and B3 with it. Severity: fix in the B-round, since it touches the same
lines.

**N4. Loader key naming.** The file key `bookkeeping_fragment_patterns` is loaded as `fragment_patterns` (`friction.py:98`), while
`bookkeeping_scripts` keeps its name. Harmless, but the two keys read differently. Suggestion: keep the file name as the loader key.

**N5. Sibling, pre-existing (question 4).** `friction()` `open_repairs` (`friction.py:228`, `SCRIPT.findall(arg.lower())`) takes a name anywhere
in the text: mention as invocation, plus the heredoc-body class of B1. `classify` also tags voluntary `--help` as `usage` friction and the role's
own test text as `validator` (the B2 evidence applies to `friction()` tallies too: `usage 7, validator 2` on these sessions). Changing these alters
old `recovery`/`usage` outputs, which N4b's DoD (d) keeps fixed. So **queue, not this node.** Proposed node text: "friction(): repair tracking
reads INVOKED scripts through `friction.invoked_scripts` (after the N4b B1 fix); `classify` does not name `usage` on a call that passed `-h/--help`,
and does not name `validator` on a Bash result that no factory script produced; the old tallies move and the change lists, per kind, before ->
after on the three LR2-1 automator sessions; code_friction `--scripts` replayed." Owner: the Lead (pile of P1 measurers). Placement: a finding
plus a node row in the next unclaimed batch, per PROJECT.md «Командная работа» item 2.

## Answers by id

1. **Spec and the six answers.** N4b rows: (a) yes, rows on the fixture, hand-verified above; (b) yes; (c) §7.14 is met except B3; (d) the compat
   row is green; (e) the run is done but the reconciliation is wrong for refused (B2); "no norm" is respected (none written). The answers:
   - digits: executed as stated.
   - invoked-not-mentioned: executed with a private tokenizer that fails on heredoc bodies (B1), so it is executed partially.
   - signed list of six: exact (`friction-markers.json`, test row).
   - fragment pattern list in data: executed, with the Write/Edit scope chosen by the builder (N2).
   - two refused rows plus a total: executed as stated, but the data refutes row 2 (B2).
   - empty list stays unknown: executed.
   - split over all calls: executed (fixture hand count; the `at least` text).
   No answer was executed differently from its statement. B1 is a defect in the execution of answer 2.
2. **Readings.**
   - "first listed in command order among invoked listed scripts": sound. On real data, 5 attributed calls depend on it (`mk2.py`/`mk3.py`/`mk4.py`/
     `traceability.py` come first and `manifest_put.py` is the bookkeeping call). Under the other reading those calls would be lost.
   - `fragment_writes` as a sibling key of `bookkeeping`: sound. The script row keeps its meaning, and the report's "bookkeeping + fragment" figure
     is a sum in the report only.
   - `bookkeeping_fragment_patterns`: sound (see N4 for the loader key).
3. **Gap to the hand figures.**
   - Calls: reconciled by arithmetic. 42 attributed calls + 6 second invocations + 2 fragment writes = 50, so the hand basis looks like one per
     script invocation (a fit; the hand list is not recorded).
   - Seconds: the hand basis is undefined (7.3 s/call is neither our turn figure, 9.0, nor our execution figure, 3.8). This is not a counter
     defect, and both of our figures are labelled.
   - Refused: double counting of a non-class. Row 2 adds 9 non-refusals (B2). The true measured comparison is 13 vs 20, with the 7-call
     difference on an unknown hand basis.
   - Printed as fact while unknown: yes, `refused_total` `state: measured` (B2) and `refused` 0 for an unreachable role (B3).
4. **The `open_repairs` sibling:** queue, do not fix here (old outputs are fixed by DoD (d)). Node text in N5.
5. **One fact, one reader.** No second counter of per-call transcript tool results. Grep `tool_use_id|is_error` over the package scripts:
   `run_counters`, `collect_stall` and `driver_*` read `is_error` on driver-journal dispatch rows (a different fact: one row per dispatch);
   `dispatch_liveness.py:597` reads host acknowledgements; `code_friction.py` imports friction. In experiments, `read_misses.py:72` counts `is_error`
   for Read misses, a different fact. `retro_numbers` goes through `story_friction`. The positive control is the same grep finding
   `friction.py` (10 hits).
   Old outputs:
   - `story_friction` keeps its keys and its reason text (`_status(..., "shares")` gives the same "shares cover" sentence); only the dict key
     order changes.
   - `turns_of` is additive.
   - `friction()` changes only for digit-named scripts, as stated.
6. **FR-12:** the markers are a closed data list of OUR refusal spellings (AR-1), legitimate on host-flagged results. Row 2 applies them to
   unflagged results, where they matched the role's own text (2 of 9). See B2.
7. **Duplication / quality / census.**
   - DUPLICATION AND CONSISTENCY: one finding, B1 (a private tokenizer next to `hooklib.walk`/`command_segments`/`scan_bodies`). The session-loop
     refactor (`_role_sessions`/`_walk_sessions`) removed the duplicate journal loop, which is good. The row shape is duplicated inside the diff (N3).
     Grepped: `def _segments|command_segments|scan_bodies` across the package.
   - CODE QUALITY: N3 (`call_spans` about 70 lines; two row constructors) and N1 (`seconds_text`/`story_calls` with no production reader yet).
   - Census rename `_refused_total` -> `_two_row_total`: legitimate. The function is a pure sum with no refusal and no judgment. The `refuse*`
     pattern is a name heuristic for check units and this was a false match, so no check is hidden. The census stays 24/24 and no census or
     baseline file is in the diff.
8. **Class completeness (axes 6, 11, 18).**
   - Axis 6: code_friction's imports are kept (compat row); its `--scripts` column was replayed by the builder (0 differences). Nothing owed.
   - Axis 11: OWED (B1). The fix belongs on the shared walker, not as a private tokenizer. If the fix keeps any program-position code in friction,
     the axis-11 table gains a recognizer row in the same commit.
   - Axis 18: no ratchet row was added or raised (diff stat: six files, none of them a baseline or census). Nothing owed.

## Trail

Read: the spec rows above; both builder reports; the full code diff of friction.py, friction-markers.json and the changelog; test_friction.py
`timed_transcript`/`call_time_rows`/`INVOCATION_SHAPES`; `friction.py` `classify`/`friction()`; SIBLING_MAP axes 6, 11, 18;
`hooklib.py:1849-1970`; `run_counters.py:630-642`; critic-diff-brief items 6-7; the verdict schema.
Probes, all read-only (Bash heredoc payloads, nothing written in the tree):
- `call_spans` on the 3 automator sessions;
- per-call listing of bookkeeping and refused calls with result heads;
- `invoked_scripts` on 12 adversarial commands;
- a cross-check over all 82 stand transcripts;
- the `hooklib.cut_bodies` control;
- `story_calls` on a temp task root (one role reachable, one not).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1 friction.py:282-350 private shell tokenizer (SIBLING_MAP axis 11) reads heredoc bodies as commands and a quote inside a body hides later real invocations: 4 of 170 real stand commands lose a bookkeeping call; wrappers (timeout/env/sudo), bash -c and $PY are not read either",
    "B2 friction.py:437-479 named_by_marker row is 9 of 9 non-refusals on the three automator sessions (7 voluntary --help, 2 role-written text matching 'is refused'); refused_total prints them as measured refusals and the report's 41 percent missed / 2 calls over reconciliation is false (true: 13 flagged vs hand 20)",
    "B3 friction.py:773-779 story_calls: a role with no reachable session prints refused calls 0 with no state (the only stateless row), against the docstring and spec 7.14"
  ],
  "fixes": [
    "B1: build invoked_scripts on hooklib.scan_bodies + cut_bodies + command_segments (cleaned_word); keep only the program-position rule in friction; wrappers from launch-causes data or named unknown in CALL_TIME_METHOD; INVOCATION_SHAPES rows for heredoc body mention, apostrophe in body then a real call, a wrapper",
    "B2: Lead decides the row-2 shape; refused_total must not present row 2 as measured refusals (drop it, or label row 2 candidates with its own state); recommended row-2 narrowing: only calls invoking a factory script, and usage on a -h/--help call is not a refusal; builder corrects the report paragraph (13 measured vs 20, 9 non-refusals listed)",
    "B3: _empty_rows gives refused state unknown with a reason, call_spans gives it measured; role-level calls carries a state when reachable is 0; one story_call_time_rows row",
    "N1: Lead opens a node wiring run_counters T9/T10 to friction.story_calls; report line correcting the commit's AR-22 claim",
    "N2: Lead decides whether Bash redirect writes of *.values.yaml (11 of 39 on stand data) join fragment_writes; report states the scope",
    "N3: split call_spans (about 70 lines) and use one row constructor for call_spans and _empty_rows",
    "N4: loader key fragment_patterns renamed to the file key bookkeeping_fragment_patterns (optional)",
    "N5: queue a node: friction() repair tracking through invoked_scripts; classify does not name usage on --help nor validator on a Bash result no factory script produced; before/after tallies on the three LR2-1 sessions"
  ],
  "class_completeness": "Axis 6: code_friction imports kept, compat row green, nothing owed. Axis 11: owed, B1, the new command reader must ride hooklib walk/command_segments/scan_bodies or be named on the axis. Axis 18: no ratchet row added or raised. Same-surface neighbours walked for B1 (heredoc body, quote in body, wrappers, bash -c, variable program, case, redirects, empty). Sibling outside the node: friction() open_repairs and classify on --help and role text, queued as N5 with node text.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261113-p1v-run-scoreboard-spec.md (T9, T10, 2.1, 7.14, N4b, F15, F16)",
      ".claude/worktrees/p1v-n4b/docs/tasks/specs/reports/20261113-p1v-n4b-round2-report.md",
      "git diff 71d7ca8..d8b86a6 (friction.py, friction-markers.json, changelog.d, test_friction.py fixtures and rows)",
      "ai-packages/qa-factory/scripts/hooklib.py:1849-1970 (walk, scan_bodies, cut_bodies)",
      "ai-packages/qa-factory/scripts/run_counters.py:630-642",
      "docs/SIBLING_MAP.md axes 6, 11, 18",
      "docs/tasks/critic-diff-brief.md items 6-7",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "python -B scripts/tests/test_friction.py (package dir, subshell)", "result": "=== test_friction: 196/196 ok ==="},
      {"command": "python -B scripts/tests/test_judgment_census.py", "result": "=== judgment_census: 24/24 ok ==="},
      {"command": "python -B scripts/selftest.py --lang", "result": "=== qa-factory selftest: 2/2 ok ==="},
      {"command": "probe: friction.call_spans on db9a9038, 8325ed4c, 5a86e7e9", "result": "bookkeeping 42/164.4/375.7, fragment 2/4.4/19.8, refused 13/32.4/128.9, named 9/25.9/59.0, total 22/58.3/187.9 (reproduces row e)"},
      {"command": "probe: invoked_scripts vs python-invocation regex over 82 stand transcripts", "result": "170 commands, 4 differ, all a real invocation after a heredoc lost"},
      {"command": "probe: story_calls with one role unreachable", "result": "unreachable role refused (0, None), other rows unknown"}
    ]
  }
}
```

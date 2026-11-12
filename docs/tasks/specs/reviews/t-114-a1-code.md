# t-114 A1 code review (critic, diff gate) -- post-compaction lines, identity by content

Spec: `docs/tasks/specs/fg-context-and-hygiene.md` (Lead acceptance sections, §2 A goal/invariant/limits, A1 whole, §9).
Diff: worktree `.claude/worktrees/agent-af2af1d4bd0f91021`, `git diff HEAD` (base 25174f7), 4 files, +424/-71.
Builder report: `.../agent-af2af1d4bd0f91021/docs/tasks/specs/reports/t-114-a1-compact-lines.md`.

**Verdict: NEEDS WORK (fit_with_fixes) -- 2 blocking (B1, B2), 6 non-blocking (F1-F6).** The decision to accept
belongs to the Lead (rule 6); this is an input.

## Blocking

### B1 -- an old snapshot whose mtime was refreshed is shown as this compaction's (error direction broken)
`tools/session_context.py:2283-2297` -- age is computed from `st_mtime` only (`age_s(mtime)`), the header's own
`written:` field (which the diff writes precisely as the measurement time) is never read. Any operation that rewrites a
committed snapshot file refreshes its mtime: `git checkout`/`switch` to a branch without the file and back, `git stash
pop`, a merge/pull that brings the file, `git worktree add`. Snapshots ARE committed (`git ls-files
docs/tasks/compact-snapshots` = 10 files) and the Lead switches branches for pile work.

Concrete inputs (probe run, verbatim output below, P1/P2):
- P1: door snapshot `2026-11-12-1300-manual.md`, header `session: s1; written: 2026-11-12T13:00:00`, mtime refreshed 5 min
  before the 14:05 compaction (branch switch), PreCompact of this compaction failed, SessionStart session `s1` ->
  `COMPACT SNAPSHOT: docs/tasks/compact-snapshots/2026-11-12-1300-manual.md (5 min old, trigger manual)`. The file was
  measured 65 min ago, before an earlier compaction (it was written as the door of the previous MISSING, and a door
  snapshot is never put into the announced record). Violates the §2 invariant "a snapshot measured before an earlier
  compaction never counts as this compaction's" and A1's error direction "never toward fresh for a snapshot older than
  STALE_MIN".
- P2: another developer's snapshot from yesterday (header `session: unknown`, e.g. written by the door with no id)
  pulled 2 min ago -> shown as this compaction's `(2 min old, ...)`; the session clause cannot help (unknown).

Fix: in `this_compactions` (and in the displayed age) use the OLDER of the two ages: `max(age_s(mtime), age of the
header's written: parsed as local naive ISO)`; an unparseable/`unknown` `written` falls back to mtime alone. Errs only
toward MISSING (a written ahead of the clock gives a negative age, clamped by max with mtime). Test rows: "headed,
written 65 min ago, mtime 5 min" -> MISSING; "written unknown, mtime 3 min" -> fresh (corrupt-header edge unchanged).
The written field is read through `snapshot_identity` (already returns it), so AR-13/AR-22 stay intact.

### B2 -- a corrupt announced record is a permanent state whose named door does not open
`tools/session_context.py:2293`, `:2320`, `:2322-2325`. When `.claude/compact_seen.json` is unreadable, every candidate
counts as announced (correct direction), but the record is written only when `chosen is not None`, which can then
never happen: the file is never rewritten, so EVERY later compaction prints MISSING forever. The MISSING door (`python
-B tools/compact_snapshot.py --source manual ...`) writes a snapshot but does not cure the record; the line
`COMPACT SNAPSHOT: announced record unreadable (<reason>)` names what is wrong but neither what is expected nor a door
(P15, AR-9, AR-25: every recorded state has a way out). Probe P3: record = empty file -> MISSING + unreadable line,
record after the call still `''`. How the corruption arises in this very diff: `record.write_text(...)` (`:2325`) is
not atomic -- a hook killed mid-write, or two sessions writing at once (both open with truncate, the shorter content
lands over the longer one and leaves the tail -> invalid JSON). After that the mechanism degrades to a permanent
false MISSING, which trains the Lead to ignore the line -- the one failure mode this node exists to remove.

Fix (both parts, small): (1) write the record through the repository's atomic writer
`dod_track._atomic_write_text` (mkstemp beside the file + `os.replace`; already reused by
`dispatch_gate.py:1661-1671`) -- removes the partial-write source; (2) on an unreadable record, after printing MISSING,
REWRITE the record with the names of all hook snapshots now present (they all counted as announced anyway, so the
direction is kept) and say so in the line: `COMPACT SNAPSHOT: announced record unreadable (<reason>) -- rewritten with
the N snapshots present; the next compaction reads it`. If the Lead prefers no self-heal, the line must at least name
the door `delete .claude/compact_seen.json`. This extends the spec's edge text; the Lead confirms the variant (spec
gap, not a builder deviation -- the builder implemented the edge as written).

## Non-blocking

- **F1 -- `.claude/compact_seen.json` is not git-ignored.** `git check-ignore -v .claude/compact_seen.json` -> rc 1
  (`.gitignore` ignores `.claude/agent_budget/`, `.claude/dod_track/`, `.claude/dispatch_claims/` -- the comment at
  the dod_track line records the incident "a worktree commit carried them into main twice"). After the first
  compaction every clone has a new untracked file, and every hook snapshot lists it under UNCOMMITTED. Fix: one
  `.gitignore` line (outside the owns -> the Lead or an extended owns in the fix round).
- **F2 -- concurrent writers lose an update toward FRESH (named limit).** Read at `:2292`, write at `:2325`; session A
  and B compacting in the same instant both read the old list; the last writer drops the other's name; that session's
  next compaction within STALE_MIN with a failed PreCompact shows its old S as fresh (session matches). Window is
  milliseconds and needs a second coincidence; acceptable as a named limit beside "record not writable" for check 32
  (node P), or narrow it by re-reading the record immediately before the atomic write and merging. Not blocking.
- **F3 -- the `unavailable` path drops the AFTER COMPACT line** (`:2279-2281` and the outer except `:2331-2333` return a
  single line). Behaviour 4 makes `AFTER COMPACT: ... accept the OPEN DISPATCH lines in a batch` part of every compact
  block; when all files fail to read the dispatch instruction is the more needed. Fix: append the same AFTER line on
  both unavailable returns.
- **F4 -- two definitions of "narrative".** `compact_snapshot.py:73-78` REMINDER: "the newest `*-narrative.md`; the
  SessionStart line COMPACT NARRATIVE names it"; `session_context` COMPACT NARRATIVE = the newest UNHEADED `*.md`
  (behaviour 2). They differ: today no `*-narrative.md` exists, and after the merge every pre-A1 hook snapshot
  (`2026-11-12-1312-manual.md`, `*-auto.md`) and `*-lead.md` is "COMPACT NARRATIVE". Both texts follow the spec
  (items 2 and 6), so the residue is the spec's; the REMINDER's parenthesis "(the ... line COMPACT NARRATIVE names it)"
  claims an equivalence that does not hold -- drop the parenthesis or make COMPACT NARRATIVE prefer `*-narrative.md`
  when one exists. Lead's call with node P (PROJECT.md rename).
- **F5 -- edge with no test row: one file failing among several.** The edge "stat or read failure of a file -> that
  file is skipped" is tested only as "all failing -> unavailable" (`test_a1_unreadable_file_is_skipped_and_all_failing_is_unavailable`
  patches `snapshot_identity` for every file). Add a row: two headed files, the newer one's read raises OSError ->
  the older one is named. Code is correct by reading (`:2268-2276`), the row is the missing proof.
- **F6 -- code quality: `compact_snapshot_lines` is ~84 lines (`:2250-2333`) with four nested closures.** Over the
  ~60-line bar of brief item 7. Fold the record read/write into two helpers (`_read_announced` exists; add
  `_write_announced` with the atomic writer of B2) -- falls out of B2's fix. Fix before merge together with B2.

## Answers a-f

**a. Behaviours and edges.**
1 header + `snapshot_identity` (512 bytes, one reader, imported by session_context): met (`compact_snapshot.py:84-127`;
BOM and CRLF read fine, probe P4). 2 hook vs narrative by header, any name/suffix/source: met (rows `headed_suffix_2`,
`headed_other_source_name`). 3 eligibility: met as written, BUT the age is mtime-only -> B1. 4 block: met (MISSING with
`(newest hook snapshot <path, age>|none)`, NARRATIVE only when newer than S or S missing, AFTER line); the unavailable
path lacks AFTER -> F3. 5 record (append, keep 200): met (row `record_keeps_the_last_200`); non-atomic and no recovery
-> B2. 6 REMINDER: met as a data join; definition mismatch -> F4.
Edges: folder absent (row `no_folder`) met; one-file failure skipped -- met in code, NO test row (F5); all failing ->
unavailable + door met; record absent met (all `None` rows); record unreadable / not a list met (rows) but stuck (B2);
record not writable met (row); corrupt header -> `unknown` met (`test_snapshot_identity_round_trip_and_narratives` c.md);
clock skew -> 0 met; session id absent either side met (two rows); two sessions met; non-compact met (row through
`main`). Temporal both worlds met (`test_a1_old_unheaded_hook_snapshots_read_as_narratives`).

**b. Error direction / crash.** Yes, inputs shown as this compaction's though older than STALE_MIN: B1 (refreshed mtime,
P1/P2). Already-announced shown fresh: only the lost-update race (F2). Another session's: no, when both ids are known
(row `two_sessions...`); with an unknown id on either side the clause is skipped by spec. Unheaded: never (P-probe and
temporal test). Crash: none found -- every path is inside `try/except Exception` (`:2331`), `main` keeps its own outer
boundary; a directory named `*.md` (P5), non-str session id (P9), JSON `null` record (P8), non-str list items (P7),
odd chars in ids (P6) all degrade correctly.

**c. Builder's small decisions.** (1) `--session` printed only when SessionStart carries an id: right (a literal `<id>`
would be a door the reader cannot run; P15). (2) `(newest hook snapshot none)` without an age: right (no age exists).
(3) the record warning lines after AFTER COMPACT: consistent with the spec's "the block is printed and one line
follows"; fine. (4) public `clean_session_id`, `header_line`: right -- the writer of the form and the shared sanitiser
sit in the one module beside the reader (AR-22); both sides clean the id identically, so the compare is like for like
(P6 probe). (5) optional `session=`/`trigger=`: right; old callers (`run`, the probe case 13) unchanged. Against P15
the only gap is the unreadable-record line (B2).

**d. Test isolation / concurrency.** Every new test writes under `tmp_path` (`_a1_put`, `--root str(tmp_path)`,
`_scm.main(tmp_path)`); `test_reminder_names_only_what_exists` reads the real tree, writes nothing. Worktree
`git status --porcelain` after my two runs: only the 4 owned files + the report (verbatim below) -- nothing landed in
`.claude/` or `compact-snapshots/`. Other suites calling `main` with `source: compact` (`test_session_context_autoboot.py:120`)
use `tmp_path` too. Concurrency: two writers can (i) lose an update -> errs toward fresh (F2), (ii) corrupt the
file -> errs toward MISSING but permanently (B2). Neither is "lost update errs toward MISSING" as the dispatch requires.

**e. Other readers.** `hook_liveness_probe.py:1174-1183` reads the snapshot by `in text` markers (`# Compact snapshot --
manual` now on line 2) -> still passes; its anchor `COMPACT SNAPSHOT: docs/tasks/compact-snapshots/` is the writer's
stdout summary, unchanged; case 12 is import-only. No other caller of `compact_snapshot_line` (grep -i over the
worktree for `compact_snapshot_line|COMPACT SNAPSHOT|compact_seen|snapshot_identity|HOOK_HEADER_PREFIX`, positive
control = the same call finds `hook_liveness_probe.py`). Stale text: `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:933-944`
check 32 still describes "prints the newest one" and a `(none)` line -- node P's (§8), not this node. Package
`postcompact_reload.py` is the factory's own, unrelated.
DUPLICATION AND CONSISTENCY: one second implementation -- the non-atomic JSON write at `:2325` where the repo has
`dod_track._atomic_write_text` (reused by `dispatch_gate.py:1671`) and `piles.write_bytes_atomic` -> folded into B2.
The payload `session_id` read in `session_context.main` (`:2403`) duplicates `claim_control_gate._session_id` /
`search_control_gate._session_id` in shape (three lines, literal key) -- not worth a finding. `_ascii_sanitize` reused.
Grepped: `def .*(session_id|sanitize|safe_id|clean_)` and `atomic|os.replace` over tools/ (non-test).
CODE QUALITY: F6 (function length); no dead branch, no lying name found; the `(OSError, ValueError)` catch around
`snapshot_identity` is reachable (`open`); test lines (~270) exceed product lines (~220) but each row is a spec-named
edge -- no finding.
ARCHITECTURE: AR-22 and AR-13 kept (one writer/one reader of the header in `compact_snapshot.py`); AR-9/AR-25 gap = B2.
JUDGMENT: data check only (header, age, record); no census row; none. ONE ROAD: none found -- no branch on a shell,
language or project; the door is the same cwd-relative `python -B tools/...` form as every forge hook. Ratchets: none touched.
Class completeness (SIBLING_MAP): no axis names snapshot identity or record sidecars (grep -i `mtime|compact|sidecar|atomic`
in docs/SIBLING_MAP.md: only the git-runner, backlog-reader and journal-key rows, none on this class). Inside the
artifact: the mtime-only age is the single age computation of the function (applied in B1 for both the eligibility
and the displayed age); the non-atomic write is the single write (B2).

**f. Live-path behaviour.** `compact_snapshot` is imported lazily only on `source == "compact"`; its import chain is
stdlib + `gitcmd` (stdlib `subprocess`) -- no new dependency, negligible cost. A non-compact SessionStart runs no new
code (row `non_compact_source`; hook timing measured equal: main tree 8.22 s / worktree 7.94 s / main 8.25 s for the
startup path). The first compaction after placement: all existing snapshots are unheaded -> MISSING + NARRATIVE (the
temporal world the spec names) unless PreCompact of that compaction already runs the new writer -- both hooks land in
one merge, so it does. The record file appears untracked (F1).

## Control runs (verbatim)

R1 `python -m pytest <wt>/tools/test_session_context.py <wt>/tools/test_compact_snapshot.py -q -p no:cacheprovider`:
```
FAILED .claude/worktrees/agent-af2af1d4bd0f91021/tools/test_session_context.py::test_main_stdout_deadline_timeout_exits_immediately_via_subprocess
1 failed, 305 passed in 107.39s (0:01:47)
```
(`assert 13.639999999999418 < 10.0`.) Not caused by the diff: the test runs the startup path (no stdin), untouched;
re-runs: worktree `1 failed in 17.29s` (14.70 s), then worktree `1 passed in 10.77s`, main tree `1 passed in 10.00s`,
then main tree `1 failed in 17.02s` -- a load-bound timing test (FR-31 class) failing on both trees alike. The
builder's witness `306 passed in 63.50s` is consistent with the 305 + this flake.

R2 probe (python stdin script over temp dirs, importing the worktree modules; no repo write), output:
```
P1 ['COMPACT SNAPSHOT: docs/tasks/compact-snapshots/2026-11-12-1300-manual.md (5 min old, trigger manual)', 'AFTER COMPACT: read the snapshot above before your next action; accept the OPEN DISPATCH lines in a batch']
P2 ['COMPACT SNAPSHOT: docs/tasks/compact-snapshots/2026-11-11-0900-manual.md (2 min old, trigger manual)', 'AFTER COMPACT: ...']
P3a ['COMPACT SNAPSHOT: MISSING for this compaction (newest hook snapshot docs/tasks/compact-snapshots/2026-11-12-1403-manual.md, 2 min old) -- write it now: python -B tools/compact_snapshot.py --source manual --session s1', 'AFTER COMPACT: ...', 'COMPACT SNAPSHOT: announced record unreadable (not JSON: Expecting value: line 1 column 1 (char 0))']
P3b record after: ''
P4 {'session': 's1', 'trigger': 'auto', 'written': '2026-11-12T14:05:00'}
P5 ['COMPACT SNAPSHOT: docs/tasks/compact-snapshots/a.md (1 min old, trigger manual)', 'AFTER COMPACT: ...']
P6 ['COMPACT SNAPSHOT: docs/tasks/compact-snapshots/a.md (1 min old, trigger manual)', 'AFTER COMPACT: ...']
P7 ['COMPACT SNAPSHOT: MISSING for this compaction (newest hook snapshot docs/tasks/compact-snapshots/a.md, 1 min old) -- write it now: python -B tools/compact_snapshot.py --source manual --session s1', 'AFTER COMPACT: ...']
P8 ['COMPACT SNAPSHOT: MISSING for this compaction (...) -- write it now: ... --session s1', 'AFTER COMPACT: ...', 'COMPACT SNAPSHOT: announced record unreadable (not a JSON list)']
P9 ['COMPACT SNAPSHOT: docs/tasks/compact-snapshots/a.md (1 min old, trigger manual)', 'AFTER COMPACT: ...']
```
(P1: header written 13:00, mtime 5 min before now 14:05. P2: header written yesterday, session unknown, mtime 2 min.
P3: record = empty file. P4: BOM + CRLF header. P5: a directory `dir.md` in the folder. P6: id `ab;c-->` on both
sides. P7: record `["a.md", 3, null]`. P8: record `null`. P9: SessionStart id = int 12345. The repeated AFTER line is
abbreviated here as `...`; it was the full text in the output.)

R3 `git -C <wt> status --porcelain` after the runs:
```
 M tools/compact_snapshot.py
 M tools/session_context.py
 M tools/test_compact_snapshot.py
 M tools/test_session_context.py
?? docs/tasks/specs/reports/t-114-a1-compact-lines.md
```
R4 `git -C <wt> check-ignore -v .claude/compact_seen.json .claude/critic_snapshot.json` -> no output, `rc=1`.
R5 `git -C C:/QAFactory/forge-repo ls-files docs/tasks/compact-snapshots | wc -l` -> `10`.

## Trail

Read: the spec lines 1-150 (both Lead acceptance sections, §0 facts, §1, §2 A0-A3, A1 whole); t-098 F5 (lines
206-212, 335, 362, 377, 463); `docs/tasks/critic-diff-brief.md` items 6-12; the full diff of the 4 files; the builder
report; `tools/compact_snapshot.py:1-72` (imports, module state); `tools/session_context.py:2335-2424` (`main`);
`tools/hook_liveness_probe.py:1174-1183` + grep of compact/session_context uses; `tools/test_hook_liveness_probe.py`
compact rows; `tools/test_session_context_autoboot.py:100-137`; `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:928-944`;
`.gitignore`; `tools/critic_verdict.schema.json`; `docs/SIBLING_MAP.md` matched rows; `claim_control_gate.py:815-824`,
`dod_gate.py:164-175`.
Needed beyond the manifest: `.gitignore`, `dod_track._atomic_write_text` (by grep), `hook_liveness_probe.py`,
`test_session_context_autoboot.py`, the calibration protocol check 32.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1 session_context.py:2283-2297 age is mtime-only; a committed snapshot whose mtime a checkout/pull/stash refreshed is shown as this compaction's though written 65 min earlier (probe P1, P2) -- breaks the A1 error direction; use the older of mtime age and the header written: age",
    "B2 session_context.py:2293,2320,2322-2325 a corrupt record is never rewritten (write only when a snapshot is chosen), so every later compaction is MISSING forever and the MISSING door does not cure it; the unreadable line names no door (P15, AR-25); the write is non-atomic, which is how it corrupts"
  ],
  "fixes": [
    "B1: in this_compactions and the displayed age use max(mtime age, age of identity written parsed as local ISO); unknown/unparseable written falls back to mtime; add rows written-65-min-mtime-5-min -> MISSING and written-unknown -> fresh",
    "B2: write the record through dod_track._atomic_write_text; on an unreadable record rewrite it with the names of all hook snapshots present and say so in the line (or at least name the door delete .claude/compact_seen.json); Lead confirms the variant (spec edge extension)",
    "F1: add .claude/compact_seen.json to .gitignore (outside owns: Lead or extended owns)",
    "F2: name the concurrent lost-update residual (errs toward fresh) as a limit for check 32, or re-read and merge right before the atomic write",
    "F3: append the AFTER COMPACT line on both unavailable returns",
    "F4: drop the REMINDER parenthesis claiming COMPACT NARRATIVE names the newest *-narrative.md, or make COMPACT NARRATIVE prefer *-narrative.md; Lead with node P",
    "F5: add a test row: two headed files, the newer one unreadable -> the older one is named",
    "F6: split compact_snapshot_lines (about 84 lines, four closures) -- a _write_announced helper falls out of B2"
  ],
  "class_completeness": "No SIBLING_MAP axis covers snapshot identity or hook sidecar records (grep -i mtime|compact|sidecar|atomic: only git-runner, backlog-reader, journal-key rows). Inside the artifact: one age computation (B1 covers eligibility and the shown age), one record write (B2), one reader of the header (snapshot_identity, AR-13 kept). Stale text in check 32 of the calibration protocol belongs to node P (spec section 8), already planned.",
  "trail": {
    "read": [
      "docs/tasks/specs/fg-context-and-hygiene.md:1-150",
      "docs/tasks/specs/reviews/t-098-fg-context-hygiene-plan.md F5 lines",
      "docs/tasks/critic-diff-brief.md:40-89",
      "worktree diff of tools/compact_snapshot.py, tools/session_context.py, tools/test_session_context.py, tools/test_compact_snapshot.py",
      "worktree docs/tasks/specs/reports/t-114-a1-compact-lines.md",
      "tools/compact_snapshot.py:1-72",
      "tools/session_context.py:2335-2424",
      "tools/hook_liveness_probe.py:1174-1183",
      "tools/test_session_context_autoboot.py:100-137",
      "PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:928-944",
      ".gitignore",
      "docs/SIBLING_MAP.md matched rows",
      "tools/claim_control_gate.py:815-824",
      "tools/dod_gate.py:164-175"
    ],
    "reruns": [
      {"command": "python -m pytest <wt>/tools/test_session_context.py <wt>/tools/test_compact_snapshot.py -q -p no:cacheprovider", "result": "1 failed, 305 passed in 107.39s; the failure is the load-bound timing test test_main_stdout_deadline_timeout_exits_immediately_via_subprocess (startup path, untouched), which also failed once on the main tree and passed once on the worktree"},
      {"command": "python -B - <wt>/tools (stdin probe over temp dirs, P1-P9)", "result": "P1 and P2 show a 65-min / 1-day old headed snapshot as fresh (B1); P3 record stays empty after the call (B2); P4-P9 degrade correctly"},
      {"command": "git -C <wt> status --porcelain", "result": "only the 4 owned files and the builder report"},
      {"command": "git -C <wt> check-ignore -v .claude/compact_seen.json", "result": "no output, rc=1 (not ignored)"}
    ]
  }
}
```

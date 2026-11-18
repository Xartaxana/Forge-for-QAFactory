# FG7-55 -- the session walk never takes the app's utility process for the session (draft card, t-1412)

Designer draft for the Lead. Node `forge/7/FG7-55` (P3), finding
`plans/piles/forge/findings/20261117-wait-reaper-walk-names-the-apps-utility-process.md`, critic t-1160 N1.
Decisions are the Lead's: the forks in §6 are returned, not closed.

## 0. Target on main, measured (file:symbol)

- `tools/session_proc.py::walk` decides "this ancestor is the session" by ONE test: `procs[ppid][1].lower() in names`
  (the first parent whose Toolhelp exe NAME, lower-cased, is in the row) -> `{"pid": ppid, "created": parent_created}`.
  Fields read per hop: ppid and exe name from `WinApi.snapshot` (`szExeFile`, a bare file name, no directory), creation
  time from `WinApi.created` (its own `OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION)` + `GetProcessTimes`). The start
  process itself is never a candidate (the test is on the parent). F-R3 (parent older than child) and HOP_CAP=32 precede
  the name test.
- `tools/session_proc.py::session_process` builds `names` from `wait-reaper.json` `session_process_names[nt|posix]`;
  an empty row -> `POSIX_NOT_MEASURED` (posix) / `NO_CLAUDE` (nt) before any OS call.
- The command line is read NOWHERE in `session_proc.py` (Toolhelp carries none). The only command-line reader of
  processes is `tools/wait_reaper.py::PS_LIST` (a PowerShell CIM child: `ProcessId,ParentProcessId,Name,CreationDate,
  CommandLine`) used for selection, not for the session.
- The image PATH is read nowhere in `tools/`: Grep `QueryFullProcessImageName` (case-insensitive) over the repo hits
  only review/finding/pile prose (t-1131, t-1160, the finding, the batch row); positive control: the same Grep shape
  found `t-1160-bounded-waits-reaper-code.md:87`.
- `tools/wait-reaper.json::session_process_names` = `{"nt": ["claude.exe"], "posix": []}`; `load_rows` is its one
  reader (docstring claim, confirmed: Grep `wait-reaper\.json|ROWS_PATH` over `tools/` hits only `session_proc.py`,
  `mechanism_gate.py:287` (a path list) and tests).
- The docstring of `session_proc.py` (lines 8-12) claims "the app above it is never reached" and "it never names a wrong
  process": both false on the measured layout below.
- Measured layout (frozen measurements, not mine): `docs/tasks/specs/reviews/t-1131-bounded-waits-plan.md` lines 16-25 --
  session `claude.exe` 26860 image `...\claude-code\2.1.321\...\claude.exe`; its parent the app `claude.exe` 17100 image
  `C:\Program Files\WindowsApps\Claude_5.1231.2.0_x64__...\app\Claude.exe`; the app's terminals `powershell -NoExit`
  8900/10312 are children of helper `claude.exe` 11816, itself a child of 17100. `t-1160...md` line 167: 11816 is
  `Claude.exe --type=utility`.
- Behaviour today in an app terminal (derived from the code above): walk from python -> powershell 8900 -> 11816 (name
  matches) -> session = 11816. `wait_reaper.run` then logs each non-wrapper child as `unknown-root` (check 27(e) false
  lead); `compact_snapshot` would stamp a narrative with 11816 (a wrong stamp); `session_context.waits_lines` reports
  the reaper for 11816.

## 1. Architecture

- The spec touches no path under `ai-packages/qa-factory/`: rule 1's AR/census duty does not bind. Named by analogy, as
  the brief asks: AR-1 (closed variety is a data row: the session image marker is a row of `wait-reaper.json`, beside
  `session_process_names`, not a constant in code -- but see fork F2); AR-13 (one reader: the new row is read only
  through `session_proc.load_rows`; no second parser of `wait-reaper.json`; change check: Grep `wait-reaper` over
  `tools/` after the edit still shows only `session_proc.py` as a parser).
- Owner of the new check: data (code) -- a path compare, no judgment. Census class: n/a (forge tool).
- `variety: none -- forge tool outside the package; the seat-install variety it meets (bundled vs CLI install) is fork F3`.
- Error direction of the changed function (it is a gate input: the reaper stops trees under the named session): the walk
  may fail to find a session; it never names a process that is not a session. Adversarial inputs that must stay on the
  safe side: the app main and its helpers (same exe name, app image); a user directory whose name CONTAINS the marker
  (`C:\Users\claude-code-fan\...`); an image read that fails; an image read on a reused pid; an empty or absent row; a
  nested `claude.exe` of another install under a recognised session.

## 2. Design (recommended options of §6 assumed; each marked by its fork)

1. Data (F2): `tools/wait-reaper.json` gains `"session_image_dirs": {"nt": ["claude-code"], "posix": []}`: directory
   segment names that an image path must contain for its process to be a session. `load_rows` validates it like
   `session_process_names` (a dict with list values under `nt` and `posix`) and names it in the RowsError message.
2. Seam: `WinApi.identity(pid) -> (created, image)` opens ONE handle (`PROCESS_QUERY_LIMITED_INFORMATION`), reads
   `GetProcessTimes` and `QueryFullProcessImageNameW(handle, 0, buf, &size)` on it, closes it; any failure raises OSError
   with `winerror` (the class's existing contract). `PosixApi.identity(pid) -> (self.created(pid),
   os.readlink("/proc/%d/exe" % pid))` (one road on both seams; unreached while the posix rows are empty).
3. Walk (F1, F4): the name test stays the cheap pre-filter. At the hop whose parent name matches, the walk calls
   `api.identity(ppid)` INSTEAD of `api.created(ppid)` and uses that creation time for the F-R3 check and the result.
   The FIRST name-matching ancestor is the ONLY candidate: image has a directory segment (case-insensitive, split on `\`
   and `/`, the file-name segment excluded) equal to a row value -> it is the session; otherwise -> `(None,
   NOT_SESSION_IMAGE % ppid)` with `NOT_SESSION_IMAGE = "claude.exe ancestor %d is not a session image"`. The walk never
   continues past a name match.
4. `session_process`: names row non-empty but `session_image_dirs` row for the platform empty -> `(None,
   IMAGE_NOT_MEASURED)` with `IMAGE_NOT_MEASURED = "session image dirs not measured"`, before any OS call. The posix
   names row stays empty, so posix still answers `POSIX_NOT_MEASURED` first (order unchanged).
5. Docstrings of `session_proc.py` (module and `session_process` reasons list) say the new rule and the two new reasons;
   the false sentence "the app above it is never reached" goes.

Result on the measured layout: app terminal -> 11816 is the first name match, its image lacks `claude-code` ->
`no session: claude.exe ancestor 11816 is not a session image`; the reaper logs `no-session: ...`, `launch` answers
`WAITS: no session (...) -- nothing stopped`, the narrative stamp is refused with the reason. A harness tool call ->
26860, image under `claude-code` -> unchanged session.

## 3. Edges, each with its invariant

- E1 (the finding): first name-matching ancestor is the app's utility process (app image) -> `(None, NOT_SESSION_IMAGE %
  pid)`. Invariant: a process whose image is not a session image is never returned as the session.
- E2 `QueryFullProcessImageNameW` or its `OpenProcess` fails (access denied 5, exited 87, buffer) -> the existing
  `except OSError` -> `(None, "api error <n>")`. Invariant: an unreadable image never counts as a match and never falls
  back to the name alone.
- E3 pid reused between snapshot and the image read: image and creation time come from ONE handle and that creation time
  feeds F-R3 -> a reused (younger) pid fails F-R3 -> `orphan at <name>`. Invariant: an image measured on another process
  never counts.
- E4 non-Windows host: posix names row empty -> `POSIX_NOT_MEASURED` before any OS call (unchanged). Invariant: posix
  names no session until both posix rows are measured; a filled posix names row with an empty posix image row ->
  `IMAGE_NOT_MEASURED`, never a name-only session.
- E5 the app path absent from `wait-reaper.json`: the design never lists the app (allow-list, F1) -> the app and all its
  helpers are refused because their image lacks the marker, wherever the app is installed. Invariant: an image not
  matched by the row is never a session. The session's own install absent from the row (a new layout) -> E1's reason
  names the residual on every WAITS line; nothing is stopped.
- E6 a process whose image matches but is the session itself = the walk STARTS at a session pid (`start_pid` = 26860):
  the start is never a candidate (unchanged), the next name match is the app -> refused by image -> `(None,
  NOT_SESSION_IMAGE % 17100)`. Invariant: a walk from a session never names the app (today it does).
- E7 nested `claude.exe` of another install under a recognised session (e.g. a CLI child of a tool call): it is the first
  name match, its image misses -> `(None, NOT_SESSION_IMAGE)`; the walk does NOT go on to the outer session. Invariant:
  the walk never names a process above the first name match.
- E8 ancestors chain ending early (ppid 0, self, absent from the snapshot) before any name match -> `NO_CLAUDE`
  (unchanged); F-R3 failure -> `orphan at <name>`; over 32 hops -> `hops over 32`. All precede the image read.
  Invariant: no image is read for a process the walk did not reach.
- E9 image row value inside a longer segment (`claude-code-fan`, `claude-code.bak`) or as a file name
  (`...\bin\claude-code`) -> no match (segment equality, file-name segment excluded). Case (`CLAUDE-CODE`) and slash form
  (`/`) -> match. Empty image string -> no segments -> no match -> E1 reason. Invariant: the marker is a whole directory
  name, never a substring.
- E10 TEMPORAL: the row `session_image_dirs` is brought into existence by this change. Before the commit: code and file
  both old, behaviour as §0. After: both new. A copy of `session_proc.py` new with an old `wait-reaper.json` (they sit in
  one folder, one commit; only a hand-mixed worktree) -> `RowsError` naming the row; `session_process` returns it as the
  reason, the reaper exits 1, nothing stopped. Invariant: no default selection when the row is missing.
- E11 POSITIONAL: the image test sits AFTER F-R3 and the hop cap of the same hop and REPLACES the name-only return. It
  must keep unreachable: a session named without an image check; an image read before F-R3 decides the hop.

## 4. Builder card

given: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-fg7-55-reaper-utility-process-card.md (§0-§3, §5), C:/QAFactory/forge-repo/tools/session_proc.py, C:/QAFactory/forge-repo/tools/wait-reaper.json, C:/QAFactory/forge-repo/tools/test_wait_reaper.py (the walk block: `FakeOs`, `chain`, `app_over_session`, `WALKS`, `test_broken_rows_file_is_named_never_a_default`)
owns:
C:/QAFactory/forge-repo/tools/session_proc.py
C:/QAFactory/forge-repo/tools/wait-reaper.json
C:/QAFactory/forge-repo/tools/test_wait_reaper.py
non-goals: no edit of `tools/wait_reaper.py` (its calls are unchanged); no command-line read; no change to selection, never_reap or wrapper rows; no edit of the frozen bounded-waits specs; no live reaper run beyond `python -B tools/session_proc.py` (read-only); mechanism files are STAGED by the builder and COMMITTED by the Lead (`tools/mechanism_gate.py` lists `tools/session_proc.py` and `tools/wait-reaper.json`)
handoff: the staged diff of the three owns + report: the `python -B tools/session_proc.py` line from the builder's Bash tool call (a harness session, expected the session found) and the test tail
edges: E1-E11 of the given spec §3, each with its invariant; E10 both worlds; E11 position
DoD: `python -m pytest tools/test_wait_reaper.py -q`
siblings: none -- `session_proc.walk` is the one process-walk reader and `wait-reaper.json` the one data file; `wait_reaper.PS_LIST` lists processes for selection, not for the session, and stays unchanged
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-fg7-55-reaper-utility-process-card.md

Acceptance criteria: §2 items 1-5 as written; the three readers of `session_process` (§5) need no edit; the report
names any test line not written (`tests not written: <line> -- over budget`).

test lines, strongest first (all in `tools/test_wait_reaper.py`; `FakeOs` gains an `images` map and an `identity(pid)`
that honours `fail` like `created`; `app_over_session` gives pid 2 a `...\claude-code\2.1.321\claude.exe` image and
pid 3 an app image, so the row `found` keeps its expectation):

- test: tools/test_wait_reaper.py::WALKS row `utility-not-session` (bash -> claude.exe app image -> claude.exe app image
  -> explorer; want `(None, NOT_SESSION_IMAGE % 2)`) | expected from: finding "Test", spec §3 E1
- test: tools/test_wait_reaper.py::WALKS row `image-unreadable` (fail on the name-matching pid -> `api error 5`) |
  expected from: spec §3 E2
- test: tools/test_wait_reaper.py::WALKS row `nested-other-install` (inner claude.exe with a non-session image under an
  outer session image; want the inner refusal, not the outer pid) | expected from: spec §3 E7
- test: tools/test_wait_reaper.py::WALKS rows `marker-substring` / `marker-case-slash` / `image-empty` (one row each:
  `C:\Users\claude-code-fan\x\claude.exe` -> refused; `C:/X/CLAUDE-CODE/2/claude.exe` -> found; `""` -> refused) |
  expected from: spec §3 E9 (host answer: outside input, adversarial rows)
- test: tools/test_wait_reaper.py::test_broken_rows_file_is_named_never_a_default (one more variant: the real rows minus
  `session_image_dirs` -> `RowsError`) | expected from: spec §3 E10
- test: tools/test_wait_reaper.py::WALKS row `image-row-empty` (rows copy with `session_image_dirs.nt = []` -> `(None,
  IMAGE_NOT_MEASURED)`) | expected from: spec §3 E4

Budget note: the code side is roughly the `identity` seam on two classes, the walk branch, two constants, the
`load_rows` check, two JSON lines and docstrings; the last two test lines are the first to drop.

## 5. Readers of every touched file

No `tools/owns_readers.py` block came with the brief (`facts: none`); hand grep instead (Grep tool, repo minus
`.claude/worktrees/`): `session_proc|wait-reaper\.json|session_process_names` -> 138 hits in 25 files; positive control:
the same call counts `tools/session_proc.py: 11`. `.githooks/`: `session_proc|wait-reaper|wait_reaper` -> 2 hits
(`post-merge` lines 9, 12). The plan critic re-runs `owns_readers.py` (block missing, Q13 (d)).

| touched file / name | reader | status |
|---|---|---|
| `session_proc.session_process` | `tools/wait_reaper.py::run` (441), `::launch` (549) | unchanged code; app terminal now answers `no session` (was 11816) |
| `session_proc.session_process` | `tools/session_context.py::waits_lines` (1959), `::_session_proc_id` (2611) | unchanged code; WAITS line / stamp id become "no session" in an app terminal |
| `session_proc.session_process` | `tools/compact_snapshot.py` stamp door (186-191) | unchanged code; stamping from an app terminal is refused with the reason (was a wrong stamp) |
| `session_proc.session_process` | `tools/test_compact_snapshot.py` 730-738, `tools/test_session_context.py` 2199-2339 | unchanged: they monkeypatch `session_process`, signature kept |
| `session_proc.load_rows`, `RowsError`, `error_code`, `default_api` | `tools/wait_reaper.py` (422-423, 339, 349, 518) | unchanged |
| `WinApi` / `PosixApi` (new `identity`) | `tools/wait_reaper.py::stop_tree` via `default_api` (uses `open_terminable/terminate/exited/close`) | unchanged; `FakeKill` in tests needs no `identity` |
| `tools/session_proc.py` path | `tools/mechanism_gate.py:286` (mechanism list) | unchanged; it forces the stage/commit split of §4 |
| `tools/wait-reaper.json` | `session_proc.load_rows` (the one reader) | changes in this card |
| `tools/wait-reaper.json` path | `tools/mechanism_gate.py:287` (comment names `never_reap, limit_seconds, wrapper_forms`) | unchanged (comment incomplete, not false; see small choice C5) |
| `tools/wait-reaper.json` | `docs/SIBLING_MAP.md:294` (names only `wrapper_forms`) | unchanged |
| `tools/wait_reaper.py` (hook entry) | `.githooks/post-merge` 9-12, `tools/dod_gate.py` 763-764, `session_context.waits_lines` | unchanged; `launch` prints the new reason in an app terminal |
| `tools/test_wait_reaper.py` | none outside itself | changes in this card |

## 6. Forks (returned, not decided)

- F1 How the walk tells the session from the app. (a) RECOMMENDED: image path allow-list (`QueryFullProcessImageNameW`,
  in-process, a directory segment from a row). (b) Command-line flag `--type=`: needs a command-line read the walk does not
  have (in-process only through `NtQueryInformationProcess` class 60, or a child process, which §5.0's "no child
  process" forbids); and on the measured layout skipping 11816 leads to its parent 17100, the app MAIN, which carries no
  `--type=` -> the app itself would be named (moves the fault one hop up, worse: its children are sessions and helpers).
  (c) Deny-list of the app image (`WindowsApps\Claude_`): an app installed elsewhere is named again (errs unsafe).
- F2 Where the marker lives. (a) RECOMMENDED: a row `session_image_dirs` in `wait-reaper.json` beside
  `session_process_names` (one data file; edits pass the mechanism review). (b) A code constant in `session_proc.py`
  (one file less; a new layout needs a code edit).
- F3 `narrows`: seats whose session `claude.exe` is not under a `claude-code` directory (estimate: a native CLI install
  such as `%USERPROFILE%\.local\bin\claude.exe`, not measured) lose their session: today they are found by name, after
  the change they answer E1's reason and the reaper stops nothing. (a) RECOMMENDED: the Lead measures once whether a CLI
  install exists on this seat (`where.exe claude`; read-only) and, if so, its directory joins the row in this card;
  (b) ship `claude-code` only and open a residual node with owns `tools/wait-reaper.json` and a WALKS row. Cost of
  covering: one row value plus one test row per measured layout.
- F4 Stop at the first name match (recommended, E7: never names a process above it) vs continue past a refused name
  match (finds a session above an app helper, but can name an OUTER session for a nested run of another install).
- F5 Code at all, or "names the residual by a line" only (correct the docstring, record the residual). Recommended:
  code; the fix is small and the residual today produces false `unknown-root` leads and wrong narrative stamps.

Load-bearing estimates the Lead measures before dispatch (no shell here), read-only, one shot:
- `Get-CimInstance Win32_Process -Filter "Name='claude.exe'" | Select-Object ProcessId,ParentProcessId,ExecutablePath | Format-Table -AutoSize`
  -> expected: the session pid's path has a `claude-code` directory segment; the app main and EVERY helper (including the
  `--type=utility` parent of `powershell -NoExit`) have none. If a helper's path has one, F1(a) does not hold.
- `where.exe claude` -> F3.

## 7. Small choices closed by the designer

- C1 Row name `session_image_dirs`; values are directory segment names, compared case-insensitively.
- C2 Segment equality, not substring (E9); the file-name segment is excluded.
- C3 Image buffer: one 32768-WCHAR buffer, no retry loop (covers the long-path maximum; a failure is E2).
- C4 Reason strings are constants with a pid only, no path: ASCII by construction (the path may hold a non-ASCII user
  name), and within `REASON_MAX` 120 of `wait_reaper`.
- C5 `mechanism_gate.py:287` comment left as is (not in owns, not false); the Lead may extend it when committing.
- C6 `PosixApi.identity` implemented (readlink) for one road on both seams; no test (unreached while posix rows are empty).

## 8. Reading trail

- Read whole: `tools/session_proc.py` (257 lines), `tools/wait-reaper.json`, the finding.
- Read slices: `tools/test_wait_reaper.py` 185-264; `tools/wait_reaper.py` 51-52, 436-447, 544-555;
  `tools/session_context.py` 1948-1967; `tools/compact_snapshot.py` 172-193; `tools/mechanism_gate.py` 270-294;
  `docs/tasks/specs/reviews/t-1131-bounded-waits-plan.md` 10-29; `t-1160-bounded-waits-reaper-code.md` 78-91, 160-171;
  `ai-packages/qa-factory/design/architecture.md` 74-81, 200-205; `docs/TESTING.md` 75-104, 213-250;
  `docs/SIBLING_MAP.md` 294.
- Greps: the pile row `FG7-55` (batch file line 80); `^def|^class|...` over `session_proc.py`, `wait_reaper.py`,
  `test_wait_reaper.py`; readers grep of §5; `wait-reaper\.json|ROWS_PATH` over `tools/`; `QueryFullProcessImageName|
  type=utility|claude-code\\|AnthropicClaude` (case-insensitive) over the repo -> prose only (control in §0);
  `test_wait_reaper` in `tools/*.json` -> 0 (forge tests carry no keep row, TESTING.md line 236 confirms; no control
  needed for a rule-confirmed absence).
- Noticed, not widened: critic t-1160 N2 (any child counts as an unknown root) and N3 (`never_reap` matched on the user's
  command) are neighbours of this node, not in its scope.

## 9. Lead decisions (18.11, Lead 501cb4e0, accepted)

Measured before deciding (read-only, PowerShell, this seat): `Get-CimInstance Win32_Process -Filter "Name='claude.exe'"`
-> 15 processes; the two sessions 26860 and 41128 have images `...\AppData\Local\Claude-Data\<id>\claude-code\2.1.321\<hash>\claude.exe`;
the app main 17100 and all 12 helpers (crashpad-handler, gpu-process, renderer, utility incl. 11816) have
`C:\Program Files\WindowsApps\Claude_5.1231.2.0_x64__...\app\Claude.exe` (no `claude-code` segment). `where.exe claude`
-> only the npm shims `...\AppData\Roaming\npm\claude` and `claude.cmd` (they run node.exe, which the names row does not
match today either).
- F1: (a) image path allow-list. The measurement holds it: no helper carries the marker.
- F2: (a) the row `session_image_dirs` in `wait-reaper.json`.
- F3: (b) ship `claude-code` only, and no residual node: no native `claude.exe` CLI install exists on this seat, and the
  npm install is not name-matched today, so the change narrows nothing measured.
- F4: stop at the first name match (E7).
- F5: code.
The builder card of section 4 stands as written.

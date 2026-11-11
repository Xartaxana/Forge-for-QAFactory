# t-2153 — critic on plan: t-2148 TR4-2 one file lock (spec `docs/tasks/specs/t-2148-tr4-2-one-file-lock.md`)

Critic (Opus), 10.11.2026. Plan review, no code exists. Reviewed against the finding `plans/piles/thinking-roles/findings/20261106-kopii-zamka-fajla-v-pakete.md`,
row TR4-2 and the order line of `batch-4-ostatki.md`, the spec's "Lead decisions on the forks", the eleven sites under
`ai-packages/qa-factory/scripts/`, and `docs/tasks/critic-diff-brief.md` (questions 10, 11, DUPLICATION) plus the
"node written for a weaker model" rule. All `file:line` below are under `ai-packages/qa-factory/scripts/` unless another path is given.

**Verdict: fit_with_fixes (NEEDS WORK).** The direction is right: the facts hold, D1-D4 are real, the home, the census reasoning
and the split are sound. Six blocking spec defects remain. Each one either makes a builder's DoD unmeetable as written or ships
a wrong behaviour that the parts' tests would not catch (several of them show up only on Windows, or only on the Linux CI image).
Each is fixed by spec text, given below as exact replacement lines. None needs a new fork to the owner. Two of them (B5, and the
N1 choice) are Lead decisions; I give a recommendation for each and do not decide.

---

## Blocking findings

### B1. The platform switch through `_is_windows()` breaks `test_event_store.py` on the Linux CI image

Spec section 2, Mechanics: "Platform switch through the existing seam `_is_windows()` (`:108-111`)". C1 today switches on
`os.name == "nt"` (`event_store.py:322`, `:335`). The `_is_windows` seam exists so tests can flip the replace-retry behaviour
"without changing os.name" (`event_store.py:108-111`). Those tests also COMMIT under the flip:
`tests/test_event_store.py:326-328` (`test_a_brief_race_inside_a_projection_does_not_make_it_stale`) and `:338-341`
(`..._still_reads_as_committed_stale`) run `self.store.commit(...)` inside `patch("event_store._is_windows", return_value=True)`.
`commit` takes `self.lock()`.
Scenario: CI python:3.12 on Linux. `_is_windows()` is True, so the helper runs `import msvcrt`, which raises ImportError. That
becomes LockBroken, then StateConflict "task has an active state writer". Test :329 fails on `event["sequence"]`, and test
:342 gets the wrong StateConflict text. Part A's own DoD file goes red on CI only; the builder's local Windows run passes.
Surface: the platform seam. Neighbours walked: `test_stage_done_lock_order.py:174-192` and `test_config_view.py:280` flip the
same seam only around `replace_file` / `atomic_text`, which take no lock, so they are unaffected. No other test flips it
(grep `_is_windows` over `scripts/tests`: 3 files).

### B2. LockBroken folded into the BUSY refusals: a broken primitive reported as "another writer", and a silent skip in hooks

Spec section 2, "Callers that today read ANY failure as busy (C1-C3, C6, C7, C9) catch `(LockBusy, LockBroken)` and keep their
refusal", and part A edges "`EventStore.lock` translates LockBusy AND LockBroken to StateConflict". The parenthesis "(today any
OSError of the lock call is the conflict)" holds only for the LOCK CALL. The spec's LockBroken also covers "the file cannot be
opened/made (missing permission, read-only FS, a folder at that path), the platform module is missing". Today those raise a raw
OSError outside every try: `event_store.py:312-313` (`mkdir`, `open("a+b")`), `case_versions.py:39-43`, `:198-201`,
`manual_capture.py:805-810`, `question_register.py:775-779`.
Scenarios:
(a) `<task>/state/events.lock` is unopenable (an old FOLDER of that name, a read-only copy of a project). Every hook writer
(wait 0, "busy means skip", `event_store.py:303-304`) now reads StateConflict and skips silently, on every tool call, for the
rest of the run. Today the same input fails loudly with PermissionError or IsADirectoryError. That breaks AR-28 (an unknown
becomes a skip) and FR-46 (the factory's or environment's fault is presented as the call's).
(b) C7 on a read-only `work/.question-answers.lock`: LockBroken comes at once, yet the text says "another writer has held
<path> for 30 s ... try again in a moment" plus "held by <holder>". All three claims are false (FR-1). `claim_projector.py:647-649`
then tells the driver "another writer holds the answers lock ... the driver repeats the step", which loops forever.
(c) The same pattern applies to C2/C3 (`RuntimeError("... has an active writer")`) and C6 ("held by another walker for over 20 s").
Surface: the error direction of the helper's callers. Neighbours walked: C8 already splits held/broken (kept). C9 maps to the
words held/free/unknown (correct). C4/C5 per part C go to `invalid_schedule`, `lease_error` or `invalid_estimate`, where the
sentence is the helper's own and stays honest once LockBroken has its own sentence. E1/E2 per part D take the same fix as C2/C3.
AR-20/AR-29 are not affected (see Q3); this is FR-1/FR-46/AR-28.

### B3. Part B: `test_probe_by_code_copy.py` injects `PBC._os_lock`, and the spec both removes `_os_lock` and promises those tests "stay green unchanged"

Part B owns "`_os_lock`, `_os_unlock`, `try_lock`, `release_locks`", and its Tests line says "existing ones stay green unchanged
(`test_probe_by_code_copy.py:318-348`)". Those tests replace the module attribute: `PBC._os_lock = raising(OSError(code, name))`
at `:337` (expects "held" for the four HELD_ERRNOS) and `raising(EBADF|ENOSPC|EIO|ImportError)` at `:341` (expects "broken").
The same pattern appears at `:371` (`no_primitive`), `:397` (`held`), `:409` (`broken`) and `:415`.
Scenario: `try_lock` delegates to `event_store.take_file_lock`, so the patched `PBC._os_lock` is never called. A free lock is
"locked" where "held" or "broken" is expected, and seven or more checks go red. A Sonnet builder then either edits the test
(not owned) or keeps a private msvcrt copy (the ratchet then still lists probe_by_code.py). Either way part B cannot meet its DoD.

### B4. Part D: its owns and DoD miss five test files that the change necessarily breaks

Part D owns only `test_install_retire.py` "at :916, :947-948 only". Measured:
- `tests/test_exit_gate_lock_wait.py`: pins `(LOCK_WAIT_STEPS, LOCK_STEP_S) == (1000, 0.01)` (`:31`). It simulates "busy" by
  the file's EXISTENCE (`lock.write_text("held")` `:36`, `:50`; release by `unlink` `:37`), so after D nothing blocks, the
  update is written, and `:60-61` fail. `free_lock_is_silent` expects "leaves no lock file" (`:72`), but the new invariant
  never deletes it. The spec's new test is ALSO placed in this file. The file is in D's DoD but not in its owns.
- `tests/test_project_decisions_change_request.py:328-357` (E16): makes the registry busy by `mkdir` of the OLD folder
  `.project-decisions.lock`. After E2 moves to `project-decisions.lock`, nothing is busy and the expected exit 2 becomes 0.
  The file is in neither owns nor DoD.
- `tests/test_install_paths.py:549` pins `{EXIT_LOCK: "exclusive_create", FOLDER_LOCK: "folder", ...}`, and `:102-103` and
  `:535-545` also name those paths. The file is in the DoD, not in owns.
- `tests/test_reinstall_equals_fresh.py:593-650` uses EXIT_LOCK/FOLDER_LOCK as existence locks (listed when three days old).
  The file is in neither.
- `tests/test_install_retire.py:931-965`: beyond `:947-948`, the expected actions at `:954` (`by[EXIT_LOCK]["action"]`) and
  the hashes at `:961` change once EXIT_LOCK is `os`/regenerated (a free one becomes `remove`).
- `tests/test_project_decisions_tables.py`: the new test lands there and the file is not owned.
The spec is also ambiguous about the constants. It says "keeps 10 s and the note when the wait exceeded 1 s", while the
existing test monkeypatches `LOCK_WAIT_STEPS = 20` to shorten the wait. The spec does not say whether the constants survive
as the source of `wait_s` / `poll_s`.

### B5. F1 writes pid and time into lock files that live in the project's TRACKED tree (Lead decision needed)

The Lead's F1 records the holder in the lock file's bytes. Several of the eleven sites lock files OUTSIDE the machine-local
`qa-factory/state/`:
- C1 for every task store (`<task>/state/events.lock`, `event_store.py:228`, task = `qa-factory/artifacts/<T>`);
- C3 `artifacts/<T>/state/.story-case-links.lock`;
- C7 `artifacts/<T>/work/.question-answers.lock`;
- C2 `<cases_root>/.case-versions.lock` (the project's own case library, `references/config-keys.json:318`).
`qa-factory/artifacts/**` is `carried` and is not git-ignored apart from four evidence patterns (`references/install-paths.json:17-23`,
`:44`). The test fixtures themselves carry `ARTIFACT_LOCK = "qa-factory/artifacts/QA-1/.case-versions.lock"`
(`tests/test_reinstall_equals_fresh.py:591`, `test_install_retire.py`).
Today these files are a constant 1 byte, "0". After F1, a killed holder, or a `git add` of the delivery while a holder is in its
block, leaves `{"pid":..,"since":..,"purpose":..}` in the project's git. That contradicts AR-4 (a pid is per machine; the spec's
AR-4 row claims "no host, no path" but ignores where the file lives) and P8 (a comparison run leaves no trace). It also
contradicts the table's own words "a lock is 1 byte, no session id or pid inside" (`install-paths.json:105`, t-363 B6).
Not a coding detail: it decides where F1 applies. Recommendation below (opt-in record).

### B6. F1's byte mechanics are unspecified at exactly the points a weaker builder will get wrong

The spec says "written after acquire, cut back to 1 byte at release; readers read unlocked bytes", and "open ...
`os.fdopen(.., "r+b")`". Four orders and forms decide whether the record is right and whether D2 stays fixed. None is named:
1. Release ORDER. Truncating after the unlock cuts the NEXT holder's fresh record: A unlocks, B locks and writes its record,
   then A truncates to 1. B's busy texts then say "no holder recorded".
2. Write ORDER. Writing over a longer stale record without truncating first leaves a garbage tail, so the record reads as `{}`.
   Writing without truncating first also means a failed write ("record is skipped", section 3) leaves the DEAD previous
   holder's pid in place, and the busy text then names a dead or reused pid as the holder (see N3).
3. The reader's offset. On Windows, `msvcrt.locking` is a mandatory byte-range lock. A reader that reads from byte 0
   (`read_bytes()`, `open().read()`) gets PermissionError on a held file, so `lock_holder` ("never raises") returns `{}` on
   Windows every time, while the Linux CI (advisory flock) passes. Only a read starting at offset 1 works.
4. Buffering. With a BUFFERED `r+b` stream, the D2 initial write that fails with PermissionError leaves `b"0"` in the buffer.
   The next `seek()` or the `close()` at the `with` exit flushes it again and raises PermissionError from the context exit,
   not LockBusy. That reproduces D2 one level down. Raw fd I/O (`os.lseek`/`os.write`/`os.ftruncate`, or `buffering=0`)
   has no pending buffer.

---

## Fixes to the spec text (exact replacement lines, per section)

### Section 2, Mechanics: replace the sentence "Platform switch through the existing seam `_is_windows()` (`:108-111`)." with
> Platform switch for the lock primitive on `os.name == "nt"` directly, through ONE new private seam `_lock_platform_is_windows()`
> (returns `os.name == "nt"`), never through `_is_windows()`: `_is_windows()` stays the replace-retry seam only, because
> `tests/test_event_store.py:326-341` flip it around a `commit` on Linux and must keep passing (B1). `test_both_platform_branches`
> monkeypatches `_lock_platform_is_windows` and the primitive.

### Section 2, Mechanics: replace "open with `os.open(path, O_RDWR|O_CREAT|O_BINARY?)` + `os.fdopen(.., "r+b")` (NOT `a+b` ...)" with
> open with `os.open(path, os.O_RDWR | os.O_CREAT | getattr(os, "O_BINARY", 0))` and keep the raw fd: every read, write,
> seek and truncate of the lock file goes through `os.lseek` / `os.write` / `os.read` / `os.ftruncate` on that fd (no
> buffered stream: a failed buffered write stays pending and re-raises at the next seek or close, which is D2 again).
> The fd is closed in `release()` / on the error path.

### Section 2: after the Mechanics paragraph, add a paragraph "Holder record bytes (F1), in this order"
> Acquire: after the lock call succeeds and only when `record_holder` is True: `os.ftruncate(fd, 1)` FIRST, then `os.lseek(fd,
> 1, 0)` and `os.write` of the compact JSON `{"pid", "since", "purpose"}`. A failure of either step is dropped; the lock stays
> held. Release: `os.ftruncate(fd, 1)` (dropped on error), THEN the unlock of byte 0 (dropped on error), THEN `os.close`.
> The truncate always comes BEFORE the unlock: after the unlock the next holder's record must not be cut. `lock_holder(path)`
> opens the file read-only, `os.lseek(fd, 1, 0)`, reads at most 4096 bytes, and never reads byte 0 (on Windows byte 0 of a held
> file raises PermissionError). Undecodable or non-object bytes give `{}`. The helper never probes the recorded pid for
> liveness. `os.kill(pid, 0)` is forbidden here: on Windows it TERMINATES the process.

### Section 2, API: replace the `hold_file_lock` / `take_file_lock` signatures with
> `def hold_file_lock(path, wait_s=0.0, *, purpose="", record_holder=False, poll_s=LOCK_POLL_SECONDS, clock=None, sleep=None, lock_call=None)`
> `def take_file_lock(path, wait_s=0.0, *, purpose="", record_holder=False, poll_s=LOCK_POLL_SECONDS, clock=None, sleep=None, lock_call=None) -> FileLock`
> `clock`/`sleep` None resolve to `time.monotonic`/`time.sleep` AT CALL TIME. `lock_call` None is the module's one primitive
> `os_try_lock(fd)` (the ONLY function that calls `msvcrt.locking(.., LK_NBLCK, 1)` / `fcntl.flock(.., LOCK_EX | LOCK_NB)`).
> A caller-given `lock_call(fd)` must raise OSError or ImportError exactly as `os_try_lock` does (the seam C8's tests inject).

### Section 2, API: replace the `LockBroken` docstring with
> `class LockBroken(OSError)`: the lock could not be TRIED. `.path`, `.reason` (str), `.stage` in {"open", "platform", "lock"}:
> "open" = the file or its folder cannot be opened or made; "platform" = ImportError of msvcrt/fcntl; "lock" = the lock call
> failed with an errno outside HELD_ERRNOS. `str(exc)`: '<path> cannot be locked (<reason>): nothing was done under it. This
> is not another writer: <path> must be a writable file.'

### Section 2: replace the paragraph "Callers that today read ANY failure as busy ... fail closed." with
> Every caller keeps today's exception TYPE for both outcomes (fail closed), but the WORDS follow the outcome: LockBusy gives the
> caller's busy head + the holder clause (F5), and LockBroken gives the caller's type carrying the LockBroken sentence, never the
> busy head ("another writer", "held by", "try again in a moment"). C1 exactly preserves today: LockBusy and LockBroken with
> stage "lock" become `StateConflict("task has an active state writer")`; LockBroken with stage "open" or "platform" is
> RE-RAISED unchanged (today a raw OSError from `open()`: a hook must fail loudly on an unopenable lock, never skip silently).
> C8 maps LockBusy to "held" and LockBroken to "broken" (unchanged contract). C9: `file_lock_state`.

### Section 2, ERROR DIRECTION list: append
> a reader of the holder record on Windows while the byte is held (must return the record, not `{}`): a REAL-primitive test,
> not monkeypatched, that runs on the Windows witness run and on Linux CI.

### Section 3, table rows: replace the "stale holder RECORD" behaviour cell with
> `lock_holder` returns what is recorded. The acquire truncates to byte 1 before it writes, so a failed write leaves "no holder
> recorded", never the previous holder. The busy text says "recorded holder pid N since T (a record, not checked)"; for `{}`
> it says "no holder recorded".

and add a row
> | lock file in a tracked tree (artifacts/**, cases_root) | `record_holder=False` (the default): the file stays the single byte "0" before, during and after | nothing the factory writes into a project's tracked tree carries a pid or a time (AR-4, P8; `install-paths.json:105`) |

### Section 4, Part A edges: replace "C1: `EventStore.lock` translates `LockBusy` AND `LockBroken` to `StateConflict(...)` ..." with
> C1: `EventStore.lock` calls `hold_file_lock(self.state / "events.lock", wait_s, record_holder=False)`. LockBusy and
> LockBroken(stage="lock") become `StateConflict("task has an active state writer")` chained `from` the helper's exception.
> LockBroken(stage "open"/"platform") propagates unchanged. Test (new, in test_file_lock.py):
> `test_event_store_lock_on_a_folder_raises_not_conflicts`. C6: `record_holder=True` (`state/created-accounts/`, machine-local).

### Section 4, Part A Tests: add
> - `test_holder_record_is_read_from_offset_one_while_held` (real primitive, no monkeypatch; another handle holds the lock with
>   `record_holder=True`; `lock_holder` returns the pid).
> - `test_release_truncates_before_unlock` (inject `lock_call` and an fd-op recorder; the order is ftruncate then unlock).
> - `test_failed_record_write_leaves_no_stale_holder` (a stale record present; `os.write` patched to raise; `lock_holder` gives `{}`).
> - `test_record_holder_false_leaves_one_byte` (the file is exactly b"0" while held and after release).
> - `test_broken_stages` (open: folder at path; platform: ImportError; lock: EINVAL), each `.stage` named.

### Section 4, Part B owns, the probe_by_code line: replace with
> probe_by_code.py (HELD_ERRNOS becomes `from event_store import HELD_ERRNOS`; `_os_lock` stays as the module-level SEAM
> `_os_lock = event_store.os_try_lock` adapted to take a handle or fd; `try_lock` calls
> `take_file_lock(path, 0, purpose="probe copy", record_holder=True, lock_call=lambda fd: _os_lock(fd))`, so it looks up
> the module global at call time and `tests/test_probe_by_code_copy.py:315-423` keep injecting `PBC._os_lock` unchanged;
> `_os_unlock` is removed (FileLock.release); `release_locks` calls `.release()`)

### Section 4, Part B edges: replace the C2/C3 and C7 clauses with
> C2/C3: wait 0, `record_holder=False` (tracked tree), `RuntimeError`: LockBusy gives the same head + "; no holder recorded -
> released when that process ends: wait and repeat"; LockBroken gives RuntimeError(the LockBroken sentence). C7: wait 30 s,
> `poll_s=0.02`, `record_holder=False`, `Refused`: LockBusy gives the head + holder clause; LockBroken gives
> `Refused("- " + <LockBroken sentence> + " Expected: the file must be writable")`. `claim_projector.py:647` stays untouched
> (non-goal); its fixed text on Refused is a named remainder (queue line below).

### Section 4, Part D owns: replace the owns block with
> exit_gate.py (_mutate_state and its three constants: `wait_s = LOCK_WAIT_STEPS * LOCK_STEP_S`, `poll_s = LOCK_STEP_S`, the
> note when `FileLock.waited_s >= LOCK_NOTE_AFTER * LOCK_STEP_S`; the constants stay so tests can shorten the wait)
> project_decisions.py (lock)
> references/install-paths.json (the rows of `.exit_gate_blocks.json.lock`, which becomes `lock_kind: os` AND `hook_written: true`;
> `.project-decisions.lock/**`; one new row `qa-factory/state/project-decisions.lock`)
> tests/test_exit_gate_lock_wait.py (whole: busy simulated by a held OS lock on another handle, the new test, "a free lock
> leaves the lock file and prints nothing")
> tests/test_project_decisions_change_request.py (E16 only: busy by a held OS lock on the new file)
> tests/test_project_decisions_tables.py (the new test only)
> tests/test_install_paths.py (the kinds map :549 and the paths at :102-103, :535-545 only)
> tests/test_install_retire.py (the EXIT_LOCK / FOLDER_LOCK expectations :915-965 only)
> tests/test_reinstall_equals_fresh.py (the EXIT_LOCK / FOLDER_LOCK expectations :593-650 only)

### Section 4, Part D DoD: replace with
> `python -B -m pytest ai-packages/qa-factory/scripts/tests/test_exit_gate_lock_wait.py ai-packages/qa-factory/scripts/tests/test_project_decisions_tables.py ai-packages/qa-factory/scripts/tests/test_project_decisions_change_request.py ai-packages/qa-factory/scripts/tests/test_install_paths.py ai-packages/qa-factory/scripts/tests/test_install_retire.py ai-packages/qa-factory/scripts/tests/test_reinstall_equals_fresh.py ai-packages/qa-factory/scripts/tests/test_judgment_census.py -q -p no:cacheprovider`
> (drop test_file_lock.py: D does not touch it; the builder checks `SLOW_TESTS` and leaves any slow one to CI)

### Section 4, Part D edges: append
> E1 and E2 pass `record_holder=True` (both under `qa-factory/state/`). LockBroken gives RuntimeError / TimeoutError carrying
> the LockBroken sentence, never the busy head. E1's row is `hook_written: true`: exit_gate runs inside hooks and remakes the
> file at every update (t-298 class; `onboard_apply.find_locks` then neither removes nor lists it, and the install never unlinks
> it under a live hook).

### Section 4, Part C edges: replace from "LeaseRegistry and the run loop" to the end with
> LeaseRegistry.snapshot/acquire/release: the helper's exception propagates unchanged (`execution_scheduler.main` `:666` already
> catches OSError and prints `{"status": "invalid_schedule", "error": <sentence>}`; no SchedulerError conversion). The run-loop
> site `:601` (the child is ALREADY started) catches LockBusy/LockBroken: it kills the child (`proc.kill()`, drains it), appends
> the group row `failed` with the sentence, releases the lease it acquired, and goes on with the loop (never an orphaned live
> child under a lease that names the dying coordinator's pid). estimate_record: the helper's exception reaches `main` and is
> printed by its `except OSError` as `{"status": "invalid_estimate", "error": <sentence>}`, exit 2 (stated, not left to the
> builder). Test: `test_estimate_record.py::test_held_ledger_lock_is_refused_not_hung` asserts that output.
> All C4/C5 sites: `record_holder=True` (all under `qa-factory/state/`).

### Section 6, Lead decisions, F1: append (B5, for the Lead to accept or change)
> F1 applies only where the lock file is machine-local: `record_holder` defaults to False. The callers under `qa-factory/state/`
> (C4 sites, C5, C6, C8, E1, E2) pass True. C1, C2, C3, C7 (tracked trees: task stores under artifacts/, cases_root) pass False
> and their busy text says "no holder recorded". Queue line: "holder of a tracked-tree lock: a machine-local sidecar keyed by
> the lock path, if the busy text there is found wanting".

### Section 7, Analogs noticed: append
> `onboard_apply._os_holder` (`:267-275`) answers "unknown" for every held os lock outside the writer folders: same D4 class,
> wire `lock_holder` there later (queue line). `onboard_apply._remove_stale_lock` (`:1330-1340`) unlinks a lock file it probed
> free, the one deliberate exception to "a lock file is never deleted" (install time; a writer that locks between the probe and
> the unlink holds an orphaned inode on POSIX). Named, not changed here. `claim_projector.py:647-649` replaces C7's text with
> its own, so the holder clause never reaches the driver (queue line).

---

## Non-blocking findings (should be fixed or consciously accepted)

- **N1 stand_lease fails OPEN on CONTENTION.** Part C maps LockBusy to "unprotected" + `lease_error` (`stand_lease.py:277-281`).
  The policy docstring covers a BROKEN lease file (`:266-267`, "A broken lease FILE never stops a run"), not a live holder.
  Under parallel walk chains, a holder hung past 10 s lets a second run go on without the stand lease, the incident the module
  exists for. Today this already happens on Windows (raw OSError after ~10 s); on POSIX it is new (today it waits forever).
  Recommendation (Lead decides): LockBusy is one "busy" try inside `hold`'s own loop (`poll_s`, until `limit`; then StandBusy
  with the lock sentence), and only LockBroken is "unprotected". If the Lead keeps the spec, record it as a decision with that reason.
- **N2** (folded into the Part C replacement above): the run-loop site `:601` raised after `Popen`, which orphaned the child.
  Same as Windows today; new on POSIX.
- **N3 Busy door wording.** "It is released when that process ends: wait for it, or stop it". The recorded pid is advice
  (FR-41): it can be stale (an old-generation holder writes none; a write failed), or from another pid namespace (a container
  sharing the volume). "Stop it" tells a role to kill a pid it cannot verify. Recommended door: "wait and repeat; if it stays
  held, the conductor checks the recorded process (pid N at T, a record, not checked)". FR-2: a door the refused party can use.
- **N4** `file_lock_state` should open the file read-only (`O_RDONLY`). Both `LockFile` and `flock` work on a read handle, so
  a read-only lock file reads free/held, not "unknown". It must never pass `O_CREAT` (K-STALE `test_install_retire.py:1154`
  pins that a 0-byte lock stays 0 bytes).
- **N5** Spec 0.7 D2 lists C8, but C8 already writes inside its try and maps the EACCES write failure to "held"
  (`probe_by_code.py:2656-2666`), so it is not a D2 instance. C2/C3 write OUTSIDE their try (`case_versions.py:41-43`,
  `:199-200`), so those are. An accuracy fix only.
- **N6** `FileLock.release()` may be called from another thread under S5 chains (C8 holds the lock across calls). Both
  primitives allow it (the lock belongs to the handle, not the thread), but a double release from two threads must not
  double-close the fd: swap the fd out atomically (`fd, self._fd = self._fd, None` under a `threading.Lock`) before the closing ops.
- **N7** Part A is at the ~3 h edge for Sonnet (helper, ~24 named tests with my additions, C1, C6). Acceptable. If it stalls, C6
  moves to B, and TR4-9 then waits for A+B on manual_capture.

---

## Answers to the six questions

### Q1. Facts by trail
Spot-checked end to end (code read):
- **C1** `event_store.py:299-338`: one non-blocking try polled at 0.05 until the monotonic deadline, then
  `StateConflict("task has an active state writer")` (`:329`), the same on both platforms. The initial write is outside the
  loop (`:314-317`). The switch is on `os.name`, not on `_is_windows`.
- **C4** `execution_scheduler.py:83-105`: `LK_LOCK` / bare `LOCK_EX`. On POSIX it blocks forever. On Windows the CRT gives
  ~10 one-second retries and then raises (CRT documentation, not run here). The unlock in `finally` runs although the lock call
  sits INSIDE the same try (`:91-105`), so an unlock without a lock is confirmed. Callers: `:127/:131/:156/:601`,
  `environment_preparation.py:20,:265`, `stand_lease.py:135-139`, `stand_health.py:357,:379,:847`. All hold short RMW sections
  (read JSON, atomic_json): read.
- **C5** `estimate_record.py:89-128`: blocking; the lock is taken OUTSIDE the try, so no unlock without a lock there. `main`
  catches OSError and prints `invalid_estimate` (`:139-143`).
- **C6** `manual_capture.py:795-830`: wait 20 s, poll 0.05, TimeoutError text as stated; constants at `:720-721`.
- **C7** `question_register.py:765-803`: 30 s, poll 0.02, the `Refused` text as stated.
- **C8** `probe_by_code.py:2587-2677`: the errno split as stated.
- **E1** `exit_gate.py:316-355` and **E2** `project_decisions.py:192-204`: as stated.
- **C2/C3/C9**: as stated.
The table is accurate (one accuracy slip, N5).
Negative claims, each re-run with a same-form positive control:
- `grep -rlic "msvcrt\|fcntl"` over the whole package gives 10 files (8 scripts + `tests/test_install_retire.py` +
  `tests/test_probe_by_code_copy.py`), as stated. Positive control in the same form: `case_versions.py` counts 12. No hit in
  hooks/ or skills/.
- `stand_lease.py` and `stand_identity.py`: 0 hits for `msvcrt|fcntl|O_EXCL|locking(` (case-insensitive). Their `_locked`
  calls C4 (`stand_lease.py:135-139`) and `EventStore.lock` (`stand_identity.py:348-358`). Confirmed: no copy.
- `driver_timing.py`: `lock|O_EXCL|msvcrt|fcntl` (case-insensitive) hits only `clock`/`block` words at `:36-106`; the same
  lines are the positive control. Confirmed: no lock.
- O_EXCL sites (non-test): environment_preparation, execution_request, exit_gate, exploration, local_keys, window_files, as
  stated. The only mkdir-as-lock is `project_decisions.py:197`, as stated.

### Q2. D1-D4 real? Missed?
D1: real (C4 unlock-not-taken; POSIX infinite). D2: real for C1, C2, C3, C5, C6, C7 (write before the loop or outside the try);
not for C8 (N5). D3: real (E1 file and E2 folder survive a killed hook; every later call waits 10 s and fails). D4: real.
Missed or under-specified:
- (a) re-entrancy inside one process: correct as specified. `flock` on a second `open()` is a separate open file description,
  and `LockFile` is per handle; both conflict within one process, which preserves `test_identity_proof_contract.py:71-73` and
  `test_probe_by_code_copy.py:320`.
- (b) taken in one thread, released in another: allowed by both primitives. Double release needs a guard (N6).
- (c) lock files in a project's tracked tree: MISSED. That is B5.
- (d) a missing directory: handled (mkdir parents), correct.
Further misses:
- (e) the platform seam vs the tests (B1).
- (f) buffered I/O re-raising D2 at close (B6.4).
- (g) the Windows mandatory range makes a byte-0 reader fail (B6.3).
- (h) `onboard_apply._remove_stale_lock` deletes lock files, contrary to the helper's invariant (named in the section 7 fix).
- (i) the E1 row needs `hook_written` once it becomes an os lock (Part D fix).

### Q3. LockBusy / LockBroken outside the census pattern
Legitimate, not an evasion. The census (`tests/test_judgment_census.py:58` UNIT_NAME_RE; `refusal_registry.py:58`
REFUSAL_RAISES = StateConflict/ValueError) measures where JUDGMENT of role output lives (AR-29). A lock outcome is a fact about
an OS primitive, with no content and no role output. Its owner is data, and naming it a unit would only inflate the shape count.
`event_store.lock` keeps its unit row because it still raises StateConflict. No ceiling moves (AR-20).
Who catches what, and what is read:
- C1: the lifecycle CLIs and hooks read StateConflict exactly as today.
- C2/C3: RuntimeError reaches case_versions' CLI.
- C6: TimeoutError reaches the walker ("Repeat the step").
- C7: Refused reaches question_register's CLI; claim_projector substitutes its own line.
- C8: held/broken words go to the probe's fallback logic.
- C4/C5: invalid_schedule / invalid_estimate JSON, `lease_error`, swallowed in stand_health.
- E1: the hook's RuntimeError. E2: project_decisions main's one line (E16 text).
The defect is the BROKEN outcome reusing the busy words at C1 (open stage), C2, C3, C6, C7 (B2): FR-1 (says what is wrong) and
FR-46 (whose fault) fail there. With the B2 fix every reader gets a true sentence and a usable door.

### Q4. F1 with msvcrt byte 0 / flock; stale holder; pid; 10 s
- Works with `msvcrt.locking` of byte 0 ONLY IF readers start at offset 1 (Windows mandatory range) and the holder writes
  through its own fd. Works with `flock` on every site (advisory, the whole file). The order and form rules are B6.
- Stale holder of a dead process: the OS frees the byte, and the next acquirer truncates and overwrites (with the B6 order). A
  waiter only reads the record when the lock is BUSY, so the current holder is alive. The record can still be stale: an
  old-generation or foreign holder (the test simulators `test_install_retire.py:160-208`), or a failed record write. Hence
  "recorded, not checked" and the door wording (N3).
- A pid is not enough across containers or pid namespaces. Keep it as advice only, never as a kill target, and never call
  `os.kill(pid, 0)`.
- 10 s (F3/F4) applies to C4, C5, E1, E2 only. Every protected section is a short RMW (read):
  - `LeaseRegistry` (`:126-166`, `:601-606`);
  - `stand_lease._try_acquire/_release/status/release_by_person` (`:201-338`): the liveness checks are ctypes or /proc reads,
    milliseconds;
  - `stand_health` `:357-365`, `:379-386`, `:849-853`: the judge call is deliberately OUTSIDE the lock (`:388-390`);
  - `environment_preparation._claim_locked` (`:268-305`): a glob of job JSONs;
  - `estimate_record` `:101-128`;
  - `exit_gate._mutate_state`: an `update` callback on a dict;
  - `project_decisions` `:304/:387/:432`: read, parse and write of one md table.
  No caller legitimately holds these past 10 s. The long holders in the package (`dashboard_refresh.py:59`, which renders the
  dashboard up to 3x under `.dashboard-writer`; cost_capture's session lock) are C1 callers whose waiters keep their own wait
  (0, which means skip). F4 does not touch them. One slow-run hazard: the run loop `:601` turning a lock wait into an orphaned
  child (fixed in the Part C replacement).

### Q5. Pinned texts
- C1 exact: `test_event_store.py:153`, `test_post_commit_refresh.py:718`, `test_story_step_finish.py:654` (whole text), plus
  the substrings `test_manifest_projection.py:423` and `test_event_store.py:522`. All stay, since C1's text is unchanged.
- C2/C3: the regex "active writer" at `test_identity_proof_contract.py:72`. Appending a clause is safe.
- C6: the substring "held by another walker for over 0.2 s" at `test_fill_new_account.py:397`. Safe.
- C7: the substring "another writer" at `test_question_register.py:1137`. Safe for LockBusy; under B2 a LockBroken text must
  NOT contain it, which no test pins.
- E1: the substrings "remained busy" and ".lock" at `test_exit_gate_lock_wait.py:60`, plus "exit gate state lock was busy" at
  `:43`. Safe if kept.
- E2: E16 checks ONE line containing "the registry is busy" and "run the same command again"
  (`test_project_decisions_change_request.py:350-353`). That text comes from project_decisions main, not from the lock. The
  holder clause must not add a newline. Its busy simulation breaks (B4).
- No test compares C2/C3/C6/C7/E1/E2 texts whole.

### Q6. Split, order, in-flight work
- File-disjoint:
  - A: event_store.py, manual_capture.py `_locked`, test_file_lock.py, changelog.
  - B: case_versions, question_register, probe_by_code, onboard_apply `_lock_state`.
  - C: execution_scheduler, environment_preparation, stand_lease, stand_health, estimate_record.
  - D: exit_gate, project_decisions, install-paths.json, and the tests named in the B4 fix.
- The only shared file is `test_file_lock.py` (`REMAINING_COPY_FILES`), between B and C, with line-local deletions; D does not
  touch it (drop it from D's DoD).
- `onboard_apply.py`: B owns `_lock_state`; D's non-goal keeps it untouched. Disjoint. `install-paths.json` is owned by D only.
- In flight:
  - probe_by_code: N4/N5 on other functions. The Lead already orders B's probe group after them. Splitting B into B1 (C2, C3,
    C7, C9) now and B2 (C8) after N4/N5 avoids holding the whole of B.
  - manual_capture: A, then TR4-9, per the batch order line `batch-4-ostatki.md:8`.
  - story_run.py (TR3-9): no part touches it (0.5).
  - stand_lease.py: C only, as the order line says.
- Size: A is at the edge (N7). B, C and D are each under ~3 h once their owns are complete.

---

## DUPLICATION AND CONSISTENCY
The spec removes nine copies and two existence mutexes. The remaining duplication it names and leaves:
- `stand_identity._locked`'s retry loop around `EventStore.lock()` (`stand_identity.py:354-363`);
- the ten generic `EventStore(dir).lock()` sites;
- the cost_capture owner sidecar (F2).
Each has a queue line. Missing from the queue: onboard_apply `_os_holder` (a second holder reader, which AR-13 makes the
helper's job) and claim_projector's substitute text; both are added by the section 7 fix. The ratchet test with positive and
negative controls is the right deterministic layer. Grepped: `msvcrt|fcntl`, `O_EXCL`, `lock[a-z_]*.mkdir()`, every lock
function name over `scripts/` (results above).

## CODE QUALITY
Plan-level only:
- the raw-fd rule (B6.4);
- call-time defaults for clock/sleep (the API fix);
- a guarded idempotent release (N6);
- one primitive function `os_try_lock` as the single ratchet target (the API fix).
None found beyond those: the API surface (two context forms, a state probe, a holder reader) is minimal for the eleven sites.

## ARCHITECTURE (question 10)
- AR-15, AR-13, AR-14: kept, with the B3 seam and the `_os_holder` queue line.
- AR-4: broken by F1 as written in tracked trees; fixed by B5.
- AR-28: broken by B2 at C1 (a silent skip); fixed by B2.
- AR-25: kept (D3).
- AR-9: kept with the N3 door wording.

## JUDGMENT (question 11)
No role judgment is moved into code or out of it. Every lock refusal is data-owned. No census row changes; that is correct (Q3).

## "Written for a weaker model"
Before the fixes the spec failed this rule at:
- B3 (an impossible "unchanged" promise);
- B4 (owns that cannot hold the required edits);
- B6 (the order and offset rules left to inference);
- Part C ("the builder reads the CLI handler and reports"): the spec now states the output.

## Reading trail
- Spec t-2148 (whole).
- The finding (whole).
- `batch-4-ostatki.md:1-12`, rows TR4-2 and TR4-9.
- `event_store.py:80-200`, `:290-345`.
- `case_versions.py:30-65`, `:190-222`.
- `execution_scheduler.py:30-165`, `:540-670`.
- `estimate_record.py:85-145`.
- `manual_capture.py:715-725`, `:790-870`.
- `question_register.py:60-75`, `:760-815`.
- `probe_by_code.py:2580-2690`.
- `onboard_apply.py:130-195`, `:267-340`, `:1238-1262`, `:1320-1340`.
- `stand_lease.py:93-145`, `:190-340`.
- `stand_health.py:345-400`, `:835-865`.
- `environment_preparation.py:15-22`, `:255-305`.
- `exit_gate.py:305-362`.
- `project_decisions.py:185-230`, `:300-312`, `:384-392`, `:428-440`.
- `log_append.py:155-180`, `dashboard_refresh.py:52-70`, `cost_capture.py:2818-2834`, `claim_projector.py:638-652`.
- `run_suite.py:395-442`.
- `refusal_registry.py:50-62`, `tests/test_judgment_census.py:30-120`.
- `references/install-paths.json:1-40`, `:86-112`.
- Tests:
  - `test_event_store.py:95-160`, `:225-345`;
  - `test_install_retire.py:160-210`, `:1135-1160`;
  - `test_exit_gate_lock_wait.py` (whole);
  - `test_project_decisions_change_request.py:328-357`;
  - `test_install_paths.py:545-552`;
  - `test_reinstall_equals_fresh.py:590-600`;
  - `test_question_register.py:1125-1143`;
  - `test_probe_by_code_copy.py:310-345`;
  - `test_stage_done_lock_order.py:165-200`;
  - `test_config_view.py:275-290`.
Greps (case-insensitive where content-negative, each with a positive control):
- `msvcrt|fcntl` package-wide (control: case_versions 12);
- the same over stand_lease/stand_identity, and `lock|O_EXCL|msvcrt|fcntl` over driver_timing (control: the clock lines);
- `O_EXCL` and mkdir-locks;
- every lock function name over `scripts/` (callers and tests);
- `_is_windows` over tests (3 files) and `event_store.time` patches;
- the pinned refusal texts over tests/skills/agents/hooks/references;
- `lock_kind|exclusive_create`;
- `invalid_estimate|invalid_schedule`;
- `artifacts` rows of install-paths.
Nothing was run beyond reads and greps (plan review; DoD: "run nothing heavy").

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1: the helper switches platform through _is_windows(); tests/test_event_store.py:326-341 commit under a patched _is_windows=True, so on the Linux CI image import msvcrt fails, giving LockBroken and then StateConflict, and Part A's DoD goes red on CI only",
    "B2: LockBroken folded into the busy refusals: an unopenable events.lock becomes a silent StateConflict skip in every hook (today a loud OSError), and C2/C3/C6/C7 tell a broken primitive 'another writer held it, try again' (FR-1, FR-46, AR-28)",
    "B3: Part B removes PBC._os_lock while test_probe_by_code_copy.py:315-423 inject PBC._os_lock and are promised to stay unchanged; the injections become dead and the held/broken checks fail",
    "B4: Part D owns miss test_exit_gate_lock_wait.py (existence-based busy, pinned constants, 'no lock file left'), test_project_decisions_change_request.py E16 (busy via the old folder), test_install_paths.py:549, test_reinstall_equals_fresh.py:593-650, test_install_retire.py:954-961, test_project_decisions_tables.py",
    "B5: F1 writes pid and time into lock files in the project's tracked tree (artifacts/<T>/state/events.lock, .story-case-links.lock, work/.question-answers.lock, cases_root/.case-versions.lock); a crash or a git add while held commits machine data (AR-4, P8, install-paths.json:105); Lead decision: opt-in record_holder",
    "B6: F1 byte mechanics unspecified: truncate must come before unlock at release and before write at acquire; lock_holder must read from offset 1 (on Windows byte 0 of a held file raises); the fd must be raw, since a buffered failed D2 write re-raises at close"
  ],
  "fixes": [
    "Section 2 Mechanics: primitive switch on os.name through a new seam _lock_platform_is_windows(), never _is_windows()",
    "Section 2 Mechanics: raw fd I/O (os.open/lseek/write/read/ftruncate), no buffered stream",
    "Section 2: holder-record paragraph with the acquire and release order, the offset-1 reader, no liveness probe, os.kill(pid,0) forbidden",
    "Section 2 API: record_holder=False, clock/sleep None resolved at call time, lock_call seam, one primitive os_try_lock",
    "Section 2: LockBroken.stage open/platform/lock and its own sentence; callers keep the type but never the busy words; C1 re-raises open/platform unchanged",
    "Section 3: stale-record cell rewritten; new row for locks in a tracked tree",
    "Part A edges and tests: record_holder per site, five new tests (offset-1 read, release order, failed write, one byte, broken stages)",
    "Part B owns: probe_by_code keeps the _os_lock seam via lock_call; C2/C3/C7 edges with the LockBroken words; optional split of B into B1 now and B2 after N4/N5",
    "Part C edges: no SchedulerError conversion; the run loop at :601 kills the child and records it failed; estimate output stated",
    "Part D owns and DoD: the six test files with line scopes; constants kept as the wait source; E1 row hook_written true; record_holder true",
    "Section 6 F1: opt-in record for machine-local locks only (for Lead acceptance)",
    "Section 7: queue lines for onboard_apply._os_holder, claim_projector's text, and the _remove_stale_lock exception named"
  ],
  "class_completeness": "Surface: the OS file lock and its callers' error direction. Walked: all 11 sites, the 10 generic EventStore.lock callers (0.4, out by the spec with a queue line), the O_EXCL claims (0.3, out, correctly), the platform seam in tests, the lock files in tracked vs machine-local trees, and the readers of lock-holder data (onboard_apply._os_holder, a second reader, now queued) and of lock-file bytes (onboard_apply._summary, unaffected). Left uncovered before the fixes: claim_projector's substituted text and onboard_apply's holder reader (now queue lines); the E1 hook_written row (now in Part D).",
  "trail": {
    "read": [
      "docs/tasks/specs/t-2148-tr4-2-one-file-lock.md",
      "plans/piles/thinking-roles/findings/20261106-kopii-zamka-fajla-v-pakete.md",
      "plans/piles/thinking-roles/batch-4-ostatki.md:1-30",
      "ai-packages/qa-factory/scripts/event_store.py:80-345",
      "ai-packages/qa-factory/scripts/case_versions.py:30-222",
      "ai-packages/qa-factory/scripts/execution_scheduler.py:30-670",
      "ai-packages/qa-factory/scripts/estimate_record.py:85-145",
      "ai-packages/qa-factory/scripts/manual_capture.py:715-870",
      "ai-packages/qa-factory/scripts/question_register.py:60-815",
      "ai-packages/qa-factory/scripts/probe_by_code.py:2580-2690",
      "ai-packages/qa-factory/scripts/onboard_apply.py:130-340,1238-1340",
      "ai-packages/qa-factory/scripts/stand_lease.py:93-340",
      "ai-packages/qa-factory/scripts/stand_health.py:345-865",
      "ai-packages/qa-factory/scripts/environment_preparation.py:15-305",
      "ai-packages/qa-factory/scripts/exit_gate.py:305-362",
      "ai-packages/qa-factory/scripts/project_decisions.py:185-440",
      "ai-packages/qa-factory/scripts/claim_projector.py:638-652",
      "ai-packages/qa-factory/scripts/refusal_registry.py:50-62",
      "ai-packages/qa-factory/scripts/tests/test_judgment_census.py:30-120",
      "ai-packages/qa-factory/references/install-paths.json:1-112",
      "ai-packages/qa-factory/scripts/tests/test_event_store.py:95-345",
      "ai-packages/qa-factory/scripts/tests/test_exit_gate_lock_wait.py",
      "ai-packages/qa-factory/scripts/tests/test_probe_by_code_copy.py:310-345",
      "ai-packages/qa-factory/scripts/tests/test_project_decisions_change_request.py:328-357",
      "ai-packages/qa-factory/scripts/tests/test_install_retire.py:160-210,915-965,1135-1160",
      "ai-packages/qa-factory/scripts/tests/test_install_paths.py:545-552",
      "ai-packages/qa-factory/scripts/tests/test_reinstall_equals_fresh.py:590-650",
      "ai-packages/qa-factory/scripts/tests/test_question_register.py:1125-1143",
      "ai-packages/qa-factory/scripts/tests/test_stage_done_lock_order.py:165-200"
    ],
    "reruns": [
      {"command": "grep -rlic msvcrt|fcntl ai-packages/qa-factory", "result": "10 files as stated (8 scripts + 2 tests); positive control case_versions.py 12 hits"},
      {"command": "grep -ic msvcrt|fcntl|O_EXCL|locking( stand_lease.py stand_identity.py", "result": "0 and 0"},
      {"command": "grep -in lock|O_EXCL|msvcrt|fcntl driver_timing.py", "result": "only clock/block words at 36-106, which are the same-form control"},
      {"command": "grep O_EXCL and lock-folder mkdir over scripts minus tests", "result": "as in spec 0.2/0.3"},
      {"command": "grep _is_windows over scripts/tests", "result": "3 files; test_event_store.py:326-341 commit under the patch"},
      {"command": "grep the pinned refusal texts over tests, skills, agents, hooks, references", "result": "as listed in Q5"},
      {"command": "no test or script run", "result": "plan review, reads and greps only"}
    ]
  }
}
```

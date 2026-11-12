# t-203 — native context on a long project root (OH3-36 + OH5-10, OH5-11, OH5-13 F3)

Draft by designer (Opus) for the Lead, 12.11.2026; fix round t-215 (12.11.2026) on the critic verdict
`docs/tasks/specs/reviews/t-212-t-203-plan-review.md` (GO-WITH-FIXES, E1-E9). Status: DRAFT, waits for Lead acceptance.
Coordinator decisions F-1, F-4, F-7, F-9, Q-2, Q-3 and the t-216 result (supported root 119) are written in «по
рекомендации, до слова владельца»; nothing is left open in §6 beyond the owner's two F-1 questions and F-2/F-5/F-6.
Nodes: onboarding-forge/1 OH3-36; onboarding-hooks/5 OH5-10, OH5-11, OH5-13 (part F3 only).
Base read: worktree `C:\QAFactory\forge-repo\.claude\worktrees\int-of1` (code), `...\oh5-7` (pile files of batch 5);
fix round t-215 re-read on `main` (`ai-packages/qa-factory/scripts/`), which carries the same lines the critic cites.

## 0. Facts that change the brief (read on disk, not from the brief)

1. **The rename the finding asks for is already done.** `native_context.py` names a packet
   `<32 hex sha256(session)>-<32 hex sha256(task_name)>.json` (`NAME_HEX = 32` `:9`, t-417) and carries
   `PACKET_ROOT_LIMIT = 119` (`:13`); `test_doctor_context.PacketNameLength` pins it. The 56-character root of the finding
   now writes (`test_the_old_failing_path_of_260_now_writes`). What is still open: (a) a root over 119 on a Windows machine
   without long paths still fails the write, and (b) that failure still passes silently.
2. **The silent pass, exactly.** `inject_context` (`main`'s Codex branch, `:645-656` on main) catches only `ValueError`
   around `native_context.stage`. A failed write raises `OSError` (`FileNotFoundError` on a 260-character path), which
   escapes to `main`'s generic handler (`:478-487`): one `person_signal` (`hook_signal` line), exit 0, the native launch
   goes ahead with no context. `StateConflict` is a `ValueError` (`event_store.py:19`), so the existing native refusals
   already exit 2.
3. **`atomic_json` is not in `hooklib.py`.** The writer is `event_store.atomic_json` -> `_publish` (`event_store.py:135-174`),
   temp name `<name>.<uuid4 hex, 32>.tmp`. `hooklib.py` has no `atomic_json` (Grep `atomic_json|uuid` on `hooklib.py`:
   no match; positive control: the same Grep finds `def artifacts_dir` at `:239`). OH3-36's owns line
   ("`scripts/hooklib.py` (`atomic_json`)") is a defect of the node; this spec does not touch `hooklib.py` for OH3-36.
4. **Refusal scanner scope.** `refusal_registry.SCANNED = ("stage_guard.py", "inject_context.py", "guard_pre_tool.py")`
   (`:56`); it sees `deny(...)`, `block(...)` and raised `StateConflict`/`ValueError`. A refusal raised inside
   `native_context.py` is invisible to A24. The three existing native refusals (size, identities, `StateConflict`) have no
   A24 row (F-6). This spec puts the NEW refusal in `inject_context.py` through `block(...)`, so A24 sees it.
5. **`pending_path` callers:** only tests (`test_doctor_context.py` 7 sites, `test_codex_host.py` 7, `test_scout_reliability.py` 2,
   the last quarantined). B-394 is right.
6. **The copy B-394 names** is `worker_lifecycle.binding_is_active` `:93-95` (`task in (".", "..") or any(c in task for c in "/\\:")`),
   the negation of `hooklib.is_one_component` (`:233-236`). The same file calls `artifacts_dir(task, event)` without its
   `root` at THREE sites although each has `root`: `_blocking_text` (`:119`), `note_unlaunched_denial` (`:160`) and
   `guard`'s stop branch (`:214`, on a receipt read by `receipt_files(root)`) — the third found by the critic (t-212 F5),
   confirmed by reading `worker_lifecycle.py:205-217`.
7. **Test layers.** Keep rows: `test_doctor_context.py` (covers `inject_context.py`, `native_context.py`, `hooklib.py`),
   `test_codex_host.py` (covers `native_context.py`, `hooklib.py`; NOT `inject_context.py`), `test_resolver.py` (table,
   `test-layers.json:4319`, covers `hooklib.py`, `inject_context.py`, `runtime_paths.py` and others, NOT
   `worker_lifecycle.py`), `test_words_doors.py` (`:6866`, "sole AR-24 detector"; the only keep row covering
   `worker_lifecycle.py`). Quarantined: `test_worker_lifecycle.py`, `test_worker_lifecycle_active.py`, `test_denial_scope.py`,
   `test_host_launch_denial.py`, `test_lifecycle_integration.py`, `test_scout_reliability.py`, `test_story_root_class.py`.
8. **Owners' standing word in the code.** `inject_context.main` docstring (`:458-463`): injection fails open (F-11), "Residual,
   by the owner's word (F-9/F-11): a crash AFTER the receipt was read allows the dispatch and leaves its signal". The native
   packet write happens after the receipt read. Turning its failure into a refusal narrows that residual: F-1.
9. **(t-212 F1, re-read.) The binding receipt in `deliver` has the same limit as the named packet.** `native_context.deliver`
   (`:145-150`) calls `host_dispatch.record(...)` BEFORE it rewrites the packet (`:153`) and before `context_output` (`:154`).
   `record` writes `host_dispatch.binding_path(root, agent)` = `<root>\qa-factory\state\host-dispatches\<64 hex>.json`
   (`host_dispatch.py:10-11`) through `atomic_json` (a new receipt after `:302`; a rebind at `:282`). Neither `deliver` nor
   `native_context.main` (`:157-161`) catches anything, and `telemetry_hook` re-raises the target's exception
   (`telemetry_hook.py:163-177`): the SubagentStart hook ends in an exception, the context is never output, the child starts
   without its rules, the packet stays `pending`. The same holds for the packet rewrite at `:153` (F-9). Lengths (critic's
   measurement with the real `_slot`/`binding_path`, string roots, + 37 for the temp name): root 119 -> named packet 259,
   binding 259; root 120 -> 260 / 260; root 152 -> unnamed packet 259. Arithmetic: binding = root + 34
   (`\qa-factory\state\host-dispatches\`) + 64 + 5 + 37 = root + 140, the same as the named packet (root + 33 + 32 + 1 + 32
   + 5 + 37). Consequence: shortening the packet name alone (the first draft's D1, `NAME_HEX` 16) only moves the failure
   into `deliver`; it is dropped. Unnamed launches (packet limit 152) already stage at 120..152 today and then crash in
   `deliver` the same way.
10. **(t-216, scout, reported by the coordinator; not re-measured by the designer.)** The factory's supported root is
   **119 characters** against a limit of 259 usable characters (basis: `native_context.py:10-13`, decided by the
   coordinator). The two bounded-suffix writers with the longest tail both take 140 characters after the root: the
   `host_dispatch` binding (`host_dispatch.py:11`) and the named `native_context` packet. The sibling
   `host_capabilities.record` allows a root of 121. Writers whose length depends on uncapped variables (story key, the
   case-id stem in `probe_by_code.write_receipt`, the session id in `cost_capture`, `baseline_contract`'s pid temp name)
   have no fixed limit and go to a separate finding (Part A non-goals).

## 1. Architecture, owners, census (designer rule 1, AR-29)

AR-n touched, with the change check each demands (written into the DoD of the part named):

| AR | how touched | change check (in DoD) |
|---|---|---|
| AR-9 | new refusal `IC-native-packet-unwritten` with a door and a pass | A24 row in the same commit; `refusal_registry.py --check` exit 0; a test opens the door (A7) and a test takes the pass (A5b). `design/controller-blocks.md` carries no `IC-` rows (Grep `IC-oversized-slice`: only `refusal_registry.py` and `judgment-census.json`), so nothing to regenerate |
| AR-28 | a failed packet write no longer becomes a pass at the dispatch boundary; a failed binding write or packet rewrite no longer drops the context | rows A6 (refusal, exit 2), A8 and A8b (`deliver` still outputs the context) |
| AR-24 | a person's recorded word (`stage_overrides[]` through `waiver.py`) reaches the new refusal through the existing reader `waiver.split_overridden` (no second road, P31) | row A5b: a live override passes, a revoked one refuses, the pass is journaled `gate_override` |
| AR-29 | one new blocking check unit, one new non-blocking helper | census rows below; `test_judgment_census.py` green; raised `blocking_per_role` counts named (AR-20) |
| AR-20 | `blocking_per_role` ratchet in `judgment-census.json` rises by one per role of the new unit | the verdict and the commit list every raised key old -> new with the reason "silent pass made a refusal (t-203)" |
| AR-25 / AR-17 | the refused launch leaves a `dispatch-denials.jsonl` row, so `recover` closes the dispatch `never_started`; a passed launch leaves none | rows A6 (denial row present) and A5b (no denial row on a pass) |
| AR-22 | new `hook_signal` lines of kind `inject` from `deliver` (F-7, F-9, F-4) have their reader: `report_facts._hook_signals`, the only reader (Q-2, decided) | rows A8, A8b, A9 read the journal line |
| AR-1 | `PATH_LIMITS = {"nt": 259}`: a platform fact read by the capability key `os.name`, default "no limit" | no language/project name is read; not project variety, so it stays a module data row (closed choice C-3); FR walk C says so |
| AR-15 / AR-13 | Part B: `worker_lifecycle` calls the survivor `hooklib.artifacts_dir` instead of its copy, at all three sites | row B4 (spy); the eight other copies are queued to a new onboarding-hooks node (Part B, "Copies") |
| AR-12 | the Agent hook on Codex changes for every role | report "code_friction: not measured" as an open item (no live run here) |
| AR-4 | refusal text names the machine's limit, writes nothing machine-tied | n/a beyond the text |

Checks the spec adds or alters, owner served, census class:

| unit | what it judges | class | owner | blocks |
|---|---|---|---|---|
| `inject_context.refuse_native_packet` (new) | PRESENCE of the written packet (the write raised `OSError`), and PRESENCE of a person's recorded word that names the line (read through `waiver.split_overridden`, never judged) | shape | data (code); the pass serves intent (the person, through the existing `waiver.py` road) | yes, every role it dispatches + conductor: copy the `roles` list of the `collect_blocks` row; `ref: "A24:IC-native-packet-unwritten"` |
| `native_context.unwritten_facts` (new) | picks which cause text applies (length arithmetic, error type); decides nothing about passing | shape | data (code) | no; a census row only if `test_judgment_census.py` reports it as a unit |
| `native_context.deliver` write guards (new, F-7 and F-9) | catch a failed binding write or packet rewrite and still output the context; report lines, not checks | — | data | no |
| `native_context.deliver` ambiguity signal (F-4) | a report line beside the existing stderr line, not a check | — | — | no |
| `hooklib.artifacts_dir` (altered: `root` parameter) | one-component ticket, unchanged | shape (existing row `:398`) | data | unchanged |
| `worker_lifecycle.binding_is_active` (altered: calls the survivor) | not a census unit; error direction unchanged: any doubt -> active (`True`) | — | data | — |

Reused functions in a more consequential role:
- `event_store.atomic_json`'s success becomes the GATE of a native launch (before: its failure was a signal). Allowed
  error direction: toward refusing (a false refusal, e.g. a sharing violation outliving the 8 retries), never toward a
  silent pass. Adversarial inputs that must stay on the refusing side: a 120-character root on a Windows machine without
  long paths (named launch); a 153-character root (unnamed); a directory sitting at the packet's path; a read-only folder;
  a lock file that cannot be opened (`LockBroken`, an `OSError`); a disk-full `OSError`; an existing packet that cannot be
  READ by `read_text` (`OSError`, newly refused) or parsed (`ValueError`, refused as before).
- `waiver.split_overridden` becomes the pass of this refusal (before: stage_guard's dispatch errors only). Its own error
  direction is toward blocking (docstring `waiver.py:206`). Inputs that must stay REFUSED: a revoked override; an override
  whose `match` holds a `<placeholder>`; an override recorded for another stage; a `match` that names only part of a word
  of the line (`names_whole`); no `pipeline.json`; a ticketless launch; a running dispatch with no `stage`. Input that
  PASSES by design (one road with every other dispatch block): a live `*` override on the same stage.

## 2. Decisions, with reasons

**D1 — Refuse; keep the name and the limit (t-212 E1).** `NAME_HEX` stays 32, `PACKET_ROOT_LIMIT` stays 119. Reason:
the binding receipt (`host_dispatch.binding_path`, 64 hex) crosses 259 at the same root (fact 9), so a shorter packet name
only moves the failure into `deliver`. The class-wide way to gain length is F-2 (the shared temp suffix, +24 for every
writer, packet and binding alike), not one file's name.
- Refuse: no length pre-check. A machine with Windows long paths turned on writes a 300-character path; a pre-check would
  refuse it for nothing. The refusal fires when `stage` raises `OSError`, and the length arithmetic only chooses which
  cause and door the text names.
- What is not shortened, and why: the packet name (above); the folder name (`native-context`) — renaming it strands
  in-flight packets and every reader of the folder; the temp suffix of `event_store._publish` — shared by every writer of
  the package: F-2.

**D2 — The refusal goes to whoever issued the native spawn** (the orchestrator session, or the driver's Codex session),
on stderr through `hooklib.block` (exit 2), plus a `note_denial` line so `recover` can close a receipt-backed dispatch as
`never_started`. It is a machine channel (`references/human-questions.md` :9-11: "the refusal a script prints to a role"
is not governed by that file); the person hears it from the conductor/orchestrator, who owns the closed question with
prices (P22, AR-16). No `person_signal` beside the refusal: it is not silent (C-4). FR-1: it says what is wrong (the
context could not be written), what was expected, how to satisfy it. FR-2 / P15: the receiver cannot shorten a path; its
door is to stop and tell the person the ways out. For a non-length failure the door is one relaunch, then report.

**D2a — F-1: the refusal does not lock the role; an informed pass stays possible, with a recorded reason** (P13, FR-4;
coordinator, «по рекомендации, до слова владельца»). The pass is the factory's one road for a person's word over a
dispatch block: `waiver.py --task <T> --stage <S> --block "could not be written" --words-file <file>` records a
`stage_overrides[]` entry; `refuse_native_packet` reads it through `waiver.split_overridden` (the same reader stage_guard
uses), journals the pass through `stage_guard.journal_override` (event `gate_override`, P13), writes NO denial row, and
lets the launch go ahead without the packet — informed, recorded, never silent. A launch with no carrier for a word
(ticketless: the doctor's probe; no `pipeline.json`; a running dispatch without `stage`) cannot be passed: there is
nothing a word could be read from, and the probe exists to prove that context arrives. That is not a dead end (FR-57):
the length cause has the person's two exits (a shorter folder, long paths), the write-error cause has relaunch-then-blocker.

**D2b — F-7 and F-9: a write that fails inside `deliver` never costs the child its context** (coordinator, «по
рекомендации, до слова владельца»). A failed binding-receipt write (F-7) or a failed rewrite of the packet as `delivered`
(F-9) still delivers the context and leaves one stderr line plus one `person_signal` of kind `inject`. The child never
starts silently without the context. The signal's only reader is the run report (`report_facts._hook_signals`): Q-2,
decided «по рекомендации, до слова владельца»; no doctor reader is added. Under D1 the binding case happens for unnamed
launches at roots 120..152 and for non-length write errors (disk full, permissions, a corrupt existing binding); the
rewrite case only for non-length errors (the rewrite has the staged packet's length).

**D3 — `hooklib.artifacts_dir(ticket, event=None, root=None)`**, body `return artifact_root(event, root=root) / str(ticket)`
after the unchanged component check. Callers that change: `worker_lifecycle.binding_is_active` (drops its copy),
`_blocking_text`, `note_unlaunched_denial`, `guard`'s stop branch (all pass `root=root`). Every other caller is unchanged
(default `None`). `native_context.pending_path` stays (F-5).

**D4 — OH5-10 stays a live row; code before the measurement keeps today's selection rule** (ambiguous -> nothing
delivered, nothing moved, nothing deleted), now with the F-4 signal. See §5.

**D5 — OH5-13 F3: only the class sentence folds in** (the old red `test_doctor_context` = OH3-36 itself). The shared temp
suffix is F-2; receipts, K1/K7 and the rest stay in OH5-13. See §5.

**D6 — The door names the factory's supported root, not this file's limit** (t-212 F3, coordinator). The door number is a
separate constant from `PACKET_ROOT_LIMIT`, set by the t-216 measurement of every bounded-suffix writer (fact 10):

supported root: 119 characters (t-216; coordinator's basis `native_context.py:10-13`, limit 259 usable characters)

It equals `PACKET_ROOT_LIMIT` today because the packet and the binding are the longest bounded writers; the two constants
stay separate so a later F-2 or a new writer changes the door's number in one place. The text says "at most N characters
(shorter is safer)" and never presents N as a guarantee: writers with uncapped components (story key, session id) can
still exceed the limit below it (non-goal, separate finding). Neither the door nor the refusal ever names 151.

## 3. Part A — OH3-36: refusal instead of silent pass; `deliver` keeps the context (builder -> critic)

Lands on `pile/onboarding-forge/batch-1` (int-of1). Critic: mandatory (refusal + census ratchet).

given: `ai-packages/qa-factory/design/factory-rules.md` (whole), `plans/builder-rules.md`, this spec, the finding
`plans/piles/onboarding-forge/findings/20261030-windows-260-codex-dispatch-bez-konteksta.md` §1, the files in owns, and
for reading only: `scripts/waiver.py` (`split_overridden` `:202-222`, the `stage_overrides[]` record shape),
`scripts/stage_guard.py` (`waiver_hint` `:792-798`, `journal_override` `:935-955`), `scripts/contract.py`
(`live_stage_overrides` `:155`), `scripts/host_dispatch.py` (`record`, `binding_path`), `scripts/hooklib.py`
(`person_signal` `:2513`, `_once_flag` `:2417`), `scripts/tests/test_test_locations.py` (`journal_signals` `:572-578`).
owns: (absolute under the builder's worktree root `<WT>`; the Lead rewrites `<WT>` at dispatch)
`<WT>\ai-packages\qa-factory\scripts\native_context.py`
`<WT>\ai-packages\qa-factory\scripts\inject_context.py`
`<WT>\ai-packages\qa-factory\scripts\refusal_registry.py`
`<WT>\ai-packages\qa-factory\scripts\tests\test_doctor_context.py`
`<WT>\ai-packages\qa-factory\scripts\tests\test_codex_host.py`
`<WT>\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json`
`<WT>\ai-packages\qa-factory\changelog.d\oh3-36-native-context-long-root.md`
non-goals: `event_store.py` (temp suffix: F-2); `hooklib.py`; `host_dispatch.py`; `host_capabilities.py` (its record allows
a root of 121, above the supported 119: no change); `waiver.py`; `stage_guard.py`; the three existing native refusals'
denial lines (F-6); `deliver`'s selection logic (OH5-10); a length pre-check; `\\?\` prefixing of paths; OH3-37 writers;
any change to `NAME_HEX` or `PACKET_ROOT_LIMIT`; a doctor reader of `hook_signal` (Q-2);
writers whose path length depends on uncapped variables (story key, the case-id stem in `probe_by_code.write_receipt`, the
session id in `cost_capture`, `baseline_contract`'s pid temp name) — finding: uncapped path components, to be filed.
handoff: builder report (rule 7 of `.claude/agents/builder.md`) with the FR walk A-G, the witness, the raised ratchet keys.
designer: <Lead fills the accepted path of this draft>

### A.1 `native_context.py`
1. `NAME_HEX = 32` and `PACKET_ROOT_LIMIT = 119` unchanged; no rename, no `_slot` docstring change. Extend the comment above
   `PACKET_ROOT_LIMIT` by one line: "the binding receipt `host_dispatch.binding_path` (64 hex) has the same limit, root + 140".
2. `TEMP_NAME_EXTRA = 37` with the comment "length of `.<uuid4 hex>.tmp`, the temp name `event_store._publish` adds".
3. `PATH_LIMITS = {"nt": 259}` with the comment "the longest path an ordinary Windows open accepts when long paths are
   off; a platform not in the table has no limit the factory knows".
4. `SUPPORTED_ROOT = 119` with the comment "the longest project root the factory's bounded-suffix writers fit under the
   Windows limit (the native packet and the host-dispatch binding, root + 140; measured across the package by t-216); not
   this file's packet alone. Writers with uncapped components are not covered by it."
5. `def write_path_length(root, session, task_name=None) -> int`: `len(str(_slot(root, session, task_name))) + TEMP_NAME_EXTRA`.
   Pure, touches no disk.
6. `def unwritten_facts(root, session, task_name, exc, platform=None) -> dict`, pure, never raises:
   - `platform = os.name if platform is None else platform`; `limit = PATH_LIMITS.get(platform)`;
   - `slot = str(_slot(root, session, task_name))`; on platform `"nt"` normalise it with
     `str(PureWindowsPath(slot))` (turns `//?/C:/...` into `\\?\C:\...` on every OS); `extended = slot.startswith("\\\\?\\")`
     (covers `\\?\C:\...` and `\\?\UNC\...`; t-212 E9);
   - `length = write_path_length(root, session, task_name)`;
   - `too_long = bool(limit) and not extended and length > limit and (isinstance(exc, FileNotFoundError) or
     getattr(exc, "winerror", None) == 206 or getattr(exc, "errno", None) == errno.ENAMETOOLONG)`;
   - returns `{"cause": "path_limit" if too_long else "write_error", "length": length, "limit": limit,
     "root_length": len(str(root)), "packet_limit": PACKET_ROOT_LIMIT, "supported": SUPPORTED_ROOT,
     "error_type": type(exc).__name__, "error": str(exc)}`.
7. **`deliver`, the two writes before the output (F-7 and F-9, t-212 E3; «по рекомендации, до слова владельца»).** One
   module helper, used for both writes:
   `def _said_write_failure(event, data, what, exc) -> None`: prints ONE stderr line
   `DELIVER_WRITE_FAILED.format(role=data.get('role'), task=data.get('task_name') or '(no task name)', what=what, error_type=type(exc).__name__, error=exc)`
   and calls `person_signal(event, "inject", <the same text>, task=data.get('task_id'))` (`from hooklib import person_signal`),
   no `once_key` (every failed launch is said: noise beats silence). It never raises (`person_signal` never raises; `print`
   to stderr). Constants:
   - `DELIVER_WRITE_FAILED = "FACTORY CONTEXT: the context of {role} ({task}) was delivered, but {what} ({error_type}: {error}). If the project folder is long, a shorter folder or Windows long paths fix it."`
   - `BINDING_UNWRITTEN = "its launch receipt could not be written; the duplicate-spawn guard and recovery cannot see this worker until it stops"`
   - `PACKET_UNMARKED = "its packet could not be marked delivered; it stays pending, so a later launch of this role in this session may find two launches waiting and get no context (said when it happens)"`
   Edits in `deliver`:
   - (F-7) wrap the `record({...})` call (`:145-150`) in `try: ... except Exception as exc: _said_write_failure(event, data, BINDING_UNWRITTEN, exc)` (C-8);
   - then `text = data.pop('context', '')` and `data.update(...)` as today;
   - (F-9) wrap `atomic_json(path, data)` (`:153`) in `try: ... except Exception as exc: _said_write_failure(event, data, PACKET_UNMARKED, exc)`;
   - `context_output(event, text)` (`:154`) runs in every case. stdout carries only the context.
   POSITIONAL invariant: both guards sit BEFORE `context_output` and around ONE call each, so no failure of a side write can
   skip the output, and nothing else in `deliver` (the selection, the lock) is newly swallowed.
8. **`deliver`, the ambiguity signal (F-4, t-212 E6).** In the `len(chosen) > 1` branch (`:133-141`), after the existing
   stderr line (unchanged text, still one line), add
   `person_signal(event, "inject", <the same text>, task=None, once_key=ambiguous_once_key(role, [x[1].get('task_name') for x in chosen]))`
   with a module helper `def ambiguous_once_key(role, names) -> str`:
   `"native-ambiguous:" + str(role) + ":" + sha256("\n".join(sorted(str(n or "") for n in names)).encode()).hexdigest()[:16]`
   — per role AND per set of waiting names, so a second, different ambiguity of the same role in one session is said again,
   and the same one is said once.
9. `stage`: no change. It keeps raising whatever the write raises.

### A.2 `inject_context.py`
1. Module constants (English, no Cyrillic):
   - `NATIVE_PACKET_UNWRITTEN = "INJECT: the factory context of {role} could not be written for its native launch, so this launch is refused: a role started without it would work without its rules. {cause} {door}"`
   - `PATH_LIMIT_CAUSE = "The context file path would be {length} characters, over the {limit} characters a path may have on this Windows machine, because the project folder is {root_length} characters long."`
   - `PATH_LIMIT_DOOR = "Nothing in this session can shorten it: stop launching factory roles and tell the person the ways out - move the project to a folder of at most {supported} characters (shorter is safer), or, if they can and want to, turn on Windows long paths on this machine (an administrator setting for the whole machine; other tools may not follow it) - then launch the role again. (owner: environment)"` (t-212 E5, F-3; `{supported}` = `SUPPORTED_ROOT` = 119)
   - `WRITE_ERROR_CAUSE = "Writing it failed: {error_type}: {error}."`
   - `WRITE_ERROR_DOOR = "Launch the role again once; if this refusal repeats, stop and tell the person this line as a factory blocker."`
   - `PASS_DOOR = "If the person decides the role may start without its rules, record their words: {hint}"` — appended only
     when the launch has a carrier for a word (ticket, `pipeline.json`, a stage); `{hint}` is
     `stage_guard.waiver_hint(ticket, stage, "could not be written")`.
2. `def refuse_native_packet(event, ticket, role, root, exc, stage=None) -> None` (module level, so A24 and the census see
   one unit; `stage` is the running dispatch's `stage`, `last.get("stage")` when `last` is a dict, else None):
   - `facts = native_context.unwritten_facts(root, event.get("session_id"), ((event.get("_qa_host") or {}).get("input") or {}).get("task_name"), exc)`;
   - pick `(PATH_LIMIT_CAUSE, PATH_LIMIT_DOOR)` when `facts["cause"] == "path_limit"`, else the write-error pair; format
     both with `facts`; when `ticket` and `stage` are non-empty, append `" " + PASS_DOOR.format(hint=...)` to the door;
   - **the pass (F-1, D2a)**, only when `ticket` and `stage` are non-empty: read `pipeline = read_json(artifacts_dir(ticket, event) / "pipeline.json", {}, kind=dict)`
     (any exception -> `{}`); `blocking, passed = waiver.split_overridden([<the formatted message>], pipeline, stage)`;
     when `passed`: `stage_guard.journal_override(pipeline, stage, passed, event)`, print one stderr line
     `"INJECT: the factory context of {role} could not be written; the person's recorded word lets it start without it."`,
     and `return` (the caller exits 0; NO `note_denial`, the launch goes ahead);
   - otherwise: `parts = dict(role=role, cause=cause, door=door)`; `note_denial(event, ticket, None, role, NATIVE_PACKET_UNWRITTEN.format(**parts))`;
     `block(NATIVE_PACKET_UNWRITTEN.format(**parts))` — format the fields once (t-212 F8/E9); the `block(` call's first
     argument must begin with `NATIVE_PACKET_UNWRITTEN` so the A24 key matches (`_key_text` reads the source of the first
     argument). Imports of `block`, `waiver`, `stage_guard` may be local to the function.
3. In the Codex branch (`:651-655`) the call becomes:
   ```
   try:
       stage(project_root(event), event, role, context, ticket)
   except OSError as exc:
       refuse_native_packet(event, ticket, role, project_root(event), exc,
                            last.get("stage") if isinstance(last, dict) else None)
   except ValueError as exc:
       print('INJECT: ' + str(exc), file=sys.stderr)
       sys.exit(2)
   sys.exit(0)
   ```
   POSITIONAL invariant: `except OSError` sits INSIDE the same function as the `stage` call, so no `OSError` of the native
   write can reach `main`'s generic `except Exception` (which allows silently). `OSError` and `ValueError` share no class,
   so the existing `ValueError` refusals keep their text and exit code exactly. A passed refusal returns to the
   `sys.exit(0)` that follows — the one road for an allowed launch.
4. `main`'s docstring: add one sentence — "EXCEPT a native context packet that cannot be written, which refuses
   (IC-native-packet-unwritten, t-203) unless the person's recorded word passes it: on the native host the packet is the
   role's whole factory context." Keep the F-9/F-11 residual sentence for every other crash.

### A.3 `refusal_registry.py`
A row after `IC-oversized-slice` (F-1 decided «по рекомендации, до слова владельца»; t-212 E4):
`{"id": "IC-native-packet-unwritten", "file": "inject_context.py", "function": "refuse_native_packet", "call": "NATIVE_PACKET_UNWRITTEN", "refuses": "a native (Codex) role launch whose context packet could not be written: native_context.stage raised OSError (a path over the Windows limit for a project folder longer than native_context.PACKET_ROOT_LIMIT, an unwritable folder, a lock that cannot be opened); until t-203 the launch went ahead with no context and left only a hook_signal", "override": WAIVER + " with `--block \"could not be written\"`: the word does not write the file, it says 'start the role without its factory context' - informed. `refuse_native_packet` filters the line through `waiver.split_overridden` like the stage_guard rules and journals the pass as `gate_override` (P13), writes no denial row, and the launch goes ahead. A ticketless launch (the doctor's probe) or one with no pipeline.json or no dispatch stage has no carrier for a word and stays refused; its ways out are in the message (a shorter project folder or Windows long paths for the length cause, one relaunch then a factory blocker otherwise). Decided by recommendation pending the owner's word (t-203 F-1).", "unpassable_because": "", "test": "scripts/tests/test_doctor_context.py (PacketNameLength: refusal and pass rows)"}`
The precedent is the `SG-manifest-unread` row (`override` = `WAIVER` + the pass), not `PT-git-config` (t-212 F9).
The registry file is plain English; the Russian mark stays in this spec only (FR-30).

### A.4 `judgment-census.json`
Row `{"file": "inject_context.py", "function": "refuse_native_packet", "class": "shape", "roles": [<the 13 of the collect_blocks row>], "owner": "data", "ref": "A24:IC-native-packet-unwritten"}`; raise `ratchet.blocking_per_role` by exactly what `test_judgment_census.py` reports (expected +1 for each of the 13 keys) and list each key old -> new in the report. A row for `native_context.unwritten_facts` only if the test names it as a unit (class `shape`, owner `data`, roles `["conductor"]` as the `stage` row). If the test names `_said_write_failure` or the guards as units, they are non-blocking `shape`/`data` rows.

### A.5 `changelog.d/oh3-36-native-context-long-root.md`
English fragment, `README.md` form: a native role launch whose context cannot be written (for example a project folder
longer than 119 characters on Windows without long paths — limit unchanged) is now refused with the cause and the way out,
or passed by the person's recorded word, instead of starting the role without its context; and a launch receipt or packet
record that cannot be written at the child's start no longer stops the context from being delivered — it is reported
instead.

### A.6 Edge behaviour (each with the invariant it protects)
Invariant I-A: a native role never starts without a factory context that was not delivered, unless a refusal or a
recorded person's word said why. Invariant I-B: a packet is never handed to a child of another launch. Invariant I-C: a
person's word passes only the line it names, on its stage, while it stands.

| edge | behaviour | invariant |
|---|---|---|
| root exactly 119 (named launch), Windows, long paths off | packet path + temp = 259: writes; binding 259: writes; delivered, no refusal | I-A (no false refusal at the limit) |
| root 120+, named launch, Windows, long paths off | write raises `FileNotFoundError` -> refusal, cause `path_limit`, exit 2, denial row, no packet file; door names 119 | I-A |
| root 120..152, unnamed launch, long paths off | `stage` writes (unnamed limit 152); in `deliver` the binding write fails -> F-7: the context is delivered, one stderr line, one `hook_signal` of kind `inject`, packet `delivered` | I-A (the context still reaches the child; the blind duplicate guard is said, not silent) |
| root 153+, unnamed launch | `stage` write fails -> refusal, cause `path_limit` | I-A |
| root 120+, Windows, long paths ON | writes; no refusal (nothing is predicted) | I-A without over-refusal |
| root over the limit, error is `PermissionError` (e.g. read-only) | refusal, cause `write_error` (the length is not blamed) | I-A; error direction: only between two refusal texts |
| UNC root `\\server\share\...` | counted as the string it is; same limit; length cause when over and the error fits | I-A |
| extended-length root `\\?\C:\...`, `\\?\UNC\...`, `//?/C:/...` | the limit does not apply (detected on the normalised slot string): any failure is `write_error` | I-A |
| non-Windows (`os.name` not in `PATH_LIMITS`) | no limit; any `OSError` -> `write_error` refusal | I-A, one road on every platform (P31) |
| an existing pending packet under the same slot that cannot be READ (`OSError`) | now refused through the `OSError` branch (was a crash that allowed) | I-A |
| an existing pending packet that cannot be PARSED | `ValueError` refusal as before (`test_codex_host.py:376-385` unchanged) | unchanged |
| lock file cannot be opened (`LockBroken`, an `OSError`) | refusal, `write_error` | I-A |
| `ticket` empty (the doctor's probe launch) | refusal the same way, no `PASS_DOOR`, no pass (no carrier); `note_denial` goes to the project-level ticketless list; `host_probe` injection stays `unverified`, which is true | I-A, one road for probe and story |
| ticket present, no `pipeline.json` or unreadable | `pipeline = {}` -> no override -> refusal (the door still shows `PASS_DOOR`: `waiver.py` is the road that creates the record) | I-C, error direction toward refusing |
| running dispatch has no `stage` (or no running dispatch: `last` is None) | no `PASS_DOOR`, no pass; refusal | I-C |
| a live override naming the line (`--block "could not be written"`) on the dispatch's stage | pass: `gate_override` journal line, stderr line, exit 0, NO denial row, no packet | I-A (informed), AR-25 (recover does not close a launch that starts) |
| a live `*` override on the same stage | passes, like every other dispatch block on that stage (one road, P31) | I-C as the existing reader defines it |
| a revoked override, a `<placeholder>` match, an override of another stage, a partial-word match | refusal | I-C |
| `journal_override` cannot write | the pass still holds (that function is best-effort by its own docstring) | person's decision kept |
| `waiver.py` recheck after recording | it asks stage_guard, which never raises this line, so it prints "block lifted ... no longer refuses"; the next launch reads the same record through `split_overridden` and passes | one road; the message is true for the next launch |
| exception with an empty message | text shows the type name and an empty tail; never raises | — |
| `deliver`: `record` raises anything (an `OSError` of the binding write, a `ValueError` from a corrupt existing binding, a `KeyError` from a malformed packet) | caught (C-8): the context is delivered, one stderr line, one signal, no `once_key` | I-A |
| `deliver`: the rewrite of the packet as `delivered` raises (lock, permission, full disk; never the length: same name as the staged packet) | caught (F-9): the context is delivered, one stderr line (`PACKET_UNMARKED`), one signal; the file stays as staged (`pending`, with the context) | I-A over tidiness |
| `deliver`: both writes fail in one start | two stderr lines and two signals (one per write), then the context | I-A; each fact said once |
| a later launch of the same role in that session, after an F-9 failure | the old packet is still `pending`: an identified child (task name) is unaffected; an unidentified child meets two waiting packets -> nothing delivered, the existing stderr line plus the F-4 signal; a restage of the SAME task name is refused `StateConflict` (existing rule) | I-B over delivery; said, never silent |
| `deliver`: `person_signal` cannot write the journal | it falls back to stderr itself and never raises (`hooklib.py:2518`); delivery unchanged | I-A |
| `deliver`: two pending packets of one role, no child identity (OH5-10 ambiguity) | as today: nothing delivered, nothing moved, the one stderr line unchanged; PLUS one `hook_signal` of kind `inject`, once per role per set of waiting names per session | I-B over delivery; the starved launch is visible in the run report |
| `deliver`: the same ambiguity a second time in one session | no second signal (once flag); stderr line still printed | — |
| `deliver`: a different ambiguity of the same role in one session | a new signal (another name set, another key) | — |
| a root of 119 or less with a long story key or session id | a writer with an uncapped component may still fail; not this node (non-goal, finding: uncapped path components) | — |
| TEMP longer than 119 characters on a test machine | `DoctorContext` rows rooted in TEMP fail with the refusal text (red and explicit, not silent); `PacketNameLength` proof rows do not use TEMP | FR-31 |

### A.7 Test rows (DoD) — variant/table rows in keep files only
In `test_doctor_context.py`, class `PacketNameLength`:
- A1 (pure, no disk, no TEMP) `N.NAME_HEX == 32`, `N.PACKET_ROOT_LIMIT == 119`, `N.SUPPORTED_ROOT == 119`; for a string root
  of length L built as `"C:\\" + "p" * (L - 3)`: `write_path_length(root, 's', 'qa_scout__qa_1') == L + 140` for L in
  (119, 120); `== 259` at 119, `== 260` at 120; unnamed: `write_path_length(root_152, 's') == 259`.
- A2 (disk confirmation) keep `test_root_at_the_limit_writes_and_one_beyond_exceeds_the_windows_path` as it is (119/120).
- A3 keep `test_the_old_failing_path_of_260_now_writes` and `test_a_packet_under_the_old_long_name...` unchanged.
- A4 table `unwritten_facts` (pure, string roots, explicit `platform`), one parameterised test, id per row:
  `at_limit_nt` (119, `FileNotFoundError`, nt) -> `write_error`; `over_nt` (120, FNF, nt) -> `path_limit`, length 260,
  root_length 120, packet_limit 119, supported 119; `over_permission` (120, `PermissionError`, nt) -> `write_error`;
  `over_enametoolong` (120, `OSError(errno.ENAMETOOLONG, "x")`, nt) -> `path_limit`; `over_winerror206` (120, a test
  subclass of `OSError` with attribute `winerror = 206`, nt) -> `path_limit`; `unc_over` (`"\\\\srv\\share\\"` padded to 120,
  FNF, nt) -> `path_limit`; `extended` (`"\\\\?\\C:\\"` padded to 200, FNF, nt) -> `write_error`; `extended_unc`
  (`"\\\\?\\UNC\\srv\\share\\"` padded to 200, FNF, nt) -> `write_error`; `extended_forward_slash` (`"//?/C:/"` padded to 200,
  FNF, nt) -> `write_error` (runs on every OS: normalisation is `PureWindowsPath`); `posix_long` (300, FNF, `"posix"`) ->
  `write_error`, `limit is None`; `unnamed_153` (153, FNF, nt, task None) -> `path_limit`; `empty_message` (120,
  `FileNotFoundError()`, nt) -> `path_limit`, `error == ""`.
- A5 refusal text (in-process): call `inject_context.refuse_native_packet` with a patched `inject_context.note_denial` spy
  and an event carrying `_qa_host.input.task_name`, ticket `""` (no pass road), for two cases — a 120-character string
  root with `FileNotFoundError` on platform nt (patch `native_context.PATH_LIMITS` to `{os.name: 259}` so the row runs on
  every OS) and any root with `PermissionError`. Each: `SystemExit` code 2; stderr contains the role, `refused`, and —
  path case — `120`, `260`, `259`, `at most 119 characters`, `shorter is safer`, `long paths`, `if they can and want to`,
  `(owner: environment)`, and NOT `151`; write case — `PermissionError`, `again once`, and NOT `151`; neither case contains
  `waiver.py`; the spy got one call whose reason equals the stderr text before the `TRAPPED` line.
- A5b the pass (F-1), one parameterised test over a scratch project with `qa-factory/config.json`, a story `T` whose
  `pipeline.json` carries `stage_overrides` in the shape `waiver.py` writes (read it from `waiver.py`), stage `S1`, and
  `refuse_native_packet(event, 'T', 'qa-scout', root, PermissionError('x'), 'S1')` with the `note_denial` spy, id per row:
  `live_named` (override `match: "could not be written"`, stage `S1`) -> returns, no `SystemExit`, spy not called, a
  `gate_override` row in the project journal; `live_star` (`*` on `S1`) -> same; `revoked` (`revoked_at` set) -> `SystemExit(2)`,
  spy called once, stderr contains `waiver.py --task T --stage S1`; `other_stage` (override on `S2`) -> `SystemExit(2)`;
  `no_pipeline` -> `SystemExit(2)`; `no_stage` (`stage=None`) -> `SystemExit(2)` and stderr has no `waiver.py`.
- A6 hook end to end (class `DoctorContext`, real subprocess, both OSes, length-free): run `guard_pre_tool.py` and
  `inject_context.py` as the first test does; take `p = pending_path(self.root, 'parent')`; `p.unlink()`; `p.mkdir()`; run
  `inject_context.py` again -> returncode 2; stderr contains `could not be written` and one of `IsADirectoryError` /
  `PermissionError` / `FileExistsError`; `p.is_dir()`; `self.factory/'state/dispatch-denials.jsonl'` has a row whose
  `reason` starts with `INJECT: the factory context of qa-scout`.
- A7 the door opens (FR-2): in the same test, `p.rmdir()`, run the hook again -> returncode 0 and `pending_path(...)` is a
  file with `status == 'pending'`.
In `test_codex_host.py`, `test_subagent_start_delivers_each_child_the_packet_of_its_own_launch` (`:387`), new steps as
variants of the same scenario (no new test file; the `:348-349` literal stays, `NAME_HEX` is unchanged):
- A8 (F-7) stage one launch `a`; patch `host_dispatch.record` to raise `OSError('disk full')`; `run(start('child-a', a)) == 'context A'`;
  the packet is `delivered` and holds no `context`; `binding_path(root, 'child-a')` does not exist; `seen['err']` is one
  line containing `qa-scout`, `launch receipt could not be written`, `OSError`, `disk full`, and not `context A`; the
  project journal (read as `test_test_locations.journal_signals` does) has one `hook_signal` of kind `inject` with the same
  text and `task == 'STORY-A'`. A second variant with `ValueError('broken receipt')` gives the same outcome.
- A8b (F-9) stage one launch `a`; patch `native_context.atomic_json` to raise `PermissionError('locked')` (the patch is
  applied after `stage`, so only the rewrite in `deliver` meets it); `run(start('child-a', a)) == 'context A'`; the packet
  file is byte-identical to the staged one (`pending`, context kept); the binding exists (record ran); `seen['err']` is one
  line containing `qa-scout`, `could not be marked delivered`, `PermissionError`, `locked`, and not `context A`; one
  `hook_signal` of kind `inject` with the same text and `task == 'STORY-A'`. A variant with both `record` and the rewrite
  failing: two stderr lines, two signals, and the context on stdout.
- A9 (F-4) in step (v) (`:450-463`): before `run(start('child-x'))`, unlink
  `hooklib._once_flag(start('child-x'), 'signal|inject|' + native_context.ambiguous_once_key('qa-scout', [a, b]))` if it
  exists (the flag lives in the OS temp and would survive a previous run); after the run, the existing assertions stay
  (stderr one line, names, no contexts) and the journal has exactly one new `hook_signal` of kind `inject` naming `a` and
  `b` and neither context; a second `run(start('child-x'))` adds no second signal; unlink the flag again at the end.
Other runs: `python -B ai-packages/qa-factory/scripts/refusal_registry.py --check` exit 0;
`python -B ai-packages/qa-factory/scripts/selftest.py --lang`.

DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for scripts/native_context.py scripts/inject_context.py scripts/refusal_registry.py scripts/tests/test_doctor_context.py scripts/tests/test_codex_host.py scripts/tests/fixtures/judgment-census.json changelog.d/oh3-36-native-context-long-root.md`
and every non-quarantined file it prints, plus the two runs above; the witness is the verbatim output. Acceptance keys:
A1-A9 (with A5b, A8b) green; A24 clean; census green with the raised keys listed; no `151` in any owned file (the builder
greps its owns for `151` with a positive control and attaches it); FR walk A (FR-1, FR-2, FR-4 — the pass, FR-57,
FR-59), B ("no person text: machine channel"), C (FR-13: `PATH_LIMITS` is a platform row, precedent `event_store` Windows
codes 5/32), D (FR-59), E (FR-8: the person's word reaches the refusal), G (FR-30, FR-31, FR-32); AR lines of §1 in the
commit (`architecture: AR-9, AR-28, AR-24, AR-29, AR-20, AR-25, AR-22, AR-1 -- ...`, `judgment:` line naming the shape unit).
edges: §A.6 table.
siblings: `session_identity.write_receipt` (same `_publish` temp name, receipts lost silently from a root of about 145:
OH5-13 / F-2); `host_dispatch` binding receipts under `qa-factory/state/host-dispatches/` — measured, root + 140, same
limit as the named packet (facts 9, 10), handled in `deliver` by A.1.7, not widened into `host_dispatch.py`;
`host_capabilities.record` (root 121, above the supported 119: no change); the three unregistered native `ValueError`
refusals (F-6); writers with uncapped path components (finding: uncapped path components, to be filed).

## 4. Part B — OH5-11: `artifacts_dir(root=)` and the copy in `worker_lifecycle` (builder -> critic)

File-disjoint from Part A, so it can be built in parallel; it lands on `pile/onboarding-hooks/batch-5` after the queue
`onboarding-forge/1 -> onboarding-hooks/5` (Lead's call). `hooklib.py` is a hot file: the edit is the function
`artifacts_dir` ONLY (signature, docstring, body). `test-layers.json` is edited in one array only.

given: `design/factory-rules.md` (whole), `plans/builder-rules.md`, this spec, finding
`plans/piles/onboarding-hooks/findings/B-394-u-native-context-pending-path-okolo-stroki-42.md`, the files in owns.
owns:
`<WT>\ai-packages\qa-factory\scripts\hooklib.py (artifacts_dir)`
`<WT>\ai-packages\qa-factory\scripts\worker_lifecycle.py`
`<WT>\ai-packages\qa-factory\scripts\tests\test_resolver.py`
`<WT>\ai-packages\qa-factory\scripts\tests\test-layers.json (the "covers" array of "test_resolver.py" only)`
non-goals: `native_context.pending_path` (F-5); `is_one_component` and its docstring; any other `artifacts_dir` caller;
the eight other copies of the one-component check (queued: new onboarding-hooks node); quarantined tests (not run, not
edited); OH5-12's literal paths.
handoff: builder report with FR walk, witness, the grep with its positive control and the verdict line per copy.
designer: <Lead fills>

Behaviour:
1. `hooklib.artifacts_dir(ticket: str, event: dict | None = None, root: Path | None = None) -> Path`: the component check
   unchanged (same `ValueError` text), then `return artifact_root(event, root=root) / str(ticket)`. Docstring: "`root`,
   when given, is the project the story lives under (a reader that walked receipts under a root of its own); else the
   event's project."
2. `worker_lifecycle.binding_is_active`: delete `:94-95` (the copy) and replace `:96-99` with
   `from hooklib import artifacts_dir` / `state = json.loads((artifacts_dir(task, event, root=root) / "state/controller.json").read_text(encoding="utf-8"))`
   inside the existing `try`, whose `except (OSError, ValueError): return True` now also covers the component refusal.
   Docstring: replace the sentence "exactly as `hooklib.artifacts_dir` would ... when no event is given" with "through
   `hooklib.artifacts_dir(..., root=root)`, so a receipt cannot steer the read outside the story folders".
3. `_blocking_text`: `artifacts_dir(task, event, root=root)` (`:119`). `note_unlaunched_denial`: same at `:160`.
   `guard`'s stop branch: same at `:214` (t-212 E7) — `artifacts_dir(task, event, root=root)`; its handler
   `except (OSError, ValueError, AttributeError, TypeError)` already turns a refused ticket into `allowed = None` -> stop
   denied, the safe direction of a stop.
4. `test-layers.json`: add `"worker_lifecycle.py"` to the `covers` array of `"test_resolver.py"` (t-212 E8, C-9), so a later
   edit to `worker_lifecycle.py` runs B2-B5.

Edges (invariant: a doubtful receipt keeps a worker ACTIVE and a stop DENIED; a ticket never leaves the story folders):
- ticket `.`, `..`, `a/b`, `a\b`, `C:x` -> `artifacts_dir` raises `ValueError` -> `binding_is_active` returns `True` (as today);
  in `guard`'s stop branch -> `allowed = None` -> the stop is refused (as today).
- ticket empty or missing -> `True` before the call (`:91-92`, unchanged); in the stop branch `{}` (`if task else {}`,
  unchanged) -> refused; `artifacts_dir` itself refuses `""`/`None`.
- broken `qa-factory/config.json` under `root` -> `artifact_root` raises `ValueError` -> `True` / stop refused (as today).
- `root=None` and `event=None` (other callers) -> unchanged behaviour (event's / cwd project).
- `root` given AND an event of another project -> `root` wins (that is the point of the parameter); in `guard` both are
  the same project, so production output is unchanged.
- a test double of `hooklib.artifacts_dir` without a `root` parameter, used where `worker_lifecycle` runs, would raise
  `TypeError`; the builder greps `scripts/tests/` for such doubles in keep files and updates them (quarantined files are
  left; name them in the report). In the stop branch a `TypeError` is caught -> stop refused (safe), but the binding and
  denial paths would differ, so the doubles are updated.

Test rows (in `test_resolver.py`, one table each, id per row):
- B1 `artifacts_dir(..., root=tmp)`: no config -> `tmp/qa-factory/artifacts/T`; config `artifact_root: "custom"` ->
  `tmp/custom/T` (resolved); broken config -> `ValueError`; tickets `..`, `a/b`, `a\\b`, `C:x`, `""` -> `ValueError`;
  `root=None` equals `artifact_root(None) / T` (cwd project).
- B2 `worker_lifecycle.binding_is_active(tmp, binding)`: the five bad tickets -> `True`; controller.json under `tmp`
  with the dispatch `accepted` -> `False`, `running` -> `True`, no status -> `True`.
- B3 `_blocking_text([{"dispatch_id": "D"}], tmp, "T", None)` names `tmp/qa-factory/artifacts/T` (resolved) in its door.
- B4 spy: patch `hooklib.artifacts_dir` with a wrapper recording calls; `binding_is_active(tmp, {"task_id": "T", "dispatch_id": "D"})`
  -> exactly one call with `root=tmp` (proof the survivor is used; replaces the node's grep-test, C-5).
- B5 (t-212 E7) `guard` stop branch, a B3-like row: under `tmp` (pinned as the project root the way `test_resolver.py`
  already pins one), one receipt answering to target `X` with `task_id` `T`, `dispatch_id` `D`; controller.json under `tmp`
  whose dispatch `D` carries `cancellation` -> `guard({... "interrupt_agent", target X})` does not block; without
  `cancellation` -> blocks with `stop denied`; receipt `task_id` `..` -> blocks; the spy of B4 records `root=tmp`.

Copies of the one-component check (t-212 F5/E7; Grep `"/\\\\:"` over `scripts/*.py`, case-insensitive, re-run in t-215;
positive control: the same call finds the survivor `hooklib.py:236`). Verdict per site (Q-3 decided «по рекомендации, до
слова владельца»: one new onboarding-hooks node, axis 8 named, "every one-component check calls
`hooklib.is_one_component`"; not OH5-12, which is literal artifact paths, another class):

| site | what it guards | verdict |
|---|---|---|
| `worker_lifecycle.py:94` | story ticket from a receipt | fixed here (behaviour 2) |
| `host_dispatch.py:21` (`controller_record`) | story ticket; error direction None on doubt | queued: new onboarding-hooks node |
| `exit_gate.py:209` | story folder names | queued: new onboarding-hooks node |
| `stage_guard.py:436` | story folder names | queued: new onboarding-hooks node |
| `stage_guard.py:643` | ticket from env | queued: new onboarding-hooks node |
| `stage_guard.py:717` | story names | queued: new onboarding-hooks node |
| `activity_capture.py:44` | session id | queued: new onboarding-hooks node |
| `cost_capture.py:1907` | session id | queued: new onboarding-hooks node |
| `cost_capture.py:3800` | session id | queued: new onboarding-hooks node |

The Lead opens that node (finding + batch row, PROJECT.md «Командная работа» p. 2) before Part B is accepted. The builder
repeats the Grep with its control in the report and confirms the list; a hit not in the table is reported, not fixed.

DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for scripts/hooklib.py scripts/worker_lifecycle.py scripts/tests/test_resolver.py scripts/tests/test-layers.json`
and every non-quarantined file it prints (expect about 80 lines, t-212 F10); plus in the report the Grep of `scripts/` for
`"/\\\\:"` with its positive control and the verdict table above. Acceptance keys: B1-B5 green; AR line
`architecture: AR-15, AR-13 -- worker_lifecycle calls hooklib.artifacts_dir(root=) at all three sites`;
`judgment: none -- no check added or altered (artifacts_dir row unchanged)`.
edges: listed above.
siblings: axis 8 (story location) of `docs/SIBLING_MAP.md` — the Lead adds `artifacts_dir(root=)` to its row; the eight
copies above (queued: new onboarding-hooks node); OH5-12 (literal artifact paths) is another remainder, not here.

## 5. OH5-10 and OH5-13 F3

**OH5-10 (B-325) — what the measurement must establish** (live row "OH5-10: измерение идентичности `SubagentStart`
на живом Codex", moved to `live-runs`, owner's word 11.11.2026). On a live Codex host, one session, two native launches of
the same agent type (one named, one whose spawn fails or is abandoned), capture the raw `SubagentStart` event and the
child's first transcript line:
(m1) does the event, or the `agent_transcript_path` it carries, give the child's `agent_path` (what
`host_dispatch.child_identity(event)["task_path"]` reads)? (m2) does a FAILED spawn produce any hook event (a `PostToolUse`
with an error) that names the staged launch? (m3) how long after the spawn does `SubagentStart` arrive (for a lifetime, if
one is ever needed)?
Code before the measurement (the safe default, deliberately unchanged): ambiguous -> nothing delivered, no packet moved,
none deleted, one stderr line — plus, now, the F-4 `hook_signal` (Part A, A.1.8), so the run report shows which role
started without context. Reasons: deleting or ageing out a packet without (m2)/(m3) can drop a LIVE launch's context;
picking by recency can hand a child another launch's context (I-B). After the measurement: (m1) yes -> the stale packet is
harmless, only cleanup of `delivered` records remains; (m1) no and (m2) yes -> explicit cancel on the failed spawn; both
no -> lifetime from (m3). That choice is OH5-10's builder node, after the row.

**OH5-13 F3 (B-451) — split:**
| piece of F3 | where |
|---|---|
| "same class as the two old red `test_doctor_context`" | folds in: Part A (the red came from the native packet path) |
| `_publish` temp name `.<uuid32>.tmp` costs 37 characters on every writer | F-2 (a separate node recommended) |
| receipts lost silently from a root of about 145 (`session_identity.write_receipt` swallows every failure; the reader falls back to env or `missing`, the safe side) | stays in OH5-13: different writer, different failure policy (a receipt must never change the tool call's outcome) |
| K1/K7 depend on TEMP length | stays in OH5-13 (session_identity tests) |
| A6 (doctor writes `qa-factory/state/` before onboarding) | OH3-37, already its own node |

## 6. Forks and open questions

Decided by the coordinator, «по рекомендации, до слова владельца» (written into the spec above):
- **F-1 — decided (D2a, A.2.2, A.3).** The refusal does not lock the role; an informed pass stays possible through
  `waiver.py`, with a recorded reason (P13, FR-4). Still owed to the owner, in plain words (t-212 §3): (1) does the
  F-9/F-11 residual ("a crash after the receipt read allows the dispatch") cover the native packet write — the spec now
  says no; (2) may a person's recorded word let a role start without its factory context — the spec now says yes, except
  a launch with no carrier for a word (the doctor's probe).
- **F-4 — decided: now** (A.1.8, A9; once per role per set of waiting names, t-212 E6).
- **F-7 — decided: (a)** (D2b, A.1.7, A8): deliver the context, one stderr line, one signal; never start silently without it.
- **F-9 — decided: same as F-7** (D2b, A.1.7, A8b): a failed packet rewrite in `deliver` still delivers the context and
  leaves the same kind of signal.
- **Q-2 — decided: the run report is the only reader** of the F-7/F-9 signal (`report_facts._hook_signals`); no doctor
  reader (non-goal).
- **Q-3 — decided: a new onboarding-hooks node** receives the eight copies (Part B table, «queued: new onboarding-hooks node»).
- **F-3 — taken on the recommendation** with the critic's caveat in the text ("if they can and want to"; an administrator
  setting; other tools may not follow).
- **Q-1 — closed by t-216**: supported root 119 (fact 10, D6, `SUPPORTED_ROOT = 119`); uncapped writers -> finding:
  uncapped path components, to be filed (non-goal).

Remaining, recommendation unchanged (the critic agrees with each):
- **F-2.** Shorten the shared temp suffix of `event_store._publish` (32 -> 8 hex: +24 characters for every writer; packet
  and binding 119 -> 143, unnamed 152 -> 176, receipts about 145 -> 169). Cost: a core file (critic mandatory), the golden
  normalisation rule `driver-golden-rules.json` N8a (`[0-9a-f]{32}` before `.tmp`) and its `test_driver_golden.py` row,
  the `TEMP_NAME_EXTRA` pin, a 32-bit uniqueness per concurrent pair on one target (open the temp in `"x"` mode so a
  collision fails instead of interleaving). Recommendation: a separate node in onboarding-hooks/5 next to OH5-13, with the
  binding limit named; if taken, `SUPPORTED_ROOT` moves with it in the same node.
- **F-5.** Keep `native_context.pending_path` (removal moves 14 live test sites onto the private `_slot`). Recommendation:
  keep; OH5-11 closes on the `worker_lifecycle` copy plus the queued copies.
- **F-6.** Give the three existing native `ValueError` refusals the same `note_denial` line and A24 rows? A `StateConflict`
  denial could make `recover` close a launch that is in fact pending. Recommendation: not in t-203; a finding in
  onboarding-hooks for the unregistered native refusals.

## 7. Small choices closed by the designer

- C-1 (withdrawn in t-215) `NAME_HEX = 16` — dropped with D1's shortening (t-212 E1).
- C-2 The refusal's cause is chosen by `unwritten_facts` from facts; the GATE is the `OSError` itself (no pre-check).
- C-3 `PATH_LIMITS` and `SUPPORTED_ROOT` live in `native_context.py`, not in `references/`: platform/package facts, not
  project variety (AR-1 n/a).
- C-4 No `person_signal` beside the refusal: an exit-2 refusal with a denial row is not silent.
- C-5 Part B proves the survivor with spy rows (B4, B5) instead of a source-grep test (TESTING.md: no source-scanning test
  for a single site); the grep with positive control goes into the report.
- C-6 TEMP independence: the proof rows (A1, A4, A5) build string roots and touch no disk; A5b, A6, A7 use a scratch
  folder whose length is irrelevant; only A2 (confirmation) still uses the TEMP base, with its skip.
- C-7 `except OSError` is placed before `except ValueError` for reading order; the classes are disjoint.
- C-8 (t-215) The `deliver` guards catch `Exception` around ONE call each (`record(...)`, the rewrite), not `OSError` alone:
  those writes are side records of the delivery, the context is the delivery, and a `ValueError` (a corrupt existing
  binding read at `host_dispatch.py:271`) or `KeyError` (a malformed packet) would otherwise drop the context the same
  silent way. Error direction: toward delivering with a signal.
- C-9 (t-215, E8) B2-B5 stay in `test_resolver.py` and `worker_lifecycle.py` joins its `covers`, rather than moving the rows
  to `test_words_doors.py`: that file is the "sole AR-24 detector" (`test-layers.json:6866-6869`), and resolver rows do not
  belong to its layer.
- C-10 (t-215, E9) `extended` is read on the slot string normalised by `PureWindowsPath` on platform nt, so the
  `extended_forward_slash` row runs on every OS instead of being skipped on POSIX.
- C-11 (t-215) The F-7/F-9 signals have no `once_key` (each failed write is its own fact); the F-4 signal has one per role
  and per set of waiting names (t-212 E6). A9 unlinks the OS-temp once flag before and after, since `_once_flag` survives runs.
- C-12 (t-215) F-7 and F-9 share one helper `_said_write_failure` and one text frame `DELIVER_WRITE_FAILED` with two
  `what` clauses: one road for "a side write in `deliver` failed" (P31), no duplicated handler.

## 8. Reading trail

First draft: the four findings given (OF finding §1-2; B-325; B-394; B-451); int-of1 `native_context.py` (whole);
`inject_context.py` `:100-140`, `:302-336`, `:444-455`, `:457-675`; `event_store.py` `:16-31`, `:135-174`, `:226-252`,
`:441-470`, `:539-559`; `hooklib.py` `:230-270`, `:640-735`, `:816-824`, `:2500-2549`; `worker_lifecycle.py` `:1-190`;
`session_identity.py` `:150-209`; `refusal_registry.py` `:56-149`, `:314-373`, `:809-930`; `scenario_walk.py` `:880-922`;
`test-layers.json` (rows by Grep); `judgment-census.json` `:4`, `:398`, `:415-421`, `:567-573`, `:947-948`;
`design/architecture.md` `:106-185`; `references/human-questions.md` `:1-63`; main `test_doctor_context.py` `:1-260`;
int-of1 `test_codex_host.py` `:340-389`, `:440-469`; batch files; `plans/builder-rules.md` 7b.
Fix round t-215 (on `main`): the critic verdict `docs/tasks/specs/reviews/t-212-t-203-plan-review.md` (whole);
`native_context.py` (whole, 166 lines: `deliver` `:110-154`, `record` call `:145-150`, rewrite `:153`, output `:154`);
`host_dispatch.py` `:1-40` (`binding_path` `:10-11`, `controller_record` `:14-26`), `:225-314` (`record`, writes `:247`,
`:282`, new receipt after `:302`); `telemetry_hook.py` `:115-182` (re-raise `:163-177`); `worker_lifecycle.py` `:80-229`
(copy `:94-95`, sites `:119`, `:160`, `:214`); `inject_context.py` `:540-674` (Codex branch `:645-656`, `last` `:601`);
`refusal_registry.py` `:1-70` (docstring on `override`, `WAIVER` `:64`), `:290-349` (`SG-manifest-unread` `override`,
`IC-oversized-slice`, `PT-git-config`); `waiver.py` `:202-284` (`split_overridden`, `recheck_stage_block`); `stage_guard.py`
`:925-955` (`journal_override`), Grep `def waiver_hint` (`:792-798`); `contract.py` Grep `live_stage_overrides` (`:155-169`);
`hooklib.py` Grep `person_signal` (`:2513-2538`), `_carries_project` (`:35-41`), `_once_flag` (`:2417-2427`);
`test_codex_host.py` `:340-474`; `test_test_locations.py` `:570-579`; `test-layers.json` Grep `test_words_doors.py|test_resolver.py`.
Coordinator messages (12.11.2026): t-216 (supported root 119, binding and named packet at root + 140,
`host_capabilities.record` 121, uncapped writers to a separate finding — taken as reported, not re-measured); decisions
Q-2, Q-3, F-9.
Greps with positive controls (t-215): `"/\\\\:"` over `scripts/*.py` -i (10 hits = the survivor `hooklib.py:236`, the
`worker_lifecycle` copy and the eight copies of the table; the survivor is the control); `hook_signal|_hook_signals` over
the package outside tests -i (writers + `report_facts.py`, `log_append.py`; the control is the known writer `hooklib.py:2528`
found by the same call); Glob `scripts/*doctor*.py`: no file; `gate_override` over `scripts/*.py` (found
`stage_guard.py:948` and the registry rows, which is the road A5b relies on).
Not read: `factory-rules.md` full text (index only, loaded in session) — the builder reads it whole (given);
`docs/TESTING.md` (C-5 relies on the CLAUDE.md summary); `hooks/codex.json`, `session_identity.py`,
`references/session-identity.json` (given; the critic's claims resting on them — receipts about 145 — were not load-bearing
for any edit here beyond F-2, so not re-read); `host_capabilities.py` (t-216's 121 taken as reported); `waiver.py` CLI body
(the record shape is left for the builder to read, named in given).
Needed beyond the manifest: `waiver.py`, `stage_guard.py`, `contract.py`, `refusal_registry.py`, `inject_context.py`,
`native_context.py`, `test_codex_host.py`, `test_test_locations.py`, `test-layers.json`, `hooklib.py`.

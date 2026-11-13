# t-212 — critic on the PLAN t-203 (native context on a long project root)

Reviewer: critic (Opus), 12.11.2026. Subject: `docs/tasks/specs/t-203-native-context-long-root.md` (designer draft t-203),
nodes OH3-36 (onboarding-forge/1), OH5-10, OH5-11, OH5-13 F3 (onboarding-hooks/5). Code base checked: `main` (carries
batches 1-3 and 5), `ai-packages/qa-factory/scripts/`.

**Verdict: GO-WITH-FIXES.** The core of the plan (refuse on the write's own `OSError`, inside `dispatch`, through `block`,
with an A24 row, a denial line and a census row) is sound and fits AR-9/AR-25/AR-28. One finding blocks dispatch as
written: **the D1 shortening (NAME_HEX 32 -> 16, limit 119 -> 151) opens a window where the launch passes the new gate
and then starts without context anyway**, because the next write on the same delivery chain (the host-dispatch binding
receipt, written inside `deliver` before the context is output) still fails above a root of 119. Fix it in the spec
(edits in §5 below), then dispatch. The Lead's interim "take every recommendation" can't apply to F-1 (it belongs to
the owner) or to F-4 (Part A gives no instruction for it); see §3.

## 1. Facts (key 1): checked against code

| claim in the spec | result | trail |
|---|---|---|
| rename done; `NAME_HEX = 32`, `PACKET_ROOT_LIMIT = 119` | true | `native_context.py:9`, `:13`; arithmetic comment `:10-12` |
| the 56-character root now writes | true | `test_doctor_context.py:162-167` (`old_root = 260-33-(64+1+64+5+37)` = 56) |
| `atomic_json` is not in `hooklib.py`; it is `event_store.atomic_json` -> `_publish`, temp `<name>.<uuid4 hex>.tmp` | true | `event_store.py:135`, `:162-174` (`:166` temp name); Grep `atomic_json\|uuid` in `hooklib.py`: no match; same call finds `def artifacts_dir` `:239` |
| `dispatch` catches only `ValueError` around `stage`; `OSError` escapes to `main`, signal + exit 0 | true (the signal is `person_signal`, which writes a `hook_signal` line) | `inject_context.py:651-655`, `:478-487`; `hooklib.py:2513-2530` |
| `StateConflict` is a `ValueError` | true | `event_store.py:19` |
| `LockBroken` is an `OSError` | true; also `LockBusy` is a `TimeoutError` (an `OSError`), but `EventStore.lock` turns it into `StateConflict` (`event_store.py:553-555`), so it stays on the `ValueError` road | `event_store.py:226`, `:249`, `:539-559` |
| `refusal_registry.SCANNED`, key = source of first arg | true | `refusal_registry.py:56`, `_key_text :812-828` (prefix `NATIVE_PACKET_UNWRITTEN` matches `NATIVE_PACKET_UNWRITTEN.format(...)`, like `CONFIG_WRITE_MSG.format(what=what)` `:343`) |
| `pending_path` callers: tests only (7/7/2) | true | Grep `pending_path` over `scripts/`: only `native_context.py:56` outside tests (the `cost_capture._pending_path` hits are another function); counts 7/7/2 |
| `worker_lifecycle` copy `:93-95`; `_blocking_text :119`, `note_unlaunched_denial :160` without `root` | true, but **incomplete**: a third site, `guard`'s stop branch `:214`, does the same (F5) | `worker_lifecycle.py:94-95`, `:119`, `:160`, `:206-214` |
| `test_codex_host.py:348-349` literal 32 | true | read |
| census `collect_blocks` row with 13 roles; `stage` row `:571` | true | `judgment-census.json:419`, `:571`, ratchet `:4` |
| test-layers rows | true for Part A; for Part B `test_resolver.py` does NOT cover `worker_lifecycle.py` (only `test_words_doors.py` does) | `test-layers.json:4319-4350`; JSON walk: `/keep/test_words_doors.py` is the only row with `worker_lifecycle.py` |
| `host_dispatch` receipts: "name length not measured, report as an analog" | **wrong framing: measurable and load-bearing** (F1) | `host_dispatch.py:10-11` (`sha256(...).hexdigest()` = 64 hex), `:247`, `:270-282` |

## 2. Findings

### F1 — BLOCKER. D1's shortening does not raise the supported root: the binding receipt in `deliver` fails at the old limit, so 120..151 becomes a silent no-context launch again (I-A broken)

Surface: the writers on the native delivery chain (PreToolUse `stage` -> SubagentStart `deliver` -> `host_dispatch.record`).

- `native_context.deliver` (`:124-130`) calls `host_dispatch.record({... 'PostToolUse' ...})` **before** it rewrites the
  packet and before `context_output` (`:150-154`). `record` writes `binding_path(root, agent)` =
  `<root>\qa-factory\state\host-dispatches\<64 hex>.json` through `atomic_json` (`host_dispatch.py:11`, `:282`, and the
  new-receipt write after `:300`). Neither `deliver` nor `native_context.main` (`:157-161`) catches anything.
  `telemetry_hook` re-raises the target's exception (`telemetry_hook.py:163-177`). So the SubagentStart hook exits 1, the
  context is never output, the child starts without its rules, and the packet stays `pending`.
- Empirical (rule 13), real functions, string roots, + 37 for the temp name
  (script `C:\Users\i_mas\AppData\Local\Temp\claude\b3e3188b390a00d9\acb1ecf0-04a8-42f3-8bdd-f14a2dae87bf\scratchpad\lens.py`):
  ```
  119 packet named 259 unnamed 226 binding 259
  120 packet named 260 unnamed 227 binding 260
  151 packet named 291 unnamed 258 binding 291
  152 packet named 292 unnamed 259 binding 292
  ```
  Today the named packet and the binding cross 259 at the same root (120). By chance the current refusal point (119) is
  exactly where delivery also works. With `NAME_HEX = 16` the packet writes up to 151, the new gate lets the launch go,
  and from 120 to 151 delivery crashes. That is the defect this node exists to end, moved one hook later.
- Same root cause, already live today and not in the spec: **unnamed launches** (packet limit 152 today, 168 under D1)
  stage fine from 120 and then crash in `deliver` the same way. The A.6 row "root 152..168, unnamed launch -> writes" is
  decided wrong: the write succeeds, but the launch still goes ahead without context.
- Neighbouring classes on this surface: the deliver-side rewrite of the packet (`:153`): same length as the staged one,
  OK. Session receipts (`session_identity.write_receipt`, `pretool-<16>-<stem>.json` under `host-receipts`, swallowed):
  about 145, so a door that promises 151 would also land in the receipt-loss zone (F3). `note_denial`: about root+59,
  append, OK.
- Fix (edits E1-E3): drop the NAME_HEX shortening from t-203 (keep 32 / 119; the TEMPORAL row and A3's 32-hex
  extension go away). Close the deliver-side crash: a `record` failure in `deliver` must not drop the context silently
  (new fork F-7). The class-wide way to gain length is F-2 (the shared temp suffix, +24 for every writer, packet and
  binding alike), not one file's name.

### F2 — MAJOR. F-1 belongs to the owner, and the "unpassable" reason in A.3 is the wrong argument (P13, FR-4)

`unpassable_because: "a word cannot write the file"`: a person's word passing this refusal would not write the file. It
would accept an INFORMED launch without context, and FR-4 ("stops a silent pass, never an informed one") and P13 ("the
person's word takes the factory through any gate") speak to exactly that. Unpassable can still be the right answer, but
only with a true reason (for example: a role with no role file is not a factory role, and there is no carrier the hook
could read a word from on a ticketless probe launch), and the owner has to say it, because it narrows the owner's own
F-9/F-11 residual (`inject_context.py:462`). Refusing in the meantime is the safe, reversible default (a pass can be added
later, a silent run cannot be undone). Edit E4.

### F3 — MAJOR. The door's number is this file's limit, not the factory's supported root

`PATH_LIMIT_DOOR` tells the person to "move the project to a folder of at most {supported} characters". Under D1 that
is 151, while the binding receipt fails above 119 (F1) and session receipts are lost silently from about 145 (B-451 F3).
A person who follows the door to 150 gets a factory that still breaks. With E1 (keep 119) the packet limit and the
binding limit are the same number. The text should still say "at most N; shorter is safer" rather than present N as a
guarantee. Edit E5.

### F4 — MAJOR. F-4 "yes" has no executable instruction in Part A

A.1 item 6 says "`stage` and `deliver`: no change"; A.7 has no row for the signal; only A.6 says "plus F-4 signal if
taken". Taking F-4 on the recommendation would leave a Sonnet builder to invent the call site, the text, the
`once_key` scope (once per role per session hides a second ambiguity) and the assertion. Because F-7 already requires a
`deliver` edit, either write F-4 out next to it (site, text, once_key, the assertion at `test_codex_host.py:450-463`) or
set F-4 = later. Edit E6.

### F5 — MAJOR (class, sweep-the-artifact-first). Part B misses a third site in the same file and leaves the other copies unqueued

- `worker_lifecycle.guard`, stop branch `:206-214`: `artifacts_dir(task, event)` on a receipt read by
  `receipt_files(root)`. Same class as `_blocking_text`/`note_unlaunched_denial`, and not in Part B's list.
- The copy of `is_one_component` (shape `"/\\:"`), Grep over `scripts/`, case-insensitive, positive control
  `hooklib.py:236` found by the same call: `host_dispatch.py:21` (`controller_record`, a story ticket),
  `exit_gate.py:209`, `stage_guard.py:436`, `:643`, `:717` (story names/tickets), `activity_capture.py:44`,
  `cost_capture.py:1907`, `:3800` (session ids; the same one-component rule). Part B only puts "the grep in the report".
  Per rule 9 each hit needs a verdict: fixed here, or queued with a pointer (OH5-12, or a new node in onboarding-hooks
  with axis 8 named). Edit E7.

### F6 — MINOR. Part B's test rows sit in a file whose layer row does not cover `worker_lifecycle.py`

B2-B4 test `worker_lifecycle`, but `test-layers.json` `test_resolver.py` `covers` has no `worker_lifecycle.py`. A later
edit to `worker_lifecycle` would never run these rows (`--witness-for scripts/worker_lifecycle.py` names only
`test_words_doors.py` plus the scenarios, as rerun). Either add `worker_lifecycle.py` to that `covers` (and
`test-layers.json` to Part B's owns), or put B2-B4 in `test_words_doors.py`. Edit E8.

### F7 — MINOR. `extended` reads the raw root string

`str(root).startswith("\\\\?\\")` misses `//?/C:/...` (Windows `Path` normalises it to `\\?\`). Test the normalised
string, `str(_slot(root, session, task_name))`, which `write_path_length` already builds. A4 gets one row
`extended_forward_slash` (platform nt; on POSIX hosts that row is skipped or uses a pre-normalised string). Edit E9.

### F8 — MINOR (code quality). `refuse_native_packet` formats the message twice

A.2.2 builds `text` and then repeats the same `.format(...)` inside `block(...)` so that the A24 key matches. The key only
reads the source of the first argument, so build the fields once (`parts = dict(role=..., cause=..., door=...)`) and
call `block(NATIVE_PACKET_UNWRITTEN.format(**parts))`, with `note_denial(..., NATIVE_PACKET_UNWRITTEN.format(**parts))`
before it. Both say one thing and the key is unchanged.

### F9 — NOTE. The registry row's slot differs from the precedent it cites

`PT-git-config` (`refusal_registry.py:335-341`) puts "the person changes their own machine" in `override`. A.3 puts the
person's moves in `unpassable_because` with `override: ""`. By the registry's own docstring (`:21-25`: `override` = a
person's WORD passing), A.3's slot is the more honest one. Fine as written, but don't cite PT-git-config as the model
for it. No blocking edit.

### F10 — NOTE (cost). Part B's witness is about 80 files

`--witness-for scripts/hooklib.py ...` prints 82 lines (keep rows of every hooklib reader) plus "run the whole scenario
layer" for `scripts/tests/test_resolver.py` (rerun below). Part A prints the same instruction for its test files and for
the changelog fragment. This is the rule's own output, so it is not a spec defect, but the Lead should expect it at
dispatch.

## 3. Forks (key 6)

| fork | designer | critic verdict |
|---|---|---|
| F-1 | refuse, unpassable | **For the owner, not the Lead.** The build may go ahead on (a) refuse as the reversible default, marked "по рекомендации, до слова владельца". Ask the owner two plain questions: does the F-9/F-11 residual cover the native packet write, and may a person's recorded word let a role start without its context? Rewrite the unpassable reason (F2). Not a dead end under FR-57: the length cause has two real exits owned by the person (move the folder, long paths), and the write-error cause has relaunch-then-blocker, so the person can fix the disk or permissions |
| F-2 | separate node | **Agree, and it is the class-wide fix that D1 is not**: +24 for every `_publish` writer (packet, binding, session receipts). For that node: open the temp in `"x"` mode so that a 32-bit collision fails instead of interleaving; update the N8a golden row. Recommend it in onboarding-hooks/5 next to OH5-13, with the binding limit named |
| F-3 | offer long paths | **Agree, with a caveat in the text**: it is the person's own machine (admin right, machine-wide). P25 covers model host/gateway settings, not an OS capability, so offering it is not proposing a cost cure. The door says "if you can and want to" and doesn't promise that every other tool follows |
| F-4 | yes, now | **Not executable as written** (F4). Either write it out inside the F-7 `deliver` edit, or later. Lean: write it out, since the file and the writer are the same |
| F-5 | keep `pending_path` | **Agree**: removal moves 14 test sites onto a private helper. OH5-11 closes on the `worker_lifecycle` copy plus F5's queue |
| F-6 | later | **Agree**. A `StateConflict` denial row could make `recover` close a live pending launch. A finding in onboarding-hooks, named |
| **F-7 (new)** | — | A `record` (binding) failure inside `deliver`: (a) catch `OSError`, still output the context, leave `person_signal(event, "inject", <the binding receipt could not be written: the duplicate-spawn guard and recovery cannot see this worker; cause>)`; or (b) catch, output nothing, signal. Critic leans (a): the role runs with its rules, and the blind duplicate guard is named rather than silent. Under E1 this only happens for unnamed launches at 120..152 and for non-length write errors. It is the Lead's call; the spec must state the choice, the text and a test row (an `OSError` from a patched `host_dispatch.record` -> the context is on stdout and the signal is written) |

## 4. Edges, parts, class, standing questions

- **Edges (key 3).** At the limit: "at_limit FNF -> write_error" is right (259 is not over), and with E1 the numbers
  become 119/120. Over the limit: right for named launches; wrong for unnamed ones (F1). `\\?\`: decided right, F7
  aside. UNC: counted as the string it is, right. Non-Windows: one road (any `OSError` -> refusal), with only the cause
  text read from a platform row. P31-clean: no exclusion, the shared mechanism is still reached. A POSIX `ENAMETOOLONG`
  gets the "relaunch once" door, which can't help, but the 75-character name component makes it unreachable in
  practice. Acceptable, noted.
- **Parts (key 4).** The owns are disjoint (A: `native_context`, `inject_context`, `refusal_registry`, two tests, census,
  changelog; B: `hooklib (artifacts_dir)`, `worker_lifecycle`, `test_resolver`). F7 adds `native_context` work to A
  only. `hooklib` is limited to one named function, OK. A Sonnet builder can execute both parts after E1-E9. Without
  them, F-4 and F-7 make it invent things.
- **Class (key 5).** No `SIBLING_MAP` axis covers "a factory write whose full path can exceed the Windows limit". The
  native chain is walked above (packet, binding, deliver rewrite, session receipts, denial). Beyond the map: **request
  to the coordinator for a scout**: list every `_publish`/`atomic_json`/`open(..., "w")` writer under `qa-factory/`
  with its longest relative path (story ticket length included), to set one supported-root number and decide whether
  this becomes a new axis (rule 9: a new symmetry is a new axis, same commit).
- **DUPLICATION AND CONSISTENCY:** found: F5 (eight more copies of the one-component check, grep with control above),
  F8 (double format). The new refusal helper sits beside `refuse_receipt`, same shape, no duplication.
- **CODE QUALITY:** F8 only. `unwritten_facts` is pure and never raises, and the A4 table is one parameterised test. Fine.
- **ONE ROAD (P31):** no exclusion. `PATH_LIMITS` selects text, not behaviour. The extended-path case still goes
  through the same refusal road.
- **ARCHITECTURE:** AR-9/AR-25/AR-28/AR-29/AR-20 named, with change checks. The spec claims AR-28, but under D1 it
  would break at the next boundary (F1). AR-1/FR-13: `PATH_LIMITS` in code is defensible (environment, not project
  variety; precedent `event_store` Windows codes 5/32 in code), and FR walk C has to say so in the report.
- **JUDGMENT:** the new unit judges presence (shape). No role judgment moves into code.

## 5. Minimal edits to the spec

- **E1 (F1).** §2 D1: drop "Shorter". `NAME_HEX` stays 32, `PACKET_ROOT_LIMIT` stays 119. Add the reason: the binding
  receipt (`host_dispatch.binding_path`, 64 hex) crosses 259 at the same root, so a shorter packet name only moves the
  failure into `deliver`. A.1 items 1-2: keep `TEMP_NAME_EXTRA`, no rename, no `_slot` docstring change. A.5: the numbers
  become "up to 119 (unchanged)". A.6: delete the TEMPORAL row and the "152..168 unnamed" row, and add the unnamed
  120..152 row pointing to F-7. A.7 A1: L in (119, 120), `L + 140`; unnamed `write_path_length(root_152, 's') == 259`.
  A3: no 32-hex extension needed. A4: 151/152 -> 119/120, `unnamed_153`. Drop the `test_codex_host.py :348-349` edit
  (Part A owns keep the file for F-7/F-4).
- **E2 (F1).** §0 add fact 9: `deliver` calls `host_dispatch.record` before `context_output`, and the binding name is
  64 hex, so its limit is root 119 (the measurement above). §3 siblings: replace "name length not measured" with that
  measurement.
- **E3 (F1, F-7).** Add A.1 item 7: the `deliver` change for F-7 as chosen (site: around the `record(...)` call at
  `:124-130`; text; signal kind `inject`; `once_key`). Add A.7 row A8: patch `host_dispatch.record` to raise `OSError`,
  run `deliver` for one pending packet, then (a) the context is on stdout, the signal is written, and the packet is
  `delivered`; or the agreed variant (b).
- **E4 (F2).** A.3 `unpassable_because`: replace "a word cannot write the file" with the true reason, marked "по
  рекомендации, до слова владельца (F-1)". §6 F-1: two plain questions for the owner, as in §3.
- **E5 (F3).** `PATH_LIMIT_DOOR`: "... move the project to a folder of at most {supported} characters (shorter is
  safer) ...". Long paths are worded per F-3: "if you can and want to".
- **E6 (F4).** Either write F-4 out inside E3 (site, text, `once_key` = per role and per pending-name set, not per role
  alone; the assertion at `test_codex_host.py:450-463`) or set F-4 = later and delete the A.6 mention.
- **E7 (F5).** Part B behaviour item 3: add `guard` stop branch `:214` -> `artifacts_dir(task, event, root=root)`, with
  a B3-like row. Part B handoff: each grep hit (list in F5) gets "fixed / queued -> <node>". The Lead names the node
  (OH5-12 or new) in the spec before dispatch.
- **E8 (F6).** Part B owns: add `<WT>\ai-packages\qa-factory\scripts\tests\test-layers.json` (only `worker_lifecycle.py`
  in `test_resolver.py` `covers`), or move B2-B4 to `test_words_doors.py`.
- **E9 (F7, F8).** A.1.5 `extended` on `str(_slot(...))`; A4 adds `extended_forward_slash`. A.2.2: format once,
  `block(NATIVE_PACKET_UNWRITTEN.format(**parts))`.

The decision to accept the plan, and which forks to take, belongs to the Lead. F-1 belongs to the owner.

## 6. Trail

Read: the spec (whole); `native_context.py` 1-161; `inject_context.py` 300-372, 436-500, 535-560, 600-680 (+ Grep
of defs/imports); `event_store.py` 130-180, 225-270, 442-471, 539-564; `hooklib.py` 228-250, 645-660, 810-830, 2513-2535;
`worker_lifecycle.py` 80-240; `host_dispatch.py` 1-30, 228-300; `host_probe.py` 497-522; `telemetry_hook.py` 118-182;
`session_identity.py` 150-210; `refusal_registry.py` 1-70, 318-345, 812-840; `test_doctor_context.py` 20-186;
`test_codex_host.py` 340-352, 440-470; `test-layers.json` 4319-4350 (+ JSON walk for `worker_lifecycle.py`);
`judgment-census.json` :4, :419, :571; `hooks/codex.json` :139-140 (Grep); `docs/SIBLING_MAP.md` axes 8, 29, 34 and the
heading list; findings `20261030-windows-260-...` (whole), B-451 (Grep); `plans/PILES.md` rows 86-93;
`references/session-identity.json:3`; `tools/critic_verdict.schema.json`; `docs/tasks/critic-diff-brief.md` headings.
Greps with controls: the `"/\\:"` shape over `scripts/*.py` -i (control `hooklib.py:236` found); `class ...(OSError.*ValueError | TimeoutError)` -i (only `LockBusy`, which proves the pattern runs); `pending_path` over `scripts/`.
Reruns: `lens.py` (output in F1); `scenario_walk.py --witness-for` for Part A's owns and Part B's owns (outputs
summarised in F6/F10). Not read: `factory-rules.md` full text (index only); `docs/TESTING.md`.
Needed beyond the manifest: `host_dispatch.py`, `telemetry_hook.py`, `hooks/codex.json`, `session_identity.py`,
`references/session-identity.json`.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "F1: NAME_HEX 32->16 raises the packet limit to 151 but host_dispatch.record writes a 64-hex binding receipt inside deliver before context_output, failing above root 119; 120..151 becomes a launch that passes the new gate and starts without context (measured: root 151 -> binding path 291). Unnamed launches already hit this at 120..152 today."
  ],
  "class_completeness": "No SIBLING_MAP axis covers writes that exceed the Windows path limit. The native chain was walked by hand: packet, binding receipt (breaks D1), deliver rewrite (ok), session receipts (~145), note_denial (ok). Part B misses worker_lifecycle.guard :214 and leaves 8 copies of the one-component check unqueued (host_dispatch:21, exit_gate:209, stage_guard:436/643/717, activity_capture:44, cost_capture:1907/3800). Requested from the coordinator: a scout census of every qa-factory writer's longest relative path, to set one supported-root number and decide on a new axis.",
  "fixes": [
    "E1 drop the NAME_HEX shortening: keep 32 and 119, delete the TEMPORAL and unnamed-168 rows, renumber A1/A4",
    "E2 add the binding-receipt measurement as fact 9 and in the siblings line",
    "E3 add F-7: deliver handles an OSError from host_dispatch.record (lean: still output the context and leave a person_signal), plus test row A8",
    "E4 rewrite unpassable_because with a true reason, marked pending the owner's word; F-1 asked to the owner in plain words",
    "E5 door text: at most N, shorter is safer; long paths offered as optional",
    "E6 write F-4 out fully inside the deliver edit, or set it to later",
    "E7 Part B adds guard stop branch :214 and gives each one-component copy a fixed or queued verdict",
    "E8 Part B adds test-layers.json covers worker_lifecycle.py for test_resolver.py, or moves B2-B4 to test_words_doors.py",
    "E9 extended check on the normalised slot string; refuse_native_packet formats once"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/t-203-native-context-long-root.md",
      "ai-packages/qa-factory/scripts/native_context.py",
      "ai-packages/qa-factory/scripts/inject_context.py",
      "ai-packages/qa-factory/scripts/event_store.py",
      "ai-packages/qa-factory/scripts/hooklib.py",
      "ai-packages/qa-factory/scripts/worker_lifecycle.py",
      "ai-packages/qa-factory/scripts/host_dispatch.py",
      "ai-packages/qa-factory/scripts/host_probe.py",
      "ai-packages/qa-factory/scripts/telemetry_hook.py",
      "ai-packages/qa-factory/scripts/session_identity.py",
      "ai-packages/qa-factory/scripts/refusal_registry.py",
      "ai-packages/qa-factory/scripts/tests/test_doctor_context.py",
      "ai-packages/qa-factory/scripts/tests/test_codex_host.py",
      "ai-packages/qa-factory/scripts/tests/test-layers.json",
      "ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json",
      "ai-packages/qa-factory/hooks/codex.json",
      "docs/SIBLING_MAP.md",
      "plans/piles/onboarding-forge/findings/20261030-windows-260-codex-dispatch-bez-konteksta.md",
      "plans/piles/onboarding-hooks/findings/B-451-b-410-identichnost-sessii-ostatki.md",
      "plans/PILES.md"
    ],
    "reruns": [
      {"command": "python -B scratchpad/lens.py (real _slot and binding_path, string roots, +37 temp)", "result": "119: packet 259, binding 259; 120: 260/260; 151: packet 291, unnamed 258, binding 291; 152: 292/259/292"},
      {"command": "scenario_walk.py --witness-for <Part A owns>", "result": "keep rows for native_context/inject_context/refusal_registry plus 'run the whole scenario layer' for the test files and changelog"},
      {"command": "scenario_walk.py --witness-for <Part B owns>", "result": "82 lines; worker_lifecycle.py covered only by test_words_doors.py plus scenarios; whole scenario layer for test_resolver.py"}
    ]
  }
}
```

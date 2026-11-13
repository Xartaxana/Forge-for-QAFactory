# Wave 0, part 3 — item 11: command rows per conductor move, and the F16 contradiction check

Draft by the designer, 2026-11-13, task t-489. Continues `20261113-told-before-work-wave0-rows.md` (part 1) item 11
in the SAME row form (part 1 §0). Parent spec: `20261113-told-before-work-mechanism-spec.md` (§2.2, §2.8, §2.9, §5.5,
fork F16 decided (a)). Package code read ONLY from
`C:\QAFactory\forge-repo\.claude\worktrees\read-main\ai-packages\qa-factory\` (origin/main); file:line below are of
that tree, paths package-relative. Forks are RETURNED, never decided. Contradictions are NAMED, not resolved.

Binding (F16 (a)): `precondition` / `forbidden_when` of a move stay move data the conductor judges; a command row states
only what the COMMAND refuses. Every row: `roles: ["conductor"]`, `stages: ["*"]`, `door_needs: none` (§5.5 header;
small choice S-P1). Refusals that are states of the story (or of the stand, or of the plugin's own data) rather than of
the call (FR-46) are listed apart as "story-state refusals", one line each, never folded into a call row.

---

## 1. Rows

### 1.1 `controller:rework` — `controller.py --operation rework` (move `rework_stage`, conductor-actions.json :66-79)

Road: `main` :9848-9877 (story root, words) → `build_rework_request` :3652-3897 (refusals collected, `_raise_all`
:3824) → `apply("dispatch", request)` :9943 → `apply` :4998-5167 → `validate` dispatch branch :5440-5721.

| check | roles | when | requirement | door | door_needs | sites | status |
|---|---|---|---|---|---|---|---|
| `controller:rework.call` | conductor | `move:rework_stage` | The call names an existing story folder by `--task-root` (exact name) that holds the story journal, and gives the person's words either inline as `--reason` or as `--words-file` (never both); a words file exists, is not a folder, is UTF-8 text and is not empty. | fix the option the refusal names and run the same command again | none | `_cli_story_root` :9636-9683 (folder / operation parts); :9874-9877; `person_words.read` :136-156, `_from_file` :77-113 | drafted |
| `controller:rework.args` | conductor | `move:rework_stage` | `--stage` is one of S0-S9; `--purpose` is one of PURPOSES; the reason (the words) is not blank; `--cause` is one of REPAIR_CAUSES; from S4 on `--cases` names at least one case and every case is inside the approved scope; every `--rows` id is a row of the approved plan; the role has an ACCEPTED dispatch on that stage (on S5: of the kind the purpose names, the plan for `s5_plan`, else a window); on S5 the cases of a code-typed reason lie in ONE window (a person's words over several windows are not refused). | take the values from `controller.py --operation stage-scope` and the accepted roles the refusal lists; one window's cases per call | none | `build_rework_request` :3674-3696, :3718-3755, :3756-3804, :3813-3824 (`_noted` :6136-6140, `_raise_all` :6093-6110) | drafted |
| `controller:rework.runner_half` | conductor | `move:rework_stage` | On a new-mode story, a qa-runner rework names the cases of ONE runner half: all manual-agent or all automated in the approved plan, none outside both halves; when the plan derives no scope, one half of the accepted runner records holds every case. | rework each half by its own cases (the command the refusal prints) | none | `_rework_kind` :3934-3972; :3761-3770 | drafted (half-kind part) |
| `controller:rework.runner_half.manual_block` | — | — | — | — | — | `_rework_block_problems` :3920-3932 → `manual_block_problems`, `_half_membership_problems` | not drafted -- body of `manual_block_problems` / `_half_membership_problems` not read |
| `controller:rework.cap` | conductor | `move:rework_stage` | A test_defect round of a repair-loop role past its repair cap on the window is dispatched only after the person's recorded pass for that role's round, the exact text the refusal prints first on its line (`round pass <n> for <role> on S<n>:<hash>`); a mechanical round past the mechanical cap, or a mechanical round for a role that is not the author, only after the pass of that mechanical round (`mechanical pass <n> for <role> on S<n>:<hash>`). | record the pass(es) the refusal prints with `waiver.py --task <T> --stage S<n> --block "<pass>" --words-file <file>`, only on the person's words that ask for one more round (the refusal prints one command per role) | none | `validate` :5577-5638; `repair_pass_key` :740-751, `repair_passes` :754-767, `mechanical_pass_key` :770-777, `repair_doors` :786-789; `_passed_by_person` :2417-2429 → `waiver.split_overridden` :202-222 | drafted (see fork F-P3) |

Helpers on the road whose bodies were NOT read (each may print further call refusals; none guessed):
`validate_record("Dispatch", p)` :5441; `_window_beside_running` :5449; `runner_kind_required` / `validate_manual_runner_block`
:5477-5488; `_validate_rerun_after` :5519-5520 (a person's-words rework carries `rerun_after`, :3889-3892);
`_validate_gate_a_content_current` :5527; `_s5_plan_problems` :5658; `_hold_dispatch_refusal` :5718;
`stage_guard_errors` :5719-5721; `_outside_approved` / `_scope_door` (text of the scope refusal); `_closed_dispatch_refusal`
helpers `_left_held_refusal`, `_executing_refusal`, `_closed_story_doors`; `event_store.commit` (revision / idempotency).
Status of these: **not drafted -- body not read**. The rows above cover every refusal of `main`, `build_rework_request`,
`apply` and the `validate` dispatch branch whose condition was read whole.

Story-state refusals of `controller:rework` (FR-46; one line each, no call row):
- S-R1 held for code from S<n>: a rework of a stage the hold keeps closed — :3708-3710 (StateConflict; doors arrive/stop/rework printed).
- S-R2 stopped while waiting for code, reason typed by code — :3711-3717 (door: `--words-file` with the person's words).
- S-R3 closed story and a blank reason — :3686-3692 (the words reopen it; covered by `.args` "reason not blank", the text differs).
- S-R4 the role's dispatch on the stage is live, not accepted — :3793-3800 (doors: driver resume; `release` then `next`).
- S-R5 another dispatch is running (sequential task) — :5448-5461 (door: `story_step.py finish`; the S5 critic `--needs-author` door).
- S-R6 the dispatch id already exists — :5472-5473.
- S-R7 qa-case-critic after a current gate A — :5474-5475 (`CASE_REVIEW_AFTER_GATE_A`).
- S-R8 packet checkpoint threshold reached — :5489-5493; cumulative packet budget reached — :5494-5502.
- S-R9 a prior stage is not completed — :5515-5518; the current gate decision (A for S5-S8, B for S9) is missing — :5521-5525.
- S-R10 scope expansion / review scope does not hold yet — :5528-5542.
- S-R11 closed story without a person's reopening on the event — :5468-5470, `_closed_dispatch_refusal` :8125-8162 (body read; its door helpers not read).
- S-R12 an orchestrator lease exists and the request carries no matching `owner_session_id` — `apply` :5010-5012. `build_rework_request` never sets `owner_session_id` (:3843-3897), so with a lease every rework meets this refusal (observation O-4).
- S-R13 idempotency key reused with different inputs — :5138-5163.
- S-R14 no story journal ("initialize task before work") — :9678-9682; the folder holds neither journal nor pipeline.json — :9673-9677.

### 1.2 `controller:release` — `controller.py --operation release --dispatch <id> --words-file <file>` (move `release_and_restart`, :112-125)

Road: `main` :9848-9861 → `release_dispatch` :8069-8117 (no `apply`: commits with `store.commit` :8109).

| check | roles | when | requirement | door | door_needs | sites | status |
|---|---|---|---|---|---|---|---|
| `controller:release.call` | conductor | `move:release_and_restart` | The call names an existing story folder that holds the journal; the person's words come either as `--words` or as `--words-file` (never both), a words file being an existing, UTF-8, non-empty file, and the words are not blank; `--dispatch` names a dispatch of this story (it may be left out only when exactly one dispatch is open, and the refusal lists the open ones). | pass `--dispatch <id>` from the ids the refusal lists, or the words file the refusal names | none | `_cli_story_root` :9636-9683; :9857-9861; `person_words.read` :136-156, `_from_file` :77-113; `release_dispatch` :8077-8098; `_unknown_dispatch` :6149-6152 | drafted |
| `controller:release.commit` | — | — | — | — | — | `self.store.commit("release", …)` :8109-8111 (event_store) | not drafted -- body of `event_store.commit` not read |

Story-state refusals of `controller:release`:
- S-L1 the dispatch's status is none of running, blocked, paused, incomplete, `returned_unaccepted`, abandoned ("holds nothing back") — :8099-8101 (StateConflict). The text names the releasable statuses but no door (fork F-P2).
- S-L2 no story journal / not a story folder — :9673-9682.

### 1.3 `waiver:block` — `waiver.py --task --stage --block … --words-file` / `--remark` (move `go_on_as_is`, :127-140)

Road: `main` :1572-1660 → `run_stage` :990-1050 (`record_refusals` :905-936, `block_standing` :674-707,
`_held_against_record` :710-733, `unmatched_text` :745-761) / `run_remark` :1221-1248.

| check | roles | when | requirement | door | door_needs | sites | status |
|---|---|---|---|---|---|---|---|
| `waiver:block.call` | conductor | `move:go_on_as_is` | The block form gives `--task`, `--stage`, `--block` and the person's words, as `--decision` or as `--words-file` (never both); a words file is an existing, UTF-8, non-empty file; inline words never arrive through run-py.cmd. | give the missing option; write the words to a file and pass `--words-file <file>` | none | :1632-1642, :1653-1656; `person_words.read` :136-156, `_from_file` :77-113 | drafted |
| `waiver:block.placeholder` | conductor | `move:go_on_as_is` | The block names a real value, never a form's `<placeholder>` (`probe gap: <case key>`, `RP-<profile>`); `*`, `stand gap:` and `protected test path:` blocks have their own rules. | record again with the real value in its place; words that name nothing the check shows are kept with `--remark` | none | `record_refusals` :914-935, `PLACEHOLDER_RE` :119 | drafted |
| `waiver:block.stand_gap_id` | conductor | `move:go_on_as_is` | A `stand gap:` block names the card's id after the prefix (a precondition id such as PC-1, a case key such as TC-7, or `RP-<profile>`). | record again with `--block "stand gap: <id>"`, the words file starting with the answer word | none | `NO_GAP_ID` :897-902, :920-921 | drafted |
| `waiver:block.grant_pattern` | conductor | `move:go_on_as_is` | A `protected test path: <pattern>` block holds a well-formed pattern that lies inside a protected folder, does not open the protected folder itself or the folder that holds it, does not start with a wildcard folder outside the protected roots, and is not a bare file name in the application root. | write the pattern the refusal asks for | none | :922-924; `test_path_grants._judge` :112-143, `pattern_errors` :146-149 (texts of BAD_PATTERN, OPENS_BOUNDARY, FIRST_FOLDER_WILDCARD, FILES_IN_APP_ROOT, OUTSIDE_ROOTS: constants not read) | drafted (condition read; constant texts not read) |
| `waiver:block.standing` | conductor | `move:go_on_as_is` | When the driver's record of the refusal standing at this stage holds lines or doors, the block is one of: every part of it named by whole words in a line of that record (a whole line matches itself), a block name the refusal printed in its own door, `*`, a block the dispatch guard refuses on, a block of the factory's own form (`stand gap: <id>`, `protected test path: <p>`, the release blocks, the four own constants), or a block name of `references/block-names.json` for this stage. With no such record the block is recorded and reported `not verified`. | `--block` set to one of the lines or door names the refusal lists, whole or by whole words that line contains; words that pass none of them are kept with `waiver.py --task <T> --remark --stage <S> --words-file <file>` | none | `block_standing` :674-707, `_held_against_record` :710-733, `_carrier_hits` :662-671, `refusal_parts` :438-452, `_is_own_form` :629-635, `block_name_row` :595-614, `unmatched_text` :745-761, `read_standing` :467-489; `references/block-names.json` | drafted |
| `waiver:remark.call` | conductor | `move:go_on_as_is` | The remark form gives `--task`, `--stage` and the person's words, as `--text` or as `--words-file` (never both). | give the missing option | none | :1644-1646, :1638-1642 | drafted |

Not reached by the move's run, no row: `--why-person` refusals :1543-1558, :1608-1610 (the run never passes it);
`--revoke`, `--gate` forms (other moves / actions).

Story-state refusals of `waiver:block` (and data-state, FR-46):
- S-W1 no `pipeline.json` for the story (exit 4) — :1003-1006 (block), :1229-1232 (remark). No door in the text (fork F-P2).
- S-W2 the project is not onboarded (`require_project`, exit `EXIT_NO_PROJECT`) — :991, :1222; `hooklib.require_project_at` :219-231.
- S-W3 data-state: `references/block-names.json` cannot be trusted where the verdict would rest on it — :1009-1016, `load_block_names` :573-592, :705-706 (door printed: `--remark`).

### 1.4 `waiver:carry` — `waiver.py --carry-from <old key> --task <new key>` (conductor-actions.json `actions` row `words_carry`, :25)

Road: `main` :1608-1625 → `run_carry` :1140-1218 (`_carry_overrides` :1063-1102, `_carry_gap_classes` :1105-1137).

**`when` is illegal as asked**: `words_carry` is an `actions` row, not a `moves` row; `when: move:<id>` must be a
`moves[].id` read through `no_move.move_ids` (`no_move.py` :60-67 reads only `spec["moves"]`; spec §2.2). Rows below
carry `when: move:words_carry` PENDING fork F-P1.

| check | roles | when | requirement | door | door_needs | sites | status |
|---|---|---|---|---|---|---|---|
| `waiver:carry.call` | conductor | `move:words_carry` (F-P1) | `--carry-from` is a form of its own: it goes with `--task` and optionally `--carry-from-root`, and with none of `--stage`, `--block`, `--revoke`, `--remark`, `--gate`, `--requirement`, `--decision`, `--text`, `--words-file`, `--list`, `--json`, `--why-person`; `--carry-from-root` only with `--carry-from`. | `waiver.py --carry-from <old key> [--carry-from-root <folder>] --task <new key>` | none | :1608-1610, :1613-1624 | drafted |
| `waiver:carry.old_key` | conductor | `move:words_carry` (F-P1) | The old key is the name of one story folder (not empty, no blank at either end, no `..`, one path component), is not the new key, and is a story folder under the project's artifacts or under `--carry-from-root`, which must be a folder; that folder's `pipeline.json` reads as an object; `--task` is one path component. | name the earlier key as its folder is named; for a folder moved by hand, `--carry-from-root <folder>` | none | `run_carry` :1153-1170, :1179-1186 | drafted |

Story-state refusals of `waiver:carry`:
- S-C1 the new story has no `pipeline.json` (exit 4; door: run the story's S0 first) — :1173-1178.
- S-C2 `stage_overrides` of either story is present but not a list — :1187-1191.
- S-C3 the new story's `work/gap-classes.json` cannot be read — :1197-1201, :1131-1134.
- S-C4 the artifact root cannot be resolved (config) — :1171-1172.
- S-C5 the words could not be stored — :1205-1210.
- S-C6 the project is not onboarded — :1147.
Not refusals: `nothing to carry` (exit 0, :1202-1204); `not carried:` / `kept yours` / `already carried` lines (:1083-1101).

### 1.5 `stand_health:probe` — `stand_health.py --probe --env <name>` (move `stand_prepare`, :158-171)

**No row.** `main` :903-930 → `probe` :756-829, which "never raises" (catch-all :826-829). The command refuses
nothing of the call the move runs: the only argument refusal, `--probe, --status, --reset or --selftest is required`
(:930), cannot meet a call carrying `--probe`, which the move's run always does. Exit 1 (:923) means the stand is not
healthy — a measured state of the stand, not a refusal of the call (FR-46).

Story-state (stand-state) lines:
- S-H1 the stand is `down` / `degraded` / `not_configured` (exit 1; JSON `sentence` and `diagnosis.remedy`) — :776-780, :801-825, :826-829.
- Observation O-5: an `--env` name that matches no `environments[]` entry is neither refused nor noted in the lines read: `stand` stays None (:510-512) and the block's addresses are probed instead. Whether `env_probe.frontend_of` adds a note (:515-516) was not read.

### 1.6 `source_exclusions:revoke` — `source_exclusions.py --task <T> --revoke <X-id|as_written> --words "<words>"` (move `revoke_exclusion`, :172-187)

Road: `main` :604-691 → `revoke` :490-511 → `read_record` :294-321.

| check | roles | when | requirement | door | door_needs | sites | status |
|---|---|---|---|---|---|---|---|
| `source_exclusions:revoke.call` | conductor | `move:revoke_exclusion` | The call gives exactly one of `--load`, `--show`, `--revoke`, each option spelled whole; `--task` names an existing story folder (its exact name); `--revoke` carries `--words` with the person's words, not blank. | add the missing part the refusal names | none | :616-631, :662-665; `_task_root` :599-601 | drafted (`hooklib.exact_options` body not read: the abbreviation refusal text is argparse's) |
| `source_exclusions:revoke.target` | conductor | `move:revoke_exclusion` | The `--revoke` value names exactly ONE exclusion of the story's record, by its X-id or, failing that, by its `as_written` text (case apart); the refusal lists every id with its `as_written`. | name one X-id from the list the refusal prints | none | `revoke` :499-503; :671-674 | drafted |

Story-state refusals of `source_exclusions:revoke`:
- S-X1 the story has no record of sources left out (exit 2, "nothing to revoke") — :495-496, :667-670. No door (fork F-P2).
- S-X2 the record cannot be read or trusted (exit 3; door: restore it, or remove the file) — `read_record` :294-321, :686-688.
- S-X3 `ListRefused` (exit 3) — :689-691; its raise site on the revoke road (`revoke_marks`?) not read.
Not a refusal: `already revoked` (exit 0, :676-679).

---

## 2. F16 contradiction check — one line per move of conductor-actions.json

| move (line) | run command | verdict | quotes (move ↔ command) |
|---|---|---|---|
| rework_stage (:66) | `controller.py --operation rework` | **contradiction** (C-2, C-3, C-4); (ii) consistent on the controller side | see (ii), C-2, C-3, C-4 |
| approve_gate (:81) | nothing (driver) | consistent: no command | — |
| resume_with_words (:96) | nothing | consistent: no command | — |
| release_and_restart (:112) | `controller.py --operation release` | consistent | :119 "the dispatch is running, blocked, paused, incomplete, returned or abandoned" ↔ controller.py:8080 `releasable = {"running", "blocked", "paused", "incomplete", RETURNED, ABANDONED}` (RETURNED = `returned_unaccepted` :185). "the new session gets the person's words": could not establish from the command (the driver's relaunch) |
| go_on_as_is (:127) | `waiver.py --stage --block` / `--remark` | **contradiction** (C-1) — case (i) | see (i) |
| story_fact (:142) | `stage_done.py --set key=value` | consistent (with O-1 on part 1's row) | :150 "the value is named by a script or by the person" ↔ stage_done.py:128-135 refuses any key outside SETTABLE whoever named it ("A person's word does not widen this list"), :138-144 `retro_mode` numbers/skip; the move claims nothing the command contradicts |
| stand_prepare (:158) | project `bring_up`; `stand_health.py --probe --env` | consistent | :162 "checks that it answers" ↔ `probe` :756-829 measures; O-5 (unknown `--env` silent) is a command gap, not a contradiction of the move text |
| revoke_exclusion (:173) | `source_exclusions.py --revoke --words` | consistent | :179 `--revoke <X-id|as_written> --words "<their words, verbatim>"` ↔ :619-621, :499-503; :181 "after S1 completes the `exclusions` row of `actions` lists the door" ↔ :683-684 prints `_door` only when S1 is completed |
| person_does (:189) | nothing | consistent: no command | — |
| stop_here (:204) | nothing | consistent: no command | — |
| (words_carry, `actions` :25 — not a move) | `waiver.py --carry-from` | consistent | :25 "once S0 of the new key made its folder" ↔ waiver.py:1173-1178 refuses with no new `pipeline.json` and names S0; "Tell the person each `not carried:` line" ↔ :1087, :1097, :1129 print them |

### (i) go_on_as_is — does waiver.py accept exactly "one of the refusal's lines, whole, or a named block such as `probe gap: <case key>`" and "refuse anything else"?

**No — it accepts MORE, and in one respect the named example differs.** Contradiction **C-1**.

Move text, conductor-actions.json:132: `"<the block: one of the refusal's lines, whole, or a named block such as `probe gap: <case key>`; waiver.py refuses anything else>"`.

What `waiver.py` accepts without refusing (`run_stage` :990-1050):
1. a PART of a line: every part of the block named by whole words in a line of the record — `_carrier_hits` :662-671
   ("EVERY part of the block must pass some line"), and its own refusal says so: :755 "Expected: --block set to one of
   these lines, whole or by whole words only that line contains";
2. `*` — :722-723 "legal always (FR-4): it passes every line there is, and is never refused";
3. a door name the standing refusal printed — :724-725;
4. a block the dispatch guard refuses on — :718-720;
5. blocks of the factory's own form, never held against the record — `_is_own_form` :629-635: `stand gap: <id>`,
   `protected test path: <p>`, anything whose block OR WORDS contain `wait_existing_job` / `resume_checkpoint`
   (`_releases` :492-495, routed to `controller.py --operation release`, :1045-1047), and the four constants :371-375;
6. every name of `references/block-names.json` at its stages (14 rows) — `block_name_row` :595-614;
7. ANY block when the driver's record of that stage is absent, empty, of another stage or unreadable — kind `unknown`
   :730-733, recorded and printed `not verified` (:769-771, :793-810); waiver.py:44-46 states this temporal edge as
   designed.

What it refuses: a `<placeholder>` block (:927-935), a `stand gap:` with no id (:920-921), a bad grant pattern
(:922-924), a block in no line or door of a record that holds lines or doors (`unmatched` :1017-1019), and an
untrustworthy names table where the verdict would rest on it (:1009-1016).

Named example: the data row is `"block": "probe gap: <case key or tooling:language>"`
(references/block-names.json:21), read as a prefix needing ONE token (`contract.prefix_value` contract.py:120-131);
the move says `probe gap: <case key>`. The command accepts `probe gap: tooling:<language>` too.

So "waiver.py refuses anything else" (conductor-actions.json:132) contradicts waiver.py:722-723 (`*`), :662-671 (part
by whole words), :629-635 and :595-614 (own forms and names) and :730-733 (no record: anything). Not decided which side
is right.

Analog noticed (an `actions` row, out of the move scope): conductor-actions.json:35 "never a line of the refusal and
never `*`" for the probe-gap action — waiver.py accepts both (:722-723, :662-671); a probe-gap word recorded as `*`
would pass every line of S5 (`split_overridden` :217).

### (ii) rework_stage — does the rework operation match on the pass "as the refusal prints it"?

**Controller side: consistent.** Move precondition conductor-actions.json:73: "A test_defect round past the repair cap
first needs the pass of that round, as the refusal prints it, for BOTH roles (the author's and the critic's):
waiver.py --task <T> --stage S<n> --block \"<that pass>\" --words-file <file> once for each".
- The rework reaches the cap check: `main` :9943 `c.apply("dispatch", …)` → `validate` :5614-5638.
- The refused line starts with the asking role's pass, `passes[p['role']]` (:5622), built by `repair_pass_key`
  (:751) `f"{kind} pass {n} for {role} on {stage}:{hash12}"`; the door prints the passes of BOTH roles of the pair
  (`repair_passes` :754-767, `repair_doors` :786-789, :5634-5638 "one pass for each of the two roles, the author's and
  the critic's, from the same words").
- The check reads the recorded word by `_passed_by_person` :2417-2429 → `waiver.split_overridden` :202-222:
  `contract.names_whole(match, line)` — the printed pass, recorded whole, names the line whole → passes.
- The mechanical clause of :73 ("one past its cap, or for a role that is not the author, first needs the pass of that
  mechanical round, as the refusal prints it") ↔ :5586-5613 (`mechanical_pass_key` :770-777): consistent.

**Waiver side, the second (critic's) pass: could not establish.** The critic's pass is NOT in the refused line
(:5619-5620 "This role's pass opens the line, and only its own"); it appears only in the door. `waiver.py` accepts it
(a) as a door name when the driver's record carries the refusal's door names (`door_blocks` :455-464, kind `door`
:724-725), (b) as `unknown` with no record (:730-733), but (c) refuses it as `unmatched` when the record holds the line
and not the door names. Whether `Driver.standing_refusal` records the door names of this refusal was not read.
`refusal_parts` cuts only ONE trailing door (:447, `_DOOR_TAIL` :387), so with two doors joined by " and " the
author's door stays inside the recorded line text — no effect on the critic's key.

### Further contradictions found by the check (rework_stage)

- **C-2 (command accepts more).** Run text :71 `[--cases <ids> | --rows <ids>]` (one or the other) ↔
  `build_rework_request` :3718-3755, :3874-3877 accepts both together (no refusal). (`no_move.check_args` refuses both
  on the conductor's ANSWER, spec §5.5 `no_move:args` — not the command.)
- **C-3 (move forbids what the command designs as the person's door).** forbidden_when :74 "the story is closed" and
  precondition :73 "the story is open" ↔ controller.py:3685-3692 and :8014-8025: a rework of a closed story with the
  person's words REOPENS it (`reopened_at` + `reopen_words` on the event, admitted by `_closed_dispatch_refusal`
  :8155-8158); the refusal text itself names it a person's decision: "rework of a closed story REOPENS it — which is a
  person's decision, not the factory's. `--reason \"<their own words>\"` records it". The conductor reads both texts.
- **C-4 (could not establish, named).** forbidden_when :74 "S1-S4 once gate A is decided" and "a delivery attempt is
  recorded": in the lines read the command refuses only qa-case-critic after gate A (:5474-5475); whether
  `stage_guard_errors` (:5719) or `_validate_rerun_after` (:5519) refuse the rest was not read. Under F16 (a) a move
  stricter than its command is legal; listed so the Lead sees the command does not back the restriction in the lines read.

---

## 3. Forks (returned, not decided)

- **F-P1 — `words_carry` is no move.** `when: move:<id>` must be a `moves[].id` (§2.2; `no_move.move_ids` reads only
  `moves`, no_move.py:60-67); `words_carry` is an `actions` row (:25), so it is never in `open_ids` and no launch
  selects its rows. Options: (a) add a `moves` row `words_carry` (token `—`, `offerable: false`, `word: person`, run =
  the carry command), the same twin pattern as `exclusions` (action :24) + `revoke_exclusion` (move :172) — cost: one
  data row, price classes, the no_move tests that enumerate moves; (b) a `when` token `action:<id>` reading `actions`
  ids — a second road beside `move:` (P31 risk); (c) no launch row: `waiver:carry` units counted `conductor_only` in
  G-free with its reason (§2.8). **Recommend (a)**: one road (`move:`), precedent in the file, and the carry refusals get told.
- **F-P2 — door-less story-state refusals.** S-L1 (release of a dispatch that holds nothing back), S-W1 (no
  pipeline.json), S-X1 (no record of exclusions). Options: (a) keep them story-state lines with no row, and T9c's told
  text gives the conductor the general door "the move does not apply here — choose another open move"; (b) owe a door
  in each command's text (a code change, out of this wave). **Recommend (a)** now, (b) as a finding for the piles.
- **F-P3 — the cap as a command row.** `controller:rework.cap` restates the clause the move's precondition already
  carries (F16 (a) keeps that text as move data; J1 checks no contradiction). Options: (a) keep the row (the command
  refuses it and the conductor can meet it with the person's recorded words — the brief's rule "one row per requirement
  the caller can meet"); (b) story-state line only. **Recommend (a)**.

## 3a. Lead acceptance, 13.11.2026 (t-489) — forks decided, contradictions routed

Accepted as the input of T9c. **F-P1 (a)** a `moves` row `words_carry` (twin of `exclusions` / `revoke_exclusion`), one
road `move:`; **F-P2 (a)** story-state lines carry no row, T9c's told text gives the general door; the door each command
owes is a finding for the pile; **F-P3 (a)** the cap row stays. Rows marked "not drafted -- body not read"
(`controller:rework.runner_half.manual_block`, the 10 helper bodies of §1.1, `controller:release.commit`) are drafted by
T9c's builder from the bodies, each returned as a question if a sentence cannot be stated from the body read whole.

F16 contradictions (move text ↔ command), fixed as MOVE DATA in T9c, the command unchanged:
- C-1 `go_on_as_is`: the move text is made exact to what `waiver.py` accepts.
- C-2 `rework_stage`: the run text stops promising "one or the other" for `--cases` / `--rows`.
- C-3 `rework_stage`: "the story is closed" leaves `forbidden_when`; the move says a closed story is reworked only on the
  person's own words, which reopen it (the command's designed door, P13).
- C-4 could not be established: T9c's builder reads `stage_guard_errors` and `_validate_rerun_after` and reports.

Observations O-2 … O-6 are factory defects outside this mechanism and become findings of `live-run-fvf` (filed by the
Lead): O-3 first — `_releases` reads the person's WORDS for `wait_existing_job` / `resume_checkpoint` and skips the
standing check (a phrase read of a person's wording, FR-12); O-2 a person's words reach a recording command by two roads
(inline `--words` vs `person_words.read`); O-4 a rework under an orchestrator lease is always refused; O-5, O-6 small.
O-1 corrects part 1's `stage_done:set` sentence (key whitelist and the `key=value` form are refusals of the same command).

## 4. Small choices closed

- S-P1: `door_needs: none` on every conductor row — §5.5 header fixes it for T9c rows.
- S-P2: sub-ids follow requirement groups (`.call`, `.args`, …), one row per requirement the caller can meet; several
  raise sites share a row (part 1 S2 practice).
- S-P3: the `--remark` form gets its own id `waiver:remark.call` (it is the same move's second command; family = the form).
- S-P4: argparse-level refusals are folded into the `.call` rows; their text is argparse's, not the factory's.

## 5. Observations for the Lead (analogs; scope not widened)

- O-1 (part 1 item 11): part 1's `stage_done:set` sentence ("coerced to the key's type") misses two refusals of the same
  command: the key whitelist (stage_done.py:128-135, `sides.*` / `sides_unknown` :95-127) and the `key=value` form
  (:216-218). `current_code_diff_refusal` :194-210 is story-state.
- O-2: `source_exclusions.py --revoke` takes the person's words inline only (`--words`, :621), with no `--words-file`
  and no run-py.cmd check, while waiver.py and controller.py read them through `person_words.read` (M30: cmd cuts at a
  line break). A person's words reach a recording command by two roads — a P31 / FR-17 sibling.
- O-3: `_releases` (waiver.py:492-495) reads the person's WORDS too: a block of any text whose words merely contain
  `wait_existing_job` or `resume_checkpoint` skips the standing check and runs `controller.py --operation release`.
- O-4: `build_rework_request` sets no `owner_session_id` (:3843-3897), so with an orchestrator lease `apply` refuses
  every rework (:5010-5012); `release_dispatch` commits without `apply` (:8109) and meets no lease check.
- O-5: stand_health `--env` with an unknown name is silent (§1.5).
- O-6: `run_stage` calls `artifacts_dir(task)` (:997) outside any `try`; a `--task` that is no single path component
  raises `ValueError` (hooklib.py:292-293) as a traceback, no FR-1 text (the carry form checks it, :1169-1170).

## 6. Status of the six rows

| # | row | status |
|---|---|---|
| 1 | `controller:rework` | drafted: `.call`, `.args`, `.runner_half`, `.cap`; `.runner_half.manual_block` and the 10 helper bodies listed in §1.1 not drafted -- body not read; 14 story-state lines |
| 2 | `controller:release` | drafted: `.call`; `.commit` not drafted -- `event_store.commit` not read; 2 story-state lines |
| 3 | `waiver:block` | drafted: 5 rows + `waiver:remark.call`; 3 story/data-state lines |
| 4 | `waiver:carry` | drafted: 2 rows, `when` pending F-P1; 6 story-state lines |
| 5 | `stand_health:probe` | no row: the command refuses nothing of the move's call (`probe` never raises; exit 1 is the stand's state) |
| 6 | `source_exclusions:revoke` | drafted: 2 rows; 3 story-state lines |

## 7. Trail (read-main tree, package-relative; "whole" = every line of the range read)

- parent spec: §2.1-2.2 (:112-141), §2.8-2.9 (:284-313), §5.5-5.6 (:571-588), F16 (:652) via grep line. Part 1: whole (:1-460).
- `references/conductor-actions.json` 1-224 whole; `references/block-names.json` 1-77 whole.
- `scripts/waiver.py` 1-122, 122-437, 438-904, 905-1254, 1540-1664 whole (1255-1539: `run` gate form, `show`,
  `selftest` — not on these moves' roads; not read).
- `scripts/person_words.py` 40-158 whole. `scripts/contract.py` 120-138 (`prefix_value`, head of `names_whole`).
- `scripts/test_path_grants.py` 90-174 whole (constants above :90 not read).
- `scripts/hooklib.py` 219-243, 269-299, 375-398 (grep -A25 on `require_project`/`is_one_component`/`is_story_folder`).
- `scripts/controller.py` 225-284, 380-467, 700-808, 2417-2429, 3652-4012, 4998-5172, 5311-5783, 6085-6152,
  8010-8049, 8060-8169, 9100-9179, 9636-9735, 9800-9977 whole; constants :179-189 (grep).
- `scripts/no_move.py` 40-81. `scripts/source_exclusions.py` 1-60, 290-325, 476-715 whole.
- `scripts/stand_health.py` 469-560, 756-833, 900-935 whole.
- `scripts/stage_done.py` 88-157, 192-221 whole; grep `coerce_value(|--set` (:15, :92-219, :1528-1566).
- Negative claims and their positive controls:
  - "build_rework_request sets no `owner_session_id`": the request dict and every later key read whole (:3843-3897);
    control — the same read shows `request["agent_id"]` (:3863), a key set by the same pattern.
  - "the rework command does not refuse `--cases` with `--rows` together": `.args` body read whole (:3674-3824), no
    branch reads both lists together; control — the same body refuses `--cases` outside scope (:3740-3743), a check of
    the same shape.
  - "move_ids reads only `moves`": no_move.py:60-67 read; control — `TOKEN_MOVES` :40 names `go_on_as_is`, a `moves` id.
  - "`--why-person` is in no move's run": conductor-actions.json read whole; the string occurs in no `run`
    (control: `--words-file` occurs in runs :71, :117, :132 in the same read).
  - "stand_health refuses nothing of a `--probe` call": `main` :903-930 and `probe` :756-829 read whole; control —
    the one refusal it has (:930) is visible in the same read.
  - "waiver.py's `require_project` exits": hooklib.py:219-231 read; control — `sys.exit(EXIT_NO_PROJECT)` :231.

# One mechanism "told before the work" (FR-38, AR-10) — DRAFT SPEC

Status: designer DRAFT after fix round 2 (13.11.2026: second critic verdict B1-B4, N1-N11, N9b; owner answers O1, O2). Not a
dispatch. The survivor decision (§2.0) is confirmed sound by the re-pass and is not reopened. Still-open forks: §9; owner questions:
§10 (none open). Lead acceptance checks this round against `reviews/20261113-told-before-work-plan-review-2.md` (no third critic pass
needed per that verdict, unless the Lead judges O1 an architecture change — §9 F20).
Source: Lead plan `docs/tasks/specs/20261113-plan-fabrika-ne-huzhe-agenta.md` §13, §15, §16. Reviews: `reviews/20261113-told-before-work-plan-review.md`
(first), `reviews/20261113-told-before-work-plan-review-2.md` (second).
Owner's word (13.11.2026): «Эту причину мы уже фиксили много много раз. Надо собрать все места где она может всплыть и
пофиксить. И не заплатками, а единым механизмом, чтобы следующими фиксами снова не наплодить такой проблемы».
Owner's word O1 (13.11.2026): «если заранее известно, что проверит код в данном запуске дирижёра, то добавляем ему. Дирижёр же
запускается точечно для решения какой-то конкретной проблемы». Owner's word O2 (13.11.2026): «закрыть всё. За ночь успеем».
Package facts are read ONLY from `C:\QAFactory\forge-repo\.claude\worktrees\read-main\ai-packages\qa-factory\` (written `pkg:`).
Builder owns below use `C:\QAFactory\forge-repo\ai-packages\qa-factory\` (written `PKG\`) — the builder's worktree path.

## 0. Facts (read first)

| # | Fact, with its carrier | Consequence |
|---|---|---|
| 0.1 | A24 registry: 102 entries, 25 `kind: operation` (Grep `^    \{"id": "` → 102 over `pkg:scripts/refusal_registry.py`; entry lines `:74-1035`) | counts use 102/77/25 |
| 0.2 | `role_cli.refuse` + `references/role-commands.json` is an existing "one source, two readers": one row per command (`input`, `verify`) read by the refusal (`pkg:scripts/role_cli.py:74-86`) and by `--help` (`:64-71`); 31 rows. `run_guarded` (`:134-172`) turns any `ValueError` into `refuse(command, str(exc) or <class name>, stream)` (`:163-164`) | joined as `requirement_from: role-commands.json`; `run_guarded` loses a Record's check — owned by T2 |
| 0.3 | The judgment census has 1142 unit rows (`pkg:scripts/tests/fixtures/judgment-census.json`); per-role ceilings `blocking_per_role` (`:4`); "Ceilings only go down" (`:3`). `roles` is a HAND label, errs both ways (over-label: guard units list every role, e.g. `stage_guard.py` rows `:956-972`; under-label: controller units that reach a role are `["conductor"]`, 0.4) | role reach is read from the census by one join, test side (FR-44). Known under-labels are fixed by the node that owns the unit; unknown ones are caught at run time (C11, G1) |
| 0.4 | Controller refusals DO reach a role: `_s3_completion_gate` (`pkg:scripts/controller.py:7465`) raises `"S3 structured test plan invalid: …"` (`:7513`); the driver routes it by `STRUCTURED_RE` (`pkg:scripts/driver_dispatch.py:36, 89`) to `resume_structured`, which resumes the ROLE's own session with the text (`pkg:scripts/driver_machine.py:515-550`, the message `:546-548`). `REPAIR_MARKER` refusals under a `RESUMABLE_HEADS` head are resumed to the role (`driver_machine.py:38-39, 551-559`): `_code_review_refusal` (`controller.py:6443-6463`), `_s5_plan_accept_problems` (`:6845-6884`, refusals `:6857, 6862`), `_plan_rework_rows_problems` (`:6886`), `_plan_review_problems` (`:6926`, refusals `:6938, 6940, 6945, 6966`). The same gate also raises `"a window-1 (labelling) dispatch of S3 cannot close the stage"` (`:7479`) and `"S3 grounding: …"` (`:7515`), whose heads do NOT match `STRUCTURED_RE` | role-resumed controller refusals are IN the universe (T9a); `:7479`/`:7515` enter only if T0 M7 finds a road that carries them to a role |
| 0.5 | **The survivor fact.** The generated key page `references/slices/<role>/handoff-keys.md` (`contract_slices.handoff_keys_page`, `pkg:scripts/contract_slices.py:539-558`) is listed in `references/inject-map.json` for 11 roles (`:22, 30, 38, 47, 61, 70, 79, 88, 97, 104, 115`); qa-case-critic has none (`:51-58`). `inject_context.collect_blocks` (`pkg:scripts/inject_context.py:242-287`) appends the WHOLE text of every listed file to the dispatch (`:283-286`); the hook calls it on every `Task`/`Agent` dispatch (`:676`), the driver for its `--agent` sessions (`driver_dispatch.py:235`). In `prompts.slices: on_demand` every `plugin:references/slices/` entry except `COMMON_LAYER_SUBJECTS` is replaced by a path list (`inject_context.py:93-111, 245-255`). The brief reaches the role only as a PATH (`pkg:scripts/story_step.py:295-300`), and a resumed rework dispatch is not given that line (`:294-295`) | the key page is the survivor (§2.0). The brief's ahead section (`brief_pack.py:4425-4426`, from `ahead_card` `:414-418` or `FIRST_LOOK_AHEAD` `:3849`) is removed (T3b) |
| 0.6 | The key page renders `validate_artifacts.PHASE_JSON_KEYS` (`contract_slices.py:468-477`), the handoff form fields (`_keys_form`, `:505-536`) and the `demands` of `stage-joints.json` producers told on the page (`:490-501`), reading `stage-joints.json` directly (`:443-446, 490`). 14 of the 50 `told` legs of today's `stage-joints.json` point at it; others: 26 `scripts/window_record.py`, 1 `scripts/exit_gate.py`, 4 `agents/<role>.md`, 4 `artifact-contract-*` slices, 1 `common-rules.md` slice | the requirement section is a fourth section of the same page, one renderer; `_keys_outputs` moves onto the reader (T1) |
| 0.7 | `design/role-rules.json` registers rule sentences, one reader `scripts/role_rules.py` (`load` `:95-109`); 11 carriers anchor in `references/ahead-cards.json`, 1 in `references/slices/qa-automator/handoff-keys.md` (`role-rules.json:7`) | JOIN by `role_rule: <id>`; a migrated card sentence re-points its carrier to the page in the same diff (§2.7) |
| 0.8 | Code readers of `stage-joints.json`: `stage_joints.py` (through `null_outcomes.load_data`, `stage_joints.py:603-604, 645-646, 667-668`), `contract_slices._keys_outputs` (`:490`), `selftest.py:722` (`_json_carrier(...).get("joints")`, `joints[].joint.test`). Prose mentions (not reads): `contract_slices.py:440, 550`, `retro_numbers.py:1229, 1290`; `retro_numbers.py:1236` reads through `stage_joints.threshold` | T1 moves BOTH code readers (`_keys_outputs` and `selftest.py:722`) onto `stage_joints.load_rows` (N5); prose is untouched |
| 0.9 | `refusal_registry.sites(plugin_root, files, raises)` (`:1187-1216`) returns `{file, function, call, line}`; `raises=` (from `raise_family`, `:1127-1184`) is the widening switch; a call with no argument is skipped (`:1053-1055, 1211-1213`); a file that does not parse raises `SyntaxError` out of `sites` (`:1203`). Census blind spots: the ONE carrier is the header of `judgment-census.json` (`:3`); it names a stdlib subclass, a class defined only under `scripts/tests/`, a base that is neither a plain name nor `alias.Name` "(a call, a subscript, or `mod.B` where `mod` comes from a from-import of a module)", a raise through a variable or assignment alias, `raise A` with no call, `raise A()` with no argument, a raise of a call to a factory or method that returns the family exception — "52 rowless functions … an upper bound" | the wide scan is the same scanner widened through the same switch; T0 copies the blind-spot list from `judgment-census.json:3` WHOLE into its table (N8b), never from this row |
| 0.10 | Ceilings a run meets: `detector_verdict.FINDINGS_MAX_BYTES = 6000` (`pkg:scripts/detector_verdict.py:63`); `brief_pack.BRIEF_MAX_BYTES = 6 * 1024` (`brief_pack.py:54`) with its ladder (`:4479-4527`); `inject_context.MAX_BLOCK_CHARS = 26000` (`inject_context.py:45`) — an injected file over it RAISES and the dispatch is refused (`:267-277`, hook `:680-685`, driver `driver_dispatch.py:236-241`); **the Codex native packet refuses a whole context over 100000 characters** (`pkg:scripts/native_context.py:174-175`, A24 `NC-context-too-large` `refusal_registry.py:345-351`, refused through `refuse_native_stage` `inject_context.py:729-730`); the Codex context is every block + the packet + the notice + the marker (`inject_context.py:676-723`), the role file first (`codex_role_instructions` `:412-423`); `role-load.json` `process_ratchet_tokens` (shrink-only, slack 0) and `allowances.packet` = 5400 (`pkg:references/role-load.json:7`) | E12/§2.6a/§2.6b: `MAX_BLOCK_CHARS` is a run ceiling the page meets — closed at dev time by K8 + the split rule; the 100000 ceiling depends on project files — a dev-time sibling K10 + a new finding (Appendix A); the brief ladder is FV1-4 |
| 0.11 | N0 of P1-v (`Record.check`, `check_id`, `with_check`, `Refusal.checks`) is NOT on main (Grep `check_id\|with_check` over `detector_verdict.py`, `driver_core.py` → no definition; control `class Record(str)` `detector_verdict.py:90`) | T2 depends on N0 |
| 0.12 | `refusal_registry.sites()` is "the one scanner of refusal sites" (`pkg:design/architecture.md:142`) | widened in this scanner (AR-13) |
| 0.13 | `expected_of_the_receiver` is what a handoff asks of the NEXT role (`pkg:handoffs/README.md:76-77`) | neighbour, no change |
| 0.14 | Test files in `keep` of `pkg:scripts/tests/test-layers.json` (`:35-6991`): `test_stage_joints.py :5254`, `test_stage_joints_12586.py :5269`, `test_refusal_registry.py :4279`, `test_detector_verdict.py :1248`, `test_brief_pack.py :286`, `test_ahead_cards.py :55`, `test_role_commands.py :4469`, `test_role_rules.py :4543`, `test_contract_slices.py :850`, `test_run_forms.py :4552`, `test_hooklib_scan.py :2403`, `test_guard_dispatch_budget_and_logs.py :2146`, `test_judgment_census.py :2725`, `test_s5_precheck.py :4770`, `test_execution_request.py :1497`, `test_validators.py :6449`, `test_check_delivery.py :529`, `test_gate_preflight.py :1864`, `test_handoff_values_refusal.py :2309`, `test_s3_strategist_rounds.py :4654`, `test_s5_plan_controller.py :4716`, `test_controller_doors.py :882`, `test_window_record.py :6865`. In `quarantine` (`:7046-`): `test_ahead_cards_rules.py`, `test_inject_kinds_packet.py`, `test_coverage_contract.py`, `test_stage_done.py`, `test_planning_contract_not_planned.py`, `test_handoff_check_investigation.py`, `test_row_fields.py`, `test_grounding_coverage.py`, `test_slices_on_demand.py` (`:9760`) | no node touches a quarantined file; a node whose owned file has no keep test printed by `--witness-for` asks the Lead before work |
| 0.15 | The kinds drop: `delivered_text` (`inject_context.py:181-196`) cuts every heading `inject-map.json` `kinds.<repair\|rework>.<role>.drop_sections.<rel>` lists; `_dropped_headings` (`:164-178`) and `map_problems` (`:199-239`) refuse only a `common` entry or a `COMMON_LAYER_SUBJECTS` name (`:172, 226`). Today one row drops two `execution-lifecycle.md` headings of the automator (`inject-map.json:7-18`). The on_demand weight report counts by `COMMON_LAYER_SUBJECTS` too (`contract_slices.py:739-752`) | B1: the never-cut set becomes `INLINE_SUBJECTS` in all four places (§2.6) |
| 0.16 | The role prompt: `story_step._prompt` (`story_step.py:250-304`) is called only by `_card_text` (`:1116-1125`), "the ONE renderer: `start` writes and prints it, `where` rebuilds it, `materialize` writes and compares it"; the brief is written by a SUBPROCESS `brief_pack.py` (`_brief` `:445-460`), so no value of `build` returns into the prompt; `story_step` already imports `brief_pack` lazily for a dispatch fact (`brief_pack.reviewed_dispatch_id`, `:330-333`). A rework that resumes its agent carries the `You are resumed` packet line (`_resumed_lines` `:1128-1148`) and still goes through `_prompt`. The dispatch facts `build` reads: `first_look` (`brief_pack.py:4127`), `s5_kind` via `_s5_kind` (`:1855`, used `:4141-4144`), `_record_kind(dispatch) == "manual"` (`:2539`, `:4263`), `walking` = a walk record on disk (`:4262-4265`) | B3: one function `brief_pack.dispatch_groups` computes the groups; `build` and `_card_text` call it (§2.6) |
| 0.17 | Driver resumes of a role: `run_claude(..., resume=sid)` with no `system_file` (`driver_dispatch.py:546-547, 575-576, 1035, 2078-2079`; `driver_machine.py:546-549`); `claude_cmd` passes `--append-system-prompt-file` only when given and drops `--agent` on resume (`driver_runner.py:568-571`). Whether `claude -p --resume` keeps an earlier call's appended system prompt is a host property no carrier states | **estimate, not verified** until T0 M9 (N1) |
| 0.18 | The conductor's launch (driver): `Driver.conductor` (`pkg:scripts/driver_conductor.py:263-348`) builds the prompt (`:315-334`) from the refusal text, `story_step where`, the person's words and up to 3 files, and passes `system_file=references/conductor.md` (`:336-337`). The refusal text it receives is composed at `:684` as `lead + no_move.moves_section(NM.data(), open_ids, facts, site) + state text`; `open_ids` = `no_move.open_moves(facts, moves)` (`no_move.py:175-187`; `driver_conductor.py:636`). `moves_section` (`no_move.py:257-285`) is "the section of the conductor's prompt that says which rows of `moves` are open now". The answer is judged by `no_move.validate_options` (`:397-470`) and `check_args` (`:228-254`); each move row of `references/conductor-actions.json` names the command it runs (`run`, e.g. `rework_stage` `:66-79`) | O1: the conductor's rows enter in `moves_section`, selected by `open_ids` (§2.9) |

## 1. Invariants touched, owners, census classes

### 1.1 AR-n (each with the change check it demands, written into the DoD of the nodes in §5)

| AR | How it is kept | Change check in DoD |
|---|---|---|
| AR-10 (`architecture.md:113-118`) | every role-reachable check id, and every check known in advance for a conductor launch, has one row; the row is rendered on the key page of every role it names (injected whole), or in the conductor launch prompt; the walker is red otherwise; holes are declared and counted | T1–T9: the row and the regenerated page in the same commit as the constructor call (or, after T1r, the row already landed); `selftest.py --slices` green |
| AR-9 (`:106-111`) | in-process transports print problem + expected + door from the row; a door that needs a shell is never shown to a role without one — by data (`door_needs` × `when` × `host_adapter.role_has_bash`), never by reading the door text (FR-12) | each migrated site keeps its A24 entry; `refusal_registry.py --check` green |
| AR-13 (`:161-166`) | one reader of `stage-joints.json` (`stage_joints.load_rows` / `row_for` / `rows_for`), one composer of words (`told_text`), one line renderer (`told_line`), one fill (`fill`), one reader of a record's check (`check_id`, N0), one scanner (`refusal_registry.sites`), one reader of `ahead-cards.json` (`contract_slices.ahead_card`), one computation of the dispatch groups (`brief_pack.dispatch_groups`) | Grep of CODE reads (N5): `(_json_of\|_json_carrier\|read_json\|json\.load\|load_ref_json)[^\n]*stage-joints` over `scripts/*.py` minus tests → only `stage_joints.py`; positive control: today's `contract_slices.py:490` and `selftest.py:722` both match before T1 |
| AR-14 (`:168-173`) | one writer of `check` on a record: N0's `with_check`; `refusal` builds through it. `inject-map.json` keeps its one (hand) writer: a split page is added by a hand line, never by a generator (§2.6a) | T2 row: `refusal()` equals `with_check(Record(problem), check)` plus the two told attributes |
| AR-15 (`:175-180`) | one told carrier per receiver kind: the key page for roles, the launch prompt section for the conductor, both rendered by `told_line`; `requirement_from` carriers joined; `role-rules.json` joined by id; `ahead-cards.json` absorbed (T1r) | every node lists its sites (Grep for the transports, not the helper) |
| AR-17 (`:203-208`) | the conductor seam is unchanged; its launch prompt gains the rows of the checks that judge its open moves (O1), through the one seam `no_move.moves_section` | T9c row: the prompt of a fixture launch holds the rows of its open moves |
| AR-18 (`:196-201`) | form-1 finding lines stay byte-identical; expected/door only by in-process transports to the role, through `detector_verdict.spoken` | `test_detector_verdict.py` contract rows green; T2 rows `match_known`/`parse` |
| AR-20 (`:210-222`) | shrink-only counters per (file, function): `bare`, `tagged`, `untold`; per package: `hand_cards` (12 → 0), `legacy_legs` (9 → 0), `unsited` (rows landed before their sites, → 0 at the last wave), `native_headroom` per role (K10, F15); every raise of `process_ratchet_tokens` and `blocking_per_role` named | DoD of every node: "ratchet rows: key, old → new, reason" |
| AR-22 / AR-23 (`:233-245`) | every row field has a reader (page/prompt + refusal); a section with zero rows declares its empty outcome; a listed continuation page with no rows says so | T3a rows "zero rows", "empty continuation page" |
| AR-28 (`:275-280`) | a missing/unreadable rows file or row never turns a refusal into a pass; a missing check id is `unknown`, counted | T1/T2 rows for absent/broken file |
| AR-29 (`:134-157`) | code checks presence and joins only; the sentence's truth is judged by a tier above (J1/J2) | see 1.2 |
| AR-1 / AR-2 | closed variety = data (`when_kinds`, `when_exclusive`, `move:<id>` from `conductor-actions.json`, `requirement_from` carriers, `door_needs`, roles); open variety = judgment | — |

AR-11/AR-12 are touched indirectly (the page grows, the brief shrinks): measured by P1-v and by named `process_ratchet_tokens` raises.

### 1.2 Checks this spec adds or alters — owner (P27) and census class (AR-29)

| Check | Where | Owner | Class |
|---|---|---|---|
| K1 every check id met in code has exactly one row; N0's `<stem>:unlabelled` and `unknown` need no row; an A24 id whose every site carries a sub-id `<id>.<part>` (C14) needs no row of its own | `stage_joints.audit` direction A | data (code) | xref |
| K2 every role a row names, whose capability the row's `when` admits, has the row on one of its generated key pages (`{"page": true}`: `rows_for(role, stage)` returns it and the role's `inject-map.json` list holds `handoff-keys.md`); for `conductor`: the row's `when` holds `conductor_answer` or a `move:<id>` token of a move of `conductor-actions.json`; hand prose is never a leg | `stage_joints._told_leg` (T1, gated, N9) | data | presence/xref |
| K3 non-empty `requirement` or a closed `requirement_from`, a `door`, `door_needs: "shell"` only with `"shell"` in `when`; `when` tokens from `when_kinds` or `move:<id>` of a real move | `stage_joints._row_problems` | data | shape |
| K4 per (file, function): `bare`/`tagged` counts of role-reachable units ≤ baseline; a role-reachable bare site in a unit with no baseline row is red | `test_stage_joints.py` over `sites(raises=raise_family(wide=True, blocking=<census set>))` | data | shape (AST) |
| K5 the role set of a unit (census `roles` minus `conductor`) ⊆ the roles of its rows | `test_stage_joints.py` | data | xref |
| K6 `untold`: every blocking census unit with a non-conductor role contains a `sourced`/`tagged` site, or counts in `untold` | `test_stage_joints.py` | data | xref |
| K7 a row's `role_rule` exists in `design/role-rules.json` | `stage_joints._row_problems` | data | xref |
| K8 each generated key page file: under 80 % of `inject_context.MAX_BLOCK_CHARS` silent; 80-100 % a WARN line naming the split move; over 100 % red with the same line (§2.6a) | `contract_slices.keys_findings` | data | shape |
| K9 dry story: a refusal a stub role receives has a row listing that role, on its key page | P1-b C11 (§7) | data | xref |
| K10 Codex headroom: per role, plugin share ≤ headroom (§2.6b), else red unless at or under the role's named baseline (F15) | `role_load` (new `native_headroom_problems`), run by the caller of `role_load.process_ratchet_problems` (T3a names that caller by Grep before work; none in CI → `contract_slices.keys_findings` calls it) | data | shape |
| K11 a `kinds.*.drop_sections` row naming an `INLINE_SUBJECTS` entry is refused | `inject_context.map_problems` (T3a) | data | xref |
| K12 `unsited` ≤ baseline; 0 at the closing wave | `test_stage_joints.py` | data | xref |
| J1 the requirement sentence states truly what the check refuses, in words the receiver can act on; a `role_rule` join names the same rule; a diff that adds a transport in a function that also loses one (swap road) | critic question (T10) on every diff that adds/edits a row; Lead accepts | judgment (critic → Lead) | meaning |
| J2 the door is one the receiver really may open (FR-2) | same critic question | judgment | meaning |

Census: K1–K3, K7 in `stage_joints.py` (CI `selftest.py --contracts`); K4–K6, K12 in `test_stage_joints.py`; K8 in `contract_slices.py`;
K10 in `role_load.py`; K11 in `inject_context.py` (`map_problems` is asserted clean by its test). A new unit is class `shape`/`xref`, owner
`data`, roles `["conductor"]` (it blocks no role at run time). Census relabels by T4, T9a and T9c are relabels of EXISTING units by
the road their refusals take (§2.8), each with a `note`; "census: no new blocking unit" is in every package node's DoD.

## 2. The mechanism

### 2.0 Lead decisions this spec carries (do not reopen)

- **Survivor.** The surviving told carrier is the one whose text reaches the receiver WHOLE before the work with no action of its
  own: for a role the key page (injected by `collect_blocks` on hook and driver roads); for the conductor the launch prompt (O1, §2.9).
  The brief carries no copy of a requirement. Confirmed by the second critic pass.
- **role-rules JOIN.** `role_rule: <id>` on a row; K7; nothing is retired.
- **Text.** Form-1 finding lines and cross-process texts stay byte-identical; expected and door are printed only by in-process
  transports to the role (`hooklib.block`, `stage_guard.deny`, `role_cli.refuse`), after the problem.
- **B1 (round 2).** `INLINE_SUBJECTS` (the common-rules slice + every generated key page) are never cut and never named instead:
  `named_instead`, `_dropped_headings`, `map_problems` and the on_demand weight report all read it; a `kinds.*.drop_sections` row
  naming a key-page entry is refused by `map_problems` and ignored by `delivered_text`.
- **B2 (round 2).** Size is decided (§2.6a, §2.6b): no truncation and no dropped row, ever; split by generation; T0 M5 measures the end
  state of every role; the Codex 100000 ceiling is named, gets a dev-time sibling K10 and a new finding (Appendix A); this mechanism
  does not remove that ceiling, it declares the dependency.
- **B3 (round 2).** The dispatch-group line goes into the role prompt built by `story_step._prompt`, from the same groups the brief
  states (one function, §2.6); exclusive headings name what they replace; resumed dispatches carry it (§2.6).
- **B4 (round 2).** §5.3 (T4) and §5.4 (T5) rows drafted now from the function bodies.
- **O1.** The conductor is IN wherever what code will check in THIS launch is known in advance (§2.9); the rest stays counted with a
  reason per group (§2.8).
- **O2.** Everything role-reachable (and conductor-launch-known) is closed before the next live run, as one night of waves (§5.0); no
  "by price, later" residue; rows land first in ONE node (T1r), migration nodes switch call sites only.
- Earlier decisions: F1 B (join by `check_of`); F2 a (literal at the call is the key; 43 rows renamed once); F5 (constructor in T2 on
  N0); F6 join; F7 → absorbed into T1r (all 12 cards at once, O2); F8 → `CARD_MAX_BYTES` removed (N12); F9 → C11 calls `rows_for`;
  F10 census, under-labels fixed; F12 (a) taken (B1 extends it); F13 → all 9 legacy legs re-legged in T1r (O2); F14 (a) + the prompt line
  (B3).

### 2.1 Check id (one namespace)
`<script stem>:<family>`; `family` matches `[A-Za-z0-9_.\[\]-]+`. Read only through `detector_verdict.check_id(record)` (N0). Written
only as a LITERAL (or a module-level str constant, resolved by AST) at `detector_verdict.refusal(...)`, N0's `with_check(...)`, a form-1
label `[<check> <id>]`. For an A24 row the id is COMPUTED: `refusal_registry.check_of(entry) = "<file stem>:" + entry["id"]`; a site of
that function may write the sub-id `<check_of>.<part>` when one sentence cannot state the function's refusals (C14). For a role CLI:
`role_cli:<command>` computed inside `role_cli.refuse` when the Record carries no check. For a conductor answer check: `no_move:<part>`.

### 2.2 Row schema (`references/stage-joints.json`, `schema_version` 2)
Top keys: v1's `schema_version, note, friction, joints, ratchet` + `when_kinds` + `when_exclusive` + `told_ratchet`
(`{"bare": {"<file>::<function>": n}, "tagged": {...}, "untold": {...}, "hand_cards": n, "legacy_legs": n, "unsited": n}`).
```
{"check": "<check id>",
 "stages": ["S5"],                           # "*" = every stage of stages.json
 "requirement": "<one English sentence: what the check refuses, said as what it expects>",   # or
 "requirement_from": "window_record.REQUIRED_ROW_FIELDS" | "role-commands.json" | "validate_artifacts.PHASE_JSON_KEYS" | "handoff_form",
 "carrier_key": "<artifact name | command>",
 "door": "<command or field; <T>/<ID>/<home> placeholders>",
 "door_needs": "shell" | "none",
 "when": ["always"],                         # tokens, ALL must hold
 "role_rule": "<role-rules id>",             # optional
 "producers": [ { v1 entry; "roles": [...] | ["*"]; "told": [{"page": true} | {"path","anchor"}]; gap ... } ],
 "joint": null}
```
`when_kinds` = `always, shell, no_shell, plan, window, manual, first_look, not_first_look, walk, conductor_answer` plus the pattern
`move:<id>` whose `<id>` must be a `moves[].id` of `references/conductor-actions.json` (read through `no_move.move_ids`, the one reader).
`when_exclusive` = `[["first_look", "not_first_look"], ["plan", "window"]]` (data; read by the page renderer for headings, C13).
`shell`/`no_shell` resolve per role through `host_adapter.role_has_bash`; dispatch tokens per dispatch (§2.6); conductor tokens per
launch (§2.9). `requirement` XOR `requirement_from` on a row reached by a receiver. Roles `["*"]` = the roles of `inject-map.json`
`roles` (C2); `conductor` is named explicitly, never inside `*`.

### 2.3 The reader and the renderers (`stage_joints.py`, T1)
- `load_rows(path=DATA) -> (data | None, why)` through `hooklib.read_json(path, None, kind=dict, errors=Exception)`; why is `"<name> is
  absent"` / `"<name> is not a readable JSON object"` / `"<name> has schema_version <v>; this reader reads 2"`. `audit`, `threshold`,
  `main`, `contract_slices._keys_outputs` and `selftest.py`'s `joints[].joint.test` read (`selftest.py:722`) go through it.
- `row_for(check) -> (row | None, why)`; `rows_for(role, stages, dispatch=None) -> list[row]`: rows naming the role in a producer,
  a stage of `stages`, capability tokens holding; `dispatch=None` returns every dispatch group (the page); a facts dict returns only the
  groups that hold. For `role == "conductor"` the facts are `{"moves": [<open move ids>]}`: a row holds when its `when` is
  `["conductor_answer"]` or a `move:<id>` with `<id>` in the list.
- `told_text(row) -> (expected, door)`: THE composer. `requirement` → the sentence; `requirement_from` → the carrier's renderer
  (`handoff_form` → "every `required` field of your handoff form (section `Handoff form` of this page)"; `PHASE_JSON_KEYS` → "`<carrier_key>`
  carries the keys " + the list; `REQUIRED_ROW_FIELDS` → `window_record.row_field_lines()` joined by `; `; `role-commands.json` → the row's
  `input`/`verify` via `role_cli.entry(carrier_key)`). Lazy carrier imports.
- `told_line(row, values=None) -> str`: THE line renderer `- [<check>] <expected> Door: <door>.` (`fill` applied when `values` given).
  The page, the conductor section and C11's expected text all call it.
- `fill(text, values) -> str`: replaces exactly `<T>`, `<ID>`, `<home>`; a missing value leaves its placeholder. `brief_pack.py:4337`
  calls it too.
- Import rule: module level stays `ast, re, sys, Path` (`stage_joints.py:33-36`); readers import only `hooklib`; the walker's heavy
  imports stay inside the walker.
INVARIANT I-S: for one dispatch, `fill(page line)` and the refusal's printed expected/door are the same strings (both from `told_text`/`fill`).

### 2.4 The constructor and the transports (T2; on top of N0)
`detector_verdict.refusal(check: str, problem: str, *, fill: dict | None = None) -> Record` — never raises.
- Builds `with_check(Record(problem), check)` and sets `expected`, `door` from `row_for` + `told_text` + `fill`. `str(record)` is the problem ONLY.
- `detector_verdict.spoken(record) -> str`: `problem` + `\n  expected: …` + `\n  door: …` + `\n  check: <id>`; a plain str unchanged.
- In-process transports call `spoken`: `hooklib.block`, `stage_guard.deny` (a plain str prints byte-identical to today),
  `role_cli.refuse(command, problem, stream=None, *, check=None)`: `{command}: {str(problem)}`, then expected/door only when the row is not
  the command's own role-commands row, then today's lines unchanged, then `  check: <problem.check or check or role_cli:<command>>`.
- `role_cli.run_guarded`: a `ValueError` whose `args[0]` is a Record is passed to `refuse` whole; else today's text.
- Form-1 producers print byte-identical text; the check crosses only through N0's label and `checks:` line; never expected/door.
- Cross-process raises keep their text byte-identical; the id crosses only where P1-v carries it (`unknown` until P1-v F18).
- `RECORD_SINKS` (code constant, `refusal_registry`): `block`, `deny`, `refuse`, `raise ValueError(...)` in a file that calls
  `run_guarded` at module level. A `refusal(...)` Record reaching a sink is `sourced`; reaching any other transport `tagged`; a list joined
  or `str(`-ed in the same function downgrades its sites to `tagged`.
- Row absent/unreadable: `expected` = `"(the factory's requirement row <id> could not be read: <why>; this is a factory defect)"`, `door` = `""`.
  INVARIANT I-P: a missing row never turns a refusal into a pass or a crash (FR-59, AR-28).
- INVARIANT I-R: for every row `driver_machine.match_known(spoken(r)) == match_known(str(r))`; no filled text holds `REPAIR_MARKER` or
  `PERSON_MARKER`; form-1 output from `refusal()` Records is byte-identical to the same from plain strings.

Error directions (reused functions in a gate role): (1) `refusal_registry.sites` becomes a GATE input (K4, K6): it may err toward
counting a non-refusal (a raised baseline, safe), never toward missing a role-reachable refusal of a shape it claims to scan.
Adversarial inputs, each a T0 table row "seen" or "named blind spot": an alias (`b = block; b(msg)`); a message built in another function;
`print(json.dumps({...}), file=sys.stderr)` then `return 2` (`run_suite.py:970`); `sys.stderr.write(...)`; `sys.exit("<message>")`;
`raise SystemExit("<message>")`; a list under any name (`reasons.append`, `acceptance.py:160-182`; `case_forms.py:70-103`); `errors += [...]`;
a `yield` of an error string; every blind spot of `judgment-census.json:3`, copied whole. K6 catches a blocking unit whose transport the
scan cannot see. (2) `stage_joints.rows_for` becomes the TOLD-LEG input (K2, C11, the conductor section): it may err toward returning a
row the receiver does not need (more text, safe), never toward omitting a row the data assigns — guarded by I-S and the T3a/T9c content
rows. (3) `brief_pack.dispatch_groups` becomes a prompt input (B3): it may err toward naming MORE groups (the role reads an extra group,
safe only for additive groups); for an exclusive pair it must never name both or neither — when a fact cannot be read it names neither
member and the line says `could not tell: read both "<A>" and "<B>" and ask the conductor` (FR-59), never a guessed member.

### 2.5 Bringing invisible refusals into the universe (T0)
`raise_family(plugin_root, files, *, wide=False, blocking=None)`: with `wide` each file's spec carries `"transports": WIDE_TRANSPORTS`
and `sites(raises=spec)` reads it (one switch; without `wide` byte-identical). `blocking` is the set of (file, function) the census marks
blocking, PASSED BY THE TEST (the census is test-only, FR-44; N8a); the list transports below count only inside those units; with
`blocking=None` the scanner counts no list site and says so in `main`'s output (`list sites: not counted, no census set given`).
`WIDE_TRANSPORTS` (code constant, C1): `deny`, `block`, `refuse`, `run_guarded`-wrapped raises, the `raises` family, `sys.exit(<str>)`,
`SystemExit(<str>)`, `print(..., file=sys.stderr)` in a function that also returns a non-zero int / `EXIT_*` name or calls
`sys.exit(<non-zero>)`, `sys.stderr.write(...)` under the same condition, `<any name>.append/extend(<expr>)` / `<any name> += [<expr>]`
inside a `blocking` unit. One state per site: `sourced`, `tagged`, `bare`. Walk error = a scanned file that fails to parse, or a
`refusal(...)`/`with_check(...)` call whose check is not a literal or module constant. Counts per (file, function). The swap road inside
one function is an accepted limit, detected by J1 and by P1-v G1.

### 2.6 The told leg: the key page and the prompt line (T3a, T3b)

**The page (T3a).** `contract_slices.handoff_keys_page(plugin_root, role)` gains, after `## Handoff form`, `## What code will check of you`:
- a legend line: "`<T>` is your ticket, `<ID>` your dispatch id, `<home>` the project's qa-factory folder — all three stand in your
  prompt (`Ticket: … Dispatch: …`, `story_step.py:257`) and in your task packet";
- rows of `rows_for(role, stage_guard.stages_of_role(model, role))` with `when` of capability tokens only, first; one `told_line` each,
  placeholders unfilled; order: first stage index in `stages.json` (`*` = 0), then check id;
- one sub-heading per dispatch token with rows, in this order: `### Only in a plan dispatch (replaces "Only in a window")`,
  `### Only in a window (replaced by "Only in a plan dispatch")`, `### Only in a manual block`, `### Only in a first look (replaces "Not in
  a first look")`, `### Not in a first look (replaced by "Only in a first look")`, `### Only in a walk`. The `(replaces …)` text is generated
  from `when_exclusive`; an additive group has none;
- `### Not yet in rows` — the role's card through `contract_slices.ahead_card(role)` while `hand_cards` > 0 (0 after T1r);
- zero rows and no card: `- none: code checks nothing of this role beyond the sections above` (AR-23).
`INLINE_SUBJECTS = COMMON_LAYER_SUBJECTS + (KEYS_NAME,)` and `contract_slices.inline_subject(name) -> bool` (true for those names and for
a continuation page `handoff-keys-<n>.md`, n ≥ 2): read by `inject_context.collect_blocks.named_instead` (`:250-251`), `_dropped_headings`
(`:172`), `map_problems` (`:226`, new message `"<where>: a common entry, the common-rules slice or a generated key page is never cut (it
reaches every dispatch)"`) and the on_demand weight report (`contract_slices.py:739-752`, N2). qa-case-critic gets its page entry in
`inject-map.json` right after its `common-rules.md` line.

**The prompt line (T3b, B3).** New `brief_pack.dispatch_groups(task_root, stage, role, dispatch_id) -> list[str]`: reads the dispatch record
and computes the four facts with the code MOVED out of `build` (`first_look` `:4127`, `s5_kind` via `_s5_kind` `:1855`, manual via
`_record_kind` `:2539`, `walking` via `walk_record` `:4262-4265`), passes them to `stage_joints.rows_for(role, stages, facts)` and returns
the headings of the groups that hold (in page order). `build` calls it for the brief's line under `## Commands`; `story_step._card_text`
(`:1116-1125`) calls it (lazy import, the precedent `:330-333`) and passes the result to `_prompt`, which prints, after the inputs and the
packet lines and BEFORE the `if brief and not resumed` branch (`:294-300`), one line:
`What code will check of this dispatch: your injected key page, section "What code will check of you" and its sub-sections <names>; the other sub-sections are not for this dispatch.`
— with no group holding: `… and none of its "Only in" sub-sections`. POSITION INVARIANT: the line is outside the `not resumed` branch, so a
rework that resumes its agent (`_resumed_lines`) gets it in its new prompt; `where` and `materialize` rebuild the same line from the same
call (the card stays one renderer, its compare stays byte-equal). Driver resumes of the SAME dispatch (`resume_structured`, `resume_repair`,
handoff resumes, `driver_machine.py:546-549`) add nothing: the line stands in the first prompt of that conversation, which a resume
restores (the user prompt is the conversation; whether the APPENDED SYSTEM PROMPT survives is 0.17, measured by T0 M9, which also checks
the first user prompt). If M9 shows the first user prompt is NOT restored, the driver's resume messages append the same line through the
same function `brief_pack.dispatch_groups` (no second reader; node of the driver owner, named by the Lead).

### 2.6a The size rule (B2; one move per state)
Let `L = inject_context.MAX_BLOCK_CHARS` (imported, never a second literal), `W = (L * 8) // 10` (20800 today), `S` = `len(text.strip())`
of one generated key page file — the same measure `collect_blocks` applies (`inject_context.py:262, 267`).

| State of one page file | K8 says | The one move |
|---|---|---|
| `S < W` | nothing | none |
| `W ≤ S ≤ L` | `WARN K8 <file>: <S> chars, at or over 80 % of MAX_BLOCK_CHARS (<L>). Split: add the line "plugin:references/slices/<role>/handoff-keys-<n+1>.md" right after "…/handoff-keys-<n>.md" in references/inject-map.json roles.<role>, then run python -B scripts/contract_slices.py --write` (exit 0) | the split, in the SAME commit as the growth (every node's DoD: a K8 WARN in the witness is not accepted) |
| `S > L` | the same text, red (`--check` exit non-zero) | the same split |

Partition (generator, deterministic): the role's pages are the listed `handoff-keys.md`, `handoff-keys-2.md`, … (consecutive). Page 1 holds
the fixed sections, the section heading, the legend and rows; rows are laid in the order of §2.6 (capability rows, then each group in
heading order) and each row goes to the current page while the page stays `≤ W` after adding it, else to the next page; the LAST listed
page takes every remaining row. A row is never cut; a group heading repeats on a page where its rows continue, with ` (continued)`.
Each continuation page opens with `## What code will check of you (continued from handoff-keys-<n-1>.md)` and the legend.
Edges, each with its invariant (no row is ever dropped or truncated; every page is injected whole):
- a listed continuation page that gets no row: legend + `- none: every row of this role stands on the pages before this one` (AR-23); not red;
- a page file on disk that is not listed: `--write` deletes it, `--check` red `unlisted generated page <file>` (no stale page is injected
  by a later hand line);
- listed pages not consecutive (a `-3` without `-2`): `keys_findings` red naming the gap;
- one row longer than `W` on its own: impossible by K3 (`FIELD_MIN`…) only in practice — if met, K8 red `one row is over the split
  threshold: shorten the sentence` (J1 judges the shorter sentence; no truncation by code);
- K2 accepts a row on any listed page of the role (the page set), never on an unlisted one.

### 2.6b The Codex native-context ceiling (B2.4; an in-run ceiling of the FV1-4 class)
`native_context.stage` refuses a role whose whole context is over 100000 characters (`native_context.py:174-175`). The owner's word on
FV1-4 (no ceiling inside a factory run; the forge watches size) makes it the same class. This mechanism does NOT remove it (Appendix A is
the finding the Lead files); it declares the dependency and adds the dev-time sibling **K10**:
- headroom `H(role) = 100000 − 26000 × P(role) − allowances.packet − 200`, where `P` = the number of `project:` entries of
  `inject_context.entries_for(role, imap)` (each is at most `MAX_BLOCK_CHARS` or the dispatch is refused already), `allowances.packet` =
  5400 (`role-load.json:7`), 200 = a reserve for the marker and the packet heading (estimate, not verified; T0 M10 measures both);
- plugin share `U(role)` = the bytes of the layers `charter` + `injection_common` + `injection_role` of `role_load.static_load(role)`
  (`role_load.py:467-484, 505-525`; bytes ≥ chars, so the share errs high, the safe side);
- `U ≤ H`: green; `U > H`: red, unless `U ≤` the role's baseline `native_headroom.<role>` in `role-load.json` (F15) — the message names
  the role, `U`, `H`, the baseline and Appendix A's finding.
A split page does not lower `U` (both pages are injected); K10 is the only check that sees this growth. Today's numbers are an estimate:
the second critic measured plugin entries + role file at 57997 for qa-automator (46913 + 11084) against `H` = 68400 with one project
entry; roles with two project entries (qa-requirements-tester, qa-test-strategist, `inject-map.json:28-44`) have `H` = 42400 and may be over
today — T0 M10 measures it and F15 decides the move.

### 2.7 role-rules join
A row whose requirement is the same rule as a `role-rules.json` row carries `role_rule: <id>` (J1; K7). When T1r migrates a card sentence
that is a role-rules anchor, the same diff re-points that carrier from `references/ahead-cards.json` to
`references/slices/<role>/handoff-keys.md` (or the continuation page the sentence lands on) with an anchor that stands once there;
`role_rules.py --check` green. Retiring a row is out of scope.

### 2.8 Roads: role-reachable, conductor-launch-known, conductor-only
A unit is role-reachable when its refusal reaches a role by a road of the code: (a) a hook on a tool a role calls; (b) a controller/
story_step refusal the driver resumes into the role's session (head matches the controller-side part of `STRUCTURED_RE`, `S\d structured
.* invalid`, case-insensitive, or `REPAIR_MARKER` under a `RESUMABLE_HEADS` head); (c) a role CLI.
A unit is conductor-launch-known (O1) when its check judges the conductor's answer (`no_move.validate_options`/`check_args`) or the command
an open move runs (`conductor-actions.json` `moves[].run`): it gets rows with `roles: ["conductor"]` (§2.9).
Everything else that only the conductor or code sees stays OUT, counted by `test_stage_joints.py` as `conductor_only N`, printed per group
WITH ITS REASON (never a silent exclusion):
- G-dispatch: refusals on the `Task`/`Agent`/`SendMessage` hook (`inject_context.dispatch` `:606-740`, `run_stage_guard`, `stage_guard`
  `check_dispatch`/`check_resume`/`_check_exploration`/`_unidentified_resume`, IC-*, NC-*, CR-*, HA-rewritten-input) — reason: the caller is the
  driver's code or the interactive main session; a driver-launched conductor has no `Agent` tool (`CONDUCTOR_TOOLS`), so no conductor
  launch makes a dispatch whose refusal it could be told in advance;
- G-free: refusals of commands a conductor runs that no open move's `run` names — reason: not known before the launch (the conductor
  chose them inside it);
- G-main: every refusal met by the interactive main session acting as conductor — reason: it is no launch for one problem; it runs the
  whole story (owner's O1 speaks of a launch);
- G-code: controller/story_step refusals answered by code moves with no resume and no conductor launch — reason: no reader but code.
T0 M7/M8 measure the sets; T4 relabels G-dispatch units of its files to `["conductor"]` with a `note`; T9a relabels road-(b) units to
the roles their dispatch names; T9c relabels the `no_move` units to `["conductor"]` with a `note` naming the launch road.

### 2.9 The conductor's launch rows (O1; T9c)
Where they enter: `no_move.moves_section(spec, open_ids, facts, site)` (`no_move.py:257-285`) appends, after the moves (and after
`## Answers this question already takes` when present), `## What code will check in this launch` with one `told_line` per row of
`stage_joints.rows_for("conductor", ["*"], {"moves": open_ids})`, placeholders filled with the task id where known, else unfilled; no
row: `- none: code checks nothing of this launch beyond your answer's form above`. Its one caller composes the conductor's text
(`driver_conductor.py:684`) and the prompt (`:315-334`), so every driver conductor launch carries it. How the launch kind selects:
`open_ids` (code-checked preconditions, `no_move.open_moves`) are the facts; `conductor_answer` rows hold on every launch whose answer
`validate_options` judges; `move:<id>` rows hold when `<id>` is open. `references/conductor.md` (the system file, `:337`) stays static and
carries no rows (it is not launch-specific). Rows of §5.5; command rows per move from §5.6 (wave 0). `forbidden_when`/`precondition`
texts of the move rows stay data the conductor judges (F16).

## 3. Edge behaviour (each with its invariant)

| Edge | Behaviour | Invariant protected |
|---|---|---|
| E1 refusal text built dynamically | check id must be a literal/module constant (else walk error); the problem may be any f-string; the requirement is static text with placeholders or a `requirement_from` carrier | page and refusal never state two requirements (I-S); an unreadable id is never green |
| E2 one refusal reached by several roles | one row; producers list the roles (or `*`); K2 per role, only for roles whose capability `when` admits; K5 when census roles ⊆ row roles | every receiver is told; never a door outside its tools (FR-2) |
| E3 conductor-only refusal | outside K2/K5/K6; counted per group with its reason (§2.8) | no exclusion is silent; a launch-known check is IN (O1) |
| E4 row whose roles list is empty | red: "a requirement nobody is told — name the roles or remove the row" | no row exists only to lower a count |
| E5 refusal reachable only by code | not in the universe: not blocking, G-code, or caught and re-raised as another A24 refusal (HA-patch-* → PT-patch-unchecked; HA-command-field-type → HA-call-shape; HA-event/tool-input-not-object → PT-unparsed-event), or a probe (PT-doctor-probe, HA-doctor-no-tools) | an under-label not yet known is found by C11/G1 |
| E6 TEMPORAL: rows/fields/pages absent before, present after | Before T1: v1 (43 rows). T1 migrates to v2 with every reader in the same commit; pages byte-identical. T1 implements the `{"page": true}` leg GATED: refused with "the page renderer is not present" while `contract_slices` has no `requirement_section` attribute; T3a adds it (N9). Before T1r: no new requirement rows. After T3a and before T3b: the requirement may stand in both carriers (page + brief ahead section) — over-telling, harmless; never in neither (T3b removes the brief section only after T1r's rows are on the pages). Runtime: an absent rows file leaves the generated page standing; refusals follow I-P | a broken install never loses a page, never passes a refusal |
| E7 two rows claim one id | walker red; `row_for` returns the first, `why = "two rows"` | never ships; never a pass |
| E8 page section with zero rows | role with reachable units: red unless each is a declared gap; else the `none` line; a dispatch with no group: the prompt line says so | an empty section is a stated outcome |
| E9 a person's recorded word | form-1 lines byte-identical, `split_overridden` unchanged; word checks judge `str(record)` | a token only in a requirement passes nothing |
| E10 migrated refusal text changes | only hook and role-CLI texts get expected/door/check lines; controller and form-1 texts do not change | no extra resume, no re-route (I-R) |
| E11 row present, site gone | after the closing wave: stale row → red. Between T1r and the last wave a row whose site is not yet migrated counts `unsited` (≤ baseline, K12), never red; a row whose site is gone AFTER being sited is red at once | rows track code; landing rows first never hides a stale row past the night |
| E12 sizes and ceilings | nothing truncated; form-1 unchanged; the brief shrinks; `MAX_BLOCK_CHARS` closed at dev time by K8 + split (§2.6a); Codex 100000 named, K10 + Appendix A (§2.6b); the brief ladder is FV1-4 | «потолок — фордж»: no role is refused or trimmed for this mechanism's text by a ceiling the forge can see |
| E13 `compound` with several ids | each item its own Record; `checks` = sorted unique | every item is told |
| E14 role-rules anchor on a migrated sentence | re-point in the same diff; anchor twice on the page → choose 2-6 other words that stand once | `role_rules.py --check` never red |
| E15 a role without a key page reached by rows | K2 red; qa-case-critic gets one in T3a | the survivor exists for every reached role |
| E16 v1 legs outside the page | 9 legacy legs re-legged by T1r to `{"page": true}` with sentences from §5.6 (wave 0) → `legacy_legs` 0 tonight (N6, O2) | one told carrier; no residual leaves without an owner |
| E17 relabel raises a ceiling | T9a raises `blocking_per_role` for roles named, named in the verdict; T4/T9c relabels to `["conductor"]` lower role ceilings | ratchets move only with a named reason |
| E18 a kinds row drops a key-page heading | `map_problems` names it (K11), `delivered_text` keeps the text whole (`_dropped_headings` returns `[]`) | rework/repair dispatches never start without the requirement section (B1) |
| E19 page size states | §2.6a, one move per state | no row dropped, no run refusal for page size |
| E20 Codex headroom | §2.6b K10; a role over its baseline is red at dev time | growth of the page never silently moves a role closer to a run refusal |
| E21 inherited no-context roads (N3) | hook fail-open after the receipt (`inject_context.py:526-551`), a host without `updatedInput` (`:30-32`), a Codex ambiguous child (`native_context.py:232-244`): the role starts with NO injected context — page included — and the person gets a signal; inherited from every injected rule, owner-accepted; this spec adds nothing and removes nothing | named, never claimed covered |
| E22 driver resume of a role (N1) | page in the appended system prompt of the first call: survives a resume = estimate, not verified, until T0 M9; the prompt line survives as part of the conversation (also checked by M9). If M9 shows the system prompt is lost: role resumes pass `system_file` (driver owner's node, the Lead names it); until then Q-free statement "the role sees it on its page before the work" holds only for first dispatches | a claim to the owner never outruns its measurement |
| E23 exclusive groups | headings name what they replace; the prompt names the members that hold; an unreadable fact names neither member and says so (§2.4 (3)) | a role is never told both or neither member silently |
| E24 conductor launch with nothing known | `none` line in its section | the launch says its empty outcome |
| E25 a move id renamed in `conductor-actions.json` | K3 red on a `move:<id>` with no such move | rows never point at a move that does not exist |

## 4. Universe today — what is measured, how approximate
Grep shape counts (not refusals; T0 replaces them): `file=sys.stderr` 471 hits / 130 files; `.append(` by list name: `errors` 834, `out` 539,
`problems` 323, `reasons` 87, `failures` 27, `bad` 27, `missing` 12; `deny(|block(` in hook files: guard_pre_tool 30, stage_guard 24,
host_adapter 9, inject_context 8, hooklib 1; `refuse(|run_guarded(|RefusingParser(` 186 in 31 files; A24 102; stage-joints 43 rows;
role-commands 31; ahead cards 12; census 1142. THE count: `python -B ai-packages/qa-factory/scripts/refusal_registry.py --sites --wide
--census ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json --json`.

## 5. Nodes (for a weaker model; PROJECT.md «Командная работа» item 11)

Every package node: `given:` `design/factory-rules.md` whole, `plans/builder-rules.md`, this spec, the files it owns. Witness:
`python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>` (builder-rules 7b). No new test file: new cases are
variant/table rows in the keep files of 0.14; a node whose owned file has no keep test asks the Lead before work. Every DoD: "census: no
new blocking unit", `test_judgment_census.py` green, `architecture:` line naming §1.1 rows, ratchet rows (key, old → new, reason),
`role_rules.py --check` and `contract_slices.py --check` green with NO K8 WARN, K10 green. Hot files owned by function.

### 5.0 The night (O2): waves, cap 6 writing builders, queues only on shared files

The cut that removes the shared-file bottleneck (a decision — the walker is written by T1, so the code allows it): **T1r lands every
drafted row (§5.1-§5.6) in `stage-joints.json`, migrates all 12 cards and re-legs the 9 legacy legs, regenerates the pages and raises
`role-load.json` in ONE node.** Migration nodes then own CODE files and test rows only; they never edit `stage-joints.json`, pages,
`role-load.json` or `role-rules.json`. Their lowered `bare`/`tagged`/`untold`/`unsited` counts stay `≤` baseline without a data edit; the
closing commit (wave 7) writes the final values.

| Wave | Builders (parallel) | Others | Merge order inside the wave | Enters when |
|---|---|---|---|---|
| 0 | — | designer: §5.6 drafts (accepted by the Lead before wave 3) | — | now |
| 1 | P1-v N0, T0, FV1-18, FV1-19 (4) | Lead: T10 prep | any | now |
| 2 | T1 (1) | Lead: T10 | — | T0 go, N0 merged |
| 3 | T2, T3a, T1r, T9c (4) | — | T2 any; T3a → T1r → T9c (data and pages) | T1 merged; §5.6 accepted |
| 4 | T3b, T4, T5, T6, T7a-1, T7a-2 (6) | — | `judgment-census.json`: T4 only; `validate_artifacts.py` by function; `brief_pack.py` after P1-v N3, RC2-1/2, FV1-4 when they are merged, else T3b merges `main` and resolves | wave 3 merged; FV1-18/19 merged for T5 |
| 5 | T7a-3, T7a-4, T7a-5, T7a-6, T7a-7, T7a-8 (6) | — | by function | wave 4 merged |
| 6 | T7b, T7c, T7d, T7e, T7f, T9a (6) | — | `judgment-census.json`: T9a only | wave 5 merged |
| 7 | closing (1 builder or the Lead): `told_ratchet` final values, `unsited` = 0 | Lead: BATCH CANON on CI | — | wave 6 merged |

If T0 says **narrow** or **stop**, the Lead re-plans before wave 2. Builder nodes: 25 (T0, T1, T1r, T2, T3a, T3b, T4, T5, T5b, T6, T7a-1…8,
T7b-f, T9a, T9c; T5b rides in wave 4 if a slot frees, else wave 5 — it then shares `execution_request.py` with T5 by function).
Declared gaps allowed after wave 7, each with its reason, nothing else: (1) a site shape T0 names a blind spot, with its count;
(2) the `conductor_only` groups of §2.8; (3) the `smell` family of `s5_precheck` (advice, never a refusal, `s5_precheck.py:22-25`);
(4) `:7479`/`:7515` of `controller.py` if M7 finds no road to a role. Any other `bare`/`untold`/`unsited` > 0 means the night is not done.

### 5.1 Node table

| Node | Owns | What, expected behaviour, test per point | Depends |
|---|---|---|---|
| **T0 spike** | `PKG\scripts\refusal_registry.py` (`raise_family` keywords `wide`, `blocking`, `sites` reading `spec["transports"]`, `WIDE_TRANSPORTS`, `RECORD_SINKS` (empty), `check_of`, `main` flags `--wide`, `--census <path>`), `PKG\scripts\tests\test_refusal_registry.py`, report `C:\QAFactory\forge-repo\docs\tasks\specs\reports\20261113-told-before-work-spike.md` | (a) `sites()` and `sites(raises=raise_family())` byte-identical to today; (b) one fixture site per transport kind; (c) sourced/tagged/bare; (d) every adversarial input and every blind spot of `judgment-census.json:3` (copied whole) — one row each; (e) `--census` joins units by (file, function), absent path → exit 2 with the reason, no census row → `roles: null` counted; (f) `blocking=None` counts no list site and prints the line of §2.5. REPORT: M1 sites per transport per (file, function); M2 role-reachable share; M3 30 stderr sites (`run_suite.py`, `stage_done.py`, `manifest_put.py`) with context — the Lead classifies; M4 per detector: family set a module tuple? M5 END state per role, every role of `inject-map.json` and the conductor section: bytes of the would-be page = today's page + the drafted rows of §5.1-§5.6 that name the role (drafted rows measured by `told_line`, undrafted by row count × the mean drafted line length, labelled estimate) and the predicted page count under §2.6a; M6 N0 landed?; M7 controller units of road (b): literals matching `S\d structured .* invalid` (case-insensitive, as `driver_machine.py:444`), or `REPAIR_MARKER` in the message — positive control `controller.py:7513`, negative control `:3203` (Gate A, no `S\d` head); report `:7479`/`:7515` by road; M8 per `stage_guard`/`inject_context`/`native_context` unit: hook events and whether any role's tool line lists `Task`/`Agent`/`SendMessage`; M9 ONE experiment (CLAUDE.md pt.6a): `claude -p --agent <role>` with `--append-system-prompt-file <a page>` and a prompt line, then `claude -p --resume <sid>` asking to quote one line of the page and the prompt line — record both answers verbatim; M10 per role `U`, `H`, `P` of §2.6b and the marker + packet heading lengths. GATE: go — walk errors ≤ 5 % of files, join ≥ 90 %, M3 precision ≥ 80 %; narrow — M3 < 80 %: stderr a named blind spot with its own counter; M4 mostly "no": coarse `<stem>:*` rows; stop — join < 90 % or walk errors > 5 % | — |
| **T1 rows v2 + reader + gate** | `PKG\scripts\stage_joints.py` (`_shape_problems`, `_row_problems`, `_told_leg`, `_direction_a`, `universe`, `_ratchet`, `audit`, `threshold`, `main`, `Report`, new `load_rows`, `row_for`, `rows_for`, `told_text`, `told_line`, `fill`), `PKG\references\stage-joints.json` (schema, renames, `when_kinds`, `when_exclusive`, `told_ratchet` baselines), `PKG\scripts\contract_slices.py` (`_keys_outputs` only), `PKG\scripts\selftest.py` (the `joints[].joint.test` read at `:722` only), tests `test_stage_joints.py`, `test_stage_joints_12586.py`, `test_contract_slices.py` | (a) v2 accepted, v1 refused; (b) K1 (fallback ids, sub-id rule C14), K3 (incl. `move:<id>` against `no_move.move_ids`), K7, E4, E7, E11 (`unsited` vs stale) — one row each; (c) universe = v1 kinds + literal ids + A24 `check_of`; (d) K4/K6/K12 baselines from T0; AT baseline green, +1 red; (e) K5; `conductor_only` printed per group with reason; (f) 43 rows renamed, pins updated, `legacy_legs` = 9; (g) `load_rows`/`row_for` absent/broken/v1 → `(None, why)`; (h) subprocess import row: none of `stage_guard`, `inject_context`, `null_outcomes`, `validate_artifacts`, `acceptance`, `handoff` loaded; (i) `keys_findings(PLUGIN) == []` after migration, `_keys_outputs` reads through `load_rows`; (j) `selftest.py:722` reads through `load_rows` (the AR-13 grep of §1.1 finds only `stage_joints.py`); (k) the gated page leg: refused while `contract_slices.requirement_section` is absent (row with a monkeypatched attribute both ways); (l) `rows_for("conductor", …, {"moves": [...]})` selects `conductor_answer` and open `move:` rows only | T0 go; N0 |
| **T1r rows landing** | `PKG\references\stage-joints.json` (rows of §5.1-§5.6, `unsited` baseline), `PKG\references\ahead-cards.json` (12 cards → rows; the file keeps `cards: {}` and its note), `PKG\design\role-rules.json` (re-points only), `PKG\references\slices\*\handoff-keys*.md` (generated), `PKG\references\inject-map.json` (continuation page lines when §2.6a says so), `PKG\references\role-load.json` (`process_ratchet_tokens` raises, named; `native_headroom` baselines per F15), tests `test_stage_joints.py` (page rows), `test_ahead_cards.py`, `test_role_rules.py` | (a) each drafted row lands verbatim (the sentence is J1's, the builder never rewrites; a mismatch is a question); (b) `hand_cards` 12 → 0, `legacy_legs` 9 → 0; (c) every reached role's page shows its rows (table row per role); (d) K8 no WARN, K10 green; (e) `role_rules.py --check` green; (f) `unsited` = the count of rows whose site is not yet migrated (printed) | T1, T3a merged first |
| **T2 constructor + transports** | `PKG\scripts\detector_verdict.py` (`Record.expected`/`door`, `refusal`, `spoken`), `PKG\scripts\hooklib.py` (`block`), `PKG\scripts\stage_guard.py` (`deny`), `PKG\scripts\role_cli.py` (`refuse`, `run_guarded`, `RefusingParser.error`), `PKG\scripts\refusal_registry.py` (`RECORD_SINKS` content), tests `test_detector_verdict.py`, `test_role_commands.py` | (a) `refusal` built through `with_check`; (b) I-P: absent row, broken file, two rows; (c) `spoken` for Record and str; (d) `block(str)`, `deny(str)` byte-identical; (e) I-R table per row + `parse`/`split_overridden` equality (E9); (f) `run_guarded` with a Record and with text; (g) `refuse(..., stream=buf)`; (h) a row per sink; (i) each of 31 commands resolves `role_cli:<command>` | T1 |
| **T3a page section + size + inline set** (N10) | `PKG\scripts\contract_slices.py` (`handoff_keys_page`, `keys_findings`, new `requirement_section`, `inline_subject`, `INLINE_SUBJECTS`, `ahead_card` (moved copy), the partition of §2.6a, the on_demand weight report `:739-752`), `PKG\scripts\inject_context.py` (`collect_blocks.named_instead`, `_dropped_headings`, `map_problems`), `PKG\scripts\role_load.py` (new `native_headroom_problems` and its call next to `process_ratchet_problems`'s caller, §1.2 K10), `PKG\references\inject-map.json` (qa-case-critic page line), generated pages, `PKG\references\role-load.json` (raises named), tests `test_contract_slices.py`, `test_stage_joints.py` (page leg on) | (a) section rows by role/stage/capability/group incl. `*`, shell vs no-shell, every group heading with its `(replaces …)` text; (b) zero-row `none`; (c) `### Not yet in rows` while cards exist; (d) K8: three fixture pages at `W−1`, `W`, `L+1` chars → silent / WARN with the split text / red; (e) partition: a fixture role with two listed pages and rows over `W` → rows split between pages, none cut, continuation heading, group `(continued)`; an empty listed page → its `none` line; an unlisted page file → red; non-consecutive pages → red; (f) on_demand: the key page and a continuation page still injected inline (via `collect_blocks` with a monkeypatched `slices_mode`), and the weight report does not count them as named; (g) B1: a fixture `kinds.repair.<role>.drop_sections` naming `## What code will check of you` of the key page → `map_problems` names it, `delivered_text` returns the text whole; (h) qa-case-critic page, `keys_findings` clean; (i) `CARD_MAX_BYTES` and its check (`test_ahead_cards.py:52, 249`) removed; (j) K10: a fixture role over `H` and over baseline → red naming Appendix A; at baseline → green | T1 |
| **T3b brief + prompt line** (N10) | `PKG\scripts\brief_pack.py` (`ahead_card` removed, the `ahead` assignment `:4344`, section `:4425-4426`, `FIRST_LOOK_AHEAD` `:3849` removed, `FIRST_LOOK_DOD` `:3847` keeps its first sentence only — the deliverable — and loses the clause naming `first_look.py put`'s check (N4), the fill `:4337` through `stage_joints.fill`, `_row_field_lines` `:2000-2013` becomes a call, new `dispatch_groups`, the brief line), `PKG\scripts\window_record.py` (new `row_field_lines`), `PKG\scripts\story_step.py` (`_prompt`, `_card_text` only), `PKG\scripts\first_look.py` (`put` refusal sites → `refusal("first_look:put…", …)`, rows from §5.6), tests `test_brief_pack.py`, `test_window_record.py` | (a) the brief has no ahead section and carries the groups line (rows: plan, window, manual, first look, walk, plain); (b) B3: for each of the five dispatch fixtures and a resumed rework fixture, the PROMPT (`_card_text`) names the groups; `where` rebuilds the same card; (c) an unreadable dispatch fact → neither exclusive member and the `could not tell` text; (d) I-S: `fill(page line)` equals a refusal's expected/door; (e) `FIRST_LOOK_*` rows: the first-look page group shows `first_look:put` | T2, T3a, T1r merged |
| **T4 command guards** | `PKG\scripts\hooklib.py` (`shell_opaque_found`, `_opaque_member`, `_DOOR_*`), `PKG\scripts\stage_guard.py` (`rule_typed_runner`, `_judge_slice`, `check_command`, `check`, `check_dispatch`, `_check_exploration`, `check_resume`, `_unidentified_resume`), `PKG\scripts\guard_pre_tool.py` (`size_check`, `runs_check`, `git_config_check`, `logs_check`, `plugin_read_check`, `big_read_check`, `case_store_check`, `handoff_write_check`, `handoff_values_check`, `artifact_rewrite_check`, `plan_write_check`, `manifest_write_check`, `owner_check`, `window_file_check`, `writes_check`, `human_word_check`, `config_write_check`, `stand_record_write_check`, `main`, `walker_refusal`, `_guard`), `PKG\scripts\host_adapter.py` (`role_policy`), `PKG\scripts\inject_context.py` (`dispatch`, `refuse_receipt`, `refuse_native_packet`, `refuse_native_stage`, `run_stage_guard` — census relabel only), `PKG\scripts\tests\fixtures\judgment-census.json` (rows of these functions), tests `test_run_forms.py`, `test_hooklib_scan.py`, `test_guard_dispatch_budget_and_logs.py`, `test_judgment_census.py` | role-facing sites → `refusal(<id of §5.3>, problem)`; FV1-27's three instances first (backslash `hooklib.py:2017-2074`/`stage_guard.py:2774`, `playwright test` `guard_pre_tool.py:322-341`, values file `:1138-1168`): a row each "the refusal prints the row's expected/door, the automator's page shows it, a no-shell role's page does not show a shell row"; G-dispatch units relabelled `["conductor"]` with a `note`; one test row per §5.3 row "the site writes this id" | T2, T1r |
| **T5 S5 chain** | `PKG\scripts\s5_precheck.py` (`report` and the family producers), `PKG\scripts\execution_request.py` (`validate_request`), `PKG\scripts\manifest_put.py` (the functions of §5.4), `PKG\scripts\run_suite.py` (`_refuse_phantom_story`, `resolve_detail_target`, `refuse_untyped_story_run`, `refuse_missing_executor`, the `invalid_*` prints in `main` `:2740, 2771, 2857, 2904` per §5.6), tests `test_s5_precheck.py`, `test_execution_request.py`, `test_manifest_put_merge.py` | sites write the ids of §5.4; s5_precheck form-1 output byte-identical (row); a test row per family "the automator's page names it"; run_suite notes stay notes | T2, T1r; FV1-18, FV1-19 |
| **T5b `--mine` refusals** | `PKG\scripts\execution_request.py` (`MineRefusal` sites of `find_active_dispatch`, `s6_close_from_state`, `_entries_of_case`, `_profile_for`, `_command_from_profile`, `sandbox_run_directory`, `_place_rows`, `_observe_precedent`, `_observe_stand`, `build_mine_request`), test `test_execution_request.py` | ids and rows of §5.6 (wave 0); text byte-identical where a driver reads it | T2, T1r |
| **T6 handoff forms** | `PKG\scripts\handoff_check.py` (`refusal_text`, `values_report`, problem builders), test `test_handoff_values_refusal.py` | ids `handoff_check:<path, list indices dropped>`; rows `requirement_from: handoff_form` + §5.6 rows; text byte-identical (driver `KNOWN_REFUSALS` `handover_form`/`form_vocabulary`) | T2, T1r, N0 |
| **T7a-1…T7a-8 `validate_artifacts.py`** | `PKG\scripts\validate_artifacts.py` (functions per sub-node, §5.2), test `test_validators.py` | appends → `refusal(<id of §5.2>, …)`; detector-printed text byte-identical; one test row per function "the writer's page shows the row" | T2, T1r |
| **T7b–T7f** | one node per file: `planning_contract.py`, `coverage_contract.py`, `check_delivery.py`, `gate_preflight.py`, `stage_done.py` (`run`, `report_problems`, `refused`); keep tests `test_check_delivery.py`, `test_gate_preflight.py`; the three with only quarantined tests ask the Lead before work | ids and rows of §5.6 | T2, T1r |
| **T8 exit families** | — | the 8 `exit:` families keep their legs (renamed in T1). No work | T1 |
| **T9a controller (role-resumed)** | `PKG\scripts\controller.py` (`_s3_completion_gate`, `_code_review_refusal`, `_s5_plan_accept_problems`, `_plan_rework_rows_problems`, `_plan_review_problems`, + units M7 lists), `PKG\scripts\tests\fixtures\judgment-census.json` (rows of those functions), tests `test_s3_strategist_rounds.py`, `test_s5_plan_controller.py`, `test_controller_doors.py`, `test_judgment_census.py` | (a) relabel to the dispatch's roles with a `note`, `blocking_per_role` raises named; (b) sites `refusal(...)`, raised text byte-identical (row per unit), counted `tagged`; (c) rows of §5.3a on those pages (row per unit); (d) `controller-blocks.md` unchanged | T2, T1r |
| **T9c conductor launch** | `PKG\scripts\no_move.py` (`moves_section`, `validate_options`, `check_args`, `prose_refusal` sites only), `PKG\scripts\tests\fixtures\judgment-census.json` (rows of those functions → `["conductor"]`, `note`), test `test_controller_doors.py` (the keep file that builds every conductor prompt, K12 of that file per `driver_conductor.py:40`) | (a) `moves_section` appends the section of §2.9 (row per fixture: rework open → the `no_move:args` row and the rework command rows; no move open → only `conductor_answer` rows; nothing → `none`); (b) refusal texts of `validate_options`/`check_args` byte-identical (they reach the driver's `_verdict_rule`); (c) the prompt of `driver_conductor.conductor` for a fixture boundary holds the section | T1, T1r |
| **T10 Lead carriers** | `docs/SIBLING_MAP.md` (axis 37 "a check's requirement: one row ↔ the constructor ↔ the key page / the conductor section ↔ the in-process transports"; axes 17, 18, 28, 32), `design/architecture.md` AR-10 Detector/Gap, AR-9 change check, `docs/tasks/critic-diff-brief.md` (J1/J2, swap road; question 9 names the new ratchets), `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` check, `design/factory-rules.md` FR-38 *Check:*, P1-b C11 | Lead-tier | T1 |

Completeness against plan §13 groups: hooks + hooklib doors → T4; exit checks → T8 + T7f; handoff forms → T6; S5 chain → T5, T5b; stage
validators → T7a–e; controller → T9a + `conductor_only`; conductor launch → T9c; role CLIs → T2; `inject_context`/`native_context`/
`codex_roles` → T4 by road (G-dispatch).

### 5.2 Rows for T7a (`validate_artifacts.py`) — re-read round 2 (N9b)
Check id `validate_artifacts:<function>`; `stages` = the writer role's stages; `when: ["always"]`; `door_needs: "none"`; door unless
stated: "edit the file and the field the refusal line names". Roles: the `writer` of the judged artifact in `references/artifact-writers.json`
(the builder confirms; a function whose artifact has no qa- writer is conductor-facing, no row). Each sentence was written against the
refusal lines of the body this round (line numbers below are the `errors.append` lines read, `validate_artifacts.py`).

| Sub-node | Function (lines read) | Roles | Requirement |
|---|---|---|---|
| T7a-1 | `check_case` (`:160-216`) | qa-case-designer | A case file opens with YAML front matter that carries every required field, takes `status`, `priority`, `channel` and `reuse_decision` from their closed lists, carries `automated_by` (file::test) when `Automated`, a `red_lock` that names a BUG-NNN, passes the form checks, and covers register requirements (or legacy `covers_ac`). |
| T7a-1 | `check_case_form` (`:376-403`) | qa-case-designer | `covers` names only register `R-n` ids of the task's register (or `legacy:<import reason>`), and the case inherits `defect_class` and `basis` from its plan row. |
| T7a-1 | `check_then_oracles` (`:310-341`) | qa-case-designer | A case written on or after the oracle cutoff gives every Then an entry in `then_oracles` with a basis per the oracle grammar. |
| T7a-1 | `check_cell_counts` (`:249-262`) | qa-case-designer, qa-requirements-tester | A table row never holds more cells than its header; a bar inside a cell is written as `\|`. |
| T7a-2 | `check_bug` (`:409-421`) | qa-bug-reporter | A bug file opens with front matter that carries every required field, with `status` from its list and `severity` from the allowed set. |
| T7a-2 | `check_bug_filing_header` (`:426-440`) | qa-bug-reporter | A bug filed from a draft of this run carries non-empty `cases` (from the draft's `case`/`cases`) and `requirements` (the R-n its `violates` names). |
| T7a-2 | `check_bug_form` (`:444-555`) | qa-bug-reporter | A bug carries an impact from the scale and the sections that make it reproducible; when its source draft has several manifestations of one cause, the source draft is readable, `cases` lists every manifestation's case and a `## Manifestations` section has one complete line per case. |
| T7a-3 | `check_register` (`:559-647`) | qa-requirements-tester | The register's front matter carries the required fields, non-empty `ids` of the form R-n, sources from the source list and `confidence` high or low; every declared id has a full-width row under the register heading with a listed source (or a derivation), matrix cells per the grammar and an impact from the project's scale. |
| T7a-3 | `check_delta_column` (`:659-673`) | qa-requirements-tester | With a `delta` column, every row carries `new`, `changed` or `unchanged`, and an `unchanged` row does not cite the diff as its observable. |
| T7a-3 | `check_behaviour_claims` (`:690-718`) | qa-requirements-tester | Every requirement seen only in the implementation has exactly one entry under the behaviour-claims heading, with an `origin` from its list and the fields of a claim. |
| T7a-3 | `check_manifest_reuse` (`:753-783`) | qa-requirements-tester | Every path the register cites was recorded in the S1 context manifest. |
| T7a-3 | `check_requirements_review` (`:1060-1078`) | qa-requirements-tester | `requirements-review.md` carries the required front matter, a `mode` and a `verdict` from their lists, and in mode B the matrix fields. |
| T7a-3 | `check_understanding` (`:1933-1954`) | qa-requirements-tester | The understanding file stays within `UNDERSTANDING_MAX_LINES`, has every section of `UNDERSTANDING_SECTIONS`, and names every requirement id in a "What we verify" or "What we do not verify" line. |
| T7a-4 | `check_plan` (`:791-898`) | qa-test-strategist | The plan carries its required fields and TS rows; each row names register R-ids, an impact from the scale with the priority it derives, a non-empty distinguishing observation and a basis per the oracle grammar; the profile is from its list and the front matter counts (smoke rows and the rest) match the table. |
| T7a-4 | `check_plan_v0` (`:1840-1927`) | qa-test-strategist | The `## Plan` table has unique TS-n rows; each names a register requirement, a disposition from its list (with a reason where owed), an observable, an oracle from the list that is not implementation-only, a level from `PLAN_LEVELS` for `automate` (never on a low-value row), and a new behaviour is never judged by `history:` or on `current-code`. |
| T7a-5 | `check_manifest_v0` (`:2155-2209`) | qa-automator, qa-code-critic | Every `automate` case of the plan has a `tests[]` or `unresolved[]` row; a `tests[]` row names an existing file and a `marker` or a full content-bound trace; an `unresolved` reason is from its list; a critic verdict is from its list, with `fix_notes[]` only for `approved_with_fixes`. |
| T7a-5 | `check_manifest_invariants` (`:2215-2247`) | qa-automator | No two `tests[]` entries carry one instance id, no case is green in `tests[]` and present in `unresolved[]`, and no `self_fixes[]` entry repeats an earlier one byte for byte. |
| T7a-5 | `check_remedy_rows` (`:2254-2289`) | qa-automator, qa-runner | A row blocked on the environment carries a `remedy` that is the fix, and names no value of a credential key. |
| T7a-5 | `check_self_fixes` (`:2331-2346`) | qa-automator | A `self_fixes[]` entry carries every required key and never drops a Then line's assertion that was there before. |
| T7a-5 | `check_marker_in_file` (`:2029-2048`) | qa-automator | The marker a manifest row names stands in the test file it names. |
| T7a-5 | `check_phase_json` (`:1711-1730`) | per artifact (`carrier_key`) | `requirement_from: validate_artifacts.PHASE_JSON_KEYS`, one row per artifact, roles = its writer. |
| T7a-5 | `check_context_manifest_v0` (`:2350-2415`) | qa-scout | Every `related[]` entry is an object with a `kind` from `RELATED_KINDS` and a `source`; every `implementations[]` entry is an object naming a `repo` once with a listed `source`; the list keys are arrays or absent. |
| T7a-6 | `check_run_report_empty` (`:1608-1626`) | qa-runner | A run with zero tests carries `env_preflight: blocked`, or names its environment-blocked, manual-check or manual-skipped rows. |
| T7a-6 | `check_run_report_head` (`:1633-1640`) | qa-runner | The run report carries a non-empty `head`. |
| T7a-6 | `check_run_report_v0` (`:2419-2428`) | qa-runner | The run report carries an `execution_status` from its list, computed from the run's own evidence, and `blocked` when `env_preflight` is blocked. |
| T7a-6 | `check_result_rows` (`:2433-2479`) | qa-runner | Every `results[]` row is an object naming one case or a test id, with a status from its list, a reason when skipped, and totals that agree with the rows. |
| T7a-6 | `check_run_report_coverage` (`:2080-2143`) | qa-runner | Every case S5 automated and every manual-agent plan row is accounted for in the run report. |
| T7a-6 | `check_triage_v0` (`:2484-2527`) | qa-failure-analyst | One triage row per observation, a verdict from its list, and a FLAKY verdict only with enough reruns, a listed mechanism and a `fix_result`. |
| T7a-7 | `check_report_sections` (`:1218-1244`) | qa-doc-scribe | Every template section stands, in the template's order, with the verdict and its `delivery_ready:` line above the rest. |
| T7a-7 | `check_report_traceability` (`:1248-1273`) | qa-doc-scribe | Every register requirement and every plan case stands in a row of the traceability appendix. |
| T7a-7 | `check_report_left_with_you` (`:1277-1297`) | qa-doc-scribe | Every `Left with you` item names its requirement and case, what a person would observe, and how. |
| T7a-7 | `check_report_test_marks` (`:1339-1368`) | qa-doc-scribe | Every test line under `Proven`, and every test a `Left with you` item names, carries the real-or-mock mark the ledger records. |
| T7a-7 | `check_report_forbidden` (`:1406-1417`) | qa-doc-scribe | The report carries none of the factory's internal identifiers, and no decision marker without its decision text. |
| T7a-7 | `check_report_human_text` (`:1430-1450`) | qa-doc-scribe | Each `Factory defects` item is written in plain words, as `human-questions.md` asks. |
| T7a-7 | `check_report_gate_b` (`:1454-1473`) | qa-doc-scribe | "Decided at gate B" quotes the person's recorded words for each decision, never a paraphrase. |
| T7a-7 | `check_report_blocks` (`:1496-1554`) | qa-doc-scribe | Every code-owned block stands with its markers, opens with its own heading and holds no section heading; "Decided at gate B" stands only when gate B has recorded words, and never quotes gate A's. |
| T7a-7 | `check_report_coverage` (`:1084-1112`) | qa-doc-scribe | The report's coverage line enumerates the check coverage. |
| T7a-7 | `check_ptr_readiness` (`:904-927`) | qa-doc-scribe | `Readiness within what was verified` gives every register requirement a row with a status from its list. |
| T7a-7 | `check_test_report` (`:1119-1140`) | qa-doc-scribe | `work/delivery-summary.md` is readable and fresh (regenerated when stale). |
| T7a-7 | `check_report_ledger_and_readiness` (`:1976-2022`) | qa-doc-scribe | Hand text outside the generated tables stays within `TEST_REPORT_MAX_BYTES`, section 1 is the table `ledger.py` generated, and a `delivery_ready: yes\|after_checks\|no` line agrees with `ledger.json`. |
| T7a-7 | `check_legacy_report_sections` (`:1173-1182`) | qa-doc-scribe | (legacy form) Every gate-B section stands, in order. |
| T7a-8 | `check_escape_ledger` (`:930-966`), `check_estimation_ledger` (`:1569-1605`), `check_charter` (`:969-999`), `check_charter_form` (`:1007-1057`), `check_nfr_report` (`:1646-1708`), `check_pipeline` (`:1558-1566`), `check_pipeline_v0` (`:2586-2604`), `check_config` (`:2610-2619`) | from `artifact-writers.json` | §5.6 (wave 0) drafts one row per function whose writer is a qa- role; none → conductor-facing |

### 5.3 Rows for T4 (command guards) — written from the bodies (B4)
Ids are `check_of(A24 entry)` (`guard_pre_tool:PT-…`, `stage_guard:SG-…`, `host_adapter:HA-…`) or a sub-id (C14). `stages: ["*"]`;
roles `["*"]` unless stated. Bodies read: `guard_pre_tool.py` lines given; `stage_guard.py:2754-2908`. HA rows are written from the
A24 entries (`refusal_registry.py:495-560`): the `role_policy` body is re-read in §5.6 (wave 0) before T4 starts — the only rows of this
table not yet checked against code.

| # | Check id | Body | When / door_needs | Requirement | Door |
|---|---|---|---|---|---|
| 1 | `guard_pre_tool:PT-command-size` | `:302-319` | shell / none | A Bash or PowerShell command is at most 64 KB (65,536 characters); a longer one is refused before any other check reads it. | split the work into several commands, or write the long text to a file with Write and name the file |
| 2 | `guard_pre_tool:PT-direct-test-run` | `:275-282, 322-341` | shell / shell | Tests are never launched directly (any form of `launch-causes.json` `run_forms`): outside a dispatch through `run_suite.py --task <T> --label <label> -- <command>`, inside an open dispatch only through a typed request; a command that runs no test carries its runner's no-run flag. | `run_suite.py --mine <CASE>` (inside a dispatch); `run_suite.py --template request` prints a request skeleton |
| 3 | `guard_pre_tool:PT-git-config` | `:344-369` | shell / none | A shell command never changes git configuration: `git config` passes only with `--get`, `--get-all`, `--get-regexp`, `--get-urlmatch`, `--list` or `-l`. | report the blocker in your digest; the person decides |
| 4 | `guard_pre_tool:PT-logs` | `:372-503` | always / none | An evidence `.log` or `.junit.xml` heavier than `guards.raw_log_free_bytes` (default 8192 bytes) is never read whole, by Read or by a shell command (a command that mentions `run_suite` is exempt). | read the `<label>-<ts>.json` summary beside the log (`error_head`, failed names); with a shell, `run_suite.py --request <file> --detail <test>` |
| 5 | `guard_pre_tool:PT-plugin-read` | `:506-568` | always / none | A role's Read, Grep or Glob never targets the installed plugin outside its `references/` folder. | read your brief `work/briefs/<ID>.md` and the plugin's `references/` |
| 6 | `guard_pre_tool:PT-big-read` | `:830-891` | always / none | A file over `config.read.max_bytes` is read with `offset`/`limit`, a PDF with a `pages` range within `config.read.max_pdf_pages`, and a picture only up to `config.read.max_image_bytes`. | `Grep -n` for the line, then Read with `offset`/`limit`; a PDF by `pages` ranges |
| 7 | `guard_pre_tool:PT-case-store` | `:905-938` | always / none | When the project declares `cases_root`, a case file is written inside it and nowhere else. | write it as `<cases_root>/<area>/<case id>.md` |
| 8 | `guard_pre_tool:PT-handoff-rewrite` | `:1114-1128` | always / none | A handover form that exists is never rewritten whole by Write. | Write `work/handoffs/<ID>.values.yaml` with `path: value` lines, or Edit one field |
| 9 | `guard_pre_tool:PT-handoff-edit-pending` | `:1096-1105` | always / none | A handover form is not edited while its `<ID>.values.yaml` waits to be applied. | put the field into `<ID>.values.yaml` (rewrite it whole with the field added) |
| 10 | `guard_pre_tool:PT-handoff-code-file` | `:1109-1113` | always / none | `<ID>.values.applied.yaml` and `<ID>.values.stale.yaml` are written by code only. | write your fields to `<ID>.values.yaml` |
| 11 | `guard_pre_tool:PT-handoff-values` | `:1138-1168` | always / none | A Write of `<ID>.values.yaml` lands only when the form with those values merged is ready (every word from its list, every line parses, every path known), or when it fills `blocked.problem`. | rewrite the file with the kept lines and the fixed lines the refusal lists; what you cannot fill goes to `blocked.field` and `blocked.problem` |
| 12 | `guard_pre_tool:PT-artifact-rewrite` | `:1233-1263` | always / none | An artifact that exists with content, and whose `artifact-writers.json` entry carries `rewrite`, is never replaced whole by Write. | the point edit the entry's `rewrite` names (quoted in the refusal) |
| 13 | `guard_pre_tool:PT-plan-rewrite` | `:1284-1317` | always / none (roles: qa-test-strategist) | `work/test-plan.json` that already holds rows is never replaced whole by Write. | Edit one row's lines; with a shell `plan_row.py --task <T> --row <TS-n> --set <field>=<value>` or `--add-row` |
| 14 | `guard_pre_tool:PT-plan-md-rewrite` | `:1318-1338` | always / none (roles: qa-test-strategist) | `work/test-plan.md` that exists is never replaced whole by Write. | Edit the lines that changed |
| 15 | `guard_pre_tool:PT-manifest-shrink` | `:1341-1370` | always / none (roles: qa-automator) | `automation-manifest.json` that holds `tests` or `unresolved` entries is never replaced whole by Write. | `manifest_put.py` (merges by case) or Edit one line |
| 16 | `guard_pre_tool:PT-owner` | `:1430-1520` | always / none | An artifact owned by a role is written only by that role, or while a dispatch of that role is open for the story. | name it in your digest; the conductor sends it back to its owner (`controller.py --operation rework`) |
| 17 | `guard_pre_tool:PT-window-file` | `:1580-1651` | always / none (roles: qa-automator) | When S5 windows run in parallel, a test file another window claimed first is not written by Write, Edit or NotebookEdit until that window releases it. | put your test in a new file in the same directory |
| 18 | `guard_pre_tool:PT-external-writes` | `:1654-1723` | shell / none | No shell command writes to a tracker or a test-management system (a declared `external_writes` command, a tracker CLI with a write verb and object, or an `api` call with a write method). | write a proposal file under `work/proposals/` in the shape `external-writes.md` defines |
| 19 | `guard_pre_tool:PT-human-word` | `:1726-1803` | shell / none | A role never runs a command that records a person's word: `waiver.py --stage` or `--carry-from`, `ticket_adapter.py accept-gap` or `review --record`, `source_exclusions.py --load` or `--revoke`, `stand_identity.py record\|confirm\|forget\|unconfirm`, `environment_record.py record\|revoke`, `project_knowledge.py account\|role\|revoke\|side\|lesson`, `report_adapt.py kind\|forget`, `story_step.py decide`. | return the open point in your digest |
| 20 | `guard_pre_tool:PT-config-write` | `:1884-1894, 2221-2256` | always / none | A role never writes `qa-factory/config.json`, by Write, Edit, NotebookEdit or a shell write shape. | name `launch: <cause>` (or `launch: unknown`) and the evidence line in your digest |
| 21 | `guard_pre_tool:PT-stand-record-write` | `:2259-2280, 2315-2353` | always / none | A role never writes `records/stand-identity.json`, `records/environment-properties.json`, `records/report-adaptations.json`, `records/project-knowledge.json` or a story's `state/stand-confirmations.jsonl`. | hand off as a halt with the row `stand · blocked · <what>` and the evidence line in `blocked` |
| 22 | `guard_pre_tool:PT-walker-error` | `:3018-3027` | shell / none | A shell command is one the guard's command reader can walk. | several simpler commands, or the long text written to a file with Write |
| 23 | `guard_pre_tool:PT-patch-unchecked` | `:3084-3093` | always / none | A write whose content the guard can read; a patch it cannot parse is blocked. | a patch in the host's grammar (`*** Begin Patch` / `*** End Patch`, a path per section) |
| 24 | `guard_pre_tool:PT-unparsed-event` | `:2995-3003` | always / none | (No requirement the role can meet: the host's hook event could not be read.) | try the call once more; the second time the factory records a finding and the conductor is called |
| 25 | `stage_guard:SG-command.opaque` | `:2774-2779` | shell / shell | Inside an open dispatch, a command that launches the runner holds none of the forms the shell reads differently from the guard (`hooklib.SHELL_OPAQUE_BAN`, e.g. a backslash-escaped quote). | write it without that form, or launch `run_suite.py --request FILE` as its own command |
| 26 | `stage_guard:SG-command.typed_runner` | `:2807-2832` | shell / shell | Inside an open dispatch, tests run only through `run_suite.py --mine <CASE>`, `--request FILE` or `--schedule FILE`, with the runner's path and flags written literally (no `$(...)`, backtick pair or `(Join-Path ...)`); `--task/--label` and the default full suite are refused. | `run_suite.py --mine <CASE>` |
| 27 | `stage_guard:SG-command.request` | `:2833-2872` | shell / shell | The `--request` file exists (or the same command writes it), parses, and each request names the running dispatch's `dispatch_id` and selects only instances inside its scope (an instance is in scope when the manifest says it `covers` a scope case). | `run_suite.py --template request`; add the case to `covers` through `manifest_put.py` |
| 28 | `stage_guard:SG-command.commit` | `:2900-2901` (`rule_pathspec` `:2392`, `rule_manifest` `:1035` — bodies in §5.6) | shell / none | A `git commit` names its paths, and a commit of test code waits for the manifest the stage rules require. | name the paths in the commit |
| 29 | `stage_guard:SG-command.stash` | `:2902-2903` (`rule_stash` `:2441`, §5.6) | shell / none | A `git stash` names its paths. | name the paths |
| 30 | `stage_guard:SG-command.delivery` | `:2904-2905` (`rule_delivery` `:1133`, §5.6) | shell / none | A delivery command waits until the stage the stage rules name allows it. | finish the stage first; the refusal names it |
| 31 | `stage_guard:SG-walker-error` | A24 `:789-797` (`check` `:1222`, §5.6) | shell / none | A shell command is one the stage guard's command reader can walk. | several simpler commands, or the long text written to a file |
| 32 | `host_adapter:HA-call-shape` | A24 `:495-503` | always / none | A tool call has a shape the host adapter can read (a command as text or an argv list, one call per code cell, no tty option). | send the command as text or as an argv list |
| 33 | `host_adapter:HA-no-command-text` | A24 `:512-518` | always / none | A shell-family call carries command text the guard can read. | send the command in the fields the refusal names |
| 34 | `host_adapter:HA-role-nested-delegation` | A24 `:519-525` | always / none | A factory role never calls Agent or Task. | name the need in your digest; the conductor dispatches |
| 35 | `host_adapter:HA-role-read-only` | A24 `:526-533` | no_shell / none | A Codex role without Bash runs only one plain read per shell call. | the read in one plain command, or the desktop tools the refusal names |
| 36 | `host_adapter:HA-stdin-chars` | A24 `:534-540` | shell / none | A `write_stdin` call never sends characters to a running process. | a guarded `exec_command` call |
| 37 | `host_adapter:HA-exec-tty` | A24 `:541-547` | shell / none | An `exec_command` call never asks for a tty. | a non-interactive call |
| 38 | `host_adapter:HA-connector-unclassified` | A24 `:548-553` | no_shell / none | A role with no shell never calls an unclassified or mutating connector tool (`mcp__…`). | the desktop tools the refusal names; a write goes through a proposal and gate B |
| 39 | `host_adapter:HA-connector-orchestrator` | A24 `:554-560` | shell / none | A caller with a shell never calls a connector tool that `host_tools.read_only` does not list. | name it in your digest; the conductor registers a verified read-only tool |

No row (E5): HA-patch-* (`:441-494`), HA-command-field-type, HA-event-not-object, HA-tool-input-not-object (re-raised as rows 23, 32, 24),
PT-doctor-probe, HA-doctor-no-tools (probes). G-dispatch (§2.8): SG-resume-*, SG-probe-*, SG-ambiguous-task, SG-explicit-no-story,
SG-explore-*, SG-unreadable-pipeline, SG-role-stage-unset, SG-stage-rules, SG-tracker-route, SG-manifest-delivery, SG-gate-ordered,
SG-manifest-unread, IC-*, NC-*, CR-*, HA-rewritten-input.

### 5.3a Rows for T9a (controller, role-resumed) — re-read round 2 (N9b)

| Check id | Lines read | Roles | When | Requirement | Door |
|---|---|---|---|---|---|
| `controller:s3_plan` | `:7465-7513` | the S3 roles of `stages.json` | always | When your exit window claims S3 complete, the structured test plan passes its contract with no blocking problem (the refusal lists them). | repair the rows the refusal names, change nothing else |
| `controller:code_review_receipts` | `:6443-6463` — body re-read owed (§5.6) | qa-code-critic | always | (draft) Your review of a window carries every receipt the code review requires; each missing one is named and is yours to produce. | add the named receipts to your review record |
| `controller:s5_plan_accept` | `:6857` | qa-automator, qa-code-critic | plan | A plan dispatch never closes S5: it is accepted without `stage_complete` (no `--complete`). | finish the plan dispatch without `--complete` |
| `controller:s5_plan_gaps` | `:6862`; `_plan_rework_rows_problems` `:6886` — body re-read owed (§5.6) | qa-automator | plan | Your plan has no gap the plan check names (the refusal lists up to six). (draft, second clause owed:) a rework changes only the rows the last review named. | repair the named rows of `work/s5-plan.json` |
| `controller:s5_plan_review` | `:6938, 6940, 6945, 6966` | qa-code-critic | plan | Your plan review does not contradict itself, is stamped on the plan bytes now on disk, reuses no remark id of an earlier review, and leaves no blocking remark undecided. | rewrite the review on the current plan with new remark ids |
| `controller:s3_window1_close`, `controller:s3_grounding` | `:7479`, `:7515` | only if M7 finds a road | — | (if in) A window-1 (labelling) dispatch of S3 never closes the stage; every grounding finding is answered. | per M7 |

### 5.4 Rows for T5 (S5 chain) — written from the bodies (B4)
`stages: ["S5"]` (S6 where the family runs there), roles `qa-automator` unless stated; door unless stated: "repair every problem the
refusal lists, each by its `fix` line".

| # | Check id | Lines read | When / door_needs | Requirement | Door |
|---|---|---|---|---|---|
| 1 | `s5_precheck:manifest` | family `:13`; `check_manifest` `:1006-1176` (findings lines; messages to be confirmed by T5 against the body) | always / none | The manifest of this dispatch's cases keeps the invariants `manifest_put.py` owns (one instance per id, a covering row per scoped case), as a hand edit would break them. | each finding's `fix` |
| 2 | `s5_precheck:row_fields` | `check_row_fields` `:3798-3842` | always / none | `requirement_from: window_record.REQUIRED_ROW_FIELDS` (one row; if N0's label must stay `manifest`, T5 returns the sub-id as a question) | add the named field to the row through `manifest_put.py` |
| 3 | `s5_precheck:bindings` | `:14-15`; `check_bindings` `:1233-1380`; `check_then_remainders` `:1512-1629` | always / none | Every Then clause of every case in scope is bound to a test and an assertion (`then_bindings`), or is a remainder the person took (`then handed:`), named. | bind the clause, or name the remainder |
| 4 | `s5_precheck:oracle` | `:16-20`; `check_open_oracle_asserted` `:1667`; `check_expectation_changes` `:1761`; `check_case_is_oracle` `:1848` | always / none | A test never asserts an expected value the case left `open` or `invalid`; a test that went red and later passed on changed code has an `expectation_changes[]` record whose `then_refs` resolve; an unresolved row never disputes the approved case. | each finding's `fix` |
| 5 | `s5_precheck:run_mapping` | `:21`; `check_run_mapping` `:1923` | shell / shell | Every test of the scope has a reporter row in its run block. | `run_suite.py --reparse-block`, never a rerun |
| 6 | `s5_precheck:environment` | `:26-28`; `check_environment` `:3525`; `check_env_evidence` `:3693-3696` | always / none | A `blocked_by_env` row of this dispatch carries the fix it found (`remedy`), names no credential value, blames the stand for no fixture the approved case never asked for, and stands on a run that shows the stand. | each finding's `fix` |
| 7 | `s5_precheck:obligations` | `:29-30`; `check_obligations` `:3843-3846` | always / none | Every coverage obligation of the plan row a scoped case belongs to has an `obligation_bindings[]` row, under the plan's own id, reaching that case. | add the binding through `manifest_put.py` |
| 8 | `s5_precheck:plan` | `:32-34`; `check_plan_conformance` `:4447-4450` | window / none | On a plan-form S5, the window's tests match its slice of the plan, unless a `deviations[]` row of the window's form declares the difference. | match the slice, or declare the deviation |
| 9 | `s5_precheck:sides` | `check_sides` `:2371-2391` (body re-read owed, §5.6) | always / none | (draft) On a story whose sides are not all real, rows follow the story's sides record. | each finding's `fix` |
| 10 | `execution_request:purpose` | `:126-128` | shell / shell | `purpose` is one of `PURPOSES` and never `impact_regression`. | `run_suite.py --template request`, or `run_suite.py --mine <CASE>` |
| 11 | `execution_request:selection` | `:132-139, 298, 304` | shell / shell | `selected_instance_ids` and `current_scope_instance_ids` are string arrays, every selected instance is in the approved current scope, a behavioural request selects at least one, and only supported selectors are used. | same |
| 12 | `execution_request:budget` | `:141-143` | shell / shell | `remaining_budget` is a non-negative number, and above zero for new behavioural execution. | same |
| 13 | `execution_request:freshness` | `:145` | shell / shell | `freshness` is `fresh`. | same |
| 14 | `execution_request:runtime` | `:149-195` | shell / shell | `runtime_provenance` is present, its `profile_id` matches the selected profile and it is matched or person_confirmed; a runtime-required request carries a read-only `runtime_probe` with a non-empty argv, an existing cwd and a positive timeout. | same |
| 15 | `execution_request:fingerprint` | `:199` | shell / shell | `fingerprint_components` carries `source_sha`, `test_content_sha` and `config_sha`. | same |
| 16 | `execution_request:command` | `:207-264` | shell / shell | `command` is an object with a non-empty string `argv`, an existing `cwd` and a `reporter` from `REPORTERS`; a behavioural request never runs a full suite; a command that runs tests declares `runs_tests`; an external reporter carries `{report_path}` in exactly one argv token and in `report_path`; `env` and `selector_join` follow their shapes. | same |
| 17 | `execution_request:execution` | `:273-292` | shell / shell | `execution` has `schema_version` 1, a reporter equal to the command's with a job-isolated `{report_path}`, a `data_seed_contract` with `result` and `evidence_refs`, and a `selection` with a typed reason and non-empty `evidence_refs`. | same |
| 18 | `execution_request:selector` | `:296-330` | shell / shell | A behavioural command has a verified adapter selector contract and framework `selector_args`: non-empty string arrays, never holding `{report_path}`. | same |
| 19 | `execution_request:instance_contracts` | `:338-354` | shell / shell | A behavioural request carries `instance_contracts`, each with a `report_test_id`, object `parameters` and a `report_id_source` that proves the reporter id, and no reporter id maps to two instances. | same |
| 20 | `manifest_put:colliding_ids` | `_refuse_colliding_ids` `:505-509` | shell / shell | Two rows of one fragment that resolve to one instance id never name different test files. | rename one function or split the fragment, then `manifest_put.py` again |
| 21 | `manifest_put:novelty` | `:531-535` | shell / shell | A `tests[]` row carries `novelty` only as the whole row form `manifest_from_tests.py` writes (an object with `measured_on` and `measured_by`, no `resolved`). | leave `novelty` out; code writes it |
| 22 | `manifest_put:base_outcome` | `:569-572` | shell / shell | `base_outcome` is `{"outcome": refused\|working, "run": <non-empty run id>}`. | same command, fixed value |
| 23 | `manifest_put:obligation_hash` | `:592-596` | shell / shell | A row never sends an `obligation_hash` the code did not build (`content_hash(obligation_refs)`). | leave it out; code writes it |
| 24 | `manifest_put:helper_rows` | `:630-634` | shell / shell | An `introduced_helpers[]` row has `file`, `name` and the four role fields as strings, `novelty` (new, changed or unknown) only when the writer sent it, and no other key. | same command, fixed row |
| 25 | `manifest_put:provisional` | `:717-721` (row form in the body, re-read owed §5.6) | shell / shell | (draft) `provisional` is a list of rows in the registry's provisional form. | same |
| 26 | `manifest_put:unknown_obligation` | `:1021-1025` | shell / shell | `obligation_bindings[]` name only obligations the plan names, in the plan's own spelling. | copy the obligation ids from the plan |
| 27 | `manifest_put:then_remainder` | `:1126-1130` | shell / shell | A Then-level hand-off row has the contract's Then-remainder form (a case with a whole-case `unresolved[]` row keeps its echo rows). | same |
| 28 | `manifest_put:expectation_changes` | `:1207-1211` (field rules in the body, re-read owed §5.6) | shell / shell | (draft) Each `expectation_changes` row carries the fields its contract names, in their shapes. | same |
| 29 | `manifest_put:retract` | `:1488-1491` | shell / shell | `retract` never names `tests`, `unresolved` or `obligation_bindings` (never replaced whole) and is otherwise well formed. | change those keys row by row |
| 30 | `manifest_put:critic_approval` | `:1684-1688` | shell / shell (roles: qa-code-critic) | A row never turns a stored `critic_verdict: unverified` into `approved` without a non-empty `critic_note`. | add the `critic_note` |
| 31 | `manifest_put:assertion_line` | `:1720-1724` | shell / shell | Every `assertion_id` `<file>:<line>` stands on a line that holds a check (`probe_by_code.check_on_line`). | point the id at the assertion's line |
| 32 | `manifest_put:ghost_rows` | `:2170-2174` | shell / shell | A fragment never binds a Then to an id it retracts in the same fragment, and never sends a ghost row of an instance the manifest retracted. | drop the row or the retract |
| 33 | `manifest_put:revision` | `_refuse_unmergeable` `:2196-2200` | shell / shell | `expected_revision` equals the revision the manifest file shows now. | read the file's revision and send again |
| 34 | `run_suite:phantom_story` | `:964-969` | shell / shell | `--task` names a story that exists (for `--detail`, `--wait` and the untyped run). | the task id of your prompt |
| 35 | `run_suite:detail_target` | `:1102-1107` (body re-read owed §5.6) | shell / shell | (draft) `--request FILE --detail TEST` names a request with a recorded run. | the request file of the run you ask about |
| 36 | `run_suite:untyped_story_run` | `:1407-1412` | shell / shell | A run for a story uses a typed request, never the untyped `--task/--label` run while a dispatch is open. | `run_suite.py --mine <CASE>` |
| 37 | `run_suite:missing_executor` | `:1552-1557` | shell / none | The launcher of the run's profile exists in this session (else the run stops with a three-option question for the person, exit 3). | hand off with the question as printed |

No row: `_problems_text` (`:1119-1123`, a renderer); the `smell` family (advice).

### 5.5 Rows for T9c (conductor launch, O1) — written from the bodies
`roles: ["conductor"]`, `stages: ["*"]`, `door_needs: "none"`.

| Check id | Lines read | When | Requirement | Door |
|---|---|---|---|---|
| `no_move:options` | `no_move.py:414-457` | conductor_answer | An `ask_person` or `stop` answer carries a list of at least two option objects (one only for the `rework` option after the person chose rework); each has a unique non-empty token that is its open move's own token (or a word the question already takes, as `site_door`), never a move that is not open or never offerable, and `says`, `factory`, `person` lines and a `story` object. | fix the options and answer again |
| `no_move:prose` | `:458-460` (`prose_refusal` `:339`) | conductor_answer | The question names, in any quote style, no token of the closed vocabulary that is not one of its options. | rephrase or offer the token |
| `no_move:class` | `:461-467` | conductor_answer | A question names a class of `references/person-owned` questions in `why_person` and what you read in `checked`. | add both fields |
| `no_move:args` | `check_args` `:228-254` | move:rework_stage | The `rework` option's `args` name a stage that can be sent back, a role that did accepted work there, cases inside the approved scope (at least one from S4) or plan rows (never both), and a cause from the list. | take the values from the list under "Moves open here" |
| command rows per move | `conductor-actions.json` `moves[].run` | move:<id> | §5.6 (wave 0): one row per code check of the command each move runs (e.g. `controller.py --operation rework` for `rework_stage`, `waiver.py` for the passes it names) | — |

### 5.6 Owed designer drafts (wave 0, before wave 3; accepted by the Lead)
One draft file, rows in the form above, each written from the body with file:line: T6 `handoff_check.py` problem builders; T7a-8 (8
functions); T7b-f (5 files); T5b `MineRefusal` sites; `run_suite.py` `main` `invalid_*` prints (`:2740, 2771, 2857, 2904`) and
`resolve_detail_target`; `first_look.py put` (rows `first_look:put…`, `when: first_look`, qa-runner; N4); the 9 legacy legs (re-legged
to the page, N6); `host_adapter.role_policy` body against rows 32-39; `stage_guard` `rule_pathspec`/`rule_manifest`/`rule_stash`/
`rule_delivery`/`check` against rows 28-31; controller `:6443-6463` and `:6886` (§5.3a drafts); `s5_precheck.check_sides`;
`manifest_put` `provisional_row_problems` and `expectation_change_problems` bodies; the command rows per conductor move (§5.5).

## 6. Four questions (CLAUDE.md rule 10)

(a) **Cost and who pays.** Package: one dict lookup per in-process refusal; pages grow by the rows of the role (T0 M5), split by §2.6a;
the conductor prompt grows by the rows of its open moves; the brief shrinks; every growth raises `process_ratchet_tokens` by name. Authors
of a new refusal pay one row + one literal id + `contract_slices.py --write`. Migration: one night, 25 builder nodes in 7 waves (§5.0), one
critic pass per topic. Roles and the conductor pay fewer refused calls.
(b) **Axes** (`docs/SIBLING_MAP.md`, 36 axes): axis 1: n/a. axis 2: n/a. axis 3: covered — CHANGELOG fragment per node. axis 4: covered —
FR-38 *Check:* (T10). axis 5: covered — S5 windows ↔ S6 rows symmetric (T5/T7a). axis 6: queued — P1-v reads check ids. axis 7: n/a.
axis 8: covered — hook and driver roads inject the page through `collect_blocks`; the prompt line is built by the one card renderer for
both. axis 9: n/a. axis 10: n/a. axis 11: covered — shell recognizers' refusals (T4) route through the constructor. axis 12: covered — waves
by the Lead. axes 13-15: n/a. axis 16: covered — `hooklib.read_json`. axis 17: covered — Record attributes, `spoken`. axis 18: covered —
new counters (T10). axis 19: covered — `role_has_bash`. axes 20-22: n/a. axis 23: covered — `REQUIRED_ROW_FIELDS` one renderer. axes 24-25:
n/a. axis 26: covered — word matching unchanged. axis 27: n/a. axis 28: covered — the page and the conductor section are the told render
sites, one line renderer `told_line`. axes 29-30: n/a. axis 31: covered — the page owns "what code checks"; `role-rules.json` joined.
axis 32: covered — one scanner, one switch, census set passed by the test. axis 33: n/a. axis 34: covered — one road per receiver kind,
rows keyed by check id and tokens, never by role or language name; conductor-only groups excluded by road with reasons. axes 35-36: n/a.
(c) **Detector.** `stage_joints.py --check`, `test_stage_joints.py` (CI `--contracts`); `contract_slices.py --check` (`--slices`);
`role_rules.py --check`; K10 with the role-load checks; P1-b C11; P1-v G1; a calibration check (T10).
(d) **What stops skipping.** A new transport without `refusal()` raises `bare` → red; a blocking unit with no seen site → `untold` red;
a constructor call without a row → K1 red; a row not on a reached page → K2 red; a stale page → `--slices` red; a page over 80 % → K8;
a role over its headroom → K10. On discipline only: the truth of a sentence and the swap road (J1/J2; detector: the calibration check).

## 7. Crossings with work in flight

| Work | Join |
|---|---|
| P1-v N0 (`20261113-p1v-run-scoreboard-spec.md:125-188`) | ONE producer of `Record.check`/`check_id`/`with_check`/`Refusal.checks`; T2 builds on it; N0's byte-identity invariant holds. Wave 1 |
| P1-v R-8 / F18 | controller refusals stay `unknown` in the scoreboard until P1-v carries their id; T9a gives them rows |
| P1-v G1 / F15 (a) | transports print `  check: <id>` last |
| P1-b (`20261113-p1b-dry-story-spec.md:75-87`) | ask: C11 (owner data, class xref) calls `rows_for`; C1 follows the T1 rename |
| FV1-27 | closed by T4 rows 2, 11, 25 |
| FV1-18, FV1-19 | wave 1, before T5 |
| FV1-4 / amendment B4 (`20261113-p1-specs-amendment-owner-words.md:529-585`) | removes the brief ladder; the Codex 100000 ceiling is the same class — Appendix A asks the same owner direction for it |
| FV1-30 | orthogonal |
| `field_cards.py` proposal | absorbed into `contract_slices` (`requirement_from` + `told_text`) |
| `ahead-cards.json` + `test_ahead_cards.py` | all 12 cards migrated by T1r; pin removed (T3a) |
| driver resumes (0.17) | T0 M9 decides; a `system_file` on role resumes is the driver owner's node if M9 says lost |

Shared files after the cut: `stage-joints.json`, pages, `role-load.json`, `role-rules.json`, `ahead-cards.json`: T1 → T3a → T1r → (closing)
only. `judgment-census.json`: T4 (wave 4) → T9c (wave 3, its own rows) / T9a (wave 6) — different functions' rows, waves serialise them.
`brief_pack.py`: P1-v N3, RC2-1/2, FV1-4 → T3b. `contract_slices.py`: T1 (`_keys_outputs`) → T3a. `inject_context.py`: T3a (`collect_blocks`,
`_dropped_headings`, `map_problems`) and T4 (census relabel only). `execution_request.py`: T5 (`validate_request`) and T5b (`MineRefusal`
functions). `hooklib.py`/`stage_guard.py`: T2 (`block`/`deny`) and T4 (other functions). `controller.py`: T9a functions only.

## 8. Small choices closed by the designer

C1 `WIDE_TRANSPORTS`/`RECORD_SINKS` are code constants. C2 roles `["*"]` = roles of `inject-map.json`; `conductor` only by name. C3 section
headings `## What code will check of you` (page) and `## What code will check in this launch` (conductor). C4 zero-row sections print one
line. C5 the spike's measurer is the scanner's own flags. C6 `check_of` computes A24 ids. C7 baselines in `told_ratchet`. C8 `when` is AND.
C9 transports print `  check: <id>` last. C10 readers stay in `stage_joints.py`. C11 the split is added by a HAND line in `inject-map.json`
(the established workflow for slice entries, `inject-map.json:3`), never by the generator — `inject-map.json` keeps one writer (AR-14).
C12 `W` = 80 % computed from the imported constant. C13 `when_exclusive` is data; the `(replaces …)` heading text is generated from it.
C14 a split A24 row uses sub-ids `<check_of>.<part>`; the A24 id needs no row when every site of its function carries a sub-id. C15 the
conductor's rows live in the launch prompt, not in `conductor.md` (static, not launch-specific). C16 K10's reserve of 200 characters is an
estimate replaced by T0 M10's measurement.

## 9. Forks — Lead

| # | Fork | Options and consequences | Recommendation |
|---|---|---|---|
| F4 | (decided by the owner, O1, 13.11.2026: «если заранее известно, что проверит код в данном запуске дирижёра, то добавляем ему…») | the conductor is IN for launch-known checks (§2.9); the rest counted per group with reasons (§2.8) | closed |
| F15 | K10 on day one: a role may already be over its worst-case headroom (two project entries) | (a) record today's `U` per role as a shrink-only baseline `native_headroom.<role>` in `role-load.json`; growth above it red, the message names Appendix A's finding (the owner removes the run ceiling) · (b) red at once: T1r cannot land rows for those roles until the ceiling finding is fixed · (c) count only the measured project files of the stand (not portable: a dev-time check cannot know a project, AR-4) | **(a)**: no role is blocked tonight by a ceiling this spec does not own, and no growth passes silently |
| F16 | `conductor-actions.json` `precondition`/`forbidden_when` texts may restate what a move's command refuses | (a) keep them as move data the conductor judges (P22); J1 checks no contradiction with the rows · (b) replace restating clauses by the rows (`requirement_from: conductor-actions`) — a second renderer of move rows | **(a)** |
| F20 | O1 extends the told carrier to the conductor (a second receiver kind) | (a) the Lead checks it against this file (one renderer, one seam, AR-17 kept) · (b) a critic pass on §2.8-§2.9 only | **(a)** unless the Lead reads it as an architecture change; then (b), one topic pass |

## 10. Questions for the owner (plain language)

None open: Q1 answered (O1), Q2 answered (O2). F15 is the Lead's; if the Lead wants the owner's word on the native-context ceiling, the
question is Appendix A's finding.

## 11. Trail

Read in fix round 2 (read-main `pkg:` unless noted): the spec (whole); the second verdict (whole); `scripts/inject_context.py:40-289,
412-424, 569-603, 604-748`; `references/inject-map.json` (whole); `scripts/native_context.py:150-219`; `scripts/role_load.py` `def` list +
`:453-527`; `references/role-load.json` Grep `allowances|packet|launch`; `scripts/story_step.py:230-330, 445-484, 1060-1170` + Grep
`_prompt\(|_resumed_lines|brief_pack|RESUMED_PREFIX`; `scripts/brief_pack.py:4116-4195` + Grep `s5_kind =|_record_kind|first_look =|walking =|
def build`, Grep `_s5_kind|FIRST_LOOK_*|ahead_card|walk_rec`; `scripts/driver_machine.py:510-564`; `scripts/refusal_registry.py` Grep entry
ids + `:300-812`; `scripts/guard_pre_tool.py` `def`/`block(` list + `:270-569, 830-939, 1069-1370, 1430-1520, 1580-1810, 1884-1925,
2221-2355, 2995-3094`; `scripts/stage_guard.py` `def` Grep + `:2754-2983`; `scripts/validate_artifacts.py` Grep of every `def check_` and
`errors.append(` line (295 lines, whole output); `scripts/s5_precheck.py:1-90` + Grep `def check_*` with 3 lines; `scripts/execution_request.py`
Grep `def |errors.append|raise`; `scripts/manifest_put.py` the 15 `def`s with 4 lines; `scripts/run_suite.py` the 4 `def`s with 5 lines;
`scripts/controller.py` Grep `raise StateConflict\(|problems.append` (lines `:6521-6966, 7479-7515` read from its output);
`scripts/driver_conductor.py` Grep `def |prompt|system_file` + `:240-349`; `scripts/no_move.py:40-69, 175-289, 397-497` + `def` list;
`references/conductor-actions.json:60-99` + Grep `"id"`.
Not read this round (owed in §5.6): `host_adapter.role_policy` body; `stage_guard` `rule_pathspec`/`rule_manifest`/`rule_stash`/
`rule_delivery`/`check`; controller `:6443-6463`, `:6886-6925`; `s5_precheck.check_manifest`/`check_sides` bodies beyond their finding lines;
`manifest_put` bodies beyond docstrings; `run_suite.main` prints; `handoff_check.py`; `first_look.py`; T7b-f files; `hooklib.shell_opaque_found`
(cited by line from round 1); `role_load` caller of `process_ratchet_problems` (T3a names it); FV1-4's finding file (not opened; Appendix A
refers to it by its id, as the brief gave it).
Carried from earlier rounds, not re-read: `docs/SIBLING_MAP.md` axes; `plans/builder-rules.md:14-22`; `docs/TESTING.md:36-65`; `selftest.py:558`;
`forge-check.yml:172`; `window_record.py:155-199`; `waiver.py:202-241`; `hooklib.py:2005-2074`; `execution_request.py:286-299`.
Needed beyond the manifest: `role_load.py`, `role-load.json`, `guard_pre_tool.py`, `stage_guard.py`, `execution_request.py`, `manifest_put.py`,
`run_suite.py`, `s5_precheck.py`, `driver_conductor.py`, `no_move.py`, `conductor-actions.json` — load-bearing for B2-B4 and O1.
Re-read: the finished file was re-read once after writing (designer's DoD item 6).

## Appendix A — finding text for the Lead to file (class of FV1-4)

Title: In-run size ceiling of the injected context blocks a role (Codex native packet, 100000 characters).
Type: factory defect, class of FV1-4 (owner: no ceiling inside a factory run; the forge watches size).
What: `native_context.stage` raises `ValueError('Native context exceeds 100000 characters; …')` (`scripts/native_context.py:174-175`,
A24 `NC-context-too-large`), and `inject_context.dispatch` refuses the role launch (`refuse_native_stage`, `scripts/inject_context.py:729-730`).
The context is the role file + every injected slice + every `project:` file (each up to `MAX_BLOCK_CHARS` = 26000) + the task packet; the
plugin share is fixed by the release, the project share is not, so the forge cannot prove at dev time that no project trips it. Measured by
the second critic of the told-before-work spec (13.11.2026, estimate): qa-automator plugin share about 58000 with one project entry; roles
with two project entries have about 42400 of worst-case headroom.
Why it matters: a role is refused at run time for the size of text the factory itself assembled — the case the owner's word forbids.
Sibling: `inject_context.MAX_BLOCK_CHARS` refuses a dispatch whose one injected file is larger (`inject_context.py:267-277`) — same class
for `project:` files (plugin files are held at dev time by K8 of the told-before-work spec).
What to change: decide with the owner the run-time move when the assembled context is over the host's limit (no silent cut, FR-59): e.g.
deliver `project:` files over a share by path with a line to the role, or split the packet; the dev-time K10 of the told-before-work spec
stays the forge's watch over the plugin share.
Decision of the owner needed: yes.

## Fix round 13.11

| Finding | Fix | Section changed |
|---|---|---|
| B1 two existing carriers | key page established as survivor; one renderer `told_text`; brief section removed; role-rules joined; prose not a K2 leg | 0.5, 0.6, 0.7, 1.1, 1.2, 2.0, 2.2, 2.3, 2.6, 2.7, E6, E14–E16, T1, T3, §7, F12–F14 |
| B2 cross-process text | form-1 and cross-process texts byte-identical; expected/door only from `block`/`deny`/`refuse`; I-R rows | 2.0, 2.4, E9, E10, T2 (e), T5, T6, T9 (b), §7 N0 |
| B3 controller reaches a role | fact 0.4; road rule; role-resumed units in with rows; relabels; Q1 rewritten | 0.3, 0.4, 2.0, 2.8, E3, E5, E17, T4, T9, 5.2, Q1 |
| B4 scan errs toward missing | no list-name filter; blind spots; `sys.exit`/`SystemExit`/`sys.stderr.write`; `untold` (K6) | 0.9, 1.2 K6, 2.4, 2.5, T0, T1 (d) |
| B5 stringifying transports | `run_guarded` passes a Record; `RECORD_SINKS`; row per sink | 0.2, 2.4, T2 (f)(h) |
| B6 second reader | `_keys_outputs` through `load_rows`; readers listed | 0.8, 2.3, E6, T1 (i) |
| N1 role filter test-side | K4–K6 and `conductor_only` in the test | 1.2, E3, T1 (d)(e) |
| N2 told ∩ when; census ownership | K2 per role ∩ capability; T4 owns its census rows | 1.2 K2, E2, T4 |
| N3 E12 false | ceilings named; FV1-4 dependency; K8; role-load raises | 0.10, E12, 1.2 K8, §7 |
| N4 T0 gate undefined | walk error; `--census` join | 2.5, T0 |
| N5 second switch | `wide` in `raise_family` | 0.9, 2.5, T0 |
| N6 second writer | `refusal` through `with_check` | 1.1 AR-14, 2.4, T2 (a) |
| N7 swap road | per (file, function); accepted limit | 2.5, 1.2 K4 |
| N8 FR-12 | `door_needs` × `when` × `role_has_bash` | 1.1 AR-9, 1.2 K3, 2.2 |
| N9 T7a too coarse | eight sub-nodes; rows drafted | T7a, 5.1 |
| N10 walker on hook path | light readers, import row | 2.3, T1 (h), C10 |
| N11 orphaned sites | T4/T5 function lists | T4, T5 |
| N12 ceiling pin | `CARD_MAX_BYTES` removed | 2.0, T3 (i) |
| N13 fallback ids | `unlabelled`/`unknown` need no row | 1.2 K1, T1 (b), §7 |
| N14 stale facts | census 1142, `sites :1187`, brief_pack lines, test-layers lines | 0.3, 0.9, 0.10, 0.14, §4, 2.4, T2 (g) |
| K9 F2-a pins / F7 role-rules / F9 | pins named; anchors re-pointed; C11 calls `rows_for` | T1 (f), 2.7, E14, §7 |

### Fix round 2, 13.11

| Finding | Fix | Section changed |
|---|---|---|
| B1 kinds drop can cut the section | `INLINE_SUBJECTS` + `inline_subject` read by `named_instead`, `_dropped_headings`, `map_problems` (K11) and the on_demand weight report; a drop row on the key page refused and ignored; T3a row (g) with the critic's fixture | 0.15, 1.2 K11, 2.0, 2.6, E18, T3a (g) |
| B2 size undecided | size rule with one move per state (`W` = 80 %, split by a hand line + `--write`, partition by stage order, never mid-row, edges with invariants); T0 M5 end state per role (estimate labelled); Codex 100000 named, K10 with formula and carriers (`role_load.static_load`, `allowances.packet`, `entries_for`), F15 for day-one excess; Appendix A finding text; dependency declared, ceiling not removed | 0.10, 1.2 K8/K10, 2.0, 2.6a, 2.6b, E12, E19, E20, T0 M5/M10, T3a (d)(e)(j), T1r (d), §9 F15, Appendix A |
| B3 exclusive groups only via the brief | one function `brief_pack.dispatch_groups` (facts moved out of `build`) called by `build` and `story_step._card_text`; the line in `_prompt` outside the `not resumed` branch (resumed reworks get it; driver resumes keep it in the conversation, M9 checks); `when_exclusive` data, headings name what they replace; error direction of the reused facts; T3b row per fixture incl. a resumed one. No fork: no second reader needed | 0.16, 0.17, 2.2, 2.4 (3), 2.6, E23, T3b (b)(c), C13 |
| B4 T4/T5 sentences missing | §5.3 (39 rows) and §5.4 (37 rows) written from the bodies with file:line; split rows by sub-id (C14); rows whose body was not readable this round are marked and owed in §5.6 (wave 0) | 5.3, 5.4, 5.6, C14 |
| N1 driver resume unverified | T0 M9 (one experiment, both the appended system prompt and the first user prompt); "estimate, not verified" on the resume delivery; both worlds stated | 0.17, 2.6, E22, T0 M9, §7 |
| N2 on_demand weight report | moved to `INLINE_SUBJECTS` | 2.6, T3a owns, T3a (f) |
| N3 inherited no-context roads | named in §3 | E21 |
| N4 `FIRST_LOOK_AHEAD`/`FIRST_LOOK_DOD` | AHEAD removed with the ahead section; DOD keeps its deliverable sentence, loses the check clause; `first_look:put` rows (wave 0) on the first-look group | T3b owns/(e), 5.6 |
| N5 AR-13 check fails on `selftest.py:722` | T1 moves that read onto `load_rows`; the grep narrowed to code reads with a positive control | 0.8, 1.1 AR-13, 2.3, T1 (j) |
| N6 legacy legs without owner | all 9 re-legged by T1r tonight (O2), sentences in §5.6 | E16, T1r (b), 5.6, §2.0 F13 |
| N7 M7 regex | controller-side part `S\d structured .* invalid`, case-insensitive, controls `:7513`/`:3203`; `:7479`/`:7515` reported by road | 0.4, 2.8, T0 M7, 5.3a |
| N8 census set; blind spots whole | (a) `raise_family(..., blocking=)` passed by the test, `None` counts no list site and says so; (b) `judgment-census.json:3` is the one carrier, copied whole by T0 | 0.9, 1.2 K4, 2.5, T0 (d)(f) |
| N9 page leg owner | T1 implements the leg gated on `contract_slices.requirement_section`; T3a's attribute enables it | E6, T1 (k), T3a owns |
| N9b §5.1 sentences | every T7a sentence re-written against the body's refusal lines with file:line (`check_understanding`, `check_manifest_invariants`, `check_context_manifest_v0` and 20 more corrected); §5.2 (now §5.3a) re-read for 4 of 6 rows with lines, 2 marked owed; the "from memory" phrase removed | 5.2, 5.3a, 5.6 |
| N10 T3 size | T3a (page, size, inline set, K10) → T3b (brief, prompt line); the world between them over-tells, never under-tells | E6, 5.1 T3a/T3b |
| N11 Q2 count | superseded by O2: Q2 removed; the node count (25) and waves stated in §5.0 | §5.0, §10 |
| O1 conductor launch | owner's word in the header and §9 F4; rows enter in `no_move.moves_section` selected by `open_ids` (`conductor_answer`, `move:<id>`); conductor-only groups with reasons; T9c real node; census relabels | header, 0.18, 1.1 AR-15/AR-17, 1.2 K2/K3, 2.0, 2.2, 2.3, 2.8, 2.9, E3, E24, E25, 5.1 T9c, 5.5, §9 F4/F16/F20, §10 |
| Lead acceptance, 13.11 (t-472) | Fix round 2 accepted against review-2, no third critic pass (no architecture change). Forks: **F15 (a)** shrink-only per-role baseline `native_headroom.<role>`; **F16 (a)** move texts stay data the conductor judges; **F20 (a)** Lead check — one renderer, one seam (`no_move.moves_section`, one caller `driver_conductor.py:684`), AR-17 kept; the code critic of T9c reads §2.8-§2.9. Wave 0 (§5.6) dispatched to a designer as t-480. Wave 1 as launched differs from §5.0: T0, P1-v N0 run with P1-a N0, P1-v N3, P1-v N5, FV1-30a; FV1-18 and FV1-19 take the first freed slots (needed before T5, wave 4). Appendix A finding is filed by the Lead | §9, §5.0 |
| O2 close everything tonight | waves 0-7 with parallel builders ≤ 6, merge orders; the rows-first cut (T1r lands all rows, migration nodes switch call sites; `unsited` ratchet, E11 both worlds); declared gaps limited to four reasoned classes; T9a no longer after T7b | §5.0, 1.1 AR-20, 1.2 K12, 2.0, E11, E16, 5.1 T1r/T5b, §7, §10 |

## T0 gate — Lead decision, 13.11.2026 (t-473): NARROW, wave 2 goes on with three changes

Carrier of every number: `.claude/worktrees/tbw-t0/docs/tasks/specs/reports/20261113-told-before-work-spike.md` (branch `wip/tbw-t0`, c973298).

| gate number | measured | bound | reading |
|---|---|---|---|
| walk errors | 0 / 279 files | ≤ 5 % | go |
| M3 precision of the stderr transport | Lead classified the 27 counted sites of the sample: refusals 17 (#1, 7, 13–16, 20–30), notes/progress 10 (#3–6, 8–10, 17–19) = 63 % | ≥ 80 % | **narrow** |
| census join over site units | 732 / 848 = 86.3 % | ≥ 90 % | below the bound; all 116 rowless units exist only through the new transports (90 stderr-only, 22 refuse-only, 4 both); over census-visible units 732 / 732 |
| M4 | 3 yes / 3 no | "mostly no" → narrow | borderline |

Decision ("решила сама", shown to the owner): not a stop — the join shortfall is made of one cause the narrowing removes or T1 closes, and the scan itself reads every file.

1. **Stderr transport narrowed (binding for T1).** A `print(..., file=sys.stderr)` / `sys.stderr.write` is a refusal site only when the NEXT statement of the same block is a failing `return` (non-zero / an `EXIT_*` name) or `sys.exit(<non-zero>)` / `raise`. On the sample this keeps all 17 refusals and drops all 10 notes (17/17). A stderr print not followed so stays a named blind spot with its count, never a site.
2. **T1 re-measures the join first.** After (1), T1's first step prints the join again; every unit still rowless gets a census row in T1 (a NAMED raise of the census count in the verdict, AR-20 — these are CLI entry points such as `manifest_put.py:run`, `stage_done.py:run` that roles do reach, so "unknown reach" is not acceptable for them). T1 stops and returns if the join after rows is under 100 %.
3. **`check_of` keeps its name**; its census row (`shape`, `["conductor"]`, `data`) is added in T1 together with the function (T0's non-goals forbade the fixture). The `--wide` CLI importing `test_judgment_census.units_of` for the blocking set is accepted as a dev-time path and goes to the code critic of the topic as an open layering question (FR-44).

Carried into later nodes: T2 — the name `refusal` already exists in `session_identity`, `role_digest`, `onboarding_notes`, `exit_gate`; the scan tells them apart by binding to `detector_verdict`, and the constructor's own pass-through of the check parameter is exempted by name. T3a/T3b — M5: a row per SITE does not fit (35.7K–47.8K per role against 26000); a row per CHECK is what ships, and role-command rows are told only for the commands the role calls (all 31 whole = 28.4K). §2.6a split pages stay the move. T4 — M7: road (b) has 3 controller units, not 5; `_code_review_refusal` has no census row. M8: dispatch-time units are conductor-facing; `check_command` and `rule_*` stay role-facing.
Still owed by the Lead: experiment M9 (resume of `claude -p` with the attached page) before T3b.

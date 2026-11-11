# t-2045 / TR2-14 — one probe road for every language (revised by t-2050, task t-2054)

Status: REVISED DRAFT for Lead acceptance. This text answers the critic's plan review `docs/tasks/specs/reviews/t-2050-critic-plan-t2045.md` (B1-B11, S1-S13, per-node amendments); §10 says where each landed. A continuation of the same spec, one designer pass.

Marked **by recommendation, until the owner's word** (the coordinator's decisions, not the owner's): F1=D, F8=A, Python check vocabulary as rows of `assertion_probes_ast.python`. Other forks: the critic's reading stands where it differs from the first draft (§2 lists each). New forks found in this pass: F12, F13; nodes are written on their recommendation.

Tree: `D:/ws1/wt-fbfix` (branch `experiment/thinking-roles`); `PKG` = `D:/ws1/wt-fbfix\ai-packages\qa-factory`. Line numbers were read on that tree on 06.11.2026; a builder finds the function by name, the line is a pointer.

## §0 Intent (the owner's words, 06.11.2026)

«во первых исходный вариант проверки упало ли там где нам надо это наш же текст ошибки. Если он не прошёл, но проверяем на какой строке упало. Для питона тоже
должен быть способ это проверить, но ждаже если код этого не может, то потом решение передаётся роли (критик) и он сам может посмотреть на какой строке упало.
И только если всё это почему-то не сработало, то мы спрашиваем человека принять ли тест без мутационной пробы. Это должен быть ооооочень редкий случай»;
«надо что бы всё было единообразно. Нигде не должно быть таких исключений для каких-то языков, проектов или случаев. Это пораждает баги фабрики»; on a Then
checked by the second assert while the probe breaks the first: «обсалютно не верное поведение»; on a check in a helper: «А в чём проблема? Так же инвертируем
проверку и всё».

The road, one for every language, in this order:

| Step | What | Who | Record |
|---|---|---|---|
| 1 | Invert the check of the Then, wherever it stands (test or helper) | code | `target` says which line and why |
| 2 | The factory's marker in the failure text proves it | code | `intended_failure`, `proved_by: marker` |
| 3 | Marker not read. **The plan wrote a marker and the text does not hold it**: the line proves nothing; it goes to the critic with the line as a fact (F1=D, by recommendation, until the owner's word). **The form takes no marker**: the row's text or the line is read, the line under the matcher-span rule | code | `proved_by: fires_as`, `proved_by: line`, a settled `wrong_location` / `no_failure`, or step 4 |
| 4 | Code cannot settle it: the code critic judges, looking at the line itself | role | `cause: judgment`, then `--judge` |
| 5 | Only after that: the person is asked whether to accept the test without a probe | person | `probe not proved: <case>` |

Top invariant: **no branch of the road asks what language the test is in.** The only per-language things are the reader of the source and the data rows.

## §1 Package-change frame (AR-n, FR, census)

### AR-n touched, each with the change check written into the DoD of the node that owns it

| AR | How it is touched | Change check (DoD) | Node |
|---|---|---|---|
| AR-1 | Python's marker form, its check forms (`assert`, `assert_that`, `self.assert*`, Playwright `expect`) and its frame order become data; `helper_declaration` and the import form grow rows; `ASSERT_THAT` leaves the code | grep `scripts/` for the shape (`"probe-"`, `qa-probe`, `AssertionError`, `assert_that`), not the helper; a new value is a row | N2, N2b, N5 |
| AR-2 | Which check is the Then's stays with the role: code offers facts on a line with no check | name what the role still decides (report line); one fixture shaped unlike the default (a page-object method helper) must report, not halt | N1, N5 |
| AR-7 | The tool inverts where it is pointed; never chooses "the nearest" by itself (F9) | as AR-2 | N1 |
| AR-9 | `--at` refusal replaced, new refusals with doors; the door `--at <n>` must be openable, in BOTH its halves: the line (today dead on 7 of 41 ids, t-2037) and the repeat check (`already_probed`, B10) | each new refusal in one commit with its A24 row (`refusal_registry.py --check`) and a test that opens its door by RUNNING the second call, not by `check_on_line` alone; `controller-blocks.md` regenerated if a block changes | N1, N1b, N2b, N6, N7 |
| AR-10 | The critic's and the automator's text says what the probe will read, before the work | `s5.md`, charter, brief card changed in the same batch; ratchet measured | N6 |
| AR-13 | One reader stays one: `AD` for the table, `proof_level.receipt_off_target`, `proof_level.probe_record_state`, `reporters.assertion_site`, `red_sandbox.matching_rows`, `launch_check.runner_identity` | grep for a second parser of `assertion_id` (`_ASSERTION_ID` is the one), a second row matcher, a second "which runner"; new readers join them | N1, N3a, N3b |
| AR-14 | `judge_record` stays the one writer of `judgment` | no second writer; grep `"judgment"` writes | N4 |
| AR-15 | **The core of the node**: one row judge, one plan contract, one target reader | list every site by grep for the problem (`detector`, `.py`, `first_assert`, "not Python", `spec.get("language")`); §3 is that list; the static test of N3b keeps it | N1-N3b, N5, N7 |
| AR-19 | Twin: `red_sandbox.py --probe` reads the same `assertion_site` and `matching_rows`; `probe_debt.py` replays this probe | name both in the report; `red_sandbox` not changed; `probe_debt` follows N1 (`at`), N5 (reader), N7 | N1, N3a, N5, N7 |
| AR-20 | Census rows and `gate-registry` counts change; `safety` is AT its ceiling 50 and `meaning-proxy` AT its ceiling 8 (count over `scripts/tests/fixtures/judgment-census.json`: 50 lines `"class": "safety"`, 58 with `meaning-proxy`; ratchet line 4) | each raise named in the critic's verdict; a stale row is removed, not left | every node with a census line |
| AR-22 | `proved_by`, `target.source`, `target.calls_in_test`, `reader`, `matcher_span`, `target_outside_body`, `frames_deepest`, `rows` gain producers and readers both ways; `observed.test_file_frame`, `mismatches` values lose or change a producer on Python | grep each name over `scripts/ agents/ skills/ references/ handoffs/` case-insensitively with a positive control; run `test_field_producers.py` | N1-N3b, N4-N7 |
| AR-23 | `judgment_facts` with no failure text; `message_marker` empty; `target` absent; `matcher_span` null; `frames_deepest` absent; `fires_as` null | each empty named in the edges, pinned by a test | N2, N3b, N4 |
| AR-24 | Step 5 goes through the existing word `probe not proved:`; no new word | follow the answer to its consumer (`not_proved_word`); no new recording command | N4 |
| AR-25 | `incomplete` + `cause: judgment` is reachable from more inputs; its exit stays `--judge`, then the word | `design/state-exits.md` rows (lines 72, 92 name this tool) re-read; `test_state_exits.py` | N4 |
| AR-28 | A place that does not separate a throw from a check is an unknown, and goes to the critic, never a pass | spec states missing, unreadable and empty input per read (§4), a test pins each | N3b, N4 |
| AR-29 | Code joins data (a token, a line, a column, a span); whether a text proves firing stays the critic's. **`proved_by: line` is code concluding "fired" from a position: that is the owner's explicit grant (step 3), reachable only on a marker-less form, with the critic's note attached, its error direction held by the matcher-span rule** (F13 for the label) | census class per check below; `judgment:` line on each package commit | all |

`architecture:` line on every package commit, for example `architecture: AR-1, AR-13, AR-15, AR-28, AR-29 -- one row judge for every language`.

### FR sections the builder's pass walks

A (refusals: FR-1, FR-2, FR-4, FR-46, FR-57), C (FR-13, FR-38), D (FR-18, FR-58, FR-59), E and F (FR-41), G (FR-30, FR-33, FR-47, FR-54). B: `probe not proved` text unchanged; a line if any printed text changes.

### Census: every check this spec adds or alters

Row vocabulary: `scripts/tests/fixtures/judgment-census.json` (classes shape, xref, word-list, meaning-proxy, meaning, safety; owner data, judgment, intent).

| Check | Change | Serves (owner) | Class | Note |
|---|---|---|---|---|
| `judge_detector` :1881, renamed `judge_probe_row` (still `^judge`, u1); census :600 | altered: every language; marker, then marker-less text and line | data | xref | old row removed, new row added, count equal. `proved_by: line` label: F13 |
| `verdict_of` :1794 | removed | - | - | no census row; `gate-registry.json` :574 site removed (N3b) |
| `_target_of` (new) | joins `--at`, `assertion_id` and the file | data | xref | row only if the census test makes it a unit |
| `check_on_line` (new), refusal at a line with no check | new | data | shape | fact plus a door; which check is the Then's is the role's |
| `_same_target` (new, `proof_level`), `already_probed` | the repeat compares bytes AND target (N1b) | data | xref | errs toward running |
| `_form_of` (new; Python's forms as rows) | replaces `_is_assert_that` | data | shape | a row match, no judgment; a form unknown is a refusal, never a verdict |
| `_refuse_flags` :2905 | shrinks (`--at` branch gone; `expected` gone) | data | shape | row stays |
| `_resolve_oracle` / `_detector_oracle`: helper outside the test tree | E10 now for every language | data | safety | protects the product. `safety` is at 50: a new unit is a raise named (AR-20); the survivor keeps the existing row if one exists, the builder reads it first |
| helper called other than once overrides the marker (F11, N5b) | new | data | xref | a count and a frame; the meaning goes to the critic |
| `judge_record` :4299 | accepts more records as owed; no new content check | judgment | xref | unchanged class; **the critic's judgment is still never judged** |
| `_judge_input` :4234 | quote presence over every unsettled row | data | shape | no new refusal: an empty quote is already refused, :4240 (S12) |
| charter text in `agents/qa-code-critic.md` | experience, not a form | judgment | - | `role-load.json` `process_ratchet_tokens` measured, N6 |

No check here reads a role's wording; no phrase list is added. `fires_as` rows remain the library's own message shapes (existing data).

## §2 Forks

Status legend: **by recommendation** = a decision of the coordinator or a recommendation the critic found sound, each until the owner's word; nodes rest on it.

**F1 = D (by recommendation, until the owner's word; the owner's literal step 3 is narrowed by it, so the owner is told).** Which rule stands for the place of failure. A language-free rule: **where the plan WROTE a marker and the text does not hold it, steps of text and line prove nothing: `cause: judgment`, the line as a fact. They prove only when `message_marker` is empty, and then the line only under the matcher-span rule (B4).**
- Why: on every form with a marker, a failure at the statement with no marker is almost by definition not our check (B5). It dissolves the pytest type separator, which proved a foreign `AssertionError`.
- Consequence to tell the owner: for a form that takes a message, "the line" no longer proves in code; the critic reads it, as «он сам может посмотреть на какой строке упало» says. Code's line proof stays for marker-less forms only. A real one exists on the stand: `tr-probe/tests/api/users/get-user.spec.ts:1` imports `expect` from a fixture file, so `M-TS2`'s `source` does not hold and `expect(x).toBe(y)` gets no marker. Java and C# frames have no column: the rule is the same, there is no data, they go to the critic.
- It also narrows t-1968's "still the table" (`test_probe_marker.py:409-412`, E1.9 for a detail WITH a marker): flipped in N3b. A detail with no marker keeps the fast path (`:401-408`).
- Corrects the Lead's F1=C of t-1968 05.11: the rule «the place alone is not a proof» now has its one named exception, the marker-less form under the span rule.
- Reuse in a more consequential role (a location from a fact to a proof): error direction toward `cause: judgment`, never `intended_failure`. Adversarial inputs that must stay safe, each pinned in N3b: a throw in `expect`'s first argument, one line and multi-line; a timed-out action in the arguments; a throw in the MATCHER's argument (`toHaveText(new RegExp(...))`, `cart_page.spec.ts:126`; `toHaveValue(String(q))`, `:40`); a rejected `.resolves`; a timeout inside a `toPass` callback; a same-numbered line in another file; a code frame echoing the statement; a column shifted by a transpiler or by a runner not measured; a helper called in the arguments raising `AssertionError`.

**F2 = B (critic: sound).** The AST stays as Python's reader of the source; everything after the reader is one road; what is data goes to `assertion_probes_ast.python` read by `AD.ast_entry`. A full row would need a new body grammar and flip `test_source.py:90`, `manifest_from_tests.py:349,380`, `red_sandbox.py:1156`, `s5_precheck.py:759`, `validate_artifacts.py:2171`. If not B: N2 and N2b are rewritten. Map row `docs/SIBLING_MAP.md:148` changes in the same batch (§5.6).

**Python check vocabulary = rows (by recommendation, until the owner's word; «Для питона тоже должен быть способ»).** The forms of `assertion_probes_ast.python` hold `assert`, `assert_that`, `self.assert*`, Playwright for Python `expect(...).to_*`; node N2b. A new form is a row: E-F's door now opens.

**F3 = A (critic: sound, with B7).** Every run with a failed or errored row that code did not settle goes to the critic with its text: `site_unread`, `error`, reason mismatch. Records with no failure text stay `cause: tooling`: the critic reports `unverified`, the seam offers the word after his window, the standing word «по всем это ок» keeps working. Reverses E2.2's «a `status: error` row stays tooling» (pin `test_probe_marker_judgment.py:133`, flipped by N4, not N3).

**F4 = A (critic: sound, with S10).** One hop for every language with no line to go on: called names, same file, then imported files inside the test tree. Deeper: refusal with the door `--at <file>:<line>`.

**F5 (critic: right, with four corrections, §5).** Split TR2-1: item (2) moves to N1, item (3) to N6, TR2-2's first bullet to N1b. TR2-1 depends on TR2-14 N1.

**F6 = A (critic: holds).** Off-target with no way left is not on step 5's door for now; `OFF_TARGET_DOOR` says the true road. N1b makes it cheaper: a retarget now runs.

**F7 = A (no fork-level objection).** `--mutation expected` is removed: one mutation, `invert`, for every language; old records read; `probe_debt` replays them as `invert`. Node N7, moved BEFORE N2 so the plan contract and the forms are written once.

**F8 = A (by recommendation, until the owner's word; THE OWNER'S QUESTION STAYS OPEN).** `--mutation alternative` (reading B) is not in this graph; it gets its own node (id issued by the Lead in batch-2; finding written by the Lead) and the owner is asked, not notified: "the alternative probe runs only on Python; a model reader per language, or the exclusion by your word?" (TR2-15: excluding a language from a shared mechanism needs the owner's word). Until that node: `observe`, `_judge_alternative_row`, `_judge_param_rows`, `load_model`, `_alt_row`, `_alternative_gap_record` stay for it alone and are named in the static guard's table.

**F9 = A (critic: right; B would breach AR-2/AR-29).** A target line with no check: refusal before the run, with facts; the tool never picks.

**F10 = A (critic: holds, with the Python half in TR2-1, §5.5).** No id or a non-line id: first check, `target.source: first`, a note.

**F11 = A, reworded by B8 (critic).** The marker stands on a target outside the test's body only when the helper is called exactly once in the body AND the failure's caller frame lies inside the body span; otherwise step 4 with both facts. Node N5b, after N5.

**F12 (NEW, returned; recommendation A).** A check in a Python fixture. Reasoned from `verdict_of` :1801-1817 and pytest's setup-failure row, not run (N0 p7 measures): today a fixture's inverted assert gives a row `error` with the marker in its message and `verdict_of` says `intended_failure`. On the road step 1 reads `failed` only (`judge_detector` :1921), and E-D says an `error` row "is not decided" by marker.
- A. (**recommended**) Keep step 1 on `failed`. The `error` row goes to the critic with its text (F3=A), where the marker is plainly in the quote. Honest: a fixture has no call in the body, so F11's rule would send it to the critic anyway. Cost: one judgment on each fixture oracle (13797's class), where today it is free.
- B. Step 1 also reads `error`, and F11 treats a fixture parameter as the one call with no frame required. Cheaper; one more rule, and a session-scoped fixture's failure then proves for the test that happened to trigger it.
- If B: N3b step 1 and N5b change.

**F13 (NEW, returned; the critic left it to the Lead; recommendation A).** The census label of `proved_by: line`.
- A. (**recommended**) `judge_probe_row` stays `xref`: frame coordinates joined with a span the plan computed, the owner's explicit grant, reachable only with no marker. No raise.
- B. `meaning-proxy`: a position stands in for the meaning. The ceiling 8 is reached (measured, §1), so the raise is named (AR-20).
- If B: N3b's census line changes, nothing else.

## §3 Every Python-only branch on the probe road, with its fate

Read by Grep over `probe_by_code.py` for `detector`, `.py`, `python` (case-insensitive; the same calls find the known line :2916), then by reading each function. `D` = `plan_detector_mutation` path. Revised: rows 1, 6, 8, 12-14, 19, 21, 23, new 25.

| # | Function :line | Today | Fate | Node |
|---|---|---|---|---|
| 1 | `parse_node` :234 | a `.py` file gets a spec with no `language`, others `parse_detector_node` | stays as the reader's dispatch; writes **`reader: "ast" \| "table"`** (N2). `language` and `entry` arrive on Python ONLY in N3b, with the one judge (B1) | N2, N3b |
| 2 | `first_assert` :291, used :372, :390, :556 | always the first; knows two forms | `_first_check`: reads the forms (N2b); for the no-target case only (F10) | N1, N2b |
| 3 | `find_oracle` :362 and `_called_names`, `_imported_modules`, `_helper_chain` | Python's auto-hop, with conftest chain and fixture parameters | the survivor of one hop; both kept on the AST reader (S10); may not reach outside the test tree | N5 |
| 4 | `_assert_replacement` :491, `_assert_that_replacement` :518 | a literal marker `probe-<iid> invert: ...` as the assert's message | keep the inversions; message becomes `AD.marker_expression` (joined at run time); driven by the form row | N2, N2b |
| 5 | `plan_mutation` :540 | no `at`, no `marker_token`; detail lacks the detector's keys | takes `at`, `marker_token`; same detail keys as `D`; no target becomes `ToolRefusal` (N4) | N1, N2, N4 |
| 6 | `observe` :1758 | pytest's traceback | stays ONLY for `_judge_alternative_row` :3653 (F8); off the road | N3b |
| 7 | `_location_hits` :1786 | Python's place check | the survivor for every language; replaces :1953-1955, which compares a line number with no file | N3b |
| 8 | `verdict_of` :1794, `_judge_row` :2721 | location + reason + kind all or `wrong_location` | **both removed**: `_judge_row` is its only caller and is only `_judge_run`'s default; the alternative brings its own judge (read :2663, :3652-3653, :3897). `verdict_of` gets one line in N2 to stay green until then | N2, N3b |
| 9 | `report_rows(raw=)` :1719, :2689 | raw for detector only | raw on the road; non-raw only for the alternative's judge | N3b |
| 10 | `build_request` :1667-1684 | pytest node id, one selected instance; others the whole case | **keep**: the runner's selection, not the proof; reads `reader` (N2), named in the static test's table | N2, N3b |
| 11 | `put_back` :2012, :2017 | `.py` keeps mtime and loses bytecode | **keep**: an interpreter's bytecode rule, not a road; named in the table | none |
| 12 | `_judge_run` :2684, :2699-2711 | the fork of the two judges | reads `judge_row` is None: the road; given: the alternative's old branch | N2 (key), N3b |
| 13 | `_judge_param_rows` :2731 | Python's, default judge | alternative only, `judge_row` required (F8) | N3b |
| 14 | `_judge_detector_rows` :2773, comment :2847 | detector only | renamed `_judge_rows`, one binding keyed by the contract's shape (B2), site gate on `reporters.READERS` (B3), `pytest_command` from `is_pytest_command(argv)` at :2800, :2810, :2823 | N3a |
| 15 | `_refuse_flags` :2912 | `expected` is Python's | F7 | N7 |
| 16 | `_refuse_flags` :2916-2919 | **`--at` refused on Python** | **removed** | N1 |
| 17 | `_refuse_flags` :2908 | `--model` required on Python | stays (F8), reads `reader`, named in the table | N2 |
| 18 | `_resolve_oracle` :2941-2952 vs `_detector_oracle` :2862 | Python has **no test-tree guard** and silently falls back to the test when the named file is absent (:2945-2946); detector refuses both (E10) | one function; the detector's guard for all | N1 (guard), N5 (hop) |
| 19 | `ProbeCtx.detector` :2970, `_plan` :3016 | fork | `ctx.detector` keeps meaning "table reader" until N3b, for the F8 branches only; `_plan` calls `_reader_plan` (named in the table), same arguments, returns `(mutated, detail, context)`; `plan_mutation` keeps its 2 values, `_reader_plan` adds `""` (S3). `run_shape_checks` :3022 stays on the whole-case selection, condition: the request's selection is not by node id (#10), i.e. `reader == "table"` | N2 |
| 20 | `_off_target_note` :3048-3055 | **Python: only `unverified`** | one door for all; `detector` argument removed | N1 |
| 21 | `_probe` :3226-3227, :3268-3269 | `detector` from `language`; `detail["file"]` only on Python | `reader`; `detail["file"]` always | N1, N2 |
| 22 | `_build_parser` :4506-4507 help; docstring :54-70, :106-112; `_run_and_judge` :3110 «of the first assert» | "a test that is not Python", "first head" | one text | N6 |
| 23 | `load_model` :3374, `_alternative_gap_record` :3761, `_probe_alternative` :3832, `_alt_row` :3974 | alternative | F8; read `reader` (N2) so a Python alternative still runs (B1); own node | N2 (key only) |
| 24 | `plan_detector_mutation` :1334 + `locate_target` :976-1025 | the other side's "first head, never skips" | `--at` becomes whole-file (N1); E7 kept; `matcher_span` (N2) | N1, N2 |
| 25 | `_tool_refusal_record` :4366, :4395, :4401 | no language for `.py`; `spec["tail"]` read on Python | reads `AD.ast_entry` too (S4); no `tail`: no record | N4 |

Outside the file, same class:

| File :line | Text or branch | Fate | Node |
|---|---|---|---|
| `probe_debt.py:202-204` `_oracle_gone` (t-2046 M3, S9) | `.endswith(".py")`: «a helper of another language is named again with --oracle» | the reader's `declared_once(data, suffix, function)` for every language | N5 |
| `probe_debt.py:232-233` `_replay_plan` | `at` read only as an int | also `<file>:<line>` | N1 |
| `probe_debt.py:161,222` | text «a test that is not Python» | one text | N6 |
| `proof_level.py:1484` `reached` | «(a test that is not Python)» | removed | N6 |
| `proof_level.py:564` `code_sha` | Python's tokenizer | off the road (receipt identity); **not** changed; t-2046 M5, TR2-16 | none |
| `window_record.py:557` `OFF_TARGET_DOOR` | «a Python test has no `--at`» | removed | N6 |
| `brief_pack.py:224-227` | `--mutation invert\|expected`, «first assert», «invert only» | one text | N6 |
| `skills/qa-story/phases/s5.md:200` | «mutates the first assert», `invert\|expected` | the Then's check | N6 |
| `references/execution-lifecycle.md:60`, slice `:24` | «non-Python test» | one text, slice regenerated | N6 |
| `references/detectors.json:302` note | «How probe_by_code.py probes a test that is not Python» | names both keys | N2 |
| `agents/qa-code-critic.md:71-72` | one record kind; `--at` | N6 charter lines | N6 |
| `references/gate-registry.json:574-576` `probe_verdict` sites | `verdict_of`, `judge_detector`, `_judge_detector_rows` | renamed (N3a), `verdict_of` removed (N3b); pin `test_gate_registry.py:937-938`, `D13_ITEM_COUNT` :974 | N3a, N3b |
| `reporters.py` `assertion_site` :346-354 | `pytest_command` | keep: a runner's grammar; named in the table with its reason (S2) | none |
| `tests/test_probe_target_fact.py:81-82` | pins «Python: no `--at` door» | flipped | N1 |
| `tests/test_probe_marker_judgment.py:133` | pins «error row stays tooling» | flipped per F3 | N4 |

The census t-2046 M3 against this table: the one missing row (`probe_debt.py:202-204`) is added. Its other rows out of this road go to TR2-16.

## §4 Named edges (all nodes), each with its invariant

- **E-A target line with no check** (F9): `--at N` or an id on a line where no check of a KNOWN form starts or spans: refusal before a byte is written, naming nearest below and a called helper; the text says "no check of a form the factory reads", never "no check". INV: a probe never silently breaks a check other than the one named; a receipt of another line never counts; a real check of an unknown form is not blamed on the author (the critic reads the line and reports `unverified`, or a `mechanical` finding if the id is wrong). Reachable on a blank line, a comment (the skeleton hides it) and a line past the file's end.
- **E-B a check in a helper shared by other tests**: inverted in place, under the file's lock and byte copy. Only the selected node or case runs; other instances of the same case run on the mutated helper, and only this row is read. INV: bytes restored or the copy stays; the product tree is never touched (E10, now every language).
- **E-C a helper more than one hop away**: `assertion_id` or `--at <file>:<line>` reaches it, no walking. No line: refusal naming `--at <file>:<line>`. INV: code never guesses a chain; the door is usable by the critic.
- **E-D parameterised tests**: every row judged, on every language through `_judge_rows` (B2); `intended_failure` only if every row is (`_worst_of_rows`). New: `proved_by` of the WEAKEST row (line < fires_as < marker). A param that never reaches the check gives `no_failure`, which speaks. All rows unsettled: the critic sees each (B7). INV: a row is never picked silently; a record never claims a stronger proof than its weakest row (today `first = judged[0]`, :2754); a critic's `fires` never covers a row whose text he was not shown.
- **E-E a language with no entry**: `ToolRefusal`, `refused: tool`, data gap named, door `red_sandbox.py --probe` (as `_no_entry` :817, kept). Critic reports `unverified`; the seam then offers the word. INV: a grammar is never guessed; the author is not blamed.
- **E-F a check that cannot be inverted** (`invert: null`, an `_inverted` guard), **or a body with no check of a known form** on any reader: refusal, never a skip to another check (E7). It becomes a `ToolRefusal` with a record (N4; today a plain `Refusal`, no record, :1335 and :557), so it reaches the seam. The door names the data row (`assertion_probes.<lang>` / `assertion_probes_ast.python.forms`, the factory's to add) and `red_sandbox`; `--at` another line only "if that line is also this Then's check". INV: what is mutated is what the record says; a factory gap is never a verdict on the test.
- **E-G a throw inside the check's arguments** (first, or the matcher's; a rejection; a callback): the marker cannot be there. With a marker written: the critic (F1=D). Marker-less: no span hit, or a form with no span: the critic. INV: it never becomes `intended_failure` by code (E2.1).
- **E-H `--at` and `assertion_id` disagree**: `--at` wins what is mutated; `is_assertion_id: false`; the receipt does not count until the id is right. INV as E-A.
- **E-I `--oracle` and a target**: `--oracle` is explicit and wins the file; with no `--at`, the first check of that function, `target.source: oracle`. INV: compare with the id stays data.
- **E-J id names a file that is absent, outside the test tree or climbing out**: refusal, never a fallback to the test. INV: the #18 hole stays closed.
- **E-K two checks start on one line**: the first, with a note; `is_assertion_id: true` (named residual).
- **E-L S6 close, no critic**: as E2.11: digest line and delivery reason; no question. INV: an unknown is never reported as proved; S6 never stops for it.
- **E-M temporal, inside one run**: a record of the old shape (no `proved_by`, `style: assert`, no `target.source`, no `rows`) reads as today; a stored `intended_failure` off-target does not stand (`keep_standing_record`, unchanged). Same bytes and a new target RUNS from N1b on. INV: a receipt measured on other bytes never counts; the repeat refusal still holds for the same target.
- **E-N pair conflicts inside this spec**: "marker first" vs "helper not called exactly once" (F11, N5b); "never skip" vs "find the Then's check" (never skip wins); "person very rare" vs "S6 no critic" (not proved in the report, not a question); "the id is the default" vs "a stale id proves another Then's check" (S8: nothing in code can see it, the critic compares, N6).
- **E-O a target outside the located test's body** (B6): a stale id on test Y's check, a helper the test never calls, a line in a page-object method. The plan writes `target_outside_body`; the target given by `--at` or the id, and (several candidates or outside the body), and the row passes: `incomplete`, no text, `cause: tooling`, never `no_failure`. Body not located: `target_outside_body: null`, read as outside. INV: a pass says nothing about which body ran; the author is not accused of a dead check on a body the run may not have touched.
- **E-P a row beside a skip** (raw reader): `status` of a raw row lets a `<skipped>` child outrank a failure (`report_rows` docstring :1728-1731). The road reads `_row_status`: `failed` / `error` when such a problem exists, else the row's. INV: the Python road loses nothing the non-raw reader saw; a failed row is never read as not executed.
- **E-Q stored text limits**: `FAILURE_TEXT_MAX` per row, head AND tail kept (pytest's raising line is the LAST); at most `FACTS_ROWS_MAX` (12) rows in `rows`, with `rows_cut: <n>`. A `fires` on a record with `rows_cut > 0` is refused, door `cannot_judge`. INV: a quote is checked against stored text only; `fires` never covers a row not shown.

## §5 TR2-1 overlap: how the reader order resolves

Fact: the batch row makes TR2-14 depend on TR2-1; TR2-1's item (2) (`20261106-proby-cel-proby-i-ostatki.md:20`) says "without `--at`, take `assertion_id`" at about :3273, and t-2037 §c confirms nothing reads it today. Python has no `at`, so item (2) done first writes one more language exception and TR2-14 rewrites the same lines.

1. The reader order is one function, `_target_of`, here (N1): `--at` > `--oracle` > `assertion_id` > first check. **Item (2) of TR2-1 moves to N1.**
2. **Item (3) of TR2-1 (charter and command card) moves to N6**, so `agents/qa-code-critic.md` is written once.
3. **TR2-2's first bullet (repeat by bytes AND target; a new record does not overwrite a proved one) moves to N1b** (B10): under N1 the first shot goes at the id, and `no_failure` on a toast that vanishes, then a retarget, is the normal way into the dead door. The rest of TR2-2 follows TR2-14.
4. TR2-1 keeps item (1): the id stands on the check, the write check, the `add_to_cart.spec.ts` fixture. Its check calls `probe_by_code.check_on_line`, which N1 ships, so no second reader (t-2037 §d). An id naming a helper's line reads that file. Where the check stands stays TR2-1's question.
5. **TR2-1 also carries the Python half of the id** (F10; the name-like id `add_returns_sum`, pin `test_probe_by_code.py:429`): the form prints `<file>:<line>` for Python from `_assert_span`; a name-like id in a new row is refused with that door.
6. Order: **N1 → TR2-1 remainder, landing BEFORE any live run** (between them 7 of 41 ids become refusals and a rework round each), independent of N2 on. Lead edits, not a builder's: batch-2 rows, TR2-14 no longer depends on TR2-1; TR2-1 depends on TR2-14 N1; TR2-2's «Зависит от» gains TR2-14 (it wants `proved_by` from Python, and its split of `judge_detector` is done by N3b's helpers); TR2-14's «Пишет в» lists every path of §6 (today two; about twenty, or `piles.py check` (б) sees nothing). `docs/SIBLING_MAP.md:148` gains `assertion_probes_ast` and `AD.ast_entry` in the same batch (rule 9); no node owns the map. The batch is `ожидает`, so not frozen.

## §6 Nodes

### Shared

`given:` `D:/ws1/wt-fbfix\ai-packages\qa-factory\design\factory-rules.md` (whole), `D:/ws1/wt-fbfix\plans\builder-rules.md`, this spec, `D:/ws1/wt-fbfix\docs\tasks\specs\t-1968-mutation-probe-marker-and-critic.md` §3, `D:/ws1/yml-text-factory\docs\tasks\specs\reports\t-2037-tr2-1-assertion-id-recon.md`, `D:/ws1/yml-text-factory\docs\tasks\specs\reviews\t-2050-critic-plan-t2045.md`.

`handoff:` the builder's report plus a commit on the worktree branch. Report lists one mutation per node with the test line that kills it (7b); a `changelog.d/t-2045-nX.md` per node.

Witness: the test FILE of each owned path, fast only. **A slow file (`scripts/slow_tests.json`: `test_probe_by_code`, `test_probe_by_code_languages`, `test_probe_by_code_alternative`, `test_probe_by_code_copy`, `test_probe_binding`, `test_probe_debt`, `test_probe_gap_word`, `test_gate_registry`, `test_window_record`, `test_brief_pack`) is EDITED by the node whose change flips its pins, NOT run locally, and named "CI".** Fast by the same read (control: `test_probe_by_code` hits): `test_probe_marker`, `test_probe_marker_judgment`, `test_probe_target_fact`, `test_probe_gap_door`, `test_probe_not_proved`, `test_assertion_detectors`, `test_judgment_census`, `test_charters_s5_s9`, `test_contract_slices`, `test_code_critic_probe_rule`, `test_state_exits`, `test_probe_plugin_param` (a plain script: `python -B`, not pytest; it has `main()`, no `test_` functions). The canon is CI on the batch branch.

Pin owners (each is edited in the node's commit; §10 has no pin without one):

| Node | File | Pins |
|---|---|---|
| N1 | `test_probe_by_code.py` (CI) | `non_python_test_refused` (:1060, the `--at` refusal :1098-1107) |
| N1 | `test_probe_target_fact.py` | :81-82 |
| N1 | `test_probe_debt.py` (CI) | the `at` case near :1325 gains `<file>:<line>` |
| N7 | `test_probe_by_code.py`, `test_probe_by_code_languages.py`, `test_probe_debt.py` (CI) | `expected_plain_assert` (:481), `plan_mutation_is_pinned` rows :744-752, the `expected` cases (F7's 29 lines, not recounted) |
| N2 | `test_probe_by_code.py` (CI) | stub `stub_seen_marker` :129 (`b"qa-probe"`), `invert_plain_assert` (:408; literal `statement_after` :424, :448), `plan_mutation_is_pinned` (detail keys, :761) |
| N3a | `test_probe_marker.py` | `judge` :92, `test_rows_record_proved_by` :449-465: the rename |
| N3a | `test_probe_marker_judgment.py` | :156-172: the rename |
| N3a | `test_probe_by_code_languages.py` (CI) | R8 table helper `judge` :814-815, :858, :871; `judge_rows` :1543-1555; `Rn1_8World.judge` :1815, `record_of` :1838: the rename |
| N3a | `test_gate_registry.py` (CI), `gate-registry.json` | :937 and the `probe_verdict` sites: the rename |
| N3b | `test_probe_marker.py` | `test_failed_row_without_marker_same_line_not_by_marker` :348-353 and `test_fires_as_still_fast_path` :409-412: a detail WITH a marker is now the critic's; the detail with `message_marker: ""` keeps `fires_as` |
| N3b | `test_probe_marker_judgment.py` | `test_unknown_text_is_judgment_not_a_phrase_match` control :119-121: the control's detail becomes marker-less |
| N3b | `test_probe_plugin_param.py` | `DETAIL` :30 gains `message_marker: MARKER` (the recorded fixture holds the old literal) and the road's keys; spec gains `reader`, `language`, `entry`; `_judge_run` calls :53, :70 pass `request` with a pytest `command.argv` and `keys` non-empty; K2's `matched_report_id` stays pinned |
| N3b | `test_probe_by_code.py` (CI) | the stub's report text carries the token read from `seen`; `invert_plain_assert`, `class_method` :500, `hamcrest_style` :521, `raises_first` :544 (a throw at the statement: the critic, S1), `oracle_in_a_helper` :900, `reporter_in_the_summary` :991, `through_real_run_suite` :812 |
| N3b | `test_gate_registry.py` (CI) | :938 removed; `D13_ITEM_COUNT` :974 with its comment line, measured |
| N4 | `test_probe_marker_judgment.py` | :132-133 (flip), `test_judgment_facts_shape_and_cut` :136-139 (`rows`, head and tail) |
| N4 | `test_probe_by_code_languages.py` (CI) | `tool_refusal_record` :1688, `refusals_before_the_write` :1137 (`invert: null` now leaves a record) |
| N4 | `test_probe_by_code.py` (CI) | `no_assert` :553 (no target: a record) |
| N5 | `test_probe_by_code_languages.py` (CI) | `oracle_in_a_helper` :1327, `data_gaps` :1386 (E6's refusal now hops first) |
| N5 | `test_probe_debt.py` (CI) | `_oracle_gone`'s non-Python case |

Order: **N0** (no dependency; feeds N3b's data row, parallel with N1) ; **N1** → **N1b** ∥ **N7** → **N2** → **N2b** → **N3a** → **N3b** → **N4** ∥ **N5** (disjoint by the named functions and helpers below; `test_probe_one_road.py` by appended test functions, the later node merges) → **N5b** → **N6**. TR2-1's remainder after N1. Critic: this pass was on the plan; one on the merged diff, carrying the census question and the DUPLICATION / CODE QUALITY layer. A node over about 3 hours was split: N1b, N2b, N3a/N3b, N5b are those splits (estimates, not measured). All splits go in one batch; no release between them, so an interim state on the branch (Python road before N3b, marker on a helper before N5b) reaches no project.

### N0 — measure the frames, no product (builder on a scratch folder)

`owns:`
`D:/ws1/mybooks-stand\tr-probe\_n0-t2045\` (new folder; no existing file of the copy is touched; removed at the end)
`D:/ws1/yml-text-factory\docs\tasks\specs\reports\t-2045-n0-frames.md` (new)

`given:` `D:/ws1/mybooks-stand\tr-probe\node_modules\@playwright\test` (1.56.0, read), `PKG\scripts\reporters.py` (`read_rows`, `assertion_site`, `failure_frames`), `PKG\references\detectors.json` (the `typescript` frame grammar), this section. Nothing else: no stand, no app, no `global-setup.ts`, no `core/config`.

Under F1=D the question is narrow: on a **marker-less** form, does a frame's (line, column) separate a check from a throw, and what do the Python rows of `assertion_probes_ast` read. Nothing here chooses F1, and a down stand chooses nothing: the scratch specs await nothing from the app.

`_n0-t2045/playwright.config.ts`: `defineConfig({ testDir: '.', retries: 0, timeout: 5000, reporter: [['junit', { outputFile: 'junit.xml' }]], projects: [{ name: 'c' }] })`, no imports but `@playwright/test`.

Forced shapes in `_n0-t2045/`, each its own `test()` with no `page` unless named, `thrower()` a local function:
- (a) `expect(thrower()).toBe(1);` (b) `expect(await rejectsLater()).toBe(1);` (a timed-out action stand-in) (c) `expect(1).not.toBe(1);` (d) `expect(1).toBe(thrower());` (e1) `await expect(Promise.reject(new Error('x'))).resolves.toBe(1);` (e2) `await expect(async () => { await rejectsLater(); }).toPass({ timeout: 200 });` (f) `await page.setContent('<div id=a>x</div>'); await expect(page.locator('#a')).toHaveText('y', { timeout: 200 });` (g) `expect(1)\n  .not\n  .toBe(1);` (h1) (c) in a spec importing `expect` from `./fx` (a local re-export: the shape of `tests/api/users/get-user.spec.ts:1`) (h2) `expect(1, 'why').not.toBe(1)` with the marker expression put in the message (i) `expect(await po.get()).toBe(1)` with `po` in `./po.ts` throwing, (j) a helper in `./h.ts` holding the check, to read the frame order.
- Python, `_n0-t2045/py/`: (p1) `assert not (1 == 1), '-'.join(['qa-probe', 'tok'])`; (p2) `assert not (helper())` where `helper` raises `AssertionError('stand said 503')`; (p3) a `ValueError` in the arguments; (p4) `assert_that(1, is_not(1), '-'.join(...))` if `hamcrest` imports; (p5) `self.assertNotEqual(1, 1, msg='-'.join(...))` in a `unittest.TestCase`; (p6) Playwright for Python `expect(x, message='-'.join(...)).not_to_be_visible()` if `playwright` imports, else one report line; (p7) an assert in a fixture; (p8) a parametrised test, rows `[a]`, `[b]`.

Run, from the session's own directory, never changing it:
`node D:/ws1/mybooks-stand\tr-probe\node_modules\@playwright\test\cli.js test --config D:/ws1/mybooks-stand\tr-probe\_n0-t2045\playwright.config.ts`
`python -m pytest D:/ws1/mybooks-stand\tr-probe\_n0-t2045\py -q --junitxml=D:/ws1/mybooks-stand\tr-probe\_n0-t2045\py\junit.xml`

A committed-in-the-report script (full source pasted) reads both XMLs through `reporters.read_rows`, then `assertion_site` (the TS grammar for Playwright; `pytest_command=True` for pytest) and `failure_frames`, and prints per shape: status, message head, the raw frame, location, kind, column, the statement, the close of `expect(...)` and the matcher's `(` counted by bracket balancing on the skeleton.

Report answers:
1. Per runner, the table: shape → frame (line, col) → inside the span `close of expect(...) .. matcher's (` or not.
2. **Decision rule (written before the run):** every thrown shape (a, b, d, e1, e2, i) off the span AND every inverted shape (c, f, g, h1) on it → that runner's `form_id` goes in `assertion_probes.typescript.line_proof_runners` (N3b). One miss or one shape not measured → no row for that runner: marker-less forms go to the critic there; the owner is told. The row is the only thing that depends on this measurement.
3. Whether `fires_as` T1/T2 matches e1's text (the critic's suspicion; N3b closes the class by data regardless).
4. Frame order: `frames_deepest` per runner from j and p2.
5. Python: the joined token in the JUnit message (p1, p4, p5, p6), the row status and message of p7 (F12), the last-line site of p2, p3, the row ids of p8.
Jest and Vitest: measured only if their packages are in the copy's `node_modules`; otherwise one line "not measured" and no row, which is the safe outcome (a Playwright reading never licenses them).

`non-goals:` any package change; any existing file of the copy; a run against the app.
`edges:` no browser for (f): the shape is "not measured", rule 2 applies. A runner that will not start (no node, no module): a report line, `line_proof_runners` stays empty, the batch does not wait, the owner is told; F1 is not affected. Limit: `timeout: 5000`, the whole run under 2 minutes. INV: a guess never becomes a row; the copy's tree is as it was (witness: listing of `tr-probe` top level before and after, verbatim, plus the folder's removal).
`DoD:` `Read` of `D:/ws1/yml-text-factory\docs\tasks\specs\reports\t-2045-n0-frames.md`: the five answers, verbatim frames, both run outputs, the script source, the before/after listing.

### N1 — the target: one reader order, `--at` on every language, whole-file line lookup (F5, F9, F10)

`owns:`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\probe_by_code.py` (`_target_of` [new], `check_on_line` [new], `test_body_span` [new], `locate_target` — the `at` filter only, `plan_detector_mutation` — takes the target, empty keys, `target_source`, `target_outside_body`, `plan_mutation` — `at` only, `_refuse_flags` — the `--at` branch, `_resolve_oracle`, `_detector_oracle`, `_off_target_note`, `_probe` — the target call and the second lock, `target_fact`, `_build_parser` — `--at` type)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\probe_debt.py` (`_replay_plan` — the `at` read only)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_target_fact.py`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_one_road.py` (new, fast)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_by_code.py` (`non_python_test_refused`; CI)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_debt.py` (the `at` case; CI)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json` (rows)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-2045-n1.md` (new)

Required behaviour:
1. `_target_of(ctx, at, oracle, test_bytes) -> {file, line | None, source, outside_body}`, `source` ∈ `at | oracle | assertion_id | first`. Order: `--at`; `--oracle`; `assertion_id` of the manifest row when it parses by `_ASSERTION_ID` (the one parser); else first. **Position**: before `_resolve_oracle`, after the test's lock; the target file's lock is claimed BEFORE its bytes are read. INV: R9 (the lock precedes the first read of each file) and "`--at` never loses to the id".
2. `--at` takes `<line>` or `<file>:<line>`; the second form is the same spelling as `assertion_id`, so a door can print the id's own text. `detail["at"]` keeps the given spelling verbatim (`int` or the string), so a replay aims at the same file; `probe_debt._replay_plan` accepts an int (not a bool) or a string `_ASSERTION_ID` matches, and passes it on. Source `assertion_id`: `at` is None and the replay re-aims through `_target_of`.
3. `check_on_line(data, name, reader_entry, line) -> {"found": {line, end_line, form} | None, "nearest_below": {...} | None, "calls_helper": name | None}`: pure, reads only arguments. A check counts when it starts on the line OR its statement spans it (the same rule as `target_fact`'s `line <= n <= end_line`, so the printed door always opens). AST reader by `ast` (`lineno..end_lineno` of `ast.Assert` and the `assert_that` call; N2b makes it the forms), table reader by `Source.skeleton` over the WHOLE file, so a check in a local helper or a page-object method needs no declaration match. `calls_helper`, one generic rule for every reader: the last identifier before `(` on the line's skeleton (`[A-Za-z_$][\w$]*\s*\(`; AST: the outermost call's name on that line), None when there is none. It is a fact for the reader, never a target (S13). `locate_target` keeps its name search for the no-target case (E7 kept). A declaration repeating twice keeps its `--at` door, unchanged (`among`, E5).
4. The file named by the target goes through the one guard: under a test root, not under protected paths (`_in_test_root`); absent is a refusal (#18). INV E10 for every language. **This reaches Python for the first time (S11, an estimate, not measured):** a helper outside `roots.test` that hopped until today is refused; door `--at` inside the tree or the row in `roots.test`. The live proof counts how many helpers of the Python sample it refuses, in its report.
5. A target line with no check (F9 A, E-A): `Refusal` before a byte is written and no record (an id is the automator's input, not a tool gap), doors `--at <nearest>` and, for the author, `manifest_put.py --fragment`. The critic takes the refusal's text into a `mechanical` finding, or `unverified` when he reads a real check the factory cannot read.
6. The plan writes `target_source` and `target_outside_body` into `detail` (E-O): `test_body_span(test_bytes, spec, reader_entry) -> (first, last) | None` (pure) is read in `_target_of`; `outside_body` is True when the file is another or the line lies outside the span, None when the body is not located, False otherwise. **Line target where `locate_target` is bypassed** (a page-object method, no declaration): `declaration_line: null`, `candidates: []`, `context: ""`; `:1353` and `:1356` must not read a missing declaration. `run_shape_checks` works on the TEST's row, with `context ""` (it reads no annotation of a helper).
7. `target_fact` adds `source`. `_off_target_note(target)` has one door. Data only: `is_assertion_id` is computed as today. **Known weight (S8):** with the default on the id `is_assertion_id` is true by construction, so this data check stops separating anything on a stale id; N6 tells the critic.
8. `among`'s fact for N3b: nothing in the verdict changes here; N3b reads `target_source` and `target_outside_body`.

`edges:` E-A, E-C, E-H, E-I, E-J, E-K, E-M, E-O; F10: id absent or not a line → `first`, note, `null`.
`non-goals:` the verdict table (N3b); the marker on Python (N2); new forms (N2b); one-hop code (N5); the repeat check (N1b); the write check (TR2-1).

tests (`test_probe_one_road.py`, parametrised `language` ∈ python, typescript, csharp, java; a red names the language and the branch, P16): `test_default_target_is_assertion_id`, `test_second_check_is_the_then` (the owner's case), `test_at_wins_over_id`, `test_at_on_python`, `test_at_file_line_reaches_helper`, `test_at_inside_multiline_statement`, `test_line_with_no_check_refused_names_nearest` (blank, comment, past the end), `test_no_id_takes_first_with_note`, `test_name_like_id_is_null`, `test_id_outside_test_tree_refused`, `test_python_oracle_absent_file_refused` (#18), `test_python_oracle_outside_tree_refused`, `test_outside_body_stale_id_and_page_object` (the empty keys; a method helper, AR-2), `test_body_not_located_is_null`, `test_calls_helper_generic_rule`, `test_debt_replays_file_line_at`. `test_probe_target_fact.py`: flip :81-82; `test_printed_line_door_holds_a_check` (the printed `--at` passes `check_on_line`; the second half of the door is N1b's).

`DoD:` `python -m pytest ai-packages/qa-factory/scripts/tests/test_probe_one_road.py ai-packages/qa-factory/scripts/tests/test_probe_target_fact.py ai-packages/qa-factory/scripts/tests/test_judgment_census.py -q` and `python -B ai-packages/qa-factory/scripts/selftest.py --lang`, from the worktree root, output pasted. CI: `test_probe_by_code.py`, `test_probe_by_code_languages.py`, `test_probe_debt.py`. AR-9: `refusal_registry.py --check` row per new refusal; AR-15: report lists the grep. `architecture: AR-2, AR-7, AR-9, AR-13, AR-15, AR-19, AR-22, AR-29`; `judgment: _target_of xref data; check_on_line shape data`.

### N1b — the door opens: a repeat compares bytes AND target (TR2-2's first bullet, B10)

`owns:`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\proof_level.py` (`already_probed` — keyword `target=None`, `_same_target` [new], `probe_record_path` — the beside form)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\probe_by_code.py` (`_repeat_check` — passes the target, `_finish_record`, `keep_standing_record`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_one_road.py`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_target_fact.py`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-2045-n1b.md` (new)

Required behaviour:
1. `_repeat_check` passes `_target_of`'s `{file, line, source}` to `proof_level.already_probed(..., target=...)`. `target=None` (any other caller) is today's behaviour, byte for byte.
2. `_same_target(source, target)`, `source` a record or receipt, read in items 1 and 2 of `already_probed` (and 3 stays as is: a product record has no line): **requested line None** (`first`): same when `source.target` is absent or its `source` is absent or `first`. **Requested line n**: same when `source.target` exists, its file (`mutation_detail.file`, or `mutated_file.path`) is the target's, and `line <= n <= end_line`. Anything else: different. Different: not blocked, a note says which line the earlier probe had. Error direction: toward running (the function's own docstring).
3. A new record does not overwrite a proved one: when the stored standing record is `intended_failure` with `target.is_assertion_id` true on the same bytes, and the new one has another target and is not itself that, the new record goes BESIDE: `probe_record_path(task_root, iid, target_line=<line>)` → `work/probes/<iid>--L<line>.json`; the answer to the caller is the new record, with a note naming the standing one. `already_probed` item 2 also reads the beside record of the requested line. No receipt is published from a beside record. `keep_standing_record`'s existing pins (`test_probe_target_fact.py:252-258`) hold.
4. Reads: `window_record._probe_from_receipt` :581 (TR2-2 names it): the builder reads it and reports whether a standing record stays what it reads; a change there returns as a question, it is not in `owns`.

`edges:` E-M. Same bytes, same target, `no_failure`: refused as today (the negative control). Old record with no `target`, requested a line: different, it runs. Earlier target overwritten by a later proved one, then asked again: it runs (error toward running, named). INV: a receipt of other bytes never counts; the person's word still passes a repeat; a retarget needs no word (the owner's «ооооочень редкий случай»).
`non-goals:` the rest of TR2-2 (the person's word by revision, `proved_by` mandatory, the door's third text).

tests: `test_same_bytes_other_target_runs`, `test_same_bytes_same_target_refused` (negative control), `test_first_after_first_refused`, `test_old_record_no_target_line_runs`, `test_new_record_never_overwrites_proved`, `test_beside_record_blocks_its_own_line`, `test_printed_door_runs_second_call` (FR-2, end to end on a stub: `no_failure` at L47, the printed `--at 46`, the second call is not `already_probed`; t-2031's trace).

`DoD:` `python -m pytest ai-packages/qa-factory/scripts/tests/test_probe_one_road.py ai-packages/qa-factory/scripts/tests/test_probe_target_fact.py -q`; `python -B ai-packages/qa-factory/scripts/selftest.py --lang`. CI: `test_probe_by_code.py` (`a_rerun_is_idempotent...`, the `already_probed` cases). `architecture: AR-9, AR-13, AR-22, AR-29`; `judgment: _same_target xref data`.

### N7 — `--mutation expected` removed (F7 A; before N2)

`owns:`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\probe_by_code.py` (`MUTATIONS`, `_refuse_flags` — the `expected` branch, `_assert_replacement`, `_assert_that_replacement`, `_literal_node`, `_replacement_literal`, `_build_parser` — the `--mutation` line)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\probe_debt.py` (`_replay_plan` — the mutation read :228)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_one_road.py`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_by_code.py`, `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_by_code_languages.py`, `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_debt.py`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-2045-n7.md` (new)

Required: `MUTATIONS = ("invert",)`. `--mutation` keeps `expected` among its `choices` (`:4489`) so argparse does not answer first (S6); `_refuse_flags` refuses it with one sentence and the door `--mutation invert`. A stored record with `mutation: expected` still reads; `probe_debt._replay_plan` maps a stored `expected` to `invert` before the `MUTATIONS` check (`LEGACY_MUTATIONS`), so it replays. INV: a live receipt of old bytes is still judged by its own record.
`edges:` a parked replay with any other unknown `mutation`: as today, refused at :228. The `:172` comment "only the two invert kinds" follows.
`non-goals:` alternatives; any new inversion.
tests (fast, `test_probe_one_road.py`): `test_expected_refused_with_door` (through the parser), `test_old_expected_record_reads`, `test_debt_replays_old_expected_as_invert`. The three slow files: old `expected` cases removed, judged by CI.
`DoD:` `python -m pytest ai-packages/qa-factory/scripts/tests/test_probe_one_road.py -q`, output pasted; CI for the three slow files. `architecture: AR-9, AR-15, AR-19, AR-22`; `judgment: _refuse_flags shape data`.

### N2 — one plan contract: the reader key, Python's marker and detail keys, as data (F2, B1)

`owns:`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\detectors.json` (`assertion_probes_ast` [new key], `frames_deepest` on the csharp, java and typescript entries, `assertion_probes_note`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\assertion_detectors.py` (`ast_entry` [new], `marker_expression` — takes that entry too, `frames_deepest` [new reader], `ENTRY_FIELDS` optional)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\probe_by_code.py` (`parse_node`, `parse_detector_node` — the `reader` key, `plan_mutation` — detail, `plan_detector_mutation` — `matcher_span`, `_assert_replacement`, `_assert_that_replacement`, `_plan`, `_reader_plan` [new], `ProbeCtx`, `verdict_of` — the one marker line, and the five sites by name: `build_request` :1667, `_judge_run` :2684, `_probe` :3226, `_alternative_gap_record` :3761, `_probe_alternative` :3832, `_refuse_flags` :2908)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_marker.py`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_assertion_detectors.py`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_one_road.py`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_by_code.py` (stub :129, `invert_plain_assert`, `plan_mutation_is_pinned`; CI)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-2045-n2.md` (new)

Required behaviour:
1. **The reader key (B1).** `parse_node` writes `reader: "ast"`, `parse_detector_node` `reader: "table"`. Each of the five sites above replaces `bool(spec.get("language"))` by `spec["reader"] == "table"`. **`language` and `entry` are NOT added to the Python spec here**: they arrive in N3b with the one judge. `ctx.detector` keeps meaning "table reader", for the F8 branches. INV: until N3b nothing about a Python run changes but the marker's spelling: a pytest run gets its node id, `_judge_run` keeps its branch, `_resolve_oracle` keeps the hop, **a Python alternative probe still runs**.
2. Data: `"assertion_probes_ast": {"python": {"suffixes": [".py"], "marker_expr": "'-'.join(['qa-probe', '{token}'])", "frames": [<the `_FRAME` grammar :192 with path and line>], "skip_frames": [], "frame_path": "path", "frames_deepest": "last", "compiled": false, "builds_by_default": [], "no_rebuild_flags": [], "line_proof_runners": []}}`, and `"frames_deepest": "first"` on csharp, java, typescript, corrected by N0's answer 4 for what it measured. No `fires_as` here: forms carry `fires_as: null` (N2b; E3.3 skips it). `AD.ast_entry(suffix)` is the one reader; unreadable is `DetectorsError` as for the table. `entry_for_suffix` does NOT read it. `AD.frames_deepest(entry)`: `"first" | "last"`, absent or other → None (AR-23), which means the frame fact is unknown. The note `:302` names both keys and says the AST key is Python's reader's, the shared contract the same.
3. `plan_mutation(..., at=None, marker_token="")` returns the same keys as `plan_detector_mutation` (:1347-1353) plus N1's: `line, end_line, mutation, style, language, head, form, pair, pair_id, at, candidates, statement_before, statement_after, statement_inverted, message_marker, message_form, message_note, fires_as, marker, matcher_at, matcher_span, declaration_line, file, target_source, target_outside_body`. `language: "python"` in the detail only. `style` keeps `assert` / `assert_that` (a test pin reads it, no reader in `scripts/*.py` beyond the writers; grep with a control in the report). `message_form` ∈ the form's row id. The marker travels as the assert's message, an expression joined at run time, so a traceback's echo of the source line never holds the contiguous token. `detail["marker"]` (the human text in `expected_reason`) stays.
4. `verdict_of`'s `reason_hit` reads `detail.get("message_marker") or detail["marker"]`, one line, so the Python road stays correct until N3b removes it (a joined marker would otherwise read as a mismatch).
5. **`matcher_span` (B4; computed, not guessed).** `plan_detector_mutation` computes on the WRITTEN statement (`mutated`, as a `Source`) at plan time: `{"line": L, "col_from": a, "col_to": b}`, 1-based, the coordinates of a stack frame: `L` is the line of the matcher's name; `b` the column of the matcher's `(`; `a` the column right after the close of the head's arguments when that close is on `L`, else 1. Only when the form has `matcher_at: "after_args"`. **Null** (with no error) on: the AST reader; `matcher_at` head or second_arg; a line and column it cannot compute; `no_proof_after` matches the text between the close and the matcher; `no_proof_args` matches the head's arguments. On `no_proof_*`, `fires_as` in the detail is null too.
6. Data on the `typescript` `expect` form: `"no_proof_after": "\\.(?:resolves|rejects)\\b"`, `"no_proof_args": "=>|\\bfunction\\b"`. Both optional keys in `ENTRY_FIELDS`, read through `AD`. INV: a rejection and a callback never reach text or line proof by code, whatever N0 says of them.
7. `_plan` is one call shape, through `_reader_plan`; the token is computed once there for every language (:3019), so direct callers with no token keep "no marker". `run_shape_checks` stays on `reader == "table"` (S3, §3 #19).
8. Unchanged: line count, BOM, "mutated must parse".

`edges:` `marker_token=""` → `message_marker: ""`, falls through (AR-23). A column under BOM: the `Source` has none, a frame counts none (N0's h2 confirms). Marker with `assert_that` whose third argument existed: replaced, as today. INV (E1.3 for Python): the failure of ANOTHER statement whose traceback echoes the mutated line never reads as this probe's marker. Adversarial: a fixture error after the mutated line printed; `-vv`; `--showlocals` printing the token's pieces (not contiguous).
`non-goals:` judging (N3b); new forms (N2b).

tests: `test_probe_one_road.py`: `test_python_spec_reader_ast_no_language` (`parse_node` has `reader`, not `language`), `test_python_alternative_still_runs_after_n2` (B1: `_probe_alternative` over a stubbed run takes the substitution branch, no `gap` record), `test_python_build_request_keeps_node_id`. `test_probe_marker.py`: `test_python_marker_joined_at_run_time`, `test_python_detail_same_keys_as_detector` (set equality with a TS plan), `test_python_marker_line_count_kept`, `test_matcher_span_single_line`, `test_matcher_span_multiline_chain`, `test_matcher_span_with_marker_written`, `test_matcher_span_null_on_resolves_and_callback`, `test_matcher_span_null_on_ast_reader`; `test_assertion_detectors.py`: `test_ast_entry_shape`, `test_suffix_not_in_entry_for_suffix` (negative control: `.py` still gives `(None, None)`), `test_frames_deepest_absent_is_none`.

`DoD:` `python -m pytest ai-packages/qa-factory/scripts/tests/test_probe_marker.py ai-packages/qa-factory/scripts/tests/test_assertion_detectors.py ai-packages/qa-factory/scripts/tests/test_probe_one_road.py -q`; `python -B ai-packages/qa-factory/scripts/selftest.py --lang`. CI: `test_probe_by_code.py`, `test_probe_by_code_alternative.py`. Grep check AR-1 pasted. `architecture: AR-1, AR-15, AR-22, AR-23, AR-29`; `judgment: none altered (data rows)`.

### N2b — Python's check vocabulary as rows (by recommendation, until the owner's word)

`owns:`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\detectors.json` (`assertion_probes_ast.python.forms`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\assertion_detectors.py` (`ast_entry` — validates `forms`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\probe_by_code.py` (`ASSERT_THAT` [removed], `_is_assert_that` → `_form_of`, `first_assert` → `_first_check`, `find_oracle` — the call of it, `check_on_line` — the AST half, `plan_mutation` — dispatch by form, `_assert_replacement`, `_assert_that_replacement` → `_call_replacement`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_one_road.py`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_assertion_detectors.py`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\fixtures\probe-languages\` (new Python samples)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-2045-n2b.md` (new)

Required behaviour. Row shape (a closed set of AST shapes in code; every name, rename and message slot in data, AR-1):

```json
"forms": [
 {"id": "PY-assert", "shape": "assert", "invert": {"kind": "wrap_test"}, "message": {"at": "assert_msg"}, "fires_as": null},
 {"id": "PY-assert_that", "shape": "call", "names": ["assert_that"], "min_args": 2,
  "invert": {"kind": "wrap_arg", "arg": 1, "wrap": "__import__(\"hamcrest\").is_not({arg})"}, "message": {"at": "arg", "arg": 2}, "fires_as": null},
 {"id": "PY-unittest", "shape": "method", "receivers": ["self"],
  "invert": {"kind": "rename", "names": {"assertEqual": {"to": "assertNotEqual", "args": 2}, "assertNotEqual": {"to": "assertEqual", "args": 2},
    "assertTrue": {"to": "assertFalse", "args": 1}, "assertFalse": {"to": "assertTrue", "args": 1},
    "assertIn": {"to": "assertNotIn", "args": 2}, "assertNotIn": {"to": "assertIn", "args": 2},
    "assertIs": {"to": "assertIsNot", "args": 2}, "assertIsNot": {"to": "assertIs", "args": 2},
    "assertIsNone": {"to": "assertIsNotNone", "args": 1}, "assertIsNotNone": {"to": "assertIsNone", "args": 1},
    "assertGreater": {"to": "assertLessEqual", "args": 2}, "assertLessEqual": {"to": "assertGreater", "args": 2},
    "assertLess": {"to": "assertGreaterEqual", "args": 2}, "assertGreaterEqual": {"to": "assertLess", "args": 2},
    "assertRegex": {"to": "assertNotRegex", "args": 2}, "assertNotRegex": {"to": "assertRegex", "args": 2},
    "assertIsInstance": {"to": "assertNotIsInstance", "args": 2}, "assertNotIsInstance": {"to": "assertIsInstance", "args": 2},
    "assertAlmostEqual": {"to": "assertNotAlmostEqual", "args": 2}, "assertNotAlmostEqual": {"to": "assertAlmostEqual", "args": 2}}},
  "message": {"at": "kw", "kw": "msg"}, "fires_as": null},
 {"id": "PY-unittest-none", "shape": "method", "receivers": ["self"],
  "names": ["assertRaises", "assertRaisesRegex", "assertWarns", "assertLogs", "assertCountEqual", "fail"], "invert": null},
 {"id": "PY-pw-expect", "shape": "chain", "names": ["expect"], "source": "from\\s+playwright\\.(?:sync|async)_api\\s+import",
  "invert": {"kind": "method_pattern", "pairs": [{"find": "^not_to_(.+)$", "replace": "to_\\1"}, {"find": "^to_(.+)$", "replace": "not_to_\\1"}]},
  "message": {"at": "head_kw", "kw": "message"}, "fires_as": null}
]
```

1. `_form_of(stmt, forms, file_text) -> (form, name) | None`: `shape` `assert` is `ast.Assert`; `call` a bare or attribute call whose name is in `names`, as a statement (`Expr`), with `min_args`; `method` a call `<receiver>.<name>(...)`; `chain` a call `<head>(...).<method>(...)`, also under `await`. `source`, when present, must match the file (as in the table's `source`). A statement no row matches is not a check. The first match in row order wins.
2. `_first_check(function_node, forms, file_text)` replaces `first_assert`, same walk (`_statements`, into compound statements, never into a nested def). **A form with `invert: null` is the first check and is refused, never skipped** (E7, one rule with the table). This is a change for Python: `self.assertRaises` before an `assert` was invisible until today.
3. Inversion by the row. `wrap_test`, `wrap_arg`: as today, the wrap text from data. `rename`: the method name replaced, every argument kept. `method_pattern`: first `find` that matches, `re.sub`-style. The message: `assert_msg` replaces the assert's message; `arg` the positional argument at that index, added if absent; `kw` a keyword: **an author's message is replaced** (keyword, or a positional beyond the row's `args`), as `assert` and `assert_that` do today; `head_kw` the keyword on the head call (`expect(x, message=...)`), an author's keyword or second positional replaced. Line count kept (`_padded`), "mutated must parse".
4. `message_form` is the row's id; `message_marker` is never empty on these rows. A row with no `message` key would be marker-less: the road takes it; `matcher_span` is null on this reader, so it goes to the critic (one rule, no data).
5. `check_on_line`'s AST half reads the forms: so an id on `self.assertEqual` opens, and TR2-1's write check accepts it.
6. **Verification before a row stands (t-1968 rule).** `PY-unittest`: `test_unittest_rows_exist` asserts every `to` and every name is an attribute of `unittest.TestCase`, and one run of a canned sample proves the marker lands in the JUnit message (N0 p5). `PY-assert_that`: N0 p4. `PY-pw-expect`: N0 p6. **If p6 could not run**, the row stays, and the report says so: an inversion to a method that does not exist or a `message` keyword an old version refuses throws at the statement with no marker, which is the critic's by F1=D; the error direction holds. The owner's sentence is met either way, and the live proof names it.

`edges:` E-F. `self.assertEqual` on a receiver not in `receivers` (`tc.assertEqual`): not a check, E-F's door (a row). `expect` from another library: `source` does not hold, not a check. A subTest block: walked, the first inside. An `assert_that` with one argument: not a check, as today. An `await` on a table of `chain`: kept in the mutated text. INV: what is mutated is what the record says; a form code does not know is never guessed or skipped over silently past a known one, unless no row matches it, which is named by the note `first` writes.
`non-goals:` readers off the road (`manifest_from_tests`, `s5_precheck`, `assert_spans` of the alternative, t-2046); pytest's `pytest.raises` as a check; the `_call_arguments` of Python.

tests (`test_probe_one_road.py`): `test_unittest_assert_equal_inverted_with_marker`, `test_unittest_author_msg_replaced`, `test_unittest_assert_raises_refused_not_skipped`, `test_unittest_rows_exist`, `test_pw_expect_to_inverted_with_marker`, `test_pw_expect_not_to_restored`, `test_pw_expect_await_kept`, `test_pw_expect_other_library_not_a_check`, `test_at_on_unittest_line_opens`, `test_unknown_form_refusal_names_the_row_and_red_sandbox` (FR-2), `test_assert_that_wrap_comes_from_data` (a planted row changes the output); `test_assertion_detectors.py`: `test_ast_forms_validated`, `test_ast_form_bad_regex_is_detectors_error`.

`DoD:` `python -m pytest ai-packages/qa-factory/scripts/tests/test_probe_one_road.py ai-packages/qa-factory/scripts/tests/test_assertion_detectors.py -q`; `python -B ai-packages/qa-factory/scripts/selftest.py --lang`. CI: `test_probe_by_code.py`, `test_probe_by_code_alternative.py`. Grep for `assert_that` under `scripts/*.py` pasted, every hit named. `architecture: AR-1, AR-2, AR-9, AR-15, AR-22, AR-29`; `judgment: _form_of shape data`.

### N3a — one binding and one site reader; the rename (B2, B3, B11)

`owns:`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\probe_by_code.py` (`judge_detector` → `judge_probe_row` [the name only], `_judge_detector_rows` → `_judge_rows`, `_row_status` [new])
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\gate-registry.json` (`probe_verdict` sites :575-576)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_marker.py`, `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_marker_judgment.py` (the rename)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_by_code_languages.py`, `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_gate_registry.py` (the rename; CI)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json` (rename row :600)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_one_road.py`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-2045-n3a.md` (new)

Required behaviour:
1. The rename goes in ONE commit with every caller and the registry (grep `judge_detector|_judge_detector_rows` over `PKG`, positive control the census row; the report pastes it).
2. **One binding, keyed by the contract's shape (B2).** In `_judge_rows`: a contract WITH a `file`: `selection_rows`, as today. A contract with NO `file` (a pytest contract, `execution_request.py:3544-3550`), or no contract: `red_sandbox.matching_rows(rows, spec["node"])`, the one matcher (HF4-12); all rows that match are judged (`_worst_of_rows`). No match: as the no-binding branch today (`_tooling_gap` when rows were held, the note with `held_ids`). `keys` empty is tolerated (`key = ...` no `keys[0]` on an empty list). A table language today always has `file` (read at :3544), so this flips nothing on it; `bind_row` stays only at :2800. `matched_report_id` stays written when one row matched by another tail (pin K2; no reader in `scripts/*.py`, kept: small choice, §7).
3. `pytest_command = execution_request.is_pytest_command(argv)`, computed once, at :2800 and :2823 (S-note B2: all three `False`s go).
4. **The site gate (B3).** `reporter in reporters.READERS`, not `("trx", "junit-xml")`, so `reporter: "pytest"` (the default of a pytest profile, `execution_request.py:1817`) is read. Else the existing `site_unread`.
5. `_row_status(row)`: E-P. Used by `judge_probe_row` for `status`.

Reuse in a more consequential role: `matching_rows` moves from one Python branch to the one binding. Error direction: more rows judged, never a row picked; `func[webkit]` never matches `func[firefox]` (its K9 pins stand). Adversarial pinned: `[chromium]` plugin row, two `[a]`, `[b]`, exact id beside param rows, a contract with no file on a table reporter.

`edges:` E-D, E-P. `argv` absent: `is_pytest_command(None)` must be false, not raise; read it, a test pins it. INV: a row is never picked silently; a report with no row of this node says what it held.
`non-goals:` the table's steps (N3b); putting Python on this road (N3b; these functions are tested directly here).

tests (`test_probe_one_road.py`, through `_judge_rows`, not the row judge): `test_no_file_contract_binds_param_rows` (`tests.t::test_x[chromium]`), `test_no_file_contract_two_rows_all_judged`, `test_no_match_is_tooling_gap_with_held_ids`, `test_reporter_pytest_reaches_site_reader`, `test_reporter_unknown_site_unread`, `test_pytest_command_from_argv`, `test_empty_keys_tolerated`, `test_failure_beside_skip_is_failed`.

`DoD:` `python -m pytest ai-packages/qa-factory/scripts/tests/test_probe_one_road.py ai-packages/qa-factory/scripts/tests/test_probe_marker.py ai-packages/qa-factory/scripts/tests/test_probe_marker_judgment.py ai-packages/qa-factory/scripts/tests/test_judgment_census.py -q`; `python -B ai-packages/qa-factory/scripts/tests/test_probe_plugin_param.py`; `python -B ai-packages/qa-factory/scripts/selftest.py --lang`. CI: `test_probe_by_code_languages.py`, `test_gate_registry.py`. `architecture: AR-13, AR-15, AR-19, AR-22`; `judgment: judge_probe_row xref data (renamed from judge_detector, rows equal)`.

### N3b — one row judge: marker, then marker-less text and line, for every language (F1=D, F3)

`owns:`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\probe_by_code.py` (`parse_node` — `language`, `entry`, `tail` on the Python spec; `judge_probe_row` and new helpers `_row_by_marker`, `_row_passed`, `_row_by_place`, `_row_unsettled`; `_at_statement` [new]; `_line_proof_allowed` [new]; `_judge_rows` — `among`, `proved_by`; `_judge_run`; `verdict_of` [removed]; `_judge_row` [removed]; `_judge_param_rows` — `judge_row` required; `_location_hits`; `_worst_of_rows` — `proved_by` of the weakest; `report_rows` call)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\detectors.json` (`typescript.line_proof_runners`, from N0's report)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\gate-registry.json` (`probe_verdict` site :574)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_one_road.py`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_marker.py`, `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_marker_judgment.py`, `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_plugin_param.py` (pins of §6)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_by_code.py`, `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_by_code_languages.py`, `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_gate_registry.py` (pins of §6; CI)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\fixtures\probe-languages\` (canned rows)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json` (notes)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-2045-n3b.md` (new)

Required behaviour. `judge_probe_row` is a short sequence of named helpers, so TR2-2 has nothing left to split. **Position invariant: a `passed` row is never read as proved; a step runs only when no earlier step settled the row; a row settled as not proved is never re-read by a later step.**

0. Python joins the road: `parse_node` adds `language: "python"`, `entry: AD.ast_entry(".py")`, `tail`; `_judge_run`: `judge_row` is None → raw rows, `_judge_rows`; `judge_row` given (the alternative) → its branch, non-raw, unchanged. `_resolve_oracle`'s and `build_request`'s `reader` reads stand. B1's test stays green.
1. `_row_by_marker`: `failed` + the exact `message_marker` in the failure or error problem's message or text → `intended_failure`, `proved_by: marker`. (F11's guard is N5b's. An `error` row is not decided here: F12=A.)
2. `_row_passed`: `passed` → `among`, `compiled`, `no_failure`. **`among` (B6): `target_source` in (`at`, `assertion_id`) and (`len(candidates) > 1` or `target_outside_body` is not False)** → `incomplete`, no text, no cause set here, so the caller writes `cause: tooling`; never `no_failure`. The note says "a pass does not say which body ran" and names the target and the test. `--oracle` and `first` keep `no_failure` as today.
3. `error` → `incomplete`, no cause, as today (N4 flips it). Other unknown statuses → `not_executed`. `site_unread` or no location → `incomplete`, as today (N4 flips it).
4. `_at_statement(site, frames, detail)`: **first_read** = `_location_hits(site["location"], ...)` (file AND line); **substitute** = the deepest frame in the mutated file by `AD.frames_deepest` over `reporters.failure_frames`, when first_read is false (this keeps `observe`'s `test_file_frame`, a hamcrest assert). `frames_deepest` None: no substitute. Neither hits → `wrong_location`, settled, kind unchanged (S1: step of settled refusal is about being OUTSIDE the statement only).
5. **F1=D:** at the statement and `message_marker` non-empty → `_row_unsettled`: `incomplete`, `cause: judgment`, `judgment_facts`, the location among them. Whatever the type, whatever `fires_as` says. INV: on a form with a marker, a failure at the statement without it never becomes `intended_failure` by code.
6. Marker-less (`message_marker` empty), **first_read** true (the substitute never proves, B5), `failure_kind == "assertion"`: `fires_as` non-null and `fires_on` → `intended_failure`, `proved_by: fires_as`.
7. Same conditions, `_line_proof_allowed` and the frame on the span → `intended_failure`, `proved_by: line`, one note: "proved by the line of the failure on a form with no marker; read the statement when it matters". **The span rule: `_COLUMN` over `site["frame"]`, line == `matcher_span.line`, `col_from <= col <= col_to`.** `_line_proof_allowed(argv, entry)`: `launch_check.runner_identity(argv)["form_id"]` is in `entry.get("line_proof_runners") or []`. Empty form id (a project's own script), absent key, empty list: False. There is no fallback by language: Java, C#, Python hold an empty list and go to step 8.
8. Everything else → `_row_unsettled`: `incomplete`, `cause: judgment`. This includes at the statement with another kind (S1: `assert not (f())`, `f` raises `ValueError`: the critic, the same as the TS throw) and a marker-less `fires_as` miss.
9. Static guard `test_no_language_question_on_the_road`: walks the AST of **every** function of the road: `_target_of`, `_plan`, `judge_probe_row` and its `_row_*`, `_at_statement`, `_line_proof_allowed`, `_judge_rows`, `_judge_run`, `_probe`, `_resolve_oracle`, `plan_detector_mutation`, `build_request`, `_off_target_note`, `_refuse_flags`, `_new_record`, `_finish_record`. It refuses: a comparison with `"python"`; `.endswith(".py")`; a read of a name `detector`; `spec.get("language")`; `.get("reader")` or `["reader"]`; the words `not Python` in a string. Named exceptions only by a table in the test, module-level `ROAD_EXCEPTIONS`, each `(function, what, why)`: `build_request` reads `reader` (the runner's selection by node id, §3 #10); `_refuse_flags` reads `reader` (`--model`, §3 #17, F8); `_judge_rows` reads `is_pytest_command` (a runner's report grammar, not a language: `reporters.assertion_site` holds two grammars, named); `_judge_run` reads `judge_row` (not a language). `_reader_plan`, `parse_node`, `put_back` (§3 #11), and the F8 functions are named as off the list with their reason. A negative control plants `if not detector:` and `spec.get("language")`.

**Reuse in a more consequential role.** `_location_hits` moves from part of a conjunction to a part of a sufficient proof: direction toward `cause: judgment`; adversaries of §2 F1 pinned. `failure_frames` (B8e) moves to a fact that decides a place: direction toward the critic; frames None, an unknown `frames_deepest`, several problems of a soft collector, a same-numbered line in another file, and a library frame all give no substitute or a hit only on the mutated file; it never proves (step 6 reads first_read only).

`edges:` E3.1 no report, no rows: as today (`not_executed`). E3.2 `error` row: N4. E3.3 `fires_as` null: step 6 skipped, no crash, `_row_by_marker`'s `missed` note skipped. E3.4 **closed, not named as a residual**: an `AssertionError` raised by a helper in the arguments has a marker written and not read, so step 5 (Python's every form); on a marker-less form first_read is the helper's line, so not step 6-7. E3.5 param rows: E-D, `proved_by` weakest of (line < fires_as < marker), N3b writes it from all rows. E3.7 soft collector: marker first, R9 as today. E3.8 F7 of t-1968 disappears: the old reason mismatch is step 5 or 8, never `wrong_location` at the statement. E3.9 `line_proof_runners` still empty when N3b lands because N0 did not license a runner: step 7 unreachable, marker-less forms go to the critic, a line in the report, the owner is told. E-P; E-G; E-O. **The fixture case (F12=A):** an inverted assert in a Python fixture gives an `error` row: the critic, one judgment each.
`non-goals:` the seam, doors, words (N4); `red_sandbox` judging; `judge_alternative`; F11 (N5b).

tests (`test_probe_one_road.py`, table-driven, same table for each language; rows canned from real outputs: pytest JUnit from N0 into `fixtures/probe-languages/`; Playwright from N0 and `tr-probe` records): one test per step and language, `test_marker_outranks_place`, `test_passed_row_never_proved`, `test_marker_written_not_read_is_critic` (each language, F1=D's invariant, with a `fires_as` that would match), `test_throw_in_first_arg_never_proved_by_code`, `test_throw_in_matcher_arg_never_proved_by_code`, `test_rejected_resolves_never_proved_by_code`, `test_topass_callback_never_proved_by_code`, `test_line_proves_on_the_span_marker_less`, `test_line_needs_a_measured_runner` (same frame, `vitest` form id: critic), `test_line_empty_form_id_critic`, `test_no_column_goes_to_critic`, `test_multiline_span_other_line_critic`, `test_same_line_number_other_file_not_inside`, `test_foreign_assertion_error_python_critic` (B5's trace: `tests/helpers.py:12`), `test_substitute_never_proves`, `test_python_reason_mismatch_is_not_wrong_location`, `test_throw_at_statement_same_on_each_language` (S1), `test_weakest_row_speaks` plus the same **through `_judge_rows`**, `test_python_param_rows_all_judged`, `test_stale_id_pass_is_incomplete_not_no_failure`, `test_helper_never_called_pass_is_incomplete`, `test_oracle_pass_still_no_failure`, `test_no_language_question_on_the_road` plus its negative control. `test_probe_marker_judgment.py`: `test_place_alone_is_not_a_proof` kept.

`DoD:` `python -m pytest ai-packages/qa-factory/scripts/tests/test_probe_one_road.py ai-packages/qa-factory/scripts/tests/test_probe_marker_judgment.py ai-packages/qa-factory/scripts/tests/test_probe_marker.py ai-packages/qa-factory/scripts/tests/test_judgment_census.py -q`; `python -B ai-packages/qa-factory/scripts/tests/test_probe_plugin_param.py`; `python -B ai-packages/qa-factory/scripts/selftest.py --lang`. CI: `test_probe_by_code.py`, `test_probe_by_code_languages.py`, `test_probe_by_code_copy.py`, `test_probe_by_code_alternative.py`, `test_gate_registry.py`. AR-22 grep pasted for `test_file_frame`, `mismatches`, `message_head`, `matched_report_id`. `architecture: AR-13, AR-15, AR-19, AR-22, AR-23, AR-28, AR-29`; `judgment: judge_probe_row xref data; proved_by line is the owner's grant on a marker-less form (F13)`.

### N4 — step 4 reaches every read failure; step 5 is the last (F3, F6, B7)

`owns:`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\probe_by_code.py` (`_row_unsettled`; `judge_probe_row` — the `error` and `site_unread` lines only; `_judge_rows` — the `incomplete` block; `judgment_facts`; `_judge_input`; `_judged_record` — text only; `plan_detector_mutation` — `invert: null` raises `ToolRefusal`; `plan_mutation` — no target raises `ToolRefusal`; `_tool_refusal_record`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_marker_judgment.py`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_not_proved.py`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_gap_door.py`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_by_code.py`, `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_by_code_languages.py` (pins of §6; CI)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\design\state-exits.md` (the rows)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-2045-n4.md` (new)

Required behaviour:
1. `site_unread` on a failed row and an `error` row become `cause: judgment` with `judgment_facts` when the row has failure text; `location` may be null, the critic reads the text himself (the owner: «он сам может посмотреть на какой строке упало»).
2. Records with no failure text stay `cause: tooling`.
3. **Every unsettled row is shown (B7, E-D, E-Q).** `judgment_facts` takes the unsettled rows: `rows: [{test_id, status, message, failure_text}]`, at most `FACTS_ROWS_MAX` = 12, then `rows_cut: <n>`. The flat keys stay, from the first of them, for the existing readers (`proof_level.py:1119-1122`, `window_record.py:781`). `_judge_input` lets a quote come from the flat keys or any row. `fires` with `rows_cut > 0`: refused, door `cannot_judge` (`_judge_refusal`, A24 row). `_judge_rows`' `facts` are built from all judged rows with `cause: judgment`, not `row_facts.get(id(first))`. A mix with a tooling `incomplete` row: tooling, as today (:2850-2857). The facts hash covers `rows`.
4. **Head and tail (B7).** `FAILURE_TEXT_MAX` per row; a longer text keeps its head and its tail around one `…` (half each, the mark counts). INV: pytest's raising line, the last, survives the cut.
5. The critic's door and word are unchanged: `--judge`, `cannot_judge`, then the person's `probe not proved: <case>` (`probe_gap_block` :685, `probe_judgment_cases` :754). No new word. Mixed cases: t-2007 S3 stands.
6. `--judge` on a Python record works, tested. INV: critic's dispatch only (`_demand_critic_dispatch`); a judgment on other bytes is refused (E2.7); never rewritten (E2.8).
7. **Tool refusals for every reader (S4, S5, E-F).** `plan_mutation`'s no-target and `plan_detector_mutation`'s `invert: null` raise `ToolRefusal`; N2b's refused forms too. `_tool_refusal_record` reads `AD.entry_for_suffix`, then `AD.ast_entry`, so the record has `language` and `cause: tooling`, and `tooling_gap_key` works, so the owner's class word covers it. `exc.name_unproved` with a spec with no `tail` or `entry`: None (no record); the AST reader never raises `name_unproved` (its name is proved by `locate`).

`edges:` E4.1 `fires` with an empty stored text: refused (an existing refusal, nothing to quote), door `cannot_judge`; keep the test, no census line (S12). INV: no proof with no evidence. E4.2 S6 close: E-L. E4.3 `probe_gap_cases` shrinks: `probe_could_not_run` is false for `judgment` (:1086), so an error row no longer offers `probe gap`. INV: «a person never judges a probe's text before the critic did». E4.4 F6=A: off-target is not on this door; `OFF_TARGET_DOOR` says so (N6). E4.5 an old record `incomplete` + no `cause`, or `judgment_facts` with no `rows`: as today (`_judge_input` reads the flat keys). E-Q. An `error` row with an empty text: tooling (item 2).
`non-goals:` the seam's wording; `waiver.split_overridden` (TR2-2); widening the word (F6=B only).

tests: `test_probe_marker_judgment.py`: `test_site_unread_is_judgment`, `test_error_row_is_judgment` (flip of :133), `test_error_row_no_text_is_tooling`, `test_fires_refused_on_empty_text`, `test_judge_on_python_record`, `test_param_rows_all_shown_to_critic` (`[a]` failed unread, `[b]` `error`: both in `rows`, a quote from `[b]` accepted), `test_rows_cut_refuses_fires`, `test_long_text_keeps_head_and_tail`, `test_old_facts_no_rows_quote_ok`; `test_probe_not_proved.py`: `test_error_row_not_offered_as_gap`, `test_person_is_last` (no person's word listed for an unjudged record of each new kind; **walks `window_round_gate`**, the seam, not the predicate: neither the draft nor the critic has read it); `test_probe_gap_door.py`: `test_no_text_record_still_offered`; `test_probe_one_road.py`: `test_python_tool_refusal_has_language_and_cause`, `test_python_no_target_leaves_a_record`, `test_table_invert_null_leaves_a_record`.

`DoD:` `python -m pytest ai-packages/qa-factory/scripts/tests/test_probe_marker_judgment.py ai-packages/qa-factory/scripts/tests/test_probe_not_proved.py ai-packages/qa-factory/scripts/tests/test_probe_gap_door.py ai-packages/qa-factory/scripts/tests/test_state_exits.py ai-packages/qa-factory/scripts/tests/test_probe_one_road.py -q`; `python -B ai-packages/qa-factory/scripts/selftest.py --lang`. CI: `test_probe_gap_word.py`, `test_window_record.py`, `test_probe_by_code.py`, `test_probe_by_code_languages.py`. `architecture: AR-9, AR-14, AR-23, AR-24, AR-25, AR-28, AR-29`; `judgment: judge_record xref judgment unchanged; _judge_input shape data`.

### N5 — one hop for every language, through data (F4)

`owns:`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\detectors.json` (`helper_declaration` per language; `import_forms` [new optional])
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\assertion_detectors.py` (`ENTRY_FIELDS` optional + validation of `import_forms`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\probe_by_code.py` (`find_oracle` → takes the reader; `_called_names`, `_imported_modules`; `_resolve_oracle` no-target branch; `declared_once` [new]; `enclosing_declaration` [new])
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\probe_debt.py` (`_oracle_gone`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_one_road.py`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_assertion_detectors.py`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_by_code_languages.py`, `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_debt.py` (pins of §6; CI)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-2045-n5.md` (new)

Required behaviour: reached only when `_target_of` said `first` and the body has no check. Called names in source order; in the file, then the helpers' chain, then imported files inside the test tree (the guard of N1: a product module is never hopped into); the first declaration holding a check; the note names it as today (:395-397).
- **What Python has is kept (S10):** on the AST reader the conftest chain (`_helper_chain`) and fixture parameters (`_called_names` :317-320) stay followed, the 13797 class. On the table reader `import_forms` rows give the files; a fixture of `test.extend` is not followed: the refusal's door names `--at <file>:<line>`.
- More than one hop: `ToolRefusal`, door `--at <file>:<line>`. An unresolved import: skipped with a note.
- `import_forms` rows: `[{"pattern": "<regex with group path>", "resolve": "relative" | "dotted", "suffixes": [...]}]`. TS: `from\s+['"](?P<path>\.[^'"]+)['"]`, relative, the entry's suffixes. Java: `^import\s+(?:static\s+)?(?P<path>[\w.]+);`, dotted. C#: none (a namespace is no path): same file only, a note.
- `helper_declaration` wider rows, each verified on a real sample by the builder (`add_to_cart.spec.ts` page objects, an arrow const, a class method); an unverified row is not written (t-1968 rule).
- `enclosing_declaration(data, reader_entry, line) -> {name, first, last} | None` (pure): AST: the innermost `FunctionDef` holding the line; table: `helper_declaration` with `{name}` as a name group, the nearest declaration whose body spans the line. For N5b. None when none fits.
- `declared_once(data, suffix, function) -> ""` or why (pure; `locate` on the AST, `helper_declaration` on the table): `probe_debt._oracle_gone`'s `.py` gate is replaced by it (S9), so a replay needs no hand-named helper in any language. Its text stays "gone" reasons; a language with no entry: the reason names the data gap.

`edges:` E-B, E-C; INV: a helper in the product is never mutated; a name resolved twice in one file is a refusal with the lines (a body not certainly the named one is never mutated). A call name in a comment: the skeleton hides it. Empty `import_forms`: same file only, a note.
`non-goals:` a call graph; type resolution (`this.page.x()` by name only: a same-name wrong hit stays bounded by `is_assertion_id`).

tests: `test_one_hop_each_language`, `test_page_object_method_found` (a fixture shaped unlike the default, AR-2), `test_arrow_const_found`, `test_hop_never_into_product`, `test_python_conftest_and_fixture_param_kept`, `test_ts_fixture_not_followed_door`, `test_two_hops_refused_with_door`, `test_enclosing_declaration_each_reader`, `test_debt_replays_ts_helper` (S9).

`DoD:` `python -m pytest ai-packages/qa-factory/scripts/tests/test_probe_one_road.py ai-packages/qa-factory/scripts/tests/test_assertion_detectors.py -q`. CI: `test_probe_by_code.py`, `test_probe_by_code_languages.py`, `test_probe_debt.py`. `architecture: AR-1, AR-2, AR-15, AR-19`; `judgment: none (shape data on existing units); the guard safety data if a new unit, a raise named`.

### N5b — a helper not called exactly once: the marker yields to the facts (F11=A, B8)

`owns:`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\probe_by_code.py` (`_row_by_marker` — the guard; `_helper_call_facts` [new]; `target_fact` — `calls_in_test`; `_judge_rows` — passes `frames` and the facts)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_one_road.py`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json` (a row if a unit)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-2045-n5b.md` (new)

Required behaviour. For a target with `target_outside_body` not False (a local helper too, B8b):
1. The helper's name and span by `enclosing_declaration` (B8c); calls by `_helper_call_facts`: AST: `ast.Call` of that name in the test's body; table: `\b<name>\s*\(` on the skeleton of the body span. Written as `target.calls_in_test: <n> | null`, plan time.
2. At judging, with a marker read: walk `failure_frames` of the row from the deepest, by `AD.frames_deepest` (B8e): the first frame inside the helper's span in the mutated file; the next frame outward is the **caller frame**.
3. **The marker stands only when `calls_in_test == 1` AND the caller frame lies inside the test's body span in the test file.** Otherwise step 8 (`incomplete`, `cause: judgment`) with both facts: `calls_in_test` and the caller frame, in `judgment_facts`. Unknown of any of these (no name, no frames, `frames_deepest` None): the critic, with "unknown" named. This is a refinement of the critic's "deepest test-file frame": in a helper of the same file the deepest test-file frame is the helper itself, so the frame to read is the caller's.
4. The check for a target in the body is untouched: the marker stands.

Why it is not vacuous any more (B8a): the condition compares the frame with the test's body, not with the id. It catches the second call (count 2), a call from a hook while the body's call never ran (B8d: count 1, the caller in `beforeEach`), and a chain helper→helper (caller outside the body: the critic).

**Reuse:** `failure_frames` as a demoting fact: direction toward the critic only; it never adds a proof.

`edges:` E-N. Zero counted: the critic (not "the marker stands", which the first draft's E3.6 said). A fixture target (F12=A): the row is `error`, never here. An `oracle` given by hand (`--oracle`): the same rule; the target is outside the body. INV: a record never says proved with the Then's call unreached; the conflict with "marker first" is decided here by the facts, the meaning stays the critic's.
`non-goals:` a call graph; per-call instrumentation.

tests: `test_helper_called_once_from_body_marker_stands`, `test_helper_called_twice_goes_to_critic`, `test_helper_called_in_hook_and_body_goes_to_critic`, `test_local_helper_same_file_caller_frame`, `test_helper_never_counted_goes_to_critic`, `test_frames_deepest_first_and_last` (a TS stack and a pytest traceback, the same rule), `test_frames_unknown_goes_to_critic`, `test_target_in_body_marker_stands`.

`DoD:` `python -m pytest ai-packages/qa-factory/scripts/tests/test_probe_one_road.py ai-packages/qa-factory/scripts/tests/test_judgment_census.py -q`; `python -B ai-packages/qa-factory/scripts/selftest.py --lang`. CI: `test_probe_by_code.py`, `test_probe_by_code_languages.py`. `architecture: AR-15, AR-22, AR-28, AR-29`; `judgment: _helper_call_facts xref data; the meaning stays the critic's`.

### N6 — what the roles read (text, after behaviour; carries TR2-1 item 3 under F5)

`owns:`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\agents\qa-code-critic.md` (:71-72)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\skills\qa-story\phases\s5.md` (:200)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\execution-lifecycle.md` (:60)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\slices\qa-code-critic\execution-lifecycle.md` (regenerated by `contract_slices.py --write`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\brief_pack.py` (:224-227, text)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\window_record.py` (`OFF_TARGET_DOOR`, text)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\proof_level.py` (`reached` :1483-1484, text)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\probe_debt.py` (:161, :222, text)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\probe_by_code.py` (module docstring, `_build_parser` help, `_run_and_judge` :3110 reason text, `plan_detector_mutation` docstring)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_code_critic_probe_rule.py`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-2045-n6.md` (new)

Required: the charter says, as experience:
- a probe proves only the check it broke; with no `--at` it aims at the row's `assertion_id`;
- **compare the line the record names with the Then, as you read the test: with the id as the default the record says "on target" by construction, so a stale id on another Then's check proves with a clean record, and you are the only reader left (S8);**
- a Then whose check passes when inverted (the element goes away by itself) returns `unverified` with its reason;
- `proved_by: line` is the code's reading of a place on a form with no marker: read the statement when it matters;
- a `cause: judgment` record may show no location, then read the failure text and see the line yourself; a marker written and not read means the run failed some other way until you see otherwise;
- several `rows`: `fires` says each row reached the check; if one did not, `other_failure`;
- a person is asked only after you say `cannot_judge`.
No text says "Python" or "not Python" on the road.

`edges:` `role_load.py --role qa-code-critic` tokens over the `process_ratchet_tokens` ceiling: cut as much as added; a raise is named (AR-20). INV: FR-37, every path and command named is what code accepts.
`non-goals:` `p1-discovery.md:211` (a list of readers, true as written); new rules.

tests: `test_code_critic_probe_rule.py`: `test_charter_says_target_and_order`; `test_no_python_exception_text` over the owned TEXTS (the markdown, `brief_pack`'s lines, `OFF_TARGET_DOOR`, `reached`, `probe_debt`'s lines, and of `probe_by_code.py` only the module docstring and the help); it imports `ROAD_EXCEPTIONS`' F8 lines as allowed (:2909, :3833 stand until F8's node), so one table serves both (negative control: a planted line). DOC witness per rule 11: keys quoted from this DoD, committed as a test.

`DoD:` `python -m pytest ai-packages/qa-factory/scripts/tests/test_code_critic_probe_rule.py ai-packages/qa-factory/scripts/tests/test_charters_s5_s9.py ai-packages/qa-factory/scripts/tests/test_contract_slices.py -q`; `python -B ai-packages/qa-factory/scripts/role_load.py --role qa-code-critic --json`; `python -B ai-packages/qa-factory/scripts/contract_slices.py --check`; `python -B ai-packages/qa-factory/scripts/selftest.py --lang`. CI: `test_brief_pack.py`, `test_window_record.py`, `test_probe_debt.py`. `architecture: AR-9, AR-10, AR-22, AR-29`; `judgment: none`.

### F8's own node (not in this graph; the owner's question open)

The Lead issues its id, writes the finding, and asks the owner (§2 F8). Nothing here depends on the answer. Until then the F8 branches stand, named in `ROAD_EXCEPTIONS`.

### Live proof (FR-33; goes with the batch's table, not a builder; after TR2-1's remainder)

On a stand copy, the owner's three cases: a Then in the second `expect`; a check in a helper; a throw in the arguments. A marker-less form (`tests/api/users/get-user.spec.ts` import shape). A retarget after `no_failure` (the door, B10). Plus one Python sample project with the same three, one `self.assertEqual`, and, if the sample has it, Playwright for Python; a count of helpers the E10 guard now refuses (S11). Not closed by code alone. Carrier: «Живые доказательства» of batch-2, or `live-runs` by a person's word.

## §7 Small choices closed by the designer

- `judge_detector` renamed `judge_probe_row`: the old name is false once Python goes through it; keeps `^judge`, keeps the census class.
- `--at <file>:<line>` as the second form rather than a new flag: it is the id's spelling.
- `--oracle` stays: one sentence in the help, no removal (out of the owner's words).
- Static guard as a test, not a gate: the road's functions are few and named.
- New test file `test_probe_one_road.py` (fast): the shared table across languages is the point.
- Column read through the existing `_COLUMN` :1969, one reader.
- `AD.ast_entry` name; the key `assertion_probes_ast`; `reader`, `matcher_span`, `frames_deepest`, `line_proof_runners`, `no_proof_after`, `no_proof_args`, `forms`, `FACTS_ROWS_MAX` = 12, `work/probes/<iid>--L<line>.json` as names and values.
- N7 before N2 (the first draft had it parallel with N4): the plan contract is then written once, without an `expected` branch. Critic's graph otherwise kept; N4 ∥ N5 by named helpers.
- Splits: N1b, N2b, N3a/N3b, N5b, over the critic's "may add N2b".
- `matched_report_id` kept: the critic said it "can go", no reader in `scripts/*.py`; K2 pins it in `test_probe_plugin_param.py:72`, which the critic's grep did not cover. Not worth a pin flip here.
- `_judge_row` removed with `verdict_of`, against the first draft's §3 #13 ("alternative only"): the alternative uses `_judge_alternative_row`, read at :3653, :3897.
- `no_proof_after` / `no_proof_args` unconditional rather than N0-conditional: the error direction costs one judgment, and a reading on one runner cannot license a rule on three.
- Caller frame for N5b, not "deepest test-file frame": §6 N5b item 3.
- E-F's refusal text says "of a form the factory reads" (FR-1): a real check of an unknown form must not read as the author's fault.

## §8 Reported, not widened

- `reporters.failure_frames` keeps text order; N5b is its first order-dependent reader. Other readers unchanged.
- A pass on a helper the id names, called exactly once, is `incomplete` here, by the critic's B6 as read, where a `--oracle` of the same helper gives `no_failure`. N5b's count could separate them later; not done, the direction is the safe one. A candidate if the critic's load shows it.
- `_resolve_oracle` :2945-2946: Python's silent fallback and no test-tree guard (closed by N1); `_imported_modules` can reach a product module (closed by N5).
- `judge_detector` :1953-1955 compares a line number with no file (fixed by N3b).
- The record at `add_to_cart.spec.ts:59`: the default probe broke a `setup:` line, and the frame's path is another clone's (`tr-arm-b`) inside `tr-probe`'s record; the location still resolved. Not chased.
- `window_record.py:176` legend «a file:line or an id»: goes to TR2-1 (F10).
- `proof_level.code_sha` :564: a language-dependent identity, off this road: TR2-16.
- `docs/SIBLING_MAP.md:148` must change with F2=B; no node owns the map: the Lead's edit (§5.6). TR2-15's new axis stays queued to Fable.
- The rest of t-2046 (`s5_precheck`, `manifest_from_tests`, `arch_check` silent `checked`, `judge_code`, `run_suite`, `manual_capture`, ...): TR2-16, untouched here. `arch_check`'s silent "checked" (FR-41 shape) is the one the census ranks second; analog, not widened.
- Python's new vocabulary is read by the probe only: `manifest_from_tests` and `validate_artifacts`' `assertion_heads` still do not see `self.assertEqual` as a check. A Then-binding gap on that road is TR2-16's.

## §9 Reading trail

First draft: `probe_by_code.py`: Grep of `first_assert|proved_by|_off_target_note|wrong_location|plan_mutation|--at|assertion_probes|assertion_id|python` (-i); Grep of `detector|.py`; Grep of `^def ` and named defs; Read :28-162, :225-414, :478-602, :828-857, :936-1036, :1179-1193, :1300-1409, :1504-1533, :1655-1694, :1720-2001, :2500-2549, :2655-3079, :3219-3299, :4270-4364. `detectors.json`, `t-1968`, `t-2037`, finding files, `batch-2`, `reporters.py`, `window_record.py`, `proof_level.py`, `assertion_detectors.py`, `brief_pack.py`, `s5.md`, `agents/qa-code-critic.md`, `architecture.md`, `judgment-census.json`, `slow_tests.json`, `builder-rules.md`, `t-2000`; stand read-only (as in the first draft).

This pass (t-2054), read on `D:/ws1/wt-fbfix`:
- Given: `t-2050-critic-plan-t2045.md` whole, `t-2045` whole, `t-2046` whole.
- `probe_by_code.py`: :160-404 (`parse_node`, `first_assert`, `find_oracle`, `_called_names`), :480-604, :1308-1407, :1504-1533, :1655-1782, :1780-2003, :2680-2905, :2905-3102, :3105-3114, :3219-3303, :4234-4263, :4366-4407.
- `references/detectors.json` :195-303 (Java, TypeScript, note). `references/gate-registry.json` :566-579.
- `red_sandbox.py` :885-924. `execution_request.py` :616-618, :3525-3564. `reporters.py` :309-368. `proof_level.py` :1225-1333. `probe_debt.py` :155-239. `launch_check.py` :701-704 (`runner_identity`). `references/launch-causes.json` :28-35 (form ids `pytest`, `jest`, `vitest`, `playwright-test`).
- Tests: `test_probe_marker.py` :335-353, :395-468; `test_probe_marker_judgment.py` :95-139; `test_probe_plugin_param.py` :1-89; `test_probe_by_code.py` :125-134, `^def` map; `test_probe_by_code_languages.py` `^def` map; Grep of `judge_detector|_judge_detector_rows|verdict_of|matched_report_id` over `tests/test_probe*.py`, and over `*.{md,json}`; `test_gate_registry.py` :937-938, :963-974.
- Counts: `judgment-census.json` ratchet line 4; `"class": "safety"` 50 lines; `safety|meaning-proxy` 58 lines.
- Controls: `assertion_probes_ast|ast_entry` over `PKG` is empty, and the same call on `assertion_probes` gives 151 hits in 28 files. `slow_tests.json` for `test_gate_registry` hits (slow), `test_probe_plugin_param` and `test_judgment_census` do not, the same call finds `test_probe_binding`.
- Stand, read-only: `playwright.config.ts` (it holds `globalSetup`, `webServer`, `cfg`: why N0 has its own config); `node_modules/@playwright/test/package.json` (1.56.0; Glob under `node_modules` returned nothing, read directly); grep of `import { ... expect ... } from` under `tests/` (`get-user.spec.ts:1` from a fixture file).

Reasoned, not run (named so): the JS frames of d, e1, e2 (N0); the pytest row for a fixture's assert (F12, N0 p7); the unittest and Playwright-for-Python message landing in JUnit (N0 p5, p6); the 3-hour sizes. Not read: `window_round_gate` (N4's test walks it), `window_record._probe_from_receipt` (N1b reports it), `_tail_matches`, `_frame_site` beyond its citation, the census's `_resolve_oracle` row.

Needed beyond the manifest: everything above outside the three given paths; the batch rows; the stand's config and `node_modules`.

## §10 Where each B-n and S-n landed

| Id | Landed in | How |
|---|---|---|
| B1 | N2 items 1, §3 #1, #10, #12, #17, #19, #21, #23; N3b item 0 | `reader` key; the five sites by name; `language`, `entry` in N3b; `test_python_alternative_still_runs_after_n2` |
| B2 | N3a item 2, 3; E-D | no-file contract through `matching_rows`; all `pytest_command`s; tests through `_judge_rows`. `matched_report_id` kept, §7 |
| B3 | N3a item 4 | gate `reporters.READERS`; `test_reporter_pytest_reaches_site_reader` |
| B4 | §2 F1; N2 items 5, 6; N3b steps 6-7 | `matcher_span` at plan time, on the matcher, line and column; `.resolves`, callback get no span; runner list |
| B5 | §2 F1=D; N3b steps 4-7, E3.4 | marker written and not read goes to the critic; substitute never proves; forms' `fires_as` null (N2b); `test_foreign_assertion_error_python_critic` |
| B6 | N1 item 6, N3b step 2, E-O | `target_outside_body`, empty keys; `among` reworded; `test_stale_id_pass_is_incomplete_not_no_failure` |
| B7 | N4 items 3, 4; E-D, E-Q | `rows`, quote from any, head and tail, `FACTS_ROWS_MAX`, `test_param_rows_all_shown_to_critic` |
| B8 | §2 F11; N5b; N2 (`frames_deepest`); N5 (`enclosing_declaration`) | (a) compared with the body; (b) local helper via `target_outside_body`; (c) name by `enclosing_declaration`; (d) count + caller frame; (e) data key |
| B9 | N0 | new DoD: all shapes, Python half, writer on a scratch folder with no product, exact commands, decision rule per runner |
| B10 | N1b; §5.3; AR-9 row | repeat by bytes AND target, beside record, `test_printed_door_runs_second_call` |
| B11 | §6 Shared and pin-owner table; each node's `owns` | slow files edited by the flipping node, "CI"; the rename in one commit; added beyond the critic: `test_probe_plugin_param.py`, `gate-registry.json` + `test_gate_registry.py` |
| S1 | N3b steps 4, 8; `test_throw_at_statement_same_on_each_language` | outside only is `wrong_location` |
| S2 | N3b item 9 | wider list, bans, `ROAD_EXCEPTIONS` with `pytest_command` named |
| S3 | §3 #19, N2 item 7 | `_reader_plan`; the condition stated |
| S4 | N4 item 7, §3 #25 | |
| S5 | N4 item 7, E-F | |
| S6 | N7 | the `--mutation` line stays until `_refuse_flags` refuses |
| S7 | N6 owns and tests | :3110, `probe_debt` texts; `detectors.json:302` in N2; `test_no_python_exception_text` narrowed, table shared |
| S8 | N6 charter; N1 item 7; E-N | |
| S9 | §3 outside table; N1 item 2; N5 `declared_once`; §8 stale line removed | t-2046 has landed; compared |
| S10 | N5 | conftest, fixtures kept; TS fixture door |
| S11 | N1 item 4; live proof | estimate named; counted in the proof |
| S12 | §1 census; N4 E4.1 | census line dropped, test kept |
| S13 | N1 item 3 | one rule |
| Answer (1), 7 branches | B5; F1 fallback removed (runner list); S1; N2b; F10 §5.5; F8; S9 | all seven answered |
| Answer (3) | §1 AR-29; F13; S8 | |
| Answer (4) | §5 | four corrections |
| Answer (5) | N0 | |
| Map, batch rows | §5.6 | the Lead's edits, not a builder's |

# P1-b, main pass after N2h-a: re-label `main/S5` (FV3-20) and N2h-v (critic stub writes the window and the digest) - DRAFT cards

task: t-1047 | feature: F19 | drafted by: designer (opus) | status: DRAFT, for Lead acceptance; forks are in §4, not decided here.
Tree read: the root checkout `C:/QAFactory/forge-repo`, `main`, head b5719988 (includes the N2h-a merge b1243561).

## 0. What the run says and what the code says (load-bearing facts, read this round)

| # | fact | carrier |
|---|---|---|
| A1 | The main pass stops at S5. The exit gate of `S5-qa-code-critic-1` has 3 findings: (a) the digest is not the handoff form, names no path, and TC-1 has no line; (b) `review.receipt_ref` is not filled; (c) `probes.runtime_provenance` is not filled, "no run block of dispatch S5-qa-code-critic-1 under work/run-blocks/ carries a runtime_provenance record". | `docs/tasks/specs/reports/20261117-p1b-n2ha-main-lines-r2.txt:24`, `:44-45` |
| A2 | The pass prints `known red: main/S5 -> FV3-5`. The label's `raised_by` still names the old reason, "9 finding(s) ... (the code critic stub leaves the handover form unfilled)". The label is stale (critic t-1029 F10). | lines `:23`; `scripts/tests/fixtures/driver-exits/known_red.json:4-7` |
| A3 | Time: `266.6 s in 4 driver process(es)`, S5 68.2 s. The limits are 800 s (stop) and `TEST_TIMEOUTS` 900. | lines `:49`; finish spec `:415` edge 8, `:617-620` F-P18 |
| A4 | The digest is the stub's final message: `mine.get("result_text") or default`. The default is prose: "<role> <stage> <task> - the stub filled the handover form of <dispatch>; nothing else to say". Every other role that passes its gate carries a `result_text` row in the story. `qa-code-critic@S5` has none: it has only `files`. | `scripts/tests/dry_stub.py:936-937`; `scripts/tests/fixtures/stories/dry-1/story.json:9-12,34-46,55,63,79` |
| A5 | What the digest check reads. `role_digest.check(text, scope)` wants a header `<role> <stage> <window> · ok|concerns|halt|impossible`, one row per scoped id, and a task-relative path line. The scope is the controller's `scope`/`cases` of the dispatch. The critic's row state is one of `approved`, `approved_with_fixes`, `rejected`, `unverified`. | `scripts/role_digest.py:183-207,368-386`; `scripts/exit_gate.py:1112-1131`; `agents/qa-code-critic.md:82-84` |
| A6 | Where `review.receipt_ref` comes from. `handoff_check --fix` derives it as `work/windows/<dispatch>.json` only when that file exists. The file is written by `window_record.py --task <T> --dispatch <ID> [--review-receipt]`, and it is written BEFORE the verdict whatever the exit (exit 1 = window not acceptable, and the file stays). `--review-receipt` writes the immutable receipt only on an acceptable, derivable or sent-back window. | `scripts/handoff_check.py:158-170,644-658,1642-1659`; `scripts/window_record.py:2161-2176,2191-2196,2230-2267,2270-2283` |
| A7 | The critic's card names `window_record.py --task <TICKET> --dispatch <your dispatch id> --review-receipt`, and `manifest_put.py --fragment` for review fields. It does NOT name `run_suite.py --mine` (only `--detail`, which launches nothing). | `agents/qa-code-critic.md:69`; `scripts/brief_pack.py:238-258` (critic card: probe_by_code, red_sandbox, RUN_DETAIL, MANIFEST_VIEW, STAND_PROBE, s5_precheck) |
| A8 | Where `probes.runtime_provenance` comes from. It is derived ONLY from the newest run block whose `dispatch_id` is THIS dispatch and that carries `runtime_provenance` (`window_runtime_record`). | `scripts/handoff_check.py:522-586,645-646` |
| A9 | The critic's probe writes no run block. `build_run_block` returns None for `purpose == "red_probe"`. The probe's own docstring says so. | `scripts/run_suite.py:470-473`; `scripts/probe_by_code.py:13-16` |
| A10 | A `run_suite.py --mine` over bytes that already hold a result answers `reused`/`already_run`, exits 0 and writes NOTHING (no request, no job, no block). The automator already ran `--mine TC-1` at S5. | `scripts/run_suite.py:30-33,2074-2082`; `scripts/tests/dry_stub.py:583-587` |
| A11 | **Conclusion (by reading, not measured):** no tool on the critic's road writes a run block of the critic's dispatch. So (c) cannot be filled by any stub that does only what the role is handed. It is a **product gap candidate**: a required field whose only producer the role never triggers (FR-5, FR-11, AR-22). It is not a stub gap. The FV3-5 finding guessed the opposite ("`probe_by_code.py:13` runs `run_suite.py --request`, so FV3-5 probably also produces the run block - an estimate"). A9 contradicts that guess. | `plans/piles/live-run-fvf/findings/20261117-p1b-s5-zaglushka-kritika-ne-zapuskaet-probu.md:14,31` |
| A12 | The `node` check is a pattern only. `known_red.load` refuses a node that does not match `^[A-Z][A-Z0-9]*-[0-9]+[a-z]?$` (`FV3-20` matches). `reconcile` matches by row id only and never reads `raised_by` text; this is why the stale label stays green. `dry_exits` fails a row that is `after:<node>` while its ledger names the same node for it. No code checks that the node has a finding file or a batch row: that is discipline (`piles.py check` (е) checks the FINDING side, i.e. that a finding is named in a batch row). | `scripts/tests/known_red.py:18,104-106,130-152`; `scripts/tests/dry_exits.py:1460-1461`; `tools/piles.py:64-66,2181-2186` |
| A13 | Batch 3 is TAKEN: `статус: в работе | взял: dev1, 17.11.2026`. Rows FV3-16…FV3-19 were added by L0 (t-969) BEFORE the take ("Взятие пачки ... отдельным ходом после этого"). For a taken batch, `piles.py check` (в) refuses any changed line outside Ход, Остатки, Статус cells, queue lines and the header's статус/MR. A new «Узлы» row is red; the door is `piles-skip: в -- <reason>`. TEAMWORK §2 puts a new finding's row in an UNTAKEN batch of the pile. Batches 1 and 2 of `live-run-fvf` are «ожидает». The card row of a taken batch freezes Что/Строки/Размер/Взял/Ветка. | `plans/piles/live-run-fvf/batch-3-live-run-fvf.md:3,14,54`; `tools/piles.py:1644-1702,1591`; `docs/TEAMWORK.md:5-14`; `plans/piles/live-run-fvf/README.md:23-25` |
| A14 | A finding must also get a row in the card's «Содержание» table (`tools/test_pile_cards_contents.py`, run by forge-check). | `docs/TEAMWORK.md:11-12`; `README.md:154-159` (the Пачка 3 rows) |

## 1. Part 1 - the label `main/S5 -> FV3-20` (call it N2h-b2; it is a node of the label class N2h-b/L2)

**What must exist for the label to be legal** (K-L of the finish spec: the row's `node` is a batch node with a finding file, and `raised_by` names the class, `:98`):
1. the finding file (full text in §1.1);
2. the batch row naming the finding (§1.2; where it goes is fork F1);
3. the «Содержание» row in the card (§1.3);
4. the `known_red.json` row (§1.4), with the pin unchanged at 1.

Code checks only item 4's form (A12). Items 1-3 are held by `piles.py check` (е) on the finding side and by the acceptor on the node side.

### 1.1 Finding file - full text

Path: `C:/QAFactory/forge-repo/plans/piles/live-run-fvf/findings/20261117-p1b-s5-kritik-ne-pishet-okno-i-daidzhest.md`

```markdown
# После N2h-а главный проход сухой стори встаёт на S5 по новой причине: заглушка критика кода не пишет запись окна и дайджест в форме передачи; `probes.runtime_provenance` у критика без производителя (метка `main/S5`)

id: — | кучка: `live-run-fvf` | от: строки главного прохода после слияния N2h-а (`docs/tasks/specs/reports/20261117-p1b-n2ha-main-lines-r2.txt`, `:23-24`, `:44-45`); вердикт критика t-1029 (F10) | приоритет: П1 | кандидат наверх: нет

## Что не так

Класс фабрики: **тестовый слой делает за роль не все её шаги, которые требует ворота выхода, и проход молча встаёт; часть причины — на стороне заглушки (`stub gap`), часть — кандидат в разрыв продукта: обязательное поле формы, производителя которого роль не запускает (`product gap`, оценка по чтению, не измерение)**.

Факты (строки CI главного прохода на `main` после N2h-а):

- Проход закрывает S0-S4 и встаёт на S5 (266,6 с в 4 процессах драйвера). Ворота выхода `S5-qa-code-critic-1` называют 3 находки: (а) итоговое сообщение не в форме дайджеста: нет пути артефакта, у TC-1 нет строки; (б) `review.receipt_ref` не заполнено: «work/windows/<this dispatch>.json, written by window_record.py»; (в) `probes.runtime_provenance` не заполнено: «no run block of dispatch S5-qa-code-critic-1 under work/run-blocks/ carries a runtime_provenance record».
- Метка `main/S5 -> FV3-5` печатает прежнюю причину («9 finding(s) … leaves the handover form unfilled»): `known_red.reconcile` сверяет только id строки, текст `raised_by` не читает (`scripts/tests/known_red.py:130-152`), поэтому новая причина на той же стадии осталась незамеченной (F10).
- (а) — заглушка: её итоговое сообщение — `result_text` строки истории или проза по умолчанию (`scripts/tests/dry_stub.py:936-937`); у `qa-code-critic@S5` в `story.json` строки `result_text` нет (`:34-44`), у остальных ролей есть.
- (б) — заглушка: карточка критика называет `window_record.py --task <TICKET> --dispatch <your dispatch id> --review-receipt` (`agents/qa-code-critic.md:69`); заглушка его не зовёт. `handoff_check --fix` выводит поле, только когда файл `work/windows/<dispatch>.json` есть (`scripts/handoff_check.py:158-170`).
- (в) — кандидат `product gap`: поле выводится только из блока запуска С ЭТИМ dispatch, несущего `runtime_provenance` (`scripts/handoff_check.py:525-586`). Проба критика блока запуска не пишет (`scripts/run_suite.py:472-473`, `scripts/probe_by_code.py:13-16`), повтор `run_suite.py --mine` на тех же байтах отвечает `reused` и не пишет ничего (`scripts/run_suite.py:30-33`, `:2074-2082`), а `--mine` в карточке критика нет (`scripts/brief_pack.py:238-258`). Ни один инструмент дороги критика не производит то, что поле требует (FR-5, FR-11, AR-22). Прогноз находки FV3-5 (`:14`: «проба, вероятно, порождает блок запуска») чтением не подтверждается.

Не установлено: (в) — по чтению кода, не по прогону; меряет первый шаг узла N2h-в (строка `main/stop` после того, как (а) и (б) сняты).

## Что именно менять

Выбранное направление (Lead, 17.11.2026; спека `docs/tasks/specs/20261117-p1b-n2h-v-critic-stub-window-card.md`):

1. (а), (б) — узел N2h-в: `ai-packages/qa-factory/scripts/tests/dry_stub.py` (ветка критика кода S5) запускает ПРОЦЕССОМ настоящий `window_record.py --review-receipt` после проб и после фрагмента отзыва; `scripts/tests/fixtures/stories/dry-1/story.json` получает строку `qa-code-critic@S5.result_text` (дайджест роли — данные истории, как у остальных ролей) и фрагмент отзыва (`critic_verdict`) — данные суждения роли. Заглушка не сочиняет вывод инструмента (AR-29, FR-58).
2. (в) — не обходится заглушкой (AR-28): если после N2h-в проход встаёт на S5 только по (в), Lead выдаёт новый id под класс `product gap`, заводится отдельная находка о производителе `probes.runtime_provenance` у критика, метка `main/S5` переходит на него (F10).
3. Тест — строки `dry_stub.py --selftest` (см. спеку, карточка N2h-в).

Принципы и правила: AR-29, AR-22, AR-28, AR-13; FR-5, FR-11, FR-58; P31.

Решение владельца нужно: нет.
```

### 1.2 Batch row - text and place (fork F1)

On recommendation F1 (b), the row goes into `plans/piles/live-run-fvf/batch-3-live-run-fvf.md` «Узлы», right after the FV3-19 row (`:48`):

```
| FV3-20 | П1 | Находка: после N2h-а главный проход встаёт на S5 по новой причине — заглушка критика кода не пишет запись окна (`window_record.py`) и дайджест; `probes.runtime_provenance` у критика без производителя — кандидат `product gap` (`findings/20261117-p1b-s5-kritik-ne-pishet-okno-i-daidzhest.md`) | designer → builder → critic | `scripts/tests/dry_stub.py` (ветка критика S5), `scripts/tests/fixtures/stories/dry-1/story.json` (строка `qa-code-critic@S5`); метка — `…/driver-exits/known_red.json` (`main/S5`) | FV3-5 | ожидает |
```

There is also a «Ход» line (Ход is masked by (в), so it is always legal):
`- 17.11 (t-1047) — находка FV3-20 (после N2h-а остановка S5 сменила причину, F10 критика t-1029); метка `main/S5 -> FV3-20`; узел N2h-в — спека `docs/tasks/specs/20261117-p1b-n2h-v-critic-stub-window-card.md`.`

The commit message carries `piles-skip: в -- Lead t-1047: FV3-20 issued by the Lead of the taken batch for the moved S5 stop of FV3-5 (F10); row added after take`.
The card row 3's frozen «Строки» cell stays `FV3-1…FV3-19`. Editing it falls under the same (в) door; the recommendation is to leave it and add the Ход line.

On F1 (а) (the rule-text road), the same row goes into `batch-2-live-run-fvf.md` «Узлы» with the id the Lead issues there (`FV2-93` - the last FV2 id in the card is FV2-92, `README.md:153`), and no door is needed. Everywhere in §1 and §2, `FV3-20` then reads as that id.

### 1.3 «Содержание» row (`plans/piles/live-run-fvf/README.md`, after `:159`, under **Пачка 3**)

```
| `findings/20261117-p1b-s5-kritik-ne-pishet-okno-i-daidzhest.md` | находка, id — | после N2h-а проход встаёт на S5: заглушка критика не пишет запись окна и дайджест; `runtime_provenance` у критика без производителя (кандидат `product gap`) | `scripts/tests/dry_stub.py`, `scripts/tests/fixtures/stories/dry-1/story.json` | пачка 3, FV3-20 | нет | строки `main` r2 (`:23-24`, `:44-45`); FV3-5, FV3-19; F10 t-1029; AR-29, AR-22, FR-5 |
```

### 1.4 The ledger row (`scripts/tests/fixtures/driver-exits/known_red.json`, `main/S5` only)

```json
  "main/S5": {
   "node": "FV3-20",
   "raised_by": "stub gap: Lead t-1047, 2026-11-17: stopped at S5: exit gate for S5-qa-code-critic-1 (qa-code-critic, S5): 3 finding(s): digest not in the handoff form; review.receipt_ref not filled (no window_record.py run); probes.runtime_provenance not filled (product gap candidate, measured after N2h-v)"
  }
```
`pins.known_red` stays 1 (one row out, one row in; no raise).

### 1.5 Card N2h-b2 (header-ready)

given:
- this spec §0, §1 (the finding text, the row texts, the ledger row, verbatim)
- `C:\QAFactory\forge-repo\docs\tasks\specs\reports\20261117-p1b-n2ha-main-lines-r2.txt`
- `C:\QAFactory\forge-repo\plans\piles\live-run-fvf\batch-3-live-run-fvf.md`
- `C:\QAFactory\forge-repo\plans\piles\live-run-fvf\README.md`
- `C:\QAFactory\forge-repo\docs\TEAMWORK.md` §2
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\known_red.py`

owns:
C:\QAFactory\forge-repo\plans\piles\live-run-fvf\findings\20261117-p1b-s5-kritik-ne-pishet-okno-i-daidzhest.md (new)
C:\QAFactory\forge-repo\plans\piles\live-run-fvf\batch-3-live-run-fvf.md (only the FV3-20 row after FV3-19 and one «Ход» line; on F1 (а): batch-2-live-run-fvf.md instead)
C:\QAFactory\forge-repo\plans\piles\live-run-fvf\README.md (only one «Содержание» row under «Пачка 3»)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-exits\known_red.json (only the `main/S5` row)
non-goals:
- the stub code (N2h-v)
- the (c) product finding (§4 F2)
- the card's «Пачки» row (frozen)
- `known_red/<group>.json` (owned by the group nodes)
- `slow_tests.json` (no time change)
handoff: builder report `C:\QAFactory\forge-repo\docs\tasks\specs\reports\20261117-p1b-n2h-b2-report.md` (new) with the witness lines verbatim
edges:
- (1) Stale label. A label whose `raised_by` names a reason that `main/stop` no longer prints is the defect fixed here. Invariant: a label never names a reason the pass does not print (AR-28, F10).
- (2) Pin. `pins.known_red` stays 1. A count of 0 or 2 is a red that `--check` names, never edited to fit.
- (3) After-rows. Rows of `known_red/<g>.json` that start after S5 print `after:FV3-20` from now on. `dry_exits.py:1460-1461` fails a row whose ledger names FV3-20 while it is `after:FV3-20`. Today the only group ledger row is `kind:halt/free words -> FV3-16`, so no such row exists. Invariant: no ledger row is expected red for the defect that made it unreachable.
- (4) Taken batch. Without the `piles-skip: в` line the commit is refused by `piles.py check` (в) in commit-msg (`.githooks/commit-msg:38-40`). This is the gate's named door, an informed pass (FR-4). On F1 (а) no door is needed.
- (5) TEMPORAL. The label is right for the tree BEFORE N2h-v. After N2h-v the S5 stop changes or vanishes, and the label must move in N2h-v's wave (card §2, edge T). Invariant: `main` never holds a label stale against the stop it prints.
- (6) Two writers. `known_red.json` `main/*` must have no second writer in the same wave (finish spec `:67`, AR-14). N2h-v does not own it until its own label step.
DoD: `python -B ai-packages/qa-factory/scripts/tests/dry_exits.py --check` prints `0 discrepancies`; `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/tests/fixtures/driver-exits/known_red.json` (the slow file it names is judged by the coordinator's `dry_only` door: `NOTE dry-1/main/known_red: known red: main/S5 -> FV3-20`); `python -B tools/piles.py check --all` shows no red for (е) on the new finding; `python -m pytest tools/test_pile_cards_contents.py -q` is green; DOC-DISPATCH key run (CLAUDE.md R11, three properties) on the finding, with the keys verbatim: `Класс фабрики:`, `stub gap`, `product gap`, `Не установлено:`, `Выбранное направление`, `Решение владельца нужно: нет.`
siblings: axis 18 (shrink-only ledger: the pin unchanged, `raised_by` named); finish spec K-L
designer: this file

## 2. Part 2 - N2h-v: the critic stub writes its window and ends with the digest

### 2.1 Items (expected behaviour per item, test row per item)

**V1. The critic's review fragment (story data) goes through the ONE fragment road before the window record.**
- Extract the story-fragment loop of `automator_branch` (`dry_stub.py:577-582`) into one function, e.g. `merge_story_fragments(project, task_dir, kit, dispatch, fragments, out, run, tag)`. It validates the shape exactly as `:539-541` does (KitError names the key), writes each fragment under `state/dry-stub-fragments/<dispatch>-story-<n>.json`, runs `manifest_put.py --task <T> --fragment <file>` through `run`, and records the result with `_record`.
- `automator_branch` calls it for `manifest_fragments` (behaviour unchanged). `critic_branch` calls it for `qa-code-critic@S5.manifest_fragments`.
- Story row (fork F4 (a)): one fragment `{"tests": [{"instance_id": "test_the_case", "file": "qa-factory/tests/TC-1_test.py", "covers": ["TC-1"], "critic_verdict": "approved"}]}`. The shape comes from `references/artifact-contract-automation.md:11-15`; the merge keys are measured by `manifest_put`'s answer, and a refusal is a `live_only` row, never retried with other keys.
- Test row: `N2h-v: the critic's story fragment goes through manifest_put.py before window_record.py (call order)`. Use a fake `run` that records calls; expected order: probes..., manifest_put, window_record.

**V2. `window_record.py --task <T> --dispatch <ID> --review-receipt` runs as a process, once per critic call, after the probes and V1, before the form.**
- Run it through `run(project, "window_record.py", [...], both=True)` (the one runner, `dry_stub.run_script` -> `harness.run_script`, with the default cap).
- Record the result: exit 0, or exit 1 with `work/windows/<dispatch>.json` present -> `wrote` lists the window path, and on exit 1 a `live_only` row carries the tool's text (cut 400) and "the tool left work/windows/<dispatch>.json". Any other exit, or no file -> a `live_only` row, and nothing in `wrote`.
- It runs even when no probe ran (no instance, no command, no selector, probe refused). The record then carries the tool's own gaps.
- Test rows:
  - `N2h-v: window_record runs after the probes with --review-receipt; work/windows/<dispatch>.json exists before the form` (fake run that writes the file; check `wrote` and the order)
  - `N2h-v: window_record exit 1 -> the file it wrote stays, live_only names exit 1`
  - `N2h-v: window_record exit 2 / no file -> live_only, nothing in wrote`
  - `N2h-v: window_record timeout -> live_only, nothing in wrote`
  - `N2h-v: no instance -> no probe, window_record still runs`
  - one real-process row as N2h-a did (`:1492`): `N2h-v: through the process window_record.py ran on the world and its answer is a row` (either outcome legal: the row carries exit and text)

**V3. The final message is the role's digest from story data.**
- Add `qa-code-critic@S5.result_text` to `story.json`:
  `"qa-code-critic S5 TC-1 · ok\nTC-1 · approved · the probe breaks the total check and the test goes red\nwork/handoffs/S5-qa-code-critic-1.yaml"`.
  The header verdict and the row state are the role's judgment as story data. The stub never derives them from the probe record (AR-29, FR-58).
- No code change for V3: `dry_stub.py:937` already returns `result_text`.
- Test row: `N2h-v: the story's qa-code-critic@S5 digest passes the product's digest check for scope [TC-1]`. It runs `role_digest.check(text, ["TC-1"]) == []` on the kit row, so a malformed story row is red here and not 70 s into the main pass.

**V4. No `run_suite.py` call by the critic stub** (fork F3 (a)). The critic's card has no `--mine` (A7), and a `--mine` on the automator's bytes writes nothing (A10). Running it would be a road the role is not handed (P31), and it would not fill (c) anyway.
- Test row: covered by V1's call-order row (the expected call list holds no `run_suite.py`).

### 2.2 POSITIONAL - the order inside `fill_role` / `critic_branch`, and the invariant of each position

Order:
1. story `files` (the model file, already at `:900-901`)
2. `probe_by_code.py` per instance (`:509-523`)
3. the story review fragment through `manifest_put.py` (V1)
4. `window_record.py --review-receipt` (V2)
5. `_fill_form` (`:909`)
6. `handoff_check.py --fix` (`:929-935`)
7. the final message `result_text` (`:937`)

Invariants:
- (2 before 3) A verdict is never written before the probe it rests on has run. The probe's records exist (or their absence is a row) when the role's verdict lands.
- (3 before 4) The window record and the immutable review receipt are built from the manifest AS the verdict left it. The receipt is immutable (`window_record.py:1939-1965`): built before the verdict, it would bind "no critic_verdict" for good, and a rebuild would be a collision refusal.
- (4 before 5/6) `--fix` derives `review.receipt_ref` only from a file that exists (`handoff_check.py:169-170`). The form never names a window path that was not written, and the stub never types it (AR-13: the deriver is the one reader).
- (7 last) The digest is the role's word, never computed from what the tools printed.
- The early `return out` paths of `critic_branch` (`:502-503`, `:505-508`) must no longer skip steps 3-4. Invariant: a missing probe never hides the window record. The tool judges the gap, and the stub never skips a tool to keep a gap out of sight (AR-28).

### 2.3 Edges (each with its behaviour and the invariant it protects)

- (E1) No instance in the window: no probe (as today). V1 and V2 still run, and `window_record` reports its own gap (e.g. empty scope). Invariant: an empty window is never a pass, and the gap is the tool's line.
- (E2) The probe test fails or passes: both are legal. The verdict is data of `work/probes/<IID>.json`. The story's `approved` stays story data. A contradiction between the record and the role's word is for a gate or a person to raise; the stub never reconciles it. Invariant: code never decides the role's verdict.
- (E3) `run_suite` refuses: not applicable, because the critic stub calls no `run_suite` (V4). The automator's `--mine` refusal stays the automator's `live_only` row as today (`:586-587`).
- (E4) `window_record` refuses (exit 2, `EXIT_BAD_ARGS`; or a `ValueError`/`OSError` row; or exit 1 with no file): a `live_only` row with the text cut at 400 and nothing in `wrote`. The form's `receipt_ref` stays blank and the gate names it. Invariant: a refusal never becomes a filled field.
- (E5) `window_record` exit 1 (window not acceptable): the file exists. It goes into `wrote`, a `live_only` row names exit 1, and `--fix` derives the path. Invariant: "written but not acceptable" is never reported as "acceptable".
- (E6) Timeout (`run_script` returns -9): the same branch as E4. Invariant: a killed process never counts as having written its file, even if a partial file exists. Check `code == -9` first and never put a file in `wrote` on -9.
- (E7) The fragment is malformed in the story (not a list of non-empty objects): `KitError` naming `qa-code-critic@S5.manifest_fragments`, the same text as `:540-541`, and the call exits 3 loudly (`:964-968`). Invariant: wrong story data is never an empty product.
- (E8) `manifest_put` refuses the critic fragment: a `live_only` row; `window_record` still runs and reports "no critic_verdict" (`window_record.py:155`). Invariant: the stub never retries with other keys.
- (E9) A second fill of the same dispatch (`repair_on_round`): `window_record --review-receipt` runs again. A receipt collision is the tool's refusal (exit 1/2) and becomes a `live_only` row. The stub never deletes a receipt or a window file. Invariant: an immutable record is never rewritten by the stub.
- (E10) (c) stays unfilled after V1-V3: expected by reading (A11). The pass stops at S5 with ONE finding, `probes.runtime_provenance`. The builder reports the verbatim `dry-1/main/stop` line and labels nothing. Invariant: a product gap is never masked by the stub (AR-28).
- (E11) TEMPORAL, the label after the fix: FV3-20 (stub gap) is wrong once V1-V3 land. On the N2h-v branch, after its CI, the coordinator sends a label step (the card of §1.5 with the id the Lead issues for the new reason; class `product gap` if E10 holds). If the pass goes further, the step names the new stage. If the pass is green to S9, the row is deleted and the pin goes to 0. The wave N2h-v = code + label. Invariant: `main` never holds a stale label (finish spec `:427`).
- (E12) Time (the conflicting pair with F-P18): about 2 added processes (manifest_put, window_record) in the S5 critic call. Estimated +5…20 s (estimate, not verified); measured is S5 = 68.2 s and the pass = 266.6 s. If `dry-1/main/time` exceeds 800 s on the branch's CI, or the 900 s kill hits, there is no merge: stop, and ask the Lead under F-P18. Invariant: no pass that hits the ceiling reaches `main`.
- (E13) The pass stops LATER (S5 automator rework, S6...): the builder reports the verbatim `main/stop`, `main/known_red` and `main/time` lines. The Lead issues the next id. The builder never labels by itself.

### 2.4 Card N2h-v (header-ready)

given:
- this spec §0, §2
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\dry_stub.py` (`run_script` :197-205, `_record` :455-463, `world_command` :466-477, `critic_branch` :483-524, `automator_branch` :527-588, `fill_role` :865-937, `selftest_n2` around :1410-1500)
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\stories\dry-1\story.json`
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\window_record.py:1-57,2161-2283`
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\handoff_check.py:158-177,522-586,1630-1677`
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\role_digest.py:1-29,183-283,368-386`
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\agents\qa-code-critic.md:64-84`
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\brief_pack.py:238-258`
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\references\artifact-contract-automation.md:1-35,131-136`
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\handoffs\s5-critic-to-automator.yaml`
- `C:\QAFactory\forge-repo\docs\tasks\specs\reviews\t-1029-p1b-step11-code.md` (F6-F9, open points b/c)
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\design\factory-rules.md`
- `C:\QAFactory\forge-repo\plans\builder-rules.md`
- `C:\QAFactory\forge-repo\docs\TESTING.md`
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\dry_stub.py (critic_branch, automator_branch's fragment loop -> merge_story_fragments, selftest rows `N2h-v:`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\stories\dry-1\story.json (only the `qa-code-critic@S5` row: `result_text`, `manifest_fragments`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\p1b-n2h-v-critic-window.md (new)
C:\QAFactory\forge-repo\docs\tasks\specs\reports\20261117-p1b-n2h-v-report.md (new)
non-goals:
- any package script outside `scripts/tests/` (`window_record.py`, `handoff_check.py`, `run_suite.py`, `probe_by_code.py`, the contract): a product defect found on the way is a report line with its class, never a stub workaround
- `known_red.json` (the label step, edge E11)
- `slow_tests.json`
- `dry_world.py`, `dry_exits.py`, `dry_driver.py` (N4:gates owns the last two)
- the window filter of critic t-1029 open point (b) (residual to N4:s5)
- a `run_suite` call by the critic (V4)
handoff: builder report `C:\QAFactory\forge-repo\docs\tasks\specs\reports\20261117-p1b-n2h-v-report.md`: the FR pass by section, the witness verbatim, and the CI lines `dry-1/main/stop`, `dry-1/main/known_red`, `dry-1/main/time` verbatim (the coordinator runs the door and pastes them)
edges: §2.3 E1-E13; POSITIONAL §2.2
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/tests/dry_stub.py ai-packages/qa-factory/scripts/tests/fixtures/stories/dry-1` (the slow `test_scenario_dry_1.py` it names is judged by the coordinator's door: `python -B tools/ci_read.py start --ref <branch> --var dry_only=true`); `python -B ai-packages/qa-factory/scripts/tests/dry_stub.py --selftest` green with the new `N2h-v:` rows of §2.1 and every existing row still green; `python -B ai-packages/qa-factory/scripts/tests/dry_exits.py --check` prints `0 discrepancies` (the label is unchanged in this node, so a "stale" here means the label step is owed: report it, do not edit)
siblings: axis 5 (twin: the automator and the critic merge story fragments through one function and run tools as processes); axis 34 (one road: one runner `run_script`, one fragment road; no `run_suite` road for the critic); axis 30 n/a (no profile command added); axis 18 n/a in this node (the label step carries it)
designer: this file

### 2.5 AR-n, owners, census (for the package commit)

- AR-29 - every value in the window record, the receipt and the probe record is written by the real tool. The verdict and the digest are story data (judgment: the role's, accepted by the Lead at acceptance).
- AR-13 - `receipt_ref`/`runtime_provenance` are filled only by `handoff_check`'s derivers. The stub types neither.
- AR-14 - the manifest is written only by `manifest_put.py`.
- AR-22 - `work/windows/<dispatch>.json` gets its producer on the critic's road (window_record).
- AR-28 - E4, E6, E10: a refusal or an unknown never becomes a pass.
- AR-15/P31 - one fragment function for both branches, and one runner.
- AR-19 - the stage twins (automator/critic) change together.
- Checks added: only selftest rows (test layer, `docs/TESTING.md` table rows). Owner: data (code). No product check is added or altered, so no census row: the census class is "none - test layer only".
- Commit lines: the `architecture:` and `judgment:` lines take the form `tools/architecture_gate.py` carries (read the form there). A `judgment: none` line always carries its ` -- <why>` (here: "test layer only; the role's word stays story data").

## 3. One node or two, and order

**Two nodes** (recommended, fork F6):
- N2h-b2 (the label, §1) owns docs, pile files and one ledger row. Its gates are `piles.py` and `dry_exits --check`. No critic is needed (data/doc). It can merge now and makes `main` honest again (A2).
- N2h-v (§2) is code. It needs the branch's CI and the critic of the topic. After its CI, its own label step follows (E11).

One node would put a doc+ledger edit behind a code critic and a CI run, and the label would be written twice inside one node with an id the Lead must issue mid-node.

**Order:**
- N2h-b2 ∥ N4:gates. No shared file: N4:gates owns `dry_exits.py`, `dry_driver.py` and `driver-exits/{gates.json, known_red/gates.json}`, and its non-goals exclude the shared `known_red.json`, finish spec `:440-442`.
- N2h-v ∥ N4:gates. No shared file: N2h-v owns `dry_stub.py` and `story.json`.
- If N4:gates changes how `dry_exits` reads ledgers, N2h-v merges `main` before its CI (PROJECT.md «Командная работа» п. 3).
- N4:s5 and N4:s6-s9 wait for the N2h-v wave (F-P7 spirit: their rows start after S5 and print `after:<label>`; fork F5).

## 4. Forks (returned, not decided)

- **F1 - where the FV3-20 row goes.** Batch 3 is taken (A13).
  - (a) Rule text, TEAMWORK §2 / D-0044: the row goes into untaken batch 2 with a batch-2 id the Lead issues (FV2-93). No door. Cost: the id differs from the issued FV3-20, and the node of this theme sits in a batch nobody has taken.
  - (b) A row in batch 3 «Узлы» as FV3-20, with `piles-skip: в -- <reason>` in the commit message. This is the gate's own named door (FR-4: informed, not silent). Cost: it deviates from the rule text; it needs the Lead's word in the commit line; the card's «Строки» cell stays `FV3-1…FV3-19`.
  - (c) A row in batch 3 «Остатки». Legal for (в) and (е) (`piles.py:64-66,1658`), but Остатки carries leftovers, not new nodes.
  - **Recommendation: (b).** The Lead of the taken batch issued the id for the batch's own theme, and the door is the informed pass the gate provides. The card is executable on (a) by swapping the file and the id.
- **F2 - when the product finding for (c) opens.**
  - (a) After N2h-v's CI shows (c) alone at S5. PROJECT.md п. 6а: measure the premise first; it costs one CI run.
  - (b) Now, on the reading evidence A8-A11, with a second id.
  - **Recommendation: (a).** The FV3-20 finding names (c) as a candidate, so nothing is hidden meanwhile.
- **F3 - should the critic stub run `run_suite.py --mine`?**
  - (a) No: it is not on the critic's card (A7), and over the automator's bytes it writes nothing (A10).
  - (b) Yes, with `--again`. `--again` repeats no result (`run_suite.py:32-33`), so it is a road the role is not given.
  - **Recommendation: (a)** (P31, AR-28).
- **F4 - should the critic's `critic_verdict` fragment be in this node?**
  - (a) Yes, through the shared fragment road. It is the role's documented step before `window_record` (`agents/qa-code-critic.md:69`), and without it the immutable receipt binds "no critic_verdict" (§2.2).
  - (b) No: wait for the next stop.
  - **Recommendation: (a).**
- **F5 - should N4:s5 and N4:s6-s9 wait for the N2h-v wave?**
  - (a) Yes. The finish spec ordered the groups after the N2h wave (F-P7), and N2h is not done until the critic passes S5.
  - (b) No. They start now; their rows print `after:FV3-20` and re-run later.
  - **Recommendation: (a).**
- **F6 - one node or two:** two (§3). Recommendation: two.
- **F7 - is FV3-20 its own node, or the continuation of FV3-5?** The FV3-5 finding names "`probes.runtime_provenance` is filled after the probe" as its own test row (`findings/…-ne-zapuskaet-probu.md:31`), so FV3-5 is not met either. The Lead already chose a new id by F10, so this is listed only so that FV3-5's status is not set to «принято» on a test row its node did not meet. Recommendation: FV3-5 is accepted with that row carried to FV3-20 (a line in Ход).

## 5. Small choices closed by the designer

- The finding's slug: `20261117-p1b-s5-kritik-ne-pishet-okno-i-daidzhest.md`.
- The digest path line is the form (`work/handoffs/S5-qa-code-critic-1.yaml`), as the S2/S3 critic story rows do (`story.json:9-10`).
- The digest header label is `TC-1` (the case under review, the contract's `window: <the case ids under review>`, `s5-critic-to-automator.yaml:34`).
- `window_record` runs with the runner's default cap (300 s), not a new constant (critic t-1029 F9: no pin on a constant).
- The function name `merge_story_fragments` (any name; one function).

## 6. Readers of every touched file (rule 7)

Grep `known_red\.json|dry_stub|stories/dry-1|batch-3-live-run-fvf|live-run-fvf`:
- `tools/`: 2 hits, both in `tools/test_workflows.py` (`:348` runs `dry_stub.py --selftest` in the tables job; `:352` the profile's pytest note). Unchanged by both nodes: the command line stays.
- `.githooks/`: 0 hits (a positive control on the same tool and path finds `piles` at `.githooks/commit-msg:38-40`). The commit-msg hook runs `tools/piles.py check`, which reads the batch, card and findings files. It changes in no stream; it is the gate of N2h-b2 (edge 4).
- `.claude/agents`, `.claude/skills`: 0 hits (a positive control on the same pattern over `.claude/` finds worktree copies, so the pattern works).
- `tools/piles.py` (reads the batch file, the card and `findings/`; check (в), (е)): unchanged; N2h-b2 obeys it.
- `tools/test_pile_cards_contents.py` (reads the card's «Содержание»; `docs/TEAMWORK.md:12`): unchanged; N2h-b2 adds its row.
- Package readers of `known_red.json`: `known_red.py` (`load`), `dry_world.py` (main pass and `walk_exits`, finish spec `:379`), `dry_exits.py` (`check`, `judge_group`), `test_scenario_dry_1.py`. All unchanged and read as data.
- Package readers of `dry_stub.py`: the dry world installs it as the stub `claude`; `test_scenario_dry_1.py`; `tools/test_workflows.py:348`. Unchanged.
- Package readers of `story.json`: `dry_stub.load_kit`/`stub_control`, `dry_world`. Unchanged; the new keys `result_text` and `manifest_fragments` are already read keys.

## 7. Not read this round (claims resting on them are marked)

- `docs/tasks/specs/reports/20261117-p1b-n2h-report.md`: not read. The N2h-a code was read directly in `main` instead.
- `form_filler.py` (how the critic form's `header.verdict` and `review.outcome` are filled): not read. If the filled form's verdict word disagrees with the digest's `ok`/`approved`, that is a FR-10 contradiction; the builder reads the filled form in the world and reports it.
- `manifest_put.py` merge keys for a critic fragment: not read (V1 shape measured by its answer).
- `test_pile_cards_contents.py`, `piles.py` (е) row grammar of «Остатки»: not read beyond the cited lines.
- The `FV3-5` grep over the whole repo stopped at its time limit. It found `known_red.json` and the docs, and no test fixture pinning `after:FV3-5`; this is not a complete negative.
- The whole-repo run of A10 is not measured (a `--mine` by the critic answering `reused` is read from code). F2 (a) measures A11 by CI.

## Lead decisions on the forks (17.11.2026, Fable; по рекомендации, до слова владельца — the owner is away)

- F1 (b): the FV3-20 row goes into batch 3 «Узлы» with the door `piles-skip: в -- Lead of the taken batch (17.11.2026): FV3-20 is the batch's own theme, a new stop reason of main/S5 (finish spec F10)` in the commit message.
- F2 (a): the product finding for `probes.runtime_provenance` opens after N2h-v's CI shows it alone at S5.
- F3 (a): the critic stub runs no `run_suite`. F4 (a): the `critic_verdict` fragment is in N2h-v.
- F5 (a): N4:s5 and N4:s6-s9 wait for the N2h-v wave. F6: two nodes. F7: FV3-5's test row "runtime_provenance is filled" is carried to FV3-20 (a «Ход» line).
- Spot-read by the Lead: `known_red.py:18` (NODE_RE), `dry_stub.py:936-937` (default digest), `run_suite.py:470-473` (no run block for `red_probe`).

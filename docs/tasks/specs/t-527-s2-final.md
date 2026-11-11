# t-527 — релиз 0.10.8, поток S2 «грунтовка»: итоговый текст узлов (G2-1, G1-5, G2-12, G2-10, G2-2, G2-3, G2-5, G2-14)

Дизайнер (Opus 5.5), 31.10.2026, дерево `release/0.10.8`. ЧЕРНОВИК на приёмку Lead. Заменяет t-504 и t-512 для билдера: узел исполним по своему блоку и коду. История и обоснования — t-504, t-512, t-521, сюда не повторены. Кода нет, тесты не запускались.

Сокращения кода: GT `grounding_table`, PC `planning_contract`, HC `handoff_check`, C `contract`, CP `claim_projector`, QR `question_register`, BS `base_slice`, CT `controller`. Пути без префикса — от `ai-packages/qa-factory/scripts/`. Номера строк — этого дерева, сверять по имени функции.

Решения, на которых стоит текст: развилки как принял критик (F-1, F-3, F-4, F-6′, F-8, F-11, F-13 + M-1, F-14); F-2, F-5 — по условиям критика; F-10, F-15 — по M-4 с уточнением F-16 (§7, **вопрос Lead**); B-4 — t-1046 F-1B и t-1015 §L-3 M-2, §L-4 стоят. В1–В4 ушли владельцу, узлы исполняются по рекомендации критика (В1: оффер MR не здесь; В2: `drift` и пара «тяжесть × вероятность» не здесь; В3: (а); В4: да).

## 1. AR-n и общие правила

| Узел | AR-n (проверка — в DoD узла) |
|---|---|
| G2-1 | AR-1, 7, 14, 18, 28 |
| G1-5 | AR-9, 10, 12, 13, 18, 22, 28 |
| G2-12 | AR-10, 11, 13, 22, 26, 28 |
| G2-10 | AR-9, 10, 12, 13, 15, 28 |
| G2-2 | AR-12, 13, 16, 17, 19, 20, 24, 25, 26, 28 |
| G2-3 | AR-11, 13, 22, 26, 27, 28 |
| G2-5 | AR-16, 22, 27 (AR-10 неприменимо: строки только человеку) |
| G2-14 | AR-1, 2, 7, 8, 11, 14, 18, 22 |

Каждому узлу: `given` несёт `factory-rules.md` и `builder-rules.md` целиком (PROJECT п. 1). Свидетель — только свой тестовый файл и ключи DoD (D-0056); мутации не гоняются, называется убивающий файл; большие файлы и соседи — BATCH CANON интегратора. Отчёт — файл по `handoff:`, в чате ≤ 25 строк; в нём проход FR по разделам (неприменимое — строкой). Коммит пакета несёт строку `architecture: AR-n -- <как сохранено>`. Фрагмент changelog — `changelog.d/<имя>.md`. Текст в пакете — английский (FR-30). Тесты запускаются из корня worktree билдера; тест, которому нужен cwd пакета, называется в отчёте и уходит в канон. Абсолютные пути `owns`/`handoff` даны от этого дерева; Lead при запуске подставляет worktree билдера.

## 2. Порядок и очереди (заменяет t-504 §1, t-500 :84-89, :162, :169 по S2; строку t-507 :184)

| № | Узел | Ждёт | Параллельно с |
|---|---|---|---|
| 1 | G2-1 | — | G2-12, G2-10 |
| 2 | G2-12 | G2-11 слит | G2-1 (G2-10 — после него только по `check_register`) |
| 3 | G2-10 | G2-12 (функция `check_register`); иначе независим (F-8) | G2-1 |
| 4 | G1-5 | G2-1 | G2-12, G2-10 |
| — | GW1-29, затем GW1-41 + G2-15 (S1) | G1-5 (`_detector_body`), G2-10 (`check_register`) | — |
| 5 | G2-2 | G1-5, G2-1; GW1-41 (`s3_strategist_lines`) | G2-3 |
| 6 | G2-3 | G1-5, G2-15 (`candidate_defects`, `candidates_without_row`) | G2-2 |
| 7 | G2-5 | G2-2, G2-3 | — |
| 8 | G2-14 | G2-12, G2-15 | — |

Циклов нет: G2-1 → G1-5 → GW1-29 → GW1-41+G2-15 → {G2-2, G2-3} → G2-5.

| Файл | Функции потока | Другие потоки | Порядок |
|---|---|---|---|
| `controller.py` | `Controller.validate` (одна строка вызова у :5261), `+_s3_completion_gate` | GW1-40 (не подтв.) | G1-5 → GW1-40. G2-2 файл НЕ трогает (`Controller._grounding_stop` снят) |
| `story_run.py` | G2-2: `s3_between_windows`, `+grounding_stop` с двумя помощниками, `s3_check_packet`, `s3_window_completion`, `s3_ticket_completion`, `s3_strategist_lines` | GW1-41 (`s3_strategist_lines`), GW1-33, S5 (метод RD1-20) | **GW1-41 → G2-2 только по `s3_strategist_lines`**; остальные функции параллельно (D-0048) |
| `planning_contract.py` | G1-5: `_detector_body` (строка), `+regression_from_blast`. G2-3: `+row_tests_it`. G2-10: `_rerender_plan_cells`, функция :910-924 | GW1-29, GW1-41, G2-15, RG1-1 | `_detector_body`: **G1-5 → GW1-29 → GW1-41+G2-15 → RG1-1** (исправляет t-504 :38). G2-3 после G2-15 |
| `handoff_check.py` | только `CLAIMS`, `DERIVERS`, `+_claim_grounding_*` (`check` НЕ трогается: M-4 снял вызов слияния) | никто | — |
| `exit_gate.py` | **не в потоке** (`stage_dispatch` :553 уже есть; G1-5 новый читатель диспатча не заводит) | GW1-10 | снято из t-500 S2.02 |
| `handoffs/s3-strategist-to-designer.yaml` | G1-5: ключи, claims, `not_planned.ref` | GW1-41 (:61 те же claims) | **G1-5 → GW1-41**; GW1-41 берёт форму `ref: <R-n, K-n or B-n>` (t-574 F-10: `|` в короткой подсказке `handoff.py` читает как закрытый список; заменяет t-502-s1b:61) |
| `agents/qa-test-strategist.md` | G2-2, G2-3 | GW1-29, GW1-41, RG1-1 | **GW1-29 → GW1-41 → G2-2 → G2-3 → RG1-1**; потолок устава — у каждого |
| `phases/s3.md` | G2-3 | GW1-41 | GW1-41 → G2-3 |
| `references/block-names.json`, `question-prices.json` | G2-2 | S5 (`by hand`, строки других ключей) | нет |
| `contract.py` | G2-12 `+unconfirmed_requirements`; G2-10 `md_table`; G2-2 `+grounding_row_question` | G2-15 `+candidate_defects`, RD1-13 `+triage_reason`, EP1-38 | параллельно по функциям (t-502-s1b:264 снимает G2-12 → G2-15); не дописывать в конец файла |
| `grammar.py` | G2-12 `DERIVED_FROM_RE`; G2-10 `+split_cells`, `+escape_cell` | — | параллельно |
| `validate_artifacts.py (check_register)` | G2-12 (текст :495), G2-10 (счёт клеток) | G2-15 (форма S2 для `bug:`, m-4) | **G2-12 → G2-10 → G2-15**: одна функция |
| `check_delivery.py` | G2-3 `+bug_candidate_record`, `+grounding_records`, `assess` (строка у :1966); G2-5 `grounding_records` | RD1-19 `_assert_stricter_how` | **G2-3 → G2-5**; с RD1-19 параллельно по функциям. Прежняя цепочка «RD1-19 → G2-3 → G2-5 → RD1-9» снята: t-507 :46, :60 — оба узла файл не трогают. RD1-21 трогает только при своей F-3: тогда после G2-5 |
| `report_facts.py` | **только G2-5**: `+_r_grounding`, `render` (:2058, одна строка). G2-3 файл не трогает | S5: `_manual_vs_table`, `_r_manual_checks`, `_test_lines`, `_regression`, сегмент :2031; RD1-20 строка итогов; EP1-37 `_unknown_line`; S1 `_r_gate_a` | **параллельно по функциям**; при конфликте в `render` G2-5 сливает `main` и решает сам. `_regression`, `_r_regression` узел не трогает. Заменяет «S5 → G2-3 → G2-5» в t-507 :184 и t-500 :169 |
| `references/delivery-reason-owners.json` | G2-5: семья `grounding:` | RD1-21 (`coverage:`) | RD1-21 → G2-5, разные строки |
| `gate_brief.py` | G2-5: `collect`, `render`, `+_grounding_lines` | GW1-11, GW1-32, GW1-39 | GW1-11 → GW1-32 → G2-5 |
| `brief_pack.py` | G2-14 `+user_path_failure_lines`, `build` | RG1-3, G2-15 | RG1-3 → G2-15 → G2-14 |
| `grounding_table.py` | G2-1 → G1-5 → G2-2 | никто | последовательно |
| `claim_projector.py` | G2-10 (чтение :422, :425); G2-2 `+project_row_questions` | никто | параллельно по функциям |
| `references/conductor-actions.json` | G2-3 (строка :8) | C5 (не подтв.) | при конфликте сливает поздний |

---

## 3. G2-1 — мера рефакторинга

**Что менять** — `grounding_table.py`:
- `+share(data, policy, findings) -> dict`: чистая, не пишет; находки подаёт вызывающий (`check` снаружи). Результат: `measure, refactoring, unclassified, total, percent, road, policy, mixed_hunks, reason`.
- `T` = сумма `added+removed` ханков `hunks[].kind == "production"` (вид решает код, `TF.file_kind`). `W`: ханк в W, когда ВСЕ метки строк `rows[]`, где он стоит, — из `numerator_labels` политики (`implements` + `refactoring` = не W). `unclassified` — в числителе, если так говорит политика. `mixed_hunks` — ханки с меткой из числителя и другой меткой.
- `road`: `100*W > stop*T` → `stop`; иначе `100*W > notify*T` → `notify`; иначе `none`. Пороги — `PC.grounding_policy` (`grounding-policy.json`). `percent` — только показ (строка), никогда не сравнивается.
- `main`: `--share --task T` в одной `mutually_exclusive`-группе с `--skeleton/--refresh/--check`; пишет ключ `refactoring_share` через `write_key` (:180).

given: `ai-packages/qa-factory/design/factory-rules.md`, `plans/builder-rules.md`, `scripts/grounding_table.py` (:45-60, :180-205, :852-914, :1138-1190, :1266-), `references/grounding-policy.json`, `scripts/planning_contract.py (grounding_policy, read_grounding)`, `scripts/test_files.py (file_kind)`, этот блок.
owns:
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\grounding_table.py (+share, main)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\tests\test_grounding_share.py (новый)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\changelog.d\g2-1-refactoring-share.md (новый)
non-goals: покрытие требований и дайджесты (G2-2); пересчёт на выходе (G2-2); правка порогов и `grounding-policy.json`; вопрос человеку; вес чистого переименования (F-3: 0 строк, файл называется); `dropped` из G1-4.
handoff: C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\docs\tasks\handoffs\g2-1-refactoring-share.md
edges: T=100: W=30 none, 31 notify, 50 notify, 51 stop («больше» строго, инвариант: float недостижим). T=0 или пустой дифф → `percent: "n/a"`, `road: none`, `reason` (неизвестное не «0 %», FR-41). Не diff/нет MR → ключ не пишется, файл таблицы не меняется (шага нет). Политика нечитаема → `road: unknown`, `reason`, выход 0 (не стоп и не none). Находка R0/R1/R5 или пустая метка → `road: unknown`, reason называет правило (мера на чужих байтах не считается). `infrastructure` на production-файле — в T, не в W (метка роли не меняет знаменатель). `generated`/`config` — вне T, отчёт называет файлы. Псевдо-ханк — 0 строк, файл в отчёте. Чистый перенос с `refactoring` — считается. Смешанный ханк одной строкой — 0 %. Строка в `orphans[]` не считается. `TF.file_kind` в роли гейта: ошибка только в production (инвариант: тест не убирает строки из T); неудобные входы `src/app/test_mode.py`, `tests_root` на смешанной папке, `.json` под docs — пины. CLI: пустой `--task`, нет истории, длинный, кириллица — как `--check` (`hooklib.story_root`); нет таблицы в мире diff → `unknown` без записи, выход 0; битый YAML → R0, ключ не пишется; `--share` с `--check` → отказ argparse. Инвариант: мера не пишется на таблице, которую нельзя прочитать.
DoD: `python -B ai-packages/qa-factory/scripts/tests/test_grounding_share.py` — все края выше, ровно 30,0 и 50,0 и +1 строка ЗА. Мутации → `test_grounding_share.py`: `>` на `>=`; `all` на `any`; float; T с тестами; unknown как stop. AR-1: grep `30`, `50` и имён меток в новом коде пуст с контролем. AR-7: сказать, что решает роль (группы, подпись); `stage_compare.py` неприменим. AR-14: только `write_key`, `test_artifact_writers.py` — канон. AR-18: `--share` не детектор, `REJECT` не печатает (строка отчёта). AR-28: нет/нечитаемо/пусто → `unknown`.

---

## 4. G1-5 — ворота S3 (остаток)

**Что менять.**

1. `grounding_table.py`: `+exit_findings(root, plan_rows, not_planned) -> list[Finding]` (F-14, дом — GT; явная отмена t-1015 §L F-1 (a); `claim_projector` импортировать лениво: CP импортирует GT на верху, `claim_projector.py:41`). Ничего не пишет (FR-45). Состав:
   - `source_state == "diff"` и нет файла → Finding `R0`, `who="conductor"`, текст: `work/grounding.yaml is missing while implementation_source is diff: this S3 was planned without a grounding table (begun before this check, or the table is gone). Expected: the table the S3 preparation writes before window 1. Way on: a person's word (waiver.py --task <T> --stage S3 --block "<this line>") or release of the dispatch; the driver then prepares the table and runs window 1.` Дальше ничего не считается. Отдельного признака `old` ворота не читают.
   - вне diff: файла нет → `[]` (F-8A, строку даёт `null_outcome`); файл с `hunks/rows/requirements/blast_radius` → G-0b, `who="conductor"` (t-1015:83).
   - `check(root)`.
   - `s3_claim_errors(root)` как findings, с дедупом: при нечитаемой таблице одна находка R0, не две.
   - **R7** (diff, план есть): каждый `rows[].risks[].id` (K-n) и каждая область `matters: yes` (B-n) названы `PC.grounding_refs(row)` какой-либо строки плана или `not_planned[].ref`. Форма `ref: K-n | B-n` без префикса. Записи роли достаточно, человек решает на гейте A (t-1015 §L F-7 (a)): «с решением человека» снято. Висящая ссылка плана (`grounding:K-9` без K-9) — R7. `add_tests: TS-n` без строки плана — R7. Текст — t-1015:91. `who="role"`.
   - **R7-регрессия (F-16):** область с `matters: yes`, у которой `regression` не `gap:`, названа в разделе `## Recommended regression` токеном `blast:B-n` (`delivery_verdict.regression_lines`); `who="role"`, текст называет B-n, файл и ожидаемую команду. Раздел нет или `No regression:` при такой области → та же находка.
2. `planning_contract.py`: `+regression_from_blast(doc) -> list[{area, command | gap, why}]`, чистая, по номеру B-n числом (`B-10` после `B-2`), одинаковые команды склеиваются. Форма — t-1015 §3.5 без записи в форму. Единственный код, выводящий регрессию из областей: её зовут R7 и строки стратега (G2-2). `regression_recommendations` формы НЕ выводятся, `HC.check` не трогается (заменяет t-1015 §3.5, §L-2 M-6, §L-3 M-4).
3. `controller.py`: `+Controller._s3_completion_gate(d, p, state)`; в `validate` у :5261 одна строка `if d["stage"] == "S3": self._s3_completion_gate(d, p, state)`, тело текущей ветки :5261-5279 переезжает внутрь (образец положения — :5283, :5285). Порядок внутри (инвариант: отказ `_plan_document` не опережает отказ по маркеру):
   a. `s3_window_of(d) == "labelling"` и `bool(p.get("stage_complete"))` → `StateConflict`: `a window-1 (labelling) dispatch of S3 cannot close the stage; it is accepted with --not-complete --unresolved plan_pending`. Словом человека не проходит: дверь — водитель (`finish --not-complete`).
   b. `labelling` без `stage_complete` → находки `GT.check` с `who == "role"`, через `_passed_by_person("S3", …)`.
   c. истинный `stage_complete` → `validate_plan` + `GT.exit_findings`, один список в одном `_passed_by_person("S3", …)`, запись `_record_person_pass`. Есть ошибки плана → голова прежняя `S3 structured test plan invalid: ` (+`; S3 grounding: …`). Только граундинг → `S3 grounding: ` + `"; ".join(blocking)`. Без находок граундинга текст и порядок байт в байт прежние.
   d. `exit_findings` бросил → `StateConflict("S3 grounding: the check could not run (<Exc>: <msg>) ... Way on: the conductor")`, не проход.
4. `planning_contract._detector_body`: одна строка — только `who == "role"` из `exit_findings`, в список отказа и счёт `S3 exit:`, импорт GT ленивый. Находки driver/conductor идут только в п. 3 (инвариант: находка не роли не закрывает стадию и не возвращается роли как её работа).
5. `handoff_check.py`: `CLAIMS` + пять утверждений с именами t-1015:107-111, верификатор `(art) -> (bool|None, text)` зовёт правило `GT.exit_findings`/`GT.share` (импорт GT ленивый: GT импортирует HC на верху), своей логики нет. `refactoring_share_computed_by_code`: ключ есть и равен `GT.share` над текущими байтами; ключа нет → `None`.
6. `handoffs/s3-strategist-to-designer.yaml`: `inputs` + `work/grounding.yaml` (required при diff); ключи `grounding`, `blast_radius` заполняет КОД (`DERIVERS`), роль их не пишет; `grounding` без `decision`, вместо него `word` (ответ из `stage_override_values`, пусто — нет слова); `not_planned` — `ref`, `state`, `reason` вместо `requirement` (:71); пять claims. Условно `references/null-outcomes.json`, если `test_null_outcomes.py` поднимет счёт.
7. `references/gate-registry.json`: строка `s3_grounding` текстом t-1015:114-122 с заменами: сайт `grounding_table.py:exit_findings`, плюс каждая функция, сравнивающая слова поля (первым ходом: `python -B ai-packages/qa-factory/scripts/gate_registry.py --check` назовёт несвязанные сравнения), `words` — реальные состояния, `test` = `scripts/tests/test_grounding_table.py`. `design/controller-blocks.md` перегенерировать.
8. Фикстуры (t-1015 §L-3 B-1): первым ходом перепись S3-приёмок при `implementation_source: "diff"` без диффа (`test_story_run_s7_live.py:71`, `:83`; `test_story_step.py:74`, `:1022`; `story_run_common.py:134`) — список в отчёт. Выбрано: хелпер `story_run_common.py` кладёт файл таблицы формы diff из существующей фикстуры `test_grounding_table.py`; тест, которому дифф не нужен, снимает `implementation_source` (мир `off_diff:absent`).
9. Мутация M9 (t-1018 §5): форма S2 снова с `diff_accounting` при ключе `grounding` в S3 → убивает `test_handoff.py`, тест T-b `the_s2_field_and_the_s3_gate_never_live_together`. Назвать в отчёте.

**R6 здесь нет** — G2-2 (F-1). `Controller.grounding_stop` нет. `exit_gate.py` не трогается: окно 1 и хук уже держат `_window_one_errors`, `_finish_gate`; прежнее `running_dispatch` D-1 снято, новых читателей диспатча нет.

given: `design/factory-rules.md`, `plans/builder-rules.md`, `docs/tasks/specs/t-1015-g1-5-s3-gate.md` (:83, :91, :99-101, :107-122 — только тексты), `scripts/controller.py` (:61, :2078, :4498, :5222, :5261-5285), `scripts/grounding_table.py` (:742-760, :1138-1190), `scripts/claim_projector.py (s3_claim_errors)`, `scripts/planning_contract.py` (:372, :625, :2834-2895), `scripts/handoff_check.py` (:760-), `scripts/traceability.py (not_planned_basis)` — образец чтения `not_planned`, `scripts/delivery_verdict.py (regression_lines)`, `handoffs/s3-strategist-to-designer.yaml`, этот блок.
owns:
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\controller.py (Controller.validate — строка; +_s3_completion_gate)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\design\controller-blocks.md (генерируется)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\grounding_table.py (+exit_findings)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\planning_contract.py (_detector_body — строка; +regression_from_blast)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\handoff_check.py (CLAIMS, DERIVERS, +_claim_grounding_*)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\handoffs\s3-strategist-to-designer.yaml
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\references\gate-registry.json (одна строка)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\references\null-outcomes.json (условно)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\tests\test_grounding_table.py
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\tests\test_controller_state.py
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\tests\test_s3_s4_chain.py
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\tests\test_handoff.py
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\tests\story_run_common.py (хелпер)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\tests\test_story_run_s7_live.py (только фикстура)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\tests\test_story_step.py (только фикстура)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\changelog.d\g1-5-s3-gate.md (новый)
non-goals: R6, вопрос, `--share` на выходе (G2-2); оффер MR (В1); `exit_gate.py`; `story_run.py`, в том числе ветка `old` драйвера (закрывает как раньше и получает отказ ворот); `EG.grounding_errors`; гейт A после `revise_plan` и тип `stage_complete` (строки «Остатков», §8); проверки в `controller.gate-inputs` (стори за S3 не отказываются); `regression_scope.py` (RG1-1).
handoff: C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\docs\tasks\handoffs\g1-5-s3-gate.md
edges: Истинный `stage_complete` — всегда окно выхода: `"true"` строкой на labelling → отказ a; `recover` между окнами S3 не закрывает (пин; инвариант: окно 1 не закрывает ни по `accept`, ни по `recover`). Автодописка `stage_complete` (`:4498`, `_closes_stage`): `finish` без `--not-complete` по labelling → отказ a. Голое `false` без `unresolved` — отказ :5222, как было. Вне diff — 0 из 0 зелёным только там. diff и 0 ханков: R2 требует состояния, стоп — G2-2. Реестр нечитаем: R2 `driver`, в контроллер, не роли. `exit_findings` бросил → отказ (ошибка к отказу, FR-59). Нечитаемый `pipeline.json`: `_passed_by_person` молча отдаёт всё блокирующим — отказ. Длинный список: `DV.named` режет на `limit` с хвостом «and K more»; `_named` отдаёт `where` (`detector_verdict.py:463`); тест: ни одно имя не потеряно без счётчика. Слово человека проходит всё, кроме отказа a (FR-57: у него своя дверь). R7: AT `grounding:K-1`, `blast:B-1`; ЗА `grounding:K-0`, `k-1`, `blast:B-1x`, бэктики снимает `grounding_refs`. K-n в `not_planned` проходит R7, запись даёт G2-3 (инвариант: подозрение не теряется). Плана нет на входе `_detector_body` — как сегодня (окно 1). До RG1-1 раздел регрессии свободной формы: токен `blast:B-n` ищется в любой его строке (инвариант: область не доходит молча; лишний отказ роли лечится одним токеном).
DoD: `python -B ai-packages/qa-factory/scripts/tests/test_grounding_table.py`, `python -B ai-packages/qa-factory/scripts/tests/test_controller_state.py`, `python -B ai-packages/qa-factory/scripts/tests/test_s3_s4_chain.py`, `python -B ai-packages/qa-factory/scripts/tests/test_handoff.py`, `python -B ai-packages/qa-factory/scripts/gate_registry.py --check`, `python -B ai-packages/qa-factory/scripts/refusal_registry.py --check`, `python tools/controller-blocks-gen.py ai-packages/qa-factory/design/controller-blocks.md`. Мутации: вызов из `validate` убран, ветка a убрана, ветка b убрана, `old` снова проходит → `test_controller_state.py`; R7 не читает `not_planned.ref`, висящая ссылка, `add_tests`, `B-10` раньше `B-2` → `test_grounding_table.py`; строка `_detector_body`, находка driver попала роли → `test_s3_s4_chain.py`; утверждение всегда true → `test_handoff.py`. AR-9: отказы в одном коммите со строкой A24 и дверью. AR-10: `risk_source_refs`, `not_planned[].ref`, токен `blast:B-n` названы в форме S3 тем же коммитом, `test_field_producers.py` — канон. AR-13: `s3_claim_errors`, `grounding_refs`, `GT.check` зовутся; grep `split("|")`, `json.loads` в новом коде пуст с контролем. AR-18: форма `REJECT`, `test_detector_verdict.py` — канон. AR-22: ключи и утверждения — производитель и читатель одним коммитом. AR-28: нет/нечитаемо/пусто — тестом, строка реестра с `unknown_branch`. AR-12: `code_friction` стратега или «не измерено» строкой. `test_gate_registry.py`, `test_controller_blocks.py`, `test_story_step.py`, `test_story_run_s7_live.py` — канон. FR: A 1, 2, 4, 57; C 10, 11, 38, 42; D 59; G 45, 54; B, E, F не менялись. `tools/mechanism_gate.py`: блок осей и `tier:` в коммите (ворота — механизм).

---

## 5. G2-12 — код и чужой тест не источник требования

**Что менять.**
- `contract.py`: `+unconfirmed_requirements(text, questions=None) -> set` = `unconfirmed_implementation_only` (:1057) ∪ строки, чей единственный источник — код или чужой тест: `source == derived`, `ac_ref` пуст, матрица молчит, `observable` начинается с `current-code:` или `derived_from` начинается с `test:`; минус подтверждённые (`claim_confirmed` :1039). `implementation_only` (:987) не меняется. Колонки нет, метка вычисляется.
- Гейты-читатели на новую функцию: `validate_artifacts.py:292`, `:1605`, `coverage_contract.py:485`, `:493`, `manual_evidence.py:654`, `traceability.py:953`. Отказ `contract.py:1208-1211` обобщить, дверь та же (`unknown` + вопрос). Пин: `:1605` пропускает строку `oracle_unknown` без `oracle`, которую требует забор G2-15 (инвариант: забор и гейт не запирают роль).
- `grammar.DERIVED_FROM_RE` (:24): + `test`. `bug:candidate-defect` уже проходит, менять ради него не надо. Обёрнутое в бэктики не проходит. Читателя, разбирающего `bug:` как id, нет (§9).
- Текст: `validate_artifacts.py:495` и `references/templates/requirements-register.md:27` называют `test:`, `norm:`, `bug:BUG-NNN`, `bug:candidate-defect`.
- Подтверждение (F-2): `## Behaviour claims`, `before: unknown`, `now_ref: current-code:…`. `claim_row_errors` целиком прочитан (:1068-1102): `now_ref` проверяется только на непустоту, `before: unknown` законен, запрета нет. Правится только текст :1088: `... and the diff line or current-code place it was read from`. Первым ходом `Grep now_ref` по `scripts/*.py`: читатель, требующий `diff:` для строки без `origin: S3-grounding`, → вопрос Lead, не обход.
- Вопрос: один пакет на класс (D-0043).
- `agents/qa-requirements-tester.md`, `skills/qa-story/phases/s2.md`: правило; тест другой стороны — `derived_from: test:<ref>` или строка противоречия, не `source`. Потолок устава 9000 байт: убрать не меньше, чем добавлено.
- Срез `UNCONFIRMED_SOURCE_CUTOFF` по `created`, форма `_oracle_dated`.

given: `design/factory-rules.md`, `plans/builder-rules.md`, `scripts/contract.py` (:946-1102, :1208-1211), `scripts/grammar.py:24`, `scripts/validate_artifacts.py` (:292, :452-514, :1596-1625), `scripts/coverage_contract.py` (:475-495), `scripts/manual_evidence.py:654`, `scripts/traceability.py:953`, находки `plans/piles/grounding/findings/20261030-chuzhoj-test-ne-istochnik-trebovanij.md`, `20261031-trebovanie-iz-tekushchego-koda-stanovitsya-orakulom.md`, этот блок.
owns:
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\contract.py (+unconfirmed_requirements, текст :1088, :1208-1211)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\grammar.py (DERIVED_FROM_RE)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\validate_artifacts.py (только вызовы и текст :495)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\coverage_contract.py (только вызовы)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\manual_evidence.py (только вызов)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\traceability.py (только вызов)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\references\templates\requirements-register.md
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\agents\qa-requirements-tester.md
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\skills\qa-story\phases\s2.md
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\tests\test_oracle_provenance.py
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\changelog.d\g2-12-code-is-no-source.md (новый)
non-goals: `implementation_only`; `candidate_defects` (G2-15); чужая документация как источник (близнец, очередь `gates-and-words`); «R-9, R-13, R-16 ушли в Not planned до ответа» (GW1-41); новое слово оракула `unconfirmed` (строка узла читается как вычисляемая метка и `oracle_unknown: true`).
handoff: C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\docs\tasks\handoffs\g2-12-code-is-no-source.md
edges: Ошибка функции только к «не подтв.» (ложное «подтв.» — тест, который умеет лишь пройти, P20). Остаются «не подтв.»: `CURRENT-CODE:`, `` `current-code:…` `` в бэктиках; `derived` + `ac_ref: -`/`n/a`; ответ `b`; строка изменена после ответа; вопрос `named`; `questions=None`; нечитаемый вопрос. НЕ попадают: `source: ac`/`story`/`discussion` с `current-code:`; `derived` + непустой `ac_ref`; матрица с `contradicts:`; `derived_from: invariant:…`. Реестр пуст/нет → `set()`; нечитаем → вызывающий как сейчас. Все R такие (CART-1: 13 из 16; фикстура — форма, не число) → один пакет, строки с `oracle_unknown: true`; ответа нет → пробел, не pass. «Подтверждаю всё» — на весь класс (FR-7). Сохранённый план до узла → срез, не краснеет (FR-14), старая `ORACLE_CUTOFF` не подходит. Кандидат и «литерала нет»: строка и кейс есть, ожидание открыто.
DoD: `python -B ai-packages/qa-factory/scripts/tests/test_oracle_provenance.py`, ключи всех неудобных входов. Мутации → он же: убрать `current-code:`; `ac_ref` пропускает; `:1605` на старой функции; `questions=None` подтверждает. `test_validators.py`, `test_coverage_contract.py` — канон. AR-26: текст говорит «requirement», перепись t-928 по тронутым файлам. AR-13: grep `unconfirmed_implementation_only` с контролем, остались только названные. AR-22: `test:`, `bug:candidate-defect` в форме, шаблоне, уставе, отказе одним коммитом. AR-28: `questions=None` — тест. AR-11: цифры A22/A25 до и после, `python -B ai-packages/qa-factory/scripts/selftest.py --limits`. AR-10: требование в форме до работы. FR: A 1; C 12, 38; D 41, 58, 59; E 35; G 30; B, F не менялись.

---

## 6. G2-10 — читатели таблиц роли

**Что менять** (F-4: оба).
- `grammar.py`: `+split_cells(line) -> list[str]` — делит по неэкранированной черте, снимает РОВНО одну крайнюю с каждой стороны, разэкранирует. `+escape_cell(value) -> str` — тело `project_decisions._escape` (:141) переезжает с `_LINE_BREAKS`; `_cells` (:74) и `_escape` делегируют. `grammar` — только stdlib, цикла нет.
- Читатели на `split_cells`: `contract.md_table` (:2236-2257), `grammar.py:469`, `planning_contract.py:923` (охватывающий `def` над :915 — имя читать), `:1920` (`_rerender_plan_cells` :1887), `claim_projector.py:422`, `:425`, `branch_accounting.py:428`. `sizing.py` получает даром. `grounding_table.py` своего разреза не имеет: только пин.
- Писатель: `_rerender_plan_cells` :1946 пишет клетки через `escape_cell`; прочие строки байт в байт. `claim_projector` не экранирует и не должен: `_cell_flaw` (:84, вызов :118) уже отказывает роли на `|` в полях утверждения, текст `holds "|", which ends a table cell` называет причину (см. поправку к M-7, §8). Пин: утверждение с `|` → этот отказ, реестр не тронут.
- Формы (`references/templates/requirements-register.md`, `phases/s2.md`, `phases/s3.md`, `agents/qa-requirements-tester.md`, `agents/qa-test-strategist.md`): черта в клетке — `\|`.
- `validate_artifacts.check_register` и проверка плана: клеток больше шапки → отказ с R/TS и дверью `write | inside a cell as \|` (строка A24). Срез `CELL_COUNT_CUTOFF` по `created`, форма `_oracle_dated`: реестр/план старше — чтение как было + строка предупреждения с R/TS.
- `design/architecture.md` (AR-13), `docs/SIBLING_MAP.md` (ось 21: выживший `grammar.split_cells`, снять `grounding_table.py` как члена), индекс `python tools/architecture_index.py`.

given: `design/factory-rules.md`, `plans/builder-rules.md`, `scripts/grammar.py` (:440-500), `scripts/project_decisions.py` (:60-90, :141-150), `scripts/contract.py` (:2236-2269), `scripts/planning_contract.py` (:905-925, :1887-1950), `scripts/claim_projector.py` (:84-120, :371-432), `scripts/branch_accounting.py:428`, `scripts/validate_artifacts.py` (:452-514), `docs/SIBLING_MAP.md` (ось 21), `design/architecture.md` (AR-13), находка `plans/piles/grounding/findings/20261020-chitateli-tablic-roli-rezhut-stroku-po-cherte-bez-escape.md`, этот блок.
owns:
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\grammar.py (+split_cells, +escape_cell, :469)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\project_decisions.py (_cells, _escape)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\contract.py (md_table)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\planning_contract.py (функция :910-924, _rerender_plan_cells)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\claim_projector.py (только чтение :422, :425)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\branch_accounting.py (:428)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\validate_artifacts.py (check_register, проверка плана :1596-1625 — только счёт клеток)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\references\templates\requirements-register.md
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\skills\qa-story\phases\s2.md
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\skills\qa-story\phases\s3.md
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\agents\qa-requirements-tester.md
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\agents\qa-test-strategist.md
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\design\architecture.md (AR-13)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\docs\SIBLING_MAP.md (ось 21)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\docs\ARCHITECTURE_INDEX.md (генерируется)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\tests\test_grammar.py
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\tests\test_project_decisions_change_request.py
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\tests\test_contract.py (блок md_table)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\changelog.d\g2-10-table-cells.md (новый)
non-goals: `audit_factory.py:1383`, `factory_dashboard.py:357, :3718` (писатели не роль); `execution_request.py:710`, `handoff.py:425` (не таблицы); разрешение `|` в утверждениях проектора; `contract.py:2273` (показ).
handoff: C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\docs\tasks\handoffs\g2-10-table-cells.md
edges: Инвариант всех: клетка не читается из чужой колонки молча. `| a \| b | c |` → `["a | b", "c"]`. Клетка кончается `\|` перед закрывающей чертой — черта сохранена. Неэкранированная `` `a|b` `` в новом реестре — отказ, не угадывание. Короче шапки (7 колонок, старый) — как раньше (FR-14). Пустая строка, `||`, разделитель `|---|` — как сейчас. Перепись плана не теряет `\|`, прочие строки байт в байт. Сохранённый реестр с `\|`: читается верно; хэш текста меняется → R5 ведёт в обновление таблицы — названо, не дефект. Сохранённый реестр/план с голой `|` на повторном `check_register`: старше среза — прежнее чтение и строка (инвариант: сохранённое не краснеет, молчаливого сдвига нет); новее — отказ. `created` нечитаем → новый мир, отказ (ошибка к отказу; дверь есть).
DoD: `python -B ai-packages/qa-factory/scripts/tests/test_grammar.py`, `python -B ai-packages/qa-factory/scripts/tests/test_project_decisions_change_request.py`, `python tools/architecture_index.py --check`. Мутации: `split` вместо разбора, обе черты сняты, нет разэкранирования → `test_grammar.py`; перепись без `escape_cell` → `test_s3_s4_chain.py`; `check_register` без счёта → `test_validators.py`. Большие `test_contract.py`, `test_validators.py`, `test_claim_projector.py`, `test_branch_accounting.py` — канон; билдер гоняет только свой блок. AR-13: grep `split("|")` с контролем, каждый оставшийся назван на оси с причиной; `test_one_source_per_fact.py` — канон. AR-15: выживший один. AR-9: отказ со строкой A24, `python -B ai-packages/qa-factory/scripts/refusal_registry.py --check`. AR-10: формы тем же коммитом. AR-28: тест чужой колонки. AR-12: `code_friction` или «не измерено». FR: A 1, 2; C 14, 38; D 41, 59; G 54; B, E, F не менялись.

---

## 7. G2-2 — покрытие и остановка

**Что менять.**

1. `grounding_table.py`:
   - `+coverage(data, register_rows, policy, evidenced=frozenset()) -> dict`: `implemented, partial, n, unknown, percent, road (none|highlight|stop|unknown), reading (""|nothing_asked)`. N: `reg.ids` минус `reg.exempt`, минус строки с `outside_diff` и `where` ≠ `none`, минус R из `evidenced`. Числитель — `implemented`, `partial` (`grounding-policy.json:3`). `unknown` остаётся в N и не в числителе. Строка реестра без строки таблицы — в N, не в числителе. `road`: `100*num < coverage_stop_below_percent*n` → stop; `num < n` → highlight; иначе none. `n == 0` → stop, `reading: nothing_asked`.
   - `+coverage_of(root) -> dict`: читает таблицу и `C.register_rows`; `evidenced` — R, где `BS.unchanged_evidence(row, root, collected=BS.collect(root))[0] == "evidenced"` (импорт BS ленивый; BS импортирует GT). Только это слово выводит `unchanged` из N. `BS.collect` бросил → никто не `evidenced`.
   - `+coverage_digest(root, cov)`, `+refactoring_digest(root, share)`: первые 12 hex sha256. Первый: отсортированные `diff_records(root)[i]["sha256"]` + отсортированные `r:state:statement_sha` строк N вне числителя (`register_info.statements`). Второй: те же sha + `W`, `T`. `register_sha256` целиком НЕ брать: проекция claims в `closing` сдвигает его на нормальной истории.
   - `+stop_word(pipeline, prefix, digest) -> entry|None`: `C.stage_override_values(pipeline, prefix, "S3")`, значение == digest; плюс живая запись `match == "*"`. Единственный читатель слова для вопроса и R6.
   - `--share` пишет и `requirement_coverage`.
   - `exit_findings` + R6: **считает заново** `share` и `coverage_of` над текущими байтами; сохранённые ключи только показ. Road `stop` без `stop_word` на текущем дайджесте → Finding `R6`, `who="driver"`, текст содержит блок `grounding coverage stop <digest>` / `grounding refactoring stop <digest>` и что изменилось. Road `unknown` → Finding `R6`, `who="conductor"`. Сохранённый road ≠ пересчитанному → Finding `R3`, `who="driver"`. Нет ключа в мире diff — не «остановки нет»: решает пересчёт (строка t-1015:96 снята).
2. `story_run.py`:
   - `s3_between_windows` (:8504): `self.py("grounding_table.py", "--share", "--task", self.task)` (код ≠ 0 → `Refusal` дирижёру); `CP.project_row_questions(self.task_root)` (проблемы → `Refusal`, образец `s3_project`); `self.grounding_stop()`. Докстринг переписать.
   - `+grounding_stop()`, `+_coverage_person(cov, digest)`, `+_refactoring_person(share, digest)`; `grounding_stop` до ~60 строк. Покрытие первым. Есть слово → дальше; нет → `raise` person. Рефакторинг спрашивается только после прохода покрытия. `unknown` любого — `Refusal` дирижёру без карточки. Образец — `gate_a_dry_person` :10672, `manual_gate_note` :10668. Вопрос: `self.site_seam_person("grounding_stop", self.closed_question(<ключ-литерал>, lead, options), "S3", block=<блок>, details=…)`, ключ — литерал в каждом вызове, `# remains:` как :10669. Варианты: `{"answer":"go on","token":"go on","says":…}`, `stop` с собственным `says`. Других токенов нет (`SITE_MOVES`, неизвестный выпадает). Ветка `take_answer` своя не нужна: общая `offered` (:15779). Lead называет требования человеческим языком, `unknown` отдельным абзацем; без `K-n`, имён полей.
   - Выбор ключа покрытия: `reading == nothing_asked` → `s3.grounding_coverage.nothing_asked`; вне числителя только `unknown` → `s3.grounding_coverage.not_known`; иначе `s3.grounding_coverage`.
   - `s3_check_packet` после `if back:` :13774: `self.s3_between_windows()`.
   - `s3_window_completion.closing` и `s3_ticket_completion.closing`: после `s3_project` тот же `--share` (ключи свежи на нормальной дороге; расхождение значит ручную правку или прямой `accept`).
   - `s3_strategist_lines`: в ветке окна 2 при diff, к `reach`: строка, что код посчитал (покрытие, слово человека, если есть, — через `GT.stop_word`), и по строке на выход `PC.regression_from_blast(doc)`: `B-n <команда>` — внеси цель в раздел `## Recommended regression`, подпись `blast:B-n`.
3. `claim_projector.py`: `+project_row_questions(task_root) -> SimpleNamespace(projected, problems, wrote)`. Каждая непустая проза `question` у `requirements[]` и `rows[]` → строка `open_questions` готовности: ключ `{"requirement": r, "origin": ORIGIN}` / `{"row": g, "origin": ORIGIN}`, через `QR._question_row`, запись через `QR._write_readiness` под тем же замком, что `project`, счётчики `_counters`. Идемпотентно. Реестр не меняет.
4. `question_register._question_row` (:1230): `row[key] = question[key]` только при `key in question` (вопрос строки не несёт before/now; `C.before_now_errors` законно молчит у вопроса без обоих). Пины: claim и S4 как были.
5. `contract.py`: `+grounding_row_question(prose, quote, where) -> dict`: `question`=проза; `source_says=[{"quote":quote,"where":where}]`; `readings` — две: `Needed in this story: the change has to do it` / `Not needed in this story`, `from: CLAIM_ORIGIN`, `if_chosen` — что будет; `severity` — слово из `claim_question` (:1115, читать); `owner_role: qa-test-strategist`. Проходит `C.question_errors`.
6. `references/block-names.json`, **строго одним коммитом с методом** (плохая строка роняет всю таблицу, `waiver.py:564-569`): `{"block": "grounding coverage stop <digest>", "reader": "story_run:Driver.grounding_stop", "stages": ["S3"]}` и такой же `grounding refactoring stop <digest>`.
7. `references/question-prices.json`, четыре ключа:
```json
"s3.grounding_coverage": [
  {"answer": "go on", "factory": "record", "person": "none", "delivery": "no", "unverified": "the requirements named above, which the change does not implement"},
  {"answer": "stop", "factory": "nothing", "person": "your_work", "delivery": "waits"}
],
"s3.grounding_coverage.not_known": [
  {"answer": "go on", "factory": "record", "person": "none", "delivery": "not_known", "unverified": "whether the requirements named above are implemented; the questions about them reach you at gate A"},
  {"answer": "stop", "factory": "nothing", "person": "your_work", "delivery": "waits"}
],
"s3.grounding_coverage.nothing_asked": [
  {"answer": "go on", "factory": "record", "person": "none", "delivery": "not_known", "unverified": "whether this merge request belongs to the story"},
  {"answer": "stop", "factory": "nothing", "person": "your_work", "delivery": "waits"}
],
"s3.grounding_refactoring": [
  {"answer": "go on", "factory": "record", "person": "none", "delivery": "not_known", "unverified": "whether the moved code behaves as before, beyond the checks the plan adds"},
  {"answer": "stop", "factory": "nothing", "person": "your_work", "delivery": "waits"}
]
```
   Слоты `what` для `your_work` — `no_move.price_row` (:470). `question-vocabulary.json`, `human-questions.md` НЕ правятся. Строки `not_implemented` — запись доставки делает G2-5 независимо от слова (В4).
8. `agents/qa-test-strategist.md`: `pending_implementation`, подсветка; окно 2 ссылается вопросы строк `question_refs`.

Нового состояния нет (F-6′): `stop` = открытый вопрос; свободные слова → шов → дирижёр, `rework --stage S1` (:3215), имя нового MR читает он (P22). `R6 (ii)` t-1015:95 снят: `not_implemented` выше порога не стоп, а подсветка гейта A и запись доставки.

given: `design/factory-rules.md`, `plans/builder-rules.md`, `scripts/story_run.py` (:3778-3865, :8313-8345, :8405-8557, :10648-10713, :13759-13778, :14412-14495), `scripts/waiver.py` (:196-235, :493-600, :664-698), `scripts/contract.py` (:112-145, :542-600, :970-979, :1115-1130), `scripts/base_slice.py` (:472-504, :557-586), `scripts/grounding_table.py` (:277-322, :852-914, :1011-1045), `scripts/claim_projector.py` (:517-575, :625-680), `scripts/question_register.py` (:1213-1242), `scripts/no_move.py` (:39, :467-497), `references/grounding-policy.json`, `references/block-names.json`, `references/question-prices.json`, этот блок.
owns:
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\story_run.py (Driver.s3_between_windows, +grounding_stop, +_coverage_person, +_refactoring_person, s3_check_packet, s3_window_completion, s3_ticket_completion, s3_strategist_lines)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\grounding_table.py (+coverage, +coverage_of, +coverage_digest, +refactoring_digest, +stop_word, main, exit_findings — R6)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\claim_projector.py (+project_row_questions)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\question_register.py (_question_row)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\contract.py (+grounding_row_question)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\references\block-names.json
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\references\question-prices.json
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\agents\qa-test-strategist.md
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\tests\test_grounding_coverage.py (новый)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\tests\test_story_run_s3_windows.py
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\tests\test_waiver_release.py (только если пинит набор строк)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\changelog.d\g2-2-coverage-stop.md (новый)
non-goals: `controller.py`; запись `pending_implementation` и строки гейта (G2-5); `question-vocabulary.json`, `human-questions.md`; новое состояние; вызов `rework` кодом; настройка потока MR (`--mr` — дирижёр, живое доказательство — `live-runs`).
handoff: C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\docs\tasks\handoffs\g2-2-coverage-stop.md
edges: Тест НА и ЗА: N=1: 0/1 стоп, 1/1 нет. N=2: 1/2 ровно 50 % — подсветка. N=3: 1/3 стоп, 2/3 подсветка. N=4: 3/4 подсветка, стопа и записи слова нет. Полный — ничего. 4 `unknown` → N=4, стоп, ключ `.not_known`, текст не говорит «не реализовано». N=0 без `unknown` → `nothing_asked`. 0/2 `outside_diff`, `where: none` → стоп, `delivery: no` (запись — G2-5, инвариант: обещание цены держится, FR-10). R-1 реализован, R-2…4 `outside_diff` с `where` → вне N (честный MR). Не тот MR: утверждения S2 из диффа вне N, стоп. `delta` нет или неверное слово → в N. `unchanged`: `unevidenced` → в N (ошибка к счёту; `before: unknown`, упавший срез); `BS.collect` бросил → всё в N. Пустой дифф: 0 из 0 не зелёный. Только тесты (T=0): стоп покрытия с вариантом свободными словами. Нет MR/current-code → шага нет. Политика/таблица нечитаема → `road: unknown`, дирижёр, не карточка (FR-3). Два стопа: покрытие первым, после `stop` рефакторинг не спрашивается. Ответ есть, дайджест тот же (рестарт) → не спрашивать (FR-7). Дайджест другой → спросить снова; повтор текста метит `ask`. **Инвариант: слово о других байтах или другом наборе не считается.** Состояние правится в окне 2 после `go on` (R-3,4 → R-3..7): новый дайджест → R6 на выходе, `who="driver"`, текст называет новое; пин, что находка доходит до дирижёра, а не роли (FR-2, AR-17), на дороге :8521 резюмируется только роль. Слово другого дайджеста НЕ снимается по подстроке. Сторона безопасности `stop_word` (пины): `grounding`, `stop` как `match`; другой дайджест; `revoked_at`; пустой `decision`; другая стадия; нечитаемый `pipeline.json` → блок стоит. Намеренно проходит `*`, в отчёт как слово человека (FR-4). Голый `--block "grounding coverage stop"`: не имя (`prefix_value` → None), идёт в `_held_against_record`; пины трёх исходов: `carrier`, `unmatched` (отказ), `unknown`. `--block "<часть строки>"` на отказе контроллера проходит через `_passed_by_person` и пишется в `passed-by-person.jsonl` — явная дверь FR-57, вопрос и `stop_word` на неё не опираются. Нет строки цены → вопрос без цен и дефект, ворота стоят. `pass_block` не записал → вопрос держится (:3860). `go on` доводит до окна 2 — тест; красный → вопрос Lead, не обход. Вопрос строки: `unknown` с прозой → `Q-n`, повтор не дублирует; проза изменилась при том же ключе → остаётся прежний `Q-n` + строка заметки (инвариант: один вопрос на ключ); готовности нет → `problems`, `Refusal`, не молчание. Прибавка вопросов пересекла порог → существующий `Driver.question_threshold` (S3 в `stages` имени) — один пакет; не обход. Вопрос без строки плана — WARN на выходе S3 (`no_row_for_question` t-502-s1b §1.3), поэтому окно 2 обязано сослаться `question_refs`. `return_to_developer` не существует; P8: наружу ничего. Рестарт по `s3_check_packet`: пакет окна 2 над неотвеченным стопом не уходит; `repair_verify` возвращается раньше.
DoD: `python -B ai-packages/qa-factory/scripts/tests/test_grounding_coverage.py`, `python -B ai-packages/qa-factory/scripts/tests/test_story_run_s3_windows.py`, `python -B ai-packages/qa-factory/scripts/tests/test_waiver_release.py`. Тесты B-1: `road: none` руками над 1/3; смена `state` после `go on`. Мутации → `test_grounding_coverage.py`: `<` на `<=`; partial вне числителя; outside_diff в N; unknown вне N; R6 читает сохранённый road; `unchanged` без улики; `register_sha256` в дайджесте; подстрока вместо `stage_override_values`. → `test_story_run_s3_windows.py`: слот не зовёт; покрытие после рефакторинга; вопрос строки не спроецирован. AR-16: новые ключи, дорога `Person`/`ask`; `human_text.py --selftest`, `test_human_questions.py` — канон. AR-17: стоп через шов либо `# remains:`, рост `NO_MOVE_BASELINE` назван; `audit_factory.py --no-move`. AR-20: поднятый храповик — ключ, было → стало, причина. AR-24: `go on` через `person_words`, `test_words_doors.py` — канон. AR-25: ход каждому ответу, `test_state_exits.py` — канон. AR-26: перепись t-928. AR-28: `gate_registry.py --check`. AR-19: `s3_check_packet` и `stage_S3` — одна функция. AR-13: `stage_override_values`, `delta_state`, `read_grounding`, `write_key`, `diff_records` зовутся. AR-12: `code_friction` или «не измерено». `test_human_questions.py`, `test_no_move_seam.py`, `test_story_run_words.py`, `test_driver_layers.py` — канон. FR: A 3, 4, 42, 48, 57; B 6, 7, 8, 9; C 13; D 59; E 21; G 54; F не менялось.

---

## 8. G2-3 — дорога FR-22

**Что менять.**
1. `check_delivery.py`: `+bug_candidate_record(ref, requirements, to_check, how, source) -> dict` = `{"text": "grounding: <ref> <to_check>", "kind": "bug_candidate", "case": "", "ref": ref, "item_key": ref, "requirements": [...], "to_check": to_check, "how": how, "source": source}`. `item_key` обязателен.
2. `+grounding_records(artifacts, doc, facts)`; в `assess` рядом с `branch_records` (:1966), до `decide`. Инвариант положения: фильтр :1960 запись не трогает, `decide` её видит.
3. **Два входа, один предикат.** Вход `K`: `rows[].risks[]` таблицы (только diff), `ref=K-n`, `source="grounding"`. Вход `register`: `C.candidate_defects(register_text)` (`[{r, requirement, file, line}]`, G2-15), `ref=R-n`, `source="register"`, в любом мире источника. **Записи реестра пишет этот узел; G2-15 их не пишет** (t-502-s1b:151; t-525-amendment не существует). Строки плана: `coverage_contract.plan_rows(task_root)`; ссылка: `PC.grounding_refs(row)["K"]`, для R — `PC.row_requirements`. Леджер: `doc["rows"]`, `kind == "plan_row"`, `ref == row["ts"]` (`ledger.py:1140`).
4. `planning_contract.py`: `+row_tests_it(row) -> bool` (`disposition ∈ {automate, manual-agent}`); `candidates_without_row` зовёт её (одно определение, поведение не меняется, `test_candidate_defects.py` зелёный).
| Кандидат | Запись |
|---|---|
| ни одна строка плана его не называет (в том числе есть в `not_planned`) | `bug_candidate`; в `how` — решение человека из `not_planned`, если есть |
| названные строки только `skip`/`manual-human`/незакрытая `unverifiable` | `bug_candidate` |
| строка `row_tests_it`, её нет в `doc["rows"]` | `bug_candidate`, `to_check` со словами «could not be linked» |
| строка `row_tests_it` в леджере, не выполнена | нет: свой вид строки |
| красный | нет: обычный баг |
| зелёный, `oracle_unknown` без ответа | `unconfirmed_expectation`, не молчание. **Первым ходом — красный тест:** если леджер уже даёт этот вид (`open_oracles`, `ledger.py:1137`) — записи нет; нет — запись `{"kind": "unconfirmed_expectation", "case": <кейс>, "ref": ref, ...}` здесь (P20, FR-58) |
| зелёный с ответом | нет |
| таблица или реестр нечитаемы при непустой истории | `own([...], "factory_record")`, не «кандидатов нет» |
5. `how` пункта: `Say at gate B that this needs a bug report (name <ref>): the conductor sends it to the failure analyst at S7; or leave it with you.` Исполнитель (В3 (а), FR-9): свободные слова → шов → дирижёр → `controller.py --operation rework --stage S7 --role qa-failure-analyst --reason "<слова человека>"`. `references/conductor-actions.json:8`: дополнить `says`. Код сам не черновит (D-0051 (3)). **Первым ходом** тест `build_rework_request` S7 с такой причиной при гейте B; отказ → долг FR-22 остаётся, строка отчёта, вопрос Lead, не обход.
6. `agents/qa-test-strategist.md`, `phases/s3.md`: K-n → строка → Then из требования, иначе `oracle_unknown` с вопросом.
7. `design/factory-rules-debt.md:24`: строка снимается ТОЛЬКО при В3 = (а) и зелёном тесте п. 5; иначе остаётся строкой с новым текстом. *Check* FR-22 пишет Lead.
8. `gate_brief.undrafted_discrepancies` не меняется; форма черновика S7: `possible_duplicate` (`gate_brief.DUPLICATE_KEYS` :71, `artifact-contract-run.md:113`).

given: `design/factory-rules.md` (FR-21, FR-22), `design/factory-rules-debt.md:24`, `plans/builder-rules.md`, `scripts/check_delivery.py` (:1592-1664, :1707-1770, :1925-1980), `scripts/ledger.py` (:1130-1142), `scripts/coverage_contract.py:287`, `scripts/planning_contract.py` (:372, `candidates_without_row`, `row_requirements`), `scripts/contract.py (candidate_defects)`, `references/delivery-verdict-kinds.json` (:43, :53, :56), `references/conductor-actions.json:8`, `docs/tasks/specs/t-502-s1b-fence-and-answers.md:54, :58`, этот блок.
owns:
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\check_delivery.py (+bug_candidate_record, +grounding_records, assess — строка у :1966)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\planning_contract.py (+row_tests_it, candidates_without_row — делегирование)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\references\conductor-actions.json (строка :8)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\agents\qa-test-strategist.md
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\skills\qa-story\phases\s3.md
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\design\factory-rules-debt.md (строка FR-22)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\tests\test_check_delivery.py
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\tests\test_report_facts.py
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\changelog.d\g2-3-fr22-road.md (новый)
non-goals: `report_facts.py`, `delivery_summary.py`, `gate_brief.py` без нужды (читают `left_items`; пункт без строки в `test_report_facts.py` → вопрос Lead); `pending_implementation` (G2-5); черновик кодом; `drift`, пара тяжесть × вероятность (В2); связь «зелёный на другом Then» с K-n (очередь: кейс не связывает Then с K-n, строка §8 Lead); `*Check* FR-22`.
handoff: C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\docs\tasks\handoffs\g2-3-fr22-road.md
edges: Инвариант: чтение кода не подтверждает баг и не двигает вердикт само (вид даёт `after_checks`, не `no`); кандидат без теста не теряется и не считается дважды. Рисков нет → записей входа K нет. Вне diff вход K молчит, вход реестра работает. `candidate_defects`: `file: None` → `to_check` со словами `place in the code not named`. K-n в `not_planned` со словом человека → строка Left с этим решением. Два K-n на одно место → две записи. K-n и R-n на одно место → две записи, строка плана, назвавшая оба, закрывает оба; показ подсказывает `possible_duplicate`. Неизвестный вид в старой установке → `no` + `VERDICT_KIND_UNKNOWN`. Текст начинается `grounding:`: семья владельца приходит с G2-5; до него `reason_owner` пишет дефект «no owner family» (видимо, не теряется; в пределах релиза).
DoD: `python -B ai-packages/qa-factory/scripts/tests/test_check_delivery.py`, ключи каждой строки таблицы + пара «`skip` закрывает» отказана. Мутации: запись потеряна, `skip` закрывает, `oracle_unknown` зелёный молчит → `test_check_delivery.py`; пункт не доходит до Left → `test_report_facts.py`; код написал черновик → `test_bug_records.py`; «никто не завёл» исчезла → `test_gate_brief_and_retro.py`. Большие и `test_third_verdict.py`, `test_candidate_defects.py` — канон. AR-27: источник называет дорогу в `bugs/`, вердикт читается `word_of`. AR-22: производитель `bug_candidate` появился; `test_field_producers.py` — канон. AR-26: K-n ведёт к требованию. AR-13: `grounding_refs`, `plan_rows`, `read_grounding`, `candidate_defects` зовутся. AR-28: нечитаемое → `factory_record`. AR-11: цифры A22/A25 до и после. FR: C 13; D 18, 58; E 19, 21, 22, 35; F 41; G 34, 54; A, B не менялись.

---

## 9. G2-5 — строки человеку

**Что менять.**
- `check_delivery.grounding_records` (G2-3): **каждая строка `not_implemented` из N** (через `GT.coverage_of`) → `{"text": "grounding: <R-n> is required by the story and this change does not implement it", "kind": "pending_implementation", "case": "", "ref": R-n, "source": "grounding"}`, **независимо от слова**. `outside_diff` с `where: none` из N → та же запись только при `GT.stop_word` на текущем дайджесте (обещание цены). `partial`, `unknown` записи не дают.
- `references/delivery-reason-owners.json`: семья `text_starts: "grounding:"`, владелец `product`, тем же коммитом (образец `coverage:` :97; «add its family in the change that writes it», `check_delivery.py:192`).
- `gate_brief.py`: `collect` (:2092) — ключ `"grounding"` в словарь (:2117), читатель `PC.read_grounding`, пересчёта нет; `+_grounding_lines(data)`; `render` (:3099): сразу после `lines = _head_lines(data)`; `cap` (:3133) прибавляет их длину (образец :3137). Строки: уведомление `road: notify`/`stop` рефакторинга; подсветка покрытия с именами требований; вопросов не задаёт. Только гейт A (`"gate": "A"`).
- `report_facts.py`: `+_r_grounding(facts)` + одна строка в `render` (:2058): доля и дорога (`n/a` печатается), покрытие, `mixed_hunks`, файлы вне T, псевдо-ханки, число `orphans`, `null_outcome.source` (t-1015 §L-3 M-3), области `truncated`, `language` (t-1046 шов 10). Ниже 30 % с рефакторингом — строка отчёта, не гейта. `_regression`, `_r_regression` НЕ трогаем (RG1-1; регрессия — раздел плана, F-10/M-4; строка узла про `blast_radius[].regression` снята).

given: `design/factory-rules.md`, `plans/builder-rules.md`, `scripts/gate_brief.py` (:59, :2092-2120, :2586, :3099-3143), `scripts/report_facts.py` (:2058-, :2267), `scripts/check_delivery.py` (:185-200, `grounding_records`), `scripts/grounding_table.py (coverage_of, stop_word)`, `references/delivery-reason-owners.json:97`, `references/delivery-verdict-kinds.json:43`, этот блок.
owns:
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\gate_brief.py (collect, render, +_grounding_lines)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\report_facts.py (+_r_grounding, render — строка)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\check_delivery.py (grounding_records)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\references\delivery-reason-owners.json (одна семья)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\tests\test_gate_brief_and_retro.py
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\tests\test_report_facts.py
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\changelog.d\g2-5-grounding-lines.md (новый)
non-goals: регрессия в отчёте; `delivery_summary.py`; `index.stand` (F-17, вопрос Lead); новые вопросы; `gate_preflight`.
handoff: C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\docs\tasks\handoffs\g2-5-grounding-lines.md
edges: Инвариант: отчёт не меняет смысла вердикта (FR-35); `pending_implementation` никогда не «Left with you»; 3/4 с R-4 `not_implemented` → вердикт `no` без всякого слова, гейт A показывает (FR-21, В4). `coverage_of` бросил при S8 → `factory_record`, не «нечего сказать». Нет таблицы/вне diff — строк нет, в отчёте `null_outcome.source`. Нечитаема — одна строка, не тишина. `road: none`, 100 % — ничего. Share `unknown` — строка дефекта фабрики. На пределе `cap` (`MAX_LINES = 40`) строки в голове, не срезаются: тест на и за. Подсветка и вопрос об одном требовании — один пакет не спорит с собой (FR-10). Показ без `K-n`/`B-n` без пояснения. `not_implemented` вне N (exempt, `unchanged` с уликой) записи не даёт.
DoD: `python -B ai-packages/qa-factory/scripts/tests/test_report_facts.py`, `python -B ai-packages/qa-factory/scripts/tests/test_gate_brief_and_retro.py`. Мутации: «только после go on», pending в Left, n/a скрыт → `test_report_facts.py`; строка ниже вопросов, `cap` не растёт → `test_gate_brief_and_retro.py`. `test_gate_question_form.py`, `test_gate_preflight.py`, `test_delivery_ownership.py` — канон. AR-16: `human_text.problems`, без имён полей. AR-27: `word_of`. AR-22: `refactoring_share`, `requirement_coverage`, `orphans`, `truncated`, `language` получают читателя; `test_field_producers.py` — канон. FR: B 6, 10; E 19, 20, 21, 35; F 41; G 54; A, C, D не менялись.

---

## 10. G2-14 — кандидат из глотающего `catch`

**Что менять.**
- `references/user-path-failure-patterns.json` (новый): `{id, why, languages: [суффиксы], start, quiet, loud, window_lines}`; записи `swallowed_catch`, `unchecked_response`.
- `scripts/user_path_failures.py` (новый; строка в `audit_factory.CLI_SCRIPTS`, форма :166): `find(task_root) -> {matches, unmeasured}`. Область: добавленные строки `DP.index(work)`; вне diff — места `current-code:` из `C.register_rows(text)["observable"]`. Совпадение: `start`, в `window_lines` есть `quiet`, нет `loud`. Полный список — `work/user-path-failures.json`.
- `brief_pack.py`: `+user_path_failure_lines(task_root)`, строка в голове `build` при `stage == "S2"` (рядом :2458).
- Устав тестера, `s2.md`: совпадение на пути пользователя → строка `derived`, `derived_from:` значение из `vocabulary.yaml`, ключ `derived_from_marks` (данные G2-15, не литерал), `observable: current-code:<файл>:<строка>`, без ожидания; вне пути — причина в `open`.
- `references/artifact-writers.json`: строка артефакта.

given: `design/factory-rules.md`, `plans/builder-rules.md`, `scripts/brief_pack.py` (:2430-2499), `scripts/diff_pass.py (index)`, `scripts/contract.py:946`, `scripts/audit_factory.py:166`, `handoffs/vocabulary.yaml`, находка `plans/piles/grounding/findings/20261031-catch-i-fetch-bez-ok-ne-stanovyatsya-trebovaniem.md`, этот блок.
owns:
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\references\user-path-failure-patterns.json (новый)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\user_path_failures.py (новый)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\audit_factory.py (CLI_SCRIPTS — строка)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\brief_pack.py (+user_path_failure_lines, build — строка)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\references\artifact-writers.json (строка)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\agents\qa-requirements-tester.md
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\skills\qa-story\phases\s2.md
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\tests\test_user_path_failure_patterns.py (новый)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\scripts\tests\fixtures\ (новые фикстуры, без кириллицы)
C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\ai-packages\qa-factory\changelog.d\g2-14-user-path-failures.md (новый)
non-goals: код не решает, лежит ли место на пути пользователя; запись в реестр кодом; `candidate_defects`; отказ на нечитаемом JSON (F-11); парсер языков.
handoff: C:\Projects\yml-text-factory\.claude\worktrees\release-0-10-8-36e54a\docs\tasks\handoffs\g2-14-user-path-failures.md
edges: Ошибка кода — в лишнее совпадение (роль отбросит), не в пропуск. Неудобные входы: `catch` с тостом через 10 строк; многострочный `fetch`; `catch` в комментарии; минифицированный файл → `unmeasured`. 20 совпадений → 20 строк, «ещё» нет; 21 → 20 + `1 more, the list is in work/user-path-failures.json` (инвариант: усечение называется, файл полный). Язык без шаблона → `not measured: no pattern for .kt`, не «мест нет». JSON нечитаем → строка брифа `not measured: <файл>, a defect of the factory`, stderr, бриф строится (P1); отличима от «совпадений нет» (тест). Нет кода и диффа → `not measured: no code`. **Вне diff на первом S2 реестра ещё нет** → та же строка `not measured`; на повторном S2 реестр есть (инвариант: ноль не выдумывается). Неразобранное `current-code:` → `unmeasured`. 0 совпадений → `no match, checked: …`.
DoD: `python -B ai-packages/qa-factory/scripts/tests/test_user_path_failure_patterns.py`, фикстура `catch { console.error }` после `fetch` — совпадение; `catch` с тостом и `if (!response.ok)` — нет. Мутации → он же: `loud` не читается; предел 21; язык → пусто; JSON ломает бриф. `test_brief_pack.py`, `test_artifact_writers.py`, `test_audit_rules.py` — канон. AR-1: строка в carriers AR-1 тем же коммитом. AR-2: скрипт отчитывается, не останавливает. AR-7: назвать, что решает роль; `stage_compare.py` неприменим (новый шаг); цена S2 или «не измерено». AR-8: путь в `known_paths` или брифе. AR-11: A22/A25 до и после, `python -B ai-packages/qa-factory/scripts/selftest.py --limits`. AR-14: строка `artifact-writers.json`. AR-18: не детектор, `REJECT` не печатает. AR-22: значение пометки и читатели. FR: C 12, 13, 15; E 37; F 41; G 30, 47; A, B, D не менялись.

---

## 11. Строки для §L и пачки (Lead; §L меняет его же решения)

1. t-1015 §L F-1 (a) → дом ворот `GT.exit_findings` (F-14). t-1015:96, :97 (ключа нет — законно; `decision`) сняты: пересчёт и `stage_overrides` (B-1, F-13). t-1015:95 (ii) снят (B-2).
2. t-1015 §3.5, §L-2 M-6, §L-3 M-4 заменены: `PC.regression_from_blast` + R7-регрессия; `HC.check` не трогается (F-10, F-15, M-4, F-16). Строка G2-5 «регрессия из `blast_radius[].regression`» снята.
3. t-1015 §L-2 D-1 (`running_dispatch`) снят: новых читателей нет.
4. t-1046 шов 2 (ii) исполняется так: проекция `CP.project_row_questions` — G2-2.
5. Строка узла G2-15 «оракул `unconfirmed`» читать `oracle_unknown: true`. Строка G2-2 `Controller._grounding_stop`, `question-vocabulary.json`, `human-questions.md`, «2*implemented<N» — снять.
6. «Остатки» пачки 1 с `сделано`/`перенос`: гейт A после `revise_plan` (t-1015 §L F-10 (a); `revise_plan` в файле пачки 0 упоминаний), тип `stage_complete` (t-1035 m-2). Очередь `gates-and-words`: связь Then с K-n (M-8 вход 3), чужая документация как источник.
7. FR-22 *Check* — Lead, по В3. Оффер MR (В1) — строка кучки `gates-and-words`, если владелец подтвердит. `drift` (В2) — перенос с подтверждением человека.

## 12. Находка → где закрыта

| Находка | Где |
|---|---|
| B-1 | §7 п. 1 (`exit_findings` R6, пересчёт), п. 2 (`--share` в `closing`), DoD |
| B-2 | §9 первая строка; §7 (R6 (ii) снят); §11.1 |
| B-3 | §7 п. 2, 3, 4, 5 |
| B-4 | §4 п. 1 первая строка, п. 8; §11 ничего не отменяет |
| B-5 | §4 п. 3a, edges |
| B-6 | §8 п. 3; §2 очередь G2-15 → G2-3 |
| M-1 | §7 п. 1 (два дайджеста, `stop_word`), edges |
| M-2 | §7 п. 1, ключ `.not_known`, edges; §9 запись `where: none` |
| M-3 | §8 п. 5, 7 (В3) |
| M-4 | §4 п. 1, 2; §7 `s3_strategist_lines`; §9; §11.2; F-16 |
| M-5 | §4 п. 1 (R7, форма, G-0b), п. 6; §2 сообщить S1 |
| M-6 | (а) §7 п. 6, DoD; (б) §7 owns, §2; (в) §4 owns, «exit_gate не трогается»; (г) §4 п. 7; (д) §4 п. 6 |
| M-7 | §6 писатель и edges. Поправка: `claim_projector._cell_flaw` (:84, :118) уже отказывает на `|`, «код пишет и сам отказывает» не воспроизводится; `escape_cell` нужен только переписи плана |
| M-8 | §8 таблица, п. 4; вход 3 — §11.6 |
| M-9 | этот файл; `unchanged` — `BS.unchanged_evidence` (`base_slice.py:557`, имя и направление прочитаны); §7 |
| m-1 | §7 edges, три исхода |
| m-2 | §3 сигнатура |
| m-3 | §8 п. 1 |
| m-4 | §5 текст :495; §2 очередь `check_register`; передать S1 |
| m-5 | §7 edges |
| §3: F-1, F-3, F-4, F-6′, F-8, F-11, F-13, F-14 | §7, §3, §6, §7, §2, §10, §7, §4 |
| §3: F-2 | §5; условие закрыто чтением :1068-1102 |
| §3: F-5 | `go_on` = чётность: §7 цена `s3.grounding_refactoring`; K-n в `not_planned`: §8; `unclassified`: §3; `N=0`, `unknown`: M-2 |
| §3: F-7 | §5 |
| §3: F-9, F-12 | В1, В2; §11.7 |
| §3: F-10, F-15 | M-4 |
| §5 `oracle_unknown` | §11.5, §5 |
| §5 `unconfirmed_requirements` | снято как поставка G2-15: потребители — гейты G2-12; пин `:1605` §5 |
| §5 `bug_candidate_record`, очередь, цепочка `_detector_body`, пометка | §8 п. 1, 3; §2; §10 |
| §6 соседи: `baseline:` | не проверено, §13 |
| §6 очереди | §2 |
| §6 КАЧЕСТВО: `+_s3_completion_gate`, `grounding_stop` ≤ ~60 | §4 п. 3; §7 п. 2 |
| §6 ось 5 `null-outcomes` | §4 п. 6 |
| §7 `claim_row_errors` | закрыто §5 |
| §7 `DV.named` | закрыто: §4 edges (`detector_verdict.py:463`; предел `LIST_LIMIT`, значение не читал; тест) |
| §7 `delivery_summary.py` | §8 non-goals, первый ход — тест |
| §7 `_append_question` | **нет в коде под этим именем** (Grep, контроль `append_question_ref`, -i не нужен для имени): дверь — `QR._question_row`, `_write_readiness`; §7 |
| §7 `BS.collect` | закрыто (M-9) |
| §7 `recheck_stage_block` | §7 тест «`go on` → окно 2» (t-512 §6) |
| §7 `:2692` | сейчас `:4498` по `_closes_stage` (Grep); тело не читал, пин §4 edges |
| §7 леджер `oracle_unknown` зелёный | §8 таблица, первый ход — красный тест |
| §7 цикл CP↔GT | закрыт чтением импортов: `claim_projector.py:41`, `grounding_table.py:35-42`; §4 п. 1, 5 |
| §7 `test_waiver_release.py:874` | §7 свидетель; пин набора → в owns условно |
| §7 `question-prices` классы | сверены формы `s6.gate_a_dry`, `s6.stand_login` (`question-prices.json:183, :193`): `no`, `waits`, `not_known`, `record`, `nothing`, `your_work` в ходу; `your_work` с `waits` — t-512, слоты проверит тест |
| §7 RD1-20/21 | закрыто: t-514 :110, t-507 :101, §2 |
| §7 `t-929` тело, `G2-10/12/14` находки | находки в `given` узлов; t-929 не читал, §13 |

## 13. Развилки

- **F-16 (новая, вопрос Lead; узлы написаны по рекомендации).** M-4 говорит «`areas[].regression` проецируется в раздел одним кодом», а t-507 §8 (RG1-1, чей узел M-4 велит не трогать) решил обратное: «код не сочиняет список; роль пишет, инструмент проверяет», одна строка `Command:`, отказ на второй. Запись кодом в `test-plan.md` — второй писатель секции (AR-14), идёт после детектора и потому не проходит `regression_scope.problems`. (а) **рек.:** код выводит (`PC.regression_from_blast`), отдаёт роли строками окна 2, роль пишет, R7 проверяет токен `blast:B-n`. У поля есть читатель, носитель для отчёта один, RG1-1 цел; цена — одна проверка роли. (б) буквально M-4: драйвер в `closing` вливает цели в `Command:`; нужна правка `_detector_body`/`regression_scope` порядка и пересмотр t-507 F-7.
- **F-17 (новая, вопрос Lead).** t-1046 шов 10 (§L F-10A (b), «обязательно») отдал G2-5 чтение `index.stand` из `evidence/runtime-provenance-*.json`; в t-504, t-512, критике этого нет, а строка узла молчит. (а) **рек.:** не в этот узел, строка очереди кучки `grounding`: регрессия по P24 от стенда не режется, отчёту не нужно. (б) в `_r_grounding` одной строкой. Узел исполним по (а).
- В1–В4 — у владельца, не повторяю. До ответа по В3 строка долга снимается только по условию §8 п. 7.

**Малые выборы, закрытые мной:** имя `_s3_completion_gate` вместо `_s3_completion_problems` (метод поднимает отказ: так не меняется маршрут генератора блоков); ключ цены `.not_known` (FR-10: иначе «все `unknown`» обещает `delivery: no`, которого нет); `outside_diff, where: none` даёт запись только при слове (M-2 «после `go on`»); `--share` в `closing` (иначе B-1 ловит законную правку окна 2 как дефект); `stop_word` в GT; необязательные before/now в `_question_row`; `grounding_row_question` с фиксированной парой чтений; текст записей с `grounding:` и одна семья владельца; срезы по `created` (`UNCONFIRMED_SOURCE_CUTOFF`, `CELL_COUNT_CUTOFF`); порядок `check_register` G2-12 → G2-10 → G2-15; тесты ворот в `test_grounding_table.py` вместо нового `test_s3_grounding_gate.py`; выбор фикстур §4 п. 8.

**Опровержения в данных:** `t-525-fence-amendment.md` не существует (Glob `docs/**/t-525*` находит только `reviews/t-525-critic-diff-b-401-b-402.md`; контроль `t-5*` дал 19 файлов): эстафета по t-502-s1b и §5 критика. Заметка: R4 в тексте `t-1015 §L F-8 (a)` перевёрнута t-1046, текст не взят.

## 14. След чтения и не проверено

Прочитано: t-521 целиком; t-504; t-512; t-1015 целиком; t-1046 :18-89, :196-297; t-502-s1b :29-103, :256-275 + grep; t-507 :120-167, :176-189 + grep; t-514 :112-119 + grep; t-500 grep; пачка 2 :105-125. Код: `story_run.py` :8313-8352, :8405-8557, :10648-10717, :13759-13788; `controller.py` :5218-5227, :5240-5295; `contract.py` :120-149, :558-600, :966-989, :1066-1125; `base_slice.py` :465-514, :538-587; `grounding_table.py` :293-326, :1011-1193 + defs; `claim_projector.py` :80-94, :513-577 + defs, импорты; `question_register.py` :1205-1242 + defs; `check_delivery.py` :190-203, :1700-1741, :1780-1804, :1925-1980; `delivery_verdict.py` :263-337; `ledger.py` :1130-1154; `waiver.py` :196-235; `detector_verdict.py` :455-489; `planning_contract.py` :915-928; `block-names.json`. Поиски с контролем: `_append_question` (контроль `append_question_ref`, тот же вызов); `pending` в `delivery-reason-owners.json` пусто (контроль `coverage` :97, та же форма); чтение `bug:` как id: паттерн `startswith("bug|"bug:|derived_from"]|.get("derived_from`, -i, по всем `*.py`: продуктовых совпадений нет, контроль — тот же вызов нашёл `artifact_producer.py:234` и тесты.

**Не проверено, первым ходом билдера:** тело `_closes_stage` и автодописка (`:4498`) — пин §4; `s3_claim_errors` форма `who` — §4 п. 1; `severity` у `claim_question` — §7 п. 5; `traceability.not_planned_basis` как читатель формы — §4 given; `rework --stage S7` при гейте B — §8 п. 5; ветка `take_answer` общая — по критику, не перечитывал; `baseline:` как источник (сосед P20) и t-929 F-3..F-22 — не читал, вне узлов, очередь Lead; оси карты кроме 5, 17, 21 по этому потоку не обходил (AR/FR взяты из индексов и t-512).
Нужно сверх манифеста: `t-1015`, `t-1046`, `t-502-s1b`, `t-507`, `t-514`, `t-500`, `batch-2` и указанный код.

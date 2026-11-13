# Читатели блоков прогонов и перепарс (разведка скаута t-613, 13.11.2026)

База: `origin/main` 5cc4f88, `ai-packages/qa-factory/scripts/`, не-тестовые `.py`. Принято Lead по следу; отрицательное утверждение
«в `metrics_projection.py` нет ни одной проверки перепарса» перепроверено: `grep -n -i "reparse"` по файлу — 0 строк, контроль той же
командой по `finalize_task.py` — находит. Источник класса: критик кода SC6-2 (`reviews/20261113-sc6-2-code-critic.md`, B1, L1).

## Писатель: `run_suite.reparse_run_block` (`run_suite.py:734-819`)

- Та же попытка: `attempt_id` старого блока; указатели на оригинал — `reparse_of` (путь) и `supersedes_block_id`; имя файла
  `<attempt>-reparse-<hash>.json`. Копирует: время попытки, `purpose`, `dispatch_id`, `input_fingerprint`, `source_fingerprint`,
  `runtime_provenance` (или `{}`), `repo_id`.
- Теряет: `data_seed_contract` = null (`:486, 577-578, 792`), `selection_provenance` = null, `equivalence_verified` = False на блоке и
  строках, `import_provenance` не копируется, `evidence[0].summary` = "" (выведено, не прогнано).

## Общий читатель `run_history.read_run_blocks` (`run_history.py:59-121`)

Перепарс — отдельный элемент сразу после оригинала (`depth` ≥ 1, `parent`, время унаследовано). Что с ним делать, решает каждый читатель.

## Читатели: меняет ли перепарс ответ

| Читатель | Как читает | Перепарс | Вердикт |
|---|---|---|---|
| `metrics_projection` сборщик `:597-622`, A09 `:96-116` | свой glob | ЕЩЁ ОДНА job и ещё попытки; строка перепарса после зелёной помечается `duplicate_execution`; `equivalence_verified` False тянет A03/A04 (`:191,197`) | считает перепарс запуском — тот же дефект, что в `retro_numbers` |
| `retro_numbers.run_block_metrics`, `_block_launches` `:1329-1380, 1437-1469` | свой glob | запуск на файл; перепарс импортированного блока считается (нет `import_provenance`) | чинится в SC6-2 (t-597, фикс-раунд) |
| `test_repo_base.late_reasons` `:275-285` | свой glob | число блоков в тексте сообщения растёт | только текст |
| `finalize_task` reduce `:347-358, 426-436` | общий читатель + rglob | перепарс ЗАМЕНЯЕТ оригинал (та же попытка, входы, сырой отчёт) | верно |
| `acceptance._run_blocks` `:67-74, 153-180` | свой glob | второй кандидат того же совпадения, не считается | верно, пока строки не расходятся |
| `probe_by_code.author_binding` `:3942-3963` / `author_green_of` `:3966-3992` | общий | `author_green_of` на перепарсе отвечает None; у `author_binding` такой защиты нет — может привязаться к строке перепарса | несимметрично внутри файла |
| `proof_level.binding_facts` `:1765-1803`, `report_facts._person_build` `:222-258` | общий | побеждает последняя строка; `runtime_provenance` перепарса может быть `{}` и затирает прежний; докстринг `report_facts.py:224` расходится с писателем | потеря данных писателем |
| `s5_precheck` (`check_run_mapping`, `_newest_run`, `_latest_runs`) | общий | новейший побеждает — перепарс и есть лекарство; `summary` пуст → «no usable summary» | верно, кроме пустого summary |
| `interim_packet`, `window_record._terminal_runs`, `stand_gaps._c1`, `check_delivery`, `run_history` внутренние | общий | новейший побеждает / своя позиция, счёта нет | верно |
| `audit_factory.a18_board_runs_row` `:1519-1537` | свой glob имён | требует каждый файл блока в `reducer.sources`, а редьюсер замещённый оригинал туда не кладёт | возможный ложный красный, не проверено прогоном |
| `brief_pack._log_of_attempt`, `import_test_receipt.import_receipt` | по имени файла | перепарс не открывается | верно |

Тестов с «reparse» нет у: acceptance, metrics_projection, retro_numbers, interim_packet, stand_gaps, audit_factory, brief_pack,
check_delivery (по счётчику файлов; сами тесты скаут не читал).

## Класс и что из этого следует (Lead)

Класс: «перепарс — та же попытка, а не новый запуск»; читателей с собственным glob четыре (`metrics_projection`, `retro_numbers`,
`audit_factory`, `test_repo_base`) плюс `acceptance`. Кандидаты в узлы (не открыты, идут находкой в кучку):
1. `metrics_projection`: job и попытки считать по попыткам через `read_run_blocks`, перепарс не `duplicate_execution`.
2. Писатель: перепарс несёт `data_seed_contract`, `import_provenance`, `equivalence_verified`, `runtime_provenance` и `summary` оригинала.
3. `probe_by_code.author_binding`: та же защита, что у `author_green_of`.
4. `audit_factory` a18 против замещённых оригиналов — сначала один прогон-проверка.
5. Новая ось SIBLING_MAP: читатели блоков прогонов (один читатель, перепарс = та же попытка).

Не сделано скаутом: тесты не читались; `parse_trx`/`parse_junitxml` и `_classify` не прослежены.

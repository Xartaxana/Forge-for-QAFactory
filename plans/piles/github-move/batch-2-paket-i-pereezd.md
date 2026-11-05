# Переезд на GitHub — пачка 2: пакет без внутренних имён, дерево готово к выгрузке

кучка: `github-move` | статус: закрыта | взял: dev1, 05.11.2026 | ветка: `pile/github-move/batch-2` | MR: `b0b92fb86` | стенд: нужен

Правило готовности: пачка закрыта, когда каждый узел «принято», свидетели узлов — в журнале взявшего, живые доказательства (FR-33) сделаны или переданы строкой в кучку «живые прогоны».

Решения владельца: O1, O1a, O3, O5, O7; слова владельца 04.11.2026: пакет — позже; ответы FK-11, FK-13, FK-14 (спека t-1855, §12).
Порядок по общим файлам: GM2-1 → GM2-2 → GM2-3 → GM2-4; GM2-7 после GM2-2; GM2-6 до GM2-4.
Скоуп свидетеля: уточняется спекой GM2-n; полный канон — пайплайн ветки.
Общий бриф дизайнерам: НАЧАТЬ только когда `experiment/thinking-roles` слита в `main`; каждому узлу — дизайнер перед билдером, §1 спеки t-1855 несёт AR-n; §12 и §13 спеки главнее её разделов.

## Бриф

Берётся сразу после слияния MR пачки 1 (слово владельца 05.11.2026: t-1765 — эксперимент, в `main` не вливается; переезжает `main` как есть, ветка эксперимента переезжает отдельно, позже, тем же инструментом — спека t-1855 §12). После GM2-1 релиз в старый репозиторий не делается (манифесты уже с новым именем).

## Узлы

Исполнитель «designer → builder → critic» — кодовый узел; «builder» — узел-документ. Статусы:
`ожидает` → `в работе` → `сдано` → `принято` / `отклонено`.

| Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус |
|---|---|---|---|---|---|---|
| GM2-1 | П1 | GM2-1: LICENSE Apache-2.0, манифесты, маркетплейс `qafactory`, URL установки, `.claude/settings.json` | designer → builder → critic | `ai-packages/qa-factory/LICENSE`, `ai-packages/qa-factory/INSTALL.md`, `ai-packages/qa-factory/UPGRADE.md`, `ai-packages/qa-factory/README.md`, `.claude/settings.json` | MR пачки 1 (t-1765 не вливается, слово владельца 05.11.2026) | принято |
| GM2-2 | П1 | GM2-2: обезличивание по O7, карта соответствия рядом с бандлом, не в git | designer → builder → critic | `ai-packages/qa-factory/` | GM2-1 | принято |
| GM2-3 | П1 | GM2-3: PROJECT.md, RUNBOOK, README, CURRENT_CONTEXT, DECISIONS, BOOT, имена людей, `kb/` обезличен, `kb_publish` удалён | designer → builder | `PROJECT.md`, `docs/RUNBOOK.md`, `README.md`, `CURRENT_CONTEXT.md`, `DECISIONS.md`, `BOOT.md`, `kb/`, `tools/kb_publish.py`, `tools/tests/test_kb_publish.py` | GM2-2 | принято |
| GM2-4 | П1 | GM2-4: отбор по O3, журнал не едет, читатели проверены на дереве без него, `cutover.json` дополнен | designer → builder → critic | `docs/migration/cutover.json` | GM2-3, GM2-6 | принято |
| GM2-5 | П2 | GM2-5: `controller-blocks-gen.py` без внутренних имён | builder → critic | `tools/controller-blocks-gen.py` | MR пачки 1 (t-1765 не вливается, слово владельца 05.11.2026) | принято |
| GM2-6 | П1 | GM2-6: измерители под новым именем `experiments/measurers/` | designer → builder → critic | `experiments/measurers/`, `experiments/measurers/`, `tools/test_dev_config.py`, `docs/SIBLING_MAP.md` | MR пачки 1 (t-1765 не вливается, слово владельца 05.11.2026) | принято |
| GM2-7 | П1 | GM2-7: корпус `investigation-14857` и `TP1-13877` заменён синтетикой той же формы, снимки сгенерированы | designer → builder → critic | `ai-packages/qa-factory/scripts/tests/fixtures/` | GM2-2 | принято |

## Ход

- 05.11, ночь (Fable): пачка взята сразу после слияния MR пачки 1 (`1e8cd2c1b`, слово владельца: t-1765 не вливается). Дизайнеры запущены параллельно на GM2-1 (t-1903), GM2-2 (t-1904), GM2-6 (t-1905), GM2-7 (t-1906); GM2-5 ждёт карту O7 из GM2-2 (единственная строка `controller-blocks-gen.py:450` несёт ключ); GM2-3 и GM2-4 — после GM2-2. Направление GM2-2 выбрано Lead: обезличивание — повторяемый инструмент в `docs/migration/` с картой рядом с бандлом, потому что ветку эксперимента владелец велела перевезти позже тем же инструментом.
- 05.11, ~03:15 (Fable): GM2-1 слит (t-1909; критик — одним проходом с GM2-2), правки Lead (P16 оба ключа `false`, SIBLING_MAP:75, правила сканера FK-D). GM2-6 принят: R1 t-1908, R2 t-1911, критик t-1913 `fit_with_fixes`, фикс t-1914 (test_measurers 297/297 и 304/304 с таблицей, test_prepare_copy 48/48, сканер по `experiments/measurers` 0); «Пишет в» дописан двумя файлами, найденными дизайнером (`test_dev_config.py` запускает `paths.py`; ось 6 карты). В работе: GM2-2 (t-1910).
- 05.11, ~05:35 (Fable): GM2-1 и GM2-2 приняты — критик t-1916 (fit_with_fixes, 2 блокера) закрыт фикс-раундом t-1919 (install-smoke PASSED, ticket_light 281/281, GA-7/DG-7 зелёные; карта O7 80 строк вне git). GM2-5 принят (t-1917, critic skipped: две строки генератора). GM2-7 слит (t-1918), критик t-1920 в работе. GM2-3 — билдер t-1923 по спеке t-1921. GM2-4 — спека t-1922 принята, билдер последним (подузлы GM2-4b, GM2-7b). Правила сканера Lead: lookaround'ы вместо `exclude`, allow-листы, собственные префиксы id. Канон 8036434 на `8378261e0`.
- 05.11, ~12:40 (Fable): **GM2-4 принято** — четыре раунда билдера (t-1929 часть 1 `423c5807d`, t-1930 часть 2 `4f3d2f886`, t-1932 и t-1933 фикс-раунды `d3236bc4e`), критик t-1931 (`fit_with_fixes`, блокер F1 и F2–F12 закрыты в t-1933, остатков нет). Итог: `cutover.json` (delete 1416 поимённо, travels 61, `sweep` исполняется экспортом), карта O7 109 строк вне git, фикстуры `investigation-14857`/`run-12586-*` синтетика одним писателем, `test_journal_fresh_clone` (J1–J10), сканер: экспорт `total: 1` — старый id плагина в `.claude/settings.json` (снимается перед D2). Слово владельца 05.11: оба репозитория GitHub уже созданы и публичные (O4). Все узлы принято; канон — пайплайн ветки на `d3236bc4e`+.
- 05.11, ~13:05 (Fable): **BATCH CANON** — пайплайн 8039190 на `cdddfbbfd`: `forge-check` success (7553 passed, 21 skipped; lint/dup 0 new), `install-smoke` success, `package-fast` красный только унаследованным `test_stage_joints` (103/111, якорь «Witness», красный и на `main`), `package-full` 1/2 `349/357 ok`, 2/2 `315/324 ok` — на `main` до пачки 349/357 и 314/324: красных не прибавилось (на один меньше). Пачка готова к MR в `main`.

## Живые доказательства

| Что | Стенд / проект | Кто | Статус |
|---|---|---|---|
| Сухой прогон `cutover-dry-run` на GitLab: зелёный `forge-check` — условие D2 | ветка CI | Lead | сделано: 8039897 \| note: пайплайн CI на ветке `cutover-dry-run` (экспорт с `main` `e5daadf61`+ плюс четыре файла GitLab CI): `forge-check` success 7383 passed 28 skipped, `install-smoke` success, `package-fast` только унаследованный `test_stage_joints` 103/111; первый прогон 8039619 был красным на `test_forge_metrics` (2 теста читали журнал этого репозитория) — починено `e5daadf61`, defect_found ref t-1933 |
| Живой прогон на стенде O8 после переезда (FR-33) | MyBooks | Lead | перенос: live-runs/findings/20261105-github-move-2-zhivoj-progon-mybooks-posle-pereezda.md \| обоснование: прогон возможен только после шага D2 — пуша дерева экспорта в GitHub командой владельца — и D3; строка стоит в «Живых доказательствах» live-runs/2 \| подтвердил: владелец, 05.11.2026 |

## Остатки


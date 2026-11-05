# `manifest_put`: строка `unresolved` с `thens` без `instance_ids` читается «весь кейс» и молча стирает `tests[]` кейса — дважды за прогон, 4 лишних диспатча

id: — | кучка: `execution-probes` | от: прогон CART-1 (MyBooks), 31.10.2026 (свод `experiments/mybooks/cart-1-run-problems.md`, п. 5.7) | приоритет: П2 | кандидат наверх: нет

## Что наблюдалось

Отчёты `docs/tasks/specs/reports/t-1632-cart1-run-problems-artifacts.md` (строка 29; `EV:86, 94`; `A/work/digests/S5-qa-automator-6.txt` «Cause of the missing row»,
`S5-qa-code-critic-4.txt`…`-6.txt`) и `t-1633-…-transcript.md` (п. 27, 10:21–10:33 UTC):
- красный TC_009 (`contradicts_requirement`, Then 2) выпал из манифеста: повторная отправка строки `unresolved` через `manifest_put.py` заменила срез кейса и удалила
  строку `tests[]` TC_009 — **дважды**. Порядок «сначала unresolved, потом tests[]» работал; обратный стирал.
- Следствия: `window_record.py` отказал `empty_scope`; критик-4 и критик-5 — `checkpoint incomplete`; 6 кругов (автор-4/5/6, критик-4/5/6), 4 лишних диспатча,
  ≈ 13 мин. Дирижёр обошёл колпак механических раундов («mechanical pass 2 … the cap is 1»), переквалифицировав причину в `test_defect`; критик-6 для сборки
  квитанции сам заменил `critic_verdict: unverified` на `approved` через `manifest_put`.

Причина в коде (проверено 31.10.2026, `ai-packages/qa-factory/scripts/manifest_put.py`): `_merge` (~1228) считает `drop_from_tests = _whole_case(incoming_unresolved, …)`;
`_whole_case` берёт строки, у которых нет среза (`_partition_scoped(entry)` ложна); `_partition_scoped` (~276) смотрит на `contract.UNRESOLVED_SLICE_KEYS` (экземпляры и
партиции), а строку, называющую только `thens`, **по комментарию в коде считает «всей»** («`thens` is not one of them (a row that names only Thens is the whole case's)»);
затем на ~1314 `_moved_out(entry, drop_from_tests)` удаляет строки `tests[]`, чьи кейсы целиком «ушли» в unresolved, и считает их `summary["moved"]`. Строка TC_009
называет Then 2 (красный), но не называет `instance_ids` → «весь кейс» → стёрт тест, который РАБОТАЛ и красный только по одному Then (остальные зелёные). Не проверено на самом манифесте CART-1
(`A/work/automation-manifest.json` в момент ошибки): что у строки TC_009 не было `instance_ids` — это следует из описания в digest автора-6, не из прочитанного манифеста.
Сама строка «заменить срез» (`_replace_contradicts_slice`, ~329) — другая функция и стирание не делает.

## Класс

Инструмент записи молча удаляет данные другого носителя (`tests[]`) по следствию, названному только в комментарии кода, а порядок вызовов — скрытое условие корректности
(FR-41 — неизвестное не выдаётся за факт; FR-1 — отказ/предупреждение называет, чего ждал; AR-14 — одна запись, один писатель; AR-23 — пустой исход объявлен). Потеря видна
на следующем гейте, а не в момент записи.

## Что именно менять

Направление выбрано: потеря не молчит, и «строка про Then» не стирает прогнанный тест. Ошибка допустимого направления — оставить `tests[]` (лишняя строка дешевле потерянной).

1. **Вывод `manifest_put.py` называет каждое перемещение (`summary["moved"]` → строки в выводе).** Всякий раз, когда `tests[]` строка ушла из-за `unresolved` строки: «moved out of tests[]:
   <instance_id> (case <TC> is now wholly unresolved because the row names no `instance_ids`/`partitions`; if the row is about particular Thens, name the instances it blocks:
   `instance_ids: [...]`)». Тест: фикстура «tests[] TC_009 + unresolved TC_009 без срезов» → вывод содержит `moved out` и дверь; сумма `moved` равна числу строк в выводе.
2. **`_partition_scoped`/`_whole_case`: строка `reason: contradicts_requirement` с непустым `thens`, у кейса которой есть `tests[]` строка с прогнанным экземпляром
   (`status` green/red, не `blocked_by_env`), — срез, а не «весь кейс»** (`tests[]` не стирается). Строка `blocked_by_env` и строка без `thens` — как сегодня (инвариант, который код
   защищает: кейс не бывает одновременно «целиком доказан» и «целиком не решён»; здесь он и не нарушен: красный Then один, остальные привязаны). Крайние входы (тесты на каждый):
   `thens` перечисляет ВСЕ Then кейса → «весь кейс», как сегодня (зелёных Then, которые стирание потеряло бы, нет; п. 1 всё равно называет перемещение); `thens: []` или `""` → «весь кейс»; `thens` + `instance_ids` → срез по `UNRESOLVED_SLICE_KEYS`, как сегодня; одна и та же строка отправлена дважды — второй вызов не меняет ни байта
   (идемпотентность); порядок «tests[] → unresolved» и «unresolved → tests[]» дают один манифест (проверка тестом на перестановку).
3. **Один писатель поля `critic_verdict` и квитанция для `unverified`.** Критик, меняющий `unverified` на `approved` ради сборки квитанции, обходит ворота; узел проверяет, что квитанция
   окна строится и для строк `unverified (tooling)` (дверь есть), и тест фиксирует: `critic_verdict` меняет только роль-критик своим вызовом, значение `approved` при `unverified`-причине
   «tooling» отказывается с дверью (место — `_merged_critic_fields`, ~942; **не проверено**, законна ли замена в этой цепочке; до проверки в узел входит только тест-констатация). Согласовать с
   `driver-controller/findings/20261030-otkaz-kritika-okna-s5-quittanciya-i-vozvrat-avtoru-ostatki.md`.

Тесты (по одному на пункт): `scripts/tests/test_manifest_put*.py` (имя уточнить по коду). Живое доказательство (FR-33): окно S5 с красным Then в мягком тесте, строка unresolved
отправляется до и после tests[] — строка TC остаётся.

## Принципы и правила

P1, P22; FR-1, FR-18, FR-41, FR-59; AR-14, AR-23, AR-25.

Связи: `driver-controller/findings/20261030-kap-remonta-s5-schitaet-raundy-bez-test-defect.md` (колпак механических раундов; переквалификация причины дирижёром — тот же сюжет, другой
узел), `codex/findings/20261020-dev2-addendum-s5-blockers-62710646-3fa8783e.md` (родственное по отчёту t-1632), EP1-18 (поля строки манифеста), EP1-38 (`s5_precheck` читает тот же манифест).

Решение владельца нужно: нет.

## Повтор LOCAL-1 (02.11.2026)

Прогон LOCAL-1 (t-1672 П-9): повторная отправка `manifest_put.py` стёрла `then_bindings` прошлых окон (TC_007–009). EP1-39 («принято, слито 0.10.8») — регрессия/не починено: узел RN1-22 (`release-next/findings/20261102-manifest-put-stiraet-then-bindings-povtor-ep1-39.md`).

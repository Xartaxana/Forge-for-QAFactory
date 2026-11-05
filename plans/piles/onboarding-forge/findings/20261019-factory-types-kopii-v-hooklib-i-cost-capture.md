# Множество «фабричных» видов активности записано литералом в четырёх местах рядом с `activity_capture.TYPES`

id: — | кучка: `onboarding-forge` | от: Lead пачки (кучка `collect`), 19.10.2026 | приоритет: П2 | кандидат наверх: нет

Что не так: «это фабричная работа» — множество видов активности `doctor`, `onboarding`, `story` (на дашборде ещё
`environment-maintenance`) — записано литералом в четырёх местах, а не прочитано из одного:
`scripts/hooklib.py:1227` (`session_has_factory_activity`), `scripts/cost_capture.py:1482` (`likely_factory` в `_capture`),
`scripts/cost_capture.py:1772` (`has_factory_activity`), `scripts/dashboard_cost_groups.py:84` (подпись группы расхода) —
рядом с `activity_capture.TYPES` (`activity_capture.py:14`). Когда скилл `qa-collect` добавит вид `collect`, расход скилла не
попадёт ни в одно из этих множеств: на дашборде он покажется строкой `Unclassified` (P18: цена задачи включает всё потраченное
на неё), а `has_factory_activity` для него останется «нет».

Что сделать: узел CL1-4 кучки `collect` заводит ОДНО множество `FACTORY_TYPES` в `activity_capture` (`TYPES` остаётся
псевдонимом) и читает его в `dashboard_cost_groups.py` (оба файла у него в «Пишет в»). Два горячих файла остаются за этой
кучкой: `hooklib.py` и `cost_capture.py` читают то же одно множество вместо своих литералов. До этого узла расход скилла на
дашборде — `Unclassified`, и это явный пробел, не ошибка (остаток в «Остатках» пачки `collect`).

Свидетель: `grep -n '"doctor", "onboarding", "story"' ai-packages/qa-factory/scripts/hooklib.py ai-packages/qa-factory/scripts/cost_capture.py`
(строки 1227, 1482, 1772); `dashboard_cost_groups.py:84`; критик t-972 F-5, спека `docs/tasks/specs/t-962-collect-skill.md` §L-2 (F-5).

Принципы и правила: P18 (цена одна и истинная, весь расход на задачу), P12 (новый код проверяется на похожие места), FR-17
(инструмент, заведённый под проблему, подключён везде, где она встречается), FR-54 (правка находит соседей по карте).

Решение владельца нужно: нет.

<!-- id выдаёт интегратор при сборке пачки (следующий свободный B-nnn на main); находка, перенесённая из
BACKLOG.md при заморозке, несёт свой старый id. Имя файла: yyyymmdd-<slug>.md. -->

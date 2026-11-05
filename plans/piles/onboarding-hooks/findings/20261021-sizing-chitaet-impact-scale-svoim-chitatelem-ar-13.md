# `sizing.py` читает `config.impact_scale` своим читателем (`impact_scale_of`), а не через `grammar.impact_scale` — второй читатель одного факта (AR-13)

id: — | кучка: `onboarding-hooks` | от: Lead, 21.10 (приёмка OH2-2(б)/OH2-6(а), t-1184 §3 F-7; критик t-1201 Q5, Q11) | приоритет: П3 | кандидат наверх: нет

Что не так / что сделать: `grammar.impact_scale` — читатель шкалы влияния пакета (`validate_artifacts.py` читает только через него:
VA:387, :488, :645, :1452). `scripts/sizing.py` держит свой `impact_scale_of` (SZ:165-167) и в `classify_requirement` читает карту
классов сам; OH2-6 (а) починил падение на не-словаре (строка/число/null → P2 по умолчанию и именованная заметка), но читателя не свёл:
два читателя одного факта с разной обработкой краёв (AR-13 «факт с функцией-читателем читается только через неё»). Край, который
остался молчаливым (Q5 критика): запись карты с отсутствующим или не-ярусным `priority` (`{}`, `{"severity": "minor"}`) становится
P2 без заметки (SZ:478-481). Сделать: `sizing.py` читает шкалу через `grammar.impact_scale` (один читатель, одни края); отсутствующий
или не-ярусный `priority` → та же именованная заметка, что у не-словаря (OH2-6 (а) K6a); пины в `test_sizing.py` (K6a-5: `{"degraded":
{"severity": "minor"}}` → заметка, вес 1.0). `architecture.md:205` цитирует SZ «:478 weight bump unavailable» — строка устарела (Q7),
правится тем же узлом.

Свидетель: `docs/tasks/specs/t-1184-oh2-risk-area-readers.md` §3 «AR-13: SZ keeps its own impact_scale reader … stated, not reworded:
F-7»; обзор `docs/tasks/specs/reviews/t-1201-oh2-topic-a-b-c.md` §6 «AR-13 is not kept for impact_scale», Q5, Q7, Q11; хэндофф
`docs/tasks/handoffs/t-1196-oh2-2b-oh2-6a.md`. Контроль: `grep -n "impact_scale_of\|grammar.impact_scale" scripts/sizing.py
scripts/validate_artifacts.py` — SZ только свой, VA только grammar.

Принципы и правила: P10, P12; FR-17, FR-54; AR-13, AR-28; D-0055.

Решение владельца нужно: нет (техническое).

# Маркер `[DEFERRED: application repo paths]` в P4 не имеет команды `add` — отложенное решение без строки реестра

id: — | кучка: `onboarding-forge` | от: Lead, 21.10 (приёмка OH2-1, t-1184 §2 F-3; критик t-1201 Q12) | приоритет: П3 | кандидат наверх: нет

Что не так / что сделать: фаза `skills/qa-onboarding/phases/p4-generate.md` (:298 на HEAD) оставляет в стратегии маркер
`[DEFERRED: application repo paths]`, но ни один шаг фазы не пишет для него строку таблицы отложенных решений
(`project_decisions.py … add --field-ref … --essence "application repo paths…"`): маркер есть, записи нет, и A13 (OH2-1: сверка
маркеров с рядами по ячейкам) видит его как непарный. Статический тест `test_onboarding_markers.py` держит его в таблице
исключений `EXCEPTIONS` с причиной «finding, the Lead» — интегратор при слиянии OH2-1 вписал туда путь этой находки; исключение
устаревает (тест краснеет), как только маркер получит пару или уйдёт из фазы. Сделать: шаг P4 рядом с маркером получает команду
`add` той же формы, что строка risk areas (P4:526-528; `--field-ref`, `--essence` начинается с «application repo paths», `--asked`);
или маркер снимается, если отложенного решения в этой точке больше нет (решает дизайнер P4 по смыслу шага); строка `EXCEPTIONS`
удаляется тем же коммитом (K2-2 иначе ловит устаревшее исключение). Соседи: маркер `impact scale not set` (P4:333) — узел OH2-6 (б);
`add` без `--essence` на P4:251 (`required=True` в PD:451 — argparse откажет; критик t-1201 Q1) — тот же узел или свой.

Свидетель: `docs/tasks/specs/t-1184-oh2-risk-area-readers.md` §2 (таблица исключений: «`application repo paths` → F-3»),
хэндофф `docs/tasks/handoffs/t-1192-oh2-1-oh2-4.md`; обзор `docs/tasks/specs/reviews/t-1201-oh2-topic-a-b-c.md` Q1, Q12;
`ai-packages/qa-factory/scripts/tests/test_onboarding_markers.py` (`EXCEPTIONS`, :38-40). Контроль: `grep -n "application repo paths"`
по `skills/qa-onboarding/phases/*.md` находит P4:298; тот же grep по `add --field-ref` в P4 находит только строку risk areas.

Принципы и правила: P4 (собранное едет дальше в YAML/реестре), P22; FR-11, FR-23, FR-38; AR-22, AR-28; D-0044.

Решение владельца нужно: нет (техническое).

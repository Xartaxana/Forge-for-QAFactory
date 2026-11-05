# Вопросы `build_check` (`stand_identity`, пять вариантов текста) задаются без цен

id: — | кучка: `driver-hosts` | от: Lead, 21.10 (приёмка C1-6a, t-699 §9 F10 (a), §10) | приоритет: П3 | кандидат наверх: нет

Что не так / что сделать: `build_check` (`story_run.py`, три места — SR:6510, :6632, :6708 на базе спеки) задаёт человеку
закрытые вопросы, чьи тексты — данные (пять вариантов `stand_identity`), с исполнителями, но без ценовой секции: человек
выбирает «подтвердить стенд / сменить / идти дальше», не видя, что стоит каждый вариант для фабрики, для него и для
доставки (P22: «с ценой и последствиями по каждому варианту»). C1-6 дал цены всем вопросам S6–S9 и доставки
(`question-prices.json` `s6.*`, `s8.*`, `closed.held`), а эти пять вариантов остались общими с S5 (тот же `build_check` на входе
S5 и S6) и вынесены в очередь (F10 (a): ~150 строк, пять строк данных). Сделать: ключи `s5.build_check.<variant>` (или один ключ
с пятью рядами) в `question-prices.json`, текст через `closed_question`, как у `s6.stand_confirm` (C1-6b) — один узел, после
слияния C1-6b (одна форма для `stand_check` и `build_check`, оси SIBLING_MAP «One question for every stop»).

Свидетель: `docs/tasks/specs/t-699-c1-6-s6-s9-delivery.md` §2 R8, §9 F10, §10 «F10 (a), F12 (a) — findings … written by the
Lead at acceptance of C1-6a»; `ai-packages/qa-factory/scripts/story_run.py` `build_check` (`grep -n "def build_check"`);
`references/question-prices.json` — ключей `build_check` нет (контроль: `grep -n "stand_confirm\|closed.held"` находит).

Принципы и правила: P22, P9; FR-6, FR-13; AR-16; D-0039.

Решение владельца нужно: нет (техническое).

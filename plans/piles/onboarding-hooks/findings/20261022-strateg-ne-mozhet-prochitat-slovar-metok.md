# Стратег S3 (окно 1, разметка) послан за метками в `handoffs/vocabulary.yaml` плагина, а гард роли чтение плагина запрещает — роль вернула «impossible», дирижёр носил списки руками

id: — | кучка: `onboarding-hooks` | от: владелец, 22.10.2026 (прогон TP1-12586 на `testproject1-dev-010`, 0.10.0) | приоритет: П1 | кандидат наверх: нет

перенос: hotfix-12586/batch-1 (узел HF1-6; слово владельца 23.10.2026 — срочная отдельная пачка; узел OH3-14 здесь закрывается её хэшем)

Что не так: `skills/qa-story/phases/s3.md:25-27` велит дирижёру сказать стратегу, что метки — `grounding_labels`, а состояния
требований — `requirement_grounding_states` «of `handoffs/vocabulary.yaml`». Бриф `work/briefs/S3-qa-test-strategist-1.md` самих списков
не несёт. Стратег (транскрипт `…/e0be59d0-…/subagents/agent-a64820fce81a7a9fd.jsonl`) поискал файл в `work/handoffs/`, нашёл его в
плагине и получил от `guard_pre_tool.py`: «Read inside the plugin is refused for a role … The brief carries the commands». Бриф их не
нёс — роль закрыла окно `SubagentHandback` «impossible: the label vocabulary is unreachable», `grounding.yaml` пуст. Дирижёр вытащил
два списка сам и переслал — окно разметки перезапущено, лишний диспатч и лишние деньги на каждом прогоне.

Почему это дефект: гард прав (P14, AR-11), неправ носитель: путь к данным, нужным роли, назван, а данные не выданы (FR-15, AR-8, AR-10 —
требование проверки доходит до роли до работы, в её полях). Отказ гарда обещает «бриф несёт» то, чего бриф не несёт (FR-2: дверь, которой
получатель не может воспользоваться).

Что сделать: (1) `brief_pack.py` для окна разметки S3 вкладывает в бриф оба закрытых списка из `vocabulary.yaml` (читатель
`handoff.options_for_role` / `role_digest.py`, не свой парсер — AR-13); (2) `s3.md` перестаёт посылать роль в файл плагина и говорит
«списки — в брифе»; (3) тест: бриф окна 1 содержит каждое слово `grounding_labels` и `requirement_grounding_states`; (4) свип по карте:
все места `phases/*.md`, агентов и форм, где роли сказано «of `handoffs/vocabulary.yaml`» (`<one of vocabulary.…>` в формах `handoffs/` —
форма заполняется, её закрытые списки должны быть в форме или брифе), — по каждому вердикт «выдано / не выдано».

Свидетель: транскрипт стратега (Grep в `work/handoffs/vocabulary.yaml` → нет; Read плагина → отказ гарда; SubagentHandback «impossible»);
сообщение дирижёра владельцу 22.10 («its guard blocks it from reading the label vocabulary … I pulled the two word lists … and sent them»);
`skills/qa-story/phases/s3.md:25-27`.

Принципы и правила: FR-15, FR-2, FR-38, AR-8, AR-10, AR-13, P14.

Решение владельца нужно: нет.

## Повтор 29.10.2026 (прогон 14857, S5)

Прогон TP1-14857 на 0.10.5, `testproject1-dev-010`, S5 план, 20:54 (UTC); разбор t-1583. Проверяющий плана автоматора: `REJECT - 18 finding(s)`
(`data` и `assert` пусты), затем ещё три: `data '...' is not one of own, run_tag, seeded`. Закрытый словарь поля `data`
(`vocabulary.yaml`, `data_strategies: [own, run_tag, seeded]`) дошёл до роли только через отказ. Прежний фикс S3
(`brief_pack.s3_labelling_vocabulary_lines`, `brief_pack.py:1446`) нёс только слова разметки S3. Роль починила себя за два круга (~1 мин).

Класс шире S3: каждое поле контракта, которое проверяется по закрытому списку `handoffs/vocabulary.yaml`, получает слова в бриф до работы —
одним механизмом для всех ролей (FR-38, AR-10); частный фикс S3 (`s3_labelling_vocabulary_lines`) — первый экземпляр.

Решение владельца нужно: нет (решение Lead, П1 0.10.7).

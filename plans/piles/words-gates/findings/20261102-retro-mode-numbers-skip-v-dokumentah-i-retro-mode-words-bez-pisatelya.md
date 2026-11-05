# Документы и контракты всё ещё называют `retro_mode numbers|skip` текущими режимами; у `retro_mode_words` нет писателя

id: — | кучка: `words-gates` | от: критик t-738 (GW1-3, m-2, F-3 спеки t-700, B-2), 02.11.2026 | приоритет: П2 | кандидат наверх: нет

## Что наблюдалось

GW1-3 (`release-next/1`) сделал ретро всегда полным: `stage_done.py --set retro_mode=numbers|skip` отказывается, допустимо только `full`. Прежние режимы остались текущими в носителях, которых узел не трогал (F-3 спеки — «развёртка», строки очереди нигде не было: поиск `F-3|s8-scribe-to-gate-b|retro_mode_words` по `plans/piles/release-next/batch-1-release-0-10-9.md` пуст, контроль `GW1-3` попадает в строку :27):

- `handoffs/vocabulary.yaml:260`, `handoffs/s9-retro-to-project.yaml:44`, `handoffs/gate-b-to-delivery.yaml:93-96` (всё ещё `recorded_by: "stage_done.py --set retro_mode=<value>"`);
- `references/artifact-contract-json.md:55` («written at gate B»), `references/artifact-contract-results.md:68` и срез `:10`, `design/driver.md:306`;
- мимо списка спеки (найдено критиком): `references/templates/retro.md:6-9` («`numbers` (asked for by name …), `skip` (asked for by name …)» — читает аналитик), `handoffs/README.md:58`, `handoffs/index.yaml:64` («authorises … `retro_mode`»);
- `retro_mode_words`: читается `story_run.py:12927` и `report_facts.py:1913`, писателя нет (предшествует GW1-3, GW1-3 писателей не убирал).

Читатели значения для СТАРОЙ стори остаются законными (`story_run.py:12925-12927, 13007, 14853, 16854`; `report_facts.py:1912-1913`; `retro_numbers.py:2388-2852`, в том числе `:2530` «asked for by name (`retro_mode: numbers`)» — верно для старой стори): их не трогать.

Из тех же вердиктов B-2: Lead принял «F-6 = рекомендации» — (i) `handoffs/s8-scribe-to-gate-b.yaml:111` заполнитель `"<stated plainly, with the waiver command its fix prints>"` получает формулировку C7 (та же фраза, которую C7 убрал из `s8.md:118`); (ii) одно предложение в `s8.md` для дороги навыка («where no driver runs, you record each such line with the same `waiver.py` call»): `s8.md:184-185` всё ещё говорит «The answer is recorded by the driver from the person's line». Ни то ни другое не сделано и не стоит в очереди.

## Класс

Сменили смысл поля — прочитать всех, кто описывает его старое значение (FR-37; AR-19, AR-22, AR-24): документ называет режим, который код уже не принимает.

## Что именно менять

Направление выбрано (Lead пачки release-next/1, 02.11.2026): текст документов — строка на строку, поведение кода не меняется.

1. Файлы из списка выше (все девять + три мимо списка): везде, где режим назван ТЕКУЩИМ, — «`full` always; `numbers` and `skip` are read only for stories recorded before 0.10.9». Тест: один ключ `scripts/tests/test_retro_always_full.py` — поиск `retro_mode: numbers|skip|retro_mode=<value>` по `handoffs/`, `references/`, `skills/`, `design/` вне тестов не находит текущего описания (допустимая строка содержит «recorded before»); положительный контроль — сам файл `stage_done.py:81`.
2. `retro_mode_words`: решение Lead до узла — (а) рекомендация: читатели `story_run.py:12927` и `report_facts.py:1913` остаются для старых стори, писатель не создаётся, поле в `handoffs/*.yaml` помечается «legacy, no writer»; (б) удалить читателей. Узел исполним по (а). Тест (а): строка «legacy, no writer» присутствует.
3. B-2 (i): `handoffs/s8-scribe-to-gate-b.yaml:111` — формулировка C7. B-2 (ii): одно предложение в `skills/qa-story/phases/s8.md:184-185` для дороги навыка. Тест: по ключу присутствия на каждую из двух строк.

## Принципы и правила

FR-37; AR-19, AR-22, AR-24.

## Связи

- `docs/tasks/specs/reviews/t-738-gw1-3-diff-critic.md` (B-2, m-2); `docs/tasks/specs/t-700-gw1-3-gate-b-words.md` (F-3, F-6); `docs/tasks/specs/t-745-c2-8-code-close.md:480-492` (развилка d опирается на носитель `retro_mode_words`).

Решение владельца нужно: нет.

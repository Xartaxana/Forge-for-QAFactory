# Очередь CL3-9: вложенность `_l_records`, три отображения (stalled, looped) в слова, `loop_ignored` без читателя, раунды окна без носителя, страница КБ про «зависшие»

id: — | кучка: `collect` | от: критики t-725 (CL3-9: m-1, m-4, m-5), билдер t-737, 02.11.2026 | приоритет: П3 | кандидат наверх: нет

## Что наблюдалось

CL3-9 (`release-next/1`): сборщик упаковывает транскрипты и историй с петлями (`collect_stall.py`, `collect_pack.py`, `collect_intake.py`). Принятое, но не сделанное:

- **m-4.** `collect_stall._l_records` (`:337-376`) глубиной 4 уровня (по правке t-737; было 5): цикл по строкам таблицы → цикл по записям → ветка формы → цикл → условие. Расщепление по одной функции на форму не сделано.
- **m-5.** Три отдельных отображения пары (`stalled`, `looped`) в слова: `collect_stall.select_transcripts` (`:492`), `collect_pack._pack_transcripts` (`:1129`), `collect_intake.stall_elements` (`:678`). Тексты продиктованы спекой (C-6, C-9, C-10), дефекта сборки нет; кандидат на схождение. Там же: `loop_ignored` не имеет производственного читателя (как и прежний `ignored`, AR-22).
- **m-1 (остаток B-6).** Окно, упёршееся в капы `cap`/`same_set` и закрывшееся, не оставляет долговечного носителя: вопрос задаётся `no_move(kind="refusal", why="threshold")` (`story_run.py:5694`), строка `driver-questions.jsonl` имеет вид `refusal`, как любой отказ; `driver-runs.jsonl` строки `no_move` не пишет; `conductor.jsonl` несёт лишь слова (читать их запрещено FR-12). Ловится только через L1/L5(а). Нужна строка журнала драйвера вида `window_round` с исходом.
- **Страница КБ.** `kb/04-onboarding-doctor.xhtml:417` по-прежнему говорит «stalled stories»: верно для половины сборки (теперь «stalled or looped»); найдено поиском `stalled stor|stalled story` вне `docs/tasks` (спека t-625 оставила Lead).

## Класс

Устаревший текст и недоразложенные копии после расширения предиката (AR-13, AR-22, AR-28; FR-37): «зависшие» стало «зависшие или зацикленные», а часть читателей и носителей осталась на старом слове; evidence, которое драйвер убирает, не имеет носителя.

## Что именно менять

Направление выбрано (Lead пачки release-next/1, 02.11.2026).

1. `scripts/collect_stall.py`, `_l_records`: по одной функции на форму (`_l_series`, `_l_records_flat`, `_l_nested`), каждая возвращает причины; вложенность ≤ 3. Тест: существующий `test_collect_stall.py` (316 проверок) без правки ожиданий.
2. Одна функция `contract`-стиля «слова пары»: `collect_stall.loop_words(stalled, looped) -> str` (`"stalled"`, `"looped"`, `"stalled and looped"`, `"neither"`); три места зовут её; тексты спеки (C-6, C-9, C-10) сохраняются побайтно. Тест: три существующих теста без правки + таблица 4 пар (T/T, T/F, F/T, F/F, None).
3. `loop_ignored`: производственный читатель — строка в `collect_intake.stall_elements` «ignored loop items: N»; либо удалить поле (решение Lead; рекомендация — читатель, чтобы утерянные пункты не пропадали молча). Тест: манифест с `loop_ignored: 2` → строка с 2.
4. `scripts/story_run.py` (драйвер; непересекающиеся функции, D-0048): при закрытии окна с капом пишется строка `driver-runs.jsonl` `{kind: "window_round", outcome: cap|same_set|continue, key, round}`; читатель — `collect_stall` L2 как носитель (это закрывает остаток B-6). Тест: `test_story_run_repair_limit.py` — раунд до капа → строка; закрытие окна после капа → строка `cap` остаётся. Пишет её драйвер-узел `driver-controller` (`перенос: driver-controller/…` не нужен: узел стоит здесь, `owns` называет файл).
5. `kb/04-onboarding-doctor.xhtml:417`: «stalled stories» → «stalled or looped stories». Страницы КБ публикуются по-английски. Тест: ключ присутствия в `test_kb_*` (если такого нет — строка в отчёте узла).

## Принципы и правила

FR-12, FR-37; AR-13, AR-22, AR-28.

## Связи

- `docs/tasks/specs/reviews/t-725-cl3-9-diff-critic.md` (m-1, m-4, m-5); `docs/tasks/handoffs/t-737-cl3-9-fix.md`; `docs/tasks/specs/t-625-cl3-9-collect-looped-transcripts.md`.

Решение владельца нужно: нет.

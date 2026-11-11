# Релиз 0.11.0 — пачка 2: один баг и его проявления (сделано) и три хвоста критика

кучка: `release-next` | статус: ожидает | взял: — | ветка: — | MR: — | стенд: нужен только для N9 (живое доказательство, ждёт слова владельца) | приоритет: П1

Открыта 10.11.2026 по спеке t-2187 (`docs/tasks/specs/t-2187-one-bug-many-manifestations.md`): пачка 1 закрыта, новая находка кучки легла в следующую (D-0044). Узлы RN2-1…RN2-8 сделаны и слиты в `experiment/thinking-roles` (`4a6ce9335`) до открытия пачки; три хвоста критика (RN2-9…RN2-11) сделаны 10.11.2026 и слиты туда же (`fcc08e09e`); в пачке остаётся только живое доказательство N9.

Правило готовности: пачка закрыта, когда каждый узел «принято», свидетели узлов — в журнале взявшего, живое доказательство (FR-33) сделано или передано строкой в кучку «живые прогоны» с подтверждением человека.

Решения владельца: слово 10.11.2026 «Да, запускай» (рекомендации F-6, F-7, F-9, F-10, F-11, F-12 спеки t-2187 §12); слово 10.11.2026 «живой перепрогон отложи. Сделаем после завершения изменений в параллельных сессиях» (N9).
Порядок по общим файлам: `scripts/place_answers.py`: RN2-9 → RN2-10.
Скоуп свидетеля: тестовый файл изменённого модуля и ключи DoD узла; BATCH CANON — интегратор (CI).
Общий бриф дизайнерам: находка узла; спека t-2187 §11 и рецензия `docs/tasks/specs/reviews/20261110-t-2187-batch-critic.md`; `plans/builder-rules.md`; узлы RN2-9…RN2-11 написаны для билдера без дизайнера.

## Бриф

Что сделать: три хвоста критика пачки t-2187 (m8, очередь K7, K10), без изменения поведения везде, кроме RN2-9. НЕ делать: новые поля черновика, слияние кодом (код не склеивает и не судит о причине — P27), ничего в таблице соседства сверх спеки.

## Узлы

Исполнитель «designer → builder → critic» — кодовый узел; «builder» — узел-документ. Статусы:
`ожидает` → `в работе` → `сдано` → `принято` / `отклонено`.

| Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус |
|---|---|---|---|---|---|---|
| RN2-1 | П1 | N1 спеки t-2187: схема, константы и читатели «механизм и проявления» в черновике (`mechanism`, `manifestations[]`) (`findings/20261110-odin-bag-mnogo-proyavlenij-bagi-odnoj-prichiny-ne-drobyatsya.md`; P20, P27; FR-41; AR-13, AR-29) | designer → critic на план → builder → critic | `scripts/bug_records.py`, `scripts/contract.py`, `scripts/place_answers.py`, `scripts/tests/test_bug_manifestations.py` | — | принято `960c86709` |
| RN2-2 | П1 | N5 спеки t-2187: уставы аналитика, исследователя, раннера и писаря — поиск общей причины до черновика, степень уверенности, зависимость проявления от стартового состояния | designer → critic на план → builder → critic | `agents/qa-failure-analyst.md`, `agents/qa-runner.md`, `agents/qa-doc-scribe.md`, `references/explore-charter.md` | — | принято `0ca148e7e` |
| RN2-3 | П1 | N2 спеки t-2187: парование черновиков, заявка аналитика на S7, репетиция гейта B, текст бага | designer → critic на план → builder → critic | `scripts/bug_records.py`, `scripts/gate_preflight.py`, `scripts/handoff_check.py` | RN2-1 | принято `8a853451c` |
| RN2-4 | П1 | N3a спеки t-2187: трассировка, отчёт и дашборд читают проявления одним читателем | designer → critic на план → builder → critic | `scripts/traceability.py`, `scripts/report_facts.py`, `scripts/factory_dashboard.py` | RN2-1 | принято `42f3d9123` |
| RN2-5 | П1 | N3b спеки t-2187: пакет гейта B показывает один баг с проявлениями и дверью «это разные баги» | designer → critic на план → builder → critic | `scripts/gate_brief.py` | RN2-3 | принято `687bcb4f5`, `a5edde046` |
| RN2-6 | П1 | N4 спеки t-2187: репортёр и проверка файла бага (`check_bug_form`) для бага с проявлениями | designer → critic на план → builder → critic | `agents/qa-bug-reporter.md`, `scripts/validate_artifacts.py`, `scripts/artifact_producer.py` | RN2-1 | принято `7e4c067fb` |
| RN2-7 | П1 | N6 спеки t-2187: таблица соседства `bug_neighbours` — улики для аналитика, код не склеивает и не судит | designer → critic на план → builder → critic | `scripts/bug_neighbours.py`, `scripts/brief_pack.py`, `scripts/story_run.py`, `scripts/tests/test_bug_neighbours.py` | RN2-1 | принято `69c7fb0eb` |
| RN2-8 | П1 | N7 и N8 спеки t-2187: места поглощённых черновиков при ответе и тексты фаз с границей отсечения; интеграция узлов (раунд правки по критику `3b77cb4e5`, починки CI `a2f3307bd`, `383062508`, `daeae50a8`) | designer → critic на план → builder → critic | `scripts/place_answers.py`, `skills/qa-story/phases/s7.md`, `skills/qa-story/phases/s8.md` | RN2-1, RN2-5 | принято `4dad89498`, `252fe62a9` |
| RN2-9 | П3 | **Хвост m8 критика пачки t-2187.** `scripts/place_answers.py::_bug_list` отказывает `--replace` ответа места, чей черновик X поглощён в сводный черновик M: по имени X — «is no draft file», по имени M — «belongs to place P_M»; у аналитика нет двери (FR-57), и место P_X на закрытии становится пробелом, хотя M его несёт. Ожидаемое: `_bug_list` принимает M для места X, если M держит проявление с `from_draft == X` (через существующий `_absorbers`, `place_answers.py:521`); без такого проявления отказ прежний (оба текста отказа не меняются). Тест в `scripts/tests/test_place_answers.py`: (а) черновик X поглощён в M (у M проявление `from_draft: X`), ответ места P_X с `draft: M` проходит `_bug_list` без отказа; (б) то же без проявления с `from_draft == X` — отказ «belongs to place» остаётся; (в) имя несуществующего файла — прежний «is no draft file». Пошагово: перед `if owner != place` в `_bug_list` дополнительно взять `_absorbers(task, <draft X места place>)`; не менять `place_of_draft` (рецензия критика, m8, строка 50) | builder → critic | `scripts/place_answers.py` (`_bug_list`), `scripts/tests/test_place_answers.py` | — | принято `df87923a9` |
| RN2-10 | П3 | **Очередь K7 критика пачки t-2187: дубли помощников.** `gate_brief._squash` (`gate_brief.py:4189`) дублирует `gate_brief._one_line` (`:1472`) в том же файле; `bug_records._fold` (`bug_records.py:1882`) дублирует `place_answers._squash` (`place_answers.py:51`) плюс casefold. Ожидаемое: по одному выжившему на пару, вызывающие переведены, поведение не меняется (то же усечение и те же пробелы; у `_fold` — тот же casefold поверх общего читателя). Тест: уже существующие `scripts/tests/test_gate_brief_and_retro.py`, `scripts/tests/test_gate_brief_attachments.py`, `scripts/tests/test_bug_records.py`, `scripts/tests/test_place_answers.py` остаются зелёными без правок, а `python -B tools/dup_ratchet.py --check` не показывает нового клона. Если у пары расходятся граничные случаи (пустое, `None`, лимит), вернуть вопрос наверх, не выбирать самому | builder → critic | `scripts/gate_brief.py` (`_squash`, `_one_line`), `scripts/bug_records.py` (`_fold`), `scripts/place_answers.py` (`_squash`) | RN2-9 | принято `f2c0e1fda` (пара `gate_brief` сведена к `_one_line`; пара `_fold` / `place_answers._squash` оставлена: модули импортируют друг друга лениво, расхождение на ложных значениях настоящее — Lead пачки, 10.11.2026) |
| RN2-11 | П3 | **Хвост K10 критика пачки t-2187: длинные функции.** `bug_neighbours.neighbours` (`bug_neighbours.py:100`, около 120 строк, три внутренних замыкания) и `bug_records.mechanism_problems` (`bug_records.py:1935`, около 85 строк) разбиты на именованные шаги не длиннее ~60 строк; поведение не меняется. Тест: `scripts/tests/test_bug_neighbours.py` и `scripts/tests/test_bug_manifestations.py` зелёные без единой правки; `python -B tools/dup_ratchet.py --check` без нового клона. Замыкания становятся функциями модуля с явными аргументами; публичные имена и порядок и тексты причин (`R_MECH_*`) не меняются | builder → critic | `scripts/bug_neighbours.py` (`neighbours`), `scripts/bug_records.py` (`mechanism_problems`) | — | принято `bed8293c2` (разбита `_mechanism_scan`, тело `mechanism_problems`) |

## Ход

Журнал передачи Lead пачки, новые записи в конец: `<дата время> — <что сделано, диспатчи t-nnn, хэши>`.

- 10.11 — открыта пачка 2 по спеке t-2187: узлы N1–N8 слиты в `experiment/thinking-roles` на `4a6ce9335` (хэши в таблице узлов); N9 отложен словом владельца; три хвоста критика пачки (m8, K7, K10) — узлы RN2-9…RN2-11
- 10.11 21:40 — хвосты сделаны одним исполнителем (t-2253) по слову владельца «почему отложили? Нельзя сделать сейчас?»: RN2-9 `df87923a9`, RN2-11 `bed8293c2`, RN2-10 `f2c0e1fda`; осталось живое доказательство N9

## Живые доказательства

| Что | Стенд / проект | Кто | Статус |
|---|---|---|---|
| N9 спеки t-2187 (FR-33): перепрогон LOCAL-1 на MyBooks. (i) хотя бы один сводный баг, у которого `mechanism.basis` держит записи `run` из двух РАЗНЫХ `start_state`, снятые аналитиком в ЭТОМ прогоне (улики в `work/evidence/manual/settle-*`); (ii) расход стадии S7 этого прогона рядом с расходом S7 прошлого прогона LOCAL-1 (`experiments/mybooks/thinking-roles/thinking-roles.md:115`, «S7 $1.37»), одна метрика и названный носитель (FR-24, FR-26). Поле количества на странице книги — ОДИН черновик с не менее чем тремя проявлениями; «12» в корзине (`CartPage.tsx:183`) — отдельный черновик. Слово владельца 10.11.2026: «живой перепрогон отложи. Сделаем после завершения изменений в параллельных сессиях» | стенд MyBooks по `docs/RUNBOOK.md` §11 | владелец и Lead | ожидает слова владельца |

## Остатки

<!--
Пачка закрывается доделкой, не переносом (слово владельца 08.10.2026): `close` отказывает, пока в этом разделе есть
пункт, у которого нет одной из двух форм (ключи в нижнем регистре, пары `ключ: значение` через ` | `, текст впереди):
  - <что осталось> | сделано: <хэш 7-40 hex | t-nnn>
  - <что осталось> | перенос: <findings/<файл> | пачка N | <кучка>/findings/<файл>> | обоснование: <почему> | подтвердил: <кто, дата>
Пустой раздел — можно закрывать.
-->

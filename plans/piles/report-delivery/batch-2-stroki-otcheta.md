# Отчёт, доставка, трассировка — пачка 2: строки отчёта называют обязательство и исход, а не шаг и ответ

кучка: `report-delivery` | статус: ожидает | взял: — | ветка: — | MR: — | стенд: не нужен (CI + эталоны) | приоритет: П2 | issue: https://git.example.com/dev1/yml-text-factory/-/work_items/70

Открыта 02.11.2026 разбором законченного прогона LOCAL-1 (t-1672 П-18, П-20; заведены t-1673): пачка 1 закрыта, новая находка кучки легла в следующую.

Правило готовности: пачка закрыта, когда каждый узел «принято», свидетели узлов — в журнале взявшего.

Решения владельца: нет (направление выбрано Lead, 02.11.2026).
Порядок по общим файлам: `report_facts.py`: после узла RN1-23 (`release-next/1`) или с непересекающимися списками функций (D-0048).
Скоуп свидетеля: тестовый файл изменённого модуля и ключи DoD узла; BATCH CANON — интегратор.
Общий бриф дизайнерам: карточка кучки («Дороги», «Содержание»); находка узла; `PROJECT.md` P21; FR-10, FR-19, FR-20; вернуть спеку в `docs/tasks/specs/t-nnn-rd2-n.md` с развилками наверх.

## Бриф

Что сделать: строки отчёта «Branches left with you» и «Not proven» называют обязательство и исход исполнения. НЕ делать: другие узлы отчёта (`batch-1-honest-report.md`).

## Узлы

Исполнитель «designer → builder → critic» — кодовый узел; «builder» — узел-документ. Статусы:
`ожидает` → `в работе` → `сдано` → `принято` / `отклонено`.

| Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус |
|---|---|---|---|---|---|---|
| RD2-1 | П2 | **Разбор LOCAL-1 (t-1672 П-18, П-20), 02.11.2026.** Исключённый кейс Jira разложен на 10 строк по шагам с противоречивой припиской, BN-2/BN-3 «no test proves it» при красных TC_007/008; причина «Not proven» R-24/R-25 взята из ответа о требовании, не из исхода исполнения: одна строка на обязательство, красный тест назван, причина — исход. **Пошагово — пп. 1–3 находки** (`findings/20261102-stroki-otcheta-razbity-po-shagam-i-prichina-ne-iz-ishoda.md`; P21; FR-10, FR-19, FR-20; AR-27) | designer → builder → critic | `scripts/report_facts.py`, `scripts/traceability.py`, их тесты, `changelog.d/` | WG1-1 (`words-gates/1`, приписка решения человеку); RN1-23 (`release-next/1`, общий отчёт) | ожидает |
| RD2-2 | П2 | Слова человека, записанные замечанием `pipeline.json remarks[]`, доходят до отчёта: раздел «Your remarks» в `report_facts`; у стори без MR слова больше не теряются (`findings/20261102-slova-cheloveka-remarks-ne-dohodyat-do-otcheta.md`; критик t-738 B-1; P13; FR-8, FR-9, FR-37; AR-13, AR-23, AR-24) | designer → builder → critic | `scripts/report_facts.py`, `scripts/gate_brief.py` (`remarks`, чтение), их тесты, `changelog.d/` | GW1-3 (`release-next/1`, влит); RD2-1 (общий `report_facts.py`, непересекающиеся функции, D-0048) | ожидает |
| RD2-3 | П3 | Хвосты RD1-4 по тексту и карте: читатель `output_tail`, одна маскировка секретов `mask_secrets` (восемь утекающих форм), шаг 7 писаря «must» (`findings/20261102-hvosty-rd1-4-tekst-karty-output-tail-maskirovka-shag-pisarya.md`; критик t-758 m-2, m-3, m-5; FR-6, FR-37, FR-41; AR-13, AR-22) | builder → critic | `scripts/stand_gaps.py`, `scripts/gate_brief.py` (:1531), `references/conductor.md`, `agents/qa-doc-scribe.md`, их тесты | RD1-4 (`release-next/1`, влит) | ожидает |
| RD2-4 | П3 | Читатели разделов отчёта — один (`report_facts._section_span`) вместо двойников и заголовки других артефактов — константами `grammar` (`findings/20261113-chitateli-razdelov-otcheta-dvojniki-i-perepisannye-zagolovki.md`; t-205 F6 (i)-(iii)). Направление: `validate_artifacts._report_section_body`, `report_facts.left_with_you_text`, `check_report_gate_b`, `traceability.py:1688-1698`, `human_text.section_problems` зовут один читатель; различия поведения (заборы кода, маркеры блоков) — в таблицу ДО правки, развилка Lead; форма бага и `UNDERSTANDING_SECTIONS` — по одному дому в `grammar`. Первый шаг — поиск заголовков отчёта литералами вне P5/P9. Тест: таблица «читатель × вход» (раздел в заборе, за маркером блока, нет, дважды, пустой, конец без перевода строки) — один ответ; сторож литералов вне `grammar` shrink-only | designer → builder → critic | `scripts/validate_artifacts.py`, `scripts/report_facts.py`, `scripts/traceability.py`, `scripts/human_text.py`, `scripts/grammar.py`, `scripts/tests/test_report_facts.py`, `scripts/tests/test_validators.py` | слияние HF8-4 (P5, P9; `onboarding-forge/2`) | ожидает |

## Ход

Журнал передачи Lead пачки, новые записи в конец: `<дата время> — <что сделано, диспатчи t-nnn, хэши>`.

- 02.11 — открыта пачка 2 под RD2-1 (разбор LOCAL-1, t-1672 П-18, П-20; t-1673)
- 13.11 — узел RD2-4 (читатели разделов отчёта и заголовки, t-205 F6) тем же ходом, что файл в `findings/` (D-0044, t-233)

## Живые доказательства

| Что | Стенд / проект | Кто | Статус |
|---|---|---|---|

## Остатки

<!--
Пачка закрывается доделкой, не переносом (слово владельца 08.10.2026): `close` отказывает, пока в этом разделе есть
пункт, у которого нет одной из двух форм (ключи в нижнем регистре, пары `ключ: значение` через ` | `, текст впереди):
  - <что осталось> | сделано: <хэш 7-40 hex | t-nnn>
  - <что осталось> | перенос: <findings/<файл> | пачка N | <кучка>/findings/<файл>> | обоснование: <почему> | подтвердил: <кто, дата>
Пустой раздел — можно закрывать.
-->

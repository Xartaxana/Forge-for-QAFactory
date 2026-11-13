# Качество тестов — пачка 2: слияние кейсов получает исполнителя у дизайнера, читатели доставки знают `Archived`

кучка: `test-code-quality` | статус: ожидает | взял: — | ветка: — | MR: — | стенд: нужен только живому доказательству (копия 12586, кучка `live-runs`) | приоритет: П2 | issue: https://git.example.com/dev1/yml-text-factory/-/work_items/71

Открыта 02.11.2026 (Lead пачки release-next/1) по вердиктам критиков TQ1-27: пачка 1 закрыта, новая находка кучки легла в следующую (D-0044).

Правило готовности: пачка закрыта, когда каждый узел «принято», свидетели узлов — в журнале взявшего.

Решения владельца: нет (направление выбрано Lead, 02.11.2026).
Порядок по общим файлам: `agents/qa-case-designer.md`, `agents/qa-case-critic.md` — после TQ1-24, TQ1-27, RN1-7, RN1-27 (`release-next/1`) или непересекающимися местами (D-0048).
Скоуп свидетеля: тестовый файл изменённого модуля и ключи DoD узла; BATCH CANON — интегратор.
Общий бриф дизайнерам: карточка кучки («Дороги», «Содержание»); находка узла; `PROJECT.md` P16, P19; FR-9, FR-40; вернуть спеку в `docs/tasks/specs/t-nnn-tq2-n.md` с развилками наверх.

## Бриф

Что сделать: слить дублирующие кейсы там, где критик назвал слияние, и научить читателей доставки состоянию `Archived`. НЕ делать: правки узлов `release-next/1`; новые правила критика кейсов (TQ1-27 уже внёс).

## Узлы

Исполнитель «designer → builder → critic» — кодовый узел; «builder» — узел-документ. Статусы:
`ожидает` → `в работе` → `сдано` → `принято` / `отклонено`.

| Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус |
|---|---|---|---|---|---|---|
| TQ2-1 | П2 | Q1 TQ1-27: правило «одна форма, ветки — параметрами» и исполнение слияния у дизайнера (`status: Archived`, выживший несёт `Then` и `covers`) вместе с читателями доставки, пропускающими `Archived` (`case_index`, `check_delivery._completeness` для архивного и удалённого, гейт A строки кейсов); один помощник «колонка таблицы по имени» вместо трёх читателей шапки (`findings/20261102-sliyanie-kejsov-bez-ispolnitelya-na-storone-dizajnera-i-dvojnye-chitateli-shapki.md`; критики t-715 B-1, t-756 m-5, m-6; P16, P19; FR-9, FR-40; AR-13, AR-19, AR-25) | designer → critic на план → builder → critic | `agents/qa-case-designer.md`, срез устава, `scripts/contract.py` (`case_index`), `scripts/check_delivery.py` (`_completeness`), `scripts/controller.py` (строки кейсов гейта A), `scripts/critic_rollcall.py`, их тесты, `changelog.d/` | TQ1-27 (`release-next/1`, влит); TQ1-7, TQ1-19 (дубли кода S5 — тот же класс стадией позже) | ожидает |
| TQ2-2 | П3 | Читатели колонки таблицы руками вне `critic_rollcall`: `audit_factory.py:749`, `planning_contract.py:1341/1345/1446/2488/2489` — через `contract.md_column`; направление ошибки названо для каждого сайта (`findings/20261113-chitateli-kolonki-tablicy-rukami-vne-critic-rollcall.md`; критик темы TQ2-1, Q1; FR-54, FR-1; AR-13, AR-15) | designer → builder → critic | `scripts/audit_factory.py`, `scripts/planning_contract.py`, их тесты | TQ2-1 | ожидает |
| TQ2-3 | П2 | Нарезка окон держит группы слияния вместе (`s5_plan.case_groups`, `controller.split_windows`, `_scope_windows`) и C12 для окон legacy; новая идея — план владельцу и критик на план до дизайнера (`findings/20261113-narezka-okon-derzhit-gruppy-slijaniya-i-c12-dlya-legacy.md`; критик темы TQ2-1, Q2, развилка F7 (a); P16, P31; FR-9, FR-40; AR-13, AR-19, AR-25) | designer → critic на план → builder → critic | `scripts/s5_plan.py` (`case_groups`, `test_adjacency`), `scripts/controller.py` (`split_windows`, `_scope_windows`), `scripts/s5_precheck.py`, `scripts/tests/test_s5_plan_windows.py` | TQ2-1 | ожидает |
| TQ2-4 | П3 | `brief_pack.case_concern_lines` на 71 строку — таблица четырёх текстов шапки, `elsewhere` только на ветке автора, причина стадии с границей `_show(..., 100)` (`findings/20261113-case-concern-lines-71-stroka-mertvaya-rabota-i-prichina-bez-granicy.md`; критик темы TQ2-1, Q3) | builder → critic | `scripts/brief_pack.py` (`case_concern_lines`), `scripts/s5_plan.py` (`concerns_for_scope`), их тесты | TQ2-1 | ожидает |

## Ход

Журнал передачи Lead пачки, новые записи в конец: `<дата время> — <что сделано, диспатчи t-nnn, хэши>`.

- 02.11 — открыта пачка 2 под TQ2-1 (очередь критиков TQ1-27; t-770)
- 13.11 — TQ2-1: спека готова, ждёт слова владельца по развилке F1 (статус остаётся «ожидает»).

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

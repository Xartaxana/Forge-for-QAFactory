# Пакет: тесты, Linux, CI — пачка 2: потолки брифа в тестах не привязаны к измеренной константе

кучка: `package-ci` | статус: в работе | взял: dev1, 11.11.2026 | ветка: `pile/package-ci/batch-2` | MR: — | стенд: не нужен (CI) | приоритет: П2 | issue: https://git.example.com/dev1/yml-text-factory/-/work_items/69

Открыта 02.11.2026 (Lead пачки release-next/1) по трём перемерам за вечер (t-747, t-755, t-769): пачка 1 закрыта, новая находка кучки легла в следующую (D-0044).

Правило готовности: пачка закрыта, когда каждый узел «принято», свидетели узлов — в журнале взявшего.

Решения владельца: нет (направление выбрано Lead, 02.11.2026).
Скоуп свидетеля: `scripts/tests/test_brief_pack.py` и ключи DoD узла; BATCH CANON — интегратор.
Общий бриф дизайнерам: карточка кучки («Дороги», «Содержание»); находка узла; `design/factory-rules.md` FR-31, FR-32; вернуть спеку в `docs/tasks/specs/t-nnn-pc2-n.md`.

## Бриф

Что сделать: пины потолков `brief_pack` строятся во время теста, а не берутся из измеренной константы. НЕ делать: правки кода `brief_pack.py`.

## Узлы

Исполнитель «designer → builder → critic» — кодовый узел; «builder» — узел-документ. Статусы:
`ожидает` → `в работе` → `сдано` → `принято` / `отклонено`.

| Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус |
|---|---|---|---|---|---|---|
| PC2-1 | П2 | Пины потолков S5 в `test_brief_pack.py` строят заполнитель до потолка бисекцией во время теста; константы `S5_DIGESTS_INLINE_CEILING` и `S5_GATE_LINE_CEILING` убраны (`findings/20261102-potolki-brief-pack-v-testah-plyvut-s-kazhdym-bajtom-brifa.md`; билдеры t-747, t-755, t-769; FR-31, FR-32; AR-20) | builder → critic | `scripts/tests/test_brief_pack.py` | — | ожидает |
| PC2-2 | П2 | `test_codex_tool_guidance`, `test_role_policy_reads`, `test_story_step_materialize` после свёртки changelog (`folded = not FRAGMENT.is_file()`) проверяют лишь непустой `CHANGELOG.md`, а не собственную запись релиза: один читатель по образцу `release_note()` в `scripts/tests/test_retro_always_full.py` (`findings/20261104-testy-posle-svertki-changelog-chitayut-ne-svoyu-zapis.md`; t-1822; FR-18, FR-31) | builder → critic | `scripts/tests/test_codex_tool_guidance.py`, `scripts/tests/test_role_policy_reads.py`, `scripts/tests/test_story_step_materialize.py` | — | ожидает |
| PC2-3 | П2 | PC2-3: хвосты критика GM3-2 — один писатель записи приёмки и один нормализатор слова `stage_awaits_acceptance` в `story_run_common.py`, фикстура повторного входа K3 с ролью и записью, ключ ветки без потребителя, подписи измеренного бюджета «budget B» (`findings/20261105-hvosty-kritika-gm3-2-obshchie-helpery-priemki-s6-i-podpisi-byudzheta.md`, раздел «Что именно менять»; вердикт t-008; AR-15, AR-20) | builder → critic | `scripts/tests/story_run_common.py`, `scripts/tests/test_story_run_s6.py`, `scripts/tests/test_controller_state.py`, `scripts/brief_pack.py` | — | ожидает |
| PC2-4 | П1 | Канон красный: `test_probe_by_code` — расписка пишется один раз за обход, ключи `judgment_owed`/`walk_ended` получают читателя или уходят, испорченная запись не отвечает на повтор (`findings/20261111-kanon-krasnyj-probe-by-code-povtor-obhoda-i-raspiska.md`; t-033, t-035) | designer → builder → critic | `scripts/probe_by_code.py`, `scripts/tests/test_probe_by_code.py` | — | в работе |
| PC2-5 | П1 | Канон красный: `test_story_run_freshness` — после приёмки S2 диспатч S3 не зарегистрирован, файл падает исключением; причина одним запуском, запись приёмки в помощнике теста (`findings/20261111-kanon-krasnyj-freshness-s3-ne-registriruetsya.md`; t-034, t-035) | builder → critic | `scripts/tests/test_story_run_freshness.py` | PC2-3 | принято |
| PC2-6 | П1 | Канон красный: `test_brief_pack` — брифы S5 и критика кода выше потолка 6 КБ; лечится бриф, не потолок, обход человека и список файлов режутся последними (`findings/20261111-kanon-krasnyj-brief-pack-brify-vyshe-potolka-6-kb.md`; t-034, t-035; для этого узла запрет брифа пачки на правку `brief_pack.py` снят) | designer → builder → critic | `scripts/brief_pack.py`, `scripts/tests/test_brief_pack.py` | PC2-1 | в работе |
| PC2-7 | П1 | Канон красный: `test_no_mr_entry` — собственный ответ о стороне не выключает продукт по умолчанию; условие смотрит на строки реестра до этой стори (`findings/20261111-kanon-krasnyj-no-mr-entry-otvet-o-storone-vyklyuchaet-produkt.md`; t-034) | designer → critic на план → builder → critic | `scripts/story_run.py (s0_sides_sets)`, `scripts/tests/test_no_mr_entry.py` | — | в работе |

## Ход

Журнал передачи Lead пачки, новые записи в конец: `<дата время> — <что сделано, диспатчи t-nnn, хэши>`.

- 02.11 — открыта пачка 2 под PC2-1 (три перемера потолков брифа; t-770)
- 04.11 — добавлен PC2-2 (три теста после свёртки changelog; Lead)
- 11.11 — добавлены PC2-4…PC2-7: четыре оставшиеся причины красного канона на `483e664` после починки четырёх устаревших тестов (`81e33d7`, t-035; Lead)
- 12.11 00:25 — работа идёт в общем дереве на `main`, без ветки пачки (решение Lead; билдеры не коммитят). Канон 43110913721 на `81e33d7`: красных файлов ровно четыре, узлы PC2-4…PC2-7. PC2-5 принят (t-044, вторая попытка: устарела фикстура, S3 закрывался ролью `qa-worker`; код пакета прав). Спеки приняты с ответами на развилки: PC2-4 (t-041), PC2-6 (t-042), PC2-7 (t-043); критики на план t-046, t-051, t-050; замер PC2-6 — t-052. Открыто у владельца: развилка F-2 спеки t-043 (вторая стори проекта и сторона `product`)

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

# Сказано до работы (`told-before-work`)

приоритет: П1 | фичи: F19 | стенд: не нужен | зона: —

<!-- Грамматика `зона:` — как в `plans/piles/_template/README.md`; у кучки зоны нет: узлы называют свои файлы в «Пишет в». -->

## Зачем

Роль должна узнавать требование проверки ДО работы, а не в момент отказа: строки требований названы на страницах и в разделе дирижёра,
а отказы фабрики называют ту же строку по id. Осталось дописать id на оставшиеся отказы, перенести карточки правил в строки страниц и свести счётчики.

## Что не так сегодня (факты)

- Часть отказов (`guard_pre_tool`, `stage_guard`, `s5_precheck`, `handoff_check`, `validate_artifacts`, `planning_contract`, `coverage_contract`, `controller`) не несёт id строки требования (`docs/tasks/specs/20261117-told-before-work-finish-spec.md` §0, §6).
- Двенадцать карточек правил (`hand_cards`) живут отдельно от строк (спека §2, `stage_joints.py --check`).
- Опыт M9 («переживает ли страница `claude -p --resume`») не поставлен (спека §4).

## Пачки

| № | Что изменится для пользователя | Строки | Размер | Статус | Взял | Ветка | MR |
|---|---|---|---|---|---|---|---|
| 1 | отказы фабрики называют строку требования, роль видит её до работы; счётчики закрыты по замеру | TBW1-1…TBW1-15 | L (15 строк; Lead режет при взятии) | ожидает | — | — | — |

Статусы пачки: `ожидает` → `в работе` → `сдано` → `принято` → `закрыта`. Размер — по узлам: S ≤ 4 узлов,
M 5–9, L 10–15 (больше — две пачки). Взятая пачка заморожена: её файл правит только взявший, новое
по теме — файлом в `findings/`.

## Бриф пачки 1

Начать с волны A (T4a, T5r, T6, T7a-A, T7b, T7c) и опыта M9 (Lead). Стенд не нужен; слово владельца по Q-O1 дано (17.11.2026). Подробно — `batch-1-finish.md`, раздел «Бриф».

## Дороги

Читать по порядку: эта карточка → `batch-1-finish.md` → находка узла (колонка «id / файл» ниже) → карточка узла в `docs/tasks/specs/20261117-told-before-work-finish-spec.md` §6 → механизм-спека `told before work` →
`ai-packages/qa-factory/references/stage-joints.json`, `scripts/stage_joints.py`, `scripts/detector_verdict.py` (`refusal`, `spoken`, `told_fields`, `Record`).
Слова: `refusal`, `told_fields`, `spoken`, `stage_joints`, `told_ratchet`, `unsited`, `hand_cards`, `legacy_legs`, `native_headroom`, `judgment-census.json`, `REPAIR_MARKER`.
Не читать: соседние кучки, `rules-debt` (отдельный замысел; общий горячий файл — `s5_precheck.py`, очередь по F-9/решению Lead).

## Содержание

Снимок 17.11.2026; пути — от `ai-packages/qa-factory/`; суть — из карточек спеки. При расхождении авторитетны файлы пачек. Каждый id строки карточки и каждый файл из `findings/` стоит здесь ровно один раз
(`tools/test_pile_cards_contents.py`); id строки стоит и в «Что» ровно одного узла файла своей пачки (`piles.py check` (д)).

| id / файл | вид | суть (≤ 20 слов) | пути | статус | слово владельца | связи |
|---|---|---|---|---|---|---|
| **Пачка 1** | | | | | | |
| `findings/20261117-tbw-m9-perezhivaet-li-stranitsa-resume.md` | находка, id — | Опыт M9: переживают ли страница и строка промпта возобновление `claude -p --resume` | — | пачка 1, TBW1-1 | нет | TBW1-12 (T3b) (ждёт этого опыта) |
| `findings/20261117-tbw-t4a-id-strok-na-otkazah-guard-pre-tool.md` | находка, id — | id строк §5.3 на отказах `guard_pre_tool` и `host_adapter` | — | пачка 1, TBW1-2 | нет | TBW1-3 (T4b) (тот же класс, другие файлы); FV1-27 |
| `findings/20261117-tbw-t4b-id-strok-na-stage-guard-i-hooklib.md` | находка, id — | id строк §5.3 25-31 на `stage_guard` и `hooklib`; перепись единиц G-dispatch | — | пачка 1, TBW1-3 | нет | TBW1-2 (T4a); TBW1-9 (T7f), TBW1-11 (T9c), TBW1-10 (T9a) (порядок переписи) |
| `findings/20261117-tbw-t5r-id-strok-na-s5-precheck-i-manifest-put.md` | находка, id — | id строк §5.4 на `s5_precheck` (11 семейств) и `manifest_put` (14 отказов) | — | пачка 1, TBW1-4 | нет | RD1-22 (FL9) (`rules-debt/1`, оба правят `s5_precheck.py`: функции не пересекаются; решение Lead: T5r после слияния FL9) |
| `findings/20261117-tbw-t6-id-21-stroki-handoff-check.md` | находка, id — | id 21 строки `handoff_check` | — | пачка 1, TBW1-5 | нет | FV2-78 (`live-run-fvf/2`, функции не пересекаются) |
| `findings/20261117-tbw-t7a-id-42-strok-validate-artifacts.md` | находка, id — | id 42 строк `validate_artifacts` тремя узлами по спискам функций (T7a-A, T7a-B, T7a-C) | — | пачка 1, TBW1-6 | нет | TBW1-5 (T6), TBW1-7 (T7b) (тот же класс, другие файлы) |
| `findings/20261117-tbw-t7b-id-12-strok-planning-contract.md` | находка, id — | id 12 строк `planning_contract` | — | пачка 1, TBW1-7 | нет | TBW1-11 (T9c) (строка `planning_contract:plan.unmarked_revision`) |
| `findings/20261117-tbw-t7c-id-2-strok-coverage-contract.md` | находка, id — | id 2 строк `coverage_contract` | — | пачка 1, TBW1-8 | нет | TBW1-7 (T7b) (тот же класс) |
| `findings/20261117-tbw-t7f-perepis-edinic-stage-done.md` | находка, id — | Перепись единиц `stage_done` → conductor | — | пачка 1, TBW1-9 | нет | TBW1-3 (T4b) (перепись по порядку) |
| `findings/20261117-tbw-t9a-id-6-strok-controller.md` | находка, id — | id 6 строк `controller:*` и перепись ролей возобновлённых единиц | — | пачка 1, TBW1-10 | нет | FV2-88 (разведка); порядок переписи |
| `findings/20261117-tbw-t9c-razdel-what-code-will-check-u-dirizhera.md` | находка, id — | Раздел «What code will check in this launch» у дирижёра и строки дирижёра | — | пачка 1, TBW1-11 | нет | TBW1-9 (T7f); TBW1-7 (T7b) (`unmarked_revision`) |
| `findings/20261117-tbw-t3b-brif-bez-kartochek-stroka-grupp.md` | находка, id — | Бриф без карточек, строка групп в промпте, `first_look:put` | — | пачка 1, TBW1-12 | нет | TBW1-1 (M9); TBW1-13 (T1rc); FV2-54/56/57/58 |
| `findings/20261117-tbw-t1rc-kartochki-v-stroki-peredraft.md` | находка, id — | Карточки → строки (`T1r-cards`): передрафт дизайнера, критик на изменённые части, затем билдер -a/-b | — | пачка 1, TBW1-13 | дано: Q-O1, 17.11.2026 | TBW1-15 (close) (счётчик `hand_cards`) |
| `findings/20261117-tbw-t10-nositeli-lead-os-38.md` | находка, id — | Носители Lead: ось 38, AR-10/AR-9, FR-38, critic-brief, калибровка | — | пачка 1, TBW1-14 | нет | ось 38 карты; AR-10 |
| `findings/20261117-tbw-close-zakrytie-schetchikov-told-ratchet.md` | находка, id — | Закрытие: счётчики `told_ratchet` и `told-ratchet.json` по замеру, мёртвый код карточек | — | пачка 1, TBW1-15 | нет | все узлы TBW; K1b (`live-run-fvf/2` FV2-79) |

## Входящие

`findings/` этой кучки; находку, не названную ни в одной пачке, называет `piles.py check --all` (е).
Каждая новая находка тем же ходом получает строку в пачке этой кучки, которую ещё не взяли, или указатель `перенос: <кучка>/…`
(`piles.py check` (е)); нет такой пачки — открывается следующая со статусом «ожидает».

## Вопросы владельцу

- Q-O1 (предел размера страниц) — ОТВЕЧЕНО (владелец, 17.11.2026): «не в ущерб правилам. Если не влезет можно поднять».

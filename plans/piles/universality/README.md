# Универсальность (`universality`)

приоритет: П1 | фичи: F19 | стенд: нужен | зона: —

<!-- Грамматика `зона:` — как в `plans/piles/_template/README.md`; у кучки зоны нет: узлы называют свои файлы в «Пишет в». -->

## Зачем

Работа «фабрика проходит все стадии, не застряв, и ничего не знает о проекте». Сегодня фабрика может остановиться или отдать кейс человеку там,
где свободный агент на той же модели пошёл бы дальше: проект, о котором она ничего не знает, неизвестный драйвер, нет отчёта после прогона,
не подготовленный стенд. После этой кучки каждое такое место либо даёт роли идти дальше, либо задаёт один человеческий вопрос с дверями.

## Что не так сегодня (факты)

Находки раунда t-1252 → где чинятся (спека `docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r3.md` §0):

- N1: прогон без отчёта нельзя разобрать, узел 4b и развилка F-13 неисполнимы → стороны 7a (ручная половина) и 7b (автоматическая), спека §2 r4, §6 7a/7b, §11 F-15, F-17.
- N2: доставка и вход S7 читают `not_executed` по-разному → один предикат `s7_pretriage.triageable_not_executed`, спека §2 r4, §3, §6 7a.
- N3: пустой манифест S5 не проходит читателей свидетельства → исход `nothing` в `acceptance.run_witness_excused`, спека §2 r11, §6 5b, §13 D5.
- M-a: два контакта с человеком на один недостающий запускатель → текст `fix` находки `s5_executor`, спека §2 r8, §6 5a.
- M-b: дорога 3 без границы и дверь роли → `executor_install` по записи хода, `s5.md:144`, спека §2 r8, §6 5a.
- M-c: учётные данные → `check_s5_credentials` не меняется, спека §3, §6 5a.
- M-d: развилка F-14 без владельца → пункт 9 потока 5a, спека §2 r8, §6 5a.
- M-e: пустой вывод читает мимо неизвестного → ключ `undisposed` в `controller.stage_scope`, спека §2 r11, §6 5b.
- M-f: читатели новых путей r2 → спека §8.
- M-g: устаревшие тексты (ось 5 карты, ячейки `architecture.md`, комментарии `driver_stage_s7.py`) → спека §2 r11, §6 1/5b/7a/7b.
- M-h: перепись и храповики → `driver-exits/gates.json` у 5a, `s5.json` у 5b, спека §1.2, §6.
- M-i: метки обхода разнообразия → спека §1.3.

## Пачки

| № | Что изменится для пользователя | Строки | Размер | Статус | Взял | Ветка | MR |
|---|---|---|---|---|---|---|---|
| 1 | фабрика проходит все стадии, не застряв: неизвестный проект, нет драйвера, нет отчёта, неподготовленный стенд — роль идёт дальше или человек получает один вопрос с дверями | U1-1…U1-11 | L (11 узлов) | ожидает | — | — | — |

Статусы пачки: `ожидает` → `в работе` → `сдано` → `принято` → `закрыта`. Размер — по узлам: S ≤ 4 узлов,
M 5–9, L 10–15 (больше — две пачки). Взятая пачка заморожена: её файл правит только взявший, новое
по теме — файлом в `findings/`.

## Бриф пачки 1

Часть узлов уже идёт: U1-3 и U1-4 приняты, U1-1, U1-6, U1-7, U1-8 в работе. Следом U1-2 (после U1-8), U1-9 (после U1-8 и U1-6), U1-10 (после U1-9), U1-5 (после RD1-24). U1-11 ждёт слова владельца по F-5. Стенд нужен для живых доказательств L1–L6. Подробно — `batch-1-pass-without-stuck.md`.

## Дороги

Читать по порядку: эта карточка → `batch-1-pass-without-stuck.md` → спека `docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r3.md` (§1 архитектура, §2 места, §6 потоки, §11 развилки) → код зоны по функциям из «Слов» → `ai-packages/qa-factory/design/factory-rules.md`.
Слова: `declared_surfaces`, `surfaces.undeclared`, `_row_of_nobody`, `check_s5_executor`, `executor_install`, `code_only`, `stage_scope`, `run_witness_excused`, `triageable_not_executed`, `run_reasons`, `report_unread`, `run_unread`, `unprepared_walk`.
Не читать: соседние кучки; `onboarding-forge/5` (поток 6 спеки — узел OF5-5, не здесь).

## Содержание

Снимок 17.11.2026; пути — от `ai-packages/qa-factory/`; суть — из потоков спеки r3 §6. При расхождении авторитетны файлы пачек. Каждый id строки карточки и каждый файл из `findings/` стоит здесь ровно один раз
(`tools/test_pile_cards_contents.py`); id строки стоит и в «Что» ровно одного узла файла своей пачки (`piles.py check` (д)).

| id / файл | вид | суть (≤ 20 слов) | пути | статус | слово владельца | связи |
|---|---|---|---|---|---|---|
| **Пачка 1** | | | | | | |
| U1-1 | строка | поверхности и готовность: «не объявлено» вслух, роль первой, строка стенда без адреса | `scripts/surfaces.py`, `references/surfaces.json`, `scripts/readiness.py`, `scripts/planning_contract.py`, `scripts/tests/test_readiness.py`, `scripts/tests/test_question_branches.py`, `design/architecture.md` | в работе (t-1263) | да, 17.11.2026 | U1-2 (пункт 4 после U1-8) |
| U1-2 | строка | строка плана без исполнителя превращается в ручной кейс агента | `scripts/planning_contract.py`, `scripts/tests/test_question_branches.py` | ожидает | да, 17.11.2026 | U1-8 (после) |
| U1-3 | строка | разведка онбординга: устройство или нативный продукт, агент пробует сам | `skills/qa-onboarding/phases/p1-discovery.md`, `skills/qa-onboarding/phases/p2-interview.md` | принято (56addbf7, t-1261) | да, 17.11.2026 | — |
| U1-4 | строка | пин S0: нет возможности — вопрос `s0.readiness`, дирижёр 0 вызовов | `scripts/tests/test_no_move_seam_sites.py` | принято (48fb860e, t-1260) | да, 17.11.2026 | — |
| U1-5 | строка | текст пробы: дверь «красная песочница» раньше предложения про инструменты | `scripts/probe_by_code.py`, `scripts/tests/test_probe_by_code.py` | ожидает | да, 17.11.2026 | RD1-24 (`rules-debt/1`) |
| U1-6 | строка | недостающий запускатель: один ход дирижёра по известной установке, затем один вопрос | `scripts/gate_preflight.py`, `scripts/driver_gates.py`, `scripts/run_suite.py`, `references/halts.md`, `skills/qa-story/phases/s5.md`, `scripts/tests/test_gate_preflight.py`, `scripts/tests/fixtures/driver-layers.json`, `scripts/tests/fixtures/driver-exits/gates.json` | в работе (t-1264) | да, 17.11.2026 | RD1-13, RD1-14 (`rules-debt/1`); U1-9 |
| U1-7 | строка | S5 закрывается кодом над пустым выводом; пустой манифест не требует свидетельства | `scripts/driver_stage_s5.py`, `scripts/controller.py`, `scripts/driver_core.py`, `scripts/driver_dispatch.py`, `scripts/acceptance.py`, `scripts/check_witness.py`, `scripts/validate_artifacts.py`, `scripts/tests/test_s5_window_leftovers.py`, `scripts/tests/test_controller_state.py`, `scripts/tests/test_check_witness.py`, `scripts/tests/fixtures/driver-exits/s5.json`, `design/controller-blocks.md` | в работе (t-1265) | да, 17.11.2026 | — |
| U1-8 | строка | вход S7 и доставка над `not_executed`, который роль может разобрать | `scripts/s7_pretriage.py`, `scripts/driver_stage_s7.py`, `scripts/check_delivery.py`, `scripts/tests/test_s7_pretriage.py`, `scripts/tests/test_story_run_s7.py`, `scripts/tests/test_check_delivery.py` | в работе (t-1266) | да, 17.11.2026 | U1-2, U1-9 (после) |
| U1-9 | строка | прогон без отчёта: экземпляры — цели аналитика, доставка `run_unread` | `scripts/run_suite.py`, `scripts/contract.py`, `scripts/ledger.py`, `scripts/check_traceability.py`, `references/delivery-verdict-kinds.json`, `agents/qa-failure-analyst.md`, `design/architecture.md`, `scripts/tests/test_ledger.py`, `scripts/tests/test_third_verdict.py` | ожидает | да, 17.11.2026 | U1-8, U1-6; U1-10 (после) |
| U1-10 | строка | непройденный ручной обход говорит `unprepared_walk` (`after_checks`), а не `chain_broken` | `scripts/check_traceability.py`, `references/delivery-verdict-kinds.json`, `scripts/tests/test_third_verdict.py` | ожидает | да, 17.11.2026 (F-16 (a), Архитектор «решила сама») | U1-9 |
| U1-11 | строка | текст исполнителя ручных прогонов: другой экземпляр — только разрешёнными проектом действиями | `agents/qa-runner.md` | ожидает | ждёт слова владельца по F-5 | — |

## Входящие

`findings/` этой кучки; находку, не названную ни в одной пачке, называет `piles.py check --all` (е).
Каждая новая находка тем же ходом получает строку в пачке этой кучки, которую ещё не взяли, или указатель `перенос: <кучка>/…`
(`piles.py check` (е)); нет такой пачки — открывается следующая со статусом «ожидает».

## Вопросы владельцу

- F-5 (второй экземпляр стенда или устройства: кто разрешает его поднять) — ждёт слова владельца; от неё зависит только U1-11 (строка «ждёт слова владельца»).

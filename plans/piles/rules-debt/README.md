# Правила фабрики: долг, фаза 2 (`rules-debt`)

приоритет: П1 | фичи: F19 | стенд: не нужен (живые доказательства — в `live-runs`) | зона: —

<!-- Грамматика `зона:` — как в `plans/piles/_template/README.md`; у кучки зоны нет: узлы называют свои файлы в «Пишет в». -->

## Зачем

Долг правил фабрики (`design/factory-rules-debt.md`) закрывается по частям. Остаток фазы 2: дома файла бага у писателя и читателей, исполнение дверей отказов
вместо чтения, перевод четырнадцати ворот в `converted` (неизвестное не проходит), дорога пробы для языка без строки, слово человека на пробеле `review`,
головы чтения как данные и второй проход файла долга. Каждый узел — карточка принятой спеки; направления развилок выбраны.

## Что не так сегодня (факты)

- Репортёр пишет баг в папку стори, а `judge_results.run_bugs` и `external_writes` ищут в каталоге состояния (`docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md` §0 п. 2).
- Четырнадцать строк `references/gate-registry.json` стоят на `status: debt`; предиката `acceptable`, которого требует `gate_registry.py:837-841`, в пакете нет (спека §0 п. 1).
- Для языка без строки пробы `red_sandbox.py --probe` отвечает `incomplete` и не оставляет расписки (спека, раздел «C4 result (t-961…)»; B-337).
- Из-за `rstrip(".exe")` в `stage_guard._is_reader` голова `catx` читается как `cat` (`stage_guard.py:2590`).

## Пачки

| № | Что изменится для пользователя | Строки | Размер | Статус | Взял | Ветка | MR |
|---|---|---|---|---|---|---|---|
| 1 | фабрика не принимает неизвестное как проход на четырнадцати воротах; баги, двери и слово человека читаются одной дорогой | RD1-1…RD1-24 | L (24 узла; Lead режет при взятии) | ожидает | — | — | — |

Статусы пачки: `ожидает` → `в работе` → `сдано` → `принято` → `закрыта`. Размер — по узлам: S ≤ 4 узлов,
M 5–9, L 10–15 (больше — две пачки). Взятая пачка заморожена: её файл правит только взявший, новое
по теме — файлом в `findings/`.

## Бриф пачки 1

Начать с волны 1 (RD1-1 (C1), RD1-2 (C2), RD1-22 (FL9), RD1-24 (B337) дизайнером), RD1-16 (C5) — процедура Lead. Стенд не нужен; слова владельца не нужны (решены F-O1…F-O6 и «Lead decisions on the forks»). Подробно — `batch-1-phase-2.md`, раздел «Бриф».

## Дороги

Читать по порядку: эта карточка → `batch-1-phase-2.md` → находка узла (колонка «id / файл» ниже) → карточка узла в `docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md` →
родительская `docs/tasks/specs/20261117-rules-debt-fix-spec.md` → `ai-packages/qa-factory/design/factory-rules-debt.md` и `references/gate-registry.json`.
Слова: `gate_registry.py`, `acceptable`, `converted`, `unknown_branch`, `bug_records`, `judge_results`, `external_writes`, `environment_record`, `window_record`, `launch-causes.json`, `FR-59`, `FR-33`.
Не читать: соседние кучки (`told-before-work` — отдельный замысел), код стадий вне «Пишет в» узла.

## Содержание

Снимок 17.11.2026; пути — от `ai-packages/qa-factory/`; суть — из карточек спеки. При расхождении авторитетны файлы пачек. Каждый id строки карточки и каждый файл из `findings/` стоит здесь ровно один раз
(`tools/test_pile_cards_contents.py`); id строки стоит и в «Что» ровно одного узла файла своей пачки (`piles.py check` (д)).

| id / файл | вид | суть (≤ 20 слов) | пути | статус | слово владельца | связи |
|---|---|---|---|---|---|---|
| **Пачка 1** | | | | | | |
| `findings/20261117-rd2-c1-doma-bug-faylov-pisatel-chitateli.md` | находка, id — | Дома файла бага: писатель (`qa-bug-reporter`) и читатели читают разные папки | `scripts/bug_records.py`, `scripts/judge_results.py`, `scripts/external_writes.py`, `references/common-rules.md` | пачка 1, RD1-1 (C1) | дано: F-O6 (a), 17.11.2026 | `external_writes`, `bug_records`; критик t-942 F8; ось 38 (Lead) |
| `findings/20261117-rd2-c2-chetyre-semejstva-dverej-odnoj-tablitsej.md` | находка, id — | Четыре семейства командных дверей — одной таблицей, дверь открывается исполнением | `scripts/tests/test_controller_doors.py` | пачка 1, RD1-2 (C2) | дано: F-O5 (b), 17.11.2026 | слово владельца F-O5 (b); `test_controller_blocks.py` — не применимо |
| `findings/20261117-rd2-c3-0-odin-predikat-acceptable.md` | находка, id — | FR-59: один предикат `acceptable` для сайтов приёма записи | `scripts/gate_template.py`, `scripts/tests/test_gate_registry.py` | пачка 1, RD1-3 (C3-0) | дано: F-O1, 17.11.2026 | F-D1 (b); все карточки C3 с сайтом приёма |
| `findings/20261117-rd2-c3-a-collected-ids-rerun.md` | находка, id — | FR-59: `collected_ids` — неизвестная ветка `rerun` (B-278) | `references/gate-registry.json`, `scripts/run_suite.py` | пачка 1, RD1-4 (C3-a) | дано: F-O1, 17.11.2026 | B-278; ось 4; очередь C3-a → C3-k |
| `findings/20261117-rd2-c3-b-test-identity-i-live-check-demand.md` | находка, id — | FR-59: `test_identity` (остаётся `rerun`) и `live_check_demand` — вопрос критику кода на приёмке окна | `references/gate-registry.json`, `scripts/proof_level.py`, `scripts/execution_request.py` | пачка 1, RD1-5 (C3-b) | дано: F-O1, 17.11.2026 | очередь C3-b → C3-k; живое доказательство — `live-runs/2` LR2-4 |
| `findings/20261117-rd2-c3-c-s5-coverage.md` | находка, id — | FR-59: `s5_coverage` — Then без установленной привязки идёт вопросом критику (B-221) | `references/gate-registry.json`, `scripts/s5_precheck.py` | пачка 1, RD1-6 (C3-c) | дано: F-O1, 17.11.2026 | B-221; очередь FL9 → C3-c |
| `findings/20261117-rd2-c3-d-s5-window.md` | находка, id — | FR-59: `s5_window` — неизмеренный детектор в окне закрывает критик, не проход (B-179) | `references/gate-registry.json`, `scripts/acceptance.py`, `scripts/window_record.py` | пачка 1, RD1-7 (C3-d) | дано: F-O1, 17.11.2026 | B-179; очередь S9 → C3-d |
| `findings/20261117-rd2-c3-e-delivery-refuse-with-door.md` | находка, id — | FR-59: `delivery` — неизвестный вид причины → `refuse_with_door` (B-061) | `references/gate-registry.json`, `scripts/delivery_verdict.py`, `scripts/check_delivery.py` | пачка 1, RD1-8 (C3-e) | дано: F-O1, 17.11.2026 | B-061; очередь C3-e → RD1-20 (FL2) |
| `findings/20261117-rd2-c3-f-environment-preparation.md` | находка, id — | FR-59: `environment_preparation` — неизвестное доказательство выкладки идёт вопросом на авторизации (B-255) | `references/gate-registry.json`, `scripts/environment_preparation.py` | пачка 1, RD1-9 (C3-f) | дано: F-O1, 17.11.2026 | B-255 |
| `findings/20261117-rd2-c3-g-baseline-identity.md` | находка, id — | FR-59: `baseline_identity` — неизвестная сборка старого стенда отказана с дверью (B-281) | `references/gate-registry.json`, `scripts/baseline_contract.py` | пачка 1, RD1-10 (C3-g) | дано: F-O1, 17.11.2026 | B-281 |
| `findings/20261117-rd2-c3-h-stand-identity.md` | находка, id — | FR-59: `stand_identity` — неопознанная сборка стенда спрашивается до стадии (B-257) | `references/gate-registry.json`, `scripts/gate_preflight.py` | пачка 1, RD1-11 (C3-h) | дано: F-O1, 17.11.2026 | B-257; очередь `gate_preflight`: четвёртый |
| `findings/20261117-rd2-c3-i-case-preconditions-rehearsal-cover.md` | находка, id — | FR-59: `case_preconditions`, `reporter_rehearsal_identity`, `environment_property_cover` — одна карточка на общие функции | `references/gate-registry.json`, `scripts/gate_preflight.py`, `scripts/driver_gates.py`, `scripts/stand_gaps.py` | пачка 1, RD1-12 (C3-i) | дано: F-O1, 17.11.2026 | горячий файл `gate_preflight.py`; очередь C3-i → C3-j |
| `findings/20261117-rd2-c3-j-s5-stand-limits-otvet-v-reestre.md` | находка, id — | FR-59: `s5_stand_limits` — неизмеренный предел стенда спрашивается, ответ человека записывается в реестр окружения (B-282) | `scripts/environment_record.py`, `scripts/gate_preflight.py`, `references/gate-registry.json` | пачка 1, RD1-13 (C3-j) | дано: F-O1, 17.11.2026 | B-282; живое доказательство — `live-runs/2` LR2-3; очередь `gate_preflight` |
| `findings/20261117-rd2-c3-k-provenance-acceptance.md` | находка, id — | FR-59: `provenance_acceptance` — неизвестное происхождение идёт вопросом, много сайтов приёма (B-255) | `references/gate-registry.json`, `scripts/execution_request.py`, `scripts/run_suite.py` | пачка 1, RD1-14 (C3-k) | дано: F-O1, 17.11.2026 | B-255; очереди C3-a → C3-k, C3-b → C3-k |
| `findings/20261117-rd2-c4-doroga-bez-stroki-proby.md` | находка, id — | Условие F-O2: язык без строки пробы идёт дорогой пробы роли до приёмки | `scripts/tests/test_probe_by_code.py` | пачка 1, RD1-15 (C4) | дано: F-O2, 17.11.2026 | слово владельца F-O2; RD1-24 (B337); B-373 (`live-runs/2` LR1-1) |
| `findings/20261117-rd2-c5-prompt-dirizhera-zamena-ili-dobavka.md` | находка, id — | Системный промпт дирижёра: заменять или добавлять — один измеренный опыт | `experiments/conductor-system-prompt/` | пачка 1, RD1-16 (C5) | дано: F-O4, 17.11.2026 | слово владельца F-O4; оркестратор → дирижёр |
| `findings/20261117-rd2-s9-slovo-cheloveka-na-review-probele.md` | находка, id — | X10: слово человека на пробеле `review` окно читает как снимающее блок (FR-57) | `scripts/window_record.py`, `scripts/controller.py` | пачка 1, RD1-17 (S9) | нет | X10; живое доказательство — `live-runs/2` LR2-5; очереди S9 → C3-d, S9 → FL4 |
| `findings/20261117-rd2-s10-golovy-chteniya-kak-dannye.md` | находка, id — | G15: головы команд чтения — данными, и `_is_reader` режет `.exe` как символы (`catx` читается как `cat`) | `scripts/stage_guard.py`, `scripts/host_adapter.py`, `references/launch-causes.json` | пачка 1, RD1-18 (S10) | нет | G15; взятые пачки `onboarding-hooks/6`, `/7`, `onboarding-forge/2` |
| `findings/20261117-rd2-fl1-ruchnoj-id-pytest-pri-zapisi.md` | находка, id — | R2: рукописный id pytest разрешается через `node_ids` в момент записи | `scripts/manifest_put.py` | пачка 1, RD1-19 (FL1) | нет | R2; thinking-roles/6 TR4-17 |
| `findings/20261117-rd2-fl2-skip-net-takoj-poverhnosti.md` | находка, id — | R3: «пропущено, потому что у продукта нет такой поверхности» — слово вердикта доставки (FR-21) | `references/delivery-verdict-kinds.json` | пачка 1, RD1-20 (FL2) | нет | R3; очередь C3-e → FL2 |
| `findings/20261117-rd2-fl4-dver-rework-bug-candidate-bez-keysa.md` | находка, id — | R4: дверь доработки S7 для `bug_candidate` без кейса | `scripts/controller.py` | пачка 1, RD1-21 (FL4) | нет | R4; очередь S9 → FL4 |
| `findings/20261117-rd2-fl9-dver-oracle-po-vozmozhnosti.md` | находка, id — | Остаток X2: дверь оракула называет дорогу привязки по возможности языка, а не по pytest | `scripts/s5_precheck.py` | пачка 1, RD1-22 (FL9) | нет | X2; очередь FL9 → C3-c; TBW1-4 (T5r) (`told-before-work/1`) |
| `findings/20261117-rd2-s1b-vtoroj-prohod-fajla-dolga.md` | находка, id — | S1b: второй проход файла долга правил, контроль K0.15 и строки Check у FR-5 и FR-23 | `design/factory-rules-debt.md`, `scripts/tests/test_null_outcomes.py` | пачка 1, RD1-23 (S1b) | нет | ось 4 карты; F-L12, F-L14 |
| `findings/20261117-rd2-b337-raspiska-proby-dlya-ne-python.md` | находка, id — | B-337: `red_sandbox.py --probe` для языка без строки пробы отвечает `incomplete` и не оставляет расписки | `scripts/red_sandbox.py`, `scripts/reporters.py` | пачка 1, RD1-24 (B337) | дано 17.11.2026: «Отдельный П1 на потом» | B-337; RD1-15 (C4); B-373 (`live-runs/2` LR1-1); слово владельца 17.11.2026 |

## Входящие

`findings/` этой кучки; находку, не названную ни в одной пачке, называет `piles.py check --all` (е).
Каждая новая находка тем же ходом получает строку в пачке этой кучки, которую ещё не взяли, или указатель `перенос: <кучка>/…`
(`piles.py check` (е)); нет такой пачки — открывается следующая со статусом «ожидает».

## Вопросы владельцу

- Нет открытых: F-C1 (карточка на гейте A как «вход в стадию») и B-1 («строка сценария» — строка теста дороги) сообщены владельцу; пересмотр — по её слову.

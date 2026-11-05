# Честность прогона: прогон не врёт и не встаёт (релиз после 0.10.3) (`run-honesty`)

приоритет: П1 | фичи: F03, F05, F06, F07, F08, F11, F13, F15, F16 | стенд: нужен только живому доказательству (повтор 12586 на `testproject1-dev-010`) | зона: `ai-packages/qa-factory/scripts/exit_gate.py`, `scripts/story_step.py`, `scripts/story_run.py`, `scripts/controller.py`, `scripts/stage_guard.py`, `scripts/hooklib.py`, `scripts/gate_brief.py`, `scripts/gate_preflight.py`, `scripts/stand_health.py`, `scripts/env_probe.py`, `scripts/run_suite.py`, `scripts/red_sandbox.py`, `scripts/node_ids.py`, `scripts/ledger.py`, `scripts/check_coverage.py`, `scripts/case_stamp.py`, `scripts/probe_by_code.py`, `scripts/proof_level.py`, `scripts/acceptance.py`, `scripts/run_history.py`, `scripts/check_delivery.py`, `scripts/host_probe.py`, `scripts/stage_done.py`, `scripts/brief_pack.py`, `agents/qa-code-critic.md`, `skills/qa-story/phases/s5.md`

## Зачем

Следующий релиз после 0.10.3 собирается из того, что мешает прогону быть честным: фабрика не должна считать неизвестное пройденным, не должна вставать, когда один модуль проекта сломан, и не должна выпускать релиз, у которого красный собственный канон. Пачка собирает в одно место то, что владелец и разведка назвали срочным для следующего прогона истории, и чинит красные канона 0.10.3. После пачки тот же прогон проходит эти места сам, а то, что фабрика не смогла установить, называет по имени и оставляет решение человеку.

## Что не так сегодня (факты)

- Docker-канон релиза 0.10.3 закончился `456/468 ok` и `INSTALL SMOKE: FAILED` (`D:/ws1/canon-release-0103\out\selftest.txt`, `install_smoke.txt`; вне репозитория): регрессия или устаревший тест K11, шесть наборов с красными ключами и A19 над реальным пакетом (`agents/qa-code-critic.md` без `## Procedure`).
- На стенде `testproject1-dev-010` (27.10.2026) сбор тестов обоих профилей (`-m api`, `-m ui`) упал целиком из-за одного устаревшего SDK и одного несуществующего модуля в `conftest.py` проекта; пин SDK в `pyproject.toml` (0.1.704) разошёлся с установленным (0.1.700), фабрика этого не назвала.
- Падение детектора под `story_step finish` читается как «ошибок нет», хук гарда при сбое пропускает проверку молча (`stage_guard.py:830`), одобрение гейта A проходит над неотвеченным пунктом репетиции: класс «неизвестное засчитано как пройденное» (`gates-and-words/findings/20261021-padenie-detektora-na-finish-chitaetsya-kak-pass.md`, `speed-cost/findings/20261027-klass-nemogo-vyvoda-hukov-exit-0.md`).
- Стенд «жив» по контейнеру и мёртв по API; доктор пишет «вход доказан» по неудачному коду 422 (`stand-and-sources/findings/20261026-stend-zhiv-po-kontejneru-mertv-po-api.md`).
- Состав и обоснование — `docs/tasks/handoffs/t-1414-next-release-urgent-survey.md`, раздел 1.

## Пачки

| № | Что изменится для пользователя | Строки | Размер | Статус | Взял | Ветка | MR |
|---|---|---|---|---|---|---|---|
| 1 | прогон не называет неизвестное пройденным (падение детектора, молчащий гард, неотвеченный пункт гейта A), сбор тестов не падает у всех из-за одного модуля, доктор называет устаревшие зависимости и стенд, мёртвый по API, красные docker-канона 0.10.3 починены, проба S6 и читатели статуса считают одну единицу | `batch-1-run-honesty.md` | L (12 узлов) | закрыта | dev1, 27.10.2026 | `pile/run-honesty/batch-1` | `0fa13e6e` |
| 2 | предикат «наследная идентичность» не присоединяет запись с точным `instance_id` к строке чужого теста по кейсу (находка критика K11); остатки пачки 1: актуальность ревью при доставке, принятый риск переноса файла, сырые сравнения байтов вне единого предиката, отказ стража называет `missing`, `s7_round` без дел, аналоги RH1-8 | `batch-2-run-honesty.md` | M (7 узлов) | закрыта | — | — | `855d4e5c` |

Открытое перенесено 01.11.2026 → release-next/1, words-gates/1, execution-report/1, execution-report/2.

Статусы пачки: `ожидает` → `в работе` → `сдано` → `принято` → `закрыта`. Размер — по узлам: S ≤ 4 узлов,
M 5–9, L 10–15 (больше — две пачки). Взятая пачка заморожена: её файл правит только взявший, новое
по теме — файлом в `findings/`.

## Бриф пачки 1

Начать с RH1-1 (критик решает, устарел K11 или это регрессия) и RH1-2 (красные канона: они блокируют любой следующий канон), параллельно — дизайнеры RH1-3 (сбор тестов не падает у всех) и RH1-4 (зависимости). RH1-5, RH1-6, RH1-10 и RH1-12 пишут горячие файлы и идут последовательно (абзац «Очередь по горячим файлам» в файле пачки). Стенд нужен только живому доказательству (повтор TP1-12586 на `testproject1-dev-010`). Слово владельца на состав есть (27.10.2026, сборная пачка релиза); новое слово нужно только развилкам дизайнеров, они поднимаются списком. Подробно — `batch-1-run-honesty.md`, раздел «Бриф».

## Дороги

Читать по порядку: эта карточка → `batch-1-run-honesty.md` → находки узла (колонка «Что» файла пачки; перенесённые находки лежат в кучках-источниках: `gates-and-words`, `speed-cost`, `stand-and-sources`, `hotfix-12586`, `driver-controller`) → разведка `docs/tasks/handoffs/t-1414-next-release-urgent-survey.md` → вывод docker-канона 0.10.3 (`D:/ws1/canon-release-0103\out\selftest.txt`, `install_smoke.txt`) → код зоны по функциям из узла → `design/factory-rules.md`, `design/architecture.md`, `references/human-questions.md`.
Слова: `plans/features.json` F11, F07, F16, F13 (поле `words`) и сверх них: `all_errors`, `_finish_gate`, `Driver.exit_errors`, `unreadable`, `verify_node_ids`, `node_id_collect_timeout_s`, `dependency_state`, `stand_health.probe`, `login_probe`, `test_state`, `instance_id`, `collect_cases`, `_cases_held`, `ticket_rework_step`, `host_probe --check`.
Не читать: остальные узлы кучек-источников (их пачки не взяты и ждут своей очереди) и красные только среды канона (нет `.git` в контейнере, таймауты 300 с) — они не в пачке.

## Содержание

Снимок 27.10.2026; пути — от `ai-packages/qa-factory/`; суть — из находок. При расхождении авторитетна доска `plans/PILES.md`. Перенесённые узлы (RH1-5…RH1-12) держат находки в кучках-источниках, в строке узла файла пачки они названы путём.

| id / файл | вид | суть (≤ 20 слов) | пути | статус | слово владельца | связи |
|---|---|---|---|---|---|---|
| **Пачка 1** | | | | | | |
| `findings/20261027-regressii-docker-kanona-0-10-3-k11-i-krasnye-selftest-install-smoke.md` | находка | docker-канон 0.10.3 красный: K11 `ledger.test_state`, шесть наборов и A19 над реальным пакетом (роль без `## Procedure`) | `scripts/ledger.py`, `scripts/tests/`, `agents/qa-code-critic.md` | пачка 1, RH1-1, RH1-2 | да, 27.10.2026 (сборная пачка релиза) | t-1414 §0; forge F6-43…F6-45 |
| `findings/20261027-collect-padaet-u-vseh-iz-za-odnogo-modulya.md` | находка | один битый модуль проекта роняет сбор тестов целого профиля; фабрика не называет битые файлы и не едет дальше | `scripts/run_suite.py`, `scripts/red_sandbox.py`, `scripts/node_ids.py` | пачка 1, RH1-3 | да, 27.10.2026 (сборная пачка релиза) | RH1-4 |
| `findings/20261027-ustarevshie-zavisimosti-proekta-posle-obnovleniya-vetki.md` | находка | пин SDK проекта разошёлся с установленным, фабрика и доктор не назвали; нужна команда проекта `dependency_state` | `scripts/gate_preflight.py`, `scripts/env_probe.py` | пачка 1, RH1-4 | да, 27.10.2026 (сборная пачка релиза) | RH1-3; conductor C3-18 |
| **Пачка 2** | | | | | | |
| `findings/20261027-legacy-identity-ignoriruet-instance-id.md` | находка | `legacy_identity_is_the_case` игнорирует `instance_id`: запись с точным id присоединяется к чужой строке по кейсу | `scripts/contract.py`, `scripts/tests/test_case_id_form_sites.py` | пачка 2, RH2-1 | нет | вердикт t-1416 (RH1-1) |
| `findings/20261028-aktualnost-revyu-pri-dostavke-posle-pravki-vne-skoupa-e8.md` | находка | ревью, ставшее неактуальным после правки вне скоупа, при доставке не проверяется (бывшая половина `review_stale`); вариант C | `scripts/check_delivery.py`, `scripts/proof_level.py` | пачка 2, RH2-2 | нет | RH1-9, t-1363 R7 |
| `findings/20261028-perenos-fajla-i-legacy-nositel-prinyatyj-risk-f5.md` | находка | перенос файла и легаси-носитель без идентичности читаются `raw`: принятый риск (Lead пачки, 27.10) | `scripts/proof_level.py` | пачка 2, RH2-3 | нет | RH1-9 F5 |
| `findings/20261028-bajtovye-sravneniya-ostalis-v-probe-by-code-red-sandbox-window-record-f6.md` | находка | сырые sha и пути остались вне предиката «тот же тест»: `probe_by_code`, `red_sandbox`, `window_record`, четыре близнеца путей | `scripts/probe_by_code.py`, `scripts/red_sandbox.py`, `scripts/window_record.py`, `scripts/sizing.py` | пачка 2, RH2-4 | нет | RH1-9 F6, RH1-3, RH1-8 |
| `findings/20261028-rh1-11-otkaz-strazha-i-zametka-host-capabilities-ne-nazyvayut-missing.md` | находка | отказ стража и заметка `host_capabilities` не называют `missing`; отказ пробе другой сессии безымянный | `scripts/stage_guard.py`, `scripts/host_capabilities.py` | пачка 2, RH2-5 | нет | RH1-11, t-1418 |
| `findings/20261028-s7-round-mozhet-poslat-rework-s5-bez-del.md` | находка | `Driver.s7_round` может отправить доработку S5 без дел и получить отказ контроллера (форма открытого пункта гейта A) | `scripts/story_run.py` | пачка 2, RH2-6 | нет | RH1-6, DC1-13 |
| `findings/20261028-analogi-rh1-8-lifecycle-reasons-immutable-proof-collect-cases.md` | находка | три аналога RH1-8: точный ключ в `lifecycle_reasons`, `immutable_proof` без `cfg`, молчаливый `except: continue` в `collect_cases` | `scripts/check_delivery.py`, `scripts/case_stamp.py`, `scripts/check_coverage.py` | пачка 2, RH2-7 | нет | RH1-8, t-1430 А9 |
| `findings/20261029-tajmaut-pytest-prochitan-kak-stend-ne-rabotaet.md` | находка | тест убит таймаутом pytest проекта, а фабрика сказала человеку «стенд не индексирует»; стенд источник проиндексировал | `scripts/run_suite.py`, `scripts/brief_pack.py`, `agents/qa-automator.md` | пачка 2, RH2-9 | да — в 0.10.7 (владелец, 29.10.2026) | SC2-40, HF8-16 |
| `findings/20261028-chitateli-uv-lock-pdm-lock-po-formatam.md` | находка | `uv.lock` и `pdm.lock` отданы в `unknown`; читатель на формат — на фикстурах из настоящих lock-файлов (маркер на звене uv, строки без версии, ключ `marker` pdm) | `scripts/dependency_drift.py`, `references/project-dependencies.json` | пачка 2, RH2-8 | нет | RH1-4, критик t-1451 B1 |

## Входящие

`findings/` этой кучки; их число и дату последней показывает `plans/PILES.md` (собирает `piles.py board`; карточку код не правит).
Каждая новая находка тем же ходом получает строку в пачке этой кучки, которую ещё не взяли, или указатель `перенос: <кучка>/…`
(`piles.py check` (е)); нет такой пачки — открывается следующая со статусом «ожидает».

## Вопросы владельцу

- нет: состав пачки и исправления, чтобы сбор тестов не падал, подтверждены словом владельца 27.10.2026.

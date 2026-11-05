# Дирижёр собирает штатные ходы руками: 19 из 165 Bash-вызовов — python-heredoc; серия отказов из-за аргументов

id: — | кучка: `driver-hosts` | от: прогон CART-1 (MyBooks), 31.10.2026 | приоритет: П2 | кандидат наверх: нет

Склейка: пункты 7.6 и 7.8 свода — один класс («у дирижёра нет готовой команды штатного хода, а отказ не называет недостающий аргумент») и один узел.

## Что наблюдалось

Свод пп. 7.6 и 7.8; отчёт `docs/tasks/specs/reports/t-1633-cart1-run-problems-transcript.md`, строки 3, 10, 12, 14, 20, 23, 26 и раздел 2, класс 5; всего 19 из 165 Bash-вызовов дирижёра — `python -c` / heredoc.
- `initialize` (строка 3, S1 start, L131–150): `story_step: refused - initialize task before work`; дирижёр читал `controller.py`, руками собрал JSON запроса `initialize` (`source_revision` из `git rev-parse`) ≈ 1,5 мин; повторится в каждой истории.
- `revise_plan` (строка 10, S4, L696–724): отказ «scope expansion requires plan/gate revision … the door is controller.py --operation revise_plan»; дирижёр сам вычислил `sha256` `test-plan.json` и собрал JSON на 12 id ≈ 2 мин.
- values-файл формы питоном (строка 12): добавил «фантомную» четвёртую запись scope с `<case id>`, вырезал блок YAML питоном ≈ 1,5 мин.
- `waiver.py` (строка 14, гейт A): четыре попытки подряд — без обязательных аргументов («--task, --stage, --block and --decision or --words-file ... are all required»), затем на стадию S4 вместо S5 ≈ 5 мин.
- `finish --digest -` (строка 20, L1032): отказ «no digest recorded … pass the role's digest line»; `--digest` в `--help` не объясняет, что `-` — «дайджест, который выход роли записал сам» (`story_step.py:2975`–`:2983`), дирижёр читал `-` как stdin.
- `finish` критика без `--complete` (строка 11): отказ контроллера «accepting S4-qa-case-critic-1 with stage_complete: false leaves S4 with no role to close it» говорит на языке контроллера (`controller.py:5025`–`:5031`), не флагом `story_step finish --complete`.
- `project_decisions.py add-finding` без `--witness` (строка 23): отказ называет оба варианта (`--witness` или `--words-file`) — исправлен со второй попытки, менять нечего.
- `review_receipt_ref` для OB-5…OB-9 (строка 26): известно, `driver-controller/findings/20261030-otkaz-kritika-okna-s5-quittanciya-i-vozvrat-avtoru-ostatki.md` — здесь не берётся.
- правка `config.json` питоном (строка 30, рантайм-проба `*`, 8 мин ремонта): ход владельца для стенда без docker; корень — `execution-probes/findings/20261031-stend-bez-docker-ruchnaya-proverka-ne-sprashivaet-versiyu.md` — здесь не берётся.

Существует: у драйвера эти ходы уже есть — `StoryRun.initialize()` (`story_run.py:5857`) и `StoryRun.revise_plan()` (`:8661`); у `story_step` подкоманд `initialize` и `revise-plan` нет (`story_step.py:2950`–`:3018`: start, materialize, bind, finish, decide, pause, resume, where, card, config-snapshot, config-restore).

Связь: SC5-3 (qa-story как оболочка над драйвером: дорога дирижёра шаг за шагом снимается) — после неё этот узел сужается до отказов; он исполним независимо, потому что 0.11.0 не завтра.

## Класс

У дирижёра нет готовых команд для штатных ходов (P3: дирижёр — помощник, не сборщик JSON; FR-48), а отказ, который не называет недостающий аргумент или флаг командой, заставляет читать код (FR-1, FR-2). Не проект: любой проект получает `initialize` на первой истории.

## Что именно менять

Направление выбрано: одни и те же методы драйвера, вторая дверь — подкоманда `story_step` (один писатель, AR-14, AR-15).
1. `scripts/story_step.py`: подкоманды `initialize --task T` и `revise-plan --task T`, тела — вызовы `StoryRun.initialize()` и `StoryRun.revise_plan()` без копий логики. `revise-plan` без закреплённых кейсов: выход 2 и строка «nothing is pinned; run case_versions.py --task-root … --all first» (метод драйвера в этом случае возвращается молча — для дирижёра это тихий пропуск, FR-41). Тесты в `scripts/tests/test_story_step.py`: свежая история → `start` отказывает «initialize task before work» и в тексте стоит `story_step.py initialize --task`; после `initialize` — `start` проходит; `revise-plan` дважды подряд даёт один и тот же scope (идемпотентность `idempotency_key`, `story_run.py:8693`); без закреплённых кейсов — выход 2.
2. Тексты отказов называют команду `story_step`: «initialize task before work» (`controller.py:4587`, `:8005`, фраза читается драйвером `story_run.py:213` — не менять слова, добавить хвост «; story_step: `story_step.py initialize --task <task>`»); «scope expansion requires plan/gate revision» (`controller.py:2150`–`:2158`, `:2307`) — хвост `story_step.py revise-plan --task <task>`; `finish` без `--complete` — перевод на `story_step finish … --complete` там, где `story_step` печатает отказ контроллера (где именно — не проверено: искать место вызова `controller.accept` рядом с `REPAIR_MARKER`). Тест на каждый: подстрока команды в тексте отказа.
3. `scripts/waiver.py` (`:1295`, `:1299`, `:1304`, `:1308`): `ap.error` называет, КАКИХ из аргументов нет (`--block` отсутствует), а не весь список; тест в `scripts/tests/test_waiver_release.py`: вызов без `--block` — в тексте `--block` и нет `--gate`.
4. `story_step.py:2977`: `help` у `--digest` — «`-` takes the digest the exit gate recorded for this dispatch (no stdin)»; тест на `--help`.
5. Не менять: `project_decisions.add-finding` (отказ уже называет дверь), `review_receipt_ref`, `config.json` (см. выше, чужие находки).

Принципы и правила: P3, P11, P12, FR-1, FR-2, FR-41, FR-48, AR-9, AR-14, AR-15.

Решение владельца нужно: нет.

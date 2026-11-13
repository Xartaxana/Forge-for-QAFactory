# Codex: перенос фиксов ветки `dev2/codex-overhead-fixes` (`codex`)

приоритет: П1 | фичи: F05, F12, F21 | стенд: только для живого доказательства | зона: `ai-packages/qa-factory/scripts/{host_adapter,host_probe,host_dispatch,dispatch_liveness,worker_lifecycle,story_progress,stage_guard,exit_gate,launch_card,story_step,brief_pack,controller,gate_preflight}.py`, `hooks/codex.json`, `references/{controller-api,conductor,codex-host}.md`

## Зачем

dev2 прогнала TP2-2406 на Codex (Desktop и CLI) и на своей ветке исправила то, из-за чего прогон вставал:
роль без оболочки получала команды, которые гард ей запрещает; чужая стори держала выход; возобновление уходило в чужую
стори; карточка запуска терялась; проверка скоупа отказывала на собственных окнах контроллера; оркестратор сам ждал ролей
(46% входных токенов). Ветка отстала от `main` на 872 коммита: фиксы переносятся по одному, на код `main`, с её тестами, так
чтобы решения `main` (один отказ списком, слово человека одной дверью, недостижимое без вопроса) остались целыми.

## Что не так сегодня (факты)

- 30 коммитов ветки, 17 фрагментов changelog, 14 файлов с конфликтом (32 ханка) — карта `docs/tasks/specs/reports/t-921-codex-branch-map.md` §1–§3.
- `controller.py --task X` молча становится `--task-root X` (`controller.py:4954`, нет `allow_abbrev=False`) — карта §3b.
- проба контекста просит 48 hex (`host_probe.py:396`), дети Codex теряют хвост — находка onboarding-hooks.
- четыре читателя строки `tools:` роли с противоположным умолчанием — карта §7.

## Пачки

| № | Что изменится для пользователя | Строки | Размер | Статус | Взял | Ветка | MR |
|---|---|---|---|---|---|---|---|
| 1 | прогон на Codex не встаёт там, где встал 2406: роль без оболочки слышит только свои инструменты, стори и возобновление — только свои, карточка запуска не теряется, скоуп сравнивается по ключам; драйвер гоняет стори через Codex CLI | — (находки ветки, перенос 30 коммитов; 16 узлов) | L (16 узлов, предел L не действует: владелец, 19.10.2026) | закрыта | — | `pile/codex/batch-1` | `855d4e5c` |
| 2 | остатки пачки 1: читатель роллаутов хоста (сжатые `.zst`, thread id), один читатель времени, фразы для `codex-host.md`, аналоги гарда за CX1-20 (ANSI-C, присваивание PS, SKILL.md:225); перенос четырёх коммитов dev2 по блокерам S5 прогона 2406 (проекция манифеста, кейс с областью, присваивания PS в гарде, `SubagentStop` при `story_step`) | — (находки 19–20.10 + очереди критиков + дополнение dev2 20.10) | L (15 узлов) | закрыта | — | `pile/codex/batch-2` | `855d4e5c` |

Открытое перенесено 01.11.2026 → words-gates/1, driver-hosts/1, execution-report/1, driver-hosts/2, onboarding-forge/2.

Статусы пачки: `ожидает` → `в работе` → `сдано` → `принято` → `закрыта`. Взятая пачка заморожена: её файл правит только
взявший, новое по теме — файлом в `findings/`.

## Решения

- Одна пачка `codex` на все узлы (16), предел L для неё не действует — владелец, 19.10.2026: «одна пачка codex на все узлы,
  предел L для неё не действует». Черновик t-924 вёл три пачки (14 + входящие + драйвер/FB-14); узлы драйвера и FB-14 стали
  CX1-15 и CX1-16 в конце порядка.
- Развилки 1–10 черновика решил Lead, 19.10.2026 (§L черновика `docs/tasks/specs/t-924-codex-batch-1-draft.md`, по вердикту
  критика на план `docs/tasks/specs/reviews/t-927-t-924-codex-plan.md`); где §L и текст черновика расходятся, §L главнее.
- Слова «владелец решил» в документах dev2 — её решения как оператора своих сессий, не владельца (D-0025).

## Бриф пачки 1

- Узлы — ПЕРЕНОСЫ, не cherry-pick: узел берёт группу фиксов (или её связный кусок), переписывает на текущем коде `main`,
  несёт её тесты (адаптированные) и держит зелёными тесты `main`. Порядок — по риску (волны в файле пачки, преамбула).
- Стенд нужен для живых доказательств (FR-33). Подробно — `batch-1-overhead-fixes.md`, разделы «Бриф» и «Края узлов».

## Дороги

Читать по порядку: эта карточка → `batch-1-overhead-fixes.md` → карта `docs/tasks/specs/reports/t-921-codex-branch-map.md`
(§3 — ханки своего узла) → черновик `docs/tasks/specs/t-924-codex-batch-1-draft.md` (§L главнее текста) и вердикт
`docs/tasks/specs/reviews/t-927-t-924-codex-plan.md` → спека/вердикт dev2 узла (`docs/tasks/codex-2406/`; пока её
документы не перенесены — `git show 62710646:<путь>`) → `git show 62710646:<путь>` её кода и тестов → код зоны на `main` по
функциям «Пишет в» → правила: `design/factory-rules.md` A, C, D, G; `docs/SIBLING_MAP.md` оси 5, 8, 11, 13, 14, 17, 18;
`docs/tasks/critic-diff-brief.md`.
Слова: F05, F12, F21 (`plans/features.json`) и сверх них: `codex`, `exec_command`, `apply_patch`, `bound_by`, `task_complete`,
`launch_card`, `materialize`, `_raise_all`, `scope_keys`, `command_segments`, `role_tools`, `source-receipt`.
Не читать: `logs/journal/*.jsonl`, отчёты о деплое ветки (bbed577e, f4f58455, 62710646), зону `story_run.py` вне Driver.

## Содержание

Снимок 19.10.2026; пути — от `ai-packages/qa-factory/` (вне пакета — от корня); находки — из их файлов. Каждая находка лежит
в `findings/` этой кучки и стоит строкой в таблице «Находки кучки» файла пачки 1. Остатки находок, которые черновик t-924 вёл в
узлы пачки 2 (CX2-n), в этой пачке привязаны к узлу CX1-n из колонки «связи».

| id / файл | вид | суть (≤ 20 слов) | пути | статус | слово владельца | связи |
|---|---|---|---|---|---|---|
| **Пачка 1** | | | | | | |
| `findings/20261012-desktop-launch-card-lost-after-exec-yield.md` | находка | карточка запуска теряется за yield exec-ячейки; `next` отвечает `wait_existing_job` | `scripts/story_step.py`, `scripts/controller.py` | пачка 1, CX1-13 | нет | — |
| `findings/20261013-state-portability-launch-card-red.md` | находка | `test_state_portability` красный: у карточки запуска нет строки `file_writers` | `scripts/tests/fixtures/env-facts-baseline.json` | пачка 1, CX1-13 | нет | — |
| `findings/20261014-receipt-active-readers.md` | находка | расписка `running` держит чекпоинт, роллаут `task_complete` не виден | `scripts/dispatch_liveness.py`, `scripts/worker_lifecycle.py` | пачка 1, CX1-3 | ось — да | — |
| `findings/20261015-controller-task-abbrev-phantom-root.md` | находка | `--task` читается как `--task-root`, контроллер пишет в фантомную стори | `scripts/controller.py` | пачка 1, CX1-10 | нет | — |
| `findings/20261015-scope-ticket-key-and-tc005-question.md` | находка | скоуп = ключ тикета; незаданный вопрос TC-005 | `scripts/controller.py`, `scripts/gate_preflight.py` | пачка 1, CX1-11 | нет | — |
| `findings/20261016-scope-identity-siblings.md` | находка | редьюсеры и `_covers` сравнивают скоуп буквально; квалификатор уникального номера не проверяется | `scripts/controller.py` | пачка 1, CX1-11 (остаток; черновик — CX2-8) | нет | — |
| `findings/20261012-exit-gate-story-resolution-leftovers.md` | находка | второй резолвер `_ticket_for_stage` угадывает свежий pipeline; оси «стори события хука» нет | `scripts/exit_gate.py` | пачка 1, CX1-8 (остаток; черновик — CX2-2) | ось — да | — |
| `findings/20261013-binding-readers-writers.md` | находка | два писателя и восемь читателей привязок без оси | `scripts/host_dispatch.py` | пачка 1, CX1-8 | ось — да | — |
| `findings/20261016-resume-identity-siblings.md` | находка | догадка «единственная running» на Claude, отказ резюма без тикета, третий сравниватель имён | `scripts/stage_guard.py`, `scripts/worker_lifecycle.py` | пачка 1, CX1-9 (остаток; черновик — CX2-10) | нет | — |
| `findings/20261012-launch-card-leftovers.md` | находка | остатки карточки: свидетельства без имён, безадресные отказы, `stage_done` 57 с | `scripts/launch_card.py`, `scripts/story_step.py` | пачка 1, CX1-13 (остаток; черновик — CX2-3); частично: SC1-12 speed-cost/1 (п. 6) | нет | — |
| `findings/20261015-materialize-siblings-and-recompute.md` | находка | драйвер и другие диспатчи мимо `start`; перерасчёт `input_hash` | `scripts/story_run.py`, `scripts/story_step.py` | пачка 1, CX1-14 (остаток; черновик — CX2-6, CX2-7) | нет | — |
| `findings/20261013-context-probe-challenge-copy.md` | находка | ребёнок Codex теряет хвост 48-hex challenge | `scripts/host_probe.py` | пачка 1, CX1-2 | нет | — |
| `findings/20261014-no-shell-roles-named-commands.md` | находка | тексты называют команды оболочки ролям без Bash | `scripts/brief_pack.py`, `scripts/story_step.py` | пачка 1, CX1-6 | нет | — |
| `findings/20261015-plan-access-leftovers.md` | находка | `hooklib._scan` в PowerShell не знает типографских кавычек | `scripts/hooklib.py` | пачка 1, CX1-5 | нет | — |
| `findings/20261016-codex-claude-only-texts-and-tools-line-readers.md` | находка | тексты Desktop называют только инструменты Claude; читатели `tools:` расходятся | `references/common-rules.md`, `scripts/guard_pre_tool.py` | пачка 1, CX1-6 | нет | — |
| `findings/20261018-s5-branch-check-carrier.md` | находка | роль S5 сверяет ветку по имени: носитель записи не назван | `scripts/brief_pack.py`, `agents/qa-automator.md` | пачка 1, CX1-7 | нет | — |
| `findings/20261019-cx1-3-queue-controller-api-sentences.md` | находка | фразы о возврате по роллауту для `codex-host.md` | `references/codex-host.md` | пачка 2, CX2-11 (или CX1-11 при создании файла) | нет | — |
| `findings/20261019-cx1-3-queue-second-time-reader.md` | находка | несколько читателей «времени без зоны» в `dispatch_liveness`, дубль `_iso` | `scripts/dispatch_liveness.py`, `scripts/story_progress.py` | пачка 2, CX2-12 | нет | — |
| `findings/20261019-cx1-3-queue-zst-rollouts.md` | находка | роллауты Codex сжаты `.jsonl.zst`, декодера нет; идентичность по thread id; порядок хуков SubagentStop | `scripts/dispatch_liveness.py`, `scripts/codex_usage.py` | пачка 2, CX2-13 | кандидат наверх | — |
| `findings/20261019-prefiltry-vne-scan-skleyka-podstanovki-i-obratnaya-kosaya-v-flage.md` | находка | гард читает подстроку, не слово оболочки: склейка подстановкой, `--p\re`, `find -exec`, метка хоста | `scripts/hooklib.py`, `scripts/stage_guard.py`, `scripts/host_adapter.py` | пачка 1, CX1-20 (остаток — пачка 2, CX2-14); частично: SC1-5 speed-cost/1 | нет | — |
| `findings/20261019-cx1-4-env-probe-unchecked-passes-without-env.md` | находка | `env_probe` без `--env`: блок без адреса даёт `liveness: unchecked` и выход 0 | `scripts/env_probe.py` | пачка 2, CX2-15 | нет | — |
| `findings/20261019-cx1-4-gate-preflight-stand-address-rule.md` | находка | `gate_preflight` читает адрес стенда не так, как `env_probe`: кортеж ключей, выбор записи, пустой адрес | `scripts/gate_preflight.py`, `scripts/env_probe.py` | пачка 2, CX2-15 | нет | — |
| `findings/20261019-cx1-4-kill-tree-twins.md` | находка | две копии убийства дерева процессов остались рядом с `node_ids.kill_tree` | `scripts/run_suite.py`, `scripts/node_ids.py` | пачка 2, CX2-15 | нет | — |
| `findings/20261019-cx1-4-node-toolchain-for-clone-install.md` | находка | установка зависимостей в клон требует `npm` на PATH, Node-инструментарий фабрика не определяет | `scripts/project_env.py`, `scripts/node_ids.py` | пачка 2, CX2-15 | нет | — |
| `findings/20261019-cx1-4-role-sentence-sandbox-setup.md` | находка | роль не знает `sandbox_setup`: нужна готовая фраза для `execution-lifecycle.md` | `agents/*.md`, `references/execution-lifecycle.md` | пачка 2, CX2-15 | нет | — |
| `findings/20261019-cx1-4-scheduler-exit-zero-without-result.md` | находка | планировщик: ребёнок с кодом 0 без сводки не `completed`; остались аналоги | `scripts/execution_scheduler.py` | пачка 2, CX2-15 | нет | — |
| `findings/20261019-cx1-4-stand-health-global-liveness-under-env.md` | находка | `stand_health` при `--env` опрашивает и глобальный адрес блока `environment` | `scripts/stand_health.py` | пачка 2, CX2-15 | нет | — |
| `findings/20261019-cx1-4-url-scrubber-twins.md` | находка | два скраббера адреса рядом с `http_client.safe_url` | `scripts/stand_access.py`, `scripts/stand_health.py` | пачка 2, CX2-15 | нет | — |
| `findings/20261020-obrabotchiki-garda-fail-open-i-str-list-posle-cx1-20.md` | находка | обработчики гарда после CX1-20: fail-open на не-walker исключении, чтения `str(list)`, след одиночной ошибки | `scripts/guard_pre_tool.py`, `scripts/stage_guard.py`, `scripts/host_adapter.py` | пачка 2, CX2-16 | нет | — |
| `findings/20261020-sem-mest-imeni-stori-vne-dverej-i-ostatki-cx1-11.md` | находка | семь мест имени стори в `controller.py` вне дверей и остатки критика CX1-11 | `scripts/controller.py`, `scripts/story_run.py`, `scripts/contract.py` | пачка 2, CX2-17 | нет | — |
| `findings/20261020-slovo-s1-waiver-prohodit-stage-done-no-ne-kontroller-i-p13.md` | находка | слово `waiver.py --stage S1` проходит `stage_done`, но не контроллер; `stage_overrides` с цитатой отказа не доходит ни до кого | `scripts/waiver.py`, `scripts/source_preflight.py`, `scripts/controller.py` | пачка 2, CX2-18 | нет | — |
| `findings/20261020-otkazy-bez-dorogi-vpered-source-inputs-i-accept-gap.md` | находка | отказы без дороги вперёд: `source_inputs` печатает сырой `str(summary)`, `accept-gap` не перечисляет допустимые id | `scripts/controller.py`, `scripts/story_run.py` | пачка 2, CX2-19 | нет | — |
| `findings/20261020-u-skills-net-dveri-receipts-dlya-stori-v-polete.md` | находка | у дорожки skills нет двери `receipts` для стори в полёте: её проходит только драйвер | `skills/qa-story/**`, `scripts/story_run.py` | пачка 2, CX2-20 | нет | — |
| `findings/20261020-install-md-shag-7-i-skill-md-33-nazyvayut-drajver-putyom-stori-na-codex.md` | находка | INSTALL.md шаг 7 и SKILL.md:33 зовут драйвер путём стори на Codex; путь один на обоих хостах — навык | `INSTALL.md`, `skills/qa-story/SKILL.md`, `design/driver.md` | пачка 2, CX2-26 | да, 20.10 20:1x | `kb` (KB2-3) |
| `findings/20261020-dev2-addendum-s5-blockers-62710646-3fa8783e.md` | дополнение передачи | четыре коммита dev2 по блокерам S5 прогона 2406: проекция манифеста и `--recover`, кейс с областью одним читателем, присваивания PS в гарде, `SubagentStop` не возвращает `story_step`-диспатч | `scripts/manifest_put.py`, `scripts/event_store.py`, `scripts/execution_request.py`, `scripts/s5_precheck.py`, `scripts/contract.py`, `scripts/stage_guard.py`, `scripts/subagent_journal.py` | пачка 2, CX2-21…CX2-24 | да (20.10 14:4x: «в батч-2 по Кодексу») | CX1-20, CX1-13, CX1-18, CL1-5, CX2-14, CX2-17 |
| `findings/20261020-shest-chitatelej-raunda-kritika-mimo-scoped-verdict.md` | находка | шесть читателей слова критика читают весь `critic-findings.md`, не раунд расписки; драйвер ветвится по прозе, не по `verdict_basis` | `scripts/controller.py`, `scripts/gate_brief.py`, `scripts/gate_preflight.py`, `scripts/story_run.py` | пачка 2, CX2-25 | нет | CX1-12 |
| `findings/20261028-strazh-chitaet-komandu-s-peremennoj-i-podstanovkoj-kak-gh-pr-create.md` | находка | страж принимает команду с `$var` и `$(...)` за `gh pr create`: ложный отказ на S2 с дверью гейта B, которой там нет | `scripts/adapter_forms.py`, `scripts/stage_guard.py` | пачка 2, CX2-27 | нет | CX1-20, CX2-14; TP1-12586 |

## Входящие

`findings/` этой кучки; находку, не названную ни в одной пачке, называет `piles.py check --all` (е). Новая находка тем же ходом получает строку в пачке 1, пока её не
взяли; после взятия — открывается следующая пачка со статусом «ожидает» (`piles.py check` (е)).

## Вопросы владельцу

Открытых вопросов нет: все развилки черновика t-924 решены Lead в его §L (слово владельца — по одной пачке на все узлы,
19.10.2026).

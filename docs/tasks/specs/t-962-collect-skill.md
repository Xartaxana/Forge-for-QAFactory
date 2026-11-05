# t-962 — скилл COLLECT: данные проекта, работающего на фабрике, — обратно разработчикам фабрики; приём на нашей стороне

Дизайнер (Opus 5.5), 19.10.2026, по брифу Lead. Черновик: развилки — §F, ни одна не решена; «[рек.]» — рекомендация, действует только после §L.
Пути пакета — от `ai-packages/qa-factory/`; проекта — от его корня (папка с `qa-factory/config.json`); `<T>` = `qa-factory/artifacts/<TASK>/`.
Закон — D-0052 (`DECISIONS.md:70`, 7 пунктов); факты — перепись t-948 (A–J, якоря; принята Lead по следу), ссылки вида «t-948 B».

**Свежесть (Read/Grep 19.10, рабочее дерево `main`):** D-0052; `plans/PILES.md` (15 кучек); строки `фичи:` всех карточек `plans/piles/*/README.md`;
`plans/features.json` (F01–F21); `tools/piles.py:1-70, 700-735` (форма находки), `:1908-2051` ((е)); `tools/test_pile_cards_contents.py:1, 53-56`;
`tools/dev_config.py`; пакет: `guard_secrets.py`, `project_decisions.py:20-45, 183-213`, `archive_task.py:1-146`, `dispatch_liveness.py`, `report_adapt.py:1-40`,
`runtime_paths.py:1-80`, `install-paths.json`, `skills/qa-doctor/SKILL.md`, `references/human-questions.md:1-90`, `references/conductor.md:30-70`,
`agents/qa-retro-analyst.md:41-75`, `scripts/tests/state_census.py:80-279`, `hooklib.py` (`story_closed`:221, `artifact_root`:262, `read_json`:286,
`story_subagent_transcripts`:1184, `version_carriers`:1376), `activity_capture.py:14`, `person_words.py`, `hooks/hooks.json`; форма пачки — `codex/batch-1`.

## §1. Цель и инварианты

Цель: человек на своём проекте вызывает `/qa-factory:qa-collect`, отвечает (или нет) на два вопроса и получает ОДИН файл для отправки нам; мы
запускаем `tools/collect_intake.py` — находки ложатся в кучки своих фич, предложения — в новую кучку, числа — в `cost-dashboard`.

- **I1 (всё, без выбора).** Каждый набор A–H собирается всегда (D-0052 (2)); отсутствующий — строка `gaps[]` с причиной; ни молчания, ни падения (P2, FR-41).
- **I2 (ни байта неочищенным).** Ничто не попадает в архив мимо редактора (§4); непрочитанное им (не UTF-8, бинарное, битый JSON) — `skipped[]`.
- **I3 (окно без дыр).** Новизна не пропускает записей: при сомнении (префикс иной, метки нет, метка чужая) — файл целиком с флагом; дубли гасит приём.
- **I4 (молчаливого среза нет).** Всё, что не скопировано целиком, — строка манифеста: `sum` (что вместо), `skipped` (почему), `too_large`.
- **I5 (дёшево).** В скилле нет роли и нет вызова LLM (FR-51, D-0052 (6)); агент — два вопроса, один Bash, дословная сводка; место нестандартного
  он называет, только когда скрипт сказал «not found at the standard place».
- **I6 (деньги не в git проекта).** Архив несёт расход (C) и пишется только туда, где git его не видит — по проверке `git check-ignore`, не допущению.
- **I7 (ответ человека читает человек).** Код хранит два ответа дословно и не классифицирует (FR-12, D-0052 (1)); у нас они идут Lead.

## §2. Наборы (пути — t-948)

Режимы: **copy** — целиком через редактор; **tail** — хвост после метки (§3); **new** — файлы каталога новые или с иным sha256; **sum** — сводка
(поля названы); **skip** — не берётся (причина). Файлы истории `<T>` — только у историй, тронутых с метки (`events.jsonl`/`pipeline.json` изменились).

**A. Паспорт** («с чем фабрика справляется, а с чем нет»)

| что | путь | режим | причина / что вместо |
|---|---|---|---|
| версия, хост, отпечаток | `hooklib.version_carriers()`; `readiness.json → runtime_paths.package_version/package_fingerprint`, `host_integration.host` | sum | факты; `plugin_root`/`python_executable` — только класс |
| readiness, config | `qa-factory/state/readiness.json` (22 КБ), `qa-factory/config.json` (43–68 КБ) | copy | capabilities = «что не встало»; профили, стек, `code_repos`, `test_locations`; URL/remote — F-6 |
| ОС, python, репозитории | процесс сборщика (`platform`, `sys.version_info`); `project_inventory.build_inventory` | sum | role, presence, git_status; remote — `_safe_remote` + F-6; нет git — `git: absent` |
| установка | `install-manifest.json` sum (версия, счёт по `class`); `records/onboarding-approvals.jsonl` tail; `state/retired/*/retire-record.json` new | — | дата установки ≈ самый ранний `recorded_at` |
| стратегия, онбординг | `qa-factory/strategy/*.md` copy; `state/onboarding/` sum (`onboarding_notes.py status`) | — | профиль — ядро паспорта; слова интервью — про продукт |
| пробы, квитанции | `state/host-probe.json`, `state/doctor-install-smoke-latest.json` copy; `state/host-receipts/` (1022 ф.) sum | — | `detect_host`, счёт по `host`, версии из `package-<session>.json`; проб скилл НЕ запускает |
| резервы конфига, карта кода | `records/config-migrations/*.json`, `<T>work/briefs/repo-map-*.md` | skip | текущего конфига хватает; карта кода продукта |

**B. Ход прогона**

| что | путь | режим | причина |
|---|---|---|---|
| события | `<T>state/events.jsonl` (до 2.4 МБ) | tail | `sequence` + `event_hash` (§3) |
| проекции | `<T>state/controller.json`, `checkpoint.json`, `driver-state.json`, `<T>pipeline.json` | copy | снимок; `stage_overrides[]` — след «слово через отказ» (D) |
| журналы | `<T>state/driver-runs.jsonl`, `conductor.jsonl`, `driver-questions.jsonl`, `driver-answers.jsonl`, `dispatch-denials.jsonl`; `records/journal.jsonl` (старое `state/journal.jsonl`, ключ `journal_path`) | tail | префикс (§3) |
| файлы драйвера, квитанции | `<T>state/driver-runs/*.json`, `driver-question*.md`, `<T>state/words/*.txt`; `state/host-dispatches/*.json` | new | слова человека фабрике — запись, не продукт |
| телеметрия, исполнение | `state/telemetry/` (4345 ф.); `<T>state/execution-jobs/`, `<T>work/run-blocks/`, `state/scheduler-receipts/` | sum | файлы, байты, счёт `span_kind×outcome×reason_code` по дням (рост — данные B-107); статусы |
| доказательства | `<T>evidence/**` (до 11.6 МБ, 697 ф.) | sum | индекс: путь (через редактор), байты, sha256; содержимое НИКОГДА (логи прогонов несут данные продукта и секреты) |
| блоки exit-gate | `state/.exit_gate_blocks.json` | copy | мал |

**C. Деньги** (куда идут — §3 п. 6, F-11): `state/cost/<sid>.json` new (`transcript` → `<transcript:<sid>>`; `.writers/` skip — замки);
`state/turns/`, `state/window/`, `state/activities/` new (активности — цена дирижёра, P18); `<T>work/retro-numbers.json` copy (`.md` skip — рендер);
`records/estimation-ledger.jsonl` tail; тарифы — skip (`config.cost` уже в копии A, таблица пакета известна по версии).

**D. Адаптации** (не дифф, D-0052 (3); след — по правилу F-1): `factory-backlog.md` + `records/project-decisions.json` (≈27 КБ) copy целиком
(новизну решает приём по `FB-n` + `idempotency:`); `records/report-adaptations.json` (единственная адаптация в коде, t-948 D),
`records/environment-properties.json`, `records/stand-identity.json` copy; `stage_overrides[]` — в B; правка плагина — sum только при F-1 (c), иначе
пробел «правка установленного плагина не обнаружима».

**E. Записи**: `<T>work/requirements-readiness.json → open_questions[]` sum (счёт + тексты), `<T>work/question-answers.jsonl` tail; `strategy/faq.md`,
`qa-factory/obligations.md` copy; `<T>work/context-manifest.json` sum (`unresolved[]`, `source_completeness`); `<T>work/automation-manifest.json`
(180 КБ) sum (`unresolved[]`); `qa-factory/bugs/BUG-*.md` (старое `<T>bugs/`) new — баги D-0052 называет явно; артефакты истории (`understanding.md`,
`test-plan.*`, `work/test-cases/**`, `test-report.md`, `work/ledger.*`, `delivery-manifest.json`) — по F-7, [рек.] sum: требования/кейсы,
`overridden: true`, вердикт доставки, счёт строк «Left with you».

**F. Качество из ретро**: `<T>retro.md` copy; `retro-numbers.json` (C); `rejected`/`failure_class`/`reason_family` — в хвосте журнала (B);
`driver-state.json → retro_feedback` (B). «Пропущенные баги» — `gaps[]`: носителя нет (t-948 F, `escape-ledger.jsonl` спит). Не дошла до S9 →
«ретро нет: история не закончена».

**G. Дашборд**: `state/metrics.json` (3.9 МБ), `state/metrics-history.json` (6.6 МБ) — по F-9; `state/metric-signals.json` copy;
`factory-dashboard.html` skip (пересобирается, несёт `file:///`); `dashboard-*.json`, `.dashboard-writer/`, `*.tmp` skip (служебное, сироты).

**H. Транскрипты** — только у зависших историй (§5): Claude — файл из поля `transcript` cost-файлов сессий истории (`driver-runs.jsonl.session_id`,
`driver-state.json.sessions`, `cost.by_task`) и их `subagents/agent-*.jsonl` через `hooklib.story_subagent_transcripts` (ось 14: свой glob не
пишется); Codex — `rollout-*.jsonl` из того же поля. Упаковка — F-5. Файла нет (почищен хостом, сменён `CLAUDE_CONFIG_DIR`) — `gaps[]` с sid.

**Никогда:** файлы по `guard_secrets.DEFAULT_SECRET_FILE_PATTERNS` + `config.secret_file_patterns`; всё вне `qa-factory/`, кроме H и сводки
`build_inventory`; код продукта и тестов; содержимое `evidence/`; переменные окружения (значения `environment.secret_keys` — только ЦЕЛИ
замазывания); `state/pre-0.7.0-recovery/`, `state/reporter-unread/` (отчёты продукта).

## §3. Новизна, метка, архив

1. **Метка** [рек. F-2] `qa-factory/state/collect/mark.json`: `{schema: 1, project_id, runs: [{archive, sha256, collected_at (UTC ISO), package_version,
   files: {<rel>: {sha256} | {bytes, prefix_sha256}}, events: {<TASK>: {sequence, event_hash}}, metrics_history_last}]}`; читается `runs[-1]`.
2. **Хвост (все append-only: jsonl, events).** Метка хранит `bytes` и sha256 первых `bytes` байт. Совпало → хвост от `bytes` до последнего `\n`;
   нет (переписан, укорочен, чужая машина) → целиком + `prefix_changed`. Хвост без `\n` (запись идёт) не берётся — граница метки = последняя целая
   строка. Events дополнительно: `event_hash` на `sequence` метки иной → весь файл + `chain_reset`.
3. **Снимки и каталоги**: sha256 = метке → строка «без изменений с <archive>», байтов нет. `metrics-history` — `snapshots[]` с `generated_at` > метки.
4. **Первый запуск (метки нет)**: «с установки» ⊆ «всё в папках фабрики» (данных старше установки у неё нет; прошлую установку переустановка
   переносит в `records/`) → берётся всё; паспорт называет дату установки (самый ранний `recorded_at`; иначе `retired/<date>`; иначе «не известна»).
   Старое место читается через `runtime_paths.record()` — тем же резолвером, что все читатели.
5. **Метка пишется** после записи архива и перечитывания (sha256 каждого члена = манифест), атомарно (tmp + replace). Сбой посередине → метка
   прежняя, недописанный архив удалён, следующий запуск берёт то же окно (I3). Сдвиг относительно ОТПРАВКИ — F-3.
6. **Архив** [рек. F-4]: zip (stdlib, deflate) `qa-factory/state/collect/qa-collect-<project_id8>-<yyyymmddThhmmZ>.zip`. Перед записью
   `git check-ignore -q <путь>`: не игнорируется (нет строки `.gitignore` для `state/`) или git нет → архив в `tempfile.gettempdir()/qa-collect/`,
   сводка называет путь и причину (I6; не отказ — P1). Скилл ничего не удаляет в `state/collect/` — прошлые архивы остаются для повтора.
7. **Потолки** (данные `references/collect-sets.json`, FR-13): файл ≤ 16 MiB после редактора — копия; +1 Б → `too_large` (байты, sha256, число
   строк, первые/последние 20 строк через редактор); архив — F-4.
8. **Манифест** `manifest.json` — первый член, приём читает его первым: `{schema: "qa-collect/1", project_id, collected_at, collector:
   {package_version, package_fingerprint}, window: {since_archive|"install", since_at, until_at}, host, os, python, sets: {A..H: {status:
   collected|summarised|empty|gap, note}}, files: [{arc, src_rel, set, mode, bytes, sha256, prefix?, flags[], redactions: {path, user, secret, host,
   email}}], skipped: [{src_rel, set, bytes, reason}], gaps: [{set, what, why}], stories: [{task, plugin_version, touched, closed_at, stalled,
   stall_signals[], transcripts[]}], answers: {problems|suggestions: {state: answered|blank|not_asked, arc}}, parts: [{name, sha256, bytes}],
   redaction_rules_sha256}`.

## §4. Редактор (I2): готовые функции в новой, более ответственной роли

Источники: `state_census.path_variants`/`short83`/`_alternation` (написания raw, forward, json_escaped, slug, 8.3; тест-замер — поднять по F-8);
`guard_secrets.DEFAULT_SECRET_CONTENT_PATTERNS` + `config.secret_content_patterns` (через `_patterns`); узкие `project_inventory._safe_remote`
(`user@`, `token=`), `stand_gaps.names_only` (`NAME=value`). Замены (длинное раньше короткого): корень проекта → `<project>`; плагина →
`<plugin>`; python → `<python>`; home → `<home>`; temp → `<tmp>`; имя пользователя (`getpass.getuser()`, `USERNAME`/`USER`, имя папки home,
`git config user.name/user.email`) → `<user>`; остаточный абсолютный путь (`[A-Za-z]:[\\/]`, `/home/`, `/Users/`, MSYS `/c/`, `file:///`) →
`<abs>/<последний сегмент>`; секрет → `<secret>`; значения `environment.secret_keys` из окружения сборщика длиной ≥ 8 — литерально `<secret:NAME>`.

**Направление ошибки.** `guard_secrets` был блокировщиком ОДНОЙ записи (ошибка — лишний отказ); здесь он фильтр выпуска наружу: допустимо только
«замазал лишнее», пропуск секрета или имени — дефект. Неудобные входы, обязанные остаться на безопасной стороне (каждый — пин §9):
`password: hunter2hunter2xx` без кавычек (дефолтный шаблон НЕ ловит → доп. шаблон в данных); `Authorization: Bearer eyJ…` и голый `Bearer <40>`;
`glpat-…`, `ghp_…`, `xoxb-…`, `AKIA[0-9A-Z]{16}`, `https://u:p@host/…`, `?token=…`; имя в `C:\\Users\\X` (JSON), `C:/Users/X`, `c:\users\x`,
`C--Users-X-…` (слаг Claude), `/c/Users/X`, `file:///C:/Users/X`, `C:\Users\DEV1~1` (8.3); имя короче 3 знаков не заменяется внутри слова
(граница `(?<![A-Za-z0-9])…(?![A-Za-z0-9])`, AT 3 / BEYOND 2); JSON после замены остаётся JSON (`json.loads` до и после; не парсится — `skipped`);
собственные шаблоны `config.secret_content_patterns` замазываются как текст — допустимо (лишнее).

## §5. Зависание — правило кодом (`scripts/collect_stall.py`, чистая функция)

`stall(project, task_dir, mark, now) -> {stalled, current, signals: [{id, where, at}]}`; признаки t-948 I, только новые с метки:
S1 `driver-state.interrupted` не пуст; S2 `in_flight` с мёртвым pid (`dispatch_liveness.in_flight_entry` + `process_alive`/`pid_reused`); S3 `launched`
без итога того же `dispatch` и без живого `in_flight`; S4 итог `is_error`/`exit_code≠0`/`infra`; S5 `conductor.jsonl` `action == "stop"`; S6 диспатч
в `returned_unaccepted|abandoned|never_started|stale|blocked|incomplete` или `running` при `dispatch_liveness.state ≠ alive`; S7 событие
`state_repair`/`release` в хвосте events. `current` = не закрыта (`hooklib.story_closed` пусто) И нет живого диспатча И `archive_task.last_activity`
старше `stall_quiet_hours` (данные, 24). `stalled` = S1–S7 ИЛИ `current` (определение — F-5). Записи, а не зависание (в манифест, транскриптов не
тянут): нерешённый halt, гейт без ответа, `gate_block`, `rejected`, `escalated`.
**Направление ошибки** (`archive_task`/`dispatch_liveness` были советом/диагнозом, стали воротами транскриптов): при F-5 (i) лишний транскрипт —
безопасная сторона, поэтому нечитаемый `driver-state`/`controller.json` → сигнал `unreadable` → `stalled`. Обязаны остаться НЕ зависшими: идущая
история (живой диспатч, свежая активность, S4 `running`) — пункт `open_items` «never reached S9 done» её не делает зависшей (поправка к t-948 I);
закрытая чистая; архивированная судится как любая (архив — «не показывать», не «закончена»).

## §6. Скилл и два вопроса (`skills/qa-collect/SKILL.md`, ≤ 19000 Б; FR-56: `allowed-tools: Bash, Write`)

Шаги: (1) `activity_capture.py --action start --type collect` (TYPES += `collect`, иначе расход скилла `unclassified` — P18); (2) ОДНО сообщение — два
вопроса; (3) ответы дословно — `qa-factory/state/words/collect-problems.txt`, `collect-suggestions.txt` (Write; «слова — в файле», conductor.md:47);
(4) один Bash: `"${CLAUDE_PLUGIN_ROOT}/hooks/run-py.cmd" collect_pack.py --root . --problems-file <f> --suggestions-file <f> [--extra <set>=<path>]`
(ответы читает `person_words.read`); (5) сводка скрипта дословно (≤ 12 строк: путь, размер, пробелы, транскрипты), `--action end --after-response`.
`--extra` — единственная работа агента сверх вопросов, только после «<набор>: not found at the standard place» (FR-13: раскладку судит роль).

Текст (FR-6, `human-questions.md`: без путей и скриптов в теле, «How to answer» внизу):
> Before I pack the factory's records for its developers, two questions — answer either, both or neither, in your own words:
> 1. What problems did you have with the QA factory since it was installed (or since you last sent its records)?
> 2. What would you like the factory to do differently or better?
> Answering costs you only this message; the factory then runs one packing command, no agent works; your stories are unchanged.
> **How to answer:** reply with your two answers, or "nothing to add".

**Конфликт требований** `human-questions.md` п. 3 («один вопрос»), п. 4 («код задаёт только закрытые») ↔ D-0052 (1) («два свободных»): слово
владельца сильнее; оба — одним сообщением; задаёт агент, читаем мы — п. 4 соблюдён буквально; п. 6 (цена) — одной строкой на оба. Инв.: ни один
ответ не становится токеном для кода. «nothing to add»/пусто → `blank`; без человека (headless) → `not_asked`; архив пишется в любом случае.

**Отказы (FR-1, FR-57; скрипт, выход 1):** нет `qa-factory/` → «COLLECT: no qa-factory folder under <root>; run the skill from the project folder that
holds qa-factory/config.json, or pass --root <that folder>»; данные `collect-sets.json`/`collect-redaction.json` не читаются → «COLLECT: the packing
rules <file> cannot be read (<why>); reinstall the plugin — packing without its redaction rules would send unredacted data» (детектора нет — не
проход); `--extra` вне корня проекта или на файл по шаблону секрета — отказ той же формы. Нет `config.json` — НЕ отказ: «not onboarded».

## §7. Приём на нашей стороне (`tools/collect_intake.py`)

`python tools/collect_intake.py <archive.zip>... [--inbox DIR] [--apply] [--place <key>=<slug>]` — по умолчанию план, ничего не пишет.
1. **Проверка** (архив — недоверенные данные): первый член `manifest.json` с известной `schema`, иначе «unknown archive schema <s>; this intake reads
   qa-collect/1 — update tools/ or ask the sender for the factory version»; член с `..`, абсолютным путём, `:` или дублем → отказ всего архива;
   sha256 членов = манифест; только `json`/текст, ничего не исполняется.
2. **Распаковка** в inbox ВНЕ git (F-11): `<inbox>/<project_id>/<archive_stem>/`; `<inbox>/index.json` — принятые архивы и решения `--place`.
3. **Повтор.** Тот же sha256 архива → «already taken in <date>», выход 0. Новый архив того же проекта — ключи дедупа: находка (`project_id`, `FB-n`,
   `idempotency:`; новый `status` — «изменилась», не новая); строка журнала — sha; событие — (`task`, `sequence`, `event_hash`); сессия — `session_id`
   (новее `ended` побеждает); ответ — sha текста; RA/EP — id + sha. Перекрытие окон (`prefix_changed`, метка не сдвинулась) гасится здесь же.
4. **Элементы:** `FB`, `retro` («What went wrong»), `stall` (история + сигналы), `answer-problems`, `answer-suggestions`, `adaptation` (RA, EP,
   change-request по F-1), `numbers` (C + G).
5. **Раскладка** [рек. F-10]: (а) файлы/скрипты, названные в элементе → `forge_metrics.attribute_text` (один читатель `features.json`) → фича;
   (б) фича → кучки по `фичи:` карточек; одна → она; несколько → совпадение пути с «зоной» карточки, ровно одна → она; (в) иначе, или атрибуция
   только по словам → `unplaced`. `answer-problems` — всегда `unplaced` (I7); `answer-suggestions`, `adaptation` → новая кучка (F-12); `numbers` →
   `cost-dashboard` (без $, F-11). Карта на 19.10: фичи↔кучки многие ко многим (F05 → 4 кучки, F07 → 3), у F10 кучки нет, у `live-runs` фич нет.
6. **Отказ раскладки:** элемент никуда → строка `unplaced` с кандидатами и причиной, выход 3 («нужен Lead»); ответ Lead — `--place <key>=<slug>`,
   запоминается в `index.json` (тот же ключ следующего архива ляжет туда же). Инв.: на входе = разложено + `unplaced` + дублей — равенство
   печатается; ни один не теряется и не уходит в `forge` молча.
7. **`--apply`** [рек. F-13 (b)]: одна находка на (архив × кучка) `plans/piles/<slug>/findings/<yyyymmdd>-collect-<project_id8>.md` в форме
   `piles.parse_finding` (`# …`, строка `id: — | кучка: \`<slug>\` | от: collect <archive> | приоритет: — | кандидат наверх: —`), внутри — элементы с
   ключами и указателями в inbox; печатает строки для Lead тем же ходом (D-0044): «Содержание» карточки (`test_pile_cards_contents`) и строку
   невзятой пачки ((е)). Файл с тем же именем есть → не перезаписывается, выход 2.

## §8. Края (поведение + инвариант)

1. **Нет `qa-factory/`** → отказ §6. Инв.: архива «ни о чём» нет. **Не онбордирован** → паспорт «not onboarded», `gaps` по B–H. Инв.: I1.
2. **Нет прогонов** → B/E/F/H `empty`, A/C/D/G как есть. Инв.: пустое ≠ пробел ≠ ошибка (три статуса).
3. **Прогон другой версии** (иной `pipeline.plugin_version`, старая раскладка) → тот же резолвер, версия в `stories[]`, нет поля — `null`, незнакомый
   файл `<T>` — `skipped: unknown file`. Инв.: незнакомое не роняет (P2).
4. **Без git** → `git: absent`, архив в temp (§3 п. 6); Инв.: I6 по проверке. **Windows-пути** — все написания §4; Инв.: I2.
6. **`evidence/` 100 МБ** → индекс; sha256 только файлов ≤ 16 MiB, крупнее `sha256: null` + `not_hashed`. Инв.: evidence архив не растит.
7. **Второй сбор подряд** без новых данных → паспорт + «без изменений», метка сдвигается. Инв.: повтор дёшев и безвреден.
8. **Метка чужой машины / потеряна** (переустановка выбросила `state/`) → как первый запуск. Инв.: I3; дубли — §7 п. 3.
9. **Запись во время сбора** → полстроки не берётся (§3 п. 2); проекции пишутся `atomic_json` — читаются целыми; битый JSON → `skipped: unreadable`.
10. **Потолок файла** AT 16 MiB — копия, BEYOND +1 Б — `too_large`; **архива** AT/BEYOND — F-4. Инв.: I4.
11. **Транскрипт не найден / не UTF-8 строка** → `gaps[]` с sid / строка выброшена со счётом. Инв.: H не ищет по диску.
12. **История идёт сейчас** → не зависла (§5). Инв.: идущая работа не выдаётся за зависание.
13. **Конфликты:** «всё» ↔ «дёшево» — sum/skip; «всё» ↔ «потолок» — F-4; «деньги» ↔ «не в git» — §3 п. 6, F-11; «два вопроса» ↔ FR-6 — §6. Инв.: без молчаливого среза.
14. **Нестандартное место** (`artifact_root`, `journal_path`) → резолверы; не нашёл — «not found at the standard place», агент даёт `--extra`. Инв.: код не ищет по диску.
15. **Временной (оба мира):** до узлов нет `state/collect/`, строк `install-paths.json`, TYPES `collect`, фичи F22; после — папку создаёт первый запуск,
    строки — CL1-2/CL1-4; старая установка может потерять `state/collect/` при переустановке → край 8. Инв.: потеря метки — только лишний сбор.

## §9. Пачка `collect` (предложение; имя — F-12)

| Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус |
|---|---|---|---|---|---|---|
| CL1-1 | П2 | Редактор §4: написания путей из теста в модуль пакета (F-8), замены, шаблоны в данных; `state_census` импортирует модуль. Тесты: `test_collect_redact.py` (все неудобные входы §4, имя AT 3 / BEYOND 2); самотест `state_census`. Критик: да (фильтр выпуска наружу) | designer → critic на план → builder → critic | `scripts/machine_facts.py` (новый), `references/collect-redaction.json` (новый), `scripts/tests/state_census.py (path_variants, short83, _alternation)`, `scripts/tests/test_collect_redact.py` (новый) | — | ожидает |
| CL1-2 | П2 | Сборщик: наборы §2 из данных, метка и хвосты §3, манифест, zip, потолки, `check-ignore`, отказы §6; строки `install-paths.json` для `state/collect/**`; тест «каждый путь наборов — строка `install-paths` или путь `<T>` реестра артефактов». Тесты: `test_collect_pack.py` (края 1–10, 13–15) | builder → critic | `scripts/collect_pack.py` (новый), `references/collect-sets.json` (новый), `references/install-paths.json`, `scripts/tests/test_collect_pack.py` (новый) | CL1-1 | ожидает |
| CL1-3 | П2 | Зависание §5 + выбор транскриптов H. Тесты: `test_collect_stall.py` (S1–S7, «идёт сейчас», `unreadable`) | builder → critic | `scripts/collect_stall.py` (новый), `scripts/tests/test_collect_stall.py` (новый) | — | ожидает |
| CL1-4 | П2 | Скилл §6, TYPES `collect`, фрагмент changelog; фича F22 в `plans/features.json` — Lead (forge) | builder | `skills/qa-collect/SKILL.md` (новый), `scripts/activity_capture.py (TYPES)`, `changelog.d/collect-1-cl1-04-skill.md` (новый) | CL1-2, CL1-3 | ожидает |
| CL1-5 | П1 | Правило D-0052 (3) по F-1 + маркер `change-request:` | designer → critic на план → builder → critic | по F-1 (a): `references/conductor.md`, `references/common-rules.md`, `scripts/tests/test_project_decisions_change_request.py` (новый); `skills/qa-story/SKILL.md` — интегратор (builder-rules п. 1) | — | ожидает |
| CL1-6 | П2 | Приём §7; ключ inbox по F-11 | builder → critic | `tools/collect_intake.py` (новый), `tools/test_collect_intake.py` (новый), `tools/dev_config.py (+collect_inbox)`, `tools/dev.config.example.yaml` | CL1-2 (схема — из спеки, фикстура архива своя) | ожидает |
| CL1-7 | П2 | Живое доказательство (FR-33): сбор на КОПИЯХ cmp2r и cmp3gb → приём в копию дерева кучек; это и детектор D-0052 | Lead + builder | отчёт `docs/tasks/handoffs/` | все | ожидает |

**owns** (`P` = `D:/ws1/yml-text-factory\ai-packages\qa-factory`, `R` = `D:/ws1/yml-text-factory`; в диспатче — полностью):
CL1-1 `P\scripts\machine_facts.py`, `P\references\collect-redaction.json`, `P\scripts\tests\state_census.py` (три функции → импорт), `P\scripts\tests\test_collect_redact.py`;
CL1-2 `P\scripts\collect_pack.py`, `P\references\collect-sets.json`, `P\references\install-paths.json`, `P\scripts\tests\test_collect_pack.py`;
CL1-3 `P\scripts\collect_stall.py`, `P\scripts\tests\test_collect_stall.py`; CL1-4 `P\skills\qa-collect\SKILL.md`, `P\scripts\activity_capture.py` (только
`TYPES`), `P\changelog.d\collect-1-cl1-04-skill.md`; CL1-5 по F-1; CL1-6 `R\tools\collect_intake.py`, `R\tools\test_collect_intake.py`, `R\tools\dev_config.py`,
`R\tools\dev.config.example.yaml`.
non-goals: отправка по сети (F-14), чтение ответов кодом, пересчёт дашборда у нас (по F-9), правка `story_run.py`/`controller.py`/`hooklib.py`, новая
анкета, пробы/доктор из скилла, «пропущенные баги» (носителя нет — находка `report-delivery`). handoff: `docs/tasks/handoffs/t-NNN-cl1-N.md` ≤ 500 слов.

**DoD узлов** (из `ai-packages/qa-factory`; свой файл — на Windows и в docker `python:3.12` на копии дерева, форма t-908): CL1-1
`python -B scripts/tests/test_collect_redact.py`; CL1-2 `python -B scripts/tests/test_collect_pack.py`; CL1-3 `python -B scripts/tests/test_collect_stall.py`;
CL1-5 `python -B scripts/tests/test_project_decisions_change_request.py`; docker:
`MSYS_NO_PATHCONV=1 docker run --rm -v <worktree>:/src:ro python:3.12 sh -c "cp -r /src /repo && cd /repo/ai-packages/qa-factory && python -B scripts/tests/<file>.py"`;
соседи один раз: `python -B scripts/tests/test_install_paths.py` (CL1-2), `python -B scripts/selftest.py --limits --lang`,
`python -B scripts/tests/test_audit_rules.py`; из корня `python tools/dup_ratchet.py --check`, `python tools/lint_ratchet.py --check`. CL1-6:
`python -m pytest tools/test_collect_intake.py -q` и `python tools/piles.py check --all` на копии дерева после `--apply` фикстуры и строк Lead.
Первые ходы: CL1-4 — байты SKILL и API `human_text` для пина текста вопросов; CL1-5 — байты `conductor.md`/`common-rules.md` и инжекта роли против капов.
**Мутации (одна — один файл):** замена имени без 8.3 → `test_collect_redact` «DEV1~1»; шаблон `Bearer` убран из данных → он же; `prefix_sha256` не
сверяется → `test_collect_pack` «переписанный журнал»; полстроки берётся → он же «запись идёт»; `check-ignore` пропущен → он же «state не
игнорируется»; `running` без `dispatch_liveness` → `test_collect_stall` «идёт сейчас»; `..` в члене не отказан → `test_collect_intake` «zip-slip»;
`unplaced` не считается → он же «равенство элементов». Ожидания — из D-0052 и t-948, не из выхода кода (FR-58).

## §10. Проход FR

- **A** — FR-1/FR-57 (отказы §6: что, чего ждали, дверь `--root`/переустановка), FR-2, FR-4 (пробел назван), FR-50 (недостижимый транскрипт — пробел без вопроса, D-0043).
- **B** — FR-6 (§6, конфликт назван), FR-7 (прежние ответы не показываются), FR-8 (слова дословно). **E** — FR-37 (сводка — реальный путь), FR-53 (пишет только `state/collect/`, words).
- **C** — FR-12 (ответы не классифицируются; у нас — по путям, слова → Lead), FR-13 (наборы, шаблоны, потолки — данные), FR-14 (манифест со `schema`), FR-15, FR-49, FR-56.
- **D** — FR-16 (дедуп по id производящих инструментов), FR-18 (индекс evidence — не покрытие), FR-58, FR-59 (нечитаемое → `unreadable`, не «чисто»).
- **F** — FR-24/25 (цена — из файлов сессий; расхождение источников приём печатает), FR-41 (неизвестное — `null`/пробел), FR-51 (цена скилла — CL1-7).
- **G** — FR-29, FR-30, FR-32, FR-33 (CL1-7), FR-44 (SKILL грузит человек → `skills/`; данные грузит код → `references/*.json`), FR-45, FR-47, FR-52, FR-54.

## §11. Оси SIBLING_MAP (18)

1, 2 — n/a. 3 — покрыто: скилл уходит релизом; `package_fingerprint` (хэширует `skills/`) меняется; F-1 (c) — сверка с релизным. 4 — покрыто: D-0052 →
правило CL1-5; «пропущенные баги» — строка долга. 5 — n/a (стадий не трогает). 6 — покрыто: приём — измеритель пакета; `collect-sets.json` — вторая
копия раскладки рядом с `install-paths.json` → тест CL1-2. 7 — n/a. 8 — покрыто: `<T>` только через `hooklib.artifact_root`/`runtime_paths`.
9, 10, 11 — n/a (git — только `check-ignore` и `build_inventory`). 12 — покрыто: §7 п. 7 (находка + «Содержание» + строка пачки). 13 — n/a. 14 — покрыто:
пакет — `hooklib.story_subagent_transcripts`, у нас — `tools/transcripts.py`, третьего читателя нет. 15 — печать через `console_io`. 16 — `hooklib.read_json`.
17 — n/a. 18 — храповики dup/lint не растут (DoD).

## §F. Развилки (решает Lead; цена каждого варианта)

- **F-1 Дом правила D-0052 (3) «просьба изменить фабрику → находка/решение».** Человек говорит с основной сессией; фабричный текст туда попадает только
  через скилл; SessionStart текста не вносит (`additionalContext` в `scripts/*.py` пишут только `inject_context.py`, `host_adapter.py` — тот же Grep нашёл
  их, контроль формы). (a) [рек.] текст: строка таблицы `conductor.md` (дирижёр драйвера), строка `common-rules.md` (роли), строка `qa-story/SKILL.md`
  (оркестратор; интегратор): «a person asking to change the factory → `project_decisions.py add-finding --scope upstream-candidate --idempotency-key
  change-request:<…>` with their words, then go on; never a plugin edit»; маркер — префикс ключа, схема FB не меняется. Цена: байты в капах
  (`references/*.md` ≤ 12000, инжект роли ≤ 42000), дисциплина; детектор — сам сбор (счёт change-request) и (c). (b) (a) + код-гейт по ДЕЙСТВИЮ (FR-12):
  хук на Write/Edit под корнем плагина или `config.json` мимо `config_contract` из основной сессии пишет находку сам, не блокирует (P1). Цена: ветка в
  горячем `guard_pre_tool.py` (очередь за CX1-5/CX1-6), ложные находки при обновлении плагина. (c) детектор без текста: релизный отпечаток в поставке
  (`references/release-fingerprint.json`, пишет релизный шаг), сбор сравнивает с бегущим; цена: шаг релиза, файл вне своего отпечатка. Рек.: (a) + (c).
- **F-2 Метка и идентичность.** (a) [рек.] `state/collect/mark.json` (B/C/H машинные); `project_id` = 16 hex sha256 нормализованного remote первого
  `code_repos` (`_safe_remote`), без remote — uuid в метке; цена: две машины без remote — два id (склейка у нас `--place`). (b) `records/collect-mark.json`
  (коммитится, один id на команду); цена: шум в git проекта на каждый сбор; хэши `state/` чужой машины всё равно не совпадут (край 8).
- **F-3 Когда сдвигается метка.** (a) [рек.] при записи архива; неотправленный остаётся в `state/collect/`, `--since install` пересобирает всё; цена:
  забытая отправка — окно на диске, не в следующем архиве. (b) после `--confirm-sent` по слову человека; цена: третий шаг человека.
- **F-4 Формат и потолок.** (a) [рек.] zip, части ≤ 25 MB сжатыми (`-part2.zip`…, манифест в первой называет все); цена: несколько файлов в худшем
  случае. (b) один zip без потолка; цена: почта/чаты отказывают > 25 MB. (c) tar.gz; цена: на Windows человек не откроет и не увидит, что отправляет.
- **F-5 Транскрипты.** Определение: (a) только «застряла сейчас»; (b) [рек.] любой эпизод S1–S7 с метки (cmp2r: 11 `release`, 6 `returned_unaccepted`
  у закончившейся истории); цена: до 5.6 МБ на историю. Упаковка: (i) [рек.] отдельная часть `…-transcripts.zip`, сводка: «это переписка агентов по
  зависшим историям; удалите файл, если не хотите её отправлять» — без третьего вопроса; (ii) внутри архива — код продукта из вывода инструментов
  уходит без шанса удержать; (iii) закрытый третий вопрос — против D-0052 (1).
- **F-6 Хосты, remote, почта, ключи тикетов.** (a) [рек.] хост стенда/трекера/remote → `host-<8hex>` (схема, порт, путь остаются), e-mail → `<email>`,
  ключ тикета остаётся (группировка, дедуп); (b) хосты как есть — внутренние имена компании уходят наружу; (c) URL вон — паспорт не знает провайдера.
- **F-7 Артефакты истории.** (a) [рек.] счёт (§2 E) — D-0052 (2) их не называет; цена: качество кейсов у нас не видно. (b) целиком через редактор;
  цена: текст продукта наружу, +150–250 КБ на историю.
- **F-8 Источник написаний путей** (t-948 вопрос 5). (a) [рек.] поднять `path_variants`/`short83`/`_alternation` в `scripts/machine_facts.py`, тест-замер
  импортирует — один генератор для детектора и редактора; цена: правка тест-замера F06. (b) своя копия — два правила, расхождение после первой правки
  (вопрос 6 критик-брифа). (c) импорт из `scripts/tests/` в поставку — не рек.
- **F-9 Дашборд-данные.** (a) [рек.] `snapshots[]` после метки + `metrics.json` целиком (3.9 МБ); (b) только входы, пересчёт у нас — наша версия
  `metrics_projection` ≠ их, числа не их; (c) оба — +3.9 МБ.
- **F-10 Раскладка.** (a) [рек.] §7 п. 5; (b) только «зона» карточки по путям — элемент без путей (ретро, сигналы) всегда к Lead; (c) всё к Lead —
  ручная раскладка каждого архива (≈15–30 элементов).
- **F-11 Деньги и inbox у нас.** P18: деньги в файлы отчёта не пишутся; бриф: «числа → `cost-dashboard`». (a) [рек.] inbox вне git (ключ `collect_inbox`
  в `tools/dev.config.yaml`, один читатель `tools/dev_config.py`); находка `cost-dashboard` несёт токены, сессии, неполные, долю дирижёра и ДА/НЕТ
  равенства двух источников (P18), без $ — доллары пересчитываются по токенам; (b) `experiments/collect/` в `.gitignore` — риск `git add -f`; (c) $ в
  находке — против P18 («цены меняются»).
- **F-12 Имена кучек.** Сборка — `collect` (бриф). Новая кучка предложений и чужих адаптаций (D-0052 (7)): (a) [рек.] `proposals`; (b) `outside-ideas`; (c) `suggestions`. Цена одинакова.
- **F-13 Что пишет `--apply`.** (a) план (`<inbox>/…/intake-plan.md`), находки пишет Lead — ручной перенос. (b) [рек.] находка на (архив × кучка) +
  напечатанные строки «Содержание»/пачки; цена: коммит красный в (е), пока Lead не поставит строки тем же ходом. (c) все три носителя кодом — второй
  код-писатель файлов пачек рядом с `piles.py` (ось 12).
- **F-14 Как архив едет к нам.** (a) [рек.] человек отправляет файл сам (сводка: путь и «send it to the QA factory developers»); (b) загрузка в issue
  GitLab токеном — токен и VPN у человека, запись наружу из скилла; отдельное слово владельца.

**Малые выборы, закрытые дизайнером:** сборщик не запускает проб и доктора; ответы — words-файлами через `person_words.read` (многострочное в cmd.exe);
режимы copy/tail/new/sum/skip; одно правило хвоста по префиксу байт для всех append-only файлов; файловый потолок 16 MiB; `stall_quiet_hours` 24 (данные);
evidence — индекс без содержимого; `.html` дашборда — skip; выходы 0/1/2 (+3 у приёма); имя находки приёма `yyyymmdd-collect-<id8>.md`; активность `collect`.

## Нужно сверх манифеста / замечено

- Прочитано сверх `given`: `tools/test_pile_cards_contents.py` (файл находки — ровно раз в «Содержание» карточки: находка = три носителя),
  `tools/forge_metrics.py` (сигнатуры `attribute_text`, `load_registry`), `tools/dev_config.py`, `activity_capture.py:14` (TYPES без `collect`),
  `person_words.py`, `hooks/hooks.json`, сигнатуры `hooklib.py`, `docs/SIBLING_MAP.md` оси 6/14, FR-13/44/51/56, `builder-rules.md` пп. 1, 5.
- Бриф против закона: «числа → `cost-dashboard`» сталкивается с P18 (F-11); «находки так, как ждут (д)/(е)» — (е) требует СТРОКУ пачки для находки от
  13.10, `test_pile_cards_contents` — строку «Содержание»: один файл находки не проходит (F-13).
- t-948 I: «остановлен = `open_items` не пусты …» делает зависшей КАЖДУЮ идущую историю («never reached S9 done») — поправлено в §5.
- Не проверено мной: что `install_paths` делает с файлом `state/`, не названным строкой (край 15 предполагает худшее); API `human_text.py`;
  байты капов (первые ходы CL1-4/CL1-5); точные статусы диспатча S6 — по t-948 I, `controller.py` я не читал.

## L. Решения Lead по развилкам (19.10.2026, Fable; слово владельца 18:4x — D-0053)

Все четырнадцать развилок F-1…F-14 — по РЕКОМЕНДОВАННОМУ варианту дизайнера (D-0053 перечисляет каждый). Имена: кучка сборки `collect`, кучка предложений и чужих адаптаций `proposals`. Правило D-0052 (3) (F-1 (a)+(c)) — механизм пакета: узел CL1-5 идёт через критика на план отдельно; фингерпринт релиза — детектор (c) правила 10. Деньги (F-11): inbox вне git, в находках долларов нет (P18). Непроверенное дизайнером (реинсталл и незарегистрированный файл под `state/`, API `human_text`, байты капов, статусы диспатча S6) — первые ходы узлов CL1-2/CL1-4/CL1-5, не стоп. Дальше: критик на план (t-972) → размещение кучки `collect` из таблицы §(4) (README, batch-1, находки) → билдеры по узлам.

## L-2. Решения Lead по ревью t-972 (19.10.2026 19:2x, Fable; fit_with_fixes, 0 блокеров, 7 мажоров, 20 миноров)

Все семь мажоров и двадцать миноров приняты в форме, которую предложил критик (`docs/tasks/specs/reviews/t-972-t-962-collect-plan.md` §2); ни одна правка не открывает развилки D-0053. Что меняется в §5, §4, §7, §9 и в диспатчах узлов:

- **F-1 → §5 (CL1-3).** S6 = только `abandoned`/`never_started` и `returned_unaccepted`, чей `returned_at` старше `stall_quiet_hours`; `stale`, `blocked`/`incomplete`/`paused`, `running`+`unknown` — не сигналы (последний остаётся делом `current`). Множества статусов — импорт `SETTLED`/`STOPPED`/`DISCOUNTED` из `controller`, не своя таблица; первый ход CL1-3 проверяет, что `import controller` без побочных действий на импорте; если есть — множества копируются, и пин `test_collect_stall` сверяет копию с `controller` (близнец связан тестом). `current` исключает историю, чей последний открытый пункт — ожидание человека (`archive_task.open_items` «gate … never answered», `driver-question.md`) → запись «ждёт человека», без транскриптов. `last_activity` None → последний `created_at` из `events.jsonl`; нет и его → `started_at` диспатча; ничего → `unreadable` (безопасная сторона §5). Каждый сигнал окнится своим временем (`at`, `started_at`, `returned_at`, `created_at`, `ts`) > метки; снимок без времени (статус в `controller.json`) сигналом не бывает. Пины и мутации на (а)–(е) ревью в `test_collect_stall.py`. Сигналы §5 переименовать K1…K7 (m1): K4 «ошибка/infra» — только когда ПОСЛЕДНИЙ итог того же `dispatch` с ошибкой.
- **F-2 → §2 H (CL1-3).** Результат `hooklib.story_subagent_transcripts` фильтруется по стеблям транскриптов сессий зависшей истории (`p.parent.parent.name == Path(transcript).stem`); hooklib не правится (non-goal). Сводка одной строкой рядом с «удалите файл»: основной транскрипт интерактивной сессии несёт и другую работу человека.
- **F-3 → §4 (CL1-1).** Редактор JSON-осознанный: parse → обход ключей и строковых значений → замены на каждой строке → dump (JSON остаётся JSON по построению); JSONL — построчно, деление только по `\n` (ось 14: `\r`/U+2028 внутри строки — данные); детекторный шаблон в роли редактора: попадание → замазать всё строковое значение / всю текстовую строку / PEM до `-----END`; `names_only` — только поштучно на строке-значении или не-склеивающий вариант в `machine_facts`. Пины: `aws_secret_access_key = wJalr…`, PEM с телом, `{"x":"FOO=bar","y":1}`, `\u`-имя, `Authorization: Basic`, `Cookie:`/`Set-Cookie`, пароль короче 16 и без кавычек, `%20`/`%5C` в `file://`, UNC и `file://server/share`, `/mnt/c/Users/X`, `AzureAD+Имя`, `DOMAIN\user`, имя машины, scp-remote, голые хосты и IP (таблица «Утечки редактора» ревью — весь список). Направление ошибки прежнее: битый JSON → файл в `skipped` с причиной, не падение; но набор B теперь не теряется, потому что валидный JSON редактор не ломает.
- **F-4 → новый узел CL1-8 «Отпечаток релиза» (механизм, правило 10).** Owns: `P\references\release-fingerprint.json` (новый), `P\scripts\release_fingerprint.py` (новый: ОДИН рецепт отпечатка, который читают и `install_smoke.package_fingerprint`, и `runtime_paths` — t-948 A, два носителя сходятся), `P\scripts\tests\test_release_fingerprint.py` (новый), `R\docs\RUNBOOK.md` (строка шага релиза: файл исключён из собственного отпечатка). Сборщик (CL1-2) сравнивает отпечаток установки с файлом и пишет в манифест `package_modified: yes|no|unknown`; детектор (c) D-0052 (3) — это сравнение. Путь: designer → critic на план → builder → critic; после CL1-2 (манифест). Осевой блок и `tier:` — на коммите слияния.
- **F-5 → CL1-4 и остаток.** В `activity_capture` одно множество `FACTORY_TYPES` (`TYPES` остаётся псевдонимом), `dashboard_cost_groups.py:84` читает его — обе в owns CL1-4 (первый ход: `dashboard_cost_groups.py` не в зоне взятой пачки по `plans/PILES.md`; в зоне → строка `очередь:`). `hooklib.py:1227` и `cost_capture.py:1482/1772` — горячие, чужие зоны: находка в `plans/piles/cost-dashboard/findings/` со строкой в её невзятой пачке 1 (D-0044) и явный пробел в «Остатках» пачки `collect`: до неё расход скилла на дашборде — `Unclassified`, `has_factory_activity` его не видит.
- **F-6 → §3 (CL1-2).** `project_id` = sha256(`remote` + путь папки проекта от git-верха, `/`, без хвостового), первые 12; `install_id` — uuid4, рождается с меткой `state/collect/mark.json` и повторяется в манифесте; дедуп приёма (§7 п. 3) — по паре (`project_id`, `install_id`); имя архива и находки несут `install_id[:8]`. CL1-7 ждёт ДВА разных id с cmp2r и cmp3gb — это ключ его DoD.
- **F-7 → §7 (CL1-6) и размещение.** Кучка `proposals` размещается тем же ходом, что `collect` (карточка + `batch-1-predlozheniya.md` «ожидает», раздел «Дороги»); `--apply` при отсутствии невзятой пачки у кучки печатает «открыть пачку N+1» с готовой строкой таблицы «Пачки» карточки и именем файла (D-0044), выход 3; имя находки `<yyyymmdd>-<hhmm>-collect-<id8>.md`, совпадение → суффикс `-2`, `-3`; выход 2 из-за имени — никогда (FR-57).
- **Миноры m1–m20** — как у критика: m2 хэш хоста одной функцией в `machine_facts` поверх `http_client.safe_url` (сведение `manual_capture._safe_url` — очередь); m3 переносится построитель таблицы `state_census.Detector`, пороги host 6 / имя 3; m4 `collect-sets.json` остаётся с тестом-сведением (очередь: поле `collect` на строках `install-paths`); m5 blank = флаг не передан, `not_asked` = явный флаг; m6 `work/evidence/**`, `work/evidence-ext/` — в индексе и в «никогда»; m7 `artifact_root` вне проекта → `--extra` требуется, битый `config.json` → пробел; m8 манифест после частей 2..n, свой sha исключён; m9 потолок распаковки потоково по `bytes` манифеста; m10 «since the factory last packed them» + дверь `--since install`; m11 git через `project_inventory._git` (ось 10 покрыта, не n/a); m12 строка `install-paths` для `state/collect/**` класса `carried`, `machine_local`; m13 факт переписи исправлен (evidence 13797 = 163 ф., 0.58 МБ); m14 номера строк — по HEAD на диспатче; m15 три Bash, цель SKILL ≤ 4 КБ; m16 → бриф критика CL1-5; m17 проводка H → упаковщик в owns CL1-4 (CL1-2 от CL1-3 не зависит); m18 DoD: CL1-1 `python -B scripts/tests/test_state_portability.py` и `test_resolver.py`, CL1-4 `python -B scripts/selftest.py --limits --lang` + пин текста вопросов через `human_text`, CL1-7 — ключи: архив собран, равенство приёма напечатано, скан распакованного архива на формы имени / 8.3 / имя машины / хосты стенда пуст при положительном контроле той же формы на исходном дереве (детектор I2), два `install_id`; m19 механизмы с осевым блоком: CL1-4, CL1-5, CL1-6, CL1-8; m20 один читатель зоны `piles.parse_zone` в `tools/piles.py` (owns CL1-6 по D-0048, `piles.py (parse_zone)`), доля `unplaced` — метрика CL1-7.
- **Мутации (одна — один файл), сверх §9:** `returned_unaccepted` без окна по `returned_at` → `test_collect_stall` «роль только что вернулась»; `stale` снова сигнал → он же; `unknown` считается зависанием → он же; ожидание человека → он же «ждёт человека»; фильтр стеблей снят → он же «чужой субагент»; значение `aws_secret_access_key` остаётся → `test_collect_redact`; `names_only` склеил JSON → он же «JSON остался JSON»; `install_id` не в ключе дедупа → `test_collect_intake` «две установки»; имя без `hhmm` → он же «второй архив за день».

**Очередь (строки «Остатков» пачки `collect` при размещении):** сведение `http_client.safe_url`/`manual_capture._safe_url` к `machine_facts` (после CL1-1); одна таблица шаблонов секретов в данных для гарда и редактора — находка `onboarding-hooks` (направление ошибки гарда решает Lead); `FACTORY_TYPES` в hooklib/cost_capture — находка `cost-dashboard`; «пропущенные баги» — находка `report-delivery`; поле `collect` на строках `install-paths` (m4).

**Порядок узлов (ревью §3):** CL1-1 → CL1-2 → CL1-8; CL1-3 ∥ CL1-1; CL1-4 после CL1-2, CL1-3; CL1-5 ∥ (свой критик на план); CL1-6 после схемы CL1-2; CL1-7 последним. Дальше: размещение кучек `collect` и `proposals` билдером в основном дереве (только `plans/`), затем дизайнеры CL1-1 и CL1-5 (читатели, вне капа), билдер CL1-3 — первым писателем узлов.

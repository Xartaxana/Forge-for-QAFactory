# Forge — пачка 1: фундамент командной работы

кучка: `forge` | статус: закрыта | взял: владелец (Lead) | ветка: `main` (интегратор; узлы — в worktree билдеров) | MR: `ff353757` https://git.example.com/dev1/yml-text-factory/-/issues/4 | стенд: не нужен | issue: https://git.example.com/dev1/yml-text-factory/-/issues/4

Правило готовности: пачка закрыта, когда каждый узел «принято», `plans/PILES.md` собран кодом и
показывает 11 кучек с первыми пачками «ожидает», BACKLOG.md заморожен, журнал на разработчика живёт,
boot-бюджет ≤ 100 КБ, разработчик с чистого клона берёт пачку по README за 10 минут.

Решения владельца: B-230 (30.09); план `plans/team/team-work-plan.md` принят 08.10 с ответами §7
(«реализуй фазу ноль, вернусь через 10 часов»). D-0036 — интеграционным коммитом этой пачки.
Порядок по общим файлам: `.githooks/pre-commit`, `tools/mechanism_gate.py`, `tools/hook_liveness_probe.py`,
`CLAUDE.md`, `PROCESS/`, `DECISIONS.md` — пишет только Lead при слиянии (гейт механизмов не пускает билдера);
`README.md` и `docs/RUNBOOK.md`: F0-6 → F0-7; `plans/BACKLOG.md`: только F0-3; `CURRENT_CONTEXT.md`: только F0-5.
Скоуп свидетеля: узел — свой тест (`tools/test_piles.py`, `tools/test_journal_*.py`, …) + `python tools/lint_ratchet.py --check`
+ `python tools/dup_ratchet.py --check`; интегратор — `python -m pytest tools/ -q`, `python tools/hook_liveness_probe.py`,
`python tools/wiring_check.py`, boot-бюджет из SessionStart.
Общий бриф дизайнерам: план §2–§3 целиком; шаблоны `plans/piles/_template/*`; эта пачка; правила
`CLAUDE.md` (журнал, гейты), `plans/builder-rules.md`; вернуть спецификацию в `docs/tasks/specs/t-nnn-<узел>.md`
с развилками наверх, не решёнными.

## Узлы

| Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус |
|---|---|---|---|---|---|---|
| F0-1 | П1 | раскладка папок, три шаблона (`_template/`), карточка Forge и этот файл | Lead (форматы — архитектура) | `plans/piles/_template/*`, `plans/piles/forge/*` | — | принято: ff353757 |
| F0-2 | П1 | `tools/piles.py` split / board / check / take / release + `tools/test_piles.py`; хук pre-commit (контент — в отчёте, кладёт Lead) | designer → builder → critic | `tools/piles.py`, `tools/test_piles.py`, `plans/PILES.md` | F0-1 | принято (разрезан на 2a t-589 d34defa, 2b `piles_split.py` t-590 83a3c45, 2c t-591 65c2028; критик плана t-587, критик диффа t-593, фиксы t-594 50117d0; хуки c671386) |
| F0-3 | П1 | заморозка BACKLOG.md: шапка-указатель, `split` исполнен, 11 карточек, findings из строк, список «закрыть словом» | builder (по выводу `split`) | `plans/BACKLOG.md`, `plans/piles/*/README.md`, `plans/piles/*/findings/*`, `plans/PILES.md` | F0-2 | принято (Lead: split с 41 назначением, 10 карточек + 198 находок, заморозка 08.10 open=343 closed=84) |
| F0-4 | П1 | журнал на разработчика: `logs/journal/<dev>.jsonl`, `developer:` в `delegation.config.yaml`, один загрузчик `journal_keys.load_all()`, читатели через него (B-454), валидатор по файлу, CI forge-check | designer → builder → critic (мех-пути кладёт Lead) | `tools/journal_keys.py`, `tools/journal_validator.py`, `tools/session_context.py`, `tools/forge_metrics.py`, `tools/calibration_counts.py`, `tools/journal_echo.py`, `tools/compact_snapshot.py`, `tools/dispatch_gate.py`, `tools/agent_budget.py`, `delegation.config.yaml`, `logs/journal/`, `.gitlab-ci.yml`, тесты | — | принято (дизайнер t-581; код c876e53 + b8f7d4c, тесты 7dbd1ba, t-585 в двух воркерах; слаг — `tools/dev.config.yaml`, не delegation.config; переключение 0222e85) |
| F0-5 | П1 | диета общих файлов: CURRENT_CONTEXT ≤ 10 КБ (старое — в compact-snapshots), `changelog.d/` + `scripts/changelog_assemble.py` в пакете (правило «DECISIONS — один писатель» — в F0-7) | builder → critic | `CURRENT_CONTEXT.md`, `docs/tasks/compact-snapshots/`, `ai-packages/qa-factory/changelog.d/`, `ai-packages/qa-factory/scripts/changelog_assemble.py`, `scripts/tests/test_changelog_assemble.py`, `scripts/selftest.py` (hygiene/lang видят фрагменты), `CHANGELOG.md` | — | принято (влито 05403ea, t-582; критик t-586 fit_with_fixes; фиксы t-588 влиты c732bd5) |
| F0-6 | П1 | разработчик без стенда владельца: `tools/dev.config.example.yaml`, читатели путей (`prepare_copy.py`, `run_headless.py`), README «взять пачку», RUNBOOK §9 | builder → critic | `tools/dev.config.example.yaml`, `tools/dev_config.py`, `experiments/measurers/prepare_copy.py`, `experiments/measurers/paths.py`, `README.md`, `docs/RUNBOOK.md`, `.gitignore` | — | принято (влито 03f9f8b + 7f980f9, t-583/t-584; критик t-586 fit_with_fixes; фиксы t-588 влиты c732bd5) |
| F0-7 | П1 | правила: PROJECT.md «Командная работа», CLAUDE.md host-адаптация 7, калибровка проверка 18, SIBLING_MAP ось 12, DECISIONS D-0036 | Lead | `PROJECT.md`, `CLAUDE.md`, `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`, `docs/SIBLING_MAP.md`, `DECISIONS.md` | F0-2, F0-4 | принято (Lead, b8f7d4c: PROJECT.md «Командная работа», CLAUDE.md адаптация 7, проверка 33, ось 12, D-0036, builder-rules п. 2/11) |
| F0-8 | П2 | GitLab-зеркало: issue на пачку, label `pile::<slug>`, milestone, assignee; `board` подтягивает assignee/статус | builder → critic | `tools/piles_gitlab.py`, `tools/test_piles_gitlab.py` | F0-1 (форматы), F0-2 (board) | принято (t-592 6192e3e, критик t-593, фиксы t-594; первый `--apply` — Lead после заморозки) |

## Ход

- 08.10 08:40 — пачка открыта; F0-1 сдан Lead (шаблоны и эта пачка); дальше: дизайнеры F0-2 и F0-4, билдеры F0-5 и F0-6 (≤ 4 воркеров), потом F0-3, F0-8, F0-7.
- 08.10 09:12 — F0-5 и F0-6 влиты (`05403ea`, `03f9f8b`, `7f980f9`), критик t-586 — fit_with_fixes, раунд фиксов t-588 (свежий билдер); спеки F0-2 (t-580) и F0-4 (t-581) приняты с решениями Lead по развилкам; критик на план F0-2 — t-587; билдер F0-4 — t-585. Решение по дублированию: единственный читатель `tools/dev.config.yaml` — `tools/dev_config.py` (stdlib), `journal_keys.developer_slug()` делегирует ему (поправка к F-1(b) спеки t-581, выполняется при интеграции F0-4).
- 08.10 11:20 — все узлы приняты: F0-4 в двух воркерах (первый остановлен хуком бюджета на 450K — мера 1 D-0035 сработала), F0-2 разрезан по критику плана на 2a/2b/2c, критик инструментов t-593 → раунд t-594; гейт кучек живой с c671386; журнал переключён (0222e85); split и заморозка — этим коммитом. Остатки → `findings/` forge (строки ниже) и пачка 2.
- 08.10 23:11 — по слову владельца: метки `priority::П1/П2/П3` в зеркале (t-595, `d4a6aa1f`, применено: 3 метки,
  12 issues, контрольный dry-run чист); три новые находки в `findings/` (остаток остановленного воркера, кучка без
  карточки, метки приоритета — закрыта); B-229 получил требование о правиле приёма чужих находок.
- 09.10 10:15 — ночь: четыре воркера сдали (t-596…t-599), сессия встала на `cd`; утром Lead закоммитил t-596 (`a3b5f0c5`),
  слил t-596/t-597/t-598 (`0ec43482`, `3725ee77`, `d319c699`), принял по свидетелям, `release` → `close` во всех носителях,
  закрыл 8 строк словом владельца, шесть находок; вторая волна t-601 (git-раннер, m-7, прочерк в `подтвердил:`) слита
  `d883049c`; пачки 2–4 собраны из черновика дизайнера t-602 (`65a24ee4`); критик t-603 — один проход по всему диффу остатков.

## Живые доказательства

| Что | Стенд / проект | Кто | Статус |
|---|---|---|---|
| разработчик с чистого клона берёт пачку по README за 10 минут | клон dev2 | dev2 | передано в кучку live-runs (`findings/20261008-forge-pachka-1-zhivye-dokazatelstva.md`, 365ca089): проверяется на первой пачке dev2 |
| два журнала (`<dev>.jsonl`) сливаются без конфликта и без строк идентичности | первое слияние ветки dev2 | интегратор | передано в кучку live-runs (та же находка) |

## Остатки

- (критик t-586, N9) `tools/ci_read.py` читал `GITLAB_TOKEN` сам, не через `dev_config.gitlab_token_env`; `scripts/tests/test_critic_rollcall_apply_fixes.py` зашивал раскладку владельца | сделано: t-597
- (критик t-586, N3) builder-rules п. 11 «2–4 строки CHANGELOG» → фрагмент `changelog.d/`; рецепт релиза — шаг `changelog_assemble.py` и проверка «в changelog.d только README»; SIBLING_MAP ось 3 — узел F0-7 | сделано: b8f7d4c
- Карточка Forge, пачка 1: B-162 и B-267 не про корень путей (критик t-586, п. 7) — строки аннотированы «(пути)», не закрыты | сделано: c55ccd86
- (критик t-593, очередь) m-1, m-5, m-8, m-10, m-11 и разрез `test_piles.py` по командам (каждый файл < 60 с) | сделано: t-596
- (критик t-593, очередь) m-7 — проверка заморозки (в) сравнивает с явной базой в CI; один git-раннер `tools/gitcmd.py` на шесть обёрток в tools/ (звенья цепи механизмов — пачка 2, узел F2-11) | сделано: t-601
- (критик t-593, очередь) публичное имя `ci_read.request`, алиас снят при интеграции | сделано: t-597
- F0-9 — читатели BACKLOG (`forge_metrics`, `compact_snapshot.backlog_rows`) читают находки | сделано: t-598
- CLOSED BY TEXT (59 строк): скаут t-599 — 12 закрыть / 28 частично / 18 открыто / 1 оставить; 8 строк закрыты словом владельца 08.10 через `close --id --word`, 3 — члены живых пачек других кучек, B-331 — вопрос владельцу (находка) | сделано: 3ba5f274

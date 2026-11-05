# Сбор — пачка 1: данные проекта, работающего на фабрике, приходят разработчикам одним архивом без секретов и имён и ложатся в кучки

кучка: `collect` | статус: закрыта | взял: — | ветка: — | MR: `855d4e5c` | стенд: только CL1-7 | приоритет: П2 | issue: https://git.example.com/dev1/yml-text-factory/-/work_items/37

Правило готовности: пачка закрыта, когда каждый узел «принято», свидетели узлов — в журнале взявшего, живое доказательство
CL1-7 (FR-33; таблица ниже) сделано, а строки «Остатков» закрыты `сделано:` или переданы человеком подтверждённым переносом.

Решения владельца: D-0052 (слово владельца 19.10.2026: семь пунктов закона о сборе), D-0053 (слово владельца 19.10.2026: все 14
развилок черновика t-962 — по рекомендации дизайнера). Решения Lead пачки, 19.10.2026: §L и §L-2 спеки
`docs/tasks/specs/t-962-collect-skill.md` (семь мажоров и двадцать миноров критика t-972 приняты в его форме); где текст §1–§9 и
§L-2 расходятся, действует §L-2.
Порядок по общим файлам: CL1-1 → CL1-2 → CL1-8; CL1-3 ∥ CL1-1; CL1-4 после CL1-2, CL1-3; CL1-5 ∥ (свой критик на план); CL1-6 после схемы CL1-2; CL1-7 последним.
очередь: codex/1 → collect/1
очередь: `runtime_paths.py (resolve_runtime)` / `release_fingerprint.py (package_fingerprint)`: CL1-8 → C3-26 (`conductor/3`; t-1019 m-12; кэш — вне `compare()`); `install_smoke.py (package_fingerprint)`: CL1-8 ∥ PC1-2 (`compare_trees`) ∥ LR1-5 (первая строка) — списки функций в каждом диспатче
Причина строки выше: `skills/qa-story/SKILL.md` пишут раньше CX1-13, CX1-14, CX1-15 (кучка `codex`) и G1-0 (кучка `grounding`); строку CL1-5 в нём пишет интегратор (builder-rules п. 1) при слиянии; такая же строка нужна в преамбуле `codex/batch-1-overhead-fixes.md`, когда обе пачки в работе.
Пути «Пишет в»: пакета — от `ai-packages/qa-factory/`, прочие — от корня репозитория; в диспатче узла — полные пути.
Скоуп свидетеля: каждый узел — свой тестовый файл из «DoD узлов» ниже на Windows и в docker `python:3.12` на копии дерева (форма t-908);
соседи один раз: `python -B scripts/selftest.py --limits --lang`, `python -B scripts/tests/test_audit_rules.py`, из корня
`python tools/dup_ratchet.py --check` и `python tools/lint_ratchet.py --check`; полный канон — интегратор при слиянии (CI `package-fast`).
Общий бриф дизайнерам: `docs/tasks/specs/t-962-collect-skill.md` §L и §L-2 (главнее текста §1–§9), ревью
`docs/tasks/specs/reviews/t-972-t-962-collect-plan.md`, перепись `docs/tasks/specs/reports/t-948-collect-census.md`; вернуть спеку
`docs/tasks/specs/t-nnn-cl1-n.md` с развилками наверх; для CL1-1 и CL1-5 спеки уже есть (`t-973-cl1-1-machine-facts.md`,
`t-974-cl1-5-change-request.md`, оба с §L).

## Бриф

Что сделать: навык `/qa-factory:qa-collect` — один Bash-вызов кода собирает все наборы A–H в один архив (zip, части до 25 MB),
без LLM и без выбора человека; редактор замазывает пути, имена, хосты и секреты до записи (ни байта неочищенным); метка
`state/collect/mark.json` и `project_id`/`install_id` отделяют новое от отправленного; правило зависания выбирает транскрипты
только зависших историй; приём `tools/collect_intake.py` на нашей стороне кладёт находки в кучки по фичам, числа — в
`cost-dashboard`, предложения и чужие адаптации — в `proposals`, остальное показывает Lead строкой `unplaced`; правило D-0052 (3)
«просьба изменить фабрику оставляет след» — в тексты ролей, отпечаток релиза показывает правку установленного плагина.

НЕ делать: отправку по сети (человек отправляет файл сам, F-14); чтение ответов кодом (их читаем мы); пересчёт дашборда у нас;
правку `story_run.py`, `controller.py`, `hooklib.py` (расход `collect` на дашборде — узел CD1-11 кучки `cost-dashboard`); новую
анкету; пробы и доктор из навыка; «пропущенные баги» (носителя нет — узел RD1-6 кучки `report-delivery`); смену таблицы
шаблонов секретов гарда (узел OH1-8 кучки `onboarding-hooks`); правило D-0052 (3) в `qa-onboarding` и `qa-doctor` (узел OH1-9).

Первые ходы: CL1-4 — байты `skills/qa-collect/SKILL.md` (цель ≤ 4 КБ, потолок 19000 Б) и API `human_text` для пина текста двух
вопросов; CL1-5 — байты `conductor.md`, `common-rules.md` и инжекта роли против капов, `wc -c` на HEAD до любой правки; CL1-3 — `import
controller` не имеет побочных действий на импорте (иначе множества статусов копируются, и пин сверяет копию); CL1-1 — читатель
env-файла с file:line (F-8 спеки t-973); CL1-2 — что `install_paths` делает с файлом под `state/`, не названным строкой.

Узлы-механизмы (CL1-4, CL1-5, CL1-6, CL1-8; m19 ревью): осевой блок «оси SIBLING_MAP» и строка `tier:` — на коммите слияния,
правило 10 `CLAUDE.md`.

**Owns по узлам** (из t-962 §9 и §L-2; CL1-1 по t-973, CL1-5 по §L t-974; в диспатче — полностью, абсолютными путями):
CL1-1 — `scripts/machine_facts.py`, `references/collect-redaction.json`, `scripts/tests/state_census.py` (`short83`, `path_variants`,
`_alternation`, `Detector.__init__` — три функции и построитель таблицы переезжают, тест-замер импортирует), `scripts/tests/test_collect_redact.py`;
CL1-2 — `scripts/collect_pack.py`, `references/collect-sets.json`, `references/install-paths.json`, `scripts/tests/test_collect_pack.py`;
CL1-3 — `scripts/collect_stall.py`, `scripts/tests/test_collect_stall.py`;
CL1-4 — `skills/qa-collect/SKILL.md`, `scripts/activity_capture.py` (только `TYPES` и новое `FACTORY_TYPES`), `scripts/dashboard_cost_groups.py` (строка 84),
проводка транскриптов H в упаковщик (`scripts/collect_pack.py`, m17), `changelog.d/collect-1-cl1-04-skill.md`;
CL1-5 — `references/conductor.md`, `references/common-rules.md`, `scripts/project_decisions.py` (`main`, `add_finding`, `_cells`),
`scripts/person_words.py` (только список в докстринге модуля), `scripts/tests/test_project_decisions_change_request.py`,
`changelog.d/collect-1-cl1-05-change-request.md`; `skills/qa-story/SKILL.md` — интегратор;
CL1-6 — `tools/collect_intake.py`, `tools/test_collect_intake.py`, `tools/dev_config.py` (+`collect_inbox`), `tools/dev.config.example.yaml`,
`tools/piles.py` (`+parse_zone` — один читатель зоны, D-0048);
CL1-8 — `references/release-fingerprint.json`, `scripts/release_fingerprint.py` (один рецепт отпечатка, который читают
`install_smoke.package_fingerprint` и `runtime_paths`), `scripts/tests/test_release_fingerprint.py`, `docs/RUNBOOK.md` (строка шага релиза:
файл исключён из собственного отпечатка).

**DoD узлов** (из `ai-packages/qa-factory`; свой файл — на Windows и в docker `python:3.12` на копии дерева, форма t-908):
CL1-1 `python -B scripts/tests/test_collect_redact.py`, `python -B scripts/tests/test_state_portability.py`, `python -B scripts/tests/test_resolver.py`;
CL1-2 `python -B scripts/tests/test_collect_pack.py`, сосед один раз `python -B scripts/tests/test_install_paths.py`;
CL1-3 `python -B scripts/tests/test_collect_stall.py`;
CL1-4 `python -B scripts/selftest.py --limits --lang` и пин текста двух вопросов через `human_text`;
CL1-5 `python -B scripts/tests/test_project_decisions_change_request.py`;
CL1-6 `python -m pytest tools/test_collect_intake.py -q` и `python tools/piles.py check --all` на копии дерева после `--apply` фикстуры и строк Lead;
CL1-8 `python -B scripts/tests/test_release_fingerprint.py`;
CL1-7 ключи: архив собран; равенство приёма (на входе = разложено + `unplaced` + дублей) напечатано; скан распакованного архива на формы имени, 8.3
и имени машины и хосты стенда пуст при положительном контроле той же формы на исходном дереве (детектор инварианта «ни байта неочищенным»);
два разных `install_id`; доля `unplaced` посчитана (метрика узла).
Docker: `MSYS_NO_PATHCONV=1 docker run --rm -v <worktree>:/src:ro python:3.12 sh -c "cp -r /src /repo && cd /repo/ai-packages/qa-factory && python -B scripts/tests/<file>.py"`.

**Мутации** (одна — один файл; ожидания — из D-0052 и t-948, не из выхода кода, FR-58): замена имени без 8.3 → `test_collect_redact`
«8.3»; шаблон `Bearer` убран из данных → он же; значение `aws_secret_access_key` остаётся → он же; `names_only` склеил JSON → он же
«JSON остался JSON»; `prefix_sha256` не сверяется → `test_collect_pack` «переписанный журнал»; полстроки берётся → он же «запись идёт»;
`check-ignore` пропущен → он же «state не игнорируется»; `running` без `dispatch_liveness` → `test_collect_stall` «идёт сейчас»;
`returned_unaccepted` без окна по `returned_at` → он же «роль только что вернулась»; `stale` снова сигнал → он же; `unknown`
считается зависанием → он же; ожидание человека → он же «ждёт человека»; фильтр стеблей снят → он же «чужой субагент»;
`..` в члене не отказан → `test_collect_intake` «zip-slip»; `unplaced` не считается → он же «равенство элементов»;
`install_id` не в ключе дедупа → он же «две установки»; имя без `hhmm` → он же «второй архив за день».

Первые 10 минут: прочитать карточку («Решения», «Дороги»), преамбулу выше и строку своего узла; первый диспатч — дизайнер (где в
«Исполнителе» он есть) или билдер со спекой узла.

## Узлы

Исполнитель «designer → critic на план → builder → critic» — узел меняет смысл гейта или несёт развилку (PROJECT.md п. 6);
«builder» — узел без развилки. Статусы: `ожидает` → `в работе` → `сдано` → `принято` / `отклонено`.

| Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус |
|---|---|---|---|---|---|---|
| CL1-1 | П2 | Редактор (ни байта неочищенным наружу): написания путей из тест-замера — в модуль пакета (F-8), JSON-осознанные замены, шаблоны секретов и хостов в данных, `machine_identities`; `state_census` импортирует модуль. Тесты: `test_collect_redact.py` (все неудобные входы §4 и таблица «Утечки редактора» ревью t-972, имя AT 3 / BEYOND 2); самотест `state_census`. Критик: да (фильтр выпуска наружу) | designer → critic на план → builder → critic | `scripts/machine_facts.py` (новый), `references/collect-redaction.json` (новый), `scripts/tests/state_census.py (short83, path_variants, _alternation, Detector.__init__)`, `scripts/tests/test_collect_redact.py` (новый) | — | принято, слито (t-986: две попытки, критик кода t-999, фикс-раунд t-1009; докер 236/236; спека t-973 §L/§L-2/§L-3) |
| CL1-2 | П2 | Сборщик: наборы A–H из данных, метка и хвосты по префиксу байт, `project_id` и `install_id`, манифест (в нём `package_modified: yes\|no\|unknown` по отпечатку CL1-8), zip с частями до 25 MB, потолки, `git check-ignore`, отказы; строки `install-paths.json` для `state/collect/**` (класс `carried`, `machine_local`); тест «каждый путь наборов — строка `install-paths` или путь истории реестра артефактов». Тесты: `test_collect_pack.py` (края 1–10, 13–15) | builder → critic | `scripts/collect_pack.py` (новый), `references/collect-sets.json` (новый), `references/install-paths.json`, `scripts/tests/test_collect_pack.py` (новый) | CL1-1 | принято, слито (8a1840cf; t-1020 a2 под критиком t-1043, фикс-раунд t-1051; docker test_collect_pack 103/103, test_collect_redact 242/242, test_install_paths 291/291) |
| CL1-3 | П2 | Правило зависания (чистая функция, сигналы K1…K7, окна по времени каждого сигнала, «идёт сейчас» и «ждёт человека» — не зависание, нечитаемое — `unreadable`) и выбор транскриптов набора H по стеблям сессий зависшей истории. Тесты: `test_collect_stall.py` (K1…K7, «идёт сейчас», «роль только что вернулась», «чужой субагент», `unreadable`) | builder → critic | `scripts/collect_stall.py` (новый), `scripts/tests/test_collect_stall.py` (новый) | — | принято, слито (d6f3f666; t-1004 a2 под критиком t-1018, фикс-раунд t-1025; docker test_collect_stall 193/193) |
| CL1-4 | П2 | Навык `qa-collect` (два вопроса одним сообщением, слова дословно в файлы, один Bash, сводка дословно); вид активности `collect` и одно множество `FACTORY_TYPES` (`TYPES` — псевдоним), которое читает `dashboard_cost_groups.py:84`; проводка транскриптов H в упаковщик; фрагмент changelog; фича F22 в `plans/features.json` — Lead. Механизм: осевой блок на слиянии | builder | `skills/qa-collect/SKILL.md` (новый), `scripts/activity_capture.py`, `scripts/dashboard_cost_groups.py`, `scripts/collect_pack.py`, `changelog.d/collect-1-cl1-04-skill.md` (новый) | CL1-2, CL1-3 | принято, слито (d9b8729e; t-1051 a2 под критиком t-1055, фикс-раунд t-1072; docker test_collect_pack 157/157, test_collect_skill 30/30, test_collect_stall 195/195, audit rules 218/218 — A1 закрыт) |
| CL1-5 | П1 | Правило D-0052 (3) «просьба изменить фабрику оставляет след в находке или решении» по F-1 (a): строка в `conductor.md` и `common-rules.md`, слова человека — файлом (`--words-file`) с маркером `change-request:` и хвостом-хэшем, три латентных дефекта `add-finding` для всех вызывающих; строки для `qa-story/SKILL.md` — интегратору. Механизм: осевой блок на слиянии | designer → critic на план → builder → critic | `references/conductor.md`, `references/common-rules.md`, `scripts/project_decisions.py (main, add_finding, _cells)`, `scripts/person_words.py`, `scripts/tests/test_project_decisions_change_request.py` (новый), `changelog.d/collect-1-cl1-05-change-request.md` (новый), `skills/qa-story/SKILL.md` (интегратор) | — | принято, слито |
| CL1-6 | П2 | Приём `tools/collect_intake.py`: проверка недоверенного архива, распаковка в inbox вне git, дедуп по паре (`project_id`, `install_id`), раскладка элемент → фича → кучка (зона — один читатель `piles.parse_zone`), `unplaced` и `--place`, `--apply` пишет находку на (архив × кучка) и печатает строки Lead; ключ inbox в `tools/dev_config.py`. Механизм: осевой блок на слиянии | builder → critic | `tools/collect_intake.py` (новый), `tools/test_collect_intake.py` (новый), `tools/dev_config.py`, `tools/dev.config.example.yaml`, `tools/piles.py (+parse_zone)` | CL1-2 (схема — из спеки, фикстура архива своя) | принято, слито (c33f1761; t-1066: два воркера (колпак 400K, финишер t-1088), критик кода t-1072 fit_with_fixes, фикс-раунд t-1099; docker test_collect_intake 71 + test_piles — 219 passed; owns сверх строки: `tools/piles.py (parse_zone, Finding.source)`, `plans/piles/_template/README.md`; отклонения D1–D5 и Q3 приняты; `--archive-max-bytes` — дверь колпака) |
| CL1-7 | П2 | Живое доказательство (FR-33): сбор на КОПИЯХ cmp2r и cmp3gb → приём в копию дерева кучек; это и детектор D-0052 | Lead + builder | `docs/tasks/handoffs/` (отчёт узла) | CL1-1…CL1-6, CL1-8 | закрыта: перенесено 01.11.2026 → live-runs/2 |
| CL1-8 | П2 | Отпечаток релиза (детектор (c) правила D-0052 (3); механизм): ОДИН рецепт отпечатка пакета в `scripts/release_fingerprint.py`, который читают `install_smoke.package_fingerprint` и `runtime_paths`; файл `references/release-fingerprint.json` пишет шаг релиза и исключён из собственного отпечатка; сборщик сравнивает отпечаток установки с файлом и пишет `package_modified` в манифест. Осевой блок и `tier:` — на коммите слияния | designer → critic на план → builder → critic | `references/release-fingerprint.json` (новый), `scripts/release_fingerprint.py` (новый), `scripts/tests/test_release_fingerprint.py` (новый), `docs/RUNBOOK.md` | CL1-2 (манифест) | принято, слито (01152924; t-1038 a2 под критиком t-1047, фикс-раунд t-1060; docker test_release_fingerprint 161/161, test_runtime_paths 78/78) |

## Ход

—

- 20.10 00:1x — CL1-3 слит в `main` 73d3e0f6 (docker test_collect_stall 193/193); ничего его не импортирует до CL1-4
- 20.10 00:2x — CL1-2 вернулся ЧАСТИЧНО на капе 400K (WIP 7fe625b3); остаток — свежий воркер t-1031 (D-0038) в том же дереве → 1afc8b2e (74/74, соседи, docker, 6 мутаций); ответы Lead на 7 отклонений — в диспатче (имя архива `install_id[:8]`, 25 000 000 Б, код `fingerprint_unavailable`); критик кода t-1043
- 20.10 00:5x — CL1-8 §L-2 (ревью t-1019) → билдер t-1044 ∥ CL1-2; клетки «Зависит» читаются так — CL1-2 ← CL1-1, CL1-8; CL1-8 ← —; `references/release-fingerprint.json` узел НЕ создаёт (F-3 (b)); пачка 2 открыта «ожидает» (CL2-1 третий рецепт, CL2-2 дефекты редактора по отчёту CL1-2)

- 20.10 10:4x — CL1-6 слит (приём архивов `qa-collect/1`: проверка без распаковки, инбокс по sha, дедуп по (project_id, install_id), один читатель зон `piles.parse_zone`, находки целиком-или-ничего с `--place`, строки Lead; сверка индекса ДО записи находок, SOURCES по сырым спискам, GIT_* очищен целиком, `piles.write_bytes_atomic`, двери `--archive-max-bytes`/`DOOR_UPDATE`, указатели относительно инбокса); `tools/collect_intake.py` в сети `tools/mechanism_gate.py`; строка карты ось 12; очередь критика t-1072 → «Остатки»; дальше CL1-5/CL1-7 ждут слова владельца

- 20.10 11:5x — слово владельца (чат): стенд полностью у фабрики — CL1-7 гоняется на текущей конфигурации, если она подходит, иначе пересобирается; каждая пересборка стоит времени — продумать, когда пересобирать и что гонять. CL1-5 X1 = (а) (t-974 §L-4), дизайнер X2 запущен (t-1111). CX1-15: F-1 терра в данных, F-2 тарифы по умолчанию с пометкой, без нового узла (t-1041 §L-2).

- 20.10 15:5x — CL1-5 слит (правило D-0052 (3): просьба человека изменить фабрику оставляет след — `project_decisions.py add-finding --words-file … --idempotency-key change-request:<T>`, строка FB в `factory-backlog.md`; inline `--witness` под ключом класса `change-request` отказан с дверью `--words-file` (FR-1); `audit_factory.py:712-730` читает строки через `_cells`; `_escape` сворачивает все переводы строк, дайджест — по свёрнутому тексту; тексты `conductor.md`/`common-rules.md` C1a–d, C2a–c; строки SKILL.md C3a–e положены интегратором (18925 Б, `--limits` зелёный)). Две попытки: t-1118 (критик t-1122 fit_with_fixes), фикс-раунд t-1127; docker-контроль билдера 128/128, 218/218. Очередь → «Остатки»; находки → cost-dashboard/1 CD1-12, grounding/2 G2-10, collect/2 CL2-3; ось 21 карты. Дальше: CL1-7 живое доказательство на копиях стенда (слово владельца 11:5x)
- 21.10 11:3x — слово владельца (чат): «Законные переносы в другие кучки подтверждаю. Всё, что касается текущих кучек, надо доделывать». Применение: строки «Остатков», которые дизайнер t-1241 (журнал t-1187) классифицирует как перенос в другую кучку (CD1-11, OH1-9, kb и т.п.), получают `подтвердил: владелец, 21.10.2026`; всё остальное — узел CL3-1 (один билдер) или `сделано: <хэш>` по уже закрытым; CL1-7 и живые доказательства — за владельцем (стенд, копии cmp2r/cmp3gb).
- 01.11 — закрыта по слову владельца 01.11.2026 (пересборка бэклога): открытые узлы → live-runs/2

## Живые доказательства

| Что | Стенд / проект | Кто | Статус |
|---|---|---|---|
| CL1-7: сбор навыком на копиях двух проектов и приём архивов в копию дерева кучек: архив собран, равенство приёма напечатано, скан распакованного архива на формы имени, 8.3, имя машины и хосты стенда пуст при положительном контроле на исходном дереве, два разных `install_id` | копии cmp2r и cmp3gb | Lead + builder | перенос: live-runs/2 «Живые доказательства» \| обоснование: пересборка бэклога \| подтвердил: владелец, 01.11.2026 (слово 2 пересборки) |

## Остатки

- Сведение `http_client.safe_url` и `manual_capture._safe_url` с хэшем хоста в `machine_facts` — после CL1-1 (m2 ревью t-972; хэш хоста — одна функция в `machine_facts` поверх `safe_url`). | перенос: driver-hosts/findings/20261101-ostatki-starykh-pachek-kodeks-sbor-granding-pri-peresborke.md | обоснование: пересборка бэклога | подтвердил: владелец, 01.11.2026 (слово 2 пересборки)
- Четвёртый чистильщик секретов `judge_run._redact` (`scripts/judge_run.py:232`) — в ту же таблицу после CL1-1 (спека t-973 §L, замеченное п. 2). | перенос: driver-hosts/findings/20261101-ostatki-starykh-pachek-kodeks-sbor-granding-pri-peresborke.md | обоснование: пересборка бэклога | подтвердил: владелец, 01.11.2026 (слово 2 пересборки)
- Литерал 6 порога хоста в `scripts/tests/test_state_portability.py:175` — свести к общему порогу при следующем касании файла (спека t-973 §L, замеченное п. 3). | перенос: driver-hosts/findings/20261101-ostatki-starykh-pachek-kodeks-sbor-granding-pri-peresborke.md | обоснование: пересборка бэклога | подтвердил: владелец, 01.11.2026 (слово 2 пересборки)
- Поле `collect` на строках `install-paths.json` вместо теста-сведения `collect-sets.json` с `install-paths` (m4 ревью t-972). | перенос: driver-hosts/findings/20261101-ostatki-starykh-pachek-kodeks-sbor-granding-pri-peresborke.md | обоснование: пересборка бэклога | подтвердил: владелец, 01.11.2026 (слово 2 пересборки)
- `FACTORY_TYPES` в `hooklib.py` и `cost_capture.py`: явный пробел — пока узел CD1-11 кучки `cost-dashboard` не слит, расход навыка `collect` на дашборде `Unclassified`, а `has_factory_activity` его не видит (находка `cost-dashboard/findings/20261019-factory-types-kopii-v-hooklib-i-cost-capture.md`; критик t-972 F-5). | перенос: driver-hosts/findings/20261101-ostatki-starykh-pachek-kodeks-sbor-granding-pri-peresborke.md | обоснование: пересборка бэклога | подтвердил: владелец, 01.11.2026 (слово 2 пересборки)
- F-5 спеки CL1-5 (t-974): правило D-0052 (3) в `qa-onboarding` и `qa-doctor` с маркером `change-request:project` — узел OH1-9 кучки `onboarding-hooks` (находка `onboarding-hooks/findings/20261019-prosba-izmenit-fabriku-v-onboarding-i-doctor.md`); до него правку плагина в этих сессиях ловит CL1-8. | перенос: driver-hosts/findings/20261101-ostatki-starykh-pachek-kodeks-sbor-granding-pri-peresborke.md | обоснование: пересборка бэклога | подтвердил: владелец, 01.11.2026 (слово 2 пересборки)
- CL1-1, очередь критика t-999 при слиянии (Lead, 19.10 23:2x): m-3 — свести к одному редактору `project_inventory._safe_remote`, `judge_run._first_url`, причуды `env_probe.parse_env_file` (`export ` ключи, ` # note` хвосты); m-5 — абсолютные пути вне домашних корней (`/opt/...`, `/var/lib/...`) проходят нетронутыми — решить на CL1-2 (сборщик видит те же пути); аналоги билдера: `test_state_portability.py:175` литерал 6, `manual_capture._safe_url`, близнецы `reachability.LOCAL`/`hosts_kept`; строка оси 5 карты «редактор ↔ гард: одна таблица секретов» (текст в хэндоффе t-987-cl1-1) — кладёт Lead ближайшей правкой карты | ранее-сделано: — | перенос: driver-hosts/findings/20261101-ostatki-starykh-pachek-kodeks-sbor-granding-pri-peresborke.md | обоснование: пересборка бэклога | подтвердил: владелец, 01.11.2026 (слово 2 пересборки)
- CL1-8, §L-2 M-1 (iii) (Lead, 20.10 00:5x) — CL1-6 печатает на архив `package_modified`, `why`, `running_version`, `install` (детектор (c) правила D-0052 (3); докстринг `release_fingerprint.py` называет эту строку) | ранее-сделано: — | перенос: driver-hosts/findings/20261101-ostatki-starykh-pachek-kodeks-sbor-granding-pri-peresborke.md | обоснование: пересборка бэклога | подтвердил: владелец, 01.11.2026 (слово 2 пересборки)
- CL1-1, дефекты по отчёту CL1-2 t-1024 (Lead, 20.10 00:5x): `Redactor.text()` квадратичен (64 КБ — 76 с), `residue()` ложный UNC на экранированном JSON — узел CL2-2 пачки 2; `defect_found` ref t-986 | ранее-сделано: строка CL2-2 | перенос: driver-hosts/findings/20261101-ostatki-starykh-pachek-kodeks-sbor-granding-pri-peresborke.md | обоснование: пересборка бэклога | подтвердил: владелец, 01.11.2026 (слово 2 пересборки)
- CL1-8, очередь критика t-1047 при слиянии (Lead, 20.10 02:5x): F7 три читателя версии `plugin.json` (`install_smoke.plugin_version`, `install_paths.plugin_version`, `config_contract.package_version`) сводятся к `hooklib._package_version_at`; F8 `selftest.cmd_hygiene` — свой читатель «что git не отслеживает», двойник `release_fingerprint._unshipped`; строка «Остатков» :127 дополняется: «`no_release_file` на версии, которая файл ВЕЗЁТ, — сигнал утечки (забытый `--write`)» — детектор (c) живёт с CL1-6; живое доказательство FR-33 — первый релиз с `--write` (таблица «Живые доказательства») | ранее-сделано: — | перенос: driver-hosts/findings/20261101-ostatki-starykh-pachek-kodeks-sbor-granding-pri-peresborke.md | обоснование: пересборка бэклога | подтвердил: владелец, 01.11.2026 (слово 2 пересборки)
- CL1-4, очередь критика t-1055 и фикс-раунда t-1072 при слиянии (Lead, 20.10 05:5x): Q1–Q4 ревью `t-1067-t-1051-cl1-4.md` (в т.ч. приём CL1-6: удалённый человеком файл транскриптов — не битый архив); три копии множества типов активности вне узла — `factory_dashboard.py:1888`, `metrics_projection.py:460`, `recover_codex_usage.py:32` (+ `hooklib.py:1227`, `cost_capture.py`) → находка `cost-dashboard/findings/20261019-factory-types-kopii-v-hooklib-i-cost-capture.md` дополняется списком (CD1-11); повторный прогон после двери `--extra`: второй архив несёт только новое с первого плюс extra — SKILL говорит «отправьте оба файла» (одна строка, следующее касание SKILL); «(or since the factory last packed them)» → «its records» (одно слово, тот же ход); `dashboard_cost_groups.py:90` мёртвое условие; `collect_stall.py:68` устаревший комментарий | ранее-сделано: — | перенос: driver-hosts/findings/20261101-ostatki-starykh-pachek-kodeks-sbor-granding-pri-peresborke.md | обоснование: пересборка бэклога | подтвердил: владелец, 01.11.2026 (слово 2 пересборки)
- CL1-6, очередь критика t-1072 (`t-1094-t-1066-cl1-6.md`) и фикс-раунда t-1099 при слиянии (Lead, 20.10 10:4x): F-6 формулировка `Finding.source` («один читатель» ↔ `finding_fields` читает `от`); F-7 одна строка схождения — `fence_for` ≡ `piles_split._fence`, четыре писателя заголовка находки (`piles_split.finding_text`, `collect_intake.finding_text`, `piles_testkit.py:110`, `hook_liveness_probe.py:950`), цикл остатка ≡ `collect_pack._verify`, `_expand_braces` для check (б); F-8 качество (`Archive.parts`, `Plan.taken` не читаются; `count_sources` дважды открывает zip; `ra_ep_elements` четыре уровня); F-9 повтор файла в `group_args` без строки; F-11 текст OPEN BATCH не печатается при повторе; Q1 фикс-раунда: SOURCES MISMATCH (не-объект в D2) — отказ без двери, только правка кода (FR-57: нужна дверь `DOOR_SENDER` «собрать заново» или информированный проход); Q3: сырой OSError в `write_inbox`/`write_findings` — ещё traceback (та же форма, что F-1); `Member.read` может пропустить сырой `_TooBig` (файл вырос между проверкой и чтением); `Refusal` одного архива в цикле `finish` обрывает последующие; детектор утечки «архив пришёл, intake не запущен» — на дисциплине (папка инбокса против `index.json`) | ранее-сделано: — | перенос: driver-hosts/findings/20261101-ostatki-starykh-pachek-kodeks-sbor-granding-pri-peresborke.md | обоснование: пересборка бэклога | подтвердил: владелец, 01.11.2026 (слово 2 пересборки)
- CL1-5, очередь критика t-1122 (`t-1122-t-1090-cl1-5.md`) и фикс-раунда t-1127 при слиянии (Lead, 20.10 15:5x): m-3 ключ с хвостовым пробелом → дубль при повторе; m-7 однострочный отказ занятого лока в `add`/`resolve`; Q1 `project_decisions.one_line` ↔ `http_client.py:45/:271` — один помощник управляющих символов; `audit_factory.py:1286` A16 `essence = cells[1]` обрезается на `\|` (недосчёт меры, ось 21) | ранее-перенос: collect/2 (CL2-2 дефекты редактора) | ранее-обоснование: правки читателя/редактора, не правила D-0052 (3) | ранее-подтвердил: — | перенос: driver-hosts/findings/20261101-ostatki-starykh-pachek-kodeks-sbor-granding-pri-peresborke.md | обоснование: пересборка бэклога | подтвердил: владелец, 01.11.2026 (слово 2 пересборки)

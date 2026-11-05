# Роль S5 проверяет ветку по имени, потому что ей не названо, где оркестратор её записал; сиблинги проверки источника

id: — | кучка: `codex` | от: Lead dev2 (прогон TP2-2406, Codex Desktop, S5, 17–18.10.2026), 18.10.2026 | приоритет: П2 | кандидат наверх: нет

Что не так / что сделать: qa-automator дважды остановился на входе в S5 (`S5-qa-automator-1`, `-2`, 17.10 14:25 и
14:37 UTC) со словами `not on story branch — orchestrator branch check did not run or failed`: он сравнил `git branch
--show-current` (`TP2-2406-factory-082-codex`) с `implementation.branch` из `context-manifest.json`
(`TP2-2406_session-feedback`) — это ветка-источник MR !57, оба имени стоят на одном коммите c4a2f1f. Устав роли
(`agents/qa-automator.md:35`) велит сверять «ветку, которую записал оркестратор», но не говорит, где она записана
(`state/test-repo-base.json`: `branch`/`head`, запись S0; её же одобрил гейт A — «S5 will write test code on branch …»),
а бриф S5 не несёт ни одной строки о ветке. Слово человека 17.10 15:07 (`state/words/s5-branch-identity-authoritative.txt`)
прошло блок, но следующий диспатч читал бы то же самое. Закрыто t-038 (спека `docs/tasks/specs/t-038-s5-branch-check-line.md`):
строка `Branch check:` в голове брифа для ролей с `execution-lifecycle.md` (из записи S0 и коммита манифеста, без git в
brief_pack), устав и lifecycle называют носитель, сравнение — по коммиту, никогда по имени.

Остаётся по теме (не в t-038):

- (а) **`source_preflight.resolve_source` считает папку фабрики содержимым источника**: на живом репозитории 2406 он отвечает
  `resolve_conflict`, `write_allowed: false`, `source content differs from the working tree` — расхождения только
  `qa-factory/config.json` и `qa-factory/factory-backlog.md` (отслеживаемые файлы самой фабрики). `test_repo_base`
  исключает `qa-factory/` (`dirty_excluded`), `source_preflight` — нет. Класс FR-17/FR-54: одно определение «что не
  репозиторий тестов» на два читателя.
- (б) **Шаг s0.md:424 («перед правами на запись — `source_preflight.py`») в прогоне Codex не выполнялся ни разу**
  (`records/journal.jsonl`: 0 упоминаний); «orchestrator's branch check» из `execution-lifecycle.md:10` — обещание
  текста без кода на пути (в режиме драйвера `story_run` его тоже не зовёт). Либо гейт A `check_vcs` и есть эта проверка —
  тогда так и написать роли, либо шаг нужен в коде.
- (в) **Строка ремонта брифа цитирует halt предыдущей роли как причину диспатча** (`brief_pack` ~:1099: «This is a repair
  dispatch - cause unnamed: Mandatory branch identity conflict…»): утверждение роли становится словами фабрики для следующей
  роли (FR-35). t-038 ставит строку фабрики раньше; саму цитату не меняет.
- (г) **Запросы к дирижёру без ответа**: `S5-qa-automator-1.help.yaml`, `-2.help.yaml` лежат с заполнителями в `answer:`;
  роли выдумали поля (`source_and_branch_check`, `scope`). На Codex Desktop дирижёр (оркестратор-тред) на help.yaml не
  отвечает — путь `handoff_help.py` там мёртв; детектора нет.
- (д) **`checkpoint.remaining` наследуется ретраем дословно** (`_retry_packet`, «the checkpoint is inherited verbatim»):
  слова роли «S5 entry reconciliation required» идут в следующий пакет как оставшаяся работа. По замыслу — но слово
  человека, снявшее блок, в пакет не попадает; роль видит его только в `-decisions.md`.
- (е) **Слова halt'а `not on story branch — orchestrator branch check did not run or failed` и строка `SKILL.md:223`**
  («Re-run the S5 entry steps») не подходят к несовпадению коммита, которым стал заголовок отказа в уставе (критик t-039,
  F1); слова оставлены, потому что по ним матчится оркестратор. Переименовать вместе с таблицей SKILL.md.
- (ж) **qa-code-critic получает строку `Branch check:`** (его инъекция держит `execution-lifecycle.md`), но раздел «Before
  the first write» помечен `roles: qa-automator` — у критика 381 Б в голове без текста контракта за ней (t-039, F2).
  Либо пометить раздел и для критика, либо сузить набор ролей строки.
- (з) **Голова брифа S5 у потолка 6 КБ теряет встроенную шапку карты репозитория** (замер t-039: без строки 6047 Б,
  со строкой 6428 Б > потолка; карта остаётся ссылкой). Измерить трение (FR-55): читает ли роль файл карты сама.
- (и) Мелочь: `_one_line` в `brief_pack.py` — третий нормализатор пробелов рядом с `_clip` и `_short`.

Свидетель: `C:\Runway202609\nightwing-2406-codex\qa-factory\artifacts\TP2-2406\work\handoffs\S5-qa-automator-{1,2}.help.yaml`
(`tried: git branch --show-current -> …factory-082-codex; context-bundle recorded …_session-feedback`); `state/test-repo-base.json`
(`branch`, `head`); `state/words/s5-branch-identity-authoritative.txt`; копия брифа `-2` на scratch без строки о ветке
(`<scratch>/t038/brief-2-copy.json`); `source_preflight.py --repo … --source-ref c4a2f1f… --task TP2-2406` (только
чтение) → `action: resolve_conflict`, `content_mismatches: [qa-factory/config.json, qa-factory/factory-backlog.md]`.

Принципы и правила: P1, P9, P13, FR-15, FR-38, FR-16, FR-41, FR-49, FR-17, FR-54, FR-35.

Решение владельца нужно: нет.
перенесено из ветки dev2/codex-overhead-fixes (plans/piles/roles-context/findings/20261018-s5-branch-check-carrier.md), узел: CX1-7

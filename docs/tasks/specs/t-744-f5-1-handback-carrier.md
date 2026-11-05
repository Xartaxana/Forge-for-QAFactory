# t-744 — узел F5-1 пачки `forge/5`: носитель отчёта воркера — файл, который пишет сам воркер (F19)

Черновик дизайнера (Opus, 14.10.2026) по брифу Lead 14.10.2026. Развилки (§7) не решены — возвращаются Lead'у; §L —
раздел Lead, здесь его нет. Строки кода — HEAD `1a3456be` (main), каждая перечитана этой сессией (§9). Находка-источник:
`plans/piles/forge/findings/20261013-pustye-transkripty-subagentov.md`; строка узла — `plans/piles/forge/batch-5-vhodyashchie.md:24`,
живое доказательство — там же :51.

## §1. Цель и замысел

Отчёт воркера (critic, scout, designer, builder) доходит до Lead ФАЙЛОМ, который воркер пишет сам, а не текстом,
который Lead переписывает на самой дорогой модели. Три механизма, каждый со своими четырьмя вопросами (§4):

- **М-а. Write на один путь.** Роли critic, scout, designer получают инструмент `Write`; хук PreToolUse на
  `Edit|Write` разрешает такому воркеру писать ровно один файл — путь со строки `handoff:` его диспатча, и только в
  папке, назначенной его роли. builder уже пишет куда угодно (`builder.md:5`), для него ничего не ограничивается.
- **М-б. Извлечение кодом.** `tools/handback_extract.py` (из скрипта-черновика Lead) с тестом: для непустого
  транскрипта финальный текст воркера копирует код, не Fable.
- **М-в. Правило 25 строк.** В файлах ролей и в `docs/tasks/critic-diff-brief.md`: ответ в чате ≤ 25 строк, полный
  отчёт — файл по `handoff:`, приёмка читает файл.

**Расхождение брифа с измерением (важно для F-1, F-5).** Бриф: «половина файлов `tasks/a*.output` — 0 байт». Это
верно для `.output` (73 из 158), но сам транскрипт воркера `~/.claude/projects/<slug>/<session>/subagents/agent-<id>.jsonl`
пуст у 0 из 158; у трёх «пустых» скаутов находки (t-712…t-714) он весит 1,0–1,2 МБ, в каждом есть строка
`"name":"SubagentHandback"` (§2, Ф-1). Значит, пустой `.output` — это несозданная жёсткая ссылка (link count 1), а
не потерянный отчёт: М-б, читающий файл из `subagents/`, восстанавливает все 158 из 158. М-а и М-в остаются нужны по
другой причине — ответ воркера целиком попадает в контекст Lead при каждом возврате; с файлом и ответом ≤ 25 строк в
контекст идут 25 строк, остальное Lead читает, только когда нужно (оценка, не замер).

## §2. Факты со следом

Каждая строка — файл:строка, прочитано этой сессией.

| # | Факт | Носитель |
|---|---|---|
| Ф-1 | `.output` этой сессии: 158 файлов, 0 байт — 73, link count 2 — 85; `subagents/agent-*.jsonl`: 158, 0 байт — 0. `ab6233f5fbed2af68` (`.output` 0) → jsonl 1186679 Б; `a076f2ad75f5f90ba` → 1056785; `a016518af2cfedb05` → 1015527; контроль `afbb0c04fb8aee325` (`.output` 930221, link 2) → jsonl 930221 Б, link 2. Во всех четырёх `grep -c '"name":"SubagentHandback"'` = 2, `agentType` = `scout` | §9, команды М-1…М-3 |
| Ф-2 | `owns_gate.py` зарегистрирован только на `Task|Agent` (settings.json:27, :39) — он работает в сессии ДИСПЕТЧЕРА в момент запуска и записи воркера не видит; всегда возвращает 0 (owns_gate.py:1095–1102, докстринг :442–449 «the exit code is ALWAYS 0»). Бриф называет его хуком, «который уже ограничивает записи воркера по `owns:`» — это не так: он пишет реестр `logs/owns_registry.jsonl` и предупреждает о пересечениях (:265–283) | owns_gate.py |
| Ф-3 | Хук PreToolUse внутри субагента получает `agent_id` (замерено t-575); транскрипт воркера — `<transcript_path без .jsonl>/subagents/agent-<agent_id>.jsonl` | agent_budget.py:6–9, :100–110 |
| Ф-4 | Единый читатель транскриптов: `agent_file_name` (transcripts.py:50–54), `subagents_dir_of` (:57–60), `find_agent_transcript(agent_id)` (:63–74, ровно одно совпадение, иначе None), `is_finished` (:153–156, последний tool_use = SubagentHandback), `iter_lines` (:159–164, байты с заменой недекодируемых), `first_user_text` (:188–206, текст диспатча — первая строка `type == "user"`), `read_meta`/`agent_type` (:215–231, `agentType` из `agent-<id>.meta.json`, никогда не бросает) | transcripts.py |
| Ф-5 | Носитель одного пути найден: хук на `Edit|Write` в воркере может прочитать свой диспатч — `agent_id` (Ф-3) → файл воркера → `first_user_text` → `dispatch_manifest.section_cut` → секции `handoff`. Секция `handoff` уже режется (ключ `hand-?off`, dispatch_manifest.py:100; `section_cut` :240–291), но читателя путей этой секции нет: есть `owned_paths` (:403–420) и `given_paths` (:483–503) | dispatch_manifest.py |
| Ф-6 | Полнота манифеста проверяется только для `subagent_type == "builder"` или диспатча с путём в `owns:` (dispatch_manifest.py:28–31, :554–561); диспатч critic/scout/designer без `owns:` не проверяется вовсе | dispatch_manifest.py |
| Ф-7 | Лимит четырёх писателей (D-0040, DECISIONS.md:52) считает пишущим диспатч builder или любой с путём в `owns:` (dispatch_gate.py:1593–1600), а живого воркера — по `agentType == "builder"` из meta (transcripts.py:234–246). Поэтому путь отчёта читающей роли должен стоять на `handoff:`, НЕ на `owns:` — иначе критик/скаут займёт слот писателя; designer, запущенный как builder (сегодняшний обход), слот занимает | DECISIONS.md:52, dispatch_gate.py, transcripts.py |
| Ф-8 | Строки `tools:` ролей: critic `Read, Glob, Grep, Bash` (critic.md:5); builder `Read, Glob, Grep, Edit, Write, NotebookEdit, Bash, PowerShell` (builder.md:5); scout `Read, Glob, Grep` (scout.md:5; :47–49 «this role has no Bash … read-only is enforced by configuration»); designer `Read, Glob, Grep` (designer.md:5; :48–51 «Edit/Write are deliberately absent»); judge `Read, Glob, Grep` (judge.md:5). Бриф «роль с Bash и так пишет через shell» верен для critic и builder и НЕВЕРЕН для scout и designer: для них Write — новая способность, и хук несёт всю защиту | .claude/agents/*.md |
| Ф-9 | Правила «последнее сообщение = ПОЛНЫЙ отчёт»: builder п. 7 (builder.md:62–72), scout п. 9 (scout.md:75–83), critic п. 16 (critic.md:116–121), designer п. 5 (designer.md:52–56), judge п. 3 (judge.md:68–72). critic п. 17 (critic.md:122–135): последнее сообщение кончается блоком ```json по схеме | .claude/agents/*.md |
| Ф-10 | `tools/critic_verdict_check.py` принимает ПУТЬ к тексту вердикта (critic_verdict_check.py:12–14) — блок json можно проверять прямо в файле обзора | critic_verdict_check.py |
| Ф-11 | `critic-diff-brief.md:42–48` «What comes back»: «under about 1800 words, trail last, then the closing ```json block» — форма ответа в чате | critic-diff-brief.md |
| Ф-12 | `plans/builder-rules.md:29` п. 11: «Формат финального отчёта (≤ 500 слов, его читает интегратор)» | builder-rules.md |
| Ф-13 | Стоп по бюджету (agent_budget.py:192–210) пропускает Write/Edit только в `ALLOWED_DIRS = ("docs/tasks/handoffs", "docs/tasks/specs/reports")` (:73) относительно `cwd` хука (:179–189) и велит писать отчёт туда; `docs/tasks/specs/reviews` (папка критика) и `docs/tasks/specs` (папка дизайнера) там нет | agent_budget.py |
| Ф-14 | В репозитории: `docs/tasks/handoffs` — 75 файлов, `docs/tasks/specs/reviews` — 90, `docs/tasks/specs/reports` — 102 (отчёты скаутов, напр. `t-715-scout-piles-rules.md`, `t-740-calibration-map.md`) | `ls`, §9 |
| Ф-15 | Калибровочная проверка 28 «Completeness of workers' final messages» держит якоря пяти правил Ф-9 и подстроку «COMPLETE final report» в `dod_gate.py` (PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:821–845; dod_gate.py:119–126) — естественный дом детектора М-а/М-в. Счётчика «отчётов, переписанных Lead» в протоколе нет (grep `transcrib\|retyp\|by hand\|переписан` → одна несвязанная строка :259) | PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md |
| Ф-16 | `dod_gate` освобождает воркера, все правки которого — `.md/.json/.jsonl` (dod_gate.py, докстринг «Doc-only exemption»): критик/скаут/дизайнер, записавшие один `.md`, не упрутся в требование зелёного прогона | dod_gate.py |
| Ф-17 | Экзамен за правку роли: critic п. 10 (critic.md:58–63, `PROCESS/CRITIC_EXAM.md`), scout п. 6 (scout.md:55–59, golden set). builder и designer — «NO set, by design» (SIBLING_MAP.md:41–64, ось 2). D-0037 (DECISIONS.md:49) откладывает экзамены; долг — пачка `forge/3` (статус «ожидает», batch-3-exam-debts.md:3), узлы F3-1 (критик, :24) и F3-2 (скаут, :25) | DECISIONS.md, batch-3 |
| Ф-18 | Сетка механизмов: `.claude/agents/`, `PROCESS/`, `.claude/settings.json`, `tools/agent_budget.py`, `tools/dispatch_manifest.py`, `tools/transcripts.py` в `MECHANISM_PREFIXES` (mechanism_gate.py:183–237); тест требует, чтобы каждый хук из settings.json был в этой сетке (комментарий :196–202). F5-6 той же пачки владеет `tools/mechanism_gate.py` (batch-5:29) | mechanism_gate.py |
| Ф-19 | Скрипт-черновик Lead: читает файл сам (`open`, строка 13) — мимо `transcripts` (ось 14: «a new reader of agent-*.jsonl imports transcripts»); из вводов tool_use берёт САМЫЙ ДЛИННЫЙ текст, а не последний (:36–39) — поздний короткий SubagentHandback проиграет раннему длинному тексту; перезаписывает выходной файл без проверки (:44) — затрёт файл, который воркер уже написал; пустой результат → код 2 без записи (:40–42) | scratchpad `extract_handback.py` |
| Ф-20 | Консоль: новый скрипт вне цепи хуков зовёт `streams.utf8_stdio()` (tools/streams.py:31; SIBLING_MAP ось 15); звено цепи (хук) держит свою копию и `streams` не импортирует | SIBLING_MAP.md:306–317 |

## §3. Механизм

### 3.1 М-а: Write на один путь и хук `handoff_gate`

**Диспатч.** Путь отчёта — абсолютный путь `.md` на строке `handoff:` (или на строках под ней до пустой строки),
никогда на `owns:` (Ф-7). Папка по роли — таблица данных `HANDOFF_DIRS` (FR-13: закрытое разнообразие в данных):

| роль (`agentType`) | папка (последние сегменты пути) |
|---|---|
| critic | `docs/tasks/specs/reviews` |
| scout | `docs/tasks/specs/reports` или `docs/tasks/handoffs` — **F-3** |
| designer | `docs/tasks/specs` (только прямой ребёнок, не `reviews/`, не `reports/`) |

builder в таблице нет: хук его не трогает; его файл отчёта — `docs/tasks/handoffs/<t>-….md` по строке `handoff:`.

**Читатель.** `dispatch_manifest.handoff_paths(cut) -> list[str]` — абсолютные пути секций `handoff` по той же петле,
что `given_paths` (:483–503): строка заголовка от `tail_start`, строки под ней до первой пустой, процитированные
строки не читаются, `(new)` снимается `split_new_marker`, кандидаты — `path_candidates(text, None)`, из них
остаются только абсолютные. Петлю не копировать: `given_paths` и `handoff_paths` — две обёртки над одной
`_section_paths(cut, item, top_entries)` (ось 13: «a new reader of a dispatch's sections reads the cut, never a private
line scan»; вопрос DUPLICATION критика). `HANDOFF_DIRS` живёт там же (чистые данные; `agent_budget` и хук берут её
оттуда — малый выбор, §7 конец).

**Хук** `tools/handoff_gate.py` (дом — **F-2**), PreToolUse, matcher `Edit|Write` (рядом с `claim_control_gate`,
settings.json:53). `decide(payload) -> (exit_code, message)`; по порядку:

1. `tool_name` не `Write` и не `Edit` → 0.
2. Нет `agent_id` (не строка / пусто) → 0: главная сессия пишет свободно.
3. Файл воркера: `transcripts.subagents_dir_of(transcript_path) / transcripts.agent_file_name(agent_id)` (та же
   композиция, что agent_budget.py:100–110; их слияние в одну функцию `transcripts` — очередь, §7 аналоги).
   `kind = transcripts.agent_type(файл)`.
4. `kind == "builder"` или `kind` известен и не в `HANDOFF_DIRS` (Explore, Plan, general-purpose, judge) → 0.
5. `kind is None` → **F-6**.
6. `kind` в `HANDOFF_DIRS`: `text = transcripts.first_user_text(файл)`; `None` или `OSError` → отказ (R-нечитаемо).
   `cut = dispatch_manifest.section_cut(text)`; `cut.degraded` → отказ (R-нечитаемо).
7. `cands` = пути из `handoff_paths(cut)`, которые оканчиваются на `.md` (без учёта регистра) и чей родитель — ровно
   папка роли (сравнение по последним сегментам, `os.path.normcase`, без привязки к `cwd`: воркер в worktree и путь в
   основном дереве равноправны). Пути секции вне папки роли в счёт не идут (это упоминания, не цель).
   `len(cands) == 0` → отказ (R-нет-пути); `> 1` → отказ (R-два-пути, оба названы).
8. `target = realpath(join(cwd, tool_input.file_path))`, `normcase`; равно `normcase(realpath(cands[0]))` → 0,
   иначе → отказ (R-не-тот-путь).

**Отказ** (exit 2, stderr; FR-1/P15: что не так, чего ждут, дверь), английский текст одной формы:
`HANDOFF GATE: this <kind> worker may write only the one report file its dispatch names on the handoff: line, inside
<dir>. Refused: <path> -- <reason>. Expected: <expected>. Door: put your whole report into your final message instead;
the coordinator extracts it (tools/handback_extract.py).` Причины: `no handoff path inside <dir> in the dispatch` /
`the dispatch names <n> handoff paths inside <dir>: <a>, <b>; exactly one is expected` / `not the handoff path
(<expected>)` / `the dispatch text could not be read`.

**`main()`**: stdin с дедлайном (копия по образцу owns_gate.py:1115–1196 — звено цепи держит свои копии, ось 15);
битый JSON / не словарь → 0; исключение внутри `decide` → 2 с причиной `the dispatch text could not be read`, если в
payload есть `agent_id` и `tool_name` ∈ {Write, Edit}, иначе 0. Инвариант: читающая роль никогда не пишет мимо одного
названного пути из-за сбоя кода (сбой — отказ с дверью, не пропуск); главная сессия и builder сбоем хука не
блокируются.

**Живой путь.** Файл хука неактивен, пока не записан в settings.json. Регистрацию, строку `MECHANISM_PREFIXES`
(mechanism_gate.py — им владеет F5-6, Ф-18) и добавление `Write` в строки `tools:` делает Lead при приёмке (CLAUDE.md
правило 2: самоактивирующийся файл кладёт на живой путь Lead) — порядок слияния **F-10**.

**`agent_budget`.** `ALLOWED_DIRS` = нынешние две папки ∪ папки `HANDOFF_DIRS`; `stop_message` велит писать отчёт
«в путь со строки handoff: диспатча, а если его нет — в docs/tasks/handoffs/». Иначе критик на STOP получит от
`agent_budget` совет писать в `handoffs/`, а от `handoff_gate` — отказ (конфликт двух хуков, Ф-13).

### 3.2 М-б: `tools/handback_extract.py`

`python tools/handback_extract.py <transcript> <out.md> [--header TEXT]` (вариант с `--agent <id>` — **F-5**).

- Чтение — только через `transcripts`: `iter_lines`, `parse_line`, `content_blocks`, `is_finished` (ось 14, Ф-19).
- Кандидаты — строки, у которых `message.role == "assistant"`: (а) блок `tool_use` с `name == "SubagentHandback"` и
  непустой строкой `input.message`; (б) непустой текстовый блок, или `message.content` — непустая строка. Итог —
  ПОСЛЕДНИЙ кандидат (а), если он есть; иначе последний (б). Не «самый длинный» (Ф-19).
- Запись: `<header>\n\n` (если дан, `rstrip("\n")`) + `text.strip()` + `\n`, UTF-8, `newline="\n"`.
- stdout — одна строка без тела отчёта: `written <out>: <bytes> bytes, <lines> lines, source=<handback|text>,
  finished=<yes|no>`; `<lines>` считается по правилу F-7 (калибровка 28 (г) берёт число отсюда). Ошибки — stderr.
  Консоль — `streams.utf8_stdio()` после бутстрапа `sys.path` (ось 15).
- Коды: `0` записано, транскрипт завершён (`is_finished`); `1` ошибка вызова (не те аргументы, транскрипта нет или
  не читается, папки выходного файла нет, ошибка записи) — ничего не пишется; `2` финального текста нет (файл 0 байт,
  нет JSON, нет текста ассистента) — ничего не пишется; `3` выходной файл уже есть — не трогается; `4` записано, но в
  хвосте нет SubagentHandback — первой строкой файла идёт `<!-- handback_extract: no SubagentHandback in the
  transcript; this is the worker's last text, not its hand-back -->`.

### 3.3 М-в: правило 25 строк и приёмка по файлу

Текст правила (английский; в critic.md, builder.md, scout.md, designer.md — НА МЕСТЕ нынешних п. 16 / 7 / 9 / 5, без
перенумерации, чтобы якоря проверки 28 (а) остались; `<report>` = verdict / report / digest / draft):

> N. The report is a FILE; the final message is its digest. When the dispatch names an absolute path on its
> `handoff:` line, write your FULL <report> to that one path (the file at `handoff:` is what the coordinator reads at
> acceptance), then end with a final message of at most 25 lines: the path, <role line>, and "needed beyond the
> manifest". Every closing message — a resubmission after a hook block or a question included — repeats the path and
> the digest WHOLE; "see above" is forbidden. When the dispatch names no such path, or the Write is refused (the hook
> says why), the FULL <report> goes into the final message as before — never lost, never shortened.

`<role line>`: critic — строка вердикта и число блокирующих находок; builder — DONE/PARTIAL/NOT DONE по пунктам и
итоговые строки свидетеля; scout — ответ на вопрос в одну-три строки и число негативов с контролем; designer — развилки
по id, по строке на каждую. Определение строки — по F-7, одной фразой в том же пункте.

Попутные правки (каждая — тем же узлом N1):
- critic п. 17: блок ```json — последний элемент ФАЙЛА обзора (проверка — `python tools/critic_verdict_check.py
  <файл>`, Ф-10); без файла — последний элемент сообщения, как сейчас.
- designer п. 4: «don't write to the tree» → «write nothing but the one draft file at `handoff:`»; при варианте F-4 B
  п. 4 не меняется, а М-в для дизайнера действует только через builder-тип.
- scout: `description` (scout.md:3) «Read-only, changes nothing» → «read-only on the repository except its one digest
  file at `handoff:`»; п. 4 (:47–49) — о Bash не трогать, добавить: Write ограничен хуком одним путём.
- `critic-diff-brief.md` «What comes back» (:42–48): всё перечисленное — в файл обзора по `handoff:`, ответ в чате
  ≤ 25 строк; приёмка читает файл и гоняет `critic_verdict_check.py` по файлу.
- `plans/builder-rules.md` п. 11 (:29): файл по `handoff:` — это отчёт п. 11 (потолок 500 слов — по F-8); ответ в
  чате ≤ 25 строк.
- `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` проверка 28: (а) якоря — те же пять пунктов с новым текстом; новый пункт
  (г) — детектор, §4.
- judge.md — не трогается (вердикт по ролям — §5 E-25).

## §4. Четыре вопроса на механизм

### М-а (Write на один путь + `handoff_gate`)

(a) Цена. Диспетчер: одна строка `handoff:` с абсолютным путём. Хук: на каждый Write/Edit воркера — чтение meta
(~300 Б); для critic/scout/designer — ещё первая строка транскрипта и один разрез (миллисекунды; число вызовов Write
у читающей роли — один-два на запуск). Воркер: один Write. Платит: харнесс-время воркера, не Fable.

(b) Оси:
- ось 1: покрыто — роли (N1), CLAUDE.md правила 1–3 носитель отчёта не называют (прочитано; новая строка R11 —
  часть Lead, §8).
- ось 2: покрыто — D-0037: critic и scout — долг F3-1/F3-2; builder и designer — «no set, by design»; judge не меняется.
- ось 3: н/п — пакет не трогается.
- ось 4: н/п — пакет и FR не трогаются; бэклог заморожен, находки — в кучки.
- ось 5: н/п — стадии пакета не затронуты.
- ось 6: н/п — инструменты замера пакета не затронуты.
- ось 7: н/п — тесты новых файлов не зависят от окружения прогона (только tmp_path).
- ось 8: н/п — история на диске не затронута.
- ось 9: н/п — «это тестовый файл?» не используется.
- ось 10: н/п — хук не читает верх git; путь сравнивается по сегментам, не от корня репозитория.
- ось 11: в очереди — обход Write критиком через Bash (у критика Bash есть) хук не ловит; распознаватели команд — не
  его дело (остаток назван, §5 E-9).
- ось 12: н/п — носители плана не меняются.
- ось 13: покрыто — `handoff_paths` читает разрез, общая петля с `given_paths`; строка в таблицу оси — Lead (§8).
- ось 14: покрыто — хук читает `agent_type`, `first_user_text` из `transcripts`; строка потребителя в оси — Lead.
- ось 15: покрыто — хук держит свою копию настройки потоков (звено цепи), `streams` не импортирует.
- ось 16: н/п — пакет не затронут.

(c) Детектор: `tools/test_handoff_gate.py` (§6) и калибровочная проверка 28 (г) — запись файла по `handoff:` в
транскрипте воркера против записи в транскрипте Lead; вне неё — `hook_liveness_probe` (кейс для нового хука —
в очереди, §7 аналоги).

(d) Что не даёт пропустить: settings.json PreToolUse `Edit|Write` → `handoff_gate.py` на каждом Write/Edit; строка
`tools:` роли — харнесс; отказ — exit 2.

### М-б (`handback_extract.py`)

(a) Цена: Lead — один вызов Bash на возврат без файла; ноль выходных токенов Fable (по находке ~30K на три дайджеста).

(b) Оси:
- ось 1: н/п — политика не меняется (правило «как Lead извлекает» — часть М-в).
- ось 2: н/п — экзамены не затронуты.
- ось 3: н/п — вне пакета.
- ось 4: н/п — вне пакета.
- ось 5: н/п.
- ось 6: н/п — меряет не пакет, а транскрипты.
- ось 7: н/п — тест на tmp_path.
- ось 8: н/п.
- ось 9: н/п.
- ось 10: н/п.
- ось 11: н/п — команд не разбирает.
- ось 12: н/п.
- ось 13: н/п — диспатч не читает.
- ось 14: покрыто — новый CLI-читатель `agent-*.jsonl` через `transcripts`; строка в «Consumers» оси — Lead.
- ось 15: покрыто — `streams.utf8_stdio()` (скрипт вне цепи).
- ось 16: н/п.

(c) Детектор: `tools/test_handback_extract.py` (§6); проверка 28 (г) считает возвраты, извлечённые кодом, и
переписанные руками.

(d) Что не даёт пропустить: только дисциплина Lead — явная строка: «on discipline alone; detector — calibration check
28 (d)». Перевод в код — после утечки по логу (правило 10 (d)).

### М-в (25 строк, файл — отчёт, приёмка читает файл)

(a) Цена: воркер пишет файл и 25 строк (вместо полного текста в чате — нетто около нуля); Lead на приёмке — один Read
файла (вход, как и сейчас; можно читать часть). Экономия: полный отчёт не попадает в контекст Lead с возвратом
(оценка, не замер); переписывание — ноль.

(b) Оси:
- ось 1: покрыто — пять файлов ролей по оси 1 получают вердикт (§5 E-25), проверка 28 (в) — ровно об этом.
- ось 2: покрыто — экзамен: D-0037, долг F3-1/F3-2 (§5 E-26).
- ось 3: н/п.
- ось 4: н/п — FR не трогаются.
- ось 5: н/п.
- ось 6: н/п.
- ось 7: н/п.
- ось 8: н/п.
- ось 9: н/п.
- ось 10: н/п.
- ось 11: н/п.
- ось 12: в очереди — `plans/builder-rules.md` п. 11 правится (N1), PROJECT.md «Отчёт агента координатору —
  выжимка» — аналог для Lead (§7 аналоги).
- ось 13: н/п — грамматика заголовков не меняется.
- ось 14: н/п.
- ось 15: н/п.
- ось 16: н/п.

(c) Детектор: проверка 28 (а) — якоря (их держит новый `tools/test_handoff_rule_anchors.py`), (г) — счётчики:
возвраты длиннее 25 строк (число строк печатает `handback_extract.py`), отчёты, записанные Lead вместо воркера.
Счётчик живого доказательства пачки («переписанных отчётов в «Ход» conductor/2 = 0», batch-5:51) — это (г) на первом окне.

(d) Что не даёт пропустить: файл роли грузится харнессом в каждый запуск роли; отказ хука называет дверь; длина
ответа — на дисциплине, детектор — проверка 28 (г).

**Текст проверки 28 (г)** (англ., вписывает N1):
> (d) Hand-back carrier (F5-1, t-744). For every `accepted` of a critic/scout/designer/builder task in the window whose
> dispatch named a `handoff:` path: who wrote the file — a Write/Edit `tool_use` with that `file_path` in the worker's
> `subagents/agent-<id>.jsonl` (its `worker_ref`) = the worker; a Write of it in the main session transcript = RETYPED by
> the Lead (a leak, target 0); a `tools/handback_extract.py` Bash call in the main transcript = extracted by code
> (legal, counted). Also count: journal notes saying "transcribed by hand"/"retyped"; hand-back messages over 25 lines
> (`handback_extract.py` prints the count); read-role dispatches with no `handoff:` path. The first window records the
> baseline.

## §5. Края

Каждый край — поведение и инвариант, который оно защищает.

**Временные (до / после).**
- E-1. До изменения: путь `handoff:` в диспатчах — проза («report ≤ 500 words …»), абсолютного пути там нет. После:
  читающая роль без пути в своей папке получает отказ на любой Write и отдаёт полный отчёт в чате, как сегодня; Lead
  извлекает его М-б. Инвариант: отчёт не теряется ни в одном мире; читающая роль не пишет мимо названного пути.
- E-2. Между слиянием текста ролей и регистрацией хука (F-10): текст правила уже велит писать файл, а `Write` в
  `tools:` ещё нет — харнесс откажет, и по тому же правилу отчёт идёт в чат. Инвариант: scout и designer не получают
  Write без хука (у них нет Bash, Ф-8, — Write без хука шире статус-кво).
- E-3. Write воркера отклонён хуком: отказ называет причину, ожидаемый путь и дверь; воркер отдаёт полный отчёт в чат
  (правило М-в). Lead видит отказ в транскрипте; проверка 28 (г) считает такие случаи по строке «no handoff path».
- E-4. Файл написан, ответ в чате пуст: приёмка читает файл по пути из СВОЕГО диспатча (Lead его знает); для критика —
  `critic_verdict_check.py <файл>` = 0 обязателен. Пустой ответ — нарушение правила, считается 28 (б); работа не
  теряется. Инвариант: приёмка не опирается на чат.
- E-5. Транскрипт 0 байт И файла нет — остаточная утечка. Замер: файлов `subagents/agent-*.jsonl` с 0 байт — 0 из
  158 (Ф-1); 0 байт бывает у `.output`. Поведение: `handback_extract.py` на файле из `subagents/` → код 2; Lead
  перезапускает воркера (`delegated` с `replaces_worker:`); детектор — 28 (б) «a sidechain … whose final message is
  empty» плюс код 2 на приёмке. Инвариант: потеря видна, а не тиха.

**Один путь (М-а).**
- E-6. Нет `agent_id` → пропуск (главная сессия). Инвариант: Lead не блокируется.
- E-7. Два и больше пути `.md` в папке роли на `handoff:` → отказ, оба названы. Инвариант: «один путь» не становится
  «любой из названных».
- E-8. Путь в `handoff:` вне папки роли (напр. `tools/x.py`) → в счёт не идёт; если других нет — отказ «no handoff
  path». Инвариант: читающая роль не пишет код и конфиги, даже если диспетчер ошибся.
- E-9. Критик пишет через Bash (`>`, `Set-Content`) — хук не видит. Остаток статус-кво (Bash у критика есть сегодня);
  у scout и designer Bash нет. Назван, не закрыт (ось 11 в очереди).
- E-10. Путь записан с другим регистром, через `..`, относительный от `cwd` → `realpath` + `normcase` сводят к одному.
  Путь-заготовка `<t>` — не путь (`_PLACEHOLDER_RE`, `path_candidates`) → «no handoff path».
- E-11. Строка `handoff:` внутри ограды или цитаты → не читается (одна полярность оси 13). Незакрытая ограда — проза.
- E-12. Разрез деградировал (текст > 2 000 000 символов, md_regions.py:172) или первая строка транскрипта не читается →
  отказ с дверью. Инвариант: неизвестное не пропуск (FR-59).
- E-13. `kind is None` (meta нет или битая) → F-6.
- E-14. builder, Explore, Plan, judge, general-purpose → пропуск: их возможности задаёт `tools:`; builder пишет свои
  owns и свой файл в `handoffs/` без ограничения (F5-1 не вводит ограничение builder по owns — не-цель).
- E-15. Воркер на STOP бюджета: `agent_budget` пропускает запись в папки `HANDOFF_DIRS` (§3.1), `handoff_gate` — только
  в свой путь; оба пропускают названный путь. Инвариант: совет одного хука не противоречит отказу другого.
- E-16. Edit своего файла отчёта (дописать после отказа dod_gate, переписать при повторе) → разрешён тем же сравнением.

**Извлечение (М-б).**
- E-17. Транскрипт 0 байт → код 2, файла нет. Инвариант: пустой отчёт не выдаётся за отчёт.
- E-18. Нет текста ассистента (только user, tool_result, строки не-JSON) → код 2.
- E-19. Обрезанная последняя строка (воркер жив или убит) → `parse_line` = None, строка пропущена, берётся последний
  целый кандидат; `is_finished` ложно → код 4 и строка-метка в файле. Инвариант: промежуточный текст не выдаётся за
  возврат.
- E-20. Недекодируемый байт → `iter_lines` заменяет на U+FFFD; запись идёт, код 0/4. Инвариант: один битый байт не
  теряет отчёт.
- E-21. Выходной файл уже есть (воркер успел написать) → код 3, байты не тронуты. Инвариант: код не затирает файл воркера.
- E-22. Два SubagentHandback (повтор после блока хука) → последний, даже если короче (Ф-19).
- E-23. Папки выходного файла нет → код 1, ничего не создаётся.

**Правило 25 строк (М-в).**
- E-24. Что считается строкой — F-7. Пустые строки и строки ограды считаются. Блок json критика — в файле, в 25
  строк не входит; без файла (E-1, E-3) — полный вердикт в чате, правило 25 строк не действует.
- E-25. Вердикт по пяти файлам ролей (один артефакт): **critic** — применяется (п. 16, 17; путь в
  `docs/tasks/specs/reviews`); **builder** — применяется (п. 7; `tools:` не меняется — Write уже есть); **scout** —
  применяется (п. 9, описание, п. 4; при F-1 B — только текст «отчёт в чате», без Write); **designer** — применяется
  при F-4 A (п. 4, 5), при F-4 B — не применяется (дизайнер запускается builder-типом и подчиняется builder п. 7);
  **judge** — не применяется: форма ответа закреплена дословно (строка `EQUIVALENT|WORSE` или строгий JSON,
  judge.md:29–41, 68–72), от неё зависит калибровка судьи (правило 13 CLAUDE.md); отчёта-файла у судьи нет.
- E-26. Экзамен (D-0037): правка critic.md и scout.md требует экзамена (Ф-17) — долг наследуется, нового экзамена нет.
  Где записано: строка коммита N1 `exam: deferred by D-0037; debt — forge/3 F3-1 (critic), F3-2 (scout)`. Пачка 3
  «ожидает» и не заморожена; экзамен, когда пройдёт, проверит файл роли в его тогдашнем виде. builder и designer —
  «no set, by design» (ось 2): долга нет. Ключи экзамена про новое поведение («отчёт — файл по handoff:») — аналог для
  пачки 3 (§7 аналоги).

## §6. Тесты и мутации

Каждая мутация — на копии файла, байтовый откат с sha (гигиена п. 7), убивается ОДНИМ названным тестовым файлом.

**N2 — `tools/test_handback_extract.py`** (транскрипты-фикстуры пишутся в tmp_path):

| тест | что | мутация → убивает |
|---|---|---|
| test_empty_transcript | 0 байт → код 2, файла нет | `return 2` → `return 0` |
| test_no_assistant_text | только user/tool_result/не-JSON → код 2 | фильтр роли пропускает `user` |
| test_handback_preferred | в одном сообщении текст «Handing back now.» + SubagentHandback(REPORT) → REPORT, source=handback | предпочесть последний текст |
| test_last_handback_wins | два SubagentHandback, второй короче → второй | выбор «самый длинный» (Ф-19) |
| test_content_string | `message.content` — строка → взята | ветка строки удалена |
| test_truncated_last_line | последняя строка обрезана посреди JSON с более поздним возвратом → предыдущий кандидат, код 4, метка первой строкой | код 4 → 0 |
| test_non_utf8_byte | байт `\xff` в строке текста → U+FFFD в файле, код 0 | `iter_lines` заменён на строгий `open(encoding="utf-8")` |
| test_existing_output_kept | файл есть → код 3, sha не изменился | проверка существования удалена |
| test_missing_out_dir | папки нет → код 1, ничего не создано | `mkdir(parents=True)` перед записью |
| test_missing_transcript | транскрипта нет → код 1 | — (граница вызова; мутация: `FileNotFoundError` → код 2) |
| test_stdout_has_no_body | уникальный маркер тела не попадает в stdout; строка `written …` с числом строк | печать головы тела (как в черновике) |

**N3 — `tools/test_handoff_gate.py`** (meta + транскрипт воркера — фикстуры в tmp_path, `transcript_path` указывает туда):

| тест | что | мутация → убивает |
|---|---|---|
| test_main_thread_passes | нет `agent_id` → 0 | `agent_id` None считать воркером |
| test_builder_passes | builder пишет `tools/x.py` → 0 | builder в `HANDOFF_DIRS` |
| test_critic_own_path | critic: Write и Edit в свой путь → 0; относительный и с `..` → 0 | сравнение без `realpath` |
| test_critic_other_path | critic пишет другой файл → 2, сообщение несёт ожидаемый путь и `Door:` | сравнение «в папке роли», а не «тот путь» |
| test_no_handoff_path | проза в `handoff:` → 2 «no handoff path» | пустой список → 0 |
| test_two_paths | два пути в папке → 2, оба названы | взять первый |
| test_path_outside_dir | `handoff:` называет `tools/x.py` → 2 | проверка папки удалена |
| test_designer_subfolder | designer: путь в `docs/tasks/specs/reviews/` → 2 | «под папкой» вместо «прямой ребёнок» |
| test_quoted_handoff | строка в ограде → 2 | читать процитированные строки |
| test_placeholder | `<t>` в пути → 2 | — (держит `path_candidates`; мутация `_PLACEHOLDER_RE` в dispatch_manifest убивается test_dispatch_manifest.py) |
| test_unreadable_dispatch | первая строка не читается / разрез деградировал → 2 | `None` → 0 |
| test_unknown_kind | meta нет → по решению F-6 | обратное направление |
| test_other_tools | `Read`, `Bash` → 0 | — |
| test_main_exception | исключение в `decide` с `agent_id` и Write → 2; без `agent_id` → 0 | `except: return 0` |

**N3 — `tools/test_dispatch_manifest.py`** (добавить): `handoff_paths` — путь на строке заголовка, путь строкой ниже,
`(new)` снят, процитированная строка не читается, относительный путь отброшен, `given_paths` после рефакторинга
отдаёт то же, что до (закрепление на двух существующих диспатчах-фикстурах). Мутация: убрать `cut.quoted[idx]` →
убивает этот файл.

**N3 — `tools/test_agent_budget.py`** (добавить): `stop_allows("Write", {"file_path": "<cwd>/docs/tasks/specs/reviews/x.md"})`
→ True; `stop_message` несёт `handoff:`. Мутация: `ALLOWED_DIRS` без `HANDOFF_DIRS` → убивает этот файл.

**N1 — `tools/test_handoff_rule_anchors.py`** (doc-witness, CLAUDE.md правило 11: ключи дословно отсюда, тест в
коммите, отрицательный контроль внутри): ключ K1 = ``the file at `handoff:` `` и K2 = `at most 25 lines` есть в
critic.md, builder.md, scout.md, designer.md (designer — только при F-4 A) и в critic-diff-brief.md; K3 = `не длиннее 25
строк` — в plans/builder-rules.md; K4 = `(d) Hand-back carrier` — в PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md; K1 НЕТ в
judge.md. Отрицательный контроль: `missing_keys("no keys here", [K1]) == [K1]`.

## §7. Развилки

Сначала рекомендация, затем цена. Ничего не решено.

- **F-1. Какие читающие роли получают Write.**
  - Рекомендация: A — critic, scout, designer (с F-4 A), все за хуком. Утечка находки была у скаутов (3 из 4); выигрыш
    в контексте Lead — у всех.
  - Цена: scout теряет read-only «конфигурацией» (scout.md:47–49, внешнее ревью P0) — защиту несёт код хука.
  - Альтернатива B: Write только critic (у него и так Bash) и designer; scout остаётся без Write, его дайджест
    достаёт М-б из `subagents/` (158 из 158 непусты, Ф-1). Дешевле и строже для scout; Lead платит один Bash на скаута.
- **F-2. Дом хука одного пути.**
  - Рекомендация: A — новый `tools/handoff_gate.py` на `Edit|Write`: одна ответственность, свой тест, отказ — exit 2.
  - Цена: +2 файла, строка в settings.json и в `MECHANISM_PREFIXES` (Lead).
  - B: внутри `agent_budget.py` (уже на каждом инструменте, уже знает `agent_id`, :100–110) — но его `main()` любое
    исключение превращает в пропуск (:242–245, «Raises on any failure -- main() turns that into fail-open»): гейт
    унаследует направление ошибки «пропуск».
  - C (бриф): `owns_gate.py` — не годится без слома его инварианта: он на `Task|Agent` в сессии диспетчера
    (settings.json:27, :39) и всегда возвращает 0 (:1095–1102); записи воркера он не видит (Ф-2).
- **F-3. Папка скаута.**
  - Рекомендация: `docs/tasks/specs/reports` — там 102 отчёта скаутов, её называет находка, она уже в
    `agent_budget.ALLOWED_DIRS` (:73).
  - Альтернатива (бриф): `docs/tasks/handoffs` — одна папка с builder; тогда scout и builder делят папку, а отчёты
    скаутов расходятся по двум местам.
- **F-4. Дизайнер — своим типом с Write или прежним обходом.**
  - Рекомендация: A — `designer.md` получает Write (за хуком, путь в `docs/tasks/specs`), Lead запускает `designer`, а
    не builder с `model: opus`. Плюсы: не занимает слот писателя (Ф-7), не требует полного манифеста builder
    (Ф-6; этот диспатч шёл с `manifest-skip`), долга экзамена нет (ось 2, «no set, by design»).
  - Цена: правка п. 4 и 5 designer.md; дизайнер с правом записи одного файла.
  - B: обход остаётся; designer.md не трогается; М-в для дизайнера — через builder п. 7.
- **F-5. Вход `handback_extract.py`.**
  - Рекомендация: B — путь ИЛИ `--agent <id>` (через `transcripts.find_agent_transcript`, :63–74). У 73 из 158 воркеров
    `.output` пуст, а файл в `subagents/` полон (Ф-1): по `.output` инструмент вернёт код 2 там, где отчёт есть.
  - Цена: ~10 строк и два теста (id не найден / неоднозначен → код 1).
  - A (бриф): только путь; Lead сам собирает путь `~/.claude/projects/<slug>/<session>/subagents/agent-<id>.jsonl`.
- **F-6. Хук при неизвестной роли (meta нет или битая).**
  - Рекомендация: B — как `transcripts.is_writer` (D-0040): нет пути в `owns:` в тексте диспатча → считать читающей и
    проверять; есть путь → пропуск; текст не читается → отказ с дверью (FR-59).
  - Цена: builder без пути в owns и без meta получит отказ (оба редки: meta 627 из 627 в t-672; builder без owns-пути —
    36 из 321, DECISIONS.md:52) — дверь «отчёт в чат» к коду не подходит, такой builder встанет.
  - A: пропуск — builder не блокируется никогда; читающая роль без meta пишет без ограничений (остаток назван).
- **F-7. Что считается строкой в «≤ 25 строк».**
  - Рекомендация: B — каждая строка по `\n`, пустые и строки ограды тоже; строка длиннее 200 символов считается как
    `ceil(len/200)`. Без этого правило обходится одной длинной строкой.
  - A: только `\n`-строки. Проще, обходится.
- **F-8. Чем становится п. 11 builder-rules (≤ 500 слов).**
  - Рекомендация: A — файл по `handoff:` и есть отчёт п. 11: ≤ 500 слов прозы, дословные выводы прогонов (свидетель) в
    блоках кода в счёт не идут; ответ в чате ≤ 25 строк.
  - B: 500 слов на всё, включая выводы; длинный свидетель — вторым файлом рядом.
- **F-9. Проверка на стороне диспатча: читающая роль без пути в `handoff:`.**
  - Рекомендация: A — сейчас без кода: хук откажет, отчёт придёт в чат (E-1), 28 (г) посчитает такие диспатчи;
    код — после утечки. `dispatch_gate.py` в этой пачке уже держат F5-8 и F5-10 (batch-5:31, :33).
  - B: WARN в `dispatch_gate.py` сейчас — нужна строка `очередь:` с F5-8/F5-10.
- **F-10. Порядок слияния против приказа «роли первыми».**
  - Рекомендация: B — N1 пишет только текст правил и НЕ трогает строки `tools:`; Lead добавляет `Write` в
    `tools:` critic/scout/designer тем же коммитом, где регистрирует хук (settings.json + `MECHANISM_PREFIXES`). N1
    сливается первым (мир E-2 закрыт текстом правила), N2 — когда угодно, N3 — со строками `tools:`.
  - Цена: три правки в одно слово у Lead при интеграции.
  - A: N1 меняет и `tools:`; тогда N1 и N3 сливаются одним коммитом, «роли первыми» — только порядок запуска.

Малые выборы, закрытые дизайнером: `HANDOFF_DIRS` — в `dispatch_manifest.py` (чистые данные, оба хука её читают);
Edit своего файла разрешён (E-16); только `.md`; «прямой ребёнок папки» для всех ролей; сравнение папки по
сегментам, не от `cwd`; блок json критика — в файле (Ф-10); коды выхода М-б 0–4; итог М-б — последний возврат, не
длиннейший; М-б не перезаписывает; stdout М-б без тела; текст отказа хука — английский, одна форма.

**Аналоги, замеченные и не расширенные:**
- `agent_budget.py:179–189` `_path_allowed` считает папки от `cwd` хука: builder в worktree, пишущий отчёт по
  абсолютному пути основного дерева, на STOP получит отказ (оценка, не проверено — `cwd` воркера в worktree не мерил).
- Композиция «`agent_id` → файл воркера» будет в двух местах (agent_budget.py:100–110 и хук) — свести в одну функцию
  `transcripts` (ось 14); очередь.
- `hook_liveness_probe.py` «for ALL 13 hook gates» (:1) — новому хуку нужен кейс; очередь.
- `dod_gate.py:119–126` BLOCK_MESSAGE «a COMPLETE final report all over again» — при файле по `handoff:` должно звучать
  «the report file and the digest»; якорь проверки 28 (а). Владелец — не этот узел (dod_gate — звено цепи).
- PROJECT.md «Отчёт агента координатору — выжимка (builder-rules п. 11: ≤ 500 слов); длинное — в файл» — строку
  про 25 строк вписывает Lead.
- CLAUDE.md R11: строка «читающая роль получает путь отчёта на `handoff:`, никогда на `owns:`» (Ф-7) — Lead.
- `docs/SIBLING_MAP.md` оси 13 и 14 — строки нового читателя и потребителей — Lead.
- Ключи экзаменов F3-1/F3-2 (пачка 3) не проверяют «отчёт — файл по handoff:» — находка для пачки 3.
- Память `subagent-handbacks-write-their-own-file.md` («transcript files are often 0 bytes») неточна: пусты `.output`,
  не транскрипты (Ф-1) — для Lead.
- Находка-источник (её «скаут не может сам записать файл», «транскрипт пустой») — то же расхождение.

## §8. Диспатчи билдеру

Три узла, owns не пересекаются; параллельно не более трёх писателей (D-0040). Порядок запуска: N1 первым, N2 сразу
следом, N3 вместе с N2. Порядок слияния — по F-10 (рекомендация: N1, N2 в любой момент; N3 — коммитом Lead со строками
`tools:` и регистрацией). Манифест — по рекомендованным F-2 A, F-3 reports, F-4 A, F-5 B; при другом решении Lead
вычёркивает: F-2 B — `handoff_gate.py` и его тест из N3, `agent_budget.py` становится домом гейта; F-4 B — designer.md
из N1; F-10 A — в N1 добавляется «и строки `tools:`». Часть Lead при интеграции: settings.json, строка
`MECHANISM_PREFIXES`, строки `tools:` (F-10 B), CLAUDE.md R11, SIBLING_MAP оси 13/14, коммит механизма с осевым
блоком §4 и строкой `tier:`.

### N1 — текст правил (роли, бриф критика, builder-rules, проверка 28)

given: D:/ws1/yml-text-factory\docs\tasks\specs\t-744-f5-1-handback-carrier.md (§3.3, §4 М-в and the check 28 (d) text, §5 E-1…E-5, E-24…E-26, §6 N1, §7 decisions as closed by the Lead), D:/ws1/yml-text-factory\.claude\agents\critic.md, D:/ws1/yml-text-factory\.claude\agents\builder.md, D:/ws1/yml-text-factory\.claude\agents\scout.md, D:/ws1/yml-text-factory\.claude\agents\designer.md, D:/ws1/yml-text-factory\.claude\agents\judge.md (read only), D:/ws1/yml-text-factory\docs\tasks\critic-diff-brief.md, D:/ws1/yml-text-factory\plans\builder-rules.md, D:/ws1/yml-text-factory\PROCESS\WEEKLY_CALIBRATION_PROTOCOL.md (check 28, lines 821-845), D:/ws1/yml-text-factory\DECISIONS.md (D-0037, line 49)
owns:
D:/ws1/yml-text-factory\.claude\agents\critic.md
D:/ws1/yml-text-factory\.claude\agents\builder.md
D:/ws1/yml-text-factory\.claude\agents\scout.md
D:/ws1/yml-text-factory\.claude\agents\designer.md
D:/ws1/yml-text-factory\docs\tasks\critic-diff-brief.md
D:/ws1/yml-text-factory\plans\builder-rules.md
D:/ws1/yml-text-factory\PROCESS\WEEKLY_CALIBRATION_PROTOCOL.md
D:/ws1/yml-text-factory\tools\test_handoff_rule_anchors.py (new)
non-goals: no edit of the `tools:` frontmatter lines (F-10 B: the Lead flips them with the hook); no edit of judge.md; no renumbering of role rules (check 28 (a) anchors keep their numbers); no edit of CLAUDE.md, PROJECT.md, DECISIONS.md, SIBLING_MAP.md, dod_gate.py, any hook or settings.json; no exam run (D-0037); no edit of plans/piles/forge/batch-3-exam-debts.md.
handoff: the report file D:/ws1/yml-text-factory\docs\tasks\handoffs\<task-id>-f5-1-n1.md (the Lead puts the task id in before sending) with the per-file diff summary, the anchors test output verbatim, the negative control and "needed beyond the manifest"; the chat answer at most 25 lines with the path and the witness's closing line.
edges: §5 E-1 and E-2 (the fallback sentence of the rule covers the world before the hook: no path or a refused Write -> the full report in chat), E-4 (acceptance reads the file; critic: `critic_verdict_check.py` on the file), E-24 (the line definition per F-7 as one sentence in each rule), E-25 (judge.md untouched: its reply shape is pinned verbatim), E-26 (the commit-message line `exam: deferred by D-0037; debt — forge/3 F3-1 (critic), F3-2 (scout)`); on a gap the builder returns a question, not a choice.
DoD: the rule text of §3.3 sits in place of critic rule 16 (and rule 17 moved to the file), builder rule 7, scout rule 9 (plus the description and rule 4 sentence), designer rules 4-5; critic-diff-brief «What comes back» and builder-rules p. 11 say file + at most 25 lines; check 28 carries (d) verbatim from §4; verification `python -m pytest tools/test_handoff_rule_anchors.py -q` green including its negative-control test, and `git diff --stat -- .claude/agents/judge.md` prints nothing.

### N2 — `tools/handback_extract.py` и его тест

given: D:/ws1/yml-text-factory\docs\tasks\specs\t-744-f5-1-handback-carrier.md (§3.2, §5 E-5, E-17…E-23, §6 N2, §7 F-5 and F-7 as closed by the Lead), C:\Users\DEV1~1\AppData\Local\Temp\claude\D--ws-yml-text-factory\a297a98c-c557-42eb-a591-3084fdd0a182\scratchpad\extract_handback.py (the seed; its three defects are §2 Ф-19), D:/ws1/yml-text-factory\tools\transcripts.py (iter_lines, parse_line, content_blocks, is_finished, find_agent_transcript), D:/ws1/yml-text-factory\tools\streams.py (utf8_stdio), D:/ws1/yml-text-factory\tools\test_transcripts.py (the fixture style), D:/ws1/yml-text-factory\docs\SIBLING_MAP.md (axes 14 and 15)
owns:
D:/ws1/yml-text-factory\tools\handback_extract.py (new)
D:/ws1/yml-text-factory\tools\test_handback_extract.py (new)
non-goals: no edit of tools/transcripts.py or any hook; no own JSONL splitter or file reader (axis 14); no printing of the report body; no overwrite of an existing output; no edit of the seed in the scratchpad.
handoff: the report file D:/ws1/yml-text-factory\docs\tasks\handoffs\<task-id>-f5-1-n2.md (the Lead puts the task id in) with the mutation table (each mutation of §6 N2, the killing test, the verbatim result, the restored sha), the DoD output verbatim and "needed beyond the manifest"; the chat answer at most 25 lines.
edges: §5 E-5 and E-17…E-23 with the exit codes of §3.2 (0 written and finished, 1 call error with nothing written, 2 no final text with nothing written, 3 output exists and untouched, 4 written with the unfinished marker line); the last SubagentHandback wins over a longer earlier text; F-5 as closed by the Lead (an unknown or ambiguous `--agent` id -> code 1).
DoD: every test of §6 N2 green and every mutation killed by test_handback_extract.py; a live run on a transcript whose `.output` was 0 bytes writes the report: `python tools/handback_extract.py C:\Users\dev1\.claude\projects\D--ws-yml-text-factory\a297a98c-c557-42eb-a591-3084fdd0a182\subagents\agent-ab6233f5fbed2af68.jsonl C:\Users\DEV1~1\AppData\Local\Temp\claude\D--ws-yml-text-factory\a297a98c-c557-42eb-a591-3084fdd0a182\scratchpad\n2-live.md` prints `written … source=handback, finished=yes` with exit 0; verification `python -m pytest tools/test_handback_extract.py -q` and `python tools/dup_ratchet.py --check`.

### N3 — хук `handoff_gate`, читатель `handoff_paths`, папки `agent_budget`

given: D:/ws1/yml-text-factory\docs\tasks\specs\t-744-f5-1-handback-carrier.md (§3.1, §4 М-а, §5 E-6…E-16, §6 N3, §7 F-2, F-3, F-6 as closed by the Lead), D:/ws1/yml-text-factory\tools\dispatch_manifest.py (section_cut 240-291, given_paths 483-503, path_candidates 441-480), D:/ws1/yml-text-factory\tools\transcripts.py (agent_file_name, subagents_dir_of, first_user_text, agent_type), D:/ws1/yml-text-factory\tools\agent_budget.py (resolve_transcript 100-110, ALLOWED_DIRS 73, _path_allowed 179-189, stop_message 205-210), D:/ws1/yml-text-factory\tools\owns_gate.py (the stdin-deadline main 1115-1232 as the pattern of a chain link), D:/ws1/yml-text-factory\tools\test_dispatch_manifest.py, D:/ws1/yml-text-factory\tools\test_agent_budget.py, D:/ws1/yml-text-factory\.claude\settings.json (read only), D:/ws1/yml-text-factory\docs\SIBLING_MAP.md (axes 13, 14, 15)
owns:
D:/ws1/yml-text-factory\tools\handoff_gate.py (new)
D:/ws1/yml-text-factory\tools\test_handoff_gate.py (new)
D:/ws1/yml-text-factory\tools\dispatch_manifest.py
D:/ws1/yml-text-factory\tools\test_dispatch_manifest.py
D:/ws1/yml-text-factory\tools\agent_budget.py
D:/ws1/yml-text-factory\tools\test_agent_budget.py
non-goals: no edit of .claude/settings.json, tools/mechanism_gate.py (F5-6 owns it; the MECHANISM_PREFIXES line is the Lead's), tools/owns_gate.py, tools/dispatch_gate.py (F5-8, F5-10), tools/transcripts.py, any role file; no restriction of builder writes by owns; no Bash-write detection; the hook is handed over inert — the settings.json snippet goes into the report, not onto the live path (CLAUDE.md rule 2).
handoff: the report file D:/ws1/yml-text-factory\docs\tasks\handoffs\<task-id>-f5-1-n3.md (the Lead puts the task id in) with the settings.json snippet to register, the mutation table (each mutation of §6 N3 with its killing file, verbatim result, restored sha), the DoD output verbatim, the dup ratchet output and "needed beyond the manifest"; the chat answer at most 25 lines.
edges: §5 E-6…E-16 in the order of §3.1 steps 1-8 — the main session and builder never blocked; a gated kind with an unreadable dispatch or a degraded cut refused with the door; two in-dir paths refused with both named; a path outside the kind's folder never counted; the folder compared by trailing segments, not from cwd; an exception in decide with agent_id and Write/Edit -> 2, otherwise 0; F-6 as closed by the Lead; `given_paths` output unchanged after the shared loop.
DoD: every test of §6 N3 green and every mutation killed by its named file; `given_paths` pinned unchanged; verification `python -m pytest tools/test_handoff_gate.py tools/test_dispatch_manifest.py tools/test_agent_budget.py tools/test_dispatch_cut.py tools/test_owns_gate.py -q` and `python tools/dup_ratchet.py --check`.

## §9. След

Прочитано на HEAD `1a3456be` этой сессией.

**Носители (файл: строки).**
- `plans/piles/forge/batch-5-vhodyashchie.md` 1–61 (строка F5-1 :24, порядок :16, доказательство :51, F5-6/8/10 :29/:31/:33).
- `plans/piles/forge/findings/20261013-pustye-transkripty-subagentov.md` 1–24.
- `.claude/agents/critic.md` 1–154, `builder.md` 1–72, `scout.md` 1–83, `designer.md` 1–56, `judge.md` 1–72.
- `docs/tasks/critic-diff-brief.md` 1–48.
- `tools/owns_gate.py` 1–1232 (целиком).
- `tools/dispatch_manifest.py` 1–130, 230–300, 300–440, 440–621.
- `tools/dispatch_gate.py` 1520–1600 (кап и `is_writing_dispatch`); grep `handoff` → :399, :1762 (читателя путей `handoff` нет).
- `tools/transcripts.py` 36–76, 153–250.
- `tools/agent_budget.py` 1–40, 60–80, 95–125, 170–215, 242–266.
- `tools/dod_gate.py` 1–60, 112–128.
- `tools/critic_verdict_check.py` 1–40, 10–16; `tools/streams.py` 1–8, :31; `tools/md_regions.py` :172.
- `tools/mechanism_gate.py` 183–260.
- `.claude/settings.json` целиком (PreToolUse: agent_budget без matcher :22; Task|Agent :27–39; Edit|Write :53–57).
- `docs/SIBLING_MAP.md` заголовки осей 1–16 (:24…:306), тела осей 1–2 (:24–64), 13–16 (:277–331).
- `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` список проверок; 17 (:462–485), 21 (:654–673), 28 (:821–845).
- `DECISIONS.md` :47 (D-0035), :49 (D-0037), :52 (D-0040).
- `plans/builder-rules.md` :12, :29; `plans/piles/forge/batch-3-exam-debts.md` 1–12, :24–25.
- `docs/tasks/specs/t-720-c2-1-2-whole-list.md` 1–14, заголовки, 743–760, 859–940 (форма).
- Скрипт-черновик Lead `extract_handback.py` 1–52.

**Замеры (команда → вывод).**
- М-1: `ls -l <subagents>/agent-<id>.jsonl` и `ls -l <tasks>/<id>.output` для четырёх id → 1186679/0, 1056785/0,
  1015527/0 (link 1), 930221/930221 (link 2) — Ф-1.
- М-2: `ls -l <tasks>/a*.output | wc -l` → 158; `… | awk '$5==0' | wc -l` → 73; `… | awk '$2==2' | wc -l` → 85;
  `ls -l <subagents>/agent-*.jsonl | wc -l` → 158; `… | awk '$5==0' | wc -l` → 0.
- М-3: `grep -c '"name":"SubagentHandback"'` по четырём файлам → 2, 2, 2, 2; `grep -o '"agentType":"[^"]*"'` по
  meta → `scout` ×4. Содержимое транскриптов не читалось (только счёт строк).
- М-4: `ls docs/tasks/{handoffs,specs/reviews,specs/reports} | wc -l` → 75, 90, 102.

**Негативы и их положительные контроли той же формы.**
- «Читателя путей секции `handoff` в dispatch_manifest нет»: `grep -n "handoff\|_HEADER_RE\|SECTION_STOP_RE\|def
  section_cut\|def owned_paths\|sections\["` по dispatch_manifest.py — тот же вызов нашёл `def owned_paths` (:403) и
  `sections["owns"]` (:410), а по `handoff` — только ключ (:100), шаблоны текста (:73, :81, :89) и `SECTION_STOP_RE`
  (:124); список `def` модуля (:170–:613) читан целиком — `handoff_*` среди них нет.
- «`owns_gate` не видит записей воркера»: settings.json прочитан целиком — `owns_gate.py` только под `Task|Agent`
  (:27, :39); контроль формы: тот же файл показал `claim_control_gate.py` под `Edit|Write` (:53, :57).
- «Счётчика переписанных отчётов в протоколе нет»: `grep -n -i "transcrib\|retyp\|by hand\|переписан"` → одна строка
  :259 («journal by hand», про схему); контроль той же формы: тот же grep по находке-источнику находит «transcribed
  by hand» (строка 18) — паттерн рабочий. Кириллица `переписан` — регистр в shell-grep не сворачивается, но слово
  в протоколе английское (файл на английском).
- «Пустых `subagents/agent-*.jsonl` нет»: `awk '$5==0'` → 0; контроль той же формы на `.output` → 73.
- «Никакой другой хук не ограничивает запись по пути»: settings.json целиком — на `Edit|Write` только
  `claim_control_gate.py` (WARN, его докстринг :1–5 «WARN MODE (non-blocking)»), без matcher — `agent_budget.py`
  (ограничивает только на STOP, :192–202).
- Не проверено (оценка): что строка `tools:` роли не умеет ограничивать Write по пути (утверждение брифа; пробы не
  было); что хук PreToolUse внутри субагента получает `agent_type` — опора спеки на meta (замер t-672, D-0040), а не на
  это поле; `cwd` хука у воркера в worktree.

**Нужно сверх манифеста.** `tools/transcripts.py`, `tools/agent_budget.py`, `tools/dod_gate.py`,
`tools/critic_verdict_check.py`, `tools/mechanism_gate.py`, `tools/streams.py`, `tools/md_regions.py` (одна строка),
`plans/builder-rules.md`, `plans/piles/forge/batch-3-exam-debts.md`; листинги `~/.claude/projects/…/subagents/` и
`…/tasks/` (размеры и счётчики, без чтения содержимого).

## §L. Решения Lead по развилкам §7 (Fable, 14.10.2026 08:16) — обязательны для билдеров

Факт Ф-1 принят как главный: пусты `.output` (несозданная жёсткая ссылка), а не транскрипты `subagents/` (158 из 158
непусты) — отчёт никогда не терялся, его не достают. Поэтому М-б (инструмент) — первый по ценности, запускается первым.

- **F-1 — B**: Write получают только critic и designer (за хуком); scout остаётся без Write (read-only конфигурацией,
  scout.md:47–49 — защита внешнего ревью P0 не ослабляется); дайджест скаута достаёт М-б из `subagents/` в
  `docs/tasks/specs/reports/<t>-….md` (F-3). Правило 25 строк к scout НЕ применяется: его финальное сообщение и есть
  отчёт; scout.md получает одну фразу «the final message is the report; the Lead extracts it to a file with
  `tools/handback_extract.py`» — без лимита строк. N1: scout.md — только эта фраза.
- **F-2 — A**: новый `tools/handoff_gate.py` на `Edit|Write`, отказ exit 2, сбой при известном `agent_id` и Write/Edit → 2
  (не пропуск). Регистрацию (settings.json, `MECHANISM_PREFIXES`) делает Lead коммитом механизма.
- **F-3 — reports** (`docs/tasks/specs/reports`) для скаутов; critic — `docs/tasks/specs/reviews`; builder —
  `docs/tasks/handoffs`; designer — `docs/tasks/specs`. `HANDOFF_DIRS` — данные в `dispatch_manifest.py` (выбор дизайнера принят).
- **F-4 — A**: designer.md получает Write за хуком; обход «builder-тип с `model: opus`» прекращается с коммитом N3.
- **F-5 — B**: путь ИЛИ `--agent <id>` через `transcripts.find_agent_transcript`; неизвестный/неоднозначный id → код 1.
- **F-6 — B**: как `transcripts.is_writer`: нет пути в `owns:` → читающая, проверяется; есть путь → пропуск; текст
  диспатча не читается → отказ с дверью (FR-59). Остаток принят: builder без пути в owns и без meta встанет — редкий,
  дверь — переформулировать диспатч с `owns:`.
- **F-7 — B**: строка по `\n`, пустые и ограды считаются; строка длиннее 200 символов — `ceil(len/200)`.
- **F-8 — A**: файл по `handoff:` и есть отчёт п. 11: ≤ 500 слов прозы, дословные выводы прогонов в блоках кода не в
  счёт; ответ в чате ≤ 25 строк.
- **F-9 — A**: без кода сейчас; 28 (г) считает; код — после утечки.
- **F-10 — B**: N1 не трогает строки `tools:`; Lead добавляет `Write` critic/designer тем же коммитом, что регистрирует
  хук. Порядок запуска: N2 первым (сегодня), N1 и N3 — по мере освобождения слотов писателей (D-0040); слияние — N2 в
  любой момент, N1 первым из правил, N3 — коммитом Lead.
- **Аналоги** — в очередь forge/6 строками при интеграции: `_path_allowed` от `cwd` (worktree), композиция
  `agent_id → файл` в двух местах (ось 14), кейс `hook_liveness_probe` для нового хука, `dod_gate` BLOCK_MESSAGE, строки
  PROJECT.md / CLAUDE.md R11 / SIBLING_MAP оси 13–14 — Lead при коммите N3; ключи экзаменов F3-1/F3-2 — находка в пачку 3;
  память Lead исправлена этим же ходом; находка-источник получает строку-поправку (Ф-1) при закрытии F5-1.
- Критик на план: не положен (D-0035 (b): развилки решены этим блоком, схемы и денег нет; дифф N3 пойдёт через критика
  как хук > 100 строк).

## §L-2. Решения Lead по вердикту критика t-753 на N2 (Fable, 14.10.2026 08:48)

- Форма stdout М-б (§3.2, §8 N2 DoD) приводится к построенной: `written <out> bytes=<n> lines=<n> source=<handback|last_text>
  finished=<yes|no>` — счёт строк по F-7 (B) нужен §6; поздний блок берёт верх.
- Отклонение 1 принято как построено: `finished` решается `transcripts.last_tool_use_names` по всему файлу (слепое окно
  64 КБ `is_finished` — forge/6 F6-7: починка в читателе + общий `handed_back(lines)`, обход снимается там).
- Маркер незавершённости — два текста: без `SubagentHandback` — прежний; при `source=handback` и вызовах после него —
  `<!-- handback_extract: the worker made tool calls after this SubagentHandback (a refused stop, or still working); this
  hand-back may not be its final one -->`. Фикс-раунд (свежий билдер, attempt 2): правки 1–4 вердикта t-753; CRLF-счёт
  строк (находка 6) — не чинится (файлы инструмента LF, вход читается как есть).
- Lead при коммите N2: строка HE в ряду «Consumers» оси 14 SIBLING_MAP.

## §L-3. Решения Lead по вердикту критика t-757 на N3 (Fable, 14.10.2026 09:57)

- Отклонения билдера: (3) неизвестный вид → объединение папок `HANDOFF_DIRS` — принято; (4) нерешаемый транскрипт
  блокирует и билдера — остаток F-6 (B), принят; (5) в хуке остаётся `owned_paths(cut)`, перенос предиката лимита
  `dispatch_gate` на тот же срез — в очередь forge/6 (ось 13, строка при регистрации); (6) префикс `docs/tasks/specs` в
  `ALLOWED_DIRS` на STOP — принят, тест прямого потомка не нужен; (7) текст `stop_message` утверждён: «a reading worker
  at STOP writes its report to the `handoff:` path of its dispatch; with no `handoff:` path the final message is the
  report» — правка 3 вердикта идёт в раунд; (1) и (2) билдера — приняты как построено.
- Фикс-раунд (свежий билдер, attempt 2): правки 1, 2, 3, 7, 8 вердикта t-757; свидетель + `tools/test_dispatch_gate.py`
  (он зовёт `given_paths` через dispatch_gate.py:716).
- Регистрация (коммит Lead после раунда и зелёного CI `forge-check` на коммите N3): settings.json, `MECHANISM_PREFIXES`,
  `Write` в `tools:` critic.md и designer.md, кейс `hook_liveness_probe`, CLAUDE.md R11 («читающая роль получает путь
  отчёта на `handoff:`, никогда на `owns:`»), PROJECT.md «выжимка», SIBLING_MAP оси 13–14. До регистрации диспатчи
  critic/designer по-прежнему builder-типом с owns (находка 6 вердикта — с момента регистрации путь на `handoff:`).

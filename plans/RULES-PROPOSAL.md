# Правила фабрики против принципов владельца — предложение

> **Внесено 29.09** в `design/factory-rules.md` с согласия владельца (вместе с исправленной FR-57).

Сверка `ai-packages/qa-factory/design/factory-rules.md` (FR-1…FR-46, 29.09.2026) с принципами
владельца P1…P15 (см. [BACKLOG.md](BACKLOG.md)). Итог: пять принципов уже стоят правилами, у
трёх правило есть, но не дотягивает, семи нет совсем, и одно правило (FR-13) с принципом
расходится.

Правила пакета пишутся по-английски (FR-30), поэтому формулировки ниже — готовый текст для
вставки; пояснения — по-русски. По контракту файла у каждого правила есть измеренный провал
(*Why*) и что смотреть в диффе (*Check*); номера — следующие свободные, не перенумеровывать.
Применяется после согласия владельца, одним коммитом вместе со строками в `factory-rules-debt.md`
для мест, которые нарушают новые правила уже сегодня.

## Сводка

| принцип | статус | правило |
|---|---|---|
| P1 код помогает роли | **нет** | новое FR-47 |
| P2 универсальность | **расходится** с FR-13 | правка FR-13 |
| P3 дирижёр — помощник | **нет** | новое FR-48 |
| P4 материал без потерь | частично (FR-8 — только слова человека, FR-15 — пути) | новое FR-49 |
| P5 лестница получения | **нет** (есть в коде с 26.09, правилом не закреплена) | новое FR-50 |
| P6 джев снимает траты LLM | **нет** | новое FR-51 |
| P7 Sonnet или Terra | частично (FR-32: «не большая модель») | новое FR-52 |
| P8 эксперименты без следов | частично (FR-36 — только проба записи) | новое FR-53 |
| P9 вопросы человеческим языком | есть FR-6 | правка Check FR-6 |
| P10 карта и оси симметрии | частично (FR-17 — одна проблема, не карта) | новое FR-54 |
| P11 метрика трения | **нет** | новое FR-55 |
| P12 новый код — похожие места и трение | частично (FR-17) | входит в FR-54 и FR-55 |
| P13 слово человека через любой гейт | есть FR-4 | правка FR-4 |
| P14 только нужные инструменты | **нет** | новое FR-56 |
| P15 отказ не запирает роль | есть FR-1, FR-2 | правка FR-2 + новое FR-57 |

Отдельно: FR-33 («материал, вставленный человеком, не доказывает правку») не противоречит P5 —
вставленный человеком текст законен как вход стори, но не доказывает, что починен маршрут
получения. Это стоит сказать в тексте FR-50.

## Новые правила

**FR-47 (G) — Code is an instrument a role calls, never a substitute for the role's judgment.**
The role runs the script itself, reads what it reports, and decides what is missing and how to
fix it; when the script meets something it was not built for, it says what it could not do and
leaves the role a move. *Why:* about 40 % of the scout's turns went to matching the form our own
scripts expect instead of understanding the story; the scout wrote 11 helper scripts and hit 12
tracebacks in one S1; the code critic's friction reached 44.2 %; the driver sends every repair as
`test_defect` although the critic already wrote the real cause — code decided what only the role
knew. *Check:* for every step the change moves into code, name what the role still decides, and
run the script on a project shaped differently from the fixture — it reports, it does not halt.

**FR-48 (A) — The conductor is called for a problem, never to run a command.** Routine commands
run from code, triggered by a stage transition or by a question appearing; the conductor gets
the problem, the evidence and the doors. *Why:* before the driver the orchestrating model was
47.7 % of a story's cost (2553); on the driver the conductor still held 76 sessions, 21 of them
($9.01) spent parsing a person's words, and 16 of 25 `ask_person` carried an empty question.
*Check:* every conductor call site names the problem that triggered it; nothing the conductor
does could be a fixed command.

**FR-49 (C) — What a stage gathers travels in its handoff, whole.** The next stage never gathers
it again, and nothing collected is dropped between contracts; material nobody downstream reads is
not gathered. *Why:* a probe overwrote `source-inventory` and the person's words were lost (F8);
the ticket snapshot written as `ticket-snapshot.md` never reached the scout's brief, which reads
`.json`; four merge requests with 17, 101 and 80 discussions were gathered and cited nowhere.
*Check:* for each field the change produces, name its reader downstream — or declare it terminal.

**FR-50 (A) — Whatever the work needs from outside is tried by every route before a person is
asked, and then the person gets three answers.** API, SSH, an agent, a browser — then the person:
*not needed*, *here is how to get it*, *here it is as text*. Text a person pastes is a legitimate
input for the story; it does not prove a fix to the route (FR-33). *Why:* S1 of 2553 took 2 h 54
min and about $12 because the Jira tool belonged to the orchestrator's session, not the scout's
process; the route ladder (API → local checkout → person with three options) was added on 26.09
after the same class of failure. *Check:* the refusal lists each route tried and why it failed;
the question to the person offers the three answers.

**FR-51 (F) — Work moved to a deterministic tool is judged by the LLM spend it removes.** The
tool's own cost is reported, not optimised. *Why:* standing design rule; on judge-on the tool cost
$0.011 for 855 records while the story rose by $11, all of it on the model side — the only number
that decides is the model's. *Check:* the change reports the LLM spend of the affected stage
before and after.

**FR-52 (G) — The factory's roles run on Sonnet or Terra, never on Haiku; a fix that holds only on
a stronger model is not a fix.** *Why:* standing design rule (owner, 29.09); FR-32 already forbids
fixing by a bigger model, and the rule names the floor it protects. *Check:* the role files bind
no other model; a quality regression is fixed in the role's instructions or the code, not in its
model line.

**FR-53 (E) — A comparison run leaves no trace in the project.** No merge request, no tracker
comment or subtask; bugs go to a Markdown file or the chat; the run works on a copy. *Why:* in a
run whose standing rule was "never write to the tracker", the conductor spent a dispatch asking
for write permission and the gate packet advertised "tracker write: confirmed" (FR-36). *Check:*
the experiment's `external_writes` is closed, and the run's record of outward writes is empty.

**FR-54 (G) — A change finds its siblings by the map.** Logic that has a twin in another stage is
listed in the factory map with both sides' files; a change to one side names the other and either
changes it or says why not. *Why:* `node_ids.py` was wired into three of four sites and the fourth
produced FR-16; the repair cause is hard-coded identically at S4, S5 and S7; the "one question
for every stop" symmetry breaks at its edges — S0 ignores the person's word, S9 halts `--until
end`. *Check:* the commit names the axis and each twin site.

**FR-55 (F) — Friction with our own code is measured on every run, and code that makes a role's
stage dearer than without it is a defect.** A turn is friction when our code returns a traceback,
a hook refusal, an argument-shape error, a validator refusal of our own artifact, or when the role
writes itself a helper script; the turn carries its full context cost. *Why:* S5 of 15045 lost
127 of 1668 calls (7.6 %) to our own hooks; across run 5 friction was 15.5 % of turns, 44.2 % for
the code critic. *Check:* the change reports `code_friction` for the affected role on a live run,
before and after.

**FR-56 (C) — A role is given only the tools its work needs.** *Why:* one tool schema is about
10K tokens of every turn's context; the scout's fixed prompt is 36.7K tokens with Bash and about
25K without, of which our own text is 7.1K. *Check:* every tool in a role's definition is named by
a step of its phase instructions.

**FR-57 (A) — A ban is never bypassed, and never a dead end.** It holds regardless of state — no
exemption because the file already exists or a step already ran — and it is never passed by a
workaround: a heredoc, a helper script, another tool. Every ban names its door: the command that
does the legitimate version of the refused act, and the person's word, which the ban accepts and
records (FR-4). Where the role can judge, the door is the role's, not a question: an interrupted
artifact is continued by default — the role keeps the rows that parse, validate and were built on
the same inputs, repairs the stale ones, and sets the rest aside as `.superseded` only when
nothing is usable. A role that cannot judge and has no door files a finding and asks; it neither
stops silently nor works around. *Why:* standing
design rule (owner, 29.09); roles worked around refusals with self-written scripts and Python
heredocs, and the pre-tool guard refused the same unparseable input twice in a row with no finding
filed (FB-6); on TP1-13877 a write interrupted by a network failure left `test-plan.json` with
3 rows, the guard refused a write over it, and the only way on was a person deleting the file by
hand — a ban with no door. *Check:* for each ban, name its door and the words that pass it; run
the ban on an interrupted artifact — the role continues without asking a person, and a person's
"delete it and start again" still reaches a command that executes it.

> Первая редакция («a trapped role writes a finding and stops the attempt») заперла бы роль и
> после слова человека: удалить или дописать файл было бы нечем, кроме обхода. Исправлено
> 29.09 по замечанию владельца — запрет стоит против обхода, а не против законного действия;
> дверь для него — FR-40 и FR-4. Вторая правка того же дня: выбор «дописать / начать заново»
> не вопрос человеку — «начать заново» лишь крайний случай «дописать», когда годных строк нет,
> и это суждение роли (P1). Старый файл не удаляется, а откладывается (P4).

## Правки существующих

**FR-13 — сейчас:** «Variety lives in data files, never in code.» Это противоречит P2: таблица
в файле данных так же не знает значения, которое принесёт новый проект, как и список в коде.
**Предлагаю:** «Closed variety lives in data files, never in code. Open variety — anything a new
project can bring: layouts, phrasings, sources, tools — is judged by a role; code reports what it
found and does not decide.» *Why* дополнить: pytest зашит в слой автоматизации (карточка
маркеров, `diff_scope`, `execution_fingerprint`), `cost_capture` узнаёт CLI `testproject1` регуляркой.
*Check* дополнить: «can a project bring a value this table does not hold? Then the table is a
hint to a role, not a decision.»

**FR-6 — Check дополнить:** «…and it applies to every text a person reads, including a role's halt
and a refusal the conductor relays; outgoing questions are checked by code for form-field names,
plugin paths and dispatch ids in the body.» Проверка на наличие идентификатора — это проверка
присутствия, FR-12 её не запрещает. *Why* уже есть в `human-questions.md`: «cannot fill
person.review_recorded».

**FR-4 — дополнить:** «…and when the block was the factory's own, the pass is also filed as a
factory finding in the person's words.» *Why:* S0 обещает «answer `go on`» и не читает ответ
(карта путей E1) — проход без записи в бэклог не оставляет следа, что блок был нашим дефектом.

**FR-2 — дополнить:** «A refusal never names a path or tool the refused party cannot reach, and
never leaves it without a move.» *Why:* 108 блоков контроллера называют дверь, которую ни разу
не открывали в тесте (долг FR-1/FR-2).

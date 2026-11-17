# Forge test rules: where the expected value comes from, a bounded can-fail proof, the critic's test questions, the `test:` line -- DRAFT r2 (fix round)

task: t-940 (draft) -> t-956 (fix round on plan critic t-949; t-940 is not reopened) | feature: F19 | designer draft for
Lead acceptance; each build stream gets its own task_id
Language: owner-facing rule texts in Russian carriers stay Russian (TESTING.md, builder-rules, RUNBOOK); English carriers
(critic brief, role files, CLAUDE.md, calibration protocol, tool docstrings) stay English; tool messages and data keys
English.
Scope: forge process files (`docs/`, `plans/`, `.claude/agents/`, `tools/`, `PROCESS/`, `CLAUDE.md`) and ONE package file:
the probe runner `ai-packages/qa-factory/scripts/tests/mutate_once.py` with its new test file and keep row (stream S-E,
Lead decision B1 -> (a)). S-E is a package change: its AR-n, owners and census class are in §1.1; every other stream
stays outside the package and carries no `architecture:`/`judgment:` lines. Owner of every forge check added below: DATA
(code) for presence/shape/joins; JUDGMENT (critic, accepted by the Lead) for sufficiency, equivalence, load-bearing,
the value's source and the new-file choice (AR-29/P27 applied to the forge by analogy; no package census row).

Fix round t-956: every change against t-949 and the owner's word on O-1 is listed in §15 (one row per remark).

---

## §0 Premises (each read in its carrier; t-940 17.11.2026, re-read in t-956 17.11.2026 where marked r2)

| # | Fact | Carrier |
|---|---|---|
| P1 | TESTING.md has no rule on the source of a test's expected value; its how-to (`:135-162`) and «Что пишется» (`:43-59`) speak of layers, doors, data, never of the oracle | `docs/TESTING.md` read whole (r2) |
| P2 | The brief retires the mutation list and sends mutation runs to the canon: `:11` «no mutation list (retired 10.11.2026, `docs/TESTING.md`)», `:19-20` «ratchets and mutation runs are not — they are the batch canon's (D-0056)»; `:14-15` «A layer not attached is returned to the dispatcher as a request, never executed by the critic» | `docs/tasks/critic-diff-brief.md:8-21` (r2) |
| P3 | builder-rules 7b `:57-59` «**Мутации** билдер не прогоняет и не перечисляет: мутации судит канон пачки (слово владельца 28.10 и 10.11.2026, `PROJECT.md` «Командная работа» п. 13)» | `plans/builder-rules.md:57-59` (r2) |
| P4 | No CI workflow runs a mutation: Grep `mutat` -i over `.github` -> 0; positive control same tool, `python` -i over `.github/workflows` -> 82 hits in 5 files | Grep tool, 17.11 (critic t-949 re-ran: same) |
| P5 | Other carriers of «мутации судит канон»: `PROJECT.md:364-365` (п. 13), `AGENTS.md:379-380` (generated), `docs/RUNBOOK.md:115` (r2: «Мутации судит канон пачки (`PROJECT.md`, «Командная работа» п. 13)»), `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:377-378` | Grep (r2 for RUNBOOK) |
| P6 | D-0056 (archive) rule (2)/(3): builder names mutants, canon runs one mutation pass, the critic's re-run is «never ... a mutation run»; no archive line supersedes it (L-6 does) | `docs/DECISIONS_ARCHIVE.md:112` |
| P7 | Brief q5 says «A missing pin is NOT a finding»; q5 also carries the offload-only new-file exception (`:42-44`) | `critic-diff-brief.md:35-46` (r2) |
| P8 | New-test-file texts (r2): TESTING «Бюджет / Файлы» `:117` «новый тестовый файл не создаётся», offload exception `:124-127`; «Чего больше нет» `:55` «нового тестового файла на новый скрипт (исключение — «Бюджет / Файлы»)»; how-to `:141` «нового файла нет («Бюджет / Файлы»)»; «Время» `:128` «новый тестовый файл укладывается в 10 с»; critic bullet `:176-178`; builder-rules 7d `:90-93` «новый тестовый файл не создаётся: ... файл у нового скрипта — только со строкой `keep` ... и не дольше 10 с»; `builder.md:51-52` «no new test file is written without a keep row (7d)»; `designer.md:22` «test file outside the keep rows of `test-layers.json`». The goal is measured at `docs/TESTING.md:26-29` (files over 10 s; edits in commits where neither code nor text changed) | read (r2) |
| P9 | 7b `:44-53` keeps a TEMPORAL branch «Пока перевод в карантин не выполнен (в `test-layers.json` нет строк `quarantine`)»; the section exists (`test-layers.json:7174`) | Grep |
| P10 | 7d `:89` «Свидетель наличия ключей в тексте — вывод в отчёте, в репозиторий не коммитится» — no negative control named | read (r2) |
| P11 | `tools/dispatch_manifest.py` (r2): `KEY_GROUPS` `:84-93`, `ITEMS` `:94`, `_DISPLAY` `:95`, `DESIGNER_THRESHOLD = 3` `:105`, `_FORM_ITEMS` `:123`, `INCOMPLETE_TEMPLATE` `:137-143` (forms from `_expected_forms()`), `SKIP_REFUSED_TEMPLATE` `:144-147` (`", ".join(ITEMS)`), `_parse_skip_line` `:258-276` (`:271` `if name not in ITEMS` -> «unknown item»), `_items_text` `:902-903` (`_DISPLAY[i]`), `check_cut` `:906-971` with the skip loop `:948-959` (`newly` at `:953`) and `still` at `:961`; mechanism path (`tools/mechanism_gate.py:236`… named net) | read (r2) |
| P12 | `tools/dispatch_new.py` prints headers only (`build_text`, `:85-106`); no `test:` line today | read |
| P13 | Verdict checker: rules hard-coded in `critic_verdict_check.validate_verdict` (`:63-170`); reference schema `tools/critic_verdict.schema.json` requires verdict, blockers, class_completeness, trail; `trail.reruns[]` items are `{command, result}` | read (r2) |
| P14 | `PROCESS/CRITIC_EXAM.md` absent; precedent road «Deviation: exam not run; debt F3-1» | Glob, Grep |
| P15 | Calibration checks run to 48 (r2: Grep `^(4[6-9]\|5\d)\. \*\*` -> 46, 47, 48 at `:1109-1113`); 49 claimed by the architect-tier spec | Grep (r2) |
| P16 | Journal evidence, re-cut BY READING (r2, F6): `logs/journal/dev1.jsonl` as read 17.11: 123 `rejected`, 70 `failure_class: spec`; the regex `"event": ?"rejected".*"failure_class": ?"spec".*(test\|pin\|тест)` -i gives 27 lines (25 at t-940; t-935, t-937 added 17.11 01:59). Read one by one: **7 in class** (the spec did not name the test place / sent rows to a quarantined file / left a door behaviour without a row / let a value come from the code's output), **2 border**, **18 out of class** — the list and the reason per id in §6.1 | Grep content mode + reading the `notes` of each line (r2) |
| P17 | r2. The probe runner exists: `ai-packages/qa-factory/scripts/tests/mutate_once.py` (60 lines): `<spec.json> <mutation id>`; `target`/`test` paths under `scripts/` (`SCRIPTS = Path(__file__).resolve().parent.parent`, `:18`); the anchor must occur exactly once else exit 64 untouched (`:35-38`); byte copy, mutate, `subprocess.run([sys.executable, "-B", test])` with NO timeout (`:41`), restore in `finally` (`:42-43`), sha256 before/after; exit 0 when the test failed (ANY non-zero exit counts as a kill, `:55`), 1 survived, 2 sha mismatch. No test file covers it: Grep `mutate_once` over the package -> only its own docstring `:3`; over `tools/` -> 0 (control: `handoff_gate` over `tools/` -> 83 in 12 files); `test-layers.json` has no row for it (Grep `mutat` -i -> 2 unrelated rows) | read, Grep (r2) |
| P18 | r2. The write boundary of a reading role: `CLAUDE.md:79-80` (rule 3) «a cheap control re-run of what is attached is legitimate, investigating the mechanics by reading is not; a layer not attached → critic asks the dispatcher for it and does not execute it»; `CLAUDE.md:237` (R11-h) «`tools/handoff_gate.py` lets it write only that file»; `tools/handoff_gate.py:1,6-8` «PreToolUse hook (Edit\|Write) … this hook is the whole protection: it lets such a worker write the one path of its dispatch and refuses every other Edit/Write»; the critic's `tools:` line carries Bash and Write (`.claude/agents/critic.md:5`, per t-949) | read, Grep (r2) |
| P19 | r2. Anchors that the CLAUDE.md edits must keep byte-identical: `tools/install_parity_anchors.json:23` «TWO-LAYER CRITIC ENTRY», `:62` «`tools/handoff_gate.py` lets it write only that file»; no anchor holds «a layer not attached» (Grep over `tools/`, `.claude/agents` -> only `handoff_gate.py:7` and the `:62` anchor for the sibling phrases) | Grep (r2) |
| P20 | r2. `tools/agent_budget.py:116` counts test runs by `TEST_RE = r"pytest\|selftest\.py\|tests[\\/]test_\w+\.py\|unittest"`; a runner call whose test path sits inside a spec JSON does not match it, an inline call naming `tests/test_x.py` or `pytest` does | read (r2) |
| P21 | r2. spec-facts-by-code S2 owns `tools/dispatch_manifest.py` + `tools/test_dispatch_manifest.py` and adds a READERS NOTE inside `check_cut` (`20261116-spec-facts-by-code-spec.md:371-381, 588-599`); not landed: Grep `READERS` over `tools/dispatch_manifest.py` -> 0 (control: `KEY_GROUPS` -> 7 in the same file) | read, Grep (r2) |
| P22 | r2. everything-in-piles: C's old-verdict door text «verdict: none -- verdict predates remarks» (`20261117-everything-in-piles-spec.md:246-247`) and A2's invalid-shape refusal «a verdict written before remarks existed: "verdict: <node> none -- verdict predates remarks"» (`:307-309`); its P31 (`:61`) «`critic_verdict_check.py` is on NO execution path (the critic self-runs it; the coordinator by hand)» | read (r2) |
| P23 | r2. `scenario_walk.py --witness-for` (`:887-922`) matches a path under `scripts/tests/` only by a keep row's `covers` (candidate `tests/<name>.py`, `:913-916`); with none it prints «no scenario or keep row covers … run the whole scenario layer» (`:920`) | read (r2) |
| P24 | r2. The package's census scope: «every check unit of every `scripts/*.py` outside `scripts/tests/`» (`design/architecture.md:146`, AR-29 detector) — `mutate_once.py` is outside it | read (r2) |
| P25 | r2. `tools/mechanism_gate.py:24-25` «lines "axis N: <verdict>" for EVERY axis of the current docs/SIBLING_MAP.md»; `:42-51` a line carries the axis KEY as a label, «axis N (<key>): …», an unlabelled line is refused since 2026-10-16; the key is the heading title cut at its first colon, its short form the first three words; SIBLING_MAP has 37 axes (Grep `^## Axis` -> `:24` … `:628`) | read, Grep (r2) |

---

## §1 What changes (map of D1-D6 to texts, carriers, detectors, cost)

| Lead direction | Text (§) | One home | Pointers | Code | Detector | Cost |
|---|---|---|---|---|---|---|
| D1 oracle | §2.1 | TESTING.md «Откуда берётся ожидаемое значение» | builder-rules 7d, builder.md 8, critic.md 20, brief q5 (b) | none (judgment) | check «Forge test discipline» (d), critic q5 (b) | 0 runs; reading |
| D2 can-fail | §2.3, §3.2, §3.4, §5.3 | builder side: TESTING «Тест может упасть»; critic side: brief «The two layers» (the probe and its cap) | 7b, 16 (б), critic.md 17/20, CLAUDE.md rule 3 and R11-h, `handoff_gate` docstring, RUNBOOK, calibration 13(j) | runner `mutate_once.py` (S-E), verdict `mutants` (S-D) | check (b)(c) | builder: 1 narrow run per defect item; critic: the probe runs capped in the brief, each <= the runner's 60 s timeout |
| D3 critic questions | §3.1 | brief q5 | critic.md 20, TESTING «Кто что делает» | none (judgment) | check (e) | reading; no new tests demanded beyond door-reachable behaviour |
| D4 spec line | §2.2 | TESTING.md «Строка теста в DoD» | designer.md 1 | gate (S-C) | gate refusal + check (a) | measured §6: <= 1 line per behaviour item, 0.8-2.7 % of a spec |
| D5 contradictions | §4 | TESTING «Бюджет / Файлы» (goal-based, the owner's word 17.11); 7b; rule 11 DOC-DISPATCH | 7d, builder.md 4, designer.md 1, brief q5 (g) | none | carrier-test rows | none |
| D6 code | §5 | `dispatch_manifest.py` (test line), `critic_verdict_check.py` (mutants), `mutate_once.py` (runner) | dispatch_new, schema | S-C, S-D, S-E | check; tests | one table each |

Owner's words answered: «у нас в фордже и требований нет. Или вместо них у нас спека?» -> §2.1. «надо исправить, но не
вернуться к куче мутантов...» -> §2.3 + §3.2 (a capped probe through one runner, narrow file only, no suite anywhere;
stale «канон судит мутации» removed §4.4). «На каждое новое поведение логично писать тест, но так что бы прогон и
написание тестов не стали основной работой форджа» -> §3.1 (c). «а это не сделает разработку в 2 раза медленнее?» ->
§2.2, §6. «не хочу что бы написание тестов зависило от моего слова. Какая была цель у сокращения количества файлов? Вот
этой цели и надо придерживаться когда решаем нужен отдельный фаил или нет» -> §4.1. «всё что недоделанно делаем
сегодня» -> §7, §8.

### 1.1 The package part (S-E only): AR-n, owners, census (designer rule 1; CLAUDE.md rule 10 package paragraph)

| AR-n | How S-E touches it | How kept | Change check written into S-E's DoD |
|---|---|---|---|
| AR-4 nothing tied to one machine | new `--root`; target/test paths relative to it | the runner stores nothing; `--root` is explicit (no git-top read, no default machine path); a target or test resolving outside `--root` is refused before touching | report line: «stores no path; prints only the test file's name and relative target»; the `outside-root` row of the table |
| AR-7 code is an instrument | the runner executes and classifies the process outcome | the critic still decides which places are load-bearing, whether a survivor is equivalent and whether a printed FAIL line is a real kill (§5.3 error direction) | report line «what the role still decides: the places, equivalence, reading the printed FAIL lines» |
| AR-9 every refusal names what it expected and a door | new exit-64 refusals (empty anchor, no change, outside root, absent test, non-UTF-8) | each prints what is wrong, what was expected and the argument that fixes it | `python -B ai-packages/qa-factory/scripts/refusal_registry.py --check` exit 0; whether its scan reaches `scripts/tests/` is not established — the builder reports what it printed |
| AR-29 code judges data | outcome classes killed / survived / invalid / restore-mismatch | classes come from the exit code, the test's summary counts and a `compile()` of the mutated text — shape, never meaning | census: `mutate_once.py` is outside the census scope (P24), no row; the builder names the class anyway in the report (shape for the outcome classes, safety for the restore/sha refusal) and runs `python -B ai-packages/qa-factory/scripts/tests/test_judgment_census.py` (if it is in `SLOW_TESTS`: «судит канон пачки») |

Owners of the checks S-E adds: outcome classification — DATA (code); refusal before touching and restore/sha — DATA
(safety class); load-bearing / equivalence / a FAIL line that is really an import error — JUDGMENT (critic, accepted
by the Lead). Commit lines of S-E: the `architecture:` line naming AR-4, AR-7, AR-9, AR-29 with how each is kept, and the
`judgment:` line in its «adds data check» form, unit `mutate_once.main` — both in the forms that `tools/architecture_gate.py`
(docstring `:15-16`, `:34-38`) carries; the builder copies the form from there, never from this spec.

---

## §2 TESTING.md texts (stream S-A1)

### 2.1 New subsection, inserted after `docs/TESTING.md:59` (end of «Что пишется — три слоя, и только они»), before «### Карантин старых тестов»

```
### Откуда берётся ожидаемое значение

Слово владельца 17.11.2026 («у нас в фордже и требований нет. Или вместо них у нас спека?» — да, спека). Требование к
тесту форджа — спека узла и её DoD, текст правила, которое исполняет код (`CLAUDE.md`, `PROJECT.md`, этот документ,
`plans/builder-rules.md`, файл роли, FR-n), или слово владельца с носителем. Ожидаемое значение берётся оттуда, и спека
называет источник строкой `expected from:` («Строка теста в DoD», ниже). С вывода кода ожидание не списывается: тест,
чьё ожидание переписано из того, что код напечатал, может только пройти (для фабрики это P20 и FR-58). Спека молчит о
значении — билдер его не выбирает, а возвращает вопрос (`CLAUDE.md` правило 11: молчащий край — дефект диспетчера).
Ожиданием из кода НЕ считаются: дословный текст отказа, который дала сама спека; срез настоящего прогона как ВХОД
(исход на нём — всё равно из спеки); значение, выведенное из входа самого теста по правилу, которое называет спека
(N строк на входе — N на выходе, если спека так велит); поведение, которое спека велит сохранить, только когда она
называет само сохраняемое — значение или инвариант (что остаётся отказом, что печатается); «вывод остаётся как
сейчас» без названного значения — это снимок кода и тест «как раньше» из таблицы «Что не пишется», а не источник.
```

Invariant: no asserted value enters a forge test without a source a tier above can check. Edges: spec silent -> question
(builder.md rule 1), never a value picked by the builder; a value picked anyway is critic q5 (b); a keep clause with no
named value or invariant is a spec defect (critic q5 (b) names it against the spec), never a licence to snapshot output.

### 2.2 New subsection after 2.1

```
### Строка теста в DoD

Слово владельца 17.11.2026: «а это не сделает разработку в 2 раза медленнее?» — поэтому одна строка на пункт, и только
на пункт поведения. Пункт спеки билдеру, который меняет то, что видно через дверь (аргумент или выход CLI, вердикт хука
или гейта, поле или файл, который читает другой), несёт внутри DoD одну строку:

    test: <файл::таблица или строка> | expected from: <§ спеки, правило, слово владельца>

или `test: none -- <почему> | expected from: <источник>` (документ — свидетель по правилу 11 `CLAUDE.md` «DOC-DISPATCH
WITNESS»; суждение роли — живой прогон; внутренняя граница без своей двери). Строка называет МЕСТО строки теста
(существующая таблица, история или стык; новый файл — по цели «Бюджет / Файлы») и ИСТОЧНИК ожидания; самих значений
не повторяет — они в тексте пункта и его краёв. Пункт без поведения (перенос текста, переименование) строки не получает;
диспатч, где такого пункта нет вовсе, несёт одну строку `test: none -- поведения нет | expected from: <§ спеки>`.
Наличие и форму строки проверяет код (`tools/dispatch_manifest.py`, диспатч билдеру от порога дизайнера); хватает ли строк
и верен ли источник — судит критик (вопрос 5 `docs/tasks/critic-diff-brief.md`).
```

### 2.3 New subsection after 2.2 (F8: no cap number here)

```
### Тест может упасть: одна проба, а не набор мутаций

Слово владельца 17.11.2026: «надо исправить, но не вернуться к куче мутантов, которые шли дольше написания кода». Набор
мутаций не пишется и не гоняется никем: список снят 10.11.2026, канон пачки мутаций не гоняет. Вместо него две пробы с
потолком:
- **Билдер, пункт-дефект** (пункт чинит дефект, найденный живым прогоном, критиком или CI): строка, которая его ловит,
  пишется ДО правки кода и прогоняется один раз — только узкий файл этой строки; вывод идёт в свидетель строкой
  `red-before: <команда> -> <хвост вывода>`, затем правка и обычный свидетель. Красным считается падение на утверждении
  строки; падение на импорте или сборе (двери ещё нет) — не красное: тогда `red-before: not runnable -- <почему>`.
  Строка в медленном или карантинном файле — `red-before: not run -- <файл> судит канон`. Цена — один узкий прогон.
- **Критик, дифф с новым поведением**: ломает несколько мест нового поведения одним раннером фабрики и смотрит, какая
  строка краснеет; раннер, процедура и потолок — `docs/tasks/critic-diff-brief.md` «The two layers».
```

Invariant: a defect row that was never seen red is never presented as a regression proof without a named reason; no
carrier sends anyone to a mutation suite; the cap number lives only in the brief and in the checker (F8).

### 2.4 «Кто что делает» (`docs/TESTING.md:174-182`)

- `:174` -> «- **Дизайнер**: DoD называет поведения и стык, а не число проверок; ребро спеки — строка таблицы теста; на
  пункт поведения — строка `test:` («Строка теста в DoD»); место новой строки, в том числе новый файл, — по цели
  «Бюджет / Файлы».»
- `:176-178` the critic bullet (a restatement of brief q5, axis 31) -> «- **Критик**: вопрос 5 и проба «The two layers»
  `docs/tasks/critic-diff-brief.md`.»
- `:181-182` detector sentence: append «; строки `test:`, пробы критика и `red-before:` — калибровочная проверка «Forge
  test discipline» (`PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`)». The check is named by its TITLE, not its number (F14 (iii)):
  the number is the next free one when S-B lands, and S-A1 lands before S-B (§8); the landing text is the title line
  above, no instruction text is landed.

### 2.5 The artifact sweep of «new test file» inside TESTING.md (rule 9, sweep-the-artifact-first; S-A1)

| Neighbour | Verdict |
|---|---|
| `:55` «нового тестового файла на новый скрипт (исключение — «Бюджет / Файлы»)» | applied -> «нового тестового файла на новый скрипт вместо строки в историю (когда новый файл верен — «Бюджет / Файлы»)» |
| `:117-127` «Бюджет / Файлы» | applied — §4.1 |
| `:128` «Время: новый тестовый файл укладывается в 10 с» | not applicable — already the goal's run-time criterion; kept |
| `:141` «нового файла нет («Бюджет / Файлы»)» | applied -> «новый файл — только по цели «Бюджет / Файлы»» |
| `:156-158` «новый файл (часть разрезанного — до 60 с в CI) укладывается в 10 с» | not applicable — consistent; kept |
| `:160` the «Плохо: файл по имени тикета» example | not applicable — the ticket-named file stays banned by §4.1's text; kept |
| `:176-178` critic bullet | applied — §2.4 |

---

## §3 Critic texts

### 3.1 `docs/tasks/critic-diff-brief.md` question 5 (`:35-46`) -> (stream S-A1)

```
5. **Tests** (`docs/TESTING.md`, the owner's words 10.11 and 17.11.2026), each sub-question answered:
   (a) KILLING POWER: would the node's test catch the defect the node exists for, through the door the factory uses --
   judged by reading AND by the probe of «The two layers»; a probe mutant in load-bearing new behaviour that survives is
   a finding (an equivalent mutant is not, with its why). For a defect item, the builder's `red-before:` line is read: a
   red at import or collection is not a red.
   (b) EXPECTED VALUE: every asserted value traces to the spec/DoD, a rule text, the owner's word, or the test's own input
   by a rule the spec states (`docs/TESTING.md` «Откуда берётся ожидаемое значение»); a literal that matches only the
   code's own output, with no such source, is a finding; a value the spec left silent and the builder picked, or a spec
   clause "stays as now" that names no value or invariant, is a finding against the spec.
   (c) NEW BEHAVIOUR HAS A ROW: each new behaviour reachable from OUTSIDE the unit -- through a door: a CLI argument or
   exit, a hook's verdict, a gate's refusal or pass, a field or file another reader reads -- has a scenario, junction or
   table row; a missing row is a finding. A new internal function, branch or helper that no door exposes on its own
   needs no row (`docs/TESTING.md`: an internal boundary gets no test); it is covered through the door that reaches it.
   (d) REWRITTEN OR DELETED TEST: the report names where its behaviour is still checked (file::row), or that the spec
   removed the behaviour; neither is a finding.
   (e) DUPLICATE: a new row that asserts what an existing row already asserts through the same door is a finding --
   name the existing row with file:line.
   (f) As before: a pin on role text, on the source of a script, on a measured constant, a receipt per DoD key / edge /
   mutation, a negative control inside a test (the table «не пишется» of `docs/TESTING.md`); more test lines than
   product lines (`docs/TESTING.md` «Бюджет / Объём») with no reason named -- the finding is the missing `tests-over:`
   line; a subprocess per check where one world per file would do. A missing PIN -- on text, source, a constant, one per
   DoD key -- is still NOT a finding: (c) asks for rows on behaviour at a door, never for pins or receipts.
   (g) A NEW TEST FILE is judged by the goal of `docs/TESTING.md` «Бюджет / Файлы» (run time, upkeep, no file per
   script instead of a story): a finding when the case fits an existing story, joint or table without making that file
   slower or wider in meaning, or when the new file runs over 10 s, builds its world more than once or holds more than
   one parameterised table (plus junction rows); a package file with no keep row, or a keep row whose layer/why does not
   hold -- finding. The layers (`ai-packages/qa-factory/scripts/tests/test-layers.json`, spec
   `docs/tasks/specs/td-15-scenarios-quarantine.md`): an edit to a quarantined file without a `quarantine-edit:` reason
   that holds -- finding; a phase-2 move whose replacement does not catch the detector's class -- finding.
```

What «A missing pin is NOT a finding» still protects: the owner's word 10.11 against receipts and pins; it no longer
shields a missing behaviour row. Invariant: (c) never reads as «a test per line or per function»; a finding under (c)
names the DOOR; (g) never reads as «a new file needs a word» — it judges the goal.

### 3.2 «The two layers» (`critic-diff-brief.md:8-21`) (stream S-A1)

- Mechanical layer, `:11` after «the DoD run tails (the scope: `plans/builder-rules.md` 7b);» insert «for a defect item,
  the `red-before:` line (`docs/TESTING.md` «Тест может упасть»);». The clause «no mutation list (retired 10.11.2026,
  `docs/TESTING.md`)» stays. `:14-15` «A layer not attached is returned to the dispatcher as a request, never executed by
  the critic.» -> append « The probe below is not a builder's layer: it is the critic's own bounded run (CLAUDE.md
  rule 3).»
- Verdict layer, `:16-21` -> two bullets:

```
- **Verdict layer** — the critic's own zone: architecture, semantics, class-wide completeness, the
  edges' error direction, the tests' killing power, and the standing questions below. A cheap
  control re-run of what is attached (ONE small fast test file the verdict depends on, or one guard
  selftest) is legitimate; `test_story_step.py`, `test_story_run_*.py`, full `selftest.py`, docker,
  ratchets and quarantined files are not — they are the batch canon's (D-0056); a mutation suite is
  nobody's (retired 10.11.2026); re-deriving the mechanics by reading everything is not.
- **The probe** (the owner's word 17.11.2026: fix it, without going back to a pile of mutants): on a
  diff with NEW behaviour, break 1 to 3 places of it — your choice, the load-bearing ones (a comparison
  flipped, a branch dropped, a refusal turned into a pass, the safe default returned). Hard cap: 3 mutant
  runs per verdict, invalid ones included. The ONE road is the runner, by Bash, never Write or Edit:
  `python -B <tree>/ai-packages/qa-factory/scripts/tests/mutate_once.py --root <tree> --id <name>
  --target <path> --old "<text>" --new "<text>" --test <path> [--pytest]` — <tree> is the node's
  worktree the dispatch names; paths are relative to it; `--pytest` for a `tools/` test. The runner
  checks the anchor, compiles the mutated file, runs ONLY the narrow test file the spec's `test:` line
  names (no line: the narrowest file of the builder's witness) with a 60 s timeout, restores the file
  from its byte copy whatever happened, compares sha256 and prints `outcome: killed | survived | invalid
  | restore-mismatch`. Never a slow (`SLOW_TESTS`, `test_story_run_*`, `test_story_step.py`),
  quarantined or canon file; never the root checkout or another session's tree; no copy, edit or
  restore by hand. Before the first mutant, the same narrow file must have run GREEN in the same tree
  as your control re-run (its command in `trail.reruns`): a red baseline makes every kill false. A
  kill whose printed FAIL line is an import or collection error is invalid, not a kill. Every runner
  call goes into `trail.reruns` (command and output tail) and into the verdict block's `mutants`
  (place, change, run, outcome, the row that killed it); a survivor is a finding under question 5 (a)
  unless it is equivalent — then say why. No probe (a docs-only or plan gate, no new behaviour, the
  narrow test slow or quarantined, no tree named by the dispatch, the control run red): `mutants: []`
  and `mutants_none: "<why>"`. `outcome: restore-mismatch` is a blocker of your own verdict: name the
  file and stop probing.
```

Edges of the probe (each with its invariant):
- E-P1 docs-only diff / plan gate: no probe, `mutants_none`. Invariant: a critic never mutates a doc (the doc witness's
  own negative control, CLAUDE.md rule 11 (iii), is the can-fail proof there).
- E-P2 diff with no new behaviour: no probe; `mutants_none: "no new behaviour: <why>"`. Invariant: the probe never
  becomes a regression sweep of old behaviour.
- E-P3 narrow test slow or quarantined: no probe; the gap NAMED. Invariant: the critic never runs a canon file; an
  unproven can-fail is said, never counted as proven.
- E-P4 a run fails or hangs: the runner's own `finally` restores; its timeout is 60 s (a constant of the runner, §5.3; 7b's
  «до минуты» is a criterion of narrowness, not a timeout); a timeout is `invalid` and counts toward the cap. Invariant:
  the reviewed tree is byte-identical after the critic; no shell choreography exists to go wrong.
- E-P5 `restore-mismatch` (runner exit 2): blocker of own verdict, probing stops; the coordinator restores the file from
  the branch before any merge. Invariant: no merge carries a probe's bytes.
- E-P6 one verdict over several nodes: the cap stays per verdict (L-3).
- E-P7 the worktree is the reviewed branch: the critic starts after the builder's handback (as today).
- E-P8 no tree named by the dispatch (the worktree removed, a review after merge): no probe, `mutants_none: "no tree named
  by the dispatch"`. Invariant: no hand-built scratch copy is ever made (one road; fork F-B).
- E-P9 the control run is red: no probe, `mutants_none: "control run red: <file>"`, and the red itself is a finding
  under q5. Invariant: a kill on a red baseline is never reported.

### 3.3 `.claude/agents/critic.md` (stream S-B; Lead commits; mechanism path)

- Rule 17, `:141-143` the clause «fields verdict (fit / fit_with_fixes / blocker), blockers, class_completeness, trail
  (read + reruns)» -> append «, mutants (the probes of docs/tasks/critic-diff-brief.md «The two layers», each run in
  trail.reruns) or, when there was no probe, mutants_none with its reason». No number (F8). Anchored on that text; if
  everything-in-piles D has added `remarks` there first, insert after its clause. The opener line «17. Your verdict MUST
  end with a fenced ```json block carrying the» stays byte-identical (`install_parity_anchors.json:162`).
- Rule 20, `:173-174` «(the rule text is docs/TESTING.md «Бюджет»)» -> «(the rule texts are docs/TESTING.md «Бюджет»,
  «Откуда берётся ожидаемое значение» and «Тест может упасть»; the probe of «The two layers» answers under this line)».
- No new rule number (spec-facts-by-code L takes 21). Exam: `PROCESS/CRITIC_EXAM.md` absent (P14) -> commit message
  «Deviation: exam not run; debt F3-1».

### 3.4 The critic's own run: CLAUDE.md rule 3, R11-h, `handoff_gate` docstring (stream S-B; B1 -> (a); overrides L-9 for this clause only)

Exact texts:
- CLAUDE.md rule 3, `:80`, after «a layer not attached → critic asks the dispatcher for it and does not execute it.»
  insert: « The critic's one run of its own is the bounded probe of `docs/tasks/critic-diff-brief.md` «The two layers»,
  through `ai-packages/qa-factory/scripts/tests/mutate_once.py`, by Bash, never Write/Edit.» (~200 B; the anchor
  «TWO-LAYER CRITIC ENTRY» untouched.)
- CLAUDE.md R11-h, `:237`, inside the duty cell, after «`tools/handoff_gate.py` lets it write only that file» (anchor
  `install_parity_anchors.json:62`, kept byte-identical) append: «; a critic's probe is no write of its own: the runner
  `mutate_once.py`, run by Bash, mutates one file and restores it from a byte copy (rule 3)» (~150 B).
- `tools/handoff_gate.py` docstring, after `:8` «path of its dispatch and refuses every other Edit/Write.» insert (ASCII):
  «Bash is not gated here. A critic's one sanctioned Bash write is the probe of docs/tasks/critic-diff-brief.md "The two
  layers" (CLAUDE.md rule 3): ai-packages/qa-factory/scripts/tests/mutate_once.py mutates one file and restores it from
  a byte copy with a sha256 check; any other write by a reading role, by any tool, stays outside its rules.» Docstring
  only; no code line changes (live hook: builder hands it STAGED, the Lead commits — enforcement-file review rule).
- AGENTS.md regenerated (builder-rules 17).

Invariant: one road for a probe — the runner; every text that describes the probe points at the runner and no text
describes a hand-built copy/mutate/restore (the landing grep of S-B: `copy, mutate|byte copy of the file BEFORE` over
the brief, TESTING, critic.md, CLAUDE.md -> 0 hits; positive control: the same call finds «byte copy» in
`handoff_gate.py`'s new line). Edge: boot bytes grow ~350 B on a CLAUDE.md already over its WARN (`tools/session_context.py`
BOOT_WARN/BREACH, `:193-212`); accepted by the Lead (B1 -> (a)), the session_context code unchanged.

---

## §4 D5 and the stale texts

### 4.1 New test file — the goal decides (the owner's word 17.11.2026; one home: TESTING «Бюджет / Файлы»)

The owner, 17.11.2026, on O-1: «не хочу что бы написание тестов зависило от моего слова. Какая была цель у сокращения
количества файлов? Вот этой цели и надо придерживаться когда решаем нужен отдельный фаил или нет». So: no owner's word
for a new test file, no blanket ban; the rule states the goal as TESTING.md measures it (`docs/TESTING.md:26-29`) and the
choice is made by that goal. O-2 (a new forge tool's own test file) is an instance of this rule, not an exception.

Replacement text (S-A1) for `docs/TESTING.md:117` (the first sentence of «Файлы») and for `:124-127` (the offload-only
exception, removed); `:118-123` (ticket-named files, split parts) stay:

```
- **Файлы**: решает цель, а не запрет и не слово владельца (слово владельца 17.11.2026: «не хочу что бы написание
  тестов зависило от моего слова. Какая была цель у сокращения количества файлов? Вот этой цели и надо придерживаться
  когда решаем нужен отдельный фаил или нет»). Цель — та, что меряет «Замер» выше: время прогона (файлы дольше 10 с),
  уход (правки тестовых файлов в коммитах, где не менялись ни код, ни текст правил) и файл на скрипт вместо истории.
  Поэтому случай по умолчанию — строка в существующую историю, стык или таблицу своего слоя. Новый файл верен, когда
  случай не ложится ни в одну из них, не сделав тот файл медленнее или шире по смыслу; новый файл укладывается в 10 с,
  строит мир один раз и держит одну параметризованную таблицу (и строки стыков). Место называет дизайнер в строке
  `test:` DoD («Строка теста в DoD»); выбор судит критик (вопрос 5 `docs/tasks/critic-diff-brief.md`). Строка `keep` в
  `test-layers.json` — учёт файла пакета (без неё канон красит `unlisted:`), а не разрешение его создать; у тестов
  форджа строки `keep` нет. Свой файл `tools/test_<x>.py` у нового инструмента форджа `tools/<x>.py` — случай этого же
  правила, не исключение.
```

builder-rules 7d (S-A2), `:90-93` from «новый тестовый файл не создаётся: случай — строка» through «не дольше 10 с;» ->
«новый тестовый файл — по цели `docs/TESTING.md` «Бюджет / Файлы» (по умолчанию случай — строка `variants.json` истории
`scripts/tests/fixtures/stories/<id>/` или строка таблицы/стыка своего слоя; место называет строка `test:` DoD; новый
файл пакета учитывается строкой `keep` в `scripts/tests/test-layers.json`, её слой и причину судит критик);». After both
edits TESTING and 7d say the same: the goal decides, the `test:` line places, keep is bookkeeping, 10 s lives in TESTING.

`.claude/agents/builder.md:51-52` (S-B) «and no new test file is written without a keep row (7d).» -> «and a new test file
is written only where the DoD's `test:` line places it (docs/TESTING.md «Бюджет / Файлы»; a package file gets its keep
row).»

`.claude/agents/designer.md` rule 1 (`:21-23`, S-B) «a DoD never asks for a new test file outside the keep rows of
`test-layers.json`; a new case is a variant/table row.» -> «a DoD names the place of every new case on its `test:` line
(`docs/TESTING.md` «Строка теста в DoD»): a variant/table row by default, a new file only by the goal of
`docs/TESTING.md` «Бюджет / Файлы».»

Brief q5 (g): §3.1. TESTING «Кто что делает»: §2.4. Invariant: no text left says «a new file needs the owner's word» or
«no new file, ever»; the run-time and one-world criteria stay (they ARE the goal). Edge: a case that fits an existing file
only by making it slower or wider -> a new file is the right answer and the critic's (g) must not flag it; a new file
over 10 s -> the builder reports the measured time and returns a question (never silently splits or drops rows).

### 4.2 Stale conditional in 7b (`plans/builder-rules.md:44-53`) (S-A2)

From «Пока перевод в карантин не выполнен (в `test-layers.json` нет строк `quarantine`), к напечатанному добавляется
прежний объём:» through «и ключи своего DoD;» -> «К напечатанному добавляются только файлы, которые называют строки
`test:` DoD узла (путь вне пакета — тестовый файл, который его судит, правило 4 `CLAUDE.md`); тронут
`story_run_common.py` — в отчёте строка «тронут story_run_common.py» (все `test_story_run_*.py` судит канон);». The
per-type list after it stays unconditional. TEMPORAL: that world ended (`test-layers.json:7174`). Invariant: a quarantined
file is never run; the per-type gate tests still run when their type of change happens.

### 4.3 Doc-dispatch negative control (7d `:89`) (S-A2)

«Свидетель наличия ключей в тексте — вывод в отчёте, в репозиторий не коммитится.» -> «Свидетель наличия ключей в
тексте — по правилу 11 `CLAUDE.md` «DOC-DISPATCH WITNESS» (ключи дословно из DoD, скрипт целиком в отчёте,
отрицательный контроль), в репозиторий не коммитится.» Also append to 7d's first sentence after «читается до первого
теста»: «; ожидаемое значение — «Откуда берётся ожидаемое значение» там же».

### 4.4 Stale «канон судит мутации» (S-A2 after boot-by-topic S2; L-5 (a))

| Carrier | Text after S2 (expected) | New text (S-A2) |
|---|---|---|
| builder-rules 7b `:57-59` | «**Мутации** билдер не прогоняет и не перечисляет: мутации судит канон пачки (слово владельца 28.10 и 10.11.2026).» | «**Набор мутаций** билдер не прогоняет и не перечисляет (слово владельца 28.10 и 10.11.2026), и канон пачки его не гоняет; проба «тест может упасть» у билдера одна — строка дефекта, красная до правки (`docs/TESTING.md` «Тест может упасть», слово владельца 17.11.2026).» |
| builder-rules 16 (б) `:120` «перепрогон после каждой правки — нарушение; мутации билдер не гоняет (п. 7b)» (F9) | unchanged by S2 | «перепрогон после каждой правки — нарушение; набор мутаций билдер не гоняет (п. 7b), а единственный прогон сверх свидетеля — `red-before:` на пункт-дефект (`docs/TESTING.md` «Тест может упасть»)» |
| RUNBOOK `:115` | «Мутации судит канон пачки (`plans/builder-rules.md` п. 7b).» | «Мутаций канон не гоняет: что тест может упасть, показывают билдер (строка дефекта красная до правки) и критик (проба) — `docs/TESTING.md` «Тест может упасть».» (no number, F8) |
| PROJECT.md п. 13 `:364` | S2 makes it a pointer; the dispatcher sentence «…или гонять мутации…» stays true | not owned by S-A2: if the landing grep finds a mutation-canon claim in PROJECT.md after S2, S-A2 stops and returns it as a question |
| brief `:19-20` | — | S-A1 (§3.2) |
| calibration 13(j) `:377-378` | — | S-B: «a docker run or a mutation SUITE is the leak — the first are the batch canon's, the last nobody's (a builder's one `red-before:` run of a defect row and a critic's probe through `mutate_once.py` are not a suite, `docs/TESTING.md` «Тест может упасть»)» |
| TESTING `:95` receipt row «каждую мутацию» | unchanged (true) | |

S2's K-check 13-f expects «7b holds «мутации судит канон пачки»» — true until S-A2, which follows S2 (§8).
Landing check (S-A2 DoD key): Grep `судит канон пачки|their judge is the canon|batch canon's.*mutation|мутации судит|[Мм]утации судит|их судит канон` -i over CLAUDE.md, PROJECT.md,
docs/*.md, docs/tasks/critic-diff-brief.md, plans/builder-rules.md, PROCESS/*.md -> 0 hits for a mutation claim
(positive control: the same call finds «судит канон пачки» in 7b's slow-files sentence, which stays; the `[Мм]` class
because a case-insensitive grep may not fold Cyrillic, t-949 K1).

### 4.5 The S-A1 -> S-A2 window: the accepted TEMPORAL edge (B2)

World between S-A1's merge and S-A2's merge: TESTING «Тест может упасть» says the canon runs no mutation suite, while 7b
`:57-59`, RUNBOOK `:115` (and PROJECT п. 13 until S2) still say «мутации судит канон пачки»; 7d still says «новый тестовый
файл не создаётся … файл у нового скрипта — только со строкой keep … не дольше 10 с» while TESTING says the goal decides;
16 (б) has no `red-before:` clause. Invariants kept in both worlds: nobody runs a suite (7b forbids the builder one, the
canon has none — P4, the probe is capped); a builder who reads 7d's stricter text and meets a `test:` line placing a new
file returns a question — the safe direction, never a file in the wrong place; a `red-before:` run is named a duty by
TESTING and by builder.md rule 8 (S-B), so 16 (б) cannot be read as forbidding it. The window closes at S-A2, whose DoD
runs the §4.4 landing grep. If S2 has not landed when this spec's other streams are done, the window stays open and
the batch's «Ход» says so.

---

## §5 Code (D6)

### 5.1 S-C: the `test:` line gate (`tools/dispatch_manifest.py`, `tools/dispatch_new.py`)

Owner served: DATA (presence and form); sufficiency and source are the critic's (q5). Behaviour:
1. `test_lines(cut) -> list[(line_index, where, source)]`: every UNQUOTED line of the cut (fenced and blockquote lines
   never count) matching: optional bullet, optional `**`, optional one pair of surrounding backticks, the key `test:`
   (case-insensitive), a non-empty WHERE, the FIRST `| expected from:` (case-insensitive), a non-empty SOURCE. WHERE
   `none` must be followed by `--`/`—` and a reason holding a word character (`_NONE_ANSWER_RE`). The header grammar does
   NOT gain `test`; `KEY_GROUPS` and `ITEMS` unchanged (`test_dispatch_manifest.py:1268-1269` stays green).
2. In `check_cut`, after the item loop (`:927-943`) and before the skip lines: for `is_builder` and
   `max(designer_threshold(cut)) >= DESIGNER_THRESHOLD`, no well-formed line -> `missing["test"] = "no line" |
   "ill-formed: <first bad line, cut at 80 chars>"`. Not checked under the threshold, for non-builder kinds, or on a
   degraded cut.
3. ONE token (F3): the item, its display name and its skip word are all `test` (the line's own key). New
   `SKIP_ONLY_ITEMS = ("test",)`, `_DISPLAY["test"] = "test"` (or `_DISPLAY` built over `ITEMS + SKIP_ONLY_ITEMS`).
4. The iteration sites that must read `ITEMS + SKIP_ONLY_ITEMS` (F4; each named, none left on `ITEMS` alone, else the key
   is set in `missing` and then dropped — a silent pass, FR-4 — or `_items_text` raises KeyError):
   - `_parse_skip_line` `:271` (`if name not in ITEMS` -> unknown item);
   - `SKIP_REFUSED_TEMPLATE` `:146` (the listed items);
   - the skip loop's `newly` `:953`;
   - `still` `:961`;
   - `_items_text` `:902-903` (`_DISPLAY`) and the INCOMPLETE hint: `_FORM_HINTS["test"]` = «(over the designer
     threshold: one line per behaviour item inside the DoD, `test: <file::table> | expected from: <spec §, rule,
     owner's word>` or `test: none -- <why> | expected from: <source>`; the form: docs/TESTING.md «Строка теста в DoD»)»,
     and `_expected_forms()` (`:128-136`) if it is built over `ITEMS`.
   S-C's report lists each site with its line after the edit.
5. Door: `manifest-skip: test -- <reason>`; the skip note as for other items.
6. Switch `TEST_LINE_REFUSES = True` — final (L-2; the owner's «ок» on O-3, 17.11.2026). False -> reported as a note.
7. `dispatch_new.py`: `--test "<where> | expected from: <source>"` repeatable; each printed as `test: <value>` on its own
   line right after the `DoD:` line; the existing newline/backtick and empty-item refusals apply.

Error direction (a presence detector promoted to a gate): it may FALSE-PASS (one line present while other behaviour
items lack one; a nonsense source) — accepted, critic q5 catches; it must NOT falsely refuse, and these inputs stay on
the PASS side when one well-formed line exists: the line under `siblings:` or after the last header; a bulleted / bold /
backticked key; CRLF line ends; a `|` inside WHERE before the first `| expected from:`; `Expected From:` in any case;
`manifest-skip: test -- <reason>`; `manifest-skip: TEST -- <reason>` (lower-cased like the other items). These stay
REFUSED (over the threshold, no other line): a `test:` line only inside a fence or blockquote; `test: none | expected
from: x`; `test: tools/x.py` with no source; an empty source; prose `Test row: ...`; `manifest-skip: test` with no
reason (SKIP REFUSED); `manifest-skip: tests -- <reason>` (unknown item — the refusal lists `test`, so the door is
copyable).

Edges (each with its invariant):
- E-C1 a resubmission (`designer: resubmission t-NNN`) whose spec predates the rule; and E-C4 (F12) the FIRST dispatch
  of any stream of a spec accepted before S-C lands (in flight 17.11: boot-by-topic S2, everything-in-piles r3,
  spec-facts S2, architect-tier, rules-debt phase 2, dry-story finish): refused like any; door `manifest-skip: test --
  spec accepted before the test line (<spec path>)`. Check «Forge test discipline» (a) counts this reason as its own
  class; that reason on a spec accepted after S-C's merge date is a finding. Invariant: no over-threshold builder dispatch
  goes out silent about its tests; the transition costs one line, never a refusal with no door.
- E-C2 TEMPORAL: the hint names a TESTING section -> S-C merges after S-A1 (§8). Before S-C: nothing is checked (the
  rule text binds, critic q5 judges); after: checked.
- E-C3 every existing over-threshold builder prompt asserting exit 0 in the owned test files gains a `test:` line (never
  a weakened check); the report lists each changed case.

Tests (rows in existing tables, no new file): `tools/test_dispatch_manifest.py` one parameterised table «test line» over
the pass/refuse inputs above (ids name the case; expected exit and missing label from this section);
`tools/test_dispatch_new.py` one row `--test` printed under DoD + one row over threshold without `--test` refused.

### 5.2 S-D: the verdict's mutants (`tools/critic_verdict_check.py`, the schema)

After everything-in-piles stream C (same three files, its `remarks`; re-read C's landed text at dispatch, t-949 K4). New
helper `_mutant_errors(obj)` called from `validate_verdict`; the schema mirrors it. The cap number lives here as DATA and
in the brief as the rule (F8).
- `mutants`: REQUIRED array (L-4), 0-3 items; > 3 -> `field 'mutants' has N items: at most 3 (the cap of
  docs/tasks/critic-diff-brief.md, The two layers)`.
- item: `place` (1-300 chars), `change` (1-300), `run` (1-500), `outcome` (one of `killed`, `survived`, `invalid`,
  `restore-mismatch` — the runner's own words, §5.3), `killed_by` (1-300 string, REQUIRED exactly when `outcome` is
  `killed`, else absent or null).
- the run join (F2): `run` equals the `command` of one `trail.reruns` item; that command contains `mutate_once.py`; the
  `run` values of the items are pairwise DISTINCT (the runner's argv names the mutant by `--id`, so two mutants never
  share a command); the joined item's `result` contains `outcome: <outcome>`. Three probes can no longer join to the one
  ordinary control rerun.
- the green control (fork F-A, recommended): `mutants` non-empty -> at least one `trail.reruns` item whose command does
  NOT contain `mutate_once.py`.
- `survived`: exactly one of `equivalent` (non-empty reason) or `remark` (the id of a `remarks` item with disposition
  `fix`, C's vocabulary); neither -> error. `invalid`: nothing more (it counts toward the cap). `restore-mismatch`:
  requires `verdict` = `blocker`.
- `mutants: []` requires `mutants_none` (a string holding a word character); `mutants_none` with a non-empty `mutants` ->
  error.
- An old verdict (no `mutants`) fails with (F13) `missing required field: mutants (a verdict written before this field
  existed passes acceptance only by the line "verdict: <node> none -- verdict predates a required field (mutants)")`.
  Diagnostics ASCII.
Error direction: shape and joins only; it may FALSE-PASS a fabricated kill (a run and a result typed to match) — caught by
check (b)'s transcript count and trail reading; it never judges whether a mutant was load-bearing or equivalent (P27).
Dependency (F13): this check is on an execution path only after everything-in-piles A2 lands (that spec's P31: today the
critic self-runs the checker, critic.md rule 17, and the coordinator runs it by hand); until then M3 (d) is discipline +
check (b). Amendment line for everything-in-piles (named here, written there by its owner, fork F-D): C `:246-247` and A2
`:307-309` say «verdict predates remarks» -> field-generic «verdict predates a required field (<name>)».
Tests: rows in `tools/test_critic_verdict_check.py`'s existing tables: valid 0/1/3 probes; 4 probes; survivor without
equivalent/remark; killed without killed_by; run not in trail; two mutants with one run; run without `mutate_once.py`;
result without the outcome word; probes with no control rerun; empty without reason; reason with probes;
restore-mismatch in a non-blocker verdict; old verdict -> the door text.

### 5.3 S-E: the probe runner `ai-packages/qa-factory/scripts/tests/mutate_once.py` (F1; the ONE road for a probe)

Interface (the spec-file form stays for back-compat):
- `python -B mutate_once.py <spec.json> <mutation id>` — as today, paths under `scripts/` (default root = `SCRIPTS`).
- `python -B mutate_once.py --root <dir> --id <name> --target <path> --old <text> --new <text> --test <path> [--pytest]`
  — the inline form: no file is written to describe a mutant (a critic may write only its report, R11-h); `<path>`s are
  relative to `--root`; `--id` names the mutant in the command (F2).
- `--root <dir>` is accepted by both forms (spec-file form: paths relative to it instead of `SCRIPTS`).
- Run: `--pytest` -> `[sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", <root>/<test>]`, else
  `[sys.executable, "-B", <root>/<test>]`; `cwd=<root>` when `--root` is given, unchanged otherwise; timeout
  `TIMEOUT_S = 60` (module constant).
- Before touching: the target and test resolve inside `--root` (resolved paths), the test file exists, the target decodes
  as UTF-8, `--old` is non-empty and occurs exactly once, `--new` differs from `--old`; for a `.py` target the mutated
  text is `compile()`d — a SyntaxError is `invalid` WITHOUT touching the file.
- Then: byte copy, write, run, restore in `finally` (timeout included), sha256 before/after.

Outcomes (exit code, last printed line `outcome: <word>`); expected values of the tests come from this table:

| Case | Exit | outcome |
|---|---|---|
| any pre-touch refusal (outside root, test absent, non-UTF-8 target, empty `--old`, `--old` == `--new`, anchor found 0 or 2+ times, bad arguments) | 64 | none printed; the message says what is wrong, what is expected, which argument fixes it; nothing touched |
| mutated `.py` target does not compile | 3 | invalid (nothing touched) |
| sha256 after != before | 2 | restore-mismatch (wins over every other outcome) |
| timeout | 3 | invalid |
| script form: non-zero exit with a `=== ` summary line and >= 1 `FAIL` line | 0 | killed |
| script form: non-zero exit with no `=== ` summary line, or with no `FAIL` line | 3 | invalid |
| pytest form: exit 1 and the summary counts >= 1 `failed` | 0 | killed |
| pytest form: exit 1 with errors only, or exit 2, 3, 4, 5 (collection error, internal, usage, no tests) | 3 | invalid |
| exit 0 (either form) | 1 | survived |

The runner prints, as today, the test's last summary line and the first 3 FAIL lines, then the sha line, then
`outcome:`.

Error direction (a builder's witness helper promoted to evidence a verdict and its checker rely on, designer rule 1): it
may err toward `invalid` or `survived` (a real kill reported as invalid costs one probe slot; a test file that prints no
`=== ` line yields invalid), NEVER toward `killed` for a mutant that did not fail an assertion. Adversarial inputs that
must stay NON-killed (each a table row): a mutant with a SyntaxError (compile -> invalid, untouched); a mutant that breaks
the import of the module the test imports at top (pytest exit 2 -> invalid); a mutant that loops forever (timeout ->
invalid, file restored); a wrong test path (64, untouched); a test file with no tests (pytest 5 -> invalid); a script that
crashes before its summary (invalid). Residual named, left to judgment: a mutant that imports cleanly but raises when a
test imports it lazily inside a test function is reported by pytest as a failure -> `killed`; the critic reads the
printed FAIL lines and records it `invalid` (brief §3.2) — no exception-name list in code (AR-1, FR-12).

Edges (each with its invariant):
- E-R1 restore always (finally; timeout raised inside the try). Invariant: the target is byte-identical after any run;
  exit 2 when not.
- E-R2 CRLF / BOM targets: read as bytes, decoded and re-encoded without newline translation. Invariant: an unmutated
  byte never changes.
- E-R3 a child process left alive by the test after the timeout is the test's own defect (a subprocess per check); the
  runner kills its direct child only. Invariant: the restore does not wait for it.
- E-R4 no `--root` (spec-file form) behaves as today except: exit 3 for invalid cases where today a crash counted as a
  kill. Readers of the exit: none (Grep `mutate_once` over `tools/` 0, `.githooks` 0, `.claude/settings.json` 0; only
  historical batch texts name it).
- E-R5 the runner never decides the cap: each call is one mutant; counting is the critic's and check (b)'s.
- E-R6 TEMPORAL: the keep row that makes `--witness-for` print the new test is created by S-E itself; the witness is run
  AFTER adding it. Before: «no scenario or keep row covers» (P23).

Test place (by the goal rule §4.1, named here as the designer's duty): no story, joint or table touches the runner (P17);
a scenario row would widen a factory-stage story with a forge tool's mechanics. So a NEW file
`ai-packages/qa-factory/scripts/tests/test_mutate_once.py`: one parameterised table over the outcome table and the
adversarial list (tiny target/test files in a temp dir, `main()` called in-process, `TIMEOUT_S` patched to 1 s for the
timeout row), plus the back-compat spec-file row; keep row `layer: table`, `covers: ["tests/mutate_once.py"]`. Under 10 s
— estimate, not measured (about 16 rows, the pytest rows ~1 s each); the builder reports the measured time, and over
10 s returns a question.

---

## §6 Cost of D4, measured (Grep tool, 17.11.2026; numbers with their command)

| Spec (recent, accepted) | lines `rg -c "^"` | numbered items `rg -c "^\s*\d+\. "` | single `Item:`/`Items:` headers | lines already naming a test | upper bound of added lines |
|---|---|---|---|---|---|
| `20261116-fg7-5-node-cost-with-rework-spec.md` | 486 | 13 (6 grouping rules, 4 analog notes) | 0 | 2 (+ §5, a 41-line test table) | 4 (T1-T4) = 0.8 % |
| `20261117-rules-debt-fix-spec.md` | 612 | 12 | 7 | 8 | 16 = 2.6 % |
| `20261116-spec-facts-by-code-spec.md` | 867 | 23 | 0 | 2 | 23 = 2.7 % |

Upper bound: 43 lines on 1,965 (2.2 %) (t-949 K1: arithmetic checked). What it removes, re-cut by reading (§6.1): 7
firm and 2 border of 70 `failure_class: spec` rejections are the class the line targets; each cost a fix round (a fresh
builder + a critic re-review, CLAUDE.md rule 12). L-2's rationale on this count: the leak is real and recurring (7-9
fix rounds in six days, three of them the same quarantine miss), and the generator prints the line; L-2 = True is final
in any case by the owner's «ок» on O-3. Estimate, not measured: the share the line would have prevented; check (d)
measures it. Critic probe cost: at most the brief's cap of runner calls per verdict, each bounded by the runner's 60 s
timeout (estimate of real time not measured; check (b) records counts). Builder: one narrow run per defect item.

### 6.1 The baseline re-cut (F6), read line by line from `logs/journal/dev1.jsonl` (the 27 regex hits)

- In class (7): t-054 (E5 product-row repeat unpinned, «the spec let the builder skip it»); t-133 (dispatch did not name
  the quarantine list, node tests written into quarantined files); t-134 (pins in a quarantined file, same miss, third
  recurrence); t-420 (the DoD sent the rows to a quarantined test file); t-502 (four stop-record rows re-pinned to the new
  output while the edge was open — an expected value from the code); t-646 (spec K7 kept a test «green and unedited»
  against spec 3.4 — a keep with no named value, §2.1); t-654 (the window test not named).
- Border (2): t-047 (M4 «shadow untested» among edge silences); t-057 (R2 the re-read's source:default unpinned, next to
  an owns miss).
- Out of class (18), why: t-056 negative control inside a test (retired pin regime); t-113 reader fixtures given to nobody
  (readers class, spec-facts); t-159 stale text pin; t-325 selftest's no-hooklib rule; t-336 red on tree after a merge,
  shapes missed; t-427 and t-439 canon reds of the t-420 incident (one defect, counted once under t-420); t-442 frozen
  pin of a measured constant; t-462 ratchet outside owns; t-479 keep pins outside owns (readers); t-541 the spec's own
  join edge; t-547 a placeholder a config key answers (silent edge; t-949 counted it in class — read here as the readers /
  edge class: its red test was not the node's own); t-559 a test outside owns red (readers; same disagreement with t-949);
  t-615 the critic's candidate sources; t-816 a designer draft, matches only via «dropping»; t-889 «triple pin» and t-935
  «22 duplicate tests» (duplicates: the baseline of q5 (e), 2); t-937 hook-copy sites outside owns (readers).
- Rule for check (d) from now on: the same per-line reading, never the regex count alone; a class hit whose notes carry
  no test word is outside this cut (named as a limit, estimate).

---

## §7 Streams

### 7.0 The five П1 nodes (an untaken batch of pile `forge`, L-7)

| Node | Lead direction | Streams |
|---|---|---|
| N1 oracle rule | D1 | S-A1 (§2.1), S-A2 (7d pointer), S-B (builder.md 8, critic.md 20) |
| N2 can-fail proof | D2 | S-E (runner), S-A1 (§2.3, §3.2), S-A2 (§4.4, 16 (б)), S-B (critic.md 17, §3.4, calibration 13(j)), S-D |
| N3 critic test questions | D3 | S-A1 (§3.1, §2.4) |
| N4 the `test:` line | D4, D6 | S-A1 (§2.2), S-B (designer.md 1), S-C |
| N5 contradictions, the goal-based file rule | D5 | S-A1 (§4.1 TESTING, §2.5), S-A2 (§4.1 7d, §4.2, §4.3), S-B (builder.md 4, designer.md 1) |

Witness scope for all streams: the named test files only (`scenario_walk.py --witness-for <owns>` for the package path;
the test file that judges the path outside the package, CLAUDE.md rule 4); no full `pytest tools/`, no CI wait (7b).
Every commit carries the axis block of §10.2 and `tier:` where the path is a mechanism path.

### 7.1 S-E — the probe runner (builder; package)

given: this spec §1.1, §5.3; `ai-packages/qa-factory/scripts/tests/mutate_once.py`; `ai-packages/qa-factory/scripts/tests/test-layers.json` (keep row form); `ai-packages/qa-factory/scripts/tests/scenario_walk.py:887-922`; `ai-packages/qa-factory/design/factory-rules.md` (whole); `plans/builder-rules.md`; `ai-packages/qa-factory/design/architecture.md` AR-4, AR-7, AR-9, AR-29; `tools/architecture_gate.py:15-16, 34-38`
owns: C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/mutate_once.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_mutate_once.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test-layers.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/changelog.d/forge-N-mutate-once-probe-runner.md
non-goals: the existing `json.loads` of the spec-file form (axis 16, untouched); any other package script; a cap counter; `agent_budget.py`
handoff: C:/QAFactory/forge-repo/docs/tasks/handoffs/<task>-se-report.md
edges: §5.3 E-R1..E-R6, the outcome table, the adversarial list and its named residual
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/tests/mutate_once.py ai-packages/qa-factory/scripts/tests/test_mutate_once.py` prints `keep test_mutate_once.py` and the printed files run green; plus `python -B ai-packages/qa-factory/scripts/tests/test_console_encoding.py` (a changed script that prints, 7b), `python -B ai-packages/qa-factory/scripts/selftest.py --lang`, and the §1.1 change checks (report lines; `refusal_registry.py --check`; `test_judgment_census.py` or «судит канон пачки»); the FR pass A–G in the report
test: ai-packages/qa-factory/scripts/tests/test_mutate_once.py::outcome table (new file by «Бюджет / Файлы»: fits no story, joint or table) | expected from: this spec §5.3 outcome table, adversarial list, E-R4
siblings: axis 3 (the release copy carries it; changelog.d fragment), axis 15 (console: test_console_encoding), axis 16 (existing json.loads untouched), axis 34 (one runner for package and forge tests)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261117-forge-test-rules-spec.md

### 7.2 S-A1 — TESTING.md and the brief (builder; does not wait for boot-by-topic S2)

given: this spec §2, §3.1, §3.2, §4.1 (TESTING text); `docs/TESTING.md`, `docs/tasks/critic-diff-brief.md`, `tools/tests/test_role_carriers_one_owner.py`, `CLAUDE.md` rule 11 (DOC-DISPATCH WITNESS)
owns: C:/QAFactory/forge-repo/docs/TESTING.md
C:/QAFactory/forge-repo/docs/tasks/critic-diff-brief.md
C:/QAFactory/forge-repo/tools/tests/test_role_carriers_one_owner.py
non-goals: any code; builder-rules, RUNBOOK, PROJECT.md (S-A2 / not owned); brief questions other than 5 and the two-layers bullets
handoff: C:/QAFactory/forge-repo/docs/tasks/handoffs/<task>-sa1-report.md
edges: §2.1 edges, §2.5 sweep, §4.1 edges, §4.5 window (S-A1 opens it); anchors kept byte-identical: «## The two layers», «6. **DUPLICATION AND CONSISTENCY**», «7. **CODE QUALITY**», «12. **ONE ROAD**», OWNER keys of q7/q12, TESTING headings «Бюджет / Объём», «Бюджет / Файлы», «Как писать эффективный тест на нашем проекте»
DoD: `python -m pytest tools/tests/test_role_carriers_one_owner.py -q` green, plus the doc-dispatch witness (keys below quoted verbatim, script in full in the report, one key deliberately absent -> failure)
test: tools/tests/test_role_carriers_one_owner.py::OWNER_KEYS,POINTERS | expected from: this spec §7.2 rows
siblings: axis 31 (one owner per aspect); `owns_readers.py:26` cites brief «item 13 (d)» (spec-facts L, not this stream)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261117-forge-test-rules-spec.md

Carrier-test rows (variant rows of the existing tables): OWNER_KEYS + `("tests:oracle", "docs/TESTING.md", "тест, чьё
ожидание переписано из того, что код напечатал, может только пройти")`, `("tests:line", "docs/TESTING.md", "Пункт без
поведения (перенос текста, переименование) строки не получает")`, `("tests:files", "docs/TESTING.md", "Новый файл верен,
когда случай не ложится ни в одну из них")`, `("review:probe", BRIEF, "The ONE road is the runner, by Bash, never Write
or Edit")`; POINTERS + `("docs/TESTING.md", "`docs/tasks/critic-diff-brief.md` «The two layers»", BRIEF, "- **The
probe**")`.
Doc keys (verbatim): «### Откуда берётся ожидаемое значение», «### Строка теста в DoD», «### Тест может упасть»,
«red-before:», «(e) DUPLICATE», «A missing PIN», «- **The probe**», «Hard cap: 3 mutant runs per verdict», «mutate_once.py
--root <tree>», «решает цель, а не запрет и не слово владельца», «Строка `keep` в `test-layers.json` — учёт файла пакета»,
«калибровочная проверка «Forge test discipline»»; absent keys: «Исключение (слово владельца 14.11.2026», «новый
тестовый файл не создаётся; случай идёт», «ratchets and mutation runs are not», «1–3 места».

### 7.3 S-A2 — builder-rules and RUNBOOK (builder; after boot-by-topic S2 is merged, L-5 (a))

given: this spec §4.1 (7d text), §4.2, §4.3, §4.4, §4.5; `plans/builder-rules.md` and `docs/RUNBOOK.md` as S2 left them; `tools/tests/test_role_carriers_one_owner.py`
owns: C:/QAFactory/forge-repo/plans/builder-rules.md
C:/QAFactory/forge-repo/docs/RUNBOOK.md
C:/QAFactory/forge-repo/tools/tests/test_role_carriers_one_owner.py
non-goals: PROJECT.md (a hit there is a question back); builder-rules beyond 7b `:44-59`, 7d, 16 (б); RUNBOOK beyond `:115`
handoff: C:/QAFactory/forge-repo/docs/tasks/handoffs/<task>-sa2-report.md
edges: §4.4 landing grep with its positive control; anchors «Покрасневший пин удаляется, а не чинится», «не регрессия, не соседи, не большие файлы», RULES_7B; S2's text is the anchor base — a sentence S2 moved is located by its words, a sentence S2 removed is a question back
DoD: `python -m pytest tools/tests/test_role_carriers_one_owner.py -q` green, the §4.4 landing grep (0 mutation-canon hits, control found), plus the doc-dispatch witness on the keys below
test: tools/tests/test_role_carriers_one_owner.py::POINTERS | expected from: this spec §7.3 rows
siblings: axis 31; builder-rules 16 (б) (F9, applied); `test_quarantine.py:51` (FORGE_CARRIERS: no test file name added)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261117-forge-test-rules-spec.md

Carrier-test rows: POINTERS + `(RULES, "«Откуда берётся ожидаемое значение»", "docs/TESTING.md", "### Откуда берётся
ожидаемое значение")`, `(RULES, "`docs/TESTING.md` «Тест может упасть»", "docs/TESTING.md", "### Тест может упасть")`,
`(RULES, "по цели `docs/TESTING.md` «Бюджет / Файлы»", "docs/TESTING.md", "- **Файлы**")`.
Doc keys (verbatim): «К напечатанному добавляются только файлы, которые называют строки», «отрицательный контроль), в
репозиторий не коммитится», «**Набор мутаций** билдер не прогоняет», «единственный прогон сверх свидетеля — `red-before:`»,
«Мутаций канон не гоняет»; absent keys: «Пока перевод в карантин не выполнен», «мутации судит канон пачки», «Мутации судит
канон пачки», «файл у нового скрипта — только со строкой `keep`».

### 7.4 S-B — role files, CLAUDE.md, handoff_gate docstring, calibration, map (builder edits, leaves STAGED; Lead commits with the axis block and `tier:`)

given: this spec §3.3, §3.4, §4.1 (builder.md, designer.md), §9, §10; the files below; `tools/install_parity_anchors.json`; `tools/test_handoff_rule_anchors.py`
owns: C:/QAFactory/forge-repo/.claude/agents/critic.md
C:/QAFactory/forge-repo/.claude/agents/builder.md
C:/QAFactory/forge-repo/.claude/agents/designer.md
C:/QAFactory/forge-repo/CLAUDE.md
C:/QAFactory/forge-repo/tools/handoff_gate.py
C:/QAFactory/forge-repo/PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md
C:/QAFactory/forge-repo/docs/SIBLING_MAP.md
non-goals: rule numbers; any rule opener line; CLAUDE.md beyond the rule 3 clause and the R11-h cell (no rule 11 pointer, L-9 (b) stands); any code line of `handoff_gate.py`; PROJECT.md
handoff: C:/QAFactory/forge-repo/docs/tasks/handoffs/<task>-sb-report.md
edges: rule openers and anchors byte-identical (`install_parity.py --check` MISSING (0); anchors `:23`, `:62`); critic.md rule 17 lands in the SAME merge as S-D (E-T1); exam deviation line (P14); §3.4 one-road grep; calibration check number = next free at landing (49 is architect-tier's; the TESTING text names the title, not the number)
DoD: `python -m pytest tools/tests/test_role_carriers_one_owner.py tools/test_handoff_rule_anchors.py tools/test_handoff_gate.py -q` and `python -B tools/install_parity.py --check` (MISSING (0)) and `python -B tools/agents_md.py --check`, plus the doc-dispatch witness on the keys of §3.3, §3.4, §9, §10
test: none -- role, policy and process texts and a docstring; doc-dispatch witness (CLAUDE.md rule 11) | expected from: this spec §3.3, §3.4, §4.1, §9, §10
siblings: axis 1 (policy <-> role files), axis 2 (critic exam absent: debt F3-1), axis 31 (SIBLING_MAP row for TESTING.md)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261117-forge-test-rules-spec.md

Texts: critic.md §3.3; CLAUDE.md and handoff_gate §3.4; builder.md rule 4 §4.1 and rule 8 (append «The expected value
of a test and the red-before run of a defect row: TESTING.md «Откуда берётся ожидаемое значение», «Тест может упасть».»);
designer.md rule 1 §4.1; calibration §9 and 13(j) §4.4; SIBLING_MAP axis 31: intro list gains «`docs/TESTING.md` (which
tests, the expected value's source, the `test:` line, the new-file goal, the builder's can-fail step)», table row
`| docs/TESTING.md | builder, critic, designer | which tests; expected value; the test: line; new-file goal; red-before |
owner; scope -> builder-rules 7b; the critic's probe -> the brief |`, brief row aspect «the two layers' content (the probe,
its runner and its cap included)».

### 7.5 S-C — test line gate (builder; `dispatch_manifest.py` left STAGED, Lead commits)

given: this spec §5.1; `tools/dispatch_manifest.py`, `tools/dispatch_new.py`, `tools/dispatch_gate.py` (`decide_full`, read), the four test files
owns: C:/QAFactory/forge-repo/tools/dispatch_manifest.py
C:/QAFactory/forge-repo/tools/dispatch_new.py
C:/QAFactory/forge-repo/tools/test_dispatch_manifest.py
C:/QAFactory/forge-repo/tools/test_dispatch_new.py
C:/QAFactory/forge-repo/tools/test_dispatch_gate.py
C:/QAFactory/forge-repo/tools/test_dispatch_gate_md.py
non-goals: the header grammar, `KEY_GROUPS`, `ITEMS`; `dispatch_gate.py` code; spec-facts S2's READERS NOTE (its own node, §8)
handoff: C:/QAFactory/forge-repo/docs/tasks/handoffs/<task>-sc-report.md
edges: §5.1 E-C1..E-C4, the iteration sites of item 4, the adversarial list
DoD: `python -m pytest tools/test_dispatch_manifest.py tools/test_dispatch_new.py tools/test_dispatch_gate.py tools/test_dispatch_gate_md.py -q`
test: tools/test_dispatch_manifest.py::<new table «test line»> | expected from: this spec §5.1 items 1-6 and the adversarial list
test: tools/test_dispatch_new.py::<existing build_text table, two rows> | expected from: §5.1 item 7
siblings: axis 13 (one cut <-> N readers); other test files that build over-threshold builder prompts (`test_owns_gate*.py`, `test_hook_liveness_probe`, `test_journal_hooks.py`) — the report names whether any asserts a launch decision on such a prompt (a turned case is a question back)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261117-forge-test-rules-spec.md

### 7.6 S-D — verdict mutants (builder; after everything-in-piles C)

given: this spec §5.2, §5.3 (outcome words); the three files; everything-in-piles §2.3 part 1 (`remarks`) as landed
owns: C:/QAFactory/forge-repo/tools/critic_verdict_check.py
C:/QAFactory/forge-repo/tools/critic_verdict.schema.json
C:/QAFactory/forge-repo/tools/test_critic_verdict_check.py
non-goals: `remarks` rules (C's); `piles.py` and its refusal texts (amendment F-D goes to that spec's owner)
handoff: C:/QAFactory/forge-repo/docs/tasks/handoffs/<task>-sd-report.md
edges: §5.2 (the run join, the control rerun per F-A, the old-verdict door text); E-T1 (same merge as critic.md rule 17)
DoD: `python -m pytest tools/test_critic_verdict_check.py -q`
test: tools/test_critic_verdict_check.py::<existing validate table, rows of §5.2> | expected from: this spec §5.2
siblings: axis 17 (one verdict shape, one reader `check_text`); `install_parity_anchors.json:699-703` (kind `path`: unchanged)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261117-forge-test-rules-spec.md

Owns across streams: S-A1 and S-A2 share `tools/tests/test_role_carriers_one_owner.py` IN SEQUENCE (S-A2 after S-A1 and
after S2; not parallel); every other owned path belongs to one stream. Disjoint or queued: yes.

---

## §8 Overlaps and order (B2, F5)

| File | Other specs in flight | Order |
|---|---|---|
| `ai-packages/.../mutate_once.py`, `test_mutate_once.py` | none (Grep `mutate_once` over `docs/tasks/specs/2026111[4-7]*.md` -> only this spec) | free |
| `ai-packages/.../test-layers.json` | any node adding a keep row (shared data file) | append one keep row; merge by hand (the late node keeps both rows) |
| `docs/TESTING.md` | boot-by-topic S3 (landed) | free -> S-A1 does not wait |
| `docs/tasks/critic-diff-brief.md` | everything-in-piles D (q4, q7, q12 (d)); spec-facts L1 (first paragraph, item 13) | anchored edits, any order; S-A1 touches only q5 and the two-layers bullets |
| `plans/builder-rules.md` 7b/7d/16 (б) | boot-by-topic S2 (7, 7b, 7c; its K-check 13-f reads «мутации судит канон пачки»); everything-in-piles D (п. 1 only) | S2 -> S-A2; D independent (anchored) |
| `PROJECT.md` п. 13 | boot-by-topic S2 (п. 13 -> pointer); everything-in-piles D | S2; not owned here (§4.4) |
| `docs/RUNBOOK.md:115` | boot-by-topic S2 RB-2 | S2 -> S-A2 |
| `.claude/agents/critic.md` | architect-tier F (rule 9); everything-in-piles D (rules 5, 17, 19); spec-facts L (rule 21) | D -> S-B (rule 17 anchored after D's clause) |
| `.claude/agents/designer.md`, `builder.md` | everything-in-piles D (designer rule 2); spec-facts L (designer rule 3) | any order (designer rule 1, builder rules 4/8 only) |
| `CLAUDE.md` rule 3, R11-h | boot-by-topic (sub-headings, F1); architect-tier L | after boot-by-topic's CLAUDE.md move (anchor text) |
| `tools/handoff_gate.py` | architect-tier reads it (`:62, :797`), writes none | free (docstring only) |
| `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` | architect-tier F (49; 5, 6, 18, 20); everything-in-piles D (33, 39); boot-by-topic S2 (33) | F -> S-B (next free number) |
| `tools/critic_verdict*.{py,json}`, its test | everything-in-piles C | C -> S-D |
| `tools/dispatch_manifest.py`, `test_dispatch_manifest.py` — the SAME function `check_cut` | spec-facts S2 (READERS NOTE in `check_cut`, not landed, P21); everything-in-piles (`judged-owns:` line) | function-disjoint owns are impossible (both write `check_cut`): an order line `очередь: spec-facts S2 → S-C` in both batch rows when S2 is dispatched first, else `очередь: S-C → spec-facts S2`; the later node merges `main` and resolves (PROJECT «Командная работа» п. 3); fork F-C |
| `tools/dispatch_new.py` | spec-facts S1 (landed); S3 (phase 2, conditional) | S-C first; S3 merges after |

Merge waves:
- wave 1: S-E and S-A1 (one `wave.py merge`, or S-E first) — the brief's probe bullet names the runner's new flags, so
  the runner is never behind the text that tells critics to use it.
- wave 2: S-B + S-D in ONE merge (E-T1: critic.md 17, the CLAUDE.md rule 3 clause and the checker switch together;
  the brief's probe text is already there from wave 1, so `mutants` never becomes required without its procedure);
  if they must split, S-B before S-D (a field the checker ignores is harmless; the reverse fails every verdict closed).
- S-C: after S-A1 (its hint names «Строка теста в DoD»), in wave 2 or later, ordered against spec-facts S2 per the row.
- S-A2: after boot-by-topic S2; closes the §4.5 window.
Between wave 1 and wave 2: TESTING names the check «Forge test discipline» before S-B writes it, and the brief asks for a
`mutants` block the checker does not read yet — both TEMPORAL, harmless, one wave long.

---

## §9 Calibration check «Forge test discipline» (S-B; number = next free at landing)

```
N. **Forge test discipline: the expected value, the `test:` line, the can-fail proof (t-940/t-956; the owner's words
17.11.2026; rule texts `docs/TESTING.md` «Откуда берётся ожидаемое значение», «Строка теста в DoD», «Тест может упасть»,
«Бюджет / Файлы», `docs/tasks/critic-diff-brief.md` question 5 and «The two layers»).** Mechanism: the `test:` line check
of `tools/dispatch_manifest.py` (door `manifest-skip: test`), the probe runner
`ai-packages/qa-factory/scripts/tests/mutate_once.py`, the `mutants` field of `tools/critic_verdict_check.py`, the
builder's `red-before:` line, critic question 5 (a)-(g). Per window, every count with its command (hygiene 6(b)):
(a) builder dispatches over the designer threshold: refused for `test` (hook log / `tools/warn_density.py`) against those
carrying `manifest-skip: test`; every skip reason listed; the reason class «spec accepted before the test line» counted
on its own — it must die out, and one on a spec accepted after the gate's merge date is a finding; any other reason class
that repeats is a finding against the rule or the generator;
(b) critic verdicts of the window (`docs/tasks/specs/reviews/`): probes per verdict by outcome, `mutants_none` reasons;
for every critic `delegated` with `worker_ref: agent:<id>`, the runner calls counted in its transcript (Grep
`mutate_once\.py` over `~/.claude/projects/<slug>/subagents/agent-<id>.jsonl`, tool_use lines) against the verdict's
`mutants` count — more calls than reported items, or more than the brief's cap, is a finding against the critic; the Lead
reads three `mutants_none` and three kills against their trail reruns (a kill whose run is absent, or whose result does
not say `outcome: killed`, is fabricated: a finding); runner calls also join the stream of check 13 (c) (a corruption
probe): a `restore-mismatch` or a `rollback not checked` marker near one is read there;
(c) defect-fix nodes (journal notes or batch rows naming a defect): builder reports with `red-before:` vs without;
`not runnable` / `not run` reasons listed;
(d) `rejected` with `failure_class: spec`: the window's lines READ one by one and classed by §6.1's rule of
`docs/tasks/specs/20261117-forge-test-rules-spec.md` (the class: the spec did not name the test place, sent rows to a
quarantined file, left a door behaviour without a row, or let a value come from the code); against the baseline 7 firm +
2 border of 70 (`dev1.jsonl` to 17.11.2026 01:59); the regex `"event": ?"rejected".*"failure_class": ?"spec".*(test|pin|тест)`
-i only finds candidates;
(e) `defect_found` whose notes say a test could not fail, asserted a literal, pinned old behaviour or duplicated a row,
against the previous window's;
(f) an empty window gets an explicit line, not a zero. Detector of this check's own leak: a window with builder
dispatches over the threshold and no line (a), or with critic verdicts and no line (b).
```

---

## §10 Four questions and axes (CLAUDE.md rule 10), per mechanism

Mechanisms: M1 oracle rule (§2.1); M2 `test:` line + gate (§2.2, §5.1); M3 can-fail proof: builder `red-before:`, critic
probe through the runner, CLAUDE.md rule 3 / R11-h / handoff_gate docstring, `mutants` (§2.3, §3.2, §3.4, §5.2, §5.3); M4
critic q5 (a)-(g) (§3.1); M5 the goal-based new-file rule, 7b conditional removed, doc negative control pointer (§4.1-4.3).

### 10.1 Four questions

| | (a) cost, who pays | (c) detector | (d) what stops a skip |
|---|---|---|---|
| M1 | designer: the source he already reads; builder: a question instead of a guess | check (d); critic q5 (b) | discipline + critic q5 (b) (named) |
| M2 | designer: <= 1 line per behaviour item (§6); coordinator: `--test` | check (a) | `dispatch_manifest.check_cut` on the launch hook (code on the path) |
| M3 | builder: 1 narrow run per defect item; critic: at most the brief's cap of runner calls per verdict, each <= 60 s; ~350 boot bytes in CLAUDE.md | check (b)(c); check 13 (c) for restores | the runner restores and classifies (code on the probe's path); `critic_verdict_check` refuses a verdict without `mutants`/`mutants_none` — on the path only after everything-in-piles A2 (until then the critic's self-run, critic.md 17, + check (b)); `red-before:` on discipline + critic q5 (a), detector (c) |
| M4 | critic: reading; builder: rows only at doors; no owner's word for a file | check (e) | discipline; the critic's verdict line under rule 20 |
| M5 | none (texts agree) | `test_role_carriers_one_owner.py` (pointers) | the carrier test in CI `forge-check` |

### 10.2 The axis block (F7) — pasted verbatim into the commit messages of S-B, S-C, S-D, S-A1, S-A2 and S-E (labels per `tools/mechanism_gate.py:42-51`)

```
axis 1 (Policy <-> role files <-> journal): covered -- M1-M5: critic.md 17/20, builder.md 4/8, designer.md 1, CLAUDE.md rule 3 and R11-h (M3) and the calibration check change together in S-B; journal fields unchanged
axis 2 (Per-tier exam instruments): covered -- M3/M4 edit critic.md; PROCESS/CRITIC_EXAM.md absent, debt F3-1, deviation line; M1/M2/M5: no exam instrument reads these texts
axis 3 (Factory package <-> its release copy <-> the installed plugin): covered -- M3: scripts/tests/mutate_once.py changes in the package and travels with the next release copy, changelog.d fragment in S-E; M1/M2/M4/M5: n/a, forge texts and tools only
axis 4 (Factory rules <-> their debt <-> the backlog <-> the principles): n/a -- M1-M5 change no FR, principle or debt line; S-E's FR pass is in its report
axis 5 (Stage twins inside the package): n/a -- M1-M5: the runner is a test helper with no stage twin; no stage function touched
axis 6 (Measurement tools <-> the package they measure): n/a -- M1-M5: no measurer changes
axis 7 (Per-test identity <-> every scope a test's behaviour depends on): n/a -- M1-M5: no per-test identity is computed or stored; the runner runs one given file
axis 8 (Where the story is on disk): n/a -- M1-M5: no story path is read
axis 9 (is this a test file): n/a -- M1-M5: no code decides whether a path is a test file; the test: WHERE is free text, the runner runs what it is given
axis 10 (git-top readers): n/a -- M3: the runner takes --root explicitly and reads no git top; M1/M2/M4/M5 read none
axis 11 (shell-command recognizers): n/a -- M3: the probe is a python -B <abs path> call, a listed hygiene door; hygiene_gate.py unchanged; M1/M2/M4/M5 none
axis 12 (carriers of the work plan): covered -- M1-M5: the five nodes go into an untaken batch of pile forge (L-7); no BACKLOG.md line
axis 13 (the dispatch text): covered -- M2 reads the one cut, adds no private scan, and joins the skip vocabulary at every iteration site of check_cut; dispatch_new asks the hook's decision; M1/M3/M4/M5 n/a
axis 14 (readers of agent transcripts): n/a -- M3: no new code reader; the check's (b) counts runner calls by a hand Grep over the critic's transcript, as check 13 (c) does; M1/M2/M4/M5 none
axis 15 (console stream setup): covered -- M3: the changed runner prints; S-E runs test_console_encoding.py (7b); M1/M2/M4/M5 n/a
axis 16 (one JSON reader of the package): n/a -- M3: S-E adds no JSON read; the spec-file form's existing json.loads stays untouched (analog noted in the spec, not widened); M1/M2/M4/M5 none
axis 17 (detector verdict shape): covered -- M3: mutants joins the one verdict shape and its one reader check_text; M1/M2/M4/M5 n/a
axis 18 (in-tree shrink-only ratchets): n/a -- M1-M5 raise no ratchet; a dup or lint raise in S-C, S-D or S-E would be named in the verdict
axis 19 (one reader of a role file's tools line): n/a -- M1-M5: no code reads a tools: line; critic.md's tools: line unchanged (Bash already there)
axis 20 (host receipt names): n/a -- M1-M5 touch no host receipt
axis 21 (readers of the package's markdown tables): n/a -- M1-M5 read no package markdown table
axis 22 (a host's return form): n/a -- M1-M5 touch no host return form
axis 23 (fields of a tests[] row): n/a -- M1-M5 touch no tests[] row
axis 24 (the record of an execution): n/a -- M1-M5 write no execution record
axis 25 (freshness of a run and of a live check): n/a -- M1-M5 judge no freshness
axis 26 (the word stand not confirmed): n/a -- M1-M5 do not use it
axis 27 (the profile of a test row): n/a -- M1-M5 name no profile
axis 28 (the render site of the row form): n/a -- M1-M5 render no row form
axis 29 (append-only jsonl writers): n/a -- M1-M5 append no jsonl line
axis 30 (the commands of a profile): n/a -- M3: the runner builds its own python/pytest argv for a probe, not a project profile command; M1/M2/M4/M5 none
axis 31 (Role carriers): covered -- M1-M5: one home per aspect (oracle, test line, red-before, new-file goal in TESTING.md; the probe, its runner and its cap in the brief, the cap number also in the checker as data); pointers elsewhere; SIBLING_MAP row; carrier-test rows
axis 32 (Where judgment lives): covered -- M2/M3: code checks presence, shape, joins and process outcomes; sufficiency, equivalence, load-bearing places, the value's source and the new-file choice stay with the critic and the Lead (M1/M4/M5)
axis 33 (which dispatch am I): n/a -- M1-M5 pick no dispatch for a session
axis 34 (One road for one action): covered -- M2: every builder dispatch over the threshold; M3: every critic diff verdict, every probe through the one runner, package and forge tests alike; M5: one file rule for package and forge; no language, project or case exempt
axis 35 (Sides of a story): n/a -- M1-M5 touch no story side
axis 36 (The row written against a substitute): n/a -- M1-M5 touch no substitute row
axis 37 (A repeat stop): n/a -- M1-M5 touch no repeat stop
```

S-E also carries the `architecture:` and `judgment:` lines of §1.1.

---

## §11 Readers of every touched file (designer rule 7; Grep tool, counts as printed)

| File | Command | Hits | Readers -> verdict |
|---|---|---|---|
| `ai-packages/.../scripts/tests/mutate_once.py` | `mutate_once` over `tools/`; `.githooks/`; `.claude/settings.json`; the package | 0; 0 (control `test_volume` -> `commit-msg:43, :48`); 0 (control `handoff_gate` -> `settings.json:51`); 1 (its own docstring) | no code reader -> unchanged; `plans/features.json:356` (feature attribution by path) -> unchanged path, unchanged; historical batch texts -> unchanged |
| `.../scripts/tests/test-layers.json` | readers named in its own `note`: `selftest.test_layers()`; `scenario_walk.witness_for`; `tools/test_quarantine.py` (writes quarantine/cohorts) | — | one keep row added -> selftest lists the new file (no `unlisted:`), witness-for prints it; test_quarantine unchanged |
| `.../changelog.d/<fragment>.md` | `changelog_assemble.py` at release | — | unchanged (one more fragment) |
| `tools/dispatch_manifest.py` | `dispatch_manifest` over `tools/` | 144 in 24 files (t-940; t-949 confirmed) | `dispatch_gate.py:798` calls `check_cut` -> unchanged code, refuses more (S-C tests); `dispatch_new.py` -> S-C; `dod_gate`, `handoff_gate`, `owns_gate`, `owns_readers`, `agent_budget`, `journal_hooks`, `hop_metrics`, `hook_liveness_probe`, `mechanism_gate` (list), `warn_layers.json` use other functions -> unchanged; tests `test_dispatch_manifest`/`_new`/`_gate`/`_gate_md` -> S-C; others unchanged (turned case = question); spec-facts S2 -> ordered (§8) |
| same, `ITEMS`/`_DISPLAY`/`check_cut`/`_parse_skip_line` | `\b(ITEMS\|KEY_GROUPS\|check_cut\|designer_threshold)\b` over `tools/` | `test_dispatch_manifest.py:1211-1272`, `test_dispatch_new.py:130`, `test_dispatch_gate*.py` monkeypatch | `ITEMS` unchanged -> pin green; `SKIP_REFUSED_TEMPLATE` text gains `test` -> a test asserting its exact item list changes in S-C (reported) |
| `tools/dispatch_new.py` | `dispatch_new` over `tools/` | 26 in 6 files | `test_dispatch_new.py` -> S-C; `owns_readers.py`, `test_gitcmd.py`, `test_dispatch_manifest.py` (mentions) -> unchanged; `.claude/skills/next-task/SKILL.md:39` -> unchanged |
| `tools/critic_verdict_check.py`, schema | `critic_verdict` over `tools/`, `.claude/agents`, `.claude/settings.json` | tools: 9 files; `critic.md:141,150`; `settings.json:163` | `test_critic_verdict_check.py` -> S-D; `critic.md` 17 -> S-B; `install_parity_anchors.json:699-703` -> unchanged; `test_handoff_rule_anchors.py:94,107` -> unchanged; `dup-baseline.json` -> unchanged unless the clone ratchet moves; everything-in-piles A2 `piles._verdict_problem` reads `check_text` -> refuses old verdicts with S-D's door text (F-D aligns its own text) |
| `tools/handoff_gate.py` | `handoff_gate` over `tools/` | 83 in 12 files | docstring only: `hook_liveness_probe.py`, `dispatch_gate.py`, `dod_gate.py`, `agent_budget.py`, `dispatch_manifest.py` (names), `mechanism_gate.py` (net list), `install_parity_anchors.json` (CLAUDE.md anchor, not this file) and tests `test_handoff_gate.py`, `test_dispatch_gate.py`, `test_dispatch_manifest.py`, `test_hook_liveness_probe.py` -> unchanged (no test pins «whole protection»: Grep -> only `handoff_gate.py:7`); `.claude/settings.json:51` hook command -> unchanged |
| `docs/TESTING.md` | `TESTING\.md\|critic-diff-brief\|builder-rules` over `tools/`; same over `.claude/agents` | tools: `test_volume.py:30`, `test_role_carriers_one_owner.py:41`; agents: `builder.md:93,95`, `critic.md:174` | headings kept -> `test_volume` unchanged; carrier test -> S-A1 rows; builder.md/critic.md -> S-B |
| `docs/tasks/critic-diff-brief.md` | same | `test_role_carriers_one_owner.py:28,55,61-63,67-68`; `test_handoff_rule_anchors.py:38`; `install_parity_anchors.json:22`; `owns_readers.py:26`; agents `critic.md:77,161,164,173` | anchors kept -> unchanged; carrier test -> S-A1 |
| `plans/builder-rules.md` | same | `test_role_carriers_one_owner.py:29-30,40,42,54-58,65,71`; `test_handoff_rule_anchors.py:39`; `test_quarantine.py:51`; `test_dispatch_manifest.py:844`; `dispatch_gate.py:1872`; `owns_readers.py:55`; agents `designer.md:20`, `builder.md:49,53` | keys and 7b anchor kept -> unchanged; no test file name added -> `test_quarantine` unchanged; item numbers kept -> unchanged; carrier test -> S-A2 |
| `docs/RUNBOOK.md` | `RUNBOOK\|SIBLING_MAP` over `tools/` | 52 in 26 files | `:115` edit keeps §7 heading -> unchanged |
| `docs/SIBLING_MAP.md` | same | `mechanism_gate.py` (reads axis headings and keys), `test_mechanism_gate.py`, `language_sites.py` and others | axis numbers and headings kept -> unchanged |
| `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` | `WEEKLY_CALIBRATION` over `tools/` | 36 in 15 files | path mentions -> unchanged; numbering read by people |
| `.claude/agents/critic.md`, `builder.md`, `designer.md` | carrier test POINTERS/OWNER_KEYS; `install_parity_anchors.json` openers (`:162`, `:175`); `test_handoff_rule_anchors.py` | — | openers and rule numbers kept -> unchanged |
| `CLAUDE.md` | `install_parity_anchors.json` (Grep `CLAUDE` anchors) ; `CLAUDE\.md["']` over `tools/*.py` | anchors `:22-25`, `:49-62` (incl. `:23` TWO-LAYER CRITIC ENTRY, `:62` R11-h phrase); 22 files | anchors kept byte-identical -> unchanged; `session_context.py:193-212` boot-size WARN/BREACH -> unchanged code, the number grows ~350 B; `agents_md.py` -> AGENTS.md regenerated (S-B); `mechanism_gate.py`, `claim_control_gate.py:253`, `journal_echo.py`, `journal_validator.py`, `permission_audit.py`, `calibration_counts.py`, `hook_liveness_probe.py`, `escape_check.py` (path names) -> unchanged |
| `tools/tests/test_role_carriers_one_owner.py` | `test_role_carriers_one_owner` over `tools/` | itself | S-A1 then S-A2 (sequence); everything-in-piles D adds rows too -> append-only rows, merge by hand |

---

## §12 Forks

### Answered by the owner (record)

- **O-1** (new test file): neither option — the goal decides (§4.1, quote there). Closed.
- **O-2** (a forge tool's own test file): «да» 17.11 — now an instance of O-1's rule (§4.1). Closed.
- **O-3** (the `test:` line is obligatory and checked by code): «ок» 17.11 — L-2 = True final. Closed.

### Remaining, for the Lead (recommendation first)

- **F-A** (S-D) the green-control join: (a) recommended — the checker requires, when `mutants` is non-empty, one
  `trail.reruns` command without `mutate_once.py`; cheap shape join that makes «a kill on a red baseline» visible; (b)
  brief rule only, check (b) reads it. Cost of (a): one more diagnostic and two table rows.
- **F-B** (§3.2 E-P8) no tree named: (a) recommended — no probe, `mutants_none: "no tree named by the dispatch"`, and the
  coordinator names the node's worktree on the critic dispatch's `given:` line (the producer of the tree path: the
  coordinator, through `dispatch_new.py`'s `given:` it already prints); (b) the critic creates a detached worktree of the
  node's branch by `git worktree add --detach` — a git write by a reading role, a second road for a probe's tree. Cost
  of (a): a probe is lost on post-merge reviews (named, counted by check (b)).
- **F-C** (§8) the order of S-C against spec-facts S2 in `check_cut`: recommended — whichever is dispatched first goes
  first, the order line written in both batch rows; if neither is dispatched, S-C first (S2 is a note, smaller rebase).
- **F-D** amendment lines in OTHER specs (named here, not written there): everything-in-piles C `:246-247` and A2
  `:307-309` «verdict predates remarks» -> «verdict predates a required field (<name>)» (owner: the Lead of that spec;
  recommended before A2's dispatch). No amendment for boot-by-topic S2 (S-A2 follows it, its K-check stays true) or for
  spec-facts S2 (order line only).

### Lead decisions L-1..L-9 stand as recorded below (L-9 (b) overridden for the CLAUDE.md rule 3 clause and the R11-h line only, by B1 -> (a)).

### Small choices closed by the designer (no design weight)

Backticks/bold/bullet around the `test:` key accepted; the FIRST `| expected from:` splits; the `none` reason rule reused;
the check named by title in TESTING, numbered at landing; ASCII diagnostics; field names `place/change/run/outcome/
killed_by/equivalent/remark`, `mutants_none`; token `red-before:`; ONE token `test` for item, display and skip (F3: the
line's own key); runner: the inline form instead of a spec file (a critic may write only its report), `--id` required in
it, `--pytest` flag (default script form = today's), `cwd=--root` only when given, `TIMEOUT_S` a module constant patched
by the test, `compile()` before touching, `outcome:` as the last printed line, exit 3 for invalid (64/2/0/1 kept);
`restore-mismatch` in the `outcome` vocabulary forcing a blocker verdict; the runner's test is a new file by §4.1's
criteria (walked in §5.3); no new critic rule number.

---

## §13 Noticed analogs and contradictions (scope not widened)

1. `PROCESS/CRITIC_EXAM.md` is absent while critic.md rule 10 demands it (debt F3-1).
2. `tools/owns_readers.py:26` cites brief «item 13 (d)», which does not exist until spec-facts L1 lands.
3. D-0056 (archive) still describes a per-node mutation list and a canon mutation pass (P6) — L-6.
4. Journal windows differ between the brief's figure and this draft's whole-file count — not a contradiction.
5. `tools/fixtures/dispatch_manifest/K3.txt:26` quotes an old «mutation (builder-rules 7a)» DoD — a fixture, history.
6. `PROCESS/DEPLOYMENT_ECONOMY_EXAM.md:111,124` keeps a kit-level «mutation kill rate» axis — untouched.
7. TESTING.md's critic bullet restated brief q5 — fixed in §2.4.
8. r2. The runner `mutate_once.py` lives in the release package although only forge builders and critics call it
   (P17); relocating it to `tools/` is a separate question for the Lead (B1 -> (a) names this path).
9. r2. `agent_budget.py:116` `TEST_RE` counts an inline runner call only when its argv names `tests/test_x.py` or
   `pytest`; the cap is counted by check (b), not by the budget hook — a code counter is promotion on evidence.
10. r2. The spec-file form's `json.loads(Path(...).read_text())` (`mutate_once.py:29`) is a JSON read outside
    `hooklib.read_json` (axis 16 closing rule); left as is (no new read).
11. r2. t-949's F4 line cites `:949`/`:956` for `newly`/`still`; on the current file they are `:953`/`:961` (`:949` is
    the `_parse_skip_line` call) — the spec uses the read lines.
12. r2. t-949 counted t-547 and t-559 in the baseline class; read here as the readers / edge class (§6.1).

---

## §14 Reading trail

t-940: `docs/TESTING.md` (whole); `docs/tasks/critic-diff-brief.md` (whole); `.claude/agents/critic.md`, `builder.md`,
`designer.md` (whole); `plans/builder-rules.md` (whole); `tools/critic_verdict.schema.json`; `tools/dispatch_manifest.py:1-383,
660-983`; `tools/dispatch_new.py:1-135`; `tools/handoff_gate.py:1-70`; `tools/tests/test_role_carriers_one_owner.py`;
`tools/test_handoff_rule_anchors.py:1-90`; `tools/install_parity_anchors.json:690-705`; `scenario_walk.py:833-932`;
calibration `:370-384, 1099-1113`; `docs/SIBLING_MAP.md:471-500`; `docs/DECISIONS_ARCHIVE.md:111-112`; four in-flight specs
by window and Grep; journal counts.
t-956 (r2), read: `docs/tasks/specs/reviews/t-949-forge-test-rules-plan.md` (whole); this spec (whole);
`ai-packages/qa-factory/scripts/tests/mutate_once.py` (whole); `tools/handoff_gate.py:1-40`; `tools/mechanism_gate.py:1-89,
215-245`; `tools/critic_verdict.schema.json` (whole); `tools/dispatch_manifest.py:80-109, 250-279, 895-983` + Grep of
templates `:123-147`; `docs/TESTING.md` (whole); `plans/builder-rules.md:38-127`; `docs/tasks/critic-diff-brief.md:1-48`;
`.claude/agents/critic.md:138-177`; `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:822-837`; `20261116-spec-facts-by-code-spec.md:366-381,
584-619`; `20261117-everything-in-piles-spec.md:226-320` (+ Grep); `tools/install_parity_anchors.json:22-67`;
`ai-packages/qa-factory/scripts/tests/scenario_walk.py:833-927`; `ai-packages/qa-factory/scripts/tests/test-layers.json:1-30,
3670-3685`; `ai-packages/qa-factory/design/architecture.md:68-157`; `docs/SIBLING_MAP.md:366-377`; `logs/journal/dev1.jsonl`
lines 139-146 and the 27 regex hits (notes read); memory note on the stale root checkout (3 days old; the root checkout
carries today's commits and t-949 read the same state — taken as current).
Greps (Grep tool) r2: `mutate_once` over the package (1), `tools/` (0; control `handoff_gate` 83/12), `.githooks` (0;
control `test_volume` 2), `.claude/settings.json` (0; control `handoff_gate` -> `:51`), `docs/tasks/specs/2026111[4-7]*.md`
(this spec, architect-tier — the latter only for `handoff_gate.py`, read-only); `mutat` -i over `test-layers.json` (2
unrelated); `READERS` over `dispatch_manifest.py` (0; control `KEY_GROUPS` 7); `^## Axis` over SIBLING_MAP (37); check
headings `^(4[6-9]|5\d)\. \*\*` (46-48); `a layer not attached|\| h \| critic/designer` over CLAUDE.md (`:79-80`, `:237`);
anchors `layer not attached|lets it write only|cheap control re-run|whole protection` over `tools/` (2) and agents (0);
`CLAUDE\.md["']` over `tools/*.py` (22 files); boot size in `session_context.py` (`:193-212`); `test.?run|pytest|TEST_RUN`
-i in `agent_budget.py`; journal: rejected 123, spec 70, regex 27; `P31` in everything-in-piles (`:61`); keep rows,
census rows; `Мутации судит канон` in RUNBOOK (`:115`); `keep row|new test file` in agents (`builder.md:51-52`,
`designer.md:22`).
Not established: whether `refusal_registry.py --check` scans `scripts/tests/` (S-E reports); the run time of
`test_mutate_once.py` (estimate); whether `test_judgment_census.py` is in `SLOW_TESTS`; whether `hygiene_gate.py` parses
quotes inside a long `--old` argument (no probe run; a refusal there is a question back from the first critic who meets
it); the current text of everything-in-piles r3 beyond `:226-320`.
Needed beyond the manifest: `scenario_walk.py`, `test-layers.json`, `architecture.md`, `agent_budget.py`,
`install_parity_anchors.json`, `session_context.py`, SIBLING_MAP axis 16, `architecture_gate.py` (grep) — all read.

---

## Lead decisions on forks L-1..L-9 (17.11.2026, Fable) and the owner's words so far

- **L-1** TESTING.md is the home of the `test:` form. **L-2** `TEST_LINE_REFUSES` = True. **L-3** cap 3 probes per
  VERDICT. **L-4** `mutants` REQUIRED, with the declared empty outcome. **L-6** yes, one decision line superseding
  D-0056 (2)/(3) on mutations. **L-7** an untaken batch of pile `forge`. **L-8** a surviving load-bearing mutant is
  «fix before merge» (fixed in the same node's fix round, as every critic remark). **L-9** (b): no CLAUDE.md pointer —
  the boot budget is already breached; designer.md rule 1, the gate's refusal and `dispatch_new` carry it.
- **L-5** (a): S-A waits for boot-by-topic S2 (one writer per sentence). S-B, S-C, S-D do not wait for S-A.
- **O-2** is already decided by the owner («да» to the Lead's five recommendations, 17.11, snapshot 02:15: «свой
  тестовый файл новому инструменту форджа») — (a).
- **Oracle (D1)**: the owner's «ок» 17.11 to «ожидаемое значение берётся оттуда [из спеки] и пишется в спеке, а не
  списывается с вывода кода» — §2.1 stands as her word.
- **O-1**, **O-3**: asked 17.11, her word pending; drafted on the recommendation (a).

## The owner's word 17.11.2026 on O-1 and O-3 — binds §4.1 and §12

- **O-3**: «ок» — the `test:` line is obligatory and checked by code.
- **O-1**: neither option as drafted. «не хочу что бы написание тестов зависило от моего слова. Какая была цель у
  сокращения количества файлов? Вот этой цели и надо придерживаться когда решаем нужен отдельный фаил или нет».
  So §4.1 is rewritten in the fix round: no owner's word is needed for a new test file, and no blanket ban; the rule
  states the GOAL of the file budget as TESTING.md already measures it (`docs/TESTING.md:26-28`: run time — files
  over 10 s; upkeep — test files edited in commits where neither code nor rule text changed; a file per script instead
  of a story) and the decision is made by that goal: the designer names the place of the row in the spec's `test:`
  line; a NEW file is right when the case fits no existing story, joint or table without making that file slower or
  wider in meaning, the new file stays under 10 s, builds its world once, and holds one parameterised table; the
  critic judges the choice (question 5). The `keep` row stays as bookkeeping. O-2 (a new forge tool gets its own
  test file) is the same rule's instance, not an exception.

## Lead decisions on plan critic t-949 (17.11.2026, Fable) — input of fix round t-956

- **B1 → (a)**: the critic RUNS the probe itself, through the existing runner
  `ai-packages/qa-factory/scripts/tests/mutate_once.py` (extended per F1: `--root`, a pytest form, a 60 s timeout, an
  import/collection error is an invalid mutant, not a kill), by Bash only, never Write/Edit; byte-copy restore and
  sha256 are the runner's. One clause is added to CLAUDE.md rule 3 (the bounded probe of the brief's «The two layers»
  is the critic's own run) and one line to R11-h and to the `handoff_gate` docstring. Reason: the owner's word is «критик
  проверяет несколько мутантов», and (b) costs a coordinator round trip per verdict. This overrides L-9 for that one
  clause only; the rule-11 pointer of L-9 stays dropped.
- **B2**: S-A is split as the critic states — S-A1 (TESTING.md texts, brief q5 and two-layers) does not wait; S-A2
  (builder-rules 7b/7d, RUNBOOK, the PROJECT column) follows boot-by-topic S2. Order: S-A1 → {S-B + S-D in one wave,
  S-C}; the window between S-A1 and S-A2 is the accepted TEMPORAL edge, named in the spec.
- **F1–F14**: all fixed in this round, none queued. F14 (iv) is moot: O-3 is answered «ок», L-2 = True is final.

---

## §15 Fix table (t-956): remark -> what changed -> section

| Remark | What changed | Section |
|---|---|---|
| B1 critic probe vs rule 3 / R11-h | road (a): the critic runs the probe by Bash through `mutate_once.py` only; exact texts for the CLAUDE.md rule 3 clause, the R11-h cell and the `handoff_gate` docstring line; anchors `:23`, `:62` kept; brief mechanical-layer sentence amended; owner of the runner extension = new stream S-E with owns, table rows and their source; one-road landing grep (no hand-built copy/mutate/restore in any text) | §3.2, §3.4, §5.3, §7.1, §7.4 |
| B2 order contradicts itself | S-A split into S-A1 (TESTING, brief; no wait) and S-A2 (7b/7d/16 (б), RUNBOOK; after S2; PROJECT not owned); order S-E + S-A1 -> {S-B + S-D one wave, S-C}; S-A2 after S2; the window named as the accepted TEMPORAL edge, landing grep in S-A2's DoD | §4.4, §4.5, §7.2, §7.3, §8 |
| F1 runner exists | `mutate_once.py` extended: `--root`, inline form with `--id`, `--pytest`, 60 s timeout, compile before touching, exit 3 invalid for import/collection/timeout/crash; error direction and adversarial list; test place by the goal rule | §5.3, §7.1, §1.1 |
| F2 vacuous run join | `run` must join a distinct `trail.reruns` command containing `mutate_once.py`, pairwise distinct, whose result says `outcome: <word>`; `outcome` field added | §5.2 |
| F3 door token | one token `test` for item, display and skip; `manifest-skip: tests` stays refused with a copyable list | §5.1 items 3, 5 |
| F4 iteration sites | named: `_parse_skip_line :271`, `SKIP_REFUSED_TEMPLATE :146`, `newly :953`, `still :961`, `_items_text :902-903` / `_DISPLAY :95`, `_FORM_HINTS`, `_expected_forms` | §5.1 item 4, §0 P11 |
| F5 spec-facts S2 overlap | row added: same function, function-disjoint impossible, order line both ways; fork F-C | §8, §12, §0 P21 |
| F6 inflated baseline | re-cut by reading the 27 hits: 7 firm + 2 border of 70, each id with its reason; check (d) reads per line, regex only for candidates; L-2 rationale restated | §0 P16, §6, §6.1, §9 (d) |
| F7 axis block | 37 labelled lines, gate-shaped, closing M1-M5 by name, pasted into every stream's commit | §10.2 |
| F8 cap restated | number kept only in the brief (rule) and the checker/schema (data); TESTING, RUNBOOK, critic.md 17, calibration point without it | §2.3, §3.3, §4.4, §5.2, §9 |
| F9 builder-rules 16 (б) | pointer clause for the one `red-before:` run, in S-A2 | §4.4, §7.3 |
| F10 oracle gaps | keep exemption only with a named value or invariant; values derived from the test's input by a rule the spec states added; q5 (b) aligned | §2.1, §3.1 |
| F11 cap counted on declaration; no timeout | check (b) counts runner calls in the critic's transcript against `mutants`; the runner's 60 s timeout | §9 (b), §5.3, §3.2 E-P4 |
| F12 first dispatches of in-flight specs | edge E-C4 with its door reason `spec accepted before the test line (<spec>)`, counted as its own class in check (a) | §5.1, §9 (a) |
| F13 verdicts before the field | S-D's own refusal names the field-generic door; amendment line for everything-in-piles C/A2 named (fork F-D); M3 (d) depends on A2, stated | §5.2, §10.1, §12 |
| F14 minors | (i) CLAUDE.md stays in S-B owns, scoped to the rule 3 clause and R11-h (B1 needs it), rule 11 pointer dropped; (ii) the O-2 placeholder gone — O-2 is an instance of the O-1 rule; (iii) TESTING names the check by title, no instruction text landed; (iv) closed by the owner's «ок» on O-3, L-2 final; (v) check (b) names check 13 (c)'s stream | §7.4, §4.1, §2.4, §5.1 item 6, §9 (b) |
| O-1 owner's word | §4.1 rewritten: goal-based rule (run time, upkeep, file per script), the designer places the row, a new file when no existing file fits without getting slower or wider, under 10 s, one world, one table; critic judges (q5 (g)); keep = bookkeeping; O-2 an instance; exact texts for TESTING «Файлы», 7d, builder.md 4, designer.md 1; owner quoted; artifact sweep of TESTING | §4.1, §2.5, §3.1 (g) |

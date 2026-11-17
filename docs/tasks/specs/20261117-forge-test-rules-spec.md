# Forge test rules: where the expected value comes from, a bounded can-fail proof, the critic's test questions, the `test:` line -- DRAFT

task: t-940 (draft) | feature: F19 | designer draft for Lead acceptance; each build stream gets its own task_id
Language: owner-facing rule texts in Russian carriers stay Russian (TESTING.md, builder-rules, RUNBOOK); English carriers
(critic brief, role files, CLAUDE.md, calibration protocol) stay English; tool messages and data keys English.
Scope: forge process files only (`docs/`, `plans/`, `.claude/agents/`, `tools/`, `PROCESS/`, `CLAUDE.md`). Nothing under
`ai-packages/qa-factory/` -> no AR-n is touched; commits carry `architecture:`/`judgment:` lines only if a stream strays
into the package (none does). Owner of every check added below: DATA (code) for presence/shape/joins; JUDGMENT (critic,
accepted by the Lead) for sufficiency, equivalence and the value's source (AR-29/P27 applied to the forge by analogy; no
package census row).

---

## §0 Premises (each read in its carrier, 17.11.2026)

| # | Fact | Carrier |
|---|---|---|
| P1 | TESTING.md has no rule on the source of a test's expected value; its how-to (`:135-162`) and «Что пишется» (`:43-59`) speak of layers, doors, data, never of the oracle | `docs/TESTING.md` read whole |
| P2 | The brief retires the mutation list and sends mutation runs to the canon: `:11` «no mutation list (retired 10.11.2026, `docs/TESTING.md`)», `:19-20` «ratchets and mutation runs are not — they are the batch canon's (D-0056)» | `docs/tasks/critic-diff-brief.md:10-21` |
| P3 | builder-rules 7b `:57-59` «**Мутации** билдер не прогоняет и не перечисляет: мутации судит канон пачки (слово владельца 28.10 и 10.11.2026, `PROJECT.md` «Командная работа» п. 13)» | `plans/builder-rules.md:57-59` |
| P4 | No CI workflow runs a mutation: Grep `mutat` -i over `.github` -> 0; positive control same tool, `python` -i over `.github/workflows` -> 82 hits in 5 files; the same `mutat` grep over `tools/` -> 74 hits in 23 files (comments, fixtures, test_quarantine) | Grep tool, 17.11 |
| P5 | Other carriers of «мутации судит канон»: `PROJECT.md:364-365` (п. 13), `AGENTS.md:379-380` (generated), `docs/RUNBOOK.md:115`, `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:377-378` («a mutation RUN is the leak — those are the batch canon's») | Grep `мутац\|mutation\|mutant\|мутант` -i over the root/doc/agent/PROCESS carriers |
| P6 | D-0056 (archive) rule (2)/(3): the builder names mutants without running them; the canon runs «one mutation pass over every node's list»; the critic's re-run is «never ... a mutation run». The 10.11 retirement removed the list; no archive line supersedes (2)/(3) | `docs/DECISIONS_ARCHIVE.md:112` |
| P7 | Brief q5 says «A missing pin is NOT a finding»; no duty to check a new behaviour has a row, a rewritten test kept coverage, a test is not a duplicate | `critic-diff-brief.md:35-46` |
| P8 | New-test-file contradiction: TESTING «Бюджет / Файлы» `:117` «новый тестовый файл не создаётся» with one forge exception `:124-127` (the offload spec's tools only); builder-rules 7d `:90-93` «файл у нового скрипта — только со строкой `keep` ... и не дольше 10 с»; builder.md rule 4 «no new test file is written without a keep row (7d)»; designer.md rule 1 «never asks for a new test file outside the keep rows» | read |
| P9 | 7b `:44-53` keeps a TEMPORAL branch «Пока перевод в карантин не выполнен (в `test-layers.json` нет строк `quarantine`)»; the section exists: `test-layers.json:7174` `"quarantine": {` | Grep |
| P10 | 7d `:89` «Свидетель наличия ключей в тексте — вывод в отчёте, в репозиторий не коммитится» — no negative control named; CLAUDE.md rule 11 DOC-DISPATCH WITNESS (iii) requires one | read |
| P11 | `tools/dispatch_manifest.py` is the one cut and the completeness check: `KEY_GROUPS` (`:84-93`), header grammar (`_HEADER_RE`), `check_cut` (`:906-971`), `DESIGNER_THRESHOLD = 3` (`:105`), `manifest-skip` parsing over `ITEMS` (`:258-276`); `ITEMS` is pinned by `tools/test_dispatch_manifest.py:1269`; it is a mechanism path (`tools/mechanism_gate.py:275`) | read |
| P12 | `tools/dispatch_new.py` prints headers only (`build_text`, `:85-106`), then asks `dispatch_gate.decide_full` on them; a `test:` line is not a header today and no argument prints one | read |
| P13 | Verdict checker: hard-coded rules in `critic_verdict_check.validate_verdict` (`:63-170`), reference schema `tools/critic_verdict.schema.json` (required: verdict, blockers, class_completeness, trail) | read |
| P14 | `PROCESS/CRITIC_EXAM.md` is absent (Glob `PROCESS/*EXAM*.md` -> two other files; `PROCESS/README.md:22` «generated at onboarding; not present»); precedent road for a critic.md edit: «Deviation: exam not run; debt F3-1» (`docs/tasks/specs/20261116-spec-facts-by-code-spec.md:464-469`) | Glob, Grep |
| P15 | Calibration checks run to 48 (`WEEKLY_CALIBRATION_PROTOCOL.md:1113`); 49 is claimed by the architect-tier spec (`20261116-architect-tier-spec.md:573`) | Grep |
| P16 | Journal evidence (whole `logs/journal/dev1.jsonl`): 116 `rejected`, 68 of them `failure_class: spec`, 25 of those 68 name a test or pin in notes (Grep `"event": ?"rejected".*"failure_class": ?"spec".*(test\|pin\|тест)` -i), 43 `defect_found`. Samples: t-420 «the DoD sent the rows to a quarantined test», t-654 «Spec did not name the window test», t-054 «the product-row repeat (E5) is unpinned. The spec let the builder skip it» | Grep, content mode |

---

## §1 What changes (map of D1-D6 to texts, carriers, detectors, cost)

| Lead direction | Text (§) | One home | Pointers | Code | Detector | Cost |
|---|---|---|---|---|---|---|
| D1 oracle | §2.1 | TESTING.md «Откуда берётся ожидаемое значение» | builder-rules 7d, builder.md 8, critic.md 20, brief q5 (b) | none (judgment) | check 50 (d), critic q5 (b) | 0 runs; reading |
| D2 can-fail | §2.3, §3.2 | builder side: TESTING.md «Тест может упасть»; critic side: brief «The two layers» (the probe) | 7b, critic.md 17/20, RUNBOOK, calibration 13(j) | verdict `mutants` (S-D) | check 50 (b)(c) | builder: 1 narrow run per defect node; critic: <= 3 narrow runs per verdict |
| D3 critic questions | §3.1 | brief q5 | critic.md 20, TESTING «Кто что делает» | none (judgment) | check 50 (e) | reading; no new tests demanded beyond door-reachable behaviour |
| D4 spec line | §2.2 | TESTING.md «Строка теста в DoD» | designer.md 1, CLAUDE.md rule 11 checklist (2) | gate (S-C) | gate refusal + check 50 (a) | measured §6: <= 1 line per behaviour item, 0.8-2.7 % of a spec |
| D5 contradictions | §4 | TESTING «Бюджет / Файлы»; 7b; CLAUDE.md rule 11 DOC-DISPATCH | 7d, builder.md 4, designer.md 1 | none | test_role_carriers rows | none |
| D6 code | §5 | `dispatch_manifest.py` (test line), `critic_verdict_check.py` (mutants) | dispatch_new, schema | S-C, S-D | check 50; tests | one table each |

Owner's words answered: «у нас в фордже и требований нет. Или вместо них у нас спека?» -> §2.1 (spec / DoD, rule text,
owner's word; silent spec -> question). «надо исправить, но не вернуться к куче мутантов...» -> §2.3 + §3.2 (cap 3 per
verdict, narrow file only, no suite anywhere; stale «канон судит мутации» removed §4.4). «На каждое новое поведение
логично писать тест, но так что бы прогон и написание тестов не стали основной работой форджа» -> §3.1 (c): a row only
for behaviour reachable through a door; internal boundary and volume budget untouched; (e) forbids duplicates. «а это не
сделает разработку в 2 раза медленнее?» -> §2.2 one line per behaviour item inside the DoD the designer already writes;
§6 measures it. «всё что недоделанно делаем сегодня» -> §7 streams and the five П1 nodes (§7.0), order §8.

---

## §2 TESTING.md texts (stream S-A)

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
(исход на нём — всё равно из спеки); поведение, которое спека велит сохранить, с причиной (это инвариант края, а не
тест «как раньше» из таблицы «Что не пишется»).
```

Invariant: no asserted value enters a forge test without a source a tier above can check. Edge: spec silent -> question
(builder.md rule 1), never a value picked by the builder; a value picked anyway is critic q5 (b).

### 2.2 New subsection after 2.1

```
### Строка теста в DoD

Слово владельца 17.11.2026: «а это не сделает разработку в 2 раза медленнее?» — поэтому одна строка на пункт, и только
на пункт поведения. Пункт спеки билдеру, который меняет то, что видно через дверь (аргумент или выход CLI, вердикт хука
или гейта, поле или файл, который читает другой), несёт внутри DoD одну строку:

    test: <файл::таблица или строка> | expected from: <§ спеки, правило, слово владельца>

или `test: none -- <почему> | expected from: <источник>` (документ — свидетель по правилу 11 `CLAUDE.md` «DOC-DISPATCH
WITNESS»; суждение роли — живой прогон; внутренняя граница без своей двери). Строка называет МЕСТО строки теста
(существующая таблица, история или стык; новый файл — только по «Бюджет / Файлы») и ИСТОЧНИК ожидания; самих значений
не повторяет — они в тексте пункта и его краёв. Пункт без поведения (перенос текста, переименование) строки не получает;
диспатч, где такого пункта нет вовсе, несёт одну строку `test: none -- поведения нет | expected from: <§ спеки>`.
Наличие и форму строки проверяет код (`tools/dispatch_manifest.py`, диспатч билдеру от порога дизайнера); хватает ли строк
и верен ли источник — судит критик (вопрос 5 `docs/tasks/critic-diff-brief.md`).
```

### 2.3 New subsection after 2.2

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
- **Критик, дифф с новым поведением**: ломает 1–3 места нового поведения и смотрит, какая строка краснеет; процедура и
  потолок — `docs/tasks/critic-diff-brief.md` «The two layers».
```

Invariant: a defect row that was never seen red is never presented as a regression proof without a named reason; no
carrier sends anyone to a mutation suite.

### 2.4 «Кто что делает» (`docs/TESTING.md:174-178`)

- `:174` «- **Дизайнер**: DoD называет поведения и стык, а не число проверок; ребро спеки — строка таблицы теста.» ->
  «- **Дизайнер**: DoD называет поведения и стык, а не число проверок; ребро спеки — строка таблицы теста; на пункт
  поведения — строка `test:` («Строка теста в DoD»).»
- `:176-178` the critic bullet (a restatement of brief q5, axis 31) -> «- **Критик**: вопрос 5 и проба «The two layers»
  `docs/tasks/critic-diff-brief.md`.»
- `:181-182` detector sentence: append «; строки `test:`, пробы критика и `red-before:` — калибровочная проверка 50
  (номер — следующий свободный при посадке).»

---

## §3 Critic texts

### 3.1 `docs/tasks/critic-diff-brief.md` question 5 (`:35-46`) -> (stream S-A)

```
5. **Tests** (`docs/TESTING.md`, the owner's words 10.11 and 17.11.2026), each sub-question answered:
   (a) KILLING POWER: would the node's test catch the defect the node exists for, through the door the factory uses --
   judged by reading AND by the probe of «The two layers»; a probe mutant in load-bearing new behaviour that survives is
   a finding (an equivalent mutant is not, with its why). For a defect item, the builder's `red-before:` line is read: a
   red at import or collection is not a red.
   (b) EXPECTED VALUE: every asserted value traces to the spec/DoD, a rule text or the owner's word
   (`docs/TESTING.md` «Откуда берётся ожидаемое значение»); a literal that matches only the code's own output, with no
   such source, is a finding; a value the spec left silent and the builder picked is a finding against the spec.
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
   (g) The layers (`ai-packages/qa-factory/scripts/tests/test-layers.json`, spec
   `docs/tasks/specs/td-15-scenarios-quarantine.md`): a new test file outside `docs/TESTING.md` «Бюджет / Файлы», or a
   keep row whose layer/why does not hold -- finding; an edit to a quarantined file without a `quarantine-edit:` reason
   that holds -- finding; a phase-2 move whose replacement does not catch the detector's class -- finding.
```

What «A missing pin is NOT a finding» still protects (asked by D3): the owner's word 10.11 against receipts and pins
(TESTING «Что не пишется»); it no longer shields a missing behaviour row. Invariant: (c) never reads as «a test per line
or per function»; a finding under (c) names the DOOR.

### 3.2 «The two layers» (`critic-diff-brief.md:10-21`) (stream S-A)

- Mechanical layer, `:11` after «the DoD run tails (the scope: `plans/builder-rules.md` 7b);» insert «for a defect item,
  the `red-before:` line (`docs/TESTING.md` «Тест может упасть»);». The clause «no mutation list (retired 10.11.2026,
  `docs/TESTING.md`)» stays.
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
  flipped, a branch dropped, a refusal turned into a pass, the safe default returned) — and run, per
  mutant, ONLY the narrow test file the spec's `test:` line names (no line: the narrowest file of the
  builder's witness). Hard cap: 3 mutant runs per verdict, invalid ones included; never a slow
  (`SLOW_TESTS`, `test_story_run_*`, `test_story_step.py`), quarantined or canon file. Where: in the
  node's worktree, never in the root checkout or another session's tree; a byte copy of the file BEFORE
  the edit, the restore FROM it whatever the run's exit, the hash comparison in the trail (CLAUDE.md
  command hygiene pt. 7); with no worktree left, a scratch copy of only the files the narrow test needs,
  or no probe. A mutant counts only when it changes behaviour and the file still imports: a red at
  import or collection is an invalid mutant, not a kill. Every mutant goes into the verdict block's
  `mutants` (place, change, run, the row that killed it or null); a survivor is a finding under
  question 5 (a) unless it is equivalent — then say why. No probe (a docs-only or plan gate, no new
  behaviour, the narrow test slow or quarantined, no tree to probe): `mutants: []` and
  `mutants_none: "<why>"`. A restore whose hash differs is a blocker of your own verdict: name the file
  and the backup path and stop probing.
```

Edges of the probe (each with its invariant):
- E-P1 docs-only diff / plan gate: no probe, `mutants_none`. Invariant: a critic never edits a doc to "mutate" it (the doc
  witness's own negative control, CLAUDE.md rule 11 (iii), is the can-fail proof there).
- E-P2 diff with no new behaviour (refactor): no probe; `mutants_none: "no new behaviour: <why>"`. Invariant: the probe
  never becomes a regression sweep of old behaviour.
- E-P3 narrow test slow or quarantined: no probe; the gap is NAMED in `mutants_none`. Invariant: the critic never runs a
  canon file; an unproven can-fail is said, never counted as proven.
- E-P4 a run fails or hangs: the restore runs anyway (one shell command: copy, mutate, run with a time cap, restore,
  hash); the time cap is the narrow file's own (<= 1 min per builder-rules 7b), a timeout counts as an invalid mutant.
  Invariant: the reviewed tree is byte-identical after the critic.
- E-P5 restore mismatch: blocker of own verdict, backup path named, probing stops; the coordinator restores from the
  backup before any merge. Invariant: no merge carries a probe's bytes.
- E-P6 one verdict over several nodes (one critic per topic): the cap stays 3 per verdict (fork L-3).
- E-P7 the node's worktree is the reviewed branch: probing it while the builder still works is forbidden — the critic
  starts after the builder's handback (it does today).

### 3.3 `.claude/agents/critic.md` (stream S-B; Lead commits; mechanism path)

- Rule 17, the clause «fields verdict (fit / fit_with_fixes / blocker), blockers, class_completeness, trail (read +
  reruns)» -> append «, mutants (0-3 probes, docs/tasks/critic-diff-brief.md «The two layers») or, when there was no
  probe, mutants_none with its reason». Anchored on that text; if everything-in-piles D has added `remarks` there first,
  insert after its clause. The opener line «17. Your verdict MUST end with a fenced ```json block carrying the» stays
  byte-identical (`install_parity_anchors.json:162`).
- Rule 20, «(the rule text is docs/TESTING.md «Бюджет»)» -> «(the rule texts are docs/TESTING.md «Бюджет», «Откуда
  берётся ожидаемое значение» and «Тест может упасть»; the probe of «The two layers» answers under this line)».
- No new rule number (spec-facts-by-code L takes 21). Exam: `PROCESS/CRITIC_EXAM.md` absent (P14) -> commit message
  «Deviation: exam not run; debt F3-1» (the precedent road).

---

## §4 D5 and the stale texts

### 4.1 New test file (one home: TESTING «Бюджет / Файлы»; fork O-1/O-2 decides the content)

Recommended text (O-1 (a) + O-2 (a)) replacing `docs/TESTING.md:117` «- **Файлы**: новый тестовый файл не создаётся;
случай идёт строкой в сценарий, стык или таблицу своего слоя.» and `:124-127` (the offload-only exception):

```
- **Файлы**: новый тестовый файл не создаётся; случай идёт строкой в сценарий, стык или таблицу своего слоя. Строка
  `keep` в `test-layers.json` — учёт файла, а не разрешение его создать. Два исключения: (1) новый инструмент форджа
  `tools/<x>.py` получает один свой файл `tools/test_<x>.py` — одна параметризованная таблица и строки стыков, до 10 с
  (слово владельца 14.11.2026, спека `docs/tasks/specs/20261114-coordinator-offload-spec-r2.md`; на все новые
  инструменты — слово владельца <дата ответа на O-2>); строки `keep` у тестов форджа нет; (2) новый файл пакета —
  только словом владельца, записанным в спеке, и со строкой `keep`.
```

Then pointers: builder-rules 7d `:90-93` «новый тестовый файл не создаётся: ... файл у нового скрипта — только со строкой
`keep` в `scripts/tests/test-layers.json` (слой и причина, их судит критик) и не дольше 10 с;» -> «новый тестовый файл —
по `docs/TESTING.md` «Бюджет / Файлы» (случай — строка `variants.json` истории `scripts/tests/fixtures/stories/<id>/` или
строка таблицы/стыка своего слоя);». builder.md rule 4 «and no new test file is written without a keep row (7d)» ->
«and a new test file only by `docs/TESTING.md` «Бюджет / Файлы»». designer.md rule 1 «a DoD never asks for a new test
file outside the keep rows of `test-layers.json`» -> «a DoD never asks for a new test file outside `docs/TESTING.md`
«Бюджет / Файлы»». TESTING `:55` «(исключение — «Бюджет / Файлы»)» stays.

### 4.2 Stale conditional in 7b (`plans/builder-rules.md:44-53`)

From «Пока перевод в карантин не выполнен (в `test-layers.json` нет строк `quarantine`), к напечатанному добавляется
прежний объём:» through «и ключи своего DoD;» -> «К напечатанному добавляются только файлы, которые называют строки
`test:` DoD узла (путь вне пакета — тестовый файл, который его судит, правило 4 `CLAUDE.md`); тронут
`story_run_common.py` — в отчёте строка «тронут story_run_common.py» (все `test_story_run_*.py` судит канон);». The
per-type list after it («`--limits --lang` и `test_audit_rules.py` — только если ...; так же по типу правки: ...
`test_console_encoding.py` ...») stays unconditional. TEMPORAL: the branch was for the world without a quarantine
section; that world ended (`test-layers.json:7174`). Invariant: a quarantined file is never run; the per-type gate
tests are still run when their type of change happens (specs rely on it: `20261117-rules-debt-fix-spec.md:224,275`).

### 4.3 Doc-dispatch negative control (7d `:89`)

«Свидетель наличия ключей в тексте — вывод в отчёте, в репозиторий не коммитится.» -> «Свидетель наличия ключей в
тексте — по правилу 11 `CLAUDE.md` «DOC-DISPATCH WITNESS» (ключи дословно из DoD, скрипт целиком в отчёте,
отрицательный контроль), в репозиторий не коммитится.» Also append to 7d's first sentence after «читается до первого
теста»: «; ожидаемое значение — «Откуда берётся ожидаемое значение» там же».

### 4.4 Stale «канон судит мутации» (every carrier; both worlds of boot-by-topic S2)

| Carrier | After S2 (expected) | If S2 has not landed (TEMPORAL, fork L-5) | New text |
|---|---|---|---|
| builder-rules 7b `:57-59` | «**Мутации** билдер не прогоняет и не перечисляет: мутации судит канон пачки (слово владельца 28.10 и 10.11.2026).» | same with «, `PROJECT.md` «Командная работа» п. 13)» | «**Набор мутаций** билдер не прогоняет и не перечисляет (слово владельца 28.10 и 10.11.2026), и канон пачки его не гоняет; проба «тест может упасть» у билдера одна — строка дефекта, красная до правки (`docs/TESTING.md` «Тест может упасть», слово владельца 17.11.2026).» |
| PROJECT.md п. 13 `:364` | gone (pointer + dispatcher sentence «...или гонять мутации...» — still true) | «**Мутации** билдер не прогоняет и не перечисляет — их судит канон» | «**Набор мутаций** билдер не прогоняет и не перечисляет (владелец, 28.10 и 10.11.2026); проба «тест может упасть» — `docs/TESTING.md`.» + AGENTS.md regenerated (builder-rules 17) |
| RUNBOOK `:115` | «Мутации судит канон пачки (`plans/builder-rules.md` п. 7b).» | «... (`PROJECT.md`, «Командная работа» п. 13).» | «Мутаций канон не гоняет: что тест может упасть, показывают билдер (строка дефекта красная до правки) и критик (1–3 мутанта) — `docs/TESTING.md` «Тест может упасть».» |
| brief `:19-20` | — | — | §3.2 |
| calibration 13(j) `:377-378` | — | — | «a docker run or a mutation SUITE is the leak — the first are the batch canon's, the last nobody's (a builder's one `red-before:` run of a defect row is not a mutation run, `docs/TESTING.md` «Тест может упасть»)» |
| builder-rules 16 (б) `:120` «мутации билдер не гоняет (п. 7b)» | unchanged (true) | | |
| TESTING `:95` receipt row «каждую мутацию» | unchanged (true) | | |

Key for S2: its K-check 13-f expects «7b holds «мутации судит канон пачки»» — true only BEFORE S-A. Hence order §8.
Landing check (S-A DoD key): Grep `судит канон пачки|their judge is the canon|batch canon's.*mutation|мутации судит|их судит канон` -i
over CLAUDE.md, PROJECT.md, docs/*.md, docs/tasks/critic-diff-brief.md, plans/builder-rules.md, PROCESS/*.md -> 0 hits
for a mutation claim (positive control: the same call finds «судит канон пачки» in 7b's slow-files sentence
«билдер НЕ гоняет и не ждёт: «судит канон пачки»», which stays).

---

## §5 Code (D6)

### 5.1 S-C: the `test:` line gate (`tools/dispatch_manifest.py`, `tools/dispatch_new.py`)

Owner served: DATA (presence and form); sufficiency and source are the critic's (q5). Behaviour:
1. `test_lines(cut) -> list[(line_index, where, source)]`: every UNQUOTED line of the cut (any section; fenced and
   blockquote lines never count — the module's rule) matching: optional bullet, optional `**`, optional one pair of
   surrounding backticks, the key `test:` (case-insensitive), a non-empty WHERE, the FIRST `| expected from:`
   (case-insensitive), a non-empty SOURCE. WHERE `none` must be followed by `--`/`—` and a reason holding a word
   character (the siblings rule, `_NONE_ANSWER_RE`). The header grammar does NOT gain `test` (a `test:` line never ends a
   section; `KEY_GROUPS` and `ITEMS` unchanged — `test_dispatch_manifest.py:1269` stays green).
2. In `check_cut`, after the existing items and before the skip lines: for `is_builder` and `max(designer_threshold(cut))
   >= DESIGNER_THRESHOLD`, no well-formed line -> `missing["tests"] = "no line" | "ill-formed: <first bad line, cut at 80
   chars>"`. Not checked under the threshold, for non-builder kinds, or on a degraded cut (the UNCHECKED note as today).
3. Refusal: the existing INCOMPLETE text names it with display name `test` and the hint «(over the designer threshold:
   one line per behaviour item inside the DoD, `test: <file::table> | expected from: <spec §, rule, owner's word>` or
   `test: none -- <why> | expected from: <source>`; the form: docs/TESTING.md «Строка теста в DoD»)».
4. Door: `manifest-skip: tests -- <reason>` (new `SKIP_ONLY_ITEMS = ("tests",)` accepted by `_parse_skip_line` and
   listed in SKIP_REFUSED_TEMPLATE); the skip note as for other items.
5. Switch `TEST_LINE_REFUSES` (default per fork L-2; recommended True): False -> the same check reported as a note.
6. `dispatch_new.py`: `--test "<where> | expected from: <source>"` repeatable; each printed as `test: <value>` on its own
   line right after the `DoD:` line; the existing newline/backtick and empty-item refusals apply to it.

Error direction (a presence detector promoted to a gate, designer rule 1): it may err to a FALSE PASS (one line present
while other behaviour items lack one; a nonsense source) — accepted, critic q5 catches; it must NOT falsely refuse, and
these adversarial inputs stay on the PASS side when one well-formed line exists: the line under `siblings:` or after the
last header; a bulleted / bold / backticked key; CRLF line ends; a `|` inside WHERE before the first `| expected
from:`; `Expected From:` in any case. These stay REFUSED (over the threshold, no other line): a `test:` line only inside
a fence or blockquote; `test: none | expected from: x`; `test: tools/x.py` with no source; an empty source; prose
`Test row: ...`; `manifest-skip: tests` with no reason (existing SKIP REFUSED).

Edges: E-C1 a resubmission (`designer: resubmission t-NNN`) whose spec predates the rule — refused like any; door
`manifest-skip: tests -- spec predates the test line (t-NNN)`. Invariant: no over-threshold builder dispatch goes out
silent about its tests. E-C2 TEMPORAL: before S-A lands, the refusal would name a section that does not exist -> S-C
merges after S-A (§8). E-C3 the K7 fixture case (`test_dispatch_manifest.py:137`, `== (0, "", "")`) and every existing
over-threshold builder prompt asserting exit 0 in the owned test files gain a `test:` line (never a weakened check); the
report lists each changed case.

Tests (rows in existing tables, no new file): `tools/test_dispatch_manifest.py` one parameterised table «test line»
over the pass/refuse inputs above (ids name the case; the expected exit and missing label come from this section);
`tools/test_dispatch_new.py` one row `--test` printed under DoD + one row over threshold without `--test` refused.

### 5.2 S-D: the verdict's mutants (`tools/critic_verdict_check.py`, the schema)

After everything-in-piles stream C (same three files, its `remarks`). New helper `_mutant_errors(obj)` called from
`validate_verdict`; the schema mirrors it:
- `mutants`: REQUIRED array (fork L-4), 0-3 items; > 3 -> `field 'mutants' has N items: at most 3 (the cap of
  docs/tasks/critic-diff-brief.md, The two layers)`.
- item: `place` (1-300 chars), `change` (1-300), `run` (1-500; must equal the `command` of some `trail.reruns` item —
  a join, so a probe without its run in the trail fails), `killed_by` (1-300 string, or null = survived).
- survivor (`killed_by` null): exactly one of `equivalent` (non-empty reason) or `remark` (the id of a `remarks` item
  with disposition `fix`, C's vocabulary); neither -> error; a survivor with `remark` in a `fit` verdict is impossible
  by C's rules (a fix remark is named in `fixes`/`blockers`).
- `mutants: []` requires `mutants_none` (a string holding a word character); `mutants_none` with a non-empty `mutants`
  -> error.
- Diagnostics ASCII; old verdicts fail with `missing required field: mutants` (history; C's `--no-verdict` door covers a
  verdict that predates the field).
Error direction: shape and joins only; it may FALSE-PASS a fabricated kill (caught by the critic-of-critic sampling in
check 50 (b)); it never judges whether a mutant was load-bearing or equivalent (judgment, P27).
Tests: rows in `tools/test_critic_verdict_check.py`'s existing tables: valid 0/1/3 probes; 4 probes; survivor without
equivalent/remark; run not in trail; empty without reason; reason with probes.

---

## §6 Cost of D4, measured (Grep tool, 17.11.2026; numbers with their command)

| Spec (recent, accepted) | lines `rg -c "^"` | numbered items `rg -c "^\s*\d+\. "` | single `Item:`/`Items:` headers `rg -c "^Items?( \(S1[ab]\))?:"` | lines already naming a test `rg -ci "\bTest( row\| rows\|s)?:\|test row\|\bT\d+\b.*(green\|red)"` | upper bound of added lines |
|---|---|---|---|---|---|
| `20261116-fg7-5-node-cost-with-rework-spec.md` | 486 | 13 (6 are grouping rules, 4 analog notes) | 0 | 2 (+ §5, a 41-line test table already) | 4 (T1-T4) = 0.8 % |
| `20261117-rules-debt-fix-spec.md` | 612 | 12 | 7 (4 single-item streams) | 8 | 16 = 2.6 % (8 of them rewrite a prose «Test:» into the line) |
| `20261116-spec-facts-by-code-spec.md` | 867 | 23 (most are lists of misses/analogs) | 0 | 2 | 23 = 2.7 % (true behaviour items fewer) |

Upper bound: 43 lines on 1,965 (2.2 %); the line names a place and a source the designer already reads for the edges, so
the added time is the typing of one line per item, not a new analysis. What it removes: of 68 `failure_class: spec`
rejections in `logs/journal/dev1.jsonl`, 25 name a test or pin (P16) — the class «the spec did not name the test / sent
rows to a quarantined or out-of-owns test / left a behaviour unpinned». Each such reject cost a fix round (a fresh
builder + a critic re-review, CLAUDE.md rule 12). Estimate, not measured: the share of those 25 the line would have
prevented; check 50 (d) measures it from the next window on.
Critic probe cost: <= 3 narrow runs per verdict (each <= 1 min by 7b's narrow criterion) — estimate, not measured;
check 50 (b) records run counts. Builder: one narrow run per defect item.

---

## §7 Streams

### 7.0 The five П1 nodes (pile and batch: fork L-7)

| Node | Lead direction | Streams |
|---|---|---|
| N1 oracle rule | D1 | S-A (§2.1, 7d pointer), S-B (builder.md 8, critic.md 20) |
| N2 can-fail proof | D2 | S-A (§2.3, §3.2, §4.4), S-B (critic.md 17, calibration 13(j)), S-D |
| N3 critic test questions | D3 | S-A (§3.1, §2.4) |
| N4 the `test:` line | D4, D6 | S-A (§2.2), S-B (designer.md 1, CLAUDE.md 11), S-C |
| N5 contradictions | D5 | S-A (§4.1-4.3), S-B (builder.md 4, designer.md 1) |

### 7.1 S-A — docs (builder)

given: this spec §2, §3.1, §3.2, §4; `docs/TESTING.md`, `docs/tasks/critic-diff-brief.md`, `plans/builder-rules.md`, `docs/RUNBOOK.md`, `tools/tests/test_role_carriers_one_owner.py`, `CLAUDE.md` rule 11 (DOC-DISPATCH WITNESS)
owns: C:/QAFactory/forge-repo/docs/TESTING.md
C:/QAFactory/forge-repo/docs/tasks/critic-diff-brief.md
C:/QAFactory/forge-repo/plans/builder-rules.md
C:/QAFactory/forge-repo/docs/RUNBOOK.md
C:/QAFactory/forge-repo/tools/tests/test_role_carriers_one_owner.py
non-goals: any code; PROJECT.md (S-B/Lead, only in the no-S2 world); brief questions other than 5 and the two-layers bullets; RUNBOOK beyond `:115`; builder-rules beyond 7b `:44-59` and 7d
handoff: C:/QAFactory/forge-repo/docs/tasks/handoffs/t-940-sa-report.md (Lead names the id)
edges: §4.4 both worlds; anchors kept byte-identical: «## The two layers», «6. **DUPLICATION AND CONSISTENCY**», «7. **CODE QUALITY**», «12. **ONE ROAD**», OWNER keys of q7/q12, RULES_7B, «Покрасневший пин удаляется, а не чинится», «не регрессия, не соседи, не большие файлы», TESTING headings «Бюджет / Объём», «Бюджет / Файлы», «Как писать эффективный тест на нашем проекте»
DoD: `python -m pytest tools/tests/test_role_carriers_one_owner.py -q` green, plus the doc-dispatch witness (keys below quoted verbatim, script in full in the report, one key deliberately absent -> failure)
test: tools/tests/test_role_carriers_one_owner.py::OWNER_KEYS,POINTERS | expected from: this spec §7.1 rows
siblings: axis 31 (one owner per aspect; the new homes are rows of the carrier test); `owns_readers.py:26` cites brief «item 13 (d)» (spec-facts L, not this stream)

Carrier-test rows (variant rows of the existing tables): OWNER_KEYS + `("tests:oracle", "docs/TESTING.md", "тест, чьё
ожидание переписано из того, что код напечатал, может только пройти")`, `("tests:line", "docs/TESTING.md", "Пункт без
поведения (перенос текста, переименование) строки не получает")`, `("review:probe", BRIEF, "a red at import or collection
is an invalid mutant, not a kill")`; POINTERS + `(RULES, "«Откуда берётся ожидаемое значение»", "docs/TESTING.md", "### Откуда
берётся ожидаемое значение")`, `(RULES, "`docs/TESTING.md` «Тест может упасть»", "docs/TESTING.md", "### Тест может упасть")`,
`("docs/TESTING.md", "`docs/tasks/critic-diff-brief.md` «The two layers»", BRIEF, "- **The probe**")`.
Doc keys (verbatim): «### Откуда берётся ожидаемое значение», «### Строка теста в DoD», «### Тест может упасть», «red-before:»,
«(e) DUPLICATE», «A missing PIN», «- **The probe**», «Hard cap: 3 mutant runs per verdict», «Строка `keep` в `test-layers.json` — учёт
файла», «К напечатанному добавляются только файлы, которые называют строки», «отрицательный контроль), в репозиторий не коммитится»;
absent keys: «Пока перевод в карантин не выполнен», «мутации судит канон пачки», «they are the batch canon's (D-0056);\n  re-deriving».

### 7.2 S-B — role files, CLAUDE.md, calibration, map (builder edits, leaves STAGED; Lead commits with the axis block and `tier:`)

given: this spec §3.3, §4.1 (pointers), §9, §10; the five files below; `tools/install_parity_anchors.json`; `tools/test_handoff_rule_anchors.py`
owns: C:/QAFactory/forge-repo/.claude/agents/critic.md
C:/QAFactory/forge-repo/.claude/agents/builder.md
C:/QAFactory/forge-repo/.claude/agents/designer.md
C:/QAFactory/forge-repo/CLAUDE.md
C:/QAFactory/forge-repo/PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md
C:/QAFactory/forge-repo/docs/SIBLING_MAP.md
non-goals: rule numbers (no new rule; critic.md 21 belongs to spec-facts L); any rule opener line; PROJECT.md unless fork L-5 (b)
handoff: C:/QAFactory/forge-repo/docs/tasks/handoffs/t-940-sb-report.md (Lead names the id)
edges: rule openers byte-identical (`install_parity.py --check` MISSING (0)); critic.md rule 17 lands in the SAME merge as S-D (E-T1); CLAUDE.md edit only if fork L-9 (a); exam deviation line for critic.md (P14)
DoD: `python -m pytest tools/tests/test_role_carriers_one_owner.py tools/test_handoff_rule_anchors.py -q` and `python -B tools/install_parity.py --check` (MISSING (0)), plus the doc-dispatch witness on the keys of §3.3, §9, §10
test: none -- role and process texts; doc-dispatch witness (CLAUDE.md rule 11) | expected from: this spec §3.3, §9, §10
siblings: axis 31 (SIBLING_MAP row for TESTING.md), axis 2 (critic exam, absent: debt F3-1), axis 1 (policy <-> role files)

Texts: critic.md §3.3; builder.md rule 4 and rule 8 (append «The expected value of a test and the red-before run of a
defect row: TESTING.md «Откуда берётся ожидаемое значение», «Тест может упасть».»); designer.md rule 1 §4.1 + «per
behaviour item the DoD carries the one `test:` line of `docs/TESTING.md` «Строка теста в DoD»»; CLAUDE.md rule 11
checklist (2): after «stated, or explicitly forked up» insert «; for a builder, one `test:` line per behaviour item
(`docs/TESTING.md` «Строка теста в DoD»)» (+ ~90 B; anchor «AND the edge behaviors NAMED» untouched; AGENTS.md
regenerated); calibration §9; SIBLING_MAP axis 31: intro list gains «`docs/TESTING.md` (which tests, the expected
value's source, the `test:` line, the builder's can-fail step)», table row `| docs/TESTING.md | builder, critic,
designer | which tests; expected value; the test: line; red-before | owner; scope -> builder-rules 7b; the critic's
probe -> the brief |`, brief row aspect «the two layers' content (the probe included)».

### 7.3 S-C — test line gate (builder; `dispatch_manifest.py` left STAGED, Lead commits)

given: this spec §5.1; `tools/dispatch_manifest.py`, `tools/dispatch_new.py`, `tools/dispatch_gate.py` (`decide_full`, read), the four test files
owns: C:/QAFactory/forge-repo/tools/dispatch_manifest.py
C:/QAFactory/forge-repo/tools/dispatch_new.py
C:/QAFactory/forge-repo/tools/test_dispatch_manifest.py
C:/QAFactory/forge-repo/tools/test_dispatch_new.py
C:/QAFactory/forge-repo/tools/test_dispatch_gate.py
C:/QAFactory/forge-repo/tools/test_dispatch_gate_md.py
non-goals: the header grammar, `KEY_GROUPS`, `ITEMS`; `dispatch_gate.py` code; any other reader of the cut
handoff: C:/QAFactory/forge-repo/docs/tasks/handoffs/t-940-sc-report.md
edges: §5.1 E-C1..E-C3 and the adversarial list
DoD: `python -m pytest tools/test_dispatch_manifest.py tools/test_dispatch_new.py tools/test_dispatch_gate.py tools/test_dispatch_gate_md.py -q`
test: tools/test_dispatch_manifest.py::<new table «test line»> | expected from: this spec §5.1 items 1-5 and the adversarial list
test: tools/test_dispatch_new.py::<existing build_text table, two rows> | expected from: §5.1 item 6
siblings: axis 13 (the dispatch text: one cut <-> N readers; the new reader reads the cut, never its own scan); other test files that build builder prompts over the threshold (`test_owns_gate*.py`, `test_hook_liveness_probe` via `hook_liveness_probe.py`, `test_journal_hooks.py`) — the report names whether any asserts a launch decision on such a prompt (a turned case is a question back, not an owns widening)

### 7.4 S-D — verdict mutants (builder; after everything-in-piles C)

given: this spec §5.2; the three files; everything-in-piles §2.3 part 1 (`remarks`)
owns: C:/QAFactory/forge-repo/tools/critic_verdict_check.py
C:/QAFactory/forge-repo/tools/critic_verdict.schema.json
C:/QAFactory/forge-repo/tools/test_critic_verdict_check.py
non-goals: `remarks` rules (C's); `piles.py`
handoff: C:/QAFactory/forge-repo/docs/tasks/handoffs/t-940-sd-report.md
edges: §5.2; E-T1 (same merge as critic.md rule 17 and the brief's probe bullet)
DoD: `python -m pytest tools/test_critic_verdict_check.py -q`
test: tools/test_critic_verdict_check.py::<existing validate table, six rows> | expected from: this spec §5.2
siblings: axis 17 (one verdict shape, one reader `check_text`); `install_parity_anchors.json:699-703` (kind `path`: unchanged)

Witness scope for all four: the named test files only (owned paths outside the package: the test file that judges the
path, CLAUDE.md rule 4); no full `pytest tools/`, no CI wait (7b).

---

## §8 Overlaps and order

| File | Other specs in flight | Order |
|---|---|---|
| `plans/builder-rules.md` 7b/7d | boot-by-topic S2 (B-1..B-7: 7, 7b, 7c; its K-check 13-f reads «мутации судит канон пачки» in 7b); everything-in-piles D (п. 1 only) | S2 -> S-A; D independent (anchored) |
| `PROJECT.md` п. 13 | boot-by-topic S2 (п. 13 -> pointer); everything-in-piles D (п. 2, 4, 9, 11) | S2 first; S-A touches PROJECT only in the no-S2 world (L-5) |
| `docs/RUNBOOK.md:115` | boot-by-topic S2 RB-2 | S2 -> S-A |
| `docs/TESTING.md` | boot-by-topic S3 (landed: `:80`, `:175` already pointers) | free |
| `docs/tasks/critic-diff-brief.md` | everything-in-piles D (q4, q7, q12 (d)); spec-facts L1 (first paragraph, item 13) | any order, anchored edits; S-A touches only q5 and the two-layers bullets |
| `.claude/agents/critic.md` | architect-tier F (rule 9); everything-in-piles D (rules 5, 17, 19); spec-facts L (rule 21) | D -> S-B (rule 17 anchored after D's clause) |
| `.claude/agents/designer.md` | everything-in-piles D (rule 2); spec-facts L (rule 3) | any order (rule 1 only) |
| `CLAUDE.md` rule 11 | boot-by-topic (sub-headings, F1); architect-tier L | after boot-by-topic's CLAUDE.md move (anchor text) |
| `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` | architect-tier F (49; 5, 6, 18, 20); everything-in-piles D (33, 39); boot-by-topic S2 (33) | F -> S-B (number 50) |
| `tools/critic_verdict*.{py,json}`, its test | everything-in-piles C | C -> S-D |
| `tools/dispatch_manifest.py`, `dispatch_new.py` | spec-facts S1 (landed: owns_readers block); everything-in-piles (`judged-owns:` line, line 291) | everything-in-piles first if launched today (same `check_cut`); else free |

Merge waves: wave 1 S-A (after S2); wave 2 S-B + S-D in ONE `wave.py merge` (E-T1: critic.md 17, the brief's probe and
the checker switch together; a checker that requires `mutants` before critics are told fails every verdict closed;
the reverse order lets critics write a field the checker ignores — harmless, so if the waves must split, S-B before
S-D); S-C after S-A (its refusal names a TESTING section).

---

## §9 Calibration check 50 (S-B; number = next free at landing)

```
50. **Forge test discipline: the expected value, the `test:` line, the can-fail proof (t-940; the owner's words
17.11.2026; rule texts `docs/TESTING.md` «Откуда берётся ожидаемое значение», «Строка теста в DoD», «Тест может упасть»,
`docs/tasks/critic-diff-brief.md` question 5 and «The two layers»).** Mechanism: the `test:` line check of
`tools/dispatch_manifest.py` (door `manifest-skip: tests`), the `mutants` field of `tools/critic_verdict_check.py`, the
builder's `red-before:` line, critic question 5 (a)-(e). Per window, every count with its command (hygiene 6(b)):
(a) builder dispatches over the designer threshold: refused for `test` (`tools/warn_density.py` / hook log) against
those carrying `manifest-skip: tests`; every skip reason listed; a reason class that repeats is a finding against the
rule or the generator; (b) critic verdicts of the window (`docs/tasks/specs/reviews/`): probes per verdict, killed,
survived-equivalent, survived-finding, `mutants_none` reasons; the Lead reads three `mutants_none` and three kills
against their trail reruns (a kill whose run is absent or green in the trail is a fabricated kill: a finding against
the critic); (c) defect-fix nodes (journal notes or batch rows naming a defect): builder reports with `red-before:` vs
without; `not runnable` / `not run` reasons listed; (d) `rejected` with `failure_class: spec` whose notes name a test
or pin (Grep `"event": ?"rejected".*"failure_class": ?"spec".*(test|pin|тест)` -i over the window's journal lines),
against the previous window's (baseline 25 of 68 over `dev1.jsonl` to 17.11.2026); (e) `defect_found` whose notes say
a test could not fail, asserted a literal, or pinned old behaviour, against the previous window's; (f) an empty window
gets an explicit line, not a zero. Detector of this check's own leak: a window with builder dispatches over the
threshold and no line (a), or with critic verdicts and no line (b).
```

---

## §10 Four questions and axes (CLAUDE.md rule 10), per mechanism

Mechanisms: M1 oracle rule (§2.1); M2 `test:` line + gate (§2.2, §5.1); M3 can-fail proof: builder `red-before:`,
critic probe, `mutants` (§2.3, §3.2, §5.2); M4 critic q5 (c)-(e) (§3.1); M5 one home for new files, 7b conditional
removed, doc negative control pointer (§4.1-4.3).

| | (a) cost, who pays | (c) detector | (d) what stops a skip |
|---|---|---|---|
| M1 | designer: the source he already reads; builder: a question instead of a guess | check 50 (d); critic q5 (b) | discipline + critic q5 (b) (named) |
| M2 | designer: <= 1 line per behaviour item (§6); coordinator: `--test` | check 50 (a) | `dispatch_manifest.check_cut` on the launch hook (code on the path) |
| M3 | builder: 1 narrow run per defect item; critic: <= 3 narrow runs per verdict | check 50 (b)(c) | `critic_verdict_check` refuses a verdict without `mutants`/`mutants_none` (code on the path); `red-before:` on discipline + critic q5 (a), detector 50 (c) |
| M4 | critic: reading; builder: rows only at doors | check 50 (e) | discipline; the critic's verdict line under rule 20 |
| M5 | none | `test_role_carriers_one_owner.py` (pointers) | the carrier test in CI `forge-check` |

Axes (one block for M1-M5):
- axis 1: covered — role files, CLAUDE.md rule 11, calibration change together (S-B), journal fields unchanged.
- axis 2: covered — critic.md edited; `PROCESS/CRITIC_EXAM.md` absent, debt F3-1, deviation line.
- axes 3-10: n/a — no package, no release copy, no measurer, no story resolver, no test-file leaf, no git-top reader (forge process texts and two forge tools).
- axis 11: n/a — no shell-command recognizer (the critic's probe uses existing hygiene doors; `hygiene_gate.py` unchanged).
- axis 12: covered — the five nodes go into a batch (fork L-7); no BACKLOG.md line.
- axis 13: covered — M2 reads the one cut (`section_cut`), adds no private scan; `dispatch_new` asks the hook's decision.
- axis 14: n/a — no transcript reader.
- axis 15, 16: n/a — no console setup, no package JSON reader.
- axis 17: covered — `mutants` joins the one verdict shape and its one reader `check_text`.
- axis 18: n/a — no ratchet raised (state at acceptance: `dup_ratchet` and `lint_ratchet` read from forge-check).
- axes 19-30: n/a — package seams (role `tools:` line, host receipts, md tables of the package, host forms, tests[] rows, run records, freshness, stand words, profiles, row render, jsonl appenders, profile commands) not touched.
- axis 31: covered — new homes in TESTING.md and the brief; pointers elsewhere; SIBLING_MAP row; carrier-test rows.
- axis 32: covered — code checks presence/shape/joins only; sufficiency, equivalence and the value's source stay with the critic and the Lead.
- axis 33: n/a — no dispatch-identity reader.
- axis 34: covered — one road: every builder dispatch over the threshold, every critic diff verdict, every carrier; no language, project or case exempt (the docs-only and no-behaviour cases take the same road with a `none -- <why>`).
- axes 35-37: n/a — package story sides, substitute rows, repeat stops.

---

## §11 Readers of every touched file (designer rule 7; Grep tool, counts as printed, 17.11.2026)

| File | Command | Hits | Readers -> verdict |
|---|---|---|---|
| `tools/dispatch_manifest.py` | `dispatch_manifest` over `tools/` | 144 in 24 files | `dispatch_gate.py:798` calls `check_cut` -> unchanged code, refuses more (S-C tests); `dispatch_new.py` -> changes in S-C; `dod_gate`, `handoff_gate`, `owns_gate`, `owns_readers`, `agent_budget`, `journal_hooks`, `hop_metrics`, `hook_liveness_probe`, `mechanism_gate` (list), `warn_layers.json` use other functions -> unchanged; tests `test_dispatch_manifest`/`_new`/`_gate`/`_gate_md` -> change in S-C; `test_dispatch_cut`, `test_handoff_gate`, `test_owns_gate_md`, `test_agent_budget`, `test_hop_metrics`, `test_journal_hooks`, `test_owns_readers` -> unchanged (S-C reports any turned case as a question) |
| same, `ITEMS`/`check_cut`/`designer_threshold` | `\b(ITEMS\|KEY_GROUPS\|check_cut\|designer_threshold)\b` over `tools/` | `test_dispatch_manifest.py:1211-1272`, `test_dispatch_new.py:130`, `test_dispatch_gate*.py` monkeypatch | ITEMS unchanged -> pin `:1269` green |
| same, over `.githooks/`, `.claude/` (settings, agents, skills) | `dispatch_manifest` | 0 (control: `test_volume` -> `.githooks/commit-msg:43`) | — |
| `tools/dispatch_new.py` | `dispatch_new` over `tools/` | 26 in 6 files | `test_dispatch_new.py` -> S-C; `owns_readers.py`, `test_gitcmd.py`, `test_dispatch_manifest.py` (mentions) -> unchanged; `.claude/skills/next-task/SKILL.md:39` -> unchanged |
| `tools/critic_verdict_check.py`, schema | `critic_verdict` over `tools/`, `.claude/agents`, `.claude/settings.json` | tools: 9 files; `critic.md:141,150`; `settings.json:163` | `test_critic_verdict_check.py` -> S-D; `critic.md` 17 -> S-B; `install_parity_anchors.json:699-703` (kind path) -> unchanged; `test_handoff_rule_anchors.py:94,107` (names the checker in critic 16/17) -> unchanged (names kept); `dup-baseline.json:350,483` -> unchanged unless the clone ratchet moves (forge-check reads it); `md_regions.py:38`, `escape_check.py:7`, `test_p4_stdin_deadline.py` (comments) -> unchanged; everything-in-piles A2 `piles._verdict_problem` reads `check_text` -> unchanged (an old verdict fails earlier on `remarks`) |
| `docs/TESTING.md` | `TESTING\.md\|critic-diff-brief\|builder-rules` over `tools/`; same over `.claude/agents` | tools: `test_volume.py:30`, `test_role_carriers_one_owner.py:41`; agents: `builder.md:93,95`, `critic.md:174` | headings kept -> `test_volume` unchanged; carrier test -> S-A rows; builder.md/critic.md -> S-B |
| `docs/tasks/critic-diff-brief.md` | same | `test_role_carriers_one_owner.py:28,55,61-63,67-68`; `test_handoff_rule_anchors.py:38`; `install_parity_anchors.json:22`; `owns_readers.py:26`; agents `critic.md:77,161,164,173` | anchors kept -> unchanged; carrier test -> S-A; `owns_readers.py:26` «item 13 (d)» -> unchanged (spec-facts L) |
| `plans/builder-rules.md` | same | `test_role_carriers_one_owner.py:29-30,40,42,54-58,65,71`; `test_handoff_rule_anchors.py:39`; `test_quarantine.py:51` (FORGE_CARRIERS: names of test files in text); `test_dispatch_manifest.py:844` (K3 given path); `dispatch_gate.py:1872` («item 20»); `owns_readers.py:55`; agents `designer.md:20`, `builder.md:49,53` | keys and 7b anchor kept -> unchanged; no test file name added -> `test_quarantine` unchanged; item numbers kept -> unchanged |
| `docs/RUNBOOK.md` | `RUNBOOK\|SIBLING_MAP` over `tools/` | 52 in 26 files | `:115` edit keeps §7 heading -> `test_role_carriers` (RUNBOOK -> 7b pointer), `dispatch_gate.py` «§12 item 8», `test_quarantine` «section 7» unchanged |
| `docs/SIBLING_MAP.md` | same | `mechanism_gate.py`, `test_mechanism_gate.py`, `language_sites.py` and others (path mentions) | axis numbers kept -> unchanged |
| `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` | `WEEKLY_CALIBRATION` over `tools/` | 36 in 15 files | path mentions (`journal_validator.py:237,368`, `test_claim_control_gate.py`, `dispatch_gate.py`, …) -> unchanged; check numbering read by people only |
| `.claude/agents/critic.md`, `builder.md`, `designer.md` | the carrier test POINTERS/OWNER_KEYS; `install_parity_anchors.json` rule openers (`:162`, `:175`); `test_handoff_rule_anchors.py` (rules 16/7/5) | — | openers and rule numbers kept -> unchanged |
| `CLAUDE.md` | `install_parity_anchors.json:49,57,58` | 3 anchors of rule 11 | «FIVE-POINT CHECKLIST», «AND the edge behaviors NAMED» kept -> unchanged; AGENTS.md regenerated |
| `tools/tests/test_role_carriers_one_owner.py` | `test_role_carriers_one_owner` over `tools/` | itself (everything-in-piles §11 count: 1) | everything-in-piles D adds rows too -> append-only rows, merge by hand |

---

## §12 Forks

### For the owner (plain words; recommendation first)

- **O-1. Новый тестовый файл в пакете.** Сейчас два правила спорят: TESTING.md — «новый файл не создаётся», builder-rules
  7d — «можно, если есть строка keep». (а) Рекомендую: файла нет, случай — строка в существующий тест; новый файл пакета
  — только вашим словом в спеке (строка keep — учёт, не разрешение). (б) Новый скрипт пакета может получить свой файл со
  строкой keep и до 10 с. Цена (а): иногда случай ляжет в чужой по смыслу файл; цена (б): файлов снова станет больше.
- **O-2. Тест у нового инструмента форджа.** Сейчас свой файл `tools/test_<x>.py` разрешён только инструментам одной
  спеки (14.11). (а) Рекомендую: так у каждого нового инструмента форджа — одна таблица, до 10 с (иначе каждый новый
  инструмент ждёт вашего отдельного слова). (б) Оставить как есть: каждый раз спрашивать вас.
- **O-3. Цена строки `test:`.** Замер на трёх последних спеках: не больше одной строки на пункт поведения, 0,8–2,7 %
  длины спеки (§6); спека без строки (от трёх пунктов) не уходит билдеру. Рекомендую принять; против — оставить строку
  советом без проверки кодом.

### For the Lead

- **L-1** home of the `test:` form: TESTING.md (recommended; one test home, boot-free) vs CLAUDE.md rule 11.
- **L-2** `TEST_LINE_REFUSES` default: True (recommended; the evidence of a leak exists: 25 of 68 spec rejects, P16; the
  generator prints the line) vs False (note first, promote after a window).
- **L-3** probe cap per verdict (recommended: 3; one critic per topic stays bounded) vs per node (3 x nodes).
- **L-4** `mutants` REQUIRED (recommended; fail-closed like `remarks`, empty outcome declared) vs optional (a silent
  verdict without a probe passes — FR-4 against).
- **L-5** if boot-by-topic S2 does not land today: (a) S-A waits (recommended, one writer per sentence); (b) S-A applies
  the no-S2 column of §4.4 (PROJECT п. 13 joins S-A's owns) and S2's K-check 13-f/RB-2 are amended to the new 7b text.
- **L-6** a decision record (DECISIONS.md, Lead) superseding D-0056 (2)/(3) and its critic clause «never ... a mutation
  run» by the 17.11 word (recommended: yes, one line; P6).
- **L-7** pile/batch for the five П1 nodes (§7.0): `forge` untaken batch (recommended) or a new one.
- **L-8** severity of a surviving load-bearing mutant: «fix before merge» (recommended) vs «blocks».
- **L-9** the CLAUDE.md rule 11 pointer (+~90 B; CLAUDE.md is over its WARN per boot-by-topic F19): (a) add (the brief's
  direction), (b) skip — designer.md rule 1, the gate's refusal and dispatch_new carry it (recommended if boot bytes are
  tight).

### Small choices closed by the designer (no design weight)

Backticks/bold/bullet around the `test:` key accepted; the FIRST `| expected from:` splits; the `none` reason rule reused
from siblings; check number = next free at landing; ASCII diagnostics; field names `place/change/run/killed_by/
equivalent/remark`, `mutants_none`; token `red-before:`; the probe's time cap = the narrow file's own; no new critic rule
number (rule 17/20 edits only).

---

## §13 Noticed analogs and contradictions (scope not widened)

1. `PROCESS/CRITIC_EXAM.md` is absent while critic.md rule 10 demands it (debt F3-1).
2. `tools/owns_readers.py:26` cites brief «item 13 (d)», which does not exist until spec-facts L1 lands.
3. D-0056 (archive) still describes a per-node mutation list and a canon mutation pass (P6) — L-6.
4. The brief's figure (114 `rejected` in 10-16.11) vs this draft's whole-file count (116 rejected, 68 spec, 43
   `defect_found`, `dev1.jsonl` to 17.11): different windows, not a contradiction.
5. `tools/fixtures/dispatch_manifest/K3.txt:26` quotes an old «mutation (builder-rules 7a)» DoD — a fixture, history.
6. `PROCESS/DEPLOYMENT_ECONOMY_EXAM.md:111,124` keeps a kit-level «mutation kill rate» axis — a kit text, not a rule of this
   deployment; untouched.
7. TESTING.md's critic bullet (`:176-178`) restated brief q5 (axis 31) — fixed in §2.4.

---

## §14 Reading trail

Read: `docs/TESTING.md` (whole); `docs/tasks/critic-diff-brief.md` (whole); `.claude/agents/critic.md`, `builder.md`,
`designer.md` (whole); `plans/builder-rules.md` (whole); `tools/critic_verdict.schema.json` (whole);
`tools/dispatch_manifest.py:1-383, 660-983`; `tools/dispatch_new.py:1-135`; `tools/handoff_gate.py:1-70`;
`tools/tests/test_role_carriers_one_owner.py` (whole); `tools/test_handoff_rule_anchors.py:1-90`;
`tools/install_parity_anchors.json:690-705`; `ai-packages/qa-factory/scripts/tests/scenario_walk.py:833-932`;
`PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:370-384, 1099-1113`; `docs/SIBLING_MAP.md:471-500`;
`docs/DECISIONS_ARCHIVE.md:111-112`; `docs/tasks/specs/20261117-everything-in-piles-spec.md:205-274` (+ Grep);
`20261116-boot-by-topic-spec.md:360-380` (+ Grep, persisted output); `20261116-architect-tier-spec.md` (Grep);
`20261116-spec-facts-by-code-spec.md:405-474` (+ Grep); `20261117-rules-debt-fix-spec.md:120-229` (+ Grep);
`20261116-fg7-5-node-cost-with-rework-spec.md:286-331` (+ Grep).
Greps (Grep tool): `mutat` -i over `.github` (0; control `python` -i over `.github/workflows` 82/5) and `tools/` (74/23);
`мутац|mutation|mutant|мутант` -i over root/doc/agent/PROCESS carriers; `mutat` -i over package `*.py` (2406/316, context);
`"quarantine"\s*:` in test-layers.json (`:7174`); `dispatch_manifest` over tools (144/24), `.githooks` (0; control
`test_volume` -> commit-msg:43); `dispatch_new` over tools (26/6); `critic_verdict` over tools/agents/settings;
`TESTING\.md|critic-diff-brief|builder-rules` over tools and `.claude/agents`; `WEEKLY_CALIBRATION` (36/15),
`RUNBOOK|SIBLING_MAP` (52/26) over tools; `MECHANISM_PREFIXES` in mechanism_gate.py; check headings of the calibration
protocol; Axis headings of SIBLING_MAP (1-37; `^## Axis (3[8-9]|4\d)` -> 0, control `^## Axis` -> 37 at :628);
Glob `PROCESS/*EXAM*.md` (2 files) and `PROCESS/**/CRITIC_EXAM*` (0); journal counts of §0 P16; spec line counts of §6.
Needed beyond the manifest: none (the brief named the carriers; the four in-flight specs were read by Grep and windows).

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

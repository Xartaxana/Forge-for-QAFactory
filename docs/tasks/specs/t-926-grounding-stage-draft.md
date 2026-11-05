# t-926 — the GROUNDING step: the MR against the requirements, and the blast radius, before any test (DRAFT)

designer draft for the Lead; forks are returned, not decided. Base: `main` at 9284908d (19.10.2026). Recon: `docs/tasks/specs/reports/t-925-grounding-digest.md`.
Owner's words 19.10.2026 folded in as DECIDED (relayed by the coordinator): (a) the S3 planner does grounding and blast radius;
(b) the blast radius is a required output; (c) refactoring thresholds 30% / 50%; (d) we work by REQUIREMENTS, not by AC.
Forks 2 and 5 are therefore closed by the owner. Fork 4 is half-closed. Forks 1, 3, 6–9 stay open, and 10–16 are new.

## 1. Для владельца: как работает шаг (одна страница)

**Зачем.** До того как написан хоть один тест, фабрика сверяет MR с требованиями задачи и сообщает человеку,
если MR не тот, если разработчик сделал много рефакторинга сверх задачи или если требование не реализовано. Рискованное
место в коде становится строкой плана. Затронутые области становятся рекомендацией регрессии и строками «добавить тест»
там, где их сейчас никто не покрывает.

**Кто и где.** Шаг делает тот же агент, что пишет тест-план (стратег, S3): граундинг и бласт-радиус нужны ему для
правильного плана (слово владельца). Место шага решает Lead (развилка 1): внутри диспатча S3 перед планом, отдельным первым
окном S3 или отдельной стадией. Требование одно: вопрос-остановка доходит до человека ДО того, как написан план.

**Что получает шаг.** Регистр требований S2. Требования берутся откуда угодно: из описания, комментариев,
вложений, диффа (как утверждения о поведении по P20). AC может не быть вовсе, это обычный случай. Ещё шаг получает
весь дифф MR (`work/impl-diff*.txt`, все репозитории), индекс изменений и индекс бласт-радиуса. Оба индекса
готовит **код** до запуска роли: у стратега нет Bash, и так ему не нужно ничего искать.

**Что делает код (без суждений).** (1) Режет дифф на ханки, даёт каждому id, файл, строки и функцию. (2) Строит
бласт-радиус: какие файлы и функции тронуты, кто их вызывает или импортирует (где это дёшево и где лежит checkout),
какие существующие тесты их касаются. Чего код измерить не смог, он пишет как «не измерено, потому что …» и никогда
не пишет «нет». (3) После разметки считает долю рефакторинга и решает, какая дорога: ничего / сообщить / остановить.
(4) На выходе S3 проверяет полноту. У каждого ханка есть строка, у каждого ТРЕБОВАНИЯ регистра есть строка. Каждый
риск и каждая важная непокрытая область дошли до плана. У каждой важной области есть регрессия или записанный
пробел. Молча не проходит ничего; слово человека проходит любой отказ (FR-4).

**Что решает роль (стратег).** Каждому ханку ставит одну метку: «реализует требование R-n», «рефакторинг вне
требований», «изменение поведения, которого нет в требованиях», «не относится к задаче (не тот MR?)», «инфраструктура
или сгенерированное», «код тестов», «не могу определить». Набор меток лежит в данных (развилка 12). Для каждого
требования роль отвечает обратным ходом: «реализовано ханками …», «не реализовано» или «реализовано вне этого диффа
(где)». Ещё роль пишет риски («здесь вероятен дефект: класс @ место») и решает, какие области бласт-радиуса важны.

**Куда идёт каждая метка.**
- «реализует R-n» связывает требование и код. Вопроса нет.
- «изменение поведения не из требований» — строка «было / стало» и закрытый вопрос человеку по P20. Код при этом
  никогда не становится оракулом. Если S2 этого поведения не записал, нужна развилка 14.
- риск — обязательная строка плана с этим риском как источником; под ней кейс на S4.
- «не тот MR» и «требование не реализовано» — остановка до плана с закрытым вопросом (развилка 5b — когда именно).
- рефакторинг считается долей от всех изменений (определение доли — §2.4):
  - **больше 30%** — строка в отчёте, строки в тест-плане и записи в регрессии, без остановки;
  - **больше 50%** — остановка и закрытый вопрос: какие области придётся перетестировать помимо самой задачи и во что
    это обойдётся. Ответы: «едем дальше» (рефакторинг входит в план и регрессию) или «вернуть задачу разработчику,
    чтобы вынес рефакторинг в отдельную задачу» (история останавливается; дорога назад — прогон с новым MR).
- важная область бласт-радиуса — строка регрессии («Left with you», P21) и, если её не покрывает ни один тест, строка
  плана «добавить тест».
- расхождение кода с требованием, которое тестом не поймать, — кандидат в баг (дорога FR-22, развилка 6).

**Кто спрашивает человека.** Вопросы пишет роль в `open_questions` по правилам `human-questions.md`: варианты,
цена и последствия по каждому. Показывает их драйвер, как любой вопрос S2/S3. Свободный ответ читает дирижёр (P22).
Неизвестное по коду не превращается в «да» (FR-59).

**Как докажем.** Прогон сравнения на копии TP1-13797 без следов (P8). Цена шага (P18) и трение (FR-55) до и после,
плюс засеянные проверки: чужой MR, раздутый рефакторинг (развилка 9).

## 2. Data shape

### 2.1 `work/grounding.yaml` (path through the story resolver, FR-37 / axis 8)
```yaml
schema_version: 1
diff:                    # CODE. One entry per diff file of the story (impl-diff.txt, impl-diff-<repo>.txt)
  - {path: work/impl-diff.txt, repo: <id>, sha256: <hex>, base: <rev | unknown>}
hunks:                   # CODE. Identity; a file with zero hunks (binary, rename, mode) gets ONE pseudo-hunk
  - {id: H-1, repo: <id>, file: src/a.py, kind: production|test|infrastructure_suggested,
     old: "10,4", new: "10,5", function: <hunk-header context | ->, added: 2, removed: 1, sha256: <hunk body>}
rows:                    # ROLE. A hunk may sit in more than one row (a mixed hunk); a whole file may be one row
  - id: G-1
    hunks: [H-1, H-2]            # or all:<repo>:<file>
    label: <vocabulary.grounding_labels>
    requirements: [R-3]          # required for implements / behaviour_change / test_code
    risks: [{id: K-1, hypothesis: "<class> @ <file:line>"}]   # 0..n, any label
    question: <Q-n | ->          # required for unrelated / unclassified
    reason: <= 160 chars>
requirements:            # ROLE. One line per REGISTER row (never per AC; owner (d))
  - {r: R-3, state: implemented|not_implemented|outside_diff, hunks: [H-1],
     where: <current-code:<path:line> | repo:<id> | none>, question: <Q-n | ->}
refactoring_share:       # CODE, after the rows (2.4)
  {measure: changed_production_lines, refactoring: 120, unclassified: 10, total: 300,
   percent: 43.3, road: none|notify|stop, policy: references/grounding-policy.json@<sha>,
   decision: go_on|return_to_developer|-, decision_ref: <state/words/... | ->}
blast_radius:            # CODE fills touched/callers/tests; ROLE fills the rest
  - id: B-1
    touched: {repo: <id>, file: src/a.py, symbols: [filter_payload]}
    callers: [{file: src/b.py, line: 40, symbol: filter_payload}]  # or {unmeasured: "<reason>"}
    tests: [{ref: tests/test_a.py::test_x, source: bundle|repo_scan}] # or {none: true} / {unmeasured: "<reason>"}
    matters: yes|no                      # ROLE
    why: <one line>                      # ROLE
    regression: <suite or command> | gap:<reason>     # ROLE; matters:yes only
    add_tests: <TS-n> | not_needed:<reason>           # ROLE; required when tests is none/unmeasured and matters:yes
```
Data: `handoffs/vocabulary.yaml` gets `grounding_labels` and `requirement_grounding_states`. `references/grounding-policy.json`
holds `{measure, notify_above_percent: 30, stop_above_percent: 50, label_weights_in_numerator: [refactoring, unclassified]}`
(FR-13). Code reads them, never a list in a `.py` file.

### 2.2 The plan link (fork 11 picks the form). Recommended form: no new row kind. A plan row's existing `risk_source_refs[]`
(`planning_contract.RISK_FIELDS`, `planning_contract.py:20`) carries `grounding:K-n` for a risk, `blast:B-n` for an
added test, and `refactoring:G-n` for a 30% / go-on refactoring row. `not_planned[]` may name `K-n` / `B-n` with the
person's decision. `regression_recommendations[]` gains `area: B-n`.

### 2.3 Handoff keys (S3 form `handoffs/s3-strategist-to-designer.yaml`; every claim gets a verifier in `handoff_check.CLAIMS`)
- `inputs`: `work/grounding.yaml` (required when `pipeline.implementation_source == diff`, else a declared null outcome).
- `inputs_read`: `{path: work/impl-diff*.txt, hunks_handed: <code>, hunks_in_rows: <code>}`; `{path: work/requirements-register.md, requirements: <code>, in_grounding: <code>}`.
- `grounding: {hunks, rows_cover: "<n> of <n>", requirements_cover: "<n> of <n>", refactoring_percent, road, decision}`. All are derived by code (DERIVERS); the role writes none of them.
- `blast_radius: [{id, matters, regression, add_tests}]`. The S8 reader of the regression line takes it from here (FR-49).
- claims, each with a verifier that calls the S3 exit check's own function, so a claim and a gate cannot disagree (FR-10):
  `every_hunk_of_the_diff_has_a_grounding_row`, `every_register_requirement_has_a_grounding_line`,
  `every_risk_and_uncovered_area_reaches_a_row_or_not_planned`, `every_area_that_matters_has_regression_or_a_gap`,
  `refactoring_share_computed_by_code`.
- S2 form: `every_hunk_of_the_diff_was_read` stays a role statement. The digest shows there is no verifier, and this draft
  makes no claim either way. The verified successor lives at S3. `diff_accounting` (S2, per file) stays or is derived (fork 15).

### 2.4 The refactoring measure (owner (c); the thresholds are data)
`percent = 100 * W / T`, where:
- `T` = added + removed lines of every hunk whose `kind` is production (the `test_files` consumer `grounding`; safe
  direction = production);
- `W` = the same lines of every production hunk that sits in at least one row labelled `refactoring` or `unclassified`.
The comparison is integer: `100*W > 30*T` means notify, `100*W > 50*T` means stop. "Больше" is strict, so exactly 30.0%
does not notify.
Error direction: toward the question. A mixed hunk and an unclassified hunk count in `W`, and test and infrastructure
lines leave `T`, so the share goes up.
Two readings a person may dispute, both stated on the 50% card: (i) lines versus units of change (a mechanical rename
over 200 call sites against one 300-line feature; lines weigh moves and reformatting heavily); (ii) whether tests and
config belong in `T` (with them in, the share drops). `T = 0` (no production lines) gives `percent: n/a` and `road: none`,
with the reason printed. The not-implemented stop covers that case (E2).

### 2.5 Exit-gate refusals (S3 exit, `planning_contract` or its own module; text per FR-1; whole list per C2-1)
Every refusal below ends with: *A person's word passes this check (FR-4).*
- **R1 hunks:** "grounding: 3 of 41 hunks of the implementation diff have no row — H-7 (src/filter.py:88), H-8
  (src/filter.py:140), H-31 (ui/Grid.tsx:12). Expected: every hunk in a row with a label from implements, refactoring,
  behaviour_change, unrelated, infrastructure, test_code, unclassified; a whole file may be one row (`hunks: all:<file>`).
  Way on: fill the empty rows the skeleton already holds in work/grounding.yaml; a hunk you cannot judge is
  `unclassified` with a reason and a question."
- **R2 requirements:** "grounding: R-4, R-9 of the register have no line under `requirements`. Expected:
  `implemented` with its hunks, `not_implemented` with a blocking question, or `outside_diff` with where it lives (`none`
  needs a question). Way on: add the two lines."
- **R3 words:** "row G-5: label `refactor` is not one of <list>. Way on: write one of the list." The same form covers
  `state`, `matters` and `road`.
- **R4 links:** "row G-2 is `implements` and names no requirement / names R-30, which the register does not hold. Way on:
  name the R ids from the register, or relabel the row."
- **R5 stale:** "work/grounding.yaml was labelled against impl-diff.txt sha 3f2a…; the diff on disk is 9c1e… (the MR
  moved). Rows measured on other bytes do not count. Way on: the S3 dispatch preparation re-runs the skeleton; rows whose
  hunk sha is unchanged are kept, changed and new hunks get empty rows."
- **R6 stop owed:** "the plan cannot be written yet: <wrong MR | R-4 not implemented | refactoring 56% of the changed
  production lines> has no answer from the person. Expected: a blocking question in open_questions (the readings are
  named) and the stage halted before the plan."
- **R7 risk / area unplanned:** "K-2 (`unbounded recursion @ src/filter.py:140`) and B-3 (src/export.py, no test
  covers it) reach no plan row: no row carries `grounding:K-2` / `blast:B-3` in risk_source_refs, and not_planned names
  neither. Way on: a plan row (`plan_row.py --row TS-n --set …` by code) or a not_planned entry with the decision."
- **R8 regression:** "B-1 and B-4 are `matters: yes` with neither a regression command nor `gap:<reason>`."

## 3. Batch draft — pile `grounding` (fork 8), batch 1, in the form of `plans/piles/_template/batch.md`

Header (draft): кучка `grounding` | статус: ожидает | стенд: нужен | приоритет: П1 (Lead).
Order on shared files:
- `handoff_check.py`: G1-1 → G1-4 → G1-7;
- `exit_gate.py`: G1-1 → G1-8;
- `agents/qa-test-strategist.md`: G1-4 → G1-5;
- `story_run.py`: after the open conductor nodes (an `очередь:` line, or function lists per D-0048).

Witness scope:
- each node: its own tests, plus `python -B scripts/selftest.py --limits --lang` and `scripts/tests/test_audit_rules.py`;
- every package test file the merge touches runs in docker python:3.12 before the merge;
- the full canon is CI `package-fast`.

Executor key: D = designer, CP = critic on the plan, B = builder, C = critic on the diff.
Every node walks FR A–G (one line per section, PROJECT.md «Как принимается»).

| Узел | Что | Исполнитель | Пишет в | Тесты | Зависит | FR (затронутые) | Оси |
|---|---|---|---|---|---|---|---|
| G1-1 | One reader of the diff. Builds the hunk index on `diff_pass.parse` with these changes: header lines are recognised only outside a hunk's counted range; the axis-7 line splitter is used; one pseudo-hunk goes to each zero-hunk file; every `impl-diff*.txt` is read; and `handoff_check._diff_counts`/`_diff_files` and `exit_gate.new_production_files` read through it. Production/test classification goes through `test_files.is_test_for("grounding")` | D→CP→B→C (reuse as a gate) | `scripts/diff_pass.py`, `scripts/handoff_check.py` (`_diff_counts`, `_diff_files`), `scripts/exit_gate.py` (`new_production_files`), the axis-9 consumer-table row | `test_diff_pass.py`, `test_exit_gate_grounding.py`, `test_handoff.py`, `test_test_files.py` | — | C FR-14, FR-17; D FR-16; G FR-28/32 | 7, 9, 15 |
| G1-2 | Blast-radius index by code (`scripts/blast_radius.py`, new). It writes touched files and symbols, callers (a bounded reference search in the checkout `handoff_check._impl_checkout`; no checkout or another language means `unmeasured`), and tests (the bundle's `existing_test_candidates` plus a repo scan through `test_files`). It runs in the S3 dispatch preparation and is linked from the brief like `repo_map` | D→B→C | `scripts/blast_radius.py`(+), `scripts/brief_pack.py` (S3 link), `scripts/tests/test_blast_radius.py`(+) | own + `test_brief_pack.py` | G1-1 | A FR-47; C FR-15, FR-56; D FR-41; F FR-51 | 9, 10, 13, 16 |
| G1-3 | The table contract. Vocabulary words; `references/grounding-policy.json` (30/50 as data); `scripts/grounding_table.py`(+) with `--skeleton` (code-filled sections from G1-1/G1-2 plus the register ids), `--check` (R1–R5, R8), `--refresh` (keeps rows by hunk sha) and the share (2.4); the contract text; the null outcome for an implementation source other than diff | D→CP→B→C (schema) | `handoffs/vocabulary.yaml`, `references/grounding-policy.json`(+), `references/artifact-contract-plan.md` (grounding section), `references/null-outcomes.json`, `scripts/grounding_table.py`(+), `scripts/tests/test_grounding_table.py`(+) | own + `test_null_outcomes.py` | G1-1, G1-2 | C FR-11, 13, 38, 49; D FR-59; E FR-23 | 5, 8, 16, 17 |
| G1-4 | S3 wiring. The exit gate calls `grounding_table --check` plus R6/R7; S3 form keys plus `CLAIMS` verifiers; a `gate-registry.json` row (if `gate_registry.py --check` names the site); the strategist text (FR-38: the fields are named before the work; the new inputs; step 5/6 blast radius rewritten onto B-n); `phases/s3.md` | D→CP→B→C | `scripts/planning_contract.py`, `handoffs/s3-strategist-to-designer.yaml`, `scripts/handoff_check.py` (`CLAIMS`), `references/gate-registry.json`, `agents/qa-test-strategist.md`, `skills/qa-story/phases/s3.md` | `test_s3_s4_chain.py`, `test_plan_contract_text.py`, `test_handoff.py`, `test_gate_registry.py` | G1-3 | A FR-1, 4, 5; C FR-11, 38, 39, 42; D FR-18 | 5 (phase↔driver, gate rows) |
| G1-5 | The stops. Wrong MR, not implemented and >50% each get a closed question (human-questions.md: price and consequences per option, the areas to re-test beyond the ticket from B-n). The moves: `go_on` (words recorded, S3 goes on to the plan) and `return_to_developer` (the story stops in a recorded state with a door back: `rework` from S1 with a new MR, FR-40). The 30% road is a report line. Free words go to the conductor (P22) | D→CP→B→C | `scripts/story_run.py` (functions named by the node's spec), `references/question-vocabulary.json`, `references/human-questions.md` (if a new card), tests | `test_human_questions.py`, `test_no_move_seam.py`, the `test_story_run_*.py` file that judges S3 | G1-4, fork 1 | A FR-2, 42, 48; B FR-6–9; E FR-20 | 5 (one question per stop), 18 (A27) |
| G1-6 | Report. The S8 regression line and "Left with you" read the S3 `blast_radius`/`regression_recommendations` (one source, FR-10). The refactoring share and its road get a report line (FR-41: `n/a` printed) | D→B→C | the S8 reader (named by the node's designer: needed beyond this manifest) | the reader's test file | G1-4 | E FR-20, 35; B FR-10 | 5 (delivery readers) |
| G1-7 | The FR-22 road per fork 6. The bug-draft contract gains `origin: grounding` with `grounding_ref` instead of `case`/`triage_ref`. The gate-B rehearsal and `undrafted_discrepancies` read it. Sibling fix: `handoff_check._claim_bug_has_a_draft` globs `*.md`, while drafts are `*.json` (`artifact-contract-run.md:69`, `gate_brief.py:2617`). The FR-22 debt row goes | D→CP→B→C | `references/artifact-contract-run.md`, `scripts/gate_brief.py` (`undrafted_discrepancies`), `scripts/handoff_check.py` (`_claim_bug_has_a_draft`), the gate-B draft check site, `design/factory-rules-debt.md` | `test_gate_brief_and_retro.py`, `test_bug_records.py`, `test_gate_preflight.py` | G1-4 | E FR-21, 22, 34; D FR-18 | 4, 5 (triage readers: no triage row is made) |
| G1-8 | Role-text versus code, one verdict per site (§6). `qa-scout.md:62,66`; `qa-requirements-tester.md:140`; `artifact-contract-grounding.md` «Checked»; `exit_gate.py:702-706` message; `s1-scout-to-tester.yaml:106-107`; `factory-rules-debt.md:23` (FR-21). Direction per fork 16 | B (docs) + C on the `exit_gate` text | the files named | `test_exit_gate_grounding.py`, `selftest.py --lang` | G1-1, G1-7 | C FR-37, 38 | 4, 5 |
| G1-9 | Measurers and the live proof. `stage_compare`/`code_friction` learn `grounding.yaml`; the S3 cost before/after; the live-run row (fork 9) | B; the live run is Lead/owner | `experiments/measurers/stage_compare.py` (+ its test) | `tools/`-side measurer tests (axis 6) | G1-5 | F FR-25, 28, 51, 55; G FR-33 | 6 |

FR text the batch implies (the Lead writes it; designers do not):
- amend **FR-22** *Check* to name the grounding road;
- amend **FR-49** *Check* to name `grounding.yaml` and its S3 readers;
- a candidate new rule: "every change of the implementation and every requirement are accounted for against each other before a plan is written".

The next free number is a question. `factory-rules.md` ends at FR-59, but SIBLING_MAP axis 8 cites an "FR-60" that the
rules file does not hold.

Axis enumeration (`docs/SIBLING_MAP.md`, 18 axes):

| Axis | Verdict |
|---|---|
| 1 | n/a: no deployment policy change. |
| 2 | n/a. |
| 3 | n/a here; it rides release hygiene. |
| 4 | Covered by G1-7 and G1-8; Lead writes FR text and regenerates the index. |
| 5 | Covered. Phase↔driver (G1-4/5), one question per stop (G1-5), null outcomes (G1-3), gate rows (G1-4), delivery readers (G1-6), triage readers (G1-7). |
| 6 | Covered by G1-9. |
| 7 | Covered by G1-1. `diff_pass.parse` uses `str.splitlines()` (`diff_pass.py:37`), which axis 7 forbids for line-number mapping. |
| 8 | Covered by G1-3: the artifact path goes through the resolver. |
| 9 | Covered by G1-1 and G1-2. `exit_gate.new_production_files` is a private recognizer that the axis-9 "open sides" do not list; G1-1 folds it. |
| 10 | Covered by G1-2: it reads the checkout through `_impl_checkout`, not a new walk. |
| 11 | n/a. |
| 12 | Fork 8. |
| 13 | Covered: the brief link is path-checked by `brief_pack`. |
| 14 | n/a. |
| 15 | Covered: new CLIs call `console_io.utf8_stdio`. |
| 16 | Covered: JSON goes through the one reader. |
| 17 | Covered: the checker prints the detector verdict shape. |
| 18 | Covered by G1-5 (an A27 site goes through `Driver.no_move` or `# remains`). |

## 4. Forks

- **F1. Where the step sits** (the owner decided WHO; WHERE stays open).
  - (a) Inside the S3 dispatch: table, then blast radius, then a halt with `verdict: blocked` before the plan if a stop is
    owed. Pro: one context, and the diff is read once at S3. Con: a long dispatch.
  - (b) An S3-entry sub-step: a first strategist window whose exit is R1–R6. Then code computes the share and asks the
    stop question, and the second window writes the plan. Pro: the stop needs no mid-dispatch halt, and the cost line is clean.
  - (c) A new stage between S2 and S3. Con: S-ordinals are hard-coded — `brief_pack.STAGE_ORDER` (range(10)),
    `window_budget.FALLBACK_ORDER`, `report_facts.GATE_A_STAGES`, `story_run._act_prepare_stage`
    (`("S1","S2","S3")` → `stage_simple`, else `getattr(self, f"stage_{stage}")`), `stages.json` `requires`.
  - Invariant: the person answers a wrong-MR / not-implemented / >50% question BEFORE any plan row is written; no plan
    spend on a rejected MR.
  - Recommendation: (b).
- **F2. Who labels — DECIDED (owner 19.10):** the S3 planner (`qa-test-strategist`). Consequence: the role has no Bash
  (`agents/qa-test-strategist.md:4`), so everything computed is precomputed by code and re-checked at exit (FR-11, FR-56).
  See F13.
- **F3. Unit of the table.**
  - (a) File.
  - (b) Function: the hunk-header context is language-dependent (P2) and empty for many files.
  - (c) Hunk, with rows allowed to group hunks and `all:<file>`.
  - Invariant: no changed line sits outside every row.
  - Recommendation: (c).
- **F4. Refactoring — HALF DECIDED (owner c).** >30%: a report line, plan rows and regression entries; >50%: a stop
  question with go_on / return_to_developer. Still open:
  - (a) Is the policy file overridable per project (config key)? The owner gave the numbers, and FR-13 permits a data
    override.
  - (b) What is the plan row for refactoring under 30%? Options: none, regression entry only, or parity rows (the A4
    "behaviour unchanged" idea).
  - Invariant: no refactoring hunk passes unseen; at least a report line names it.
- **F5. Threshold or judgement — DECIDED (owner c):** thresholds 30/50 as data; the measure is proposed in §2.4. The Lead
  confirms the measure (lines; T = production only) or picks hunks/functions.
- **F5b (new). When "unrelated" stops.** The owner gave no number.
  - (a) Any production hunk labelled `unrelated` asks.
  - (b) A share threshold in the same policy file.
  - (c) Stop only when no requirement is `implemented`.
  - Invariant: a wholly wrong MR never reaches a plan.
  - Recommendation: (c) stops; (a) as a non-blocking gate A question.
- **F6. The FR-22 road.**
  - (a) Code drafts a candidate from a `discrepancy` row the role wrote (fields copied, `confirmation: unconfirmed`).
  - (b) The role drafts it (needs a Write permission on `work/bug-drafts/`, FR-39).
  - (c) The row travels, and S8 drafts it at gate B.
  - Timing: before or only after the person answers "the requirement stands" (P20 reading).
  - Invariant: a code-reading never confirms a bug and never by itself moves the delivery verdict (the verdict stays with
    `delivery_verdict` kinds).
  - Recommendation: (a), after the answer.
- **F7. The "before" code.**
  - (a) The `-` lines of the diff (`diff:-<path>:<line>`, already legal in `contract.claim_row_errors`).
  - (b) The base revision read on demand. This needs Bash, which the strategist lacks, so it could only be a
    code-precomputed slice of the touched files at base.
  - (c) A stored snapshot.
  - Note: `kb/06-roadmap.xhtml:47` item 3 is a RUNTIME behaviour snapshot (API answers before the merge), not base code.
    It stays v1 and out of this batch.
  - Invariant: `before: unknown` is said, never guessed (`contract.py:653-656`).
  - Recommendation: (a), plus (b) precomputed only for files with a claim.
- **F8. Where the work lives.**
  - (a) A new pile `grounding`.
  - (b) Nodes in `conductor`: its zone is P22 and `story_run`/`controller`, and only G1-5 is in it.
  - (c) Split: G1-5 goes into conductor, the rest into a new pile.
  - Recommendation: (a), with an `очередь:` line for G1-5.
- **F9. The live proof (FR-33).**
  - (a) A cmp run on a 13797 copy: the table N of N, the S3 cost and friction before/after.
  - (b) Seeded copies: another ticket's diff gives the wrong-MR stop before the plan; injected refactoring above 50% gives
    the stop card, and 30–50% gives the report line and plan rows.
  - (c) TP1-15045, the cmp2 refactoring case (R-17: 400 before / 403 now): a behaviour_change with before/now.
  - Invariant: a person hand-filling the table proves nothing.
  - Recommendation: (a) + (b); (c) if a copy exists.
- **F10 (new). The oracle of a risk row** (P20, FR-58).
  - (a) A risk must attach to an existing R (`requirement:R-n`).
  - (b) Project-wide invariants as a new oracle form (`invariant:<class>` from project-profile).
  - (c) Otherwise `oracle_unknown` plus a question.
  - Invariant: no risk row asserts what the code does.
  - Recommendation: (a), else (c).
- **F11 (new). The plan-row kind.**
  - (a) A new row kind.
  - (b) A ref form in the existing `risk_source_refs` (2.2).
  - Note the name clash: `derived_risk` is ALREADY a register `requirement_kinds` word (`vocabulary.yaml:126`).
  - Recommendation: (b).
- **F12 (new). The label set.** The brief's four labels, plus `infrastructure` (`judge_diff._ac_criteria` already uses
  the word), `test_code` (developer tests feed existing coverage) and `unclassified` (an honest unknown, FR-59).
  - Invariant: no hunk is forced into a wrong label.
- **F13 (new). Tools of the strategist.**
  - (a) Code precomputes at dispatch preparation and the exit re-checks.
  - (b) Give the strategist Bash: P14/FR-56 cost, about 10K tokens a turn.
  - Recommendation: (a).
- **F14 (new). A behaviour change found at S3 that S2 did not register.** The S2 form says the strategist "may not add a
  requirement" (`s2-tester-to-strategist.yaml:9`).
  - (a) `rework` S2 with the list (the existing route).
  - (b) The strategist raises the before/now question itself, and the hunk's plan row stays `oracle_unknown`.
  - (c) R4 refuses and the conductor decides.
  - Invariant: a code-only behaviour never becomes an oracle, and the register keeps one writer.
- **F15 (new). S2 `diff_accounting`** (per file, an optional placeholder).
  - (a) Keep it.
  - (b) Retire it in favour of the S3 table.
  - (c) Derive it.
  - Invariant (FR-10): two carriers of one fact may not disagree.
- **F16 (new). Direction of the role-text versus code fixes** (§6): change the text to the code, or the code to the text,
  per site. Example: the `observables[].source` check that `artifact-contract-grounding.md` claims (code to text adds an
  S1 gate).
- **F17 (new). `judge_diff.py`.**
  - (a) Wire it as a first-guess pre-fill (`judged` rows the role confirms; cap `MAX_HUNKS` 80 — past it, no guess,
    never "skipped").
  - (b) Retire it.
  - (c) Leave it dormant.

## 5. Edges (behaviour and the invariant each protects)

- **E1 empty diff** (`source: diff`, 0 hunks). The table is empty, and every requirement is `not_implemented` or
  `outside_diff`, so R6 stops with "give the right MR / go on requirements-only / stop".
  Invariant: a 0-of-0 table is never a green completeness gate.
- **E2 tests-only diff.** Hunks are `test_code`, `T = 0`, so `percent: n/a`. The reverse check finds no production hunk
  behind any requirement, so the not-implemented stop fires with an added reading "the task is test-only by design".
  Invariant: no requirement is reported implemented without a production hunk.
- **E3 generated files** (lockfiles, bundles, snapshots). Code marks `infrastructure_suggested` from data and the role
  decides. A row `hunks: all:<file>` with `infrastructure` is legal without reading every hunk; the report lists such files
  by name, and their lines leave `T`.
  Invariants: no file is excluded from the index by code; a change hidden in a "generated" file stays visible.
- **E4 requirement with no observable in code.** `outside_diff` with `where`. `none` becomes the existing gate-A
  question (`agents/qa-test-strategist.md` step 2).
  Invariant: `outside_diff` is never `implemented`; no plan row counts it as covered by this MR.
- **E5 a hunk the role cannot classify.** `unclassified` with a reason and a question (owner `dev_arch`, non-blocking).
  It counts in the share numerator and enters regression scope.
  Invariant: an unknown is never reported as a label (FR-41); it errs toward the question.
- **E6 a ticket with no AC — the normal case** (owner d). The reverse check runs over register rows whatever their
  source (`inferred`, description, comments, attachments, diff claims). An empty register means S2 is already `blocked`.
  Invariant: no gate counts ACs; code never becomes the oracle for want of an AC.
- **E7 no diff** (`ungrounded` / `current-code`). The step does not run. Code writes the declared null outcome from
  `pipeline.implementation_source`, not from the role's word.
  Invariant: an absent table is legal only off `diff`.
- **E8 several repositories.** Every `impl-diff*.txt` is indexed. Hunk ids are global, and `repo` is on each hunk.
  Invariant: the second repository's hunks are never dropped. Today `handoff_check._diff_counts` reads `impl-diff.txt`
  alone while `grounding_errors` globs `impl-diff*.txt`, and G1-1 unifies them.
- **E9 the MR moved / `ticket_changed` re-runs S2–S3.** R5. `--refresh` keeps the rows of hunks with an unchanged sha
  and re-validates R ids against the new register.
  Invariant: a label measured on other bytes never counts.
- **E10 a huge diff** (the 360 KB UI case). The index has no cap; the role groups by file.
  Invariant: no truncation means no under-count. The only caps are a refusal's byte ceiling, with the full list in a file
  (C2-1), and `judge_diff`'s 80 if F17(a).
- **E11 zero-hunk files** (binary, rename-only, mode). There is one pseudo-hunk per file, and a pure move lists its
  callers in the blast radius at line weight 0.
  Invariant: no changed file is invisible.
- **E12 boundaries.** Tests sit at exactly 30.0% / 50.0% (no road / notify only) and at +1 line beyond each threshold;
  `T = 0`; an unreadable policy file means `road: stop` with the reason (safe default, FR-59).
  Invariant: "больше" is strict and the comparison is integer, with no float rounding.
- **E13 no checkout / another language.** `callers` and `tests` are `unmeasured: <reason>`; a `matters: yes` area with
  unmeasured tests needs `add_tests` or `not_needed`.
  Invariant: "not measured" is never written as "none".
- **E14 a mixed hunk.** The hunk is listed in two rows. It is `W`-weighted if any of its rows is refactoring.
  Invariant: the error goes toward the question.

Conflicting pairs:
- **P1 several stops at once.** Wrong MR is asked first; not-implemented and >50% wait (they are moot if the MR changes).
  Invariant: the person is not asked about the behaviour of code they may reject.
- **P2 the S1 "read every hunk" rule vs `all:<file>` infrastructure rows.** Allowed, named in the report.
- **P3 `exit_gate.grounding_errors` at S2** (a new module needs a `derived` row) **vs a `refactoring` label at S3.** Both
  stand, and the S2 gate is unchanged.
  Invariant: the 13797 class (limits of a new module missed) is still caught.
- **P4 an early FR-22 candidate vs an S7 `APP_BUG` draft for the same R.** One bug at gate B: the S7 draft names the
  candidate in `possible_duplicate`.
- **P5 the owner's "add to the plan" (30%) vs the size cap** (strategist step 4). The rows are planned and flagged
  over-cap, never silently cut.
- **P6 `return_to_developer` vs P8 comparison runs.** It writes nothing outward; it is a stop and a report line.
- **P7 S2 owns the register vs S3 finds an unregistered behaviour.** F14.

Reused functions in a gate role (designer rule 1):
- **`diff_pass.parse`** (advice to gate). It may over-count (an extra row costs a label), never under-count or
  misattribute. Adversarial inputs, from `diff_pass.py:52-59`, where header tests run before the in-hunk test:
  - a REMOVED line whose text starts `-- ` (SQL, Lua, Haskell comments) arrives as `--- …` and is taken for a header,
    dropping the line;
  - an ADDED line whose text starts `++ ` arrives as `+++ …` and re-points `current["path"]` mid-file;
  - a path holding ` b/`;
  - a combined `@@@` diff, where `HUNK_RE` fails and the lines are silently ignored: refuse, never skip;
  - `\ No newline at end of file`;
  - CRLF and U+2028 (axis 7);
  - `@@ -0,0 +1 @@` with the count omitted;
  - `Binary files … differ`.
- **`test_files.is_test_for`, consumer `grounding`.** Safe direction: production (a false "test" drops lines from `T`
  and from requirement accounting).
- **`contract.implementation_only` as the link check for `behaviour_change`.** Its error already goes toward a claim
  (`contract.py:406-410`).
- **`exit_gate.grounding_errors`.** Unchanged, not promoted.

## 6. Role text versus code (fixed on the way, one verdict per site; direction per F16)

The brief says three; the digest lists four, and the reading found five more.
1. `artifact-contract-grounding.md:27-28` says "every observable carries a `source`"; the validator does not check it.
   Verdict: G1-8, per F16.
2. `qa-scout.md:66` uses `derived: mr-diff`, a token with no reader. Verdict: G1-8; the text moves to the `derived` grammar.
3. `factory-rules-debt.md:23` still lists FR-21 as open. Verdict: G1-8 (doc).
4. `exit_gate.py:702-706` does not mention the Behaviour-claims gate. Verdict: G1-8.
5. NEW: `qa-scout.md:62` and `qa-requirements-tester.md:140` say `implementation_source: none`. `vocabulary.yaml:135`
   and `stage_done.py:60` allow only `diff | current-code | ungrounded`. Verdict: G1-8.
6. NEW: `handoff_check.py:503` reads `work/bug-drafts/*.md`; drafts are `*.json` everywhere else (`gate_brief.py:2617`,
   `delivery_summary.py:226`, `artifact-contract-run.md:69`). Verdict: G1-7.
7. NEW: `s1-scout-to-tester.yaml:106-107` says "the S2 exit gate compares the numbers". No compare of `inputs_read`
   handed/read exists: the grep of `handoff_check/exit_gate/handoff/stage_done.py` for `production_files_accounted_for`
   found 0, and the same form found `handed` elsewhere. Verdict: G1-8 (text), or G1-4 if F15 makes it true.
8. NEW: there are two private "production file" recognizers, `exit_gate.NOT_PRODUCTION` and
   `handoff_check._production_files`, and two hunk counters, `^@@ ` (`handoff_check.py:223`) and `HUNK_RE`. Verdict: G1-1.
9. NEW: SIBLING_MAP axis 8 cites FR-60; `factory-rules.md` ends at FR-59. Verdict: Lead (the number for the new rule).

## 7. Small choices I closed
- The table is YAML (P4).
- Hunk ids are global `H-n` with a sha for staleness.
- Rows may group hunks.
- Thresholds and the measure live in one data file.
- The stop uses the existing S2/S3 `blocked` with `open_questions` (FR-42 already has the branch).
- The dated rule follows the `contract.ORACLE_CUTOFF` precedent: stories created before the cutoff are legacy and are
  not refused.
- The brief's "S3 entry refuses a plan" is read as the S3 EXIT gate, because no plan exists at entry.
- No AC→register gate is built (owner d; the digest's gap Q3-1 is not this step).

## 8. DoD of this draft and of the batch
- This draft: the sections above; ≤ 400 lines; no repo file edited.
- Each node: inline DoD with the exact run, `python -m pytest ai-packages/qa-factory/scripts/tests/<own files> -q`
  (form per `plans/builder-rules.md`, to be confirmed by the node spec), plus `python -B scripts/selftest.py --limits --lang`
  and `scripts/tests/test_audit_rules.py`. Docker python:3.12 runs before the merge; the R1–R8 boundary tests sit AT and
  BEYOND each limit (E12).

## 9. Reading trail
Read:
- the digest t-925 (whole);
- `exit_gate.py:640-899`;
- `handoff_check.py:175-226, 300-345, 380-609`;
- `contract.py:390-470, 560-729`;
- `gate_brief.py:2611-2620, 2680-2724, 2790-2900` (grep);
- `diff_pass.py`, `judge_diff.py` and `plan_row.py:1-90` (whole);
- `diff_scope.py:1-40`;
- `s5_precheck.py:700-775`;
- `story_run.py:10740-10770`;
- the handoffs `s1`, `s2`, `s3`, `vocabulary.yaml`, `index.yaml`, `README.md`;
- `agents/qa-requirements-tester.md`, `qa-scout.md:1-128`, `qa-test-strategist.md:1-109`;
- `references/human-questions.md:1-80`, `artifact-contract-grounding.md`, `artifact-contract-plan.md:25-64`,
  `artifact-contract-run.md:66-91`;
- `repo_map.py:1-40`;
- `factory-rules.md:40-488`;
- `docs/SIBLING_MAP.md` (headings, 82-226);
- `docs/factory-map/qa-factory-paths.md:95-166`;
- `kb/06-roadmap.xhtml:47`;
- `plans/piles/_template/batch.md`, `conductor/batch-2-cmp3-classes.md:1-94`, `conductor/README.md:1-40`.

Greps, with their positive controls:
- `bug-drafts` over the package;
- `risk_source_refs|required_scenarios`;
- `blast radius`;
- `implementation_source` in `stage_done.py`;
- `\*\*FR-6\d` (0; control `\*\*FR-5\d` found FR-50…);
- `handed|production_files_accounted_for` (control found `handed`);
- `def stage_S\d` (control: S4–S9 found).

Not read: `docs/DECISIONS_ARCHIVE.md` and the archive A4 text (no git tool; the digest's trail is relied on);
`references/null-outcomes.json` and `gate-registry.json` bodies (existence only); the S8 "Left with you" reader.

## L. The Lead's decisions on the forks (19.10.2026, Fable; the owner's where marked) — the input of critic on plan t-929

- F1: a FIRST S3 WINDOW (the designer's recommendation): the person answers a stop before any plan exists; no new stage number (S0–S9 are hard-coded in several scripts — the invariant: no renumbering). Invariant kept: the S3 exit still refuses a plan with an unplanned risk row.
- F2 (owner, D-0049): the S3 planner labels; code prepares the indexes before the role starts (F13 = code; the planner keeps no Bash, P14/FR-56).
- F3: unit = HUNK; a row may cover a whole file (the error direction: a file row can hide a hunk that implements a requirement — the completeness gate counts hunks, so a file row must list the hunks it covers).
- F4 (owner, D-0049): 30 % / 50 % as data; NO per-project override in this batch (P2 keeps the data file, an override is a later word of the owner); refactoring under 30 %: one report line, no plan rows.
- F5 (owner's thresholds; the measure is the Lead's): refactoring + unclassified changed PRODUCTION lines over all changed production lines, integer, strict «>», erring toward the question; tests and config are OUT of the denominator; the two disputable readings are printed on the 50 % question.
- F5b: STOP only when the diff implements NO requirement of the register (wrong MR); otherwise a non-blocking question. Invariant: a stop is never silent (FR-4) and names its door (FR-57).
- F6: the bug candidate (FR-22's road) is drafted by CODE after the person's answer, from the discrepancy row; the role words it later at S7 if it stands. Invariant: a discrepancy a person confirmed never leaves the run without a `bugs/` record.
- F7: the «before» code = the removed lines of the diff + a code-prepared base slice (the base commit, read on demand) for files that carry a claim; no stored runtime snapshot (roadmap item 3 stays v1).
- F8 (OWNER, 19.10 15:0x: «новая кучка»): a NEW pile `grounding`, one batch for the step + the vocabulary node (P23) as its first node.
- F9 (OWNER, 19.10 15:0x): the live proof is collected on a copy of TP1-15045, not 13797 («доказательства лучше собирать на 15045»); seeded wrong-MR and refactoring copies of the same story; 13797 only as a control if cheap.
- F10: the expected value of a risk row = an existing requirement, else an OPEN question (`unresolved`, never a literal — P20/FR-58).
- F11: no new plan-row kind; reuse `risk_source_refs` with `grounding:K-n` / `blast:B-n`; `derived_risk` stays the requirement kind it already is (`vocabulary.yaml:126`).
- F12: labels = the brief's four + infrastructure, test code, unclassified (data, FR-13); «unclassified» counts toward the refactoring share (F5).
- F14: a behaviour change found at S3 that S2 never registered → the planner registers it as a claim row (P20, before/now) and asks the person; S2 is NOT sent back (cost; FR-7 no re-asking).
- F15: RETIRE S2's per-file `diff_accounting` in favour of the grounding table as the one carrier — the critic confirms no reader is left behind (FR-14/FR-40: the old key stays readable in stored artifacts).
- F16: per site, the critic of the vocabulary node decides which side moves: the text where the code is the measured truth, the code where the text states the rule's intent.
- F17: `judge_diff.py` RETIRED (no call site, the judge provider is none); its removal is a node row with the clone ratchet and `test_audit_rules` as the witness.
- Open for the owner: none beyond F4's future override and F9's stand (a 15045 copy must exist on the stand — the Lead checks before the live-proof node; the stand checkouts are the owner's).

## L-2. The owner's words (D-0051, 19.10 15:1x) and the Lead's answers to critic t-929 (the fix round of the plan; the re-review carries this section)

Owner (supersedes §L where they differ): (1) the share's denominator is PRODUCTION code (F5 stands; tests and config are out — the owner's word, not the Lead's). (2) REQUIREMENT COVERAGE replaces §L F5b: the table yields the share of the register's requirements the diff implements; «< 50 % implemented» = the wrong-MR class → STOP with a closed question; «≥ 50 % but not all» → a plan line the person cannot miss (the gate brief's first lines + the «Left with you» regression entry); 100 % → nothing to say. (3) FR-22's road (replaces §L F6): a suspicious spot → a `derived_risk` plan row → a test → an ordinary test-found bug; where no test can be written → a report line «bug candidate / gap / question» (the three kinds exist: `delivery-verdict-kinds.json`, gaps, `human-questions.md`), never a silent loss; code drafts nothing by itself. (4) The planner writes the claim row into the register (replaces §L F14; critic F-12): `artifact-writers.json` gains the S3 planner as a writer of `## Behaviour claims` rows only, with the row's `origin: S3-grounding`; and a NEW principle for the grounding batch to add to PROJECT.md: a role that found a problem always has a place to record it (the owner: «не должна теряться только потому, что он не может никуда её записать»). (5) S2 `diff_accounting` retired (F15 stands) with its seven readers migrated to the grounding table, each reader's meaning pinned by a test before the field goes (critic F-13: the migration is a node of its own, before the retirement). (6) `judge_diff.py` stays DORMANT (replaces §L F17: no removal node).
Lead on the remaining majors: F-2 — nodes added to batch 1: G1-0 vocabulary (P23, census t-928, D-0050), G1-1a the S3 two-window driver (F1), G1-7 the `diff_accounting` reader migration (before the retirement), G1-8 the base slice (F7), no F6/F17 nodes (the owner's (3) and (6)). F-3 — the S3 gate runs in `controller.py:3312`: the gate node owns that function by name; `очередь: codex/1 → grounding/1` on `controller.py`, `story_run.py`, `exit_gate.py`, `brief_pack.py` written in BOTH batch files at placement (codex/1 goes first). F-4 — three production-file recognizers on main (the third in `runtime_probe.py`): one reader, the S2 gate's behaviour pinned before and after (a census test). F-5 — the measure: a hunk's label is its STRONGEST claim (implementation beats refactoring when both are true), so a one-line implement+rename diff is 0 % refactoring; a pure move counts its moved lines as refactoring (not 0 %); rename-only refactoring counts. F-6 — code's file kind decides the denominator (production vs test vs config vs generated), the role's label never changes it. F-7 — one parity question per refactoring GROUP (the role groups hunks), not per row. F-8 — the 30 % notice goes into the S3 gate brief (the person sees it at the plan, before tests). F-9 — refusal R7 names the form field to fill, no CLI for a role without Bash (FR-2). F-10 — hunk ids are content hashes (file + normalized hunk text); a refreshed diff re-attaches labels by id and lists the orphans. F-11 — the blast radius reads the checkout at the RECORDED implementation commit (the S5 `Branch check:` carrier of codex CX1-7), refusing another revision by name.

## L-3. The Lead's answers to the re-review t-937 (fit_with_fixes, 6 new major G-1..G-6, 4 minor; 19.10.2026)

G-1 (the owner's (4) kept, the one-writer rule kept): the planner writes its claim rows into ITS OWN `grounding.yaml` (the S3 handoff carrier); CODE appends them to the register through the existing `raise_questions` door as `## Behaviour claims` rows with `origin: S3-grounding`, the `## Register` row, the `ids:` entry and the readiness `open_questions` entry in one move (one writer of the register stays S2's tool; the planner never edits the file). Invariant: a claim the planner wrote is in the register before the S3 gate closes, or the gate refuses naming the claim. G-2 (the coverage denominator): the register rows gain `delta: new | changed | unchanged` set by the S2 tester (what the ticket asks to change; `unchanged` = behaviour already present before the MR — checked against the base slice, F7); COVERAGE = implemented rows with `delta ≠ unchanged` AND `origin ≠ diff` over all such rows; diff-derived claims never enter the numerator or the denominator (they are claims to confirm, P20). The two concrete errors of the review become the two pinned tests. G-3: the implementation commit is RECORDED by the grounding step itself (the checkout HEAD at the moment the diff is read, `grounding.yaml: implementation_commit`); S5's `Branch check:` (codex CX1-7) compares against it, never the other way; a different HEAD at S5 → a refusal naming both. G-4: the former G1-7/G1-8 contents (the `*.md` glob bug of handoff_check.py:503, the FR-22 debt row, the §6 role-text-vs-code sites) return as G1-9 and G1-10; the §3 table is rewritten by the placement builder from §L/§L-2/§L-3 (the draft body is not edited by hand). G-5: a new kind `bug_candidate` in `delivery-verdict-kinds.json` (FR-13: data), mapping to the THIRD verdict `after_checks` with its «Left with you» line (P21: the person decides; a candidate is not a confirmed failure); the `derived_risk` name stays a requirement kind only (§L F11), the plan row refers to it by `risk_source_refs: grounding:K-n`. G-6: an unimplemented requirement is kind `pending_implementation` in the SAME file, BLOCKING (the FR-21 class: the product lacks what a requirement demands), never a «Left with you» line. Minors F-14..F-22 and G-7..G-10: rows of the batch's «Остатки» at placement, each with its site; G-10's existing carriers (findings files, the handoff `open` section, gaps) are the roads the new principle names — no new carrier. Next: placement of pile `grounding` (batch 1 from §2 + §L..§L-3) by a builder; the vocabulary node G1-0 first; every node gets its own critic on plan.

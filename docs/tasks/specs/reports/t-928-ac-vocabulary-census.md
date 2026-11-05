# t-928 — AC vocabulary census (recon, read-only)

Serves PROJECT.md P23 / DECISIONS D-0049. Verdicts are PROPOSALS (R reword · K keep · C code identifier · U unclear); the Lead decides.
Row = one site or a group of sites of one file (line numbers are the hit lines). `(q)` = quote/history, `(fp)` = false positive, `(schema)` = stored artifact/config key (edge b).
Tests: `t_` = `ai-packages/qa-factory/scripts/tests/test_`, `fx` = `.../tests/fixtures/`. No test pins a wording unless the last column names it.

## Commands (verbatim) and controls
- DoD command: `grep -rniE "acceptance criteri|\bAC\b|\bACs\b|\bAC[0-9]" ai-packages/qa-factory/design/factory-rules.md`
  -> lines 94, 247, 268, 304, 308 (FR-21), 310, 318. POSITIVE CONTROL PASSED (FR-21 at 308).
- Working regex (all scopes): `acceptance criteri|\bACs?\b|\bAC[0-9]|acceptance_criteri`, case-insensitive; tools: Bash grep -E and the Grep tool.
- LINE-WRAP GAP of the DoD command: it is line-oriented and MISSES `acceptance` / `criterion` split by a newline. Multiline pass
  (Grep `acceptance\s*\n\s*criteri`, multiline, over the package + PROJECT.md + index + builder-rules + critic-brief + .claude/agents) found 2 more
  hits: factory-rules.md:257-258 (FR-58) and scripts/source_inventory.py:1800-1801. Both are in the table.
- Negative claims and their controls (same tool, same pattern shape):
  - handoffs/*.yaml hold no AC word: `grep -rniE "acceptance|\bACs?\b|\bAC[0-9]|criteria"` there finds only README.md:19 and vocabulary.yaml:214 (fp);
    control: the same shape with `oracle` finds 12+ lines in the same directory.
  - delivery-verdict-kinds.json, human-questions.md, artifact-contract-plan.md, phases/s3.md: 0 hits of `criterion|acceptance`;
    control: `grep -c blocked delivery-verdict-kinds.json` = 3.
  - docs/tasks/critic-diff-brief.md, plans/builder-rules.md: 0 hits; control: `grep -c requirement critic-diff-brief.md` = 1, `grep -c test builder-rules.md` = 10.
  - docs/SIBLING_MAP.md: 0 hits (Grep tool); control: the same tool/pattern finds .claude/agents/builder.md:23 and designer.md:17.
  - no script reads the digest token `AC/code conflict`: `grep -rn "code conflict" scripts/*.py` = 0; control: `grep -rn "tested the letter" scripts/*.py` = 4.
  - no test pins `Every acceptance criterion carries`, `When grounding is complete`, `consists of AC only`, `built from the criteria` (grep -rlF over tests = empty);
    control: `go on without criteria` -> t_story_run_s0.py with the same grep -rlF shape.
- Not read: testproject1-dev-fresh copies. Not censused (outside the seven scopes, counts only, same regex): plans/ 24, docs/RUNBOOK.md 6, tools/ 54,
  experiments/ 470, AGENTS.md 11 (GENERATED from CLAUDE.md+PROJECT.md+index, regenerates), DECISIONS.md 1.

## Totals (hit LINES by grep -c; rows and verdicts are in the tables)
| scope | hit lines | notes |
|---|---|---|
| 1 factory-rules.md / -debt.md | 7 (+1 wrapped) / 2 | |
| 2 PROJECT.md / FACTORY_RULES_INDEX.md | 8 / 1 | PROJECT: 47,101,111,136,138,140,141,177 |
| 3 package forms, references, roles, skills, design, evals | references 59, agents 16, skills 14, evals 6, design(other) 4, handoffs 0 (+2 fp) | |
| 4 package code scripts/*.py | 157 (+1 wrapped) | 21 are `import acceptance as AC` (fp); tests 642 (fixtures incl.) |
| 5 kb/ | 6 real lines in 4 xhtml + 1 html; ~60 more are the XHTML `ac:` namespace (fp) | |
| 6 dev carriers | critic-diff-brief 0, builder-rules 0, SIBLING_MAP 0, factory-map 3 md lines (+3 svg/html), .claude/agents 2 (fp) | |
| 7 records | t-925 digest: 23 lines (29 `AC`, 3 `ac`, 2 `acceptance_criteria` tokens); t-926 draft: 5 lines (5 `AC`, 1 `ACs`) | count only, no verdict |
CHANGELOG.md: 11 lines, all K (history, edge d). Verdict totals per scope: see the end of the file (counted by command).

## Scope 1 — design/factory-rules.md, factory-rules-debt.md
| site | phrase | V | proposal | pin |
|---|---|---|---|---|
| rules:94 (FR-50 Why) | "found 0 of 15 acceptance criteria" | K(q) | past finding, TP1-15045 | - |
| rules:247 (FR-18 Why) | "the story's own AC7 was undelivered" | K(q) | past finding | - |
| rules:257-258 (FR-58) | "from a requirement — an acceptance criterion, a spec, a precedent a person confirmed" | R | "from a requirement of any source (description, AC, comment, attachment, linked task, spec, a precedent a person confirmed)"; AC is named FIRST and ALONE among ticket sources | index line FR-58 has none; DoD grep misses it |
| rules:268 (FR-58 Check) | "`then_oracles`: `ac` / `spec` / `person` / `unknown`" | C(schema) | follows class C-ORACLE; also the list OMITS `precedent` though contract.py:395 has 5 words (stale list) | t_oracle_provenance.py |
| rules:304 (FR-20 Why) | "the ticket's AC7 is undelivered" | K(q) | past finding | - |
| rules:308 (FR-21 title) | "what an acceptance criterion requires blocks delivery" | R | "...what a requirement demands blocks delivery" (title is generated into the index and cited by P21) | `tools/factory_rules_index.py --check` (pre-commit) |
| rules:310 (FR-21 Why) | "the UI half of AC7 — stood `skipped`" | K(q) | past finding TS-12 | - |
| rules:318 (FR-22 Why) | "AC7 was found at S2 and decided by a person at gate A" | K(q) | past finding | - |
| debt:24 (FR-22 row) | "an acceptance criterion unmet in the product can never produce a red test" | R | "a requirement unmet in the product..." (axis 4: move with rules:317-321, whose title already says "requirement") | - |
| debt:107 (FR-50 row) | "the agent route lost 15 of 15 AC" | K(q) | past finding | - |
FR-21 body (309-316) uses "skip", "product gap", `blocked-flow`: no further AC word. FR-5 line 63 "acceptance record" = window acceptance (fp).

## Scope 2 — PROJECT.md, docs/FACTORY_RULES_INDEX.md
| site | phrase | V | proposal | pin |
|---|---|---|---|---|
| PROJECT.md:47 (P5) | "агент потерял 15 из 15 AC" | K(q) | owner's word 01.10 | - |
| PROJECT.md:101 (P20) | "Ожидаемое значение берётся из требований (AC, спека, прецедент, подтверждённый человеком)" | R | list the sources as P23 does (описание, AC, комментарии, вложения, связанные задачи, спека, прецедент); AC currently the first of three | - |
| PROJECT.md:111 (P21) | "продукт не умеет то, что требует AC; FR-21" | R | "...то, что требует требование реестра; FR-21" | - |
| PROJECT.md:136-141 (P23) | the principle; names FR-21, P21, `then_oracles: ac/spec` as nodes to sweep | K | itself | - |
| PROJECT.md:177 (§Как принимается, п.5) | "S0 ... однажды потерял AC, комментарии и parent" | K(q) | history of S0 | - |
| docs/FACTORY_RULES_INDEX.md:46 | "FR-21 — ... what an acceptance criterion requires blocks delivery" | R | GENERATED: edit the rules title, run `python tools/factory_rules_index.py`; AGENTS.md regenerates from it | pre-commit `--check` |
§«Как принимается изменение пакета» rules 1-6: no other AC word (P20 `Then`/`oracle` text names "требования" already).

## Scope 3 — package forms, references, roles, skills, evals, design
### 3a handoffs
| site | phrase | V | proposal | pin |
|---|---|---|---|---|
| handoffs/*.yaml | no AC word (see negatives) | K | register/plan/case handoffs speak of `requirement`, `R-n`, `oracle` | - |
| handoffs/README.md:19, vocabulary.yaml:214 | "the acceptance refused the window" / `acceptance.validate_window` | K(fp) | window acceptance, not AC | - |
### 3b references/
| site | phrase | V | proposal | pin |
|---|---|---|---|---|
| artifact-contract.md:120,123 + slices/qa-case-designer/artifact-contract.md:118,121 | `then_oracles` `"source": "ac"`; "`source`: `ac \| spec \| ...`" | C(schema) | class C-ORACLE (the slice file is a twin: axis 5) | t_oracle_provenance.py, t_validators.py |
| artifact-contract.md:124 + slice:122 | "`precedent`: only when an AC names the parity with OLDER behaviour" | R | "when a requirement names..." | t_oracle_provenance.py |
| artifact-contract-json.md:118 | "a register built from AC alone while a parent feature exists" | K | rule about source breadth; keep, matches check_witness | - |
| artifact-contract-json.md:126 | origins `acceptance_criteria:AC-4`, `comment:...` | K | origin list names AC beside comment/parent/code | t_question_register.py |
| artifact-contract-grounding.md:14,27 | `acceptance_criteria` [] ; "Checked required keys `ticket`, `acceptance_criteria`, `implementation`" | C(schema) | class C-SNAPSHOT; empty list is already the stated shape (K) | t_audit_rules.py:126 (A11) |
| ahead-cards.json:20 | "`by_source` within ac\|story\|feature\|discussion\|assumption\|derived ... a register of AC alone while a parent feature" | K | class C-REQSRC | t_ahead_cards.py (REQ_SOURCES) |
| adapters-read.md:82 | "A description edited or an acceptance criterion dropped in [the window]" | K | AC named as one example of a moved field | - |
| coverage-design.md:12,17 + slices/qa-scout/coverage-design.md:12,17 | "read the description, acceptance criteria, links, every page of comments" | K | the model phrasing: AC one source among several (twin file) | - |
| gate-registry.json:401,403 | words `["ac","spec",...]`, `"ac": {"class":"matched"}` | C(schema) | class C-ORACLE (sites listed: contract.then_oracle_errors, resolve_then_oracle) | t_gate_registry.py (reads gate-registry.json; the `ac` words not opened) |
| jira-direct-access.md:37; jira-fields.json:3,19-21,43 | "acceptance-criteria field/section" ; names `Acceptance Criteria`, `AC` | K | where the AC field is READ: correct source-reading | t_ticket_light.py |
| judge.md:24 | "a recorded AC/code decision" | C | class C-CONFLICT: "requirement/code decision" | - |
| judge.md:65 | "S1 `judge_diff.py` — per diff hunk: which AC it implements" | U | class C-JUDGEDIFF: (1) AC is the only list that exists at S1, the register is built at S2; (2) with no AC the judge degrades (judge_diff.py:102 `not_ready`) and the scout reads all hunks | t_judge_discovery.py |
| judgments.d/discovery.json:96,98,100 | "which one acceptance criterion listed in `acceptance_criteria` does the hunk implement"; "none of the listed acceptance criteria" | U | same as above (judge prompt text + criteria keys) | t_judge_discovery.py |
| judgments.d/discovery.json:106 | calibration note "11-item AC/TR list" | K(q) | | - |
| judgments.d/results.json:166 | "A changed title, description, type or acceptance criterion, or comment text" | K | freshness severity list: AC one of several | t_ticket_adapter.py |
| judgments.d/results.json:173 | "drop AC2's lowercasing" | K(q) | fixture comment | - |
| judgments.json:54,71 | "States requirements, acceptance criteria or a design"; "expected behaviour or acceptance criteria of the work" | K | AC listed beside requirements/behaviour | - |
| question-prices.json:39 | `"unverified": "the acceptance criteria the ticket does not give"` | R | the S0 `go on` price label; class C-S0 | t_conductor_doors.py reads question-prices.json (line 39 not opened) |
| scout-recovery.md:43 | "Collect ... complete body/AC, all comment pages, all attachments" | K | AC one of several | - |
| templates/questions-for-owner.md:36,42 | "e.g. AC-4"; "from `acceptance_criteria:AC-n`" | K | reading-origin example | - |
| templates/requirements-register.md:5,6,26,29 | `by_source: {... ac: 0 ...}`; "`ac` alone while a parent feature"; row `source = ac`; "closed list: ... ac ..." | K | class C-REQSRC (AC is a legal source) | t_validators.py |
| templates/requirements-register.md:14-15 | "AC are the developer's checkpoints, one of six sources, not the boundary" | K | already P23-aligned: model wording for the other texts | - |
| templates/requirements-register.md:22,26 | column value `AC-1`/`AC-2` in the `ac_ref` column | C(schema) | class C-ACREF | t_validators.py |
| templates/ticket-snapshot.md:20,28,29,52 | "A summary of an acceptance criterion is a false oracle"; `ticket_light.acceptance_criteria`; heading `## Acceptance criteria` | K | the snapshot form reads the AC section; class C-SNAPSHOT/C-CONFIG | t_ticket_light.py, t_ticket_adapter.py |
| tester-manifesto.md:46 | "an acceptance criterion vs its parent story" (example of a conflict) | K | | - |
| vocabularies.md:33 | "`ac` <-> `requirement:`, `spec` <-> `external:`" | C | the case `basis` prefix for `ac` is ALREADY `requirement:` (hint for the rename: the word `requirement` exists) | t_oracle_provenance.py |
| vocabularies.md:36 | "`ac` — an acceptance criterion; `ref` is the register's R-n" | R | "`ac` — a requirement of the register read from the ticket's sources" (`spec` also has ref R-n: the two differ only by origin) | t_oracle_provenance.py |
| vocabularies.md:38 | "`precedent` — an AC names parity with OLDER behaviour" | R | "a requirement names parity..." | - |
### 3c roles (agents/)
| site | phrase | V | proposal | pin |
|---|---|---|---|---|
| qa-scout.md:34 | "`peek` each mention (description, AC, ...)" | K | source list | - |
| qa-scout.md:64 | "Flag a code/AC conflict (same observable, disagreeing...)" | U | (1) AC-only conflict kept; (2) any requirement source vs code; class C-CONFLICT | - |
| qa-scout.md:90,93 | "Every acceptance criterion carries at least one `observable` ... while an AC still lacks its observable" | R+U | the S1 completion criterion keys on AC: with no AC it is vacuous. (1) "every requirement statement found in the sources"; (2) wait for the grounding batch (t-926) which owns S1's completion | none (grep -rlF) |
| qa-scout.md:119,120 | halt token "Code contradicts an acceptance criterion" / `AC/code conflict: "<AC quote>"` | C | class C-CONFLICT | t_s1_s2_contract.py:116 |
| qa-requirements-tester.md:38 | "Keep confirmed AC, confirmed technical invariants, and derived risks distinct" | U | "confirmed AC" = confirmed requirement class; (1) keep; (2) "confirmed requirements" | - |
| qa-requirements-tester.md:46 | "`... ac \| derived`) and `inferred: true` where the story had no ACs to point to" | K | already P23-aligned (a story without ACs is expected); class C-REQSRC | t_validators.py |
| qa-requirements-tester.md:74,75,78 | "never a silent override of the AC, never dropped because it is not an AC"; "tested the letter of the AC" | K | contrasts comment vs AC; the 78 line is a finding (q) | - |
| qa-requirements-tester.md:104 | origins `acceptance_criteria:AC-n`, `comment:...`, `parent_ticket` | K | origin list | - |
| qa-case-critic.md:49,53 | "sources like the AC"; "AC-4's 'former position'" | K | 53 is (q) | - |
| qa-case-designer.md:55 | "`then_oracles` ... `ac \| spec \| precedent \| person \| unknown`" | C(schema) | class C-ORACLE | t_oracle_provenance.py |
### 3d skills (qa-story) and evals
| site | phrase | V | proposal | pin |
|---|---|---|---|---|
| SKILL.md:221 | "`qa-scout ... AC/code conflict`" | C | class C-CONFLICT | - |
| phases/s0.md:53 | "the criteria (the headings of jira-fields.json plus...)" | K | reading | - |
| phases/s0.md:79 | "acceptance criteria found -> the person's question too (it names the headings looked for ...)" | U | class C-S0: S0 asks when no AC. (1) a task may have no AC (P23) -> note, not a question; (2) keep the question for tickets whose AC section may exist but was not parsed (headings). Behaviour, not wording | t_story_run_s0.py |
| phases/s0.md:120 | "`requirements` (title, type, description, acceptance criteria) -> stop" | K | freshness severity; AC one of four | t_story_run_freshness.py |
| phases/s1.md:5,117 | "tracker keys discovered in descriptions, acceptance criteria, comments"; "`peek` reads ... acceptance criteria, parent and links" | K | source lists | t_source_peek.py |
| phases/s1.md:322,325,330,331,384 | heading "Digest `halt` — AC/code conflict"; "The acceptance criterion and the code disagree. AC: ...  test the AC and file the code as a bug?"; table row `AC/code conflict` | C+R | class C-CONFLICT; lines 330-331 are TEXT TO A PERSON (P9): "The requirement and the code disagree ..." | t_s1_s2_contract.py |
| phases/s2.md:5,53 | "confirmed AC, technical invariants, and derived risks"; "<AC/code conflict decision from S1>" | K / C | 5 as qa-requirements-tester:38; 53 class C-CONFLICT | - |
| skills/qa-story/evals/evals.json:236 | "no acceptance criteria is the person's question that names the headings" | C | pins the S0 behaviour; class C-S0 | the eval itself |
| skills/qa-story/evals/evals.json:256 | "requirements (title, type, description, acceptance criteria) stops before the gate" | K | freshness | - |
| evals/plugin-eval-benchmark.json:4,53,55,61,142; evals/fixtures/tickets/QA-1.md | fixture QA-1 with AC1-5; eval id `ac3-unimplemented-becomes-gate-a-question` | K | the fixture ticket HAS AC; no fixture/eval has a ticket WITHOUT AC (gap: add a sibling) | evals |
### 3e design/ (package)
| site | phrase | V | proposal | pin |
|---|---|---|---|---|
| design/driver.md:99 | "no criteria is the `ticket_incomplete` question" | C | class C-S0 | fx/driver-layers.json |
| design/driver.md:134, state-exits.md:118 | "(title, type, description, acceptance criteria)" | K | freshness list | - |
| design/codex-scout-reliability-plan.md:22 | "collect full body/acceptance criteria, all comment pages" | K | | - |
| design/dashboard-cost-repair-plan.md:20 | "requirements and acceptance criteria ... Codex integration and cost acceptance" | K(fp) | plan acceptance, not ticket AC | - |

## Scope 4 — package code scripts/*.py (tests listed in the class summary)
| site | phrase | V | proposal | pin |
|---|---|---|---|---|
| contract.py:395,398,625,727,734,767,773-774 | `THEN_ORACLE_WORDS = ("ac",...)`; refusal "a requirement read from the code is never an AC" (774); `ac:R-19` | C(schema) | class C-ORACLE; 773-774 refusal text -> R "never a requirement" (AC and requirement are conflated: only "never an AC" is said) | t_oracle_provenance.py, t_validators.py |
| contract.py:292 | `READING_ORIGINS = ("acceptance_criteria","description","comment","parent_ticket","code","test","precedent","person","claim")` | K | AC beside the other origins; no attachment/linked-task origin (U: sibling origin words) | t_question_register.py |
| contract.py:276,279,407 | comments: cmp2 finding "tested the letter of AC-4"; "no AC reference" | K(q) | history | - |
| contract.py:545-582 | `register_rows` -> key `ac_ref`; `implementation_only` requires `ac_ref` empty | C(schema) | class C-ACREF; error direction OK (empty cell -> claim, costs a question) | t_validators.py, t_oracle_provenance.py |
| planning_contract.py:343,381-422 | `ac_ref` in `{R-n: {text, ac_ref}}` and in contradiction statements | C(schema) | class C-ACREF | t_s3_s4_chain.py, t_gate_question_form.py |
| gate_brief.py:1535 | `first_from = f"acceptance_criteria:{ac_ref}" if ac_ref else "description"` | C+U | a register row with no `ac_ref` is labelled "description" even when it came from a comment/attachment (a wrong origin shown to a person): class C-ACREF | t_gate_question_form.py |
| gate_brief.py:1482,2640; gate_preflight.py:1251; controller.py:1508; story_run.py:9529; planning_contract.py:343 | comments citing cmp2 / 15045 findings ("tested the letter of the AC", "AC-7", "AC7") | K(q) | history | - |
| sizing.py:97,310-311,269-273 | `REGISTER_COLUMNS ... "ac_ref"`; `requirement_signal` joins `observables[].requirement` by `ac_ref` | C+U | a requirement without an `ac_ref` gets NO per-requirement surface signal (silent weight loss on a no-AC task): class C-ACREF; both readings: join by R-n | t_sizing.py |
| sizing.py:61,466-467 | reducer name `single-criterion` ("criterion" = a verifiable requirement) | C(schema) | lying name; stored in `reducers_applied`; sibling `single-requirement`, readers accept old | t_sizing.py |
| sizing.py:15,662-703 | "2 x criteria" (sibling STLC factory); selftest rows `AC-1..3` | K | | t_sizing.py |
| grammar.py:20,355; check_witness.py:46,52-56,165; validate_artifacts.py:60,142,446-467; artifact_producer.py:33; form_selftest.py:74-84 | `REQ_SOURCES = {story, feature, assumption, discussion, ac, derived}`; `by_source`; "register consists of AC only while a parent feature was found" | K | class C-REQSRC: `ac` is a legal source; check_witness rule 52-56 is P23-aligned. U: set has no word for attachment/linked task/diff (probably `story`/`feature`/`derived`): state the mapping | t_ahead_cards.py, t_gap_points.py, t_gate_preflight.py, t_oracle_provenance.py |
| validate_artifacts.py:98 | `PHASE_JSON_KEYS["context-manifest.json"] = [ticket, acceptance_criteria, implementation]` | C(schema) | key required, PRESENCE only (`if key not in data`, validate_artifacts.py:1450-1452): `[]` passes, so a no-AC manifest is legal; class C-SNAPSHOT | t_audit_rules.py:126 (A11), fx/*/context-manifest.json |
| validate_artifacts.py:54-55,206-210 | `covers_ac` accepted for old cases (before RULE_CUTOFF), new must carry `covers` | K | already migrated to the requirement; legacy key stays readable | t_validators.py, form_selftest.py:162,354 |
| validate_artifacts.py:278,334,530,2060 | "an `ac` ref to an R the register derives from the diff alone"; "A case is the unit of coverage of a register requirement, not of an AC"; refusal "(no AC, no source speaks to it)"; "the key was read (description, AC, a comment...)" | K / R | 334 and 2060 K (aligned); 278 K (oracle word); 530 refusal text R: "no ticket source speaks to it" | t_validators.py |
| exit_gate.py:658,672 | "code the acceptance criteria never spelled out"; "grounded the 13 criteria in the diff" | R / K(q) | 658 docstring R "the requirements"; 672 (q) | - |
| check_delivery.py:1653 | comment "an acceptance criterion the product does not deliver" (FR-21 sibling) | R | "a requirement the product does not deliver" | - |
| handoff_check.py:311 | comment "an `AC-1` that is no requirement" | K | confirms AC id is not a requirement id | - |
| judge_diff.py:1,6,8,27-46,102,116; judge_sources.py:57,86; manifest_view.py:112 | per-hunk "which acceptance criterion it relates to", `acceptance_criteria` list, `"no acceptance_criteria in context-manifest.json yet"` | U | class C-JUDGEDIFF (see judge.md:65) | t_judge_discovery.py |
| source_inventory.py:337-357,608-623,956-978,1050-1057,3462-3477; ticket_adapter.py:507-517,689,773,1253; ticket_light.py:114,633-655; story_run.py:6167-6172 | `acceptance_headings`, `acceptance_criteria_fields`, `acceptance_criteria_from_description` | K(schema) | class C-CONFIG: configures WHERE the AC are read | t_source_inventory.py, t_ticket_light.py, t_config_migration.py |
| ticket_light.py:6,58,278-395,663,719-852; ticket_adapter.py:38,55,63,100,178,190,198,396,569-595,947,1011,1186,1584,1731-1822; source_inventory.py:572,1076-1086,1554,1662,1800-1801; judge_sources.py:57 | `acceptance_criteria` extractor, snapshot key, REQUIREMENT_FIELDS, ticket-view heading `ACCEPTANCE CRITERIA` | K(schema) | class C-SNAPSHOT: extracting the AC field is correct; REQUIREMENT_FIELDS = (title,type,description,acceptance_criteria) is the freshness set | t_ticket_light.py, t_ticket_adapter.py |
| brief_pack.py:738,747; source_exclusions.py:15,670; story_run.py:4867-4872 | "the criteria" in ticket-view / paste hint; "six criteria" (q) | K | | t_source_exclusions.py |
| story_run.py:5759,6076,6134-6156,6167-6172 | `s0_criteria`: problems=["no acceptance criteria"]; question "found no acceptance criteria ... The requirements, the test plan and the test cases are all built from the criteria, and I will not invent them"; options retry / paste / `go on without criteria` | R+U | class C-S0, DIRECT P23 CONFLICT: text says requirements are BUILT FROM the criteria. Readings: (1) wording only; (2) behaviour: absence of AC is not a halt, the S2 register derives from the other sources (P23 line 137-138) | t_story_run_s0.py, t_conductor_doors.py, fx/driver-layers.json |
| manifest_put.py:270-341; report_facts.py:879-880; s5_precheck.py:568-589,1886-1887; stand_gaps.py:273-291,574-575 | `import acceptance as AC` (module `acceptance.py`: "Semantic acceptance of a bounded automation window") | K(fp) | 21 lines; NOT AC; do not rename in a sweep | - |

## Scope 5 — kb/ page sources
| site | phrase | V | proposal | pin |
|---|---|---|---|---|
| kb/03-pipeline-flow.xhtml:62; qa-factory-route-en.html:185 | "A requirement (AC) contradicts the code" | K | AC glossed as a requirement; class C-CONFLICT row text | - |
| kb/03-pipeline-flow.xhtml:76 | "the AC said 'shown at its former position' ... tested the letter of the AC" | K(q) | pilot finding | - |
| kb/03-pipeline-flow.xhtml:113 | readings from "(the AC, the description, a comment, the parent ticket, the code, a test, a precedent)" | K | origin list | - |
| kb/02-architecture.xhtml:42 | digest row "`qa-scout … AC/code conflict`" | C | class C-CONFLICT (must follow SKILL.md:221) | - |
| kb/06-roadmap.xhtml:50 | "Findings beyond the acceptance criteria" (charter exploratory testing) | R | "beyond the requirements" | - |
| kb/*.xhtml, KB-BRIEF.md | `ac:structured-macro`, `ac:image`, `ac:name` | K(fp) | Confluence namespace, ~60 lines | - |

## Scope 6 — dev-side carriers
| site | phrase | V | proposal | pin |
|---|---|---|---|---|
| docs/tasks/critic-diff-brief.md; plans/builder-rules.md; docs/SIBLING_MAP.md | no AC word (controls above) | K | nothing to fix; SIBLING_MAP axis 4/5 are the walk, not a site | - |
| docs/factory-map/qa-factory-paths.md:71,95,117,119 (+ .html, graph-02/03.svg) | "потеряны AC, parent, comments"; "противоречие AC и кода"; "AC и код не конфликтуют"; "AC верны; тестировать их" | R | snapshot of 28.09 (generated graph in svg/html): "противоречие требования и кода"; regenerate with the map, not by hand | - |
| .claude/agents/builder.md:23; designer.md:17 | "no DoD — no acceptance criteria and no verification run"; "explicit acceptance criteria" | K(fp) | the DISPATCH's acceptance criteria, a different thing; keep | - |

## Scope 7 — records (count only)
- docs/tasks/specs/reports/t-925-grounding-digest.md: 23 lines / 34 tokens (29 `AC`, 3 `ac`, 2 `acceptance_criteria`).
- docs/tasks/specs/t-926-grounding-stage-draft.md: 5 lines / 6 tokens (5 `AC`, 1 `ACs`).
Command: `grep -ciE "acceptance criteri|\bACs?\b|\bAC[0-9]|acceptance_criteri" <file>`; token split by `grep -oiE ... | sort | uniq -c`.

## Class summary (code identifiers; one rename = N sites; readers/writers)
Convention for every class below: stored data keeps its OLD key readable (edge b, FR-14, FR-40): add the sibling, accept both, write the new.

**C-ORACLE — the Then oracle word `ac`** (K as a source; C because it means "a register requirement from the ticket's sources"; `spec` also has ref R-n).
Definition: contract.py:395 `THEN_ORACLE_WORDS`; registry references/gate-registry.json:401-403 (verdict_map). Writers: the case-designer role (case front matter `then_oracles`
JSON line, schema in cases under state/ stories), `question_register.py:776-812` (rewrites the line). Readers: contract.then_oracle_errors (715-840), resolve_then_oracle (872-893),
validate_artifacts.check_then_oracles (273-302), traceability.then_oracle_states (309-336), ledger.py:64-92, coverage_contract.py:461-489, gate_preflight.py:1344,
manual_evidence.py:496-521, story_run.py:7043-7050. Docs/roles: artifact-contract.md:118-124 (+slice twin), vocabularies.md:33-38, qa-case-designer.md:55, FR-58 (rules:257-268), P23:140.
Pins: t_oracle_provenance, t_validators, t_traceability_report, t_coverage_contract, t_gate_preflight, t_manual_evidence, t_question_register, t_story_run_s6.
Sites: ~12 code-reading functions + 6 doc files + 1 registry.

**C-ACREF — register column `ac_ref` (+ `AC-n` ids; `observables[].requirement: "AC-n"`)**.
Writers: the S2 role (register table header), templates/requirements-register.md:22-26, form_selftest/sizing selftests. Readers: contract.register_rows/implementation_only (545-582),
planning_contract.py:381-422, gate_brief.py:1535, sizing.py:97,269-273,310-311. Schema: `work/requirements-register.md` header. Defect candidates found: gate_brief.py:1535
(origin mislabelled `description`), sizing.py:310 (no signal without `ac_ref`). Pins: t_validators, t_sizing, t_oracle_provenance, t_traceability_report, t_report_facts,
t_s3_s4_chain, t_gate_question_form, t_validate_artifacts_report. Sites: 4 modules + 2 templates/docs.

**C-REQSRC — register source word `ac` / `by_source` key**: grammar.py:20,355 (REQ_SOURCES: THE one set), validate_artifacts.py:60,446-467, check_witness.py:46,52-56,
artifact_producer.py:33, templates/requirements-register.md, ahead-cards.json:20, qa-requirements-tester.md:46. K (a legal source). Open: the set names no
attachment / linked-task / diff word (U). Pins: t_ahead_cards, t_gap_points, t_gate_preflight, t_oracle_provenance.

**C-SNAPSHOT — key `acceptance_criteria`** (ticket snapshot, context-manifest.json, ticket-view): K, keep. Writers: ticket_light.py:719, ticket_adapter.py:595, scout (context-manifest.json).
Readers: validate_artifacts.py:98 (required key), judge_sources.py, manifest_view.py:112, judge_diff.py:30, source_inventory.py:1080,1554,1662, ticket_adapter diff 1011. 21 test files pin it.
A task with no AC still carries the key as `[]` (presence check only) - no change needed for P23.

**C-CONFIG — `direct_api.acceptance_headings` / `acceptance_criteria_fields`** (project config.json): K(schema), 5 modules, t_config_migration, t_source_inventory, t_ticket_light.

**C-CONFLICT — digest token `AC/code conflict` / halt "Code contradicts an acceptance criterion"**: qa-scout.md:64,119-120, SKILL.md:221, s1.md:322-384, s2.md:53,
judge.md:24, kb 02-architecture:42 / 03-pipeline-flow:62, t_s1_s2_contract.py:116. No script reads the token (negative, controlled). Rename = a doc/text + digest grammar sibling.

**C-S0 — S0 `s0_criteria` / question `ticket_incomplete` "no acceptance criteria"**: story_run.py:5759,6076,6134-6172; question-prices.json:39; phases/s0.md:79; design/driver.md:99;
evals.json:236; pins t_story_run_s0, t_conductor_doors, fx/driver-layers.json. Behaviour class, not a rename (see row; Lead decision).

**C-JUDGEDIFF — S1 hunk relevance judge keyed on AC**: judge_diff.py, judge_sources.py, judgments.d/discovery.json `disc_hunk_relates`, judge.md:65, t_judge_discovery.

**Smaller**: `single-criterion` reducer (sizing.py:61,466); legacy `covers_ac` (K, already migrated).
**Sibling twins to touch together (axis 5)**: artifact-contract.md <-> slices/qa-case-designer/artifact-contract.md; coverage-design.md <-> slices/qa-scout/coverage-design.md;
rules <-> debt <-> index (axis 4); PROJECT.md/index -> AGENTS.md (generated).

## Needed beyond the manifest
Read beyond "given": tests/ (pins by grep), scripts/ bodies for sizing/contract/story_run/gate_brief, references/artifact-contract*.md, vocabularies.md, gate-registry.json,
agents/*.md, phases/s0-s2, kb/*.xhtml. The manifest had no line on `scripts/tests` (needed for edge c) and no list of the multi-line phrasing (DoD command misses wrapped hits).

## Trail
Files read/grepped: design/factory-rules.md (63,94,245-330), factory-rules-debt.md, PROJECT.md (47,101,111,136-141,177), docs/FACTORY_RULES_INDEX.md, docs/SIBLING_MAP.md (axis 4),
ai-packages/qa-factory/{handoffs,references,agents,skills,evals,design,hooks}, scripts/*.py (grep -noiE with context), scripts/tests (grep -l by phrase), kb/, docs/factory-map/,
docs/tasks/critic-diff-brief.md, plans/builder-rules.md, .claude/agents/, t-925 digest and t-926 draft (counts). Spot-read in context: story_run.py 5755-5765 and 6128-6160,
sizing.py 255-320 and 458-468, contract.py 290-296 and 540-590, gate_brief.py 1530-1538, check_witness.py 44-60, validate_artifacts.py 96-99, qa-scout.md 86-96,
qa-requirements-tester.md 30-48, templates/requirements-register.md 10-18, artifact-contract.md 118-128, vocabularies.md 28-40, gate-registry.json 396-410.
Not verified: which test pins the gate-registry `ac` words (t_gate_registry reads the file) and question-prices.json:39 (t_conductor_doors reads the file).

## Verdict totals per scope (rows, primary letter; `K+R` style mixed rows counted by first letter; awk over the table, one row with escaped pipes is missed in scope 4: 22 counted of 23)
Scope 1: 10 rows = K6 R3 C1 U0 | Scope 2: 6 = K3 R3 C0 U0 | Scope 3: 54 = K32 R5 C12 U5 | Scope 4: 22 = K12 R2 C7 U1 | Scope 5: 6 = K4 R1 C1 U0 | Scope 6: 3 = K2 R1 C0 U0 | Scope 7: records, no verdict.
Overall R sites that are real wording fixes: FR-58, FR-21 (+index), debt:24, P20, P21, vocabularies.md:36/38, artifact-contract.md:124, contract.py:774, validate_artifacts.py:530,
exit_gate.py:658, check_delivery.py:1653, kb 06-roadmap:50, factory-map; behaviour (U) decisions for the Lead: C-S0 (story_run.py:6134-6156), qa-scout.md:90-93, C-JUDGEDIFF,
gate_brief.py:1535 and sizing.py:310 (silent defects on a no-AC task).

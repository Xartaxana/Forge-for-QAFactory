# t-539: critic re-review of the P1-a fix round (t-524), fix diff only

Diff: `git -C .claude/worktrees/p1a-fix diff 8580665 4e0c61d`. I verified HEAD with rev-parse: `4e0c61db9bf1...`.
First verdict: `docs/tasks/specs/reviews/20261113-p1a-topic-code-critic.md` (t-521).
Fix report: `.claude/worktrees/p1a-fix/docs/tasks/specs/reports/20261113-p1a-fix-report.md`.
Critic: opus (claude-opus-5-5). This verdict is an input to the Lead's acceptance. It is not the acceptance.

**Verdict: ACCEPT WITH FIXES. 2 blocking findings (N1, N2), 4 fixes for the same round (N3-N6), and 3 conditions that belong to the Lead (L1-L3).**

The round did most of what t-521 asked for:
- The deriver round now runs on the world's context.
- The world now holds grounding.yaml, context-manifest.json, a pinned case version and the size.
- Both templates are fixed, and `project:bugs/[base]` is green.
- No placeholder node remains. Every node in the ledger exists in `plans/piles/live-run-fvf/batch-1-live-run-fvf.md`.

I checked the 30 rows that remain in the ledger, and they are real. Two things still do not hold:
- The new `not_in_world` section is a second ledger with no ratchet.
- B2 left a residue: hints still stay silently inside values.

## Mechanical layer: control re-run
- `( cd <p1a-fix>/ai-packages/qa-factory && time python -B scripts/tests/test_field_producers.py )` gave:
  - `known red rows 30, rows walked 880`;
  - `=== test_field_producers: 890/890 ok ===`;
  - `forms 24, variants 434, fields 980, unfillable 8, left_for_code 82`;
  - `readers 19, pairs 36, languages 5`;
  - `deriver round: forms 24, fields met 38`;
  - 18.3 s wall.
- KNOWN RED lines: 30. NOT IN WORLD lines: 47. This matches the coordinator's witness and the report.
- Node ids in `form-rounds.json`: FV1-1 x5, FV1-14 x17, FV1-19 x6, FV1-22 x2. Each id is present in the batch file: 6, 2, 4 and 4 hits. No `"node": "P1A-...` remains. A case-insensitive `p1a-` matches only the `raised_by` path of the t-521 verdict, 30 lines.

## Per DoD item

### 1. B1 (a)-(d): partly landed
- **(a) landed.**
  - What changed: `test_field_producers.py:1295` fills each form with `dataclasses.replace(w.ctx, author_dispatch=..., dispatch_id=...)`. `form_filler._issued`, together with the world's `gen.world`, turns hint ids into the world's issued ids.
  - Result: fields met went from 28 to 38. The case_version and requirements rows that were "world" rows in my t-521 sample went green and left the ledger.
- **(b) partly landed.**
  - Landed: grounding.yaml and context-manifest.json are written by the filler. `CV.pin(CV.create_version(...))` and `sizing.run` are product writers (`:992-1005`).
  - Not landed: the inputs that stay out went into `not_in_world` with no outcome or node from the Lead. t-521 B1(b) said: "For each input that stays out, Lead decides the outcome and gives it a REAL node." The builder decided the outcome himself, and he asks about it (report Q2). See N1 and L2.
- **(c) landed.**
  - The bugs template carries all eight front-matter fields from `ahead-cards.json:84`. `output: project:bugs/[base]` PASSES (run :616).
  - The `test_file:python` body writes `obligations=["OB-1"]`.
  - Re-measured: the `@python` row stays red, but for a NEW reason. The run shows `Refusal: ... obligations names OB-1 for TC-001, and the case's plan row (none recorded) is not in work/test-plan.json`. That is `case_plan_row` answering '' for P-1, the same detail as the `contract.case_plan_row` row. So the FV1-1 attribution is right.
- **(d) partly landed.** Every row carries an existing id. But 6 rows (P2 x3, P5 x3) carry FV1-14 as a stand-in.
  - My F2 said, with evidence, that fixing FV1-14 does not turn these rows green.
  - The note on each row says so honestly. Still, the node field names a node that does not own the defect.
  - The builder could not do better: `known_red` NODE_RE refuses `lead-queue`. This is L1.

**The 30 rows: are they real?** I read all 30 KNOWN RED detail lines from my run and traced 11 of them. All are real defects of main:

| rows | node | detail seen | verdict |
|---|---|---|---|
| 3 `unfillable test_file:{csharp,java,typescript}:marker` | FV1-19 | `case-markers.json has no marker form for the language X` | real |
| 3 `obligation_refs@{csharp,java,typescript}` | FV1-19 | `no writer for the language X: marker` | real, the SAME defect as the 3 rows above (counted twice; t-521 K4 already noted this) |
| `contract.case_plan_row`, `s5_precheck.case_plan_row` | FV1-1 | `given 'P-1' and answered ''` | real |
| `obligation_refs@python`, `@pytest` | FV1-1 | the refusal above | real, but `@pytest` is the same file as `@python` (N4) |
| 10 TS-only readers + `check_plan_v0` + `agree` | FV1-14 | `given 'P-1' and answered False` / `no TS-n rows` / 1 accepts and 13 refuse | real; consequences of the one split (t-521 P1) |
| `identity: plan-row id` | FV1-1 | P-n carriers vs TS-n carriers listed | real |
| 2 `accept: s7-analyst-to-automator...` | FV1-22 | failure_class None refused; reviewed_author_dispatch '' | real |
| `_plan_row_of` + 2 `derive ...plan_row` | FV1-14 (stand-in) | `answered None` / deriver returned nothing | real P2 (front-matter `plan_row:` is not in the case contract); wrong node, L1 |
| 3 `derive ...requirements` (s3 x2, s8) | FV1-14 (stand-in) | deriver returned nothing | real P5 (BY_LEAF over-match, t-521 trace); wrong node, L1 |

Taken as input to the Lead, this re-review names the raises of these 30 rows as real defects of main. That covers the `raised_by` gap from t-521 K4: t-521 named no raises, and every row's `raised_by` now cites t-521 B1. Whether to accept the rows stays with the Lead.

**Is `not_in_world` an honest shape under AR-20/AR-28?** Not yet. It is a second ledger without a ratchet. **N1, blocking.**
- What it does well:
  - every row is named and printed;
  - a green row fails as `stale`;
  - an unknown id fails;
  - a row that is in both sections fails (`test_field_producers.py:1385-1395`).
- What it lacks:
  - no `raised_by`;
  - no node;
  - no count pin;
  - it is not loaded through `known_red.py`.
- Failure scenario, traced:
  1. A future change breaks a deriver that is green today, say `derive: s2-tester-to-strategist:size.computed`.
  2. The author adds one line, `"derive: ...size.computed": "sizing input not in the world"`, to `not_in_world`.
  3. `check()` at `:74-77` prints NOT IN WORLD and appends a PASS.
  4. The reconcile at `:1396` drops the row from WALK.
  5. The loop at `:1385-1395` sees a non-empty reason, no ledger entry, a known row, and a red row. No check fails.
  6. The file stays green. Nobody named the raise.
- This is exactly the class B1 was raised for: self-authorised entries in the ledger. It is cheaper than the ledger itself, because the ledger at least demands a `raised_by`.
- Fix (either one):
  - (i) give every `not_in_world` row `{"reason", "raised_by"}`, check it through the same loader as `known_red`, and add `pins.not_in_world: 47` checked as `<=`, so growth fails and a raise edits the pin in a commit a critic sees; or
  - (ii) fold the rows into `known_red` under one real node for the test-world gap. The Lead opens that node (L2).
- Also, the comment at `_round_world` (`:1001-1002`) says "their rows stay in the ledger". It no longer tells the truth: they moved to `not_in_world`.

**Does anything now pass that should be red?** No row went from red to green wrongly. One `not_in_world` reason is false, though:
- `derive: s5-automator-to-runner:inputs_read[1].version` is listed as "its path is an unfillable hint of the filler".
- In fact `inputs_read[1].path` of that form is NOT unfillable. The template is `<cases_root>/<case>.md` (`handoffs/s5-automator-to-runner.yaml:36`). The filler substitutes `<case>` and silently leaves `<cases_root>/TC-001.md`, which my probe shows. The deriver round then skips it because the path contains `<` (`:1298`).
- The real cause is N2. If it stays, the row's reason misleads the person who later fixes it.

### 2. B2: partly landed. "unfillable 8" is not the full count. **N2, blocking.**
I probed once: every form, its base variant, the test's own context, read-only (Bash heredoc, source in the trail).
- `unfillable 8`: true as far as it goes. These are the 8 `inputs_read`/`records`/`bug_drafts` paths named in `not_in_world`.
- Literal-text rows cover 7 values. All are command templates or the git-add prose, so they are legitimate as text.
- **13 values still carry a `<...>` hint silently.** They are neither filled, nor `Unfillable`, nor literal text, nor `left_for_code`. There are two causes in `form_filler._Survey` (`form_filler.py:288-312`):
  - **(a) Partial substitution.** When a value holds a context token, it takes the `token` branch, and only the tokens are replaced. Any other hint left in it is never checked: the `embedded` test sits in the `elif` AFTER the token test.
    - Examples: `<cases_root>/<area>/<case>.md` becomes `<cases_root>/general/TC-001.md` in 3 forms (s4 x3 `inputs[1].path`), and `s5-automator-to-runner inputs_read[1].path` becomes `<cases_root>/TC-001.md`.
    - The last one is a role-written field, and it is the false reason in item 1.
  - **(b) Fields the contract owns.** The new branch at `:290-293` takes them only when they contain a context token. Every other hint in them is skipped with no count.
    - Examples: `inputs[0].path: work/handoffs/<the automator's dispatch>.yaml` (s5-critic, s5-critic-plan), `inputs[4].path: work/probes/<instance>.json`, `<test files listed in artifacts.tests>`, `<the repair_verify run witness>` and others (s5/s7), and the prose `expected_of_the_receiver[2]` (s2).
- Fix:
  - after token substitution, re-test `HINT` and apply the same `embedded` rule (`Unfillable`, or a `literal_text` row);
  - for fields the contract owns, either name them in a separate counted line of the summary (`kept_in_contract N`), or make them `Unfillable` like the rest;
  - `cases_root` has a form field of its own (`s4-designer-to-case-critic.yaml:70`), so a context token `<cases_root>` is the cheap fill.
- B2 asked that "any other embedded hint is Unfillable or a named literal-text rule". Today that holds only for role-written values with no token.

### 3. F1-F8, and F9
- **F1 landed.**
  - `languages` rows with a one-hop `like`, and `language_body` returns `Unfillable` naming the language, never another language's body (`form_filler.py:689-700`).
  - `_marker_entry(w, written)` reads `written[0]`, the file that this language's fill wrote (`test_field_producers.py:1114-1119,1141`).
  - Edge traced: once FV1-19 adds a csharp marker, the csharp row gets `Unfillable body`, not the Python file. Good.
- **F2 partly landed.** The row is re-attributed by its note, but the node is still FV1-14 (L1).
- **F3 landed.** The world writes the base case (`:582-583`). The report says "refusal shows", but `output: manifest_row[base]` PASSES (run :635), and line 774 lists `manifest_row` under "outputs no reader refuses". So the manifest reader simply does not check the case's plan row. The row is now honest; the report's sentence is inaccurate (minor).
- **F4 landed.** `pins {readers: 19, families: 3}` are checked as equality (`:1270-1273`). Both PASS.
- **F5 landed, with one side effect (N4).**
  - One language reader: `FF.test_file_languages(source)`, driven by the registry and called from both walks.
  - One environment swap: `_in_project`.
  - Side effect: the reverse walk now also walks the runner key `pytest` as a language, so the ledger holds `@python` and `@pytest` for one file and one refusal.
- **F6 landed.** The `tool_fields` rows, `_f_tool_fields`, its FEEDS entry and its expand branch are removed. Pairs went from 62 to 36.
- **F7 landed.** test-layers covers: +ahead-cards.json, +handoff-keys.md, +qa-automator.md.
- **F8 landed as a report line.**
  - Breakdown: the N3 rows (readers 1.80 s + derived 3.59 s + one_fact 0.13 s) add about 5.5 s in-process. The whole file is 19.0 s (report) / 18.3 s (my run), against the 10 s budget of spec §2, and it grew from 15.1 s at t-521. `every_form_fills_from_its_own_hints` alone takes 8.7 s.
  - Lead decides. This is input, not a block.
- **F9: what the builder did is correct.**
  - (a) is returned by name with a concrete reason: no filler row builds question-register rows.
  - (b): the search ran with a positive control. The candidates `report_facts._manual` (`meta.get("plan_row")`) and `_cases:817` are named as unverified, not claimed clean. That is the honest outcome of "do or queue by name".

### 4. New defects and standing questions
- **N3 (fix).** `_not_in_world()` re-reads and re-parses `form-rounds.json` twice for every red row (`:74-75`). It is not cached, unlike `_ledger_ids`, and it is a second loader beside `KR.load`, a duplication of the ledger reader. Fold it into N1(i).
- **N4 (fix).** `@python` / `@pytest` count one defect twice. Fix either way:
  - collapse runner keys onto their language in the reverse walk: `like`, or case-markers' language key; or
  - mark `@pytest` as an alias.
  The FV1-19 rows are a second double count (marker + obligation per language); t-521 K4 noted it, and it stays queued.
- **N5 (fix).** The comment at `_round_world` `:1001-1002` no longer tells the truth (N1). The report says F3 "refusal shows", which is also inaccurate.
- **N6 (fix).** The `not_in_world` reason for `s5-automator-to-runner:inputs_read[1].version` is false (item 1). Correct it with N2.
- **DUPLICATION AND CONSISTENCY:** N3 and N4. I grepped the loaders of `form-rounds.json` in the test (`KR.load`, `_rounds`, `_not_in_world`) and the language readers (`_languages` now delegates to `FF.test_file_languages`, which is one road).
- **CODE QUALITY:**
  - Names that lie: N5.
  - The new `_hint_list` branch, `_issued` and `language_body` are small and clear.
  - `every_stage_output_fills_or_is_named` is still about 420 lines. The split stays queued, as in t-521.
- **q10 ARCHITECTURE:** AR-20 (N1: a ratchet with no shrink/pin), AR-28 (N2: a hint passes as a value), AR-13 (N3: a second loader). AR-22 is improved by B1(a).
- **q11 JUDGMENT:** none. The changes stay in test code and data rows. No role judgment moves into code.
- **q12 ONE ROAD:** the language bodies are now data rows with a one-hop `like`, so there is no hidden Python road. The runner-key-as-language walk (N4) is a duplicate walk of one language, not an excluded language, so it is a fix, not a blocker.

### 5. B3: expected carrier text (input to the Lead; I do not re-raise B3)
I would expect the three carriers to say:
- **SIBLING_MAP axis 18:** "the `known_red` ledger of form-rounds.json, and its `not_in_world` section, are shrink-only ratchets like lint_ratchet: a row leaves when its check turns green (`stale` fails otherwise), and a row is added only with a `raised_by` naming a critic verdict path or a Lead word."
- **AR-20 Carriers:** list `scripts/tests/known_red.py`, `fixtures/form-rounds.json` `known_red` and `not_in_world` (with their pin), and `test_field_producers.red_rows_equal_the_known_red_ledger` as the detector.
- **Critic question 9:** "a diff that adds a row to `known_red` or `not_in_world`, or raises its pin, names each raise and its existing node; a raise the verdict does not name is a blocker."

## Conditions for the Lead (not builder fixes)
- **L1.** Open real nodes for P2 (`_plan_row_of` reads front-matter `plan_row:` that `artifact-contract.md:59-62` does not define) and for P5 (the BY_LEAF `requirements` over-match). Then re-point the 6 stand-in rows. The other option is to allow a queue node in `known_red` NODE_RE, but that is a mechanism change.
- **L2.** Decide the outcome for the inputs kept out of the world (t-521 B1(b)): a real node, or the N1 shape. This answers the builder's Q2.
- **L3.** The F8 time: whole file 18-19 s against the 10 s budget of spec §2.

## Trail
Read:
- the t-521 verdict, whole;
- the fix report, whole;
- the whole fix diff (6 files);
- `handoffs/s5-automator-to-runner.yaml:20-41`;
- `handoffs/s2-tester-to-strategist.yaml:112-116`;
- `form_filler.py:100-119`;
- `test_field_producers.py:20-54,418-429`;
- `tools/critic_verdict.schema.json`.

Searches:
- `cases_root` over `handoffs/`: 5 hits.
- Node ids in form-rounds.json, then each in `batch-1-live-run-fvf.md`: all present.
- Case-insensitive `p1a-|FV1-1\b`: 30, all in `raised_by` paths.

Re-runs:
- `test_field_producers.py` (control).
- The B2 probe: a Bash heredoc, read-only. For each contract in `handoff.index()` it takes the base variant, runs `FF.fill_form` with `FillContext(author_dispatch="S2-author-1", dispatch_id=f"{contract}-w1", cases=["TC-001"])`, and walks `data` for `FF.HINT`, excluding unfillable paths, `left_for_code` prefixes and `FF._literal_text`.
- Result: unfillable 8, literal 7, left_for_code 82, silent 13.

Not re-run: `test_selftest_slow_tests`. Its one failure names the rows `test_app_card_stand_lessons.py` and `test_place_of_draft_observation.py`. The test-layers diff touches only the `test_field_producers.py` covers, so this diff cannot cause it.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "N1 not_in_world (form-rounds.json, 47 rows) is a second ledger with no ratchet: no raised_by, no node, no count pin, not loaded through known_red.py; adding a reason line silences any new red row (check() test_field_producers.py:74-77, reconcile filter :1396, loop :1385-1395 only checks reason/unknown/stale/both) - AR-20; fix: raised_by + pins.not_in_world checked <=, or fold under a real Lead node",
    "N2 B2 residue: 13 values keep a hint silently - partial token substitution leaves other hints (<cases_root>/TC-001.md in s4 x3 inputs[1].path and role field s5-automator-to-runner inputs_read[1].path) because the embedded test sits after the token branch (form_filler.py:288-312); contract-owned fields with non-token hints are skipped uncounted (:290-293); the summary unfillable 8 is not the full count - AR-28"
  ],
  "fixes": [
    "N3 _not_in_world re-reads form-rounds.json twice per red row, uncached, a second loader beside KR.load (test_field_producers.py:57-63,74-75): fold into N1",
    "N4 @python and @pytest ledger rows count one file and one refusal twice: collapse runner keys onto their language in the reverse walk or alias",
    "N5 _round_world comment (:1001-1002) says the out-of-world rows stay in the ledger (they moved to not_in_world); report F3 line says refusal shows but manifest_row[base] passes",
    "N6 not_in_world reason of derive s5-automator-to-runner:inputs_read[1].version is false (path is partially substituted, not unfillable): correct with N2"
  ],
  "class_completeness": "B1(a) landed; B1(b) partly (out-of-world outcome decided by builder, not Lead: L2); B1(c) landed (bugs[base] green, python obligation red for FV1-1, detail verified); B1(d) partly (6 stand-in FV1-14 rows for P2/P5: L1). 30 known_red rows traced real; all node ids exist in batch-1-live-run-fvf.md. B2 class: role values without tokens covered; token+hint values and contract-owned values not (N2). F1-F8 landed (F2 partly via L1; F5 side effect N4); F9 actions correct. Axis 34: language bodies now data rows, one reader; runner-key walk duplicates python (N4). Axis 18 carriers: B3, Lead node, expected text given in section 5.",
  "trail": {
    "read": [
      "docs/tasks/specs/reviews/20261113-p1a-topic-code-critic.md",
      ".claude/worktrees/p1a-fix/docs/tasks/specs/reports/20261113-p1a-fix-report.md",
      "git diff 8580665 4e0c61d (form-fill-rules.json, form-rounds.json, form_filler.py, test-layers.json, test_field_producers.py)",
      "ai-packages/qa-factory/handoffs/s5-automator-to-runner.yaml:20-41",
      "ai-packages/qa-factory/handoffs/s2-tester-to-strategist.yaml:112-116",
      "ai-packages/qa-factory/scripts/tests/form_filler.py:100-119",
      "ai-packages/qa-factory/scripts/tests/test_field_producers.py:20-54,418-429",
      "plans/piles/live-run-fvf/batch-1-live-run-fvf.md (node id grep)",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "( cd .claude/worktrees/p1a-fix/ai-packages/qa-factory && python -B scripts/tests/test_field_producers.py )", "result": "known red rows 30, rows walked 880; 890/890 ok; unfillable 8, left_for_code 82; readers 19, pairs 36, languages 5; fields met 38; KNOWN RED 30 lines, NOT IN WORLD 47 lines; 18.3 s wall"},
      {"command": "python -B heredoc probe: every form base variant, FF.fill_form with the test context, walk data for FF.HINT outside unfillable/left_for_code/literal_text", "result": "unfillable 8, literal_text 7, left_for_code 82, silent embedded hints 13 (s4 x3 inputs[1].path <cases_root>/general/TC-001.md; s5-automator-to-runner inputs_read[1].path <cases_root>/TC-001.md; 8 contract-owned inputs paths; s2 expected_of_the_receiver[2])"}
    ]
  }
}
```

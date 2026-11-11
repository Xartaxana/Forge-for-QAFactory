# t-2064 / TR2-14 — a red probe on every check (part of t-2045, its §11; revised by t-2076, task t-2081)

Status: REVISED DRAFT for Lead acceptance. It answers the critic's plan review `docs/tasks/specs/reviews/t-2076-critic-plan-t2064.md` (B1-B10, S1-S11) and P0's measurement `docs/tasks/specs/reports/t-2064-p0-joint.md`. A new part of `docs/tasks/specs/t-2045-one-probe-road.md`, written as its own file; t-2045 is not edited here. Where this file and t-2045 differ, this file wins (§11.3 names each place). An edge of this file is `EP-x`; `t-2045 E-x` always means t-2045's own edge.

**Lead's edit of t-2045, three lines, text ready:**
- head: `Part: docs/tasks/specs/t-2064-probe-every-check.md wins where the two differ (its §11.3 names each place).`
- §6 at "Order": `Order, whole: t-2064 §11.3. The pin rows of N3b in this table are void: t-2064 §11.5 N3b carries them.`
- at `### N3b`: `Void. N3b is written whole in t-2064 §11.5; proved_by is marker or critic.`

Tree and names as in t-2045: `D:/ws1/wt-fbfix`, branch `experiment/thinking-roles`, `PKG` = `D:/ws1/wt-fbfix\ai-packages\qa-factory`. Lines read 06.11.2026; a builder finds a function by name, the line is a pointer. N1's code is read on the worktree `D:/ws1/wt-tp-n1` (branch `tr/tp-n1`, ref 9a2985725). Nothing here changes N0's or N1's `owns`.

**The owner has six questions open (§11.2, Q1-Q6). Every node below is executable on the recommendation; a node resting on one carries the line «по рекомендации, до слова владельца» with the fork named. Decisions attributed to the owner are only those whose words stand in `plans/piles/thinking-roles/findings/20261106-odna-doroga-proby-na-vse-yazyki.md`.**

## Change table (t-2076 → this text)

| Finding | What changed | Where |
|---|---|---|
| **B1** `lexical_shape` equal refuses a bracketed actual | The removed text and the added text are each balanced and end in code; the file's shape = base − removed + added | P3 item 2, EP-N, tests per language |
| **B2** "no role" not tellable, callers unowned, stored models no producer | No role = the dispatch row's stage is S6, never a flag; `checks[].entry` stores the whole edit; S5 settle with nothing stored: "model owed", no run; owns gain `_replay_plan`, `_item`, `_classify`, `settle`, `proof_level._replay`, a test of `s6_reprove` | F-P8, P4b item 2, P4c |
| **B3** `--at` a second road | `--at` is a plan of one row through the same loader: same refusal, per-check record, aggregate rebuilt, receipt only when complete | P4b item 3, F-P8, tests |
| **B4** default flip, no pin table | "Pin owners" table for P3-P7; one test helper `probe_entries.py`; owns gain the named files | §11.5 head, P3, P4a-c |
| **B5** chain with an inner failure | Run of one, absent token: the critic. Walk stops only when the failure lies on an EARLIER check's span; otherwise it goes on | P4a item 2, EP-F, EP-G, tests |
| **B6** a check cut by the test timeout may print its marker | P0's s4 already shows it on `s4n5`; P0b s4b measures the undecided case before P4a; the demote rule is in `_judge_joint_rows` | §11.0, P0b, P4a item 2 step C, EP-V, F-P11 |
| **B7** P0's rule leaves branches open | P0's table with the real results and each later node's consequence | P0 |
| **B8** N3b contradictory | Edges renamed `EP-*`; N3b written whole with its pin rows; pointer text above; `proved_by` is `marker` or `critic` | §11.4, §11.5 N3b, §11.3 |
| **B9** `red_sandbox` a second road | A product receipt counts only for the check it names, through the critic's `product` entry; the others stay owed; «по рекомендации, до слова владельца» (Q1) | EP-W, P3 entry, P6 |
| **B10** a branch not taken traps a healthy test | Entry kind `not_here`, presence only, read by a tier above; «по рекомендации, до слова владельца» (Q3) | EP-T, P3, P4b, P6, P7 |

| Finding | What changed | Where |
|---|---|---|
| **S1** cost text | A range; fix rounds, extra judgments and the cache named; EP-J's INV dropped | §11.6, EP-J |
| **S2** aggregate keys | Every key its readers need; the vacuous equalities stated | P4b item 1 |
| **S3** per-check records | `work/probes/checks/`; `probe_record_path`'s beside form moves there | P4a item 4, §11.3 N1b |
| **S4** soft reading on Java, C# | The critic judges by what he knows of the framework; the row decides only the plan | EP-M, §11.9, Q6 |
| **S5** doors that do not open | The refusal prints only the doors that open; `unverified` named | P3 item 6, F-P8 |
| **S6** P5 not executable | Call form, two entries on a check, full owns, `ROAD_EXCEPTIONS` line | P5 |
| **S7** P3 owns no Python edit | `_assert_with_marker`, `plan_mutation` for `invert`, bottom-up edits, the helper's body bounds `find` | P3 items 2, 4, 5 |
| **S8** tokens, failure text | `started_at` per run; `_problem_texts` reads every problem | P3 item 4, P4a item 2 |
| **S9** wall of a call | Aggregate rewritten after each row; the critic runs the walk in the background | EP-J, P4b item 1, P7 |
| **S10** retry row never fires on a project's script | The row is keyed by a `source` condition, not by a form id (new F-P10) | F-P7, F-P10, P1, P4a |
| **S11** guard list, old spellings | Each node extends the guard's list; `--mutation alternative` removed at P5, old model shape refused | P2-P5, §11.7 |

Duplication and quality findings of t-2076: `_row_by_marker` takes a token and the joint judge is a loop over it (P4a); P4 is split into P4a, P4b, P4c; `author_green_of` keeps `_run_alternative`'s reading (`bound.get("status") == "passed"`, :3893).

## §11.0 Intent (the owner's words, 06.11.2026, verbatim; carrier: the finding above)

«1) Они должны доказывать что тест не всегда зелёный просто по умолчанию. 2) Если нпа каком-то одном шаге несколько ассертов, то один упавший не должен останавливать проверку других, а то мы не увидим результата. Только зависимые друг от друга проверки могут быть последовательными. […] 3) Красная проба должа быть на каждый ассерт (если их 3 независимых, то мы 3 переворачиваем и за один прогон смотрим все 3, а если они последовательные, но придётся запускать 2 раза. Например первый ассёрт проверяет что такое-то правило вызвалось, а второй что текст сообщения в правиле был таким-то. Тут может быть 2 отдельных бага: правило вообще не сработало или текст был не тот. Такое можно проверить красной пробой только последовательно)»

Also, and these win where they differ:
- On proof: «В обоих случаях пусть смотрит роль. Только наш текст доказывает без роли».
- On independent and dependent checks: «правильно и надо записать это в принципы или в решения самого форджа, что правильно писать автотесты именно так: определять где проверки независимы, а где последовательны».
- On what a red probe is: «замечательное правило. Я бы сказала что все красные пробы нужно делать именно так и только если мы не знаем какое может быть другое значение, то переворачиваем проверку. В любых языках. Предпологать как бы сломаный продукт ответил должна роль».
- «разные рабочие пути для одного и того же это баг. Всё должно быть единообразно». On a case: an ordinary `if` on the task's own condition is no exception («да», F7 of t-2065); a case is an exception only when the common mechanism goes another road for it or does not reach it.

The road after these words, one for every language:

| Step | What | Who | Record |
|---|---|---|---|
| 0 | The list of the test's checks and the plan of runs | code (data) | `checks[]`, `plan[]` |
| 1 | For each check: suppose what the broken product answers (a **model**); no idea of another value: **inversion, with the reason written** | code critic (judgment) | the model file |
| 2 | Run by the plan: stopping checks one run each, non-stopping checks jointly | code | one `red_probe` per plan row |
| 3 | **Our marker in the failure text proves, and nothing else proves without a role** | code | `intended_failure`, `proved_by: marker` |
| 4 | Everything else with failure text: the critic reads it (the line is a fact he is given) | code critic | `cause: judgment`, `--judge`; `proved_by: critic` on `fires` |
| 5 | Only after that the person: accept without a probe | person | `probe not proved: <case>` (unchanged) |

Top invariants: (a) **a check not read in a joint run is never called dead on that run's word;** (b) **no failure text but our marker proves without a role, and a marker on a check cut by a timeout does not prove either;** (c) no branch asks what language the test is in: a framework with no soft form is a data row, and its checks go by one run per check on the same road.

### The answer to the first question: does proof without a role survive substitution?

**Yes, measured, on a value check. On a check the test's timeout cut, no: rule EP-V. On a throwing actual, no marker: the role. On a hard web-first form: not measured, owed in P0b.**

The model changes the value the check reads; the check's matcher and expected value stay as written. The marker goes into that same check's MESSAGE by the existing variants (`_with_marker`, `M-TS1`, `M-TS2`, N2's Python row), now on the **un-inverted** statement.

What P0 measured (Playwright 1.56.0, `run-playwright.mjs`, line output; pytest, JUnit read):
- s6a `expect(500, m).toBe(400)`: marker PRESENT under substitution.
- s6b `expect(thrower(), m).toBe(1)`: marker ABSENT, the body is the thrower's own error.
- s5: a marked soft check that PASSED beside a failed one: its marker ABSENT. So a token in a failure body means that check did not pass.
- s4: `s4n5`'s block carries its marker and `Received: undefined` where the others have `Error: element(s) not found`: **a check the timeout cut prints its marker.** So "the marker appears only for checks that failed" holds for a check that ran to its end; for a cut one it is EP-V.
- s6c `expect(page.locator('#none'), m).toBeVisible()`, hard form: NOT MEASURED, no result under the load cap on a machine at 100 % CPU; the soft form's call log in s4 is evidence for the soft form only.

A marker under substitution is weaker than under inversion in one way, and the rule pays for it: an inverted check fails on a healthy product by construction, while a model's check may also fail on its own. So **the marker proves only with the author's run green on these bytes** (F-P4). What it never says: that the model was a realistic bug. That is the role's judgment, accepted by a tier above (AR-29); no code reads the model's meaning.

Reuse in a more consequential role: `_with_marker` goes from "adds a proof" to "the only proof without a role". **Error direction: toward `cause: judgment`, never `intended_failure`.** Adversarial inputs that must stay on the safe side, each pinned in P3/P4a: a `replace` that throws in the check's own arguments (the message is never built: no marker: role; P0 s6b); a throw in the matcher's argument; the author's run red or unknown with the marker read (role); a marked sibling that PASSED beside a failed one (its marker absent, P0 s5, positive control s1); **a check still waiting when the test times out (its marker printed, undecided: EP-V)**; a neighbour's code frame echoing the marker expression (joined at run time, never contiguous; P0's frames show the expression, not the token); the marker in system-out or an attachment (`_problem_texts` reads failure and error bodies only); a retried attempt where only the retry failed; one marker being the prefix of another (fixed 12 hex); a message-less form with a matching library text (role: `fires_as` no longer proves).

## §11.1 Package-change frame

### AR-n touched, each with its change check in the DoD of the owning node

| AR | How | Change check (DoD) | Node |
|---|---|---|---|
| AR-1 | "This form does not stop", "this argument is the actual value", "this runner's flag", "this text means the test was cut" are data rows; a framework with no soft form is an explicit `[]` | grep `scripts/` for `expect.soft`, `soft`, `retries`, `Test timeout` in a code literal: only readers of `AD`; a new form is a row | P1, P2 |
| AR-2 | Open variety stays with the role: what a broken product answers, independent or dependent, whether a model is realistic, whether a branch is reached | name what the role still decides (report line); a fixture with a page-object helper must report, not halt | P2, P3 |
| AR-7 | The tool enumerates and runs where the role's model points; it never invents a value | a check with no model is a refusal with a door, never a value chosen by code; the one inversion by code is the no-role case, recorded so | P3, P4b |
| AR-9 | New refusals (no model, model region, reason empty, stale key), each with a usable door | one commit with its A24 row (`refusal_registry.py --check`); a test opens each door by RUNNING the second call | P3, P4b |
| AR-10 | The automator hears before writing that independent checks are written non-stopping and each check is probed; the critic hears what the plan reads | charter, `s5.md`, ahead card in one batch; ratchet measured | P7 |
| AR-12 | **This moves work to a role** (FR-55): cost in §11.6, measured on the live proof | live proof's report compares §11.6's range with the transcript; a figure over the range returns to the owner | P4b, live proof |
| AR-13 | One reader stays one: `_ASSERTION_ID`, `AD`, `reporters.failure_frames`, `check_on_line` (N1), `_row_by_marker`; `then_assertions`' parse is not duplicated | grep for a second heads-in-a-body walk, a second id parser, a second marker reader | P2, P4a |
| AR-14 | One writer per record: the per-check record by the walk, `judgment` by `judge_record`, the aggregate by `_aggregate_record` | grep writes of `checks`, `judgment` | P4a, P4b |
| AR-15 | **One road:** the alternative probe's planner and judge merge into the model road; a product receipt is one entry on the road | grep `ALTERNATIVE`, `plan_alternative`, `judge_alternative`, `--model`; `ROAD_EXCEPTIONS` shrinks | P5, P6 |
| AR-19 | Twins, each named in the report: `red_sandbox.py` (follows: B9), `probe_debt.py` replays stored entries, `proof_level._replay`, `story_run.s6_reprove`, `s5_precheck._all_soft` reads the same soft rows | name each; a test for each that changes | P2, P4c, P6 |
| AR-20 | Census rows and `gate-registry` counts change; `safety` at ceiling 50, `meaning-proxy` at 8: no new unit in either; `judge_alternative` row removed; the word-list row of F-P11 named | the census test; a raise is named in the verdict | every census line |
| AR-22 | `checks[]` with `entry` and `statement_sha`, `plan[]`, `check_key`, `author_green`, `plan_remaining`, `plan_unfinished` gain producers and readers; `matcher_span` and `line_proof_runners` are removed from the plan: never a producer | case-insensitive grep with a positive control; `test_field_producers.py` | P2-P6 |
| AR-23 | Empty: no checks, no model file, empty reason, empty `not_here`, `soft_assert_patterns` `[]` vs absent, `interruption_texts` absent | each named in §11.4, pinned | P1-P4c |
| AR-25 | New states `not_reached`, `plan_unfinished`, `not_owed` have exits | `design/state-exits.md` rows; `test_state_exits.py` | P4a, P4b |
| AR-28 | A check not read is an unknown: alone run or the role, never a pass or a blame | §11.4, tests | P4a |
| AR-29 | Code: heads, order, form rows, markers, plan. Role: the model, independence, realism, `not_here`, `product`. The tier above: the critic's outcome | census class per check below; `judgment:` line on each commit | all |

FR sections: A (FR-1, FR-2, FR-4, FR-46, FR-57), C (FR-13, FR-38), D (FR-18, FR-58, FR-59), E, F (FR-41, FR-55, FR-51), G (FR-30, FR-33, FR-47, FR-54). B: unchanged unless a person's text changes, one line.

### Census: every check this part adds or alters

Vocabulary: `scripts/tests/fixtures/judgment-census.json` (shape, xref, word-list, meaning-proxy, meaning, safety; owner data, judgment, intent).

| Check | Change | Serves | Class | Note |
|---|---|---|---|---|
| `checks_of` (new) | heads in a body, joined with the bindings | data | shape | never decides which matter |
| `run_plan` (new) | groups by form row and order | data | shape | independence itself is the role's; the plan reads the form the author wrote |
| `load_models` (new, beside `load_model` until P5) | keys, sizes, one of the kinds | data | shape | **`invert`'s reason, `supposes` and `not_here` are checked for presence only**, never read |
| `_model_region` (new) | the edit stays off matcher, expected, `.not`, message | data | shape | a row match; errs toward refusal with a door |
| `_edit_shape` (new) | removed and added balanced; file shape adds up | data | shape | B1 |
| `_no_role` (new) | the dispatch row's stage is S6 | data | xref | a role cannot type it |
| `judge_probe_row` (N3b, altered) | marker, or passed, or the role | data | xref | `proved_by` by a place does not exist |
| `_judge_joint_rows` (new) | a loop of `_row_by_marker` over tokens; the walk's next move | data | xref | a location orders the walk, never proves |
| `_cut_by_runner` (new) | the row's text holds a row of `interruption_texts` | data | word-list | runner text, data row; **only demotes, never proves** (F-P11); the census test decides whether this is a new unit, a raise is named |
| `author_green_of` (new) | run block's identity joined with these bytes | data | xref | unknown is `None` |
| `_aggregate_record` (new) | worst of per-check verdicts; complete or not | data | xref | |
| `_product_entry_holds` (new) | receipt exists, level product, same bytes, location on the key's span | data | xref | the critic names it; code joins (Q1) |
| `_evaluate`, `_probe_from_receipt` (altered) | a `scope: one_check` receipt covers no instance | data | xref | (Q1) |
| `red_sandbox.verify` | unchanged | data | meaning-proxy as it stands, not read in the census file | its result now only gates publication of a fact; it proves nothing for an instance (B9); no count change expected, the census test decides |
| `judge_record` | by check key | judgment | xref | unchanged class; the critic's judgment is still never judged |
| `judge_alternative` | removed | - | - | census row removed, count shrinks |
| "stopping where independent" | the critic's reading | judgment | - | no code check; a `mechanical` finding (EP-M) |

No check reads a role's wording; no phrase list over a role's or a person's text is added.

## §11.2 Forks and the owner's questions (nodes are written on the recommendation, «по рекомендации, до слова владельца»)

t-2076 found all nine first forks on the owner's side, F-P4 stricter than the word. The critic's reading is carried in each.

**F-P1 What is "every check".** The owner: «на каждый ассерт»; 29 of the 169 measured checks are `setup:` / `step` / `precondition` lines.
- A. (**recommended**) Every head of a known form in the test's body, setup included, plus every check a binding names outside the body. Literal. A setup helper's checks that no binding names are not listed, with a count in the note (named, the owner should hear it).
- B. Only checks bound to a Then. Cheaper (§11.6: 48 runs against 77), but a green-by-default setup check stays unproved: against the owner's point 1.
- If B: `checks_of` filters, nothing else.

**F-P2 The manifest shape.** The carriers already hold the list, twice: `then_bindings[]`, `trace_binding.assertion_refs`. A second typed list would go stale the way these do: arm B's rows for TC_001 read `:46, :47, :48` where the checks stand at `:47, :48, :49`, and `:46` is a blank line.
- A. (**recommended**) `assertion_id` stays a scalar; no new manifest field; **code enumerates the checks from the bytes** (`checks_of`) at probe time, and joins the bindings only to label a check with its Then (`then: null` when no row hits). Readers of the id (`acceptance.py:1055,1093`, `window_record.py:618,647`, `red_sandbox.py:711`, others as in the first draft) stay untouched.
- B. `assertion_ids: []` in the row: about ten production readers, a reader for old rows, the automator types what code can read.
- If B: one more node before P2, and P4b grows.

**F-P3 Where "dependent" is declared.** The owner's «правильно» covers the rule "determine what is independent, what is sequential"; who declares it is not in the words.
- A. (**recommended**) **The form is the declaration.** The author writes dependent checks stopping and independent ones non-stopping; the plan reads the form; the critic reads the test and judges. No field, no second truth. Bypass named by t-2076: writing everything soft shrinks the plan and a dependent soft check reads junk; the critic is the one reader (EP-M), AR-29 correct. An unlisted form (`expect.configure({soft:true})`) is a head of an unknown form: EP-P.
- B. A field `dependent_checks: [{check, after, why}]` on the row. An explicit trail, but a typed copy of what the code already says.
- If B: `run_plan` takes the field and P7 adds a form line.

**F-P4 Does the marker need the author's green?**
- A. (**recommended**) Yes for a model; not for an inversion. Green unknown or red: `incomplete`, `cause: judgment`, with `author_green` as a fact. **Measured gap this opens:** `author_binding` matches `instance_content_sha`, and arm B's TS record has it empty (one record read), so today every TS model would read as unknown. P4a's `author_green_of` also accepts the run block's `source_fingerprint.test_content_sha` equal to the fingerprint over the author's bytes. Direction: any edit in the file gives `None`, the role. How often `None` falls: unknown, §11.6 (b).
- B. Marker alone. Free, and a check already failing on its own "proves" a model.

**F-P5 `wrong_location`.** «В обоих случаях пусть смотрит роль».
- A. (**recommended**) It stops settling: with failure text the row goes to the critic, the location a fact. `no_failure` on a passed row stays code (a status, not a reading of a failure). Old records read as today. A model's region throwing before its check lands here too.
- B. Keep it settled for an inversion. Two rules, and a verdict by a line.

**F-P6 The run's selection. Returned, no node until the word.** Measured: a probe runs a selection wider than its test and reads one row (`testsuites tests=` 15 and 16 in most of arm B's reports); t-2076 recounted 31 of 49 reports carrying more than one failed test. With 3x the runs this dominates the time.
- A. (**recommended**) One node after P4c narrows a `red_probe` to the selected test where the form can (`--grep` exact title, a data row); falls back to today's selection when it cannot. The builder reads `build_request` and `instance_contracts` first; `instance_contracts` **not read here**.
- B. Leave it. Time as in §11.6.

**F-P7 Retries.** Measured: the stand's `retries: 1` (`playwright.config.ts:28`) reruns every failed test; P0 s7: the text appears twice, one testcase in JUnit. **P0 s7: `--retries=0` through `run-playwright.mjs` overrides the config.**
- A. (**recommended**) A data row appends the flag to a `red_probe`'s argv; how it fires: F-P10. The project's config is not touched.
- B. Leave it: every probe pays twice on purpose-made reds.

**F-P8 A check with no model when the critic did not write one.**
- A. (**recommended**) Refusal before a byte is written, naming the checks with their lines and only the doors that open (S5). «Предпологать … должна роль». **No role** is told by the context, never by a flag a role can type: the dispatch row's stage is S6, or the call is `--s6-close`. There: stored entries, then inversion with `reason: "no role at this call"`, written by code, so the record says so. **S5 settle under the critic's dispatch** has a role later: nothing stored: the item stays with the critic, "model owed", no run. `--mutation invert` selects nothing: it is no bypass.
- B. Default to inversion with `reason: none given`. Cheaper for a lazy critic, and the owner's rule becomes optional.

**F-P9 May a model touch the check's own statement?** Today `plan_alternative` refuses it. In arm B the value is read inside the statement on 101 of 169 checks, and on the 68 others the actual is a locator.
- A. (**recommended**) Yes, only the **actual argument**, as model kind `actual`. Never the matcher, the expected value, `.not` or the message (`_model_region`). A form with no `actual_arg` row: `find` before the statement, or inversion.
- B. Keep the refusal: API checks with an inline read cannot be modelled at all.

**F-P10 (new, S10) How the retry row fires on a project's own script.** Read: `runner_identity` gives `form_id` "" for "the project's own script; the factory does not read inside it" (`launch_check.py:701-726`), so a row per form never fires on arm B's `node scripts/run-playwright.mjs`. Whether arm B's argv gets an empty form id: not run, P0b prints it.
- A. (**recommended**) The row lives in the language's entry with the grammar `M-TS2` already uses, a `source` regex over the test file: `"probe_no_retry": [{"source": "from\\s+['\"]@playwright/test['\"]", "flags": ["--retries=0"]}]`. A script that does not forward it ends a run with no rows or `error`: that call reruns the row once without the flags, with a note, and the rest of the walk drops them. INV: a flag never becomes a verdict on the test.
- B. Per-form only. On arm B nothing fires; every probe pays twice.
- C. A project config key `red_probe_args` (AR-3). Exact, but one more thing to set at onboarding, and absent by default.

**F-P11 (new, B6) How "the test was cut" is told when every token is present.**
- A. (**recommended**) A data row of the runner's interruption text (`interruption_texts`, `"Test timeout of \\d+ms exceeded"` on TypeScript, P0 s4's verbatim line). It only demotes. Absent on a language: nothing to demote there, the absent-token case still holds (named residual).
- B. No text read: the last read token of every group always reruns alone. No word-list, +1 run per group (about +44 runs on arm B, §11.6).

Owner's questions, as t-2076 wrote them, with what the nodes do until the word:

| Q | Question (русскими словами) | Recommendation; what the nodes do |
|---|---|---|
| Q1 | Проба продукта (`red_sandbox`) ломает сам продукт и считается доказательством по строке и тексту библиотеки, без роли и за весь тест. Оставить так как исключение, или считать её только за одну проверку и через критика? | Второе; EP-W, P6. If the owner names the exception (P31): the `one_check` lines of `_evaluate` and `_probe_from_receipt` fall, nothing else |
| Q2 | В 68 проверках из 169 проверяется элемент экрана. «Значение сломанного продукта» там выглядит как подмена элемента (`page.locator('#qa-none')`), что близко к перевороту. Это то, что имелось в виду, или на таких проверках честнее сразу переворачивать с записанной причиной? | Роль решает сама; §11.8 shows both; no code differs |
| Q3 | Проверка внутри `if`, куда этот параметр не заходит: можно ли критику записать «этот прогон сюда не доходит, потому что …», и проба за эту проверку с этого экземпляра не нужна? | Да; EP-T. If no: the entry kind falls, the critic reports `unverified`, the person is asked |
| Q4 | Если замер покажет, что на совместном прогоне маркеру верить нельзя: каждая проверка отдельным прогоном (примерно 58 лишних прогонов, без роли) или совместный прогон и всё читает критик (136 лишних ходов)? | Первое. **P0 s5 did not fail (the passing marker absent, control s1 holds), so nothing rests on it now**; it stays with the owner in case P0b's JUnit case (s1j) disagrees |
| Q5 | После этой пачки формулировка библиотеки больше не доказывает ничего: все проверки без нашего маркера стоят одного хода критика. Подтверждаете? (Слово «Только наш текст» читается именно так.) | N3b is written so. Named residual: an old receipt by `fires_as` on the same bytes stands, reached only by a plugin change inside a story |
| Q6 | На Java и C# есть мягкие формы (`SoftAssertions`, `assertAll`, `Assert.Multiple`), фабрика их пока не читает: такие тесты работают, но идут по прогону на проверку. Считать это отдельным узлом сейчас? | Узел в пачке TR2-16; the critic still advises the soft form (EP-M). Lead's row: §11.9 |

**Closed by the owner, 06.11.2026; carrier: the finding.** Q1 «да»: the second option stands. Q2 «ок»: the role decides, §11.8 shows both. Q3 «ок»: EP-T stands. Q4 «при софт падении 3х ассертов там будет 3 наших сообщения. Надо делать их разными и всё»: every check has its own marker text, the joint run stands, and no fallback road is built; a JUnit result that disagrees (P0b s1j, s5j) comes back to the owner as a measured fact, not a chosen fallback. Q5 «да»: N3b as written. Q6 «надо чтоб читала, можно реализовать отдельным узлом»: node P1b (TR2-17), not TR2-16. Where this file still says "по рекомендации, до слова владельца" on Q1-Q3 and Q5, read "by the owner's word".

Also to tell the owner, no fork: (i) «Только наш текст» ends `proved_by: fires_as`. (ii) `--mutation alternative` was a non-goal of the first dispatch; bringing it into the road (P5) is the designer's reading of «разные рабочие пути для одного и того же это баг» and «Что именно другое? Красная проба проверяет что кейс умеет падать на каждой проверке»; F8 of t-2045 stays by recommendation. (iii) P0's s6c is not measured.

Small choices closed: §11.7.

## §11.3 What changes in the revised t-2045

| Item | Fate | What exactly |
|---|---|---|
| §0 table, steps 1, 3 | **replaced** | §11.0 steps 1, 3-4 |
| F1=D, F13 | **dissolve** | proof by the place of a failure does not exist, no label to choose |
| F3, F12=A, F4, F7, F9, F10, F11 | stand | F12's fixture `error` row goes to the critic, the same rule |
| F8 | **flips, by recommendation** | "F8's own node" falls; the alternative is inside the road (P5) |
| N0 | **stands, built** | report stays as facts; answers 1-2 now decide nothing; answer 4 (`frames_deepest`) still feeds N5b |
| N1 | **stands, in work** | `_target_of`, `check_on_line`, `test_body_span`, `_source_checks`, `_python_checks`, `--at <file>:<line>` are what P2-P4b reuse. From P4b no call reaches `_target_of`'s `assertion_id` and `first` branches; P4b removes them with their pins unless the builder's grep finds another reader (then a report line). S8's weight goes |
| N1b | stands, with one move | P4a moves `probe_record_path(..., target_line=)` to `work/probes/checks/` (S3) and adds the check key and the entry's sha to the repeat identity |
| N7 | stands | `expected` goes; P4b changes `_refuse_flags`' door `--mutation invert` to name the `invert` entry (FR-2) |
| N2 | **shrinks** | items 5-6 and the `line_proof_runners` part of 2 **fall**: no `matcher_span`, `no_proof_after`, `no_proof_args`; drop `test_matcher_span_*` and `matcher_span` from the plan contract. Reader key, Python marker, detail keys, `frames_deepest` stay |
| N2b | stands, one addition by P1 | `actual_arg` rows beside `fires_as: null` |
| N3a | stands | |
| N3b | **rewritten whole in §11.5** | t-2045's N3b section, its §6 pin rows and its edges E3.4, E3.5, E3.8, E3.9 are void |
| N4 | **grows** | All failed rows with text are `cause: judgment` by construction; `facts` carry `check_key`, `model`, `author_green`. `--judge` by check: P4b. t-2045 E4.3, E-Q stand |
| N5, N5b | stand | N5b's guard reads on a model's marker too: a helper check called other than once: critic. N5b's "step 8" is N3b's `_row_unsettled` here |
| N6 | **rewritten by P7** | Bullets on "the first", `proved_by` by a place, "with no `--at`" fall. **Passes to P7:** charter :71-72, `s5.md:200`, `brief_pack.py:224-227`, so its §3 rows never write "the Then's check". **N6 keeps:** `execution-lifecycle.md`:60 and its slice, `OFF_TARGET_DOOR`, `reached` :1483-1484, `probe_debt` :161, :222, `probe_by_code.py` docstring, help, `_run_and_judge` reason text. `test_no_python_exception_text` loses its F8 lines. N6 lands after P7 |
| t-2045 E-D, E-G, E3.x, §2 F1's adversaries | simplified | t-2045 E-D: no rank of proofs, `intended_failure` only if every row holds the marker; all else goes to the critic with no span rule |
| §3 rows marked F8; `ROAD_EXCEPTIONS` F8 lines, its `_judge_run` line | fall | P5 |
| Live proof | grows | §11.5 end |

Order, whole: N0, N1 (in work) → N1b ∥ N7 → N2 → N2b → N3a → N3b → N4 ∥ N5 → N5b → **P0b** (before P1 by choice, before P4a by need; it depends on no code) → **P1** → **P2** → **P1b** ∥ **P3** → **P4a** → **P4b** → **P4c** → **P5** ∥ **P6** → **P7** → N6. P0 is done. No release between (t-2045 §6): an interim state on the branch reaches no project.

## §11.4 Named edges, each with its invariant

- **EP-A A test with one check.** A plan of one row; a joint run of one is the plain run; nothing about it differs but the record's `checks[]` length. No check at all: `checks: []`: t-2045 E-F (a refusal naming the data row and `--at`), never a pass. INV: the same road for one or many; an empty list never reads as "all proved".
- **EP-B A soft check after a stopping one** (`add_to_cart.spec.ts:122`, then `:128`). The stopping check goes alone, the soft ones in the next run with `:122` untouched. The stopping check may join a group only as its LAST check in source order. **Measured:** P0 s2 (soft markers survive, the hard one's marker appended last), s3 (a soft line after a failed hard one never runs). INV: **a group holds at most one stopping check, last**; a check behind a stop is never counted as read or unread on that run.
- **EP-C A parameterised row.** A shared check gets one model entry with no `instance`, or one per `instance`. Rows of one node (pytest `[a]`, `[b]`): the marker must be read in EVERY row (`_worst_of_rows`, t-2045 E-D). A model value equal to one row's healthy value (`expect(x).toBe(qty)`, `actual: 999`, `qty=999`) gives `passed` on that row: not proved, the note names the row; the critic writes an expression. Titles from a loop (`TC_008`) are instances, each with its own record. INV: no row is picked silently; a proof never covers a row that passed.
- **EP-D A check in a helper called by two.** Real: `cart.spec.ts:176 separateOwners` from `:207` and `:211`. Inverted or modelled in place, under the file's lock and byte copy (t-2045 E-B); each instance has its own record and receipt, never shared; called twice inside one test: N5b, the critic. A check outside the body always goes in its own run (§11.7). INV: a receipt of one instance never counts for another; bytes restored or the copy stays; the product is never touched.
- **EP-E Two edits where one failure masks another.** Masking by a stop: forbidden by EP-B. Masking by time: a web-first check waits its whole `expect` timeout, and a transient element may be gone by the next check; a test timeout may end the test mid-way (P0 s4: `s4n6`-`s4n8` absent). Hence EP-F, EP-V. INV: **a joint run proves firing, and never non-firing.**
- **EP-F A check that does not fire in a run.** The record names it by `check_key` with `read_in_joint: false`. By the row's status:
  - **passed**: nothing failed, so nothing masked: every check of the group `no_failure`, no rerun (EP-H per check).
  - **`error`, or no row**: t-2045's rules for the whole group, no verdict per check.
  - **failed, token absent, group of 2 or more**: `not_reached`, **and it is rerun alone**, once, in the same walk (others untouched), unless EP-G's stop applies. Alone: its marker read: proved under the same conditions (a note "not read jointly"); passed: `no_failure`, for a model under EP-H; failed with no marker: the critic.
  - **failed, token absent, run of one**: **no rerun: it is already alone.** `_row_unsettled`, the critic, the failure text in the facts. A throw in that check's own arguments lands here (P0 s6b).

  INV: which check is always named; a check is never blamed on a run's silence; a marker read in that same run still stands (the token exists only there), except EP-V's.
- **EP-G A chain longer than two, with an inner failure.** Each stopping check gets one run, in source order, with everything before it untouched: `a`, then `b` with `a` as written, then `c`. n links, n runs; no combination. **The walk stops only when the failure's file and line (a fact, never a proof) lie on the span of an EARLIER check of the plan, one this run did not edit**, and the run's edit does not stand before that check: the run's absent keys and every later row are `not_reached`, listed in `plan_remaining`, the aggregate `incomplete`, `cause: judgment`, the text in the facts, the critic reads. **Any other failure (a helper's throw, the check's own argument, no location, a `find` of this run standing before the earlier check): the walk goes on**; the run's key goes by EP-F. The same call on the same bytes continues (proved rows skipped). INV: a later link is read only behind green earlier ones; a chain is never compressed; a throw in `b`'s argument never kills the proof of `c`; a stand hiccup on `a` does not spend one failing run per later check.
- **EP-H A model's check passes.** `actual` kind: the check accepted the supposed value: `no_failure` (`test_defect` to weigh, by the critic; or `not_here`, EP-T; the model is on the record). `find` kind: the read may not reach the check, code cannot show it on every reader: `incomplete`, `cause: judgment`, the model in the facts. `model_reach` goes (P5). INV: the author is not blamed on an unproved reach.
- **EP-I The manifest shape, old rows.** F-P2 A: no manifest change. **Temporal:** a receipt written before this batch (no `checks` on a live one, no `scope` on a product one) reads as today; an old standing receipt on the same bytes stands with an info line "proves one check" (a story keeps its plugin generation, B-014); on new bytes the plan runs. After this batch every receipt writer writes `checks`, so a missing key can only mean old. INV: a receipt measured on other bytes never counts; a new receipt claims only what its `checks` hold. The aggregate's `target.is_assertion_id`: True when the id's line lies in a proved check; None (counts, info line, `_unknown_target_notes`) when it lies in the body on no check (arm B's `:46`); False when it lies outside the body and the plan. `receipt_off_target` is unchanged. TR2-1's write check still lands.
- **EP-J Cost and the wall.** **Today no per-window cap on this probe was found in code** (Grep of `probe.*budget|cap` over `scripts/`, `s5.md`, charter: the same call finds `investigation_probe`'s budget; none for this probe); `s5.md:125` says "one critic probe per test" in words, which P7 turns into "per check". A plan is not cut by a budget: cutting would be a silent unproved check. Limits: one call walks one instance's plan within `--timeout`, default `RUN_TIMEOUT_S` (1860 s, the existing limit, now per call). What is left: `plan_unfinished: true`, `plan_remaining: [keys]`, `verdict: incomplete`, `cause: tooling`; the same call again continues. **A killed walk writes no ending,** so per-check records and the aggregate are written after EVERY row, marked unfinished until the last; a copy left behind is restored by the next call's `scan_copies`. A critic's Bash foreground ends at 600 s (reasoned from the tool's documented limit, not run): P7 tells him to run a plan of more than 3 rows in the background and read the answer. The brief card prints `plan_runs` per instance. `probe_could_not_run` is False for `plan_unfinished`: the door is the same call, not a person's word. INV: an unfinished plan is never `intended_failure`; a person is not asked about a plan a repeat of the call finishes.
- **EP-K What `approved` needs.** A receipt is published **only when every check of the plan is `intended_failure` by the marker or by the critic's `fires`, or `not_owed` (EP-T), and at least one is proved**; `window_record` and `acceptance` then read the aggregate as today. Any check unproved: the instance's word is `unverified` with `sensitivity_proof_missing_reason` naming the check keys, or `rejected` with a `test_defect`; the person's `probe not proved: <case>` remains the last door and covers the case's unproved checks, one word. A check proved by inversion with its reason counts the same as a model. INV: `approved` never stands on one proved check of several; a person is asked only after the critic said `cannot_judge`.
- **EP-L The critic has no idea.** `{"check": k, "invert": "<why no other value is known>"}`. Empty reason: refusal (shape). The record carries `probe_kind: invert`, `reason`. Inversions and models may share a joint run; each has its own marker. On `invert: null` forms it is not offered (S5). INV: code never reads the reason; inversion is reachable wherever the form has a pair.
- **EP-M A test written stopping where the critic judges the checks independent.** `findings[N]`, `cause: mechanical`, naming the lines and the framework's form: "`:47-:49`: independent, write `expect.soft`". The author's, once, in words; **no person's word**; the existing route of the `cause` list. No assertion and no expected value changes. Its price: `code_sha` changes, and on arm B's records (`instance_identity: {}`, `test_code_sha: ""`) that makes every proved check of every instance in that FILE stale: a re-walk of the file, §11.6 (a). **The critic judges by what he knows of the framework; the row `soft_assert_patterns` decides only the plan.** So on Java or C# he may ask for `SoftAssertions`, `assertAll`, `Assert.Multiple`; the factory does not read those scopes yet and the plan stays one run per check (Q6). A framework where he knows no soft form: no finding, the same road. A soft check the critic judges dependent (its failure leaves the next one reading junk): also `mechanical`. If the author disagrees: the digest's `for_the_reviewer`; the critic's reading stands. INV: code never judges independence; a person is not asked about test style; a test stays correct while the finding is open: the plan just costs more.
- **EP-N A model that does not build or breaks the file.** Before the write: `_edit_shape` (P3 item 2) or, on the AST reader, `ast.parse` of the new text: refusal naming the check and what failed. A balanced edit is never refused for its brackets. Compile error or a collection error at run: row `error` or no rows: t-2045's rules, the critic with the text; the model file may change and the same bytes run again (identity holds the entry's sha). INV: bytes restored; a bad model never blames the test.
- **EP-O Two checks on one line.** Keys `<file>:<line>` and `<file>:<line>#2`, by head order on the skeleton. `--at <line>` means a plan of the first; the second is reachable as `--at <line>#2` (P4b). INV: the second is on the plan and owed; never covered by the first's marker.
- **EP-P A check of an unknown form** in the body. Not on the list: `checks_of` can't see it, and that's stated: the plan prints "heads of forms the factory reads" and the critic compares with the test (`unverified` + a data-row note). An `invert: null` form known to the table: listed, model allowed, inversion not offered. INV: a list never claims to be the test's whole truth to the role.
- **EP-Q A check in a branch or a loop** (`cart_page.spec.ts:84`, `cart.spec.ts:199`-shaped). On the plan; a branch not taken gives no marker: EP-F, EP-H; the critic's door is EP-T. In a loop, the marker appears many times: read once. INV: order and reach are not guessed.
- **EP-R Pair conflicts.** "A soft form in the row" vs "the author chose stopping": form wins for the plan, the critic for the meaning. "Every check" vs "time cap": the cap ends the call, never cuts the list. "One marker per check" vs `MARKER_INSERT_CAP`: no marker on overflow: role. "Default model" vs "S6 close, no critic" (F-P8): stored entry, else inversion, named; t-2045 E-L for the report. "Refuse before a byte" vs "no-role inversion on an `invert: null` form": no refusal of the walk: that check's row is `incomplete`, `cause: tooling`, the others walk, the digest line names it.
- **EP-S (new) `--oracle` on the road.** `--oracle` stays explicit and wins the file (t-2045 E-I), and from P4b it **selects rows**: the checks of that function, through the same loader, each its own run, per-check records, aggregate rebuilt, no partial receipt. INV: an old record's replay with `--oracle` does not publish on one check of several.
- **EP-T (new, B10) A check this instance does not reach.** Real: `cart_page.spec.ts:83-85`, `if (!guestKept) { await expect.soft(notice, 'Then 1: …').toBeVisible(); }`. `{"check": k, "instance": i, "not_here": "<why this instance does not reach it>"}`: `instance` required, the why present, neither read by code. The row leaves the plan's runs for this instance; the aggregate shows `verdict: not_owed`, `reason`; the window block lists it by key; a tier above reads it. The `no_failure` note on such a check names this door. All checks `not_owed`: no receipt, `incomplete`, `cause: judgment` (nothing is proved). INV: a healthy test is neither blamed nor sent to a person for a branch its instance never takes; a receipt never stands on nothing proved; code does not judge whether the why is true (AR-29). Named bypass: a critic may write it on a reached check; only the tier above sees it. «по рекомендации, до слова владельца» (Q3).
- **EP-U (new) A key that moved.** A stored entry was written for `<file>:<line>` on other bytes. It is joined to the current plan by `statement_sha`, the sha of the check's whitespace-folded statement as the author wrote it, in order among equal ones; the model file of the current window is joined by key, as written. No join, or a `find` that no longer stands once: not applied: S5: "model owed" naming the key; S6: no-role inversion with a note. INV: a stored edit is never applied to a check it was not written for; the expected value in the statement is part of what is compared, so a changed expected value drops the entry.
- **EP-V (new, B6) A check cut by the test's timeout.** Measured: P0 s4: `s4n5`'s marker printed with `Received: undefined`, then blocks with no marker, `Test timeout of 6000ms exceeded.` in the body. Whether a check that would have gone green later prints it: s4b in P0b; reasoned yes. A row that **failed**: (1) any token of the group absent: the **last read token in source order** is demoted too; (2) all present, and `_cut_by_runner`: the last one is demoted. Demoted in a group of 2 or more: rerun alone with the absent ones. **Demoted in a run of one** (the row has the interruption text): `_row_unsettled`, the critic, `interrupted: true` in the facts. Alone again with the interruption text: the critic. It only demotes, never proves. No row on a language: only (1) applies: named residual. INV: top invariant (b): a marker of a check that never decided is never `intended_failure` by code.
- **EP-W (new, B9) A product receipt.** `red_sandbox.py --probe` breaks the product; its `verify` reads status, line and library wording. That stays what publishes the receipt, and from this batch it proves nothing for an instance by itself. The receipt carries `scope: "one_check"` and `checks: [{key, probe_kind: "product"}]` by its `assertion_location`. To count, the critic writes `{"check": k, "product": "<receipt path>"}`: code joins (exists, level product, `same_test` holds, location on `k`'s span) and the check reads `probe_kind: product`, `proved_by: critic`, no run. The others stay owed. Receipt's location unread: `checks: []`, the entry refused with the door `actual`, `find`, `invert`. **A language with no entry** (`AD` has no reader, no plan can exist, t-2045 E-E): `scope: "whole_unlisted"`, valid as today with a note "the factory cannot list this test's checks"; the critic's `unverified` stays his choice. The instance's level after a full plan is `live`; the product fact stands in `checks[]` (named loss of the higher level's words; D-0010 not re-read). INV: `approved` never stands on one proof of several, by wording, with no role; an old receipt is EP-I's. «по рекомендации, до слова владельца» (Q1).

## §11.5 Nodes

Shared `given:` as t-2045 §6 Shared, plus this file and `D:/ws1/yml-text-factory\docs\tasks\specs\reports\t-2045-n0-frames.md`, `D:/ws1/yml-text-factory\docs\tasks\specs\reports\t-2064-p0-joint.md`. `handoff:` builder's report plus a commit on the worktree branch; a `changelog.d/t-2064-pN.md` per node, one mutation per node with the line that kills it. New test file `scripts/tests/test_probe_every_check.py`: fast, parametrised over `python`, `typescript`, `csharp`, `java`, a red names the language and branch (P16). Witness: the test FILE of each owned path, fast only; slow files (t-2045 §6 list, plus `test_story_run_*`) are EDITED and named "CI", never run locally or waited for. Canon: CI on the batch branch.

**The fixture helper (B4).** `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\probe_entries.py` (new, P3; no `test_` function, English). `write_invert_entries(task_root, dispatch, keys=None, reason="fixture: the inverted form is what this test reads")`: `keys` None takes every key of `probe_by_code.py --plan --json`; writes `work/probe-models/<dispatch>.json`. The flip of a wrapper is one call to it, never an environment variable or a flag in product code. INV: no test door exists in the tool.

**Pin owners, P3-P7** (each edited in the node's commit; count = lines by one regex, t-2076's, not tests; "reads" = not read here, the builder reads and edits by the same rule):

| Node | File | Pins |
|---|---|---|
| P3 | `test_probe_marker.py` | `marker_token` callers (a key argument), `_with_marker`'s docstring wording on "INVERTED", `test_fires_none_skips_guard` new |
| P4a | `test_probe_target_fact.py` | :252-258 (`keep_standing_record`) hold; beside path now under `checks/` |
| P4a | `test_probe_one_road.py` | N1b's `test_new_record_never_overwrites_proved`, `test_beside_record_blocks_its_own_line`: the path |
| P4b | `test_probe_by_code.py` (CI, 32) | wrappers `run` :326, `run_recorded` :1148, `run_dispatch` :2818 call the helper first; `run_close` :2688 does not (S6: `no role`); `a_rerun_is_idempotent...` :1311; a fixture test with several asserts now walks: its stub answers per run; call counts in `_calls` :1787 readers |
| P4b | `test_probe_by_code_languages.py` (CI, 4), `test_probe_by_code_copy.py` (CI, 9), `test_probe_binding.py` (CI, 6) | their wrappers (reads), the same call |
| P4b | `test_probe_marker_judgment.py` (9) | `world` :66 and the direct calls: the helper, or `--check` where several checks |
| P4b | `test_probe_target_fact.py` (2), `test_probe_gap_door.py` (2), `test_probe_not_proved.py` (1), `test_probe_container_answer.py` (1), `test_handoff_init_author.py` (1) | the helper (reads whether each reaches a real probe; a stub stays) |
| P4b | `test_probe_one_road.py` | N1's `test_default_target_is_assertion_id` :215, `test_second_check_is_the_then` :229, `test_no_id_takes_first_with_note` :307, `test_two_checks_on_one_line_the_first_with_a_note` :412: removed or reduced with `_target_of`'s branches; `test_at_*` :240-277 and N1b's `test_printed_door_runs_second_call` write the entry first |
| P4c | `test_probe_debt.py` (CI, 10) | replay cases, `test_debt_replays_file_line_at` in `test_probe_one_road.py` :424, N7's `test_debt_replays_old_expected_as_invert`: an old record is now "model owed" under S5 |
| P4c | `test_story_run_s6.py` (CI) | :2192-2194: the argv stays; reads replies as stubs |
| P5 | `test_probe_by_code_alternative.py` (CI, 9), `test_probe_one_road.py` | `--mutation alternative` calls become `--alternative`; old model shape refused; `ROAD_EXCEPTIONS` F8 and `_judge_run` lines |
| P6 | `test_window_record.py` (CI), `test_proof_level.py` (reads), `test_red_sandbox_probe.py`, `test_red_sandbox_reports.py` (reads) | a new product receipt carries `scope`, `checks`; a `one_check` receipt is not an instance's level |
| P7 | `test_story_run_s6.py` (CI) | :262, :264: `check_in` of "one probe per new/changed test" phrases in the phase text |
| P7 | `test_code_critic_probe_rule.py`, `test_charters_s5_s9.py`, `test_brief_pack.py` (CI) | texts |

### P0 — measured (done, report `t-2064-p0-joint.md`); the table every later node reads

| Case | Result (as read in the report) | Effect |
|---|---|---|
| s1 three soft | **three markers in one failure, each its own block** | joint road stands: P2, P4a |
| s2 two soft, last hard | **all three, the hard one last** | EP-B's "last" stands: P2 item 2 unchanged |
| s3 hard, then soft | **second marker absent** | EP-B stands |
| s4 eight soft locators past the timeout | **`s4n1`-`s4n5` read, none earlier lost; `s4n6`-`s4n8` absent; `s4n5` `Received: undefined`; three markerless closed-browser blocks; final status not measured (no JUnit, killed at my 120 s cap)** | P4a: `_problem_texts`, EP-F's alone rerun, EP-V from this evidence; P0b finishes it on JUnit |
| s5 marked soft pass beside a fail | **passing marker absent; control s1 holds** | joint proof by marker stands; Q4 not triggered; P2, P4a, §11.6, P7 as written |
| s6a substituted value | **marker present** | models keep the marker: P3 item 4, F-P4, §11.0, P7 |
| s6b throwing actual | **marker absent, `Error: boom from thrower`** | the role, by EP-F's run of one; no new rule |
| s6c hard web-first | **NOT MEASURED (no result under the load cap)** | owed in P0b; no rule made from it; owner told |
| s7 `retries: 1` | **text twice, JUnit one testcase; `--retries=0` through the wrapper overrides the config: one attempt** | F-P7's row (P1), fires by F-P10 |
| wrapper | **`--reporter=line,junit` replaces the config's reporter when `--junit=` is given; every other argument forwarded** | P1 reads it: the row adds no reporter flag; the report stays the JUnit the probe reads |
| p1 pytest | **marker in `message` and body, the `assert` line after** | agrees with N0 |

### P0b — the rest of the measurement, before P4a (scratch, no product)

Status: RUN twice (06.11.2026, commit 20830d749, and 10.11.2026, t-2259; both agree), report `docs/tasks/specs/reports/t-2064-p0b.md`, read by the Lead 10.11.2026: no "stop, owner" row fired. Fired rows: s4b "marker read on the undecided check" (EP-V as written, P4a step C pinned on this body); s6c "marker present"; form id "" (F-P10 A as written); s1j three markers; s5j the passing marker absent; s4c green, no marker. s4j: no earlier marker lost, but the CUT POSITION moves with load (s4n5 in P0, s4n6 here) - **P4a pins on structure (the timeout line, a block with no `Timeout:` line), never on a fixed index of the cut check.** P4a may start.
`given:` this table; `t-2064-p0-joint.md` (config shape, marker form); `D:/ws1/mybooks-stand\tr-probe\node_modules\@playwright\test` (1.56.0); `D:/ws1/mybooks-stand\tr-arm-b\scripts\run-playwright.mjs`.
`owns:`
`D:/ws1/mybooks-stand\tr-probe\_p0b-t2064\` (new; no existing file touched; removed at the end)
`D:/ws1/yml-text-factory\docs\tasks\specs\reports\t-2064-p0b.md` (new)
Cases, `retries: 0`, `timeout: 6000`, `expect: {timeout: 1000}` unless said, each through `run-playwright.mjs --junit=<abs>`, XML read and pasted:
- **s4b** `page.setContent` with a script adding `#late` at 9000 ms; `await expect.soft(page.locator('#late'), m('s4b')).toBeVisible({ timeout: 30000 })`, then a second soft check on `#none`. Question: is `qa-probe-s4b` in the failure body when the check was still waiting at the test's timeout? **Control s4c:** the same, `#late` added at 1500 ms: green, no marker.
- **s4j** s4 again to its end: the JUnit body: which markers, the timeout line, the test's status.
- **s1j, s5j** s1 and s5: the same answers in the JUnit CDATA (P0 read them in line output; the probe reads JUnit).
- **s6c** `await expect(page.locator('#none'), m('s6c')).toBeVisible()`, hard form: marker in the body?
- **form id** `python -B -c` (a pure read) printing `launch_check.runner_identity(["node", "scripts/run-playwright.mjs", "--junit=x"])`: `form_id`, `no_direct_form`.

One attempt per case with a 180 s cap; no retry loop; note the machine's load at the start. A case with no result: "not measured".

| Case | Result | Effect (written before the run) |
|---|---|---|
| s4b | marker read on the undecided check | EP-V as written: P4a's step C pinned on this body |
| s4b | marker absent | step C (2) falls to s4j's reading; step C (1) stays: `s4n5` is measured; owner told |
| s4b | not measured | EP-V as written (the safe side: it only demotes); owner told. t-2076's "go alone until measured" is not needed: EP-V covers it |
| s4c | a marker on the green control | stop, owner: the whole marker rule is in doubt |
| s4j | an earlier marker lost in JUnit, or status not `failed` | P4a reads the row by what is measured, report line; if tokens are lost on JUnit: Q4, owner |
| s1j | fewer than three markers in JUnit | as s5 fails: Q4, stop P4a, owner |
| s5j | passing marker present in JUnit | Q4, stop P4a, owner |
| s6c | marker present | as written |
| s6c | marker absent | a hard web-first check with a model goes by EP-F's run of one: the critic. No new code; §11.6's judgments grow by the count; owner told |
| s6c | not measured | no rule made from it; EP-F covers it as it stands; owner told |
| form id | "" (as read in the code) | F-P10 A as written |
| form id | non-empty | F-P10 A still; the report line |

`non-goals:` any package change; the app; arm A or B trees.
`edges:` a runner that won't start: report line. Load: the machine was at 100 % CPU in P0; never run beside another's run; no waiting loop. INV: a guess never becomes a rule; tree as it was (listing before and after, verbatim, plus the removal).
`DoD:` `Read` of the report: an answer per case, verbatim failure bodies and XML, the table applied line by line, the listing. No pytest.

### N3b — one row judge: the marker, or passed, or the role, for every language (replaces t-2045's N3b)

«по рекомендации, до слова владельца»: F-P5, Q5.

`given:` Shared; t-2045 §3, §4; N0's report for the canned rows.
`owns:`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\probe_by_code.py` (`parse_node` — `language`, `entry`, `tail` on the Python spec; `judge_probe_row` and new helpers `_row_by_marker`, `_row_passed`, `_row_unsettled`; `_judge_rows` — `among`, `proved_by`; `_judge_run`; `verdict_of` [removed]; `_judge_row` [removed]; `_judge_param_rows` — `judge_row` required; `_worst_of_rows` — `proved_by`; `report_rows` call)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\gate-registry.json` (`probe_verdict` site :574)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_one_road.py`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_marker.py`, `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_marker_judgment.py`, `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_plugin_param.py`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_by_code.py`, `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_by_code_languages.py`, `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_gate_registry.py` (CI)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\fixtures\probe-languages\` (canned rows)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json` (notes)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-2045-n3b.md` (new)

Required. `judge_probe_row` is a short sequence of named helpers. **Position invariant: a `passed` row is never read as proved; a step runs only when no earlier step settled the row; a row settled as not proved is never re-read by a later step; no step reads the failure's wording or place to prove.**

0. Python joins the road: `parse_node` adds `language: "python"`, `entry: AD.ast_entry(".py")`, `tail`; `_judge_run`: `judge_row` None → raw rows, `_judge_rows`; `judge_row` given (the alternative, until P5) → its branch, non-raw, unchanged. `_resolve_oracle`'s and `build_request`'s `reader` reads stand.
1. `_row_by_marker(row, token, detail, entry)`: `failed` + the exact token in the failure or error problem's message or text → `intended_failure`, `proved_by: marker`. The `missed` note of today's lines 1922-1924 stays only as a note. An `error` row is not decided here (F12=A). N5b adds its guard here; P4a loops over this function.
2. `_row_passed`: `passed` → `among`, `compiled`, `no_failure`. **`among`: `target_source` in (`at`, `assertion_id`) and (`len(candidates) > 1` or `target_outside_body` is not False)** → `incomplete`, no text, no cause set here, so the caller writes `cause: tooling`; never `no_failure`. The note says "a pass does not say which body ran" and names the target and the test. `--oracle` and `first` keep `no_failure` as today.
3. **Not a failure to read:** no report, no rows: `not_executed`, as today. Any status other than `passed`, `failed`, `error`: `not_executed`. `error`: `incomplete`, no cause, as today (N4 flips it). `site_unread` on a failed row: `incomplete`, as today (N4 flips it). A `failed` row with an empty text: `incomplete`, no cause: `cause: tooling` by the caller (N4's item 2).
4. **Everything else, that is a failed row with text and no token:** `_row_unsettled`: `incomplete`, `cause: judgment`, `judgment_facts`, with `location` (`_location_hits`' answer, a fact) and `frames` among them. Whatever the type, whatever `fires_as` says, whether the form takes a marker or not, whether the location hits or not. No `wrong_location` from this judge (F-P5 A), no `fires_as` proof.
5. `_worst_of_rows`: `intended_failure` only when every row is, and then `proved_by: marker`. Any other row speaks as today. No rank of proofs.
6. `proved_by` is `marker` or, from `judge_record` :4321, `critic`; `_receipt_core`'s `== "critic"` :2544 stays. No third value is written; an old record's `fires_as` reads as today (`_receipt_core` carries it unread, `window_record.py:612`).
7. Static guard `test_no_language_question_on_the_road`: walks the AST of **every** function of the road: `_target_of`, `_plan`, `judge_probe_row` and its `_row_*`, `_judge_rows`, `_judge_run`, `_probe`, `_resolve_oracle`, `plan_detector_mutation`, `build_request`, `_off_target_note`, `_refuse_flags`, `_new_record`, `_finish_record`. It refuses: a comparison with `"python"`; `.endswith(".py")`; a read of a name `detector`; `spec.get("language")`; `.get("reader")` or `["reader"]`; the words `not Python` in a string. Named exceptions only by a table in the test, module-level `ROAD_EXCEPTIONS`, each `(function, what, why)`: `build_request` reads `reader` (the runner's selection by node id, t-2045 §3 #10); `_refuse_flags` reads `reader` (`--model`, F8, until P5); `_judge_rows` reads `is_pytest_command` (a runner's report grammar, not a language); `_judge_run` reads `judge_row` (not a language, until P5). `_reader_plan`, `parse_node`, `put_back`, and the F8 functions are named as off the list with their reason. A negative control plants `if not detector:` and `spec.get("language")`. **P2-P4b extend the list** by their functions.

**Reuse.** `_location_hits` moves from part of a conjunction to a fact only: it decides nothing. `fires_on` stays only for the `missed` note; `fires_as` rows stay in data for the note and the echo guard (§11.7). Error direction of the judge: toward `cause: judgment`. Adversaries: a throw at the statement, a matcher's throw, a rejected promise, a `toPass` callback, a foreign `AssertionError` from a helper (`tests/helpers.py:12`), a same-numbered line in another file, a library frame, a matching library wording: none proves.

`edges:` t-2045 E-P, E-O. A soft collector: marker first (R9 as today). Param rows: step 5. `fires_as` null: no crash, no `missed` note. **The fixture case (F12=A):** an inverted assert in a Python fixture gives an `error` row: the critic, one judgment each. INV: «Только наш текст доказывает без роли»: `intended_failure` by code exists only on a read token.
`non-goals:` the seam, doors, words (N4); `red_sandbox` (P6); `judge_alternative` (P5); F11 (N5b); several tokens (P4a).

**Pin rows** (replacing t-2045 §6's N3b rows):

| File | Pins |
|---|---|
| `test_probe_marker.py` | The test ending :341: `wrong_location` at the same place becomes `incomplete`, `cause: judgment`. `test_failed_row_without_marker_same_line_not_by_marker` :344-353: lines :349 and :353 flip: a matching wording is `incomplete`, `cause: judgment`, no `proved_by`. `test_fires_as_still_fast_path` :404-412, all three asserts, flip; renamed `test_fires_as_no_longer_proves`, with and without a marker in the detail |
| `test_probe_marker_judgment.py` | `test_unknown_text_is_judgment_not_a_phrase_match` :119-121: the control flips: a library wording is judgment; the positive control becomes a row holding the token, `proved_by: marker`. `test_place_alone_is_not_a_proof` kept |
| `test_probe_plugin_param.py` | `DETAIL` :30 gains `message_marker: MARKER` and the road's keys; spec gains `reader`, `language`, `entry`; `_judge_run` calls :53, :70 pass `request` with a pytest `command.argv` and `keys` non-empty; K2's `matched_report_id` stays pinned. A plain script: `python -B` |
| `test_probe_by_code.py` (CI) | the stub's report text carries the token read from `seen`; `invert_plain_assert`, `class_method` :500, `hamcrest_style` :521, `raises_first` :544 (a throw at the statement: the critic), `oracle_in_a_helper` :900, `reporter_in_the_summary` :991, `through_real_run_suite` :812 |
| `test_probe_by_code_languages.py` (CI) | every case expecting `proved_by: fires_as` or `wrong_location` from a failed row: the critic, or the stub prints the token (reads) |
| `test_gate_registry.py` (CI) | :938 removed; `D13_ITEM_COUNT` :974 with its comment line, measured |

tests (`test_probe_one_road.py`, table-driven, one table per language; rows canned from real outputs): one test per step and language; `test_marker_outranks_place`, `test_passed_row_never_proved`, `test_only_marker_proves` (each language, a marker written and not read, with a `fires_as` that would match; and a message-less row whose `fires_as` would match), `test_wrong_place_with_text_is_judgment`, `test_failed_no_text_is_tooling_cause`, `test_error_row_no_cause_until_n4`, `test_unknown_status_not_executed`, `test_no_rows_not_executed`, `test_throw_in_first_arg_never_proved_by_code`, `test_throw_in_matcher_arg_never_proved_by_code`, `test_rejected_resolves_never_proved_by_code`, `test_topass_callback_never_proved_by_code`, `test_foreign_assertion_error_python_critic`, `test_throw_at_statement_same_on_each_language`, `test_all_rows_or_not_proved` plus the same **through `_judge_rows`**, `test_python_param_rows_all_judged`, `test_stale_id_pass_is_incomplete_not_no_failure`, `test_helper_never_called_pass_is_incomplete`, `test_oracle_pass_still_no_failure`, `test_old_record_fires_as_reads`, `test_critic_proved_by_keeps_quote` (`_receipt_core`), `test_no_language_question_on_the_road` plus its negative control.

`DoD:` `python -m pytest ai-packages/qa-factory/scripts/tests/test_probe_one_road.py ai-packages/qa-factory/scripts/tests/test_probe_marker_judgment.py ai-packages/qa-factory/scripts/tests/test_probe_marker.py ai-packages/qa-factory/scripts/tests/test_judgment_census.py -q`; `python -B ai-packages/qa-factory/scripts/tests/test_probe_plugin_param.py`; `python -B ai-packages/qa-factory/scripts/selftest.py --lang`. CI: `test_probe_by_code.py`, `test_probe_by_code_languages.py`, `test_probe_by_code_copy.py`, `test_probe_by_code_alternative.py`, `test_gate_registry.py`. AR-22 grep pasted for `test_file_frame`, `mismatches`, `message_head`, `matched_report_id`. `architecture: AR-13, AR-15, AR-19, AR-22, AR-23, AR-28, AR-29`; `judgment: judge_probe_row xref data; nothing proves by place or wording`.

### P1 — data: what does not stop, what is the actual, the runner's rows

«по рекомендации, до слова владельца»: F-P7, F-P10, F-P11.

`given:` Shared; P0's table (s7, wrapper).
`owns:`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\detectors.json` (`soft_assert_patterns` on csharp, java and `assertion_probes_ast.python`: `[]`; `actual_arg` per form; `probe_no_retry`; `interruption_texts`; `assertion_probes_note`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\assertion_detectors.py` (`ENTRY_FIELDS`, validation allowing an empty `soft_assert_patterns`, `actual_arg_of` [new], `soft_stated` [new], `no_retry_flags` [new], `interruption_texts` [new])
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_assertion_detectors.py` (:317-327 pins)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_every_check.py` (new)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-2064-p1.md` (new)
Required:
1. Every entry says it: `[]` = "this framework's plain forms have no soft form"; absent reads as `[]` with a note "the row does not say" (`soft_stated`).
2. `actual_arg`: `1` where `matcher_at` is `after_args` (TS `expect`, AssertJ `assertThat`); per form elsewhere only where verified in the library's docs and on a sample (xUnit `Assert.Equal(expected, actual)`: 2; JUnit `assertEquals(expected, actual)`: 2; `assertTrue(x)`: 1). Python `assert`: `"compare_left"`, read by the AST reader; a form in doubt has no key. An unverified row is not written (t-1968 rule).
3. `probe_no_retry` on `assertion_probes.typescript`: `[{"source": "from\\s+['\"]@playwright/test['\"]", "flags": ["--retries=0"]}]`; P0 s7 licenses it. `AD.no_retry_flags(entry, source_text) -> list`: the flags of the first row whose `source` matches, `[]` otherwise; a regex that fails: `[]`, a note. **Read from P0:** the wrapper replaces the reporter with `line,junit` when `--junit=` is given and forwards the rest: this row adds no reporter flag, and nothing here touches the config.
4. `interruption_texts` on `assertion_probes.typescript`: `["Test timeout of \\d+ms exceeded"]`, P0 s4's line. `AD.interruption_texts(entry) -> list`, `[]` when absent.
5. AssertJ `SoftAssertions`, JUnit `assertAll`, NUnit `Assert.Multiple` are soft SCOPES, not heads, already `invert: null` or unread: not soft rows here; node P1b reads them (the owner's word, Q6).
`non-goals:` readers of the rows beyond `AD`; plan.
`edges:` AR-23: absent and `[]` same plan; a regex that fails: gap, as :535. `s5_precheck._all_soft` with `[]`: False, unchanged (test). INV: "no soft form" is data, never a language branch; a row never edits the project's config.
tests: `test_every_entry_says_soft`, `test_absent_soft_reads_empty_with_note`, `test_actual_arg_rows`, `test_all_soft_empty_list_false`, `test_no_retry_by_source_not_by_language` (a TS file with no Playwright import: `[]`), `test_no_retry_bad_regex_empty`, `test_interruption_absent_empty`.
`DoD:` `python -m pytest ai-packages/qa-factory/scripts/tests/test_assertion_detectors.py ai-packages/qa-factory/scripts/tests/test_probe_every_check.py -q`; `python -B ai-packages/qa-factory/scripts/selftest.py --lang`. AR-1 grep pasted. `architecture: AR-1, AR-22, AR-23, AR-29`; `judgment: none altered (data rows)`.

### P1b — soft scopes of Java and C# (TR2-17; the owner's word, Q6; runs after P2)

`given:` Shared; P1, P2 as landed.
`owns:` `references/detectors.json` (`soft_scopes` [new] on csharp and java), `scripts/assertion_detectors.py` (`soft_scopes_of` [new], `ENTRY_FIELDS`), `scripts/probe_by_code.py` (`checks_of`, `run_plan`: a check inside a declared scope reads as non-stopping), `scripts/tests/test_probe_every_check.py`, `changelog.d/t-2064-p1b.md`; all under `D:/ws1/wt-fbfix\ai-packages\qa-factory\` at the node's worktree.
Required:
1. Data, per framework: a row `{ "opens": <regex of the scope's opening>, "head": <regex of a check inside, when it differs from the plain form> }`. Rows to verify in the library's docs and on a sample before writing them (t-1968 rule): AssertJ `SoftAssertions` and `assertSoftly` (`softly.assertThat`), JUnit `assertAll(() -> ...)`, TestNG `SoftAssert`, NUnit `Assert.Multiple(() => {...})`. A form in doubt has no row and its report line says so.
2. `checks_of` lists every check inside a scope with its own key and `stops: false`, by the same rule as a soft head; the plan groups them in one joint run as it does `expect.soft`. No branch on a language's name (P31): the row decides.
3. Each check gets its own marker text (the owner's word, Q4), reached through the form's message argument; a form with no message argument in the row goes by the existing door (a model or the critic) and the report names it.
`non-goals:` other frameworks; plan shape; the walk.
`edges:` a scope with no check found: as a head of an unknown form (EP-P). A nested scope: the outer one decides, a test pins it. A check after the scope closes: stopping as written. INV: a row never makes a stopping check soft outside its scope.
tests (fixture sources, parametrised by framework, a red names it): `test_scope_checks_do_not_stop`, `test_check_after_scope_stops`, `test_scope_markers_differ`, `test_nested_scope_one_group`, `test_no_scope_row_plain_plan`, `test_no_language_name_in_branch`.
`DoD:` `python -B ai-packages/qa-factory/scripts/tests/test_probe_every_check.py` and `python -B ai-packages/qa-factory/scripts/selftest.py --lang`. The stand has no Java or C# runner (not read: the builder checks and reports): the live proof is a row of the batch's table for a project on that language. `architecture: AR-1, AR-15, AR-22, AR-29`; `judgment: none altered (data rows)`.

### P2 — the list and the plan (pure)

«по рекомендации, до слова владельца»: F-P1, F-P2, F-P3.

`given:` Shared; N1's functions on the branch.
`owns:`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\probe_by_code.py` (`checks_of` [new], `run_plan` [new], `_build_parser` — `--plan`, `main` — its branch)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_every_check.py`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_one_road.py` (the guard's list)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json` (rows)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-2064-p2.md` (new)
Required:
1. `checks_of(data, spec, reader_entry, bindings, helpers) -> [{key, file, line, end_line, form, soft: bool, invertible, has_message, in_body, then: n|null, statement_sha}]`, source order. Heads of known forms inside `test_body_span` (N1), through N1's `_source_checks` (table reader) and `_python_checks` (AST reader), the two `check_on_line` already uses: no third walker. `statement_sha`: sha256 of the check's statement, whitespace folded. Plus heads on the lines of `bindings` outside the body (read through `then_assertions`' source; a range `a-b` read by `s5_precheck._ref_span`). Plus, when the body holds none, the heads of N5's hop. A setup helper's checks that no binding names are not listed, with a note counting them. `then` by line within the row's span; no hit: null.
2. `run_plan(checks) -> [{run, keys, why}]`: outside-body checks alone; in-body in source order: collect non-stopping; a stopping check after a collected group joins it as its last and closes it; a stopping check with no open group runs alone, and it does not open one. Pure.
3. `--plan --task T --instance I --test N [--json]` prints `{checks, plan, notes}`, writes nothing, runs nothing, takes no locks; exit 0. `brief_pack` reads it in P7; `probe_entries.py` reads it.
**Position invariant of 2:** a check behind a stopping check in the same run is unreachable; no group holds a stopping check before another check. P0 s2, s3 measure both sides.
`non-goals:` writing or running; a model; what a check means.
`edges:` EP-A, EP-B, EP-D, EP-O, EP-P, EP-Q; F-P1. A file that does not lex: refusal as `Source`. Binding on a line with no check: its row gives no check and a note "binding `:46` holds no check" (arm B's real case). INV: code lists, never ranks.
tests: `test_plan_three_soft_one_run`, `test_plan_soft_then_hard_joins_last`, `test_plan_hard_then_soft_two_runs` (`:122`, `:128`), `test_plan_chain_of_three_three_runs`, `test_plan_no_soft_row_one_per_check` (each language: same function, no language read), `test_helper_alone`, `test_two_heads_one_line_keys`, `test_binding_on_blank_line_note`, `test_plan_writes_nothing`, `test_list_is_arm_b_tc019` (a canned copy of `add_to_cart.spec.ts:117-139` gives 8 checks and 2 runs), `test_statement_sha_ignores_whitespace`.
`DoD:` `python -m pytest ai-packages/qa-factory/scripts/tests/test_probe_every_check.py ai-packages/qa-factory/scripts/tests/test_probe_one_road.py ai-packages/qa-factory/scripts/tests/test_judgment_census.py -q`; `python -B ai-packages/qa-factory/scripts/selftest.py --lang`. AR-13 grep pasted. `architecture: AR-1, AR-2, AR-13, AR-19, AR-22, AR-23, AR-29`; `judgment: checks_of shape data; run_plan shape data`.

### P3 — the model on every reader, with our marker

«по рекомендации, до слова владельца»: F-P8, F-P9, Q1 (the `product` kind), Q3 (the `not_here` kind).

`given:` Shared; P0's table (s5, s6); N2's Python row.
`owns:`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\probe_by_code.py` (`load_models` [new; `load_model` stays for the alternative until P5, its guards shared], `_edit_shape` [new], `_model_region` [new], `plan_model` [new], `_with_marker` — the un-inverted statement, `fires_as` None skips its guard, `marker_token` — takes the check key, `_assert_with_marker` [new, Python's un-inverted `assert`], `_assert_that_with_marker` [new], `_models_refusal` [new], `MODEL_FILE_MAX`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_every_check.py`, `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_marker.py`, `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_one_road.py` (the guard's list)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\probe_entries.py` (new)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json` (rows)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\refusal-registry` row, wherever `refusal_registry.py --check` names it (A24; file not read here)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-2064-p3.md` (new)
Required:

1. **Shape.** `work/probe-models/<dispatch id>.json` (one per window; `--model` overrides the path), under `load_model`'s existing guards (`resolve`, size, UTF-8):
```json
{"models": [
{"check": "tests/api/cart/cart.spec.ts:112", "supposes": "the refusal answers 500", "actual": "500"},
{"check": "tests/x.spec.ts:40", "supposes": "the stored line is lost", "find": "const lines = await guest.cart();", "replace": "const lines = [];"},
{"check": "tests/x.spec.ts:47", "invert": "the element is fixed by the page; I know no other value"},
{"check": "tests/x.spec.ts:84", "instance": "P-guest", "not_here": "this instance keeps the guest, the branch is not taken"},
{"check": "tests/x.spec.ts:90", "product": "work/sensitivity-receipts/<file>.json"}
]}
```
Exactly one kind per entry; `instance` optional except on `not_here`; `alternative` optional (P5); `supposes` required on a value kind, 1-300 characters, presence only. A file with no `models` key: refusal naming this shape. `MODEL_FILE_MAX` (16384 today) becomes 65536 (a window's entries at about 90-150 bytes each, estimate; named). Two entries with the same `check`, `instance`, `alternative`: refusal naming both.

2. **The edit.** **`actual`:** replaces the check's actual argument by `_call_arguments` and `AD.actual_arg_of`; a form with no row: refusal, door `find` or `invert` where they open. **`find`:** exactly once between the start of the body **holding the check** (the helper's own body when the check stands in a helper: a read in the test cannot be modelled from there: `actual` or `invert`) and the check's statement, in code on the skeleton's terms; never in the statement. Both kinds: same count of line breaks in removed and added; text not equal after whitespace strip. **`_edit_shape(base_text, removed, added, lexer)` (B1):** `lexical_shape(added)` and `lexical_shape(removed)` each have every bracket balanced and end in `code`; `lexical_shape(new_text) == ({char: base[char] - removed[char] + added[char]}, base_state)`: the arithmetic `_with_marker` uses at :1296-1298. So `expect(r.status(), m)` with `actual: "500"` holds (removed one `(`/`)` pair, added none), and `catalog.cartBadge` with `page.locator('body')` holds. A half-bracket `find` (`foo(`) is refused: its removed text is not balanced. AST reader: `ast.parse` of the new text for the same spans, and no `lexical_shape`.

3. `_model_region` errs to refusal. **Position invariant:** the matcher, the expected value, `.not` and the message of any check are never edited by a model: an inversion is the only edit of a matcher, and only by `invert`.

4. **Marker.** After the value edit, on the check as written, one token per check: `marker_token(iid, sha, started_at, key)`, still 12 hex. **`started_at` is per run, not per walk**, so an alone rerun does not share the joint run's token. Table reader: `_with_marker`. **AST reader: `_assert_with_marker(rep, token)`, `_assert_that_with_marker(rep, token)`**, by N2's Python row, the statement otherwise as written; an `assert` that already has a message: N2's rule for it (reads). `invert` entries: `plan_mutation` / `plan_detector_mutation` as they stand, with `at`. `message_form` "" → the check has no marker, the detail says it, the row goes to the role.

5. `plan_model(data, spec, entries, checks) -> (bytes, details[])` for one plan row: one file. **Edits apply bottom-up** (highest offset first), so earlier offsets hold. Regions must not overlap; overlap: refusal naming both. One `find` may break several checks; each is read by its own marker, and `supposes` is then not what failed for the second (named residual, EP-H's facts). `not_here` and `product` entries make no edit: `plan_model` never sees them (P4a filters).

6. **Refusal per F-P8 (`_models_refusal`).** Names each check with its line and prints **only the doors that open for that check**: `actual` if `actual_arg_of` has a row; `find` if at least one line of the body stands before the statement; `invert` if `invertible`; always `not_here`; `product` if the form's language has a product probe door (t-2045 E-E, E-F); and the exit: "if none fits, report `unverified` for this check". Empty `models`, absent file: the same refusal.

**Reuse:** `_with_marker`, error direction per §11.0. `_call_arguments` from "where the message goes" to "where the value goes": a call it cannot split gives a refusal, never a guess.
`non-goals:` running; judging; `--alternatives` report; the alternative's own `load_model`.
`edges:` EP-L, EP-N, EP-O, EP-R, EP-T; F-P8, F-P9. An `actual` in a form with `has_message: false`: runs, no marker, role. CRLF, BOM kept. Unknown `check` key: refusal listing the plan's keys. INV: the plan keeps line numbers; what is mutated is what the record says.
tests: per language: `test_actual_replaces_argument_only`, `test_actual_with_brackets_replaced_by_literal`, `test_actual_literal_replaced_by_brackets`, `test_find_bracket_change`, `test_half_bracket_find_refused`, `test_added_unbalanced_refused`, `test_find_before_statement`, `test_find_in_statement_refused`, `test_find_in_helper_bounded_by_helper`, `test_expected_and_matcher_never_edited` (negative: a planted `actual` spanning a matcher), `test_invert_needs_reason`, `test_not_here_needs_instance_and_why`, `test_no_model_refused_names_checks` (door opens by running the second call), `test_refusal_prints_only_open_doors` (an `invert: null` form: no `invert` in the text), `test_marker_on_uninverted_statement`, `test_python_assert_marker_uninverted`, `test_two_tokens_no_prefix`, `test_token_differs_per_run`, `test_overlap_refused`, `test_edits_apply_bottom_up`, `test_two_entries_same_key_refused`, `test_old_shape_refused_names_new`, `test_model_no_message_form_no_marker`, `test_line_count_kept`; `test_probe_marker.py`: `test_fires_none_skips_guard`.
`DoD:` `python -m pytest ai-packages/qa-factory/scripts/tests/test_probe_every_check.py ai-packages/qa-factory/scripts/tests/test_probe_marker.py ai-packages/qa-factory/scripts/tests/test_probe_one_road.py ai-packages/qa-factory/scripts/tests/test_judgment_census.py -q`; `python -B ai-packages/qa-factory/scripts/selftest.py --lang`; `python -B ai-packages/qa-factory/scripts/refusal_registry.py --check`. `architecture: AR-1, AR-2, AR-7, AR-9, AR-15, AR-22, AR-23, AR-29`; `judgment: load_models shape data; _edit_shape shape data; _model_region shape data`.

### P4a — the walk, the joint judge, per-check records (a function, not yet on `_probe`)

«по рекомендации, до слова владельца»: F-P4, F-P10, F-P11. Starts after P0b's report is read.

`given:` Shared; P0's and P0b's tables.
`owns:`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\probe_by_code.py` (`_walk_plan` [new]; `_judge_joint_rows` [new]; `_problem_texts` [new]; `_cut_by_runner` [new]; `_row_by_marker` — takes the token, reads `_problem_texts`; `_earlier_check_at` [new]; `author_green_of` [new]; `build_request` — appends `AD.no_retry_flags`; `_check_record` [new])
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\proof_level.py` (`probe_record_path` — the `checks/` directory, `already_probed` — key and the entry's sha)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\design\state-exits.md` (`not_reached`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_every_check.py`, `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_one_road.py`, `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_target_fact.py`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json` (rows)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-2064-p4a.md` (new)
Required:

1. **`_walk_plan(ctx, plan, entries, locks, timeout) -> outcomes`.** For each plan row, in order: drop `not_here` and `product` keys (P4b reads them); skip keys proved on these bytes with the same entry sha (`_same_target` of N1b, plus the sha); `begin_copy`, write `plan_model`'s bytes, `_run_and_judge`, restore verified, `_check_record` per key, then the next. A failed restore ends the walk. The no-retry flags go through `build_request`; a run with flags that gives no rows or `error`: that row once more without them, a note, none for the rest of the walk (F-P10). Whether a changed `command.argv` passes `validate_request` and what `input_fingerprint` covers: **not read here**, the builder reads `execution_request.py:114`, :1818 first; a conflict is a question, not a workaround. Time: `--timeout` shared by the walk; what is left at the end of a row is checked before the next (EP-J).

2. **`_judge_joint_rows(rows, tokens, group, plan, details, facts) -> {key: outcome}, move`, in this order; position invariant: a token read outranks everything but step C, and only a passed row can settle a not-fire without another run.** It is a loop over `_row_by_marker(row, token, ...)`, so one judge stays (EP-A).
   - **A. Status.** Passed: every key `no_failure` or, on `find`, `incomplete`, `cause: judgment` (EP-H). `error` or no row: t-2045's rules for the whole group. Failed: go on.
   - **B. Read.** `_problem_texts(row)`: message and text of **every** problem of kind `failure` or `error` (`failure_problem` :1841 returns the first only; P0's Playwright body is one, other reporters may hold several). A key is read when its exact token stands there.
   - **C. Demote (EP-V).** If any key is absent, or `_cut_by_runner(texts, entry)`: the last read key in source order is demoted. Group of 2 or more: into the alone reruns. Run of one: `_row_unsettled`, `interrupted: true`.
   - **D. Read keys that stand.** `invert` kind: proved. Value kind: proved only with `author_green_of(...) is True`; else `_row_unsettled` with `author_green` a fact (F-P4).
   - **E. The stop (EP-G).** Absent keys, and `_earlier_check_at(location, plan, row, edits)` names a check before this row's first key that this run did not edit, with no edit of this run standing before it: absent keys and all later rows `not_reached`, `plan_remaining`, move `stop`. The location is `site["location"]`'s reading: a fact that orders the walk, never a proof.
   - **F. Otherwise.** Group of 2 or more: each absent or demoted key is rerun alone, once, in the same walk, others untouched; its outcome by steps A-D with no further rerun. **Run of one, token absent: `_row_unsettled`; no rerun; the walk goes on**, whether the cause is a helper's throw, the check's own argument or no location.

3. **`author_green_of(task_root, iid, identity, fingerprint) -> True|False|None`.** `author_binding` first, read as `_run_alternative` reads it (`None if bound is None else bound.get("status") == "passed"`, :3893); then the latest run block row of `iid` whose `source_fingerprint.test_content_sha` equals `original_input_hash`'s value over the author's bytes. Reuse: `author_binding` from a fact to a proof's condition: errs to `None`. Adversarial: an empty sha; a row of another instance; a reparse block; a helper changed since (fingerprint differs); a block with `status` other than `passed`; a retried green.

4. **Records.** `_check_record`: `work/probes/checks/<iid>--L<line>.json`, `-2` for EP-O: `probe_record_path(task_root, iid, target_line=)` now returns that path (S3): `probe_debt._scan` (:300-316) and `handoff_check.py:419` glob `work/probes/*.json` non-recursively, the convention of `alternative/` (`proof_level.py:990`). `already_probed` reads there. No receipt from a per-check record. Written after each row, so a killed walk keeps what it proved.

`non-goals:` `_probe`'s wiring, the aggregate, the receipt, `--judge` (P4b); replay (P4c); text (P7); the seam.
`edges:` EP-E, EP-F, EP-G, EP-H, EP-Q, EP-V. INV: the bytes back after every row or the copy stays; a joint row settled by nothing leaves `incomplete`, not a pass; a retried run's doubled text reads each token once.
tests, on a stub runner, each language where it differs: `test_three_soft_one_run_three_proved`, `test_one_absent_named_and_rerun_alone`, `test_absent_alone_passes_is_no_failure`, `test_absent_alone_marker_proves_with_note`, `test_row_passed_no_rerun`, `test_chain_three_runs_earlier_untouched` (assert the bytes each run saw), `test_chain_red_link_stops_walk` (a, b, c; b's run fails on `a`'s span: b and c `not_reached`, `plan_remaining`, no third run), `test_chain_helper_throw_walk_goes_on`, `test_chain_own_argument_throw_walk_goes_on` (b unsettled, c proved), `test_chain_no_location_walk_goes_on`, `test_find_breaks_earlier_check_goes_on`, `test_run_of_one_absent_is_critic_no_rerun`, `test_cut_last_token_rerun_when_one_absent` (P0 s4's body: `s4n5` demoted, `s4n6`-`s4n8` alone), `test_cut_text_all_present_demotes_last`, `test_cut_run_of_one_goes_to_critic`, `test_cut_never_proves`, `test_all_problems_read` (two `failure` problems, the token in the second), `test_marker_in_system_out_not_read`, `test_only_marker_proves`, `test_model_red_author_goes_to_critic`, `test_author_green_by_fingerprint_on_ts`, `test_author_unknown_critic`, `test_invert_needs_no_green`, `test_find_model_pass_is_judgment`, `test_actual_model_pass_is_no_failure`, `test_rerun_new_token`, `test_mutation_restored_after_each_row`, `test_failed_restore_ends_walk`, `test_no_retry_flag_reaches_request`, `test_no_retry_dropped_when_no_rows`, `test_param_rows_every_row`, `test_helper_called_by_two_two_records`, `test_check_records_under_checks_dir`, `test_debt_scan_ignores_checks_dir`.
`DoD:` `python -m pytest ai-packages/qa-factory/scripts/tests/test_probe_every_check.py ai-packages/qa-factory/scripts/tests/test_probe_one_road.py ai-packages/qa-factory/scripts/tests/test_probe_target_fact.py ai-packages/qa-factory/scripts/tests/test_state_exits.py ai-packages/qa-factory/scripts/tests/test_judgment_census.py -q`; `python -B ai-packages/qa-factory/scripts/selftest.py --lang`. AR-13 grep (one marker reader) pasted. CI: `test_probe_debt.py`. `architecture: AR-1, AR-13, AR-14, AR-22, AR-25, AR-28, AR-29`; `judgment: _judge_joint_rows xref data; _cut_by_runner word-list data (only demotes); author_green_of xref data`.

### P4b — the aggregate, the receipt, `--judge`, and the flip of `_probe`

«по рекомендации, до слова владельца»: F-P8, Q3. **This node flips every no-`--at` call: the pin table is its size.** The walk reaches `_probe` only here, together with the aggregate, so no state publishes on one check through the old `_finish_record`.

`given:` Shared; P4a's code; `acceptance.py:1050-1119`; `window_record.py:600-648`.
`owns:`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\probe_by_code.py` (`_probe` — every branch but the alternative's; `_no_role` [new]; `_dispatch_stage` [new]; `_entries_for` [new]; `_aggregate_record` [new]; `_finish_record`; `attach_receipt`; `_receipt_core` — `checks`; `judge_record`, `_judged_record`, `_judge_cli` — `--check`; `_build_parser` — `--check`; `_refuse_flags` — the door text of `--mutation`; `_target_of` — the `assertion_id` and `first` branches removed, per §11.3)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\proof_level.py` (`probe_could_not_run` — `plan_unfinished`; `probe_record_state` — `plan_unfinished`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\design\state-exits.md` (`plan_unfinished`, `not_owed`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_every_check.py`, `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_marker_judgment.py`, `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_one_road.py`, `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_target_fact.py`, `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_gap_door.py`, `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_not_proved.py`, `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_container_answer.py`, `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_handoff_init_author.py`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_by_code.py`, `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_by_code_languages.py`, `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_by_code_copy.py`, `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_binding.py` (CI)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json` (rows)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-2064-p4b.md` (new)
Required:

1. **`_aggregate_record` writes `work/probes/<iid>.json`, after every row and at the end; the one writer.** Every key its readers need (S2):
   - `failure_kind: "assertion"` (`acceptance.py:1081`); `mutation: "invert"` (a compat spelling: `_replay_plan` :228 refuses others; the truth of what was edited is `checks[]`); `target`; `restore` (`verified` only when every row's was); `test_node`; `mutation_detail` with no `at` (`proof_level.py:1686` returns None otherwise); `test_file_sha256`; `record`; `words` (`s6_reprove` prints it: "x of n checks proved; left: keys"); every key `_receipt_core` and `WINDOW_PROBE_FIELDS` (:2498) read.
   - `checks: [{key, then, probe_kind, supposes|reason, entry, statement_sha, verdict, proved_by, run, read_in_joint}]` (`entry`: the whole entry as written: the replay's producer, AR-22), `plan_runs`, `plan_remaining`, `plan_unfinished`.
   - `verdict`: `intended_failure` only under EP-K; otherwise by `_SURVIVOR_ORDER` (`no_failure`, `wrong_location`, `not_executed`, :2718), else `incomplete`, `cause` as the survivor's; a mix with a tooling row: tooling, as today.
   - `expected_location`, `actual_location`: the first proved check's, equal; `expected_reason`, `actual_reason`: one fixed aggregate line naming the count, equal. **So `acceptance.py:1078-1080` is vacuous for a walk: it checks shape, and `_aggregate_record` is the check.** Stated in the function's docstring, no new gate. `test_one_check_same_record_shape`: a plan of one keeps today's location and reason.
   - The answer to the caller is the aggregate, `record` under `work/probes/`, so `s6_reprove`'s path pattern (`story_run.py:12360`) holds.

2. **`_probe`, no `--at`.** Loads list and plan, `_entries_for(ctx, checks)`, per check in this order: (1) an entry of this window's model file, by key; (2) an entry stored in the instance's aggregate, joined by `statement_sha` (EP-U); (3) `_no_role(ctx)`: inversion, `reason: "no role at this call"`, written by code; (4) otherwise owed. **Anything owed: `_models_refusal` before a byte is written.** `_no_role(ctx)`: `ctx.stage == "S6"` (`--s6-close`) or `_dispatch_stage(task_root, dispatch) == "S6"`: `_dispatch_context` returns `stage ""` on `--dispatch` (:3188), so the stage is read from the same dispatch row `_judge_dispatch_why` reads. **Unknown stage: a role is assumed: the refusal, never an inversion** (error direction; in S6 it is one digest line, S6 still closes). `--mutation invert` selects nothing. An `invert: null` check under no role: EP-R.

3. **`--at` and `--oracle` are plans of the selected rows (B3, EP-S).** `--at <line>` or `<file>:<line>` or `<line>#2`: one row through `_entries_for`, the same refusal and door with no entry; the check always gets its per-check record; then `_aggregate_record`; **a receipt only when complete**. The line must be a check (t-2045 E-A); a helper's line outside the plan: added to the plan (it is a real check, N1's door), and owed from then on. `_refuse_flags`' door names the `invert` entry, not `--mutation invert` (FR-2).

4. **Receipt** from the aggregate only (EP-K), with `checks`. Same bytes, same check, same entry sha, proved: skipped; all proved and the aggregate standing: `already_probed` as today.

5. **`--judge <instance> --check <key>`.** `_judged_record` reads `checks/`; the door names `--check`; with one unsettled check `--check` may be omitted. `_judge_input`'s facts per check. Then the aggregate is rebuilt, one writer. `--judge` still refuses `no_failure` (the door there: `not_here`, or a `test_defect` finding).

6. **`not_here`, `product`.** `not_here`: the check reads `verdict: not_owed`, `reason`; `product`: `_product_entry_holds` (EP-W) or a refusal naming what failed. An entry never changes a check's standing on the record's other keys.

7. **Wall:** EP-J. `plan_unfinished` is `verdict: incomplete`, `cause: tooling`, `plan_unfinished: true`; `probe_record_state` returns state `plan_unfinished`; `probe_could_not_run` False for it.

`non-goals:` window and acceptance readers (P6); text (P7); replay (P4c); `acceptance.validate_window`.
`edges:` EP-A, EP-I, EP-J, EP-K, EP-O, EP-R, EP-S, EP-T, EP-U, EP-W. S6 close with an inversion plan and no critic: t-2045 E-L. INV: a receipt of other bytes never counts; **`--at` never publishes one check of several**; a role cannot type its way out of a model; every refusal's door opens.
tests: `test_no_model_refused_before_a_byte`, `test_mutation_invert_flag_is_no_bypass` (a critic's dispatch, the flag, no entry: refused), `test_at_no_entry_refused`, `test_at_never_publishes_partial`, `test_at_fills_the_aggregate`, `test_at_second_on_line`, `test_oracle_selects_rows`, `test_s6_dispatch_is_no_role` (a running S6 dispatch, no model: inverts, reason written), `test_s6_close_is_no_role`, `test_unknown_stage_refuses`, `test_stored_entry_before_inversion`, `test_all_checks_or_no_receipt`, `test_not_here_counts_not_as_proof`, `test_all_not_here_no_receipt`, `test_not_here_door_on_no_failure`, `test_invert_null_under_no_role_others_walk`, `test_wall_leaves_plan_unfinished_then_continues`, `test_killed_walk_keeps_rows` (the process killed between rows: per-check records and the aggregate stand, the copy restored by the next call), `test_plan_unfinished_not_a_persons_door`, `test_repeat_skips_proved_runs_new_model`, `test_judge_by_check_rebuilds_aggregate`, `test_judge_no_failure_refused_door`, `test_one_check_same_record_shape`, `test_aggregate_feeds_every_reader` (walks `_receipt_core`, `WINDOW_PROBE_FIELDS`, `_replay`, `_replay_plan`, `s6_reprove`'s pattern), `test_printed_door_runs_second_call` (kept, with the entry).
`DoD:` `python -m pytest ai-packages/qa-factory/scripts/tests/test_probe_every_check.py ai-packages/qa-factory/scripts/tests/test_probe_marker_judgment.py ai-packages/qa-factory/scripts/tests/test_probe_one_road.py ai-packages/qa-factory/scripts/tests/test_probe_target_fact.py ai-packages/qa-factory/scripts/tests/test_probe_gap_door.py ai-packages/qa-factory/scripts/tests/test_probe_not_proved.py ai-packages/qa-factory/scripts/tests/test_state_exits.py ai-packages/qa-factory/scripts/tests/test_judgment_census.py -q`; `python -B ai-packages/qa-factory/scripts/selftest.py --lang`; `python -B ai-packages/qa-factory/scripts/refusal_registry.py --check`. CI: `test_probe_by_code.py`, `test_probe_by_code_languages.py`, `test_probe_by_code_copy.py`, `test_probe_binding.py`. `architecture: AR-7, AR-9, AR-12, AR-14, AR-22, AR-25, AR-28, AR-29`; `judgment: _no_role xref data; _aggregate_record xref data; _product_entry_holds xref data; judge_record xref judgment unchanged`.

### P4c — replay: settle and S6 (B2)

«по рекомендации, до слова владельца»: F-P8.

`given:` Shared; P4b's aggregate; `probe_debt.py:160-344`, :606-640, :893-925; `proof_level.py:1663-1692`; `story_run.py:12319-12378`.
`owns:`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\probe_debt.py` (`_replay_plan`, `_item`, `_classify`, `settle` — the `plan_unfinished` outcome; `_probe_args` unchanged, named)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\proof_level.py` (`_replay`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\probe_by_code.py` (`replay_owed` [new, pure])
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_every_check.py`, `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_one_road.py`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_debt.py`, `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_story_run_s6.py` (CI; `story_run.s6_reprove` itself is not edited: its argv, `record` pattern and digest lines are pinned)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-2064-p4c.md` (new)
Required:
1. `replay_owed(record, data, spec, reader_entry, bindings) -> [keys]`: the plan's keys on the current bytes with no stored entry joined (EP-U). Pure. A record with no `checks`: every key.
2. **S5 settle.** `_item`: `_replay_plan` as today for node and oracle; then `replay_owed`. Non-empty: `LEAVE_TO_CRITIC`, why "model owed: the critic writes the entry for <keys> (the record proved <one check | these>)", **no run**. Empty: `REPROBE` with no `--at`; `_probe` joins the stored entries itself (P4b item 2), so no flag says "replay". An old record with `mutation: invert` and no `checks` is owed: it proved one check of several, and no reason was written. A stored `invert` replays as `invert` with its reason.
3. **Settle's budget.** Under 90 s the probe gets `--timeout <remaining>` (:908). Reasoned, not run: mean 72 s a run, so about one row per settle; a row cut by that timeout restores and ends the row `not_executed` (as the docstring at :900-902 says); the walk ends `plan_unfinished`. `_classify`: `plan_unfinished: true` → `{"result": "plan_unfinished", "settled": False, "stop": False, words: plan_remaining}`, so `not_executed`'s `stop: True` does not fire and the next settle or the critic continues. It is not in `STABLE_LEFT`.
4. **S6.** `s6_reprove` calls as today (`--mutation invert --json`, `--dispatch` or `--s6-close`); `_probe` sees no role, walks stored entries or inversions; the answer is the aggregate. `_replay` reads the aggregate as it stands (`mutation`, `test_node`, `mutation_detail` with no `at`), so a new record replays and an old `--at` one still returns None. A verdict not `intended_failure`: one digest line, `words`, S6 closes (t-2045 E-L). Nothing is added to the S6 code.
`non-goals:` the critic's text; `s6_reprove`'s wording; a budget for S6's wall (not read: `self.py`'s timeout; a walk may be cut there: report line).
`edges:` EP-I, EP-J, EP-U; a stored `find` that no longer stands: owed (S5), inversion with a note (S6). INV: a replay never invents an edit under S5; a `--mutation` value is never read as "no role"; the stale debt's item is never dropped: it stays with the critic by name.
tests: `test_settle_no_stored_stays_with_critic_no_run`, `test_settle_old_record_owed`, `test_settle_stored_replays_no_flag`, `test_settle_stored_invert_keeps_reason`, `test_settle_moved_key_joined_by_statement`, `test_settle_changed_expected_owed`, `test_classify_plan_unfinished_continues`, `test_settle_budget_cut_keeps_rows`, `test_replay_reads_aggregate`, `test_replay_old_at_none`, `test_s6_replay_stored_then_inversion` (fast, on `_probe`); CI in `test_story_run_s6.py`: `s6_reprove`'s argv unchanged, the aggregate's `record` matched, `incomplete` + `judgment` one line, S6 closes.
`DoD:` `python -m pytest ai-packages/qa-factory/scripts/tests/test_probe_every_check.py ai-packages/qa-factory/scripts/tests/test_probe_one_road.py -q`; `python -B ai-packages/qa-factory/scripts/selftest.py --lang`. CI: `test_probe_debt.py`, `test_story_run_s6.py`. AR-19 twins named in the report. `architecture: AR-14, AR-19, AR-22, AR-28, AR-29`; `judgment: replay_owed shape data`.

### P5 — the alternative joins the road (F8 flips)

«по рекомендации, до слова владельца»: F8 of t-2045.

`given:` Shared; `probe_by_code.py:3293-3900`.
`owns:`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\probe_by_code.py` (`_refuse_flags` — the `--model` branch; `_probe` — the alternative's branch; `_build_parser` — `--mutation` loses `alternative`, `--alternative` stays; `load_model` [removed]; `_probe_alternative`, `_run_alternative`, `_alternative_run_record`, `plan_alternative`, `judge_alternative`, `_judge_alternative_row`, `_judge_param_rows`, `observe`, `_reach_of`, `model_reach`, `_Identities`, `model_changes_value`, `assert_spans`, `_walk_statements`, `_model_target`: removed or reduced; `_judge_run` — its `judge_row`; `report_rows` — the non-raw branch if no reader stays (grep, a report line); `_alternative_gap_record` — kept for `gap`; `alternatives_report`, `_alt_row`, `_judge_alt_row`, `alternative_now` — read the road's records)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_one_road.py` (`ROAD_EXCEPTIONS`: F8 lines and the `_judge_run` line go), `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_every_check.py`, `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_by_code_alternative.py` (CI)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json` (the `judge_alternative` row removed)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-2064-p5.md` (new)
Required:
1. **Call form:** `probe_by_code.py --task T --dispatch D --test N --instance I --alternative <case>:ALT-n [--model <file>]`. `--mutation alternative` is **removed** here (S11: a story keeps its plugin generation, B-014, and the batch has no release between): argparse keeps the word among `choices` as N7 does, and `_refuse_flags` refuses with the door `--alternative`.
2. **Entries.** A declared reading B is an entry with `alternative: "<case>:ALT-n"` on checks of that Then. **A plain entry and an alternative entry may stand on one check: they never meet.** A plain walk reads entries with no `alternative`; `--alternative T` reads only entries of `T`, and its plan is those keys, which must lie on the plan (unknown: refusal); a check of that Then with no entry of `T`: the report's `proven` stays false, no refusal. Two entries of one `T` on one key: P3's refusal.
3. It runs on the road, on every language, with marker and author green (`author_green_of`). `--alternatives` keeps its report and tokens; `proven` reads: all that Then's checks proved under the entry. Record stays `work/probes/alternative/<IID>--<CASE>--<ALT>.json`, never a live receipt.
4. **`gap`:** `{"alternative": "<case>:ALT-n", "gap": "<why B cannot be modelled>"}`, no `check`, presence only: `_alternative_gap_record`, as a report row.
5. The old model shape (one object with `find`, `replace`, `gap`, `function`): P3's refusal naming the new shape; old alternative RECORDS read as today.
**Reuse:** `model_changes_value` gives way to text equality, losing `x + 0` on Python only: a pass there reads `no_failure` beside the model and the critic sees it. Direction: not toward proof. `_Identities` was a language exception.
`non-goals:` the case's `alternatives` key; `red_sandbox`.
`edges:` EP-H replaces `judge_alternative`'s table. INV: an alternative record is never a live receipt; a reading never proves on a red author; a plain walk is never fed a reading's edit.
tests: `test_alternative_runs_on_ts`, `test_alternative_python_keeps_token_and_path`, `test_alternatives_report_proven_all_checks`, `test_plain_and_alternative_entry_never_meet`, `test_alternative_flag_spelling_refused_with_door`, `test_old_alt_record_reads`, `test_gap_entry_writes_gap_row`, `test_no_language_question_on_the_road` (F8 exceptions removed).
`DoD:` `python -m pytest ai-packages/qa-factory/scripts/tests/test_probe_every_check.py ai-packages/qa-factory/scripts/tests/test_probe_one_road.py ai-packages/qa-factory/scripts/tests/test_judgment_census.py -q`; `python -B ai-packages/qa-factory/scripts/selftest.py --lang`. CI: `test_probe_by_code_alternative.py`. AR-15 grep pasted. `architecture: AR-15, AR-20, AR-22, AR-29`; `judgment: judge_alternative removed, count shrinks`.

### P6 — the readers of the aggregate, and the product receipt

«по рекомендации, до слова владельца»: Q1, Q3.

`given:` Shared; `red_sandbox.py:700-862`; `proof_level.py:1375-1510`; `window_record.py:600-648`.
`owns:`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\window_record.py` (`_probe_from_receipt` — `measured` carries `checks`, a `one_check` receipt; `_unknown_target_notes`; `probe_gap_block` — names the check keys)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\proof_level.py` (`_evaluate` — the `one_check` line; `probe_judgment_cases` if the keys change)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\red_sandbox.py` (`write_sensitivity_receipts` — `scope`, `checks`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_every_check.py`, `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_not_proved.py`, `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_proof_level.py`, `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_red_sandbox_probe.py`, `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_red_sandbox_reports.py`, `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_window_record.py` (CI)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-2064-p6.md` (new)
Required:
1. `acceptance.validate_window` is NOT edited: it reads the aggregate as it stands (test proves it); a partial aggregate gives `sensitivity:` as any unproved one. The window's gap text names the unproved keys; `not_owed` keys listed with their reason for the tier above. `receipt_off_target` per EP-I.
2. **`write_sensitivity_receipts`** (:790): `proof["scope"]`: `"whole_unlisted"` when `AD` has no reader for the test file's suffix, else `"one_check"`; `proof["checks"]`: `[{"key": <file>:<line> of `assertion_location`, "probe_kind": "product"}]`, `[]` when unread. Inside `receipt_hash`. `verify` is unchanged. Whether `C.sensitivity_proof_issues` refuses an unknown key: **not read here**, the builder reads it first; a conflict is a question.
3. **`_evaluate`:** `scope == "one_check"`: level None, one issue: "a product receipt proves the one check it names; the critic names it with a `product` entry, and the other checks of this test stay owed". So `reached`, `already_probed`'s receipt path and `check_delivery` follow by themselves (`reached` is their one reader; `already_probed` :1267 reads its level).
4. **`_probe_from_receipt`:** a `one_check` receipt returns a block with `verdict: "partial_product"` and the key, so `acceptance.py:1075` gives `sensitivity:` by its own line.
5. A receipt with no `scope` and `probe_tool: red_sandbox.py`: old, reads as today (EP-I).
`non-goals:` new gates; the seam's wording; `red_sandbox.verify`; the product probe's run.
`edges:` EP-I, EP-K, EP-T, EP-W. The owner's Q1 answered otherwise: items 3-4 fall, nothing else. INV: approved never on one of several; approved never by a library's wording with no role; a test whose language the factory cannot read keeps its only door.
tests: `test_partial_aggregate_is_sensitivity_gap`, `test_full_aggregate_passes_validate_window`, `test_old_receipt_info_line`, `test_id_on_blank_line_unknown_not_off_target`, `test_id_outside_body_off_target`, `test_person_after_critic_by_check`, `test_not_owed_listed_in_window`, `test_product_receipt_has_scope_and_checks`, `test_one_check_product_is_no_level`, `test_one_check_product_is_sensitivity_gap`, `test_old_product_receipt_stands`, `test_no_entry_language_product_stands_with_note`, `test_product_entry_counts_its_key_only` (8 checks, one `product` entry, 7 owed).
`DoD:` `python -m pytest ai-packages/qa-factory/scripts/tests/test_probe_every_check.py ai-packages/qa-factory/scripts/tests/test_probe_not_proved.py ai-packages/qa-factory/scripts/tests/test_proof_level.py ai-packages/qa-factory/scripts/tests/test_red_sandbox_probe.py ai-packages/qa-factory/scripts/tests/test_red_sandbox_reports.py -q` (a file of these found in `scripts/slow_tests.json` is not run: named CI); `python -B ai-packages/qa-factory/scripts/selftest.py --lang`. CI: `test_window_record.py`, `test_probe_gap_word.py`. `architecture: AR-13, AR-15, AR-19, AR-22, AR-23, AR-25, AR-28, AR-29`; `judgment: _evaluate xref data; _probe_from_receipt xref data`.

### P7 — what the roles read (before N6)

«по рекомендации, до слова владельца»: F-P3, Q1, Q2, Q3, Q6.

`given:` Shared; the N6 boundary in §11.3.
`owns:`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\agents\qa-automator.md` (:58, :68, Techniques)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\agents\qa-code-critic.md` (:23, :45, :47-:49, :51, :63, :71-:72, Techniques)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\skills\qa-story\phases\s5.md` (:122, :125, :199-:208)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\code-review-rubric.md` (the row for soft and stopping checks)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\ahead-cards.json` (the automator's and critic's cards)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\brief_pack.py` (:224-227; the critic's card: `--plan` per instance, model file path)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_code_critic_probe_rule.py`, `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_charters_s5_s9.py`, `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_brief_pack.py` (CI), `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_story_run_s6.py` (CI, :262, :264)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-2064-p7.md` (new)
As experience, not form (P27).
- **Automator:** a check that fails must not hide the others: independent checks on a step use the framework's non-stopping form where it has one; a check that only makes sense behind another stays stopping. This replaces "move independent Thens before the red one" where a soft form exists; with no soft form that line and the `blocked_by_check` row remain.
- **Critic, what:** every check is probed; for each ask how the broken product would answer, and write that value; a value the healthy product can also give proves nothing; no idea: invert and say why; a write-up per window, not per test; on a check of a screen element the choice between a substituted element and an inversion is yours (Q2). Read the plan's stopping checks: an independent one is `mechanical`, by what you know of the framework, whatever form the factory reads; a soft one whose next read is junk behind a failure too. Only our marker proves without you; a marker on a test not green under the author: yours; a check cut by a timeout: yours; a pass under a `find` model: yours to read whether the model reached; a real check not on the plan's list: `unverified`. "A setup line proves only the setup" stays.
- **Critic, how (FR-37, every word what code accepts):** one call per instance with no `--at` walks the plan; a plan of more than 3 rows runs in the background, and you read its answer; `plan_unfinished`: the same call again; `--at` is a plan of one row and needs its entry, and `--mutation invert` is not a way past it; a check this instance does not reach: `not_here`, with why; `no_failure` is `test_defect` **unless the instance never reaches the check** (replaces the absolute at :63); `--judge … --check <key>`; `red_sandbox.py --probe` proves the one check it names, and you name it with a `product` entry; the others stay owed.
- **`s5.md`:** :125 and :199-208 say the above; "instead of the code probe for that instance" at :208 goes; a line on the background.
`non-goals:` new rules; the `cause` list; N6's texts (§11.3).
`edges:` `role_load.py` over `process_ratchet_tokens`: cut as much as added, a raise named. Sibling: critic's :35 "A Then hidden behind a red", automator's :68, `s5_precheck` `red-own-behind`: unchanged behaviour, text agrees. INV: FR-37 every path and command named is what code accepts; no text names a language in the soft rule.
tests (doc witness per rule 11: keys quoted from this DoD, committed, with a negative control): `test_charter_says_every_check`, `test_charter_says_model_then_invert`, `test_charter_says_only_marker`, `test_charter_says_background_walk`, `test_charter_says_not_here`, `test_charter_at_is_one_row`, `test_charter_product_one_check`, `test_automator_says_non_stopping`, `test_no_language_named_in_soft_rule`.
`DoD:` `python -m pytest ai-packages/qa-factory/scripts/tests/test_code_critic_probe_rule.py ai-packages/qa-factory/scripts/tests/test_charters_s5_s9.py ai-packages/qa-factory/scripts/tests/test_contract_slices.py -q`; `python -B ai-packages/qa-factory/scripts/role_load.py --role qa-code-critic --json`; `python -B ai-packages/qa-factory/scripts/role_load.py --role qa-automator --json`; `python -B ai-packages/qa-factory/scripts/contract_slices.py --check`; `python -B ai-packages/qa-factory/scripts/selftest.py --lang`. CI: `test_brief_pack.py`, `test_story_run_s6.py`. `architecture: AR-9, AR-10, AR-11, AR-12, AR-29`; `judgment: none`.

### Live proof (FR-33; the batch's table; after P7)

On a stand copy: TC_019 as in §11.8 (soft group, timeout, alone rerun); the chain at `cart.spec.ts:98-99`, and the same chain with `:98` made to fail (the walk stops); a helper called by two (`separateOwners`); a helper's throw in a chain (the walk goes on); an all-stopping test giving a `mechanical` finding and an author round; a `--check` judgment on a message-less form; an inversion with its reason; `cart_page.spec.ts:84` with `not_here` on the instance that keeps the guest; a product probe named by a `product` entry beside a walk of the others; a settle and an S6 replay on a changed file. A Python sample with one test of three `assert`s (one run per check). Report: runs, wall time and critic tokens per check from the transcript against §11.6's range. Not closed by code alone.

## §11.6 Cost: arm B's 44 probes (ESTIMATE; counts measured, products estimated)

**Measured.** Checks: `Grep` of heads with lines over `tests/api/cart/cart.spec.ts`, `tests/e2e/cart/{add_to_cart,cart_page,wishlist_move}.spec.ts` in `D:/ws1/mybooks-stand\tr-arm-b`, counted by hand per test body for the 44 records of `.../LOCAL-1/work/probes/` (a loop's title is an instance). Body heads only; helper-only setup checks are not counted.

| File | Instances | Checks | Stopping | Soft |
|---|---|---|---|---|
| `cart.spec.ts` | 20 | 62 | 62 | 0 |
| `add_to_cart.spec.ts` | 10 | 46 | 26 | 20 |
| `cart_page.spec.ts` | 8 | 33 | 15 | 18 |
| `wishlist_move.spec.ts` | 6 | 28 | 18 | 10 |
| **total** | **44** | **169** | **121** | **48** |

Runs: `testsuites time=` over the 49 `red_probe-*.junit.xml` under `.../evidence/runs` (44 records, 5 more runs): t-2076's recount: sum 3,540.84 s, mean 72.26 s, median 39.77 s, 12 over 120 s, 31 with more than one failed test. Of the stopping checks, 29 are `setup` / `step` / `precondition`, 4 read a value through an earlier check (`cart.spec :98→:99`, `:232→:233`, `wishlist :55→:56`, `:88→:89`). The classification of those 33 is mine, by reading messages and lines.

**Runs, estimate** (time = runs × mean 72 s; in brackets × median 40 s; alone reruns excluded, about 2-3 per TC_019-sized test):

| Scenario | Runs | Time, estimate | Against today |
|---|---|---|---|
| Today (one per test) | 49 | 59 min, measured | |
| Every check, tests as written: 121 + 14 groups (slightly over: EP-B lets a stop join a group) | 135 | 2.7 h (1.5 h) | x2.8 |
| Every check, after the automator writes independents soft: 33 + 44 groups | 77 | 1.5 h (51 min) | x1.6 |
| F-P1 B, Then-bound only, as written: 92 + 14 | 106 | 2.1 h (1.2 h) | x2.2 |
| F-P1 B, after soft: 4 + 44 | 48 | 58 min (32 min) | x1 |
| F-P11 B on top of any row | about +44 | +53 min (+29 min) | |

Not modelled, each lowering: F-P6 (narrow run), F-P7 with F-P10 (no double run of a red; P0 s7 shows the double text; the mean holds many retried reds). Raising: each failing web-first check waits `expect.timeout` 5 s (`playwright.config.ts:43`), 68 of the 169 checks are web-first; a group of 6 such reaches `timeout: 30_000` (`:27`), and each such group pays at least one alone rerun under EP-V.

**Critic tokens, ESTIMATE, nothing measured.** No per-window token figure was found in the arm's files (one Grep over `work/windows`, empty, not controlled; treat as unknown); the live proof measures. Assumptions: 150 output tokens per check (about 100 to reason what the product would answer beyond what the review already read, about 50 to write the entry; less on an `actual`, more on a `find`).

| Part | Estimate |
|---|---|
| Output: 169 × 150 | ≈ 25K tokens |
| Writes: one per window, about 14, × a context of 60-100K | 0.8-1.4M cached input |
| Carried: about 1.8K of model text per window, re-read on about 25 later turns × 14 | ≈ 0.6M cached input |
| Judgments, marker-less forms: about 6 × 60-100K (`separateOwners`' template messages, if `M-TS1` refuses a template: not run) | ≈ 0.5M |
| **Base** | **≈ 25K output, 2-2.5M cached input** |
| (b) Judgments beyond those: `author_green` `None`, a `find` that passes, a model that does not separate, a not-reached check failing alone, a cut check; at 10 % of 169 (t-2076's assumption): 17 × 60-100K | 1-1.7M more |
| **Range to compare with** | **3-4.2M cached input, 25K+ output, per story of 169 checks** |

**Not in the range, each raising it:**
- (a) **Fix rounds.** Arm B's record has `instance_identity: {}` and `test_code_sha: ""`, so any byte change in a file makes every proved check of every instance in that file stale. "One author rerun per changed instance" and "same bytes skipped" then mean a re-walk of the file, and files hold 6-20 instances. Runs, not tokens, mostly; not priced. Stored entries spare the critic's writing (EP-U).
- (c) **Cache.** P25 names a 5-minute TTL on one project. A walk over it makes the next turn a rebuild, not a cached read; 3.07 runs × 72 s is 3.7 min on average, and 12 single runs already exceed 2 min. All priced as cached: a floor.

**FR-55 stated plainly:** this makes S5's critic dearer and the stage's wall time longer, in exchange for the proof the owner asked for: the test is shown to fail on a supposed wrong value at each check, not merely on an inverted one. If the live proof's figure exceeds the range's top by more than half, it returns to the owner with F-P1 B and F-P6 as the levers. The walk itself is code running with no LLM in the loop, FR-51's right direction.

## §11.7 Small choices closed by the designer

- One model file per window (`work/probe-models/<dispatch id>.json`) rather than per test: fewer turns. The old file shape is refused with the new one named, not read (S11).
- A joint group holds checks of ONE file; a check outside the test's body goes alone. One byte copy per run, `begin_copy` unchanged; costs runs only on helpers.
- Rerun alone happens inside the walk, no second call. One call per instance stays the role's whole interface (P1).
- `--plan` prints and writes nothing; the brief carries it.
- Key spelling `<file>:<line>`, `#2`; per-check `work/probes/checks/<iid>--L<line>.json`, `-2`; `plan_runs`, `plan_remaining`, `plan_unfinished`, `read_in_joint`, `probe_kind`, `statement_sha`, `not_reached`, `not_owed`, `scope`, `one_check`, `whole_unlisted`, `partial_product`, `interrupted` as names.
- `actual` and `find` as two kinds: an `actual` needs no uniqueness search (in TC_019 `catalog.cartBadge` stands three times).
- No cap on group size: the alone rerun covers a timeout; a cap is a number with no carrier.
- `fires_as` rows stay in data: read by the echo guard and a note only.
- The aggregate's `mutation` stays `invert` as a compat spelling rather than a new value in `MUTATIONS` (t-2076 S2).
- `statement_sha` as the stored entry's join (EP-U); a line number does not survive the edit that makes a record stale.
- A helper line given by `--at`, outside the plan, joins the plan from then on.
- P0's second part is its own node P0b and its own report, so the first report stays as measured.
- The critic's "s4/s4b unmeasured: joint web-first rows go alone" is replaced by EP-V for s4b: s4 is measured, and `s4n5` is the evidence. A difference from t-2076, flagged for the Lead.

## §11.8 Worked example: real MyBooks tests, arm B

`D:/ws1/mybooks-stand\tr-arm-b\tests\e2e\cart\add_to_cart.spec.ts`, lines verbatim (the title at 117 cut):

```ts
117    test(`@regression LOCAL-1_TC_019 P-${how} failed POST /api/cart: error shown, ...`, async ({ page, admin, books }) => {
122      await expect(catalog.cartBadge, 'step 1: badge empty before the add').toHaveCount(0);
123      await failCall(page, 'POST', /^\/api\/cart$/, how);
125      await catalog.clickAdd(A);
128      await expect.soft(catalog.cartBadge, 'Then 2: badge stays 0').toHaveCount(0);
129      expect.soft(await guestCart(page), 'Then 2: GET /api/cart holds no line').toEqual({});
130      await expect.soft(catalog.successToast, 'Then 1: no success message after the failed add').toHaveCount(0);
131      await expect.soft(catalog.errorToast, 'Then 1: an error text is shown').toBeVisible();
133      await expect.soft(catalog.card(A), 'Then 3: the catalog list is still shown').toBeVisible();
135      await expect.soft(catalog.addButton(A), 'Then 3: Add is enabled again').toBeEnabled();
137      await expect.soft(catalog.cartBadge, 'Then 3: Add works again, badge reads 1').toHaveText('1');
```

**`checks_of`:** 8 checks; `:122` stopping, the rest soft; `then` by binding. **`run_plan`:** run 1 `[:122]`; run 2 `[:128 ... :137]`. Two runs, per instance (`P-error500`, `P-timeout`).

**The critic's models** (excerpt of the window's file; illustrative, the values are the role's; the last line shows Q2's other choice):
```json
{"models": [
 {"check":"tests/e2e/cart/add_to_cart.spec.ts:122","supposes":"the badge shows before any add","actual":"page.locator('body')"},
 {"check":"tests/e2e/cart/add_to_cart.spec.ts:128","supposes":"the failed add bumps the badge","actual":"page.locator('body')"},
 {"check":"tests/e2e/cart/add_to_cart.spec.ts:129","supposes":"the line was stored though the POST failed","actual":"{ [A]: 1 }"},
 {"check":"tests/e2e/cart/add_to_cart.spec.ts:130","supposes":"success is said on the failed add","actual":"page.locator('body')"},
 {"check":"tests/e2e/cart/add_to_cart.spec.ts:131","supposes":"no error text appears","actual":"page.locator('#qa-none')"},
 {"check":"tests/e2e/cart/add_to_cart.spec.ts:133","supposes":"the list disappears","actual":"page.locator('#qa-none')"},
 {"check":"tests/e2e/cart/add_to_cart.spec.ts:135","supposes":"Add stays dead","actual":"page.locator('#qa-none')"},
 {"check":"tests/e2e/cart/add_to_cart.spec.ts:137","invert":"I know no realistic wrong badge here that the healthy flow cannot also show"}
]}
```
Every one of these passes `_edit_shape`: `catalog.cartBadge` → `page.locator('body')` adds a balanced pair; `await guestCart(page)` → `{ [A]: 1 }` removes one pair and adds two.

**Run 2's `:129` as written to disk** (marker on the un-inverted check, `M-TS1`): `expect.soft({ [A]: 1 }, ['qa-probe', 'c1a2…'].join('-') + ' ' + 'Then 2: GET /api/cart holds no line').toEqual({});`

**What is expected to read** (estimate; P0 s4's body is the shape): with `expect.timeout` 5 s (config `:43`), six web-first checks fail at 5 s each; with the set-up the test reaches `timeout: 30_000` (`:27`) around `:135`-`:137`. Say `:128`-`:135` are read and `:137` absent. Step C: `:135`, the last read, may have been cut: demoted. Step F: `:135` and `:137` alone: each its marker with author green: proved. Four runs on this instance, against today's one, which broke `:122` only. If `:137` stands green alone (the model not separating), `no_failure` names `:137`; the rest stay proved; no receipt; the critic reads (EP-K).

**A chain, real:** `cart.spec.ts:98-99`:
```ts
98    expect(lines.length, 'Then 3: exactly one line for A').toBe(1);
99    expect(lines[0].quantity, 'Then 3: 2 + 3').toBe(5);
```
`:99` reads through what `:98` guards: written stopping, rightly. Run a: `{"check":"…:98","supposes":"a second line is created","actual":"2"}`; the test stops at `:98`. Run b: `:98` as written and green, `{"check":"…:99","supposes":"quantity not summed","actual":"3"}`. Two runs, the owner's example in shape: the line's count and the wrong quantity are two bugs. Run a does not read `:99` and does not need to (EP-G). **If `:98` fails in run b on a stand hiccup:** the failure lies on an earlier check's span: `:99` `not_reached`, the walk stops, the same call continues. **If `lines[0]` throws in run b:** the failure is `:99`'s own: a run of one, token absent: the critic; the walk goes on.

**A `mechanical` finding, real:** `add_to_cart.spec.ts:47-49`, TC_001 in-stock (toast; badge; `GET /api/cart`): independent by my reading (the critic's to judge), three stopping checks, and a `:47` red hides `:48`-`:49`. The finding: `cause: mechanical`, «`:47-:49`: independent Thens, write `expect.soft`». After it the plan goes from 4 runs to 2 (`:43` alone, then the group). The same on `:66-:69`, where the author's comment at `:65`, «independent Thens first: a red error-toast assert below stops the test», shows he reordered for what the soft form gives directly.

**An inversion, real:** `add_to_cart.spec.ts:170` `await expect(detail.mainArea, 'Then 3: the page shows text, it is not blank').not.toHaveText(/^\s*$/);` could have a model; if the critic has no idea: `{"check":"…:170","invert":"<his reason>"}`, recorded, and the inverted form removes the `.not` (pair T1).

**A branch not taken, real:** `cart_page.spec.ts:83-85`, `if (!guestKept) { await expect.soft(notice, 'Then 1: …').toBeVisible(); }`. On the instance where `guestKept` is true: `{"check":"…:84","instance":"<that instance>","not_here":"guestKept is true on this instance, so the branch is not taken"}`. On the other instance the check is owed as any other.

## §11.9 Reported, not widened

- `then_bindings` in arm B read one line above the check for TC_001 (`:46` blank); `t-2037` counted 7 of 41 ids of this shape. TR2-1's write check still owed; `checks_of` is independent of it. Cause not chased.
- `proof_level.code_sha` empty on TS keeps every code-only-change credit (D-0017) off TS: TR2-16's; `author_green_of` goes around it, does not fix it; §11.6 (a) is its price here.
- `then_assertions` reads `file:line` only and drops a range; `_assertion_ref` writes ranges by default. P2 reads through `_ref_span`; `then_assertions` itself goes in P5 with the alternative.
- **For the Lead's pile (not done here, no carrier write of mine):** soft scopes (`SoftAssertions`, `assertAll`, `Assert.Multiple`) need a row in the batch's «Остатки» with `узел:` in TR2-16, not "TR2-16's candidate" (S4, Q6).
- The axis "one road for every language" stays TR2-15's, queued; t-2076 walked `docs/SIBLING_MAP.md` only by Grep. Twins found by it are in AR-19's row.
- `story_run.self.py`'s timeout for `s6_reprove` was not read: a long walk at the S6 close may be cut there (P4c reports).

## §12 Lead decisions after N3b (10.11.2026; carrier of the reasons: `docs/tasks/handoffs/20261110-lead-window-acceptance.md` section 4)

Each line is part of the named node's DoD; a dispatch of that node quotes its lines.

- **N4.** (a) A failed pytest row with text and site `{}` (no trace-tail line) ends in the critic's judgment with the row's text as the
  fact, never `incomplete` + `cause: tooling`; test with the N0 pytest fixture row. (b) The fixture `error` row goes to the critic
  (F12 = A); `test_error_row_no_cause_until_n4` is rewritten to pin that. (c) `detectors.json` is read once per process
  (`assertion_detectors._document`), not on every `parse_node` call; test: two calls, one read. (d) The «compiled output wrapper»
  residual is text of the entry: printed where the entry carries it, absent on Python.
- **P4a.** Remove the dead guess `detector=bool(spec.get("language"))` in `test_probe_target_fact.py:101`.
- **P5.** `ROAD_EXCEPTIONS` (`_resolve_oracle`, `_probe`, `_plan`) ends empty: P5 removes `ProbeCtx.detector` and with it the three rows.
- **P7 (live proof).** The report of the live run carries one more line: how many probes of the story ended in a critic judgment
  because the form has no message slot (xunit `Assert.Equal…`, jest `toBe` outside `@playwright/test`), and what those judgments
  cost. P3 is not reordered before that number exists.
- **Standing (done, not to reopen):** `marker_read` per entry is the place where a runner's token may be read; `with assertRaises` /
  `pytest.raises` is a check with `invert: null`; Python `tail` = chain::function.

## Reading trail

Read for this revision (the guard refuses whole reads of these three, so ranges): the first draft of this file whole by ranges (`wt-fbfix`, :1-409); t-2076 whole by ranges; `t-2064-p0-joint.md` whole; the finding whole; `PROJECT.md` P29-P31 by Grep with context; `t-2045` :1-30, :177-243, :307-343, :452-513, :541-605.

N1: **read through the worktree on disk, not `git show`: this role has no Bash.** `.git/worktrees/wt-tp-n1/gitdir` names `D:/ws1/wt-tp-n1`, its HEAD is `refs/heads/tr/tp-n1`, and that ref reads `9a2985725...`. Whether the worktree's files have uncommitted edits: not checked. Function names and docstrings by Grep: `_python_checks`, `_source_checks`, `check_on_line`, `test_body_span`, `_target_of`, `_repeat_check`, `_off_target_note`; test names of `test_probe_one_road.py` there.

Code, read on `wt-fbfix`: `probe_by_code.py` :1251-1305, :1657-1696, :1841-1844, :1912-1925, :2905-2919, :3142-3290, :3313-3317, :4209-4248, :4288-4296, Grep of defs, of `proved_by`, `fires_on`, `author_green`, `_SURVIVOR_ORDER`, `WINDOW_PROBE_FIELDS`; `probe_debt.py` :155-170, :218-249, :254-344, :606-637, :893-925; `proof_level.py` :1075-1089, :1262-1301, :1375-1414, :1447-1510, :1660-1692; `red_sandbox.py` :700-887; `window_record.py` :600-648; `acceptance.py` :1050-1119; `story_run.py` :12319-12378; `launch_check.py` :701-729; `execution_request.py` by Grep (`argv`: lines only); `handoff_check.py` :418-422; `s5.md` :196-209 and Grep; `qa-code-critic.md` by Grep; `test_probe_marker.py` :340-353, :404-412; `test_probe_marker_judgment.py` :108-122; `test_story_run_s6.py` by Grep; `tr-arm-b/scripts/run-playwright.mjs` whole; `detectors.json` by Grep (`soft_assert_patterns` :276, M-TS2 :284).

Carried from the first draft or t-2076 and **not re-read here**: the §11.6 counts; `cart_page.spec.ts:83-85`, `add_to_cart.spec.ts`, `cart.spec.ts` lines; arm B's record identity keys; `playwright.config.ts` lines; t-2076's per-file probe call counts; `proof_level.py:990`; `artifact-writers.json:136`; `s5_precheck._all_soft` (:765, existence by Grep only); `_judge_dispatch_why` body; `direct_test_form`.

Marked not read in the text: `instance_contracts`; `validate_request` against a changed argv; `C.sensitivity_proof_issues` on unknown keys; the A24 registry file's name; test wrappers of `test_probe_by_code_languages`, `_copy`, `_binding`; `self.py`'s timeout; D-0010; N2's rule for an `assert` that has a message.

Grep with a negative result: `9a2985725|tr/tp-n1` over `.git/packed-refs` was empty; the positive answer came from reading the loose ref itself, so no absence claim rests on it.

No run of any kind; no write but this file.

Needed beyond the manifest: `probe_debt.py`, `proof_level.py`, `red_sandbox.py`, `window_record.py`, `acceptance.py`, `story_run.py`, `launch_check.py`, `handoff_check.py`, `s5.md`, `qa-code-critic.md`, `detectors.json`, three test files, `run-playwright.mjs`, the worktree `wt-tp-n1`.

## §13 Lead decisions after the P3 partial hand-in (10.11.2026)
- `_edit_shape(base_text, start, end, added, lexer)` is the signature (the removed text is `base_text[start:end]`); item 2's `(base_text, removed, added, lexer)` is withdrawn: the arithmetic needs the position.
- `plan_model` takes `tokens` and `instance_id`; `_assert_with_marker` takes the marker expression; `_assert_that_with_marker` also takes the form row.
- The `product` door in `_models_refusal`: listed only where the product probe door opens for the check's language. The carrier is whatever t-2045 E-E / E-F and the product probe module already read; if no reader of that fact exists, `product` is listed for every check and the gap is a named residual for P6 (FR-2: a door a refusal names must open).
- Two `find` entries with identical text on one region are refused as overlapping, naming both.
- `write_invert_entries(task_root, dispatch, keys=None, reason=..., plan_args=None)`: `plan_args` is the keyword that carries the `--plan` arguments.
- `invert` on a `#2` key (the second check of one line) is refused in P3; P4b opens it or keeps the refusal with its door - P4b's dispatch quotes this line.

## §14 Lead decisions after P4a parts 1 and 2 (11.11.2026)

- `author_green_of`: identity = the instance's content sha, fingerprint = `original_input_hash`'s value. Route 1 (the binding) is read exactly as `_run_alternative` reads it and does not compare the fingerprint; that asymmetry and the inline copy of route 1 in `_run_alternative` are named for the chain's critic at P4b.
- A retried green: no row field marks a retry, so the latest row of the instance on these bytes decides. Named residual.
- The entry's sha is the sha256 of the model entry's canonical JSON (sorted keys, the fields `check`, `instance`, `alternative` and the entry's one kind with its value and `supposes`); the record field and the `already_probed` keyword are `entry_sha`.
- `probe_record_path(..., target_line=, ordinal=1)` names the per-check file; `ordinal` 2 gives the `-2` suffix.
- A key is skipped by the walk as proved only through `_check_proved(task_root, iid, line, ordinal, entry_sha) -> bool`: the per-check record exists, is readable, carries the same `entry_sha` on the same target bytes, and its outcome is a proof (`intended_failure`). Anything else, an unreadable record included, is not proved. `already_probed` keeps its meaning.
- The checks directory has ONE writer rule: every write goes through `_check_record` (and so through `keep_standing_record`); `_finish_record` writing there by its own rule is a defect for P4b's wiring to remove.

### Amended 11.11.2026 (critic t-2411 F3, F4; Lead)

- **F3 - a survivor is carried.** A per-check record whose verdict is `no_failure` or `wrong_location`, with the SAME `entry_sha`, the SAME bytes key (next point) and the same no-retry flags, is carried as it stands: no run. Its row keeps the verdict in the aggregate (a survivor stays a survivor: it is not a proof, the plan stays incomplete, no receipt). Any other stored verdict (`incomplete`, `not_executed`, an unknown one) reruns as before; a changed entry or changed bytes rerun. This replaces "its outcome is a proof (`intended_failure`)" as the only skip of the point above; `_check_proved` still answers only for `intended_failure`, and the walk reads the stored verdict through `_check_standing`.
- **F4 - the bytes key.** "Target bytes" is, for a check that lives in the test's OWN body, the INSTANCE's code sha (`proof_level.instance_identity`'s `instance_code_sha`: the test function's own code); for a check in a helper file, the sha of that FILE; so a comment or another test's edit in the same test file reruns nothing, and one test's fix never makes another test's proof stale (D5). Two refinements, both toward running: a check of the test file that lies OUTSIDE the test's body (a helper function of the same file) is keyed by the file's sha too, since the instance's code sha does not cover it; when the instance's code sha cannot be computed (no mined job, no reader for the language, an unparseable file) the key falls back to the file's sha. The record carries the key it used as `bytes_key: {kind: "code_sha" | "file_sha", sha}`, beside `mutated_file.sha256` (still the file's sha).
- **Reading an older record.** A record is read by ITS OWN kind of key: `file_sha` stands when equal to the file's sha now (even when an instance code sha is available: the same file is the same instance); `code_sha` stands only when the same instance code sha is measured now (none: it does not stand); an unknown kind or an empty sha never stands. A record that carries no `bytes_key` (written before this amendment) is read by the old rule alone: its `mutated_file.sha256` equal to the file's sha now stands, any other does not - never a silent pass, never a silent drop. The code is `probe_by_code._same_bytes`; the tests are in `test_probe_fix_round.py` (`test_f3_*`, `test_f4_*`).

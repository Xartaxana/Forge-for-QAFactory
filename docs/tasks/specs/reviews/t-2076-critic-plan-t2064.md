# t-2076 — critic on plan: t-2064 a red probe on every check, on top of t-2045

## Verdict

**NEEDS WORK (`fit_with_fixes`). 10 blocking, 11 to fix in the same text pass.** Accepting the spec and deciding the forks stay with the Lead tier and the owner.

The direction carries out the owner's words: the road, P29-P31, all nine forks. A weaker builder cannot execute it yet. P0 and P3-P7, plus N3b through §11.3, need the amendments below. P1 and P2 are executable. All are text amendments; nothing needs redesign.

Marked "reasoned" = traced in code or from the library's behaviour, not run. Nothing was run on a stand.

## Blocking findings

**B1. P3 refuses its own worked example: `lexical_shape` equal cannot hold for a replaced value.** `lexical_shape` counts each bracket and the lexer's end state (`probe_by_code.py:759-763`). P3 item 2 and E-N demand it equal.
- Input: `{"check":"…cart.spec.ts:112","actual":"500"}` on `expect(r.status(), m)`.
- Wrong output: `(` goes 1→0, refusal before the write. The same happens to §11.8's `page.locator('body')` for `catalog.cartBadge`, `{ [A]: 1 }` for `await guestCart(page)`, and `"3"` for `lines[0].quantity`. F-P9 exists for the 101 of 169 checks read inside the statement, and it is dead on them. A `find` with a bracket change dies too.
- Amendment: the replacement is balanced by itself and ends in code; the file's shape equals base minus removed plus added, the rule `_with_marker` already uses (:1296-1298). Add a test per language with an argument that has brackets replaced by a literal, and the reverse.

**B2. F-P8's "no role" cannot be told, and the callers that have no role are not owned.** P4 names `--s6-close` and `probe_debt._replay_plan`. The real callers:
- `story_run.s6_reprove` (`story_run.py:12338-12357`) calls with `--dispatch <running S6>` or `--s6-close`, no `--at`, no model.
- `probe_debt.settle` calls through `_probe_args` (:160-170) under the critic's `--dispatch`, at the critic's `start`, before he has written anything (t-1937 :140; budget `story_step.py:475`, about 90 s for the whole `start`).
- `_replay_plan` only builds arguments, so `_probe` cannot know.

Wrong outputs:
- S6 with a running S6 dispatch: P4 item 1 refuses every stale test. "not proved again" appears as a digest line per test and the delivery carries the reason, with no bug visible anywhere.
- Settle at `start`: refused, debt left.
- If a builder keys "no role" on `--mutation invert`: the critic gets a free bypass, since that flag is in his text (`s5.md:199`).
- "Replays stored `models`" has no producer: `checks[]` in P4 item 4 stores `probe_kind`, `supposes|reason`, not the edit (AR-22).
- A walk under settle's 90 s: 3 runs at mean 72 s is 216 s (how settle cuts a running probe: not read).

Amendment, stated by context, not by a flag the role can type:
- No role = `stage == "S6"` from `_dispatch_context`/the dispatch row.
- Replay = the entries stored in the record (the full edit goes into `checks[]`).
- S5 settle with no stored entry and no inversion on record: the item stays with the critic ("model owed"), no run.
- A record whose stored kind is `invert` replays as `invert` with its reason.
- Owns gain `probe_debt._probe_args`, `settle`/`_classify` (`plan_unfinished`), `proof_level._replay` (:1686), and `story_run.s6_reprove` (a read check, or a test). AR-19's row names `s6_reprove`.

**B3. `--at` is a second road around F-P8 and E-K.** P4: "`--at` stays: one check, inversion or its model entry, one record".
- Input: a critic refused by F-P8 runs `--at :128` with no entry, then `--at :129`, and so on.
- Wrong output: silent inversions with no reason, which E-L refuses on the walk. On a fresh instance the record goes to `<iid>.json` (N1b writes beside only over a proved one), and `_finish_record` (:3150) publishes on `intended_failure`. So a receipt can stand on one check of several, against E-K's invariant, unless the builder guesses. Whether `--at` rebuilds the aggregate is not stated.
- Amendment: `--at` is a plan of one row through the same loader. No entry: the same refusal and door. Always the per-check record, then the aggregate rebuilt by its one writer; receipt only when complete. Tests: `test_at_no_entry_refused`, `test_at_never_publishes_partial`, `test_at_fills_the_aggregate`. N7's door `--mutation invert` changes to name the `invert` entry (FR-2).

**B4. P4 flips the default of every no-`--at` call and has no pin table. This is the class of t-2050's own findings.** A no-model call becomes a refusal.
- Probe call sites by grep (a count of lines by one regex, not of tests): `test_probe_by_code` 32, `_copy` 9, `_binding` 6, `_languages` 4, `test_probe_debt` 10, `test_probe_marker_judgment` 9, `test_probe_target_fact` 2, `test_probe_gap_door` 2. Plus `test_probe_one_road.py` (447 new lines on N1's branch: `test_default_target_is_assertion_id`, `test_no_id_takes_first_with_note`; N1b's `test_printed_door_runs_second_call`).
- P4 owns only `by_code`, `debt`, `marker_judgment`. Its DoD names `_languages` and `_copy` as "CI", yet they are not in `owns`, and the builder may not run them.
- Wrong output: the batch pipeline red, owner of the red nobody.
- Amendment: a "Pin owners" table for P3-P7 in the form of t-2045 §6; one test helper that writes an `invert` entry so the flip is one place; `owns` gains the named files.

**B5. Edge 4: E-F and E-G do not state what happens to a chain with an inner failure.**
- Input: chain a, b, c; run b with a as written; a fails on a stand hiccup, or a helper throws between them, or b's own argument throws. In all of them the row is failed and b's token absent.
- Wrong output: E-F says `not_reached`, rerun alone, but b is already alone. E-G says later rows `not_reached`, walk stops "for that chain", but `run_plan` returns `{run, keys, why}` with no chain. `test_chain_red_link_stops_walk` has no definition. Keying on "no token = stop" lets a throw in b's arguments kill the proof of every later check. Keying on "continue" spends a failing run per later check.
- Amendment, position invariant in P4 item 2: E-F's rerun applies only to a group of 2 or more. A run of one, failed, token absent: that key is `_row_unsettled`, the critic. The walk stops only when the failure's file and line (as a fact, never a proof) lie on the span of an EARLIER check of the plan: later rows `not_reached`, `plan_remaining`. Any other failure (helper, own argument, no location): the walk goes on. A throw in a helper's own run is the same rule. Pin all three cases.

**B6. Edge 3: a check still waiting when the test times out may print its marker without having decided.** §11.0 rests on "a library prints a check's message only when the check fails". Reasoned, not run: Playwright ends a polling `expect` at the test timeout and reports it as an error of that `expect`, carrying its custom message.
- Input: a group of 7 web-first soft checks; `:137 toHaveText('1')` is polling when `timeout: 30_000` fires (§11.8 predicts exactly this neighbourhood), and it would have gone green later.
- Wrong output: token read, `intended_failure`, `proved_by: marker`, no role, on a check that never decided. This breaks top invariant (b). P0 s4's checks all fail anyway, so it cannot see this, and the adversarial list omits it.
- Amendment:
  - P0 gains s4b: a soft check on an element that appears after the test timeout.
  - The browser is not "if installed": arm B ran e2e, so one exists, and `page.setContent` needs no app. 68 of 169 checks hang on this; N0 had no browser run.
  - If the marker prints: rule in `_judge_joint_rows`, language-free. With any token absent, the last read token in source order also reruns alone. With all present, a data row of the runner's interruption text demotes the last one to an alone run. It only demotes, never proves.

**B7. Edge 8: P0's rule leaves branches unstated and names no later node.** The full table is under Edge 8.
- s1, s2, s3, p1, s6's second and third cases have no result rule.
- "The same rule" for unmeasured is unclear for s4.
- The s5-fail rule sends every joint row to the critic: 136 checks × a turn of 60-100K = 8-14M cached input (estimate), against §11.6's 2-2.5M. The other exit, one run per check, keeps proof by marker with no role at +58 runs. That is a fork for the owner; it is not written.
- Amendment: the table below goes into P0, each row naming the nodes it changes.

**B8. Edge 7: §11.3 leaves two contradictory places for N3b. N2 is followable, N3b is not.**
- (a) Edge letters collide: E-A..E-Q exist in both specs with different meanings, and "this file wins". N3b's `edges: E-G` is the throw in t-2045 and the chain here. Rename §11.4's edges `EP-A…`.
- (b) §6's pin rows stand: `test_fires_as_still_fast_path` says "the detail with `message_marker: ""` keeps `fires_as`", and `test_unknown_text…` gets a marker-less control. A builder following them keeps library wording as proof, against §11.3 and «Только наш текст».
- (c) N3b item 9's guard lists `_at_statement`, `_line_proof_allowed`, which fall.
- (d) "Everything else `_row_unsettled`" collides with step 3 (`error` no cause until N4; unknown status `not_executed`; E3.1 no rows).
- (e) `proved_by` "`marker` or `judged`": the code writes `critic` (`:4321`) and `_receipt_core` reads `== "critic"` (`:2544`). `judged` loses `judgment_quote`.
- (f) E-D and E3.5 still rank `line < fires_as < marker`.
- Amendment: write N3b whole in this file (the designer cannot Edit t-2045) with its pin rows, and leave a one-line pointer in t-2045. Read `proved_by` as `marker` or `critic`.

**B9. Edges 2 and 5: `red_sandbox.py --probe` settles a proof by status, line and library wording, with no role, and reaches the same acceptance on another road.**
- `verify` at `red_sandbox.py:717-722`: `failed` + `failure_kind == assertion` + location equal + `reason_matches`.
- Its receipt goes through `write_sensitivity_receipts` (:790), `already_probed` (`proof_level.py:1270-1296`) and `window_record._probe_from_receipt` (:628-648), which outputs `verdict: intended_failure` with equal locations.
- The charter, `s5.md:122` and the doors of t-2045 E-E and E-F offer it. t-2064 says "not changed, named".
- Input: an instance with 8 checks, one `invert: null`; the critic takes the named door. Trace from reading, not run.
- Wrong output: a receipt with no `checks`, which E-I reads as an old receipt ("stands, info line"), so `approved` on one proof of several, proved by wording. E-K's invariant, "no text but our marker" and the one-road rule all fail.
- Amendment, on the recommendation until the word: a product receipt counts only for the check it names. The others stay owed, and its proof goes through the critic (it is his run). E-I's "old" means "written before this batch", not "has no `checks`". P6 owns this. If the owner wants the product probe to stand alone, that is his named exception (P31). Question 1.

**B10. E-Q has no door: a check in a branch not taken traps a healthy test.** Real: `cart_page.spec.ts:83-85`, `if (!guestKept) { await expect.soft(notice, 'Then 1: …').toBeVisible(); }`.
- Input: an instance where `guestKept` is true.
- Wrong output: row passed, `actual` kind, `no_failure`. `--judge` refuses it (`_judged_record` :4223 takes only `incomplete` + `judgment`, though E-Q says "the critic reads"). Charter :63 calls `no_failure` a `test_defect`. E-K gives no receipt. So either the author is blamed or the person is asked, against «ооооочень редкий случай».
- Amendment: an entry kind `{"check":k,"instance":i,"not_here":"<why this instance does not reach it>"}`, presence-checked only (AR-29). The aggregate shows it as not owed by this instance, with the reason, and a tier above reads it. Question 3.

## To fix in the same text pass

- **S1. §11.6 cost text** (Edge 6).
- **S2. P4 item 4 aggregate keys.**
  - Name every key its readers need: `failure_kind` (`acceptance.py:1081`), `mutation` = `invert` (`_replay_plan` :228 refuses others), `target`, `restore`, `test_node`, `mutation_detail` with no `at` (`proof_level.py:1686` returns None otherwise).
  - The forced-equal location and reason make those acceptance lines vacuous for a walk: say so, and let `_aggregate_record` be the check.
- **S3. Per-check records in `work/probes/`.** `probe_debt._scan` (:301-316) reports every `<iid>--L47.json` as "row gone: the manifest has no row"; `handoff_check.py:419` lists them. Put them in `work/probes/checks/`: readers glob non-recursively, the convention of `alternative/` (`proof_level.py:990`).
- **S4. E-M keyed on `soft_assert_patterns: []` gives "no finding" on Java and C#**, where `SoftAssertions`, `assertAll`, `Assert.Multiple` exist (§11.9, P1). P29 says "автотест пишут так" for all, and P7's charter says "where it has one". The two disagree. Amendment: the critic judges by what he knows of the framework; the row decides only the plan. Scope rows get a line in Остатки with a node, not "TR2-16's candidate".
- **S5. F-P8's refusal offers `invert` on `invert: null` forms** (`assertThrows`, `assertAll`, `Assert.Throws`: `detectors.json:161,239,289`), where `find` may have no meaning (FR-2). Print only the doors that open. Name the exit: `unverified` for that check.
- **S6. P5 is not executable.** No call form for an alternative on the road; no rule for two entries on one check (a plain one and one with `alternative`); `_judge_run` (its `judge_row`), `report_rows` non-raw, `_alternative_gap_record`, `_model_target` not in `owns`. N3b's `ROAD_EXCEPTIONS` line for `_judge_run` must fall with it.
- **S7. P3 owns no Python edit.** An un-inverted `assert` with a marker needs `_assert_replacement`, `_assert_that_replacement` or a named new function; `plan_mutation` for `invert` in `plan_model`. Say edits apply bottom-up. Say which body bounds `find` when the check is in a helper (the helper's) and what follows if the read is in the test (`invert`).
- **S8. Tokens and failure text.**
  - `started_at` per run, not per walk, or an alone rerun shares the joint run's token.
  - `failure_problem` (:1841) returns the first failure only: `_judge_joint_rows` must read all problems (safe today, costs reruns).
- **S9. E-J.** `RUN_TIMEOUT_S` per call is 1860 s, and a critic's Bash foreground ends at 600 s (reasoned from the tool's documented limit). A killed walk writes no `plan_unfinished`, and only row-by-row records make "the same call continues" true. P7 tells him to run it in the background. `s5.md` has no such line.
- **S10. F-P7.** The row is per form, and arm B's command is `run-playwright.mjs`. By N3b item 7's reading the form id of a project's script is empty, so the row never fires there (`runner_identity` not read). The wrapper forwards extra arguments (read). P0 s7 must test the form id too.
- **S11. Static guard and old spellings.**
  - No node extends the road list to `checks_of`, `run_plan`, `plan_model`, `_walk_plan`, `_judge_joint_rows`, `_aggregate_record`: add it, or the detector does not see them.
  - `--mutation alternative` "for one release" is a second spelling nobody needs: a story keeps its plugin generation (B-014), and the batch has no release between. Remove at P5.

## The edges by name

**Edge 1. All nine forks: on the owner's side. F-P8 needs B2, B3; F-P9 needs B1; F-P7 may do nothing (S10).**

| Fork | Owner's side | Note |
|---|---|---|
| F-P1 A | yes («на каждый ассерт») | a setup helper's unbound checks stay unlisted, with a count: named, tell him |
| F-P2 A | yes | a second list would go stale; the `:46` case is real as cited |
| F-P3 A | yes («правильно») | see below |
| F-P4 A | yes, stricter than the word | `None` frequency unknown: cost, S1 |
| F-P5 A | yes, literal | |
| F-P6 A | no word yet; returned | take it: 31 of 49 reports carried more than one failed test, recounted |
| F-P7 A | no word needed | S10 |
| F-P8 A | yes | below |
| F-P9 A | yes | B1 |

**F-P3, "the form is the declaration".**
- Trap: none. Whatever the author wrote gets a plan; only the bill changes.
- Bypass: writing everything soft shrinks the plan. A dependent soft check then reads junk under a model, and the alone rerun still reads it. The critic is the one reader (E-M), which is AR-29 correct.
- Unlisted form: `expect.configure({soft:true})` gives a head of an unknown form, so E-P applies.
- Hole: S4.

**F-P8, refuse with no model.**
- Trap: only on `invert: null` (S5), and the person's word is still the last door.
- Bypass: yes, today by `--at` (B3) and by whatever flag means "no role" (B2).

**Edge 2. «Только наш текст доказывает без роли».** The probe road itself is clean after §11.3: marker, or the critic; `no_failure` stays a status and is not a proof. Three paths remain:
- `red_sandbox` (B9, real).
- N3b's pins keeping `fires_as` (B8b, a spec contradiction).
- Old receipts by `fires_as` on the same bytes (E-I): a residual reached only by a plugin change inside a story, acceptable as named; tell the owner.

**Edge 3. Joint run.**
- One marker read as another's proof: no. 12 hex per key and instance, exact match, joined at run time; other instances' rows are not read. S8's `started_at` is the one looseness.
- A `find` shared by two checks: the second may fire from the first's edit. It still shows the check can fail, but its `supposes` is then not what failed: name it as a residual.
- A soft timeout hiding one: an absent token is caught by E-F. A false proof at the timeout is not (B6).

**Edge 4.** Chain of three, healthy: sound (E-G, position invariant, `test_chain_three_runs_earlier_untouched`). Inner failure and throw in a helper: B5.

**Edge 5. Two roads. Left on the road:**
- `red_sandbox` (B9)
- `--at` (B3)
- `--mutation alternative` spelling (S11)
- Java and C# soft reading (S4)

Not exceptions:
- `--s6-close` and debt replay inverting with no role: an ordinary condition on the task, same marker, same record, named. This holds once B2 states it by stage.
- `build_request`'s selection, `is_pytest_command`, `put_back`: a runner's or interpreter's grammar, in `ROAD_EXCEPTIONS`.
- `[]` as data for the plan; `compare_left` as the AST reader's row.

**Edge 6. Cost.** The run figures are honest and labelled estimates: recount 49 reports, sum 3,540.84 s, mean 72.26 s, median 39.77 s, 12 over 120 s; the table's products check out. `121 + 14` slightly overcounts (E-B lets a stop join a group), the safe side. The token total is not an honest bound. It omits:
- (a) Fix rounds: arm B's record has `instance_identity: {}` and `test_code_sha: ""`, so any byte change in a file makes every proved check of every instance in that file stale. "One author rerun per changed instance" and "same bytes skipped" then mean a re-walk of the file, not one instance. Files hold 6-20 instances.
- (b) Judgments beyond the 6 marker-less: `author_green` `None`, a `find` that passes, a model that does not separate, a not-reached check failing alone. At 10 % of 169 (my assumption) that is 1-1.7M more. E-J's INV "one per instance plus one Write" is false by its own edges.
- (c) Cache: P25 names a 5-minute TTL on a project. A walk over it makes the next turn a rebuild, not a cached read; 3.07 runs × 72 s is 3.7 min on average, and 12 single runs already exceed 2 min. Priced as all cached, so a floor.

Amendment: print a range, name (a)-(c), drop the INV, and keep the live proof's return-to-owner rule. It compares with the range.

**Edge 7.** B8. N2's row is sufficient. N1, N1b, N7, N2b, N3a, N4, N5, N5b rows are followable. N6: state that charter :71-72 and `s5.md:200`, `brief_pack.py:224-227` pass to P7, or its §3 rows still write "the Then's check". §0 step 1 ("invert") is superseded too, not only step 3.

**Edge 8. P0, by result:**

| Case | Result | Effect (proposed where the spec is silent) |
|---|---|---|
| s1 | three markers | joint road stands |
| s1 | not three | as s5 fails |
| s2 | hard's marker read | E-B's "last" stands |
| s2 | absent | stop never joins; P2 item 2 changes |
| s3 | second absent | E-B stands |
| s3 | present | owner told; hard stop not a stop in this runner: stop and report |
| s4 | earlier lost | a line; `not_reached` |
| s4b | marker on undecided | B6's rule in P4; absent: no change |
| s5 | passes | as written |
| s5 | fails | fork (Q4); P2, P4 item 2, §11.6, P7 |
| s6.1 | fails | every model to the role, owner told; P3 item 4, F-P4, P7, §11.0 |
| s6.2 | marker read on a throw | message built before the throw: marker does not prove on this form; stop, owner |
| s6.3 | absent | web-first models to the role, owner told |
| s7 | forwards | row (with S10) |
| s7 | does not | none |
| p1 | absent | N2 already measured p1 yes: stop, conflict with N0 |
| unmeasured | any | no rule made from it, owner told; s4/s4b unmeasured: joint web-first rows go alone until measured |

## One line per node

| Node | Status |
|---|---|
| P0 | after B6, B7 |
| P1 | executable (S4 changes E-M, not P1's rows) |
| P2 | executable; add names `_source_checks`, `_python_checks` (on N1's branch) |
| P3 | after B1, S5, S7 |
| P4 | after B2, B3, B4, B5, B6, S2, S3, S8, S9; split it (see CODE QUALITY) |
| P5 | after B4 (pins), S6, S11 |
| P6 | after B9, B4 |
| P7 | after B3, B10, S4, S9, and the N6 boundary of Edge 7 |

## Questions for the owner (русскими словами; рекомендации мои, решает владелец)

1. Проба продукта (`red_sandbox`) ломает сам продукт и считается доказательством по строке и тексту библиотеки, без роли и за весь тест. Оставить так как исключение, или считать её только за одну проверку и через критика? Рекомендую второе: иначе это вторая дорога.
2. В 68 проверках из 169 проверяется элемент экрана. «Значение сломанного продукта» там выглядит как подмена элемента (`page.locator('#qa-none')`), что по сути близко к перевороту. Это то, что вы имели в виду, или на таких проверках честнее сразу переворачивать с записанной причиной? Рекомендую: роль решает сама, а в примере спеки показать оба варианта.
3. Проверка внутри `if` в тесте, куда этот параметр не заходит: можно ли критику записать «этот прогон сюда не доходит, потому что …», и проба за эту проверку с этого экземпляра не нужна? Рекомендую да; иначе здоровый тест идёт к вам на вопрос.
4. Если замер покажет, что на совместном прогоне маркеру верить нельзя: каждая проверка отдельным прогоном (дольше, примерно 58 лишних прогонов, но без роли) или совместный прогон и всё читает критик (136 лишних ходов)? Рекомендую первое.
5. После этой пачки формулировка библиотеки больше не доказывает ничего: все проверки без нашего маркера стоят одного хода критика. Подтверждаете? (Ваше слово «Только наш текст» читается именно так.)
6. На Java и C# есть мягкие формы (`SoftAssertions`, `assertAll`, `Assert.Multiple`), фабрика их пока не читает: такие тесты работают, но идут по прогону на проверку. Считать это отдельным узлом сейчас? Рекомендую: узел в пачке TR2-16, критик при этом всё равно советует мягкую форму.

## Standing questions

**«Разные рабочие пути для одного и того же — это баг»:** not yet met. Three second roads remain (`red_sandbox`, `--at`, the `alternative` spelling) and one language-shaped reading (S4). After B3, B9, S4, S11 none is left that I found.

**DUPLICATION AND CONSISTENCY:** two findings. `_judge_joint_rows` beside `_judge_rows` and `_row_by_marker` risks two judges, although E-A says a joint run of one is the plain run: make `_row_by_marker` take tokens, and let the joint function be the per-token loop over it. `plan_model` and `plan_alternative` live together from P3 to P5, named and queued, so not a finding. `author_green_of` should reuse what `_run_alternative` passes as `author_green` (:3877 on: not read). Grep of `lexical_shape`, `_call_arguments`, `failure_problem`, `author_binding`: reused, correctly except B1.

**CODE QUALITY:**
- P4 is too big for a weaker builder: 8 requirements, 21 tests, walk, judge, aggregate, receipt, `--check`, debt, state exits. t-2045 split nodes over about 3 hours. Split into P4a walk and records; P4b aggregate, receipt, `--judge`; P4c replay. Severity: fix before dispatch.
- Forced-equal reasons (S2): a check whose result nobody reads.

**JUDGMENT (AR-29):** no check reads a role's words; `supposes`, `reason` by presence. B5's location is a join that orders a walk, never a proof. Sound. **ARCHITECTURE:** AR-19's row misses `story_run.s6_reprove` and `proof_level._replay` (B2).

**Class completeness (map):** `docs/SIBLING_MAP.md` by Grep for the probe's readers (:142 report rows; others too long for the tool's line). The new axis stays TR2-15's, queued. By that walk `red_sandbox` is the twin that does not follow (B9). A wider scan was not done.

## Trail

The guard refused whole reads, so everything was read in ranges.
- `t-2064` whole. `t-2045` :1-243, :278-372, :452-635 (not N0, N2b, N3a, §9-§10). `t-2050` :1-30. N0 report :1-64 and a Grep. Finding and P29-P31 whole. `critic-diff-brief.md` whole.
- `probe_by_code.py` map and :753-766, :1179-1305, :1841-1846, :2472-2495, :2522-2560, :3156-3290, :3326-3377, :3560-3608, :4209-4332, :4474-4518, :4575-4649. `probe_debt.py` :150-324, :560-646. `proof_level.py` :268-308, :1270-1296, :1663-1692. `story_run.py` :12318-12378. `window_record.py` :575-654. `acceptance.py` :1050-1119. `red_sandbox.py` :712-725, :1175-1196. `s5.md` :118-131, :196-206. `qa-code-critic.md` :40-75. `detectors.json` by Grep. `story_step.py:471-482` by Grep.
- Arm B, read only: `run-playwright.mjs`, `playwright.config.ts` by Grep, one record's identity keys, `cart_page.spec.ts:80-88`.
- N1: `git show 9a2985725` stat and function names.

Control re-runs:
- 49 `red_probe*junit.xml` under `evidence/runs`: sum 3540.84, mean 72.262, median 39.767, over 120 s: 12, more than one failed test: 31 (positive control of the walk: 83 entries in the directory, 49 hits).
- First listing by a wrong glob (not in subfolders) gave 0; redone by `find`.
- Negative on `probe-models` over five named files was empty; control: the same tool found 8 in `probe_by_code.py`, and `artifact-writers.json:136` names the critic its writer, so that path is open by data; the guard's Write rule itself not read.

Deviations: ripgrep timed out over the package tree, so three reads went through shell `grep` on named files; one command began with a `cd` by mistake, harmlessly. No pytest, no process left (the background count finished, exit 0).

Needed beyond the manifest: `story_run.py`, `proof_level.py`, `red_sandbox.py`, `window_record.py`, `acceptance.py`, `story_step.py`, `s5.md`, `qa-code-critic.md`, `detectors.json`, `t-1937`, `SIBLING_MAP.md`, arm B's files.

```json
{"verdict":"fit_with_fixes","blockers":["B1 lexical_shape equal refuses every bracketed actual, including the worked example","B2 no-role in F-P8 undetectable; s6_reprove and settle callers unowned; stored models have no producer","B3 --at bypasses F-P8 and can publish on one check","B4 P4 has no pin table; slow test files named CI are not owned","B5 chain inner failure and throw: E-F and E-G state no rule","B6 marker of a check interrupted by the test timeout may read as proof; P0 cannot see it","B7 P0 decision rule leaves branches and later nodes unstated","B8 N3b: colliding edge letters, fires_as pins, removed functions in the guard, proved_by judged vs critic","B9 red_sandbox settles by status, line and wording with no role and reaches acceptance on one proof","B10 a check in a branch not taken has no door: no_failure, no judge, person asked"],"fixes":["Replacement balanced by itself; file shape = base minus removed plus added","No role by stage S6; replay stored entries; own _probe_args, settle, _replay, s6_reprove","--at is a plan of one row through the same loader, aggregate rebuilt, no partial receipt","Pin owners table for P3-P7 and one helper writing an invert entry","Position rule: run of one with absent token goes to the critic; walk stops only on a failure on an earlier check's span","P0 s4b with a browser; demote rule for the last read token","Decision table by result naming nodes, in P0","Write N3b whole in t-2064, rename edges, marker or critic","Product receipt counts for its named check, via the critic, unless the owner names the exception","Entry kind not_here with a reason, presence only","S1-S11 in the same text pass; split P4"],"class_completeness":"Twins walked by reading: red_sandbox does not follow (B9), s6_reprove and proof_level._replay missing from AR-19 (B2). SIBLING_MAP read by Grep only; the one-road axis stays queued at TR2-15. No wider scan.","trail":{"read":["docs/tasks/specs/t-2064-probe-every-check.md","docs/tasks/specs/t-2045-one-probe-road.md (ranges)","plans/piles/thinking-roles/findings/20261106-odna-doroga-proby-na-vse-yazyki.md","PROJECT.md P29-P31","docs/tasks/specs/reports/t-2045-n0-frames.md (ranges)","docs/tasks/specs/reviews/t-2050-critic-plan-t2045.md (head)","docs/tasks/critic-diff-brief.md","scripts: probe_by_code.py, probe_debt.py, proof_level.py, story_run.py, window_record.py, acceptance.py, red_sandbox.py (ranges)","skills/qa-story/phases/s5.md, agents/qa-code-critic.md (ranges)","arm B: run-playwright.mjs, one probe record, cart_page.spec.ts:80-88"],"reruns":[{"command":"count of testsuites time over 49 red_probe junit reports of arm B","result":"sum 3540.84 s, mean 72.262, median 39.767, over 120 s: 12, more than one failed test: 31"}]}}
```

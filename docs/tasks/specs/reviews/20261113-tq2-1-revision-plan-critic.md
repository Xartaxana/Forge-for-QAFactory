# Critic on the plan: TQ2-1 revised for option (c) (K1, K2, N5)

Plan under review: `docs/tasks/specs/20261113-tq2-1-revision-option-c-spec.md` (designer, 13.11.2026). The facts were checked on
read-main at **5cc4f88** (`git -C ...read-main log -1` → `5cc4f88 wave 1 CI repair round 1`). R = `C:\QAFactory\forge-repo\.claude\worktrees\read-main\ai-packages\qa-factory`.
Mode: read-only. I ran two deterministic control measurements (a test file and role_load); both are listed in the trail.

## Verdict line

**NEEDS WORK (fit_with_fixes). 4 findings block DISPATCH (B1-B4). Each is a spec-text decision the Lead can make by editing the
spec; none needs a re-cut. 11 small amendments (A1-A11).** The direction of K1, K2 and N5 is right, and so is the K1/K2/N5 cut.
G1 is a real leak. As written, though, K1 and K2 would each hit a stop with certainty (B2). K2 would also give the plan critic
two lines that contradict each other (B1). Whether to accept, and the decision on every fork, stay with the Lead.

---

## Blocking findings (fix in the spec before any builder dispatch)

**B1. K2 item 7 says the plan critic's brief needs no change. That is false: merged into `hint_rows`, merge hints reach the critic
under a line that calls them grouping hints and says "never a blocker", which contradicts F5 (a).**
- R/scripts/brief_pack.py:2011-2017 (5cc4f88): `rows, why = _sp().hint_rows(task_root)`; `if why:` → `"grouping hints not computed (...)"`;
  `elif rows:` → `"... prints {len(rows)} grouping hint(s): tests at one level in one file that each prove one case ... a test left
  unmerged is a remark, never a blocker on its own"`.
- K2 item 7 makes `hint_rows` return `grouping_hints + merge_hints`. Item 8 (F5 a) makes an unanswered merge a `blocker`. So
  the plan critic would read: the count of "tests at one level in one file" includes a merge pair, and the line calls it "never a
  blocker", while the rubric clause calls it a blocker.
- A second effect of item 7's new `why`: when `case_concerns` raises, `hint_rows` returns (grouping rows, "merge hints not computed").
  The `if why:` branch at :2012 then prints only "grouping hints not computed (merge hints not computed ...)" and drops the grouping
  hints that WERE computed. That is a false negative on the grouping road. `s5_precheck.plan_result` (s5_precheck.py:4296-4298)
  handles both values, so only brief_pack is wrong.
- The line is pinned by test_brief_pack_s5_plan.py:562-564 (K7, `endswith("a test left unmerged is a remark, never a blocker on its
  own")`). That pin stays green only because the K7 story has no S4 round, so the contradiction would ship without a red test.
- Fix (Lead): keep `merge_hints` OUT of `hint_rows`'s single count. Either give `hint_rows` a separate merge list, or have
  `plan_dispatch_lines` (already K2's) call `merge_hints` and print its own line, e.g. "`s5_plan.py --check` prints N merge
  hint(s): the case critic asked to parametrise cases the plan keeps apart with no `apart_reason` - an unanswered one is a blocker
  (rubric «On the plan»)". Restate item 7's contract: `why` is non-empty only when nothing was computed, or the two whys are kept
  apart. Add one acceptance row for the critic head carrying both lines.

**B2. Every ratchet K1 and K2 touch has zero headroom at 5cc4f88, so the "stop and return a question" edges (K1 key 4, K2-E8)
are certain to fire. They are decisions left undecided, not edges.**
- Measured: `python -B R/scripts/tests/test_brief_pack_s5_plan.py` → `RATCHET S5_PLAN_BRIEF_BYTES_MAX 9520`, `213/213 ok`, exit 0.
  The ceiling is `S5_PLAN_BRIEF_BYTES_MAX = 9520` (test_brief_pack_s5_plan.py:541; FV1-4 N1 renamed it, so `DOORS_ONLY_BRIEF_MAX`
  no longer exists). Measured equals ceiling. K2 item 3 adds the files line `- case critic's concerns: none carried` to the plan
  critic's brief even with 0 concerns, and that is exactly the K7 story (no S4 round). So K7 turns red on any K2 build.
  `_short(..., HEAD_LINE_CHARS)` does not help (K2-E8 assumes it does).
- Measured: `python -B R/scripts/role_load.py --all --json` → `qa-case-designer tokens 13316` against `ratchet_tokens` 13320
  (4 tokens of room), and `qa-case-critic tokens 18296` against 18296 (0 of room) (role-load.json:14-15). K1's bullet grows by
  ~350 characters (~90 tokens), and the critic :44 parenthesis by ~40 characters (~10 tokens). Both roles go over their rows.
- K1 key 4 reads the bound as "13320 + slack". role-load.json:2 says the opposite: "a role over its row is a red A22";
  `ratchet_slack_tokens` measures how far a row may sit ABOVE the measured load before A22-K8 calls it "not tight". It is no
  headroom above the row.
- Fix (Lead, AR-20 / axis 18: "a raise in the diff that adds the site"): the spec names the raises up front, with numbers to
  re-measure at build time, so the builder never has to stop. Examples: qa-case-designer row +~100, qa-case-critic row +~15,
  `S5_PLAN_BRIEF_BYTES_MAX` + the measured delta of the new files line. Alternatively, decide a compensating cut and name its
  source (K1: shorten the new bullet to the P16 example alone; K2: print nothing for 0 concerns, with the empty outcome stated
  in the side file or the `--check` output instead). Without one of these, both nodes are guaranteed to bounce once.

**B3. A load-bearing G1 fact is wrong, and the conclusion drawn from it is overstated.**
- The plan (§C.2, §1 G1) says the UI window cap defaults to 1 (`ui_window_cases or 1`). In fact the default is **2**:
  controller.py:271 `DISPATCH_DEFAULTS = {..., "ui_window_cases": 2, "api_window_cases": 4}`, and `_dispatch_setting` returns that
  default (controller.py:4287-4303). `or 1` applies only when a project sets 0 (controller.py:4540, :4443).
- `pack_windows` (controller.py:414-436) packs groups first-fit into a window of the same surface with room. Single-case groups
  of ungrouped partners can therefore share a window (UI cap 2, other cap 4, the driver's `s5_window_cases` 8).
- So the claim "they land apart WHENEVER the plan did not group them" (§C.2; §9's answer to t-723 L4) is false as stated. The
  true statement: partners stay together for certain only if the plan grouped them; otherwise packing decides by order and cap.
  The leak is real but conditional, and it is still worth closing: the plan dispatch is the only step that can make them one
  test for certain. The rubric sentence in K2 item 8, "no window can merge cases cut into two windows", is true only for the
  pairs that were cut apart.
- Fix (Lead): correct §C.2, the §9 L4 line and the F5 rationale. No node changes.

**B4. F3 (a) "on every road" is not delivered on the legacy road. The edge is left silent.**
- A legacy (driver) S5 is cut by CASES, not by tests: controller.py:4428-4443 (`split_windows(list(scope), ...)` when the mode
  is not PLANNED). Legacy has no plan step and no C12 `plan_remarks` machinery (C12 belongs to the planned window).
- K2 item 5 hands every legacy automator window the WHOLE story's side file. Each window then sees concerns about cases of
  other windows: noise that the automator charter's "what its brief does not list is not yours" would now invite it to act on.
  A merge pair that the cut split across two legacy windows still cannot be merged, which is the same leak as G1.
- Fix (Lead decides): (a) filter the legacy side file to the window's scope plus global concerns. Use one placement rule
  (`_placement` against the `split_windows` scope) so legacy and planned place concerns the same way (P31, axis 34). (b) Write
  the residual in the spec as an edge: "partners split by the legacy cut-by-cases: the window answers it in its digest; no merge
  possible". Either queue the legacy cut (keeping merge groups together) as a named node with its owner, or have the owner
  accept the residual. Correct the changelog wording "on every road (... driver process)" to what is actually delivered.

---

## Answers by question

### 1. Facts by trail (G1, G2) on 5cc4f88; wave 1 effects; stale references

- **G1 (under the cap: only the plan file, no CC-n):** CONFIRMED. brief_pack.py:2022-2025 names the plan file alone. The
  skeleton carries no concern (s5_plan.py:319-323). The plan dispatch's `names` come from `_input_names` (brief_pack.py:3550-3562):
  S5 `inputs` (stages.json: `state/story-case-links.json`, `test-plan.md`, `work/context-bundle.json`, `work/first-look.yaml`)
  plus ROLE_FILES `qa-automator` (brief_pack.py:99: s5-notes, notes glob, OWN_FINDINGS = the S5 code critic's file, PLAN_FILE).
  No S4 `critic-findings.md` appears there.
  **Over the cap: slices with remarks:** CONFIRMED (brief_pack.py:2026-2046 → `window_slice(n=)` → `remarks_of` → `case_concerns`,
  s5_plan.py:1092, :1297; printed at :1358-1364). **Windows are cut from the plan's tests:** CONFIRMED (controller.py:4524-4525
  docstring; `case_groups` at s5_plan.py:157-196 runs on `test_adjacency`). **UI cap default 1:** WRONG, it is 2 (B3).
- **G2 (the legacy brief carries no CC-n):** CONFIRMED by my own search. Grep (case-insensitive)
  `carried_concerns|case_concerns|remarks_of|accepted_rounds` over R/scripts/*.py. Non-test hits: critic_rollcall definitions;
  s5_plan :28-29, :1077-1092, :1133, :1146, :1297; gate_brief :2226, :2234; brief_pack :2566 (`_delta_tail`, plan blockers of a
  RESUMED plan or window, brief_pack.py:2561/2363). Positive control: the same call found the definition `s5_plan.py:1146`.
  None of these hits lies on a legacy brief path: `build` gives `legacy` no branch (brief_pack.py:4244-4256), and
  `_resumed`/delta runs only for `plan`/`window` (:4363).
  **`digests` read end to end** (brief_pack.py:1581-1615): it prints each EARLIER stage's `pipeline.stages[sid].digest` (or
  reason), shortened to `DIGEST_CHARS`, plus this stage's other dispatches' `returned_digest`. It names no file and no CC.
  The designer's estimate ("a legacy window may see the case critic's digest line (path to critic-findings.md)") does not hold:
  at most S4's stage digest prose appears, cut short. No carrier.
- **Did wave 1 change anything K2 owns?** s5_plan.py: 2 lines changed (a docstring in `_settled_lines`); nothing K2 owns
  changed. critic_rollcall.py, the rubric, both charters and role-rules.json: unchanged (diff --stat be2c988..5cc4f88 lists only
  brief_pack, controller, s5_plan). brief_pack.py `plan_dispatch_lines` DID change (FV1-4 N2): every exception text in it is now
  whole, via `_text_whole` (hunks at old :1907 and :1929 → new :2013, :2035). The K7 test pins this at 80/81/800 characters
  (test_brief_pack_s5_plan.py:575-582). K2 item 3's `_short(exc, 100)` is therefore against the rule now in force (A2). The
  6 KB brief ceiling comment was removed from `build`, and the S5 plan ceiling was renamed and re-based (B2).
- **Stale references a builder would trip on (plan → current):**
  - brief_pack: `plan_dispatch_lines` :1887-1949 → **:1993-2055**; author head :1898-1901 → **:2005-2007**; critic hint count
    :1905-1911 → **:2011-2017**; under-cap :1916-1919 → **:2020-2025**; over-cap :1920-1940 → **:2026-2046**; `plan_lines`
    :1970-1997 → **:2076-2103** (side-file wording :2101-2102); resumed window :2491-2502 → `delta_lines` **:2525** /
    `_delta_tail` **:2561**, blockers **:2566** (plan said :2482); `build` :4185-4199 and the chain :4187-4196 → chain
    **:4244-4256** (the legacy `elif` goes after :4256); `_s5_kind`'s `mode` call :1867 → **:1973**.
  - controller: :4499-4500 → **:4524-4525**; :4515 → **:4540** (default 2: :271); :4412 → **:4437**; :6525 → **:6553**
    (`_run_mode` **:6519**).
  - tests and registries: test_s5_plan.py:253/:258 → **:277/:279**; `DOORS_ONLY_BRIEF_MAX` (test-layers.json:347) →
    **`S5_PLAN_BRIEF_BYTES_MAX` test_brief_pack_s5_plan.py:541** (test-layers keep row still :345); test_s5_plan_grouping keep
    :4761 → **:4820**; test_role_rules :4564 → **:4623**; test_carried_concerns quarantine :7313 → **:7372**;
    `keep_fail_at_entry` :7038 → **:7097**; judgment-census s5_plan rows :881-890 → **:885-894** (`plan_dispatch_lines` still :60).
  - Unchanged and correct: s5_plan `case_concerns` :1146-1160, `render_slice` :1316-1365 (remarks :1358-1364), `grouping_hints`
    :1405-1433, `hint_rows` :1447-1457, `print_hints` :1460-1465, `--check` :1489-1496 (plan :1491); critic_rollcall
    `PARAMETRISE_TOKEN` :57, `_carries` :914-919; N5's :89, :793, :819, :832, :836, :990; qa-case-critic.md :41, :44;
    qa-case-designer.md :23, :46, :50; role-rules.json :26, :161; gate_brief :2226-2234 (its printing line is :3038).

### 2. Is G1 a real leak, or does another carrier hand the plan author the merge?

Real (with B3's qualification on how often partners land apart). I checked every candidate carrier for the plan author on
5cc4f88:
- the case files: `cases[:8]` of the scope (brief_pack.py:4289, 4348-4351). The case critic writes its `merge` into
  `work/test-cases/**/critic-findings.md`, never into a case file (qa-case-critic.md:44, :121).
- the S4 `critic-findings.md`: **NOT in the plan author's read list.** It is neither in S5 `inputs` nor in ROLE_FILES (above).
- the understanding brief: not an S5 input (`understanding.md` is only in the strategist's and case critic's ROLE_FILES,
  brief_pack.py:96-98).
- digests: no structured carrier (Q1).
- gate A text: gate_brief.py:3038 shows "Concerns carried to automation: TC-.." to the PERSON. It reaches S5 only through
  `decisions` (the person's own words), and only if the person retypes it.
- context bundle: context_bundle.py holds no `concern|critic-findings|case_concerns` (case-insensitive Grep, count 0; the
  control of the same call shape, `critic|BUNDLE` -i on the same file, counts 55).
The only structured carrier is `remarks_of`, and it reaches the plan dispatch only over the cap.

### 3. The owner's word vs K1, K2, N5

No contradiction found. Nothing writes `Archived` or `merged_into`, deletes a case or changes a reader of case status. The
merge stays an instruction: K2 hands it to the step that can act on it and adds no gate on the case side. The count of manual
cases is untouched, and K1 lowers it only as a side effect. K2 is aimed at identical automated steps, exactly the owner's
point 4. K1-E1 (two plan rows stay two cases) is consistent: the owner said the merge remains "an instruction for the
automator", and K1-E1 routes cross-row duplicates exactly there. It also respects "no reader changes" (`plan_row`). One note:
K1's new bullet puts a form detail (`P-<name>`) inside a `kind: craft` section, and RC2-3 (`roles-context/2`) moves procedure
out of craft sections (see A10).

### 4. F5 (a) against AR-29 / P27, P17, FR-4, t-723 E21; census

- AR-29 / P27: code computes the join (`merge_hints`, no verdict), and a role (the plan critic) decides blocker or not.
  Consistent. **P17:** the plan author is not forced to merge; one `apart_reason` answers. Consistent. **FR-4:** stops a
  silent pass (no answer); an informed answer passes. Consistent. **E21** ("never a delivery gate"): a plan-review blocker is
  not a delivery gate. Consistent.
- Two gaps. (i) The rubric clause is appended to the first bullet, whose own text says "A `remark`, never a `blocker` on its
  own" (code-review-rubric.md:17-21). One bullet would then carry both rules for neighbouring situations. Make it its own
  bullet (A6). (ii) Any non-blank `apart_reason` dissolves the blocker. A nominal reason ("x") is, by the same bullet, at most
  a remark (rubric :19-20: "an `apart_reason` that is not another setup, surface or fixture" → remark). Decide explicitly
  whether a bad reason answering a CASE-CRITIC merge is a blocker or a remark; otherwise the leak reopens through one word (A6).
- `merge_hints` as specified has no refusal site: no `raise`, and its rows only feed `print_hints` and counts (`--check` exit
  code untouched, s5_plan.py:1491-1504; `s5_precheck` hints never move `ok`, :4293-4299). **Census claim: right.**
  test_judgment_census.py:16-24 defines a unit as u1 (name matching `UNIT_NAME_RE`, :69: `check_*|rule_*|judge*|validate*|refuse*|
  *_check|*_errors|*_problems|check|run`), u2 (a judge call) or u3 (a refusal site). `merge_hints`, `parametrise_group`,
  `case_concern_lines` and `remark_lines` match none of these. `grouping_hints` has no row (census s5_plan rows :885-894).
  Condition: no `raise ValueError` inside them (a parse helper must return []).

### 5. F3 (a), K2 item 5: legacy placement

- Implementable: the chain sits at brief_pack.py:4244-4256, and a 4th `elif s5_kind == "legacy" and role == "qa-automator":`
  after the `unknown` branch is outside the `plan`/`window` branches, so K2-E10 holds. "After the chain ... `elif`" means
  "appended to the chain"; say so.
- `_s5_kind` returns `legacy` there: the dispatch's own S5 window record is live, so `s5_plan.mode` rule 2 gives LEGACY
  (s5_plan.py:405-406) before `run_mode` matters (`_s5_kind` passes no run_mode, brief_pack.py:1973; §9's analog is real
  but harmless here). It also returns `legacy` for "no record of this dispatch" (:1967-1968). That brief would get the
  concerns too, which is harmless.
- Twice? No: legacy has no slice and no delta (`_resumed` only for plan/window, :4363). Brief ceiling: no legacy-brief ceiling
  test found in test_brief_pack_s5_plan.py (Grep `legacy` -i: only k8 at :517-534, positive by its own hits). k8 asserts
  `written == [brief]`. Its story has no S4 round, so it stays green. **Sibling text left out:** the `build` comment at
  brief_pack.py:4197 ("`legacy` ... is the brief as it was, byte for byte") and the test docstring at
  test_brief_pack_s5_plan.py:14 become false. Name both in owns/siblings (A8). Scope noise and the split-pair residual: B4.

### 6. Edges: decided correctly?

- `apart_reason` is an EXISTING optional field: validator s5_plan.py:632-633, renderer :1354-1355, hint candidate :1401-1402.
  K2 does not introduce it. Correct.
- `placement: "plan"`: `render_slice` prints `remark['placement']` verbatim (:1361), so `remark_lines` prints it unchanged.
  Correct.
- A group of 2 ids both outside the plan → |G'| < 2 → no hint (row l). Correct: those cases are not automated in S5.
- `C.case_ids` on ids of another story: read by id form (contract.py:4257-4270), so a colliding bare id over-reports. That is
  the safe direction, as K2-E4 says. Correct.
- **Silent edge: area-keyed scope ids.** Plan case keys are controller scope keys (s5_plan.py:266-271, 319). An area story
  keys a case as `speakers/TC-009` (contract.py:4282-4290), while `parametrise_group` returns bare ids via `case_ids`. G ∩ plan
  cases = ∅ → no hint, which is a silent UNDER-report and the opposite of the stated error direction. Decide the match: compare
  bare ids of each plan key (`case_ids(key)`), or report the concern "not matched to a plan case" (A3).
- **Silent edge: `cfg`.** Item 7 calls `merge_hints(plan, concerns)` without `cfg`. `case_ids(cfg=None)` then reads the
  PROCESS's project (contract.py:4261-4263), not the story's. Pass `C.case_config(task_root)` (A3).
- **Wrongly decided: K2-E3 says "none carried".** On a receipt mismatch the plan brief would state "case critic's concerns:
  none carried" while a round WAS accepted and dropped. That reports an unknown as an empty fact (FR-41, AR-28). The spec's
  own error-direction paragraph says "never UNDER-carry silently", and stderr is not read (s5_plan.py:1119-1120 says so). The
  wording must distinguish "no round with concerns" from "N accepted round(s) carried nothing (findings changed after the
  receipt) - read <file>" (A4).
- **Vacuous "answered":** when no test holds any id of G' (both cases left as remainders), "every test row holding an id of G'
  has an apart_reason" is vacuously true → no hint. That is defensible (nothing is automated), but state it. The message
  template's `'no test'` then appears only in the mixed case (A7).
- K2-E10 invariant vs item 4: over the cap, the author gets each CC in the side file AND in the slices (unplaced ones in every
  slice). Same printer, but "no brief carries the same CC-n twice" does not hold literally. Reword (A11).
- K1 E1-E7: decided correctly as written. I did not check that `references/manual-evidence.md` names partitions (K1-E7) and
  leave it unverified.
- Temporal (K2-E9): fine. Unstated: an S4 rework after the plan was reviewed adds new CC-n. The plan is not refreshed by K2;
  the windows get them through C12. Acceptable, but write one line.

### 7. Reused functions in a more consequential role

- `_carries` through `parametrise_group`: behaviour is unchanged. I traced it against critic_rollcall.py:914-919: the current
  code folds whitespace (`" ".join(str(note or "").split())`), does a case-insensitive `re.search` of the escaped token (so the
  FIRST occurrence), and takes `set(partners) <= set(C.case_ids(rest, cfg=cfg))`. The spec's `parametrise_group` does the
  same, plus de-duplication and ordering, neither of which changes set inclusion. The "token-present" conjunct is redundant
  whenever partners are non-empty, and `_merge_concern_errors` never calls with empty partners (:933-935). Equivalent.
- `case_concerns`: the stated direction (over-carry allowed, never under-carry silently) is right, but K2-E3's wording breaks
  it (A4), and so does the area-key match (A3). A "parameterize" spelling (z) is not read, but the S4 exit refuses a `merge`
  without the exact token (:944-955). The S5 side may therefore rely on the token for `merge` rows. Correct.

### 8. Tests

- `keep_fail_at_entry` holds `test_brief_pack_s5_plan.py`: TRUE (test-layers.json:7094-7097). But the file is GREEN at 5cc4f88
  (my run: `213/213 ok`, exit 0). The before/after rule is workable, and it reduces to "every check green after". State that
  in the DoD so a builder does not lean on the exemption.
- Against docs/TESTING.md: the homes are keep files (test_brief_pack_s5_plan :345 `data_join`; test_s5_plan_grouping :4820
  `data_join`, "held by import"; test_role_rules :4623), and no quarantined file is touched. Good. But 17 rows (a-q) is one row
  per edge and key, the "квитанция на ключ" pattern (TESTING.md:96, :55: "теста на ... ребро спеки или ключ DoD" no longer).
  - Row **g** ("byte-equal to its pre-change text") is the forbidden «Как раньше» kind (TESTING.md:97).
  - Rows e, p (internal exceptions) and m, o (token and id parsing, already the job of `_carries` / `case_ids`) are internal
    boundaries (CLAUDE.md rule 11: "an internal boundary gets no test").
  - Keep the rows that fail BEFORE the change (TESTING.md:56): a and b (under the cap, author and critic), f (legacy), d (empty
    outcome). Keep h-l and q as ONE parameterised table for `merge_hints`, plus the B1 row (the critic head shows both lines).
  - Also the budget: test lines ≤ product lines (TESTING.md:115).
  These are amendments (A5), not blockers.

### 9. Ownership

- K2 vs N5 in critic_rollcall.py: disjoint. K2: new `parametrise_group`, `_carries`. N5: `parse_rollcall` :89,
  `parse_merge_candidates` :793, `_read_rounds` :819, `_level_errors` :972, and the deletion of `_has_note_column` :836, whose
  only caller is `_read_rounds` :832 (Grep `_has_note_column\(`). Neither calls the other's functions. TRUE.
- K1 vs RC1-2: the proposed home is right. TQ2's batch is «ожидает» and not taken (batch file :3). onboarding-forge/1 is «в
  работе», dev1, 12.11 (:3), so it is frozen, and RC1-2 is at :44. The «Ход» pointer is a legal edit there. X4 (RC2-3,
  roles-context/2 batch :30) is correctly identified.
- Functions K2 touches (for the Lead's cross-branch check): brief_pack.py `plan_dispatch_lines`, new `case_concern_lines`,
  `build` (one `elif`; plus the comment at :4197); s5_plan.py new `remark_lines`, `render_slice`, new `merge_hints`,
  `hint_rows`; critic_rollcall.py new `parametrise_group`, `_carries`. Tests: test_brief_pack_s5_plan.py (incl. docstring :14),
  test_s5_plan_grouping.py. With B1's fix, `plan_dispatch_lines` changes in its critic branch too.

### 10. Feasibility

- K2's core (hand the plan dispatch the CC side file, both roles, both cap branches) is the smallest change that closes G1.
  "Always hand the plan dispatch the slices" is not simpler: under the cap it duplicates the plan the author must edit, and
  it still would not reach the legacy road. `merge_hints` plus the rubric clause is an extra layer, but cheap, AR-29-clean,
  and the only thing that makes "unanswered" visible to the critic without a manual cross-check. Keep it, once B1 is fixed.
- An alternative survivor the spec should name as rejected or queued: let the window CUT keep merge groups together
  (`case_groups` adjacency gains the critic's merge edges; `split_windows` likewise for legacy). That is ONE mechanism for
  both the planned and the legacy road (P31) and would close B4's residual. It costs window size (over_cap) and changes the
  legacy cut "byte for byte", so it is a fork for the Lead, not a requirement here.
- Recommendation: dispatch K1, K2 and N5 as cut, AFTER the Lead edits B1-B4 and A1-A11 into the spec. No re-cut. No second
  critic-on-plan pass is needed unless the Lead takes the cut-level alternative (that changes architecture; PROJECT.md new-idea
  step 6).

---

## Small amendments (Lead may apply directly)

- A1. Replace every stale reference with the current line (list in Q1).
- A2. K2 item 3, exception head: `_text_whole(exc)`, not `_short(exc, 100)` (FV1-4 N2, brief_pack.py:443-446, :2013, :2035).
- A3. `merge_hints`: pass `cfg=C.case_config(task_root)` from `hint_rows`; decide the area-key match rule (Q6).
- A4. Word the receipt-mismatch outcome so it is not "none carried" (Q6, FR-41).
- A5. Cut the acceptance rows to the defect rows plus one table (Q8); drop g, e, p, m, o.
- A6. The rubric clause becomes its own bullet; decide blocker or remark for a nominal `apart_reason` that answers a
  case-critic merge.
- A7. State the vacuous "answered" case (no test holds any id of G').
- A8. Put brief_pack.py:4197 (comment) and test_brief_pack_s5_plan.py:14 (docstring) in owns/siblings.
- A9. DoD: the file is green at entry, so after the change every check must be green.
- A10. K1: keep `P-<name>` (form) out of the craft bullet, or accept that RC2-3 may move it (X4). Note that a move into
  `process` meets `process_ratchet_tokens` with slack 0 (role-load.json:28, 12079 = measured 12079).
- A11. Reword K2-E10's invariant to match item 4's over-cap double print.

## Class completeness (SIBLING_MAP)

- axis 5 (stage twins): plan dispatch vs window road, both now fed by the same `case_concerns` / `remark_lines`. Covered by
  K2. The legacy road is the open twin (B4).
- axis 18 (ratchets: a raise in the diff that adds the site): three ratchets at zero headroom (B2), not covered.
- axis 32 (where judgment lives): the F5 blocker stays with a role. Covered; wording gap A6.
- axis 34 (one road): under vs over cap is unified by K2; legacy only partly (B4).
- Beyond the map: none requested.

## DUPLICATION AND CONSISTENCY / CODE QUALITY / ONE ROAD (critic-diff-brief items 6, 7, 12, as plan checks)

- Duplication: the spec already removes duplication (one token reader `parametrise_group`, one remark printer `remark_lines`).
  None found beyond B1 (two meanings under one count). Grepped: `hint_rows|grouping_hints|print_hints` (callers: brief_pack
  :2011, s5_precheck :4296, :4688, s5_plan :1491), `PARAMETRISE_TOKEN` readers (only `_carries`).
- Code quality: B1 (the contract change to `hint_rows`'s `why`), A2.
- One road (P31): over/under cap unified; legacy residual B4 is owed a fix or a named node with its owner (Lead opens it).

## Trail

Read on read-main 5cc4f88: the plan (whole); brief_pack.py 70-119, 443-446, 1581-1615, 1945-2104, 3550-3562, 4173-4402;
s5_plan.py 128-217, 259-328, 384-411, 890-894, 1077-1201, 1245-1504; critic_rollcall.py 895-964 (+ def/`note_col` grep);
controller.py 271, 414-436, 4287-4320, 4425-4445, 4518-4552, 6515-6534; s5_precheck.py 4285-4309; contract.py 2845-2866,
3302-3327, 4257-4302; code-review-rubric.md 1-40; qa-case-critic.md 36-49; qa-case-designer.md (grep of :13-80);
role-rules.json :26, :161; role-load.json :2, :14-15, :28-29; test-layers.json 340-365, 4760-4830, 7080-7128;
test_brief_pack_s5_plan.py 505-602; test_s5_plan_grouping.py 218-260; test_judgment_census.py 12-41, :69;
judgment-census.json head, :59-60, :237-244, :885-894; stages.json S5 entry; docs/TESTING.md (whole); SIBLING_MAP.md headings;
batch files test-code-quality/2 :1-4, onboarding-forge/1 :1-4, :44, roles-context/2 :30.
Searches (case-insensitive where a negative was concluded, positive control named): the G2 grep (control `s5_plan.py:1146`);
carriers `test-cases/.*critic-findings|approve_with_concerns|carried to automation|parametrise into one test` over the package
(hits listed, none on the S5 plan or legacy path); context_bundle.py `concern|critic-findings|case_concerns` → 0 (control
`critic|BUNDLE` → 55); `legacy` in test_brief_pack_s5_plan.py; `hint_rows|grouping_hints|print_hints|merge_hints`;
`\.mode\(|def _run_mode`; `def _text_whole|FV1-4 N2`; wave-1 diff `git diff be2c988 5cc4f88 --stat` plus hunks of brief_pack.py.
Not read: the old draft's N5 text :290-302 beyond the line references the plan restates (N5 line refs re-checked on 5cc4f88);
`references/manual-evidence.md` (K1-E7 left unverified).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1: K2 item 7 merges merge_hints into hint_rows, but the plan critic head line (brief_pack.py:2011-2017) counts them as grouping hints and says 'never a blocker on its own', contradicting F5(a); the new why also drops the computed grouping count",
    "B2: ratchets at zero headroom on 5cc4f88 - S5_PLAN_BRIEF_BYTES_MAX measured 9520 of 9520, qa-case-designer 13316 of 13320, qa-case-critic 18296 of 18296; K1 and K2 are certain to exceed; the spec must name the raises (AR-20) or decide compensations; '13320 + slack' misreads role-load.json:2",
    "B3: G1 fact wrong - UI window cap default is 2 (controller.py:271), not 1; pack_windows packs ungrouped partners first-fit, so 'they land apart whenever the plan did not group them' is overstated; correct section C.2, the L4 answer and the F5 rationale",
    "B4: F3(a) does not deliver 'every road' - the legacy cut is by cases (controller.py:4428-4443), the whole-story side file goes to every legacy window, and split partners still cannot merge; decide scope filtering and name the residual or a node"
  ],
  "class_completeness": "axis 5 stage twins: plan and window roads unified by K2, legacy twin open (B4); axis 18 ratchets: three ratchets at zero headroom need a named raise in the same diff (B2); axis 32 judgment: F5 blocker stays with the plan critic, wording gap A6; axis 34 one road: under/over cap unified, legacy residual owed a fix or a named node (B4). Nothing beyond the map requested.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261113-tq2-1-revision-option-c-spec.md",
      "read-main 5cc4f88: scripts/brief_pack.py 70-119, 443-446, 1581-1615, 1945-2104, 3550-3562, 4173-4402",
      "read-main: scripts/s5_plan.py 128-217, 259-328, 384-411, 1077-1201, 1245-1504",
      "read-main: scripts/critic_rollcall.py 895-964",
      "read-main: scripts/controller.py 271, 414-436, 4287-4320, 4425-4445, 4518-4552, 6515-6534",
      "read-main: scripts/s5_precheck.py 4285-4309",
      "read-main: scripts/contract.py 3302-3327, 4257-4302",
      "read-main: references/code-review-rubric.md 1-40; agents/qa-case-critic.md 36-49; references/role-load.json",
      "read-main: scripts/tests/test-layers.json 340-365, 4760-4830, 7080-7128; test_brief_pack_s5_plan.py 505-602; test_s5_plan_grouping.py 218-260; test_judgment_census.py 12-41",
      "read-main: scripts/tests/fixtures/judgment-census.json; references/stages.json S5",
      "docs/TESTING.md; docs/SIBLING_MAP.md headings; tools/critic_verdict.schema.json",
      "read-main plans: test-code-quality batch-2 head, onboarding-forge batch-1 head and :44, roles-context batch-2 :30"
    ],
    "reruns": [
      {
        "command": "python -B read-main/ai-packages/qa-factory/scripts/tests/test_brief_pack_s5_plan.py",
        "result": "exit 0; 213/213 ok; RATCHET S5_PLAN_BRIEF_BYTES_MAX 9520 (ceiling 9520, zero headroom)"
      },
      {
        "command": "python -B read-main/ai-packages/qa-factory/scripts/role_load.py --all --json",
        "result": "qa-case-designer tokens 13316 (ratchet 13320, process 12079); qa-case-critic tokens 18296 (ratchet 18296); both verdict within"
      },
      {
        "command": "git -C read-main diff be2c988 5cc4f88 --stat on brief_pack/s5_plan/controller/critic_rollcall/rubric/charters/role-rules",
        "result": "brief_pack 908, controller 73, s5_plan 2 changed lines; critic_rollcall, rubric, charters, role-rules unchanged; plan_dispatch_lines exception texts now _text_whole (FV1-4 N2)"
      }
    ]
  },
  "fixes": [
    "B1: keep merge hints out of the single grouping count; give plan_dispatch_lines its own merge-hint line naming the blocker rule; restate hint_rows' why contract; add one critic-head row",
    "B2: name in the spec the raises of qa-case-designer, qa-case-critic and S5_PLAN_BRIEF_BYTES_MAX (re-measured at build), or decide the compensations (shorter K1 bullet; no 0-concern line)",
    "B3: correct the UI cap default (2) and the 'land apart whenever' claim in section C.2, section 9 L4 and the F5 rationale",
    "B4: filter the legacy side file to the window's scope plus global concerns through one placement rule, and write the split-pair residual as an edge with a queued node or the owner's word; correct the changelog 'every road'",
    "A1-A11 as listed in the review (stale lines, _text_whole, cfg and area keys, receipt-mismatch wording, test rows per TESTING.md, rubric bullet, vacuous answered, legacy comment siblings, green-at-entry DoD, craft/process placement, E10 wording)"
  ]
}
```

# td-15 story local-1-0108: judging the four red facets R1..R4

Critic (Opus), 2026-11-11. Read-only work in `D:/ws1/wt-td\15-5-3b` (branch td/15-5-3b, HEAD 0a4f8fec9). I did not run the
scenario test file or any selftest. I ran one narrow probe: today's `branch_accounting` on two scratch copies, one of the
UNSCRUBBED source root and one of the fixture, both under a scratch project that carries the decoded recorded config. The source
archive was only read and copied, never written.

## Verdict lines

- **R1: (b)** - commit fec3f4593 (TR2-7, today) made the S1 exit refuse a diff file at `current-code`, but left the S1 hand-over form
  saying `work/impl-diff.txt` is `required: true # absent only when implementation_source is ungrounded`. The S2 brief line also
  still says "(absent when ungrounded)". So today's package tells the scout and the tester that a file is required when its own exit
  forbids that file. The walker read the form literally and caught the contradiction.
- **R2: (d) for the facet; 22 of its 23 parts are (c).** Part 1 ("an exclusion nobody decided", 10 U-ids) is a real catch. The register
  attributes the exclusion to "person's scope decision" without quoting the person, and the person never named it. WG1-1
  (d55fa3caf, 0.10.9) was made from this very line. Parts 2-23 (57 unhomed units and the `localhost` Attachments row) are produced by
  the capture. On the unscrubbed source, today's code finds 0 unhomed units and accepts the attachment row.
- **R3: (d)** - TS-24 (a P0 money row) and TS-25 were sent to the `manual-agent` rung with `rung_basis.kind: not_measured` ("no
  injection seam was probed"). TS-26 does the same through its `if_answered` patch. The P19 ladder says that not trying the lower rung
  is no reason to climb. 0.10.8 accepted it. RN1-13 (350c3c300, 0.10.9) was filed from this run and now refuses it, which is the right
  behaviour.
- **R4: (d)** - no waiver and no person's word for the design review. The order rule did not exist in 0.10.8. Designer-3 rewrote
  TC_021/022/024 after the gate A answers (seq 45-47), and no case critic ran after it. Gate A was approved at seq 48 on critic-2's
  receipt (seq 40). RN1-20 (08e788add, 0.10.9) was filed from this run and now refuses that. It is the right behaviour.

Package bugs: **1** (R1). Real catches of the scenario layer: **3** (R2 part 1, R3, R4).

---

## R1 - S1/handed: `work/impl-diff.txt is named by the form and absent`

**Class (b): a defect of today's package text. TR2-7 did not reach the hand-over form or the S2 brief.**

Evidence:
- The run is `current-code`. The source `pipeline.json:7` has `"implementation_source": "current-code"`. `ls work | grep -c impl` on
  the source gives `0`: no diff file was ever written. Positive control with the same form: `grep -rln impl-diff` over the source finds
  the S1/S2 forms and briefs.
- Today's contract says a `current-code` story writes NO diff file:
  - `scripts/stage_done.py:152-168` (`current_code_diff_refusal`): "a story grounded in the current code writes no diff file";
  - `agents/qa-scout.md:88`: "With `current-code` write no `work/impl-diff.txt`, no stub there: the exit refuses it";
  - `skills/qa-story/phases/s1.md:35`: the same rule;
  - `references/stages.json:44-47`: `required_outputs` of S1 do not include it.
  - The rule came in with `fec3f4593 2026-11-11 packages: TR2-7 the S1 exit refuses a stub impl-diff.txt at current-code (B-8)`, which
    is an ancestor of HEAD. `git show 658ceac29:.../stage_done.py | grep -c "def current_code_diff_refusal"` gives `0`; HEAD gives `1`.
- Today's texts a role reads still say the opposite:
  - `handoffs/s1-scout-to-tester.yaml:27-29`: `- path: work/impl-diff.txt` / `required: true # absent only when implementation_source
    is ungrounded`. The same file also asks for `implementation.diff.path/files/hunks/bytes` (`:46-51`) and for the claim
    `diff_is_complete_not_truncated` (`:94`), all for a file the exit forbids. `git log` on that file: the last edits (3a9c6b4d0,
    3031325af, cac05f48b) are all older than TR2-7.
  - `scripts/story_run.py:9689`, the S2 brief line: `impl-diff.txt: {base}work/impl-diff.txt (absent when ungrounded)`.
  - Sibling `handoffs/s2-tester-to-strategist.yaml:38-40` asks for `handed`/`read` hunks of `work/impl-diff.txt`. That one has no
    `required` flag, and the real tester filled it as `handed: 0 (no diff; implementation_source current-code)` (fixture
    `work/handoffs/S2-qa-requirements-tester-1.yaml:39-41`). This shows a role had to resolve the contradiction by itself.
- What breaks for a real user, on every `current-code` story (every LOCAL story with no MR):
  - the scout's form demands a required input and diff sizes that its charter forbids it to produce;
  - the S2 tester is told the implementation diff "in full" is a required input, and it does not exist.
  - This breaks FR-37 (a path named in text a role reads is a path the code writes), FR-10 and AR-10. No refusal comes of it today
    (`story_step start` of S2 passed in the same facet), only friction and a false instruction.
- The walker side: `scenario_walk.door_handed` (`scripts/tests/scenario_walk.py:399-423`) reads `required: true` from the RECORDED form
  copy. That form was written by package code at dispatch time from the 0.10.8 template, so even after the package fix this story's
  form still says `required: true`. See W-1 below.

## R2 - S2/accepted: branch_accounting, 23 parts

**Class (d) for the facet: one real catch. The other 22 parts are a capture artifact (c), established by experiment.**

The builder's open question ("does the scrub move the unit-id hashes?") is settled by this experiment:
```
python -B scripts/branch_accounting.py --unhomed --task LOCAL-1 --task-root <scratch>/src/qa-factory/artifacts/LOCAL-1 --project-root <scratch>/src
  -> exit 0, "page 1 of 1", 0 lines with U-        (the UNSCRUBBED source root)
python -B scripts/branch_accounting.py --unhomed ... --task-root <scratch>/fix/qa-factory/artifacts/LOCAL-1 --project-root <scratch>/fix
  -> exit 0, 57 lines with U-, first: U-95793e7df256 (LOCAL-1 description): "Existing stories, ... https://example.invalid/49" has no home
in-process branch_accounting.s2_check(<root>):
  src -> unhomed 0, blocks 1: ["... U-a929b15ff589, ... U-4e59f1300e2c: an exclusion nobody decided - fix: ..."]
  fix -> unhomed 57, blocks 3: [the same exclusion block; "21 part(s) of the story's text have no home"; "1 file(s) of the story have
         no row in `## Attachments`: https://example.invalid/20: localhost ..."]; notes include "U-beb44ce1686c: no unit has this id now
         (the text changed?)"
```
The two runs use the same command and the same config, and differ only in the root, so each serves as the other's control. The
fixture gives the builder's 57, which confirms the invocation.

**Part 1, a real catch (d).**
- Register line 84, identical in source and fixture: `| U-a929b15ff589, ... U-4e59f1300e2c | excluded: raising a cart line quantity is
  a cart edit, not an add-to-cart path (person's scope decision, s1-conflict-20261101-234118) |`.
- What the person actually said (`state/words/s1-conflict-20261101-234118.txt`): "Scope: только функционал попадания товара в корзину
  (все пути добавления и сценарии, где он используется)". They never mentioned raising a cart line's quantity. "Scenarios where it is
  used" can just as well be read to include it, so the exclusion is the role's inference, signed with the person's name.
- Today's rule: `d55fa3caf 2026-11-02 18:37 WG1-1 + RN1-12 + RN1-17.0: an inferred exclusion is asked at the S2 halt`.
  `git show 658ceac29:.../branch_accounting.py | grep -c "an exclusion nobody decided"` gives `0`; HEAD gives `2`. It is an ancestor
  of 878641cc9 (release 0.10.9) and not of 658ceac29 (0.10.8).
- The node row `plans/piles/release-next/batch-1-release-0-10-9.md:95` (WG1-1) cites this exact place: "Разбор живого прогона LOCAL-1
  ... `requirements-register.md:84` ... «person's scope decision»".
- What 0.10.8 missed: it let a scope exclusion attributed to the person pass without the person's words (P13, P20, FR-8). Today's
  refusal is right: either quote at least 3 of their words, or ask a Q<n> at the S2 halt.

**Parts 2-22 (21 parts / 57 units), capture artifact (c).**
- A unit id is `"U-" + sha256(normalize(text))[:12]`, and a comment group is `"G-" + ...` over the whole comment body
  (`scripts/branch_accounting.py:209-224`). The register hard-codes those ids, computed on the original ticket text.
- The scrub's `ticket-key` and `example-url` rewrites change that text: "REF-10, REF-19", "https://example.invalid/49". Every unit that
  holds a rewritten token moves its id, and every comment group whose body holds one moves its G-id. The source register's groups are
  G-30d13d9ff3a8 / G-eca312b6401b / ...; the walk reports G-b6c3203ddd4f. A unit with no token of its own (U-342069a44e46) still loses
  its home, because its GROUP id moved.
- The capture's follow remaps only whole-file sha256 values (`tools/story_capture.py:308-336`). Content-addressed 12-hex sentence ids
  are not followed.

**Part 23 (`localhost` Attachments row), capture artifact (c).**
- The source register row is `| localhost | XPANBFLFA-140 | not_an_expectation | ...`; the fixture has `| localhost | REF-1 | ...`.
- The source's key comes from `source_inventory._key` = `canonical_ref.rsplit("/browse/", 1)[-1]` (`scripts/source_inventory.py:2673-2674`),
  and the source `canonical_ref` is `https://example.org/browse/<KEY>`.
- The `example-url` rewrite (`tools/story-scrub-rules.json`, rewrites[0]) replaces the WHOLE URL with `https://example.invalid/<n>`. That
  drops the `/browse/<KEY>` tail, so the key becomes the bare URL and no longer matches the register's `REF-1`.
- The same effect shows in the notes: the source lists left-out "RUN-2026, TC-001..."; the fixture lists "https://example.invalid/1, ...".

## R3 - S3/accepted: TS-24, TS-25, TS-26 rest on `not_measured`

**Class (d): a real catch.**

Evidence:
- The rows on file (fixture `work/test-plan.json`; the source plan holds the same 3 `not_measured`: `grep -c not_measured` gives 3 in
  both):
  - `TS-24 manual-agent, priority P0, rung_basis {"kind":"not_measured","ref":"no injection seam was probed at S3"}`;
  - `TS-25 manual-agent, P2`, the same basis;
  - `TS-26 unverifiable`, `if_answered.Q9.*` sets `manual-agent` with `not_measured` "no expiry seam was probed at S3".
- The refusal comes from `scripts/branch_accounting.py:1502-1523` (`_rung_problem`): a kind in `rung_kinds` but not in
  `rung_kinds_accepted` (`references/branch-accounting.json`) is refused.
- Which commit: `350c3c300 2026-11-03 RN1-13: a manual rung rests on a probe or an environment reason, not on not_measured (D5-A, t-1701)`.
  It is not an ancestor of 658ceac29 and it is an ancestor of 878641cc9. `git show 658ceac29:.../branch_accounting.py | grep -c
  rung_kinds_accepted` gives `0`; HEAD gives `1`. CHANGELOG line 179 records it.
- Origin: `plans/piles/release-next/findings/20261102-lestnica-p19-ne-izmerena-ruchnaya-stupen-po-not-measured.md`, "from the LOCAL-1
  run". The steps of TC_022 are API calls plus one click, and TC_023 itself prescribes a Playwright route intercept. So the lower rung
  was reachable and was never tried. The manual check later never reached the stand (RN1-10), and the red that the code predicts
  (R-24, money) was never obtained.
- What 0.10.8 missed: P19 (the owner's principle of 30.09) was already in force, yet the gate accepted "not tried" as a basis for a
  higher rung. Today's refusal is right: it names the row and both ways out (`measured` / `impossible`).
- Caveat (as W4 in cart-1): the facet is walked on the final plan bytes, not on the S3-3 receipt. The three rows' `rung_basis` was
  written by the strategist, and no later stage writes it, so the class stands.

## R4 - gateA/decision: TS-22, TS-24, TS-25 "the critic has not reviewed the cases as they stand"

**Class (d): a real catch. There is no waiver; it is a 0.10.8 gap that today's code closes.**

What the recorded events show (source `state/events.jsonl`; times UTC):
```
38 23:37:53 dispatch S4 qa-case-critic ; 39 S4-qa-case-critic-2 running ; 40 23:41:07 accept
41-44 S3-qa-test-strategist-3 (TS-24..26 question branches), accept 43
45 00:27:19 dispatch S4 qa-case-designer, reason "the person's gate A answers (state/words/gate-a-answer-1.txt) change the cases: TC_021 Then 1 ..."
46 S4-qa-case-designer-3 running ; 47 00:31:46 accept
48 00:34:37 decision gate A approved
```
No `qa-case-critic` dispatch comes after seq 47; seq 38 is the positive control of the same form.

How the run passed gate A:
- `state/passed-by-person.jsonl` holds ONE row: S5, `S5-qa-code-critic-14`, probe_gap. Nothing for gate A or for the design review.
- The decision event (seq 48) carries `authorization_source` = the text of `gate-a-decision.txt` ("approve", the R-/Q- tokens,
  vcs-1, case_environment-1..5). There is no design-review waiver. Its pipeline snapshot has `stage_overrides: null`.
- The person's words in `gate-a-answer-1.txt` ("Пробелы в плане (TS-7, TS-23..26): принять ...") accept plan GAPS. They do not waive
  the case review.
- In 0.10.8 the order rule did not exist: `git show 658ceac29:.../controller.py | grep -c review_is_stale` gives `0`; HEAD gives `3`.
  It came in with `08e788add 2026-11-03 t-1725 D1-D: a design review is void when the case designer was accepted after the case critic
  (RN1-20, R6)`. Not in 0.10.8, in 0.10.9 (878641cc9). CHANGELOG line 394 records it.
- Code: `scripts/controller.py:2827-2852` (`accept_order`, `review_is_stale`) and `:2932` (the refusal text).
- Origin: `plans/piles/release-next/findings/20261102-kvitanciya-recenzii-perezhivaet-novuyu-versiyu-avtora.md`, from this run. It
  records that `gates.A.design_reviews` named critic-2 as the reviewer of TS-22/24/25/26 for case versions that critic never saw.

What 0.10.8 missed: the receipt of a case review survived the author's new version (FR-18, AR-28). The person approved cases at gate A
that no critic had reviewed. Today's refusal is right, and today's repair runs the critic again before the person sees the gate
(CHANGELOG 394).

Note, not established and not load-bearing: the finding lists TS-26 among the rows that cite critic-2, but today's refusal names only
TS-22/24/25. TS-26 is an `unverifiable` row with a conditional branch, and probably not a critical row under `_design_review_problems`.
I did not trace it.

---

## What to do

### Amendment rows to write (owner of the decision: Lead; `fixtures/stories/local-1-0108/expected.json`)

Important: today the walker reads only `expected.json` `stages`. `scenario_walk.py` reads no `amendments` key: `grep -i amend` finds
only the docstring line 5, and the positive control `names` is found at `:485`. An amendment row by itself is inert. Each row below
needs the matching edit of `stages.<stage>` (`outcome`/`decision` and `names`), or the walker change W-2.

1. R2, but ONLY after capture change C-1/C-2 (with the capture as it is, a bare `refused` would also absorb 22 capture parts):
```
{"stage": "S2", "field": "outcome", "recorded": "accepted (0.10.8, events seq 14)", "expected": "refused", "names": "an exclusion nobody decided", "why": "WG1-1 (d55fa3caf, 02.11.2026 18:37, shipped 0.10.9): an exclusion attributed to the person's word quotes their words or is asked; register line 84 cites 'person's scope decision' without the person naming it - a real catch filed from this run", "ref": "docs/tasks/specs/reviews/td-15-local-1-0108-reds.md", "accepted_by": "Lead, <date>"}
```
2. R3:
```
{"stage": "S3", "field": "outcome", "recorded": "accepted (0.10.8, events seq 43)", "expected": "refused", "names": "not trying the lower rung", "why": "RN1-13 (350c3c300, 03.11.2026, shipped 0.10.9): a manual rung rests on a probe or an environment reason, not on not_measured; TS-24 (P0), TS-25, TS-26 (if Q9) - a real catch filed from this run", "ref": "docs/tasks/specs/reviews/td-15-local-1-0108-reds.md", "accepted_by": "Lead, <date>"}
```
3. R4 (`names` is checked for a decision facet only after W-3):
```
{"stage": "gateA", "field": "decision", "recorded": "approve (0.10.8, events seq 48)", "expected": "refused", "names": "has not reviewed the cases", "why": "RN1-20 (08e788add, 03.11.2026, shipped 0.10.9): a design review is void when the case designer (S4-qa-case-designer-3, accept seq 47) was accepted after the case critic (S4-qa-case-critic-2, seq 40); no waiver in the root - a real catch filed from this run", "ref": "docs/tasks/specs/reviews/td-15-local-1-0108-reds.md", "accepted_by": "Lead, <date>"}
```
No amendment for R1: it is a package bug. The facet stays red until B-1 and W-1 land.

### Bugs to file (factory class)

- **B-1, "a refusal added at an exit leaves the hand-over form and the next role's brief stating the old requirement".** TR2-7
  (fec3f4593) changed what `current-code` produces, but not what the forms and briefs say about it.
  - Fix in one commit (producer and readers together, AR-22): `handoffs/s1-scout-to-tester.yaml:29`, e.g. `required: false  # present
    only when implementation_source is diff; with current-code or ungrounded no file is written`, and the `implementation.diff`
    block / `diff_is_complete_not_truncated` claim conditional on `diff`;
  - `scripts/story_run.py:9689` "(absent unless implementation_source is diff)";
  - `handoffs/s2-tester-to-strategist.yaml:38` the same condition.
  - FR-37, FR-10, AR-10. Sibling axis: forms (`handoffs/*.yaml`) and phase/charter text of the same rule.

### Tool / walker changes (scenario layer, TD-15)

- **C-1 (capture), content-addressed ids follow the scrub.** After the rewrite, `story_capture.py` re-keys every `U-<12hex>` and
  `G-<12hex>` token in the captured files. Map: for each snapshot (`work/ticket-snapshot.json`, kept `work/sources/*/ticket.json`),
  run `branch_accounting.snapshot_units` on the source bytes and on the scrubbed bytes, pair the units by position, and compute
  `unit_id`/`group_id` on both sides. The pairing is the same split and the same order, because the rewrite never touches a sentence
  boundary; the tool should refuse and name the snapshot when the counts differ. If two scrubbed texts collide on one id, the tool
  refuses. Without C-1, every story whose ticket text holds a corporate key or URL arrives with a register that the S2 exit cannot
  read.
- **C-2 (capture), the `example-url` rewrite keeps the key tail.** A URL of the form `.../browse/<KEY>` must keep `/browse/<KEY>`, for
  example `https://example.invalid/browse/<KEY>` with `<KEY>` then mapped by `ticket-key` to the same `REF-n` as everywhere else.
  Otherwise `source_inventory._key` returns a URL where the register says `REF-n`. This alone produced part 23 and the "left out:
  https://example.invalid/1" notes.
- After C-1 and C-2, re-capture and confirm `branch_accounting.s2_check` on the fixture gives `unhomed 0, blocks 1` (as on the source),
  then write amendment 1.
- **W-1 (walker), a code-written form is judged by today's template.** `door_handed` should take the `required` flags from today's
  `handoffs/<contract>.yaml` (the form's `contract:` line) and the concrete paths from the recorded form. A recorded form carries the
  template text of the package that printed it.
- **W-2 (walker), apply `amendments`.** `_run_facet` should overlay `expected.json` `amendments[]` (`field` gets `expected`, plus
  `names`) on `stages[stage]`. Otherwise the amendment rows required by spec A.2 are decoration, and an edit to `stages` loses the
  recorded value.
- **W-3 (walker), `names` on decision facets.** `_run_facet` checks `names` only for `accepted`/`refused` (`scenario_walk.py:485`). The
  decision branch (`:500-502`) compares only `decision` and `tokens`, so an amended `refused` gate decision cannot pin WHICH refusal it
  is.

### Real catches (the scenario layer found what 0.10.8 let through)

1. R2 part 1: a scope exclusion signed with the person's name that the person did not make (WG1-1).
2. R3: a P0 money row and two others sent to manual by "not tried" (RN1-13).
3. R4: gate A approved cases that no critic had reviewed after the designer's last round (RN1-20).

All three were already found by the manual analysis of this run (t-1666/t-1671/t-1672) and fixed in 0.10.9. The scenario layer now
reproduces them mechanically, and that is its value here.

### Notes on the builder's report

- R-2's "Observation, not established" pointed in the right direction. It is now established by the experiment above.
- R-4's "how it passed is NOT established" is now established: there was no waiver.
- R-3's "possibly a rule added after 0.10.8" is confirmed (350c3c300).

## Trail

Read:
- `docs/tasks/specs/reports/td-15-5-3-report.md`; `../15-5-2/docs/tasks/specs/reviews/td-15-cart-1-reds.md`;
  `docs/tasks/specs/td-15-scenarios-quarantine.md` (170-209)
- `scripts/tests/scenario_walk.py` (360-547); `scripts/branch_accounting.py` (205-429, 1480-1523, 2580-2617);
  `scripts/stage_done.py` (145-170); `scripts/controller.py` (2827-2860, grep 2932); `scripts/story_run.py` (9680-9695)
- `handoffs/s1-scout-to-tester.yaml`, `handoffs/s2-tester-to-strategist.yaml` (36-42); `references/stages.json` (30-52),
  `references/artifact-writers.json` (28-45); `agents/qa-scout.md:88`; `skills/qa-story/phases/s1.md` (grep)
- `tools/story_capture.py` (grep 28, 308-336); `tools/story-scrub-rules.json`; `scripts/source_inventory.py:2673-2674`
- CHANGELOG lines 179, 394 and its headings
- plans: release-next batch-1 rows RN1-13, RN1-20, WG1-1; findings `20261102-kvitanciya-...`, `20261102-lestnica-p19-...`
- source root: `pipeline.json` (7, 576), `state/events.jsonl` (seq 1-50 summarised, seq 48 in full), `state/passed-by-person.jsonl`,
  `state/words/{gate-a-decision,gate-a-answer-1,s1-conflict-20261101-234118,s1-20261101-233259,s5-branch-accounting}.txt`,
  `work/handoffs/S1-qa-scout-1.yaml`, `work/requirements-register.md` (60-112, 160-170), `work/source-inventory.json` (canonical_ref),
  `work/test-plan.json` (grep), `state/config-at-start.json` (decoded)
- fixture: `expected.json`, `work/requirements-register.md` (84, 167), `work/test-plan.json` (TS-24..26),
  `work/handoffs/S1-qa-scout-1.yaml`, `work/handoffs/S2-qa-requirements-tester-1.yaml` (39-41)

Git: `log -S` for `def review_is_stale`, `the critic has not reviewed the cases as they stand`, `not trying the lower rung`,
`an exclusion nobody decided`, `def current_code_diff_refusal`, `absent only when implementation_source`;
`merge-base --is-ancestor` of 08e788add, 350c3c300 and d55fa3caf against 658ceac29 (0.10.8) and 878641cc9 (0.10.9); fec3f4593 against
HEAD; `git show 658ceac29:` greps with HEAD controls (review_is_stale 0/3, rung_kinds_accepted 0/1, an exclusion nobody decided 0/2,
def current_code_diff_refusal 0/1, positive control `def unit_id` in 0.10.8 = 1).

Process notes: I copied the source `work/`, `state/` and `pipeline.json`, and the fixture `work/` and `state/`, into the session
scratchpad, together with a decoded `config.json`. One Bash call was refused by the hook for a trailing ` 2>&1` and re-run without it.
Nothing in the repo was written except this file.

## Standing questions (critic-diff-brief items 6-7)

- DUPLICATION AND CONSISTENCY: one finding (B-1). The `current-code` diff rule is stated in `stage_done.py`, `qa-scout.md:88` and
  `s1.md:35`. Three readers repeat the old condition: `s1-scout-to-tester.yaml:29`, `story_run.py:9689`, `s2-tester-to-strategist.yaml:38`.
  Grepped: `impl-diff` over `handoffs/`, `scripts/`, `agents/`, `skills/`.
- CODE QUALITY: in the capture tool, `example-url` throws away the key that the URL encodes (C-2), and the follow covers whole-file
  sha256 values but not the content-addressed sentence ids (C-1). In the walker, amendments are not read (W-2). No package code
  quality finding beyond B-1.

```json
{"verdict": "fit_with_fixes", "blockers": [], "class_completeness": "R1 class (an exit rule changed without its hand-over form and next-role brief) covers handoffs/s1-scout-to-tester.yaml:29, story_run.py:9689 and handoffs/s2-tester-to-strategist.yaml:38 - all three named in B-1; R2 capture class (content-addressed U-/G- ids and URL-encoded keys moved by the scrub) applies to every captured story whose ticket text holds a rewritten key or corporate URL - fixed once in story_capture.py (C-1, C-2); walker gaps W-1..W-3 apply to every story; R2 part 1, R3, R4 are per-story amendments of already-fixed 0.10.9 rules, no sibling left in the package", "trail": {"read": ["docs/tasks/specs/reports/td-15-5-3-report.md", "docs/tasks/specs/reviews/td-15-cart-1-reds.md (wt 15-5-2)", "docs/tasks/specs/td-15-scenarios-quarantine.md", "ai-packages/qa-factory/scripts/tests/scenario_walk.py", "ai-packages/qa-factory/scripts/branch_accounting.py", "ai-packages/qa-factory/scripts/stage_done.py", "ai-packages/qa-factory/scripts/controller.py", "ai-packages/qa-factory/scripts/story_run.py", "ai-packages/qa-factory/scripts/source_inventory.py", "ai-packages/qa-factory/handoffs/s1-scout-to-tester.yaml", "ai-packages/qa-factory/handoffs/s2-tester-to-strategist.yaml", "ai-packages/qa-factory/references/stages.json", "ai-packages/qa-factory/agents/qa-scout.md", "ai-packages/qa-factory/CHANGELOG.md", "tools/story_capture.py", "tools/story-scrub-rules.json", "plans/piles/release-next/batch-1-release-0-10-9.md", "plans/piles/release-next/findings (RN1-13, RN1-20 origins)", "source root LOCAL-1-run-20261102: pipeline.json, state/events.jsonl, state/passed-by-person.jsonl, state/words, work/requirements-register.md, work/source-inventory.json, work/handoffs/S1-qa-scout-1.yaml", "fixture local-1-0108: expected.json, work/requirements-register.md, work/test-plan.json, work/handoffs"], "reruns": [{"command": "branch_accounting.py --unhomed on scratch copy of the UNSCRUBBED source root vs the fixture (recorded config)", "result": "source: 0 unhomed; fixture: 57 unhomed"}, {"command": "branch_accounting.s2_check in-process, source vs fixture", "result": "source: unhomed 0, 1 block (an exclusion nobody decided); fixture: unhomed 57, 3 blocks (exclusion + 21 parts no home + localhost no Attachments row)"}, {"command": "git show 658ceac29 vs HEAD grep -c: review_is_stale, rung_kinds_accepted, an exclusion nobody decided, def current_code_diff_refusal; control def unit_id", "result": "0/3, 0/1, 0/2, 0/1; control 1 in 0.10.8"}, {"command": "merge-base --is-ancestor 08e788add / 350c3c300 / d55fa3caf vs 658ceac29 and 878641cc9", "result": "all three: not in 0.10.8, in 0.10.9"}]}, "fixes": ["B-1: file and fix the impl-diff condition in s1-scout-to-tester.yaml:29, story_run.py:9689, s2-tester-to-strategist.yaml:38 (TR2-7 class completeness)", "C-1: story_capture re-keys U-/G- content ids by pairing source and scrubbed snapshot units", "C-2: example-url rewrite keeps the /browse/<KEY> tail so source_inventory._key matches the register", "W-1: door_handed takes required flags from today's handoffs/<contract>.yaml", "W-2: the walker applies expected.json amendments over stages", "W-3: names checked on decision facets", "amendment rows for S3 (RN1-13) and gateA (RN1-20) now; for S2 (WG1-1) after C-1/C-2 and a re-capture"]}
```

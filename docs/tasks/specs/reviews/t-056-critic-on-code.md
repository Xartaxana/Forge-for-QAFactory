# t-056 — critic on CODE: PC2-6 «briefs over the ceiling» (batch package-ci/2)

Under review: the uncommitted diff of `ai-packages/qa-factory/scripts/brief_pack.py` (`decisions`, `build` with nested `render`,
`main`) and `ai-packages/qa-factory/scripts/tests/test_brief_pack.py` (the N4 W6 block), plus the new
`ai-packages/qa-factory/changelog.d/pc2-6-briefs-over-ceiling.md`. Spec/DoD: `docs/tasks/specs/t-042-pc2-6-briefs-over-ceiling.md`
(read in the order the dispatch names; the «Fixes after the plan critic» section binding) and the plan review
`docs/tasks/specs/reviews/t-042-critic-on-plan.md`. `bp` = brief_pack.py, `tbp` = test_brief_pack.py (working-tree line numbers).

**VERDICT: ACCEPT WITH FIXES** — 1 blocking finding (a test expectation outside the builder's owns; the product code is right),
11 non-blocking.

The code does what the spec says. K1, O-c, O-d (built always, per B3), the B6 pop priority over an unchanged rendered order, and the
over line (a `render()` argument, measured without the line, placed before the SLICE loop) are all implemented as written. My
census over all 266 builds of an unmodified `tbp.main()` found 0 briefs with the over line under the ceiling and 0 over the
ceiling without it. The one red check (K6 negative control, `tbp:2223`) is a stale proxy, and the product is not at fault there.

---

## Answers 1-9

### 1. When the over line is added; K6

- The line is added only when the brief is still over after the last resort: `bp:4452` `budget_bytes = budget_of(text)` comes after
  the last-resort loop `bp:4442-4449`, and `bp:4453` `if budget_bytes > BRIEF_MAX_BYTES:` guards both `over_ceiling` and `over_line`
  (`bp:4462-4465`). Outside that branch `over_line` stays `""`, and every other `render` call passes either nothing or that empty
  value (`bp:4475`).
- **The builder's note (1) is wrong on one point.** The unpinned build (`tbp:2220`) carries **no** over line. Measured
  (control run 2, below): `2220 ... ceil 6144 scripts 151 budget 6007 chars 7500 over [] omitted [..., '- 3 input file(s)']`. Over the
  whole run: `builds 266 | over-line iff budget>ceiling violations: 0`. So no brief that ends under the ceiling carries the line,
  and there is no defect here (non-blocking N1 is about the report's accuracy).
- Why a longer path now gives a SHORTER brief: the budget tokenises only the real plugin root (`bp:3582-3585`). The fixed
  `FIXED_SCRIPTS` (60 chars) and `"/" + "x"*150` are not tokenised, and the card prints the folder once (control run 3: `count in
  unpinned: 1`). That adds 91 B: `nothing` sits at level 1 with no pops at 6136 B, so the unpinned build goes to 6227 B and over.
  The last resort then pops three lines in the B6 priority («critic findings: none yet», then the named inputs `s5-notes.md` and
  `first-look.yaml` from the end; control run 3 lists exactly these as «only in nothing»). Those three lines weigh more than the 91 B
  the path added, and the first pop also adds the `- 3 input file(s)` line. Result: 6007 budget B and 7500 chars against 7629.
  `len(unpinned) > len(nothing)` held only while both builds popped about the same lines. It never measured the pin.
- The control's intent is «the pin is what keeps the running folder out of the brief». `unpinned != nothing["markdown"]` alone is
  weak: any difference passes it, including one unrelated to the folder. The better expectation is the one you suggested: compare
  the card line. Blocking B1 gives the exact text.

### 2. The reason vocabulary

- With `chosen[1] >= 1` (`bp:4456`), and since a kept form is always level 1 or 2 (level 0 is rendered only by the probe,
  `bp:4342-4343, 4455`), `words at level 1` is named whenever `full` is non-empty AND `budget_bytes > probe`. The probe is the same
  render with the words as the pointer-only line. In words: the words at their shortest KEPT form weigh more than a pointer would.
  `doors only` is named when the pointer-only render is itself over (`probe > BRIEF_MAX_BYTES`) or when no words reason was named
  (`bp:4458`). This matches spec O-d («the words at their shortest kept form») and the plan critic's B3 intent: a level-2 brief
  whose words keep it over is NOT relabelled `doors only`, which K7 would read as green. The builder's note (2) is accurate.
- K7 `['words at level 1', 'doors only']` → `['doors only']` is the correct new truth, not a lost reason. Before, the level-1 words
  section carried the extra pointer `- every decision in full: <path>` (old `bp:4328`), so the words outweighed the level-0
  pointer line. O-c removed that duplicate, and now the kept words weigh no more than the pointer form: the words are not what keeps
  this brief over, and `probe > ceiling` (doors and card alone are over) still names `doors only`.
- Readers: K7 `ceiling_verdict` (`test_brief_pack_s5_plan.py:444-452`) is green before (6380 ≤ 6443 with `doors only`) and green
  after (6170 with `doors only`), so its side does not change. `test_case_id_form_texts.py:215` accepts under-ceiling or
  `== ["words at level 1"]`, and its witness is 90/90. The other consumers are tests only (grep `over_ceiling` -i over the package:
  bp, tbp, s5_plan, sd_head, case_id_form_texts). `main` now filters the budget reasons for the stdout note (`bp:4530`). No reader
  changes sides.

### 3. K1, O-c, O-d and monotonicity

- K1: `bp:1706` `minimal` = gate + warning + override + halt + answer pair[1], in the order of `shown` (`bp:1703`). The count line
  is gone (grep `waiver(s) of` over the package: only the CHANGELOG remains; positive control: the same grep run found
  `bp:1709` `every decision in full: `). Waivers of stage `*` are included (`bp:1692`). A waiver of this stage is now present at
  every SHIPPED level (2 via `shown`, 1 via `minimal`), so the unreachable state of §2 is unreachable outright.
- O-c: `bp:4340-4341`. Level 1 renders `minimal` only, and the side-file pointer is the single `omitted` line `bp:4330-4331`. Since
  `full` is non-empty whenever level 1 renders words, that line is always present.
- O-d: `bp:4407-4411`. At the level-1 attempt, if `budget_of(L1) >= budget_of(L2)` (L2 is the previous attempt
  `(0, 2, False, -1)`), the L2 render and its `chosen` are restored. `sides_needed` is then computed from the kept `dec_level`
  (`bp:4412-4413`), and the last resort renders `*chosen` (`bp:4449`), so files are popped from the kept form. Exercised in control
  run 4 (S5 fixture with the S1 waiver removed, so words are short and there are no others, which is the B3 class): `L1 pointer in
  brief: False | waiver inline: True | over: ['doors only'] | sides.decisions: False`. Level 2 is kept and the files are popped.
- Strictly smaller: `>=` reverts on equality, as spec B3 asks. When `full` is empty, L1 and L2 render identically, so the revert is
  a no-op.
- Monotone bisections: the digests predicate (`tbp:2872`) depends only on rungs 1-5, which are untouched. The gate predicate
  (`tbp:2947`, «`- every decision in full - read` absent») depends on the L1-vs-L2 comparison, which is made at fixed parameters and
  so does not depend on the ceiling. The predicate therefore stays monotone, and it tips inside 512..65536 because L1 < L2 in the
  10 KB fixture (if it did not, `tbp:2318`'s assert would fail loudly). Both checks pass in control run 1.

### 4. Pop priority (B6)

- Tags are set where each line is built (`bp:4212-4246`): `none_yet`, `case` (including the `... and N more` line), `test`,
  `source`. Everything else, including the masks and view block and the non-door `plan_files` lines, defaults to `named`
  (`bp:4444`). Text is never re-parsed. The rendered order of `files` is unchanged: same appends, same positions.
- Loop `bp:4440-4449`: for each kind in `priority`, the last eligible index of that kind, never a door (`files[i] not in doors`).
  This gives none_yet → source → named (from the end, so masks go before their snapshot line and `plan_files` go last among named)
  → case (`... and N more` first, then the last case first) → test. `trimmed_files` is rebuilt in rendered order from
  `rendered_order` (`bp:4448`). Control run 4: `trimmed in rendered order: True`.
- Is step P's sample enough? Yes, together with reading: every change is confined to (a) a render at `dec_level == 1`, (b) the
  last resort (only when over after the ladder), and (c) the over line (only when over). A brief that fits at rung ≤ 6 takes none
  of these paths, and `render` with `over_line=""` is the old `render` byte for byte (`if omitted or over_line` reduces to
  `if omitted`). So step P's «0 eligible rows differ» confirms a property that already holds by construction.
- Doors are never popped: the `doors` set is computed as before (`bp:4425-4434`) and excluded in the generator.

### 5. The over line

- Placement: `bp:4344-4345`. It is the first line of `## Not in the brief`, and the section is opened when `omitted` is empty.
  Control run 2: `over line present: 33 | not first: 0 | >1: 0 | in omitted: 0`.
- It is outside the budget: `budget_bytes` is taken before the re-render with the line (`bp:4452`) and returned (`bp:4504`).
  `budget_of` is never applied to a text carrying the line, and the line is never searched for.
- W3/W8: the by-range note still goes in at `head[:2] + [note, ""]` (`bp:4334`); the loop passes `over_line` on every re-render
  (`bp:4475`), so the size the note prints is the final text's size. W8 (`tbp:2450-2452`) is green, and `over_ceiling` stays
  `["words at level 1", "over SLICE_BYTES"]` because the reasons are fixed before `sd head`/SLICE are appended.
- `--output`/`--dry-run`: the suffix ` (side files not written in this run)` is added when `not (write and output is None)`
  (`bp:4464`), the same predicate that gates side-file writing (`bp:4484-4489`). That is right.
- stdout: `bp:4530-4533`. The clause sits after `against the ceiling` and before `, side files:`, as plan-review N4 asked; it is
  filtered to the budget reasons.
- Can the line change the predicate that prints it? No: the predicate is computed first, and control run 2 shows 0 violations. It
  can push `bytes` over SLICE_BYTES, which is the correct direction.

### 6. The 116 differing rows

- I did not re-run step P (a non-goal). My substitute is the invariant census (control run 2) plus reading (answer 4). A brief can
  differ only through paths (a)-(c), and each of those is reached only when the brief was over at the old level-2 attempt `(0, 2,
  False, -1)`. Such a brief is by definition one whose old build took the words rung, so the builder's class «a rung at or after
  the words rung was taken before» holds by construction.
- «No brief got longer in budget bytes without a line explaining it»: every build over the ceiling carries the over line (0
  violations in 266). A brief under the ceiling is within budget by definition. K1 can make a level-1 brief longer (a waiver line
  of up to 242 chars instead of a 93-char count line), and the extra cost is then either absorbed by pops or announced by the line.
  I could not compare BEFORE vs AFTER budget per row without step P's BEFORE data. The spot-check is by invariant, not by row
  (see «What I did not check»).

### 7. Tests

- `tbp:2432-2433`: the count-line expectation is replaced by the S5 waiver line inline. That is right per the F1(a) answer and
  plan-review B4. The expectation comes from the Lead's direction (the waiver goes last), not from the implementation, so FR-58
  holds.
- `tbp:2434-2436`: the first line of `## Not in the brief` of `battery` starts with
  `f"- the brief stays over its {brief_pack.BRIEF_MAX_BYTES} B budget after every cut (words at level 1"`. It is built from the
  constant (A3: no numeric literal) and read after the helper has restored `BRIEF_MAX_BYTES`. Right.
- Nothing else was weakened: the diff of tbp is exactly these 6 lines.
- Gap (non-blocking N5): O-d and the B6 priority have no test that would go red if they were removed. In every committed fixture
  L1 < L2 after K1 + O-c (spec measurement table), and W5 checks membership of trimmed lines, not their order. Control run 4 shows
  both behaviours work. The spec forbade new tests, so this is the Lead's call.

### 8. Architecture, rules, duplication, quality, changelog

- AR-24: kept (K1; the question-answer sibling is queued in roles-context batch 2, commit 28f59e9). AR-21: every popped line goes
  to `<ID>-files.md` in rendered order and is named in `## Not in the brief`. AR-20: `BRIEF_MAX_BYTES` and `DOORS_ONLY_BRIEF_MAX`
  untouched (diff). AR-22: `over_ceiling` reaches the role (the line) and the conductor (stdout), but the stderr displacement
  (plan-review N2) is still queued. AR-12: briefs shrink (O-c) or keep their size, and no new file is added. AR-10: the ahead card is
  untouched (`bp:4360-4361` not in the diff). AR-29: nothing judges a role's work; it is a byte comparison and a carry rule. The
  `judgment:` line «no census unit added» is consistent with the witness `test_judgment_census.py 22/22`.
- FR walk: A — FR-4 (a silent overflow becomes informed); B — no person text; C — FR-8, FR-49, FR-38 kept; E — FR-37 (the line
  says when no side file was written); F — FR-41 (states a measured fact); G — FR-30: a non-ASCII grep of the fragment and of the
  diff's added lines found nothing (positive control: the same grep finds `bp:976`).
- DUPLICATION AND CONSISTENCY: the diff removes one duplicate (the doubled decisions pointer). One small new duplication:
  `main` re-lists the closed reason vocabulary as a literal tuple (`bp:4530`) to filter what `build` already computed as the
  budget reasons (N8). Grepped: `over_ceiling`, `waiver(s) of`, `every decision in full`, `against the ceiling`, and the stdout
  regex readers (`test_story_step_materialize.py:247`, `test_story_run_s6_w1_frozen.py:158`; N11). The clone ratchet is the batch
  `forge-check` output, which I have not read (not run here).
- CODE QUALITY: the new code lives inside `build`, an existing function of about 450 lines (pre-existing, not new). The new blocks
  are about 10 lines each, with nesting ≤ 3. The `before is not None` guard can never be False at `dec_level == 1` given the fixed
  `attempts` list: a harmless defensive branch, not a finding. One stale comment (N4). Rebuilding `trimmed_files` costs O(n²) over
  at most a few dozen lines, which is negligible.
- ONE ROAD (item 12): K1 applies to every stage and role (stage `*` included), the over line to every role through one predicate,
  and the pop priority to every role. The `none_yet` tag exists only where that line exists (an S5 automator condition, not an
  exclusion). None found that blocks: I grepped the diff for role/stage/language branches.
- Changelog fragment name: `changelog.d/README.md` says `<pile>-<batch>-<slug>.md` («the pile and the batch lead the name»), so the
  form would be `package-ci-2-briefs-over-ceiling.md`. The spec's designer chose `pc2-6-...` and the owns line carries it. Many
  existing fragments ignore the form (`gm2-2-…`, `tr1-1-…`, `t-1936-…`), and the assembler refuses only by extension/case. Non-blocking N2.

### 9. `DOORS_ONLY_BRIEF_MAX`

- Do not tighten in this node. A3 forbids an edit, and 6170 is a Windows number: the constant's own comment (`test_brief_pack_s5_plan.py:441`)
  says it is measured on CI, where temp paths are longer. Tightening to 6170 would turn the CI shard red.
- Do not leave it either. A ratchet about 270 B looser than reality lets that much doors-only growth pass silently, which defeats
  AR-20's purpose. Proposal (N9): after the canon CI run of this batch, read the `REPORT K7: doors-only overflow: N B ...` line from
  the CI shard log (`tools/ci_read.py`) and set `DOORS_ONLY_BRIEF_MAX = N` in a named shrink commit, with the old value, the new
  value and «PC2-6 O-c» as the reason. My estimate, not verified: if the G8 CI value was 6443, the CI number is now about
  6443 − 210 ≈ 6233. Owner: Lead of package-ci (the decision belongs to the Lead tier).

---

## Blocking findings

**B1 — `tbp:2223` K6 negative control is red, and its expectation is a stale proxy.** A2 is breached («no other check red»). The
product is right (answer 1). The line is outside the builder's tbp owns (W6 block only), so the Lead has to extend the owns or apply
the edit at commit. Exact change in `ai-packages/qa-factory/scripts/tests/test_brief_pack.py`, the single line at 2223:

old:
`        check("K6 negative control: an unpinned build at a 150-char folder is a different (longer) brief", unpinned != nothing["markdown"] and len(unpinned) > len(nothing["markdown"]))`

new:
`        check("K6 negative control: an unpinned build at a 150-char folder prints that folder in its card, the pinned brief does not", f'python "/{"x" * 150}/<script>"' in unpinned and "x" * 150 not in nothing["markdown"])`

Why this and not the bare inequality: it tests what the pin exists for (the running folder must not reach the scenario's brief).
It does not depend on how many file lines either build pops, and it contains no byte constant. Verified on the run's own builds
(control run 3): `needle in unpinned: True | x*150 in nothing: False`. Witness for the fix: `python -B
ai-packages/qa-factory/scripts/tests/test_brief_pack.py`, expected `=== test_brief_pack: 880/880 ok ===`.

## Non-blocking findings

- **N1** — Builder's report, note (1): «plus the over line» is false. The unpinned build is under the ceiling (6007) and carries no
  over line (control run 2). The rest of the note's mechanism is right. A load-bearing claim of a report that was not reproduced:
  it is recorded here so the Lead does not act on it.
- **N2** — Rename `changelog.d/pc2-6-briefs-over-ceiling.md` → `changelog.d/package-ci-2-briefs-over-ceiling.md` (README form;
  it then sorts with the batch's two other fragments). The Lead's call: the spec named the current file.
- **N3** — Changelog wording, in `pc2-6-briefs-over-ceiling.md`:
  - bullet 1: «The S5 briefs that reach the words rung of the trim ladder keep the person's waivers» → «Briefs that reach the words
    rung of the trim ladder keep the person's waivers» (the bullet itself says «at EVERY stage and role»);
  - bullet 2: «level-2 briefs and briefs that never reach the words rung are byte-identical» → «briefs that never reach the words
    rung are byte-identical; a brief kept at level 2 by the rule below and still over pops its input files in the new priority»;
  - bullet 5: append «`budget_bytes` no longer counts the by-range note of a brief over 30 KB either: it is measured before that
    note, like the over line». Spec B1 makes the returned number the one taken before the SLICE loop; it used to include the note
    (old `"budget_bytes": budget_of(text)` at the end).
- **N4** — Stale comment `bp:4424`: «they stay at level 1 and the brief goes over» → «they stay at their kept level (1, or 2 when
  level 1 is not strictly smaller) and the brief goes over».
- **N5** — O-d and the B6 order have no test that fails when they are removed (answer 7). If the Lead wants one: one variant in
  `n4_scenario` with the S1 waiver removed and ceiling 1, checking that `- every decision in full - read` is absent, the S5 waiver
  is inline, and `<ID>-files.md` lists the trimmed lines in rendered order (control run 4 is the shape). That needs a tbp owns
  line; the decision belongs to the Lead.
- **N6** — When level 2 is kept and the words keep the brief over, the role's over line reads «(words at level 1)» while its words
  are whole at level 2. This is spec-sanctioned (closed vocabulary, «shortest kept form») and recorded only so the wording is a
  known trade-off.
- **N7** — O-d compares L1 and L2 with all files present. If the level-2 render has no other `omitted` line, its first pop also
  pays the `## Not in the brief` heading (about 22 B) that L1 already carries, so L2 can be kept although L1 would end up to about
  22 B smaller after the pops. The error goes in the safe direction (the words stay whole, at the cost of at most one more popped
  line). No action.
- **N8** — `bp:4530` re-lists `("words at level 1", "doors only")` as a literal. Optional: return the budget reasons from `build`
  (e.g. `"budget_reasons": list(over_ceiling)` captured at `bp:4459`) and print those, so the vocabulary lives in one place.
- **N9** — `DOORS_ONLY_BRIEF_MAX` tightening from the CI REPORT K7 number after the canon (answer 9). A queue line for the Lead:
  `tighten DOORS_ONLY_BRIEF_MAX to the CI REPORT K7 value after PC2-6 (AR-20) | узел: <Lead opens in package-ci>`.
- **N10** — Awareness: the non-door `plan_files` lines (e.g. the window's `<ID>-code.md` line «the code you will touch»,
  `bp:4250-4252`) are tagged `named` and now pop BEFORE the case files. Before the diff they popped after them. This is per spec B6
  category (2), but the Lead may want that line treated like the case files.
- **N11** — The stdout normalisers `test_story_step_materialize.py:247` and `test_story_run_s6_w1_frozen.py:158` require `)` right
  after `against the ceiling`, so an over brief's note (like a side-files note today) would not normalise. This is pre-existing,
  and no fixture of theirs is over. No action now.

---

## Control runs (verbatim)

1. `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_brief_pack.py | grep -E "^FAIL|^==="`
```
FAIL K6 negative control: an unpinned build at a 150-char folder is a different (longer) brief
=== test_brief_pack: 879/880 ok ===
```
(The run also printed the pre-existing stderr line `test_files: references/test-path-markers.json is missing, ...`, which is not
part of this node.)

2. A spy around `brief_pack.build` during an unmodified `test_brief_pack.main()` (an inline `python -B -c`, read-only):
```
['FAIL K6 negative control: an unpinned build at a 150-char folder is a different (longer) brief', '=== test_brief_pack: 879/880 ok ===']
2859 qa-automator ceil 6144 scripts 54 budget 6092 chars 7623 over [] omitted ['- the repository map head', '- the digests of earlier roles', '- every decision in full'] first False n 0
2937 qa-automator ceil 6144 scripts 54 budget 6057 chars 7588 over [] omitted ['- the repository map head', '- the digests of earlier roles', '- every decision in full', '- 3 input file(s)'] first False n 0
2220 qa-automator ceil 6144 scripts 151 budget 6007 chars 7500 over [] omitted ['- the repository map head', '- the digests of earlier roles', '- every decision in full', '- 3 input file(s)'] first False n 0
builds 266 | over-line iff budget>ceiling violations: 0
over line present: 33 | not first: 0 | >1: 0 | in omitted: 0
reason sets: [('doors only',), ('words at level 1',), ('words at level 1', 'doors only'), ('words at level 1', 'over SLICE_BYTES')]
```
Helper-level rows from the same run (excerpt): `45 2179 ... ceil 6144 scr 60 budget 6136 chars 7629 L 1 over []` (the `nothing`
build of tbp:2202) and `48 2220 ... ceil 6144 scr 151 budget 6007 chars 7500 L 1 over [] om [..., '- 3 input file(s)']`.
(266 builds here against step P's 278: P added one brief per role of ROLE_FILES and `expectation_lines()`, which the spy did not
run.)

3. The pinned vs unpinned K6 briefs (from the pickled rows of run 2):
```
needle in unpinned: True | x*150 in nothing: False | count in unpinned: 1
only in nothing:
   - qa-factory/artifacts/QA-9/work/first-look.yaml: no first look - work/first-look.yaml does not exist: no first look was
   - qa-factory/artifacts/QA-9/work/s5-notes.md (30 B)
   - critic findings: none yet - no critic has reviewed this dispatch's window, so there is no findings file to read
   Every command is `python "/builds/dev1/yml-text-factory/ai-packages/qa-factory/scripts/<script>"`, run from the project
only in unpinned:
   - 3 input file(s) - read qa-factory/artifacts/QA-9/work/briefs/S5-qa-automator-1-files.md
   Every command is `python "/xxxxxxxx...
```

4. O-d and the pop order on the S5 fixture with the S1 waiver removed (temp project via `harness`, cleaned up):
```
shown==minimal (no truncation, no others): True | full 3
ceiling 1: L1 pointer in brief: False | waiver inline: True | over: ['doors only'] | sides.decisions: False
first line of Not in the brief: - the brief stays over its 1 B budget after every cut (doors only): what it names is here whole or one named file away
trimmed in rendered order: True | kept (doors): []
```

5. Greps: `waiver(s) of|every decision in full: ` -i over the package → only `bp:1709` (control hit) and CHANGELOG.md; a non-ASCII
   grep (`[^\x00-\x7F]`) of the fragment and of the diff's `+` lines → nothing (control: `bp:976` hit); `over_ceiling` -il over
   `scripts/*.py` → bp, tbp, s5_plan, sd_head, case_id_form_texts; `question answer|question_answer_lines|free-text` over
   `plans/piles/package-ci/findings/` → none (B5 is queued in roles-context, per commit 28f59e9's message, which I read).

## What I did not check

- I did not re-run `test_brief_pack_s5_plan.py`, `test_brief_pack_sd_head.py`, `test_case_id_form_texts.py`, `test_judgment_census.py`
  or `selftest.py --lang`. Those rest on the builder's witness and are consistent with the diff (K7's 6170/`['doors only']` matches
  answer 2's reasoning).
- I did not re-run step P (a non-goal), so there is no per-row BEFORE/AFTER budget comparison. Answer 6 rests on the invariant
  census plus reading.
- The CI shard (A6) and the `forge-check` clone and lint ratchets: not available or not run.
- I did not open the roles-context finding file for B5. Its existence rests on the commit message of 28f59e9.
- I did not read `factory-rules.md` whole. The FR walk is over the sections the spec names, against the index.

## Trail

Read: the spec t-042 whole; the plan review t-042 whole; `critic-diff-brief.md:8-101`; `architecture.md` AR-12, AR-20, AR-22; `bp:1655-1713, 3577-3591,
4180-4541`; `tbp:60-129, 2150-2489, 2777-3006`; `test_brief_pack_s5_plan.py:425-516`; `test_case_id_form_texts.py:212-217`;
`changelog.d/README.md`; the fragment; `batch-2-potolki-brief-pack.md` (grep PC2-6); `docs/SIBLING_MAP.md` (grep brief_pack/ceiling;
axes 18, 34 headings); `git show --stat 28f59e9`.
Needed beyond the manifest: `docs/SIBLING_MAP.md`, `test_story_step_materialize.py:247` and `test_story_run_s6_w1_frozen.py:158` (grep only).

The decision to accept this diff, to extend the tbp owns for B1, and to tighten the ratchet belongs to the Lead (critic rule 6).
This verdict is an input to that decision.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1 tbp:2223 K6 negative control red (A2 breached): len(unpinned) > len(nothing) is a stale proxy - the unpinned build now pops 3 file lines (budget 6007, no over line) and is shorter; replace with a card-line check: f'python \"/{\"x\" * 150}/<script>\"' in unpinned and \"x\" * 150 not in nothing[\"markdown\"]; the line is outside the builder's tbp owns (Lead extends owns or applies at commit)"
  ],
  "class_completeness": "No SIBLING_MAP axis names the brief trim order (grep brief_pack/ceiling); DOORS_ONLY_BRIEF_MAX is a ratchet in AR-20's sense, tightening proposed after the CI canon (N9). In-artifact sweep of person's words at level 1: gate, warnings, halts, journal answers kept; waivers fixed by K1 (stage * included); question answers queued in roles-context batch 2 (commit 28f59e9). The words-rung-costs-bytes class is fixed class-wide by O-d (exercised in control run 4). The over line reaches every role through one predicate.",
  "trail": {
    "read": [
      "docs/tasks/specs/t-042-pc2-6-briefs-over-ceiling.md",
      "docs/tasks/specs/reviews/t-042-critic-on-plan.md",
      "docs/tasks/critic-diff-brief.md:8-101",
      "ai-packages/qa-factory/design/architecture.md AR-12, AR-20, AR-22",
      "ai-packages/qa-factory/scripts/brief_pack.py:1655-1713,3577-3591,4180-4541",
      "ai-packages/qa-factory/scripts/tests/test_brief_pack.py:60-129,2150-2489,2777-3006",
      "ai-packages/qa-factory/scripts/tests/test_brief_pack_s5_plan.py:425-516",
      "ai-packages/qa-factory/scripts/tests/test_case_id_form_texts.py:212-217",
      "ai-packages/qa-factory/changelog.d/README.md",
      "ai-packages/qa-factory/changelog.d/pc2-6-briefs-over-ceiling.md",
      "docs/SIBLING_MAP.md (grep)"
    ],
    "reruns": [
      {
        "command": "python -B ai-packages/qa-factory/scripts/tests/test_brief_pack.py",
        "result": "=== test_brief_pack: 879/880 ok === with the one FAIL line K6 negative control (matches the builder's witness)"
      },
      {
        "command": "inline spy around brief_pack.build during test_brief_pack.main()",
        "result": "builds 266, over line present iff budget_bytes > ceiling: 0 violations; over line first in its section in all 33, never in omitted; tbp:2220 unpinned: budget 6007, 3 input files popped, no over line"
      },
      {
        "command": "inline probe: S5 fixture without the S1 waiver, ceiling 1, write=True",
        "result": "level 2 kept (no L1 pointer), S5 waiver inline, over ['doors only'], trimmed lines in rendered order: True"
      }
    ]
  },
  "fixes": [
    "B1: tbp:2223 replace the K6 negative-control check with the card-line check given in the report; witness test_brief_pack 880/880",
    "N2: rename the fragment to changelog.d/package-ci-2-briefs-over-ceiling.md (README form; Lead's call)",
    "N3: changelog wording - bullet 1 drop 'S5', bullet 2 qualify byte-identity, bullet 5 add that budget_bytes no longer counts the by-range note",
    "N4: bp:4424 stale comment 'they stay at level 1' becomes 'they stay at their kept level'",
    "N9: after the canon, tighten DOORS_ONLY_BRIEF_MAX to the CI REPORT K7 value in a named shrink commit (Lead)"
  ]
}
```

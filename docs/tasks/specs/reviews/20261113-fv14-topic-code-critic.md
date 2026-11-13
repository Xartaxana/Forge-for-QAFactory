# t-532 — critic, one topic pass (R13-g): FV1-4 N0 + N1 + N2, merged tree `wip/fv14-topic` 77966e9

Spec: `docs/tasks/specs/20261113-fv1-4-no-brief-cut-spec.md` (§2a, §4-§8, §9c, §10). Range reviewed: merge-base `5c16661` (origin/main)
..77966e9. Commits in scope: a83b5f3 (N0), 8207150 (N1), 4a1e555 + 84500d4 (N2), 77966e9 (merge). Out of scope, present in the range:
079dc63/bea0bb0 (P1-v N0) and 9fa6fd2 (P1-v N3), reviewed elsewhere.

**Verdict: ACCEPT WITH FIXES** (`fit_with_fixes`). No finding blocks the design. Four fixes are owed before the merge (F1-F4).
Q1-Q7 are proposed queue nodes. The decision to accept belongs to the Lead.

## Findings

### FIX (before merge)

**F1. Two silent cuts in `build`'s head that the spec's §5.6 row puts on N1 are still in the code.**
`brief_pack.py:4213` `_short(dispatch.get('reason'), 200)` and `:4222` `Purpose: {_short(dispatch['purpose'], 300)}`.
The spec row: "`build` head `:4194`, `:4203` | repair reason 200, purpose 300 | dispatch record words, no carrier named | whole, one line
| N1 (inside `build`)". Failure scenario: a repair dispatch whose `reason` is the reviewer's 600-character text. The brief head shows 197
characters + "..." and names no file. The delta side file carries it whole (N2, `delta_lines`), but only for a resumed S5 plan/window.
For every other repair dispatch the rest of the reason reaches no one. This is the class the topic exists to remove ("still cuts
silently"). N2's report flagged the hit as N1's (`4218, 4227 build head (N1)`), and nobody picked it up. N2's changelog fragment also
claims "the repair reason ... whole on one line", which the brief head contradicts.
Fix: `_text_whole(...)` at both sites, plus one variant row each (AT 200/300, BEYOND +1, 10×) in an existing `build` test function.

**F2. A quarantined test file was edited and run.** `scripts/tests/test_brief_pack_timeout.py` sits in the `quarantine` section of
`test-layers.json`. Commit 84500d4 rewrote K-B5/K-B6 with no `quarantine-edit:` line, and the coordinator then ran it as a control
("brief timeout 22/22"). docs/TESTING.md:64-65 says a quarantined file is "не чинится и не правится". critic-diff-brief item 5 makes an
edit without a holding `quarantine-edit:` reason a finding. The rows are also redundant: keep `test_brief_pack.py`
`n2_summaries_name_their_whole` already pins 3/4/30 profiles and a 120/121/1200-character why. The other nine quarantined files were
left alone (correctly), so this also treats quarantine two ways (P31).
Fix: restore the file to cf4dede bytes. Let quarantine-watch judge its reds (see the quarantine answer below).

**F3. E-27 (F13, owner N1) has no test row.** `_legacy_cut_reworded` (`brief_pack.py:1623-1628`) carries two edges: the ≥ 20 000-character
threshold and the exact trailing match. Neither is pinned in a keep file. Grep `cut when it was recorded|_legacy_cut_reworded|more
characters, the whole text is in` (case-insensitive) over `scripts/tests` finds only the quarantined `test_s5_settled_oracle.py:150`,
which also serves as the positive control. N1's own edges line says "E-1 … E-30 that name N1, each a variant row".
Failure the missing row would catch: an off-by-one in `found.start() < LEGACY_CUT_TEXT_MIN` would re-word a short answer a person typed.
Fix: one parametrised row in `answers_of`'s test: 20 000 chars + marker → re-worded; 19 999 + marker → kept; marker not at the end → kept.

**F4. N1's mechanical layer is not on file, and the changelog contradicts itself.**
(a) N1's report was delivered inline only. The DoD's handoff asks for the §7 table with both RATCHET runs (step 2/4) and
`role_load.py --all` before/after outputs verbatim. Only a paraphrase reached this review (rule 7). I reproduced S5 (below). The 12
`ROLE_BRIEF_BYTES_MAX` rows I did not: I had one re-run, and N2 merged after N1 measured them, so their tightness on 77966e9 is unshown.
Fix: persist the N1 report under `docs/tasks/specs/reports/` with the verbatim runs. Attach the `RATCHET ROLE_BRIEF_BYTES_MAX` lines from
the coordinator's merged 1097/1097 run. Any row whose measured value is below its constant is loose and is lowered (shrink-only).
(b) N0's report lives only in `.claude/worktrees/fv14-n0/`, not in the topic tree the dispatch names. Copy it.
(c) `changelog.d/p1v-n3-brief-sizes.md:2` still announces the record `{ts, stage, role, dispatch, bytes, budget_bytes, ceiling, over}`.
`fv1-4-no-brief-cut.md` announces `bytes` only. Both are unreleased fragments of one release, so the assembled CHANGELOG would contradict
itself. Spec §3 names this fragment as a reader. Fix: reword the p1v-n3 fragment (one line).

### QUEUE (proposed nodes; the Lead opens them, rule 6)

- **Q1 (spec gap, F10).** A MULTI-line answer with one line over 1 000 characters is not wrapped. `_words_block` sets
  `wrapped = not broken` (`brief_pack.py:~1708`). Input `"a\n" + "x"*200000` → a fenced block holding one 200 000-character line, which a
  range read cannot split. F10's own reason ("a range read cannot split one line") applies equally. The spec covered only the
  no-line-break case, and the builder followed it. Proposed node: wrap every block line over `WORDS_LINE_WIDTH`, with the `<decisions>`
  pointer and a row. Owner: brief_pack (live-run-fvf).
- **Q2 (AR-13 sibling).** `driver_machine.take_answer:3320` has its own inline `replace("\r\n","\n").replace("\r","\n")`, a second copy of
  the rule `person_words.lf` was made the one place of. Found by Grep, case-insensitive. The same search found
  `person_words.py:162`, which serves as the positive control. Outside N0's owns.
- **Q3 (duplication, item 6).** The write-then-pass road is copied three times: `driver_runner.py:289-292`, `driver_machine.py:3311-3314`
  and `:3892-3895` (`kept = person_words.write_words(...)`; `--notes-file` if kept else `--notes`). N0's owns forbade a helper. Proposed:
  one helper (`DriverRunner` method or `person_words.notes_args`) so the three cannot drift (absolute vs relative path, blank rule).
- **Q4 (feeds the open Lead question on `app_card`).** After N1 a lesson line can exceed 400 characters. `app_card.py:165`
  `_clip(x, LESSON_LINE_CHARS)` now cuts a person's lesson words in the walk card (middle "...", no pointer). Its comment at `:57`
  ("words cut at 200 by project_knowledge.lessons") is now false. Before N1 the 200 cut kept that clip from ever firing. This makes
  `LESSON_LINE_CHARS` the first candidate in the Lead's "which `app_card` ceilings without a pointer go". Not decided here.
- **Q5.** `driver_sources.py:87, :142` `"; ".join(pasted)[:1500]` (spec §12 item 7) cuts the names of the material a person supplied,
  inside a `human_answer` note. I did not find it queued in the topic tree's piles (Grep `driver_sources` over `plans/`, `docs/tasks`).
  The Lead confirms a node, or opens one.
- **Q6 (code quality, minor).** `_fl_line_clipped` (`brief_pack.py:~4017`) infers a clip from the output's shape (length == 180 and a
  trailing `... [first-look:…]`), a second source for a fact `_fl_line` knows. `_fl_line` is in N2's owns and could return the flag.
  The trace is correct (clipped length = room-3+3+1+len(mark) = 180), so this is only fragile.
- **Q7 (nit).** `role_load.settings` does not validate `allowances.brief` / `brief_charter_head` types. A malformed value raises a raw
  `ValueError` in `_brief_allowance`. The file is package-owned, so this is low.

## Class completeness — every remaining slice / ceiling in `brief_pack.py` (77966e9)

Both §5.6 patterns were re-run on 77966e9. Positive control: `S4_REQUIRED_BY_CHARS` at `:2814`.

| Site | State |
|---|---|
| `_words_block` / `decisions` / `question_answer_lines` (words, gates, warnings, overrides, halts) | renders whole (one line ≤ 1000, else fenced; wrap → `<decisions>`); Q1 gap for long lines inside a multi-line block |
| `digests` `:1592, :1603` `_short(DIGEST_CHARS)`, `same[-DISPATCH_DIGESTS:]` | names its whole (`- every digest in full: <digests>`, side file written) |
| `source_material`, `tests`, `rows`, dispatch scope `[:8]` | renders whole |
| `cases[:8]` `:4331` | names its whole (count + "same folder", per spec) |
| `build` head repair reason `:4213` (200), purpose `:4222` (300) | **still cuts silently** — F1 |
| SD head `_form_line` `:3679` | names its whole (`(whole: <where>)`) |
| `request_lines` `MAX_REQUEST_LINES`, `SITE_FILES_SHOWN` `:3305, :3318` | names its whole (the list file) |
| `walk_lines` `FUNCTIONS_SHOWN` `:3350` | names its whole (register table); names whole |
| `exploration_cell_lines` `:3407` | names its whole |
| `branch_check_line` `:600` (late_why), `:616` | names its whole (`base_rel` in line / `(whole: …)`) |
| `expectation_change_lines` `:704-711` | names its whole (pointer on every line when clipped or > 8) |
| `proof_required_lines` `:767, :836-839` | names its whole |
| `side_lines` `:912-934` | names its whole (`whole: pipeline.json sides`) |
| `_bind_lines` `:1037-1060` | names its whole |
| `_log_of_attempt` `:1071`, `_sha12` `:524` | out of class |
| `base_log_lines` `:1113` | names its whole (`work/run-blocks/`) |
| `REFERENCES_SHOWN` `:1371` | names its whole (references file) |
| `blast_radius_line` built `:1904` (reason room) | names its whole (blast-radius.json in line); failure branch renders whole |
| plan notes `:2079` `HEAD_LINE_CHARS` | names its whole (slice file in the same head) |
| `_names_by_module` `HELPER_NAMES` `:2157` | names its whole (map path) |
| `EXCERPT_LINES` `:2255` | names its whole (range + Read) |
| code side file `CODE_FILE_BYTES` | names its whole (every left-out excerpt by `file:lines`; brief line adds "over 30 000 B: read it by range") |
| `_shared_fixture_lines`, `helper_lines`, `reached_by_receipted` | renders whole |
| `STAND_PATHS_MAX` `:2732`, `STAND_HELPER_NAMES` | names its whole (map path) |
| `_stand_text` / `_stand_names` / case actors | renders whole |
| `S4_INTEGRATIONS_MAX` `:2847`, `S4_REQUIRED_BY_CHARS` `:2848` | names its whole |
| `_s3_roster_line` `:2873-2874`, roster `:2925-2936` | names its whole (`roster_file` named) |
| `APPROACH_DOCS_MAX` `:3024`, `APPROACH_LINE_CHARS` | names its whole (folder / file in line) |
| `CANDIDATE_LINE_MAX` `:3116` | names its whole (rest by id + register) |
| `_fit_row_line` `:3139-3151`, `FIT_LINES_MAX` `:3195` | names its whole |
| `FIRST_LOOK_REQ_CHARS/MAX` `:3951` | names its whole (register named above) |
| `_fl_line` / `first_look_lines` `:4014, :4119-4121` | names its whole (`whole: work/first-look.yaml`) |
| every "could not" exception line (N2 list) | renders whole (`_text_whole`) |
| `SLICE_BYTES` note | guard limit, not a cut |

Callees: `project_knowledge` lessons render whole (2a, F9). `app_card` is the open Lead question (Q4). `driver_sources` `[:1500]` (Q5).

## Standing questions

- **Fit to spec:** N0 meets J-1…J-5, E-25/26/31/32/33 and DoD (1)-(5). I read the product diff. N0's witness is verbatim
  (49/49 + fast files). For N1, keys (1), (2), (4)-(8), (10) and (11) hold by diff reading. (3) and E-22/23/24/30 have rows at
  `test_brief_pack.py:1839-1863`. (9) rests on the report (F4). (12) S5 is reproduced and ROLE is not (F4). Gaps: F1 (§5.6 build-head
  row) and F3 (E-27 row). N2: every §5.6 N2 row is applied, per diff reading against the table, plus F2.
- **Builder decisions in the silent spots:** `harness.PLUGIN_ROOT` instead of the absent `PLUGIN` is safe. `source_material out[:8]`
  removed is per spec. `role_brief_ratchet` as its own function, not inside `p1v_n3_brief_size_record`, is harmless. `_text_whole` /
  `_clipped` helpers are consistent with `_clip`/`_short` folding (traced).
- **DUPLICATION AND CONSISTENCY:** Q3 (three copies of the notes-file road). Q2 (inline LF rule in `take_answer`). `digests` computes
  `len(" ".join(...split())) > DIGEST_CHARS` twice inline where `_clipped` now exists (minor). `harness.normalised_bytes` replaces the
  deleted `measured_bytes` (spec-sanctioned move, one copy). Grepped: `replace("\r\n"` over the driver/brief/person_words files (control
  `person_words.py:162`), `_answer_note(`, `human_answer` producers.
- **CODE QUALITY:** no new function over ~60 lines (`_words_block` ~20, `_wrapped` ~10, `pointed` ~6). `build` shrank by ~250 lines.
  The unused parameters `person_words_whole(project, holder)` and `_stand_names(limit)` are spec-sanctioned and documented. Q6 is fragile
  inference. No dead branch found in the new code.
- **Architecture (q10):**
  - AR-13 kept, apart from the pre-existing `take_answer` copy (Q2).
  - AR-14 kept: every note file goes through `write_words`, and the N0 diff has no `open`/`write_text` on `state/words`.
  - AR-20: S5 re-base is honest. The control re-run measures 9520 = the constant, AT, green. ROLE rows are unreproduced (F4).
    Both carry the named re-base line. CI equality is unproven until the batch canon.
  - AR-21 kept.
  - AR-22: the result keys' readers (`main`, `_record_brief_size`, role_load, retro_numbers, gate_preflight, artifact-writers) changed
    in the same commits. The removed-names grep (case-insensitive, over the package) leaves only comments, controller's own unrelated
    `BRIEF_MAX_BYTES`, quarantined tests, and the p1v-n3 fragment (F4c).
  - AR-24 kept for a person's words in the brief and journal. `app_card` now clips lessons (Q4).
  - Naming: N0's commit omits AR-13 (minor). N0 is recorded "not a mechanism" although spec §11 M2 is one. The four questions live in
    the spec, not in the commit or DECISIONS (process note for the Lead).
- **Judgment (q11):** none moved into code. The FV1-4 commits touch no census row, no craft marker, no `blocks_override`. The census
  delta in the range is P1-v N0's.
- **One road (q12):** one words renderer for every role, stage and language, and no role/language branch in the diff. The one
  two-way treatment found is F2 (quarantine). Grepped the diff for role/language-name branches and found none new.

## Quarantined files using removed names (the nine)

Acceptable under docs/TESTING.md: canon skips them, and they are not fixed or edited. They will go red in `quarantine-watch`. The
coordinator should record, for its `judge` step, that these reds pin cuts FV1-4 removed (not a catch, nothing to `land`).
`test_controller_brief.py` hits are `controller.BRIEF_MAX_BYTES` (a different constant, `pin_holds`) and are unaffected.

## Pre-existing reds

test_role_load K10-b/c and audit A22/A27 (qa-failure-analyst): the brief allowance keeps 6144 + 1024. N2's base-vs-branch run shows
the same two FAIL lines at cf4dede (18,426 / 16,401 tokens), so this topic does not make them worse. The merged tree is not re-run by me.
test_exploration_perturbations T2: N2 changed only `exploration_lines`' exception text, and the same FAIL is at cf4dede. Not worse.

## Trail

Read: spec (whole, 907 lines); critic-diff-brief.md (whole); docs/TESTING.md:60-91; N0 report (fv14-n0 worktree); N2 report (topic tree);
`git show a83b5f3` (product files); diff cf4dede..8207150 and cf4dede..84500d4 of brief_pack.py (whole); `git show 8207150` for role_load,
role-load.json, project_knowledge, gate_preflight, retro_numbers, test-layers.json; `git show 84500d4 test_brief_pack_timeout.py`;
person_words.py:60-215; role_load.settings/_settings_problems; brief_pack.py merged at :429-440, :594-616, :640-725, :1133-1135,
:1368-1392, :1579-1628, :1898-1910, :2072-2082, :2150-2162, :2250-2258, :3018-3028, :3108-3120, :3190-3200, :3944-3954, :4010-4017,
:4205-4225, :4420-4500; harness.normalised_bytes; test_brief_pack_s5_plan.py:540-600, :859-874; test_brief_pack.py:2290-2330, :1839-1863;
driver_machine.py:3296-3325; app_card.py lesson lines; waiver/controller/ticket_adapter human_answer writers; changelog fragments.
Searches (positive controls named inline above): §5.6 patterns (i)/(ii) on merged brief_pack.py; broader slice/"more)" pattern;
removed-names grep over the package; `_answer_note(`; `human_answer`; `replace("\r\n"`; `lessons(`/`["more"]`; `lesson` in app_card;
legacy-marker tests; quarantine sections of test-layers.json (python json read); `quarantine-edit` absent in 84500d4's message.
Re-run (one, cheap): `python -B .../fv14-topic/ai-packages/qa-factory/scripts/tests/test_brief_pack_s5_plan.py` at HEAD 77966e9 →
`RATCHET S5_PLAN_BRIEF_BYTES_MAX 9520` / `=== test_brief_pack_s5_plan: 213/213 ok ===`.
Not done: ROLE ratchet re-measure, role_load --all, CI (batch canon's).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "Every remaining slice/ceiling in brief_pack.py enumerated (table in the review): all render whole or name their whole one step away except build head repair reason :4213 and purpose :4222 (F1, a spec row of N1 left undone). Callee siblings queued: app_card lesson clip now live (Q4, Lead question), driver_sources [:1500] (Q5), take_answer inline LF rule (Q2), multi-line long-line wrap gap (Q1).",
  "fixes": [
    "F1 brief_pack.py:4213 and :4222 - render the repair reason and purpose whole (_text_whole) with AT/BEYOND/10x rows",
    "F2 test_brief_pack_timeout.py - quarantined file edited in 84500d4 without quarantine-edit; restore cf4dede bytes",
    "F3 add E-27 rows for _legacy_cut_reworded (20000+marker reworded; 19999 kept; marker not at end kept)",
    "F4 persist N1 report with verbatim RATCHET and role_load --all runs, attach merged ROLE ratchet lines and lower loose rows; copy N0 report into the topic tree; reword changelog.d/p1v-n3-brief-sizes.md:2"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/20261113-fv1-4-no-brief-cut-spec.md",
      "docs/tasks/critic-diff-brief.md",
      "docs/TESTING.md",
      ".claude/worktrees/fv14-n0/docs/tasks/specs/reports/20261113-fv14-n0-report.md",
      "docs/tasks/specs/reports/20261113-fv14-n2-report.md",
      "ai-packages/qa-factory/scripts/brief_pack.py",
      "ai-packages/qa-factory/scripts/person_words.py",
      "ai-packages/qa-factory/scripts/log_append.py",
      "ai-packages/qa-factory/scripts/driver_core.py",
      "ai-packages/qa-factory/scripts/driver_runner.py",
      "ai-packages/qa-factory/scripts/driver_machine.py",
      "ai-packages/qa-factory/scripts/role_load.py",
      "ai-packages/qa-factory/references/role-load.json",
      "ai-packages/qa-factory/scripts/project_knowledge.py",
      "ai-packages/qa-factory/scripts/gate_preflight.py",
      "ai-packages/qa-factory/scripts/app_card.py",
      "ai-packages/qa-factory/scripts/tests/harness.py",
      "ai-packages/qa-factory/scripts/tests/test_brief_pack.py",
      "ai-packages/qa-factory/scripts/tests/test_brief_pack_s5_plan.py",
      "ai-packages/qa-factory/scripts/tests/test_brief_pack_timeout.py",
      "ai-packages/qa-factory/scripts/tests/test-layers.json",
      "ai-packages/qa-factory/changelog.d"
    ],
    "reruns": [
      {
        "command": "python -B C:/QAFactory/forge-repo/.claude/worktrees/fv14-topic/ai-packages/qa-factory/scripts/tests/test_brief_pack_s5_plan.py (HEAD 77966e9)",
        "result": "RATCHET S5_PLAN_BRIEF_BYTES_MAX 9520; === test_brief_pack_s5_plan: 213/213 ok ==="
      }
    ]
  }
}
```

Critic on plan: FV1-4 no brief cut spec (t-495)

report: not written. The handoff gate refused C:\QAFactory\forge-repo\docs\tasks\specs\reviews\20261113-fv1-4-plan-critic.md ("no handoff path inside docs/tasks/specs/reviews in the dispatch"), so the full verdict is below for tools/handback_extract.py.

# Critic on the plan: FV1-4 "no cut of a brief by size in a run" (task t-495)

Spec reviewed: docs/tasks/specs/20261113-fv1-4-no-brief-cut-spec.md (all 533 lines, §9a included). PKG = C:\QAFactory\forge-repo\.claude\worktrees\p1v-n3\ai-packages\qa-factory; every file:line below is from that tree. Method: reading plus targeted Grep, case-insensitive with a positive control. No tests run.

**VERDICT: ACCEPT WITH FIXES** (one finding blocks N0's dispatch, 6 must be fixed before N1/N2, 7 minor; no redesign needed).

- **What holds:**
  - The §3/§4 facts I checked hold by trail (30+ lines).
  - The mechanism is sound.
  - N1 alone does not make a run that works today start being refused (K3): the brief is only pointed at, never injected.
- **What fails:**
  - **K1:** the class sweep misses sites, including a second cut of a person's words.
  - **N0:** as written it can lose a person's words on the owed-row path.
  - **F4:** the ratchet has no procedure a builder can follow.
  - **T3a:** two shared-file crossings are not queued.
  - **Edge:** the spec's own "fold every words line to one line" choice leaves an edge undecided.

Acceptance is the Lead's decision; this verdict is input to it.

## Defects, ranked

### Blocks N0's dispatch

**1. N0 deletes the note file that the owed-row replay needs, and adds a second writer of words files (AR-14, AR-24, P31).**

- **What the DoD says:** spec :414, "writes the note through a file under `state/` passed as `--notes-file` and removes it after the call".
- **How the words get lost:**
  - `driver_runner.owe_row` saves a failed write with its args: `"args": [str(a) for a in args]` (driver_runner.py:276).
  - `driver_conductor.owed_rows_step` replays those args later (driver_conductor.py:149).
  - After N0 the args hold `--notes-file <path>`, but the file is already gone. `person_words._from_file` answers "no such file" (person_words.py:81-85).
  - The row fails, is given up after OWED_ROW_TRIES (driver_conductor.py:154-157), and the person's words are lost.
  - This breaks owe_row's own error direction: "a duplicate row is allowed ..., a lost row is not" (driver_runner.py:267-268). Today `--notes <text>` keeps the words inside the owed row.
- **Second writer:** person_words.py is "the ONE writer of that folder" and "never deletes or rewrites" (person_words.py:40-45).
- **Smallest fix:**
  - N0 writes through `person_words.write_words(task_root, "", "<kind>", note)` and keeps the file.
  - Add a J-row: "log_append fails once → the owed row replays from the kept file → the note equals the words whole".
  - State the TEMPORAL world: owed rows written before N0 carry `--notes <text>` and still replay.

### Fix before dispatching N1 / N2

**2. K1 misses: size bounds that cut content and are not in §5 / §5.6.**

The spec's constant grep `^[A-Z_]*(CHARS|...)` cannot match names that contain a digit. I reproduced it: a digit-aware pattern finds 9 lines, including S4_REQUIRED_BY_CHARS and S3_ROSTER_WHY_CHARS. Missed sites:

- **a. A person's words cut at 200 characters, inside a brief.** `stand_lesson_lines` (brief_pack.py:2696-2708) renders `project_knowledge._lesson_line`, which cuts the words at LESSON_WORDS_SHOWN = 200 with " ..." and no pointer (project_knowledge.py:64, 440-442). These are "what a person taught": the same class as the core defect. project_knowledge.py is in neither N1's nor N2's owns.
- **b. A silent count cap on collected material.** `source_material` ends with `return told + out[:8]` (brief_pack.py:1515), with no count line and no pointer. It includes "material the person supplied" (pasted-*, :1512-1513). This is AR-21, a sibling of the `tests[:6]` cap the spec removes. No node owns it.
- **c.** `s4_stand_lines` clips with `_clip(words, S4_REQUIRED_BY_CHARS=80)` (:2754, :2788); the pointer appears only past 15 lines (:2789-2790).
- **d.** Roster clips: `_clip(role,60)` and `_clip(story,40)` at :2812-2813 and :2872, and `_clip(problem, 120)` at :2856. The role/story clips may be "stays" (the header names the file, :2859); the problem clip is not.
- **e.** First-look problem/why clips at :3861, :3891, :3939, :4015, :4019. (FIRST_LOOK_REQ_CHARS at :3934 is fine: the line names the register.)
- **f. Code side file.**
  - The F5(a) "... and N more" tail is in `_fit_code_file` (:2386-2422, tail at :2421). N2's owns name only `window_code_file` and `_shared_fixture_lines`.
  - The helpers tail "(+N more)" with no carrier (:2152-2154) is in no row.
  - :2316 is a list of notes "(+N more)", not exception text.
- **g.** `exploration_lines` cuts with `str(exc)[:60]` (:3401). `decisions` cuts with `json.dumps(halt)[:200]` (:1731); N1 owns `decisions`, but §5.1 does not name it.

**Fix:** add each site to §5.6 with a verdict, assign owners in N1/N2 owns, and rerun the class grep digit-aware and over the called modules (`project_knowledge`, `sizing.clip_name` at sizing.py:612-625, `app_card`).

**3. Undecided edge: a long answer becomes one huge line (K3/K5/K9).**

- **The choice:** §5.1 folds every words line into one line and writes the decisions side file only when `others > 0`. A 24 576-character answer (E-1), or a 200 000-character one, becomes a single 24-200 KB line. No copy that keeps the line breaks sits one step away.
- **The unknown:** whether a host's Read returns such a line whole is not verified. In this harness Read showed a per-call cap ("cap 25000" tokens), and range reads go by line, so a range read cannot split one line. Today every words line is at most 400 characters and the whole text is in the side file.
- **Fix, either way:**
  - Run one experiment (hygiene 6(a)): a brief with a 200 000-character line, read by a role on Claude Code and on Codex.
  - Or take the safe side: render the words section from `full` with line breaks kept.
- **Edges to add:** a 200 000-character answer and a multi-paragraph answer.

**4. The F4 ratchet is not executable by a builder (K6, AR-20).** §7 says "CI-measured bytes ..., never typed by the builder".

- **No procedure.** The builder commits before CI runs, so it must either type a number or land a red commit plus a fix-up commit. Neither is described.
- **Wrong unit.**
  - The raw byte count differs between CI and Windows because temp-path lengths differ (test_brief_pack_s5_plan.py:441).
  - N1 also deletes `measured_bytes`, the one path-independent measure.
- **Inconsistent count.** F4(a) says "one ratchet per keep file", but:
  - §6 deletes every size row of test_brief_pack.py (:873, the size row in :1856-1868, :3380-3399);
  - test_ahead_cards.py:364-365 gets only "→ F4", with no key and no number.
- **Fix:**
  - Keep a path-normalised size helper in the test (temp root replaced by a token), so the number is the same everywhere.
  - The builder measures it with the helper and writes a named raise line; the critic reruns that one test.
  - Name key and old → new for each keep file that keeps a ratchet; mark the rest deleted.

**5. Shared-file crossings with T3a are not queued (K8, «Командная работа» п. 3).**

- **What T3a owns:**
  - told-before-work spec :625: test_ahead_cards.py, "pin removed (T3a)";
  - :628: role-load.json is a shared file, T1 → T3a → T1r;
  - T3a also adds `native_headroom` baselines and a function to role_load.py (:271-273).
- **What N1 owns:** role-load.json (allowances), role_load.py (`_brief_ceiling`, `static_load`) and test_ahead_cards.py :364-365.
- **What §9a queues:** only brief_pack.py and the driver files.
- **Fix:** add `очередь:` lines, with function lists, for role-load.json, role_load.py and test_ahead_cards.py in both specs.

**6. The data premise is not measured (PROJECT.md «Как принимается изменение пакета» п. 6(a)).** §9a itself calls this a meaning change of the result keys, and the rule requires one command on real data with the result in the spec. There is no number for how big briefs become without the cut; LR2-1 had "35 of 41 over" (scoreboard spec :592). That number also decides #3 and the starting value of the forge norm. **Fix:** rebuild the recorded cart-1 / LR2-1 briefs with the ladder off, record bytes and longest line per brief, and write the result into §2.

**7. §6 misses rows that will turn red.** In test_brief_pack.py:

- :2414 ("under 6 KB");
- :2425 (`over["sides"]["decisions"] is True`);
- :2426-2427 (reads `-decisions.md`).

After §5.1 those words are inline, `others == 0`, and no side file is written. All three are outside the cited range :2324-2420. **Fix:** list them with their new expectations.

### Minor

- **m1.** N0 must stop calling `brief_pack.person_words_whole`. Otherwise the 40 000-character row stays red until N1 lands (order is N0 → N1; driver_core.py:268-269). Name the one place the line-ending normalisation lives.
- **m2.** `--notes` defaults to "" (log_append.py:202), and `person_words.read` refuses "both" whenever inline is not None (person_words.py:145). The spec must say `args.notes or None`, as --reason-file does at :212.
- **m3.** TEMPORAL: old journal notes carry "[cut: ..., the whole text is in journal.jsonl]", which points at the very file holding the cut (driver_core.py:269; brief_pack.py:1601-1603). Decide how they are rendered after N1.
- **m4.** test_ahead_cards.py:366-375 (same files listed without the card) becomes trivially true. Say whether it is kept.
- **m5.** F2's limit of 32 767 is the CreateProcess limit. Through run-py.cmd the limit is 8 191 (run-py.cmd:27), and cmd cuts at the first line break (person_words.py:3-7). Correct the figure.
- **m6.** P1-v's N-brief norm reads the run-log `note: brief:` lines (scoreboard spec :354), and N1 changes that line's format. Name the new format for P1-v.
- **m7.** FR-55 window: until P1-v N6 lands, the only watch is one fixture ratchet, and nothing reads brief-sizes.jsonl. Name it as a residual owned by П1-в N6.

## Per-key table

| Key | Verdict | Evidence |
|---|---|---|
| K1 class completeness | defect | Finding 2. Control: the `_short(`/`_clip(` grep found 73 sites, including every §5.6 site. |
| K2 facts by trail | holds | 30+ lines checked: constants :54-65; person_words_whole; question_answer_lines; decisions; digests; _record_brief_size; ladder, last resort, over line, SLICE, result, main :4619-4624; story_step :445-460; role_load :453-464/:521/:715; retro_numbers :962-980; driver_core :263-269; `_answer_note` call sites (only those three, by Grep); log_append :192-215; DOORS_ONLY 6443 at :441; controller 1500 at :9695; inject_context :267-277; native_context :173-175; test-layers lines. The broken digests pointer is real (:1559 vs :4499/:4580). The "no decision record" negative reproduced: 0 hits, control D-00 = 23. |
| K3 what replaces the protection | holds; #3 open | `collect_blocks` reads only inject-map entries (inject_context.py:154, 242-287). The Codex context is those blocks + packet (:707-725); the driver twin is the same (driver_dispatch.py:213-241). No in-run consumer of role_load (story_load is CLI-only, :747). |
| K4 AR-22 readers | holds for product code; tests partial (#7) | Grep -i over PKG: 381 hits in 26 files; control brief_pack.py = 72. Extra files beyond §4 are legitimate: controller's own constant, recorded fixtures. |
| K5 edges | partly defect | m2, #3, #1 (owed-row replay), m3. E-11..E-13 are correct; settings() validates only packet/launch (role_load.py:87-89). |
| K6 ratchets | defect | #4. role-load ratchets unchanged under F3(a) is credible: DoD key (9). Census unchanged for N0-N2. |
| K7 architecture / principles | defect | AR-14/AR-24/P31 (#1, #2a); AR-21 (#2b). AR-13, AR-29 and P25 hold; FR-55 partial (m7). |
| K8 nodes for a weaker model | defect | N1 as one node is justified (AR-22). N2 lacks `_fit_code_file`; `source_material`, `stand_lesson_lines`, the roster and first-look clips have no owner. #5 crossings. FV1-30a: no crossing (its owns, fv1-19 spec :277). |
| K9 silent | defect | #1, #3, #6, m1, m2, m3, m6. |

Class completeness: the class is "a size bound that drops or clips brief content whose whole is not one named step away"; the surface is the brief_pack line builders and their callees.

- **Spec covers:** about 25 sites.
- **Missed:**
  - the lessons cut of a person's words (200 characters);
  - `source_material` `out[:8]`;
  - about 12 clip sites.
- **Axes:**
  - 29: covered;
  - 34: broken on N0's write side;
  - 18: ratchet procedure missing;
  - 5: holds.
- **Queued elsewhere:** the in-run refusals in inject_context/native_context are N4 (owner).
- **Open:** the app_card caps are a scout question for the Lead.

## Trail

- **Read:**
  - the spec (whole);
  - brief_pack.py:1167-1246, 1478-1517, 1532-1746, 1800-1830, 2140-2160, 2696-2711, 2780-2875, 3655-3716, 3855-4137, 4280-4625;
  - project_knowledge.py:60-71, 437-488;
  - s5_plan.py:1196-1237;
  - role_load.py:73-131, 448-527, 570-611;
  - retro_numbers.py:958-982;
  - driver_core.py:255-274;
  - driver_runner.py:263-293, 1212-1235;
  - driver_conductor.py:129-160;
  - driver_dispatch.py:205-274;
  - log_append.py:135-244;
  - person_words.py:1-185;
  - inject_context.py:200-289, 550-589, 690-734;
  - native_context.py:120-219;
  - story_step.py:444-461;
  - test_brief_pack.py:2408-2443;
  - test_ahead_cards.py:350-371;
  - told-before-work spec :262-275, 620-633;
  - SIBLING_MAP headings and axis 13;
  - the critic verdict schema.
- **Grep:**
  - the scoreboard spec and the amendment;
  - constants with and without digits;
  - clip and slice patterns;
  - removed names over PKG;
  - `_answer_note`, "--notes", `answer_row` (50 hits in 11 files);
  - story_load/static_load;
  - test-layers;
  - the DECISIONS.md negative, with control.
- **Not run:** no tests.

```json
{"verdict":"fit_with_fixes","blockers":["N0 dispatch: the DoD removes the --notes-file after the call, but owe_row stores the args and owed_rows_step replays them (driver_runner.py:276, driver_conductor.py:149): a failed first write loses the person's words; also a second writer of words files beside person_words.write_words (person_words.py:40-45) - write through write_words and keep the file"],"fixes":["K1: add to 5.6 with verdicts and owners: project_knowledge._lesson_line 200-char cut of a person's words, source_material out[:8] (brief_pack.py:1515), S4_REQUIRED_BY_CHARS :2788, roster clips :2812-2813/:2856/:2872, first-look problem clips :3861/:3891/:3939/:4015/:4019, _fit_code_file :2421 into N2 owns, :2152-2154, :2316, :3401, :1731; rerun the grep digit-aware and over callees","Decide the one-line words edge (24-200 KB folded line vs host per-read caps): one experiment, or render words from full with line breaks; add 200000-char and multi-paragraph edges","F4 ratchet: a path-normalised size helper in the test, key old to new per keep file; reconcile with section 6 deletions and test_ahead_cards :364-365","Queue lines for role-load.json, role_load.py, test_ahead_cards.py against T3a (told-before-work :625, :628)","PROJECT.md package change 6(a): one measurement of uncut brief sizes and longest line on recorded briefs, written into section 2","Section 6: name test_brief_pack.py :2414, :2425, :2426-2427","Minor: N0 stops calling person_words_whole; args.notes or None; temporal old cut journal notes; test_ahead_cards :366-375; argv 8191 via run-py.cmd; N-brief line format for P1-v; FR-55 window as residual of P1-v N6"],"class_completeness":"Class: size bound clipping brief content with its whole not one named step away; spec covers ~25 sites, missed a second person's-words cut (project_knowledge lessons), a silent material count cap (source_material out[:8]) and ~12 clip sites; axis 29 covered, 34 broken on N0 write side, 18 ratchet procedure missing, 5 holds; inject_context/native_context queued as N4; app_card caps are a scout question","trail":{"read":["docs/tasks/specs/20261113-fv1-4-no-brief-cut-spec.md","PKG/scripts/brief_pack.py (ranges above)","PKG/scripts/project_knowledge.py:60-71,437-488","PKG/scripts/role_load.py:73-131,448-611","PKG/scripts/driver_runner.py:263-293","PKG/scripts/driver_conductor.py:129-160","PKG/scripts/person_words.py:1-185","PKG/scripts/log_append.py:135-244","PKG/scripts/inject_context.py:200-289,690-734","PKG/scripts/native_context.py:120-219","PKG/scripts/driver_dispatch.py:205-274","told-before-work spec :262-275,:620-633"],"reruns":[{"command":"Grep -i removed names over PKG (count)","result":"381 hits / 26 files; brief_pack.py 72 control"},{"command":"Grep digit-aware constants in brief_pack.py","result":"9 lines incl S4_REQUIRED_BY_CHARS, S3_ROSTER_WHY_CHARS"},{"command":"Grep -i ceiling origin in read-main DECISIONS.md; control D-00","result":"0; control 23"},{"command":"Grep _answer_note over PKG/scripts","result":"def driver_core:263 + driver_runner:285, driver_machine:3309, :3889 only"}]}}
```

questions: none
needed beyond the manifest: PKG/scripts/project_knowledge.py, person_words.py, driver_conductor.py, driver_dispatch.py, story_step.py

# FV1-4 — no cut of a brief by size inside a factory run (DRAFT spec, designer → Lead)

Status: DRAFT for Lead acceptance; fix round t-502 after the critic on the plan (t-495, verdict
`docs/tasks/specs/reviews/20261113-fv1-4-plan-critic.md`) applied in place — what changed where: §9b. Forks are RETURNED (§9), not
decided. The spec is English (FR-30 applies to what the builder writes). Pile `live-run-fvf`, node FV1-4
(`batch-1-live-run-fvf.md:37`), finding `plans/piles/live-run-fvf/findings/20261112-srezka-briefa-rezhet-slova-cheloveka.md`
(read in worktree `findings-1413c`).

Owner's words (binding, verbatim): «в прогоне фабрики вообще не должно быть потолка, за потолком следит фордж. Максимум в ретро
это может отметить фабрика»; 12.11.2026: «код не должен урезать бриф, фордж следит за длиной брифа» (finding `:12`).

`PKG` below = `C:\QAFactory\forge-repo\.claude\worktrees\p1v-n3\ai-packages\qa-factory` — the code base FV1-4 lands on (origin/main +
P1-v N3's `_record_brief_size`). Every `file:line` is from that tree, read by this designer on 13.11.2026 (first draft and fix round).
Owns paths in the node headers are written against the repository root `C:\QAFactory\forge-repo\`; the Lead re-roots them to the
builder's worktree at dispatch (the worktree mirrors the tree).

---

## §0 Goal and DoD by class (as decided by the Lead — not narrowed here)

Inside a run there is NO cut of brief content by size — the person's words, the input files, the SD head, the request lines, and
every other section the brief carries — and NO line about a ceiling shown to a role or to the conductor. The result of
`brief_pack.build` has no `budget_bytes` / `over_ceiling` (and, consequently, no `omitted`). Size is written only as `bytes` in
`state/brief-sizes.jsonl`. A summary that points at a whole file ONE step away is not a cut. The by-range instruction for a brief
over `SLICE_BYTES` (30 000 B) stays: it is the guard's whole-read limit, not a brief ceiling. The factory may note a size in the
retro (S9) from the record's data, nothing more (this spec adds no such note: non-goal).

What the cut protected and what replaces it (FR-55, P11) — §2.

---

## §1 Architecture, owners, census (AR-29; CLAUDE.md rule 10, P27)

| AR | Touched how | Change check written into the DoD |
|---|---|---|
| AR-24 (a person's words reach whoever acts, whole) | the core of the node: words go whole into the brief (line breaks kept, §5.1) and the decisions side file; the journal note carries them whole by a kept words file (N0); a stand lesson's words are no longer cut at 200 (N1, §5.6 2a) | DoD N1 rows W-1…W-6 and keys (3), (11); DoD N0 rows J-1…J-5: "follow each answer to the command that consumes it" (`architecture.md:252`) — the answer reaches the next brief whole, including after an owed-row replay (J-5) |
| AR-14 (one artifact, one writer) | N0 writes each journal note file through `person_words.write_words`, "the ONE writer of that folder" (`person_words.py:40-45`), and keeps it; no second writer of `state/words` is added | DoD N0: no `open(`/`write_text` of a `state/words` path in the changed driver functions; `Grep "state\" / \"words\"|state_dir / \"words\""` over the N0 diff returns nothing new |
| AR-21 (what a stage gathers travels whole) | input-file lines are never popped; the SD head never drops DoD leads; `source_material` loses its silent `out[:8]` (§5.6 2b) | DoD N1 rows F-1…F-4, H-1…H-3 |
| AR-22 (every field produced has a reader, removing a producer re-homes its readers in one commit) | `budget_bytes`, `over_ceiling`, `omitted` leave `build`'s result; `ceiling`/`over`/`budget_bytes` leave the record; `BRIEF_MAX_BYTES`, `SD_HEAD_MAX_BYTES`, `DECISION_CHARS*`, `PERSON_WORDS_MAX`, `APPROACH_*SHORT/ONE_LINE/POINTER`, `measured_bytes`, `head_bytes` leave `brief_pack`; `LESSON_WORDS_SHOWN`, `LESSON_LINES_MAX` and the `more` key of `project_knowledge.lessons` leave with their reader in `gate_preflight.check_stand_lessons` (F9 a) | §4 reader table: every reader changes in the SAME commit as its producer; DoD: `Grep` of each removed name over `PKG\scripts`, `agents`, `skills`, `references`, `handoffs` (case-insensitive) with a positive control returns only the changed sites |
| AR-20 (shrink-only ratchets; a raise is named) | `test_brief_pack_s5_plan.DOORS_ONLY_BRIEF_MAX` (on `budget_bytes`) is re-based to path-normalised bytes; the per-role watch of `test_ahead_cards.py:364-365` moves to `test_brief_pack.py` (F8 b); `role-load.json` totals must not move (F3 a) | §7: per keep file key and old → new, or "deleted"; the number is measured by the builder with `harness.normalised_bytes` and written with a named raise line; the critic re-runs that one test |
| AR-13 (one reader per fact) | `person_words.read` is the one reader of a person's words given by file; N0's `--notes-file` reads through it; `person_words.lf` becomes the one place of the CRLF → LF rule for a person's words (m1) | DoD N0 rows J-3, J-4 |
| AR-4 (nothing tied to one machine) | `measured_bytes` (the path-independent count) is deleted from the product; the record keeps raw `bytes`; the TEST ratchet uses `harness.normalised_bytes` (temp root and plugin root replaced by a token) so its number is the same on CI and Windows | E-14 (record); §7 (ratchet) |
| AR-29 | no check the node removes is a census unit (census rows of `brief_pack.py` are only `judge_lines`, `plan_dispatch_lines`, `judgment-census.json:59-60`); `gate_preflight.check_stand_lessons` (census row `:392`, class `shape`, owner `data`) keeps its function name and class — only its display loses a count tail | §1a table; `test_judgment_census.py` is in the witness set only if `--witness-for` prints it |
| AR-12 (friction measured; code that makes a stage dearer is a defect) | briefs grow; the measure moves to the forge record; the growth is measured BEFORE N1 (N0m, §2) | §2 N0m table, E-15 |

Not touched: AR-1/2/3/5/6/8/9/10/11/15/16/17/18/19/23/25/26/27/28 — no data row, role judgment, config key, host read, refusal,
question form, stage twin, empty outcome, state exit, requirement unit or finding road changes. (AR-10: the brief still states
every check's requirement before the work; only its size changes. AR-16: the gate note of `check_stand_lessons` keeps its text form,
it only carries more lessons and whole words.)

### §1a Every check the node removes or alters — owner and census class

| Check | Where today | Change | Owner it served | Census class |
|---|---|---|---|---|
| brief body ≤ `BRIEF_MAX_BYTES` (the ladder and the last-resort pop) | `brief_pack.py:4487-4535` | removed (no replacement in the run) | data (code) — a size bound on text code assembled | shape (size), never a census unit |
| SD head ≤ `SD_HEAD_MAX_BYTES` (DoD leads and `given` names cut) | `brief_pack.py:3700-3713` | removed | data (code) | shape (size), not a census unit |
| request lines ≤ `BRIEF_MAX_BYTES // 2` (file names folded) | `brief_pack.py:3284` | removed | data (code) | shape (size), not a census unit |
| person's words ≤ 400 / 240 chars in the brief, ≤ 20 000 chars anywhere | `brief_pack.py:1599-1603, 1657-1664, 1695-1733` | removed | data (code) | shape (size), not a census unit |
| a stand lesson's words ≤ 200 chars; ≤ 10 lessons shown | `project_knowledge.py:441-442, 480-483` | removed (F9 a) | data (code) | shape (size); `check_stand_lessons` census row unchanged |
| brief size verdict in the package tests (`ceiling_verdict`, `DOORS_ONLY_BRIEF_MAX`, "≤ 6 KB" checks) | `test_brief_pack_s5_plan.py:441-514`, `test_brief_pack.py` (§6), `test_ahead_cards.py:364-365` | re-based / moved / deleted per §7 (F4 a, F8) | data (code) at DEV time — a forge check | shape (size) |
| static brief layer of the role load (A22) | `role_load.py:453-464, 521` | an allowance with the same number (F3 a) | data (code) at dev time | shape (size), census rows `role_load.py` unchanged |
| journal note ≤ 20 000 chars (argv transport) | `driver_core.py:263-269` | whole by a kept file (F2 a, N0) | data (code) | not a check: a transport cut |
| injected block ≤ 26 000 chars refuses a dispatch; native context ≤ 100 000 refuses a role | `inject_context.py:267-277`, `native_context.py:173-175` (census `:486`, `:652`) | node N4 of this spec, blocked on the owner's word (F6 a) | data (code) | shape (census rows `collect_blocks`, `stage`) |

No check is ADDED that classifies a role's judgment. The test ratchets of §7 are data checks at dev time (owner: data, through the
forge); the forge norm (owner: intent, through the forge) is P1-v N6's — non-goal.

---

## §2 Why the cut existed, and what replaces its protection (FR-55, P11)

- Origin: release 0.8.0 (2026-10-04) introduced the brief "≤ 6 KB" (`PKG\CHANGELOG.md:5820-5826`): a short packet every dispatch reads
  first, with the commands, so a role stops reading the plugin (TP1-13797: 106 of 711 automator calls read plugin scripts). The bound
  protected (a) the role's per-turn cost — the brief is read by a tool call and then re-read from cache on every later turn
  (`role_load.py:58`: "the brief, its side files and the form are read later, by tool calls"), (b) attention (the commands near the
  top), (c) the role-load census, which counts the brief at its ceiling (`role_load.py:453-464`, `role-load.json:2`).
- No decision record introduced it: `DECISIONS.md` and `docs/DECISIONS_ARCHIVE.md` (p1v-n3) hold no line on `6 KB|6144|BRIEF_MAX|brief
  budget|потолок брифа|бюджет брифа|brief_pack|brief…ceiling` (case-insensitive; positive control: `D-00` finds 23 lines in
  `DECISIONS.md`, `brief` finds 8 lines in the archive, none about a budget). The rationale lives only in the CHANGELOG and in specs
  (`docs/tasks/specs/t-042-pc2-6-briefs-over-ceiling.md` and its reviews).
- What replaces it OUTSIDE the run: the record `state/brief-sizes.jsonl` (`bytes` per dispatched brief, P1-v N3) read by the forge's
  scoreboard and judged against the forge norm (`norms.json`, P1-v N6 — non-goal here), and, until N6 lands, the two dev-time test
  ratchets of §7 on path-normalised bytes (F4 a, F8 b). Cost of compliance: briefs with long words or many inputs grow; measured growth
  is the scoreboard's number, never a run-time refusal (owner: «за потолком следит фордж»).
- What the run still bounds, legitimately: `SLICE_BYTES` (guard's whole-read limit → by-range note), the code side file
  `CODE_FILE_BYTES = 28 000` for excerpts (under the same guard limit; F5 a — every left-out excerpt is named), and summaries whose
  whole is ONE named step away.
- **FR-55 window — a residual owned by П1-в N6 (m7).** Between N1's merge and П1-в N6's merge nothing in a run or in the forge reads
  `state/brief-sizes.jsonl`; the only watch on brief growth is the two fixture ratchets of §7, which see the fixtures, not real stories.
  This window is closed by П1-в N6 (the forge norm over the record), not by this spec; the Lead names it in N6's node as its first
  reader of the record. Until then a real brief's growth is visible only by reading the record by hand.

### §2a The data premise, measured BEFORE N1 (PROJECT.md «Как принимается изменение пакета» п. 6(а); node N0m)

N1 is not dispatched before the table below holds numbers. The number decides three things: whether any real brief passes
`SLICE_BYTES` once the ladder is gone (E-6 in practice), the wrap width of F10, and the starting value of the forge norm (П1-в N6).

Measurement (N0m, §10): rebuild every primary brief of the two recorded stories with the ladder off, on COPIES (FR-53; command
hygiene 7(d): the live arm is never written):
- inputs: (1) cart-1 — `PKG\scripts\tests\fixtures\stories\cart-1\` (its `work\briefs\<dispatch>.md`, 116 files in the folder, the
  primary briefs are the names matching `^S\d-[a-z-]+-\d+\.md$`), installed into a temp project by `harness.temp_project` +
  `harness.install_artifacts(root, <cart-1 folder>, <ticket of its pipeline.json>)`; (2) LR2-1 — a byte copy of
  `C:\QAFactory\mybooks-stand\arm-factory\test-automation-framework\` without `node_modules\` and `.git\` into the session scratchpad
  (its story is `qa-factory\artifacts\LOCAL-1\`, 204 files under `work\briefs\`);
- command: `python -B <scratchpad>\fv1-4-n0m-measure.py --project <copy root> --ticket <ticket> --label <cart-1|LR2-1>` — a scratch
  script, NOT committed, attached in full source with its output (the doc-dispatch witness form: CLAUDE.md rule 11); it imports
  `PKG\scripts`, sets `CLAUDE_PROJECT_DIR` to the copy (as `harness.use_project` does), sets `brief_pack.BRIEF_MAX_BYTES`,
  `SD_HEAD_MAX_BYTES`, `DECISION_CHARS`, `DECISION_CHARS_MIN`, `PERSON_WORDS_MAX` to `10**9`, and for each primary brief calls
  `brief_pack.build(ticket, stage, role, dispatch, write=False)` (`write=False` records nothing: `brief_pack.py:4593`); stage, role and
  dispatch come from the file name (`S5-qa-automator-3` → `S5`, `qa-automator`, `S5-qa-automator-3`); the words' own longest line is
  `max(len(l) for l in "\n".join(brief_pack.decisions(pipeline, stage, role, ticket, project, task_root)[2]).splitlines())`; a build
  that raises is a row with the exception's class and message, never a skipped row;
- negative control: one dispatch whose name does not exist in the story is passed with `--only <name>` and must print a row
  `build_error` — a run that prints no such row is a miscall, not a measurement.

Result table — columns (one row per primary brief, then one totals row per source):

| source | dispatch | stage | role | recorded_bytes | recorded_longest_line | rebuilt_bytes | rebuilt_longest_line | words_longest_line | over_6144 | over_30000 | build_error |
|---|---|---|---|---|---|---|---|---|---|---|---|
| (rows: N0m report t-513, 13.11.2026, in the journal's `accepted t-513` witness and the session scratch folder `fv1-4-n0m`) | | | | | | | | | | | |

Totals measured 13.11.2026 (t-513; tree `wip/p1v-n0` bea0bb0; an estimate — no N2 changes, no fenced words, no F10 wrap):

| source | n | median rebuilt_bytes | max rebuilt_bytes | over_6144 | over_30000 | max words_longest_line | build_error |
|---|---|---|---|---|---|---|---|
| cart-1 | 26 | 13 129 | 15 382 | 26 | 0 | 259 | 0 |
| LR2-1 | 41 | 28 838 | 36 468 | 41 | 17 | 556 | 0 |

Read by the Lead: every uncut primary brief is over the 6 144 ceiling (the ladder cut every one of them); 17 of LR2-1's 41 (all S5:
automator 33 K, code critic 35–36 K) pass 30 000; the longest line of a person's words is 556, so F10's width of 1 000 stands.
The spec's negative control is a miscall: `build` does not raise on a dispatch id the story does not have (`brief_pack.py:4122` reads
it as an empty dispatch) — a finding of its own (a wrong id yields a plausible brief), not part of N1.

Totals row per source: `n`, median and max `rebuilt_bytes`, count `over_6144`, count `over_30000`, max `words_longest_line`.
Label: the rebuild approximates N1 (it does not apply N2's class-C changes, the fenced words rendering or F10's wrap): an estimate,
written with the date of the copy. The Lead writes the table here before N1's dispatch.

---

## §3 Facts read first (load-bearing, `PKG` tree)

Constants: `brief_pack.py:54` `BRIEF_MAX_BYTES = 6*1024`; `:55` `SD_HEAD_MAX_BYTES = 1024`; `:56` `SLICE_BYTES = 30_000`; `:57`
`DIGEST_CHARS = 200`; `:58` `DISPATCH_DIGESTS = 4`; `:59` `DECISION_CHARS = 400`; `:60` `DECISION_CHARS_MIN = 240`; `:64`
`PERSON_WORDS_MAX = 20000`; `:65` `MAP_INLINE_LINES = 14`.

Person's words: `person_words_whole` `:1591-1603` (cuts past 20 000 with "[cut: N more characters, the whole text is in <holder>]");
`WORDS_BY_REFERENCE` `:1610`; `question_answer_lines` `:1618-1666` (the `minimal` clause cut by `_short(key, DECISION_CHARS_MIN)`
`:1657-1659`; `shown` becomes a pointer when the line passes 400 `:1663-1664`); `decisions` `:1681-1743` (pairs
`_short(…, DECISION_CHARS)` / `_short(…, DECISION_CHARS_MIN)` at `:1695, :1709, :1716-1717, :1724, :1733`; an open halt with neither
`reason` nor `message` is `json.dumps(halt)[:200]` `:1731`; "every decision in full" `:1738-1740`; returns `(shown, minimal, full)`
`:1743`; `full` carries the other stages' overrides too, `shown` only this stage's `:1720-1726`). `_short` `:1093-1095` folds
whitespace and cuts with "...". `answers_of` `:1563-1588` reads `human_answer` notes of the project journal.

Stand lessons: `stand_lesson_lines` `:2696-2708` renders `project_knowledge.lessons(...)["lines"]`; `project_knowledge._lesson_line`
`project_knowledge.py:437-449` folds the words and cuts them at `LESSON_WORDS_SHOWN = 200` (`:64`) with " ..." and no pointer;
`lessons` `:452-487` caps at `LESSON_LINES_MAX = 10` (`:63`) with `(+k more: project_knowledge.py lessons --stand "<stand>")`; that
command (`cmd_lessons` `:979-1002`) prints the SAME capped `lines` — the pointer leads to the same cut list. Readers of `lessons`:
`brief_pack.stand_lesson_lines` and `gate_preflight.check_stand_lessons` (`gate_preflight.py:3210-3233`, uses `more` at `:3230-3231`).
`app_card.py:57` `LESSON_LINE_CHARS = 400` ("words cut at 200 by `project_knowledge.lessons`") renders lessons in the app card (the
app_card caps are a scout question, §9b row 2).

Collected material: `source_material` `:1474-1515` ends `return told + out[:8]` — no count line, no pointer; it includes "material the
person supplied" (`pasted-*`, `:1512-1513`).

Digests: `digests` `:1532-1560` — each digest `_short(…, DIGEST_CHARS)` `:1545, :1555`; dispatch scope `[:8]` silent `:1552`; only the
last 4 same-stage dispatches inline, then "N earlier dispatch(es) of S are in the side file" `:1557-1559`. The digests side file is
written only when `not inline_dig` (`:4499`, `:4580-4583`) — at the fullest level (`inline_dig=True`) the side file the line names is
NOT written: an existing broken pointer (a cut whose whole is not one step away).

Approach block: `APPROACH_SHORT_BYTES` `:2904`, `APPROACH_ONE_LINE` "(cut for room)" `:2908`, `APPROACH_POINTER` "not shown, the brief
is full" `:2912` — ceiling text that reaches a role; `approach_forms` returns `{2,1,0,-1}` `:2986-3011`.

Request lines: `request_lines` `:3259-3286` folds file names to `(+N more sites)` when the lines pass `BRIEF_MAX_BYTES // 2`
(`:3264-3265, :3270, :3284`; `_site_note` `names=False` `:3248-3249`). `MAX_REQUEST_LINES = 12` `:3235` with "N more, the list is in
<file>" `:3272-3273` (a pointer: stays).

SD head: `_form_line` `:3625-3635` clips a value over `line_chars` (300) with " ... (whole: <where>)" (a pointer: stays);
`measured_bytes` `:3638-3647` (plugin root replaced by a token before counting), `head_bytes` `:3650-3652`; the hard cap `:3700-3713`
pops DoD leads, then `given` names, then adds `head: — (head over cap: N budget B)`.

Record: `_record_brief_size` `:4116-4134` writes `budget_bytes`, `ceiling`, `over` only when the result carries `budget_bytes` /
`over_ceiling`; `bytes` only otherwise (P1-v N3's two worlds, tested `test_brief_pack.py:2145-2248`). Called only when
`write and output is None` (`:4593-4594`).

`build` `:4137-4595`: head lines `:4153-4248` (repair reason `_short(…, 200)` `:4194`; `Purpose: _short(…, 300)` `:4203`); input files
`:4292-4339` (`kind_of` pop tags `:4295-4300, :4319, :4322, :4326, :4328`; rows `[:8]` silent `:4314`; cases `[:8]` + "... and N more
case files of the scope, same folder" `:4317-4322`; test files `[:6]` with NO count line `:4324-4326`; the code side file line
`:4330-4335`; "first: the trimming below takes from the end" `:4338`); `trimmed_files` `:4394-4396`; `render` `:4399-4463` (`omitted`
`:4406-4417`; words levels `:4420-4429`; `## Not in the brief` `:4430-4431`; digests `:4435-4438`; `if ahead:` `:4446-4447` — T3b's);
`side` `:4465-4466`; ladder `attempts` `:4475-4476`; `form_cost` `:4478`; `sd_cost` `:4482`; `budget_of` `:4484-4485`; loop
`:4487-4502`; last resort `:4503-4535` (`files.pop` `:4533`); `over_ceiling`/`over_line` `:4536-4553` (role line `:4548-4550`); SLICE note
`:4554-4565`; `-files.md` side file `:4566-4567`; writes `:4569-4587`; result `:4588-4592`; record call `:4593-4594`. `main()`
`:4598-4625` (conductor line `:4620-4624`). `story_step._brief` takes the last line starting `brief: ` (`story_step.py:445-458`, RC2-2
already in code).

Journal note road (N0): `driver_core._answer_note` `driver_core.py:263-269` (calls `brief_pack.person_words_whole`); its callers
`driver_runner.answer_row` `driver_runner.py:282-286` (through `owe_row`), `driver_machine.py:3308-3312` (`py_trace` of
`defect_found`) and `driver_machine.py:3888-3889` (`self.py` of `human_answer`) — all pass the note as `log_append.py --notes <text>`
(`log_append.py:202`, default `""`). `owe_row` (`driver_runner.py:263-280`) saves a failed write with `"args": [str(a) for a in args]`
(`:276`); `owed_rows_step` replays those args (`driver_conductor.py:149`) and gives a row up after `OWED_ROW_TRIES`
(`:154-157`); `owe_row`'s ERROR DIRECTION: "a duplicate row is allowed …, a lost row is not" (`driver_runner.py:267-268`).
`--reason-file` reads through `person_words.read(args.reason or None, args.reason_file, "--reason", "--reason-file")`
(`log_append.py:207-215`); `person_words.read` refuses "both" whenever `inline is not None` (`person_words.py:144-148`).
`person_words.write_words(task_root, dispatch_id, kind, text)` (`person_words.py:172-203`): `<task root>/state/words/driver-<kind>-<ms>[-<n>].txt`,
UTF-8, `newline=""`, mode `"x"` (never overwrites), empty/whitespace-only → None, a failed write removes the half file and raises
`OSError`; the module "never deletes or rewrites" a words file (`:40-41`) and is "the ONE writer of that folder" (`:43-45`).
`Driver.words_file` (`driver_runner.py:321-…`) writes into `self.state_dir / "words"` with its own code (§12 item 6).
Command-line limits: the driver's list argv is bounded by the Windows command line (32 767 characters, `driver_runner.py:327`); any
call through `hooks/run-py.cmd` is bounded by cmd.exe's 8 191 characters (`run-py.cmd:27`) and cut at the first line break
(`person_words.py:3-7`).

Readers outside `brief_pack`: `role_load._brief_ceiling` `role_load.py:453-464` and the static `brief` layer `:521`, note `:715-716`;
`role-load.json:2` note ("the brief counts at its ceiling, brief_pack.BRIEF_MAX_BYTES"); `retro_numbers.py:962-980` prices the brief
layer of `static_load` in the S9 retro ("The brief is a ceiling by design"); `s5_plan._settled_lines` `s5_plan.py:1231-1233`;
`stand_identity.py:528-530`; `artifact-writers.json:203` (record's `why`); `changelog.d/p1v-n3-brief-sizes.md:2`.

Not readers (checked): `controller.py:9686-9752` has its OWN `BRIEF_MAX_BYTES = 1500` for `--brief` (a conductor summary with the whole
result in `state/output/controller-<op>.json`) — a summary one step away, not a role brief: out of class, unchanged (name collision
only). No file under `experiments/` or `tools/` of the p1v-n3 tree reads `budget_bytes|over_ceiling|brief-sizes|"omitted"` (the same
search finds `docs/` and `plans/` files outside the package: positive control). No `agents/`, `skills/`, `references/`, `handoffs/`
file tells a role about the ceiling (`Not in the brief|6 KB|budget B|brief…ceiling|cut for room|brief is full`, case-insensitive;
positive control `your brief` finds 27 lines in `agents/`); the recorded briefs under `scripts/tests/fixtures/stories/cart-1/work/briefs/`
carry it — recorded history, unchanged (E-12).

Tests: keep files (run in canon, `test-layers.json` `keep` = lines 35-7045): `test_brief_pack.py` `:286`,
`test_brief_pack_s5_plan.py` `:344`, `test_flow_requests.py` `:1739`, `test_gate_preflight.py` `:1864`, `test_readiness.py` `:4157`,
`test_project_knowledge.py` `:3976`, `test_role_load.py` `:4512`, `test_silent_passes.py` `:5123`, `test_story_run_refusals.py` `:5880`,
`test_whole_identifier.py` `:6776`, `test_ahead_cards.py` `:55`. Quarantine (`:7046`+): `test_brief_pack_manual.py`,
`test_brief_pack_roles.py`, `test_brief_pack_sd_head.py`, `test_brief_pack_timeout.py`, `test_brief_stand_helpers.py`,
`test_case_id_form_texts.py`, `test_project_approach.py`, `test_retro_prior_tried.py`, `test_role_digest_template.py`,
`test_s5_settled_oracle.py`.

---

## §4 Readers of every removed key / name — each changes in the SAME commit as its producer (AR-22)

| Removed | Reader | Change |
|---|---|---|
| result `budget_bytes`, `over_ceiling` | `brief_pack.main` `:4618-4624` | line becomes `brief: <path> (<bytes> B[, side files: a, b][, not written])`; prefix `brief: ` kept (RC2-2 reads it); the two ceiling clauses go (m6: the new format is named for П1-в in §10a) |
| same | `_record_brief_size` `:4127-4131` | the two `if` branches deleted; the line is always `{ts, stage, role, dispatch, bytes}` |
| same | tests: §6 rows | named expectation changes |
| result `omitted` | none in product code (`Grep "omitted"` in `brief_pack.py` hits only `render` and `window_code_file`'s own local of the same name `:2039-2422`, which stays) | tests §6 |
| `BRIEF_MAX_BYTES`, `SD_HEAD_MAX_BYTES` | `role_load._brief_ceiling` `:453-464`, `:521`, `:715`; `role-load.json:2`; `retro_numbers.py:962-966` (comment) | F3 (a): `role-load.json` `allowances` gains `"brief": 6144, "brief_charter_head": 1024`; `_brief_ceiling` → `_brief_allowance` reading them; layer reason `"allowance"`; notes reworded "brief at its allowance"; totals unchanged |
| `DECISION_CHARS`, `DECISION_CHARS_MIN`, `WORDS_BY_REFERENCE` | `question_answer_lines`, `decisions` | words whole (§5.1) |
| `PERSON_WORDS_MAX` | `person_words_whole`; `driver_core._answer_note` (docstring `:266`; N0 removes the call, m1); `s5_plan.py:1204` (docstring); `test_story_run_refusals.py:1307-1308` (N0 rewrites to literal sizes); `test_s5_settled_oracle.py:136` (quarantined, expected red) | §5.1, N0 |
| `APPROACH_SHORT_BYTES`, `APPROACH_ONE_LINE`, `APPROACH_POINTER` | `approach_forms` `:2993` | `approach_forms` returns the full list only (§5.4) |
| `approach_forms` dict shape `{2,1,0,-1}` | `project_approach_lines` `:2973-2975`, `build` `:4247`, `render` `:4409, :4432-4433` | `approach_forms(...) -> list` (the old `[2]`); `project_approach_lines` returns it; render renders it |
| `measured_bytes`, `head_bytes` | `build` (`form_cost`, `sd_cost`, `budget_of`), `sd_head_lines` cap | deleted with them; no product reader remains; the test-side size count is `harness.normalised_bytes` (§7) |
| `decisions()` 3-tuple, `question_answer_lines()` 3-tuples | `build` `:4369`; tests `test_brief_pack.py:1653, 1720, 1738, 1766, 2441, 3524, 3696`; `test_whole_identifier.py:171, 173`; `test_story_run_refusals.py:1293, 1304` | `decisions -> (shown, full)`; `question_answer_lines -> ([(full, shown)], said)`; every site re-unpacked |
| record keys `budget_bytes`, `ceiling`, `over` | P1-v W3 / scoreboard (not in this tree; P1-v spec `:220-224`, N-brief `:354`) | readers read `bytes` and ignore extra keys of old lines (E-11) — the P1-v amendment B4 already says so |
| `project_knowledge.LESSON_WORDS_SHOWN`, `LESSON_LINES_MAX`, `lessons()["more"]` | `_lesson_line`, `lessons`; `gate_preflight.check_stand_lessons` `:3230-3231`; `app_card.py:57` (comment only, names the old 200 cut); tests `test_project_knowledge.py:912, 915, 952-968`, `test_gate_preflight.py:2985-2987`, `test_brief_pack.py:2965-2967, 3011-3016` | F9 (a): the cut and the cap go; `more` leaves the result and its reader in one commit; the `app_card.py:57` comment is the app_card scout question's (§9b row 2), not edited here |

---

## §5 Mechanism — what `build` does when content is large

One rule: the brief is rendered ONCE, at its fullest form; nothing is measured against a size; nothing is dropped or shortened for
room. A section stays a summary only where its whole lives in a file the same section names (one step away).

### 5.1 The person's words (N1)
- `person_words_whole(words, project=None, holder="")` returns `person_words.lf(words)`: CRLF/CR → LF, nothing else (`person_words.lf`
  is added by N0, m1). `project`/`holder` stay in the signature (callers pass them) and are unused (small choice closed: kept,
  documented "kept for the callers; no cut, no pointer"). `_plain_words` (`:1613-1615`) becomes `person_words.lf(words).strip()`.
- One renderer for a words clause, `_words_block(head, words) -> str` (new, N1), used by `question_answer_lines` and `decisions` for
  every line that carries a person's words or a gate / warning / override / halt text:
  - words with NO line break and at most `WORDS_LINE_WIDTH` characters (F10; recommended 1 000): ONE line `head + " ".join(words.split())`
    — today's fitting form, so a brief whose words fit stays byte-identical for such lines (whitespace folding only, no character dropped);
  - words WITH a line break: the head line, then the words in a fenced block indented by two spaces, every line as given (only CRLF/CR →
    LF), so a line of the words that starts with `#`, `|`, `>`, `-` or a fence is literal text inside the block and never a heading,
    table or section of the brief (F7, recommended (a)). The fence is backticks, `max(3, longest backtick run in the words + 1)` long;
  - words with no line break and MORE than `WORDS_LINE_WIDTH` characters: F10 — recommended (b): the fenced block form with the text
    hard-wrapped at the last whitespace at or before `WORDS_LINE_WIDTH` (a run with no whitespace is split at exactly
    `WORDS_LINE_WIDTH`), no character dropped, and the head line ends `(lines over 1000 characters are wrapped here; the text as given:
    <decisions>)` so the side file is written and holds the bytes as given.
- `question_answer_lines`: per item `full = f"- {head}; {clause}"` with the words whole (as today's `full`); `shown =
  _words_block(f"- {head}; the person's words: ", words)` (the "not recorded" / "the same text as under Qn" clauses stay one line); no
  `minimal`. Returns `([(full, shown)], said)`.
- `decisions`: every `shown` entry is `_words_block(...)` of the same text `full` carries for it (`- answer: …`, `- gate A (…): …`,
  `- standing: …`, `- <stage> block "…" -> …`, `- open halt …: …`); an open halt with neither `reason` nor `message` shows
  `json.dumps(halt)` whole (`:1731`, finding 2g); no `_short`; no `minimal`. `full` keeps the other stages' overrides; `shown` keeps
  only this stage's (today's rule). The "- every decision in full: <decisions>" line is appended when `others` (decisions of other
  stages) > 0 OR any F10 wrap happened. Returns `(shown, full)`.
- `answers_of` (`:1563-1588`): a note recorded before N0 that ends with the old cut marker is re-worded per F13 (recommended (b)).
- `render`: the words section is `shown` with `<decisions>` replaced by the side-file path ONLY in lines `decisions` /
  `_words_block` appended themselves (the pointer lines), never inside a person's text; the levels 1 and 0 are deleted. The decisions
  side file is written when a pointer line carries `<decisions>`.

### 5.2 Input files (N1)
- No `files.pop`, no `trimmed_files`, no `<dispatch>-files.md`, no `doors` set, no `kind_of` tags, no priority tuple. `files` is
  rendered whole, in today's rendered order.
- `tests[:6]` (`:4324`) → every test file of the scope is listed (no cap). `rows[:8]` (`:4314`) → every row id. `cases[:8]` with "... and
  N more case files of the scope, same folder" stays (a pointer to the folder whose files are listed one step away). Small choice
  closed: the case list keeps its 8 + pointer because the folder is named by the 8 lines above it.
- `source_material` (`:1515`): `return told + out` — every collected file is listed (finding 2b, a REMOVED cut of the core class: it
  silently dropped "material the person supplied"). The docstring's "the cap of eight lines" sentence goes.
- The code side file line (`:4333-4335`): when `len(code_text.encode("utf-8")) > SLICE_BYTES`, the line adds ` - over 30 000 B: read it by
  range` (the guard's limit, the same clause family as the brief's SLICE note); otherwise unchanged. (It can pass 30 000 B only when
  F5 a names hundreds of left-out excerpts, E-29.)

### 5.3 The SD head (N1)
- `sd_head_lines`: `lines_for(leads, len(names))` once; no loops `:3706-3711`; no `head over cap` line `:3712-3713`. `_form_line`'s
  per-line clip at `line_chars` with " ... (whole: <where>)" stays — a pointer one step away (DoD wording).

### 5.4 Request lines, approach block, digests (N1)
- `request_lines`: one pass with `names=True`; the `for names in (True, False)` loop and the half-ceiling test go. `_site_note`'s
  `names` parameter is removed with its `False` branch. `MAX_REQUEST_LINES`, `SITE_FILES_SHOWN`, `FUNCTIONS_SHOWN` stay (pointers).
- `approach_forms` returns the full block (today's level 2, `APPROACH_LINE_CHARS` clip after the path stays: the line names its
  file). The three short-form constants go.
- Digests: inline always (today's attempt 0). `digests()` appends `- every digest in full: <digests>` when ANY digest was shortened by
  `DIGEST_CHARS` or ANY same-stage dispatch was left out by `DISPATCH_DIGESTS`; `render` replaces `<digests>` by the side-file path; the
  side file `<dispatch>-digests.md` is written when the digest lines carry `<digests>`. The dispatch scope `[:8]` in a digest line
  (`:1552`) is rendered whole. This closes the broken pointer of §3.

### 5.5 `build`'s remaining flow (N1)
`render(note: str = "") -> str` (no tuple, no `omitted`, no `over_line`, no level arguments). After render: the SLICE fixed point
(`:4554-4565`) stays, minus `over_ceiling.append`. Result keys: `task, stage, role, dispatch, scope, path, bytes, files, sides,
written, repo_map, markdown`. `sides` = `{"decisions": bool, "digests": bool}` by the `<…>` pointer rule. The record call is unchanged.
Head comments that say "never shrunk" / "under the 6 KB ceiling" (`:4173, :4242, :4245-4246, :4273, :4338`, `:4468-4477`, `:4480-4481`)
are reworded or removed (comments only; no role reads them).

### 5.6 Class-C summaries — bounds whose whole is NOT one named step away (N2, and N1 where named; F1 a)
Rule for every row below: when the bound shortens or drops anything, the same line (or the section's last line) names the carrier
of the whole; where no carrier exists (text the code derives), the bound is removed and the text rendered whole. "Whole, one line"
means `" ".join(str(x).split())` (whitespace folded, no character dropped).

**The class search (re-stated, digit-aware, over the callees; finding 2).** Surface: `brief_pack.py` line builders and the three modules
whose text they render — `project_knowledge` (lessons), `sizing.clip_name`, `app_card`. Patterns (Grep, `-n`, on each file):
(i) constants `^[A-Z][A-Z0-9_]*(CHARS|BYTES|LINES|SHOWN|MAX|LIMIT|CAP|NAMES|ROWS|MIN)[A-Z0-9_]*\s*=` — the digit in the class
`[A-Z0-9_]` is what the first draft lacked; positive control: it finds `S4_REQUIRED_BY_CHARS` (`:2754`) and `S3_ROSTER_WHY_CHARS`
(`:2800`), the two names the critic's reproduction found; on `brief_pack.py` it returns 63 lines; (ii) call sites
`_short\(|_clip\(|_stand_short\(|clip_name\(|\[:\d+\]|\[:[A-Z][A-Z0-9_]+\]` — on `brief_pack.py` every hit is a row below, a row of
§5.1-5.5 (N1), or a line of the "stays" list. Callees: `project_knowledge.py` `LESSON_SUBJECT_MAX`, `LESSON_WAIT_MAX_S` (input
checks, not display — stay), `LESSON_LINES_MAX`, `LESSON_WORDS_SHOWN` (rows 2a, F9); `sizing.py` `NAME_SHOWN` / `clip_name` (row 2h;
`NAMES_ON_LINE` is a person-facing gate/report line with the whole list in `sizing.json` — out of the brief class, stays);
`app_card.py` `CARD_MAX_BYTES`, `FIRST_LOOK_REQ_MAX`, `FIRST_LOOK_REQ_LINES`, `FIRST_LOOK_LINE_CHARS`, `LESSON_LINE_CHARS`,
`LINE_CHARS`, `PROFILE_LINES`, `NOTE_LINES`, `NOTE_CHARS`, `PAGE_OBJECT_LINES`, `_clip(a, 60)` `:208` — NOT decided here: a scout
question for the Lead (§9b row 2).

| Site (`brief_pack.py` unless named) | Bound | Today | Change | Node |
|---|---|---|---|---|
| `case_form_lines` `:427-428, :463-469` | `CASE_FORM_LINE_CHARS` 300 (clip), `CASE_FORM_PROBLEMS_SHOWN` 3 ("N more problem(s) are not shown") | derived text, no carrier | both bounds removed: every problem, whole | N2 |
| `branch_check_line` `:594, :609` | `BRANCH_WHY_CHARS` 200 | `:594` names `base_rel` in the same line (stays); `:609` does not | `:609`: when clipped, append ` (whole: <base_rel>)` | N2 |
| `expectation_change_lines` `:697-700, :722` | `EXPECTATION_NAME_CHARS` 160 per name; `EXPECTATION_WHY_CHARS` 300 | the full-list pointer appears only past 8 names; reasons derived | names: when any name is clipped, the line ends with `The full list, with its fields: <EXPECTATION_POINTER>` (already the ≤ 8 tail `:706`); reasons: whole | N2 |
| `proof_required_lines` `:745, :789, :805` | `PROOF_NAME_CHARS` 160; `PROOF_WHY_CHARS` 300; `_clip(…, 120)` | pointer only past 8 | names: when any clipped, append ` - the full list: work/automation-manifest.json`; reasons/exception text: whole | N2 |
| `side_lines` `:876-877, :898` | `SIDE_LINE_CHARS` 160 (×2) | pointer only past 6 sides | when any line clipped, the last line says `whole: pipeline.json \`sides\`` | N2 |
| `_assumption_lines` `:965-972` | `HEAD_LINE_CHARS` ×2 / ×1 | factory text from data files, no carrier | clip removed | N2 |
| `_bind_lines` `:1002-1003, :1020` | `PROVISIONAL_LINE_CHARS` 200 (×2) | pointer only past 6 | when any clipped, last line `whole: work/automation-manifest.json \`provisional\` / \`unresolved\`` | N2 |
| `delta_lines` `:2455`; `_delta_tail` `:2484, :2489, :2498, :2501` | `_short(reason, 400)`, `_short(problem, 200)`, `_short(expected/fix, 160)`, `_short(exc, 100)` | the repair reason and the reviewer's problem/expected/fix are the words the role acts on | all whole, one line | N2 |
| `build` head `:4194`, `:4203` | repair reason 200, purpose 300 | dispatch record words, no carrier named | whole, one line | N1 (inside `build`) |
| `_stand_short` `:2516-2517` (`STAND_WHY_CHARS` 80, SILENT slice, no "...") and its callers `_stand_address_lines` `:2608`, `_case_actor_lines` `:2651`, `_repo_stand_lines` `:2667`, `manual_stand_lines` `:2727` | reasons in the stand section | silent cut | renamed `_stand_text(text)` (no `limit`), whole, one line; `STAND_WHY_CHARS` removed; the four callers drop their limit argument | N2 |
| `_stand_names` `:2520-2521` (`STAND_ROLES_MAX` 8, "(+N more)") and `STAND_CASE_LINES_MAX` `:2742-2744` (`manual_stand_lines`) | count bounds with no carrier | | removed: every name / every case line; `_stand_names(names, limit=None)` keeps the `limit` parameter accepted and unused (callers pass `FIRST_LOOK_ROLES_MAX`, a T3b constant this spec does not edit, §10a) | N2 |
| `STAND_PATHS_MAX` `:2669-2670`, `STAND_HELPER_NAMES` `:2687` | "(+N more: <map path>)" | pointer | stays | — |
| `_timeout_entry` `:3206`; `test_timeout_line` `:3222-3224` | `TIMEOUT_WHY_CHARS` 120; `TIMEOUT_PROFILES_SHOWN` 3 "(+K more profiles)" | no carrier | why: whole; profiles: every profile | N2 |
| `fit_target_lines` / `_fit_row_line` `:3083-3084, :3094` | `FIT_ABSENT_CHARS` 160 | the row is in `work/test-plan.json` | when clipped, append ` (whole: work/test-plan.json <row id>)` | N2 |
| `blast_radius_line` `:1818-1819` | reason `room` | the line names `blast-radius.json` | stays; failure branch `:1824` `[:120]`/`[:BLAST_LINE_MAX]` → whole exception text, one line | N2 |
| every `_short(exc, N)` in a "could not …" line: `_s5_kind` `:1869`, `_plan_cap` `:1880`, `plan_dispatch_lines` `:1907, :1929`, `plan_lines` `:1984`, `_CodeCollector.read` `:2118`, `_CodeCollector.extends` `:2200`, `prior_retro_lines` `:3615, :3620, :3622` | exception / reason text | no carrier | whole, one line | N2 |
| **2a** `project_knowledge._lesson_line` `project_knowledge.py:440-442` (`LESSON_WORDS_SHOWN` 200, " ...", no pointer) — a person's words | what a person taught about the stand | silent cut of a person's words, the core defect's class | **REMOVED**: the words whole, one line (`_plain(" ".join(words.split()))`, today's fold, no character dropped); `LESSON_WORDS_SHOWN` deleted; docstring of `lessons` `:456` reworded; and the count cap per F9 (a): `LESSON_LINES_MAX` and the `(+k more: …)` line removed, every lesson a line, `more` key removed with its reader `gate_preflight.check_stand_lessons` `:3230-3232` (the note lists every lesson) | N1 |
| **2b** `source_material` `:1515` `out[:8]` | collected material incl. "material the person supplied" | silent count cap, no line, no pointer | **REMOVED**: every collected file listed (§5.2) | N1 |
| **2c** `s4_stand_lines` `:2788` `_clip(words, S4_REQUIRED_BY_CHARS=80)` | what the project says of who needs an integration | pointer only past 15 lines (`:2789-2790`) | when any `required_by` text is clipped, that line ends ` (whole: <RP.HOME>/config.json, environment.integrations)` | N2 |
| **2d** `_s3_roster_line` `:2812-2813` (`_clip(role, 60)`, `_clip(story, 40)`) | roster names | the section's first line names the registry `roster_file` (`:2859`) whenever a roster line exists | **stays — why**: the line above names the file holding the whole name | — |
| **2d** `s3_roster_lines` `:2856` `_clip(problem, S3_ROSTER_WHY_CHARS=120)` | an unreadable registry's reason | no carrier | whole, one line; `S3_ROSTER_WHY_CHARS` removed | N2 |
| **2d** `s3_roster_lines` `:2872` ("Removed by the person" line, `_clip(role, 60)`, `_clip(story, 40)`) | names the person removed | names `roster_file` only past 15 | when any name or story is clipped, the line ends ` (whole: <roster_file>)` | N2 |
| **2e** `first_look_input_line` `:3861` (`_clip(problem, 160)`), `_first_look_accounts` `:3891` (`_clip(problem, 80)`), `first_look_runner_lines` `:3939` (`_clip(why, 120)`), `_fl_state` `:4015` (`_clip(problem, 80)`), `:4019` (`_clip(problem, 120)`) | problem / why text | no carrier | whole, one line (no `FIRST_LOOK_*` constant edited) | N2 |
| `first_look_runner_lines` `:3934` (`FIRST_LOOK_REQ_CHARS` 70) | requirement statement | the line above names the register (`:3932`) | stays — why: the register holding each whole text is named one line above | — |
| `_first_look_accounts` / `first_look_runner_lines` (`FIRST_LOOK_ROLES_MAX` via `_stand_names`) | count, no carrier | | follows `_stand_names` (removed bound); **no `FIRST_LOOK_*` constant is edited** (T3b owns them) | N2 |
| `_fl_line` `:3996-3997` (`FIRST_LOOK_LINE_CHARS` 180) and `first_look_lines` `:4097` | per-line clip | `+N more: work/first-look.yaml` only past 12 | when any line is clipped in `_fl_line`, `first_look_lines` ends the block `whole: work/first-look.yaml` (constant untouched) | N2 |
| **2f** `_fit_code_file` `:2419-2421` ("... and N more", no names) | left-out excerpts when even the bare file is over `CODE_FILE_BYTES` | no carrier | F5 (a): every left-out excerpt named by `file:lines`; the second `while` loop goes; the file may then pass 28 000 B (E-29) | N2 |
| **2f** `_shared_fixture_lines` `:2356-2383` ("(+K more fixtures not listed)"; per fixture "(+N more)" instances under `SHARED_FIXTURE_INSTANCES` 20 and the `SHARED_SECTION_BYTES` 6 000 share) | the shared-fixture section | derived from the manifest, no carrier | F5 (a) "every fixture named" applied with the §5.6 rule: every fixture and every instance named; `SHARED_FIXTURE_INSTANCES`, `SHARED_SECTION_BYTES`, `SHARED_TAIL_RESERVE` removed (the per-fixture instance tail has no carrier either — flagged for the Lead in §9b row 2f) | N2 |
| **2f** `_CodeCollector.helper_lines` `:2152-2154` (`unread[:4]` "(+N more)") | test files not read | no carrier | every unread file named | N2 |
| **2f** `_CodeCollector.reached_by_receipted` `:2315` (`broken[0]` "and N more"), `:2316` (`_short(closure_notes[0], 160)` "(+N more)") | fixtures that could not be read; closure notes (a list of notes, not exception text) | no carrier | every broken id named; every closure note whole, joined by "; " | N2 |
| **2g** `exploration_lines` `:3401` (`str(exc)[:60]`) | exception text | no carrier | whole, one line | N2 |
| **2g** `decisions` `:1731` (`json.dumps(halt)[:200]`) | an open halt with no reason/message | no carrier | whole (§5.1) | N1 |
| **2h** `walk_lines` `:3305` (`sizing.clip_name`, `NAME_SHOWN` 60) | a function's name the strategist must name in a row's `walks` | the register's `## Functions` is named only past 8 functions | the brief line uses the whole name, one line (`" ".join(str(f["name"]).split())`); `sizing.clip_name` stays for its person-facing callers | N2 |
| `REFERENCES_SHOWN`, `FIRST_LOOK_REQ_MAX`, `FIRST_LOOK_LINES_MAX`, `FIT_LINES_MAX`, `MAP_INLINE_LINES`, `MAX_REQUEST_LINES` (incl. `exploration_cell_lines` `:3362-3365`), `SITE_FILES_SHOWN`, `FUNCTIONS_SHOWN`, `APPROACH_DOCS_MAX`, `APPROACH_LINE_CHARS`, `EXPECTATION/PROOF_NAMES_SHOWN` (incl. `base_log_lines` `:1073-1074`), `SIDES/PROVISIONAL/PENDING_SHOWN`, `S4_INTEGRATIONS_MAX`, `S3_ROSTER_MAX`, `HELPER_NAMES` (`(+N more: repo map)`), `CANDIDATE_LINE_MAX` (the rest named by id), `EXCERPT_LINES` (the excerpt names its range), plan notes `HEAD_LINE_CHARS` `:1994` (the slice file named in the same head) | pointer in the same line/section | | stay (not a cut) | — |
| `_sha12` `:518` (`[:12]`), `_log_of_attempt` `:1031` (`[:1]`), `DIFF_ALL_LINES` `:183` (a command argument) | not brief content: a short commit id git resolves, a lookup, a flag value | | stay (out of class) | — |
| `window_code_file` excerpts under `CODE_FILE_BYTES` 28 000 with "## Left out (N excerpts; 28000 B is the limit of this file): read these by range" | the code side file under the guard's read limit | F5 (a) | stays (the cap and the by-range list) | — |

---

## §6 Existing tests that pin the cut — named expectation changes (no silent edits)

Keep files only. Quarantined files are NOT run, fixed or edited (`plans/builder-rules.md` 7b); their expected reds are listed in the
handoff: `test_brief_pack_sd_head.py`, `test_brief_pack_roles.py`, `test_brief_pack_manual.py`, `test_project_approach.py`,
`test_case_id_form_texts.py`, `test_brief_stand_helpers.py`, `test_role_digest_template.py`, `test_retro_prior_tried.py`,
`test_s5_settled_oracle.py` (references `BP.PERSON_WORDS_MAX` `:136`). A comparison of brief text below is on whitespace-folded text
(`" ".join(text.split())`) wherever the words may sit in a fenced or wrapped block (F7, F10), so the rows hold under either option.

`test_brief_pack.py` (N1 unless marked N2):

| Function (line) | Old expectation | New expectation |
|---|---|---|
| `left_out_sources` (`:234-300`) | (no row on the count cap) | NEW variant row (2b): 12 collected files (4 `mr-*.md`, 8 `pasted-*.txt`) → 12 lines plus the `told` lines, none missing; AT 8 and BEYOND 9 files: every file named |
| expectation scenario, edge 5 (`:765-776`) | 10 KB gate words: `budget_bytes ≤ 6 KB`; `sides["decisions"] is True` | the whole gate text (`"Keep every UI case in scope. " * 400`, folded comparison) is in the brief; `sides["decisions"] is False`; changed-test line and count present (kept) |
| `proof_lines` (`:873`) | 12 instances: `budget_bytes ≤ 6 KB` | row deleted (size is the forge's and §7's); count/names rows kept |
| blast-radius M13 (`:1523-1534`) | AT / 1 byte BEYOND a patched ceiling | rows deleted; `real_ceiling` save/restore removed (`:1466, :1558`) |
| `labelling_vocabulary_lines` (`:1600-1610`) | AT / BEYOND ceiling keeps the line | rows deleted (`:1568, :1638` restore removed) |
| `p4_min_words` (`:1711-1742`) | minimal line cut at 240 + pointer | renamed `p4_words_whole_short`; on `shown` (`[s for _f, s in …]`): words of 239, 240, 241 chars — all whole, no "the whole text is in"; same-words-once and whitespace-fold rows kept; empty/blank/None/0 rows assert the "not recorded" clause on one line |
| `p4_long_words` (`:1745-1776`) | at 400 inline; 401 → pointer; minimal cut; H24 20 000 whole, 20 001 cut naming answers file | 400 and 401: `shown` carries the words whole, no `<decisions>`; `decisions(...)[0]` carries no `<decisions>`; H24: 20 000 and 20 001 (and 24 576) whole in `full` and `shown` (folded comparison), no `[cut:`; NEW rows: a 3-paragraph answer → `shown` keeps its line breaks inside one fenced block (E-23); an answer with a line `## Heading` and a line `| a | b |` → both inside the fence, the brief's `## ` section list unchanged (E-24); an answer holding a ```` ``` ```` run → the fence is longer than that run (E-30); a 200 000-char one-line answer → F10 (b): no line of `shown` over 1 000 characters, folded text equals the words, the head line carries `<decisions>` (E-22) |
| `p4_build` (`:1856-1868`) | body ≤ 6 KB; level-1 cut names the side file | size row deleted; a 300-char Q1 answer is whole in the brief; no `<decisions>` literal (kept); no "the whole text is in" for Q1 |
| `sc1_10_lines` B-K7 (`:2087-2126`) | ceiling 1: doors never trimmed; `-files.md` named | rows replaced by: every line of `result["files"]` of the roomy build is in the brief and no `*-files.md` exists under `work/briefs/` after a written build |
| `p1v_n3_brief_size_record` (`:2145-2248`) | (a) keys incl. `budget_bytes, ceiling, over`; (d) AT/BEYOND; (e) bytes-only world | (a) keys exactly `ts, stage, role, dispatch, bytes`, values from the result; (d) deleted; (e) kept as the only world; (b)(c)(f) kept; ceiling patching removed; NEW (F8 b, §7): per role of `stages.json` on the shared fixture, `harness.normalised_bytes(result["markdown"], root) <= ROLE_BRIEF_BYTES_MAX[role]`, a role missing from the dict is red naming it, and the verdict helper is pinned AT (green) and AT + 1 (red) |
| approach scenario (`:2324-2410`) | levels ≤ 200 B, AT/BEYOND 200, "(cut for room)", 1-byte / 2 KB ceilings (`:2405-2410`), under 6 KB | `approach_forms` returns a list; "the full block is in every brief of the three roles"; rows on `APPROACH_SHORT_BYTES`, the one-line form, the ceiling loop `:2405-2410` and 6 KB deleted; nothing-recorded row kept (`APPROACH_NOTHING`) |
| approach scenario, overflow tail (`:2412-2427`, finding 7) | `:2414` "overflow, approach recorded: under 6 KB" (`budget_bytes <= 6 * 1024`); `:2425` `over["sides"]["decisions"] is True`; `:2426-2427` the words whole in `S5-qa-automator-1-decisions.md` | `:2414` deleted (size is §7's); `:2425` → `over["sides"]["decisions"] is False` (the words are inline, `others == 0`, no F10 wrap: the line is 11 618 characters of words with no line break — under F10 (b) it IS wrapped, so the row reads `over["sides"]["decisions"] is (WORDS_LINE_WIDTH < len(words))`, i.e. True under (b), False under (a)); `:2426-2427` → the words (folded comparison) are in `over["markdown"]` itself; under F10 (b) the decisions file also holds them as given; `:2421-2423` (the same needles with and without the approach) kept unchanged |
| `s5_build_at`, `s5_ceiling` (`:2466-2485`) | ceiling bisection helpers | deleted with every caller row |
| `n4_scenario` (`:2488-2622`) | W3, W4, W9, W2, W5, W7, empty map, W6, W8 | W3 kept; "no `## Not in the brief` section" in EVERY build of the scenario; W4 deleted; W9 → digests inline, and with a digest over `DIGEST_CHARS` the line `- every digest in full: …-digests.md` is present and the file written; W2 kept minus the budget equality (`:2559-2560`); W5 → no `-files.md` ever; W7 kept; empty-map row deleted; W6 (60 × 380-char warnings) → each warning whole, no over line, decisions side file not written, waiver line kept; W8 (150 warnings) → `bytes > SLICE_BYTES`, `top[2]` is the by-range note (kept), the `over_ceiling` row deleted; AR-24 gate-A rows kept |
| `ss1_11_stand_lessons` E48 (`:2963-2967`) | one line, the words cut at 200 with ' ...' and the wait shown | one line, the 1 000-char words whole (no ' ...'), the wait shown (2a) |
| `ss1_11_stand_lessons` E47 (`:3009-3016`) | 10 lessons → 10 lines no pointer; 11 → 10 lines + the pointer quoting the stand | 10 → 10 lines; 11 → 11 lines, no `more:` pointer (F9 a) |
| E54 (`:3017-3032`) | ceiling 1: head holds the lesson lines; "each lesson cut at 200"; over-budget line | `:3018` kept (every lesson line whole in the head); `:3020-3032` deleted (the ceiling patch and the cut-at-200 row) |
| S1 SD head (`:3302`) | head within `SD_HEAD_MAX_BYTES` | every DoD lead of the charter is in the head; no `head over cap` |
| S5 fixture (`:3380-3399`) | ≤ 6 KB; `bytes − budget_bytes` = form + head; ceiling is 6144 | deleted; the section and SD head present (kept) |
| 7 KB build / short words (`:3441-3484`) | 7 KB budget, `input file(s)` omitted, 10 KB words ≤ 6 KB | the S5 waiver line and the 10 KB gate words whole; no `omitted` reference |
| decisions call sites (`:1653, :2441, :3524, :3696`) | 3-tuple | 2-tuple `(shown, full)` |
| rows of the §5.6 N2 functions (`:751-762`, `:875-880` and the C-rows of the same functions) — N2 | clip / count AT and BEYOND | per site: AT the bound, one BEYOND (the carrier line present, or the text whole), a 10× value |

`test_project_knowledge.py` (N1, 2a and F9 a): `:912`, `:915` the expected dicts lose `"more": 0`;
`test_lessons_cap_ten_lines_and_cut_the_words_at_200` (`:952-959`) → renamed `test_lessons_every_line_and_the_words_whole`: 11 lessons
of 1 000-char words → 11 lines, none ends ' ..."', no `(+1 more` line, no `more` key; the store row keeps the words (kept);
`test_lessons_at_ten_no_pointer_and_words_at_200_and_201` (`:962-968`) → words of 200 and 201 characters both whole, no " ...".

`test_gate_preflight.py` (N1, F9 a): `test_stand_lessons_are_one_note_never_a_card` 11-lessons block (`:2977-2987`): `:2985` → no
"and 1 more" in the note; `:2986` → `notes[0].count(': "words ') == 11` and "op11" is in the note; `:2983`, `:2984`, `:2987` kept.

`test_brief_pack_s5_plan.py`: N1 — `:199` (§7 row), `ceiling_verdict` and `DOORS_ONLY_BRIEF_MAX` (`:439-453`) and the K7 verdict rows
(`:497-514`) → §7: `S5_PLAN_BRIEF_BYTES_MAX` and `size_verdict(n)` pinned AT (green) / AT + 1 (red); N2 — the K7 row `:486-487` ("the
words cut at 80") → the 200-char reason is in the line whole (`_short(why, 80)` at `brief_pack.py:1907` removed); `window_code_file`
rows `:222-303` and C-K13 `:694-706` per F5 (a).

`test_ahead_cards.py` (N1): `:364-365` "brief under 6 KB" → deleted (the per-role watch moves to `test_brief_pack.py`
`p1v_n3_brief_size_record`, F8 b); `:366-376` (the same brief without the card lists the same files) → deleted (m4: with no trimming the
row is trivially true; the "no input file is ever dropped" invariant is N1 DoD key (4) on the shared fixture); `:361-363` kept.

Other keep files: `test_flow_requests.py:207-210` (B5 under half the ceiling) → deleted; `:230-236` → inverted: with 12 requests of 200+
char URLs every line keeps `(also in p1.tsx, p2.tsx, p3.tsx, +1 more)`; `test_role_load.py:123-124` (K-S6) →
`(layers["brief"]["bytes"], layers["brief"]["reason"]) == (allowances.brief [+ brief_charter_head for a charter], "allowance")` (F3 a);
`test_readiness.py:740-756` (the pointer path of a cut answer) → the four rows become one: `person_words_whole("x" * 20001, root) == "x" * 20001`;
`test_whole_identifier.py:171, 173` and `test_story_run_refusals.py:1293, 1304` → 2-tuple (N1);
`test_story_run_refusals.py:1306-1317` (row (3)) → N0: literal sizes (no `brief_pack.PERSON_WORDS_MAX`): answers of 20 000, 21 000
and 40 000 characters are each in their `human_answer` note whole, no `[cut:`; docstring INVARIANT reworded "whole, any size"; NEW
row (5) J-5 (owed-row replay) in the same function (§10 N0).

---

## §7 Ratchets (AR-20) — key, old → new, reason; the procedure

The size helper (N1, `PKG\scripts\tests\harness.py`, new function only): `normalised_bytes(text, *roots) -> int` — every given root and
the plugin root (`harness.PLUGIN`), each in both separator spellings and without a trailing separator, longest first, is replaced by
the token `<root>`; an empty root is skipped; the result is the UTF-8 byte length. It is the test-side twin of the deleted
`brief_pack.measured_bytes` (`:3638-3647`), extended to the temp project root, so the same fixture brief weighs the same on CI and on
Windows (the CI/Windows gap of `DOORS_ONLY_BRIEF_MAX`, `test_brief_pack_s5_plan.py:441`, was the temp-path length).

Procedure (the builder, inside N1; no CI round needed): (1) add the helper and the new constants with the value `0`; (2) run the one test
file of each constant once locally; each prints `RATCHET <key>[ <role>] <n>` for every measured brief before it asserts; (3) write each
printed `<n>` as the constant's value with the named raise line `# FV1-4 N1 (AR-20): re-based from <old key/unit> to normalised bytes
(harness.normalised_bytes); measured <date> on <machine>` ; (4) run the file again: green; the report attaches both runs. The critic
re-runs that one test file (the control re-run of the mechanical layer); a number that differs on CI is a defect of the helper (a path
not under a replaced root), not a re-type.

| Key (keep file) | Old | New | Reason |
|---|---|---|---|
| `test_brief_pack_s5_plan.DOORS_ONLY_BRIEF_MAX` (`:441`) | 6443 (budget B, raw, CI-measured) | renamed `S5_PLAN_BRIEF_BYTES_MAX`; value = `harness.normalised_bytes` of the K7 full brief (`build(CRITIC, "S5-plan-critic-1")`, `:495`) as measured by step (2); `ceiling_verdict` → `size_verdict(n)`: green at or under the constant, red above; the "doors only" branch goes | the unit `budget_bytes` and the trimmer's reasons no longer exist |
| `test_brief_pack.ROLE_BRIEF_BYTES_MAX` (new dict, in `p1v_n3_brief_size_record`) | none in this file; the per-role watch was `test_ahead_cards.py:364-365` (6144 budget B per role) | `{role: n}` for every role of `stages.json` on the shared fixture, measured by step (2) | F8 (b): the per-role watch moves out of a file T1r rewrites |
| `test_brief_pack.py` size rows `:873`, `:1856-1868` (size row), `:2414`, `:3380-3399` | ≤ 6 KB / budget equalities | deleted | covered by `ROLE_BRIEF_BYTES_MAX` |
| `test_ahead_cards.py:364-365` | ≤ `BRIEF_MAX_BYTES` per role | deleted | moved (row above) |
| `role-load.json` `ratchet_tokens`, `process_ratchet_tokens` (12 + 12 rows) | as `role-load.json:10-37` | unchanged (F3 a: the allowance keeps the number) | the static brief layer keeps its size |
| `judgment-census.json` | — | unchanged for N0-N2; N4 (F6) alters rows `inject_context.collect_blocks` `:486`, `native_context.stage` `:652` | — |

---

## §8 Edges (each with the invariant it protects)

| # | Edge | Behaviour | Invariant |
|---|---|---|---|
| E-1 | a person's answer of 24 KB (24 576 chars) to 18 questions | the brief's words section carries all of it: each answer whole, an answer with line breaks in its own fenced block with its line breaks kept (F7 a), one over `WORDS_LINE_WIDTH` with no break wrapped per F10 | no question's words are ever absent from the next role's brief (the live-run defect: Q3–Q18 lost) |
| E-2 | words of 239 / 240 / 241 chars (old `DECISION_CHARS_MIN`) | whole at all three | no word is cut at any length |
| E-3 | words of 399 / 400 / 401 chars (old `DECISION_CHARS`) | whole at all three, no `<decisions>` pointer instead of words | a pointer never stands in place of words |
| E-4 | words of 20 000 / 20 001 / 40 000 chars | whole in brief and side file; in the journal note only after N0 (F2 a) — before N0 lands, N1 must NOT run (order N0 → N1, §10) | a journal write never fails for a note's length; a note never claims a whole text that is elsewhere |
| E-5 | brief at 6 144 B and 6 145 B (old ceiling) | identical construction; no section changes at the boundary | size never changes content |
| E-6 | brief over 30 000 B | the by-range note is the line after the title (fixed point, today's `:4554-4565`); nothing else changes | the role can read the whole brief (guard limit); the note is the guard's, not a ceiling |
| E-7 | SD head at 1 024 B and 1 025 B (old cap) | every DoD lead and every `given` name (each line still clipped at `line_chars` with `(whole: …)`) | no DoD lead is dropped |
| E-8 | hundreds of input files (e.g. 300 test files of a scope) | every test file listed (no `[:6]`), every row id listed; cases keep 8 + folder pointer | every input a role is told to read is named in its brief or one named step away |
| E-9 | a side file the brief names is missing (decisions/digests not written: `--output`, `--dry-run`, an `OSError`) | `--output`/`--dry-run`: the pointer line says " (side files not written in this run)" (the existing clause of the over line, moved to the `every … in full` lines and the F10 wrap line); an `OSError` on write propagates as today (no new catch) | a pointer never names a file that this build claims exists but did not write |
| E-10 | digests: one digest over 200 chars, or 5+ same-stage dispatches | `- every digest in full: <path>` line + side file written | a shortened digest always has its whole one step away (closes today's broken pointer) |
| E-11 | TEMPORAL — records written before FV1-4 (lines with `budget_bytes`, `ceiling`, `over`) | stay as written; the package reads none; forge readers read `bytes`, ignore extra keys | no reader of the record breaks on either world; the package never compares a size in a run |
| E-12 | TEMPORAL — briefs and `-files.md` side files written before FV1-4 (stories in flight, fixtures `cart-1`) | never rewritten; a rebuilt brief (`start` again) has no `## Not in the brief`; old `-files.md` stay on disk, unnamed | a new brief never points at an old side file |
| E-13 | TEMPORAL — `role-load.json` before N1 has no `allowances.brief` | N1 writes the keys in the same commit as the reader; `settings()` default for a missing key = the old numbers (6144 / 1024) — a project copy of an older release still loads | role load never raises on an older settings file |
| E-14 | the record's `bytes` depends on the length of the paths printed (AR-4) | recorded raw (what the role pays); `measured_bytes` deleted from the product; the test ratchet uses `harness.normalised_bytes` | the forge compares sizes within one stand; the package claims no cross-machine number; the test number is the same on every machine |
| E-15 | role cost grows (long words, many inputs) | measured by N0m before N1 (§2a), then by the record and the scoreboard; the fixture ratchets of §7 watch the fixtures meanwhile | no run-time refusal or cut for cost; FR-55 detector moves to the forge (П1-в N6; the window is the residual of §2) |
| E-16 | POSITIONAL — removed ladder branch: words section | stays the first `## ` section after the head; the digest template stays the last section | the person's words come before everything they could be pushed out by (W3) |
| E-17 | POSITIONAL — removed last-resort branch: input files | `files` keep their rendered order (`plan_files` first); doors are rendered as before | no line that was a door can disappear (a door now cannot go at all) |
| E-18 | POSITIONAL — SLICE note | after the title, before the SD head (`head[:2] + note + head[2:]`, today's order) | the by-range instruction is read before any other content |
| E-19 | CONFLICT — FV1-4 vs P1-б row `:839` ("…несёт слова целиком **или называет файл слов**") | FV1-4 follows the finding (`:21-22`: "Слова человека в бриф идут целиком") and amendment B4 (P1-б E9: "слова в брифе целиком") | the stricter reading; the P1-б row is reported (§12), not edited |
| E-20 | empty / blank / non-string words | the existing "not recorded" clause (unchanged), one line | an absent word is said, never silently dropped |
| E-21 | words with CRLF, tabs, NBSP | one-line words (no line break, ≤ `WORDS_LINE_WIDTH`): whitespace folded (today's fitting-line form); words with a line break: lines as given inside the fence, CRLF/CR → LF only; `full` keeps LF | the text is not altered beyond whitespace folding on one line, or LF normalisation in the block |
| E-22 | a 200 000-character answer with no line break | F10 (b, recommended): fenced block, hard-wrapped at ≤ 1 000 characters per line, folded text equal to the words, head line names the decisions side file which holds the bytes as given; F10 (a): one line of 200 000 characters | no character is dropped; under (b) every line of the brief is readable by a by-range read (a range read cannot split one line) |
| E-23 | a multi-paragraph answer (blank lines between paragraphs) | one fenced block, every line and blank line kept | the paragraph structure the person wrote reaches the role (no fold into one line) |
| E-24 | an answer whose line starts with `#` / `## ` (a markdown heading) or `|` (a table mark) or `>` | inside the fenced block, literal (F7 a); the brief's own `## ` sections are only those `render` writes | a person's text can never open, close or impersonate a section of the brief (W3's "words first" stays checkable) |
| E-25 | `log_append` fails once on a `human_answer` row (N0, J-5) | the row is owed with args `--notes-file <absolute path of the kept file>`; `owed_rows_step` replays it; the journal note equals prefix + words whole | a lost row is not allowed (`driver_runner.py:267-268`): the words survive the failure in the kept file |
| E-26 | TEMPORAL — owed rows saved before N0 (args carry `--notes <text>`) | replayed unchanged: `log_append` keeps `--notes` | a row owed in one release replays in the next |
| E-27 | TEMPORAL — journal notes recorded before N0 that end with the old marker `[cut: N more characters, the whole text is in <journal>]` | F13 (b, recommended): `answers_of` re-words the marker only when it matches exactly at the end and the note is at least 20 000 characters before it | a pointer that leads to the same cut is never shown as if it led to the whole |
| E-28 | 12 collected source files (2b); 11 stand lessons, lesson words of 200 / 201 / 1 000 / 200 000 chars (2a, F9 a) | every file named; every lesson a line, its words whole (one line, folded); the gate note lists every lesson | collected and taught material is never dropped silently |
| E-29 | the code side file when hundreds of excerpts are left out (F5 a) | every left-out excerpt named; the file may pass 28 000 / 30 000 B; when over 30 000 B the brief's code-file line says to read it by range (§5.2) | an excerpt is never left out unnamed; the guard's limit is said, not hidden |
| E-30 | words containing a run of backticks (e.g. ```` ``` ````) | the fence is one backtick longer than the longest run (min 3) | the person's text can never close the block early |
| E-31 | the note file cannot be written (full disk, no folder; N0) | F12 (a, recommended): `OSError` propagates and stops the driver with its own error, as `Driver.words_file` does (`driver_runner.py:335-337`); the words are never put on the command line instead | a person's words are never cut silently by a fallback road |
| E-32 | the story folder moved between the failed write and the replay (N0) | the replay is refused by `person_words.read` naming the missing file; the row stays owed and becomes the seam's question after `OWED_ROW_TRIES` (existing); the kept file is still in the moved folder | a lost row is said, never silent |
| E-33 | `--notes-file` together with `--notes "<non-empty>"`; `--notes-file` with the default `--notes ""` | refused naming both / accepted (`args.notes or None`, m2) | the default empty inline value is not words and never blocks the file road |

Reused function in a more consequential role: `person_words_whole` becomes the ONLY road of the words into the brief with no cut. Error
direction allowed: toward MORE text (never fewer characters than given). Adversarial inputs that must stay on the safe side: a 40 000-char
answer; a 200 000-char one-line answer (E-22); an answer containing the literal `<decisions>` or `[cut:` (rendered as words; `build`
replaces `<decisions>` only in lines it appended itself — the pointer lines, not the person's text); an answer with a `## ` line, a `|`
line or a backtick run (E-24, E-30); a lone surrogate (cannot reach here: the driver decodes answers with `replace`,
`driver_machine.py:3315`; if met, written with `errors` as today).
Second reused function: `person_words.write_words` becomes the road of every journal note file (N0). Error direction: a duplicate file
is allowed, an overwritten or a deleted one never (mode `"x"`, no delete — the module's own rule); a blank note writes nothing and the
row passes `--notes` with the blank note exactly as today. Adversarial inputs: two notes in the same millisecond (the `-<n>` suffix);
a note of 40 000 characters with line breaks (written as given, `newline=""`).

---

## §9 Forks — RETURNED (options, consequences, recommendation)

**F1. Class-C summaries (§5.6) — in this spec or out?** (a) node N2 of this spec (one road: rule 6 — the rest of the class is a named
node, not an exclusion); (b) a separate finding/pile row. Cost of (a): ~25 sites, one builder, function-disjoint from N1. *Recommended:
(a).*

**F2. The journal note carries the person's words through argv (`log_append --notes`).** Removing the 20 000 cut makes a long answer a
command line Windows may refuse — 32 767 characters for the driver's own list argv (`driver_runner.py:327`), 8 191 and a cut at the
first line break for any call through `hooks/run-py.cmd` (`run-py.cmd:27`, `person_words.py:3-7`) (m5) — and `--reason-file` exists
because "a command line cuts a multi-line text", `log_append.py:193-194`. (a) add `--notes-file <path>` to `log_append.py`, read by
`person_words.read` (AR-24's change check, AR-13), and pass every `_answer_note` through it (`driver_runner.py:285`,
`driver_machine.py:3309, :3889`) — the note is whole at any size; (b) keep a transport cut in `_answer_note` only (renamed
`JOURNAL_NOTE_ARGV_MAX`), pointer corrected to `state/driver-answers.jsonl`, and make `answers_of` read the whole from there; (c) leave
it (a 24 KB answer passes; a 33 KB one fails the row). *Recommended: (a)* — one road, no second reader. Cost: one option in
`log_append.py`, three call sites in driver files (`driver_machine.py` is a hot file of other piles: function-disjoint owns).

**F3. The static brief layer of the role load and the S9 retro's rules cost.** (a) `role-load.json` `allowances.brief: 6144` and
`allowances.brief_charter_head: 1024`, labelled "allowance" (the same number, honestly named an estimate; totals and all 24 ratchet
rows unchanged; the retro prices the allowance as today); (b) the brief layer becomes "per story" (`bytes: null`) like `brief_sides`:
totals drop, every ratchet row must be re-measured, `retro_numbers` marks every role unmeasured; (c) the retro reads mean bytes per
role from `state/brief-sizes.jsonl` (the owner allows a size in the retro "from the record's data"; a new reader in S9). *Recommended:
(a) now; (c) as a later forge-side node if the Lead wants the retro to show real sizes.*

**F4. Size checks inside the package tests (`DOORS_ONLY_BRIEF_MAX`, "≤ 6 KB" checks).** A test runs at dev time — that is the forge
watching, not the run. (a) keep ONE fixture ratchet per keep file, on `bytes` (§7), named raise at re-base; (b) delete every package-side
size check, the forge norm (P1-v N6) is the only watch. *Recommended: (a)* until N6 lands — otherwise nothing watches brief growth in
between (FR-55). (Fix round: the unit is path-normalised bytes and the builder measures it, §7; which keep files keep one is F8.)

**F5. The code side file `<dispatch>-code.md` (`CODE_FILE_BYTES = 28 000`).** Its cap keeps the file under the guard's whole-read limit
— the same family as `SLICE_BYTES`, which the DoD keeps; but its fitter drops excerpts ("Left out (N excerpts; 28000 B is the limit of
this file): read these by range" — a pointer to source ranges) and, past that, "... and N more" (no names) and "(+K more fixtures not
listed)" (no carrier). (a) treat as guard-limit family: keep the cap and the by-range list, remove only the two unnamed tails (every
left-out excerpt named; every fixture named) — N2; (b) remove the cap: the file grows past 30 KB and the role reads it by range (as the
brief does); (c) out of scope. *Recommended: (a).*

**F6. In-run refusals by context size: `inject_context.MAX_BLOCK_CHARS` (26 000, refuses a dispatch, `inject_context.py:267-277`) and
the Codex native-context limit (100 000, `native_context.py:173-175`).** Same class (owner: no ceiling in a run), but the 100 000 is the
host's real limit (P25: host settings are given) and both functions are owned by T3a of the told-before-work spec (`collect_blocks`,
spec `:630`). (a) node N4 of this spec: owns `inject_context.collect_blocks` (the size branch) and `native_context.stage`, lands AFTER
T3a, direction set by the owner (Appendix A of the told-before-work spec `:685-701`); (b) a separate finding only. Rule 6 makes (b) a
defect ("a line 'tell the owner' closes nothing"). *Recommended: (a)*, node executable only after the owner's answer. Owner question
(plain language): «Когда текст, который фабрика сама собрала для роли, больше, чем принимает Codex, — что делать: отдавать большие
файлы проекта роли ссылкой (роль дочитает сама), или делить пакет на части? Сейчас фабрика роль не запускает.»

### Forks returned in the fix round (t-502) — each node is executable by its recommendation until the Lead answers

**F7. How a multi-line answer is rendered so a `## ` / `|` line of the person's text cannot read as part of the brief (decision 3).**
Two renderings are defensible: (a) the words in a fenced block indented by two spaces under their head line, fence =
`max(3, longest backtick run + 1)` backticks — markdown and a plain reader both see literal text; cost: two fence lines per multi-line
answer; (b) every continuation line prefixed by `  > ` (a blockquote under the bullet) — lighter, but a quoted line starting with `#`
still renders as a heading inside the quote in markdown viewers, and a `>` line of the person's own becomes a nested quote.
*Recommended: (a)* — the only form whose content is literal by definition. Drafted in §5.1 per (a).

**F8. Which keep files keep a size ratchet (decision 4: "per keep file").** (a) literally one per keep file that has a size check
today: `test_brief_pack_s5_plan.py`, `test_brief_pack.py` (one fixture), `test_ahead_cards.py` (per role) — but `test_ahead_cards.py` is
rewritten by T1r (all 12 cards migrated, "pin removed", told-before-work `:625`, `:391`), so its ratchet would be lost or conflict; (b)
two: `S5_PLAN_BRIEF_BYTES_MAX` in `test_brief_pack_s5_plan.py` and the per-role `ROLE_BRIEF_BYTES_MAX` in `test_brief_pack.py`
`p1v_n3_brief_size_record` (which already builds one brief per role of `stages.json`), `test_ahead_cards.py:364-365` deleted; (c) one:
only the S5 plan fixture — leaves every other role unwatched until П1-в N6. *Recommended: (b).* Drafted in §6/§7 per (b).

**F9. The stand-lesson count cap (`LESSON_LINES_MAX` 10, found in this round).** Its pointer `(+k more: project_knowledge.py lessons
--stand "<stand>")` names a command that prints the SAME capped list (`cmd_lessons` `:992-1001`), so the 11th lesson reaches no one: a cut
whose whole is not one step away. (a) remove the cap in `lessons()`: every lesson a line; the `more` key leaves the result and its
reader `gate_preflight.check_stand_lessons` (`:3230-3232`) in one commit (AR-22); cost: `gate_preflight.py` is a hot file (function
`check_stand_lessons` only) and three test rows (§6); (b) keep the cap in `lessons()` and make `cmd_lessons` print every row, so the
pointer is true — cheaper, but a role without a shell (the pointer is a command) still cannot reach the 11th lesson, and two readings of
one list exist (P31). *Recommended: (a).* Drafted per (a), owner N1.

**F10. A one-line answer longer than a host reads in one line (decision 3's "no fold of a long answer into one line" leaves the
no-line-break case open).** A host's Read may cap a line or a call (the critic saw a per-call cap of 25 000 tokens in this harness; a
per-line cap of ~2 000 characters in Claude Code's Read is an estimate, not verified), and range reads go by line, so a range read cannot
split one 200 000-character line. (a) render as given: one line, the side file identical — relies on the host; (b) inside the words
section only, hard-wrap such words in a fenced block at the last whitespace at or before `WORDS_LINE_WIDTH` = 1 000 characters (a run with
no whitespace split at 1 000), no character dropped, the head line names the decisions side file, which holds the bytes as given;
(c) wait for N0m's `words_longest_line` and decide then. *Recommended: (b)* — the safe side the Lead chose without an experiment; the
width is revisited if N0m shows real lines far below it. Lessons (2a) stay one folded line under every option (a lesson is one display
line by `lessons()`'s contract and the gate note joins lessons by "; "); a lesson over 1 000 characters is E-28's 200 000 row — one line,
no character dropped — and is the same question if the Lead wants it extended.

**F11.** (number not used — kept free so the Lead's references to F7-F13 stay stable.)

**F12. The note file cannot be written (N0, E-31).** (a) the `OSError` propagates and stops the driver with its own error — the same
behaviour as its sibling `Driver.words_file` (`driver_runner.py:335-337`: "the words are NOT passed on the command line instead");
(b) fall back to `--notes <text>` on the command line (the road that cuts at 32 767 / 8 191 characters and at a line break); (c) record
the row owed with no args and a marker — a row that can never replay. *Recommended: (a)* — a full disk fails the owed-row save
(`save_state`) too; no silent cut road is added.

**F13. Journal notes recorded before N0 carrying the old cut marker (m3).** The marker "[cut: N more characters, the whole text is in
<journal>]" (`brief_pack.py:1601-1603`, written through `driver_core.py:269`) names the very file that holds the cut note. (a) render as
recorded — the role is sent to a file that does not have the rest; (b) `answers_of` re-words an exact trailing match of
`\[cut: (\d+) more characters, the whole text is in [^\]\n]+\]$` — only when the text before it is at least 20 000 characters, so a
person who typed such a tail in a short answer keeps it — to `[cut when it was recorded, before FV1-4: <N> more characters are not in the
journal; the whole answer is in this story's state/words/ files, named by state/driver-answers.jsonl]`; (c) (b) and also read the whole
from those files — a second reader of the answers (AR-13), rejected. *Recommended: (b)*; owner N1 (`answers_of`). The match reads
the factory's own marker, never a person's wording (FR-12 holds).

**F14. Queue order on the three files shared with T3a (finding 5, §10a).** (a) `FV1-4 N1 → T3a` (N1 is drafted and waits only for N0
and N0m; T3a waits for T1); (b) `T3a → FV1-4 N1`; either way the function lists are disjoint and the later merger merges `main` and
resolves (PROJECT.md «Командная работа» п. 3). *Recommended: (a)*; if T3a is ready first, the Lead flips the line in both specs (one edit
each).

Closed by the designer (small, no design weight): `person_words_whole` keeps its parameters unused; `decisions` / `question_answer_lines`
return 2-tuples (no dead middle element, AR-22); `measured_bytes` / `head_bytes` deleted (no product reader left); one-line words keep
today's whitespace-folded form (briefs whose words fit stay byte-identical); the case list keeps 8 + folder pointer; the conductor line
keeps `bytes` (a size is not a ceiling); `controller.BRIEF_MAX_BYTES` (1 500) untouched (out of class). Fix round: the one place of the
CRLF → LF rule for a person's words is a new pure `person_words.lf(text)` (N0 adds it; `_answer_note` and, after N0 merges,
`brief_pack.person_words_whole` / `_plain_words` call it — m1); the owed row stores the note file's ABSOLUTE path (a replay may run with
another working directory); the note file's kind word is `journalnote` (file `driver-journalnote-<ms>.txt`); the size helper lives once
in `harness.py` (two test files use it; no clone); `_stand_short` becomes `_stand_text` without a limit (its name would lie);
`_stand_names` keeps an unused `limit` (T3b's constant is passed to it); the per-fixture instance tail of `_shared_fixture_lines` is
removed with the fixture tail (same rule, flagged in §9b row 2f); the K7 hint row of `test_brief_pack_s5_plan.py:486-487` belongs to N2
and the ceiling rows of the same function to N1 (row-disjoint; the later merger resolves).

---

## §9a Lead acceptance of the draft, 13.11.2026 (t-486) — forks

| fork | decided | by | note |
|---|---|---|---|
| F1 | (a) class-C summaries are node N2 of this spec | Lead | rule 9: the rest of the class is a named node |
| F2 | (a) `--notes-file` in `log_append.py`, read by `person_words.read`; every `_answer_note` goes through it | Lead | one road for a person's words (AR-24); N0 |
| F3 | (a) `role-load.json` allowances, labelled an estimate; totals and ratchets unchanged | Lead | (c) real sizes in the retro stays a later forge-side node |
| F4 | (a) one fixture ratchet per keep file on `bytes`, re-based by measurement on CI | Lead | until П1-в N6 lands, something must watch growth (FR-55) |
| F5 | (a) the code side file keeps its guard-limit cap; both unnamed tails are removed | Lead | N2 |
| F6 | (a) node N4 here, BLOCKED on the owner's word and on T3a | owner | her question is asked in plain language; nothing else waits for it |

Queue on shared files: `driver_core.py`, `driver_runner.py`, `driver_machine.py` are written by П1-в N0 (commit 079dc63,
in code review) — `очередь: П1-в N0 → FV1-4 N0`, N0's worktree is cut from the N0 branch after its fix round;
`brief_pack.py`: `очередь: П1-в N3 (9fa6fd2, `_record_brief_size`) → FV1-4 N1 ∥ N2 → T3b`.
Next: critic on the plan (core of `brief_pack`, ratchets re-based, a meaning change of the result keys), then N0.

## §9b Fix round after the critic on the plan (t-495)

Verdict: `docs/tasks/specs/reviews/20261113-fv1-4-plan-critic.md` (ACCEPT WITH FIXES). Lead decisions of the intent brief t-502 applied;
what a decision left open is a fork (F7-F14, §9).

| Finding | What changed | Where |
|---|---|---|
| 1 (blocks N0) | N0 writes each note through `person_words.write_words(<task root>, "", "journalnote", note)` and KEEPS the file; "removes it after the call" is gone from the DoD; new row J-5 "log_append fails once → the owed row replays from the kept file → the note equals the words whole"; TEMPORAL stated: owed rows saved before N0 carry `--notes <text>` and still replay; AR-14 added to §1; edges E-25, E-26, E-31 (F12), E-32 | §1 (AR-14, AR-24), §3 journal note road, §8 E-25/E-26/E-31/E-32, §9 F12, §10 N0 (owns, edges, DoD) |
| 2a | `project_knowledge._lesson_line`'s 200-character cut of a person's words: REMOVED (core class); with it the count cap whose pointer leads to the same cut list (F9 a); test rows in `test_project_knowledge.py`, `test_gate_preflight.py`, `test_brief_pack.py` `ss1_11_stand_lessons`; owner N1 | §3 stand lessons, §4 last row, §5.6 row 2a, §6, §8 E-28, §9 F9, §10 N1 owns |
| 2b | `source_material` `out[:8]`: REMOVED (core class, AR-21); test row in `left_out_sources`; owner N1 | §1 (AR-21), §3, §5.2, §5.6 row 2b, §6, §8 E-28, §10 N1 owns |
| 2c | `s4_stand_lines` `S4_REQUIRED_BY_CHARS` clip: the line names `config.json, environment.integrations` when clipped; owner N2 | §5.6 row 2c, §10 N2 owns |
| 2d | roster: `_s3_roster_line` role/story clips "stays — why" (the section's first line names `roster_file`); the problem clip `:2856` whole; the "Removed by the person" clip `:2872` names `roster_file` when clipped; owner N2 | §5.6 rows 2d, §10 N2 owns |
| 2e | first-look problem/why clips `:3861, :3891, :3939, :4015, :4019` whole; `:3934` stays (register named above); `_fl_line` named as the clip's real site; owner N2 | §5.6 rows 2e, `_fl_line` row, §10 N2 owns |
| 2f | `_fit_code_file` (the "... and N more" tail) and `_CodeCollector.helper_lines` (`:2152-2154`) and `_CodeCollector.reached_by_receipted` (`:2315` ids, `:2316` notes — a list, not exception text) enter N2's owns; the per-fixture instance tail of `_shared_fixture_lines` is removed with the fixture tail — FLAGGED: F5 (a) named two tails, this third one has no carrier either and is applied by the §5.6 rule; the Lead may keep it instead | §5.6 rows 2f, §8 E-29, §10 N2 owns; the code-file line clause in §5.2 (N1) |
| 2g | `exploration_lines` `str(exc)[:60]` (N2) and `decisions` `json.dumps(halt)[:200]` (N1) whole | §3, §5.1, §5.6 rows 2g, §10 N1/N2 owns |
| 2 (class grep) | re-stated digit-aware with a positive control (`S4_REQUIRED_BY_CHARS`, `S3_ROSTER_WHY_CHARS`), over the call patterns and over the callees `project_knowledge`, `sizing.clip_name` (new row 2h: `walk_lines` uses the whole function name, N2), `app_card`; the `app_card` caps are NOT decided — scout question for the Lead: «Is `app_card.py`'s card read by a role inside a run (injected, or named in a brief)? If yes, which of `CARD_MAX_BYTES` (8000), `FIRST_LOOK_REQ_MAX/LINES/LINE_CHARS`, `LESSON_LINE_CHARS` (400 — after 2a a lesson longer than ~400 is clipped in the card where it was cut at 200 before), `LINE_CHARS`, `PROFILE_LINES`, `NOTE_LINES/CHARS`, `PAGE_OBJECT_LINES`, `_clip(a, 60)` `:208` drop content whose whole is not named one step away? Is `app_card.CARD_MAX_BYTES` the constant T3a (i) removes?» | §5.6 class-search paragraph and row 2h; N2 DoD key (c) |
| 3 | the words section is rendered from `full` with line breaks KEPT (no fold of an answer with line breaks); one renderer `_words_block`; edges: 200 000-character answer (E-22), multi-paragraph (E-23), heading/table marks (E-24), backtick runs (E-30); two defensible renderings returned as F7 (rec. fenced block); the no-line-break 200 000 case returned as F10 (rec. wrap at 1 000 in the words section) | §5.1, §6 `p4_long_words` rows, §8 E-1/E-21/E-22/E-23/E-24/E-30, §9 F7/F10 |
| 4 | ratchet procedure: `harness.normalised_bytes` (temp root and plugin root → token), measured by the builder, named raise line, critic re-runs the one test; per keep file key and old → new or "deleted", reconciled with §6 and `test_ahead_cards.py:364-365`; the "which files" choice returned as F8 (rec. two ratchets) | §1 (AR-4, AR-20), §6, §7 (rewritten), §9 F4 note and F8, §10 N1 owns/DoD |
| 5 | `очередь:` lines with function lists for `role-load.json`, `role_load.py`, `test_ahead_cards.py` against T3a (and T1r), plus the exact mirror line the Lead adds to the told-before-work spec; order returned as F14 | §10a |
| 6 | new first step N0m — measurement: command, inputs' paths, result table columns, negative control; N1 not dispatched before the numbers are in §2a | §2a, §10 order and N0m |
| 7 | `test_brief_pack.py:2414` (deleted), `:2425` (decisions side file false — or true under F10 b), `:2426-2427` (words in the brief itself) listed with new expectations | §6 row "approach scenario, overflow tail" |
| m1 | N0 stops calling `brief_pack.person_words_whole`; the one place of the LF rule is the new `person_words.lf` (N0), which N1's `person_words_whole` / `_plain_words` call | §4, §5.1, §9 closed choices, §10 N0 owns/DoD |
| m2 | `args.notes = person_words.read(args.notes or None, args.notes_file, "--notes", "--notes-file")` | §8 E-33, §10 N0 DoD |
| m3 | old "[cut: …]" journal notes: returned as F13 (rec. (b): re-word the exact legacy marker in `answers_of`) | §5.1, §8 E-27, §9 F13, §10 N1 owns |
| m4 | `test_ahead_cards.py:366-376` deleted (trivially true without trimming; the invariant lives in N1 DoD key (4)) | §6 `test_ahead_cards.py` paragraph |
| m5 | the argv figure corrected: 32 767 for the driver's list argv, 8 191 and a cut at the first line break through `run-py.cmd` (`run-py.cmd:27`) | §3 journal note road, §9 F2 |
| m6 | the new conductor-line format named for П1-в: `brief: <path> (<n> B[, side files: <a>, <b>][, not written])`; the token N-brief counted (`, over the 6144 budget B ceiling …`) disappears | §4 first row, §10a (П1-в line) |
| m7 | the FR-55 window named as a residual owned by П1-в N6 | §2 last bullet, §8 E-15 |

## §9c Lead acceptance of the fix round, 13.11.2026 (t-503) — forks F7–F14

Owner away: every row is decided by the designer's recommendation («решила сама», reversible until the owner's word).

| fork | decided | by | note |
|---|---|---|---|
| F7 | (a) multi-line words in a fenced block, fence = max(3, longest backtick run + 1) | Lead | the only rendering whose content is literal by definition |
| F8 | (b) two ratchets: `S5_PLAN_BRIEF_BYTES_MAX` and the per-role `ROLE_BRIEF_BYTES_MAX` in `test_brief_pack.py`; `test_ahead_cards.py:364-365` deleted | Lead | T1r rewrites `test_ahead_cards.py`; a ratchet there would be lost |
| F9 | (a) the lesson count cap and the `more` key removed, `gate_preflight.check_stand_lessons` in the same commit | Lead | a pointer to the same capped list reaches no one; P31 |
| F10 | (b) hard-wrap at `WORDS_LINE_WIDTH` = 1 000 inside the words fence, no character dropped; the decisions side file holds the bytes as given | Lead | the host's line cap is an estimate, not verified; the width is revisited after N0m's `words_longest_line` |
| F12 | (a) `OSError` propagates | Lead | same as the sibling `Driver.words_file`; no silent cut road |
| F13 | (b) `answers_of` re-words the exact legacy marker (text before it at least 20 000 characters) | Lead | reads the factory's own marker, never a person's wording (FR-12) |
| F14 | (a) `FV1-4 N1 → T3a`; flipped in both specs if T3a is ready first | Lead | mirror line added to the told-before-work spec §7 |
| §9b 2f | the per-fixture instance tail of `_shared_fixture_lines` is removed with the fixture tail | Lead | same rule as F5 (a): a tail with no carrier |
| §9b 2 (`app_card` caps) | NOT decided here: scout question dispatched; the answer becomes a row of N2 or a finding | Lead | N2 is not dispatched before the scout's digest is accepted |

Order now: N0m (measurement, no repository write) ∥ N0 → N1; N2 after the `app_card` digest.

---

## §10 Nodes (for a weaker model; owns by FUNCTION; witness via `scenario_walk.py --witness-for`)

Order: **N0m (measurement) ∥ N0 → N1**; N1 is dispatched only when N0 is merged AND the N0m table is in §2a. **N2** is independent of
N0, N0m and N1 (it uses no helper they add) and runs in parallel with them (function-disjoint owns in `brief_pack.py`; the later merger
merges `main` and resolves — PROJECT.md «Командная работа» 3). N4 after T3a and the owner's word. T3b (told-before-work, wave 4) lands
AFTER N1/N2 and owns `ahead_card`, the `ahead` assignment, `FIRST_LOOK_*`, `_row_field_lines`, `dispatch_groups`: N1/N2 do not edit
those names, and `render`'s `if ahead:` lines (`:4446-4447`) are carried over byte for byte. Builder nodes: 3 now (N0, N1, N2) + 1
blocked (N4); N0m is a measurement run (a scout with a shell, or a builder; no repository write). After N1 merges: the
`known_red: FV1-4` marks of P1-б E9 rows (registry `scripts/tests/known_red.py`, P1-а) are removed in N1's commit if present on the
branch; if P1-а/P1-б are not merged yet (TEMPORAL), nothing to remove and P1-б lands its E9 rows unmarked. No node depends on a row an
unmerged node provides: N1's only inputs from another node are `person_words.lf` and the `--notes-file` road (N0, merged first) and the
N0m numbers (a text in §2a).

### §10a Crossings with work in flight (queue lines; finding 5)

Shared with T3a / T1r of the told-before-work spec (`docs/tasks/specs/20261113-told-before-work-mechanism-spec.md` `:391`, `:393`, `:625`,
`:628`). Function lists are disjoint; F14 sets the order (recommended (a)):

- `references/role-load.json`: `очередь: FV1-4 N1 (allowances.brief, allowances.brief_charter_head, note) → T3a (process_ratchet_tokens raises named) → T1r (process_ratchet_tokens raises, native_headroom baselines)`.
- `scripts/role_load.py`: `очередь: FV1-4 N1 (_brief_ceiling → _brief_allowance, the brief layer of static_load, the table notes :715-716) → T3a (new native_headroom_problems and its call next to process_ratchet_problems' caller)`. Invariant both sides keep: T3a's K10 share `U(role)` reads only the `charter`, `injection_common`, `injection_role` layers of `static_load` (told-before-work `:269-270`); N1 changes only the `brief` layer's reason word and keeps its bytes, so `U` is unchanged by N1.
- `scripts/tests/test_ahead_cards.py`: `очередь: FV1-4 N1 (:364-376 deleted) → T3a (CARD_MAX_BYTES check :52, :249 removed) → T1r (the 12 cards migrated; the rest of the file)`. TEMPORAL: if T1r lands first and the loop at `:346-378` is gone, N1 has nothing to delete there and its per-role watch already lives in `test_brief_pack.py` (F8 b).

The mirror line the Lead adds to the told-before-work spec, §7 (after the paragraph "Shared files after the cut", `:628-632`), verbatim:
`FV1-4 (docs/tasks/specs/20261113-fv1-4-no-brief-cut-spec.md §10a): role-load.json — FV1-4 N1 (allowances.brief, allowances.brief_charter_head, note) → T3a → T1r; role_load.py — FV1-4 N1 (_brief_allowance, static_load brief layer, notes) → T3a (native_headroom_problems + call); test_ahead_cards.py — FV1-4 N1 (:364-376) → T3a (:52, :249) → T1r. brief_pack.py: after N2, _stand_names ignores its limit argument, so FIRST_LOOK_ROLES_MAX is unused and T3b may delete it with its arguments.`

Other crossings: `scripts/gate_preflight.py` (a hot file, PROJECT.md «Командная работа» 3) — N1 owns `check_stand_lessons` only; any
other pile's dispatch on that file names its own functions (function-disjoint form). `scripts/tests/harness.py` — N1 adds
`normalised_bytes` only (a new function; no existing line changes). `scripts/person_words.py` — N0 adds `lf` only. П1-в (scoreboard
spec `20261113-p1v-run-scoreboard-spec.md:354`, N-brief): the run-log line N1 changes is `brief: <path> (<n> B[, side files: <a>, <b>][, not written])`
(m6); the clauses `, <n> budget B against the ceiling` and `, over the 6144 budget B ceiling after every cut: …` disappear, so N-brief
("briefs over the budget ceiling") has no token to count after N1 and reads `bytes` from `state/brief-sizes.jsonl` instead — the Lead
mirrors this line into П1-в's N-brief row.

### N0m — measurement of uncut brief sizes (finding 6; PROJECT.md п. 6(а))
given: this spec §2a (the command, the inputs, the columns, the negative control); `PKG\scripts\brief_pack.py:4137-4595`; `PKG\scripts\tests\harness.py:279-319`
owns: none — no repository write; the copies and the scratch script live in the session scratchpad
non-goals: any change to the package; any write into `C:\QAFactory\mybooks-stand\` (read and byte-copy only); interpreting the numbers
handoff: the result table of §2a (one row per primary brief + totals per source), the script in full source, its verbatim output, the negative-control row
edges: a build that raises → a row with the exception (never a skipped row); a story copy whose pipeline names no ticket → one line saying so and no rows; a brief file name that does not parse into stage-role-n → listed as `unparsed`
DoD: every primary brief of both copies has a row or an `unparsed`/`build_error` line; the negative control prints `build_error`; the live arm folder's newest mtime is unchanged before/after (printed). Verification: the command of §2a, both labels, output attached verbatim.
siblings: none -- a measurement, no mechanism
designer: this draft.

### N0 — the person's words reach the journal whole (F2 a)
given: this spec §3 (journal note road), §5.1, §8 E-4, E-25, E-26, E-31, E-32, E-33, §9 F12; `PKG\scripts\log_append.py` (whole); `PKG\scripts\person_words.py` (whole); `PKG\scripts\driver_core.py:259-270`; `PKG\scripts\driver_runner.py:263-290, 321-360`; `PKG\scripts\driver_conductor.py:128-165`; `PKG\scripts\driver_machine.py:3300-3315, 3880-3895`; `PKG\scripts\tests\test_story_run_refusals.py:1246-1323, 3095-3108`; `PKG\design\factory-rules.md`; `PKG\design\architecture.md`; `plans\builder-rules.md`; `docs\TESTING.md`
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\log_append.py (main: new `--notes-file`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\person_words.py (new `lf` only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\driver_core.py (_answer_note)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\driver_runner.py (answer_row only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\driver_machine.py (the two _answer_note call sites :3308-3312, :3888-3889 only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_story_run_refusals.py (refusal_person_words_kept_whole rows (3), (4), new (5); the F-3 row :3103-3105)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\fv1-4-n0-notes-file.md
non-goals: `brief_pack` (N1); `driver_conductor.owed_rows_step` (unchanged: it replays the args it is given); `Driver.words_file` (its own writer of `state/words` is reported, §12 item 6, not changed); any other `log_append` option; the driver's answers file.
handoff: builder report (rule 7 of `.claude/agents/builder.md`) with the witness output; the FR section walk (A, C, D, G).
edges: J-1 a 40 000-char answer → note whole (no `[cut:`); J-2 empty answer → the note is the prefix alone, written to its file (kept row `:1320`); J-3 CRLF → LF via `person_words.lf` (kept row `:1321`); J-4 a `--notes-file` that is missing/unreadable/empty/not UTF-8 → `log_append` exits 1 with the `person_words.read` refusal (the same form as `--reason-file`, `log_append.py:207-215`); `--notes "<x>"` and `--notes-file` together → refused naming both; `--notes` left at its default `""` with `--notes-file` → accepted (`args.notes or None`, m2); J-5 the first `log_append` call of a `human_answer` row exits non-zero → `owe_row` saves args with `--notes-file <absolute path>`; `owed_rows_step` replays → the journal's newest `human_answer` note equals prefix + words whole and the file still exists (E-25); TEMPORAL: an owed row saved with `--notes <text>` (the pre-N0 shape, written by hand into `state["owed_rows"]`) replays to the same note (E-26); a blank note (`write_words` returns None) → the row passes `--notes` with the blank note as today; the note file cannot be written → F12 (a): `OSError` propagates (E-31); the story folder moved before the replay → the replay is refused naming the file and the row stays owed (E-32).
DoD: (1) `_answer_note(prefix, words)` returns `prefix + person_words.lf(words)` and imports nothing from `brief_pack` (m1); (2) `log_append.py --notes-file <path>` sets `args.notes = person_words.read(args.notes or None, args.notes_file, "--notes", "--notes-file")` before the `--event`/`--batch` split, exactly where `--reason-file` is resolved; (3) `answer_row` and the two `driver_machine.py` sites write the note with `person_words.write_words(<task root = self.state_dir.parent>, "", "journalnote", note)`, pass `--notes-file <absolute path>` instead of `--notes <note>`, and NEVER delete the file; (4) no new writer of `state/words` (no `open`/`write_text` on such a path in the diff); (5) rows J-1…J-5 and the TEMPORAL row are variant rows of `refusal_person_words_kept_whole` (row (3) uses literal sizes 20 000 / 21 000 / 40 000 — no `brief_pack.PERSON_WORDS_MAX`), and the F-3 row `:3103-3105` expects `--notes-file` in the owed args. Verification: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/log_append.py ai-packages/qa-factory/scripts/person_words.py ai-packages/qa-factory/scripts/driver_core.py ai-packages/qa-factory/scripts/driver_runner.py ai-packages/qa-factory/scripts/driver_machine.py` — run every file it prints (quarantine excluded); all green.
siblings: axis 29 (append-only jsonl writers: `log_append.write` is the journal's writer, unchanged); `--reason-file` is the twin door (same reader); `person_words.write_words` is the one writer of `state/words` (AR-14) — `Driver.words_file` is a known second writer, reported (§12 item 6).
designer: this draft (fix round t-502).

### N1 — `build` renders once, whole; the result and the record carry `bytes` only; a person's words whole everywhere in the brief
given: this spec (whole); the N0m table in §2a; `PKG\scripts\brief_pack.py`; `PKG\scripts\person_words.py` (with N0's `lf`); `PKG\scripts\project_knowledge.py:55-71, 425-490, 975-1005`; `PKG\scripts\gate_preflight.py:3205-3235`; `PKG\scripts\role_load.py:440-530, 690-720`; `PKG\references\role-load.json`; `PKG\scripts\retro_numbers.py:955-990`; `PKG\references\artifact-writers.json:203`; `PKG\scripts\tests\harness.py:260-330`; `PKG\scripts\tests\test_brief_pack.py`; `PKG\scripts\tests\test_brief_pack_s5_plan.py:190-205, 435-520`; `PKG\scripts\tests\test_flow_requests.py:190-240`; `PKG\scripts\tests\test_role_load.py:100-130`; `PKG\scripts\tests\test_readiness.py:740-760`; `PKG\scripts\tests\test_whole_identifier.py:165-175`; `PKG\scripts\tests\test_ahead_cards.py:340-380`; `PKG\scripts\tests\test_project_knowledge.py:905-970`; `PKG\scripts\tests\test_gate_preflight.py:2944-2996`; `PKG\scripts\tests\test_story_run_refusals.py:1285-1305`; `PKG\design\factory-rules.md`; `PKG\design\architecture.md`; `plans\builder-rules.md`; `docs\TESTING.md`
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\brief_pack.py (constants BRIEF_MAX_BYTES, SD_HEAD_MAX_BYTES, DECISION_CHARS, DECISION_CHARS_MIN, PERSON_WORDS_MAX, WORDS_BY_REFERENCE, APPROACH_SHORT_BYTES, APPROACH_ONE_LINE, APPROACH_POINTER, new WORDS_LINE_WIDTH; answers_of, person_words_whole, _plain_words, question_answer_lines, decisions, new _words_block, digests, source_material, approach_forms, project_approach_lines, _site_note, request_lines, measured_bytes, head_bytes, sd_head_lines, _record_brief_size, build incl. render and the code side file line, main)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\project_knowledge.py (LESSON_WORDS_SHOWN, LESSON_LINES_MAX, _lesson_line, lessons)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\gate_preflight.py (check_stand_lessons only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\role_load.py (_brief_ceiling, static_load, the table notes)
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\role-load.json (allowances, note)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\retro_numbers.py (the comment at :962-966 only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\artifact-writers.json (the brief-sizes `why`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\s5_plan.py (_settled_lines docstring only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\harness.py (new normalised_bytes only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_brief_pack.py (the §6 N1 rows: left_out_sources, expectation edge 5, proof_lines :873, blast-radius M13, labelling_vocabulary_lines, p4_*, sc1_10_lines, p1v_n3_brief_size_record incl. ROLE_BRIEF_BYTES_MAX, approach scenario, s5_build_at, s5_ceiling, n4_scenario, ss1_11_stand_lessons, E54, S1 SD head, S5 fixture, 7 KB build, decisions call sites)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_brief_pack_s5_plan.py (DOORS_ONLY_BRIEF_MAX → S5_PLAN_BRIEF_BYTES_MAX, ceiling_verdict → size_verdict, k9_grouping_hint_line rows :488-514 only, :199)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_flow_requests.py (b5 rows)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_role_load.py (K-S6)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_readiness.py (block 11)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_whole_identifier.py (:171, :173)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_story_run_refusals.py (:1293, :1304 only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_ahead_cards.py (:364-376)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_project_knowledge.py (:912, :915, test_lessons_cap_ten_lines_and_cut_the_words_at_200, test_lessons_at_ten_no_pointer_and_words_at_200_and_201)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_gate_preflight.py (test_stand_lessons_are_one_note_never_a_card: the 11-lessons block :2977-2987 only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\fv1-4-no-brief-cut.md
non-goals: the §5.6 N2 sites; `ahead_card`, the `ahead` assignment, `FIRST_LOOK_*`, `_row_field_lines`, `dispatch_groups` (T3b); `window_code_file`, `_fit_code_file`, `_shared_fixture_lines` (N2); `app_card.py` (scout question); `controller.py`; quarantined test files; the forge norm; a retro size note; `driver_*` (N0).
handoff: builder report with the witness output; the FR walk (B, C, D, E, F, G); the §7 table filled with the measured numbers and both runs of step (2)/(4); the list of quarantined files expected red.
edges: E-1 … E-30 that name N1 (§8), each a variant row of an existing test function in the keep files named above; F7, F9, F10, F13 as recommended until the Lead answers.
DoD (acceptance keys): (1) `build`'s result has no `budget_bytes`, `over_ceiling`, `omitted`; (2) no brief contains `## Not in the brief`, `budget`, `ceiling`, `cut for room`, `the brief is full`, `head over cap` (n4_scenario + one row per role of `stages.json` on the shared fixture); (3) 60 × 380-char, 24 576-char and 200 000-char words appear whole (folded comparison), a multi-paragraph answer keeps its line breaks, a `## ` line of an answer is inside a fenced block; (4) every input file line of a roomy build is in the written brief, no `*-files.md` is written, 12 collected sources are 12 lines; (5) the SD head carries every DoD lead; (6) request lines keep their names at 12 × 200+ chars; (7) `state/brief-sizes.jsonl` lines are exactly `{ts, stage, role, dispatch, bytes}`; (8) `main()` prints `brief: <path> (<n> B…)` with no ceiling words; (9) `role_load.py --all` totals equal before/after (F3 a); (10) the AR-22 `Grep` of §1 over the removed names returns only changed sites; (11) a stand lesson of 1 000 characters is whole in the S5 head and in the gate note, 11 lessons are 11 lines; (12) the two ratchets of §7 are measured with `harness.normalised_bytes`, carry the named raise line, and the verdict rows pin AT / AT + 1. Verification: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/brief_pack.py ai-packages/qa-factory/scripts/project_knowledge.py ai-packages/qa-factory/scripts/gate_preflight.py ai-packages/qa-factory/scripts/role_load.py ai-packages/qa-factory/scripts/retro_numbers.py ai-packages/qa-factory/references/role-load.json ai-packages/qa-factory/scripts/tests/harness.py` — run every file it prints (quarantine excluded; a slow file of PROJECT.md п. 2 is not run locally, CI judges it); all green; plus `python -B ai-packages/qa-factory/scripts/role_load.py --all` before and after, both outputs attached.
siblings: axis 5 (stage twins: none — `build` is one function for every stage); axis 18 (the test ratchets, §7); axis 29 (`_record_brief_size` appends through `hooklib.append_jsonl_line`, unchanged); axis 32 (census unchanged; `check_stand_lessons` row `:392` keeps function and class); axis 34 (one road: every role, stage and language gets the same no-cut brief and the same words renderer — no data row or branch per role).
designer: this draft (fix round t-502).

### N2 — class-C summaries name their whole, or render whole (F1 a, F5 a)
given: this spec §5.6, §8; `PKG\scripts\brief_pack.py` (the functions below); `PKG\scripts\sizing.py:609-626`; `PKG\scripts\tests\test_brief_pack.py`; `PKG\scripts\tests\test_brief_pack_s5_plan.py:215-310, 455-500, 590-710`; `PKG\design\factory-rules.md`; `PKG\design\architecture.md`; `plans\builder-rules.md`; `docs\TESTING.md`
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\brief_pack.py (case_form_lines, branch_check_line, expectation_change_lines, proof_required_lines, side_lines, _assumption_lines, _bind_lines, delta_lines, _delta_tail, _stand_short → _stand_text, _stand_address_lines, _case_actor_lines, _repo_stand_lines, manual_stand_lines, _stand_names, _timeout_entry, test_timeout_line, _fit_row_line, fit_target_lines, blast_radius_line (failure branch), _s5_kind, _plan_cap, plan_dispatch_lines (the two "could not" lines :1907, :1929 only), plan_lines (:1984 only), _CodeCollector.read, _CodeCollector.extends, _CodeCollector.helper_lines, _CodeCollector.reached_by_receipted, prior_retro_lines, s4_stand_lines, s3_roster_lines, first_look_input_line, _first_look_accounts, first_look_runner_lines (text only), _fl_state, _fl_line, first_look_lines (text only), exploration_lines, walk_lines, window_code_file, _fit_code_file, _shared_fixture_lines; constants CASE_FORM_LINE_CHARS, CASE_FORM_PROBLEMS_SHOWN, STAND_WHY_CHARS, STAND_ROLES_MAX, STAND_CASE_LINES_MAX, TIMEOUT_WHY_CHARS, TIMEOUT_PROFILES_SHOWN, S3_ROSTER_WHY_CHARS, SHARED_FIXTURE_INSTANCES, SHARED_SECTION_BYTES, SHARED_TAIL_RESERVE — no FIRST_LOOK_* constant)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_brief_pack.py (rows of the functions above: :751-762, :875-880 and the C-rows of the same functions)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_brief_pack_s5_plan.py (window_code_file rows :222-303, k9_grouping_hint_line row :486-487 only, C-K13 :694-706)
non-goals: everything N1 owns; `FIRST_LOOK_*` constants, `ahead_card` (T3b); `sizing.clip_name` and its person-facing callers; `app_card.py` (scout question); any summary that already names its whole (§5.6 "stays" rows).
handoff: builder report with witness; per site of §5.6 marked N2 one line: applied / unchanged-pointer, with the test row that proves it; the class-search output of DoD key (c) verbatim.
edges: per site: AT the bound, one BEYOND (a clipped/dropped item → the carrier line present, or the text whole), and a 10× value; an empty value (the existing "no reason recorded" / "none" text unchanged); `window_code_file` past 28 000 B: every left-out excerpt named by `file:lines` (no "... and N more"), every shared fixture and instance named (no "+K more fixtures not listed", no per-fixture "(+N more)"); a function name of 61 / 200 characters in `walk_lines` → whole; 30 broken fixture ids → all named.
DoD: (a) each §5.6 N2 "Change" applied, each with one variant row in the existing test function of that brief line (no new test file); (b) no `_short(exc, …)` / `_clip(problem|why, …)` left in a "could not" / "cannot be read" line; `Grep "more\)" brief_pack.py` lists only lines whose same line or section names a file; (c) the class search of §5.6 (both patterns, positive control `S4_REQUIRED_BY_CHARS`) re-run on the changed `brief_pack.py`: every hit is a §5.6 row or a "stays" line — the output attached. Verification: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/brief_pack.py` — every file it prints, quarantine excluded, green.
siblings: axis 17 (detector verdict: the "whole in a file past the cap" pattern is the same idea — not touched); axis 34.
designer: this draft (fix round t-502).

### N4 — in-run context-size refusals (F6 a) — BLOCKED on the owner's word and on T3a
given: told-before-work spec Appendix A `:685-701`; `PKG\scripts\inject_context.py:40-60, 250-290, 505-560, 720-735`; `PKG\scripts\native_context.py:150-220`; `judgment-census.json:486-490, 652`
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\inject_context.py (collect_blocks: the MAX_BLOCK_CHARS branch only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\native_context.py (stage: the 100000 branch only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json (rows :486, :652 only if their refs change)
non-goals: T3a's K8/K10 dev-time checks; any host setting (P25).
handoff: not dispatchable until the Lead writes the owner's direction into this node.
edges: to be written with the direction (at/beyond 26 000 per file; at/beyond 100 000 total; a project file of 200 000).
DoD: to be written with the direction; witness `scenario_walk.py --witness-for` over the two owned scripts.
siblings: Appendix A sibling list; axis 32 (census refs A24:IC-oversized-slice, A24:NC-context-too-large).
designer: this draft (direction pending).

---

## §11 Rule 10 — four questions (one block per mechanism)

Mechanism M1 — "no size cut in a run; size is a forge record" (N1, N2):
(a) cost: briefs grow for long words / many inputs (measured by N0m before N1); the role pays bytes × turns of cache reads; the forge
pays a norm (P1-v N6). (b) axes:
1 n/a (no policy/role file text); 2 n/a; 3 n/a (release copy unchanged in kind); 4 covered — finding row + `factory-rules-debt` none;
5 covered — no stage twin (one `build`); 6 covered — measurers: none in `experiments/` read the keys (checked); 7 n/a; 8 n/a; 9 n/a;
10 n/a; 11 n/a; 12 covered — the pile node; 13 n/a (forge dispatch cut); 14 n/a; 15 n/a; 16 n/a; 17 n/a (detector shape untouched);
18 covered — the §7 ratchets (path-normalised, measured, named raise); 19 n/a; 20 n/a; 21 n/a; 22 n/a; 23 n/a; 24 n/a; 25 n/a; 26 n/a;
27 n/a; 28 n/a; 29 covered — the record keeps the one appender; 30 n/a; 31 n/a; 32 covered — census unchanged (§1a); 33 n/a; 34 covered —
one road for every role/stage/language, one words renderer; 35 n/a; 36 n/a. (c) detector: the scoreboard over `brief-sizes.jsonl` against
the forge norm (P1-v N6) + the two fixture ratchets of §7; a cut creeping back is caught by N1's DoD key (2) rows (texts absent in every
brief of the fixture) and N2's DoD key (c) (the class search). (d) on the path: `build` is the only producer of a brief; the test rows run
in the canon (`test_brief_pack.py` keep).

Mechanism M2 — "the journal note carries a person's words by a kept file" (N0):
(a) cost: one kept file per `human_answer` row under `state/words/` (the audit trail, never deleted — the same cost `Driver.words_file`
already pays per answer). (b) axes: 29 covered (the appender unchanged); 24/AR-24 carriers (`person_words.read` the one reader,
`person_words.write_words` the one writer, AR-13/AR-14) — covered; every other axis n/a for the same reasons as M1 (one line each, as
above). (c) detector: `test_story_run_refusals.py` rows (3) and (5) (keep, canon) — row (5) is the owed-row replay. (d) on the path:
`_answer_note` + `answer_row` are what every human_answer writer calls; the two direct `driver_machine.py` sites are changed in the same
commit.

Mechanism M3 — "the static brief layer is an allowance" (F3 a): (a) none at run time; (b) axis 18 covered (ratchets unchanged), others
n/a; (c) `test_role_load.py` K-S6; (d) `role_load.static_load` is the one producer of the layer.

---

## §12 Contradictions and analogs noticed (reported, not widened)

1. P1-б `20261113-p1b-dry-story-spec.md:839` still reads "…несёт слова целиком или называет файл слов"; amendment B4 and the finding
   require the words whole in the brief. FV1-4 follows the stricter reading (E-19); the Lead may align `:839`.
2. The B4 table (`20261113-p1-specs-amendment-owner-words.md:689-699`) cites origin/main line numbers; in the p1v-n3 tree every
   `build` line is +~25 (e.g. `files.pop` `:4512` → `:4533`; the role line `:4515-4530` → `:4548-4550`; the conductor line
   `:4595-4598` → `:4620-4624`).
3. Missed by the B4 table (found by the class search): `PERSON_WORDS_MAX` (20 000, cuts words in the brief AND in the journal note via
   argv); `APPROACH_ONE_LINE` "(cut for room)" and `APPROACH_POINTER` "the brief is full" (ceiling text to a role); the approach / map /
   digests rungs of the ladder; the broken digests pointer (side file not written at the full level); silent caps `tests[:6]`,
   `rows[:8]`, dispatch scope `[:8]`, `_stand_short` (80, no "..."); `role_load` / `retro_numbers` reading `BRIEF_MAX_BYTES`; the test
   ratchet `DOORS_ONLY_BRIEF_MAX`; the class-C sites of §5.6; `inject_context` / `native_context` size refusals (F6); and, in the fix
   round, the stand lessons cut and cap (2a, F9), `source_material` `out[:8]` (2b).
4. `plans/piles/roles-context/batch-2-…md:28-29` (main checkout) shows RC2-1/RC2-2 "ожидает", but both are in the p1v-n3 code
   (`brief_pack.py:1645-1659`, `story_step.py:453-458`) — the main checkout is stale (memory note); FV1-4 supersedes RC2-1's minimal line.
5. Analog outside class: `controller.BRIEF_MAX_BYTES = 1500` — same name, different thing (conductor summary + whole file).
6. (fix round) `Driver.words_file` (`driver_runner.py:321-…`) writes into `state/words` with its own code, while `person_words.py:43-45`
   says it is "the ONE writer of that folder" and that the driver's copy comes through `write_words` — a pre-existing AR-14 gap, the same
   class as finding 1's second-writer half. N0 does not widen to it; the Lead files it (owner: the driver's pile).
7. (fix round) `driver_sources.py:87` and `:142` write the `human_answer` prefix `"S1 material supplied by the person: " + "; ".join(pasted)[:1500]`
   — a silent cut of the list of material names the person supplied, inside a journal note every later brief reads (`answers_of`): the
   core class, outside this spec's owns. Reported for the Lead to place as a node (rule 6: a residual is a node with owns and a test).
8. (fix round) `app_card.py:57`'s comment documents the 200-character lesson cut 2a removes; after N1 a long lesson is clipped at 400 in
   the card (it was cut at 200 before) — inside the app_card scout question (§9b row 2).

---

## §13 Reading trail

First draft — Read (Read tool): finding `findings-1413c\…\20261112-srezka-briefa-rezhet-slova-cheloveka.md` (whole); batch row `:37`
(Grep); amendment `20261113-p1-specs-amendment-owner-words.md:660-759`; `PKG\scripts\brief_pack.py:40-200, 420-509, 580-614, 625-864,
864-1023, 1085-1104, 1313-1352, 1515-1560, 1560-1759, 1790-1849, 1975-1998, 2445-2534, 2895-3044, 3238-3372, 3596-3724, 4100-4380,
4380-4630`; `driver_core.py:250-299`; `controller.py:9682-9756`; `role_load.py:445-529, 700-724`; `role-load.json` (whole);
`retro_numbers.py:955-994`; `inject_context.py:44-57, 258-282`; `native_context.py:165-179`; `s5_plan.py:1198-1237`;
`log_append.py:1-30, 138-207`; `test_brief_pack.py:745-879, 1515-1614, 1708-1907, 2140-2254, 2440-2629`;
`test_story_run_refusals.py:1246-1323`; `test_readiness.py:730-761`; `test_flow_requests.py:195-238`; `test-layers.json:1-56,
280-349, 6985-7054`; `judgment-census.json:57-61, 486-490, 652`; `design/architecture.md:134-258`; `docs/SIBLING_MAP.md:311-328`
(+ axis headings); told-before-work spec `:394, :685-704` (+ Grep lines); `CHANGELOG.md:5810-5834`.

Fix round t-502 — Read: the critic verdict (whole); this spec (whole); `PKG\scripts\person_words.py` (whole); `driver_runner.py:255-299,
318-346`; `driver_conductor.py:125-164`; `log_append.py:180-224`; `driver_core.py:255-274`; `driver_machine.py:3300-3315, 3880-3893`;
`project_knowledge.py:55-74, 425-488, 979-1003`; `gate_preflight.py:3210-3234`; `brief_pack.py:1028-1077, 1476-1517, 1563-1746,
2138-2157, 2306-2425, 2694-2711, 2750-2879, 3296-3311, 3341-3375, 3394-3405, 3636-3653, 3852-4026, 4326-4339, 4586-4626`;
`sizing.py:605-628`; `test_brief_pack.py:2404-2433, 2944-3038`; `test_brief_pack_s5_plan.py:435-516`; `test_ahead_cards.py:330-379`;
`test_story_run_refusals.py:1290-1324`; `test_project_knowledge.py:940-969`; `test_gate_preflight.py:2976-2987`; told-before-work spec
`:255-279, :391-394, :610-639`; `p1v-run-scoreboard-spec.md:8-15`.
Searched (Grep/Glob; controls): `write_words\(|_answer_note|answer_row\(|def words_file` over `PKG\scripts\*.py` (control: the known
`driver_core.py:263` hit); digit-aware constants on `brief_pack.py` (63 lines; control `S4_REQUIRED_BY_CHARS`, `S3_ROSTER_WHY_CHARS`)
and on `app_card.py`; clip/slice patterns on `brief_pack.py`; `lessons\(|_lesson_line|LESSON_*` over `PKG\scripts`; `stand_lessons`
over tests; `source_material` over tests; `DIFF_ALL_LINES|CANDIDATE_LINE_MAX|HELPER_NAMES|clip_name|app_card` on `brief_pack.py`;
`-code\.md` on `brief_pack.py`; `8191` in `run-py.cmd`; `driver-answers` over `driver*.py` (a first narrower search in `driver_runner.py`
was empty; the same pattern over `driver*.py` found 8 hits — the control); `test-layers.json` section heads (`keep` `:35`, `quarantine`
`:7046`) and the keep lines of the touched test files; Glob of the cart-1 briefs (116 files) and of the LR2-1 arm briefs (204 files;
a Glob of `experiments/.../factory-out/**/briefs/*.md` is empty — that copy holds no briefs, its folder listing is the control);
`LR2-1|35 of 41|note: brief:` in the specs folder; `T3a|role_load|role-load.json|test_ahead_cards` in the told-before-work spec.
Not opened: P1-в spec body beyond `:8-15` and `:354`/`:592` (Grep), `t-042-pc2-6-briefs-over-ceiling.md` (named only), `known_red.py`
(not in this tree), the arm's live files (only their names, by Glob).

Needed beyond the manifest: `PKG\scripts\project_knowledge.py`, `gate_preflight.py`, `sizing.py`, `app_card.py` (Grep only),
`driver_conductor.py`, `hooks\run-py.cmd`, `scripts\tests\harness.py`, `test_project_knowledge.py`, `test_gate_preflight.py`,
`test-layers.json`, the LR2-1 arm folder (Glob only), `20261113-p1v-run-scoreboard-spec.md`.

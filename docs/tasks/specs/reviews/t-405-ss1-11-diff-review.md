# t-405 — diff gate, node onboarding-forge/2/SS1-11 (parts B1 f0c6c10, B2 4a74dc3)

Critic (Opus), one pass for the topic. Diff: `git diff 5d79f97 4a74dc3` in `.claude/worktrees/ss1-11-b1`. Spec: `docs/tasks/specs/t-365-f6-39-ss1-11-specs.md` §2, §3, §3a, §5, §8. This verdict feeds acceptance. The acceptance decision itself belongs to the coordinator/Lead.

## Verdict per part

- **B1 (registry key, `lesson` / `lessons`, door): fit_with_fixes.** The writer, guard, dedup, reader, unknowns and the AR-13/14 ways in are correct. The fixes are small: the "+k more" pointer is unquoted (F3), AT rows are missing (F4), a read verb uses write wording (F6), and two blocks are copy-pasted (F7).
- **B2 (gate note, `stand_lesson_lines` in two places): fit_with_fixes, one finding blocks acceptance (F1).** The automator and code-critic head looks up the stand differently from its twin, the manual-runner section. For the same story, S5 roles can get no lessons while the gate and the manual runner show them (P31, AR-19). F2 breaks FR-6 in the person-facing gate note. F5 is a spec gap: the walking manual runner never gets the lines.

Blocking findings: 1 (F1). Fix this round: F2, F5 (F5 needs the coordinator to widen the owns). Non-blocking: F3, F4, F6, F7, F8.

## Findings

### F1 (BLOCKS, B2): the S5 head finds the stand by a different route from its twin
- `brief_pack.py:4199` passes `head += stand_lesson_lines(project, str(pipeline.get("environment") or ""))`, which is the raw field.
- Its twin in the same file, `manual_stand_lines` at `brief_pack.py:2711`, gets `name` from `_stand_pick` (`:2538-2550`). When the pipeline names no stand, `_stand_pick` uses "the config's ONE row is the stand".
- The gate does the same with `_selected_environment` (`gate_preflight.py:5128-5135`: "the one the pipeline recorded, else the only one").
- So does the writer, with `stand_gaps.stand_name` (`stand_gaps.py:148-159`).
- **Input:** `config.environments = [{"name": "localhost"}]`. `pipeline.json` has `"environment": null`, as S0 writes it on the person's "go on without a stand" (`driver_s0.py:2283-2292`: `environment, pending = None, True`). One lesson is on `localhost`.
- **Output:**
  - The gate A note lists the lesson.
  - The manual runner's `## The stand` lists it.
  - The `qa-automator` and `qa-code-critic` heads get `stand_lesson_lines(project, "")`. Then `PK.lessons` returns `no_stand`, so they get `[]` and no line.
  - The gate note tells the person "(the roles read it)", which is false for exactly the role that writes the waits.
- Whether the stand check later fills `pipeline.environment` was not verified. Three sibling readers treat this state as "the only stand", so it is a state the factory recognises.
- **Spec defect:** §2.3 B2-2 says the field is "the same source `build` passes to `manual_stand_lines`". The field is the same; how the stand is found from it is not.
- **Fix:** in `build`, use `_stand_pick(hooklib.load_config() or {}, str(pipeline.get("environment") or ""))[1]`, the same function the manual branch uses. Add a test row (below).

### F2 (fix this round, B2): the gate note shows machine text to a person (FR-6)
- The gate's INFO lines are rendered to the person (`gate_preflight.py:6124-6128`).
- `check_stand_lessons` (`gate_preflight.py:3227`) puts `got['problem']` into the person's text unchanged. **Input:** a registry holding `{not json`. **Output:** `what the person taught about localhost could not be read (qa-factory/records/project-knowledge.json cannot be read (Expecting property name enclosed in double quotes: line 1 column 2 (char 1)))`. This text comes from `environment_record.load_rows:224`.
  - Other `load_rows` texts are just as bad: "… has no `facts` list" and "… has schema_version 2, not 1".
  - Three bans in `references/human-questions.md` apply: `:57` (the factory's own records, a JSON file), `:44` (a field name), `:61` (raw text relayed as-is).
- With 11 or more lessons, `:3229` joins the pointer line `(+1 more: project_knowledge.py lessons --stand localhost)` into the body. That puts a script name and a flag outside the how-to-answer block (`human-questions.md:46`).
- The sibling note in the same file does it right: `gate_preflight.py:2603-2604` keeps the problem in the machine field (`problem=plan["problem"]`) and words the sentence plainly.
- The spec's FR walk (§2.1 `:273`) committed to "FR-6: the gate note is plain words, no field names".

### F3 (non-blocking, B1): the "+k more" pointer does not quote the stand
- `project_knowledge.py:476` builds `f"(+{extra} more: project_knowledge.py lessons --stand {stand})"`.
- **Input:** a stand named `staging eu`. **Output:** a role that runs the line as given gets argparse `unrecognized arguments: eu` (exit 2). The full list (FR-49) is then out of reach by the route the brief names.
- The conductor-actions row quotes its free words (`--subject "<a few words>"`).
- I did not read whether the config validator allows a space in a stand name (estimate). `PLACEHOLDER_STAND = "this stand"` shows the code itself treats stand names as words.
- **Fix:** quote the stand. Better, return the count as data (`more: k`, see the fix list) and let each reader render it: the brief as a command, the gate note in words (closes F2's half too).

### F4 (non-blocking, tests B1/B2): AT rows of the limits are missing; E54 is not driven over the ceiling
- `test_lessons_cap_ten_lines_and_cut_the_words_at_200` and the B2 scenario cover only BEYOND (11 lessons, 1,000 characters). Missing:
  - exactly 10 lessons: 10 lines and no pointer;
  - words of exactly 200 characters: shown whole, no ` ...`;
  - 201 characters: cut.
- The person's words are outside input, so CLAUDE.md rule 11 owes a case AT and a case BEYOND for every limit.
- **E54** (B2 deviation, K8): `check_in("E54: …", "\n".join(many), pc8_head(brief_of()))` uses 11 short lessons of about 60 bytes. Nothing shows that brief is over `BRIEF_MAX_BYTES`, so the ceiling ladder may never run.
  - The code behaviour is correct by reading: `render` keeps `list(head)` whole (`brief_pack.py:4383`), and the trims at `:4463-4524` take only files, map and words.
  - The edge row is still unpinned.

### F5 (fix this round, needs owns: `app_card.py`; spec gap of §2.3): the walking manual runner gets no lessons
- `build` skips `manual_stand_lines` for a walk (`brief_pack.py:4343`, `not walking`: "the app card holds the stand of a walk").
- The app card does call `manual_stand_lines` (`app_card.py:162`), but it keeps only lines starting with `"- Stand:", "- API:", "- Frontend:", "- Accounts:", "- Env keys:"` (`:163-164`). `"- Stand lessons: …"` does not start with `"- Stand:"`, so it is dropped.
- The card's `inputs_hash` (`app_card.py:436-457`) does not include the registry. Even after the filter is fixed, a lesson taught during the story would not rebuild a cached card.
- **Input:** a manual dispatch with a walk session (`walk_record` true, `brief_pack.py:4249-4251`) and one lesson on the stand. **Output:** neither the thin walk brief nor `work/app-card.md` carries the lesson.
- This is the main manual road since t-1957. It is also the road where "indexing takes minutes" matters most, because a walker waits in the browser.
- The builder followed the spec's two call sites. The gap is the spec's: E55 says the manual runner gets them "only through `manual_stand_lines`" but missed the walk road.

### F6 (non-blocking, B1): the read verb uses a write verb's wording when it refuses
- `cmd_lessons` (`project_knowledge.py:953-957`) reuses `_context`. **Input:** `lessons --task T-9 --stand dev`. **Output:** "there is no story `T-9` in this project, so nothing was recorded; …" for a read-only verb (FR-1: the refusal says what is wrong). Exit 2 is tested; the wording is not.

### F7 (non-blocking, duplication: brief item 6): blocks copied inside the diff
- `cmd_lesson` `project_knowledge.py:946-955` (stand from `--stand`, else `stand_gaps.stand_name`, and the placeholder refusal with the list of stands) repeats `cmd_side` `:995-1002` line for line. Extract `_story_stand(ns, task_root, cfg) -> (stand, refusal)`; both verbs call it.
- The subject check at `:591` repeats the side-name check at `:630`: `text != text.strip() or any(ord(ch) < 32 or ord(ch) == 127 …)`. One helper for both.
- `_lesson_line`'s `given` clause (`:442-443`) is `acting_line`'s (`:780-781`) with `_plain` added. Low; may stay.
- The test helpers `teach` (test_brief_pack.py) and `teach_stand` (test_gate_preflight.py) are the same function. Both files are script-style, so this is acceptable. Note only.

### F8 (non-blocking, note): `_plain` defines "control character" differently from the package
- `_plain` (`project_knowledge.py:427-429`) strips C0 and DEL only, as the spec chose (§2.2 B1-2).
- `http_client._CONTROL_RE` (`:45`) and `planning_contract._GROUNDING_CONTROL` (`:825`) also strip C1 (U+0080-U+009F). U+009B, a single-byte CSI, passes through `_plain` into a brief line.
- Queue, not this round: the package has three definitions of "control character" (an AR-15 analog).

## Answers per key

### K1 fit to spec

| item | status | evidence |
|---|---|---|
| B1-1 catalogue row | met | `config-keys.json:711`, verbatim to spec |
| B1-2 constants and limits | met | `project_knowledge.py:58-64` |
| B1-2 `record_problems` branch before the role rules, `_lesson_value_faults` | met | `:636-637`, `:585-601`; tests `test_lesson_value_faults`, `test_lesson_subject_never_meets_the_role_rules…` |
| B1-2 person-words door names `lesson` | met | `:655-657`; test `test_lesson_empty_words_name_the_lesson_door` |
| B1-2 dedup compares the words | met | `:679-686`; E37 in `test_lesson_verb_scenario` |
| B1-2 `lessons()` loads once, `_latest`, sorted, line form, never raises, `no_stand` | met | `:447-481`; `load` called once at `:464` |
| B1-2 verb `lesson` (prologue, stand, `--wait-s` pattern then `int` in try then range) | met | `:919-949` |
| B1-2 verb `lessons` (stand from `--stand` or `--task`; three outcomes plus problem exit 1) | met; wording defect F6 | `:952-975` |
| B1-2 `cmd_revoke` sentence chosen by key data | met | `:907-912` |
| B1-2 docstring verbs and E41 residual | met | `:24-31` |
| B1-3 guard regex `lesson(?![\w-])` and text | met | `guard_pre_tool.py:1789`, `:1746-1747`; tests assert `lessons` open |
| B1-4 conductor-actions row and revoke row | met | `conductor-actions.json:29-30`; `says` names no script |
| B1-5 `PT-human-word` refuses | met | `refusal_registry.py:733` |
| B1-6 `state-exits.md` row `known` | met | `state-exits.md:161` |
| E31 | met | `test_lesson_wait_s_pattern`, all 18 forms incl. 4,301 digits and `٣` |
| E32 | met | scenario plus value table |
| E33 | met | 80 accepted, 81 refused |
| E34 | met | NON_ASCII plus emoji; `Indexing`/`indexing` give two lessons |
| E35 | met | `" x"`, `"x\t"`, `"a\x00b"` |
| E36 | met | absent file, blank file, no flag (BOM: inherited from `person_words.read`, not re-tested; not checked) |
| E37 | met | same / new words / new wait |
| E38 | met | `test_lesson_refused_on_a_no_trace_story_with_the_door` |
| E39 | met (new-code world); old-plugin world not checked: old code, `_usable` `KEYS.get` None skips, by reading `:198` |
| E39a | met | `test_lessons_reader_never_drops_a_hand_edited_row…` |
| E40 | met | monkeypatched KEYS / CATALOGUE_PROBLEM |
| E41 | met | PK-4 on prod not shown |
| E42 | met | guard test |
| E43 | met | stored whole, shown cut, re-read whole |
| E44 | met | revoke newest, then all |
| E53 | met | `""` and placeholder give `no_stand` with no problem |
| B2-1 gate note | met in behaviour; wording breaks FR-6 (F2) | `gate_preflight.py:3210-3230`, `:6070` |
| B2-2 one formatter, two call sites | met; stand lookup diverges (F1) | `brief_pack.py:2682-2694`, `:2721`, `:4199` |
| B2-3 over the ceiling | met by reading; not pinned (F4) | `:4383`, `:4463-4524` |
| E45 | met (byte-identical by construction: `[]` adds nothing; the test checks absence) |
| E46 | met | gate and brief rows |
| E47 | BEYOND met, AT not pinned (F4) |
| E48 | BEYOND met, AT not pinned (F4) |
| E49 | met | gate (two stands, none named) and formatter `""` |
| E50 | met | gate and brief |
| E51 | met | `findings == []` asserted in every gate row |
| E52 | met | no `skip_*` added (grep of the diff) |
| E54 | not pinned (F4); behaviour met by reading |
| E55 | met for S4 (brief built); for S5 roles outside `SIDES_ROLES`, by reading `:4195` |
| census row (§2.1) | met | fixture `:343`, class shape, owner data |

### K2 writer and door
- **One writer (AR-14):** `record` (`:663-693`) is the only writer.
- **The guard:** `lesson` is closed to roles by `human_word_check` (`guard_pre_tool.py:1789`), and `lessons`/`show` stay open (tested).
- **Direct writes:** writing the file by Write/Edit is closed by `STAND_RECORD_FILES` (`guard_pre_tool.py:2280`, earlier code).
- **Refusals (FR-1, FR-2, P15):**
  - Each refusal says what is wrong and its door. Examples: "--wait-s takes whole seconds from 1 to 86400 … leave it out when the person gave no time; nothing was recorded"; the subject sentences; "pass --stand <name> (the stands: …)".
  - The guard text names the open verbs.
  - The door it names is one the conductor can use (the conductor-actions row).
- **The reader is the only way in (AR-13):**
  - Grep `stand_lessons|LESSONS_KEY|\.lessons\(` (case-insensitive) outside tests finds only `project_knowledge.py`, `gate_preflight.py:3223` and `brief_pack.py:2689`, both through `PK.lessons`.
  - Grep `project-knowledge\.json|PK\.load\(` (case-insensitive) outside tests finds `stand_gaps.py:780,987`. Both are earlier, id-specific reads of other keys; no consumer opens the file for lessons.
  - Positive control: the same greps found the known definitions.

### K3 the person's words
- **Whole and unedited (AR-24):** stored whole in `provenance.words`. The `.strip()` is the existing rule for every key.
- **Never classified (AR-29, FR-12):** no phrase list, and nothing reads the words except the display. `wait_s` is shown only.
- **Display:** collapses whitespace, strips C0/DEL and cuts at 200 characters. It never writes back (E43, tested).
- **The "+N more" limit:**
  - BEYOND is pinned (11 lessons give 10 lines plus the pointer). AT is not pinned (F4).
  - The role is told about the cut lessons by a pointer naming `project_knowledge.py lessons --stand <stand>`. Under the brief card convention (`brief_pack.py:4308`: "Every command is `python <root>/scripts/<script>`") and with Bash in the tools of `qa-automator`, `qa-code-critic` and `qa-runner`, the pointer can be run.
  - It breaks for a stand name with a space (F3), and the person gets it as machine text in the gate note (F2).
- **Data loss (FR-49):** none. The cut is display only, and the full list is one call away once F3 is fixed.

### K4 unknowns
Each case has a stated outcome; "could not be read" never reads as "no lessons":
- **Unreadable registry:** `problem`. The gate note says "could not be read", the brief line says "could not be read", the verb exits 1 printing the problem.
- **Damaged catalogue:** `CATALOGUE_PROBLEM` or "no row for …" (`:460-462`).
- **Exception:** `lessons`' outer `except` returns a problem (`:478-479`). `stand_lesson_lines` has its own `except` and gives one line (`brief_pack.py:2693-2694`).
- **No stand, or the placeholder:** `no_stand`, and the readers print nothing (E53). The verb says "no stand is chosen".
- **Gate with two stands and none named:** `_selected_environment` returns `{}`, so the gate returns silently (tested).
- **Empty list:** nothing (gate, brief); "no lesson is recorded for X" (verb).
- **Residual:** rows of the key in a shape `_usable` refuses (a wrong scope or state) are skipped silently. This is the registry's existing "asking side" rule (`:193-203`), not new.

### K5 the gate note never blocks
- `check_stand_lessons` (`gate_preflight.py:3210-3230`) calls only `self.note`.
- `note` (`:1664-1668`) appends to `self.info`. `add` (`:1620-1662`) is the only writer of `self.findings`, and `can_proceed = not r.findings` (`:6085`).
- The only road to a card is `run`'s `except` turning an exception into `unavailable`, which becomes `add(FACTORY_DEFECT)` (`:6078-6082`, `:1670-1673`). `PK.lessons` never raises, and `_selected_environment` reads config dicts only. Residual accepted: it is the common road for every check.
- Tested: `findings == []` in all five gate rows.

### K6 the three call sites, and the roles
- **Same function:** the manual-stand branch and the S5 heads both call `stand_lesson_lines`, so the format is the same. The stand lookup is not (F1): for the same story, the manual runner and gate can show lessons while `qa-automator` and `qa-code-critic` show none.
- **Roles that act on the stand:**
  - `qa-automator` (S5 head): gets the lines when the pipeline names the stand; misses them under F1.
  - `qa-code-critic` (S5 head, same block): same.
  - `qa-runner` manual, not walking (`## The stand`): gets them.
  - `qa-runner` manual, walking (thin walk brief plus app card): does not get them (F5).
  - `qa-runner` on an automated S5 window, and `qa-failure-analyst` (judges red tests, where a timeout red may be the stand slowness the person taught): do not get them. This is by the spec's decided scope (E55, F-B3 (b)), so it is not a finding of this diff. Proposed node below.

### K7 census and `breach=1`
- **Run:** `python -m pytest ai-packages/qa-factory/scripts/tests/test_judgment_census.py -q -s` in the worktree printed `952 units … breach=1; … conductor=476` and `census breaches: validate_artifacts.py::check_behaviour_claims`, then `21 passed in 27.95s`.
- **At 5d79f97:** the fixture's ratchet has `"breach": 1` (fixture line 4). The row `validate_artifacts.py::check_behaviour_claims`, class `meaning-proxy`, is at fixture line 887. `validate_artifacts.py` is not in the diff.
- **Conclusion:** the breach was there before this diff; not blocking.
- **This diff's census change:** one row added (`gate_preflight.py check_stand_lessons`, shape, conductor, data). Units go from 951 to 952. `blocking_per_role.conductor` stays 476, and no ratchet value moves (brief item 9: no raise).

### K8 the two test deviations
- **`manual_stand_lines` with lessons:** pinned. "the manual runner's stand carries the same lines" compares the filtered list with the formatter output for the same stand, and E46 is pinned in the manual section too. Placing the row in a new scenario instead of the manual table is acceptable (outside owns).
- **E54:** not pinned (F4). The assertion never shows the brief was over the ceiling. Missing row: lessons with 200-character words (about 3.4 KB, estimate) on a story whose brief then goes past 6 KB. Assert the lesson lines whole in the head, and that either a trimmed part is listed under `## Not in the brief` or `over_line` is present.

### K9 duplication and code quality
- **DUPLICATION AND CONSISTENCY:** F7 (two copied blocks inside the diff, one near-copy), F8 (three definitions of control characters), F1 (a fourth way of finding the story's stand).
- Greps for this answer:
  - `ord\(ch\) (<|>=) 32|CONTROL_RE|…` over `scripts/*.py`;
  - the `stand_name` / `_selected_environment` / `_stand_pick` definitions, read;
  - `acting_line`.
- The clone ratchet output from the builder ("0 new") was taken as given and not re-derived.
- **CODE QUALITY:**
  - New functions are all well under 60 lines: `lessons` `:447-481` has 35, `cmd_lesson` `:919-949` 31, `check_stand_lessons` 21. Nesting is no deeper than 3 levels.
  - No dead branches.
  - `out["rows"]` is read only by tests and the `lessons` verb indirectly. It is in the spec, so not a finding.
  - Names are true, with one exception: the gate note's "(the roles read it)" is false under F1 and F5.

### K10 analogs (named, not widened)
Other things said during a run that die with the run in the same way:
- the person's answer when "the stand got in the way" (`driver_dispatch.py:3058`, `fixed` / `debt` / `stop`): story-scoped;
- the walkers' notes in the app card (`app_card.py` `NOTES_REL` under `task_root`, `:439`): role words about the app, story-scoped;
- S9 `knowledge_fold` `stand_quirk`: already routed to this key by F-B1 (the coordinator's OF3 finding carrier).

I did not check whether the first two should outlive the run. They are named as analogs only.

### ONE ROAD (brief item 12, P31)
- F1 is a residual of this class inside the diff: one fact, "the story's stand", found four ways. They are:
  - `stand_gaps.stand_name`: falls back to the raw name and then the placeholder;
  - `_selected_environment`: falls back to `{}`;
  - `_stand_pick`: falls back to the named name;
  - the raw field at `brief_pack.py:4199`.
- Fix in this round: the S5 head uses `_stand_pick`, like its twin.
- The three earlier ways are older than this diff. I propose a node (owner: Lead, pile onboarding-forge or the stand-identity pile): one stand resolver for the readers of the story's stand.
- No language, project or case exclusion was found. Grep of the diff for language or runner names: none.

### FR walk and AR (check of the builders' claims)
- **FR:**
  - A: FR-1/FR-2 met (F6 minor).
  - B: FR-6 not met (F2).
  - C: FR-11 met (`command_problems` was in B1's 164 passed); FR-12 met.
  - D: FR-59 met.
  - G: FR-30. The builder's `--lang 4/4` was taken as the witness. The test literals use the `NON_ASCII` constant. Not re-run.
- **AR met:** AR-3, AR-13, AR-14, AR-22 (the producer row exists, and the `needed_by` readers exist at the named functions), AR-24, AR-25, AR-28, AR-29.
- **AR-19 (stage twins) not met:** F1, F5.
- **AR-20:** no ratchet moved.

## Class-wide (SIBLING_MAP)
- **Axis 5 (stage twins: manual runner vs automator/code critic):** open (F1 lookup, F5 walk road).
- **Axis 11:** the lookahead `lesson` vs `lessons` is tested.
- **Axis 18/32:** the census row lands with its unit; no ratchet moves.
- **Axis 34 (one road):** F1 in this round, plus the proposed resolver node.
- **Axis 35:** the `PT-human-word` text and the `state-exits.md` cell are closed.

## Fix list (for a fresh builder; one line per fix)

1. **F1:** `brief_pack.py:4199`: pass `_stand_pick(hooklib.load_config() or {}, str(pipeline.get("environment") or ""))[1]` instead of the raw field. Test row in `ss1_11_stand_lessons`: a one-stand config, pipeline without `environment`, one lesson. The line is present in the `qa-automator` and `qa-code-critic` heads and equals the manual-section line.
2. **F2 + F3:**
   - `PK.lessons` also returns `more: <k>` (0 when none). It keeps the pointer line in `lines` for the brief, with the stand quoted: `--stand "<stand>"`.
   - `check_stand_lessons` drops a trailing pointer line from the person's note and says `and <k> more (the roles are told how to read them all)`.
   - On a problem, it notes in words only (`… could not be read this time`) and passes the problem as the machine field `problem=`, as the note at `gate_preflight.py:2603` does.
   - Test rows:
     - `test_gate_preflight.py` `test_stand_lessons_are_one_note_never_a_card`, 11 lessons: the note holds no `project_knowledge.py` and no `--stand`.
     - Same test, unreadable registry: no `.json` in the message, and `problem` is in the info row.
     - `test_project_knowledge.py`: a stand `staging eu` with 11 lessons gives a pointer with `--stand "staging eu"` and `more == 1`.
3. **F4:** `test_project_knowledge.py` `test_lessons_cap_ten_lines_and_cut_the_words_at_200`: add 10 lessons (10 lines, no pointer, `more == 0`) and words of exactly 200 characters (no ` ...`) and of 201 (cut). In `test_brief_pack.py` `ss1_11_stand_lessons`: an E54 row with 10 lessons of 200-character words where the brief is over `BRIEF_MAX_BYTES`. Assert the lines whole in the head, plus a `## Not in the brief` entry or `over_line`.
4. **F5** (the coordinator adds `app_card.py` and its test to the owns):
   - `app_card.py:163-164`: carry the `"- Stand lessons:"` lines into the Stand section.
   - `app_card.py:439-450`: add `PK.record_path(project)` to `inputs_hash`.
   - Test row in the app card's existing test: one lesson gives the line in the card, and a second `record` changes the hash.
5. **F6:** `cmd_lessons` (`project_knowledge.py:953-957`): replace "so nothing was recorded" in the `_context` problem text with a read wording (e.g. `there is no story <T>; pass the running story's id as --task, or --stand <name>`). Row in `test_lessons_reader_and_verb`: `--task T-9` stderr has no "recorded".
6. **F7:** extract `_story_stand(ns, task_root, cfg) -> (stand, refusal)` from `cmd_side` `:995-1002` and call it from `cmd_lesson` `:946-955`. Extract `_untrimmed_or_control(text)` for `:591` and `:630`. Existing tests stay green (`test_lesson_stand_comes_from_the_story_or_is_refused`, the side CLI tests).
7. **Proposed nodes (not this round; owner Lead):**
   - (a) one stand resolver for "the story's stand" (four ways today, ONE ROAD residual);
   - (b) the stand lessons for `qa-failure-analyst` and the automated S5 `qa-runner` (E55 scope, re-asked);
   - (c) F8: one definition of "control character" (C0/C1) across `project_knowledge._plain`, `http_client._CONTROL_RE` and `planning_contract._GROUNDING_CONTROL`.

## Trail
- **Read:**
  - The spec §2 whole, §3, §3a, §5, §8 (lines 228-519).
  - The full non-test diff `5d79f97..4a74dc3`, and the test diffs of `test_project_knowledge.py`, `test_brief_pack.py`, `test_gate_preflight.py` and `test_guard_project_knowledge.py`.
  - `project_knowledge.py:95-230, 603-842, 978-1013`.
  - `gate_preflight.py:1615-1690, 2598-2608, 5128-5135, 6060-6128`.
  - `brief_pack.py:64-77, 865-900, 2528-2550, 2697-2735, 4190-4201, 4240-4269, 4300-4350`; grep of the ceiling logic `:4383-4524`.
  - `stand_gaps.py:148-159, 776-792, 985-995`.
  - `app_card.py:1-30, 150-175, 436-457`.
  - `driver_s0.py:2270-2295, 2380-2422`.
  - `environment_record.py:208-232`.
  - `references/human-questions.md:1-62`; `tools/critic_verdict.schema.json`; `docs/tasks/critic-diff-brief.md:40-89`; the agents' `tools:` lines.
  - The census fixture at 5d79f97 (ratchet line 4, line 887).
- **Greps, each with a positive control** (it found the known definitions):
  - `stand_lessons|LESSONS_KEY|\.lessons\(` and `project-knowledge\.json|RECORD_REL|record_path\(|PK\.load\(`, case-insensitive, over the package and scripts;
  - `["']environment["']\]\s*=|setdefault` and `["']environment["']\s*:` over scripts;
  - control-character predicates.
- **Rerun:** `test_judgment_census.py` (output quoted in K7). `test_brief_pack.py` was not re-run: no finding depends on it. F1 is a code trace whose case the existing scenario does not build.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "F1 (B2): brief_pack.py:4199 reads the raw pipeline.environment for the S5 automator and code-critic head, while its twin manual_stand_lines (:2711 via _stand_pick), the gate (_selected_environment) and the writer (stand_gaps.stand_name) fall back to the only configured stand. One-stand config with pipeline environment null gives lessons in the gate and the manual runner and none for qa-automator and qa-code-critic (P31, AR-19)."
  ],
  "fixes": [
    "F1: brief_pack.py:4199 use _stand_pick(hooklib.load_config() or {}, pipeline environment)[1]; test row in ss1_11_stand_lessons: one-stand config, no pipeline environment, line present in both S5 heads and equal to the manual line",
    "F2+F3: PK.lessons returns more:k and quotes the stand in the pointer; check_stand_lessons words the cut and the problem plainly and passes the problem as the machine field problem= (as gate_preflight.py:2603); rows: 11 lessons note has no script name, unreadable note has no .json, stand with a space quoted",
    "F4: AT rows: exactly 10 lessons (no pointer), words of 200 (not cut) and 201 (cut); E54 row driving a brief over BRIEF_MAX_BYTES with the lesson lines whole",
    "F5 (owns widened by the coordinator): app_card.py:163-164 keep the '- Stand lessons:' lines, inputs_hash adds PK.record_path(project); row in the app card test",
    "F6: cmd_lessons read-wording for the _context refusal; row --task T-9 stderr has no 'recorded'",
    "F7: extract _story_stand from cmd_side/cmd_lesson and _untrimmed_or_control for the two subject predicates; existing tests stay green"
  ],
  "class_completeness": "Axis 5 stage twins open: S5 head stand lookup (F1) and the walk road through the app card filter (F5). Axis 11 lesson vs lessons tested. Axis 18/32 census row with its unit, no ratchet moved; breach=1 predates the diff (validate_artifacts.py::check_behaviour_claims, ceiling 1 at 5d79f97). Axis 34 one road: F1 fixed this round; four stand resolvers proposed as a Lead node. Axis 35 PT-human-word and state-exits cell closed. Analogs named: stand-got-in-the-way answer, app card walker notes, S9 stand_quirk (already routed).",
  "trail": {
    "read": [
      "docs/tasks/specs/t-365-f6-39-ss1-11-specs.md:228-519",
      "git diff 5d79f97 4a74dc3 (all non-test files, four test files)",
      "ai-packages/qa-factory/scripts/project_knowledge.py:95-230,603-842,978-1013",
      "ai-packages/qa-factory/scripts/gate_preflight.py:1615-1690,2598-2608,5128-5135,6060-6128",
      "ai-packages/qa-factory/scripts/brief_pack.py:64-77,865-900,2528-2550,2697-2735,4190-4201,4240-4269,4300-4350",
      "ai-packages/qa-factory/scripts/stand_gaps.py:148-159,776-792,985-995",
      "ai-packages/qa-factory/scripts/app_card.py:1-30,150-175,436-457",
      "ai-packages/qa-factory/scripts/driver_s0.py:2270-2295,2380-2422",
      "ai-packages/qa-factory/scripts/environment_record.py:208-232",
      "ai-packages/qa-factory/references/human-questions.md:1-62",
      "ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json at 5d79f97 and 4a74dc3",
      "docs/tasks/critic-diff-brief.md:40-89",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {
        "command": "( cd .claude/worktrees/ss1-11-b1 && python -m pytest ai-packages/qa-factory/scripts/tests/test_judgment_census.py -q -s )",
        "result": "952 units; breach=1; conductor=476; census breaches: validate_artifacts.py::check_behaviour_claims; 21 passed in 27.95s (breach row and ceiling 1 present at 5d79f97)"
      }
    ]
  }
}
```

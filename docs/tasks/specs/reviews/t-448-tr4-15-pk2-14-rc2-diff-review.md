# t-448 — critic diff gate: TR4-15, PK2-14, RC2-1, RC2-2 (topic: a role's or a person's data reaches its reader whole)

Reviewer: critic (Opus). Read-only on the repo; this file is the only write. Branches are cut from origin/main 33dbe73; every diff read with
`git -C <wt> diff refs/remotes/origin/main...HEAD`.

## Verdicts per node (input to the Lead's acceptance; the acceptance decision is the Lead's)

| node | verdict | blockers |
|---|---|---|
| TR4-15 (b700f0f) | fit_with_fixes (one non-blocking text fix) | none |
| PK2-14 (a7e7812) | **unfit** | B1: the early return erases the registry's roles, and the noticed-role writer then overwrites the person's `known` / `not_needed` answers (reproduced) |
| RC2-1 (05dfffe) | fit_with_fixes (fix before merge) | none block on their own; F3 has to be fixed before the merge |
| RC2-2 (f388bfe) | fit | none |

Overall verdict for the topic: **blocker**, because of PK2-14 B1. TR4-15, RC2-1 and RC2-2 can merge on their own once their fixes are in.

---

## TR4-15 — `observation` field of a bug draft

**K1 fit to DoD, edge by edge.** Read `place_answers.py:172-209` on the branch.
- Position: the new rule sits after the `case` loop and before `rows`/`violates`. A draft whose `case` matches a target returns at :195,
  before :197 is reached. Test row "case match wins over a different observation" → `case-TC-007`. Kept.
- Unmatched `observation` → falls through the loop to (3)/(4). Rows "foreign well-formed", "TC-004", "obs-" → `draft-d1`. Kept.
- `case` holding `obs-...` is not joined: the case loop compares against `target["case"]`, never against `target["id"]`. Row "case holding an obs id". Kept.
- Non-string, empty or whitespace-only reads as absent (`isinstance(str) and strip()`). Rows: number, list, None, "", "   ". Kept.
- No new raise: the loop is over `targets`, which is always a list here (None is replaced at :187-191). `test_no_targets_no_exception` covers it. No validator change. Kept.
- Builder's own decision: an `observation` equal to a pinned target's id (`case-TC-006`) joins it. The DoD says "a target's id", so this is within it and harmless.
- The test file is new and has a keep row in `test-layers.json` (layer `table`). It imports its fixtures from the quarantined `test_place_answers.py`. That is existing practice: `test_place_driver`, `test_place_session`, `test_walk_oracle` and `test_walk_receipt` do the same, so it is not a finding of this node.
- Control re-run: `python -B -m pytest scripts/tests/test_place_of_draft_observation.py -q -p no:cacheprovider` → `14 passed in 7.22s`. This matches the attached witness.

**K2 FR-38/AR-10 and other readers (AR-22).**
- The contract sentence names the field, its form (`place_id_pattern`, named, not copied), when to write it, and "never put it in `case`". That is enough to write a valid value.
- **F1 (non-blocking, fix before merge):** the sentence does not say where the analyst reads the id. Its sibling text in `references/role-commands.json` (the `manual_capture` and `place_answers.py write` rows) says "the place id as `place_answers.py list` prints it". The analyst has no other way to see `obs-<dispatch>-<index>`: `investigation.py:170` builds it, and the charter's tools line (`agents/qa-failure-analyst.md:74`) names `place_answers.py list`. Fix: one clause, then regenerate the slice.
- Other readers: every production reading of "which place a draft belongs to" goes through `place_of_draft`: `place_answers.py` :282, :460, :590, :677 and `bug_records.py` :907, :930 (the U2 reading). There is no draft key whitelist or validator. `field-producers.json` lists only required fields, and `observation` is optional. Result: no reader meets the new field without a move.

**Tests:** red-first with the rule removed gave 3 failed (attached). A row-table on role output is the encoding battery for input from outside, so the test lines outweighing the product lines has its reason.

---

## PK2-14 — roster on an unreadable config

**K1, the three config worlds.**
- **Absent file:** `_read` → `(None, "absent", "")`. No problem; the roster is built from the registry. Kept.
- **Caller-passed cfg:** `_read` returns it as given. Kept (test `test_state_and_roster_with_a_given_cfg_ignore_the_file`).
- **Present but unreadable:** a non-empty `problem` comes back, and the registry problem is kept next to it. Kept as far as the DoD goes.
- `state()` stays `unknown`. Kept.

**B1 (BLOCKER) — the early return erases the registry and the person's answers get overwritten.**
- At `project_knowledge.py:424-429` the unreadable branch does `return out` with `elements=[]` and `removed=[]`. That throws away the
  `product.roles` registry rows. Those rows are readable and do not depend on the config.
- The one caller that passes `cfg=None` is `notice_from_handoff` (:649). It builds `have` from `held["elements"]` (state `known`) and `held["removed"]`, then calls `record(...state=NOTICED...)` for every role not in `have`.
- `record` (:580-582) writes a new row whenever the latest state differs. The guard "write only if the latest state is absent or noticed" is PK2-18, not yet done.
- So with a broken config, a role the person confirmed (`known`) or turned down (`not_needed`) gets a fresh `noticed_unconfirmed` row, and that row becomes its latest state.
- Probe (`scratchpad/probe/pk_probe.py`): registry `auditor: not_needed`, `editor: known`, config `{broken`, strategist names both.
  - BRANCH: `roster elements: [] removed: []` / `written: ['PK-3', 'PK-4']` / `state auditor: noticed_unconfirmed | editor: noticed_unconfirmed`
  - MAIN (origin/main `project_knowledge.py`): `roster elements: ['editor'] removed: ['auditor']` / `written: []` / `state auditor: not_needed | editor: known`
- This is a regression of AR-24 (the person's word kept whole) and FR-7: gate A asks the removed role again. The commit names AR-13 and AR-28 but not AR-24, which it breaks.
- The DoD line "roles empty" was a dispatcher spec defect on this edge: it is silent on the registry part of the roster.
- Fix: see Fix list P1. The registry part stays; the config part and the `account` flag become unknown.

**K3 — who reads `roster()['problem']`.** Walked every production caller (`grep "roster("` in the package, positive control: the definition and :649 found).
- `brief_pack.py:2818-2822` (S3/S4 brief): `cfg = hooklib.load_config() if cfg is None else cfg`, then `{}`.
  `hooklib.load_config` (:971-975) turns a broken or non-object config into `{}`. A dict reaches `roster`, so the new branch **never fires** and the brief prints `S3_ROSTER_NONE`: "no roles".
- `first_look.walk_actors` (:253) receives `hooklib.load_config() or {}` (brief_pack:3852) or `self.config` (driver_dispatch:2486, driver_stage_plan:239). Same result.
- `gate_preflight.py:743` (`cfg` from its caller) and `:2521` (`self.config`, read at :1501 by `_read_json(..., {}) or {}`). Same result. At :743 an empty roster only makes it ask, which errs toward safe.
- Conclusion: the new problem reaches **no person and no role** today. Its only reader is the noticed-role writer, and B1 harms exactly that reader.
  The goal of the finding (FR-41: unknown shown as absent) still fails on every person-facing and role-facing path. The cause is upstream: the project-config reader class on SIBLING_MAP axis 16, queued in `plans/piles/forge/findings/20261010-json-readers-outside-the-list.md`.
- Under the DoD ("a caller-passed cfg is used as is") this does not block the node. It is queue item Q1.
- Once wired, brief_pack's problem wording would also be wrong: "the record of earlier answers cannot be read (...); listed from the stand's accounts only" does not describe a config problem. That goes into Q1 too.

**K3 — problem text.**
- FR-1/FR-2: it says what is wrong, what was expected ("one JSON object") and a door ("repair that file (or move it aside and run onboarding again) and ask again"). The door is usable by the reader. No paths of the plugin, no tracebacks. It reads as plain English and fits the human-questions form for a statement.
- **F2 (folded into P1):**
  - The text drops the specific reason `_read` already computed (`unreadable`: the parser's why, cut at 200), so FR-1's "what is wrong" stays generic.
  - "the product's roles are not known" over-claims once the registry part is kept.

**K3 — `_config` / `_context` left as they are.**
- `_context` (:697-714) gives the CLI writers `_config(root, None)`, which is `{}` on an unreadable file.
- The node did not change this, so it is not a blocker for this node.
- It is **not** PK2-18 either: PK2-18 is the check-then-write lock in `record`. It is queue item Q2 (same class as Q1).

**Control re-run:** `python -B scripts/tests/test_project_knowledge.py` → `97 passed in 8.67s`. This matches the witness.
The tests do not catch B1: none combines registry rows with an unreadable config.

---

## RC2-1 — the person's words on the minimal brief line

**K1 fit.**
- The words are cut by the sisters' `_short(key, DECISION_CHARS_MIN)`, with the pointer when cut.
- The same words under several questions appear once ("the same text as under Q1").
- Wordless, kept-open and not-needed lines are unchanged.
- Edges are tested at limit-1, at the limit and at limit+1, plus folding and wordless inputs (`p4_min_words`). Fits as written.

**F3 (fix before merge) — the minimal line carries a literal `<decisions>` placeholder that is never resolved (FR-37, FR-15).**
- `WORDS_BY_REFERENCE` contains `<decisions>`. The placeholder is replaced only for `shown` (`brief_pack.py:4381`, level 2). At level 1 the render does `parts += minimal` (:4383) **unreplaced**.
- Before RC2-1 no minimal line carried `<decisions>`. The PC2-6 O-c comment says the side-file pointer at level 1 is the line under «Not in the brief», given once.
- Probe (`scratchpad/probe/rc_probe.py`, 300-character answer): `shown has <decisions>: False | shown len: 395`, and the minimal line ends with `...; the person's words: the whole text is in <decisions>`.
- So the level-1 brief tells the role that the words are "in <decisions>", which is not a path. The side file does exist at level 1 (`sides_needed["decisions"] = dec_level < 2`, :4453), so the fix is a substitution, not a new file.
- The test pins the line text inside `question_answer_lines`, but no test renders level 1. That is the missing junction test.

**K4 — the doubled prefix.**
- On a cut line the text reads `the person's words: www...; the person's words: the whole text is in <decisions>`. Two prefixes read like two answers, which is a text defect.
- The reader is a role, so FR-6 (person text) does not strictly apply, but FR-10 (one packet does not contradict itself) does in spirit.
- Fix it with F3 in one edit (P3).

**K4 — size.**
- Each distinct-words answer line at level 1 grows by at most 22 + 240 + 54 = 316 B (the prefix `; the person's words: `, the words, then `; ` plus the pointer). After P3 the cut suffix is shorter.
- Ceiling: `BRIEF_MAX_BYTES = 6 * 1024` (:54). The O-d guard (:4449-4453) takes the level-1 rung only when it strictly shrinks the brief, so a level 1 that saves nothing is never chosen.
- I did not measure a real brief, so the margin against 6 KB on a story with many answers is an **estimate, not verified**. The builder's 6 KB checks in test_brief_pack passed (957/957 attached).

---

## RC2-2 — the brief note is the helper's own `brief: ` line

**K1.**
- The exit code and the file are checked first (`story_step.py:452`). The `brief:` selection lives only inside the success branch, so a prefixed line cannot turn a refusal into a success. Test: code 3 with a `brief:` line → refusal.
- No prefix → the last line, as before. Case-sensitive and stripped, with leading blanks allowed.
- The producer (`brief_pack.py:4573`) prints exactly one `brief: ...` line on stdout. `_run` joins stdout before stderr (:152), so a stderr warning used to land last. That is what the fix addresses.
- Fits.

**K5 analogs.**
- `story_step.py:984` (the builder's ":979") `notes.append("stage_done running: " + out.splitlines()[-1] if out else "stage_done running failed")`
  is **not a bug**. The conditional expression binds looser than `+`, so it parses as `("…: " + last) if out else "…failed"`, which is the intended meaning. An `out` of whitespace only still gives `['']` or `[' ']` with no IndexError.
  A clarifying pair of parentheses is optional and needs no queue item.
- `driver_stage_s6.py` :432/:469/:697/:718/:967, `driver_stage_s7.py` :192/:775, `driver_stage_s8s9.py` :57/:65/:125/:137: all are **refusal tails** (exit ≠ 0). There the wanted line is the error, which is the helper's last line, and the helpers print no own marker to select by.
  This is not the same class as RC2-2 (a success summary read by position). No queue.

---

## K6 DUPLICATION AND CONSISTENCY
- RC2-1: `len(re.sub(r"\s+", " ", key).strip()) > DECISION_CHARS_MIN` (:1657) re-derives `_short`'s fold (:1094) to learn whether `_short` cut. It is a second copy of the fold rule. Non-blocking.
  Fold it into P3: `cut = _short(key, MIN); clause += cut; if cut != re.sub(...)` is no better. The smallest consistent change is a one-line helper `_is_cut(text, limit)` next to `_short`, or leave it as is. Severity: queue-free nit, not required.
- PK2-14: `cfg = data if isinstance(data, dict) else {}` repeats the body of `_config` (:224-226). It disappears in P1.
- TR4-15: none found. Grepped `place_of_draft` callers and draft-field readers (`distinct_defect` in the package scripts: only bug_records), and found no second join.
- Clone ratchet: the branches' `forge-check` output was not attached. That is batch level, read at the canon, not re-run here.

## K6 CODE QUALITY
- No new function over 60 lines and no nesting over 3 levels in new code. No dead branches.
- RC2-1 annotation: the docstring says "WORDS_BY_REFERENCE when cut", and after P3 the docstring changes with the code.
- PK2-14's comment "the roles are UNKNOWN, not none" lies about the registry part (B1). P1 fixes it.

## K7 class completeness (SIBLING_MAP)
- **Axis 5 (stage twins):** n/a. None of the three changes a stage-specific twin: `place_of_draft` is one reading, the roster is one reader, `_brief` is one site.
- **Axis 16 (one JSON reader, project-config reader class):** PK2-14 fixed one instance, `_read` in roster. The siblings that defeat it are `hooklib.load_config`, `gate_preflight` :1501 and `_context`.
  The class is queued in the axis-16 finding, but that finding does not record the roster consequence → Q1/Q2.
- **Axis 31 (role carriers):** TR4-15 puts the field into the contract, the owner of the aspect, and leaves the charter to TR2-13 per the finding. Kept.
- **Axis 32 (judgment):** see K8.
- **Axis 34 (one road):** none found. Grepped the diffs for language, runner and project names: none.
- **Sweep-the-artifact:**
  - RC2-1's neighbours in `decisions`: gate, warning, override and halt minimal lines use `_short` with no pointer and no placeholder. Consistent with P3's alternative (Lead decision L2).
  - `question_answer_lines` is the only branch carrying a pointer.

## K8 standing questions 10 and 11
- **Q10 (architecture):**
  - TR4-15 names AR-10 and AR-22. Kept: one producer, one reader, both walked.
  - PK2-14 names AR-13 and AR-28 but **breaks AR-24** (B1) and does not name it. A producer of the person's words is overwritten while its reader stays: blocks.
  - RC2-1 names AR-24. Kept in substance, but the carrier text names a placeholder path (F3, FR-37).
  - RC2-2 names AR-22. Kept.
- **Q11 (judgment):** none of the four adds a check that judges meaning. TR4-15 joins by id equality and the analyst decides the belonging. No census row and no `blocks_override` was added. No craft markers were added. `judgment: none` holds on all four.
- **Q9 (ratchets):** no in-tree ratchet row was added or raised. `test-layers.json` +1 keep row is not a ratchet.

---

## Fix list (a fresh builder can execute it)

**P1 — PK2-14, BLOCKING.** File `ai-packages/qa-factory/scripts/project_knowledge.py`, function `roster`.
- Replace the early `return out` with a flag:
  `config_unknown = bool(unreadable)`. When it is set, put the problem text in, set `cfg = {}`, and continue.
- The registry loop runs as is, so `known` rows go into `elements` and `not_needed` rows into `removed`.
- `_stands(cfg)` yields nothing, so no config roles are added.
- In the final loop: `element["account"] = None if config_unknown else (...)`. An account that cannot be read is unknown, not False.
- Text: `f"qa-factory/config.json is there but cannot be read ({unreadable}); the roles of the stand accounts and which role has an account are not known; repair that file (or move it aside and run onboarding again) and ask again"`. Keep the registry problem joined with `; `.
- Update the inline comment to match.
- Tests in `scripts/tests/test_project_knowledge.py`:
  - (a) registry `auditor: not_needed` + `editor: known`, config `{broken` → `roster(root, None, "dev")`: `editor` in elements with `account is None`, `auditor` in removed, problem non-empty.
  - (b) the same world plus `notice_from_handoff` with `story_roles` naming both → returns `[]`, and the two states stay `not_needed` / `known`. This is the probe in `pk_probe.py` turned into a test.
  - Adjust `test_roster_says_an_unreadable_config_is_unknown` (`elements == []` still holds with no registry rows).
- Witness: `python -B scripts/tests/test_project_knowledge.py`, red-first on a7e7812 for (a) and (b).

**P2 — TR4-15, non-blocking.** File `ai-packages/qa-factory/references/artifact-contract-run.md`, the `observation` sentence.
- After "e.g. `obs-...`" add: "the place id as `place_answers.py list` prints it".
- Then `python -B scripts/contract_slices.py --write` from the package directory.
- Witness: `python -B scripts/contract_slices.py --check` → "all present and fresh".

**P3 — RC2-1, fix before merge.** File `ai-packages/qa-factory/scripts/brief_pack.py`.
- (i) In `question_answer_lines` (:1658) replace `minimal_clause += f"; {WORDS_BY_REFERENCE}"` with
  `minimal_clause += "; the whole text is in <decisions>"`. This gives one prefix per line.
- (ii) In the render of `build`, level 1 (:4383), replace `parts += minimal` with
  `parts += [line.replace("<decisions>", side["decisions"]) for line in minimal]`.
- Update the docstring of `question_answer_lines`.
- Test in `test_brief_pack.py`:
  - Adjust the two `p4_min_words` / `p4_long_words` expectations.
  - Add one build-level check: a story with a 300-character answer forced to level 1 (the existing level-1 fixture of PC2-6) → the brief text has no literal `<decisions>` and does name the side-file path.
- Witness: `python -B scripts/tests/test_brief_pack.py` (all ok), red-first: the new build check fails on f388bfe.

## Lead decisions (not fixes; the decision belongs to the Lead)
- **L1 (PK2-14):** amend the node's DoD "roles empty" to "registry roles kept, config roles and the account flag unknown". P1 assumes yes. The DoD as written produced B1.
- **L2 (RC2-1):** alternative to P3 (ii): drop the pointer from the minimal line entirely. The line would end with `_short`'s `...` like its sister minimal lines (gate, warning, override, halt), and the «Not in the brief» line stays the one pointer (PC2-6 O-c).
  This is more consistent and shorter, but it departs from the DoD's "plus WORDS_BY_REFERENCE when cut". The Lead chooses; P3 is the default because it keeps the DoD.

## Queue items (findings, one line each; the Lead writes them)
- **Q1** `project-knowledge`: the roster's unreadable-config problem never reaches a person or a role. brief_pack:2818, first_look.walk_actors via brief_pack:3852 / driver_dispatch:2486 / driver_stage_plan:239, and gate_preflight:743/:2521 pass a cfg that `hooklib.load_config` or `gate_preflight` :1501 already turned into `{}`. brief_pack's problem wording does not fit a config problem. | перенос: findings/<new> → link to the axis-16 finding `plans/piles/forge/findings/20261010-json-readers-outside-the-list.md` (project-config reader class) | обоснование: the class is upstream of the node's DoD | подтвердил: —
- **Q2** `project-knowledge`: `project_knowledge._context` (:714) gives the CLI writers `{}` for an unreadable config, so a stand or account record then refuses or answers on "no stand" instead of "config unreadable". Same class as Q1, not PK2-18. | перенос: findings/<new> | обоснование: the node left it by its DoD | подтвердил: —

## Trail
- Read:
  - `docs/tasks/critic-diff-brief.md` (whole); `docs/SIBLING_MAP.md` (axis headings; axis 16 lines 360-372)
  - the three diffs in full
  - TR4-15 finding; PK2-14 finding; `place_answers.py:160-240`; `project_knowledge.py` :205-300, :395-470, :565-660, :697-714
  - `brief_pack.py` :54-60, :1093-1096, :1610-1665, :1733-1745, :2805-2850, :4365-4390, :4435-4460, :4565-4580; `first_look.py:233-265`; `gate_preflight.py` :730-760, :2510-2535
  - `hooklib.py:971-975`; `story_step.py` :143-152, :445-460, :970-990
  - `references/place-answers.json:10`; `references/role-commands.json` (place_answers/manual_capture rows); `agents/qa-failure-analyst.md` (grep)
  - commit messages of b700f0f, a7e7812, 05dfffe, f388bfe
- Greps (positive controls: each found its definition site):
  - `roster(` and `place_of_draft` callers; `distinct_defect` readers; `<decisions>`; `WORDS_BY_REFERENCE`; `splitlines()[-1]` in story_step/driver_stage_s6/s7/s8s9
  - `PK2-18` in the project-knowledge pile
- Runs:
  - `python -B -m pytest scripts/tests/test_place_of_draft_observation.py -q -p no:cacheprovider` (tr4-15) → `14 passed in 7.22s`
  - `python -B scripts/tests/test_project_knowledge.py` (pk2-14) → `97 passed in 8.67s`
  - `python -B scratchpad/probe/pk_probe.py` branch vs main → shown under B1
  - `python -B scratchpad/probe/rc_probe.py` → shown under F3
  - Not run: `test_brief_pack.py` (the probe covers the verdict point) and ratchets (batch level)

```json
{
  "verdict": "blocker",
  "blockers": [
    "PK2-14 B1: project_knowledge.roster returns early on an unreadable config with elements and removed empty, dropping readable registry roles; notice_from_handoff (roster(root, None, '')) then records noticed_unconfirmed over the person's known/not_needed answers (probe: branch writes PK-3, PK-4 and both states become noticed_unconfirmed; main writes nothing). AR-24/FR-7 regression, AR-24 not named in the commit."
  ],
  "class_completeness": "Axis 16 (project-config reader class): PK2-14 fixed only roster's own read; every production caller (brief_pack, first_look.walk_actors, gate_preflight) passes a cfg already turned into {} by hooklib.load_config or gate_preflight :1501, so the new problem reaches no person or role; queued as Q1, with _context as Q2. Axis 5 n/a (no stage twin). Axis 31 kept (the contract owns the field, the charter is TR2-13). Axis 32: no judgment moved. Axis 34: none found. RC2-2 analogs: story_step :984 is not a bug (precedence correct); driver refusal tails are a different class, no queue. Artifact sweep in brief_pack.decisions: the sister minimal lines carry no pointer, so the placeholder exists only on the RC2-1 line (F3).",
  "fixes": [
    "P1 (blocking, PK2-14) project_knowledge.roster: replace the early return with config_unknown flag, cfg = {}, keep the registry loop, account None when config_unknown; problem text carries the _read reason; tests (a) roster with registry rows + broken config, (b) notice_from_handoff writes nothing over known/not_needed",
    "P2 (non-blocking, TR4-15) artifact-contract-run.md observation sentence: add 'the place id as place_answers.py list prints it'; regenerate slices with contract_slices.py --write",
    "P3 (before merge, RC2-1) brief_pack.question_answer_lines :1658 suffix '; the whole text is in <decisions>' (one prefix); build render level 1 :4383 replace <decisions> with side['decisions'] in minimal lines; build-level test that a level-1 brief has no literal <decisions>"
  ],
  "trail": {
    "read": [
      "docs/tasks/critic-diff-brief.md",
      "docs/SIBLING_MAP.md (axis headings, axis 16)",
      ".claude/worktrees/tr4-15 diff b700f0f; scripts/place_answers.py:160-240; finding 20261110-tr1-11",
      ".claude/worktrees/pk2-14 diff a7e7812; scripts/project_knowledge.py:205-300,395-470,565-660,697-714; brief_pack.py:2805-2850; first_look.py:233-265; gate_preflight.py:730-760,2510-2535; hooklib.py:971-975; finding 20261111-chitatel-config",
      ".claude/worktrees/rc2-1 diffs 05dfffe f388bfe; brief_pack.py:54-60,1093-1096,1610-1665,1733-1745,4365-4460,4565-4580; story_step.py:143-152,445-460,970-990",
      "commit messages of the four commits"
    ],
    "reruns": [
      {"command": "python -B -m pytest scripts/tests/test_place_of_draft_observation.py -q -p no:cacheprovider (tr4-15)", "result": "14 passed in 7.22s"},
      {"command": "python -B scripts/tests/test_project_knowledge.py (pk2-14)", "result": "97 passed in 8.67s"},
      {"command": "python -B scratchpad/probe/pk_probe.py branch vs origin/main project_knowledge.py", "result": "branch: written PK-3, PK-4, auditor and editor noticed_unconfirmed; main: written [], auditor not_needed, editor known"},
      {"command": "python -B scratchpad/probe/rc_probe.py (rc2-1, 300-char answer)", "result": "shown has <decisions>: False, len 395; minimal ends '...; the person's words: the whole text is in <decisions>'"}
    ]
  }
}
```

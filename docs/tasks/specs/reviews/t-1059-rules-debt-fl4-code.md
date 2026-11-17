# t-1059 — critic, code review of t-1050 (rules-debt card FL4: an S7 rework door for a bug candidate that has no case)

Reviewed: commit `13c4a757` on `worktree-agent-ab0738c6a4bd8d773` (tree `.claude/worktrees/agent-ab0738c6a4bd8d773`), against the spec
`docs/tasks/specs/20261117-rules-debt-phase2-s9-fl-cards-spec.md` §1 (FL4 rows), §3b.1–§3b.6, §4 (F-L4-B/C/D, recommendation (a)), and
`docs/tasks/critic-diff-brief.md`.

**Verdict: NEEDS WORK.** 1 finding blocks the merge (B1: the commit turns the CI canon red). The rest are fixes for this round or notes. The
design is sound: one reader, one refusal text, unknown reads as "not known", case-only behaviour untouched. Acceptance stays with the Lead.

## Findings

### B1 — blocks merge: `references/controller-api.md` goes over the reference size cap; CI `checks / package-fast` is red
- Canon run 44034288063: job `checks / package-fast` fails, log `FAIL limits: SKILL.md / agents / references within size caps ? 1 file(s)`,
  `=== qa-factory selftest (fast): 214/215 ok ===`.
- My local re-run on the tree: `( cd <tree>/ai-packages/qa-factory && python -B scripts/selftest.py --limits )` →
  `FAIL limits ... — 1 file(s)` / `- references\controller-api.md: 12133 bytes > 12000`.
- The cause is this commit: `wc -c` of the file at the parent `027a04ea` is 11998, at `13c4a757` it is 12133 (`origin/main` is 11998 too). The
  added sentence pushes it over `REFERENCE_MD_MAX_BYTES = SLICE_MAX_BYTES` (12000).
- The builder's witness ran only `selftest.py --lang`, not `--limits`, so the report's "70/72 + rows green" did not cover this check.
- Fix: cut at least 134 bytes of `controller-api.md`. For example, merge the new sentence into the `--rows` one: "On S1-S3 `--rows TS-3`
  names plan rows (`plan_rows`), on S7 `--candidates K-n,R-n` names bug candidates (`bug_candidates`), instead of `--cases`". If that is not
  enough, trim another sentence of that paragraph. Witness: `selftest.py --limits` green.

### F1 — fix in round: two conductor-facing carriers of the `args` shape still say `"cases" | "rows"` only (AR-22, FR-10, FR-37)
- `scripts/driver_conductor.py:332`, the conductor's answer template:
  `'"args": {"stage": "S<n>", "role": "<role>", "cases": ["<id>", ...] | "rows": ["<id>", ...], "cause": "<cause>"}}]} '`.
- `references/conductor.md:94`: `Only the rework option adds "args": {"stage", "role", "cases"|"rows", "cause"}`.
- The same prompt carries `rework_args_list`, which now lists `candidates (S7 only, instead of cases)`, and `conductor-actions.json` names
  `"candidates": [<refs>]`. So one prompt shows two forms of `args` (FR-10). The conductor is the one producer of `args.candidates` on the
  driver road, and the answer form it is told to fill omits the key (FR-38).
- Neither site is in the §3b.4 reader table, so this is a spec gap that the builder's "every reader" claim carried over. It is not invented
  by the builder.
- Fix: add `| "candidates": ["<ref>", ...]` at both sites. This widens owns: `driver_conductor.py` (the prompt template) and
  `references/conductor.md` (line 94).

### F2 — fix in round: `conductor-actions.json` actions row 8 `run` still lacks the flag (FR-37)
- Row 8 `says` now says "(`--candidates <its ref>` instead of `--cases`)".
- Its `run` stays `... [--rows <ids> | --cases <ids>] ...`. The command text the conductor copies does not carry the door the `says` text
  names.
- Fix: `[--rows <ids> | --cases <ids> | --candidates <refs>]`. Same row, same file, already owned.

### F3 — fix in round (Lead's call): the analyst charter line, +45 process tokens on every S7 dispatch, can reach the role at zero standing cost (AR-11, AR-20, AR-10)
- The line in `agents/qa-failure-analyst.md` is paid on every analyst dispatch of every story. It serves only a candidate rework, which is
  rare.
- The requirement already has a conditional carrier that appears exactly when it applies. `story_step._packet_lines` and the `brief_pack`
  rework head print `Bug candidates of this dispatch: <refs> (K-n: ...; R-n: ...)` only when the packet carries `bug_candidates`.
- Proposal:
  - Append the instruction to that one line: "for each, a bug draft in the code-reading form, or the reason in your digest why no bug is
    owed".
  - Drop the charter line.
  - Put `process_ratchet_tokens.qa-failure-analyst` back to 20261.
- This satisfies FR-38 (the requirement reaches the role before the work, in the packet it acts on) and AR-10. It costs nothing on the
  other dispatches (AR-11), and the shrink-only ratchet stays unraised (AR-20).
- Card item 7's DOC key `code-reading` in `qa-failure-analyst.md` would then move to the packet-line test row (item 6). That is a spec edit
  between attempts, and the decision belongs to the Lead.
- Side remark: the charter line says "say in your digest why no bug is owed", but the digest form is "one line per failing test triaged"
  and nothing reads such a line. That is acceptable under F-L4-D (a) and gate B being asked again, but it is free prose with no reader.

### F4 — fix in round: E7 is not total. Two partial reads still give the definite "not in this story" (FR-41, FR-59)
Measured on scratchpad copies of `cart-1` with `check_delivery.bug_candidates` plus `candidate_refusal(["K-1"], ...)`:
- (a) `work/grounding.yaml` exists but is a directory. Output: `['R-13'] []` and "bug candidate(s) not in this story: K-1; ...". The reason:
  `PC.read_grounding` files "a path that is not a file" and "a file that cannot be read (OSError)" under kind `missing`, and
  `_grounding_candidates` treats `missing` as "no table", silently. An existing table that raises OSError (a lock, a permission) therefore
  reads as absent.
- (b) A non-empty register whose `## Register` heading is misspelled (35 `R-` lines). Output: `[] []` and "... not in this story: K-1; the
  story's bug candidates are none". The reason: `md_table` finds no table, so `register_rows` returns `[]`, and that reads as "read, holds
  nothing".
- Same class, a package defect: `contract.candidate_marks()` returns `()` when the vocabulary cannot be read, so every R-n is "not in this
  story".
- Direction is still safe. The ref is refused in every case, so no unknown becomes "is a candidate" and AR-28 holds. What fails is the
  claim in the text, the FR-41 half of the E7 invariant ("never 'is not a candidate' either").
- Surface: the reader `_grounding_candidates`, which FL4 promotes from a report producer to a gate input (spec "Reused function in a more
  responsible role").
- Neighbouring classes walked:
  - empty bytes: covered, gives unreadable;
  - non-UTF-8 table: covered, kind `encoding` gives unreadable;
  - no file: correctly silent;
  - not-a-file or OSError: (a) above;
  - missing table heading: (b) above;
  - vocabulary unreadable: as above.
- The spec's adversarial list did not name (a) or (b), so this is not a builder defect against the card.
- Fix (owns widening, a Lead decision): in `_grounding_candidates`, treat a `missing` problem whose path exists as `the grounding table`
  unreadable, and treat a register with text but no `## Register` table as `the requirements register` unreadable. Each gets a row. The
  same reader feeds `grounding_records` ("Left with you"), which silently drops candidates today in the same two states. Alternatively,
  queue this as a node.

### F5 — fix in round: edges with no test row (key 1)
- E4: no row has a consumer-reject record at S7 plus `--candidates`. Dropping `and not wanted_candidates` from the `sent_back` condition
  would fail no FL4 row, because `story_to_s8` holds no S7 reject record.
- E12: no row. I measured it holds: a candidate rework built with `words_given=True` on `story_to_s8` carries
  `rerun_after == {'stages': ['S8'], 'reviews': [], 'decisions': []}`, `person_words: True`, `scope: []`, and none without words. This is a
  NEW path, because before FL4 an S7 rework with an empty `wanted` never reached `_rerun_stamp`, and it is the reason the door works (S8
  and gate B run again). Pin it.
- The spec's adversarial inputs "an R-n the register holds without `bug:candidate-defect`" and "a K-n of a story whose table is not
  `implementation_source: diff`" have no row. The E11 battery uses only misspellings of R-13. Add `R-1` (a register row with no mark) and
  `K-1` on cart-1 (a current-code table) as refused "not in this story".
- Item 4: the spec asks the conductor's text to equal "the controller's text of item 2 (vii)". The row compares it to a fresh
  `candidate_refusal(...)` call, not to `text_vii`. Compare to `text_vii` itself (it is in scope) so the row would catch the controller
  wrapping the text.
- Weak rows (they cannot fail independently of the constant they read):
  - "FL4 E2: the field is compared at `materialize`" is `"bug_candidates" in IDENTITY_FIELDS`;
  - item 6 has no row for the brief head line or `PACKET_DISPATCH_KEYS` (the spec asked only `_packet_lines`, so this is a note on those
    two, not a defect).

### N1 — note: duplication (brief item 6)
- The parenthetical `(K-n: a risk in work/grounding.yaml rows[].risks[]; R-n: a register row marked bug:candidate-defect)` is typed twice:
  `story_step.py:1165` and `brief_pack.py:4506`. The plan-rows line is already duplicated the same way, so FL4 follows the existing
  pattern. Under F3, one constant (for example beside `bug_candidates` in `check_delivery`) read by both is the place to put the
  instruction once.
- `rework_args_list` copies the `CASES_IN_LIST` cut expression of the scope line, in a small helper-worthy form. This is a note only.

### N2 — note: the two judges are not symmetric on the role
- `check_args` accepts any role in `rework_roles["S7"]` (roles with accepted S7 work). The controller requires the S7 author
  (`stage_def_of("S7")["roles"][0]`).
- `stages.json` S7 roles = `['qa-failure-analyst']`, so today they coincide. A second S7 role would pass the conductor's judge and be
  refused by the controller (on the `ReworkRefused` road, not silently). The spec accepted this. Recorded for axis 5.

### N3 — note: unreadable `stages.json` gives a misleading door
- `author = (stage_def_of("S7").get("roles") or [""])[0]`. With `stages.json` unreadable, the right call is refused with "for S7
  qa-failure-analyst name `--cases` ...". The direction is safe (refused), but the door is wrong for that package defect. Rare, so a note
  only.

### N4 — note: `controller-blocks.md` row text
- The generated row's message cell reads `(ValueError, check_delivery.candidate_refusal(refused, known_refs, unr`: the generator quotes code
  where a message is built by a call. This is a generator limit, not FL4's.

### N5 — note: `story_step materialize` echo
- `story_step.py:1385-1388` prints `; plan rows ...` but nothing for `bug_candidates`. It is an operator echo, not a role reader. A twin
  line is optional.

## Keys

1. **Items 1–8 and edges.** Items 1–8 are implemented as stated. I traced each in the diff, and the rows re-run green (see trail).
   - No row: E4, E12, the two adversarial inputs of the spec (F5), and the brief head / `PACKET_DISPATCH_KEYS` (N1/F5).
   - Weak: E2 (a constant-membership pin), and item 4's "equals the controller's text" compares to a fresh call (F5).
   - E9/E13 are by construction (no open-filter; the text only), so no row is needed.
2. **AR-13.** Holds. Grep of `bug_candidates|candidate_refusal|_grounding_candidates` over `scripts/` (non-test) shows `_grounding_candidates`
   called only by `bug_candidates` and the pre-existing `grounding_records`. `bug_candidates` is called by the controller and
   `no_move_facts`. The brief reads the request field, not the reader (the spec's "the brief calls it" is satisfied through the field;
   nothing re-reads the register). Both judges refuse through `candidate_refusal`: `controller.py:3794` and `no_move.py:268`. There is no
   second copy of the text.
3. **E7 / FR-59 / AR-28.** Where an input is flagged unreadable, the behaviour is correct at both judges (rows (vii) and item 4; reader
   raise → `None` → "could not be read"). A partial read with a definite answer does exist: F4 (a) a table path that exists but is not
   readable as a file, (b) a register with text but no `## Register` table, and the vocabulary marks unreadable. All three still refuse
   (AR-28 holds), but the text says "not in this story" (FR-41 is broken).
4. **AR-22.** The report's reader list is right for the request field. A grep of `plan_rows`-style dispatch readers found no other packet
   reader; `_carry_plan_rows` is not needed (the binding carries it, and the relaunch row is green). But the list misses the `args.candidates`
   form carriers: `driver_conductor.py:332` and `references/conductor.md:94` (F1). Also, conductor-actions row 8 `run` is stale (F2).
5. **AR-19 twins.**
   - Parsing is alike (comma split, strip, drop blanks).
   - The refusal shape is alike (`ValueError` list at the controller; `ArgsRefused` text at `check_args`).
   - The dispatch packet carries `bug_candidates` beside `plan_rows` through the same four readers.
   - The driver road is alike (`seam_rework_step` → `Driver.rework` → `--candidates`).
   - Asymmetries: the conductor form text (F1), the role rule (N2), and the stricter nesting check on `candidates` only (deviation 1:
     acceptable, see key 8).
   - `ANSWER_REWORK_OWNERS` untouched is right. A candidate rework is the conductor's `rework_stage` road, not the question-answer road
     (`driver_machine.py:693`, `owed_item`, strategist/designer only).
6. **Refusals.**
   - FR-46: all new controller refusals are `ValueError` (the call's fault), which is correct.
   - FR-1/FR-2: the stage/role refusal names `--cases`/`--rows`, and "together" says "name one of them".
   - Rule R names the known refs (a usable door: pick one) or the unreadable input. "record the input, then ask again" is the spec's
     verbatim text and is vague about who records. FR-3/E13 means the person is not asked, so the receiver is the conductor, whose door is
     `add-finding`. That is a note on the spec text, not on the builder.
   - `check_args`: "candidates are for S7 only (S4 and later take cases, S1-S3 rows)" names the door.
   - F4's wrong claim is the only text defect.
7. **Census.** The move is true and was even overdue: `check_args` already joined `cases` against the approved scope
   (`set(cases) - set(scope)`) before FL4, and now joins `candidates` against the read list. Both are cross-references between data, with
   no role judgment, so `xref` is right. `xref`/`shape` have no ceiling (`judgment-census.json` `ratchet`). I re-ran
   `test_judgment_census.py`: 25/25. The shrink-only ratchets stay shrink-only. The one raised ratchet is `role-load.json` (F3), and it is
   named in the commit.
8. **Deviations.**
   - (1) The stricter non-string check for `candidates` only: acceptable and needed for E11 nesting. The message text change is the spec's
     own (§3b.5 check_args 1), and a case-insensitive grep finds no pin on the old text (positive control: the same grep finds the new text
     in `no_move.py:251` and the spec).
   - (2) `none` for an empty read list: acceptable and correct ("(not read)" would claim an unknown).
   - (3) Row placement: acceptable.
   - (4) Collected problems: acceptable (K1).
   - (5) `Driver.rework` faked: acceptable, since the CLI rows cover the process.
   - The report's "NOT COMMITTED / question 2" section is stale (the Lead committed). A fix round should refresh it.
9. **Duplication and code quality.** Duplication: N1. Code quality: clear, comments name E3/E4/E5; nothing else found. My greps: the K-n
   parenthetical, `CASES_IN_LIST` uses, `"cases"|"rows"` carriers. `build_rework_request` grows by about 20 lines (the builder flags
   ~190 lines, and the clone/size ratchet in forge-check is green on CI).
   - Class-wide completeness: other "ref against a list" checks (`_outside_approved` for cases, plan rows "not in the approved plan") each
     keep their own texts. That is fine, because they have no unreadable-input state that Rule R serves. Other rework doors: the gate-B
     exploratory bug road keeps `--cases` because it has a case (a non-goal, correct). The conductor carriers are F1.
   - **FR-33 live proof.** The report's line (the spec's) is incomplete. It should also prove:
     - the driver road: the conductor offers a `rework_stage` option with `args.candidates`, `check_args` passes it, and the seam calls
       `--candidates`;
     - the empty-scope S7 analyst rework is accepted by the S7 exit/accept and the driver's S7 loop (premise PL4-4);
     - a K-n variant needs a diff story (no fixture holds one, F15);
     - the no-oracle outcome: the analyst says why no bug is owed, and gate B is asked again (`rerun_after` S8);
     - the charter line or packet-line behaviour change of the analyst (F3).
   - I propose two `live-runs` rows, R-n and K-n, each covering the driver road. The Lead decides.

## Trail

- Read:
  - the spec §1 FL4 rows, §3b.1–§3b.6, §4 F-L4-B/C/D;
  - the full diff of `13c4a757` (all 21 files);
  - the builder report;
  - `check_delivery._grounding_candidates`, `planning_contract.read_grounding` (docstring and kinds), `contract.candidate_defects`,
    `candidate_marks`, `register_rows`;
  - `controller.build_rework_request` head (`:3730-3815`) and its tail (`:3955-3975`), `_carry_plan_rows` and the relaunch binding
    (`:8985-9001`);
  - `driver_conductor` `no_move_facts` (`:380-415`), its prompt template (`:322-336`), `record_seam_rework` (`:741-760`);
  - `story_step` `materialize` echo (`:1378-1395`) and `_no_change_note`;
  - `selftest.cmd_limits`;
  - `stages.json` S7 roles;
  - `references/conductor.md:94`.
- Greps (case-insensitive where content-negative):
  - `bug_candidates|candidate_refusal|_grounding_candidates` over `scripts/`;
  - dispatch readers of `plan_rows`;
  - `manual_case_ids|retry_words` registries;
  - `ARGS_KEYS|rework_args_list`;
  - `"cases": [` / `"cases"|"rows"` carriers;
  - the old "lists of ids" text (positive control found the new text).
- Re-runs, all on the tree:
  - `test_exploratory_answers.py` → `111/111 ok`;
  - `test_judgment_census.py` → `25/25 ok`;
  - `test_role_load.py` → `186/186 ok` (with the Lead's raise);
  - row functions called directly: `fl4_candidate_rework` → `42/42 ok`, `fl4_candidate_rows` → `7/7 ok` (match the report);
  - `selftest.py --limits` → `FAIL ... controller-api.md: 12133 bytes > 12000`;
  - `wc -c` of `controller-api.md` at `027a04ea` / `13c4a757` / `origin/main` = 11998 / 12133 / 11998.
- Probes in the scratchpad (copies of `cart-1`, no live artifact touched):
  - grounding.yaml as a directory → `['R-13'] []` plus "not in this story: K-1";
  - register heading misspelled → `[] []` plus "not in this story ... none";
  - E12 on `story_to_s8` plus S7 analyst plus R-13 → `rerun_after {'stages': ['S8'], ...}`, `person_words True`; without words, `None`.
- CI: `ci_read.py jobs 44034288063`: `checks / package-fast` failure, `package-full (1)/(2)` in progress, the others success or skipped.
  `ci_read.py log 133873479799`: the limits FAIL. `why` printed only "in_progress" (the run was not finished, and I did not wait). The run
  header shows head `75da0581`, but the branch ref on origin is `13c4a757`, and my local `--limits` reproduces the failure on `13c4a757`.

```json
{
  "verdict": "blocker",
  "blockers": [
    "B1: references/controller-api.md grows 11998 -> 12133 bytes, over the 12000 reference cap; selftest --limits FAIL, CI checks/package-fast red (run 44034288063)"
  ],
  "fixes": [
    "B1: trim controller-api.md to <= 12000 bytes (merge the --candidates sentence into the --rows one); witness selftest.py --limits",
    "F1: add candidates to the args form at driver_conductor.py:332 and references/conductor.md:94 (owns widening)",
    "F2: conductor-actions.json actions row 8 run gains | --candidates <refs>",
    "F3 (Lead decision): move the analyst instruction into the conditional packet line (_packet_lines / brief head), drop the charter line, restore the process ratchet 20261",
    "F4: _grounding_candidates reads an existing-but-unreadable table (kind missing, path exists) and a register with text but no Register table as unreadable, or queue it as a node",
    "F5: rows for E4, E12, R-1 unmarked and K-1 non-diff refused; item 4 compares to the controller's text_vii"
  ],
  "class_completeness": "Axis 5 twins rows/cases/candidates: judges, seam, Driver.rework, packet readers moved together; missed carriers of the args form driver_conductor.py:332 and conductor.md:94 (F1) and row 8 run (F2). The E7 class on the reader surface _grounding_candidates has two uncovered states (F4). ANSWER_REWORK_OWNERS correctly untouched. Other ref-against-list checks have no unreadable state: n/a.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-rules-debt-phase2-s9-fl-cards-spec.md sections 1, 3b.1-3b.6, 4",
      "git show 13c4a757 (21 files)",
      "docs/tasks/specs/reports/20261117-rules-debt-fl4-report.md",
      "check_delivery._grounding_candidates; planning_contract.read_grounding; contract.candidate_defects, candidate_marks, register_rows",
      "controller.build_rework_request 3730-3815, 3955-3975; _carry_plan_rows 8985-9001",
      "driver_conductor.py 322-336, 380-415, 741-760; references/conductor.md:94; story_step.py 1378-1395, 1850-1870; selftest.cmd_limits; stages.json S7"
    ],
    "reruns": [
      {"command": "python -B tests/test_exploratory_answers.py (tree)", "result": "111/111 ok"},
      {"command": "python -B tests/test_judgment_census.py (tree)", "result": "25/25 ok"},
      {"command": "python -B tests/test_role_load.py (tree)", "result": "186/186 ok"},
      {"command": "fl4_candidate_rework and fl4_candidate_rows called directly", "result": "42/42 ok; 7/7 ok"},
      {"command": "cd pkg; python -B scripts/selftest.py --limits", "result": "FAIL references/controller-api.md 12133 bytes > 12000"},
      {"command": "scratchpad probes of bug_candidates on cart-1 copies; E12 build_rework_request words_given", "result": "directory table and misspelled Register heading give not in this story; rerun_after stages S8"},
      {"command": "ci_read.py jobs/log 44034288063", "result": "checks/package-fast failure (limits)"}
    ]
  }
}
```

# FV1-22 — S7 loops on the acceptance of S6: spec (designer draft, fix round 1)

pile `live-run-fvf`, batch 1, node FV1-22 (P1). Finding: `plans/piles/live-run-fvf/findings/20261113-s7-petlya-dirizhera-na-prieme-s6.md`.
Critic-on-plan verdict: `docs/tasks/specs/reviews/20261113-fv1-22-plan-critic.md` (fit_with_fixes, 6 blockers, 13 fixes) - applied
below; the closing section "Fix round" maps every item to its place.
Status: DRAFT for Lead acceptance. F1 = (b) and F2 = (a) are the Lead's decisions (critic-confirmed). F3 is the OWNER's and stays
open: the nodes are written by its recommendation (a); §5 says exactly what changes under (b). F4: designer recommendation to the Lead.
Package text stays English (FR-30); this file is a forge doc.

Tree of facts: every `file:line` in this file is on `C:\QAFactory\forge-repo\.claude\worktrees\read-main\ai-packages\qa-factory`
(origin/main e4ba384) unless marked "arm" (the live run copy, below). Builders work in worktrees the Lead creates from origin/main:
`C:\QAFactory\forge-repo\.claude\worktrees\fv1-22-n1\` (N1) and `C:\QAFactory\forge-repo\.claude\worktrees\fv1-22-n2\` (N2).

---------------------------------------------------------------------------------------------------------------------------

## 0. Facts

### 0.1 Producer and reader of the three fields

| field | READER | PRODUCER on the analyst's road |
|---|---|---|
| the verdict word | `scripts/acceptance.py:1565-1566` (`stage_acceptance_from_form`: `header.verdict`), mapped by `handoffs/vocabulary.yaml:124`; also read by `driver_stage_plan.stage_verdict_known` `:681-689`, by `handoff_check.check` `:1460` (relax), by the brief lines `driver_stage_s7.py:136-137`, `driver_stage_s8s9.py:80-82`, and test-side by `tests/form_filler.fill_form` `:446` | the analyst's `header.verdict` of the automator form, whose vocabulary meaning is its OWN handoff (`vocabulary.yaml:25`) |
| `failure_class`, `quote` | `acceptance.py:1571-1576`; judged `acceptance.stage_acceptance_errors` `:1353-1357` | NONE. The section is only in `handoffs/s7-analyst-to-scribe.yaml:53-59`, a `secondary: true` contract (`index.yaml:65`, critic trail); `handoff.contract_of` skips secondary rows (`handoff.py:378-379`); the dispatch form is `s7-analyst-to-automator` (no `stage_acceptance`, no `required_when`: whole file read, `:1-136`) |
| reviewed `inputs_read` row | `stage_done.reviewed_author_dispatch` (refusal `stage_done.py:1028-1032`, critic trail) | prefill `story_step._author_argv` `:319-336` only when the contract text holds `handoff.AUTHOR_TOKEN` (`handoff.py:406`); the token is in `s7-analyst-to-scribe.yaml:35` and `s8-scribe-to-gate-b.yaml:38`, NOT in `s7-analyst-to-automator.yaml:64-69` |

The pins of the wrong contract (`test_stage_done.py`, `test_handoff_init_author.py`, `test_stage_acceptance_consumer.py`) are all in the
`quarantine` section of `scripts/tests/test-layers.json` (rows `:9922`, `:8403`, `:9896`; the section starts `:7126`). The KEEP test of
exactly this defect is `scripts/tests/test_field_producers.py` (keep `:1682`), registry `scripts/tests/fixtures/form-rounds.json:27-28`
(family `RR-accept`), with two `known_red` rows of node FV1-22 at `form-rounds.json:66-67`.

### 0.2 The loop on real data (arm `factory`, LR2-1; the refusal strings are byte-equal on e4ba384: `acceptance.py:1355,1357`)

Carrier: `C:\QAFactory\mybooks-stand\arm-factory\test-automation-framework\qa-factory\artifacts\LOCAL-1\`.

| ts (UTC) | arm carrier:line | boundary | refusal | conductor move |
|---|---|---|---|---|
| 22:51:50 | `state/conductor.jsonl:49` | `S7:S7-qa-failure-analyst-1` | stage_done exit 2: "a reject needs failure_class ... (got None); ... a reject needs a quote", form `S7-qa-failure-analyst-1.yaml` | continue: rework refused, "the dispatch is running" |
| 22:53:38 | `conductor.jsonl:50` | `S7` | same, same form (analyst-1) | `controller.py rework --stage S7 --role qa-failure-analyst --cases TC-005 --cause tooling` -> analyst-2 |
| 23:15:24 | `conductor.jsonl:51` | `S7` | same, form analyst-2 | rework -> analyst-3 |
| 23:45:43 | `conductor.jsonl:52` | `S7` | same, form analyst-3 | rework -> analyst-4 |
| 23:57:18 | `conductor.jsonl:53` | `S7` | new text (`state/driver-question-details.md:6`: the reviewed runner dispatch is not named) | `unusable: the conductor cap was reached` -> person |

The analyst's intent (arm `work/handoffs/S7-qa-failure-analyst-1.yaml:69-70,76`): it named the runner row and wrote
`header.verdict: concerns` while accepting the run and handing a TEST_BUG repair to the automator. Cost: 4 paid conductor calls
($0.6613, the sum of `total_cost_usd` of arm rows 49-52, critic re-run) and 3 analyst sessions; TC-005 was never repaired.

### 0.3 Why it repeated (and why N2 as first drafted did nothing)

1. The refusal named fields the role's contract cannot hold (FR-11): a rework of the same role builds the same form.
2. The conductor prompt never carries its own previous move at this stage; each call is fresh.
3. The conductor ran `controller.py rework --cause tooling` directly (arm row 50 `did`); the no-cap rule for that cause is the
   controller's.
4. The survivor for this class is `Driver.window_round_gate` (`driver_machine.py:319-414`), but it returns at `:337-338` for every stage
   outside `WINDOW_ROUND_STAGES = {"S5": "qa-code-critic"}` (`driver_dispatch.py:109`).
5. B1 (critic): even with S7 listed it returns. `stage_acceptance_write` (`driver_stage_plan.py:641-651`) calls
   `self.py(..., check=True, expect=...)`; `DriverRunner.py` raises `gate_refusal(...)` (`driver_runner.py:234`), whose text is ONE line
   (`driver_core.py:78-79`) and which carries no `findings` and no `dispatch` (`Refusal.__init__` `driver_core.py:159,165-166`). So
   `source` is `[]` (`driver_machine.py:341-342`) and `if not key or not found: return` (`:344-345`) passes it to `conductor_round` (`:575`).
6. The only bound that fired was the per-boundary conductor cap (in memory, keyed by the boundary string).

### 0.4 Why F1 exists (unchanged reasoning)

Building `failure_class` from `repairs[].verdict: TEST_BUG` would reject the RUNNER for the automator's defect (P27, AR-29). The word that
decides accept/reject is `header.verdict`, whose vocabulary meaning is the analyst's own handoff; the real analyst used it that way. -> F1 (b).

---------------------------------------------------------------------------------------------------------------------------

## 1. Package spec header (designer rule 1, CLAUDE.md rule 10)

AR-n / FR-n touched and the change check each demands (written into the node DoDs):
- FR-11 (root rule): a contract may not demand a field the role's tool cannot produce - N1 (producer: the dispatch-time template;
  B2: the field is not demanded when nothing awaits). Check: RR-accept rows green with `known_red :66-67` deleted (N1 DoD).
- AR-10: the S6 acceptance fields stand in the form the analyst fills, before the work. Check: same rows.
- AR-22: producer (template + prefill) and reader change in ONE commit (N1). Check: same rows.
- AR-13: the acceptance word is read through ONE path reader `handoff.acceptance_verdict_path` by ALL its readers: `acceptance.acceptance_word`
  (record), `stage_verdict_known`, `handoff_check.check` (relax), the two brief lines, `form_filler.fill_form` (test side). Check: N1 grep
  in the DoD (no `get("header")`-style read of the word outside the reader in the owned functions) + rows N1-c.
- FR-37: the path named in the brief text is the path code reads (both brief lines built from `acceptance_verdict_path`). Check: N1-g.
- AR-19: the S8 scribe form is the twin consumer (F2 = a); the loop stop covers every stage (F3 = a). Check: N1-c S8 rows; N2-f.
- AR-23: the conditional section declares its empty outcome: absent from the skeleton when nothing awaits (B2), relaxed under `accept`.
  Check: N1-h, N1-c.
- AR-25 / FR-40 / FR-57: every token of N2's question has an executor; `go on` at a consumer stage is the existing person pass (B6).
  Check: N2-g, N2-h.
- AR-28: an unknown never becomes a pass: empty / old / unreadable word -> no record -> the seam; empty finding set never "equal".
  Check: N1-c (empty), N1-f, N2-c.
- AR-15 / AR-17: one survivor (`window_round_gate`), one seam (`no_move(... call=False)`). Check: N2 rows.
- AR-11 / AR-8: `acceptance_verdict_at` joins `handoff.CONTRACT_OWNED` (B5): never a role field, never on a key page. Check: N1-i +
  `contract_slices.py --check`.
- AR-20: the `known_red` ledger shrinks by two rows (N1); a role-load raise from the S8 template comment, if any, is named in the merge
  verdict (F2). Check: `test_field_producers.py` / `test_role_load.py` as printed by `--witness-for`.
- AR-29 / P27: no code check judges meaning; accept/return stays the analyst's (and the scribe's) word. AR-1: the switches are data
  (`acceptance_verdict_at`, `CONSUMER_ROUTES`), never a role or stage name in code.

Checks added or altered (owner / census class; `scripts/tests/fixtures/judgment-census.json` - the builder adds a row for any NEW raising unit
in the same commit; none is planned):

| check | where | owner | class |
|---|---|---|---|
| `stage_acceptance` owed under the acceptance word `return` (form finish) | `handoff_check.check` via `handoff.relaxed_sections` (keyed by `acceptance_verdict_path`) | data | shape |
| the acceptance word is a choice of the field (`accept|return`) | `handoff_check.check` choice check `:1584-1586` (unchanged) | data | shape |
| the section and token row exist only when a dispatch awaits | `handoff_init.drop_unowed_acceptance` (NEW, skeleton shaping, raises nothing: not a check) | data | - |
| a reject carries class + quote | `acceptance.stage_acceptance_errors` (unchanged) | data | shape |
| the same refusal set a second time goes to the person (every stage, F3 = a) | `driver_machine.window_round_gate` (altered) | data (identity of a set) - the person keeps the judgment | shape |
| the accept/return MEANING | the analyst (S6) / the scribe (S7), each accepted by the tier above at the next stage | judgment | - |

---------------------------------------------------------------------------------------------------------------------------

## 2. Design

D1 (N1). `s7-analyst-to-automator` carries the S6 acceptance: the reviewed-row token as `inputs_read[0]`, a `stage_acceptance` section with
its OWN word `verdict: <accept|return>` plus `failure_class`, `quote`, `witness_paths`, the contract key `acceptance_verdict_at:
stage_acceptance.verdict` (contract-owned) and `required_when: {return: [stage_acceptance]}` (whole section). One path reader
`handoff.acceptance_verdict_path` (default `header.verdict`: S2-S4 unchanged). When the dispatch awaits nothing (re-triage, later S7 lives,
unreadable state), the skeleton carries neither the token row nor the section (B2). `s8-scribe-to-gate-b` gets the same shape (F2 = a).

D2 (N2, merged with the first draft's N3 under F3 = a). The same-set stop of `window_round_gate` covers the `refusal` cause on EVERY stage;
the `window` cause stays S5's. `stage_acceptance_write` gives its refusal the dispatch whose form was refused, the refusal text as its one
finding (B1), and, at a stage the driver's `CONSUMER_ROUTES` table names, the person's pass line (B6). Round 1 -> conductor; the same set
again (dispatch ids masked) -> the person, no paid call; a different set within `WINDOW_ROUND_CAP` (2) -> conductor; beyond -> person.
On the data of 0.2: one conductor call (22:51); 22:53 is the person's free question; analysts 2-4 never run.

---------------------------------------------------------------------------------------------------------------------------

## 3. Nodes

Common to every node:
- given: this spec; `ai-packages/qa-factory/design/factory-rules.md` WHOLE; `plans/builder-rules.md`; `docs/TESTING.md`;
  `ai-packages/qa-factory/design/architecture.md` (rows of §1); the files of the node's owns, read in the node's own worktree.
- non-goals (all nodes): no charter edit (`agents/*.md`; FV1-24 owns S6/S7 charters; P27); no edit of `driver_conductor.py`, of
  `CONDUCTOR_CALLS_PER_BOUNDARY` or the conductor prompt; no new test file; no edit of a quarantined test file (builder-rules 7b); no local
  run of slow files (`test_story_run_*`, `test_controller_*`); no edit of `handoffs/s7-analyst-to-scribe.yaml` (it stays pinned by quarantine,
  §5 F4 note); the S5 window cause is not changed; no new node beyond N1/N2 (and N4 only if the Lead takes F4 = a).
- handoff: builder report per `.claude/agents/builder.md` rule 7 with the verbatim witness, FR pass over sections A-G.
- witness (rule 4 / builder-rules 7b): `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <the node's owns>` and the
  fast files it prints; a slow file it prints is named in the report for CI; "no scenario or keep row covers X" is a report line, never a
  reason for a new test file.

### N1 — the S7 (and S8) form carries the consumer acceptance; one reader of the word  [builder -> critic]

owns (absolute; functions named; worktree `fv1-22-n1`):
- `C:\QAFactory\forge-repo\.claude\worktrees\fv1-22-n1\ai-packages\qa-factory\handoffs\s7-analyst-to-automator.yaml`
- `C:\QAFactory\forge-repo\.claude\worktrees\fv1-22-n1\ai-packages\qa-factory\handoffs\s8-scribe-to-gate-b.yaml` (F2 = a)
- `C:\QAFactory\forge-repo\.claude\worktrees\fv1-22-n1\ai-packages\qa-factory\handoffs\vocabulary.yaml` (`stage_acceptance_verdicts` line `:124` only)
- `C:\QAFactory\forge-repo\.claude\worktrees\fv1-22-n1\ai-packages\qa-factory\scripts\handoff.py` (`CONTRACT_OWNED`; NEW `acceptance_verdict_path`)
- `C:\QAFactory\forge-repo\.claude\worktrees\fv1-22-n1\ai-packages\qa-factory\scripts\handoff_check.py` (`check`: line `:1460` only)
- `C:\QAFactory\forge-repo\.claude\worktrees\fv1-22-n1\ai-packages\qa-factory\scripts\handoff_init.py` (NEW `drop_unowed_acceptance`; `main`: one call line after `fill_head` `:478-481`)
- `C:\QAFactory\forge-repo\.claude\worktrees\fv1-22-n1\ai-packages\qa-factory\scripts\acceptance.py` (NEW `acceptance_word`; `stage_acceptance_from_form` `:1565-1566` + docstring)
- `C:\QAFactory\forge-repo\.claude\worktrees\fv1-22-n1\ai-packages\qa-factory\scripts\driver_stage_plan.py` (`stage_verdict_known` only)
- `C:\QAFactory\forge-repo\.claude\worktrees\fv1-22-n1\ai-packages\qa-factory\scripts\driver_stage_s6.py` (`consumer_settled` only)
- `C:\QAFactory\forge-repo\.claude\worktrees\fv1-22-n1\ai-packages\qa-factory\scripts\driver_stage_s7.py` (`stage_S7`: the brief line `:136-137` only)
- `C:\QAFactory\forge-repo\.claude\worktrees\fv1-22-n1\ai-packages\qa-factory\scripts\driver_stage_s8s9.py` (`stage_S8`: the brief lines `:80-82` only)
- `C:\QAFactory\forge-repo\.claude\worktrees\fv1-22-n1\ai-packages\qa-factory\references\slices\qa-failure-analyst\handoff-keys.md` and `...\references\slices\qa-doc-scribe\handoff-keys.md` (REGENERATED only: `python -B ai-packages/qa-factory/scripts/contract_slices.py --write`)
- `C:\QAFactory\forge-repo\.claude\worktrees\fv1-22-n1\ai-packages\qa-factory\scripts\tests\test_handoff.py` (function `a_section_owed_only_under_a_header_value_has_an_empty_outcome_otherwise` `:664-707` only: rows)
- `C:\QAFactory\forge-repo\.claude\worktrees\fv1-22-n1\ai-packages\qa-factory\scripts\tests\test_field_producers.py` (`_accept_form` `:1167-1173` only)
- `C:\QAFactory\forge-repo\.claude\worktrees\fv1-22-n1\ai-packages\qa-factory\scripts\tests\form_filler.py` (`fill_form`: the `dropped` line `:446` only)
- `C:\QAFactory\forge-repo\.claude\worktrees\fv1-22-n1\ai-packages\qa-factory\scripts\tests\fixtures\form-rounds.json` (delete `known_red` rows `:66-67` only)
- `C:\QAFactory\forge-repo\.claude\worktrees\fv1-22-n1\ai-packages\qa-factory\changelog.d\fv1-22-consumer-acceptance-form.md` (new fragment)

What to change:
1. `s7-analyst-to-automator.yaml`:
   a. `inputs_read:` gets as row 0 `- path: work/handoffs/<the author's dispatch>.yaml` / `version: <its window id>` (the literal
      `handoff.AUTHOR_TOKEN`), the two existing rows follow; the comment line above `inputs_read:` is the text of
      `s7-analyst-to-scribe.yaml:33` verbatim (`# Reviewed dispatch (as in your brief): ...`).
   b. Top-level key `acceptance_verdict_at: stage_acceptance.verdict` with a one-line comment: "where the acceptance word of the runner's
      handoff is read; `header.verdict` stays the verdict of THIS handoff".
   c. Section `stage_acceptance:` with `verdict: <accept|return>`, `failure_class: <spec|capability|data|tooling>`,
      `quote: "<the runner's own words, with path#anchor>"`, `witness_paths:` / `- <task-relative path the verdict rests on, or omit when none>`
      (the scribe-form wording, so the placeholder stays optional by `handoff.OPTIONAL_WORDS` `:35-36`), and a comment of at most four lines,
      experience not procedure: "Your word on the runner's handoff: `accept` when you can rely on the run - your repairs, bugs and doubts do
      not make it a return; `return` sends the run back to the runner for one repair round and owes the class and the runner's own words
      that show why. This section is absent when no runner's handoff awaits your word."
   d. `required_when:` / `  return: [stage_acceptance]` (WHOLE section; no dotted path - B4).
2. `vocabulary.yaml:124` `stage_acceptance_verdicts` gains `accept: accept, return: reject` (the five existing words unchanged).
3. `handoff.py`:
   a. `CONTRACT_OWNED` (`:452-454`) gains `"acceptance_verdict_at"` (B5).
   b. NEW `acceptance_verdict_path(contract_id) -> str`: the template's top-level `acceptance_verdict_at` when it is a string that, stripped,
      matches `^[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)+$`; else `"header.verdict"`. Never raises (`FileNotFoundError` and any other
      exception -> `"header.verdict"`; `contract_id` `""` or None -> `"header.verdict"`). Docstring: THE reader of where the acceptance word is.
4. `handoff_check.check` `:1460`: `relaxed = handoff.relaxed_sections(contract, doc.get(handoff.acceptance_verdict_path(contract)))`.
   `rows_owed` (`:1508-1509`) stays on `header.verdict`.
5. `acceptance.py`: NEW `acceptance_word(form) -> str`: walk the dotted path `handoff.acceptance_verdict_path(form.get("contract"))` over the
   PLAIN dict `form` (one key per dot; a non-dict step or a missing key -> `""`); the leaf must be a `str` (a list, a map, a number, None -> `""`);
   return it `.strip()`ped, case kept. `form` not a dict -> `""`. No `contract` key -> the path is `header.verdict` (one rule: today's
   behaviour for every critic form). `stage_acceptance_from_form` takes `word = acceptance_word(form)` instead of `:1565-1566`; its docstring
   says the word is read at the contract's `acceptance_verdict_at` (default `header.verdict`). Nothing else in it changes.
6. `driver_stage_plan.stage_verdict_known` (`:681-689`): `return bool(acceptance.stage_acceptance_verdict(acceptance.acceptance_word(data or {})))`;
   docstring updated; same `except`.
7. `driver_stage_s6.consumer_settled` (`:371-401`), recovery road (critic Q2, the sweep of the artifact): before `self.stage_acceptance_write(stage, mine)`
   (`:387`), `form_mine = f"work/handoffs/{mine}.yaml"`; `if not self.stage_verdict_known(form_mine): self.stage_review_exhausted(stage,
   route["author"], mine, None, form_mine, unreadable=True); return True`. (The guard its two siblings already have: `:357-358`, `:669-670`.)
8. `handoff_init.py`: NEW `drop_unowed_acceptance(text, contract, author_dispatch) -> str`, called in `main` right after `fill_head` (before
   the carry): when `author_dispatch` is empty AND `handoff.acceptance_verdict_path(contract) != "header.verdict"`, return the text without
   (i) the top-level section named by the path's head (`stage_acceptance`) with its comment block directly above it, and (ii) the
   `inputs_read` row whose `path` holds `handoff.AUTHOR_TOKEN` (both of its lines). Otherwise the text unchanged. Any exception -> the text
   unchanged (the role then meets the fields and the finish refuses them: the old trap, never an accept). It writes nothing else.
9. `s8-scribe-to-gate-b.yaml` (F2 = a): the same `acceptance_verdict_at: stage_acceptance.verdict`, `stage_acceptance.verdict: <accept|return>`
   as the section's first key, `required_when: {return: [stage_acceptance]}` replacing `:49-50`; the comment `:45-48` and `:58-59` replaced by
   the four-line experience comment of 1c with "the analyst's handoff" and "you can rely on the triage"; its token row `:38` stays.
   If `test_role_load.py` (when `--witness-for` prints it) reports a raise for the scribe, the report names it for the merge verdict (AR-20).
10. Brief lines, built from the reader (AR-13, FR-37): `stage_S7` `:136-137` -> `f"You also accept or return the runner's handoff ({awaiting}):
    your word on it is `{path}` of your form (`accept` or `return`), and `inputs_read` names the runner's form work/handoffs/{awaiting}.yaml."`
    with `path = handoff.acceptance_verdict_path(handoff.contract_of("S7", "qa-failure-analyst"))`; `stage_S8` `:80-82` -> the same sentence for
    "the analyst's handoff" with `contract_of("S8", "qa-doc-scribe")`, keeping "A concern about the report itself belongs in `unresolved`."
11. `tests/form_filler.fill_form` `:446`: the word that `relaxed_sections` gets is the ACCEPTANCE word: `path = handoff.acceptance_verdict_path(contract)`;
    `key_word = word_text if path == "header.verdict" else (overrides.get(path) if isinstance(overrides.get(path), str) else None)`; `dropped =
    set(handoff.relaxed_sections(contract, key_word)) & set(survey.tmpl.data) if key_word else set()`. Read `overrides` BEFORE line 452 consumes it.
12. `tests/test_field_producers._accept_form`: `path = handoff.acceptance_verdict_path(row["contract"])`; `header.verdict` path -> today's call
    (`verdict="concerns"`); any other path -> `verdict=None, overrides={path: "return"}`. The reject word is per path because the field's options
    differ (`header_verdicts` vs `accept|return`).
13. `fixtures/form-rounds.json`: delete the two rows `:66-67` (node FV1-22) in the same commit. Row ids (`:27` label `{contract}[concerns]...`) are
    NOT renamed (a rename would churn every RR-accept id; the label names the family, the feed names the word).
14. Regenerate both key pages; changelog fragment, one paragraph: the analyst's (and scribe's) acceptance word is its own field; nothing is asked
    when nothing awaits.

Edges (each with the invariant it protects):
- E1 present but empty/placeholder word on an awaiting dispatch: `_verdict_block` relaxes nothing on a placeholder (`handoff.py:564-566`), so the word
  and the class/quote are refused at finish as blanks; if a form reaches `stage_done` anyway, `acceptance_word` `""` -> no record -> `stage_verdict_known`
  False -> `stage_review_exhausted(unreadable=True)` on the live road (`driver_stage_s6.py:357-358`) and, with item 7, on the recovery road.
  INVARIANT: an empty word never becomes an accept.
- E2 `return` with empty class/quote: owed at finish (relax keyed on `return` owes the section); at record time `acceptance.py:1353-1357` still refuse.
  INVARIANT: a reject without class and quote is never recorded.
- E3 `accept` with a filled class: recorded `failure_class: None` (`acceptance.py:1575`). INVARIANT: an accept carries no class.
- E4 (B2, AR-23) a dispatch that awaits nothing (re-triage `s7_retriage_once` `driver_stage_s7.py:68`, a later S7 life, an unreadable state):
  `_author_argv` returns `[]` -> `drop_unowed_acceptance` removes the token row and the section -> nothing is owed and nothing is read
  (`consumer_completion` is wired only `if awaiting`, `driver_stage_s7.py:130-133`, `driver_stage_s8s9.py:76-79`). An awaiting dispatch whose state
  could not be read gets the same skeleton -> no word -> E1's seam (paid, one conductor call). INVARIANT: no form demands an acceptance nobody
  reads; an acceptance that IS read is never guessed (FR-59).
- E5 a quote citing no recorded evidence: presence only (F4).
- E6 triage verdicts (NO_DEFECT, APP_BUG, TEST_BUG ...) are independent of the acceptance word. INVARIANT: no triage verdict becomes an S6 reject by code.
- E7 TEMPORAL: the key is read from the TEMPLATE by the form's `contract`; a form written before this commit has no `stage_acceptance.verdict` ->
  `acceptance_word` `""` -> E1's seam (live road and, item 7, recovery road). Before the commit: today's behaviour. The move that creates the key:
  this commit. INVARIANT: an old form is never read as accept; a story in flight meets a door (the seam), not a dead end.
- E8 S2-S4 critic forms: no `acceptance_verdict_at` -> `header.verdict`; `drop_unowed_acceptance` does nothing for them. INVARIANT: no critic's accept
  or reject changes meaning (G2 rows stay green unchanged).
- E9 `header.verdict: concerns` + `stage_acceptance.verdict: accept` -> S6 accepted; the concerns travel in the analyst's own form.
  INVARIANT: the analyst's own verdict never decides S6.
- E10 the word's adversarial battery (outside input: an LLM-written form): `acept` and `Accept` -> refused at finish by the choice check
  (`handoff_check.py:1584-1586`, options `accept|return` from the placeholder); ` accept ` -> stripped, accepted; a list or map at the path ->
  `acceptance_word` `""` (E1); `concerns` at the new path -> choice refusal at finish (it would map to reject in the shared table only if it
  reached `stage_done`). INVARIANT: only `accept`/`return` written at the path decide; nothing else is read as either.
- E11 conflicting pair (resolved): the word lives inside the section it relaxes. Under `accept` the word is filled by definition, so relaxing the
  whole section relaxes only the blanks class/quote/witness; under a placeholder nothing is relaxed, so the word stays owed.

Reused function, new role (rule 1): `relaxed_sections` / `_verdict_block` keyed by a second field. Correct statement of its direction (critic Q4):
it relaxes every listed section for ANY real word other than the keyed one (`handoff.py:567-574`); a placeholder or empty word relaxes nothing. The
safety against an unknown word is NOT this function but the choice check (`handoff_check.py:1584-1586`). Adversarial inputs that must stay on the
owing/refusing side: malformed `acceptance_verdict_at` (not a string, empty, no dot, a path with spaces) -> `header.verdict`; a word outside the
options -> refused by the choice check (row N1-c `acept`).

Tests (rows in KEEP files only; ids name the input):
- RR-accept (`test_field_producers.py`, keep `:1682`): the two rows of `form-rounds.json:66-67` go GREEN and their ledger rows are deleted; the
  ratchet (`:199` "stale ... remove its known_red row") makes this the witness of the fix. The S8 rows (`s8-scribe-to-gate-b[...]`) stay green.
  If either S7 row is still red after the change, the builder does NOT keep its ledger row: it reports the red line verbatim and returns a question.
- N1-c: in `a_section_owed_only_under_a_header_value_has_an_empty_outcome_otherwise` (`test_handoff.py:664-707`), a second loop over
  `("s7-analyst-to-automator", "s8-scribe-to-gate-b")` writing the word at `stage_acceptance.verdict: <accept|return>`; ids
  `G3 <contract> accept` (no `stage_acceptance` problem), `G3 <contract> return` (class and quote owed), `G3 <contract> word missing` (the word itself
  owed: AR-28), `G3 <contract> acept` and `G3 <contract> Accept` (the path `stage_acceptance.verdict` is in the problems: choice refusal),
  `G3 <contract> header concerns + accept` (no `stage_acceptance` problem: E9). One pure row: `G3 acceptance_verdict_path` of
  `s7-analyst-to-automator` == `stage_acceptance.verdict`, of `s2-stage-critic-to-tester` == `header.verdict`, of `""` == `header.verdict`.
- N1-i (B5): one row in the same function: `handoff.owned_by_contract("acceptance_verdict_at")` is True.
- N1-h (B2): one row in the same function: `handoff_init.drop_unowed_acceptance(<template text>, "s7-analyst-to-automator", "")` parses with
  no `stage_acceptance` key and no `inputs_read` row holding `AUTHOR_TOKEN`; with `"S6-qa-runner-2"` the text is unchanged; for
  `s2-stage-critic-to-tester` with `""` the text is unchanged.
- N1-d/e/f (`acceptance_word` on a plain dict: nested path, list leaf -> `""`, no `contract` -> header word): covered through the RR-accept feed
  (it calls `stage_acceptance_from_form` on a filled form); no extra row file. N1-a/N1-b text pins of the first draft are DROPPED (critic Q7).
- N1-g (FR-37): no runtime row; the DoD grep below proves the brief lines read the reader.
DoD:
- `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/handoffs/s7-analyst-to-automator.yaml ai-packages/qa-factory/handoffs/s8-scribe-to-gate-b.yaml ai-packages/qa-factory/handoffs/vocabulary.yaml ai-packages/qa-factory/scripts/handoff.py ai-packages/qa-factory/scripts/handoff_check.py ai-packages/qa-factory/scripts/handoff_init.py ai-packages/qa-factory/scripts/acceptance.py ai-packages/qa-factory/scripts/driver_stage_plan.py ai-packages/qa-factory/scripts/driver_stage_s6.py ai-packages/qa-factory/scripts/driver_stage_s7.py ai-packages/qa-factory/scripts/driver_stage_s8s9.py ai-packages/qa-factory/scripts/tests/form_filler.py`
  and every fast file it prints, green - `test_field_producers.py` and `test_handoff.py` among them (if it does not print them, run both by name:
  `python -B ai-packages/qa-factory/scripts/tests/test_field_producers.py`, `python -B ai-packages/qa-factory/scripts/tests/test_handoff.py`);
  `python -B ai-packages/qa-factory/scripts/contract_slices.py --check` exit 0; `python -B ai-packages/qa-factory/scripts/selftest.py --lang` green.
- Grep (attach output): `git -C <worktree> grep -n "header.verdict" -- ai-packages/qa-factory/scripts/driver_stage_s7.py ai-packages/qa-factory/scripts/driver_stage_s8s9.py`
  shows no hit in the two brief lines; `git -C <worktree> grep -n "acceptance_verdict_path" -- ai-packages/qa-factory/scripts` shows the reader and its six callers.
- Acceptance key (DOC-DISPATCH form, full script attached, not committed): on a COPY of arm `S7-qa-failure-analyst-1.yaml` with
  `stage_acceptance: {verdict: accept}` added, `acceptance.stage_acceptance_from_form` returns verdict `accept`, `failure_class` None; negative
  control: the same copy without the field -> `(None, [<"not one of" problem>])`.
- Quarantine note in the report: `test_stage_acceptance_consumer.py:341-345` (quarantine) pins the old S8 `required_when: concerns` and comment; it
  will go red in `quarantine-watch`. Not edited (7b); the Lead tells the owner (CLAUDE.md rule 11, TEST QUARANTINE ALERT).
- architecture line: `AR-10, AR-11, AR-13, AR-19, AR-20, AR-22, AR-23, AR-25, AR-28 -- ...`; `judgment:` line names the analyst (S6) and the scribe
  (S7) as owners of accept/return.
siblings: S8 scribe form (in owns, F2 = a); S2-S4 critic forms (default path); `driver_stage_s6.CONSUMER_ROUTES` (`:146-156`, unchanged);
`driver_stage_plan.py:618` retypes `header.verdict` in an S2-S4 stage-critic brief (default path, text right today) - queued to the Lead as an
AR-13 sweep line, not owned here; the quarantined pins of 0.1.
designer: this file.

### N2 — the same refusal set a second time goes to the person, on every stage (F3 = a; first draft's N2 + N3)  [builder -> critic]

owns (absolute; functions named; worktree `fv1-22-n2`):
- `C:\QAFactory\forge-repo\.claude\worktrees\fv1-22-n2\ai-packages\qa-factory\scripts\driver_machine.py` (`window_round_gate` only)
- `C:\QAFactory\forge-repo\.claude\worktrees\fv1-22-n2\ai-packages\qa-factory\scripts\driver_core.py` (class `Refusal`: ONE new class attribute `person_pass = None` and its comment; nothing else)
- `C:\QAFactory\forge-repo\.claude\worktrees\fv1-22-n2\ai-packages\qa-factory\scripts\driver_stage_plan.py` (`stage_acceptance_write` only)
- `C:\QAFactory\forge-repo\.claude\worktrees\fv1-22-n2\ai-packages\qa-factory\scripts\driver_dispatch.py` (`finish`: the series-close condition line `:855` only)
- `C:\QAFactory\forge-repo\.claude\worktrees\fv1-22-n2\ai-packages\qa-factory\scripts\tests\test_probe_gap_door.py` (new test functions at the end of the file + `refusal_rig` only if a row needs it)
- `C:\QAFactory\forge-repo\.claude\worktrees\fv1-22-n2\ai-packages\qa-factory\changelog.d\fv1-22-same-refusal-every-stage.md` (new fragment)

What to change:
1. `Refusal` (`driver_core.py:114-119`, beside `chain`/`checks`): class attribute `person_pass = None` - "`{stage, line}` of the person's pass that
   closes what this refusal stops, set by the raiser that knows it (FR-16: a field, never a regex over the text); None everywhere else".
2. `stage_acceptance_write` (`driver_stage_plan.py:641-651`): wrap BOTH `self.py(...)` calls in `try/except Refusal as exc:`; set
   `exc.dispatch = exc.dispatch or dispatch` and `exc.findings = exc.findings or [exc.text]` (B1); on the `stage_done.py` call only, when
   `stage in getattr(self, "CONSUMER_ROUTES", {})`, also `exc.person_pass = {"stage": stage, "line": f"{acceptance.STAGE_ACCEPTANCE_PHRASE}:
   no accept record stands for {author}"}` with `author = acceptance.stage_author_dispatch(self.controller_state(), acceptance.stage_def_of(stage))`
   (skip when `author` is ""); re-raise the SAME object (`raise`). Never parse stage_done's problems out of the text (FR-12).
3. `window_round_gate` (`driver_machine.py:319-414`):
   a. The early return `:337-338` becomes `if stage not in WINDOW_ROUND_STAGES and refusal.window_findings: return` - i.e. the `refusal` cause
      is gated on every stage; the `window` cause (window_findings exist only at S5, `driver_dispatch.py:786-814`) keeps S5's table.
   b. Lead for `cause == "refusal"` outside `WINDOW_ROUND_STAGES`: the S5 strings (`:370-371`, `:378-379`) stay byte-equal for S5; another stage
      gets "The factory's own checks refused this step again with the same reasons as round {same}; asking the same role again brings the same
      refusal. Tell me how to go on.\n\n" (same_set) and "The factory's own checks refused this step {len(mine)} times, and the driver does not
      hand it on again.\n\n" (cap). Human-questions form (FR-6); the builder's critic checks the wording.
   c. After `state = {...}` (`:384-386`) and before the S5 branch: `extra = getattr(refusal, "person_pass", None)`; when it is a dict whose
      `stage` matches `^S\d+$` and whose `line` is a non-empty string: `state["stage"] = extra["stage"]`, `state["block"] = extra["line"]`,
      `state["lines"] = [extra["line"]] + [l for l in state["lines"] if l != extra["line"]]`, and the lead ends with "`go on` passes the
      acceptance on your word (recorded as a finding)." Nothing else of the method changes (key, series, cap, S5 branch).
4. `finish` `:855`: `if complete is True and (WINDOW_ROUND_STAGES.get(stage) == role or stage not in WINDOW_ROUND_STAGES):` - the accepted
   completion that closes a stage outside the table closes the series of its own key (`close_window_series`, `:944-951`, unchanged). The S5
   branch inside (`:860-861`) stays S5-only.
Behaviour: `handle_refusal` (`:416-576`) untouched: `second_delivery`, known rows, resumes, `code_close`, then `window_round_gate`, then
`conductor_round`. Blast radius (changelog and report say it): every refusal that today reaches `conductor_round` through `handle_refusal` and
carries a dispatch (its own, or the boundary's) - S1-S9, the automator's S7 repair dispatches included - now stops at the second identical set
and after two different sets per key; `gate_repair`'s `hand_to_conductor` (`:328-329` docstring) never meets it.

Edges (each with the invariant):
- POSITIONAL: the stop stays AFTER every known row of `handle_refusal` and after `code_close` (`:567-573`), BEFORE `conductor_round` (`:575`) and its
  per-boundary cap. INVARIANT: a set that differs from every earlier round of its key and is within the cap ALWAYS reaches the conductor; the
  acceptance itself stays refused (no record is written by the stop).
- B1 the single-line gate refusal: before this node its finding set was `[]` -> never gated. Now `[exc.text]`; `finding_lines` masks dispatch ids
  (`driver_core.py:55-64`). The text holds `out[-600:]` (`driver_core.py:79`): an output longer than 600 characters whose ids differ in LENGTH
  shifts the cut and makes the sets "different" -> the conductor is called. INVARIANT (error direction of the reused identity, advice -> gate):
  it may err only toward "different"; adversarial inputs that must stay different: the same text naming another field (`inputs_read` vs
  `failure_class`), another stage, another count.
- Empty finding set (a refusal with no text at all): never recorded, never equal (`:344-345`). INVARIANT: an unknown is not a repeat.
- Key "" (no dispatch on the refusal and none on the boundary: S0, gates, bare `S7` without `exc.dispatch`): passes to the conductor (`:344-345`).
  INVARIANT: no stop without an identity; the conductor cap bounds it.
- B6 the person's way out, per token at the stop (`take_seam_answer` `:2335-2386`, `seam_chosen` `:2388-2435`):
  - consumer stage (S6, S7: `person_pass` set): the Person's stage is the ACCEPTED stage and `block` the pass line; `go on` -> `pass_block`
    (`driver_dialog.py:631-641`) writes `waiver.py --stage <S6> --block "stage acceptance: no accept record stands for <author>"`, checked against
    the standing record the seam wrote at that stage with that line (`driver_conductor.py:566-589`, `waiver.py:674-729` kind `carrier`); next
    turn `consumer_word_step` (`driver_stage_s6.py:200-213`) -> `consumer_person_pass` (`:227-260`, line `:241`, the same text) records the
    driver accept `by: person` and files the finding. `retry` -> nothing passed, the step runs again (the same set asks again, free). `stop` -> held.
  - any other stage (`person_pass` None, e.g. an S2 critic form or an automator repair refusal): no `block`; `go on` goes to the conductor with
    the person's choice (`why=chosen`, one paid call, the existing executor) ; `retry`, `stop` as above.
  INVARIANT: every token has an executor; no answer loops the person with no exit (AR-25, FR-9, FR-57).
- A person's answer clears nothing: the same set afterwards asks again (docstring `:331-332`).
- Series close: outside the table, an accepted `complete is True` finish closes its own key. Under a consumer the analyst's finish is mostly
  `OpenWork` (`driver_stage_s6.py:158-166`): its series may stay open into a later life, where the same set asks at once. INVARIANT: no paid
  repeat on a known set; accepted cost, said in the changelog.
- TEMPORAL: `driver-state` written before this node holds no key outside S5 -> the first refusal is round 1. The move that creates the keys: the
  first gated refusal after the upgrade.
- `stage_acceptance_write` also serves S2-S4 critics: `dispatch`/`findings` set there now feed the stop (F3 = a); `person_pass` is not set
  (not a `CONSUMER_ROUTES` stage). INVARIANT: the dispatch is never read out of the refusal text.
Tests (new functions in `test_probe_gap_door.py`, keep `:3780`; driver pieces on a stub `self`, as `refusal_rig` `:272-294`):
- `test_fv122_acceptance_refusal_through_the_real_raise` (N2-a): stub with `py` raising `driver_core.gate_refusal("stage_done.py", 2, <the 0.2 text>,
  "<expect>")`, `task_root` without the form file, `controller_state` holding `S6-qa-runner-2` accepted, `CONSUMER_ROUTES = SR.Driver.CONSUMER_ROUTES`;
  `SR.Driver.stage_acceptance_write(stub, "S6", "S7-qa-failure-analyst-1")` raises a Refusal with `dispatch == "S7-qa-failure-analyst-1"`,
  `findings == [text]`, `person_pass == {"stage": "S6", "line": "stage acceptance: no accept record stands for S6-qa-runner-2"}`; that refusal fed
  twice to `window_round_gate(stub2, exc, "S7")`: the first returns (one `to_conductor` record), the second reaches `no_move` with `call False`,
  `stage "S6"`, `block` = the line, `lines[0]` = the line.
- `test_fv122_two_different_sets_reach_the_conductor_then_the_person` (N2-b): sets A, B on one S7 key -> both return (AT the cap 2); a third set C
  -> `no_move` (BEYOND).
- `test_fv122_no_identity_passes` (N2-c): bare `S7` boundary, refusal without dispatch -> returns, nothing recorded.
- `test_fv122_another_field_named_is_another_set` (N2-d): two texts differing only in `failure_class` vs `inputs_read` -> both return.
- `test_fv122_arm_rows_50_51_are_one_set` (N2-e): the `refusal` fields of arm `state/conductor.jsonl` rows 50 and 51 pasted as two literals
  (English text; check no Cyrillic) -> `SR.finding_lines([t50]) == SR.finding_lines([t51])`.
- `test_fv122_stage_outside_the_table_is_gated` (N2-f): an S2 refusal with dispatch, twice -> the second reaches `no_move`; its lead is the
  neutral one; the S5 tests above it stay green unchanged.
- `test_fv122_go_on_at_a_consumer_stage_records_the_pass` (N2-g, B6): the file's `Rig` with `choose("go_on_as_is", "go on", block=<line>)` at stage
  `S6` -> `passes` holds `("S6", <line>, ...)`.
- `test_fv122_go_on_without_a_pass_goes_to_the_conductor` (N2-h): the same with `block=""` -> no pass, one conductor move (today's `older` row
  pattern, `:257-259`).
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/driver_machine.py ai-packages/qa-factory/scripts/driver_core.py ai-packages/qa-factory/scripts/driver_stage_plan.py ai-packages/qa-factory/scripts/driver_dispatch.py`
- run the fast files it prints (not the slow list of 7b) plus `python -m pytest ai-packages/qa-factory/scripts/tests/test_probe_gap_door.py -q`;
slow ones named for CI. Acceptance keys: N2-a and N2-g green. A no-keep-row note for the `finish` line (`:855`) is a report line; the critic
reads the one-line condition. architecture line `AR-15, AR-17, AR-19, AR-25, AR-28 -- ...`; census: no new raising unit.
siblings: the conductor cap (unchanged); `stage_review_exhausted` (FV1-6) uses the bare-phrase pass at the accepted stage - the same door shape;
FV1-6's `seam_chosen` is the executor N2-g pins (semantic dependency, §4).
designer: this file.

### N4 — the quote cites recorded evidence (only if the Lead takes F4 = a; after N1)  [builder -> critic]

owns: `handoff_check.py` (the consumer/critic form check: `stage_acceptance.quote` must start with a task-relative path whose file exists under
the task root, before `#`); `test_handoff.py` rows (absolute path, `..`, URL, no `#`, existing path, missing path). Owner data, class xref;
refused at the role's OWN finish, never at record time. A sketch: the Lead orders its full spec after N1 merges.

---------------------------------------------------------------------------------------------------------------------------

## 4. Parallelism and crossings

- N1 ∥ N2: may run in parallel. Shared file `driver_stage_plan.py` with disjoint functions (N1 `stage_verdict_known`; N2 `stage_acceptance_write`;
  FV1-6 `stage_review_exhausted`) - D-0048, not a hot file. N1 touches no `driver_machine`, `driver_core`, `driver_dispatch`; N2 touches no
  handoff, acceptance, `driver_stage_s6/s7/s8s9` or form-filler file. The later merge takes main into its tree.
- N2 vs CL4-1 N1 (`docs/tasks/specs/20261113-cl4-1-collect-stalled-looped-spec.md:151-152`, owns `driver_machine.window_round_gate` and
  `test_probe_gap_door.py` `refusal_rig`, its C19): a SHARED function -> SEQUENTIAL. Recommended order: FV1-22 N2 first (P1 live loop), CL4-1 N1
  after it (its builder merges main; its stub gains `journal_run` over a gate that now covers every stage). The Lead writes `очередь: FV1-22/N2
  -> CL4-1/N1` in both batch rows.
- FV1-6 (`20261113-fv1-6-s2-door-back-to-tester-spec.md:142-147`: `driver_machine.take_seam_answer`, `seam_chosen`, `seam_rework_step`;
  `driver_conductor.no_move_facts`, `unread`; `driver_stage_plan.stage_review_exhausted`; `no_move.FINISHING_WHYS`): no shared function with N1/N2.
  Semantic dependencies: N1 E1/E4/E7 route an unreadable word to `stage_review_exhausted`, the seam FV1-6 rewrites (its fix is the door that
  refused the conductor's rework at arm row 49); N2-g pins `seam_chosen`'s `go on` with a block. The later node merges main and keeps both green.
- FV1-3 (`20261113-fv1-3-free-answer-to-conductor-spec.md:160-167`: `driver_dispatch.take_question_answer`, NEW `register_words_to_conductor`;
  `driver_machine._unread_halt_or_review`, one line of `take_answer`; `question_stop.BLOCKING_NOTE`; and `:252-256`, an estimated later node:
  `question_register.raise_for_case`, `_raise`, `gate_brief` card lines): no shared function. `finish` is not FV1-3's; the first draft's
  `queue: FV1-3 -> N3` is dropped.
- FV1-24 (S6/S7 charters): FV1-22 edits no charter; FV1-24 reads N1's form comment so the charter does not restate it (P27). FV1-20: no shared function.
- Live proof (FR-33): one `live-runs` row: an S7 where the analyst accepts the run and hands a TEST_BUG repair -> S6 recorded `accept`, the repair
  dispatched, no conductor call at S7.

---------------------------------------------------------------------------------------------------------------------------

## 5. Forks

F1 - where the S6 acceptance word lives: DECIDED (b) by the Lead, critic-confirmed. Not reopened.
F2 - the S8 twin: DECIDED (a) by the Lead, critic-confirmed. Not reopened.
F3 - the same-set stop beyond S5/S7: THE OWNER'S (process risk; (b) is a P31 exception). OPEN.
  (a) RECOMMENDED (one road, P31): every stage's unmatched refusal with a dispatch stops at the second identical set and after two different sets
      (N2 as written). Cost: fewer paid conductor calls; in exchange the person gets a free closed question earlier on S1-S4, S6, S8, S9 refusals the
      conductor might have untangled on a third try; blast radius unmeasured.
  (b) S5 + S7 only: an exclusion that needs the owner's word. What changes in N2 under (b): item 3a and 3b are dropped (the early return stays);
      `WINDOW_ROUND_STAGES` gains `"S7": "qa-failure-analyst"` (`driver_dispatch.py:109`, owned instead of the `finish` line); item 4 is dropped
      (`finish` unchanged, the table names the closing role); N2-f is dropped; items 1, 2, 3c and rows N2-a..e, g, h stay. The S8 consumer stop
      and S2-S4/S6 stay on the conductor road - one line with the owner's word and its carrier beside it in the batch file (not "tell the owner").
F4 - the quote cites recorded evidence: to the Lead. RECOMMENDED (a): N4 as its own node AFTER N1 - a data/xref check at the role's own finish
  on every acceptor form; reason: E5 leaves a P26-adjacent gap (an accept/return grounded on a quote nobody can open), and the check is shape
  (path exists), not judgment. Not a blocker of the loop. (b) no check: the quote stays trusted text -> that gap goes to the owner.
  Note: `s7-analyst-to-scribe.yaml` keeps its now-duplicate section while three quarantined tests pin it; removal waits for td-15 §D.3.

## 6. Small choices closed by the designer

- Words `accept|return` for the new field (no collision with `header_verdicts`).
- The contract key is read from the TEMPLATE by the form's `contract` name, never from the form; it is contract-owned (B5).
- B2: option (i) of the critic, realised as skeleton shaping only (`drop_unowed_acceptance`) - no new xref in `handoff_check`, so no census
  row: `check` judges only the nodes a form holds (`handoff_check.py:1540-1582` iterates `doc.nodes`), so a section the skeleton never wrote is
  never owed. The safe side on an awaiting dispatch whose state was unreadable is the seam (E4).
- B6: the pass line is the existing `consumer_person_pass` line (`driver_stage_s6.py:241`), at the accepted stage; it is set only where
  `CONSUMER_ROUTES` names the stage (a data row of the driver, AR-1), because only there a pre-`where` step reads the pass.
- N2 sets `dispatch` and `findings` on both refusals of `stage_acceptance_write` (both are about the form of `dispatch`); `person_pass` only on
  the `stage_done.py` one.
- Row ids of RR-accept keep `[concerns]` in the label (§3 N1 item 13).
- No change to `CONDUCTOR_CALLS_PER_BOUNDARY`; observation kept: the cap is in memory and keyed by the boundary string.

## 7. Analogs noticed (not widened)

- `driver_stage_plan.py:618`: an S2-S4 brief retypes `header.verdict` (default path, right today) - AR-13 sweep line for the Lead.
- `test_stage_acceptance_consumer.py:341-345` (quarantine) pins the S8 template text N1 changes: red in `quarantine-watch` after N1.
- The class "pin on a form nobody fills" (critic): a map-axis candidate "a test resolves the form through `handoff.contract_of`, never by naming it"
  - the Lead's proposal, not added here.
- S2-S4 critic forms keep the token row with no author when none is accepted (`brief_pack.reviewed_dispatch_lines` `:3621-3622` tells the role
  to leave it); `drop_unowed_acceptance` does not cover them (default path). Not observed in a run; noted only.

## 8. Reading trail

Read on read-main (e4ba384): the critic verdict (whole); this spec (whole); `scripts/driver_machine.py:140-590,2330-2460`; `driver_core.py:40-174,
640-679`; `driver_runner.py:200-244`; `driver_stage_plan.py:625-764`; `driver_stage_s6.py:140-419`; `driver_stage_s7.py:50-179`;
`driver_stage_s8s9.py:60-99`; `driver_dispatch.py:100-115,785-866`; `driver_conductor.py:352-416,420-601,602-801`; `driver_dialog.py:625-654`;
`waiver.py:200-229,620-729`; `acceptance.py:1275-1581`; `brief_pack.py:3595-3634`; `story_step.py:310-379`; `handoff.py:350-594` (+ grep
`is_placeholder|OPTIONAL_WORDS|sections|spec`); `handoff_check.py:1450-1609`; `handoff_init.py:105-502`; handoffs `s7-analyst-to-automator.yaml`
(whole), `s8-scribe-to-gate-b.yaml` (whole), `s7-analyst-to-scribe.yaml` (whole), `vocabulary.yaml` (grep `:23-27,124`); tests
`test_handoff.py:655-714`, `test_field_producers.py:1140-1290` (+ grep `known_red|_accept_form`), `form_filler.py:420-509` (+ grep `verdict`),
`fixtures/form-rounds.json` (whole), `test_probe_gap_door.py:1-32,255-357` (+ grep), `test_stage_acceptance_consumer.py:325-354`;
`test-layers.json` (grep of the files and of `"quarantine"`: section `:7126`); `no_move.py` (grep `TOKEN_MOVES|fallback_options`).
Forge docs: FV1-6 spec owns `:142-147`; FV1-3 spec owns `:160-167,252-256`; CL4-1 spec (grep `window_round_gate`, owns `:151-152`, table `:437`).
Searches with controls:
- `grep -n "AUTHOR_TOKEN|author.dispatch|relaxed_sections|rows_owed\(|def check"` in `handoff_check.py` -> `:1453,1460,1509` (no AUTHOR_TOKEN reader
  there; positive control same call: `relaxed_sections` hit).
- `grep "stage acceptance" -i` over `references/` -> no match; positive control, same tool and path: `grep "quarantine|block-names"` -> 6 files. So
  `block-names.json` has no stage-acceptance row and the pass goes the `carrier` road (`waiver.py:726-729`).
- `grep required_when` over `scripts/*.py` -> readers only `handoff.py:454,538,543`, `handoff_check.py:1459` (comment) and the tests
  `test_handoff.py:666`, `test_stage_acceptance_consumer.py:343` (positive: the known `handoff.py` reader is found).
- `grep "def stage_S7|def stage_S8|def s7_retriage_once"` -> `driver_stage_s7.py:48,342`, `driver_stage_s8s9.py:44`.
Not re-read (taken from the critic's trail, marked where used): `index.yaml:63,65`; `stage_done.py:1028-1054`; arm rows and costs;
`judgment-census.json` rows; `references/role-load.json` slack (the builder's `test_role_load.py` run decides).
Needed beyond the manifest: the arm copy (`C:\QAFactory\mybooks-stand\arm-factory\...`) for N2-e's literals.

---------------------------------------------------------------------------------------------------------------------------

## Fix round (critic-on-plan verdict, 13.11.2026)

Verdict: `docs/tasks/specs/reviews/20261113-fv1-22-plan-critic.md`. Every file:line re-taken on read-main e4ba384 (§0 table refreshed; no f52faed
line is left).

Blockers:
- B1 (N2 no-op on a one-line gate refusal) -> §3 N2 item 2 (`findings = [exc.text]` + `dispatch`), §0.3 (5), edge "B1"; N2-a goes through the real
  raise path (`gate_refusal` from a stubbed `py` into `stage_acceptance_write`).
- B2 (unfillable field on a non-accepting analyst) -> DECIDED by the designer (technical, FR-11/FR-5/AR-23): critic option (i), realised as skeleton
  shaping - §3 N1 item 8 (`handoff_init.drop_unowed_acceptance`), edge E4, row N1-h, §6 (why no `handoff_check` xref and no census row).
- B3 (keep test would go red) -> §3 N1 items 11-13, owns (`test_field_producers._accept_form`, `form_filler.fill_form` `:446`, `form-rounds.json:66-67`),
  Tests "RR-accept"; N1-a/N1-b text pins dropped. Found while applying it: `form_filler.fill_form` drops sections by `header.verdict` (`:446`), so
  without item 11 the S7 section would be dropped and the override could not land.
- B4 (dotted relax unworkable) -> §3 N1 item 1d `required_when: {return: [stage_acceptance]}` whole section; the "if" deleted; edge E11; the
  reused-function paragraph restated with the choice check (`handoff_check.py:1584-1586`) as the carrier.
- B5 (`CONTRACT_OWNED`) -> §3 N1 item 3a, owns `handoff.py`, row N1-i.
- B6 (the person's way out) -> DECIDED by the designer (technical, AR-25/FR-9/FR-57, P22): the critic's recommendation, with the stage made the
  ACCEPTED stage (the waiver reader `consumer_person_pass` reads only that stage) - §3 N2 items 1, 2, 3c; edge "B6" naming each token's executor;
  rows N2-g, N2-h; §6. Consequence: N2 edits `window_round_gate` -> sequential with CL4-1 N1 (§4).

Fixes (critic amendments 1-13):
1. -> B1 above.  2. -> B2 above.  3. -> B3 above.  4. -> B4 above.  5. -> B5 above.  6. -> B6 above.
7. items 3/4 contradiction -> one rule: no contract -> `header.verdict` (§3 N1 items 3b, 5); dotted getter over the plain dict named (item 5); case kept,
   whitespace stripped, `Accept` refused at finish (E10).
8. S8 brief line -> owns `driver_stage_s8s9.stage_S8` `:80-82`; both brief lines read `acceptance_verdict_path` (§3 N1 item 10; DoD grep).
9. `consumer_settled` guard -> §3 N1 item 7, owns `driver_stage_s6.consumer_settled`, E1/E7.
10. tests -> N1-c in the G2 function `test_handoff.py:664-707` (accept / return / missing / `acept` / `Accept` per contract); N2-b AT and BEYOND the cap,
    N2-d field-name adversarial row, N2-e uses arm rows 50/51.
11. §1 gains AR-25, AR-11, AR-20, FR-11, FR-37; the blast radius (every unmatched refusal with a dispatch, the automator's S7 repairs included) is in
    §3 N2 "Behaviour"; S8 is now covered by N2 under F3 = a (and named as uncovered under (b), §5).
12. §4: `queue: FV1-3 -> N3` dropped; FV1-3 owns corrected; FV1-6 named as the node that rewrites the seam N1's E1/E4/E7 use; §0 refreshed.
13. F3 marked the owner's; under the recommendation N2 and N3 are MERGED (§3 N2); §5 F3 says exactly what changes under (b).
Also from the verdict body: the role-load carrier is `references/role-load.json` and its keep test (not a quarantined comment) - §3 N1 item 9.

New nodes: none beyond what a blocker forces. N2 grew by the first draft's N3 (F3 = a: merged so no interim two-road state ships); its new owns
(`driver_core.Refusal` attribute, `finish` line `:855`) are forced by B6 and by the merge. N4 is unchanged and conditional on F4.

Forks returned: F3 (owner; recommendation (a), the (b) delta in §5); F4 (Lead; recommendation (a), reason in §5). F1, F2 closed by the Lead.

## Owner's word on F3 (13.11.2026, verbatim): F3 = (a), plus a duty

«для начала такого повтора быть не должно, но если возник, то да можно останавливать на любой стадии. Надо разобраться в причине
повтора и там тоже чинить»

F3 = (a): the same-set stop covers every stage. Added by the owner: a repeat is itself a defect — when one occurs, its CAUSE is
investigated and fixed where it arises (the stop is the net, not the cure). Carrier owed by the re-cut of this spec: the stop records
a finding that names the repeated set and the stage, so the cause has an owner; the known repeats of past runs get a recon of cause.

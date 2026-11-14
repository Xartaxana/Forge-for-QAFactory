# FV1-30b N4 and N5 — two dispatch-ready builder cards (DRAFT, designer, t-696)

Status: DRAFT for Lead acceptance. Addendum to `docs/tasks/specs/20261113-fv1-30b-word-fact-downstream-spec.md` (`P\`).
Lead decisions binding here (not returned as forks): F1 of `P\:673-675` = (a) — N4 is cut now; every other open fork of `P\`
goes by its own recommendation; the `known_red: FV1-30` labels of P1-b N4 are NOT in N4's owns (a `siblings:` line instead).
Forks opened by these two cards: §6 (each card is executable by its recommendation). Small choices closed: §7. Reading trail: §8.
Not established: §9.

**Base.** `B\` = `C:\QAFactory\forge-repo\.claude\worktrees\fv130b-n5\ai-packages\qa-factory\scripts\` — branch `wip/fv130b-n5`
at d5d602d (`.git\packed-refs:17`; `read-main` is detached at 50d9012, a `refs/worktree-sweep/wip/wave6` ref, `packed-refs:383`, so
it was not used). On this base N0, N1, N2, N3 and N6 of `P\` are already in: `window_record.word_let_go` `B\window_record.py:1217`,
the live index inside `build` `:1344-1366`, `word_let_go` callers in `controller.py`, `story_step.py`, `driver_dispatch.py` (Grep
count). Every line number below is for d5d602d and is a help; the builder locates by FUNCTION name and quoted text.
`T2\` = `C:\QAFactory\forge-repo\.claude\worktrees\tbw-t2\ai-packages\qa-factory\scripts\` (branch `wip/tbw-t2`, not merged).

## §0. What the reading changed against the brief

- **R1. Item 6 (1) of the amendment is already on the base.** The report tail prints the door by tag / whole id and the `*`
  clause with its two exceptions (`B\s5_precheck.py:4792-4800`), as `R30a\:30` asked. N4 carries 6 (2), 6 (3) unchanged, and 7.
- **R2. After FV1-30a, the cause `family` is reached ONLY by `open-oracle-asserted-*`.** `refusal_cause` returns `""` for
  `then-remainder-unrecorded-*` first (`:4000-4001`), then `family` for every non-passable finding (`:4002-4003`); `NOT_PASSABLE_TAGS`
  holds exactly the two tags (`:3964`). So N4 renames the cause of one tag; the `family` value stays in the table for any other
  producer or a future non-passable tag (edge N4-E1).
- **R3. `_gate_refusal` today calls an open-oracle finding "the author's repair" and nothing else.** A record with any truthy
  `refused` is class `refused` (`B\exit_gate.py:1809-1810`); `_gate_refusal` splits off only the WAITING records that carry NO
  `refused` (`B\story_step.py:2041-2043`) and prints for the rest "No recorded word passes these; they are the author's repair." or
  "... carry the source's `refused` tag: no recorded word passes them, `*` included; they are the author's repair." (`:2047-2050`).
  The finding's own fix line names two doors — bind the Then `expectation_unconfirmed` and let the person answer the registered
  question, or (no registered question) back to S4 (`B\s5_precheck.py:1654-1671`). The gate text is silent on the question.
- **R4. The parse defect sentence lists the causes by hand**: "gives no known cause (family or predating)"
  (`B\detector_verdict.py:170-171`), pinned at `B\tests\test_detector_verdict.py:111`. Adding a cause makes it false (sweep of the
  artifact, rule 9) — fork N4-F1.
- **R5. `test_detector_verdict.py` is owned WHOLE by tbw T2** (`docs/tasks/specs/20261114-told-before-work-t1r-t2-dispatch-spec.md:217`).
  On `T2\` the function `tag_cases` is untouched (still `T2\tests\test_detector_verdict.py:97-111`) and `REFUSAL_CAUSES` /
  `_tag_lines` are untouched (`T2\detector_verdict.py:68`, `:211-223`); T2 adds `refusal` `:148`, `spoken` `:178`, `told_cases`
  `:269`. So a function-level split exists (D-0048) — fork N4-F2.
- **R6. Four pins in `test_s5_precheck.py` read `family` for an open-oracle finding** (`:2168`, `:3039`, `:3061`, `:3074`) and turn red
  by design (TESTING.md «Когда тест покраснел» 1: rewritten in the same node). `test_s5_precheck.py` is a slow file (28.5 s,
  `B\slow_tests.json:112`; threshold `slow_over_s: 10`, `:5`) — judged by the batch canon.
- **R7. Fast keep files exist for every N4 behaviour**: `test_then_remainder.py` (keep, covers `s5_precheck.py`, `story_step.py`,
  `detector_verdict.py`, `exit_gate.py`; `test-layers.json:6450-6472`; holds the `_gate_refusal` table K20 `:801-834`),
  `test_exit_gate_scope.py` (keep, covers `exit_gate.py`, `detector_verdict.py`; `:1544-1559`; the cause table `:359-366`),
  `test_detector_verdict.py` (keep `:1250-1270`). None of the three is in `slow_tests.json` (Grep of the three names: no hit; positive
  control in the same call: `test_s5_precheck.py` `:112`, `test_window_record.py` `:152`, `test_words_doors.py` `:154`).
  `test_words_doors.py` (the amendment's file for the door row, `A\:390`) is 151.4 s — small choice §7.2.
- **R8. `_terminal_runs` has seven readers, not one.** `window_record.build` (`:1343`, and through it `blocked_instances`,
  `pending_instances`, `red_by_requirement`, `handed_instances`, `:1388-1421`), `acceptance.blocked_instances` (`:445`),
  `acceptance.handed_instances` (`:699`), `acceptance._red_source` (`:865`), `proof_level.staleness` (`:2003`), `stand_gaps` (`:403`),
  `story_step._ran_outcomes` (`:2965`). N5 changes what all of them see (fork N5-F1; §5.3 lists each reader's error direction).
- **R9. `instance_id_aliases` takes a manifest ENTRY, not an id** (`B\contract.py:4074-4105`): canonical, `<case>::<bare>` per link,
  bare, and the legacy hash only when it was computed from the instance's own identity (`legacy_identity_is_the_case`,
  `:4051-4071`). `_terminal_runs(task_root)` has no manifest today (`B\window_record.py:462-484`), so N5 must read one.
- **R10. Two readers already resolve aliases against the map, each its own way**: `proof_level.staleness` walks `_row_ids(entry)`
  over `runs` (`B\proof_level.py:2018`, first alias with a run), `acceptance._red_source.failed(names)` the same (`B\acceptance.py:876-881`);
  the precheck takes the FIRST alias (canonical first) that has any row (`B\s5_precheck.py:1954-1955`). After N5 the map itself is
  alias-complete, so these first-hit loops all land on the same tuple (the latest of any spelling). They are not changed (siblings).
- **R11. `test_window_record.py` is 87.4 s** (`slow_tests.json:152`) — over the one-minute line of PROJECT.md p. 2 — fork N5-F2.

## §1. Scope, AR-n touched, owners and census of every check

**Goal.** N4: an `open-oracle-asserted-*` finding is refused at the source with its own cause `awaits_answer`, the gate's reader
reads that cause, and the gate's refusal names the expectation question as the way out (never a word, never only "the author's
repair"). N5: the window record and the six other readers of "the latest terminal run of an instance" find a run spelled under any
`contract.instance_id_aliases` spelling of that instance — the precheck's road (`B\s5_precheck.py:1950-1955`) — so "no run row" means
one thing at the precheck and at the window (P31).

**AR-n touched and the change check each demands (copied into the DoD of the node that touches it):**

| AR | node | why touched | change check (DoD line) |
|---|---|---|---|
| AR-9 | N4 | the gate's refusal names a door per class; a new class gets its door | the K20 rows (§4.4 g1-g6): the `awaits_answer` line names the question and the author's binding, never a word door |
| AR-18 | N4 | one output shape, one reader: a new cause value in `WORDS_REFUSED_AT_SOURCE` | `test_detector_verdict.py` `tag_cases` row: the cause is read; an unknown cause is still `unreadable` + one defect |
| AR-22 | N4 | a new produced value (`awaits_answer`) gets its reader in the SAME commit | producer (`refusal_cause`) and readers (`REFUSAL_CAUSES`, `_gate_refusal`) in one commit; no other reader of the value exists (Grep -i `predating` over the package: only `detector_verdict.py`, `s5_precheck.py`, tests, CHANGELOG; `WORDS_REFUSED_AT_SOURCE` readers: only `detector_verdict.py`) |
| AR-28 | N4 | an open expectation must never become a pass | `test_exit_gate_scope.py` cause table gains `awaits_answer`: `*` and a named word pass nothing |
| AR-13 | N5 | "the latest terminal run of an instance" has one reader; its identity join becomes the contract's one alias reader | `_terminal_runs` calls `C.instance_id_aliases` only; no `startswith`, no `function_name`, no `split("::")` in it (Grep on the diff, pasted) |
| AR-15 | N5 | one survivor wired everywhere: all seven readers get aliases by the one change | no reader of the map is edited (diff touches `_terminal_runs` only) |
| AR-28 | N5 | an unknown (unreadable manifest, ambiguous alias) never credits a run | rows w5, w6, w7 (§5.4) |
| AR-29 | both | every changed function judges data | census rows: none added, none changed (below); `test_judgment_census.py` judged by CI |
| AR-1 | N4 | the tag → cause choice is a constant in code | not a new list: `OPEN_ORACLE_ASSERTED` already exists (`B\s5_precheck.py:92`) and `NOT_PASSABLE_TAGS` is the existing code tuple (`:3964`); N4 adds one branch on the existing constant, no new tuple (stated so the critic does not read it as a new closed list) |

**Checks added or altered — owner served and census class (AR-29, P27):**

| # | check | node | owner it serves | census class |
|---|---|---|---|---|
| K1 | `s5_precheck.refusal_cause`: `open-oracle-asserted-*` → `awaits_answer` (was `family`) | N4 | intent — the owner's word that only the answer settles it (`A\:304`, `:383-390`, exception 2), carried by data (a tag) | not a check: it labels a refusal `_passable` already makes (`_passable` unchanged); not in the census (Grep `"function": "refusal_cause"` in `judgment-census.json`: no hit; control `check_run_mapping` hits `:995`) |
| K2 | `detector_verdict.REFUSAL_CAUSES` += `awaits_answer` (read by `_tag_lines`, `_refused_of`, `_link`) | N4 | data | not a check (the vocabulary of a shape reader) |
| K3 | `story_step._gate_refusal`: records with `refused == awaits_answer` get their own door line | N4 | data (text of an existing refusal) | not a check (text) |
| K4 | `window_record._terminal_runs`: a terminal row is keyed under every alias of the ONE manifest entry its id resolves to | N5 | data (identity join) | not a census row today (Grep `"function": "_terminal_runs"`: no hit, same control); if a census tool lists it after the change, class `xref`, owner `data` |

No check reads a role's or a person's wording (FR-12): every join is by tag prefix, a cause value or an instance id spelling.

---

## §2. FR walk the builders inherit (sections touched)

A (refusals and doors): N4 — FR-1, FR-2, FR-57 (the door of the new line is usable by the role or names who acts); N5 — no refusal text
changes (FR-1 n/a). B (text a person reads): N4's texts are read by the conductor and the author role, not put to a person as a
question; `human-questions.md` applies only to the question itself, which N4 does not write (B: "the question text is not changed").
C: FR-14 — the `refused` value set is a contract (N4 changes it with its reader); FR-42 — the new state has a move. D: FR-58 — an open
expectation stays refused (N4); FR-16 — an identifier resolved through the tool that produces it (N5: `instance_id_aliases`). E, F:
untouched. G: FR-30 English, FR-32 root cause with a test.

---

## §3. Card N4 — `awaits_answer`: the cause, its reader, its door (items 6 (2-3) and 7 of `A\:383-392`)

given: this file whole; `P\` §0, §6 N4 line of §8 F1 (`:673-675`); `C:\QAFactory\forge-repo\docs\tasks\specs\20261113-p1-specs-amendment-owner-words.md` lines 299-310 and 374-419; `C:\QAFactory\forge-repo\docs\tasks\specs\reviews\20261113-fv130a-code-critic.md`; `ai-packages/qa-factory/design/factory-rules.md` whole; `plans/builder-rules.md`; `docs/TESTING.md`; `ai-packages/qa-factory/references/human-questions.md`; code: `scripts/s5_precheck.py` (`OPEN_ORACLE_ASSERTED` :88-92, `_open_oracle_door` :1654-1671, `NOT_PASSABLE_TAGS` :3961-3964, `_passable` :3967-3970, `refusal_cause` :3991-4004, `report` :4744-4805), `scripts/detector_verdict.py` (:65-69, `_tag_lines` :158-172, `_refused_of` :252-254, `_link` :263-281), `scripts/exit_gate.py` (`word_class` :1798-1817, `judge_words` :1820-1859), `scripts/story_step.py` (`_gate_refusal` :2009-2055); tests `scripts/tests/test_detector_verdict.py` (`tag_cases` :97-126), `scripts/tests/test_exit_gate_scope.py` (:359-366), `scripts/tests/test_then_remainder.py` (`k20_the_gate_refusal_names_the_remainder_door` :801-834, `main` :1161), `scripts/tests/test_s5_precheck.py` (`no_word_passes_the_open_oracle_gate` :2152-2170, `the_verdict_is_one_line_per_finding` :3013-3095)
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\s5_precheck.py (refusal_cause; report — the one footer clause of item 3 only; the comment above NOT_PASSABLE_TAGS)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\detector_verdict.py (REFUSAL_CAUSES; _tag_lines — the defect sentence only, under fork N4-F1 (a))
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\story_step.py (_gate_refusal)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_detector_verdict.py (tag_cases only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_exit_gate_scope.py (the cause table at the `tagged = {...}` loop only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_then_remainder.py (k20_the_gate_refusal_names_the_remainder_door; new table function k22_open_oracle_awaits_its_answer; main — one call line)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_s5_precheck.py (no_word_passes_the_open_oracle_gate; the_verdict_is_one_line_per_finding — the four `family` pins of R6 only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\fv1-30b-n4-awaits-answer.md
non-goals: `exit_gate.word_class` and `judge_words` (read the new value unchanged — `A\:388`); `_passable`, `_names`, `NOT_PASSABLE_TAGS`, `NEVER_JUDGED_TAGS`; `_open_oracle_door` and the finding's message/fix text; the REPAIR_MARKER sentence of `report` (`story_run.match_known` routes on it); `detector_verdict` `Record`, `refusal`, `spoken` (tbw T2); `s5_precheck.report` beyond the one clause (tbw T5 later); the quarantined `test_row_fields.py` and `test_story_step_gate.py` (builder-rules 7b: a quarantine file is not run, not edited); the `known_red: FV1-30` labels of P1-b N4 (they do not exist yet; see `siblings:`); `test_words_doors.py` (§7.2); any new question form
handoff: the branch commit + `docs/tasks/specs/reports/20261114-fv1-30b-n4-report.md` (FR walk §2, the narrow witness output verbatim, the R6 grep, the AR-13/AR-22 greps with their positive controls)
edges: N4-E1 … N4-E9 (§3.3), each with its invariant
DoD: rows §3.4 green; `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/s5_precheck.py ai-packages/qa-factory/scripts/detector_verdict.py ai-packages/qa-factory/scripts/story_step.py` — run every printed file that is NOT over 10 s in `scripts/slow_tests.json`, at least `python -B ai-packages/qa-factory/scripts/tests/test_then_remainder.py`, `python -B ai-packages/qa-factory/scripts/tests/test_exit_gate_scope.py`, `python -B ai-packages/qa-factory/scripts/tests/test_detector_verdict.py`; `test_s5_precheck.py` (28.5 s), `test_words_doors.py`, `test_story_step.py` and every other slow printed file: judged by the batch canon (named in the report, not run); `architecture: AR-1, AR-9, AR-18, AR-22, AR-28, AR-29 -- <how kept, one clause each from §1>`; `judgment: refusal_cause labels an existing refusal with the owner's own cause -- no judgment moves into code, the answer stays the person's and the question register's`
siblings: P1-b N4 must NOT plant `known_red: FV1-30` on the C4г rows of groups `gates`/`s5` for families 1 `manifest`, 2 `bindings`, 3 `oracle` (except `open-oracle-asserted-*`), 4 `run_mapping`, 6 `plan`, 7 `sides` (`A\:302-308`, `:407`) — after FV1-30a+30b those rows are expected PASS; the exception-2 row (`open-oracle-asserted-<n>`) stays the NOTE "owner idea node OI-assumptions" (`A\:310`), never `known_red: FV1-30`; family 5 `smell` stays `n/a: no blocking producer` (`A\:306`); the row ids themselves are P1-b N4's to write (`<key|route|joint|kind>/<variant>`, `docs/tasks/specs/20261113-p1b-dry-story-spec.md:242`); `exit_gate.WAITING_FINDING_TAGS` (`B\exit_gate.py:1787`) — not a sibling to change: an open-oracle finding carries a `refused` cause, it does not WAIT unrefused; `test_row_fields.py:366-374` (quarantine) — fork N4-F4; SIBLING_MAP axes 17, 26, 34 walked in the report (axis line per axis, rule 10)
designer: C:\QAFactory\forge-repo\docs\tasks\specs\20261114-fv1-30b-n4-n5-cards-spec.md

### 3.1 What to change (numbered)

1. **`s5_precheck.refusal_cause`** becomes, in this order (positional invariant N4-E5):
   ```
   tag = _finding_tag(finding).lower()
   if tag.startswith(THEN_REMAINDER_WAITS): return ""          # unchanged, first
   if tag.startswith(OPEN_ORACLE_ASSERTED): return DV.AWAITS_ANSWER   # NEW
   if not _passable(finding): return "family"                  # unchanged
   return "predating" if finding.get("refused") == "predating" else ""   # unchanged
   ```
   `DV.AWAITS_ANSWER = "awaits_answer"` is a module constant in `detector_verdict.py` (item 2), imported, never retyped (AR-13).
   Docstring: drop "`family` (not passable)" as the only non-time cause; say `awaits_answer` (an `open-oracle-asserted-*` finding:
   only the answer to its expectation question settles it, no word, `*` included), `family` (any other finding no word may pass),
   `predating`; keep the GW1-14 paragraph. The comment above `NOT_PASSABLE_TAGS` (`:3961-3963`) gets one clause: "its refusal
   line carries the cause `awaits_answer` (`refusal_cause`)".
   (Note: the existing `THEN_REMAINDER_WAITS` test reads `_finding_tag(finding)` without `.lower()` (`:4000`); lowering it is the
   refusing-side change — an upper-case spelling of that tag today falls to `_passable`, which lowers, and returns `family`; after
   this item it returns `""` like the lower-case one. State it in the report; row k22-7.)
2. **`detector_verdict`**: `AWAITS_ANSWER = "awaits_answer"`; `REFUSAL_CAUSES = ("family", "predating", AWAITS_ANSWER)`. The
   module docstring line that lists the causes (`:23`, "`family` / `predating`") and `parse`'s docstring (`:324`, "`family`,
   `predating` or `unreadable`") name the third value. Under N4-F1 (a): `_tag_lines`' defect sentence is built from the tuple —
   `f"the line '{line}' gives no known cause ({' or '.join(REFUSAL_CAUSES)}): the source refusal cannot be read"` (the rest of the
   sentence unchanged).
3. **`s5_precheck.report` — one clause, item 6 (2).** After the existing star clause (`:4796-4800`) and before the `then handed`
   clause (`:4801-4804`), append, only when `any(refusal_cause(f) == DV.AWAITS_ANSWER for f in findings)`:
   `" A finding whose refusal line above says `awaits_answer` (`open-oracle-asserted-*`) waits for the answer to its expectation question: no recorded word passes it, `*` included; its own line names the author's repair and the question the person settles by answering it."`
   Nothing else in `report` changes (the REPAIR_MARKER sentence, the header, the refusal-line loop `:4776-4779` — it already prints
   whatever `refusal_cause` returns). Item 6 (3) (the `then handed` clause) is unchanged.
4. **`story_step._gate_refusal` — the door by class (`A\:389-390`).** After `waiting`/`refused` are split (`:2041-2043`), split
   `refused` once more: `awaiting = [r for r in refused if getattr(r, "refused", "") == DV.AWAITS_ANSWER]`, `refused = [r for r in
   refused if r not in awaiting]` (`DV` = `detector_verdict`, already imported at module level — `:2054` uses it). Print, after the
   `waiting` line and before the `refused` line, when `awaiting`:
   `"  " + str(len(awaiting)) + " finding(s) wait for the answer to an expectation question (`awaits_answer`): no recorded word passes them, `*` included. Each line above names the question and the command with which the conductor records the person's answer; until it is answered, the author binds that Then `expectation_unconfirmed` as the line says, or returns the item in its digest when the line sends the case back to S4."`
   The `refused` sentence's condition becomes `not (named or starred or waiting or awaiting)` (so an `awaiting`-only refusal never
   says "No recorded word passes these; they are the author's repair."). The repair-marker line and the `checks:` machine line stay
   LAST, in that order (`:2051-2054`, POSITION INVARIANT there).
5. **Red pins rewritten (R6)**: `test_s5_precheck.py:2168` → cause `awaits_answer` (label "cause awaits_answer"); `:3039` →
   `["", "awaits_answer", "awaits_answer"]`; `:3061` → `... {f['id']} awaits_answer`; `:3074` → `(True, ["", "awaits_answer"])`;
   their labels say `awaits_answer` instead of "family". Before handoff the builder greps the keep tests for the old behaviour
   (`Grep -n "family" scripts/tests/test_*.py`, read each hit that concerns an `open-oracle` finding) and lists every hit with
   "rewritten / not about open-oracle"; a hit in a quarantine file is listed, not edited.
6. **Changelog fragment** (one English ASCII bullet): "The S5 exit check now refuses an asserted open expectation with its own cause
   `awaits_answer`, and the finish refusal names the expectation question as its way out."

### 3.2 Error direction of the reused function (designer rule 1; P20, FR-58)

`refusal_cause` already feeds a gate: its value becomes `Record.refused`, and `exit_gate.word_class` returns `refused` for ANY truthy
value (`:1809-1810`) — a record no word opens, `*` included. N4 changes only WHICH truthy value one tag gets. Allowed error: a finding
gets a refusal cause it did not need (a false refusal; the author or the person sees one more round). Forbidden error: a finding the
code refused today reads `""` after N4 (it would become class `star`, and `*` would pass an open expectation — the P20 defect).
Invariant: `bool(refusal_cause(f))` is identical before and after N4 for every finding EXCEPT the upper-case
`THEN-REMAINDER-UNRECORDED-*` spelling of item 1's note (`family` → `""`; that finding waits for the `then handed:` word and
`word_class` still reads it `refused` through `WAITING_FINDING_TAGS`, `:1813-1814`, when its tag field is lower-case — and the source
prints the tag as written; row k22-7 pins what happens). Adversarial inputs that must stay on the refusing side (rows k22-1…k22-8):
`open-oracle-asserted-1`; `OPEN-ORACLE-ASSERTED-2` (upper case); `open-oracle-asserted` (no number); an open-oracle finding that ALSO
carries `refused: "predating"`; a word `*`, a word = the tag, a word = the whole id, a word `awaits_answer` (the cause as a word) at
the gate; a finding with no `id`; `xopen-oracle-asserted-1` (a prefix elsewhere — passable today, stays `""`).

### 3.3 Edges (each with its invariant)

| # | Edge | Behaviour | Invariant |
|---|---|---|---|
| N4-E1 | A refusal line with a cause the table does not know (`other`, a typo, a missing cause) | `_tag_lines` reads it `unreadable` + one defect, as today; the defect sentence names the three known causes | a cause the table does not know stays what it is today — never silently re-classed, never a pass |
| N4-E2 | A record whose `refused` is truthy but neither `awaits_answer` nor empty (`family`, `predating`, `unreadable`, a hand-set value like K20's `smell-1`) | `_gate_refusal` prints today's `refused` sentence for it | only the exact constant moves a record to the new line; everything else keeps today's text |
| N4-E3 | A story with no open-oracle finding | `report` output and `_gate_refusal` text byte-identical to today (rows k22-5, g5) | no finding of another family sees any change |
| N4-E4 | A mixed refusal: `awaits_answer` + a `named` + a `star` + a waiting Then + a `family` record | each class gets its own line, in today's order with the new line after `waiting`; counts add up to `len(blocking)`; the listing (`render_saved`) is unchanged | one packet does not contradict itself (FR-10): no line calls the open-oracle record "the author's repair" alone or offers it a word |
| N4-E5 | POSITIONAL — `refusal_cause` branch order | `then-remainder-unrecorded` first, `open-oracle-asserted` second, `_passable` third, `predating` last | a waiting Then never gets a refusal line; an open-oracle finding never reads `""` or `predating`; a passable finding never reads `awaits_answer` |
| N4-E6 | TEMPORAL — a story mid-S5 when N4 lands | the precheck runs fresh at every finish (no cause is stored: the only reader of `WORDS_REFUSED_AT_SOURCE` is `detector_verdict.parse`, R7 grep); the next refusal of that dispatch prints the new cause and the new door line; `state/findings/<D>-finish.txt` holds record TEXT, which is unchanged, so `finding_key` repeat counting carries on | the world before and after differs only in the cause word and the door line; a story never loses a finding or gains a pass across the boundary |
| N4-E7 | TEMPORAL — producer without reader | `refusal_cause` and `REFUSAL_CAUSES` land in ONE commit; a tree where only the producer changed would read `awaits_answer` as `unreadable` + defect (N4-E1) — never a pass | AR-22: a produced value has its reader in the same commit |
| N4-E8 | A person's stage word `awaits_answer` / `*` / the tag / the whole id at the gate | `judge_words` blocks the record (class `refused` first, `:1844-1846`) | `*` never passes an expectation awaiting its answer (A3-E2) |
| N4-E9 | The open-oracle finding of door B (no registered question: back to S4) | same cause `awaits_answer` (fork N4-F3); the new gate line covers it by "or returns the item in its digest when the line sends the case back to S4" | the door the line names is one the refused role can use (FR-2): the author can always bind or return the item; the answer is the conductor's to record |

### 3.4 Test rows (ids name the input; one parameterised test per behaviour)

`test_then_remainder.py`, new table function `k22_open_oracle_awaits_its_answer` (registered in `main`), over `P._finding(...)` dicts
and `P.report` captured stdout (the file's existing helpers):
- k22-1 `open-oracle-asserted-1` → `refusal_cause == "awaits_answer"`, `_passable` False.
- k22-2 `OPEN-ORACLE-ASSERTED-2` → `awaits_answer`.
- k22-3 `open-oracle-asserted` (no number) → `awaits_answer`.
- k22-4 open-oracle tag + `refused: "predating"` → `awaits_answer`.
- k22-5 `stand-login` (environment), `no-bindings`, `changed-after-red-a.py:12` with `refused: "predating"` → `""`, `""`, `predating`
  (today's values); `report` of a result holding only these → no `awaits_answer` text anywhere (N4-E3).
- k22-6 `report` of `[environment finding, open-oracle-asserted-1]` → the line `WORDS_REFUSED_AT_SOURCE: <id> awaits_answer` above
  the header, the item-3 clause present once, the star clause still present; `DV.parse(1, out, "")["refused"] == ["", "awaits_answer"]`
  and no defect.
- k22-7 `THEN-REMAINDER-UNRECORDED-1` (upper case) → `""` (the note of item 1).
- k22-8 `xopen-oracle-asserted-1` → `""`.
`test_then_remainder.py` `k20_the_gate_refusal_names_the_remainder_door`, rows added to its table:
- g1 one `Record(..., words="source", refused="awaits_answer")` alone → the text has "1 finding(s) wait for the answer to an
  expectation question (`awaits_answer`)" and "the conductor records the person's answer"; does NOT have "No recorded word passes
  these; they are the author's repair." nor any `--block` door.
- g2 that record + K20's `smell-1` record → both lines; the `smell-1` line keeps "1 finding(s) carry the source's `refused` tag".
- g3 that record + the waiting Then → the `then handed` line and the new line, in that order.
- g4 a record with `refused="family"` alone → today's sentence byte-identical (N4-E2).
- g5 the K20 inputs as they are → byte-identical to today (N4-E3).
- g6 the last two lines of g1's text are the repair-marker line and the `checks:` line (position invariant kept).
`test_exit_gate_scope.py`: the cause tuple of the `tagged` loop gains `"awaits_answer"` → `*` and the named word `x:t` pass nothing
(N4-E8).
`test_detector_verdict.py` `tag_cases`: (d1) a refusal line with cause `awaits_answer` → that finding's `refused` is
`awaits_answer`, no defect; (d2) the existing "unknown cause" rows stay, their defect check reads the new sentence (under N4-F1 (a):
`"gives no known cause (family or predating or awaits_answer)"`).
`test_s5_precheck.py`: item 5's four pins (canon).

---

## §4. Card N5 — `_terminal_runs` finds a run under any alias of its instance (residual M4, `P\:626-632`)

given: this file whole; `P\` D3 (`:51-62`) and N5 stub (`:626-632`); `ai-packages/qa-factory/design/factory-rules.md` whole; `plans/builder-rules.md`; `docs/TESTING.md`; code: `scripts/window_record.py` (`_load` :436-441, `_terminal_runs` :462-484, `build` :1307-1421), `scripts/contract.py` (`legacy_identity_is_the_case` :4051-4071, `instance_id_aliases` :4074-4105, `manifest_test_links` :4108), `scripts/s5_precheck.py` (`check_run_mapping` :1930-1960), `scripts/acceptance.py` (`blocked_instances` :410-524, `handed_instances` :665-734, `_red_source` :851-886), `scripts/proof_level.py` (`staleness` :1996-2021), `scripts/stand_gaps.py` (:395-419), `scripts/story_step.py` (`_ran_outcomes` :2960-2969), `scripts/run_history.py` (`read_run_blocks`); tests `scripts/tests/test_window_record.py` (`a_terminal_run_is_the_latest_by_the_clock` :1188-1224, helpers `run_block` :109, `test_row` :93)
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\window_record.py (_terminal_runs only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_window_record.py (a_terminal_run_is_the_latest_by_the_clock — rows added to it)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\fv1-30b-n5-run-aliases.md
non-goals: every reader of the map (`build`, `acceptance.*`, `proof_level.staleness`, `stand_gaps`, `story_step._ran_outcomes`) — not edited; `window_record.row_field_lines` (tbw T3b) and every other function of `window_record.py`; `contract.instance_id_aliases`, `legacy_identity_is_the_case`; `s5_precheck.check_run_mapping` and `_why_no_row` (the precheck's road is the model, not a target); `run_history.read_run_blocks` order; the quarantined `test_acceptance_semantics.py`
handoff: the branch commit + `docs/tasks/specs/reports/20261114-fv1-30b-n5-report.md` (FR walk §2, the witness output verbatim, the AR-13 diff grep, the reader table §4.3 re-confirmed by one line per reader)
edges: N5-E1 … N5-E9 (§4.2), each with its invariant
DoD: rows §4.4 in `a_terminal_run_is_the_latest_by_the_clock`; `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/window_record.py` — run every printed file NOT over 10 s in `scripts/slow_tests.json`; `test_window_record.py` (87.4 s) is judged by the batch canon under fork N5-F2 (a) (named in the report); `architecture: AR-13, AR-15, AR-28, AR-29 -- <how kept, one clause each from §1>`; `judgment: none -- an identity join of run rows to manifest entries through the contract's one alias reader; nothing about meaning is decided`
siblings: `s5_precheck.check_run_mapping` (`:1950-1955`, first alias with a row — after N5 the window and the precheck agree on "has a run"; precedence differs only when two spellings both carry rows: the precheck uses the canonical's series, the map the latest of both — stated, not changed, N5-E4); `proof_level.staleness` `:2018` and `acceptance._red_source.failed` `:876-881` (first alias found in the map — after N5 every alias key holds the same latest tuple, so no change is needed); `story_step._ran_outcomes` `:2966` (canonical key only — after N5 it sees alias-spelled runs too); `exit_gate`/`branch_accounting` no-row parsing (`P\` K9) — n/a here; SIBLING_MAP axes 17, 26, 34 walked in the report (one line per axis)
designer: C:\QAFactory\forge-repo\docs\tasks\specs\20261114-fv1-30b-n4-n5-cards-spec.md

### 4.1 What to change (numbered)

1. **Read the manifest once inside `_terminal_runs`** (signature unchanged — every caller stays as it is):
   `manifest = _load(Path(C.artifact(task_root, "automation-manifest.json")))` (the path `build` reads, `:1333-1334`), then build
   `owner: dict` = alias → the tuple of ALL aliases of the one entry it belongs to:
   ```
   try:
       cfg = C.case_config(task_root)
       spellings = {}                                    # alias -> set of entry keys (canonical id) naming it
       aliases_of = {}                                   # canonical id -> tuple(instance_id_aliases(entry, cfg))
       for entry in C.manifest_tests(manifest):
           names = tuple(C.instance_id_aliases(entry, cfg))
           if not names: continue
           aliases_of.setdefault(names[0], names)
           for name in names: spellings.setdefault(name, set()).add(names[0])
       owner = {name: aliases_of[next(iter(keys))] for name, keys in spellings.items() if len(keys) == 1}
   except Exception:
       owner = {}
   ```
   An alias claimed by two different entries (two canonical ids) is NOT in `owner` (ambiguous — N5-E5). Two manifest rows with the
   SAME canonical id are one entry (the first row's aliases are used, as `blocked_instances` does with `setdefault`, `:438-441`).
2. **Key each terminal row under every spelling of its instance.** In the existing loop (`:476-483`), after
   `found[identity] = value` (kept, unchanged), add: `for name in owner.get(identity, ()): found[name] = value`. The loop order is
   `run_history.read_run_blocks`' order and, inside a block, the `results` list order — so for every key the LAST terminal row of
   ANY spelling of that instance wins (N5-E3).
3. **Docstring**: "instance id -> (...)" becomes "every spelling of an instance (`contract.instance_id_aliases` of the ONE manifest
   entry the run row's id names) -> (the latest terminal result row of that instance under any spelling, its block, the block's
   path)"; add the ambiguity rule, the manifest-unreadable rule, and "a run of another instance (another parameter, a name that only
   shares a prefix) never counts: the join is equality of whole spellings".
4. **Changelog fragment** (one English ASCII bullet): "The window record finds an instance's run under any spelling of its id, the
   same spellings the S5 exit check accepts."

### 4.2 Edges (each with its invariant)

| # | Edge | Behaviour | Invariant |
|---|---|---|---|
| N5-E1 | A run row of `test_a[neg]`; manifest entries `test_a` and `test_a[pos]` | neither entry gets the run (no alias of theirs equals `test_a[neg]`); the raw key `test_a[neg]` stays as today | a run of ANOTHER instance (a parameter-label prefix, a shared function name) never counts as this instance's terminal run |
| N5-E2 | Manifest absent, unreadable, no `tests`, an entry with no id, `instance_id_aliases` returning `[]`, `case_config` raising | `owner == {}` → the map is byte-identical to today's (exact keys only) | an alias list that is empty/absent behaves as today; an unknown never credits a run (AR-28) |
| N5-E3 | Two terminal runs under two spellings of one instance (`TC-012::test_x` in block 1, `test_x` in block 2; and the reverse order) | every alias key and the raw keys hold block 2's tuple; with the reverse order, block 2's (= the `TC-012::test_x` row) | "latest" is read ONE way: `run_history.read_run_blocks` order (the block's own clock, a reparse right after the block it supersedes), then the order of `results` inside a block; a spelling never outranks a later run |
| N5-E4 | The precheck and the window when both spellings carry rows | precheck: "has a run" (first alias with rows, canonical first); window: the LATEST of both | both agree that the instance ran; the outcome the window cites is the latest run (the window's own rule, t-149) — stated, not unified (sibling line) |
| N5-E5 | One spelling claimed by two entries (two instances sharing a bare `test_x[eu]` under different cases; or a bare spelling equal to another entry's canonical id) | that spelling maps to nobody; its raw key is kept as today; each entry's own other spellings still map | an ambiguous spelling never credits a run to one instance on a guess (refusing side: the instance reads "no run" and its own refusal stands) |
| N5-E6 | A legacy hash computed from the case alone (`legacy_identity_is_the_case`) | not an alias (the contract drops it, `:4102`) → never joins two tests | two parameterized tests of one case never read as one instance |
| N5-E7 | A non-terminal row (`skipped`, `not_run`) under an alias | not counted, as today (`TERMINAL_RESULT_STATUSES`) | only a product outcome is a terminal run |
| N5-E8 | TEMPORAL — a story mid-S5 when N5 lands | the next `build` (at `finish` / `window_record.run`) gives an alias-spelled instance its outcome, fingerprint and run evidence; an already accepted window is history and is not rebuilt; a recorded `no-row-<iid>` word pass of that instance stops applying because its fact no longer stands (`P\` §2.3: a pass counts only while its fact stands; `word_let_go`'s no-run shape fails, E29) | both worlds are consistent with the precheck; a word never covers an instance that shows a run |
| N5-E9 | A reader that now sees a run it did not see (per reader, §4.3) | each moves to its documented allowed side or to the correct reading | no reader is moved toward its forbidden error |

### 4.3 Error direction of the reused map, per reader (designer rule 1)

`_terminal_runs` is already a gate input for seven readers (R8). N5 makes it see MORE runs (alias-spelled ones). Allowed error of the
map: miss a run (the instance reads "not run"). Forbidden error: credit a run of instance X to instance Y. What N5 adds can only be a
run of the SAME manifest entry (equality of whole spellings from one entry, ambiguity dropped), so it moves no reader to its forbidden
side; per reader:

| reader | what a newly found run changes | its documented allowed error | side after N5 |
|---|---|---|---|
| `build` window item | outcome/fingerprint/evidence present instead of the no-run branch | refuse (tier 2 "outcome is missing") | correct reading; the no-run refusal is no longer raised for a test that ran |
| `acceptance.blocked_instances` (iii) | a passed run on current bytes → not blocked (`REFUSED_STALE`) | "not blocked" (`:425`, `:447`) | allowed side |
| `acceptance.handed_instances` (3) | a run → not handed (`ran`) | "not handed" (`:660-663`) | allowed side; today's exact keys could err to the forbidden "handed" for an alias-spelled run — N5 removes that |
| `acceptance._red_source` (v-b) | a failed latest run → may be red with its row | "not red" (`:853-854`) | a red is credited only to the instance whose own run failed (same entry) — the forbidden attribution needs another instance's run, which N5 cannot add |
| `proof_level.staleness` | a run to judge freshness on instead of `unknown` | `unknown` | correct reading (it already walked aliases over a partial map) |
| `stand_gaps` `ran_red_of` | a red run mark may appear | "the person seeing less" (`:405`) | correct reading |
| `story_step._ran_outcomes` | the observed outcome replaces `handed` for a case | empty | correct reading (edge 12 there: a red result never becomes `handed`) |

Adversarial inputs that must stay on the refusing side: N5-E1 (parameter label, shared function), N5-E5 (shared bare spelling; bare
equal to another canonical), N5-E6 (case-only legacy hash), an `instance_id` of `""`/`None`/a number, a result row that is not a
dict, a manifest whose `tests` is not a list.

### 4.4 Test rows (in `a_terminal_run_is_the_latest_by_the_clock`, the file's `run_block` / `test_row` helpers)

- w1 manifest entry canonical `test_x` linked to `TC-012`; one terminal block row spelled `TC-012::test_x` → `_terminal_runs(root)`
  has `test_x` and `TC-012::test_x` with the same tuple; `build` gives the window item an `outcome` and an `execution_fingerprint`
  (the stub's row).
- w2 (N5-E3) block 1 `TC-012::test_x` `failed`, block 2 `test_x` `passed` (block clocks ordered) → both keys hold the `passed` row
  of block 2; the reverse clocks → both hold the block-2 `failed` row.
- w3 (N5-E1) run row `test_a[neg]`; entries `test_a` and `test_a[pos]` → neither `test_a` nor `test_a[pos]` is a key; `test_a[neg]`
  is (raw, as today).
- w4 (N5-E5) entries `TC-1::test_x[eu]` and `TC-2::test_x[eu]` (different canonicals sharing bare `test_x[eu]`); a run spelled
  `test_x[eu]` → keyed only under `test_x[eu]`; neither canonical is a key.
- w5 (N5-E2) the w1 run with NO manifest file / a manifest that is not JSON / `{"tests": "x"}` → the map has only `TC-012::test_x`
  (byte-identical keys to today).
- w6 (N5-E7) an alias-spelled `skipped` row → no key for it.
- w7 (N5-E2) `case_config` monkeypatched to raise → the map equals today's exact map.
- The existing F-order rows (`:1206-1224`, no manifest in that fixture) stay green unchanged.

---

## §5. Crossings (function level)

| other | its owns | overlap with N4 / N5 | resolution |
|---|---|---|---|
| tbw T2 (`wip/tbw-t2`, unmerged) | `detector_verdict.py` (`Record`, `refusal`, `spoken`); `test_detector_verdict.py` WHOLE | N4: `REFUSAL_CAUSES`, `AWAITS_ANSWER`, `_tag_lines` sentence; `tag_cases` | disjoint functions (R5); fork N4-F2 |
| tbw T5 (later) | `s5_precheck.report` | N4: one footer clause | `очередь: FV1-30b N4 → tbw T5` (the later node merges main and keeps the clause) |
| tbw T3b | `window_record.row_field_lines` | N5: `_terminal_runs` | none (different functions; `row_field_lines` is not on d5d602d) |
| FV1-30b N4 ∥ N5 | — | no shared file | parallel-safe |
| P1-b N4 | C4г exit rows (not yet written) | N4 `siblings:` line | the label rule in N4's `siblings:` |

## §6. Forks (returned, never decided; each card executes by the recommendation)

**N4-F1 — the hand-written cause list in the parse defect sentence (`B\detector_verdict.py:170-171`, pinned `test_detector_verdict.py:111`).**
(a) build the sentence from `REFUSAL_CAUSES` (N4 owns `_tag_lines`' sentence and the `tag_cases` pin) — the text stays true for any
later cause; cost: one more function in a file tbw T2 is editing (no function overlap, R5). (b) leave the sentence; it then names two
of three causes (a false text, FR-1; the class rule 9 forbids leaving a known sibling). (c) hand-write "family, predating or
awaits_answer" — fixes now, same drift next time. **Recommendation (a).** Card written for (a).

**N4-F2 — tbw T2 owns `test_detector_verdict.py` whole while unmerged.** (a) function-level split per D-0048: N4 owns `tag_cases`
only, T2 every other function; the later of the two merges main and resolves; one critic after the merge (PROJECT.md «Командная
работа» 3). (b) `очередь: tbw T2 → FV1-30b N4` — N4 waits for T2's merge (delays FV1-30 tonight if T2 is not merged). (c) move N4's
two `tag_cases` rows to `test_exit_gate_scope.py` (keep, covers `detector_verdict.py`) and leave `test_detector_verdict.py` untouched —
only possible under N4-F1 (b) or with the `:111` pin left red, so it breaks (a) of N4-F1. **Recommendation (a)** (the owner's
priority is tonight; R5 shows `tag_cases` untouched on `T2\`). The Lead narrows T2's `owns` line to "every function but `tag_cases`"
or records the split in both dispatches.

**N4-F3 — the cause of an open-oracle finding with NO registered question (door B, `B\s5_precheck.py:1668-1671`).** The finding
carries the same tag; its way out is the case going back to S4, not an answer. (a) the same cause `awaits_answer` (the amendment's
literal rule: "`refusal_cause` для `open-oracle-asserted-*` → `awaits_answer`", `A\:386-387`); the gate line names both roads
(card item 4). (b) a fourth cause for door B (e.g. `awaits_case`) — `refusal_cause` would need the door flag on the finding (a new
field, a producer change in `check_open_oracle_asserted`, a new reader row). **Recommendation (a)**: one cause per tag (data join by
tag only); the line already names the S4 road, and both stay refused.

**N4-F4 — item 7's second half: `test_row_fields.py:366-374` (quarantine).** `A\:391-392` says it goes "by TESTING.md:130-131"
(rewrite in the same node); builder-rules 7b and TESTING.md «Кто что делает» say a builder neither runs nor edits a quarantine file.
(a) not touched by N4; the pin is red in quarantine since FV1-30a (`R30a\:83`); it leaves by the quarantine rule (td-15 §D.3, owner's
word for deletion); the report names it. (b) the Lead or an integrator edits it by hand outside the builder rule. **Recommendation
(a)**; the card lists it under `non-goals:`/`siblings:`.

**N5-F1 — where the alias join lives.** (a) inside `_terminal_runs` for every reader (the card) — one road for "latest run of an
instance" (P31, AR-15), seven readers fixed by one change, all moved to their allowed or correct side (§4.3); cost: one manifest read
per call (the map is read once per `build`; the `acceptance` readers read it only when not handed `runs`). (b) an opt-in parameter
`_terminal_runs(task_root, manifest=None)` used only by `build` — the six other readers keep exact ids: two roads for one fact (P31
defect, and `build` hands its alias map to `blocked/handed/red` while their standalone calls use the exact map — one reader, two
answers). (c) alias lookup at each reader — seven edits, beyond N5's owns. **Recommendation (a).**

**N5-F2 — the narrow witness for a row in a slow file (`test_window_record.py`, 87.4 s, over PROJECT.md p. 2's one minute).**
(a) the rows go into `test_window_record.py` (the file `P\:629` names), the builder runs only the fast files `--witness-for` prints,
and the rows are judged by the batch canon; the report says so. (b) the builder runs `test_window_record.py` once (87 s) as the
node's own witness — a deviation from p. 2 that only the owner's word allows. (c) put the rows in a fast keep file that covers
`window_record.py` — the designer found none: the two keep files that cover it and name `_terminal_runs`'s readers are
`test_window_record.py` (slow) and `test_s5_precheck.py` (slow, 28.5 s); `test_acceptance_semantics.py` and
`test_mixed_then_outcomes.py` (which monkeypatch `_terminal_runs`) are quarantine / an import holder (`test-layers.json:7167`,
`:3068-3072`). **Recommendation (a)**, with the cost said plainly: N5's own rows are proved only by the CI canon; a canon failure
is a `defect_found` against N5.

### Lead decisions on the forks (14.11.2026, owner away — by recommendation, listed in the morning report)

N4-F1 (a). N4-F2 (a): function-level split, N4 owns `tag_cases` only; the later of N4 / tbw T2 merges main and resolves.
N4-F3 (a): one cause per tag. N4-F4 (a): the quarantined pin is not touched. N5-F1 (a): the join lives inside `_terminal_runs`.
N5-F2 (a): N5's rows are judged by the batch canon; the report says so. §7 choices 1-5 accepted.
critic on plan: skipped -- the parent spec (20261113-fv1-30b) and the amendment passed their plan critics; these cards change no
meaning beyond them (the `awaits_answer` cause is the amendment's own rule); the topic's code critic follows the build.
In a dispatch the cards' `owns` paths are re-rooted to the builder's worktree by the Lead.

## §7. Small technical choices closed by the designer

1. `AWAITS_ANSWER` lives in `detector_verdict.py` beside `REFUSAL_CAUSES` (the shape's vocabulary has one home; `s5_precheck` and
   `story_step` import it).
2. The `_gate_refusal` rows go into `test_then_remainder.py` K20 (fast keep file that already holds the `_gate_refusal` class table),
   not `test_words_doors.py` (`A\:390`'s file, 151.4 s slow): same behaviour, a witness the builder can run.
3. `refusal_cause` lowers the tag once for both prefix tests (consistent with `_passable`, `:3970`); its one consequence is stated
   in item 1's note and pinned by k22-7.
4. N5 adds no top-level helper: the alias map is built inside `_terminal_runs` (owns literally one function).
5. The new door texts say "conductor" in `story_step` (the file's own word, `:2025`) and keep "orchestrator" in `s5_precheck.report`
   (that function's word, `:4796`).

## §8. Reading trail (every load-bearing line re-read on its carrier this turn)

- `.git\worktrees\read-main\HEAD` (50d9012), `.git\worktrees\fv130b-n5\HEAD` (`wip/fv130b-n5`), `.git\packed-refs` :17, :72, :115, :383
  (Grep); `.git\worktrees\tbw-t2\HEAD`.
- `P\` :1-789 (whole up to §9; §9-§12 not re-read beyond :789); `A\` :290-424; `R30a\` whole.
- `B\s5_precheck.py` :76-111, :1640-1729, :1880-1960, :3955-4014, :4660-4805 (Read); Grep `refusal_cause|report|awaits_answer|...`.
- `B\detector_verdict.py` :40-289 (Read); Grep `REFUSAL_CAUSES|_tag_lines|...`.
- `B\exit_gate.py` :1780-1859 (Read). `B\story_step.py` :1930-2099, :2950-2979 (Read).
- `B\window_record.py` :420-499, :1307-1441 (Read); Grep `def word_let_go` :1217.
- `B\contract.py` :4000-4110 (Read). `B\acceptance.py` :405-524, :660-734, :840-949 (Read). `B\proof_level.py` :1990-2022.
  `B\stand_gaps.py` :395-419.
- Tests: `test_detector_verdict.py` :95-129, :225-252 + Grep `^def`; `test_exit_gate_scope.py` :345-374; `test_then_remainder.py`
  :795-839; `test_s5_precheck.py` :2152-2172, :3015-3096, :4773-4802 + Grep `^def`; `test_window_record.py` :1184-1191 + Grep.
- `test-layers.json` :1-50, :1245-1274, :1540-1560, :4886-4935, :6300-6319, :6450-6479, :6975-7103, :10255-10274 + Grep;
  `slow_tests.json` :1-20 + Grep; `judgment-census.json` Grep (`check_run_mapping` :995, no row for the four functions).
- `T2\detector_verdict.py` Grep (:68, :148, :178, :211, :223); `T2\tests\test_detector_verdict.py` Grep `^def` (tag_cases :97).
- `docs/tasks/specs/20261114-told-before-work-t1r-t2-dispatch-spec.md` :205-254. `docs/tasks/specs/20261113-p1b-dry-story-spec.md` Grep
  `C4г|known_red` (:242, :636). `plans/builder-rules.md` :14-73. `docs/TESTING.md` :100-144.
- Negative claims with their positive controls: `awaits_answer` in the package → 0 hits (Grep -i, count); control `predating` → 27
  hits in 8 files, same call shape. `WORDS_REFUSED_AT_SOURCE` readers → `detector_verdict.py`, `s5_precheck.py`, tests, CHANGELOG
  (files_with_matches). Non-py `predating|awaits_answer` → CHANGELOG only. The three fast files absent from `slow_tests.json` — control:
  three slow names hit in the same Grep.

## §9. What the designer did NOT establish

- The list of files `scenario_walk.py --witness-for` prints for each card (no shell in this role): the DoD names the command and the
  fast/slow rule; the builder pastes the actual list.
- Whether `test_repair_marker.py`, `test_words_doors.py` or `test_driver_stop_record.py` pin a text N4 changes for an open-oracle
  record (Grep for `family` pins found none in them; their `_gate_refusal` inputs were not read) — the builder's item-5 grep covers it.
- The exact C4г row ids P1-b N4 will write (rows do not exist yet).
- Whether tbw T2 will touch `tag_cases` before it merges (read on the T2 worktree as it stands).
- Whether `C.case_config(task_root)` can raise on a real story (N5 wraps it; row w7 forces it).
- `run_history.read_run_blocks`' ordering code was not re-read (taken from `_terminal_runs`' own docstring, `:465-470`, and the F-order
  test `:1188-1224`).
- That every `Record` reaching `_gate_refusal` from `s5_precheck` carries `refused` from `parse` (`exit_gate.py:463` zips `refused`
  into records — seen in a Grep line, the function body not read).

# Rules-debt phase 2 — builder cards S9, FL2, FL4 (t-995, t-1000, F19)

Designer draft for the Lead. It answers plan critic t-989 (`docs/tasks/specs/reviews/t-989-rules-debt-phase2-wave2-plan.md`,
sections S9, FL2, FL4, K6, K8). The cards spec `docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md` was read, not
written. Parent spec: `docs/tasks/specs/20261117-rules-debt-fix-spec.md` (S9 :379-394, F-L2/F-L4 :538-544).

**Two rounds.** t-995 drafted §1, §2 (S9) and the FL2 facts, then stopped at its budget. t-1000 (this round) applied the
Lead's three decisions (§4), drafted FL4 (§3b) and replaced §5. It too stopped at its budget (WARN at 250K) before the FL2
producer files were read, so FL2 is still not a builder card (§5).

**Where the code was read.** t-995: the root checkout, branch `main`, head `a6df7fd1`. t-1000: the root checkout, head
`03249c95` (git status at session start). The memory pointer `.claude/worktrees/read-main` does not exist: a Glob for
`.claude/worktrees/*/ai-packages/qa-factory/scripts/controller.py` lists 80 worktrees and no `read-main`. The critic read
`origin/main` = `a372b01a`. t-1000 re-read every line it cites (for example `controller.py:3779-3788`, `:9387`, `:9904`). No
designer in either round had Bash, so **no command was run**. Every measurement below is a reading with file:line. Every
premise that needs a run is listed under "Premises the Lead must measure before dispatch", with the command.

---

## §1. Architecture, rules, owners (designer rule 1)

FR sections: S9 A (FR-4, FR-57), B (FR-7, FR-8), D (FR-59), E (FR-35). FL2 E (FR-21, FR-35), C (FR-12, FR-13). FL4 E (FR-22),
A (FR-1, FR-2, FR-46), C (FR-11, FR-14, FR-38, FR-42), D (FR-59), E (FR-37).

| card | AR-n touched | how kept (the change check written into the DoD) |
|---|---|---|
| S9 | AR-13 | the person's word on a `review` gap has ONE reader, `window_record.review_gap_words`, and every judge reads it through `word_let_go`; no judge reads `stage_overrides[]` for it by itself |
| S9 | AR-15 | the one predicate `window_record.word_let_go` gains the rule, so all five judge sites (controller ×1 for gaps, `word_kept` → `window_record.run`, `story_step finish`, `driver_dispatch`) agree with no wiring of their own |
| S9 | AR-24 | the person's words reach the pass record whole (`_record_person_pass` keeps `word_at`; the report reads the word by `at`) |
| S9 | AR-25 | the new recorded state "review gap passed by a person's word" has its way out: the next window build (a critic verdict written) removes the gap, and the pass line in the report goes too (`_word_bare_lines` reads facts) — row in `design/state-exits.md` |
| S9 | AR-27 | the delivery reason keeps its owner `review` (verdict `no`); the pass shows as its own line in "passes recorded by your word" |
| S9 | AR-28 | `review_gap_words` errs toward NO entry: an unreadable pipeline, `*`, a revoked word, another stage, a placeholder word → nothing is let go |
| S9 | AR-9 | the door text of the `review` gap (`GAP_ORIGIN["review"]`, `window_record.py:318-320`) names the person's road |
| FL2 | AR-13, AR-22, AR-26 | §3: the closed `skip_class` (F-L2-A decided (a)) has one producer (the strategist's plan row, checked by the plan contract) and one reader (the ledger's skip branch); the kind and owner stay the existing `pending_implementation` ones |
| FL4 | AR-22 | the new request field `bug_candidates` has its producer (`Controller.build_rework_request`) and EVERY reader (§3b.4) in ONE commit; a record without the field reads as "no candidates" at every reader |
| FL4 | AR-13 | "is K-n / R-n a bug candidate of this story" has one reader, `check_delivery.bug_candidates` (the existing `_grounding_candidates` body under a public name); the controller, the driver's facts and the brief all call it, none re-reads the grounding table or the register |
| FL4 | AR-9 | every new refusal names what it expected (the candidate refs the story holds, or the input that could not be read) and a door (`--candidates <ref>` / `--cases <ids>`) |
| FL4 | AR-25 | the refusal "no case" of an S7 rework gains its move for the state "a bug candidate has no case" (today the conductor borrows a case: `factory-rules-debt.md:24`); no new recorded state |
| FL4 | AR-28 | an unreadable grounding table or register never makes a ref a candidate: the call is refused and names the unreadable input |
| FL4 | AR-19 | stage twins: `--rows` (S1-S3), `--cases` (S4+) and `--candidates` (S7) are three spellings of "what this rework goes back over", read by the same two judges (`no_move.check_args`, `build_rework_request`); no new command road |

Checks added or altered (AR-29, census classes of `scripts/tests/fixtures/judgment-census.json`):

| check | card | owner it serves | census class | blocking |
|---|---|---|---|---|
| `window_record.review_gap_words` + the `review` rule of `word_let_go` (a person's word lifts a window gap) | S9 | intent (the person's word, P13) | xref (a join of the word to the gap by an identifier; the class `contract.probe_gap_words` / `word_let_go` already carry — the builder copies the class of the `word_let_go` row of the census; when the census has no such row, the builder returns a question naming the missing row) | lifts a block, never adds one |
| FL2's skip class | FL2 | judgment (the S3 strategist picks the class; a tier above accepts it at the S3 window) for the word; data for the mapping | shape (the plan-contract check of a closed value) | blocks delivery (`no`) |
| FL4: the candidate-membership refusal in `build_rework_request` (a ref the story does not name as a bug candidate; candidates on another stage or role; candidates with cases or rows) | FL4 | data (code: the ref joins a list the code reads) | xref | refuses the call (`ValueError`, the call's fault, FR-46) |
| FL4: the same membership rule in `no_move.check_args` (an option's `args.candidates`) | FL4 | data | xref | refuses the conductor's option (`ArgsRefused` road, the conductor is told once) |
| FL4: whether a candidate deserves a bug, and which draft form | FL4 | judgment (the S7 analyst; accepted at gate B by the person and by the S8 reporter's own checks, which already exist) | not a code check: no census row | — |

Commit lines: the form is `tools/architecture_gate.py`'s (not copied here). Content for S9:
`architecture: AR-13, AR-15, AR-24, AR-25, AR-27, AR-28 -- <how kept, from the table>`; `judgment: adds data check
review_gap_words` (the gate's own vocabulary decides the exact form; `judgment: none` is not legal here because a check
is added). Content for FL4: `architecture: AR-9, AR-13, AR-19, AR-22, AR-25, AR-28 -- <how kept, from the table>`, and a
`judgment:` line that names the two xref checks it adds, in the gate's own form. `judgment: none` is not legal for FL4.

---

## §2. S9 — X10: a person's word on a `review` gap (FR-57)

### 2.1 Measured premises (PROJECT.md «Как принимается изменение пакета» п. 6 (а))

| # | premise | carrier | result |
|---|---|---|---|
| P-a | a person's word on a `review` gap happens on real runs | `scripts/tests/fixtures/stories/local-1-arm-b/pipeline.json:615-635` | **yes**: three live S5 records, `match` = the whole window line `review:@regression LOCAL-1_TC_001 in-stock add shows success toast, badge 1 and one cart line — the manifest row carries no \`critic_verdict\`` (and two more for TC_002), `by: human`, words "go on … They stay unverified in the report." |
| P-b | the person also typed `*` on the same window | same file `:678-684` | **yes**: `match: "*"` at 15:53:20, after the three review words (15:49) — the hostile input of F-9-4 occurs in real data |
| P-c | instance ids carry spaces | same file `:617-631` | **yes** (Playwright titles). So the one-token prefix road (`contract.prefix_value`, `contract.py:121-132`: "must be a single token") **cannot** name these instances; `probe gap:` words on the same run named CASE keys (`:687`, `:695`) |
| P-d | today nothing reads such a word | `window_record.py:1741` (`WORD_READ_KINDS = ("quality", PROBE_GAP_KIND)`), `:1891-1892` (only those kinds join `read`), `:1912` (`_unread_words` over every line not in `read`), `GAP_ORIGIN["review"]` comment `:314-317` ("NO recorded word of a person passes this gap"); `word_let_go` keeps `review:` lines, pinned `test_window_record.py:1847-1850` | **yes, by reading**. Not run: no single recorded fixture has both a window and a review word (`local-1-arm-b` has no `work/automation-manifest.json` and no `work/windows/` — Glob over `local-1-arm-b/**/*.json`, 34 files, none; `cart-1/work/windows/` has six windows and no `review:` word in `cart-1/pipeline.json` — Grep `"match":` lists all 15 cart-1 matches, none `review:`). Step 0 of the card makes the run |
| P-e | the existing "a word passes a window line" road | `window_record.py:1242-1289 word_let_go` ("THE one predicate", AR-13, AR-15); callers `controller.py:7122`, `:7522`; `window_record.word_kept` `:1292-1310` → `window_record.py:2185`, `story_step.py:2563`, `driver_dispatch.py:1018` (Grep `word_let_go\(|word_kept\(` over scripts) | five judges, one predicate |
| P-f | delivery today for a test with no critic verdict | `ledger.py:1183-1185` → `review_skipped`; `ledger.py:1630`, `check_delivery.py:1676-1679` → kind `review_gap`; `delivery-verdict-kinds.json:35` `review_gap: no, owner review`, `:100-102` | `no`, owner `review` |
| P-g | the precedent "the word passes the STEP, never the FACT" | `delivery-verdict-kinds.json:3` note (`word_passed:then_unbound` keeps `chain_broken`, `no`); `check_delivery.py:1640-1658 _no_run_word_suffix` (a `not_run` pass keeps its `no` row, adds "passed by the person's word at S5"); `report_facts.py:3291-3363` (every recorded pass gets a line; fact `other` via `_word_bare_lines`, `:3360`) | the precedent exists twice |
| P-h | the precedent for "the person's word moves the test into their debt" | `window_record.py:344-351` (`probe_gap`: "S8 reads it as the critic's `unverified` ('Left with you')"); `ledger.py:1213-1217` `review_unverified` → `after_checks` (`delivery-verdict-kinds.json:58`) | exists for probe gaps, not for reviews |

### 2.2 Direction (chosen; forks F9-1 and F9-2 decided by the Lead, §4)

1. **Which road.** The review rule joins **`word_let_go`** (P-e): one predicate, all judges. It is not a third road
   beside `WORD_READ_KINDS`/`probe_gap_named` (critic F-9-6, P31).
2. **Which matcher** (critic F-9-4). A NEW reader `window_record.review_gap_words(window, task_root) -> dict`
   `{instance id: {"words", "at"}}`, built on the two primitives every word reader already uses: the filter
   `contract.live_stage_overrides(pipeline, ("S5",))` (`contract.py:158-174`: revoked and empty words out) and the
   predicate `contract.names_whole` (`contract.py:135-155`). Rule: an instance `iid` of `window["instances"]` is
   named when a live S5 record's `match`, stripped, is NOT `*`, does NOT hold a `<placeholder>`
   (`waiver.PLACEHOLDER_RE`, the rule `split_overridden` applies, `waiver.py:210-211`), and
   `contract.names_whole("review:" + iid, match)` is True. The latest record by file order wins (`words` = its
   `decision` whitespace-folded, `at` = its `at`). The pipeline is read from `task_root / "pipeline.json"`, never from the
   window (a role writes the window). Why not `waiver.split_overridden` itself: it reads `*` as everything
   (`waiver.py:205`, `:217`), and it asks "is the WORD whole inside the LINE". The controller's lines are bare
   (`review:<iid>`, `acceptance.py:1157-1172`), so a word that is the whole printed line (P-a, the real data) is never
   inside the bare line, while `window_record.run`'s lines carry the explanation. Asking "does the word name the gap
   head `review:<iid>`" gives the same answer at every judge, whatever the line form. This is the same direction as
   `contract.probe_gap_words` (word → identifier, `contract.py:5648-5659`).
3. **What the pass does to delivery** (critic F-9-3): **reading (i)**. The word passes the S5 STEP. The ledger is
   untouched, so the test still reads `review_skipped` / `review_rejected` → `review_gap` → `no`, owner `review` (P-f).
   The pass is recorded and the report shows it in "passes recorded by your word" (P-g). FR-35 holds, because the
   critic's verdict, or its absence, is never rewritten. Fork F9-1: **decided (i) — Lead, 17.11.2026, по рекомендации, до
   слова владельца** (§4). (ii) would add a ledger state and a kinds row later. The ledger is not in S9's owns.
4. **Recording**: `controller._s5_gap_problems` writes one `_record_person_pass` line per let-go review gap, ONLY when
   the completion is otherwise accepted (`not problems`), the precedent `controller.py:7527-7534`.

### 2.3 Card S9 (header-ready)

```
given: this file §2; docs/tasks/specs/reviews/t-989-rules-debt-phase2-wave2-plan.md (S9 section);
  ai-packages/qa-factory/design/factory-rules.md (whole); plans/builder-rules.md; ai-packages/qa-factory/design/architecture.md
  (AR-13, AR-15, AR-24, AR-25, AR-27, AR-28); scripts/tests/fixtures/stories/local-1-arm-b/pipeline.json:615-700 (the world)
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/window_record.py (review_gap_words [new], word_let_go, word_kept, verdict, GAP_ORIGIN["review"] text and its comment :314-320, the WORD_READ_KINDS comment :1732-1740)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/controller.py (_s5_gap_problems only) — HOT
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_window_record.py (rows in fv1_30b_word_let_go_is_the_one_predicate and one new row function beside it)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_probe_gap_word.py (one row: the controller end to end)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json (the row of review_gap_words only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/state-exits.md (one row)
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/controller-blocks.md (regenerated by tools/controller-blocks-gen.py only if a block text of _s5_gap_problems changes)
non-goals: ledger.py, check_delivery.py, delivery-verdict-kinds.json, waiver.py, contract.py, acceptance.py (no change: reading (i));
  the `*` meaning anywhere else; the not_run / row_fields rules of word_let_go; the run() line-form observation O-1 (§5)
handoff: the builder report (builder.md rule 7) with the witness, the FR walk (A, B, D, E), the census row, and step 0's output
edges: E1-E12 below
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>` — the slow files it names
  (test_window_record.py, test_probe_gap_word.py, test_controller_*) are named "judged by the batch canon"; plus
  `python -B tools/architecture_index.py --check`
siblings: axis 26 (n/a by design: the word is not split_overridden's — reason in §2.2 item 2, stated in the
  review_gap_words docstring); axis 32 (census row, owned); axis 34 (the word_let_go road, no third road); axis 5 (S5
  windows <-> S6 walker lanes: no S6 twin reads a review word — the builder confirms with one Grep for
  `word_let_go` over driver_stage_s6.py, positive control: the same Grep finds it in driver_dispatch.py)
designer: <this file, once accepted>
```

**Step 0 (premise run, before any edit; output goes into the report).** In the scratchpad copy `cart-1` whole. In the
copy's `pipeline.json`, add one S5 record whose `match` is `review:<iid>`, with `<iid>` = an instance of
`work/windows/S5-qa-code-critic-2.json` whose `review.verdict` is not `approved`. If none is non-approved, delete that
instance's `critic_verdict` in the copy's manifest. Then run `python -B <pkg>/scripts/window_record.py --task <copy> --dispatch S5-qa-code-critic-2 --out <scratch>/w.json`.
Expected on today's code: the gap line `review:<iid> — …` is listed, and a `note: recorded, not read by this window: …`
line names the word. If the line does not appear, the builder stops and returns the output (the premise is false, and
the Lead re-plans).

**Items** (each with its test row and the source of the expected value):

1. `review_gap_words(window, task_root)`, per §2.2 item 2. It never raises: anything that is not a dict, an unreadable
   or absent `pipeline.json`, or any exception → `{}`. Test: a table row in a new function
   `s9_review_gap_words` in `test_window_record.py`, one row per input of E1-E6. Expected from the debt row FR-57
   (`factory-rules-debt.md:85`), the parent spec S9 (в) (`20261117-rules-debt-fix-spec.md:384-387`), and critic F-9-4.
2. `word_let_go(lines, window, index, lets_go=None, review_words=None)`: a third rule. For each instance `iid` of the
   window that is in `review_words`, the line `review:<iid>` is let go, and so is any line that starts with
   `review:<iid> — ` (the `verdict` form, `window_record.py:1868`). `review_words=None` lets no review line go (the
   refusing default; every existing caller is unchanged until it passes the argument). The `index is None` early return
   (`:1260-1261`) must NOT skip the review rule. The invariant is that a broken precheck index does not hide a person's
   word, and that a broken word read does not let anything go. So: if `index` is None, the not_run and row_fields rules
   let nothing go, and the review rule still runs. The docstring names the third rule. Test: rows in
   `fv1_30b_word_let_go_is_the_one_predicate`. The existing pin `"review:i" in kept` (`test_window_record.py:1847-1850`)
   stays true with `review_words` absent. New rows: a word naming `i` lets `review:i` go; `stale_review:i` is kept
   (another kind); `review:i[neg]` is kept (a parameter sibling); `review_words` given + `index=None` lets `review:i`
   go and nothing else. Expected: the same sources plus `word_let_go`'s own docstring invariant ("Every other line is
   kept").
3. `word_kept(...)` passes `review_words=review_gap_words(window, task_root)`. This wires `window_record.run`,
   `story_step finish` and `driver_dispatch` with no edit of theirs. Test: one row beside `test_window_record.py:2522`
   (`word_kept` over `["review:A"]` with a pipeline holding `review:A`) → `([], ["review:A"])`.
4. `verdict(...)`: a `review` line whose instance `review_gap_words` names joins `read` (`:1891-1892`), so
   `_unread_words` no longer prints "recorded, not read" for a word that IS read. A `*` word, or a word naming the reason
   only, is still printed as unread. Test row: `info` holds no "recorded, not read" line for the naming word, and still
   holds one for `*`. Expected: the `_unread_words` docstring (`:1750-1751`: "never passes a gap nobody reads it for").
5. `GAP_ORIGIN["review"]` door text (`:318-320`) adds the person's road: `… or, when the person accepts the test without
   the critic's verdict, the orchestrator records their words with \`waiver.py --task <T> --stage S5 --block
   "review:<instance id>"\` (the S5 step passes; delivery still reads no critic verdict)`. The comment `:314-317` and the
   `WORD_READ_KINDS` comment `:1732-1740` are rewritten to say the review word is read through `word_let_go`. Test: one
   `check_in` row on `WR._explain("review:x", [])` for `--block "review:`. Expected: FR-2 and AR-9 (a door the receiver
   can use).
6. `controller._s5_gap_problems` (`controller.py:7520-7535`): the call `word_let_go(other_gaps, window,
   self._s5_word_index(d))` gains `review_words=window_record.review_gap_words(window, self.store.root)`. After the
   refusals, when `not problems`, every let-go line that starts with `review:` gets one `_record_person_pass("S5",
   d.get("id"), [...])` item: `{"error": "review:<iid>", "decision": words, "at": at, "by": "human", "check": "review",
   "case": "", "tag": <iid>, "subjects": [{"instance_id": <iid>}]}`. Test: one row in `test_probe_gap_word.py` (it already
   drives `_s5_gap_problems` end to end with `PASSED_BY_PERSON`, `:51`, `:145`): a window whose only gap is `review:IID`,
   plus the word → accepted, and ONE line in `passed-by-person.jsonl` with `block` `review:IID` and the words whole;
   the same window with `*` instead → refused "unresolved window: review:IID". Expected: FR-4 ("a check stops a silent
   pass, never an informed one"), P13, and the precedent `:7527-7534`.
7. `design/state-exits.md`: one row: state "S5 review gap passed by the person's word"; exit = a critic verdict
   recorded later removes the gap (the next window has none) / the word revoked (`waiver.py --revoke`) → the gap
   refuses again. Doc only; the witness is the DoD key run (CLAUDE.md rule 11 DOC-DISPATCH WITNESS) or the walker
   row if `scenario_walk.py --witness-for` names one.
8. Census: one row for `window_record.review_gap_words`, class per §1. `word_let_go`'s existing row (if any) changes its
   note only.

**Edges (rule 11), each with the invariant it protects:**

- E1 `*` (P-b, real). → not read. INVARIANT: a stage-wide word never lifts a review gap. (Critic F-9-4.)
- E2 a revoked record (`revoked_at`) naming the gap → not read (`live_stage_overrides`). INVARIANT: a word taken back acts
  nowhere (FR-40).
- E3 a word of another stage (S6) naming `review:<iid>` → not read. INVARIANT: an S5 gap is passed only by an S5 word.
- E4 a word naming another instance: `review:A` vs instance `A[neg]`, and vs `B`; a word naming `sensitivity:<iid>`; a
  word naming only the reason tail ("the manifest row carries no `critic_verdict`"); a bare `<iid>` or a case key → not
  read. INVARIANT: only a word that names THIS gap head lifts it (`names_whole` right edge, `contract.py:141-145`).
  (Fork F9-2 — whether a case key also counts — is **decided: no — Lead, 17.11.2026, по рекомендации, до слова
  владельца**, §4.)
- E5 empty input: a window with no `instances`, an empty `stage_overrides`, a pipeline that is not an object, an absent
  `pipeline.json`, unreadable bytes → `{}`, nothing let go. INVARIANT: an unknown is never a pass (AR-28, FR-59).
- E6 a `match` holding a `<placeholder>` (an unfilled door) → not read (the `split_overridden` rule, `waiver.py:211`).
- E7 limit / truncation: `_record_person_pass` cuts `block` at 400 and `decision` at 1000 (`controller.py:2425-2426`) and
  keeps `word_at` and `finding_id` for the whole (`:2432-2435`). An instance id over 400 chars → `finding_id` carries the
  whole block. INVARIANT: the cut loses nothing the report needs (AR-24). No new limit.
- E8 CONFLICT with the critic's own verdict: the gap stands for `rejected` too (`acceptance.py:1171-1172`). A word naming a
  rejected instance lets the S5 step go (P13: through any gate). The ledger still reads `review_rejected` → `no`
  (`ledger.py:1189-1190`). INVARIANT: FR-35, the report never changes the critic's verdict. In `window_record.run`, the
  let-go happens before `_sent_back_lines` (`:2235`), so a word-passed rejected instance is not sent back. That is
  the person's decision, recorded.
- E9 POSITIONAL (`word_let_go`): the review rule runs even when `index is None`. INVARIANT: the not_run and row_fields
  rules still let nothing go on a None index (pinned `:1832`), and the review rule depends only on `review_words`.
- E10 POSITIONAL (`_s5_gap_problems`): the record is written only after every refusal of the method ran and none fired,
  and is never written for a refused completion. INVARIANT: no pass line for a window that did not close (the probe_gap
  precedent). `passed_green` keeps reading the whole `gaps` (`:7525`). INVARIANT: a word-passed review never makes a
  `passed_green` completion legal.
- E11 TEMPORAL: windows and pipelines written before S9 have no new field and need none. The reader reads existing
  `stage_overrides[]` records, so the three words of a story in flight (P-a shape) start to act on the next judge after
  the upgrade. That is intended: they were recorded as words and promised to pass (debt row cost line). An OLD
  `passed-by-person.jsonl` with no `review:` line reads as before. Nothing is rewritten (builder-rules 9).
- E12 outside input: the `match` text is the person's (through `waiver.py`). Battery rows in item 1's table: magnitude
  (a 10 000-char match), nesting (n/a, a string), encoding (a non-ASCII instance id, a match with `\u2014`, which is the
  verdict separator), empty / blank / non-string `match` → not read, never raises. The 400 cut is E7.

**Reused function in a more responsible role.** `contract.names_whole` moves from advice (`_unread_words`, reporting) to a
gate input. The error it may make is toward False (it then asks the person again). Adversarial inputs that must stay
False: E4's list, plus `review:A` inside `review:AB`, `review:A.1`, `review:A::x`, `review:A[`, and `review:A@x`
(`contract.py:141-145`). `contract.live_stage_overrides` keeps its role (a filter).

**FR walk the builder writes** (PROJECT.md p. 1): A FR-4 (informed pass recorded), FR-57 (the ban now has a door), FR-2
(the door is usable: the conductor records it); B FR-7 (the same boundary is not re-asked: the word is read), FR-8
(words carried whole); D FR-59 (unknown → no pass); E FR-35 (critic verdict unchanged); C, F, G one line each.

**Live proof (FR-33):** a `live-runs` row "a person's `review:<iid>` word at S5 lets the window close; the report shows
the pass and delivery `no` owner review". Reading the `waiver.py` CLI's acceptance of the block text is part of it. NOT
ESTABLISHED by reading: whether `waiver.py`'s recheck holds `review:<iid>` against the standing refusal (`waiver.py:225-252`).
The tests write the record with `waiver.apply_stage_override` the way `test_controller_release.py:516` does.

### 2.4 Readers of every touched file (rule 7)

The S9 readers of rule 7 were not grepped this session (no Bash; the budget ran out first). The command for the Lead
or the builder: Grep over `tools/`, `.githooks/`, `.claude/` for
`window_record|controller\.py|state-exits|controller-blocks|judgment-census|test_window_record|test_probe_gap_word`.
Positive control in the same shape: `architecture_gate` in `.githooks/commit-msg`. The known readers from the cards
spec §8 (`docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md:773`): `tools/controller-blocks-gen.py` reads
`controller.py`. It changes in S9 only if a block text of `_s5_gap_problems` changes, and item 6 changes none. Package
readers of `word_let_go`/`word_kept` (P-e): `story_step.py:2563`, `driver_dispatch.py:1018` are unchanged (the new
argument is passed inside `word_kept`); `controller.py:7122` (shape call) is unchanged (`review_words` stays None, and
review is not a shape line).

### 2.5 Collisions

- `controller.py` HOT: S9 owns `_s5_gap_problems` only. FL4 owns `BINDING_KEYS`, `build_rework_request` and the `rework`
  argument parsing of `main` (§3b). These are function-disjoint, so they can run in parallel by D-0048. The Lead's order
  is `S9 → FL4` (§6 Order).
- `window_record.py`: C3-d (after S9, critic F-d1) touches `verdict`. Queue `S9 → C3-d`.
- `judgment-census.json`: `wave-a/integrate` (unmerged) edits it (critic F-S4). S9 starts after that merge (S-e).
- `test_window_record.py`, `test_probe_gap_word.py`: slow (cards spec §0.3). Rows only, with no new test file, so
  `test-layers.json` is untouched. `pile/live-run-fvf/batch-3` (dry_*, fixtures, slow_tests.json): no overlap, because S9
  only reads `local-1-arm-b` and copies `cart-1` into the scratchpad.
- Taken batches (cards spec §4): onboarding-forge/2 names `window_record` and `controller` rows. Lead decision 17.11:
  dev1's batches do not hold each other.

---

## §3. FL2 — R3: "skipped because the product has no such surface" (FR-21)

### 3.1 Facts

- The writer is the S3 PLAN row: `disposition: skip` with a free `reason` → `ledger.py:763-773` returns
  `skipped:<reason>` (re-read t-1000: `:771-772` `return (f"skipped:{reason or 'no reason given'}", "")`). The kinds lookup
  reads the prefix `skipped` → `planned_skip` (`delivery-verdict-kinds.json:95`, `:21` `none`). The run-row form
  `skipped:marked skipped in the run` (`:94`) is `decided_elsewhere` (critic F-L2-1).
- The existing road for "the product does not carry this yet": manifest `unresolved: [{case, reason:
  "pending_implementation"}]` → `ledger.py:731-732` → state `pending_implementation` (returned as
  `("pending_implementation", case)`) → kind `pending_implementation`, `no`, owner product (`delivery-verdict-kinds.json:44`,
  `:97`). It is read per CASE (`_cases_for_row`, `ledger.py:707`). A plan row with no case is never reached by it: the loop
  `for case in cases` (`:716`) is empty for a row that S4 never cased, and a `skip` row gets no case.
- Premise (critic F-L2-2): 3 skip rows over the recorded plans, 1 of class R3 (`local-1-0108/work/test-plan.json`, "the
  owner's answer leaves no implemented quick-view add path …"). The critic counted by a script. It was not re-run here
  (premise PL-1, §5).

### 3.2 Why the existing road cannot carry it as is (critic F-L2-3, P31)

The `pending_implementation` road is written at S5 (the automator's manifest) or by grounding, and it keys on a case. A
row the strategist skips at S3 never reaches S4/S5, so no case and no manifest row exist for it. **One road is still
possible**: the S3 strategist writes the existing word `pending_implementation` as the plan row's closed class (not a
new word), and the ledger's skip branch reads it into the existing state `pending_implementation`. The kind, the owner
and every reader downstream stay the existing ones. No new kind, and no new kinds-file word.

### 3.3 Direction (F-L2-A decided)

- **F-L2-A: decided (a) — Lead, 17.11.2026, по рекомендации, до слова владельца** (§4, P31: one road). A closed field
  `skip_class` on the plan row, with the ONE value `pending_implementation` (the existing state word).
  `ledger.py:771-772` returns `("pending_implementation", "")` for a `skip` row carrying it, before the free-reason
  return. The kinds file is unchanged. The producer is the strategist charter plus the plan contract (`planning_contract`).
- The meaning of a delivery word changes (a skip row can now read `no`). PROJECT.md п. 6 (б): the plan critic reads this
  text before the builder.

### 3.4 Card FL2 — NOT complete (budget stop, t-1000)

What is decided and can stand in the card:

```
owns (function names of the producer files NOT read yet — §5 item 1):
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/ledger.py (the skip branch of the plan-row state, :763-773, only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/planning_contract.py (<the plan-row field check — function to name>) — after wave-a/integrate
C:/QAFactory/forge-repo/ai-packages/qa-factory/agents/qa-test-strategist.md (one line: when to set skip_class)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_third_verdict.py (one row: a skip row with skip_class -> pending_implementation -> no) — after C3-R (C3-R adds a row to the same file)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json (own row: the plan-contract check of skip_class)
non-goals: references/delivery-verdict-kinds.json (unchanged: the state word already maps); the manifest `unresolved` road;
  parsing `reason` (FR-12); any change to `unverifiable` rows
edges:
  E1 TEMPORAL: skip_class absent (every plan written before FL2) -> today's `skipped:<reason>` -> planned_skip. INVARIANT: no
     old plan changes its verdict, and no story in flight is refused for lacking the field (builder-rules 9).
  E2 skip_class with a value outside the closed set (`Pending_Implementation`, `pending`, "", a list, a number) -> refused
     by the plan contract, the allowed value named (FR-1). INVARIANT: an unknown class is never read as planned_skip, and the
     ledger never sees one (if it does, through a hand-edited plan: the ledger reads it as absent -> E1, and the plan
     contract's refusal is the one place that speaks).
  E3 skip_class on a non-skip row (automate, gap, unverifiable, manual-*) -> refused by the plan contract (the class belongs
     to a skip). INVARIANT: an automate row never reads `pending_implementation` through this field.
  E4 POSITIONAL: the new return sits after `_placeholder_reading` (:766-769) and before the free-reason return (:772).
     INVARIANT: an open placeholder still wins (J-C7), a red of the row's cases still wins (:767), and a skip row without
     the class reads exactly as today.
  E5 the reason text is never read for the class (FR-12): a reason saying "not implemented" with no skip_class stays
     planned_skip.
  E6 CONFLICT: a skip row with skip_class whose requirement is ALSO `not_implemented` in the grounding table ->
     two `pending_implementation` records (the ledger row and `check_delivery._pending_implementation_records`); both
     `no`, owner product. INVARIANT: the verdict is `no` either way; the report may list both (each is its own item:
     plan row vs requirement). Whether to dedupe is NOT this card's.
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>`; test_third_verdict.py is slow:
  "judged by the batch canon"
siblings: axis 34 (one road: the existing state word, no new kinds word); axis 32 (census row owned); the delivery-verdict
  axis (SIBLING_MAP:144: readers unchanged — the state maps through the existing row)
```

Readers of the touched files (rule 7): not grepped (§5 item 2).

---

## §3b. FL4 — R4: the S7 rework door for a case-less bug candidate (FR-22)

### 3b.1 Facts (read t-1000; file:line on head `03249c95`)

| # | fact | carrier |
|---|---|---|
| F1 | the refusal: `if stage_ok and not wanted and int(stage[1:]) > 3:` → `"--cases must name at least one case of the approved scope …"` (critic F-L4-1 lines re-verified) | `controller.py:3779-3788` |
| F2 | its comment: the driver's roads never reach it, because `no_move.check_args` and `answer_pairs_owed` stop an empty S4+ list first | `controller.py:3780-3782` |
| F3 | `check_args` refuses `not cases and int(stage[1:]) >= 4` ("names no case, and {stage} needs at least one of the approved scope"); `ARGS_KEYS = ("stage", "role", "cases", "rows", "cause")`; it refuses cases + rows together | `no_move.py:191`, `:246-251` |
| F4 | `answer_pairs_owed` serves only the question-answer rework of `ANSWER_REWORK_OWNERS` = strategist (S3, `--rows`) and designer (S4, `--cases`); it is NOT on the conductor's `rework_stage` road a bug candidate takes | `driver_machine.py:718-746`; `controller.py:9387` |
| F5 | the conductor's road: an option `rework_stage` with `args` → `NM.check_args` (`no_move.py:451`) → `record_seam_rework` stores `{**args, words_file, at, before}` → `seam_rework_step` calls `self.rework(stage, role, cases, …, rows=…)` → `driver_dispatch.rework` adds `--cases` / `--rows` | `driver_conductor.py:733-752`; `driver_machine.py:617-645`; `driver_dispatch.py:2847-2896` |
| F6 | the facts `check_args` reads come from `no_move_facts`, each fact in its own try (`None` when its reader raises) | `driver_conductor.py:352-407` |
| F7 | today the conductor is told to borrow a case: `conductor-actions.json` actions row 8 "a bug candidate … goes to the failure analyst at S7 as a bug report (the rework names any case of the approved scope)" | `references/conductor-actions.json:8` |
| F8 | the candidate record: `bug_candidate_record` → `{"kind": "bug_candidate", "case": "", "ref": <K-n or R-n>, "item_key": ref, …}`; kind `after_checks`, owner product | `check_delivery.py:2363-2368`; `delivery-verdict-kinds.json:63` |
| F9 | the candidates are listed by `_grounding_candidates(artifacts) -> (candidates, unreadable)`: `K-n` = `rows[].risks[].id` of the grounding table of a DIFF story; `R-n` = `contract.candidate_defects` of the register; `unreadable` names an input that exists and cannot be read. Its one caller is `_grounding_records` (`:2496`); callers pass the task root as `artifacts` (`test_check_delivery.py:2123`) | `check_delivery.py:2371-2405` |
| F10 | the request fields a continuation carries: `BINDING_KEYS` (…, `"plan_rows"`); a record is `dict(p, …, request_binding=request_binding(p))`, so every request field lands on the record; retry and relaunch packets read `_original_request` (the binding) | `controller.py:310-317`, `:1820-1821`, `:8932`, `:8940-8955`, `:9006` |
| F11 | an S7 dispatch with an empty scope is not refused by `dispatch`: the empty-scope rule covers `DERIVED_SCOPE_STAGES` only (S5/S6 by the controller-api text "Never type an S5/S6 scope") | `controller.py:5599-5620`; `references/controller-api.md:63-68` |
| F12 | the role-facing readers of a rework packet: `inject_context.PACKET_DISPATCH_KEYS` (the keys a role is handed), `story_step._packet_lines` (prompt lines), `story_step.IDENTITY_FIELDS` ("every field the prompt reads … is compared"), `brief_pack` rework head (`Plan rows of this dispatch:`) | `inject_context.py:571-573`; `story_step.py:1147-1166`, `:1237-1244`; `brief_pack.py:4498-4504` |
| F13 | the S7 author: `acceptance.stage_def_of(stage)["roles"][0]`, already used by the controller (`_consumer_reject_parent`) | `controller.py:3952-3960` |
| F14 | a draft resting on no failing test already has a form: `evidence: "code-reading"`, required `title, impact, violates, oracle, fact, check_state, manual_steps`; no `case` / `triage_ref`; one requirement, one draft (`R_CR_TWICE`); checked by `bug_records.code_reading_problems` | `contract.py:1964-1968`; `bug_records.py:798-848` |
| F15 | the recorded world: `cart-1` holds a register row `R-13 … | bug:candidate-defect |` (a candidate); no recorded story holds a grounding table with `risks[]` K-n ids (Grep `"K-\d+"` over `fixtures/stories`: 2 hits, both in `cart-1/work/handoffs/S5-qa-code-critic-1.values.applied.yaml`, which is not a grounding table) | `cart-1/work/requirements-register.md:25` |
| F16 | `--cases` users in package text: `controller-api.md:19`, `:61`; `conductor-actions.json:8`, `:71`; `s7.md:130`, `:140`, `:249`, `:258` | Grep `--cases` (this round) |

### 3b.2 Direction (one road, P31)

1. **The route.** `controller.py --operation rework --stage S7 --role qa-failure-analyst --candidates <ref>[,<ref>]
   (--words-file <file> | --reason "<…>") --brief`. It belongs to `rework`, not to `stage-scope` (critic F-L4-2):
   `stage-scope` is read-only and derives S5/S6 scope; a rework sends back accepted work. `--candidates` is the third
   spelling of "what this rework goes back over", beside `--rows` (S1-S3) and `--cases` (S4+). It is not a new command.
2. **The schema change** (§3b.3): one new request/record field, `bug_candidates`. No triage, ledger, draft or kinds
   schema changes.
3. **No triage row for a candidate** (critic F-L4-2, "how its triage row is keyed"). A triage row answers a failed test
   or an observation (`contract.row_names`). A candidate has neither. The analyst's product for a candidate is a bug
   draft in the existing code-reading form (F14), keyed by `violates` (one requirement, one draft), or the reason in
   its digest why no bug is owed. The S8 reporter files only drafts that gate B selects, and gate B is asked again after
   an S7 rework (s7.md:259-260; `conductor-actions.json` `rework_stage.precondition`: "the stages after S<n> that are
   completed … run again after it"). So the reporter, the ledger and `grounding_records` need no change (§3b.4 lists
   each one with "unchanged"). Whether the K-n form fits the code-reading draft is premise PL4-3 and fork F-L4-C.
4. **Which judges change**: `build_rework_request` (the controller, the last judge) and `no_move.check_args` (the
   conductor's option). `answer_pairs_owed` is unchanged (F4: not on this road). `ANSWER_REWORK_OWNERS` is unchanged:
   a candidate rework is not an answer rework (axis 5 below).

### 3b.3 The schema change, field by field

| field | where | type and values | producer | absent (TEMPORAL world 1: every record, packet and driver state before FL4) |
|---|---|---|---|---|
| `bug_candidates` | dispatch REQUEST and so the RECORD (F10); its `request_binding` (through `BINDING_KEYS`) | a sorted list of distinct strings, each a `ref` that `check_delivery.bug_candidates(task_root)` lists; present ONLY on an S7 rework by the S7 author that named candidates; never `[]` (no candidates → key absent) | `Controller.build_rework_request(…, candidates=…)` from `--candidates` | every reader treats an absent key as "no candidates" and does exactly what it does today |
| `candidates` | `args` of a `rework_stage` option (conductor's verdict), and the driver state `seam_rework` record (`{**args, …}`) | a list of strings | the conductor writes `args`; `check_args` normalises it (`clean("candidates")`); `record_seam_rework` stores it unchanged (`**args`) | `args.get("candidates") or []` → today's path; an old `seam_rework` record with no key → `pending.get("candidates") or []` → today's call |
| `candidates` | `no_move_facts` result | a list of refs, or `None` when the reader raised | `driver_conductor.no_move_facts` through `check_delivery.bug_candidates` | n/a (computed each time) |

TEMPORAL world 2 (after FL4): a record with `bug_candidates` is read by the same package that wrote it (one generation,
B-014). A story in flight keeps its old records (no key) and gains the field only on a new S7 candidate rework. Nothing is
rewritten.

The flag: `--candidates` (comma-separated, like `--cases`). The Lead's text said `--candidate <K-n>`; the plural keeps the
three spellings parallel. This is a closed small choice (§4). A rename is a find-and-replace before dispatch.

### 3b.4 Producer and every reader, in one commit (AR-22)

| site | change | why it must move in the same commit |
|---|---|---|
| `check_delivery.bug_candidates(artifacts) -> (candidates, unreadable)` [new, public] | returns `_grounding_candidates(artifacts)`; any exception → `([], ["the bug candidates"])`; never raises | the ONE reader of the fact (AR-13); the controller, the facts and the brief call it |
| `controller.BINDING_KEYS` | gains `"bug_candidates"` | without it a retry or relaunch packet of a candidate rework loses its candidates (F10: the TP2-2406 class) |
| `controller.Controller.build_rework_request` | new keyword `candidates=None`; the rules of §3b.5; `request["bug_candidates"] = sorted(set(valid))` when non-empty | the producer |
| `controller.main` (the `rework` operation's argument parsing beside `--cases`, `:9904`, and the call into `build_rework_request`) | `--candidates` help text; splits on `,`, strips, drops blanks, passes `candidates=` | the CLI door the conductor and the driver call |
| `no_move.ARGS_KEYS`, `rework_args_list`, `check_args` | `ARGS_KEYS` gains `"candidates"`; `rework_args_list` prints one more line `candidates (S7 only, instead of cases): <refs>` (at most `CASES_IN_LIST`, then `… (+N more)`; `(not read)` when the fact is `None`); `check_args` per §3b.5 | the conductor's option is judged before the controller (F2); without it the conductor's candidate option is refused "names no case" |
| `driver_conductor.no_move_facts` | one more `read("candidates", lambda: [c["ref"] for c in CD.bug_candidates(self.task_root)[0]])`; when `bug_candidates` reports `unreadable` and returns no candidate, the fact is `None` | the closed list `check_args` reads |
| `driver_machine.seam_rework_step` | passes `candidates=list(pending.get("candidates") or [])` to `self.rework` | carries the stored choice to the controller |
| `driver_dispatch.Driver.rework` | new keyword `candidates=()`; `args += ["--candidates", ",".join(candidates)]` when non-empty, after the `--rows` branch | the one method every code road of a rework passes (`:2889-2890`) |
| `inject_context.PACKET_DISPATCH_KEYS` | gains `"bug_candidates"` | the role is handed the key (FR-49, FR-38) |
| `story_step._packet_lines` | after the plan-rows line: `Bug candidates of this dispatch: <refs> (K-n: a risk in work/grounding.yaml rows[].risks[]; R-n: a register row marked bug:candidate-defect)` when the packet carries them | the prompt says what the rework is for |
| `story_step.IDENTITY_FIELDS` | gains `"bug_candidates"` | its invariant: every field the prompt reads is compared (`:1237-1239`) |
| `brief_pack` rework head (`:4498-4504`) | the same line after `Plan rows of this dispatch:` | the brief says it too (FR-49) |
| `references/conductor-actions.json` actions row 8 | "(the rework names any case of the approved scope)" → "(`--candidates <its ref>` instead of `--cases`)"; `rework_stage.run`: `[--cases <ids> \| --rows <ids> \| --candidates <refs>]`, `args`: `… \| "candidates": [<refs>]`; `precondition`: "ids inside the approved scope; candidate refs among the story's bug candidates" | FR-37: the command text the conductor reads is the command the code takes; F7 removes the borrowing |
| `references/controller-api.md:55-61` | one sentence: on S7 the failure analyst may be sent back over bug candidates with `--candidates <K-n,R-n>` (`bug_candidates`), instead of `--cases` | the API text names every field of the request |
| `agents/qa-failure-analyst.md` | one line: a rework whose packet names bug candidates asks, for each, for a bug draft in the code-reading form, or the reason in your digest why no bug is owed | FR-38: the role hears the requirement before the work (a role behaviour change: FR-33 live row) |
| `skills/qa-story/phases/s7.md` (section "No repair — …", after the APP_BUG bullet) | one sentence: a bug candidate sent at gate B is reworked with `--candidates <ref>`, never with a borrowed case | the skill road reads s7.md (P31: the driver road and the skill road take one door) |
| `scripts/tests/fixtures/judgment-census.json` | two rows (the two xref checks of §1) | axis 32 |

Readers that do NOT change (each read, with the reason):

| reader | why unchanged |
|---|---|
| `controller._cover_basis` / `_covers` (`:2966-3009`) | S4 designer credit only; a candidate rework is S7 |
| `controller.dispatch` empty-scope rule (`:5599-5620`) | S5/S6 only (F11); an S7 candidate dispatch has `scope: []` and passes as today |
| `controller._carry_plan_rows` | `plan_rows` only; `bug_candidates` rides in the binding (F10) |
| `driver_machine.answer_pairs_owed`, `ANSWER_REWORK_OWNERS`, `driver_dispatch.py:2142` | question-answer reworks only (F4) |
| `check_delivery.grounding_records` / `bug_candidate_record` / `GROUNDING_HOW` | the candidate record and its `how` text are unchanged and still true ("the conductor sends it to the failure analyst at S7") |
| `ledger.py`, `delivery-verdict-kinds.json` | no ledger state, no kind: a candidate stays `after_checks` until the person decides (fork F-L4-D on what a filed bug does to the line) |
| the S8 reporter / `bug_records.code_reading_problems` / `gate_preflight` draft checks (`:5918`) | the analyst writes an existing draft form (F14); the reporter files what gate B selects, as today |
| `story_step.py:360-362` (S3 rework plan rows) | S3 only |

### 3b.5 Rules of the two judges (exact behaviour; expected values from FR-22, the debt row `factory-rules-debt.md:24` and critic F-L4-2)

`build_rework_request(…, candidates=None)`:

1. `wanted_candidates` = the given refs, stripped, blanks dropped, duplicates dropped, order sorted.
2. When `wanted_candidates` is non-empty:
   a. the stage must be `S7` and the role the S7 author (`acceptance.stage_def_of("S7")["roles"][0]`, F13); otherwise one
      `ValueError` problem: "--candidates sends the S7 failure analyst back over bug candidates; for <stage> <role> name
      `--cases` (S4 and later) or `--rows` (S1-S3)";
   b. cases or rows given too → one problem: "--candidates and --cases/--rows together: name one of them";
   c. `found, unreadable = check_delivery.bug_candidates(self.store.root)`; refs not in `{c["ref"] for c in found}` → one
      problem: "bug candidate(s) not in this story: <refs>; the story's bug candidates are <refs or 'none'>" plus, when
      `unreadable` is non-empty, "; <names> could not be read, so a candidate there is not known (record the input, then
      ask again)";
   d. the `sent_back` lookup (`:3776`) does NOT run (a candidate rework never inherits a consumer-reject scope).
3. The case refusal (F1) becomes `if stage_ok and not wanted and not wanted_candidates and int(stage[1:]) > 3:` with its
   text unchanged. Every problem joins `problems` and is raised whole by `_raise_all` (K1 C3-11 rule, `:3729-3731`).
4. When no problem: `request["bug_candidates"] = wanted_candidates`; `scope` stays `sorted(wanted)` = `[]`;
   `case_version_links` = `[]` (no case).

`check_args(args, facts)`:

1. `candidates = clean("candidates")`; a non-list → "\"args\" cases / rows / candidates are not lists of ids".
2. Candidates given: stage must be `S7` and the role one of `roles["S7"]` (the existing role rule already holds the
   accepted-work part); cases or rows together → "\"args\" names candidates with cases or rows; one of them only";
   `facts.get("candidates")` is `None` → "the story's bug candidates could not be read, so \"args\" candidates cannot be
   checked"; refs outside the fact → "\"args\" names a bug candidate the story does not hold: <refs>".
3. The "names no case" rule (`no_move.py:250-251`) fires only when `not cases and not candidates`.
4. The normalised result carries `**({"candidates": candidates} if candidates else {})`.
5. An args object naming only cases or rows behaves byte for byte as today, whatever `facts["candidates"]` holds (also
   `None`).

### 3b.6 Card FL4 (header-ready)

```
given: this file §1, §3b; docs/tasks/specs/reviews/t-989-rules-debt-phase2-wave2-plan.md (FL4, K6, K8);
  ai-packages/qa-factory/design/factory-rules.md (whole); plans/builder-rules.md; ai-packages/qa-factory/design/architecture.md
  (AR-9, AR-13, AR-19, AR-22, AR-25, AR-28); ai-packages/qa-factory/design/factory-rules-debt.md:24 (the FR-22 row);
  scripts/tests/fixtures/stories/cart-1/work/requirements-register.md:25 (the world: R-13)
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/controller.py (BINDING_KEYS; Controller.build_rework_request; main: the rework operation's --candidates argument and its call into build_rework_request) — HOT
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/check_delivery.py (bug_candidates [new] only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/no_move.py (ARGS_KEYS, rework_args_list, check_args)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_conductor.py (no_move_facts only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_machine.py (seam_rework_step only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_dispatch.py (Driver.rework only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/inject_context.py (PACKET_DISPATCH_KEYS only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/story_step.py (_packet_lines, IDENTITY_FIELDS)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/brief_pack.py (the rework head block :4498-4504 only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/conductor-actions.json (actions row 8; moves.rework_stage run/args/precondition)
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/controller-api.md (the rework paragraph :55-61, one sentence)
C:/QAFactory/forge-repo/ai-packages/qa-factory/agents/qa-failure-analyst.md (one line)
C:/QAFactory/forge-repo/ai-packages/qa-factory/skills/qa-story/phases/s7.md (one sentence in "No repair — …")
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_controller_rework_window_words.py (rows beside B-K8 :1024 and B-K16 :1064-1069)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_check_delivery.py (one row beside :2123)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_exploratory_answers.py (one row beside :206: the seam carries candidates to the controller call)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json (FL4's two rows only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/controller-blocks.md (regenerated by tools/controller-blocks-gen.py only if its check says a block of the owned functions changed)
non-goals: ANSWER_REWORK_OWNERS, answer_pairs_owed, driver_dispatch.py:2142; ledger.py, delivery-verdict-kinds.json, triage
  schema, bug draft schema, bug_records.py, the S8 reporter; grounding_records' own behaviour; stage-scope; _s5_gap_problems
  (S9's); the gate B exploratory `bug` road (EXPLORATORY_REWORK, it has a case); any change to what the analyst judges
handoff: the builder report (builder.md rule 7) with the witness, the FR walk (A, C, D, E), the two census rows, step 0's output
edges: E1-E13 below
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>`; the slow files it names
  (test_controller_rework_window_words.py, test_check_delivery.py) are "judged by the batch canon";
  test_exploratory_answers.py is keep and not slow (run it as the walker names it); plus
  `python -B tools/architecture_index.py --check`
siblings: axis 5 (stage twins --rows / --cases / --candidates: one pair of judges, ANSWER_REWORK_OWNERS unchanged because a
  candidate rework is not an answer rework; the gate B exploratory bug road keeps --cases because it has a case);
  axis 34 (one door: `rework`, no new command; the borrowed-case workaround is removed from conductor-actions.json);
  axis 32 (two census rows owned); axis 26 (n/a: no new reader of a person's word; the words travel whole by --words-file
  as today)
designer: <this file, once accepted>
```

**Step 0 (before any edit; output into the report).** (a) `python -B -c "import sys; sys.path.insert(0, r'<pkg>/scripts'); import controller, check_delivery; print('ok')"`
— confirms the lazy import of `check_delivery` inside `build_rework_request` makes no cycle (if it fails, the builder
returns the trace: the reader's home is then a Lead question). (b) In a scratchpad copy of `cart-1`, print
`check_delivery._grounding_candidates(<copy>)`. Expected: `R-13` in the candidates (F15). If `R-13` is absent, the builder
stops and returns the output (the test world is false; the Lead re-plans).

**Items** (each with its test row and the source of the expected value):

1. `check_delivery.bug_candidates` per §3b.4. Test row in `test_check_delivery.py`: the cart-1 copy → `R-13` among the
   refs and `unreadable == []`; a copy whose register is empty bytes → `([], ["the requirements register"])`, never a
   raise. Expected: the docstring of `_grounding_candidates` (`:2372-2375`, "never read as 'no candidates'").
2. `build_rework_request` per §3b.5. Rows in `test_controller_rework_window_words.py` (the file drives the CLI, `:156`):
   (i) S7 analyst + `--candidates R-13` on a story whose register holds R-13 → a request with `bug_candidates ==
   ["R-13"]`, `scope == []`; (ii) the same with `--candidates R-99` → refused, the text names `R-99` and the story's refs;
   (iii) `--candidates R-13 --cases TC-1` → refused "name one of them"; (iv) S6 `qa-runner` + `--candidates R-13` →
   refused naming `--cases`; (v) S7 with neither → the unchanged text "--cases must name at least one case of the approved
   scope" (the B-K8 pin's twin); (vi) `--candidates " , "` → read as none → (v). Expected: FR-22 (the debt row's "refuses a
   call with no case while a candidate has none"), FR-1, FR-46.
3. `BINDING_KEYS`: row: a request with `bug_candidates` → `request_binding(p)["bug_candidates"] == ["R-13"]`, and
   `_relaunch_packet` of that record carries it. Expected: the TP2-2406 comment `controller.py:304-309`.
4. `check_args` per §3b.5. Rows beside B-K16 (`:1064-1069`): S7 args with `candidates: ["R-13"]` and facts
   `candidates: ["R-13"]` → clean, carries `candidates`; facts `candidates: None` → refused "could not be read"; the same
   args with an S6 role → refused; args with cases only and facts `candidates: None` → clean (byte for byte today's).
   `rework_args_list` row: the candidates line appears, and `(not read)` when `None`.
5. The driver: one row in `test_exploratory_answers.py` beside `:206` (it fakes `no_move_facts`): a `seam_rework` record
   with `candidates: ["R-13"]` → the controller call carries `--candidates R-13` and no `--cases`. An old record with no
   key → the call carries no `--candidates`. Expected: F5 and AR-22.
6. Packet readers: `PACKET_DISPATCH_KEYS`, `_packet_lines`, `IDENTITY_FIELDS`, brief head. Row (in the item 2 test, on the
   request it built): `story_step._packet_lines(packet)` holds `Bug candidates of this dispatch: R-13`; a packet without the
   key gives the same lines as today. (No row in `test_story_step_materialize.py`: it is QUARANTINED,
   `test-layers.json:10291`.)
7. Text carriers (conductor-actions.json, controller-api.md, analyst line, s7.md): witness = DOC-DISPATCH key run (rule 11)
   with these keys quoted before the run: `--candidates <its ref>` (conductor-actions.json), `--candidates` (controller-api.md,
   s7.md), `code-reading` (qa-failure-analyst.md), and the negative control: the key `the rework names any case of the
   approved scope` is ABSENT from conductor-actions.json.
8. Census: two rows (§1), class `xref`, owner data.

**Edges (rule 11), each with the invariant it protects:**

- E1 TEMPORAL (world 1): records, packets, bindings and driver `seam_rework` records written before FL4 have no
  `bug_candidates` / `candidates` key → every reader behaves as today. INVARIANT: no story in flight changes or is refused
  (builder-rules 9).
- E2 TEMPORAL (world 2): `materialize` of a packet with `bug_candidates` compares the field (`IDENTITY_FIELDS`); `where`
  rebuilds from the record, which carries it (F10). INVARIANT: the card `where` writes equals the card `materialize`
  renders.
- E3 POSITIONAL (`build_rework_request`): the candidate rules run BEFORE the case refusal, and the case refusal reads
  `not wanted and not wanted_candidates`. INVARIANT: an empty S4+ case list WITHOUT a valid candidate is still refused
  with today's exact text; candidates never open the door for another stage or role.
- E4 POSITIONAL: the `sent_back` lookup (`:3776`) is skipped when candidates are given. INVARIANT: a candidate rework never
  takes a consumer-reject scope.
- E5 POSITIONAL (`check_args`): the candidate rules sit after the stage and role rules and before the "names no case" rule.
  INVARIANT: a case-only option is judged exactly as today, whatever the candidates fact holds.
- E6 empty / absent: `--candidates ""`, `" , "`, `[]` in args → none → the case refusal (E3). `bug_candidates` with no
  grounding table and no register → `([], [])` → every ref refused "not in this story; the story's bug candidates are
  none". INVARIANT: a ref is accepted only when the code read it in the story.
- E7 unknown (FR-59, AR-28): a register or table that exists and cannot be read, and the ref is not among the readable
  candidates → refused, the unreadable input named. A ref found in the readable input while the OTHER input is unreadable
  → accepted (it is established). INVARIANT: an unknown never becomes "is a candidate".
- E8 CONFLICT: the person's words name a case and a candidate in one answer → `check_args` refuses "one of them only"; the
  conductor offers two reworks. INVARIANT: one rework, one unit (the K1 rule), no silent drop of either.
- E9 CONFLICT: a candidate a green plan row already closes (no `bug_candidate` line in the report) is still in
  `bug_candidates` (the list is every candidate the story names, not only the open ones) → accepted. Fork F-L4-B.
  INVARIANT: the person's word reaches the analyst (P13); the analyst judges whether a bug is owed.
- E10 limit: `rework_args_list` prints at most `CASES_IN_LIST` (60) refs, then `… (+N more)`; `check_args` reads the whole
  fact. No limit on refs per call. INVARIANT: the printed list may be cut, the check never is.
- E11 outside input (the person's words → the conductor's args → the CLI): battery rows in item 2/4: magnitude (200
  refs, all valid → accepted; one invalid → refused naming it), spelling (`r-13`, `R-013`, `R-13a`, `R-13 ` → only the last,
  stripped, matches), encoding (a non-ASCII ref → refused), nesting (a list inside `candidates` → "not lists of ids").
- E12 words: a candidate rework with `--words-file` carries `person_words` and the `rerun_after` stamp exactly as a case
  rework of S7 does (`_rerun_stamp(state, stage, role, [])`, premise PL4-2). INVARIANT: S8 and gate B run again after it.
- E13 FR-3: a refusal for an unreadable input is the factory's own defect text; the person is not asked to fix the file.

**Reused function in a more responsible role.** `check_delivery._grounding_candidates` moves from a report producer
("Left with you", advice) to a gate input (the rework door). The error it may make is toward NOT a candidate (the call is
refused with the door: the known refs, or the unreadable input). Adversarial inputs that must stay refused: a K-n of a
story whose table is not `implementation_source: diff`; an R-n the register holds without `bug:candidate-defect`; `r-13`,
`R-013`, `R-13a`, `K-1,K-2` passed as ONE ref; an empty string; a ref read while the register is empty bytes.

**FR walk the builder writes:** A FR-1, FR-2 (each refusal names the expected refs and a usable door), FR-46 (`ValueError`:
the call's fault); C FR-11 (the analyst is told the field it must act on), FR-14 (the request shape grows one optional key;
old shapes still read), FR-38 (the requirement reaches the role in the brief and the charter), FR-42 (the state "candidate,
no case" now has a move); D FR-59 (E7); E FR-22 (the road to a bug no longer borrows a case), FR-37 (the command text equals
the code); B, F, G one line each.

**Live proof (FR-33):** a `live-runs` row "a person's gate B words 'this needs a bug report (K-n/R-n)' send the analyst to
S7 with `--candidates`, a draft is written, gate B lists it, the reporter files it".

### 3b.7 Readers of every touched file (rule 7)

Not grepped this round (budget stop). The command: Grep over `tools/`, `.githooks/`, `.claude/` for
`check_delivery|no_move|driver_conductor|driver_machine|driver_dispatch|inject_context|story_step|brief_pack|conductor-actions|controller-api|qa-failure-analyst|phases/s7|test_controller_rework_window_words|test_check_delivery|test_exploratory_answers|judgment-census|BINDING_KEYS|PACKET_DISPATCH_KEYS|IDENTITY_FIELDS|ARGS_KEYS`,
positive control `architecture_gate` in `.githooks/commit-msg`. Known from the cards spec §8: `tools/controller-blocks-gen.py`
reads `controller.py` (changes only if a block text of the owned functions changes) and reads `stage_guard`/`host_adapter`
names (not touched). The Lead runs the command before dispatch and adds one line per hit ("unchanged / changes in stream X").

### 3b.8 Collisions

- `controller.py` HOT: FL4's functions (`BINDING_KEYS`, `build_rework_request`, `main`'s rework parsing) are disjoint from
  S9's `_s5_gap_problems`. The Lead's order is `S9 → FL4`. The late node merges `main` into its tree (D-0048).
- `judgment-census.json`: `wave-a/integrate` edits it → FL4 starts after that merge (S-e), as S9 does; S9 and FL4 add
  different rows.
- `test_check_delivery.py`: FL2 does not own it; C3-R does not own it (C3-R owns `test_third_verdict.py`, F-e1).
- `pile/live-run-fvf/batch-3` (dry_*, fixtures, slow_tests.json, test-layers.json, selftest.py, scenario_walk.py,
  test_form_selftest.py, per critic K6): no FL4 owned path. FL4 only reads `cart-1` and copies it into the scratchpad.
- Taken batches: onboarding-forge/2 names `controller`, `story_step`-adjacent rows (cards spec §4); onboarding-forge/1
  names `controller.py` (:50). Lead decision 17.11.2026: dev1's batches do not hold each other. Not checked this round:
  whether any taken batch names `no_move`, `driver_conductor`, `driver_machine`, `driver_dispatch`, `inject_context`,
  `brief_pack` or `conductor-actions` (§5 item 3).

---

## §4. Forks

| id | question | options | recommendation | status |
|---|---|---|---|---|
| F9-1 | what the person's word on a review gap does to delivery | (i) passes the S5 step only; delivery `no`, owner review, pass line shown; (ii) a new ledger state / kind | (i) | **decided (i) — Lead, 17.11.2026, по рекомендации, до слова владельца** |
| F9-2 | does a case-key word also pass the review gaps of its instances? | (a) no; (b) yes, via `scope_instances` | (a) | **decided (a) no — Lead, 17.11.2026, по рекомендации, до слова владельца** |
| F-L2-A | how a skip "because the product lacks it" is typed | (a) closed `skip_class: pending_implementation`; (b) a new kinds word `skipped:<word>` | (a) | **decided (a) — Lead, 17.11.2026, по рекомендации, до слова владельца** |
| F-L4-B (new) | which refs `--candidates` accepts | (a) every candidate `_grounding_candidates` names (one reader, the person may name a candidate whose check is green); (b) only the OPEN ones (`grounding_records` kind `bug_candidate`; needs the ledger and `gather` facts at the rework door) | **(a)**: cheaper, one reader, and errs toward letting the person's word through; the analyst judges whether a bug is owed. (b) refuses a ref the person can see in the grounding table | open (FL4 is executable on (a)) |
| F-L4-C (new) | which draft form the analyst uses for a candidate | (a) the existing code-reading draft (F14; needs `oracle` and an S1 `fact` id); (b) a new draft form for a grounding K-n with no S1 fact | **(a)**, one road (P31). If PL4-3 shows a K-n has no S1 fact id, the analyst's draft is refused by `code_reading_problems` with its own door, and the gap is a NEW node (b) with owns and a test, never a silent workaround | open (FL4 is executable on (a); it changes no draft code) |
| F-L4-D (new) | what a filed bug does to the candidate's "Left with you" line | (a) nothing: the `bug_candidate` line stays (`after_checks`) beside the filed bug; (b) a filed bug that names the candidate closes the line (a reader change in `grounding_records`, a draft field naming the ref) | **(a) for FL4**; (b) as a finding in the rules-debt pile: it changes a delivery line's meaning (п. 6), and FL4's debt is the door only | open (FL4 unaffected) |

Closed by me (no design weight): the pass record uses fact `other` (S9). The new S9 reader lives in `window_record.py`.
Test rows go into existing keep files, no new file. FL4: the flag is `--candidates` (plural, parallel to `--cases` /
`--rows`); the request field is `bug_candidates` (the record kind's own word); the brief line names refs only, with no
subjects, so no new truncation is introduced; the candidate reader is a public wrapper over the existing body, not a
second body.

---

## §5. What is left (t-1000 budget stop at 250K)

**Premises the Lead must measure before dispatch** (each never stated as a fact above):

- PL-1 (FL2): `python -B -c "import json,glob,collections; c=collections.Counter(); [ (c.update([r.get('disposition')]), print(p, r.get('reason')) if r.get('disposition')=='skip' else None) for p in glob.glob(r'C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/stories/*/work/test-plan.json') for d in [json.load(open(p,encoding='utf-8'))] for r in (d.get('rows') if isinstance(d,dict) else d) or [] if isinstance(r,dict)]; print(dict(c))"`
  — expected `automate 96, gap 58, skip 3, unverifiable 5` and the local-1-0108 R3 reason (critic F-L2-2).
- PL4-1 (FL4): the cart-1 candidate: `python -B -c "import sys; sys.path.insert(0, r'C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts'); import check_delivery as D; from pathlib import Path; print(D._grounding_candidates(Path(r'C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/stories/cart-1')))"`
  — expected `R-13` among the candidates, `unreadable == []` (the card's test world; step 0 (b) repeats it).
- PL4-2 (FL4, E12): what `_rerun_stamp(state, "S7", "qa-failure-analyst", [])` returns on a story with S8 done — read
  `controller._rerun_stamp` (not read this round) or run it on a copy of `local-1-0108`. Expected: the same stages as a
  case rework of S7 (S8, gate B). If it returns nothing for an empty list, E12 is false and the card needs a line for it.
- PL4-3 (FL4, F-L4-C): does a grounding K-n map to an S1 code fact id (`bug_records.bundle_facts`)? No recorded story has
  K-n risks (F15), so this is a reading of `grounding_table.py` risks vs `bundle_facts`, or the plan critic's judgment.
- PL4-4 (FL4): `driver_dispatch.run_role` with `scope=[]` for S7 `qa-failure-analyst` behaves as a rework with a reason
  (the brief carries the candidates). Read `run_role` (not read this round).

**Not done:**

1. FL2 producers not read: `planning_contract.py` (after the wave-a merge; the function that checks a plan row's
   fields — its name goes into owns), `agents/qa-test-strategist.md` (the line for `skip_class`), the
   `test_s1_s2_contract.py` G1-10 reader (quarantined, by reading). FL2 stays a partial card until then. The rest of its
   text (§3.4) is decided.
2. Rule 7 greps not run: S9 (§2.4), FL2 (`ledger|planning_contract|qa-test-strategist|test_third_verdict|judgment-census`
   over `tools/`, `.githooks/`, `.claude/`), FL4 (§3b.7).
3. Collisions not checked by diff: `git -C C:/QAFactory/forge-repo diff --stat origin/main...wave-a/integrate` and
   `...pile/live-run-fvf/batch-3` against FL4's and FL2's owns; the taken batches' status cells for the FL4 file names
   (§3b.8).
4. Observation O-1 (an analog noticed, not widened): `window_record.run` calls `word_kept(problems, …)` on lines that
   carry ` — <explain>` (`verdict` `:1868`), while `word_let_go` matches the exact `<kind>:<iid>` (`:1277-1285`). The
   not_run and row_fields rules may let nothing go in `run()`. Found by reading, not run. A finding for the Lead.
5. The census class of `word_let_go` (S9 item 8) and the census row form FL4 copies were not read in
   `judgment-census.json`.

## §6. Critic finding → where answered

| finding | answered |
|---|---|
| F-9-1 no plan | §2.2, §2.3 items 1-8 |
| F-9-2 premise unmeasured | §2.1 P-a..P-h (by reading); the run is step 0 |
| F-9-3 delivery effect | §2.2 item 3; F9-1 decided (i) |
| F-9-4 `*` vs split_overridden | §2.2 item 2; E1, E4; reused-function paragraph |
| F-9-5 lines drifted | header: 7421/7440 confirmed |
| F-9-6 axes 26/32/34 | card `siblings:`; §1 census row |
| K6 (S9) | §2.5 |
| F-L2-1 writer | §3.1 (the plan row, `ledger.py:763-773`, re-read t-1000) |
| F-L2-2 premise | §3.1; run PL-1 (§5) |
| F-L2-3 second road | §3.2; F-L2-A decided (a) |
| K6 (FL2) | §3.4 owns notes: after C3-R (`test_third_verdict.py`) and after wave-a (`planning_contract`, census) |
| K8 axis 34 (FL2) | §3.4 `siblings:` |
| F-L4-1 lines drifted | §3b.1 F1, F2 (`:3779-3788`), `:9387`, `:9904` re-read |
| F-L4-2 pointer, not a plan | §3b.2-§3b.6: route (`rework`, not `stage-scope`), refusal invariant (E3), which pre-check moves (`check_args` yes, `answer_pairs_owed` no: F4), triage key (none: §3b.2 item 3), readers (§3b.4), controller-blocks (owns line), tests per item |
| K6 (FL4) | §3b.8 |
| K8 axis 5 (FL4) | card `siblings:` (stage twins `--rows` / `--cases` / `--candidates`; ANSWER_REWORK_OWNERS unchanged, with the reason) |

**Order.** S9 first (after the `wave-a/integrate` merge, for the census). Then FL4 on `controller.py` (`S9 → FL4`, the
Lead's order; their functions are disjoint, so the late node merges `main` and keeps both pins green). C3-d after S9
(`window_record.py`). FL2 after C3-R (`test_third_verdict.py`, C3-e's pin) and after the wave-a merge
(`planning_contract.py`, census), and only once its card is finished (§5 item 1) and the plan critic has read §3. In
parallel now: S9 alongside C3-R (disjoint owns). FL4 may run alongside C3-R (disjoint owns), but after S9 by the Lead's
order. The FL2 card's completion (a designer read of two files) can run alongside everything.

## §7. Reading trail

t-995: the critic review t-989 (whole); cards spec `:1-76`, `:520-609`, `:640-852`; parent spec `:370-399`, `:525-662`;
`factory-rules-debt.md:15-89`; `window_record.py:140-169`, `:300-380`, `:1170-1315`, `:1725-1925`, `:2170-2280`;
`controller.py:2400-2489`, `:6990-7120`, `:7380-7567`, `:7680-7756`; `acceptance.py:999-1039`, `:1130-1179`;
`contract.py:115-204`, `:5630-5690`; `waiver.py:202-252`, `:740-1050`; `s5_precheck.py:4060-4130`; `ledger.py:700-779`,
`:1150-1229`, `:1610-1674`; `check_delivery.py:1615-1694`; `report_facts.py:3285-3375`; `delivery-verdict-kinds.json`;
`word-passed-facts.json`; `block-names.json`; `SIBLING_MAP.md:115-144`, `:448-457`, `:564-600`;
`local-1-arm-b/pipeline.json:466-735`; `test_window_record.py:1800-1859`.

t-1000 (head `03249c95`, root checkout): this file (whole); critic review t-989 (whole); cards spec `:570-779`; parent spec
`:530-549`; `factory-rules-debt.md:15-29`; `controller.py:296-320`, `:1790-1834`, `:2960-3009`, `:3700-3978`,
`:5570-5629`, `:8920-9010`; `check_delivery.py:2355-2534`, imports `:31-54`; `no_move.py:100-299`;
`driver_machine.py:610-654`, `:690-769`, `:2730-2779`; `driver_conductor.py:352-411`, `:733-763`;
`driver_dispatch.py:2820-2909`; `inject_context.py:555-589`; `story_step.py:1148-1252`; `brief_pack.py:4488-4512`;
`validate_artifacts.py:2485-2531`; `contract.py:1895-1984`, `:4540-4569`; `bug_records.py:798-848` (Grep -A);
`place_answers.py:200-339`; `references/conductor-actions.json` (whole); `references/controller-api.md:10-74`;
`references/delivery-verdict-kinds.json` (whole); `skills/qa-story/phases/s7.md` (whole); `ledger.py:700-779`;
`test-layers.json:1-30` and section keys (`keep` :36, `quarantine` :7182).
Greps (Grep tool; shapes noted): `ANSWER_REWORK_OWNERS|must name at least one case|…` over `scripts/*.py`; `bug_candidate`
over the package minus tests; `triage_ref` over `scripts/*.py`; `"plan_rows"` (files) and `plan_rows` in seven named files;
`check_args\(|…` over scripts; `def no_move_facts|"rework_roles"`; `"K-\d+"` and `"R-\d+"` (count) over
`fixtures/stories`; `bug_candidate|candidate-defect` (count) over fixtures; `candidate-defect` in cart-1's register;
`grounding_records\(|_grounding_candidates\(`; `import acceptance|import check_delivery|check_delivery as` over five
driver/controller files (positive control: `import acceptance` found in `controller.py`, `driver_machine.py`; no
`check_delivery` import there); `new_prefix|"new-` in `place-answers.json` (an earlier call with a brace path glob
returned nothing and was a miscall: the direct path found `:12`); the test-file names in `test-layers.json` and
`slow_tests.json` (positive control: `test_check_delivery.py: 85.4` found). Glob: worktrees list (no `read-main`); `*s7*`.

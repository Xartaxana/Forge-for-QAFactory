# TQ2-1 — case merge on the designer's side and the readers of `Archived`: state check, history, spec for the remainder

Draft by the designer (t-579), 13.11.2026, for node TQ2-1 of
`plans/piles/test-code-quality/batch-2-sliyanie-kejsov-i-chitateli.md` and its finding
`plans/piles/test-code-quality/findings/20261102-sliyanie-kejsov-bez-ispolnitelya-na-storone-dizajnera-i-dvojnye-chitateli-shapki.md`.
Code read on the root checkout `C:\QAFactory\forge-repo` (equal to origin/main per the brief). P = `C:\QAFactory\forge-repo\ai-packages\qa-factory`.
Acceptance of this draft belongs to the Lead; every fork in section 7 is returned, none is decided here.

---

## 1. State: what is done, partly done, not done

### 1.1 The table (one row per item of the finding's «Что именно менять», plus the facts it observed)

| # | Item of the finding | State | Evidence (file:line, read on the root checkout) |
|---|---|---|---|
| 1a | Designer charter: rule "one form, branches as parameters" | NOT DONE | `P\agents\qa-case-designer.md` has no such rule. The only nearby lines: :10 "how many tests it becomes is the automator's call" (P17), :50 "never two cases for one class", :57 "Equivalence by consequence ... Apply it when you are about to merge cases to save space" (this argues AGAINST a merge, it does not order one). Grep `(?i)archiv\|merge\|parametr\|one form\|branches as` on the file -> only :57. Positive control: the same pattern on `P\agents\qa-case-critic.md` finds :41, :43, :44, :69, :81. |
| 1b | Designer charter: merge EXECUTION (absorbed case `status: Archived`, survivor carries its Thens and `covers`) | NOT DONE | Same grep as 1a: no `Archived`, no fold. :23 still says "One case per plan row" (a fold across rows contradicts it, edge E3). |
| 1c | Paired cut in the case critic's charter | PARTLY (the critic side exists for the S5 route, not for a fold) | `P\agents\qa-case-critic.md:41-46` (dimension 2, 2b: `## Merge candidates`, `merge` -> `parametrise into one test: <ids>` -> `approve_with_concerns`). Nothing tells the critic how to judge a FOLDED case (survivor carries the Thens). Line :44 says "(... it merges the CASES)" while the code asserts "a merge changes no case" (`P\scripts\tests\test_case_merges.py:588`) — a wording contradiction, noted in §9. |
| 1d | "Paired slice in `references/`" | NOT DONE | `P\references\slices\qa-case-designer\artifact-contract.md` is generated from `P\references\artifact-contract.md`; the case section (`artifact-contract.md:56-69`) names `status` only as "moved to `Automated` by `qa-code-critic`" (:59-60) and the closed-list validator (:66-69); `Archived` is not described anywhere in `P\references\` as a CASE state (grep `(?i)Archived` over `P\references` -> 6 hits, all about the STORY flag `pipeline.json archived`: `artifact-contract-json.md:79`, `artifact-contract-results.md:87`, `brief-form.json:48`, `metrics-contract.md:24`, two slices). |
| 1e | Contract: `Archived` is a legal case status | DONE (enum only) | `P\scripts\validate_artifacts.py:76` `CASE_STATUS = {"Draft", "Review", "Approved", "Automated", "Blocked", "Archived"}`; :169-170 refuses others. No writer of the value exists (no package code writes `status: Archived`; `case_lifecycle.py:74` writes a REMOTE TMS `"archived": True` proposal, a different thing). |
| 1f | The one reader of a case's status | DONE (the reader exists) | `P\scripts\contract.py:3622-3637` `CASE_STATUS_RE`, `case_status(path)` (front matter only). Callers outside tests: `branch_accounting.py:1673` (`_case_records`), `case_stamp.py:534`, `check_delivery.py:820` (`_stamp_transition_reasons`). |
| 2a | `contract.case_files` / `case_index` skip or mark `Archived` | NOT DONE | `P\scripts\contract.py:3416-3446` `case_files` filters by `task` only; `:3680-3731` `case_index` entry = `{path, requirements, plan_row, version, case_id, area}` (:3723-3730) — no status field, no filter. The finding's line numbers (`:3024`, `:3303-3338`) have moved; the code they describe is unchanged. |
| 2b | `check_delivery._completeness` skips an `Archived` case (and the deleted-case sentence) | NOT DONE | `P\scripts\check_delivery.py:727-768`: `cases = C.case_index(artifacts)` (:733), `row_cases` (:756) takes every index entry; "plan ... is `automate` but no case names it as its plan row" (:758); "case ... is `automate` but is neither in automation-manifest tests[] nor in unresolved[]" (:766-767). The finding's `:637-649`/`:644` moved to these lines. |
| 2c | Gate A row cases skip `Archived` | NOT DONE | `P\scripts\controller.py:2431-2460` `_case_rows` (scope -> index -> plan_row, no status); `:2844-2867` `_row_cases`; `:3049-3051` "no case names this plan row in its front matter ..." (the finding's `:2625` moved here). |
| 2d | Tests for 2a-2c (fixture with an `Archived` case, survivor carries `covers`; control: `Archived` with no survivor -> finding) | NOT DONE | No test builds an `Archived` case against `check_delivery` or the controller. The only `Archived` fixtures are in `P\scripts\tests\test_case_merges.py:121-138, 324-329, 413-426` (the TQ1-27 S4 merge check) — and that file is in the `quarantine` section of `P\scripts\tests\test-layers.json` (:7394; section starts :7067). |
| 2e | (observed, not an item) the S4 merge check already treats `Archived` as retired | DONE (TQ1-27) | `P\scripts\critic_rollcall.py:1037` `live = {... if c["status"] != "Archived"}` (exact word, over-include); :859 form refusal "... or it is Archived"; `_budget_errors` (:1011-1027) counts live cases only. `case_stamp.py:535` skips `Blocked`/`Archived`. These are the ONLY two code readers of the value. |
| 3 | Order: Q1 before any live proof relying on folded cases | HOLDS (nothing folded yet) | The TQ1-27 live-proof row (`plans/piles/live-runs/batch-2-live-proofs.md:128`) proves the S5-concern route only, status «ожидает прогона». |
| 4a | `_has_note_column` removed; `parse_rollcall` gives `note=None` when the column is absent | NOT DONE | `P\scripts\critic_rollcall.py:836-839` `_has_note_column` still re-reads the roll-call header; called at :832, read at :990; `parse_rollcall` :136 gives `""` (not `None`) for a missing `note` column. |
| 4b | One helper "table column by name" for `parse_rollcall`, `parse_merge_candidates`, `_table_rows` | NOT DONE | Three own readers: `critic_rollcall.py:112-118` (`next(... enumerate ...)` per column), `:804-808` (`header.index(name)`), `P\scripts\branch_accounting.py:451-468` `_table_rows` (fixed-order header equality — a different contract, §8 C5). Siblings outside the finding: `planning_contract.py:1341, 1345, 2488-2489`, `audit_factory.py:748` (not widened, §9). |

**Verdict in three lines:** nothing of TQ2-1 has landed; what exists is the TQ1-27 S5-concern route (critic `merge` -> `approve_with_concerns` -> automator parametrises; "a merge changes no case") and two code readers that already treat `Archived` as retired. The designer has no fold rule and no fold form; `case_index` and every delivery reader do not know the status; the three header readers are still three. The node is NOT closable by an evidence row; the decision that made it "discussed but not done" is a standing Lead choice (TQ1-27 B-1, §2) that this node either reverses or confirms — fork F1.

### 1.2 Negative claims, each with its pattern and a positive control of the same shape

| Claim | Pattern / tool | Positive control (same tool, same flags) |
|---|---|---|
| No package code outside tests compares a CASE status to `Archived` except `case_stamp.py:535` and `critic_rollcall.py:1037` | Grep `["']archived["']` `-i` over `P\scripts` (output mode content) -> case-level hits only those two plus the enum `validate_artifacts.py:76`; all other hits are the story flag (`archive_task.py`, `factory_dashboard.py`, `stage_guard.py`, `window_budget.py`, `config_contract.py:2461`, `metrics_projection.py:517`, `log_append.py:65`, `case_lifecycle.py:74`) | the same query finds `case_stamp.py:535` and `critic_rollcall.py:1037` (known samples) |
| No reader of `case_index` knows the status | structural: the entry built at `contract.py:3723-3730` carries no status key, so no reader of the index CAN read it; Grep `case_status\b` over `P\scripts` -> 3 non-test callers (1.1 row 1f), none of them a `case_index` consumer except through its own `path` | the same Grep finds `contract.py:3626` (the definition) |
| No `merged_into` field anywhere | Grep `merged_into` over `P` -> only a test FUNCTION name `test_controller_gate_decision.py:576` (`identical_problems_are_merged_into_one_line`) | same Grep, pattern `parse_rollcall`, finds 5 files |
| Nothing in `changelog.d` mentions a case fold | Grep `archived\|merged_into` `-i` over `P\changelog.d` -> no match | Grep `artifact root\|artifact_root` `-i` over the same dir -> 15 hits in 10 files |
| No decision record on case merging | Grep `(?i)archived\|слия\|слит\|merge_candidates\|parametri[sz]\|параметри\|P16\|P17` over `DECISIONS.md` -> only :13 ("Archived so far: D-0004", decision archiving) ; over `docs/DECISIONS_ARCHIVE.md` -> only decision-archive headings (:8-206) | the same Grep finds `DECISIONS.md:13` |
| The plan critic t-715 and the diff critic t-756 reviews are not in this checkout | Glob `docs/tasks/**/t-7{15,36,56}*` -> none | Glob `docs/tasks/**/*tq1-27*` -> `docs/tasks/specs/t-723-tq1-27-amended.md` |
| No scenario `variants.json` exists yet | Glob `P\scripts\tests\fixtures\stories\**\variants*.json` -> none | Glob `...\stories\*\*.json` -> 9 files (`expected.json`, `pipeline.json`, `story.json` of three stories) |

### 1.3 AR-n invariants this change touches (designer rule 1), the change check each demands (carried into the DoDs), and the owner/census class of every check added or altered

| AR | How it is touched | Change check (DoD) |
|---|---|---|
| AR-13 (one reader per fact) | a case's retired state and its `merged_into` get ONE reader each (`contract.case_index` entry fields), one predicate `contract.case_retired`, one row map `contract.cases_by_plan_row`; every work-owing reader goes through them | critic confirms no reader in the diff reads `status:` or `merged_into:` text itself (Grep `merged_into\|"Archived"` over the diff lands only in `contract.py`, `validate_artifacts.py`, `branch_accounting.py`) |
| AR-22 (every field read has a producer, every field produced a reader) | producer: the designer (charter + contract doc); readers: N1-N3. Producer and readers land in ONE PR (fork F7) | N4 is merged last; before N4 no package text tells any role to write `merged_into` |
| AR-25 (every recorded state has a way out) | `Archived` becomes a state a role writes; its way out: the designer un-archives it in a rework round (status back to `Draft`, `merged_into` removed) | test row "un-archived case counts again" (N2 table) |
| AR-26 (requirements are the unit) | a fold must never lose a requirement's coverage | S4: survivor `covers` ⊇ absorbed `covers` (N3 fold check); S8: an R covered only by a retired case falls to the existing "requirement no case covers" road (`traceability.py:1232-1249` `caseless_plan_row`) — never a pass |
| AR-28 (an unknown never becomes a pass) | an unreadable status or `merged_into` reads as LIVE (the case keeps owing work) | test rows on the adversarial inputs of §5 (E10) |
| AR-15 / AR-19 (one survivor, twins together) | designer twin of the critic's 2b; the one column helper | N4 changes both charters in one commit; N5 one helper, three callers |
| AR-29 (code judges data, roles judge meaning) | WHETHER two cases are one form stays the designer's and the case critic's; code checks only that the fold kept the data | census rows below |
| AR-20 (shrink-only ratchets) | `judgment-census.json` `ratchet.blocking_per_role` (`qa-case-critic`: 164) and `role-load.json` `process_ratchet_tokens` may rise | any raise is NAMED in the critic verdict and the commit message (forks F5, F11) |

Checks added or altered, with owner and census class (`P\scripts\tests\fixtures\judgment-census.json` classes: shape, xref, word-list, meaning-proxy, meaning, safety):

| Check | Where | Owner it serves | Census class |
|---|---|---|---|
| fold integrity: `merged_into` names a live case of this story; survivor `covers` ⊇ absorbed; survivor `branches` ids ⊇ absorbed; survivor `then_oracles` refs ⊇ absorbed (F8); same plan-row level and same `channel` (F4) | new `branch_accounting._fold_problems`, called by `s4_problems` | data (code) | xref |
| does the survivor's Then TEXT really carry the absorbed case's checks; were the two cases one form | case critic charter 2b (judgment), accepted by the tier above (gate A / Lead acceptance of the run) | judgment | not a code unit |
| whether to fold at all | designer charter (judgment), the critic reviews it | judgment | not a code unit |
| retired cases owe no work in delivery readers | `contract.case_retired` used by N2/N3 readers | data | xref (on rows that already exist: `_completeness`, `lifecycle_reasons`, ...; no new refusal sentence except E7) |
| `Archived` beside a green test names the contradiction | `check_delivery._stamp_transition_reasons` (altered sentence) | data | shape (existing row) |

---

## 2. Where this was discussed before, and why it did not land

| # | Carrier (path) | Date | What was decided | Why the fold did not land |
|---|---|---|---|---|
| H1 | `PROJECT.md` P16, P17 (owner, 30.09 and 04.11.2026) | 30.09 | "cases merge (parametrisation, several checks in one scenario)"; "-1, 0, 1.5, «абв» — ONE test with parameters, not four cases"; P17: the automator decides HOW, many-to-many | principle only; no carrier gave the designer a fold |
| H2 | `plans/piles/roles-context/README.md:63` (B-188) -> `plans/piles/roles-context/batch-1-role-texts.md:39` RC1-2 -> moved 01.11 to `plans/piles/onboarding-forge/batch-1-onboarding-roles-forge.md:44` | 30.09 -> 01.11 | "P16 into the charters of strategist, designer and critics" | RC1-2 is still «ожидает» inside a batch that is «в работе» (dev1, 12.11, `batch-1-onboarding-roles-forge.md:3`): the designer line never landed. This is the SAME charter line as item 1a — an overlap (§9, queue line) |
| H3 | `plans/piles/roles-context/findings/B-191-p17-glavnaya-logika-keysy.md` | 30.09 | P17 alignment: many-to-many, parametrise, consolidate; S5 code checks only Then binding completeness | addressed the S5 side (tests), not cases |
| H4 | `plans/piles/hotfix-12586/findings/20261028-s5-odin-kejs-odin-test.md` (spec `docs/tasks/specs/t-1502-test-grouping.md`) | 28.10 | owner "Да, в 0.10.5": one grouping rule for the automator, `fit: new` += `parameterize` | the S5 side again: fewer TESTS, the case count unchanged |
| H5 | `plans/piles/release-next/findings/20261030-kritik-kejsov-ne-ishchet-dubli-i-sliyaniya-p16.md` | 30.10 | owner: "лишние кейсы были, потолок не двигать" (12 cases, honest minimum 9). Lead's direction there: the critic writes `merge_candidates`; "`merge` without the designer's rework — refusal" (item 3 of «Что именно менять», :40-43) | the next step reversed exactly this rework (H6) |
| H6 | `docs/tasks/specs/t-723-tq1-27-amended.md` §0 :16-19, AR-25 :58-60, B-1 :376, (2) :379, L1 :387-392 (closing the plan critic t-715 B-1) | 02.11 | **Lead, B-1: "a `merge` changes no case"**: the merge rides to S5 as a concern; "No `Archived` status is written, no case is deleted"; AR-25 kept "by NOT introducing `Archived`"; the fold + delivery readers = queued node Q1 (L1) | THIS is where it stopped: the case-count reduction the owner asked for in H5 became a test-count reduction; the fold was queued as Q1 = TQ2-1, which nobody took (batch 2 «ожидает» since 02.11, `batch-2-...md:3`) |
| H7 | `plans/piles/test-code-quality/findings/20261102-...shapki.md` + `batch-2-sliyanie-kejsov-i-chitateli.md:25` | 02.11 | TQ2-1 opened; direction chosen by Lead release-next/1; "Решение владельца нужно: нет" | not taken; the batch brief also says "НЕ делать: новые правила критика кейсов (TQ1-27 уже внёс)" (`batch-2-...md:16`) while the finding says the critic's paired cut is "обязательный" (:21) — a contradiction (fork F9) |
| H8 | `plans/piles/roles-context/findings/20261112-razdely-masterstva-nesut-stroki-procedury-p27.md` | 12.11 | the critic charter's fixed tokens (`parametrise into one test:`, `## Merge candidates`) are PROCEDURE sitting under `kind: craft`; they move to a `process` section | same file (`agents/qa-case-critic.md`) as N4; order needed (§9) |
| H9 | `docs/DECISIONS_ARCHIVE.md`, `DECISIONS.md` | — | nothing on case merging (§1.2) | the choice lives only in spec t-723 and the batch files — no D-nnnn ever recorded the B-1 trade-off |

Why it keeps "not landing", in one line: each pass solved the cheaper half (tests merge at S5) and queued the case half behind a node that needs the designer charter, a new case state and ~25 readers at once; the B-1 choice that the case count stays was a Lead call, never put to the owner, while the owner's 30.10 answer was about the case count.

---

## 3. What the remainder is (if F1 = build)

1. The designer folds: a rule (craft) "one form, branches as parameters" and a form (process): the absorbed case keeps its file, gets `status: Archived` and `merged_into: <survivor id>`; the survivor takes the absorbed case's Thens, `covers`, `branches` and its plan row's binding.
2. The data stays whole by code at the S4 exit (fold integrity, §1.3).
3. Every reader that OWES work per case stops owing it for a retired case; every reader that RESOLVES a case it was handed keeps finding it.
4. The case critic judges the fold (paired cut, 2b).
5. The three header readers become one helper (independent of 1-4).

What is NOT part of the remainder (with reason): the TQ1-27 S5-concern route stays as it is (F2 keeps it as the road when the designer did not fold); a REMOTE TMS archive keeps its one road, `case_lifecycle.prepare_archive` with a gate B decision (`P\scripts\case_lifecycle.py:60-80`) — a different action (retiring a published case), not a second road for the same action (P31).

---

## 4. Design

### 4.1 Data (the fold form)

- Absorbed case file: front matter `status: Archived` (exact word, unquoted — `contract.case_status` reads `\S+`, so `"Archived"` is a different word and stays LIVE, E10) and `merged_into: <case id>` in the project's id form (`<area>/<id>` when two areas hold the number). The body is left as it was (history; a pinned story keeps its versions through `story_case_links`). The file is NEVER deleted.
- Survivor: its own plan row line stays; it lists the absorbed case's requirements in `covers` (and the `Requirements:` line), carries every absorbed `branches` entry (renumbered `then` to the survivor's Then that proves it), carries the absorbed `then_oracles` refs, and gives the absorbed partitions as parameters (`P-<name>`).
- Un-archive: `status` back to `Draft`, `merged_into` removed; the survivor drops what it took. Nothing else.

### 4.2 Contract helpers (N1, `P\scripts\contract.py`, functions disjoint from the in-flight `_binding_stamp_allowed`, `stamp_obligation_refs`, `binding_currency*`)

- `CASE_ARCHIVED = "Archived"` beside `CASE_AUTOMATED` (:3623).
- `case_index` (:3680): each entry gains `"status": case_status(path)` and `"merged_into": <front_line(text, "merged_into") stripped of quotes, or "">`. The index still holds EVERY case (resolving readers unchanged).
- `_case_ran(case, manifest, report) -> bool`: the body of `case_set_aside` lines :3036-3046 moved out unchanged (a result, an impossible row, a manifest test or unresolved link under either spelling). `case_set_aside` calls it (behaviour unchanged).
- `case_retired(key, entry, manifest=None, report=None) -> bool`: True ONLY when `entry["status"] == CASE_ARCHIVED` AND not `_case_ran(key, manifest, report)` (both default to `{}`: at S4 nothing ran). Error direction: toward LIVE (§5.2).
- `live_cases(index, manifest=None, report=None) -> CaseIndex`: a new `CaseIndex` (same `_cfg`) without retired entries, keys unchanged.
- `cases_by_plan_row(index, manifest=None, report=None) -> dict[str, list[str]]`: `{plan_row: [keys]}` over live entries; for each RETIRED entry with a non-empty `merged_into` that resolves (through `scope_member_resolution([merged_into], index)`) to exactly one LIVE key, that survivor key is added under the RETIRED entry's plan row (one hop; no chains). Order: index order, no duplicates.

### 4.3 Readers (N2 delivery, N3 S4/S5/gate A)

The rule that classifies a reader (written so no builder chooses): a reader is WORK-OWING when it builds a set, map, count, list or table of the story's cases to DEMAND, COUNT or SHOW as owed work; it then reads `live_cases(...)` and, where it groups by plan row, `cases_by_plan_row(...)`. A reader is RESOLVING when it looks up one case it was handed by id (a manifest row, a bug, a scope member, a CLI argument); it keeps the full `case_index`. The classification of every caller is in §6 (N2, N3 tables); a caller whose shape on reading is NOT what the table says is returned as a question, never reclassified by the builder.

### 4.4 The S4 fold check (N3, `branch_accounting.py`)

`_fold_problems(task_root, cases) -> list` called from `s4_problems` (:1734) after `cases` is read; `cases` there and in `s5_problems` (:1921) and `_branch_records` (:2324) exclude retired records (status exactly `Archived`; nothing ran at S4/S5 entry for the S4 exit — the S5 exit and `_branch_records` pass manifest/report through `case_retired`). For every record with status exactly `Archived`:
1. `merged_into` empty -> no fold problem (another flow archived it); its branches are simply not carried by it any more (the existing "branch has no home" refusal of `s4_problems` speaks, :1751-1760).
2. `merged_into` names no case of this story, names itself, names a retired case, or names several keys -> problem naming the case and the form `merged_into: <live case id of this story>`.
3. survivor `covers` lacks an R of the absorbed `covers` -> problem naming the Rs.
4. survivor `branches` lacks an absorbed branch id -> problem naming the ids.
5. survivor `then_oracles` refs lack an absorbed ref (F8) -> problem naming the refs.
6. plan-row level differs (`contract.plan_levels`) or `channel` differs -> problem naming both values (F4).
Every problem's door: "send the designer back: `--operation rework --stage S4 --role qa-case-designer --cases <ids> --reason \"<why>\" --brief`, or answer the pair `keep`" — the same door text `controller.py:3073-3078` uses. Problems obey the existing `limit("refusal_units_shown")` cut.

### 4.5 Charters and contract text (N4)

- Designer `## Techniques` (craft): one line — "One form, branches as parameters: two cases that differ only by a branch of the same Given/When are one case whose partitions are the parameters; keep them apart only when one red line could not tell the branches apart (P16) or they need different levels (P19)."
- Designer `## Tools` (process): one line — "Folding an existing case: keep its file, set `status: Archived` and `merged_into: <survivor id>`; the survivor takes its Thens, `covers`, `branches` and partitions; never delete a case file." Item 1 of `## Good outcome` (:23) gains "or folded into another (`merged_into`)".
- Critic 2b: one sentence — "A case `Archived` with `merged_into`: read the survivor; every Then of the absorbed case is a Then or a parameter of the survivor, or it is a `fail` 'fold lost Then n of TC-x'."
- `references/artifact-contract.md` case section: `status` closed list and the meaning of `Archived` + `merged_into`; regenerate slices.
- `design/role-rules.json`: three registry rows (designer craft line, designer fold form, critic fold judgment) — the rule guard of `docs/TESTING.md` «Правила ролей не теряются», not pin tests.

---

## 5. Edges, each with the invariant it protects

### 5.1 Edge table

| # | Edge | Behaviour | Invariant protected |
|---|---|---|---|
| E1 | Merge of cases on DIFFERENT levels (plan rows with different `level`) | S4 fold check refuses (F4); the critic's `keep` with P19 is the road | one parametrised case runs at one level: a fold never silently drops a level the strategist chose (P19) |
| E2 | Merge of cases with different `channel` | same refusal as E1 | a survivor's single test cannot run on two channels; a check must not vanish because its channel was overwritten |
| E3 | Fold across plan rows (the common case: 12586's three calibration merges are all cross-row, t-723 :31) | the absorbed row's cases ARE its retired cases' survivors (`cases_by_plan_row`); `_completeness` (:756), gate A `_row_cases`, ledger, traceability use that map | an `automate` row never loses its case: "no case names it as its plan row" stays reachable only when no live case and no fold stands for the row |
| E4 | Survivor ALREADY has the Then (the absorbed Then duplicates one of its own) | allowed: the check is on `branches` ids, `covers` and `then_oracles` refs as SETS; a duplicate Then is not demanded twice | no Then is lost; no Then is forced to repeat (AR-29: whether the two Thens are the same check is the critic's) |
| E5 | `Archived` case named by a manifest test row | `_case_ran` -> True -> NOT retired: counted everywhere as before | a case that a test proves or that ran is never hidden (the `case_set_aside` direction, `contract.py:3031-3032`) |
| E6 | `Archived` case named by a manifest `unresolved[]` row | same as E5: not retired; the unresolved reason stands | an open reason on a case never disappears with the case |
| E7 | `Archived` case beside an APPROVED GREEN test (`lifecycle_reasons`) | the case is live (E5); `case_stamp` refuses to stamp `Archived` (:535), so `_stamp_transition_reasons` (:818) says: "case X is `Archived` (merged into Y) but test T still proves it — drop X from the test's `covers`/`case`, or un-archive X" instead of "the Draft -> Automated transition never happened" | the person sees the true contradiction; no permanent block with a wrong door (FR-1, FR-2) |
| E8 | `Archived` case named by a bug record | bug readers resolve through the FULL `case_index` (`bug_neighbours.py:246`, `traceability.Story.bug_for`), so the bug keeps its case | a filed bug never loses its case reference (AR-27) |
| E9 | `Archived` case named by a plan row's `required_scenarios` (gate A fallback, `controller.py:2861-2866`) | `_row_cases` first adds fold survivors for the row (§6 N3); the `required_scenarios` fallback runs only when the row still has no case; a fallback name that is a retired case is replaced by its survivor | gate A binds the design review to the case that will be tested, never to a retired version |
| E10 | Adversarial status/field inputs: `status: "Archived"` (quoted), `status: archived` (lower), `status:` only in the body, BOM before `---`, `merged_into:` empty, naming itself, naming a missing id, naming a retired case (chain), naming two ids, naming `<area>/TC-n` of another area | quoted/lower/body-only -> LIVE (exact word only); BOM -> read as front matter (as `case_status` does today, K0 of t-723); empty -> no fold (rule 1 of 4.4); self/missing/chain/two -> S4 problem (rule 2); at S8 a fold that does not resolve to ONE live key adds nothing to the row (E3 map) | unknown never becomes a pass (AR-28): every unreadable form keeps the case owing work or refuses at S4 |
| E11 | TEMPORAL — a story written before this change (no `merged_into` anywhere) | `case_index` gains two fields, `live_cases` returns every case, `cases_by_plan_row` equals the old per-reader maps: delivery verdicts unchanged. The move that creates the new world is N4 (the charter line); before N4 no role writes `merged_into` | old stories keep their verdicts byte for byte (test row "no Archived" in the N2 table) |
| E12 | TEMPORAL — an old story with `status: Archived` written by a person (legal since `validate_artifacts.py:76`) and no `merged_into` | after N2 that case owes no work unless it ran (E5); its row may become caseless -> the existing "no case names it as its plan row" reason (was: "case X is `automate` but neither in tests[] nor unresolved[]"); both say `no` | the verdict direction never flips to `yes` from the change; only the sentence changes |
| E13 | A case DELETED instead of archived | unchanged: `_completeness` :758 "no case names it as its plan row"; at S4 its branches lose their carrier -> "branch has no home" | a merged case never vanishes silently: deletion keeps refusing |
| E14 | `Archived` set on a case of ANOTHER story in a shared store | not visible to this story (`case_files` selects by `task`, :3446); the charter line says "fold only cases this story wrote"; a pinned other story keeps its pinned versions | a fold never changes another story's coverage |
| E15 | Scope and S5 window: an archived case is pinned (history) | `case_versions._scope_plan` (:455) and `review_scope` (:582) take pinned keys minus retired ones; the archived file stays pinned | the automator is never handed a retired case; the pin history is never cut |
| E16 | Older critic rounds name the archived case in `## Merge candidates` | unchanged TQ1-27 behaviour: `_answers` reads live ids only (:886), newest round naming it is a form refusal (:858-860) | a stale merge row never revives a retired case |
| E17 | The fold row limit: more fold problems than `refusal_units_shown` | first N, then the existing "N more ..." tail line, as `_owed_pair_errors` (:908-910) | a truncation never hides that problems remain |
| E18 | The un-archived case | `status` no longer `Archived` -> live everywhere; the survivor's extra `covers` is harmless (it may still cover them) | AR-25: the state has a way out |
| E19 | Conflict of requirements: "one case per plan row" (designer :23) vs a fold across rows | resolved by the charter edit of 4.5 (item 1 names the fold) and by E3 | no rule of the charter contradicts another |
| E20 | Conflict: the S5-concern route (TQ1-27) and a designer fold on the same pair | after the fold the absorbed case is retired; the critic's next round lists only the survivor; an older `approve_with_concerns` for the absorbed case lands in no S5 window (E15) | one pair is executed once: as a fold, or as an S5 parametrisation, never both counted |

### 5.2 A reused function in a more consequential role (designer rule 1)

`contract.case_set_aside`'s "did the case run" body (`_case_ran`) moves from "a row is set aside in the traceability table" (advice in a table) to "a case owes no delivery work" (a gate input).
**Direction it may err in:** only toward LIVE (counting a retired case as owing work -> a `no` too many). It must never err toward RETIRED for a case that ran.
**Adversarial inputs that must stay on the safe side (each a table row in N2):** an area case `web/TC-002` linked by a manifest test under the bare id `TC-002`; linked only under the area spelling; a `run-report` result with no manifest row; a `run_impossible` entry only; an `unresolved[]` row marked stale; a manifest test whose `covers[]` (not `case`) names the archived case; `status: Archived` on the pinned version but `Draft` on the authoring copy (the pinned version decides — `case_files` returns pinned paths, :3427-3437).

`contract.scope_member_resolution` (:3734) is reused to resolve `merged_into`; its own error direction is REFUSAL (nothing widened, :3742-3743) — kept: an unresolvable `merged_into` adds no survivor (E3) and refuses at S4 (E10).

---

## 6. Nodes for the remainder (if F1 = build)

Order: N1 -> N2 -> N3 -> N4 on ONE branch, one PR (F7); N5 is independent and may run in parallel (disjoint owns). Hot files: `controller.py` (D-0048 list) — N3 names its functions; `contract.py` in flight by another node — N1 names its functions, disjoint from `_binding_stamp_allowed`, `stamp_obligation_refs`, `binding_currency*`. Every builder dispatch carries in `given` the whole `P\design\factory-rules.md` and `C:\QAFactory\forge-repo\plans\builder-rules.md` (PROJECT.md, package change item 1).

### N1 — contract: status and fold in the index, one predicate, one row map

given: this spec §4.2, §5; P\scripts\contract.py (functions below); P\design\factory-rules.md (whole); C:\QAFactory\forge-repo\plans\builder-rules.md; C:\QAFactory\forge-repo\docs\TESTING.md
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\contract.py (functions: `case_index`, `case_set_aside`; new: `CASE_ARCHIVED`, `_case_ran`, `case_retired`, `live_cases`, `cases_by_plan_row`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_check_delivery.py (one new parameterised table `RETIRED_CASES` and its runner function)
non-goals: any reader outside contract.py; `_binding_stamp_allowed`, `stamp_obligation_refs`, `binding_currency*`; any charter; quarantined files (`test_contract.py`, `test_case_merges.py`)
handoff: builder report path given by the Lead's dispatch
edges: §5.2 (all seven adversarial inputs), E10, E11
DoD: `python -B C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\scenario_walk.py --witness-for C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\contract.py` and the tests it prints, green; acceptance keys: (1) `case_index` entries carry `status` and `merged_into`; (2) `case_set_aside` behaviour unchanged (its existing rows green); (3) `RETIRED_CASES` rows: each §5.2 input -> `case_retired` False; `Archived` + nothing ran -> True; quoted/lower/body-only -> False; `cases_by_plan_row` with a cross-row fold -> survivor under both rows; chain / self / two ids / missing -> nothing added; no-Archived story -> map equal to the plain per-row grouping
siblings: `case_set_aside` (same "never hide what ran" direction) — reused, not duplicated
designer: this file

Expected behaviour per function: as §4.2, with the exact return shapes written there. Test rows: one table, one runner, ids naming the input (P16).

### N2 — delivery readers know a retired case

given: this spec §4.3, §5, the table below; the files below
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\check_delivery.py (functions: `_case_map`, `_completeness`, `_stamp_transition_reasons`, `lifecycle_reasons`, `person_check_rows`, `handed_plan_rows`, `gather`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\ledger.py (function: `build`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\traceability.py (functions: `case_oracles`, `Story.__init__`, `check`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\check_traceability.py (function: `walk`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\validate_artifacts.py (the functions holding lines 1267, 2106, 2157 — `check_manifest_v0` and its two neighbours)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\delivery_summary.py (function: `_manual_plan_count`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\coverage_contract.py (function: `_oracle_context`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\report_facts.py (the functions holding lines 283, 1342, 2055)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_check_delivery.py (rows in `RETIRED_CASES`)
non-goals: contract.py; controller.py; resolving readers (table below, column R); TMS publication (`planning_contract.publication_manifest`); any charter
handoff: builder report path given by the Lead's dispatch
edges: E3, E5, E6, E7, E8, E11, E12, E13, E18
DoD: `python -B C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\scenario_walk.py --witness-for <every owns path above>` and the tests it prints, green; acceptance keys (rows of `RETIRED_CASES`, each through `check_delivery.assess` or `completeness_reasons`/`lifecycle_reasons` on a temp story): (a) cross-row fold, survivor tested -> no completeness reason for either row; (b) `Archived` with no survivor and its R covered by no live case -> the R is a gap (not `yes`); (c) `Archived` linked by a manifest test -> counted as before; (d) `Archived` + approved green test -> the E7 sentence; (e) no `Archived` anywhere -> reasons equal to the pre-change run on the same story; (f) un-archived -> counted again; (g) deleted case -> "no case names it as its plan row"
siblings: SIBLING_MAP axis of case readers — every work-owing reader in the table; the S4/S5 readers are N3 (same class, one PR)
designer: this file

| Caller (file:line) | Class | Change |
|---|---|---|
| `check_delivery.py:409` `_case_map` | W | `cases` from `live_cases(index, manifest, report)`; `plan_rows` from `cases_by_plan_row` |
| `check_delivery.py:733,756` `_completeness` | W | `row_cases` = `cases_by_plan_row(cases, manifest)[row["ts"]]` |
| `check_delivery.py:820,845` `_stamp_transition_reasons`, `lifecycle_reasons` | W | E7 sentence when status is `Archived` |
| `check_delivery.py:1015` `person_check_rows` | W | iterate `live_cases` |
| `check_delivery.py:1291` `gather` | W | `"index": live_cases(index, manifest, report)` (read manifest and report before the index); a resolving consumer of `facts["index"]` found on reading -> question |
| `check_delivery.py:1674` `handed_plan_rows` | W | `cases_by_plan_row` |
| `ledger.py:1582` `build` | W | `cases_by_row` from `cases_by_plan_row(cases, manifest, report)` |
| `traceability.py:419` `case_oracles`; `:453` `Story.__init__`; `:1754` `check` | W | `live_cases(..., manifest, report)`; `check` groups by `cases_by_plan_row` |
| `check_traceability.py:173` `walk` | W | `live_cases` |
| `validate_artifacts.py:1267, 2106, 2157` | W | `live_cases` (an appendix need not name a retired case; a manifest need not test one) |
| `delivery_summary.py:142` `_manual_plan_count` | W | `live_cases` |
| `coverage_contract.py:491` `_oracle_context` | W | `live_cases` |
| `report_facts.py:283, 1342, 2055` | W | `live_cases` |
| `bug_neighbours.py:246`, `manual_evidence.py:802, 1005, 1224`, `investigation.py:145`, `story_step.py:2762`, `s5_precheck.py:527, 545`, `s5_plan.py:243`, `manifest_from_tests.py:680`, `execution_request.py:1127`, `case_stamp.py:507`, `contract.py:2103` (`case_levels`), `factory_dashboard.py:679, 1109` (display, already reads front matter incl. status) | R | none |

### N3 — S4/S5/gate A readers and the fold check

given: this spec §4.3, §4.4, §5, the table below
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\branch_accounting.py (functions: `_case_records` (adds `merged_into`, `then_refs`), `s4_problems`, `s5_problems`, `_branch_records`; new `_fold_problems`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\case_versions.py (functions: `_scope_plan`, `review_scope`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\controller.py (functions: `_row_cases` only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\gate_preflight.py (functions: `plan_rows_of`, `default_login_needed`; the callers at :1370, :2030, :2067, :4707, :4886, :5518 per the table)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\planning_contract.py (the function holding line 2240 only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\stand_gaps.py (functions: `_case_texts`, `_case_context`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\driver_stage_plan.py (function: `unraised_cases`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json (one row for `_fold_problems`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_branch_accounting.py (one parameterised table `FOLDS`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_controller_gate_decision.py (one row: cross-row fold, design review bound to the survivor's pinned version)
non-goals: `controller._case_rows` (its case -> row shape is read by `stage_scope`; unchanged), any other controller function, `critic_rollcall.py` (TQ1-27 already filters), charters
handoff: builder report path given by the Lead's dispatch
edges: E1, E2, E3, E9, E10, E15, E16, E17, E20
DoD: `python -B C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\scenario_walk.py --witness-for <every owns path above>` and the tests it prints, green; acceptance keys (`FOLDS` rows through `s4_problems`): clean fold -> no problem; survivor lacks an R / a branch / a then_oracles ref -> one problem naming it; level differs / channel differs -> problem naming both values; `merged_into` self / missing / chain / two ids -> problem with the form; `Archived` without `merged_into` and its branch carried by nobody -> the existing "no home" refusal; problems over `refusal_units_shown` -> N + tail line; gate A row: absorbed row TS-3 reviewed against the survivor's version, not the archived one; census row present, `test_judgment_census.py` green with the named raise (F5)
siblings: `critic_rollcall.merge_candidate_errors` (:1037, already live-only), `case_stamp.py:535` (already skips)
designer: this file

| Caller (file:line) | Class | Change |
|---|---|---|
| `branch_accounting.py:1742` `s4_problems` | W | live records + `_fold_problems` |
| `branch_accounting.py:1921` `s5_problems`, `:2324` `_branch_records` | W | `case_retired` with manifest/report |
| `case_versions.py:455` `_scope_plan`, `:582` `review_scope` | W | pinned keys minus retired (status read through `case_index`) |
| `controller.py:2844` `_row_cases` | W | after the scope mapping, add `cases_by_plan_row(index)` survivors that are in scope; then the `required_scenarios` fallback, with a retired name replaced by its survivor (E9) |
| `gate_preflight.py:664` `plan_rows_of`, `:705` `default_login_needed`, `:4886` | W | `live_cases` |
| `gate_preflight.py:1370, 2030, 2067, 4707, 5518` (`case_files` callers) | W | skip a path whose `case_status` is `Archived` (these read preconditions/env needs of cases that will run) — if the reading shows otherwise, a question |
| `gate_preflight.py:2336, 4928, 5053` | R | none |
| `planning_contract.py:2240` | W | `cases_by_plan_row` |
| `stand_gaps.py:67` `_case_texts`, `:548` `_case_context` | W | live only |
| `driver_stage_plan.py:880` `unraised_cases` | W | skip `Archived` paths (a retired case's `raise` asks no question) |
| `driver_stage_s6.py:912` | W via scope | none (filtered by `state["scope"]`, which N3 makes retired-free) |
| `driver_stage_s6.py:836, 1124`, `brief_pack.py:1264`, `env_probe.py:763`, `repo_map.py:423`, `gate_brief.case_files` (own function) | R / verify | the builder reads each; a WORK-OWING shape found -> question to the Lead, not a fix |

### N4 — the producer: charters, contract text, registry rows (merged LAST)

given: this spec §4.1, §4.5; P\agents\qa-case-designer.md; P\agents\qa-case-critic.md; P\references\artifact-contract.md; P\design\role-rules.json; P\references\role-load.json
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\agents\qa-case-designer.md
C:\QAFactory\forge-repo\ai-packages\qa-factory\agents\qa-case-critic.md (dimension 2b only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\artifact-contract.md (case section only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\slices\ (regenerated by `python -B scripts/contract_slices.py --write`, not hand-edited)
C:\QAFactory\forge-repo\ai-packages\qa-factory\design\role-rules.json (three rows)
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\role-load.json (only if the measured process share rises — named raise, F11)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\tq2-1-case-fold.md (new fragment, English)
non-goals: any script; the critic charter's other dimensions; moving the critic's fixed tokens (roles-context H8)
handoff: builder report path given by the Lead's dispatch
edges: E11 (this node creates the new world), E14, E19, E20; FR-30 (no Cyrillic: `selftest.py --lang` on the touched files)
DoD: `python -B C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\scenario_walk.py --witness-for <every owns path above>` and the tests it prints (it prints `test_role_rules.py` for `role-rules.json`), green; `python -B C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\contract_slices.py --check` exit 0; `python -B C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\role_load.py --all --json` verdict `within` for both roles (before/after attached)
siblings: RC1-2 (`onboarding-forge/1`, the same designer P16 line) — queue line §9
designer: this file

### N5 — one table-column helper (independent)

given: this spec §1.1 rows 4a-4b, §8 C5
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\contract.py (new function `md_column` only, beside `md_table` :2845)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\critic_rollcall.py (functions: `parse_rollcall`, `parse_merge_candidates`, `_read_rounds`, `_level_errors`; delete `_has_note_column`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_critic_rollcall_apply_fixes.py (one table row: roll-call with no `note` column)
non-goals: `branch_accounting._table_rows` (§8 C5); `planning_contract.py`, `audit_factory.py` siblings (queued, §9)
handoff: builder report path given by the Lead's dispatch
edges: header cell with backticks or spaces (`  ` `note` `  `) -> found; two columns of the same name -> the first; a name that is a prefix of another (`case` vs `cases`) -> `md_column` matches EXACTLY; `parse_rollcall`'s `case` column keeps its `startswith("case")` rule (a caller-side choice kept as is), `reviewed` its `"reviewed" in name` rule
DoD: `python -B C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\scenario_walk.py --witness-for C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\critic_rollcall.py C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\contract.py` and the tests it prints, green; keys: `md_column(header, name) -> int | None` (cells stripped, backticks off, lower case, exact); `parse_rollcall` row `note` is `None` when the column is absent, the cell text otherwise; `_read_rounds` sets `note_col` from `parse_rollcall` rows (`any(row["note"] is not None ...)` or, for a table with no rows, from `md_column`); `_level_errors` unchanged in behaviour; `parse_merge_candidates` finds columns by `md_column` with its `bad_header` sentence unchanged; `_has_note_column` gone (Grep finds no caller); every reader of `row["note"]` that did `or ""` keeps working with `None` (the builder greps `["note"]` in critic_rollcall.py and `carried_concerns` callers and lists them)
siblings: `planning_contract.py:1341, 1345, 2488`, `audit_factory.py:748` — queued, not widened
designer: this file

---

## 7. Forks (returned, not decided)

| # | Fork | Options | Recommendation and cost |
|---|---|---|---|
| F1 | Is a designer-side fold wanted at all? Lead's B-1 (t-723, 02.11) chose "a merge changes no case" and queued the fold; the owner's 30.10 answer was "лишние кейсы были" (the case count) | (a) build N1-N4 (cases really fold; case count drops; budget check `_budget_errors` already counts live cases); (b) close the fold half as superseded by the S5 route and keep only N5 + a reader-hardening node (N1+N2 without a producer: AR-22 breach — a state read with no producer); (c) build only the designer's PROACTIVE rule (write one case instead of two at first draft, no `Archived` at all) | **(a)** — it is what P16 says ("ONE test with parameters, not four cases") and what the owner measured; (c) is a cheap subset that needs no state, but leaves every rework-round fold unexecutable. Owner question: this reverses a Lead decision; cost ~4 builder nodes + 1 critic pass |
| F2 | What triggers a fold | (a) the designer folds proactively and in ANY rework round folds the pairs the critic answered `merge`; the critic's `merge` keeps riding to S5 when no fold happened (no new round forced); (b) a critic `merge` forces a designer rework round (t-697's original, reversed by B-1) | **(a)** — no extra round per story (the B-1 cost argument stays true), the S5 route is the safety net (E20) |
| F3 | A fold across plan rows | (a) `merged_into` maps the absorbed row to the survivor (E3, `cases_by_plan_row`); (b) folds only inside one plan row (code refuses cross-row); (c) a survivor names several plan rows | **(a)** — all three 12586 calibration merges are cross-row; (b) forbids the measured case; (c) breaks `CASE_PLAN_ROW_RE` (one row) and its ~10 readers |
| F4 | Fold across different plan-row level or `channel` | (a) code refuses (data mismatch, §4.4 rule 6); (b) left to the critic | **(a)** — field equality is data (AR-29), and a parametrised test has one level; the door is `keep` with P19 |
| F5 | Census: the fold check as a new unit | (a) new `_fold_problems` with a census row (xref, data) and a NAMED raise of `blocking_per_role["qa-case-critic"]` 164 -> 165 (AR-20); (b) inline in `s4_problems` (no new unit, a longer function) | **(a)** — one unit per check; the raise is named in the verdict and the commit |
| F6 | The fold pointer | (a) new front-matter field `merged_into`; (b) reuse `reuse_decision: dedupe:<id>` | **(a)** — `dedupe:` already means "an existing project case covers this row" and `branch-accounting.json` `reused_decisions` treats it as reused (homes, `branch_accounting.py:1770`); one word, two meanings is the defect class AR-13 names |
| F7 | One commit for producer and readers (AR-22) | (a) N1-N4 sequential on one batch branch, one PR, N4 last; (b) one builder writes all four | **(a)** — readers before the producer are inert (nothing writes `merged_into` until N4); one PR keeps AR-22 at the merge boundary; four smaller witnesses |
| F8 | "Code refuses a merge that drops a Then" | (a) code checks `then_oracles` refs ⊇ and `branches` ids ⊇ (data forms of the Thens); the Then TEXT is the critic's; (b) code checks nothing about Thens, critic only | **(a)** — the brief asks code to refuse a dropped Then; the structured refs are the only data form of a Then code may read (FR-12) |
| F9 | The batch brief forbids new case-critic rules ("НЕ делать: новые правила критика кейсов", `batch-2-...md:16`) while the finding makes the critic's paired cut obligatory (:21) | (a) allow ONE critic sentence (fold judgment, 4.5); (b) no critic line (the fold's Then text unjudged) | **(a)** — without it the judgment half of AR-29 has no owner |
| F10 | Home of the column helper | (a) `contract.md_column` beside `md_table`; (b) `critic_rollcall.column_index` (the finding's text) | **(a)** — the readers of `md_table` output live in several modules (siblings §9); one survivor where the table reader lives (AR-15) |
| F11 | Charter growth | the two designer lines and one critic sentence raise bytes; the fold FORM line is process | name any `role-load.json` `process_ratchet_tokens` raise (AR-20) or cut the same bytes from repeats — Lead's call; recommend the named raise |

## 8. Small technical choices closed here

- C1: the exact word `Archived`, unquoted, is the only retired value (as TQ1-27 E7 already does; one rule for both readers).
- C2: `case_retired`'s "ran" test is `case_set_aside`'s body, moved, not copied (clone ratchet).
- C3: `cases_by_plan_row` follows ONE hop; chains are refused at S4 and add nothing at S8.
- C4: test homes are existing keep files (`test_check_delivery.py`, `test_branch_accounting.py`, `test_controller_gate_decision.py`, `test_critic_rollcall_apply_fixes.py`, `test_role_rules.py` via the registry); no new test file; the quarantined `test_case_merges.py` / `test_contract.py` are not touched (docs/TESTING.md).
- C5: `branch_accounting._table_rows` stays out of the column helper: it checks the header EQUALS a fixed column tuple and keeps every `|` in the last cell (`:451-468`) — a positional contract, not "column by name"; the finding's inclusion of it is closed as not applicable for that reason.
- C6: the E7 sentence wording is fixed in §5.1.
- C7: `case_index` keeps every case; filtering is done by readers through `live_cases` (filtering inside `case_index`, the finding's default, would make scope members, bug cases and manifest rows naming a retired case unresolvable — `scope_member_resolution` refuses what it cannot find, :3742).

## 9. Analogs and overlaps noticed (reported, not widened)

- RC1-2 (`plans/piles/onboarding-forge/batch-1-onboarding-roles-forge.md:44`, batch in work since 12.11): the same designer P16 line as N4 — an `очередь:` line is owed in both batches, or RC1-2's designer part is closed by N4.
- roles-context H8 (`20261112-razdely-masterstva-nesut-stroki-procedury-p27.md`) moves the critic's fixed tokens into a process section of the same file N4 edits — order or disjoint lines (D-0048).
- `qa-case-critic.md:44` "(... it merges the CASES)" contradicts `test_case_merges.py:588` "a merge changes no case" under the current route; N4 rewords it in the same edit if F1 = (a); if F1 = (b) it is a one-line fix elsewhere.
- Column-by-name siblings outside the finding: `planning_contract.py:1341, 1345, 2488-2489`, `audit_factory.py:748`.
- The finding's line numbers are stale (code moved): `contract.py:3024 -> 3416`, `:3303-3338 -> 3680-3731`, `check_delivery.py:637-649 -> 727-768`, `controller.py:2625 -> 3049-3051`, `critic_rollcall.py:115 -> 117`.
- No D-nnnn records the B-1 trade-off (case count vs test count); if F1 is answered, its record belongs in the batch file, not DECISIONS.md (single-node decision).

## 10. Reading trail

Read whole: the node file `plans/piles/test-code-quality/batch-2-sliyanie-kejsov-i-chitateli.md`; the finding `.../findings/20261102-...shapki.md`; `P\agents\qa-case-designer.md`; `plans/piles/release-next/findings/20261030-kritik-kejsov-ne-ishchet-dubli-i-sliyaniya-p16.md`; `plans/piles/roles-context/findings/20261112-razdely-masterstva-nesut-stroki-procedury-p27.md`; `plans/piles/hotfix-12586/findings/20261028-s5-odin-kejs-odin-test.md`; `plans/piles/roles-context/findings/B-191-p17-glavnaya-logika-keysy.md`; `plans/piles/test-code-quality/README.md`; `docs/TESTING.md`; `P\scripts\case_lifecycle.py`.
Read in part: `P\agents\qa-case-critic.md:36-50`; `P\scripts\contract.py:2840-2866, 3028-3053, 3410-3449, 3600-3748`; `P\scripts\check_delivery.py:406-445, 600-850, 1000-1029, 1280-1316` + its def list; `P\scripts\controller.py:2431-2460, 2844-2874, 2990-3079`; `P\scripts\critic_rollcall.py:85-140, 760-1079`; `P\scripts\branch_accounting.py:440-479, 1662-1700, 1730-1760, 1905-1934, 2310-2339`; `P\scripts\case_versions.py:435-475, 498-507, 570-591`; `P\scripts\driver_stage_plan.py:870-919`; `P\scripts\gate_preflight.py:650-679`; `P\scripts\planning_contract.py:4490-4534`; `P\scripts\tests\test_case_merges.py:1-60, 555-604`; `P\scripts\tests\test-layers.json:1-30, 250-286, 460-549, 894-913, 1199-1218, 4564-4578, 7380-7409` and the keep/cohorts/quarantine section lines (:35, :7019, :7067); `P\references\stages.json:135-172`; `P\references\artifact-contract.md:55-79`; `P\design\role-rules.json:24-27, 135-141, 179-180`; `P\scripts\tests\fixtures\judgment-census.json:1-25` + rows 235-242; `docs/tasks/specs/t-723-tq1-27-amended.md:11-70, 384-403` (+ Grep hits); `plans/piles/onboarding-forge/batch-1-onboarding-roles-forge.md:1-6, 44`; `docs/SIBLING_MAP.md:378-381`.
Searches (all with their controls in §1.2 or here): Grep `Archived` (case-sensitive and `-i`) over `P\scripts` and `P\references`; `["']archived["']` `-i`; `case_status\b`; `case_index\(|case_files\(|_case_records\(` over `P\scripts` (all callers, then context -B3 -A4 for non-test files); def lists of check_delivery, ledger, traceability, check_traceability, delivery_summary, coverage_contract, stand_gaps; `merged_into`; `dedupe`; `reuse_decision` in validate_artifacts; `parametrise into one test|carried_concerns`; `(?i)merge|concern|parametri` in qa-automator.md; decisions files; piles (`Archived|merge_candidates|Merge candidates|parametrise into one test|слияние кейсов|...`, then per-pile for thinking-roles and roles-context); TQ2-1 in `logs/journal`; Globs for t-715/t-756 reviews, slices of qa-case-designer, scenario stories and variants.
Not read (named for the Lead): the plan-critic review t-715 and diff-critic review t-756 (not in this checkout); `docs/tasks/specs/t-1502-test-grouping.md`; the bodies of the R/verify callers in N3's last row.

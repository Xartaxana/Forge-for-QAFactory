# Told before work: node T1r-cards — the 12 ahead cards become rows (draft, designer, t-697)

Status: DRAFT for Lead acceptance. Forks are returned (§8) and decided nowhere here; every item that depends on a fork says
which option the card follows (the recommendation), so the node is executable tonight by recommendation.

Parents: `docs/tasks/specs/20261114-told-before-work-t1r-t2-dispatch-spec.md` ("dispatch": §2 T1r, §8 with the Lead decisions
F-3 (b), F-4 (a), F-5 (a), F-6 (a)); `docs/tasks/specs/20261113-told-before-work-mechanism-spec.md` ("parent": §2.6, §2.6a K8,
§2.6b K10, §2.7, §5.1 T1r row, §5.2-§5.4 row tables); wave-0 drafts `...-wave0-rows.md`, `-part2.md`, `-part3.md`.

Read base: worktree `C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r` (T3a with T2 merged, T1r in progress; read only).
`W` = `ai-packages\qa-factory` of that tree. The card is written against the tree T1r WILL leave; every assumption about
that tree is listed in §0.2 and must be checked by the Lead at dispatch.

---

## §0 Facts and assumptions

### §0.1 Facts read on the carrier (tbw-t1r)

| # | fact | carrier |
|---|---|---|
| F1 | 12 cards `{sources, text}`, one per role; the note says a card is rendered by `brief_pack.py` under `## The rules code will apply to your handoff` | `W\references\ahead-cards.json` 1-95 |
| F2 | `hand_cards` is `len(cards)` of ahead-cards.json; an absent or unreadable file is `None` with a reason and red ("never 0"); the counter is DENSE (red below its stored number too) | `W\scripts\stage_joints.py` 997-1036, 1125-1129 |
| F3 | The key page tells the card under `### Not yet in rows` ONLY while `told_ratchet.hand_cards` > 0 (absent / not a count: told); at 0 the card is not told from the page even if the file still has it | `W\scripts\contract_slices.py` 656-660; test row `test_contract_slices.py` 652-656 |
| F4 | `brief_pack.ahead_card(role)` reads the file; an empty card gives no brief section (`if ahead:`) | `W\scripts\brief_pack.py` 414-418, 4481, 4545-4546 |
| F5 | All 12 roles list `references/slices/<role>/handoff-keys.md` in inject-map.json (qa-case-critic since T3a) | `W\references\inject-map.json` 19-122 |
| F6 | 11 role-rules carriers anchor in ahead-cards.json, ids: letter-branch-settles-oracle (64), case-id-in-briefs-form (161), case-id-note-not-read-by-code (162), designer-one-case-per-plan-row (163), designer-now-before-keys (164), merge-keep-only-for-p16-p19 (181), scribe-card-delivery-ready-line-is-the-blocks (306), tester-card-derived-row-also-gets-a-behaviour-claims-row (347), designer-card-observation-sufficiency-review (482), designer-card-reuse-decision-vocabulary (483), critic-card-over-plan-case-budget-line (484). Count by Grep: 11 | `W\design\role-rules.json` |
| F7 | role_rules: every anchor stands EXACTLY once in its carrier, folded (whitespace, case); a `.json` carrier is searched by its string values; HOMES include `references` | `W\scripts\role_rules.py` 1-31, 42, 219-256 |
| F8 | A row is one id (two rows of one id red, E7); a sub-id `<id>.<part>` of a sited id is sited; an unsited row counts against `told_ratchet.unsited` | `stage_joints.py` 332-334, 966-985, 1002-1025 |
| F9 | `told_line` = `- [<check>] <expected> Door: <door>.`; a `requirement_from` row renders its carrier's words (PHASE_JSON_KEYS: "`<artifact>` carries the keys ...") | `stage_joints.py` 550-597 |
| F10 | K3: a row with `requirement` needs a `door` and a named role; `when` tokens from `when_kinds`; `door_needs: shell` needs `when` shell; `role_rule` must be a role-rules id (K7) | `stage_joints.py` 847-906 |
| F11 | K8: `L = inject_context.MAX_BLOCK_CHARS`, `W = L*8//10`; a page at or over W WARNs (split), over L red; a row longer than W alone is red; the partition never cuts a row | `contract_slices.py` 598-602, 687-716, 765-775 |
| F12 | K10 runs inside `contract_slices.keys_findings` (`role_load.native_headroom_problems`); `role-load.json` holds `native_headroom: {qa-test-strategist: 46008}` (U 46008 > H 42400 after T3a) | `contract_slices.py` 830-834; `W\references\role-load.json` 38-40; T3a report §2 |
| F13 | The brief layer is counted at its fixed allowance (6144), so removing the card from the BRIEF changes no measured load; only the PAGE (injection_role) moves `ratchet_tokens` / `process_ratchet_tokens` / K10 | `role-load.json` 2, 7 |
| F14 | T3a's measured card cost on the pages: +293..+357 process tokens per role (qa-case-critic +1550 for a whole new page) | T3a report §2 table |
| F15 | `exit_gate:grounding` (S2, qa-requirements-tester, demands `derived`) and `exit_gate:case_identity` (S4, qa-case-designer, demands `= the file name`) are rows with NO requirement, told by the key-page path, anchor `## Outputs` | `W\references\stage-joints.json` 182-229 |
| F16 | `grounding_errors` refuses a register in which a production module the diff creates is cited by no `derived` row | `W\scripts\exit_gate.py` 1584-1655 |
| F17 | `check_context_manifest_v0` judges `related[]` {key, kind in `RELATED_KINDS`, source}, `implementations[]` (one per repo, listed source), and the v2 sections `coverage_search` / `existing_test_candidates` via `context_bundle.v2_discovery_problems`; PHASE_JSON_KEYS `context-manifest.json` = ticket, acceptance_criteria, implementation | `W\scripts\validate_artifacts.py` 2350-2416, 103 |
| F18 | `test_ahead_cards.py` pins: every stage role has a card; the closed lists of `VOCABULARIES` stand in the card text; FLAKY_MIN_RERUNS and TEST_REPORT_MAX_BYTES quoted; expectation-change fields; brief_pack renders the card for every role | `W\scripts\tests\test_ahead_cards.py` 65-87, 231-369 |
| F19 | Other tests read the cards: `test_ahead_cards_rules.py` 26-47, `test_case_id_form_texts.py` 242, `test_context_bundle.py` 478, `test_env_evidence.py` 171, `test_oracle_provenance.py` 335, `test_question_branches.py` 1780, `test_report_texts.py` 25-27, `test_validator_class.py` 47, 222, 446, `test_s7_rejudge.py` 109, `test_brief_pack_roles.py` 52 | Grep `ahead-cards\|ahead_card\|hand_cards` over `W` |
| F20 | Six held-out bodies: `s5_precheck._sides_provisional` 2085-2149, `_sides_pending` 2152-2179; `execution_request._profile_for` no-profile raise 1790-1797; fingerprint raise 3714-3724 (`execution_fingerprint.build` 104-151, `file_hash` 73-82, `_check_claim` 85-92); `stage_done.coerce_value` 92-157, `SETTABLE` 71-86, `--set key=value` form 218 | those files in `W\scripts\` |

### §0.2 Assumptions about the tree T1r leaves (CHECK AT DISPATCH)

| # | assumption | where T1r says so | if false |
|---|---|---|---|
| A1 | T1r landed every row of its §2.2 verbatim, including the §5.2 `validate_artifacts:<function>` rows, the §5.4 rows (`s5_precheck:bindings`, `:oracle`, `:environment`, `:manifest`, `manifest_put:critic_approval`, `manifest_put:expectation_changes`), `coverage_contract:obligations` and `.observation` (R8), `planning_contract:plan` (wave0 item 3a), the PT/SG/HA rows | dispatch §2.2 | a target row of §3 that is absent: the segment takes a NEW row with that id (same sentence, door per §3.0 D-rule); the report names each |
| A2 | `exit_gate:grounding` and `exit_gate:case_identity` are still sentence-less with key-page path legs | dispatch §2.3 note | if T1r gave them a sentence, §3 appends to it (rule M1) |
| A3 | `critic_rollcall:*` states a requirement with a page leg (L9 → `{"page": true}`) | dispatch §2.3 L9 | if sentence-less, the qa-case-critic segments become its requirement and its told becomes `[{"page": true}]` |
| A4 | T1r did NOT regenerate the 12 key pages and did NOT edit `role-load.json`, `inject-map.json`, `role-rules.json`, `ahead-cards.json` (dispatch non-goals) | dispatch §2 non-goals | if T1r regenerated pages / raised role-load, items C-7..C-9 measure only the delta of this node |
| A5 | After T1r: `told_ratchet` = {hand_cards 12, legacy_legs 0, unsited N1 (measured, named)}; `gaps` 3; `rowless` 25 | dispatch §2.5 | the builder reads the real values first and writes them in the report's "before" column |
| A6 | T2 is merged (`role_cli:<key>` sited) | dispatch §4, T2 report | no effect on this node |
| A7 | `contract_slices.py --check` may be RED after T1r (stale pages) and audit A22 / K10 may be red; this node is the one that turns them green | A4 | the report says which were red before the node |

---

## §1 Architecture invariants, owners, census class (rule 10, AR-29, P27)

| AR | how this node keeps it | change check written into the DoD |
|---|---|---|
| AR-10 a check's requirement reaches the role before the work | every check-stating clause of a card lands on a row of the role's key page | C-test `cards/segment-coverage` (report table) and `ahead/vocabulary-on-page/*` rows |
| AR-15 one survivor, wired everywhere | the hand card is retired (`cards: {}`); the page is the one told carrier; no card survives beside its row (P31, axis 34) | `stage_joints.py --check`: hand_cards 0; real-tree row `T1rc/no-not-yet-heading` |
| AR-13 a fact with a reader is read through it | tests read the told text through `contract_slices.handoff_keys_pages`, never by opening stage-joints.json or the page files themselves | review of the test diff (critic) |
| AR-14 one artifact, one writer | `stage-joints.json`, pages, `role-load.json`, `role-rules.json`, `ahead-cards.json` written by this node only in its wave | owns list |
| AR-20 shrink-only ratchets | hand_cards 12 → 0 (dense, lowered); `process_ratchet_tokens` / `ratchet_tokens` / `native_headroom` moves each named (key, old → new, reason); `unsited` raise named with its siting node | ratchet rows in the report |
| AR-22 every field read has a producer | every new row's producer names a role file (`agents/<role>.md` exists) | `_producer_leg` green |
| AR-11 a role gets only the context it needs | K10 measured per role; growth named | `contract_slices.py --check` K10 green |
| AR-29 code judges data | rows say what code CHECKS (fields, lists, presence, joins); procedure / advice clauses of a card do not become rows (§3.0 rule K) | critic question 11 |

Checks this node adds or alters, owner and census class:

| check | owner it serves | census class |
|---|---|---|
| `test_ahead_cards.py` card-presence rows → page-presence rows (`ahead/vocabulary-on-page/<role>/<label>`) | data (a closed list of code is present in the text a role receives) | xref; test only, not a census unit |
| `test_ahead_cards.py` brief rows (card in brief) inverted to "no ahead section while hand_cards is 0" | data (shape of the brief) | shape; test only |
| re-pointed reads in the F19 tests | data | unchanged class per file |
| `told_ratchet.hand_cards` 12 → 0 | data (count) | ratchet; no unit change |
| no code check is added or altered (`_hand_cards`, `_told_units`, `ahead_card` unchanged) | — | census: no new blocking unit |

The judgment itself (is the role's artifact right) stays with the role and the tier above; nothing here moves a judgment into code.

---

## §2 The builder card

given: this file; `docs/tasks/specs/20261114-told-before-work-t1r-t2-dispatch-spec.md` §2 and §8; parent spec §2.6, §2.6a, §2.6b, §2.7, §5.2-§5.4; `wave0-rows-part2.md` §4 and the F-P2 acceptance block; `W\references\ahead-cards.json`; `W\references\stage-joints.json`; `W\design\role-rules.json`; `W\references\role-load.json`; `W\references\inject-map.json`; `W\scripts\contract_slices.py` (`_told_units`, `requirement_section`, `keys_findings`, `keys_write`); `W\scripts\stage_joints.py` (`told_line`, `_row_requirement`, `_hand_cards`, `_told_counters`); `W\scripts\role_rules.py`; `W\scripts\role_load.py` (`native_headroom_problems`, `static_load`); the F19 test files; `design/factory-rules.md` whole; `plans/builder-rules.md`
owns:
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r-cards\ai-packages\qa-factory\references\stage-joints.json (rows of §3 and §4; `told_ratchet.hand_cards`, `told_ratchet.unsited`)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r-cards\ai-packages\qa-factory\references\ahead-cards.json (`cards` → `{}`, `note` rewritten)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r-cards\ai-packages\qa-factory\design\role-rules.json (the 11 carriers of F6: file re-pointed only)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r-cards\ai-packages\qa-factory\references\slices\ (every `handoff-keys*.md` and `index.md`, generated by `contract_slices.py --write` only)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r-cards\ai-packages\qa-factory\references\inject-map.json (continuation page lines only, when K8 says split)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r-cards\ai-packages\qa-factory\references\role-load.json (`ratchet_tokens`, `process_ratchet_tokens`, `native_headroom` values only)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r-cards\ai-packages\qa-factory\agents\ (only the charter lines rule K moves, per F-2; one line per moved clause)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r-cards\ai-packages\qa-factory\scripts\tests\test_ahead_cards.py (main, VOCABULARIES readers, the brief block)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r-cards\ai-packages\qa-factory\scripts\tests\test_role_rules.py (rows naming ahead-cards.json, if any)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r-cards\ai-packages\qa-factory\scripts\tests\test_contract_slices.py (the real-tree card rows: 659-661 and a new variant row)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r-cards\ai-packages\qa-factory\scripts\tests\test_stage_joints.py (the told_ratchet table rows 295-298, 875 only if hand_cards values there are read from the real file)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r-cards\ai-packages\qa-factory\scripts\tests\ (the card read of each F19 file, re-pointed per item C-10: test_ahead_cards_rules.py, test_case_id_form_texts.py, test_context_bundle.py, test_env_evidence.py, test_oracle_provenance.py, test_question_branches.py, test_report_texts.py, test_validator_class.py, test_s7_rejudge.py, test_brief_pack_roles.py — the card-reading lines only)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r-cards\ai-packages\qa-factory\changelog.d\tbw-t1r-cards.md
non-goals: `brief_pack.py` (its `ahead_card`, `FIRST_LOOK_AHEAD`, the ahead section: T3b); `contract_slices.py` code (`ahead_card`, `CARD_GROUP`, `NOT_YET_HEAD` stay as dead-at-zero code until T3b/closing); `stage_joints.py` code (`_hand_cards`, `AHEAD_CARDS` stay: the counter keeps reading the file); any refusal text or site; conductor-producer rows (`stage_done:set`, `planning_contract:plan.unmarked_revision`: T9c, F-6 (a)); retiring any role-rules row; any T1r row's sentence other than by rule M1 (append); quarantined tests (`test-layers.json` `quarantine`); a new test file
handoff: the branch commit plus `docs/tasks/specs/reports/20261114-t1r-cards-report.md`: the segment coverage table (§3, one line per segment with its final row id and status), the ratchet rows (key, old → new, reason), K8 page sizes, K10 U/H per role before/after, the FR walk, and the verbatim witness
edges: §5 (each with its invariant)
siblings: `brief_pack.ahead_card` + its section (T3b, axis 34 twin; between this node and T3b the brief has no ahead section: F-5); `test_report_texts.py` `CARD_MAX_BYTES` 27 (T3a report §6: retire here, the cards it caps are gone); `contract_slices.ahead_card` / `CARD_GROUP` dead at hand_cards 0 (closing node removes); `design/factory-rules-debt.md` 271-272 ("All twelve have a card now") — text owner Lead, queued; SIBLING_MAP axis 34 (one road)
DoD: see §6 (inline, exact commands)
designer: this file (once accepted)
architecture: AR-10, AR-11, AR-13, AR-14, AR-15, AR-20, AR-22, AR-29 -- the hand cards are absorbed into rows on the key page (one told carrier); ratchet moves named; no code check added
judgment: none moved -- the rows state what code checks of a field (data); a card clause that states procedure or advice goes to the role's charter (the role's judgment), never into a row or a code check

Gate: starts after T1r is merged into main (same files: `stage-joints.json`, `told-ratchet.json` is not touched here). The builder
merges main first and re-checks A1-A7 against the merged tree before item C-1.

### §2.1 Items

| item | what | expected behaviour | test |
|---|---|---|---|
| C-1 | Measure "before" | run `stage_joints.py --check`, `contract_slices.py --check`, `role_rules.py --check`, and `role_load.static_load` per role (U per §2.6b); paste verbatim | report §before |
| C-2 | Land the segments of §3 | each segment lands on its target row by rule M1/M2/M3 (§3.0); placement P resolved by rule P (§3.0); rule K clauses per F-2 | `stage_joints.py --check` green; `cards/segment-coverage` table |
| C-3 | Land the four held-out rows of §4 that land here | rows `s5_precheck:sides.provisional`, `s5_precheck:sides.pending`, `execution_request:profile.none`, `execution_request:fingerprint` with the sentence, door, roles, stages, when of §4, told `[{"page": true}]` | `--check` green; page row `T1rc/held-out-on-page` |
| C-4 | Retire the cards | `ahead-cards.json` keeps `schema_version`, `cards: {}` and a rewritten `note`: "Retired by T1r-cards (told-before-work): every card is a row of references/stage-joints.json, told on the role's key page; this file stays so the hand_cards counter reads 0, not unknown." | `--check`: hand_cards 0 |
| C-5 | `told_ratchet.hand_cards` 12 → 0; `unsited` → measured (named raise per new unsited row, each with its siting node: validate_artifacts → T7a-n, s5_precheck → T5, execution_request → T5b, other → named in the report or STOP) | dense counter green; ceiling equals measured | `--check` summary line |
| C-6 | Re-point the 11 role-rules carriers | `"file"` becomes `references/slices/<role>/handoff-keys.md` of the role in the table §3.13 (or `handoff-keys-<n>.md` where `--write` put the row); anchors unchanged; set `role_rule: <id>` on the row carrying it (one per row; a row carrying two: the first in card order, the second named in the report) | `role_rules.py --check` 0 findings |
| C-7 | Regenerate pages | `contract_slices.py --write`; no page at or over W (K8 WARN not accepted): a page that reaches W gets its split line in inject-map.json in the SAME commit (§2.6a) | `contract_slices.py --check` clean, no WARN |
| C-8 | role-load | set `ratchet_tokens` / `process_ratchet_tokens` to the measured values; every change a named row (role, old → new, reason "T1r rows and card rows on the page; card section removed") | audit A22 clean (`role_load.py --all` per role-load note) |
| C-9 | K10 | for each role: U after vs H; a role over H and over its baseline: raise by F-4 (recommended: named baseline = measured U, Appendix A cited); a role newly over H gets a `native_headroom` row (named) | `contract_slices.py --check` K10 green |
| C-10 | Re-point the card readers in the F19 tests | a read of a card text becomes the role's told text: `"\n".join(contract_slices.handoff_keys_pages(PLUGIN, role))` (one helper in `test_ahead_cards.py`, `told_text_of(role)`, imported by the others, as `test_validator_class` already imports `test_ahead_cards`); an assertion that the BRIEF carries the card is inverted (no `## The rules code will apply to your handoff` while hand_cards is 0) | each file green alone |
| C-11 | Changelog fragment `changelog.d/tbw-t1r-cards.md` | one English ASCII bullet | `selftest.py --lang` |

### §2.2 Test rows (variant rows in keep files; no new file)

| id | file | input | expected |
|---|---|---|---|
| `ahead/vocabulary-on-page/<role>/<label>` (19 rows, one per VOCABULARIES entry) | test_ahead_cards.py | the real package; `told_text_of(role)` | every value of the closed list stands in the role's page text |
| `ahead/quoted-numbers-on-page/flaky`, `/report-bytes` | test_ahead_cards.py | real package | `>= {FLAKY_MIN_RERUNS} isolated executions` on qa-failure-analyst's page; `{TEST_REPORT_MAX_BYTES:,} bytes` on qa-doc-scribe's |
| `ahead/expectation-fields-on-page/<role>` | test_ahead_cards.py | real package | the B-194 field checks (AUTHOR_FIELDS for qa-automator, CRITIC_FIELDS + KEY_FIELDS for qa-code-critic) read the page text |
| `ahead/cards-retired` | test_ahead_cards.py | real file | `cards == {}` and `told_ratchet.hand_cards == 0` |
| `ahead/brief-no-ahead-section/<role>` (12) | test_ahead_cards.py | `brief_pack.build(..., write=False)` per stage role | the brief does NOT carry `## The rules code will apply to your handoff` (inverted row; T3b deletes the code) |
| `T1rc/no-not-yet-heading/<role>` (12) | test_contract_slices.py | real package, `handoff_keys_pages` | no `### Not yet in rows` on any page |
| `T1rc/card-file-empty-counter-zero` | test_contract_slices.py | fixture plugin, `cards: {}`, hand_cards 0 | section has no card group; `ahead_card(...) == ""` |
| `T1rc/held-out-on-page/<id>` (4) | test_contract_slices.py | real package | qa-automator's page holds `[s5_precheck:sides.provisional]`, `[s5_precheck:sides.pending]`, `[execution_request:profile.none]`, `[execution_request:fingerprint]` lines (the last two on every `--mine` role's page whose capability admits the row) |
| `T1rc/role-rule-anchor-once/<id>` (11) | test_role_rules.py (existing real-register run covers it; add rows only if the file has a per-carrier table) | real package | each re-pointed anchor counts 1 on its page |
| `cards/segment-coverage` | report table (not a test) | §3 | every segment has a final status (row id / told by <row> / charter line / question) |

---

## §3 The mapping (12 cards)

### §3.0 Rules (read once; every row of the tables applies them)

- **M1 append (F-1, recommended).** A segment whose target row already states a requirement (`requirement`) is APPENDED verbatim
  to it: `<existing sentence> <segment>`. The builder never rewords the T1r sentence or the segment. Over-telling is accepted;
  under-telling is not.
- **M2 own sentence.** A target row with no requirement (sentence-less, A2/A3) takes the segment as its `requirement`; its told
  items become `[{"page": true}]` (dispatch F-3 (b), one road); its `demands` tokens stay (looked up on the page, T1r-3).
- **M3 new row.** A target id with no row: a new row, `requirement` = the segment, `door` per rule D, `roles` = the card's role,
  `stages` = that role's stages (`stage_guard.stages_of_role`), `when: ["always"]`, told `[{"page": true}]`, `demands: []`,
  `joint: null`.
- **X cross-role guard.** When the target row names a role OTHER than the card's role, the segment does not go into that row:
  it lands by M3 on the sub-id `<target id>.<role without "qa-">` (e.g. `validate_artifacts:check_manifest_v0.automator`).
  Invariant: a role is never told another role's card words. A sub-id of a sited id is sited (F8); of an unsited id, unsited.
- **R requirement_from target.** A target row stated by `requirement_from` cannot take a sentence (K3: one way). The segment is
  dropped as TOLD when the carrier's rendered words already carry every token of the segment (builder compares on the page);
  otherwise it lands by M3 on `<target id>.<role without "qa-">`.
- **D door.** A new row's door: the segment's own door clause when the card gives one (quoted in the table), else the default
  of parent §5.2: "edit the file and the field the refusal line names". `door_needs: "none"` unless the door is a command,
  then `"shell"` with `when` holding `shell` — never for a role without Bash (FR-2).
- **P placement.** Rows marked **P** were placed by the card's `sources` and the field names the segment quotes, not by reading
  the function body. The builder Greps the segment's first quoted field (`` `goal_summary` `` etc.) in the card's sources:
  exactly ONE `def` of a source contains it → that function's id `<stem>:<function>` is the target (when it differs from the
  table, the function found wins and the report names it); zero or several → STOP, the segment is a question to the Lead
  (never a guess). Rows marked **V** were verified on the body (§0.1).
- **K procedure.** A segment marked **K** states procedure, advice or rationale (no field a check reads). It is no row
  (AR-29). Under F-2 (a): the builder Greps 2-6 words of it in `agents/<role>.md`; present → dropped (already in the charter,
  named in the report); absent → one line appended verbatim to the charter's closing section. Invariant: no card clause is
  lost; no procedure becomes a row.
- **T told elsewhere.** A segment marked **T** is already told by the named row on the same role's page; it is dropped and the
  report names the row.

Columns: seg = segment id; text = the card text in full (verbatim from `ahead-cards.json`); target = row id; how = M1/M2/M3/X/R/K/T;
place = V/P; deleted = what goes away (always: that text from the card).

### §3.1 qa-scout (S1)

| seg | text | target | how | place |
|---|---|---|---|---|
| sc-1 | "work/context-manifest.json is read field by field: `ticket`, `acceptance_criteria` and `implementation` present;" | `validate_artifacts:check_phase_json` row of `context-manifest.json` (requirement_from PHASE_JSON_KEYS) | R → T (the carrier renders "`context-manifest.json` carries the keys `ticket`, `acceptance_criteria`, `implementation`") | V (F17) |
| sc-2 | "every `related[]` row is {key, kind, source}, kind one of implementation\|blocker\|bug\|mention, `source` saying WHERE in this ticket the key was read; one `implementations[]` row per repository. `coverage_search[]` rows: repo, revision, changed_area, searched_paths, status complete\|partial\|unavailable, reason; nothing found is top-level `coverage_status: not_found`. `existing_test_candidates[]` rows: candidate_id, repo, revision, path, selector, parameter_ids, level, assertion_refs, candidate_requirement_refs, origin existing\|added_in_change\|unknown, result_candidate_refs." | `validate_artifacts:check_context_manifest_v0` | M1 | V (F17) |
| sc-3 | "S1 closes on work/source-inventory.json: every required source retrieved and inspected, none `pending`, no material without receipts." | `source_preflight:<function>` | M3; door = sc-4 | P (Grep `pending` in source_preflight.py) |
| sc-4 | "A source you could not get: name it in your digest with its id and what is missing - recording a person's words is the orchestrator's door; you are resumed with their answer." | door of sc-3's row | (door) | — |
| sc-5 | "Build with `context_bundle.py --manifest`, then `--validate`." | `validate_artifacts:check_context_manifest_v0` | M1 (after sc-2) | V |

### §3.2 qa-requirements-tester (S2)

| seg | text | target | how | place |
|---|---|---|---|---|
| rt-0 | "Three artifacts, three checks." | — | K (framing; no field) → dropped, no charter line | — |
| rt-1 | "work/requirements-register.md: `ids` non-empty and all R-n, `by_source` within ac\|story\|feature\|discussion\|assumption\|derived, `confidence` high\|low - a register of AC alone while a parent feature exists must be `low`; every row's observable prefixed diff:\|current-code:\|expected-contract: or the word `none`; every `derived` row naming what it was derived from; `impact` from config.json impact_scale." | `validate_artifacts:check_register` | M1 | V by §5.2 sentence (body P for the parent-feature clause: Grep `parent` in check_register; absent → STOP) |
| rt-2 | "Every production module work/impl-diff*.txt CREATES has to be cited by a `derived` row - the exit gate compares them, so read every hunk, limits, rejected inputs and guards included;" | `exit_gate:grounding` | M2 (A2) | V (F16) |
| rt-3 | "a `derived` row only the diff speaks to also gets its `## Behaviour claims` row." | `validate_artifacts:check_behaviour_claims` | M1; `role_rule: tester-card-derived-row-also-gets-a-behaviour-claims-row` | V by §5.2 sentence |
| rt-4 | "work/requirements-readiness.json: `verdict` ready\|blocked agreeing with the facts, `goal_summary` >= 30 characters in your own words, `aspects` non-empty with status ready\|blocked\|n/a and a reason on every n/a, `open_questions[]` each with question, severity blocker\|major\|minor and owner_role po_ba\|dev_arch\|qa." | function holding `goal_summary` | M1 or M3 | P (Grep `goal_summary` in validate_artifacts.py, check_witness.py, exit_gate.py) |
| rt-5 | "understanding.md: at most 40 lines, its five sections in order, and every register R named in a 'What we verify' or 'What we do not verify' line." | `validate_artifacts:check_understanding` | M1 | V by §5.2 sentence |

### §3.3 qa-test-strategist (S3)

| seg | text | target | how | place |
|---|---|---|---|---|
| ts-0 | "planning_contract.py and observation_contract.py will check, so write to them in fields, not in prose." | — | K → charter by F-2 | — |
| ts-1 | "`verification_depth: low` is accepted ONLY together with `impact: low`, `likelihood: low`, `confidence: high` and `bounded_reversible: true`; repeating the detector's sentence in a note is not evidence, and `impact: unknown` can never be low while `impact: severe` demands `critical`. Every row needs `risk_source_refs` and `required_scenarios` non-empty." | `planning_contract:plan` | M1 | P (Grep `bounded_reversible` in planning_contract.py) |
| ts-2 | "A no-write obligation (kind `state_unchanged` or `no_write_attempt`) needs three things beside the claim: `sequence` of exactly four items with phases before_read, action, completion, after_read, each `ref` naming a check or step that exists; `positive_control_ref` naming a MUTATING check that is not one of those four; and `reachability_assertion_ref`." | `coverage_contract:obligations.observation` | M1 | P (Grep `positive_control_ref` in observation_contract.py; the accepted id F-P2-4 (a)) |
| ts-3 | "An oracle you cannot settle is `oracle_unknown: true` with `source_conflict: true`; an unresolved oracle does not authorize execution. A letter branch whose answer settles the oracle sets `oracle_unknown: false` and its `coverage_obligations` (`oracle_status: resolved`), each with `sufficiency_review {author_dispatch_id, input_hash, rationale}` and `observation_contract`." | `coverage_contract:obligations` | M1; `role_rule: letter-branch-settles-oracle` (second anchor `designer-card-observation-sufficiency-review` named in the report) | P (Grep `source_conflict` in planning_contract.py / observation_contract.py / coverage_contract.py) |

### §3.4 qa-case-designer (S4)

| seg | text | target | how | place |
|---|---|---|---|---|
| cd-1 | "A case file's `id` IS its file name, both in the form named on this brief's `Case id form:` line: `<case id>.md` declares `id: <case id>`. That is the factory's contract over any project note (a note naming another form is not read by code), and the exit gate refuses the handoff otherwise." | `exit_gate:case_identity` | M2 (A2); `role_rule: case-id-in-briefs-form` (second: case-id-note-not-read-by-code, named) | V (F15) |
| cd-2 | "Frontmatter every case owes: id, title, area, priority P0\|P1\|P2\|P3, status (yours are Draft\|Review\|Approved - only the code critic moves a case to Automated, and only after a probe), channel auto\|manual-agent\|manual-human, reuse_decision new\|updated\|extend:<case id>\|dedupe:<case id>, updated, task, covers: [R-n] that exist in that task's register (an R the register does not carry reads as invented), defect_class from the project's closed list (or smoke, or regression:BUG-NNN), and basis." | `validate_artifacts:check_case` | M1; `role_rule: designer-card-reuse-decision-vocabulary` | V by §5.2 sentence |
| cd-3 | "defect_class and basis are inherited from your plan row, never reassigned." | `validate_artifacts:check_case_form` | M1 | V by §5.2 sentence |
| cd-4 | "One case per plan row, an `unverifiable` row too; its Thens that wait on a question go in `question_thens` under that question's id as requirements-readiness.json has it (never `raise` once raised); a before/now question (a `raise` too) keys its texts `now` / `before`, never by letter." | function holding `question_thens` | M1 or M3; `role_rule: designer-one-case-per-plan-row` (second: designer-now-before-keys, named) | P (Grep `question_thens` in exit_gate.py, validate_artifacts.py) |

### §3.5 qa-case-critic (S4) — source `critic_rollcall.py` only

| seg | text | target | how | place |
|---|---|---|---|---|
| cc-1 | the whole card text (F1 line 40), from "critic_rollcall.py computes your verdict" to "an `Over the plan case budget:` line." | `critic_rollcall:*` | M1 (A3; M2 if sentence-less); `role_rule: merge-keep-only-for-p16-p19` (second: critic-card-over-plan-case-budget-line, named) | V (single source; the detector row is the family) |

### §3.6 qa-automator (S5) — source `s5_precheck.py`

| seg | text | target | how | place |
|---|---|---|---|---|
| au-1 | "s5_precheck.py will check, so write to it: every Then is bound in `then_bindings[]` {case, then, instance_id, assertion_ref \"file:line\"}, and the names it demands appear in that assertion." | `s5_precheck:bindings` | M1 | V by §5.4 #3 |
| au-2 | "A status code or literal a Then fixes is asserted as written and NEVER changed after a red run: that test is handed over RED, `unresolved[] reason: contradicts_requirement`. A value you invented may change after a red run only with an `expectation_changes[]` row through manifest_put.py: `then_refs` [{case, then}] it still proves, `what_changed`, `reason`; a deleted or renamed test owes it too." | `s5_precheck:oracle` | M1 | V by §5.4 #4 |
| au-3 | "A `blocked_by_env` row has `remedy` {kind, where, change, restart}, names only; it stands only on a run showing the stand (`env_blocked`, a STAND SIGNAL on a run no timeout killed, a connection refusal); a test the project's timeout killed is yours." | `s5_precheck:environment` | M1 | V by §5.4 #6 |
| au-4 | "Smells refused: env credentials in an assert, `None == None`, `sleep`, a copied helper." | `s5_precheck:*` if a smell blocks, else K | F-3 rule: Grep `smell` in s5_precheck.py 1-40; parent says the smell family is advice (`s5_precheck.py:22-25`, parent §5.0 (3)) → K (charter) | P (contradiction reported: the card says "refused") |
| au-5 | "One `tests[]` entry per INSTANCE (`func[param]`); `covers` lists cases." | `s5_precheck:manifest` | M1 | P (Grep `covers` in check_manifest) |
| au-6 | "A `deferred_by_decision:*` row carries `disputes` nothing\|derivation\|case_expectation; `derivation` = not derivable; `case_expectation` = you disagree with the approved case; no route out after gate A." | `s5_precheck:oracle` | M1 (after au-2) | P (Grep `disputes` in s5_precheck.py) |

### §3.7 qa-code-critic (S5)

| seg | text | target | how | place |
|---|---|---|---|---|
| ck-1 | "Static review first, the whole window; then probe_by_code.py and, on doubt, red_sandbox.py --probe (the calls, the model file work/probe-models/<your dispatch id>.json and the reasons are on the card); reuse the author's green receipt, never run a duplicate green. A `mechanical` finding is worded, not fixed." | — | K (procedure) → F-2 | — |
| ck-2 | "Findings go to work/test-code/critic-findings-<your dispatch id>.md with `cause:` on each." | function holding `cause:` | M3 | P (Grep `cause` in check_witness.py, probe_by_code.py) |
| ck-3 | "A test that changed after its red run is listed in your brief (`s5_precheck.py --json`: `expectation_changes`): give each row ONE verdict through manifest_put.py, a patch with its function, `red_attempt` and `green_attempt` plus `critic_verdict` legitimate_correction\|fitted_to_code\|could_not_judge and `critic_note`." | `manifest_put:expectation_changes` | X → `manifest_put:expectation_changes.code-critic` (the row names qa-automator) | V by §5.4 #28 id; field names pinned by test_ahead_cards |
| ck-4 | "`fitted_to_code` is also a `test_defect` finding whose expected is \"the Then's value restored, the test handed RED with contradicts_requirement\". A change you cannot judge is `could_not_judge` with a note, never silence." | `manifest_put:critic_approval` | M1 (row names qa-code-critic only) | P (Grep `could_not_judge` in manifest_put.py) |

### §3.8 qa-runner (S6)

| seg | text | target | how | place |
|---|---|---|---|---|
| ru-1 | "work/run-report.json is read field by field. `witness` at least 30 characters naming the run_suite summary that EXISTS on disk (evidence/<label>-<ts>.json) with the exit code and the totals line - a retelling is not a witness." | `check_witness:<function>` | M3 | P (Grep `30` / `witness` in check_witness.py) |
| ru-2 | "`head` non-empty: evidence not bound to a sha goes stale." | `validate_artifacts:check_run_report_head` | M1 | V by §5.2 |
| ru-3 | "`env_preflight` pass\|blocked, and blocked means `execution_status` is env_blocked - one field, one source. `execution_status` from passed\|failed\|env_blocked\|not_executed\|broken_run\|timeout. `totals` an object." | `validate_artifacts:check_run_report_v0` | M1 | V by §5.2 |
| ru-4 | "Every `results[]` row names ONE case, even when one test covers several, with a status from passed\|failed\|error\|skipped\|not_run, and a skip carries its reason; `manual_checks[].result` is pass\|fail\|inconclusive; a manual `build` takes a `--then-quote` per Then (`thens`)." | `validate_artifacts:check_result_rows` | M1 | V by §5.2 (manual clauses P: Grep `inconclusive`) |
| ru-5 | "Empty is not clean: a zero run with env_preflight pass and no env_blocked, manual_checks or manual_skipped is refused - return blocked with a reason instead." | `validate_artifacts:check_run_report_empty` | M1 | V by §5.2 |
| ru-6 | "And every case S5 automated, plus every manual-agent row of the plan, has to appear in some lane of this report: results, manual_checks, skipped, impossible, env_blocked, manual_skipped or manual_human. Where a case went is your call; saying nothing about it is not." | `validate_artifacts:check_run_report_coverage` | M1 | V by §5.2 |

### §3.9 qa-failure-analyst (S7)

| seg | text | target | how | place |
|---|---|---|---|---|
| fa-1 | the whole card text (F1 line 67) | `validate_artifacts:check_triage_v0` | M1 | V by §5.2 (FLAKY, verdict list) |

### §3.10 qa-doc-scribe (S8)

| seg | text | target | how | place |
|---|---|---|---|---|
| ds-1 | "test-report.md is read by code, not skimmed. Begin it from the template and run `report_facts.py --task <T> --write`: it renders the code-owned blocks (the verdict, Proven, Product bugs, Open questions, Skipped by the plan, Not proven, Decided at gate A, Size, Where to look; Decided at gate B after the gate) and you never type a number they carry." | `validate_artifacts:check_report_blocks` | M1 | V by §5.2 |
| ds-2 | "The `delivery_ready:` line is the block's (check_delivery.py feeds it): yes, after_checks or no." | `validate_artifacts:check_report_ledger_and_readiness` | M1; `role_rule: scribe-card-delivery-ready-line-is-the-blocks` | V by §5.2 |
| ds-3 | "Eleven sections in this order: Proven, Product bugs, Left with you, Open questions, Not proven, Decided at gate A, Decided at gate B, Factory defects, Size, Where to look, Appendix - the verdict above the first." | `validate_artifacts:check_report_sections` | M1 | V by §5.2 |
| ds-4 | "A green test the critic could not verify is in Left with you, not under Proven. Left with you has one item per case in `ledger.json` `left_items`, each with its R-n, case id, `To check:` and `Needed:` or `How:`; its last two blocks are code's." | `validate_artifacts:check_report_left_with_you` | M1 | V by §5.2 (first sentence P) |
| ds-5 | "The Appendix is `traceability.py --render` pasted, a row for every R and every case." | `validate_artifacts:check_report_traceability` | M1 | V by §5.2 |
| ds-6 | "`report_facts.py --task <T> --check` must exit 0 before you finish. Your prose outside the blocks stays under 6,144 bytes." | `validate_artifacts:check_report_ledger_and_readiness` | M1 (after ds-2) | V by §5.2 (TEST_REPORT_MAX_BYTES) |
| ds-7 | "check_coverage.py re-runs at the exit gate: regenerate the coverage map first." | `check_coverage:*` | M1 (M2 if sentence-less) | V (detector row) |

### §3.11 qa-bug-reporter (S8)

| seg | text | target | how | place |
|---|---|---|---|---|
| br-1 | "bugs/BUG-n.md in the task root IS the bug, whatever the channel. Frontmatter is checked: id, title, severity, status, area, found_by, created, `violates` per the oracle grammar (requirement:R-n \| invariant:<id> \| consistency:<where> \| history:<baseline> \| impact:<harm> \| external:<norm>) - with no oracle from that list this is an observation, not a bug;" | `validate_artifacts:check_bug` | M1 | V by §5.2 |
| br-2 | "`impact` from config.json impact_scale, with `severity` DERIVED from it by the scale rather than assigned; `confirmation` unconfirmed\|reproduced_by_factory\|confirmed_by_person\|confirmed_by_rerun (confirmed_by_person from the person's words, else the draft's value; the code derives reproduced_by_factory), so an unreproduced bug is shown apart. Two sections are mandatory: `## User impact` and `## Initial state`." | `validate_artifacts:check_bug_form` | M1 | V by §5.2 |
| br-3 | "A tracker is never yours to write: for a non-markdown channel write a proposal under work/proposals/; external_writes.py performs it after the gate." | `guard_pre_tool:PT-external-writes` | T (row 18 of §5.3, roles `*`, door "write a proposal file under `work/proposals/`") — kept as M1 only if the bug-reporter has no shell (that row is `when: shell`): builder checks `host_adapter.role_has_bash("qa-bug-reporter")`; no shell → M3 on `guard_pre_tool:PT-external-writes.bug-reporter`? NO: a no-shell role cannot hit that guard; the clause is then K | V |
| br-4 | "A bug from a draft also names `cases` (or `cases: []` with `no_case_reason`) and `requirements`; your handoff form lists each bug, each draft not filed, and with no draft chosen the one `gate_b` row - a complete answer." | `validate_artifacts:check_bug_filing_header` | M1 | V by §5.2 (handoff clause P: Grep `gate_b` in handoff_check.py → if a handoff row tells it, T) |

### §3.12 qa-retro-analyst (S9)

| seg | text | target | how | place |
|---|---|---|---|---|
| ra-1 | "Every number in retro.md comes from work/retro-numbers.md and .json, already computed by retro_numbers.py: do not re-add and do not re-price." | function in retro_numbers.py / validate_artifacts.py that compares retro.md numbers | M3 | P (Grep `retro-numbers` in validate_artifacts.py, exit_gate.py); none → K |
| ra-2 | "The story's spend is the sessions the driver's own journal names - a roll-up over every session that merely mentions the ticket once published $1,911 against the $128 actually charged. Two records of the same money exist on purpose: the journal is what the CLI charged and is authoritative, the cost files are token-priced and mark themselves `provisional`; where they disagree, print the gap and say which is which. An unknown is written as `unknown`, never rounded into a fact." | — | K (rationale and craft; FR-24/25/41 for the role) → F-2 | — |
| ra-3 | "The precedent line is written by `estimate_record.py --task <T> --facts <file>`: the file holds `forecast` and `actual` objects and an optional `drivers` array, and code derives the row (ts, task, forecast, actual, delta, hit, drivers) from it; every wrong key is listed in one refusal." | `estimate_record:<function>` (or `role_cli:` row of estimate_record if role-commands.json carries it: then T) | M3 / T | P |
| ra-4 | "What outlives this story goes to the project's ledgers through `project_decisions.py --root <project> add-finding`, not into retro prose." | — | K → F-2 | — |

### §3.13 role-rules re-points (C-6)

| id | new carrier file | anchor (unchanged) | lands with |
|---|---|---|---|
| letter-branch-settles-oracle | `references/slices/qa-test-strategist/handoff-keys.md` | "whose answer settles the oracle" | ts-3 |
| designer-card-observation-sufficiency-review | same | "each with `sufficiency_review {author_dispatch_id" | ts-3 |
| case-id-in-briefs-form | `references/slices/qa-case-designer/handoff-keys.md` | "this brief's `Case id form:` line" | cd-1 |
| case-id-note-not-read-by-code | same | "form is not read by code" | cd-1 |
| designer-card-reuse-decision-vocabulary | same | "extend:<case id>\|dedupe:<case id>" | cd-2 |
| designer-one-case-per-plan-row | same | "an `unverifiable` row too" | cd-4 |
| designer-now-before-keys | same | "keys its texts `now` / `before`" | cd-4 |
| merge-keep-only-for-p16-p19 | `references/slices/qa-case-critic/handoff-keys.md` | "keep starts P16 or P19" | cc-1 |
| critic-card-over-plan-case-budget-line | same | "case budget:` line" | cc-1 |
| scribe-card-delivery-ready-line-is-the-blocks | `references/slices/qa-doc-scribe/handoff-keys.md` | "is the block's (check_delivery.py feeds it)" | ds-2 |
| tester-card-derived-row-also-gets-a-behaviour-claims-row | `references/slices/qa-requirements-tester/handoff-keys.md` | "`derived` row only the diff speaks" | rt-3 |

A page where `--write` puts the row on `handoff-keys-2.md` takes that file. The anchor must count 1 on that page (F7): if a
segment appended twice (M1 on two rows read by the same role) makes it 2, the builder lengthens the anchor within the
segment's own words (2-6 words, F7 limits) and names it.

### §3.14 Accounting by card

| card | segments | to rows (V / P) | told elsewhere | K (charter by F-2) | question |
|---|---|---|---|---|---|
| qa-scout | 5 | 3 (2 V, 1 P) + 1 door | 1 | 0 | P resolves |
| qa-requirements-tester | 6 | 5 (4 V, 1 P) | 0 | 1 (dropped framing) | — |
| qa-test-strategist | 4 | 3 (P) | 0 | 1 | P resolves |
| qa-case-designer | 4 | 4 (3 V, 1 P) | 0 | 0 | — |
| qa-case-critic | 1 | 1 (V) | 0 | 0 | — |
| qa-automator | 6 | 5 (3 V, 2 P) | 0 | 1 by F-3 | au-4 |
| qa-code-critic | 4 | 3 (1 V, 2 P) | 0 | 1 | — |
| qa-runner | 6 | 6 (5 V, 1 P) | 0 | 0 | — |
| qa-failure-analyst | 1 | 1 (V) | 0 | 0 | — |
| qa-doc-scribe | 7 | 7 (V) | 0 | 0 | — |
| qa-bug-reporter | 4 | 3 (V) | 1 (br-3, conditional) | 0 or 1 | — |
| qa-retro-analyst | 4 | 2 (P) | 0 or 1 | 2 | ra-1 may turn K |
| **12 cards** | **52** | | | | |

---

## §4 The six held-out rows (dispatch F-5 (a)): sentences in full

| id | lands in | roles / stages / when / door_needs | requirement (full) | door | what code checks (owner: data) |
|---|---|---|---|---|---|
| `s5_precheck:sides.provisional` | this node | qa-automator / ["S5"] / ["window", "shell"] / shell | "Every live `provisional[]` row of this window has a `kind` from `references/provisional-kinds.json`, a `settles_on` that is a side of this story, a `home.file` whose placeholder line carries the comment `qa-provisional: <id>`, and `dependents` as a list of `{case, then}` that are bound in `then_bindings`; every `qa-provisional: <id>` marker in a test file of the window has its `provisional[]` row." | "send the row or the field through `manifest_put.py --fragment`, or take the marker out of the test file" | presence and joins: kind in a data list, side name in the story record, marker line in the file, dependents ⊆ then_bindings, marker → row (`s5_precheck.py` 2085-2149) |
| `s5_precheck:sides.pending` | this node | qa-automator / ["S5"] / ["window", "shell"] / shell | "On a story with sides, a `pending_implementation` row of a case in scope stands only while a side its test declares is `absent`: an instance that can run owes its run, and a row whose every instance has run stamped real on every side its test names is retracted." | "run it (`run_suite.py --mine <case>`) and retract the row through `manifest_put.py --fragment`, or declare the absent side in the test's `sides` when one really is" | joins: pending row ↔ declared sides ↔ latest terminal runs (`s5_precheck.py` 2152-2179) |
| `execution_request:profile.none` | this node | the `--mine` roles of `execution_request:profile` (same producers) / same stages / ["shell"] / shell | "`qa-factory/config.json` holds at least one execution profile that can run the asked cases; with none, `--mine` cannot build the run." | "report it in your digest as an onboarding gap, and write this one run with `run_suite.py --template request`" (F-P2-3 (a), accepted; the refusal text gains it in T5b) | presence of a profile (`execution_request.py` 1790-1797) |
| `execution_request:fingerprint` | this node | same as above / same / ["shell"] / shell | "The inputs of a `--mine` run can be fingerprinted when it is built: every test, helper, config and dependency file it reads exists and keeps its bytes while it is hashed, and the stand's runtime provenance is `matched`, confirmed by the person, or `not_applicable`." | "report it in your digest, and write this one run with `run_suite.py --template request`" (F-P2-6 (a), accepted) | presence and byte identity of files, provenance result word (`execution_request.py` 3714-3724; `execution_fingerprint.py` 73-92, 104-151) |
| `stage_done:set` | T9c (conductor producer, dispatch F-6 (a)); sentence fixed here | conductor / ["*"] / ["move:story_fact"] / none | "`stage_done.py --set` takes `key=value` items and writes only the keys it lists: `implementation_source`, `size`, `environment_pending`, `no_trace`, `retro_mode`, `environment`, `parent_feature`, `sides.<name>.<attribute>` and `sides_unknown`; a closed key takes one of its listed words (true/false for the two flags, a reality word of `references/side-realities.json` for a side's `reality`, `retro_mode` only `full`), `parent_feature` is the parent's key alone, and a person's word does not widen the list." | "give the value in the key's form, or have the script that owns the field write it" | the key list and the value forms (`stage_done.py` 71-86, 92-157, 218); O-1 included (whitelist and `key=value` form) |
| `planning_contract:plan.unmarked_revision` | T9c (conductor-only sub-row, F-W4 (b)) | conductor / ["S3"] / per T9c | NOT WRITTEN: the meaning of `planning_contract.py::unmarked_revision_errors` (wave0 cites :273-283) was not read in this pass | — | fork F-8 |

---

## §5 Edges (each with its invariant)

- **A card segment with no row to carry it** (no V/P target, or P finds no function): rule P stops the builder; the segment is a
  question; the card is NOT emptied until every segment has a status. Invariant: no check-stating card clause ever leaves the
  package without a row (or a named row that already tells it). The `cards: {}` write is the LAST step of C-4, after the
  coverage table is complete.
- **A card read by a role that has no key page**: today none (F5). Invariant: a row lands on a role's page only when that role
  lists the page; `_page_leg` stays red otherwise ("does not receive"). If a role lost its page line, C-7 red stops the node.
- **Two cards mapping to one row**: one id, one row (E7 red on two). Segments of different roles on one id: rule X gives each
  role its own sub-id; segments of the same role concatenate in card order, a byte-identical segment is written once.
  Invariant: no role is told another role's card words; no two rows share an id.
- **A role whose page grows past K8 / K10**: K8 WARN or red → the split line in inject-map.json in the same commit (never a cut,
  never a shortened sentence); K10 over H and over baseline → F-4 (recommended: named raise = measured U, the report names
  role, U, H, old → new, Appendix A). Invariant: no sentence is truncated to fit; no raise is unnamed.
- **TEMPORAL — a story started before the change** (its brief `work/briefs/<ID>.md` written with the hand card, its pages
  from the old plugin): the brief file is not rewritten; a dispatch already running keeps the card it was given (the rows carry
  the same words, so nothing contradicts); every dispatch after the plugin update gets the pages (rows) and a brief with no
  ahead section. A rework of an old dispatch rebuilds its brief from the new plugin. Invariant: a role is never told less than
  before at any point (card OR rows, never neither); the plugin generation is one per run (B-014), so no dispatch mixes them.
- **TEMPORAL — the world between this node and T3b**: `brief_pack.ahead_card` reads `cards: {}` → "" → no brief section
  (F4); `contract_slices` shows no `### Not yet in rows` (F3). Before this node: the card is told twice (brief + page). After:
  once (page). Invariant: the page is injected whole (inline subject, T3a), so the requirement still reaches the role before
  its work.
- **Empty / absent**: `ahead-cards.json` absent or unparsable after this node → `_hand_cards` red "cannot be counted" (never 0;
  unchanged code). `cards: {}` → 0. A segment whose P-function is found but whose row is `requirement_from`: rule R.
- **Conflict M1 vs J1 ownership of T1r sentences**: M1 appends and never rewrites; a rewrite is a fork (F-1 (b)).
- **Error direction of reused functions in a new role**: `contract_slices.ahead_card` / `brief_pack.ahead_card` (advice
  renderers) are not promoted to gates. `role_rules` anchor count may err toward "lost" (red, visible) when a page renders the
  anchor split by markup; never toward "holds" — adversarial inputs that must stay red: the anchor only inside a marker
  comment, the anchor twice on one page, the anchor on another role's page only. The page leg `_page_leg` may err toward "not
  told" (red); never toward told on a page nothing renders (T3a K2).

---

## §6 DoD (inline; narrow witnesses only, no CI wait, no mutation pass — PROJECT.md «Командная работа» п. 13)

Acceptance keys: (1) `stage_joints.py --check` clean with `told counters: hand_cards 0, legacy_legs 0, unsited <N>` and N
equal to the stored ceiling, every unsited row named with its siting node; (2) `contract_slices.py --check` clean, no `WARN K8`,
K10 green; (3) `role_rules.py --check` 0 findings; (4) every segment of §3 has a final status in the report table; (5) the F19
tests and the keep tests listed by the witness command green; (6) ratchet rows named.

Commands (from the worktree root `C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r-cards`):

1. `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for references/stage-joints.json references/ahead-cards.json design/role-rules.json references/role-load.json references/inject-map.json scripts/tests/test_ahead_cards.py` — run every non-slow file it lists, each alone.
2. `python -B ai-packages/qa-factory/scripts/contract_slices.py --write` then `python -B ai-packages/qa-factory/scripts/contract_slices.py --check`
3. `python -B ai-packages/qa-factory/scripts/stage_joints.py --check`
4. `python -B ai-packages/qa-factory/scripts/role_rules.py --check`
5. `python -B ai-packages/qa-factory/scripts/tests/test_ahead_cards.py`, `test_contract_slices.py`, `test_role_rules.py`, `test_role_load.py`, and each F19 file the node edits (not quarantined, not SLOW_TESTS)
6. `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang`
7. `python -B ai-packages/qa-factory/scripts/tests/test_stage_joints.py` — ONCE (about 146 s), last.

census: no new blocking unit (`test_judgment_census.py` is in the witness list if `--witness-for` names it; run it then).

---

## §8 Forks (returned, not decided)

- **F-1 How a card segment joins an existing T1r row.** (a) Append verbatim (M1); (b) a merged rewrite per row, J1-reviewed;
  (c) always a sub-id row `<id>.card`. Recommend (a): no rewording by a builder, no lost words, one row per check; cost: some
  over-telling on pages (a few hundred bytes per role). (b) costs a designer pass with every final sentence written; (c) doubles
  lines for one check. Card follows (a).
- **F-2 Card clauses that state procedure / advice / rationale (K: rt-0, ts-0, ck-1, ra-2, ra-4, maybe au-4, ra-1, br-3).**
  (a) charter line when the charter lacks it, dropped when present; (b) drop all (the charters carry the procedure today —
  unmeasured); (c) keep them in rows (AR-29 breach: a row would claim a check that does not exist). Recommend (a): no clause
  lost, P27 kept; cost: charters grow a few lines (the `charter` layer of role-load and K10, measured in C-8/C-9; owns adds
  `agents/`). Card follows (a).
- **F-3 au-4 "Smells refused".** The parent says the smell family is advice (never a refusal); the card says "refused".
  (a) the code decides: a blocking smell → row on `s5_precheck:*`, advice → K (charter); (b) a row anyway. Recommend (a);
  the contradiction is reported (one of the card or the parent is wrong about the code).
- **F-4 K10 / native headroom after T1r's rows and this node.** T1r's PT/SG/HA rows with `roles: ["*"]` reach every page;
  growth is not measured here (no shell in this pass). Options: (a) named raise: baseline = measured U for every role over H
  (new rows for roles newly over H), report names role, U, H, Appendix A; (b) stop the node and narrow rows (e.g. move `*`
  rows behind capability tokens) — a T1r redesign; (c) the owner removes the Codex ceiling (Appendix A finding). Recommend
  (a) for tonight (reversible data, the forge watches size), with the morning line to the owner: which roles moved closer to
  the Codex 100000 refusal and by how much. Card follows (a).
- **F-5 The brief between this node and T3b.** (a) accept: the brief loses its card section now, the page carries the rows;
  (b) keep the cards until T3b (hand_cards stays 12; contradicts the node's goal and P31). Recommend (a). Card follows (a).
- **F-6 The file ahead-cards.json.** (a) keep it with `cards: {}` (parent §5.1 T1r row says so); (b) delete it and teach
  `_hand_cards` absent → 0 (breaks "never 0 on unknown", AR-28). Recommend (a). Card follows (a).
- **F-7 Tests that read card text (F19).** (a) re-point to the page text through one helper (C-10); (b) quarantine them.
  Recommend (a): the pins (closed lists, quoted numbers, B-194 fields) keep their meaning on the new carrier. A quarantined
  file among them is not edited (non-goal) and named in the report.
- **F-8 `planning_contract:plan.unmarked_revision`: meaning not established.** The sentence needs `planning_contract.py`
  `unmarked_revision_errors` (wave0: :273-283) read; this pass did not read it. (a) T9c's dispatch carries "read the body,
  write the sentence, Lead accepts" (the row is T9c's anyway); (b) a short designer pass now. Recommend (a). Card: no action.
- **F-9 Landing node of `stage_done:set`.** (a) T9c (conductor producer, dispatch F-6 (a)); (b) here, with `_producer_leg`
  accepting the conductor (a code change outside owns). Recommend (a). Card: no action; sentence fixed in §4.
- **F-10 Placement P resolved by the builder under rule P (one function or STOP)** vs a second designer pass placing every P
  segment on the body. Recommend rule P: the Grep is deterministic and a miss stops the node; cost: up to 15 Greps.

### Lead decisions on the forks (14.11.2026, owner away — by recommendation, listed in the morning report)

F-1 (a) append verbatim. F-2 (a) a procedure clause goes to the role's charter when the charter lacks it; never into a row.
F-3 (a) the code decides; the contradiction is reported. F-4 (a) a NAMED raise per role (role, U, H) — the owner is told in the
morning which roles moved toward the Codex ceiling and by how much; a role that would CROSS the ceiling stops the node (no raise
past the refusal). F-5 (a). F-6 (a). F-7 (a). F-8 (a) and F-9 (a): both rows land in T9c. F-10 rule P. S-1..S-6 accepted.
The draft goes to a plan critic (t-703) before any builder dispatch; the builder starts only after T1r (t-693) is accepted.

## §9 Small choices closed by the designer

- S-1 Report `20261114-t1r-cards-report.md`; changelog fragment `tbw-t1r-cards.md`; worktree `tbw-t1r-cards`.
- S-2 Segments split at the card's sentence boundaries where one check owns the sentence; a sentence quoting two checks stays whole on the first.
- S-3 `role_rule` on a row carrying two role-rules sentences: the first in card order; the second named in the report (the K7 key holds one id).
- S-4 Sub-id suffix for rule X: the role name without `qa-`.
- S-5 `T1rc/` prefix for new test ids in `test_contract_slices.py`; `ahead/` for `test_ahead_cards.py`.
- S-6 The `note` of ahead-cards.json rewritten (C-4) instead of left stale.

## §10 Reading trail (tbw-t1r unless noted)

- Repo root: `docs/tasks/specs/20261114-told-before-work-t1r-t2-dispatch-spec.md` whole; `20261113-told-before-work-mechanism-spec.md` 195-294, 340-404, 400-599 (§2.6-§2.8, §5.0-§5.6); `20261113-told-before-work-t1-revision-spec.md` Grep (346-347, 463-464); `wave0-rows.md` 240-269 and Grep hits (109, 127, 322-323, 347, 376, 404); `wave0-rows-part2.md` 50-94, 200-269; `wave0-rows-part3.md` Grep hits (150, 271, 283).
- `W\references\ahead-cards.json` 1-95; `stage-joints.json` 1-240 and the `"check":` Grep (rows 9-1093); `inject-map.json` whole; `role-load.json` whole.
- `W\design\role-rules.json` lines 7, 64, 161-166, 181, 306, 347, 467, 482-484 (Grep `ahead-cards`, count 11; line 161 read).
- `W\scripts\contract_slices.py` 465-943; `stage_joints.py` 1-170, 270-399, 400-599, 660-990, 990-1149; `role_rules.py` 1-60 and def Grep; `brief_pack.py` 385-424 and Grep `ahead` (4481, 4545-4546); `validate_artifacts.py` def Grep and 2350-2419, line 103; `exit_gate.py` Grep and 1575-1664; `s5_precheck.py` 2040-2184; `execution_request.py` 1785-1834, 3705-3734; `execution_fingerprint.py` 70-164 and `raise ValueError` Grep; `stage_done.py` 68-157 and Grep (218).
- `W\scripts\tests\test_ahead_cards.py` whole; Grep `ahead-cards|ahead_card|hand_cards` over `W` (F19 list).
- Reports: `W\..\docs\tasks\specs\reports\20261114-t3a-report.md` whole; `20261114-t2-report.md` 1-60.
- Negative claims and controls: "no T1r report yet" — Glob `**/2026111*-t1r*` under the tbw-t1r docs found nothing; control: the same Glob form `**/20261114-t2-report.md` found the T2 report. A Glob at the worktree root returned nothing (miscall, as in t-677); no claim rests on it. "No wave0 hit for `exit_gate:(scoped|...)`": control — a case-insensitive Grep of `scoped|grounding|case_identity|L1` in `wave0-rows.md` found item 7 (the exit families have no drafted sentence there).

## §11 What I did NOT establish

- The real sizes after T1r (U, page bytes, tokens): no shell in this pass; every K8/K10/role-load number is the builder's measurement (C-1, C-7..C-9).
- The function bodies behind every **P** segment (sc-3, rt-4, ts-1..3, cd-4, au-4..6, ck-2, ck-4, ru-1, ra-1, ra-3); rule P resolves or stops.
- Whether `s5_precheck`'s smell family blocks (au-4, F-3).
- Whether `planning_contract:plan`, `coverage_contract:obligations(.observation)`, `critic_rollcall:*`, `check_coverage:*` carry a requirement after T1r (A1, A3): M1 vs M2 follows what the merged tree shows.
- `planning_contract.unmarked_revision_errors` body (F-8).
- Which of the F19 tests are quarantined in `test-layers.json` (only `test_ahead_cards.py` / `test_ahead_cards_rules.py` keep rows were seen in the Grep hits).
- Whether the charters already carry the K clauses (F-2 decides per clause by Grep).
- Whether `qa-bug-reporter` has a shell (br-3 branch).
- The sited status of the new ids (`source_preflight:*`, `check_witness:*`, `estimate_record:*`, sub-ids under `validate_artifacts:*`); `unsited` after this node is measured, not predicted.

Needed beyond the manifest (this draft): `execution_fingerprint.py`, `stage_done.py`, `s5_precheck.py`, `execution_request.py`, `brief_pack.py`, `role_rules.py`, the wave0 part2/part3 files, the T3a and T2 reports.

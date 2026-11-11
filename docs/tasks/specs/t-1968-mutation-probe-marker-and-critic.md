# t-1968 — EP3-1: the mutation probe proves "failed by the broken check" by its own marker; a text it cannot read goes to the code critic, not to a person — SPEC (designer, revised after critic-on-plan t-1970)

Status: critic-on-plan t-1970: fit_with_fixes; fixes R1–R14 applied.
- R1 (ratchet numbers wrong, the form is process) → §3 N3 "Ratchets": measured numbers from t-1970, the byte deltas of every change, the cut list; no row raised.
- R2 (drop the form's `judgment:` row) → §3 N3 "Exact text" (the row is not added; the record is the one carrier).
- R3 (missed `data_row` readers; re-key, not remove) → §3 N2 owns + item 7 (every reader listed, re-keyed to `cause: judgment`).
- R4 (no new refusal in `window_record.run`) → §3 N2 item 5 (the probe-missing note's tail names the judge door; the sent-back receipt untouched, tested).
- R5 (`cannot_judge` is not `probe_could_not_run`) → §3 N2 item 4 + N5 (own predicate, own question, own word; the class word untouched).
- R6 (S6-close re-probe gives an unjudged record) → §3 N2 item 8 + E2.11 (route: the close asks nothing, the delivery reason says "not proved").
- R7 (marker searched only in failure/error problem text) → §3 N1 item 3 + E1.11 + test.
- R8 (runtime join, format-character guard) → §3 N1 "Data" (`marker_expr` per language, joined at run time) + guard + E1.3.
- R9 (marker present, frame outside the statement) → §3 N1 item 3 + E1.12.
- R10 (one door constant; `--dispatch` in the charter) → §3 N2 item 3 (`JUDGE_DOOR`), N3 :70 text, pin test.
- R11 (census unit name) → §3 N2 item 3 (`judge_record`, matches `UNIT_NAME_RE`), §3 N3 "Census".
- R12 (N3 owns) → §3 N3 owns (vocabulary.yaml:135, s5.md:163/:170/:200, two charter test files, slice regeneration).
- R13 (`target` has a reader) → §3 N4 (receipt core, window probe block, `proof_level.receipt_off_target`, the window gap, charter bullet).
- R14 (table corrections) → §3 N1 table (both JUnit imports skip; M-CS3 3-arg variant; NUnit 4 classic "sure").

Decided by the Lead, 05.11.2026:
- F1 = C: the place of the failure alone is NOT a proof; it is a fact handed to the critic. **Lead's correction of the finding (step 2 of «Что именно менять»), to be told to the owner.**
- F2 = B plus R13: the probe records which line it broke; a receipt of a probe that inverted a line which is not the obligation's assertion does not count as the obligation's proof (FR-18) — by data, not by judgment.
- F3: the `data_row` readers are re-keyed, not removed.
- F5 = A (the craft bullet "Break the Then's own check"). F6 = A (`roles: ["qa-code-critic"]`).
- All 14 fixes accepted; no compatibility with records of an older package version; temporal edges only inside one run.

Decided by the owner, 05.11.2026 ≈20:25 (F4, «да» to A): when the critic cannot judge a probe, the person is asked SEPARATELY, with the
facts (which test, which check was broken, what the test printed), and decides «accept as not proved / send the test back to its author»;
an earlier «go on» given for probes the tool could not run never covers it. Node N5.

Node: EP3-1 of `plans/piles/execution-probes/batch-3-mutacionnaya-proba-marker-i-kritik.md` (П1). Finding:
`plans/piles/execution-probes/findings/20261105-mutacionnaya-proba-neznakomyj-tekst-otkaza-marker-i-kritik.md`.
Code read in `D:/ws1/wt-fbfix` (branch `fb-fix` at 32c1223c7: experiment head + the doors batch merged); `PKG\` =
`D:/ws1/wt-fbfix\ai-packages\qa-factory`. Facts §2 F1–F32 were read in wt-fb1 by the first draft; line numbers below that the revision
re-read in wt-fbfix are marked (fbfix). The builder re-reads lines in its own tree before editing.

---

## §1 Goal, AR-n / FR touched, owners and census class of every check

**Goal.** A mutation probe of a test in any language says "the broken check fired" by a fact the FACTORY controls (its own marker in the
broken check's message), keeps the library-wording rows as a fast path, and hands every failure it cannot read to the code critic as a record
of facts; the critic's verdict (quoting the record) closes the probe; when the critic cannot judge, the person is asked that one question,
with the facts. The probe records which line it broke, and a probe of another line never counts as the obligation's proof.

**AR-n touched (change check → in the DoD of).**

| AR | how | change check (DoD of) |
|---|---|---|
| AR-1 closed variety is data | how a message attaches to an assertion form = row field `message` of `detectors.json`; the person's new word = a row of `block-names.json` | N1 `test_marker_forms_are_rows`; N5 `test_not_proved_word_is_a_block_row` |
| AR-2 open variety is judgment | an unknown failure text is the critic's, never a new phrase list | N2 `test_unknown_text_is_judgment_not_a_phrase_match` |
| AR-7 / AR-29 code judges data | marker = join of a token the factory placed; `judge_record` checks presence/joins only; `target` = equality of two line numbers | N1, N2, N4 census rows below |
| AR-9 refusal names a door | every `--judge` refusal names what it expected and the command; the window note names `JUDGE_DOOR`; the off-target gap names `--at` and the person's word | N2 `test_judge_refusals_name_the_door`; N4 `test_off_target_gap_names_both_doors` |
| AR-10 requirement before the work | the critic is told in the charter, the form and the record | N3 pins |
| AR-13 one reader | `proof_level.probe_record_state` THE reader of a record; `proof_level.receipt_off_target` THE reader of `target` (window and delivery) | N2, N4 tests |
| AR-14 one writer | `probe_by_code.py` the only writer of records and receipts; `judgment` only through `judge_record` | N2 `test_judgment_written_only_by_probe_by_code` |
| AR-16 one question form | the cannot-judge question goes through the S5 seam (`no_move` state, the `rows` pattern), text per `human-questions.md` | N5 `test_lead_obeys_human_text_rules` |
| AR-19 stage twins | `window_record.probe_gap_block` ∥ `acceptance.probe_gap_named` change together (N2 and N5) | both in one commit per node |
| AR-20 shrink-only ratchets | `role-load.json` rows of `qa-code-critic`: NOT raised (cuts, §3 N3); census `blocking_per_role.qa-code-critic` 130 → 131 only if printed | N3 witness `role_load.py`; census test |
| AR-22 producer and readers together | `cause: data_row` → `cause: judgment`: every reader re-keyed in N2's commit (R3 list) | N2 `test_no_reader_of_data_row_left` |
| AR-23 declared empty outcome | `message: []` = form takes no message; `target.is_assertion_id: null` = unknown | N1, N4 tests |
| AR-24 a person's words whole | a probe-gap word never covers a `cannot_judge` test; the new word is read only for its own class and only after the judgment | N5 `test_go_on_for_tooling_never_covers_cannot_judge` |
| AR-25 every state has a way out | `cause: judgment` exits: `fires` / `other_failure` / `cannot_judge` → person (N5); S6-close unjudged → delivery reason; off-target → `--at` or the person's word | one test per exit |
| AR-27 owner of what reaches the report | `cannot_judge` / unjudged stays factory-owned (`review_unverified_factory` re-keyed) | N2 `test_cannot_judge_left_item_is_factory_owned` |
| AR-28 an unknown never becomes a pass | an unjudged record is never a receipt; the place alone never proves; an off-target receipt never counts | N1/N2/N4 tests |

FR walked: A (FR-1, FR-2, FR-4, FR-57), B (FR-6, FR-7, FR-9: N5's word is kept whole), C (FR-12, FR-13, FR-38, FR-42), D (FR-18: off-target
receipt; FR-58; FR-59: unknown → `cause: judgment`, never a pass), E (FR-35, FR-41: S6-close), F (FR-41), G (FR-30, FR-32, FR-33 §6, FR-47,
FR-52, FR-54).

**Owners and census class of every check this spec adds or alters** (census rows `{file, function, class, roles, owner}`):

| check (file :: function) | added / altered | owner | census class | why it is not a judgment |
|---|---|---|---|---|
| `probe_by_code.py :: judge_detector` (N1 marker step; N2 E15 branch) | altered (row :596 fbfix, `shape`) | data | **xref** (raised from shape; no ceiling on xref) | joins a token the factory wrote with the run's failure text |
| `probe_by_code.py :: judge_record` (N2, the `--judge` executor) | added | judgment (carries the critic's verdict) | xref | record exists, same bytes, owed, word in 3, dispatch open, quote is a substring. Never whether the quote proves it |
| `proof_level.py :: receipt_off_target` (N4) | added | data | not a unit (name outside `UNIT_NAME_RE`) | compares two line numbers |
| `acceptance.py :: validate_window` (N4: off-target → `semantic_sensitivity`) | altered (existing row) | data | unchanged class | reads `receipt_off_target` |
| `window_record.py :: probe_gap_block` / `acceptance.py :: probe_gap_named` (N2 remove data_row branch; N5 new word branch) | altered | intent (the person's word) | not units today (names outside the RE; verify in the census print) | equality joins + a timestamp comparison |
| `contract.py :: probe_not_proved_words` (N5) | added | intent | not a unit | reads `stage_overrides[]` like `probe_gap_words` |

---

## §2 Facts

The first draft's F1–F32 (read in wt-fb1) stand, with the critic's corrections (t-1970 §1): F12/F13 measured — the Playwright junit body
carries a code frame of the source (fixture `playwright-locator-author-message/tc001-in-stock.failure.txt`: `> 43 | await expect(catalog.cartBadge,
'step 1: …').not.toHaveCount(0);`, caret at col 79 = `toHaveCount`) AND echoes the RUNTIME message (`Call log: - step 1: badge empty before the
add …`). F28 measured: `role_load.py --role qa-code-critic --json` → tokens 18685, craft 1410, process 17275, total_bytes 74739; layers charter
10604 B, form 5096 B, injection_role 38546 B. F29 measured: census `blocking_per_role.qa-code-critic` = 130 = ceiling. F30 corrected:
`test_decision_classes.py` (15.7 s, `slow_tests.json:40`) and `test_check_delivery.py` (:22) ARE slow; NOT slow: `test_probe_gap_door.py`,
`test_assertion_detectors.py`, `test_judgment_census.py`, `test_code_critic_probe_rule.py`, `test_charters_s5_s9.py`, `test_contract_slices.py`.
`handoffs/vocabulary.yaml` has `probe_verdicts` (:130-135 fbfix; `incomplete` text :135). The critic's exit requires the review receipt
(`controller._code_review_problems`, controller.py:6790-6833 wt-fb1).

Re-read in wt-fbfix for this revision:
- G1. `role-load.json:2` (fbfix): the process row is "SHRINK-ONLY, slack-0 … process above its row, below its row … turns A22 red" (dense: the
  row must EQUAL the measured process); the total row may sit up to `ratchet_slack_tokens` 1000 above the measured (:9). `role_load.py:36,488`:
  tokens = ceil(total_bytes/4), craft_tokens = ceil(craft_bytes/4), process = tokens − craft_tokens.
- G2. The critic's injected files (`inject-map.json:68-75`): slices `common-rules.md`, `handoff-keys.md`, `execution-lifecycle.md`,
  `artifact-contract-automation.md`, `test-code-patterns.md`, `code-review-rubric.md`, project `framework-rules.md`. `vocabulary.yaml` and
  `s5.md` are NOT in the critic's load. `handoff-keys.md` (generated from the form) echoes field placeholders (`:32-33`), not `#` comments.
- G3. `references/execution-lifecycle.md:60-61` (section `<!-- roles: qa-code-critic -->`, only the critic's slice carries it, `slices/qa-code-critic/
  execution-lifecycle.md:24-25`): "so is what `probe_by_code.py` cannot read of a non-Python test (frame, message, a launcher that may not rebuild):
  no verdict" — false for a message at the mutated line after N2. Not in the verdict; found by this revision. Also
  `references/gate-registry.json:572` "… a message its table does not know …" (the `probe_verdict` row text) — same class.
- G4. Charter pins (fbfix): `test_code_critic_probe_rule.py:21` KEYS (incl. "the probe's `data_row` case", "read the probe-run log",
  "`expect(received).not.toBe`"); `test_charters_s5_s9.py:55` craft keys "beside its Then", "never beside the code", "could not verify", "a hint to
  read"; `:250` M1 Tools tokens incl. "`contradicts_requirement`", "the probe's `data_row` case", "`sensitivity_proof_missing_reason`";
  `:281` "`cause: data_row`" absent; `test_red_window.py:598` "a red test with its `contradicts_requirement` row takes no probe" in Tools;
  `test_case_alternatives.py:126-141` (:62 Tools); `test_s7_control_experiment_texts.py:90,93` (:71); `test_s5_precheck.py:3164` (:63).
- G5. `window_record.build` (fbfix :1077-1102): a green owed item with no receipt and no gap gets the note `_origin_text("probe") +
  PROBE_GAP_DOOR` (:1102), printed as the ` — ` tail of `<iid>: probe is missing …` (`verdict` :1294); `_sent_back_lines` (:1602) matches
  that line with or without the tail. `run` (:1612-1710): non-derivable lines → exit 1, no receipt.
- G6. `probe_gap_block` (fbfix :616-652): person word by id / case key / `tooling:<lang>` (:639), class word only when `probe_could_not_run` (:641),
  factory `data_row` last (:644-645). `probe_gap_cases` (:655-685). Twin `acceptance.probe_gap_named` (:874-916). `contract.prefix_value`
  (:115) takes ONE token; instance ids are phrases (window_record.py:98-103), so a person's per-test word keys on the CASE KEY.
- G7. `references/block-names.json:20-25`: `probe gap: <case key or tooling:language>`, reader `contract:probe_gap_words`, `class:
  probe_gap_accepted` — the class that widens one word to every could-not-run test.
- G8. `story_run.window_round_gate` (fbfix :6018-6027): the S5 probe-gap state; `probe_gap_lead` (:5934-5948, owner-confirmed text);
  `seam_chosen` (:16050-16077) records `probe gap: <case>` on `go_on_as_is`; `rework_stage` without args goes to the conductor with the words.
- G9. `story_run.s6_reprove` (fbfix :11675-11733): the driver re-probes stale live checks at the S6 close with `--dispatch <running S6>` or
  `--s6-close`; a verdict other than `intended_failure` is one digest line, no question; S6 closes (`s6_reprobed_close` :11735-11756).
- G10. `check_delivery` (fbfix): a required live check with no valid current receipt is a delivery reason "requires current sensitivity proof"
  (:983-989, `PL.reached`); `unverified_records` (:1887-1904) and `factory_data_gap_findings` (:1907-1923) key on `_is_factory_data_gap`
  (:1874-1884); `delivery-verdict-kinds.json:55` `review_unverified_factory` after_checks / factory; `report_facts.py:2179`.
- G11. `acceptance.validate_window` (fbfix :1063-1087): `sensitivity:` gap on a probe that is not a valid intended failure; `semantic_sensitivity:`
  when obligation ids / hash / defect location / `assertion_id` copies differ.
- G12. Census (fbfix `judgment-census.json:4`, `test_judgment_census.py:58,199-262,340-351`): a unit is u1 by name (`^judge…` matches, `_judge…`
  does not), or u3 by a refusal site of `refusal_registry.sites`; it BLOCKS when a site sits in it or its file is on the blocking path; a blocking
  unit counts once per role in `roles`. No census row exists for `window_record.probe_gap_cases` (not a unit).

### Analogs noticed, NOT widened
- Census rows of `probe_by_code.py` name `conductor` though the critic calls the tool.
- Python `wrong_location` with `mismatches: ["reason"]` (F7) — the same class as E15, decided the opposite way.
- `probe_debt.py` replays `MUTATIONS` only (whether it re-probes `cause: judgment` records not read).
- Accepted probe gaps are not listed in "Left with you" (t-1959 Q2).
- Fixtures under `scripts/tests/fixtures/run-12586-red-then/.../S5-qa-code-critic-*.yaml` carry old copies of the form comments (data, not pins).

---

## §3 Nodes

Shared vocabulary (STABLE across nodes):
- record `verdict` ∈ `intended_failure | no_failure | wrong_location | not_executed | incomplete` (no new word).
- E15 slot: `verdict: incomplete`, `cause: judgment` (replaces `data_row`), plus `judgment_facts`.
- record field `proved_by`: `marker` | `fires_as` | `critic` on every detector-path `intended_failure` (absent on Python).
- record block `judgment`: `{"verdict": "fires"|"other_failure"|"cannot_judge", "quote", "why", "by": <dispatch>, "at": <UTC ISO>, "facts_sha"}`.
- record and receipt field `target`: `{"line", "end_line", "assertion_id", "is_assertion_id": true|false|null}`.
- `probe_by_code.JUDGE_DOOR = 'probe_by_code.py --task <T> --dispatch <D> --judge "<instance>" --verdict fires|other_failure|cannot_judge --quote "<a line of its failure text>" [--why "<one sentence>"]'`.
- person's word `probe not proved: <case key>` (N5).

Order: **N1 ∥ N4** (disjoint functions of `probe_by_code.py`) → **N2** (after N1: same `judge_detector`) ∥ **N3** (text; merged after N2,
ratchet measured on the merged tree) → **N5** (after N2: reads `judgment`; touches doors functions of `story_run.py`/`window_record.py`).
Writer cap: at most 2 builders at once in this batch (N1 ∥ N4, then N2 ∥ N3, then N5).

### N1 — the factory's marker in the broken check's message, as data

**Owns** (absolute; functions):
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\probe_by_code.py` (`marker_token` [new], `_with_marker` [new], `plan_detector_mutation`, `_plan`, `judge_detector` — the marker step only, before the `passed` branch; `_judge_detector_rows` — copying `proved_by` only)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\assertion_detectors.py` (`message_forms` [new] — the one reader of the new fields)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\detectors.json` (`assertion_probes.<language>.marker_expr` [new]; `assertions[i].message` [new]; the key note)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_marker.py` (new, fast)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json` (row `probe_by_code.py::judge_detector`: class `shape` → `xref`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-1968-n1.md` (new)

**Data (R8).** Per language `"marker_expr"`: an expression that builds `qa-probe-<token>` AT RUN TIME from two pieces, never a `+` of two
literals (a transpiler folds that, and a code frame of the folded output would show the marker contiguous):
typescript `['qa-probe', '{token}'].join('-')`; csharp `string.Join("-", "qa-probe", "{token}")`; java `String.join("-", "qa-probe", "{token}")`.
Per assertion form `"message": [<variant>, ...]`, `[]` = takes no message (AR-23). Variant: `{"id", "at": "args_close"|"arg_start:<n>"|"after_args",
"args": <top-level argument count>, "string_arg": <n, optional>, "source": "<regex the file must match, optional>", "not_source": "<regex it must
NOT match, optional>", "not_after": "<regex, optional>", "insert": "<text with {marker}>"}`. Variants tried in order; first whose conditions
hold applies; none → no marker (a note), never a refusal.

**Rows** (sure = documented signature; to verify = the builder confirms on a real sample or the library source before committing; an unverified row
is NOT written):

| language / form | variant | insert | status |
|---|---|---|---|
| typescript `expect(` (T1/T2) | M-TS1 `arg_start:2`, `args: 2`, `string_arg: 2` | `{marker} + ' ' + ` | sure (Playwright `expect(v, msg)`, `expect.soft`; Jest throws on a 2nd arg, so a green 2-arg `expect` is not Jest) |
| typescript `expect(` | M-TS2 `args_close`, `args: 1`, `source: "from\\s+['\"]@playwright/test['\"]"` | `, {marker}` | sure for Playwright; a project importing `expect` from its fixtures module gets no marker (safe, named E1.1). Vitest: not written |
| typescript `assert.*` | `[]` | — | `invert: null` today |
| csharp xUnit `Assert.True/False` (X3/X4) | M-CS1 `args_close`, `args: 1` → `, {marker}`; M-CS2 `arg_start:2`, `args: 2`, `string_arg: 2` → `{marker} + " " + ` | — | sure (xUnit 2 and 3: `True(bool, string?)`) |
| csharp xUnit Equal/NotEqual/Null/NotNull/Empty/NotEmpty/Contains/DoesNotContain | `[]` | — | no message overload |
| csharp NUnit `Assert.That` (N1/N2) | M-CS3 `args_close`, `args: 2` → `, {marker}`; M-CS3b `arg_start:3`, `args: 3`, `string_arg: 3` → `{marker} + " " + ` | — | sure (NUnit 3 `That(actual, constraint, string message, params object[])`); NUnit 4 `That` (interpolated message) to verify |
| csharp NUnit classic `AreEqual/AreNotEqual` (N3/N4) | M-CS4 `args_close`, `args: 2` → `, {marker}` | — | sure (NUnit 3 and NUnit 4 `ClassicAssert.AreEqual(e, a, string message, params object[])`) |
| java JUnit 5 J1-J6 | M-J5 `args_close`, `args: 2` (1 for True/False/Null/NotNull), `source: "org\\.junit\\.jupiter\\.api\\.Assertions"`, `not_source: "import\\s+(?:static\\s+)?org\\.junit\\.Assert\\b"` → `, {marker}` | — | sure (message last) |
| java JUnit 4 same names | M-J4 `arg_start:1`, same `args`, `source: "import\\s+(?:static\\s+)?org\\.junit\\.Assert\\b"`, `not_source: "org\\.junit\\.jupiter\\.api\\.Assertions"` → `{marker}, ` | — | sure (message first). A file importing BOTH → neither variant applies (R14) |
| java AssertJ `assertThat(` (A1-A8) | M-AJ `after_args`, `args: 1`, `not_after: "^\\s*\\.(?:as|describedAs|withFailMessage|overridingErrorMessage)\\s*\\("` → `.as({marker})` | — | sure |
| python | — | — | unchanged (own marker, F1) |

**Required behaviour.**
1. `marker_token(instance_id, original_sha, started_at) -> str`: sha256 of `f"{instance_id}\0{original_sha}\0{started_at}"`, first 12 hex.
   `_plan` computes it once per probe; `plan_detector_mutation(..., marker_token="")`. `detail["message_marker"]` = `qa-probe-<token>`,
   `detail["message_form"]` = the variant id, both `""` when none applied; `detail["message_note"]` says why when a form had rows but none applied.
2. `_with_marker(...) -> (after2, variant_id, note)`, after `_inverted`, on the mutated statement. Guards (each failing → unchanged statement,
   `""`, a note; never a refusal): the variant's conditions; no line break in the inserted text; `lexical_shape` of the new file = that of the
   inverted file plus the inserted brackets; the contiguous `qa-probe-<token>` occurs nowhere in the new file text; the marker string holds no
   `%`, `{`, `}` (format-string arguments: NUnit message, AssertJ `as`, JUnit 4 is plain — one guard for all); the `fires_as` echo guard still
   holds. File = `text[:start] + after2 + text[end:]`.
3. `judge_detector` — ONE step, first among the failed branches: `detail["message_marker"]` non-empty, row `status == "failed"`, and the exact
   token occurs in the failing problem's `message` or `text` → `intended_failure`, `proved_by: "marker"` — WHATEVER the frame site says (R9:
   a soft collector's frame is at `assertAll`/the end of the test; the token is only in the text of the check that threw). The text searched is
   ONLY the `<failure>`/`<error>` problem body that `reporters` builds (reporters.py:208-211 wt-fb1), never system-out, attachments or step
   titles (R7). `passed` rows: not looked for. `error` rows: not decided here. Then today's table (`proved_by: "fires_as"`).
4. `_judge_detector_rows` copies `proved_by` into the record beside `verdict`.

**Edges (invariant each).**
- E1.1 Empty outcome (`message: []`, no `marker_expr`, no variant applies, fixtures-module `expect`) → today's table. INV: the marker only ADDS a proof the factory wrote; its absence never changes a verdict.
- E1.2 Only `failed` rows. INV: a passing inverted check stays `no_failure`/`incomplete`; an `error` row is never proved by the marker alone.
- E1.3 Echo (R8): joined at run time; source, code frame and transpiled output never hold the contiguous token (guard 2). INV: "a text that merely echoes the statement could pass for the intended one" stays unreachable. Residual (named): a printer of the RUNTIME string of a check that PASSED — closed by E1.11.
- E1.4 Another run's token never matches (`started_at` in it). INV: a receipt measured on another run never counts.
- E1.5 Truncation: the marker is placed FIRST in the message; a cut that drops it → today's table. INV: truncation only loses a proof.
- E1.6 Several report rows of one test: each judged; `_worst_of_rows` unchanged.
- E1.7 `expect.soft`: the token anywhere in the failing text proves THAT check threw. INV: no other check's text can carry this token.
- E1.8 Marker says fired, `fires_as` misses → marker wins, note names the missed row; the reverse → `proved_by: fires_as`.
- E1.9 Temporal inside one run: a probe planned before N1 has no `message_marker` → today's table. Older records not read (owner).
- E1.10 Inserted text ≤ 64 characters.
- E1.11 (R7) The token in system-out / a passed step title only. INV: never read; a passing check is never proved by its echoed title. Test.
- E1.12 (R9) Marker present, frame read outside the statement (soft collector, AssertJ `softly`) → `intended_failure` by the marker. INV: the token exists only in the mutated statement's message, so its presence in a failure text is that check's failure.
- E1.13 Matcher-internal errors (Playwright strict-mode violation, target closed) carry the custom message header (to verify on a sample). Named residual: such a run would read as fired; mitigated because the original test was green on the same state. The builder records the measured behaviour in the test docstring.

**Non-goals**: Python path; new/edited `fires_as` rows; any wording reader beyond the exact token; FluentAssertions; `probe_debt.py`.

**DoD** — `test_probe_marker.py` (fast, pure: `plan_detector_mutation`, `judge_detector` on in-memory text and rows):
`test_marker_forms_are_rows`, `test_ts_prepend_to_author_message` (real lines `add_to_cart.spec.ts:43`, `:105` → `await expect(catalog.cartBadge,
['qa-probe', 'abc123def456'].join('-') + ' ' + 'step 1: badge empty before the add').not.toHaveCount(0);`), `test_ts_add_message_only_with_playwright_import`,
`test_xunit_true_false_get_message`, `test_xunit_equal_gets_none`, `test_nunit_that_two_and_three_args`, `test_nunit_classic_gets_message`,
`test_junit5_last_junit4_first`, `test_junit_both_imports_gets_none`, `test_junit_without_import_gets_none`, `test_assertj_as_inserted_and_skipped_when_described`,
`test_marker_is_runtime_join_never_literal_plus`, `test_marker_never_contiguous_in_source`, `test_marker_has_no_format_characters`,
`test_marker_keeps_lines_and_brackets`, `test_failed_row_with_marker_unknown_text_is_intended`, `test_marker_with_frame_outside_statement_is_intended`,
`test_failed_row_without_marker_same_line_not_by_marker`, `test_other_token_not_counted`, `test_error_row_with_marker_not_intended`,
`test_passed_row_ignores_marker`, `test_marker_in_system_out_only_is_not_read`, `test_empty_message_list_skips_marker`, `test_fires_as_still_fast_path`,
`test_code_frame_echo_cannot_prove` (the real fixture `tc001-in-stock.failure.txt` with its code frame → no match).
Witness (fast, worktree root): `python -m pytest ai-packages/qa-factory/scripts/tests/test_probe_marker.py ai-packages/qa-factory/scripts/tests/test_assertion_detectors.py ai-packages/qa-factory/scripts/tests/test_judgment_census.py -q`; `python -B ai-packages/qa-factory/scripts/selftest.py --lang`.
CI only: `test_probe_by_code_languages.py`, `test_probe_by_code.py`. `architecture: AR-1, AR-23, AR-28, AR-29 -- the form of a message is a row; the marker only adds a proof the factory placed`. `judgment: judge_detector shape->xref`.

### N2 — `cause: judgment`: the critic judges the facts; the window closes on its verdict

After N1 is merged into the batch branch.

**Owns** (absolute; functions):
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\probe_by_code.py` (`JUDGE_DOOR` [new], `judge_detector` — the E15 return only; `_judge_detector_rows` — the `cause` aggregation :2624-2629 fbfix; `judgment_facts` [new]; `judge_record` [new]; `_judge_cli` [new]; `_build_parser`; `main` — the `--judge` branch before the probe branch; module docstring :54-70, :106-114)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\proof_level.py` (`probe_record_state`; `probe_could_not_run`; `probe_factory_data_gap` → re-keyed `probe_owes_judgment` [rename]; `FACTORY_DATA_GAP_KEY`, `FACTORY_DATA_GAP_WORDS` — removed; docstrings :1037, :1074)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\window_record.py` (`probe_gap_block` — the factory branch :644-645 removed, docstring :619-623; `build` — the probe note at :1102 only; `verdict` unchanged)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\acceptance.py` (`probe_gap_named` — the factory branch :911-915 removed, docstring :878-879; comment :46-52)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\check_delivery.py` (`_is_factory_data_gap` → `_owes_factory_judgment` [rename, re-key]; `unverified_records`; `factory_data_gap_findings` — re-keyed, code `PROBE_NOT_JUDGED`; caller :2548)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\report_facts.py` (:2179 tuple — unchanged words, verify)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\story_run.py` (`s6_reprove` — the digest line for a `cause: judgment` record only)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\delivery-verdict-kinds.json` (:55 note text of `review_unverified_factory` if any; kind kept)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\gate-registry.json` (row `probe_verdict` :572 — the clause "a message its table does not know")
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_marker_judgment.py` (new, fast)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_gap_word.py` (K21 :820-917 rewritten to `cause: judgment`; CI)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_decision_classes.py` (c4 :328-344; slow, CI)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_by_code_languages.py` (K4/K8/K10 :1862, :1920-1931, :1949-1956 → `judgment`; slow, CI)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json` (row `judge_record`; ceilings as printed)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-1968-n2.md` (new)

**Required behaviour.**
1. E15 (`judge_detector`): same condition; `incomplete`, `cause="judgment"`, note `"the run failed at the mutated statement and the factory cannot
   read its text; the code critic judges it: " + JUDGE_DOOR`. `_judge_detector_rows`: all `incomplete` rows `judgment` → record `cause: judgment`
   + `judgment_facts`; any other mix → `tooling`. No "place" step (F1 = C).
2. `judgment_facts(record, row, site, detail) -> dict` (pure): `file, line, end_line, statement_before, statement_after, frame, location, column`
   (regex `:(\d+):(\d+)\)?\s*$` on the frame line, else null), `status, message` (whole), `failure_text` (cut at 16384 chars, "…"),
   `message_marker, fires_as_pair, evidence_ref`. `facts_sha` = sha256 of its canonical JSON.
3. `JUDGE_DOOR` (vocabulary above) — ONE constant: the E15 note, the window note (item 5) and the error texts import it; the N3 pin checks
   the charter carries each of its flags (R10). `judge_record(task_root, root, instance_id, dispatch, verdict, quote, why)` — the ONE writer of
   `judgment` (AR-14); its name matches `UNIT_NAME_RE` (`^judge`) so the census sees it (R11). Refusals (exit 2, one JSON
   `{"status":"refused","error":…}`, nothing written), each naming what it expected and the door: no record (run the probe); other bytes
   (`proof_level.current_test_sha`; probe again); not `incomplete`+`cause: judgment` ("this probe owes no judgment: its verdict is <v>");
   a `judgment` present (probe again; never rewritten); verdict not in the three words; quote empty, > 300 chars or not a substring of
   `message`+`failure_text` after folding whitespace both sides ("quote a line of the stored text, or name `cannot_judge`"); `cannot_judge`
   without `--why` (1-300); `--dispatch` not the open S5 critic dispatch of the instance's window (`_dispatch_context`). Refusals use the module's
   existing refusal path; whether that is a `refusal_registry` site decides the census (§3 N3 "Census").
   Effects (then `atomic_json`, `publish_binding`): `fires` → `intended_failure`, `proved_by: critic`, `actual_location = expected_location`,
   `actual_reason = expected_reason`, `failure_kind: assertion`, `judgment`, then `attach_receipt` when `restore.verified`; receipt core gains
   `proved_by`, `judgment_quote`. `other_failure` → `wrong_location`, `actual_location = judgment_facts.location`, `actual_reason` = quote,
   `mismatches: ["reason"]`, `judgment`. `cannot_judge` → stays `incomplete`/`judgment` + `judgment` with `why`.
4. `probe_record_state` adds `"judgment": <word or "">`. `probe_could_not_run`: `incomplete` → True only when `cause` not in (`judgment`) —
   a `cause: judgment` record is NEVER "could not run", judged or not (R5): the doors seam and the class word never see it.
   `probe_owes_judgment(task_root, iid, sha) -> str` (renamed from `probe_factory_data_gap`): `"unjudged"` for `incomplete`+`judgment` with no
   judgment, `"cannot_judge"` with that judgment, `""` otherwise.
5. (R4) No new refusal in `window_record.run`. In `build` (:1102 fbfix): an owed green item whose current-bytes record `probe_owes_judgment ==
   "unjudged"` gets the note `"its probe failed at the mutated line with a text the factory cannot read; the code critic judges it: " +
   JUDGE_DOOR` instead of `_origin_text("probe") + PROBE_GAP_DOOR` — printed as the ` — ` tail of `<iid>: probe is missing …`. `"cannot_judge"`
   → the note N5 writes. The sent-back branch (`_sent_back_lines`) is unchanged and still writes the receipt for a `rejected` instance.
6. Window closing: `fires` → receipt → `_probe_from_receipt` → `approved` possible. `other_failure` → judged record, today's `wrong_location`
   road, no gap. `cannot_judge` → N5.
7. (R3, F3 re-key) Every reader of `data_row`/`FACTORY_DATA_GAP` re-keyed in this commit: `probe_gap_block` and `probe_gap_named` lose the factory
   branch (the factory no longer names a gap: an unjudged record is the critic's, a `cannot_judge` record the person's, N5);
   `check_delivery._owes_factory_judgment` = `probe_owes_judgment(...) != ""`; `unverified_records` keeps kind `review_unverified_factory`
   (after_checks, owner factory, AR-27) for those; `factory_data_gap_findings` writes `{"code": "PROBE_NOT_JUDGED", "entity": iid, "owner":
   "factory", "detail": "factory: the probe of <iid> failed at the mutated line with a text the factory could not read, and no judgment proved
   it; the test is left with you unprobed"}`; `report_facts.py:2179` keeps both kinds. Charter/form/s5.md readers: N3. Docstrings
   `proof_level.py:1037,1074`, `probe_by_code.py:69`, `acceptance.py:46-52`: say `judgment`. `gate-registry.json:572`: "a message its table
   does not know" → removed from the incomplete list, plus "; a failure at the mutated line whose text the tool cannot read is `cause:
   judgment`, owed the code critic's `--judge`".
8. (R6) S6 close. `s6_reprove`: a re-probe record `cause: judgment` → the digest line `"<iid>: the probe failed at the mutated line with a text the
   factory cannot read; nobody judges it at the S6 close, so the test is not proved again"`, no question, S6 closes (the factory does not stop).
   READER: `check_delivery` — the test has no valid receipt of its current bytes, so `_sensitivity_state`/`PL.reached` gives the existing
   delivery reason "requires current sensitivity proof" (FR-41: said as not proved, never as a fact of proof); `PL.reached`'s issue text for
   such a record names "its probe owes the code critic's judgment (`cause: judgment`)". The record does NOT wait for a critic window (none
   follows S6). `judge_record` refuses `--s6-close` (no open S5 critic dispatch).

**Edges (invariant each).**
- E2.1 (F1 = C) The place is never a proof; it is `judgment_facts.location`. INV: a throw inside the statement's arguments (`add_to_cart.spec.ts:59`) never becomes `intended_failure` by code.
- E2.2 Reused condition in a more consequential role: E15 moves from "advice" to "a record owed the critic's judgment before the window closes". Error direction: toward `cause: judgment`, never toward `intended_failure`. Adversarial inputs kept safe: empty failure text; only the author's message line; frame on the mutated line with a TimeoutError of an action; a code frame echoing the statement; a `status: error` row (stays `tooling`).
- E2.3 `--quote` presence only. INV: code never decides whether the quote proves firing (AR-29); relevance is the acceptor's (named residual).
- E2.4 Limits: `failure_text` ≤ 16384 stored; a quote beyond the cut refused; quote/why ≤ 300; whitespace folded both sides.
- E2.5 `cause: judgment` without `judgment_facts` cannot exist (one move). `incomplete`+`tooling` → `--judge` refuses; tooling road stays.
- E2.6 Temporal inside one run: a re-probe of the same bytes rewrites the record; `keep_standing_record` keeps a stored ON-TARGET `intended_failure` over a new `incomplete` (N4 owns that function).
- E2.7 Judgment on other bytes → refused. INV: a receipt measured on other bytes never counts.
- E2.8 Second `--judge` → refused. INV: a written judgment is never rewritten.
- E2.9 The critic finishes without judging: no receipt (exit 1 on the probe-missing line); the critic's exit is refused "not receipted"; the seam's fallback shows the line naming `JUDGE_DOOR`. INV: the person is never asked to judge a probe's text; `probe_gap_cases` never lists it (not "could not run").
- E2.10 "the critic decides" vs "a live receipt to be `approved`": `fires` writes the receipt; both hold.
- E2.11 (R6) S6-close unjudged record → digest line + delivery reason. INV: an unknown is never reported as proved (FR-41); S6 never stops for it.
- E2.12 Sent-back instance (critic `rejected`) with an unjudged record: `_sent_back_lines` matches the line with its new tail → the receipt is written as today. INV: t-1603 stands.

**Non-goals**: Python path; `contract.py` (N5 adds its reader); `probe_debt.py`; a new verdict word; any phrase list; the doors seam (N5).

**DoD** — `test_probe_marker_judgment.py` (fast; tmp task root; no run): `test_unknown_text_is_judgment_not_a_phrase_match`, `test_place_alone_is_not_a_proof`,
`test_judgment_facts_shape_and_cut`, `test_judge_fires_writes_receipt_and_proved_by_critic`, `test_judge_other_failure_is_wrong_location`,
`test_cannot_judge_is_not_could_not_run`, `test_unjudged_is_not_could_not_run`, `test_could_not_run_reads_judgment_through_record_state`,
`test_judge_refusals_name_the_door` (one per refusal), `test_quote_not_in_text_refused`, `test_quote_whitespace_folded`, `test_second_judgment_refused`,
`test_other_bytes_refused`, `test_judgment_writes_no_receipt_until_fires`, `test_window_note_names_judge_door` (the probe-missing line's tail
holds `JUDGE_DOOR`), `test_sent_back_receipt_still_written_with_unjudged_record`, `test_window_closes_on_fires_without_person_word`,
`test_cannot_judge_left_item_is_factory_owned` (`unverified_records` kind `review_unverified_factory`, finding `PROBE_NOT_JUDGED`),
`test_s6_reprove_judgment_record_is_a_digest_line` (`Driver` stubbed as in `test_probe_gap_door.py`), `test_delivery_reason_names_owed_judgment`,
`test_no_reader_of_data_row_left` (scan of `data_row` and `FACTORY_DATA_GAP` over `scripts/*.py` and `references/*.json` is empty; positive control: the
same scan finds `cause: tooling`), `test_judgment_written_only_by_probe_by_code`, `test_judge_door_is_one_constant`.
Witness (fast): `python -m pytest ai-packages/qa-factory/scripts/tests/test_probe_marker_judgment.py ai-packages/qa-factory/scripts/tests/test_probe_marker.py ai-packages/qa-factory/scripts/tests/test_probe_gap_door.py ai-packages/qa-factory/scripts/tests/test_judgment_census.py -q`; `python -B ai-packages/qa-factory/scripts/selftest.py --lang`.
CI only: `test_probe_gap_word.py`, `test_decision_classes.py`, `test_probe_by_code_languages.py`, `test_window_record.py`, `test_check_delivery.py`, `test_probe_by_code.py`, `test_story_run_*`.
Census row: `{"file": "probe_by_code.py", "function": "judge_record", "class": "xref", "roles": ["qa-code-critic"], "owner": "judgment"}` (F6 = A).
`architecture: AR-2, AR-9, AR-13, AR-14, AR-19, AR-22, AR-25, AR-27, AR-28, AR-29`.

### N3 — the critic's charter, form, vocabulary and slices (experience, inside the ratchets)

∥ N2 (text against the stable vocabulary); merged after N2.

**Owns** (absolute):
`D:/ws1/wt-fbfix\ai-packages\qa-factory\agents\qa-code-critic.md` (:45, :48, :70; one craft bullet after :48; one Tools bullet after :70)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\handoffs\s5-critic-to-automator.yaml` (comments :51-52, :58, :67-72, :84-86 only; no new key)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\handoffs\vocabulary.yaml` (:135 `probe_verdicts.incomplete`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\execution-lifecycle.md` (:60-61)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\slices\qa-code-critic\execution-lifecycle.md` (regenerated: `python -B ai-packages/qa-factory/scripts/contract_slices.py --write`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\role-load.json` (`process_ratchet_tokens.qa-code-critic` lowered to the measured; `ratchet_tokens.qa-code-critic` unchanged or lowered)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\skills\qa-story\phases\s5.md` (:163, :170, :200)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_code_critic_probe_rule.py` (KEYS rewritten)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_charters_s5_s9.py` (`M1_TOKENS["qa-code-critic"]`: "the probe's `data_row` case" → "`--judge`"; :281 kept)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-1968-n3.md` (new)

**Exact text.**
- :45 (craft): "A probe that did not conclude is a tooling matter" → "A probe that did not run is a tooling matter" (−5 B).
- :48 (craft) REPLACED (keeps the pinned craft keys "read the probe-run log", "`expect(received).not.toBe`"):
  > - **A probe that failed at the mutated line.** Before you call it anything, read the probe-run log: the library's inverted form (`expect(received).not.toBe`, `Expected: not <v>`) shows the broken check fired; a timeout, a network error or a throw inside the check's own arguments shows it did not, even on that line; a text you cannot place either way is not yours to guess.
- New craft bullet after :48 (F5 = A; form tokens stay out of Techniques, X9 M-1):
  > - **Break the Then's own check.** A probe of a setup line proves only the setup; aim it at the check the Then names, though an element that vanishes by itself may pass when inverted.
- :70 (process) REPLACED (R10: `--dispatch`; the flags of `JUDGE_DOOR`):
  > - A probe record `cause: judgment` failed at its mutated line on a text code cannot read; your verdict is the proof: `probe_by_code.py --task <TICKET> --dispatch <your dispatch id> --judge <instance> --verdict fires|other_failure|cannot_judge --quote "<a line of its failure text>"`, `--why` for `cannot_judge`.
- New Tools bullet after :70 (R13):
  > - `target.is_assertion_id: false`: the probe broke another line; `--at <n>` or a reason in `critic-findings.md`.
- Form :51-52 → `# Every probe this review ran, by code. One that failed at its line on a text code cannot read` / `# is yours to judge (`--judge`); one that did not run is a `tooling` finding.`
- Form :58 comment → `   # incomplete: the tool could not read the run (`cause: tooling`) or it owes your judgment (`cause: judgment`)`.
- Form :60 `note` placeholder: UNCHANGED (it is echoed in the `handoff-keys.md` slice; no slice change). No `judgment:` row (R2).
- Form :67-72 (CUT 1, see Ratchets) removed; :66 header stays.
- Form :84-86 (CUT 2) → `# A `tooling` or `environment` finding is not the author's and not a round: it goes to` / `# `unverified` below, with `would_settle_it`, and to the factory backlog.`
- `execution-lifecycle.md:60-61`: "(frame, message, a launcher that may not rebuild): no verdict." → "(frame, a launcher that may not rebuild): no verdict; a failure at the mutated line it cannot read is yours to judge (`--judge`)." (G3), then regenerate the slice.
- `vocabulary.yaml:135` → `incomplete: the probe ran but the tool could not read the run well enough to judge the test (an error row, an unresolved frame, a launcher that may not rebuild): a tooling finding, never a verdict on the test; or it failed at the mutated line with a text the tool cannot read (`cause: judgment`), and the code critic judges it (`probe_by_code.py --judge`)`.
- `s5.md:163`: the `cause: data_row` sentence → "`cause: judgment` (the run failed at the mutated line on a text the tool cannot read) is the code critic's to judge (`probe_by_code.py --judge`), not a question and not `tooling`; after its `cannot_judge` the person is asked that one question (N5), never covered by a probe-gap word." `:170` "(other than `cause: data_row`)" → "(other than `cause: judgment`)". `:200` "it mutates the first assert of that test" → "it mutates the first assert of that test (or the line `--at` names); the record's `target` says whether that is the obligation's assertion".

**Ratchets (R1; AR-20) — measured before, byte deltas by hand count, after = to be measured by the builder FIRST.**
Before (t-1970, measured): tokens 18685 (total_bytes 74739), craft 1410, process 17275; rows 18685 / 17275 (slack 0). Constraint (G1): total bytes
after ≤ 74740 (tokens ≤ 18685); then process = tokens − craft ≤ 17275 automatically when craft does not shrink; the process row is set to the
measured value (a lowering, shrink-only allowed).
| change | layer | Δ bytes (LF; CRLF adds 1 per removed/added line) |
|---|---|---|
| :45 "conclude" → "run" | craft | −5 |
| :48 old 311 → new 374 | craft | +63 |
| F5 bullet | craft | +183 |
| :70 old 281 → new 309 | process | +28 |
| Tools bullet `target.is_assertion_id` | process | +113 |
| form :51-52 old 128 → new 173 | process | +45 |
| form :58 comment old 126 → new 112 | process | −14 |
| **CUT 1** form :67-72 (the "riddle" paragraph, 458 B) | process | −458 |
| **CUT 2** form :84-86 old 251 → new 161 | process | −90 |
| slice `execution-lifecycle.md` :24-25 | process | +67 |
| **net** | | **−68 B** (craft +241, process −309) |
Expected after (estimate, builder measures): total_bytes ≈ 74671 → tokens ≈ 18668; craft ≈ 1470-1471; process ≈ 17197-17198. Rows: process
17275 → the measured value (lowered); total 18685 stays (17 under, within slack) or is lowered to the measured. **No raise.**
Cut list (each: repeated process text; the grep that shows it is not pinned):
- CUT 1, form :67-72 "A refusal that does not say what the reviewer expects is not a refusal, it is a riddle … `check` is how to check it
  without asking the reviewer again." Repeats the field placeholders `expected:` / `check:` of the same form (:78, :80) and the forms' common rule
  (`handoffs/README.md:83`, `index.yaml:16`). Grep `riddle|every guess is a round|EXPECTED state|without asking the reviewer again` over
  `D:/ws1/wt-fbfix`: in `scripts/tests` only `test_handoff.py:1710` (a check MESSAGE about `remarks[].expected` of the plan form, not a pin
  of this text) and fixture copies of old forms (data); positive control in the same call: the form's own lines :68-72 matched.
- CUT 2, form :84-86: repeats charter :66 ("`environment`, `tooling`, `reviewer_error` nobody's round") and form :93-94. Grep `blames the work|author's
  to fix`: only the form, fixture copies, `story_budget.py:382` (unrelated text); no test pin; positive control: form :84, :86 matched.
- Not cut (pinned, found by grep): charter :69 (`test_red_window.py:598`, M1 `contradicts_requirement` in Tools), :71 (`test_s7_control_experiment_texts.py:90,93`),
  :62 (`test_case_alternatives.py:126-141`), :63 (`test_s5_precheck.py:3164`), :68 "could not verify" (`test_charters_s5_s9.py:55`). The craft halves
  of X9 pairs (:45 "its red is the proof") are experience by design (t-1908 Q1), not repeated process; not cut.
- Fallback if the measurement exceeds 74740 B: CUT 3, form :24-26 `inputs_read` comment (≈ 190 B, repeats the `version:` placeholder; grep
  `a review of a file that has since changed` → forms and fixtures only). Only if CUT 3 also does not cover it: a named raise of
  `ratchet_tokens.qa-code-critic` by the measured excess, reason "the critic's experience of a failed mutation and of the Then's own check
  (owner's word 05.11.2026)", for the Lead's verdict — never of the process row.
Generated slice line: R2 drops the form row, so `handoff-keys.md` gains no line (G2: placeholders only; the `note` placeholder unchanged).

**Census (AR-20).** The one new unit is `probe_by_code.py::judge_record` (N2): u1 by name (`^judge`). It BLOCKS only if a
`refusal_registry.sites()` site sits in it or `probe_by_code.py` is on the blocking path (G12). If it blocks, `blocking_per_role.qa-code-critic`
counts it: 130 → 131 — a named raise (reason: "the critic's `--judge` refuses a judgment of other bytes, a closed record or an absent quote:
data checks, owner judgment"), written only when the census test prints 131. N1's `judge_detector` row changes class only (count unchanged).
`_judge_cli`, `judgment_facts`, `marker_token`, `_with_marker`, `receipt_off_target`, `probe_owes_judgment`, `probe_not_proved_words`,
`probe_judgment_cases`, `probe_judgment_lead` do not match `UNIT_NAME_RE`; they become units only with a refusal site (none required).

**Edges.** E3.1 Temporal: a critic dispatched before N2 lands carries the old :70; its `unverified` on a `cause: judgment` record leaves the
window's probe-missing line (no gap is named for it) and the resume brings the new charter. INV: no instance is closed by the old road.
E3.2 The charter names no field the code does not produce (`target`, `--at`, `--judge` exist after N2/N4; merged before N3). E3.3 The builder
measures FIRST (`role_load.py`), then writes the row. E3.4 CRLF: if the form or charter is CRLF, each removed line also removes 1 B (helps).

**Non-goals**: other charter sections; `qa-automator.md`; brief writer; `handoff-keys.md` by hand.

**DoD**: pins in `test_code_critic_probe_rule.py`: `test_charter_names_judge_command` (every flag of `probe_by_code.JUDGE_DOOR` in the Tools bullet;
negative control: one flag removed → red), `test_charter_has_no_data_row_road`, `test_craft_keys_kept` ("read the probe-run log",
"`expect(received).not.toBe`" in Techniques), `test_form_comment_names_judgment`, `test_vocabulary_incomplete_names_judgment`,
`test_lifecycle_slice_names_judge`; `test_charters_s5_s9.py` M1 tokens. Witness (fast): `python -m pytest ai-packages/qa-factory/scripts/tests/test_code_critic_probe_rule.py ai-packages/qa-factory/scripts/tests/test_charters_s5_s9.py ai-packages/qa-factory/scripts/tests/test_contract_slices.py -q`;
`python -B ai-packages/qa-factory/scripts/role_load.py --role qa-code-critic --json` (verbatim; tokens ≤ 18685, process == the new row);
`python -B ai-packages/qa-factory/scripts/contract_slices.py --check`; `python -B ai-packages/qa-factory/scripts/selftest.py --lang`.
`architecture: AR-10, AR-20, AR-29`.

### N4 — the probe says which check it broke, and a probe of another line never proves the obligation

∥ N1 (disjoint functions). F2 = B + R13.

**Owns** (absolute; functions):
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\probe_by_code.py` (`_probe` — after `_plan`, before `_new_record`; `_new_record` — `target`; `WINDOW_PROBE_FIELDS` — + `target`; `write_receipt` — receipt core + `target`; `keep_standing_record`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\proof_level.py` (`receipt_off_target` [new]; `reached` — one issue)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\acceptance.py` (`validate_window` — the `semantic_sensitivity` condition only)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\window_record.py` (`_explain_parts`/`GAP_ORIGIN` — the door text of `semantic_sensitivity` for an off-target probe only)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_target_fact.py` (new, fast)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-1968-n4.md` (new)

**Required behaviour.**
1. Record and receipt core gain `target: {"line": detail["line"], "end_line": detail["end_line"], "assertion_id": <manifest copy or null>,
   "is_assertion_id": …}`: `true` when `assertion_id` = `<file>:<n>` names the probed file (`_same_file`) and `line <= n <= end_line`;
   `false` when it names another line or file; `null` when absent or not `<path>:<digits>`. When `false`, one note naming `--at <n>`.
   Python path the same (`--at` on the Python path: the builder confirms `plan_mutation` honours it; if not, the note names only the critic's reason road).
2. `proof_level.receipt_off_target(receipt_or_block) -> str`: the why (`"the probe broke line L, not the obligation's check at <id>"`) when
   `target.is_assertion_id is False`, else `""`. THE reader (AR-13): `acceptance.validate_window` appends `semantic_sensitivity:<iid>` when it is
   non-empty; `proof_level.reached` reports it as an issue (so a binding publication never counts it at delivery: FR-18 by data).
3. Door of that gap (window_record): "probe the Then's line: `probe_by_code.py … --at <n>`; or, when no check of the Then can be inverted here,
   return the item `unverified` with its reason — the person decides «accept as not proved» (N5's word)". INV: never a dead end (FR-57).
4. `keep_standing_record`: a stored `intended_failure` that `receipt_off_target` names does NOT stand over a new record (so an `--at` re-probe that
   ends `cause: judgment` is stored and judgeable).

**Edges.** E4.1 `null` → counts as today (no issue), the window prints a note "the probe's target could not be compared with the obligation's
assertion (no `assertion_id` of the form `<file>:<line>`)". INV: an unknown is never written as `false`; the residual (an unknown target still
proves) exists today and is named, not widened — manifests carry `<file>:<line>` (F32). E4.2 Positional: computed from the PLAN. INV: the fact
describes what was mutated, never what failed. E4.3 Several Thens, one `assertion_id`: compared with that one line (named residual). E4.4 A
multi-line statement containing the line → `true`. E4.5 Temporal: inside one run a receipt without `target` (written before N4) → treated as `null`.

**Non-goals**: choosing the target by code (no default `--at`); the doors functions.

**DoD**: `test_target_true_when_mutated_line_is_assertion_id`, `test_target_false_names_at_door`, `test_target_null_when_absent`,
`test_target_python_path`, `test_off_target_receipt_is_semantic_gap`, `test_off_target_receipt_not_reached_at_delivery`,
`test_off_target_gap_names_both_doors`, `test_off_target_record_does_not_stand_over_reprobe`, `test_target_in_window_probe_block`.
Witness (fast): `python -m pytest ai-packages/qa-factory/scripts/tests/test_probe_target_fact.py -q`. CI only: `test_window_record.py`, `test_check_delivery.py`, `test_probe_by_code.py`.
`architecture: AR-13, AR-21, AR-23, AR-28, AR-29`.

### N5 — `cannot_judge`: the person's own question, with the facts (owner's word 05.11.2026, F4 = A)

After N2 (reads `judgment`) on a tree with the doors batch (wt-fbfix has it).

**Owns** (absolute; functions — D-0048 against the doors batch's functions):
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\contract.py` (`PROBE_NOT_PROVED_PREFIX` [new], `probe_not_proved_words` [new])
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\block-names.json` (one row [new])
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\window_record.py` (`probe_judgment_cases` [new]; `probe_gap_block` — the cannot-judge branch; `build` — the cannot-judge note at :1102; NOT `probe_gap_cases`, `PROBE_GAP_RECORD`, `PROBE_GAP_DOOR`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\acceptance.py` (`probe_gap_named` — the twin branch)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\story_run.py` (`Person.__init__`, `_person_of`, `ask`, `held_question` — the `probe_judgment_cases` transport beside `probe_gap_cases`; `window_round_gate` — the S5 branch :6018-6027; `seam_chosen` — one branch; `probe_judgment_lead` [new]; NOT `probe_gap_lead`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\conductor-actions.json` (one `actions` row [new]; the doors probe-gap row: one clause)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_not_proved.py` (new, fast)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-1968-n5.md` (new)

**Required behaviour.**
1. Word: `probe not proved: <case key>` — row `{"block": "probe not proved: <case key>", "reader": "contract:probe_not_proved_words", "stages":
   ["S5"]}`, NO `class` (one word never widens). `probe_not_proved_words(pipeline)` = `probe_gap_words`' reading with the new prefix.
2. `probe_gap_block` and `probe_gap_named` (twins): for an item whose current-bytes record `probe_owes_judgment == "cannot_judge"`, ONLY the new
   word names it, by its case key, and only when the word's `at` ≥ the judgment's `at` (`named_by: "probe not proved: <case>"`); the `probe gap:`
   words (instance, case, `tooling:`, class) are NOT read for it. Every other item: unchanged.
3. `build` note for a `cannot_judge` item: "the code critic could not tell whether its probe failed because of the broken check; the person
   decides: `waiver.py --task <T> --stage S5 --block "probe not proved: <case key>"` (return this item: a role records no word)".
4. `probe_judgment_cases(window, root) -> list[(case, [ {iid, file, line, statement_after, printed, why} ])]`: owed green items whose record says
   `cannot_judge`, grouped by case; `printed` = the first 3 non-empty lines of `failure_text`, each ≤ 160 chars, folded. A case is listed when
   every owed green item of it is `cannot_judge` (as `probe_gap_cases`). Never raises.
5. Seam: in `window_round_gate` S5 branch, `probe_judgment_cases` is read FIRST; non-empty → state `probe_judgment_cases`, lead
   `probe_judgment_lead(pairs)`; the doors' `probe_gap_cases` branch runs only when it is empty (one question per seam; the other comes at the next
   refusal). Transport identical to `probe_gap_cases`. `seam_chosen`: `go_on_as_is` with `probe_judgment_cases` → `pass_block("S5", "probe not
   proved: <case>", …)` per case, print `S5: <cases> stay not proved on your word`; `rework_stage` → unchanged (the conductor gets the words and
   runs `rework`, sending the test back to its author).
6. `probe_judgment_lead` (human-questions form; no field, script, path or dispatch id):
   > The review of this window of tests is finished, but for {n} test case(s) the factory could not prove that a test would catch a broken
   > product. It broke one check in each test and ran it; the test failed, and the code reviewer could not tell whether it failed because of
   > that check or for another reason: {list}. Only you can decide what happens to these tests.
   >
   > Answer `go on` to accept them as not proved: your words are recorded for these cases only, and the report lists them as not proved. Answer
   > `rework` to send them back to their author with your words. An earlier answer about tests the factory's tool could not read does not cover these.
   `{list}` per test: `<case key>: the test "<instance id>", the check broken at line <line> (`<statement_after ≤ 120>`), it printed "<printed>"; the
   reviewer said: <why ≤ 160>`; > 10 → first 10 and `, and {k} more`.
7. `conductor-actions.json`: `actions` row `{"says": "the person accepts that tests whose probe the code reviewer could not judge stay not proved",
   "run": "waiver.py --task <T> --stage S5 --block \"probe not proved: <case key>\" --words-file <file>, once per case key the question names;
   a `probe gap:` word never covers such a test"}`; the doors probe-gap row gains "; never a test the code reviewer could not judge".

**Edges.** E5.1 A `go on` given for tooling probes (case word or class word) before or after → never names a `cannot_judge` item. INV: the owner's
word — never covered silently. E5.2 A `probe not proved` word older than the judgment (same case, earlier bytes) → not read; asked again. INV: a
word answers the facts it was shown. E5.3 Empty (no `cannot_judge` item) → no state key; seam as today. E5.4 Both kinds owed in one window → this
question first, the probe-gap question at the next refusal. INV: one question per seam (AR-16), no word recorded for a token not chosen. E5.5
`pass_block` refused → held question; recorded cases stay. E5.6 Red item, unjudged record, never-run probe → not listed. INV: a red test is never
closed by a word; a person never judges a probe's text before the critic did. E5.7 Temporal: an `asked` record without `probe_judgment_cases` →
today's path. E5.8 Report: the accepted item is `review_unverified_factory` (N2 item 7), so it is listed as not proved.

**Non-goals**: `probe_gap_lead` text and `probe_gap_cases` (doors, owner-confirmed); `question_from_refusal`; `waiver.py` logic (the row is data).

**DoD** — `test_probe_not_proved.py` (fast; `Driver` stubbed as in `test_probe_gap_door.py`): `test_not_proved_word_is_a_block_row`,
`test_go_on_for_tooling_never_covers_cannot_judge`, `test_word_older_than_judgment_not_read`, `test_cases_list_cannot_judge_only`,
`test_lead_shows_test_check_and_printed_text`, `test_lead_obeys_human_text_rules` (`human_text.problems`), `test_seam_go_on_records_not_proved_per_case`,
`test_seam_rework_goes_to_conductor_with_words`, `test_judgment_question_before_probe_gap_question`, `test_twins_name_the_same_items`.
Witness (fast): `python -m pytest ai-packages/qa-factory/scripts/tests/test_probe_not_proved.py ai-packages/qa-factory/scripts/tests/test_probe_gap_door.py ai-packages/qa-factory/scripts/tests/test_judgment_census.py -q`; `python -B ai-packages/qa-factory/scripts/selftest.py --lang`.
CI only: `test_probe_gap_word.py`, `test_story_run_*`, `test_conductor_doors.py`, `test_window_record.py`.
`architecture: AR-1, AR-16, AR-19, AR-24, AR-25, AR-29`.

---

## §4 Parallelism and the doors batch (merged in wt-fbfix)

- `probe_by_code.py`: N1 {`marker_token`, `_with_marker`, `plan_detector_mutation`, `_plan`, `judge_detector` marker step, `_judge_detector_rows`
  `proved_by` copy} ∥ N4 {`_probe`, `_new_record`, `WINDOW_PROBE_FIELDS`, `write_receipt`, `keep_standing_record`}; N2 after N1 {`JUDGE_DOOR`,
  `judge_detector` E15, `_judge_detector_rows` cause, `judgment_facts`, `judge_record`, `_judge_cli`, `_build_parser`, `main`}.
- `window_record.py`: doors N1 owned `PROBE_GAP_RECORD`, `PROBE_GAP_DOOR`, `probe_gap_cases` — untouched here. N2 {`probe_gap_block` factory branch,
  `build` note}; N4 {`_explain_parts`/`GAP_ORIGIN` door}; N5 {`probe_judgment_cases`, `probe_gap_block` cannot-judge branch, `build` note} — N5 after N2.
- `acceptance.py`: N2 {`probe_gap_named` factory branch} → N5 {`probe_gap_named` new branch}; N4 {`validate_window`}.
- `story_run.py` (hot): N2 {`s6_reprove`}; N5 {`Person.__init__`, `_person_of`, `ask`, `held_question`, `window_round_gate` S5 branch, `seam_chosen`,
  `probe_judgment_lead`} — the doors functions are edited beside their doors lines, after the doors integration (done in wt-fbfix).
- `conductor-actions.json`: N5 only. `contract.py`: N5 only. `proof_level.py`: N2 {record state, could-not-run, owes-judgment} ∥ N4 {`receipt_off_target`, `reached`}.
- `judgment-census.json`: N1 (one class), N2 (one row) — sequential.

## §5 Questions for the owner

No open owner questions (F4 decided by the owner 05.11.2026 ≈20:25: option A, node N5).

## §5b Small choices closed by the designer

Marker word `qa-probe-` + 12 hex; token inputs; `failure_text` cap 16384; quote/why caps 300; new test files; `proved_by` a record field; no new
verdict word; `printed` = first 3 lines ≤ 160 chars; the cannot-judge question asked before the probe-gap question in one window; `null` target
counts as today with a note (E4.1, the Lead may override at acceptance); CUT 3 as the fallback before any raise.

## §6 Live proof (FR-33) — MyBooks LOCAL-1, `D:/ws1/mybooks-stand\tr-arm-b`

Preconditions: N1-N5 merged, CI green; the stand installed from the batch branch; an open S5 critic dispatch for TC_001/TC_002.
1. Re-probe TC_001 in-stock and TC_002 out-of-stock: records `intended_failure`, `proved_by: marker`, `message_form: M-TS1`, marker found as
   `Error: qa-probe-<hex> step 1: …` / `… Then 4: …`; `restore.verified`; live receipt with `proved_by: marker` and `target`; `target.is_assertion_id`
   `false` for TC_001 in-stock (:43, a step line) → window gap `semantic_sensitivity` naming `--at`; the critic re-probes with `--at <Then line>`.
2. The S5 window of TC_001/TC_002 closes with `approved` and NO person's word.
3. The critic path: one probe without a marker whose text the factory cannot read (a stand test without author message, if one exists); otherwise
   N2/N5 unit tests + an offline replay of a stored junit, said honestly in the batch's "Живые доказательства".

## Could not establish
- `role_load.py` after the change: not run (this designer has no shell); the byte deltas are hand counts (LF assumed; CRLF only helps).
- Whether `judge_record`'s refusals are `refusal_registry` sites and whether `probe_by_code.py` is a blocking-path file (decides 130 → 131).
- Whether the Python `plan_mutation` honours `--at`; NUNit 4 `That` message form; Playwright matcher-internal errors' message header (E1.13).

## Reading trail
This revision read in `D:/ws1/wt-fbfix\ai-packages\qa-factory`: `agents/qa-code-critic.md` (whole); `handoffs/s5-critic-to-automator.yaml`
(whole); `handoffs/vocabulary.yaml:126-137`; `references/role-load.json` (whole); `inject-map.json` (Grep); `references/slices/qa-code-critic/
handoff-keys.md`, `execution-lifecycle.md` (whole); `references/execution-lifecycle.md:35-69`; `block-names.json` (whole); `gate-registry.json:572`
(Grep); `scripts/role_load.py` (def index); `scripts/tests/test_judgment_census.py:1-110,189-418`; `judgment-census.json` (Grep);
`test_code_critic_probe_rule.py` (whole); `test_charters_s5_s9.py:50-89,244-283`; `test_case_alternatives.py:110-154`; `test_red_window.py:585-604`;
`test_s5_precheck.py:855-874,3160-3187`; Grep pins in `test_blocked_by_env_texts.py`, `test_case_role_twins.py`, `test_mixed_then_texts.py`,
`test_s7_control_experiment_texts.py`; `window_record.py:95-106,540-690,1060-1180,1266-1390,1590-1720`; `acceptance.py:40-59,874-918,1056-1089`;
`contract.py` (Grep `prefix_value`, `PROBE_GAP_*`, `probe_gap_words`, `probe_gap_class_word`); `check_delivery.py:976-1005,1866-1927` + Grep;
`story_run.py:5925-6044,11600-11768,16050-16094` + Grep; `skills/qa-story/phases/s5.md:158-173` + Grep :200. Greps for cut pins over
`D:/ws1/wt-fbfix` (with positive controls named in §3 N3). Not run: `role_load.py` (no shell tool in this dispatch). Docs: the verdict
t-1970 (whole), the finding (whole), t-1955 N1 (lines 163-260), the first draft (whole), `t-1908-critic-x9.md:50-74`.

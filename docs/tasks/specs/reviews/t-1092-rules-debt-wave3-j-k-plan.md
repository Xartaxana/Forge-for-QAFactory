# t-1092 — plan critic: rules-debt wave 3, cards C3-j and C3-k1..k4 (F19)

Under review: `docs/tasks/specs/20261117-rules-debt-wave3-j-k-cards.md` (§1-§11 and "Lead decisions on the forks"), against its
parent `20261117-rules-debt-phase2-cards-spec.md` (C3-j/C3-k sketches :1287-1380, F-C1/F-C2 :1691-1700) and card C3-g
(`20261117-rules-debt-wave3-g-h-cards.md` §2, G-0). Code read on main `c0022c96` (= origin/main) and on the C3-b2/C3-d/
C3-reg-precondition branch `origin/worktree-agent-ac40b44fb0a175afa` (extracted with `git archive` to the scratchpad).
I had a shell, so the measurements the designer could not make are below (M1-M7). Read-only on the code; this file is
the only write.

## Verdict per card

| card | verdict |
|---|---|
| C3-j | **not dispatchable**: the measured premise is the wrong way round (M5), two questions are the owner's (J1, J2), and the card's own stop fires for certain (J4). gate_brief/driver reads of a profile-level gap are left out of owns (J3) |
| C3-k1 | **dispatchable with fixes** K1-1, K1-2 |
| C3-k2 | **dispatchable with fixes** K2-1 (blocking: a test file breaks), K2-2, K2-3, K2-4, K-C1 |
| C3-k3 | **dispatchable with fixes** K3-1 (the collision amendment), K3-2, K3-3, K-C1 |
| C3-k4 | **dispatchable with fixes** K4-1, K4-2, K4-3, K-C1 |

The k1..k4 split and order hold. Every card merges green on its own, as long as the allow-list pin K-C1 moves with it.
The F-k1/F-k3 decisions keep every decision the same on every word the producers write (traced per consumer in §B).
The recorded-data control can fail, but only on `person_confirmed` (M3). It needs widening.

## Measurements (with a shell)

- **M1 `--check` / `--sites` on main.** `python -B .../scripts/gate_registry.py --check`: "A26 gate registry: no violations",
  6 debt, exit 0. `--sites`: 145 lines, 0 UNREGISTERED. On the C3-b2 branch: 4 debt, 150 items (`D13_ITEM_COUNT = 150`,
  `test_gate_registry.py:1069` on the branch).
- **M2 Simulating k1 and k4 in memory** (`GR.analyse(registry=<edited copy>)`, script `sim.py` in the scratchpad). The
  copy adds k1's two words: 0 findings and +5 items, exactly `coverage_contract.py:824`, `:845` (target_kind),
  `execution_request.py:164` (`:165` on the branch), `manual_evidence.py:80` and `profile_contract.py:718`
  (`== NO_CHANGED_FILE`). That equals the plan's E-k1.4 and k1 item 4.
  Turning the row `converted` on today's code (both trees) gives F-b on all 13 accept sites, the `vocabulary` finding, and
  F-a on exactly these literals: coverage_contract :824 :832 :839 :845(x2); environment_preparation :388;
  execution_fingerprint :122 :134; execution_request :164 :166 :169 :176; gate_preflight :3444; manual_evidence :80 :86
  :90 :129 :682 :686; profile_contract :908 :917-921. **That is exactly the plan's §3 table**, with nothing missing. No
  provenance accept site is registered under a second row (no "registered more than once" finding on either tree).
- **M3 Recorded provenance records.** The 25 `evidence/runtime-provenance-*.json` are ALL `person_confirmed`, and all are
  accepted today (`acceptable_provenance(r, ACCEPTS)` True, with and without `rehearsal`). So the §3 control's
  `old==bad` False can fail, but only on the pc word. A walk of every fixture JSON for provenance-shaped dicts
  (`observed_runtime_identity` or `result`+`expected_source_revision`) finds 133 records: 79 `matched`, 53
  `person_confirmed`, 1 invalid, **0 `not_applicable`**. No recorded data exists for `no_changed_file`, `local_source`
  or a bare NA.
- **M4 F-k2.** There are 0 recorded NA records (M3). `manual_capture.stand_probe` refuses a bare NA today
  (`acceptable_provenance(value, ACCEPTS, task=story)`, `manual_capture.py:1612`). So tightening the registry token to
  `not_applicable:no_changed_file` changes no decision and no recorded story. It makes the registry say what the code
  does. F-k2 (a)/(a) holds.
- **M5 C3-j premise.** The plan's grep looked for the PRESENCE of `page_object_max_wait_s|e2e_page_load_s` (0 hits) and
  concluded "the change moves no recorded story". But the card fires on their ABSENCE. I decoded
  `state/config-at-start.json` of the three recorded stories with a config (cart-1, local-1-0108, local-1-arm-b): each
  has profile `web` with no `page_object_max_wait_s`, and environment `local` with no `measured`.
  `s5_automate_rows` + `s5_profiles` give these e2e-ui rows on `web`: cart-1 1/10, local-1-0108 13/21,
  local-1-arm-b 10/17. So `_e2e_limit` returns `unmeasured` (both absent, `gate_preflight.py:3123-3125`) on **3/3**
  recorded stories. Today that is a note. After C3-j it is a PERSON_DECIDES card at gate A on every one of them. Because
  the wait is absent, there is no key (E2), so `accept always` is never offered and the card comes back on every story.
- **M6 Simulating C3-j's registry row** (row re-roled per item 6, `simj.py`). 0 findings on both trees; +5 items in two
  new triples: `check_s5_stand_limits` :3192 :3196 :3207 :3217 and `check_s5_reporter` :3323. That matches item 8's
  "about five" before the code edit. The code edit will move it, and the measurement decides.
- **M7 Readers of the changed names** (grep `acceptable_provenance|\bACCEPTS\b` over `scripts/`). Beyond the plan's §10
  and F-k3 lists, there is `tests/test_launch_wrappers.py:163, :167`. It does
  `mock.patch.object(RS, "acceptable_provenance", ...)` / `(ER, "acceptable_provenance", ...)` around
  `RS.probe_runtime` / `ER.rehearsal_probe` (finding K2-1). The other extra hits are prose: `brief_pack.py:3668`,
  `runtime_probe.py:57`, `gate_registry.py:42,:360`, `test_brief_pack_roles.py:405`, `test_no_move_seam_k4s.py:252`.

## A. C3-j — findings

**J1 (blocking; owner question, rule 11a) — what the answers DO.** On a stand-gap card, the data's `accept` says "it stays
blocked and is reported as not run", and `accept always` says "the same as `accept` for this story, and the record keeps
it" (`question-vocabulary.json` `stand_gap_words`). A covered gap is carried into the story as accepted:
`driver_machine.carry_environment_properties` (:3074-3119) puts its cases into `stand_accept_cases`. So on the planned
road, `accept always` on the unmeasured-limit card means "the e2e rows of this profile are never run on this stand, in
any story". The card's question reads "whether the e2e rows fit this stand is unknown". That invites the opposite answer
("accept the risk, run them"), and the existing word set has no option for that. Items 3 and 7 never say what happens to
the cases. `unmeasured-covered` pins only "no finding, a note, the row in covered_gaps", not that the cases are blocked.
This breaks FR-9 (each option has an executor, the decision kept whole), FR-10 and AR-24. The owner must say which
meaning she gave in F-O1:
- (i) accept = the e2e rows are reported not run here (the existing road, no new word);
- (ii) a new "run them here anyway" option. That is a data row and a record option (`environment_record.record` takes
  only `accept`, :333-334), so the card's owns grow.

The card is then rewritten to that answer, and a test pins the cases' fate.

**J2 (blocking; owner/Lead fork) — "answer persisted" fails on the measured default.** M5: on 3/3 recorded projects the
wait is absent. Then E2 gives no key, so no `accept always`, so the card is asked on every story, forever, until
onboarding records a wait. That contradicts F-O1's "the answer persisted". The scale of the change is not named either:
every project without measurements gets a new gate-A stop per story. Fork for the Lead, and the owner for the scale:
- (a) key the absent wait as an explicit token (`wait_s: "unrecorded"`), so `accept always` persists, and a wait recorded
  later is a `wait` near-miss that is asked again (FR-7 safe direction);
- (b) keep E2 as decided and tell the owner the measured cost.

The plan's E2 also differs from the parent's E2. Parent: "the card offers (b)/(c) only". Plan: "offers `accept` (this
story), (b) and (c)". Settle it with J1.

**J3 (blocking for dispatch) — profile-level gap readers outside owns.** Item 5 walks only `stand_gaps.py`, and the
non-goals call `gate_brief.py` and `driver_machine.py` "generic". They are not. A gap with `scope: "stand_limit"`,
`case: ""` and no `case_id` falls into the CASE branch of each of these:
- `gate_brief._gap_heading` :1565 → "SL-web — a test the stand cannot run yet — one case". That is a wrong sentence (it
  costs several cases), and it contradicts the finding text (FR-10).
- `gate_brief._lasting_lines` :1612-1614 → `LASTING_CASE` "until the stand's address changes". That is false: a wait
  change also reopens it.
- `gate_brief.stand_gap_form_ids` :959 → the person writes `SL-web`, not the profile.
- `gate_brief._card_context` :1639 → the cases are not linked.
- `gate_brief._ids_of` :1303, `:1742` (applied accept), `:1794`.
- `gate_preflight.gap_name` :1612 → `GAP_SLOT` renders "SL-web".
- `driver_machine._level_remedies` :3129 → no remedy is carried.
- `environment_record.live_level` :289 and the lost-contour note in `_environment_cover` :4235-4239.
- `stand_gaps.gate_b_split` :1007-1009, which hard-codes the key `f"RP-{contour}"`.

Fix: owns gains `gate_brief.py` (`_gap_heading`, `_lasting_lines`, a third lasting text, `stand_gap_form_ids`, `_ids_of`,
`_card_context`) and `gate_preflight.gap_name`. `PROFILE_SCOPES` lives in `stand_gaps.py` beside `ROLE_SCOPES` (:200),
and every read above uses it. `driver_machine._level_remedies` is applied if J1 = (i). Each listed hit gets its report
line (applied / n/a — why). This is the sweep-the-artifact enumeration the card left to one file.

**J4 (blocking for dispatch) — the card's own stop fires.** Item 1 reads the wait "by the same reader `_e2e_limit` uses
(`limit_seconds`)", and "if that reader lives in gate_preflight.py … the node stops". It does live there
(`gate_preflight.py:157-164`; §11 lists it as "not read"). Decide it now: move `limit_seconds` (pure, 7 lines) into
`environment_record.py`, and have `gate_preflight` import it from there. That keeps one survivor (AR-15) and creates no
cycle: environment_record imports only the stdlib at the top. The existing pin `gate_preflight.py:6394` keeps passing
through the import. Add `environment_record.limit_seconds` to item 1, and the import line to gate_preflight's owns.

**J5 — F-j4 (b) is not carried into the card.** The card was drafted under F-j2 (a). Lines that must change:
- §2 :70 "Decided: … F-j2 (E9)" → F-j4 (b).
- Item 3, finding message: `f"e2e stand limit: {profile_id} — {GAP_SLOT} — "` → `f"e2e stand limit not measured: {profile_id} — …"`.
- Item 3 :170, "The message opens with the block `e2e stand limit: <profile>`, so a waiver recorded earlier still passes
  (E9)" → it opens with `e2e stand limit not measured: <profile>`, and a waiver for `e2e stand limit: <profile>` (written
  for an `over` card) does not pass it. Checked: `add()` matches through `waiver.split_overridden` on whole words
  (`gate_preflight.py:1590-1600`), and `e2e stand limit: web` is not a whole-word run inside `e2e stand limit not
  measured: web`. No door offers a waiver on the new block, so only `*`, the stand-gap line and the handed door pass the
  card.
- Item 7 `old-waiver` (E9): flips to "an old `e2e stand limit: web` waiver → the card IS shown, its message starts
  `e2e stand limit not measured: web`". Add the pair row "the same waiver still passes the `over` card" (beside
  `over-unchanged`).
- Item 7 `unmeasured-card`: the expected prefix becomes `e2e stand limit not measured: web`.
- E9 is rewritten as TEMPORAL. Waivers written before C3-j exist only for `over` cards, because no unmeasured card
  existed (:3192). They keep passing `over` and never pass the unmeasured card. INVARIANT: a word given for one fact
  never passes another (FR-7, FR-4).
- E13: the pair is now "stand-gap answer `stand gap: SL-<p>: <word>`" vs "handed waiver `executor unavailable: <p>`"
  (`_handed()` skips the profile, :3183). The old waiver leaves the pair.
- §8 F-j4 is marked decided (b).

**J6 — item 3 leaves "find an approach".** "The builder reads how `gap_name` and `stand_gaps.collect` treat a row whose
finding was dropped … and if … the row is not left". The precedent is decided code: `check_s5_reporter` appends the row
and then calls `add` (:4152-4153), and an answered row stays and renders as answered (gate_brief `_short_line`). Write:
"append the row, then add, as the reporter does; a dropped finding leaves the row, which renders as answered". Add a test
row: answered `SL-web: run` → no finding, and the row present and answered.

**J7 — a near-miss word without its registry row.** Item 4 adds `"wait"` to `_environment_cover`'s near-miss table. That
function is a site of row `environment_property_cover`, whose `words` are `["command","reason","address"]` with
`vocabulary: code` (gate-registry, row printed in the trail). Its words would no longer be the code's words (S-c). Owns
gains that row: `words` + `wait`, `verdict_map.wait = {"class": "mismatched"}`. Also name the precedence when both
`wait_s` and `definition_sha` differ (item 1 `near_miss` is silent). Recommended: `address`, the stand first, as in the
CASE branch.

**J8 — item 6 contradicts itself.** "`policy_file`, `scope_keys`, `binding_keys`, `question_kind` are copied in shape
from `environment_property_cover`". That row holds `null`, `[]`, `[]`, `null`, yet the item lists non-empty keys. Pick
one. Both pass `_check_row` (:636-641).

**J9 — tests (docs/TESTING.md, rule 11).**
- Name the existing rows that flip instead of "if a table pins": `test_k5_nothing_recorded_is_not_measured_and_never_a_card`
  (`test_gate_preflight.py:2801-2830`, its four sub-rows) and `test_a_measurement_older_than_the_stand_is_not_a_measurement`
  (:2860-2870).
- Add `_limit_gap_row` to `NEW_CHECK_FUNCTIONS` (:3651) and to the static FR-6 scan list (:3806-3809): its `what` and
  remedy texts reach the person. The remedy's `where_words` may carry field paths only where FR-6 allows them (the fix,
  as :2840-2843 pins).
- The CLI `record --limit` is outside input, so it gets its mini-battery as rows: `--limit ""`, `--limit nosuch` (no
  profile), `--limit web` with the wait absent / `"30"` / `0` (each refused naming the part, nothing written), a
  non-ASCII profile id and a 200-character one (`about` cut at 160, `record` :346). Today only key-level rows are listed.

**J10 — size.** After J1-J9 the card touches environment_record, gate_preflight (HOT), stand_gaps, gate_brief, the
registry (2 rows) and three tests. That is likely over a 250K worker. If the decisions keep it large, split it along
AR-22. j1: the key + `limit_seconds` + `current_key`/`near_miss` with `covering` round-trip rows, and no CLI form and no
gate reader. j2: the CLI writer, the card, the gate_brief/stand_gaps reads, the registry rows, together (writer and
reader in one commit).

What holds in C3-j:
- F-C1 (a): gate A, `run` :6084-6094, gate A only, checked.
- F-j3 (a): one road, and no second store (P31, F-C2 (a)).
- E4 and E5: the switch at :3176 and the reporter `== "over"` at :3323 are unchanged.
- E6: `load_rows` does not check scopes, so an older plugin covers nothing (safe).
- E7 positional.
- The registry row passes `_check_row`: the unknown owners are mixed environment/factory, so the person addressee is
  legal (:629-633).
- `stand_gaps.stand_name` and `_selected_environment` derive the same stand (`stand_gaps.py:148-159`,
  `gate_preflight.py:5139-5146`).
- AR-28: a PERSON_DECIDES card holds gate A (`can_proceed` false) until answered. An unanswered card is never a pass.

## B. C3-k — trace of decision preservation (F-k1/F-k3), per consumer

Today's predicate is `acceptable_provenance` (`profile_contract.py:893-923`). The new one is
`acceptable(provenance_word(...), c)` (`gate_template.py:60-96`; pc needs row `promotable: true`, which
provenance_acceptance has). Words the producers can write: matched, mismatched, unknown, not_applicable (± reason_code
`no_changed_file`), person_confirmed, plus off-case or invalid records.

| consumer (site) | today accepts | new tokens | equal? |
|---|---|---|---|
| automation (`validate_request`) | ACCEPTS(task) or valid NA ∧ local_source | matched, pc, NA:ncf, NA:local_source | yes: a valid NA → ncf / local_source / bare; bare refused, and `said_local` already wrote the sentence |
| rehearsal (`rehearsal_probe` default) | ACCEPTS, rehearsal | matched, pc, NA:ncf | yes (task None both) |
| identity (`_observed_identity`) | ("matched","person_confirmed"), rehearsal | matched, pc | yes |
| run (`run_suite.probe_runtime`) | ACCEPTS | matched, pc, NA:ncf | yes |
| fingerprint (`build`) | ACCEPTS or any valid NA | matched, pc, NA (bare) | yes: every NA word has class NA |
| manual (`_provenance_errors`, `validate_manual_current`) | ACCEPTS(task) or valid NA ∧ local | as automation | yes |
| manual_capture (`stand_probe`) | ACCEPTS(task) | matched, pc, NA:ncf (F-k2 a) | yes (M4) |
| baseline_identity.capture (`validate_baseline_record`) | valid ∧ effective ∈ {matched, NA} | matched, NA | yes: effective matched/NA ⇔ declared = effective; the pc sentence keyed on `checked` as today |
| environment_preparation.deploy_proof (`_run_step`) | valid ∧ effective matched | matched | yes |

The ncf+local precedence (`no_changed_file` first) is safe, because no consumer takes `local_source` without `ncf`.

## C. C3-k — findings

**K-C1 (blocking for k2, k3; class across the k cards) — the allow-list pin.** `test_gate_registry.py:299-302` on main
(`:305-308` on the C3-b2 base) asserts the EXACT list of all allow entries in the registry: "the allow entries today are
S1's data-seed shape check and two display flags of test_identity". k2 adds three (:166, :169, `build` :134). k3 adds four
(:86, :682, :839, :845). Neither card's owns of `test_gate_registry.py` names this pin, and the file is slow, so the
builder never sees it go red: only the canon does. Fix: k2 item 6 and k3 item 7 each add "the allow-list pin gains <the
entries, whole text>". The deltas are taken from the base (S-f), and C3-b2's entries are already in it.

**K2-1 (blocking) — `test_launch_wrappers.py` breaks.** `other_places_use_the_one_launcher` (:157-171) patches
`RS.acceptable_provenance` and `ER.acceptable_provenance` to True around `probe_runtime` / `rehearsal_probe`, with
`probe_record` stubbed to `{"x": 1}`. After k2:
- if k2 drops the import, `mock.patch.object` raises `AttributeError`;
- if it keeps the import, the patch no longer applies, `provenance_word({"x":1})` is `unknown`, and `ProvenanceRefused`
  is raised.

Either way the test fails. Fix: k2 owns `scripts/tests/test_launch_wrappers.py` (that function only). It patches
`acceptable` (and `provenance_word` if needed) in RS/ER. §10 must correct "`test_launch_wrappers.py:168` (positional,
unchanged)".

**K2-2 — an allow entry that can mask the acceptance it replaces.** In `validate_request`, :166 and :176 are the SAME text
`checked['result'] == 'not_applicable'`. One allow entry covers every comparison with that exact text in its site
(`gate_registry.py:81-82`, `_allowed` :772-784). So k2's allow for :166 would also whitelist :176, the acceptance
literal, if it were left. A26 cannot see it: F-b only asks that `acceptable` is called. Fix: a k2 row asserting that
`--sites --json` holds exactly ONE item `(execution_request.py, validate_request, "checked['result'] == 'not_applicable'")`.
No other site has this collision (texts checked: manual_evidence :86 vs :90, coverage :832 vs :839/:845, build :122 vs
:134 all differ).

**K2-3 — E-k2.2's gate A world is not true.** "C3-reg-precondition stops the dispatch first" covers stage dispatch
(`controller.py` dispatch branch on the branch, +5540-5554). The gate A rehearsal is not a dispatch. There,
`_observed_identity` swallows `ProvenanceRefused` into `""` (:3446-3447), so on an unreadable registry gate A shows an
unobserved stand identity, a false cause (FR-41), until the S5 dispatch is stopped. Write that world into E-k2.2 and
queue it as a finding (`rules-debt` findings/) beside the k4 F-k5 text. It is not a k2 code item.

**K2-4 — import placement.** Say per file whether `acceptable` / `provenance_word` are imported at the top or at the
point of use (C3-g's lazy-import rule, g-h §2 item 2). A26's `acceptable_in` accepts either. `execution_request` already
imports `acceptable` at the top on the branch (:24). k2 and k4 both claim `execution_request.py`'s import line; let k2
drop `ACCEPTS` there, so k4's owns of that line becomes "only if still present".

**K1-1 — a mismatched record gets two words.** Item 1 returns `mismatched` for an invalid record whose effective result is
mismatched, but "anything else → `unknown`" for a VALID declared `mismatched`. The docstring makes this function the ONE
producer of the word, so the honest word should not depend on validity. Fix: "declared `mismatched` or `unknown` whose
checked result equals it → that word". This is not an acceptance change: neither word is taken.

**K1-2 / K3-3 / K4-1 — the behaviour-preservation control is too weak, and void at k4.** M3: the 25 records are all pc,
so the §3 control proves only pc on one consumer (`provenance.run`). Fix:
- (i) k1's cross-check row becomes a matrix: for each adversarial and plain record, each consumer of §B, today's site
  predicate (the left column, as code) == the new composition. Run on the live registry after k1's words, using only
  consumers that already exist at that card. k2/k3 add rows for their new consumers.
- (ii) The recorded control walks every fixture JSON for provenance-shaped dicts (133: 79 matched, 53 pc, 1 invalid;
  M3's walk) over every consumer, not 25 files over one.
- (iii) At k4 the old function is gone, so the §3 one-liner cannot run, and E-k4.4's "the §3 control equal" is not
  checkable. Freeze the per-record, per-consumer vector in the k3 report, and have k4 compare the recast
  `acceptable_provenance(r, consumer)` to it.

The negative control stays (`old==bad` must be False). With matched records in the walk, it can fail on two words, not
one.

**K3-1 (blocking) — THE COLLISION (F-k4), answer.** These are **two true sites, not one acceptance under two names**:

| | C3-g `baseline_identity.readiness` | C3-k3 `baseline_identity.capture` |
|---|---|---|
| row | `baseline_identity` (field `status`) | `provenance_acceptance` (field `result`, via `provenance_word`) |
| word | the receipt's capture status (captured / inconclusive) | the probe's provenance word (matched / NA) |
| producers | `baseline_receipt:134`, `write_baseline_receipt:718` | runtime_probe |
| reader | `baseline_contract.deployment_readiness:199` (counts before-evidence, never blocks) | `manual_evidence.validate_baseline_record:680-687` (refuses a capture) |

Both carry the `baseline_identity` prefix. The capture consumer inherits `promotable: false` through the prefix rule
(`gate_registry.py:728-742`), so a later pc on it is one finding. The readiness consumer is guarded by its own row
(`_check_row` :658-660).

Owner of the registry edit: **C3-g removes `provenance.baseline`** (G-0 (a), already in its item 1 and E6), and
**C3-k3 only adds `baseline_identity.capture`** under `provenance_acceptance`. C3-g lands first (the Lead's order). So
F-k4 (a)'s "C3-k3 … removes `provenance.baseline` wherever the merged main holds it" and E-k3.5 world (ii) are a second
writer of a row k3 does not need. Restate F-k4 as: C3-g removes, k3 adds.

Exact amendments:
- **C3-g** (g-h §2), E6, last sentence → "C3-k3 adds `baseline_identity.capture` (row `provenance_acceptance`, reader
  `manual_evidence.validate_baseline_record`) in its own commit. C3-g edits no `provenance_acceptance` line and no F1 line
  but the readiness ones." Nothing else in C3-g changes.
- **C3-k3 owns**: delete "row `baseline_identity`: `provenance.baseline` removed if still there (F-k4)". Add the
  precondition: "based on a main where C3-g is merged: `provenance.baseline` absent from `gate-registry.json` and
  `baseline_identity.readiness` present; otherwise stop and return".
- **E-k3.5**: replace the two worlds with that precondition. INVARIANT: k3 writes no line of row `baseline_identity`.
- **k3 item 2**: delete "`provenance.baseline` is removed from `baseline_identity` if the merged main still holds it".
- **k3 item 7** (F1 / K-N2.12): it must not replace C3-g's readiness pins. On top of C3-g's main it adds:
  - `home["baseline_identity.capture"] == "provenance_acceptance"`;
  - the F1 line for `provenance.environment_preparation` (:640-641) is replaced by
    `home["environment_preparation.deploy_proof"] == "provenance_acceptance"`;
  - the sorted `provenance_acceptance` consumer list (:642-645) gains `baseline_identity.capture` and
    `environment_preparation.deploy_proof` (beside k2's `provenance.identity` and `provenance.run`);
  - the F1 loop keeps `("baseline_identity.readiness","baseline_identity")`, adds `("baseline_identity.capture",
    "baseline_identity")`, and replaces the environment_preparation pair with `("environment_preparation.deploy_proof",
    "environment_preparation")`, each still exactly one finding naming the consumer and the guarding row;
  - K-N2.12 NEG keeps C3-g's readiness probe and adds a parallel probe on `baseline_identity.capture` (exactly one
    finding, naming it and `person_confirmed`);
  - "both guarding rows are promotable false" stays.
- **k4 `decides`**: name the capture consumer: "baseline capture takes matched or any not_applicable; a person's word
  never".

**K3-2 — owns by pointer.** "The existing keep test files that `--witness-for` prints … (the builder names them before
writing)" breaks R11-m (owns inline). I ran `--witness-for` on the four scripts. The files that hold these sites' rows
today are:
- `scripts/tests/test_manual_evidence.py` (`_provenance_errors`, `baseline_person`);
- `scripts/tests/test_coverage_contract.py` (`validate_manual_current`);
- `scripts/tests/test_manual_capture.py` (`stand_probe`);
- `scripts/tests/test_environment_preparation.py` (`_run_step` / `provenance_validation`).

Name them as absolute paths. If one is not a keep row of `test-layers.json`, the builder names the keep file that
`--witness-for` printed instead (the coverage_contract list printed no `test_coverage_contract.py` within its first rows,
so check it).

**K4-2 — F-k5 (a) adds a fifth copy of a prefix a standing finding wants built once.** The finding
`plans/piles/rules-debt/findings/20261117-c3-odin-stroitel-teksta-reestr-ne-chitaetsya.md` (on the branch) chose one
builder (`gate_template.registry_why(tail)`) for the four copies of "the gate registry cannot be read (<reason>): a
factory defect, …". k4's `refusal_text` sentence is a fifth copy. Fix, either:
- k4 waits for that node and calls the builder; or
- k4 writes its copy, and the finding gains `profile_contract.refusal_text` as its fifth place in the same move
  (rule 9: queued explicitly).

Also: `refusal_text` must import `registry_problem` at the point of use. `profile_contract` is imported at module load by
most scripts, and a top import would load `gate_registry` everywhere.

**K4-3 — readers list.** F-k3's list of `ACCEPTS` / `acceptable_provenance` readers lacks `test_launch_wrappers.py` (K2-1,
fixed in k2). The k4 mapping `("matched",)` → `"environment_preparation.deploy_proof"` in
`test_runtime_probe_onboarding.py:1277, :1389` is legal but names a deploy consumer for an onboarding strictness row.
Accept it, or add a comment line saying why that consumer.

What holds in C3-k:
- the §3 site table (M2: complete);
- the A26 constraint reading (`gate_registry.py:837-841`; K-T1.7 :587-589);
- the four-way split and its TEMPORAL chain. k1 words leave `--check` green (M2). k2/k3 allow entries on a debt row are
  inert: `_allowed` returns True for a non-converted row (:775-776), and every entry matches a live comparison (F-d). k4
  converts with every literal already gone or allowed (M2's list minus k2/k3's removals equals the allow set);
- F-k6 (a): `acceptable` resolves a consumer to the row that lists it, so a consumer under `environment_preparation`
  (words blocked/unknown) could accept nothing;
- removing `provenance.environment_preparation` (A2) leaves that converted row with `accepts: {}`, which is legal;
- F-k2 (a)/(a) (M4); F-k3 (a); F-k7.
- On the unreadable registry, every site errs toward refusal. `registry_problem`/`acceptable` never raise. No path makes
  a broken registry a pass. The false-cause residue until k4 is named (E-k2.2) and fixed by F-k5 in k4.

## D. Standing questions

- **DUPLICATION AND CONSISTENCY**: J3 (`PROFILE_SCOPES` beside `ROLE_SCOPES`, instead of per-site literals), J4 (one
  `limit_seconds`), K4-2 (the registry sentence). The four local-source copies get one survivor (k1, measured: exactly 4
  copies, grep `target_kind.*local_source` over `scripts/` outside tests; the positive control is the same grep finding
  `run_suite.py:2513`). Nothing else found: greps `acceptable_provenance|\bACCEPTS\b`, `"level"` scope reads in
  gate_brief/gate_preflight/stand_gaps/environment_record/driver_machine.
- **CODE QUALITY**: K1-1 (two words for one fact), K2-2 (the masking allow), J6 (a "find an approach" item).
- **ONE ACTION, ONE ROAD (P31)**: C3-j stays on the stand-gap → record → cover road (F-j3 (a)). J3 is its missing half:
  the card reaches gate_brief's case branch, which is a second rendering of a profile-level gap. C3-k: one producer, one
  predicate, one composition (F-k3 (a)). `driver_stage_build.build_outcome` stays under `stand_identity` `dispatch` and
  reaches the predicate only through the composition. That is legal: its tuple `result in ("matched","person_confirmed",
  "not_applicable")` (:377) only picks the line to print.
- **TESTS (TESTING.md)**: every row goes into existing keep tables (good). Missing: J9 (the named flips, the FR-6 scan
  list, the CLI battery), K2-1, K2-2, K-C1, K1-2. None of the five needs a `tests-over:` line if the rows land in
  existing tables.

## E. Class completeness (rule 5, SIBLING_MAP)

Axis 5 (row ↔ sites ↔ prose twins) is walked per card (C3-j siblings, k4 siblings). The class "a profile-level gap read
by scope" is not walked beyond one file (J3). The class "a mock or pin bound to a renamed predicate" is not walked (K2-1,
K-C1). The class "the registry-unreadable sentence" is K4-2. The class "a converted row's word compared in an unregistered
function" (A1) is covered for C3-j (`check_s5_reporter`) and for C3-k (M2: no unregistered item after k4 on either tree).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "C3-j J1: the stand-gap accept/accept always on the unmeasured card means the e2e cases are blocked forever (driver_machine.carry_environment_properties :3074-3119, stand_gap_words accept says stays blocked); the card never states the executor - owner question",
    "C3-j J2/M5: the premise is inverted - 3/3 recorded stories (cart-1, local-1-0108, local-1-arm-b) have e2e-ui rows and no wait/load, so every one gets a new gate A card with no key and no persistence",
    "C3-j J3: gate_brief.py (_gap_heading :1565, _lasting_lines :1612, stand_gap_form_ids :959, _ids_of :1303, :1639, :1742, :1794), gate_preflight.gap_name :1612, driver_machine._level_remedies :3129 read scope level and are out of owns",
    "C3-j J4: limit_seconds lives in gate_preflight.py:157, so the card's own stop fires - move it to environment_record",
    "C3-k2 K2-1: tests/test_launch_wrappers.py:163,:167 patch acceptable_provenance on RS/ER and break after k2",
    "C3-k2/k3 K-C1: the exact allow-list pin test_gate_registry.py:299-302 (branch :305-308) is not in owns and goes red on the canon only",
    "C3-k3 K3-1: the collision - k3 must add baseline_identity.capture beside C3-g readiness pins, not replace them, and must not write row baseline_identity"
  ],
  "fixes": [
    "J1 owner question on the meaning of accept for the unmeasured card, then pin the cases' fate in a test",
    "J2 fork: key an absent wait as wait_s unrecorded, or keep E2 and tell the owner the measured cost; reconcile E2 with the parent",
    "J3 owns gains gate_brief.py functions and gate_preflight.gap_name; PROFILE_SCOPES in stand_gaps beside ROLE_SCOPES; enumerate each listed read",
    "J4 move limit_seconds into environment_record and import it in gate_preflight",
    "J5 carry F-j4 (b) into item 3, E9, E13, the old-waiver and unmeasured-card rows, and section 8",
    "J6 decide the row-then-add order as the reporter does and add an answered-row test",
    "J7 add wait to row environment_property_cover and name the near_miss precedence",
    "J8 pick null/empty or the named keys for scope_keys and binding_keys",
    "J9 name the flipping tests, add _limit_gap_row to the FR-6 scans, add the CLI adversarial rows",
    "J10 split C3-j along AR-22 if it stays large",
    "K-C1 k2 and k3 update the allow-list pin by their exact entries",
    "K2-1 k2 owns test_launch_wrappers.py other_places_use_the_one_launcher and patches acceptable",
    "K2-2 pin exactly one checked result not_applicable comparison in validate_request",
    "K2-3 state the gate A world in E-k2.2 and queue the finding",
    "K2-4 name the import placement per file; k2 drops ACCEPTS from execution_request",
    "K1-1 a valid declared mismatched or unknown keeps its word",
    "K1-2/K3-3/K4-1 per-consumer matrix, the 133-record walk, and a frozen vector for k4",
    "K3-1 apply the collision amendments to C3-g E6 and to k3 owns, E-k3.5, item 2, item 7, and the k4 decides",
    "K3-2 name the four test files inline",
    "K4-2 route the refusal_text sentence through the one-builder finding or add it to that finding; lazy import",
    "K4-3 complete the readers list"
  ],
  "class_completeness": "Axis 5 walked per card; the profile-level gap scope class is not walked beyond stand_gaps.py (J3); the class of mocks and pins bound to the renamed predicate is not walked (K2-1, K-C1); the registry-unreadable sentence class goes to the standing one-builder finding (K4-2); the A1 class holds (M2, M6).",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-rules-debt-wave3-j-k-cards.md (whole)",
      "docs/tasks/specs/20261117-rules-debt-wave3-g-h-cards.md :1-317, :434-439, :533-536",
      "docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md :1287-1380, :1686-1704 (+ grep of C3-j/C3-k/forks)",
      "ai-packages/qa-factory/scripts/gate_registry.py :560-912",
      "ai-packages/qa-factory/scripts/gate_template.py :40-97",
      "ai-packages/qa-factory/references/gate-registry.json :37-95 and the rows s5_stand_limits, environment_property_cover, environment_preparation, baseline_identity",
      "ai-packages/qa-factory/scripts/profile_contract.py :15-24, :705-925",
      "execution_request.py (branch) :155-185, rehearsal_probe; execution_fingerprint.py :110-140; manual_evidence.py :74-133, :660-700; coverage_contract.py :815-850; manual_capture.py :1595-1616; run_suite.py :916-930; environment_preparation.py :378-395; gate_preflight.py :150-175, :1495-1665, :3089-3280, :4130-4252, :5139-5146, :6078-6112; driver_stage_build.py :372-386",
      "environment_record.py :100-215, :280-350; stand_gaps.py :148-159, :955-1025; gate_brief.py :945-1000, :1295-1310, :1546-1645; driver_machine.py :3074-3135",
      "question-vocabulary.json stand_gap_words, environment_words",
      "tests: test_gate_registry.py :255-320, :580-592, :630-706 (and the branch :305-308); test_gate_preflight.py :2795-2870, :3645-3660, :3800-3815, :4255-4268; test_execution_request.py :678-690, :1328-1337; test_role_commands.py :958-968; test_launch_wrappers.py :150-175",
      "branch findings: plans/piles/rules-debt/findings/20261117-c3-*.md (six files); controller.py dispatch diff"
    ],
    "reruns": [
      {"command": "python -B ai-packages/qa-factory/scripts/gate_registry.py --check (main)", "result": "A26 gate registry: no violations; 6 gate(s) left as debt; exit 0"},
      {"command": "python -B ai-packages/qa-factory/scripts/gate_registry.py --sites (main)", "result": "145 lines, exit 0; the provenance_acceptance lines match the plan's table"},
      {"command": "gate_registry.py --check on the C3-b2 branch tree (git archive to the scratchpad)", "result": "no violations; 4 gate(s) left as debt; 150 items"},
      {"command": "sim.py: analyse() with k1 words, then the row converted (main and branch)", "result": "k1: 0 findings, +5 items (4 local_source, 1 NO_CHANGED_FILE); convert-now: F-b on 13 accept sites and F-a exactly on the plan's literals"},
      {"command": "simj.py: analyse() with C3-j's row (main and branch)", "result": "0 findings; +5 items: check_s5_stand_limits x4, check_s5_reporter x1"},
      {"command": "acceptable_provenance over the 25 runtime-provenance-*.json", "result": "25 person_confirmed, all accepted (rehearsal too)"},
      {"command": "walk of every fixture JSON for provenance-shaped dicts", "result": "79 matched, 53 person_confirmed, 1 invalid, 0 not_applicable"},
      {"command": "decode config-at-start + s5_automate_rows/s5_profiles for cart-1, local-1-0108, local-1-arm-b", "result": "web has no page_object_max_wait_s and local no measured; e2e-ui rows 1, 13, 10 - unmeasured on 3/3"},
      {"command": "grep acceptable_provenance|ACCEPTS over scripts/ (positive control: the known execution_request.py:17 hit found)", "result": "extra reader test_launch_wrappers.py:163,:167 (mock.patch.object)"},
      {"command": "scenario_walk.py --witness-for manual_evidence/coverage_contract/manual_capture/environment_preparation", "result": "scenario and keep files printed; the site rows live in test_manual_evidence, test_coverage_contract, test_manual_capture, test_environment_preparation"}
    ]
  }
}
```

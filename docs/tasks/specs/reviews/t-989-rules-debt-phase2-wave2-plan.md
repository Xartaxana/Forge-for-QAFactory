# t-989 — critic on plan: rules debt phase 2, wave 2 cards (C3-*, S9, FL2, FL4)

Spec under review: `docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md` (§0, §1, C3, S9, FL2, FL4, §3, §4, §6-§7,
Lead decisions, C4 result), the parent spec `docs/tasks/specs/20261117-rules-debt-fix-spec.md` (S9 :379-394, F-L2/F-L4
:538-545, the owner's F-O1 words :614-643), the wave 1 review `reviews/t-968-rules-debt-phase2-wave1.md`. Code read on
`origin/main` = `a372b01a` (`git archive origin/main ai-packages/qa-factory` into the scratchpad; every line below is from
that tree). One critic pass for the topic (R13-g). This is a verdict, not the decision: acceptance and the spec edits are
the Lead's.

## Verdicts

| card | K1 facts | K2 meaning | K3 weaker model | K4 AR/P | K5 edges | K6 collisions | K7 feasibility | K8 siblings | verdict |
|---|---|---|---|---|---|---|---|---|---|
| C3 shared (S-a..S-d, DoD, E-a..E-d) | 2 stale | S-c open question is decidable now | S-c "return a question" fires on most cards | ok | ok | registry row-disjoint | merge the no-code cards (F-K7) | census axis missing | fit_with_fixes |
| C3-0 | stale (scoped to F-D1 (a), but the Lead took (b)) | signature does not fit the rows it must serve | not drafted | ok | — | — | needed under (b) too | — | unfit (designer) |
| C3-a | ok | ok, code already does it | S-c words open; pin lives in a quarantined file | ok | ok | none | no code | ok | fit_with_fixes |
| C3-b | ok | unknown vs absent conflated; relaxes a block | answer carrier "named by the plan" | AR-29 ok | E3 not decidable | judgment-census | split; test_identity needs C3-0 | axis 7 | unfit (designer) |
| C3-c | ok | ok, done and pinned (K-C4) | new row duplicates K-C4 | ok | ok | wave-a touches s5_precheck (not `run`) | no code | — | fit_with_fixes |
| C3-d | ok | S-b is red by design: an unmeasured detector is INFO today | not drafted | AR-28 change | — | after S9 | meaning change | axis 25 | unfit (designer) |
| C3-e | ok | ok, `decide` already does it | new row duplicates `test_third_verdict` | FR-19 ok | E1 unpinned | none | no code | — | fit_with_fixes |
| C3-f | "test status not read" now read | S-b names the wrong unknown; code refuses, no question exists | branch to pick | — | — | none | registry branch vs code | — | fit_with_fixes |
| C3-g | ok | refusal site not named; `deployment_readiness` never blocks | needs C3-0 | — | — | — | waits for C3-0 | — | unfit (wave 3, after C3-0) |
| C3-h | ok | ok | ok | ok | ok | gate_preflight queue 4th | registry + pin | — | fit_with_fixes (queue text) |
| C3-i | ok | ok | item (1) "the plan confirms"; re-roles undecided | ok | ok | gate_preflight 1st | no code | census | fit_with_fixes |
| C3-j | ok (all lines hold) | the writer path for the answer is not established | `stand_gaps` road not owned | AR-22 at risk | E6 ok | owns must add `stand_gaps.py`, census | — | axis 26/32 | fit_with_fixes (wave 3) |
| C3-k | ok | — | designer first (stated) | — | — | — | — | — | fit_with_fixes (queue text) |
| S9 | 2 lines drifted | the pass's effect on delivery not decided; `*` vs `split_overridden` | no plan at all | AR-27/FR-35 open | premise (а) not measured | controller HOT, census | — | axis 26, 32, 34 | unfit (designer) |
| FL2 | the named writer is wrong (plan row, not run row) | premise measured here: 1 live row | writer "named by the plan" | P31 second road | — | after C3-e | weigh the existing road | axis 34 | unfit (designer) |
| FL4 | 2 lines drifted | schema change not drafted | pointer only | — | — | controller HOT | — | axis 5 | unfit (designer) |

Counts: fit_with_fixes 9 (C3 shared, a, c, e, f, h, i, j, k); unfit 7 (C3-0, C3-b, C3-d, C3-g, S9, FL2, FL4). Nothing is
proposed for a queue: every fix below is card text the Lead can write this round. Six cards are unfit only in the sense
that they are not builder specs yet: they need a designer draft. That is the plan's own wording ("design detail is the
plan's", "Designer + plan critic"), so they cannot be wave 2 builder dispatches.

**Wave 2 as I would dispatch it after the fixes:** one registry node **C3-R** (C3-a + C3-c + C3-e + C3-f + C3-i, F-K7),
plus designer drafts for C3-0, C3-b (split), C3-d, S9, FL2 and FL4. C3-g, C3-h, C3-j and C3-k go to wave 3.

---

## Findings — C3 shared items

**F-S1 (K1/K3) — S-c's open point is decidable now: a `code` row with empty `words` FAILS the row check.**
`gate_registry.py` `_check_row`: `words` "must be a non-empty list of strings (only an exempt row may list none)". `--sites`
on origin/main also lists NO literal comparison at the sites of `collected_ids` (run_suite `verify_node_ids`,
`ids_pytest_did_not_find`), `s5_coverage` (`s5_precheck.run`), `reporter_rehearsal_identity`, `environment_property_cover` and
`s5_stand_limits`. So S-c's "if the sites compare no literal word, the builder returns a question" would fire on C3-a,
C3-c, C3-i and C3-j: four returns by design. The converted precedents show the rule. `inputs_unchanged` is `code` with
`["inconclusive"]`, `finish_exit_gate` is `code` with `["accepted","refused","unreadable"]`: the words are the outcome words
the gate's code WRITES, compared or not.
Replacement for the S-c bullet's last sentence ("If the sites compare no literal word at all, the builder returns a question
(…not established).") —
> `words` = the outcome words the row's code writes for each class, as they appear in the code: the literal verdict words
> the sites compare (`python -B ai-packages/qa-factory/scripts/gate_registry.py --sites`, the row's files), and when the
> sites compare none, the words the row's own functions return or write for matched / mismatched / unknown (precedents:
> `inputs_unchanged` `["inconclusive"]`, `finish_exit_gate`). Each word gets a `verdict_map` entry, and the unknown-class
> word carries its `owner`. `words` is never empty: `_check_row` refuses an empty list on any non-exempt row. The per-card
> words are given in the card.

**F-S2 (K1) — DoD flag.** `--check` exists (`gate_registry.py:942`), exits 0 on origin/main, and prints `14 gate(s) left as
debt:` followed by one line per row. Replace "(the A26 CLI; exit 0 and the row gone from the debt list — exact flag confirmed
by the builder from `--help`)" with:
> (exit 0, and the row's id is absent from the `N gate(s) left as debt:` block that `--check` prints)

**F-S3 (K1) — §0.1 small stale reference.** "`_scan_tree` records any call whose name or attribute is `acceptable`,
:234-237": the recording sits in `_walk` (`gate_registry.py:205-237`, the check at :235-237). The meaning is unchanged.
Replace `_scan_tree` with `_walk`.

**F-S4 (K8, axis 32) — no C3 card owns the census.** Axis 32: "a new check in ANY `scripts/*.py` gets its census row in the
SAME commit". C3-j (a cover lookup and a new card), C3-b (a new window question) and any C3 card whose S-b is red and moves
code add check units. None of them lists `scripts/tests/fixtures/judgment-census.json`. `wave-a/integrate` (not merged)
also edits that file (`+_load` row, :834). Add to "Shared items":
> - S-e. A card that adds or changes a check unit in `scripts/*.py` owns
>   `ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json` (its own rows only, class per the §1 table) and is
>   based on `main` after `wave-a/integrate` lands (that branch edits the same file). A card that moves no code does not
>   touch the census.

**F-S5 (K2/K4) — E-c needs the re-role judgments themselves, and here they are.** The Lead's decision (F-D1 (b)) puts every
re-role to this critic. Reading each accept site on origin/main:

| row | site | today | judgment | why |
|---|---|---|---|---|
| test_identity | `proof_level.same_test` (:850) | accept | **produce** | it RETURNS the row's words (`raw`/`instance`/`instance_code`/`file_code`/`""`); it consumes none |
| test_identity | `proof_level.already_probed` (:1404) | accept | **true accept** | compares `hit['holds'] in ('instance_code','file_code')` (:1520): it consumes the word to reuse a probe |
| test_identity | `execution_request._match` (:2078), `green_over_same_bytes` (:2169) | accept | **true accept** | they decide whether an old job or green is reused for this request |
| live_check_demand | `proof_level.proof_required` (:467) | accept | **produce** | it produces the demand (flags, `_NOVELTY_DEMANDS` membership, handed) and accepts no record; the receipt check is `reached` / the window's, registered elsewhere |
| s5_coverage | `s5_precheck.run` (:4598) | accept | **validate** | it produces findings and `unchecked[]` over the author's artifacts; no verdict word is compared (`--sites`: none) |
| delivery | `delivery_verdict.decide` (:119) | accept | **produce** | it computes the word |
| delivery | `check_delivery.assess` (:2558) | accept | **produce** | it FINALISES the word (`after_checks` with no item -> `no`, VERDICT_WITHOUT_ITEMS, :2626-2634) and writes `delivery_verdict`; its `in ('no', None)` reads go through `DV.verdict_of_kind` and err toward `no` |
| delivery | `check_delivery.ledger_reasons` (:1740) | accept | **produce** | it returns the texts of the blocking ledger records; no comparison |
| baseline_identity | `baseline_contract.deployment_readiness` (:175) | accept | **true accept** | it accepts `provenance.baseline` receipts (registry `accepts`) |
| reporter_rehearsal_identity + environment_property_cover | `gate_preflight._rehearse_reporter` (:3577) | accept (two rows) | **validate**, under `reporter_rehearsal_identity` only | the reuse decision is a key join (`_earlier_proof` -> `onboarding_probe.earlier_proof`); no verdict word is compared. Precedent `finish_exit_gate` (registry :596, "compares no verdict word and calls no acceptable()") |
| reporter_rehearsal_identity | `driver_gates.hand_to_conductor` (:1024) | accept | **dispatch** | it hands the state to the conductor and accepts nothing |
| environment_property_cover | `gate_preflight.check_case_preconditions` (:5460) | accept (+ dispatch under case_preconditions) | **drop from this row** | it stays only under `case_preconditions` (dispatch) |
| environment_property_cover | `gate_preflight._environment_cover` (:4214) | not registered | **validate** (new registration) | it holds the whole cover decision for gate A: key, `ER.load`, `ER.covering`, `ER.near_miss`, the note. Its three callers are :4149, :4995, :5645 |
| environment_property_cover | `stand_gaps.gate_b_split` (:962) | accept | **validate** | the gate B cover is a key join (`ER.covering` through `_c4`, :756-802), with no verdict word |
| s5_stand_limits | `gate_preflight.check_s5_stand_limits` (:3165) | accept | **produce** | it measures and cards; it accepts no record. After C3-j the record read is `_environment_cover`'s |
| s5_window | `acceptance.validate_window`, `window_record.verdict` | accept | not judged here | C3-d is unfit (F-d1) |

Result: under (b) the predicate is needed for exactly **test_identity** (three sites), **baseline_identity** (one) and
**provenance_acceptance** (C3-k). Every other row converts with no `acceptable()` call. Add the table to the C3 section
under "Decided branches" as "Re-roles judged by the plan critic (E-c)". In the table above it, replace the "accept sites
(F-D1)" column with "true accept sites after E-c": C3-b test_identity `already_probed, _match, green_over_same_bytes`;
C3-b live_check_demand none; C3-c none; C3-e none; C3-g `deployment_readiness`; C3-i none; C3-j none; C3-k (designer).

**F-K7 (K7, PROJECT.md «Командная работа» п. 9) — one node instead of five similar ones.** Measured on origin/main, the
unknown branch is ALREADY implemented, and in most cases already pinned, for:

- C3-a: `run_suite` docstring :36-41 and the row's own `decides`. The pin is `test_run_suite_mine.py` M-B3 (:1744,
  "an unreadable collect, then pytest's `not found`: node_id_mismatch, NOT EXECUTED"), but that file is QUARANTINED.
- C3-c: `s5_precheck.run` `unchecked[]` (:4614, :4665, :4737), pinned by K-C4 in `test_s5_precheck.py` (:843).
- C3-e: `delivery_verdict.decide` (:119-145: an unknown kind -> `no` + `VERDICT_KIND_UNKNOWN`, owner `factory` via
  `_finding` :46-47; an unreadable file -> `no` + `VERDICT_KINDS_UNREADABLE`). The unknown kind is pinned in
  `test_third_verdict.py:190` (keep, slow). The unreadable file is pinned nowhere: grep `VERDICT_KINDS_UNREADABLE` over
  `scripts/tests/` gives 0 hits; positive control, same tool and folder: `VERDICT_KIND_UNKNOWN` gives 2 files.
- C3-i: `uncheckable` rows in `test_gate_preflight.py` (5 hits); E9 / E14 (unreadable / revoked) in
  `test_environment_record.py:3-5,113`.

All five cards edit the same file (`gate-registry.json`) and move no code. Five builders on one JSON file give five
row-merges and five `--check` witnesses for what is one edit pattern. Proposed replacement for the wave 2 line of §3:
> **Wave 2 — C3-R (one builder node, registry conversions with no code):** rows `collected_ids`, `s5_coverage`,
> `delivery`, `environment_preparation`, `case_preconditions`, `reporter_rehearsal_identity`, `environment_property_cover`,
> each per its card (status, words, roles per the E-c table, branch, `test`), plus the pin rows named in each card. Owns:
> `references/gate-registry.json` (those seven rows), `scripts/tests/test_node_ids.py` (one row),
> `scripts/tests/test_third_verdict.py` (one row), and `test_gate_preflight.py` (one row) only if the C3-i grep finds no
> pin. Witness: `python -B ai-packages/qa-factory/scripts/gate_registry.py --check` (exit 0, the seven ids absent from the
> debt block) + `scenario_walk.py --witness-for <owns>`; the slow pin files are judged by the batch canon. A code edit of
> any site is OUT of C3-R: a pin that is red on real code stops the node with the red output (the C4 precedent).
> Designer drafts in parallel: C3-0 (F-D1 (b) scope), C3-b, C3-d, S9, FL2, FL4.

---

## C3-0 — unfit as written (designer)

**F-0-1 (K1/K2) — the card is written for the fork the Lead did NOT take.** C3-0 says "Not dispatchable until F-D1 is
decided. On F-D1 (a): …", and §3 wave 2 says "C3-0 (if F-D1 (a))". The Lead took (b): "the predicate only for true accept
sites". Under (b) the predicate is STILL owed for test_identity, baseline_identity and provenance (F-S5), and
`gate_registry.py:837-841` makes it mandatory (F-b fires on any converted accept site with no `acceptable` call). As the
plan reads now, C3-b, C3-g and C3-k depend on a card the plan says will not be built.

**F-0-2 (K2) — the signature does not fit two of the three rows it must serve.** `acceptable(record, consumer)` "reading the
row's `accepts[consumer]` and `verdict_map`" assumes a row with a `field` and an `accepts` map. `test_identity` has
`field: null` and `accepts: {}`. Its sites compare a bare word (`hit['holds']`), not a record field. Only
`baseline_identity` (`accepts: provenance.baseline`) and provenance fit the record form.
Replacement for the C3-0 header and first sentence:
> #### C3-0 — the one predicate for true accept sites (F-D1 (b), Lead 17.11) — designer, then plan critic
> Needed by C3-b (test_identity: `already_probed`, `_match`, `green_over_same_bytes`), C3-g (`deployment_readiness`) and
> C3-k. The designer settles: (1) the call shape for a bare word as well as for a record (`acceptable(value, consumer)`,
> where `value` is the record or the word and `consumer` is `<gate>.<consumer>`), and the `accepts` entries test_identity
> gains for its three consumers; (2) the error direction, toward NOT acceptable (unknown consumer, absent record or word,
> a word outside `words`, another case such as `Matched`, a list or dict as the word, an unreadable registry -> False);
> (3) where it lives (`gate_template.py`, the name the A26 finding texts already print, `gate_registry.py:840,878`).
> Not a wave 2 builder dispatch.

---

## C3-a — fit_with_fixes (into C3-R)

**F-a1 (K3/TESTING) — the S-b row's world exists only in a quarantined file.** `test_node_ids.py` (keep, slow) has no
`node_id_mismatch` row. The exit-4 branch is pinned only by M-B3 in `test_run_suite_mine.py` (quarantine). Positive
control: the same grep found the word in four test files. Replacement for the S-b sentence:
> S-b row in `test_node_ids.py`: the world of `test_run_suite_mine.py` M-B3 (:1744, a quarantined file, read for its world
> only, not edited): an unreadable collect, then pytest's exit 4 -> the summary says `node_id_mismatch`,
> `execution_status: not_executed`, never passed or failed, and the ids are named "not verified", never "missing".
> Expected values from the row's `decides` and the owner's «да» (F-O1). `run_suite.py` is not in owns: if the row is red on
> real code, the node stops with the red output.

**F-a2 (S-c words).** Add:
> Row edit: `vocabulary: code`, `words: ["node_id_mismatch", "not_verified"]`,
> `verdict_map: {"node_id_mismatch": {"class": "mismatched"}, "not_verified": {"class": "unknown", "owner": "environment"}}`,
> `unknown_branch: rerun`, `on_no_answer: rerun`, sites keep `validate`.

Here `not_verified` is the token form of the "not verified" note (`run_suite.py:1674`). If the builder finds the code
writes no such token, the row says `["node_id_mismatch"]` alone and the report names it.

## C3-b — unfit (split; designer)

**F-b1 (K2, blocking for this card) — the card conflates stored `unknown` with an absent key, and the conversion would
RELAX a block.** `proof_level.novelty_of` (:393-427): an absent key gives `(None, "")` (a legacy row). A stored `unknown`
already DEMANDS a live probe: `proof_required` (c), `_NOVELTY_DEMANDS`. The debt the row names ("a legacy row whose novelty
nobody measured is shown to the person as a debt") is `not_required_why == "unmeasured"`: no key, no flag, not handed. The
card's "novelty `unknown` -> a question to `role:qa-code-critic`" applied to stored `unknown` would replace a demanded
probe with a question, which is weaker. E2 ("absent novelty field = unknown (asked)") is the actual change.
Measured (п. 6 (а), which the card asks for and does not carry), `novelty_of` / `proof_required` / `not_required_why` over
every `tests[]` row of the recorded stories:
`cart-1: 18 rows {None: 18}, all (None, required=True, why='')`;
`local-1-0108: 34 rows {None: 34}, all (None, required=True, why='')`.
So on both recorded stories every row is legacy, yet every row is already required by its flags. The question would fire
on **0 of 52** rows. The change bites only on keyless, flagless rows, which neither fixture has. A test row for it must
build that world.

**F-b2 (K3) — the critic's typed answer has no carrier.** "the window-acceptance reader of the critic's answer (named by the
plan — not established here)". The builder would invent the field, its writer and its reader. Existing carriers:
`novelty` (one writer, `manifest_from_tests.py`, row form with `measured_by`; `manifest_put.novelty_row_problems` refuses
anything else, :531-558) and `sensitivity_proof_required` (a row flag that makes the probe required). The designer picks
one. My recommendation: the critic's "a probe is owed" = setting `sensitivity_proof_required: true` through the existing
fragment, which then flows through `proof_required` with no new reader, and "not owed" = a typed answer the window reads.

**F-b3 (K4/K2) — the registry edit is incomplete.** `on_no_answer: wait` requires non-empty `closed_by`, and a `role:`
closer requires `person` (`_check_row`: "names a role without `person`: a person's word passes every block (FR-4, P13)").
The card names only the addressee. Add:
> `unknown_branch: question`, `on_no_answer: wait`, `waits_at: window_acceptance`,
> `closed_by: ["role:qa-code-critic", "person"]`, `addressee: ["role:qa-code-critic"]`,
> `vocabulary: code` (the words `new/changed/unchanged/unknown` are already the code's).

**F-b4 (K5) — E3 is not decidable by code.** "rows already shown as debt in stories in flight are not re-asked": nothing
tells a story in flight from a new one. Builder-rules 9 (`plans/builder-rules.md:99`) also forbids refusing a story in
flight over an old artifact's missing field. The designer states the observable that decides it (for example: the question
applies only to a window whose manifest has at least one row carrying `novelty`, which means the writer of this version
ran), or the owner accepts that in-flight stories are asked.

**F-b5 (K7) — split the card.** test_identity needs C3-0 (three true accept sites, F-S5). live_check_demand needs no
predicate (`proof_required` -> produce, `novelty_of` -> produce) but does need F-b1..F-b4 designed. Two cards: C3-b1
live_check_demand (designer, then builder, wave 2½) and C3-b2 test_identity (after C3-0, wave 3; `same_test` -> produce).

## C3-c — fit_with_fixes (into C3-R)

**F-c1 (K7/TESTING) — the S-b row exists.** The card's row ("a Then whose binding cannot be established -> a question to the
code critic") is already `unchecked[]`: the case, the file and the checks not done, left to the code critic (module
docstring :46, :74; built at :4665). It is pinned by K-C4 (`test_s5_precheck.py:843-854`, a `.cs` file). A new row would
duplicate it (brief q6). Replacement for "Item: …":
> Item: no code moves and no new test row: S-b is `test_s5_precheck.py` K-C4 (:843). Row edit: `vocabulary: code`,
> `words: ["matched", "mismatched", "unchecked"]`, with `unchecked` -> `{"class": "unknown", "owner": "role"}`;
> `s5_precheck.run` re-roled `validate` (E-c table). The branch stays question / wait / window_acceptance; the window's
> wait is the instance's `review` gap, which stays until the critic records `critic_verdict`.

**F-c2 (K6).** The FL9 queue line is moot: FL9 (t-962) stopped at its E1 with no diff (`a18336d2`). `wave-a/integrate` edits
`s5_precheck.py` (check_manifest … check_plan_conformance, not `run`) and shifts its lines by about +19. Since C3-c moves no
code, it runs in parallel. Replace the Edge sentence with:
> Edge: no code in `s5_precheck.py` moves, so no queue against FL9 or `wave-a/integrate`.

## C3-d — unfit (designer, after S9)

**F-d1 (K2, blocking for this card) — S-b is red by design, and making it green changes a meaning the card does not name.**
`window_record.verdict` (:1816-1838) says of `expectation_changes_unmeasured`: "Not a problem and not a gap: the detector
could not measure, the story goes on". `_run_freshness_unknown` (:1785-1797): "not a gap - the story goes on". The row's
`decides` ("an unmeasured detector is a gap closed by the critic, never a pass") does not describe the code. The card's
S-b would turn INFO lines into blocking gaps that wait on the critic. That is a meaning change of the S5 window, so
PROJECT.md п. 6 applies: measure first how often recorded stories carry these lines, and decide which unmeasured
detectors (expectation changes, run freshness, unknown targets, probe scope: `verdict` :1822-1828) become gaps. The other
option is to correct the row's `decides` to the code ("said as INFO, owner role") and convert on that. The card states
neither. Replacement for the C3-d Item:
> Item: designer first. Today an unmeasured detector of the window is an INFO line, never a gap
> (`window_record.verdict` :1831-1837, `_run_freshness_unknown`). The designer returns the fork: (i) the row's `decides`
> is corrected to the code and converted as is (S-b pins the INFO line), or (ii) the listed unmeasured detectors become
> gaps closed by the critic (a meaning change: п. 6 measurement on `cart-1` / `local-1-0108` windows, plan critic). Rec (i)
> unless the Lead or the owner wants the stricter window.

## C3-e — fit_with_fixes (into C3-R)

**F-e1 (K7/TESTING).** The unknown-kind branch is implemented and pinned (`test_third_verdict.py:190`). The row's `test`
names `test_check_delivery.py`, which carries no such row. The unreadable-file branch (E1) is pinned nowhere (0 hits,
control above). Replacement for the owns line and the S-b sentence:
> owns: gate-registry.json (row `delivery`); `ai-packages/qa-factory/scripts/tests/test_third_verdict.py` (one row).
> No code moves: `delivery_verdict.decide` (:119-145) already answers an unknown kind and an unreadable file with `no` and
> a `factory`-owned finding. Row edit: `vocabulary: code` (the words are the code's), `unknown_branch: refuse_with_door`,
> `on_no_answer: refuse_with_door`, `test: scripts/tests/test_third_verdict.py` (it pins the unknown kind, :190), the
> three sites re-roled `produce` (E-c table). S-b row added to `test_third_verdict.py`: an unreadable / empty kinds file
> -> `("no", [VERDICT_KINDS_UNREADABLE])`, never `yes` or `after_checks`. Expected from the row's `decides` and FR-19.

**F-e2 (K4, FR-3).** The door of `refuse_with_door` here is the factory developer's ("add the kind there in the change that
writes it", :140). FR-3 says our own defect is reported, never asked. `addressee: []` stays. Add to E2:
> The door is the factory's own (the finding text names the kinds file); no person is asked (FR-3).

## C3-f — fit_with_fixes (Lead picks the branch)

**F-f1 (K1).** "The keep/quarantine status of those two test files was not read today": both are keep, not slow, not
quarantined. (Checked against `test-layers.json` `quarantine` and `slow_tests.json`. Positive control: the same check
reports `test_judge_results.py` quarantined.) Replace the sentence with:
> `test_environment_preparation.py` and `test_baseline_contract.py` are keep and fast: run them in the DoD.

**F-f2 (K2) — S-b names the wrong unknown, and the declared branch is not what the code does.** The card says "unknown deploy
proof -> question at authorization, waits". The deploy proof is provenance's (`_run_step`, registered under
`provenance_acceptance`). This row's own unknown is unknown compatibility facts or an unknown existing runtime. The code
REFUSES them: `_facts` raises `PreparationError("unknown compatibility facts: …")` (:44-60), `plan_environment` refuses
an unidentified existing runtime (:126-130), and `execute_environment` turns refusals into `blocked` with the reason
(:443-466). The CLI exits 2 (:613-617). No question at authorization exists in the module. Pins exist:
`test_unknown_compatibility_never_selects_rebuild` (:81) and `test_unknown_outcome_blocks_instead_of_relaunch` (:133).
Replacement for C3-f's text:
> C3-f owns: gate-registry.json (row `environment_preparation`). No code moves. The unknown is an unknown compatibility
> fact or an unidentified existing runtime; the code refuses it as `blocked` with the missing facts named (exit 2).
> Row edit: `vocabulary: code`, `words: ["blocked", "unknown"]` (`unknown` from `_facts` :51), `unknown_branch:
> refuse_with_door`, `on_no_answer: refuse_with_door`, `waits_at: null`, `closed_by: []`; S-b =
> `test_environment_preparation.py::test_unknown_compatibility_never_selects_rebuild` (exists). This changes the
> registry's declared "question at authorization" to what the code does; the Lead confirms it (a keep the owner did not
> word).

If the Lead keeps "question at authorization", C3-f becomes a designer card: a new question mechanism in a module that has
none.

## C3-g — unfit (wave 3, after C3-0)

**F-g1 (K2/K3).** `deployment_readiness` is a true accept site (F-S5), so the card cannot convert before C3-0. Its docstring
(:175-182) says it reports gaps "without blocking current-version execution" and that `ready` "is always true". The S-b
"unknown old-build identity -> refused with its door" therefore has to name the function that refuses. Candidate:
`validate_baseline_request` (validate). This was not established. Add:
> Dispatch after C3-0. S-b names the refusing function (`baseline_contract.validate_baseline_request` is the candidate:
> designer confirms by reading); `deployment_readiness` never refuses (docstring :175-182) and goes through
> `acceptable(…, "provenance.baseline")`.

Move C3-g from wave 2 to wave 3 in §3.

## C3-h — fit_with_fixes

The facts hold: the five sites exist (A26 `--check` reports no stale site). The current words are the code's
(`_derive_probe` :4586-4594 compares all five), so `vocabulary: code` with the same words is honest. Fix:
> Row edit: `vocabulary: code`, words unchanged. Sites keep their roles (produce/dispatch: none is accept).

## C3-i — fit_with_fixes (into C3-R)

**F-i1 (K3) — item (1) leaves the decision to the builder ("if it holds the whole cover decision; the plan confirms").**
Confirmed by reading (`gate_preflight.py:4214-4247`): `_environment_cover` holds the whole gate A cover decision. The gate B
cover lives in `stand_gaps.gate_b_split` (`_c4` :756-802). Replacement for item (1):
> (1) Registrations after the change. `environment_property_cover`: `gate_preflight._environment_cover` (validate) and
> `stand_gaps.gate_b_split` (validate); `_rehearse_reporter` and `check_case_preconditions` are removed from this row.
> `reporter_rehearsal_identity`: `_rehearse_reporter` (validate), `_read_probe_report` (measure),
> `driver_gates.hand_to_conductor` (dispatch). `case_preconditions`: unchanged. No function is then registered by two
> rows (the F-f "more than once" rule). Words: `case_preconditions` unchanged (`code` already);
> `reporter_rehearsal_identity` `["reused", "rehearsed", "none", "command_changed", "unreadable"]` and
> `environment_property_cover` `["covered", "changed_since", "not_covered", "unreadable"]`, the outcome words the
> `decides` texts name, read against the code (`row["changed_since"]` :4241, the `unreadable`/`none`/`command_changed` of
> the rehearsal's record reader). The unknown-class words carry their owner per `verdict_map`.

**F-i2 (K7/TESTING).** S-b pins mostly exist: `uncheckable` -> gate A question (`test_gate_preflight.py`, 5 hits) and
unreadable / revoked record (E9, E14, `test_environment_record.py:3-5,113`). The rehearsal `unknown` (no row of this
command -> rehearsed again) has no hit for `command_changed` in `test_gate_preflight.py` (control: `uncheckable` found by
the same grep). Replacement for item (2):
> (2) S-b: name the existing pins in the report (`test_environment_record.py` E9, E14; the `uncheckable` rows of
> `test_gate_preflight.py`); write ONE new row in `test_gate_preflight.py` only for `reporter_rehearsal_identity`'s
> unknown (a record with no row of this command -> the command is rehearsed again, nothing reused), expected from the
> row's `decides`, unless the builder's grep finds it pinned. No code moves (out of C3-R otherwise).

Owns lose `gate_preflight.py`, `driver_gates.py` and `stand_gaps.py` (no code). That takes C3-i OUT of the gate_preflight
HOT queue: the queue becomes C3-j -> C3-k -> C3-h.

## C3-j — fit_with_fixes (wave 3)

The facts hold line by line (`environment_record.py` :33, :35, :133, :165, :188, :300, :326; `gate_preflight.py` :3088,
:3165, :3191-3194, :3242, :4200, :4214, :6084-6093; `stand_gaps.py:1243-1249`).

**F-j1 (K2/K3, AR-22) — the road that WRITES the person's answer is not owned and not established.** The card says the driver
writes `accept always` through `stand_gaps.record_lasting`. That function is fed by the stand-gap flow: gap rows with
`scope` and `property_key` that `stand_gaps.collect` reads. Today the stand-limit card is an `add(check, PERSON_DECIDES, …)`
finding with options `a` (handed) and `b` (`manual_by_agent`) (`_stand_limit_card` :3242-3268). It is not a gap row. So
whether a person's `accept always` on the new card ever reaches `record_lasting` depends on code the card does not own:
`stand_gaps.collect` and the answer executor that calls `record_lasting`, plus the answer vocabulary for the stand-gap
words. The owner's word makes persistence the point ("A node that asks and does not persist the answer is incomplete").
Replacement for the owns bullet "the question vocabulary carrier if the new card needs a new kind":
> - `ai-packages/qa-factory/scripts/stand_gaps.py` (`collect` and the function that calls `record_lasting`, so a
>   `stand_limit` gap row is collected and its `accept always` recorded) and the answer-vocabulary row that offers
>   `accept always` on a stand-gap card (`references/question-vocabulary.json` `stand_gap_words`); the new card is a GAP
>   ROW of the stand-gap flow (`scope: "stand_limit"`, `property_key` from `lasting`), not a `PERSON_DECIDES` finding;
>   test: one row in `test_environment_record.py` or the stand-gap test that drives answer -> `record_lasting` -> a
>   record row under the stand_limit key -> the next rehearsal covers it (the AR-22 round trip).
> - `ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json` (S-e).

**F-j2 (K4, FR-4).** The `waiver` block text `e2e stand limit: <profile>` keeps passing the card (`add()`'s own rule, comment
:3256-3258). If the card becomes a gap row, that existing word must still pass it. Add an edge:
> E9 (temporal, FR-4): a waiver already recorded for `e2e stand limit: <profile>` still passes the new card. INVARIANT: an
> informed word recorded before the change is never re-asked.

## C3-k — fit_with_fixes

Correctly marked designer-first. Fix only the queue: replace "(after F-D1 / C3-0)" with "(after C3-0 under F-D1 (b))". The
gate_preflight queue now reads C3-j -> C3-k -> C3-h (F-i2).

---

## S9 — unfit (designer)

**F-9-1 (K3) — there is no plan.** The card says "the spec's S9 stands as written", and the parent S9 ends "Design detail is
the plan's (Lead or designer), not drafted here" (parent :394). No function body, no expected outputs, no test row with a
source. A builder would have to «придумать подход».

**F-9-2 (K2/K5) — premise (а) is still unmeasured**, although the card orders it first. Measuring it needs a fixture story
with a `review` gap and an S5 word. Neither recorded fixture was checked for one here: that is the designer's first step,
named in the card.

**F-9-3 (K2/K4, FR-35, AR-27) — what the pass does to delivery is undecided.** After the window reads the word, the ledger
still sees `critic_verdict` missing: `review_skipped` (ledger.py :1185) -> `review_gap` -> verdict `no`, owner `review`
(`delivery-verdict-kinds.json:35,100`). There are two honest readings:
(i) the word passes the S5 step, never the fact, as the precedent `word_passed:then_unbound` -> `chain_broken` (`no`)
does, and delivery still says `no` with the person's words shown;
(ii) a new ledger state "review passed by the person's word" with its own kind (`after_checks` or `none`).
This decides whether FR-57's door actually lets the story through, so it is the Lead's call (or the owner's). The card
must carry it.

**F-9-4 (K2) — the reused matcher does the opposite of the required error direction on `*`.** The card lists "`*` where the
block names the review gap of a different instance" as must-stay-unread. `waiver.split_overridden` treats `*` as matching
everything (`_unread_words` docstring :1748-1752: "`*` matches everything"). Reusing it in the gate role without a wrapper
reads `*` for every review gap. The design must say: for a `review` gap only a word that names the instance id (whole
words, `contract.names_whole`) is read, `*` is not; or the owner accepts `*`.

**F-9-5 (K1).** `controller.py:7425 _s5_word_index` is now :7421, and `:7444 _s5_gap_problems` is now :7440. The
`window_record.py` lines (1741, 1745, 1766, 1891) hold.

**F-9-6 (K8) — siblings.** Axis 26 (`waiver.split_overridden` is the ONE reader of a person's word on a block): the new
reader must go through it, or through a wrapper registered on that axis. Axis 32 (census): a gate read added in
`window_record` / `controller` gets its row (intent / xref). Axis 34 (one road): the road for "a person's word passes a
window gap" is `WORD_READ_KINDS` plus `probe_gap_named`; a review gap must join that road, not get a third one.
Replacement for the card's first paragraph:
> Designer first (not a builder card). The draft settles, in order: (а) the premise measured on a fixture story (named),
> result in the draft; (б) F-9-3, the delivery effect, as a fork with a recommendation; (в) F-9-4, the matcher: only a
> word naming the instance passes a `review` gap, `*` does not, through a wrapper over `split_overridden` (axis 26);
> (г) the recorded pass (`design/state-exits.md` row, AR-25) and the census rows (axis 32). Then plan critic, then builder.
> Queue: `S9 -> C3-d` (window_record), `S9 -> FL4` (controller.py).

## FL2 — unfit (designer)

**F-L2-1 (K1) — the writer the card names does not exist in that form.** "the run-row writer that carries the closed
skip-reason word". On origin/main, `skipped:<reason>` comes from the S3 PLAN row: `disposition: skip` with a free `reason`
(`ledger.py:763-773`, `return (f"skipped:{reason or 'no reason given'}", "")`). That is read through the prefix row
`"skipped": "planned_skip"` (`delivery-verdict-kinds.json:95`). The run-row form `skipped:marked skipped in the run`
(`ledger.py:1238`) maps to `decided_elsewhere`.

**F-L2-2 (K2) — premise measured here.** Over the plan rows of the recorded stories: 96 automate, 58 gap, 3 skip, 5
unverifiable. One skip row in `local-1-0108/work/test-plan.json` reads "the owner's answer leaves no implemented quick-view
add path to verify inside add-to-cart scope". That is exactly R3's class, and today it reads `planned_skip` (`none`).

**F-L2-3 (K4/K7, P31, rule 19) — a second road for a fact that already has one.** "The product does not carry this yet" has
a typed road today: `unresolved: [{case, reason: "pending_implementation"}]` in the automation manifest (ledger.py
:731-732) and the grounding write for an unimplemented requirement (debt row FR-21). Both map to kind
`pending_implementation` (`no`, owner product). A new skip-reason word on plan rows mapped to the same kind is a second road
for one action. It is legitimate only if the strategist at S3 cannot use the existing road, which may well be true (the
plan is written before S5's manifest). The card does not weigh this. Replacement for FL2's body:
> Designer first. The writer is the S3 strategist's plan row (`disposition: skip`, `reason`), read at `ledger.py:763-773`.
> The draft answers, before any word is added: (1) why the existing `pending_implementation` road (manifest `unresolved`,
> grounding) cannot carry an S3 skip — or routes the strategist to it (P31); (2) if a new closed word is needed, its field
> on the plan row (a closed `skip_class`, never parsed from `reason`, FR-12), its producer (strategist charter + plan
> contract), and the kinds-file row `skipped:<word>` -> `pending_implementation` (the lookup is by colon prefix,
> `delivery_verdict._lookup`); (3) the measured case `local-1-0108` (one row) as the scenario world; (4) the readers that
> must agree (`check_traceability`, `test_s1_s2_contract.py` G1-10 by reading). Queue: after C3-R (which pins the
> unknown-kind branch the new word passes through).

## FL4 — unfit (designer)

**F-L4-1 (K1).** `ANSWER_REWORK_OWNERS` is at `controller.py:9387` (card :9391) and `--cases` at :9904 (card :9908). The
refusal the debt row quotes is at :3783-3789. Its comment says the driver's roads never reach it ("`no_move.check_args` and
`answer_pairs_owed` stop an empty S4+ list first").

**F-L4-2 (K3) — a pointer, not a plan.** "a typed candidate argument in place of `--cases` for that route" leaves undecided:
what the S7 analyst's scope becomes for a K-n with no case; how its triage row is keyed so that S8's reporter and the
ledger accept it (today `bug_candidate_record` has `"case": ""`, `check_delivery.py:2363-2367`); whether `--candidate`
belongs to `rework` or to `stage-scope`; the `controller-blocks.md` rows that change; and which of `no_move.check_args` /
`answer_pairs_owed` must let it through. The FR-22 live proof goes to `live-runs`.
Replacement for FL4's body:
> Designer first, then plan critic. The draft names: the route (`--operation rework --candidate <K-n>` for S7 only), the
> refusal changes at `controller.py:3779-3789` and in the driver's pre-checks (`no_move.check_args`, `answer_pairs_owed`)
> with the invariant that an empty S4+ case list without a candidate is still refused; the triage row key for a
> case-less candidate and its readers (S8 reporter, ledger, `check_delivery.grounding_records`); the `controller-blocks.md`
> regeneration; one test row per refusal branch (canon). Axis 5 (stage twins: the S3/S4 rework owners in
> `ANSWER_REWORK_OWNERS`). Queue: `S9 -> FL4` (controller.py).

---

## K6 — collisions and order

- `references/gate-registry.json`: every C3 card; F-K7 makes wave 2 one writer.
- `scripts/tests/fixtures/judgment-census.json`: touched by `wave-a/integrate` (unmerged). C3-j, C3-b1, S9 and any
  code-moving card come after that merge (S-e).
- `s5_precheck.py`: `wave-a/integrate` changes it (not `run`). C3-c moves no code, so it runs in parallel. FL9's line
  `:1654` will drift by about +19 after the merge (out of this review's cards; noted for the Lead).
- `gate_preflight.py` (HOT): C3-j -> C3-k -> C3-h. C3-i leaves the queue (no code, F-i2).
- `window_record.py`: S9 -> C3-d. `controller.py` (HOT): S9 -> FL4. Both are designer-first, so nothing collides tonight.
- `delivery-verdict-kinds.json`: FL2 only (C3-e moves no code).
- `pile/live-run-fvf/batch-3` (dry story: `dry_*.py`, fixtures, `slow_tests.json`, `test-layers.json`, `selftest.py`,
  `scenario_walk.py`, `test_form_selftest.py`): no card touches these. C3-R adds rows to existing keep files only, with no
  new test file, so `test-layers.json` is untouched.
- Taken batches (§4): the Lead decision (dev1's batches do not hold each other) stands; no new hit beyond §4's list.
- Parallel now: C3-R alongside the six designer drafts. Afterwards: C3-0 -> {C3-b2, C3-g, C3-k}; C3-b1 after its draft;
  C3-j after the wave-a merge; C3-d after S9.

## K8 — class completeness (SIBLING_MAP)

- axis 4 (rules <-> debt <-> backlog): the debt rows move at S1b and B-nnn close via `piles.py close --id`. Stated for
  C3-a only. Applied to every C3 card by F-S-c's S-d, and the C3-R report lists the seven B-ids (B-278, B-221, B-061,
  B-255 (env prep only; provenance keeps B-255 open, so S1b must not close it), B-280, B-283 x2).
- axis 7 (per-test identity): C3-b2 `same_test` -> produce keeps the identity rules in one predicate. Covered by F-S5.
- axis 25 (freshness predicates): C3-d's fork touches `run_freshness_of` lines. Named in F-d1.
- axis 26: S9 (F-9-6). axis 32: S-e (F-S4). axis 34: FL2 (F-L2-3), S9 (F-9-6). axis 5: FL4 (F-L4-2).
- B-255 is shared by `provenance_acceptance` and `environment_preparation`. Converting the latter must not close B-255 in
  the backlog; this goes into C3-f's report line.

## Standing questions (critic rules 18-20)

- DUPLICATION AND CONSISTENCY (q6): found. New S-b rows for C3-c and C3-e would duplicate the K-C4 and
  `test_third_verdict.py:190` pins (F-c1, F-e1). Five near-identical registry nodes (F-K7). Grepped: the pins of each
  unknown branch over `scripts/tests/`, with controls.
- CODE QUALITY (q7): not applicable to a plan beyond K3. The plan's open "return a question" clauses (S-c, C3-f/g test
  status, C3-i item 1) are fixed by F-S1, F-f1 and F-i1.
- ONE ACTION, ONE ROAD (q12, P31): FL2 opens a second road for "the product lacks it" (F-L2-3, a fix of this round:
  designer weighs it). S9 must join the word-reading road (F-9-6). No exclusion of a language, project or case found in the
  C3 cards. Grepped: the cards' text for language names and for "only for".
- TESTS (q5, `docs/TESTING.md`): each pin row is checked against existing pins above. The C3-a world comes from a
  quarantined file and is moved into keep (F-a1). No new test file in any card.

## Trail

Read (origin/main `a372b01a` via `git archive`): `references/gate-registry.json` (header, the 14 debt rows and the 13
converted rows, dumped by script); `scripts/gate_registry.py` (:30-70, :485-684, :800-912, `--help` flags :942-944);
`proof_level.py` (:393-500, :850-880); `window_record.py` (:1700-1900); `controller.py` (:3760-3800, :7405-7500, grep
:9387, :9904); `delivery_verdict.py` (:46-47, :119-150); `check_delivery.py` (:1740-1760, :2615-2682, grep
bug_candidate); `delivery-verdict-kinds.json` (whole note, :18-48, :85-137); `ledger.py` (:700-775, :1200-1240, greps);
`s5_precheck.py` (:1654-1675, :4598-4625, greps `unchecked`); `environment_preparation.py` (:44-60, :113-135, :430-470,
:606-620); `baseline_contract.py` (:175-190); `gate_preflight.py` (:3165-3200, :3242-3275, :4200-4250, :6080-6096);
`stand_gaps.py` (:756-802 grep, :962-975, :1225-1262); `environment_record.py` (greps scope/LEVEL/CASE); `manifest_put.py`
(:138-150, greps novelty); `run_suite.py` (:30-45, greps); `driver_gates.py` (def line). Tests by grep:
`test_s5_precheck.py:843-854`, `test_third_verdict.py:190`, `test_node_ids.py`, `test_run_suite_mine.py:1704-1746`,
`test_environment_preparation.py:81,133`, `test_environment_record.py:3-5,113`, `test_gate_preflight.py`. Also
`slow_tests.json`, `tests/test-layers.json` (`keep` / `quarantine`), `plans/builder-rules.md:99`,
`docs/SIBLING_MAP.md` (headings, axes 26, 32, 34), the parent spec (:379-396, :533-563, :614-660), the wave 1 review
(head), `tools/critic_verdict.schema.json`; `git diff --stat` and hunk headers of `wave-a/integrate` and
`pile/live-run-fvf/batch-3` against their merge base with origin/main.

Runs (verbatim tails):
- `python -B <tree>/scripts/gate_registry.py --check` -> `A26 gate registry: no violations` … `14 gate(s) left as debt:` …
  `exit 0`.
- `gate_registry.py --sites` filtered to the cards' files: comparisons listed only for `check_delivery.assess` (:2626-2679),
  `delivery_verdict.decide` (:127, :143), `environment_preparation._facts` (:51), `_run_step` (:388),
  `proof_level.novelty_of` (:417-424), `already_probed` (:1520), `gate_preflight` `_derive_probe`/`named_container_said`/
  `_check_one_precondition`/`_sort_items`/`_case_question`/`_observed_identity`. None for `run_suite`, `s5_precheck.run`,
  `proof_required`, `same_test`, `_rehearse_reporter`, `check_s5_stand_limits`, `gate_b_split`, `hand_to_conductor`.
- novelty probe (script over `fixtures/stories/*/work/automation-manifest.json`): `cart-1 … 18 {'None': 18}
  {('None', True, ''): 18}`; `local-1-0108 … 34 {'None': 34} {('None', True, ''): 34}`.
- plan dispositions over `fixtures/stories`: `96 automate, 58 gap, 3 skip, 5 unverifiable`. The skip/unverifiable reasons
  listed; local-1-0108 skip "the owner's answer leaves no implemented quick-view add path…".
- test status: `test_environment_preparation/test_baseline_contract/test_environment_record` keep-fast;
  `test_node_ids/test_proof_level/test_s5_precheck/test_window_record/test_check_delivery/test_stand_identity/
  test_gate_preflight/test_execution_request/test_gate_registry/test_probe_gap_word/test_third_verdict` SLOW;
  `test_run_suite_mine/test_run_budget/test_grounding_schema/test_judge_results` QUARANTINED (positive control).
- Negative greps with positive controls of the same shape: `VERDICT_KINDS_UNREADABLE` in `scripts/tests/` 0 (control
  `VERDICT_KIND_UNKNOWN` 2 files); `node_id_mismatch` case-insensitive in `scripts/tests/` hits only 4 files, none
  test_node_ids (control `verify_node_ids` hits); `command_changed` in `test_gate_preflight.py` 0 (control `uncheckable` 5).

Not done: S9's premise run (needs a fixture with a review gap and a word: the designer's step); C3-i's rehearsal words
read in `onboarding_probe.earlier_proof` (the card fix says "read against the code"); whether `environment_record.load`
refuses a third scope (C3-j E6 keeps its return-a-question clause). Budget held, and all cards were reviewed.

```json
{
  "verdict": "blocker",
  "blockers": [
    "C3-0 is written for F-D1 (a) and §3 says 'C3-0 (if F-D1 (a))', but the Lead took (b), which still requires the predicate for test_identity, baseline_identity and provenance (gate_registry.py:837-841 F-b); its signature acceptable(record, consumer) does not fit test_identity (field null, accepts empty)",
    "C3-b conflates stored novelty unknown (already demands a probe, proof_level.py:467) with an absent key (legacy, not required): applied as written it relaxes a block; the critic's answer carrier is unnamed; closed_by lacks role+person; premise measured: 0 of 52 recorded rows would be asked",
    "C3-d S-b is red by design: window_record.verdict says an unmeasured detector is INFO, not a gap (:1831-1837, :1785-1797); making it a gap is an unnamed meaning change",
    "C3-g depends on the unbuilt predicate; deployment_readiness never refuses (docstring :175-182) and the refusing function is not named",
    "S9 has no plan; its delivery effect (review_skipped -> review_gap -> no) is undecided; the reused split_overridden reads '*' as everything, against the card's required direction",
    "FL2 names a run-row writer that does not carry the skip (the writer is the S3 plan row, ledger.py:763-773) and does not weigh the existing pending_implementation road (P31)",
    "FL4 is a pointer to a schema change with no route, keys, readers or tests"
  ],
  "fixes": [
    "F-S1: replace S-c's last sentence: words = the outcome words the row's code writes, never empty (_check_row refuses empty words on a non-exempt row); per-card words given",
    "F-S2: DoD: --check exit 0 and the row id absent from the 'N gate(s) left as debt:' block",
    "F-S3: §0.1 _scan_tree -> _walk (gate_registry.py:235-237)",
    "F-S4: new shared item S-e: a code-moving card owns its judgment-census.json rows and starts after wave-a/integrate lands",
    "F-S5: add the E-c re-role table; true accept sites under (b) are only test_identity x3, baseline_identity, provenance",
    "F-K7: wave 2 = one registry node C3-R (C3-a, C3-c, C3-e, C3-f, C3-i) plus designer drafts for C3-0, C3-b, C3-d, S9, FL2, FL4",
    "F-0-1/F-0-2: C3-0 rewritten for F-D1 (b) with the word-or-record call shape, designer first",
    "F-a1/F-a2: C3-a pin row ports M-B3's world from quarantined test_run_suite_mine into test_node_ids; words node_id_mismatch/not_verified",
    "F-b1..F-b5: C3-b split into b1 live_check_demand (designer: absent key only, carrier, E3 observable, closed_by) and b2 test_identity after C3-0",
    "F-c1/F-c2: C3-c no code and no new row (K-C4 pins it); run -> validate; drop the FL9 queue",
    "F-d1: C3-d designer fork: correct decides to INFO (rec) or make unmeasured detectors gaps (meaning change, measure first)",
    "F-e1/F-e2: C3-e test -> test_third_verdict.py, one new row for the unreadable kinds file; three sites -> produce; door is the factory's (FR-3)",
    "F-f1/F-f2: C3-f tests are keep-fast; registry branch -> refuse_with_door matching the code's blocked refusal, pinned by test_unknown_compatibility_never_selects_rebuild (Lead confirms)",
    "F-g1: C3-g to wave 3 after C3-0, refusing function named by the designer",
    "C3-h: vocabulary code, words unchanged",
    "F-i1/F-i2: C3-i registrations decided (_environment_cover + gate_b_split validate, _rehearse_reporter validate under one row, hand_to_conductor dispatch), existing pins named, one new rehearsal row only if absent; C3-i leaves the gate_preflight queue",
    "F-j1/F-j2: C3-j owns stand_gaps.py collect/record path and the stand-gap answer vocabulary, the card becomes a gap row, AR-22 round-trip test; E9 keeps an old waiver passing",
    "C3-k: queue text after C3-0 under (b); gate_preflight queue C3-j -> C3-k -> C3-h",
    "F-9-1..F-9-6: S9 designer-first with premise, delivery-effect fork, instance-only matcher over split_overridden, state-exits and census rows; controller lines 7421/7440",
    "F-L2-1..F-L2-3: FL2 designer-first: writer is the S3 plan row, weigh pending_implementation road (P31), measured world local-1-0108",
    "F-L4-1/F-L4-2: FL4 designer-first with route, refusal invariant, triage key, readers, tests; controller lines 9387/9904/3783"
  ],
  "class_completeness": "Walked SIBLING_MAP axes 4, 5, 7, 25, 26, 32, 34: axis 32 (census) uncovered by every code-moving card -> S-e; axis 26/34 uncovered by S9 -> F-9-6; axis 34 by FL2 -> F-L2-3; axis 5 by FL4 -> F-L4-2; axis 4 B-255 shared by two rows -> must not close at C3-f. Sweep of the C3 artifact: every sub-card checked against the shared items; the S-c question-return clause fired on a, c, i, j and is replaced.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md",
      "docs/tasks/specs/20261117-rules-debt-fix-spec.md:379-396,533-563,614-660",
      "docs/tasks/specs/reviews/t-968-rules-debt-phase2-wave1.md (head)",
      "origin/main ai-packages/qa-factory/references/gate-registry.json",
      "origin/main ai-packages/qa-factory/scripts/gate_registry.py",
      "origin/main ai-packages/qa-factory/scripts/proof_level.py",
      "origin/main ai-packages/qa-factory/scripts/window_record.py",
      "origin/main ai-packages/qa-factory/scripts/controller.py",
      "origin/main ai-packages/qa-factory/scripts/delivery_verdict.py",
      "origin/main ai-packages/qa-factory/scripts/check_delivery.py",
      "origin/main ai-packages/qa-factory/references/delivery-verdict-kinds.json",
      "origin/main ai-packages/qa-factory/scripts/ledger.py",
      "origin/main ai-packages/qa-factory/scripts/s5_precheck.py",
      "origin/main ai-packages/qa-factory/scripts/environment_preparation.py",
      "origin/main ai-packages/qa-factory/scripts/baseline_contract.py",
      "origin/main ai-packages/qa-factory/scripts/gate_preflight.py",
      "origin/main ai-packages/qa-factory/scripts/stand_gaps.py",
      "origin/main ai-packages/qa-factory/scripts/environment_record.py",
      "origin/main ai-packages/qa-factory/scripts/manifest_put.py",
      "origin/main ai-packages/qa-factory/scripts/run_suite.py",
      "origin/main ai-packages/qa-factory/scripts/slow_tests.json",
      "origin/main ai-packages/qa-factory/scripts/tests/test-layers.json",
      "docs/SIBLING_MAP.md axes 26, 32, 34",
      "plans/builder-rules.md:99",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "python -B <origin/main tree>/scripts/gate_registry.py --check", "result": "A26 gate registry: no violations; 14 gate(s) left as debt; exit 0"},
      {"command": "python -B <origin/main tree>/scripts/gate_registry.py --sites (filtered to the cards' files)", "result": "no comparisons at run_suite, s5_precheck.run, proof_required, same_test, _rehearse_reporter, check_s5_stand_limits, gate_b_split, hand_to_conductor"},
      {"command": "novelty probe over fixtures/stories/*/work/automation-manifest.json", "result": "cart-1 18 rows all key-absent and required; local-1-0108 34 rows all key-absent and required"},
      {"command": "plan dispositions over fixtures/stories/*/work/test-plan.json", "result": "96 automate, 58 gap, 3 skip, 5 unverifiable; local-1-0108 skip row is the R3 class"},
      {"command": "grep VERDICT_KINDS_UNREADABLE scripts/tests (control VERDICT_KIND_UNKNOWN)", "result": "0 hits (control 2 files)"}
    ]
  }
}
```

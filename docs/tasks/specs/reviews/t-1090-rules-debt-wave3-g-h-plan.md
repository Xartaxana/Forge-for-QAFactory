# t-1090 — plan critic: rules-debt wave 3 cards C3-g (baseline_identity) and C3-h (stand_identity)

Plan under review: `docs/tasks/specs/20261117-rules-debt-wave3-g-h-cards.md` (t-1085), §0-§8 and «Lead decisions on the
forks». Parent: `docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md` (S-a..S-f :278-346, E-c table, the C3-g/C3-h
sketches :1256-1283, C3-reg-precondition :1164-1254). Tree: root checkout, HEAD `c0022c96`. Read-only on code; the only
write is this file. Every control run below is a deterministic call on the live tree or on an in-memory registry copy.

## Verdict per card

- **C3-g — dispatchable with fixes** (2 must-fix before dispatch: G1, G2; 5 more fixes of the same round).
- **C3-h — dispatchable with fixes** (2 must-fix before dispatch: H1, H2; 3 more fixes of the same round).

Neither card is unfit: the core premise of each is right and was reproduced (C3-g: the predicate equals today's literal on
every producer word, D13 +1/+1; C3-h: no accept site, H-1 (a) holds, and holds on a stronger trail than the card's).

## Facts checked by trail (reproduced, not taken from the plan)

| plan claim | my check | result |
|---|---|---|
| `gate_template` :31, :46-57, :60-96; dict word via `row["field"]`, exact str member, never raises | read whole file | holds |
| `validate_baseline_request` :8-30, refusal :21-23; callers `build_baseline_fields` :50-52, `baseline_receipt` :114-116, `validate_request` :124-125 / :375-378, `validate_baseline_record` :673, `write_baseline_receipt` :713-715 | read `baseline_contract.py` whole, `execution_request.py:115-182, 370-380`, `manual_evidence.py:650-745` | holds |
| two producers of `status`: `baseline_receipt:134`, `manual_evidence.write_baseline_receipt:718` (shape-checked at :668) | read; grep of `work/baseline-receipts` writers over `scripts/*.py` (baseline_contract.py:159, manual_evidence.py:730; readers controller.py:2256, delivery_summary.py:156; stand_identity.py:218 is a protected-folder list) | holds: two writers, two readers, both readers feed only `deployment_readiness` |
| one reader of the word (E12) | grep `["']captured["']\|["']inconclusive["']` over `scripts/*.py`: the only `captured` comparisons are :134 (producer IfExp) and :199; every `inconclusive` hit is another vocabulary (check_delivery, coverage_contract, judge_run, ledger ...) | holds |
| G-0: `provenance.baseline` read by no script | own grep, case-insensitive, `provenance\.baseline` over the whole package: registry :349 + `test_gate_registry.py:293,295,297,639,648` only; positive control same call shape `provenance\.environment_preparation`: 4 hits | holds (negative reproduced) |
| predicate after the change == today's literal on every word | **run** (scratchpad `d13.py`): `acceptable(r, "baseline_identity.readiness", registry=<copy with item 1's row>)` vs `r.get("status") == "captured"` over `captured, inconclusive, Captured, " captured", "", None, 5, ["captured"], "matched", <no key>` | 10/10 equal (True only on `captured`); `{"rows":"x"}` registry -> False, `registry_problem` = "it carries no `rows` list" |
| D13: G-1 (a) gives +1 triple / +1 item (`manual_evidence.py:728`), `baseline_receipt` 0, `deployment_readiness` 0 after | **run**: `GR.analyse` live = 145 items / 49 triples / 0 findings; copy with item 1's row (code unchanged) = 147 / 51, the two new items are `baseline_contract.py:199` (the literal the code change removes) and `manual_evidence.py:728`; `baseline_receipt` contributes none | holds: after the code edit 146 / 50, exactly the card's delta |
| behaviour-preservation control can fail | **run**: the same copy with `status: converted` and the code NOT edited -> 2 findings (F-b "calls no acceptable()", F-a on :199) | the `--check` DoD turns red if the literal stays; item 4's `captured` row turns red on a consumer-id typo (E3); its registry rows are red today (today's code counts the receipt) |
| K-N2.12 NEG / F1 after the move: exactly one finding naming consumer, word, row | **run**: `person_confirmed` appended to `baseline_identity.readiness` on the copy -> one new finding `baseline_identity.promotable: is false, yet baseline_identity.readiness accepts person_confirmed ...` | holds (the prefix rule `gate_registry.py:735-745` is skipped for `prefix == row id`, so not two) |
| `--sites` has no `baseline_contract.py` line today | **run** `gate_registry.py --sites` filtered | holds (none) |
| census: `deployment_readiness` has no unit | grep `judgment-census.json`: rows :42-47, 0 `deployment_readiness` | holds |
| C3-h: row :7-36, five sites, `accepts {}`; vocabulary rule :512-519 | read registry :1-60, `gate_registry.py:485-700` | holds |
| C3-h: `named_container_said` '' exactly on `result == "matched"` :4484-4485; driver registers on '' :2644-2648 | read `gate_preflight.py:4465-4500`, `driver_machine.py:2600-2660`, `driver_gates.py:630-662`, `runtime_probe.py:1505-1555` | holds; see H-1 below |
| C3-h: F4 flip control copies `rows[0]` and overrides the keys it needs | read `test_gate_registry.py:736-772` | holds |
| Lead line E4 of C3-h: push run 44052586866 is green, so no stand-identity pin is red | **run** `ci_read.py jobs 44052586866` | **does not hold as a witness**: its jobs are `changes`, `forge-check`, `runner-facts` success and `package-fast` **skipped**; no package-full job. See H2 |

## C3-g findings

**G1 (must-fix) — owns incomplete for the two findings the Lead decided the builder files (G-2 (a), G-3 (a)).**
Plan «Lead decisions» :538-541 say "filed by the C3-g builder with its row"; the C3-g `owns:` (:142-146) lists only the
registry, `baseline_contract.py`, the two test files. Writing `plans/piles/rules-debt/findings/<file>.md` (×2), the row in a
batch file and the README «Содержание» row (PROJECT.md «Бэклог и находки», «Командная работа» п. 2) is outside owns, so the
builder must either break the manifest or skip the findings. Fix: add to `owns:` the absolute paths
`C:/QAFactory/forge-repo/plans/piles/rules-debt/findings/` (two named new files),
`C:/QAFactory/forge-repo/plans/piles/rules-debt/batch-1-phase-2.md` (one row each, or the batch the Lead names — the pile has
only `batch-1-phase-2.md`, header "статус: ожидает, взял: —" while its nodes are in work; the Lead names the target batch)
and `C:/QAFactory/forge-repo/plans/piles/rules-debt/README.md` («Содержание» row), with the finding text given in the card
(class, FR-1/FR-2, file:line, «Решение владельца нужно: нет»). Same move: the two "noticed analogs" of the siblings line
(:162-163: `delivery_summary.py:157-160` skips an unreadable receipt and the row then says "missing" — an FR-41 shade;
`controller.deployment_inputs` :2258-2259 crashes on a non-dict receipt) are named but queued nowhere: CLAUDE.md rule 9
("silently leaving a known sibling unfixed is a violation") — either a third finding in the same owns, or a Lead line
naming where they are queued.

**G2 (must-fix) — the consumer move collides with the open fork F-k4 of the C3-j/k cards.**
`docs/tasks/specs/20261117-rules-debt-wave3-j-k-cards.md:436-451` (Fork F-k4) recommends (a) "C3-k3 owns the move ... C3-g's
card then leaves `provenance.baseline` alone" and says "The Lead tells C3-g's designer which". This plan's G-0 (a) removes
`provenance.baseline` in C3-g, which is F-k4 (b), and does not name F-k4 at all. Both worlds are survivable (k3's E-k3.5
handles both), but two Lead decisions now point opposite ways. Second half: k3's items (j-k :675-679) say "F1 :639-641: the
two ids are replaced by `baseline_identity.capture` ...", "K-N2.12 NEG :291-298 uses `baseline_identity.capture`" — applied
literally on a post-C3-g tree that rewrite deletes C3-g's `baseline_identity.readiness` pins (item 6). Fix: (i) record F-k4 =
(b) beside G-0 (a) (or flip C3-g to leave the consumer, and drop item 1's removal + the F1/K-N2.12 edits); (ii) C3-g E9 gets
the INVARIANT "after C3-k3, both `baseline_identity.readiness` (under `baseline_identity`, reader `deployment_readiness`) and
`baseline_identity.capture` (under `provenance_acceptance`, reader `validate_baseline_record`) exist with their F1 pins; k3
adds its pin beside C3-g's and never replaces it", and the same line goes into the k3 card's E-k3.5 (Lead's edit of that
spec). Verified: the two ids do not collide (`acceptable` resolves by the full consumer key, `gate_template.py:67-68`; F-f
"consumer id used by two rows" is per id, `gate_registry.py:724-727`).

**G3 — item 5's refusal table has no accepting control, so it cannot fail on a validator that refuses everything.**
Item 5 (:223-233): rows `{}`, `{expected: None}`, `{expected: ""}` and the "control" `{expected: "new"}` all expect the
refusal. Fix: add the row `{"expected_source_revision": "old"}` -> `validate_baseline_request` holds no "baseline runtime
must match ..." error and `build_baseline_fields` does not raise (the green half already in `test_baseline_contract.py:122`,
here inside the table). Also name the `row` passed to `build_baseline_fields`: the approved-row shape of
`test_baseline_contract.py:118-121` (it carries `baseline_reason`; `contract()` does not, and a weaker builder passing
`contract()` gets an extra "requires reason" error that hides nothing but muddies the expectation).

**G4 — the FR walk misses section B; the new gap reason reaches a person.**
§1 :47 lists C3-g as A/C/D/E. The gap dict travels `deployment_readiness` -> `delivery_summary.py:172-178` (`reason` kept) ->
`comparison_gaps` (:415) of the delivery summary a person reads. The item 3 sentence "the gate registry cannot be read
(<problem>): a factory defect, the baseline receipt was not judged" is text shown to a person: FR-6 (human-questions.md) and
FR-3 (a factory reason is reported, never asked) apply. Fix: add B (FR-3, FR-6) to the walk and state the sentence obeys
human-questions.md (the `<problem>` string is `load_registry`'s own short sentence, as in C3-reg-precondition item 1). Consistency
(rule 18): the family's texts differ — C3-reg-precondition uses the stable prefix "gate registry unreadable:"; the card
should align its prefix with that one (or with the C3-b2/C3-d per-site wording) rather than coin a third.

**G5 — item 3 needs the conjunct list twice; prescribe the shape so the builder does not copy it.**
Item 3's condition "at least one receipt met every conjunct except the predicate" needs the filter without the predicate,
and item 2 needs it with. A weaker builder will paste the 10-line comprehension (:189-199) twice (a clone the ratchet will
count, and two lists that can drift). Fix: prescribe `matching = [r for r in receipts if <the equalities, in order>]`,
`candidates = [r for r in matching if acceptable(r, "baseline_identity.readiness")]`, and the reason test reads `matching`.
That keeps E4 (predicate last, hashes after) and gives item 3 its set for free. Also settle the wording gap between item 3
("met every conjunct" of the comprehension — the source-revision/hash checks :201-214 are NOT part of it) and E2 ("only where a
receipt was otherwise valid"): make E2 say what item 3 says. And name the case item 3 implies but leaves silent: a broken
registry with an `inconclusive` receipt gets the registry reason (true: it was not judged), not "missing".

**G6 — E11 conflates two reads under `refuse_with_door`.**
After F-T3 (a) the row's words are the receipt's; its unknown word `inconclusive` is never refused — it takes the
non-blocking `awaiting_baseline` gap with `next_action` offering baseline sources. `refuse_with_door` describes the REQUEST
site (`validate_baseline_request`), which refuses a revision, not a row word. The parent decided "keep refuse_with_door"
(phase2 spec, decided-branches table, C3-g row), and `unknown_branch` has no runtime reader (grep `unknown_branch` over
`scripts/*.py`: only `gate_registry.py`), so no re-decision is needed — but E11's "both hold" is not true as written. Fix:
E11 says "the row's unknown word `inconclusive` takes the declared safe default — an awaiting_baseline gap, never a count
(FR-59's safe-default road); the refusal-with-door of the row is the request site's", and item 4 names its `inconclusive`
row as the S-b pin of the word's unknown. G-2's finding then records that the request site's refusal names no door, so the
row's `refuse_with_door` is held without its door until that finding's node lands.

**G7 — E2 TEMPORAL: C3-reg-precondition is not on main.** E2 leans on it ("stops the next dispatch first"); it is built and
in its fix round (dispatch statement). State both worlds: before it lands, item 3's reason is the only sign of a broken
registry on this road; after, the dispatch stops first and item 3 is belt-and-braces. No pin assumes either order.

### C3-g fork decisions judged

- **G-0 (a) — right**, with G2's coordination. `provenance.baseline` has no reader (reproduced); a consumer without its reader
  is AR-22's defect; the readiness consumer lands with its reader.
- **G-1 (a) — right.** Measured: +1 item (`manual_evidence.py:728`) / +1 triple; `baseline_receipt` adds 0 (its IfExp is a
  dict value, not a Compare operand). The F-f double-registration rule (`gate_registry.py:829-834`) is why `:668`
  stays out — correct.
- **G-2 (a) — acceptable.** FR-1 at a site the row registers, but not one the card owns; the door must be a command in the
  refused party's set (FR-2), which needs a read of who builds a baseline request — outside a conversion. Condition: G1's
  owns, and G6's line that the row's door is the finding's residue.
- **G-3 (a) — right.** Verified: `baseline_contract.py:14` and `:21` call `.get` on `x or {}`; in `validate_request` the call
  :124-125 precedes the dict check :150-153. A truthy non-dict raises `AttributeError` — a stop, never a pass; the missing
  field name is FR-1 hardening of outside input, a finding.

## C3-h findings

**H1 (must-fix) — E1 states the unknown branch wrongly, against a pinned test.**
E1 (:415-416): "(empty / absent / unreadable build): `unknown` -> the question at stage entry, the stage waits ... INVARIANT: a
stand whose build is not established never runs S5 on a guess". At stage entry only an unknown whose record carries
`asks_person` (`how`/`confirm`) raises the question (`driver_stage_build.py:401-412`); an unknown with nobody to ask is a
printed line "I could not read which build ... This is not a question for you" and the stage GOES ON
(`driver_stage_build.py:413-418`, `build-identity-methods.json:265`; `build_check` docstring :300-301 "a doubt is a line, never
a question and never a silent pass - the run path still refuses a build nobody could prove"). Pinned:
`test_story_run_stand_identity.py:1008-1023` (K39 "docker down (unknown, nobody to ask)": "no question (exit 0), the role
starts"); and the card's own cited pin `test_stand_identity.py:887-896` says "unknown, **no question**". So E1 contradicts its
own pin. Fix: split E1 — (i) askable unknown -> question at stage entry, wait (K36 :449-450, K35); (ii) unknown with nobody
to ask -> one line, the role starts, and the run is refused at launch by the provenance predicate
(`execution_request.validate_request:175-179`); INVARIANT: no run on an unproven build (the launch refuses), not "S5 never
starts". Add K39 to §3's pins, and have the builder name a launch-refusal pin of an `unknown` record (candidates to re-grep
in `test_execution_request.py`: :558, :589, :930 — I did not read their assertions). State in the card that the row's
`question / wait / stage_entry` covers the askable unknown and the unaskable one takes the declared safe default (FR-59) —
the same honesty point as G6; no change of the decided branch.

**H2 (must-fix) — the Lead's E4 witness does not witness the stand-identity files.**
«Lead decisions» :543-544: run 44052586866 green -> "no stand-identity pin is red on main". `ci_read.py jobs 44052586866`:
`package-fast skipped`, no `package-full`. Neither `test_stand_identity.py` nor `test_story_run_stand_identity.py` ran.
The latest nightly 44048500307 (9344a58c) is `failure` (package-full (2) failed; its log lists
`test_story_run_stand_identity.py 247.1s` among the slowest with no FAIL line matched by my grep — the cause of the failure
is not established by me). Fix: re-take E4 on a run where package-full ran on a tree containing C3-0/C3-rr/C3-b1 (e.g. the
canon runs 44059241756 / 44059237092 at c0022c96, in progress when read), quoting the two files' lines; until then E4's
gate is open, not passed.

**H3 — the pin count.** Item 2 (:389) "quotes the eight pins of §3 facts"; §3 enumerates ten (probe level 7: :818-820,
:833-837, :840-843, :887-896, :932-939, :941-944, :957-960; stage level 3: :449-450, :481-498, :583-597), and H1 adds K39.
Fix: enumerate them as a numbered list in item 2 and drop the count word.

**H4 — §3 fact ":771" is a test seed, not producer output.** `test_stand_identity.py:771` is the input record the `probe`
helper seeds; the claim "the record's `result` carries these words" is true, but its carrier is
`runtime_probe.finish/finish_unknown` (:1272-1290) and `conclude` (:1043-1055). Cite those.

**H5 — H-1's trail: record the decisive evidence in the card** (see the judgment below), so the next reader does not have to
redo it.

### H-1 judged — (a) keep `dispatch` is right

`named_container_said` returns '' exactly on `result == "matched"` (`gate_preflight.py:4484-4485`), and on '' the driver runs
`probe_move` (`driver_machine.py:2644-2648`) = `runtime_probe --suggest --write` (`driver_gates.py:630-636`). What that
writes: one config entry `execution.runtime_probes.<profile>` — a probe COMMAND, no verdict, no evidence
(`runtime_probe.py:1510-1518`); its verification run is a rehearsal that writes nothing ("ALWAYS a rehearsal (S14)",
:1524-1527; "the story's first run checks the stand"). The driver's own comment says so: "No waiver is recorded (nothing is
passed: the next rehearsal proves the stand with the registered probe's own check)" (`driver_machine.py:2630-2636`). And the
rehearsal's own registration road `_derive_probe` offers the same registration on `unknown` as well as on `matched`
(`gate_preflight.py:4587-4592` -> `_probe_unknown` -> `_probe_derived(..., write_argv)`, :4519-4523, :4317-4328): registering a
probe is not an acceptance of the stand's identity anywhere in the package. Every later consumer runs the registered
command and judges its fresh word (`build_outcome` at stage entry, `validate_request:175-179` at launch). So the '' gates a
config write that passes nothing: the E-c invariant ("a re-role never hides a literal acceptance") is not engaged, and (b)
would put a `matched` predicate in front of a non-acceptance. The card's stated ground (launch re-probe only) is true but
weaker; H5 asks to record the trail above. Noticed analog (not this card's, reported): the two registration roads differ
on `unknown` — the rehearsal registers on `matched` and `unknown`, the named-container road only on `matched`
(`driver_machine.py:2631-2633`). Whether that is one action on two roads (P31) is a question for the Lead; it is not a
validity gate.

"No accept site" for every site of the row: `runtime_probe.conclude` / `finish` write the word (and `finish` writes a
discovered method row on matched/mismatched, :1282-1285 — a config write too); `_derive_probe` routes the five words into
helpers that register or card; `build_outcome` turns every word into a line or a question — `matched` and the nobody-to-ask
`unknown` both let the stage go on, so the stage entry never takes `matched` as a pass; `named_container_said` as above.
Holds.

S-b pin "question before the stage": K36 setup (`test_story_run_stand_identity.py:449`) asserts exit 3, kind
`stand_identity`, variant `how` on the real ladder — a real pin of the askable branch. It lives in `stand_check`'s `test`
file, not in the row's own `test` (`test_stand_identity.py`, which pins only the probe's `asks_person`). S-b allows a named
existing pin; the card should say in one line that the stage half is pinned in the sibling row's test file and why the row's
`test` stays (the probe is the row's producer).

## Standing questions

- **Architecture / principles (q1).** C3-g: AR-13 (one reader, `gate_template`) kept; AR-22 kept once G2 is settled; AR-28
  kept (absent/unaccepted/unreadable each a gap, pinned by item 4); AR-29 class right — a membership join of a producer's word
  to its registry row, owner data, no census unit (verified: census rows :42-47, none for `deployment_readiness`); AR-20 deltas
  named and measured; AR-19 axis-5 grep prescribed. P27: the person's word never stands in for the old build (promotable
  false, K-N2.12 NEG). FR-41/FR-59 on the unreadable branch: never a count, told as the registry's fault where a receipt was
  there (item 3), with the E3 residue named. Missing: section B (G4). C3-h: no check moves; AR-28 statement wrong (H1).
- **Edges (q4).** Limits: none introduced (both cards), right. Empty/absent/None: C3-g item 4 rows cover them; C3-h E1 wrong
  (H1). Conflicting pairs: C3-g E11 needs G6's wording. TEMPORAL: C3-g E5-E7 right; E2 both worlds missing (G7); C3-d landing
  before C3-g: no pin text in either card assumes the old order — every pin is a delta and D13 is re-measured (E7, item 6,
  C3-h E3) — holds. POSITIONAL: C3-g E4 right and G5 keeps it; C3-h E7 right.
- **Tests (q5).** C3-g: two parameterised tables in the keep, fast file `test_baseline_contract.py` (`test-layers.json:213`
  keep row), expectations from the row's `decides` — right; G3 fixes the control. C3-h: no new row, named pins — right once
  H1/H3 land. Nothing in a quarantined file. Volume: two tables in one keep file, under any budget reason (no `tests-over:`
  expected).
- **Dispatchability (q6).** File, function, expected behaviour and test are named per item in both cards; no "find an
  approach" remains except G5 (shape prescribed by the fix). Owns incomplete (G1).
- **DUPLICATION AND CONSISTENCY.** Found: G5 (the conjunct list would be duplicated), G4 (a third wording of the
  unreadable-registry text). Grepped: `captured|inconclusive` over `scripts/*.py`, `references/*.md`, `skills/`, `agents/`
  (no prose twin of the receipt words: 0 hits with baseline/receipt); `provenance\.baseline` package-wide.
- **CODE QUALITY.** Plan-level only: G5. Nothing else found in what the cards prescribe.
- **ONE ACTION, ONE ROAD (P31).** C3-g: the receipt word is read at one site through the one predicate (verified one reader).
  The per-site registry-why of item 3 sits beside C3-reg-precondition's one stop by the Lead's belt-and-braces decision; no
  exclusion of a language/project/case. C3-h: none added. Residue for the Lead (not a blocker of these cards): the two
  probe-registration roads differ on `unknown` (H-1 analog) — a proposed question for the Lead tier, not decided here.
- **Class completeness (map, rule 5).** Axis 5 (gate rows <-> sites <-> prose twins): C3-g walks it (grep prescribed; my grep
  found no twin). The second producer (`manual_evidence.write_baseline_receipt`) is registered (G-1). The shape check at
  `manual_evidence.py:668` is a `provenance_acceptance` site, named for C3-k — right. The cross-card axis (consumer pins
  shared with C3-k3) is the gap of G2.

Acceptance of these cards and of the fork decisions stays with the Lead (this verdict is an input).

## Trail

Read: the plan whole; parent spec :270-410, :1164-1290; j-k cards spec :430-455 + grep for C3-g/F-k4/provenance.baseline;
`baseline_contract.py` whole; `gate_template.py` whole; `gate-registry.json:1-60, 325-360` + grep; `gate_registry.py:1-60,
290-330, 450-475, 485-700, 724-745, 786-915`; `manual_evidence.py:650-745`; `execution_request.py:115-182, 370-380`;
`test_baseline_contract.py` whole; `test_live_audit_contract.py:38-57`; `test_gate_registry.py:55-75, 246-254, 285-300,
320-345, 630-672, 736-772, 950-962, 1000-1050`; `gate_preflight.py:4317-4339, 4465-4605`; `driver_machine.py:2600-2680`;
`driver_gates.py:630-662`; `runtime_probe.py:1036-1056, 1268-1292, 1505-1555` + grep `suggest`;
`driver_stage_build.py:210-225, 291-440`; `test_stand_identity.py:768-773, 810-965` + defs;
`test_story_run_stand_identity.py:440-500, 575-600, 997-1030` + defs; `controller.py:2248-2265`;
`delivery_summary.py:150-178` + grep; `judgment-census.json` grep; `test-layers.json` grep; `plans/piles/rules-debt/` listing,
README, batch header; `tools/critic_verdict.schema.json`.

Runs: see the json block.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "G1 C3-g owns lacks the pile files for the G-2/G-3 findings the Lead assigned to its builder (findings/*.md, batch row, README Содержание row); the two noticed analogs are queued nowhere",
    "G2 C3-g G-0 (a) removes provenance.baseline = F-k4 (b), opposite to the open F-k4 rec (a) of the j-k cards; record F-k4 and add the E9 invariant that C3-k3 keeps the baseline_identity.readiness pins",
    "H1 C3-h E1 says every unknown asks at stage entry and waits; K39 (test_story_run_stand_identity.py:1008-1023) and test_stand_identity.py:887-896 pin that an unknown with nobody to ask is a line and the role starts; the launch refuses",
    "H2 C3-h E4 witness run 44052586866 skipped package-fast and has no package-full: the stand-identity files did not run"
  ],
  "fixes": [
    "G1 add the rules-debt pile paths to C3-g owns with the finding texts; queue the delivery_summary/controller analogs",
    "G2 record F-k4 = (b) beside G-0 (a) (or flip C3-g); E9 invariant: after C3-k3 both baseline_identity.readiness and baseline_identity.capture exist with pins",
    "G3 item 5: add the accepting row expected_source_revision old (no error, no raise); name the approved-row shape of test_baseline_contract.py:118-121",
    "G4 add FR section B (FR-3, FR-6): the gap reason reaches delivery_summary comparison_gaps; align its prefix with the C3-reg-precondition text family",
    "G5 prescribe matching then candidates (one conjunct list); align E2 with item 3; name the broken-registry plus inconclusive case",
    "G6 E11: inconclusive takes the declared safe default (gap, never a count); refuse_with_door is the request site; item 4 inconclusive row is the S-b pin",
    "G7 E2 TEMPORAL: both worlds of C3-reg-precondition",
    "H1 split E1 into askable and nobody-to-ask unknowns; add K39 and a launch-refusal pin; say the stage half is pinned in stand_check test file",
    "H2 re-take E4 on a run where package-full ran (canon 44059241756 or 44059237092 at c0022c96, or a green nightly)",
    "H3 enumerate the pins in item 2 (ten plus K39), drop the word eight",
    "H4 cite runtime_probe conclude/finish for the words, not the test seed at test_stand_identity.py:771",
    "H5 record the H-1 trail: driver_machine.py:2630-2636, runtime_probe.py:1510-1527, _derive_probe registers on unknown too"
  ],
  "class_completeness": "Axis 5 walked by C3-g (prose twins: none found by grep captured|inconclusive over references/*.md, skills/, agents/ with baseline/receipt); second producer registered by G-1; the manual_evidence.py:668 shape check is named for C3-k. Gap: the cross-card consumer pins with C3-k3 (G2). C3-h changes no words, axis 5 n/a. Noticed analog for the Lead: the two probe-registration roads differ on unknown (P31 question, not decided here).",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-rules-debt-wave3-g-h-cards.md",
      "docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md:270-410,1164-1290",
      "docs/tasks/specs/20261117-rules-debt-wave3-j-k-cards.md:430-455",
      "ai-packages/qa-factory/scripts/baseline_contract.py",
      "ai-packages/qa-factory/scripts/gate_template.py",
      "ai-packages/qa-factory/scripts/gate_registry.py:1-60,290-330,450-475,485-700,724-745,786-915",
      "ai-packages/qa-factory/references/gate-registry.json:1-60,325-360",
      "ai-packages/qa-factory/scripts/manual_evidence.py:650-745",
      "ai-packages/qa-factory/scripts/execution_request.py:115-182,370-380",
      "ai-packages/qa-factory/scripts/tests/test_baseline_contract.py",
      "ai-packages/qa-factory/scripts/tests/test_gate_registry.py:55-75,246-254,285-345,630-672,736-772,950-1050",
      "ai-packages/qa-factory/scripts/gate_preflight.py:4317-4339,4465-4605",
      "ai-packages/qa-factory/scripts/driver_machine.py:2600-2680",
      "ai-packages/qa-factory/scripts/driver_gates.py:630-662",
      "ai-packages/qa-factory/scripts/runtime_probe.py:1036-1056,1268-1292,1505-1555",
      "ai-packages/qa-factory/scripts/driver_stage_build.py:210-225,291-440",
      "ai-packages/qa-factory/scripts/tests/test_stand_identity.py:768-773,810-965",
      "ai-packages/qa-factory/scripts/tests/test_story_run_stand_identity.py:440-500,575-600,997-1030",
      "ai-packages/qa-factory/scripts/controller.py:2248-2265",
      "ai-packages/qa-factory/scripts/delivery_summary.py:150-178",
      "ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json (grep)",
      "plans/piles/rules-debt/README.md, batch-1-phase-2.md header"
    ],
    "reruns": [
      {"command": "python -B ai-packages/qa-factory/scripts/gate_registry.py --sites (filtered baseline_contract, runtime_probe, driver_stage_build, gate_preflight, manual_evidence)", "result": "no baseline_contract.py line; stand_identity lines at driver_stage_build.py:379-419, gate_preflight.py:4484, 4587-4595, runtime_probe.py:1043-1284; manual_evidence.py:682,686 under provenance_acceptance"},
      {"command": "scratchpad d13.py: GR.analyse live vs in-memory copy with C3-g item 1 row (G-1 sites)", "result": "live 145 items / 49 triples / 0 findings; copy 147 / 51, new items baseline_contract.py:199 (removed by the code edit) and manual_evidence.py:728; after the edit 146 / 50 = card delta +1/+1"},
      {"command": "scratchpad d13.py: copy with status converted and code unchanged", "result": "2 findings: F-b deployment_readiness calls no acceptable(), F-a on :199 - the DoD control can fail"},
      {"command": "scratchpad d13.py: person_confirmed appended to baseline_identity.readiness", "result": "exactly one new finding naming baseline_identity.promotable, the consumer and the token"},
      {"command": "scratchpad d13.py: acceptable(r, baseline_identity.readiness, registry=copy) vs r.get(status) == captured over 10 values", "result": "10/10 equal; broken registry rows:x -> False, registry_problem 'it carries no rows list'"},
      {"command": "grep -rniE provenance\\.baseline ai-packages/qa-factory (control provenance\\.environment_preparation: 4 hits)", "result": "registry :349 and test_gate_registry.py:293,295,297,639,648 only"},
      {"command": "python -B tools/ci_read.py jobs 44052586866", "result": "changes, forge-check, runner-facts success; package-fast skipped; no package-full"},
      {"command": "python -B tools/ci_read.py pipelines --n 40 and jobs/log of nightly 44048500307", "result": "nightly failure (package-full (2), quarantine-check); test_story_run_stand_identity.py listed 247.1s, no FAIL line matched; cause not established"}
    ]
  }
}
```

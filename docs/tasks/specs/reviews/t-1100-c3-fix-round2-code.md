# t-1100 — re-review of the C3 fix round (RD1-27, RD1-30, RD1-31), diff c1b4ce7a..f1265890

Tree: `.claude/worktrees/agent-ac40b44fb0a175afa`, HEAD `f1265890`. Spec: the three finding files (their «Что именно менять») plus the Lead's dispatch choices. Earlier verdict: `docs/tasks/specs/reviews/t-1084-c3-b2-d-topic-code.md`, fixes 2, 3(d) and 5.

## Verdict

**NEEDS WORK (fit_with_fixes).** RD1-30 is accepted as is. RD1-27 works, but it ships two templates under one name: fix A. RD1-31 is correct on the paths it tests. Two defects remain: a committed dispatch loses its pass rows on the `EventCommitted` path (fix B, shown by a probe), and the dispatch branch has three more pass roads that this round did not cover (fix C). My earlier verdict's count of "five sites" was too low, and that miss is mine. Fixes D and E are small. Fix F covers the analog sites outside the dispatch branch. Every fix is "fix before merge". The decision to accept stays with the Lead.

## Findings

**B. RD1-31: a committed dispatch whose after-commit step fails keeps no pass row (fix before merge).**
- `apply` (`controller.py:5215-5253`) records `kept` only when the `try` exits normally. Two failures happen after the event is durable: `event_store.commit` raises `ProjectionStale`, or the deferred `_run_after_commit` raises `DerivedViewStale`. Both are subclasses of `EventCommitted` (StateConflict).
- In both cases control enters `except StateConflict`. There `_replayed_with_other_scope` returns None (the exception is not `IdempotencyKeyReused`), and `_revise_key_fields` returns None (the operation is not `revise_plan`). So the handler runs a bare `raise`, `finally` sets `kept = ...; None`, and `_record_person_pass` is never reached.
- A retry with the same key goes down the store's replay branch (`event_store.py:693-702`), which does not run validate. So `kept` stays `[]` and the row is lost for good.
- The Lead's invariant "a committed dispatch leaves exactly one row per passed block" is broken. The callers already treat `EventCommitted` as "the event is in" (`controller.py:8111`).
- Probe (scratchpad `probe_rd131.py`, which imports the test module's harness): the registry stop is passed by a word; then `store._run_after_commit` is patched to raise `DerivedViewStale`:
  ```
  stale=False raised=None EventCommitted=False dispatch_event_committed=True pass_rows=1
  stale=True raised=DerivedViewStale EventCommitted=True dispatch_event_committed=True pass_rows=0
  ```
- Fix: in `except StateConflict as exc:`, before any re-raise, add `if operation == "dispatch" and isinstance(exc, EventCommitted): self._record_person_pass(request.get("stage"), request.get("id"), self._dispatch_passes)`. `finally` has not run at that point, so the list is still there. Change the comment's POSITION wording from "after the commit stands" to "once the event is in".
- Test: one more row in `REG_PRECONDITION_ROWS` where the store's after-commit step raises. Expect `DerivedViewStale` and 1 row. The door is `apply`.

**C. RD1-31: the dispatch branch has more pass roads than the five that were fixed (fix before merge, same file, within owns).**
`validate`'s dispatch branch runs from `controller.py:5530` to `5832`. It also reaches `_passed_by_person` through helpers that keep only `[0]` or `blocking`:
- (c1) `_unreadable_plan_problems` (`:4282`, `return self._passed_by_person(stage, [text])[0]`). It is called at `:5656` for an S5/S6 empty scope (`S5 scope: unreadable` / `S6 half membership: unreadable`).
- (c2) The same function through `_half_membership_problems` (`:4301`), called at `:5589/:5591` for the S6 runner packet.
- (c3) `_plan_refusal` (`:6587`, `blocking, _ =`). It is reached through `_s5_plan_problems` at `:5768`, via `_before_windows` (`:6600`) and `:6643/:6662/:6683/:6719`, for the words `plan before windows`, `plan form switch` and `plan review round`.
- `refusal_registry.py:886` says the `plan before windows` pass "is recorded in `state/passed-by-person.jsonl`". That holds only for the accept-side site (`:7072-7083`), not for this dispatch-side road.
- Fix (either shape closes the class):
  - Minimal: unpack `passed` in `_unreadable_plan_problems` and `_plan_refusal`, and call `self._note_dispatch_pass(passed)`. Outside a dispatch `apply` the collector is None, so the rehearsal callers (`:2191`, `:2200`, `:3851`, `:4015`) write nothing, which is correct.
  - Preferred, one road: call `self._note_dispatch_pass(passed)` once, inside `_passed_by_person`, and delete the five per-site calls. Then any future dispatch-branch block is covered by construction. The accept-branch sites are not affected: for them the collector is None.

**A. RD1-27: `registry_why(reason, tail, *, stop=False)` is two texts in one name (fix before merge).**
- The flag picks between two complete templates. They share only `cannot be read ({reason})`, and even the subject differs ("the gate registry" vs "the plugin's references/gate-registry.json"). If one head is edited, the other does not move. So the function prevents none of the drift the finding was about (P31, AR-16).
- The pinned bytes do not force this shape. For the stop, the pins are the prefix `gate registry unreadable:` (`test_controller_state.py:2332`), the substrings "Reinstall or update the qa-factory plugin" and "nothing is wanted from you", and now "Owner: factory". Nothing pins "the plugin's references/gate-registry.json cannot be read". I grepped the package, `tools/` and `kb/`; the only hits are the gate_template docstring and the new row. The generator matches the local name `registry_blocking[0]`, not the text (`controller-blocks-gen.py:354`).
- Better shape:
  - One head, `registry_why(reason, tail) -> "the gate registry cannot be read ({reason}): a factory defect, {tail}"`.
  - A block-name constant in `gate_template` (e.g. `REGISTRY_BLOCK = "gate registry unreadable"`). Precedent: the block constant at `proof_level.py:65-67`, "one constant, so the refusal and the door cannot drift apart".
  - The stop is then `f"{REGISTRY_BLOCK}: " + registry_why(registry_reason, "<tail naming references/gate-registry.json, Owner: factory, nothing is wanted from you, Reinstall ...>")`.
- This rewords a text a person reads, so it needs its FR-6 walk. If the Lead decides the current stop wording must stay byte for byte, that decision belongs to the Lead. In that case the honest form is two named functions, not one function with a flag.

**D. Names and a test label that say more than they hold (fix before merge, trivial).**
- `proof_level.py:946-947`: `WHY_RUN_REGISTRY` / `WHY_RECEIPT_REGISTRY` are now tails, while every other `WHY_*` there is a whole sentence (`WHY_NO_RUN`, `WHY_RUN_NOT_COMPARED`). Rename them (`*_REGISTRY_TAIL`) or inline them.
- `test_gate_registry.py:1188-1199`: the comment says "the four sites take ONE builder", but the row feeds a literal tail for `execution_request` and never reaches a site. If a site went back to an inline copy, the row would stay green.
  - Change the label to what the row checks: "the builder reproduces the four texts the sites had".
  - The text actually produced at each site is still checked by the site rows: `test_run_freshness.py:124`, `test_proof_level.py:1862`, `test_execution_request.py:1626`, `test_controller_state.py:2332`.

**E. RD1-31 test gap: no row for a non-registry block passed and committed.**
- Under fix C's preferred shape there is one note inside `_passed_by_person`, so the registry rows already exercise the one road, and per-site rows would only pin wiring (TESTING.md, one parameterised test per behaviour). No extra row is needed then.
- Under the minimal shape, add one row through a helper road (c1 or c3). Otherwise a dropped `_note_dispatch_pass` line there would leave every test green.

## Analog sites (`_passed_by_person` callers outside the five; plus the two items)

| site | road | verdict |
|---|---|---|
| `:3164` `_design_review_problems` | gate A `decision` (S4 design review) | same defect: the word passes and leaves no row; there is no recording anywhere in the decision branch. Fix: open the collector for `decision` as well (`apply`: `[]` for dispatch and decision), note it, record after commit with stage S4 (fix F) |
| `:3253` `_decision_problems` (empty scope) | `decision` | same defect, same fix F |
| `:3391` `open_gate_items` (items unreadable) | `decision`. Read BEFORE the lock in `apply`'s memo pass (`:5085-5088`) and by the rehearsal | same defect. Fix F must open the collector before the memo read, or note on the memo reuse inside validate; a rehearsal stays a no-op |
| `:4282` `_unreadable_plan_problems` | dispatch branch (`:5589/:5591`, `:5656`) plus rehearsals | dispatch-branch member: fix C (c1, c2) |
| `:6003` S6 completion | accept | same defect. The S5 twin records after its raise (`:5986-5993`, FV1-30a). Fix F: record `passed` at the same position for S6 |
| `:6561` `_code_review_refusal` | accept of qa-code-critic (`:5920`) | same defect. Fix F: return `passed` and record it once the accept's refusals did not raise |
| `:6587` `_plan_refusal` | dispatch branch via `_s5_plan_problems` (`:5768`) | dispatch-branch member: fix C (c3) |
| `:7403` `_s5_v2_collect` mechanical round | S5 accept | same defect, unless `s5_precheck.word_passes` (`_record_s5_word_passes`) names this block, which I did not verify. Fix F: check that, else record at the S5 accept position |
| `tools/fixtures/dispatch_manifest/K8.txt:3` | historical dispatch text, a fixture of `dispatch_manifest` tests | not applicable: it names no caller, and editing it would rewrite a fixture's history |
| `test_proof_level.py` `proven`, `live_body` | — | not applicable: both are still used (`:1512-1526`) |

Fix F is in the same file and within the node's owns, so brief item 4 says: repaired in the round, with the Lead widening it. If the Lead keeps RD1-31 narrow, the line is `decision- and accept-branch person passes leave no row (controller.py:3164,3253,3391,6003,6561,7403) | узел: <new rules-debt node>`. The owner of that node is the Lead of rules-debt.

There is a larger sibling of the POSITION defect, a proposed node for the Lead and not a fix of this round. The accept branch records inside `validate`, BEFORE the event (`:5985`, `:6990`, `:7074`, `:7083`, `:7165`, `:7296`, `:7594`, `:7603`, `:7705`). So a later refusal in the same validate leaves a row for an accept that never committed. The one-road shape is: a collector for every operation, the note inside `_passed_by_person`, and recording in `apply` after the event is in (including `EventCommitted`). It would replace about ten explicit calls. `accept/decision passes recorded after commit by one collector | узел: <new rules-debt node>, owner Lead rules-debt`.

## Standing questions

- **Fit to spec:**
  - RD1-30: fit.
  - RD1-27: fit to the letter, and keeps the pinned bytes; the shape is wrong (A).
  - RD1-31: fit on the five sites named; B and C remain.
- **Builder's own decisions:**
  - The instance collector is safe for re-entry. The only `apply` re-entry is the decision memo pass (`:5085-5088`), which re-enters before the collector is set. `validate` called outside `apply` sees None and writes nothing.
  - An exception between collecting and recording goes through `finally`, so nothing is written (correct), except on the `EventCommitted` path (B).
  - A replayed key writes nothing (the store's replay skips validate).
  - "Owner: factory" carried in the block text is enough. No reader reads an `owner` field: `run_counters.py:514` counts rows, and `waiver.person_passes` (`waiver.py:977-1036`) reads S5 only, by `block`/`finding_id`. The phrase sits at about 160 characters, inside the 400-character cut, and `finding_id` keeps a longer block whole.
- **Seams:** additive. The changelog fragment is new; `controller-blocks.md` has no diff (builder's output; not re-run).
- **Class completeness:** findings C and F. SIBLING_MAP: the class lives in one file, and the sweep of the artifact is given in the table above.
- **Tests:**
  - (a) Killing power: `passed-by-word` (1 row) and `passed-by-word-other-block-refuses` (0 rows, refused after the note) both fail if the note or the position is wrong.
  - (b) The expected values trace to the finding text.
  - (c) The `EventCommitted` row is missing (B).
  - (d) The deleted `holds_over_comments` block went with its function (spec).
  - (f) `tests-over:` is present, and test lines are fewer than product lines.
  - The label is wrong (D).
- **Duplication and consistency:** `registry_why` is the one builder. A grep of `registry cannot be read|gate-registry.json cannot be read` over package, tools and kb finds no fifth role-facing copy. `gate_registry.py:797/979` (`{REGISTRY_REL} cannot be read: {why}`) is the A26 linter's text for developers, a different family: not applicable.
- **Code quality:** no new function over 60 lines. Names that lie: D.
- **Hygiene:** `selftest --lang` 2/2 was attached; nothing in the diff is Cyrillic.
- **Ratchets:** none touched.
- **Architecture:** the commit names AR-16, AR-13 and AR-25. AR-24 (a person's words reach what acts on them) is the closer fit for RD1-31, and B and C are breaches of it. Naming AR-24 is a fix of the commit message.
- **Judgment:** `judgment: none` holds. No check on a role's output is added.
- **One road:** A (two templates under one name) and the per-site notes of C are this class. The preferred shapes above close both.

## Spot-checks

- RD1-30 negative: `git grep -n -i holds_over_comments f1265890` returns only docs, specs, handoffs, the pile files, the changelog and `K8.txt`. There is no code or test hit. Positive control of the same shape: `git grep -n -i other_bytes` returns `proof_level.py:1588` and two tests. A filesystem grep, which includes untracked files, gives the same set.
- `proven` / `live_body` are still used: `test_proof_level.py:1512-1526`.
- Nested `apply`: `grep "self.apply("` returns `:5088` (decision memo) and `:8461-8657` (top-level helpers). None of them runs inside `validate`.

## Trail

- Read:
  - the earlier verdict (fixes 1-6);
  - the three finding files («Что именно менять»);
  - `critic-diff-brief.md` items 1-12;
  - `git diff c1b4ce7a f1265890` (whole) and the commit message;
  - `controller.py`: 2366-2475, 2865-2889, 3140-3170, 3235-3262, 3366-3395, 4262-4301, 5078-5092, 5170-5253, 5530-5832 (boundaries), 5640-5662, 5755-5772, 5978-6012, 6545-6630, 6975-6997, 7390-7412;
  - `event_store.py`: 35-65 (classes), 548-570, 632-740;
  - `waiver.py:975-1036`; `run_counters.py:505-525`; `refusal_registry.py:880-890`;
  - `test_controller_state.py:2270-2350`; `test_gate_registry.py:825-840`, 1185-1199;
  - `test_s5_plan_controller.py:660-675`; `test_s5_grown_windows.py:300-320`.
- Re-runs:
  - `( cd <tree>/ai-packages/qa-factory && python -B scripts/tests/test_gate_registry.py )` gives `=== test_gate_registry: 502/502 ok ===` (matches the builder).
  - Probe: `python -B <scratchpad>/probe_rd131.py <tree>/ai-packages/qa-factory/scripts` gives the two lines quoted in B.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "Dispatch branch: five sites fixed, three more pass roads remain inside validate(dispatch): _unreadable_plan_problems via :5656 and via _half_membership_problems :5589/:5591, and _plan_refusal via _s5_plan_problems :5768 (fix C). Decision-branch (:3164, :3253, :3391) and accept-branch (:6003, :6561, :7403) callers also drop passed (fix F, same file, within owns). Sibling of the position defect: the accept branch records before the event at about ten sites, proposed as a node with owner Lead rules-debt. RD1-30 negative verified with a same-shape control; K8.txt and the test locals are not applicable.",
  "fixes": [
    "B: controller.py apply :5215-5253 - on EventCommitted (ProjectionStale/DerivedViewStale) a committed dispatch writes no pass row (probe: pass_rows=0 with dispatch_event_committed=True); record self._dispatch_passes in the except branch when isinstance(exc, EventCommitted) before re-raise; add a REG_PRECONDITION_ROWS row with the after-commit step raising, expect 1 row",
    "C: controller.py - route _unreadable_plan_problems (:4282, called at :5589/:5591/:5656) and _plan_refusal (:6587, via :5768) passes through _note_dispatch_pass; preferred one road: call _note_dispatch_pass inside _passed_by_person and drop the five per-site calls; fix refusal_registry.py:886 claim if the dispatch-side road stays unrecorded",
    "A: gate_template.registry_why - drop the stop flag; one head plus a REGISTRY_BLOCK constant, the stop = REGISTRY_BLOCK + ': ' + registry_why(reason, tail with references/gate-registry.json, Owner: factory, the reinstall door); FR-6 walk; if the Lead keeps the stop bytes, two named functions instead of a flag",
    "D: proof_level.py:946-947 rename WHY_RUN_REGISTRY/WHY_RECEIPT_REGISTRY (now tails) or inline; test_gate_registry.py:1188 relabel the row to what it checks (the builder reproduces the four texts), it does not see the sites",
    "E: if fix C takes the minimal per-site shape, add one row for a helper-road pass (c1 or c3) committed with 1 row; not needed under the one-road shape",
    "F: decision branch :3164/:3253/:3391 and accept branch :6003/:6561/:7403 drop passed - open the collector for decision (mind the memo read before the lock at :5085-5088) and record S6/critic/mechanical passes at the accept branch's after-raise position; or the Lead opens a rules-debt node with this line",
    "commit message: name AR-24 for RD1-31"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/reviews/t-1084-c3-b2-d-topic-code.md",
      "docs/tasks/critic-diff-brief.md",
      "plans/piles/rules-debt/findings/20261117-c3-odin-stroitel-teksta-reestr-ne-chitaetsya.md",
      "plans/piles/rules-debt/findings/20261117-c3-holds-over-comments-udalit-ili-podklyuchit.md",
      "plans/piles/rules-debt/findings/20261117-c3-dispatch-prohody-ne-zapisany-cherez-record-person-pass.md",
      "git diff c1b4ce7a f1265890; git log -1 f1265890",
      "scripts/controller.py ranges listed in Trail",
      "scripts/event_store.py 35-65, 548-570, 632-740",
      "scripts/waiver.py 975-1036; scripts/run_counters.py 505-525; scripts/refusal_registry.py 880-890",
      "scripts/tests/test_controller_state.py 2270-2350; test_gate_registry.py 825-840, 1185-1199; test_s5_plan_controller.py 660-675; test_s5_grown_windows.py 300-320"
    ],
    "reruns": [
      {"command": "( cd <tree>/ai-packages/qa-factory && python -B scripts/tests/test_gate_registry.py )", "result": "=== test_gate_registry: 502/502 ok ==="},
      {"command": "python -B <scratchpad>/probe_rd131.py <tree>/ai-packages/qa-factory/scripts", "result": "stale=False pass_rows=1; stale=True raised=DerivedViewStale EventCommitted=True dispatch_event_committed=True pass_rows=0"},
      {"command": "git grep -n -i holds_over_comments f1265890 (control: git grep -n -i other_bytes)", "result": "no code or test hit, docs/pile/changelog/K8.txt only; control 3 hits incl. proof_level.py:1588"}
    ]
  }
}
```

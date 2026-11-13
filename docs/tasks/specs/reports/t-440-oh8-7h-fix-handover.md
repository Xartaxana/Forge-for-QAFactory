# t-440 handover: OH8-7h fix round (critic t-430 F1-F4, Lead decision D1)

Tree STAGED, not committed (3 files; this handover is untracked, per the handoff line the owned files were staged).

## Draft commit message (plain text)

OH8-7h fix round (t-440): release text, blind-spot text, test assertions and one class for the idempotency-reuse refusal after the critic t-430

F1 (critic t-430): changelog.d/oh8-7-census-subclass-raises.md no longer says a subclass-only refuser is counted as pending under a shrink-only constant; it says every such raise site is a check unit that needs its census row (OH8-7..OH8-7h classified the 190 functions).
F2 (critic t-430): the BLIND SPOTS docstring, BLIND_SPOT and the fixture about add the method/attribute factory form (raise self._reuse_refusal(...), event_store.py) to the still-unseen list; "it measured 52" now reads "the Lead measured 52 module-function rowless functions (spec t-346 6b)"; the number 52 and the token factory function stay.
F3 (critic t-430): test_neg_subclass_raises_flip_blocks_and_create_units asserts `not r["problems"]["C1"]` (the old assertion could not fire); the neutral_only row carries blocking=1 and the rowed assertion reads it. F3(c) not done.
F4 (Lead decision D1): one refusal, one class. IdempotencyKeyReused has three carriers, all now xref (one record against another under one key): story_step.py::start safety -> xref, controller.py::apply shape -> xref, event_store.py::_commit_locked shape -> xref. Owner and roles of the rows unchanged; apply(settle_order) stays safety.

Raise list (AR-20):
safety: 83 -> 82 -- story_step.py::start moves to xref (a LOWERING, critic t-430 D1)
no other ratchet key moves (blocking_per_role included); the census test reports 24 passed.

architecture: AR-20 -- the one ratchet key that moves, safety 83 -> 82, is a lowering and is named above with its one cause; AR-29 -- three rows re-judged by the critic verdict t-430 and the Lead decision D1, each one class per unit, the fixture and the test text change together
judgment: adds data check none -- three existing rows are re-classified (one safety to xref, two shape to xref), no row added or removed, no blocks_override added; each stays a data check classified per unit; the ceiling is lowered by one

tier: claude-fable-5-2 (to be confirmed by the Lead at commit)

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

(Axis block and four questions: the Lead's, as in 0818336; the axes touched are 1, 18, 32 as there. The Lead sets the tier line.)

## Per fix

- F1: changelog fragment clause replaced as worded in the review (the clause is joined into the sentence with "; and every such raise site ...").
- F2: docstring BLIND SPOTS paragraph, BLIND_SPOT, fixture `about` (line 3 of the json): method/attribute form added after the module-factory clause; docstring says "the Lead measured 52 module-function rowless functions ... (spec t-346 §6b; an upper bound ...)". Token `factory function` and 52 kept.
- F3(a): `assert not r["problems"]["C1"], (case, r["problems"]["C1"])`. (b): neutral_only third column 0 -> 1, rowed assertion `== blocking`. (c): NOT DONE (skipped as optional; not attempted).
- F4/D1: fixture rows `story_step.py::start` safety -> xref; `controller.py::apply` (plain row, line 206) shape -> xref; `event_store.py::_commit_locked` shape -> xref; `ratchet.safety` 83 -> 82. `apply(settle_order)` untouched. Neither the test file nor the fixture `about` stated the safety count or listed these functions by class.

## Siblings

No fourth carrier found among census rows: the fixture does not mention "Idempotency" at all; rows are keyed by file/function, and the three functions each have exactly one row in their file (controller.py has also apply(accept/decision/dispatch/settle_order/first_look_continue), per-branch rows of A24, not this refusal). Per review K2 the refusal is decided in _commit_locked (event_store.py:692-694), re-raised in apply and start. Not searched beyond the fixture.

## Witness

F1 key run. Keys quoted BEFORE the run: present "census row", absent "pending". Script (scratchpad keys.py, not committed):

```
import sys

PRESENT = ["census row"]
ABSENT = ["pending"]
text = sys.stdin.read()
bad = [k for k in PRESENT if k not in text] + [k for k in ABSENT if k in text]
for k in PRESENT:
    print("present", repr(k), k in text)
for k in ABSENT:
    print("absent", repr(k), k not in text)
print("FAIL" if bad else "OK")
sys.exit(1 if bad else 0)
```

Output on the new file:

```
present 'census row' True
absent 'pending' True
OK
exit 0
```

Negative control (`git -C <wt> show HEAD:ai-packages/qa-factory/changelog.d/oh8-7-census-subclass-raises.md | python -B keys.py`):

```
present 'census row' False
absent 'pending' False
FAIL
exit 1
```

Census test, from the package directory:

```
........................                                                 [100%]
24 passed in 92.35s (0:01:32)
```

`python -B scripts/selftest.py --limits --lang` tail:

```
PASS limits: SKILL.md / agents / references within size caps
PASS limits: every mandatory role rule of design/role-rules.json holds in its carrier

=== qa-factory selftest: 4/4 ok ===
```

`git -C <wt> status --short` (before this handover was written):

```
M  ai-packages/qa-factory/changelog.d/oh8-7-census-subclass-raises.md
M  ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json
M  ai-packages/qa-factory/scripts/tests/test_judgment_census.py
```

## Not done / notes

- F3(c) not done.
- The test's AR-20 reconciliation passes with safety 82 (no other number depended on it; no K4-derived number needed adjusting).
- Needed beyond the manifest: none.

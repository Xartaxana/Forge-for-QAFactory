# t-547: P1-a fix round 2 (after critic re-review t-539)

Worktree `.claude/worktrees/p1a-fix2`, branch `wip/p1a-fix2`, base 4e0c61d. Commit hash: see the final line of this report's handoff message (the report is committed together with the code, so the hash cannot be written inside it).

## What was done
- L1: the three P2 rows (`_plan_row_of`, two `derive ...plan_row`) carry `node: FV2-1`, the three P5 rows (`derive ...requirements`) carry `node: FV2-2`. "stand-in" wording gone from their notes; `raised_by` names the Lead's issue of the node.
- L2/N1/N3: `not_in_world` is a ratcheted section read by `known_red.load(path, "not_in_world")` (ONE loader, `Row.reason`); every row is `{"reason","raised_by"}`; `raised_by` of the 47 rows is `docs/tasks/specs/reviews/20261113-p1a-fix-rereview.md L2 (Lead word 13.11.2026)`. New `known_red.pin_problem(path, section, count)` and key `pins.not_in_world: 47`. `_not_in_world()` and its per-row re-reads are removed; one cached `_loaded(section)` serves `check()`.
  - Strictness: EQUALITY, like the file's other pins (`readers`, `families`), with two messages: count above the pin names both numbers ("holds N rows, above pins.not_in_world M"), count below says "stale pin: ... lower the pin to N". Pin absent / not an int / a bool never passes and names the key; section absent = empty, pin 0 still required.
  - Kept: green row listed = stale, unknown id, row in both sections fail.
- L3: wall time measured, nothing else done: 15.7 s (final run), 17.4 s (previous run), 18.7 s before the round (same machine).
- N2: `form_filler`: after token substitution the value is re-tested (`_finish_token`): a leftover hint that is no literal_text row makes it `Unfillable` (message lists the leftover hints). `<cases_root>` is a `form_field_tokens` row in `form-fill-rules.json` (`"<cases_root>": "artifacts.cases_root"`), resolved after every field of the form has its value (override included); form with no such field / no plain value -> `Unfillable` naming the token and the field. Contract-owned values with a non-token hint are NOT unfillable: `Filled.kept_in_contract`, counted in the summary and listed by name (hint cut to 100 chars in print). `Filled.literal_text` counts the literal-text values.
- N4: `form_filler.reverse_walk_languages(source)` collapses a runner key onto its language through the `{"like": ...}` rows of the `test_file:<lang>` template row (no pair in code); a runner key with no link, or whose target language is not walked, stays walked and `LANG_NOTES` prints why in the row detail and the summary line. The `@pytest` ledger row is deleted (29 known_red rows). Forward walk untouched (`output: test_file:pytest[base]` rows stay).
- N5: `_round_world` comment fixed. N6: reason of `derive: s5-automator-to-runner:inputs_read[1].version` corrected (path `<cases_root>/<case>.md`, the form has no cases_root field); the row did NOT leave the section: after N2 it is red again for a TRUE reason (path is Unfillable, deriver has no file to hash), so the pin stays 47.

## Summary lines before / after (`test_field_producers.py`)
| | before (4e0c61d) | after |
|---|---|---|
| unfillable | 8 | 11 |
| literal | 7 (critic's probe; not printed before) | 7 |
| left_for_code | 82 | 82 |
| kept_in_contract | n/a (13 silent hints, 9 contract-owned) | 9 |
| known red rows | 30 | 29 |
| not in world rows | 47 | 47 |
| pairs / languages | 36 / 5 | 35 / 4 |
| rows walked | 880 | 905 |

## NEWLY RED ROWS: a raise, NOT added by me (Lead names it)
Cause: `<cases_root>` is now Unfillable in the three forms that carry the token but have no `cases_root` field (only s4-designer-to-case-critic has one, `:70`). 5 rows, none in `known_red` or `not_in_world`; the file is RED on exactly these 5 (plus the aggregate row "known_red: the red rows of the walk are exactly the ledger — 5 problems"):
1. `unfillable s4-case-critic-to-designer:inputs[1].path «<cases_root>/<area>/<case>.md»` — the contract's token <cases_root> reads the field `artifacts.cases_root` of this form, which gives no plain value (it was None)
2. `unfillable s4-designer-to-runner:inputs[1].path «<cases_root>/<area>/<case>.md»` — same detail
3. `unfillable s5-automator-to-runner:inputs_read[1].path «<cases_root>/<case>.md»` — same detail
4. `accept: s4-case-critic-to-designer[concerns].stage_acceptance.failure_class -> acceptance.stage_acceptance_errors` — the form s4-case-critic-to-designer cannot be filled: [('inputs[1].path', "the contract's token <cases_root> ... (it was None)")]
5. `accept: s4-case-critic-to-designer.inputs_read[-1].path -> stage_done.reviewed_author_dispatch` — same cascade

Rows 4-5 are cascades of row 1 (the accept round refuses an unfillable form). Fork for the Lead: instead of raising 5 rows, give `FillContext` a `cases_root` key (a `context_tokens` row) as the fallback when the form has no field; I did not decide it.

## The critic's B2 probe, re-run (FULL source: `b2_probe.py`, scratchpad, source below)
```python
"""B2 probe (critic t-539, re-run): every form, base variant, the test's own context, read-only.
Walks the filled data for a hint (FF.HINT) that is NOT: unfillable, left_for_code, a literal_text value, or named in kept_in_contract."""
import sys
from pathlib import Path

TESTS = Path(sys.argv[1])
CONTROL = len(sys.argv) > 2 and sys.argv[2] == "control"
sys.path.insert(0, str(TESTS))
import harness  # noqa: E402,F401
sys.path.insert(0, str(harness.SCRIPTS))
import handoff  # noqa: E402
import form_filler as FF  # noqa: E402


def walk(node, path=""):
    if isinstance(node, dict):
        for k, v in node.items():
            yield from walk(v, f"{path}.{k}" if path else k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk(v, f"{path}[{i}]")
    elif isinstance(node, str):
        yield path, node


index = handoff.index()
forms = list(dict.fromkeys([r["contract"] for r in index["handoffs"]] + [index["escalation"]["contract"]]))
silent, literal, kept, unfill, left = [], 0, 0, 0, 0
for contract in forms:
    cx = FF.FillContext(author_dispatch="S2-author-1", dispatch_id=f"{contract}-w1", cases=["TC-001"])
    verdict, variant = FF.variants(contract)[0]
    f = FF.fill_form(contract, cx, verdict=verdict, variant=variant)
    unfill += len(f.unfillable)
    left += len(f.left_for_code)
    literal += len(f.literal_text)
    kept += len(f.kept_in_contract)
    named_kept = set() if CONTROL else {p for p, _h in f.kept_in_contract}   # control: pretend kept_in_contract is not a named class
    skip_paths = {u.path for u in f.unfillable} | set(f.literal_text) | named_kept
    for path, value in walk(f.data):
        if not FF.HINT.search(value):
            continue
        if path in skip_paths or any(path == c or path.startswith(c + ".") or path.startswith(c + "[") for c in f.left_for_code):
            continue
        if FF._literal_text(value) is not None:
            continue
        silent.append((contract, path, value[:80]))
print(f"unfillable {unfill}, literal {literal}, left_for_code {left}, kept_in_contract {kept}, silent {len(silent)}")
for row in silent:
    print("SILENT", row)
```
Output (`python -B b2_probe.py <TESTS>` from the package root):
```
unfillable 11, literal 7, left_for_code 82, kept_in_contract 9, silent 0
```
NEGATIVE control (`... control`: kept_in_contract not treated as a named class) shows the probe sees them: `silent 9` (s2 expected_of_the_receiver[2]; s5-automator-to-critic inputs[3], inputs[4]; s5-critic-to-automator inputs[0]; s5-automator-to-runner inputs[2]; s5-critic-plan-to-automator inputs[0]; s7-analyst-to-automator inputs[3]; s7-automator-to-analyst inputs[1], inputs[2]). The 4 partial-substitution values of the critic's 13 are now Unfillable (the 3 s4 forms and s5-automator-to-runner inputs_read[1].path).

## Witness (verbatim)
Command: `( cd C:\QAFactory\forge-repo\.claude\worktrees\p1a-fix2\ai-packages\qa-factory && python -B scripts/tests/test_field_producers.py )`, real 0m15.676s. Selected lines (the whole output was captured; the red lines are all of them):
```
FAIL unfillable s4-case-critic-to-designer:inputs[1].path «<cases_root>/<area>/<case>.md» — the contract's token <cases_root> reads the field `artifacts.cases_root` of this form, which gives no plain value (it was None)
FAIL unfillable s4-designer-to-runner:inputs[1].path «<cases_root>/<area>/<case>.md» — the contract's token <cases_root> reads the field `artifacts.cases_root` of this form, which gives no plain value (it was None)
FAIL unfillable s5-automator-to-runner:inputs_read[1].path «<cases_root>/<case>.md» — the contract's token <cases_root> reads the field `artifacts.cases_root` of this form, which gives no plain value (it was None)
forms 24, variants 434, fields 980, unfillable 11, literal 7, left_for_code 82, kept_in_contract 9
FAIL accept: s4-case-critic-to-designer[concerns].stage_acceptance.failure_class -> acceptance.stage_acceptance_errors — the form s4-case-critic-to-designer cannot be filled: [...]
FAIL accept: s4-case-critic-to-designer.inputs_read[-1].path -> stage_done.reviewed_author_dispatch — the form s4-case-critic-to-designer cannot be filled: [...]
readers 19, pairs 35, languages 4
deriver round: forms 24, fields met 38
FAIL new red: ... (the same 5 rows, as `known_red.reconcile` words them)
FAIL known_red: the red rows of the walk are exactly the ledger — 5 problems
known red rows 29, not in world rows 47, rows walked 905
=== test_field_producers: 910/921 ok ===
```
(921 - 910 = 11 FAIL lines = the 5 rows, their 5 `new red` echoes by the reconcile, and the aggregate row. The new DoD rows all PASS: 16 `not_in_world ratchet: ...` rows, 7 `filler: ...` rows for N2, `not_in_world: the count equals its pin`.)

Other runs: `python -B scripts/tests/test_judgment_census.py` -> `=== judgment_census: 24/24 ok ===`; `python -B scripts/selftest.py --lang` -> `=== qa-factory selftest: 2/2 ok ===`.

## DoD test rows (parameterised, ids name the case)
- `known_red`-style table `not_in_world_ratchet_cases` (16 rows): row without raised_by / whitespace / null; without reason; unknown key; old string shape; count equals pin; above pin; below pin; missing pin; pin string; pin bool; pins not an object; section absent (pin 0 ok, no pin fails, pin above 0 fails).
- `form_filler_hint_cases` (7 rows): token + leftover hint -> Unfillable; `<cases_root>` filled; follows the field value; no field -> Unfillable; no case in the world -> Unfillable; kept_in_contract counted; kept value unchanged.
- Python/pytest one row: the real walk (`@pytest` ledger row removed, `languages 4`); no separate synthetic row (the collapse reads the registry's `like` row).

## Deviations / findings
- Fixture paths as named. `known_red.py` `load` signature unchanged (`section` argument now selects the schema); `Row` gained `reason`.
- Edge not specified by the spec, handled as stated by N2 text: a contract-owned value that holds a token AND another hint is Unfillable after substitution (it carries a token, so the filler substitutes it); 0 such values exist today (all 9 kept values have no token).
- `form_field_tokens` is a new key of `form-fill-rules.json` (data row, AR-1).
- Report note: the critic's F3 sentence "refusal shows" in the previous report was inaccurate (`manifest_row[base]` passes); not repeated.

## siblings (reported, not fixed)
No exhaustive scan of scripts/tests for other silencers (a grep of "known_red|ratchet|allowlist..." matches 123 files, mostly unrelated words). Candidates a critic should check for a `raised_by`-like naming of each raise: `state_census.py` and `fixtures/judgment-census.json` (shrink-only ratchets with their own mechanism, not re-read by me). `hand_inputs` section of `form-rounds.json` is data, not a silencer.
Also open (queued by the Lead, not mine): FV1-19 marker + obligation double count; split of `every_stage_output_fills_or_is_named`; B3 carriers (SIBLING_MAP / architecture.md / critic brief).

## Commit lines
```
architecture: AR-20 -- not_in_world is a ratchet like known_red (same loader, raised_by on every row, pins.not_in_world equality both ways), the six stand-in rows carry real nodes; AR-28 -- a value never leaves the filler carrying a hint (Unfillable, literal_text row, left_for_code) and the contract's own hints are named in kept_in_contract; AR-13 -- one loader for both sections, one language reader with the runner keys collapsed by the data's own `like` rows
judgment: none -- test-side data and harness only; no check decides a role's judgment (P27)
```

needed beyond the manifest: handoffs/s4-designer-to-case-critic.yaml, handoffs/s5-automator-to-runner.yaml, references/case-markers.json, references/detectors.json, scripts/handoff.py (CONTRACT_OWNED), tools none.

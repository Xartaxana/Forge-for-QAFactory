# t-377 — critic on the OH8-7b diff (commit e9a3822, parent 0bc7b1d, branch wip/oh8-7b)

Verdict: **fit_with_fixes**. No blockers. Three fixes, all test or witness work that the OH8-7c fix round can carry on the pair's tip (E15). One process note.

What I reviewed: a `git archive e9a3822 ai-packages/qa-factory` copy in my scratchpad. I did not review the worktree itself, because the worktree
`C:\QAFactory\forge-repo\.claude\worktrees\oh8-7b` held UNCOMMITTED edits while I was reviewing. Another worker is editing it: at first
`SUBCLASS_UNIT_FILES = ("probe_by_code.py",)` in the test, and a few minutes later the fixture as well (`git status --short`: ` M ...judgment-census.json`,
` M ...test_judgment_census.py`). That looks like the OH8-7c builder working in b's worktree. So my first control run in the worktree
(26/26 ok) does not count as evidence. Every result below comes from the clean copy.

## Key 1 — FIT TO SPEC (spec t-346 §2.1, §2.2, §3.3 DoD 1-11, §3.4)

| DoD / spec item | Status | Evidence |
|---|---|---|
| §2.1 step 1: family and widened sites computed before the per-file loop | met | test l.247-252 (e9a3822); the old computation after the loop is removed (diff hunk @@ -272) |
| §2.1 step 2: a listed file or `file::fn` creates u3 from widened sites | met (equivalent form) | l.285-287 adds widened-site units AS WELL AS the literal-site units (l.283-284), not instead of them. The spec allows this ("literal ⊂ widened"), so behaviour is identical |
| §2.1 step 3/4: stage, registry and flip passes run after creation, unchanged | met | the order in `units_of` is unchanged after l.293 |
| §3.4 item 2: list-form checks under C7 (E4 duplicate / a function of a listed file; E5 stale file / stale function) | met | l.253-265; `analyse` extends C7 at l.519; the real-tree `test_c7_...` reads `_real()["problems"]["C7"]` (l.595), so a stale real entry turns red |
| §3.4 item 3: the C7 "above" door text | met, verbatim | l.491-492 "or list its file in SUBCLASS_UNIT_FILES with its rows (the OH8-7 chain)"; asserted in `test_neg_pending_is_dense_and_only_shrinks_c7` |
| §3.4 item 4: `_run` setdefault `unit_files=()`, SUBCLASS_ROWS column, seven listed rows, C7 table (ok/twice/file_and_function/stale_file/stale_function) | met, but four rows are vacuous (F1) | l.646, l.845-857, l.884-890 |
| §3.4 item 5: docstring u3 line, blind-spot paragraph, BLIND_SPOT, fixture `about`, needle `subclass_unit_files` | met | diff hunks; `test_blind_spot_states_the_subclass_clause` passes in my run |
| §3.4 items 6/7: SIBLING_MAP axes 18 and 34, brief q9/q11 | met | see key 7 |
| DoD 2: 23 entries | met | l.101-110 match §3.1's OH8-7b list name for name (compared by reading) |
| DoD 3: intermediate run, C1 names exactly the 23 and C7 asks for 167 | met (Lead-attached text) | consistent with my whole-file probe (key 5), which yields exactly the 23 OTHER names for c |
| DoD 4 / C-8: 23 rows, sorted | met | fixture hunk @@ -615: 15 shape, 7 xref, 1 safety; byte order checked by hand ("__init__" < "_first_check"; "check_on_line" < "checks_of"; "_profile_cwd" < "_profile_of" < "_python_entry") |
| DoD 5: ceiling 190 -> 167, dense | met | my run: `subclass_pending=167 (ceiling 167)` |
| DoD 6: raise list plus reconciliation | met | key 4 |
| DoD 7: green, totals line | met | my control re-run, identical totals line (trail) |
| DoD 8: refusal_registry.py not in the diff; no `ast.Raise` in the test | met | `--stat` shows 4 files; `grep -ci "ast\.raise"` on the test = 0, positive control on refusal_registry.py = 1 |
| DoD 1 (step-0 output) and DoD 9 (doc-dispatch witness for SIBLING_MAP and the brief, with a negative control) | NOT in the attached mechanical layer | F3. I checked the keys myself by reading the diff: `SUBCLASS_UNIT_FILES` is in the axis-18 row, `OH8-7b` is in the axis-34 row, and both constants are in the brief. The substance holds; the witness is missing |
| DoD 10 / 11 | met | `selftest --lang 2/2` (attached); the commit message has the architecture, judgment, raise-list, four-question and tier lines |

Nothing beyond the spec was added: no new test file, and none of the `MEANING_CEILING`/`BLOCKING_ENTRY_FILES`/`UNIT_NAME_RE`/`JUDGE_CALLS`/`SCAN_*` constants was touched.

## Key 2 — MECHANISM SOUNDNESS

Traced cases (code l.247-287, flip loop l.318-327):
- **Shadowed local name, a class defined in tests only, no binding, `raise A()`, cycle.** Unit creation in a listed file reads ONLY `wide`, the output of
  the same `raise_family` + `sites(raises=)` the flip rows already pin. If such a raise is not a widened site, then `blocking=0` in the unlisted
  rows `unrelated` / `shadowed_local` / `tests_only` / `no_arg` / `cycle` proves it, and a listed file cannot create a unit from it. The safe side
  holds in the code.
- **A function entry whose file is also listed.** It is red under E4 in either order, because `listed_files` is built from all entries before
  the loop (l.254, l.259). Mutation M5 (drop that clause) turns `file_and_function` red.
- **A stale entry.** A file missing from `trees` is red. A `file::fn` with no widened site named `fn` is red (M4 turns `stale_function` red).
  Hostile spellings fail closed, traced by hand: `""` and `"a.py::"` give stale; `"a.py::b::c"` gives function `b::c`, also stale; a bare string passed as the
  tuple (a missing comma) iterates character by character, and every character is stale.
- **A function with both a literal and a widened raise.** It is already a u3 unit through the literal site. The entry is not stale (literal ⊂ widened) and
  adds nothing. That matches E5/C-4.
- **Positional invariant: pending ∩ listed = ∅.** A listed widened site creates `(file, s["function"])`. In the flip loop, `s["function"] == key[1]`
  is a hit, so the site cannot go to pending. Holds.
- **No false green on the real tree.** See key 5: listing the whole file on e9a3822 gives C1 = exactly 23 rowless units and C7 = "lower to 144".

Do the test tables fail when the mechanism breaks? I ran copy probes (mutated copies of the test module, run only for the two synthetic tests):

| mutation | SUBCLASS_ROWS test | C7 test |
|---|---|---|
| M2: no creation from widened sites | FAIL (`listed_neutral` pending) | FAIL (`ok`) |
| M3: function entries ignored | FAIL (`listed_function`) | pass |
| M4: no stale-function check | pass | FAIL (`stale_function`) |
| M5: no file-and-function duplicate check | pass | FAIL (`file_and_function`) |
| **M1b: a listed whole file creates a u3 unit for EVERY function in it, refusing or not (a false unit)** | **pass** | **pass** |

So every table turns red under some mutation. But the four "E11 safe side" rows prove nothing about creation: M1b passes them (F1).

**F1 (fix, test strength / duplication; `test_judgment_census.py` l.849-854, e9a3822).** `listed_unrelated`, `listed_shadowed_local`, `listed_tests_only`
and `listed_no_arg` reuse the sources of the unlisted rows. Those sources define only `check_f`, which is a unit through u1 (`UNIT_NAME_RE` `^check_`)
whether or not anything is listed. "Listed, still no unit" therefore cannot be observed. The created-unit assertion (l.873) checks only
`helpers_x.py::f`, and these sources have no `f`. The rows repeat the unlisted rows' `blocking=0` and nothing more, so the comment at l.848 ("the E11 safe-side misses
stay misses even when listed") claims more than the rows show. Exact fix: give the four rows a neutral-named function. For example, `listed_unrelated` becomes
`{"helpers_x.py": "class A(Exception):\n    pass\n\n\ndef f():\n    raise A('no')\n"}`, and do the same for the other three by replacing `_RAISE.format("A")`
/ `def check_f(x):` with `def f():`. Add an explicit expected column (`unit_f: bool`), or derive "created" as `listed and pending_of_unlisted_twin == 1`,
and assert `not _has(C1, "helpers_x.py::f is a check unit")` and `pending == 0` for these four. With that change, M1b turns them red. The fix is test-only,
needs no fixture or ratchet change, and fits the OH8-7c fix round.

## Key 3 — THE 23 ROWS (q11, AR-29)

Read in full, with every raise site, in `scripts/probe_by_code.py` (e9a3822 copy):
- **`_target_file` (l.2519-2539), Lead decision: safety. Agree.** There are three raises. The first is absence and the second is the suffix (shape), but the third
  (l.2534) refuses a target outside a test root or under `protected_app_paths`: "this probe never touches the product tree knowingly". That is a guard on the
  application, and CLASS_ORDER puts safety above shape. Owner `data` follows the safety precedent. The note is accurate.
- **`find_oracle` (l.759-816), Lead decision: shape. Agree, argued.** The subclass site is `ToolRefusal` at l.810: no recognised assertion in the body or the
  one-hop helpers. It does read the role's test text by pattern, but it is form recognition against `assertion_probes`. The door is "add the assertion's
  head as a form of references/detectors.json (the factory's data)". `ToolRefusal` is recorded as `refused: tool` (class docstring l.208-215). It never
  says the test is bad, so it is not meaning-proxy (quality by pattern). Same-file precedent: `_first_check` and `check_on_line` are both `shape`.
- **`plan_mutation` (l.1110-1220), Lead decision: shape. Agree.** The sites are: mutation name known (1128), parse (1134, 1218), no check of a known form (1154),
  data gaps (1172, 1197), and an internal invariant on line count (1213). All are form, presence or parse.
- **`_inverted` (l.1755-1798), builder's borderline: shape. Agree.** No inversion pair matches at the form's position, the `replace` does not expand, `fires_as`
  echoes the mutated text, the line breaks change, or the lexical state changes. All of these check the mutation's own form or data, before any byte is written.
  The output write is guarded elsewhere (`_target_file`, locks), so this is not a write guard.
- **`run_shape_checks` (l.2749-2829), builder's borderline: xref. Agree.** It mixes presence checks (`selector_args`/`report_test_id`, `selectors.verified`,
  `no_rebuild_flags`) with joins (the manifest row's file == the `--test` file, l.2796; the report id ends with the tail, l.2805; a longer title of another
  test, l.2809). The higher class is xref.
- **Five more.** `__init__` (one unit for every `__init__`; the subclass raises are in `Source.__init__` l.1402-1425: the lexer end state and unbalanced brackets)
  is shape. `locate` (l.281-291: the name resolves to exactly one def) is xref. `manifest_entry` (l.2832-2842: the instance id resolves in the manifest) is xref.
  `_profile_cwd` (l.2875-2899: a known profile; a shared root with different cwds is a tie) is xref. `build_request` (l.2902-2950: the request's selected
  instances include the asked one) is xref. All agree.
- I scanned the raise lines of the remaining 13 (`parse_node`, `_python_entry`, `parse_detector_node`, `body_span`, `locate_target`, `_statement_span`,
  `_matcher_position`, `plan_detector_mutation`, `checks_of`, `_parse_at`, `_parse_at_row`, `_profile_of`, `_longer_title`). Each tests form, parse,
  encoding, a data gap or one name resolving. None guards a lock, a claim, a secret, git state or an outside write, and none reads the meaning of content.
  The roles are `["conductor"]` throughout, following same-file precedent (iii) (every probe_by_code row except `judge_record`). The owner is `data`.

No blocker: no guard was filed as shape, and the content-pattern readers (find_oracle, _inverted) are argued above.

## Key 4 — RATCHETS (AR-20)

The fixture diff changes only the `about` string, `safety` 55->56, `conductor` 491->514 and 23 inserted rows. No existing row line is touched (the hunk is pure `+`
inside `rows`). 23 new rows name `conductor`, which equals +23. One new safety row (`_target_file`) equals +1. Both raises are named in the commit message
with the reason. `SUBCLASS_PENDING_CEILING` 167 is dense (my run: `subclass_pending=167 (ceiling 167)`, C7 silent). The Lead-attached reconciliation agrees
with my reading of the diff.

## Key 5 — THE CHAIN (OH8-7c)

Probe: on the e9a3822 copy I replaced the tuple with `("probe_by_code.py",)` and ran `analyse` on the real package. Result: C1 = 23 problems, all
"`probe_by_code.py::<c-name>` is a check unit (u3) with no row" (first: `_body_of`, `_check_record`), C2-C5 = 0, C7 = "144 ... below
SUBCLASS_PENDING_CEILING 167: lower" and pending 144. So the replacement is unambiguous: if c keeps any of the 23 function entries next to the file entry,
E4 turns it red, and the file entry alone creates exactly c's 23. Nothing in b blocks c.

## Key 6 — DUPLICATION, CODE QUALITY, q10, q12

- DUPLICATION AND CONSISTENCY: F1 (four rows that duplicate the unlisted rows' behaviour). The neutral source `_A + "def f():\n    raise A('no')\n"`
  appears four times (`neutral_only`, `listed_neutral`, `listed_function`, and `C7_NEUTRAL` l.884). `C7_NEUTRAL` was introduced but not reused in
  SUBCLASS_ROWS; fold this into F1. Grepped: the test file for the source literal and for `wide_by_file`/`raise_family` (a single computation, l.248-249).
- CODE QUALITY: **F2 (fix): test l.848 says "the sixth column".** The rows are `(id, files, blocking, pending, unit_files)`, so it is the FIFTH column.
  Also, l.866 `rows = [] if "def f()" in files["helpers_x.py"] else ...` picks the rows by sniffing the source text. It works for every current row, but it is brittle:
  a later row with a `def f()` beside `check_f` would silently drop the `check_f` row. Optional: make it an explicit column together with F1.
- q10 ARCHITECTURE: the line is true. AR-13: one scanner, and the computation was moved, not duplicated (no `ast.Raise`, refusal_registry untouched).
  AR-22: producer and reader are born together. Strictly, `analyse` also reads the constant as its default; that is harmless. AR-20 and AR-28: key 4. AR-29: key 3.
- q12 ONE ROAD: the temporary second road (pending in an unlisted file, a unit in a listed one) is recorded on axis 34 "known roads off it". It is bounded
  by both constants and closed by OH8-7h. The sub-road `file::fn` versus `file` is bounded to OH8-7c by E4. This is not an unbounded exclusion.

## Key 7 — CLASS-WIDE COMPLETENESS (docs/SIBLING_MAP.md)

- Axis 18 member text (the SIBLING_MAP hunk): "`SUBCLASS_UNIT_FILES` ... grow-only, each growth lowers `SUBCLASS_PENDING_CEILING` by its count ... removed together with it
  by OH8-7h". This matches the code comment l.96-100 and E6 (in the code, removing an entry turns C1 stale and C7 above).
- Axis 34 row matches the code's behaviour.
- Brief: q9 gains `SUBCLASS_PENDING_CEILING`; q11 gains both constants. This matches 6a F-B; q9 does not list the grow-only tuple, as decided.
- Commit axis lines, spot-checked:
  - Axis 1: true. `grep -c "SUBCLASS_|MEANING_CEILING"` = 0 in `CLAUDE.md` and in `.claude/agents/designer.md`, against 1 `MEANING_CEILING` in the brief.
  - Axis 12: true, but on another branch. `batch-9-perepis-podklassov-oh8-7b-h.md` is absent from origin/main, the root checkout and the oh8-7b tree, but
    present in `.claude/worktrees/conv-wave13/plans/piles/onboarding-hooks/`, together with the E3 finding file. That is the coordinator's move, as the line says.
  - Axis 18: true.
  - Axis 32: true.
  - Axis 34: true.
- No sibling outside the map is implied: the mechanism lives only in the census test.

## Fixes (none blocking; carry in the OH8-7c fix round on the pair tip, E15)

- **F1.** `test_judgment_census.py` l.849-854. Give the four `listed_*` safe-side rows a neutral `def f()` source and an expected-unit column, assert that no
  `helpers_x.py::f` unit exists and `pending == 0`, and reuse one `_NEUTRAL` constant for the neutral source. Proof that the fix works: mutation M1b (a listed file creates a unit for every function) goes red.
- **F2.** `test_judgment_census.py` l.848. Change "sixth column" to "fifth column".
- **F3.** Witness. Attach builder t-369's step-0 output (DoD 1) and the DoD-9 doc-dispatch key-presence run (full script source and a negative control) to the
  `accepted` event. If they are absent from the builder's report, DoD 1 and DoD 9 are retellings, and the c builder runs them for b's docs in the fix round.

Process note (for the Lead, not a node finding): OH8-7c's builder is writing in OH8-7b's worktree while b is under review. Any "run it there" dispatch to a
reviewer on that path reads c's state.

## Trail

Read:
- the commit message and full diff of e9a3822 (`git show`)
- spec t-346: §2.1-2.2, §3.1-3.5, §4, §6-10
- the scope of the t-353 plan review (verdict block)
- test_judgment_census.py l.1-110, 225-330, 820-890 (e9a3822 copy)
- probe_by_code.py l.200-232, 233-330, 519-560, 759-822, 960-975, 1110-1220 (raise lines), 1396-1430, 1460-1800 (raise lines), 1943-2518 (raise lines), 2519-2560, 2679-2950
- tools/critic_verdict.schema.json
- the SIBLING_MAP headings of axes 1, 12, 32, 34

Commands:
- `git -C <wt> status --short`: test and fixture modified, uncommitted, by another worker
- `git archive e9a3822 ai-packages/qa-factory | tar -x -C <scratch>/e9`
- `python -B <scratch>/e9/.../test_judgment_census.py`: exit 0, `26/26 ok`, totals line identical to the attached one: `census: 279 files scanned, 974 units; shape=729 xref=157 ... safety=56; breach=1; blocks_overrides=10; blocking_per_role: conductor=514 ...; subclass_family=55 subclass_pending=167 (ceiling 167)`
- `<scratch>/mut.py` (M1-M5) and `mut3.py` (M1b) on the copy: table above. M1 (an extra u1 name in a listed file) also went red, but only through the `(u3)` text of the C1 needle, so I don't count it
- `<scratch>/mut4.py` (whole-file entry): C1 23 rowless c-units, C7 "lower ... 144", pending 144
- `grep -ci "ast\.raise"`: test 0, refusal_registry.py 1 (control)
- `git ls-tree origin/main plans/piles/onboarding-hooks/`: no batch-9; Grep (case-insensitive) `OH9-1`: found the batch-9 file in the conv-wave13 worktree

Not run: the slow scenario files (as dispatched).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "F1 test_judgment_census.py l.849-854: listed_unrelated/listed_shadowed_local/listed_tests_only/listed_no_arg reuse check_f sources (a u1 unit), so 'listed, still no unit' is unobservable; mutation M1b (listed file makes every function a u3 unit) passes both synthetic tests. Give them a neutral def f() source plus an expected-unit column, assert no helpers_x.py::f unit and pending 0; reuse one _NEUTRAL constant (now repeated 4x, C7_NEUTRAL not reused). Carry in the OH8-7c fix round (E15).",
    "F2 test_judgment_census.py l.848: comment says 'the sixth column'; the rows are (id, files, blocking, pending, unit_files) - fifth.",
    "F3 witness: DoD 1 step-0 output and DoD 9 doc-dispatch key-presence run (source + negative control) are not in the attached mechanical layer; attach from builder t-369 to the accepted event, or re-run in the fix round. Keys verified present by the critic reading the diff."
  ],
  "class_completeness": "Axis 18 and 34 rows match the code (grow-only tuple, removal by OH8-7h; second road bounded by both constants); brief q9/q11 edits match 6a F-B; commit axis lines 1, 12, 18, 32, 34 spot-checked true (axis 12 batch-9 lives on conv-wave13, the coordinator's move). The mechanism is confined to the census test; no sibling outside the map.",
  "trail": {
    "read": [
      "git show e9a3822 (message + full diff)",
      "C:/QAFactory/forge-repo/docs/tasks/specs/t-346-oh8-7b-chain-spec.md sections 2-4, 6-10",
      "C:/QAFactory/forge-repo/docs/tasks/specs/reviews/t-353-oh8-7b-chain-plan-review.md verdict block",
      "e9a3822 copy: scripts/tests/test_judgment_census.py l.1-110, 225-330, 820-890",
      "e9a3822 copy: scripts/probe_by_code.py l.200-330, 519-560, 759-822, 960-975, 1110-1220, 1396-1430, 1460-1800, 1943-2518 raise lines, 2519-2560, 2679-2950",
      "C:/QAFactory/forge-repo/tools/critic_verdict.schema.json",
      "docs/SIBLING_MAP.md axes 1, 12, 18, 32, 34 (worktree)"
    ],
    "reruns": [
      {"command": "python -B <scratch>/e9/ai-packages/qa-factory/scripts/tests/test_judgment_census.py (git archive of e9a3822)", "result": "exit 0, 26/26 ok, totals line identical to the attached one (conductor=514 safety=56 subclass_pending=167 ceiling 167)"},
      {"command": "<scratch>/mut.py and mut3.py: mutated copies M1b/M2/M3/M4/M5, two synthetic tests", "result": "M2,M3,M4,M5 red; M1b (false unit for every function of a listed file) green on both - F1"},
      {"command": "<scratch>/mut4.py: SUBCLASS_UNIT_FILES=('probe_by_code.py',) on the real package", "result": "C1 = 23 rowless OH8-7c units, C7 lower to 144, pending 144: chain unambiguous"},
      {"command": "grep -ci 'ast\\.raise' test_judgment_census.py / refusal_registry.py", "result": "0 / 1 (positive control)"},
      {"command": "git -C <wt> status --short", "result": "test and fixture modified uncommitted by another worker; review done on the archive copy"}
    ]
  }
}
```

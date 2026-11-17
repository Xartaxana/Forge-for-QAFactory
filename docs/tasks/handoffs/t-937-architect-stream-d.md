# t-937 stream D -- family readers (green after the Lead's option (a))

DoD: `python -m pytest tools/test_tier_echo.py tools/test_journal_echo.py tools/test_dispatch_gate.py tools/test_journal_hooks.py tools/test_token_usage_stats.py -q -p no:cacheprovider`

## Output
```
........................................................................ [ 89%]
..................................................................       [100%]
642 passed in 74.42s (0:01:14)
```
(test_dispatch_gate.py is included and ran in this one run; the whole command took 74 s. Earlier red run before the test-copy fix: 30 failed, 612 passed, cause ModuleNotFoundError: tier_ladder in copied hooks.)

## Table: file -> what changed (all STAGED, nothing committed)
| file | change |
|---|---|
| tools/tier_echo.py:126-130 | `from tools import tier_ladder` / `import tier_ladder` fallback (no try/except around the word list: a missing home stays a loud ModuleNotFoundError); `KNOWN_TIER_WORDS = tier_ladder.FAMILIES` |
| tools/dispatch_gate.py:1039-1044 | same import pair; `_FAMILY_NAMES = tuple(reversed(tier_ladder.FAMILIES))` (strongest-first as before) |
| tools/dispatch_gate.py:~1058-1060 | `_model_family` -> `tier_ladder.family_of(model_id)`; docstring reworded: home is a leaf, not a gate |
| tools/journal_hooks.py:37, :211 | `import tier_ladder`; door text from `" / ".join(tier_ladder.FAMILIES)` (weakest-first now) |
| tools/token_usage_stats.py:100, :120, :173-177 | `import tier_ladder`; `FAMILY_ORDER = [f.capitalize() for f in tier_ladder.FAMILIES]`; `family()` -> `family_of` + `.capitalize()`, unknown -> `model or "unknown"`; "mythos" -> Fable via ALIASES |
| tools/test_tier_echo.py:568 | `_hook_copy` also copies tier_ladder.py (one line added) |
| tools/test_journal_echo.py:1237 | `tier_ladder.py` added to the copied-name tuple |
| tools/test_dispatch_gate.py:3385, :3344 | `tier_ladder.py` added to the copy list of test_a_missing_transcripts_is_silent; `_gate_run` shadow folder (sibling style) also gets tier_ladder.py (one line). No assertion/expectation changed |

## Search: non-test lists naming tier_echo (tools/*.py excl. test_*, tools/*.json, .claude/settings.json, .githooks/, .github/workflows)
- tools/mechanism_gate.py:266 `"tools/tier_echo.py"` in the live-wiring list; line 267 ALREADY names `"tools/tier_ladder.py"` -> nothing to add.
- tools/mechanism_gate.py:83, :276 comments only.
- tools/dup-baseline.json:394, :527 clone-baseline entries, not a copy/install list -> tier_ladder need not join.
- Other hits are comments/docstrings (agent_budget.py:28, permission_audit.py:126, negative_lint.py:93, journal_echo.py, transcripts.py).
- .claude/settings.json, .githooks/, .github/workflows: no `tier_echo` hit (Grep with the same glob/pattern shape found the other hits above, so the empty result is a positive-controlled one for that glob).
Verdict: no non-test list requires a change; no question back.
Note (not a list, test side, not edited): tools/test_p4_stdin_deadline.py:80 and tools/test_streams.py:375 name tier_echo; both passed-by-design/not run here.

## Deviations
Test edits only as authorised by the Lead (copy lists). Not run: other test files beyond the DoD.

## Questions
none

## needed beyond the manifest
tools/mechanism_gate.py:198-205,266-267, tools/streams.py (import pattern), tools/test_p4_stdin_deadline.py, tools/test_streams.py (read only)

## Fix round (critic t-946)

D-1 -> added tier_ladder.py to the two single-file copies of dispatch_gate.py:
- tools/test_transcripts.py:1386 and :1388 (`_alone(..., "dispatch_gate.py", "tier_ladder.py"[, "transcripts.py"])`)
- tools/test_critic_snapshot.py:485 (`_write_isolated_copy`: tier_ladder.py written next to dispatch_gate.py)
How seen: the copied gate imports cleanly; `import dispatch_gate; decide({})` in the copy dir (broken_decide=True) dies with `RuntimeError: simulated dispatch_gate.decide failure` (not ModuleNotFoundError); test_dispatch_gate_decide_raises_fail_open_snapshot_written PASSED.

Q7 -> removed `if basis == "judge": return None  # S4` (tools/journal_echo.py ~:2199), the S4 comment lines (~:1994) and the two stale "S1/S4", "judge" mentions in neighbouring comments; deleted test_s4_basis_judge_silences_unconditionally and test_edge_r3xr13_collision_s4_silences in tools/test_journal_echo_r3.py (the negative twin kept, renamed test_no_basis_warns). Forced consequence: test_k7_fixture_marks_exactly_the_expected_lines now also expects line 7 (fixture row basis "judge", t-104) as no_input -- the same echo as any failing line (test_journal_echo_r3.py:~822). Fixture file not touched.
Edge witness: `_check_accepted_r3({accepted, builder, t-9, basis:"judge"}, set())` -> ('no_input','t-9'); same without basis -> ('no_input','t-9'); no crash.

DoD (verbatim):
$ python -m pytest tools/test_transcripts.py tools/test_critic_snapshot.py tools/test_journal_echo_r3.py tools/test_dispatch_gate.py -q
653 passed in 49.50s

Sibling grep (Grep tool, glob tools/test_*.py, pattern `dispatch_gate\.py|tier_ladder`; positive control = same call finds tier_ladder in test_dispatch_gate.py:3344,3386, test_tier_echo.py:568, test_journal_echo.py:1237):
- test_transcripts.py:1386/1388 _alone: added now
- test_critic_snapshot.py:477-485 copy: added now
- test_dispatch_gate.py:3344 shadow copy, :3386 file list: has tier_ladder.py
- test_tier_echo.py:568 (tier_echo copy): has tier_ladder.py
- test_journal_echo.py:1237 list: has tier_ladder.py
- test_dispatch_gate.py:3278-3324 `_race` (codes by name over the repo tools): n/a, runs in the real tools dir
- test_owns_gate.py:1030 (read_text only), test_dispatch_new.py:14 (paths), test_warn_messages.py:96 (_load_module from real tools dir), test_dispatch_gate_md.py:54: n/a, no isolated copy
- no hit copies journal_hooks.py or token_usage_stats.py alone (grep of those names in tools/test_*.py: only via real tools dir) -> n/a
Everything left unstaged-modified (not committed).

Correction to the last sibling line (verified with a Grep, pattern `journal_hooks\.py|token_usage_stats\.py|tier_echo\.py`, same glob; positive control: it finds test_tier_echo.py:567): test_journal_hooks.py:508 runs journal_hooks.py from the real tools dir: n/a; test_token_usage_stats.py has no copy (no copy/shutil hit; imports from real tools): n/a. Extra run: test_token_usage_stats + test_journal_hooks + test_tier_echo -> 169 passed.

# t-885 report

DoD: `python -B -m pytest tools/test_piles_close.py tools/test_wave.py tools/test_journal_echo_r3.py tools/test_hygiene_gate.py -q -p no:cacheprovider`
Output (verbatim tail): `489 passed in 227.36s (0:03:47)`
Also (pre-edit run, same worktree): tools/test_warn_messages.py green with the hygiene file: 566 passed + the 7 piles/echo reds then fixed below.

Per test (cause -> fix):
- test_piles_close (6 tests): fixture ids `t-1`/`t-5`/`t-12` are non-canonical under the offload id grammar -> TEST side: `t-001`, `t-005`, `t-012` (no test existed to prove a non-canonical id is refused; none touched). Product right (P31).
- test_wave test_origin_hook_refusal_prints_its_text_E_C3_4 and test_status_commit_refusal_takes_the_same_road_C3_5: hook files written with write_bytes are not executable on Linux, git skips them -> TEST side: `chmod(0o755)` after write. wave.py not touched; not reproducible on Windows (bit ignored), so Linux effect is by reasoning, not witnessed.
- test_journal_echo_r3 test_r3_events_joins_the_same_silence_check_as_siblings: offload moved the silence check from an inline `if (not violations ...)` in main() to `if not _echo_visible(...): return 0` with `_echo_visible` one expression over all sources incl. parts["r3"]. Protected property (r3 in the SAME shared check) intact -> TEST side: pin re-anchored to main()'s `_echo_visible` call and the names in `_echo_visible`'s source.
- test_hygiene_gate [git-checkout-on-a-dirty-tree] and keeps_the_refusal_classes_of_the_live_gate: fixed by 9f486c3d (CI run was f07dcbc3, pre-fix); green on HEAD, nothing touched.
- test_warn_messages::test_c4_imperative_verb_present: fixed by 9f486c3d; green in my run.

Newer run 43969697881 was in_progress (not read). Siblings: other test files grep-match `t-1` but I did not verify them as stale; none reported red.
Needed beyond manifest: none.

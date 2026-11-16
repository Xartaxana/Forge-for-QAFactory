# t-900 FG7-49 report
DoD: `python -B -m pytest tools/test_dispatch_gate.py -q -p no:cacheprovider`
Output (verbatim tail): `349 passed in 23.51s`

Done: `format_path_report` (tools/dispatch_gate.py) prints `PATH CHECK: ok (<n> owns, <m> given)` when every path has status ok/new. Otherwise it lists only paths with another status (missing/outside/unchecked/glob), with the same lines as before (`_describe` unchanged); ok/new lines are not printed. Bytes/lines are computed only inside `_describe` and used for no decision, so nothing else to keep computing.
Tests: pin at ~2900 rewritten; new parametrized rows (all exist, `(new)` owns counted, one given missing -> only the missing named, no `tools/have.py` line, no bytes) + a zero-given / non-missing-problem row via fake path reports (empty given is refused earlier by the completeness check, so zero given is tested on the function).
Decision to confirm: statuses outside/unchecked/glob are treated as "needs action" (still listed), the spec only named missing. Easy to change if Lead wants them folded into ok.
git grep hits (outside owns): docs/SIBLING_MAP.md:326, :329 (prose, no pin on text); tools/warn_layers.json:307,310 literal `PATH CHECK: ` prefix, still emitted (prefix unchanged). No hits in .claude/.githooks.
Questions: none. Needed beyond the manifest: tools/warn_layers.json, docs/SIBLING_MAP.md (grep only).

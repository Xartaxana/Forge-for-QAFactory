# t-1459 FG7-6 card B report

DONE: B1 (new section `## Weekly cost review (scout report form)` before `## Closing out a run`), B2 (table columns verbatim, `not measured:` lines, no money), B3 (check 17 `(h) Cost review input`, four parts; 17(b) one pointer clause). File: PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md (staged, not committed: mechanism path).

Edges: EB1 absent report -> finding line, never "nothing to cut". EB2 money check (iii). EB3 `not measured:`. EB4 trail required. EB5 card A merged: `moves` is in forge_metrics.py on this base (grep count 23). EB6 no RESTATED words, no `path:N` anchors; pytest green.

Verified: scout.md line 5 `tools: Read, Glob, Grep` (so the print is pasted in). No `$`+digit in the protocol (grep -c = 0).

Deviations: none. Needed beyond manifest: none. Analogs noticed: none. New config keys: none. Changelog fragment: not written (document-only, PROCESS/ not in the package).

## Witness

Script (never committed; at scratchpad/keys_fg7_6.py):

    import pathlib, sys
    KEYS = ["## Weekly cost review (scout report form)",
            "| row (node or role) | tokens | repeats | reason | proposed cut |",
            "not measured:", "python -B tools/forge_metrics.py --node-cost --window",
            "docs/tasks/specs/reports/cost-review-", "(h) Cost review input", "nothing to cut",
            "cost review: absent for"]
    text = " ".join(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8").split())
    missing = [k for k in KEYS + sys.argv[2:] if " ".join(k.split()) not in text]
    print("missing:", missing or "none")
    sys.exit(1 if missing else 0)

Output:

    missing: none
    exit=0
    missing: ['NEGATIVE-CONTROL-KEY-ABSENT']
    exit=1
    python -m pytest tools/test_handoff_rule_anchors.py -q  ->  16 passed in 0.14s

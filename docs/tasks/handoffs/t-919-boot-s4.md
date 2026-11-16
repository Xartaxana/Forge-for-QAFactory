# t-919 — S4 principles index row

DoD: `python -m pytest tools/test_factory_rules_index.py -q -p no:cacheprovider`

## Output
```
..............................                                           [100%]
30 passed in 8.74s
```

## --check output (python -B tools/factory_rules_index.py --check)
```
factory rules index: up to date (59 rules)
skip: docs/OWNER_PRINCIPLES.md absent
exit 0
```
`git diff --stat -- docs/FACTORY_RULES_INDEX.md` after regenerating: empty.

## What was done
`tools/factory_rules_index.py`: data table `SOURCES` (name, kind, source, out, opener, header, line_cap, file_cap); row FR (unchanged logic, byte-identical output), row P (kind "bullets"). New: `first_sentence`, `cap_line`, `parse_bullets`, `build_bullets`, `run_row`; CLI gets `--row FR|P`. Without `--row` all rows run; with `--source/--out` and no `--row` the FR row runs (old form, old tests unchanged). Exit code = max over rows.

## edge -> test row (tools/test_factory_rules_index.py)
| edge | test row |
|---|---|
| FR byte-identical | test_fr_row_byte_identical_to_committed |
| both TEMPORAL worlds | test_p_row_temporal_both_worlds |
| per-file cap AT passes / one byte beyond refused, three longest lines + door | test_p_row_file_cap_at_and_beyond |
| duplicate P id (both lines named) | test_p_row_refusals[duplicate-id] |
| empty bullet (line named) | test_p_row_refusals[empty-bullet] |
| no entries at all | test_p_row_refusals[no-bullets] |
| first sentence; `.!?`; dot not before whitespace; period inside backticks | test_p_row_lines[first-sentence, gap-in-numbering, period-inside-backticks, dot-not-followed-by-space] |
| no sentence end -> whole bullet | test_p_row_lines[no-sentence-end] |
| numbering gap | test_p_row_lines[gap-in-numbering] |
| line cap AT limit passes | test_p_row_lines[cap-at-limit-passes] |
| line cap one byte beyond cut; long P19-like sentence; " …" | test_p_row_cut[cap-one-byte-beyond-is-cut, long-first-sentence] |
| never cut inside a UTF-8 char | test_p_row_cut[multibyte-with-spaces, multibyte-no-whitespace] |
| CRLF == LF (also multi-line bullet joined) | test_p_row_crlf_equals_lf |
| check ok / stale | test_p_row_check_ok_then_stale |

All P tests use fixtures in tmp_path.

## Deviations / decisions (spec silent; flag for acceptance)
- The first sentence KEEPS its terminating `.`/`!`/`?` (FR lines strip the period; the spec says "up to").
- The per-line cap applies to the WHOLE line `- P<n> — <sentence>` (prefix included), 220 bytes.
- Multi-line bullets: continuation lines (until blank line, a line starting `- ` or `#`) are joined with single spaces before the sentence scan.
- Write mode with source absent and out absent also prints the skip line (exit 0); out present + source absent -> exit 2 in both modes.
- If no whitespace fits before the cap, the cut is a hard cut at a character boundary.
- `--row` flag is new (needed to point the P row at fixtures).
- Existing FR-row messages "run ... and stage docs/FACTORY_RULES_INDEX.md" now print the row's own out path (same text for FR).

## Questions
none

## needed beyond the manifest
none. Siblings: tools/architecture_index.py stays a second generator (FG7-55). Staged: the two owned tool files and this handoff; no commit.

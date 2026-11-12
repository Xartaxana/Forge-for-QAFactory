- Briefs that reach the words rung of the trim ladder keep the person's waivers (`brief_pack.py`): a waiver of this stage (or
  of `*`) now keeps its own line at words level 1, in the order of level 2, instead of a count line, at EVERY stage and role;
  its whole text stays in `<ID>-decisions.md`. A level-1 brief therefore carries one line per waiver, and may pop more input-file
  lines than before: the person's words outrank the file list.
- The level-1 brief names the decisions side file once, in `## Not in the brief`, not twice (`brief_pack.py`): about 95 bytes
  less in every level-1 brief; briefs that never reach the words rung are byte-identical; a brief kept at level 2 by the rule
  below and still over pops its input files in the new priority.
- The words rung is taken only when it makes the brief strictly smaller (`brief_pack.py`): a rung that costs the person's words
  and saves nothing is skipped, and the last resort pops input files from the form that is kept. `over_ceiling` keeps its
  closed vocabulary: `words at level 1` still means the words at their shortest kept form.
- The last resort pops input-file lines in a fixed priority (`brief_pack.py`): the "critic findings: none yet" line, the source
  material, the other named inputs, the case files (the "... and N more" line first, then the last case first), the window's
  test file last; the doors never. The order the lines are RENDERED in does not change; `<ID>-files.md` lists them in it.
- A brief that stays over its budget after every cut says so (`brief_pack.py`): the first line of `## Not in the brief` names
  the budget and the reasons, outside the budget (`budget_bytes` is the same with and without it), and the line printed by
  `brief_pack.py` carries the same reasons for the conductor. Under `--output` or `--dry-run` the line adds that no side
  file was written in this run. `budget_bytes` no longer counts the by-range note of a brief over 30 KB either: it is measured
  before that note, like the over line.

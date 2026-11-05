- exploration charter for `qa-runner` at S6 (`references/explore-charter.md`, `scripts/brief_pack.py`): the first manual window of a story
  prints the charter's path, the cells of the perturbation table and the axis oracles in its brief; the role keeps a `tried` table
  beside the case and records a violated oracle as an `observations[]` entry, which reaches S7 as `<case>#obs<n>`. A flow with no
  request list is "not measured: <reason>", never "no bugs"; the charter carries no rule of any one project.
- perturbation axes `keyboard_input` and `reload_mid_operation` (`references/perturbations.json`, `scripts/user_path_failures.py`):
  one reader, `perturbation_axis`; `failure_axis` is its `request_failure` view and S3 reads it as before.
- `requests-seen.txt` (`scripts/manual_capture.py`, `references/manual-capture-steps.json`): each `ui` call stores the requests its page
  sent to a stand host (no query, repeats counted, capped, secret-looking lines counted not kept); a device writes no file and says so.
- every `manual_capture.py` `ui`, `http` and `app` call holds the stand's lease while it runs and answers `stand_busy` (exit 3, nothing
  opened) when another run holds the stand; a lease that cannot be used is a stderr note, not a block.

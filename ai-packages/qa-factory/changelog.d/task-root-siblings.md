- Four scripts that read a story folder (`judge_results.py --bugs`, `judge_diff.py`, `walk_timing.py`, `branch_accounting.py`) found the project by
  counting folders above the story, so with `artifact_root` set in the project config (for example `qa-artifacts`) they read the
  bugs, the cost records, the diff files and the manual evidence from the wrong folder. They now find the project by the one walk
  (`runtime_paths.nearest_project`) and read `<project>/qa-factory`, as `traceability.py` does. A story folder under no project, and a
  project with the default artifact root, behave as before

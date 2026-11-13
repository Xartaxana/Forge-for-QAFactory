- `traceability.py --task-root` and `--task` now read the same bugs folder (`traceability.py`): with `artifact_root` set in the
  project config (for example `qa-artifacts`), `--task-root <story>` used to take the bugs root two folders above the story
  (the project itself) and read no bugs; it now finds the project by the one walk (`runtime_paths.nearest_project`) and reads
  `<project>/qa-factory`, as `--task` does. `report_facts.py` shares the option block and changes the same way. A story folder
  under no project, and a project with the default artifact root, behave as before (B-348)

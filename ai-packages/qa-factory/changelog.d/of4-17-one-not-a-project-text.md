- one "this root is not a project" refusal (`hooklib.py`, `host_probe.py`, `dashboard_refresh.py`): the words are built in
  one place, `not_a_project_text`, which `require_project_at` prints and `host_probe._not_a_project` returns, so a person
  reads the same refusal from every caller; it names the `--root <above>` door when an ancestor carries
  `qa-factory/config.json`, onboarding when none does, and a door only the caller has (`extra_door`); the dashboard
  refresh asks the project marker through `_carries_project`
- the dashboard's refusal names its `--read-only --out <file outside the root>` door and `config_view.py` prints the shared
  text on a root with no project (its old sentence stays only for a marker present yet a loader that found no config)

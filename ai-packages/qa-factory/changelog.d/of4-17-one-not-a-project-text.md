- one "this root is not a project" refusal (`hooklib.py`, `host_probe.py`, `check_coverage.py`, `dashboard_refresh.py`): the words are built in
  one place, `not_a_project_text`, which `require_project_at` prints, `host_probe._not_a_project` returns,
  `check_coverage.marked_root` returns and `hooklib.story_root` raises, so a person reads the same refusal from every
  caller; with an ancestor that carries `qa-factory/config.json` it names `--root <above>` only for a caller that has
  that option (`root_option`), else run from inside the project or set `CLAUDE_PROJECT_DIR`; with nothing above an
  ambient root it names onboarding and the wrong-root door together; a door only the caller has (`extra_door`) is
  added; the dashboard refresh asks the project marker through `_carries_project`
- the dashboard's refusal names its `--read-only --out <file outside the root>` door and `config_view.py` prints the shared
  text on a root with no project (a marker present yet a loader that found no config gets one sentence naming the file)
- `host_probe.py` tells the role to report the hooks as unknown only where no door but onboarding exists

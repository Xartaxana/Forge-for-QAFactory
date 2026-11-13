- one path-component test everywhere (`event_store.py`, `selftest.py`, `dependency_drift.py`): the `stale_marker` of an
  event store, a `files` key of `slow_tests.json` and a `locks[].file` of `project-dependencies.json` now call
  `hooklib.is_one_component`, so `a\b`, `a:b` and a NUL byte are refused on every OS, and `..` / `.` where a copy let
  them pass; the OH6-1 sentinel allowance shrinks to empty

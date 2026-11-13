- one path-component test everywhere (`event_store.py`, `dependency_drift.py`, `selftest.py`): the `stale_marker` of an
  event store and a `locks[].file` of `project-dependencies.json` now call `hooklib.is_one_component`, so `a\b`, `a:b`
  and a NUL byte are refused on every OS, and `..` / `.` where a copy let them pass; the runner `selftest.py` does not
  import hooklib, so its `files` key check of `slow_tests.json` uses the named mirror `_is_one_component`, pinned to
  the survivor by an agreement row; the OH6-1 sentinel allowance shrinks to that one mirror

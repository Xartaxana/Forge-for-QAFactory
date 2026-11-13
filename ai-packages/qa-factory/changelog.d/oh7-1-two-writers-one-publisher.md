- atomic writes: the dashboard page (`factory_dashboard.py`) and the coverage-migration backup (`migrate_coverage.py`) now
  publish through `event_store` (`atomic_text` and the new `atomic_bytes`) instead of their own 32-hex temp name. The
  dashboard page is now written with LF line endings on Windows (it was CRLF), a lone surrogate in it is written as `?`
  instead of raising, and its temp file is removed when the write fails; the backup is still the plan's exact bytes
  (OH7-1)

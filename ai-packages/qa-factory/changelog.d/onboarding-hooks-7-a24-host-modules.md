- refusal registry (`scripts/refusal_registry.py`): `codex_roles.py` and `host_adapter.py` join the files the A24 audit scans, and every
  raise or block of theirs that the scanner sees has a registry row keyed by its literal text, among them the two dispatch refusals of
  `inject_context.dispatch` (`check_override`, `rewritten_input`); the rows' test field names a test that drives the refusal through its
  public function. A raise of a `ValueError` subclass (`LaunchIdRowRefused` in `launch_id_keys`) is not yet seen by the scanner; no
  refusal changed its outcome or its text

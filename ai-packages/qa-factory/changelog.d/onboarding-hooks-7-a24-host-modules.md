- refusal registry (`scripts/refusal_registry.py`): `codex_roles.py` and `host_adapter.py` join the files the A24 audit scans, and every
  raise or block they carry now has a registry row keyed by its literal text, among them the two dispatch refusals of
  `inject_context.dispatch` (`check_override`, `rewritten_input`); no refusal changed its outcome or its text

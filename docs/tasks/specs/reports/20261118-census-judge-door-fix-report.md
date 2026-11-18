# t-1516 census row for window_record.py::judge_door

Added one row to ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json, after window_record.py::build:
`{"file": "window_record.py", "function": "judge_door", "class": "shape", "roles": ["qa-code-critic"], "owner": "data", "note": ...}`

- class shape: judge_door (window_record.py:1101) only compares a record path (`work/probes/product/`) and returns one of two fixed command strings; it reads no content and refuses nothing (exceptions are swallowed). Sibling: onboarding_notes.py::_refuse_door_status (shape), window_record.py::main (shape). Not xref: it reads no cross-file claim, it picks a constant.
- roles [qa-code-critic]: the door text is the code critic's `--judge` command (docstring); sibling window_record.py::main uses the same role.
- owner data: the decision is made from record structure; sibling window_record.py::main / build owner data.
- No ceiling moved (shape has none; no blocking/breach change). No code edited.

Witness: `python -B tools/registry_preflight.py check census`
```
registry preflight: census ok (36.0 s)
```
Committed on the worktree branch: see below (git log).

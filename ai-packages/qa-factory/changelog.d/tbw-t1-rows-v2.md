- `refusal_registry.py --sites --wide`: a `print(..., file=sys.stderr)` / `sys.stderr.write(...)` is a refusal site only when the next statement of
  its block is a failing `return` (non-zero or an `EXIT_*` name), `sys.exit(<non-zero>)` or a `raise`; any other stderr text is a counted
  named blind spot (a note or a progress line is not a refusal). New `check_of(entry)`: the check id `<file stem>:<id>` of an A24 entry.
  The default scans and audit A24 are unchanged.

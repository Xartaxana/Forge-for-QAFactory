- `scripts/friction.py` measures, per role session and from the role's own transcript, how many tool calls were factory bookkeeping
  and how many were refused or failed, and the seconds they took: new `call_spans` (one transcript) and `story_calls` (a story's role
  sessions, sharing one session loop with `story_friction`); every call carries two time figures, execution (`tool_use` line to
  `tool_result` line) and turn-attributed (previous transcript line to the result, a multi-call message split evenly); a call with no
  result or no readable timestamp is counted with unknown seconds and a sum says `at least N s (K calls unmeasured)`; a refused call is
  one whose result carries the host's `is_error`, split by `classify` where it names a kind, else `failed, cause not recorded`;
  `turns_of` only gains keys (`prev_ts` on a turn; `ts`, `result_ts`, `has_result`, `is_error` on a call)
- `references/friction-markers.json` gains the optional key `bookkeeping_scripts` (the factory scripts whose calls are bookkeeping, one
  `why` each); a file without it reads as `unknown: no bookkeeping list`, never as zero bookkeeping

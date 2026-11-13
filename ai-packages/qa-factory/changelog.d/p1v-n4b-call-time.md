- `scripts/friction.py` measures, per role session and from the role's own transcript, how many tool calls were factory bookkeeping
  and how many were refused or failed, and the seconds they took: new `call_spans` (one transcript) and `story_calls` (a story's role
  sessions, sharing one session loop with `story_friction`); every call carries two time figures, execution (`tool_use` line to
  `tool_result` line) and turn-attributed (previous transcript line to the result, a multi-call message split evenly among ALL its
  calls); a call with no result or no readable timestamp is counted with unknown seconds and a sum says
  `at least N s (K calls unmeasured)`; `turns_of` only gains keys (`prev_ts` on a turn; `ts`, `result_ts`, `has_result`, `is_error`
  on a call)
- A call is bookkeeping only when a Bash command INVOKES a listed script (the program an interpreter runs, or the command itself); a
  name that is only an argument (grep, cat, an editor) is not counted; a Write or Edit of a file matching a fragment pattern is its own
  row (fragment writes). A Bash command is read by the one shell reader (`hooklib` command segments, heredoc and here-string bodies
  cut out first), so a body that names a script is not a call and an apostrophe in a body hides nothing. Refused calls are the host's
  `is_error` flag and nothing else (a voluntary `--help` and a role's own text that says "is refused" are not refusals); a role session
  whose transcript cannot be read (absent, unreadable, torn, empty) is `unknown` for every row and has no call count, never 0
- `friction.SCRIPT` now accepts digits in a script name (`s5_precheck.py` was read as `_precheck.py`)
- `references/friction-markers.json` gains the optional keys `bookkeeping_scripts` (the factory scripts whose calls are bookkeeping,
  one `why` each) and `bookkeeping_fragment_patterns` (file-name patterns of the fragments a role writes for the factory's own
  forms); a file without a key, or with an empty one, reads as `unknown: no bookkeeping list` / `unknown: no fragment pattern list`,
  never as zero

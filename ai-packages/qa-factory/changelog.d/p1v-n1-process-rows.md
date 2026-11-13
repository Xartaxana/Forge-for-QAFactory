- the story driver writes two rows of its own process into `driver-runs.jsonl`: `process` `start` (package fingerprint, config hash, whether an
  answer file was given, run class) as the first thing `run` writes, and `process` `end` (the returned code, null when it ended by an
  exception; the kind of the open question) in a `finally`; they carry no session, dispatch, outcome or money key (`scripts/driver_machine.py`)
- the run class is read in one place, `driver_journal.run_class`, from `STORY_RUN_CLASS` against `references/run-record.json` (`dry`, `smoke`;
  nothing set is `live`; any other value, or an unreadable table, is `unknown` with a note); `driver_journal.run_record` is the one loader of that file

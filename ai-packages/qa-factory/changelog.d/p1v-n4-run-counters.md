- run counters (`scripts/run_counters.py`, `references/run-record.json`): `python run_counters.py --task <KEY> [--json]` reads the carriers of one
  story folder and prints the counters of the run: time rows (wall, role time with overlap counted once, conductor time, hung calls, time between
  processes by cause, driver time outside the hops), first pass against rework by the road of each resumed call (the new `rework_kinds` list of the
  run record names the roads that sent a role back to its own work; person answers, stand answers and service cuts are not rework), returns and
  role seconds per check, gate repairs, questions and repeated answers, brief sizes, friction shares and a data-quality row; an input that is
  absent prints `unknown` (or `n/a` for a run with no driver journal), never 0; it writes nothing and prints no money. The scoreboard that reads
  these counters is still to come.

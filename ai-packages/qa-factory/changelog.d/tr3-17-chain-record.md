- The driver keeps `boundary` and `last_dispatch` per thread (`story_run.py`, same names, no call site edited), and gains the chain record that a
  window's thread will run under: `Driver.as_chain(record)` / `Driver.adopt_chain(record)`, `ChainRecord`, a `chain` field on `Refusal`, and
  `ChainStream` (a `[W<n>] ` prefix for a chain thread's console lines, nothing for the main thread; not installed yet). The S5 review's close
  check now reads the critic dispatch once and hands it to both readers. On the serial road every value and every printed byte is unchanged.

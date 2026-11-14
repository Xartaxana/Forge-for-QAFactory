- the stand probe says WHY it blocks: `env_probe.probe()` returns, and `env_probe.py --json` prints, a new key `blocked_by` - one word
  per Layer-1 line, in the same order (`selection`, `env_file`, `stand_dead`, `no_address`, `login`, `login_key`, `device`; exit 0 is
  an empty list); the four existing keys and the words of every Layer-1 line are unchanged. `env_probe.blocked_by_of(text)` is the one
  reader of the probe's text for those words (empty or crashed text is `unknown`, the `ENVIRONMENT: not configured` line is
  `not_configured`)
- the driver says "did not answer" about a stand only when the probe's evidence is a dead stand: the S5/S6 stand question
  (`stand_question_text`) has four sentences - did not answer, answers but the login recorded for the project did not get in (with a
  retry option that names the login), could not be checked because its setting is missing or broken, and "I could not check the stand"
  for an unknown word, an empty list or a crashed probe; the S0 warning, the S1 stand line (`phases/s1.md`) and the refusal-seam
  question now say "did not pass its check"; stories that already carry the old warning keep it

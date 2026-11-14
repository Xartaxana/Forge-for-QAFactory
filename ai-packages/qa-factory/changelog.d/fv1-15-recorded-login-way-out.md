- the stand check words what the recorded sign-in came to: `env_probe.py` names the answer in the Layer-1 login line (the address did not look like a sign-in,
  its answer did not show whether a sign-in is there, no answer, a server error, a limit on requests, the project's own command did not get in), reads it back
  with `login_answer_of`, and records it as `login_probe.answer` (receipts the probe builds itself say `answer: not_tried`, `source: access`); every such line is
  still the one word `login`, and a line with no answer or an unknown one reads as before
- a recorded sign-in that is not the stand's way in has a way out: the stand question offers `find the way in` (once per stand per story), which runs
  `project_decisions.py stand-login` - every way the factory knows is tried (`stand_access.try_roads`), the first that signs in is recorded as
  `environment.access` on the person's word (receipt kept, so the story's revert still works); after one search the question names the onboarding that asks
  how the project signs in, and the stand question words a stand that failed on its side or limits requests apart from an account that was refused
- `stand_health.py` reads the login record through `stand_access.recorded_login` (a project's own sign-in command records no HTTP code: `status: 0` now reads as
  proved), says the answer in plain words, and `login_remedies` gains the row L0 for a wrong door; an old record with no `answer` reads as before

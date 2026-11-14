- stand sign-in says WHAT one attempt came to (`scripts/stand_access.py`): every receipt carries `answer` (`in`, `credentials_refused`,
  `fields_unconfirmed`, `body_shape`, `wrong_door`, `unjudged`, `throttled`, `stand_error`, `no_answer`, `did_not_finish`,
  `command_failed`, `command_missing`, `not_tried`) and `source` (who recorded the way); `in` only on positive proof, every other HTTP answer
  is worded by the new `login_answers` rows of `references/stand-answers.json`, and an answer the table cannot place is `unjudged`, never a refusal
- access kinds `form_login` (a csrf step, one submit, a session step; the forms are rows of the new `references/login-roads.json`) and
  `ui_only` (the person's word that the tests sign in through the UI only)
- `python scripts/stand_access.py --project-root . --roads --json` tries every way the project could sign in by and reports each answer;
  it writes nothing and spends at most the attempt budget of `login-roads.json` on the account
- a session token counts only when it is a non-empty string (`true`, a number or a list is no token); a recorded `login_probe.status`
  outside 100..599 is refused by `--check-environment`
- a config written by this version (`form_login`, `ui_only`, `login_probe.answer`) is refused by `--check-environment` of an older installed
  plugin: install this version on every machine that runs the project's factory

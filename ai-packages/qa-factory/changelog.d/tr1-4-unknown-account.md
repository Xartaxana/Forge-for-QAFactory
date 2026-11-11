- Walk lanes with an account key (`story_run.py`, `walk_timing.py`): an `env:<login key>` account is looked up in the stand's records
  (`credentials_by_role`) by its login key, the way `--as` reads them; exactly one role with the key opens the walk session. A lane whose
  accounts cannot open a walker session - no pair, two roles with the key, a role the stand does not list, no two-key note, an account no
  machine can check, more accounts than a walk holds, a request that cannot be read - is no longer walked on the old road and no longer stops
  the run with a question: each of its cases is recorded `not walked: <reason>` in the story's words, one finding is filed per lane, and the
  next lane walks. Only a failed session open takes the old road. `walk_timing.py` leaves the items the driver marked `walk_old_road` out of
  every figure and names them, with or without a timed walk.

- the S5 brief carries the first look in substance (`scripts/brief_pack.py`): the automator's block now lists every item of a row
  (screen, steps, locators, routes, samples, data) one line per item, each item cut at 400 characters with `...` and the block then
  ends `whole: work/first-look.yaml`; on a window dispatch only the window's own requirements are listed, with no count cap, and one
  line names how many requirements of the record are outside the window; the plan, legacy and unknown dispatches and every other
  reader keep the 12-line cap and the `+N more` pointer (FV1-28)
- a missing first look is a gap, not a fact (`scripts/brief_pack.py`): the briefs of S3-S7 and the file line of
  `work/first-look.yaml` say "a GAP - what the stand shows is not known ... it is not a fact that there is no stand" with the
  reason, and a clause for the reader (look yourself where the stand is needed, or name it as a gap); no line names a script
  (FV1-28)
- the first-look walker's brief says, when the check of the stand at the start did not pass, that the check is a guess of code and
  not a fact, and that the role finds the way in itself (FV1-28)
- when every row shown to the case designer or the automator is a row the walker could not reach for want of a way in, the brief says
  so in one line with each reason, instead of "no row names such a path"; the two closed words are data (`first-look-statuses.json`,
  key `gap_rows`) (FV1-28)
- the briefs of the first look's readers and the walker carry the way in this story's own first look found (`sign_in` of the
  record): one line, surface, actor, address, selectors, steps, never an account value, cut at 600 characters with a pointer to the
  record; a stale or empty record gives no line (FV1-28)

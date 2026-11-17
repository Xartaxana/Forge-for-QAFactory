# ARCHITECT_START — the start checklist of an Architect session

Loaded only through the SessionStart pointer `ARCHITECT SESSION: start with PROCESS/ARCHITECT_START.md; queue
docs/tasks/architect-queue.md (<N> open)`, which is printed only when the session's function is `architect`. No other
session reads this file (a non-Architect session never pays boot bytes for the Architect). The Architect is never a
subagent: the owner switches the session model.

Ordered steps:

1. **Tier check.** The MODEL line says function `architect` (exact or `family match`). If not, this file does not
   apply; stop.
2. **The owner's reason first.** If the owner switched with a question, that question is item 0; the steps below run
   after it is answered, or in parallel only when cheap.
3. **Architect queue.** Read `docs/tasks/architect-queue.md`; every `- [ ]` item gets an answer, a decision, or an
   explicit "оставлено: <почему>".
4. **Escalations to the Architect.** A named command, no new event and no SessionStart reader (the open-dispatch
   reader cannot serve: `escalated` closes a task there). Run
   `git -C C:/QAFactory/forge-repo grep -n "\"event\":\"escalated\",\"agent\":\"architect\"" -- logs/journal/`
   (the pattern is the journal text `"event":"escalated","agent":"architect"`; the one writer emits `"ts"`,
   `"event"`, `"agent"` in this order). Every hit dated after the previous
   `reviewed_through` marker must match a queue item (open or struck) by its task id; a hit with no item, or an item
   whose task id has no hit, is a finding. Error direction: a line written in another field order (by hand, against
   hygiene pt.5) is missed by the grep; the reverse direction (item -> hit) and calibration check 49 (c) catch that
   side.
5. **Mechanism commits since the last Architect review.**
   `python -B tools/mechanism_gate.py --list --since <reviewed_through sha>` prints one line per commit touching a
   mechanism path (merges against first parent): `<sha> <committer date> <tier: values> <subject>` and its mechanism
   paths. The "since" value is the `reviewed_through` field of the newest `calibrated` line; none yet means the date
   of the stream-L commit (the Architect landing); if no review has happened yet and that commit has not landed,
   there is nothing to review before the Architect landing. For each commit: OK, or a finding / `defect_found` against the accepting
   task. Review for: the axis block truthful, the rule placed at the right level (rule 9), the detector registered
   (rule 10 c), D-entries consistent. A defect is a `defect_found` (agent = the accepting tier, `ref` = the original
   task) or a finding in `plans/piles/forge/findings/` with its batch row.
6. **Calibration.** If the SessionStart `Last calibration` line says overdue (more than 7 days), run the weekly
   calibration (`PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`), which includes step 5.
7. **Boot budget.** The `BOOT BUDGET` line: over WARN, the boot-diet backlog item goes to `docs/tasks/lead-queue.md`
   (the Architect does not trim boot files itself unless the owner says so).
8. **Close the review.** Write the marker:
   `python -B tools/journal_write.py calibrated --reviewed-through <sha of the last reviewed commit> --notes "<period, counts>"`
   (the `reviewed-through` option is the marker the next review starts from).

The Architect's absence never stops Lead work; Fable unavailable is not a Lead degradation (queue items wait, the
owner is told once).

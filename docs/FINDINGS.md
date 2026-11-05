# Findings

Registry of observations from operating the supervised-delegation architecture in this repository.
Format and the applicability-question norm: `docs/FINDINGS.template.md`.

---

## F-1 -- Boot Report skipped when the operator's first message is a work order

**Date:** 2026-09-29.

**Observation.** Session of 29.09 (15:56): the SessionStart hook injected Boot Layer A (closing line
present) and told the session to read Layer B; the session read CURRENT_CONTEXT.md, but the
operator's first message was a work order ("делай изменения которые нужно завершить до прогона
тестовой стори"), and the session went straight into recon dispatches without emitting the Boot
Report (PROCESS/BOOT_REPORT_PROTOCOL.md rules 1-2). The operator noticed and asked why.

**Class.** A mandatory session-entry output is skipped when the first operator message carries its
own task, because the task is read as superseding the protocol instead of following it.

**Applicability question.** Did a session that was required to emit a fixed entry artifact omit it
because the first operator message already asked for other work?

**Consequence.** An explicit work order may satisfy rule 4 (the STOP), but never rules 1-3 (the
report itself); the report is emitted first, then the ordered work starts in the same turn. The
detector today is only the operator's eye; nothing in the SessionStart output or a hook checks that
a report was emitted.

**Status.** Resolved by the operator's word (29.09, 16:20): no machine detector; while the Boot
Layer A injection is in place, the report stays on discipline alone, the detector is the operator.
The report was emitted retroactively in the same session (16:13).

---

## F-2 -- Three rejected attempts of one task, all traced to the Lead's own amendments

**Date:** 2026-09-29.

**Observation.** t-023 (B-002 A, the live receipt) was rejected three times, each `failure_class: spec`
(journal: rejected attempt 1 after critic t-030, attempt 2 after t-035, escalation to Opus, attempt 3
after t-048; attempt 3 alone ran ~3.5 h on Opus). Each defect was in a Lead amendment written between
attempts, and in the draft the Lead accepted: (1) the designer's draft NAMED the edges (rows 6/7 of
the t-016 edge list), but chose a wrong behavior -- current bytes only as a tie-break, so a receipt on
OLD bytes still counted; the Lead accepted it without checking what "a receipt for other bytes" must
mean; (2) "MEASURED BYTES" assumed one meaning for
`test_content_sha`, while the package carries two (raw file sha vs run fingerprint) -- an unmeasured
premise; (3) Amendment 3 made the per-line `is_prose` heuristic, built to ADVISE a re-review, the
load-bearing GATE for "the check is live", so real code edits passed as comments. Every amendment went
straight to the builder; none had a critic-on-plan; a new owner decision (D-0017/D-0019) was folded into
the running task, widening it mid-flight.

**Class.** A retry amendment is treated as "a continuation of the existing spec" (rule 2), so it skips
the plan review a fresh spec of the same weight would get; the amendment changes semantics (what a field
means, what a predicate decides) on an unmeasured premise.

**Applicability question.** Did an amendment to a running task change the MEANING of a field, a
predicate or a gate, and reach a builder without a measurement of the premise and without a plan
review?

**Consequence (practice from 29.09).** Before an amendment that changes a meaning goes to a builder:
(a) one measurement of the premise on real data (command hygiene 6a); (b) a critic-on-plan of the
amendment text (rule 3 already requires it for specs over ~30 min of work -- an amendment is a spec);
(c) a reused function gets its failure direction stated in the spec (advice vs gate), with the
adversarial inputs written by the Lead before dispatch; (d) a new owner decision opens a new node, it
is not folded into a running one. Detector: the journal -- two `rejected` events with `failure_class:
spec` on one task_id are this finding recurring.

**Status (F-2).** Carried as a project rule: PROJECT.md "Как принимается изменение пакета", item 6 (loaded
into every session through the CLAUDE.md import; reaches other developers with the commit). Discipline,
detector = the journal (spec-class rejections per task at calibration).

---

## F-3 -- Where a development day's time went (session of 29.09)

**Date:** 2026-09-30.

**Observation.** Measured by two scratch scripts over the session's own transcripts (26 subagent
transcripts + the main session; carrier: the session scratchpad `lead_session_audit.py`,
`lead_session_audit2.py`). Main session 8.8 h wall; subagents 29.7 h summed wall, 19.2 h of it
inside tools. Of the tool time: waiting on background test runs by polling loops ~4.5 h;
`test_story_run.py` ~3.3 h (about 8 min a run, also rerun by critics whose verdict did not need it);
mutation runs on package copies ~2.0 h; neighbour sweeps ~1.1 h; one mistaken full selftest 0.2 h;
Edit/Write calls ~1.9 h in subagents and 0.3 h in the Lead (~7 s a call, the PostToolUse hooks).
Journal 29-30.09: 58 delegated, 15 critic dispatches, 6 rejected, and almost every builder task
needed a second (fix) round. Section 0 grew mid-day by owner decisions D-0017..D-0020 (run budget,
B-147..B-152) and the AGENTS.md task.

**Class.** The cost of a change is dominated by verification runs that repeat (whole sets after
each edit, several sets per mutant, slow suites rerun by reviewers) and by rework rounds, not by
the model's own work (~0.5 h of model time between tool results in the longest Opus task).

**Applicability question.** Does a task's tool time exceed its model time several times over
because the same test sets run repeatedly?

**Consequence.** builder-rules item 7a and PROJECT.md item 2 (one sweep at the end, one test file
per mutant); PROJECT.md item 6 (critic-on-plan for meaning-changing specs, fewer rework rounds);
further proposals in the reply of 30.09 (test_story_run speed, critic rerun scope, hook latency,
commit cadence).

**Status.** Open: proposals with the operator.

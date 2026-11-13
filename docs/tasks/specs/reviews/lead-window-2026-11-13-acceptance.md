# Acceptance of the degraded window 2026-11-12 18:18 .. 2026-11-13 10:20 (full Lead, Fable)

The window was coordinated by Opus (journal `lead_degraded` 2026-11-12T18:19:50, retroactive boundary 18:18). The line of
17:38:45 belongs to the LR2-1 operator session, not to this one; this file does not accept that session's work.

## What the window holds (counted from logs/journal/dev1.jsonl, events with ts >= 2026-11-12T17:38:45)
539 events: 252 delegated, 198 accepted (57 on a critic verdict, 63 queued-to-lead, 78 from above), 34 rejected,
46 dispatch_skipped, 5 defect_found, 2 escalated. Merged to main: PR #5 .. #15 (waves 1-10).

## What the Lead read itself
- **OH8-7** (t-329, critic t-334): the staged diff of `refusal_registry.py`, the census `about` and ratchet line, the
  SIBLING_MAP axis-18 row and the commit message. Accepted and committed as 0bc7b1d on wip/oh8-7 with `tier: claude-fable-5-2`.
  Census test on that tree: `=== judgment_census: 26/26 ok ===`.
- **Ratchet raise blocks_overrides 8 -> 10** (b794bd2, t-189): both hand marks read (load_personal_path: raised and caught
  inside; epoch_of: guards a caller's argument). Confirmed.
- **t-344** (CI fix of wave 11): one-line test fix read; the cause (a spy kept by a by-name import) is a test defect.
- The journal's event table and every `queued-to-lead` note of the window (63 lines, read as a list).

## What is accepted by outcome, not by a re-read
The 63 queued-to-lead accepts are designer specs and critic verdicts. Where their nodes are already on main, they went
through a builder witness, a critic verdict on the diff and a green batch canon (waves 1-10); the Lead accepts those by
that outcome and did not re-read each spec. This is a stated limit, not a claim of a full review.

Still open, and reviewed when their work lands: t-321 part B / t-326 / t-334 (OH8-7: now committed), t-322 / t-327 / t-341
(OH8-4, wave 12), t-324 / t-328 / t-339 (OH8-2a/2b/6, wave 11), t-337 (OH8-7b draft: forks decided below).

## Lead decisions taken at restore
- OH8-7b fork F1 = (a) `SUBCLASS_UNIT_FILES`; F3 20-40 functions per node; F4 one critic pass per pair of nodes, the last
  node its own pass. Spec: designer t-346.
- The coordinator's own decisions of the window ("решила сама" lists of the 09:17 and 10:11 snapshots) stand; none is
  reverted. They stay on the owner's morning list, where the owner can undo them.
- Take friction (broad zones of onboarding-forge/1,2): the road is closing finished batches, not editing a frozen zone;
  scout t-345 measures what each of the ten taken batches still owes.

## Not done here
- The SIBLING_MAP axis-8 row (critic t-339 F9) and the t-324 text on `landing_name`: they land with wave 11's follow-up.
- Calibration items of the window (heredoc edits, a dispatch without `handoff:`, a builder claiming a run it did not see)
  go to the next weekly calibration from the journal.

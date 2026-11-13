# Weekly Calibration Protocol

An executable checklist for the weekly calibration run. Loaded only
for the duration of the run, not at boot. Without a single canonical
checklist, checks tend to scatter across separate decision entries
covering rules 1–10, and the calibrator ends up re-deriving them each
time; this file is their canonical home. A new mechanism that
promises "calibration will catch X" is obligated to add a check here
in the same commit — otherwise the promise is empty (a mechanism with
no registered detector is not a mechanism, it's a wish).

Input data: logs/routing-log.jsonl (across every deployment you run),
usage records (cc_usage) via tools/usage_report.py, the git history
for the period, and diffs to DECISIONS.md.

## Checklist (mechanism → violation → how to check)

1. **Rules 1/2/8 — silent self-exclusion.** Main sessions in the
   usage records with a large volume of reads/edits, for which the
   same period shows neither a `delegated` nor a `dispatch_skipped`
   event. Source: usage report + journal.
   (b) WITHIN-SESSION RECURRENCE of the "first move free" self-execution
   waiver (rule 8): `dispatch_skipped` events of ONE session are
   grouped by reason CLASS in ts order; the SECOND and later event of
   the SAME class in the SAME session is a VIOLATION IN ITS OWN RIGHT,
   independent of whether that reason class has also crossed any
   across-window repeat threshold elsewhere (a separate signal, not
   replaced or overridden by this one). Reference class: "the operator
   is waiting / an interactive request blocks the move". SESSION
   BOUNDARY: the transcript is the final arbiter; a cheap first pass
   is self-declaration — every `dispatch_skipped` event from the
   second one of its class onward in a session is obligated to carry a
   repeat marker in notes — the closed lowercase literal `repeat:`
   (FG7-21; `tools/calibration_counts.py` counts it per agent and
   prints every unmarked chain of 2+ events in one window as a
   "candidate repeat" row), making the violation visible by grep without
   touching the transcript. Both layers are checked: the transcript
   scan is the final arbiter, the notes marker is the cheap first pass;
   a second-or-later same-class event with no marker is itself a
   violation (self-declaration failed). An empty window (no skip
   events, or no class repeated within one session) is noted
   explicitly — "no within-session recurrence".
   (c) DISPATCHER THRESHOLD OF THE DESIGNER (the detector for rule 2's
   designer-drafting threshold clause): every WRITING `delegated` of
   the window whose spec carries 3 OR MORE numbered items, OR touches
   3 or more files (counted by `dispatch_manifest.designer_threshold`
   on the dispatch text — the gate refuses such a dispatch without a
   `designer:` line; a `designer: skip` line without a matching
   `dispatch_skipped(agent=designer)` is the violation; a pointer-spec
   dispatch, count 0 by construction, is judged from the diff of the
   accepted work), is obligated to carry EITHER a
   paired `delegated(designer)` before it, OR a
   `dispatch_skipped(agent=designer)` with a named reason. Neither of
   the two = a silent absorption of the function by the coordinator —
   the same violation class as self-reading instead of dispatching
   scout. A measure alongside, for TREND not violation: the count of
   designer dispatches in the window against the count of writing
   dispatches above the threshold. Track this ratio over time: a rule
   can exist on paper and still see zero real use until routing
   default forces it — a rising share is the rule's own goal; no rise
   while the rule is live is a leak, a finding.
   (d) THE "RESUBMISSION = CONTINUATION OF THE SPEC" EXCEPTION (rule
   2's own carve-out) — detector: a `delegated` with `attempt`>=2
   under the SAME `task_id` after a `rejected` is a continuation of an
   already-written spec; a designer dispatch and a
   `dispatch_skipped(agent=designer)` are NOT required for it, and
   threshold (c) above does not project onto it. LEAKAGE OF THE
   EXCEPTION: re-badging the continuation under a NEW `task_id` — a
   window task whose subject and `owns` set match a just-rejected task
   (adjacent `ts`, the same path owner), with no paired
   `delegated(designer)` and no `dispatch_skipped(agent=designer)` —
   is a leak of the exception (the norm bypassed by swapping the
   task_id). REVERSE LEAKAGE: a skip event whose reason names
   "resubmission" as its class means the norm is misunderstood —
   either it really was a new task (a designer dispatch was owed and
   the event was filed wrong), or the event itself is superfluous (the
   exception already frees a resubmission with no events at all);
   either case is a finding. An empty window (no rejected-then-
   resubmitted tasks under threshold (c), no re-badging under an
   adjacent task_id, no skip events of class "resubmission") is noted
   explicitly — "no resubmissions".
2. **Rule 3 — critic on large diffs.** Commits in the period with
   over roughly 100 changed lines, accepted with no
   `delegated(critic)` and no "critic: skipped, <reason>" note in the
   accepting `accepted` event. Source: `git log --stat` + journal.
   CUMULATIVE SUBCASE (R13-g of CLAUDE.md): ONE critic pass per TOPIC,
   not one per part (Cost gates, rule 12) — this check reads COMMITS:
   a commit over the threshold whose own `accepted` has no critic
   entry is covered when the critic pass of its topic names it; a
   second critic pass on a part of an already-reviewed topic is a
   Cost-gates finding, not a credit (whether "one topic" holds is a
   semantic call for the calibrating Lead).
3. **Rule 6 / the escalation rule.** Two `rejected` events for the
   same task at the same tier with no subsequent `escalated` = a
   violation. An `escalated` with no `rejected` trail = a question
   about the self-declaration. This is checked mechanically: events
   for one task are linked by `task_id`, attempts by the `attempt`
   field; an event from the task_id-mandatory set with no `task_id`
   is a violation in its own right (the typed-fields rule).
4. **The self-declared-model discrepancy check.** The `model` field
   on delegated/escalated/accepted/rejected against the actual
   execution models in the usage records; a discrepancy is itself a
   calibration event.
5. **Degradation.** Every `lead_restored` carries, in its notes, a
   review of the window (what was reviewed, the verdict; an empty
   window is noted explicitly). A `lead_degraded` with no matching
   `lead_restored` by the session boundary — cross-check against the
   journal's last event. Cross-check the actual models of Lead
   sessions in the period (main chains in the usage records, NOT
   sidechains) against window coverage by matched
   lead_degraded/lead_restored pairs: Lead-tier activity on a model
   below the top tier, outside a declared window, is silent
   degradation — a failure of both in-session checkpoints (this
   extends check 4 from workers to Lead itself; retroactive pairs are
   found via a note in notes).
6. **Acceptance.** Every completed `delegated` has a matching
   `accepted` or `rejected`. `accepted` for scout dispatches carries a
   note of a targeted spot-check (negative claims — mandatory).
   Acceptance from above: for every `accepted`, cross-check the tier
   of the accepting session (usage records, main chain at the time of
   the event) against the tier of `agent` — strictly above: fine;
   equal or below: notes must carry input from a tier above (a critic
   verdict) or a "queued for the full Lead" note, otherwise it's a
   violation (the session self-certifying). The "critic: skipped"
   waiver is legitimate only for an acceptor above the executor —
   read this together with check 5 (degradation windows).
   Environment-negative claims: negative claims ABOUT THE ENVIRONMENT
   in reports/verdicts of the window (no service/command/file) are
   valid only with a positive check using the canonical form (command
   hygiene, point 6).
7. **Journal vs. transcripts, both directions.** A sidechain in the
   usage records with no matching `delegated` event = an
   undocumented dispatch; a `delegated` with no matching sidechain =
   a phantom event.
8. **The four-questions-per-mechanism rule.** New DECISIONS.md
   entries for the period contain answers to (a)/(b)/(c)/(d), and the
   (c)-answer is REGISTERED: a check in this protocol added in the
   same commit, or an explicit external detector named in the
   decision's own text. An unregistered detector is a wish dressed as
   a mechanism — write it up as a finding. The (d)-answer names the
   enforcement layer: what triggers the mechanism and what code sits
   on the execution path, or an explicit "on discipline alone" line
   with a named leak detector; a missing (d)-line, or a
   discipline-only answer with no detector, is a finding. The (b)
   enumeration is checked by MACHINE over the window (F5-6, 15.10.2026):
   `python tools/mechanism_gate.py --audit --since <window start>` names
   every axis line whose label is not the map's heading key (the gate
   refuses them at commit; from 2026-10-16 an unlabelled line is a
   mismatch too) — a non-zero exit is a bypass (a rewritten, web-edited
   or `--no-verify` commit), each line a finding; the count of
   unlabelled lines before the date is the baseline (392 at the first
   reading, window from 2026-10-07). A
   recognition audit: commits for the period, across every repo you
   run this in, are scanned for mechanism-shaped edits with no
   four-questions block and no matching decision entry (a duty or
   machine check added outside DECISIONS.md is an "unrecognized
   mechanism"); the verdict is a judgment call for the calibrating
   Lead — the gate's net only supplies candidates; anything found is
   a finding, plus a retroactive four-questions writeup. The
   (b)-answer is an axis-by-axis ENUMERATION against the current
   SIBLING_MAP (prose saying "axes are covered" is not an answer);
   gate liveness = `git config core.hooksPath` pointing at
   `.githooks` in every repo you run this in; mechanism-shaped commits
   for the period are spot-checked for the axis block (the only way
   around the gate is `--no-verify` or an explicit waiver line);
   "axes: not a mechanism" lines for the period are audited for
   honesty — a waiver used on a substantive mechanism is a violation.
   Tier declarations: `tier:` lines on mechanism commits for the
   period are reconciled against the sessions' actual models per your
   usage records/transcripts (same reference as check 5) — a lead-tier
   declaration written by a below-lead session is a violation (the
   recognized-then-did-it-anyway class: the gate forces the
   declaration, this check judges its truth); "axes: not a mechanism"
   lines are also audited as a potential bypass of the tier
   requirement (a substantive mechanism relabeled to avoid declaring
   the tier).
9. **SIBLING_MAP — class-wide completeness.** Commits that close a
   finding name the axes it touches; "new axis for SIBLING_MAP" lines
   noted anywhere in your logs get folded into the map.
   (b) SWEEP INSIDE THE ARTIFACT (the sweep-the-artifact-first rule,
   CLAUDE.md rule 9). Every window finding that names a CLASS (a
   findings log, critic verdicts, journal event notes) carries an
   enumeration of its own artifact's neighbors with a verdict on each,
   or an explicit line "no neighbors: <why>". Either form missing is a
   window finding in its own right. A cheap first pass: grep for the
   enumeration marker, with a positive control of the same form; the
   final arbiter is reading the entry itself. FORMALITY DETECTOR: an
   enumeration where EVERY neighbor gets "not applicable" with no
   statement of what distinguishes that neighbor from the found
   instance is a rubber stamp, and a finding in its own right. An
   empty window (no class-named findings) is noted explicitly.
10. **Growth of live files.** Line counts of the boot-path files (the
    files BOOT.md's boot sequence reads, plus CLAUDE.md and
    CURRENT_CONTEXT.md), plus docs/SIBLING_MAP.md (the map is
    supposed to stay small); compare against the previous run (the
    numbers go in the `calibrated` event's notes). Monotonic growth of
    a live file = a violation (closed material not being archived).
11. **Rule #1 applied to the routing machinery itself.** Routing
    overhead measured from data, not estimates: the share of Lead-tier
    tokens spent on journal/acceptance/spot-checks/specs, against the
    cost of the delegated work itself (usage records: main session vs.
    sidechains for the period). If the mechanism's overhead is
    systematically comparable to the work it routes, that's evidence
    for simplifying the mechanism — by a decision, not by quietly
    ignoring it. Also here — the synchronous-dispatch check: window
    dispatches run synchronously are spot-checked against a
    justification in the delegating event's notes (rule 7: synchronous
    only when the next step depends on the result AND no other work is
    pending); a sync dispatch with no justification is a finding.
    Also here — the size of the SessionStart hook's output (Rule #1
    applied to "reality piped into context"): measure
    `echo '{}' | python tools/session_context.py` with a byte/line
    count, both numbers going in the `calibrated` event's notes next
    to the check-10 counts; monotonic growth run over run with no
    decision behind it is evidence for simplification — the same
    class as the overhead check above.
    Also here — WARN LAYER DENSITY (extension from a single hook's
    output size to the load of EVERY warn layer). Run
    `python tools/warn_density.py --window-start <ts of the previous
    calibrated> --window-end <ts of this run>` and record, per layer,
    its calls/achievable share (or the honest "n/a (population not
    declared: <reason>)" line for a layer whose registry entry has no
    measured `reachable` kind) plus the rate-per-100-tool_use number
    (the one base comparable ACROSS layers) in the `calibrated` event's
    notes. Layers and carriers: GIVEN-PATH, ROLE-TYPE, FRESHNESS WARN,
    WRITE-QUOTED, DOD-QUOTED, MANIFEST-QUOTED, PATH CHECK --
    tools/dispatch_gate.py; MANIFEST-SKIP, MANIFEST-UNCHECKED --
    tools/dispatch_manifest.py; OWNS OVERLAP, BLIND_OWNS, QUOTED_OWNS --
    tools/owns_gate.py; TIER ECHO, WITNESS ECHO, TS DRIFT, ESCALATION,
    NOTES LEN, R3 MIRROR, JOURNAL ECHO -- tools/journal_echo.py; NEGATIVE LINT --
    tools/negative_lint.py; Negative
    claim -- tools/claim_control_gate.py; Search returned nothing --
    tools/search_control_gate.py; Command hygiene -- tools/
    hygiene_gate.py.
    LIST IS OPEN: a live layer missing from this list
    is a finding about THIS CHECK, not about the layer; a layer NAMED
    here but missing from `tools/warn_layers.json` is a finding about
    the registry (`warn_density.py`'s own `--check` mode surfaces both
    directions as its reconciliation section). A layer stably marking
    tens of percent of its own achievable population is a finding: not
    "the layer is strict", but a mechanism defect, because a warn that
    dense trains the reader to ignore it. No share threshold is set in
    advance -- the run's own judgment names one; the OBLIGATION is to
    name every layer's share as a number (or the honest n/a), not to
    hit a target.
12. **SIBLING_MAP liveness.** Every concrete path named in the map
    exists; the rules/mechanisms it names are still live. A dead path
    is a violation of the map's own same-commit-maintenance rule.
    Repeats in the period (a defect of an already-fixed class
    recurring outside the map's listed spots) get written up as
    findings about the map itself, and the axis gets corrected. If
    you keep decisions as an index plus a full-text companion file,
    the count of entries in each must match; if you keep a single
    DECISIONS.md, this half of the check doesn't apply.
13. **Evidence-based acceptance (both directions), typed fields.**
    (a) Every `accepted` for a builder dispatch carries a `witness`
    field — the actual output of the verification run (command +
    result); `accepted` for builder work with no witness is a
    violation. (b) `defect_found` events reference the task_id of the
    original `accepted` via the `ref` field; the false-accept rate by
    tier (defect_found / accepted for the window) is computed and
    written into the `calibrated` event's notes; a systematic
    false-accept rate for a tier is evidence for moving that tier's
    table status DOWN (Update Rule 1). (c) Every `rejected` carries a
    `failure_class` (spec / capability / recon / tooling); a missing
    class is a violation (check together with check 3). Counts for
    checks 3 and 13 are produced by `tools/calibration_counts.py`: the
    script prints CANDIDATES, and the verdict is left to the
    calibrating Lead. The counting script's own failure detector:
    tests in the canonical suite run; a baseline cross-check (the
    numbers from your first manual count are recorded in a
    `calibrated` event's notes and reproduced by the script on later
    runs); on every run, Lead spot-checks 1–2 counts against the
    journal by hand; schema drift is caught by a test that keeps the
    counting script's constants in sync with the journal validator.
    (d) A systematic `failure_class=spec` for a tier signals
    dispatches with no DoD; check the Lead's recent specs for
    acceptance criteria plus a verification run AND for the context
    manifest (a writing dispatch with no "given"/"owns" is a leak of
    the dispatch-context-manifest rule); since 2026-09-30 the header
    form of rule 11 (table R11-f) is checked by
    tools/dispatch_manifest.py at dispatch time, so a `rejected` with
    `failure_class=spec` for a MISSING manifest item after that date
    is a leak of the gate itself (a finding), and a high
    MANIFEST-SKIP or MANIFEST-UNCHECKED density (check 11) is the
    gate being walked around; a systematic
    `failure_class=recon` on builder signals an insufficient "given"
    basket; "needed beyond the manifest" report lines are direct
    telemetry of the same (piling up → the Lead's baskets are
    systematically thin).
    (e) Task_id integrity: no duplicate task_ids between unrelated
    tasks, across every journal you run. An id is read by its
    identity (`<id>@<label>`): logs/journal-segments.json declares
    which journal lines came from another clone under a label, and
    tools/journal_keys.py is the one reader of that declaration
    (B-402); an id that collides across segments is two tasks, not a
    duplicate. A known-duplicate id
    recorded in the journal counts as TWO tasks in every check-3/13
    count from then on (note it on the following event; don't rewrite
    history).
    (f) Timestamp honesty: spot-check event timestamps for the window
    against an external clock (a request database / usage records /
    git log — sources written by code, not narrative); an
    out-of-order or non-monotonic timestamp within a session is a
    violation (the `ts` field is read from the clock right before
    writing, never from the session's own narrative). A known past
    timestamp error stays un-rewritten; for any timeline count that
    spans it, take the real times from the correcting event's notes.
    (g) SessionStart hook liveness: the hook fails open (if it breaks,
    it warns and exits 0, so sessions keep running without "reality
    piped in"). Check: 1–2 transcripts in the window show a
    "NOW: ... (local system clock)" line at session start; its
    absence means the hook is broken or unregistered — a violation.
    The same check catches a failed startup preflight: a new
    `rejected`/`failure_class=tooling` from a provider quota error
    while `tools/preflight_quota.py` exists means either something
    bypassed the script, or the script's own math has a leak — work
    out which. The hook's MODEL line is a harness-supplied
    declaration, not a measurement, and its wording says so: liveness
    also includes a "declared by harness, not measured" marker on
    that line — the marker disappearing after a hook edit is a
    regression. Reconciling the actual tier against reality is check
    5's job; this subcheck only verifies the declaration's wording
    stays honest. AUTO-BOOT EMISSION CLOSING LITERAL (coordinated with
    the session-hook node's own delta): the same window transcripts
    checked above for the "NOW: ..." line are also checked for the
    boot hook's CLOSING line for its layer-A emission — a count of
    files/lines/bytes taken BY EMISSION (what actually got written to
    stdout), not by what exists on disk; the closing line's absence on
    a transcript that otherwise shows a live boot is the same class of
    violation as (g)'s own "NOW: ..." absence — a truncated emission
    with no closing count is indistinguishable from a healthy one
    without it. On a fresh install with no BOOT.md yet (layer A empty),
    the honest "layer A empty" line takes its place — silence in
    either world is the violation, not the specific wording.
    (h) traffic_kind honesty: a spot-scan of the window's requests for
    the signature of an unmarked generator — a multi-alias batch in a
    single tick (several models sharing a millisecond-precision ts)
    AND/OR tiny token counts (total < ~100) carrying
    traffic_kind='real'. Found → identify the generator, add a
    self-tag, and correct the mistagged rows loudly by an explicit
    Lead decision (rows named + rationale); a silent after-the-fact
    correction with no commit/journal record is itself a violation of
    this check.
    (i) Phantom dispatches: an open `delegated` window (the task_id's
    last lifecycle event is `delegated`, with no matching
    accepted/rejected/escalated) that outlives the session that opened
    it is a phantom candidate — reconcile its `worker_ref` against
    transcripts / the task list (did the worker actually exist?); a
    `delegated` line with no `worker_ref` once the field is
    validator-enforced is itself a violation (the validator should
    have blocked it — something bypassed the commit-time gate);
    spot-check 1–2 window `worker_ref` values against a real worker (a
    sidechain transcript, a job log).
    (j) NARROWED WITNESS SCOPE OF A PARALLEL NODE (rule 4). For every
    group of window `delegated` entries that ran CONCURRENTLY
    (overlapping delegated…accepted windows with different
    `worker_ref`s), check whether the DoD required TWO OR MORE workers
    of the group to each run the SAME full canonical run
    (command hygiene, point 1). Requiring that is a spec defect of the
    DISPATCHER, even when the runs happened not to conflict that time.
    DATA SIGNATURE: the `witness` field of two or more concurrent
    builder acceptances carries the output of the FULL canonical run
    instead of a narrowed target. Exactly ONE full canonical run is
    legitimate per window — the coordinator's, AFTER the branches
    converge — identified by a "BATCH CANON" label in the `witness` of
    the batch's LAST `accepted` event (rule 4 names this the carrier);
    a second or later full run in the `witness` of the same group is a
    violation. SECOND SIGNATURE: a parallel node's `witness` NOT
    covering what `scenario_walk.py --witness-for <its owns>` prints (rule 4)
    (the per-command file where the tests are split; the rule says
    "narrowed BY OWNS", not "narrowed to whatever the node
    touched") is the same class of spec defect, even when the missed
    path wasn't touched by the node's diff. THIRD SIGNATURE (D-0056,
    any builder node, parallel or solo): a builder `witness` that
    names `test_story_step.py`, every `test_story_run_*.py` at once,
    a full `selftest.py`, a docker run or a mutation RUN is the leak —
    those are the batch canon's (`plans/builder-rules.md` 7b); the
    DoD that asked for it is the dispatcher's defect, a run nobody
    asked for is the builder's. An empty window (no
    concurrent `delegated` groups) is noted explicitly — "no
    concurrent groups".
    (k) DOC-DISPATCH WITNESS (rule 11). For every builder acceptance
    of the window whose witness is NOT a pytest run but a
    deterministic key-presence script (owns — markdown/config with no
    test set of their own): check the three properties of the norm —
    (i) keys quoted from the DoD as written BEFORE the run; (ii) the
    script committed as a test or attached in full source; (iii) the
    run carried a NEGATIVE control (a deliberately absent key → a
    reported failure). Any missing property = a finding (the witness
    is a retelling, the witness-rule class); a script witness with no
    negative control is a finding ALWAYS, even with (i)-(ii) intact.
    An empty window (no doc witnesses) gets an explicit line.
    (l) MERGE ACKNOWLEDGEMENTS (B-401). For every merge commit of
    the window that changed logs/routing-log.jsonl (`git log --merges
    --full-history --since=<window start> -- logs/routing-log.jsonl`;
    `--full-history` because the default simplification hides a merge
    that is TREESAME to one parent), list the
    `merge-accepts:<n>:<fields>` tokens its new tail lines carry: per
    merge, the number of tokens, the field names, and whether each
    token is followed in the same notes by the corrected value and a
    reason. Find them with a case-insensitive content search for
    `merge-accepts:` over the journal, with a positive control of the
    same form (a token known to exist, or a fixture line). A token
    with no corrected value or no reason is a finding. A token naming
    `by` (an acknowledged acceptance pair) is a finding unless its
    notes name the Lead's decision. An empty window gets the explicit
    line "no merge acknowledgements".
14. **A golden set for recon, and a regression rule for prompt
    edits.** (a) Git log for the window on `.claude/agents/*.md`:
    every edit to a tier's role file that has an exam set (scout —
    PROCESS/SCOUT_GOLDEN_SET.md; critic — PROCESS/CRITIC_EXAM.md,
    both generated at onboarding), and every change to its `model:`
    frontmatter, is accompanied by a Runs-log line in that set's
    file in the same commit; an edit with no run is a violation. (b) Key
    liveness: run the verify commands for at least 2 questions in the
    set; a stale key is a bug in the eval itself — fix it BEFORE
    drawing any conclusion about scout degrading. (c) A rise in
    `failure_class=recon` for the window (check together with check
    3), with no out-of-cycle set run, means one should be scheduled.
    (d) Edits to tier role files with NO exam set (builder — by
    design: execution-based acceptance covers every task) get a note
    in the `calibrated` event. (e) A fabrication guard for any exam or
    entrance run that goes through a non-Claude harness: every such
    run in the window is checked by `tools/pi_run_guard.py` and
    carries a guard verdict (a Runs-log line / journal event) BEFORE
    it's graded against the key; an accepted or graded run with no
    guard line is a leak of the discipline-only trigger (evidence for
    promoting it into a code gate). Guard liveness: a known-bad replay
    fed to the guard must come back REJECTED.
15. **Repeated critic findings -> codification, with mandatory
    attribution.** (i) Base: verdicts of the window are walked for a
    finding CLASS that recurs 2 or more times (including findings that
    never escalated all the way to a formal defect) -- a recurring
    class is codified: a line in a spec/builder template, a new axis
    in the symmetry map, or a rule (the fix-the-class-not-the-instance
    rule, extended here to review findings, not only code defects); a
    repeat of an ALREADY-codified class is itself a finding -- the
    codification leaked. (ii) MANDATORY ATTRIBUTION: every verdict of
    the window carrying a rework/blocker note, and every `rejected`
    event, is attributed to its source -- a spec defect of the
    DISPATCHER (a gap/contradiction in the spec, an unnamed item in
    the given basket) | an error of the performer | external. (iii)
    Cluster the attributed causes; record the cluster COUNT in the
    `calibrated` event's notes. (iv) Landing: a dispatcher-side cause
    recurring 2 or more times in the SAME run is landed as a line/
    refinement of the five-point pre-dispatch checklist (rule 11's own
    checklist; this deployment keeps no separate checklist file — a
    recorded choice against a diverging duplicate) -- or an explicit
    line `not codified: <why>`. (v) The measurable goal: a class that
    has landed in the checklist produces no repeat rework in the NEXT
    window; a repeat is itself a codification leak. (vi) This check's
    OWN failure detector: a window with rework/reject verdicts but no
    cluster count in the `calibrated` event's notes is a leak of this
    very norm.

    Edge behavior (named, not left to the runner's guess): an EMPTY
    window (no rework/reject verdicts at all) records an explicit line
    `no rework/reject verdicts in the window` rather than silence. An
    AMBIGUOUS source (more than one plausible cause) is attributed to
    the class `unattributed`, with the ambiguity itself named in
    notes. A verdict whose cause chains through BOTH the dispatcher and
    the performer (e.g. a vague spec that the performer also
    misread) is attributed to the EARLIEST cause in the chain (the
    dispatcher) as primary, with the second cause recorded alongside,
    not silently dropped. At the landing THRESHOLD (exactly 2
    repeats): landing into the checklist is mandatory, same as any
    higher count; at 1 repeat: record the class, do not land it yet
    (landing needs the SECOND occurrence to confirm a pattern, not a
    single data point). Landing a class into the pre-dispatch
    checklist is itself an edit of CLAUDE.md -- Lead-tier work, named
    explicitly, not delegated.

    Acceptance of this check's own output is TEXTUAL (a witness run
    does not cover a judgment call like class/attribution) -- a named,
    accepted limit of this check, not an oversight.
16. **Two-pass external recon.** New RELATED_WORK entries for the
    period (and queue entries referencing an external survey): does
    each one name Lead's own second-pass trail — which files of the
    external repo Lead read itself, beyond the scout's digest? A
    section or plan resting on the digest alone, with no second-pass
    trail, is a finding; mechanisms drawn from such a plan freeze in
    the queue until the second pass happens.
17. **Cost gates (this deployment's slot; DECISIONS.md D-0035, BACKLOG
    B-462..B-466).** Over the window, from the transcripts (the
    session's `*.jsonl` and `subagents/agent-*.jsonl`; the script of
    07.10.2026 lives in the retrospective, the weights cache-read 0.1,
    cache-write 2, output 5) and the journal: (a) workers whose context
    passed 400K — expected 0 (`tools/agent_budget.py` STOP); each one
    is a leak of the gate; (b) fix rounds run by a RESUMED worker (a
    `SendMessage` to a builder after a critic verdict) — expected 0;
    (c) critic entries per task_id > 2, and re-review dispatches that
    carry the whole node instead of the fix diff — each a finding;
    critic-on-plan dispatches on specs with no fork or schema/money
    change — a finding; (d) the Lead session's median context per turn
    (target ≤ 350K; a turn over 600K means a compaction was skipped; with
    auto-compaction at 350K, once the experiment A0.1 confirms the key
    is honoured, a turn over 400K is a finding of the auto window),
    stage commits per merge (target ≤ 0.5), journal notes over 300
    chars written after 07.10.2026 23:00 (`journal_echo` warns),
    CI reads through the browser instead of `tools/ci_read.py`; (e)
    more than 4 WRITING workers alive at once (`dispatch_gate.py` blocks;
    D-0040: a worker is a writer when its `agent-<id>.meta.json` says
    `agentType: builder` or its first user line carries an owns line
    with a path — `transcripts.is_writer`; readers are not counted;
    `budget-skip:` lines counted and read); (f) the total effective
    units per merged node, compared with the 0.9 baseline (48M per
    node, 1113M for 23 nodes): the measures are working when the next
    graph of the same size costs under half of that. The carrier of the
    unit weights in code is `tools/hop_metrics.py` `UNIT_WEIGHTS` (the
    three weights above and input 1); the weight of input, 1, is an
    assumption, not a measurement (t-797 F5-2, F17).
18. **Economic trend (Rule #1 applied to the whole system) — "are we
    actually saving, and which way is the trend going."** Every run:
    `python tools/savings_report.py --until <end of window>` (full
    list-price API rates from usage_report.py, cache discounts
    counted, no batch pricing). In the `calibrated` event's notes,
    record four numbers against the previous data point: (a) $/day for
    the routed window; (b) gross savings versus the delegation
    counterfactual (in $ and %: sidechains as they actually ran,
    priced against that same token profile at top-tier rates); (c)
    cost per accepted unit of delegated work (sidechain actuals /
    accepted count across your journals for the window — check 13
    supplies the count); (d) API-track accounting: a rollup by
    traffic_kind plus the real-traffic share. Your first run records
    the baseline — note the method caveats alongside it (a baseline
    taken while still building mechanisms is censored, and the
    coordination premium isn't separable from non-delegable Lead
    work); read the trend only with those caveats until you've
    accumulated weeks without active mechanism-building. This check's
    own failure detector: missing economic numbers in a `calibrated`
    event's notes are visible to the next run and to the operator (the
    same class as a partial count silently passing as complete); the
    script's own failure mode is caught by tests in the canonical
    suite run. In the subscription contour (no `cc_usage` table, no
    gateway database) the four numbers come from `python
    tools/usage_report.py --days 7` (transcripts), or the
    `calibrated` event's notes carry the literal `n/a: no usage DB`;
    the `savings report: n/a` line of `tools/savings_report.py` is the
    detector of that leak (a traceback in a calibration run = red).

19. **Policy-as-code gates.** Posture: this check compares
    `.claude/settings.json` against its OWN state AT RUN TIME — every
    SessionStart/PreToolUse/PostToolUse/SubagentStop/Stop entry, the
    full list of `command` strings — not against a fixed list in this
    protocol, which is a dated reference snapshot and goes stale the
    moment a hook is added or removed; a mismatch between the
    reference snapshot below and the file's actual content is itself a
    finding, even when the added/missing hook isn't touched by any
    other sub-check here. REFERENCE SNAPSHOT (navigation only, not the
    source of truth): twelve command hooks — session_context
    (SessionStart); dispatch_gate/critic_snapshot/owns_gate (PreToolUse
    Task|Agent); hygiene_gate (PreToolUse Bash|PowerShell);
    claim_control_gate (PreToolUse Edit|Write); dod_track/journal_echo
    (PostToolUse Edit|Write|MultiEdit|NotebookEdit|Bash|PowerShell);
    search_control_gate (PostToolUse Bash|PowerShell|Grep|Glob|Read);
    negative_lint (PostToolUse Task|Agent); dod_gate (SubagentStop);
    main_gate (Stop) — a missing entry against the actual file is
    itself a finding (a rule that used to be enforced by discipline
    alone has silently reverted to that).
    Liveness: with live dispatches in the window, `.claude/dod_track/`
    is non-empty for at least one session, and any accumulated
    `gate_log` entries are non-empty; every gate silent while
    dispatches keep happening is a failure of the posture check above,
    not a clean bill of health -- verify the hooks actually ran before
    concluding "no blocks were needed". Blocks: spot-check 1-2
    `gate_log` entries (`blocked` / `skipped_after_2_blocks`) against
    the session's actual edits/runs for the window; a logged block
    with no matching fact in the track, or a block that shouldn't have
    fired given the track's own contents, is a finding about the gate
    itself, not about the session it blocked.

    PER-GATE ACCOUNTING: this posture check's duty is, for EVERY hook
    this posture names, to establish whether it is named ANYWHERE in
    this protocol as the subject of a failure/liveness check — a grep
    of the hook's name across the whole file, with a positive control
    of the same call form on every zero result. A name-match falls
    into one of three categories, and only the middle one counts:
    (1) MERELY MENTIONED — the name appears in prose, in a reference
    snapshot, or in a rollup that lists every hook by name (a rollup
    like that cannot serve as its own positive control) — does NOT
    count; (2) NAMED AS THE SUBJECT of its own failure/liveness check
    — a subcheck here prescribes what is verified for THIS gate and
    what counts as its failure, OR a mechanism resolves unambiguously
    to this gate from the run's own data (e.g. a `gate_log` event
    whose `gate` field names it, even where the surrounding prose
    never spells the name out) — counts, but FULL credit requires the
    prescribed check to be able to detect the gate's SILENCE (firing
    zero times), not only its wrong firing: a check that only
    cross-references EXISTING records ("no false blocks found") cannot
    tell "no violations happened" apart from "the gate is dead and
    writes nothing", and earns PARTIAL credit only; (3) NAMED AS A
    TOOL FOR SOMEONE ELSE'S CHECK — the gate is cited only because
    another check borrows something from it (a file, a line, an
    anchor) to verify a DIFFERENT subject — does NOT count. Category
    (2) is re-derived at every run by re-reading the relevant
    subchecks fresh, never from a cached summary of a past run (a
    summary is navigation, not a source of truth, and goes stale the
    moment the underlying subchecks change). A hook covered nowhere —
    neither the full nor the partial form of (2), nor the excusing
    form (3) — is itself a finding.

    (a) PROBE OF GATE-CODE LIVENESS: run
    `python tools/hook_liveness_probe.py` from the repo root and
    attach its output VERBATIM. The probe feeds each command hook of
    `.claude/settings.json` — including claim_control_gate,
    search_control_gate and negative_lint — a deliberately triggering
    stdin payload inside an isolated temporary tree, and asserts the
    expected trace: a printed reply carrying an anchor and a declared
    exit code, or a file artifact for gates that are silent by design.
    The run itself is the INDEPENDENT fact-trigger: the trace is
    obligated, so a gate's silence is distinguishable from "no
    violations happened" — closing exactly the gap PER-GATE ACCOUNTING
    names above for a category-(2) check that only cross-references
    existing records. Any verdict other than OK (DEAD / MISMATCH /
    CRASH / HUNG / MISSING / CASE-MISSING / STALE-CASE /
    LIVE-STATE-TOUCHED / SETTINGS-UNREADABLE) is a posture finding
    addressed BY GATE NAME. No attached output = this check is NOT
    done. KNOWN BENIGN FLAKE: a LIVE-STATE-TOUCHED verdict on the
    CURRENT session's own ledger file during a long run can be a
    timing coincidence with that same session's own PostToolUse hook
    writing — rerun; a PERSISTENT repeat is a genuine finding. LIMIT,
    STATED EXPLICITLY: the probe proves CODE liveness, not WIRING
    liveness (registration in `.claude/settings.json`, the matcher,
    `core.hooksPath`) — wiring stays with the Posture paragraph above
    and `tools/wiring_check.py`; crediting Posture through this probe
    is forbidden.

Numbering note: checks 20 and 21 below are this deployment's own
sequence, continuing straight on from 19 (no numbering gap) -- they are
the local equivalents of a source deployment's checks 30 and 31, ported
adapted to this file's own numbering rather than reproduced under
matching numbers, since this protocol's own sequence has never mirrored
a source protocol number-for-number (see checks 15/17, reserved
placeholders unique to this file). The correspondence is recorded here,
once, rather than in every cross-reference below.

Checks 23-29 continue the same pattern (source checks ported under this
file's own continuous numbering, not reproduced under matching
numbers): source check 0 -> 23; source check 20 -> 24; source check 21
-> 25; source check 24 -> 26; source check 25 -> 27; source check 29 ->
28; source check 32 -> 29 (recast from the adopting/receiving side to
the REDISTRIBUTOR side -- see check 29's own applicability clause; the
receiving side is check 22, already ported earlier). Source check 26's
liveness-probe sub-point lands inside THIS file's existing check
19, as a new lettered sub-point, rather than as its own numbered check
(its subject -- hook-code liveness -- is a posture detail of check 19's
own gate list). Source check 1's designer-threshold / resubmission
sub-points land inside THIS file's existing check 1, as sub-points (c)/
(d), for the same reason. Source checks 15/17/27/28 are NOT ported (15
duplicates this file's own already-ported check 15; 17 is a reserved
placeholder in both files independently; 27/28 are specific to a
sibling deployment this deployment does not run). Check 30 continues
the same pattern (kit v0.9.0 release batch, node C4): the local
equivalent of a source deployment's Opportunity-scan-of-delegation
check, ported under this file's own continuous numbering rather than
the source's own number.

20. **Leaf-routing judge acceptance (rule 13).** Mechanism: rule 13 of
    CLAUDE.md reads 'not used in this deployment': no judge is bound,
    and the judge's files stay dormant (the owner's word 11.11.2026).
    Window check: (a) rule 13 reads 'not used in this deployment';
    (b) any `accepted` with `basis: "judge"` in the window is a
    self-certification finding (the same class as a role-vs-tier
    violation, CLAUDE.md's "Role != tier"). `tools/journal_validator.py`
    still accepts the value (residual node R-1 of t-013), so (b) is
    its only detector.
21. **Durable persistence of accepted deliverables (session-handoff
    step 2a).** Class: "deliverable drift" -- work accepted against the
    working tree (a real witness at the time) gets washed out by a
    later wide checkout/reset before the commit that should have
    carried it, and neither the witness nor a critic verdict re-checks
    persistence after the fact. Window check: (a) for every
    `accepted(builder)` in the journal, the entity the witness names (a
    test, a function, a file) exists in the COMMITTED HEAD (`git show`
    / grep against HEAD; on doubt, `git log -S` by name -- a carrying
    commit exists and was not reverted). A real witness with the entity
    absent from HEAD is drift -- a finding, plus a `defect_found` (`ref`
    pointing at the original `accepted`). (b) liveness of the
    evening-side check -- session-handoff's step 2a is in place (a
    targeted lookup, not a re-derivation); systematic drift while step
    2a is live and being run is a discipline leak -- evidence for
    promoting the check into a code gate. (c) a disputed "did the
    artifact ever exist" is settled by runtime witnesses outside git (a
    test-cache entry, a file mtime, a process/track log) -- the same
    forensic class as the check above.

22. **Ledger drift and completeness.** Mechanism: the
    adoption ledger records the kit snapshot revision and mirrors the
    current template's row nomenclature; an upgrade is a
    re-inventory BY DELTA-PER-REVISION — new/changed mechanisms since
    the recorded revision, including role-file CONTENT (not just
    their model: frontmatter), skills, tools, PROCESS; a full rescan
    applies only when no revision is recorded (a pre-versioning
    install, one-off). Violation: an "adopt" row
    whose mechanism is absent or stale in the tree; a template row
    missing from the ledger entirely (a dropped row hides forever —
    the class of a row silently dropped from the host's own mirror of
    the template nomenclature); a recorded revision no upgrade batch
    has reconciled. Window check: (a) every current template row has a
    ledger row (completeness); (b) spot-check adopt rows against the
    tree (mechanism present, wired); (c) the recorded kit revision
    exists, and the last upgrade batch's delta was decided row by
    row — at least deferred, silence is not a decision. For (b),
    "wired" is explicit (wiring drift): the row's mechanism
    is not just present on disk but actually wired — its hooksPath
    entry / settings hook / invocation path exists; an adopt row
    whose wiring silently fell off is a finding even when the file
    itself is still in the tree. Continuous pair of (b): the
    deployment's SessionStart wiring check reads this ledger's adopt
    rows, not only the configured hooks. The counterpart of this
    check, on the side of whoever maintains the kit you're adopting
    from, is their own port-batch delta check (their calibration
    protocol). (d) Install-parity leg: CONTENT actually landed, not just ledger
    rows — a recorded "Kit snapshot revision" with no matching
    "Install parity: ..." record is a finding, the same class
    `tools/wiring_check.py`'s own notices channel (K12) surfaces as a
    non-blocking WARN at SessionStart; this window check runs
    `tools/install_parity.py --check` against the CURRENT tree and
    treats any MISSING/UNKNOWN anchor with no matching waiver row as
    the finding, not a bare ledger-row read. MISSING > 0 in CI = red; a `parity-skip` door is counted.

23. **Closing out the previous run (retro-contour).** Open the notes
    of the last `calibrated` event and that run's findings: each is
    closed by a mechanism/decision, OR sits queued with a NAMED
    trigger that has not fired yet. A queue item (the CURRENT_CONTEXT
    queue, or the deployment's FINDINGS log) whose trigger fired, with
    the work neither started nor re-decided, is a finding OF THE
    CURRENT run. Sources: the journal's `calibrated` events, the
    FINDINGS log for the window, the CURRENT_CONTEXT queue. A fresh
    deployment with no prior `calibrated` event has nothing to close —
    note it explicitly: "no previous run".

24. **Gate walk by `defect_found`.** For each `defect_found` of the
    window: list the gates that stood on the path of the defect
    (witness, the critic entry, trail-based acceptance, code gates),
    and name which stayed silent and why (a discipline leak / a check
    blind spot / a new class). A silent gate is a finding and a
    candidate for promotion into a code gate (rule 10's
    code-gates-execution clause); the breakdown line goes into the
    `calibrated` event's notes. An empty window (0 `defect_found`) is
    noted explicitly.

25. **Cost crossover of escalations (Update Rule 4 of the assignment
    table).** For every escalated task of the window (`escalated` plus
    its `task_id` chain): the actual full cost of every attempt
    (sidechains of the attempts, plus Lead overhead of acceptance)
    against the estimate of a direct dispatch to the tier where the
    task was accepted. A systematic loss by category (a cheap tier
    with retries costing more) is evidence for revising the delegation
    boundary (a table row / rule 6). An empty window (0 escalations)
    is noted explicitly.

26. **Freshness of navigation documents.** Direct pass: window events
    (phase/task closures, decisions, status moves — from the journal
    and git log) are reflected in their OWNER documents: DECISIONS.md
    (decisions), CURRENT_CONTEXT.md (the live task/queue),
    DELEGATION_TABLE.md (tier statuses), README.md (navigation),
    docs/SIBLING_MAP.md (the axis map). OWNERSHIP PASS: the same list
    of owners is read in REVERSE — for every block of the boot-path
    files, ask "is this fact at its OWN owner?" A block whose owner is
    a DIFFERENT document is a finding of the same class even when it's
    fresh and not duplicated: it is paid for by every session, but
    lives in the wrong place. Separately verify that a calibration
    run's OWN findings land in the `calibrated` event's notes, and
    CURRENT_CONTEXT keeps only the UNRESOLVED decision, one line per
    item — a finding written to the journal AND duplicated in prose in
    the queue bloats the live file and evades the boot-diet skill's
    size/dedup steps, since it is neither closed nor a duplicate of
    another boot file. Reverse pass: load-bearing claims of the boot
    path ("waiting on X", "next is Y", dates) are spot-checked against
    fact; a stale claim is a finding of this same class. The verdict
    is a semantic judgment for the calibrating Lead; a weekly cadence
    is enough. Distinct from check 10: that one watches the SIZE of
    live files, this one watches whether their CONTENT still matches
    fact, and whether it lives in the right place. Execution: both
    passes are carried out by a scout dispatch (walking documents is
    recon, rule 1); DoD — a line-by-line verdict "fresh / staleness
    candidate" per document with a trail, "no staleness" is a valid
    outcome with a trail; digest acceptance follows the trail-based
    acceptance rule. An off-cycle run of this check is legal at any
    time on the operator's word. A fresh deployment with no closed
    phases/decisions yet has nothing to check against — note it
    explicitly: "no events to reconcile".

27. **Permission/hygiene audit of the window.** Run
    `python tools/permission_audit.py --minutes <window>` (or `--all`)
    against transcripts of the period; the walkthrough steps are
    `.claude/skills/permission-audit/SKILL.md`. `--summary` prints the
    "hygiene class breakdown" — a count by the four REFUSAL classes of
    `tools/hygiene_gate.py` (`cd`, content write, journal, rollback)
    across ALL scanned calls; the SHAPES come from `--summary` (labels
    from `HYGIENE_CLASS_LABELS`), the VERDICTS (refused / not refused)
    from the gate's own denials in the transcripts. The first
    run of this check after the gate records ITS OWN baseline: the
    baseline of 12.11 (39/68/58/1 unique) is NOT comparable; later
    runs compare against the new one. An
    empty window (no transcripts, or a fresh deployment with none yet)
    is noted explicitly — "no calls to audit". Two categories: (a)
    hygiene VIOLATIONS themselves: a call of a refusal class that was
    NOT refused, or one of the gate's named residuals (file-level
    copies onto tree files, non-literal targets, scripts outside the
    repo writing into it, unclassified interpreters) found by reading
    the suspects; compound commands, `2>&1` in Bash, reads via
    `python -c` and poll loops are not counted (poll loops are check
    17 cost); also a RELATIVE NUMBER
    WITH NO NAMED BASE, a REGISTRY ENTRY'S STATUS CLAIMED FROM A
    PARTIAL READ (command hygiene point 6: the entry's status line was
    never reached) — fix at the source; the count and class go into
    the calibration report. (b) `settings.local.json` curation
    (MASKED-by-broad-allowlist rules, duplicates, one-off entries) —
    the skill's steps 3-5; narrowing broad rules is an operator
    decision.
    (c) UNSAFE ROLLBACK OF CORRUPTION: the gate's refusals of dirty
    paths are counted from the window transcripts, and every
    `rollback not checked` marker (a rollback the gate could not
    measure, so it passed) is read by hand NEAR a mutation probe (a
    file corruption, a red-probe, "corrupt then restore"): was a byte
    copy taken BEFORE the corruption, and was the file clean per
    `git status --porcelain`? If not, that is a violation of command
    hygiene point 7 (the byte-copy rollback rule), and a finding —
    independent of whether harm actually occurred that time. A
    positive-form control of the search itself is mandatory (command
    hygiene point 6). An empty window (no refusals, no markers) is
    noted explicitly — "no rollback events".
    (d) THE "TRUNCATED REGISTRY WINDOW -> STATUS CLAIM" LINK: an
    address scan of window transcripts for the combination of reading
    a registry (escalations/decisions/tasks/ledgers) through a
    truncated/limited window (a `Read` with `limit`/`offset`, a
    headline grep that never reaches the entry's status line) followed
    by a status claim about that SAME entry in a summary or report
    with NO re-read of the status field. A hit is a finding plus a
    reminder of command hygiene point 6. HONEST CAVEAT: this class's
    base detector is INCIDENTAL (an operator's question exposes the
    mismatch by fact, not by rule) — this transcript scan only
    SUPPLEMENTS the incidental layer, it does not replace it with a
    machine one; do not present one as the other. An empty window (the
    combination never occurred) is noted explicitly — "no truncated
    status claims".

28. **Completeness of hand-backs: the report file and the short digest.** Mechanism: the rule
    "the report is a FILE at the dispatch's `handoff:` path and the
    final message is its digest of at most 2,000 characters and at most
    4 + N lines (N = the numbered items the dispatch asks) — the FULL
    report/digest/verdict goes into the final message only when no
    path is named or the Write is refused — and a resubmission
    restates it from scratch" (F5-1, t-744; the anchors' wording is
    pinned by `tools/test_handoff_rule_anchors.py`; `scout.md` has
    no Write and carries only the sentence that its final message is
    the report, extracted by the Lead) lives in the role files
    (`.claude/agents/builder.md` point 7, `scout.md` point 9,
    `critic.md` point 16, `designer.md` point 5, `judge.md` point 3)
    plus the code layer on SubagentStop: `tools/dod_gate.py` blocks
    once, with "HANDOFF MISSING", a worker whose dispatch names a
    `handoff:` path it did not write after its start. Window check:
    (a) liveness — the five anchors are in place (a point lookup; the
    cap key is "at most 2,000 characters"); (b)
    failure — `gate_log` entries `handoff_missing` of `dod_gate` in the
    window (each is a worker that skipped its file), hand-back messages
    over the cap (see (d)), AND window events marked with a content re-request ("repeat
    the report", "re-requested", "prior messages not delivered") in
    journal notes, AND/OR a usage-record sidechain with a large volume
    of work whose final message is empty or truncated, is a leak of
    the rule — a finding. The first window that measures this records
    its OWN baseline (rate per day/week); later windows compare
    against it — growth is grounds to revise the mechanism's form, a
    decline toward zero is the healthy direction; the first window
    after the short-digest form (12.11.2026) records a NEW baseline. (c) siblings — every role file on Axis 1 of
    `docs/SIBLING_MAP.md` carries the rule; a new tier/role file added
    later gets the same line in the same commit (Axis 1's own
    same-commit maintenance duty) — a role file missing it is a
    finding of this check, not just of Axis 1's own upkeep. An empty
    window (no re-request events, no truncated-message sidechains) is
    noted explicitly — "no re-requests".
    (d) Hand-back carrier (F5-1, t-744). For every `accepted` of a critic/scout/designer/builder task in the window whose
    dispatch named a `handoff:` path: who wrote the file — a Write/Edit `tool_use` with that `file_path` in the worker's
    `subagents/agent-<id>.jsonl` (its `worker_ref`) = the worker; a Write of it in the main session transcript = RETYPED by
    the Lead (a leak, target 0); a `tools/handback_extract.py` Bash call in the main transcript = extracted by code
    (legal, counted). Also count: journal notes saying "transcribed by hand"/"retyped"; hand-back messages over the cap of 2,000
    characters or 4 + N lines (`handback_extract.py` prints `lines=` and `bytes=`; bytes over-count non-ASCII text, so a
    message near the cap is read by hand); read-role dispatches with no `handoff:` path. The first window records the
    baseline.

29. **Upgrade delivery by delta-per-revision — the REDISTRIBUTOR
    side.** Applicable ONLY when this deployment itself further
    redistributes its (adapted) copy of the template to one or more
    downstream sub-deployments; a deployment that only ADOPTS from an
    upstream kit and never ships its own template onward has nothing
    to check here — note explicitly "not applicable: this deployment
    does not redistribute" and stop. The RECEIVING side of the same
    duty (this deployment reconciling deltas from whatever it adopted
    FROM) is check 22 above — do not conflate the two directions.
    Mechanism, mirrored outward: a port-batch shipped to a downstream
    sub-deployment is assembled as a delta from that sub-deployment's
    OWN recorded snapshot revision of your template; role files travel
    as diffable CONTENT of the delivery, not just their `model:`
    frontmatter. Violation: a batch shipped with new/changed
    mechanisms since the recorded revision carrying no corresponding
    ledger-delta lines in the target's own carrier — a mechanism
    invisible to the delivery (role-file content changes are the
    highest-risk case: a content-only edit with no frontmatter change
    can stay invisible to a delta check that only looks at
    frontmatter, and the blind spot can live for a long time before
    anyone notices). Window check, per outgoing port-batch: (a) the
    target's recorded snapshot revision exists; (b) your delta from
    that revision (a diff of your own template tree) is matched,
    position by position, against the ledger-delta lines in the
    target's handoff carrier — an uncovered position is a finding; (c)
    accepted role changes at the target are accompanied by their own
    exam gate; (d) SEALED DELIVERY OF THE CONTROL CHAIN: a delta
    position that changes an EXECUTABLE file of the control chain (a
    git hook, a hook script invoked by one) carries the FULL target
    content, not a delta line; the batch's acceptance carries a
    liveness-probe witness (an invalid input is rejected, and the
    probe state is rolled back afterward); and the target's required
    hook files land in git's index at mode 100755 — a mode of 100644
    ships a silently dead gate on Linux even though the file itself is
    present and looks installed. An empty window (no port-batches
    shipped in the period) is noted explicitly — "no outgoing
    batches".

30. **Opportunity scan of delegation (the assignment table's Update
    Rule 2, executable).** For the LARGEST blocks of the window's
    self-executed Lead-class work (usage records: main chains with no
    sidechain; git diffs of Lead sessions): for each one, ask "could
    this largest block of self-executed Lead work have gone DOWN to an
    existing tier, and did not — and what stopped it (no spec / the
    tier lacks the tool / an operator decision / nothing — a miss)."
    Output: 0..N new table rows; "no candidates" is a valid outcome as
    an explicit line in notes. This complements the violation-hunting
    checks above — the one place calibration looks for OPPORTUNITIES,
    not failures. CADENCE: this check runs ONCE EVERY FOUR calibration
    runs, or on the operator's word; a skipped run gets the line "check
    30: cadence, next run #NN". The signal for revising the check's own
    wording is not "empty" but "costs attention and catches nothing".

31. **Forge feature attribution and fragility.** Mechanism:
    `plans/features.json` + the journal's `feature` field +
    `tools/forge_metrics.py` (commit 6ba43b6). How to check: run
    `python tools/forge_metrics.py` (rewrites `plans/forge-metrics.md`)
    and `python tools/forge_metrics.py --check --base <sha of the
    previous calibration's HEAD>`; read the UNCLASSIFIED buckets first
    (events with no `feature` and no attributable tag/file/word) — a
    growing unclassified share is the violation; then the fragility
    index per feature (defects / fixes-of-fixes / reworks per feature)
    and the repeats metric (the same role/dispatch re-run on one task)
    — a feature whose index rose with no backlog row naming it is a
    finding. The merge gate (`.githooks/pre-merge-commit`,
    `.gitlab-ci.yml` job `forge-check`) is re-verified by one pipeline
    of the window being green (the owner reads it on GitLab, project
    100001).

32. **Compact snapshot (PreCompact hook).** Mechanism:
    `tools/compact_snapshot.py` on `PreCompact` writes
    `docs/tasks/compact-snapshots/<ts>-<source>.md`;
    `tools/session_context.py` prints the newest one on a `compact`
    start. How to check: for every compact in the window (the
    transcript's `compact` SessionStart with a `COMPACT SNAPSHOT:` line)
    a snapshot file exists whose age at that line is <= 2 min; a
    `COMPACT SNAPSHOT: failed` line, a `(none)`/missing line after a
    compact, or a snapshot older than the compact it should precede is a
    violation (the hook fails open, so this check is its only detector
    besides `tools/test_compact_snapshot.py`); uncommitted snapshots
    beyond the newest 30 are noted (the hook never deletes them).
    Since 12.11.2026 (F19, node A1): a hook snapshot carries its
    identity in its first line, and every compaction is followed by the
    `AFTER COMPACT:` line; a `COMPACT SNAPSHOT: MISSING` line is a
    violation of the snapshot duty; a compaction of `trigger: auto` is
    checked like a manual one; a Lead action after a compaction before
    any Read of the named snapshot is a finding. Named open limits, each
    counted when met: a session opened in the clone's parent (no hooks
    load: a compaction there has no line at all); auto compactions
    before the experiment A0.1 settles which event carries the pointer
    (the auto window is live since 97fae62); an `announced record not
    written` line, and two sessions writing the record at once (the
    lost update errs toward "fresh once more").
33. **Piles and batches, the journal per developer (DECISIONS.md D-0036;
    CLAUDE.md rule 4a; PROJECT.md «Командная работа»).**
    Mechanism: `tools/piles.py check` in `.githooks/commit-msg` (door
    `piles-skip: <item> -- <reason>`; a commit is judged on the piles it touches, and on a staged `.py` an active batch's function list names) and `check --base` in CI forge-check (the pushed range), `piles.py take`/`status`/`close` as the only code writers of a batch's status, `piles.py close` (formerly
    `release`, now a refused alias) as the only writer of «Закрыто», `logs/journal/<dev>.jsonl` with
    `journal_validator --all --base` in CI. How to check, over the
    window: (a) `python tools/piles.py check --all` on `origin/main` — any red line is a leak past the hooks; (a) is THE named reader of reds in piles no commit touched (t-356 SL-2: such reds never block a commit, and CI judges only the pushed range; no CI step audits the whole tree) (a `--no-verify`, a rebase, a web
    edit, a carried red); (b) `piles-skip:` lines in
    `git log --format=%B` per item letter — the door rate; a high rate on
    one item is that item's false-red finding, a door used for a routine
    operation (closing by the owner's word, a queue line) is a missing
    command; (b′) `piles-skip:` lines whose reason names another session's or pile's files — after t-356 SL-2 such a red cannot block, so each is a leak of the scope rule (a finding against `run_check`); (b″) one-developer pairs: for every pair the (б) ok line of `check --all` on origin/main names as «of one developer», read the claimed slug's journal `logs/journal/<slug>.jsonl`: it must show that clone's work on BOTH batches (an event whose `node` or notes name each batch). A pair whose second batch has no trace in that journal is a false "same" — two people under one slug, or `take --who` with another's slug — and is a finding against `piles.dev_of`; (c) the open set of `plans/BACKLOG.md` on `main` is a subset
    of the open set at the freeze commit, and `open=` of the freeze line
    minus the ids moved by `close` equals the current open count — a
    row that vanished otherwise is a lost item; (d) batches `в работе`
    without a taker or a branch, findings older than 14 days with no
    batch, a card row whose «Статус» is ahead of its batch file (this (d) item is the detector of `piles.py status`, t-356 SL-3);
    (d′) the D-0044 detector — `check --all` item (е) «findings placed»
    (F5-3, 15.10.2026): a red (е) on `main` is a bypass; its WARN line is
    the baseline of older orphans (dated before 2026-10-13 or undated —
    185 at the first reading, `piles.py check --all` on the merge of
    F5-3) and it must not grow between runs — a growth is a finding
    placed past the detector, the door rate of `piles-skip: е` is read
    with (b);
    (e) the journal: two files with one slug, a developer file whose
    line 1 is not `journal_created`, a line added to
    `logs/routing-log.jsonl` after the switch, `closes:` tokens with a
    label naming no file (each a finding; the validator refuses the
    first three, so a hit means a bypass); (f) REMOVED (github-move GM1-1, 04.11.2026,
    the owner's word: the GitLab board goes off): this detector lived on
    `tools/piles_gitlab.py`, which is deleted with the mirror, so it has
    nothing left to read (rule 10 (c): the end of a mechanism ends its
    detector in the same commit); a batch's status lives in the batch header and the card row only (written by `take`/`status`/`close`), and (a)-(d) judge those;
    (g) closed batches with an open proof row (F5-5, 15.10.2026): for
    every batch whose card row says `закрыта`, the «Живые доказательства»
    table holds only `сделано: …` / `перенос: … | обоснование: … |
    подтвердил: …` cells — `python tools/piles.py close` refuses otherwise,
    so a hit is a bypass (a batch closed by editing the card by hand);
    the three batches closed before the gate (forge/1, forge/2, forge/4)
    are the baseline, named once, not re-judged.
34. **Exchange form (F5-2).** (t-797 spec §3.4; the scout digest form v1,
    the brief as pointers, the `node` field of a `delegated` line.)
    Mechanism: `tools/digest_form.py` read by `tools/handback_extract.py`
    (`digest=` in its stdout line), the prose target of a brief (N = 8
    counted lines, a target, not a gate), the node `<slug>/<N>/<id>` of
    `journal_keys.node_of`, the measurer `tools/hop_metrics.py`. How to
    check, over the window: run `python tools/hop_metrics.py --window
    <start of the window> --json` and read, per hop of the window:
    (a) the share of scout hand-backs with `form` = `v1`, and the `flags`
    per v1 hand-back (a flag is a reading to look at, not a verdict; a
    hand-back with `form` = `none` after the form was taught is a scout
    that did not use it); (b) the median `brief_prose_lines` against
    N = 8 (the limit: prose glued to a header with no blank line is read
    as manifest, so the count can only be too low; a hop whose `cut` is
    `degraded` counts everything outside the manifest); (c) the median of
    `lead_intake_chars + lead_read_chars` per scout hop against the target
    of the finding (at most 2K tokens; the characters-to-tokens factor is
    an ESTIMATE and is labelled as one where written); (d) the share of
    hops with an `n/d` and the number of `unlinked` hops (a hop with no
    node, or a `delegated` whose node field is bad): a growth is a
    measurer going blind or the `node` field leaking, and each `warnings`
    line is one `delegated` to look at. The first run is the BASELINE (its
    `unlinked` share includes the old fix rounds that wrote no node,
    F13; the intake of a hand-back is read from BOTH carriers in which
    it reaches the Lead, a `user` line and a peer / task-notification
    `queued_command` `attachment` (never an `instructions` attachment),
    each message counted once, and `no_intake` means neither carrier
    holds it; a hop with an `n/d` column prints `chars` as a partial
    `N+`);
    the numbers go to the calibration file, not to notes. Money is not
    printed by the tool and not read here (P18); the two sums, `chars` and
    `units`, are never added to each other. Detector of this check's own
    failure: no numbers of check 34 in the calibration file is visible to
    the next run.

35. **Package detectors of the factory rules.** Mechanism: audit A27 (`python -B
    ai-packages/qa-factory/scripts/audit_factory.py --no-move`, conductor/1 C1-8,
    spec t-820; FR-42's check). Per window:
    (a) the A27 totals line (`A27 totals: P-built … S-built … seam … builder-built …
    builder-calls … U … delegated … py-wrappers … doors … counted … baseline … new …
    stale …`) against the previous window's, with the command beside the numbers
    (hygiene 6(b)); a growth of `delegated`, `py-wrappers` or `builder-calls` is read
    site by site, and `seam` at 0 while the seam exists is a dead scanner;
    (b) every `NO_MOVE_BASELINE` row added or raised and every `NO_MOVE_BASELINE_MAX`
    raise in the window (`git log -p -- ai-packages/qa-factory/scripts/audit_factory.py`,
    the `+    ('…'): n,` lines inside the dict and the `NO_MOVE_BASELINE_MAX =` line) —
    each must be named by the critic verdict of its merge, else it is a finding: this is
    the one growth the in-tree ratchet cannot see (I-shrink); the same reading applies to
    every member of SIBLING_MAP axis 18 (in-tree shrink-only ratchets);
    (c) every `# remains:` door added (`git log -p -S'# remains:' -- ai-packages/`) — the
    Lead reads each reason, and a reason that is not a reason is a finding;
    (d) the measured time of `--no-move` and of `test_audit_rules.py` against the previous
    window's (the cost of a gate on every package push; 5.2 s and 13.4 s at C1-8's merge,
    16.10 — the floor is the parse of `story_run.py` twice);
    (e) an empty window gets an explicit line.
    Detector of this check: a window with `story_run.py` commits and no line (a), (b) or (e)
    is itself a finding.

36. **Architecture kept (D-0055).** Over the window, list package commits (`git log --format=%H%n%B -- ai-packages/qa-factory/`) and their `architecture:` lines; count `none` lines vs named AR-n; read every finding of the breakage class filed in the window (an interview answer lost, a reader starved, a second reader/writer/seam added) and check whether its commit named the AR-n — a `none` on a commit that later produced such a finding is a false `none` (a calibration case for the gate's door); `python tools/architecture_index.py --check` green on main. Detector of this check's own leak: the finding count of the class in `plans/piles/*/findings/` dated in the window vs the `none` count.

37. **Worktrees removed after their merge (forge/6 F6-38, spec t-1210 F10 (a); forge/7 FG7-4, spec t-1738: the FULL background sweep).** Mechanism: `.githooks/post-merge` runs `python tools/worktree_sweep.py --post-merge` after every merge INTO `main` in the main checkout, and `piles.py close` runs the same; since t-1738 that call STARTS a detached background process which sweeps EVERY registered worktree (no count or time limit, one heartbeat lock in `<common .git>/worktree-sweep/`, `status.json` + `run.log` there); the SessionStart line `WORKTREES: …` of `tools/session_context.py` reports the last run's outcome (`running` / `finished N removed` / `died` / `crashed` / `refused` / `not-started`), and that line is the leak detector — a `died`, `crashed` or `not-started` outcome, or a `finished` older than the last merge into `main`, is the leak. The check runs the FULL dry run, not the status: `python tools/worktree_sweep.py` in the main checkout; the number of `CAN REMOVE` lines whose branch merged into `origin/main` more than 7 days ago (the merge date by `git log -1 --format=%cd origin/main ^<branch>` of the branch's last commit, or the archive ref) must be 0; each such line names why the sweep did not run or did not finish (E19 of spec t-1210: a conflict merge finished by `git commit`, a `pull --rebase`, an MR merged in GitLab with no local pull — or a hook not placed, `tools/wiring_check.py`; spec t-1738: the background process died — `run.log` / `prev.log` say where). `KEEP real changes` and `KEEP active` lines do not count, so correctly kept copies never redden the check for good. Detector of this check's own leak: the SessionStart line of the week's first Boot Report vs this count — a `finished 0 removed` with a count above 0 means the sweep judges against local `main` while the check judges against `origin/main` (pull first), or the check was read without the dry run.

38. **The conductor investigates before it asks a person (PROJECT.md P22, the owner's word 02.11.2026; release-next/1 RN1-9, spec t-722 + reviews t-727/t-764).** Mechanism: a question to a person carries a class of `references/person-owned.json` (`why_person`) and what was read (`checked`); the driver road refuses one without them once (`no_move.ClassRefused`, `story_run.Driver.waiver_road` passes `--by driver --why-person <id>` on every recorded word), the INTERACTIVE road (`waiver.py --why-person`) holds on discipline: a word without a class is recorded and counted, never refused (rule 10(d), an explicit discipline choice). The check: `python -B ai-packages/qa-factory/scripts/person_owned.py --share --task-root <root>` over every story root of the window (the stand copies, RUNBOOK §9) — read `words` (the interactive road) and `driver_words` (the driver road) SEPARATELY: `words.unclassified` above 50 % of `words.total` on any root is a finding against the interactive road (the conductor asked without naming what only a person decides); `driver_words.unclassified` above 0 is a finding against the driver (a code-raised question with no class — `person_owned.json` lacks a row or `waiver_road` was bypassed: `grep -n "waiver.py" scripts/story_run.py` must show no call without `--why-person`, positive control = the seven sites of t-767); an empty window (no story root) gets an explicit line. Detector of this check's own leak: `test_person_owned_paths.py` (the grep key over the driver's calls) and `test_conductor_investigates_first.py` K2/K4 (the texts) stay green while the share is never read — a window with story roots and no `--share` line in the calibration record is itself a finding.

39. **«Остатки» items carry an executor (onboarding-forge/1 F6-30; the owner's word 21.10.2026, PROJECT.md «Командная работа» п. 9).** Mechanism: `piles.py check` (д) refuses a NEW or CHANGED «Остатки» item without `сделано:` / `узел:` / `перенос:` (commit-msg; CI `check --all --base`); `piles.py summary` (its count line) and the compact snapshot print «остатков без исполнителя: N». Check: (a) N at the window's end, by pile — each item is either older than the gate's commit (the baseline) or a leak: count the `piles-skip: д` doors in the window's commit messages; (b) `перенос: … | подтвердил: —` items older than 48 hours (`git log -S "<item text>"`) — a carry waiting for a person goes into the morning report; (c) `узел:` items whose node is still «ожидает» after its batch closed. An empty window (no item, no door) is noted explicitly.

40. **BATCH CANON within the hour, always in CI (onboarding-forge/1 F6-50; the owner's words 28.10.2026 and 03.11.2026 «Канон всегда на CI»).** Mechanism: the `canon-clock` job of every `api`/`web` pipeline (`tools/canon_clock.py`) is red over 60 minutes unless the head commit carries `canon-over-hour: <reason>`. Check: for every batch and release accepted in the window, its canon pipeline id in the last `accepted` witness and that pipeline's `canon-clock` line (`python tools/ci_read.py jobs <id>`, `log <job_id> --grep "canon wall time"`); a batch or release accepted with no canon pipeline, a canon without a green `canon-clock`, every `canon-over-hour:` door and every local docker canon (with why CI could not run) are listed. An empty window is noted explicitly.

41. **Where judgment lives (P27, AR-29; D-0060, spec t-1765).** Mechanism: the census `scripts/tests/fixtures/judgment-census.json` with `test_judgment_census.py`, the `judgment:` line of `tools/architecture_gate.py`, the critic's question 11, `role-load.json` `process_ratchet_tokens`. Per window: (a) the census totals by class and `breach`, `blocks_overrides` and `blocking_per_role`, against the previous window's, with the command beside the numbers (hygiene 6(b)): `python -B -m pytest ai-packages/qa-factory/scripts/tests/test_judgment_census.py -q` green and the totals line it prints (the scanned-file count included: a fall with no deleted scripts is a narrowed scan); every raise named by a critic verdict, else a finding (axis 18); while the census is not on `main` yet (part A lands forge-first, F-6 (a)), the line says "census not on main" — not a finding, not a zero; (b) every role's start load, `craft_tokens`, `process_tokens` and the craft share (`role_load.py --all --json`), against the previous window's; a process growth with no named raise is a finding; before node A4 lands, the line says "craft split not on main"; (c) the `judgment:` lines of package commits (`git log --format=%H%n%B -- ai-packages/qa-factory/`): count `none`, `adds data check`, `moves … to role`, `moves … to code`; the Lead reads every `to code` line, and samples three `none` and three `adds data check` lines against their diffs; a `none` whose diff changed a census row or added a refusal on content is a false `none`; (d) the share of craft in each role's charter — three `kind: craft` sections sampled and read: a procedure marked craft is a finding; and three census rows of class `shape`/`xref` and every `blocks_override` sampled against their function bodies: judgment under a data label is a finding; (e) an empty window gets an explicit line. Detector of this check's own leak: a window with package commits and no line (a)–(c) is itself a finding; the forge metric «findings of the class "role halted on a form" in `plans/piles/*/findings/`» growing while the census counts fall means the census is being relabelled, not the code changed. (Numbers 39 and 40 are reserved for t-1702 D3, not on `main` yet.)

42. **One road for one action (PROJECT.md P31; TR2-15, spec t-2065; SIBLING_MAP axis 34).** Mechanism: designer rule 6, critic rule 19 with brief question 12; later `tools/language_sites.py` over `tools/language-sites-baseline.json` (spec t-2065 N3). Per window: (a) specs of the window: `grep -n -i -E "non-goals?.*(python|typescript|java|c#|csharp|pytest|язык)" docs/tasks/specs/` (positive control: `t-1968-mutation-probe-marker-and-critic.md:222` must hit); each hit in a spec dated in the window quotes the owner's word with its carrier, or is a named node of the same spec, or came back as a fork; otherwise a finding against the designer (`failure_class=spec`); (b) verdicts of the window (`docs/tasks/specs/reviews/`): every critic verdict on a plan or a diff carries a `ONE ROAD:` line; every exclusion named as kept has a carrier read and checked as said in a session with the owner (PROJECT.md «Командная работа» п. 6); (c) residuals: every finding answering question 12 has a node id in its pile; a "tell the owner" line with no node is a finding; (d) once the baseline exists: `python tools/language_sites.py --totals` against the previous window's, with the command beside the numbers (hygiene 6(b)), and `--raises --base <window start>` read against the verdicts (axis 18); before that, the line says "code layer not wired" — not a finding, not a zero; (e) an empty window gets an explicit line. Detector of this check's own leak: findings of the class (a language, project or case left out of a shared mechanism) in `plans/piles/*/findings/` dated in the window whose spec or verdict this check passed.

43. **The test quarantine is watched and judged (the owner's words 10.11.2026; spec `docs/tasks/specs/td-15-scenarios-quarantine.md` §D; rule text `docs/TESTING.md`).** Mechanism: `ai-packages/qa-factory/scripts/tests/test-layers.json` (`keep`, `pin_holds`, `quarantine`, `cohorts`), the CI job `quarantine-watch` on a schedule twice a week, `tools/test_quarantine.py` (`pull`, `judge`, `land`, `status`, `check` in the nightly job `quarantine-check`), the SessionStart line `TEST QUARANTINE …` of `tools/session_context.py`. Per window, with the command beside every number (hygiene 6(b)) — `python tools/test_quarantine.py status`: (a) the age of the newest watch run on CI — over 8 days is a finding (the schedule is off or the job is red by the runner); (b) red observations with no verdict older than 7 days — each is a finding against the Lead; (c) `real_catch` verdicts with no `land` row — a catch that was judged and not carried into a scenario or table row; (d) the count of `blind` observations (a file that could not be judged) against the previous window's; (e) `git log --format=%H%n%B -- ai-packages/qa-factory/scripts/tests/` over the window: every commit touching a quarantined file carries a `quarantine-edit:` reason, every new `test_*.py` has a keep row whose layer and why a critic verdict judged; (f) the test : product line ratio of accepted nodes (check 33 reads the same number); (g) no quarantine yet, or an empty window — an explicit line, not a zero. Detector of this check's own leak: a window in which the SessionStart line said `ALERT` and the calibration record carries no line (a)–(c).

44. **Stories with a non-real side are never delivered as `yes` (t-2181 §8, PC-10; AR-28, AR-25, AR-12).** Mechanism: the package detectors `test_sides_ledger.py` (no `on_substitute` or `sides_unknown` input reads `passed`), `test_awaiting_state.py` (no held story reaches S6 or gate B; a stopped story is terminal) and `test_state_exits.py` (every new state has a row), registered in `design/architecture.md` under AR-28 and AR-25; the counters `sides_measure` of `python -B ai-packages/qa-factory/scripts/report_facts.py --task-root <task> --json` (written by `report_facts._sides_measure`; the key exists only for a story with a sides record). Per window, over the window's live runs, with the command beside every number (hygiene 6(b)): (a) the stories whose `sides_measure.non_real_sides` is not empty and whose `sides_measure.verdict` is `yes` — must be 0; each one is a finding against the package, and the test that should have caught it is named; (b) the stories whose `sides_measure.awaiting.since` is older than 14 days with `awaiting.state` not `stopped` — listed with their ages, not a defect; (c) the per-story counters, read as they stand: `provisional.settled_matched` of `provisional.total`, `phase2_cost` against `phase1_cost` (one metric per comparison; the median of from-scratch stories is read from `stage_compare.py`, not here), `on_substitute_count`, `sides_unknown_count`; a counter that reads `unmeasured: <why>` is written down with its why and is never read as 0 — `test_body_edits_at_bind` and `green_after_bind_only` read `unmeasured` until the factory keeps a record of them; (d) a window with no story that has a sides record gets an explicit line, not a zero. Detector of this check's own leak: a story of the window that has a non-real side in its `pipeline.json` (`sides` record) and no `sides_measure` in its `--json` facts.

45. **Worktree base differs from the dispatch (F6-35, spec `docs/tasks/specs/t-366-f6-37-f6-35-f6-58-specs.md` §B.5 (c)).** Over the window's builder reports and `delegated` notes, count (1) reports saying the worker's base differed from its dispatch ('BASE NOTE', 'reality differs from the dispatch', a cherry-pick onto another base); (2) the dispatches that drew a WORKTREE BASE WARN of `tools/dispatch_gate.py`, and of those, how many were re-dispatched or re-based in the same session (`tools/warn_density.py` for the WARN count). Target: (1) = 0; a WARN never acted on is a fatigue finding. The WARN is a WARN by design; promotion to a refusal follows a leak counted here, not symmetry.

46. **Task id race: dispatch id differs from its journal line (F6-58, same spec §C.7 (c); CLAUDE.md, Routing log: id bands).** For each `delegated` in the window, read the worker's dispatch through `dispatch_manifest.handoff_mentions(section_cut(prompt))` — relative entries included, so scout dispatches count — take the `t-NNN` in a mentioned file name, and compare it with the journal line's `task_id` for the same `worker_ref`. A mismatch is the race of 13.11.2026 (two sessions writing one journal file). Second count: notes carrying 'collision', 'renumber' or 're-keyed'. Target 0 once bands (`id_band`, `journal_validator` rule 9e) and the PARALLEL SESSION note of the SessionStart and journal hooks are in use. Opening a band when the NOTE fires stays on discipline; this check is its leak detector.

## Closing out a run

DELEGATION_TABLE.md statuses move only on this data (Update Rule 1;
full cost including retries — Update Rule 4). On completion, write a
`calibrated` event to the journal: notes carry the period, the number
of events reviewed, table status changes, the check-10 line counts,
the check-11 hook output size, the check-13 false-accept rate by tier,
and the check-18 economic numbers (against the previous data point).
No `calibrated` event for more than 7 days while routed traffic is
live is itself a violation, visible as a Last Calibration line in
every session's Boot Report (the detector lives outside this protocol
on purpose: calibration cannot be the detector of its own absence).

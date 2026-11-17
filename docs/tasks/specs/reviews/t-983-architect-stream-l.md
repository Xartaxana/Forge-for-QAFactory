# t-983 — critic verdict on stream L (`614bc01f`, branch `lead/stream-l`): the ladder flip

Reviewer: critic (Opus). Under review: the Lead's own commit, stream L of `docs/tasks/specs/20261116-architect-tier-spec.md`.
DoD: keys K1-K7 of the dispatch. Read on the worktree `C:\QAFactory\forge-repo\.claude\worktrees\stream-l` (HEAD = 614bc01f).

**Verdict: NEEDS WORK (fit_with_fixes).** The flip is sound: the config parses as intended, every gate behaves as the
new texts say (probe below), nothing in the in-between world breaks, and the mechanical layer re-runs green. But two
items should be fixed before the merge: one CLAUDE.md sentence the validator contradicts (F1), and a batch-7 status
word that leaves a node stuck (F2). Ten more are text fixes that fit in the same round. Accepting the commit is the
coordinator's decision, not mine.

## Findings

**F1 (K1; fix before merge). CLAUDE.md:339, SHAPES row `accepted`: «`by` (a bare tier word)».** After this commit
CLAUDE.md defines a TIER as a FUNCTION RANK («Role ≠ tier», :367), and the `by` paragraph (:353) says `by` is a
model-family word. A reader who follows the row and writes a tier word gets a FAIL. Probe on the flipped config:
`_matrix_d0058_violation("accepted","builder","lead",{},cfg)` returns `FAIL: … by='lead' is not a known tier ([haiku,
sonnet, opus, fable]) ('lead' is a FUNCTION word …)`. Replacement text: «`by` (a bare model-family word —
`haiku`/`sonnet`/`opus`/`fable`, see below)».

**F2 (K6; fix before merge). batch-7 FG7-16 status «закрыта: поглощён потоком B…» (`plans/piles/forge/batch-7-vhodyashchie-4.md:41`).**
The vocabulary reading is right: `_node_reds` (`tools/piles.py:1846-1857`, the node check; it is not (д), which is the
«Остатки» check at :2856) accepts a cell only when it starts with a word of `NODE_STATUSES`
(`ожидает, в работе, сдано, принято, закрыта, отклонено`, :111-112). «снят» would be red. But `закрыта` is the wrong
word for a NODE:
- (a) `NOT_WRITING = ("принято","отклонено")` (:115), so `writers_of`/`fn_lists_of` (:1341-1368) still count FG7-16
  as writing `tools/journal_validator.py` and `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`. That is a phantom zone claim
  in check (б) once batch 7 is taken.
- (b) `status forge 7 --set принято` refuses while FG7-16 is «neither принято nor отклонено» (:3320-3324).
- (c) The node can never reach принято through the tool. `STATUS_ORDER[закрыта]=4 > принято=3` triggers «a status
  only goes forward» (:3292). `закрыта` is also not a word `status` writes for a node (`STATUS_NODE_WORDS`, :3221).
- (d) A batch word on a node misleads the pane: the row reads as «batch closed».

The work really was done, by stream B (`5a7cc343` «Architect stream B: acceptance matrix by function…», t-935, on
origin/main). Replacement text: «принято: 5a7cc34 (t-935) — поглощён потоком B спеки 20261116-architect-tier».
FG7-33 «отклонено: снят, заменён…» is right: отклонено is terminal and NOT_WRITING, and a withdrawn node fits it.

**F3 (K3). CLAUDE.md:256, rule 11a: «(rule 6; once tiers are exhausted, it queues for Lead via `escalated`)».** Rule 6
(:120-126) now sends escalations above the critic's model to the architect queue, so this sentence contradicts it.
Replacement: «(rule 6; once the tiers up to the Lead are exhausted it queues for the Lead, and above the Lead for the
architect — an item in `docs/tasks/architect-queue.md` + `escalated` with `agent: architect`)».

**F4 (K1). CLAUDE.md:390-391: «a `Last calibration` line ending in `overdue`».** The code
(`tools/session_context.py:618-630`) prints `Last calibration: <ts> (<n> days ago) -- overdue: tell the owner «…»
(calibration and mechanism review)`, or `Last calibration: NONE -- overdue: …`. The line never ENDS in `overdue`.
Replacement: «a `Last calibration` line carrying `-- overdue:`».

**F5 (K2). F23 is missing from the builder-rank bullet (CLAUDE.md:392-394).** The spec's F23 (recommended (a), «executable
on its recommendation») assigns L the CLAUDE.md «Role ≠ tier» builder-rank bullet, and check 6 (iii) already counts
this road (`PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:138`). The bullet says only «critic and designer work — `basis:
queued-to-lead`». Replacement: «critic and designer work — `basis: queued-to-lead`, cleared later by a Lead-ranked
session writing a second `accepted` of the same task with no basis (calibration check 6 (iii) lists the uncleared);».

**F6 (K3). The «standard mid-tier mode» is now dangling.** `.claude/agents/critic.md:52-53` (rule 9) says «below the Lead
rank (degradation, or the standard mid-tier mode, per the role-vs-tier acceptance matrix)». The new CLAUDE.md
(:397-399) no longer names a mid-tier mode (grep `mid-tier|mid tier` over CLAUDE.md finds 0; the same grep finds the
critic.md hit). The cheapest fix is in CLAUDE.md, which spares the critic.md exam duty: at :398 write «a session on a
model below lead (the mid-tier mode) is the same matrix».

**F7 (K3). CLAUDE.md:120: «ABOVE the critic tier «one tier up» is the architect».** By the new definition the critic's
model (Opus) ranks lead, so one tier above the critic FUNCTION is the Lead. The sentence means the model. Replacement:
«ABOVE the critic's model (Opus, which is also the Lead's) «one tier up» is the architect».

**F8 (K3). CLAUDE.md:356-358: «Events: the six of the table — … — plus `returned`, `decomposable`, `lead_degraded`,
`lead_restored`, `journal_created`, `calibrated`».** The table now has 8 rows. `calibrated` (added by this commit) and
`returned` appear both as rows and in the «plus» list. Replacement: «Events: the rows of the table — `rejected` is a
failed attempt (rule 6), `defect_found` a late defect in ACCEPTED work (…) , `calibrated` a calibration run — plus
`decomposable`, `lead_degraded`, `lead_restored`, `journal_created`».

**F9 (K3, minor). CLAUDE.md:6: «Lead ends up doing delegable work itself on the most expensive tier».** False after the
flip: Lead is on Opus, Fable is dearer. Replacement: «… on a tier above the work's».

**F10 (K3, PROJECT.md). PROJECT.md:317: «`DECISIONS.md` пишет только Lead владельца».** CLAUDE.md:31 and D-0067 say the
Architect writes its own lines (F21). The spec §4.1(4) only *reads* the text as «Lead rank or above», so the text
still contradicts. Replacement: «`DECISIONS.md` пишет только Lead владельца или Архитектор (D-0067)».

**F11 (K5, minor). delegation.config.yaml:4.** The header names `designer` among the functions «bound to actual models»
in «the ONE file», while :28 says «`designer` has no row here». Replacement for :4-5: «# architect / lead / critic /
builder / scout -- see CLAUDE.md; designer is bound in its role file's frontmatter)».

**F12 (K7, siblings the flip made false; code text, fix this round).**
- (a) `tools/journal_validator.py:304` comment «The upper-mid-tier CLASS» and :709 message «…voiding the critic-gate
  guarantee for the upper-mid tier». Replace with «for the critic/designer class».
- (b) `tools/mechanism_gate.py:592` docstring «anyone below the top tier». Replace with «anyone ranked below lead».
- (c) `tools/test_savings_report.py:25` comment «(the real delegation.config.yaml binds the same)» is false now that
  the real config binds Opus. Drop the parenthesis.
- (d) `tools/savings_report.py:253,276,283` print `as-top-tier=` and key `as_fable`, but the counterfactual is now
  priced at the lead binding, Opus (:122, :272 «coordinator model»). The label lies, and check 18 reads this report.
  Tests pin the literal (`test_savings_report.py:66,95,160-161,418,430,460,462`), so this is a builder-class fix
  («as-coordinator=», key `as_coordinator`). It does not block L; it belongs to this round, as a stream-A fix node.

**F13 (rule 7, witness; non-blocking).** The attached layer covered only part of the L witness the spec names (§7 L:
«the narrow sets of A-E re-run on the merged tree + `journal_validator.py`»). `test_install_parity.py` was not re-run
after the two anchor fixes, and neither the validator nor the A/B/E sets were run. I re-ran the critical ones (trail):
install_parity, agents_md, tier_ladder and role-carrier tests are green, and the validator exits 0. The
mechanism_gate tests give 595 passed, 2 failed, and both failures predate this commit (see the note below). The
`accepted` event's witness should carry these outputs.

Pre-existing red, not attributable to L:
`test_transitive_import_closure_of_live_wiring_is_covered_by_mechanism_prefixes` and
`test_b23_the_closure_of_the_live_settings_is_inside_the_net` fail on `tools/usage_report.py`, which
`tools/forge_metrics.py` imports (commit e9204bde, t-905). L touches no `.py`. This matches «main-red diagnosis
dispatched» in origin/main `10410330`.

## Answers per key

- **K1**: The matrix by rank is TRUE of the code. It holds for the Lead (Opus) accepting critic/designer/builder with no
  basis, for Sonnet needing `critic` on builder and `queued-to-lead` on critic, for haiku as the floor, for `judge`
  refused, and for an unknown/capitalised/full-id/function `by` FAILing. The other claims are TRUE as well: `escalated`
  `agent: architect` opens a task (`journal_validator.py:1280-1287`, `journal_write.py:719,825-828`); the
  `calibrated.reviewed_through` shape (:939-950, `journal_write.py:724,839`); the MODEL line; the worker refusal
  (`hygiene_gate.py:78,1511-1512`); «unrecognised never reads as Lead» (gpt-5 → `function none`). Contradicted or
  inexact: F1, F4, and F7 (the wording).
- **K2**: Present: the config, all five sections, the two SHAPES rows (verbatim to the spec), PROJECT.md line, D-0067 +
  D-0003 note, batch-7 rows (FG7-33/14/16/22), AGENTS.md regen, the ADOPTION_LEDGER D-nnnn fill, and the commit-message
  axis block, `tier: fable` and «exam not re-run». Missing: F23 text (F5). Wrong: the FG7-16 word (F2). `.claude/settings.json`
  is unchanged, as intended (still `claude-fable-5-1`). D-0067 is free on every ref (searched all branches; it appears
  only on `lead/stream-l`).
- **K3**: No «Lead = Fable», «top tier» or «upper-mid» is left in CLAUDE.md. The grep found only the intended lines :31,
  :354, :369 and the architect bullets. Remaining inconsistencies: F3 (11a vs 6), F6 (critic.md), F8, F9, F10 (PROJECT.md).
  `ARCHITECT_START.md`, the calibration header (:7-8 «run by an Architect session») and `TWO_VOCABULARIES.md` (:14-15
  Lead → Opus, Architect → Fable) are consistent.
- **K4**: Nothing is broken in the in-between world.
  - **Validator.** The flip only raises Opus (2 → 3); Fable stays 4, Sonnet 1, haiku −1. So every old-legal pair stays
    legal, and `by fable` lines (in-flight builder acceptances included) pass at ok_rank. `basis: queued-to-lead` by
    opus now passes with a «queued to itself» WARN, and Opus critic acceptances with no `agent:` worker get the
    INDEPENDENT CONTEXT WARN. Both are WARNs only.
  - **Tier gate.** `tier: fable`/`claude-fable-5-2`/`opus` pass; `sonnet` and `haiku` are refused.
  - **SessionStart.** With the settings default (`claude-fable-5-1`), every new session prints `function architect`,
    the `ARCHITECT SESSION` line and the pin WARN `settings.json model claude-fable-5-1 != lead binding claude-opus-5-5`.
    That is correct by the texts (architect rank may do Lead work), but every default-opened session is pointed at
    the Architect checklist until the settings step. Keep that window short, and tell the other developers (spec §3.4).
  - **Merge.** origin/main moved to `10410330` during the review; `git merge-tree` against `lead/stream-l` is clean (no
    shared files).
- **K5**: `tier_ladder.bindings` returns lead/architect/critic/builder/scout exactly as intended, with no note. No
  `reserve` reader is left outside `tier_ladder.py`'s rename note. The other readers are unaffected:
  `claim_control_gate` (scope list), the `dispatch_gate:92` docstring, the `agents_md:257` text, the skills' prose,
  `savings_report.read_contour` (a `contour:` regex, not bindings), and `preflight_quota` (gateway config, not this
  file). One minor issue: F11.
- **K6**: FG7-33 is right. FG7-16 needs a fix (F2).
- **K7**:
  - DUPLICATION AND CONSISTENCY: none found. I grepped `tier_ladder|FAMILIES|TIER_ORDER` and the CLAUDE.md matrix
    against `journal_validator._matrix_d0058_violation`; the policy prose restates the code's matrix by design. One
    overlap: ARCHITECT_START:42 and CLAUDE.md degradation p.5 say the same thing on purpose (role carrier ↔ policy,
    axis 1).
  - CODE QUALITY: label/annotation lies made false by the flip (F12 a-d). There is no new code.
  - TESTS: the diff has no test lines; `tests-over:` n/a.
  - ONE ROAD (P31): none found. The stand-in applies to every tier alike, there is no exclusion by project or language,
    and degradation has one step for all.
  - ARCHITECTURE/JUDGMENT: non-package diff, so AR-n is n/a; there is no judgment moved into code.
  - IN-TREE RATCHETS: none touched. `install_parity_anchors.json` is not a shrink-only ratchet; its two anchors follow
    their texts, and the old ones are gone (grep → 0).
  - CLASS COMPLETENESS (rule 9, axis 1 policy ↔ role/code): the siblings left are F6, F10 and F12.

## Trail

Read:
- `git show 614bc01f` (full diff; message incl. axis block)
- spec §2-§7, Stream L card, F22/F23, owner's word on settings
- `critic-diff-brief.md`
- worktree `CLAUDE.md` (:1-12, :108-128, :330-435 + greps)
- `tools/tier_ladder.py` (whole)
- `journal_validator.py:636-790, 1270-1300` + greps
- `journal_write.py` greps
- `session_context.py:600-640, 1058-1100`
- `hygiene_gate.py` greps
- `piles.py:111-115, 200-206, 1338-1372, 1846-1857, 3221-3326`
- `delegation.config.yaml` (whole)
- `DECISIONS.md:20-45`
- `TWO_VOCABULARIES.md:8-20`
- `WEEKLY_CALIBRATION_PROTOCOL.md:1-20, 1129`
- `.claude/agents/*.md` greps

Commands, with results:
- probe script `scratchpad/probe.py` (ranks, matrix, tier gate on the worktree config):
  - ranks: haiku −1, sonnet 1, opus 3, fable 4, claude-fable-5-2 4 (family match), gpt-5 None.
  - matrix:
    - OK: opus+critic, opus+designer, opus+builder, sonnet+builder+critic, sonnet+critic+queued-to-lead,
      opus+critic+queued-to-lead, fable+critic, sonnet+scout, opus+architect.
    - FAIL: sonnet+builder (no basis), sonnet+critic (no basis), haiku+scout, fable+builder+judge, `Opus`,
      `claude-opus-5-5`, `lead`, sonnet+builder+queued-to-lead.
  - tier gate: sonnet False, opus True, fable True, claude-fable-5-2 True, claude-opus-5-5 True, haiku False.
- `( cd <wt> && echo '{"model":M}' | python -B tools/session_context.py )` for 5 models → MODEL/ARCHITECT/pin lines as in K4.
- `python -B tools/journal_validator.py` (worktree) → exit 0, no output.
- `python -B tools/agents_md.py --check` → «AGENTS.md: up to date (126884 bytes)».
- `python -B tools/install_parity.py --check` → «UNKNOWN (0) / informational (0)».
- `python -B tools/piles.py check --all` → «piles check: ok».
- `python -m pytest tools/test_install_parity.py tools/test_agents_md.py tools/test_tier_ladder.py -q` → «263 passed, 2 skipped».
- `python -m pytest tools/tests/test_role_carriers_one_owner.py tools/test_mechanism_gate.py -q` → «2 failed, 595
  passed»; both failures are on `tools/usage_report.py` closure (pre-existing, see F13).
- Negative greps with positive controls:
  - `top tier|upper-mid|lead-queue-fable|…` over PROCESS, agents, skills, TWO_VOCABULARIES, SIBLING_MAP,
    builder-rules, boot files, tools → hits only DEPLOYMENT_ECONOMY_EXAM:238 (the control; generic text) and the
    F12 sites. The same pattern on the spec → 3 hits (control).
  - `D-0067` over all refs → only `lead/stream-l`. Control: `D-0066` in the archive → 2.
  - `reserve` readers → only `tier_ladder.py`.
- `git merge-tree --write-tree origin/main lead/stream-l` → clean tree `a244529b`.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "F1 CLAUDE.md:339 SHAPES accepted row says by is a bare tier word; after the flip a tier is a function rank and the validator FAILS by=lead -- write: a bare model-family word (haiku/sonnet/opus/fable)",
    "F2 batch-7 FG7-16 status 'закрыта' on a node: still a writer (NOT_WRITING excludes it), blocks status --set принято of the batch, can never move to принято (STATUS_ORDER) -- write: принято: 5a7cc34 (t-935) -- поглощён потоком B спеки 20261116-architect-tier"
  ],
  "fixes": [
    "F1 CLAUDE.md:339 by (a bare model-family word -- haiku/sonnet/opus/fable, see below)",
    "F2 plans/piles/forge/batch-7-vhodyashchie-4.md:41 FG7-16 status -> принято: 5a7cc34 (t-935) -- поглощён потоком B спеки 20261116-architect-tier",
    "F3 CLAUDE.md:256 rule 11a -> once the tiers up to the Lead are exhausted it queues for the Lead, and above the Lead for the architect (architect-queue item + escalated with agent: architect)",
    "F4 CLAUDE.md:390 'ending in overdue' -> carrying '-- overdue:'",
    "F5 CLAUDE.md:392-394 builder-rank bullet adds the F23 clearing road: a second accepted of the same task by a Lead-ranked session with no basis (check 6 (iii))",
    "F6 CLAUDE.md:398 name 'the mid-tier mode' so critic.md:53 'standard mid-tier mode' resolves",
    "F7 CLAUDE.md:120 'ABOVE the critic tier' -> 'ABOVE the critic's model (Opus, which is also the Lead's)'",
    "F8 CLAUDE.md:356-358 'the six of the table ... plus returned ... calibrated' -> the rows of the table plus decomposable, lead_degraded, lead_restored, journal_created",
    "F9 CLAUDE.md:6 'on the most expensive tier' -> 'on a tier above the work's'",
    "F10 PROJECT.md:317 'DECISIONS.md пишет только Lead владельца' -> '... или Архитектор (D-0067)'",
    "F11 delegation.config.yaml:4 drop designer from the bound-here list; say designer is bound in its role file",
    "F12 journal_validator.py:304,709 upper-mid wording; mechanism_gate.py:592 top tier; test_savings_report.py:25 stale comment; savings_report.py as-top-tier/as_fable label (builder fix, tests pin it) -- this round, not blocking L",
    "F13 attach the re-run outputs (install_parity tests after the anchor fix, journal_validator) to the accepted witness"
  ],
  "class_completeness": "Axis 1 (policy <-> role/code): CLAUDE.md sections, AGENTS.md, config, DECISIONS, anchors covered; siblings left: critic.md:53 dangling 'standard mid-tier mode' (F6), PROJECT.md:317 DECISIONS writer (F10), code texts journal_validator/mechanism_gate/savings_report/test_savings_report made false by the flip (F12). Inside CLAUDE.md: rule 11a (F3), SHAPES accepted row (F1), Events list (F8), head line (F9). Axis 34 one road: none found.",
  "trail": {
    "read": [
      "git show 614bc01f (all 8 files, message)",
      "docs/tasks/specs/20261116-architect-tier-spec.md sec 2-7, Stream L, F22/F23, owner's word on settings",
      "docs/tasks/critic-diff-brief.md",
      "worktree CLAUDE.md 1-12, 108-128, 330-435 + greps",
      "tools/tier_ladder.py whole",
      "tools/journal_validator.py 636-790, 1270-1300",
      "tools/journal_write.py greps escalate/calibrated",
      "tools/session_context.py 600-640, 1058-1100",
      "tools/hygiene_gate.py greps",
      "tools/piles.py 111-115, 200-206, 1338-1372, 1846-1857, 3221-3326",
      "delegation.config.yaml whole",
      "DECISIONS.md 20-45",
      "docs/TWO_VOCABULARIES.md 8-20",
      "PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md 1-20, 1129",
      ".claude/agents/*.md greps"
    ],
    "reruns": [
      {"command": "python -B scratchpad/probe.py (ranks, matrix, tier gate on worktree config)", "result": "opus=3 fable=4 sonnet=1 haiku=-1 gpt-5=None; matrix as CLAUDE.md states; by=lead FAIL; tier gate sonnet False, opus True, fable True"},
      {"command": "session_context.py with model payloads fable-5-1, fable-5-2, opus-5-5, sonnet-5-5, gpt-5", "result": "architect / architect (family match) / lead / builder / function none; pin WARN on every session; ARCHITECT line on fable"},
      {"command": "python -B tools/journal_validator.py (worktree)", "result": "exit 0"},
      {"command": "python -B tools/agents_md.py --check", "result": "AGENTS.md: up to date (126884 bytes)"},
      {"command": "python -B tools/install_parity.py --check", "result": "UNKNOWN (0), informational (0)"},
      {"command": "python -B tools/piles.py check --all", "result": "piles check: ok"},
      {"command": "python -m pytest tools/test_install_parity.py tools/test_agents_md.py tools/test_tier_ladder.py -q", "result": "263 passed, 2 skipped"},
      {"command": "python -m pytest tools/tests/test_role_carriers_one_owner.py tools/test_mechanism_gate.py -q", "result": "595 passed, 2 failed (closure tests on tools/usage_report.py via forge_metrics, pre-existing, L touches no .py)"},
      {"command": "git merge-tree --write-tree origin/main lead/stream-l", "result": "clean (a244529b)"}
    ]
  }
}
```

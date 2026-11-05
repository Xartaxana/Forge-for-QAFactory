# Adoption Ledger — QA Factory development (yml-text-factory)

Template shipped by the toolkit itself; filled in by the onboarding
skill's "Ledger" step (`.claude/skills/onboarding/SKILL.md`), right
after the intake inventory step. One row per kit MECHANISM, named by
the kit's own NOMENCLATURE (its CLAUDE.md rules, PROCESS docs, tool
names) — not by an enumeration of whichever files a given install
happened to copy. That choice is deliberate (see the greenfield note
below): a nomenclature-based ledger can be drafted straight from
reading the toolkit's own docs, independently of exactly when the file
copy itself lands, instead of waiting on it.

## Statuses

- **adopt** — the mechanism is installed and used as shipped (cosmetic
  adaptation — naming, paths — doesn't change the status).
- **native-equivalent** — the FUNCTION the mechanism serves is already
  closed by something the host already has; the kit's own version is
  NOT installed for that surface, and the correspondence is written
  down here so the substitution doesn't silently drift out of sync
  with either side losing track of it.
- **deferred(\<trigger\>)** — the mechanism has no installed
  prerequisite yet (see the onboarding skill's PREREQUISITES table);
  name the exact condition that reopens the row — a fixed defect, a
  contour change, a volume threshold crossed — never a bare "later".
- **rejected** — the mechanism actively conflicts with something the
  host needs, by Rule #1 (its cost/friction outweighs what it buys
  here); name the conflict.

A mechanism is installed WITHOUT its own prerequisite by construction
never: either the whole bundle (mechanism + prerequisite) goes in
together as **adopt**, or the row is **native-equivalent** /
**deferred(\<trigger\>)** instead. A blank status is not a legal state
— every row resolves to one of the four above, even when the answer is
the default "nothing to compare against here, adopt."

## Example row — native-equivalent (anonymized precedent)

| Kit mechanism | Status | Basis / trigger |
|---|---|---|
| Leaf-routing judge acceptance (rule 13) | native-equivalent | the host's own deterministic pipeline gates already close the leaf-class acceptance function for one class of content, on a rule-triggered path; installing the kit's judge machinery on top of that surface would open a second acceptance path for a function the host already closes — correspondence recorded here; re-open only if the host retires those gates |

(The row above generalizes a real adoption precedent without naming
the source deployment: a host running its own AI-agents-on-rules
pipeline had already closed one class of leaf-work acceptance natively
before this kit was ever considered for it.)

## Greenfield note

An empty intake inventory — every host FUNCTION row blank (acceptance /
journal-accounting / escalation / isolation / calibration, per the
onboarding skill's step 0) — means every mechanism's status is
**adopt**: there is nothing at the host to compare against, so the
bundles install whole. The ledger is still created in this case, even
though every row says the same thing: it exists as the place a project
that starts greenfield and later grows its OWN mechanisms records a
future native-equivalent/deferred, instead of that divergence living
only as undocumented drift discovered by accident. Because the form
here is nomenclature-based rather than file-listing-based, this
greenfield ledger can be written before, or independent of, the actual
template copy landing on disk — straight from this template plus the
toolkit's own docs.

## Kit snapshot revision

Kit snapshot revision: `89ce7a60db62bcba52b3b459e68e81e3dc22c860` (Supervised-Delegation v0.9.0 hotfix 2; installed 29.09.2026, Path B) — written at install, updated by
every upgrade batch in the same move. An upgrade re-inventories by
the REVISION DELTA (role-file CONTENT included, not just `model:`
frontmatter); ledger completeness is checked against the CURRENT
template's row nomenclature — a template row missing from this ledger
entirely is part of the delta. No recorded revision = pre-versioning
install: record the current kit revision and treat the whole ledger
as the delta, once.

## Rows

One row per mechanism the onboarding skill's PREREQUISITES table lists
(plus any host-specific mechanism your own intake inventory surfaces —
add rows freely, never remove the standard ones without recording why):

| Kit mechanism | Status | Basis / trigger |
|---|---|---|
| Routing policy (CLAUDE.md core rules, Role != tier, Lead degradation, command hygiene) | adopt | whole block between the BEGIN/END markers; host adaptation 1 (scout tier line, D-0002) listed above the block; project rules imported from PROJECT.md outside the block; CLAUDE.md also imports `@docs/FACTORY_RULES_INDEX.md` there (generated FR index; pre-commit `--check`) |
| Role profiles (`.claude/agents/{scout,builder,critic,designer,judge}.md`; judge carries the pinned prompt — see the escape-check role pin) | adopt | models bound per D-0003; judge.md left as shipped (its role is deferred, see rule 13 row); designer.md rule 1 extended by host adaptation 2 (D-0021: edge invariants, error direction of a reused function) |
| Model binding (`delegation.config.yaml`) | adopt | D-0003 |
| Routing journal + validator (`logs/routing-log.jsonl`, `tools/journal_validator.py` pre-commit, `tools/journal_echo.py` PostToolUse) | adopt | journal seeded 2026-09-29T14:08:31 local |
| Mechanism gate + symmetry map (`tools/mechanism_gate.py`, `.githooks/commit-msg`, `docs/SIBLING_MAP.md`) | adopt | hooksPath set by the operator's own hand (the installing session's qa-factory guard blocks configuration changes, D-0007); project axes added to docs/SIBLING_MAP.md |
| Tier verification / SessionStart (`tools/session_context.py`, `tools/tier_echo.py`) | adopt | — |
| Wiring integrity check (SessionStart wiring check reconciling this ledger's adopt rows against actual hooksPath/settings) | adopt | — |
| Dispatch gate / critic snapshot (`tools/dispatch_gate.py`, `tools/critic_snapshot.py`) | adopt | host adaptation 3 (D-0022): the gate's two phrase-list checks of a builder dispatch are replaced by `tools/dispatch_manifest.py`, a completeness check of the rule-11 manifest in header-line form (CLAUDE.md table R11-f); `tools/hook_liveness_probe.py` anchors and `tools/mechanism_gate.py` prefixes follow |
| Owns gate — parallel-dispatch path-ownership overlap (`tools/owns_gate.py`, PreToolUse Task/Agent) | adopt | parallel builders in one tree (plans/builder-rules.md: no git state changes) is exactly its case |
| Hygiene gate (`tools/hygiene_gate.py`) | adopt | — |
| Judge role-file pin (`tools/escape_check.py` judge_role_pin leg + `tools/escape_allowlist.template.json` section) | adopt | pins verified green; gateway/shadow_eval.py installed only as the pinned source |
| DoD track / gate (`tools/dod_track.py`, `tools/dod_gate.py`) | adopt | — |
| Main gate / Stop hook (`tools/main_gate.py`) | adopt | — |
| Calibration / usage tooling (`tools/calibration_counts.py`, `tools/savings_report.py`, `tools/usage_report.py`, `tools/preflight_quota.py`, `tools/token_usage_stats.py` — reuses `usage_report.py`'s own price table and cost formula, not a second ledger) | deferred(trigger: usage carrier configured — the Test Project 1 analytics export or cc_usage) | no price/usage carrier wired yet |
| Permission audit (`tools/permission_audit.py`) | adopt | — |
| Non-Claude worker guard (`tools/pi_run_guard.py`, `gateway/PI_HARNESS.md`) | deferred(trigger: api-keys contour adopted) | subscription contour (D-0006) |
| Leaf-routing judge acceptance (rule 13, `gateway/judge_calibration.json`, `PROCESS/JUDGE_CALIBRATION_PROTOCOL.md`) | deferred(trigger: calibration run) | no calibrated judge; every acceptance goes through Lead/critic |
| Command-hygiene claim/search/negative-form hooks (`tools/claim_control_gate.py`, `tools/search_control_gate.py`, `tools/negative_lint.py` — command hygiene point 6, one row: all three mechanize the same claim/search/negative-form control class) | adopt | — |
| Hook liveness probe (`tools/hook_liveness_probe.py` — proves gate-CODE liveness for the hook-backed gates above; wiring liveness stays the wiring-integrity-check row's job) | adopt | run at install close |
| Owns verification, layer 2 (`tools/owns_verify.py` — post-batch CLI companion to the owns-gate PreToolUse hook above, same manifest-overlap defense) | adopt | — |
| Judge-calibration sanitize feed (`tools/judge_calib_sanitize.py` — key-stripped probe material for a live subscription-judge re-check against the leaf-routing calibration set above) | deferred(trigger: calibration run) | same as leaf-routing judge |
| Lead-replay shadow evaluation (`gateway/lead_replay.py`, `gateway/lead_replay_corpus.template.jsonl` — api-keys contour) | deferred(trigger: contour changed) | subscription contour |
| WARN layer density meter (`tools/warn_density.py`, `tools/warn_layers.json` — Rule #1 applied to the routing machinery's own WARN layers, weekly-calibration check 11) | adopt | — |
| R3 integration-review coverage informer (`tools/r3_integration_check.py` — deterministic large-commit/critic-trail informer for the critic-on-integration gate, rule 13(g)) | adopt | — |
| Critic verdict schema (`tools/critic_verdict.schema.json` — the structured verdict shape the critic role file's own acceptance rule references) | adopt | — |
| FINDINGS form + machine check (`docs/FINDINGS.template.md`, `tools/test_findings_form.py`) | deferred(trigger: findings log created from the template) | the factory's own findings live in plans/BACKLOG.md and the Why lines of design/factory-rules.md; a routing FINDINGS log is not created yet |
| Skills (`.claude/skills/*`) | adopt | — |
| PROCESS docs (`PROCESS/*.md`) | adopt | host-adapted: check 17 rewritten (D-0035, 07.10.2026) |
| Boot sequence / decision log / delegation table (`BOOT.md`, `DECISIONS.md`, `DELEGATION_TABLE.md`) | adopt | DECISIONS.md D-0001…D-0011 |
| Gateway / api-keys contour (`gateway/*.py`, `gateway/*.template.yaml`) | deferred(trigger: contour changed) | gateway/ is on disk only because the judge pins read gateway/shadow_eval.py; nothing in it is wired or run |
| Install parity (`tools/install_parity.py`, `tools/install_parity_anchors.json` — read-only structural check that every policy carrier's rules and clauses physically landed, run at the close of both a fresh install and an upgrade; see this template's own "Parity waivers" section below) | adopt | run at install close |

| Factory selftest and install smoke (host) | native-equivalent | the witness for a builder diff in the package (`scripts/selftest.py`, `scripts/install_smoke.py`); the kit's witness rule is satisfied by their verbatim output |
| Factory rules walk (host) | native-equivalent | `ai-packages/qa-factory/design/factory-rules.md` walked by touched section (D-0008); critic checks the answers |

Intake inventory (step 2), brownfield: acceptance — selftest + FR walk + owner review; journal — git history, CHANGELOG, plans/BACKLOG.md; escalation — the owner, via the backlog's decisions section; isolation — builder rules (no git state changes in a shared tree); calibration — run comparisons (stage_compare, compare.py) for the factory product, none for routing.

Rows with no plausible native-equivalent and no missing prerequisite
default to **adopt** — leaving the status blank is not itself a
decision; "nothing to compare against here" IS the adopt decision, and
gets written down as one.

## Parity waivers

Rows above resolve WHOLE mechanisms. `tools/install_parity.py --check`
resolves at the finer grain of individual ANCHORS (a rule, a clause) —
so a mechanism can be `adopt` overall while one specific anchor is
legitimately absent (a deliberate host adaptation, a rule the host
dropped on purpose). Record that here, one row per anchor, instead of
forcing the whole mechanism's row to a coarser status it doesn't
actually hold:

| unit_id | anchor | host_path | host_equivalent file:line | reason |
|---|---|---|---|---|

A waiver row is not legal without BOTH `host_equivalent file:line` (a
concrete pointer to where the host's own equivalent lives, or `—` if
there truly is none) and `reason` filled in — an empty pair is not a
waiver, it's an unexplained gap that `install_parity.py --check` will
keep reporting as `MISSING`/`UNKNOWN` every time it runs. Every
upgrade's closing parity run (the onboarding skill's Upgrade mode,
step 7) writes "Install parity: ..." as its own record line (in this
ledger's "Kit snapshot revision" note, or the upgrade commit message)
— that record names which run this waiver table reflects.

This ledger is a first-class artifact, not scratch notes: once a
deployment runs its own calibration process, drift between this
ledger's rows and the mechanisms actually live on disk is that
process's job to catch, the same way `DELEGATION_TABLE.md` statuses
are audited — see this toolkit's `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`
if you've adopted it.

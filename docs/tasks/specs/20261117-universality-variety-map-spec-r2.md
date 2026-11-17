# Spec r2 (designer t-1216, fix round of t-1207 after plan critic t-1212): universality — the variety map, the passage rule, the execution points (phase A, nodes U2 -> U4)

Status: r2 for Lead acceptance. r1 (`docs/tasks/specs/20261117-universality-variety-map-spec.md`) stays untouched; this file
is the WHOLE spec and replaces it for the U4 dispatch.
Input: r1; the plan critic verdict `docs/tasks/specs/reviews/t-1212-universality-variety-map-plan.md` (accept with fixes,
0 blocking); the intent brief `docs/tasks/specs/20261117-universality-variety-map-brief.md` (the owner's words, decided
points 1-3, definition, nodes); the three frozen scout digests t-1200, t-1201, t-1203 (`docs/tasks/specs/reports/`).

**Decisions in force (Architect session, 17.11.2026).** F1 = A (AR-2 widened, title unchanged; no new invariant).
F2 / Q-i = (b), decided BY THE OWNER 17.11.2026 ("Да, роль первой"; brief, «Решено владельцем» item 3). F5 = (b).
F6 = (b) (calibration check 42 gains sub-item (f)). F7 = (a). F8 = (a). F9 = (a). R13 = short cells. F3 / Q-ii and
F4 / Q-iii stay the owner's open questions. The definition and the F7 reading go to the owner for approval (section 8)
before U4 is dispatched.

## 0. Findings of t-1212 -> where fixed

| Finding | Where fixed in r2 |
|---|---|
| R1 (passage vs refusals with a door, AR-28, P22/AR-17) | fixed at §3.1 Invariant: the critic's sentence in meaning (a refusal naming a door the receiving role can take is not a block; the gate never passes either, AR-28; the move goes to the owning role or the conductor's seam, AR-17, P22); Carriers gain FR-2, AR-9, AR-17, AR-28, P15. Legend half: moot in form — with short cells the map carries no (i)-(iii) class scale at all; cells say "refused with a door" or "silently" in words |
| R2 (cost sentence misquotes P11/AR-12) | fixed at §2 definition, the critic's sentence verbatim in meaning |
| R3 (Q-i closed by implication; axis 10 label) | Q-i half: closed by the owner's decision — the breach sentence gains the third form (§2), AR-2 states it as decided (§3.1), Q-i leaves the open list. Q-ii half: fixed at §2 axis 10 cell ("whether that is a breach is Q-ii") |
| R4 (E5 sends the walk to report and commit) | fixed at §4.1 E5 |
| R5 (critic.md rule 22 opener stale) | fixed at §4.3 E8 + key in §7.1 |
| R6 (critic exam not addressed) | fixed at §5 (b) axis 2 and §6a item 5: commit line `Deviation: exam not run; debt F3-1` for the Lead |
| R7 (AR-2 Breakage contradicts itself) | fixed at §3.1 Breakage |
| R8 (Detector points at an undefined U6) | fixed at §3.1 Detector: the detector is described without a node id |
| R9 (t-1203 rank scale) | moot: the legend no longer names t-1203 classes and no cell carries a class (Lead decision 3) |
| R10 (no detector for a skipped walk) | fixed at §4.7 (check 42 sub-item (f)), §3.3, §5 (c); owns gain the protocol file |
| R11 (Q12 overlap; axis 34 row) | fixed at §4.3 (critic sentence separates VARIETY from Q12) and §4.6 (SIBLING_MAP axis 34 reviewers and detector rows; the optional axis 31 aspect cell applied too); owns gain SIBLING_MAP |
| R12 (witness cannot catch copy errors) | fixed at §7.1: equality of the normalised insert and AR-2 block against THIS file's marked blocks; keys for E5, E6, R5 and the new files; negative control kept |
| R13 (short cells) | fixed at §2: four columns, one-line cells, inventory left in the digests; size in §2.1 |
| n1 (reservations thinned) | moot: short cells carry no per-object inventory; the reservations stay in the digests |
| n2 (two cutoff tests; "blocks" attaches to a missing walk) | fixed: one test, "a spec whose primary draft started before the map landed", in §2 walk text, §4.3 and §7 D8; "blocks when it stops a stage" attaches to the diff only |
| n3 (`named_by` shift) | fixed at §4.9: shift about 35 lines (estimate; the insert is shorter now) |
| n4 (`--names` form) | fixed at §4.9: `--names AR-2 variety` |
| n5 (Option B leftovers) | fixed: Option B cut from §§1, 3, 4, 6, 7 |
| n6 (builder upkeep under F8) | fixed at §5 (a) |
| n7 (AR-3 scope of the clause) | fixed at §1.1 AR-3 row |
| n8 (definition not yet the owner's) | fixed: section 8 "For the owner's approval"; §7 gates U4 on that approval |

---

## 1. AR-n, P-n, FR-n touched and how each is kept

The change is prose only: `ai-packages/qa-factory/design/architecture.md` (package text, loaded at no runtime, FR-44),
two role files, two boot files, the symmetry map and the calibration protocol. No file under `scripts/`, `references/`,
`agents/`, `skills/`, `handoffs/` changes.

### 1.1 AR-n

| AR | Touched how | How kept / change check (goes into the DoD, section 7) |
|---|---|---|
| AR-2 | its Invariant gains the passage clause; Carriers, Detector, Breakage and Change check gain one sentence each; the opener line (title) is byte-identical | "For each decision moved into code, name what the role still decides": no decision moves into code; the clause states which way code yields. "Run the changed script on a fixture shaped unlike the default": no script changes. Detector stays `test_judgment_census.py` + check 41 for the existing invariant; the passage clause gets `none — discipline` with the gap named (§3.3). |
| AR-1 | cited by the map ("tables"); no table or reader changes | "grep scripts/ for the shape of the problem": n/a, no code; the map names code-held closed sets (axes 7, 11) without moving them (node U7). |
| AR-3 | cited by the map ("keys") | Kept. The passage clause covers only values NO key, row or role step names; a key's own declared default (`absent_means`) is AR-3's and outside the clause's scope (n7). No template row, key or interview topic changes. |
| AR-7 | cited by the definition (code yields to the role) | No step moves to code; `stage_compare.py`: n/a. |
| AR-9 | cited by the passage clause (a refusal naming a usable door is not a block) | Not edited; no refusal added or changed. |
| AR-12 | cited by the definition: code that makes a stage dearer stays a defect | AR-12's text is NOT edited. A role's extra turns on an unknown shape are role work that buys quality, not code friction (R2). `code_friction` before/after: "not measured — no hook, guard, validator or role-called script changes". |
| AR-17 | cited by the passage clause (no owning role -> the conductor's seam) | Not edited; no state code or seam changes. |
| AR-28 | cited by the passage clause (the gate never passes on an unknown shape; a silent default is its twin) | No gate read added or changed. |
| AR-29 | the commit's `judgment:` line | No check unit in `scripts/*.py` added, altered or moved; census ceilings unchanged. |
| others (AR-4..AR-6, AR-8, AR-10, AR-11, AR-13..AR-16, AR-18..AR-27) | not touched | Map cells name carriers of some (e.g. the host adapter under axis 8) without changing them. |

Commit lines: the form is owned by `tools/architecture_gate.py` (point there, do not copy). The builder does not commit
(§7); the Lead writes an `architecture:` line naming AR-2 with how it is kept, and `judgment: none -- prose in a design
document, role rules, the symmetry map and a calibration check; no check in scripts/ is added, altered or moved`.

### 1.2 Checks this spec adds or alters — owner and census class (AR-29, P27)

| Check | Who performs it | Owner it serves | Census class |
|---|---|---|---|
| The variety walk in the Lead's plan of a new idea | Lead; shown to the owner (step 4) | intent (the person) and judgment | n/a — not code |
| The variety walk in §1 of a package spec | designer; accepted by the Lead, reviewed by the plan critic | judgment (a role, accepted by a tier above) | n/a — not code |
| Critic Q10's VARIETY sentence on a package plan and diff | critic; verdict accepted by the Lead | judgment | n/a — not code |
| Calibration check 42 (f): walk lines and `VARIETY:` lines present | Lead at calibration (grep), reviewed by the Architect's weekly calibration | data (presence of lines) | n/a — not in `scripts/` |
| The passage clause (an invariant, not a check) | nobody mechanically; detector `none — discipline` | intent (the owner's words 17.11.2026) | n/a |
| The U4 witness script (§7.1) | builder, not committed | data (presence and equality) | n/a — never committed |

### 1.3 P-n and FR-n

- P1, P2, P22: code yields to the role, which settles an unknown itself; the conductor takes what no role owns.
- P11: code that makes a stage dearer stays a defect; P13: a person's word still passes any gate; P15: a refusal names a door.
- P27: the owner of every new check is named (1.2). P31: a `narrows` line in a walk is a fork, never a non-goal; an
  exclusion stays critic Q12's (R11).
- FR walk (PROJECT.md acceptance rule 1), by section:
  - A refusals — FR-2, FR-5, FR-57 cited by the definition and the clause; no refusal added or changed.
  - B text to a person — not changed. C contracts — FR-13 cited; no contract changes.
  - D identity — FR-59 cited (a declared safe default, never a pass). E delivery, F measurement — not changed.
  - G code — FR-30: the package text is English, no Cyrillic (`selftest.py --lang`); FR-44: the map lives in `design/`,
    loaded by designer, critic and Lead only; FR-54: siblings by the map (§5).

---

## 2. The definition and the variety map (exact text, English)

Placement (the owner, 17.11.2026, "таблицу в начале раздела A architecture.md" — "ок"): right after the heading
`## A. Universality across projects` and its blank line, before `**AR-1 — `. POSITIONAL invariant (unchanged from r1):
the inserted block contains no line starting with `## ` (`tools/architecture_index.py::scan` stops at the first `## `
that is not a lettered section heading and would drop later invariants), no line starting with `**AR-` and no bold
`**AR-<n>` (the opener count stays 29; a package test finds AR-17 by the first line starting `**AR-17`), and no test
file name (selftest reads `design/architecture.md` as prose; a new name would become gate-named).

The exact text to insert is between the two marker lines below (the marker lines are NOT inserted):

----- BEGIN INSERT (architecture.md, after `## A. Universality across projects`) -----

**Universality.** The factory is universal when no difference on the map below requires a change to its code, and on a project of any shape it works no worse than a free agent on the same model. Every difference has exactly one of three answers:

- a row in a data table, for a closed set of values (AR-1);
- a config key or an answer-registry record, asked at onboarding (AR-3);
- a role's judgment, for an open set and for everything the factory does not know yet (AR-2): the role gets what the factory has, asks the person for what is missing, and carries the work to a result.

A breach of universality is any place where code, on a value of an axis it does not know, blocks the factory (stops the role, or demands an artifact nobody on a project of that shape can produce), silently takes the branch of a default value, or hands to a person work the role could try first as a free agent would; the person gets only what the role cannot do, such as a physical device or a credential (P1, FR-5, FR-57; the owner, 17.11.2026). The extra turns of a role working an unknown shape as a free agent are not a breach when they buy quality (the owner, 17.11.2026); code that makes a stage dearer stays a defect (P11, AR-12). How code must yield is AR-2's passage clause.

**The variety map.** One row per axis on which projects differ. "Held by today" is one line: which part is a data table (AR-1), a config key or registry record (AR-3) or a role's judgment (AR-2), what is hard-coded and what it does on a value it does not know, and what is not addressed. "Proven on" names a live project, a fixture, or not proven. The bracketed id is the verdict of a frozen scout digest of 17.11.2026, which holds the per-sub-item inventory: axes 1-6 in `dev:docs/tasks/specs/reports/20261117-universality-scout-t-1200-axes-1-6.md`, axes 7-13 in `dev:docs/tasks/specs/reports/20261117-universality-scout-t-1201-axes-7-13.md`, and the stage walk of a native mobile project in `dev:docs/tasks/specs/reports/20261117-universality-scout-t-1203-mobile-stage-walk.md`. Their bounds hold here: the code places are the strongest reached, not a census of `scripts/`, and S1, S2 and S7-S9 were read through `references/stages.json` only.

| Axis | Examples | Held by today | Proven on |
|---|---|---|---|
| 1. Product language and build | Python, .NET, Java, Go, JS/TS, Kotlin/Swift; pip, maven, gradle, npm, nuget; monorepo, subfolder, several repositories | tables: manifests, code extensions, lock kinds, build identity; keys: app root, repositories, runtime, install command; role: reads the stack, writes the project's way; code: Python-shaped environment, lock and pytest helpers report other stacks as unknown (a1V) | fixture: Java, C#, TypeScript probes; live: pytest-playwright only |
| 2. What is tested | web UI, mobile app, API (REST, GraphQL, gRPC), database and data pipelines, queues, desktop, CLI, combinations | table: surfaces web, api, cli, desktop, android, ios; keys: capabilities, environments, driver, device; role: takes the lowest rung that observes; code: agent hands are browser, http and driver, cases of any other surface go to a person; an undeclared surface takes the web road silently; not addressed: database, queue, GraphQL, gRPC as surfaces (a2V) | live: web and API; device: no row has run on one |
| 3. The project's test stack | pytest, JUnit, NUnit, Playwright, Appium; BDD or code; tests in the product repository or apart; a test language unlike the product's; own case ids and fixtures | tables: runner collect forms, assertion probes (none for Kotlin or Swift), path markers, case form; keys: test roots, case id form, commands, reporter; role: confirms the framework by reading a test; code: pytest-shaped rehearsals; reporter `none` records a green run as not executed, silently; not addressed: BDD runners (a3V) | fixture: pytest, Java, C#, TypeScript, jest; live: pytest-playwright |
| 4. Starting state (flow) | code present or not; autotests present or not; requirements good, only AC, or one line; a reference system or none; the change merged, in an MR, or not written | table: side realities; keys: repositories, registry sides and reference; role: the S0 no-change question, the scout and the requirements tester ground on what exists; code: the no-change entry is offered only for a local story; requirements quality is the role's alone (a4V) | live: MR-grounded runs; fixture: a local story; a reference system: not proven |
| 5. Where requirements come from | Jira, YouTrack, Azure DevOps, GitHub Issues, no tracker; Confluence, Notion, Figma, knowledge in people's heads; ticket types | tables: tracker, source and link kinds, a Jira field table; keys: ticket adapter, sources; role: finds and judges every source, reads an unlisted tracker on its recorded route; code: source refresh and the direct client are Jira-only; an unknown command adapter is refused (a5V) | live: Jira only; fixture: file tickets |
| 6. Where the result is delivered | GitLab, GitHub, Bitbucket; an MR into the product, into a test repository, or no code; TestRail, Allure TestOps, Xray or nothing; where bugs are filed | table: VCS kinds gitlab and github; keys: external writes, VCS adapter, git conventions; role: S8/S9 delivers from data; code: case channels xray, testrail, zephyr, any other refused; MR evidence is GitLab-only; a Draft MR is assumed (a6V) | live: GitLab with Jira; GitHub, Bitbucket, TestRail, Xray: not proven |
| 7. Stand and access | local docker, a shared stand, a preview per MR, behind a VPN; SSO and 2FA; test data; how to know the build on the stand; devices and emulators | tables: build identity (container-shaped), one sign-in form; keys: access, environments, test data; role: tells a stand fault from a product one; code: seven access kinds in a tuple; a row with no URL passes S0 as in-process, silently; not addressed: SSO and 2FA beyond one form, preview stands (ax7V) | live: a Keycloak stand; device: not proven |
| 8. Machine and host | Windows, Mac, Linux; Claude Code or Codex; subscription or gateway; prompt-cache settings (P25); no internet | tables: host forms, driver infra, path markers, rates; keys: host, child environment `keep`; onboarding asks nothing here; code: the host is claude or codex only; guards read Bash and PowerShell only; not addressed: no internet, the cache TTL (ax8V) | live: macOS, Windows and POSIX defects from users, one Codex run; per-OS fixture: not determined |
| 9. People and process | who answers questions and how fast; manual testers; who reviews tests; regression policy; what "done" means | tables: approval words, question thresholds, manual policy; keys: dod, walkers, budget, stop point; role: finds regression without running it, routes review by impact; code: a word not in the table goes to the conductor; a main-branch fallback; not addressed: who answers and how fast (ax9V) | fixture and live: recorded answers and question counts |
| 10. Language of communication and artifacts | tickets and answers in Russian or English; the language of cases and bugs | tables: English acceptance headings and approval words; key: extra acceptance headings; role: writes every artifact in English (whether that is a breach is Q-ii); code: English bug headings refused when missing; a non-English approval word goes to the conductor; not addressed: a language key (ax10V) | not proven: no non-English fixture |
| 11. Size and shape of the task | a bugfix or an epic over several services; a task over several repositories; e2e in minutes or in hours | table: none (the XS-XL caps are a code constant); keys: sizing, windows, budget, stand wait; role: puts an XXL story to the person; code: several implementation repositories refused with a door; the install timeout sits below an assumed host cap (ax11V) | fixture: sizing goldens, two repositories; live: an S5 of 12.5 hours |
| 12. Kinds of checks and constraints | functional, load, security, accessibility; external integrations; personal data, a regulated domain | table: side realities; keys: integrations, the PII rule; role: masks everything it writes; code: S0 says v0 covers functional testing only (Q-iii); CLI and desktop checks go to a person; not addressed: load, security, accessibility, regulated domains (ax12V) | not determined |
| 13. The project's age in the factory | the first onboarding or the hundredth story; a project from an old factory version; several stories in parallel | tables: install path classes, config migrations; key: schema version; role: rediscovery re-reads only what was unreachable; code: parallel stories guess the newest pipeline, silently; one run per stand on a lease (ax13V) | fixture: an old-generation project, migration, parallel stories |

**Open owner questions** (17.11.2026, not decided; the record is `dev:docs/tasks/specs/20261117-universality-variety-map-spec-r2.md`, section 6):

- Q-ii: roles write every artifact in English whatever the ticket's language. Is the artifact language a project fact?
- Q-iii: "v0 covers functional testing only". Is that a declared scope, or a place where AR-2's passage clause applies?

**How the map is walked.** Three places walk it, axis by axis: the Lead's plan of a new idea (`dev:PROJECT.md`, new-idea step 4), §1 of a package spec (`dev:.claude/agents/designer.md` rule 1), and the critic of a package plan or diff (`dev:.claude/agents/critic.md` rule 22 question 10 and rule 24). Every axis is named by its number: one line for each axis the change meets, in the first or the third form, and the axes it does not meet in `n/a` lines, which may group several numbers under one reason:

- `axis N: held by table|key|role -- <carrier>; unknown value -> <what the code does>`
- `axes N, N, ...: n/a -- <why the change does not meet them>`; an `n/a` line that names no axis number is not a walk
- `axis N: narrows -- <which projects lose what>`; a `narrows` line is a fork for the Lead and the owner (one road, P31), never a non-goal.

A change that meets no axis writes the one line `variety: none -- <reason>` instead of thirteen. A spec whose primary draft started before this map landed owes no walk. A builder dispatch carries no walk: it points at its spec's §1. A change that alters how an axis is held (a new table row, key or role step, a code site removed) edits that axis's line of the map in the same commit; the frozen digests stay the evidence of 17.11.2026.

----- END INSERT -----

### 2.1 Checks of the insert

- Edge (2) — no empty cell: every cell above is non-empty; an axis part nothing addresses is written "not addressed"
  (axes 2, 3, 7, 8, 9, 10, 12); the axes with no such part (1, 4, 5, 6, 11, 13) have none in their digests' verdicts.
  The per-part "what a role does there today" moved to the digests with the inventory.
- Edge (3) — Q-i is written as decided (definition, AR-2); Q-ii stands in the axis 10 cell and the list, Q-iii in the
  axis 12 cell and the list; no text answers them.
- Edge (5) — no `## ` line, no line starting `**AR-`, no bold `**AR-<n>`, no test file name, no Cyrillic (by reading;
  the builder's script checks it).
- SIZE (estimate, not verified — counted by hand per line; the builder's script prints the measured bytes): definition
  about 1.2 KB, legend about 0.9 KB, map about 6.0 KB (examples about 1.8 KB, held-by about 3.3 KB, proven-on about
  0.8 KB, row framing), open questions about 0.4 KB, walk about 1.0 KB: about 9.5 KB in about 35 lines, against r1's
  measured 19,269 B and the Lead's target of about 6 KB. Over the target: fork F11.

---

## 3. The passage rule: exact text, place, detector

Place: AR-2, widened, title unchanged (F1 = A): index and boot bytes unchanged, 29 of 30 entries.

### 3.1 The new AR-2 block

It replaces the current five bullet lines of AR-2; the opener line stays byte-identical. The text is between the marker
lines (not inserted):

----- BEGIN AR-2 -----
**AR-2 — Open variety is a role's judgment; code reports and leaves a move.**
- Invariant: some variety no table can close: layouts, id spellings, sources, frameworks, a person's or role's wording. The owning role or the conductor judges it. Code triggers on a field, a state or the presence of words, reports what it found, and never decides meaning. Passage: on a project shape the factory does not know (a value of a variety axis that no table row, key or role step names), code never blocks and never takes a default branch silently; it says what it could not establish and leaves the move to the owning role, or to the conductor's seam when no role owns the state (AR-17, P22). The gate never passes on such a shape either (AR-28). A refusal that names a door the receiving role can take (FR-2, FR-57, AR-9, P15) is not a block. The role proceeds as a free agent on the same model would, with what the factory already has (onboarding answers, testing knowledge, the critic), asks the person for what it cannot find, and carries the stage to a result. Work that code hands to a person goes to the role first; the person gets only what the role cannot do, such as a physical device or a credential, and a door that leads to a person past the role is not passage (the owner, 17.11.2026). A stage may cost somewhat more or take longer when that buys quality; it does not block (the owner, 17.11.2026). A default is silent unless it is declared in data and the run says it was taken (FR-59, AR-28). A safety refusal stays a refusal (AR-29), and a person's word still passes any gate (P13).
- Carriers: FR-2, FR-12, FR-13, FR-47, FR-57, FR-59, P1, P2, P15, P22, P31; AR-9, AR-17, AR-28; `handoffs/README.md` "When the judge is on" (a judged value never lifts a block); the variety map at the head of this section.
- Detector: the census (AR-29): test_judgment_census.py; calibration check 41. Gap: FR-47's check ("run the script on a project shaped differently") has no gate, and nothing scans for phrase lists (FR-12). Passage: none — discipline; no gate finds a block, a silent default or a hand-off past the role on an unknown shape. Calibration check 42 (f) sees a skipped variety walk, not the behaviour. The planned detectors are a live comparison of the factory with a free agent on the same model on a project of a shape the factory does not know, and the scoreboard's free-agent bar, which has no writer yet (AR-12).
- Breakage: FR-13's record. On TP1-13877 the contract knew only `TC-\d+` while the project wrote `TP1-13877_TC_001`. The automator spent about 35 calls reading factory code, then halted. Passage: the same record — an id form the contract did not know halted the role.
- Change check: for each decision moved into code, name what the role still decides. Add no regex over prose meaning. Run the changed script on one fixture shaped unlike the default; it must report, not halt. A change that reads the value of a variety axis says what it does on a value it does not know (report and leave the move; never block, never a silent default, never a hand-off to a person past the role) and gives the variety walk of this section.
----- END AR-2 -----

Note for the builder: `test_judgment_census.py` already stands in the current AR-2 Detector line (no new test name).
The marker lines are the spec's quoting only.

### 3.2 Detector, honestly

The behaviour (a block, a silent default, a hand-off past the role on an unknown shape): `none — discipline`, gap named
in AR-2's Detector field. The walk: the plan critic (mandatory for a new idea), critic Q10's VARIETY line on every
package plan and diff it reviews, and calibration check 42 (f) (F6 = b), which also sees the escapes the critic cannot:
a `critic: skipped` diff's spec, a Lead-drafted package spec below the designer threshold, a verdict missing its
`VARIETY:` line. Promotion to a code layer follows evidence of a leak (CLAUDE.md rule 10 (d)).

---

## 4. Exact edits per file (path::anchor, old -> new), byte deltas for boot files

All files land in ONE commit (temporal edge D8: the role and policy texts point at a map that does not exist before
that commit; a split leaves a rule pointing at nothing).

### 4.1 `ai-packages/qa-factory/design/architecture.md`

E1 — `architecture.md::intro paragraph (line 3)` — a stale pointer met in the node's reach (fixed here, designer rule 2):
- old: ``the owner's principles in `dev:PROJECT.md` (P1-P23)``
- new: ``the owner's principles in `dev:docs/OWNER_PRINCIPLES.md` (P1-P31)``

E2 — `architecture.md::**Who reads it.**`:
- old: `the designer drafting a package spec, and the critic on a package diff.`
- new: `the designer drafting a package spec, the Lead writing the plan of a new idea (the variety walk of section A), and the critic on a package plan or diff.`

E3 — `architecture.md::## A. Universality across projects` — insert the block of §2 after the heading's blank line,
followed by one blank line before `**AR-1 — `.

E4 — `architecture.md::**AR-2 — ` — replace the five bullet lines with those of §3.1.

E5 — `architecture.md::## How a change walks this map` step 2 (R4):
- old: `A change that touches none says so in one line, with the reason. An invariant the change cannot keep is stated, never reworded.`
- new: `A change that touches none says so in one line, with the reason. The variety walk of section A goes into the spec's §1 (and the Lead's plan of a new idea); the report and the commit point at it. An invariant the change cannot keep is stated, never reworded.`

E6 — same section, step 9:
- old: `The critic asks four questions. Which AR-n is touched but not named? Is each change check done? Was the producer-reader walk controlled? Is every raise named?`
- new: `The critic asks five questions. Which AR-n is touched but not named? Is each change check done? Was the producer-reader walk controlled? Is every raise named? On a project of what shape does the change break, and does the factory there still pass no worse than a free agent (section A)?`

Sweep of the enclosing block "How a change walks this map" (rule 9, artifact first): step 1 n/a (grep by changed file);
step 2 applied (E5); step 3 n/a (the map-line upkeep duty lives in the walk text of §2); step 4 n/a (SIBLING_MAP walk
unchanged); steps 5-7 n/a (FR walk, friction, ratchets); step 8 n/a (it already covers a `none — discipline` detector);
step 9 applied (E6); step 10 n/a (no new invariant). Section A's invariants: AR-1 n/a (its change check already routes a
value the table lacks to AR-2); AR-2 applied (E4); AR-3 n/a (the clause's scope excludes declared key defaults, n7);
AR-4, AR-5, AR-6 n/a.

Not boot: architecture.md is loaded at no boot or runtime; AR titles unchanged, so `docs/ARCHITECTURE_INDEX.md` stays
byte-identical.

### 4.2 `.claude/agents/designer.md` (not boot)

`designer.md::rule 1, last sentence` — after `` `judgment: none` always carries its ` -- <why>`, and a spec never prescribes it bare.`` append:
- new: ` The same §1 carries the variety walk of `design/architecture.md` § A, every axis named by its number in the forms that section owns, or its one line `variety: none -- <reason>`; a `narrows` line is also a fork (rule 6).`

The rule's anchored first line (`tools/install_parity_anchors.json`) is untouched.

### 4.3 `.claude/agents/critic.md` (not boot)

E7 — `critic.md::rule 22, Q10` — at the end of the Q10 line, after `(blocks when a reader is starved).` append (R11, n2):
- new: ` VARIETY (§ A of the same file: its variety map and AR-2's passage clause), on its own verdict line `VARIETY:`: on a project of what shape does the diff break, and does the factory there still pass the stage no worse than a free agent on the same model, with no block, no silent default and no hand-off to a person past the role on a value it does not know? An exclusion from a shared mechanism stays Q12; VARIETY asks the unknown-value behaviour. A package spec whose §1 lacks the variety walk is a finding; a diff that blocks, defaults silently or hands the role's work to a person on an unknown value is a finding that blocks when it stops a stage. A spec whose primary draft started before the map landed owes no walk; the critic answers the question itself.`

E8 — `critic.md::rule 22 opener` (line 192) (R5):
- old: `(Q4, Q6 and Q12 also on a plan gate, rule 24)`
- new: `(Q4, Q6, Q12 and Q10's VARIETY sentence also on a plan gate, rule 24)`

E9 — `critic.md::rule 24`:
- old: `answer Q13 below and Q4, Q6 and Q12 of` / `rule 22 (read "the diff" as "the plan")`
- new: `answer Q13 below and Q4, Q6, Q12 and Q10's VARIETY sentence of` / `rule 22 (read "the diff" as "the plan")`

Sweep of the critic.md artifact (rule 9): every place listing the plan-gate questions — the rule 22 opener (E8) and
rule 24 (E9) — applied; Q12 (axis 34) not edited, separated by the new sentence; Q11 n/a (no judgment moves).

### 4.4 `PROJECT.md` (boot)

`PROJECT.md::Как разрабатывается новая идея владельца, step 4`:
- old: `что меняется, фазы, какие AR/P затронуты и` / `с какими идеями и пачками в работе это пересекается (...)`
- new: `что меняется, фазы, какие AR/P затронуты, вердикт по каждой оси карты различий (`architecture.md` § A) и` / `с какими идеями и пачками в работе это пересекается (...)` (the builder rewraps at the file's width).

Added: 94 bytes (measured by the plan critic, t-1212 K4) plus a rewrap.

### 4.5 `CLAUDE.md` (boot) — F5 = (b)

`CLAUDE.md::Rule 10 · a change to the package`, the "change together" sentence:
- old: `This` / `paragraph, critic question 11 and designer rule 1 change together (axis 1).`
- new: `This` / `paragraph, critic questions 10-11, designer rule 1 and new-idea step 4 change together (axis 1).`

Added: 21 bytes (measured, t-1212 K4) plus at most 4 for a rewrap.

### 4.6 `docs/SIBLING_MAP.md` (not boot) — R11

S1 — `SIBLING_MAP.md::Axis 34, row "The reviewers"`:
- old: `a kept exclusion is named in the verdict like a ratchet raise |`
- new: `a kept exclusion is named in the verdict like a ratchet raise; the variety walk of `ai-packages/qa-factory/design/architecture.md` § A (designer rule 1, critic Q10's VARIETY sentence) asks what code does on a value it does not know, Q12 asks whether a side is left out |`

S2 — `SIBLING_MAP.md::Axis 34, row "The detector"`:
- old: `| The detector | calibration check 42 (spec t-2065 §5.6);`
- new: `| The detector | calibration check 42 (spec t-2065 §5.6; its sub-item (f) for the variety walk);`

S3 — `SIBLING_MAP.md::Axis 31, row `ai-packages/qa-factory/design/*.md``, the aspect cell (optional per t-1212; applied):
- old: `the factory building rules and the architecture invariants (FR-n, AR-n)`
- new: `the factory building rules, the architecture invariants (FR-n, AR-n), and the variety map with its walk form (architecture.md § A)`

No axis heading changes (`tools/mechanism_gate.py` reads the headings; the axis count stays 38).

### 4.7 `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` (not boot) — R10, F6 = (b)

C1 — `WEEKLY_CALIBRATION_PROTOCOL.md::42.`, the Mechanism sentence:
- old: `Mechanism: designer rule 6, critic rule 19 with brief question 12;`
- new: `Mechanism: designer rule 6, critic rule 19 with brief question 12; for (f), designer rule 1's variety walk and critic question 10's VARIETY line (`ai-packages/qa-factory/design/architecture.md` § A);`

C2 — same check, after `(e) an empty window gets an explicit line.` insert:
- new: ` (f) the variety walk: every spec of the window that changes `ai-packages/qa-factory/` carries in its §1 `axis N:` lines or one `variety: none --` line (`grep -L -E "axis [0-9]+: |variety: none --" <spec>` lists the misses; positive control: `docs/tasks/specs/20261117-universality-variety-map-spec-r2.md` must not be listed), unless its primary draft started before the map landed; every critic verdict of the window on a package plan or diff carries a `VARIETY:` line; a miss is a finding against the designer (`failure_class=spec`) or the critic.`

C3 — same check, the leak-detector sentence:
- old: `whose spec or verdict this check passed.`
- new: `whose spec or verdict this check passed. For (f): findings of the class (code blocks, defaults silently or hands the role's work to a person on a project shape it does not know) dated in the window whose spec or verdict (f) passed.`

About 900 bytes, outside boot (estimate, not verified).

### 4.8 Boot byte budget and generated copies

Boot at brief time and at the critic's run: `BOOT BUDGET: 112646 bytes / 120000 ... WARN` (t-1212 rerun). Delta:
PROJECT.md 94 + rewrap, CLAUDE.md 21 + at most 4; index 0: about +123, to about 112,769 (the exact after-size is the
builder's measurement, D10). SIBLING_MAP.md and the protocol are not boot. No offset inside this change (F5 = b; the
delta is recorded for the boot-diet batch). `AGENTS.md` is regenerated in the same commit (`python -B tools/agents_md.py`);
only the CLAUDE.md and PROJECT.md edits change it (it takes frontmatter only from role files, t-1212 K6).

### 4.9 Readers of every touched file (designer rule 7)

The plan critic ran `python -B tools/owns_readers.py --paths <the five r1 files> --names AR-2 variety` (the working
`--names` form, n4) on base b5fca9bd; its block and answers (t-1212 K6), carried over:

| line | answer |
|---|---|
| names AR-2 (surfaces.json, request-call-patterns.json, test-layers.json) | unchanged: the AR-2 id and title stay byte-identical |
| names variety (about 67 hits) | miss 7, a common word: nothing owed |
| more (five files) | interface kept: prose appends only; no anchored line start and no pinned phrase changes |
| miss 1 | `--witness-for design/architecture.md` -> the two keep rows; in the DoD |
| miss 3 | "four questions" -> "five" is pinned nowhere |
| miss 6 | base is origin/main: yes |

The two files r2 adds (SIBLING_MAP.md, WEEKLY_CALIBRATION_PROTOCOL.md) had no `owns_readers` block (no shell). Hand
grep (Grep tool, case-sensitive; positive control of the same shape: `architecture` over `.githooks/` = 2 files):
`SIBLING_MAP` over `tools/**/*.py`: 22 files; `WEEKLY_CALIBRATION_PROTOCOL` over `tools/**/*.py`: 13 files; either over
`.githooks/`: 0. The Lead re-runs `owns_readers.py --paths docs/SIBLING_MAP.md PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`
before the dispatch, or the critic of the diff does (Q13 (d)).

| Touched file | Reader | Verdict |
|---|---|---|
| architecture.md | `tools/architecture_index.py`, `architecture_gate.py`, their tests, `.githooks/pre-commit` | unchanged; D1/D2/D11 keep the parse |
| architecture.md | `tools/tests/test_role_carriers_one_owner.py` | unchanged; no brief path cited (D5); in the witness |
| architecture.md | `tools/test_quarantine.py` (`PACKAGE_PROSE`, `gate_named_files`), `selftest.py` `_PROSE_CARRIERS` | unchanged; no new test name (D3) |
| architecture.md | `scripts/tests/test-layers.json` `named_by` `design/architecture.md:<line>` | unchanged; anchors shift by about 35 lines (n3, estimate); selftest checks non-emptiness only |
| architecture.md | `test_conductor_investigates_first.py`, `test_sizing_impact_scale.py`, `test_selftest_slow_tests.py` | unchanged; AR-17 and AR-22 not edited |
| designer.md, critic.md | `tools/install_parity_anchors.json` + `install_parity.py --check`; `test_handoff_rule_anchors.py` | unchanged; appends only, anchored line starts untouched; in the witness |
| designer.md, critic.md | dispatch/journal tools reading role names or handoff paths | unchanged (owns_readers "more" line) |
| CLAUDE.md, PROJECT.md | `tools/agents_md.py`; `session_context.py` boot budget; `test_role_carriers_one_owner.py` TOC | AGENTS.md changes in this stream; budget line grows by 4.8's delta; TOC unchanged |
| SIBLING_MAP.md | `tools/mechanism_gate.py` (`MAP_PATH`, axis headings for the rule 10 (b) block) | unchanged; no heading added or renamed, 38 axes |
| SIBLING_MAP.md | `tools/tests/test_role_carriers_one_owner.py::main_documents` (axis 31 table: File and Owner / pointer cells only) | unchanged; S3 edits the aspect cell only; in the witness |
| SIBLING_MAP.md | `tools/test_quarantine.py` `FORGE_CARRIERS` (test names in carriers) | unchanged; S1-S3 name no test file |
| SIBLING_MAP.md | the other 18 hand-grep hits (comments and docstrings citing an axis: agent_budget, claim_control_gate, dispatch_gate, exam_runner, gitcmd, handback_extract, handoff_gate, hop_metrics, language_sites, negative_lint, session_context, judge_calib_sanitize, test_digest_form, test_mechanism_gate, test_language_sites, test_split, test_wiring_check, tier_ladder, transcripts) | unchanged by assumption: cite axis numbers, none renumbered; not opened |
| WEEKLY_CALIBRATION_PROTOCOL.md | `tools/test_handoff_rule_anchors.py` (check 28 anchors) | unchanged; check 28 not edited; in the witness |
| WEEKLY_CALIBRATION_PROTOCOL.md | `tools/warn_density.py` (block "WARN LAYER DENSITY") | unchanged; that block not edited |
| WEEKLY_CALIBRATION_PROTOCOL.md | `tools/test_quarantine.py` `FORGE_CARRIERS` | unchanged; C2 names no test file |
| WEEKLY_CALIBRATION_PROTOCOL.md | `tools/dispatch_gate.py` (check-number anchor class, not ported), `journal_validator.py`, `journal_echo.py`, `hook_liveness_probe.py` and the remaining tests (comments citing checks) | unchanged: no check renumbered; (f) is a new sub-item letter of 42 |

---

## 5. The four questions of CLAUDE.md rule 10

Mechanism: "the variety map and its walk" (a duty for the Lead's plan, the designer's §1 and the critic, with check 42 (f))
plus the passage clause (an invariant of the package's design). One block covers both.

(a) Cost and who pays. The Lead: up to 13 lines per new-idea plan, and one more sub-item per weekly calibration. The
designer: up to 13 lines in §1 per package spec, or one `variety: none` line. The critic: one more verdict line per
package plan and diff. Every session: about +123 boot bytes. The builder: one map line when its diff changes how an axis
is held, as its spec prescribes (F8); no walk otherwise (n6).

(b) SIBLING_MAP axes, by enumeration:
- axis 1 (Policy <-> role files <-> journal): covered — CLAUDE.md rule 10 paragraph, designer.md rule 1, critic.md Q10,
  opener and rule 24, PROJECT.md step 4 in one commit; AGENTS.md regenerated.
- axis 2 (per-tier exam instruments): covered — critic.md is edited, its rule 10 owes `PROCESS/CRITIC_EXAM.md`, which is
  absent (generated at onboarding, PROCESS/README.md); the commit carries `Deviation: exam not run; debt F3-1` (precedent
  1f165a38, worker-boot r2 spec) (R6).
- axis 3 (package <-> release copy <-> installed plugin): covered — architecture.md travels with the next release; no
  runtime reader (FR-44); nothing edited in a release copy or cache.
- axis 4 (rules <-> debt <-> backlog <-> principles): covered — index unchanged (no title change), AGENTS.md regenerated;
  no FR or principle added; debt rows for the breaches the map names: F9 = (a), node U7.
- axis 5 (stage twins): n/a — no stage logic changes.
- axis 6 (measurement tools <-> package): n/a — no measurer changes; the free-agent bar's missing writer is named as a
  planned detector (AR-12's existing gap).
- axes 7-11 (per-test identity, story on disk, "is this a test file", git-top readers, shell-command recognizers): n/a —
  no code touched.
- axis 12 (carriers of the work plan): covered — the idea's DAG stays in its brief file (rule 4a); this file is the record
  of U2 r2; statuses move with the journal events.
- axis 13 (the dispatch text): covered — a builder dispatch carries no walk and points at its spec's §1.
- axes 14-17 (transcripts, console stream, one JSON reader, detector verdict shape): n/a — no code, no detector output.
- axis 18 (shrink-only ratchets): n/a — no ratchet row; the index cap is a cap, 29 of 30 unchanged.
- axes 19-20 (`tools:` line reader, host receipt names): n/a.
- axis 21 (markdown table readers): covered — the map is a table inside section A, where `architecture_index.py` reads no
  table; the SIBLING_MAP axis 31 table edit keeps the File and Owner / pointer cells its reader parses.
- axes 22-30 (host return form, `tests[]` row fields, execution record, run freshness, `stand not confirmed`, test-row
  profile, row-form render site, append-only jsonl writers, profile commands): n/a — cited by the map at most, not changed.
- axis 31 (role carriers: one owner per aspect): covered — the walk form and the passage clause have ONE owner,
  architecture.md section A, now named in the `design/*.md` row's aspect cell (S3); designer.md, critic.md, PROJECT.md,
  CLAUDE.md, SIBLING_MAP and check 42 carry pointers and their own consequence; no new document.
- axis 32 (where judgment lives): covered — no check unit added; every new check is a role's judgment accepted by a tier
  above or a presence read at calibration (1.2); `judgment: none -- <why>`.
- axis 33 ("which dispatch am I"): n/a.
- axis 34 (one road): covered — the passage clause is the one road for an unknown shape; Q12 keeps exclusions, VARIETY
  asks the unknown-value behaviour (E7); the axis 34 reviewers and detector rows name both (S1, S2) (R11).
- axes 35-38 (sides of a story, the substitute row, a repeat stop, the dry census): n/a — cited at most, not changed.

(c) Detector, registered: for the walk — calibration check 42 (f) in `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` (C2), plus
the plan critic and critic Q10 as named detectors; for the passage clause — `none — discipline`, gap named in AR-2's
Detector field; planned: the live comparison with a free agent and the free-agent bar.

(d) What stops it from being skipped: designer rule 1 is loaded with every designer dispatch; critic Q10 with every
critic dispatch; new-idea step 4 is in PROJECT.md, loaded every session; the plan critic is mandatory for a new idea. No
code gate: "on discipline alone, detector: calibration check 42 (f)". Promotion to a commit-msg line follows a leak in
the log, not symmetry.

---

## 6. Forks: decided, open, new

| Fork | State |
|---|---|
| F1 place of the passage rule | decided by the Lead: A (AR-2 widened, title unchanged). Options B (a new invariant) and C (retitle) are cut |
| F2 / Q-i hand-offs to a person | decided by the OWNER 17.11.2026: (b) the role first; written into §2 and §3.1 |
| F3 / Q-ii artifact language | OPEN, the owner's. Options: (a) English always; (b) a config key with default English, asked at onboarding, English-only checks become language rows; (c) the ticket's language by role judgment. Designer's recommendation (b), unchanged from r1 |
| F4 / Q-iii "functional only" | OPEN, the owner's. Options: (a) a declared scope; (b) the passage clause applies; (c) declared scope plus a door by the person's word. Designer's recommendation (b), unchanged from r1 |
| F5 boot bytes | decided: (b) |
| F6 detector of the walk | decided: (b) — check 42 (f) |
| F7 meaning of "silently" | decided by the Lead: (a) declared in data and said in the run; shown to the owner (section 8) |
| F8 map upkeep | decided: (a) — one line edited in the same commit |
| F9 debt rows | decided: (a) — node U7 |
| F10 the walk's length | decided by the Lead 17.11.2026: neither (a) nor (b) as worded. Every axis is named by its number; a met axis gets its own line; unmet axes go into `n/a` lines that may group numbers under one reason; `other axes: n/a` with no numbers is not a walk (the owner's reason for the map is that axes get forgotten, so each one is looked at by name). §2 walk text and §4.2 are edited to this form |
| F11 insert size | decided by the Lead 17.11.2026: (a) accept. Measured: the insert was 10,193 B before the F10 edit |

New forks of r2:

F10 — The walk's length (t-1212 K7, second half; the Lead's decision 3 named short cells, not the walk form). Options:
(a) keep r1's form: thirteen lines, or `variety: none -- <reason>` when no axis is met; (b) the critic's form: lines for
the met axes only, plus one line `other axes: n/a`; `variety: none -- <reason>` stays for a change that meets none.
Recommendation: (b) — most package diffs meet one or two axes (t-1212 K7), and thirteen `n/a` lines bury them; cost: a
silently skipped axis reads as n/a, which the critic's VARIETY question has to catch. If (b): in §2's walk text replace
"One line per axis, in one of three forms:" by "One line per axis the change meets, in one of three forms, then one line
`other axes: n/a`:", and in §4.2 replace "one line per axis in the form that section owns" by "one line per met axis in
the form that section owns"; check 42 (f)'s grep is unaffected. The §2 insert above is written for (a) until decided.

F11 — Insert size over the target (§2.1: about 9.5 KB, estimate, against about 6 KB). Options: (a) accept: half of r1,
one line per cell, the examples are the owner's own list; (b) cut the Examples column to three or four per axis and drop
the legend's sentence on digest bounds: about 8 KB; (c) reach 6 KB by dropping the Examples column (it lives in the brief,
which no main document may cite — so the examples would be lost to walkers). Recommendation: (a).

Noticed, not widened (designer rule 3): check 42 is titled "One road for one action"; (f) is a sibling sub-item hosted
there per t-1212 R10, not a retitle. If the Lead prefers its own check number, that is a new check (a fork with the
same owns), not a builder choice.

## 6a. Small technical choices closed by the designer (no design weight)

1. The critic's variety question is a sentence appended to Q10 with its own verdict line `VARIETY:` (check 42 (f) greps
   it), not a new Q14; no question is renumbered.
2. architecture.md's "How a change walks this map" gets sentences inside steps 2 and 9; no step is added.
3. The insert cites no test file name and no brief path; fixtures are cited by description.
4. No changelog fragment: `design/` is not loaded at runtime and this is not a pile batch.
5. The builder does not commit: the commit touches mechanism paths (CLAUDE.md, PROJECT.md, role files, SIBLING_MAP.md,
   PROCESS/). The Lead commits after acceptance with: `tier: opus`; §5 as the axis block; the `architecture:` and
   `judgment:` lines in the form of `tools/architecture_gate.py`; and `Deviation: exam not run; debt F3-1` for critic.md
   (R6).
6. Cells cite only digest verdict ids (a1V ... ax13V); the legend names the three digests once.
7. Map cells use plain `AR-n` (no bold).
8. §7 edges are numbered D1-D11 so they do not collide with the edit ids E1-E9 of §4.
9. The AR-2 block in §3.1 is quoted between marker lines, not a fence, so the witness script can cut it exactly.

---

## 7. The builder dispatch for U4

GATE: U4 is not dispatched before the owner's approval of section 8 is recorded in the brief («Решено владельцем»), and
before F10 and F11 are decided (a decided F10 = (b) edits §2 and §4.2 of this file first, so the equality check reads
the final text). Header lines are printed by `python -B tools/dispatch_new.py`; their content is below. `<wt>` is the
builder's worktree root.

- given: this spec r2 (§2, §3.1, §4); `ai-packages/qa-factory/design/architecture.md`;
  `ai-packages/qa-factory/design/factory-rules.md` (whole, PROJECT.md acceptance rule 1); `.claude/agents/designer.md`;
  `.claude/agents/critic.md`; `PROJECT.md`; `CLAUDE.md`; `docs/SIBLING_MAP.md`; `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`;
  `tools/architecture_index.py` (parse rules).
- owns:
  C:/QAFactory/forge-repo/ai-packages/qa-factory/design/architecture.md
  C:/QAFactory/forge-repo/.claude/agents/designer.md
  C:/QAFactory/forge-repo/.claude/agents/critic.md
  C:/QAFactory/forge-repo/PROJECT.md
  C:/QAFactory/forge-repo/CLAUDE.md
  C:/QAFactory/forge-repo/AGENTS.md
  C:/QAFactory/forge-repo/docs/SIBLING_MAP.md
  C:/QAFactory/forge-repo/PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md
  (the worktree paths are printed by `dispatch_new.py`.)
- non-goals: no file under `scripts/`, `references/`, `agents/`, `skills/`, `handoffs/`; no fix of any place the map
  names (node U7); no teaching of mobile (U8); no new document; no boot text beyond §4.4/§4.5; no edit of
  `test-layers.json` line anchors; no new invariant and no index regeneration; no answer to Q-ii or Q-iii; no commit.
- handoff: the uncommitted diff in the worktree + the report in the form of `.claude/agents/builder.md` rule 7 with the
  witness (every command below, verbatim tail) and the witness script in full source.
- edges (each with the invariant it protects):
  - D1 no line starting `## ` between `## A. Universality across projects` and `**AR-1 — ` — invariant: the index
    generator still sees all four sections and all 29 openers.
  - D2 no line starting `**AR-` and no bold `**AR-<n>` in the inserted text — invariant: exactly 29 openers, and the
    package test still finds the real AR-17 first.
  - D3 no test file name in the inserted text — invariant: the gate-named test set is unchanged.
  - D4 no Cyrillic character in architecture.md (FR-30) — invariant: `selftest.py --lang` stays green.
  - D5 no touched file cites the brief file — invariant: no role must read a brief; `test_role_carriers_one_owner.py`
    stays green.
  - D6 every map cell non-empty; a part nothing addresses reads "not addressed" — invariant: no axis reads as covered by
    silence.
  - D7 Q-i written as decided, Q-ii and Q-iii as questions — invariant: no owner decision is written or dropped by a
    builder; the inserted text equals §2/§3.1 (the script checks it).
  - D8 TEMPORAL: all files in one commit — before it, no rule points at a missing map; after it, a spec whose primary
    draft started after the map landed owes the walk, an earlier one owes none and is no critic finding.
  - D9 AR-2's opener line byte-identical; `architecture_index.py --check` green with no regeneration; an exit other than
    0 is a stop-and-report, never a title or a text trimmed by the builder.
  - D10 boot bytes: `wc -c <wt>/CLAUDE.md <wt>/PROJECT.md` before the first edit and after the last; a delta above 185
    bytes (1.5 times §4.8's estimate) is a report line, never a trim of other text.
  - D11 POSITIONAL: the insert sits after the section A heading and before AR-1; the summary table before the first
    section is unchanged — invariant: `verify()` finds table and headings agreeing.
  - D12 the equality check fails on any copy difference beyond whitespace — invariant: what lands is what the critic and
    the owner read; a needed deviation is a question back, never an edit of the text.
- DoD (acceptance keys: the eight files carry the texts of §§2-4 as decided; every command below exits 0; the script
  prints `ALL KEYS PRESENT`, `INSERT EQUAL`, `AR-2 EQUAL` and `NEGATIVE CONTROL: red as expected`):
  1. `python -B <wt>/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/design/architecture.md` — run what it prints.
  2. `python -B <wt>/tools/architecture_index.py --check`
  3. `python -m pytest <wt>/tools/test_architecture_index.py <wt>/tools/tests/test_role_carriers_one_owner.py <wt>/tools/test_handoff_rule_anchors.py <wt>/tools/test_mechanism_gate.py -q`
  4. `python -B <wt>/tools/install_parity.py --check`
  5. `python -B <wt>/tools/agents_md.py` then `python -B <wt>/tools/agents_md.py --check`
  6. `python -B <wt>/ai-packages/qa-factory/scripts/selftest.py --lang`
  7. `python -B <scratchpad>/u4_keys.py <wt> C:/QAFactory/forge-repo/docs/tasks/specs/20261117-universality-variety-map-spec-r2.md`
  8. `wc -c <wt>/CLAUDE.md <wt>/PROJECT.md` (before and after, D10)
  - test: none -- documents; the witness is the DOC-DISPATCH key-presence and equality run (CLAUDE.md rule 11) | expected from: spec r2 §2, §3.1, §4
  - AR-n change checks (from §1): AR-2 — "no decision moves into code; no script changed" in words; AR-12 —
    "code_friction: not measured — no hook, guard, validator or role-called script changes"; AR-29 — no census edit.
- siblings: none -- the class walk is §5 (all 38 axes); the artifact sweeps are in §4.1 and §4.3.
- designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261117-universality-variety-map-spec-r2.md

### 7.1 The DOC-DISPATCH witness script (attached in full to the report, never committed)

Keys are quoted verbatim from §4 before the run; matching is whitespace-normalised. The equality blocks are read from
this spec file itself (the first marker lines of each pair, which stand in §2 and §3.1, before this section). The script
runs its own negative control (the arch text with one key removed -> must report failure on both a key and equality).

```python
"""t-1216 / U4 witness (doc dispatch). Not committed. Usage: python -B u4_keys.py <root> <spec-r2 path>"""
import pathlib
import re
import sys

ARCH = "ai-packages/qa-factory/design/architecture.md"
SMAP = "docs/SIBLING_MAP.md"
PROTO = "PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md"
FILES = [ARCH, ".claude/agents/designer.md", ".claude/agents/critic.md", "PROJECT.md", "CLAUDE.md", SMAP, PROTO]
KEYS = [
    (ARCH, "`dev:docs/OWNER_PRINCIPLES.md` (P1-P31)"),
    (ARCH, "the Lead writing the plan of a new idea (the variety walk of section A)"),
    (ARCH, "The variety walk of section A goes into the spec's §1 (and the Lead's plan of a new idea); the report and the commit point at it."),
    (ARCH, "The critic asks five questions."),
    (".claude/agents/designer.md", "the variety walk of `design/architecture.md` § A"),
    (".claude/agents/critic.md", "on its own verdict line `VARIETY:`"),
    (".claude/agents/critic.md", "An exclusion from a shared mechanism stays Q12; VARIETY asks the unknown-value behaviour."),
    (".claude/agents/critic.md", "(Q4, Q6, Q12 and Q10's VARIETY sentence also on a plan gate, rule 24)"),
    (".claude/agents/critic.md", "Q4, Q6, Q12 and Q10's VARIETY sentence of"),
    ("PROJECT.md", "вердикт по каждой оси карты различий (`architecture.md` § A)"),
    ("CLAUDE.md", "critic questions 10-11, designer rule 1 and new-idea step 4 change together"),
    (SMAP, "Q12 asks whether a side is left out"),
    (SMAP, "its sub-item (f) for the variety walk"),
    (SMAP, "the variety map with its walk form (architecture.md § A)"),
    (PROTO, "for (f), designer rule 1's variety walk and critic question 10's VARIETY line"),
    (PROTO, "(f) the variety walk: every spec of the window that changes"),
    (PROTO, "For (f): findings of the class"),
]
BRIEF = "20261117-universality-variety-map-brief"


def norm(text):
    return " ".join(text.split())


def marked(spec, begin, end):
    b = re.search(r"^" + re.escape(begin) + r".*$", spec, re.M)
    e = re.search(r"^" + re.escape(end) + r".*$", spec, re.M)
    return spec[b.end():e.start()] if b and e and b.end() < e.start() else None


def problems(texts, insert, ar2):
    out = []
    for rel, key in KEYS:
        if norm(key) not in norm(texts[rel]):
            out.append("missing key in %s: %s" % (rel, key))
    arch = texts[ARCH]
    if re.search("[\u0400-\u04ff]", arch):
        out.append("Cyrillic character in architecture.md")
    head = "## A. Universality across projects"
    start = arch.find(head)
    end = arch.find("**AR-1 — ")
    block = arch[start + len(head):end] if 0 <= start < end else ""
    if not block:
        out.append("section A head or AR-1 opener not found in order")
    if any(l.startswith("## ") for l in block.splitlines()):
        out.append("a '## ' line inside the inserted block")
    if "**AR-" in block:
        out.append("a bold AR opener inside the inserted block")
    if re.search(r"test_[a-z0-9_]+\.py", block):
        out.append("a test file name inside the inserted block")
    rows = [int(m.group(1)) for m in re.finditer(r"^\| (\d+)\. ", block, re.M)]
    if rows != list(range(1, 14)):
        out.append("map rows are %s, expected 1..13" % rows)
    if insert is None or norm(block) != norm(insert):
        out.append("INSERT differs from the spec block")
    a2s = arch.find("**AR-2 — ")
    a2e = arch.find("**AR-3 — ")
    if ar2 is None or not (0 <= a2s < a2e) or norm(arch[a2s:a2e]) != norm(ar2):
        out.append("AR-2 differs from the spec block")
    found = len(re.findall(r"^\*\*AR-\d+ — ", arch, re.M))
    if found != 29:
        out.append("AR openers: %d, expected 29" % found)
    for rel in FILES:
        if BRIEF in texts[rel]:
            out.append("%s cites the brief file" % rel)
    return out


def main():
    root = pathlib.Path(sys.argv[1])
    spec = pathlib.Path(sys.argv[2]).read_bytes().decode("utf-8")
    insert = marked(spec, "----- BEGIN INSERT", "----- END INSERT")
    ar2 = marked(spec, "----- BEGIN AR-2", "----- END AR-2")
    texts = {rel: (root / rel).read_bytes().decode("utf-8") for rel in FILES}
    if insert is not None:
        print("insert bytes (UTF-8, as in the spec):", len(insert.strip().encode("utf-8")))
    real = problems(texts, insert, ar2)
    for p in real:
        print("FAIL", p)
    if not real:
        print("ALL KEYS PRESENT")
        print("INSERT EQUAL")
        print("AR-2 EQUAL")
    neg = dict(texts)
    neg[ARCH] = neg[ARCH].replace("**Universality.**", "")
    red = problems(neg, insert, ar2)
    print("NEGATIVE CONTROL:", "red as expected" if any("INSERT" in p for p in red) else "NOT RED (the script is broken)")
    sys.exit(0 if not real and red else 1)


main()
```

Notes for the builder: the script's own marker strings sit inside this fenced section, after §2 and §3.1, and the regex
takes the FIRST line starting with each marker, so it reads the real blocks. A rewrap of architecture.md text is
legal (normalised compare); any word difference is a FAIL (D12).

---

## 8. For the owner's approval (n8)

The Lead shows the owner these two formulations, with Q-ii and Q-iii, and records her answer in the brief («Решено
владельцем») before U4 (§7 GATE).

1. The definition (the Architect's formulation on the owner's words, with the owner's decision of 17.11.2026 "Да, роль
   первой" and the critic's correction of the cost sentence), as it lands in architecture.md:

   > The factory is universal when no difference on the map below requires a change to its code, and on a project of
   > any shape it works no worse than a free agent on the same model. Every difference has exactly one of three
   > answers: a row in a data table, for a closed set of values; a config key or an answer-registry record, asked at
   > onboarding; a role's judgment, for an open set and for everything the factory does not know yet: the role gets
   > what the factory has, asks the person for what is missing, and carries the work to a result.
   > A breach of universality is any place where code, on a value of an axis it does not know, blocks the factory
   > (stops the role, or demands an artifact nobody on a project of that shape can produce), silently takes the branch
   > of a default value, or hands to a person work the role could try first as a free agent would; the person gets only
   > what the role cannot do, such as a physical device or a credential. The extra turns of a role working an unknown
   > shape as a free agent are not a breach when they buy quality; code that makes a stage dearer stays a defect.

   Rendering for the conversation (the English text binds): «Фабрика универсальна, если ни одно различие из карты не
   требует править её код и на проекте любой формы она работает не хуже свободного агента на той же модели. Нарушение —
   код на незнакомом значении блокирует фабрику, молча идёт по умолчанию или отдаёт человеку то, что роль могла бы
   сначала попробовать сама; человеку — только то, чего роль не может (устройство, учётные данные). Лишние ходы роли не
   нарушение, если покупают качество; код, от которого стадия дороже, — дефект».

2. The reading of "silently" (F7 = a, the Lead's decision; AR-1/AR-3/FR-59 reasoning, not yet the owner's word):

   > A default is silent unless it is declared in data and the run says it was taken.

   Rendering: «Умолчание молчаливо, если оно не объявлено в данных или прогон не сказал, что его взял».

---

## Reading trail

| What | Range | Why |
|---|---|---|
| docs/tasks/specs/20261117-universality-variety-map-spec.md (r1) | whole (1-653) | the base text of every section |
| docs/tasks/specs/reviews/t-1212-universality-variety-map-plan.md | whole | findings R1-R13, n1-n8, K1-K8, the owns_readers block |
| docs/tasks/specs/20261117-universality-variety-map-brief.md | whole | the owner's decision item 3 (Q-i), definition, nodes |
| .claude/agents/critic.md | grep 192, 251-266, 281; 58-60 | rule 22 opener, Q10-Q12 text, rule 24 anchor, rule 10 exam |
| docs/SIBLING_MAP.md | 489 (grep), 589-602 | axis 31 `design/*.md` row; axis 34 rows |
| PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md | 1112-1123 | check 42 text (a)-(e), leak sentence; checks 41, 43 neighbours |
| docs/tasks/specs (grep "Deviation: exam not run") | 15 hits | the R6 precedent line and its uses |
| tools/tests/test_role_carriers_one_owner.py | 262-301 + grep | axis 31 parse: File and Owner / pointer cells only; brief-path regex |
| tools/mechanism_gate.py | grep SIBLING_MAP | reads axis headings (MAP_PATH) |
| tools/warn_density.py | 425-439 | protocol block it reads |
| tools/test_handoff_rule_anchors.py | 1-60 | protocol anchors it reads (check 28) |
| tools/dispatch_gate.py | 1384-1399 | protocol anchor class not ported |
| Greps with counts | §4.9 | readers of SIBLING_MAP and the protocol; positive control `architecture` over `.githooks/` |

Needed beyond the manifest: the files above past the three given ones (read for the new edits' anchors and readers).
Not done: the `owns_readers.py` block for SIBLING_MAP.md and the protocol (no shell); the insert size is a hand estimate.

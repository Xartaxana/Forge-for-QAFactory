# Spec (DRAFT, designer t-1207): universality — the variety map, the passage rule, the execution points (phase A, nodes U2 -> U4)

Status: DRAFT for Lead acceptance; then critic on the plan (node U3, mandatory for a new idea, PROJECT.md new-idea step 6).
Input: the intent brief `docs/tasks/specs/20261117-universality-variety-map-brief.md` (the owner's words, decided points,
definition, the 13-axis draft) and the three frozen scout digests t-1200, t-1201, t-1203 (`docs/tasks/specs/reports/`).
Object ids below (a1V, ax7D3, r4, s6.unknownword ...) are the digests' object ids. Note on ids: `r1`-`r12` are the
OBJECT ids of t-1203; the `r*` ids in t-1201 are its trail ids and are never cited here.

Forks are in section 6; none is decided. Where the text of a later section depends on a fork, both texts are given and
the recommended one is marked.

**Lead decisions (Architect session, 17.11.2026) on the technical forks; the draft is accepted for the plan critic.**
F1 = A (AR-2 widened, title unchanged; Option B is not built). F5 = (b). F6 = (a). F7 = (a). F8 = (a). F9 = (a).
F2, F3, F4 are the owner's: put to the owner 17.11.2026, no answer yet; the texts stay as open questions Q-i, Q-ii, Q-iii
until the owner's word. Lead's own question to the plan critic: the map cells carry a per-sub-item inventory with scout
ids (about 1 KB a cell); the map is walked by every package spec and kept true by F8 -- is a short cell with a pointer
to the frozen digest the better form?

---

## 1. AR-n, P-n, FR-n touched and how each is kept

The change is prose only: `ai-packages/qa-factory/design/architecture.md` (package text, not loaded at runtime, FR-44),
two role files, two boot files. No file under `scripts/`, `references/`, `agents/`, `skills/`, `handoffs/` changes.

### 1.1 AR-n

| AR | Touched how | How kept / change check (goes into the DoD, section 7) |
|---|---|---|
| AR-2 | Option A (recommended, fork F1): its Invariant gains the passage clause, its Carriers, Detector, Breakage and Change check gain one sentence each; the title is unchanged | Change check "for each decision moved into code, name what the role still decides": no decision moves into code; the clause moves nothing, it states which way code must yield. "Run the changed script on a fixture shaped unlike the default": no script changes. Detector stays `test_judgment_census.py` + check 41 for the existing invariant; the passage clause gets `none — discipline` with the gap named (section 3). |
| AR-30 (only if fork F1 = B) | a new invariant in section A | Step 10 of "How a change walks this map": entry + summary-table row + regenerated index in the same commit; index at or under 3072 bytes and exactly 30 entries (`python -B tools/architecture_index.py --check`). |
| AR-1 | cited by the map (column "Held by", tag `table:`); no table and no reader changes | Change check "grep scripts/ for the shape of the problem": n/a, no code; the map NAMES the known code tuples (an1, ax7A4, ax11A1) as code-held, it does not move them (node U7). |
| AR-3 | cited by the map (tag `key:`); the passage clause meets "a default for every key" | Kept: the clause says a default declared in data and reported in the run is not silent (fork F7 confirms the reading). No template row, key or interview topic changes. |
| AR-7 | cited by the definition (code yields to the role) | Change check "name what the role still decides": the role decides everything on an unknown shape; no step moves to code. `stage_compare.py`: n/a (no step moved). |
| AR-12 | cited by the definition (cost is not a breach by itself; cost without quality is) | AR-12's text is NOT edited: it counts our code's friction; the extra turns of a role working as a free agent are role work, not friction. `code_friction` before/after: "not measured — no hook, guard, validator or role-called script changes". |
| AR-28 | cited by the passage clause (a silent default is the stage-boundary twin of "an unknown becomes a pass") | No gate read added or changed; nothing to pin. |
| AR-29 | the commit's `judgment:` line | No check unit in `scripts/*.py` is added, altered or moved; census ceilings unchanged (gate world (iv), silent). |
| AR-4, AR-5, AR-6, AR-8..AR-11, AR-13..AR-27 | not touched | Map cells cite carriers of some of them (e.g. AR-5's host adapter under axis 8) without changing them. |

Commit lines: the form is owned by `tools/architecture_gate.py` (its docstring, points 2 and 6); the builder does not
commit (section 7), the Lead writes the lines in that form, e.g. an `architecture:` line naming AR-2 (or AR-30) with how
it is kept, and `judgment: none -- <why>` whose reason is "prose in a design document and in role rules; no check in
scripts/ is added, altered or moved".

### 1.2 Checks this spec adds or alters — owner and census class (AR-29, P27)

| Check | Who performs it | Owner it serves | Census class |
|---|---|---|---|
| The variety walk in the Lead's plan of a new idea | Lead; accepted by the owner (step 4 shows the plan to her) | intent (the person) and judgment | n/a — not code (the census covers `scripts/*.py` only) |
| The variety walk in §1 of a package spec | designer; accepted by the Lead, reviewed by the plan critic | judgment (a role, accepted by a tier above) | n/a — not code |
| Critic question 10, its VARIETY sentence, on a package plan and diff | critic; its verdict accepted by the Lead | judgment | n/a — not code |
| The passage clause (an invariant, not a check) | nobody mechanically; detector `none — discipline` | intent (the owner's words 17.11.2026) | n/a |
| The U4 key-presence witness script (section 7) | builder, not committed | data (presence) | n/a — never committed |

### 1.3 P-n and FR-n

- P1, P2, P22: code yields to the role, which settles an unknown itself and calls for help (passage clause).
- P11: cost is a defect only without a gain in quality (definition); P13: a person's word still passes any gate.
- P27: the owner of every new check is named (1.2). P31: a `narrows` verdict in a walk is a fork, never a non-goal.
- FR walk (PROJECT.md acceptance rule 1), by section:
  - A refusals — FR-5, FR-57 are cited by the definition; no refusal is added or changed.
  - B text to a person — not changed (no text a person reads).
  - C contracts — FR-13 is cited (closed variety = row, open = role); no contract changes.
  - D identity — FR-59 is cited by the passage clause (a declared safe default, never a pass).
  - E delivery — not changed. F measurement — not changed.
  - G code — FR-30: the new package text is English with no Cyrillic character (`selftest.py --lang`); FR-44: the map
    lives in `design/` because only the designer, the critic and the Lead load it, never a role at runtime; FR-54:
    siblings by the map (section 5).

---

## 2. The definition and the variety map (exact text, English)

Placement (owner, 17.11.2026: "таблицу в начале раздела A architecture.md" — "ок"): right after the heading
`## A. Universality across projects` and its blank line, before `**AR-1 — `. POSITIONAL invariant: the inserted block
contains no line starting with `## ` (the index generator `tools/architecture_index.py::scan` stops at the first such
line and would drop every later invariant), no line starting with `**AR-` (it would be counted as an invariant opener),
no bold `**AR-<n>` anywhere (a package test, `test_conductor_investigates_first.py`, finds AR-17 by the first `**AR-17`
in the file), and no `test_<name>.py` file name (selftest's `gate_named_files` reads `design/architecture.md` as prose:
a new name would become gate-named and refuse `test_quarantine.py enter`).

The exact text to insert (between the two marker lines, which are NOT inserted):

----- BEGIN INSERT (architecture.md, after `## A. Universality across projects`) -----

**Universality.** The factory is universal when no difference on the map below requires a change to its code, and on a project of any shape it works no worse than a free agent on the same model. Every difference has exactly one of three answers:

- a row in a data table, for a closed set of values (AR-1);
- a config key or an answer-registry record, asked at onboarding (AR-3);
- a role's judgment, for an open set and for everything the factory does not know yet (AR-2): the role gets what the factory has, asks the person for what is missing, and carries the work to a result.

A breach of universality is any place where code, on a value of an axis it does not know, blocks the factory (stops the role, or demands an artifact nobody on a project of that shape can produce) or silently takes the branch of a default value (P1, FR-5, FR-57). Cost alone is not a breach: a stage may cost somewhat more and take longer when that buys quality (the owner, 17.11.2026); the defect is cost with no gain in quality (P11, AR-12). How code must yield is AR-2's passage clause.

**The variety map.** One row per axis on which projects differ. "Held by today" lists each sub-item under its holder: `table:` (AR-1), `key:` (a config key or registry row with its onboarding topic, AR-3), `role:` (AR-2), `code:` (hard-coded; the outcome on an unknown value is (i) refuses or halts, (ii) silent default, (iii) reports and leaves a move), `not addressed:` (with what a role does there today). "Proven on" says live project, fixture, or not proven. The ids in brackets are objects of the scout digests of 17.11.2026: `a*` and `an1`, `an2` in `dev:docs/tasks/specs/reports/20261117-universality-scout-t-1200-axes-1-6.md`; `ax*` in `dev:docs/tasks/specs/reports/20261117-universality-scout-t-1201-axes-7-13.md`; `r1`-`r12`, `s*`, `ob.*`, `an.*`, `dsg.*` in `dev:docs/tasks/specs/reports/20261117-universality-scout-t-1203-mobile-stage-walk.md`. Their reading bounds hold here: the `code:` lists are the strongest places reached, not a census of `scripts/`; S1, S2 and S7-S9 were read through `references/stages.json` only; within what was read, no place blocks with no door at all.

| Axis | Examples | Held by today | Proven on |
|---|---|---|---|
| 1. Product language and build | Python, .NET, Java, Go, JS/TS, Kotlin/Swift; pip, maven, gradle, npm, nuget; monorepo, subfolder, several repositories | table: manifests of eight languages (a1A1); 20 code extensions (a1A3); lock kinds and install commands for poetry, uv, pdm only (a1A2); the build-identity ladder (a1A4). key: `app_root`, `code_repos`, `implementation_repos`, profile runtime and package manager, the install command; topics 1, 2b, 5 (a1B1, a1B2). role: onboarding phase 1 reads the stack; the automator writes the project's way (a1C1). code: Python environment selection, any other stack is `inherited` (a1D1, iii); Poetry-only lock drift, others `unknown` (a1D2, iii); a six-file Python/JS floor beside the table (a1D3, an2, iii); pytest ini names (a1D4, iii). Verdict: mixed (a1V). | fixture: Java, C# and TypeScript probe files, a subfolder project, a sample pytest repository (a1E1). live: pytest-playwright projects; the stack of the other runs is not stated (a1E2). .NET, Java, Go, Kotlin, Swift on a live project: not proven. |
| 2. What is tested | web UI, mobile app, API (REST, GraphQL, gRPC), database and data pipelines, queues, desktop, CLI, combinations | table: surfaces web, api, cli, desktop, android, ios (a2A1); not-surfaces and the unknown-word text (a2A2). key: profile capabilities, `environments[]` surface, driver, device, app (a2B1); the phase 1 mobile row and the topic 2 mobile batch (a2B2), reached only when Appium is named (r1, ob.detect, ii). role: the automator takes the lowest rung that observes the behaviour (a2C1). code: agent hands are browser, http and driver, any other row's cases go to a person (a2D1, a2C2, an1, iii); an unknown capability word, or a native profile with no stand, gives hands `person` (a2D2, s6.unknownword, iii), open owner question Q-i; the sign-in probe defaults to Playwright (a2D3, iii); no UI address is derived for a non-browser profile, silently (a2D4, ii); an undeclared surface follows the web road (r2, s6.web, ii); an all-manual story reaches a refusal to the conductor at S5 whose closure is not traced (r11, s5.scope, dsg.empty). not addressed: database, queue, GraphQL and gRPC as surfaces (a2A3; pattern advice only, a2A4); a role today: such a case gets hands `person` (a2D2). Verdict: mixed (a2V). | live: web and API only (a2E2). fixture: the mobile-road tests, known by name only (a2E1). device: no row has run on a device; iOS is general knowledge (a2E1, ax7E2). Database, queue, CLI, desktop: not proven. |
| 3. The project's test stack | pytest, JUnit, NUnit, Playwright, Appium; BDD or code; tests in the product repository or apart; a test language unlike the product's; own case ids and fixtures | table: about 24 runner collect forms (a3A1); assertion probes for C#, Java, TypeScript, Python (a3A2), none for `.kt` or `.swift` though the path markers list them (s5.rows, an.kt); path markers, a hint only (a3A3); the default case form `TC-{nnn}` (a3A4); the case marker `@pytest.mark.` only (an.marker). key: `tests_root`, `test_locations`, `cases_root`, `case_id_form`, command templates, profile selectors and reporter (a3B1, a3B2). role: the framework is confirmed by reading a test file (a3C1); the automator and the code critic follow the project's framework (a3C2); the case designer writes Given-When-Then with no framework binding (a3C3). code: a non-Python file with no detector row is a note with a door for the role (a3D1, r6, iii); probe by code on an unlisted suffix refuses and names doors (a3D2, r5, i with a door); pytest wording and an all-or-nothing collect (a3D3, iii); the pytest rootdir walk (a3D4, iii); the toolchain rehearsal runs only for a pytest-shaped command (s4.tool, s4.pytest, ii); the reporter rehearsal globs omit Kotlin, Swift and Java names (s4.rep, an.globs); reporter `none` records a run `not_executed` however green its log, and S6 trips (r4, s5.report, ob.report, ii); a missing executor puts three answers to the person (r8, s4.exec, s5.exec, iii). not addressed: BDD runners such as Gherkin, Cucumber, SpecFlow, Reqnroll (a3A5); a role today: the case designer writes Given-When-Then and the automator the project's way (a3C3, a3C2). Verdict: mixed (a3V). | fixture: a sample pytest repository; Java, C# and TypeScript probes; Playwright TypeScript; a jest JUnit report (a3E1). live: a project's own case id form on TP1-13877; pytest-playwright on TP1-15045 (a3E2). JUnit, NUnit, Appium on a live project: not proven. |
| 4. Starting state (flow) | code present or not; autotests present or not; requirements good, only AC, or one line; a reference system or none; the change merged, in an MR, or not written | table: side realities real, absent, substituted; an MR or PR is a change (a4A1). key: `code_repos`, `implementation_repos`, `app_root`; registry rows `product.sides`, `environments.sides`, `environments.reference_for` (a4B1); onboarding takes no checkout, no case library and no tests as answers (a4B2). role: the S0 no-change question with four doors (a4C1); the scout grounds a side not built yet on the requirements (a4C2); the requirements tester records what is not checkable as an open question (a4C3); the first look records a null for no stand, no code yet, an empty register (s3.look). code: the no-change entry is asked only for a local story (a4D1, iii); "current code" is offered only with `code_repos` (a4D2, iii); `app_root` "." proves nothing (a4D3, iii); missing S0 capabilities get the person's "go on" (r9, s0.door, iii). Requirements quality: role only; no classifier in code was found, absence not proven (a4C3). Verdict: mixed (a4V). | live: MR-grounded runs, TP2-2553 and pilot 13958 (a4E2). fixture: a local story, an implementation diff (a4E1). A reference system: no fixture found by name, the miss not proven (a4E1). A local-only story on a live project: not named. |
| 5. Where requirements come from | Jira, YouTrack, Azure DevOps, GitHub Issues, no tracker; Confluence, Notion, Figma, knowledge in people's heads; ticket types | table: tracker kinds jira, file, github, gitlab, ado, local, with fallback jira (a5A1); source kinds, an unknown kind routed to a role (a5A2); link kinds (a5A3); a Jira-only field table (a5A4). key: `adapters.ticket`, `requirements_sources`, `strategy_documents`; topics 7 and 10 (a5B1, a5B2). role: the scout finds and judges every source by content (a5C1); an unlisted tracker is read by the role on its recorded route (a5C2). code: an unknown command adapter is refused (a5D1, an1, i); source refresh needs Jira (a5D2, i); an unknown tracker kind takes the Jira key form, marked a guess (a5D3, iii); the direct client is Jira-only, others take the role route (a5D4, iii); a built-in adapter set twins the table (a5D5, iii). Verdict: mixed (a5V). | live: Jira only (a5E2). fixture: file-adapter tickets (a5E1). YouTrack, Azure DevOps, GitHub Issues, Notion: not proven. |
| 6. Where the result is delivered | GitLab, GitHub, Bitbucket; an MR into the product, into a test repository, or no code; TestRail, Allure TestOps, Xray or nothing; where bugs are filed | table: VCS kinds gitlab and github with their delivery commands (a6A1); GitLab auth wording (a6A2). key: `external_writes` channels for bugs and cases, `adapters.vcs`, `git_conventions`; topics 5, 7 and 8, markdown first-class (a6B1, a6B2). role: S8/S9 runs branch, commits, push and the MR from data (a6C1); the VCS is reached by the route onboarding named, every route before a person (a6C2); an unknown channel passes on the person's word (a6C3). code: case channels xray, testrail, zephyr, anything else `NO_ADAPTER` (a6D1, an1, i); MR evidence collection is GitLab-only (a6D2, iii; a6D3); an unlisted tracker CLI passes the guard (a6D4, ii); the delivery prompt assumes a Draft merge request, and no code-free branch was seen in the range read (a6D5). Verdict: mixed (a6V). | live: GitLab MR runs with Jira (a6E2). GitHub, Bitbucket, Azure DevOps, TestRail, Xray: not proven (a6E1). |
| 7. Stand and access | local docker, a shared stand, a preview per MR, behind a VPN; SSO and 2FA; test data; how to know the build on the stand; devices and emulators | table: the build-identity ladder, container-shaped (ax7A1, s5.ident); surfaces (ax7A2); one sign-in form, NextAuth credentials (ax7A3). key: `environment.access`, `environments[]`, integrations, `test_data` (ax7B1); topics 2 and 3 (ax7B2); the stand interview asks for an HTTP address, unanswered is a deferred marker (ob.url, ob.keys). role: who owns an environment issue, telling the stand from the product (ax7C1); the dropped-VPN cause (ax7C2). code: seven access kinds in a code tuple (ax7A4); an unknown access kind is refused by the config contract (ax7D3, i); the docker build read ends `unknown` with a question (ax7D1, iii); the `/app` checkout default (ax7D2, ii); a silent remote stand gets the VPN text (ax7D5, iii); an environment row with no URL passes S0 as in-process (r3, s0.inproc, ii); a device row is probed read-only (s0.device); the device-build question (s5.devbuild); the first typed run with no runtime probe is refused with a door for the role (r7, s5.probe, s5.nockout); the S4 runtime-probe repair may loop on a project with no container, not proven (r12, s4.fix); an unconfirmed stand passes on the person's word (r10, s6.stand, iii). not addressed: SSO providers and 2FA beyond one NextAuth row, per-MR preview stands (ax7D7, ax7V); what a role does there today: not read. Verdict: mixed (ax7V). | live: a Keycloak stand (ax7E3). fixture: stand records of an old-generation project, run configurations (ax7E1). device: no fixture named for a device (ax7E4); no row has run on a device (ax7E2). |
| 8. Machine and host | Windows, Mac, Linux; Claude Code or Codex; subscription or gateway; prompt-cache settings (P25); no internet | table: host report forms for claude and codex (ax8A1); driver infra per host (ax8A2); machine path markers and install path classes (ax8A3); model rates (ax8A4). key: `driver.host`, `driver.child_env.keep` (the gateway door) and others (ax8B1); onboarding asks nothing about OS, shell, host or gateway (ax8B2). role: a Codex host reference exists, not read (ax8C1). code: the host must be claude or codex (ax8D1, i); a default model literal for a non-Codex host (ax8D2, ii); guards act only on Bash and PowerShell (ax8D3, ii); a Windows `.cmd` argv refusal with a door (ax8D4, i with a door); the child loses proxy variables, `keep` is the way back (ax8D5, iii). not addressed: no internet, the prompt-cache TTL (ax8B3, ax8V); what a role does there today: not read. Verdict: mixed (ax8V). | live: macOS PATH, Windows backslash and POSIX shell defects found by users; a Codex desktop run (ax8E1). Per-OS fixture: not determined (ax8E2). |
| 9. People and process | who answers questions and how fast; manual testers; who reviews tests; regression policy; what "done" means | table: approval words (ax9A1); question thresholds, person-owned classes, manual policy by level (ax9A2). key: `dod`, manual walkers, accounts and data way, `external_writes`, `git_conventions`, `pipeline.stop_after`, budget, `impact_scale` (ax9B1); topics 4, 5, 8, 9 (ax9B2). role: regression is found, not run (ax9C1); who reviews a row follows its impact class (ax9C2, partial). code: a gate passes when the first line is a table word, otherwise the answer goes to the conductor (ax9D1, iii); the main-branch fallback `origin/main` or `origin/master` (ax9D2, iii). not addressed: who answers and how fast (ax9D3); what a role does there today: not read. Verdict: mixed (ax9V). | fixture: recorded answers of a bench run and of gate A (ax9E1). live: regression policy and question counts of recorded runs (ax9E1). |
| 10. Language of communication and artifacts | tickets and answers in Russian or English; the language of cases and bugs | table: three English acceptance headings (ax10A1); English approval words (ax10A2). key: a project may add acceptance headings in its own language (ax10B1); the words file keeps the person's language (ax10B3, partial). role: every artifact is written in English whatever the ticket's language (ax10C1, ax10D1, ii by design), open owner question Q-ii. code: English bug-form headings, refused when missing (ax10D2, i); a non-English approval word goes to the conductor (ax10D3, iii); a mostly non-ASCII phrase gets a hash slug (ax10D4, iii). not addressed: a language or locale key (ax10B2); what a role does there today: writes English (ax10C1). Verdict: mixed (ax10V). | not proven: no fixture holds a non-English ticket or answer, the package being English by FR-30 (ax10E1). |
| 11. Size and shape of the task | a bugfix or an epic over several services; a task over several repositories; e2e in minutes or in hours | table: none; the XS-XL cap table is a code constant (ax11A1). key: sizing weights, window sizes, `parallel_windows`, S5 window cases, budget, stand wait, repositories (ax11B1); topics 1 and 5 (ax11B2). role: an XXL story is put to the person: test it as one story, or name what to leave out (ax11C1). code: above XL is labelled XXL, advice only (ax11D1, iii); several implementation repositories get a refusal with the door `--checkout` (ax11D2, i with a door); the run timeout is reported as the factory's own limit (ax11D3, iii); the install timeout sits below an assumed host cap (ax11D4, ii); a branch word naming no repository leaves the sha null, never a refusal (ax11D5, iii). Verdict: mixed (ax11V). | fixture: sizing goldens, a two-repository comparison (ax11E1). live: TP1-15045 with an S5 of 12.5 hours (ax11E2). |
| 12. Kinds of checks and constraints | functional, load, security, accessibility; external integrations; personal data, a regulated domain | table: side realities (ax12A1). key: integrations, `pii_and_masking`, shared records, registry sides (ax12B1); topic 3 asks the PII rule (ax12B2). role: the masking rule applies to everything a role writes (ax12C1). code: S0 prints that v0 covers functional testing only, with no question (ax12D1), open owner question Q-iii; onboarding never asks about performance, security or accessibility (ax12D2); a plan level with no evidence rule stays as planned and the gate line names it (ax12D3, iii); CLI and desktop agent checks go to a person (ax12D4, iii). not addressed: load, security, accessibility (declared out of scope, ax12V); regulated domains (ax12D5); what a role does there today: the PII rule only (ax12C1). Verdict: not addressed for non-functional checks and regulated domains (ax12V). | not determined: no fixture found by name for these shapes (ax12E1). |
| 13. The project's age in the factory | the first onboarding or the hundredth story; a project from an old factory version; several stories in parallel | table: install path classes (ax13A1); config migration rows (ax13A2). key: `schema_version`; re-onboarding asks only what is not on record (ax13B1). role: rediscovery re-reads only the sources unreachable before (ax13C1). code: parallel stories pick the newest running pipeline, two copies of the guess (ax13D1, ax13D2, ii); another `schema_version` makes a capability missing, halting not traced (ax13D3, iii); two running dispatches of a role are never placed by a guess (ax13D4, iii); one run per stand, a second waits on a lease (ax13D5, ii). Verdict: mixed (ax13V). | fixture: an old-generation project, config migration, reinstall (ax13E1); parallel story tests, known by name (ax13E2). |

**Open owner questions** (17.11.2026, not decided; the record is `dev:docs/tasks/specs/20261117-universality-variety-map-spec.md`, section 6):

- Q-i: cases on a surface the table does not know go to a person today (a2D1, s6.unknownword). Should the role try them first, as a free agent would, and hand to the person only what it cannot do?
- Q-ii: roles write every artifact in English whatever the ticket's language (ax10C1). Is the artifact language a project fact?
- Q-iii: "v0 covers functional testing only" (ax12D1). Is that a declared scope, or a place where the passage clause applies?

**How the map is walked.** Three places walk it, axis by axis: the Lead's plan of a new idea (`dev:PROJECT.md`, new-idea step 4), §1 of a package spec (`dev:.claude/agents/designer.md` rule 1), and the critic of a package plan or diff (`dev:.claude/agents/critic.md` rule 22 question 10 and rule 24). One line per axis, in one of three forms:

- `axis N: held by table|key|role -- <carrier>; unknown value -> <what the code does>`
- `axis N: n/a -- <why the change does not meet this axis>`
- `axis N: narrows -- <which projects lose what>`; a `narrows` line is a fork for the Lead and the owner (one road, P31), never a non-goal.

A change that meets no axis writes the one line `variety: none -- <reason>` instead of thirteen. A builder dispatch carries no walk: it points at its spec's §1. A change that alters how an axis is held (a new table row, key or role step, a code site removed) edits that axis's cell in the same commit and names its carrier; the scout ids stay the evidence of 17.11.2026.

----- END INSERT -----

Edge (1) check of the text above: every cell is non-empty; every `not addressed:` names what a role does there today or
says "not read" (axes 7, 8, 9, where the digests did not read it). Edge (2): the three owner questions stand as
questions, in the cells (axes 2, 10, 12) and in the list; no cell states an answer.

---

## 3. The passage rule: exact text, place, detector

Place: fork F1 (edge 6). Option A (recommended) widens AR-2 with the title unchanged (index and boot bytes unchanged,
one free slot kept: 29 of 30). Option B adds AR-30 (fills the last slot: the next invariant must merge, step 10).

### 3.1 Option A (recommended) — the new AR-2 block (replaces the current five bullet lines of AR-2; the opener line stays byte-identical)

```
**AR-2 — Open variety is a role's judgment; code reports and leaves a move.**
- Invariant: some variety no table can close: layouts, id spellings, sources, frameworks, a person's or role's wording. The owning role or the conductor judges it. Code triggers on a field, a state or the presence of words, reports what it found, and never decides meaning. Passage: on a project shape the factory does not know (a value of a variety axis that no table row, key or role step names), code never blocks and never takes a default branch silently; it says what it could not establish and leaves the move to the owning role. The role proceeds as a free agent on the same model would, with what the factory already has (onboarding answers, testing knowledge, the critic), asks the person for what it cannot find, and carries the stage to a result. A stage may cost somewhat more or take longer when that buys quality; it does not block (the owner, 17.11.2026). A default is silent unless it is declared in data and the run says it was taken (FR-59, AR-28). A safety refusal stays a refusal (AR-29), and a person's word still passes any gate (P13). Whether a door that hands the work to a person instead of the role counts as passage is open owner question Q-i of the variety map.
- Carriers: FR-12, FR-13, FR-47, FR-57, FR-59, P1, P2, P22, P31; `handoffs/README.md` "When the judge is on" (a judged value never lifts a block); the variety map at the head of this section.
- Detector: the census (AR-29): test_judgment_census.py; calibration check 41. Gap: FR-47's check ("run the script on a project shaped differently") has no gate, and nothing scans for phrase lists (FR-12). Passage: none — discipline; no gate finds a block or a silent default on an unknown shape. The planned detectors are the live comparison with a free agent on the same model (node U6 of the universality idea, `dev:docs/tasks/specs/20261117-universality-variety-map-spec.md`) and the scoreboard's free-agent bar, which has no writer yet (AR-12).
- Breakage: FR-13's record. On TP1-13877 the contract knew only `TC-\d+` while the project wrote `TP1-13877_TC_001`. The automator spent about 35 calls reading factory code, then halted. Passage: none recorded in a live run; the reconnaissance of 17.11.2026 lists the candidate places per axis in the map (r1-r12).
- Change check: for each decision moved into code, name what the role still decides. Add no regex over prose meaning. Run the changed script on one fixture shaped unlike the default; it must report, not halt. A change that reads the value of a variety axis says what it does on a value it does not know (report and leave the move; never block, never a silent default) and gives the variety walk of this section.
```

Note for the builder: `test_judgment_census.py` already stands in the current AR-2 Detector line (unchanged words; no
new test name is introduced). The fence above is the spec's quoting only; the text goes into the file without it.

### 3.2 Option B — AR-30 (only if the Lead/owner choose it)

AR-2 stays byte-identical. After AR-6's last line and its blank line (before `## B. Low friction with our code`)
insert:

```
**AR-30 — On a project shape the factory does not know, code never blocks and never defaults silently.**
- Invariant: <the "Passage:" sentences of 3.1, from "on a project shape" to "variety map.", with "Passage: " dropped>
- Carriers: FR-5, FR-57, FR-59, P1, P2, P22, P31; AR-2, AR-28; the variety map at the head of this section.
- Detector: none — discipline; <the "Passage:" Detector sentences of 3.1>.
- Breakage: none recorded in a live run; the reconnaissance of 17.11.2026 lists the candidate places per axis in the map (r1-r12).
- Change check: <the last sentence of the 3.1 Change check>.
```

and in the summary table row `| A. Universality across projects | AR-1, AR-2, AR-3, AR-4, AR-5, AR-6 |` append
`, AR-30`; regenerate the index with `python -B tools/architecture_index.py`. Index line added, estimated: 105 bytes
(estimate, not verified; the builder measures). Current index size, estimated by hand from its text: about 2,680 bytes
of 3,072 (estimate, not verified). With B, every reference to "AR-2's passage clause" in sections 2 and 4 reads "AR-30".

### 3.3 Detector, honestly

`none — discipline`, with the gap named in the Detector field itself (above). Leak detectors that exist: the plan critic
(mandatory for a new idea) and critic question 10 on every package diff it reviews. A diff waived from the critic
(`critic: skipped`) escapes; promotion to a code layer follows evidence of a leak (CLAUDE.md rule 10 (d)); fork F6.

---

## 4. Exact edits per file (path::anchor, old -> new), byte deltas for boot files

All five files land in ONE commit (edge 3, temporal: the role and policy texts point at a map that does not exist until
that commit; a split would leave a rule pointing at nothing).

### 4.1 `ai-packages/qa-factory/design/architecture.md`

E1 — `architecture.md::intro paragraph (line 3)` — a stale pointer met in the node's reach (fixed here, designer rule 2):
- old: ``the owner's principles in `dev:PROJECT.md` (P1-P23)``
- new: ``the owner's principles in `dev:docs/OWNER_PRINCIPLES.md` (P1-P31)``
(carrier read: PROJECT.md "Принципы владельца" says the full text P1–P31 is `docs/OWNER_PRINCIPLES.md`.)

E2 — `architecture.md::**Who reads it.**`:
- old: `the designer drafting a package spec, and the critic on a package diff.`
- new: `the designer drafting a package spec, the Lead writing the plan of a new idea (the variety walk of section A), and the critic on a package plan or diff.`

E3 — `architecture.md::## A. Universality across projects` — insert the block of section 2 after the heading's blank
line, followed by one blank line before `**AR-1 — `.

E4 — `architecture.md::**AR-2 — ` — Option A: replace the five bullet lines with those of 3.1. Option B: no change to
AR-2; insert 3.2 and edit the summary table.

E5 — `architecture.md::## How a change walks this map` step 2:
- old: `A change that touches none says so in one line, with the reason. An invariant the change cannot keep is stated, never reworded.`
- new: `A change that touches none says so in one line, with the reason. The variety walk of section A goes to the same places, in the form given there. An invariant the change cannot keep is stated, never reworded.`

E6 — same section, step 9:
- old: `The critic asks four questions. Which AR-n is touched but not named? Is each change check done? Was the producer-reader walk controlled? Is every raise named?`
- new: `The critic asks five questions. Which AR-n is touched but not named? Is each change check done? Was the producer-reader walk controlled? Is every raise named? On a project of what shape does the change break, and does the factory there still pass no worse than a free agent (section A)?`

Sweep of the enclosing block "How a change walks this map" (rule 9, artifact first): step 1 n/a (grep by changed file,
unaffected); step 2 applied (E5); step 3 n/a (the map-cell update duty is stated in the walk text of section 2, not a
producer-reader edit); step 4 n/a (the SIBLING_MAP walk is unchanged); steps 5-7 n/a (FR walk, friction, ratchets
untouched by variety); step 8 n/a (it already covers a `none — discipline` detector, which the passage clause is);
step 9 applied (E6); step 10: n/a for Option A, applies for Option B (entry + regenerated index). Sweep of section A's
invariants: AR-1 n/a (its change check already routes a value the table lacks to AR-2); AR-2 applied (E4); AR-3 n/a
(its "default for every key" is reconciled inside the passage clause: declared and reported is not silent); AR-4, AR-5,
AR-6 n/a (paths, host reader, read routes: no variety rule changes them).

Not boot: architecture.md is loaded by nobody at boot or runtime. Option A leaves every AR title unchanged, so
`docs/ARCHITECTURE_INDEX.md` stays byte-identical (0 boot bytes).

### 4.2 `.claude/agents/designer.md` (not boot)

`designer.md::rule 1, last sentence` — after `` `judgment: none` always carries its ` -- <why>`, and a spec never prescribes it bare.`` append:
- new: ` The same §1 carries the variety walk of `design/architecture.md` § A, one line per axis in the form that section owns, or its one line `variety: none -- <reason>`; a `narrows` line is also a fork (rule 6).`

The rule's anchored first line (`tools/install_parity_anchors.json`) is untouched.

### 4.3 `.claude/agents/critic.md` (not boot)

`critic.md::rule 22, Q10` — at the end of the Q10 line, after `(blocks when a reader is starved).` append:
- new: ` VARIETY (§ A of the same file: its variety map and AR-2's passage clause): on a project of what shape does the diff break, and does the factory there still pass the stage no worse than a free agent on the same model, with no block and no silent default on a value it does not know? A package spec whose §1 lacks the variety walk, or a diff that blocks or defaults silently on an unknown value, is a finding (blocks when it stops a stage); a spec accepted before the map landed owes no walk, and the critic answers the question itself.`
(Option B: "AR-2's passage clause" -> "AR-30".)

`critic.md::rule 24`:
- old: `answer Q13 below and Q4, Q6 and Q12 of` / `rule 22 (read "the diff" as "the plan")`
- new: `answer Q13 below and Q4, Q6, Q12 and Q10's VARIETY sentence of` / `rule 22 (read "the diff" as "the plan")`

### 4.4 `PROJECT.md` (boot)

`PROJECT.md::Как разрабатывается новая идея владельца, step 4` (lines 130-131):
- old: `что меняется, фазы, какие AR/P затронуты и` / `с какими идеями и пачками в работе это пересекается (...)`
- new: `что меняется, фазы, какие AR/P затронуты, вердикт по каждой оси карты различий (`architecture.md` § A) и` / `с какими идеями и пачками в работе это пересекается (...)` (the builder rewraps at the file's width).

Added: `, вердикт по каждой оси карты различий (`architecture.md` § A)` = 94 bytes (UTF-8; Cyrillic letters 2 bytes
each, `§` 2 bytes) plus about 4 for one more wrapped line: about +98 bytes (count by hand; the builder measures).

### 4.5 `CLAUDE.md` (boot) — fork F5; recommended (b)

`CLAUDE.md::Rule 10 · a change to the package` (lines 273-275).

(b) recommended — only the "change together" sentence:
- old: `This` / `paragraph, critic question 11 and designer rule 1 change together (axis 1).`
- new: `This` / `paragraph, critic questions 10-11, designer rule 1 and new-idea step 4 change together (axis 1).`
Added: 21 bytes (+ at most 4 for a rewrap). Reason: by axis 31 the designer's duty is owned by its role file and the
Lead's by PROJECT.md step 4; this paragraph only has to name its co-changers.

(a) alternative — also name the walk in the designer clause:
- old: `the designer` / `names the AR-n, and for every check the owner it serves`
- new: `the designer` / `names the AR-n, a verdict per axis of the variety map (architecture.md § A), and for every check the owner it serves`
plus the sentence of (b). Added: about 63 + 21 + 4 = about 88 bytes.

### 4.6 Boot byte budget

Lead's measure at brief time: 112,646 of 120,000 bytes (WARN zone already; not re-measured by the designer).

| File | Option A + CLAUDE (b) | Option A + CLAUDE (a) | Option B + CLAUDE (b) |
|---|---|---|---|
| PROJECT.md | about +98 | about +98 | about +98 |
| CLAUDE.md | about +25 | about +88 | about +25 |
| docs/ARCHITECTURE_INDEX.md (imported) | 0 | 0 | about +105 |
| Total | about +123 (to about 112,769) | about +186 | about +228 |

All hand counts, "estimate, not verified"; the builder reports exact before/after sizes. No offset is proposed inside
this change: the added lines are the execution points the owner asked for; an offset candidate is fork F5.

### 4.7 Generated copies

`AGENTS.md` is regenerated in the same commit (`python -B tools/agents_md.py`; pre-commit enforces, SIBLING_MAP axis 4)
because CLAUDE.md, PROJECT.md and two agent files change.

### 4.8 Readers of every touched file (designer rule 7)

The `tools/owns_readers.py` block was NOT attached to the brief. Below is the hand grep; the plan critic re-runs
`python -B tools/owns_readers.py --paths <the five files> --names "AR-2,variety"` (critic rule 24 Q13 (d)).

Commands and counts (Grep tool, case-sensitive, each a positive control of itself where it hit):
`architecture\.md` over `tools/`: 7 files; over `.githooks/`: 1; over `ai-packages/qa-factory/scripts/`: 5 files.
`critic\.md|designer\.md|CRITIC|DESIGNER` over `tools/*.{py,json}`: 20 files. `change together|Короткий
верхнеуровневый|AR/P затронуты|standing questions` over `tools/`: 0 (control: the same pattern on CLAUDE.md 2, PROJECT.md 1);
`critic question 11|designer rule 1 change|questions 10 and 11` over `tools/` and `PROCESS/`: 0 (control: CLAUDE.md 2).

| Touched file | Reader | Verdict |
|---|---|---|
| architecture.md | `tools/architecture_index.py` (`scan`, `verify`, `render`) | unchanged; edges E1-E2 of section 7 keep its parse (no `## ` line, no `**AR-` line in the insert). Option B changes the index (regenerated in the stream). |
| architecture.md | `tools/architecture_gate.py` | unchanged; reads only the index. |
| architecture.md | `tools/test_architecture_index.py`, `tools/test_architecture_gate.py` | unchanged; `--check` on the real file runs in the witness. |
| architecture.md | `.githooks/pre-commit` (runs the index `--check`) | unchanged. |
| architecture.md | `tools/tests/test_role_carriers_one_owner.py` (a main document: names no deleted file, no `docs/tasks/<x>brief<y>.md`) | unchanged; edge E5: the insert cites the scout reports and this spec, never the brief. In the witness. |
| architecture.md | `tools/test_quarantine.py` (`forge_texts`, `gate_named_files`) and `scripts/selftest.py` `_PROSE_CARRIERS` | unchanged; edge E3: no new `test_*.py` name in the insert. |
| architecture.md | `tools/source-split-carriers.json` row 10 ("line anchors in prose") | unchanged; line anchors shift, the row is a note. |
| architecture.md | `scripts/tests/test-layers.json` `named_by` entries `design/architecture.md:<line>` | unchanged; the insert shifts these lines by about 30, and `selftest.py` (line 629) checks only that `named_by` is non-empty, never the line. Stale-as-text, not red; out of owns (the file is a ratchet-adjacent carrier). |
| architecture.md | `scripts/tests/test_conductor_investigates_first.py` (`block_from(arch_text, "**AR-17")`) | unchanged; AR-17 not edited; edge E2 (no other `**AR-17`). |
| architecture.md | `scripts/tests/test_sizing_impact_scale.py` (the AR-22 `- Breakage: commit 28fc7170` line once) | unchanged; AR-22 not edited. |
| architecture.md | `scripts/tests/test_selftest_slow_tests.py` (names the file in a fixture tuple) | unchanged; not opened beyond the grep line. |
| designer.md, critic.md | `tools/install_parity_anchors.json` + `tools/install_parity.py --check` | unchanged; edits append to rule 1 / Q10 / rule 24, no anchored line start changes. In the witness. |
| designer.md, critic.md | `tools/test_handoff_rule_anchors.py` | unchanged; hand-back keys and critic rule 23 untouched. In the witness. |
| designer.md, critic.md | `tools/tests/test_role_carriers_one_owner.py` | unchanged; no deleted file named. |
| designer.md, critic.md | `tools/dispatch_gate.py`, `dispatch_manifest.py`, `dispatch_new.py`, `journal_echo.py`, `forge_metrics.py`, `session_context.py`, `owns_readers.py`, `r3_integration_check.py`, `critic_verdict.schema.json` and their tests (grep hits on the role NAMES) | unchanged by assumption: they read role names or handoff paths, not rule text; not opened. The plan critic's owns_readers run confirms or lists. |
| designer.md, critic.md, CLAUDE.md, PROJECT.md | `tools/agents_md.py` (AGENTS.md) | changes in this stream: regenerated, same commit. |
| CLAUDE.md, PROJECT.md | `tools/session_context.py` (`boot_budget_lines`: file sizes + CLAUDE.md imports) | the BOOT BUDGET line grows by section 4.6's delta; no code change. |
| CLAUDE.md, PROJECT.md | `tools/tests/test_role_carriers_one_owner.py` (TOC_POINTERS; main documents) | unchanged; no heading or Contents cell changes. |
| docs/ARCHITECTURE_INDEX.md (Option B only) | `tools/architecture_gate.py` (ids), CLAUDE.md import, session_context | changes in this stream: AR-30 becomes a legal id; boot +105. |

---

## 5. The four questions of CLAUDE.md rule 10

Mechanism: "the variety map and its walk" (a duty for the Lead's plan, the designer's §1 and the critic), plus the
passage clause (an invariant of the package's design). One block covers both; lines name which when they differ.

(a) Cost and who pays. The Lead: up to 13 lines in each new-idea plan. The designer: up to 13 lines in §1 of each
package spec, or one `variety: none` line. The critic: one more question on each package plan and diff. Every session:
about +123 boot bytes (4.6, recommended options). Every package change that alters how an axis is held: one map cell
edit. The builder: nothing (a dispatch points at §1).

(b) SIBLING_MAP axes, by enumeration:
- axis 1 (Policy <-> role files <-> journal): covered — CLAUDE.md rule 10 paragraph, designer.md rule 1, critic.md
  Q10 and rule 24, PROJECT.md step 4 change in one commit; AGENTS.md regenerated.
- axis 2 (per-tier exam instruments): n/a — no exam discipline changes.
- axis 3 (package <-> release copy <-> installed plugin): covered — architecture.md ships with the package and
  travels with the next release; no runtime reader (FR-44); nothing edited in a release copy or cache.
- axis 4 (rules <-> debt <-> backlog <-> principles): covered for the index (Option A: no title change; B:
  regenerated) and AGENTS.md; no FR or principle added. Debt rows for the breaches the map names: queued as fork F9.
- axis 5 (stage twins): n/a — no stage logic changes; the map's r-ids across S0-S9 are U7's input.
- axis 6 (measurement tools <-> package): n/a — no measurer changes; the free-agent bar's missing writer is named as
  the passage clause's planned detector (AR-12's existing gap).
- axis 7 (per-test identity): n/a — no test identity touched.
- axis 8 (story on disk): n/a — no resolver touched.
- axis 9 ("is this a test file"): n/a — no code touched.
- axis 10 (git-top readers): n/a — no code touched.
- axis 11 (shell-command recognizers): n/a — no code touched.
- axis 12 (carriers of the work plan): covered — the idea's DAG stays in its brief file (rule 4a); this spec is the
  record of U2; node statuses are moved by the Lead with the journal events.
- axis 13 (the dispatch text): covered — a builder dispatch carries no walk and points at the spec's §1, keeping the
  brief-size target of CLAUDE.md rule 11 (edge 5).
- axis 14 (agent transcripts): n/a — not read or written.
- axis 15 (console stream setup): n/a — no code.
- axis 16 (one JSON reader): n/a — no code.
- axis 17 (detector verdict shape): n/a — no detector added.
- axis 18 (in-tree shrink-only ratchets): n/a — no ratchet row; the index's 30-entry cap is a cap, not a ratchet
  (Option B fills it to 30 of 30, named in F1).
- axis 19 (`tools:` line reader): n/a — no role file's `tools:` line changes.
- axis 20 (host receipt names): n/a — no code.
- axis 21 (markdown table readers): covered — the map is a markdown table inside section A, where
  `architecture_index.py` reads no table (it reads only the summary table before the first section); no package
  runtime reader reads `design/`.
- axis 22 (host return form): n/a — no code.
- axis 23 (fields of a `tests[]` row): n/a.
- axis 24 (the record of an execution): n/a.
- axis 25 (freshness of a run): n/a.
- axis 26 (`stand not confirmed`): n/a — cited by the map (r10), not changed.
- axis 27 (the profile of a test row): n/a.
- axis 28 (the render site of the row form): n/a.
- axis 29 (append-only jsonl writers): n/a.
- axis 30 (the commands of a profile): n/a.
- axis 31 (role carriers: one owner per aspect): covered — the walk's form and the passage clause have ONE owner,
  architecture.md section A (the `design/*.md` row of the axis 31 table); designer.md and critic.md carry a pointer
  and the role's own consequence; PROJECT.md step 4 and CLAUDE.md carry pointers; no new carrier (no new document,
  the owner's word 17.11.2026); no restatement of the form outside section A.
- axis 32 (where judgment lives): covered — no check unit added; every new check is a role's judgment accepted by a
  tier above (1.2); `judgment: none -- <why>`.
- axis 33 ("which dispatch am I"): n/a — no code.
- axis 34 (one road): covered — the passage clause is the one road for an unknown shape; a `narrows` line is a fork,
  never a non-goal (critic Q12, designer rule 6 unchanged and consistent).
- axis 35 (sides of a story): n/a — cited by the map (axis 4 row), not changed.
- axis 36 (the row written against a substitute): n/a.
- axis 37 (a repeat stop): n/a.
- axis 38 (the dry census): n/a — no joint, route, price key or keyless kind changes.

(c) Detector, registered: for the walk — externally named: the plan critic (rule 24, mandatory for a new idea) and
critic question 10 on every reviewed package diff; for the passage clause — `none — discipline`, gap named in AR-2's
Detector field, planned detectors node U6 and the free-agent bar. A calibration check is not added here (fork F6).

(d) What stops it from being skipped: the designer's rule 1 is loaded with every designer dispatch; critic Q10 with
every critic dispatch; new-idea step 4 is in PROJECT.md, loaded every session; the critic on the plan is mandatory
for a new idea (PROJECT.md step 6). No code gate: "on discipline alone, detector: the critic's question 10 and rule 24
(c)". Promotion to a commit-msg line follows a leak in the log, not symmetry.

---

## 6. FORKS returned to the Lead / owner (none decided)

F1 — Place of the passage rule (edge 6). Options: (A) widen AR-2, title unchanged — 29 entries stay, index and boot
unchanged, the passage clause shares AR-2's Detector field with the census; (B) new AR-30 — its own five fields,
index +105 bytes, 30 of 30 entries (the next invariant must merge, step 10); (C) widen AR-2 and retitle it (e.g. "...
code reports and leaves a move, and never blocks an unknown shape") — index changes by the title delta. Recommendation:
A. The passage clause is AR-2's own invariant ("code reports and leaves a move") applied to an unknown shape; the owner
decided "not a new principle" for the map, and A spends no boot byte and no slot.

F2 — Owner question Q-i (a2D1, s6.unknownword; also r5, r8, r9, r10, a2C2, ax12D4). Today a case on an unknown surface,
and several doors (executor missing, S0 capabilities, unconfirmed stand), go to a PERSON; the factory does not block.
Options: (a) a door to a person counts as passage, nothing changes; (b) the role tries first as a free agent would
(e.g. runs a CLI case through its own shell, reads a desktop app's logs), and hands the person only what it cannot do
(a physical device, a credential); (c) per door, decided in U7. Recommendation: (b) — closest to the owner's words "он
бы меня спросил пару вещей и всё равно выдал бы какой-нибудь результат"; cost: U7 reworks `surfaces.py` hands and the
doors listed, and the price of a person's question becomes a role's attempt first. The passage clause text is written
neutral until the answer.

F3 — Owner question Q-ii (ax10C1, ax10D1-D3, ax10B2). Options: (a) artifacts stay English always (status quo; FR-30
binds only the package, not a project's artifacts); (b) the artifact language is a project fact: one config key with
default English, asked at onboarding (AR-3), roles write in it; English-only checks (ax10D2 bug headings, ax10D3
approval words, ax10A1 acceptance headings) become table rows per language; (c) artifacts follow the ticket's language
by role judgment. Recommendation: (b) — a key with a default is the AR-3 road and keeps code free of a language name
(AR-1); cost: the three English-only checks get language rows; a fixture with a non-English ticket cannot live in the
package as Cyrillic text (FR-30) and needs escaped strings or a forge-side fixture.

F4 — Owner question Q-iii (ax12D1, ax12D2, ax12V, ax12D5). Options: (a) a declared scope: functional only, the person
is told and nothing else happens (status quo, text kept); (b) the passage clause applies: a non-functional ask (load,
security, accessibility) is carried by the role as a free agent would, with the factory's critic, and reported as
such; (c) declared scope plus a door: the person's word sends a named non-functional ask to a role. Recommendation:
(b) — the owner's bar "не хуже свободного агента" reads on any ask the factory meets; cost: the S0 scope line and
onboarding lines 400-404 are rewritten in U7, and the report states the depth reached.

F5 — Boot bytes and the CLAUDE.md edit. Options: (a) the fuller CLAUDE.md edit (about +88) and justify; (b) only the
"change together" sentence (about +21) and justify — total about +123; (c) (b) plus an offset found by the boot-diet
batch at handoff. Recommendation: (b), with the delta recorded for the boot-diet batch; the designer found no
redundant sentence of equal size in the two paragraphs touched.

F6 — Detector registration for the walk. Options: (a) the critic as the externally named detector, no new check
(rule 10 (c) allows it; promotion on evidence); (b) a new weekly calibration check now (package specs and plans of
the week without a `variety:` / `axis N:` block), one more file in owns (`PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`).
Recommendation: (a).

F7 — The meaning of "silently" in the definition ("молча идёт по ветке значения по умолчанию"). Options: (a) a default
is not silent when declared in data (`absent_means`, a table default) AND reported in the run (a note, problem or
warning the role reads); (b) any default taken on an unknown value is a breach. Recommendation: (a) — it keeps AR-3's
"a default for every key" and FR-59's "the safe default it declares" consistent with the definition; under (b) AR-3
and the passage clause contradict each other. The passage clause in 3.1 is written for (a).

F8 — The map-cell update duty ("a change that alters how an axis is held edits that cell in the same commit"). Options:
(a) keep it in the walk text (one more duty on package changes; the map stays true); (b) drop it, the map is a dated
snapshot of 17.11.2026 refreshed by a scout when needed. Recommendation: (a) — a map no change updates is the
`docs/factory-map/` failure (a 28.09 snapshot that lags the code, dsg.lag).

F9 — Debt rows. SIBLING_MAP axis 4 / PROJECT.md "Бэклог и находки": a rule broken and not fixed now is a row in
`design/factory-rules-debt.md`. The map names breaches of FR-13 (an1, ax7A4, ax11A1) and FR-5/FR-57-class places
(r1-r12). Options: (a) none now; node U7's spec names each place and its fix (U7 exists in the idea's DAG); (b) U4 adds
debt rows now (owns widen to the debt file). Recommendation: (a) — U7 is the named node with an executor; rows written
now would be rewritten by U7 within days.

Noticed in the brief, not widened (designer rule 3): the brief lists "AR-7, AR-12, AR-29; P1, P2, P11, P22, P31; FR-13,
FR-47, FR-57" as touched; this draft adds AR-28 and FR-59 (the passage clause's "silent default" is their twin) and P13.

## 6a. Small technical choices closed by the designer (no design weight)

1. The critic's variety question is a sentence appended to Q10 (ARCHITECTURE; section A is architecture), not a new
   Q14; rule 24 names it for the plan gate. No question is renumbered.
2. architecture.md's "How a change walks this map" gets sentences inside steps 2 and 9; no step is added, so the
   references to "step 10" (`architecture_index.py`, its docstring, the file) stay valid.
3. The map cites no `test_*.py` file name and no brief path (edges E3, E5); fixtures are cited by description.
4. No changelog fragment: `design/` is not loaded at runtime and this is not a pile batch (changelog.d/README.md
   "one fragment per batch").
5. The builder does not commit: the commit touches mechanism paths (CLAUDE.md, PROJECT.md, role files) whose gate
   refuses a tier below the Lead's; the Lead commits after the critic with section 5 as the axis block.
6. Report ids are cited with a one-line legend naming the three digest files; `r1`-`r12` are t-1203 objects only.
7. Map cells use plain `AR-n` (no bold) everywhere.

---

## 7. The builder dispatch for U4

(Header lines are printed by `python -B tools/dispatch_new.py`; their content is below. `<wt>` is the builder's
worktree root. Dispatch only after the Lead has decided F1, F5, F7, F8 and the plan critic (U3) has passed; F2-F4 stay
open questions in the text either way.)

- given: this spec (sections 2, 3.1 or 3.2 per F1, 4); `ai-packages/qa-factory/design/architecture.md`;
  `ai-packages/qa-factory/design/factory-rules.md` (whole, PROJECT.md acceptance rule 1); `.claude/agents/designer.md`;
  `.claude/agents/critic.md`; `PROJECT.md`; `CLAUDE.md`; `tools/architecture_index.py` (parse rules).
- owns:
  C:/QAFactory/forge-repo/ai-packages/qa-factory/design/architecture.md
  C:/QAFactory/forge-repo/.claude/agents/designer.md
  C:/QAFactory/forge-repo/.claude/agents/critic.md
  C:/QAFactory/forge-repo/PROJECT.md
  C:/QAFactory/forge-repo/CLAUDE.md
  C:/QAFactory/forge-repo/AGENTS.md
  C:/QAFactory/forge-repo/docs/ARCHITECTURE_INDEX.md   (Option B only; generated)
  (paths of the worktree that mirror these.)
- non-goals: no file under `scripts/`, `references/`, `agents/`, `skills/`, `handoffs/`; no fix of any place the map
  names (node U7); no teaching of mobile (U8); no new document; no text in boot files beyond section 4.4/4.5; no
  edit of `test-layers.json` line anchors; no commit (the Lead commits).
- handoff: the uncommitted diff in the worktree + the report in the form of `.claude/agents/builder.md` rule 7 with
  the witness (every command below, verbatim tail) and the key-presence script in full source.
- edges (each with the invariant it protects):
  - E1 no line starting `## ` between `## A. Universality across projects` and `**AR-1 — ` — invariant: the index
    generator still sees all four sections and all 29 (B: 30) openers.
  - E2 no line starting `**AR-` and no bold `**AR-<n>` in inserted text — invariant: the opener count is exactly
    29 (B: 30), and `test_conductor_investigates_first.py` still finds the real AR-17 first.
  - E3 no `test_<name>.py` in inserted text — invariant: the gate-named test set is unchanged.
  - E4 no Cyrillic character in architecture.md (FR-30) — invariant: `selftest.py --lang` stays green.
  - E5 no main document cites the brief file — invariant: no role must read a brief (PROJECT.md "Лишних документов
    нет"); `test_role_carriers_one_owner.py` stays green.
  - E6 every map cell non-empty; `not addressed:` carries what a role does today or "not read" — invariant: no axis
    reads as covered by silence.
  - E7 Q-i, Q-ii, Q-iii stay questions — invariant: no owner decision is written by a builder.
  - E8 TEMPORAL: all files in one commit — before it, no rule points at a missing map; after it, specs whose primary
    draft starts after the merge owe the walk, and a pre-map spec is no critic finding.
  - E9 Option A: AR-2's opener line byte-identical, `architecture_index.py --check` green with no regeneration.
    Option B: regenerate; an exit 2 (byte cap or 30 entries) is a stop-and-report, never a title trimmed by the builder.
  - E10 boot bytes: report CLAUDE.md, PROJECT.md (and B: the index) sizes before and after (read the bytes before
    the first edit); a delta above 1.5 times section 4.6's estimate is a report line, not a trim of other text.
  - E11 POSITIONAL: the insert sits after the section A heading and before AR-1; the summary table before the first
    section is unchanged (A) or gains only `, AR-30` (B) — invariant: `verify()` finds table and headings agreeing.
- DoD (acceptance keys: the five files carry the texts of sections 2-4 as decided; every command below exits 0;
  the key script prints `ALL KEYS PRESENT` and `NEGATIVE CONTROL: red as expected`):
  1. `python -B <wt>/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/design/architecture.md` — run what it prints, or report its "no scenario or keep row covers" line.
  2. `python -B <wt>/tools/architecture_index.py --check`
  3. `python -m pytest <wt>/tools/test_architecture_index.py <wt>/tools/tests/test_role_carriers_one_owner.py <wt>/tools/test_handoff_rule_anchors.py -q`
  4. `python -B <wt>/tools/install_parity.py --check`
  5. `python -B <wt>/tools/agents_md.py` then `python -B <wt>/tools/agents_md.py --check`
  6. `python -B <wt>/ai-packages/qa-factory/scripts/selftest.py --lang`
  7. `python -B <scratchpad>/u4_keys.py <wt> --openers 29` (B: `--openers 30`)
  - test: none -- documents; the witness is the DOC-DISPATCH key-presence run (CLAUDE.md rule 11) | expected from: spec §2, §3, §4
  - AR-n change checks (from section 1): AR-2 — "no decision moves into code; no script changed" in words; AR-12 —
    "code_friction: not measured — no hook, guard, validator or role-called script changes"; AR-29 — no census edit.
- siblings: none -- the class walk is section 5 of this spec (all 38 axes) and the artifact sweep is in 4.1.
- designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261117-universality-variety-map-spec.md

### 7.1 The DOC-DISPATCH witness script (attached in full to the report, never committed)

Keys are quoted verbatim from this DoD (section 4 texts) before the run; matching is whitespace-normalised so a
rewrap does not break a key. The script runs its own negative control (one key removed -> must report failure).

```python
"""t-1207 / U4 key-presence witness (doc dispatch). Not committed. Usage: python -B u4_keys.py <root> --openers 29|30"""
import pathlib
import re
import sys

ARCH = "ai-packages/qa-factory/design/architecture.md"
FILES = [ARCH, ".claude/agents/designer.md", ".claude/agents/critic.md", "PROJECT.md", "CLAUDE.md"]
KEYS = [
    (ARCH, "**Universality.**"),
    (ARCH, "| Axis | Examples | Held by today | Proven on |"),
    (ARCH, "**Open owner questions**"),
    (ARCH, "**How the map is walked.**"),
    (ARCH, "variety: none -- <reason>"),
    (ARCH, "on a project shape the factory does not know"),
    (ARCH, "`dev:docs/OWNER_PRINCIPLES.md` (P1-P31)"),
    (ARCH, "The critic asks five questions."),
    (ARCH, "the Lead writing the plan of a new idea (the variety walk of section A)"),
    (".claude/agents/designer.md", "the variety walk of `design/architecture.md` § A"),
    (".claude/agents/critic.md", "VARIETY (§ A of the same file"),
    (".claude/agents/critic.md", "Q4, Q6, Q12 and Q10's VARIETY sentence of"),
    ("PROJECT.md", "вердикт по каждой оси карты различий (`architecture.md` § A)"),
    ("CLAUDE.md", "critic questions 10-11, designer rule 1 and new-idea step 4 change together"),
]
BRIEF = "20261117-universality-variety-map-brief"


def norm(text):
    return " ".join(text.split())


def problems(texts, openers):
    out = []
    for rel, key in KEYS:
        if norm(key) not in norm(texts[rel]):
            out.append("missing key in %s: %s" % (rel, key))
    arch = texts[ARCH]
    if re.search("[\u0400-\u04ff]", arch):
        out.append("Cyrillic character in architecture.md")
    start = arch.find("## A. Universality across projects")
    end = arch.find("**AR-1 — ")
    block = arch[start:end] if 0 <= start < end else ""
    if not block:
        out.append("section A head or AR-1 opener not found in order")
    lines = block.splitlines()[1:]
    if any(l.startswith("## ") for l in lines):
        out.append("a '## ' line inside the inserted block")
    if "**AR-" in block:
        out.append("a bold AR opener inside the inserted block")
    if re.search(r"test_[a-z0-9_]+\.py", block):
        out.append("a test file name inside the inserted block")
    rows = [int(m.group(1)) for m in re.finditer(r"^\| (\d+)\. ", block, re.M)]
    if rows != list(range(1, 14)):
        out.append("map rows are %s, expected 1..13" % rows)
    found = len(re.findall(r"^\*\*AR-\d+ — ", arch, re.M))
    if found != openers:
        out.append("AR openers: %d, expected %d" % (found, openers))
    for rel in FILES:
        if BRIEF in texts[rel]:
            out.append("%s cites the brief file" % rel)
    return out


def main():
    root = pathlib.Path(sys.argv[1])
    openers = int(sys.argv[sys.argv.index("--openers") + 1]) if "--openers" in sys.argv else 29
    texts = {rel: (root / rel).read_bytes().decode("utf-8") for rel in FILES}
    real = problems(texts, openers)
    for p in real:
        print("FAIL", p)
    if not real:
        print("ALL KEYS PRESENT")
    neg = dict(texts)
    neg[ARCH] = neg[ARCH].replace("**Universality.**", "")
    red = problems(neg, openers)
    print("NEGATIVE CONTROL:", "red as expected" if red else "NOT RED (the script is broken)")
    sys.exit(0 if not real and red else 1)


main()
```

### 7.2 Index regeneration (Option B only)

`python -B <wt>/tools/architecture_index.py` then `python -B <wt>/tools/architecture_index.py --check`; report the
byte size of `docs/ARCHITECTURE_INDEX.md` before and after.

---

## Reading trail

| What | Range | Why |
|---|---|---|
| docs/tasks/specs/20261117-universality-variety-map-brief.md | 1-138 (whole) | the owner's words, decisions, definition, nodes |
| docs/tasks/specs/reports/20261117-universality-scout-t-1200-axes-1-6.md | whole | axes 1-6 objects |
| docs/tasks/specs/reports/20261117-universality-scout-t-1201-axes-7-13.md | whole | axes 7-13 objects |
| docs/tasks/specs/reports/20261117-universality-scout-t-1203-mobile-stage-walk.md | whole | r1-r12, stage objects |
| ai-packages/qa-factory/design/architecture.md | 1-296 (whole) | section A, AR-2 text, walk steps, line 3 stale pointer |
| .claude/agents/critic.md | 225-290 | Q6-Q13, rule 23-24 text and anchors |
| .claude/agents/designer.md | 1-50 | rule 1 anchor sentence |
| CLAUDE.md | 273-275 (grep) | the rule 10 paragraph lines |
| PROJECT.md | 130-131 (grep) | new-idea step 4 lines |
| docs/SIBLING_MAP.md | 1-116, 473-657, heading grep | axes 1-38 list, axes 1, 4, 31-38 text |
| tools/architecture_index.py | 1-160 | parse rules (`## ` stops, opener regex), caps 3072 / 30 |
| tools/architecture_gate.py | 1-70 | line forms (pointed at, not copied) |
| tools/session_context.py | 1380-1409 | boot budget counts CLAUDE.md imports |
| tools/install_parity_anchors.json | 135-184 | anchored line starts of critic.md and designer.md |
| tools/tests/test_role_carriers_one_owner.py | 254-342 | main documents, deleted-file and brief-path scan |
| tools/test_quarantine.py | 1120-1149, 1350-1373 | gate-named files refuse `enter` |
| ai-packages/qa-factory/scripts/selftest.py | 665-736 | `_PROSE_CARRIERS` includes architecture.md; no design/ size cap (grep 359-419) |
| ai-packages/qa-factory/scripts/tests/test-layers.json | 25-50 + grep | `named_by` line anchors; only non-emptiness checked (selftest.py:629 grep) |
| ai-packages/qa-factory/scripts/tests/test_conductor_investigates_first.py | 170-189 | `block_from(arch_text, "**AR-17")` |
| ai-packages/qa-factory/scripts/tests/test_sizing_impact_scale.py | 136-145 | AR-22 Breakage line pinned |
| ai-packages/qa-factory/changelog.d/README.md | whole | fragment rule (one per batch) |
| docs/TESTING.md | 75-144 | `test:` line, witness scope |
| Greps with counts | section 4.8 | readers, each negative with a same-shape positive control |

Needed beyond the manifest: the `tools/owns_readers.py` block for the five touched files (not attached; the plan
critic re-runs it, Q13 (d)). Index size and boot sizes are hand estimates, not measured (no shell).

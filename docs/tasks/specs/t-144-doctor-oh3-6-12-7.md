# t-144 — DRAFT spec: stream "doctor" — OH3-6, OH3-12, OH3-7 (qa-doctor speaks to a person only about what is theirs)

Status: DESIGNER DRAFT for Lead acceptance (forks returned, not decided). Author: designer (Opus), 12.11.2026.
Brief: Lead intent brief of t-144 (stream "doctor", nodes OH3-6, OH3-12, OH3-7).

## 0. Brief contradictions and freshness findings (read first)

1. **OH3-7 is not a node of batch onboarding-forge/1.** Its row is `plans/piles/onboarding-forge/batch-2-onboarding-roles-forge-p3.md:32`
   (batch 2, also taken by dev1 on 12.11.2026). Batch 1 holds OH3-6 (:29) and OH3-12 (:31) only; the batch-1 lines that mention
   "OH3-5"/"OH3-7" text are OH3-37 (:34) and OF1-4 (:70). Lead: either move the row or record the node under batch 2 in the journal
   (`node: onboarding-forge/2/OH3-7`). The queue line `onboarding-forge/1 -> onboarding-forge/2` (batch-2 :13) makes one dispatch
   across both legal only if the Lead says so.
2. **OH3-7 still holds on `main`** (re-check requested by the brief). Trail:
   - `skills/qa-doctor/SKILL.md:175` runs `project_gitignore.py --root . --check` in step 3 with no condition; step 2 (`:110`) and
     step 7 (`:215`) are gated on `qa-factory/config.json`, step 3 is not.
   - `skills/qa-doctor/SKILL.md:50` runs the smoke with `--report "qa-factory/state/doctor-install-smoke-latest.json"` (relative to
     the cwd) before anything checks onboarding; `scripts/install_smoke.py:573-586` and `run_report` (`:518-560`,
     `atomic_json(path, ...)`) write it with no onboarding check. So the "own receipts in `state/`" premise is still true.
   - OH3-5 (0.10.7) fixed only `host_probe.main` (exit 3, no write; `docs/SIBLING_MAP.md:256`, axis 10). The remaining pre-onboarding
     writers (`install_smoke --report`, `factory_dashboard`) are node OH3-37 (batch 1 :34), still `ожидает`.
   - `scripts/project_gitignore.py:29-30` says explicitly: "No qa-factory/config.json under --root is not refused here ... that
     check belongs to the caller" — the caller is the doctor, and it does not make that check.
3. **The doctor cannot do the guard-probe Write it is told to do.** `phases/repair.md:57-58` tells the doctor to `Write` a throwaway
   line to `qa-factory/state/doctor-guard-probe-<session>.txt`, and `phases/repair.md:39` tells it to write the person's words file
   "with the host's file tool"; but `SKILL.md:12-18` `allowed-tools` lists Read, Glob, Grep, Bash, Agent, Task — no `Write`. This is
   the likely mechanism of OH3-6's first symptom (the doctor relayed `guard_parse.reason`, `scripts/host_probe.py:463-467`, "Make one
   ordinary call of each shape ... then re-run --check", to the person). Fork F2.
4. **Stale carriers in the same skill** (same class as OH3-12, they describe the doctor's writes/questions wrongly):
   `skills/qa-doctor/README.md:25` ("the only file this skill writes") and `:62` ("Never asks a question"); `evals/evals.json` id 4
   (same two claims) — contradicted by `SKILL.md:34-40` (three questions; dashboard + telemetry + receipts + word-gated writes).
5. **Byte ceiling.** Carrier: `scripts/selftest.py:341` `SKILL_MD_MAX_BYTES = 19_000` (bytes after CRLF->LF, `content_size.py:5-6`),
   also pinned at 19000 by `test_host_probe_shapes.py:1064` and `test_session_identity.py:624` (both QUARANTINED in
   `test-layers.json`, not run by a builder). Current size: **estimate, not measured — ≈ 18,750 B ± 250, headroom ≈ 0–500 B.**
   Counting carrier: Grep line-length histogram over `SKILL.md` (lines with length >= N: N=1:267, 10:237, 20:225, 30:215, 40:206,
   50:190, 60:178, 70:167, 80:146, 90:90, 100:23, 120:12, 140:8, 160:5; 335 lines), trapezoid sum ≈ 18,430 chars + 335 LF. The
   designer has no shell; the builder's first move measures it exactly (item 0). OF1-4 (batch 1 :70) and OH1-9 (batch 2 :30) edit the
   same file after this node and need headroom too — hence the design target **net bytes <= 0** for this node (item 7).

## 1. Scope, AR-n, owners and census (designer rule 1; CLAUDE.md rule 10, P27, AR-29)

Goal: the person reads from the doctor only what they must do or decide; everything the factory can do, the doctor does; everything
that needs nothing from the person goes into one last block. Before onboarding the doctor asks for nothing but onboarding.

AR-n touched and the change check each demands (written into the DoD, §4):

| AR | how it is touched | kept by / change check |
|---|---|---|
| AR-16 (one question form) | the doctor's person-facing text loses script names, factory-internal rows and working-tree narration (OH3-6, OH3-12) | `references/human-questions.md` "may never carry" list applied to the report body; eval rows 14, 15 assert it; no new question is added under F1-A (under F1-B the new question follows rules 1-6, with prices) |
| AR-9 (a door the receiver can use) | a person is given a skill, a closed question or an action of their own, never a factory script | item 3 rule + eval 14 `no-factory-script-in-person-steps` |
| AR-11 (only the tools the work needs) | `Write` joins the doctor's `allowed-tools` (F2) | change check "a new tool is named by a phase step": `phases/repair.md` already names two Write targets; `role_load.py` does not cover skills (n/a, agents only); `selftest.py --limits` run |
| AR-14 (one artifact, one writer) | the `.gitignore` block gets a second CALLER (the doctor), not a second writer | the only writer stays `project_gitignore.write_block`; the doctor calls the same CLI onboarding calls (`p4-generate.md:624`) |
| AR-17 / P22 (settle before asking) | the doctor makes the guard-probe calls and the `.gitignore` write itself instead of handing them over | items 2, 4 |
| AR-25 (every state a way out) | "block missing after onboarding" gets a move (the write), "write failed" a factory note | item 4 edges |
| AR-28 (an unknown never becomes a pass) | factory-owned unknowns move out of the main part but stay counted as not `ok` | item 5: READINESS line never reads "ok - n of n" while FACTORY NOTES holds a non-ok row |
| AR-29 (code judges data, roles judge meaning) | no `scripts/*.py` check unit is added or altered | `judgment: none -- skill text and evals only; no check unit of scripts/*.py added or altered`; census unchanged |
| AR-19 (twins) | onboarding and qa-story person texts are the same class | §6 siblings (queued, not widened) |

Checks this spec adds or alters — owner served and census class:

| # | check | owner served | census class | where it runs |
|---|---|---|---|---|
| C1 | "onboarded?" = `qa-factory/config.json` exists in the current directory, gating step 3's `.gitignore` line | data (file presence) | shape (presence) | the doctor's own text (same predicate as steps 2, 7 and verdict row 3); no code unit, no census row |
| C2 | a step addressed to the person names no factory script, flag or plugin path | judgment (the doctor decides what is the person's; accepted by the eval grader, a tier above) | would be word-list if coded — deliberately NOT coded (FR-12) | the doctor's text + eval rows 14/15 |
| C3 | a non-`ok` row whose `remedy.owner` is `factory` goes to FACTORY NOTES | data (`remedy.owner` field from `readiness.py`) | shape (field routing) | the doctor's text; no code unit |
| C4 | `guard_parse` re-checked once after the doctor's own calls | data (`host_probe.py --check` verdict, unchanged script) | unchanged (existing unit) | `phases/repair.md` |
| C5 | eval assertions (rows 1, 3, 4, 9, 13, 14, 15) | judgment (accepted by the eval grader) | n/a (not a script) | `evals/evals.json` |

Reused function in a new role: `project_gitignore.py --check/--write` — today onboarding's writer and the doctor's report; after this
spec also the doctor's own repair (F1-A). Error direction allowed: a FALSE "not whole" (block present, reported missing) is safe — the
`--write` that follows is a no-op (`write_block` returns early on `_is_whole`, mtime kept). A FALSE "whole" is the unsafe side (state
stays visible to git) and must stay unreachable; adversarial inputs that must stay on the safe side (all already handled by
`_is_whole`/`write_block`, `project_gitignore.py:81-127`): header present but one of our lines also elsewhere; a partial old block; the
old header (`OLD_HEADERS`); a CRLF file; a project line equal to one of ours; no `.gitignore` at all; an unreadable install table
(exit 2, never a guess). No code change to `project_gitignore.py` in this spec.

One road (designer rule 6, P31): the onboarded/not-onboarded branch is an ordinary condition of the task with one predicate shared by
steps 2, 3, 7 and verdict row 3 — not an exception. The guard-probe write uses "the host's file tool" on every host (the host adapter
normalizes the name, `host_probe.py:330`); no host, language or project is given another road. The `.gitignore` block under F1-A is
written by the same CLI on the same road as onboarding's `p4-generate.md:624`. No exclusion is left; nothing goes to the owner from
this section.

## 2. Requirements (numbered; each names file/section, behaviour, test)

Paths are from `ai-packages/qa-factory/`.

**0. Measure first (no edit).** Exact bytes of `skills/qa-doctor/SKILL.md` before any edit: `python -B scripts/selftest.py --limits`
plus the byte count printed by the key script of §4 (it prints `len(bytes.replace(b"\r\n", b"\n"))`). Recorded in the report as
`before: N B`. Test: the report line.

**1. `SKILL.md` frontmatter — `Write` joins `allowed-tools` (F2, recommended A).** Add `  - Write` after `  - Bash`. Its permitted
targets are written in item 2 and the writes sentence (item 6): `qa-factory/state/doctor-guard-probe-<session>.txt` and
`qa-factory/artifacts/<TICKET>/state/words/<name>.txt` (both already named by `phases/repair.md:39,57-58`). Never a config, a
`pipeline.json`, `controller.json`, `events.jsonl`, an artifact a role wrote. Test: eval 11 `repairs-by-code` (unchanged) and eval 14
`guard-write-by-the-doctor`; key presence `  - Write` (§4).

**2. Step 1b + `phases/repair.md` last section — the doctor settles `guard_parse` itself (OH3-6 symptom 1).**
- `SKILL.md:102`: replace "`guard_parse` in that report: `phases/repair.md`, last section." with exactly:
  "`guard_parse` not `verified`: make the missing call yourself (`phases/repair.md`, last section), then `--check` once."
- `phases/repair.md` section "Does the pre-tool guard still parse this host's events?":
  - after "a shell call (the ALLOW echo of step 1b is one)" add: "; if `families.bash` is still unverified, step 2's
    `git rev-parse --show-toplevel` is another";
  - "If `families.write` is still `unverified`, make one: `Write` a single throwaway line" -> "make one with the host's file tool: a
    single throwaway line" (same path);
  - the `unverified` bullet becomes: "`unverified` after those calls and one more `--check` -> one FACTORY NOTES line: which call has
    no clean record, in plain words. Its `reason` tells you what to do; it is never shown to the person."
  - the `guard_defect` bullet: "Print its `reason`" -> "One FACTORY NOTES line: its `reason` in plain words and the `host_version`";
    the rest ("stop ... never becomes the next action") stays.
  - Untouched: `FLAG` and `state/words/` (pinned by `test_person_words.py:641`).
- Test: eval 14 assertions `guard-write-by-the-doctor`, `one-recheck-only`, `reason-not-relayed`.

**3. "Rules of printing" — the person is given no factory script (OH3-6 symptom 2 and the class).** Insert as the first bullet:
"- **The person gets a skill, a closed question or an action of their own - never a factory script, flag or plugin path.** Run such a
step yourself, or name the skill that owns it; a script's `reason` is addressed to you."
Invariant: a step addressed to the person never names a `scripts/*.py`, `hooks/run-py.cmd`, `${CLAUDE_PLUGIN_ROOT}` or a flag of
them. Adversarial inputs that must stay on the safe side: a `remedy.steps` entry from `readiness.py` that names a script
(`readiness.py:654` `run env_probe.py --json again`, `:1005` `dependency_drift.py ...`, `:1113` `host_probe.py --prepare ...` — all
`remedy.owner: factory` today, so they go to FACTORY NOTES as a fact, not as steps); a refusal `reason` written for a role
(`host_probe.py:466`). Must stay allowed (not over-applied): a command of the person's OWN tool (`glab auth login`, eval 12), a
`/qa-factory:` skill in the "Next action" line, turning a VPN on (eval 6). Test: eval 14 `no-factory-script-in-person-steps`; evals 6,
8, 12 unchanged and still passing (no over-application).

**4. Step 3 — the `.gitignore` block: before onboarding nothing, after onboarding the doctor writes it (OH3-7 + OH3-6 symptom 2;
F1, recommended A).** Replace "The third lists the `.gitignore` lines it lacks; `--write` rewrites the block." (`SKILL.md:178`) with
exactly (F1-A wording):
"Run the third only when `qa-factory/config.json` exists in the current directory (before that the block is onboarding's). Lines
listed: run it with `--write` yourself, then `--check`; tell the person to commit `.gitignore`."
The code fence of step 3 keeps its `--check` line. Behaviour by world (TEMPORAL edge, CLAUDE.md rule 11 (i)) — the move that creates
the config is onboarding (`p4-generate.md`, `onboard_apply.py`), and the same onboarding writes the block (`p4-generate.md:624`,
`--phase early`):
- **Before onboarding** (no `qa-factory/config.json` in the cwd): the third command is not run; the report carries no `.gitignore`
  line, no warning about `qa-factory/state/` or committing receipts, no step; verdict row 3 (`/qa-factory:qa-onboarding`) is the next
  action. Invariant: a project that is not onboarded is asked for nothing but onboarding.
- **After onboarding, block whole**: `--check` exits 0 silently -> nothing printed (unchanged).
- **After onboarding, block missing or out of place** (onboarding interrupted before 8b, an old install, a hand edit): the doctor
  runs `--write`, then `--check`; on exit 0 the main part carries one ordinary line: the factory's block was put back into
  `.gitignore`, commit it with the next change. Not an AUDIT violation, not the next action (verdict row 8 does not fire on it).
- **`--write` or the re-`--check` fails** (exit 2 table error, an `OSError`/traceback on a read-only file, still listing lines):
  one FACTORY NOTES line with the fact, `owner: factory`; no retry, no step to the person, never the next action.
- Positional invariant: the gate sits before the command, not after — a not-onboarded project must never even produce the
  `--check` output that the doctor would then have to suppress.
- Test: eval 1 (extended, before world): assertion `no-gitignore-demand-before-onboarding`; eval 14 (after world):
  `gitignore-block-written-by-the-doctor`.
- Under F1-B instead: the sentence becomes "Lines listed: after the report ask once whether to put the factory's block back
  (`phases/` none; form `references/human-questions.md`, rules 1-6), and run `--write` only on yes"; the "Three questions" sentence
  (`SKILL.md:34-37`) and "What this skill never does" first bullet name it; eval 14 asserts the closed question instead.

**5. "Rules of printing" + "Report format" — FACTORY NOTES, the last block (OH3-12; F3, recommended A).**
- Insert as the second bullet of "Rules of printing":
  "- **Nothing for the person goes last**, under `FACTORY NOTES (nothing for you to do)`: each non-`ok` `remedy.owner: factory` row,
  its fact in one line. No working tree, `git status` or own writes."
- Report format block: READINESS line becomes
  "READINESS: ok - <n> of <n>   (or: <k> of <n>, your help is needed | <k> of <n>, the rest in FACTORY NOTES)";
  after `Next action: <exactly one line>` add
  "FACTORY NOTES (nothing for you to do)      ... only when there is one\n  <capability>  <status>  <the fact, one line>".
- The sentence "The complete repository inventory follows this block and is exempt from the line limit." becomes "FACTORY NOTES and
  the complete repository inventory follow this block; both are exempt from the line limit."
- What goes there: a non-`ok` capability with `remedy.owner: factory` (e.g. `host_hooks` unknown, `injection: unverified` after the
  probe, a guard-parse fact, a dependency check that did not run), `ACTIVITY NOT RECORDED` (`SKILL.md:27`), a failed `.gitignore`
  write (item 4). What never goes there: an AUDIT line (verdict row 8 may make it the next action, eval 10), a STORIES line, a
  `repair.md` recover/release result (it answers the person's own confirmation), a row with `remedy.owner: user`, the
  unreachable-host line of eval 6 (its first step, the VPN, is the person's).
- Edges: FACTORY NOTES empty -> the header is not printed (the READINESS line already says "ok - n of n"); every non-ok row is
  factory-owned -> READINESS reads "<k> of <n>, the rest in FACTORY NOTES", never "ok - n of n" and never "your help is needed"
  (FR-10, AR-28); a note's wording carries the observed fact without "failed", "could not" or "not confirmed" phrasing that reads as
  a breakage when nothing is broken (the injection case: "the role-context delivery has no receipt in this session yet"); the
  verdict table's rows 5/5a/5b are unchanged (a factory-owned row is still never the next action).
- Never narrated anywhere (main part or notes): `git status`, untracked/unindexed files (`qa-factory/records/journal.jsonl`), "I did
  not commit", what the doctor wrote in `state/`. The dashboard is named only as a place to open ("Dashboard: <path>") after step 7.
- Test: eval 15 (all four assertions); eval 9 and eval 13 expected outputs updated (the `host_hooks` row is in FACTORY NOTES; their
  assertion NAMES unchanged — eval 13's names are pinned by `test_host_probe_shapes.py:1070-1071`).

**6. The writes sentence and the "never" list stay true.**
- `SKILL.md:38-40` becomes: "**It writes the dashboard, activity telemetry, smoke and host-probe receipts, the guard-probe file, the
  factory's `.gitignore` block (step 3), and - only on a person's explicit word - `archive_task.py`'s flag and `repair.md`'s
  `controller.py --operation recover|release`.**" (F1-B: the block moves into the "on a person's word" half.)
- "What this skill never does", bullet "Never fixes an audit finding itself": "Its only repairs are `controller.py --operation
  recover` and, on their word, `release` (`phases/repair.md`)" -> add ", plus the `.gitignore` block of step 3".
- `skills/qa-doctor/README.md:25` and `:62` brought in line with the charter (what it writes; that it asks the questions of
  `SKILL.md:34-37`). Test: key presence (§4) + eval 4 updated.

**7. Byte budget — cuts that pay for items 1-6 (net bytes <= 0).** Estimated additions of items 1-6 ≈ 810 B (allowed-tools 10,
writes sentence 60, step 1b 54, step 3 135, two printing bullets 410, READINESS 40, FACTORY NOTES lines 80, exempt sentence 20).
Cuts (estimated ≈ 1,000 B):
- (a) **Move section 7b into a new `phases/permissions.md`** (≈ 580 B saved). `SKILL.md` keeps: "### 7b. The permission block - only
  when asked\n\nWhen asked why every command needs a confirmation, read `phases/permissions.md` and follow it." The phase file holds
  today's `SKILL.md:224-237` verbatim, with one correction: "the factory writes nothing into a project except `qa-factory/`" ->
  "except `qa-factory/` and its own `.gitignore` block". Read only when asked (same pattern as `phases/archive.md` in step 6) — no
  added Read on an ordinary run (FR-55). `audit_factory.py:31` "every phases/*.md a skill references exists" stays green because
  the file exists.
- (b) "Never report a green it cannot back": cut the anecdote `SKILL.md:310-312` ("Its green lines are worth something ... halted in
  S0 on a missing executable.") (≈ 230 B); the three bullets stay.
- (c) "What this skill never does", first bullet (`:322-324`) -> "- Never asks a clarifying question to produce a **fact**; its
  questions are those of the opening section." (≈ 150 B; the list of questions lives once, at `:34-37`).
- (d) `SKILL.md:244-245`: drop the parenthetical "(a dropped VPN once became a project's single next action)" (≈ 55 B).
- Must NOT be cut or reworded (role-rules carriers, `design/role-rules.json:260,261,432,433,473`, and `test_story_run_monorepo.py`
  T5/T6): "partial answer: re-probe", "no pair, no probe", "never ask for a key value", "no third bucket", "(it finds its own
  session)", "exists in the current directory, run:"; and must not reintroduce "exists at that".
- If the measured `after` exceeds 19000 B, or exceeds `before`, the builder does NOT invent further cuts: it stops and returns the
  numbers as a question (the next candidates, for the Lead: the Codex code-mode paragraph `:56-60`, the stray `# Evidence capability
  checks` section `:332-335`).
- Test: `selftest.py --limits` green; `before`/`after` bytes in the report; `after <= 19000`; target `after <= before`.

**8. Evals (`skills/qa-doctor/evals/evals.json`) — rows, no test file.** Ids stay unique; ids 12 and 13 keep their assertion names
(pinned by `test_vcs_evidence.py:613-615` (keep) and `test_host_probe_shapes.py:1068-1071` (quarantined)).
- id 1 (variant, before world): prompt adds "`qa-factory/state/` already holds this run's smoke receipt and `.gitignore` has no
  factory block"; expected output adds "no `.gitignore` line, no warning about committing `qa-factory/state/`"; new assertion
  `no-gitignore-demand-before-onboarding`.
- id 3: assertion `dashboard-rebuilt` -> "The report names where to open the rebuilt dashboard; it does not narrate other files it
  wrote, the working tree or git status."
- id 4: expected output and assertion `dashboard-is-only-write` rewritten to the charter's writes and questions (item 6); assertion
  name may stay.
- id 9, id 13: expected output — the `host_hooks` unknown row stands in FACTORY NOTES; assertion names unchanged.
- **new id 14 (OH3-6, after world):** "Run qa-doctor in an onboarded project. After the allow/deny pair `host_probe.py --check`
  reports `guard_parse` unverified for the file-write family, and `.gitignore` lacks the factory block." Assertions:
  `guard-write-by-the-doctor` (the doctor writes the throwaway line with the host's file tool and re-runs `--check`),
  `one-recheck-only` (one extra `--check`, no second `--prepare`), `reason-not-relayed` (the `reason` text "Make one ordinary call
  ..." never reaches the person), `gitignore-block-written-by-the-doctor` (F1-A: `--write` then `--check` run by the doctor, one line
  asks the person to commit `.gitignore`; F1-B: one closed question with priced options instead),
  `no-factory-script-in-person-steps` (no `*.py`, `run-py.cmd`, `${CLAUDE_PLUGIN_ROOT}` or script flag in any step addressed to the
  person).
- **new id 15 (OH3-12, right after onboarding):** "Run qa-doctor right after onboarding: the context probe returned no injection
  receipt (`injection: unverified`), `qa-factory/records/journal.jsonl` is untracked, the cost summary in `qa-factory/state/` was
  updated." Assertions: `no-factory-rows-in-main` (no `remedy.owner: factory` row above FACTORY NOTES), `no-working-tree-narration`
  (no git status, untracked files, "I did not commit", `state/`), `fact-in-notes-without-alarm` (the injection fact is in FACTORY
  NOTES, without "failed"/"could not"), `readiness-not-green` (the READINESS line does not read "ok - n of n" while the note stands).
- Test: JSON parses, ids unique (key script §4); the eval grader judges the meaning (C5).

**9. Changelog fragment.** New `changelog.d/onboarding-forge-1-doctor-person-text.md` (name rule `changelog.d/README.md:8`), one
bullet per change (items 1-5), English, no Cyrillic. Test: `selftest.py --lang`.

## 3. Edges (consolidated; each with the invariant it protects)

| edge | behaviour | invariant |
|---|---|---|
| no `qa-factory/config.json` in cwd (before world) | step 3's `.gitignore` command not run, no line, no warning | a not-onboarded project is asked for nothing but onboarding (FR-5) |
| config in a parent folder only (nested project) | treated as not onboarded, like steps 2/7 and row 3 | one predicate for "onboarded" across the skill (P31) |
| after world, block whole | silent | unchanged |
| after world, block missing/out of place | doctor `--write` + `--check`, one "commit `.gitignore`" line | the factory's own block is the factory's to write (same road as `p4-generate.md:624`) |
| `--write` raises / exit 2 / still listing | one FACTORY NOTES line, no retry, not next action | a factory failure is never the person's errand (row 5a) |
| person removed the block on purpose | F1-A rewrites it each run (named cost of F1-A) | see F1 |
| `guard_parse` unverified, write family | doctor writes the throwaway file, `--check` once | the doctor settles evidence it can produce; one re-check, no loop (eval 9 spirit) |
| `guard_parse` unverified, bash family | step 2's `git rev-parse` is the extra shell call, `--check` once | same |
| the Write is refused by the guard | that refusal is the evidence: `--check` reports `guard_defect` -> FACTORY NOTES, stop | never a plugin edit, never a retry with variations |
| exit 3 (not onboarded) | no pair, no probe, no Write | no pre-onboarding write by the doctor's own hand |
| FACTORY NOTES empty | header omitted | silence only when READINESS already says ok |
| every non-ok row factory-owned | READINESS "<k> of <n>, the rest in FACTORY NOTES" | never a green the evidence cannot back (AR-28, FR-59) |
| a `remedy.owner: user` step names a factory script | the doctor runs it (read-only) or names the owning skill | the person never gets a script (AR-9) |
| a person's own CLI command (`glab auth login`) | stays a step | item 3 is not over-applied (eval 12) |
| measured `after` > 19000 or > `before` | builder stops, returns numbers as a question | no invented cuts; anchors safe |

Conflicting requirement pairs and their resolution: (i) OH3-12 "hide factory rows" vs "never report a green it cannot back" ->
resolved by the READINESS count (item 5). (ii) OH3-6 "the doctor runs the step" vs "never fixes an audit finding itself" -> resolved by
naming the `.gitignore` block as the one extra repair (item 6). (iii) OH3-12 "no own writes narrated" vs eval 3 "confirms the dashboard
write" -> eval 3 rewritten (item 8). (iv) `allowed-tools` least privilege vs `repair.md`'s two Writes -> F2.

## 4. Dispatch header (R11-f) — for the Lead to copy after accepting the forks

given: this spec (`C:\QAFactory\forge-repo\docs\tasks\specs\t-144-doctor-oh3-6-12-7.md`, §2-§3 are the DoD source); `C:\QAFactory\forge-repo\ai-packages\qa-factory\design\factory-rules.md` (whole); `C:\QAFactory\forge-repo\plans\builder-rules.md`; `C:\QAFactory\forge-repo\ai-packages\qa-factory\references\human-questions.md`; `C:\QAFactory\forge-repo\ai-packages\qa-factory\design\role-rules.json` (rows 260, 261, 432, 433, 473); the three findings of `C:\QAFactory\forge-repo\plans\piles\onboarding-forge\findings\` named in the brief
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\skills\qa-doctor\SKILL.md
C:\QAFactory\forge-repo\ai-packages\qa-factory\skills\qa-doctor\evals\evals.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\skills\qa-doctor\phases\repair.md
C:\QAFactory\forge-repo\ai-packages\qa-factory\skills\qa-doctor\phases\permissions.md
C:\QAFactory\forge-repo\ai-packages\qa-factory\skills\qa-doctor\README.md
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\onboarding-forge-1-doctor-person-text.md
non-goals: any `scripts/*.py` edit (`project_gitignore.py`, `install_smoke.py`, `host_probe.py`, `readiness.py` stay as they are); OH3-37 (pre-onboarding writers' root); OF1-4 (browser readiness); OH1-9 (change-request marker); `gate_preflight.py`, `onboard_apply.py`, `config_contract.py`, `hooklib.py`; onboarding and qa-story texts (siblings, queued); verdict row 8 semantics
handoff: the builder report per `.claude/agents/builder.md` rule 7 at the path the Lead names at dispatch
edges: §3 of this spec, every row
DoD: items 0-9 of §2 hold; `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for skills/qa-doctor/SKILL.md skills/qa-doctor/evals/evals.json skills/qa-doctor/phases/repair.md skills/qa-doctor/phases/permissions.md skills/qa-doctor/README.md` and every file it prints that is not in the `quarantine` section (by reading `test-layers.json`: SKILL.md -> keep `test_story_run_monorepo.py` (detector, T5/T6 pin the doctor text); the rest expected "no scenario or keep row covers" = a report line); `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang` (size cap and role-rules anchors are touched); the doc-dispatch key run below with its negative control
siblings: onboarding (`skills/qa-onboarding/SKILL.md`, `phases/p*.md`) and qa-story (`skills/qa-story/SKILL.md`, `phases/s*.md`) person-facing texts that may hand a `*.py` to a person or narrate internals — queued by the Lead (§6), not in owns; axis 5 row "Conductor's own investigation before a question" (three conductor skills); axis 10 (OH3-37)
designer: C:\QAFactory\forge-repo\docs\tasks\specs\t-144-doctor-oh3-6-12-7.md

Doc-dispatch key run (CLAUDE.md rule 11, three properties): keys quoted verbatim from §2 BEFORE the run; the script attached in full
in the report, never committed; a negative control with one key removed from a COPY of `SKILL.md` must report failure. Keys:
`SKILL.md` — `  - Write`; "make the missing call yourself"; "then `--check` once."; "Run the third only when `qa-factory/config.json`
exists in the current directory"; "tell the person to commit `.gitignore`"; "never a factory script, flag or plugin path";
"FACTORY NOTES (nothing for you to do)"; "No working tree, `git status` or own writes."; "the rest in FACTORY NOTES";
"read `phases/permissions.md`"; plus the six must-keep anchors of item 7; absent: "exists at that", "rewrites the block. The".
`phases/permissions.md` — "its own `.gitignore` block"; "The human writes that file, not". `phases/repair.md` — "it is never shown to
the person"; "with the host's file tool"; `state/words/`. `evals.json` — parses; ids unique; ids 14 and 15 present; assertion names of
§2 item 8 present; id 13 names unchanged. The script also prints `len(bytes.replace(b"\r\n", b"\n"))` of `SKILL.md` (item 0/7).

Live proof (FR-33, PROJECT.md «Командная работа» p. 9): the behaviour change is "closed by code, not proved" until a live doctor run
(before onboarding on an empty git folder; after onboarding with a removed block and a cleared guard-parse receipt). The Lead moves
that row to the `live-runs` pile.

## 5. FR walk A-G (PROJECT.md, package change p. 1)

- A — FR-2: the person's door is a skill, a question or their own action (item 3). FR-3: under F1-A the factory's own block is not
  put to the person as a choice. FR-5: before onboarding the doctor demands no artifact only onboarding produces (item 4). FR-48: the
  doctor settles the guard-probe and the block itself before anything reaches a person (items 2, 4).
- B — FR-6: report body follows `human-questions.md` "may never carry" (items 3, 5). FR-7: no question re-asked under F1-A (F1-B
  would re-ask each run — its named cost). FR-10: READINESS count and FACTORY NOTES never contradict (item 5).
- C — FR-11 / FR-39: the tools the charter tells the doctor to use (Write) are in its tool set (item 1, F2). FR-12: no phrase-list
  detector is added (C2 judged by evals). FR-56: Write is named by phase steps and limited to two targets.
- D — FR-59: an unknown stays not-ok in the count (item 5). FR-40: the "block missing" state has a way out (item 4).
- E — FR-19: every FACTORY NOTES line names `owner: factory` implicitly by its block; failures name the owner. FR-37: the paths named
  (`doctor-guard-probe-<session>.txt`, `state/words/`) are unchanged and are the paths written. FR-41: no unknown printed as a fact.
- F — not touched (no measurement code); FR-55 friction: the moved permission block costs a Read only when asked.
- G — FR-30/FR-29: English, no control bytes (`--lang`). FR-33: live proof row (§4). FR-47: no code replaces the role's judgment.

## 6. Siblings by the map (rule 9; enumerated)

- Same artifact (sweep-the-artifact-first), `SKILL.md` printing sections: "Steps are printed by remedy.owner" — applied (kept, now
  complemented by FACTORY NOTES); "A step needing something the person does not hold" — applied (consistent with item 3); "What is
  legitimately not_configured" — not applicable (stays in the first part, anchor "no third bucket" kept); "An unreachable host" —
  not applicable (person's VPN step stays main, eval 6); "Next action is drawn only from..." — applied (unchanged). Verdict row 8 —
  noticed analog, NOT changed: it makes a factory-owned audit line (eval 10, A23) the person's next action, against row 5a's
  principle; queued for the Lead as a finding.
- `phases/repair.md`: guard section applied (item 2); recover/release reports — not applicable (they answer the person's own
  confirmation); `phases/archive.md` — not applicable (its questions are decisions; not read for this draft beyond its name).
- Axis 5, row "Conductor's own investigation before a question" (`docs/SIBLING_MAP.md:155`): the same rule lives in
  `skills/qa-onboarding/SKILL.md` :41/:88 and `skills/qa-story/SKILL.md` :72 — queued (Lead: one finding "person-facing text names a
  factory script / narrates internals" for onboarding and qa-story, as both findings ask).
- Axis 5, row "Gate A card <-> gate B card for a stand gap" (`:137`): "gate A still prints the script line (owner's rule: no script
  shown to a person)" — same class, already queued there (t-342 analog 1).
- Axis 10 (`:256`): the pre-onboarding writers' root (`install_smoke --report`, `factory_dashboard`) — node OH3-37; this spec does not
  touch it (F5).
- Axis 32 (judgment): no census change (§1). Axis 34 (one road): no exclusion (§1).
- Remaining axes 1-4, 6-9, 11-31, 33, 35, 36: not applicable — no script, reader, ratchet, journal, dispatch or story-side code is
  changed; axis 18 not touched (the 19000 cap is a fixed cap, not a ratchet row).

## 7. Forks (returned, not decided)

- **F1 — after onboarding, who puts the missing `.gitignore` block back?**
  (A) the doctor runs `project_gitignore.py --write` itself, then `--check`, and tells the person to commit `.gitignore`;
  (B) a closed question ("put the factory's block back into .gitignore?" with priced options), `--write` only on yes;
  (C) name `/qa-factory:qa-onboarding` as the remedy.
  Recommendation: **A** — it is the factory's own block, onboarding writes it with no question on the same road
  (`p4-generate.md:624`), the write is idempotent and moves no project line (P22, P31, FR-3). Cost of A: a project that removed the
  block on purpose gets it back on every doctor run (no record of a "no"). Cost of B: one human turn, and no recorder of a "no" exists,
  so the same question returns every run (FR-7) unless a record is added (a new writer — out of this spec). C sends the person through
  a whole interview for one line.
- **F2 — `Write` in the doctor's `allowed-tools`.** (A) add it, limited by text to the two targets `repair.md` already names;
  (B) keep the tool set and print a factory note when the write family is unverified (the doctor then cannot settle it, and
  `repair.md`'s words-file step stays undoable); (C) change `host_probe` so a shell-made file counts as the write family (a code change
  to the probe's meaning — out of this stream). Recommendation: **A** (FR-11, FR-39: the charter already tells it to Write). Cost:
  target limits rest on discipline; detector: eval 11 `repairs-by-code` and eval 14.
- **F3 — the form of the "collapsed tail".** (A) a last in-chat block `FACTORY NOTES (nothing for you to do)` after `Next action`;
  (B) a file `qa-factory/state/doctor-notes-latest.md` named in one line (the `driver-question-details.md` precedent of
  `human-questions.md:158`); (C) drop factory rows from the output entirely. Recommendation: **A** — no new writer or artifact
  (AR-14), the fact stays visible to whoever debugs; a terminal has no real collapse. C breaks "never report a green it cannot back".
- **F4 — should the doctor tell the person to commit `qa-factory/records/` after onboarding** (finding OH3-12, "what to do" p. 2)?
  (A) no line: the working tree is not the doctor's subject; the advice belongs to onboarding's closing report (sibling, queued);
  (B) one main-part line when `records/` is untracked. Recommendation: **A** — B reintroduces working-tree narration (the very
  symptom) and needs a git-status read the doctor does not make today.
- **F5 — the root of OH3-7 (the doctor's own receipts land in the project tree before onboarding).** (A) leave it to OH3-37
  (`install_smoke.py`, `factory_dashboard.py` are its owns; batch 1 :34); (B) this node also drops `--report` from step 1 when no
  config exists (loses the reuse window and the receipt that survives a lost shell handle, `SKILL.md:53-63`). Recommendation: **A**;
  this spec removes only the demand placed on the person.

## 8. Small choices closed by the designer (no design weight; reversible)

- Byte room comes mainly from moving section 7b to `phases/permissions.md` (read only when asked, the `archive.md` pattern), plus three
  trims that remove no rule (item 7). Further cuts are the Lead's call, not the builder's.
- No change to `scripts/project_gitignore.py` (its docstring already assigns the onboarding check to the caller); OH3-7's row lists the
  file as writable, the spec does not need it.
- `repair.md` recover/release result lines stay in the main part (they answer the person's own confirmation).
- The extra shell call for the bash family is step 2's existing `git rev-parse --show-toplevel` (no new command).
- OH3-7's "before" world reuses the predicate of steps 2/7 ("in the current directory"), keeping `test_story_run_monorepo.py` T6.
- The eval rows extend id 1 (before world) instead of adding a third new row: one behaviour, one row.
- Changelog fragment named for batch 1 (two of three nodes); the Lead renames it if OH3-7 is recorded under batch 2.

## 9. Reading trail

Read whole: `skills/qa-doctor/SKILL.md`; `skills/qa-doctor/evals/evals.json`; `skills/qa-doctor/phases/repair.md`;
`scripts/project_gitignore.py`; `references/human-questions.md`; the three findings
(`20261022-doctor-daet-cheloveku-komandy-skriptov.md`, `20261022-doktor-rasskazyvaet-cheloveku-o-svoej-kuhne.md`,
`20261022-doctor-do-onbordinga-trebuet-gitignore.md`); `plans/piles/onboarding-forge/batch-1-onboarding-roles-forge.md`.
Read in part: `batch-2-onboarding-roles-forge-p3.md:1-40` (OH3-7 row :32); `scripts/install_smoke.py:480-589`;
`scripts/host_probe.py:425-484`; `scripts/readiness.py:640-660, 995-1009, 1095-1124`; `scripts/selftest.py:330-400`;
`scripts/content_size.py` (`content_bytes`); `scripts/role_permissions.py:1-40`; `scripts/tests/scenario_walk.py:833-932`;
`scripts/tests/test-layers.json` (keep starts :35, quarantine :6966; `test_story_run_monorepo.py` :5780-5813 covers SKILL.md;
`test_host_probe_shapes.py` :8332, `test_project_gitignore.py` :9027, `test_session_identity.py` :9648 quarantined;
`test_vcs_evidence.py` :6387 keep); `test_host_probe_shapes.py:1055-1072`; `test_story_run_monorepo.py:380-404`;
`test_session_identity.py:612-626`; `test_vcs_evidence.py:600-620`; `references/role-load.json:1-30` (agents only, not skills);
`design/architecture.md:96-265`; `skills/qa-onboarding/phases/p4-generate.md:610-634`; `docs/SIBLING_MAP.md` headings, axis 5
(:111-158), axis 10 (:248-266), axes 32-34 (:557-593); `plans/builder-rules.md` 7/7b/7a; `changelog.d/README.md:3-36`.
Greps (each with a hit, so no negative claim rests on them): `guard_parse|check_guard_parse|one ordinary shell call` (package, not
tests); `project_gitignore` in package `*.md` (SKILL.md:175, p4-generate.md:624, CHANGELOG); `qa-doctor` in `scripts/` and tests;
`role-rules.json` rows for `qa-doctor` (5 anchors); `allowed-tools` in scripts (only `test_collect_skill.py`); `README.md` of the
skill (`:25`, `:62`); `The human writes that file|Bash\(git status|permission block` (only SKILL.md — no test pins section 7b);
`'owner': 'user'` (single quotes) in readiness.py returned 0 — re-run with `["']...["']` found 12, so the first was a quoting miss,
not an absence; `steps.*\w+\.py` in readiness.py (:654, :1005, :1113). Line-length histogram greps for the byte estimate (§0.5).
Not read: `factory-rules.md` full text (FR one-liners taken from the auto-loaded generated index `docs/FACTORY_RULES_INDEX.md`);
`phases/archive.md`; `skills/qa-onboarding/SKILL.md`, `skills/qa-story/SKILL.md` (sibling lines cited from SIBLING_MAP :155 only).
Needed beyond the manifest: `phases/repair.md`, `README.md` of the skill, `install_smoke.py`, `host_probe.py`, `readiness.py`,
`selftest.py`, `scenario_walk.py`, `test-layers.json`, the four pinning tests, `role-rules.json`, `batch-2` file, `p4-generate.md`.

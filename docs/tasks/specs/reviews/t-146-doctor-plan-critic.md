# t-146 — critic on plan: stream "doctor" spec t-144 (OH3-6, OH3-12, OH3-7)

Reviewer: critic (Opus), 12.11.2026. Subject: `docs/tasks/specs/t-144-doctor-oh3-6-12-7.md` (items 0-9, forks F1-F5).
The verdict is an input to the Lead's acceptance. The decision stays with the Lead.

**Verdict line: ACCEPT WITH FIXES (9 fixes, 0 blocking).** The design is sound: the forks are judged below, and every
item has a file, a behaviour and a test. The fixes are spec corrections the Lead can make before the dispatch. Fix 2 is
a queue action the Lead owes, not a builder item.

## Mechanical layer (control reruns)

- `python -B -c` byte count of `skills/qa-doctor/SKILL.md`: **18,995 B raw = 18,995 B after CRLF->LF**. The file has no
  CRLF, so the raw-byte pins in `test_host_probe_shapes.py:1064` and `test_session_identity.py:624` (both quarantined)
  see the same number.
- `selftest.py --limits` (cwd = package): `PASS limits: SKILL.md / agents / references within size caps`, `PASS limits:
  every mandatory role rule of design/role-rules.json holds in its carrier`, `2/2 ok`.
- `scenario_walk.py --witness-for <the five owns>`: SKILL.md -> `keep test_story_run_monorepo.py (layer detector, covers
  it)`. evals.json, repair.md, permissions.md and README.md -> `no scenario or keep row covers ...` (5 scenario files
  listed). This matches the spec's DoD reading under builder-rules 7b ("a report line").
- Live-stream collision check: `git diff --name-only $(merge-base main B) B | grep -E "qa-doctor|project_gitignore|
  install_smoke|changelog.d/onboarding-forge-1"` for wip/of-handoff, of-hooklib, of-hot, of-misc, of-small, of-tests and
  pile/onboarding-hooks/batch-4 returned empty. Positive control: the same command on wip/of-hooklib lists
  `cost_capture.py`, `factory_dashboard.py` and others.

## Answers to the DoD questions

### Q1. Each item names file/section, behaviour and test

| item | file/section | behaviour | test that fails without it | verdict |
|---|---|---|---|---|
| 0 | SKILL.md (measure) | before-bytes recorded | report line | ok |
| 1 | frontmatter | `Write` added | key `  - Write` + eval 14 | ok |
| 2 | SKILL.md:102, repair.md last section | doctor makes the call; reason never relayed | eval 14 (3 assertions) + keys | ok |
| 3 | "Rules of printing" bullet 1 | no script/flag/plugin path to a person | eval 14 + evals 6/8/12 unchanged | ok |
| 4 | step 3 sentence (SKILL.md:178) | gated on config; doctor writes the block | eval 1 variant + eval 14 + key | ok, see fix 5 |
| 5 | printing bullet 2, report format | FACTORY NOTES last; READINESS not green | eval 15 + evals 9/13 updated + keys | ok, see fix 4 |
| 6 | writes sentence, never-list, README | carriers true | keys + eval 4 | incomplete, see fix 3 |
| 7 | cuts | net <= 0 | `--limits` + before/after | ok, see Q2 |
| 8 | evals.json | rows 1,3,4,9,13 edited; 14,15 new | parse/ids/names key script | ok |
| 9 | changelog fragment | one bullet per change | `--lang` | ok |

Every item has a test in the DoD's accepted form (eval row or key). The gap: CI does not run evals, and the key script
is not committed. OF1-4 (batch 1 :70) and OH1-9 edit the same SKILL.md after this node and could undo the step-3 gate
or the no-script rule without any committed check going red. The package already has a cheap CI-run guard for
skill text: `design/role-rules.json` anchors, checked by `selftest --limits`. See fix 7.

### Q2. Byte budget (measured)

**Measured 18,995 B. Cap 19,000 B (`selftest.py:341`). Headroom 5 B.** The spec says "≈ 18,750 B ± 250, headroom
≈ 0–500 B". The measurement sits at the edge of that band, and the real headroom is 5 B, not 0–500. So "net <= 0" is
not just a design target. It is close to a hard requirement: `after <= 19000` means net <= +5.

I computed the bytes from the spec's own replacement strings against the file (`python -B` over SKILL.md, scratch
calculation):
- Additions of items 1-6: allowed-tools 10, step 1b +54, step 3 +145, printing bullet 1 221, bullet 2 197, READINESS
  +31, FACTORY NOTES format lines 117, exempt sentence +20, writes sentence +66, never-list repair clause +39.
  **Total ≈ 900 B** (spec estimate 810).
- Cuts: (a) 7b block 717 B replaced by 143 B, saving **574**; (b) anecdote :310-313, **249**; (c) never-list first
  bullet, **152**; (d) VPN parenthetical, **59**. **Total ≈ 1,034 B** (spec estimate ≈ 1,000).
- **Net ≈ −134 B: feasible.** Fixes 3 and 4 add about 40–70 B. Fix 5 removes about 16 B. The margin stays roughly
  −80 B.

The two follow-up nodes OF1-4 and OH1-9 will start with about 80 B of room. Recommendation for the Lead, not
blocking: approve now the next candidates the spec names (Codex code-mode paragraph :56-60 = 355 B; the stray
`# Evidence capability checks` H1 :332-335 = 174 B, which carries a rule, so relocate it into step 2 rather than delete
it). Otherwise the next node will stall on bytes.

Readability of moving 7b to `phases/permissions.md`: fine. The trigger sentence ("When asked why every command needs a
confirmation") stays in SKILL.md and the payload is read on demand. This is the existing `phases/archive.md` pattern,
so an ordinary run makes no extra Read (FR-55). No test or role-rules anchor pins 7b: I grepped the package without
CHANGELOG, case-insensitive, for `human writes that file|permission block|git status:\*`, and the only hits were
SKILL.md itself. The `audit_factory` rule "a referenced phases/*.md exists" holds because the file is created in the
same commit.

### Q3. Owns vs live streams

The owns are the five files under `skills/qa-doctor/` plus one new `changelog.d/` fragment. They do not overlap
hooklib, hot, handoff or OF3-1 phase 1 (lists checked; branch diffs above are empty). `p4-generate.md` (OF3-1) and
`project_gitignore.py`, `install_smoke.py`, `host_probe.py` and `readiness.py` are only cited read-only. Note for
ordering: OF1-4 (batch 1 :70) depends on OH3-6 for SKILL.md, so it is sequential by row and not a collision.

### Q4. Edges

- Before onboarding (no config in cwd): step 3's gitignore command is not run. The predicate is the same as steps
  2/7 and row 3 ("exists in the current directory"), so `test_story_run_monorepo.py` T6 is kept. **Correct.**
- After onboarding, block whole: silent. Missing: `--write`. **Correct.** Fix 5 removes a redundant re-check that
  collides with an existing rule.
- Nested project (config only in a parent folder): treated as not onboarded. Consistent.
- No `.gitignore` at all: `write_block` creates it (`project_gitignore.py:106-127`). Covered by the edges table.
- FACTORY NOTES empty: header omitted. Covered.
- **Missing edge:** user-owned and factory-owned non-ok rows both present. The READINESS alternatives
  "your help is needed | the rest in FACTORY NOTES" do not say which one wins. See fix 4.
- **Wrong edge:** "the Write is refused by the guard -> `--check` reports `guard_defect`". See fix 6.
- **OH3-7 root (before world, receipts in `state/`):** unowned once F5-A points at a stream that excludes it. See fix 2.

### Q5. AR-n and the FR walk

- AR-14 kept. The doctor calls the same CLI, and the one writer is `project_gitignore.write_block`, which
  `onboard_apply.py:1460` (`G.write_block(root)`) and `p4-generate.md` also go through.
- AR-11 kept. `Write` is named by phase steps (`repair.md:39,57-58`). The sibling skills qa-story, qa-onboarding and
  qa-collect hold Write. No audit covers skill `allowed-tools`: I grepped role_permissions/audit_factory/selftest/
  role_load for `allowed-tools|skills/` and found none on this axis.
- AR-16 is kept **only after fix 4**. The FACTORY NOTES format line `<capability>  <status>  <the fact>` prints field
  names in a block the person reads. That breaks `references/human-questions.md:44` ("may never carry a form or schema
  field name"), which the spec itself names as AR-16's keeper. Item 2 already says "in plain words".
- FR walk: A, C, D, E, F and G are true as written. B (FR-6) holds only with fix 4.
- F1 wording "moves no project line" is slightly false: `write_block` takes every line equal to one of ours out of its
  place and puts the block at the end (`project_gitignore.py:116-124`). This is onboarding's own accepted behaviour,
  so it is not a defect of the plan. Reword it ("moves only lines that are ours").

## Forks — coordinator's provisional decisions judged

- **F1 = A (doctor writes the block after onboarding): RIGHT.** FR-3: the factory's own block is not put to a person
  as a choice. P22/FR-48: settle before asking. Onboarding writes the same block with no question on the same road
  (AR-14, P31). The write is idempotent (`write_block` returns early on `_is_whole`). F1-B would re-ask on every run
  with no recorder of a "no" (FR-7). The named cost (a block removed on purpose comes back) is acceptable and correctly
  stated.
- **F2 = add Write: RIGHT, and no narrower tool exists.** The guard-parse write family is keyed on the host's tool name
  (`host_probe.py:334-336`, `GUARD_FAMILIES`: Write/Edit/NotebookEdit/apply_patch). A Bash or script call produces only
  bash-family evidence, so no script can certify the write family (the test `test_claude_host_probe.py:473-484` uses a
  real `Write` event). The release words file must also be written with a file tool because a command line cuts
  multi-line text (`repair.md:38-40`). Write is the least privilege that does the job. Do not add Edit.
  On the spec's §0.3 causal claim: in Claude Code a skill's `allowed-tools` pre-approves tools rather than removing
  others (estimate, not verified here). The direct carrier of OH3-6 symptom 1 is `repair.md:62`: "`unverified` →
  `owner: factory`, its `reason` verbatim". That line told the doctor to print "Make one ordinary call ... re-run
  --check" to the person. Item 2 rewrites that line, so the outcome is right. F2's justification should rest on
  FR-11/FR-39 and the tool-name keying above, not on "cannot".
- **F3 = in-chat FACTORY NOTES block: RIGHT.** It needs no new writer or artifact (AR-14), and the fact stays visible
  to whoever debugs (AR-28). F3-C (drop the rows) would contradict "never report a green it cannot back". Condition:
  fix 4 (plain words, mixed precedence).
- **F4 = no "commit records/" line: RIGHT.** It would reintroduce working-tree narration, the very symptom of OH3-12,
  and needs a git-status read the doctor does not make. The advice belongs to onboarding's closing report. The Lead
  must actually write that sibling finding into a carrier (rule 9, "queued" means written). §6 currently says "queued
  (Lead: ...)", which is an instruction, not a carrier.
- **F5 = leave the root to OH3-37: WRONG as stated.** The OH3-37 stream (hooklib, wip/of-hooklib) does not touch
  `install_smoke.py`. Verdict t-141 F5 (`docs/tasks/specs/reviews/t-141-of1-hooklib-critic.md:75-82`) explicitly asks
  for a disposition or a node id. Pointing at OH3-37 therefore leaves `install_smoke --report` before onboarding with
  no owner, an axis-10 member left neither fixed nor queued. **Is OH3-7 complete?** Its row's "what" (the doctor
  DEMANDS the block before onboarding, FR-5) is fully closed by item 4. The finding's alternative (2), the root, is the
  axis-10 class, not this node. So OH3-7 needs no extra builder item in this stream, provided the root gets its own
  node: fix 2. Do not take F5-B. It drops the reuse window and the receipt that survives a lost shell handle
  (SKILL.md:53-63), and it touches a code file outside this stream's owns.

## Fixes (numbered, pointing at spec items)

1. **§0.5 and item 0/7, byte facts.** Replace the estimate with the measurement: 18,995 B, headroom 5 B (carrier: the
   `python -B` byte count above and `selftest.py --limits` PASS). State that `after <= 19000` already forces
   net <= +5. Keep "net <= 0". Optionally pre-approve the two next candidates (355 B and 174 B, relocated) so the
   builder's stop rule does not trigger a round trip.
2. **F5 / §6 axis 10 (Lead queue action, not a builder item).** Give `install_smoke --report` under a root with no
   config a node id and an owner, as t-141 F5 asks (for example, the remaining part of OH3-37 as a new node in
   onboarding-forge, owning `scripts/install_smoke.py` and its test). F5 must name that node. Record in the OH3-7 row's
   disposition that the node closes on the demand (item 4) and the root lives in the named node. Update the
   SIBLING_MAP axis 10 row in the same move (t-141 F5).
3. **Item 6, never-list and README.**
   - The never-list bullet `SKILL.md:326-327` ("Never writes a config, a strategy file or anything under `artifacts/`")
     contradicts item 1's permitted Write target `qa-factory/artifacts/<TICKET>/state/words/<name>.txt`. The
     contradiction predates this spec (it already clashed with `repair.md:39`), but the tool grant now makes it live.
     Amend the bullet, for example "... anything under `artifacts/` except `repair.md`'s words file". Keep the byte cost
     inside the margin.
   - Item 6 names README :25 and :62. **README :61** ("Does not modify any file other than
     `qa-factory/state/factory-dashboard.html`") is the same stale class and must also change.
4. **Item 5, FACTORY NOTES form and READINESS precedence.**
   - (a) Change the format line from `<capability>  <status>  <the fact, one line>` to plain words, for example
     `<what, in plain words>: <the fact, one line>`. This applies `human-questions.md:44` (no field names), which the
     spec cites for AR-16, and matches item 2's "in plain words" and eval 15's example.
   - (b) State the mixed case: when any non-ok row has `remedy.owner: user`, READINESS reads "<k> of <n>, your help is
     needed", and FACTORY NOTES is still printed last for the factory-owned rows. Only when every non-ok row is
     factory-owned does it read "the rest in FACTORY NOTES". Add one edges-table row.
5. **Item 4, drop the post-write `--check`.**
   - "run it with `--write` yourself, then `--check`" collides with `SKILL.md:180` "Never re-run a detector yourself".
   - The re-check is also redundant: `write_block` produces a whole block by construction. It removes every line of
     ours, appends HEADER plus the block at the end (`project_gitignore.py:116-127`), and `_is_whole` is then true.
     A `--check` after exit 0 can never list lines.
   - Replace with "Lines listed: run it with `--write` yourself and tell the person to commit `.gitignore`; a non-zero
     exit is one FACTORY NOTES line."
   - Delete "still listing lines" from the item 4 edges, the §3 row, eval 14 `gitignore-block-written-by-the-doctor`
     ("then `--check`") and the doc-key list. This also saves about 16 B.
6. **§3 edge "the Write is refused by the guard".** The row says `--check` reports `guard_defect`. Wrong:
   `guard_defect` comes only from the PT-unparsed-event/PT-patch-unchecked counter (`host_probe.py:482-494`). A policy
   refusal records `exit_code: 2` with no `parsed_at` (`:420-422`) and yields `unverified` (`:461-467`). The behaviour
   ends the same way (one FACTORY NOTES line, stop, no retry), but the row must say `unverified`, so that neither the
   builder nor the eval grader expects a `guard_defect` that will not appear.
7. **Item 8 / DoD, a CI-run guard for the two load-bearing rules.**
   - Add two `design/role-rules.json` rows (checked in CI by `selftest --limits`): one anchored on "Run the third only
     when" (doctor step-3 gate, OH3-7), one on "never a factory script, flag or plugin path" (OH3-6 class). This needs
     `design/role-rules.json` in owns.
   - Reason: the evals are not run by CI and the key script is not committed. The next two nodes editing SKILL.md
     (OF1-4, OH1-9) could revert either rule with nothing going red.
   - If the Lead declines, record why in the spec (Q1 is then met only by eval rows).
8. **§0.3 / F2 wording.** Reword the causal claim ("cannot do the Write") to "the charter tells it to Write without
   granting the tool (FR-39), and `repair.md:62` told it to relay the `reason` verbatim". The second is the direct
   carrier of symptom 1, and item 2 removes it.
9. **§6 sweep-the-artifact.** `repair.md:42-45` (a guard refusal repeating on a different call -> "report it
   `owner: factory` with the host version and stop") is a factory-owned fact. It is not an answer to the person's
   confirmation, yet §6 folds it into "recover/release reports — not applicable". The same applies to
   `SKILL.md:330-331` ("Never debugs the factory ... one line `unknown / owner: factory`"). Route both to FACTORY NOTES
   in a clause of items 2/5, or give each a per-neighbour "not applicable — why".

## Standing questions (critic-diff-brief items 6, 7, 12)

- **DUPLICATION AND CONSISTENCY:** no duplicate mechanism. The `.gitignore` write reuses `project_gitignore.py`, the
  one writer that `onboard_apply.py:1460` also calls. The "onboarded?" predicate is the same sentence form as steps
  2/7. Cut (c) removes a second list of the doctor's questions (it stays once, at :34-37), which reduces duplication.
  The inconsistencies found are fixes 3, 5 and 6. What I checked: grep of `gitignore` in onboard_apply.py, grep of
  `allowed-tools` across the package, grep of `qa-doctor/phases|phases/(archive|repair).md`.
- **CODE QUALITY:** n/a for scripts (no `scripts/*.py` change). For the skill text: the stray `# Evidence capability
  checks` H1 after the never-list (:332-335) is a structural defect of the carrier, which the spec noticed and left to
  the Lead (Q2 recommendation).
- **ONE ROAD (P31):** no exclusion of a language, project or case. The before/after-onboarding branch is the task's
  own condition with one shared predicate. The guard-probe write uses "the host's file tool" on every host
  (`apply_patch` on Codex counts by `GUARD_FAMILIES`). The block goes through the same CLI as onboarding. Nothing goes
  to the owner.

## Trail

Read in full: spec t-144; `skills/qa-doctor/SKILL.md`; `phases/repair.md`; `scripts/project_gitignore.py`; finding
`20261022-doctor-do-onbordinga-trebuet-gitignore.md`. Read in part: `host_probe.py:325-494`;
`test_claude_host_probe.py:460-537`; `test_host_probe_shapes.py:1050-1072`; `test_vcs_evidence.py:600-620`;
`test_story_run_monorepo.py:391-397`; `test_session_identity.py:622-625`; `design/role-rules.json` doctor rows (260,
261, 432, 433, 473); `references/human-questions.md:42-54`; `plans/builder-rules.md` 7/7b; batch-1 rows OH3-6 (:29),
OH3-12 (:31), OH3-37 (:34), OF1-4 (:70); batch-2 OH3-7 (:32); t-141 critic F5 (:75-82); skill README :20-30, :58-64;
evals.json (all ids and assertion names; prompts and expected outputs of 1, 4, 10); `onboard_apply.py` gitignore
grep; `tools/critic_verdict.schema.json`.
Not read: the two other findings in full (their content is covered by the node rows and the spec's quotes);
`factory-rules.md` full text (the FR index is auto-loaded); `p4-generate.md` (cited read-only by the spec).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "1 (spec 0.5, items 0/7): replace the byte estimate with the measurement: SKILL.md 18995 B, cap 19000, headroom 5 B; net <= 0 is effectively mandatory; computed net of items 1-7 is about -134 B (adds about 900, cuts about 1034), feasible; optionally pre-approve the Codex paragraph (355 B) and relocating the stray Evidence H1 (174 B)",
    "2 (F5, axis 10; Lead queue action): OH3-37 stream excludes install_smoke.py (t-141 F5), so F5-A orphans install_smoke --report before onboarding; give it a node id and owner, name it in F5, update SIBLING_MAP axis 10; OH3-7 closes on item 4 (the demand)",
    "3 (item 6): amend the never-list bullet SKILL.md:326-327 'anything under artifacts/' which contradicts the permitted Write of artifacts/<TICKET>/state/words/ (item 1, repair.md:39); also README.md:61 'Does not modify any file other than factory-dashboard.html'",
    "4 (item 5): FACTORY NOTES format line in plain words, not '<capability> <status>' (human-questions.md:44, AR-16, FR-6); state READINESS precedence when user-owned and factory-owned non-ok rows coexist ('your help is needed' wins, notes still printed)",
    "5 (item 4): drop the post-write --check: it collides with SKILL.md:180 'Never re-run a detector yourself' and is redundant (write_block yields a whole block by construction, project_gitignore.py:116-127); remove the 'still listing' edge and the eval 14 and key references to it",
    "6 (section 3 edges): a guard refusal of the doctor's Write yields unverified, not guard_defect (host_probe.py:420-422, 461-467, 482-494); correct the row",
    "7 (item 8 / DoD): add design/role-rules.json anchors for 'Run the third only when' and 'never a factory script, flag or plugin path' so CI (selftest --limits) guards the two rules against the following SKILL.md nodes OF1-4/OH1-9; or record why not",
    "8 (section 0.3 / F2): reword the causal claim: repair.md:62 'its reason verbatim' is the direct carrier of symptom 1; F2-A rests on FR-11/FR-39 and GUARD_FAMILIES keying on tool name (no script can certify the write family)",
    "9 (section 6 sweep): repair.md:42-45 (repeating guard refusal, owner factory) and SKILL.md:330-331 (unknown / owner factory line) are factory-owned facts; route them to FACTORY NOTES or give a per-neighbour not-applicable reason"
  ],
  "class_completeness": "Same-artifact sweep mostly done; two neighbours missed (repair.md:42-45, SKILL.md:330-331; fix 9) and two stale carriers missed (SKILL.md:326-327 artifacts bullet, README:61; fix 3). Map: axis 5 sibling skills (onboarding, qa-story) queued by instruction only, so the Lead must write the finding into a carrier; axis 10 install_smoke --report is orphaned by F5-A because OH3-37 stream excludes install_smoke.py (fix 2). Axes 32/34: no census change, no exclusion.",
  "trail": {
    "read": [
      "docs/tasks/specs/t-144-doctor-oh3-6-12-7.md",
      "ai-packages/qa-factory/skills/qa-doctor/SKILL.md",
      "ai-packages/qa-factory/skills/qa-doctor/phases/repair.md",
      "ai-packages/qa-factory/skills/qa-doctor/README.md (20-30, 58-64)",
      "ai-packages/qa-factory/skills/qa-doctor/evals/evals.json (ids, names, ids 1/4/10 text)",
      "ai-packages/qa-factory/scripts/project_gitignore.py",
      "ai-packages/qa-factory/scripts/host_probe.py (325-494)",
      "ai-packages/qa-factory/scripts/tests/test_claude_host_probe.py (460-537)",
      "ai-packages/qa-factory/scripts/tests/test_host_probe_shapes.py (1050-1072)",
      "ai-packages/qa-factory/scripts/tests/test_vcs_evidence.py (600-620)",
      "ai-packages/qa-factory/design/role-rules.json (doctor rows)",
      "ai-packages/qa-factory/references/human-questions.md (42-54)",
      "plans/builder-rules.md (7, 7b)",
      "plans/piles/onboarding-forge/batch-1-onboarding-roles-forge.md (29, 31, 34, 70)",
      "plans/piles/onboarding-forge/batch-2-onboarding-roles-forge-p3.md (32)",
      "plans/piles/onboarding-forge/findings/20261022-doctor-do-onbordinga-trebuet-gitignore.md",
      "docs/tasks/specs/reviews/t-141-of1-hooklib-critic.md (75-82)"
    ],
    "reruns": [
      {"command": "python -B byte count of skills/qa-doctor/SKILL.md (raw and CRLF->LF)", "result": "18995 / 18995"},
      {"command": "python -B scripts/selftest.py --limits (cwd package)", "result": "PASS size caps; PASS role-rules anchors; 2/2 ok"},
      {"command": "python -B scripts/tests/scenario_walk.py --witness-for <five owns>", "result": "SKILL.md -> keep test_story_run_monorepo.py; other four -> no scenario or keep row covers (5 scenario files listed)"},
      {"command": "git diff --name-only merge-base..branch for 6 wip branches + pile/onboarding-hooks/batch-4, grep qa-doctor|project_gitignore|install_smoke", "result": "empty; positive control on wip/of-hooklib lists files"},
      {"command": "python -B byte arithmetic of spec replacement strings vs SKILL.md", "result": "adds about 900 B, cuts about 1034 B, net about -134 B"}
    ]
  }
}
```

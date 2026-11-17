# t-1212 — critic on the plan: universality, variety map, passage rule (spec t-1207, phase A)

Reviewed: `docs/tasks/specs/20261117-universality-variety-map-spec.md` (653 lines). Base: origin/main = HEAD = b5fca9bd. It moved
from dc23e384 during the review; `git diff --stat dc23e384 b5fca9bd` over the five touched files, SIBLING_MAP and the spec is empty.

**Verdict: NEEDS WORK — accept with fixes.** No blocking finding. The direction holds: one owner (architecture.md § A), A for F1,
F2-F4 left open, all 38 axes enumerated, and every anchor real and unique. Thirteen fix-round findings need edits to the spec text
before the U4 dispatch. Two of them (R1, R2) are meaning-level. They touch the invariant text the builder copies verbatim, so the
Lead should check their wording before the dispatch. No second critic pass is needed unless the fixes change the architecture
(PROJECT.md new-idea step 6). Accepting the work and deciding F6 and K7 stay with the Lead (rule 6).

## Findings

Ranks: **fix-round** (edit before the U4 dispatch) and **note** (optional or cosmetic).

**R1 (fix-round, meaning). The passage clause says "never blocks" but does not reconcile it with refusals that carry a door, with
AR-28 or with P22.** Spec §3.1, line 143 (AR-2 Invariant); map taxonomy at line 94.
- FR-59 lists "refuse with a door" as a declared safe default (factory-rules.md:289-297).
- AR-29 keeps shape and presence refusals (architecture.md:135-140). FR-57 and P15 require every ban to have a door.
- The map's outcome classes lump "(i) refuses or halts" together and then label cells "i with a door" (a3D2, ax8D4, ax11D2). A
  reader cannot tell whether those cells are breaches.
- The clause sends the move "to the owning role" only. P22 (OWNER_PRINCIPLES.md:80-82) and AR-17 send a state that code has no move
  for to the conductor. The current AR-2 itself says "the owning role or the conductor judges it". The clause lists P22 as a
  carrier but drops the conductor.
- "Never blocks" also needs AR-28's other half spelled out: the gate does not open either.

Fix: one sentence in the clause. "A refusal that names a door the receiver can take (FR-2, FR-57, AR-9, P15) is not a block. On an
unknown shape the gate never passes either (AR-28): the move goes to the owning role, or through the conductor's seam when no role
owns the state (AR-17, P22)." In the map legend, replace "(i) refuses or halts" with "(i) halts or refuses with no usable door".

**R2 (fix-round, meaning). The cost sentence gives P11 and AR-12 a meaning they do not have.** Spec §2, line 92. The definition
says "the defect is cost with no gain in quality (P11, AR-12)". P11 says "код, от которого стадия дороже, — дефект"
(OWNER_PRINCIPLES.md:30), and AR-12 says "code that makes a stage dearer is a defect" (architecture.md:127). Neither has an
exception for quality. Spec §1.1 (line 35) itself says AR-12 counts our code's friction, not role work. As written, a future diff
could cite the map to excuse code friction. Fix: "The extra turns of a role working an unknown shape as a free agent are not a
breach when they buy quality (the owner, 17.11.2026); code that makes a stage dearer stays a defect (P11, AR-12)."

**R3 (fix-round, K1). Q-i is closed by implication in the definition, and the axis 10 label leans on Q-ii.**
- Q-i: line 92 lists only "blocks" and "silent default" as breaches. A door that hands the role's work to a person is neither, so
  under the definition it is not a breach, which is option (a) of F2. AR-2 reserves this question explicitly (line 143); the
  definition does not. Fix: add the same Q-i sentence to the breach sentence of the definition.
- Q-ii: the axis 10 cell (line 107) labels English-only artifacts "ii by design". Under line 92, (ii) means silent default, which
  is a breach, so the status quo (F3 option (a)) reads as a breach. Fix: "(the digest's class ii; whether it is a breach is Q-ii)".
- F4/Q-iii is neutral. The ax12D1 cell carries no class; the digest gives "i".

**R4 (fix-round). E5 puts the walk where §2 says it does not go.** Spec §4.1 E5, line 204: "The variety walk of section A goes to
the same places". Step 2's places are "the spec, the report and the commit" (architecture.md:287). The walk text in §2 (lines
118-124) names three places: the Lead's plan, §1 of the spec, and the critic. It also says "a builder dispatch carries no walk".
A builder reading step 2 would write up to 13 axis lines into its report and the commit. Fix: "The variety walk of section A goes
into the spec's §1 (and the Lead's plan of a new idea); the report and the commit point at it."

**R5 (fix-round, K6, artifact sweep). The opener of critic.md rule 22 is left stale.** critic.md:192 reads "(Q4, Q6 and Q12 also on
a plan gate, rule 24)". Spec §4.3 (lines 235-237) adds Q10's VARIETY sentence to rule 24 but not to this opener, so the two lines
disagree. Fix: add one more old→new pair, plus a key in §7.1.

**R6 (fix-round, K5 axis 2). critic.md rule 10 (the exam) is not addressed.** The spec edits critic.md, and rule 10 of that file
requires the PROCESS/CRITIC_EXAM.md exam before the commit. That file is absent. Positive control: `ls PROCESS` lists
DEPLOYMENT_ECONOMY_EXAM.md and LEAD_RANKING_EXAM.md; PROCESS/README.md:22 says CRITIC_EXAM.md is generated at onboarding. Spec §5
axis 2 (line 330) answers "n/a — no exam discipline changes", which is wrong. The precedent is the worker-boot r2 spec (lines 532 and
562): `Deviation: exam not run; debt F3-1`. Fix: change axis 2 to "covered: critic.md edited with the deviation line" and put that
line into §6a item 5 as a commit line.

**R7 (fix-round). AR-2's Breakage field contradicts itself.** Spec §3.1, line 146. The field keeps the TP1-13877 record: "the
automator spent about 35 calls reading factory code, then halted". That is code halting a role on an unknown shape (the id form),
the exact breach the clause defines. It then says "Passage: none recorded in a live run". Fix: "Passage: the same record —
TP1-13877, an id form the contract did not know, halted the role."

**R8 (fix-round). AR-2's Detector points at a node the pointer target does not define.** Spec line 145 cites "node U6 of the
universality idea, `dev:docs/tasks/specs/20261117-universality-variety-map-spec.md`". U6 appears in the spec only as a bare name
(lines 145, 383). The DAG with U6 lives in the brief, and edge E5 forbids citing the brief. Fix: point at a carrier that defines U6
(a pile batch node, or a node table copied into the spec), or describe the detector without a node id.

**R9 (fix-round, K3). The map legend does not warn that t-1203 uses a different class scale.** In t-1203, r4 and r2 are
"rank-iii" (silent default; objects s5.report and s6.web are "silent-default"), and r5, r6, r7 are "rank-ii" (a door). The map uses
the t-1200/t-1201 scale, where (ii) is silent default and (iii) reports and leaves a move. The designer translated correctly (r4→ii,
r6→iii, r5→"i with a door"). But a walker who follows `r4` into the digest finds "iii" where the map says "ii". Fix: one clause in
the legend at line 94: "t-1203's rank-ii/iii are a door and a silent default; the map gives them in its own (i)-(iii) scale."

**R10 (fix-round, K5(c); the decision is the Lead's). F6=a leaves the walk without a detector that sees a skipped walk.** The critic
sees a walk only on diffs and plans that reach it. It misses a `critic: skipped` diff, a Lead-drafted package spec below the
designer threshold with no plan critic, and a critic that omits the VARIETY line. The spec names the first escape honestly (§3.3).
The closest sibling mechanism is axis 34 (designer rule 6 with critic Q12). It registered calibration check 42, which greps the
week's specs and requires a `ONE ROAD:` line in every verdict (WEEKLY_CALIBRATION_PROTOCOL.md:1117). The evidence favours F6 (b), at
about 300 bytes outside boot: check 42 gains a sub-item, "(f) package specs of the window carry `axis N:` or `variety:` lines;
critic verdicts on package plans and diffs carry a VARIETY line". It adds one owns path. Alternative: keep (a), and state in §5(c)
that the waived-diff and Lead-drafted-spec escapes have no detector.

**R11 (fix-round, K6). Axis 34 and critic Q12 overlap with the new question, and nothing says so.** Q12 asks whether a language,
project or case is left outside a shared mechanism. VARIETY asks what the code does on a value it does not know. Both can fire on
the same line of a diff, and the `narrows`→fork rule restates axis 34's symmetry. Spec §5 axis 34 (line 374) says "covered" without
an edit. Fix: in the critic sentence, say "an exclusion from a shared mechanism stays Q12; VARIETY asks the unknown-value
behaviour". Add the variety walk to the "The reviewers" row of SIBLING_MAP axis 34 (line 598). That adds one owns path, not a boot
file. Optional: add "the variety map and its walk form (§ A)" to the aspect cell of the `design/*.md` row of axis 31.

**R12 (fix-round, K8). The witness cannot catch a copy error in about 22 KB of verbatim text.** The 14 keys in §7.1 cover headings
and a few phrases. A typo in a cell id, a dropped cell clause, or a mangled Carriers or Change check line of AR-2 all pass. The spec
holds the exact text between markers, so an equality check costs nothing. Fix: the script reads the spec and compares the
whitespace-normalised block between `BEGIN INSERT` and `END INSERT` (lines 86-124) with the file between the section A heading and
`**AR-1 — `. It does the same for the five bullet lines of 3.1 against AR-2. Keep the negative control. Also add keys for E5, E6
and R5.

**R13 (fix-round, K7 — the Lead's question). Recommendation: short cells, with the inventory left in the frozen digests.** See K7.

Notes:
- **n1.** Reservations dropped from the digests: a1D3 ("used only when the table is unreadable"), a6D4 ("unless external_writes
  declares it"), ax7D3 (the iii half: the stand_access probe records not_recorded).
- **n2.** The cutoff is stated twice, with two different tests. The critic sentence (line 232) uses "a spec accepted before the map
  landed"; E8 (line 507) uses "primary draft starts after the merge". "(blocks when it stops a stage)" reads as attached to a
  missing walk too.
- **n3.** The `named_by` line anchors shift by about 40 lines (39 inserted lines plus a blank), not 30. They stay harmless: selftest
  only checks that `named_by` is non-empty (selftest.py:629-630).
- **n4.** The invocation suggested at line 285, `--names "AR-2,variety"`, is read as one name ("absent ... not named anywhere"). The
  working form is `--names AR-2 variety`.
- **n5.** §7 still carries Option B (owns, E9, the `--openers 30` key). Cut it to A before the dispatch. The owns worktree paths come
  from `dispatch_new.py`.
- **n6.** §5(a) says "The builder: nothing", but under F8 the builder edits a map cell whenever its diff changes how an axis is held.
- **n7.** §1.1, AR-3 row: the reasoning implies AR-3 key defaults must be reported in the run. The clause only covers values no key
  names, so a key's `absent_means` is out of its scope. Say so.
- **n8.** The definition text is the Architect's formulation, "утверждается вместе со спекой" (brief:44), and is not yet among the
  "Решено владельцем" items. The "declared in data" half of F7 is AR-1/AR-3/FR-59 reasoning, not the owner's word. Show the
  definition to the owner with F2-F4 and record the approval.

## Answers to the keys

**K1 — fit to the owner's words: holds, with R2, R3 and n8.** No blocking, cost allowed when it buys quality, "no worse than a free
agent on the same model", "with what the factory already has (answers, testing knowledge, the critic)", and "carries the stage to a
result" all trace to brief lines 16-30. "No silent default" comes from the Architect's definition (brief:54), not from the owner's
verbatim words (n8). F2 is closed by implication in the definition (R3). F3 is tilted by the axis 10 label (R3). F4 is open. Every
other inserted text (designer.md, critic.md, PROJECT.md, E2, E6) is neutral. Brief cited in none: checked by script over §2 and
§3.1, no hit.

**K2 — architecture and principles: R1 and R2.** AR-3 is consistent, because the scope is values no key names (n7). FR-59 and AR-29
need the refusal-with-door sentence (R1). AR-28 needs "never passes" (R1). P13 is kept. P22 and AR-17 are touched and not reconciled
(R1). AR-9 and P15 should be named as carriers (R1). P11 and AR-12 are misquoted (R2). AR-15 and AR-23 are not touched in substance.

**K3 — facts by trail: holds, with n1 and R9.** I sampled 27 cells over axes 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12 and 13. Ids
checked: a1D3, a2D1, a2D2, a2D4, a3D2+r5, a4D2, a5D2, a5D3, a6D1, a6D4, ax7D2, ax7D3, ax7D5, ax8D2, ax8D3, ax9D1, ax10C1, ax10D1,
ax10D2, ax11A1, ax11D2, ax12D1, ax13D1, ax13D3, r1/ob.detect, r2/s6.web, r3/s0.inproc, r4/s5.report, r11, s4.tool. Each cell says
what its object says. Three reservations are thinned (n1).

Positional claims:
- The index stops at the first `## ` that is not `## <Letter>. ` (architecture_index.py:72-84). The spec says "the first such
  line", which is imprecise, but edge E1 (no `## ` at all) is stricter and holds.
- `OPENER_RE = ^\*\*AR-(\d+)`; there are 29 openers.
- `block_from(arch_text, "**AR-17")` matches the first line *starting* with `**AR-17`. The spec's "anywhere" is conservative.
- `_PROSE_CARRIERS` includes design/architecture.md (selftest.py:673); `test_quarantine.PACKAGE_PROSE` includes it too (line 52).
- The insert carries no Cyrillic, no `## ` line, no `**AR-` line, and no test name apart from the existing `test_judgment_census.py`
  in AR-2 (checked by script).

**K4 — exact edits: holds, with R4 and R5.**
- Each anchor occurs exactly once: E1 `(P1-P23)` ×1, the E2 sentence ×1, step 2 ×1, step 9 ×1, designer.md:32, critic.md:251,
  critic.md:281.
- install_parity anchors are untouched (critic and designer line starts only).
- No code pins the old wording (case-sensitive Grep over tools, scripts, hooks, PROCESS and skills). The one hit is the unrelated
  `P1-P23` rows of test_dispatch_gate.py:2745, which shows the same Grep call works.
- One commit (E8): yes.
- Bytes measured: the PROJECT.md insert is 94 B and the CLAUDE.md delta is 21 B, exactly as the spec says, plus a rewrap each.
- Boot now: `BOOT BUDGET: 112646 bytes / 120000 ... WARN`, so about 112,769 after the change: inside BREACH, already over WARN
  110000, and CLAUDE.md 51953/58500.
- The index is 2682 B. Under A it does not change (`--check` up to date, 29 invariants).

**K5 — four questions.**
- (a) Holds apart from n6.
- (b) All 38 axes are enumerated; axis 2 is wrong (R6) and axis 34 is under-answered (R11).
- (c) The critic as named detector is honest about the waived-diff escape, but it misses Lead-drafted specs and a critic who omits
  the line (R10).
- (d) What stops a skip is honest. The architecture.md step 2 sentence also binds Lead-drafted specs, once R4 fixes where it sends
  the walk.

**K6 — class-wide completeness.**
- FR-13 and FR-47 agree (the clause is their stronger form).
- P2 agrees (data rows are not code). The owner's text is not edited.
- designer.md rule 6 agrees.
- critic.md: the rule 22 opener disagrees (R5); Q12 overlaps (R11).
- builder.md and TESTING.md: none found. Case-insensitive search for `universal|variety|универсальн` over the role files,
  TESTING.md, CLAUDE.md, PROJECT.md, SIBLING_MAP and factory-rules.md; positive control FR-13:189 hit.
- The generated indexes do not change under A.
- AGENTS.md takes only frontmatter from role files (agents_md.py:183), so only the CLAUDE.md and PROJECT.md edits regenerate it.

Readers (my run of `owns_readers.py`, which the spec's hand grep replaced):

| line | answer |
|---|---|
| names AR-2 (surfaces.json, request-call-patterns.json, test-layers.json) | unchanged: the AR-2 id and title stay byte-identical (A) |
| names variety (about 67 data/code hits) | miss 7, a common word: nothing owed |
| more (five files) | interface kept: prose appends only; no anchor line start and no pinned phrase changes |
| miss 1 | `--witness-for design/architecture.md` → test_conductor_investigates_first.py and test_selftest_slow_tests.py (a fixture tuple only) |
| miss 3 | "four questions" → "five" is pinned nowhere (Grep, 0 hits; control above) |
| miss 6 | base b5fca9bd is origin/main: yes |

**K7 — feasibility and weight. Recommendation: short cells (R13).**
- Measured: the insert is 19,269 B. Cells run 849-1,960 B (axis 3 is the largest), with 570-1,501 B in "Held by". architecture.md
  grows from 46,930 B to about 69 KB (+41%).
- Section A is read on every package change and walked by every package spec and critic, at about 5K tokens per read.
- Long form, cost:
  - Every F8 upkeep edit has to touch an id-laden inventory whose evidence is frozen 17.11 digests citing line numbers. New rows
    carry no scout id, so cells drift into mixed and stale evidence: the `dsg.lag` failure that F8 itself cites.
  - The `code:` lists are U7's work list, not walking aids.
- Long form, gain: a walker sees the breach list in place.
- Short form: axis, examples, holders in a few words each, the worst unknown-value class, proven-on, and a pointer
  (`inventory: t-1200 a1*`).
  - About 300-400 B a cell, about 5-6 KB for the block.
  - Upkeep is a one-line verdict edit.
  - Detail costs one digest read, only for a touched axis.
  - The breach inventory moves into U7's spec, which needs it anyway.
  - Cost: F9's deferral then rests on the U7 spec rather than the map. The owner asked for a table with "чем держится" and "на чём
    проверено"; both forms satisfy that.
- The `variety: none` short form is enough only for diffs that truly meet no axis, and most package diffs meet one or two (axes 8,
  13). Recommend: lines for met axes only, plus `other axes: n/a`, instead of 13 lines or none. This also keeps the Lead's plan and
  §1 short.

**K8 — the U4 dispatch: holds, with R12 and n5.**
- The DoD is checkable, and every command was re-checked. All four tool files exist. The index check and `--witness-for` run green
  on the base.
- The keys are verbatim and the negative control is real. They are too thin for verbatim text (R12).
- Owns are complete for §4 as written. R10 and R11 would add PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md and docs/SIBLING_MAP.md.
- Left for the builder to invent: only the PROJECT.md rewrap (fine) and Option B capitalisation (moot once n5 is done). E10 should
  name its command: `session_context.boot_budget_lines` or `wc -c`.

## Trail

Read:
- the spec (whole), the brief (whole), architecture.md (1-62, 127-158, 277-296 and grep), factory-rules.md (FR-13, FR-47, FR-57,
  FR-59).
- OWNER_PRINCIPLES.md (P2, P11, P13, P15, P22), critic.md (192, 251, 281), designer.md (22-36), SIBLING_MAP (headings, axes 31 and
  34), WEEKLY_CALIBRATION_PROTOCOL.md (checks 36, 41, 42), PROCESS/README.md:20-27, worker-boot r2 spec (528-534, 560-566).
- Code and data: tools/architecture_index.py (whole); session_context.py (thresholds); agents_md.py (head); install_parity_anchors.json
  (135-180); test_conductor_investigates_first.py (88-96, 182); selftest.py (620-635, 673); test-layers.json (`named_by` grep);
  test_quarantine.py (`named_by`, PACKAGE_PROSE).
- Digest rows for the sampled ids in t-1200, t-1201 and t-1203, plus the t-1203 header and line 146.

Commands:
- `git rev-parse origin/main HEAD` → b5fca9bd (twice). `git diff --stat dc23e384 b5fca9bd -- <touched>` → empty.
- `boot_budget_lines(root)` → `BOOT BUDGET: 112646 bytes / 120000 (4 files + 4 imports) WARN | CLAUDE.md: 51953/58500 incl. imports
  101738`.
- `python -B tools/architecture_index.py --check` → `architecture index: up to date (29 invariants, 2682 bytes)`.
- `grep -c "^\*\*AR-[0-9]* — "` → 29.
- Byte script → 94, 21, 62. Insert script → 19269 B; cells 849-1960; Cyrillic none; test names `['test_judgment_census.py']`.
- `owns_readers.py --paths <5> --names AR-2 variety` → as in the table.
- `scenario_walk.py --witness-for ai-packages/qa-factory/design/architecture.md` → two keep rows.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "38 SIBLING_MAP axes enumerated by the spec; axis 2 wrong (critic.md rule 10 exam deviation line missing, R6); axis 34 overlap with critic Q12 unaddressed and no SIBLING_MAP row (R11); artifact sweep missed critic.md rule 22 opener (R5); passage clause not reconciled with FR-59, AR-29, AR-28, AR-9, P15, P22 and AR-17 siblings (R1); FR-13, FR-47, P2, designer rule 6, TESTING.md, builder.md, generated indexes consistent",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-universality-variety-map-spec.md",
      "docs/tasks/specs/20261117-universality-variety-map-brief.md",
      "docs/tasks/specs/reports/20261117-universality-scout-t-1200-axes-1-6.md (sampled rows)",
      "docs/tasks/specs/reports/20261117-universality-scout-t-1201-axes-7-13.md (sampled rows)",
      "docs/tasks/specs/reports/20261117-universality-scout-t-1203-mobile-stage-walk.md (header, sampled rows)",
      "ai-packages/qa-factory/design/architecture.md",
      "ai-packages/qa-factory/design/factory-rules.md (FR-13, FR-47, FR-57, FR-59)",
      "docs/OWNER_PRINCIPLES.md",
      ".claude/agents/critic.md",
      ".claude/agents/designer.md",
      "docs/SIBLING_MAP.md (axes 31, 34, headings)",
      "PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md (checks 36, 41, 42)",
      "PROCESS/README.md",
      "docs/tasks/specs/20261117-worker-boot-and-round-rules-spec-r2.md (axis 2 precedent)",
      "tools/architecture_index.py",
      "tools/session_context.py",
      "tools/agents_md.py",
      "tools/install_parity_anchors.json",
      "tools/critic_verdict.schema.json",
      "ai-packages/qa-factory/scripts/tests/test_conductor_investigates_first.py",
      "ai-packages/qa-factory/scripts/selftest.py",
      "ai-packages/qa-factory/scripts/tests/test-layers.json"
    ],
    "reruns": [
      {"command": "python -B tools/architecture_index.py --check", "result": "architecture index: up to date (29 invariants, 2682 bytes)"},
      {"command": "session_context.boot_budget_lines(root)", "result": "BOOT BUDGET: 112646 bytes / 120000 (4 files + 4 imports) WARN | CLAUDE.md: 51953/58500 incl. imports 101738"},
      {"command": "python byte count of the PROJECT.md and CLAUDE.md inserts", "result": "94 and 21 bytes, as the spec says"},
      {"command": "python measure of the spec section 2 insert", "result": "19269 bytes; cells 849-1960 bytes; no Cyrillic; no new test name"},
      {"command": "python -B tools/owns_readers.py --paths <5 files> --names AR-2 variety", "result": "names lines for AR-2 (3 data files) and variety (common word); more lines per file; base b5fca9bd"},
      {"command": "python -B scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/design/architecture.md", "result": "keep test_conductor_investigates_first.py, keep test_selftest_slow_tests.py"}
    ]
  },
  "fixes": [
    "R1 spec 3.1 line 143: a refusal with a usable door is not a block (FR-2, FR-57, AR-9, P15); the gate never passes either (AR-28); the move goes to the owning role or the conductor's seam (AR-17, P22); in the legend, (i) becomes halts or refuses with no usable door",
    "R2 spec 2 line 92: scope the cost sentence to role work; code that makes a stage dearer stays a defect (P11, AR-12)",
    "R3 spec 2 lines 92 and 107: Q-i pointer in the definition's breach sentence; axis 10 label says whether it is a breach is Q-ii",
    "R4 spec 4.1 E5 line 204: the walk goes into spec section 1 and the Lead plan; the report and commit point at it",
    "R5 spec 4.3: add old to new for critic.md:192 rule 22 opener, plus a key",
    "R6 spec 5 axis 2 and 6a item 5: critic.md exam deviation line, the precedent Deviation: exam not run; debt F3-1",
    "R7 spec 3.1 line 146: AR-2 Breakage passage half names the TP1-13877 halt",
    "R8 spec 3.1 line 145: the U6 pointer must reach a carrier that defines U6",
    "R9 spec 2 line 94: legend clause on the t-1203 rank scale",
    "R10 spec 3.3 and 5(c): F6 (b) one sub-item in calibration check 42, or state the uncovered escapes",
    "R11 spec 4.3 and 5 axis 34: separate VARIETY from Q12 in the critic sentence; one row edit in SIBLING_MAP axis 34",
    "R12 spec 7.1: witness compares normalised insert and AR-2 block with the spec text; keys for E5, E6 and R5",
    "R13 K7: short cells with a digest pointer; walk only the met axes plus other axes: n/a (the Lead decides)"
  ]
}
```

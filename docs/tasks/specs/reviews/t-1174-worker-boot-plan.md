# t-1174 — critic on PLAN: worker boot + round rules (spec t-1137, `docs/tasks/specs/20261117-worker-boot-and-round-rules-spec.md`)

Gate: plan gate (critic.md rule 24: Q13 a-e, plus Q4, Q6, Q12). Base: origin/main **fb01d9c6**. nobriefs-n7 was merged
while this review ran (`c75dd0c7 wave: merge nobriefs-n7 (t-1161)`), so "main + n7" is now just main. All facts below were
read from `git show HEAD:<path>` on that base, not from the dirty working tree.

**Verdict: NEEDS WORK, with 5 blocking findings.** The cards cannot go out as written: they rest on files that no longer
exist, they leave a role file holding stale pointers that the plan's own new test turns red, and they do not carry the Lead's
own fork decisions. failure_class: spec. JSON `blocker` (rule 23: any blocking finding). Accepting the spec, or deciding the
forks again, stays with the Lead.

## Findings

### Blocking

**B1. Stale premises: the no-briefs wave-1 deletions (Q13 c).** On main, `docs/tasks/critic-diff-brief.md` and
`plans/builder-rules.md` are deleted. `tools/tests/test_role_carriers_one_owner.py` `DELETED` (lines 254-263) keeps them
untracked (`test_deleted_files_stay_untracked`), and K-NOBRIEF stops any main document from naming them.
`docs/tasks/exchange-form.md` is gone too, since n7. Yet the spec still relies on them:
- Card A `owns` lists both deleted files, and Card A `given` lists critic-diff-brief.md. A builder who writes them re-creates
  a deleted file, and the test goes red.
- §3 row C9-C12 says "B reads builder-rules 7b, as today". That carrier is gone.
- The §5 item-6 block quote, which Card A behaviour 3 pastes verbatim, says "today `docs/tasks/critic-diff-brief.md` items
  1-12". The Lead's F14 decision ("cite the critic role file directly") changed nothing in §5. COORDINATOR.md would then name
  a deleted file.
- The F14 decision says "Q1-Q13", but Q13 is the plan-gate question (critic.md rule 24). The standing questions of a diff gate
  are **rule 22, Q1-Q12**.
- Owns_readers output: `absent: docs/tasks/critic-diff-brief.md (owned) -- not on origin/main df6707a3`.

**B2. critic.md is a non-goal but carries pointers this plan makes stale. B1's K-STALE row turns red by construction (Q4,
Q13 d; I-2).** critic.md on main cites `CLAUDE.md rule 3` (lines 178 and 281), `CLAUDE.md rule 9's exit` (198) and
`(CLAUDE.md rule 11)` (286, inside Q13(a), which wraps). All three rules leave CLAUDE.md. §4 still says "critic.md 66/165
unchanged (targets stay valid)". That is stale: only line 66 (hygiene) stays valid.
- `git grep -P "CLAUDE\.md(?:'s)?\`?\s+(?:routing\s+)?rules?\s+\d"` (the B1 K-STALE regex) over the scanned set lists
  `.claude/agents/critic.md`. Control: designer.md gives 3 hits.
- K-STALE scans every tracked file outside EXCLUDED, and `.claude/agents/` is not excluded. So Card B1's own DoD cannot
  pass.
- Who reads rule 11 is also wrong. The critic applies rule 11's edge classes on every plan gate (Q13 a), but F1 makes
  DISPATCH_RULES.md readable only by the coordinator, designer and builder.
- The non-goal's reason ("an exam is owed on any edit") no longer holds: the Lead's F8 decision already runs
  `PROCESS/CRITIC_EXAM.md` after B1 and before the commit. That is the order critic.md rule 10 needs.
- Fix: put critic.md (the 4 citations) into Card A owns, make the critic a DISPATCH_RULES reader, and run the F8 exam on the
  edited file.

**B3. The cards do not carry the Lead's fork decisions (Q13 e; the spec header itself says "F1, F5, F9 and F13 change card
text").**
- **F5 = alternative** (`.next` / `*_next.py` copies with a `*_PATH` test variable). Card B2 still owns 14 live hook and
  gate files directly. Card B1 still owns live `tools/session_context.py` and `tools/mechanism_gate.py`. The only precedent
  for `*_PATH` is `HYGIENE_GATE_PATH` in `test_hygiene_gate.py` and `test_permission_audit.py`. Nothing says:
  - which files go as copies. The hazard only bites hooks that fire on the builder's own calls: PreToolUse Edit/Write and
    Bash, PostToolUse, SubagentStop, and `.githooks/` → `mechanism_gate`. It does not bite `dispatch_gate` (Task) or
    `session_context` (SessionStart), which never fire in a builder. So F5's original recommendation was sound for those
    two;
  - how the cross-imports resolve. `dispatch_gate` and `dispatch_new` import `dispatch_manifest`, and the B1 pins read B2's
    strings. A `_next.py` copy is invisible to the importers;
  - when the Lead places the copies relative to B1's test run.
- **F14**: §5 is unchanged (B1).
- **F3** ("package critic dispatches carry `design/architecture.md` + `design/factory-rules.md`; one line in PROJECT p.1")
  has no executor. Card A behaviour 2 says "Apply §3's last column and nothing more", and §3 P5-P10 says "none".

**B4. A worker duty loses every worker reader (question 4).** §3 C26 sends Cost gates to COORDINATOR.md with reader C only.
Cost gates holds a worker duty that no role file restates: "a worker trims run output before it enters its context (`-q`, a
30-line tail, `Read` with a limit over 400 lines, `Grep` …)". A grep of `30-line|trim|tail|250K|400K|agent_budget` over
builder, critic, designer and scout.md on main finds only unrelated hits. After the split, no worker sees this rule. The fix
follows the plan's own logic for the enforcement-file sentence (§2 item 3, "moved out because it is a builder duty"): move
this sentence into the CLAUDE.md worker block. Sweep of the other worker-duty sentences in the coordinator rules:
- rule 4, parallel sessions → builder rule 10 ✓;
- rule 5 → all four role files ✓;
- rule 9, analogs → builder rule 5 ✓;
- rule 11, "needed beyond the manifest" and "no DoD → questions" → builder 23/47, critic 8/16, designer 5 ✓;
- rule 12, Cost gates trimming ✗. This one is the instance.

**B5. Two new MAIN documents lack axis-31 rows and the owner's word (question 4; PROJECT.md «Лишних документов нет»).** That
rule says: «Новый основной документ — словом владельца и строкой оси 31 (коммит Lead)».
- The spec creates COORDINATOR.md and docs/DISPATCH_RULES.md. No card adds their axis-31 rows to `docs/SIBLING_MAP.md`, and
  §8 says only "31 covered: owners, pointers, TOC, K-STALE".
- Without those rows, `main_documents()` in the role-carriers test leaves both files out of the K-NOBRIEF scan. Then nothing
  stops a deleted-file name from landing in them (the B1 scenario).
- COORDINATOR.md is the core of the owner-approved split («давай сделаем сейчас»). DISPATCH_RULES.md is a third document
  that the designer invented (F1), decided «до слова владельца». The rule asks for the owner's word, not a Lead default.
- Alternative the fork missed: (d) rule 11 goes into the CLAUDE.md worker block. It is about 7.0 KB, so CLAUDE.md would be
  about 14.4 KB, still under the plan's 20000 WARN. Designer, builder and critic would all reach it with no new document.
  The cost is about 7 KB on every worker call.
- The choice is the Lead's and the owner's. Either way, Card A must write the axis-31 rows.

### Fix before dispatch (non-blocking)

**N1. F12(a) contradicts the spec's own error direction (Q13 e).** §5 says a ternary, a lambda or a dict-dispatch entry
"must stay outside the border". The chosen regex `^\+\s*(def |class |…|if |elif |else\b|…)` matches none of them.
- Input `+    mode = "strict" if flag else "loose"` → 0 matches → border 0 → the Lead self-accepts a new branch. That breaks
  the invariant "no new logic is ever accepted without a critic".
- Fix: take F12(b), add `lambda\b`, and state that a dict-dispatch entry is caught only by the Lead's Q-walk. The other
  route is to weaken the stated invariant.

**N2. The border's base `<verdict sha>` is undefined.** `tools/critic_verdict.schema.json` has no sha field. The spec must
name the carrier (for example, the reviewed head recorded in the critic dispatch) and the absent case, which goes outside
the border.

**N3. Card A's DoD check (k1) fails on a correct build.** "Every line ≥ 8 chars … occurs in exactly one of four files" does
not hold for markup that is already repeated in HEAD: `|---|---|---|` appears 4 times and `|---|---|` 5 times
(`git show HEAD:CLAUDE.md; …PROJECT.md | awk 'length>=8' | sort | uniq -c`). The R1, R13, R11 and pt.6 tables land in three
different files. Exempt markup-only lines, or count against the original multiplicity.

**N4. Branch mechanics for B1 "after A and B2, on the same branch" are not stated (question 2).** CLAUDE.md, `.claude/agents/`,
BOOT.md and most B2 files are in `MECHANISM_PREFIXES`. By builder.md rule 10 they stay STAGED and are never committed by the
builder. Two parallel worktrees therefore end up as two staged sets, and the spec does not say how B1 gets both. Pick one:
- one worktree with disjoint owns;
- a Lead WIP-merge;
- A and B2 run sequentially.

Combine this with B3's timing for the copies.

**N5. `CLAUDE_WARN = 20000` is asserted, not derived, so edge 5's detector does not work.**
- `session_context.py:223-225` derives the WARN as ceil(measured × 1.15 / 100) × 100. For about 7.4 KB that gives about
  8600.
- At 20000, a merge that doubles a moved paragraph (rule 4 is about 3 KB) does not fire. K-OWN keys only about 6 sentences.
- Fix: B1 derives the value from Card A's measured size.

**N6. Readers and wording, partly from owns_readers (Q13 d, Q13 b).**
- The spec has no `owns_readers.py` block (designer.md rule 7), so this review ran it. Lines with no answer in the spec:
  - `names: tools/test_streams.py names MECHANISM_PREFIXES` → S4: `coordinator_rules.py` must not import `tools/streams.py`.
    That is an edge for B1;
  - `names: tools/test_worktree_sweep.py` → unchanged: it only calls `_matches`;
  - `absent: critic-diff-brief.md` → B1.
- The hook line ("workers never read them") and the COORDINATOR.md head line contradict the reader column:
  - designer reads COORDINATOR rule 10 (C18-19);
  - builder reads PROJECT p.1 (builder rule 11);
  - designer, builder and, after B2, critic read DISPATCH_RULES.

  Fix the wording to "workers do not read these at boot; a role reads only the section its role file names".
- `F13 "through the same path as designer:"`: `designer:` is a builder-dispatch item. Name the place: the critic/designer
  `handoff:` branch of `dispatch_gate`. State its positional invariant: the handoff refusal still fires first or alongside.
- Edge 8: K4 is a scout fixture and K8 a critic fixture, so both stay unaffected. That is a value, not "B2's case table".

**N7. Stale numbers and line references (question 1). Correct values:**
- Boot budget: 112183 → **112646** (live `session_context.py` on fb01d9c6).
- Worker auto-load "about 99 KB" → **101738** (`CLAUDE.md: 51953/58500 incl. imports 101738`).
- `routing-policy` anchors: 88 → **89**.
- role-carriers test: `OWNER_KEYS 47-50` → the CLAUDE.md keys sit at **57, 59-61**; `TOC 107-158` → **109-165**.
- builder.md: `62` → **67** (hygiene), plus rule-12, rule-10 and rule-2 citations at **107, 116, 117**. Card A item 6 covers
  these, but §4 calls the file unchanged.
- critic.md: see B2.
- Still true: CLAUDE_WARN 58500 at :235; MAX_LINES 25 at :190; `_ALWAYS_INCLUDE_BOOT_FILE` at :211; the pins
  `test_compact_snapshot.py:684` and `test_session_context.py:3335`; main() order layer A → compact
  (`peer_note_lines` follows and is empty in the pin); dispatch_gate 620/710; dispatch_manifest 138; journal_write 58/422;
  journal_validator 153/315/679; journal_hooks 41; probe 1273; designer.md 17/24/32; ROOT_FILES; handoff_gate
  `WRITE_TOOLS`/`GATED_KINDS` 68-69; designer frontmatter; calibration checks 2/7/10/17/28/33.
- Also missed but harmless: citations at dispatch_gate.py:3 and journal_validator.py:17. B2 behaviour 1 covers them.

**N8. Cost (question 5).** Estimates from section byte counts on HEAD (script in the trail):
- **The plan holds in direction, but understates the coordinator side.**
- New CLAUDE.md ≈ **7.4 KB**: hygiene 4386 + Язык 1167 + cwd bullet 910 + enforcement sentence 340 + about 650 new. The plan
  says 10-11 KB, so it holds conservatively.
- Worker auto-load goes from 101.7 KB to about 7.4 KB. That holds, and is better than claimed.
- COORDINATOR.md ≈ **43.7 KB**, not "about 37 KB" (edge 12). That is still about 11K tokens, under the Read cap.
- DISPATCH_RULES ≈ 7.0 KB. PROJECT.md ≈ 34.2 KB.
- **BOOT BUDGET after the split ≈ 116.8 KB of 120000**. Headroom drops from 7.4 KB to about 3.2 KB, because the §5 texts add
  bytes and the imports simply become boot files.
- The spec never states the post-split total. M1(a)'s "which it already paid" understates by about 4 KB, plus the Read
  line-number overhead.
- Ask: §8 should state the total, and name the next lever if a later rule pushes it over 120000.

## Plan-gate questions

- **Q13(a) EDGES:** the edges that go unstated are N2 (base sha absent), N3, N4, the positional placement in N6, and the S4
  import edge. The others are stated, each with its invariant (§6 1-15).
- **Q13(b) MEANING:** the `CLAUDE.md:` suffix comes to mean the worker auto-load. That is stated. The meaning of "workers
  never read" contradicts the reader table (N6).
- **Q13(c) PREMISES:** B1 does not reproduce. Re-ran: boot budget (112646, not 112183), K-STALE regex over the scan set
  (critic.md hit), deleted-file status (absent).
- **Q13(d) READERS:** block missing; ran it, answers in N6.
  - Miss 3 (pinned VALUE): `58500` appears only in session_context.py:223-235.
  - Miss 6: base fb01d9c6 is origin/main: yes.
- **Q13(e) FORKS:**
  - F12(a) is contradicted by the spec's own evidence (N1).
  - F1(a) needs the owner's word (B5).
  - F5 and F14 are not carried into the cards (B3).
  - F3 has no executor (B3).
  - F2, F4, F6, F7, F9, F10, F11 and F13 are consistent.
  - No fork is left undecided. The implicit fork (critic.md edit plus exam) is B2.
- **Q4 CLASS COMPLETENESS:** axis 31 is incomplete (critic.md, new axis-31 rows). Axis 2: the F8 exams are not placed in
  the §7 order. `PROCESS/PATCH_PROTOCOL.md:19` lists policy carriers as "(CLAUDE.md, …)", so COORDINATOR.md becomes one too.
  This is a minor sibling: retarget it in Card A.
- **Q6 DUPLICATION:** `boot_path_files` treats BOOT.md as "the single owner" of the boot list. `COORDINATOR_FILES` is a
  second list, which is fine only if BOOT.md never lists those files in the `Read X.md` form (Card A item 7 must not). The
  fallback literal of edge 2 is a pinned copy, which is acceptable. Otherwise none found. Grepped:
  `MECHANISM_PREFIXES`, `ROOT_FILES` and `_ALWAYS_INCLUDE_BOOT_FILE` readers via owns_readers.
- **Q12 ONE ROAD:** Codex AGENTS.md keeps the full text (F7). That is a host-capability condition (no SessionStart, no
  import), and the same generator reaches it, so it is not an exclusion. None blocking. Grepped: agents_md import handling
  and the axis-34 row in §8.

## Trail

- Read: spec lines 1-555 (whole); critic.md on HEAD 155-317; builder.md 60-68, 104-128; designer.md 1-6, 15-33, 98-112;
  session_context.py 1157-1185, 1300-1420, 2600-2660; test_role_carriers_one_owner.py 1-166, 251-366 (HEAD and n7);
  SIBLING_MAP axis 31 (473-540); mechanism_gate.py 215-270; test_streams.py 335-380; settings.json hook commands; fixtures
  K4 and K8 heads.
- Commands, verbatim results:
  - `python -B tools/session_context.py < /dev/null | grep BOOT` → `BOOT BUDGET: 112646 bytes / 120000 (4 files + 4
    imports) WARN | CLAUDE.md: 51953/58500 incl. imports 101738`. Before the n7 merge it read 112183 / 51490 / 101275.
  - `git cat-file -e HEAD:docs/tasks/critic-diff-brief.md` → `fatal: path ... does not exist`.
    `git show HEAD:plans/builder-rules.md` → br-gone.
  - `owns_readers.py --base origin/main --paths CLAUDE.md PROJECT.md <3 indexes> docs/tasks/critic-diff-brief.md --names
    CLAUDE_WARN _ALWAYS_INCLUDE_BOOT_FILE ROOT_FILES MECHANISM_PREFIXES` → `readers: 135 outside owns`; absent critic-diff-brief;
    names in test_streams / test_worktree_sweep / test_claim_control_gate / test_mechanism_gate / test_session_context.
  - K-STALE regex git grep → 37 files, including `.claude/agents/critic.md`; control designer.md → 3.
  - Duplicate lines in HEAD CLAUDE+PROJECT ≥ 8 chars → `4 |---|---|---|`, `5 |---|---|`.
  - Section byte script → `CLAUDE 51953 hyg 4386 r11 6975 enf 340 ats 101 lang 1167 cwd 910 PROJECT 36026` / `est new CLAUDE
    7398 COORD 43711 DISPATCH 7035 PROJECT 34249` / `est BOOT total 116770`.
  - install_parity units → routing-policy 89 anchors; designer anchor `the text is CLAUDE.md rule 11`; lead-ranking anchor
    present; no kit_path uniqueness check (install_parity.py 290-376).

```json
{
  "verdict": "blocker",
  "blockers": [
    "B1 stale premises: docs/tasks/critic-diff-brief.md and plans/builder-rules.md are deleted on main (kept untracked by test_role_carriers_one_owner DELETED); Card A owns/given them, section 3 cites builder-rules 7b, section 5 item-6 text names the brief (F14 not applied; also Q1-Q13 should be rule 22 Q1-Q12)",
    "B2 critic.md is a non-goal but cites CLAUDE.md rule 3 (178, 281), rule 9 (198), rule 11 (286): stale after the split, and B1's own K-STALE regex matches critic.md, so Card B1 DoD cannot pass; critic is also a rule-11 reader missing from DISPATCH_RULES readers; F8 already pays the exam",
    "B3 cards not rewritten for Lead decisions: F5 alternative (.next / _next.py copies) absent from B2/B1 owns, no file list, no import resolution, no placement timing; F14 not in section 5; F3 (package critic given line in PROJECT p.1) has no executor",
    "B4 Cost gates worker duty (trim run output: -q, 30-line tail, Read limit, Grep) goes to COORDINATOR.md reader C only and is restated in no role file: workers lose it; move it to the CLAUDE.md worker block like the enforcement-file sentence",
    "B5 two new main documents (COORDINATOR.md, docs/DISPATCH_RULES.md) get no axis-31 rows in any card, so K-NOBRIEF does not scan them; DISPATCH_RULES.md needs the owner's word per PROJECT.md (Lishnih dokumentov net), not a Lead default; alternative (d): rule 11 in the CLAUDE.md worker block, about 14.4 KB total"
  ],
  "class_completeness": "Axis 31 incomplete: critic.md pointers (B2), new axis-31 rows (B5), wording 'workers never read' vs reader table (N6). Axis 2: F8 exams not placed in the card order. Minor sibling PROCESS/PATCH_PROTOCOL.md:19 policy-carrier list. Sweep of worker-duty sentences in coordinator rules: rules 4, 5, 9, 11 restated in role files; rule 12 Cost-gates trimming is the uncovered instance (B4).",
  "fixes": [
    "Drop the deleted brief files from Card A owns/given; rewrite section 3 C9-C12 reader note; rewrite the section 5 item-6 quote to cite critic.md rule 22, Q1-Q12",
    "Add critic.md to Card A owns (4 citations), list critic as DISPATCH_RULES reader, run the F8 critic exam on the edited file before the commit",
    "Rewrite B2/B1 owns per F5 alternative: name the files that fire in a builder as copies, state import resolution and when the Lead places them; give F3 an executor",
    "Move the Cost-gates worker trimming sentence into the CLAUDE.md worker block",
    "Card A writes axis-31 rows for both new documents; Lead obtains the owner's word for DISPATCH_RULES.md or picks an alternative",
    "N1 take F12(b) plus lambda, or weaken the stated invariant; N2 name the border base sha carrier and its absent case",
    "N3 exempt markup-only lines from k1; N4 state how B1 receives A and B2 staged mechanism-path edits",
    "N5 derive CLAUDE_WARN by the existing 1.15 formula from Card A's measured size; N6 state the S4 no-streams edge for coordinator_rules.py, fix the 'workers never read' wording, name the facts-check branch and its positional invariant, set K4/K8 as unaffected",
    "N7 correct stale numbers (112646, 101738, 89 anchors, role-carriers 57-61 and 109-165, builder.md 67/107/116/117); N8 state the post-split BOOT BUDGET (about 116.8 KB of 120000) in section 8"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-worker-boot-and-round-rules-spec.md 1-555",
      "HEAD:.claude/agents/critic.md 155-317",
      "HEAD:.claude/agents/builder.md 60-68, 104-128",
      "HEAD:.claude/agents/designer.md 1-6, 15-33, 98-112",
      "HEAD:tools/session_context.py 1157-1185, 1300-1420, 2600-2660",
      "HEAD:tools/tests/test_role_carriers_one_owner.py 1-166, 251-366",
      "nobriefs-n7:docs/SIBLING_MAP.md axis 31 473-540",
      "HEAD:tools/mechanism_gate.py 215-270",
      "HEAD:tools/test_streams.py 335-380",
      "HEAD:tools/fixtures/dispatch_manifest/K4.txt, K8.txt heads"
    ],
    "reruns": [
      {"command": "python -B tools/session_context.py < /dev/null | grep BOOT", "result": "BOOT BUDGET: 112646 bytes / 120000 (4 files + 4 imports) WARN | CLAUDE.md: 51953/58500 incl. imports 101738"},
      {"command": "git cat-file -e HEAD:docs/tasks/critic-diff-brief.md", "result": "fatal: path does not exist in HEAD (brief-gone); plans/builder-rules.md also gone"},
      {"command": "python -B tools/owns_readers.py --base origin/main --paths CLAUDE.md PROJECT.md indexes critic-diff-brief.md --names CLAUDE_WARN _ALWAYS_INCLUDE_BOOT_FILE ROOT_FILES MECHANISM_PREFIXES", "result": "readers: 135 outside owns; absent critic-diff-brief.md; MECHANISM_PREFIXES named by test_streams.py and test_worktree_sweep.py"},
      {"command": "git grep -l -P K-STALE regex over the role-carriers scan set", "result": "37 files incl. .claude/agents/critic.md; control designer.md 3 hits"},
      {"command": "awk length>=8 | sort | uniq -c over HEAD CLAUDE.md + PROJECT.md", "result": "4 x '|---|---|---|', 5 x '|---|---|'"},
      {"command": "section byte estimate script over HEAD CLAUDE.md / PROJECT.md", "result": "est new CLAUDE 7398 COORD 43711 DISPATCH 7035 PROJECT 34249; est BOOT total 116770"}
    ]
  }
}
```

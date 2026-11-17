# t-1239 critic topic 1 (spec r2 §7): Cards A (FG7-57) + B2 (FG7-58), diff 7f945fdd..26aa2064 (wb-int)

**Verdict: NEEDS WORK, 0 blocking findings, 13 fixes before merge.** Accepting the topic, and amending the spec texts that
fixes F2, F4, F6 and F13 touch, is the Lead's decision.

Nothing blocks. The move is complete and checks out: my re-run of k1-k5 gives the same result, the copies differ from their
live files only where the spec allows, the facts gate keeps the order the spec sets, and the loader really swaps the copy in.
The fixes fall into four groups:
- one rule regex is broken by line wrapping and errs on the unsafe side (F1);
- coordinator and pointer texts are stale (F2, F3, F5, F13);
- the gate's refusal and the doc text of one unknown case disagree with the sibling checks or with the spec (F6, F7);
- there is a second loader road, plus test hygiene and report-file hygiene (F8-F12).

## Findings

**F1 — the border regex is split inside code spans; the counter misses `.mkdir(` and `open(p,"w")`.** Severity: fix before
merge (the error is on the unsafe side).
- Where: COORDINATOR.md:318-320. The write list wraps as ``open\(.*`` + newline + ``['"][wax]`` and as ``subprocess\.|\`` +
  newline + ``.mkdir\(``. Read with the line join (CommonMark turns a line break inside a code span into one space), it
  becomes `open\(.* ['"][wax]` and `\ .mkdir\(`.
- Probe (trail R3):
  - `+    out.mkdir(parents=True)`: rendered pattern False, intended pattern True.
  - `+    fh = open(p,"w")`: rendered False, intended True.
- So a fix round that adds a write path measures border 0. That breaks the invariant of §5.1 and of t-1202 fix 1 ("errs
  only toward a re-review").
- The other wraps are harmless when joined: `match |case`/`|return` joins to `case |return`; `git ls-files`/`--others`;
  `opus:`/`reviewed:`.
- Fix: put the three patterns (line-start, anywhere, write list) each on one unbroken line. A fenced block under the
  paragraph is best, so nothing re-wraps them.

**F2 — builder call A-Q1: the intro of COORDINATOR.md is false.** Fix.
- Where: COORDINATOR.md:5-9 says "Auto-loaded into every session: the routing policy … and its command hygiene" and
  "Without an auto-loaded policy, Lead ends up doing delegable work". This file is not auto-loaded and holds no hygiene.
- boot-diet SKILL.md:103 now cites this "opening rationale" as the reason not to cut auto-loaded policy.
- Spec §3 C1 asked for the move verbatim (I-1), so the defect is in the spec, not the builder.
- Fix (a Lead amendment of C1): rewrite to "The coordinator's routing policy of this repository (the worker block — the
  dispatch form, command hygiene, worker duties, Язык — is `CLAUDE.md`, auto-loaded) … Without this policy in context (the
  `COORDINATOR RULES:` line), Lead ends up doing delegable work itself …". Keep boot-diet:103's pointer.

**F3 — builder call A-Q2: dangling colons.** Fix.
- Where: COORDINATOR.md:11 ends "(the `COORDINATOR RULES:` line):" and COORDINATOR.md:15 ends "rule 10):". Both colons
  introduced the deleted `@` lines, so nothing follows them now.
- Fix: end both sentences with a period.

**F4 — the §5.1 block cuts the Cost-gates sentence in half.** Fix.
- Where: COORDINATOR.md:306-325. "…the fix diff and the verdict;" is followed by "After a critic verdict … step 6." and then
  "the Lead compacts by PROJECT.md § Сессия форджа …", which now starts in lower case after a full stop.
- The spec's anchor ("after '…the verdict;'") produced this, so the cause is the spec text.
- Fix: capitalise "The Lead compacts". Or place the §5.1 block as its own paragraph right after "Detector: check 17."; that
  keeps the meaning, and moving it is the Lead's call.

**F5 — class completeness, axis 31: Card A left stale pointers in its own files and in one outside file. B1's K-STALE will
fail on two of them.** Fix.
- My scan with B1's K-STALE regexes (§8 B1 behaviour 6) over the scan set (trail R4) finds:
  - docs/SIBLING_MAP.md:550 ("every cell of CLAUDE.md § Contents");
  - docs/TWO_VOCABULARIES.md:11 and :18 ("CLAUDE.md Tiers").
  B1 owns neither file, so B1's DoD would fail on files it cannot edit.
- Siblings in the same artifact, inside Card A's owns (the builder listed most of them as analogs; rule 9 sweep):
  - SIBLING_MAP:28 ("Routing policy | CLAUDE.md"), :37 and :40 (rule changes "in CLAUDE.md"), :97 ("loaded every session …
    imported by CLAUDE.md": false now), :99, :105 (the AGENTS.md regeneration list is missing COORDINATOR.md), :548, :668
    ("Role ≠ tier, CLAUDE.md").
  - PROJECT.md:79 («`docs/FACTORY_RULES_INDEX.md`, грузится в каждую сессию»: false now; the same class as the P4/P5
    retargets). PROJECT.md:28 (the Оглавление row «Сессия форджа | шелл, …»: the shell bullet moved to CLAUDE.md).
  - delegation.config.yaml:4, :7, :70. Line 70 is the twin of gateway/config.template.yaml:49 ("function/grade split"):
    49 was retargeted to COORDINATOR.md and 70 was not, so the twins now disagree.
- Outside every card's owns, inside this pile: `docs/TWO_VOCABULARIES.md:4,11,18`. The Lead widens the Card A fix round to
  this file.
- The cause is in the spec: §4.1's census grep had the rule-number form only and never searched for section names
  (Tiers, Contents, Role ≠ tier).

**F6 — builder call B2-Q1(c): FACTS MISSING does not name the waiver door; its sibling refusals do.** Fix.
- Every handoff refusal except HANDOFF_MANY names `HANDOFF_SKIP_DOOR` (dispatch_gate.py.next:713-723). FACTS MISSING names
  only `facts: none -- <why>`.
- FR-2 / AR-9: the named door is usable, so this is not an FR-2 breach. But a Lead who has facts and cannot measure them
  yet is pushed toward a false `facts: none`. The honest door is `manifest-skip: facts -- <reason>`, which the spec edge
  passes with a note (FR-4), and it goes unnamed. It also breaks the one refusal shape (AR-18).
- Fix: append "To send it on purpose without measured facts, add: manifest-skip: facts -- <reason>." (amend the §5.3 text).
  Add a `message_has` entry for it in the "no-line" row.

**F7 — the code does not match its docstring, the report or the spec on the "manifest without FACTS_KINDS" unknown.** Fix.
- Where: `facts_check` (dispatch_gate.py.next:788-807). The docstring says "an unknown (…, a manifest without the facts
  reader) is a NOTE and a pass". The report says the same: "Unknowns (no cut, degraded cut, manifest without FACTS_KINDS) =
  note + pass".
- The code returns `(0, "", "")` when `FACTS_KINDS` is absent, and test_dispatch_gate.py `OldManifest` pins exactly that
  silent result.
- Spec §5.3: "an unknown (… import failure) is a NOTE and a pass".
- Fix: return `FACTS_NOTE_UNCHECKED.format(what="dispatch_manifest has no FACTS_KINDS")` and update the OldManifest
  assertion.

**F8 — Q6/Q12: a second loader road; one docstring now lies.** Fix.
- `tools/under_test.py::load_under_test` already loads "the file named by the environment variable … so a sibling import of
  that name resolves to it". Five test files use it (test_hygiene_gate, test_permission_audit, test_dod_gate,
  test_session_context, test_compact_snapshot), and its docstring says "the environment read lives only here".
- The conftest `_NextCopyFinder` is a second implementation of the same action. With it, that sentence is false.
- Spec F5-r compared the new loader with per-module loaders but never named `under_test.py`, a premise the spec did not
  measure.
- Fix in this round: correct the under_test.py docstring so it names the split (`.py` candidate → load_under_test;
  `.py.next` import closure → conftest finder). Also open a convergence node (one loader for both forms), owner Lead,
  forge/7.

**F9 — the loader's typo guard misses t-1202 fix 4's own example.** Fix.
- Reproduced: `DISPATCH_GATE_PATH=tools/dispatch_gate.py.nxt` is silently ignored and the live file is tested (trail R2:
  9 failed). Here the tests caught it only because the facts rows fail on the live file. A comment-only copy would be
  false-green.
- Fix: in `next_copy_map`, raise when the value's file name starts with `<name>.py` and is neither `<name>.py` nor
  `<name>.py.next`. Add one row. Do not fail on every value that is not `.py`: Git Bash's `ORIGINAL_PATH` and the like
  would break the session.

**F10 — Q5 (c)/(e)/(f): tests.** Fix.
- `test_facts_state` (test_dispatch_manifest.py, 13 rows) tests an internal reader. Six of its rows (tail/ok-line, empty,
  bare-none, none-why, quoted, prose) repeat `_FACTS_ROWS`, which already goes through the door (`decide_full`). Each row
  also asserts `FACTS_KINDS == ("designer",)`, a pin on a constant.
- test_dispatch_new.py "facts-builder-untouched" (:80) repeats "ok" (:44) and "readers-no-note" (:83).
  "facts-designer-bare-none" repeats the hook row.
- Fix: move the 5 unique facts_state rows (empty-then-blank, block, n/a, none-why-below, none-then-fact) into
  `_FACTS_ROWS`, delete `test_facts_state` and the constant pin, and delete the two duplicate dispatch_new rows.

**F11 — Q2, a builder decision: `dispatch_new --facts` refuses backticks.** Fix.
- `FORBIDDEN_CHARS` applies to `--facts`. A "verbatim result" grepped from this repo's markdown usually contains
  backticks, so the generator refuses the common case and the Lead has to hand-type the header.
- The generator wraps nothing in backticks for `facts:`.
- Fix: exempt `--facts` from the backtick ban (keep newline and CR banned) and add one row. If the builder knows a reader
  that the backticks would break, it names that reader instead.

**F12 — hygiene of the report file.** Fix.
- docs/tasks/handoffs/t-1233-card-a.md is not valid UTF-8: at byte 51537 there is a truncated `\xe2\x80` (an em dash cut
  in the pasted WEEKLY diff line). Its line endings are mixed (223 CRLF / 780 LF). The file is in 26aa2064, so it lands
  in main.
- Fix: repair the byte; use one line ending.

**F13 — axis 31: the dispatch form (rule 11, CLAUDE.md) does not mention the new code-refused designer header.** Fix.
- R11-h ("critic/designer dispatch") names only `handoff:`. `facts:` is now refused by code for the designer kind, but
  its text lives only in COORDINATOR.md rule 2.
- Fix: add a pointer to R11-h: "a designer dispatch also carries `facts:` (COORDINATOR.md rule 2)". This is a spec delta;
  the Lead decides.

## Builder calls

| call | verdict |
|---|---|
| A-Q1 stale intro | fix: F2 |
| A-Q2 trailing colons | fix: F3 |
| A-Q3 retarget wordings (boot-diet 8/21-24/85/99/103, session-handoff 56, README 15/41, BOOT 5-8, RUNBOOK 201-202/622, SIBLING_MAP) | fit: each is the smallest true wording; e17 holds (BOOT.md has no "Read X.md") |
| A-Q4 WEEKLY 498 left as is | fit: the text means rule 11's five-point checklist, which stays in CLAUDE.md under (d); the §4.1 row was a spec error |
| B2-Q1(a) `facts` in SECTION_STOP_RE and ITEM_EXCLUDED_SECTIONS | fit: the same treatment as siblings/designer; one cut (axis 13) |
| B2-Q1(b) key `facts` only, bare header | fit: the rule text and the refusal both name `facts:`; a `fact:` line gets the refusal with the right door |
| B2-Q1(c) FACTS MISSING verbatim, no manifest-skip door | fix: F6 |
| B2-Q1(d) `dispatch_new --facts` for any kind | fit: an extra header does nothing for other kinds, and nothing is refused by a name; the backtick part is F11 |
| B2: 4 loader rows instead of 3 | fit |

## Standing questions (critic.md rule 22)

- **Q1 fit to spec.**
  - Card A: items 1-8 are implemented and k1-k5 pass on my re-run (R1).
  - The §5.1 text carries t-1202 fixes 1-2, but F1 corrupts fix 1's text. §5.2-§5.4 and the F3 sentence are present.
  - Card B2: items 1-5 are implemented. Order: completeness → handoff → facts → path → label (decide_full :827-856).
    Every edge has a row: empty, bare none, `none -- -`, waiver, unknown cut, handoff wins, builder/critic untouched.
  - Deviations: F6 (spec text), F7.
- **Q2 the builders' own decisions.** Safe and consistent, except F7 (silent instead of a note) and F11.
- **Q3 seams.**
  - The copies are additive. All 8 comment-only copies differ only in §4.1 lines (R5), and claim_control differs only in
    those plus ROOT_FILES.
  - owns_gate and critic_snapshot reach the new branch through `decide()`, so a refused designer dispatch is not
    registered, which is consistent.
  - No other test builds a designer dispatch: Grep `subagent_type…designer` over tools/ finds only test_dispatch_gate.py,
    which is also the positive control.
  - origin/main has not drifted on any owned path since 7f945fdd (R6).
- **Q4 class-wide completeness.**
  - Axis 13 ✓: facts reach the gate only through dispatch_manifest.facts_state, and the sibling regexes are reused.
  - Axis 31 ✗: F5, F8 (docstring), F13.
  - Axis 34 ✓: facts are read by kind from the FACTS_KINDS data row.
  - One road ✗: F8.
- **Q5 tests.**
  - (a) Killing power: 9 of 15 facts rows fail on the live file (R2).
  - (b) Expected values trace to §5.3 and the edges.
  - (c) Every door has a row (decide_full; the dispatch_new CLI).
  - (d) The rewritten pins (K6 items, ITEMS, ITEM_EXCLUDED_SECTIONS, `_reading_dispatch`) carry the spec's change.
  - (e)/(f): F10.
  - Volume: about 145 product lines against 108 test lines, so the volume rule holds.
  - (g) No new test file.
- **Q6 DUPLICATION AND CONSISTENCY.**
  - F8 (under_test.py vs the conftest finder).
  - F5 (yaml:70 vs gateway:49 twins).
  - F6 (the refusal shape differs from HANDOFF_*).
  - facts_state reuses `_extent_lines`, `_NONE_ANSWER_RE`, `_BARE_NONE_RE` and `_WORD_CHAR_RE`: no second grammar.
  - The forge-check clone ratchet for wb-int is not among the last 15 pipelines (positive control: 5 other pushes were
    listed), so the Lead reads it at placement.
- **Q7 CODE QUALITY.** facts_check (20 lines) and facts_state (22 lines, 3 levels of nesting) are under the caps. One
  annotation lies (F7). No dead branches.
- **Q8 hygiene.** Not a package change. Line endings follow checkout conversion (the base blobs are LF). Report file: F12.
- **Q9 ratchets.** The diff touches no ratchet row (no baseline, census or known_red file in `--name-only`).
- **Q10 architecture.** No package path, so no AR-n is touched. VARIETY: forge-only; there is no project shape on which
  this diff could block a stage.
- **Q11 JUDGMENT.** facts_check judges FORM and presence only (P27): no content judgment and no census row.
- **Q12 ONE ROAD.** No exclusion of a language, project or case. There is a residual of two roads for one action (F8); it
  is a fix in this round plus a proposed node, owner Lead.

## Spot-checks (claims and their carriers)

- "1111 passed with the PATH vars, 9 failed without": the facts subset re-run with the vars gives 15 passed; without them,
  9 failed and 6 passed (R2). Consistent with the claim.
- "the loader fails loudly on a typo": true for a missing `.py.next`, false for `.py.nxt` (R2, F9).
- "journal_write 422 / validator 679 message strings: no test pins them": Grep `CLAUDE.md (rule 1[23]|…)` over
  `tools/test*.py` finds only the comment in test_role_carriers:62, which is also the positive control of the pattern.
- "Unknowns = note + pass": false for the third case (F7).
- Card A "`git diff HEAD origin/main` over owns empty": reproduced against today's origin/main d7b99048 (R6).
- k5 "0 stale hits": reproduced. The wider K-STALE form finds 3 hits (F5); its positive control is the base critic.md,
  where it finds 3.

## Trail

- Read: spec r2 (all), t-1202 Fixes 112-137 and its N1/N2/F5-r rows, both reports (Card A 1-70 and 176-520; B2 whole).
- Read from 26aa2064: CLAUDE.md headings and 1-40; COORDINATOR.md 1-22, 92-125, 277-343, 312-320 (with the Read tool:
  character-level); the role-file diffs; SIBLING_MAP 28-40, 97-105, 475-550, 668; the PROJECT.md diff; the diffs of
  WEEKLY, RUNBOOK, TESTING and host adaptations; boot-diet 18-27, 99-125; delegation.config.yaml; gateway 47-51;
  TWO_VOCABULARIES 1-20.
- Copies: dispatch_manifest and dispatch_gate copy vs live (full), dispatch_gate.py.next 580-598, 741-860, 878-883; the
  diffs of conftest, dispatch_new and the three test files; `under_test.py` 7-21; handoff_gate WRITE_TOOLS;
  settings.json 30-51.
- Commands, with their output:
  - R1: `python -B <scratch>/card_a_check.py --base 7f945fdd` (the source extracted from the report) → k1 PASS (38 lost /
    76 gained, 0 unlisted), k2/k2b/k3/k4 PASS (14428 / 43785), k5 PASS, k5-control PASS, negative control detected,
    OVERALL: PASS.
  - R2: `( cd wb-int && DISPATCH_MANIFEST_PATH=… DISPATCH_GATE_PATH=… python -m pytest tools/test_dispatch_gate.py -q -k
    facts )` → `15 passed, 349 deselected`. Without the vars → `9 failed, 6 passed`. With `DISPATCH_GATE_PATH=
    tools/dispatch_gate.py.nxt` → `9 failed, 6 passed` (ignored silently).
  - R3: a python probe of the rendered vs the intended write regex → mkdir False/True, `open(p,"w")` False/True,
    `open(p, "w")` True/True, touch True/True.
  - R4: the K-STALE regexes over `git ls-files *.md *.yaml` minus EXCLUDED → 3 hits (SIBLING_MAP 550, TWO_VOCABULARIES 11,
    18); control on the base critic.md → 3.
  - R5: `git diff --no-index -U0` live vs copy for the 8 copies → only the lines quoted in the B2 report.
  - R6: `git diff --stat 7f945fdd origin/main -- <all A and B2 owns>` → empty.
  - Also: the UTF-8 and line-ending check over the changed files → only t-1233-card-a.md is BAD (byte 51537, MIXED
    223/780). `ci_read.py pipelines --n 15` → no 26aa2064 pipeline.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "Axis 13 covered: facts are read only via dispatch_manifest.facts_state of the one cut. Axis 34 covered: FACTS_KINDS is a data row read by kind. Axis 31 NOT complete: stale pointers in Card A owns (SIBLING_MAP 28/37/40/97/99/105/548/550/668, PROJECT.md 28/79, delegation.config.yaml 4/7/70 vs the retargeted gateway twin 49) and outside the owns docs/TWO_VOCABULARIES.md 4/11/18. B1 K-STALE would fail on SIBLING_MAP 550 and TWO_VOCABULARIES 11/18. under_test.py docstring is false after the conftest loader. R11-h lacks the facts pointer. One road: two copy loaders (under_test.load_under_test vs the conftest finder), a fix plus a proposed node with owner Lead.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-worker-boot-and-round-rules-spec-r2.md",
      "docs/tasks/specs/reviews/t-1202-worker-boot-r2-rereview.md",
      ".claude/worktrees/wb-int/docs/tasks/handoffs/t-1233-card-a.md",
      ".claude/worktrees/wb-int/docs/tasks/handoffs/t-1234-card-b2.md",
      "wb-int@26aa2064: CLAUDE.md, COORDINATOR.md (1-22, 92-125, 277-343), PROJECT.md diff, .claude/agents diffs, skills diffs, SIBLING_MAP 28-40/97-105/475-550/668, WEEKLY/RUNBOOK/TESTING/host-adaptations diffs, delegation.config.yaml, gateway/config.template.yaml, docs/TWO_VOCABULARIES.md 1-20",
      "wb-int tools: dispatch_manifest.py(.next) diff, dispatch_gate.py.next 580-598/741-883, 8 comment-only copy diffs, conftest.py, dispatch_new.py, test_dispatch_gate.py, test_dispatch_manifest.py, test_dispatch_new.py, test_claim_control_gate.py diffs, under_test.py 7-21, handoff_gate WRITE_TOOLS, .claude/settings.json 30-51"
    ],
    "reruns": [
      {"command": "python -B <scratch>/card_a_check.py --base 7f945fdd (source from the Card A report)", "result": "OVERALL: PASS; k1 38 lost / 76 gained, 0 unlisted; CLAUDE.md 14428, COORDINATOR.md 43785; negative control detected"},
      {"command": "DISPATCH_MANIFEST_PATH=tools/dispatch_manifest.py.next DISPATCH_GATE_PATH=tools/dispatch_gate.py.next python -m pytest tools/test_dispatch_gate.py -q -k facts", "result": "15 passed, 349 deselected; without vars 9 failed, 6 passed; with DISPATCH_GATE_PATH=tools/dispatch_gate.py.nxt 9 failed, 6 passed (typo ignored silently)"},
      {"command": "python probe: rendered vs intended border write regex", "result": "out.mkdir(...) False/True; open(p,\"w\") False/True; open(p, \"w\") True/True; p.touch() True/True"},
      {"command": "K-STALE regexes of spec B1 behaviour 6 over git ls-files *.md *.yaml minus EXCLUDED", "result": "3 hits: docs/SIBLING_MAP.md:550, docs/TWO_VOCABULARIES.md:11, :18; positive control base critic.md 3"},
      {"command": "git diff --no-index -U0 tools/<n>.py tools/<n>.py.next for the 8 comment-only copies", "result": "only the section 4.1 lines (+ ROOT_FILES in claim_control_gate)"}
    ]
  },
  "fixes": [
    "F1 COORDINATOR.md:318-320 border write-list regex split inside code spans (open\\(.* / ['\"][wax] and subprocess\\.|\\ / .mkdir\\(): put each pattern on one unbroken line, preferably a fenced block",
    "F2 COORDINATOR.md:5-9 stale intro (auto-loaded, command hygiene): Lead amends spec C1 and rewrites the intro to the coordinator file plus the hook line",
    "F3 COORDINATOR.md:11 and :15 dangling colons after the deleted @ lines: end with a period",
    "F4 COORDINATOR.md:306-325 the section 5.1 block splits the Cost-gates sentence: capitalise 'The Lead compacts' or place the block after 'Detector: check 17.'",
    "F5 axis 31 stale pointers: SIBLING_MAP 28/37/40/97/99/105/548/550/668, PROJECT.md 28/79, delegation.config.yaml 4/7/70 (twin of gateway 49); widen Card A to docs/TWO_VOCABULARIES.md 4/11/18 (B1 K-STALE fails on 550, 11, 18)",
    "F6 dispatch_gate.py.next FACTS_MISSING: name the door manifest-skip: facts -- <reason> like HANDOFF_SKIP_DOOR (Lead amends the 5.3 text); add a message_has entry",
    "F7 dispatch_gate.py.next facts_check: a manifest without FACTS_KINDS returns a FACTS_NOTE_UNCHECKED note (spec 5.3, docstring, report), update the OldManifest assertion",
    "F8 tools/under_test.py docstring ('the environment read lives only here') is false after the conftest finder: name the split; propose a convergence node, owner Lead (forge/7)",
    "F9 tools/conftest.py next_copy_map: raise on a value whose file name starts with <name>.py and is neither .py nor .py.next (t-1202 fix 4 example .py.nxt is ignored silently); one row",
    "F10 tests: move the 5 unique facts_state rows into _FACTS_ROWS, delete test_facts_state and its FACTS_KINDS pin; delete test_dispatch_new rows facts-builder-untouched (dup of :44/:83) and facts-designer-bare-none",
    "F11 tools/dispatch_new.py: exempt --facts from the backtick ban (keep newline/CR) with one row, or name the reader the backtick would break",
    "F12 docs/tasks/handoffs/t-1233-card-a.md: invalid UTF-8 at byte 51537 and mixed line endings: repair before it lands in main",
    "F13 CLAUDE.md R11-h: add the pointer 'a designer dispatch also carries facts: (COORDINATOR.md rule 2)' (spec delta, Lead decides)"
  ]
}
```

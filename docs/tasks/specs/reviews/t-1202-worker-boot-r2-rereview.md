# t-1202 — critic re-review of spec r2 (t-1187) against verdict t-1174: worker boot + round rules

Gate: plan re-review (CLAUDE.md rule 3, critic on plan; the one re-pass of this topic). Scope per dispatch: each B1-B5 and
N1-N8 of t-1174 against the r2 revision table, plus the Lead decisions at the end of r2 (F1'(d), F5-r(a), F8', F12', F15,
F16, F17) for feasibility; one size measurement. Spec read:
`docs/tasks/specs/20261117-worker-boot-and-round-rules-spec-r2.md` (whole, by sections). Base actually checked: origin/main =
HEAD = **69f6272f** (r2 says da47f648; the measured values below did not move: CLAUDE.md 51953 bytes, BOOT 112646).

**Verdict: FIT WITH FIXES, 0 blocking findings.** All five blockers of t-1174 are answered correctly. Two of the eight
non-blocking items are answered only in part (N1, N2), and three Lead decisions need a wording fix before the cards go out
(F5-r, F8', F17). Every fix is a text edit to r2 by the Lead (a resubmission under the same task, no designer needed). They are
listed under "Fixes" below. Accepting r2 and dispatching the cards is the Lead's decision.

## The size measurement (the one run)

One script read `git show origin/main:` blobs and ran `tools/session_context.py`. Output, verbatim:

```
origin/main CLAUDE 51953 PROJECT 36026 idx {'FACTORY_RULES_INDEX.md': 5575, 'ARCHITECTURE_INDEX.md': 2682, 'OWNER_PRINCIPLES_INDEX.md': 5212}
sections r11 6975 hyg 4386 tail3_in_hyg True enf 340 trim 245 lang 1167 cwd 911 ats 101 s5 2841
live: BOOT BUDGET: 112646 bytes / 120000 (4 files + 4 imports) WARN | CLAUDE.md: 51953/58500 incl. imports 101738
est new CLAUDE 14732 COORD 43357 PROJECT 34368 BOOT 117124 WARN 17000
```

Method: the new CLAUDE.md = title + 600 (the new intro) + headings + the enforcement and trimming sentences + rule 11 + hygiene
(minus the point-3 tail) + the cwd bullet + Язык. COORDINATOR = old CLAUDE.md minus everything that moves, minus the `@` lines,
plus about 650 bytes of new head and stub lines, plus the §5.1-§5.3 quoted texts (2841 bytes, measured from r2 lines 207-223,
236-237 and 244-249). BOOT = the live BOOT figure minus the old CLAUDE.md and PROJECT.md, plus the three new files.

- **CLAUDE.md ≈ 14.7 KB: confirmed** (14732 bytes; r2 says ≈14.7 KB). The derived WARN is ceil(14732 × 1.15 / 100) × 100 =
  **17000**, as r2 §8 B1 and e5 state. Edge 5's margin is then about 2.27 KB, which matches r2's "≥ ≈2.3 KB".
- **Post-split BOOT ≈ 117.1 KB, not 116.8 KB.** r2 §9 M1(a) says "≈116.8 KB of 120,000". The difference is the §5 texts, which
  r2 carried over from the t-1174 estimate without adding them in. Headroom is about **2.9 KB**, not 3.2 KB. The direction holds
  and nothing breaks; this is fix 8.
- COORDINATOR.md ≈ 43.4 KB (r2 e12 says 43.4 KB: confirmed). PROJECT.md ≈ 34.4 KB (r2 says 34.2 KB: close enough).

## Per verdict item (t-1174 → r2)

| item | status | where in r2, and what was checked |
|---|---|---|
| B1 deleted files | **answered** | Card A owns (§8, lines 371-396) and its given (368) name no deleted file. §3 C9-C12 (line 112) now names `docs/TESTING.md` «Что запускать по своей правке». §5.1 (line 217) cites `.claude/agents/critic.md` rule 22, Q1-Q12. Verified by carrier: critic.md:190-192 is "22. The standing questions … Q1." and :281 is the rule 24 plan gate. |
| B2 critic.md stale | **answered** | Card A owns critic.md (382). §4.1 row (151) retargets 178, 198 and 281. 286 stays valid under (d), because rule 11 stays in CLAUDE.md. My grep of `CLAUDE.md` in the four role files lists exactly 66, 178, 198, 281 and 286 for critic.md, and 67, 107, 116 and 117 for builder.md: the census is complete. The critic reads rule 11 by auto-load. The exam decision is F8' (see below). |
| B3 F5 copies | **answered** | §7 tables (335-353): each builder-firing file, why it fires, and how it is delivered. The import closure is resolved by one conftest finder (355-362). Placement is §7 step 2. Spot-checked: `dispatch_new.py`, `judge_calib_sanitize.py` and `calibration_counts.py` appear in no `settings.json` or `.githooks` command, and only tests import them (grep, with `import dispatch_manifest` as the positive control). That holds the "live edit" row. The B2 test files load their modules with plain `import` (test_dispatch_manifest:22, test_dispatch_gate:20, test_dispatch_new:9-10, test_claim_control_gate:23), so a `meta_path` finder does intercept them. Gap: the DoD covers only part of the cut's readers (fix 5). |
| B3 F14 | **answered** | §5.1 is rewritten. |
| B3 F3 | **answered** | §3 P6 (127) and Card A behaviour 2 (408); k2 keys it. |
| B4 trimming duty | **answered** | §2 item 3(b) (71-73) quotes the sentence. I matched it against CLAUDE.md on origin/main: the same text, 245 bytes. §3 C26 leaves a pointer. The §4.3 sweep enumerates rules 1-13 with a verdict for each. k2 keys `a 30-line tail`. |
| B5 new main docs | **answered** | (d) is drafted, and there is no DISPATCH_RULES.md. The COORDINATOR.md axis-31 row (Card A behaviour 4) has an Owner cell that starts with "owner". `test_role_carriers_one_owner.py::main_documents` (268-290) keeps any row whose `Owner / pointer` cell `casefold().startswith(("owner", "procedure"))`, and the axis-31 header (SIBLING_MAP:481) is `File \| Role(s) \| Aspect \| Owner / pointer`. So K-NOBRIEF scans COORDINATOR.md once the file exists. The owner's word gates the merge (F1'). What the text does not yet say is who replaces "owner word pending", and when (fix 7). |
| N1 border regex | **answered in part** | The ternary, lambda, `and`/`or` and comprehension-`if` cases now land outside, as stated. The stated error direction ("the counter errs only toward a re-review", line 227) is still false for other inputs, which give border 0. One is an inserted early exit: `+        return []`, `+    raise SystemExit(2)`, `+            continue`, `break`, `yield`. Another is a new `with` block. Another is a comprehension loop with no `if`: `+    out = [f(x) for x in rows]`, since `for ` is caught only at line start. The last is a write call outside the regex: `json.dump(obj, fh)`, `p.unlink()`, `os.replace(a, b)`, `shutil.copy(...)`, `subprocess.run(...)`, `p.mkdir()`. Each is new logic or a new write path, and §5.1's own invariant (225) bars it. Fix 1. |
| N2 base sha | **answered in part (the carrier cannot be written as worded)** | §5.1 and F16 put `reviewed:<sha>` "in the notes of the critic's `delegated` event, written by the Lead". But `delegated` is written by the PostToolUse hook, and its notes come from the Agent call's `description`: `journal_hooks.py:256` `obj["notes"] = cut_notes(tool_input.get("description"), …)`. `cut_notes` (62-69) cuts the text to `NOTES_MAX = 300` (:41) and keeps only a `replaces_worker` suffix whole. The Lead cannot write that line: a second `delegated` through the CLI is not a legal repeat. A token placed late in a long description gets cut. Either way the result is always `nobase`. That fails safe, but M2 never fires. A second gap, from F15: topic 1 and topic 2 are reviewed UNCOMMITTED (§7 steps 2 and 4 commit after the critic), so no sha exists at dispatch time. Fix 2. |
| N3 k1 | **answered** | k1 (426-428) counts multiplicity and exempts markup-only lines. Changed lines go into the edited-lines list. |
| N4 branch mechanics | **answered** | §7 and F15: one integration worktree, builders commit nothing, two critic topics. Feasibility checked: `.githooks/pre-commit` runs journal_validator, escape_check, enforcement_probe, factory_rules_index --check, architecture_index --check, agents_md --check and forge_metrics. It runs neither install_parity nor the role-carriers test, so Lead commit #1 is not refused by e8's known-red anchors. `agents_md --check` passes, because Card A regenerates AGENTS.md with the live generator (behaviour 7). |
| N5 CLAUDE_WARN | **answered** | Derived, not asserted (§8 B1 behaviour 2). The value 17000 is confirmed by the measurement above. |
| N6 readers / wording | **answered** | §4.2 has the readers block. S4 is e16. The wording "workers do not read these at boot -- a role reads only the section its role file names" is in the hook line (89-90) and in C1 (104). The facts branch is named (`facts_check` after `handoff_folder_check` in `decide_full`), with its positional invariant (260-263). K4/K8 are unaffected (e8, §4.2). |
| N7 stale numbers | **answered** | §12 carries carriers. BOOT 112646, CLAUDE.md 51953 and 101738 re-measured today: unchanged. |
| N8 cost | **answered, one figure low** | Totals are stated and the next lever is named (§9 M1). The measured BOOT is 117.1 KB, not 116.8 KB (fix 8). |

## The Lead decisions: feasibility

- **F1' = (d): feasible.** It keeps every rule-11 pin valid; I checked this through critic.md:286 and the census above. The
  merge waits for the owner's word, and that wait rests on discipline only: `wave.py merge` has no check for it. That is
  acceptable, but r2 must name the move that turns «owner word pending» into the owner's dated word before the merge, and say
  what happens on a refusal (fix 7).
- **F5-r = (a): feasible, with one contradiction.** Plain imports are verified (above), and the finder resolves `owns_gate`'s
  module-level `from dispatch_gate import`. The contradiction is between two edges. §7 (356) says the loader acts on "every
  variable `<NAME>_PATH` whose value names an EXISTING `tools/<name>.py.next`". Card B2 behaviour 5 says "a variable naming a
  missing file fails loudly". Under the §7 reading, `DISPATCH_GATE_PATH=tools/dispatch_gate.py.nxt` (a typo) is silently
  ignored. The tests then run the live file, and the "copy tested" witness is false-green. That is exactly the error direction
  a witness must not have. Fix 4.
- **F8' = the precedent line: feasible.** The precedent is real: commit **9616b6f4** ("no briefs, wave 1") carries
  `Deviation: exam not run; debt F3-1.` (body line 60) and `axis 2 …: queued -- exam not run …; debt F3-1` (line 17). r2 F8' and
  §9 cite **1f165a38**, which is the t-847 Offload A1 commit. Its deviation has a different form ("Deviation (F-A1-2)"), so the
  hash is wrong. The debt F3-1 is live in `plans/piles/onboarding-forge/batch-2-onboarding-roles-forge-p3.md:67`; the forge
  batch-3 row says «закрыта: перенесено → onboarding-forge/2». r2 §9 writes axis 2 as "covered". With the exam not run, the
  enumeration word is "queued", as the precedent wrote. Fix 3.
- **F12' = §5.1 as written: feasible but leaky** (N1 above). Fix 1 widens the counter, or narrows the stated error direction to
  what the counter actually catches.
- **F15 = §7: feasible** (N4 above). It interacts with F16: under this order the border cannot apply inside this topic (fix 2).
- **F16 = the `reviewed:` token: feasible only once the write path is named** (N2 above, fix 2).
- **F17 = B1 after bounded-waits merges: feasible for `session_context.py` / `test_session_context.py`, but incomplete.**
  - Bounded-waits r2 (owns at lines 330-395) also owns `tools/journal_write.py` as a live edit. B2 delivers
    `journal_write.py.next` as a byte copy of the integration base. This is safe only because commit #1 differs from its base
    in comment lines 58 and 422, so git's three-way merge combines both. State that, so that nobody "re-places" a stale copy
    over a merged file.
  - Bounded-waits also owns `.claude/skills/session-handoff/SKILL.md`, which Card A owns too (24, 56). B1's DoD runs
    `test_compact_snapshot.py`, which bounded-waits owns.
  - §7 step 3 says B1 runs "on top of commit #1", but the integration branch was cut before bounded-waits. Unless the Lead
    first merges origin/main into the integration branch, B1's base lacks the placed `session_context.py` that F17 names as
    its base.
  - Fix 6.

## Plan-gate lines (rule 24, held to this re-review's scope)

- Q13(a) EDGES: the new edges from r2 are stated. The silent ones are the loader typo case (fix 4) and the
  uncommitted-review-state case of the border (fix 2).
- Q13(b) MEANING: `reviewed:<sha>` means "the head the critic reviewed". As worded, nothing can write it (fix 2).
- Q13(c) PREMISES: spot-verified, one per blocker (table above). One premise is wrong: the precedent hash (fix 3). r2's base
  da47f648 is stale (main is now 69f6272f), but the measured values did not move.
- Q13(d) READERS: B3's readers of the cut are covered only in part by B2's DoD (fix 5).
- Q13(e) FORKS: all seven Lead decisions were checked above. None is contradicted by the spec's evidence once fixes 1-8 are
  in.
- Q4 CLASS COMPLETENESS: axis 31 is now complete for the items reviewed: critic.md pointers, the COORDINATOR.md row, the
  wording. Axis 2 should read "queued", not "covered" (fix 3).
- Q6 DUPLICATION: none found in scope. Grepped: importers of `dispatch_manifest`, importers of the three live-edit B2 files,
  and `main_documents`. The `COORDINATOR_FILES` vs BOOT.md double list is closed by e17.
- Q12 ONE ROAD: `facts_check` takes the unknown → note + pass road of its sibling `handoff_folder_check` (§11), which is one road
  for both header checks. No exclusion of a case from a shared mechanism.
- Tests (rule 20): plan gate. The cards ask for table rows in existing test files (B2 behaviour 4-5, B1 edges), consistent with
  `docs/TESTING.md`. No volume question at plan stage.
- Note, not a finding: K-STALE's regexes use `\s+`. A wrapped stale citation ("CLAUDE.md⏎ rule 3") is caught only if B1 matches
  over the whole file text rather than line by line, as git grep does. It is worth one line in B1 behaviour 6.

## Fixes (Lead text edits to r2 before the cards go out)

1. **N1 / F12'.** Widen the counter. Add line-start `return\b|raise\b|break\b|continue\b|yield\b|with\b|assert\b|del\b`, and a
   mid-line `\bfor\b` (comprehension) to the anywhere list. Widen the write list with `json\.dump|\.unlink\(|os\.(remove|replace|rename|makedirs)|shutil\.|subprocess\.|\.mkdir\(|\.touch\(`. Alternatively, rewrite line 227 to name what only the Q-walk catches, and weaken the invariant at line 225 to match.
2. **N2 / F16 + F15.** Name the write path. The Lead puts `reviewed:<sha>` as the first token after the model label in the
   critic Agent call's `description` (for example `opus: reviewed:69f6272f re-review …`), because `journal_hooks.cut_notes`
   builds the `delegated` notes from `description` and cuts at 300 characters. A missing or cut token means `nobase`. Also
   state the uncommitted case: either the Lead commits the reviewed state before each critic dispatch, or every fix round of
   an uncommitted review is `nobase`. That includes both topics of this spec under §7.
3. **F8'.** Cite 9616b6f4, not 1f165a38. Write axis 2 as `queued -- exam not run after the critic.md edit; debt F3-1
   (plans/piles/onboarding-forge/batch-2-onboarding-roles-forge-p3.md:67)`.
4. **F5-r.** One rule for the loader: any `*_PATH` variable whose value ends in `.py.next` must name an existing file, or the
   test session fails loudly, naming the variable. Variables naming `.py` are ignored. Make §7 line 356 and Card B2 behaviour 5
   say the same thing.
5. **B3 test resolution.** Card B2's DoD, and the Lead's post-placement re-run in §7 step 2, add the other cut readers:
   `tools/test_dispatch_cut.py`, `tools/test_dispatch_gate_md.py`, `tools/test_owns_gate.py` and `tools/test_handoff_gate.py`.
   `facts` joins the cut's header vocabulary, and these tests import `dispatch_manifest` or `dispatch_gate`, so without them a
   regression shows first in the batch canon.
6. **F17.** §7 step 3 starts with the Lead merging origin/main (after bounded-waits) into the integration branch, and B1 runs
   on that. F17 also names the other overlaps and how each resolves: `journal_write.py` (git merge; the copy differs in comment
   lines only, never re-placed after the merge), `session-handoff/SKILL.md` (Card A, line-level merge) and
   `test_compact_snapshot.py` (B1 runs it).
7. **F1' / B5.** Name the move that replaces «owner word pending» in the axis-31 row with the owner's word and its date:
   the Lead, in commit #2, before `wave.py merge`. k2's `owner word pending` key is then a pre-merge key only. Also state what
   happens on a refusal: the topic stops before the merge, and B2's F13 and the §5 texts need a new home.
8. **N8.** §9 M1(a): BOOT after the split ≈ 117.1 KB (measured estimate, this review), headroom ≈ 2.9 KB.

## Trail

- Read: t-1174 verdict (whole). r2: 1-140, 140-364, 364-512 and 512-637 (whole, by sections). r1 was not re-read; the r2
  revision table and the t-1174 text were enough to compare. critic.md 190-194 and 279-288. `.githooks/pre-commit` (gate
  lines, 40-61). `test_role_carriers_one_owner.py` 268-290. SIBLING_MAP axis-31 header (481-484). `journal_hooks.py` 41,
  62-69, 256. Bounded-waits r2 owns (330-395). The batch-3 forge and onboarding-forge batch-2 rows F3-1. The bodies of commits
  9616b6f4 and 1f165a38.
- Greps (each with a positive control): `CLAUDE.md` citations in the four role files (critic 66/178/198/281/286; builder
  67/107/116/117; designer 17/24/32; scout none). Hook and import reach of `judge_calib_sanitize|calibration_counts|dispatch_new`
  (none; control: `import dispatch_manifest` → 12+ files). Import form in the four B2 test files (plain `import`). Designer
  dispatches in neighbouring tests (test_dispatch_cut, test_handoff_gate and test_owns_gate concern the `designer:` header or
  handoff_gate, not designer-kind dispatch_gate refusals). `reviewed:` handling in journal_hooks and journal_validator (0
  hits). `NOTES_MAX` (300). `owner word|pending|SIBLING_MAP` in `tools/wave.py` -> 2 hits, both the CI state (89, 96):
  no owner-word check on the merge.
- Run (the one measurement, output above): an inline python script over `git show origin/main:` blobs, plus
  `python -B tools/session_context.py </dev/null`.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "B1-B5 of t-1174 all answered; axis 31 complete for the reviewed items (critic.md pointers 178/198/281 retargeted, 286 valid under (d), COORDINATOR.md axis-31 row read by main_documents). Axis 2 should read queued, not covered (exam not run, debt F3-1 live in onboarding-forge batch 2). Cut readers outside B2 DoD (test_dispatch_cut, test_dispatch_gate_md, test_owns_gate, test_handoff_gate) are the uncovered siblings of the facts header change. F17 overlap list incomplete (journal_write.py, session-handoff SKILL.md, test_compact_snapshot.py).",
  "fixes": [
    "N1/F12': widen the border counter with line-start return/raise/break/continue/yield/with/assert/del, mid-line for (comprehension), and write calls json.dump/unlink/os.remove|replace|rename|makedirs/shutil/subprocess/mkdir/touch; or narrow the stated error direction and invariant to what the counter catches",
    "N2/F16+F15: the reviewed:<sha> token goes as the first token after the model label in the critic Agent call description (journal_hooks.cut_notes builds delegated notes from description, cut at 300 chars); missing or cut token is nobase; state the uncommitted-review case (commit before the critic dispatch, or nobase), which covers both topics under section 7",
    "F8': cite commit 9616b6f4 not 1f165a38; axis 2 line becomes queued with debt F3-1 at plans/piles/onboarding-forge/batch-2-onboarding-roles-forge-p3.md:67",
    "F5-r: one loader rule in section 7 and Card B2 behaviour 5: a *_PATH value ending .py.next that names a missing file fails loudly; .py values ignored (a silent ignore gives a false-green copy witness)",
    "B3: Card B2 DoD and the Lead post-placement run add tools/test_dispatch_cut.py, tools/test_dispatch_gate_md.py, tools/test_owns_gate.py, tools/test_handoff_gate.py",
    "F17: section 7 step 3 begins with the Lead merging origin/main (after bounded-waits) into the integration branch; name the journal_write.py, session-handoff SKILL.md and test_compact_snapshot.py overlaps and their resolution",
    "F1'/B5: name who replaces owner word pending with the owner's dated word (Lead, commit #2, before wave merge) and what happens on refusal",
    "N8: section 9 M1(a) BOOT after split about 117.1 KB measured estimate, headroom about 2.9 KB"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/reviews/t-1174-worker-boot-plan.md whole",
      "docs/tasks/specs/20261117-worker-boot-and-round-rules-spec-r2.md 1-637 by sections",
      ".claude/agents/critic.md 190-194, 279-288",
      ".githooks/pre-commit 35-61",
      "tools/tests/test_role_carriers_one_owner.py 268-290",
      "docs/SIBLING_MAP.md 481-484",
      "tools/journal_hooks.py 41, 62-69, 256",
      "docs/tasks/specs/20261117-bounded-waits-mechanism-spec-r2.md 330-395 owns",
      "plans/piles/forge/batch-3-exam-debts.md F3-1; plans/piles/onboarding-forge/batch-2-onboarding-roles-forge-p3.md:67",
      "git show -s 9616b6f4, 1f165a38"
    ],
    "reruns": [
      {"command": "inline python size script over git show origin/main blobs + python -B tools/session_context.py </dev/null", "result": "origin/main CLAUDE 51953 PROJECT 36026; r11 6975 hyg 4386 enf 340 trim 245 lang 1167 cwd 911 s5 2841; live BOOT BUDGET 112646/120000, CLAUDE.md 51953/58500 incl. imports 101738; est new CLAUDE 14732 COORD 43357 PROJECT 34368 BOOT 117124 WARN 17000"},
      {"command": "grep -o CLAUDE.md citations in .claude/agents/{critic,builder,designer,scout}.md", "result": "critic 66,178,198,281,286; builder 67,107,116,117; designer 17,24,32; scout none"},
      {"command": "grep settings.json/.githooks and tools imports for judge_calib_sanitize|calibration_counts|dispatch_new", "result": "no hook reach; importers are tests only; control import dispatch_manifest finds 12+ files"},
      {"command": "git show -s 9616b6f4 | grep Deviation", "result": "Deviation: exam not run; debt F3-1. (1f165a38 carries Deviation (F-A1-2) instead)"}
    ]
  }
}
```

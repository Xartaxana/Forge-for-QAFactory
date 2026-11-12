# t-169: critic re-review, onboarding-forge/1, streams "hooklib" (097968a) and "doctor" (34ec7ae)

Reviewer: critic (Opus), 12.11.2026. This is one pass for both streams (R13-g). The inputs were the fix diffs plus the verdicts
t-141 and t-152. The verdicts below are inputs to acceptance. The decision belongs to the coordinator of the proper tier.

**hooklib: ACCEPT. 0 blocking findings.** A0 is closed and the accept door is legitimate. A1-A3 are still open, but they are
Lead queue actions, not builder work (see below).
**doctor: ACCEPT WITH FIXES. 0 blocking findings.** D1-D6 and D7a are closed. Two non-blocking fixes remain (N1, N2). D7b is
still open and belongs to the Lead. The byte headroom is now 4 B (N3, a Lead queue item).

---

## Stream hooklib: 097968a (t-133 attempt 3)

### A0: is the accept door legitimate here?

Yes. I checked the facts behind it myself, as follows.

- **Net-zero claim, verified.** `git diff --stat origin/main...wip/of-hooklib -- ai-packages/qa-factory/scripts/tests/` shows
  exactly one file, `test_cost_capture_settled.py | 104 +-` (a keep row). The same diff restricted to the two quarantined files
  `test_cost_capture_nonfactory_summary.py` and `test_factory_dashboard_joins.py` is empty (rc=0). Nothing reaches `main` in a
  quarantined file, so TESTING.md's rule that a quarantined file is "not edited" holds in substance. Only the intermediate
  history touched those files.
- **The commit is empty, verified.** `git show --format= --name-only 097968a` lists no files. `097968a^{tree}` and
  `b1875b4^{tree}` are the same tree (`c42ddc0a...`). So every closure in t-152 Part A (B2, B3, F4, F6, F8, F9) and its
  159/159 re-run applies unchanged. No code moved.
- **The door does what the check needs (traced).** In `tools/test_quarantine.py`, `check_history`:1728-1731 drops a found
  item when any LATER commit carries `_DOORS["accept"]` (`^quarantine-accept:\s*([0-9a-fA-F]{7,40})\s*--\s*\S`, re.M), matched
  by `sha.startswith(prefix)`. I ran that regex over the actual 097968a message. It extracted `['b898935','f99b9f3','b1875b4']`,
  and the prefix test was True for the full shas b8989353, f99b9f37 and b1875b4b. The control `deadbeef` was False.
  097968a is a child of b1875b4, so it sits in `commits[i+1:]` for all three. 097968a touches no file, so it produces no found
  item of its own. t-152 recorded all 5 violations as "quarantined file ... changed" items on exactly those three shas, so
  none survives. That is consistent with the attached `0 violation(s) rc=0`. I did not re-run the check (about 20 min). The
  git and regex evidence above replaces it, as the dispatch preferred.
- **Scope of the accept is acceptable.** An accept line clears EVERY found item of the named commit, not just the quarantine
  edit. In t-152 the only items on those shas were the five "quarantined file changed" lines, so nothing else is hidden.
- **The alternative (squash) was not necessary.** The accept door is the check's own named door ("or a later commit line
  quarantine-accept"), and its reason lines are true.

**Integration caveat (not a finding, an instruction for the integrator):** the accept lines name shas. If the stream reaches
`pile/onboarding-forge/batch-1` or `main` by rebase or cherry-pick, b898935, f99b9f3 and b1875b4 get new shas, the accept lines
name dead shas, and the 5 violations come back on the rewritten commits. Converge with a merge commit, which keeps the shas, or
squash the whole stream, which gives one commit with no net touch and needs no door.

### A1-A3 status (from t-152)

| item | status | evidence |
|---|---|---|
| A1 `recover_codex_usage.py:32` literal set `{'doctor','onboarding','story'}` | **open, not queued** | Unchanged in the worktree (line 32 read) and on main (grep). Case-insensitive grep of `plans/piles` for `recover_codex_usage` finds nothing, so no node or finding carries it. |
| A2 SIBLING_MAP axis 10 row | **open** | `docs/SIBLING_MAP.md:256` is byte-identical in the worktree and on main. It still says OH3-37 is queued, "cost_capture is NOT established", and "factory_dashboard ... not run". |
| A3 F5 / F7 nodes | **open, not carried** | Grep of `plans/piles` (case-insensitive) for `not_a_project_text` and "install_smoke --report на голом" finds nothing. Batch 1's row OH3-37 (:34) still reads "ожидает" with the original text. The only carrier is still the narrative snapshot. |

These were Lead queue actions in t-152, not builder fixes, so they do not block the stream's merge. Batch 1 is taken, so it is
frozen. Under PROJECT.md «Командная работа» p. 2 and p. 9 each item must therefore become a finding file plus a row in an untaken
onboarding-forge batch, with an owner, before batch 1 can close. A3's node contents are as t-152 specified (F5: a non-refusal
direction; F7: one hooklib builder with the ancestor hint and an extra door). A1 is a one-line fix (`kind not in
REAL_FACTORY_TYPES`) and can instead ride in any later stream that owns the file.

### Standing lines (hooklib)

- DUPLICATION AND CONSISTENCY: no new code, so nothing new. The duplicates still open are those of t-152: A1 (a third literal
  copy of the set) and F7 (two refusal builders). Grepped: `recover_codex_usage|not_a_project_text` over `plans/piles`
  (case-insensitive). Positive control: the same search found the known `t-152` mentions in `plans/piles/live-run-fvf`.
- CODE QUALITY: none found. The commit is empty, and its message is accurate (`axes: not a mechanism`, `architecture: none`
  are correct for a message-only commit).
- ONE ROAD: no change. The door used is the check's own single door.

---

## Stream doctor: 34ec7ae (t-149 attempt 2)

### Closure of the t-152 Part B findings

| finding | closed? | evidence |
|---|---|---|
| D1 | yes | SKILL.md:99 now says `phases/repair.md`, section "Does the pre-tool guard". repair.md:47 is `## Does the pre-tool guard still parse this host's events?`, which is a prefix match. The pointer names the section, not a position, so it also survives a future reorder. |
| D2 | yes (one wording nit: N2) | Row 6a no longer names `controller.py`. Step 4 prints `STALE ACTIVE STATE AFTER CLOSURE` "without its command" (:193-194). Row 6 adds "in plain words - never a script name", which answers my row-6 question. The remaining `controller.py` hits (:41 writes sentence, :316 never-list) are the doctor's own description of what it runs, not printed text. |
| D3 | yes | :293: "(FACTORY NOTES is not: READINESS counts its rows)". The anchor "No third bucket" is kept. `selftest --limits` role-rules PASS. |
| D4 | yes in SKILL.md and README; **eval 4 half-done (N1)** | Opening (:38) names step 2b's sample ticket. README:65-67 does too. Never-list :311 ("its questions are those of the opening section") is consistent again. Eval 4's assertion `dashboard-is-only-write` is updated, but its `expected_output` (evals.json:59) still says "asks only the questions after its report (archive offer, is anybody working on this story, price table)". |
| D5 | yes | :40: "the guard-probe file and a release's words file (Write serves only these two)". This agrees with never-list :313 and repair.md:39 (`qa-factory/artifacts/<TICKET>/state/words/<name>.txt`). |
| D6 | yes | `project_gitignore.py ... --check` now sits in its own fence (:178-180) behind "If `qa-factory/config.json` exists in the current directory, run:" (:176). That is word for word the step-2 form at :107 (one road). A pre-onboarding paste of the first fence can no longer produce the `--check` listing. The deleted reason "(before that the block is onboarding's)" is acceptable to lose. |
| D7a | yes | repair.md:77 "Step 1's smoke, on Codex in code mode: print ..." (the duplicate words are gone). |
| D7b | **open (Lead's)** | `docs/tasks/specs/t-144-doctor-oh3-6-12-7.md`: last commit e950d58 (the draft), no working-tree change, and no `t-146`/`t-152`/"fix round" mention (grep). The `designer:` carrier still disagrees with what was built. |
| D7c | settled by D1's choice | The section is now named, not positional, so where it sits no longer matters. |

### Non-blocking fixes

**N1 (D4 residue, FR-10 within one eval): eval 4's `expected_output` contradicts its own assertion.** evals.json:59 still says
"asks only the questions after its report (archive offer, ..., price table)". The updated assertion (:64) says "plus the sample
ticket of step 2b, asked once before it". Failure scenario: a grader comparing a run with `expected_output` marks a correct
answer that names the 2b question as a deviation. Fix: in :59, after "price table", add "; plus, once before it, step 2b's sample
ticket when no story supplies one". evals.json is outside the SKILL.md byte cap.

**N2 (printing rule 1, :283): row 6a's next action still carries a plugin path.** :247 reads "the stale tail of `<T>`: the doctor
repairs it (`phases/repair.md`, which asks first)". The column is "Next action", and :283 forbids "a factory script, flag or
plugin path" to the person. This wording came almost verbatim from my own t-152 D2 suggestion, so the defect is partly mine. The
person's actual action here is repair.md's closed question. A byte-neutral wording: "ask \"is anybody working on `<T>`?\", then
repair per `phases/repair.md`". The quoted part is what the person reads. The tail is the doctor's instruction. Low risk, but it
costs nothing to fix.

**N3 (Lead queue, budget): SKILL.md is at 18,996 / 19,000 B (raw = LF, my control), so headroom is 4 B.** The follow-up nodes that
edit this file (OF1-4, OH1-9, and the axis-5 siblings' carriers if they touch it) now have no room. t-146 and t-152 both
recommended that the Lead pre-approve relocating the stray `# Evidence capability checks` H1. It is still at the file's tail
(:320), about 174 B. That approval is now a precondition of the next doctor node, not an option. Any N2 wording must be
byte-neutral.

### Standing lines (doctor)

- DUPLICATION AND CONSISTENCY: D1, D3 and D4 are resolved in SKILL.md and README. One residue remains in eval 4 (N1). The
  STALE line and row 6a now agree, and the step-3 gate uses the same predicate sentence as step 2. Grepped in the worktree:
  `exists in the current directory` (hits :107, :176; identical form), `controller.py|questions are those|third bucket|sample
  ticket` over SKILL.md (hits :38, :41, :149, :292, :311, :316, each judged above), `words` over repair.md/SKILL.md/evals.json.
- CODE QUALITY (text): line :40 is now long (about 150 chars), cosmetic only. "The first two take no `--next`" (:183) still
  reads correctly because the first fence holds exactly two commands. The stray H1 at the tail is pre-existing (N3).
- ONE ROAD (P31): D6 aligns step 3 with step 2's form. No language, project or case exclusion was introduced.
- AR walk of the commit: AR-9 holds once N2 is applied (it holds in substance now: no script is named). AR-11 holds (Write is
  bounded by text, per F2-A). AR-28 holds (READINESS counts FACTORY NOTES rows, and the clause is explicit). `judgment: none`
  agreed.

### Class completeness

- hooklib: unchanged since t-152. The CD1-11 predicate is unified at four readers. A1 (the recovery literal), A2 (axis 10 row)
  and A3 (F5/F7 nodes) are not yet carried by any batch row (Lead).
- doctor: the same-artifact sweep of D2 now covers verdict rows 6 and 6a and step 4's printed line. The remaining class
  instance is N2 (a plugin path in the same column). D4's carriers are SKILL.md opening, never-list, README and eval 4, and all
  are fixed except eval 4's `expected_output` (N1). Axis 5 sibling skills: still queued per spec §6 (as in t-152).

## Trail

Read: t-152 verdict (whole); t-141 verdict (whole); `git -C of-hooklib log origin/main..wip/of-hooklib`; `git show -s 097968a`
(the whole message); `tools/test_quarantine.py:1667-1756` (of-hooklib copy) and `:1513-1522` (doors via grep);
`recover_codex_usage.py:28-36` (worktree) and the main grep; `docs/SIBLING_MAP.md:256` (worktree and main); grep of `plans/piles`
for A1/A3 carriers; batch-1 row OH3-37; `git show 34ec7ae` (all 4 files); of-doctor SKILL.md :36-42, :228-300, :305-322,
headings of repair.md, README.md :55-68, evals.json :59 and the assertion diff; git log/status of spec t-144.

Re-runs (verbatim):
- `git diff --stat origin/main...wip/of-hooklib -- ai-packages/qa-factory/scripts/tests/` -> ".../scripts/tests/test_cost_capture_settled.py | 104 ++++++++++++++++++++- / 1 file changed, 103 insertions(+), 1 deletion(-)".
- The same diff restricted to the two quarantined files -> empty, rc=0.
- `git show --format= --name-only 097968a` -> "files:[]"; `rev-parse 097968a^{tree} b1875b4^{tree}` -> both `c42ddc0a54d9b15c411a000ae0da79e9f42a800a`.
- The accept regex from test_quarantine.py:1520 over the 097968a message -> "['b898935', 'f99b9f3', 'b1875b4']", then "b8989353 True / f99b9f37 True / b1875b4b True / deadbeef False".
- SKILL.md bytes at 34ec7ae: "18996 18996" (raw / CRLF->LF).
- `( cd <of-doctor>/ai-packages/qa-factory && python -B scripts/selftest.py --limits --lang )` -> "PASS limits: SKILL.md / agents / references within size caps / PASS limits: every mandatory role rule of design/role-rules.json holds in its carrier / === qa-factory selftest: 4/4 ok ===".
- Not re-run: `tools/test_quarantine.py check` (about 20 min; replaced by the git and regex evidence, as the dispatch preferred), and test_cost_capture_settled, scenario_walk and scenario_world. The tree is identical to b1875b4, where I re-ran settled 159/159 in t-152.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "N1 (doctor, D4 residue): evals.json:59 expected_output of eval 4 still says the doctor asks only the three questions after its report; add step 2b's sample ticket asked once before it, matching the updated assertion and SKILL.md:38",
    "N2 (doctor, printing rule 1): SKILL.md:247 row 6a next action carries the plugin path phases/repair.md; make the person-facing part repair.md's closed question (ask: is anybody working on <T>?) with the path as the doctor's own instruction, byte-neutral",
    "N3 (Lead queue): SKILL.md at 18996/19000 B, headroom 4 B; pre-approve relocating the stray Evidence capability checks H1 (about 174 B) before the next node that edits the doctor (OF1-4, OH1-9)",
    "D7b (Lead): record the t-146/t-152 binding fixes in spec t-144 or the node rows; spec unchanged since draft e950d58",
    "A1-A3 (Lead, from t-152, still not carried): recover_codex_usage.py:32 literal set; SIBLING_MAP axis 10 row :256 stale; F5/F7 nodes; each becomes a finding plus a row in an untaken onboarding-forge batch before batch 1 closes",
    "Integration (hooklib): converge wip/of-hooklib by merge or full squash, not rebase or cherry-pick, otherwise the quarantine-accept lines name dead shas and the 5 violations return"
  ],
  "class_completeness": "hooklib: A0 closed by the check's own door; net branch diff on both quarantined files empty; commit empty (tree equals b1875b4) so the t-152 closures of B2, B3, F4, F6, F8, F9 stand; A1, A2, A3 remain uncarried Lead queue items. doctor: D1-D6 and D7a closed; the D2 sweep now covers rows 6, 6a and step 4, with one residue in the same column (N2); D4 carriers fixed except eval 4 expected_output (N1); D7b open (Lead); axis 5 siblings queued per spec section 6.",
  "trail": {
    "read": [
      "docs/tasks/specs/reviews/t-152-of1-rereview-and-doctor.md",
      "docs/tasks/specs/reviews/t-141-of1-hooklib-critic.md",
      "git show -s 097968a (message)",
      "of-hooklib tools/test_quarantine.py 1513-1522, 1667-1756",
      "of-hooklib ai-packages/qa-factory/scripts/recover_codex_usage.py 28-36",
      "docs/SIBLING_MAP.md:256 (main and of-hooklib)",
      "plans/piles grep for recover_codex_usage, not_a_project_text, install_smoke bare-root node",
      "plans/piles/onboarding-forge/batch-1-onboarding-roles-forge.md row OH3-37",
      "git show 34ec7ae (README.md, SKILL.md, evals.json, repair.md)",
      "of-doctor skills/qa-doctor/SKILL.md 36-42, 228-300, 305-322",
      "of-doctor skills/qa-doctor/phases/repair.md headings and lines 35-39",
      "of-doctor skills/qa-doctor/README.md 55-68",
      "of-doctor skills/qa-doctor/evals/evals.json:59",
      "git log and status of docs/tasks/specs/t-144-doctor-oh3-6-12-7.md"
    ],
    "reruns": [
      {"command": "git diff --stat origin/main...wip/of-hooklib -- ai-packages/qa-factory/scripts/tests/", "result": "1 file: test_cost_capture_settled.py, 103 insertions, 1 deletion"},
      {"command": "git diff --stat origin/main...wip/of-hooklib -- the two quarantined files", "result": "empty, rc=0"},
      {"command": "git show --format= --name-only 097968a; rev-parse trees of 097968a and b1875b4", "result": "no files; both trees c42ddc0a54d9b15c411a000ae0da79e9f42a800a"},
      {"command": "accept regex of test_quarantine.py:1520 over the 097968a message", "result": "b898935, f99b9f3, b1875b4 extracted; prefix match True for b8989353, f99b9f37, b1875b4b; control deadbeef False"},
      {"command": "byte count of of-doctor SKILL.md at 34ec7ae", "result": "18996 raw / 18996 LF"},
      {"command": "selftest.py --limits --lang (of-doctor package cwd)", "result": "4/4 ok; size caps PASS; role-rules anchors PASS"}
    ]
  }
}
```

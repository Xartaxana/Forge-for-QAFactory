# t-1164 — code critic, "no briefs" wave 2 (N7-L cd018f24 + N7 fc241060, 6d33e385)

Base `1f552166`, head `6d33e385`, worktree `.claude/worktrees/nobriefs-n7`. Judged against spec r2 §4.5, §11 Wave 2, §12 E16
and critic.md rule 22.

**Verdict: NEEDS WORK** — no blocking findings; 3 findings to fix before the merge (F1 is the Lead's, on a mechanism path; F2-F3 go to the
builder's fix round). Accepting the work is the coordinator's call (rule 6).

## Answers to the dispatch's questions

1. **Is anything of exchange-form lost?** Yes, a little (F1). Every section in the §4.5 table has its home: the flag table and the note after it
   are in scout.md rule 11, the grammar sentence too, the example is the fixture, the brief form is in CLAUDE.md rule 11, the intro and the t-795
   example are dropped as the spec says, and the prose-count definition from §2 lives in `hop_metrics.prose_lines` and check 34(b). But §4.5's
   premise that "rule 10 already carries ... id, gist, status, ev" is only partly true. The Objects-column meanings at exchange-form :26-30 and
   the `## Not done` meaning at :15 are now nowhere in scout.md. One of them, the `ev` separator and its case, is a requirement the reader
   judges.
2. **Is the copy verbatim?** Yes. scout.md rule 11 with its 3-space indent stripped, lines 5-33 vs `1f552166:docs/tasks/exchange-form.md`
   :51-79: `diff` is empty. Fixture vs :81-130: `diff` is empty. Neither file has a CR. Declared deviations, both acceptable: (a) the :49
   heading became the rule title, with the `first=<flag>` clause from §4.5 added (the Lead's decision, written in cd018f24); (b) the grammar
   sentence writes `n >= 1` where §4.5 writes `n ≥ 1`. That matches the original file's ASCII and the table, so it is not a finding.
3. **Are the CLAUDE.md rule 11 sentences as the spec wrote them?** Yes. Programmatic check: after normalizing whitespace, the spec's three
   sentences appear in `6d33e385:CLAUDE.md` exactly, right after "is NOT a DoD." (True/True). AGENTS.md is fresh: `agents_md.py --check` →
   "up to date (111314 bytes)".
4. **Is any live reader of the deleted path left?** None outside history files. `git grep -i "exchange-form|exchange_form|exchange form"` on
   6d33e385, excluding specs, handoffs, snapshots, logs and piles, finds only the K-NOBRIEF row (`test_role_carriers_one_owner.py:262`, the
   intended pin) and `WEEKLY_CALIBRATION_PROTOCOL.md:1047` "Exchange form (F5-2)", which is a title with no path and no stem match. The piles
   have hits only in `forge/batch-5` and `batch-6`, both `статус: закрыта`, plus one finding file. Those are records.

## Findings

**F1 — the scout no longer sees reader-judged column requirements (fix before merge; the Lead, scout.md rule 10; also a finding against spec §4.5).**
exchange-form :29-30 said "`ev` -- the tids ..., comma separated, exact case; `—` or empty means NO trail". At 6d33e385, scout.md rule 10 says
only "`ev` lists the tids". Grep -i over scout.md for `comma|exact case|owner|from-to|not done` hits only `id` (:95), the header (:94) and flag
rows. The positive control is the :95 hit itself ("no spaces or commas"). Probe through `digest_form.parse/flags` in the worktree:
- `ev` = `R1 R2` → `['ev_unknown:q1:R1 R2']`
- `R1,R2` → `[]`
- `r1,R2` → `['ev_unknown:q1:r1']`

So the reader judges a separator and a case that the scout is told nowhere except by imitating the fixture. That is FR-38 / AR-10's class: the
requirement must reach the role before the work. Rule 10's own pointer cites FR-38 as the reason the flag table moved, yet these requirements
did not move with it. Also lost, though not judged by code: `paths` (`path:line` or `path:from-to`), `owner` (the owner's word or `—`), `links`
(ids, B-ids, `file:line` of a carrier), `kind` (a free word the reader does not check), and `## Not done` ("what was not checked and why").

Fix: one sentence in scout.md rule 10 after the `ev` clause, taken from exchange-form :15, :26-30: "`ev` is comma separated, exact case (`—`
or empty = no trail); `paths` is `path:line` or `path:from-to`; `owner` is the owner's word or `—`; `links` are ids of other objects, B-ids or
the `file:line` of a carrier; `kind` is a free word the reader does not check; `## Not done` says what was not checked and why." That is about
+350 bytes. The commit carries the same Deviation line and `tier: opus`. The flag-name pin is unaffected.

**F2 — annotations that now lie (fix before merge; builder, files in N7's owns).**
- `tools/test_handoff_rule_anchors.py:142-143`: the docstring still says rule 10 carries "the key line of the form and the note that holds its
  grammar". K_SCOUT_FORM's second key is now `` `tools/digest_form.py` `` (the reader), and the note is deleted.
- `tools/test_digest_form.py:76`: the comment says "the example of the note"; it is now the fixture.
- `tools/test_digest_form.py:114`: "against the note"; it is now scout.md.
- `tools/test_digest_form.py:119`: the variable `note = SCOUT.read_text(...)`.

The two test NAMES that contain "note" are named by the spec's DoD and stay. Also, `digest_form.py:39` now says "scout.md rule 11 must carry
every FLAG_NAMES entry" while the test reads the whole scout.md. This is the same reach as before (the whole note), and today every flag name
occurs only in rule 11, so it is noted, not a finding.

**F3 — tests over the volume rule with no `tests-over:` line, and an undeclared red commit (fix before merge; builder or the coordinator's
squash).**
- TESTING.md:206-207 requires the line when test lines exceed product lines. The hook counted +61 test vs +5 product, and neither N7 commit
  carries a `tests-over:` line.
- The reason itself holds: the 50 fixture lines are exchange-form :81-130 moved verbatim (the file's 156 doc lines are deleted), and no new
  test or row was added.
- fc241060 is titled "fold exchange-form into scout.md rules 10-11 and a t-794 fixture", but it contains only the deletion. Traced: at
  fc241060, `test_digest_form.py` is byte-identical to the base and reads `NOTE = docs/tasks/exchange-form.md`, which is gone, so every test
  calling `example_block()` fails with FileNotFoundError. Unlike cd018f24's two declared reds, this red is undeclared.
- E16's invariant (main never holds a test reading a missing file) still holds, because one merge brings the whole branch.

Fix: squash fc241060 into 6d33e385 as one N7 commit that carries `tests-over: the t-794 example moved verbatim from the deleted
docs/tasks/exchange-form.md (-156 doc lines); no new test`. If the branch must not be rewritten, a fix-round commit carries that line and the
journal note names the fc241060 red.

## Standing questions (rule 22)

- **Q1 Fit to the spec:** fit, except F1, which is against §4.5's premise.
  - Every N7 transformation in §11 was checked line by line: fixture, FIXTURE, SCOUT, the PI_HARNESS wanted entry, docstring :5,
    digest_form :13/:39, handback_extract :37, the PI_HARNESS sentence, K_SCOUT_FORM, DELETED with its stale "wave 2 adds" comment removed, and
    `git rm`.
  - N7-L was checked too: the rule 10 parenthetical, rule 11, SIBLING_MAP :35/:343/:486 and row :505 removed, the Deviation line, `tier: opus`.
  - E16 holds for main.
- **Q2 Builder's own decisions:** dropping the DELETED comment is safe. No other silent points were found.
- **Q3 Seams:** additive. The base 1f552166 carries wave 1 (DELETED already listed the six files). Nothing was reordered.
- **Q4 Class-wide completeness:** the digest-form trio (axis 1, SIBLING_MAP :35) has all three carriers re-pointed. The other readers were
  walked: handback_extract, PI_HARNESS (axis 2), hop_metrics (no path), check 34 (no path), the :343 consumers row and the :486 axis-31 row.
  Same-artifact sweep of SIBLING_MAP: :35 applied, :343 applied, :486 applied, :505 removed, no other digest row. Sweep of scout.md: rules
  10-11 applied, no other rule names the note. The one residual of the class is F1, fixed in this round.
- **Q5 Tests:**
  - (a) Killing power: the K-NOBRIEF row turns red on any MAIN mention of the path or stem, and on the file being re-tracked (parametrized
    `test_deleted_files_stay_untracked`). The fixture test still pins the two flags.
  - (b) Expected values: unchanged, and they trace to the fixture text (:84 names the two flags).
  - (c) No new behaviour at a door.
  - (d) No test was deleted.
  - (e) No duplicates.
  - (f) The missing `tests-over:` line is F3. No new pins (the role-text pins already existed and were re-pointed).
  - (g) No new test file. The fixture is data under `tools/fixtures/`.
- **Q6 DUPLICATION AND CONSISTENCY:** none found. Grepped: the brief-prose target 8 (CLAUDE.md, check 34 "N = 8", the
  `hop_metrics.prose_lines` docstring — consistent); flag names (FLAG_NAMES is the one list, and scout.md holds the table once, since
  exchange-form is deleted); rules 10 and 11 overlap only on the stray-row mention (rule vs flag meaning, not a second definition).
- **Q7 CODE QUALITY:** F2 (lying annotations) and F3 (a commit message that claims content it lacks). No new functions.
- **Q8 Hygiene:** not in the package. No CR in scout.md or the fixture.
- **Q9 Ratchets:** no ratchet row touched.
- **Q10 ARCHITECTURE:** forge-only files, no AR-n carrier touched. AR-10's forge analog (FR-38) is F1.
- **Q11 JUDGMENT:** no judgment moved into code. Rule 11 adds procedure text to the scout's context (+4 395 bytes of scout.md, measured
  7101 → 11496), which is Lead decision F-R2-4 (a) with FR-38 as the reason. scout.md is not a package role, so `process_ratchet_tokens` does
  not apply.
- **Q12 ONE ROAD (rule 19):** none found. Grepped: language, project or runner names in the diff (none). Gateway scouts are taught by
  pointer to the same scout.md rules (one road, axis 2).
- **Rule 20 Tests:** F3.

## Spot-checks

- Mechanical layer re-run in the worktree at 6d33e385: `444 passed in 3.00s`. This matches the builder's 444.
- Budget: CLAUDE.md own bytes 51 490 → 51 953 (+463; §9 estimated about +450, under CLAUDE_WARN 58 500).
- `agents_md.py --check` exit 0.

## Trail

- Read: spec r2 :1-80, :340-360, :520-610, :736-960; critic.md :170-317; the diff 1f552166..6d33e385 (all files); exchange-form at
  1f552166 (all 156 lines); scout.md at 6d33e385 :80-149; test_handoff_rule_anchors.py :138-153; test_digest_form.py :76-122;
  digest_form.py :325-345; PI_HARNESS.md :56-66; WEEKLY_CALIBRATION_PROTOCOL.md :1047-1082; TESTING.md :206-207; the three commit messages.
- Commands (verbatim results):
  - `diff <(rule 11 lines 5-33, de-indented) <(exchange-form :51-79)` → empty, FLAGS-VERBATIM
  - `sed -n 81,130p ef.md | diff - fix.md` → empty, FIXTURE-VERBATIM
  - `grep -c $'\r'` scout.md / ef.md → 0 / 0
  - python containment of the spec's sentences in CLAUDE.md → True / True
  - the `git grep -i` exchange-form searches above (2 live-tree hits; piles: closed batches)
  - the digest_form ev probe (three outputs quoted in F1)
  - `pytest` (4 files) → 444 passed in 3.00s
  - `agents_md.py --check` → up to date (111314 bytes)
  - `wc -c` of scout.md: 7101 → 11496; CLAUDE.md: 51490 → 51953

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "Digest-form trio (SIBLING_MAP axis 1 :35): all three carriers re-pointed; readers handback_extract, PI_HARNESS (axis 2), hop_metrics, check 34, map rows :343/:486 walked; :505 removed; scout.md and SIBLING_MAP swept in-artifact. Residual F1 (ev separator/case and Objects column meanings not carried into scout.md rule 10) is fixed in this round, no queue.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-no-briefs-fold-into-roles-spec-r2.md :1-80, :340-360, :520-610, :736-960",
      ".claude/agents/critic.md :170-317",
      "git diff 1f552166 6d33e385 (all 12 files)",
      "1f552166:docs/tasks/exchange-form.md :1-156",
      "6d33e385:.claude/agents/scout.md :80-149",
      "tools/test_handoff_rule_anchors.py :138-153",
      "tools/test_digest_form.py :76-122",
      "tools/digest_form.py :325-345",
      "gateway/PI_HARNESS.md :56-66",
      "PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md :1047-1082",
      "docs/TESTING.md :206-207"
    ],
    "reruns": [
      {"command": "python -m pytest tools/test_digest_form.py tools/test_handoff_rule_anchors.py tools/tests/test_role_carriers_one_owner.py tools/test_handback_extract.py -q (worktree at 6d33e385)", "result": "444 passed in 3.00s"},
      {"command": "diff scout.md rule 11 (de-indented) vs exchange-form :51-79; fixture vs :81-130", "result": "both empty"},
      {"command": "python -B tools/agents_md.py --check --repo <worktree>", "result": "AGENTS.md: up to date (111314 bytes), exit 0"},
      {"command": "digest_form.flags probe with ev 'R1 R2' / 'R1,R2' / 'r1,R2'", "result": "['ev_unknown:q1:R1 R2'] / [] / ['ev_unknown:q1:r1']"},
      {"command": "git grep -i exchange-form on 6d33e385 outside records", "result": "2 hits: K-NOBRIEF row (intended), check 34 title (no path)"}
    ]
  },
  "fixes": [
    "F1 (Lead, scout.md rule 10, fix before merge): add the ev separator/case and the Objects column meanings from exchange-form :15, :26-30 (ev comma separated, exact case, dash or empty = no trail; paths, owner, links, kind; Not done meaning)",
    "F2 (builder, fix before merge): correct stale 'note' annotations at tools/test_handoff_rule_anchors.py:142-143 and tools/test_digest_form.py:76, :114, :119 (test names stay: spec DoD names them)",
    "F3 (builder or coordinator, fix before merge): squash fc241060 into 6d33e385 with a tests-over line naming the verbatim fixture move; otherwise a fix-round commit carries tests-over and the journal note names the fc241060 red"
  ]
}
```

# t-952 — critic re-pass on R5 (and R6 as far as §8.2.2 carries it), spec 20261117-everything-in-piles r3

critic (Opus), 17.11.2026. Scope: §8.2 (spec :867-952), forks F22/F23 (:1090-1095), «Lead decisions on the r3 forks»
(:1242-1249), t-943 R5/R6, boot-by-topic §4.3 (+ the sections of it that §8.2.1's amendment touches), the axis-31 test,
PROJECT.md:322-341. The rest of the spec is NOT reviewed.

**Verdict: NEEDS WORK. R5: NOT CLOSED. R6: PARTLY CLOSED** (grammar, whitespace, openers, own-line home, order: done;
the grammar now fails boot-by-topic's real targets). 6 blocking findings (B1-B6), 5 fixes (F1-F5).

What R5 asked for is in place STRUCTURALLY: one form (`rule:`/`правило:`), one resolver (`rule_pointers.resolve`),
one scan set (8.2.4), `see:`/`rule_stamps.py` gone. It is not closed because (a) the survivor's contract is changed
in a way that turns accepted boot-by-topic text red (uniqueness, B1), so "§4.3 kept whole" (:883, :939) does not hold;
(b) second readers stay in the window with no end (B3); (c) absorbing FG7-52 drops part of its scope (B4);
(d) the amendment line does not cover what it changes (B5); (e) the carrier side of the form is not defined, and the
real S2 text is red under the literal reading (B6).

## Blocking findings

**B1 (K3, K4) — the uniqueness rule + the item kind make accepted TOC cells and K's own rewrites red on day one.**
Carrier: spec :906 (item kind), :909 (0 → E31, 2+ → E32). Item kind matches after stripping whitespace, with no
scoping by section, and `### <x>` is a bare prefix.
- `CLAUDE.md § 3` (boot-by-topic §4.1 :398, "Under F19 (a) a numbered rule is cited by number (`CLAUDE.md § 3`)") →
  hits CLAUDE.md:70, :389, :413 → E32. `§ 1` → :37, :386, :409 → E32. `§ 6` → :109, :420 → E32. Boot-by-topic §3.1
  rows C-LD and C-H1..7 keep Lead degradation 1-4 and Command hygiene 1-7 numbered, so S1 does not remove the collision.
- `plans/builder-rules.md § 7b` (boot-by-topic §4.1 :394; also 8.2.3's own rewrite `RULES_7B → 7b`, :932) → the
  file (origin/main) has `### 7b. Уровень билдера и уровень пачки` (:36) AND `7b. **Уровень билдера и уровень пачки**`
  (:38); both "open with `7b.` (or `### <x>`)" → E32. Every builder-rules number is doubled the same way (`### 1.` :8
  and `1.` :10; `### 3.` :14 / :16; `### 6.` :23 / :25; `### 11.` :103 / :105) — this is the S3-2 shape t-943 R6 (v) named.
- `### <x>` has no delimiter: `<x>` = `1` also prefix-matches `### 10.` … `### 19.` (builder-rules :100-:130).
- K's DoD (spec :736, `rule_pointers.py check --staged` exit 0 on the tree) and §8.5 "nothing goes red on day one"
  (:1007) are then unattainable, and K's owns (rule_pointers.py, rule_sources.json, baseline, the test) cannot edit
  CLAUDE.md / builder-rules to repair it. "It errs safe" (:910) is true for FR-59 but it is a contract change.
Expected fix (in 8.2.2, and the amendment line, B5): (i) `### <x>` matches only when `<x>` is followed by `.`, space or
end of line; (ii) a `### <x>.` heading whose next non-blank line is the `<x>.` opener is ONE place (the heading's
section); (iii) ids repeated under different `##` sections: choose ONE road and write it — a scoped address
(`<file> § <heading> § <x>`), or the TOC cites S1's sub-headings / bold kind instead of bare numbers (amending
boot-by-topic §4.1 :397-398 F19 (a) wording); (iv) a row in the axis-31 test for each of the three instances above.

**B2 (K3) — heading equality against real headings: 8.2.3's own rewrite is red.** Spec :931 rewrites `## The two
layers` → `The two layers` (heading kind, "text equals `<x>`", :905). The target heading is
`## The two layers (CLAUDE.md rule 3, the two-layer review rule)` (docs/tasks/critic-diff-brief.md:8) → E31; today's
substring row passes. Same class in the accepted TOC example `CLAUDE.md § Tiers` (boot-by-topic :392) against
CLAUDE.md:21 `## Tiers (see DELEGATION_TABLE.md; all assignments are estimates until calibrated)`, while row C-T says
the heading "stays by name". Expected fix: 8.2.3 rewrites to the full heading text (or the literal kind
`"## The two layers"`); 8.2.2 states, for heading kind, whether a parenthetical tail is part of the text (today: yes,
so the TOC cells either carry the whole heading or S1 renames the heading — say which, in the amendment, B5).

**B3 (K1, K2) — second readers remain, with no stated end.**
- Boot-by-topic §4.3 item 5 (:416-417) makes EVERY TOC cell and pointer line written by S1/S2 a POINTERS row, and
  §7.3 of this spec (:758) knows the S1/S2 rows exist; 8.2.3 (:930) inventories only "the 20 hand POINTERS rows + D's 5"
  (origin/main has 20: test :54-:73). Once K lands, each S1/S2 pointer is judged twice — by its row (anchor rewritten)
  and by the scan of its `rule:` line — and their rewritten anchors inherit B1/B2. "A row disappears when K2 writes the
  matching `rule:` line" (:934) does not fire for them: the line already exists.
- For the 20+5 rows, only the ANCHOR half moves to `resolve`; the carrier half (`squash(pointer) in squash(carrier)`,
  test :133) stays a substring match on a prose phrase. "The substring rule is retired" (:935) is half true; K2 (:1012)
  has no completion condition for the `pointers` list (empty, or a named residual with a reason).
Expected fix: 8.2.3 says K DELETES every row whose carrier already holds the matching `rule:`/`правило:` line (all S1/S2
rows), in K's commit; the remaining rows carry both halves as `rule:` data (carrier line + `<x>`), or state the
substring carrier half as a named temporary form; K2's DoD ends with `pointers` empty or each leftover row listed
with why it cannot be a `rule:` line (TEMPORAL: both worlds named).

**B4 (K2) — absorbing FG7-52 drops part of its scope.** FG7-52's scope (boot-by-topic :690; batch-7-vhodyashchie-4.md:75)
is pointers + TOC cells AND "пути, диапазоны FR/P/rules и числа гейтов в текстах правил" AND "пары записаны в
`docs/SIBLING_MAP.md`"; boot-by-topic §4.3 item 5 (:417-418) also hands TOC COMPLETENESS to FG7-52. K's row (spec :736)
and 8.2.1 cover pointer resolution and TOC cells only. With the row turned `отклонено: поглощён узлом K` (:893) the
paths / ranges / gate-count checks, the SIBLING_MAP pairs and TOC completeness are dropped silently. Expected fix:
either K's row lists them (with DoD rows), or FG7-52's row is narrowed in place (not rejected) to the remainder with
its owner and an order after K, reusing `resolve`; the decision is the Lead's, the spec states one.

**B5 (K4) — the amendment line is insufficient and contradicts itself.** The line (:895-896): "FG7-52 is built inside
K …; the resolver lives in `tools/rule_pointers.py`, called by the axis-31 test — still no second checker".
- "still no second checker" vs 8.2.1 (:887-888): pointer resolution is judged by the test in CI AND by
  `rule_pointers.py check` in commit-msg — a separate tool on a hook path, which is what A1 refused ("отдельного
  `tools/pointer_lint.py` нет", boot-by-topic :690, :759-760, §1.4 :98). One resolver/two triggers is defensible, but
  the amendment must SAY A1 is amended and why (doors live in commit messages, R4), not deny it.
- Not amended although changed: §4.3 item 1 (:408-410: the bold and literal kinds, uniqueness), item 5 (:416-418
  "Until FG7-52"), §1.3 row (:81 "FG7-52 extends the scan later", :87 "on discipline until FG7-52"), §6 item 7 of the
  PROJECT.md rule text S2 writes (:498-499 "затем FG7-52 … до FG7-52"), the check 33 line (:510 "on discipline until
  FG7-52"), the §7.6 FG7-52 ready row (:690), and the F19 (a) cell wording if B1 (iii) picks it. After F23 (a) these
  live texts name a node that will never land.
Expected fix: 8.2.1 lists each amended carrier of boot-by-topic with its replacement wording ("FG7-52" → "K of
everything-in-piles"), including B1/B2's TOC decisions.

**B6 (K5, K3) — the carrier side of the form is undefined; the literal reading reds the real S2 text.** 8.2.2 defines
the target side only; `<x>` heading kind is "to end of line" (:905). Real instances boot-by-topic S2 writes into
PROJECT.md (:315-:323): `правило: \`docs/TEAMWORK.md\` § 2 (что меняется …`, `§ 3. При общем файле поздний узел …`,
`§ 8.`, `§ 9 (отказы …` — backticked `<file>`, `<x>` followed by prose / parenthesis / period. Read literally, `<x>` =
"3. При общем файле поздний узел сливает" → heading kind → E31. TOC cells (§4.1 :397) join homes with ` + ` inside
`|` cells. And S2's rule text (§6 item 1, :487) puts the PLACEHOLDER `правило: <файл> § <раздел>` (inline code) into
PROJECT.md, which is in the scan set → `<файл>` does not exist → E31. Expected fix: a carrier grammar in 8.2.2 —
what recognizes a pointer (marker + `§`), `<file>` with or without backticks, how `<x>` ends (item id: the regex match,
then a non-id char; heading: up to ` (`, `. `, ` |`, ` + `, end of line — pick and state), the kind dispatch order
(`**` → bold, quoted → literal, id regex → item, else heading), TOC cell splitting, and inline code spans holding a
placeholder (`<…>` file) not being pointers; each a row in the axis-31 test.

## Fixes (non-blocking)

- **F1** (8.2.2 :906) `FR-\d+`/`AR-\d+` item ids match no real carrier: factory-rules.md:32 is `**FR-1 — …**`,
  architecture.md:35 `**AR-1 — …**`; none of `FR-1.`, `### FR-1`, `**FR-1.**`, `- **FR-1.**`. Add the opener
  `**<id> — ` or drop the ids.
- **F2** (8.2.2 :906) an item's section ends at ANY later heading, so S1's sub-heading «### Rule 2 · drafting →
  designer» (boot-by-topic :169) cuts rule 2; a stamp on `CLAUDE.md § 2` / `§ 11` covers the first paragraph only —
  the unsafe direction for stamps. State whether `### Rule N · …` sub-headings end item N.
- **F3** (8.2.2 :907) the bold lead-in end heuristic outside the home: a wrapped sentence that starts a line with bold
  after a line ending in `.` ends the section early (unsafe for stamps). The "no wrapped line begins with `**`" text
  rule protects the home only; state it for every stamped bold section, or have `stamp` refuse such a section.
- **F4** (8.2.5 :945) silent inputs: case sensitivity of matching (§4.3 :413 "renamed by one character" must be red;
  the axis-31 test casefolds, :78); `<file>` resolved from the repo root; a target that exists but is untracked; a
  `§` written with NBSP. One line each.
- **F5** (8.2.2 :932) `6. **DUPLICATION…** → 6 scoped by uniqueness in the brief, else the bold kind` leaves a choice
  to the builder; in the brief `6.` occurs once (critic-diff-brief.md:47) — write `6`.

## Keys

- **K1** — one form, one resolver, one scan set: in design, yes. Remaining second forms/readers: the S1/S2 POINTERS rows
  (boot-by-topic :416; test file) beside the scan (B3); the substring carrier half of the `pointers` rows (test :133;
  spec :935) (B3); commit-time `check` as a second trigger of the same resolver — acceptable, mis-stated (B5).
- **K2** — `see:`/`rule_stamps.py`: retired before birth, concrete. K-PTR: by K2 with no end condition; S1/S2 rows:
  silent (B3). FG7-52: scope partly lost (B4).
- **K3** — PROJECT.md:333 today: mid-line → E31 with hint, as stated; after 5.3 (own line, 3 spaces) resolves; end
  traced at the `   **Живые прогоны…**` line (prev line :336 ends `.`) — correct. Three headings picked:
  builder-rules.md:36 `### 7b. …` (heading kind, full text: unique; item `7b`: E32 with :38); critic-diff-brief.md:8
  `## The two layers (…)` (`The two layers`: E31); CLAUDE.md:21 `## Tiers (…)` (`Tiers`: E31); plus `CLAUDE.md § 3`
  (E32, three hits). AT/BEYOND edges are stated for the home only; ambiguous id (B1), parenthetical tail (B2),
  carrier tokenization (B6) are not.
- **K4** — not sufficient, and "no second checker" contradicts 8.2.1 and A1 (B5).
- **K5** — B6 and F4.

## Duplication and consistency / code quality / one road / tests

- DUPLICATION AND CONSISTENCY: B3 (row + scan judging one pointer); otherwise none found in 8.2: grepped `FG7-52`,
  `pointers`, `ranges|диапазон|completeness` over the spec.
- CODE QUALITY: plan only, no code; n/a.
- ONE ROAD (P31): structurally one resolver; the residual second readers are B3; B1 (iii) must pick one road for
  repeated ids.
- TESTS: 8.2.2's edge rows cover the home only; B1/B2/B6 each owe rows (named in the fixes). No diff, no volume count.

## Class completeness

Surface: the pointer resolver's address grammar (target side) and the pointer recognizer (carrier side). Neighbouring
classes walked: magnitude/prefix (`### 1` vs `### 1x`, B1), duplication (repeated ids, doubled heading+item, B1),
tail/encoding (parenthetical headings B2, NBSP and case F4), nesting (sub-headings inside items F2, bold inside a
section F3), empty/broken input (placeholders in inline code, missing anchor, B6). Map axes in play: 31 (role-text
carriers — this test), 34 (one road), 1 (rule text and its checker change together — B5); not walked further.

## Not checked

The rest of the spec (§1-§7, §8.1, §8.3-§8.6, other forks); 5.3's replacement text itself (only its result as 8.2.2
describes it); `scan_extra` contents and whether F25 (a) main files under `ai-packages/` (EXCLUDED, test :24) are
scanned as carriers; boot-by-topic headings after S1 beyond what §3.1 states (S1 is not on disk); the `check --staged`
mode of K's witness vs §8.3's `--msg-file`/`--base`.

## Trail

Read: spec :860-959, :1085-1104, :1240-1249, :74-75, :736, :1005-1016 and Grep `FG7-52|pointers|ranges|completeness`;
t-943 :85-159 and Grep R5/R6; boot-by-topic :93-102, :161-195, :310-325, :383-420, :483-512, :686-697, :753-762 and
Grep `^#+ |FG7-52|A1`; PROJECT.md:318-343; origin/main of tools/tests/test_role_carriers_one_owner.py (:1-140),
plans/builder-rules.md, CLAUDE.md, critic-diff-brief.md, builder.md, critic.md, factory-rules.md, architecture.md,
delegation.config.yaml, batch-7-vhodyashchie-4.md:75. Runs (git show origin/main:<f> | grep -nE item/heading openers):
CLAUDE.md `1.` ×3 (:37 :386 :409), `3.` ×3 (:70 :389 :413), `6.` ×2 (:109 :420); builder-rules `### 7b.` :36 and
`7b.` :38, `### 1`-prefixed lines :8 :100-:130; brief heading :8 with parenthetical; factory-rules :32 `**FR-1 — `;
`scout:` once in delegation.config.yaml (:70); `Cost gates (D-0035` once in CLAUDE.md (:257).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1 s8.2.2 :906/:909 uniqueness + unscoped item kind + bare ### prefix: CLAUDE.md s3/s1/s6 (3/3/2 hits) and builder-rules s7b (:36 heading + :38 item) are E32; accepted TOC cells (boot-by-topic :394, :398) and K's own RULES_7B rewrite red on day one; K's owns cannot repair them",
    "B2 s8.2.3 :931 'The two layers' heading kind vs critic-diff-brief.md:8 heading with parenthetical tail is E31; same for TOC cell CLAUDE.md s Tiers vs CLAUDE.md:21",
    "B3 s8.2.3 :930-935 boot-by-topic S1/S2 POINTERS rows not inventoried (row + scan judge one pointer); carrier half of pointers rows stays substring; K2 has no end condition for the pointers list",
    "B4 s8.2.1 :893 FG7-52 rejected as absorbed drops its paths / FR-P-rules ranges / gate counts / SIBLING_MAP pairs / TOC completeness scope (boot-by-topic :690, :417; batch-7 :75)",
    "B5 s8.2.1 :895-896 amendment says no second checker while 8.2.1 adds commit-time rule_pointers.py check (A1 refused a separate tool); does not amend boot-by-topic s4.3 items 1 and 5, s1.3 :81/:87, s6 item 7 :498-499, check 33 line :510, s7.6 row :690",
    "B6 s8.2.2 carrier side undefined: real S2 text (boot-by-topic :315-323) has backticked file and prose after x, TOC cells use ' + ', S2 rule text :487 puts placeholder 'pravilo: <file> s <section>' into scanned PROJECT.md; literal reading is E31"
  ],
  "fixes": [
    "F1 s8.2.2 :906 FR/AR ids match no carrier (factory-rules.md:32, architecture.md:35 use bold id plus dash): add that opener or drop the ids",
    "F2 s8.2.2 :906 state whether S1 sub-headings Rule N inside item N end its section (stamps would cover a part)",
    "F3 s8.2.2 :907 bold lead-in end heuristic can end a stamped section early outside the home: generalize the text rule or refuse such a stamp",
    "F4 s8.2.5 :945 state case sensitivity, repo-root resolution of file, untracked-existing target, NBSP section sign",
    "F5 s8.2.3 :932 write 6 for the brief (6. occurs once, critic-diff-brief.md:47) instead of a builder's choice"
  ],
  "class_completeness": "Surface: pointer address grammar (target) and pointer recognizer (carrier). Walked: prefix magnitude, repeated ids, parenthetical tails, case and NBSP encoding, nesting by sub-headings and bold, placeholders and missing anchors. Axes 31, 34, 1 in play; B3-B5 are the axis-1 and axis-34 residue; scan_extra vs EXCLUDED package main files not checked.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-everything-in-piles-spec.md:74-75,736,860-959,1005-1016,1085-1104,1240-1249",
      "docs/tasks/specs/reviews/t-943-everything-in-piles-r2.md:85-159",
      "docs/tasks/specs/20261116-boot-by-topic-spec.md:93-102,161-195,310-325,383-420,483-512,686-697,753-762",
      "PROJECT.md:318-343",
      "origin/main tools/tests/test_role_carriers_one_owner.py:1-140",
      "origin/main plans/builder-rules.md, CLAUDE.md, docs/tasks/critic-diff-brief.md, .claude/agents/builder.md, .claude/agents/critic.md, design/factory-rules.md, design/architecture.md, delegation.config.yaml (opener greps)",
      "plans/piles/forge/batch-7-vhodyashchie-4.md:75"
    ],
    "reruns": [
      {"command": "git show origin/main:CLAUDE.md | grep -nE item openers 1/3/6", "result": "1. at 37,386,409; 3. at 70,389,413; 6. at 109,420"},
      {"command": "git show origin/main:plans/builder-rules.md | grep -nE openers", "result": "### 7b. at 36 and 7b. at 38; ### 1. 8 / 1. 10; ### 10.-19. at 100-130"},
      {"command": "git show origin/main:docs/tasks/critic-diff-brief.md | grep heading", "result": "8: ## The two layers (CLAUDE.md rule 3, the two-layer review rule)"},
      {"command": "git show origin/main:design/factory-rules.md, architecture.md | grep FR-1/AR-1", "result": "32: **FR-1 — ...; 35: **AR-1 — ..."},
      {"command": "grep scout: delegation.config.yaml; grep Cost gates (D-0035 CLAUDE.md", "result": "one hit each (70; 257)"}
    ]
  }
}
```

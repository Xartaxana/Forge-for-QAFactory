# t-1010 — critic review of FG7-51 stream S1 (builder t-1008), staged diff in worktree agent-ac0ebd53313b8a61e

**Verdict: fit_with_fixes. Blocking findings: 0. Fixes: 5 (X1-X5).**

On top of the fixes, the Lead has two decisions to take before the commit:
- D1: the F19 fork (K4).
- D2: the named raise of the two constants (K6).

Whether to accept the work stays with the Lead (rule 6). The Lead also decides whether to raise the constants: the owner's word allows it, but this review does not decide it.

The work under review: S1 is the CLAUDE side of the boot-by-topic spec (`docs/tasks/specs/20261116-boot-by-topic-spec.md` §7.2 S1). The DoD is as given in the dispatch: a § Contents table, the sub-headings, the pointer line, the PROJECT TOC row and the POINTERS rows — and nothing else (INV-M). Every TOC cell must resolve. Nothing is committed.

## Blocking findings

None. INV-M holds byte for byte (K1). Every cell resolves (K9 control run: 0 red). No OWNER_KEYS sentence appears in either TOC (E10, my own run). The size overshoot was stopped and reported as E22 requires.

## Fixes (exact text)

**X1 — T30 names a pointer, not the home (K2).**
- S2's fix F4 moved the rule-writing text to boot-diet. `PROJECT.md:246-248` now holds only the heading and the line «Правило: `.claude/skills/boot-diet/SKILL.md` § Как пишутся правила для агентов.».
- The home is `.claude/skills/boot-diet/SKILL.md:111` `## Как пишутся правила для агентов`.
- The cell reaches it in 2 hops, against §2's «ONE home» and the DoD's «names its home».
- Cost: +23 B.

CLAUDE.md:42, replace

    | How rule text for agents is written | PROJECT.md § Как пишутся правила для агентов |

with

    | How rule text for agents is written | .claude/skills/boot-diet/SKILL.md § Как пишутся правила для агентов |

In `tools/tests/test_role_carriers_one_owner.py` (TOC_POINTERS), replace

    (_TOC_CL, "PROJECT.md § Как пишутся правила для агентов |", _PRJ, "## Как пишутся правила для агентов"),

with

    (_TOC_CL, "| How rule text for agents is written | .claude/skills/boot-diet/SKILL.md § Как пишутся правила для агентов |", ".claude/skills/boot-diet/SKILL.md", "## Как пишутся правила для агентов"),

**X2 — the `## Contents` heading now swallows the import paragraphs (K1 judgment: «the heading names the topic of what follows»).**
- The table was inserted before «The project's own rules, principles and layout live in PROJECT.md…».
- As a result, CLAUDE.md:47-59 sits under «## Contents — topic → where to read». That text is the three import intros and the four `@` lines, none of it Contents.
- Recommended fix (0 B): move the block of staged lines 8-46 (blank, heading, blank, the 35-line table) so it sits immediately before `## Tiers (see DELEGATION_TABLE.md; …)`.
  - This does not change what a session loads: imported files are delivered as separate blocks, not at the `@` position. The `@` lines still sit in CLAUDE.md, and this review's own context shows exactly that.
  - It departs from the letter of §4.1 «after line 6». The table is still the first content above any rule, but the Lead should name the deviation.
- Alternative that keeps §4.1's position: add a heading above the import paragraph. Check 33 (h) would then report that heading as unrouted. Not recommended.

**X3 — the commit's `tests-over:` line (rule 20).**
- `( cd <worktree> && python -B tools/test_volume.py --help )` printed `TEST VOLUME (WARN, the commit goes on): +61 test lines vs +0 product lines in this commit`.
- The builder report names no reason.
- The reason holds: spec §4.3 item 5 requires one POINTERS row per TOC cell until FG7-52. They are rows of an existing table, with no new test function or file.
- Commit-message line:

    tests-over: 50 POINTERS rows, one per TOC cell of both TOCs, required by the boot-by-topic spec §4.3 item 5 until FG7-52 (rows of an existing table; no new test function or file)

**X4 — axis 31 rows for the new aspect (K8).**
- The spec's «Lead places» list for S1 says only «everything». However, axis 31's closing rule requires «a new carrier of role text joins this table in the commit that creates it». The topic map is a new routing aspect of CLAUDE.md.

In `docs/SIBLING_MAP.md:491`, replace

    | `CLAUDE.md` | all | routing rules 1-13, journal, Role ≠ tier, degradation, command hygiene; cost gates (rule 12) | owner; critic questions → the brief (rule 3) |

with

    | `CLAUDE.md` | all | routing rules 1-13, journal, Role ≠ tier, degradation, command hygiene; cost gates (rule 12); the cross-file topic map (§ Contents, one row per topic T1-T33 of the boot-by-topic spec) | owner; critic questions → the brief (rule 3); every Contents cell is a POINTERS row of `tools/tests/test_role_carriers_one_owner.py` until FG7-52 |

In `docs/SIBLING_MAP.md:553`, replace

    | `tools/tests/test_role_carriers_one_owner.py` | all | one owner per key, pointers resolve | detector |

with

    | `tools/tests/test_role_carriers_one_owner.py` | all | one owner per key, pointers resolve, every cell of CLAUDE.md § Contents and PROJECT.md § Оглавление resolves (TOC_POINTERS) | detector |

**X5 — the builder report's row count is wrong (witness consistency, rule 12).**
- The report says «50 rows: 37 for CLAUDE TOC cells, 13 for PROJECT TOC». My count from the imported module is 50 rows: 36 with carrier CLAUDE.md and 14 with carrier PROJECT.md (the new PROJECT row targets CLAUDE.md).
- The fix is not to the diff: the Lead corrects the count in the `accepted` notes.

## K1 — INV-M, proven by script

Script (`scratchpad/k1.py`): for each of CLAUDE.md and PROJECT.md it diffs the HEAD blob against the index blob with `difflib.SequenceMatcher`. It requires that every opcode is `insert`, then strips the inserted lines and compares the result with HEAD byte for byte. Output:

    CLAUDE.md non-insert ops: 0 | inserted lines: 55 | stripped == HEAD: True | bytes HEAD 47132 staged 50150
    PROJECT.md non-insert ops: 0 | inserted lines: 1 | stripped == HEAD: True | bytes HEAD 34234 staged 34332

The 55 inserted CLAUDE.md lines:
- 3 lines around the Contents heading (8-10).
- 35 table lines (11-45) and a blank (46).
- Seven sub-headings with their blank lines: 105-106, 139-141, 235-236, 317-318, 382-383, 503-505, 528-529.
- The pointer line 496 `   why and how to recover: PROJECT.md § Сессия форджа`, verbatim from §3.1 C-H1..5.

The one PROJECT.md line is :35. **No byte outside these changed.** The blank line 139 splits the rule-4 paragraph at the sentence boundary that §3.1 C4b names. It is whitespace only.

`install_parity.py --check` re-run: `MISSING (0)`, `UNKNOWN (0)`.

## K2 — TOC truth, row by row (homes as on disk after S2)

Every row was checked against §2 and the headings on disk: `grep -n "^#"` over CLAUDE.md, PROJECT.md, RUNBOOK, TESTING, TEAMWORK, OWNER_PRINCIPLES and boot-diet SKILL, plus the numbered openers. Rows marked **ok** need no change.

| T | Cell (staged) | Verdict |
|---|---|---|
| 1 | CLAUDE.md § Tiers | ok per the spec sample. The cell is a prefix of `## Tiers (see DELEGATION_TABLE.md; …)` — see note N1 |
| 2 | § 1 + § 2 + § Rule 2 · drafting → designer | ok (§2: rule 1, rule 2, § Rule 2 · drafting). § 1 and § 2 are ambiguous in the file (N2) |
| 3 | § 11 | ok |
| 4 | § 2 | ok |
| 5 | plans/builder-rules.md § 7b | ok: the cell is literally the §4.1 sample. §2 says «7b (+ 7, 7a, 7c)»; the sample takes precedence |
| 6 | § Rule 4 · witness scope and the BATCH CANON + docs/RUNBOOK.md § 7. CI на GitHub и BATCH CANON | ok (the full heading text `## 7. CI на GitHub и BATCH CANON`, RUNBOOK:96) |
| 7 | docs/TESTING.md | ok. Whole-file cell: §4.3 grammar has no file-only form (N3) |
| 8 | § 3 | disputable: §2 says «rule 3 (+ R13 g)». Optional cell `CLAUDE.md § 3 + CLAUDE.md § 13` (+16 B). Not required: rule 12 · Cost gates also carries «ONE critic pass per topic (R13-g)» |
| 9 | docs/tasks/critic-diff-brief.md | ok (whole file, N3) |
| 10 | CLAUDE.md § Routing log | ok, prefix of `## Routing log — logs/journal/<dev>.jsonl` (N1) |
| 11 | RUNBOOK § 7… + PROJECT § Командная работа (кучки и пачки) | ok. «Слить принятое» is a bold paragraph at RUNBOOK:111, not a heading, so § 7 is the right granularity. PROJECT п. 1 is under that section |
| 12 | PROJECT § Командная работа (кучки и пачки) | ok. п. 12 is at PROJECT:228, under `### Знание, узлы, темп, проверки билдера` — the parent section is acceptable |
| 13 | § Rule 12 · Cost gates | ok |
| 14 | § Command hygiene + PROJECT § Сессия форджа | ok. §2 says «hygiene pt. 3», but `CLAUDE.md § 3` would resolve to rule 3, so the section is the only unambiguous form |
| 15 | § Command hygiene | ok (prefix of `## Command hygiene (permission hygiene)`, N1) |
| 16 | § 9 | ok |
| 17 | § 10 | ok |
| 18 | PROJECT § Командная работа… + docs/TEAMWORK.md | ok |
| 19 | PROJECT § Бэклог и находки | ok (PROJECT:111) |
| 20 | docs/OWNER_PRINCIPLES.md | ok (the index is imported anyway) |
| 21 | PROJECT § Как принимается изменение пакета | ok |
| 22 | PROJECT § Как разрабатывается новая идея владельца | ok |
| 23 | docs/RUNBOOK.md § 4.1. Шаги релиза | ok (RUNBOOK:52) |
| 24 | PROJECT § Язык | ok |
| 25 | PROJECT § Что решать самому… + CLAUDE.md § 11a | ok |
| 26 | PROJECT § Ссылки на файлы в ответах | ok |
| 27 | .claude/agents/<role>.md | ok as §2 writes it. It has no POINTERS row (correct: not a path). Under FG7-52's §4.3 item 4 («unresolvable is RED») a placeholder cell would go red (N4). The aspects are already pinned by OWNER_KEYS `hand-back:*` |
| 28 | .claude/agents/designer.md § 7 | ok |
| 29 | .claude/skills/boot-diet/SKILL.md | ok |
| 30 | PROJECT.md § Как пишутся правила для агентов | **wrong → X1** |
| 31 | PROCESS/SESSION_PROTOCOL.md | ok |
| 32 | § Role ≠ tier + § Lead degradation | ok |
| 33 | PROJECT § Как принимается… + PROJECT § Командная работа… | ok. A more precise optional form is `PROJECT.md § Пакет: проход и свидетель + PROJECT.md § Знание, узлы, темп, проверки билдера` (п. 2 is under PROJECT:67, п. 13 under PROJECT:215). Not required |

Notes for FG7-52's contract (§4.3). These are not S1 defects: S1 follows the spec's own sample. I propose them as a queue line for the FG7-52 node, which the Lead opens:
- **N1, prefix cells.** §4.3 item 1 says `<x>` «equals the text of a heading», yet the spec's own sample `§ Tiers` is a prefix. So are `§ Routing log`, `§ Command hygiene` and the PROJECT row's `§ Contents`. Exact contract line:

    `<x>` equals a heading's text, or that text up to its first ` (` or ` — ` (the TOC short form: `§ Tiers`, `§ Routing log`, `§ Command hygiene`, `§ Contents`).

- **N2, number cells are not unique in CLAUDE.md.**
  - `1.`, `2.` and `3.` each open three lines: routing rules :82/:96/:117, Lead degradation :459/:464/:466, Command hygiene :491/:494/:495.
  - Item 4's adversarial case «a numbered item deleted while its number is cited» would therefore stay green under the line-start rule.
  - Today's POINTERS rows anchor on the full opener, so they are safe.
  - Contract line:

    a number `<x>` resolves within the `##` section of `<file>` that holds the routing rules (CLAUDE.md § Routing rules), or must be unique in the file.

- **N3, whole-file cells** (TESTING, critic-diff-brief, OWNER_PRINCIPLES, boot-diet, SESSION_PROTOCOL, TEAMWORK). Contract line:

    a cell `<file>` with no `§` routes to the whole file; it resolves when the file exists.

- **N4, the T27 placeholder.** Contract line:

    a cell holding `<role>` expands to every file of `.claude/agents/` that has a `hand-back:*` key in OWNER_KEYS; each expansion must exist.

## K3 — the PROJECT TOC row

`| Все темы → `CLAUDE.md` § Contents | карта «тема → где читать» |`. The left cell is the spec's literal (§4.1, E21). The right cell has 4 words, within the ≤ 8 cap, and is in the same register as the other «О чём» cells. **Acceptable as is.** Its POINTERS row anchors on the full heading `## Contents — topic → where to read`, and my K9 control turns it red if that heading is renamed.

## K4 — fork F19, the consequence of option (a) as built

Facts. Lines are staged CLAUDE.md; «section» means heading to next heading at any level; script `scratchpad/sec.py`. A `###` sub-heading inside `## Routing rules` takes everything after it until the next heading. So each sub-heading under (a) swallows the numbered rules that follow it:

| Sub-heading | Spans | Holds besides its own topic |
|---|---|---|
| `### Rule 2 · drafting → designer` (105) | 105-139 | rule 3 (the critic gate, T8's home) and rule 4's opener |
| `### Rule 4 · witness scope and the BATCH CANON` (140) | 140-234, **95 lines, no table** | rules 4a, 5, 6, 7, 8, 9 (T16's home) and 10's opener (T17's home) |
| `### Rule 10 · a change to the package` (235) | 235-316, 82 lines (R11 table inside) | rule 11 (T3's home), 11a (T25's home), rule 12's opener |
| `### Rule 12 · Cost gates` (317) | 317-333 | rule 13 |

Consequences for the check-33 (h) line, as landed by S2 at `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:1045`. On its first run it reports:
- **(i)** «a section over 50 lines without a table» on CLAUDE.md 140-234 (95 lines). That is the only CLAUDE.md hit. PROJECT.md `## Командная работа` (167-241, 75 lines, no table) is a hit only if «section» is read as `##`-to-`##`. At any level, its two `###` halves are 42 and 27 lines.
- **(ii)** «a `##` heading of the boot that no TOC row routes to» on `## Routing rules` (CLAUDE.md:80): no cell names it, because the cells cite the numbers under it. This holds under (a) and under (b) alike.
- **(iii)** E14 (≈40 lines) is broken by 140-234 and 235-316.
- **(iv)** Under §1.1 item 4 «one heading per topic», rules 3, 4a-9, 11, 11a and 13 have no heading of their own and sit under a heading that names a different topic.

The builder did what (a) says: «sub-headings only inside rules over ~40 lines (2, 4, 10, 11, 12)». The defect is in (a) itself, not in the execution.

Recommendation (for the Lead to decide; not decided here):
- Take **(b)-narrow**: one `### Rule N · <topic>` heading above every numbered routing rule, keeping the four existing sub-headings. This removes (i), (iii) and (iv).
- Measured cost of the 15 headings below, blank lines included: **567 B** (`scratchpad/bytes.py`). The named raise absorbs it (K6).
- Rule numbers and openers stay byte-identical (E1; the parity anchors are opener lines).
- Rule 4a sits inside item 4 at a sentence boundary (:151/:152), so it needs the same whitespace-only split as the Rule 4 sub-heading.
- Suggested texts, inserted above the opener at the staged line given (a blank line before where there is none, and one after):

    :82  ### Rule 1 · recon → scout
    :96  ### Rule 2 · implementation → builder; acceptance by witness
    :117 ### Rule 3 · the critic gate
    :134 ### Rule 4 · parallel parts
    :152 ### Rule 4a · a task DAG; team work
    :157 ### Rule 5 · flat delegation
    :159 ### Rule 6 · escalation
    :172 ### Rule 7 · background by default
    :182 ### Rule 8 · the skip rule; small-work batching
    :197 ### Rule 9 · fix the class
    :213 ### Rule 10 · four questions per mechanism
    :246 ### Rule 11 · DoD in every dispatch
    :298 ### Rule 11a · question routing
    :310 ### Rule 12 · the coordinator's cadence
    :326 ### Rule 13 · leaf routing

The TOC cells can keep the number form (§4.1).

For (ii) the Lead has two options; this is a calibration-protocol edit for the Lead or Architect:
- Add a TOC row `| Routing rules 1-13 | CLAUDE.md § Routing rules |` (+46 B). That is a row outside the §2 map, which the Lead would have to name.
- Or amend the (h) clause to: «a `##` heading of the boot that no TOC row routes to, directly or through the numbered items under it».

If the Lead keeps (a) instead, the first check-33 run will report (i) and (ii) as findings. The spec's own detector would then be flagging the spec's own choice.

## K5 — Rule 11 sub-headings

F1 is decided (a), and §3.1 C11a-e asks for `### Rule 11 · …` sub-headings «at paragraph boundaries». Rule 11 (246-296) has only one blank-line boundary, :291 before the R11 table. Its topic changes fall at sentence boundaries, so each sub-heading needs the same whitespace-only split the builder used for Rule 4.
- None is strictly needed for the length limit: 52 lines including a table, so (h) is silent.
- One heading is needed for structure: under (a), rule 11's opener and edges (:246-256) sit under `### Rule 10 · a change to the package`. That is fixed only by a heading above :246, which is the (b)-narrow line `### Rule 11 · DoD in every dispatch` from K4.

Proposed sub-headings, measured 176 B together. Each goes as a blank line, the heading and a blank line, inserted before the staged line named:

    before :257 «Which tests a DoD asks for:»            ### Rule 11 · which tests a DoD asks for
    before :265 «scout: an explicit question …»         ### Rule 11 · scout and critic DoD; the manifest; the five-point checklist
    before :282 «The DoD is written INLINE …»           ### Rule 11 · inline DoD; the DOC-DISPATCH witness

None of these splits a condition from its consequence:
- The forward reference «(2) the DoD inline (below)» at :276 still points to the next section.
- The T7 row of §2 already names «CLAUDE.md rule 11 · which tests», which matches the first heading.

If the Lead wants the bytes back, the first heading alone is the minimum that §2 names.

## K6 — size

Measured: the TOC block (staged lines 9-46) is **2656 B** (`sed -n 9,46p CLAUDE.md | wc -c`). Headings plus the pointer line are the other 362 B of the +3018 B.

**(i) What the TOC can shed without losing a routed topic** (bytes counted on the staged table by `scratchpad`'s Python count):

| Lever | Saves | Note |
|---|---|---|
| `PROJECT.md § Командная работа (кучки и пачки)` → `PROJECT.md § Командная работа` (4 cells) | 108 B | the same prefix form as `§ Tiers`, `§ Command hygiene`, so the table becomes self-consistent. Needles of 4 POINTERS rows change; anchors `_TW_HEAD` stay |
| `docs/RUNBOOK.md § 7. CI на GitHub и BATCH CANON` → `docs/RUNBOOK.md § 7` (2 cells) | 62 B | a number form against a `## 7.` line, which §4.3's number forms do not list. Not recommended before N2/N1 are settled |
| `§ 4.1. Шаги релиза` → `§ 4.1` | 23 B | same caveat |
| merge T14 + T15 into `| Command and session hygiene | CLAUDE.md § Command hygiene + PROJECT.md § Сессия форджа |` | ≈ 50 B | both topics stay routed; T-numbering diverges from §2 |
| drop the `CLAUDE.md ` prefix in CLAUDE-internal cells (17 occurrences) | 170 B | needs a §4.3 grammar change («§ X» = this file). That is a spec change, the Lead's |

Total ≈ 240 B without a grammar change, ≈ 410 B with it. **Against the 2350 B CLAUDE.md overshoot this is marginal. A raise is needed either way**, as is the 1298 B boot overshoot.

**(ii) The smallest raises.**

CLAUDE_WARN. The comment's formula (`tools/session_context.py:216-229`) is `ceil(size × 1.15 / 100) × 100`, with «raising should keep the same >=15% margin»:

| CLAUDE.md size at commit | CLAUDE_WARN |
|---|---|
| 50150 (as staged) or 50173 (+ X1) | **57700** |
| 50740 (+ X1 + K4 (b)-narrow) | 58400 |
| 50916 (+ X1 + K4 + K5) | 58600 |

The literal minimum that only fits (50200) breaks the comment's 15% clause. Taking it would need the comment re-worded, and that is the weaker choice.

BOOT_WARN_THRESHOLD has no formula. The 15% rule cannot apply to it: 109298 × 1.15 = 125693 > BREACH 120000. The smallest raise is the next hundred above the boot measured at commit:
- 109400 with X1 only (109321).
- 110000 with K4 (109888).
- 110100 with K4 + K5 (110064).

The ceiling the existing tests allow is ≤ 114999: `test_session_context.py:1040-1054` seeds a total of 115000 and asserts `total > sc.BOOT_WARN_THRESHOLD`. The `_WARN_BAND_README` tests sit at ≥ 118000.

**(iii) Pins that must change in the same commit.** I used `git -C <wt> grep -n -i -E "47800|47 800|108000|108 000|108,000|47,800|CLAUDE_WARN|BOOT_WARN_THRESHOLD"`, excluding logs, experiments, docs/tasks and the archive, plus a second pass for the `47.8K`/`108 KB` forms. Positive control: the same call found `tools/session_context.py:204`. Results:
- `tools/session_context.py:204` `BOOT_WARN_THRESHOLD = 108000`. The value changes, and the comment line :203 gains:

    # raised to <N> by the owner's word 17.11.2026 («не в ущерб правилам. Если не влезет — можно поднять») after the boot-by-topic TOC (measured <boot> at commit)

- `tools/session_context.py:216-229`: the CLAUDE_WARN re-derivation comment («Re-derived 2026-11-11 … 41502 … = 47800») and the value at :229. The new comment states the new measurement and the owner's word. The 11.11 lines move to «Prior measurement».
- `tools/session_context.py:1382`, docstring «crosses the WARN (>108000)»: the number changes.
- `tools/test_session_context.py` references only `sc.CLAUDE_WARN` and `sc.BOOT_WARN_THRESHOLD` symbolically (:1035, :1052-1054, :1078, :1093, :1140, :1152-1156), so no literal changes. The Lead's witness for the raise is `python -m pytest tools/test_session_context.py -q -k "budget or imports"` after the edit.
- No other carrier pins either number: SIBLING_MAP, PROCESS, `.claude`, BOOT.md, CURRENT_CONTEXT.md and DECISIONS.md were grepped. `.gitattributes:5` names `CLAUDE_WARN` only.

Not a pin but a conflict: spec §1.4 says «`CLAUDE_WARN` stays 47800», and §1.1 item 5 says «lands under 108000». The raise overrides both on the owner's word 17.11.2026. Record it in the batch's «Ход» line and in the commit message; specs are history and are not edited. `tools/session_context.py` is a `tools/` mechanism file, so the commit needs the axis block and `tier:` line.

## K7 — the two word edits from t-999 «For S1»

Recommendation: **do not land them in S1.**
- The S1 card (§3.1 C-H1..5: «stay; pt. 3 gains one pointer line») does not list them. The DoD is «NOTHING else».
- Both citations resolve in 2 hops today, which is the state E2 declares by design. The CLAUDE TOC already routes both destinations (T6 → RUNBOOK §7, T18 → TEAMWORK).

If the Lead lands them anyway, name them as K3 rows in the commit message. Exact text:
- (a) CLAUDE.md:492. Replace `   the narrow target the work needs; the full sets run on CI, never on this machine (PROJECT.md, package change p. 2);` with `   the narrow target the work needs; the full sets run on CI, never on this machine (`docs/RUNBOOK.md` §7);`.
  - The target carries the clause: RUNBOOK:127-128 «(слово владельца 03.11.2026: канон — на CI)».
  - The parity anchor on :491 «1. Tests — the canonical form, from the repo root:» is untouched.
- (b) CLAUDE.md:156. Replace `   Team work in piles and batches: the rule text is PROJECT.md «Командная работа» (D-0036; detector: check 33).` with `   Team work in piles and batches: the rule text is PROJECT.md «Командная работа» + `docs/TEAMWORK.md` (D-0036; detector: check 33).`.
  - The parity anchor «Team work in piles and batches: the rule text is PROJECT.md» survives as a prefix.
  - Axis 31 (`SIBLING_MAP:492`) declares rule 4a «a trimmed ↔ full pair» with `docs/CLAUDE_HOST_ADAPTATIONS_FULL.md`. Its :43-44 header «PROJECT.md «Командная\n   работа»)» then becomes «PROJECT.md «Командная\n   работа» + `docs/TEAMWORK.md`)» in the same commit.

## K8 — class completeness, and what the commit owes outside the staged diff

- Axis 31: X4 (two rows).
- install-parity: nothing owed. No anchored line changed; re-run `MISSING (0)`. Even if K7 lands, the anchors stay prefixes.
- Check 33 (h): already landed by S2 (PROCESS:1045). If F19 stays (a), see K4 (ii) and the amendment text.
- AGENTS.md: must be regenerated after every fix (`python -B tools/agents_md.py --repo <worktree>`). The current staged copy is up to date (107817 B).
- The commit message for this mechanism commit (CLAUDE.md is in `mechanism_gate.py`'s net, :216) carries:
  - `tier: opus`;
  - X3's `tests-over:` line;
  - the four questions;
  - the axis block for every axis of the current map (1-37).

Draft:

    four questions (CLAUDE.md § Contents + TOC_POINTERS):
    (a) cost: 2656 B in every session (sed -n 9,46p CLAUDE.md | wc -c); whoever renames a heading updates its TOC cell and POINTERS row
    (b) axes: below
    (c) detector: POINTERS rows of tools/tests/test_role_carriers_one_owner.py (CI forge-check, pytest tools/); TOC completeness and section length: calibration check 33 (h)
    (d) on the path: pytest in forge-check refuses a dangling cell; completeness on discipline until FG7-52, detector check 33 (h)
    axis 1: covered - CLAUDE.md headings, TOC and one pointer line; no role duty changed, profiles untouched, AGENTS.md regenerated
    axis 2: n/a - no exam instrument touched
    axis 3: n/a - package not touched
    axis 4: covered - AGENTS.md regenerated with CLAUDE.md/PROJECT.md (pre-commit agents_md --check); principles index untouched
    axis 5: n/a - package not touched
    axis 6: n/a - no measurer touched
    axis 7: n/a - no test identity scope touched (rows of an existing table)
    axis 8: n/a - package not touched
    axis 9: n/a - no test-file recognizer touched
    axis 10: n/a - no git-top reader touched
    axis 11: n/a - no shell recognizer touched
    axis 12: n/a - no work-plan carrier touched (batch status is the Lead's separate move)
    axis 13: n/a - dispatch text and its cut untouched
    axis 14: n/a - no transcript reader touched
    axis 15: n/a - no console setup touched
    axis 16: n/a - package not touched
    axis 17: n/a - no detector verdict shape touched
    axis 18: n/a - no shrink-only ratchet raised in this commit (the WARN constants, if raised, are named in this message)
    axis 19: n/a - no tools: line reader touched
    axis 20: n/a - package not touched
    axis 21: n/a - package not touched
    axis 22: n/a - package not touched
    axis 23: n/a - package not touched
    axis 24: n/a - package not touched
    axis 25: n/a - package not touched
    axis 26: n/a - package not touched
    axis 27: n/a - package not touched
    axis 28: n/a - package not touched
    axis 29: n/a - no jsonl writer touched
    axis 30: n/a - package not touched
    axis 31: covered - CLAUDE.md row gains the topic-map aspect, the test row gains the TOC cells; every cell a POINTERS row
    axis 32: n/a - no package check; the TOC check is data presence (spec §1.3)
    axis 33: n/a - dispatch identity untouched
    axis 34: covered - one road: TOC cells checked by the existing POINTERS table, no second checker (spec A1)
    axis 35: n/a - package not touched
    axis 36: n/a - package not touched
    axis 37: n/a - package not touched

If the raise lands in the same commit, axis 18's line names it.

- Outside the diff, for the Lead: the FG7-51 S1 node status in its batch file, and the journal.

## K9 — do the POINTERS rows go red when a heading is renamed

Script `scratchpad/k9.py`:
- It imports the test module with `ROLE_CARRIERS_ROOT` pointed at a **copy** of every carrier and target named by `TOC_POINTERS`.
- It runs each row's two assertions on the copy. The worktree is never touched.

Output:

    TOC_POINTERS rows: 50 CLAUDE-carrier: 36 PROJECT-carrier: 14
    control (unchanged copy) -> red rows: 0
    rename PROJECT '## Сессия форджа' -> 'форжа' -> red rows: 2
    rename CLAUDE '### Rule 12 · Cost gates' -> 'gate' -> red rows: 1
    rename PROJECT '## Язык' -> '## Языки' (one char appended) -> red rows: 0
    rename RUNBOOK '### 4.1. Шаги релиза' -> '... и тега' -> red rows: 0
    demote CLAUDE '## Lead degradation' -> '####' -> red rows: 0
    renumber CLAUDE 11a -> 11b (cell '§ 11a') -> red rows: 1

**A rename that changes or cuts heading text turns the row red. A rename that only APPENDS to the heading, or changes its level, stays green.** The check is squashed substring presence in the whole target file.
- This is the existing K-PTR mechanism's documented direction, and spec §4.3 item 5 makes it the interim check. So it is not an S1 defect.
- But it misses §4.3 item 4's adversarial case «a heading renamed by one character» when the character is appended.
- Needle scoping (rule 15) holds: every CLAUDE-carrier needle occurs inside the TOC block (staged 9-46) and nowhere else in CLAUDE.md. The script printed no unscoped needle.

Proposal for the FG7-52 node, not this commit: anchor TOC rows on a whole heading line, not a substring. A drop-in for the test, if the Lead wants it now:

    def heading_lines(text):
        return {" ".join(l.lstrip("#").split()).casefold() for l in text.splitlines() if l.startswith("#")}
    # in test_pointer_resolves: when anchor starts with "#", assert squash(anchor.lstrip("#")) in heading_lines(read(target))
    # (squash() = " ".join(text.split()).casefold(); a heading whose text merely starts with the anchor no longer matches)

The `## Tiers (see` row would then need its anchor written as the full heading.

## E10 (S1 DoD: no OWNER_KEYS sentence in a TOC) — independent run

The builder substituted `test_one_owner_per_key` for the DOC-DISPATCH run. That test cannot see a key owned by CLAUDE.md being quoted in CLAUDE.md's own TOC, because the same file stays the single carrier. This covers 4 keys: `routing:rule-11`, `routing:hygiene-6`, `routing:rule-9` and `cost:cap`.

My run (`scratchpad/e10.py`, squashed key vs the squashed CLAUDE TOC 9-46 and the PROJECT TOC 18-36) printed «absent» for all 16 keys, then:
- `negative control (routing:rule-11 pasted into the TOC copy) detected: True`;
- `keys present in a TOC: 0`, exit 0.

**E10 holds.** The witness-form gap is closed by this run. It goes to the Lead's `accepted` notes and is not a fix round.

## Standing questions

- **DUPLICATION AND CONSISTENCY:** one inconsistency, inside the table. Cells to PROJECT use the full heading `Командная работа (кучки и пачки)`, while cells to CLAUDE use the short form (`§ Tiers`, `§ Command hygiene`). The K6 lever row 1 fixes it (−108 B). In the test, `_RS`/`_PRJ` restate literals `"docs/RUNBOOK.md"`/`"PROJECT.md"` that the S2 rows above spell out inline. This is cosmetic and not a finding. Grepped: the TOC block, the TOC_POINTERS block, the POINTERS block.
- **CODE QUALITY:** the test change is data rows only, plus one concatenation `POINTERS = POINTERS + TOC_POINTERS`. Parametrize ids repeat (`CLAUDE.md->CLAUDE.md`), but the assertion message names the pointer text, so a red row names its cell. None found beyond that. Read: test file :1-160.
- **ONE ROAD (P31):** TOC cells are checked by the existing POINTERS table, with no second checker (A1). No language, project or case is excluded. None found.
- **TESTS (TESTING «Бюджет»):** over the volume rule (+61 vs +0). The reason holds, but it is unnamed in the report and in the commit → X3.

## Trail

Read:
- the staged diff (`git -C <wt> diff --cached` for CLAUDE.md, PROJECT.md and the test);
- the builder report;
- spec §1, §2, §3.1, §4, §5, §6, §7.1-7.2, §8, §9;
- t-999 verdict :100-175;
- `tools/session_context.py:185-240, 1375-1390`;
- `tools/test_session_context.py:1035-1160`;
- the test file :1-160;
- PROJECT.md headings and TOC :14-40, :78-90, :167-172, :242-250;
- CLAUDE.md :44-62, :134-160, :246-300, :491-493, the heading and opener list;
- RUNBOOK :96-112 and the heading list;
- headings of TEAMWORK, OWNER_PRINCIPLES, TESTING and boot-diet SKILL;
- `docs/SIBLING_MAP.md` :24-44, :470-566, :593-605, the axis list;
- `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:1045`;
- `docs/CLAUDE_HOST_ADAPTATIONS_FULL.md:43-50`;
- the `install_parity_anchors.json` routing-policy unit;
- the TESTING «Бюджет» section;
- the `forge-check.yml` pytest line.

Scripts were written to the session scratchpad (never committed): `k1.py`, `k9.py`, `e10.py`, `sec.py`, `bytes.py`.

Hook denial, verbatim: my first K1 command started with a stray `cd /c &&` and was refused with «PreToolUse:Bash hook error: the shell's working directory must not move: the hooks find tools/ from it. Use git -C <dir>, python -B <absolute path>, a tool's --repo/--root, or a ( cd <dir> && ... ) subshell.» I re-ran it without the `cd`. The budget hook also printed «AGENT BUDGET WARN: 10 test runs …» once.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "X1: T30 cell names PROJECT.md section that is now a pointer; replace with .claude/skills/boot-diet/SKILL.md § Как пишутся правила для агентов and re-target its TOC_POINTERS row (exact text in K2/X1)",
    "X2: the Contents heading swallows the import paragraphs CLAUDE.md:47-59; move the staged block 8-46 to just above ## Tiers (0 B; Lead names the deviation from spec 4.1)",
    "X3: commit message carries the tests-over line (test_volume: +61 test vs +0 product lines; reason: spec 4.3 item 5)",
    "X4: docs/SIBLING_MAP.md axis 31 rows :491 (CLAUDE.md gains the topic-map aspect) and :553 (test gains TOC cells), exact text in X4",
    "X5: correct the row count in the accepted notes (36 CLAUDE-carrier + 14 PROJECT-carrier, not 37 + 13)"
  ],
  "class_completeness": "Surface: CLAUDE.md heading structure and TOC cells. Walked: every T1-T33 cell against its home on disk (one wrong: T30); every sub-heading's scope (four swallow the following numbered rules: K4, Lead fork F19); axis 31 rows owed (X4); axis 1 twin CLAUDE_HOST_ADAPTATIONS_FULL owed only if K7(b) lands; install-parity anchors unaffected (MISSING 0); check 33 (h) consequences stated; FG7-52 contract gaps N1-N4 and the append-rename false green (K9) proposed as a queue line for the FG7-52 node, not this commit.",
  "trail": {
    "read": [
      "worktree staged diff: CLAUDE.md, PROJECT.md, tools/tests/test_role_carriers_one_owner.py",
      "docs/tasks/handoffs/t-1008-boot-s1-report.md",
      "docs/tasks/specs/20261116-boot-by-topic-spec.md sections 1-9",
      "docs/tasks/specs/reviews/t-999-boot-by-topic-s2.md:100-175",
      "tools/session_context.py:185-240,1375-1390",
      "tools/test_session_context.py:1035-1160",
      "docs/SIBLING_MAP.md axes 1, 31, 34",
      "PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:1045",
      "docs/RUNBOOK.md:96-128 and headings",
      ".claude/skills/boot-diet/SKILL.md headings",
      "docs/CLAUDE_HOST_ADAPTATIONS_FULL.md:43-50",
      "tools/install_parity_anchors.json routing-policy unit",
      "docs/TESTING.md Budget section"
    ],
    "reruns": [
      {"command": "python -m pytest tools/tests/test_role_carriers_one_owner.py tools/test_agents_md.py -q (worktree)", "result": "162 passed in 8.54s"},
      {"command": "python -B tools/install_parity.py --check (worktree)", "result": "MISSING (0), UNKNOWN (0)"},
      {"command": "python -B tools/agents_md.py --check (worktree)", "result": "AGENTS.md: up to date (107817 bytes)"},
      {"command": "echo {} | python -B tools/session_context.py | grep BOOT BUDGET (worktree)", "result": "BOOT BUDGET: 109298 bytes / 120000 (4 files + 4 imports) WARN | CLAUDE.md: 50150/47800 incl. imports 98276 OVER"},
      {"command": "scratchpad/k1.py (HEAD vs index, strip inserted lines)", "result": "CLAUDE.md non-insert ops 0, 55 inserted, stripped == HEAD True; PROJECT.md non-insert ops 0, 1 inserted, stripped == HEAD True"},
      {"command": "scratchpad/k9.py (rename headings in a copy, evaluate TOC_POINTERS)", "result": "control 0 red; body rename red; one-char append and level change stay green; 11a renumber red"},
      {"command": "scratchpad/e10.py (OWNER_KEYS vs both TOCs, negative control)", "result": "16 absent, negative control detected, exit 0"},
      {"command": "python -B tools/test_volume.py (worktree)", "result": "TEST VOLUME WARN: +61 test lines vs +0 product lines"}
    ]
  }
}
```

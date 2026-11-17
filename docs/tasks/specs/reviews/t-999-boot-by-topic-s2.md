# t-999 — critic gate, FG7-51 stream S2 «the PROJECT side» (builder t-991)

Reviewed: the STAGED change in `C:\QAFactory\forge-repo\.claude\worktrees\agent-adbe4143d52ee10c3` (worktree HEAD 551405f6; `origin/main` = a9d25118: the commits between them do not touch PROJECT.md, CLAUDE.md, RUNBOOK, builder-rules, TESTING or critic-diff-brief, checked with `git diff 551405f6 a9d25118 -- <those files>` → empty). Baseline = `origin/main`. Spec/DoD: `docs/tasks/specs/20261116-boot-by-topic-spec.md` §1.2, §2, §3.2-§3.4, §5, §7.2 S2, §7.4, §8, §9, §10.

**Verdict: fit_with_fixes. Blocking findings: 0. Fixes: 7** (F1-F7 below; exact text given). Plus one proposed node (N1, a one-road leftover the spec decided to keep) and a list of items for S1. Whether to accept stays with the Lead (rule 6).

---

## K1 — NOTHING LOST (the core)

**Method (my own script, independent of the builder's key script).** I extracted the `origin/main` and staged copies to the scratchpad and squashed them (`" ".join(t.split()).casefold()`). The old file is split into clauses at blank-line blocks, at sentence ends `.!?`, at `;`, and at table-cell bars. A leading list marker or heading mark is stripped, and fragments under 12 characters are dropped. Each clause is then looked up in the squashed union of the staged PROJECT.md, OWNER_PRINCIPLES.md, TEAMWORK.md, RUNBOOK.md, builder-rules.md, TESTING.md and critic-diff-brief.md (a second try ignores `**`). Source:

```python
import re, sys, pathlib
S = pathlib.Path(sys.argv[1]); src = sys.argv[2]; union = sys.argv[3:]
sq = lambda t: " ".join(t.split()).casefold()
U = sq("\n".join((S/"new"/u).read_text(encoding="utf-8") for u in union)); U_nomark = U.replace("**", "")
text = (S/src).read_text(encoding="utf-8"); frags = []
for line_block in re.split(r"\n\s*\n", text):
    for part in re.split(r"(?<=[.!?;])\s+|\s\|\s|^\|\s|\s\|$", sq(line_block)):
        p = re.sub(r"^(#+\s*|-\s+|\d+[a-z]?\.\s+)", "", part.strip(" |")).strip()
        if len(p) >= 12: frags.append(p)
miss = [f for f in frags if f not in U and f.replace("**","") not in U_nomark]
print(f"{src}: {len(frags)} clauses, {len(miss)} not found in union")
for m in miss: print("  MISS:", m[:240])
```

**Results:**
- `old/PROJECT.md`: 413 clauses, 24 not found.
- `old/plans/builder-rules.md`: 176 clauses, 8 not found.
- `old/docs/RUNBOOK.md`: 525 clauses, 3 not found.
- `old/CLAUDE.md` (checked against the staged CLAUDE.md): 424 clauses, 3 not found.

Every miss is accounted for by a spec row:

| Miss (old PROJECT.md, opener) | Spec row | Verdict |
|---|---|---|
| «**Тесты идут в CI…**: билдер гоняет только быстрые узкие свидетели… (до минуты каждый)…» | 2-3 + 2-4 K4 (+R2) | allowed; 7b holds «НЕ гоняет и не ждёт» and «точечные проверки своей правки» |
| «медленный файл (`SLOW_TESTS`…) …его судит CI;» | 2-5 K4 | allowed; 7b holds `SLOW_TESTS` and `test_fixes_13797` |
| «Задача на один инструмент в `tools/`…» | 2-7 K4 | allowed; CLAUDE.md rule 4 «the test file that judges the path», 7b «`pytest tools/` целиком» |
| «**Канон всегда на CI** (D-0059)… не больше часа…» | 2-8 K4 | allowed; RUNBOOK §7 BATCH CANON paragraph holds both keys (`grep` run: RUNBOOK:117-118) |
| «Полный `selftest.py` и `install_smoke.py` на машине владельца не гоняются.» | 2-10 K4 | allowed; builder-rules 7 «на машине их не гоняет никто» |
| «карантин гоняет задача `quarantine-watch`…», «удаление — по условию спеки td-15 §D.3 и только по слову владельца» | 2-11 K4 | allowed; TESTING:110, :124, :129 |
| «Голый пуш ветки ничего не запускает;» | 2-13 K4 | allowed; RUNBOOK:100 «пуш ветки без PR ничего не запускает» |
| «как прогнать ветку и прочитать результат — `docs/RUNBOOK.md` §7.» | 2-14 K3 | allowed; replaced by the pointer line |
| «Локальный прогон и локальный докер — только запасной путь (там же), …» | 2-15 K2 («(там же)» dropped) + R5 | allowed |
| «**Бэклог.** Новая находка…» | PA4 K2 (the bold title stays on the pointer line) | allowed; text verbatim in § Бэклог и находки |
| «**Сжатие контекста…**: на ~300K контекста — одна строка…» | PR7 + TR1 | allowed |
| «две пачки с общим горячим файлом… — D-0048):» | 3a («:» → «.», §10) | allowed |
| «перенос подтверждает **человек**, не агент сам;» | 9c (in the pointer line, «;» → «.») | allowed |
| п. 12: «(владелец, 13.11.2026): в работе всегда шесть…», «Не хватает параллельных узлов…», «меньше шести…», «Шесть — не потолок…» | R1 (12-1, 12-3, 12-7) | allowed; ready text §3.4c matched word for word |
| п. 13: all six clauses | 13-a…13-h | allowed (13-b, 13-e in 7b with «(слово владельца 14.11.2026)» carried from the item header) |

- builder-rules misses: B-1, B-2, B-4, B-5 (two fragments), B-7, plus the clause fragments of the same edits. All allowed.
- RUNBOOK misses: RB-1, RB-2, RB-3. All allowed.
- CLAUDE.md misses: the two C12b edits, (1) and (2). All allowed.
- **No LOSS found.**
- P1-P31: zero misses. The reverse check (staged text not in the old sources) finds only the PI-1 title and intro line and the range sub-headings. So the bullets are verbatim.

**Reverse direction** (`rev.py`: staged clauses not found in the old sources). Every new clause comes from a spec row or a spec ready text: the TOC cells, the pointer lines, the «Диспетчеру:» connective, «При общем файле», R1 (a)/(b)/(c), TR1, the §6 text, the TEAMWORK intro, «**Интегратор.**», R5's clause, B-1/B-5 and RB-1..3. Nothing else was added.

**The 162-of-185 negative control.** In the builder's script, `mut()` is applied only inside `k2()`, `k1()` and `home()`. The 23 rows that survive `--mutate` are:
- **19 absence-only rows.** These are never mutated: mutating a key that must be ABSENT makes it pass trivially, so a mutation is no control for them. They are 9c-in-TW, 12-1-old, 12-3-old, 12-7-old, C12b1-old ×2, 13-b-src, 13-e-src, 13-f-src, 2-15-там-же, R2 (PROJECT), R2 ×2 (builder-rules), B-1-old, B-4 (absent), B-5-src ×2, RB-1-old, RB-3-old.
- **4 direct `report(ok=…)` rows** that bypass `mut()`: TR1, C12b2, R5-order, CL-1pin.

They do not discriminate under the mutation control. I gave them my own positive control (`absctl.py`): each absence phrase is checked to be present in the OLD file, so its absence in the new file is a real change.
- 18 of the 19 absence phrases are `in-old=True in-new=False`.
- The odd one is 2-15-там-же. It tests RUNBOOK, which never held «запасной путь (там же)», so it is vacuous. The real check for that clause is the absent-from-source flag of 2-15a/2-15b on PROJECT.md, and that flag passes.
- I verified the 4 direct rows by reading the staged text: TR1 PROJECT:160, C12b2 CLAUDE:275, R5 order RUNBOOK §7, pin test_session_context:1325.
- Not a defect of the witness, but the report should have named the 23. Noted here so the trail is complete.

## K2 — NOTHING IN TWO HOMES

`k2.py` checked every clause of 25+ characters in the staged PROJECT.md against OWNER_PRINCIPLES, TEAMWORK, RUNBOOK, builder-rules, TESTING, critic-diff-brief and CLAUDE. The only hits are heading names: «Как принимается изменение пакета», «Что решать самому…», `ai-packages/qa-factory/`. TEAMWORK against PROJECT: 0. RUNBOOK against builder-rules and PROJECT: 0.

Near-duplicates that exist by spec decision:
- RUNBOOK «Что остаётся локально»: two local-fallback sentences side by side (R5).
- RUNBOOK «**Интегратор.**»: two integrator sentences (F17 a). See N1.

**None found beyond pointers.**

## K3 — ONLY THE RESOLVED MEANINGS CHANGED

Every non-verbatim difference maps to R1, R2, R3 (RB-1), R5, TR1, B-1…B-7, RB-1…RB-4, PI-1, CL-1, C12b (1)/(2), or a connective listed in §10.
- The PROJECT ready texts of §3.4a-§3.4d were compared word for word: п. 2, п. 2/3/4/8/9 boot side, п. 12, п. 13. They match. The only difference is line wrapping: «**Находка называет класс…**» starts on its own line.
- The owner's dated words travel with their clauses: «(владелец, 13.11.2026)» п. 3; «(владелец, 11.11.2026)» 9f; «(владелец, 16.11.2026)» 12-4; «(владелец, 14.11.2026)» on п. 13's header plus «(слово владельца 14.11.2026)» on 13-b/13-e in 7b; «(слово владельца 03.11.2026)» on B-5; «(D-0052 (3), узел CL1-8, 20.10.2026)» on §4.1.
- The stream L sentences travelled verbatim: «Новая идея» step 1 «Шаги 1–4 могут идти в сессии Архитектора … D-0067 …» (PROJECT:122-123), and п. 5 «или Архитектор (D-0067)» (PROJECT:190).
- **No other rewording found.**
- Context-word check (the K2 judgment): PROJECT § Бэклог и находки «(там же п. 4)» still refers to «Командная работа» in the same sentence. RUNBOOK «Тогда исходники…» now follows the R5 clause and still refers to the local run. The moved §4.1 text says «(выход 2 — список причин в RUNBOOK §4)», which now refers to its own file. It still resolves. Kept verbatim per K2.

## K4 — POINTERS RESOLVE

- Every pointer in the staged PROJECT.md resolves: TEAMWORK § 2/3/4/8/9 (numbered line openers), RUNBOOK § 4.1 and §7, `docs/OWNER_PRINCIPLES.md`, § Бэклог и находки, `plans/builder-rules.md` п. 7b.
- TEAMWORK → PROJECT п. 3 resolves.
- builder-rules → RUNBOOK §7 (×2) resolves.
- RUNBOOK → 7b and → PROJECT § Сессия форджа resolve.
- CLAUDE.md → PROJECT § Сессия форджа and п. 12 resolve.
- The POINTERS rows pass (control re-run below).

**CLAUDE.md citations of PROJECT** (grep `PROJECT\.md|Командная работа` over the staged CLAUDE.md):

| Line | Citation | Status |
|---|---|---|
| :33 | «PROJECT.md, steps 1–4» | lands |
| :91 | «step 6», «package change, item 6» | lands |
| :113 | «PROJECT.md «Командная работа»» | lands (the section points on to TEAMWORK) |
| :262 | owner-away paragraph | lands |
| :275 | § Сессия форджа | lands |
| :277 | п. 12 | lands |
| :442 | «(PROJECT.md, package change p. 2)» | lands in 2 hops (p. 2 → RUNBOOK §7 / 7b) |

**No BLOCKER:** no citation in a file outside S1's owns now points at nothing.

Readers outside the diff: one case-insensitive grep over `.claude/agents`, `.claude/skills`, `PROCESS`, `tools/*.py`, `tools/tests/*.py`, `.githooks`, `docs/*.md`, root `*.md` and builder-rules. Pattern: `Прогоны и эксперименты|Принципы владельца|«Релиз»|Как принимается изменение пакета»,? п. ?[24]|Командная работа»,? п. ?(2|3|4|8|9|13)|PROJECT.md,? п. ?2`. Positive control in the same output: TEAMWORK:18 and PROJECT:84 were found.

| Reader | Citation | Status |
|---|---|---|
| PROCESS:1109 (check 39) | п. 9 | 2 hops via the pointer line |
| tools/piles.py:2183 | п. 2 | 2 hops |
| RUNBOOK:176 | «Прогоны и эксперименты», P8, P18 | section stays; P ids via the index |
| RUNBOOK:220, :358, :364 | п. 2 | 2 hops |
| RUNBOOK:389 | п. 4 | 2 hops |
| SIBLING_MAP:34 (axis 1) | п. 13 | keeps the dispatcher sentence (spec Q1, unchanged) |
| critic.md:165, designer.md:79, language_sites.py:106 | «PROJECT.md P31» | 2 hops via the index |
| agent_budget.py:278 | «(PROJECT.md)» | lands (file-level) |

- **Stale carrier claims in SIBLING_MAP: :94 (axis 4) and :309 (axis 12).** See F1.
- `docs/tasks/specs/20261117-everything-in-piles-spec.md` (t-907) already writes «PROJECT.md or `docs/TEAMWORK.md` § with the same number» (:514). E20's re-sync is therefore pre-armed.

**For S1** (CLAUDE.md lines; no blocker; S1 owns them):
- (a) hygiene pt. 1 «(PROJECT.md, package change p. 2)» could cite `docs/RUNBOOK.md` §7 directly (2 hops today).
- (b) rule 4a «the rule text is PROJECT.md «Командная работа»» → add «+ `docs/TEAMWORK.md`».
- (c) the C-H3 pointer line «why and how to recover: PROJECT.md § Сессия форджа».
- (d) the PROJECT TOC row «Все темы → `CLAUDE.md` § Contents» (E21), plus one POINTERS row per TOC cell of BOTH TOCs (§4.3 item 5; the 13 PROJECT cells S2 wrote have no POINTERS rows yet — S1's by the card).
- (e) the budget forecast in K6.

## K5 — THE BOOT STILL CARRIES WHAT EVERY SESSION NEEDS

I read all 31 lines of the principles index. **None inverts its principle.**

The emptiest cuts:
- **P21** «У доставки три исхода, не два.» The third outcome is not named.
- **P7** «Фабрика работает на Sonnet или Terra.» The ban «Haiku не используется нигде» is cut. FR-52 and CLAUDE.md «No tier runs on Haiku» carry it in the boot.
- **P5** The cut drops «LLM-агент — не источник данных для чтения». AR-6 and FR-50 carry it in the boot.
- **P16** drops «одно поведение на кейс — правило юнит-уровня».

None of them misleads into the opposite. They are the S4 cut rule working as specified, not an S2 defect.

Nothing a coordinator needs every turn is one hop away without a route:
- TEAMWORK is named in the TOC row «Командная работа».
- OWNER_PRINCIPLES is in its own TOC row and in «Где что лежит».
- RUNBOOK §7 is reached from п. 2 and CLAUDE rule 4. The PROJECT TOC lists own sections only, by spec.

**Placement of «## Как пишутся правила для агентов»:** acceptable where it is, in the tail group of «how we write» sections (Язык, Ссылки). However, the measured budget triggers the spec's own F19 (d): this section should leave the boot (F4).

## K6 — EDGES

- **E20:** п. 9 was moved as it stands. 9a minus 9c and 9b are in TEAMWORK § 9; 9c-9f are in the boot. t-907's edit is not on `main`, and its spec already targets both homes (:514). Holds.
- **E7:** all 12 files are staged together, the exchanges included. The Lead commits them as ONE commit. Holds.
- **E21:** no TOC row names CLAUDE § Contents. Holds.
- **TEMPORAL (E7 / S4 edge):** `docs/OWNER_PRINCIPLES.md` and `docs/OWNER_PRINCIPLES_INDEX.md` are both staged as `A`. `factory_rules_index.py --check` prints «up to date (31 rules)». The import and the pin are in the same index. Holds.
- **E8:** the only new import is from CLAUDE.md; PROJECT.md's «Импорт `@`» is inside backticks mid-line, not an import line. Holds.
- **E9:** BOOT.md is untouched. Holds.
- **E2, E3, E19:** hold (pointer lines carry the bold titles; P ids are in the index; `cost:queue` was re-quoted).

**Budget.** The control re-run gives `BOOT BUDGET: 107885 bytes / 120000 (4 files + 4 imports) | CLAUDE.md: 47129/47800`.
- The spec's F19 trigger reads: «if the measured BOOT BUDGET after S2 is still above 104000, add (d)». 107885 > 104000, so the spec ALREADY prescribes (d): §6 moves to boot-diet. The section measures **2363 B** (`sed -n 238,253p | wc -c`), more than the spec's 1.9 KB estimate. Net after F4 and F3: about 105.7 KB.
- **S1's real wall is CLAUDE.md's own cap, not the total.** It has 671 B of headroom against an estimated ≈2.0 KB TOC (F19 a) plus about 0.5 KB of sub-headings. Even with (d), CLAUDE.md lands about 1.8 KB over CLAUDE_WARN 47800.
- The spec's only remaining CLAUDE-side lever is F19 (c): restore F5 (a), moving the Routing-log section, −2.0 KB measured. The alternatives are a TOC of at most about 600 B, or E22: S1 stops and the Lead takes the number to the owner.
- This is a Lead decision to take BEFORE dispatching S1, not an S2 defect. §5.1 allows no further clause-level removal from PROJECT.md without a new spec row.

## K7 — TESTS AND CARRIERS

- **POINTERS rows match the card's «test rows (S2)» one for one:** PROJECT→TEAMWORK § 2/3/4/8/9 (anchors = the byte-identical TEAMWORK openers, distinct from the PROJECT pointer lines), →OWNER_PRINCIPLES («- **P31.**»), →RUNBOOK § 4.1, →RUNBOOK §7, «правило: § Бэклог и находки», RUNBOOK→§ Сессия форджа, builder-rules→RUNBOOK §7, TESTING→7b, BRIEF→7b.
- `cost:queue` is re-quoted «цель держать 6 пишущих билдеров» (E19). Expected values come from the spec.
- The `test_session_context.py` pin has the 4th import, in the order of CLAUDE.md.
- **Gap:** two pointers this node writes have no row, although §4.3 item 5 asks for «every pointer line this node writes»: CLAUDE.md «PROJECT.md § Сессия форджа» (C12b (2)) and TEAMWORK «`PROJECT.md` «Командная работа» п. 3». See F5.

**TESTS (rule 20, brief question 5):**
- (a) Killing power: a renamed heading or opener turns its row red (`test_pointer_resolves` checks both sides).
- (b) Values trace to the spec.
- (c) New doors: none.
- (d) Nothing deleted.
- (e) No duplicate row; checked against the whole table, :37-92.
- (f) About 17 test lines against about 1000 product lines, so no `tests-over:` is needed.
- (g) No new file.
- Verdict: fine except F5.

**DUPLICATION AND CONSISTENCY:**
- No duplicated rule sentence across homes. Searched with k2.py over the 7 homes plus CLAUDE.md; listed in K2.
- One duplication in tests: the import list is now hand-kept in three places: CLAUDE.md's `@` lines, the `test_session_context` pin (a deliberate pin), and the `test_agents_md.py` `real_copy` fixture tuple. The fixture is not a pin, it is a copy, and it is why DoD 1 went red in t-991 (7 errors). See F7.

**CODE QUALITY:** four new lines exceed the files' ~120-column wrap: CLAUDE.md:276 (C12b (1)), PROJECT.md:61, :181, :228. Cosmetic; F6.

## K8 — MECHANISM FORM AND CLASS COMPLETENESS

The card's «Lead places» names SIBLING_MAP axis 31 (two new files plus the :308 edit, now line 309) and the check-33 line. **Walking the map finds one axis the card missed: axis 4**, «Factory rules <-> … <-> the principles». Its :94 row still names `PROJECT.md (P1…P31)` as the principles' carrier, and the axis has no row for the new generated index. Exact lines are in F1. Check 33's header carrier list also misses TEAMWORK (F2).

**ONE ROAD (rule 19):** the residual is N1, a proposed node. AR index as a second generator: already queued (FG7-55), not this stream.

---

## Fixes (the Lead applies; exact text)

**F1 — `docs/SIBLING_MAP.md` (Lead-placed; class completeness).**
- (a) Axis 4, line 94: replace `| The owner's principles | PROJECT.md (P1…P31), mirrored as FR-47…FR-57 |` with `| The owner's principles | docs/OWNER_PRINCIPLES.md (P1…P31; PROJECT.md § Принципы владельца points there), mirrored as FR-47…FR-57 |`.
- (b) Axis 4: after the row `| One-line index (generated, loaded every session) | docs/FACTORY_RULES_INDEX.md ← … |`, insert `| Principles index (generated, loaded every session) | docs/OWNER_PRINCIPLES_INDEX.md ← tools/factory_rules_index.py (row P); imported by CLAUDE.md; pre-commit `--check` |`.
- (c) In axis 4's prose, after «A rules change regenerates the index in the same commit (enforced by pre-commit).», insert «A change to docs/OWNER_PRINCIPLES.md regenerates docs/OWNER_PRINCIPLES_INDEX.md, and with it AGENTS.md, in the same commit (both enforced by pre-commit).».
- (d) Axis 12, line 309: «PROJECT.md «Командная работа» item 3» → «`docs/TEAMWORK.md` § 3».
- (e) Axis 31 intro: after «`docs/tasks/critic-diff-brief.md` (the critic review),», insert «`docs/TEAMWORK.md` (the piles mechanics a gate refuses), `docs/RUNBOOK.md` §7 (the integrator's local run and the CI, merge and canon procedure),».
- (f) Axis 31 table, replace the `PROJECT.md` row with `| `PROJECT.md` | builder, critic, integrator, coordinator | package-change acceptance p. 1-6; «Командная работа» discipline | owner of p. 1, 3-6, of the owner's words in p. 2 and of its «Диспетчеру:» line; p. 2 otherwise holds pointers: scope → D-0056 + builder-rules 7b; CI job map → the `.github/workflows/` files; CI, canon, merge, local fallback → RUNBOOK §7; critic re-run → the brief; report → builder.md 7 + builder-rules 11; «Командная работа» п. 2, 3, 4, 8, 9 → `docs/TEAMWORK.md` (gated clauses), п. 13 → builder-rules 7b (keeps the dispatcher sentence) |`.
- (g) Axis 31 table, right under the PROJECT.md row, add:
  - `| `docs/TEAMWORK.md` | coordinator, integrator | the gated clauses of «Командная работа» п. 2, 3, 4, 8, 9 and the check line | owner (openers byte-identical to the PROJECT.md items, which point here per item) |`
  - `| `docs/OWNER_PRINCIPLES.md` | all | the owner's principles P1–P31, full text | owner; `docs/OWNER_PRINCIPLES_INDEX.md` is its generated index (machine copy), imported by CLAUDE.md |`
  - `| `docs/RUNBOOK.md` §7 | integrator, coordinator | the integrator's local run, CI reading, merge, canon procedure, local fallback (R5) | owner; builder-rules 7 and 7b and PROJECT p. 2 point here |`

**F2 — `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` check 33 (Lead-placed).**
- In the header, «CLAUDE.md rule 4a; PROJECT.md «Командная работа»).**» → «CLAUDE.md rule 4a; PROJECT.md «Командная работа»; `docs/TEAMWORK.md`).**».
- After item (g), which ends «…are the baseline, named once, not re-judged.», append the spec §6 (c) line, adding only the explicit «`##`» so that the existing `###` sub-headings, routed by their parent row, are not false hits: «(h) Boot form (boot-by-topic, FG7-51): sample CLAUDE.md and PROJECT.md for a rule sentence restated outside its home (topic map), a section over 50 lines without a table, a `##` heading of the boot that no TOC row routes to — each a finding; on discipline until FG7-52.»

**F3 — PROJECT.md «Командная работа» is 68 lines with no table (staged :165-232).** The rule this same commit lands (§ Как пишутся п. 2: «раздел не длиннее ~40 строк»), and the (h) detector of F2, flag it on the first calibration run. Add two K1 headings at paragraph/item boundaries:
- `### Пачки: взятие, заморозка, зоны, закрытие` on its own line (blank lines around it) right before «1. **Пачку берёт один разработчик**». This covers items 1-9, 39 lines.
- `### Знание, узлы, темп, проверки билдера` right before «10. **Знание — в проекте, не в памяти машины**». This covers items 10-13 plus the check line, 23 lines.
- Cost: about 120 B. It fits only together with F4.

**F4 — spec F19 (d), triggered by measurement (107885 > 104000). The decision is the Lead's; the spec prescribes it.**
- Move the 7 items of PROJECT.md § Как пишутся правила для агентов (staged :240-252) verbatim into `.claude/skills/boot-diet/SKILL.md`, as a new section `## Как пишутся правила для агентов` placed right before `## Detectors` (:111).
- In PROJECT.md keep the heading and one line: `Правило: `.claude/skills/boot-diet/SKILL.md` § Как пишутся правила для агентов.`
- Add a POINTERS row `("PROJECT.md", "`.claude/skills/boot-diet/SKILL.md` § Как пишутся правила для агентов", ".claude/skills/boot-diet/SKILL.md", "## Как пишутся правила для агентов")`.
- The TOC row stays.
- Saves about 2.2 KB, so the boot lands at about 105.7 KB.
- The commit's four-question (d) line keeps «retelling and length — on discipline, the (c) detector».
- If the Lead declines (d), the reason goes in the `accepted` notes, and F3 must then be bought elsewhere: F3 alone puts the boot at about 108.0 KB.

**F5 — `tools/tests/test_role_carriers_one_owner.py` POINTERS: append two rows** (§4.3 item 5):
- `("CLAUDE.md", "PROJECT.md § Сессия форджа", "PROJECT.md", "## Сессия форджа"),`
- `(TEAMWORK, "`PROJECT.md` «Командная работа» п. 3", "PROJECT.md", "3. **Зоны файлов пачек «в работе» не пересекаются** — правило: `docs/TEAMWORK.md` § 3"),`

**F6 — re-wrap to the files' ~120-column width (whitespace only, no word changes):**
- CLAUDE.md:275-277. The C12b (1) line becomes: «… CI through `tools/ci_read.py`; a push before a worktree launch» / «(`tools/dispatch_gate.py`). The writers, the FULL queue, the per-topic critic and merge waves: PROJECT.md» / ««Командная работа» п. 12. Detector: check 17.». Re-run `install_parity.py --check`.
- PROJECT.md:61, :181, :228.

**F7 — `tools/test_agents_md.py` `real_copy`:** derive the import files from CLAUDE.md instead of a hand-kept tuple. Replace the tuple loop header with:

`imports = [ln[1:].strip() for ln in (REAL / "CLAUDE.md").read_text(encoding="utf-8").splitlines() if ln.startswith("@")]`
`for rel in ("CLAUDE.md", *imports, ".claude/settings.json"):`

The next import then cannot break this fixture again. A missing imported file still fails at `copyfile`. The deliberate pin in `test_session_context.py` stays the one hand-kept list.

## Proposed node (not this round: the spec decided F17 (a), and INV-M forbids rewording here)

**N1 — one road for the integrator's local run.** RUNBOOK §7 «**Интегратор.**» now holds two «только» sentences with different sets:
- «гоняет только свидетелей узлов и `--limits --lang`»
- «локально гоняет только узкие свидетели узлов с конфликтом слияния и `--limits --lang`, затем push»

A reader cannot tell whether it is every node's witnesses or only those of conflicted nodes (P31, brief q.12). Owner: the Lead opens a node in the forge pile with the question to the owner, one sentence to replace both. The tier above decides (rule 6).

## Trail

**Read:**
- the spec §1-§10 and the fix-round table, whole;
- the staged PROJECT.md, whole; TEAMWORK.md, whole; OWNER_PRINCIPLES.md (headings and intro); OWNER_PRINCIPLES_INDEX.md, whole;
- staged diffs of CLAUDE.md, RUNBOOK, builder-rules, test_agents_md, test_session_context, test_role_carriers;
- `test_role_carriers_one_owner.py` (logic and table);
- the builder's report t-991 (rows, witness, the DOC-DISPATCH script, whole);
- SIBLING_MAP axes 1, 4, 12 (:305-312), 31;
- check 33 of the calibration protocol;
- `critic-diff-brief.md` questions 5-7, 12; TESTING «Бюджет» area; the critic verdict schema;
- the t-907 spec (grep);
- the readers grep over agents, skills, PROCESS, tools, docs/*.md and root md.

**Scripts** (scratchpad `C:\Users\i_mas\AppData\Local\Temp\claude\b3e3188b390a00d9\501cb4e0-b55f-46d8-9262-11b1caefad61\scratchpad\`):
- `k1.py`: source above.
- `k2.py`: same split; reports a staged clause found in another home.
- `rev.py`: staged clauses absent from the old sources.
- `absctl.py`: the 19 absence keys checked in-old / in-new.

**Control re-runs** (in the worktree):
- `python -m pytest tools/tests/test_role_carriers_one_owner.py tools/test_agents_md.py -q` → 109 passed
- `python -m pytest tools/test_session_context.py -q -k imports` → 15 passed, 294 deselected
- `agents_md.py --check` → up to date (106729 bytes)
- `factory_rules_index.py --check` → up to date (59 rules) / (31 rules)
- `install_parity.py --check` → MISSING (0), UNKNOWN (0)
- `piles.py check --all` → ok
- `session_context.py` → BOOT BUDGET 107885 / CLAUDE.md 47129/47800

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "INV-M holds: own clause scripts over old PROJECT.md (413 clauses, 24 misses), builder-rules (176, 8), RUNBOOK (525, 3), CLAUDE.md (424, 3) - every miss maps to a spec row (K4 2-3..2-13, R1, R2, R3, R5, TR1, 3a, 9c, 13-a..13-h, B-1..B-7, RB-1..RB-3, C12b); no loss, no two-home sentence. Map walk: axis 31 and axis 12 (:309) as the card says; axis 4 (:94 principles carrier, missing index row, regeneration prose) MISSED by the card -> F1; check 33 carrier list -> F2. One-road residual (F17 two integrator sentences) -> proposed node N1, owner Lead.",
  "fixes": [
    "F1 SIBLING_MAP: axis 4 :94 carrier -> docs/OWNER_PRINCIPLES.md + new principles-index row + regeneration sentence; axis 12 :309 item 3 -> docs/TEAMWORK.md section 3; axis 31 intro + replaced PROJECT.md row + rows for docs/TEAMWORK.md, docs/OWNER_PRINCIPLES.md, docs/RUNBOOK.md section 7 (exact text in the report)",
    "F2 check 33: header adds docs/TEAMWORK.md; append item (h) Boot form line from spec section 6 (c), naming ## headings",
    "F3 PROJECT.md Komandnaya rabota is 68 lines without a table: add two ### headings before item 1 and before item 10 (exact text in the report)",
    "F4 spec F19 (d) triggered by measured 107885 > 104000: move section Kak pishutsya pravila dlya agentov verbatim to .claude/skills/boot-diet/SKILL.md before ## Detectors, keep heading + pointer line in PROJECT.md, add its POINTERS row (Lead decision; spec prescribes it)",
    "F5 POINTERS rows: CLAUDE.md -> PROJECT.md section Sessiya forjda; docs/TEAMWORK.md -> PROJECT.md Komandnaya rabota item 3",
    "F6 re-wrap long lines CLAUDE.md:275-277 and PROJECT.md:61, :181, :228 (whitespace only), re-run install_parity --check",
    "F7 tools/test_agents_md.py real_copy: derive the import list from CLAUDE.md @ lines instead of a hand-kept tuple"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/20261116-boot-by-topic-spec.md",
      "worktree staged PROJECT.md, docs/TEAMWORK.md, docs/OWNER_PRINCIPLES.md, docs/OWNER_PRINCIPLES_INDEX.md",
      "worktree staged diffs: CLAUDE.md, docs/RUNBOOK.md, plans/builder-rules.md, tools/test_agents_md.py, tools/test_session_context.py, tools/tests/test_role_carriers_one_owner.py",
      "docs/tasks/handoffs/t-991-boot-s2-report.md (worktree)",
      "docs/SIBLING_MAP.md axes 1, 4, 12, 31",
      "PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md check 33",
      "docs/tasks/critic-diff-brief.md questions 5-7, 12; docs/TESTING.md budget area",
      "docs/tasks/specs/20261117-everything-in-piles-spec.md (grep)",
      "readers grep over .claude/agents, .claude/skills, PROCESS, tools, docs/*.md, root md",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "python -m pytest tools/tests/test_role_carriers_one_owner.py tools/test_agents_md.py -q", "result": "109 passed"},
      {"command": "python -m pytest tools/test_session_context.py -q -k imports", "result": "15 passed, 294 deselected"},
      {"command": "python -B tools/agents_md.py --check", "result": "AGENTS.md: up to date (106729 bytes)"},
      {"command": "python -B tools/factory_rules_index.py --check", "result": "up to date (59 rules); up to date (31 rules)"},
      {"command": "python -B tools/install_parity.py --check", "result": "MISSING (0), UNKNOWN (0)"},
      {"command": "python -B tools/piles.py check --all", "result": "piles check: ok"},
      {"command": "echo {} | python -B tools/session_context.py", "result": "BOOT BUDGET: 107885 bytes / 120000 (4 files + 4 imports) | CLAUDE.md: 47129/47800"},
      {"command": "k1.py old/PROJECT.md vs union of 7 staged homes", "result": "413 clauses, 24 misses, all mapped to spec rows"},
      {"command": "absctl.py the 19 unmutated absence keys", "result": "18 in-old=True in-new=False; 2-15-tam-zhe vacuous (RUNBOOK never held it), covered by 2-15a/b absent-from-source"}
    ]
  }
}
```

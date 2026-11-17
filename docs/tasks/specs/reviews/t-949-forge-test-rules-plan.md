# t-949 — critic on PLAN: «Forge test rules» (docs/tasks/specs/20261117-forge-test-rules-spec.md, draft t-940 + Lead decisions L-1..L-9)

Reviewer: critic (Opus 5.5), 17.11.2026. Review only: no code, no test runs. I checked the facts by trail. The verdict is an INPUT to the Lead's acceptance; the decision belongs to the Lead (critic rule 6).

**Verdict: fit_with_fixes (NEEDS WORK).** 2 blockers must be fixed in the plan before any stream is dispatched. 14 non-blocking fixes can go into the same Lead edit.

---

## Blockers

### B1 — The critic probe breaks two standing rules, and the plan amends neither (K2, K6; spec §3.2, §2.3, L-9)
- `CLAUDE.md:78-81` (rule 3, two-layer review rule): the critic's zone is the VERDICT layer; "a cheap control re-run of what is attached is legitimate … a layer not attached → critic asks the dispatcher for it and does not execute it". The probe in §3.2 is a NEW mechanical run (break the code, run, restore). It is not a re-run of something attached. The brief would then contradict the policy line that points to it. L-6 supersedes only D-0056 (2)/(3), and L-9 (b) rules out any CLAUDE.md edit. So no step of the plan touches rule 3.
- `CLAUDE.md:237` (R11-h) says "`tools/handoff_gate.py` lets it [critic] write only that file". `tools/handoff_gate.py:6-8` says "this hook is the whole protection: it lets such a worker write the one path". The critic's `tools:` line is `Read, Glob, Grep, Write, Bash` (`.claude/agents/critic.md:5`). So a probe made with Write is REFUSED by handoff_gate. Only Bash gets through, which goes around the stated write boundary of a reading role. The plan names neither the road nor the exception. A critic who follows §3.2 with Write runs into a refusal whose door ("put your report into the final message") does not fit its situation. That is the FR-2 / P15 class.
- Expected fix (the Lead chooses, a fork of the plan): (a) add one clause to CLAUDE.md rule 3 ("…and the bounded probe of `docs/tasks/critic-diff-brief.md` «The two layers»"), name the road (Bash through a runner script, never Write/Edit), and add one line to R11-h and to the handoff_gate docstring saying a probe is a script-run byte-copy mutation, not a report write. This costs boot bytes, which L-9 was protecting. Or (b) the critic NAMES 1-3 mutants (place, change: judgment), and a deterministic runner executes them: the coordinator under rule 8 "deterministic script runs", or the builder in the fix round. The verdict then carries the named mutants and the run result is attached before acceptance. This keeps the two-layer rule and the reading boundary as they are. Either way, the runner is the existing `ai-packages/qa-factory/scripts/tests/mutate_once.py` (see F1), not a shell choreography hand-built per probe (§3.2 E-P4).

### B2 — The order contradicts itself, and L-5 (a) leaves pointers to texts that do not exist yet (K7, TEMPORAL; spec §8, §5.1 E-C2, E-T1, «Lead decisions»)
- «Lead decisions» L-5: "S-A waits for boot-by-topic S2 … S-B, S-C, S-D do not wait for S-A." But:
  - §5.1 E-C2 and §8 say "S-C merges after S-A (its refusal names a TESTING section)". The INCOMPLETE hint names `docs/TESTING.md «Строка теста в DoD»`, which is created by S-A §2.2.
  - E-T1 (§3.2 edges, §7.2 edges, §8) says "critic.md 17, the brief's probe and the checker switch together". The brief's probe bullet is S-A §3.2. If S-B and S-D merge while S-A waits, `mutants` becomes REQUIRED with no procedure text. Worse, `docs/tasks/critic-diff-brief.md:19-20` still says "ratchets and mutation runs are not — they are the batch canon's". The critic is told to fill `mutants` and also told that mutation runs are forbidden to it.
  - S-B's texts point at S-A's headings: critic.md rule 20 → «Откуда берётся ожидаемое значение», «Тест может упасть»; builder.md rule 8, designer.md rule 1 → «Строка теста в DoD»; check 50 names all three. All of them dangle until S-A lands.
- Expected fix: split S-A. S-A1 = TESTING.md §2.1-2.4 and §4.1, plus the brief q5 and the two-layers bullets (§3.1, §3.2). None of these is in boot-by-topic S2's owns (§8 itself rows TESTING as "free" and the brief as "D / spec-facts L1 only"), so S-A1 does not wait. S-A2 = builder-rules 7b/7d, RUNBOOK:115 and the PROJECT column of §4.4. S-A2 waits for S2 (L-5 a). New order: S-A1 → {S-B + S-D in one wave, S-C}. S-A2 follows S2. Name the window between S-A1 and S-A2: 7b `:57-59` still says «мутации судит канон пачки» while TESTING says the canon runs none. Both still forbid the builder a suite, so the window contradicts only a claim about the canon. State it as the accepted TEMPORAL edge, with the landing grep of §4.4 run at S-A2.

---

## Non-blocking fixes (each: section — carrier — expected fix)

- **F1 Duplication (q6). A runner already exists.** §3.2 and E-P4 describe a hand-built "copy, mutate, run with a time cap, restore, hash". `ai-packages/qa-factory/scripts/tests/mutate_once.py:1-10` already does it: one mutation, one test file, byte-copy restore in `finally`, sha256 before and after, exit 2 on a mismatch. The spec does not mention it (§0, §11 and §14 are silent; I found it with Grep `mutat|mutant` over the package scripts). Differences to settle: it runs `python -B <test>` under `scripts/` only (no `tools/` pytest), it has no timeout, and it counts ANY non-zero exit as a kill, including a collection or import error. §3.2 calls that an "invalid mutant, not a kill". Fix: name it as the probe runner and extend it (`--root`, a pytest form, a timeout, an import/collection exit as its own exit code). Or state why it is not reused.
- **F2 The `run` join in §5.2 proves nothing.** The rule says "`run` must equal the `command` of some `trail.reruns` item". Three mutants that run the same narrow file join to the one ordinary control rerun (`tools/critic_verdict.schema.json` `trail.reruns[].command`), so "a probe without its run in the trail fails" is false. Fix: require a distinct rerun per mutant whose command names the mutant (with F1: `mutate_once.py <spec> <id>`), or drop the claim and keep only check 50 (b).
- **F3 Door token mismatch in §5.1 items 3-4 (FR-2).** The refusal shows display name `test`; the skip door accepts the item `tests`. A coordinator who copies the refused name writes `manifest-skip: test -- …` and gets `MANIFEST-SKIP REFUSED: unknown item 'test'` (`tools/dispatch_manifest.py:270-272`). Fix: one token in both places, or accept both.
- **F4 §5.1 item 2 drops silently unless more iteration sites are named.** `check_cut` filters `missing` through `ITEMS` (`tools/dispatch_manifest.py:949` `newly = [i for i in ITEMS …]`, `:956` `still = [i for i in ITEMS …]`), and `_items_text` reads `_DISPLAY` built from KEY_GROUPS (`:95`, `:902-903`). With "`ITEMS` unchanged", a literal build sets `missing["tests"]` and then drops it, which is a silent pass (FR-4). The other path is a KeyError in `_items_text`. Fix: name the iteration sites, `ITEMS + SKIP_ONLY_ITEMS` for `newly`, `still` and display.
- **F5 §8 misses an in-flight writer of the same function.** spec-facts S2 owns `tools/dispatch_manifest.py` and `tools/test_dispatch_manifest.py` and adds a READERS NOTE inside the same check (`docs/tasks/specs/20261116-spec-facts-by-code-spec.md:371, 588-597`; not landed: no `READERS` in `tools/dispatch_manifest.py`, last commit ea52f84f FG7-49). §8 lists only "spec-facts S1 (landed)". Fix: add the row with an order (`очередь:`) or function-disjoint owns (PROJECT «Командная работа» п. 3).
- **F6 The P16 baseline is inflated (K1).** Re-running the §0 grep gives 25, which matches. But the 25 are not the class «the spec did not name the test». t-816 matches only through "dropping". t-427, t-439 are canon quarantine-edit reds. t-442, t-462 are ratchet pins. t-325 is selftest's no-hooklib rule. Several (t-054, t-056, t-057, t-134, t-159) belong to the retired pin regime. Roughly 8-10 (t-133, t-420, t-502, t-547, t-559, t-654 …) are the class the line targets. Fix: re-cut the baseline of check 50 (d) by reading, not by regex. Restate the L-2 rationale on the read count.
- **F7 The §10 axis block will not pass the gate.** "axes 3-10: n/a", "axes 19-30: n/a", "axes 35-37" are ranges. `tools/mechanism_gate.py:24` requires "axis N: <verdict>" for EVERY axis (37 per `^## Axis`), and CLAUDE.md rule 10 (b) asks for one line per axis, closing each mechanism by name. Fix: write the 37 lines as they will stand in the S-B and S-C commit messages.
- **F8 Axis 31: the cap number is restated in five carriers.** The brief ("Hard cap: 3"), TESTING §2.3 ("1–3 места"), RUNBOOK §4.4 ("критик (1–3 мутанта)"), critic.md 17 ("0-3 probes"), and the checker. The checker's diagnostic already cites the brief. Fix: keep the number in the brief (rule text) and in the checker (data). Elsewhere, pointers without the number.
- **F9 Artifact sweep in builder-rules.** `plans/builder-rules.md:120` 16 (б) says "один прогон-свидетель закрывает раунд … перепрогон после каждой правки — нарушение". The new `red-before:` run is an extra run inside the round. Fix: a pointer clause in 16 (б) ("плюс один `red-before:` на пункт-дефект, TESTING «Тест может упасть»"). It belongs to S-A2.
- **F10 Gaps in the oracle rule (K5; §2.1).** (i) «поведение, которое спека велит сохранить, с причиной» lets a spec line like "existing output stays" turn into a snapshot of the current output. That is expectation-from-code and the «как раньше» row of `docs/TESTING.md:96`. Fix: the keep exemption holds only when the spec names the kept VALUE or invariant (what stays refused or printed), never "as now". (ii) Values derived from the test's own input (N fixture rows in → N out) are neither listed nor excluded, so critics will judge them differently. Fix: add "a value derived from the test's input by the rule the spec states".
- **F11 The cap counts only what the critic declares, and the time cap is not stated (K2).** The `mutants` maxItems 3 counts declared probes. A critic who runs ten and reports three is caught by nothing on the path. Check 50 (b) reads only the verdict trail. Fix: check 50 (b) counts probe runs from the worker transcript (the agent_budget test-run counter already exists: `plans/builder-rules.md:120` "предупреждает на 10-м прогоне"). And put an explicit timeout in the runner (60 s). 7b's "до минуты" is a criterion of narrowness, not a timeout (E-P4).
- **F12 First dispatches of in-flight specs also lack test lines (K3, TEMPORAL).** E-C1 covers only resubmissions. The first stream dispatches of boot-by-topic S2, everything-in-piles r3, spec-facts S2, architect-tier and rules-debt phase 2 are all over the threshold and all would be refused on day one. Fix: name this edge and its door reason (`manifest-skip: tests -- spec accepted before the test line (<spec>)`), and have check 50 (a) count it as its own class.
- **F13 Verdicts written before the field (K4).** With everything-in-piles A2, every acceptance runs `check_text` (`20261117-everything-in-piles-spec.md:279-291`). A topic verdict written before S-D lands, for nodes accepted after it, fails with `missing required field: mutants`. C's door text says "verdict predates remarks" (`:246-247, 308-309`), which is the wrong field and the wrong reason (FR-1). Fix: S-D asks C for a field-generic door text ("verdict predates a required field (<name>)"), or S-D's own refusal names it. Also, §10 M3 (d) "code on the path" holds only after A2 lands: P31 of that spec says the checker is on no path today. State that dependency.
- **F14 Minor items.** (i) S-B owns `CLAUDE.md`, but L-9 (b) rules out the edit, so drop it from owns (`§7.2`). (ii) §4.1 TESTING text keeps the placeholder «<дата ответа на O-2>»; O-2 is answered 17.11 (`docs/tasks/compact-snapshots/2026-11-17-0215-narrative.md:32`). (iii) §2.4 «(номер — следующий свободный при посадке)» is an instruction, not landing text: say so. (iv) L-2 equals O-3 ("против — оставить строку советом без проверки кодом"). The Lead's L-2 = True is provisional until the owner's word on O-3. Mark it so, and S-C flips `TEST_LINE_REFUSES` on her answer. (v) Check 13 (c) (`PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:828-835`) reads "rollback not checked" markers near a mutation probe by hand. Critic probes add to that stream, so check 50 should name it.

---

## Keys

**K1 — facts by trail: answered.** Spot-checked and TRUE:
- P1-P3, P8-P10 line numbers (`docs/TESTING.md:43-59, 61, 117, 124-127, 172-182`; `plans/builder-rules.md:44, 57-59, 89, 91`; brief `:11, :19-20, :38`)
- P4 (Grep `mutat` -i over `.github` → 0; control `python` -i → 82 in 5 files, same tool and shape)
- P5 (all four carriers present: `PROJECT.md:364`, `AGENTS.md:379`, `docs/RUNBOOK.md:115`, calibration `:377`. Note: shell grep -i does not fold Cyrillic, and my first pass missed «Мутации»; re-run with `[Мм]`)
- P6 (`docs/DECISIONS_ARCHIVE.md:112`)
- P11 (`KEY_GROUPS` :84-93, `DESIGNER_THRESHOLD` :105, skip parse :258-276, pin `tools/test_dispatch_manifest.py:1268`, mechanism path `tools/mechanism_gate.py:275`)
- P12, P13, P14 (Glob `PROCESS/*EXAM*.md` → the two other files)
- P15 (checks end at 48, `:1113`; no other spec claims 50: Grep)
- §11 counts `dispatch_manifest` 144/24 and `dispatch_new` 26/6, exact
- §6 arithmetic (43/1965)

FALSE or misleading:
- P16's class claim (F6)
- "nobody runs mutants" is true of CI, but the spec misses that the forge has a mutation runner, `mutate_once.py` (F1). Not stale, and relevant to the design.
- §8's overlap table misses spec-facts S2 (F5)

**K2 — owner's words, bounded proof: answered with fixes.** No suite comes back: §2.3 and §3.2 forbid one in every carrier, and the builder's step is one narrow run per defect item. The cap is declared (3 per verdict, L-3) but counted only on the critic's declaration (F11). The time bound is implicit (F11). Narrow-file-only is stated (§3.2 "ONLY the narrow test file the spec's `test:` line names"). New duties per dispatch:
- builder: +1 run and +1 report line per defect item; questions instead of guessed values
- critic: q5 grows to sub-questions (a)-(g); 1-3 probe runs on behaviour diffs; `mutants`/`mutants_none` on every verdict, plan gates included
- designer: +1 `test:` line per behaviour item
- coordinator: `--test`

Bounded, so not "the main work". The real cost risk is the probe's choreography, not its runs. That is why I ask for the runner (F1, B1).

**K3 — `test:` gate: answered with fixes.** Refused on day one when over the threshold: every builder fix round and resubmission without the line (E-C1); every first dispatch of an in-flight spec (F12); doc dispatches and small-work batches owning 3 or more paths, which need `test: none -- …`; `dispatch_new` without `--test`. Doors: `--test "none -- <why> | expected from: …"` through the generator, `manifest-skip` by hand. Usable, except for the token mismatch (F3). The informed pass is a line, not a silence. Edges named in §5.1:
- empty value, `none` with no reason: refused
- several items: one line passes (a declared false pass)
- under the threshold: not checked by code, though the rule text applies (stated in §2.2)

F4 is a silent-pass trap in the build.

**K4 — `mutants` REQUIRED: answered with fixes.** Plan reviews, doc-only diffs and no-behaviour diffs take `mutants: []` plus `mutants_none` (empty outcome declared, E-P1/E-P2). Old verdicts fail `check_text` (both worlds named; the door text is wrong: F13). The order C → S-D in §8 is enough for the file collision, but the field is coupled to C's `remarks` vocabulary, which r3 is still moving. S-D's `remark` join must be re-read against C's landed text at dispatch.

**K5 — oracle: answered with fixes.** "expected from:" can be checked by a tier above, at the granularity of a spec section. The keep exemption and fixture-derived values leave the holes in F10.

**K6 — architecture and principles: answered with fixes.**
- One home and pointers: yes, except the restated cap (F8).
- Code checks presence, form and joins only; sufficiency stays with the critic (P27 class): yes, but the `run` join is vacuous (F2).
- Doors: F3, and B1's refusal.
- Four questions: M1-M5 rows complete. M3 (d) depends on everything-in-piles A2 (F13).
- Axis block: not gate-shaped (F7).
- Check 50: drafted (§9), number free.

**K7 — streams and order: answered (B2, F5).** The owns of S-A to S-D are disjoint from each other. Files handed STAGED: `dispatch_manifest.py` (S-C) and the role files, CLAUDE.md and calibration (S-B). `critic_verdict_check.py` is not a live hook today, so staging S-D is not required. The TEMPORAL dangles are listed in B2.

**K8 — forks: answered.**
- O-1 and O-3 are rightly the owner's, and both can be reversed (O-1 is a text, O-3 is a switch). Building on the recommendation is legal under the owner-away clause.
- L-2 duplicates O-3, so a Lead decision now covers an open owner question: mark it provisional (F14 iv).
- L-5 (a) conflicts with the order (B2).
- L-6 belongs in this topic: a Lead decision line, not a queue item.
- L-9 (b) collides with B1 if the Lead picks road (a).
- O-2 is verified in the Lead's snapshot (`2026-11-17-0215-narrative.md:32`).

**K9 — class completeness: answered.** Map axes checked: 1, 2, 13, 17, 31, 32, 34. Must be fixed in THIS spec's streams, not queued:
- the CLAUDE.md rule 3 / R11-h / handoff_gate docstring triple (B1)
- `mutate_once.py` (F1)
- builder-rules 16 (б) (F9)
- the cap restatements (F8)

From §13: #3 (D-0056) is done by L-6 in this topic. #1, #2, #5, #6 are correctly left as they are (exam debt F3-1; spec-facts L; fixture history; kit text). #7 is fixed by §2.4.

## Standing lines (rules 18-20)
- **DUPLICATION AND CONSISTENCY:** one found, `mutate_once.py` (F1). Grepped `mutat|mutmut|mutant` -i over `ai-packages/qa-factory/scripts/*.py` and `mutate_once` over the repo (only piles and features mention it).
- **CODE QUALITY (plan sketch):** F2, F3, F4.
- **ONE ROAD (P31):** no exclusion without a data row. The threshold reuses `DESIGNER_THRESHOLD`, and the probe's no-probe cases go through the same `mutants_none` road. None found beyond that.
- **TESTS:** rows in existing tables, one parameterised table per behaviour, no new test file (§5.1, §5.2, §7.1). Within the volume rule. No `tests-over` needed at plan level.

## Not checked
- the current text of everything-in-piles r3 (it is moving; only §2.3 of the file on disk was read)
- whether boot-by-topic S2 has landed (PROJECT.md:364 still holds the mutation sentence, so not as of this read)
- architect-tier beyond its check 49 claim
- the run time of any narrow test file
- no test runs at all (plan gate)
- `docs/tasks/critic-diff-brief.md` beyond :50
- `test_handoff_rule_anchors.py` line pins
- the critic exam (absent)
- whether hygiene_gate refuses a Bash `cp` / `python -c` mutation by a critic inside another worktree (not probed: the plan must name the road first, B1)

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1 the critic probe (spec 3.2) runs NEW mechanics against CLAUDE.md rule 3 (critic does not execute an unattached layer, CLAUDE.md:78-81) and writes outside the handoff boundary (CLAUDE.md:237 R11-h, tools/handoff_gate.py:6-8); the plan amends neither and names no road -- choose: amend rule 3 + R11-h with a script road, or critic names mutants and a deterministic runner executes them",
    "B2 Lead decision L-5 (S-A waits for boot S2; S-B, S-C, S-D do not) contradicts spec 5.1 E-C2, section 8 and E-T1 (critic.md 17 + the brief probe + checker in one merge); S-B/S-C texts point at TESTING sections S-A creates -- split S-A into S-A1 (TESTING + brief, free of S2) and S-A2 (7b/7d, RUNBOOK, PROJECT; after S2)"
  ],
  "fixes": [
    "F1 reuse or extend ai-packages/qa-factory/scripts/tests/mutate_once.py as the probe runner (pytest form, root, timeout, collection error not a kill) or state why not",
    "F2 the mutants run join to trail.reruns is vacuous when mutants share the control command: require a distinct rerun per mutant or drop the claim",
    "F3 refusal display test vs skip item tests: one token (FR-2)",
    "F4 name the ITEMS iteration sites in check_cut (newly, still, _DISPLAY) or the new key passes silently",
    "F5 section 8: add spec-facts S2 (same file and check_cut) with an order",
    "F6 re-cut the P16 baseline by reading (t-816 false hit; canon, ratchet and pin-regime rejects are not the class); restate L-2 rationale",
    "F7 section 10: one line per axis (37), gate-shaped, per mechanism",
    "F8 the probe cap number only in the brief and the checker; pointers elsewhere (axis 31)",
    "F9 builder-rules 16 b: pointer clause for the red-before run",
    "F10 oracle: keep-exemption needs a named value or invariant; add input-derived values",
    "F11 count probe runs from transcripts in check 50 b; explicit runner timeout",
    "F12 name the first-dispatch edge of in-flight specs and its skip reason",
    "F13 field-generic predates door with everything-in-piles C; state M3 d depends on A2",
    "F14 drop CLAUDE.md from S-B owns; fill the O-2 date; mark L-2 provisional until O-3; section 2.4 number note; check 13 c stream"
  ],
  "class_completeness": "Axes 1, 2, 13, 17, 31, 32, 34 walked. In-scope siblings missing: CLAUDE.md rule 3 + R11-h + handoff_gate docstring (B1), mutate_once.py (F1), builder-rules 16 b (F9), cap restatements (F8), spec-facts S2 overlap (F5). Section 13 items 1, 2, 5, 6 correctly left; 3 handled by L-6; 7 fixed in 2.4.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-forge-test-rules-spec.md (whole)",
      "docs/TESTING.md:40-60, 85-135, 168-182",
      "docs/tasks/critic-diff-brief.md:1-50",
      "plans/builder-rules.md:30-125",
      "tools/dispatch_manifest.py:84-190, 254-280, 311-320, 727-740, 860-982",
      "tools/dispatch_new.py:1-30, 85-200",
      "tools/critic_verdict_check.py:60-175",
      "tools/critic_verdict.schema.json",
      "tools/handoff_gate.py:1-80",
      "tools/tests/test_role_carriers_one_owner.py:1-120",
      "ai-packages/qa-factory/scripts/tests/mutate_once.py",
      ".claude/agents/critic.md (front matter, rules 17, 20)",
      "docs/tasks/specs/20261117-everything-in-piles-spec.md:225-320",
      "docs/tasks/specs/20261116-boot-by-topic-spec.md (grep)",
      "docs/tasks/specs/20261116-spec-facts-by-code-spec.md (grep)",
      "docs/SIBLING_MAP.md:471-500",
      "PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md (check headings, 825-835)",
      "docs/DECISIONS_ARCHIVE.md:112",
      "docs/tasks/compact-snapshots/2026-11-17-0215-narrative.md:31-35",
      "logs/journal/dev1.jsonl (grep of rejected spec lines)"
    ],
    "reruns": [
      {"command": "Grep mutat -i over .github (control: python -i over .github)", "result": "0; control 82 in 5 files"},
      {"command": "grep -iE rejected.*spec.*(test|pin|тест) logs/journal/dev1.jsonl | wc -l", "result": "25 (68 spec, 118 rejected now); t-816 matches only via dropping"},
      {"command": "Grep dispatch_manifest / dispatch_new over tools (count)", "result": "144 in 24; 26 in 6 (matches spec 11)"},
      {"command": "Glob PROCESS/*EXAM*.md", "result": "DEPLOYMENT_ECONOMY_EXAM.md, LEAD_RANKING_EXAM.md (no CRITIC_EXAM)"},
      {"command": "grep -rnE [Мм]утац over PROJECT.md RUNBOOK AGENTS CLAUDE agents skills", "result": "PROJECT.md:364-365, RUNBOOK:115, AGENTS.md:379-380"}
    ]
  }
}
```

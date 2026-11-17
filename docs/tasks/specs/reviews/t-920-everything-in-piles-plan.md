# t-920 — critic on PLAN: «Всё в кучках» (spec t-907, `docs/tasks/specs/20261117-everything-in-piles-spec.md`)

Reviewer: critic (Opus). Object: the designer draft incl. the final section «The owner's word on leftovers (17.11.2026)»
(added mid-review by the coordinator's message; keys 2, 6, 7 judged against it). Nothing edited except this file; no test
set run. The verdict is an INPUT to the Lead's acceptance, not the acceptance (critic rule 6).

**Verdict: GO WITH FIXES — NEEDS WORK. Five blocking findings (B1-B5) must be fixed in the spec before any build
dispatch; ten non-blocking fixes (N1-N10).** A re-pass of the critic is owed only on B1/B2 (they change the
mechanism); the rest the Lead checks (PROJECT «Новая идея» п. 6).

---

## Key 1 — Facts by trail

All commands run from Git Bash with absolute paths (`R=/c/QAFactory/forge-repo`).

| # | spec claim | command (abridged where a loop) | result | state |
|---|---|---|---|---|
| P1 | 103 batches; 26 ожидает + 10 в работе + 67 закрыта | `ls $R/plans/piles/*/batch-*.md \| wc -l`; `grep -h "^кучка:" … \| grep -oE "статус: (…)" \| sort \| uniq -c` | 103; 10 в работе, 67 закрыта, 26 ожидает | confirmed |
| P2 | 103 of 106 node headers are the 7-column header | `grep -h "^\| *Узел *\|" … \| sed … \| sort \| uniq -c` | 103 × `Узел\|Приоритет\|Что\|Исполнитель\|Пишет в\|Зависит от\|Статус`, + 3 helper headers | confirmed |
| P3 | `NODE_COLS`/`NODE_REQUIRED` at piles.py:608-609 | `sed -n '600,615p' tools/piles.py` | at 608-609, no `Тип` | confirmed |
| P4 | ~698 waiting rows in 32 files | `grep -hE '^\| [^\|]+\|.*\| *ожидает[^\|]*\|\s*$' …/batch-*.md \| wc -l` and `-l … \| wc -l` | 691 rows, 32 files | confirmed (±1 %; shell grep vs Grep tool) |
| P5 | statuses at 111-115, `status_word` 200-206 | `sed -n '105,120p;195,210p'` | as stated | confirmed |
| P6 | backlog_tree's own words | not re-read | — | not re-checked (not load-bearing for this verdict) |
| P7 | (д) `_node_reds` refuses an unknown first word, 1855-1857 | `sed -n '1846,1870p'` | as stated | confirmed |
| P9 | leftover roads; lines | critic brief read whole (33-36, 55-58, 94-95 exact); `sed -n '2760,2860p;2925,3000p' tools/piles.py` | (a)-(e), (g), (h) as stated; **(f) builder-rules п. 1 is at line 10, not 8** (`sed -n '8,11p' plans/builder-rules.md`) | confirmed, one stale line no. (N1) |
| P10 | forge/7 «Ход» 86, 88, 89 | `sed -n '86p;88p;89p' …batch-7-vhodyashchie-4.md` | as quoted ("заведена узлами FG7-34 … FG7-35") | confirmed |
| P11 | close refuses bare `узел:` (2979-2981) | same read | `" -- a «узел:» item is closed by «сделано: …» when the node merges, or carried"` | confirmed |
| P12 | FINDINGS_FROM 2038; WARN baseline; count NOT MEASURED | `python -B $R/tools/piles.py check --all \| grep "(е)"` | `(е) findings: ok (1110 findings read, 0 dated from 2026-10-13 on are orphans, 152 older are the baseline)`; `WARN: 152 … or undated (69)` | confirmed, now MEASURED: 152 (69 undated) |
| P13 | 1110 findings, 33 piles | `ls …/findings/*.md \| wc -l`; `summary` line `кучек: 33` | 1110; 33 | confirmed |
| P14/P15 | Lead queue 10 done / 2 open (п. 11 boot, probe count lines) | `sed -n '1,26p' docs/tasks/lead-queue-fable.md` | as stated | confirmed |
| P16 | lead-queue-fable named by 4 files, no code | `grep -rl --exclude-dir=worktrees --exclude-dir=.git lead-queue-fable $R` | tracked: snapshot, architect spec, this spec, t-902 review, journal (+ untracked ledgers); no code | confirmed |
| P17 | debt header "25"; 47 rows + 3 walk entries; 6 "Closed by" (93-96, 98, 99) → 44 open | `grep -n "^\| " …factory-rules-debt.md` enumerated; `grep -n "Closed by"` | 11 + 18 + 16 + 1 + 1 = 47 data rows; "Closed by" at 93, 94, 95, 96, 98, 99; header says "Twenty-five rows are open today" | confirmed — **the owner's section repeats the stale "25"** (N8) |
| P18 | `factory-rules-debt` named in 54 files | `grep -rli … \| wc -l` | 60 (includes untracked ledgers/specs) | confirmed in substance |
| P19 | collect_intake builds rows from header, other columns `—` | `sed -n '979,1003p' tools/collect_intake.py` | `values = {"узел":…,"исполнитель":"Lead","пишет в":"нет","статус":"ожидает"}`, else `"—"` | confirmed (and see N6: temporal A→B window) |
| P20 | mechanism paths | `grep -n … tools/mechanism_gate.py` | piles.py 254, md_table 269, compact_snapshot 252, wave 281, CLAUDE.md, PROCESS/, .claude/agents/, SIBLING_MAP; no brief / builder-rules / PROJECT | confirmed |
| P21 | schema fields; no node field | `python -c "…json.load(schema)…"` | `['verdict','blockers','class_completeness','trail','fixes']`, required 4, **additionalProperties True** (a `nodes` array already passes the schema; only the check script would refuse) | confirmed |
| P23 | stale `board --check` allow lines 157, 176 | `grep -n board .claude/settings.json` | 157, 176 | confirmed |
| P25 | six plans list | — | needs t-895 trail | not checkable here (Lead) |
| P26 | BACKLOG open rows NOT MEASURED | `python -B $R/tools/piles.py summary` | `открытых id: 296 (в пачках 114 / в находках 182 / не разложено 0)` | now MEASURED |
| §2.1/forge7 | "batch 7 opened with 3 nodes, holds 54" | `grep -c "^\| FG7-"`; status loop; header | **54 nodes, 16 принято, 38 ожидает; header `статус: ожидает \| взял: —`; 28 commits** | confirmed — basis of B2 |
| legacy carries | (spec silent) | loop over non-closed batches, `awk '/^## Остатки/…' \| grep -c перенос:` | real `перенос:` items in taken batches: onboarding-hooks/5 (3 proof rows `перенос: live-runs`), onboarding-forge/2 (critic R3/R4 remarks), etc. | basis of B4 |

---

## Key 2 — Does it solve the owner's problem (t-906 numbers + the owner's per-origin word)

| origin (206) | owner's word | spec as written | stopped on the execution path? |
|---|---|---|---|
| critic, deferred minor (51) | «делать сразу» | default §2.2 + brief q4/q7 text | **text only** — see B1 |
| critic, other code / wider class (20) | «можно оставлять» | key `другая-кучка` = other pile's zone AND other class | stricter than her word (same-pile other-topic code is forced into the round) — B3 |
| owner's new word (31) | on-topic → now; off-topic → node | nothing; key `слово-владельца` means "needs an intent decision" — a different thing | not addressed — B3 |
| defect after acceptance / red CI (27) | «CI не записываем отдельными узлами» | silent; worse, §5.1 "every finding gets a node" + PROJECT «Как принимается» п. 2 (red `main` → «находка в `findings/`») would MAKE every red-CI finding a node, and (е) after FINDINGS_FROM removal would make a node-less one red | contradicts her word — B3 |
| scope cut by spec (24) | legal only if she cut for tokens; else do or ask | silent; no key fits, so it would be labelled `план` and pass | not addressed — B3 |
| calibration/process (27), new ideas (8) | — | legitimate nodes (`Откуда: находка`/`владелец`) | correctly out of scope |
| builder-noticed (14) | — | default §2.2 + builder-rules 5.11 | text only (B1) |
| live proof (4) | 11.11 word: live-runs | key `живой-прогон` | fine |

Best case, if every rule is obeyed: 51 + 14 + parts of 31/27/24 stop ≈ 40-55 % of the leftover stream; the spec never
says this to the owner (its §2.1 is still "[depends on t-906]"). State the expected effect honestly (N9).

**B1 — the 34 % critic share is closed by rule text, not by code.** What code refuses after stream A/C: (i)
`critic_verdict_check` refuses an unknown key in a `nodes` item — but the critic is free not to use `nodes` and the Lead
free not to read it; (ii) (д) checks the `остаток <node> · <key>` FORM only on rows that declare it; (iii) `close` refuses
b > a without `приток:`, where b counts only rows whose `Откуда` names a node of the batch. Every check keys on the
author's self-label: the 14.11 practice of P10 ("очередь критика … заведена узлами FG7-34, FG7-35") passes untouched
when the Lead writes those rows as `Откуда: находка` (with a finding file) or `план`. The owner's DoD was that the default
"holds on the execution path". Expected fix: name ONE code point on the acceptance road that reads the critic's verdict
block and refuses a node's `принято` (`piles.py status --set принято`, which `wave.py:208,224` calls) while an item of
that verdict's `fixes` / `nodes` is neither fixed in a later attempt nor carried as a row whose `Откуда` names the parent
and the key — a data xref (P27-clean); or, if the Lead rejects that, say plainly in §2.3 that the default rests on
discipline and register its detector (rule 10 (c)/(d)): a calibration item sampling NEW rows with `Откуда: находка|план`
added in the same commit window as a critic verdict of the same pile.

**B2 — the per-batch gate never fires on the batch the owner complained about.** forge/7 is `ожидает`, `взял: —`, yet 16
of its 54 nodes are `принято` (status loop above): forge works an UNTAKEN incoming batch node by node and never runs
`close` on it. The spec's per-batch brakes (the `close` flow line, `приток:` F6, the `узел:` back-reference at close)
all live in `close`; the «Остатки» gate is irrelevant there because leftovers are NODE ROWS appended to the same untaken
batch. Only the 7-day global line in `summary` sees it, and it refuses nothing. This is also a P31 seam: two roads of
working a batch (take→close vs work-in-untaken). Expected fix: either (a) the flow check fires per NODE at `status --set
принято` (rows born of that node since its last status move, needing `приток:`/a key), or (b) a node may not move to
`принято` in an untaken batch (taking becomes the one road); pick one, with the forge/7 example as the edge.

---

## Key 3 — Feasibility, order, collisions

- Streams have owns, test files (all exist: `ls tools/test_piles_form.py tools/test_piles_close_gate.py tools/test_piles.py
  tools/test_piles_findings.py tools/piles_testkit.py tools/test_critic_verdict_check.py tools/test_backlog_tree.py
  tools/test_collect_intake.py` → all present) and chosen directions — except where forks remain.
- **Stream F is void** under the owner's word (debt rows fixed now, not migrated) — B3.
- Stream A is one node over the 3482-line mechanism file with nine features (columns, vocab, (д), `план:`, back-ref write
  and close, F4/F5/F6, flow counter via `git log -p`, debt_warnings, template). Split into sequential nodes by function
  list (D-0048): A1 vocab+columns+(д); A2 leftover forms/close; A3 flow counter (N5). H also owns piles.py — sequential
  after M1, fine.
- G owns `plans/piles/package-ci/`; E-k groups exclude only forge, so a group with package-ci collides with G (N4).
- Collisions with the parallel specs (`grep -oE … | sort | uniq -c` over both): architect-tier edits `.claude/agents/critic.md`
  (rule 9), `.claude/settings.json`, `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`, `tools/mechanism_gate.py`,
  `session_context.py` and rewrites CLAUDE.md sections (its stream L); boot-by-topic rebuilds CLAUDE.md/PROJECT.md homes.
  This spec's C (critic.md 5.10), D (CLAUDE.md 5.6-5.8) and H (settings.json, WEEKLY, mechanism_gate) touch the same files.
  F12 names only the PROJECT overlap. All are Lead-placed, so not fatal, but the order lines are missing (N3).
- F12 granularity: boot-by-topic rows 2c, 2d, 9a, 9b go to `docs/TEAMWORK.md`; 9c («перенос подтверждает человек»),
  9d («Остатков в идеале нет»), 9e stay in PROJECT (`sed -n '290-308p'` of that spec). So 5.1 edits TEAMWORK §2 (if it
  lands first), 5.3 edits PROJECT, and F4/F5 must edit BOTH 9a (TEAMWORK) and 9c (PROJECT). Also boot-by-topic's move
  criterion is "a gate refuses it": if B1 adds a gate, 9d's classification shifts (N10).
- F7 vs architect-tier: that spec is accepted with F8(a) (`git mv` to `lead-queue.md`, new `architect-queue.md`, counted by
  `session_context.py`, named in `mechanism_gate._tier_queue_note`, calibration check 49(b), SIBLING_MAP «Lead Queue»).
  Retiring the file means amending those readers; the spec's E19/F7 does not list them (N7).

## Key 4 — Architecture and principles

- P31: one table, one parser, one leftover form (F4 a), (е) single rule after M1 — good. Open seams: B2 (two roads of
  working a batch); the red-CI finding would need a (е) exemption or a different road (B3).
- P27 / AR-29: (д) checks shape/xref; `приток:` is a presence check; "does the key hold" stays with the Lead — clean. One
  soft spot: `collect_intake` writes `Тип: баг` by default (`intake_default`) — code picking a work type; acceptable only as
  FR-59's declared default with the row visibly marked for the Lead (N6).
- FR-4: `приток:` is an informed pass — fine. FR-1/FR-2/P15: the refusal TEXTS of the new `close` b>a refusal, the
  `Откуда` form red, the `план:` red and the back-reference red are not written; only the critic-check text is (N6).
- FR-40: every new state has an exit (`отклонено: возвращён в <parent>`, key-nodes close normally) — fine.
- Frozen rule (п. 2): migration skips taken batches (F9 a) and writes «Ход» only — respected; but see B4 for what F4 does
  to legacy items in those same taken batches.

## Key 5 — Edges the spec is silent on

**B4 — both worlds of F4 and of the new columns are not stated.**
(a) Legacy `перенос:` items already written in «Остатки» / «Живые доказательства» of the 10 taken batches (e.g.
onboarding-hooks/5: three `перенос: live-runs` proof rows; onboarding-forge/2: critic R3/R4 carries) — after stream A
under F4(a), `close` refuses them, and rewriting each as `узел:` needs a node with a back-reference in another pile. The
spec must say: grandfathered (items present at the base stay legal at close) or migrated by a named stream.
(b) Adding `Тип`/`Откуда` to an untaken table changes the TEXT of every row, so under the multiset rule the spec cites
(F6-30) every row becomes "new or changed" and needs a `Тип` and an `Откуда` — contradicting "old rows legal, counted in
`без типа`" (E9) and M1, which edits untaken tables. Fix: row identity = node id + the old seven cells; and name the value
an old row carries after the column lands (`—` legal only for an id present at the base).

Other silent edges (N6): `Откуда: находка` — must the named finding exist?; `план:` path later renamed/deleted (which
commit goes red, given the carrier-scoped reds); `Откуда: владелец <дд.мм>` without a year across a year boundary; a
near-miss separator (` - ` or `.` instead of U+00B7) — red text should name the character; the A→B window where
`collect_intake` still writes 7 columns or `—` into the new columns and (д) refuses its row.

## Key 6 — Rule texts (§5) vs the tension and the owner's list

- The brief edits (5.9) remove the `queue` severity and the `перенос:` road; critic.md 5.10, CLAUDE.md 5.7/5.8, builder-rules
  5.11 aligned. Remaining carriers saying the old thing: **`PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` check 39** (line 1095:
  "(д) refuses … without `сделано:` / `узел:` / `перенос:`", the human-confirmation reading) — not in §5 nor in stream H
  (N2); PROJECT «Как принимается» п. 2 (red `main` → finding) — collides with her CI word (B3).
- **B5 — the owner's "and a check keeps it so" has no carrier.** Her word: the brief is a service file that must never
  contradict the main rules. The spec rewrites the brief but adds nothing that detects the next divergence; rule 10 (c)/(d)
  unanswered for that duty. The existing mechanism for exactly this class is axis 31 / `tools/tests/test_role_carriers_one_owner.py`
  (K-OWN one owner per aspect, K-PTR pointers). Its own docstring names the blind spot "a restatement in another language
  does not match an English key" — PROJECT is Russian, the brief English — so the fix is structural: the brief STOPS
  restating the leftover rule and carries a K-PTR pointer to its owner (PROJECT/TEAMWORK п. 9), plus a calibration item
  for the semantic drift the pointer cannot see.

**B3 — §2.2, §5 and forks F2/F5/F8 diverge from the owner's per-origin list (which the section says IS the criterion):**
1. `другая-кучка` requires another pile AND another class; she said "code outside the node's topic may be left". Rename to
   that condition (other code than the node's topic/`Пишет в`), keep rule 9's same-class sweep explicitly as hers or ask.
2. `слово-владельца` ("needs an intent decision") is not her rule: she said on-topic new word → do now, off-topic → node
   (that is `Откуда: владелец`, not a leftover key); a scope question → ask her, then do. The key as written lets a remark
   leave as a node by asking; replace with her two branches.
3. `живой-прогон` is backed by her 11.11 word (cite it); `занятый-файл` and `ждёт-события` are NOT in her list — "exactly
   the owner's list" means they go to her as a question (recommendation: not nodes — a second round of the same node after
   the blocking event), never kept by the designer.
4. Red CI / defect after acceptance: add the rule "repaired on the spot, no node" to §2.2 and 5.3, change PROJECT «Как
   принимается» п. 2's "находка в `findings/`" so no node-less finding is born (else (е) goes red after M1); her word names
   CI only — whether a non-CI defect after acceptance follows it is a question to her (recommend: same; the fix is a new
   task_id with `defect_found`, CLAUDE.md rule 4 forbids reopening).
5. Scope cut: add "a spec non-goal that defers in-topic work is legal only with her quoted token-saving word; else do or
   ask" — to §2.2, 5.3, and as a critic-on-plan key (designer rule / brief q12-style), with `доделка` rows citing that word.
6. F8 / M3 / stream F / §5.5 / §4 `debt_warnings` widening / `строки долга без node` in summary: all pre-decide F8(a);
   her word is "fix now, fate after it is empty". Remove stream F and §5.5; keep the `долг` type (it is in her five).
7. F2: matches her word (a). F5: the section's title says it binds F5, but its text answers nothing on who confirms —
   F5 is still OPEN for her (and today's «перенос подтверждает человек» is her rule).

## Key 7 — Forks

- F1 OWNER — correct (her vocabulary; she named five). F2 — decided (a), matches.
- F3 Lead — sound; cost of `git log -p` must be measured by A3 (stated).
- F4 Lead — sound as a form change (P31), PROVIDED B4(a) and F5 keep her confirmation semantics; it edits her 11.11
  live-runs sentence (9a, 9f) in form only.
- F5 OWNER — correctly hers; still open (B3.7).
- F6 Lead — sound only with B2 fixed (otherwise it brakes batches that close, not the ones that grow).
- F7 "OWNER/Lead" — the owner already decided the substance (spec lines 12-14: "the Lead queue … become nodes"); what
  remains is the Lead's amendment of the accepted architect-tier spec; mark it Lead and list its readers (N7).
- F8 OWNER — answered by her differently from all three options (B3.6).
- F9, F11, F12 Lead — sound (F12 widened by N3/N10). F10 marked OWNER — conservative; deleting done finding files is
  reversible (git) and technical, so Lead could decide with a «решила сама» line; harmless either way.

## DUPLICATION AND CONSISTENCY / CODE QUALITY / ONE ROAD / TESTS (standing lines, plan gate)

- Duplication: the spec itself removes one (backlog_tree's status words → `piles`); the new vocab has ONE reader
  (`node_vocab`). The brief/PROJECT double statement of the leftover rule is the duplication B5 addresses. Grepped:
  `grep -rniE "proposed node|Needed from integration|fix before merge|минорн|остатк"` over `.claude/agents/`, builder-rules,
  CLAUDE.md, SIBLING_MAP, WEEKLY, RUNBOOK → critic.md:169, builder-rules:10, WEEKLY:1095 (check 39, N2).
- Code quality: no code yet; Stream A size is the risk (N5).
- One road: B2 (two batch-working roads), B3.4 (red-CI finding road); otherwise one table/one form/one (е) rule.
- Tests: one row per behaviour in existing files, E15 battery one parametrised table — consistent with `docs/TESTING.md`;
  the battery applies to a data file a person edits (outside input) — correct.

## Fixes (non-blocking)

- N1 P9(f): builder-rules п. 1 is line 10. P12, P26 now measured (152 / 69 undated; 296 open ids) — write them in.
- N2 add WEEKLY check 39 to §5 and stream H (it describes `перенос:` and the human-confirmation reading).
- N3 order lines for CLAUDE.md (three specs), critic.md, settings.json, WEEKLY, mechanism_gate.py with architect-tier and
  boot-by-topic.
- N4 exclude `package-ci` from E-k groups (G owns it), or move test-diet rows to an E-k node.
- N5 split stream A into A1/A2/A3 by function list, sequential.
- N6 write the refusal texts (what is wrong / expected / door) for every new red; state the silent edges of key 5; mark
  `intake_default` rows for the Lead; close the A→B temporal window (B merges with A, or A's (д) accepts intake rows
  until B lands — pick one).
- N7 F7: relabel Lead; list architect-tier readers to amend (`session_context.py` count, `mechanism_gate._tier_queue_note`,
  check 49(b), SIBLING_MAP «Lead Queue»).
- N8 tell the debt-fix stream the open count is 44 by the file's own rows, not the header's "25" the owner quoted.
- N9 state to the owner the expected reduction against the t-906 table (which origins stop, which stay legitimately).
- N10 F12 at fragment level (2c/2d/9a/9b → TEAMWORK; 9c/9d/9e stay) and boot-by-topic's gate criterion shift if B1 adds a gate.

## Class completeness

Class: "a remark leaves its node by a road that costs less than the fix". Roads walked: brief q4/q7/q12(d), critic.md
5/19, CLAUDE.md 9/12, builder-rules п. 1, piles.py write/close gates, WEEKLY check 39 (missed by spec, N2), PROJECT
«Как принимается» п. 2 red-CI finding (missed, B3.4), spec non-goals (missed, B3.5), untaken-batch node appends (missed,
B2). SIBLING_MAP axes not re-walked by me beyond the spec's named axes 1/4/18/34 (the committer's enumeration, rule 10).

## Trail

Read: the spec whole (1-555 incl. the owner section); `docs/tasks/critic-diff-brief.md` whole; `tools/piles.py` 105-120,
195-210, 600-615, 1846-1870, 2195-2220, 2760-2860, 2925-3000 + grep of defs; `tools/collect_intake.py` 979-1003;
`tools/critic_verdict.schema.json`; `tools/mechanism_gate.py` grep; `factory-rules-debt.md` table enumeration + headings;
`docs/tasks/lead-queue-fable.md` 1-26; `plans/piles/forge/batch-7-vhodyashchie-4.md` header, node statuses, 86-89;
`PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` 1095-1112; `plans/builder-rules.md` 8-11; `tools/tests/test_role_carriers_one_owner.py`
1-30; boot-by-topic spec rows 290-308 + greps; architect-tier spec greps (lead-queue, critic.md, mechanism_gate).
Reruns: `piles.py check --all` (е) lines and `piles.py summary` (outputs quoted in key 1); counting greps as listed.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1 s2.2-2.3: the critic-remark default is closed by rule text and self-labelled Откуда only; name one code point on the acceptance road (status --set принято reading the verdict fixes/nodes) or declare discipline with a registered detector",
    "B2 s2.4/s4: per-batch flow and приток gates live in close, but forge/7 is worked untaken (ожидает, 16 of 54 принято) and never closes; fire the check per node at status принято or forbid принято in an untaken batch",
    "B3 s2.2/s5/F2/F5/F8: diverges from the owner's per-origin list: другая-кучка stricter, слово-владельца not her rule, занятый-файл and ждёт-события not in her list, red CI and scope cut silent (PROJECT Как принимается p.2 makes red CI a finding and so a node), stream F/M3/5.5 pre-decide F8, F5 still unanswered",
    "B4 s5-6 edges: legacy перенос items in taken batches become unclosable under F4(a); adding columns makes every row changed under the multiset rule, contradicting E9",
    "B5 s5.9: the owner's check that keeps the brief consistent with the main rules has no carrier; use axis 31 K-PTR pointer instead of restating, plus a calibration item"
  ],
  "fixes": [
    "N1 P9(f) line 10 not 8; write measured P12 (152, 69 undated) and P26 (296 open ids)",
    "N2 add WEEKLY check 39 to s5 and stream H",
    "N3 order lines for CLAUDE.md, critic.md, settings.json, WEEKLY, mechanism_gate.py with architect-tier and boot-by-topic",
    "N4 exclude package-ci from E-k groups",
    "N5 split stream A into A1/A2/A3 by function list",
    "N6 refusal texts with doors for every new red; silent edges (finding existence, plan path renamed, dd.mm year, separator near-miss, A to B intake window); mark intake_default rows",
    "N7 F7 relabel Lead and list architect-tier readers to amend",
    "N8 debt open count is 44 by the file rows, not 25",
    "N9 state the expected reduction against the t-906 table to the owner",
    "N10 F12 at fragment level and boot-by-topic gate-criterion shift"
  ],
  "class_completeness": "Class: a remark leaves its node by a road cheaper than the fix. Walked: brief q4/q7/q12d, critic.md 5/19, CLAUDE.md 9/12, builder-rules p.1, piles.py write and close gates (covered by spec); WEEKLY check 39 (missed, N2), PROJECT Как принимается p.2 red-CI finding (missed, B3), spec non-goals (missed, B3), untaken-batch node appends (missed, B2). SIBLING_MAP axes beyond 1/4/18/34 left to the committer's rule-10 enumeration.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-everything-in-piles-spec.md",
      "docs/tasks/critic-diff-brief.md",
      "tools/piles.py",
      "tools/collect_intake.py",
      "tools/critic_verdict.schema.json",
      "tools/mechanism_gate.py",
      "ai-packages/qa-factory/design/factory-rules-debt.md",
      "docs/tasks/lead-queue-fable.md",
      "plans/piles/forge/batch-7-vhodyashchie-4.md",
      "PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md",
      "plans/builder-rules.md",
      "tools/tests/test_role_carriers_one_owner.py",
      "docs/tasks/specs/20261116-boot-by-topic-spec.md",
      "docs/tasks/specs/20261116-architect-tier-spec.md"
    ],
    "reruns": [
      {"command": "python -B tools/piles.py check --all (the (е) lines)", "result": "1110 findings read, 0 dated from 2026-10-13 on are orphans, 152 older are the baseline; WARN 152 ... or undated (69)"},
      {"command": "python -B tools/piles.py summary", "result": "кучек: 33; пачек: ожидает 26, в работе 10, закрыта 67; открытых id: 296"},
      {"command": "grep -c node rows and status loop on forge batch 7", "result": "54 nodes: 16 принято, 38 ожидает; header статус ожидает, взял —"},
      {"command": "grep waiting rows over batch-*.md", "result": "691 rows in 32 files"},
      {"command": "grep перенос in Остатки/Живые доказательства of non-closed batches", "result": "real перенос items in taken batches, e.g. onboarding-hooks/5 three live-runs proof rows, onboarding-forge/2 critic carries"}
    ]
  }
}
```

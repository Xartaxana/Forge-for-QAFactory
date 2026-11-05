# t-618 critic-on-plan: F2-8 spec t-616 (`docs/tasks/specs/t-616-f2-8-piles-findings-gate.md`)

**Verdict: fit_with_fixes.** No blocker; every anchor confirmed at its carrier (two inaccuracies: piles_split :334 is a
findings loop, not a load_tree call; `пачка 2` does not need its target put first — the fixture card has ROW2
"ожидает", piles_testkit :111/:122). The Q5 item rule as written contradicted §5; the gate kept two silent passes of
today's section locator; the rename pairing could name the wrong file as new.

Lead's disposition 09.10: the spec is amended by the Lead (section 7) with F-1..F-7 and F-9; F-8 decided — the non-goal
is lifted for `plans/piles/_template/batch.md` (the «Остатки» comment must state the new item rule, SIBLING_MAP :270);
F-10 queued on Axis 12 by the Lead at merge (finding_fields :1885/:1894 twins; the N5 row WARN reaches only pre-freeze
bases because (г) refuses new rows).

## Answers
1. Facts: Finding :609-617/:620-644, gate :1977-2049, finding_date :322, monkeypatch :447, CHECKS :1587, piles_split :663,
   piles_gitlab :655, MECHANISM_PREFIXES :221-223 — confirmed.
2. Real data: batch-1 at ff353757 «Остатки» :54-64 = 8 single-line column-0 bullets with `сделано:` → today PASS, the
   new rule (model) PASS. batch-2/3/4 and the template hold only the template comment → `([], None)`. No prose, fence,
   sub-bullet or indented line outside a comment anywhere; batch-2 :57 has an inline same-line comment, harmless.
3. Q6: close stages nothing (`apply_changes` writes and unlinks; :2128 prints `Next: git add`); close runs on main after
   the merge. `ls-files -z --cached` probe: modified-unstaged listed (passes); `rm --cached` not listed but on disk (the
   git-add door is right); `git rm` absent from both; `git mv` lists only the destination; outside a repo rc=128.
   `piles.git` returns (rc, bytes); decode as `staged_paths` :776 does.
4. Q3 pairing: (a) base `20261008-dubl.md`; now `B-480-dubl.md` (renamed) AND a new `20261009-dubl.md` → sorted pairing
   matches the new one to the old file; if unclassified, `findings_unclassified` hides it. (b) close deletes
   `B-200-cleanup.md` and a new `20261009-cleanup.md` appears → paired and hidden. `str` sort deterministic; `Path`
   sort on Windows ignores case.
5. Error direction: (a) a commit staging only tools/*.py returns before load_tree (:1624) — correct; a different staged
   finding matches CARD_OR_FINDING_RE → the red; (b) close is strict (:2092, :2145) so `fl[0]` is never unreadable;
   (c) forge_metrics `--check` WARNs, never an offender (:1117-1123), only for findings new to the base; CI
   `check --all` is red on every push — the spec said neither.
7. Twins: the header locator (moved finding_date 8 lines vs parse_finding 5 lines under the heading; finding_fields
   :1894 a third copy; 0 of 206 real files disagree); the slug (N4 vs FINDING_NAME_RE :75); comment blanking (:1885,
   :1993; md_regions has no comment kind — control 6 KIND_ constants); the «Остатки» locator (`_frozen_lines`
   :1343-1348 vs `leftover_bullets` disagree on fences/comments while :1991 says they match); `_incoming` :831 (Q8).

## Findings
| # | Severity | Finding |
|---|---|---|
| F-1 | fix spec (Q5, N7, §5) | "keys on the JOINED text" refuses p10 (`сделано: t-1 продолжение…` fails LEFTOVER_DONE_RE); Q5's "not starting a bullet" refuses p9; §5 said both stay. Replacement: an indented (2+ spaces) non-marker line is appended to its item as a new ` \| ` segment; an indented marker line is an item of its own; a tab-indented line is an item of its own; p10 stays passing, p9 moves to the refuse test. |
| F-2 | fix spec (N7, Edges, §6) | Two silent passes today: an unclosed fence in «Ход», and an inline `` `<!--` `` in «Ход» pairing with the template's `-->` hide the heading ("- undone, no keys" passes). Replacement: the section is found on raw column-0 `## ` lines as `_frozen_lines` does; comments are blanked inside the section only; an unclosed `<!--` there refuses; a stray `-->` is an item; Edges row → "a comment cannot hide the section: refused"; M15 "a fence in Ход hides the section". |
| F-3 | fix spec (N4) | Pair only when the (pile, slug) has exactly one unmatched P and one unmatched Q; the slug is a named group of FINDING_NAME_RE imported by forge_metrics; an empty slug or a rejected name is never paired; a Q whose name id is in `backlog.closed_ids` is not a rename source; otherwise the file is new. Tests for (a) and (b). |
| F-4 | fix spec (N1) | The `от:` fallback reads parse_finding's own `pairs`, not an 8-line rescan; both regexes move to piles.py and leave compact_snapshot; the no-header return (:636) also carries date and text. |
| F-5 | fix spec (N6, §5) | `leftover_problem(pairs)` stays pure (tests :224-254 call it with one argument); existence in a separate function called after the form passed; `check_leftovers(text, rel)` keeps 2 positional args (:125), extras as keywords; the deleted set comes from whole not-yet-closed members via `findings_by_id()` across piles, without `_plan_batch_close` (the gate stays before the plan, :113). |
| F-6 | fix spec (§5) | `пачка 2` does not flip; test :128 → `leftover_items(template) == ([], None)`; one forge_metrics WARN per unreadable finding (:915 "warned once") and ONE (д) red (not pile.errors' generic red plus N2's). |
| F-7 | fix spec (§3) | forge_metrics: WARN only for findings new to the base; CI `check --all`: red until fixed or `piles-skip: д` in the pushed range; `board --check`: exit 0 with the WARNING. |
| F-8 | Lead | SIBLING_MAP :270: a format change goes to the templates in the same commit; the non-goal forbade the templates while the template comment still says «строка-пункт… без пунктов — можно закрывать». Decided: lifted for `_template/batch.md`. |
| F-9 | builder note | "Staged in the same close" = staged before running close; the refusal says "then run close again"; `пачка N` judged by `View.status` (P7: the file leads); "non-empty" = `strip()`; `rebuild_board` :1805 is strict. |
| F-10 | Lead / queue | Axis 12 next to Q8: finding_fields :1885/:1894 (comment regex, 8-line window); the N5 row WARN reaches only pre-freeze bases. |

## Trail
Read: the spec; t-615 review; piles.py :100-224, :590-1100, :1165-1194, :1334-1363, :1560-1700, :1795-1830,
:1875-2185; forge_metrics.py :80-104, :415-589, :1085-1184; compact_snapshot.py :310-389; gitcmd.py; piles_testkit.py;
test_piles_close_gate.py (whole); test_piles_split.py :436-455; test_forge_metrics.py :840-971; test_compact_snapshot.py
:220-289; B-471; B-472; batch-1 at ff353757/e17cd017; batch-2/3/4 and the template «Остатки»; SIBLING_MAP :253-270;
mechanism_gate :183, :215-225; .gitlab-ci.yml :72-89; the verdict schema. Greps: `^## Остатки` -i over plans: 5;
`<!--` over tools/*.py: piles :1885, :1993 (+ tests); `KIND_|comment` -i in md_regions: no comment kind (control 6
KIND_); `перенос:|leftover_bullets|finding_date|load_tree\(|LEFTOVER_OK` over tools: 40; `name_id` in piles: 4.
Probes (scratchpad): batch-1 today PASS / new rule PASS; p9, p10 REFUSE under the draft rule; the two «Ход» holes pass
silently today; header windows disagree on 0 of 206 real findings (116 dated); the ls-files matrix; rc=128 outside a
repo. Reruns: `python -m pytest tools/test_piles_close_gate.py -q -p no:cacheprovider` → `87 passed in 49.51s`;
`python tools/piles.py check --all` → `piles check: ok`.

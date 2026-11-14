# t-864 report

Part 1: branch `piles/owner-words-1411` (from origin/main), pushed, not merged. Batch is NOT taken ("ожидает"), so not frozen. Edited `plans/piles/live-run-fvf/batch-2-live-run-fvf.md` and `README.md`.
- FV2-79 row: "S1 вопрос владельцу" replaced by "S1 решён: вариант A, «ок, оставляем» (владелец, 14.11.2026)"; card row "решение владельца" column and the «Вопросы владельцу» S1 bullet marked ОТВЕЧЕНО.
- FV2-92 row: owner decision (yes, after two fixes: S8 bug-reporter form created before the work; required/optional marks in the form file; measurement on a run) written in the "Что"; the dependency changed from «слово владельца да/нет» to the two fixes + measurement; status still «ожидает». Card column "Q7" and the Q7 question bullet carry both verbatim owner quotes and the new idea (code assembles the handoff file; recon t-863; own node later).
- «Ход» line `14.11 (t-864)` added with both records.
Witness: `python -B tools/piles.py check --all` tail: `(д) form: ok (33 piles, 103 batches)` / `(е) findings: ok (1106 findings read, 0 ... orphans ...)` / `piles check: ok`. Also the commit-hook run printed `piles check: ok`.
`git show --stat` (piles commit): README.md 8 ++++----, batch-2-live-run-fvf.md 5 +++--, 2 files, 7 insertions, 6 deletions.

Part 2: finding found at `plans/piles/forge/findings/20261114-testing-md-podprocess-na-proverku-protiv-suhoj-istorii.md`. Branch `offload/a2-f1` from origin/offload/a2; added 3 lines in `docs/TESTING.md` after the "Время" bullet: "Исключение сухой истории (слово владельца 14.11.2026, спека ...p1b-dry-story-spec.md, §4.3): драйвер запускается процессом на строку обхода, на копии снимка («создавать `Driver` в процессе теста» в рецепте запрещено; время строки ограничено капом на строку, E6); лимит — потолок набора, не 10 с; другие файлы под правило." The reason is quoted from spec §4.3 (the "Запрещено в рецепте" clause and the row-cap line), with a short framing sentence; the finding told the designer to take it verbatim, so check the wording.
Push: `36ab846c..4699b563  offload/a2-f1 -> offload/a2` (fast-forward OK).
`git show --stat HEAD`: docs/TESTING.md | 3 +++, 1 file changed.
Key-presence script `t864_keys.py` (not committed, scratchpad):
```
import sys
t = open(sys.argv[1], encoding='utf-8').read()
keys = ["слово владельца 14.11.2026", "Исключение сухой истории", "драйвер запускается процессом на строку обхода"]
bad = [k for k in keys if k not in t]
print("MISSING" if bad else "ALL PRESENT", [k.encode('unicode_escape').decode() for k in bad])
sys.exit(1 if bad else 0)
```
Run on edited file: `ALL PRESENT []` rc=0. Negative control (file at HEAD~, before my edit): `MISSING [...Исключение сухой истории..., ...драйвер запускается процессом на строку обхода...]` rc=1. The first key already exists in the file (line 125, another exception), so the other two carry the proof.

Deviations/notes: the finding's item 2 (a test reading TESTING.md) was not investigated (no test written, out of owns). The finding says the edit waits for owner word on F2; the dispatch states owner said «ок» 14.11, used as given. The finding itself and the P1-b spec F2 status were not edited (non-goals); the finding's "Решение владельца нужно: да" line stays stale. The scratchpad name `keys.py` collided with a pre-existing file; discarded, used `t864_keys.py`. This report file is in the worktree (the shared path was refused) and is not committed.
Needed beyond the manifest: `plans/piles/forge/findings/20261114-testing-md-podprocess-na-proverku-protiv-suhoj-istorii.md`, `docs/tasks/specs/20261113-p1b-dry-story-spec.md`.
Siblings: none noticed.

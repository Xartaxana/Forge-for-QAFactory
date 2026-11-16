# t-918 — FG7-51 stream S3 (role and worker docs): handoff

DoD: `python -m pytest tools/tests/test_role_carriers_one_owner.py tools/test_handoff_rule_anchors.py -q -p no:cacheprovider`

## Output

```
.........................................................                [100%]
57 passed in 1.54s
```

`python -B <worktree>/tools/install_parity.py --check` (tail):

```
install_parity --check
ledger: C:\QAFactory\forge-repo\.claude\worktrees\agent-a73cd32db80a7245f\docs\ADOPTION_LEDGER.md

CLEAN units (46)

MISSING (0)

UNKNOWN (0)

informational (0)
```

`python -B <worktree>/tools/agents_md.py --check`:

```
AGENTS.md: up to date (123421 bytes)
```

Staged (not committed): `.claude/agents/designer.md`, `plans/builder-rules.md`, `docs/TESTING.md`, `docs/tasks/critic-diff-brief.md`, this handoff.
`git diff --cached --stat` (before the handoff was added): 4 files, 64 insertions, 21 deletions.

## DOC-DISPATCH run (spec 7.4) — script, full source (throwaway, kept in the session scratchpad, NOT committed)

Keys were typed from the spec rows before the run. Source = `git show HEAD:` version for S3-1, the file named in the row for the old text of the others.

```python
import sys, subprocess
sys.stdout.reconfigure(encoding="utf-8")
W = "C:/QAFactory/forge-repo/.claude/worktrees/agent-a73cd32db80a7245f/"
sq = lambda s: " ".join(s.split()).casefold()
def rd(p): return sq(open(W + p, encoding="utf-8").read())
def head(p):  # source = HEAD version
    return sq(subprocess.run(["git", "show", "HEAD:" + p], cwd=W, capture_output=True, encoding="utf-8").stdout)
D = "docs/TESTING.md"; R = "plans/builder-rules.md"; DS = ".claude/agents/designer.md"; B = "docs/tasks/critic-diff-brief.md"
P1 = "READERS OF EVERY TOUCHED FILE (the owner's word 16.11.2026): for each file a spec creates or changes"
P2 = "a ratchet on importers, two count pins)."
def rule7(t): return t[t.index(sq("7. READERS OF EVERY TOUCHED FILE")):]
def rule3(t): return t[t.index(sq("3. Freshness")):t.index(sq("4. Don't launch"))]
rows = [
 ("S3-1a", "K2", P1, DS), ("S3-1b", "K2", P2, DS),
 ("S3-3", "K5", "Мерджи, пуши, переключение веток — не билдер: принятое сливает координатор (`tools/wave.py merge`), пачку закрывает интегратор (`piles.py close`).", R, "Мерджи, пуши, переключение веток — только интегратор."),
 ("S3-4", "K5", "координатор запускает один прогон BATCH CANON", R, "интегратор делает один прогон BATCH CANON"),
 ("S3-5a", "K4", "не запускается, не чинится и не правится", D, "Файл карантина не запускается, не чинится и не правится", R),
 ("S3-5b", "K4", "его случай уходит строкой в сценарий или таблицу", D, "тест, показавший из карантина настоящий дефект, не возвращается", R),
 ("S3-5c", "K4", "Покрасневший пин удаляется, а не чинится", R, None),
 ("S3-6a", "K4", "--witness-for", R, None),
 ("S3-6b", "K4", "строки `keep`", R, None),
 ("S3-6c", "K4", "- **Что запускать по своей правке** — правило: `plans/builder-rules.md` п. 7b.", D, "печатает истории и строки `keep`, которые покрывают тронутые пути"),
 ("S3-7a", "K4", "Файл карантина билдер не запускает", R, None),
 ("S3-7b", "K4", "мутации судит канон пачки", R, None),
 ("S3-7c", "K4", "что запускает — `plans/builder-rules.md` п. 7b.", D, "мутации не перечисляет (слово владельца 28.10.2026"),
 ("S3-8a", "K4", "Не регрессия, не соседи, не большие файлы", R, None),
 ("S3-8b", "K4", "(the scope: `plans/builder-rules.md` 7b)", B, "the files `scenario_walk.py --witness-for <owns>` prints"),
 ("S3-8c", "K4", "## The two layers", B, None),
]
bad = 0
def rep(name, ok):
    global bad
    print(name, "yes" if ok else "no")
    bad += (not ok)
def run(rows, tag):
    for r in rows:
        i, k, key, f = r[:4]; old = r[4] if len(r) > 4 else None; srcf = r[5] if len(r) > 5 else f
        txt = rd(f); ks = sq(key)
        lbl = "present-in-home" if k == "K4" else "present-in-destination"
        if i in ("S3-1a", "S3-1b"):
            rep(f"[{tag}] {i} {lbl} (rule 7) key={key[:40]!r}:", ks in rule7(txt))
            rep(f"[{tag}] {i} absent-from-source (rule 3):", ks not in rule3(txt))
        else:
            rep(f"[{tag}] {i} {lbl} key={key[:50]!r}:", ks in txt)
            if old:
                rep(f"[{tag}] {i} absent-from-source (old text gone, in {srcf}):", sq(old) not in rd(srcf))
run(rows, "REAL")
hs = head(DS); a = hs.index(sq("READERS OF EVERY TOUCHED FILE")); e = hs.index(sq("two count pins).")) + len("two count pins).")
blk = hs[a:e]
rep("[REAL] S3-1 whole block (from HEAD) present-in-destination rule 7:", blk in rule7(rd(DS)))
rep("[REAL] S3-1 whole block absent-from-source rule 3:", blk not in rule3(rd(DS)))
rep("[REAL] S3-1 rule 3 keeps 'readers of every touched file: rule 7.':", sq("Readers of every touched file: rule 7.") in rule3(rd(DS)))
real_bad = bad
print("--- NEGATIVE CONTROL (one char altered; failure expected)")
bad = 0
run([("S3-6c-NEG", "K4", "- **Что запускать по своей правке** — правило: `plans/builder-rules.md` п. 7c.", D)], "NEG")
print("negative control reported failure:", bad > 0)
sys.exit(1 if (real_bad or bad == 0) else 0)
```

Output (command `python -B <scratchpad>/dd.py`, exit code 0 = every real key yes AND the negative control reported failure):

```
[REAL] S3-1a present-in-destination (rule 7) key='READERS OF EVERY TOUCHED FILE (the owner': yes
[REAL] S3-1a absent-from-source (rule 3): yes
[REAL] S3-1b present-in-destination (rule 7) key='a ratchet on importers, two count pins).': yes
[REAL] S3-1b absent-from-source (rule 3): yes
[REAL] S3-3 present-in-destination key='Мерджи, пуши, переключение веток — не билдер: прин': yes
[REAL] S3-3 absent-from-source (old text gone, in plans/builder-rules.md): yes
[REAL] S3-4 present-in-destination key='координатор запускает один прогон BATCH CANON': yes
[REAL] S3-4 absent-from-source (old text gone, in plans/builder-rules.md): yes
[REAL] S3-5a present-in-home key='не запускается, не чинится и не правится': yes
[REAL] S3-5a absent-from-source (old text gone, in plans/builder-rules.md): yes
[REAL] S3-5b present-in-home key='его случай уходит строкой в сценарий или таблицу': yes
[REAL] S3-5b absent-from-source (old text gone, in plans/builder-rules.md): yes
[REAL] S3-5c present-in-home key='Покрасневший пин удаляется, а не чинится': yes
[REAL] S3-6a present-in-home key='--witness-for': yes
[REAL] S3-6b present-in-home key='строки `keep`': yes
[REAL] S3-6c present-in-home key='- **Что запускать по своей правке** — правило: `pl': yes
[REAL] S3-6c absent-from-source (old text gone, in docs/TESTING.md): yes
[REAL] S3-7a present-in-home key='Файл карантина билдер не запускает': yes
[REAL] S3-7b present-in-home key='мутации судит канон пачки': yes
[REAL] S3-7c present-in-home key='что запускает — `plans/builder-rules.md` п. 7b.': yes
[REAL] S3-7c absent-from-source (old text gone, in docs/TESTING.md): yes
[REAL] S3-8a present-in-home key='Не регрессия, не соседи, не большие файлы': yes
[REAL] S3-8b present-in-home key='(the scope: `plans/builder-rules.md` 7b)': yes
[REAL] S3-8b absent-from-source (old text gone, in docs/tasks/critic-diff-brief.md): yes
[REAL] S3-8c present-in-home key='## The two layers': yes
[REAL] S3-1 whole block (from HEAD) present-in-destination rule 7: yes
[REAL] S3-1 whole block absent-from-source rule 3: yes
[REAL] S3-1 rule 3 keeps 'readers of every touched file: rule 7.': yes
--- NEGATIVE CONTROL (one char altered; failure expected)
[NEG] S3-6c-NEG present-in-home key='- **Что запускать по своей правке** — правило: `pl': no
negative control reported failure: True
```

(An earlier run of the same script printed one real `no` for S3-5b: the absence check was pointed at TESTING.md, where the phrase legitimately lives, instead of builder-rules; a script bug, fixed by naming builder-rules as the source file, not a text defect.)

## Rows

| row | status |
|---|---|
| S3-1 | done: whole paragraph moved verbatim to new rule 7 of designer.md; rule 3 ends with «Readers of every touched file: rule 7.»; the two 17.11 sentences in rules 1 and 6 untouched |
| S3-2 | done: 24 lines `### <n>. <bold title>` (1-20, 7a-7d), each above its opener with one blank line; openers byte-identical (`git diff -U0` shows no removed opener line; only the 3 edited rules S3-3/4/5 differ inside their text) |
| S3-3 | done |
| S3-4 | done |
| S3-5 | done, one sentence removed from 7d (see below); all others stay |
| S3-6 | done |
| S3-7 | done |
| S3-8 | done |

S3-5 decision per 7d sentence (key phrase in TESTING.md, outside any code fence):
- REMOVED «Файл карантина не запускается, не чинится и не правится; тест, показавший из карантина настоящий дефект, не возвращается — его случай уходит строкой в сценарий или таблицу.» — keys «не запускается, не чинится и не правится» (TESTING.md «Карантин старых тестов», «в каноне не запускается, не чинится и не правится») and «его случай уходит строкой в сценарий или таблицу» (same section, «Из карантина тест не возвращается: если он показал настоящий дефект, его случай уходит строкой в сценарий или таблицу»), both present; 7b also keeps «Файл карантина билдер не запускает, не чинит и не правит».
- STAY (key absent or only a paraphrase): «Тест — на поведение через дверь скрипта… тест стыка…»; «Правило роли охраняется… (до его появления…)»; «НЕ пишутся и при встрече удаляются: …» (TESTING table words differ); «Свидетель наличия ключей в тексте — вывод в отчёте…» (not in TESTING); «Бюджет: … `tests-over:` …» (TESTING phrase differs in backticks and words); «новый тестовый файл не создаётся: случай — строка `variants.json`… не дольше 10 с; мир драйвера…» (paraphrase only).
- «Покрасневший пин удаляется, а не чинится» stays (OWNER_KEYS `scope:tests`).

## Needed from integration

POINTERS rows for S2 (not mine, per non-goals): TESTING.md -> `plans/builder-rules.md` п. 7b (my S3-6 and S3-7 lines are the TESTING pointers) and critic-diff-brief -> 7b (my S3-8 parenthetical is the BRIEF pointer); S2 should add them to the POINTERS table in `tools/tests/test_role_carriers_one_owner.py` (rows: TESTING key «`plans/builder-rules.md` п. 7b», BRIEF key «`plans/builder-rules.md` 7b», both to RULES_7B). Also the new 7b text of S2 (B-1…B-7) must keep «Файл карантина билдер не запускает», «мутации судит канон пачки», «Не регрессия, не соседи, не большие файлы», «--witness-for», «строки `keep`» — S3 now depends on them.

## Deviations

- DOC-DISPATCH S3-1: the keys are the block's opening key (first words, since a block of this length would otherwise need first/last 60 squashed chars) and the clause ending «two count pins).» plus a whole-block comparison against the HEAD version; this covers the first/last-60 requirement and is stricter.
- Rule 3 of designer.md: the spec's «rule 3 keeps `Readers of every touched file: rule 7.`» is placed as the final line of rule 3.
- AGENTS.md regeneration not needed (CLAUDE.md/PROJECT.md/FACTORY_RULES_INDEX untouched); `agents_md.py --check` says up to date.
- CRLF/LF: heading insertion preserved the file's existing line endings.

## Questions

none

## Needed beyond the manifest

`tools/test_handoff_rule_anchors.py` (run by the DoD, read for its anchors); `docs/ADOPTION_LEDGER.md` (read by `install_parity.py`, not edited); `AGENTS.md` (checked only).

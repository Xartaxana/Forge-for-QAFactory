# t-939 — Architect tier, stream F (rule texts outside CLAUDE.md, deletions)

State: all changes STAGED in the worktree `C:/QAFactory/forge-repo/.claude/worktrees/agent-a27e965d90cc34002`, no commit, no push.
The handoff file itself is untracked (not staged).

DoD: `python -m pytest tools/tests/test_role_carriers_one_owner.py tools/test_calibration_counts.py -q -p no:cacheprovider`

## Output

```
$ python -m pytest tools/tests/test_role_carriers_one_owner.py tools/test_calibration_counts.py -q -p no:cacheprovider
........................................................................ [ 50%]
........................................................................ [100%]
144 passed in 2.95s

$ python -B keys_f.py <worktree>          (positive run)
ok   PROCESS/ARCHITECT_START.md has 'ARCHITECT_START'
ok   PROCESS/ARCHITECT_START.md has 'reviewed-through'
ok   PROCESS/ARCHITECT_START.md has '"event":"escalated","agent":"architect"'
... (every line ok; tail:)
ok   docs/ADOPTION_LEDGER.md lacks "onboarding skill's Upgrade mode"
ok   .claude/skills/critic-exam-gen/SKILL.md lacks "onboarding skill's Upgrade mode"
ok   .claude/skills/onboarding deleted
ok   .claude/skills/next-task deleted
ok   docs/tasks/lead-queue-fable.md deleted
RESULT: all keys ok
exit=0

$ python -B keys_f.py <worktree> --neg    (negative control: one key deliberately absent)
FAIL docs/tasks/architect-queue.md has 'KEY-THAT-IS-DELIBERATELY-ABSENT'
RESULT: FAILURES=1
exit=1
```

An earlier positive run failed once (key `"event":"escalated","agent":"architect"` was present only in its
backslash-escaped shell form inside the step-4 command); fixed by naming the plain journal pattern in the step text,
re-run green (above). The Cyrillic key `Очередь для Lead` is checked as UTF-8 (the console only mis-prints it).

## Key-presence script (full source, NOT committed; lives in the scratchpad)

Keys quoted verbatim from the spec block "### Stream F" items F1-F6 before the run.

```python
import sys, pathlib

ROOT = pathlib.Path(sys.argv[1])
NEGATIVE_CONTROL = len(sys.argv) > 2 and sys.argv[2] == "--neg"

# keys quoted verbatim from the spec block "### Stream F" items F1-F6
PRESENT = {
    "PROCESS/ARCHITECT_START.md": ["ARCHITECT_START", "reviewed-through", '"event":"escalated","agent":"architect"'],
    "PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md": ["run by an Architect session", "ranked below lead", "INDEPENDENT CONTEXT", "Architect tier", "refuses the value (FG7-16)"],
    "PROCESS/LEAD_RANKING_EXAM.md": ["FUNCTION_RANKS", "Architect", "distinguish a Lead candidate from the critic/builder"],
    "docs/TWO_VOCABULARIES.md": ["Architect"],
    "docs/SIBLING_MAP.md": ["Architect", "docs/tasks/lead-queue.md"],
    ".claude/agents/critic.md": ["below the Lead rank"],
    "docs/tasks/lead-queue.md": ["Очередь для Lead"],
    "docs/tasks/architect-queue.md": ["- [ ] <YYYY-MM-DD>"],
}
ABSENT = {  # negative keys of F4 (every F4 file)
    "PROCESS/PATCH_PROTOCOL.md": ["onboarding skill's Upgrade mode"],
    "docs/ADOPTION_LEDGER.md": ["onboarding skill's Upgrade mode"],
    ".claude/skills/critic-exam-gen/SKILL.md": ["onboarding skill's Upgrade mode"],
}
GONE = [".claude/skills/onboarding", ".claude/skills/next-task", "docs/tasks/lead-queue-fable.md"]

if NEGATIVE_CONTROL:
    PRESENT["docs/tasks/architect-queue.md"].append("KEY-THAT-IS-DELIBERATELY-ABSENT")

fails = 0
for f, keys in PRESENT.items():
    text = (ROOT / f).read_text(encoding="utf-8")
    for k in keys:
        ok = k in text
        fails += not ok
        print(("ok   " if ok else "FAIL ") + f + " has " + repr(k))
for f, keys in ABSENT.items():
    text = (ROOT / f).read_text(encoding="utf-8")
    for k in keys:
        ok = k not in text
        fails += not ok
        print(("ok   " if ok else "FAIL ") + f + " lacks " + repr(k))
for g in GONE:
    ok = not (ROOT / g).exists()
    fails += not ok
    print(("ok   " if ok else "FAIL ") + g + " deleted")
print("RESULT:", "FAILURES=%d" % fails if fails else "all keys ok")
sys.exit(1 if fails else 0)
```

## Item -> files changed

| item | files |
|---|---|
| F1 | `PROCESS/ARCHITECT_START.md` (new): eight steps of spec 4.5, step-4 grep command and step-8 `journal_write.py calibrated --reviewed-through` command verbatim; step 5 carries the 4.6 review criteria; step 7 points the boot-budget item to `docs/tasks/lead-queue.md` |
| F2 | `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`: header sentence (run by an Architect session); check 5 (rank_of_model, Architect is not degradation); check 6 (rank_of_model, «queued for the Lead», added items i-iii); check 18 (coordinator model = lead binding); check 20 (validator refuses the value FG7-16); new check 49 «Architect tier» (a)-(d) + empty-window line + own-leak detector |
| F3 | `PROCESS/LEAD_RANKING_EXAM.md`: purpose lines 3-4; ceiling-case text now `FUNCTION_RANKS` in `tools/tier_ladder.py`, plus «Fable (Architect) judges an Opus candidate» |
| F4 | `PROCESS/PATCH_PROTOCOL.md` (parenthetical dropped; parity duty kept in its own words), `docs/ADOPTION_LEDGER.md` (5 references -> «retired 16.11.2026 (D-nnnn)», D-nnnn is the placeholder for stream L's decision number), `.claude/skills/critic-exam-gen/SKILL.md` (lines 163, 182); deleted (staged): `.claude/skills/onboarding/SKILL.md`, `.claude/skills/next-task/SKILL.md` |
| F5 | `docs/TWO_VOCABULARIES.md` (Lead row -> Opus, new Architect row, vocabulary list); `docs/SIBLING_MAP.md` (next-task and onboarding rows of axis 31 deleted; Lead-queue sentence -> `docs/tasks/lead-queue.md`; axis 1 table row «Ladder home»; axis 2 Lead-exam row note; no heading renamed); `.claude/agents/critic.md` rule 9 «below the Lead rank» (rule 10 untouched) |
| F6 | `docs/tasks/lead-queue-fable.md` -> `docs/tasks/lead-queue.md` (`git mv`, retitled «Очередь для Lead», header text updated incl. the Opus-outage line «ждёт критика», both OPEN items untouched); `docs/tasks/architect-queue.md` (new, item form of 4.4, no items) |

## Deviations / facts

- The brief said `lead-queue.md` does NOT exist today and only `lead-queue-fable.md` does: confirmed; I `git mv`-ed it as F6 says.
- F22 outage text: the Lead-queue header names the wait-for-critic line of 5.3 item 2; the F22 stand-in clause (Fable stand-in dispatch legal for a declared outage) lives in CLAUDE.md rule 6 / Lead degradation (stream L). No F1-F6 item carries the outage text, so none was added elsewhere.
- critic.md: exam not re-run: wording only (rule 9, rank's name only; no duty changed).
- `tools/tier_ladder.py` exists in this worktree (checked with Glob, positive hit), so the `FUNCTION_RANKS` / `tier_ladder.py` references point at a real file. `FUNCTION_RANKS` occurs 12 times in it (Grep count).
- No axis-2 or 31 row for ARCHITECT_START.md / architect-queue.md was added to SIBLING_MAP (spec 6 does not ask for it).
- `D-nnnn` placeholders in ADOPTION_LEDGER.md are literal, as the spec writes them; stream L / Lead fills in the number.

## Questions

none

## Needed beyond the manifest

- `tools/mechanism_gate.py` and `tools/test_mechanism_gate.py` (grep for `lead-queue` to confirm the path text, already pointing at `docs/tasks/lead-queue.md`).
- `docs/SIBLING_MAP.md` lines 1-60 and 471-530 (axis 1, 2, 31 tables).

## Noticed analogs (not changed)

- critic-exam-gen/SKILL.md lines 3, 37, 49 and the description use "onboarding" as a generic word (an event, not the retired skill); left as is.
- `docs/tasks/lead-queue.md` body items (the 11 numbered items) still say «Fable» in places: history, left.

## Fix round (critic t-946)

F-2, PROCESS/ARCHITECT_START.md step 5, lines 28-29.

Old (line 29): "none yet means the date of the commit that landed this checklist."

New (lines 28-30, line 29): "none yet means the date of the stream-L commit (the Architect landing); if no review has happened yet and that commit has not landed, there is nothing to review before the Architect landing."

Siblings (grep "landed this checklist|Architect landing" in PROCESS): ARCHITECT_START.md:29 fixed; WEEKLY_CALIBRATION_PROTOCOL.md:1129 contains "Architect landing" - consistent (not an alternative start-date definition; not in owns).

DoD script (not committed):
```python
import sys,re
t=open(sys.argv[1],encoding='utf-8').read()
t=re.sub(r'\s+',' ',t)
for k,want in (("the stream-L commit (the Architect landing)",True),("the commit that landed this checklist",False)):
    ok=(k in t)==want
    print(("PRESENT" if want else "ABSENT"),repr(k),"->","PASS" if ok else "FAIL")
```
Output:
```
PRESENT 'the stream-L commit (the Architect landing)' -> PASS
ABSENT 'the commit that landed this checklist' -> PASS
```

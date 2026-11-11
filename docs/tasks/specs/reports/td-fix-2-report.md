# td-fix-2 report (fix round after critic t-2276, TD-5.1 / TD-14.5)

Worktree `D:/ws1/wt-td\fix-2`, branch `td/fix-2`. No push.

## Items

1. B-A1 DONE. `_row_problems` refuses a repeated carrier file in one row: `row N (id): carriers[k].file names <file> again; expected one carrier entry per file; put the second rule in its own row.` CASES row: `E-7 same file twice in one row`.
2. R-A2 DONE. `SUFFIXES = (".md", ".yaml", ".yml", ".json")`; any other suffix is a row problem naming the path and the allowed suffixes. The 138 shipped carriers were counted first by suffix: md 132, yaml 5, json 1 (all pass). CASES row: `E-7 carrier suffix is not text`.
3. R-A1 DONE (no doubt). The register has 107 rows / 142 carriers (was 104 / 138). Anchors (carrier, line, count under the matcher; every count is 1, proven by `--check` 0 findings):
   - row `time-fork-case-cannot-tell` (new; the old row `time-fork-case-tolerance` keeps its two anchors, rule text narrowed to the tolerance clause):
     - `agents/qa-case-designer.md` line 37: `requirements and a "cannot tell" outcome`, count 1
     - `agents/qa-case-critic.md` line 68: ``or no `cannot tell` outcome``, count 1
   - row `time-fork-test-window` (re-pointed; rule text now the cannot-tell duty):
     - `references/test-code-patterns.md` line 134: ``outcome is `pytest.skip("cannot tell:``, count 1
     - `references/code-review-rubric.md` line 59: `case's tolerance and its cannot-tell skip`, count 1
   - row `time-fork-window-upper-bound` (new, window bounds): `references/test-code-patterns.md` line 134: `t_after + tolerance]`, count 1
   - row `red-value-never-received-names-field` (new, first clause of K13): `agents/qa-code-critic.md` line 84: `the field in the response shape`, count 1 (the existing `field-absent-accepted-red` row keeps the second clause; one row cannot hold both, the same file twice being refused)
4. R-A4 DONE. `plans/features.json`, feature F15 (the one holding `scripts/role_digest.py`): added `scripts/role_rules.py`, `design/role-rules.json`, `scripts/tests/test_role_rules.py` as plain list entries next to it.
5. B-B1 DONE. `test_codex_hooks_matchers.py`, end of `matchers_part`: every `guard_pre_tool.py` hook of `hooks/hooks.json` PreToolUse has no truthy `async` (one check), and the guard matchers fullmatch each of Write, Edit, Bash, Read, Grep, Glob (six checks, the red line names the tool and lists the wired matchers). The manifest has all of them today.

## Verification (verbatim tails)

```
python -B .../scripts/tests/test_role_rules.py        -> === role rules: 57/57 ok ===   (was 55)
python -B .../scripts/role_rules.py --check           -> role-rules: 107 rows, 142 carriers checked, 0 finding(s)
python -B .../scripts/tests/test_codex_hooks_matchers.py -> === test_codex_hooks_matchers: 283/283 ok ===   (was 276)
python -B .../scripts/selftest.py --limits --lang     -> PASS limits: every mandatory role rule of design/role-rules.json holds in its carrier
                                                         === qa-factory selftest: 4/4 ok ===
python -B .../scripts/tests/test_judgment_census.py   -> === judgment_census: 22/22 ok ===
python -B -c "import json;json.load(open(r'...\plans\features.json',encoding='utf-8'))" -> json=0
```

## Deviations / notes

- The hooks test gained 7 checks (1 synchronous + 6 tool wirings), not "one more": the DoD said one check more than 276; the per-tool lines give the red line the missing matcher's name, as the spec of item 5 asks.
- A stray `cd /dev/null` ran once in a verification Bash call (no effect, hook warned). Not repeated.
- `doubt:` none. `red before:` none (all four matchers present in the manifest; guard hooks all `async: false`).

## Fix the class (noticed, not widened)

- The clause class (an anchor guarding one clause of a multi-clause key) remains open for other TD-5.2/5.3 keys, as the critic said.
- R-A3, R-A5..R-A7, R-B1..R-B3 untouched (non-goals).

#!/usr/bin/env python3
"""`handoff_init.py --purpose`: the contract row of a dispatch that has its own purpose is reachable through the tool (OF5-7).

`handoffs/index.yaml` registers S5's plan pair under `purpose: s5_plan`; `handoff.contract_of` finds such a row only when asked
for the purpose, and the tool a role is told to use had no way to ask (FR-11). One table, one test: every row is one call of the
real script against a story folder; the id of the row is the name in the red line. The expected contract names are read from
`handoffs/index.yaml` (rows `purpose: s5_plan` and the usual S5 pair), not from the lookup function.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import check, cleanup, finish, run_script, temp_project  # noqa: E402

PLAN_AUTHOR = "s5-automator-plan-to-critic"     # index.yaml: S5 qa-automator -> qa-code-critic, purpose: s5_plan
PLAN_CRITIC = "s5-critic-plan-to-automator"     # index.yaml: S5 qa-code-critic -> qa-automator, purpose: s5_plan
USUAL_AUTHOR = "s5-automator-to-critic"         # index.yaml: S5 qa-automator -> qa-code-critic, no purpose
USUAL_RUNNER = "s5-automator-to-runner"         # index.yaml: S5 qa-automator -> qa-runner, secondary
AUTHOR, CRITIC = "qa-automator", "qa-code-critic"
NON_ASCII = "".join(chr(code) for code in (0x43F, 0x43B, 0x430, 0x43D))   # a Cyrillic word built from code points (FR-30)

# (id, stage, role, argv of the purpose and the rest, exit code, contract written | None, words the output must carry)
ROWS = [
    ("author + s5_plan -> the plan contract", "S5", AUTHOR, ["--purpose", "s5_plan"], 0, PLAN_AUTHOR, []),
    ("critic + s5_plan -> the plan review contract", "S5", CRITIC, ["--purpose", "s5_plan"], 0, PLAN_CRITIC, []),
    ("author + --to + s5_plan -> the plan contract", "S5", AUTHOR, ["--to", CRITIC, "--purpose", "s5_plan"], 0, PLAN_AUTHOR, []),
    ("no purpose -> the stage's usual contract", "S5", AUTHOR, [], 0, USUAL_AUTHOR, []),
    ("empty purpose given -> read as none", "S5", AUTHOR, ["--purpose", ""], 0, USUAL_AUTHOR, []),
    ("whitespace-only purpose -> read as none", "S5", AUTHOR, ["--purpose", "   "], 0, USUAL_AUTHOR, []),
    ("unknown purpose -> a refusal naming it and the known ones", "S5", AUTHOR, ["--purpose", "no_such"], 2, None,
     ["no contract for qa-automator at S5", "`no_such`", "Known purposes for qa-automator at S5: s5_plan"]),
    ("purpose on a stage that names none -> says so in words", "S4", "qa-case-designer", ["--purpose", "s5_plan"], 2, None,
     ["`s5_plan`", "carries a purpose"]),
    ("--contract + purpose -> --contract wins", "S5", AUTHOR, ["--contract", USUAL_RUNNER, "--purpose", "s5_plan"], 0, USUAL_RUNNER, []),
    ("--contract + an unknown purpose -> --contract wins, the purpose is not judged", "S5", AUTHOR,
     ["--contract", USUAL_RUNNER, "--purpose", "no_such"], 0, USUAL_RUNNER, []),
    ("--contract + a purpose with a space -> --contract wins", "S5", AUTHOR,
     ["--contract", USUAL_RUNNER, "--purpose", "s5 plan"], 0, USUAL_RUNNER, []),
    ("purpose with a space -> a call refusal", "S5", AUTHOR, ["--purpose", "s5 plan"], 2, None, ["not a purpose word", "no space inside"]),
    ("purpose of 64 characters (at the limit) -> the unknown-purpose refusal", "S5", AUTHOR, ["--purpose", "a" * 64], 2, None,
     ["no contract for qa-automator at S5", "Known purposes"]),
    ("purpose of 65 characters (beyond the limit) -> a call refusal", "S5", AUTHOR, ["--purpose", "a" * 65], 2, None, ["65 characters"]),
    ("purpose of 10000 characters -> a call refusal, no traceback", "S5", AUTHOR, ["--purpose", "a" * 10000], 2, None,
     ["10000 characters"]),
    ("non-ASCII purpose -> a call refusal, no traceback", "S5", AUTHOR, ["--purpose", NON_ASCII], 2, None, ["not a purpose word"]),
    ("purpose starting with a dash (=form) -> a call refusal", "S5", AUTHOR, ["--purpose=-x"], 2, None, ["not a purpose word"]),
    ("purpose starting with a dash (separate word) -> the parser's refusal, no traceback", "S5", AUTHOR, ["--purpose", "-x"], 2, None, []),
    ("upper-case purpose -> a call refusal (no silent fall back)", "S5", AUTHOR, ["--purpose", "S5_PLAN"], 2, None, ["not a purpose word"]),
]


def test_purpose_table() -> None:
    root = temp_project()
    try:
        art = root / "artifacts" / "QA-9"
        (art / "work").mkdir(parents=True)
        for number, (name, stage, role, argv, code, contract, words) in enumerate(ROWS):
            dispatch = f"{stage}-{role}-{number}"
            run = run_script("handoff_init.py", "--task", "QA-9", "--stage", stage, "--role", role,
                             "--dispatch", dispatch, "--task-root", str(art), *argv)
            form = art / "work" / "handoffs" / f"{dispatch}.yaml"
            seen = run.stdout + run.stderr
            ok = run.returncode == code and "Traceback" not in seen
            if contract:
                ok = ok and f"contract: {contract} (" in run.stdout and form.is_file() \
                    and f"contract: {contract}" in form.read_text(encoding="utf-8")
            else:
                ok = ok and not form.exists()
            ok = ok and all(word in seen for word in words)
            check(name, ok, f"exit {run.returncode}, form {form.is_file()}, output:\n{seen[:700]}")
    finally:
        cleanup(root)


# (id, stage, role, argv that make the form, words the door must carry, words it must not carry). The door is the line a
# not-UTF-8 refusal of handoff_check.py prints; the purposes and receivers expected are the ones of the handoffs/index.yaml rows.
DOOR_ROWS = [
    ("door: a plan form (purpose s5_plan, author) names --to then --purpose", "S5", AUTHOR, ["--purpose", "s5_plan"],
     [f"--role <role> --to {CRITIC} --purpose s5_plan --dispatch"], []),
    ("door: a plan review form (purpose s5_plan, critic) names --to then --purpose", "S5", CRITIC, ["--purpose", "s5_plan"],
     [f"--role <role> --to {AUTHOR} --purpose s5_plan --dispatch"], []),
    ("door: an ordinary S5 form prints no --purpose and no --to", "S5", AUTHOR, [],
     ["--role <role> --dispatch"], ["--purpose", "--to "]),
    ("door: a two-contract stage form (S4 secondary) still prints --to alone", "S4", "qa-case-designer", ["--to", "qa-runner"],
     ["--role <role> --to qa-runner --dispatch"], ["--purpose"]),
]


def test_door_table() -> None:
    root = temp_project()
    try:
        art = root / "artifacts" / "QA-9"
        (art / "work").mkdir(parents=True)
        for number, (name, stage, role, argv, words, absent) in enumerate(DOOR_ROWS):
            dispatch = f"{stage}-{role}-door-{number}"
            made = run_script("handoff_init.py", "--task", "QA-9", "--stage", stage, "--role", role,
                              "--dispatch", dispatch, "--task-root", str(art), *argv)
            form = art / "work" / "handoffs" / f"{dispatch}.yaml"
            if made.returncode != 0 or not form.is_file():
                check(name, False, f"the form was not made: exit {made.returncode}\n{(made.stdout + made.stderr)[:500]}")
                continue
            form.write_bytes(form.read_bytes() + b"\n# \xff\xfe\n")
            run = run_script("handoff_check.py", "--file", str(form), "--task-root", str(art), "--no-judge")
            seen = run.stdout + run.stderr
            ok = run.returncode == 2 and "Traceback" not in seen and "not UTF-8" in seen \
                and all(word in seen for word in words) and not any(word in seen.split("Start it again:")[-1] for word in absent)
            check(name, ok, f"exit {run.returncode}, output:\n{seen[:700]}")
    finally:
        cleanup(root)


test_purpose_table()
test_door_table()
finish("handoff_init purpose")

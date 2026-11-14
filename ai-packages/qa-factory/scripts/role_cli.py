"""role_cli.py — a refusal a role can act on (P3).

A role calls these commands by hand, reads the refusal, and writes the file again. It cannot
open a debugger, and it does not have the script's source in context: `KeyError: 'case'` tells
it nothing, so it guesses, and on TP1-13797 one such traceback cost 96 turns and fourteen
rewritten input files. A refusal owes its reader three things and this module is the one place
that puts them together:

  (a) what is wrong        - the caller's own sentence, about THIS input
  (b) what to write        - `input` of references/role-commands.json
  (c) how to prove it      - `verify` of the same entry

    from role_cli import refuse
    return refuse("manual_evidence.py prepare", "`case` is missing")

The registry is the single source of (b) and (c): the same text answers the role at the moment
of the refusal, `--help` before the first call, and `test_role_commands.py`, which feeds every
registered command a deliberately broken file and fails the one that raises instead of
refusing. A command missing from the registry refuses with (a) alone rather than pretending -
the exit code and the sentence are still right, and the test names the gap.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = PLUGIN_ROOT / "references" / "role-commands.json"

EXIT_REFUSED = 2

# Who a refusal belongs to, marked in the refusal's own text. The driver's table of known
# refusals was written from experience - one regex per message it had already met - so a NEW
# refusal in any script went to the person or to the conductor by default, whoever the answer
# actually belonged to. A refusal that knows the answer is the role's own work says so in these
# words, and `story_run.match_known` routes on them before it consults the table (P6). One
# sentence, one owner: a script prints the constant, never a paraphrase.
REPAIR_MARKER = "This is a repair, not a question for the person"
PERSON_MARKER = "This is a question for the person"


def registry() -> dict:
    try:
        data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):                        # pragma: no cover - broken install
        return {}
    return data.get("commands") or {}


def entry(command: str) -> dict:
    return registry().get(command) or {}


def shape(command: str) -> str:
    """The two lines a role needs BEFORE the first call — for an argparse epilog."""
    row = entry(command)
    if not row:
        return ""
    return f"--input: {row.get('input', '')}\nverify: {row.get('verify', '')}"


def epilog(script: str) -> str:
    """Every registered command of one script, for `--help`: the role reads the shape BEFORE
    writing the file, not after the refusal."""
    rows = registry()
    parts = [f"{name}\n  what to write: {rows[name].get('input', '')}\n"
             f"  how to prove it: {rows[name].get('verify', '')}"
             for name in sorted(rows) if name.split()[0] == script]
    return ("what a role-written --input must carry:\n\n" + "\n\n".join(parts)) if parts else ""


def _is_record(problem) -> bool:
    """A `detector_verdict.Record` by its fields (this module cannot import that one: it imports this one)."""
    return isinstance(problem, str) and all(isinstance(getattr(problem, name, None), str) for name in ("check", "expected", "door"))


def _extra_record_lines(records, first: str, own: str) -> list:
    """The further refused checks of an error, one indented told line each (THE line renderer
    `stage_joints.told_line`). `records` is read only when it is a list or tuple; an item that is not a Record is skipped; a check
    equal to `first` (printed by the caller), to `own`, or already kept is dropped; first-seen order. More than
    `branch_accounting.limit("refusal_units_shown")` lines keep that many and a tail line naming the rest (never a silent drop);
    when the limit cannot be read there is no cap. Never raises: on any exception it returns what it had built."""
    lines: list = []
    try:
        if not isinstance(records, (list, tuple)):
            return []
        import stage_joints                      # inside: `stage_joints` imports this module lazily, a top-level import is a cycle
        seen = {first, own}
        for item in records:
            if not _is_record(item) or item.check in seen:
                continue
            seen.add(item.check)
            lines.append("  " + stage_joints.told_line(stage_joints.row_for(item.check)[0] or {"check": item.check}))
        try:
            import branch_accounting
            cap = branch_accounting.limit("refusal_units_shown")
        except Exception:  # noqa: BLE001 - an unreadable limit means no cap
            cap = None
        if cap is not None and len(lines) > cap:
            rest = len(lines) - cap
            lines = lines[:cap] + [f"  {rest} more refused checks are not shown: fix these and run the command again; it names the rest"]
    except Exception:  # noqa: BLE001
        pass
    return lines


def refuse(command: str, problem, stream=None, *, check=None, records=()) -> int:
    """Print the refusal as an instruction and return the exit code. Never raises.

    `problem` is a plain `str` or a `detector_verdict.refusal(...)` Record. The lines keep their order: `<command>: <problem>`,
    the Record's `expected` / `door` lines (skipped when empty, and when the Record's check is this command's own
    `role_cli:<command>` row: the card lines below already say it), what to write, how to prove it, one line for every further
    distinct check in `records` (an error that refused several), `if you cannot`, and LAST
    `  check: <the Record's check, else `check`, else role_cli:<command>>`. No `records`: today's output, byte for byte."""
    out = stream or sys.stderr
    row = entry(command)
    own = f"role_cli:{command}"
    record = _is_record(problem)
    print(f"{command}: {str(problem)}", file=out)
    if record and problem.check != own:
        if problem.expected:
            print(f"  expected: {problem.expected}", file=out)
        if problem.door:
            print(f"  door: {problem.door}", file=out)
    if row.get("input"):
        print(f"  what to write: {row['input']}", file=out)
    if row.get("verify"):
        print(f"  how to prove it: {row['verify']}", file=out)
    for line in _extra_record_lines(records, problem.check if record else "", own):
        print(line, file=out)
    print("  if you cannot: do not repeat this call — record what you were trying to do and why it "
          "could not be done in your findings and your handover, and halt. A refusal with no way "
          "out is a factory defect, not your mistake.", file=out)
    print(f"  check: {(problem.check if record else '') or check or own}", file=out)
    return EXIT_REFUSED


class RefusingParser(argparse.ArgumentParser):
    """An `ArgumentParser` whose usage errors end as `refuse`: the argparse line (`--kind is required`) is the problem, and
    the registry's card for the command follows it (what to write, how to prove it) - one survivor for the class (AR-15,
    RC1-10 item 2; SC1-7). Plain argparse printed the usage and the sentence and nothing a role could act on.

        parser = RefusingParser(command=command_from_argv("artifact_producer.py"), description=...)

    `command` is the registry key; without it the program name is used (a script absent from the registry still refuses
    with the sentence alone, as `refuse` does). Exit code `EXIT_REFUSED`, as argparse's own 2."""

    def __init__(self, *args, command=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.refusing_command = command

    def error(self, message):
        print(self.format_usage(), end="", file=sys.stderr)
        command = self.refusing_command or self.prog
        if not entry(command):
            # `refuse` stays silent about a missing card (its callers are many); a usage error says so, because the
            # usage above is then all the role has and `--help` of the script is the next door.
            print(f"{command}: no command card is registered for this call, so the usage above is all the "
                  "factory can quote; `--help` of the script lists every registered shape.", file=sys.stderr)
        refuse(command, message, check=f"role_cli:{command}")
        raise SystemExit(EXIT_REFUSED)


DEFECT = (TypeError, AttributeError, KeyError, IndexError)


def command_from_argv(script: str) -> str:
    """`manual_evidence.py write-block` or `case_versions.py --pin` when that is the registered
    key, else the script itself.

    The registry keys a subcommand separately because its `--input` shape is its own, and some
    commands are told apart by a flag rather than a word (`manifest_put.py --fragment`); a refusal
    should carry the shape of the command the role actually ran. Every argv token is tried, not
    only the first, because the deciding one can sit behind `--task <T>`."""
    rows = registry()
    for argument in sys.argv[1:]:
        candidate = f"{script} {argument}"
        if candidate in rows:
            return candidate
    return script


def run_guarded(command: str, entrypoint, stream=None) -> int:
    """Run a script's `main` and turn whatever it raises into a refusal a role can act on.

    Measured on TP1-13797: 50+ dispatch turns ended in a Python traceback from our own
    scripts. The message at the bottom of one was usually right — `fingerprint specification
    missing source_revision`, `existing artifact requires its exact previous sha256` — but a
    traceback does not say what value is allowed or which command repairs it, so the role guessed,
    and every guess cost a turn on a context of a quarter-million tokens.

    A `ValueError` is a rule this run broke: it becomes the refusal, with the command's own shape
    from the registry. A `TypeError`/`AttributeError`/`KeyError`/`IndexError` is OUR defect: the
    refusal says so in the role's terms and asks for it in the findings, because the role cannot
    fix our code and must not spend turns trying. `KeyboardInterrupt` and `SystemExit` pass
    through untouched — they are not the role's business."""
    # The refusal text above carries a dash and is printed from THIS module, inside the process
    # of a role CLI that may have no setup of its own (B-413, critic t-523 F1): the guard stands
    # here so every run_guarded entry prints it as UTF-8, whatever the console code page is.
    try:
        import console_io
        console_io.utf8_stdio()
    except ImportError:
        pass
    try:
        return entrypoint()
    except SystemExit:
        raise
    except FileNotFoundError as exc:
        return refuse(command, f"{exc.filename or exc}: no such file. A path is read as given, "
                               "relative to the directory you run from", stream)
    except ValueError as exc:
        # a `refusal(...)` Record raised as `ValueError(record)` reaches `refuse` whole (its row's sentence and door print);
        # any other ValueError is today's text
        first = exc.args[0] if exc.args else None
        return refuse(command, first if _is_record(first) else (str(exc) or exc.__class__.__name__), stream,
                      records=getattr(exc, "records", ()))
    except DEFECT as exc:
        return refuse(command, f"this is a defect in {command}, not something you wrote wrong: "
                               f"{exc.__class__.__name__}: {exc}. Do not try other argument shapes "
                               "— record it in your findings as a factory defect and go on with "
                               "what does work", stream)
    except OSError as exc:
        return refuse(command, f"the operating system refused this: {exc}. If an argument is a "
                               "path, it is read as a path — a JSON value goes in a file", stream)


def main() -> int:
    """`role_cli.py [command]` — the registry as a table, or one command's shape."""
    try:
        import console_io
        console_io.utf8_stdio()
    except ImportError:
        pass
    rows = registry()
    if len(sys.argv) > 1:
        name = sys.argv[1]
        if name not in rows:
            print(f"role_cli: {name} is not a registered role command. Known: "
                  + ", ".join(sorted(rows)), file=sys.stderr)
            return 1
        print(f"{name}\n{shape(name)}")
        return 0
    for name in sorted(rows):
        print(f"{name}\n{shape(name)}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())

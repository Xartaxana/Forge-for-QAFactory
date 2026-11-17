"""The driver as the dry world runs it (P1-b spec 4.4, F10 (a), node N2): `story_run.py` behind a passing spy on `no_move.priced_options`.

    python -B dry_driver.py <the arguments of story_run.py>

The driver does not write the price key of a question into the question's record (`driver_dialog.ask` holds no such field), so the walker
cannot learn WHICH closed question was raised, with WHICH answers, from the driver's files. This wrapper records it: every call of the
one resolution of a closed question's prices (`no_move.priced_options`, the call each question site makes) appends `{"key", "answers", "q", "prompt"}` to
`state/dry-priced.jsonl` of the task, in the world of the dry story, and then returns what the real function returned. The spy never changes
an argument or a result, and it records only after the real call succeeded - a question whose prices cannot be read is not offered, so it is
not recorded either. It is the process of the driver, not a test's lambda over a seam: the loop, `no_move`, `take_answer` and the rest of
the driver run as shipped; no attribute of the driver's own class is replaced here (the class is never imported).

A record that cannot be written is said on stderr and the question goes on; the walker's E17 (a row with a key and no record: "key not
observed") is the check that turns the gap red.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))


def sink_path(argv: list):
    """`<project>/qa-factory/artifacts/<task>/state/dry-priced.jsonl` of the call's own `--project` and `--task`, or None when either is not there."""
    def opt(name):
        return argv[argv.index(name) + 1] if name in argv and argv.index(name) + 1 < len(argv) else ""
    project, task = opt("--project"), opt("--task")
    if not project or not task:
        return None
    return Path(project) / "qa-factory" / "artifacts" / task / "state" / "dry-priced.jsonl"


def _append(sink: Path, record: str, what: str) -> None:
    """One line to the spy's sink; a sink that cannot be written is a stderr line naming what was not recorded, never a stop of the driver."""
    try:
        sink.parent.mkdir(parents=True, exist_ok=True)
        with sink.open("a", encoding="utf-8") as handle:
            handle.write(record + "\n")
    except OSError as exc:
        print(f"dry_driver: cannot record {what} in {sink} ({type(exc).__name__}); expected a writable state folder", file=sys.stderr)


def _raising_for_conductor() -> bool:
    """True when a frame named `_conductor_text` is on the call stack of the spy's caller: the driver is composing a conductor PROMPT, not raising a
    question for the person (walk `f_back` by name; `inspect.stack()` would read source on every call). The only conductor-prompt pricing road today is
    `_conductor_text` -> `gate_prices` -> `priced_section` -> `priced_options` (a selftest row of `dry_stub.py` guards the name)."""
    frame = sys._getframe(2)
    while frame is not None:
        if frame.f_code.co_name == "_conductor_text":
            return True
        frame = frame.f_back
    return False


def _question_count(sink: Path):
    """How many question rows the driver had written when the spy was called: `driver_journal.question_rows` (the one reader) of the task root, which is
    `sink.parent.parent` (`<task root>/state/dry-priced.jsonl`). None when the rows cannot be read: a record with no integer `q` is never attributed to an ask."""
    try:
        import driver_journal
        return len(driver_journal.question_rows(sink.parent.parent)[0])
    except (OSError, ValueError):
        return None


def passing_spy(real, sink: Path):
    """A function with the signature of `real` that returns exactly what `real` returns and, after a successful call, appends one line to `sink`:
    `{"key", "answers", "q", "prompt"}` - the key, the answers (the `answer` id of each option the site offered, in order), `q` = the number of rows of
    `state/driver-questions.jsonl` at the call (the driver writes the row of a question AFTER pricing it, so a record priced while raising question number
    `n`, 0-based, carries `q == n`), and `prompt` = true when the call happens while the driver composes a conductor prompt (`_raising_for_conductor`). The
    walker reads these two fields in `dry_world.ask_window`: a record counts for an ask only when `q` is the ask's ordinal and `prompt` is not true."""
    def spy(key, options, *args, **kwargs):
        result = real(key, options, *args, **kwargs)
        line = json.dumps({"key": key, "answers": [str(option.get("answer")) for option in options], "q": _question_count(sink), "prompt": _raising_for_conductor()})
        _append(sink, line, f"the price key {key!r}")
        return result
    return spy


def route_spy(real, sink: Path):
    """A function with the signature of `real` (`driver_machine.match_known`) that returns exactly what `real` returns and, after a call that matched a
    route (a non-None result), appends `{"route": <name>}` to `sink` (`state/dry-routes.jsonl`): the walker's record of WHICH route the driver took
    (N4w, F-W4 (a)). Nothing is recorded for a text no row matches, and nothing of the driver's own class is replaced (AR-17: a module function)."""
    def spy(*args, **kwargs):
        result = real(*args, **kwargs)
        if result is not None:
            _append(sink, json.dumps({"route": result[0] if isinstance(result, tuple) else str(result)}), "the route")
        return result
    return spy


def main(argv: list) -> int:
    sink = sink_path(argv)
    if sink is None:
        print("dry_driver: no --project and --task in the arguments; expected the arguments of story_run.py", file=sys.stderr)
        return 2
    import no_move
    no_move.priced_options = passing_spy(no_move.priced_options, sink)
    import driver_machine
    driver_machine.match_known = route_spy(driver_machine.match_known, sink.with_name("dry-routes.jsonl"))
    import story_run
    sys.argv = [story_run.__file__, *argv]
    return story_run.main()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

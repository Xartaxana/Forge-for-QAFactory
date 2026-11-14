"""The driver as the dry world runs it (P1-b spec 4.4, F10 (a), node N2): `story_run.py` behind a passing spy on `no_move.priced_options`.

    python -B dry_driver.py <the arguments of story_run.py>

The driver does not write the price key of a question into the question's record (`driver_dialog.ask` holds no such field), so the walker
cannot learn WHICH closed question was raised, with WHICH answers, from the driver's files. This wrapper records it: every call of the
one resolution of a closed question's prices (`no_move.priced_options`, the call each question site makes) appends `{"key", "answers"}` to
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


def passing_spy(real, sink: Path):
    """A function with the signature of `real` that returns exactly what `real` returns and, after a successful call, appends the key and the
    answers (the `answer` id of each option the site offered, in order) as one line to `sink`."""
    def spy(key, options, *args, **kwargs):
        result = real(key, options, *args, **kwargs)
        line = json.dumps({"key": key, "answers": [str(option.get("answer")) for option in options]})
        try:
            sink.parent.mkdir(parents=True, exist_ok=True)
            with sink.open("a", encoding="utf-8") as handle:
                handle.write(line + "\n")
        except OSError as exc:
            print(f"dry_driver: cannot record the price key {key!r} in {sink} ({type(exc).__name__}); expected a writable state folder", file=sys.stderr)
        return result
    return spy


def main(argv: list) -> int:
    sink = sink_path(argv)
    if sink is None:
        print("dry_driver: no --project and --task in the arguments; expected the arguments of story_run.py", file=sys.stderr)
        return 2
    import no_move
    no_move.priced_options = passing_spy(no_move.priced_options, sink)
    import story_run
    sys.argv = [story_run.__file__, *argv]
    return story_run.main()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

"""readers: a part of test_story_sides.py, split by tools/test_split.py (TD-11c). The shared helpers are in story_sides_common."""
import contextlib
import io
import json
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import check, check_eq  # noqa: E402
sys.path.insert(0, str(harness.SCRIPTS))
import contract  # noqa: E402
import stage_done  # noqa: E402
from story_sides_common import ABSENT, DATA, REAL, SUBSTITUTED, side, stderr_of  # noqa: E402


def refusal(spec):
    try:
        stage_done.parse_sets([spec])
        return ""
    except ValueError as exc:
        return str(exc)


def reader_cases():
    expected = {name: {**row, "reference": None, "source": "default"} for name, row in DATA["default"].items()}
    for label, record in (("no pipeline.sides", {}), ("an empty sides record", {"sides": {}}),
                          ("an unreadable pipeline (None)", None), ("sides that is not a dict", {"sides": "x"})):
        check_eq(f"default: {label}", stderr_of(lambda: contract.story_sides(record, {}))[0], expected)
    sides = contract.story_sides({"sides": {"kiosk": side(SUBSTITUTED, False, settles_by="platform team", source="launch"),
                                            "api": side(ABSENT, settles_by=None)}}, {})
    check_eq("pipeline.sides is read, settles_by kept", sides["kiosk"]["settles_by"], "platform team")
    check_eq("settles_by empty reads ''", sides["api"]["settles_by"], "")
    check_eq("an entry with no deliverable reads true; no reality reads unknown, never real",
             (contract.story_sides({"sides": {"x": {}}})["x"]["deliverable"], contract.story_sides({"sides": {"x": {}}})["x"]["reality"]),
             (True, ""))
    check("a recorded side wins over the default (product is not implied)", "product" not in sides)


def parks_cases():
    def parks(*entries):
        return contract.parks_after_s5({"sides": {f"s{i}": e for i, e in enumerate(entries)}})
    check_eq("absent + deliverable parks", parks(side(ABSENT, True)), True)
    check_eq("substituted + deliverable does not", parks(side(SUBSTITUTED, True)), False)
    check_eq("absent + not deliverable does not", parks(side(ABSENT, False)), False)
    check_eq("real does not", parks(side(REAL, True)), False)
    check_eq("an unrecorded story does not park", contract.parks_after_s5({}), False)


def awaiting_cases():
    check_eq("no record -> none", contract.awaiting({})["state"], "none")
    check_eq("an unreadable pipeline -> none", contract.awaiting(None)["state"], "none")
    old = contract.awaiting({"awaiting": {"since": "2026-11-01T10:00:00", "sides": ["api"], "packet": "interim-report.md"}})
    check_eq("a record without cause/held_from (old shape) reads s5_absent_side / S6",
             (old["state"], old["cause"], old["held_from"], old["packet"]), ("awaiting", "s5_absent_side", "S6", "interim-report.md"))
    new = contract.awaiting({"awaiting": {"since": "t", "cause": "first_look_stop", "held_from": "S3"}})
    check_eq("a record with first_look_stop / S3 is returned as given", (new["state"], new["cause"], new["held_from"]),
             ("awaiting", "first_look_stop", "S3"))
    stopped = contract.awaiting({"awaiting": {"since": "t", "stopped": {"at": "t2", "words": "stop"}}})
    check_eq("a stopped mark -> stopped", (stopped["state"], stopped["stopped"]["words"]), ("stopped", "stop"))


def stage_done_cases():
    check_eq("a data word is accepted and is the word", stage_done.parse_sets([f"sides.api.reality={ABSENT}"]),
             {"sides.api.reality": ABSENT})
    message = refusal("sides.api.reality=mocked")
    check("an unknown reality is refused, naming every allowed word and the data file",
          all(w in message for w in DATA["realities"]) and "side-realities.json" in message, message)
    check_eq("a side `kiosk` outside any list passes (open variety)",
             stage_done.parse_sets([f"sides.kiosk.reality={SUBSTITUTED}"]), {"sides.kiosk.reality": SUBSTITUTED})
    check_eq("deliverable is a bool, settles_by empty is ''",
             stage_done.parse_sets(["sides.kiosk.deliverable=false", "sides.kiosk.settles_by="]),
             {"sides.kiosk.deliverable": False, "sides.kiosk.settles_by": ""})
    check("deliverable `maybe` is refused", "true or false" in refusal("sides.kiosk.deliverable=maybe"))
    check("an unknown attribute is refused naming the attributes", "reality" in refusal("sides.kiosk.colour=red"))
    check_eq("sides_unknown= clears", stage_done.parse_sets(["sides_unknown="]), {"sides_unknown": None})
    pipeline = {"sides_unknown": {"at": "t", "why": "x"}}
    stage_done.apply_facts(pipeline, stage_done.parse_sets([f"sides.kiosk.reality={ABSENT}", "sides.kiosk.deliverable=true"]), [])
    check_eq("a set lands as a nested record the reader reads", contract.story_sides(pipeline)["kiosk"]["reality"], ABSENT)


class pointed_at:
    """`contract.SIDE_REALITIES_PATH` pointed elsewhere for a block (a temp copy or a missing path - never the live file)."""
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self.old, contract.SIDE_REALITIES_PATH = contract.SIDE_REALITIES_PATH, self.path

    def __exit__(self, *exc):
        contract.SIDE_REALITIES_PATH = self.old


def word_cases():
    check("the test words are in the data file", all(w in DATA["realities"] for w in (REAL, ABSENT, SUBSTITUTED)))


def note_cases():
    value, err = stderr_of(lambda: contract.story_sides(None))
    check("an unreadable pipeline reads the default and says why on stderr (one line)",
          "pipeline.json could not be read" in err and err.count("\n") == 1 and "product" in err, err)
    check("the default is still returned", "product" in value)
    value, err = stderr_of(lambda: contract.story_sides({}))
    check_eq("an empty readable record is the default and prints nothing", ("product" in value, err), (True, ""))
    value, err = stderr_of(lambda: contract.story_sides("not a dict"))
    check("a pipeline that is not a dict is unreadable too", "pipeline.json could not be read" in err)
    with tempfile.TemporaryDirectory(prefix="qa-sides-") as td, pointed_at(Path(td) / "missing.json"):
        value, err = stderr_of(lambda: contract.story_sides({}))
        check_eq("an unreadable data file: {} and a note naming it", (value, "side-realities.json" in err), ({}, True))
        value, err = stderr_of(lambda: contract.story_sides({"sides": {"api": side(ABSENT)}}))
        check_eq("a recorded side needs no data file and prints nothing", ("api" in value, err), (True, ""))
        message = refusal(f"sides.api.reality={ABSENT}")
        check("coerce_value refuses when the data file cannot be read (AR-28)",
              "cannot be read" in message and "side-realities.json" in message, message)


def edge_cases():
    sides = contract.story_sides({"sides": {"api": "absent"}})
    check_eq("a non-dict entry reads unknown reality", sides["api"]["reality"], "")
    check_eq("and does not park", contract.parks_after_s5({"sides": {"api": "absent"}}), False)
    check_eq("a non-dict awaiting record -> none", contract.awaiting({"awaiting": "yes"})["state"], "none")
    check_eq("sides_unknown.at / .why land nested",
             _applied(["sides_unknown.at=t1", "sides_unknown.why=no access"], {"sides_unknown": None})["sides_unknown"],
             {"at": "t1", "why": "no access"})
    check("sides_unknown=x is refused naming the clear form", "--set sides_unknown=" in refusal("sides_unknown=x"))


def _applied(specs, pipeline):
    stage_done.apply_facts(pipeline, stage_done.parse_sets(specs), [])
    return pipeline


def bom_cases():
    with tempfile.TemporaryDirectory(prefix="qa-sides-") as td:
        copy = Path(td) / "side-realities.json"
        copy.write_bytes(b"\xef\xbb\xbf" + (harness.PLUGIN_ROOT / "references" / "side-realities.json").read_bytes())
        with pointed_at(copy):
            value, err = stderr_of(lambda: contract.story_sides({}))
            check_eq("a BOM copy: the reader gives the default", ("product" in value, err), (True, ""))
            check_eq("a BOM copy: the --set door accepts a data word",
                     stage_done.parse_sets([f"sides.x.reality={ABSENT}"]), {"sides.x.reality": ABSENT})
            check_eq("both read the same words", contract.side_realities().get("realities"), DATA["realities"])


def transition_cases():
    import hooklib
    with tempfile.TemporaryDirectory(prefix="qa-sides-") as td:
        proj = Path(td)
        art = proj / "qa-factory" / "artifacts" / "QA-1"
        art.mkdir(parents=True)
        (proj / "qa-factory" / "config.json").write_text("{}", encoding="utf-8")
        old = hooklib._PROJECT_ROOT_CACHE
        hooklib._PROJECT_ROOT_CACHE = proj
        try:
            (art / "pipeline.json").write_text(json.dumps({"ticket": "QA-1", "stages": {}, "gates": {}}), encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                stage_done.set_facts("QA-1", stage_done.parse_sets(
                    [f"sides.kiosk.reality={ABSENT}", "sides_unknown.at=t1", "sides_unknown.why=w"]), [])
                code = stage_done.run("QA-1", "S1", "done", "qa-scout", "one fact", True)
            written = json.loads((art / "pipeline.json").read_text(encoding="utf-8"))
            check_eq("a stage transition ran", (code, written["stages"]["S1"]["status"]), (0, "done"))
            check_eq("and kept sides on disk", written.get("sides", {}).get("kiosk", {}).get("reality"), ABSENT)
            check_eq("and sides_unknown", written.get("sides_unknown"), {"at": "t1", "why": "w"})
        finally:
            hooklib._PROJECT_ROOT_CACHE = old


def main() -> None:
    word_cases()
    reader_cases()
    parks_cases()
    awaiting_cases()
    stage_done_cases()
    note_cases()
    edge_cases()
    bom_cases()
    transition_cases()
    harness.finish("test_story_sides_readers")


# split: runner piece 1
if __name__ == "__main__":
    main()

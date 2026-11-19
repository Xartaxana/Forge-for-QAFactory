"""FV3-29: `SkillRoad.record_close` makes a failed `tail` row visible (one `note:` line), never raises, keeps running the later rows."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import stage_close  # noqa: E402

GOOD = ("ev_a", "--x", "1")
BAD = ("ev_b", "--x", "2")
LAST = ("ev_c",)


@pytest.mark.parametrize("name, tail, results, notes, tail_calls", [
    ("empty tail: silent", (), {}, [], 0),
    ("one failing row: one note, later row runs", (GOOD, BAD, LAST), {"ev_b": (1, "x\nboom")},
     ["note: journal row ev_b was not filed: boom"], 3),
    ("missing script: exit 127 note", (GOOD,), {"ev_a": (127, "")},
     ["note: journal row ev_a was not filed: log_append.py exit 127"], 1),
    ("stage_done refused: Refused, tail never runs", (GOOD,), {"stage_done.py": (2, "no")}, None, 0),
])
def test_tail(capsys, name, tail, results, notes, tail_calls):
    road = stage_close.SkillRoad.__new__(stage_close.SkillRoad)
    road.task = "QA-1"
    calls = []

    def py(script, *args, check=False, expect=""):
        calls.append((script, args))
        code, out = results.get(script if script == "stage_done.py" else args[0], (0, ""))
        if check and code:
            raise stage_close.Refused(f"{script} exit {code}: {out}")
        return code, out
    road.py = py
    if notes is None:
        with pytest.raises(stage_close.Refused):
            road.record_close("s", "S6", tail=tail)
    else:
        road.record_close("s", "S6", tail=tail)
        assert capsys.readouterr().out.splitlines() == notes
    assert sum(1 for s, _ in calls if s == "log_append.py") == tail_calls

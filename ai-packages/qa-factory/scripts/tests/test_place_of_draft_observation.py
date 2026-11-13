"""test_place_of_draft_observation.py - the optional `observation` field of a bug draft joins the place it names (node TR4-15).

Run: python -B -m pytest scripts/tests/test_place_of_draft_observation.py -q
"""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import test_place_answers as T  # noqa: E402  (fixture_story and draft: the one fixture the place tests share)
import investigation as INV  # noqa: E402
import place_answers as PA  # noqa: E402

OBS = "obs-S6-qa-runner-4-0"
OWN = "draft-d1"

# (case id, draft fields, expected place)
ROWS = [
    ("observation joins its place", {"observation": OBS}, OBS),
    ("foreign well-formed observation stays on own place", {"observation": "obs-S6-other-9-9"}, OWN),
    ("case holding an obs id is not joined", {"case": OBS}, OWN),
    ("observation empty string is absent", {"observation": ""}, OWN),
    ("observation whitespace only is absent", {"observation": "   "}, OWN),
    ("observation number is absent", {"observation": 5}, OWN),
    ("observation list is absent", {"observation": [OBS]}, OWN),
    ("observation None is absent", {"observation": None}, OWN),
    ("observation of another form falls through", {"observation": "TC-004"}, OWN),
    ("observation obs- with junk falls through", {"observation": "obs-"}, OWN),
    ("case match wins over a different observation", {"case": "TC-007", "observation": OBS}, "case-TC-007"),
    ("observation naming a target with a pinned case still joins it", {"observation": "case-TC-006"}, "case-TC-006"),
]


@pytest.mark.parametrize("fields,expected", [r[1:] for r in ROWS], ids=[r[0] for r in ROWS])
def test_place_of_draft_observation(fields, expected):
    task = T.fixture_story()
    name = T.draft(task, "d1.json", **{"case": "TC-1", **fields})
    body = json.loads((task / "work" / "bug-drafts" / name).read_text(encoding="utf-8"))
    targets = INV.investigation_targets(task)["targets"]
    assert PA.place_of_draft(task, name, body, [], targets) == expected


def test_places_shows_draft_source_at_the_observation():
    task = T.fixture_story()
    T.draft(task, "d1.json", observation=OBS)
    found = PA.places(task)
    place = next(p for p in found["places"] if p["id"] == OBS)
    assert "draft" in place["sources"] and "draft-d1" not in T.ids(found)


def test_no_targets_no_exception(tmp_path):
    body = {"observation": OBS, "violates": "R-1"}
    assert PA.place_of_draft(tmp_path, "d1.json", body, [], []) == OWN
    assert PA.place_of_draft(tmp_path, "d1.json", body, [], None) == OWN

#!/usr/bin/env python3
"""SS1-11 F5 (t-405): what a person taught about the stand reaches the app card and rebuilds it.

Moved out of test_app_card.py (quarantined, so a test there never runs in the canon); the helpers `make`, `card_of` and
`body` are imported from it (importing it has no side effects: sys.path and `import app_card` only).

Run: python -B scripts/tests/test_app_card_stand_lessons.py    or    python -m pytest scripts/tests/test_app_card_stand_lessons.py -q
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))
import app_card as AC  # noqa: E402
from test_app_card import body, card_of, make  # noqa: E402


def test_stand_lessons_reach_the_card_and_rebuild_it(tmp_path):
    """F5 (t-405): what a person taught about the stand is a line of the card's Stand section (the walk road); a lesson recorded
    after the card was built changes the hash and the card is rebuilt; no registry file: no line, the hash is stable."""
    import project_knowledge as PK
    task = make(tmp_path)
    project = task.parents[2]
    AC.build(task)
    assert "Stand lessons" not in card_of(task)                                       # no registry file: no line
    assert AC.build(task).startswith("app-card: unchanged")                          # ... and the hash is stable
    row, problem, _ = PK.record(project, key=PK.LESSONS_KEY, environment="local", element="indexing", state=PK.KNOWN, scope="stand",
                                value={"wait_s": 300}, words="Indexing takes minutes", source="person", story="S-1", by="conductor")
    assert problem == ""
    assert AC.build(task).startswith("app-card: written")                            # the lesson changed the inputs: rebuilt
    stand = body(card_of(task), "Stand")
    assert '- Stand lessons: indexing: "Indexing takes minutes" (at least 300 s)' in stand
    assert AC.build(task).startswith("app-card: unchanged")
    row, problem, _ = PK.record(project, key=PK.LESSONS_KEY, environment="local", element="login", state=PK.KNOWN, scope="stand",
                                value={"wait_s": None}, words="Login is slow", source="person", story="S-1", by="conductor")
    assert problem == "" and AC.build(task).startswith("app-card: written")          # a second record changes the hash
    assert "- Stand lessons: login:" in body(card_of(task), "Stand")


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-q", "-p", "no:cacheprovider"]))

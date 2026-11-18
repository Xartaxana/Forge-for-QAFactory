"""t-2181 PC-1a: the story's sides (one reader over the story record), the `stage_done --set sides.*` door, the hold readers.

The reality words are read ONLY from `references/side-realities.json` (AR-1); side names are open (AR-2: `kiosk`).
"""
# Shared helpers of test_story_sides.py, split by tools/test_split.py (TD-11c).
import contextlib
import io
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
sys.path.insert(0, str(harness.SCRIPTS))
import contract  # noqa: E402


DATA = json.loads((harness.PLUGIN_ROOT / "references" / "side-realities.json").read_text(encoding="utf-8"))


# Test words are picked BY NAME, never by list position; `word_cases` pins that each is in the data file.
REAL, ABSENT, SUBSTITUTED = "real", contract.PARKING_REALITY, "substituted"


def side(reality, deliverable=True, **extra):
    return {"reality": reality, "deliverable": deliverable, **extra}


def stderr_of(call):
    buf = io.StringIO()
    with contextlib.redirect_stderr(buf):
        value = call()
    return value, buf.getvalue()


def copy_registry(root, root2):
    """A second story of the same project: the project's registry file is copied to `root2` (the registry is the project's, not the story's)."""
    import shutil
    import project_knowledge as PK
    PK.record_path(root2).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(PK.record_path(root), PK.record_path(root2))

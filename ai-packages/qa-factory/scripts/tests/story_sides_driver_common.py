"""driver: a part of test_story_sides.py, split by tools/test_split.py (TD-11c). The shared helpers are in story_sides_common."""
# Shared helpers of test_story_sides_driver.py, split by tools/test_split.py (TD-11c).
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
sys.path.insert(0, str(harness.SCRIPTS))
import project_knowledge as PK


repos = {"code_repos": [{"name": "app", "path": "app"}]}


# PC2-7 (t-043): ONE table - the implicit `product` is carried exactly when no side of the story is a real side of this team, whatever the
# registry holds from earlier stories and with or without `--no-trace`. Each S0 row runs traced AND `--no-trace` and the two records are
# equal without `at`; the id of the row names the case in every label. `second-story` has no `--no-trace` half (that flow asks again).
product_default = {"reality": "real", "deliverable": True, "source": "default"}


def strip(sides):
    return {name: {k: v for k, v in entry.items() if k != "at"} for name, entry in sides.items()}


stands = {"code_repos": [{"name": "app", "path": "app"}], "environments": [{"name": "dev"}]}


def break_registry(root):
    PK.record_path(root).parent.mkdir(parents=True, exist_ok=True)
    PK.record_path(root).write_text("{not json", encoding="utf-8")

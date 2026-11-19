"""FV3-41 (t-1558 R1): `story_step start --scope` on an S6 the code closed writes nothing before step 1b.

Reuses the S6 fixtures of the close rows (`test_story_step_manual_block`: `_s6_world`, `_close`)."""
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import check_eq, finish, temp_dir  # noqa: E402
import test_story_step_manual_block as MB  # noqa: E402


def _tree_hash(root) -> str:
    """One hash of every file under the story folder (path + bytes): 'no bytes written' is this value unchanged."""
    digest = hashlib.sha256()
    for path in sorted(Path(root).rglob("*")):
        if path.is_file():
            digest.update(str(path.relative_to(root)).encode() + b"\0" + path.read_bytes())
    return digest.hexdigest()


def test_fv3_41_a_closed_s6_is_not_prepared_again():
    """KILLS: the guard after `_manual_block_check` (X3 prepare runs, request.json rewritten); a guard that also catches an open S6; an
    unreadable record read as written. Rows: closed -> refused-as-completed, nothing written; open -> today's prepare; record unreadable -> E9 door."""
    count = len(harness.RESULTS)
    author = "S6-qa-runner-1"
    for name, close, age, want in (("closed", True, False, (0, True, [], True)),
                                   ("open", False, False, (0, False, ["TC-2", "TC-3", "TC-4", "TC-5", "TC-6", "TC-7"], None)),
                                   ("record unreadable", True, True, (2, False, [], True))):
        with temp_dir() as root:
            ctl = MB._s6_world(root)
            if close:
                MB.BASE.record_stage_acceptance(root, "S6", author)
                MB._close(root, ctl, [])
            if age:
                data = MB._pipeline(root)
                data["stages"]["S6"]["finished"] = "2000-01-01T00:00:00+00:00"
                (root / "pipeline.json").write_text(json.dumps(data), encoding="utf-8")
            before = _tree_hash(root)
            code, text, seen = MB.start(root, ctl, "TC-2", prepare=lambda case: ([], f"refused {case}", ""))
            check_eq(f"{name}: exit code, the stage-closed words, what was prepared",
                     (code, "S6 is completed already" in text, seen["prepared"]), want[:3])
            if want[3] is not None:      # the open row's writes are today's (prepare is stubbed: the fact is `prepared`)
                check_eq(f"{name}: the story folder is byte-identical", _tree_hash(root) == before, want[3])
    MB._assert_green_since(count)


def main():
    test_fv3_41_a_closed_s6_is_not_prepared_again()
    finish("test_story_step_close")


if __name__ == "__main__":
    main()

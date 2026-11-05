"""tools/canon_clock.py: the batch canon's wall time against the owner's 60 minute norm (F6-50, t-1702 D2 keys C1-C6).

Every case passes `now` and the start explicitly: nothing here waits on or reads the clock (FR-31).

Verification: python -m pytest tools/test_canon_clock.py -q
"""
import pathlib
import subprocess
import sys
from datetime import timedelta

import pytest

TOOLS = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
import canon_clock as CC  # noqa: E402

START = "2026-11-03T10:00:00Z"


def at(seconds):
    """`now` = the start + `seconds`."""
    return CC.parse_time(START) + timedelta(seconds=seconds)


def test_c1_the_limit_is_inclusive_3600_passes_3601_is_red():                    # C1 (M-g: >= instead of >)
    assert CC.judge(START, "", at(3600))[0] == 0
    code, line = CC.judge(START, "", at(3601))
    assert code == 1 and "over the hour" in line and "canon-over-hour: <reason>" in line


def test_c2_a_door_with_a_real_reason_passes_a_placeholder_is_no_door():          # C2 (M-h: an empty reason accepted)
    code, line = CC.judge(START, "fix\n\ncanon-over-hour: runner queue was 40 min\n", at(4000))
    assert code == 0 and 'passed by "canon-over-hour: runner queue was 40 min"' in line
    for placeholder in ("—", "-", "n/a", "none", "tbd", "?", "TBD", "N/A", ""):
        message = f"fix\n\ncanon-over-hour: {placeholder}\n"
        assert CC.judge(START, message, at(4000))[0] == 1, repr(placeholder)
    assert CC.judge(START, "see canon-over-hour: a reason mid-line", at(4000))[0] == 1     # a door starts a line
    assert CC.judge(START, "canon-over-hour: -\ncanon-over-hour: a real reason", at(4000))[0] == 0
    assert CC.judge(START, "canon-over-hour: reason", at(10))[0] == 0                      # the door is not needed under the limit


def test_f6_canon_clock_and_the_leftover_gate_refuse_the_same_empty_words():            # t-1755 F6: one table, not two
    import piles
    assert CC.PLACEHOLDERS is piles.LEFTOVER_EMPTY_WORDS
    for word in piles.LEFTOVER_EMPTY_WORDS + ("–", "нет", "НЕТ"):      # en dash and the Russian "no" were passed by the old table
        assert CC.judge(START, f"canon-over-hour: {word}\n", at(4000))[0] == 1, repr(word)
        assert CC.door_reason(f"canon-over-hour: {word}") is None, repr(word)


@pytest.mark.parametrize("created", [None, "", "   ", "yesterday", "2026-13-45T00:00:00Z", "2026-11-03T10:00:00"])
def test_c3_an_absent_or_unreadable_start_is_exit_2_and_the_door_passes_it(created):          # C3
    code, line = CC.judge(created, "", at(10))
    assert code == 2 and line.startswith("canon wall time: unknown -- ") and "the same door passes it" in line
    code, line = CC.judge(created, "canon-over-hour: queue", at(10))
    assert code == 0 and "unknown" in line and 'passed by "canon-over-hour: queue"' in line


def test_c4_a_start_after_the_clock_is_unknown_not_a_pass():                                     # C4
    code, line = CC.judge(START, "", at(-1))
    assert code == 2 and "after the clock" in line
    assert CC.judge(START, "canon-over-hour: skew", at(-1))[0] == 0
    assert CC.judge(START, "", at(0))[0] == 0                                                   # zero elapsed is fine


@pytest.mark.parametrize("text", ["2026-11-03T10:00:00Z", "2026-11-03T10:00:00+00:00", "2026-11-03T10:00:00.5Z",
                                  "2026-11-03T10:00:00.123456789Z", "2026-11-03T12:00:00+02:00", "2026-11-03T10:00:00z"])
def test_c5_z_offset_and_fractional_seconds_parse_to_the_same_instant(text):                     # C5
    parsed = CC.parse_time(text)
    assert abs((parsed - CC.parse_time(START)).total_seconds()) < 1


def test_c5_naive_and_empty_timestamps_are_refused():
    for bad in ("2026-11-03T10:00:00", "", "  ", "nonsense"):
        with pytest.raises(ValueError):
            CC.parse_time(bad)


def test_c6_the_printed_line_shape():                                                            # C6
    assert CC.judge(START, "", at(125)) == (0, "canon wall time: 2 min 5 s (limit 60 min) -- within the hour")
    code, line = CC.judge(START, "", at(3725))
    assert code == 1 and line.startswith("canon wall time: 62 min 5 s (limit 60 min) -- over the hour: the owner's norm")
    assert "\n" not in line and line.isascii()
    code, line = CC.judge(START, "canon-over-hour: queue", at(3725))
    assert line == 'canon wall time: 62 min 5 s (limit 60 min) -- over the hour, passed by "canon-over-hour: queue"'


def test_the_command_line_reads_the_overrides_and_the_environment(tmp_path):
    tool = str(TOOLS / "canon_clock.py")
    p = subprocess.run([sys.executable, "-B", tool, "--created-at", START, "--now", "2026-11-03T10:01:30Z"],
                       capture_output=True, text=True, timeout=60)
    assert p.returncode == 0 and p.stdout == "canon wall time: 1 min 30 s (limit 60 min) -- within the hour\n"
    env = {"CI_PIPELINE_CREATED_AT": START, "CI_COMMIT_MESSAGE": "x\ncanon-over-hour: queue\n", "PATH": "",
           "SYSTEMROOT": ""}
    p = subprocess.run([sys.executable, "-B", tool, "--now", "2026-11-03T12:00:00Z"], capture_output=True,
                       text=True, timeout=60, env=env)
    assert p.returncode == 0 and "passed by" in p.stdout
    p = subprocess.run([sys.executable, "-B", tool, "--now", "2026-11-03T12:00:00Z"], capture_output=True,
                       text=True, timeout=60, env={"PATH": "", "SYSTEMROOT": ""})
    assert p.returncode == 2 and "unknown" in p.stdout
    p = subprocess.run([sys.executable, "-B", tool, "--now", "garbage"], capture_output=True, text=True, timeout=60)
    assert p.returncode == 2 and p.stdout == ""                                                  # argparse refuses

#!/usr/bin/env python3
"""The canon clock (F6-50): how long the batch canon pipeline has been running, against the owner's norm.

The owner's norm (28.10.2026) is a batch canon within 60 minutes, always in CI (03.11.2026). The `canon-clock`
job of .gitlab-ci.yml runs this last in every api/web pipeline (`when: always`) and prints ONE line:

    canon wall time: <M> min <S> s (limit 60 min) -- <verdict>

Elapsed = now - CI_PIPELINE_CREATED_AT, wall time with the runner queue included (the norm is wall time).
Exit 0 at elapsed <= 3600 s; exit 1 above it. The door is a line `canon-over-hour: <reason>` in the head commit
message (CI_COMMIT_MESSAGE): with a real reason an over-the-hour canon passes (exit 0, the line says so); a
placeholder reason ("-", "n/a", "none", "tbd", "?") is not a door. A start that cannot be read (variable absent,
unparseable, or in the future) is exit 2, never a pass: an unknown is not a green clock; the same door passes it.

Overrides for tests and by hand: --created-at, --message, --now (ISO 8601; `Z`, `+00:00`, fractions are read).
A timestamp without a zone is not read (it would be a guess), so it is the unknown case.

Verification: python -m pytest tools/test_canon_clock.py -q
"""
import argparse
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from piles import LEFTOVER_EMPTY_WORDS as PLACEHOLDERS  # noqa: E402  (t-1755 F6: a reason that says nothing is no reason; the ONE table of those words, the one the leftover gate refuses)

LIMIT_S = 3600
DOOR_RE = re.compile(r"^canon-over-hour:[ \t]*(\S.*)$", re.MULTILINE)
_FRACTION = re.compile(r"(\.[0-9]+)")


def parse_time(text: str) -> datetime:
    """An ISO 8601 timestamp WITH a zone (`Z`, `+00:00`, ...), fractions of any length; ValueError otherwise."""
    value = (text or "").strip()
    if not value:
        raise ValueError("empty")
    if value.endswith(("Z", "z")):
        value = value[:-1] + "+00:00"
    value = _FRACTION.sub(lambda m: (m.group(1) + "000000")[:7], value, count=1)     # fromisoformat: 3 or 6 digits
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError("no time zone")
    return parsed


def door_reason(message: str | None) -> str | None:
    """The reason of a `canon-over-hour:` line in the commit message, None when absent or a placeholder."""
    for match in DOOR_RE.finditer(message or ""):
        reason = match.group(1).strip()
        if reason.lower() not in PLACEHOLDERS:
            return reason
    return None


def judge(created_at: str | None, message: str | None, now: datetime) -> tuple[int, str]:
    """(exit code, the printed line)."""
    door = door_reason(message)
    why = None
    elapsed = 0.0
    if not (created_at or "").strip():
        why = "the pipeline start (CI_PIPELINE_CREATED_AT) is absent"
    else:
        try:
            elapsed = (now - parse_time(created_at)).total_seconds()
        except (ValueError, OverflowError) as exc:
            why = f"the pipeline start {created_at!r} cannot be read ({exc})"
        else:
            if elapsed < 0:
                why = f"the pipeline start {created_at!r} is after the clock ({int(-elapsed)} s)"
    if why:
        if door:
            return 0, f'canon wall time: unknown -- {why}; passed by "canon-over-hour: {door}"'
        return 2, (f"canon wall time: unknown -- {why}; the same door passes it "
                   '(a line "canon-over-hour: <reason>" in the head commit message)')
    minutes, seconds = divmod(int(elapsed), 60)
    head = f"canon wall time: {minutes} min {seconds} s (limit 60 min) -- "
    if elapsed <= LIMIT_S:
        return 0, head + "within the hour"
    if door:
        return 0, head + f'over the hour, passed by "canon-over-hour: {door}"'
    return 1, head + ("over the hour: the owner's norm (28.10.2026) is a batch canon within 60 minutes; find the "
                      "longest job in ci_read.py jobs <pipeline>; door: a line \"canon-over-hour: <reason>\" in the "
                      "head commit message")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="batch canon wall time against the 60 minute norm")
    ap.add_argument("--created-at", default=None, help="pipeline start (default: $CI_PIPELINE_CREATED_AT)")
    ap.add_argument("--message", default=None, help="head commit message (default: $CI_COMMIT_MESSAGE)")
    ap.add_argument("--now", default=None, help="the clock, ISO 8601 with a zone (default: the system clock)")
    args = ap.parse_args(argv)
    created = args.created_at if args.created_at is not None else os.environ.get("CI_PIPELINE_CREATED_AT")
    message = args.message if args.message is not None else os.environ.get("CI_COMMIT_MESSAGE")
    if args.now is not None:
        try:
            now = parse_time(args.now)
        except ValueError as exc:
            ap.error(f"--now {args.now!r} cannot be read ({exc})")
    else:
        now = datetime.now(timezone.utc)
    code, line = judge(created, message, now)
    print(line)
    return code


if __name__ == "__main__":
    sys.exit(main())

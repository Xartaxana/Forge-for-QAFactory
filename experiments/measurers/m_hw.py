"""M-HW (t-1518 §5.4, HF7-4): `human_wait` of a transcript under the OLD predicate and the NEW classifier.

A measurement, not a test. The same transcript is scanned twice and only the predicate changes:
  old      a `user` row with a `promptId` is the person coming back (`person_rule=False`, today's reader);
  new      `cost_capture.user_line_kind` (flags `isMeta`/`isCompactSummary`, `tool_result`, notification prefixes);
  new+turn the new classifier plus `start_turn_activities` (the turn that opened an activity is its own; the wait is
           worked out on that list). Equal to `new` when no activities are given.
Each transcript is COPIED into a temporary folder first and the copy is read; the original is never opened for
writing. Output, one line per transcript: `<name>  old <seconds>/<answers>  new <seconds>/<answers>  new+turn ...`.

  python -B experiments/measurers/m_hw.py --synthetic
      builds a small transcript out of invented rows (a person's turn, a tool result, an `isMeta` row, a
      `<task-notification>` row, a person's turn) and checks the numbers it must give: old 190/5, new 70/2. Exit 0
      when they match, 2 when they do not (a divergence is a stop and a report, never a fit).
  python -B experiments/measurers/m_hw.py <transcript.jsonl> [<transcript.jsonl> ...] [--activities <file.json>]
        [--cap <seconds>] [--expect-old S/N ...] [--expect-new S/N ...]
      the real run (on the machine with the stand: full copies of the sessions to compare). `--activities` is a JSON
      list of activity records (`activity_id`, `segments`) as `state/activities/*.json` holds them; without it every
      row is unclassified. `--expect-old` / `--expect-new` are the control numbers, one per transcript in order; a
      mismatch exits 2.
"""
import argparse
import json
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[2] / "ai-packages" / "qa-factory" / "scripts"
sys.path.insert(0, str(SCRIPTS))
import cost_capture as C  # noqa: E402

CAP_DEFAULT = 1800


def measure(path: Path, activities: list, cap: float) -> dict:
    """`{old, new, new_turn}`, each `(seconds, answers)`, over a copy of `path`."""
    with tempfile.TemporaryDirectory(prefix="m_hw-") as folder:
        copy = Path(folder) / path.name
        shutil.copy2(path, copy)
        old_events = C.scan_file(copy, person_rule=False)[5]
        rule = C._person_rule()
        if not rule:
            raise SystemExit("m_hw: the host report forms hold no claude.not_a_person_turn: nothing to measure")
        new_events = C.scan_file(copy, person_rule=rule)[5]
    bound, _kept = C.attribution_activities(activities)
    turned = C.start_turn_activities(bound, new_events)
    return {"old": C.human_wait(old_events, bound, cap),
            "new": C.human_wait(new_events, bound, cap),
            "new_turn": C.human_wait(new_events, turned, cap)}


def said(pair) -> str:
    return f"{pair[0]:,.0f}/{pair[1]}"


def parse_pair(text: str) -> tuple:
    seconds, answers = text.replace(",", "").split("/")
    return float(seconds), int(answers)


def synthetic_transcript(folder: Path) -> Path:
    """Invented rows only: no real session, no personal path, no money."""
    base = datetime(2026, 10, 1, 10, 0, 0, tzinfo=timezone.utc).timestamp()

    def stamp(offset):
        return datetime.fromtimestamp(base + offset, tz=timezone.utc).isoformat().replace("+00:00", "Z")

    def assistant(offset, n):
        return {"type": "assistant", "timestamp": stamp(offset), "requestId": f"r{n}", "uuid": f"a{n}",
                "message": {"model": "claude-sonnet-5", "usage": {"input_tokens": 1, "output_tokens": 1},
                           "content": [{"type": "text", "text": "placeholder"}]}}

    def user(offset, n, content, **extra):
        return dict({"type": "user", "timestamp": stamp(offset), "uuid": f"u{n}", "promptId": f"p{n}",
                     "message": {"role": "user", "content": content}}, **extra)

    rows = [assistant(0, 1),
            user(10, 1, "placeholder question"),                                                  # a person: both count it
            assistant(20, 2),
            user(50, 2, [{"type": "tool_result", "tool_use_id": "t1", "content": "ok"}]),          # the host answering a tool
            assistant(55, 3),
            user(85, 3, "placeholder meta", isMeta=True),                                           # an `isMeta` row
            assistant(90, 4),
            user(150, 4, "<task-notification>placeholder</task-notification>"),                    # a background task
            assistant(155, 5),
            user(215, 5, "placeholder second question")]                                            # a person again
    path = folder / "synthetic.jsonl"
    path.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    return path


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("transcripts", nargs="*")
    parser.add_argument("--synthetic", action="store_true", help="run on invented rows and check the numbers they must give")
    parser.add_argument("--activities", help="JSON list of activity records")
    parser.add_argument("--cap", type=float, default=CAP_DEFAULT, help="the wait cap in seconds (default 1800)")
    parser.add_argument("--expect-old", action="append", default=[], metavar="S/N")
    parser.add_argument("--expect-new", action="append", default=[], metavar="S/N")
    args = parser.parse_args(argv)
    activities = []
    if args.activities:
        activities = json.loads(Path(args.activities).read_text(encoding="utf-8-sig"))
        if not isinstance(activities, list):
            raise SystemExit("m_hw: --activities must be a JSON list")
    paths, expect_old, expect_new = [Path(p) for p in args.transcripts], list(args.expect_old), list(args.expect_new)
    holder = None
    if args.synthetic:
        holder = tempfile.TemporaryDirectory(prefix="m_hw-syn-")
        # the numbers the invented rows must give, unless the caller names others (the negative control: a wrong one fails)
        paths, expect_old, expect_new = [synthetic_transcript(Path(holder.name))], expect_old or ["190/5"], expect_new or ["70/2"]
    if not paths:
        parser.error("give a transcript or --synthetic")
    bad = 0
    try:
        for i, path in enumerate(paths):
            got = measure(path, activities, args.cap)
            print(f"{path.name}  old {said(got['old'])}  new {said(got['new'])}  new+turn {said(got['new_turn'])}")
            for label, wanted in (("old", expect_old), ("new", expect_new)):
                if i < len(wanted) and parse_pair(wanted[i]) != (float(round(got[label][0])), got[label][1]):
                    bad += 1
                    print(f"  MISMATCH {label}: expected {wanted[i]}, got {said(got[label])} - a stop and a report, not a fit")
    finally:
        if holder is not None:
            holder.cleanup()
    print("m_hw: control numbers match" if not bad and (expect_old or expect_new) else
          "m_hw: no control numbers given" if not bad else f"m_hw: {bad} control number(s) differ")
    return 2 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

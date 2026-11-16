"""dispatch_new.py -- print the header lines of a dispatch in the form tools/dispatch_manifest.py reads (offload C1, M7).

    python -B tools/dispatch_new.py --kind builder --task t-862 [--feature F19] [--node slug/N/id]
        --given <p>... --owns <abs>... --non-goals "<t>" --handoff <abs .md> --edges "<t>" --dod "<cmd>"
        --siblings "<t>" [--designer <abs> | "skip -- <why>" | "resubmission t-NNN"]

The generator has NO grammar of its own: it only lays the values out one header per line (list values one path per line
under their header), then asks the launch hook's own decision (dispatch_gate.decide_full: completeness, handoff folder, paths; no description,
so no label check) and the one id reader (header_ids). Whatever the hook refuses, this refuses (exit 2, the hook's message
with its doors on stderr, nothing on stdout); a degraded read is refused too. A `--task`, `--node` or `--feature` that
header_ids does not read back is refused the same way. Pure output: stdout only, no file. An argument holding a newline
or a backtick, and an empty `--given`/`--owns` item, are refused before anything is printed (they could forge a header,
close the DoD span or end the section); these are the only rules of the generator's own. A new owned file is written
`<abs path> (new)`.

Exit: 0 printed (hook notes: one stderr line each); 2 refused.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_TOOLS_DIR = Path(__file__).resolve().parent
if str(_TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(_TOOLS_DIR))
import dispatch_gate  # noqa: E402
import dispatch_manifest  # noqa: E402
import streams  # noqa: E402

KINDS = ("builder", "critic", "designer", "scout")
FORBIDDEN_CHARS = ("\n", "\r", "`")


def _parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="dispatch_new.py", description=__doc__.splitlines()[0])
    ap.add_argument("--kind", required=True, choices=KINDS)
    ap.add_argument("--task", required=True)
    ap.add_argument("--feature")
    ap.add_argument("--node")
    ap.add_argument("--given", nargs="*", default=[])
    ap.add_argument("--owns", nargs="*", default=[])
    ap.add_argument("--non-goals", dest="non_goals", default="")
    ap.add_argument("--handoff", default="")
    ap.add_argument("--edges", default="")
    ap.add_argument("--dod", default="")
    ap.add_argument("--siblings", default="")
    ap.add_argument("--designer")
    return ap


def _forbidden(args) -> str:
    """The name of the first argument holding a newline / carriage return / backtick, or ''."""
    for name, value in vars(args).items():
        for item in (value if isinstance(value, list) else [value]):
            if isinstance(item, str) and any(c in item for c in FORBIDDEN_CHARS):
                return name
    return ""


def _empty_item(args) -> str:
    """The name of the first list argument holding an empty or whitespace-only item (it would end the section), or ''."""
    for name in ("given", "owns"):
        if any(not p.strip() for p in getattr(args, name)):
            return name
    return ""


def _path(p: str) -> str:
    """Backtick a path holding whitespace; a trailing ` (new)` marker (the owns door) stays outside the span."""
    mark = ""
    if p.lower().endswith(" (new)"):
        p, mark = p[:-6], p[-6:]
    return ("`%s`" % p if any(c.isspace() for c in p) else p) + mark


def build_text(args) -> str:
    """The header lines. Layout only: one header per line; paths one per line under `given:` / `owns:`."""
    lines = ["task: %s" % args.task]
    if args.node:
        lines.append("node: %s" % args.node)
    if args.feature:
        lines.append("feature: %s" % args.feature)
    lines.append("given:")
    lines.extend(_path(p) for p in args.given)
    lines.append("owns:")
    lines.extend(_path(p) for p in args.owns)
    lines.append("non-goals: %s" % args.non_goals)
    lines.append("handoff: %s" % _path(args.handoff) if args.handoff else "handoff:")
    lines.append("edges: %s" % args.edges)
    lines.append("DoD: `%s`" % args.dod if args.dod else "DoD:")
    lines.append("siblings: %s" % args.siblings)
    if args.designer is not None:
        # the checker's own two forms stay as typed; anything else is a path
        is_form = bool(dispatch_manifest._DESIGNER_SKIP_RE.match(args.designer)
                       or dispatch_manifest._DESIGNER_RESUBMISSION_RE.match(args.designer))
        lines.append("designer: %s" % (args.designer if is_form else _path(args.designer)))
    return "\n".join(lines) + "\n"


def _ids_refusal(args, text: str) -> str:
    """'' when header_ids reads back every id that was asked for; else a refusal text naming the one that was not."""
    read = dispatch_manifest.header_ids(dispatch_manifest.section_cut(text))
    bad = [k for k, v in (("task", args.task), ("node", args.node), ("feature", args.feature))
           if v is not None and read.get(k) != v]
    if not bad:
        return ""
    return ("DISPATCH ID REFUSED: --%s is not read back by the header reader (task t-NNN with an optional lower-case "
            "letter, node <slug>/<N>/<id>, feature Fnn); nothing printed." % ", --".join(bad))


def main(argv=None) -> int:
    streams.utf8_stdio()
    args = _parser().parse_args(argv)
    name = _forbidden(args)
    if name:
        print("DISPATCH ARGUMENT REFUSED: --%s holds a newline or a backtick; it would forge or break a header line. "
              "Write it on one line without backticks (the DoD command is wrapped for you)." % name.replace("_", "-"),
              file=sys.stderr)
        return 2
    name = _empty_item(args)
    if name:
        print("DISPATCH ARGUMENT REFUSED: --%s holds an empty item; a blank line would end the section. "
              "Drop the empty value." % name, file=sys.stderr)
        return 2
    text = build_text(args)
    refusal = _ids_refusal(args, text)
    if refusal:
        print(refusal, file=sys.stderr)
        return 2
    # the launch hook's own decision (completeness, handoff folder, paths); no description, so the label check is skipped
    payload = {"cwd": str(_TOOLS_DIR.parent), "tool_name": "Agent",
               "tool_input": {"subagent_type": args.kind, "prompt": text}}
    try:
        decision = dispatch_gate.decide_full(payload)
    except Exception as exc:  # fail closed: an unchecked text is not handed out
        print("DISPATCH CHECK FAILED (%s: %s): the checker could not read this text; nothing printed."
              % (type(exc).__name__, exc), file=sys.stderr)
        return 2
    if decision.code != 0:
        print(decision.message, file=sys.stderr)
        return 2
    if decision.cut is None or decision.cut.degraded:
        print("DISPATCH CHECK FAILED: the text could only be read in a degraded way, so it was not checked; "
              "nothing printed.", file=sys.stderr)
        return 2
    note = "\n".join(n for n in decision.notes if n)
    if note:
        print(note, file=sys.stderr)
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())

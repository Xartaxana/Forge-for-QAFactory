"""dispatch_new.py -- print the header lines of a dispatch in the form tools/dispatch_manifest.py reads (offload C1, M7).

    python -B tools/dispatch_new.py --kind builder --task t-862 --feature F19 [--node slug/N/id]
        --given <p>... --owns <abs>... --non-goals "<t>" --handoff <abs .md> --edges "<t>" --dod "<cmd>"
        --siblings "<t>" [--names <n>...] [--designer <abs> | "skip -- <why>" | "resubmission t-NNN"]
        [--test "<where> | expected from: <source>"...]  (one `test:` line each, right after DoD:; the gate over the designer threshold)
        [--facts "<claim> | <command> | <result>"... | "none -- <why>"]

The generator has NO grammar of its own: it lays the values out one header per line (list values one path per line
under their header), appends the readers block of tools/owns_readers.py (data about the owned paths, not grammar: behind a
blank line, after the last header; only for a dispatch that owns paths), and asks the launch hook's own decision
(dispatch_gate.decide_full: completeness, handoff folder, paths; no description, so no label check) on headers + block, and the
one id reader (header_ids). Whatever the hook refuses, this refuses (exit 2, the hook's message with its doors on stderr,
nothing on stdout); a degraded read is refused too. A `--task`, `--node` or `--feature` that header_ids does not read back is
refused the same way. `--feature` is required with `--task` (FG7-73: the hook refuses a task: line with no feature:).
A block the hook refuses is replaced by `readers: unknown -- the manifest check refused the block (...)`
(one stderr line says so); a tool that raises gives `readers: unknown -- <ExcType>: <first line>`: a failing helper never
blocks or hides a dispatch and never prints a count it did not measure. Stdout only, no file. An argument holding a newline
or a backtick, and an empty `--given`/`--owns` item, are refused before anything is printed (they could forge a header,
close the DoD span or end the section). A new owned file is written `<abs path> (new)`; `--names <n>...` passes the names the
spec changes to the readers tool (` (new)` marks a name the change creates). The default (counts) block is printed, never
`--readers`.

Exit: 0 printed (hook notes: one stderr line each); 2 refused.
"""
from __future__ import annotations

import argparse
import shlex
import sys
from pathlib import Path

_TOOLS_DIR = Path(__file__).resolve().parent
if str(_TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(_TOOLS_DIR))
import dispatch_gate  # noqa: E402
import dispatch_manifest  # noqa: E402
import gitcmd  # noqa: E402
import owns_readers  # noqa: E402
import streams  # noqa: E402

KINDS = ("builder", "critic", "designer", "scout")
FORBIDDEN_CHARS = ("\n", "\r", "`")


def _parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="dispatch_new.py", description=__doc__.splitlines()[0])
    ap.add_argument("--kind", required=True, choices=KINDS)
    ap.add_argument("--task", required=True)
    ap.add_argument("--feature", required=True)  # FG7-73: with --task (always given) the hook refuses a dispatch without it
    ap.add_argument("--node")
    ap.add_argument("--given", nargs="*", default=[])
    ap.add_argument("--owns", nargs="*", default=[])
    ap.add_argument("--non-goals", dest="non_goals", default="")
    ap.add_argument("--handoff", default="")
    ap.add_argument("--edges", default="")
    ap.add_argument("--dod", default="")
    ap.add_argument("--siblings", default="")
    ap.add_argument("--names", nargs="*", default=[])
    ap.add_argument("--designer")
    ap.add_argument("--facts", nargs="*", default=[])
    ap.add_argument("--test", action="append", default=[])  # test rules S-C: repeatable, printed as `test: <value>`
    return ap


def _forbidden(args) -> str:
    """The name of the first argument holding a newline / carriage return / backtick, or ''. `--facts` may hold backticks:
    a measured result grepped from this repo's markdown usually does, and the generator wraps nothing in them for facts:."""
    for name, value in vars(args).items():
        banned = FORBIDDEN_CHARS[:2] if name == "facts" else FORBIDDEN_CHARS
        for item in (value if isinstance(value, list) else [value]):
            if isinstance(item, str) and any(c in item for c in banned):
                return name
    return ""


def _empty_item(args) -> str:
    """The name of the first list argument holding an empty or whitespace-only item (it would end the section), or ''."""
    for name in ("given", "owns", "facts", "test"):
        if any(not p.strip() for p in getattr(args, name)):
            return name
    return ""


def _path(p: str) -> str:
    """Backtick a path holding whitespace; a trailing ` (new)` marker (the owns door) stays outside the span."""
    mark = ""
    if p.lower().endswith(" (new)"):
        p, mark = p[:-6], p[-6:]
    return ("`%s`" % p if any(c.isspace() for c in p) else p) + mark


NOT_APPENDED = "registry preflight: not appended (the manifest check refused the longer DoD)"


def _refusal_text(decision) -> str:
    """The text to print when `decision` is a refusal (a string from _decide, or a non-zero code), else ''."""
    return decision if isinstance(decision, str) else (decision.message or "DISPATCH REFUSED") if decision.code != 0 else ""


def _without_tests(cmd: str) -> str:
    """`cmd` (a command_for call) minus the test_*.py names of its `--paths` list: the DOD-RUN check counts such a name as a test
    run (R3 max 3, R2 canon-only), and this is a lint call. No path left: the `lint` id goes too; no id left: ''."""
    head, sep, tail = cmd.partition(" --paths ")
    if not sep:
        return cmd
    keep = [p for p in shlex.split(tail) if not (Path(p).name.startswith("test_") and p.endswith(".py"))]
    ids = head.split(" check ", 1)[1].split()
    if not keep:
        ids = [i for i in ids if i != "lint"]
    out = "python -B tools/registry_preflight.py check " + " ".join(ids) if ids else ""
    if keep and ids:
        out += " --paths " + " ".join(shlex.quote(p) if any(c in p for c in " '\"") else p for p in keep)
    return out


def _dod(args) -> str:
    """The DoD command; for a builder whose owns touch a registry_preflight table row the row's `check` call is appended after
    ' ; then ' so the one witness run includes it (FG7-93). No owns, no row, a non-builder, an empty DoD or a DoD that already
    names registry_preflight.py: the DoD is returned as typed. A selector that cannot run leaves a visible gap, never a silent skip."""
    if args.kind != "builder" or not args.owns or not args.dod or "registry_preflight.py check" in args.dod:
        return args.dod
    try:
        import registry_preflight  # noqa: E402
        # command_for reads the absolute `<path> (new)` form itself (a new file keeps its A status, which some rows need)
        cmd = registry_preflight.command_for(list(args.owns), _TOOLS_DIR.parent)
        cmd = _without_tests(cmd) if cmd else cmd
    except Exception as exc:  # a failing selector never blocks a dispatch
        return "%s ; then registry preflight: not computed (%s)" % (args.dod, type(exc).__name__)
    return "%s ; then %s" % (args.dod, cmd) if cmd else args.dod


def build_text(args, augment: bool = True, dod: str = None) -> str:
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
    if dod is None:
        dod = _dod(args) if augment else args.dod
    lines.append("DoD: `%s`" % dod if dod else "DoD:")
    lines.extend("test: %s" % t for t in args.test)
    lines.append("siblings: %s" % args.siblings)
    if args.designer is not None:
        # the checker's own two forms stay as typed; anything else is a path
        is_form = bool(dispatch_manifest._DESIGNER_SKIP_RE.match(args.designer)
                       or dispatch_manifest._DESIGNER_RESUBMISSION_RE.match(args.designer))
        lines.append("designer: %s" % (args.designer if is_form else _path(args.designer)))
    if args.facts:
        # the Lead's measured facts (F13): one line per fact under the header, as typed (the gate reads the form only)
        lines.append("facts:")
        lines.extend(args.facts)
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


def _decide(kind: str, text: str):
    """The launch hook's decision on `text`, or a refusal STRING when the checker itself could not run (fail closed)."""
    payload = {"cwd": str(_TOOLS_DIR.parent), "tool_name": "Agent",
               "tool_input": {"subagent_type": kind, "prompt": text}}
    try:
        return dispatch_gate.decide_full(payload)
    except Exception as exc:  # an unchecked text is not handed out
        return ("DISPATCH CHECK FAILED (%s: %s): the checker could not read this text; nothing printed."
                % (type(exc).__name__, exc))


def _clean(decision) -> bool:
    """True for a decision that passed and was read whole: not a refusal string, code 0, a cut that is there and not degraded."""
    return (not isinstance(decision, str) and decision.code == 0
            and decision.cut is not None and not decision.cut.degraded)


def _readers_block(args) -> str:
    """The default (counts) readers block of tools/owns_readers.py for the owned paths; a tool that raises is the unknown line."""
    try:
        return owns_readers.render(owns_readers.report(args.owns, args.given, args.names))
    except Exception as exc:  # a failing helper never blocks a dispatch
        return "readers: unknown -- %s: %s\n" % (type(exc).__name__, gitcmd.first_line(str(exc), 160))


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
    headers = build_text(args, augment=False)
    refusal = _ids_refusal(args, headers)
    if refusal:
        print(refusal, file=sys.stderr)
        return 2
    # the launch hook's own decision on the headers first: a refused dispatch never runs the readers tool (the same refusal
    # step 4 would end in)
    decision = _decide(args.kind, headers)
    if _refusal_text(decision):
        print(_refusal_text(decision), file=sys.stderr)
        return 2
    # FG7-93: the typed DoD passed alone (a bad one is refused exactly as before); now the same DoD with the preflight call.
    # The call lists owned test_*.py files, which the DOD-RUN check counts as runs (it is a lint call, not a run): a refusal of
    # the longer span never blocks a dispatch that the typed DoD passes -- the typed DoD is printed with a visible gap text
    longer = build_text(args)
    if longer != headers:
        got = _decide(args.kind, longer)
        if _clean(got):
            headers, decision = longer, got
        else:
            headers = build_text(args, dod=args.dod + " ; then " + NOT_APPENDED)
            decision = _decide(args.kind, headers)
            if _refusal_text(decision):
                headers = build_text(args, augment=False)  # even the gap text is refused: the typed DoD, as before
                decision = _decide(args.kind, headers)
                if _refusal_text(decision):
                    print(_refusal_text(decision), file=sys.stderr)
                    return 2
    text = headers
    block = _readers_block(args) if args.owns else ""
    if block:
        # the hook checks exactly what is printed: the block sits behind a blank line, so it never enters a manifest section;
        # anything but a clean pass on headers + block (a refusal, a checker that raised, a degraded cut) is not a reason to
        # refuse the dispatch: the block is replaced by the unknown line and the text is decided once more (section 3.1)
        full = headers + "\n" + block
        got = _decide(args.kind, full)
        if _clean(got):
            text, decision = full, got
        else:
            why = got if isinstance(got, str) else (got.message or "the cut was degraded")
            text = headers + "\n" + "readers: unknown -- the manifest check refused the block (%s)\n" % gitcmd.first_line(why, 160)
            decision = _decide(args.kind, text)
            if isinstance(decision, str):
                print(decision, file=sys.stderr)
                return 2
            if decision.code != 0:
                print(decision.message, file=sys.stderr)
                return 2
            print("OWNS_READERS: the manifest check refused the readers block -- a defect of tools/owns_readers.py; "
                  "the block was replaced", file=sys.stderr)
    if decision.cut is None or decision.cut.degraded:
        print("DISPATCH CHECK FAILED: the text could only be read in a degraded way, so it was not checked; "
              "nothing printed.", file=sys.stderr)
        return 2
    refusal = _ids_refusal(args, text)
    if refusal:
        print(refusal, file=sys.stderr)
        return 2
    note = "\n".join(n for n in decision.notes if n)
    if note:
        print(note, file=sys.stderr)
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())

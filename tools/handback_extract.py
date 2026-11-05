"""handback_extract.py -- copy a worker's final hand-back out of its transcript into a report file (t-744 N2, F19).

A worker's report reaches the Lead as a FILE written by code, not as text the Lead retypes on the dearest
model. The transcript <projects>/<slug>/<session>/subagents/agent-<id>.jsonl is complete even when the
harness' .output twin is 0 bytes (an uncreated hard link), so this tool reads the transcript.

    python tools/handback_extract.py <transcript.jsonl> <out.md> [--header TEXT]
    python tools/handback_extract.py --agent <agent id> <out.md> [--header TEXT]

The transcript is read ONLY through tools/transcripts.py (SIBLING_MAP axis 14): iter_lines (utf-8, an
undecodable byte becomes U+FFFD), parse_line (a truncated or non-JSON line is skipped), content_blocks and
is_finished (whether the worker ended in a hand-back). There is no second JSONL reader here.

The text taken is the LAST hand-back: the last assistant tool_use named SubagentHandback with a non-empty
`input.message`; failing that, the last non-empty assistant text. Not the longest -- a later short hand-back
(a resubmission after a hook block) beats an earlier long text.

Exit codes:
  0  written, the transcript ends in a SubagentHandback
  1  call error, nothing written (bad arguments, no transcript, unknown or ambiguous --agent id, no output
     folder, a read or write error)
  2  no final assistant text (0-byte file, no assistant text), nothing written
  3  the output file exists, left untouched (the file is created exclusively: the worker's own file is never
     overwritten, not even by a race)
  4  written, but the transcript does not end in a SubagentHandback (the worker is alive or was killed): the
     first line of the file is UNFINISHED_MARKER, or AFTER_HANDBACK_MARKER when a hand-back exists and tool
     calls followed it

stdout is ONE line and never the report body:
  written <out> bytes=<n> lines=<n> source=<handback|last_text> finished=<yes|no> digest=<v1 ...|none|n/d>
`lines` counts the report text the way the 25-line rule does (F-7): every "\\n" line, blank and fence lines
included, a line over LINE_WIDTH characters as ceil(len / LINE_WIDTH).

The `digest=` tail (t-797 F5-2, I2): tools/digest_form.py reads the EXTRACTED text (not the file, whose first line may be
a marker) and the tail reports what it found -- `digest=v1 objects=<n> trail=<n> flags=<n>[ first=<flag>]` for a digest
in form v1, `digest=none` for any other text (today's prose digest is extracted as prose and says so), `digest=n/d` when
the reader failed to import or raised. The file and the exit code never depend on it. Form: docs/tasks/exchange-form.md.

The trail against the transcript (t-863, F6-14): the `## Trail` rows of a digest are matched with the Read / Grep / Glob tool_use
calls of the WHOLE transcript (tool_calls: one streaming pass, iter_lines -- never the tail window). Each unmatched row counts in
ONE extra flag, `trail_unbacked:<n>`, which joins the flags=<n> count after the digest's own flags (so `first=` stays the digest's
first flag); the digest is still copied and printed whole -- a flag, not a refusal. The rule (digest_form.trail_backing_flags):
a read row needs a Read whose file_path contains the row's target; a grep / glob row (a zero row too) needs a Grep / Glob whose
pattern contains the row's pattern and whose path contains the target (a root target `.` needs no path); texts compared lower
case, backslash as slash, white space collapsed, no `./` or trailing slash on a path. With no transcript to check against
(digest_tail(text) called without calls, or the transcript unreadable) the flag is `trail_unchecked`, never `trail_unbacked`.
"""
import argparse
import re
import sys
from pathlib import Path

_TOOLS_DIR = Path(__file__).resolve().parent
if str(_TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(_TOOLS_DIR))
import streams  # noqa: E402
import transcripts  # noqa: E402
try:
    import digest_form  # noqa: E402
except Exception:  # degraded, loudly: the stdout line says `digest=n/d`; the file and the exit code are as without it (I2)
    digest_form = None

LINE_WIDTH = 200
UNFINISHED_MARKER = ("<!-- handback_extract: no SubagentHandback in the transcript; "
                     "this is the worker's last text, not its hand-back -->")
AFTER_HANDBACK_MARKER = ("<!-- handback_extract: the worker made tool calls after this SubagentHandback "
                         "(a refused stop, or still working); this hand-back may not be its final one -->")
EXIT_OK, EXIT_CALL, EXIT_NO_TEXT, EXIT_EXISTS, EXIT_UNFINISHED = 0, 1, 2, 3, 4


class _Parser(argparse.ArgumentParser):
    """argparse exits 2 on a bad call; here 2 means "no text", a bad call is 1."""

    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(EXIT_CALL, "handback_extract: %s\n" % message)


def _text_of(value):
    """value when it is a non-blank str, else None."""
    return value if isinstance(value, str) and value.strip() else None


def _candidates(obj):
    """(is_handback, text) of every candidate in one parsed assistant line, in order."""
    message = obj.get("message")
    if not isinstance(message, dict) or message.get("role") != "assistant":
        return
    content = message.get("content")
    if isinstance(content, str):
        blocks = [{"type": "text", "text": content}]
    else:
        blocks = [b for b in transcripts.content_blocks(obj) if isinstance(b, dict)]
    for block in blocks:
        if block.get("type") == "text":
            text = _text_of(block.get("text"))
            if text:
                yield False, text
        elif block.get("type") == "tool_use" and block.get("name") == transcripts.HANDBACK:
            inp = block.get("input")
            text = _text_of(inp.get("message")) if isinstance(inp, dict) else None
            if text:
                yield True, text


def extract(path):
    """(text, source, finished) of the last hand-back in the transcript, source "handback" or "last_text";
    None when the transcript holds no assistant text. Raises OSError (iter_lines, is_finished).

    `finished` is transcripts.is_finished, the one reader of it (t-840, F6-7): the file's last line is
    read whole at any length, so the live hand-back of 74153 bytes (agent-ab6233f5fbed2af68) is seen."""
    handback = last_text = None
    finished = transcripts.is_finished(path)
    for line in transcripts.iter_lines(path):
        obj = transcripts.parse_line(line)
        if obj is None:
            continue
        for is_handback, text in _candidates(obj):
            if is_handback:
                handback = text
            else:
                last_text = text
    if handback is not None:
        return handback.strip(), "handback", finished
    if last_text is not None:
        return last_text.strip(), "last_text", finished
    return None


def tool_calls(path):
    """The Read / Grep / Glob tool_use calls of the whole transcript as digest_form.ToolCall, in file order. Raises OSError.
    One streaming pass over every line (transcripts.iter_lines): a call in the first megabyte is seen as well as one in the last
    64 KB. A malformed or non-dict input gives a call with no path and no pattern, which backs nothing."""
    calls = []
    for line in transcripts.iter_lines(path):
        obj = transcripts.parse_line(line) if '"tool_use"' in line else None
        if obj is None:
            continue
        for block in transcripts.content_blocks(obj):
            name = block.get("name") if isinstance(block, dict) and block.get("type") == "tool_use" else None
            if name not in digest_form.BACKING_TOOL.values():
                continue
            inp = block.get("input") if isinstance(block.get("input"), dict) else {}
            calls.append(digest_form.ToolCall(name, inp.get("file_path" if name == "Read" else "path"), inp.get("pattern")))
    return calls


def _calls_of(path):
    """tool_calls(path), or None (the trail is `trail_unchecked`) when the transcript cannot be read again or the reader is
    missing: the report is already extracted, nothing here may change its exit code (I2)."""
    try:
        return tool_calls(path)
    except Exception:
        return None


def count_lines(text):
    """The report's length by the 25-line rule (F-7): "\\n" lines, blank ones included, a long line as
    ceil(len / LINE_WIDTH)."""
    return sum(max(1, -(-len(line) // LINE_WIDTH)) for line in text.split("\n"))


def digest_tail(text, calls=None):
    """The ` digest=...` tail of the stdout line for the extracted report text (see the module docstring). `calls` are the
    transcript's tool calls (tool_calls); None is "no transcript to check the trail against" -> `trail_unchecked`. Never raises: a
    reader that is missing or breaks is `digest=n/d`, because the report is already written and its exit code is decided."""
    try:
        d = digest_form.parse(text)
        if d is None:
            return " digest=none"
        found = digest_form.flags(d) + digest_form.trail_backing_flags(d, calls)
    except Exception:
        return " digest=n/d"
    first = " first=" + re.sub(r"\s+", "_", found[0]) if found else ""
    return " digest=v1 objects=%d trail=%d flags=%d%s" % (d.n_objects, d.n_trail, len(found), first)


def render(text, header, marker):
    """The file content: [marker], [header], the report text, one final newline."""
    parts = []
    if marker:
        parts.append(marker)
    header = header.rstrip()
    if header:
        parts.append(header)
    parts.append(text)
    return "\n\n".join(parts) + "\n"


def _parse(argv):
    parser = _Parser(prog="handback_extract.py", description=__doc__.split("\n")[0])
    parser.add_argument("--agent", metavar="ID", help="read the transcript of this agent id instead of a path")
    parser.add_argument("--header", default="", help="a line put above the report text")
    parser.add_argument("paths", nargs="+", metavar="PATH", help="[transcript] out.md")
    args = parser.parse_args(argv)
    want = 1 if args.agent else 2
    if len(args.paths) != want:
        parser.error("expected %s" % ("<out.md> after --agent" if args.agent else "<transcript> <out.md>"))
    return args


def _resolve_source(args):
    """The transcript path, or None (reported on stderr) when --agent names no single transcript."""
    if not args.agent:
        return args.paths[0]
    found = transcripts.find_agent_transcript(args.agent)
    if found is None:
        sys.stderr.write("handback_extract: agent id %r matches no single transcript\n" % args.agent)
    return found


def _write_new(out, data):
    """Create `out` exclusively and write data; the exit code (0, 1 or 3)."""
    try:
        with open(out, "xb") as fh:
            fh.write(data)
    except FileExistsError:
        sys.stderr.write("handback_extract: %s exists; left untouched\n" % out)
        return EXIT_EXISTS
    except OSError as exc:
        sys.stderr.write("handback_extract: cannot write %s: %s\n" % (out, exc))
        return EXIT_CALL
    return EXIT_OK


def main(argv=None):
    try:
        args = _parse(sys.argv[1:] if argv is None else argv)
    except SystemExit as exc:  # --help is 0, a bad call is 1 (_Parser.error)
        return exc.code
    src = _resolve_source(args)
    out = Path(args.paths[-1])
    if src is None:
        return EXIT_CALL
    if not out.parent.is_dir():
        sys.stderr.write("handback_extract: no folder %s for the output\n" % out.parent)
        return EXIT_CALL
    try:
        found = extract(src)
    except OSError as exc:
        sys.stderr.write("handback_extract: cannot read %s: %s\n" % (src, exc))
        return EXIT_CALL
    if found is None:
        sys.stderr.write("handback_extract: no assistant text in %s; nothing written\n" % src)
        return EXIT_NO_TEXT
    text, source, finished = found
    marker = None if finished else (AFTER_HANDBACK_MARKER if source == "handback" else UNFINISHED_MARKER)
    data = render(text, args.header, marker).encode("utf-8", errors="replace")
    code = _write_new(out, data)
    if code != EXIT_OK:
        return code
    print("written %s bytes=%d lines=%d source=%s finished=%s%s"
          % (out, len(data), count_lines(text), source, "yes" if finished else "no", digest_tail(text, _calls_of(src))))
    return EXIT_OK if finished else EXIT_UNFINISHED


if __name__ == "__main__":
    streams.utf8_stdio()
    sys.exit(main())

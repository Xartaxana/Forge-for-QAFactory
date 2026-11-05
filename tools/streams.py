"""One place that puts stdout and stderr on UTF-8 for the tools/ scripts OUTSIDE the mechanism chain (B-449).

A Windows pipe is cp1251, cp866 or ascii, and the reports print non-ASCII text; under such a stream a
script either dies with UnicodeEncodeError or prints the wrong bytes. Before this module sixteen tools
carried their own copy of the reconfigure loop, in six shapes. Now each calls

    streams.utf8_stdio()                 # at the place where its copy stood
    streams.utf8_stdio(newline="\\n")     # a report that must write LF on Windows too

The twin for the release side is ai-packages/qa-factory/scripts/console_io.py `utf8_stdio` (B-413). This
is a deliberate second copy: tools/ must not depend on the release package's layout, and the twin has no
`newline` parameter (adding one is a package edit).

RULE: a mechanism-chain link (a file in mechanism_gate.MECHANISM_PREFIXES under tools/) NEVER imports this
module, directly or through any chain of tools/ imports -- the links keep their own copies so that a
broken helper can never gate a hook. tools/test_streams.py checks both halves: S3 (no stream reconfigure
call outside the chain except here) and S4 (no link reaches this file). A link that must share it is brought
into the net by the Lead with a mechanism commit, not by an import.

Error direction: the function may leave a stream exactly as it was (a StringIO, a capture, a closed
stream, `None` under pythonw, a stream without `reconfigure`, a `reconfigure` that rejects an option) and
it NEVER raises and never rebinds `sys.stdout`. A stream that fails does not stop the other one. Streams
are looked up at CALL time, so a stream swapped in before the call is the one handled. stdin is never
touched. Importing the module has no side effect.
"""
from __future__ import annotations

import sys


def utf8_stdio(*, newline: str | None = None) -> None:
    """Reconfigure stdout and stderr, in place, to UTF-8 with errors="replace".

    `newline` is passed only when it is not None (an explicit newline=None would switch on os.linesep
    translation). The last call wins; calling twice is harmless."""
    options = {"encoding": "utf-8", "errors": "replace"}
    if newline is not None:
        options["newline"] = newline
    for name in ("stdout", "stderr"):
        stream = getattr(sys, name, None)
        try:
            stream.reconfigure(**options)
        except Exception:
            pass

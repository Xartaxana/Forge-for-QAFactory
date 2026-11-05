"""ci_read_common.py -- what the two CI readers share (GM1-4, t-1887): tools/ci_read.py (GitHub Actions) and
tools/ci_read_gitlab.py (the GitLab it replaces; deleted whole at the move).

Shared: the output filters (`sanitize` for REMOTE text, `sanitize_own` for the tool's own words and local paths), the
tail printer, the argument parser, the ONE token-variable reader (`token_env_name(key, fallback, ...)`: a parameter
pair, not a copy per backend), the refusal classes and the run loop (`run`). A backend is a `Backend`: its commands
(name -> function(args, token)), the key and fallback of its token variable, the hint printed when the variable is
unset, and an optional `check(args)` that refuses a bad argument BEFORE the token is read and before any request.

`piles.printable` (tools/piles.py) repeats `sanitize_own` on purpose: piles must not import a CI reader (t-1856).

Exit codes of `run`: 0 ok, 1 HTTP/network error or a refused answer, 2 missing token, a refused config or a refused
argument. The token value is never printed or logged."""

import argparse
import os
import re
import sys
import urllib.error
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

import dev_config  # noqa: E402

DEFAULT_GREP = r"FAIL|===|Error|Traceback"
DEFAULT_TAIL = 200
BODY_CHARS = 200
TIMEOUT_SECONDS = 30
FROM_FALLBACK = "the fallback token variable: there is no tools/dev.config.yaml"
_UNSAFE_RE = re.compile(r"[^A-Za-z0-9 _./:()=,'\[\]-]")


def sanitize(text: str) -> str:
    """Remote text: a character outside [A-Za-z0-9 _./:()=,'\\[\\]-] becomes "?"."""
    return _UNSAFE_RE.sub("?", text)


def emit(line: str) -> None:
    sys.stdout.write(sanitize(line) + "\n")


def sanitize_own(text: str) -> str:
    """For the tool's own words and a local path (not remote text): only what is not printable becomes "?"."""
    return "".join(ch if ch.isprintable() else "?" for ch in text)


def emit_own(line: str) -> None:
    sys.stdout.write(sanitize_own(line) + "\n")


class Refusal(Exception):
    """A refusal of the call (exit 2): the message is the tool's OWN text; remote parts are sanitized by the raiser."""


class Failure(Exception):
    """A refused answer (exit 1): the message is the tool's OWN text; remote parts are sanitized by the raiser."""


class TokenEnvRefusal(Refusal):
    """tools/dev.config.yaml exists but cannot name the token variable; the message says what is wrong and what
    is expected (it names the key and the file, never a value)."""


def from_config(key: str) -> str:
    return "the token variable named by %s in tools/dev.config.yaml" % key


def token_env_name(key, fallback, label, root, who="ci_read"):
    """(variable name, where the name comes from): the `key` (gitlab_token_env / github_token_env) of
    tools/dev.config.yaml; the `fallback` name, with ONE stderr line saying so (`who` prefixes it), ONLY when there is
    no such file; a file that exists and is unusable, empty or without the key raises TokenEnvRefusal (F-8: the one
    reader, the refusing behaviour -- every caller that can write goes through it). `label` ("GitLab"/"GitHub") only
    words the refusal."""
    try:
        cfg, origins = dev_config.resolve(root)
    except dev_config.DevConfigError as exc:
        raise TokenEnvRefusal(str(exc)) from None
    if origins[key] == "file":
        return cfg[key], from_config(key)
    if dev_config.refused_default(key, cfg, origins):
        raise TokenEnvRefusal(
            "%s names no %s (%s, %s) -- expected a line %s: NAME_OF_THE_VARIABLE naming the environment variable "
            "that holds the %s token; add it (template tools/%s) or delete the file to use %s"
            % (dev_config.CONFIG_NAME, key, cfg["path"],
               "the file is empty" if cfg["source"] != "file" else "the key is absent", key, label,
               dev_config.EXAMPLE_NAME, fallback))
    sys.stderr.write(sanitize("%s: no tools/dev.config.yaml, token variable %s" % (who, fallback)) + "\n")
    return fallback, FROM_FALLBACK


def _grep_lines(text: str, regex):
    pattern = re.compile(regex) if regex else None
    return [ln for ln in text.splitlines() if pattern is None or pattern.search(ln)]


def _emit_tail(text: str, regex, tail: int) -> None:
    """The last `tail` lines of the grep-filtered text, then a count line `(N of M lines)`."""
    lines = _grep_lines(text, regex)
    shown = lines[-tail:]
    for ln in shown:
        emit(ln)
    emit("(%d of %d lines)" % (len(shown), len(lines)))
    total = len(text.splitlines())
    if not lines and total:
        # t-418: "(0 of 0 lines)" read as an empty trace while the grep had simply matched nothing
        emit("(the text has %d lines and none matched the grep, --grep '' prints them all)" % total)


def _positive_int(text: str) -> int:
    value = int(text)
    if value < 1:
        raise argparse.ArgumentTypeError("must be 1 or more")
    return value


def http_error_line(exc: urllib.error.HTTPError) -> str:
    try:
        body = exc.read().decode("utf-8", errors="replace")
    except Exception:
        body = ""
    return "HTTP %s: %s" % (exc.code, body[:BODY_CHARS])


@dataclass
class Backend:
    name: str
    commands: dict                      # "pipelines" / "jobs" / "log" / "artifact" / "start" -> function(args, token)
    token_key: str
    token_fallback: str
    token_label: str
    missing_hint: str                   # contains one %s: the variable name
    root: Path = None
    check: Optional[Callable] = field(default=None)

    def token_env_name(self):
        return token_env_name(self.token_key, self.token_fallback, self.token_label, self.root)


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="ci_read.py", description="read (and start) CI runs with a few lines of output")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("pipelines")
    p.add_argument("--n", type=int, default=5)
    j = sub.add_parser("jobs")
    j.add_argument("id", type=int)
    lg = sub.add_parser("log")
    lg.add_argument("job_id", type=int)
    lg.add_argument("--grep", default=DEFAULT_GREP)
    lg.add_argument("--tail", type=_positive_int, default=DEFAULT_TAIL)
    ar = sub.add_parser("artifact")
    ar.add_argument("id", type=int)
    ar.add_argument("path")
    ar.add_argument("--grep", default=None)
    ar.add_argument("--tail", type=_positive_int, default=DEFAULT_TAIL)
    st = sub.add_parser("start")
    st.add_argument("--ref", default="main")
    return ap


def execute(args, backend: Backend) -> int:
    try:
        if backend.check is not None:
            backend.check(args)
        name, source = backend.token_env_name()
    except Refusal as exc:
        emit_own(str(exc))
        return 2
    token = os.environ.get(name)
    if not token:
        emit("%s is not set (its name comes from %s): %s" % (name, source, backend.missing_hint % name))
        return 2
    try:
        backend.commands[args.cmd](args, token)
    except urllib.error.HTTPError as exc:
        emit(http_error_line(exc))
        return 1
    except Refusal as exc:
        emit_own(str(exc))
        return 2
    except Failure as exc:
        emit_own(str(exc))
        return 1
    except (urllib.error.URLError, OSError, ValueError, re.error) as exc:
        emit("request failed: %s" % type(exc).__name__)
        return 1
    return 0


def run(argv, choose) -> int:
    """Parse, choose the backend (`choose()` -> Backend, or raises Refusal; no request is made before it), execute."""
    args = build_parser().parse_args(argv)
    try:
        backend = choose()
    except Refusal as exc:
        emit_own(str(exc))
        return 2
    return execute(args, backend)

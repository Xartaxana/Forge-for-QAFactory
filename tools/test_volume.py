#!/usr/bin/env python3
"""Commit-time WARN: a commit adds more test lines than product lines (owner 14.11.2026).

Usage (last line of .githooks/commit-msg): python tools/test_volume.py "$1" || true
Reads the STAGED diff, sums ADDED lines per class, prints one WARN to stderr when test > product and the
message carries no "tests-over: <reason>" line. ALWAYS exits 0: a WARN never blocks (FR-4 spirit).
"""
import fnmatch
import os
import re
import subprocess
import sys

# Data row (first match wins). Paths as git prints them, "/" separated. Unsure -> product (fewer WARNs).
EXCLUDED_GLOBS = (
    "docs/*", "plans/*", "logs/*", "kb/*", "*/changelog.d/*", "changelog.d/*", ".claude/*", ".githooks/*",
)
MEASURERS_PREFIX = "experiments/measurers/"
TEST_SEGMENTS = ("tests", "test", "fixtures")
TEST_BASENAMES = ("test_*.py", "*_test.py", "conftest.py", "*_testkit.py")
PRODUCT_PREFIXES = ("ai-packages/", "tools/", "gateway/", MEASURERS_PREFIX)

DOOR_RE = re.compile(r"^\s*tests-over:(.*)$", re.IGNORECASE)

WARN_TEXT = (
    "TEST VOLUME (WARN, the commit goes on): +{t} test lines vs +{p} product lines in this commit; name the "
    'reason in a line "tests-over: <reason>" of the message and in your report (docs/TESTING.md «Бюджет»).'
)


def classify(path):
    """Return 'test', 'product' or 'excluded' for a repo-relative path."""
    path = path.replace("\\", "/")
    if "/" not in path:
        return "excluded"  # root files
    if path.startswith("experiments/") and not path.startswith(MEASURERS_PREFIX):
        return "excluded"
    if any(fnmatch.fnmatchcase(path, g) for g in EXCLUDED_GLOBS):
        return "excluded"
    parts = path.split("/")
    if any(seg in TEST_SEGMENTS for seg in parts[:-1]) or any(
        fnmatch.fnmatchcase(parts[-1], b) for b in TEST_BASENAMES
    ):
        return "test"
    if path.startswith(PRODUCT_PREFIXES):
        return "product"
    return "excluded"


def new_path(raw):
    """The destination path of a numstat path field: 'a => b' or 'dir/{a => b}/f' (rename)."""
    m = re.match(r"^(.*)\{(.*) => (.*)\}(.*)$", raw)
    if m:
        pre, _old, new, post = m.groups()
        return (pre + new + post).replace("//", "/")
    if " => " in raw:
        return raw.split(" => ", 1)[1]
    return raw


def sum_numstat(text):
    """(test_added, product_added) from `git diff --numstat -M` text; binary rows skipped."""
    test = product = 0
    for line in text.splitlines():
        cols = line.split("\t", 2)
        if len(cols) < 3 or not cols[0].isdigit():
            continue  # binary ("-") or malformed
        cls = classify(new_path(cols[2].strip()))
        if cls == "test":
            test += int(cols[0])
        elif cls == "product":
            product += int(cols[0])
    return test, product


def door_reason(message):
    """None = no door line; '' = door with empty reason; else the reason. '#' lines are ignored."""
    found = None
    for line in message.splitlines():
        if line.lstrip().startswith("#"):
            continue
        m = DOOR_RE.match(line)
        if m:
            reason = m.group(1).strip()
            if reason:
                return reason
            found = ""
    return found


def decide(numstat_text, message, merge):
    """(warned, (test, product), text). A merge never warns; equal or both-zero is silent."""
    t, p = sum_numstat(numstat_text)
    if merge or t <= p:
        return False, (t, p), ""
    reason = door_reason(message)
    if reason:
        return False, (t, p), ""
    text = WARN_TEXT.format(t=t, p=p)
    if reason == "":
        text += ' (a "tests-over:" line is present but its reason is empty)'
    return True, (t, p), text


def _git(*args):
    return subprocess.run(
        ("git",) + args, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30
    )


def run(msg_file):
    try:
        r = _git("diff", "--cached", "--numstat", "-M")
        if r.returncode != 0:
            print("test_volume: not measured -- git diff failed: " + r.stderr.strip()[:200], file=sys.stderr)
            return
        g = _git("rev-parse", "--git-path", "MERGE_HEAD")
        merge = g.returncode == 0 and os.path.exists(g.stdout.strip())
        try:
            with open(msg_file, encoding="utf-8", errors="replace") as fh:
                message = fh.read()
        except (OSError, TypeError):
            message = ""
        _warned, _nums, text = decide(r.stdout, message, merge)
        if text:
            print(text, file=sys.stderr)
    except Exception as exc:  # never change the hook's exit code
        print("test_volume: not measured -- %s: %s" % (type(exc).__name__, exc), file=sys.stderr)


def main(argv):
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    run(argv[1] if len(argv) > 1 else "")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

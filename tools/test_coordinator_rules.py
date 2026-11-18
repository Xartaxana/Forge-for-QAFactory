"""The coordinator-rules read check (FG7-89): coordinator_rules.read_state / read_warn over synthetic transcripts.

Layer 3: ONE parameterised table (ROWS) of transcripts built once in tmp_path; each row names the verdict and the text
the detail must (not) hold. The card's section 5 safe-side lists are rows: must stay `unread` (limit-1 Read, error Read,
worktree copy, Write result, sidechain, a read before the newest boundary, a quoted toolUseResult), must stay
`cannot-judge` (missing transcript, no boundary within the cap), must stay silent (a worker, a probe payload).
"""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import coordinator_rules as cr  # noqa: E402

NAMES = cr.COORDINATOR_FILES
FILLER = json.dumps({"type": "assistant", "message": {"content": [{"type": "text", "text": "x" * 900}]}})


def _read(root, name, start=1, num=4, total=4, **extra):
    line = {"type": "user", "toolUseResult": {"type": "text", "file": {
        "filePath": str(Path(root) / name), "startLine": start, "numLines": num, "totalLines": total}}}
    line.update(extra)
    return json.dumps(line)


def _all(root, skip=()):
    return [_read(root, n) for n in NAMES if n not in skip]


def _hook(source):
    return json.dumps({"type": "attachment", "attachment": {"type": "hook_success", "hookName": "SessionStart:" + source}})


COMPACT = json.dumps({"type": "system", "subtype": "compact_boundary"})
def _quoted(root):
    return json.dumps({"type": "user", "message": {"content": [{"type": "text", "text": _read(root, "PROJECT.md")}]}})



MENTION = json.dumps({"type": "user", "message": {"content": [{"type": "text", "text": '"subtype":"compact_boundary"'}]}})
# (id, root key, lines(root), verdict, detail must hold, detail must not hold)
ROWS = [
    ("all-five-whole", "full", lambda r: _all(r), "read", "", "PROJECT"),
    ("start-then-all", "full", lambda r: [_hook("startup")] + _all(r), "read", "", "PROJECT"),
    ("one-unread-named", "full", lambda r: _all(r, skip=("PROJECT.md",)), "unread", "PROJECT.md", "COORDINATOR.md"),
    ("read-before-compact-boundary", "full", lambda r: _all(r) + [COMPACT], "unread", "COORDINATOR.md", ""),
    ("read-before-compact-hook", "full", lambda r: _all(r) + [_hook("compact")], "unread", "PROJECT.md", ""),
    ("read-before-clear", "full", lambda r: _all(r) + [_hook("clear")], "unread", "PROJECT.md", ""),
    ("resume-keeps-reads", "full", lambda r: _all(r) + [_hook("resume")], "read", "", "PROJECT"),
    ("newest-boundary-wins", "full", lambda r: [COMPACT] + _all(r) + [_hook("compact")] + _all(r, skip=("PROJECT.md",)),
     "unread", "PROJECT.md", "COORDINATOR.md"),
    ("partial-union-covers", "full",
     lambda r: _all(r, skip=("PROJECT.md",)) + [_read(r, "PROJECT.md", 1, 2), _read(r, "PROJECT.md", 3, 2)], "read", "", ""),
    ("partial-gap", "full", lambda r: _all(r, skip=("PROJECT.md",)) + [_read(r, "PROJECT.md", 1, 2)],
     "unread", "PROJECT.md (lines 1-2 of 4)", ""),
    ("limit-1-read", "full", lambda r: _all(r, skip=("PROJECT.md",)) + [_read(r, "PROJECT.md", 1, 1)], "unread", "PROJECT.md", ""),
    ("zero-and-huge-numlines", "full", lambda r: _all(r, skip=("PROJECT.md",))
     + [_read(r, "PROJECT.md", 1, 0), _read(r, "PROJECT.md", 1, 10**9)], "unread", "PROJECT.md", ""),
    ("error-read", "full", lambda r: _all(r, skip=("PROJECT.md",))
     + [json.dumps({"type": "user", "toolUseResult": "Error: file not found"})], "unread", "PROJECT.md", ""),
    ("write-result", "full", lambda r: _all(r, skip=("PROJECT.md",)) + [
        json.dumps({"type": "user", "toolUseResult": {"type": "create", "file": {"filePath": str(Path(r) / "PROJECT.md")}}})],
     "unread", "PROJECT.md", ""),
    ("sidechain-read", "full", lambda r: _all(r, skip=("PROJECT.md",)) + [_read(r, "PROJECT.md", isSidechain=True)],
     "unread", "PROJECT.md", ""),
    ("worktree-copy", "full", lambda r: _all(r, skip=("PROJECT.md",))
     + [_read(Path(r) / ".claude" / "worktrees" / "w", "PROJECT.md")], "unread", "PROJECT.md", ""),
    ("quoted-toolUseResult-text", "full", lambda r: _all(r, skip=("PROJECT.md",)) + [_quoted(r)],
     "unread", "PROJECT.md", ""),
    ("boundary-text-in-content", "full", lambda r: _all(r) + [MENTION], "read", "", "PROJECT"),
    ("missing-file-is-a-note", "short", lambda r: _all(r, skip=(NAMES[4],)), "read", "cannot judge " + NAMES[4] + " (absent)", ""),
    ("missing-file-keeps-the-others", "short", lambda r: _all(r, skip=(NAMES[4], "PROJECT.md")), "unread", "PROJECT.md",
     "COORDINATOR.md"),
    ("cut-last-line", "full", lambda r: _all(r) + ['{"type":"user","toolUseResult":{"type":"te'], "read", "", ""),
    ("broken-and-nonobject-lines", "full", lambda r: ["not json", "[1,2]", "[" * 200000] + _all(r), "read", "", ""),
    ("big-segment-boundary-found-by-growth", "full", lambda r: [_hook("startup")] + _all(r) + [FILLER] * 700, "read", "", ""),
    ("big-segment-old-reads-before-boundary", "full", lambda r: _all(r) + [COMPACT] + [FILLER] * 700, "unread", "PROJECT.md", ""),
]


@pytest.fixture(scope="module")
def world(tmp_path_factory):
    base = tmp_path_factory.mktemp("rules")
    roots = {}
    for key, drop in (("full", ()), ("short", (NAMES[4],))):
        root = base / key
        for name in NAMES:
            if name not in drop:
                (root / name).parent.mkdir(parents=True, exist_ok=True)
                (root / name).write_text("a\nb\nc\nd\n", encoding="utf-8")
        roots[key] = root
    return base, roots


@pytest.mark.parametrize("rid,rootkey,build,verdict,has,hasnt", ROWS, ids=[r[0] for r in ROWS])
def test_read_state_table(world, rid, rootkey, build, verdict, has, hasnt):
    base, roots = world
    root = roots[rootkey]
    transcript = base / (rid + ".jsonl")
    transcript.write_text("\n".join(build(root)) + "\n", encoding="utf-8")
    got, detail = cr.read_state(str(transcript), str(root))
    assert got == verdict, detail
    assert has in detail
    assert not hasnt or hasnt not in detail
    assert detail.isascii()


def test_read_state_cannot_judge_rows(world, monkeypatch):
    base, roots = world
    root = str(roots["full"])
    assert cr.read_state(str(base / "absent.jsonl"), root)[0] == "cannot-judge"      # E6: never unread
    assert cr.read_state(str(base), root)[0] == "cannot-judge"                       # a directory
    assert cr.read_state(str(base / "x.jsonl"), str(base / "nowhere"))[0] == "cannot-judge"   # no rule file at all
    capped = base / "capped.jsonl"
    capped.write_text("\n".join(_all(root) + [FILLER] * 700) + "\n", encoding="utf-8")       # no boundary, file > cap
    monkeypatch.setattr(cr, "READ_SCAN_MAX", 100 * 1024)
    verdict, detail = cr.read_state(str(capped), root)
    assert verdict == "cannot-judge" and "no start within" in detail                  # E7


def test_read_warn_text_and_silences(world):
    base, roots = world
    root = str(roots["full"])
    transcript = base / "warn.jsonl"
    transcript.write_text("\n".join([COMPACT] + _all(root, skip=("PROJECT.md",))) + "\n", encoding="utf-8")
    payload = {"transcript_path": str(transcript), "cwd": root}
    text = cr.read_warn(payload, "commit")
    assert text.startswith("COORDINATOR-READ WARN: ") and "PROJECT.md" in text and "(before this commit)" in text
    assert "\n" not in text and text.isascii() and len(text) <= 400
    assert cr.read_warn(dict(payload, agent_id="a1"), "commit") == ""                # E4: a worker
    assert cr.read_warn({"cwd": root}, "commit") == ""                               # E6a: a probe payload
    assert cr.read_warn({"transcript_path": str(transcript)}, "commit") == ""
    assert cr.read_warn("not a dict", "commit") == ""
    assert "cannot judge" in cr.read_warn(dict(payload, transcript_path=str(base / "no.jsonl")), "dispatch")
    done = base / "done.jsonl"
    done.write_text("\n".join(_all(root)) + "\n", encoding="utf-8")
    assert cr.read_warn(dict(payload, transcript_path=str(done)), "commit") == ""    # a read verdict prints nothing

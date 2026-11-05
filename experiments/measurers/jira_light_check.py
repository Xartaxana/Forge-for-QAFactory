#!/usr/bin/env python3
"""What a ticket file weighs and how much of it is the ticket's own words (spec t-267, keys K2 and K16).

    python jira_light_check.py <story-dir> [--snapshot <path>] [--rest <path>] [--json]

<story-dir> is the story's artifacts folder (`.../artifacts/PROJ-1`). Two files are measured side
by side, read-only:

  snapshot   `work/ticket-snapshot.json` - what S0 hands the roles (today the agent's markdown turned
             into JSON; after t-267 the light projection of the REST read)
  rest       the REST `_snapshot` output of S1 `collect`, `work/sources/SRC-*/<revision>/ticket.json`
             whose `key` is the story's (a copy under `assessment/` is a peek of another ticket, skipped)

Every number is UTF-8 BYTES (`len(text.encode("utf-8"))`); the file size is `os.path.getsize`. The share
is own-words bytes / file bytes, where the own words are title + description + the acceptance criteria
joined by `\\n` + the comment texts. A file that is not there reads "absent", never 0; so does a ticket fact
the file does not carry (a key that is missing, as opposed to an empty one). A count of what the file
itself holds (the custom-field keys) is 0 when the file has no such block.

The module is standalone stdlib: it does not import the package (it must run before the package change
lands, and a measurer that imports the code it measures agrees with it by construction - PROJECT.md p.5).
"""
import argparse
import json
import os
import sys
from pathlib import Path

ABSENT = "absent"

# (label, key of measure(), the counting command the number comes from)
ROWS = (
    ("bytes", "bytes", "os.path.getsize(file)"),
    ("own_words_bytes", "own_words_bytes", "sum len(s.encode('utf-8')): title, description, AC joined by \\n, comment texts"),
    ("share_%", "share_pct", "100 * own_words_bytes / bytes"),
    ("custom_field_keys", "custom_field_keys", "len(file['custom_fields'])"),
    ("custom_field_empty_keys", "custom_field_empty_keys", "keys whose value is None, '', [], {} or blank"),
    ("custom_field_bytes", "custom_field_bytes", "json.dumps(custom_fields, indent=2, sort_keys=True, ensure_ascii=False), utf-8"),
    ("comments", "comments", "len(file['comments'])"),
    ("attachments", "attachments", "len(file['attachments']), else len(file['attachment_names'])"),
    ("parent", "parent", "file['parent']"),
    ("acceptance_criteria", "acceptance_criteria", "len(list), or the non-empty lines of a string"),
)


def u8(text) -> int:
    return len(text.encode("utf-8"))


def text_of(value) -> str:
    """A field's text: a string as it is, None as nothing, anything else (an ADF document) as its JSON."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def is_empty(value) -> bool:
    return value is None or value == "" or value == [] or value == {} or (isinstance(value, str) and not value.strip())


def ac_parts(data: dict):
    """(count, text) of the acceptance criteria; (None, "") when the file does not carry the key."""
    if "acceptance_criteria" not in data:
        return None, ""
    ac = data["acceptance_criteria"]
    if isinstance(ac, list):
        return len(ac), "\n".join(text_of(item) for item in ac)
    text = text_of(ac)
    return sum(1 for line in text.splitlines() if line.strip()), text


def comment_texts(data: dict) -> list:
    out = []
    for comment in data.get("comments") or []:
        out.append(text_of(comment.get("text") if isinstance(comment, dict) else comment))
    return out


def measure(path) -> dict:
    """The numbers of one file. `state` is ok / absent / unreadable; every number of a file that is not
    ok is None (printed "absent"), never 0."""
    out = {"path": str(path) if path else None, "state": "absent"}
    for _, key, _ in ROWS:
        out[key] = None
    if not path or not Path(path).is_file():
        return out
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8-sig"))
        if not isinstance(data, dict):
            raise ValueError("the top level is not an object")
    except (OSError, ValueError) as error:
        out["state"] = "unreadable"
        out["error"] = str(error)
        return out
    out["state"] = "ok"
    size = os.path.getsize(path)
    out["bytes"] = size
    ac_count, ac_text = ac_parts(data)
    out["acceptance_criteria"] = ac_count
    words = u8(text_of(data.get("title"))) + u8(text_of(data.get("description"))) + u8(ac_text) \
        + sum(u8(text) for text in comment_texts(data))
    out["own_words_bytes"] = words
    out["share_pct"] = round(100.0 * words / size, 1) if size else None
    fields = data.get("custom_fields")
    fields = fields if isinstance(fields, dict) else {}
    out["custom_field_keys"] = len(fields)
    out["custom_field_empty_keys"] = sum(1 for value in fields.values() if is_empty(value))
    out["custom_field_bytes"] = u8(json.dumps(fields, indent=2, sort_keys=True, ensure_ascii=False)) if fields else 0
    out["comments"] = len(data["comments"]) if isinstance(data.get("comments"), list) else None
    for key in ("attachments", "attachment_names"):
        if isinstance(data.get(key), list):
            out["attachments"] = len(data[key])
            break
    out["parent"] = data["parent"] if "parent" in data else None
    out["parent_present"] = "parent" in data
    return out


def find_rest(story_dir, key=None) -> list:
    """The REST `_snapshot` files of the story: `work/sources/SRC-*/<revision>/ticket.json` whose `key` is
    the story's. The `assessment/` copies are peeks of OTHER tickets and are not looked at."""
    story_dir = Path(story_dir)
    key = key or story_dir.name
    found = []
    for path in sorted((story_dir / "work" / "sources").glob("*/*/ticket.json")):
        if path.parent.name == "assessment":
            continue
        try:
            if json.loads(path.read_text(encoding="utf-8-sig")).get("key") == key:
                found.append(path)
        except (OSError, ValueError, AttributeError):
            continue
    return found


def cell(m: dict, key: str) -> str:
    if m["state"] == "absent":
        return ABSENT
    if m["state"] == "unreadable":
        return "unreadable"
    value = m[key]
    if key == "parent":
        return str(value) if m.get("parent_present") else ABSENT
    if value is None:
        return ABSENT
    return f"{value:.1f}" if key == "share_pct" else str(value)


def report(story: str, snap: dict, rest: dict, notes=()) -> str:
    lines = [f"## jira_light_check - {story}",
             f"[snapshot] {snap['path'] or '(none)'}  -> {snap['state']}",
             f"[rest]     {rest['path'] or '(none)'}  -> {rest['state']}"]
    lines += [f"note: {note}" for note in notes]
    wide = max(10, *(len(cell(m, key)) for m in (snap, rest) for _, key, _ in ROWS))
    lines.append(f"{'metric':24} | {'snapshot':>{wide}} | {'rest':>{wide}} | carrier (the counting command)")
    for label, key, how in ROWS:
        lines.append(f"{label:24} | {cell(snap, key):>{wide}} | {cell(rest, key):>{wide}} | {how}")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("story_dir", help=".../artifacts/<TICKET>")
    ap.add_argument("--snapshot", help="the snapshot file (default <story-dir>/work/ticket-snapshot.json)")
    ap.add_argument("--rest", help="the REST file (default: the story's own ticket.json under work/sources)")
    ap.add_argument("--json", action="store_true", help="print the same numbers as JSON")
    args = ap.parse_args(sys.argv[1:])
    story_dir = Path(args.story_dir)
    if not story_dir.is_dir():
        print(f"story folder not found: {story_dir} (pass .../artifacts/<TICKET>)")
        return 2
    notes = []
    snap_path = Path(args.snapshot) if args.snapshot else story_dir / "work" / "ticket-snapshot.json"
    if args.rest:
        rest_path = Path(args.rest)
    else:
        found = find_rest(story_dir)
        rest_path = found[-1] if found else None
        if len(found) > 1:
            notes.append(f"{len(found)} REST files carry this key; the last by path is measured: "
                         + ", ".join(str(p) for p in found))
    snap, rest = measure(snap_path), measure(rest_path)
    if args.json:
        print(json.dumps({"story": story_dir.name, "snapshot": snap, "rest": rest,
                          "carriers": {label: how for label, _, how in ROWS}, "notes": notes},
                         indent=2, ensure_ascii=False))
    else:
        print(report(story_dir.name, snap, rest, notes))
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    raise SystemExit(main())

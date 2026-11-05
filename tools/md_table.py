"""md_table.py -- the markdown-table reader as a leaf: stdlib `re` only, no import of anything in tools/ (t-797 F5-2 N1).

Why a leaf: tools/digest_form.py is read by tools/handback_extract.py, which must not break because `piles` does -- `import piles`
pulls six modules (gitcmd, forge_metrics, md_regions, ...). The objects below are the table reader of `piles.py` (`_code_mask`,
`split_pipes`, `split_cells`, `TABLE_RULE_RE`, `walk_table`, `table_after`) and the two line filters of the pile-card readers
(`md_lines_outside_fences`, `_blank_comments`); since node N3 of the same spec `piles.py` IMPORTS them from here -- there is one
copy, and the two modules share the very same objects. This module imports NOTHING from tools/ (a pin in test_digest_form.py):
`piles`, `forge_metrics`, `journal_validator` and `gitcmd` are out.
"""
import re


def _code_mask(s: str) -> list:
    """mask[i] is True where s[i] sits inside a backtick span (a run of n backticks closes at the next run of n)."""
    mask = [False] * len(s)
    i, n = 0, len(s)
    while i < n:
        if s[i] != "`":
            i += 1
            continue
        j = i
        while j < n and s[j] == "`":
            j += 1
        run, k, end = j - i, j, -1
        while k < n:
            if s[k] != "`":
                k += 1
                continue
            m = k
            while m < n and s[m] == "`":
                m += 1
            if m - k == run:
                end = m
                break
            k = m
        if end < 0:
            i = j                      # a lone backtick run is literal text
            continue
        for p in range(i, end):
            mask[p] = True
        i = end
    return mask


def split_pipes(s: str) -> list:
    """Split at a '|' that is not escaped ('\\|') and not inside a backtick span of the same string (P10)."""
    mask = _code_mask(s)
    out, start = [], 0
    for p, ch in enumerate(s):
        if ch == "|" and not mask[p] and not (p > 0 and s[p - 1] == "\\"):
            out.append(s[start:p])
            start = p + 1
    out.append(s[start:])
    return out


def split_cells(line: str) -> list:
    """The cells of a markdown table row, stripped (outer pipes dropped)."""
    parts = split_pipes(line.strip())
    if parts and parts[0] == "":
        parts = parts[1:]
    if parts and parts[-1] == "":
        parts = parts[:-1]
    return [c.strip() for c in parts]


TABLE_RULE_RE = re.compile(r":?-{2,}:?")                 # a cell of a table's `|---|---|` separator row


def walk_table(lines):
    """THE table walker: one boundary rule for every reader of a table -- table_after (cards, nodes), (в)'s `_frozen_lines` and
    the proofs gate of `close`. A table is a run of lines that start with `|` at COLUMN 0; any other line -- blank, comment-only,
    indented, text -- ends it, and the next `|` line starts a new table (its first line is that table's header). Yields
    (kind, cells) for every line, in step with `lines`: ("header", cells) the first line of a run, ("rule", cells) a separator
    row, ("row", cells) any other line of the run, (None, None) a line outside every table."""
    inside = False
    for line in lines:
        if not line.startswith("|"):
            inside = False
            yield None, None
            continue
        cells = split_cells(line)
        if not inside:
            inside, kind = True, "header"
        else:
            kind = "rule" if cells and all(TABLE_RULE_RE.fullmatch(c) for c in cells) else "row"
        yield kind, cells


def table_after(lines, heading: str):
    """The first table under '## <heading>': (header_cells, [(cells, line_no)]) or None. line_no is 1-based."""
    start = next((i + 1 for i, line in enumerate(lines)
                  if line.startswith("## ") and line[3:].strip().lower().startswith(heading.lower())), None)
    if start is None:
        return None
    header, rows = None, []
    for j, (kind, cells) in enumerate(walk_table(lines[start:]), start):
        if kind is None:
            if header is not None:
                break
            if lines[j].startswith("## "):
                return None
        elif kind == "header":
            header = cells
        elif kind == "row":
            rows.append((cells, j + 1))
    return None if header is None else (header, rows)


FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")           # a ``` / ~~~ line: up to 3 spaces, then a run of 3 or more marks


def fence_walk(lines):
    """(index, line, role) for every line. role: "text" outside every ``` / ~~~ block, "open" the line that opens a block (it may
    carry an info string), "close" the line that closes it, "inside" any line between them. CommonMark's closing rule: a line closes
    a block only when it is a run of the SAME character, at least as long as the opener's run, with nothing but whitespace after the
    run -- a mark of the OTHER character, a shorter run and a run with an info string (```sh) are "inside". The one fence reader
    of the repository's own markdown (CLAUDE.md imports, batch files, digests): md_lines_outside_fences and unclosed_fence are
    views of it."""
    fence = None
    for i, line in enumerate(lines):
        role, fence = _fence_step(fence, line)
        yield i, line, role


def _fence_step(fence, line):
    """(role of `line`, the open block after it) -- the one step of the fence grammar; `fence` is (character, run length) of the
    block still open before the line, or None."""
    m = FENCE_RE.match(line)
    if m and fence is None:
        return "open", (m.group(1)[0], len(m.group(1)))
    if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= fence[1] and not line[m.end():].strip():
        return "close", None
    return ("text" if fence is None else "inside"), fence


def md_lines_outside_fences(lines):
    """(index, line) of the lines not inside a ``` / ~~~ block."""
    for i, line, role in fence_walk(lines):
        if role == "text":
            yield i, line


def unclosed_fence(lines):
    """The index of the line that opens a ``` / ~~~ block nothing closes, or None when every block is closed."""
    opened = None
    for i, _line, role in fence_walk(lines):
        if role == "open":
            opened = i
        elif role == "close":
            opened = None
    return opened


def _blank_line(line: str, in_comment: bool):
    """-> (the line with its comment parts removed, whether a comment is still open at its end, the column of the `<!--` that opens
    the open one or None). A `<!--` closes at the next `-->`; `<!-->` closes nothing."""
    out, pos, column = "", 0, None
    while pos < len(line):
        if in_comment:
            end = line.find("-->", pos)
            if end < 0:
                break
            pos, in_comment, column = end + 3, False, None
        else:
            start = line.find("<!--", pos)
            if start < 0:
                out, pos = out + line[pos:], len(line)
                break
            out, pos, in_comment, column = out + line[pos:start], start + 4, True, start
    return out, in_comment, column


def _blank_comments(lines: list):
    """-> (the lines with every `<!-- … -->` removed and the line count kept, the index of a `<!--` that never closes or None).
    Only a comment hides a line: what stands between two comments on one line is kept. The comment and the fence are read in ONE
    walk and the FIRST OPENER WINS: a `<!--` inside an open ``` / ~~~ block is code (no comment starts there), a ``` / ~~~ mark
    inside a comment is commented out (no block starts there). A comment that never closes leaves its opener and every line after
    it as they are."""
    blanked, fence, in_comment, opened = [], None, False, None
    for i, line in enumerate(lines):
        if fence is not None or (not in_comment and FENCE_RE.match(line)):  # inside a block, or a mark at the line start opens before any comment
            text, still, column = line, False, None
        else:
            text, still, column = _blank_line(line, in_comment)
            if column is not None:
                opened = (i, text, column)
        in_comment = still
        blanked.append(text)
        if not in_comment:
            _, fence = _fence_step(fence, text)
    if not in_comment:
        return blanked, None
    i, prefix, column = opened
    return blanked[:i] + [prefix + lines[i][column:]] + list(lines[i + 1:]), i

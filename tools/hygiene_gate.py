"""hygiene_gate.py -- PreToolUse hook for command hygiene on the Bash and PowerShell tools: it refuses exactly four behaviours (moving the shell's working directory, writing the content of a git working-tree file by a literal target past Edit/Write, writing the journal, discarding dirty working-tree changes) and lets every other form pass silently.

DELIVERY CHANNEL (verified against the installed harness): the hook answers on stdout, exit 0, as
`{"hookSpecificOutput": {"hookEventName": "PreToolUse", "additionalContext": "...", "permissionDecision": "deny",
"permissionDecisionReason": "..."}}`. `permissionDecision` appears ONLY on a refusal (never "allow": that would
auto-approve a command the operator's own prompt should see); `additionalContext` always carries the refusal reasons too,
so a refusal degrades to a visible text if the deny channel were inert.

THE FOUR REFUSALS (spec docs/tasks/specs/fg-context-and-hygiene.md section 4; each text names what is wrong, what is
expected and a door the refused party can use -- FR-1, FR-2, P15):
  cd        the session shell's working directory is never moved: `cd`, `chdir`, `pushd`, `popd`, `Set-Location`, `sl`,
            `Push-Location`, `Pop-Location` at a statement start, `eval "cd x"`, `[IO.Directory]::SetCurrentDirectory`,
            `[Environment]::CurrentDirectory =`. Legal: a bare `cd <this checkout's root>` (the way back), a verb inside a
            subshell when the tool's capability row says the subshell scopes the directory (Bash), a verb inside a quoted
            child-shell argument.
  mutation  a file of a git working tree never gets its CONTENT written by a redirect, tee / Tee-Object / Out-File /
            Set-Content / Add-Content, a .NET file write, an in-place editor (sed -i, perl -i, awk -i inplace, ruby -i) or
            an interpreter payload, when the target is a LITERAL path. File-level rm / mv / cp / mkdir pass (in every
            syntax). Null sinks, non-literal targets and targets outside every working tree pass.
  journal   a write (the same M1-M3 forms) whose literal target is a journal file (`logs/journal/*.jsonl` or
            `logs/routing-log.jsonl`, under any directory prefix, either slash); refused wherever the file lies. Any other
            `.jsonl` is judged only by the general tree check. Reading a journal is never refused.
  rollback  `git checkout/restore/reset --hard/clean -f/switch --discard-changes/stash [push]` whose scope has changes
            `git status` shows, measured in the repository the command ADDRESSES (`git -C` composed left to right).

NAMED RESIDUALS (a data row each in PAYLOAD_INTERPRETERS, `payload_classifier: None`): the payload of node, ruby, perl,
pwsh/powershell, bash/sh/zsh/dash/ksh and cmd is not read; only python is classified.

INVARIANT ABOVE ALL: a read or a calculation is never refused (`>` inside `(( ))`, `$(( ))`, `[[ ]]` is not a redirect),
and no refusal is issued on a target the gate could not resolve. A refusal needs a certain form AND a resolved literal target (or a measured dirty status); everything uncertain
passes. The one exception to silence is a single short WARN for a python payload the gate cannot resolve (a non-literal
path or mode, an unresolved `.write`, exec/eval/subprocess, a parse failure, a payload over PYC_PAYLOAD_LIMIT).

WHERE EACH SIGNAL IS COMPUTED: `_collect_signals(command)` is PURE (no subprocess, no filesystem, no clock) because
permission_audit.classify_hygiene replays every historical command through it; it returns FORMS only (cd hits, literal
write targets, the journal flag, the rollback shape, the payload classes). Everything that needs the filesystem or git
(the working tree of a target, `git status`, statting a checkout argument) runs only in `decide()`.

Fail-open: a non-Bash/PowerShell tool, empty or malformed stdin, a non-dict payload or a missing command pass silently;
an exception while classifying a real command passes too, but VISIBLY (MSG_FAIL_OPEN_TEMPLATE); a rollback that cannot be
measured passes with the marker `Command hygiene: rollback not checked: <reason>`. Every check is linear in the command:
masks are plain regex substitutions or one pass over the lines, a statement is split once, a payload over
PYC_PAYLOAD_LIMIT is never parsed, and past MAX_HEREDOC_OPENERS heredoc-bearing statements yield no write targets.

Reading stdin on a deadline: main() reads the harness JSON through a bounded background-thread read (a local copy per
hook, like tools/session_context.py's); past the deadline the read degrades to "no payload" (silent pass, exit 0).
`OSLLM_STDIN_TIMEOUT` overrides the default; the `__main__` guard escalates to `os._exit()` after a timeout.
"""

import ast
import json
import os
import re
import sys
import threading
from pathlib import Path
from typing import NamedTuple

try:
    import gitcmd
except Exception:  # a copy of this file alone in a folder (permission_audit's CLI) carries no gitcmd
    gitcmd = None

# --- texts (P15: what is wrong, what is expected, the door; each <= 350 characters) --------------------------
WARN_PREFIX = "Command hygiene (WARN, does not block): "
DENY_PREFIX = "Command hygiene: "

MSG_CD_BASH = (
    "the shell's working directory must not move: the hooks find tools/ from it. "
    "Use git -C <dir>, python -B <absolute path>, a tool's --repo/--root, or a ( cd <dir> && ... ) subshell."
)
MSG_CD_POWERSHELL = (
    "the shell's working directory must not move: the hooks find tools/ from it. "
    "Use git -C <dir>, python -B <absolute path>, a tool's --repo/--root, or a child shell: "
    "powershell -NoProfile -Command \"Set-Location <dir>; <cmd>\"."
)
MSG_MUTATION = (
    "{target} is a file of a git working tree and this command writes its content past the Edit/Write hooks. "
    "Use Edit/Write (or a named committed script). Scratch output: write it outside the tree, or put the code in "
    "a script under the scratchpad (python -B <path>). A reading role: Edit/Write your handoff file."
)
MSG_JOURNAL_BLOCK = (
    "the journal is written only through Edit/Write at the file's tail (journal_echo checks the line). "
    "Reading it with grep, cat or tail is fine."
)
MSG_ROLLBACK = (
    "{n} path(s) under {dir} have uncommitted changes that may be another session's, and this command would discard "
    "them. Your own edit: undo it with Edit/Write. A byte copy you took: restore from it. Changes that are not yours: "
    "leave them and tell the Lead."
)
MSG_WARN_PAYLOAD = (
    "this python payload may write a file the gate cannot resolve; if it writes inside a repository, use Edit/Write."
)
MSG_ROLLBACK_NOT_CHECKED = "rollback not checked: {reason}"
MSG_FAIL_OPEN_TEMPLATE = "hygiene_gate: internal classifier error ({exc_type}), hygiene was NOT checked"

# --- data rows (AR-1: variety is data, never a list in logic) ----------------------------------------------
# Read by capability, never by the tool's name in logic; an unknown tool takes the PowerShell row (the conservative
# capability: no subshell scopes the directory).
# Keys: `subshell_scopes_cwd` (a `( )` group keeps its own directory), `dq_escape` (the escape character inside a
# double-quoted string: a backslash is an escape in Bash and a path character in PowerShell, where the backtick escapes),
# `arith_regions` (`(( ))`, `$(( ))`, `[[ ]]` hold comparisons, never redirects), `assign_prefix` (`$x = cmd` starts a
# statement). A doubled quote inside a PowerShell string reads as two adjacent strings: same mask, same statements.
SHELL_CAPABILITIES = {
    "Bash": {"subshell_scopes_cwd": True, "cd_door": MSG_CD_BASH, "dq_escape": "\\", "arith_regions": True,
             "assign_prefix": False},
    "PowerShell": {"subshell_scopes_cwd": False, "cd_door": MSG_CD_POWERSHELL, "dq_escape": "`",
                   "arith_regions": False, "assign_prefix": True},
}
SHOWN_TARGET_CHARS = 40     # the target / directory a refusal shows is clipped to its tail, so a text stays <= 350
# A root-relative path starting with a row is not "in a working tree" for the content-write refusal (F-C3).
HYGIENE_IGNORE_ROWS = ("ci-out/",)
# Statement starts: after these words the next word is a command again (t-098 F2).
_START_WORD_RE = re.compile(r"\s*(?:then|do|else|elif|builtin|command|time|!)(?=\s|$)", re.IGNORECASE)
_CD_VERBS = frozenset({"cd", "chdir", "pushd", "popd", "set-location", "sl", "push-location", "pop-location"})
_CD_RETURN_VERBS = frozenset({"cd", "chdir", "set-location", "sl"})
_NULL_SINKS = frozenset({"/dev/null", "nul", "nul:", "$null"})
_PS_ASSIGN_RE = re.compile(r"\s*\$[A-Za-z_][A-Za-z0-9_:]*\s*=(?!=)\s*")
# Commands that write the file(s) they are given -> which operands are targets (read by _path_targets): `tee` writes
# EVERY operand, the cmdlets and their aliases take one path.
_TEE_LIKE = {"tee": "all", "tee-object": "first", "out-file": "first", "set-content": "first", "add-content": "first",
             "sc": "first", "ac": "first"}
_PS_PATH_PARAMS = frozenset({"-filepath", "-path", "-literalpath", "-pspath"})
_PS_VALUE_PARAMS = frozenset({"-value", "-encoding", "-width", "-stream", "-filter", "-include", "-exclude",
                              "-inputobject", "-variable"})
# Interpreters with an inline payload; `payload_classifier: none` = no classifier exists for it (P31: the difference is
# data, not a branch by name). Only "python" is classified.
_PYTHON_NAME = r"python[0-9.]*|py"      # one spelling, read by the row below and by the advisory _PY_HEAD
PAYLOAD_INTERPRETERS = (
    {"name": re.compile(rf"^(?:{_PYTHON_NAME})$"), "payload_classifier": "python", "payload_flags": ("-c",)},
    {"name": re.compile(r"^(?:bash|sh|zsh|dash|ksh)$"), "payload_classifier": None, "payload_flags": ("-c",)},
    {"name": re.compile(r"^cmd$"), "payload_classifier": None, "payload_flags": ("/c", "/k")},
    {"name": re.compile(r"^(?:node|nodejs)$"), "payload_classifier": None, "payload_flags": ("-e", "--eval", "-p")},
    {"name": re.compile(r"^(?:ruby|perl)$"), "payload_classifier": None, "payload_flags": ("-e",)},
    {"name": re.compile(r"^(?:pwsh|powershell)$"), "payload_classifier": None, "payload_flags": ("-c", "-command")},
)
_PATH_CTORS = frozenset({"Path", "pathlib.Path"})

# A cap on repeated heredoc openers: past it, heredoc-bearing statements yield no write targets (a pathological input
# never widens a refusal).
MAX_HEREDOC_OPENERS = 64
# One payload over this many characters is never parsed: it is UNCERTAIN (a WARN, never a refusal).
PYC_PAYLOAD_LIMIT = 20_000
_MAX_PAYLOADS_PER_COMMAND = 16

_REPO_ROOT_NAME = Path(__file__).resolve().parents[1].name


# --- masks (own: F-C4) -----------------------------------------------------------------------------------
_QUOTE_CHAR_RE = re.compile(r"['\"]")
_BASH_ESC = SHELL_CAPABILITIES["Bash"]["dq_escape"]


class _Rules(NamedTuple):
    """The quote rules of one shell, built from its `dq_escape` capability (the one place the dialects differ)."""
    dq_close: object     # matches the rest of a double-quoted string up to and including its closing quote
    dq: object           # a whole double-quoted string, the body in group 1
    unescape: object
    dynamic_dq: object


def _build_rules(esc: str) -> _Rules:
    e = re.escape(esc)
    # unrolled loops (`a*(?:e.a*)*`): linear on success and on failure, unlike `(?:a|e.)*`
    body = rf'[^"{e}]*(?:{e}.[^"{e}]*)*'
    dyn = "$" if esc == "`" else "$`"
    return _Rules(re.compile(body + '"', re.DOTALL), re.compile('"(' + body + ')"', re.DOTALL),
                  re.compile(rf'{e}(["{e}$`' + ("'" if esc == "`" else "") + '])'), re.compile(rf'(?<!{e})[{re.escape(dyn)}]'))


_RULES = {row["dq_escape"]: _build_rules(row["dq_escape"]) for row in SHELL_CAPABILITIES.values()}
_HEREDOC_OPEN_RE = re.compile(r"<<(?!<)(-?)[ \t]*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\2")
_COMMENT_RE = re.compile(r"(?m)(?:^|(?<=[\s;&|(]))#[^\n]*")
_SEP_RE = re.compile(r"[;&|\n(){}]")
# Kept for the advisory payload classifier (permission_audit's measurement), not read by the gate itself.
COMMIT_HEREDOC_RE = re.compile(
    r"(<<-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\2)([^\n]*)(\n.*?^\3\s*$)",
    re.DOTALL | re.MULTILINE,
)


def _mask_quoted_segments(text: str, esc: str = _BASH_ESC) -> str:
    """Blanks single/double-quoted segments (quoted text is data by construction); length is kept. An unclosed quote
    is left unmasked. LINEAR: a quote that has no closer means no later quote of its kind has one either (the closers
    are the same characters), so the first failure retires that quote kind instead of rescanning to the end again."""
    if "'" not in text and '"' not in text:
        return text
    rules = _RULES[esc]
    out, last, pos, dead = [], 0, 0, set()
    while True:
        m = _QUOTE_CHAR_RE.search(text, pos)
        if m is None:
            break
        i, q = m.start(), m.group(0)
        if q in dead:
            pos = i + 1
            continue
        if q == "'":
            j = text.find("'", i + 1)
            end = -1 if j == -1 else j + 1
        else:
            c = rules.dq_close.match(text, i + 1)
            end = -1 if c is None else c.end()
        if end == -1:
            dead.add(q)
            pos = i + 1
            continue
        out.append(text[last:i])
        out.append(" " * (end - i))
        last = pos = end
    out.append(text[last:])
    return "".join(out)


def _mask_heredoc_bodies(text: str) -> str:
    """Advisory-classifier mask (regex form): blanks every heredoc BODY, keeping the opener line."""
    return COMMIT_HEREDOC_RE.sub(lambda m: m.group(1) + m.group(4) + " " * len(m.group(5)), text)


def _scan_heredocs(text: str):
    """One linear pass over the lines: -> (masked, bodies). `masked` is `text` with every heredoc body and terminator
    line blanked (length and newlines kept); `bodies` = [(opener position, quoted delimiter?, body text)]. An
    unterminated heredoc is masked to the end (bash reads it to the end too)."""
    if "<<" not in text:
        return text, []
    lines = text.split("\n")
    out, bodies, pending = [], [], []
    pos = 0
    for line in lines:
        if pending:
            entry = pending[0]
            check = line.strip() if entry["dash"] else line.rstrip("\r ")
            if check == entry["delim"]:
                pending.pop(0)
                bodies.append((entry["pos"], entry["quoted"], "\n".join(entry["buf"])))
            else:
                entry["buf"].append(line)
            out.append(" " * len(line))
        else:
            for m in _HEREDOC_OPEN_RE.finditer(line):
                pending.append({"dash": bool(m.group(1)), "quoted": bool(m.group(2)), "delim": m.group(3),
                                "pos": pos + m.start(), "buf": []})
            out.append(line)
        pos += len(line) + 1
    for entry in pending:
        bodies.append((entry["pos"], entry["quoted"], "\n".join(entry["buf"])))
    return "\n".join(out), bodies


def _blank_comments(raw: str, masked: str):
    """A `#` at a word start (outside quotes) opens a comment to the end of the line: blank it in both texts."""
    if "#" not in masked:
        return raw, masked
    spans = [m.span() for m in _COMMENT_RE.finditer(masked)]
    if not spans:
        return raw, masked
    r, q, last = [], [], 0
    for a, b in spans:
        r.append(raw[last:a]); q.append(masked[last:a])
        r.append(" " * (b - a)); q.append(" " * (b - a))
        last = b
    r.append(raw[last:]); q.append(masked[last:])
    return "".join(r), "".join(q)


class _Stmt(NamedTuple):
    start: int
    end: int
    sub: bool
    depth: int = 0      # how many `(` / `$(` groups enclose the statement


def _neutralize_regions(raw: str, masked: str):
    """Bash arithmetic and test regions -- `(( ))`, `$(( ))`, `for (( ))`, `[[ ]]` -- hold comparisons: a `<` or `>` inside
    one is never a redirect, so each is blanked (in both texts, length kept). A real redirect after the closing bracket
    is untouched. One stack pass for the parentheses and one forward `find` per `[[`: linear."""
    spans = []
    if "((" in masked:
        stack, match = [], {}
        for m in re.finditer(r"[()]", masked):
            p = m.start()
            if masked[p] == "(":
                stack.append(p)
            elif stack:
                match[stack.pop()] = p
        spans += [(p, q) for p, q in match.items() if masked[p + 1:p + 2] == "(" and match.get(p + 1) == q - 1]
    i = 0
    while True:
        p = masked.find("[[", i)
        if p == -1:
            break
        if p > 0 and masked[p - 1] not in " \t\r\n;&|(!{":
            i = p + 2
            continue
        q = masked.find("]]", p + 2)
        if q == -1:
            break
        spans.append((p, q))
        i = q + 2
    if not spans:
        return raw, masked
    table = str.maketrans("<>", "  ")
    covered, r, q_out, last = 0, [], [], 0
    for p, q in sorted(spans):
        a = max(p, covered)
        if q <= a:
            continue
        r.append(raw[last:a]); q_out.append(masked[last:a])
        r.append(raw[a:q].translate(table)); q_out.append(masked[a:q].translate(table))
        last = covered = q
    r.append(raw[last:]); q_out.append(masked[last:])
    return "".join(r), "".join(q_out)


def _split_statements(masked: str) -> list:
    """Statement spans of the quote- and heredoc-masked text, split on ; & | newline and on ( ) { } (a subshell or a
    group opens a new statement; `(`/`$(` also mark the region as a subshell). `2>&1`, `>&`, `&>`, `>|` stay whole,
    and a brace counts only when it stands alone (`{ cd x; }`, not `${x}`, `@{}` or `{}`)."""
    out, start, depth, n = [], 0, 0, len(masked)
    for m in _SEP_RE.finditer(masked):
        i = m.start()
        ch = masked[i]
        if ch == "&":
            if (i > 0 and masked[i - 1] in "<>") or (i + 1 < n and masked[i + 1] == ">"):
                continue
        elif ch == "|":
            if i > 0 and masked[i - 1] == ">":
                continue
        elif ch in "{}":
            prev = masked[i - 1] if i > 0 else " "
            nxt = masked[i + 1] if i + 1 < n else " "
            if not (prev in " \t\r\n;&|(" and nxt in " \t\r\n"):
                continue
        out.append(_Stmt(start, i, depth > 0, depth))
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        start = i + 1
    out.append(_Stmt(start, n, depth > 0, depth))
    return out


# --- tokenizer ------------------------------------------------------------------------------------------
_DYNAMIC_RUN_RE = re.compile(r'[$`]|%\w+%')
_GLOB_RUN_RE = re.compile(r'[*?]')
_RUN_RE = re.compile(r"[^\s'\"<>]+")
_FD_WORD_RE = re.compile(r"\d+|\*")
_ASSIGN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*=")


class _Word(NamedTuple):
    text: str        # quotes removed
    inner: str       # quoted segments verbatim (for a payload parsed as written)
    dynamic: bool    # holds a variable / substitution: the real text is unknown
    glob: bool       # holds an unquoted wildcard
    quoted: bool

    @property
    def literal(self) -> bool:
        return not self.dynamic and not self.glob


class _Redir(NamedTuple):
    op: str
    fd: str
    target: object   # _Word or None


def _read_word(s: str, i: int, rules: _Rules):
    n = len(s)
    text, inner, dynamic, glob, quoted = [], [], False, False, False
    start = i
    while i < n:
        c = s[i]
        if c in " \t\r\n" or c in "<>":
            break
        if c == "&" and i + 1 < n and s[i + 1] == ">":
            break
        if c == "'":
            j = s.find("'", i + 1)
            seg = s[i + 1:] if j == -1 else s[i + 1:j]
            i = n if j == -1 else j + 1
            text.append(seg); inner.append(seg); quoted = True
        elif c == '"':
            m = rules.dq.match(s, i)
            if m:
                seg, i = m.group(1), m.end()
            else:
                seg, i = s[i + 1:], n
            text.append(rules.unescape.sub(r"\1", seg)); inner.append(seg); quoted = True
            if rules.dynamic_dq.search(seg):
                dynamic = True
        else:
            m = _RUN_RE.match(s, i)
            if m is None:       # a lone `&`
                run, i = c, i + 1
            else:
                run, i = m.group(0), m.end()
            text.append(run); inner.append(run)
            if _DYNAMIC_RUN_RE.search(run):
                dynamic = True
            if _GLOB_RUN_RE.search(run):
                glob = True
    if i == start:
        i += 1
    return _Word("".join(text), "".join(inner), dynamic, glob, quoted), i


def _tokenize(s: str, rules: _Rules) -> list:
    """Words and redirects of one statement (quote-aware; outside quotes a backslash is a path character, not an
    escape; inside double quotes the shell's own escape character applies)."""
    toks, i, n = [], 0, len(s)
    while i < n:
        c = s[i]
        if c in " \t\r\n":
            i += 1
            continue
        fd = ""
        if not (c in "<>" or (c == "&" and i + 1 < n and s[i + 1] == ">")):
            word, j = _read_word(s, i, rules)
            if j < n and s[j] in "<>" and not word.quoted and _FD_WORD_RE.fullmatch(word.text):
                fd, i = word.text, j
            else:
                toks.append(word)
                i = j
                continue
        for op in ("&>>", "&>", ">>", ">|", ">&", ">", "<<<", "<<-", "<<", "<&", "<"):
            if s.startswith(op, i):
                break
        i += len(op)
        while i < n and s[i] in " \t":
            i += 1
        target = None
        if i < n and s[i] not in "\r\n":
            target, i = _read_word(s, i, rules)
        toks.append(_Redir(op, fd, target))
    return toks


# --- class extractors ------------------------------------------------------------------------------------
def _cmd_name(text: str) -> str:
    name = re.split(r"[\\/]", text)[-1].lower()
    return name[:-4] if name.endswith(".exe") else name


_JOURNAL_RE = re.compile(r"(?:^|/)logs/(?:journal/[^/]+|routing-log)\.jsonl$")


def _is_journal_target(target: str) -> bool:
    norm = target.replace("\\", "/").lower()
    return bool(_JOURNAL_RE.search(norm))


def _is_absolute(path: str) -> bool:
    return bool(re.match(r"^(?:[A-Za-z]:[\\/]|[\\/]|~)", path))


def _bound_value(a):
    """`-Path:value` (a PowerShell parameter bound with a colon) -> (lowercased name, a word holding the value) | None."""
    if not a.text.startswith("-") or ":" not in a.text:
        return None
    name, value = a.text.split(":", 1)
    return name.lower(), a._replace(text=value)


def _first_path_arg(args: list):
    for i, a in enumerate(args):
        bound = _bound_value(a)
        if bound is not None and bound[0] in _PS_PATH_PARAMS and bound[1].text:
            return bound[1]
        if a.text.lower() in _PS_PATH_PARAMS and i + 1 < len(args):
            return args[i + 1]
    skip = False
    for a in args:
        if skip:
            skip = False
            continue
        if a.text.startswith("-") and len(a.text) > 1:
            skip = a.text.lower() in _PS_VALUE_PARAMS and ":" not in a.text
            continue
        return a
    return None


def _all_path_args(args: list) -> list:
    """Every operand that is not an option (`tee a b` writes both; a lone `-` is no file)."""
    return [a for a in args if a.text and not a.text.startswith("-")]


def _path_targets(cmd: str, args: list) -> list:
    """The words a tee-like command writes (data row `_TEE_LIKE`): [] when it has no file operand."""
    mode = _TEE_LIKE.get(cmd)
    if mode == "all":
        return _all_path_args(args)
    first = _first_path_arg(args) if mode else None
    return [first] if first is not None else []


def _sed_targets(args: list) -> list:
    inplace = has_script = False
    pos, i = [], 0
    while i < len(args):
        t = args[i].text
        if t == "--":
            pos.extend(args[i + 1:])
            break
        if t.startswith("--"):
            if t == "--in-place" or t.startswith("--in-place="):
                inplace = True
            elif t in ("--expression", "--file"):
                has_script = True
                i += 1
            elif t.startswith(("--expression=", "--file=")):
                has_script = True
        elif t.startswith("-") and len(t) > 1:
            body = t[1:]
            for j, ch in enumerate(body):
                if ch == "i":
                    inplace = True
                    break
                if ch in "efl":
                    has_script = has_script or ch in "ef"
                    if j == len(body) - 1:
                        i += 1
                    break
        else:
            pos.append(args[i])
        i += 1
    if not inplace:
        return []
    return pos if has_script else pos[1:]


def _perl_targets(args: list) -> list:
    """perl and ruby: `-i[ext]` among the short flags, `-e script` consumed."""
    inplace = has_e = False
    pos, i = [], 0
    while i < len(args):
        t = args[i].text
        if t == "--":
            pos.extend(args[i + 1:])
            break
        if t.startswith("-") and len(t) > 1 and not t.startswith("--"):
            body = t[1:]
            for j, ch in enumerate(body):
                if ch == "i":
                    inplace = True
                    break
                if ch in "eE":
                    has_e = True
                    if j == len(body) - 1:
                        i += 1
                    break
                if ch in "IMmdDxCFl0":
                    break
        elif not t.startswith("--"):
            pos.append(args[i])
        i += 1
    if not inplace:
        return []
    return pos if has_e else pos[1:]


def _awk_targets(args: list) -> list:
    texts = [a.text for a in args]
    if not any(texts[k] == "-i" and k + 1 < len(texts) and texts[k + 1] == "inplace" for k in range(len(texts))):
        return []
    pos, has_f, i = [], False, 0
    while i < len(args):
        t = texts[i]
        if t in ("-i", "-v", "-F"):
            i += 2
            continue
        if t == "-f":
            has_f = True
            i += 2
            continue
        if not t.startswith("-"):
            pos.append(args[i])
        i += 1
    return pos if has_f else pos[1:]


# Data row: in-place editor -> the reader of its target arguments (an argument it cannot place yields no target).
INPLACE_EDITORS = {"sed": _sed_targets, "perl": _perl_targets, "ruby": _perl_targets, "awk": _awk_targets,
                   "gawk": _awk_targets}

_NET_WRITE_RE = re.compile(
    r"\[(?:System\.)?IO\.File\]::(?:WriteAllText|WriteAllLines|WriteAllBytes|AppendAllText|AppendAllLines)\(",
    re.IGNORECASE)
_NET_CD_RE = re.compile(
    r"\[(?:System\.)?IO\.Directory\]::SetCurrentDirectory\(|\[(?:System\.)?Environment\]::CurrentDirectory\s*=",
    re.IGNORECASE)


def _net_target(seg: str, end: int):
    """The literal first argument of a .NET file write (the masked text blanked it; `seg` is the unmasked statement)."""
    while end < len(seg) and seg[end] in " \t":
        end += 1
    if end >= len(seg) or seg[end] not in "'\"":
        return None
    j = seg.find(seg[end], end + 1)
    if j == -1:
        return None
    text = seg[end + 1:j]
    return None if re.search(r"[$`]", text) and seg[end] == '"' else text


# --- rollback shapes (data row: git subcommand -> reader of the shape) --------------------------------------
def _split_args(rest: list, value_opts=()):
    opts, pos, dd, i = [], [], None, 0
    while i < len(rest):
        t = rest[i].text
        if dd is not None:
            dd.append(rest[i])
        elif t == "--":
            dd = []
        elif t.startswith("-") and len(t) > 1:
            opts.append(t)
            if t in value_opts and i + 1 < len(rest):
                i += 1
        else:
            pos.append(rest[i])
        i += 1
    return opts, pos, dd


def _has_short(opts: list, letter: str) -> bool:
    return any(o.startswith("-") and not o.startswith("--") and letter in o[1:] for o in opts)


def _shape(name, words, view="tracked", **extra):
    scope = [w.text for w in words]
    d = {"shape": name, "scope": scope, "view": view, "check_arg": None,
         "dynamic": any(w.dynamic for w in words)}
    d.update(extra)
    return d


def _shape_checkout(rest):
    opts, pos, dd = _split_args(rest, value_opts=("--conflict",))
    if (any(_has_short(opts, ch) for ch in "bBp")
            or any(o in ("--orphan", "--detach", "--patch") or o.startswith("--orphan=") for o in opts)):
        return None
    if any(o.startswith("--pathspec-from-file") for o in opts):
        return _shape("checkout --pathspec-from-file", [], unresolvable="--pathspec-from-file")
    if dd is not None:
        return _shape("checkout -- paths", dd) if dd else None
    if "--force" in opts or _has_short(opts, "f"):
        return _shape("checkout -f", [])
    if len(pos) >= 2:
        return _shape("checkout rev paths", pos[1:])
    if len(pos) == 1:
        if pos[0].text == ".":
            return _shape("checkout .", pos)
        return _shape("checkout one-arg", pos, check_arg=pos[0].text)
    return None


def _shape_switch(rest):
    opts, _pos, _dd = _split_args(rest)
    if "--discard-changes" in opts or "--force" in opts or _has_short(opts, "f"):
        return _shape("switch --discard-changes", [])
    return None


def _shape_restore(rest):
    opts, pos, dd = _split_args(rest, value_opts=("-s", "--source"))
    if any(o.startswith("--pathspec-from-file") for o in opts):
        return _shape("restore --pathspec-from-file", [], unresolvable="--pathspec-from-file")
    staged = "--staged" in opts or _has_short(opts, "S")
    worktree = "--worktree" in opts or _has_short(opts, "W")
    if (staged and not worktree) or "--patch" in opts or _has_short(opts, "p"):
        return None
    paths = pos + (dd or [])
    return _shape("restore", paths) if paths else None


def _shape_reset(rest):
    opts, _pos, _dd = _split_args(rest)
    return _shape("reset --hard", []) if "--hard" in opts else None


def _shape_clean(rest):
    opts, pos, dd = _split_args(rest, value_opts=("-e", "--exclude"))
    force = "--force" in opts or _has_short(opts, "f")
    dry = "--dry-run" in opts or _has_short(opts, "n")
    if dry or not force or _has_short(opts, "i") or "--interactive" in opts:
        return None
    return _shape("clean", pos + (dd or []), view="clean", clean_d=_has_short(opts, "d"),
                  clean_x=_has_short(opts, "x"), clean_X=_has_short(opts, "X"))


def _shape_stash(rest):
    opts, pos, dd = _split_args(rest, value_opts=("-m", "--message"))
    sub = pos[0].text if pos else None
    if sub not in (None, "push", "save"):
        return None
    words = list(dd or []) + (pos[1:] if sub == "push" else [])
    inc_all = "--all" in opts or _has_short(opts, "a")
    inc_untracked = inc_all or "--include-untracked" in opts or _has_short(opts, "u")
    return _shape("stash", words, view="stash" if inc_untracked else "tracked", stash_ignored=inc_all)


ROLLBACK_SHAPES = {"checkout": _shape_checkout, "switch": _shape_switch, "restore": _shape_restore,
                   "reset": _shape_reset, "clean": _shape_clean, "stash": _shape_stash}
_GIT_FLAG_GLOBALS = frozenset({"--no-pager", "--literal-pathspecs", "--no-optional-locks", "--paginate", "-P",
                               "--no-replace-objects", "--glob-pathspecs", "--noglob-pathspecs"})


def _rollback_form(args: list):
    texts = [a.text for a in args]
    c_chain, unresolvable, i = [], None, 0
    while i < len(texts):
        t = texts[i]
        if t == "-C" and i + 1 < len(texts):
            if args[i + 1].dynamic:
                unresolvable = "non-literal -C directory"
            c_chain.append(texts[i + 1])
            i += 2
        elif t == "-c" and i + 1 < len(texts):
            i += 2
        elif t in _GIT_FLAG_GLOBALS:
            i += 1
        elif t.startswith(("--git-dir", "--work-tree")):
            unresolvable = "--git-dir/--work-tree"
            i += 1 if "=" in t else 2
        else:
            break
    if i >= len(texts):
        return None
    reader = ROLLBACK_SHAPES.get(texts[i].lower())
    form = reader(args[i + 1:]) if reader else None
    if form is None:
        return None
    form["c_chain"] = c_chain
    form["literal_pathspecs"] = "--literal-pathspecs" in texts[:i]
    form["unresolvable"] = form.get("unresolvable") or unresolvable or (
        "non-literal path" if form["dynamic"] else None)
    return form


# --- python payload, gate grade (t-098 B1, B5) ---------------------------------------------------------
# Gate-grade writes, exactly: (i) open(<literal>, <literal mode with w/a/x/+>) / io.open, free or in `with`;
# (ii) Path(<literal>).write_text / write_bytes / .open(<mode with w/a/x/+>); (iii) json.dump / pickle.dump whose file is
# an inline call of form (i). A `.write` on such a call belongs to it. STDIO and FILE-LEVEL calls are silent; every
# other advisory-M/O call is UNCERTAIN. The advisory lists further below are NOT re-labelled: they lean toward M on
# purpose and stay the audit's instrument (`pyc_payload`).
_GATE_WRITE_FORMS = ("open", "io.open", "Path().write_text", "Path().write_bytes", "Path().open", "json.dump", "pickle.dump")
_FILE_LEVEL_ATTRS = frozenset({"unlink", "rename", "replace", "mkdir", "touch", "rmdir"})
_METHOD_MODE_RE = re.compile(r"[rwxabtU+]+")


def _literal_str(node):
    return node.value if isinstance(node, ast.Constant) and isinstance(node.value, str) else None


def _is_stdio(node, alias_map) -> bool:
    d = _resolve_dotted(_dotted_call_name(node), alias_map)
    if d is None:
        return False
    if d.endswith(".buffer"):
        d = d[:-7]
    return d in _STDIO_DOTTED


def _path_ctor_literal(recv, alias_map):
    """The literal of `Path('x')` (through the alias map), or None."""
    if not isinstance(recv, ast.Call) or len(recv.args) != 1 or recv.keywords:
        return None
    if _resolve_dotted(_dotted_call_name(recv.func), alias_map) not in _PATH_CTORS:
        return None
    return _literal_str(recv.args[0])


def _gate_open(node, alias_map):
    """For an `open`-shaped call: ("w", literal path | None) for a certain write mode, ("r", None) for a read or a
    non-mode, ("U", None) when the mode or the call cannot be placed."""
    func = node.func
    dotted = _resolve_dotted(_dotted_call_name(func), alias_map)
    free = dotted in _FREE_OPEN_DOTTED_NAMES
    if any(kw.arg is None for kw in node.keywords):
        return "U", None
    mode_index = 1 if free else 0
    mode_node = node.args[mode_index] if len(node.args) > mode_index else next(
        (kw.value for kw in node.keywords if kw.arg == "mode"), None)
    if mode_node is None:
        return "r", None
    mode = _literal_str(mode_node)
    if mode is None:
        return "U", None
    if not free and not _METHOD_MODE_RE.fullmatch(mode):
        return "r", None          # `Image.open('a.png')`, `os.open(p, flags)`: not a mode
    if not any(ch in mode for ch in "wax+"):
        return "r", None
    if free:
        path_node = node.args[0] if node.args else next((kw.value for kw in node.keywords if kw.arg == "file"), None)
        return "w", _literal_str(path_node) if path_node is not None else None
    if isinstance(func, ast.Attribute):
        return "w", _path_ctor_literal(func.value, alias_map)
    return "U", None


def _is_inline_open(node, alias_map) -> bool:
    """An `open(...)`-shaped call (free, `io.open` or a method `.open`)."""
    if not isinstance(node, ast.Call):
        return False
    return (getattr(node.func, "attr", None) == "open"
            or _resolve_dotted(_dotted_call_name(node.func), alias_map) in _FREE_OPEN_DOTTED_NAMES)


def _gate_call(node, alias_map):
    """None (silent) | "U" (uncertain) | a literal path (a certain write)."""
    func = node.func
    attr = func.attr if isinstance(func, ast.Attribute) else (func.id if isinstance(func, ast.Name) else None)
    dotted = _resolve_dotted(_dotted_call_name(func), alias_map)
    root = dotted.split(".", 1)[0] if dotted else None
    if dotted in _OPAQUE_BARE_NAMES or root in _OPAQUE_ROOT_MODULES:
        return "U"
    if root == "os" and attr and (attr in ("system", "popen") or attr.startswith(("exec", "spawn"))):
        return "U"
    if dotted == "fileinput.input" and any(kw.arg == "inplace" for kw in node.keywords):
        return "U"
    if attr == "open" or dotted in _FREE_OPEN_DOTTED_NAMES:     # an alias (`from io import open as o`) resolves
        kind, path = _gate_open(node, alias_map)
        if kind == "r":
            return None
        return path if (kind == "w" and path is not None) else "U"
    if attr in ("write_text", "write_bytes"):
        path = _path_ctor_literal(func.value, alias_map) if isinstance(func, ast.Attribute) else None
        return path if path is not None else "U"
    if dotted in ("json.dump", "pickle.dump", "csv.writer"):
        index = 0 if dotted == "csv.writer" else 1
        target = node.args[index] if len(node.args) > index else next(
            (kw.value for kw in node.keywords if kw.arg in ("fp", "file", "csvfile")), None)
        if target is not None and (_is_stdio(target, alias_map) or _is_inline_open(target, alias_map)):
            return None           # stdout, or the inner open call yields the write
        return "U"
    if dotted == "os.truncate":
        return "U"
    if dotted in _OS_MUTATING_QUALIFIED or root == "shutil" or attr in _FILE_LEVEL_ATTRS:
        return None
    if attr in _PANDAS_LIKE_METHOD_NAMES:
        return "U"
    if attr in _WRITE_METHOD_NAMES:
        recv = func.value if isinstance(func, ast.Attribute) else None
        if recv is not None and (_is_inline_open(recv, alias_map) or _is_stdio(recv, alias_map)):
            return None           # belongs to the open call that yields the write, or goes to stdout
        return "U"
    if dotted == "print" or attr == "print":
        file_kw = next((kw for kw in node.keywords if kw.arg == "file"), None)
        if file_kw is not None and not _is_stdio(file_kw.value, alias_map):
            return "U"
    return None


def _gate_writes(tree):
    """(literal write targets, uncertain) of one parsed payload."""
    alias_map = _build_import_alias_map(tree)
    targets, uncertain = [], False
    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign, ast.NamedExpr)):
            value = node.value
            if isinstance(value, (ast.Name, ast.Attribute)) and _is_known_mutating_or_opaque_name(
                    _resolve_dotted(_dotted_call_name(value), alias_map)):
                uncertain = True
            continue
        if not isinstance(node, ast.Call):
            continue
        verdict = _gate_call(node, alias_map)
        if verdict == "U":
            uncertain = True
        elif verdict is not None:
            targets.append(verdict)
    return targets, uncertain


def _payload_verdict(texts: list, dynamic: bool):
    """(literal write targets, uncertain) of one inline python payload given as candidate readings (as the shell
    delivers it, then as written)."""
    if dynamic or any(len(t) > PYC_PAYLOAD_LIMIT for t in texts):
        return [], True
    if not any(t.strip() for t in texts):
        return [], False
    for text in texts:
        try:
            tree = ast.parse(text)
        except (SyntaxError, ValueError, RecursionError, MemoryError):
            continue
        try:
            return _gate_writes(tree)
        except Exception:
            return [], True
    return [], True


def _python_payload(args: list, row):
    """(payload word, True) for `-c <payload>`; (None, True) for `-` (stdin); (None, False) when neither."""
    i = 0
    while i < len(args):
        a = args[i].text
        if a in row["payload_flags"]:
            return (args[i + 1], True) if i + 1 < len(args) else (None, False)
        if a == "-":
            return None, True
        if a in ("-X", "-W"):
            i += 2
            continue
        if a.startswith("-"):
            i += 1
            continue
        break
    return None, False


# =========================================================================
# Advisory payload classification ("M" mutates / "P" proven pure / "O" opaque /
# "U" not classified). NOT read by the gate: `permission_audit` measures with
# it (`pyc_payload`). The lists lean toward M on purpose.
# =========================================================================
_PY_HEAD = (rf"\b(?:{_PYTHON_NAME})(?:\.exe)?"
            r"(?:\s+(?:-[XW]\s+\S+|-(?![XWc]\b)[A-Za-z0-9.]+))*")
PY_DASH_C_RE = re.compile(_PY_HEAD + r"\s+-c\b", re.IGNORECASE)
PY_HEREDOC_RE = re.compile(_PY_HEAD + r"\s+-\s*<<", re.IGNORECASE)
_PY_DASH_C_ARG_RE = re.compile(
    _PY_HEAD + r"\s+-c\s+"
    r"(?:"
    r'"(?P<dq>(?:[^"\\]|\\.)*)"'
    r"|'(?P<sq>[^']*)'"
    r"|(?P<bare>\S+)"
    r")",
    re.IGNORECASE | re.DOTALL,
)
_PY_HEREDOC_EXTRACT_RE = re.compile(
    _PY_HEAD + r"\s+-\s*<<-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1[^\n]*"
    r"\n(?P<body>.*?)^\2\s*$",
    re.IGNORECASE | re.DOTALL | re.MULTILINE,
)

_PATH_MUTATING_METHOD_NAMES = {
    "write_text", "write_bytes", "unlink", "rename", "replace",
    "mkdir", "touch", "rmdir",
}
_OS_MUTATING_QUALIFIED = {
    "os.remove", "os.unlink", "os.rename", "os.replace", "os.rmdir",
    "os.mkdir", "os.makedirs", "os.truncate", "os.chmod",
}
_DUMP_QUALIFIED = {"json.dump", "pickle.dump", "csv.writer"}
_PANDAS_LIKE_METHOD_NAMES = {"to_csv", "to_excel"}
_WRITE_METHOD_NAMES = {"write", "writelines"}
_STDIO_DOTTED = {"sys.stdout", "sys.stderr"}
_OPAQUE_BARE_NAMES = {
    "exec", "eval", "compile", "__import__",
    "getattr", "setattr", "globals", "locals", "vars",
}
_OPAQUE_ROOT_MODULES = {
    "importlib", "subprocess", "ctypes", "marshal", "socket",
    "urllib", "requests", "multiprocessing", "pty", "builtins",
}
# The free `open(path, mode)`/`io.open` carries its mode at index 1; the METHOD form `X.open(mode)` at index 0.
_FREE_OPEN_DOTTED_NAMES = {"open", "io.open"}


def _dotted_call_name(node):
    """A dotted name from an ast.Attribute/ast.Name chain; None when the base is not a plain chain."""
    parts = []
    cur = node
    while isinstance(cur, ast.Attribute):
        parts.append(cur.attr)
        cur = cur.value
    if isinstance(cur, ast.Name):
        parts.append(cur.id)
        return ".".join(reversed(parts))
    return None


def _classify_open_call(node, dotted):
    """ONE `open(...)`/`X.open(...)` call -> "M" (literal write mode), "O" (mode hidden or non-literal), None."""
    if any(kw.arg is None for kw in node.keywords):
        return "O"
    mode_index = 1 if dotted in _FREE_OPEN_DOTTED_NAMES else 0
    mode_node = node.args[mode_index] if len(node.args) > mode_index else next(
        (kw.value for kw in node.keywords if kw.arg == "mode"), None
    )
    if mode_node is None:
        return None
    if isinstance(mode_node, ast.Constant) and isinstance(mode_node.value, str):
        return "M" if any(ch in mode_node.value for ch in "wax+") else None
    return "O"


def _build_import_alias_map(tree) -> dict:
    """"local name -> canonical path" from every import in the tree (a relative import is skipped)."""
    alias_map = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.asname:
                    alias_map[alias.asname] = alias.name
                else:
                    top = alias.name.split(".")[0]
                    alias_map[top] = top
        elif isinstance(node, ast.ImportFrom):
            if not node.module:
                continue
            for alias in node.names:
                alias_map[alias.asname or alias.name] = f"{node.module}.{alias.name}"
    return alias_map


def _resolve_dotted(raw_dotted, alias_map):
    """Substitutes the ROOT of a dotted chain through the alias map."""
    if raw_dotted is None:
        return None
    parts = raw_dotted.split(".")
    if parts[0] in alias_map:
        parts[0] = alias_map[parts[0]]
        return ".".join(parts)
    return raw_dotted


def _is_known_mutating_or_opaque_name(dotted) -> bool:
    """True when a resolved name is `open` or any M/O name: a reassigned callable makes a later call untrackable."""
    if dotted is None:
        return False
    if dotted == "open":
        return True
    if dotted in _OPAQUE_BARE_NAMES or dotted in _OS_MUTATING_QUALIFIED or dotted in _DUMP_QUALIFIED:
        return True
    root = dotted.split(".", 1)[0]
    attr_last = dotted.rsplit(".", 1)[-1]
    if root in _OPAQUE_ROOT_MODULES or root == "shutil":
        return True
    if root == "os" and (attr_last in ("system", "popen") or attr_last.startswith("exec") or attr_last.startswith("spawn")):
        return True
    if attr_last in _PATH_MUTATING_METHOD_NAMES or attr_last in _PANDAS_LIKE_METHOD_NAMES or attr_last in _WRITE_METHOD_NAMES:
        return True
    return False


def _classify_single_payload(text: str) -> str:
    """ONE extracted payload -> "M"/"P"/"O" by `ast.parse` and a tree walk (M > O > P); a parse failure, an empty text
    or a text over PYC_PAYLOAD_LIMIT -> "O". An unresolvable base of `.write` is NOT excluded -> "M"."""
    if len(text) > PYC_PAYLOAD_LIMIT:
        return "O"
    if not text.strip():
        return "O"
    try:
        tree = ast.parse(text)
        alias_map = _build_import_alias_map(tree)
        has_m = False
        has_o = False
        for node in ast.walk(tree):
            if isinstance(node, (ast.Assign, ast.AnnAssign, ast.NamedExpr)):
                value = node.value
                if isinstance(value, (ast.Name, ast.Attribute)):
                    resolved_value = _resolve_dotted(_dotted_call_name(value), alias_map)
                    if _is_known_mutating_or_opaque_name(resolved_value):
                        has_o = True
                continue
            if not isinstance(node, ast.Call):
                continue

            if isinstance(node.func, ast.Attribute):
                attr = node.func.attr
            elif isinstance(node.func, ast.Name):
                attr = node.func.id
            else:
                attr = None
            dotted = _resolve_dotted(_dotted_call_name(node.func), alias_map)
            root = dotted.split(".", 1)[0] if dotted else None

            if dotted in _OPAQUE_BARE_NAMES or root in _OPAQUE_ROOT_MODULES:
                has_o = True
                continue
            if root == "os" and attr in ("system", "popen"):
                has_o = True
                continue
            if root == "os" and attr and (attr.startswith("exec") or attr.startswith("spawn")):
                has_o = True
                continue
            if dotted == "fileinput.input" and any(kw.arg == "inplace" for kw in node.keywords):
                has_o = True
                continue

            if attr == "open":
                verdict = _classify_open_call(node, dotted)
                if verdict == "M":
                    has_m = True
                elif verdict == "O":
                    has_o = True
                continue
            if attr in _PATH_MUTATING_METHOD_NAMES:
                has_m = True
                continue
            if root == "os" and dotted in _OS_MUTATING_QUALIFIED:
                has_m = True
                continue
            if root == "shutil":
                has_m = True
                continue
            if dotted in _DUMP_QUALIFIED:
                has_m = True
                continue
            if attr in _PANDAS_LIKE_METHOD_NAMES:
                has_m = True
                continue
            if attr in _WRITE_METHOD_NAMES:
                base_dotted = (
                    _resolve_dotted(_dotted_call_name(node.func.value), alias_map)
                    if isinstance(node.func, ast.Attribute) else None
                )
                if base_dotted not in _STDIO_DOTTED:
                    has_m = True
                continue
            if dotted == "print" or attr == "print":
                file_kw = next((kw for kw in node.keywords if kw.arg == "file"), None)
                if file_kw is not None and _resolve_dotted(
                    _dotted_call_name(file_kw.value), alias_map
                ) not in _STDIO_DOTTED:
                    has_m = True
                continue
    except Exception:
        return "O"
    if has_m:
        return "M"
    if has_o:
        return "O"
    return "P"


def _is_python_dash_c_certain(command: str) -> bool:
    """True when the python `-c`/`-` token survives the heredoc-body and quote masks. Past MAX_HEREDOC_OPENERS: False."""
    if command.count("<<") > MAX_HEREDOC_OPENERS:
        return False
    masked = _mask_quoted_segments(_mask_heredoc_bodies(command))
    return bool(PY_DASH_C_RE.search(masked) or PY_HEREDOC_RE.search(masked))


def _classify_pyc_payload(command: str, certain: bool | None = None) -> str:
    """"M"|"P"|"O"|"U": "U" when the match is not certain; any exception -> "O"."""
    if certain is None:
        certain = _is_python_dash_c_certain(command)
    if not certain:
        return "U"
    try:
        payloads = []
        for k, m in enumerate(_PY_DASH_C_ARG_RE.finditer(command)):
            if k >= _MAX_PAYLOADS_PER_COMMAND:
                return "O"
            payloads.append(m.group("dq") if m.group("dq") is not None
                            else m.group("sq") if m.group("sq") is not None else m.group("bare"))
        for m in _PY_HEREDOC_EXTRACT_RE.finditer(command):
            payloads.append(m.group("body"))
        if not payloads:
            return "O"
        classes = [_classify_single_payload(p) for p in payloads]
    except Exception:
        return "O"
    if "M" in classes:
        return "M"
    if "O" in classes:
        return "O"
    return "P"


# =========================================================================
# The pure signal walk
# =========================================================================
_CD_OPTIONS = frozenset({"-p", "-l", "-e", "-@", "-path", "-literalpath", "-pspath", "--"})


def _compose(prefix: tuple, target: str) -> str:
    """`target` seen from the directory the literal `cd` chain `prefix` leads to, as a string (no filesystem): an absolute
    component restarts the path, a relative one is appended; the caller resolves the result against the payload cwd."""
    path = ""
    for part in (*prefix, target):
        path = part if (not path or _is_absolute(part)) else path.rstrip("\\/") + "/" + part
    return path


class _Walker:
    """One pass over the statements of a command: fills the signal dict. Pure (no subprocess, filesystem or clock).

    `scopes` is a stack of directory scopes, one per open `( )` / `$( )` group (the entry for depth d is what the group's
    statements run in): a tuple of the literal `cd` targets seen so far in the group (`()` = the payload cwd), or None
    = unresolved (a non-literal cd, `cd -`, `popd`, a shell whose groups do not scope the directory). A group inherits
    its parent's scope when it opens and loses its own when it closes, so a `cd` inside `( ... )` never leaks out."""

    def __init__(self, command: str, tool_name: str):
        self.cap = SHELL_CAPABILITIES.get(tool_name, SHELL_CAPABILITIES["PowerShell"])   # decide() passes only known names
        self.rules = _RULES[self.cap["dq_escape"]]
        self.sig = {"cd": [], "write_targets": [], "journal": False, "rollback_forms": [],
                    "pyc_payload": "U", "payload_uncertain": False}
        self.over_cap = command.count("<<") > MAX_HEREDOC_OPENERS
        self.raw, self.bodies = _scan_heredocs(command)
        masked = _mask_quoted_segments(self.raw, self.cap["dq_escape"])
        self.raw, masked = _blank_comments(self.raw, masked)
        if self.cap["arith_regions"]:
            self.raw, masked = _neutralize_regions(self.raw, masked)
        self.masked = masked
        self.scopes = [()]
        self.last_content = -1
        self.payloads_seen = 0
        self.start_res = [_START_WORD_RE] + ([_PS_ASSIGN_RE] if self.cap["assign_prefix"] else [])

    # --- the statement loop
    def run(self) -> dict:
        for idx, st in enumerate(_split_statements(self.masked)):
            self._enter_scope(st.depth)
            a = self._content_start(st)
            seg = self.raw[a:st.end]
            if not seg.strip():
                continue
            self.last_content = idx
            toks = _tokenize(seg, self.rules)
            words = [t for t in toks if isinstance(t, _Word)]
            k = 0
            while k < len(words) and _ASSIGN_RE.match(words[k].text) and not words[k].text.startswith("-"):
                k += 1
            cmdwords = words[k:]
            cmd = _cmd_name(cmdwords[0].text) if cmdwords else ""
            args = cmdwords[1:]
            self._cd_class(cmd, args, st, idx)
            if not (self.over_cap and "<<" in self.masked[a:st.end]):
                self._write_classes(cmd, args, [t for t in toks if isinstance(t, _Redir)], st)
                if cmd == "git":
                    self._rollback(args)
        self._dotnet()
        self._bare_return()
        return self.sig

    def _enter_scope(self, depth: int) -> None:
        del self.scopes[depth + 1:]
        while len(self.scopes) < depth + 1:
            self.scopes.append(self.scopes[-1])

    def _content_start(self, st) -> int:
        a = st.start
        moved = True
        while moved:
            moved = False
            for rx in self.start_res:
                m = rx.match(self.masked, a, st.end)
                if m and m.end() > a:
                    a, moved = m.end(), True
        return a

    # --- cd class
    def _cd_class(self, cmd: str, args: list, st, idx: int) -> None:
        hit = None
        if cmd in _CD_VERBS:
            tgt = [w for w in args if w.text.lower() not in ("-path", "-literalpath", "-pspath", "--")]
            hit = {"verb": cmd, "target": tgt[0].text if tgt else "", "in_subshell": st.sub,
                   "bare_return": False, "_n": len(tgt), "_idx": idx}
            self._move_scope(cmd, args)
        elif cmd == "eval" and args:
            first = " ".join(w.text for w in args).split(None, 1)
            if first and first[0].lower() in _CD_VERBS:
                hit = {"verb": "eval", "target": "", "in_subshell": st.sub, "bare_return": False, "_n": 2, "_idx": idx}
                self._move_scope("eval", args)
        if hit is not None:
            self.sig["cd"].append(hit)

    def _move_scope(self, cmd: str, args: list) -> None:
        """A directory move changes the scope of the group it stands in (and of the groups it opens afterwards)."""
        if not self.cap["subshell_scopes_cwd"]:
            self.scopes[:] = [None] * len(self.scopes)      # the move is refused anyway; nothing after it resolves
            return
        words = [w for w in args if w.text.lower() not in _CD_OPTIONS]
        target = words[0] if len(words) == 1 and cmd in ("cd", "chdir", "set-location", "sl", "pushd", "push-location") \
            else None
        if target is None or not target.literal or target.text in ("-", ""):
            self.scopes[-1] = None
        elif _is_absolute(target.text):
            self.scopes[-1] = (target.text,)
        elif self.scopes[-1] is not None:
            self.scopes[-1] = (*self.scopes[-1], target.text)

    # --- write classes
    def _add_target(self, form: str, target: str) -> bool:
        """Records a literal write target as seen from the payload cwd; False (nothing recorded) when the directory the
        statement runs in is unresolved and the target is relative."""
        prefix = self.scopes[-1]
        if prefix is None and not _is_absolute(target):
            return False
        full = _compose(prefix or (), target)
        if _is_journal_target(full):
            self.sig["journal"] = True
        self.sig["write_targets"].append((form, full))
        return True

    def _write_classes(self, cmd: str, args: list, redirs: list, st) -> None:
        for r in redirs:                                    # M1: redirects
            path = self._redirect_path(r)
            if path:
                self._add_target("redirect", path)
        for w in _path_targets(cmd, args):                  # M1: tee-likes
            text = w.text.strip("\r ")
            if w.literal and text and text.lower() not in _NULL_SINKS:
                self._add_target(cmd, text)
        reader = INPLACE_EDITORS.get(cmd)                   # M2: in-place editors
        if reader is not None:
            for w in reader(args):
                if w.literal and w.text.strip("\r "):
                    self._add_target(cmd, w.text.strip("\r "))
        row = next((r for r in PAYLOAD_INTERPRETERS if cmd and r["name"].match(cmd)), None)
        if row is not None and row["payload_classifier"] == "python":      # M3: interpreter payloads
            self._payload(args, row, st)

    @staticmethod
    def _redirect_path(r):
        if r.op not in (">", ">>", ">|", "&>", "&>>", ">&") or r.fd == "0" or r.target is None:
            return None
        t = r.target
        if r.op == ">&" and re.fullmatch(r"\d+-?|-", t.text):
            return None
        path = t.text.strip("\r ")
        if not path or path.lower() in _NULL_SINKS or path.startswith("/dev/") or not t.literal:
            return None
        return path

    def _payload(self, args: list, row, st) -> None:
        word, is_payload = _python_payload(args, row)
        texts, dynamic, found = None, False, False
        if word is not None:
            texts = [word.text] + ([word.inner] if word.inner != word.text else [])
            dynamic, found = word.dynamic, True
        elif is_payload:
            mine = next(((q, b) for p, q, b in self.bodies if st.start <= p < st.end), None)
            if mine is not None:
                texts, found = [mine[1]], True
                dynamic = not mine[0] and bool(re.search(r"[$`]", mine[1]))   # an unquoted delimiter expands
        if not found:
            return
        self.payloads_seen += 1
        if self.payloads_seen > _MAX_PAYLOADS_PER_COMMAND:
            self.sig["payload_uncertain"] = True
            return
        targets, uncertain = _payload_verdict(texts, dynamic)
        self.sig["payload_uncertain"] = self.sig["payload_uncertain"] or uncertain
        for t in targets:
            t = t.strip("\r ")
            if t and not self._add_target("payload", t):
                self.sig["payload_uncertain"] = True

    # --- rollback forms: EVERY shape in the command is kept, each with the directory it runs in
    def _rollback(self, args: list) -> None:
        form = _rollback_form(args)
        if form is None:
            return
        prefix = self.scopes[-1]
        if prefix is None:
            form["unresolvable"] = form.get("unresolvable") or "the directory was changed by a cd the gate cannot follow"
        else:
            form["c_chain"] = [*prefix, *form["c_chain"]]
        self.sig["rollback_forms"].append(form)

    # --- after the loop
    def _dotnet(self) -> None:
        """.NET calls hold a `(`, which the statement split cuts at: they are read from the whole masked text."""
        for _nm in _NET_CD_RE.finditer(self.masked):
            self.sig["cd"].append({"verb": "SetCurrentDirectory", "target": "", "in_subshell": False,
                                   "bare_return": False})
        if self.over_cap:
            return
        moved = any(not h["bare_return"] for h in self.sig["cd"])
        for nm in _NET_WRITE_RE.finditer(self.masked):
            t = (_net_target(self.raw, nm.end()) or "").strip("\r ")
            if t and not (moved and not _is_absolute(t)):
                if _is_journal_target(t):
                    self.sig["journal"] = True
                self.sig["write_targets"].append(("dotnet", t))

    def _bare_return(self) -> None:
        """A bare `cd <this root>` as the LAST statement is the way back and stays legal."""
        for h in self.sig["cd"]:
            if (h["verb"] in _CD_RETURN_VERBS and h["_idx"] == self.last_content and not h["in_subshell"]
                    and h["_n"] == 1
                    and re.split(r"[\\/]", h["target"].rstrip("\\/"))[-1].lower() == _REPO_ROOT_NAME.lower()):
                h["bare_return"] = True
        for h in self.sig["cd"]:
            h.pop("_n", None)
            h.pop("_idx", None)


def _collect_signals(command: str, tool_name: str = "Bash") -> dict:
    """FORMS only, pure (no subprocess, no filesystem, no clock): permission_audit replays history through it.
    `tool_name` picks the shell's capability row (quote rules, groups, arithmetic); Bash by default.

      - `cd`              list of {verb, target, bare_return, in_subshell}: every directory move found
      - `write_targets`   list of (form, literal target seen from the payload cwd): redirects, tee-likes, .NET writes,
                          in-place editors, python payload writes; non-literal targets and relative targets of an
                          unresolved directory are not here
      - `journal`         a resolved write target is a journal file
      - `rollback_forms`  list of dicts (shape, scope, view, c_chain, unresolvable ...), one per git rollback shape
      - `pyc_payload`     advisory "M"/"P"/"O"/"U", kept for measurement
      - `payload_uncertain` a python payload the gate cannot resolve"""
    sig = _Walker(command, tool_name).run()
    try:
        sig["pyc_payload"] = _classify_pyc_payload(command)
    except Exception:
        sig["pyc_payload"] = "O"
    return sig


# =========================================================================
# decide(): the only place that touches the filesystem or git
# =========================================================================
_MSYS_PATH_RE = re.compile(r"^/([A-Za-z])/(.*)$")


def _absolute_target(target: str, cwd: str) -> str:
    p = os.path.expanduser(target)
    if os.name == "nt":
        m = _MSYS_PATH_RE.match(p.replace("\\", "/"))
        if m:
            p = f"{m.group(1).upper()}:/{m.group(2)}"
    if not os.path.isabs(p):
        p = os.path.join(cwd, p)
    return os.path.normpath(p)


def _tree_root(path: str):
    """The nearest ancestor of `path` holding `.git` (file or directory), by path walk; None when there is none."""
    d = os.path.dirname(path)
    while True:
        if os.path.lexists(os.path.join(d, ".git")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def _tree_display(target: str, cwd: str):
    """The root-relative path of `target` when it lies in a git working tree (not under `.git/`, not an ignore row);
    None otherwise. A target that cannot be resolved is not in a tree."""
    try:
        path = _absolute_target(target, cwd)
        root = _tree_root(path)
        if root is None:
            return None
        rel = os.path.relpath(path, root).replace("\\", "/")
    except (ValueError, OSError):
        return None
    low = rel.lower()
    if low == ".git" or low.startswith(".git/") or any(low.startswith(row) for row in HYGIENE_IGNORE_ROWS):
        return None
    return rel


def _measure_rollback(form: dict, cwd: str):
    """("refuse", n, dir) | ("pass",) | ("marker", reason). Never raises."""
    try:
        if form.get("unresolvable"):
            return ("marker", "unresolvable: " + form["unresolvable"])
        if os.environ.get("GIT_DIR") or os.environ.get("GIT_WORK_TREE"):
            return ("marker", "GIT_DIR or GIT_WORK_TREE is set in the hook environment")
        run = getattr(gitcmd, "git", None)
        if run is None:
            return ("marker", "gitcmd is not importable")
        directory = cwd
        for c in form["c_chain"]:
            directory = _absolute_target(c, directory)      # the one resolver (MSYS paths, ~, absolute restarts)
        if not os.path.isdir(directory):
            return ("marker", f"addressed directory absent: {directory}")
        scope = list(form["scope"])
        if form["check_arg"] is not None:
            if not os.path.exists(os.path.join(directory, form["check_arg"])):
                return ("pass",)            # a branch switch: git itself refuses to overwrite dirty files
        view = form["view"]
        flags = ["--untracked-files=no"] if view == "tracked" else ["--untracked-files=normal"]
        if view == "clean" and (form.get("clean_x") or form.get("clean_X")) or form.get("stash_ignored"):
            flags.append("--ignored")
        args = (["--literal-pathspecs"] if form.get("literal_pathspecs") else []) + [
            "status", "--porcelain=v1", "-z", *flags]
        if scope:
            args += ["--", *scope]
        rc, out = run(directory, *args, timeout=5)
        if rc != 0:
            return ("marker", f"git status did not run (rc {rc})")
        entries = gitcmd.parse_status_z(out)
        if view == "clean":
            want_untracked = not form.get("clean_X")
            want_ignored = form.get("clean_x") or form.get("clean_X")
            kept = []
            for xy, path in entries:
                if xy == "??" and want_untracked and (form.get("clean_d") or not path.endswith("/")):
                    kept.append((xy, path))
                elif xy == "!!" and want_ignored and (form.get("clean_d") or not path.endswith("/")):
                    kept.append((xy, path))
            entries = kept
        elif not form.get("stash_ignored"):
            entries = [e for e in entries if e[0] != "!!"]
        if entries:
            return ("refuse", len(entries), directory)
        return ("pass",)
    except Exception as exc:  # noqa: BLE001 -- never a refusal from an exception
        return ("marker", f"{type(exc).__name__}: {str(exc)[:80]}")


def _clip(text: str) -> str:
    """The tail of a long path (the informative end), at most SHOWN_TARGET_CHARS characters."""
    return text if len(text) <= SHOWN_TARGET_CHARS else "..." + text[-(SHOWN_TARGET_CHARS - 3):]


def _decide_command(tool_name: str, command: str, payload: dict):
    sig = _collect_signals(command, tool_name)
    cwd = payload.get("cwd")
    if not isinstance(cwd, str) or not cwd:
        cwd = os.getcwd()
    deny, notes, warn = [], [], []
    if sig["journal"]:
        deny.append(MSG_JOURNAL_BLOCK)
        shown = [t for _f, t in sig["write_targets"] if _is_journal_target(t)][:1]
        if shown:
            notes.append("journal target: " + shown[0][:120])
    for form in sig["rollback_forms"]:          # every shape is measured; the first one that hits a dirty tree refuses
        verdict = _measure_rollback(form, cwd)
        if verdict[0] == "refuse":
            deny.append(MSG_ROLLBACK.format(n=verdict[1], dir=_clip(verdict[2])))
            break
        if verdict[0] == "marker":
            note = MSG_ROLLBACK_NOT_CHECKED.format(reason=verdict[1])
            if note not in notes:
                notes.append(note)
    capability = SHELL_CAPABILITIES[tool_name]      # decide() lets only the two rows' tools through
    if any(not h["bare_return"] and not (h["in_subshell"] and capability["subshell_scopes_cwd"]) for h in sig["cd"]):
        deny.append(capability["cd_door"])
    for _form, target in sig["write_targets"]:
        shown = _tree_display(target, cwd)
        if shown is not None:
            deny.append(MSG_MUTATION.format(target=_clip(shown)))
            break
    if sig["payload_uncertain"]:
        warn.append(MSG_WARN_PAYLOAD)
    if deny:
        return 0, {"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": deny[0],
            "additionalContext": DENY_PREFIX + "; ".join(deny + notes + warn),
        }}
    if notes:
        return 0, {"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "additionalContext": DENY_PREFIX + "; ".join(notes)
            + ("; " + "; ".join(warn) if warn else ""),
        }}
    if warn:
        return 0, {"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "additionalContext": WARN_PREFIX + "; ".join(warn),
        }}
    return 0, None


def decide(payload: dict) -> tuple[int, dict | None]:
    """Entry point: a silent pass on empty or malformed input, else the classification. exit_code is ALWAYS 0 (a
    refusal is `permissionDecision: "deny"` on stdout). Any exception while classifying fails open VISIBLY."""
    if not isinstance(payload, dict):
        return 0, None
    tool_name = payload.get("tool_name")
    if tool_name not in ("Bash", "PowerShell"):
        return 0, None
    tool_input = payload.get("tool_input") or {}
    if not isinstance(tool_input, dict):
        return 0, None
    command = tool_input.get("command")
    if not isinstance(command, str) or not command:
        return 0, None
    try:
        return _decide_command(tool_name, command, payload)
    except Exception as exc:  # noqa: BLE001 -- intentionally broad: see module docstring
        return 0, {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "additionalContext": MSG_FAIL_OPEN_TEMPLATE.format(exc_type=type(exc).__name__),
            }
        }


def _reconfigure_stdout_utf8():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


# ---------------------------------------------------------------------------
# stdin-deadline helper: reading stdin to EOF must never hang a PreToolUse
# check (and by extension the tool call it gates) forever on a harness that
# opens the pipe but never actually writes/closes it. A daemon thread does
# the blocking read; the main thread joins on a deadline instead of calling
# sys.stdin.read() directly. On a timeout, the payload degrades to "no
# payload" (silent pass, same as empty/malformed stdin), never a hang or a
# crash. This is a LOCAL copy of the same helper tools/session_context.py
# carries -- by design, not an oversight: each hook stays self-contained.
# ---------------------------------------------------------------------------

_STDIN_DEADLINE_DEFAULT = 10.0
_STDIN_DEADLINE_MAX = 600.0
_STDIN_DEADLINE_ENV = "OSLLM_STDIN_TIMEOUT"


def _stdin_deadline_seconds():
    """Seconds to wait for stdin: env override, else the default. Invalid, non-numeric, <=0, or > _STDIN_DEADLINE_MAX
    all fall back to the default -- there is deliberately NO "0 = wait forever" mode."""
    try:
        value = float(os.environ.get(_STDIN_DEADLINE_ENV, ""))
    except (TypeError, ValueError):
        return _STDIN_DEADLINE_DEFAULT
    if not (0.0 < value <= _STDIN_DEADLINE_MAX):
        return _STDIN_DEADLINE_DEFAULT
    return value


def _read_stdin_bytes_deadline():
    """Returns (bytes, timed_out). Reads stdin to EOF, bounded by the deadline above (a daemon thread does the
    blocking read; `thread.join(timeout)` enforces the deadline, portable to Windows pipes). A TTY returns b""
    immediately. Any read error degrades to b""."""
    stdin = getattr(sys, "stdin", None)
    if stdin is None:
        return b"", False
    try:
        if stdin.isatty():
            return b"", False
    except Exception:
        pass
    stream = getattr(stdin, "buffer", stdin)
    box = {}

    def _reader():
        try:
            box["data"] = stream.read()
        except Exception:
            box["data"] = b""

    thread = threading.Thread(target=_reader, name="stdin-deadline", daemon=True)
    thread.start()
    thread.join(_stdin_deadline_seconds())
    if thread.is_alive():
        return b"", True
    data = box.get("data") or b""
    if not isinstance(data, bytes):
        data = str(data).encode("utf-8", "replace")
    return data, False


_STDIN_DEADLINE_MSG = "stdin deadline exceeded -- fail-open, payload discarded"

# Set when a stdin read actually timed out: the reader thread is left running as a daemon, and a normal interpreter
# shutdown with it blocked in a platform read can crash, so the __main__ path escalates to os._exit().
_STDIN_DEADLINE_STATE = {"hit": False}


def main() -> int:
    _reconfigure_stdout_utf8()
    raw_bytes, timed_out = _read_stdin_bytes_deadline()
    if timed_out:
        _STDIN_DEADLINE_STATE["hit"] = True
        try:
            sys.stderr.write(f"{Path(__file__).name}: {_STDIN_DEADLINE_MSG}\n")
        except Exception:
            pass
        return 0
    raw = raw_bytes.decode("utf-8-sig", errors="replace")   # a UTF-8 BOM is decoded, not a parse failure
    try:
        payload = json.loads(raw)
    except Exception:
        return 0

    exit_code, output = decide(payload)
    if output is not None:
        sys.stdout.write(json.dumps(output, ensure_ascii=False) + "\n")
    return exit_code


if __name__ == "__main__":
    _rc = main()
    if _STDIN_DEADLINE_STATE["hit"]:
        try:
            sys.stdout.flush()
        except Exception:
            pass
        try:
            sys.stderr.flush()
        except Exception:
            pass
        os._exit(_rc)
    sys.exit(_rc)

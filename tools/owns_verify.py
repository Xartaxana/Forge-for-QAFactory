"""owns_verify.py -- deterministic CLI acceptance step: a post-batch
check of paths ACTUALLY touched against the declared owns manifest
(the dispatch-context-manifest rule, CLAUDE.md rule 11) -- layer 2 of
protection against parallel-dispatch collisions (alongside
tools/owns_gate.py, the PreToolUse hook that is layer 1).

INTERFACE:
  python tools/owns_verify.py --owns "<path1;path2;glob3>" \
      [--paths "<t1;t2;...>"] [--paths-file FILE] [--git-diff REF]

 --owns    REQUIRED -- the ownership declaration, tokens separated by
           `;` (`,`/newline are also accepted -- the same shared
           helper split_and_clean_tokens as tools/owns_gate.py uses;
           more tolerant of input shape than the documented interface
           strictly requires, which is harmless).
 --paths   an explicit list of paths actually touched, same token form.
 --paths-file FILE
           a path list, one per line (empty lines skipped).
 --git-diff REF
           paths of CHANGED tracked files (`git diff --name-only REF`)
           MERGED with untracked files (`git ls-files --others
           --exclude-standard`) -- both sources are needed because
           `git diff` alone never sees untracked files (that command
           diffs tracked content, it doesn't enumerate new paths), and
           a NEW file is the single most common product of a writing
           builder dispatch (the owns manifest of CLAUDE.md rule 11)
           -- without the second source this check is systematically
           blind to the main case. The repo root is resolved ONCE via
           `git rev-parse --show-toplevel` (subprocess as a list, no
           shell=True); EVERY path from BOTH git calls (both return
           paths RELATIVE to the repo root) is resolved to an ABSOLUTE
           path (root / rel) BEFORE comparison against --owns -- owns
           declarations carry absolute paths by this kit's convention
           (rule 11), and a relative-vs-absolute comparison would
           never match. Both git calls inherit the caller's cwd
           (command hygiene point 1 already requires running from the
           repo root); a failure of `git rev-parse` (not a git repo)
           is the same call-error exit 2 as a `git diff`/`git
           ls-files` failure.
 Sources --paths/--paths-file/--git-diff are ADDITIVE: when more than
 one is given, all their paths are merged into a single list for the
 check (an own engineering decision -- the spec does not describe
 behavior when several sources are given at once; documented here, not
 silently guessed). No source given (or --paths is an empty
 string/omitted) -- the path list is empty -- a legal case (DoD: "an
 empty --paths on an otherwise valid call -> OWNS OK 0").

CODE SHARED WITH tools/owns_gate.py: normalize_path/paths_overlap/
split_and_clean_tokens are IMPORTED from owns_gate.py here (one
implementation of the check for both). Overlap semantics are the
SAME as owns_gate.py's (lower+`/` normalization, segment-boundary
nesting, fnmatch for globs).

A DIRECT sibling-module import only, not a package-style
`tools.owns_gate` attempt -- this kit's install tree can live nested
inside a larger repository that ALSO carries its own top-level tools/
directory with a differently behaving owns_gate.py (the exact hazard
tools/owns_gate.py's own docstring documents for its dispatch_gate
import); the sys.path insertion below guarantees a sibling `import
owns_gate` resolves to THIS directory's module unambiguously.

OUTPUT:
 - every path from --paths/--paths-file/--git-diff that does not
   overlap ANY token of the --owns declaration -> a line
   "OUT-OF-OWNS: <path>" on stdout; if at least one such path is
   found -> exit 1 (after ALL offending lines are printed, not on the
   first one).
 - all paths are within the declaration (or there are 0 paths) ->
   "OWNS OK: N paths within M declared" (N = number of paths checked,
   M = number of tokens in the owns declaration) and exit 0.
 - CALL ERROR (not a verdict!) -- --owns missing (or an empty string
   -- treated as no declaration at all, an own decision, documented:
   a wholly empty owns is meaningless for a writing dispatch under
   this kit's rule 11) OR a `git diff` failure (nonzero return code,
   or git unavailable at all, e.g. FileNotFoundError) -> a message on
   stderr, exit 2 -- deliberately DISTINCT from the verdict exit 1
   (violation), the same economy the rest of this kit's tools use to
   separate "verdict" from "call failure"."""

import argparse
import sys
from pathlib import Path

_TOOLS_DIR = Path(__file__).resolve().parent
if str(_TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(_TOOLS_DIR))

import streams  # noqa: E402
import gitcmd  # noqa: E402
from owns_gate import paths_overlap, split_and_clean_tokens  # noqa: E402

__all__ = ["verify", "main"]


def _read_paths_file(path_str: str) -> list:
    raw = Path(path_str).read_text(encoding="utf-8", errors="replace")
    return [line.strip() for line in raw.splitlines() if line.strip()]


def _git_repo_root() -> Path:
    """`git rev-parse --show-toplevel` -- the repo root, ONE call per
    --git-diff invocation. A failure (not a git repo, git unavailable)
    is a call error, RAISED as RuntimeError -- caught in main() and
    turned into exit 2 (see the module docstring).

    ENCODING (release-gate v0.8.1 fix): the bytes tools/gitcmd.py returns
    are decoded here as UTF-8 with errors="replace" -- git's stdout is
    always UTF-8, so a non-UTF-8 console locale cannot mojibake a repo
    root path that itself contains non-ASCII bytes. The runner always
    adds `-c core.quotepath=false`; for `rev-parse --show-toplevel`
    (a single directory path, not a path LISTING) it changes nothing."""
    rc, out, err = gitcmd.git(None, "rev-parse", "--show-toplevel", stderr=True)
    if rc != 0:
        raise RuntimeError(
            f"git rev-parse --show-toplevel failed (exit {rc}): "
            f"{err.decode('utf-8', 'replace').strip()}"
        )
    return Path(out.decode("utf-8", "replace").strip())


def _run_git_name_only(args: list) -> list:
    """Runs a git name-LISTING subcommand -- this module's only two
    callers pass `["git", "diff", "--name-only", ref]` and `["git",
    "ls-files", "--others", "--exclude-standard"]` (see
    _git_diff_paths), through the one git runner tools/gitcmd.py:

    ENCODING -- the runner's bytes are decoded as UTF-8 with
    errors="replace", so git's always-UTF-8 output decodes correctly
    regardless of the console's own locale.

    QUOTEPATH -- the runner ALWAYS passes `-c core.quotepath=false`:
    both of this function's callers list tracked/untracked PATHS, and
    git's default (quotepath=true) octal-escapes any non-ASCII path
    byte in that output (e.g. a two-byte UTF-8 sequence renders as
    `"\\320\\277..."`), which never matches a plain-UTF-8 owns
    declaration when compared in `verify()` -- a FALSE OUT-OF-OWNS on
    a perfectly in-owns non-ASCII path. `args[0]` is always `"git"`."""
    rc, out, err = gitcmd.git(None, *args[1:], stderr=True)
    if rc != 0:
        raise RuntimeError(
            f"{' '.join(args)} failed (exit {rc}): {err.decode('utf-8', 'replace').strip()}"
        )
    return [line.strip() for line in out.decode("utf-8", "replace").splitlines() if line.strip()]


def _git_diff_paths(ref: str) -> list:
    """Merges `git diff --name-only REF` (changed tracked files) WITH
    `git ls-files --others --exclude-standard` (untracked files) --
    WHY BOTH SOURCES: see the module docstring, "--git-diff REF". Both
    return paths RELATIVE to the repo root -- each is resolved to an
    ABSOLUTE path (root / rel) before returning, deduplicated in
    order (diff results first, then untracked)."""
    root = _git_repo_root()
    diff_rel = _run_git_name_only(["git", "diff", "--name-only", ref])
    untracked_rel = _run_git_name_only(["git", "ls-files", "--others", "--exclude-standard"])

    seen = []
    for rel in diff_rel + untracked_rel:
        abs_path = str((root / rel).resolve())
        if abs_path not in seen:
            seen.append(abs_path)
    return seen


def _collect_paths(args) -> list:
    paths = []
    if args.paths:
        paths.extend(split_and_clean_tokens(args.paths))
    if args.paths_file:
        paths.extend(_read_paths_file(args.paths_file))
    if args.git_diff:
        paths.extend(_git_diff_paths(args.git_diff))
    return paths


def verify(owns_decl: list, paths: list) -> list:
    """Returns the paths from `paths` that don't overlap any token of
    `owns_decl` (order preserved, following `paths`)."""
    violations = []
    for p in paths:
        if not any(paths_overlap(p, o) for o in owns_decl):
            violations.append(p)
    return violations


def main(argv=None) -> int:
    streams.utf8_stdio()
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--owns")
    parser.add_argument("--paths", default="")
    parser.add_argument("--paths-file")
    parser.add_argument("--git-diff")
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])

    if not args.owns:
        sys.stderr.write("owns_verify: --owns is required\n")
        return 2

    owns_decl = split_and_clean_tokens(args.owns)

    try:
        paths = _collect_paths(args)
    except Exception as exc:
        sys.stderr.write(f"owns_verify: {exc}\n")
        return 2

    violations = verify(owns_decl, paths)
    for v in violations:
        print(f"OUT-OF-OWNS: {v}")

    if violations:
        return 1

    print(f"OWNS OK: {len(paths)} paths within {len(owns_decl)} declared")
    return 0


if __name__ == "__main__":
    sys.exit(main())

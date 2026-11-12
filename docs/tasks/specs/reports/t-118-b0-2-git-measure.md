# t-118 B0-2: git command forms G1-G13 measured in scratch repositories

git version: `git version 2.56.0.windows.2`

Command: `python -B C:\Users\i_mas\AppData\Local\Temp\claude\b3e3188b390a00d9\f92520fc-f552-4e47-9d06-efbc3daae572\scratchpad\b0-2\measure2.py`

## How to read this report

- Task t-118, node B0-2 of `docs/tasks/specs/fg7-8-b-vcs-words.md`. Measurement only: nothing written in the package, the forge tools or the repository except this file. Scratch repositories: `...\scratchpad\b0-2\repos\<name>`, one FRESH repository per sub-case (the script deletes and rebuilds each).
- Every repository carries, beside the listed paths, a dirty factory folder: tracked `qa-factory/x.txt` modified (` M`), untracked `qa-factory/new.txt` (`??`), and a STAGED new `qa-factory/staged.txt` (`A `). "qa untouched" below means all three, plus the staged blob, are byte-equal after the action.
- Repositories use `core.autocrlf=false` (B0's report had CRLF warnings on stderr; here stderr is clean). The commit message in the commit rows is `MSG = "QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]"` (regex characters on purpose); the stash message is `SMSG = "QA Factory story t-118: your uncommitted changes, put aside before the tests"`. `repo_words.message` does not exist yet, so these are stand-in texts.
- The per-sub-case verbatim output (command as run, exit, stdout, stderr, porcelain before/after; `-z` output as Python bytes repr) is in the last section ("Verbatim output of the run"), under the headers named below.
- Run count: see "Runs" at the end.

## Result per spec row (summary of the verbatim log; the log is the evidence)

### Row 1 - G1 `git status --porcelain=v1 -z -uall` (log headers `row 1 | class ...`)

| sub-case | exit | raw `-z` bytes (as run) | note |
|---|---|---|---|
| `??` file | 0 | `...?? u1.txt\x00` | |
| `??` folder, two files | 0 | `?? d2/a.txt\x00?? d2/b.txt\x00` with `-uall`; `?? d2/\x00` without it | `-uall` lists file by file |
| `??` nested git repo | 0 | `?? nested/\x00` (with `-uall` too) | trailing `/`, not expanded |
| ` M` | 0 | ` M m3.txt\x00` | |
| `M ` | 0 | `M  m4.txt\x00` | |
| `MM` | 0 | `MM m5.txt\x00` | |
| ` D` | 0 | ` D del6.txt\x00` | |
| `D ` | 0 | `D  del7.txt\x00` | |
| `A ` | 0 | `A  add8.txt\x00` | |
| ` A` (`add -N`) | 0 | ` A itd10.txt\x00` | |
| `R ` both sides outside | 0 | `R  new9.txt\x00old9.txt\x00` | order is NEW then OLD |
| space | 0 | `?? a b.txt\x00` | unquoted; the plain form quotes it |
| non-ASCII (e-acute, two CJK) | 0 | `?? caf\xc3\xa9.txt\x00`, `?? \xe4\xb8\xad\xe6\x96\x87.txt\x00` | UTF-8 bytes, unquoted; the plain form prints octal escapes in quotes |
| rename, one side under `qa-factory/` | 0 | `R  src/y.txt\x00qa-factory/r.txt\x00` | |
| submodule, moved pointer | 0 | ` M sub12\x00` | |
| NEW submodule (extra, not in spec list) | 0 | `A  .gitmodules\x00` and `A  sub13\x00` | two entries |
| all classes in one tree | 0 | one stream, see the log line | the script's split into person/factory is printed |

### Row 2 - G2 (log headers `row 2 | ...`, `row 2d | ...`)

`git rev-parse --git-path <name>` exits 0 and prints `.git/<name>` (relative to the cwd) for EVERY name whether or not it exists; presence is the `exists` check.

| state | which name exists | porcelain |
|---|---|---|
| clean repo (control) | none | |
| merge stopped on conflict | `MERGE_HEAD` | `UU c.txt` |
| rebase stopped, default backend | `rebase-merge` (directory) | `UU c.txt` |
| rebase `--apply` stopped | `rebase-apply` (directory) | `UU c.txt` |
| cherry-pick stopped | `CHERRY_PICK_HEAD` | `UU c.txt` |
| revert stopped (extra) | `REVERT_HEAD` | `UD c.txt`, `D  qa-factory/x.txt` |
| after a killed commit (git tree killed by `taskkill /F /T` on the pid I started, hook sleeping) | `index.lock` exists (also `.git/next-index-<pid>.lock`); no process left | `read-tree <tree>` with the lock in place: exit 128 `Unable to create '.../.git/index.lock': File exists`; after deleting the lock by hand (scratch only) exit 0 and `MM m5.txt` is back |

### Row 3 - G3 (log header `row 3 | ...`)

| path | `ls-files -s -z -- <path>` stdout |
|---|---|
| `sub12` (submodule) | `160000 a009164c... 0\tsub12\x00` (mode 160000) |
| `m5.txt` (plain file) | `100644 19d9cc85... 0\tm5.txt\x00` |
| unmerged `c.txt` (row 2a) | three entries, stages 1, 2, 3 |
| `del7.txt` (staged delete), `nested` (nested repo), `a b.txt` / `caf<e-acute>.txt` (untracked), `nothere.txt` | empty, exit 0 |

### Row 4 - G4 -> G5 -> (G12, G11, G13) -> G7 + G6, per class (log headers `row 4 | ...`)

Each repo also holds the staged `qa-factory/staged.txt`; "undo" = `git reset --soft <head_before[:12]>` then `git read-tree <tree from G4>`; "equal" = porcelain AND the full index (`ls-files -s -z`) equal the before state, qa state equal, HEAD == head_before.

| class | G5 add | commit exit | commit took exactly the person's paths (G12 set == paths, no `qa-factory/`) | undo equals before |
|---|---|---|---|---|
| `??` file | yes | 0 | yes | yes |
| `??` folder (2 files) | yes | 0 | yes | yes |
| ` M` | yes | 0 | yes | yes |
| `M ` | skipped (Y = ' ') | 0 | yes | yes |
| `MM` | yes | 0 | yes | yes; `git show :m5.txt` = `staged` before and after |
| ` D` | yes | 0 | yes | yes |
| `D ` | skipped | 0 | yes | yes |
| `A ` | skipped | 0 | yes | yes |
| ` A` (intent-to-add) | yes | 0 | yes | **NO**: G4 write-tree succeeds but the tree has no `itd10.txt`; after the undo the entry is `?? itd10.txt` (was ` A`) |
| `R ` both sides | skipped | 0 | yes (`R100 old new`) | yes |
| space | yes | 0 | yes | yes |
| non-ASCII (e-acute + CJK) | yes | 0 | yes | yes |
| submodule ` M sub12` | yes | 0 | yes | yes |
| NEW submodule (`.gitmodules`, `sub13`) | skipped | 0 | yes | yes |
| nested repo `?? nested/` | - | not run: blocker | - | - |
| rename `qa-factory/r.txt -> src/y.txt` | - | not run: blocker (partial-home) | - | - |
| MIXED (all non-blocked classes) | yes (11 paths) | 0 | yes (16 paths) | **NO**, and only because of ` A` (`?? itd10.txt`); every other entry equal |

HEAD^ == head_before and G13 returned the new commit in every committed row. `MM` HEAD content was not re-read here (B0 measured it: the WORKTREE content lands).

### Row 5 - pre-commit hook `exit 1` (log headers `row 5 | ...`)

| tree | add | commit exit / stderr | HEAD | after the failure (before G6) | after `read-tree <tree>` (G6) |
|---|---|---|---|---|---|
| `MM` only | ok | 1 / `hook: refused` | not moved | `M  m5.txt` (the add's effect stays) | `MM m5.txt`; `git show :m5.txt` = `staged` before and after; porcelain and full index equal before |
| MIXED | ok | 1 / `hook: refused` | not moved | everything staged | equal before EXCEPT ` A` -> `??` (as row 4) |

### Row 6 - hooks that change files (log headers `row 6a/6b/6c`)

| hook | commit exit | porcelain after the commit | what the commit took | undo (G7+G6) |
|---|---|---|---|---|
| 6a appends to `m3.txt` and `u1.txt` in the work tree only | 0 | ` M m3.txt`, ` M u1.txt` remain | the content as listed at `add` time (hook's lines NOT committed) | equal before |
| 6b appends to `m3.txt` and runs `git add m3.txt` | 0 | `MM m3.txt` remains | G12 set exact | equal before |
| 6c creates `hook-new.txt` | 0 | `?? hook-new.txt` appears | G12 set exact (new file not in it) | porcelain differs only by `?? hook-new.txt`; full index equal |

### Row 7 - hook sleeping 200 s, `subprocess.run(timeout=5)` (log header `row 7`)

(stdout/stderr of the commit went to files: with pipes `run()` would wait for the orphaned hook after the kill.)

| moment | HEAD | `index.lock` | processes |
|---|---|---|---|
| right after TimeoutExpired (5.0 s) | not moved | EXISTS (`.git/index.lock` and `.git/next-index-<pid>.lock`) | `run()` killed only the `git.exe` it started; the real `git.exe` child AND `sh.exe .git/hooks/pre-commit` are still alive |
| 10 s later | not moved | exists | both still alive |
| `read-tree <tree>` at that moment | - | - | exit 128 `Unable to create '.../index.lock': File exists` |
| after `taskkill /F /T /PID <hook sh pid read from the hook's own file>` | not moved | GONE (git aborted the commit itself and removed both lock files) | none left |
| `read-tree <tree>` after that | - | - | exit 0; porcelain and index equal before (`MM m5.txt` back), HEAD == head_before |

So a leftover lock exists only while the git/hook processes live; killing the git tree from outside (row 2d, `taskkill /F /T` on the git pid) leaves a STALE `index.lock`.

### Row 8 - G8 with the stash message, G9, G10 (log headers `row 8 | ...`, `row 8e`, `row 8f`, `row 8g`, `row 8h`)

| class | stash exit | stash entry / tree | `apply --index <sha12>` (a staged `qa-factory/staged.txt` in the index) |
|---|---|---|---|
| `??` file, folder, ` M`, ` D`, space, non-ASCII | 0 | person's entries gone, qa untouched | exit 0, porcelain and index equal before |
| `M `, `MM`, `A ` | 0 | gone, qa untouched | **exit 128** `error: qa-factory/staged.txt: already exists in index` / `conflicts in index. Try without --index.`; tree unchanged |
| `D `, `R ` | **128** | entry LEFT, tree unchanged (as B0) | exit 0 |
| ` A` | **128** `Entry 'itd10.txt' not uptodate. Cannot merge.` | no entry, tree unchanged | - |
| submodule ` M sub12` | 0 `No local changes to save` | no entry, nothing taken | - |
| NEW submodule | 0, stderr `warning: unable to rmdir 'sub13': Directory not empty` | entry made, but `?? sub13/` stays in the work tree | **exit 128** (same message) |
| MIXED | **128** (` A` in it) | no entry | - |

Cause check (row 8g, same stashes in repos WITHOUT the staged qa file): `apply --index <sha12>` exit 0 and porcelain == before AND index == before for `M `, `MM` (the split comes back), `A `, NEW submodule. With the staged qa file: `apply --index stash@{0}` also 128; plain `apply <sha12>` exit 0 and equals before for `A ` and NEW submodule, but NOT for `M ` / `MM` (staging lost: ` M m4.txt`, ` M m5.txt`). The failure shows only when the stash holds STAGED changes and the index has another staged entry.

G9: `rev-parse -q --verify refs/stash` exit 1, empty, before the first stash; the stash sha after; `git log -1 --format=%s <sha>` = `On master: <SMSG>`. G10 `stash list --format="%H %gd %s"` prints `<sha> stash@{N} On master: <SMSG>`.

DROP (rows 8, 8e, 8f, 8g, 8h):

| form | result |
|---|---|
| `git stash drop <sha12>` (letters in it) | **exit 128 `error: '<sha12>' is not a stash reference`**; entry stays. Same for the full 40-char sha and a 4-char prefix |
| `git stash drop stash@{N}`, N found by sha in `stash list --format="%H %gd"` | exit 0 `Dropped stash@{N} (<sha>)`; with ours at `stash@{1}` and another stash on top, only ours is dropped, the other remains |
| `git stash drop 0000000000000000` / `000000000000` (digits only) | exit 0 `Dropped refs/stash@{000000000000} (<sha of ANOTHER stash>)`: git read the digits as a date and dropped the TOP stash, which was not ours |

### Row 9 - G12, G11, G13 (log headers `row 9 | ...`)

| form | result |
|---|---|
| G12 `diff --name-status -z <head_before> HEAD`, mixed commit | `A\0a b.txt\0A\0add8.txt\0A\0caf\xc3\xa9.txt\0...D\0del6.txt\0...R100\0old9.txt\0new9.txt\0M\0sub12\0...` (rename: status token, OLD, NEW; every other: status token, path); `--no-renames` gives `A new9.txt`, `D old9.txt`; the plain (non `-z`) form quotes non-ASCII |
| G11 `rev-parse HEAD`, `HEAD^`, `--abbrev-ref HEAD` | sha, parent sha, `master` |
| G11 detached `--abbrev-ref HEAD` | `HEAD` (exit 0) |
| G11 `--show-toplevel` from root, from a subfolder, from `qa-factory/` | the same top path, forward slashes |
| unborn repo | `rev-parse HEAD` exit 128, stdout `HEAD`; `--abbrev-ref HEAD` exit 128; `--show-toplevel` exit 0; G1 exit 0 empty; G13 exit 128 `your current branch 'master' does not have any commits yet` |
| root commit | `rev-parse HEAD^` exit 128, stdout `HEAD^` |
| G13 with MSG (`(a\|b) [1.2]`) | exit 0, the newest matching sha |
| G13, a LATER commit whose subject merely CONTAINS MSG | that later commit is returned (substring match, not equality) |
| G13, no match | exit 0, empty |
| G13 without `--fixed-strings` | exit 0, EMPTY (regex characters of MSG break the match) |
| G13 with `--all` | same result |

## G-form -> ran, result, safe to use as written

| G | form | ran | result | safe as written |
|---|---|---|---|---|
| G1 | `status --porcelain=v1 -z -uall` | row 1, 17 trees | paths unquoted; rename = `XY new\0old\0`; folder expanded; nested repo stays `?? nested/`; ` A` visible; submodule ` M` | yes |
| G2 | `rev-parse --git-path <name>` + exists | row 2, 5 states + killed commit | exit 0 even for absent names; existence is the signal; rebase uses `rebase-merge` or `rebase-apply` by backend; revert (not in the spec list) uses `REVERT_HEAD` | yes, with the exists test |
| G3 | `ls-files -s -z -- <paths>` | row 3 | `160000` for the submodule; empty for untracked, nested, staged-deleted; 3 stages when unmerged | yes |
| G4 | `write-tree` | rows 4-7 | succeeds on every class incl. ` A`, but the tree has no intent-to-add entry | NO for ` A` (a later G6 cannot bring the ` A` entry back); yes otherwise |
| G5 | `add -- <Y != ' ' or ??>` then `commit -m MSG -- <all paths, both rename sides>` | rows 4, 5, 6, 9 | takes exactly the paths for all 16 classes incl. `MM`, `D `, `R `, `A `, space, non-ASCII, submodule, ` A`; leaves the staged qa file staged and uncommitted; hooks run | yes for the non-blocked classes; the undo is wrong only for ` A` |
| G6 | `read-tree <tree>` | rows 4, 5, 7, 2d | restores porcelain and full index incl. `MM` (`git show :m5.txt` equal); a hook-created file stays; exit 128 while `index.lock` exists | yes, except it cannot restore ` A` (shows `??`) |
| G7 | `reset --soft <head12>` | row 4 | abbreviated sha accepted; HEAD == head_before after it | yes |
| G8 | `stash push --include-untracked -m SMSG -- <paths>` | row 8 | exact for `??`, folder, ` M`, `M `, `MM`, ` D`, `A `, space, non-ASCII; FAILS or NO-OPS for `D `, `R ` (128 + entry left), ` A` (128, no entry), submodule ` M` (silent no-op, exit 0), NEW submodule (exit 0, `sub13/` left behind), and any mixed set containing them (128) | NO outside the exact-take classes |
| G9 | `rev-parse -q --verify refs/stash`; `log -1 --format=%s <sha>` | row 8 | exit 1 empty when no stash; sha after; subject `On master: <SMSG>` | yes |
| G10 | `stash apply --index <sha12>` | rows 8, 8e, 8g | exit 0 and equal before when the stash holds no staged change or no other staged entry is in the index; exit 128 when the stash holds staged changes (`M `, `MM`, `A `, new submodule) and the index has another staged entry (here the factory's staged file) | NO as the single undo form |
| G10 | `stash drop <sha12>` | rows 8, 8e, 8f, 8g, 8h | REFUSED, exit 128 `is not a stash reference`; a digits-only token is read as a date and drops the top stash | NO. `stash drop stash@{N}` (N from `stash list --format="%H %gd"`) worked, also when ours is not on top |
| G10 | `stash list --format="%H %gd %s"` | row 8 | `<sha> stash@{N} On master: <SMSG>` | yes |
| G11 | `rev-parse HEAD`, `HEAD^`, `--abbrev-ref HEAD`, `--show-toplevel` | row 9 | as the table; detached `--abbrev-ref` prints `HEAD`; unborn and root-commit forms exit 128 with the argument echoed on stdout | yes (exit code, not stdout, is the signal) |
| G12 | `diff --name-status -z <head_before> HEAD` | rows 4, 9 | exact path set in every committed row; rename is `R100\0old\0new` | yes (rename has two path tokens) |
| G13 | `log --fixed-strings --grep=<MSG> --format=%H -n 1` | rows 4, 9 | works with `(a\|b) [1.2]`; BUT substring match (a later commit containing MSG is returned); the regex form without `--fixed-strings` finds nothing | yes with `--fixed-strings`; not an equality test |

## Where reality differs from what the spec text assumes (facts for the Lead; no judgment on the spec)

1. G10 `git stash drop <sha12>` (spec §3.5 G10, §3.8 "drop that entry <drop form from B0-2>"): refused with exit 128. The form that worked is `git stash drop stash@{N}` with N looked up by sha through `stash list --format="%H %gd"`. A digits-only token drops the top stash (a different one).
2. G10 `git stash apply --index <sha12>` (spec §3.8 undo, state-exits): exit 128 and nothing restored when the stash holds staged changes and the index already holds another staged entry (the factory's own staged file is enough); plain `apply <sha12>` works there but loses the staging for `M `/`MM`.
3. G8 on ` A` (the spec's blocker list says ` A` blocks until B0-2 shows G4 handles it): stash exits 128 with no entry; commit of ` A` works, but `write-tree` omits the entry so G6 cannot restore it (` A` returns as `??`).
4. G8 on submodule: silent exit 0 no-op (the spec blocks stash on mode 160000: consistent); NEW submodule (`A  sub13`): stash exit 0, entry made, `sub13/` left in the work tree (not in the spec's blocker list).
5. G13 is a substring test: a later commit whose subject contains MSG is returned; without `--fixed-strings` an MSG with regex characters finds nothing.
6. The leftover `index.lock` after a timeout: while the git child and hook live the lock exists and G6 fails 128; killing the hook's process ends the commit and removes the lock; killing the git tree from outside leaves a stale lock and G6 fails 128 until it is removed.
7. Run-time note (not a git form): `subprocess.run(timeout=5)` kills only the git wrapper process it started; the real git child and the hook shell keep running.

## Runs

- Final source: `measure2.py` below. It was run from scratch twice on this final source (the script rebuilds every repository); the summary line is the last line of the verbatim output.
- Earlier runs on a source before rows 8g/8h were added (1711 git calls, 69 cases) gave the same results for rows 1-9; rows 8g/8h were added to establish the cause of the `apply --index` failure.
- Needed beyond the manifest: nothing outside the two given files; the rest of the spec (below line 511) was read to see B2's use of the forms.

## measure2.py (full source)

```python
"""B0-2 measurement (t-118): git command forms G1..G13 of fg7-8-b-vcs-words.md section 3.5.
Fresh scratch repos only (one per sub-case); every git call is `git -C <repo>` with cwd=<repo>; GIT_TERMINAL_PROMPT=0.
Script file is ASCII; non-ASCII names are built from code points. Writes the report file (header + analysis + source + log)."""
import json, os, shutil, stat, subprocess, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
ROOT = Path(r"C:\Users\i_mas\AppData\Local\Temp\claude\b3e3188b390a00d9\f92520fc-f552-4e47-9d06-efbc3daae572\scratchpad\b0-2")
REPOS = ROOT / "repos"
REPORT = Path(r"C:\QAFactory\forge-repo\docs\tasks\specs\reports\t-118-b0-2-git-measure.md")
ANALYSIS = ROOT / "analysis.txt"
ENV = dict(os.environ, GIT_TERMINAL_PROMPT="0", GCM_INTERACTIVE="Never")
MSG = "QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]"
SMSG = "QA Factory story t-118: your uncommitted changes, put aside before the tests"
LOG = []
STATS = {"cases": 0, "git_calls": 0, "errors": 0}
TABLE = []
DEVNULL = subprocess.DEVNULL
EACUTE = chr(0xE9)
CJK = chr(0x4E2D) + chr(0x6587)


def L(text=""):
    LOG.append(text)
    print(text)


def T(b):
    return b.decode("utf-8", "replace")


def fmt(args):
    return " ".join(a if (a.isascii() and a and not any(c in a for c in " \"'|&;()[]")) else ascii(a) for a in args)


def short(s, n=700):
    s = ascii(s)
    return s if len(s) <= n else s[:n] + "...(cut)"


def G(repo, *args, log=True, raw=False, timeout=60, note=""):
    p = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, cwd=str(repo), env=ENV, timeout=timeout, stdin=DEVNULL)
    STATS["git_calls"] += 1
    if log:
        so = repr(p.stdout) if raw else short(T(p.stdout).strip())
        L(f"$ git {fmt(args)}{('   # ' + note) if note else ''}\n  exit={p.returncode}\n  stdout={so}\n  stderr={short(T(p.stderr).strip(), 500)}")
    return p.returncode, p.stdout, p.stderr


def GS(repo, *args, **kw):
    rc, o, e = G(repo, *args, **kw)
    return rc, T(o).strip(), T(e).strip()


def porcelain(repo):
    return T(G(repo, "status", "--porcelain", log=False)[1])


def showp(label, text):
    L(f"porcelain {label}:\n" + (ascii(text.rstrip("\n")) if text.strip() else "(clean)").replace("\\n", "\n"))


def rmtree(path):
    def onerr(fn, p, exc):
        os.chmod(p, stat.S_IWRITE)
        fn(p)
    if path.exists():
        shutil.rmtree(path, onerror=onerr)


def W(repo, rel, text):
    p = repo / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(text.encode("utf-8"))


def fwd(p):
    return str(p).replace("\\", "/")


def parse_z(out):
    toks = out.split(b"\0")
    res, i = [], 0
    while i < len(toks):
        t = toks[i]
        i += 1
        if len(t) < 4:
            continue
        xy, path = T(t[:2]), T(t[3:])
        orig = ""
        if "R" in xy or "C" in xy:
            orig = T(toks[i]) if i < len(toks) else ""
            i += 1
        res.append({"xy": xy, "path": path, "orig": orig})
    return res


HOME = "qa-factory/"


def under_home(p):
    return p == HOME.rstrip("/") or p.startswith(HOME)


def classify(entries):
    person, factory, why = [], [], []
    for e in entries:
        sides = [e["path"]] + ([e["orig"]] if e["orig"] else [])
        inside = [under_home(s) for s in sides]
        if all(inside):
            factory.append(e)
            continue
        person.append(e)
        if any(inside):
            why.append("partial-home rename: " + e["path"])
        if e["path"].endswith("/") and e["xy"] == "??":
            why.append("nested repository: " + e["path"])
        if e["xy"] in ("DD", "AU", "UD", "UA", "DU", "AA", "UU"):
            why.append("unmerged: " + e["path"])
    return person, factory, why


def person_paths(person):
    out = []
    for e in person:
        out.append(e["path"])
        if e["orig"]:
            out.append(e["orig"])
    return out


# ---------------- classes: (label, base, dirty) ----------------
def mk_sub(repo, name, subdir):
    sub = repo.parent / (repo.name + "-subsrc-" + name)
    rmtree(sub)
    sub.mkdir(parents=True)
    G(sub, "init", "-q", log=False)
    G(sub, "config", "user.name", "t", log=False); G(sub, "config", "user.email", "t@t", log=False)
    W(sub, "s.txt", "s\n")
    G(sub, "add", "-A", log=False); G(sub, "commit", "-q", "-m", "s", log=False)
    rc, o, e = G(repo, "-c", "protocol.file.allow=always", "submodule", "add", "-q", str(sub), subdir, log=False)
    if rc:
        raise RuntimeError("submodule add failed: " + T(e))
    return sub


def c_ufile(r, ph):
    if ph == "dirty": W(r, "u1.txt", "u1\n")
def c_udir(r, ph):
    if ph == "dirty": W(r, "d2/a.txt", "a\n"); W(r, "d2/b.txt", "b\n")
def c_nested(r, ph):
    if ph == "dirty":
        (r / "nested").mkdir()
        G(r / "nested", "init", "-q", log=False); G(r / "nested", "config", "user.name", "t", log=False); G(r / "nested", "config", "user.email", "t@t", log=False)
        W(r, "nested/n.txt", "n\n"); G(r / "nested", "add", "-A", log=False); G(r / "nested", "commit", "-q", "-m", "n", log=False)
def c_mwt(r, ph):
    if ph == "base": W(r, "m3.txt", "base\n")
    else: W(r, "m3.txt", "worktree\n")
def c_midx(r, ph):
    if ph == "base": W(r, "m4.txt", "base\n")
    else: W(r, "m4.txt", "staged\n"); G(r, "add", "--", "m4.txt", log=False)
def c_mm(r, ph):
    if ph == "base": W(r, "m5.txt", "base\n")
    else: W(r, "m5.txt", "staged\n"); G(r, "add", "--", "m5.txt", log=False); W(r, "m5.txt", "worktree\n")
def c_dwt(r, ph):
    if ph == "base": W(r, "del6.txt", "x six\n")
    else: (r / "del6.txt").unlink()
def c_didx(r, ph):
    if ph == "base": W(r, "del7.txt", "unique seven\nzzz\n")
    else: G(r, "rm", "-q", "--", "del7.txt", log=False)
def c_aidx(r, ph):
    if ph == "dirty": W(r, "add8.txt", "totally different eight\n"); G(r, "add", "--", "add8.txt", log=False)
def c_aitd(r, ph):
    if ph == "dirty": W(r, "itd10.txt", "itd ten differs\n"); G(r, "add", "-N", "--", "itd10.txt", log=False)
def c_ridx(r, ph):
    if ph == "base": W(r, "old9.txt", "some content that is long enough\nline2\nline3\n")
    else: G(r, "mv", "old9.txt", "new9.txt", log=False)
def c_space(r, ph):
    if ph == "dirty": W(r, "a b.txt", "space\n")
def c_nonascii(r, ph):
    if ph == "dirty": W(r, "caf" + EACUTE + ".txt", "nonascii\n"); W(r, CJK + ".txt", "cjk\n")
def c_rnqa(r, ph):
    if ph == "base": W(r, "qa-factory/r.txt", "factory file with long enough content\nl2\nl3\n")
    else: (r / "src").mkdir(exist_ok=True); G(r, "mv", "qa-factory/r.txt", "src/y.txt", log=False)
def c_sub(r, ph):
    if ph == "base": mk_sub(r, "a", "sub12")
    else:
        W(r, "sub12/s2.txt", "s2\n"); G(r / "sub12", "add", "-A", log=False)
        G(r / "sub12", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "s2", log=False)
def c_subadd(r, ph):
    if ph == "dirty": mk_sub(r, "b", "sub13")


CL = {
    "u_file": ("?? file", c_ufile), "u_dir": ("?? folder with two files", c_udir), "nested": ("?? nested git repository", c_nested),
    "m_wt": (" M", c_mwt), "m_idx": ("M ", c_midx), "mm": ("MM", c_mm), "d_wt": (" D", c_dwt), "d_idx": ("D ", c_didx),
    "a_idx": ("A ", c_aidx), "a_itd": (" A (add -N)", c_aitd), "r_idx": ("R  (both sides outside)", c_ridx),
    "space": ("space in path", c_space), "nonascii": ("non-ASCII paths (e-acute, CJK)", c_nonascii),
    "rn_qa": ("rename qa-factory/r.txt -> src/y.txt", c_rnqa), "sub": (" M submodule pointer", c_sub), "sub_added": ("A  new submodule", c_subadd),
}
ALLOK = ["u_file", "u_dir", "m_wt", "m_idx", "mm", "d_wt", "d_idx", "a_idx", "a_itd", "r_idx", "space", "nonascii", "sub"]
ALLX = ALLOK + ["nested", "rn_qa"]


def build(name, ks, qa_staged=True):
    repo = REPOS / name
    rmtree(repo)
    rmtree(REPOS / (name + "-subsrc-a")); rmtree(REPOS / (name + "-subsrc-b"))
    repo.mkdir(parents=True)
    G(repo, "init", "-q", "-b", "master", log=False)
    for k, v in (("user.name", "t"), ("user.email", "t@t"), ("commit.gpgsign", "false"), ("core.autocrlf", "false")):
        G(repo, "config", k, v, log=False)
    W(repo, "qa-factory/x.txt", "base\n"); W(repo, "qa-factory/r.txt", "factory file with long enough content\nl2\nl3\n")
    for k in ks: CL[k][1](repo, "base")
    G(repo, "add", "-A", log=False)
    rc, o, e = G(repo, "commit", "-q", "-m", "base", log=False)
    if rc: raise RuntimeError("base commit failed: " + T(e))
    for k in ks: CL[k][1](repo, "dirty")
    W(repo, "qa-factory/x.txt", "dirty\n"); W(repo, "qa-factory/new.txt", "new\n"); W(repo, "qa-factory/staged.txt", "staged factory\n")
    if qa_staged:
        G(repo, "add", "--", "qa-factory/staged.txt", log=False)
    return repo


def qa_state(repo):
    lines = [l for l in porcelain(repo).splitlines() if "qa-factory/" in l]
    rc, o, e = G(repo, "show", ":qa-factory/staged.txt", log=False)
    return (lines, (repo / "qa-factory/x.txt").read_bytes(), (repo / "qa-factory/new.txt").read_bytes(), T(o))


def head(repo):
    rc, o, e = G(repo, "rev-parse", "HEAD", log=False)
    return T(o).strip() if rc == 0 else ""


def idx(repo):
    return G(repo, "ls-files", "-s", "-z", log=False)[1]


def fresh_state(repo):
    """Read the change set (G1), split it, return (entries, person, factory, why)."""
    rc, o, e = G(repo, "status", "--porcelain=v1", "-z", "-uall", log=False)
    entries = parse_z(o)
    person, factory, why = classify(entries)
    return entries, person, factory, why


def case(title):
    STATS["cases"] += 1
    L(f"\n=== {title} ===")


def safe(fn, *a):
    try:
        fn(*a)
    except Exception as ex:  # a failing row is a finding, never a crash of the whole run
        STATS["errors"] += 1
        L(f"!!! ROW ERROR in {fn.__name__}{a}: {ex!r}")


# ---------------- row 1: G1 ----------------
def row1():
    L("\n##### ROW 1: G1 `git status --porcelain=v1 -z -uall` per class (raw -z bytes shown as Python bytes repr)")
    for k in ALLX + ["sub_added"]:
        case(f"row 1 | class {k}: {CL[k][0]}")
        repo = build("r1-" + k, [k])
        showp("(plain, for reference)", porcelain(repo))
        G(repo, "status", "--porcelain=v1", "-z", "-uall", raw=True, note="G1")
        if k == "u_dir":
            G(repo, "status", "--porcelain=v1", "-z", raw=True, note="without -uall (folder collapsed)")
    case("row 1 | ALL classes together (nested and rn_qa included, sub_added excluded)")
    repo = build("r1-all", ALLX)
    showp("(plain)", porcelain(repo))
    G(repo, "status", "--porcelain=v1", "-z", "-uall", raw=True, note="G1")
    e, p, f, why = fresh_state(repo)
    L("split: person=" + ascii([(x['xy'], x['path'], x['orig']) for x in p]))
    L("split: factory=" + ascii([(x['xy'], x['path'], x['orig']) for x in f]))
    L("blockers seen by this script's classify(): " + ascii(why))


# ---------------- row 2: G2 ----------------
G2NAMES = ["MERGE_HEAD", "CHERRY_PICK_HEAD", "REVERT_HEAD", "rebase-merge", "rebase-apply", "index.lock"]


def g2(repo, label):
    L(f"-- G2 {label}")
    for n in G2NAMES:
        rc, o, e = G(repo, "rev-parse", "--git-path", n, log=False)
        pth = T(o).strip()
        ex = (repo / pth).exists() if rc == 0 else None
        L(f"   git rev-parse --git-path {n}: exit={rc} out={ascii(pth)} exists={ex} stderr={ascii(T(e).strip())}")


def conflict_repo(name):
    repo = REPOS / name
    rmtree(repo); repo.mkdir(parents=True)
    G(repo, "init", "-q", "-b", "master", log=False)
    for k, v in (("user.name", "t"), ("user.email", "t@t"), ("commit.gpgsign", "false"), ("core.autocrlf", "false")):
        G(repo, "config", k, v, log=False)
    W(repo, "c.txt", "base\n"); W(repo, "qa-factory/x.txt", "base\n")
    G(repo, "add", "-A", log=False); G(repo, "commit", "-q", "-m", "base", log=False)
    G(repo, "checkout", "-q", "-b", "topic", log=False); W(repo, "c.txt", "topic\n"); G(repo, "commit", "-q", "-am", "topic", log=False)
    G(repo, "checkout", "-q", "master", log=False); W(repo, "c.txt", "master\n"); G(repo, "commit", "-q", "-am", "master", log=False)
    return repo


def row2():
    L("\n##### ROW 2: G2 in operation states")
    case("row 2 | control: clean repo")
    repo = conflict_repo("r2-clean"); g2(repo, "clean repo")
    case("row 2a | merge stopped on a conflict")
    repo = conflict_repo("r2-merge")
    G(repo, "merge", "topic", note="expected conflict")
    showp("now", porcelain(repo)); G(repo, "status", "--porcelain=v1", "-z", "-uall", raw=True, note="G1 during merge")
    g2(repo, "merge conflict")
    G(repo, "ls-files", "-s", "-z", "--", "c.txt", raw=True, note="G3 on the unmerged path: three stages")
    case("row 2b | rebase stopped on a conflict (default backend)")
    repo = conflict_repo("r2-rebase")
    G(repo, "checkout", "-q", "topic", log=False)
    G(repo, "rebase", "master", note="expected conflict")
    showp("now", porcelain(repo)); g2(repo, "rebase (merge backend)")
    case("row 2b2 | rebase --apply stopped on a conflict")
    repo = conflict_repo("r2-rebase-apply")
    G(repo, "checkout", "-q", "topic", log=False)
    G(repo, "rebase", "--apply", "master", note="expected conflict")
    showp("now", porcelain(repo)); g2(repo, "rebase --apply")
    case("row 2c | cherry-pick stopped on a conflict")
    repo = conflict_repo("r2-cherry")
    G(repo, "cherry-pick", "topic", note="expected conflict")
    showp("now", porcelain(repo)); g2(repo, "cherry-pick")
    case("row 2c2 | revert stopped on a conflict (not in the spec list; same family)")
    repo = conflict_repo("r2-revert")
    G(repo, "revert", "--no-edit", "HEAD~1", note="expected conflict")
    showp("now", porcelain(repo)); g2(repo, "revert")


def sleeper_hook(repo, tag):
    pidf, winf = ROOT / f"{tag}-pid.txt", ROOT / f"{tag}-winpid.txt"
    for f in (pidf, winf):
        if f.exists(): f.unlink()
    hook = f'#!/bin/sh\necho $$ > "{fwd(pidf)}"\ncat /proc/$$/winpid > "{fwd(winf)}"\nsleep 200\n'
    hp = repo / ".git" / "hooks" / "pre-commit"
    hp.write_bytes(hook.encode("ascii"))
    return pidf, winf


def write_hook(repo, body):
    (repo / ".git" / "hooks" / "pre-commit").write_bytes(("#!/bin/sh\n" + body).encode("ascii"))


def ps_procs():
    cmd = ('Get-CimInstance Win32_Process -Filter "Name=\'git.exe\' OR Name=\'sh.exe\' OR Name=\'sleep.exe\' OR Name=\'bash.exe\'" | '
           'Select-Object ProcessId,ParentProcessId,Name,CommandLine | ConvertTo-Json -Compress')
    p = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", cmd], capture_output=True, timeout=60, stdin=DEVNULL)
    txt = T(p.stdout).strip()
    if not txt:
        return []
    data = json.loads(txt)
    return data if isinstance(data, list) else [data]


def pid_alive(pid):
    p = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True, timeout=30, stdin=DEVNULL)
    return str(pid) in T(p.stdout)


def read_pid(f):
    return f.read_text().strip() if f.exists() else ""


def lockfiles(repo):
    gd = repo / ".git"
    return sorted(str(p.relative_to(repo)).replace("\\", "/") for p in gd.rglob("*") if p.is_file() and p.name.endswith(".lock"))


def snapshot(repo, label, head_before, winf):
    win = read_pid(winf)
    L(f"-- snapshot {label}: HEAD={head(repo)[:12]} (before {head_before[:12]}, moved={head(repo) != head_before}); lock files in .git: {lockfiles(repo)}; "
      f"index.lock exists={(repo / '.git' / 'index.lock').exists()}; hook winpid file={win!r}; hook shell alive={pid_alive(win) if win else 'n/a'}")
    mine = []
    for pr in ps_procs():
        cl = pr.get("CommandLine") or ""
        if "b0-2" in cl or str(pr["ProcessId"]) == win or str(pr["ParentProcessId"]) == win:
            if pr["ProcessId"] != os.getpid():
                mine.append(pr)
    L("   scratch-related git/sh/sleep processes: " + ascii([(m["ProcessId"], m["ParentProcessId"], m["Name"], (m.get("CommandLine") or "")[:140]) for m in mine]))
    return mine


def killtree(pid):
    p = subprocess.run(["taskkill", "/F", "/T", "/PID", str(pid)], capture_output=True, timeout=30, stdin=DEVNULL)
    L(f"   taskkill /F /T /PID {pid}: exit={p.returncode} {ascii(T(p.stdout).strip())} {ascii(T(p.stderr).strip())}")


def row2d():
    case("row 2d | G2 after a killed commit (git commit started by Popen, hook sleeping, killed with taskkill /T on the pid I started)")
    repo = build("r2d", ["mm", "u_file"])
    hb = head(repo); tree = T(G(repo, "write-tree", log=False)[1]).strip()
    e, person, f, why = fresh_state(repo); paths = person_paths(person)
    pidf, winf = sleeper_hook(repo, "r2d")
    G(repo, "add", "--", *[x["path"] for x in person if x["xy"][1] != " "])
    proc = subprocess.Popen(["git", "-C", str(repo), "commit", "-m", MSG, "--", *paths], cwd=str(repo), env=ENV, stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL)
    time.sleep(4)
    L(f"popen pid={proc.pid} alive(poll)={proc.poll() is None}")
    snapshot(repo, "while commit runs", hb, winf)
    killtree(proc.pid)
    time.sleep(1)
    win = read_pid(winf)
    L(f"after taskkill /T: popen poll={proc.poll()}; hook shell alive={pid_alive(win) if win else 'n/a'}")
    left = snapshot(repo, "after kill", hb, winf)
    g2(repo, "after killed commit")
    if win and pid_alive(win): killtree(win)
    G(repo, "read-tree", tree, note="G6 with the stale lock in place")
    (repo / ".git" / "index.lock").unlink(missing_ok=True)
    L("   (scratch only: removed .git/index.lock by hand; the factory itself never deletes it)")
    G(repo, "read-tree", tree, note="G6 after removing the lock")
    showp("after read-tree", porcelain(repo))


# ---------------- row 3: G3 ----------------
def row3():
    L("\n##### ROW 3: G3 `git ls-files -s -z -- <paths>`")
    case("row 3 | submodule, plain file, deleted-staged path, nested repo, qa path")
    repo = build("r3", ["sub", "mm", "d_idx", "nested", "space", "nonascii"])
    for pth in ["sub12", "m5.txt", "del7.txt", "nested", "a b.txt", "caf" + EACUTE + ".txt", "qa-factory/x.txt", "nothere.txt"]:
        G(repo, "ls-files", "-s", "-z", "--", pth, raw=True, note="G3, pathspec " + ascii(pth))
    G(repo, "ls-files", "-s", "-z", "--", "sub12", "m5.txt", raw=True, note="G3, two paths (mode 160000 = submodule)")


# ---------------- row 4: G4 -> G5 -> G7 + G6 ----------------
def flow_commit(tag, ks, hook=None, expect_fail_hook=False):
    repo = build("r4-" + tag, ks)
    if hook: write_hook(repo, hook)
    hb = head(repo)
    before = porcelain(repo); idx0 = idx(repo); qa0 = qa_state(repo)
    mm_show0 = T(G(repo, "show", ":m5.txt", log=False)[1]) if "mm" in ks else None
    showp("BEFORE", before)
    e, person, factory, why = fresh_state(repo)
    if why:
        L(f"BLOCKED by blocker rules of spec 3.7 ({why}); not run")
        TABLE.append((tag, "blocked: " + "; ".join(why)[:60], "", "", "", ""))
        return
    paths = person_paths(person)
    L("person paths: " + ascii(paths))
    rc, o, er = G(repo, "write-tree", note="G4")
    if rc:
        L("G4 FAILED: nothing is written (spec step 5)")
        TABLE.append((tag, "G4 failed rc=%d" % rc, "", "", "", ""))
        return
    tree = T(o).strip()
    addp = [x["path"] for x in person if x["xy"][1] != " "]
    if addp: G(repo, "add", "--", *addp, note="G5 add: entries with Y != ' ' or ??")
    else: L("G5 add skipped: no entry has a worktree change (edge 5)")
    rc, o, er = G(repo, "commit", "-m", MSG, "--", *paths, note="G5 commit")
    after = porcelain(repo); showp("AFTER commit", after)
    qa1 = qa_state(repo)
    hn = head(repo)
    took = remaining = "n/a"
    if rc == 0:
        rc2, d, _ = G(repo, "diff", "--name-status", "-z", hb, "HEAD", raw=True, note="G12")
        dp = set()
        toks = T(d).split("\0")
        for t in toks[1:]:  # status tokens (letters) alternate with paths; take non-status tokens
            pass
        i = 0
        while i < len(toks) and toks[i]:
            st = toks[i]; i += 1
            n = 2 if st[0] in "RC" else 1
            dp.update(toks[i:i + n]); i += n
        took = (dp == set(paths)) and not any(under_home(x) for x in dp)
        L(f"G12 path set {ascii(sorted(dp))} == person paths: {dp == set(paths)}; touches qa-factory: {any(under_home(x) for x in dp)}")
        parent = T(G(repo, "rev-parse", "HEAD^", note="G11 HEAD^")[1]).strip()
        L(f"HEAD^ == head_before: {parent == hb}; HEAD moved: {hn != hb}")
        ee, pp, ff, ww = fresh_state(repo)
        remaining = [x["path"] for x in pp]
        L("person entries remaining after commit: " + ascii(remaining))
        G(repo, "log", "--fixed-strings", "--grep=" + MSG, "--format=%H", "-n", "1", note="G13")
        G(repo, "reset", "--soft", hb[:12], note="G7")
        G(repo, "read-tree", tree, note="G6")
        after2 = porcelain(repo); showp("AFTER undo (G7+G6)", after2)
        same_p = after2 == before; same_i = idx(repo) == idx0; qa2 = qa_state(repo)
        mm_note = ""
        if mm_show0 is not None:
            now = T(G(repo, "show", ":m5.txt", log=False)[1])
            mm_note = f"; git show :m5.txt before={ascii(mm_show0.strip())} after-undo={ascii(now.strip())}"
        L(f"undo: porcelain == before: {same_p}; full index (ls-files -s -z) == before: {same_i}; qa-factory state == before: {qa2 == qa0}; HEAD == head_before: {head(repo) == hb}{mm_note}")
        TABLE.append((tag, f"rc={rc}", f"took exactly: {took}", f"qa untouched: {qa1 == qa0}", f"undo porcelain==before: {same_p}", f"undo index==before: {same_i}"))
    else:
        L(f"commit failed rc={rc}; HEAD moved={hn != hb}; qa untouched={qa1 == qa0}; porcelain == before (index state after add differs?): {after == before}")
        G(repo, "read-tree", tree, note="G6 restore after failure")
        after2 = porcelain(repo); showp("AFTER G6", after2)
        mm_note = ""
        if mm_show0 is not None:
            now = T(G(repo, "show", ":m5.txt", log=False)[1])
            mm_note = f"; git show :m5.txt before={ascii(mm_show0.strip())} after-G6={ascii(now.strip())}"
        L(f"restore: porcelain == before: {after2 == before}; full index == before: {idx(repo) == idx0}; qa state == before: {qa_state(repo) == qa0}{mm_note}")
        TABLE.append((tag, f"rc={rc}", "n/a", f"qa untouched: {qa_state(repo) == qa0}", f"G6 porcelain==before: {after2 == before}", f"G6 index==before: {idx(repo) == idx0}"))


def row4():
    L("\n##### ROW 4: G4 -> G5 -> G12/G11/G13 -> G7 + G6 per class (every repo also carries dirty qa-factory/x.txt, untracked qa-factory/new.txt and a STAGED qa-factory/staged.txt)")
    for k in ALLX + ["sub_added"]:
        case(f"row 4 | class {k}: {CL[k][0]}")
        safe(flow_commit, k, [k])
    case("row 4 | MIXED: all non-blocked classes in one tree")
    safe(flow_commit, "ALLOK", ALLOK)


# ---------------- row 5, 6 ----------------
def row5():
    L("\n##### ROW 5: pre-commit hook exits 1")
    for tag, ks in (("mm", ["mm"]), ("allok", ALLOK)):
        case(f"row 5 | hook exit 1, {tag}")
        safe(flow_commit, "hook1-" + tag, ks, "echo 'hook: refused' >&2\nexit 1\n")


def row6():
    L("\n##### ROW 6: hooks that change files")
    case("row 6a | hook rewrites a listed file (appends to m3.txt and u1.txt in the work tree) and does not touch the index")
    safe(flow_commit, "hook-rewrite", ["m_wt", "u_file", "mm"], "echo hookline >> m3.txt\necho hookline >> u1.txt\nexit 0\n")
    case("row 6b | hook rewrites a listed file AND re-adds it (git add m3.txt)")
    safe(flow_commit, "hook-rewrite-add", ["m_wt", "u_file"], "echo hookline >> m3.txt\ngit add m3.txt\nexit 0\n")
    case("row 6c | hook creates a new untracked file")
    safe(flow_commit, "hook-newfile", ["m_wt", "u_file"], "echo created > hook-new.txt\nexit 0\n")
    for tag in ("hook-rewrite", "hook-rewrite-add", "hook-newfile"):
        repo = REPOS / ("r4-" + tag)
        L(f"-- {tag}: repo state after the flow (undo already ran in the flow; shown for the record)")
        showp(tag + " final", porcelain(repo))


# ---------------- row 7 ----------------
def row7():
    L("\n##### ROW 7: pre-commit hook sleeping 200 s; subprocess.run(timeout=5) (stdout/stderr to files, not pipes, so run() does not wait for the orphaned hook)")
    case("row 7 | G5 commit with timeout")
    repo = build("r7", ["mm", "u_file"])
    hb = head(repo); before = porcelain(repo); idx0 = idx(repo)
    tree = T(G(repo, "write-tree", note="G4")[1]).strip()
    e, person, f, why = fresh_state(repo); paths = person_paths(person)
    pidf, winf = sleeper_hook(repo, "r7")
    G(repo, "add", "--", *[x["path"] for x in person if x["xy"][1] != " "], note="G5 add")
    of, ef = open(ROOT / "r7-out.txt", "wb"), open(ROOT / "r7-err.txt", "wb")
    t0 = time.time()
    try:
        r = subprocess.run(["git", "-C", str(repo), "commit", "-m", MSG, "--", *paths], cwd=str(repo), env=ENV, stdin=DEVNULL, stdout=of, stderr=ef, timeout=5)
        L(f"commit returned exit={r.returncode} after {time.time() - t0:.1f}s (no timeout)")
    except subprocess.TimeoutExpired:
        L(f"TimeoutExpired after {time.time() - t0:.1f}s; run() killed the git process it started")
    of.close(); ef.close()
    snapshot(repo, "right after the timeout", hb, winf)
    showp("right after the timeout", porcelain(repo))
    time.sleep(10)
    mine = snapshot(repo, "10 s later", hb, winf)
    G(repo, "read-tree", tree, note="G6 while the lock / orphaned hook are still there")
    win = read_pid(winf)
    if win and pid_alive(win): killtree(win)
    time.sleep(1)
    snapshot(repo, "after killing the hook's tree (pid read from its own file)", hb, winf)
    for pr in ps_procs():
        cl = pr.get("CommandLine") or ""
        if "b0-2" in cl and pr["ProcessId"] != os.getpid():
            L("   leftover scratch process, killing by pid: " + ascii((pr["ProcessId"], pr["Name"])))
            killtree(pr["ProcessId"])
    L(f"index.lock still exists after every process is gone: {(repo / '.git' / 'index.lock').exists()}")
    G(repo, "read-tree", tree, note="G6 with the stale lock (no process left)")
    (repo / ".git" / "index.lock").unlink(missing_ok=True)
    L("   (scratch only: removed .git/index.lock by hand; the factory never deletes it)")
    G(repo, "read-tree", tree, note="G6 after removing the lock")
    after = porcelain(repo); showp("after G6", after)
    L(f"porcelain == before: {after == before}; index == before: {idx(repo) == idx0}; HEAD == head_before: {head(repo) == hb}")


# ---------------- row 8 ----------------
def flow_stash(tag, ks):
    repo = build("r8-" + tag, ks)
    hb = head(repo); before = porcelain(repo); idx0 = idx(repo); qa0 = qa_state(repo)
    showp("BEFORE", before)
    e, person, f, why = fresh_state(repo)
    if why:
        L(f"BLOCKED by blocker rules of spec 3.7 ({why}); not run")
        return
    paths = person_paths(person)
    rc9, o9, _ = G(repo, "rev-parse", "-q", "--verify", "refs/stash", note="G9 before")
    rc, o, er = G(repo, "stash", "push", "--include-untracked", "-m", SMSG, "--", *paths, note="G8")
    rc9b, o9b, _ = G(repo, "rev-parse", "-q", "--verify", "refs/stash", note="G9 after")
    sha = T(o9b).strip()
    after = porcelain(repo); showp("AFTER stash", after)
    ee, pp, ff, ww = fresh_state(repo)
    L(f"person entries remaining: {ascii([x['path'] for x in pp])}; qa-factory untouched: {qa_state(repo) == qa0}")
    if not sha:
        L("no stash ref after the command")
        TABLE.append((tag, f"stash rc={rc}", "no entry", f"qa untouched: {qa_state(repo) == qa0}", "", ""))
        return
    G(repo, "log", "-1", "--format=%s", sha, note="G9 subject")
    G(repo, "stash", "list", "--format=%H %gd %s", note="G10 list")
    rca, oa, ea = G(repo, "stash", "apply", "--index", sha[:12], note="G10 apply by sha12")
    aa = porcelain(repo); showp("AFTER apply --index", aa)
    same_p = aa == before; same_i = idx(repo) == idx0
    L(f"after apply --index: porcelain == before: {same_p}; full index == before: {same_i}; qa untouched: {qa_state(repo) == qa0}")
    G(repo, "stash", "drop", sha[:12], note="G10 drop by sha12")
    G(repo, "stash", "list", "--format=%H %gd %s", note="G10 list after drop")
    G(repo, "rev-parse", "-q", "--verify", "refs/stash", note="G9 after drop")
    TABLE.append((tag, f"stash rc={rc}", f"person left: {len(pp)}", f"apply rc={rca}", f"apply porcelain==before: {same_p}", f"apply index==before: {same_i}"))


def row8():
    L("\n##### ROW 8: G8 with the stash message, G9, G10 (apply --index by sha12, drop by sha12)")
    for k in [x for x in ALLX if x not in ("nested", "rn_qa")] + ["sub_added"]:
        case(f"row 8 | class {k}: {CL[k][0]}")
        safe(flow_stash, k, [k])
    case("row 8 | MIXED all non-blocked classes")
    safe(flow_stash, "ALLOK", ALLOK)
    case("row 8e | our stash is NOT on top: another stash is pushed after ours, then drop <our sha12>")
    repo = build("r8-notop", ["mm", "u_file"])
    e, person, f, why = fresh_state(repo); paths = person_paths(person)
    G(repo, "stash", "push", "--include-untracked", "-m", SMSG, "--", *paths, note="G8 ours")
    sha = T(G(repo, "rev-parse", "-q", "--verify", "refs/stash", log=False)[1]).strip()
    W(repo, "other.txt", "o\n"); G(repo, "stash", "push", "--include-untracked", "-m", "someone elses stash", "--", "other.txt", note="another stash on top")
    G(repo, "stash", "list", "--format=%H %gd %s", note="G10 list: ours is stash@{1}")
    G(repo, "stash", "apply", "--index", sha[:12], note="G10 apply ours by sha12 (not on top)")
    G(repo, "stash", "drop", sha[:12], note="G10 drop ours by sha12")
    G(repo, "stash", "list", "--format=%H %gd %s", note="G10 list after: only the other stash must remain")
    case("row 8f | drop with an unknown / too-short / full sha")
    G(repo, "stash", "drop", "0000000000000000", note="unknown sha")
    G(repo, "stash", "drop", sha, note="full sha of the already dropped entry")
    G(repo, "stash", "drop", sha[:4], note="4-char abbreviation")


def gd_of(repo, sha):
    """Find `stash@{N}` of a stash by its sha through the list (the form `git stash drop` accepts)."""
    rc, o, e = G(repo, "stash", "list", "--format=%H %gd", log=False)
    for line in T(o).splitlines():
        h, _, gd = line.partition(" ")
        if h == sha:
            return gd
    return ""


def row8g():
    L("\n##### ROW 8g: why `apply --index` failed above (a STAGED qa-factory/staged.txt is in the index) and what drop form works")
    for k in ["m_idx", "mm", "a_idx", "sub_added"]:
        case(f"row 8g | class {k}: the SAME stash in a repo WITHOUT the staged qa-factory/staged.txt (cause check)")
        repo = build("r8g-noqa-" + k, [k], qa_staged=False)
        before = porcelain(repo); idx0 = idx(repo)
        e, person, f, why = fresh_state(repo); paths = person_paths(person)
        G(repo, "stash", "push", "--include-untracked", "-m", SMSG, "--", *paths, note="G8")
        sha = T(G(repo, "rev-parse", "-q", "--verify", "refs/stash", log=False)[1]).strip()
        G(repo, "stash", "apply", "--index", sha[:12], note="G10 apply --index by sha12, no staged qa file")
        aa = porcelain(repo)
        L(f"porcelain == before: {aa == before}; index == before: {idx(repo) == idx0}")
        showp("after apply", aa)
        gd = gd_of(repo, sha)
        G(repo, "stash", "drop", gd, note=f"drop by the list's own name {gd} (found by sha {sha[:12]} in `stash list --format=%H %gd`)")
        G(repo, "stash", "list", "--format=%H %gd %s", note="list after drop")
    for k in ["m_idx", "mm", "a_idx", "sub_added"]:
        case(f"row 8g | class {k}: WITH the staged qa-factory/staged.txt: apply WITHOUT --index, and apply --index by stash@{{N}}")
        repo = build("r8g-qa-" + k, [k])
        before = porcelain(repo); idx0 = idx(repo)
        e, person, f, why = fresh_state(repo); paths = person_paths(person)
        G(repo, "stash", "push", "--include-untracked", "-m", SMSG, "--", *paths, note="G8")
        sha = T(G(repo, "rev-parse", "-q", "--verify", "refs/stash", log=False)[1]).strip()
        gd = gd_of(repo, sha)
        G(repo, "stash", "apply", "--index", gd, note="apply --index by " + gd)
        G(repo, "stash", "apply", sha[:12], note="apply WITHOUT --index, by sha12")
        aa = porcelain(repo); showp("after plain apply", aa)
        L(f"porcelain == before: {aa == before}; index == before: {idx(repo) == idx0}")
        G(repo, "stash", "drop", gd, note="drop by " + gd)
    case("row 8h | drop by stash@{N} when ours is NOT on top (another stash on top); drop must remove ours only")
    repo = build("r8h", ["u_file", "m_wt"], qa_staged=False)
    e, person, f, why = fresh_state(repo); paths = person_paths(person)
    G(repo, "stash", "push", "--include-untracked", "-m", SMSG, "--", *paths, note="G8 ours")
    sha = T(G(repo, "rev-parse", "-q", "--verify", "refs/stash", log=False)[1]).strip()
    W(repo, "other.txt", "o\n"); G(repo, "stash", "push", "--include-untracked", "-m", "someone elses stash", "--", "other.txt", note="another stash on top")
    gd = gd_of(repo, sha)
    L("ours is " + gd)
    G(repo, "stash", "apply", "--index", gd, note="apply --index ours by " + gd + " (qa-factory not staged here)")
    G(repo, "stash", "drop", gd, note="drop ours by " + gd)
    G(repo, "stash", "list", "--format=%H %gd %s", note="only the other stash must remain")
    case("row 8h | a sha12 made only of decimal digits is read by git as a date/number (sha-prefix risk): drop <digits>")
    G(repo, "stash", "drop", "000000000000", note="12 digits, no such stash (what does git drop?)")
    G(repo, "stash", "list", "--format=%H %gd %s", note="list after")


# ---------------- row 9 ----------------
def row9():
    L("\n##### ROW 9: G12, G11, G13")
    case("row 9 | G12 `git diff --name-status -z <head_before> HEAD` after a mixed commit (rename, delete, add, modify, submodule, space, non-ASCII)")
    repo = build("r9", ALLOK)
    hb = head(repo)
    e, person, f, why = fresh_state(repo); paths = person_paths(person)
    G(repo, "add", "--", *[x["path"] for x in person if x["xy"][1] != " "], log=False)
    G(repo, "commit", "-q", "-m", MSG, "--", *paths, note="G5 commit")
    G(repo, "diff", "--name-status", "-z", hb, "HEAD", raw=True, note="G12")
    G(repo, "diff", "--name-status", "-z", "--no-renames", hb, "HEAD", raw=True, note="G12 with --no-renames")
    G(repo, "diff", "--name-status", hb, "HEAD", note="G12 plain, for reference")
    case("row 9 | G11 forms")
    G(repo, "rev-parse", "HEAD", note="G11 HEAD")
    G(repo, "rev-parse", "HEAD^", note="G11 HEAD^ (parent of the new commit)")
    G(repo, "rev-parse", "--abbrev-ref", "HEAD", note="G11 branch")
    G(repo, "rev-parse", "--show-toplevel", note="G11 toplevel from the root")
    (repo / "deep" / "er").mkdir(parents=True)
    G(repo / "deep" / "er", "rev-parse", "--show-toplevel", note="G11 toplevel from a subfolder (git -C <subfolder>)")
    G(repo / "qa-factory", "rev-parse", "--show-toplevel", note="G11 toplevel from qa-factory/")
    G(repo, "checkout", "-q", "--detach", log=False)
    G(repo, "rev-parse", "--abbrev-ref", "HEAD", note="G11 detached: prints HEAD")
    G(repo, "rev-parse", "HEAD^", note="G11 detached HEAD^")
    case("row 9 | G11 on a repository with no commit, and HEAD^ on a root commit")
    un = REPOS / "r9-unborn"; rmtree(un); un.mkdir(parents=True); G(un, "init", "-q", "-b", "master", log=False)
    G(un, "rev-parse", "HEAD", note="unborn: HEAD")
    G(un, "rev-parse", "--abbrev-ref", "HEAD", note="unborn: abbrev-ref")
    G(un, "rev-parse", "--show-toplevel", note="unborn: toplevel")
    G(un, "status", "--porcelain=v1", "-z", "-uall", raw=True, note="unborn: G1 (empty)")
    G(un, "log", "--fixed-strings", "--grep=" + MSG, "--format=%H", "-n", "1", note="unborn: G13")
    rt = build("r9-root", [])
    G(rt, "rev-parse", "HEAD^", note="root commit: HEAD^")
    case("row 9 | G13 `git log --fixed-strings --grep=<MSG> --format=%H -n 1`")
    repo = build("r9-g13", ["m_wt"])
    G(repo, "add", "--", "m3.txt", log=False)
    G(repo, "commit", "-q", "-m", MSG, "--", "m3.txt", note="commit with MSG")
    W(repo, "next.txt", "n\n"); G(repo, "add", "--", "next.txt", log=False)
    G(repo, "commit", "-q", "-m", MSG + " second commit with the same MSG as its prefix", "--", "next.txt", note="a later commit whose subject CONTAINS MSG")
    G(repo, "log", "--format=%H %s", note="whole log")
    G(repo, "log", "--fixed-strings", "--grep=" + MSG, "--format=%H", "-n", "1", note="G13 (newest match wins with -n 1)")
    G(repo, "log", "--fixed-strings", "--grep=no such message", "--format=%H", "-n", "1", note="G13 no match: empty, exit?")
    G(repo, "log", "--grep=" + MSG, "--format=%H", "-n", "1", note="WITHOUT --fixed-strings (regex chars in MSG), for contrast")
    G(repo, "log", "--fixed-strings", "--grep=" + MSG, "--format=%H", "-n", "1", "--all", note="G13 with --all (stash refs / other branches)")


def main():
    REPOS.mkdir(parents=True, exist_ok=True)
    ver = subprocess.run(["git", "--version"], capture_output=True, text=True).stdout.strip()
    L("git version: " + ver)
    L("note: repos are built with core.autocrlf=false to keep stderr free of CRLF warnings (B0 had them)")
    for r in (row1, row2, row2d, row3, row4, row5, row6, row7, row8, row8g, row9):
        safe(r)
    L("\n\nTABLE rows 4/8 (tag, commit/stash exit, took, qa untouched, undo porcelain, undo index)")
    for t in TABLE:
        L("| " + " | ".join(str(x) for x in t) + " |")
    L(f"\nSUMMARY: cases={STATS['cases']} git_calls={STATS['git_calls']} row_errors={STATS['errors']} git={ver}")
    src = Path(__file__).read_text(encoding="utf-8")
    analysis = ANALYSIS.read_text(encoding="utf-8") if ANALYSIS.exists() else "(analysis not written yet)\n"
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("# t-118 B0-2: git command forms G1-G13 measured in scratch repositories\n\ngit version: `" + ver + "`\n\nCommand: `python -B " + str(Path(__file__)) +
                      "`\n\n" + analysis + "\n## measure2.py (full source)\n\n```python\n" + src + "\n```\n\n## Verbatim output of the run\n\n```\n" + "\n".join(LOG) + "\n```\n", encoding="utf-8")
    return 0


sys.exit(main())

```

## Verbatim output of the run

```
git version: git version 2.56.0.windows.2
note: repos are built with core.autocrlf=false to keep stderr free of CRLF warnings (B0 had them)

##### ROW 1: G1 `git status --porcelain=v1 -z -uall` per class (raw -z bytes shown as Python bytes repr)

=== row 1 | class u_file: ?? file ===
porcelain (plain, for reference):
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt
?? u1.txt'
$ git status --porcelain=v1 -z -uall   # G1
  exit=0
  stdout=b'A  qa-factory/staged.txt\x00 M qa-factory/x.txt\x00?? qa-factory/new.txt\x00?? u1.txt\x00'
  stderr=''

=== row 1 | class u_dir: ?? folder with two files ===
porcelain (plain, for reference):
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? d2/
?? qa-factory/new.txt'
$ git status --porcelain=v1 -z -uall   # G1
  exit=0
  stdout=b'A  qa-factory/staged.txt\x00 M qa-factory/x.txt\x00?? d2/a.txt\x00?? d2/b.txt\x00?? qa-factory/new.txt\x00'
  stderr=''
$ git status --porcelain=v1 -z   # without -uall (folder collapsed)
  exit=0
  stdout=b'A  qa-factory/staged.txt\x00 M qa-factory/x.txt\x00?? d2/\x00?? qa-factory/new.txt\x00'
  stderr=''

=== row 1 | class m_wt:  M ===
porcelain (plain, for reference):
' M m3.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
$ git status --porcelain=v1 -z -uall   # G1
  exit=0
  stdout=b' M m3.txt\x00A  qa-factory/staged.txt\x00 M qa-factory/x.txt\x00?? qa-factory/new.txt\x00'
  stderr=''

=== row 1 | class m_idx: M  ===
porcelain (plain, for reference):
'M  m4.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
$ git status --porcelain=v1 -z -uall   # G1
  exit=0
  stdout=b'M  m4.txt\x00A  qa-factory/staged.txt\x00 M qa-factory/x.txt\x00?? qa-factory/new.txt\x00'
  stderr=''

=== row 1 | class mm: MM ===
porcelain (plain, for reference):
'MM m5.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
$ git status --porcelain=v1 -z -uall   # G1
  exit=0
  stdout=b'MM m5.txt\x00A  qa-factory/staged.txt\x00 M qa-factory/x.txt\x00?? qa-factory/new.txt\x00'
  stderr=''

=== row 1 | class d_wt:  D ===
porcelain (plain, for reference):
' D del6.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
$ git status --porcelain=v1 -z -uall   # G1
  exit=0
  stdout=b' D del6.txt\x00A  qa-factory/staged.txt\x00 M qa-factory/x.txt\x00?? qa-factory/new.txt\x00'
  stderr=''

=== row 1 | class d_idx: D  ===
porcelain (plain, for reference):
'D  del7.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
$ git status --porcelain=v1 -z -uall   # G1
  exit=0
  stdout=b'D  del7.txt\x00A  qa-factory/staged.txt\x00 M qa-factory/x.txt\x00?? qa-factory/new.txt\x00'
  stderr=''

=== row 1 | class a_idx: A  ===
porcelain (plain, for reference):
'A  add8.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
$ git status --porcelain=v1 -z -uall   # G1
  exit=0
  stdout=b'A  add8.txt\x00A  qa-factory/staged.txt\x00 M qa-factory/x.txt\x00?? qa-factory/new.txt\x00'
  stderr=''

=== row 1 | class a_itd:  A (add -N) ===
porcelain (plain, for reference):
' A itd10.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
$ git status --porcelain=v1 -z -uall   # G1
  exit=0
  stdout=b' A itd10.txt\x00A  qa-factory/staged.txt\x00 M qa-factory/x.txt\x00?? qa-factory/new.txt\x00'
  stderr=''

=== row 1 | class r_idx: R  (both sides outside) ===
porcelain (plain, for reference):
'R  old9.txt -> new9.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
$ git status --porcelain=v1 -z -uall   # G1
  exit=0
  stdout=b'R  new9.txt\x00old9.txt\x00A  qa-factory/staged.txt\x00 M qa-factory/x.txt\x00?? qa-factory/new.txt\x00'
  stderr=''

=== row 1 | class space: space in path ===
porcelain (plain, for reference):
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? "a b.txt"
?? qa-factory/new.txt'
$ git status --porcelain=v1 -z -uall   # G1
  exit=0
  stdout=b'A  qa-factory/staged.txt\x00 M qa-factory/x.txt\x00?? a b.txt\x00?? qa-factory/new.txt\x00'
  stderr=''

=== row 1 | class nonascii: non-ASCII paths (e-acute, CJK) ===
porcelain (plain, for reference):
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? "caf\\303\\251.txt"
?? qa-factory/new.txt
?? "\\344\\270\\255\\346\\226\\207.txt"'
$ git status --porcelain=v1 -z -uall   # G1
  exit=0
  stdout=b'A  qa-factory/staged.txt\x00 M qa-factory/x.txt\x00?? caf\xc3\xa9.txt\x00?? qa-factory/new.txt\x00?? \xe4\xb8\xad\xe6\x96\x87.txt\x00'
  stderr=''

=== row 1 | class sub:  M submodule pointer ===
porcelain (plain, for reference):
'A  qa-factory/staged.txt
 M qa-factory/x.txt
 M sub12
?? qa-factory/new.txt'
$ git status --porcelain=v1 -z -uall   # G1
  exit=0
  stdout=b'A  qa-factory/staged.txt\x00 M qa-factory/x.txt\x00 M sub12\x00?? qa-factory/new.txt\x00'
  stderr=''

=== row 1 | class nested: ?? nested git repository ===
porcelain (plain, for reference):
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? nested/
?? qa-factory/new.txt'
$ git status --porcelain=v1 -z -uall   # G1
  exit=0
  stdout=b'A  qa-factory/staged.txt\x00 M qa-factory/x.txt\x00?? nested/\x00?? qa-factory/new.txt\x00'
  stderr=''

=== row 1 | class rn_qa: rename qa-factory/r.txt -> src/y.txt ===
porcelain (plain, for reference):
'A  qa-factory/staged.txt
 M qa-factory/x.txt
R  qa-factory/r.txt -> src/y.txt
?? qa-factory/new.txt'
$ git status --porcelain=v1 -z -uall   # G1
  exit=0
  stdout=b'A  qa-factory/staged.txt\x00 M qa-factory/x.txt\x00R  src/y.txt\x00qa-factory/r.txt\x00?? qa-factory/new.txt\x00'
  stderr=''

=== row 1 | class sub_added: A  new submodule ===
porcelain (plain, for reference):
'A  .gitmodules
A  qa-factory/staged.txt
 M qa-factory/x.txt
A  sub13
?? qa-factory/new.txt'
$ git status --porcelain=v1 -z -uall   # G1
  exit=0
  stdout=b'A  .gitmodules\x00A  qa-factory/staged.txt\x00 M qa-factory/x.txt\x00A  sub13\x00?? qa-factory/new.txt\x00'
  stderr=''

=== row 1 | ALL classes together (nested and rn_qa included, sub_added excluded) ===
porcelain (plain):
'A  add8.txt
 D del6.txt
D  del7.txt
 A itd10.txt
 M m3.txt
M  m4.txt
MM m5.txt
R  old9.txt -> new9.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
R  qa-factory/r.txt -> src/y.txt
 M sub12
?? "a b.txt"
?? "caf\\303\\251.txt"
?? d2/
?? nested/
?? qa-factory/new.txt
?? u1.txt
?? "\\344\\270\\255\\346\\226\\207.txt"'
$ git status --porcelain=v1 -z -uall   # G1
  exit=0
  stdout=b'A  add8.txt\x00 D del6.txt\x00D  del7.txt\x00 A itd10.txt\x00 M m3.txt\x00M  m4.txt\x00MM m5.txt\x00R  new9.txt\x00old9.txt\x00A  qa-factory/staged.txt\x00 M qa-factory/x.txt\x00R  src/y.txt\x00qa-factory/r.txt\x00 M sub12\x00?? a b.txt\x00?? caf\xc3\xa9.txt\x00?? d2/a.txt\x00?? d2/b.txt\x00?? nested/\x00?? qa-factory/new.txt\x00?? u1.txt\x00?? \xe4\xb8\xad\xe6\x96\x87.txt\x00'
  stderr=''
split: person=[('A ', 'add8.txt', ''), (' D', 'del6.txt', ''), ('D ', 'del7.txt', ''), (' A', 'itd10.txt', ''), (' M', 'm3.txt', ''), ('M ', 'm4.txt', ''), ('MM', 'm5.txt', ''), ('R ', 'new9.txt', 'old9.txt'), ('R ', 'src/y.txt', 'qa-factory/r.txt'), (' M', 'sub12', ''), ('??', 'a b.txt', ''), ('??', 'caf\xe9.txt', ''), ('??', 'd2/a.txt', ''), ('??', 'd2/b.txt', ''), ('??', 'nested/', ''), ('??', 'u1.txt', ''), ('??', '\u4e2d\u6587.txt', '')]
split: factory=[('A ', 'qa-factory/staged.txt', ''), (' M', 'qa-factory/x.txt', ''), ('??', 'qa-factory/new.txt', '')]
blockers seen by this script's classify(): ['partial-home rename: src/y.txt', 'nested repository: nested/']

##### ROW 2: G2 in operation states

=== row 2 | control: clean repo ===
-- G2 clean repo
   git rev-parse --git-path MERGE_HEAD: exit=0 out='.git/MERGE_HEAD' exists=False stderr=''
   git rev-parse --git-path CHERRY_PICK_HEAD: exit=0 out='.git/CHERRY_PICK_HEAD' exists=False stderr=''
   git rev-parse --git-path REVERT_HEAD: exit=0 out='.git/REVERT_HEAD' exists=False stderr=''
   git rev-parse --git-path rebase-merge: exit=0 out='.git/rebase-merge' exists=False stderr=''
   git rev-parse --git-path rebase-apply: exit=0 out='.git/rebase-apply' exists=False stderr=''
   git rev-parse --git-path index.lock: exit=0 out='.git/index.lock' exists=False stderr=''

=== row 2a | merge stopped on a conflict ===
$ git merge topic   # expected conflict
  exit=1
  stdout='Auto-merging c.txt\nCONFLICT (content): Merge conflict in c.txt\nAutomatic merge failed; fix conflicts and then commit the result.'
  stderr=''
porcelain now:
'UU c.txt'
$ git status --porcelain=v1 -z -uall   # G1 during merge
  exit=0
  stdout=b'UU c.txt\x00'
  stderr=''
-- G2 merge conflict
   git rev-parse --git-path MERGE_HEAD: exit=0 out='.git/MERGE_HEAD' exists=True stderr=''
   git rev-parse --git-path CHERRY_PICK_HEAD: exit=0 out='.git/CHERRY_PICK_HEAD' exists=False stderr=''
   git rev-parse --git-path REVERT_HEAD: exit=0 out='.git/REVERT_HEAD' exists=False stderr=''
   git rev-parse --git-path rebase-merge: exit=0 out='.git/rebase-merge' exists=False stderr=''
   git rev-parse --git-path rebase-apply: exit=0 out='.git/rebase-apply' exists=False stderr=''
   git rev-parse --git-path index.lock: exit=0 out='.git/index.lock' exists=False stderr=''
$ git ls-files -s -z -- c.txt   # G3 on the unmerged path: three stages
  exit=0
  stdout=b'100644 df967b96a579e45a18b8251732d16804b2e56a55 1\tc.txt\x00100644 1f7391f92b6a3792204e07e99f71f643cc35e7e1 2\tc.txt\x00100644 0f62d67e76ce1255a098942495a846df0f8a2c11 3\tc.txt\x00'
  stderr=''

=== row 2b | rebase stopped on a conflict (default backend) ===
$ git rebase master   # expected conflict
  exit=1
  stdout='Auto-merging c.txt\nCONFLICT (content): Merge conflict in c.txt'
  stderr='Rebasing (1/1)\rerror: could not apply a1aaf75... topic\nhint: Resolve all conflicts manually, mark them as resolved with\nhint: "git add/rm <conflicted_files>", then run "git rebase --continue".\nhint: You can instead skip this commit: run "git rebase --skip".\nhint: To abort and get back to the state before "git rebase", run "git rebase --abort".\nhint: Disable this message with "git config set advice.mergeConflict false"\nCould not apply a1aaf75... # topic'
porcelain now:
'UU c.txt'
-- G2 rebase (merge backend)
   git rev-parse --git-path MERGE_HEAD: exit=0 out='.git/MERGE_HEAD' exists=False stderr=''
   git rev-parse --git-path CHERRY_PICK_HEAD: exit=0 out='.git/CHERRY_PICK_HEAD' exists=False stderr=''
   git rev-parse --git-path REVERT_HEAD: exit=0 out='.git/REVERT_HEAD' exists=False stderr=''
   git rev-parse --git-path rebase-merge: exit=0 out='.git/rebase-merge' exists=True stderr=''
   git rev-parse --git-path rebase-apply: exit=0 out='.git/rebase-apply' exists=False stderr=''
   git rev-parse --git-path index.lock: exit=0 out='.git/index.lock' exists=False stderr=''

=== row 2b2 | rebase --apply stopped on a conflict ===
$ git rebase --apply master   # expected conflict
  exit=1
  stdout='First, rewinding head to replay your work on top of it...\nApplying: topic\nUsing index info to reconstruct a base tree...\nM\tc.txt\nFalling back to patching base and 3-way merge...\nAuto-merging c.txt\nCONFLICT (content): Merge conflict in c.txt\nPatch failed at 0001 topic'
  stderr='error: Failed to merge in the changes.\nhint: Use \'git am --show-current-patch=diff\' to see the failed patch\nhint: Resolve all conflicts manually, mark them as resolved with\nhint: "git add/rm <conflicted_files>", then run "git rebase --continue".\nhint: You can instead skip this commit: run "git rebase --skip".\nhint: To abort and get back to the state before "git rebase", run "git rebase --abort".\nhint: Disable this message with "git config set advice.mergeConflict false"'
porcelain now:
'UU c.txt'
-- G2 rebase --apply
   git rev-parse --git-path MERGE_HEAD: exit=0 out='.git/MERGE_HEAD' exists=False stderr=''
   git rev-parse --git-path CHERRY_PICK_HEAD: exit=0 out='.git/CHERRY_PICK_HEAD' exists=False stderr=''
   git rev-parse --git-path REVERT_HEAD: exit=0 out='.git/REVERT_HEAD' exists=False stderr=''
   git rev-parse --git-path rebase-merge: exit=0 out='.git/rebase-merge' exists=False stderr=''
   git rev-parse --git-path rebase-apply: exit=0 out='.git/rebase-apply' exists=True stderr=''
   git rev-parse --git-path index.lock: exit=0 out='.git/index.lock' exists=False stderr=''

=== row 2c | cherry-pick stopped on a conflict ===
$ git cherry-pick topic   # expected conflict
  exit=1
  stdout='Auto-merging c.txt\nCONFLICT (content): Merge conflict in c.txt'
  stderr='error: could not apply 4cc9ec7... topic\nhint: After resolving the conflicts, mark them with\nhint: "git add/rm <pathspec>", then run\nhint: "git cherry-pick --continue".\nhint: You can instead skip this commit with "git cherry-pick --skip".\nhint: To abort and get back to the state before "git cherry-pick",\nhint: run "git cherry-pick --abort".\nhint: Disable this message with "git config set advice.mergeConflict false"'
porcelain now:
'UU c.txt'
-- G2 cherry-pick
   git rev-parse --git-path MERGE_HEAD: exit=0 out='.git/MERGE_HEAD' exists=False stderr=''
   git rev-parse --git-path CHERRY_PICK_HEAD: exit=0 out='.git/CHERRY_PICK_HEAD' exists=True stderr=''
   git rev-parse --git-path REVERT_HEAD: exit=0 out='.git/REVERT_HEAD' exists=False stderr=''
   git rev-parse --git-path rebase-merge: exit=0 out='.git/rebase-merge' exists=False stderr=''
   git rev-parse --git-path rebase-apply: exit=0 out='.git/rebase-apply' exists=False stderr=''
   git rev-parse --git-path index.lock: exit=0 out='.git/index.lock' exists=False stderr=''

=== row 2c2 | revert stopped on a conflict (not in the spec list; same family) ===
$ git revert --no-edit HEAD~1   # expected conflict
  exit=1
  stdout='CONFLICT (modify/delete): c.txt deleted in (empty tree) and modified in HEAD.  Version HEAD of c.txt left in tree.'
  stderr='error: could not revert 6d82363... base\nhint: After resolving the conflicts, mark them with\nhint: "git add/rm <pathspec>", then run\nhint: "git revert --continue".\nhint: You can instead skip this commit with "git revert --skip".\nhint: To abort and get back to the state before "git revert",\nhint: run "git revert --abort".\nhint: Disable this message with "git config set advice.mergeConflict false"'
porcelain now:
'UD c.txt
D  qa-factory/x.txt'
-- G2 revert
   git rev-parse --git-path MERGE_HEAD: exit=0 out='.git/MERGE_HEAD' exists=False stderr=''
   git rev-parse --git-path CHERRY_PICK_HEAD: exit=0 out='.git/CHERRY_PICK_HEAD' exists=False stderr=''
   git rev-parse --git-path REVERT_HEAD: exit=0 out='.git/REVERT_HEAD' exists=True stderr=''
   git rev-parse --git-path rebase-merge: exit=0 out='.git/rebase-merge' exists=False stderr=''
   git rev-parse --git-path rebase-apply: exit=0 out='.git/rebase-apply' exists=False stderr=''
   git rev-parse --git-path index.lock: exit=0 out='.git/index.lock' exists=False stderr=''

=== row 2d | G2 after a killed commit (git commit started by Popen, hook sleeping, killed with taskkill /T on the pid I started) ===
$ git add -- m5.txt u1.txt
  exit=0
  stdout=''
  stderr=''
popen pid=26356 alive(poll)=True
-- snapshot while commit runs: HEAD=3d4c646fd50b (before 3d4c646fd50b, moved=False); lock files in .git: ['.git/index.lock', '.git/next-index-912.lock']; index.lock exists=True; hook winpid file='12856'; hook shell alive=True
   scratch-related git/sh/sleep processes: [(1692, 25448, 'bash.exe', '"C:\\Program Files\\Git\\bin\\bash.exe" -c "source /c/Users/i_mas/.claude/shell-snapshots/snapshot-bash-1794478599150-q85ezr.sh 2>/dev/null || t'), (24764, 1692, 'bash.exe', '"C:\\Program Files\\Git\\bin\\..\\usr\\bin\\bash.exe" -c "source /c/Users/i_mas/.claude/shell-snapshots/snapshot-bash-1794478599150-q85ezr.sh 2>/de'), (26356, 15380, 'git.exe', 'git -C C:\\Users\\i_mas\\AppData\\Local\\Temp\\claude\\b3e3188b390a00d9\\f92520fc-f552-4e47-9d06-efbc3daae572\\scratchpad\\b0-2\\repos\\r2d commit -m "Q'), (912, 26356, 'git.exe', 'git.exe -C C:\\Users\\i_mas\\AppData\\Local\\Temp\\claude\\b3e3188b390a00d9\\f92520fc-f552-4e47-9d06-efbc3daae572\\scratchpad\\b0-2\\repos\\r2d commit -'), (12856, 912, 'sh.exe', 'sh .git/hooks/pre-commit')]
   taskkill /F /T /PID 26356: exit=0 'SUCCESS: The process with PID 12856 (child process of PID 912) has been terminated.\r\nSUCCESS: The process with PID 912 (child process of PID 26356) has been terminated.\r\nSUCCESS: The process with PID 26356 (child process of PID 15380) has been terminated.' ''
after taskkill /T: popen poll=1; hook shell alive=False
-- snapshot after kill: HEAD=3d4c646fd50b (before 3d4c646fd50b, moved=False); lock files in .git: ['.git/index.lock', '.git/next-index-912.lock']; index.lock exists=True; hook winpid file='12856'; hook shell alive=False
   scratch-related git/sh/sleep processes: [(1692, 25448, 'bash.exe', '"C:\\Program Files\\Git\\bin\\bash.exe" -c "source /c/Users/i_mas/.claude/shell-snapshots/snapshot-bash-1794478599150-q85ezr.sh 2>/dev/null || t'), (24764, 1692, 'bash.exe', '"C:\\Program Files\\Git\\bin\\..\\usr\\bin\\bash.exe" -c "source /c/Users/i_mas/.claude/shell-snapshots/snapshot-bash-1794478599150-q85ezr.sh 2>/de')]
-- G2 after killed commit
   git rev-parse --git-path MERGE_HEAD: exit=0 out='.git/MERGE_HEAD' exists=False stderr=''
   git rev-parse --git-path CHERRY_PICK_HEAD: exit=0 out='.git/CHERRY_PICK_HEAD' exists=False stderr=''
   git rev-parse --git-path REVERT_HEAD: exit=0 out='.git/REVERT_HEAD' exists=False stderr=''
   git rev-parse --git-path rebase-merge: exit=0 out='.git/rebase-merge' exists=False stderr=''
   git rev-parse --git-path rebase-apply: exit=0 out='.git/rebase-apply' exists=False stderr=''
   git rev-parse --git-path index.lock: exit=0 out='.git/index.lock' exists=True stderr=''
$ git read-tree 14ce1a6a0caabce2eabebbc764e1675b550132d6   # G6 with the stale lock in place
  exit=128
  stdout=''
  stderr="fatal: Unable to create 'C:/Users/i_mas/AppData/Local/Temp/claude/b3e3188b390a00d9/f92520fc-f552-4e47-9d06-efbc3daae572/scratchpad/b0-2/repos/r2d/.git/index.lock': File exists.\n\nAnother git process seems to be running in this repository, or the lock file may be stale"
   (scratch only: removed .git/index.lock by hand; the factory itself never deletes it)
$ git read-tree 14ce1a6a0caabce2eabebbc764e1675b550132d6   # G6 after removing the lock
  exit=0
  stdout=''
  stderr=''
porcelain after read-tree:
'MM m5.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt
?? u1.txt'

##### ROW 3: G3 `git ls-files -s -z -- <paths>`

=== row 3 | submodule, plain file, deleted-staged path, nested repo, qa path ===
$ git ls-files -s -z -- sub12   # G3, pathspec 'sub12'
  exit=0
  stdout=b'160000 afd625081a77b359e2682289b512279ca69205ee 0\tsub12\x00'
  stderr=''
$ git ls-files -s -z -- m5.txt   # G3, pathspec 'm5.txt'
  exit=0
  stdout=b'100644 19d9cc8584ac2c7dcf57d2680375e80f099dc481 0\tm5.txt\x00'
  stderr=''
$ git ls-files -s -z -- del7.txt   # G3, pathspec 'del7.txt'
  exit=0
  stdout=b''
  stderr=''
$ git ls-files -s -z -- nested   # G3, pathspec 'nested'
  exit=0
  stdout=b''
  stderr=''
$ git ls-files -s -z -- 'a b.txt'   # G3, pathspec 'a b.txt'
  exit=0
  stdout=b''
  stderr=''
$ git ls-files -s -z -- 'caf\xe9.txt'   # G3, pathspec 'caf\xe9.txt'
  exit=0
  stdout=b''
  stderr=''
$ git ls-files -s -z -- qa-factory/x.txt   # G3, pathspec 'qa-factory/x.txt'
  exit=0
  stdout=b'100644 df967b96a579e45a18b8251732d16804b2e56a55 0\tqa-factory/x.txt\x00'
  stderr=''
$ git ls-files -s -z -- nothere.txt   # G3, pathspec 'nothere.txt'
  exit=0
  stdout=b''
  stderr=''
$ git ls-files -s -z -- sub12 m5.txt   # G3, two paths (mode 160000 = submodule)
  exit=0
  stdout=b'100644 19d9cc8584ac2c7dcf57d2680375e80f099dc481 0\tm5.txt\x00160000 afd625081a77b359e2682289b512279ca69205ee 0\tsub12\x00'
  stderr=''

##### ROW 4: G4 -> G5 -> G12/G11/G13 -> G7 + G6 per class (every repo also carries dirty qa-factory/x.txt, untracked qa-factory/new.txt and a STAGED qa-factory/staged.txt)

=== row 4 | class u_file: ?? file ===
porcelain BEFORE:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt
?? u1.txt'
person paths: ['u1.txt']
$ git write-tree   # G4
  exit=0
  stdout='ba3e7bb61e014cc4203a4f131270231dda6ff60f'
  stderr=''
$ git add -- u1.txt   # G5 add: entries with Y != ' ' or ??
  exit=0
  stdout=''
  stderr=''
$ git commit -m 'QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' -- u1.txt   # G5 commit
  exit=0
  stdout='[master 875b889] QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]\n 1 file changed, 1 insertion(+)\n create mode 100644 u1.txt'
  stderr=''
porcelain AFTER commit:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
$ git diff --name-status -z 4b0a8b68304514a50cccfc9d318f9467469180eb HEAD   # G12
  exit=0
  stdout=b'A\x00u1.txt\x00'
  stderr=''
G12 path set ['u1.txt'] == person paths: True; touches qa-factory: False
$ git rev-parse HEAD^   # G11 HEAD^
  exit=0
  stdout='4b0a8b68304514a50cccfc9d318f9467469180eb'
  stderr=''
HEAD^ == head_before: True; HEAD moved: True
person entries remaining after commit: []
$ git log --fixed-strings '--grep=QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' --format=%H -n 1   # G13
  exit=0
  stdout='875b889f587d00685e5564b51562f999e0ff5edf'
  stderr=''
$ git reset --soft 4b0a8b683045   # G7
  exit=0
  stdout=''
  stderr=''
$ git read-tree ba3e7bb61e014cc4203a4f131270231dda6ff60f   # G6
  exit=0
  stdout=''
  stderr=''
porcelain AFTER undo (G7+G6):
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt
?? u1.txt'
undo: porcelain == before: True; full index (ls-files -s -z) == before: True; qa-factory state == before: True; HEAD == head_before: True

=== row 4 | class u_dir: ?? folder with two files ===
porcelain BEFORE:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? d2/
?? qa-factory/new.txt'
person paths: ['d2/a.txt', 'd2/b.txt']
$ git write-tree   # G4
  exit=0
  stdout='ba3e7bb61e014cc4203a4f131270231dda6ff60f'
  stderr=''
$ git add -- d2/a.txt d2/b.txt   # G5 add: entries with Y != ' ' or ??
  exit=0
  stdout=''
  stderr=''
$ git commit -m 'QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' -- d2/a.txt d2/b.txt   # G5 commit
  exit=0
  stdout='[master 8b74deb] QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]\n 2 files changed, 2 insertions(+)\n create mode 100644 d2/a.txt\n create mode 100644 d2/b.txt'
  stderr=''
porcelain AFTER commit:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
$ git diff --name-status -z d885c8bb28c39786c416ae5bac6d0b62b0463550 HEAD   # G12
  exit=0
  stdout=b'A\x00d2/a.txt\x00A\x00d2/b.txt\x00'
  stderr=''
G12 path set ['d2/a.txt', 'd2/b.txt'] == person paths: True; touches qa-factory: False
$ git rev-parse HEAD^   # G11 HEAD^
  exit=0
  stdout='d885c8bb28c39786c416ae5bac6d0b62b0463550'
  stderr=''
HEAD^ == head_before: True; HEAD moved: True
person entries remaining after commit: []
$ git log --fixed-strings '--grep=QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' --format=%H -n 1   # G13
  exit=0
  stdout='8b74deb323fa143dc21bffe0cd5475b0af574c7c'
  stderr=''
$ git reset --soft d885c8bb28c3   # G7
  exit=0
  stdout=''
  stderr=''
$ git read-tree ba3e7bb61e014cc4203a4f131270231dda6ff60f   # G6
  exit=0
  stdout=''
  stderr=''
porcelain AFTER undo (G7+G6):
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? d2/
?? qa-factory/new.txt'
undo: porcelain == before: True; full index (ls-files -s -z) == before: True; qa-factory state == before: True; HEAD == head_before: True

=== row 4 | class m_wt:  M ===
porcelain BEFORE:
' M m3.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
person paths: ['m3.txt']
$ git write-tree   # G4
  exit=0
  stdout='f74d8e874a59d2c315808522601e0fda9d5c8edc'
  stderr=''
$ git add -- m3.txt   # G5 add: entries with Y != ' ' or ??
  exit=0
  stdout=''
  stderr=''
$ git commit -m 'QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' -- m3.txt   # G5 commit
  exit=0
  stdout='[master 20dda54] QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]\n 1 file changed, 1 insertion(+), 1 deletion(-)'
  stderr=''
porcelain AFTER commit:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
$ git diff --name-status -z de9f6a1d4e287be02a99bb27926435adca3850eb HEAD   # G12
  exit=0
  stdout=b'M\x00m3.txt\x00'
  stderr=''
G12 path set ['m3.txt'] == person paths: True; touches qa-factory: False
$ git rev-parse HEAD^   # G11 HEAD^
  exit=0
  stdout='de9f6a1d4e287be02a99bb27926435adca3850eb'
  stderr=''
HEAD^ == head_before: True; HEAD moved: True
person entries remaining after commit: []
$ git log --fixed-strings '--grep=QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' --format=%H -n 1   # G13
  exit=0
  stdout='20dda54983204bd66572c91f787d9603709d0ae4'
  stderr=''
$ git reset --soft de9f6a1d4e28   # G7
  exit=0
  stdout=''
  stderr=''
$ git read-tree f74d8e874a59d2c315808522601e0fda9d5c8edc   # G6
  exit=0
  stdout=''
  stderr=''
porcelain AFTER undo (G7+G6):
' M m3.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
undo: porcelain == before: True; full index (ls-files -s -z) == before: True; qa-factory state == before: True; HEAD == head_before: True

=== row 4 | class m_idx: M  ===
porcelain BEFORE:
'M  m4.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
person paths: ['m4.txt']
$ git write-tree   # G4
  exit=0
  stdout='9482b61b867a3f870c9479e5fb1f9c8a5d02891d'
  stderr=''
G5 add skipped: no entry has a worktree change (edge 5)
$ git commit -m 'QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' -- m4.txt   # G5 commit
  exit=0
  stdout='[master 82068a9] QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]\n 1 file changed, 1 insertion(+), 1 deletion(-)'
  stderr=''
porcelain AFTER commit:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
$ git diff --name-status -z 8f453050193f9efc67ef5fc9d2710422661f084e HEAD   # G12
  exit=0
  stdout=b'M\x00m4.txt\x00'
  stderr=''
G12 path set ['m4.txt'] == person paths: True; touches qa-factory: False
$ git rev-parse HEAD^   # G11 HEAD^
  exit=0
  stdout='8f453050193f9efc67ef5fc9d2710422661f084e'
  stderr=''
HEAD^ == head_before: True; HEAD moved: True
person entries remaining after commit: []
$ git log --fixed-strings '--grep=QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' --format=%H -n 1   # G13
  exit=0
  stdout='82068a97edd717989492dded681ac111d863c325'
  stderr=''
$ git reset --soft 8f453050193f   # G7
  exit=0
  stdout=''
  stderr=''
$ git read-tree 9482b61b867a3f870c9479e5fb1f9c8a5d02891d   # G6
  exit=0
  stdout=''
  stderr=''
porcelain AFTER undo (G7+G6):
'M  m4.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
undo: porcelain == before: True; full index (ls-files -s -z) == before: True; qa-factory state == before: True; HEAD == head_before: True

=== row 4 | class mm: MM ===
porcelain BEFORE:
'MM m5.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
person paths: ['m5.txt']
$ git write-tree   # G4
  exit=0
  stdout='14ce1a6a0caabce2eabebbc764e1675b550132d6'
  stderr=''
$ git add -- m5.txt   # G5 add: entries with Y != ' ' or ??
  exit=0
  stdout=''
  stderr=''
$ git commit -m 'QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' -- m5.txt   # G5 commit
  exit=0
  stdout='[master 8a63cdc] QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]\n 1 file changed, 1 insertion(+), 1 deletion(-)'
  stderr=''
porcelain AFTER commit:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
$ git diff --name-status -z 0ab245309703ea008d2ac175a93b27299ebfb0d4 HEAD   # G12
  exit=0
  stdout=b'M\x00m5.txt\x00'
  stderr=''
G12 path set ['m5.txt'] == person paths: True; touches qa-factory: False
$ git rev-parse HEAD^   # G11 HEAD^
  exit=0
  stdout='0ab245309703ea008d2ac175a93b27299ebfb0d4'
  stderr=''
HEAD^ == head_before: True; HEAD moved: True
person entries remaining after commit: []
$ git log --fixed-strings '--grep=QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' --format=%H -n 1   # G13
  exit=0
  stdout='8a63cdca459146202f978b0b06cf5b7d85da578d'
  stderr=''
$ git reset --soft 0ab245309703   # G7
  exit=0
  stdout=''
  stderr=''
$ git read-tree 14ce1a6a0caabce2eabebbc764e1675b550132d6   # G6
  exit=0
  stdout=''
  stderr=''
porcelain AFTER undo (G7+G6):
'MM m5.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
undo: porcelain == before: True; full index (ls-files -s -z) == before: True; qa-factory state == before: True; HEAD == head_before: True; git show :m5.txt before='staged' after-undo='staged'

=== row 4 | class d_wt:  D ===
porcelain BEFORE:
' D del6.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
person paths: ['del6.txt']
$ git write-tree   # G4
  exit=0
  stdout='13167e816efc0e4e88dbd69c048733be70ff44b3'
  stderr=''
$ git add -- del6.txt   # G5 add: entries with Y != ' ' or ??
  exit=0
  stdout=''
  stderr=''
$ git commit -m 'QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' -- del6.txt   # G5 commit
  exit=0
  stdout='[master 0117a0d] QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]\n 1 file changed, 1 deletion(-)\n delete mode 100644 del6.txt'
  stderr=''
porcelain AFTER commit:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
$ git diff --name-status -z d31cf8071cf4bb3561384062ab7217a10335cf00 HEAD   # G12
  exit=0
  stdout=b'D\x00del6.txt\x00'
  stderr=''
G12 path set ['del6.txt'] == person paths: True; touches qa-factory: False
$ git rev-parse HEAD^   # G11 HEAD^
  exit=0
  stdout='d31cf8071cf4bb3561384062ab7217a10335cf00'
  stderr=''
HEAD^ == head_before: True; HEAD moved: True
person entries remaining after commit: []
$ git log --fixed-strings '--grep=QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' --format=%H -n 1   # G13
  exit=0
  stdout='0117a0dff8fc12c07d5f1dad75b88709c60e7cc9'
  stderr=''
$ git reset --soft d31cf8071cf4   # G7
  exit=0
  stdout=''
  stderr=''
$ git read-tree 13167e816efc0e4e88dbd69c048733be70ff44b3   # G6
  exit=0
  stdout=''
  stderr=''
porcelain AFTER undo (G7+G6):
' D del6.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
undo: porcelain == before: True; full index (ls-files -s -z) == before: True; qa-factory state == before: True; HEAD == head_before: True

=== row 4 | class d_idx: D  ===
porcelain BEFORE:
'D  del7.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
person paths: ['del7.txt']
$ git write-tree   # G4
  exit=0
  stdout='ba3e7bb61e014cc4203a4f131270231dda6ff60f'
  stderr=''
G5 add skipped: no entry has a worktree change (edge 5)
$ git commit -m 'QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' -- del7.txt   # G5 commit
  exit=0
  stdout='[master 10562bd] QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]\n 1 file changed, 2 deletions(-)\n delete mode 100644 del7.txt'
  stderr=''
porcelain AFTER commit:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
$ git diff --name-status -z 5cecdc33553d5c3c35854216bb7afbe54dcc402c HEAD   # G12
  exit=0
  stdout=b'D\x00del7.txt\x00'
  stderr=''
G12 path set ['del7.txt'] == person paths: True; touches qa-factory: False
$ git rev-parse HEAD^   # G11 HEAD^
  exit=0
  stdout='5cecdc33553d5c3c35854216bb7afbe54dcc402c'
  stderr=''
HEAD^ == head_before: True; HEAD moved: True
person entries remaining after commit: []
$ git log --fixed-strings '--grep=QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' --format=%H -n 1   # G13
  exit=0
  stdout='10562bd235a67d323f2d364ed0df1e18e018c140'
  stderr=''
$ git reset --soft 5cecdc33553d   # G7
  exit=0
  stdout=''
  stderr=''
$ git read-tree ba3e7bb61e014cc4203a4f131270231dda6ff60f   # G6
  exit=0
  stdout=''
  stderr=''
porcelain AFTER undo (G7+G6):
'D  del7.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
undo: porcelain == before: True; full index (ls-files -s -z) == before: True; qa-factory state == before: True; HEAD == head_before: True

=== row 4 | class a_idx: A  ===
porcelain BEFORE:
'A  add8.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
person paths: ['add8.txt']
$ git write-tree   # G4
  exit=0
  stdout='d8d547edecdfca2e10ee0faa737fec6e817c5685'
  stderr=''
G5 add skipped: no entry has a worktree change (edge 5)
$ git commit -m 'QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' -- add8.txt   # G5 commit
  exit=0
  stdout='[master 830d310] QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]\n 1 file changed, 1 insertion(+)\n create mode 100644 add8.txt'
  stderr=''
porcelain AFTER commit:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
$ git diff --name-status -z b7e67ec0b5e988b1a02c342170e88f805bf3171e HEAD   # G12
  exit=0
  stdout=b'A\x00add8.txt\x00'
  stderr=''
G12 path set ['add8.txt'] == person paths: True; touches qa-factory: False
$ git rev-parse HEAD^   # G11 HEAD^
  exit=0
  stdout='b7e67ec0b5e988b1a02c342170e88f805bf3171e'
  stderr=''
HEAD^ == head_before: True; HEAD moved: True
person entries remaining after commit: []
$ git log --fixed-strings '--grep=QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' --format=%H -n 1   # G13
  exit=0
  stdout='830d31084ed83d08eeaf607036af392242b90464'
  stderr=''
$ git reset --soft b7e67ec0b5e9   # G7
  exit=0
  stdout=''
  stderr=''
$ git read-tree d8d547edecdfca2e10ee0faa737fec6e817c5685   # G6
  exit=0
  stdout=''
  stderr=''
porcelain AFTER undo (G7+G6):
'A  add8.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
undo: porcelain == before: True; full index (ls-files -s -z) == before: True; qa-factory state == before: True; HEAD == head_before: True

=== row 4 | class a_itd:  A (add -N) ===
porcelain BEFORE:
' A itd10.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
person paths: ['itd10.txt']
$ git write-tree   # G4
  exit=0
  stdout='ba3e7bb61e014cc4203a4f131270231dda6ff60f'
  stderr=''
$ git add -- itd10.txt   # G5 add: entries with Y != ' ' or ??
  exit=0
  stdout=''
  stderr=''
$ git commit -m 'QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' -- itd10.txt   # G5 commit
  exit=0
  stdout='[master 21c8b15] QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]\n 1 file changed, 1 insertion(+)\n create mode 100644 itd10.txt'
  stderr=''
porcelain AFTER commit:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
$ git diff --name-status -z 5469e2205b04594cfcad8a86f3fa51d57e90544b HEAD   # G12
  exit=0
  stdout=b'A\x00itd10.txt\x00'
  stderr=''
G12 path set ['itd10.txt'] == person paths: True; touches qa-factory: False
$ git rev-parse HEAD^   # G11 HEAD^
  exit=0
  stdout='5469e2205b04594cfcad8a86f3fa51d57e90544b'
  stderr=''
HEAD^ == head_before: True; HEAD moved: True
person entries remaining after commit: []
$ git log --fixed-strings '--grep=QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' --format=%H -n 1   # G13
  exit=0
  stdout='21c8b15f9fa72899df97a49b75dcc413bfe5329d'
  stderr=''
$ git reset --soft 5469e2205b04   # G7
  exit=0
  stdout=''
  stderr=''
$ git read-tree ba3e7bb61e014cc4203a4f131270231dda6ff60f   # G6
  exit=0
  stdout=''
  stderr=''
porcelain AFTER undo (G7+G6):
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? itd10.txt
?? qa-factory/new.txt'
undo: porcelain == before: False; full index (ls-files -s -z) == before: False; qa-factory state == before: True; HEAD == head_before: True

=== row 4 | class r_idx: R  (both sides outside) ===
porcelain BEFORE:
'R  old9.txt -> new9.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
person paths: ['new9.txt', 'old9.txt']
$ git write-tree   # G4
  exit=0
  stdout='0fef72c62cf569dc071f439d06404f50d2224234'
  stderr=''
G5 add skipped: no entry has a worktree change (edge 5)
$ git commit -m 'QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' -- new9.txt old9.txt   # G5 commit
  exit=0
  stdout='[master 3299c5b] QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]\n 1 file changed, 0 insertions(+), 0 deletions(-)\n rename old9.txt => new9.txt (100%)'
  stderr=''
porcelain AFTER commit:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
$ git diff --name-status -z 7eecf86210526676def76b1be74fdb36fee293c8 HEAD   # G12
  exit=0
  stdout=b'R100\x00old9.txt\x00new9.txt\x00'
  stderr=''
G12 path set ['new9.txt', 'old9.txt'] == person paths: True; touches qa-factory: False
$ git rev-parse HEAD^   # G11 HEAD^
  exit=0
  stdout='7eecf86210526676def76b1be74fdb36fee293c8'
  stderr=''
HEAD^ == head_before: True; HEAD moved: True
person entries remaining after commit: []
$ git log --fixed-strings '--grep=QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' --format=%H -n 1   # G13
  exit=0
  stdout='3299c5b2fecc50b74b7e4b30ed75eb6024aa85ac'
  stderr=''
$ git reset --soft 7eecf8621052   # G7
  exit=0
  stdout=''
  stderr=''
$ git read-tree 0fef72c62cf569dc071f439d06404f50d2224234   # G6
  exit=0
  stdout=''
  stderr=''
porcelain AFTER undo (G7+G6):
'R  old9.txt -> new9.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
undo: porcelain == before: True; full index (ls-files -s -z) == before: True; qa-factory state == before: True; HEAD == head_before: True

=== row 4 | class space: space in path ===
porcelain BEFORE:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? "a b.txt"
?? qa-factory/new.txt'
person paths: ['a b.txt']
$ git write-tree   # G4
  exit=0
  stdout='ba3e7bb61e014cc4203a4f131270231dda6ff60f'
  stderr=''
$ git add -- 'a b.txt'   # G5 add: entries with Y != ' ' or ??
  exit=0
  stdout=''
  stderr=''
$ git commit -m 'QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' -- 'a b.txt'   # G5 commit
  exit=0
  stdout='[master 4d766be] QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]\n 1 file changed, 1 insertion(+)\n create mode 100644 a b.txt'
  stderr=''
porcelain AFTER commit:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
$ git diff --name-status -z afd287d5093734f89e9b982dd17fb5af602f9dee HEAD   # G12
  exit=0
  stdout=b'A\x00a b.txt\x00'
  stderr=''
G12 path set ['a b.txt'] == person paths: True; touches qa-factory: False
$ git rev-parse HEAD^   # G11 HEAD^
  exit=0
  stdout='afd287d5093734f89e9b982dd17fb5af602f9dee'
  stderr=''
HEAD^ == head_before: True; HEAD moved: True
person entries remaining after commit: []
$ git log --fixed-strings '--grep=QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' --format=%H -n 1   # G13
  exit=0
  stdout='4d766be5cf2eb45806d539c09dae336db03f7b8a'
  stderr=''
$ git reset --soft afd287d50937   # G7
  exit=0
  stdout=''
  stderr=''
$ git read-tree ba3e7bb61e014cc4203a4f131270231dda6ff60f   # G6
  exit=0
  stdout=''
  stderr=''
porcelain AFTER undo (G7+G6):
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? "a b.txt"
?? qa-factory/new.txt'
undo: porcelain == before: True; full index (ls-files -s -z) == before: True; qa-factory state == before: True; HEAD == head_before: True

=== row 4 | class nonascii: non-ASCII paths (e-acute, CJK) ===
porcelain BEFORE:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? "caf\\303\\251.txt"
?? qa-factory/new.txt
?? "\\344\\270\\255\\346\\226\\207.txt"'
person paths: ['caf\xe9.txt', '\u4e2d\u6587.txt']
$ git write-tree   # G4
  exit=0
  stdout='ba3e7bb61e014cc4203a4f131270231dda6ff60f'
  stderr=''
$ git add -- 'caf\xe9.txt' '\u4e2d\u6587.txt'   # G5 add: entries with Y != ' ' or ??
  exit=0
  stdout=''
  stderr=''
$ git commit -m 'QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' -- 'caf\xe9.txt' '\u4e2d\u6587.txt'   # G5 commit
  exit=0
  stdout='[master 8a52249] QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]\n 2 files changed, 2 insertions(+)\n create mode 100644 "caf\\303\\251.txt"\n create mode 100644 "\\344\\270\\255\\346\\226\\207.txt"'
  stderr=''
porcelain AFTER commit:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
$ git diff --name-status -z 7b48ee5a029ad91db64319aae7d2a3a2485d1375 HEAD   # G12
  exit=0
  stdout=b'A\x00caf\xc3\xa9.txt\x00A\x00\xe4\xb8\xad\xe6\x96\x87.txt\x00'
  stderr=''
G12 path set ['caf\xe9.txt', '\u4e2d\u6587.txt'] == person paths: True; touches qa-factory: False
$ git rev-parse HEAD^   # G11 HEAD^
  exit=0
  stdout='7b48ee5a029ad91db64319aae7d2a3a2485d1375'
  stderr=''
HEAD^ == head_before: True; HEAD moved: True
person entries remaining after commit: []
$ git log --fixed-strings '--grep=QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' --format=%H -n 1   # G13
  exit=0
  stdout='8a52249250c912e61a8d541e408daf945a1d13ee'
  stderr=''
$ git reset --soft 7b48ee5a029a   # G7
  exit=0
  stdout=''
  stderr=''
$ git read-tree ba3e7bb61e014cc4203a4f131270231dda6ff60f   # G6
  exit=0
  stdout=''
  stderr=''
porcelain AFTER undo (G7+G6):
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? "caf\\303\\251.txt"
?? qa-factory/new.txt
?? "\\344\\270\\255\\346\\226\\207.txt"'
undo: porcelain == before: True; full index (ls-files -s -z) == before: True; qa-factory state == before: True; HEAD == head_before: True

=== row 4 | class sub:  M submodule pointer ===
porcelain BEFORE:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
 M sub12
?? qa-factory/new.txt'
person paths: ['sub12']
$ git write-tree   # G4
  exit=0
  stdout='0db4f98ba35687a03bcfb371d856af77a4329906'
  stderr=''
$ git add -- sub12   # G5 add: entries with Y != ' ' or ??
  exit=0
  stdout=''
  stderr=''
$ git commit -m 'QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' -- sub12   # G5 commit
  exit=0
  stdout='[master c052ef4] QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]\n 1 file changed, 1 insertion(+), 1 deletion(-)'
  stderr=''
porcelain AFTER commit:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
$ git diff --name-status -z d8e66904b09e9d9ebb5409fc1eb766ec6a8c430a HEAD   # G12
  exit=0
  stdout=b'M\x00sub12\x00'
  stderr=''
G12 path set ['sub12'] == person paths: True; touches qa-factory: False
$ git rev-parse HEAD^   # G11 HEAD^
  exit=0
  stdout='d8e66904b09e9d9ebb5409fc1eb766ec6a8c430a'
  stderr=''
HEAD^ == head_before: True; HEAD moved: True
person entries remaining after commit: []
$ git log --fixed-strings '--grep=QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' --format=%H -n 1   # G13
  exit=0
  stdout='c052ef48c8d43daaa3ee0da5ff7a15f817404dd5'
  stderr=''
$ git reset --soft d8e66904b09e   # G7
  exit=0
  stdout=''
  stderr=''
$ git read-tree 0db4f98ba35687a03bcfb371d856af77a4329906   # G6
  exit=0
  stdout=''
  stderr=''
porcelain AFTER undo (G7+G6):
'A  qa-factory/staged.txt
 M qa-factory/x.txt
 M sub12
?? qa-factory/new.txt'
undo: porcelain == before: True; full index (ls-files -s -z) == before: True; qa-factory state == before: True; HEAD == head_before: True

=== row 4 | class nested: ?? nested git repository ===
porcelain BEFORE:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? nested/
?? qa-factory/new.txt'
BLOCKED by blocker rules of spec 3.7 (['nested repository: nested/']); not run

=== row 4 | class rn_qa: rename qa-factory/r.txt -> src/y.txt ===
porcelain BEFORE:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
R  qa-factory/r.txt -> src/y.txt
?? qa-factory/new.txt'
BLOCKED by blocker rules of spec 3.7 (['partial-home rename: src/y.txt']); not run

=== row 4 | class sub_added: A  new submodule ===
porcelain BEFORE:
'A  .gitmodules
A  qa-factory/staged.txt
 M qa-factory/x.txt
A  sub13
?? qa-factory/new.txt'
person paths: ['.gitmodules', 'sub13']
$ git write-tree   # G4
  exit=0
  stdout='93d1a6d701d7d28f624d529960738e33b402da8e'
  stderr=''
G5 add skipped: no entry has a worktree change (edge 5)
$ git commit -m 'QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' -- .gitmodules sub13   # G5 commit
  exit=0
  stdout='[master 52ccf07] QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]\n 2 files changed, 4 insertions(+)\n create mode 100644 .gitmodules\n create mode 160000 sub13'
  stderr=''
porcelain AFTER commit:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
$ git diff --name-status -z 7f47912964e1b206580d1021067ebc1b2dedb736 HEAD   # G12
  exit=0
  stdout=b'A\x00.gitmodules\x00A\x00sub13\x00'
  stderr=''
G12 path set ['.gitmodules', 'sub13'] == person paths: True; touches qa-factory: False
$ git rev-parse HEAD^   # G11 HEAD^
  exit=0
  stdout='7f47912964e1b206580d1021067ebc1b2dedb736'
  stderr=''
HEAD^ == head_before: True; HEAD moved: True
person entries remaining after commit: []
$ git log --fixed-strings '--grep=QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' --format=%H -n 1   # G13
  exit=0
  stdout='52ccf07047c5897935efee533c1c8907b361f94c'
  stderr=''
$ git reset --soft 7f47912964e1   # G7
  exit=0
  stdout=''
  stderr=''
$ git read-tree 93d1a6d701d7d28f624d529960738e33b402da8e   # G6
  exit=0
  stdout=''
  stderr=''
porcelain AFTER undo (G7+G6):
'A  .gitmodules
A  qa-factory/staged.txt
 M qa-factory/x.txt
A  sub13
?? qa-factory/new.txt'
undo: porcelain == before: True; full index (ls-files -s -z) == before: True; qa-factory state == before: True; HEAD == head_before: True

=== row 4 | MIXED: all non-blocked classes in one tree ===
porcelain BEFORE:
'A  add8.txt
 D del6.txt
D  del7.txt
 A itd10.txt
 M m3.txt
M  m4.txt
MM m5.txt
R  old9.txt -> new9.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
 M sub12
?? "a b.txt"
?? "caf\\303\\251.txt"
?? d2/
?? qa-factory/new.txt
?? u1.txt
?? "\\344\\270\\255\\346\\226\\207.txt"'
person paths: ['add8.txt', 'del6.txt', 'del7.txt', 'itd10.txt', 'm3.txt', 'm4.txt', 'm5.txt', 'new9.txt', 'old9.txt', 'sub12', 'a b.txt', 'caf\xe9.txt', 'd2/a.txt', 'd2/b.txt', 'u1.txt', '\u4e2d\u6587.txt']
$ git write-tree   # G4
  exit=0
  stdout='669b2e018fc6aab4a4235f7ea9aebea6981fe6a3'
  stderr=''
$ git add -- del6.txt itd10.txt m3.txt m5.txt sub12 'a b.txt' 'caf\xe9.txt' d2/a.txt d2/b.txt u1.txt '\u4e2d\u6587.txt'   # G5 add: entries with Y != ' ' or ??
  exit=0
  stdout=''
  stderr=''
$ git commit -m 'QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' -- add8.txt del6.txt del7.txt itd10.txt m3.txt m4.txt m5.txt new9.txt old9.txt sub12 'a b.txt' 'caf\xe9.txt' d2/a.txt d2/b.txt u1.txt '\u4e2d\u6587.txt'   # G5 commit
  exit=0
  stdout='[master eeffaa4] QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]\n 15 files changed, 12 insertions(+), 7 deletions(-)\n create mode 100644 a b.txt\n create mode 100644 add8.txt\n create mode 100644 "caf\\303\\251.txt"\n create mode 100644 d2/a.txt\n create mode 100644 d2/b.txt\n delete mode 100644 del6.txt\n delete mode 100644 del7.txt\n create mode 100644 itd10.txt\n rename old9.txt => new9.txt (100%)\n create mode 100644 u1.txt\n create mode 100644 "\\344\\270\\255\\346\\226\\207.txt"'
  stderr=''
porcelain AFTER commit:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
$ git diff --name-status -z 5c2113986f9b628eb8f53a22ef25b0d719169204 HEAD   # G12
  exit=0
  stdout=b'A\x00a b.txt\x00A\x00add8.txt\x00A\x00caf\xc3\xa9.txt\x00A\x00d2/a.txt\x00A\x00d2/b.txt\x00D\x00del6.txt\x00D\x00del7.txt\x00A\x00itd10.txt\x00M\x00m3.txt\x00M\x00m4.txt\x00M\x00m5.txt\x00R100\x00old9.txt\x00new9.txt\x00M\x00sub12\x00A\x00u1.txt\x00A\x00\xe4\xb8\xad\xe6\x96\x87.txt\x00'
  stderr=''
G12 path set ['a b.txt', 'add8.txt', 'caf\xe9.txt', 'd2/a.txt', 'd2/b.txt', 'del6.txt', 'del7.txt', 'itd10.txt', 'm3.txt', 'm4.txt', 'm5.txt', 'new9.txt', 'old9.txt', 'sub12', 'u1.txt', '\u4e2d\u6587.txt'] == person paths: True; touches qa-factory: False
$ git rev-parse HEAD^   # G11 HEAD^
  exit=0
  stdout='5c2113986f9b628eb8f53a22ef25b0d719169204'
  stderr=''
HEAD^ == head_before: True; HEAD moved: True
person entries remaining after commit: []
$ git log --fixed-strings '--grep=QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' --format=%H -n 1   # G13
  exit=0
  stdout='eeffaa440eaa74c792455e9e295c271a0790d7c4'
  stderr=''
$ git reset --soft 5c2113986f9b   # G7
  exit=0
  stdout=''
  stderr=''
$ git read-tree 669b2e018fc6aab4a4235f7ea9aebea6981fe6a3   # G6
  exit=0
  stdout=''
  stderr=''
porcelain AFTER undo (G7+G6):
'A  add8.txt
 D del6.txt
D  del7.txt
 M m3.txt
M  m4.txt
MM m5.txt
R  old9.txt -> new9.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
 M sub12
?? "a b.txt"
?? "caf\\303\\251.txt"
?? d2/
?? itd10.txt
?? qa-factory/new.txt
?? u1.txt
?? "\\344\\270\\255\\346\\226\\207.txt"'
undo: porcelain == before: False; full index (ls-files -s -z) == before: False; qa-factory state == before: True; HEAD == head_before: True; git show :m5.txt before='staged' after-undo='staged'

##### ROW 5: pre-commit hook exits 1

=== row 5 | hook exit 1, mm ===
porcelain BEFORE:
'MM m5.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
person paths: ['m5.txt']
$ git write-tree   # G4
  exit=0
  stdout='14ce1a6a0caabce2eabebbc764e1675b550132d6'
  stderr=''
$ git add -- m5.txt   # G5 add: entries with Y != ' ' or ??
  exit=0
  stdout=''
  stderr=''
$ git commit -m 'QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' -- m5.txt   # G5 commit
  exit=1
  stdout=''
  stderr='hook: refused'
porcelain AFTER commit:
'M  m5.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
commit failed rc=1; HEAD moved=False; qa untouched=True; porcelain == before (index state after add differs?): False
$ git read-tree 14ce1a6a0caabce2eabebbc764e1675b550132d6   # G6 restore after failure
  exit=0
  stdout=''
  stderr=''
porcelain AFTER G6:
'MM m5.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
restore: porcelain == before: True; full index == before: True; qa state == before: True; git show :m5.txt before='staged' after-G6='staged'

=== row 5 | hook exit 1, allok ===
porcelain BEFORE:
'A  add8.txt
 D del6.txt
D  del7.txt
 A itd10.txt
 M m3.txt
M  m4.txt
MM m5.txt
R  old9.txt -> new9.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
 M sub12
?? "a b.txt"
?? "caf\\303\\251.txt"
?? d2/
?? qa-factory/new.txt
?? u1.txt
?? "\\344\\270\\255\\346\\226\\207.txt"'
person paths: ['add8.txt', 'del6.txt', 'del7.txt', 'itd10.txt', 'm3.txt', 'm4.txt', 'm5.txt', 'new9.txt', 'old9.txt', 'sub12', 'a b.txt', 'caf\xe9.txt', 'd2/a.txt', 'd2/b.txt', 'u1.txt', '\u4e2d\u6587.txt']
$ git write-tree   # G4
  exit=0
  stdout='d2222d86a8ae3f2f93fad50666972bb058ba30ad'
  stderr=''
$ git add -- del6.txt itd10.txt m3.txt m5.txt sub12 'a b.txt' 'caf\xe9.txt' d2/a.txt d2/b.txt u1.txt '\u4e2d\u6587.txt'   # G5 add: entries with Y != ' ' or ??
  exit=0
  stdout=''
  stderr=''
$ git commit -m 'QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' -- add8.txt del6.txt del7.txt itd10.txt m3.txt m4.txt m5.txt new9.txt old9.txt sub12 'a b.txt' 'caf\xe9.txt' d2/a.txt d2/b.txt u1.txt '\u4e2d\u6587.txt'   # G5 commit
  exit=1
  stdout=''
  stderr='hook: refused'
porcelain AFTER commit:
'A  "a b.txt"
A  add8.txt
A  "caf\\303\\251.txt"
A  d2/a.txt
A  d2/b.txt
D  del6.txt
D  del7.txt
A  itd10.txt
M  m3.txt
M  m4.txt
M  m5.txt
R  old9.txt -> new9.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
M  sub12
A  u1.txt
A  "\\344\\270\\255\\346\\226\\207.txt"
?? qa-factory/new.txt'
commit failed rc=1; HEAD moved=False; qa untouched=True; porcelain == before (index state after add differs?): False
$ git read-tree d2222d86a8ae3f2f93fad50666972bb058ba30ad   # G6 restore after failure
  exit=0
  stdout=''
  stderr=''
porcelain AFTER G6:
'A  add8.txt
 D del6.txt
D  del7.txt
 M m3.txt
M  m4.txt
MM m5.txt
R  old9.txt -> new9.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
 M sub12
?? "a b.txt"
?? "caf\\303\\251.txt"
?? d2/
?? itd10.txt
?? qa-factory/new.txt
?? u1.txt
?? "\\344\\270\\255\\346\\226\\207.txt"'
restore: porcelain == before: False; full index == before: False; qa state == before: True; git show :m5.txt before='staged' after-G6='staged'

##### ROW 6: hooks that change files

=== row 6a | hook rewrites a listed file (appends to m3.txt and u1.txt in the work tree) and does not touch the index ===
porcelain BEFORE:
' M m3.txt
MM m5.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt
?? u1.txt'
person paths: ['m3.txt', 'm5.txt', 'u1.txt']
$ git write-tree   # G4
  exit=0
  stdout='f205394bd55c36a10f7aeb719ffac992c3cec3d4'
  stderr=''
$ git add -- m3.txt m5.txt u1.txt   # G5 add: entries with Y != ' ' or ??
  exit=0
  stdout=''
  stderr=''
$ git commit -m 'QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' -- m3.txt m5.txt u1.txt   # G5 commit
  exit=0
  stdout='[master 795abc0] QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]\n 3 files changed, 3 insertions(+), 2 deletions(-)\n create mode 100644 u1.txt'
  stderr=''
porcelain AFTER commit:
' M m3.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
 M u1.txt
?? qa-factory/new.txt'
$ git diff --name-status -z 375303aa06353607fd5796d2702eea8a812fea84 HEAD   # G12
  exit=0
  stdout=b'M\x00m3.txt\x00M\x00m5.txt\x00A\x00u1.txt\x00'
  stderr=''
G12 path set ['m3.txt', 'm5.txt', 'u1.txt'] == person paths: True; touches qa-factory: False
$ git rev-parse HEAD^   # G11 HEAD^
  exit=0
  stdout='375303aa06353607fd5796d2702eea8a812fea84'
  stderr=''
HEAD^ == head_before: True; HEAD moved: True
person entries remaining after commit: ['m3.txt', 'u1.txt']
$ git log --fixed-strings '--grep=QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' --format=%H -n 1   # G13
  exit=0
  stdout='795abc023b72e3ad0b8401c36546cee12bf31746'
  stderr=''
$ git reset --soft 375303aa0635   # G7
  exit=0
  stdout=''
  stderr=''
$ git read-tree f205394bd55c36a10f7aeb719ffac992c3cec3d4   # G6
  exit=0
  stdout=''
  stderr=''
porcelain AFTER undo (G7+G6):
' M m3.txt
MM m5.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt
?? u1.txt'
undo: porcelain == before: True; full index (ls-files -s -z) == before: True; qa-factory state == before: True; HEAD == head_before: True; git show :m5.txt before='staged' after-undo='staged'

=== row 6b | hook rewrites a listed file AND re-adds it (git add m3.txt) ===
porcelain BEFORE:
' M m3.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt
?? u1.txt'
person paths: ['m3.txt', 'u1.txt']
$ git write-tree   # G4
  exit=0
  stdout='f74d8e874a59d2c315808522601e0fda9d5c8edc'
  stderr=''
$ git add -- m3.txt u1.txt   # G5 add: entries with Y != ' ' or ??
  exit=0
  stdout=''
  stderr=''
$ git commit -m 'QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' -- m3.txt u1.txt   # G5 commit
  exit=0
  stdout='[master 55352b9] QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]\n 2 files changed, 3 insertions(+), 1 deletion(-)\n create mode 100644 u1.txt'
  stderr=''
porcelain AFTER commit:
'MM m3.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
$ git diff --name-status -z a2b1728306ba3d168505607e06534f3286653d73 HEAD   # G12
  exit=0
  stdout=b'M\x00m3.txt\x00A\x00u1.txt\x00'
  stderr=''
G12 path set ['m3.txt', 'u1.txt'] == person paths: True; touches qa-factory: False
$ git rev-parse HEAD^   # G11 HEAD^
  exit=0
  stdout='a2b1728306ba3d168505607e06534f3286653d73'
  stderr=''
HEAD^ == head_before: True; HEAD moved: True
person entries remaining after commit: ['m3.txt']
$ git log --fixed-strings '--grep=QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' --format=%H -n 1   # G13
  exit=0
  stdout='55352b91b97022ca768b52884cf8a1231e8b3179'
  stderr=''
$ git reset --soft a2b1728306ba   # G7
  exit=0
  stdout=''
  stderr=''
$ git read-tree f74d8e874a59d2c315808522601e0fda9d5c8edc   # G6
  exit=0
  stdout=''
  stderr=''
porcelain AFTER undo (G7+G6):
' M m3.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt
?? u1.txt'
undo: porcelain == before: True; full index (ls-files -s -z) == before: True; qa-factory state == before: True; HEAD == head_before: True

=== row 6c | hook creates a new untracked file ===
porcelain BEFORE:
' M m3.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt
?? u1.txt'
person paths: ['m3.txt', 'u1.txt']
$ git write-tree   # G4
  exit=0
  stdout='f74d8e874a59d2c315808522601e0fda9d5c8edc'
  stderr=''
$ git add -- m3.txt u1.txt   # G5 add: entries with Y != ' ' or ??
  exit=0
  stdout=''
  stderr=''
$ git commit -m 'QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' -- m3.txt u1.txt   # G5 commit
  exit=0
  stdout='[master e64575e] QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]\n 2 files changed, 2 insertions(+), 1 deletion(-)\n create mode 100644 u1.txt'
  stderr=''
porcelain AFTER commit:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? hook-new.txt
?? qa-factory/new.txt'
$ git diff --name-status -z ddc6b9307b6c65a65f2ca10128b4f25feaaf7940 HEAD   # G12
  exit=0
  stdout=b'M\x00m3.txt\x00A\x00u1.txt\x00'
  stderr=''
G12 path set ['m3.txt', 'u1.txt'] == person paths: True; touches qa-factory: False
$ git rev-parse HEAD^   # G11 HEAD^
  exit=0
  stdout='ddc6b9307b6c65a65f2ca10128b4f25feaaf7940'
  stderr=''
HEAD^ == head_before: True; HEAD moved: True
person entries remaining after commit: ['hook-new.txt']
$ git log --fixed-strings '--grep=QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' --format=%H -n 1   # G13
  exit=0
  stdout='e64575e6315406d48b18d1faca0f4f1378019a5e'
  stderr=''
$ git reset --soft ddc6b9307b6c   # G7
  exit=0
  stdout=''
  stderr=''
$ git read-tree f74d8e874a59d2c315808522601e0fda9d5c8edc   # G6
  exit=0
  stdout=''
  stderr=''
porcelain AFTER undo (G7+G6):
' M m3.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? hook-new.txt
?? qa-factory/new.txt
?? u1.txt'
undo: porcelain == before: False; full index (ls-files -s -z) == before: True; qa-factory state == before: True; HEAD == head_before: True
-- hook-rewrite: repo state after the flow (undo already ran in the flow; shown for the record)
porcelain hook-rewrite final:
' M m3.txt
MM m5.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt
?? u1.txt'
-- hook-rewrite-add: repo state after the flow (undo already ran in the flow; shown for the record)
porcelain hook-rewrite-add final:
' M m3.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt
?? u1.txt'
-- hook-newfile: repo state after the flow (undo already ran in the flow; shown for the record)
porcelain hook-newfile final:
' M m3.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? hook-new.txt
?? qa-factory/new.txt
?? u1.txt'

##### ROW 7: pre-commit hook sleeping 200 s; subprocess.run(timeout=5) (stdout/stderr to files, not pipes, so run() does not wait for the orphaned hook)

=== row 7 | G5 commit with timeout ===
$ git write-tree   # G4
  exit=0
  stdout='14ce1a6a0caabce2eabebbc764e1675b550132d6'
  stderr=''
$ git add -- m5.txt u1.txt   # G5 add
  exit=0
  stdout=''
  stderr=''
TimeoutExpired after 5.0s; run() killed the git process it started
-- snapshot right after the timeout: HEAD=a55eb041840f (before a55eb041840f, moved=False); lock files in .git: ['.git/index.lock', '.git/next-index-9316.lock']; index.lock exists=True; hook winpid file='26324'; hook shell alive=True
   scratch-related git/sh/sleep processes: [(1692, 25448, 'bash.exe', '"C:\\Program Files\\Git\\bin\\bash.exe" -c "source /c/Users/i_mas/.claude/shell-snapshots/snapshot-bash-1794478599150-q85ezr.sh 2>/dev/null || t'), (24764, 1692, 'bash.exe', '"C:\\Program Files\\Git\\bin\\..\\usr\\bin\\bash.exe" -c "source /c/Users/i_mas/.claude/shell-snapshots/snapshot-bash-1794478599150-q85ezr.sh 2>/de'), (9316, 16968, 'git.exe', 'git.exe -C C:\\Users\\i_mas\\AppData\\Local\\Temp\\claude\\b3e3188b390a00d9\\f92520fc-f552-4e47-9d06-efbc3daae572\\scratchpad\\b0-2\\repos\\r7 commit -m'), (26324, 9316, 'sh.exe', 'sh .git/hooks/pre-commit')]
porcelain right after the timeout:
'M  m5.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
A  u1.txt
?? qa-factory/new.txt'
-- snapshot 10 s later: HEAD=a55eb041840f (before a55eb041840f, moved=False); lock files in .git: ['.git/index.lock', '.git/next-index-9316.lock']; index.lock exists=True; hook winpid file='26324'; hook shell alive=True
   scratch-related git/sh/sleep processes: [(1692, 25448, 'bash.exe', '"C:\\Program Files\\Git\\bin\\bash.exe" -c "source /c/Users/i_mas/.claude/shell-snapshots/snapshot-bash-1794478599150-q85ezr.sh 2>/dev/null || t'), (24764, 1692, 'bash.exe', '"C:\\Program Files\\Git\\bin\\..\\usr\\bin\\bash.exe" -c "source /c/Users/i_mas/.claude/shell-snapshots/snapshot-bash-1794478599150-q85ezr.sh 2>/de'), (9316, 16968, 'git.exe', 'git.exe -C C:\\Users\\i_mas\\AppData\\Local\\Temp\\claude\\b3e3188b390a00d9\\f92520fc-f552-4e47-9d06-efbc3daae572\\scratchpad\\b0-2\\repos\\r7 commit -m'), (26324, 9316, 'sh.exe', 'sh .git/hooks/pre-commit')]
$ git read-tree 14ce1a6a0caabce2eabebbc764e1675b550132d6   # G6 while the lock / orphaned hook are still there
  exit=128
  stdout=''
  stderr="fatal: Unable to create 'C:/Users/i_mas/AppData/Local/Temp/claude/b3e3188b390a00d9/f92520fc-f552-4e47-9d06-efbc3daae572/scratchpad/b0-2/repos/r7/.git/index.lock': File exists.\n\nAnother git process seems to be running in this repository, or the lock file may be stale"
   taskkill /F /T /PID 26324: exit=0 'SUCCESS: The process with PID 26324 (child process of PID 9316) has been terminated.' ''
-- snapshot after killing the hook's tree (pid read from its own file): HEAD=a55eb041840f (before a55eb041840f, moved=False); lock files in .git: []; index.lock exists=False; hook winpid file='26324'; hook shell alive=False
   scratch-related git/sh/sleep processes: [(1692, 25448, 'bash.exe', '"C:\\Program Files\\Git\\bin\\bash.exe" -c "source /c/Users/i_mas/.claude/shell-snapshots/snapshot-bash-1794478599150-q85ezr.sh 2>/dev/null || t'), (24764, 1692, 'bash.exe', '"C:\\Program Files\\Git\\bin\\..\\usr\\bin\\bash.exe" -c "source /c/Users/i_mas/.claude/shell-snapshots/snapshot-bash-1794478599150-q85ezr.sh 2>/de')]
   leftover scratch process, killing by pid: (1692, 'bash.exe')
   taskkill /F /T /PID 1692: exit=0 'SUCCESS: The process with PID 10488 (child process of PID 24764) has been terminated.\r\nSUCCESS: The process with PID 24764 (child process of PID 1692) has been terminated.\r\nSUCCESS: The process with PID 1692 (child process of PID 25448) has been terminated.' ''
   leftover scratch process, killing by pid: (24764, 'bash.exe')
   taskkill /F /T /PID 24764: exit=128 '' 'ERROR: The process "24764" not found.'
index.lock still exists after every process is gone: False
$ git read-tree 14ce1a6a0caabce2eabebbc764e1675b550132d6   # G6 with the stale lock (no process left)
  exit=0
  stdout=''
  stderr=''
   (scratch only: removed .git/index.lock by hand; the factory never deletes it)
$ git read-tree 14ce1a6a0caabce2eabebbc764e1675b550132d6   # G6 after removing the lock
  exit=0
  stdout=''
  stderr=''
porcelain after G6:
'MM m5.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt
?? u1.txt'
porcelain == before: True; index == before: True; HEAD == head_before: True

##### ROW 8: G8 with the stash message, G9, G10 (apply --index by sha12, drop by sha12)

=== row 8 | class u_file: ?? file ===
porcelain BEFORE:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt
?? u1.txt'
$ git rev-parse -q --verify refs/stash   # G9 before
  exit=1
  stdout=''
  stderr=''
$ git stash push --include-untracked -m 'QA Factory story t-118: your uncommitted changes, put aside before the tests' -- u1.txt   # G8
  exit=0
  stdout='Saved working directory and index state On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git rev-parse -q --verify refs/stash   # G9 after
  exit=0
  stdout='6f637506b936148f630f85bfa10eeee37f72c7e9'
  stderr=''
porcelain AFTER stash:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
person entries remaining: []; qa-factory untouched: True
$ git log -1 --format=%s 6f637506b936148f630f85bfa10eeee37f72c7e9   # G9 subject
  exit=0
  stdout='On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git stash list '--format=%H %gd %s'   # G10 list
  exit=0
  stdout='6f637506b936148f630f85bfa10eeee37f72c7e9 stash@{0} On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git stash apply --index 6f637506b936   # G10 apply by sha12
  exit=0
  stdout='On branch master\nChanges to be committed:\n  (use "git restore --staged <file>..." to unstage)\n\tnew file:   qa-factory/staged.txt\n\nChanges not staged for commit:\n  (use "git add <file>..." to update what will be committed)\n  (use "git restore <file>..." to discard changes in working directory)\n\tmodified:   qa-factory/x.txt\n\nUntracked files:\n  (use "git add <file>..." to include in what will be committed)\n\tqa-factory/new.txt\n\tu1.txt'
  stderr=''
porcelain AFTER apply --index:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt
?? u1.txt'
after apply --index: porcelain == before: True; full index == before: True; qa untouched: True
$ git stash drop 6f637506b936   # G10 drop by sha12
  exit=128
  stdout=''
  stderr="error: '6f637506b936' is not a stash reference"
$ git stash list '--format=%H %gd %s'   # G10 list after drop
  exit=0
  stdout='6f637506b936148f630f85bfa10eeee37f72c7e9 stash@{0} On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git rev-parse -q --verify refs/stash   # G9 after drop
  exit=0
  stdout='6f637506b936148f630f85bfa10eeee37f72c7e9'
  stderr=''

=== row 8 | class u_dir: ?? folder with two files ===
porcelain BEFORE:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? d2/
?? qa-factory/new.txt'
$ git rev-parse -q --verify refs/stash   # G9 before
  exit=1
  stdout=''
  stderr=''
$ git stash push --include-untracked -m 'QA Factory story t-118: your uncommitted changes, put aside before the tests' -- d2/a.txt d2/b.txt   # G8
  exit=0
  stdout='Saved working directory and index state On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git rev-parse -q --verify refs/stash   # G9 after
  exit=0
  stdout='451ade64f8001e6a6e59eb6c71e28f3ff3ce176e'
  stderr=''
porcelain AFTER stash:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
person entries remaining: []; qa-factory untouched: True
$ git log -1 --format=%s 451ade64f8001e6a6e59eb6c71e28f3ff3ce176e   # G9 subject
  exit=0
  stdout='On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git stash list '--format=%H %gd %s'   # G10 list
  exit=0
  stdout='451ade64f8001e6a6e59eb6c71e28f3ff3ce176e stash@{0} On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git stash apply --index 451ade64f800   # G10 apply by sha12
  exit=0
  stdout='On branch master\nChanges to be committed:\n  (use "git restore --staged <file>..." to unstage)\n\tnew file:   qa-factory/staged.txt\n\nChanges not staged for commit:\n  (use "git add <file>..." to update what will be committed)\n  (use "git restore <file>..." to discard changes in working directory)\n\tmodified:   qa-factory/x.txt\n\nUntracked files:\n  (use "git add <file>..." to include in what will be committed)\n\td2/\n\tqa-factory/new.txt'
  stderr=''
porcelain AFTER apply --index:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? d2/
?? qa-factory/new.txt'
after apply --index: porcelain == before: True; full index == before: True; qa untouched: True
$ git stash drop 451ade64f800   # G10 drop by sha12
  exit=128
  stdout=''
  stderr="error: '451ade64f800' is not a stash reference"
$ git stash list '--format=%H %gd %s'   # G10 list after drop
  exit=0
  stdout='451ade64f8001e6a6e59eb6c71e28f3ff3ce176e stash@{0} On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git rev-parse -q --verify refs/stash   # G9 after drop
  exit=0
  stdout='451ade64f8001e6a6e59eb6c71e28f3ff3ce176e'
  stderr=''

=== row 8 | class m_wt:  M ===
porcelain BEFORE:
' M m3.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
$ git rev-parse -q --verify refs/stash   # G9 before
  exit=1
  stdout=''
  stderr=''
$ git stash push --include-untracked -m 'QA Factory story t-118: your uncommitted changes, put aside before the tests' -- m3.txt   # G8
  exit=0
  stdout='Saved working directory and index state On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git rev-parse -q --verify refs/stash   # G9 after
  exit=0
  stdout='7dd828a8d7733229b2fc5166da5d73bcd73679da'
  stderr=''
porcelain AFTER stash:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
person entries remaining: []; qa-factory untouched: True
$ git log -1 --format=%s 7dd828a8d7733229b2fc5166da5d73bcd73679da   # G9 subject
  exit=0
  stdout='On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git stash list '--format=%H %gd %s'   # G10 list
  exit=0
  stdout='7dd828a8d7733229b2fc5166da5d73bcd73679da stash@{0} On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git stash apply --index 7dd828a8d773   # G10 apply by sha12
  exit=0
  stdout='On branch master\nChanges to be committed:\n  (use "git restore --staged <file>..." to unstage)\n\tnew file:   qa-factory/staged.txt\n\nChanges not staged for commit:\n  (use "git add <file>..." to update what will be committed)\n  (use "git restore <file>..." to discard changes in working directory)\n\tmodified:   m3.txt\n\tmodified:   qa-factory/x.txt\n\nUntracked files:\n  (use "git add <file>..." to include in what will be committed)\n\tqa-factory/new.txt'
  stderr=''
porcelain AFTER apply --index:
' M m3.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
after apply --index: porcelain == before: True; full index == before: True; qa untouched: True
$ git stash drop 7dd828a8d773   # G10 drop by sha12
  exit=128
  stdout=''
  stderr="error: '7dd828a8d773' is not a stash reference"
$ git stash list '--format=%H %gd %s'   # G10 list after drop
  exit=0
  stdout='7dd828a8d7733229b2fc5166da5d73bcd73679da stash@{0} On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git rev-parse -q --verify refs/stash   # G9 after drop
  exit=0
  stdout='7dd828a8d7733229b2fc5166da5d73bcd73679da'
  stderr=''

=== row 8 | class m_idx: M  ===
porcelain BEFORE:
'M  m4.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
$ git rev-parse -q --verify refs/stash   # G9 before
  exit=1
  stdout=''
  stderr=''
$ git stash push --include-untracked -m 'QA Factory story t-118: your uncommitted changes, put aside before the tests' -- m4.txt   # G8
  exit=0
  stdout='Saved working directory and index state On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git rev-parse -q --verify refs/stash   # G9 after
  exit=0
  stdout='ee7cad4577d020569b052c2bec2355c6be6cdf4f'
  stderr=''
porcelain AFTER stash:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
person entries remaining: []; qa-factory untouched: True
$ git log -1 --format=%s ee7cad4577d020569b052c2bec2355c6be6cdf4f   # G9 subject
  exit=0
  stdout='On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git stash list '--format=%H %gd %s'   # G10 list
  exit=0
  stdout='ee7cad4577d020569b052c2bec2355c6be6cdf4f stash@{0} On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git stash apply --index ee7cad4577d0   # G10 apply by sha12
  exit=128
  stdout=''
  stderr='error: qa-factory/staged.txt: already exists in index\nerror: conflicts in index. Try without --index.'
porcelain AFTER apply --index:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
after apply --index: porcelain == before: False; full index == before: False; qa untouched: True
$ git stash drop ee7cad4577d0   # G10 drop by sha12
  exit=128
  stdout=''
  stderr="error: 'ee7cad4577d0' is not a stash reference"
$ git stash list '--format=%H %gd %s'   # G10 list after drop
  exit=0
  stdout='ee7cad4577d020569b052c2bec2355c6be6cdf4f stash@{0} On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git rev-parse -q --verify refs/stash   # G9 after drop
  exit=0
  stdout='ee7cad4577d020569b052c2bec2355c6be6cdf4f'
  stderr=''

=== row 8 | class mm: MM ===
porcelain BEFORE:
'MM m5.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
$ git rev-parse -q --verify refs/stash   # G9 before
  exit=1
  stdout=''
  stderr=''
$ git stash push --include-untracked -m 'QA Factory story t-118: your uncommitted changes, put aside before the tests' -- m5.txt   # G8
  exit=0
  stdout='Saved working directory and index state On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git rev-parse -q --verify refs/stash   # G9 after
  exit=0
  stdout='89b46e41a63fd990e460222ee38c43a5c2bbba7f'
  stderr=''
porcelain AFTER stash:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
person entries remaining: []; qa-factory untouched: True
$ git log -1 --format=%s 89b46e41a63fd990e460222ee38c43a5c2bbba7f   # G9 subject
  exit=0
  stdout='On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git stash list '--format=%H %gd %s'   # G10 list
  exit=0
  stdout='89b46e41a63fd990e460222ee38c43a5c2bbba7f stash@{0} On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git stash apply --index 89b46e41a63f   # G10 apply by sha12
  exit=128
  stdout=''
  stderr='error: qa-factory/staged.txt: already exists in index\nerror: conflicts in index. Try without --index.'
porcelain AFTER apply --index:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
after apply --index: porcelain == before: False; full index == before: False; qa untouched: True
$ git stash drop 89b46e41a63f   # G10 drop by sha12
  exit=128
  stdout=''
  stderr="error: '89b46e41a63f' is not a stash reference"
$ git stash list '--format=%H %gd %s'   # G10 list after drop
  exit=0
  stdout='89b46e41a63fd990e460222ee38c43a5c2bbba7f stash@{0} On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git rev-parse -q --verify refs/stash   # G9 after drop
  exit=0
  stdout='89b46e41a63fd990e460222ee38c43a5c2bbba7f'
  stderr=''

=== row 8 | class d_wt:  D ===
porcelain BEFORE:
' D del6.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
$ git rev-parse -q --verify refs/stash   # G9 before
  exit=1
  stdout=''
  stderr=''
$ git stash push --include-untracked -m 'QA Factory story t-118: your uncommitted changes, put aside before the tests' -- del6.txt   # G8
  exit=0
  stdout='Saved working directory and index state On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git rev-parse -q --verify refs/stash   # G9 after
  exit=0
  stdout='969d00e5cbf9a1edcb0a9e113e7d5860b4bdc7d8'
  stderr=''
porcelain AFTER stash:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
person entries remaining: []; qa-factory untouched: True
$ git log -1 --format=%s 969d00e5cbf9a1edcb0a9e113e7d5860b4bdc7d8   # G9 subject
  exit=0
  stdout='On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git stash list '--format=%H %gd %s'   # G10 list
  exit=0
  stdout='969d00e5cbf9a1edcb0a9e113e7d5860b4bdc7d8 stash@{0} On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git stash apply --index 969d00e5cbf9   # G10 apply by sha12
  exit=0
  stdout='On branch master\nChanges to be committed:\n  (use "git restore --staged <file>..." to unstage)\n\tnew file:   qa-factory/staged.txt\n\nChanges not staged for commit:\n  (use "git add/rm <file>..." to update what will be committed)\n  (use "git restore <file>..." to discard changes in working directory)\n\tdeleted:    del6.txt\n\tmodified:   qa-factory/x.txt\n\nUntracked files:\n  (use "git add <file>..." to include in what will be committed)\n\tqa-factory/new.txt'
  stderr=''
porcelain AFTER apply --index:
' D del6.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
after apply --index: porcelain == before: True; full index == before: True; qa untouched: True
$ git stash drop 969d00e5cbf9   # G10 drop by sha12
  exit=128
  stdout=''
  stderr="error: '969d00e5cbf9' is not a stash reference"
$ git stash list '--format=%H %gd %s'   # G10 list after drop
  exit=0
  stdout='969d00e5cbf9a1edcb0a9e113e7d5860b4bdc7d8 stash@{0} On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git rev-parse -q --verify refs/stash   # G9 after drop
  exit=0
  stdout='969d00e5cbf9a1edcb0a9e113e7d5860b4bdc7d8'
  stderr=''

=== row 8 | class d_idx: D  ===
porcelain BEFORE:
'D  del7.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
$ git rev-parse -q --verify refs/stash   # G9 before
  exit=1
  stdout=''
  stderr=''
$ git stash push --include-untracked -m 'QA Factory story t-118: your uncommitted changes, put aside before the tests' -- del7.txt   # G8
  exit=128
  stdout='Saved working directory and index state On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr="fatal: pathspec ':(prefix:0)del7.txt' did not match any files"
$ git rev-parse -q --verify refs/stash   # G9 after
  exit=0
  stdout='255e0ff3d486a916d57ba8c087acd83d59a8ee6d'
  stderr=''
porcelain AFTER stash:
'D  del7.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
person entries remaining: ['del7.txt']; qa-factory untouched: True
$ git log -1 --format=%s 255e0ff3d486a916d57ba8c087acd83d59a8ee6d   # G9 subject
  exit=0
  stdout='On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git stash list '--format=%H %gd %s'   # G10 list
  exit=0
  stdout='255e0ff3d486a916d57ba8c087acd83d59a8ee6d stash@{0} On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git stash apply --index 255e0ff3d486   # G10 apply by sha12
  exit=0
  stdout='On branch master\nChanges to be committed:\n  (use "git restore --staged <file>..." to unstage)\n\tdeleted:    del7.txt\n\tnew file:   qa-factory/staged.txt\n\nChanges not staged for commit:\n  (use "git add <file>..." to update what will be committed)\n  (use "git restore <file>..." to discard changes in working directory)\n\tmodified:   qa-factory/x.txt\n\nUntracked files:\n  (use "git add <file>..." to include in what will be committed)\n\tqa-factory/new.txt'
  stderr=''
porcelain AFTER apply --index:
'D  del7.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
after apply --index: porcelain == before: True; full index == before: True; qa untouched: True
$ git stash drop 255e0ff3d486   # G10 drop by sha12
  exit=128
  stdout=''
  stderr="error: '255e0ff3d486' is not a stash reference"
$ git stash list '--format=%H %gd %s'   # G10 list after drop
  exit=0
  stdout='255e0ff3d486a916d57ba8c087acd83d59a8ee6d stash@{0} On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git rev-parse -q --verify refs/stash   # G9 after drop
  exit=0
  stdout='255e0ff3d486a916d57ba8c087acd83d59a8ee6d'
  stderr=''

=== row 8 | class a_idx: A  ===
porcelain BEFORE:
'A  add8.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
$ git rev-parse -q --verify refs/stash   # G9 before
  exit=1
  stdout=''
  stderr=''
$ git stash push --include-untracked -m 'QA Factory story t-118: your uncommitted changes, put aside before the tests' -- add8.txt   # G8
  exit=0
  stdout='Saved working directory and index state On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git rev-parse -q --verify refs/stash   # G9 after
  exit=0
  stdout='741565d0c3631c6c78f14b37311bdaf9e07b01fe'
  stderr=''
porcelain AFTER stash:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
person entries remaining: []; qa-factory untouched: True
$ git log -1 --format=%s 741565d0c3631c6c78f14b37311bdaf9e07b01fe   # G9 subject
  exit=0
  stdout='On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git stash list '--format=%H %gd %s'   # G10 list
  exit=0
  stdout='741565d0c3631c6c78f14b37311bdaf9e07b01fe stash@{0} On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git stash apply --index 741565d0c363   # G10 apply by sha12
  exit=128
  stdout=''
  stderr='error: qa-factory/staged.txt: already exists in index\nerror: conflicts in index. Try without --index.'
porcelain AFTER apply --index:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
after apply --index: porcelain == before: False; full index == before: False; qa untouched: True
$ git stash drop 741565d0c363   # G10 drop by sha12
  exit=128
  stdout=''
  stderr="error: '741565d0c363' is not a stash reference"
$ git stash list '--format=%H %gd %s'   # G10 list after drop
  exit=0
  stdout='741565d0c3631c6c78f14b37311bdaf9e07b01fe stash@{0} On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git rev-parse -q --verify refs/stash   # G9 after drop
  exit=0
  stdout='741565d0c3631c6c78f14b37311bdaf9e07b01fe'
  stderr=''

=== row 8 | class a_itd:  A (add -N) ===
porcelain BEFORE:
' A itd10.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
$ git rev-parse -q --verify refs/stash   # G9 before
  exit=1
  stdout=''
  stderr=''
$ git stash push --include-untracked -m 'QA Factory story t-118: your uncommitted changes, put aside before the tests' -- itd10.txt   # G8
  exit=128
  stdout=''
  stderr="error: Entry 'itd10.txt' not uptodate. Cannot merge.\nCannot save the current worktree state"
$ git rev-parse -q --verify refs/stash   # G9 after
  exit=1
  stdout=''
  stderr=''
porcelain AFTER stash:
' A itd10.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
person entries remaining: ['itd10.txt']; qa-factory untouched: True
no stash ref after the command

=== row 8 | class r_idx: R  (both sides outside) ===
porcelain BEFORE:
'R  old9.txt -> new9.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
$ git rev-parse -q --verify refs/stash   # G9 before
  exit=1
  stdout=''
  stderr=''
$ git stash push --include-untracked -m 'QA Factory story t-118: your uncommitted changes, put aside before the tests' -- new9.txt old9.txt   # G8
  exit=128
  stdout='Saved working directory and index state On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr="fatal: pathspec ':(prefix:0)old9.txt' did not match any files"
$ git rev-parse -q --verify refs/stash   # G9 after
  exit=0
  stdout='df569a63a3db4fd93aae0e03f15ee04d20b62b43'
  stderr=''
porcelain AFTER stash:
'R  old9.txt -> new9.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
person entries remaining: ['new9.txt']; qa-factory untouched: True
$ git log -1 --format=%s df569a63a3db4fd93aae0e03f15ee04d20b62b43   # G9 subject
  exit=0
  stdout='On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git stash list '--format=%H %gd %s'   # G10 list
  exit=0
  stdout='df569a63a3db4fd93aae0e03f15ee04d20b62b43 stash@{0} On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git stash apply --index df569a63a3db   # G10 apply by sha12
  exit=0
  stdout='On branch master\nChanges to be committed:\n  (use "git restore --staged <file>..." to unstage)\n\trenamed:    old9.txt -> new9.txt\n\tnew file:   qa-factory/staged.txt\n\nChanges not staged for commit:\n  (use "git add <file>..." to update what will be committed)\n  (use "git restore <file>..." to discard changes in working directory)\n\tmodified:   qa-factory/x.txt\n\nUntracked files:\n  (use "git add <file>..." to include in what will be committed)\n\tqa-factory/new.txt'
  stderr=''
porcelain AFTER apply --index:
'R  old9.txt -> new9.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
after apply --index: porcelain == before: True; full index == before: True; qa untouched: True
$ git stash drop df569a63a3db   # G10 drop by sha12
  exit=128
  stdout=''
  stderr="error: 'df569a63a3db' is not a stash reference"
$ git stash list '--format=%H %gd %s'   # G10 list after drop
  exit=0
  stdout='df569a63a3db4fd93aae0e03f15ee04d20b62b43 stash@{0} On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git rev-parse -q --verify refs/stash   # G9 after drop
  exit=0
  stdout='df569a63a3db4fd93aae0e03f15ee04d20b62b43'
  stderr=''

=== row 8 | class space: space in path ===
porcelain BEFORE:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? "a b.txt"
?? qa-factory/new.txt'
$ git rev-parse -q --verify refs/stash   # G9 before
  exit=1
  stdout=''
  stderr=''
$ git stash push --include-untracked -m 'QA Factory story t-118: your uncommitted changes, put aside before the tests' -- 'a b.txt'   # G8
  exit=0
  stdout='Saved working directory and index state On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git rev-parse -q --verify refs/stash   # G9 after
  exit=0
  stdout='30202e8bea54d0d58b2700d0bed5a4b5fa95c207'
  stderr=''
porcelain AFTER stash:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
person entries remaining: []; qa-factory untouched: True
$ git log -1 --format=%s 30202e8bea54d0d58b2700d0bed5a4b5fa95c207   # G9 subject
  exit=0
  stdout='On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git stash list '--format=%H %gd %s'   # G10 list
  exit=0
  stdout='30202e8bea54d0d58b2700d0bed5a4b5fa95c207 stash@{0} On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git stash apply --index 30202e8bea54   # G10 apply by sha12
  exit=0
  stdout='On branch master\nChanges to be committed:\n  (use "git restore --staged <file>..." to unstage)\n\tnew file:   qa-factory/staged.txt\n\nChanges not staged for commit:\n  (use "git add <file>..." to update what will be committed)\n  (use "git restore <file>..." to discard changes in working directory)\n\tmodified:   qa-factory/x.txt\n\nUntracked files:\n  (use "git add <file>..." to include in what will be committed)\n\ta b.txt\n\tqa-factory/new.txt'
  stderr=''
porcelain AFTER apply --index:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? "a b.txt"
?? qa-factory/new.txt'
after apply --index: porcelain == before: True; full index == before: True; qa untouched: True
$ git stash drop 30202e8bea54   # G10 drop by sha12
  exit=128
  stdout=''
  stderr="error: '30202e8bea54' is not a stash reference"
$ git stash list '--format=%H %gd %s'   # G10 list after drop
  exit=0
  stdout='30202e8bea54d0d58b2700d0bed5a4b5fa95c207 stash@{0} On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git rev-parse -q --verify refs/stash   # G9 after drop
  exit=0
  stdout='30202e8bea54d0d58b2700d0bed5a4b5fa95c207'
  stderr=''

=== row 8 | class nonascii: non-ASCII paths (e-acute, CJK) ===
porcelain BEFORE:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? "caf\\303\\251.txt"
?? qa-factory/new.txt
?? "\\344\\270\\255\\346\\226\\207.txt"'
$ git rev-parse -q --verify refs/stash   # G9 before
  exit=1
  stdout=''
  stderr=''
$ git stash push --include-untracked -m 'QA Factory story t-118: your uncommitted changes, put aside before the tests' -- 'caf\xe9.txt' '\u4e2d\u6587.txt'   # G8
  exit=0
  stdout='Saved working directory and index state On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git rev-parse -q --verify refs/stash   # G9 after
  exit=0
  stdout='99a8bfa859bb4dd1fafff379e1c65d02a87732ad'
  stderr=''
porcelain AFTER stash:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
person entries remaining: []; qa-factory untouched: True
$ git log -1 --format=%s 99a8bfa859bb4dd1fafff379e1c65d02a87732ad   # G9 subject
  exit=0
  stdout='On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git stash list '--format=%H %gd %s'   # G10 list
  exit=0
  stdout='99a8bfa859bb4dd1fafff379e1c65d02a87732ad stash@{0} On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git stash apply --index 99a8bfa859bb   # G10 apply by sha12
  exit=0
  stdout='On branch master\nChanges to be committed:\n  (use "git restore --staged <file>..." to unstage)\n\tnew file:   qa-factory/staged.txt\n\nChanges not staged for commit:\n  (use "git add <file>..." to update what will be committed)\n  (use "git restore <file>..." to discard changes in working directory)\n\tmodified:   qa-factory/x.txt\n\nUntracked files:\n  (use "git add <file>..." to include in what will be committed)\n\t"caf\\303\\251.txt"\n\tqa-factory/new.txt\n\t"\\344\\270\\255\\346\\226\\207.txt"'
  stderr=''
porcelain AFTER apply --index:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? "caf\\303\\251.txt"
?? qa-factory/new.txt
?? "\\344\\270\\255\\346\\226\\207.txt"'
after apply --index: porcelain == before: True; full index == before: True; qa untouched: True
$ git stash drop 99a8bfa859bb   # G10 drop by sha12
  exit=128
  stdout=''
  stderr="error: '99a8bfa859bb' is not a stash reference"
$ git stash list '--format=%H %gd %s'   # G10 list after drop
  exit=0
  stdout='99a8bfa859bb4dd1fafff379e1c65d02a87732ad stash@{0} On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git rev-parse -q --verify refs/stash   # G9 after drop
  exit=0
  stdout='99a8bfa859bb4dd1fafff379e1c65d02a87732ad'
  stderr=''

=== row 8 | class sub:  M submodule pointer ===
porcelain BEFORE:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
 M sub12
?? qa-factory/new.txt'
$ git rev-parse -q --verify refs/stash   # G9 before
  exit=1
  stdout=''
  stderr=''
$ git stash push --include-untracked -m 'QA Factory story t-118: your uncommitted changes, put aside before the tests' -- sub12   # G8
  exit=0
  stdout='No local changes to save'
  stderr=''
$ git rev-parse -q --verify refs/stash   # G9 after
  exit=1
  stdout=''
  stderr=''
porcelain AFTER stash:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
 M sub12
?? qa-factory/new.txt'
person entries remaining: ['sub12']; qa-factory untouched: True
no stash ref after the command

=== row 8 | class sub_added: A  new submodule ===
porcelain BEFORE:
'A  .gitmodules
A  qa-factory/staged.txt
 M qa-factory/x.txt
A  sub13
?? qa-factory/new.txt'
$ git rev-parse -q --verify refs/stash   # G9 before
  exit=1
  stdout=''
  stderr=''
$ git stash push --include-untracked -m 'QA Factory story t-118: your uncommitted changes, put aside before the tests' -- .gitmodules sub13   # G8
  exit=0
  stdout='Saved working directory and index state On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr="warning: unable to rmdir 'sub13': Directory not empty"
$ git rev-parse -q --verify refs/stash   # G9 after
  exit=0
  stdout='b56f5b7efd8831b86d9391d9616f044dac49c6b6'
  stderr=''
porcelain AFTER stash:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt
?? sub13/'
person entries remaining: ['sub13/']; qa-factory untouched: True
$ git log -1 --format=%s b56f5b7efd8831b86d9391d9616f044dac49c6b6   # G9 subject
  exit=0
  stdout='On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git stash list '--format=%H %gd %s'   # G10 list
  exit=0
  stdout='b56f5b7efd8831b86d9391d9616f044dac49c6b6 stash@{0} On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git stash apply --index b56f5b7efd88   # G10 apply by sha12
  exit=128
  stdout=''
  stderr='error: qa-factory/staged.txt: already exists in index\nerror: conflicts in index. Try without --index.'
porcelain AFTER apply --index:
'A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt
?? sub13/'
after apply --index: porcelain == before: False; full index == before: False; qa untouched: True
$ git stash drop b56f5b7efd88   # G10 drop by sha12
  exit=128
  stdout=''
  stderr="error: 'b56f5b7efd88' is not a stash reference"
$ git stash list '--format=%H %gd %s'   # G10 list after drop
  exit=0
  stdout='b56f5b7efd8831b86d9391d9616f044dac49c6b6 stash@{0} On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git rev-parse -q --verify refs/stash   # G9 after drop
  exit=0
  stdout='b56f5b7efd8831b86d9391d9616f044dac49c6b6'
  stderr=''

=== row 8 | MIXED all non-blocked classes ===
porcelain BEFORE:
'A  add8.txt
 D del6.txt
D  del7.txt
 A itd10.txt
 M m3.txt
M  m4.txt
MM m5.txt
R  old9.txt -> new9.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
 M sub12
?? "a b.txt"
?? "caf\\303\\251.txt"
?? d2/
?? qa-factory/new.txt
?? u1.txt
?? "\\344\\270\\255\\346\\226\\207.txt"'
$ git rev-parse -q --verify refs/stash   # G9 before
  exit=1
  stdout=''
  stderr=''
$ git stash push --include-untracked -m 'QA Factory story t-118: your uncommitted changes, put aside before the tests' -- add8.txt del6.txt del7.txt itd10.txt m3.txt m4.txt m5.txt new9.txt old9.txt sub12 'a b.txt' 'caf\xe9.txt' d2/a.txt d2/b.txt u1.txt '\u4e2d\u6587.txt'   # G8
  exit=128
  stdout=''
  stderr="error: Entry 'itd10.txt' not uptodate. Cannot merge.\nCannot save the current worktree state"
$ git rev-parse -q --verify refs/stash   # G9 after
  exit=1
  stdout=''
  stderr=''
porcelain AFTER stash:
'A  add8.txt
 D del6.txt
D  del7.txt
 A itd10.txt
 M m3.txt
M  m4.txt
MM m5.txt
R  old9.txt -> new9.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
 M sub12
?? "a b.txt"
?? "caf\\303\\251.txt"
?? d2/
?? qa-factory/new.txt
?? u1.txt
?? "\\344\\270\\255\\346\\226\\207.txt"'
person entries remaining: ['add8.txt', 'del6.txt', 'del7.txt', 'itd10.txt', 'm3.txt', 'm4.txt', 'm5.txt', 'new9.txt', 'sub12', 'a b.txt', 'caf\xe9.txt', 'd2/a.txt', 'd2/b.txt', 'u1.txt', '\u4e2d\u6587.txt']; qa-factory untouched: True
no stash ref after the command

=== row 8e | our stash is NOT on top: another stash is pushed after ours, then drop <our sha12> ===
$ git stash push --include-untracked -m 'QA Factory story t-118: your uncommitted changes, put aside before the tests' -- m5.txt u1.txt   # G8 ours
  exit=0
  stdout='Saved working directory and index state On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git stash push --include-untracked -m 'someone elses stash' -- other.txt   # another stash on top
  exit=0
  stdout='Saved working directory and index state On master: someone elses stash'
  stderr=''
$ git stash list '--format=%H %gd %s'   # G10 list: ours is stash@{1}
  exit=0
  stdout='65177dfb5fead41639c8744b7eddb6cfe6c50964 stash@{0} On master: someone elses stash\n3b9ea9301082e326cc72af09ca4556da9b947cb1 stash@{1} On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git stash apply --index 3b9ea9301082   # G10 apply ours by sha12 (not on top)
  exit=128
  stdout=''
  stderr='error: qa-factory/staged.txt: already exists in index\nerror: conflicts in index. Try without --index.'
$ git stash drop 3b9ea9301082   # G10 drop ours by sha12
  exit=128
  stdout=''
  stderr="error: '3b9ea9301082' is not a stash reference"
$ git stash list '--format=%H %gd %s'   # G10 list after: only the other stash must remain
  exit=0
  stdout='65177dfb5fead41639c8744b7eddb6cfe6c50964 stash@{0} On master: someone elses stash\n3b9ea9301082e326cc72af09ca4556da9b947cb1 stash@{1} On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''

=== row 8f | drop with an unknown / too-short / full sha ===
$ git stash drop 0000000000000000   # unknown sha
  exit=0
  stdout='Dropped refs/stash@{0000000000000000} (65177dfb5fead41639c8744b7eddb6cfe6c50964)'
  stderr=''
$ git stash drop 3b9ea9301082e326cc72af09ca4556da9b947cb1   # full sha of the already dropped entry
  exit=128
  stdout=''
  stderr="error: '3b9ea9301082e326cc72af09ca4556da9b947cb1' is not a stash reference"
$ git stash drop 3b9e   # 4-char abbreviation
  exit=128
  stdout=''
  stderr="error: '3b9e' is not a stash reference"

##### ROW 8g: why `apply --index` failed above (a STAGED qa-factory/staged.txt is in the index) and what drop form works

=== row 8g | class m_idx: the SAME stash in a repo WITHOUT the staged qa-factory/staged.txt (cause check) ===
$ git stash push --include-untracked -m 'QA Factory story t-118: your uncommitted changes, put aside before the tests' -- m4.txt   # G8
  exit=0
  stdout='Saved working directory and index state On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git stash apply --index 9a734a107004   # G10 apply --index by sha12, no staged qa file
  exit=0
  stdout='On branch master\nChanges to be committed:\n  (use "git restore --staged <file>..." to unstage)\n\tmodified:   m4.txt\n\nChanges not staged for commit:\n  (use "git add <file>..." to update what will be committed)\n  (use "git restore <file>..." to discard changes in working directory)\n\tmodified:   qa-factory/x.txt\n\nUntracked files:\n  (use "git add <file>..." to include in what will be committed)\n\tqa-factory/new.txt\n\tqa-factory/staged.txt'
  stderr=''
porcelain == before: True; index == before: True
porcelain after apply:
'M  m4.txt
 M qa-factory/x.txt
?? qa-factory/new.txt
?? qa-factory/staged.txt'
$ git stash drop stash@{0}   # drop by the list's own name stash@{0} (found by sha 9a734a107004 in `stash list --format=%H %gd`)
  exit=0
  stdout='Dropped stash@{0} (9a734a107004fa89ac86dd8803632785e4b71637)'
  stderr=''
$ git stash list '--format=%H %gd %s'   # list after drop
  exit=0
  stdout=''
  stderr=''

=== row 8g | class mm: the SAME stash in a repo WITHOUT the staged qa-factory/staged.txt (cause check) ===
$ git stash push --include-untracked -m 'QA Factory story t-118: your uncommitted changes, put aside before the tests' -- m5.txt   # G8
  exit=0
  stdout='Saved working directory and index state On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git stash apply --index a18d80045eb0   # G10 apply --index by sha12, no staged qa file
  exit=0
  stdout='On branch master\nChanges to be committed:\n  (use "git restore --staged <file>..." to unstage)\n\tmodified:   m5.txt\n\nChanges not staged for commit:\n  (use "git add <file>..." to update what will be committed)\n  (use "git restore <file>..." to discard changes in working directory)\n\tmodified:   m5.txt\n\tmodified:   qa-factory/x.txt\n\nUntracked files:\n  (use "git add <file>..." to include in what will be committed)\n\tqa-factory/new.txt\n\tqa-factory/staged.txt'
  stderr=''
porcelain == before: True; index == before: True
porcelain after apply:
'MM m5.txt
 M qa-factory/x.txt
?? qa-factory/new.txt
?? qa-factory/staged.txt'
$ git stash drop stash@{0}   # drop by the list's own name stash@{0} (found by sha a18d80045eb0 in `stash list --format=%H %gd`)
  exit=0
  stdout='Dropped stash@{0} (a18d80045eb0cc40e77d47df46cf72a6f155688f)'
  stderr=''
$ git stash list '--format=%H %gd %s'   # list after drop
  exit=0
  stdout=''
  stderr=''

=== row 8g | class a_idx: the SAME stash in a repo WITHOUT the staged qa-factory/staged.txt (cause check) ===
$ git stash push --include-untracked -m 'QA Factory story t-118: your uncommitted changes, put aside before the tests' -- add8.txt   # G8
  exit=0
  stdout='Saved working directory and index state On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git stash apply --index 150c6362bacd   # G10 apply --index by sha12, no staged qa file
  exit=0
  stdout='On branch master\nChanges to be committed:\n  (use "git restore --staged <file>..." to unstage)\n\tnew file:   add8.txt\n\nChanges not staged for commit:\n  (use "git add <file>..." to update what will be committed)\n  (use "git restore <file>..." to discard changes in working directory)\n\tmodified:   qa-factory/x.txt\n\nUntracked files:\n  (use "git add <file>..." to include in what will be committed)\n\tqa-factory/new.txt\n\tqa-factory/staged.txt'
  stderr=''
porcelain == before: True; index == before: True
porcelain after apply:
'A  add8.txt
 M qa-factory/x.txt
?? qa-factory/new.txt
?? qa-factory/staged.txt'
$ git stash drop stash@{0}   # drop by the list's own name stash@{0} (found by sha 150c6362bacd in `stash list --format=%H %gd`)
  exit=0
  stdout='Dropped stash@{0} (150c6362bacd9a4ff583e885666ef1583eeca34f)'
  stderr=''
$ git stash list '--format=%H %gd %s'   # list after drop
  exit=0
  stdout=''
  stderr=''

=== row 8g | class sub_added: the SAME stash in a repo WITHOUT the staged qa-factory/staged.txt (cause check) ===
$ git stash push --include-untracked -m 'QA Factory story t-118: your uncommitted changes, put aside before the tests' -- .gitmodules sub13   # G8
  exit=0
  stdout='Saved working directory and index state On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr="warning: unable to rmdir 'sub13': Directory not empty"
$ git stash apply --index 3b71e712c89e   # G10 apply --index by sha12, no staged qa file
  exit=0
  stdout='On branch master\nChanges to be committed:\n  (use "git restore --staged <file>..." to unstage)\n\tnew file:   .gitmodules\n\tnew file:   sub13\n\nChanges not staged for commit:\n  (use "git add <file>..." to update what will be committed)\n  (use "git restore <file>..." to discard changes in working directory)\n\tmodified:   qa-factory/x.txt\n\nUntracked files:\n  (use "git add <file>..." to include in what will be committed)\n\tqa-factory/new.txt\n\tqa-factory/staged.txt'
  stderr=''
porcelain == before: True; index == before: True
porcelain after apply:
'A  .gitmodules
 M qa-factory/x.txt
A  sub13
?? qa-factory/new.txt
?? qa-factory/staged.txt'
$ git stash drop stash@{0}   # drop by the list's own name stash@{0} (found by sha 3b71e712c89e in `stash list --format=%H %gd`)
  exit=0
  stdout='Dropped stash@{0} (3b71e712c89eab97434975c5d4965882ccfd553c)'
  stderr=''
$ git stash list '--format=%H %gd %s'   # list after drop
  exit=0
  stdout=''
  stderr=''

=== row 8g | class m_idx: WITH the staged qa-factory/staged.txt: apply WITHOUT --index, and apply --index by stash@{N} ===
$ git stash push --include-untracked -m 'QA Factory story t-118: your uncommitted changes, put aside before the tests' -- m4.txt   # G8
  exit=0
  stdout='Saved working directory and index state On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git stash apply --index stash@{0}   # apply --index by stash@{0}
  exit=128
  stdout=''
  stderr='error: qa-factory/staged.txt: already exists in index\nerror: conflicts in index. Try without --index.'
$ git stash apply 063b2bfe36d4   # apply WITHOUT --index, by sha12
  exit=0
  stdout='On branch master\nChanges to be committed:\n  (use "git restore --staged <file>..." to unstage)\n\tnew file:   qa-factory/staged.txt\n\nChanges not staged for commit:\n  (use "git add <file>..." to update what will be committed)\n  (use "git restore <file>..." to discard changes in working directory)\n\tmodified:   m4.txt\n\tmodified:   qa-factory/x.txt\n\nUntracked files:\n  (use "git add <file>..." to include in what will be committed)\n\tqa-factory/new.txt'
  stderr=''
porcelain after plain apply:
' M m4.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
porcelain == before: False; index == before: False
$ git stash drop stash@{0}   # drop by stash@{0}
  exit=0
  stdout='Dropped stash@{0} (063b2bfe36d4d4b89d0e943f920b32e49c585669)'
  stderr=''

=== row 8g | class mm: WITH the staged qa-factory/staged.txt: apply WITHOUT --index, and apply --index by stash@{N} ===
$ git stash push --include-untracked -m 'QA Factory story t-118: your uncommitted changes, put aside before the tests' -- m5.txt   # G8
  exit=0
  stdout='Saved working directory and index state On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git stash apply --index stash@{0}   # apply --index by stash@{0}
  exit=128
  stdout=''
  stderr='error: qa-factory/staged.txt: already exists in index\nerror: conflicts in index. Try without --index.'
$ git stash apply 0ec222d06d31   # apply WITHOUT --index, by sha12
  exit=0
  stdout='On branch master\nChanges to be committed:\n  (use "git restore --staged <file>..." to unstage)\n\tnew file:   qa-factory/staged.txt\n\nChanges not staged for commit:\n  (use "git add <file>..." to update what will be committed)\n  (use "git restore <file>..." to discard changes in working directory)\n\tmodified:   m5.txt\n\tmodified:   qa-factory/x.txt\n\nUntracked files:\n  (use "git add <file>..." to include in what will be committed)\n\tqa-factory/new.txt'
  stderr=''
porcelain after plain apply:
' M m5.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
porcelain == before: False; index == before: False
$ git stash drop stash@{0}   # drop by stash@{0}
  exit=0
  stdout='Dropped stash@{0} (0ec222d06d318c7fbc89ca2c4edcb0e276f7d982)'
  stderr=''

=== row 8g | class a_idx: WITH the staged qa-factory/staged.txt: apply WITHOUT --index, and apply --index by stash@{N} ===
$ git stash push --include-untracked -m 'QA Factory story t-118: your uncommitted changes, put aside before the tests' -- add8.txt   # G8
  exit=0
  stdout='Saved working directory and index state On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git stash apply --index stash@{0}   # apply --index by stash@{0}
  exit=128
  stdout=''
  stderr='error: qa-factory/staged.txt: already exists in index\nerror: conflicts in index. Try without --index.'
$ git stash apply ab6fc2a52efb   # apply WITHOUT --index, by sha12
  exit=0
  stdout='On branch master\nChanges to be committed:\n  (use "git restore --staged <file>..." to unstage)\n\tnew file:   add8.txt\n\tnew file:   qa-factory/staged.txt\n\nChanges not staged for commit:\n  (use "git add <file>..." to update what will be committed)\n  (use "git restore <file>..." to discard changes in working directory)\n\tmodified:   qa-factory/x.txt\n\nUntracked files:\n  (use "git add <file>..." to include in what will be committed)\n\tqa-factory/new.txt'
  stderr=''
porcelain after plain apply:
'A  add8.txt
A  qa-factory/staged.txt
 M qa-factory/x.txt
?? qa-factory/new.txt'
porcelain == before: True; index == before: True
$ git stash drop stash@{0}   # drop by stash@{0}
  exit=0
  stdout='Dropped stash@{0} (ab6fc2a52efbd3c42bbbe876de68a339e4f7fc47)'
  stderr=''

=== row 8g | class sub_added: WITH the staged qa-factory/staged.txt: apply WITHOUT --index, and apply --index by stash@{N} ===
$ git stash push --include-untracked -m 'QA Factory story t-118: your uncommitted changes, put aside before the tests' -- .gitmodules sub13   # G8
  exit=0
  stdout='Saved working directory and index state On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr="warning: unable to rmdir 'sub13': Directory not empty"
$ git stash apply --index stash@{0}   # apply --index by stash@{0}
  exit=128
  stdout=''
  stderr='error: qa-factory/staged.txt: already exists in index\nerror: conflicts in index. Try without --index.'
$ git stash apply 07c4ff29dec5   # apply WITHOUT --index, by sha12
  exit=0
  stdout='On branch master\nChanges to be committed:\n  (use "git restore --staged <file>..." to unstage)\n\tnew file:   .gitmodules\n\tnew file:   qa-factory/staged.txt\n\tnew file:   sub13\n\nChanges not staged for commit:\n  (use "git add <file>..." to update what will be committed)\n  (use "git restore <file>..." to discard changes in working directory)\n\tmodified:   qa-factory/x.txt\n\nUntracked files:\n  (use "git add <file>..." to include in what will be committed)\n\tqa-factory/new.txt'
  stderr=''
porcelain after plain apply:
'A  .gitmodules
A  qa-factory/staged.txt
 M qa-factory/x.txt
A  sub13
?? qa-factory/new.txt'
porcelain == before: True; index == before: True
$ git stash drop stash@{0}   # drop by stash@{0}
  exit=0
  stdout='Dropped stash@{0} (07c4ff29dec5c18f5809acdb54a5d6352cc4d53a)'
  stderr=''

=== row 8h | drop by stash@{N} when ours is NOT on top (another stash on top); drop must remove ours only ===
$ git stash push --include-untracked -m 'QA Factory story t-118: your uncommitted changes, put aside before the tests' -- m3.txt u1.txt   # G8 ours
  exit=0
  stdout='Saved working directory and index state On master: QA Factory story t-118: your uncommitted changes, put aside before the tests'
  stderr=''
$ git stash push --include-untracked -m 'someone elses stash' -- other.txt   # another stash on top
  exit=0
  stdout='Saved working directory and index state On master: someone elses stash'
  stderr=''
ours is stash@{1}
$ git stash apply --index stash@{1}   # apply --index ours by stash@{1} (qa-factory not staged here)
  exit=0
  stdout='On branch master\nChanges not staged for commit:\n  (use "git add <file>..." to update what will be committed)\n  (use "git restore <file>..." to discard changes in working directory)\n\tmodified:   m3.txt\n\tmodified:   qa-factory/x.txt\n\nUntracked files:\n  (use "git add <file>..." to include in what will be committed)\n\tqa-factory/new.txt\n\tqa-factory/staged.txt\n\tu1.txt\n\nno changes added to commit (use "git add" and/or "git commit -a")'
  stderr=''
$ git stash drop stash@{1}   # drop ours by stash@{1}
  exit=0
  stdout='Dropped stash@{1} (531620af561f26bdfb37d414a31f97c09bcbbdce)'
  stderr=''
$ git stash list '--format=%H %gd %s'   # only the other stash must remain
  exit=0
  stdout='2fb94ec10877a3c9061e2538f028ef46d999a0d2 stash@{0} On master: someone elses stash'
  stderr=''

=== row 8h | a sha12 made only of decimal digits is read by git as a date/number (sha-prefix risk): drop <digits> ===
$ git stash drop 000000000000   # 12 digits, no such stash (what does git drop?)
  exit=0
  stdout='Dropped refs/stash@{000000000000} (2fb94ec10877a3c9061e2538f028ef46d999a0d2)'
  stderr=''
$ git stash list '--format=%H %gd %s'   # list after
  exit=0
  stdout=''
  stderr=''

##### ROW 9: G12, G11, G13

=== row 9 | G12 `git diff --name-status -z <head_before> HEAD` after a mixed commit (rename, delete, add, modify, submodule, space, non-ASCII) ===
$ git commit -q -m 'QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' -- add8.txt del6.txt del7.txt itd10.txt m3.txt m4.txt m5.txt new9.txt old9.txt sub12 'a b.txt' 'caf\xe9.txt' d2/a.txt d2/b.txt u1.txt '\u4e2d\u6587.txt'   # G5 commit
  exit=0
  stdout=''
  stderr=''
$ git diff --name-status -z 183dd35a7001ec557ec2c7933bfa2d2ff40ee9da HEAD   # G12
  exit=0
  stdout=b'A\x00a b.txt\x00A\x00add8.txt\x00A\x00caf\xc3\xa9.txt\x00A\x00d2/a.txt\x00A\x00d2/b.txt\x00D\x00del6.txt\x00D\x00del7.txt\x00A\x00itd10.txt\x00M\x00m3.txt\x00M\x00m4.txt\x00M\x00m5.txt\x00R100\x00old9.txt\x00new9.txt\x00M\x00sub12\x00A\x00u1.txt\x00A\x00\xe4\xb8\xad\xe6\x96\x87.txt\x00'
  stderr=''
$ git diff --name-status -z --no-renames 183dd35a7001ec557ec2c7933bfa2d2ff40ee9da HEAD   # G12 with --no-renames
  exit=0
  stdout=b'A\x00a b.txt\x00A\x00add8.txt\x00A\x00caf\xc3\xa9.txt\x00A\x00d2/a.txt\x00A\x00d2/b.txt\x00D\x00del6.txt\x00D\x00del7.txt\x00A\x00itd10.txt\x00M\x00m3.txt\x00M\x00m4.txt\x00M\x00m5.txt\x00A\x00new9.txt\x00D\x00old9.txt\x00M\x00sub12\x00A\x00u1.txt\x00A\x00\xe4\xb8\xad\xe6\x96\x87.txt\x00'
  stderr=''
$ git diff --name-status 183dd35a7001ec557ec2c7933bfa2d2ff40ee9da HEAD   # G12 plain, for reference
  exit=0
  stdout='A\ta b.txt\nA\tadd8.txt\nA\t"caf\\303\\251.txt"\nA\td2/a.txt\nA\td2/b.txt\nD\tdel6.txt\nD\tdel7.txt\nA\titd10.txt\nM\tm3.txt\nM\tm4.txt\nM\tm5.txt\nR100\told9.txt\tnew9.txt\nM\tsub12\nA\tu1.txt\nA\t"\\344\\270\\255\\346\\226\\207.txt"'
  stderr=''

=== row 9 | G11 forms ===
$ git rev-parse HEAD   # G11 HEAD
  exit=0
  stdout='afc380ae8378b6bfb16a860fcafc35260dbf01b8'
  stderr=''
$ git rev-parse HEAD^   # G11 HEAD^ (parent of the new commit)
  exit=0
  stdout='183dd35a7001ec557ec2c7933bfa2d2ff40ee9da'
  stderr=''
$ git rev-parse --abbrev-ref HEAD   # G11 branch
  exit=0
  stdout='master'
  stderr=''
$ git rev-parse --show-toplevel   # G11 toplevel from the root
  exit=0
  stdout='C:/Users/i_mas/AppData/Local/Temp/claude/b3e3188b390a00d9/f92520fc-f552-4e47-9d06-efbc3daae572/scratchpad/b0-2/repos/r9'
  stderr=''
$ git rev-parse --show-toplevel   # G11 toplevel from a subfolder (git -C <subfolder>)
  exit=0
  stdout='C:/Users/i_mas/AppData/Local/Temp/claude/b3e3188b390a00d9/f92520fc-f552-4e47-9d06-efbc3daae572/scratchpad/b0-2/repos/r9'
  stderr=''
$ git rev-parse --show-toplevel   # G11 toplevel from qa-factory/
  exit=0
  stdout='C:/Users/i_mas/AppData/Local/Temp/claude/b3e3188b390a00d9/f92520fc-f552-4e47-9d06-efbc3daae572/scratchpad/b0-2/repos/r9'
  stderr=''
$ git rev-parse --abbrev-ref HEAD   # G11 detached: prints HEAD
  exit=0
  stdout='HEAD'
  stderr=''
$ git rev-parse HEAD^   # G11 detached HEAD^
  exit=0
  stdout='183dd35a7001ec557ec2c7933bfa2d2ff40ee9da'
  stderr=''

=== row 9 | G11 on a repository with no commit, and HEAD^ on a root commit ===
$ git rev-parse HEAD   # unborn: HEAD
  exit=128
  stdout='HEAD'
  stderr="fatal: ambiguous argument 'HEAD': unknown revision or path not in the working tree.\nUse '--' to separate paths from revisions, like this:\n'git <command> [<revision>...] -- [<file>...]'"
$ git rev-parse --abbrev-ref HEAD   # unborn: abbrev-ref
  exit=128
  stdout='HEAD'
  stderr="fatal: ambiguous argument 'HEAD': unknown revision or path not in the working tree.\nUse '--' to separate paths from revisions, like this:\n'git <command> [<revision>...] -- [<file>...]'"
$ git rev-parse --show-toplevel   # unborn: toplevel
  exit=0
  stdout='C:/Users/i_mas/AppData/Local/Temp/claude/b3e3188b390a00d9/f92520fc-f552-4e47-9d06-efbc3daae572/scratchpad/b0-2/repos/r9-unborn'
  stderr=''
$ git status --porcelain=v1 -z -uall   # unborn: G1 (empty)
  exit=0
  stdout=b''
  stderr=''
$ git log --fixed-strings '--grep=QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' --format=%H -n 1   # unborn: G13
  exit=128
  stdout=''
  stderr="fatal: your current branch 'master' does not have any commits yet"
$ git rev-parse HEAD^   # root commit: HEAD^
  exit=128
  stdout='HEAD^'
  stderr="fatal: ambiguous argument 'HEAD^': unknown revision or path not in the working tree.\nUse '--' to separate paths from revisions, like this:\n'git <command> [<revision>...] -- [<file>...]'"

=== row 9 | G13 `git log --fixed-strings --grep=<MSG> --format=%H -n 1` ===
$ git commit -q -m 'QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' -- m3.txt   # commit with MSG
  exit=0
  stdout=''
  stderr=''
$ git commit -q -m 'QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2] second commit with the same MSG as its prefix' -- next.txt   # a later commit whose subject CONTAINS MSG
  exit=0
  stdout=''
  stderr=''
$ git log '--format=%H %s'   # whole log
  exit=0
  stdout='418a568fc92e2eb9a72fc4d8e282f805aa44e9ce QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2] second commit with the same MSG as its prefix\n183e7fbd91138c26de63e2a078179c451b35e37d QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]\n4a33578b99d5e876b5c8e4de65ab3e380403c8fa base'
  stderr=''
$ git log --fixed-strings '--grep=QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' --format=%H -n 1   # G13 (newest match wins with -n 1)
  exit=0
  stdout='418a568fc92e2eb9a72fc4d8e282f805aa44e9ce'
  stderr=''
$ git log --fixed-strings '--grep=no such message' --format=%H -n 1   # G13 no match: empty, exit?
  exit=0
  stdout=''
  stderr=''
$ git log '--grep=QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' --format=%H -n 1   # WITHOUT --fixed-strings (regex chars in MSG), for contrast
  exit=0
  stdout=''
  stderr=''
$ git log --fixed-strings '--grep=QA Factory story t-118: your uncommitted changes, committed before the tests (a|b) [1.2]' --format=%H -n 1 --all   # G13 with --all (stash refs / other branches)
  exit=0
  stdout='418a568fc92e2eb9a72fc4d8e282f805aa44e9ce'
  stderr=''


TABLE rows 4/8 (tag, commit/stash exit, took, qa untouched, undo porcelain, undo index)
| u_file | rc=0 | took exactly: True | qa untouched: True | undo porcelain==before: True | undo index==before: True |
| u_dir | rc=0 | took exactly: True | qa untouched: True | undo porcelain==before: True | undo index==before: True |
| m_wt | rc=0 | took exactly: True | qa untouched: True | undo porcelain==before: True | undo index==before: True |
| m_idx | rc=0 | took exactly: True | qa untouched: True | undo porcelain==before: True | undo index==before: True |
| mm | rc=0 | took exactly: True | qa untouched: True | undo porcelain==before: True | undo index==before: True |
| d_wt | rc=0 | took exactly: True | qa untouched: True | undo porcelain==before: True | undo index==before: True |
| d_idx | rc=0 | took exactly: True | qa untouched: True | undo porcelain==before: True | undo index==before: True |
| a_idx | rc=0 | took exactly: True | qa untouched: True | undo porcelain==before: True | undo index==before: True |
| a_itd | rc=0 | took exactly: True | qa untouched: True | undo porcelain==before: False | undo index==before: False |
| r_idx | rc=0 | took exactly: True | qa untouched: True | undo porcelain==before: True | undo index==before: True |
| space | rc=0 | took exactly: True | qa untouched: True | undo porcelain==before: True | undo index==before: True |
| nonascii | rc=0 | took exactly: True | qa untouched: True | undo porcelain==before: True | undo index==before: True |
| sub | rc=0 | took exactly: True | qa untouched: True | undo porcelain==before: True | undo index==before: True |
| nested | blocked: nested repository: nested/ |  |  |  |  |
| rn_qa | blocked: partial-home rename: src/y.txt |  |  |  |  |
| sub_added | rc=0 | took exactly: True | qa untouched: True | undo porcelain==before: True | undo index==before: True |
| ALLOK | rc=0 | took exactly: True | qa untouched: True | undo porcelain==before: False | undo index==before: False |
| hook1-mm | rc=1 | n/a | qa untouched: True | G6 porcelain==before: True | G6 index==before: True |
| hook1-allok | rc=1 | n/a | qa untouched: True | G6 porcelain==before: False | G6 index==before: False |
| hook-rewrite | rc=0 | took exactly: True | qa untouched: True | undo porcelain==before: True | undo index==before: True |
| hook-rewrite-add | rc=0 | took exactly: True | qa untouched: True | undo porcelain==before: True | undo index==before: True |
| hook-newfile | rc=0 | took exactly: True | qa untouched: True | undo porcelain==before: False | undo index==before: True |
| u_file | stash rc=0 | person left: 0 | apply rc=0 | apply porcelain==before: True | apply index==before: True |
| u_dir | stash rc=0 | person left: 0 | apply rc=0 | apply porcelain==before: True | apply index==before: True |
| m_wt | stash rc=0 | person left: 0 | apply rc=0 | apply porcelain==before: True | apply index==before: True |
| m_idx | stash rc=0 | person left: 0 | apply rc=128 | apply porcelain==before: False | apply index==before: False |
| mm | stash rc=0 | person left: 0 | apply rc=128 | apply porcelain==before: False | apply index==before: False |
| d_wt | stash rc=0 | person left: 0 | apply rc=0 | apply porcelain==before: True | apply index==before: True |
| d_idx | stash rc=128 | person left: 1 | apply rc=0 | apply porcelain==before: True | apply index==before: True |
| a_idx | stash rc=0 | person left: 0 | apply rc=128 | apply porcelain==before: False | apply index==before: False |
| a_itd | stash rc=128 | no entry | qa untouched: True |  |  |
| r_idx | stash rc=128 | person left: 1 | apply rc=0 | apply porcelain==before: True | apply index==before: True |
| space | stash rc=0 | person left: 0 | apply rc=0 | apply porcelain==before: True | apply index==before: True |
| nonascii | stash rc=0 | person left: 0 | apply rc=0 | apply porcelain==before: True | apply index==before: True |
| sub | stash rc=0 | no entry | qa untouched: True |  |  |
| sub_added | stash rc=0 | person left: 1 | apply rc=128 | apply porcelain==before: False | apply index==before: False |
| ALLOK | stash rc=128 | no entry | qa untouched: True |  |  |

SUMMARY: cases=79 git_calls=1894 row_errors=0 git=git version 2.56.0.windows.2
```

# t-110 B0: git measurement

git version: `git version 2.56.0.windows.2`

## Findings (builder's reading of the verbatim output below; the table is at the end of the output block)

- Fine for both C and S, qa-factory untouched, listed entries only: classes 1, 2, 3, 4, 5, 6, 8, and 10/11 ONLY with the UNQUOTED real path (and 12 for C only).
- Fails, both C and S: class 7 (`D ` staged delete) and class 9 (`R ` rename, both sides passed): `git add -- <path>` exits 128 `pathspec 'del7.txt' did not match any files` (path is in neither worktree nor index); nothing is left staged for C (the add is atomic, porcelain unchanged). Class 13 fails the same way (7 and 9 inside it), nothing staged. S on 7 and 9: exit 128 AND stdout `Saved working directory and index state`, `stash show` lists the entry, and porcelain after is unchanged: a stash ENTRY was left behind while the tree kept the change (a half-done stash, needs cleanup).
- Quoted porcelain text passed as-is (10, 11): C exits 128 (pathspec did not match); S exits 0 with `No local changes to save` (silent no-op, stash pop then fails `No stash entries found`). A lossless read is the unquoted real path; porcelain's quoted form is not usable as a pathspec.
- Class 12 submodule pointer: C ok; S exit 0, `No local changes to save`, takes nothing (silent no-op).
- Class 4 (`M `) and 5 (`MM`), C: `git commit -- paths` commits the WORKTREE content (class 5: HEAD='worktree', the staged-only 'staged' version is not what lands); class 4 unchanged by that. Index split after `reset --soft HEAD~1`: 4 returns to `M `, 5 returns to `M ` (the MM split is lost, worktree content stays).
- S then plain `git stash pop`: 4 and 5 come back as ` M` / ` M` (staged state lost); `git stash pop --index`: 4 `M `, 5 `MM` restored.
- C `reset --soft HEAD~1` equals the BEFORE porcelain only for classes 4 and 8; for `??`, ` M`, ` D`, 5, 12 and the unquoted 10/11 it differs (everything comes back staged).
- Environment note: default `core.autocrlf` of this machine prints LF/CRLF warnings on stderr of exit-0 steps (visible in the output); not a failure.
- Test-design note: in the first run class 13 had del7/add8 with identical content, which git paired into a rename; contents were made distinct and the run repeated; the report holds the second run.

Command: `python -B C:\Users\i_mas\AppData\Local\Temp\claude\b3e3188b390a00d9\f92520fc-f552-4e47-9d06-efbc3daae572\scratchpad\b0\measure.py`

## measure.py (full source)

```python
"""B0 measurement: do `git add + git commit -- paths` (C) and `git stash push -u -- paths` (S) take exactly the listed entries?
Fresh scratch repos only; every git call is `git -C <repo>` with subprocess cwd=<repo>. Writes the report file too."""
import os, shutil, stat, subprocess, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(r"C:\Users\i_mas\AppData\Local\Temp\claude\b3e3188b390a00d9\f92520fc-f552-4e47-9d06-efbc3daae572\scratchpad\b0")
REPOS = ROOT / "repos"
REPORT = Path(r"C:\QAFactory\forge-repo\docs\tasks\specs\reports\t-110-b0-git-measure.md")
ENV = dict(os.environ, GIT_TERMINAL_PROMPT="0", GCM_INTERACTIVE="Never")
LOG = []


def log(text=""):
    LOG.append(text)
    print(text)


def g(repo, *args, user=False):
    cmd = ["git"] + (["-c", "user.name=t", "-c", "user.email=t@t"] if user else []) + ["-C", str(repo), *args]
    p = subprocess.run(cmd, capture_output=True, cwd=str(repo), env=ENV)
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


def porcelain(repo):
    return g(repo, "status", "--porcelain")[1]


def porcelain_path(line):  # copy of gate_preflight.porcelain_path
    parts = str(line).strip().split(None, 1)
    return parts[1] if len(parts) > 1 else str(line).strip()


def w(repo, rel, text):
    p = repo / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(text.encode("utf-8"))


def rd(repo, rel):
    p = repo / rel
    return p.read_bytes().decode("utf-8") if p.exists() else "<absent>"


def rmtree(path):
    def onerr(fn, p, exc):
        os.chmod(p, stat.S_IWRITE)
        fn(p)
    if path.exists():
        shutil.rmtree(path, onerror=onerr)


# --- class builders: (phase) phase "base" creates tracked files before the base commit; "dirty" makes the state
def k1(r, ph):
    if ph == "dirty": w(r, "u1.txt", "u1\n")
def k2(r, ph):
    if ph == "dirty": w(r, "d2/a.txt", "a\n"); w(r, "d2/b.txt", "b\n")
def k3(r, ph):
    if ph == "base": w(r, "m3.txt", "base\n")
    else: w(r, "m3.txt", "worktree\n")
def k4(r, ph):
    if ph == "base": w(r, "m4.txt", "base\n")
    else: w(r, "m4.txt", "staged\n"); g(r, "add", "--", "m4.txt")
def k5(r, ph):
    if ph == "base": w(r, "m5.txt", "base\n")
    else: w(r, "m5.txt", "staged\n"); g(r, "add", "--", "m5.txt"); w(r, "m5.txt", "worktree\n")
def k6(r, ph):
    if ph == "base": w(r, "del6.txt", "x\n")
    else: (r / "del6.txt").unlink()
def k7(r, ph):
    if ph == "base": w(r, "del7.txt", "unique seven\nzzz\n")
    else: g(r, "rm", "-q", "--", "del7.txt")
def k8(r, ph):
    if ph == "dirty": w(r, "add8.txt", "totally different eight\n"); g(r, "add", "--", "add8.txt")
def k9(r, ph):
    if ph == "base": w(r, "old9.txt", "some content that is long enough\nline2\nline3\n")
    else: g(r, "mv", "old9.txt", "new9.txt")
def k10(r, ph):
    if ph == "dirty": w(r, "a b.txt", "x\n")
def k11(r, ph):
    if ph == "dirty": w(r, "caf\u00e9.txt", "x\n")
def k12(r, ph):
    if ph == "base":
        sub = r.parent / (r.name + "-subsrc")
        rmtree(sub); sub.mkdir(parents=True)
        g(sub, "init", "-q"); w(sub, "s.txt", "s\n"); g(sub, "add", "-A"); g(sub, "commit", "-q", "-m", "s", user=True)
        rc, o, e = g(r, "-c", "protocol.file.allow=always", "submodule", "add", "-q", str(sub), "sub12", user=True)
        if rc: raise RuntimeError("submodule add failed: " + e)
    else:
        w(r, "sub12/s2.txt", "s2\n"); g(r / "sub12", "add", "-A"); g(r / "sub12", "commit", "-q", "-m", "s2", user=True)

SETUPS = {1: k1, 2: k2, 3: k3, 4: k4, 5: k5, 6: k6, 7: k7, 8: k8, 9: k9, 10: k10, 11: k11, 12: k12}
# class -> list of (variant, real paths or None meaning "from porcelain as-is")
CLASSES = [
    ("1 ?? untracked file", [1], [("raw", None)]),
    ("2 ?? untracked folder", [2], [("raw", None)]),
    ("3 ' M' modified unstaged", [3], [("raw", None)]),
    ("4 'M ' modified staged", [4], [("raw", None)]),
    ("5 'MM' staged+modified", [5], [("raw", None)]),
    ("6 ' D' deleted unstaged", [6], [("raw", None)]),
    ("7 'D ' deleted staged", [7], [("raw", None)]),
    ("8 'A ' added staged", [8], [("raw", None)]),
    ("9 'R ' rename (both sides)", [9], [("raw", None)]),
    ("10 space in path", [10], [("quoted-as-is", None), ("unquoted-real", ["a b.txt"])]),
    ("11 non-ASCII in path", [11], [("quoted-as-is", None), ("unquoted-real", ["caf\u00e9.txt"])]),
    ("12 submodule pointer", [12], [("raw", None)]),
    ("13 ALL 1-9 together", [1, 2, 3, 4, 5, 6, 7, 8, 9], [("raw", None)]),
]


def build(repo, ks):
    rmtree(repo); repo.mkdir(parents=True)
    g(repo, "init", "-q"); g(repo, "config", "user.name", "t"); g(repo, "config", "user.email", "t@t")
    g(repo, "config", "commit.gpgsign", "false")
    w(repo, "qa-factory/x.txt", "base\n")
    for k in ks: SETUPS[k](repo, "base")
    g(repo, "add", "-A"); rc, o, e = g(repo, "commit", "-q", "-m", "base")
    if rc: raise RuntimeError("base commit failed: " + e)
    for k in ks: SETUPS[k](repo, "dirty")
    w(repo, "qa-factory/x.txt", "dirty\n"); w(repo, "qa-factory/new.txt", "new\n")


def qa_state(repo):
    return ([l for l in porcelain(repo).splitlines() if "qa-factory/" in l], rd(repo, "qa-factory/x.txt"), rd(repo, "qa-factory/new.txt"))


def paths_for(before, real):
    if real is not None: return list(real)
    out = []
    for line in before.splitlines():
        body = porcelain_path(line)
        if body.startswith("qa-factory/"): continue
        out.extend(body.split(" -> "))
    return out


def outside(p): return [l for l in p.splitlines() if "qa-factory/" not in l]


def measure(label, ks, variant, real, cmd, pop_index=False):
    tag = f"{label.split()[0]}-{variant}-{cmd}{'-idx' if pop_index else ''}"
    repo = REPOS / tag
    build(repo, ks)
    before = porcelain(repo); qa0 = qa_state(repo)
    paths = paths_for(before, real)
    log(f"\n=== class {label} | variant {variant} | cmd {cmd}{' (pop --index)' if pop_index else ''} ===")
    log("porcelain BEFORE:\n" + before.rstrip("\n"))
    log("paths passed: " + repr(paths))
    res = {"label": label, "variant": variant, "cmd": cmd + ("-idx" if pop_index else "")}
    steps = [["add", "--", *paths], ["commit", "-m", "m", "--", *paths]] if cmd == "C" else [["stash", "push", "--include-untracked", "-m", "m", "--", *paths]]
    rc_all = 0
    for s in steps:
        rc, o, e = g(repo, *s, user=True)
        log(f"$ git {' '.join(s)}\n  exit={rc}\n  stdout={o.strip()!r}\n  stderr={e.strip()!r}")
        if rc: rc_all = rc; break
    after = porcelain(repo)
    log("porcelain AFTER:\n" + after.rstrip("\n"))
    qa1 = qa_state(repo)
    res["exit"] = rc_all
    res["qa_untouched"] = qa0 == qa1
    if cmd == "C":
        rc, o, e = g(repo, "show", "--stat", "--name-status", "HEAD"); log("$ git show --stat --name-status HEAD\n" + o.rstrip())
        for f in ("m4.txt", "m5.txt"):
            if (repo / f).exists() or f in o:
                log(f"  content {f}: HEAD={g(repo, 'show', 'HEAD:' + f)[1].strip()!r} worktree={rd(repo, f).strip()!r}")
        taken_ok = rc_all == 0 and not outside(after) and "qa-factory" not in o
        res["exact"] = taken_ok
        if rc_all == 0:
            rc, o, e = g(repo, "reset", "--soft", "HEAD~1"); log(f"$ git reset --soft HEAD~1 exit={rc} stderr={e.strip()!r}")
            after2 = porcelain(repo); log("porcelain after reset --soft:\n" + after2.rstrip("\n"))
            res["restored"] = after2 == before
        else:
            res["restored"] = "n/a"
    else:
        rc, o, e = g(repo, "stash", "show", "--include-untracked", "--name-status", "stash@{0}")
        if rc: rc, o, e = g(repo, "stash", "list")
        log("$ git stash show --include-untracked --name-status stash@{0}\n" + o.rstrip() + ("  stderr=" + e.strip() if e.strip() else ""))
        res["exact"] = rc_all == 0 and not outside(after) and "qa-factory" not in o
        if rc_all == 0:
            pop = ["stash", "pop"] + (["--index"] if pop_index else [])
            rc, o, e = g(repo, *pop, user=True)
            log(f"$ git {' '.join(pop)} exit={rc}\n  stderr={e.strip()!r}")
            after2 = porcelain(repo); log("porcelain after pop:\n" + after2.rstrip("\n"))
            res["restored"] = after2 == before
        else:
            res["restored"] = "n/a"
    return res


def main():
    REPOS.mkdir(parents=True, exist_ok=True)
    rc, ver, _ = g(ROOT, "--version"); ver = subprocess.run(["git", "--version"], capture_output=True, text=True).stdout.strip()
    log("git version: " + ver)
    results = []
    for label, ks, variants in CLASSES:
        for variant, real in variants:
            for cmd in ("C", "S"):
                try:
                    results.append(measure(label, ks, variant, real, cmd))
                    if cmd == "S" and label.split()[0] in ("4", "5", "13"):
                        results.append(measure(label, ks, variant, real, cmd, pop_index=True))
                except Exception as ex:
                    log(f"\n=== class {label} {variant} {cmd}: NOT MEASURED: {ex!r}")
                    results.append({"label": label, "variant": variant, "cmd": cmd, "exit": "not measured", "exact": "-", "qa_untouched": "-", "restored": "-"})
    yn = lambda v: v if isinstance(v, str) else ("yes" if v else "no")
    log("\n\nTABLE (C = add+commit; S = stash -u; restored = C: reset --soft HEAD~1 equals BEFORE porcelain / S: stash pop equals BEFORE porcelain)")
    log("| class | variant | cmd | exit | took exactly the listed | qa-factory untouched | restores BEFORE |")
    log("|---|---|---|---|---|---|---|")
    for r in results:
        log(f"| {r['label']} | {r['variant']} | {r['cmd']} | {r['exit']} | {yn(r['exact'])} | {yn(r['qa_untouched'])} | {yn(r['restored'])} |")
    src = Path(__file__).read_text(encoding="utf-8")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("# t-110 B0: git measurement\n\ngit version: `" + ver + "`\n\nCommand: `python -B " + str(Path(__file__)) +
                      "`\n\n## measure.py (full source)\n\n```python\n" + src + "\n```\n\n## Verbatim output of the run\n\n```\n" + "\n".join(LOG) + "\n```\n", encoding="utf-8")
    return 0


sys.exit(main())

```

## Verbatim output of the run

```
git version: git version 2.56.0.windows.2

=== class 1 ?? untracked file | variant raw | cmd C ===
porcelain BEFORE:
 M qa-factory/x.txt
?? qa-factory/new.txt
?? u1.txt
paths passed: ['u1.txt']
$ git add -- u1.txt
  exit=0
  stdout=''
  stderr="warning: in the working copy of 'u1.txt', LF will be replaced by CRLF the next time Git touches it"
$ git commit -m m -- u1.txt
  exit=0
  stdout='[master 6e7b297] m\n 1 file changed, 1 insertion(+)\n create mode 100644 u1.txt'
  stderr="warning: in the working copy of 'u1.txt', LF will be replaced by CRLF the next time Git touches it\nwarning: in the working copy of 'u1.txt', LF will be replaced by CRLF the next time Git touches it"
porcelain AFTER:
 M qa-factory/x.txt
?? qa-factory/new.txt
$ git show --stat --name-status HEAD
commit 6e7b2977a386e04b5964073552ebe28aedaf405a
Author: t <t@t>
Date:   Thu Nov 12 13:05:21 2026 +0100

    m

A	u1.txt
$ git reset --soft HEAD~1 exit=0 stderr=''
porcelain after reset --soft:
 M qa-factory/x.txt
A  u1.txt
?? qa-factory/new.txt

=== class 1 ?? untracked file | variant raw | cmd S ===
porcelain BEFORE:
 M qa-factory/x.txt
?? qa-factory/new.txt
?? u1.txt
paths passed: ['u1.txt']
$ git stash push --include-untracked -m m -- u1.txt
  exit=0
  stdout='Saved working directory and index state On master: m'
  stderr="warning: in the working copy of 'u1.txt', LF will be replaced by CRLF the next time Git touches it\nwarning: in the working copy of 'u1.txt', LF will be replaced by CRLF the next time Git touches it"
porcelain AFTER:
 M qa-factory/x.txt
?? qa-factory/new.txt
$ git stash show --include-untracked --name-status stash@{0}
A	u1.txt
$ git stash pop exit=0
  stderr=''
porcelain after pop:
 M qa-factory/x.txt
?? qa-factory/new.txt
?? u1.txt

=== class 2 ?? untracked folder | variant raw | cmd C ===
porcelain BEFORE:
 M qa-factory/x.txt
?? d2/
?? qa-factory/new.txt
paths passed: ['d2/']
$ git add -- d2/
  exit=0
  stdout=''
  stderr="warning: in the working copy of 'd2/a.txt', LF will be replaced by CRLF the next time Git touches it\nwarning: in the working copy of 'd2/b.txt', LF will be replaced by CRLF the next time Git touches it"
$ git commit -m m -- d2/
  exit=0
  stdout='[master 71c3ef0] m\n 2 files changed, 2 insertions(+)\n create mode 100644 d2/a.txt\n create mode 100644 d2/b.txt'
  stderr="warning: in the working copy of 'd2/a.txt', LF will be replaced by CRLF the next time Git touches it\nwarning: in the working copy of 'd2/b.txt', LF will be replaced by CRLF the next time Git touches it"
porcelain AFTER:
 M qa-factory/x.txt
?? qa-factory/new.txt
$ git show --stat --name-status HEAD
commit 71c3ef03d161cb36a2b3e27373f8e34bef770fb4
Author: t <t@t>
Date:   Thu Nov 12 13:05:24 2026 +0100

    m

A	d2/a.txt
A	d2/b.txt
$ git reset --soft HEAD~1 exit=0 stderr=''
porcelain after reset --soft:
A  d2/a.txt
A  d2/b.txt
 M qa-factory/x.txt
?? qa-factory/new.txt

=== class 2 ?? untracked folder | variant raw | cmd S ===
porcelain BEFORE:
 M qa-factory/x.txt
?? d2/
?? qa-factory/new.txt
paths passed: ['d2/']
$ git stash push --include-untracked -m m -- d2/
  exit=0
  stdout='Saved working directory and index state On master: m'
  stderr="warning: in the working copy of 'd2/a.txt', LF will be replaced by CRLF the next time Git touches it\nwarning: in the working copy of 'd2/b.txt', LF will be replaced by CRLF the next time Git touches it\nwarning: in the working copy of 'd2/a.txt', LF will be replaced by CRLF the next time Git touches it\nwarning: in the working copy of 'd2/b.txt', LF will be replaced by CRLF the next time Git touches it"
porcelain AFTER:
 M qa-factory/x.txt
?? qa-factory/new.txt
$ git stash show --include-untracked --name-status stash@{0}
A	d2/a.txt
A	d2/b.txt
$ git stash pop exit=0
  stderr=''
porcelain after pop:
 M qa-factory/x.txt
?? d2/
?? qa-factory/new.txt

=== class 3 ' M' modified unstaged | variant raw | cmd C ===
porcelain BEFORE:
 M m3.txt
 M qa-factory/x.txt
?? qa-factory/new.txt
paths passed: ['m3.txt']
$ git add -- m3.txt
  exit=0
  stdout=''
  stderr="warning: in the working copy of 'm3.txt', LF will be replaced by CRLF the next time Git touches it"
$ git commit -m m -- m3.txt
  exit=0
  stdout='[master 63f7485] m\n 1 file changed, 1 insertion(+), 1 deletion(-)'
  stderr="warning: in the working copy of 'm3.txt', LF will be replaced by CRLF the next time Git touches it\nwarning: in the working copy of 'm3.txt', LF will be replaced by CRLF the next time Git touches it"
porcelain AFTER:
 M qa-factory/x.txt
?? qa-factory/new.txt
$ git show --stat --name-status HEAD
commit 63f7485887e6a6d5476941d07265361fa9fa8f03
Author: t <t@t>
Date:   Thu Nov 12 13:05:27 2026 +0100

    m

M	m3.txt
$ git reset --soft HEAD~1 exit=0 stderr=''
porcelain after reset --soft:
M  m3.txt
 M qa-factory/x.txt
?? qa-factory/new.txt

=== class 3 ' M' modified unstaged | variant raw | cmd S ===
porcelain BEFORE:
 M m3.txt
 M qa-factory/x.txt
?? qa-factory/new.txt
paths passed: ['m3.txt']
$ git stash push --include-untracked -m m -- m3.txt
  exit=0
  stdout='Saved working directory and index state On master: m'
  stderr="warning: in the working copy of 'm3.txt', LF will be replaced by CRLF the next time Git touches it\nwarning: in the working copy of 'm3.txt', LF will be replaced by CRLF the next time Git touches it"
porcelain AFTER:
 M qa-factory/x.txt
?? qa-factory/new.txt
$ git stash show --include-untracked --name-status stash@{0}
M	m3.txt
$ git stash pop exit=0
  stderr=''
porcelain after pop:
 M m3.txt
 M qa-factory/x.txt
?? qa-factory/new.txt

=== class 4 'M ' modified staged | variant raw | cmd C ===
porcelain BEFORE:
M  m4.txt
 M qa-factory/x.txt
?? qa-factory/new.txt
paths passed: ['m4.txt']
$ git add -- m4.txt
  exit=0
  stdout=''
  stderr="warning: in the working copy of 'm4.txt', LF will be replaced by CRLF the next time Git touches it"
$ git commit -m m -- m4.txt
  exit=0
  stdout='[master bdbf5e9] m\n 1 file changed, 1 insertion(+), 1 deletion(-)'
  stderr="warning: in the working copy of 'm4.txt', LF will be replaced by CRLF the next time Git touches it\nwarning: in the working copy of 'm4.txt', LF will be replaced by CRLF the next time Git touches it"
porcelain AFTER:
 M qa-factory/x.txt
?? qa-factory/new.txt
$ git show --stat --name-status HEAD
commit bdbf5e90836429b9392106ef1c6f90e557c78fbd
Author: t <t@t>
Date:   Thu Nov 12 13:05:30 2026 +0100

    m

M	m4.txt
  content m4.txt: HEAD='staged' worktree='staged'
$ git reset --soft HEAD~1 exit=0 stderr=''
porcelain after reset --soft:
M  m4.txt
 M qa-factory/x.txt
?? qa-factory/new.txt

=== class 4 'M ' modified staged | variant raw | cmd S ===
porcelain BEFORE:
M  m4.txt
 M qa-factory/x.txt
?? qa-factory/new.txt
paths passed: ['m4.txt']
$ git stash push --include-untracked -m m -- m4.txt
  exit=0
  stdout='Saved working directory and index state On master: m'
  stderr="warning: in the working copy of 'm4.txt', LF will be replaced by CRLF the next time Git touches it"
porcelain AFTER:
 M qa-factory/x.txt
?? qa-factory/new.txt
$ git stash show --include-untracked --name-status stash@{0}
M	m4.txt
$ git stash pop exit=0
  stderr=''
porcelain after pop:
 M m4.txt
 M qa-factory/x.txt
?? qa-factory/new.txt

=== class 4 'M ' modified staged | variant raw | cmd S (pop --index) ===
porcelain BEFORE:
M  m4.txt
 M qa-factory/x.txt
?? qa-factory/new.txt
paths passed: ['m4.txt']
$ git stash push --include-untracked -m m -- m4.txt
  exit=0
  stdout='Saved working directory and index state On master: m'
  stderr="warning: in the working copy of 'm4.txt', LF will be replaced by CRLF the next time Git touches it"
porcelain AFTER:
 M qa-factory/x.txt
?? qa-factory/new.txt
$ git stash show --include-untracked --name-status stash@{0}
M	m4.txt
$ git stash pop --index exit=0
  stderr=''
porcelain after pop:
M  m4.txt
 M qa-factory/x.txt
?? qa-factory/new.txt

=== class 5 'MM' staged+modified | variant raw | cmd C ===
porcelain BEFORE:
MM m5.txt
 M qa-factory/x.txt
?? qa-factory/new.txt
paths passed: ['m5.txt']
$ git add -- m5.txt
  exit=0
  stdout=''
  stderr="warning: in the working copy of 'm5.txt', LF will be replaced by CRLF the next time Git touches it"
$ git commit -m m -- m5.txt
  exit=0
  stdout='[master d075440] m\n 1 file changed, 1 insertion(+), 1 deletion(-)'
  stderr="warning: in the working copy of 'm5.txt', LF will be replaced by CRLF the next time Git touches it\nwarning: in the working copy of 'm5.txt', LF will be replaced by CRLF the next time Git touches it"
porcelain AFTER:
 M qa-factory/x.txt
?? qa-factory/new.txt
$ git show --stat --name-status HEAD
commit d0754405acdd7671ab786ca860fb105fa03c5313
Author: t <t@t>
Date:   Thu Nov 12 13:05:37 2026 +0100

    m

M	m5.txt
  content m5.txt: HEAD='worktree' worktree='worktree'
$ git reset --soft HEAD~1 exit=0 stderr=''
porcelain after reset --soft:
M  m5.txt
 M qa-factory/x.txt
?? qa-factory/new.txt

=== class 5 'MM' staged+modified | variant raw | cmd S ===
porcelain BEFORE:
MM m5.txt
 M qa-factory/x.txt
?? qa-factory/new.txt
paths passed: ['m5.txt']
$ git stash push --include-untracked -m m -- m5.txt
  exit=0
  stdout='Saved working directory and index state On master: m'
  stderr="warning: in the working copy of 'm5.txt', LF will be replaced by CRLF the next time Git touches it\nwarning: in the working copy of 'm5.txt', LF will be replaced by CRLF the next time Git touches it"
porcelain AFTER:
 M qa-factory/x.txt
?? qa-factory/new.txt
$ git stash show --include-untracked --name-status stash@{0}
M	m5.txt
$ git stash pop exit=0
  stderr=''
porcelain after pop:
 M m5.txt
 M qa-factory/x.txt
?? qa-factory/new.txt

=== class 5 'MM' staged+modified | variant raw | cmd S (pop --index) ===
porcelain BEFORE:
MM m5.txt
 M qa-factory/x.txt
?? qa-factory/new.txt
paths passed: ['m5.txt']
$ git stash push --include-untracked -m m -- m5.txt
  exit=0
  stdout='Saved working directory and index state On master: m'
  stderr="warning: in the working copy of 'm5.txt', LF will be replaced by CRLF the next time Git touches it\nwarning: in the working copy of 'm5.txt', LF will be replaced by CRLF the next time Git touches it"
porcelain AFTER:
 M qa-factory/x.txt
?? qa-factory/new.txt
$ git stash show --include-untracked --name-status stash@{0}
M	m5.txt
$ git stash pop --index exit=0
  stderr=''
porcelain after pop:
MM m5.txt
 M qa-factory/x.txt
?? qa-factory/new.txt

=== class 6 ' D' deleted unstaged | variant raw | cmd C ===
porcelain BEFORE:
 D del6.txt
 M qa-factory/x.txt
?? qa-factory/new.txt
paths passed: ['del6.txt']
$ git add -- del6.txt
  exit=0
  stdout=''
  stderr=''
$ git commit -m m -- del6.txt
  exit=0
  stdout='[master 00c5df7] m\n 1 file changed, 1 deletion(-)\n delete mode 100644 del6.txt'
  stderr=''
porcelain AFTER:
 M qa-factory/x.txt
?? qa-factory/new.txt
$ git show --stat --name-status HEAD
commit 00c5df776b6de1d29d1a8227d4c2e4d6aab0b548
Author: t <t@t>
Date:   Thu Nov 12 13:05:42 2026 +0100

    m

D	del6.txt
$ git reset --soft HEAD~1 exit=0 stderr=''
porcelain after reset --soft:
D  del6.txt
 M qa-factory/x.txt
?? qa-factory/new.txt

=== class 6 ' D' deleted unstaged | variant raw | cmd S ===
porcelain BEFORE:
 D del6.txt
 M qa-factory/x.txt
?? qa-factory/new.txt
paths passed: ['del6.txt']
$ git stash push --include-untracked -m m -- del6.txt
  exit=0
  stdout='Saved working directory and index state On master: m'
  stderr=''
porcelain AFTER:
 M qa-factory/x.txt
?? qa-factory/new.txt
$ git stash show --include-untracked --name-status stash@{0}
D	del6.txt
$ git stash pop exit=0
  stderr=''
porcelain after pop:
 D del6.txt
 M qa-factory/x.txt
?? qa-factory/new.txt

=== class 7 'D ' deleted staged | variant raw | cmd C ===
porcelain BEFORE:
D  del7.txt
 M qa-factory/x.txt
?? qa-factory/new.txt
paths passed: ['del7.txt']
$ git add -- del7.txt
  exit=128
  stdout=''
  stderr="fatal: pathspec 'del7.txt' did not match any files"
porcelain AFTER:
D  del7.txt
 M qa-factory/x.txt
?? qa-factory/new.txt
$ git show --stat --name-status HEAD
commit 31db6b62f36e9a9f5d25e3b5f0789d8d556a4d33
Author: t <t@t>
Date:   Thu Nov 12 13:05:45 2026 +0100

    base

A	del7.txt
A	qa-factory/x.txt

=== class 7 'D ' deleted staged | variant raw | cmd S ===
porcelain BEFORE:
D  del7.txt
 M qa-factory/x.txt
?? qa-factory/new.txt
paths passed: ['del7.txt']
$ git stash push --include-untracked -m m -- del7.txt
  exit=128
  stdout='Saved working directory and index state On master: m'
  stderr="fatal: pathspec ':(prefix:0)del7.txt' did not match any files"
porcelain AFTER:
D  del7.txt
 M qa-factory/x.txt
?? qa-factory/new.txt
$ git stash show --include-untracked --name-status stash@{0}
D	del7.txt

=== class 8 'A ' added staged | variant raw | cmd C ===
porcelain BEFORE:
A  add8.txt
 M qa-factory/x.txt
?? qa-factory/new.txt
paths passed: ['add8.txt']
$ git add -- add8.txt
  exit=0
  stdout=''
  stderr="warning: in the working copy of 'add8.txt', LF will be replaced by CRLF the next time Git touches it"
$ git commit -m m -- add8.txt
  exit=0
  stdout='[master 8c4a94b] m\n 1 file changed, 1 insertion(+)\n create mode 100644 add8.txt'
  stderr="warning: in the working copy of 'add8.txt', LF will be replaced by CRLF the next time Git touches it"
porcelain AFTER:
 M qa-factory/x.txt
?? qa-factory/new.txt
$ git show --stat --name-status HEAD
commit 8c4a94bc72792a6864241d951f4e01cd4770e6b2
Author: t <t@t>
Date:   Thu Nov 12 13:05:48 2026 +0100

    m

A	add8.txt
$ git reset --soft HEAD~1 exit=0 stderr=''
porcelain after reset --soft:
A  add8.txt
 M qa-factory/x.txt
?? qa-factory/new.txt

=== class 8 'A ' added staged | variant raw | cmd S ===
porcelain BEFORE:
A  add8.txt
 M qa-factory/x.txt
?? qa-factory/new.txt
paths passed: ['add8.txt']
$ git stash push --include-untracked -m m -- add8.txt
  exit=0
  stdout='Saved working directory and index state On master: m'
  stderr="warning: in the working copy of 'add8.txt', LF will be replaced by CRLF the next time Git touches it"
porcelain AFTER:
 M qa-factory/x.txt
?? qa-factory/new.txt
$ git stash show --include-untracked --name-status stash@{0}
A	add8.txt
$ git stash pop exit=0
  stderr=''
porcelain after pop:
A  add8.txt
 M qa-factory/x.txt
?? qa-factory/new.txt

=== class 9 'R ' rename (both sides) | variant raw | cmd C ===
porcelain BEFORE:
R  old9.txt -> new9.txt
 M qa-factory/x.txt
?? qa-factory/new.txt
paths passed: ['old9.txt', 'new9.txt']
$ git add -- old9.txt new9.txt
  exit=128
  stdout=''
  stderr="fatal: pathspec 'old9.txt' did not match any files"
porcelain AFTER:
R  old9.txt -> new9.txt
 M qa-factory/x.txt
?? qa-factory/new.txt
$ git show --stat --name-status HEAD
commit 31b5f2715e5dd0cebd284e78752ed9ef5abed2ad
Author: t <t@t>
Date:   Thu Nov 12 13:05:50 2026 +0100

    base

A	old9.txt
A	qa-factory/x.txt

=== class 9 'R ' rename (both sides) | variant raw | cmd S ===
porcelain BEFORE:
R  old9.txt -> new9.txt
 M qa-factory/x.txt
?? qa-factory/new.txt
paths passed: ['old9.txt', 'new9.txt']
$ git stash push --include-untracked -m m -- old9.txt new9.txt
  exit=128
  stdout='Saved working directory and index state On master: m'
  stderr="fatal: pathspec ':(prefix:0)old9.txt' did not match any files"
porcelain AFTER:
R  old9.txt -> new9.txt
 M qa-factory/x.txt
?? qa-factory/new.txt
$ git stash show --include-untracked --name-status stash@{0}
R100	old9.txt	new9.txt

=== class 10 space in path | variant quoted-as-is | cmd C ===
porcelain BEFORE:
 M qa-factory/x.txt
?? "a b.txt"
?? qa-factory/new.txt
paths passed: ['"a b.txt"']
$ git add -- "a b.txt"
  exit=128
  stdout=''
  stderr='fatal: pathspec \'"a b.txt"\' did not match any files'
porcelain AFTER:
 M qa-factory/x.txt
?? "a b.txt"
?? qa-factory/new.txt
$ git show --stat --name-status HEAD
commit f8c550feefc7e41d8faac833e1fdb1a21f271003
Author: t <t@t>
Date:   Thu Nov 12 13:05:53 2026 +0100

    base

A	qa-factory/x.txt

=== class 10 space in path | variant quoted-as-is | cmd S ===
porcelain BEFORE:
 M qa-factory/x.txt
?? "a b.txt"
?? qa-factory/new.txt
paths passed: ['"a b.txt"']
$ git stash push --include-untracked -m m -- "a b.txt"
  exit=0
  stdout='No local changes to save'
  stderr=''
porcelain AFTER:
 M qa-factory/x.txt
?? "a b.txt"
?? qa-factory/new.txt
$ git stash show --include-untracked --name-status stash@{0}

$ git stash pop exit=128
  stderr='No stash entries found.'
porcelain after pop:
 M qa-factory/x.txt
?? "a b.txt"
?? qa-factory/new.txt

=== class 10 space in path | variant unquoted-real | cmd C ===
porcelain BEFORE:
 M qa-factory/x.txt
?? "a b.txt"
?? qa-factory/new.txt
paths passed: ['a b.txt']
$ git add -- a b.txt
  exit=0
  stdout=''
  stderr="warning: in the working copy of 'a b.txt', LF will be replaced by CRLF the next time Git touches it"
$ git commit -m m -- a b.txt
  exit=0
  stdout='[master 5f4abbc] m\n 1 file changed, 1 insertion(+)\n create mode 100644 a b.txt'
  stderr="warning: in the working copy of 'a b.txt', LF will be replaced by CRLF the next time Git touches it\nwarning: in the working copy of 'a b.txt', LF will be replaced by CRLF the next time Git touches it"
porcelain AFTER:
 M qa-factory/x.txt
?? qa-factory/new.txt
$ git show --stat --name-status HEAD
commit 5f4abbc499626e1f79c2ab2e9ce31c2d90baeb4b
Author: t <t@t>
Date:   Thu Nov 12 13:05:56 2026 +0100

    m

A	a b.txt
$ git reset --soft HEAD~1 exit=0 stderr=''
porcelain after reset --soft:
A  "a b.txt"
 M qa-factory/x.txt
?? qa-factory/new.txt

=== class 10 space in path | variant unquoted-real | cmd S ===
porcelain BEFORE:
 M qa-factory/x.txt
?? "a b.txt"
?? qa-factory/new.txt
paths passed: ['a b.txt']
$ git stash push --include-untracked -m m -- a b.txt
  exit=0
  stdout='Saved working directory and index state On master: m'
  stderr="warning: in the working copy of 'a b.txt', LF will be replaced by CRLF the next time Git touches it\nwarning: in the working copy of 'a b.txt', LF will be replaced by CRLF the next time Git touches it"
porcelain AFTER:
 M qa-factory/x.txt
?? qa-factory/new.txt
$ git stash show --include-untracked --name-status stash@{0}
A	a b.txt
$ git stash pop exit=0
  stderr=''
porcelain after pop:
 M qa-factory/x.txt
?? "a b.txt"
?? qa-factory/new.txt

=== class 11 non-ASCII in path | variant quoted-as-is | cmd C ===
porcelain BEFORE:
 M qa-factory/x.txt
?? "caf\303\251.txt"
?? qa-factory/new.txt
paths passed: ['"caf\\303\\251.txt"']
$ git add -- "caf\303\251.txt"
  exit=128
  stdout=''
  stderr='fatal: pathspec \'"caf\\303\\251.txt"\' did not match any files'
porcelain AFTER:
 M qa-factory/x.txt
?? "caf\303\251.txt"
?? qa-factory/new.txt
$ git show --stat --name-status HEAD
commit 65fb24f23570bee6c34166ea2a649c082c718a14
Author: t <t@t>
Date:   Thu Nov 12 13:06:00 2026 +0100

    base

A	qa-factory/x.txt

=== class 11 non-ASCII in path | variant quoted-as-is | cmd S ===
porcelain BEFORE:
 M qa-factory/x.txt
?? "caf\303\251.txt"
?? qa-factory/new.txt
paths passed: ['"caf\\303\\251.txt"']
$ git stash push --include-untracked -m m -- "caf\303\251.txt"
  exit=0
  stdout='No local changes to save'
  stderr=''
porcelain AFTER:
 M qa-factory/x.txt
?? "caf\303\251.txt"
?? qa-factory/new.txt
$ git stash show --include-untracked --name-status stash@{0}

$ git stash pop exit=128
  stderr='No stash entries found.'
porcelain after pop:
 M qa-factory/x.txt
?? "caf\303\251.txt"
?? qa-factory/new.txt

=== class 11 non-ASCII in path | variant unquoted-real | cmd C ===
porcelain BEFORE:
 M qa-factory/x.txt
?? "caf\303\251.txt"
?? qa-factory/new.txt
paths passed: ['café.txt']
$ git add -- café.txt
  exit=0
  stdout=''
  stderr="warning: in the working copy of 'café.txt', LF will be replaced by CRLF the next time Git touches it"
$ git commit -m m -- café.txt
  exit=0
  stdout='[master 4fec49e] m\n 1 file changed, 1 insertion(+)\n create mode 100644 "caf\\303\\251.txt"'
  stderr="warning: in the working copy of 'café.txt', LF will be replaced by CRLF the next time Git touches it"
porcelain AFTER:
 M qa-factory/x.txt
?? qa-factory/new.txt
$ git show --stat --name-status HEAD
commit 4fec49efb70baf8c59bed2f83e19da6eaf3d84a6
Author: t <t@t>
Date:   Thu Nov 12 13:06:04 2026 +0100

    m

A	"caf\303\251.txt"
$ git reset --soft HEAD~1 exit=0 stderr=''
porcelain after reset --soft:
A  "caf\303\251.txt"
 M qa-factory/x.txt
?? qa-factory/new.txt

=== class 11 non-ASCII in path | variant unquoted-real | cmd S ===
porcelain BEFORE:
 M qa-factory/x.txt
?? "caf\303\251.txt"
?? qa-factory/new.txt
paths passed: ['café.txt']
$ git stash push --include-untracked -m m -- café.txt
  exit=0
  stdout='Saved working directory and index state On master: m'
  stderr="warning: in the working copy of 'café.txt', LF will be replaced by CRLF the next time Git touches it\nwarning: in the working copy of 'café.txt', LF will be replaced by CRLF the next time Git touches it"
porcelain AFTER:
 M qa-factory/x.txt
?? qa-factory/new.txt
$ git stash show --include-untracked --name-status stash@{0}
A	"caf\303\251.txt"
$ git stash pop exit=0
  stderr=''
porcelain after pop:
 M qa-factory/x.txt
?? "caf\303\251.txt"
?? qa-factory/new.txt

=== class 12 submodule pointer | variant raw | cmd C ===
porcelain BEFORE:
 M qa-factory/x.txt
 M sub12
?? qa-factory/new.txt
paths passed: ['sub12']
$ git add -- sub12
  exit=0
  stdout=''
  stderr=''
$ git commit -m m -- sub12
  exit=0
  stdout='[master 74208b8] m\n 1 file changed, 1 insertion(+), 1 deletion(-)'
  stderr=''
porcelain AFTER:
 M qa-factory/x.txt
?? qa-factory/new.txt
$ git show --stat --name-status HEAD
commit 74208b88c5699ee62de55ac9a62ff4c208600224
Author: t <t@t>
Date:   Thu Nov 12 13:06:11 2026 +0100

    m

M	sub12
$ git reset --soft HEAD~1 exit=0 stderr=''
porcelain after reset --soft:
 M qa-factory/x.txt
M  sub12
?? qa-factory/new.txt

=== class 12 submodule pointer | variant raw | cmd S ===
porcelain BEFORE:
 M qa-factory/x.txt
 M sub12
?? qa-factory/new.txt
paths passed: ['sub12']
$ git stash push --include-untracked -m m -- sub12
  exit=0
  stdout='No local changes to save'
  stderr=''
porcelain AFTER:
 M qa-factory/x.txt
 M sub12
?? qa-factory/new.txt
$ git stash show --include-untracked --name-status stash@{0}

$ git stash pop exit=128
  stderr='No stash entries found.'
porcelain after pop:
 M qa-factory/x.txt
 M sub12
?? qa-factory/new.txt

=== class 13 ALL 1-9 together | variant raw | cmd C ===
porcelain BEFORE:
A  add8.txt
 D del6.txt
D  del7.txt
 M m3.txt
M  m4.txt
MM m5.txt
R  old9.txt -> new9.txt
 M qa-factory/x.txt
?? d2/
?? qa-factory/new.txt
?? u1.txt
paths passed: ['add8.txt', 'del6.txt', 'del7.txt', 'm3.txt', 'm4.txt', 'm5.txt', 'old9.txt', 'new9.txt', 'd2/', 'u1.txt']
$ git add -- add8.txt del6.txt del7.txt m3.txt m4.txt m5.txt old9.txt new9.txt d2/ u1.txt
  exit=128
  stdout=''
  stderr="fatal: pathspec 'del7.txt' did not match any files"
porcelain AFTER:
A  add8.txt
 D del6.txt
D  del7.txt
 M m3.txt
M  m4.txt
MM m5.txt
R  old9.txt -> new9.txt
 M qa-factory/x.txt
?? d2/
?? qa-factory/new.txt
?? u1.txt
$ git show --stat --name-status HEAD
commit 87e144d1ac4f5f98763d6bf23d61619785060903
Author: t <t@t>
Date:   Thu Nov 12 13:06:18 2026 +0100

    base

A	del6.txt
A	del7.txt
A	m3.txt
A	m4.txt
A	m5.txt
A	old9.txt
A	qa-factory/x.txt
  content m4.txt: HEAD='base' worktree='staged'
  content m5.txt: HEAD='base' worktree='worktree'

=== class 13 ALL 1-9 together | variant raw | cmd S ===
porcelain BEFORE:
A  add8.txt
 D del6.txt
D  del7.txt
 M m3.txt
M  m4.txt
MM m5.txt
R  old9.txt -> new9.txt
 M qa-factory/x.txt
?? d2/
?? qa-factory/new.txt
?? u1.txt
paths passed: ['add8.txt', 'del6.txt', 'del7.txt', 'm3.txt', 'm4.txt', 'm5.txt', 'old9.txt', 'new9.txt', 'd2/', 'u1.txt']
$ git stash push --include-untracked -m m -- add8.txt del6.txt del7.txt m3.txt m4.txt m5.txt old9.txt new9.txt d2/ u1.txt
  exit=128
  stdout='Saved working directory and index state On master: m'
  stderr="warning: in the working copy of 'd2/a.txt', LF will be replaced by CRLF the next time Git touches it\nwarning: in the working copy of 'd2/b.txt', LF will be replaced by CRLF the next time Git touches it\nwarning: in the working copy of 'u1.txt', LF will be replaced by CRLF the next time Git touches it\nwarning: in the working copy of 'm3.txt', LF will be replaced by CRLF the next time Git touches it\nwarning: in the working copy of 'm5.txt', LF will be replaced by CRLF the next time Git touches it\nfatal: pathspec ':(prefix:0)del7.txt' did not match any files"
porcelain AFTER:
A  add8.txt
 D del6.txt
D  del7.txt
 M m3.txt
M  m4.txt
MM m5.txt
R  old9.txt -> new9.txt
 M qa-factory/x.txt
?? d2/
?? qa-factory/new.txt
?? u1.txt
$ git stash show --include-untracked --name-status stash@{0}
A	add8.txt
A	d2/a.txt
A	d2/b.txt
D	del6.txt
D	del7.txt
M	m3.txt
M	m4.txt
M	m5.txt
R100	old9.txt	new9.txt
A	u1.txt

=== class 13 ALL 1-9 together | variant raw | cmd S (pop --index) ===
porcelain BEFORE:
A  add8.txt
 D del6.txt
D  del7.txt
 M m3.txt
M  m4.txt
MM m5.txt
R  old9.txt -> new9.txt
 M qa-factory/x.txt
?? d2/
?? qa-factory/new.txt
?? u1.txt
paths passed: ['add8.txt', 'del6.txt', 'del7.txt', 'm3.txt', 'm4.txt', 'm5.txt', 'old9.txt', 'new9.txt', 'd2/', 'u1.txt']
$ git stash push --include-untracked -m m -- add8.txt del6.txt del7.txt m3.txt m4.txt m5.txt old9.txt new9.txt d2/ u1.txt
  exit=128
  stdout='Saved working directory and index state On master: m'
  stderr="warning: in the working copy of 'd2/a.txt', LF will be replaced by CRLF the next time Git touches it\nwarning: in the working copy of 'd2/b.txt', LF will be replaced by CRLF the next time Git touches it\nwarning: in the working copy of 'u1.txt', LF will be replaced by CRLF the next time Git touches it\nwarning: in the working copy of 'm3.txt', LF will be replaced by CRLF the next time Git touches it\nwarning: in the working copy of 'm5.txt', LF will be replaced by CRLF the next time Git touches it\nfatal: pathspec ':(prefix:0)del7.txt' did not match any files"
porcelain AFTER:
A  add8.txt
 D del6.txt
D  del7.txt
 M m3.txt
M  m4.txt
MM m5.txt
R  old9.txt -> new9.txt
 M qa-factory/x.txt
?? d2/
?? qa-factory/new.txt
?? u1.txt
$ git stash show --include-untracked --name-status stash@{0}
A	add8.txt
A	d2/a.txt
A	d2/b.txt
D	del6.txt
D	del7.txt
M	m3.txt
M	m4.txt
M	m5.txt
R100	old9.txt	new9.txt
A	u1.txt


TABLE (C = add+commit; S = stash -u; restored = C: reset --soft HEAD~1 equals BEFORE porcelain / S: stash pop equals BEFORE porcelain)
| class | variant | cmd | exit | took exactly the listed | qa-factory untouched | restores BEFORE |
|---|---|---|---|---|---|---|
| 1 ?? untracked file | raw | C | 0 | yes | yes | no |
| 1 ?? untracked file | raw | S | 0 | yes | yes | yes |
| 2 ?? untracked folder | raw | C | 0 | yes | yes | no |
| 2 ?? untracked folder | raw | S | 0 | yes | yes | yes |
| 3 ' M' modified unstaged | raw | C | 0 | yes | yes | no |
| 3 ' M' modified unstaged | raw | S | 0 | yes | yes | yes |
| 4 'M ' modified staged | raw | C | 0 | yes | yes | yes |
| 4 'M ' modified staged | raw | S | 0 | yes | yes | no |
| 4 'M ' modified staged | raw | S-idx | 0 | yes | yes | yes |
| 5 'MM' staged+modified | raw | C | 0 | yes | yes | no |
| 5 'MM' staged+modified | raw | S | 0 | yes | yes | no |
| 5 'MM' staged+modified | raw | S-idx | 0 | yes | yes | yes |
| 6 ' D' deleted unstaged | raw | C | 0 | yes | yes | no |
| 6 ' D' deleted unstaged | raw | S | 0 | yes | yes | yes |
| 7 'D ' deleted staged | raw | C | 128 | no | yes | n/a |
| 7 'D ' deleted staged | raw | S | 128 | no | yes | n/a |
| 8 'A ' added staged | raw | C | 0 | yes | yes | yes |
| 8 'A ' added staged | raw | S | 0 | yes | yes | yes |
| 9 'R ' rename (both sides) | raw | C | 128 | no | yes | n/a |
| 9 'R ' rename (both sides) | raw | S | 128 | no | yes | n/a |
| 10 space in path | quoted-as-is | C | 128 | no | yes | n/a |
| 10 space in path | quoted-as-is | S | 0 | no | yes | yes |
| 10 space in path | unquoted-real | C | 0 | yes | yes | no |
| 10 space in path | unquoted-real | S | 0 | yes | yes | yes |
| 11 non-ASCII in path | quoted-as-is | C | 128 | no | yes | n/a |
| 11 non-ASCII in path | quoted-as-is | S | 0 | no | yes | yes |
| 11 non-ASCII in path | unquoted-real | C | 0 | yes | yes | no |
| 11 non-ASCII in path | unquoted-real | S | 0 | yes | yes | yes |
| 12 submodule pointer | raw | C | 0 | yes | yes | no |
| 12 submodule pointer | raw | S | 0 | no | yes | yes |
| 13 ALL 1-9 together | raw | C | 128 | no | yes | n/a |
| 13 ALL 1-9 together | raw | S | 128 | no | yes | n/a |
| 13 ALL 1-9 together | raw | S-idx | 128 | no | yes | n/a |
```

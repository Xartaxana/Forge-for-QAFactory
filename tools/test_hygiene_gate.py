"""tools/hygiene_gate.py: four refusals (cd, content write by a literal target in a git working tree, journal write,
rollback of dirty paths), one WARN, silence for everything else (spec docs/tasks/specs/fg-context-and-hygiene.md, C1).

Layer 3: ONE parameterised table over `decide()` (ROWS). The trees are made in tmp_path: `tree` and `tree2` hold a `.git`
(a directory / a file, like a worktree), `scratch` holds none; rollback rows run in real `git init` repositories
(`repo` dirty, `clean` clean with one ignored file). Each refusal row asserts its door text. Outside the table: the
text budget of the constants, the process-level reader (BOM, empty and broken JSON) and one 100 KB / 1 MB ratio check.
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path, PurePosixPath

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import gitcmd  # noqa: E402
import hygiene_gate as hg  # noqa: E402

SCRIPT = Path(__file__).resolve().parent / "hygiene_gate.py"
ROOT = hg._REPO_ROOT_NAME

DOORS = {
    "cd_bash": "( cd <dir> && ... ) subshell",
    "cd_ps": "powershell -NoProfile -Command",
    "mutation": "Edit/Write your handoff file",
    "journal": "Reading it with grep, cat or tail is fine",
    "rollback": "leave them and tell the Lead",
}


def _git(repo, *args):
    subprocess.run(["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@t", *args],
                   check=True, capture_output=True)


def _make_repo(path: Path, dirty: bool):
    path.mkdir(parents=True)
    (path / "docs").mkdir()
    _git(path, "init", "-q")
    (path / ".gitignore").write_text("*.log\n", encoding="utf-8")
    (path / "f.py").write_text("a\n", encoding="utf-8")
    (path / "docs" / "d.md").write_text("d\n", encoding="utf-8")
    (path / "sub").mkdir()
    (path / "sub" / "s.py").write_text("s\n", encoding="utf-8")
    _git(path, "add", "-A")
    _git(path, "commit", "-qm", "init")
    (path / "i.log").write_text("ignored\n", encoding="utf-8")
    if dirty:
        (path / "f.py").write_text("changed\n", encoding="utf-8")
        (path / "sub" / "s.py").write_text("changed\n", encoding="utf-8")
        (path / "docs" / "u.md").write_text("untracked\n", encoding="utf-8")


@pytest.fixture(scope="module")
def world(tmp_path_factory):
    base = tmp_path_factory.mktemp("hyg")
    tree, tree2, scratch = base / "tree", base / "tree2", base / "scratch"
    (tree / ".git").mkdir(parents=True)
    (tree / "docs").mkdir()
    tree2.mkdir()
    (tree2 / ".git").write_text("gitdir: elsewhere\n", encoding="utf-8")
    scratch.mkdir()
    repo, clean = base / "repo", base / "clean"
    _make_repo(repo, dirty=True)
    _make_repo(clean, dirty=False)
    return {"tree": tree, "tree2": tree2, "scratch": scratch, "repo": repo, "clean": clean,
            "repo_msys": _msys(repo), "tree_msys": _msys(tree)}


def _msys(path: Path) -> PurePosixPath:
    """`C:\\dir` as the MSYS spelling `/c/dir` (a POSIX path stays as it is)."""
    p = path.as_posix()
    return PurePosixPath(f"/{p[0].lower()}{p[2:]}" if len(p) > 2 and p[1] == ":" else p)


@pytest.fixture(autouse=True)
def _no_git_env(monkeypatch):
    monkeypatch.delenv("GIT_DIR", raising=False)
    monkeypatch.delenv("GIT_WORK_TREE", raising=False)


def _decide(command, tool, cwd):
    return hg.decide({"tool_name": tool, "tool_input": {"command": command}, "cwd": str(cwd)})


def _kind(output):
    if output is None:
        return "silent"
    hso = output["hookSpecificOutput"]
    if hso.get("permissionDecision") == "deny":
        return "deny"
    ctx = hso["additionalContext"]
    if ctx.startswith(hg.WARN_PREFIX):
        return "warn"
    return "marker" if "rollback not checked" in ctx else "other:" + ctx


# (id, command, tool, cwd, expect): expect = "silent" | "warn" | ("deny", door) | ("marker", text)
S, W = "silent", "warn"
B, P = "Bash", "PowerShell"
JNL = "logs/journal/dev1.jsonl"
SILENT = [
    ("grep-journal-devnull", f"grep x {JNL} 2>/dev/null", B, "tree", S),
    ("grep-journal-2to1-head", f"grep -n y {JNL} 2>&1 | head -5", B, "tree", S),
    ("grep-echo-word", f'grep -c "echo" {JNL}', B, "tree", S),
    ("ls-journal-2to1", f"ls {JNL} 2>&1", B, "tree", S),
    ("py-heredoc-read-journal-and-gt", "python - <<'PY'\nprint('logs/journal/dev1.jsonl > x')\nPY", B, "tree", S),
    ("py-replace", "python -c \"print('a/b'.replace('/','-'))\"", B, "tree", S),
    ("py-json-dump-stdout", "python -c \"import json,sys; json.dump({'a':1}, sys.stdout)\"", B, "tree", S),
    ("py-stdout-buffer", "python -c \"import sys; sys.stdout.buffer.write(b'x')\"", B, "tree", S),
    ("py-csv-stdout", "python -c \"import csv,sys; csv.writer(sys.stdout).writerow([1])\"", B, "tree", S),
    ("py-open-scratch", "python -c \"open(r'{scratch}/f.txt','w').write('x')\"", B, "tree", S),
    ("py-read", "python -c \"print(open('a').read())\"", B, "tree", S),
    ("py-B-c-print", 'python -B -c "print(1)"', B, "tree", S),
    ("py-os-remove", "python -c \"import os; os.remove('docs/a.md')\"", B, "tree", S),
    ("py-named-script", "python -B tools/x.py", B, "tree", S),
    ("py-m-pytest", "python -m pytest tools/ -q", B, "tree", S),
    ("rm-file", "rm docs/a.md", B, "tree", S),
    ("cp-onto-tree", "cp x docs/a.md", B, "tree", S),
    ("commit-message-gt", 'git commit -m "fix > 3 cases"', B, "tree", S),
    ("commit-heredoc-message", "git commit -F - <<'EOF'\nfix > docs/a.md\nEOF", B, "tree", S),
    ("echo-scratch", "echo x > {scratch}/f.txt", B, "tree", S),
    ("null-sinks", "echo x > /dev/null; echo y > $null; echo z > NUL; echo w > nul", B, "tree", S),
    ("non-literal-target", 'echo x > "$out"', B, "tree", S),
    ("env-target", "echo x > $env:TEMP\\f.txt", P, "tree", S),
    ("ignore-row-ci-out", "echo x > ci-out/log.txt", B, "tree", S),
    ("under-dot-git", "echo x > .git/info/exclude", B, "tree", S),
    ("bash-subshell-cd", "( cd sub && make )", B, "tree", S),
    ("bash-subshell-cd-subst", "x=$(cd sub && pwd)", B, "tree", S),
    ("bash-c-child-cd", 'bash -c "cd x && ls"', B, "tree", S),
    ("ps-child-shell-cd", 'powershell -NoProfile -Command "Set-Location x; ls"', P, "tree", S),
    ("bare-cd-root", f"cd {ROOT}", B, "tree", S),
    ("bare-cd-root-quoted-ps", f"Set-Location -Path '{ROOT}'", P, "tree", S),
    ("cd-in-comment", "ls # then cd x; cd y", B, "tree", S),
    ("echo-cd-word", "echo cd x", B, "tree", S),
    ("compound-no-cd", "git status && git log -1 | head -3; ls", B, "tree", S),
    ("leading-var", "FOO=1 ls", B, "tree", S),
    ("2to1-everywhere", "python tools/x.py 2>&1", P, "tree", S),
    ("sed-no-inplace", "sed -n 1p docs/a.md", B, "tree", S),
    ("cat-read", "cat docs/a.md", B, "tree", S),
    ("sed-i-scratch", "sed -i s/a/b/ {scratch}/f.txt", B, "tree", S),
    ("ps-dotnet-scratch", "[IO.File]::WriteAllText('{scratch}\\f.txt','x')", P, "tree", S),
    ("checkout-untracked-only-scope", "git checkout -- docs/", B, "repo", S),
    ("checkout-branch-no-such-file", "git checkout main", B, "repo", S),
    ("checkout-b", "git checkout -b newbranch", B, "repo", S),
    ("restore-staged-only", "git restore --staged f.py", B, "repo", S),
    ("clean-dry-run", "git clean -n", B, "repo", S),
    ("clean-f-nothing-untracked", "git clean -f", B, "clean", S),
    ("clean-f-only-ignored", "git clean -f", B, "clean", S),
    ("other-tree-clean-cwd-dirty", "git -C {clean} restore f.py", B, "repo", S),
    ("stash-list", "git stash list", B, "repo", S),
    ("stash-push-clean-scope", "git stash push -- f.py", B, "clean", S),
    ("stash-drop-residual", "git stash drop", B, "repo", S),
    ("reset-soft", "git reset --soft HEAD~1", B, "repo", S),
    ("non-bash-tool-handled-elsewhere", "cd docs && ls", "Read", "tree", S),
]
WARN_ONLY = [
    ("py-stringio-write", "python -c \"import io; io.StringIO().write('x')\"", B, "tree", W),
    ("py-open-variable-path", "python -c \"p='a.txt'; open(p,'w').write('x')\"", B, "tree", W),
    ("py-exec", "python -c \"exec('x=1')\"", B, "tree", W),
    ("py-parse-failure", 'python -c "def ("', B, "tree", W),
    ("py-dynamic-dq", 'python -c "print($X)"', B, "tree", W),
]
MUTATION = [
    ("redirect", "echo x > docs/a.md", B, "tree", ("deny", DOORS["mutation"])),
    ("redirect-append-quoted", "echo x >> 'docs/a b.md'", B, "tree", ("deny", DOORS["mutation"])),
    ("redirect-2gt", "echo x 2> docs/err.txt", B, "tree", ("deny", DOORS["mutation"])),
    ("cat-heredoc", "cat > docs/a.md <<EOF\nx\nEOF", B, "tree", ("deny", DOORS["mutation"])),
    ("sed-i", "sed -i 's/a/b/' docs/a.md", B, "tree", ("deny", DOORS["mutation"])),
    ("sed-i-e", "sed -i -e 's/a/b/' docs/a.md", B, "tree", ("deny", DOORS["mutation"])),
    ("perl-pi", "perl -pi -e s/a/b/ docs/a.md", B, "tree", ("deny", DOORS["mutation"])),
    ("awk-inplace", "awk -i inplace '{print}' docs/a.md", B, "tree", ("deny", DOORS["mutation"])),
    ("ruby-i", "ruby -i -pe '$_.upcase!' docs/a.md", B, "tree", ("deny", DOORS["mutation"])),
    ("tee", "echo x | tee docs/a.md", B, "tree", ("deny", DOORS["mutation"])),
    ("set-content", "Set-Content docs\\a.md x", P, "tree", ("deny", DOORS["mutation"])),
    ("out-file", "Out-File -FilePath docs\\a.md", P, "tree", ("deny", DOORS["mutation"])),
    ("add-content-value-first", "Add-Content -Value x docs\\a.md", P, "tree", ("deny", DOORS["mutation"])),
    ("dotnet-write", "[IO.File]::WriteAllText('docs\\a.md','x')", P, "tree", ("deny", DOORS["mutation"])),
    ("py-open-w", "python -c \"open('docs/a.md','w').write('x')\"", B, "tree", ("deny", DOORS["mutation"])),
    ("py-B-c", "python -B -c \"open('docs/a.md','w').write('x')\"", B, "tree", ("deny", DOORS["mutation"])),
    ("python3-c", "python3 -c \"open('docs/a.md','w').write('x')\"", B, "tree", ("deny", DOORS["mutation"])),
    ("py-3-c", "py -3 -c \"open('docs/a.md','w').write('x')\"", P, "tree", ("deny", DOORS["mutation"])),
    ("py-heredoc-open", "python - <<'PY'\nopen('docs/a.md','a').write('x')\nPY", B, "tree", ("deny", DOORS["mutation"])),
    ("py-path-write-text", "python -c \"from pathlib import Path; Path('docs/a.md').write_text('x')\"", B, "tree",
     ("deny", DOORS["mutation"])),
    ("py-json-dump-open", "python -c \"import json; json.dump({}, open('docs/a.json','w'))\"", B, "tree",
     ("deny", DOORS["mutation"])),
    ("env-prefix", "PYTHONUTF8=1 python -c \"open('docs/a.md','w')\"", B, "tree", ("deny", DOORS["mutation"])),
    ("cross-tree", "echo x > {tree}/docs/a.md", B, "tree2", ("deny", DOORS["mutation"])),
    ("new-dir-inside-tree", "echo x > docs/newdir/deeper/a.md", B, "tree", ("deny", DOORS["mutation"])),
    ("git-show-redirect", "git show HEAD:f > docs/a.md", B, "tree", ("deny", DOORS["mutation"])),
    ("crlf", "echo x > docs/a.md\r\nls\r\n", B, "tree", ("deny", DOORS["mutation"])),
    ("cyrillic-space-path", 'echo x > "docs/привет мир.md"', B, "tree", ("deny", DOORS["mutation"])),
]
JOURNAL = [
    ("append", f"echo x >> {JNL}", B, "tree", ("deny", DOORS["journal"])),
    ("tee-a", f"tee -a {JNL}", B, "tree", ("deny", DOORS["journal"])),
    ("add-content", "Add-Content logs\\journal\\dev1.jsonl x", P, "tree", ("deny", DOORS["journal"])),
    ("py-open-a", f"python -c \"open('{JNL}','a').write('x')\"", B, "tree", ("deny", DOORS["journal"])),
    ("sed-i", f"sed -i s/a/b/ {JNL}", B, "tree", ("deny", DOORS["journal"])),
    ("routing-log", "echo x >> logs/routing-log.jsonl", B, "tree", ("deny", DOORS["journal"])),
    ("outside-any-tree", "echo x >> {scratch}/logs/journal/dev1.jsonl", B, "scratch", ("deny", DOORS["journal"])),
]
CD = [
    ("cd-and", "cd docs && ls", B, "tree", ("deny", DOORS["cd_bash"])),
    ("cd-worktree-root-git-grep", f"cd /x/{ROOT} && git grep -n x", B, "tree", ("deny", DOORS["cd_bash"])),
    ("set-location", "Set-Location docs; ls", P, "tree", ("deny", DOORS["cd_ps"])),
    ("pushd", "pushd docs && ls", B, "tree", ("deny", DOORS["cd_bash"])),
    ("popd", "popd", B, "tree", ("deny", DOORS["cd_bash"])),
    ("push-location", "Push-Location x", P, "tree", ("deny", DOORS["cd_ps"])),
    ("sl", "sl x", P, "tree", ("deny", DOORS["cd_ps"])),
    ("chdir", "chdir x", B, "tree", ("deny", DOORS["cd_bash"])),
    ("eval-cd", 'eval "cd x"', B, "tree", ("deny", DOORS["cd_bash"])),
    ("brace-group", "{ cd x; }", B, "tree", ("deny", DOORS["cd_bash"])),
    ("if-then", "if true; then cd x; fi", B, "tree", ("deny", DOORS["cd_bash"])),
    ("for-do", "for d in a; do cd $d; done", B, "tree", ("deny", DOORS["cd_bash"])),
    ("second-statement", "ls; cd x", B, "tree", ("deny", DOORS["cd_bash"])),
    ("builtin", "builtin cd x", B, "tree", ("deny", DOORS["cd_bash"])),
    ("bare", "cd", B, "tree", ("deny", DOORS["cd_bash"])),
    ("dash", "cd -", B, "tree", ("deny", DOORS["cd_bash"])),
    ("dotnet-setcwd", "[IO.Directory]::SetCurrentDirectory('x')", P, "tree", ("deny", DOORS["cd_ps"])),
    ("ps-subshell", "( cd sub; ls )", P, "tree", ("deny", DOORS["cd_ps"])),
    ("root-with-continuation", f"cd {ROOT} && ls", B, "tree", ("deny", DOORS["cd_bash"])),
]
ROLLBACK = [
    ("checkout-dd-path", "git checkout -- f.py", B, "repo", ("deny", DOORS["rollback"])),
    ("checkout-rev-path", "git checkout HEAD f.py", B, "repo", ("deny", DOORS["rollback"])),
    ("checkout-rev-dd-path", "git checkout HEAD -- f.py", B, "repo", ("deny", DOORS["rollback"])),
    ("checkout-one-file-arg", "git checkout f.py", B, "repo", ("deny", DOORS["rollback"])),
    ("checkout-dot", "git checkout .", B, "repo", ("deny", DOORS["rollback"])),
    ("checkout-f", "git checkout -f", B, "repo", ("deny", DOORS["rollback"])),
    ("switch-discard", "git switch --discard-changes main", B, "repo", ("deny", DOORS["rollback"])),
    ("restore", "git restore f.py", B, "repo", ("deny", DOORS["rollback"])),
    ("restore-worktree-staged", "git restore --worktree --staged f.py", B, "repo", ("deny", DOORS["rollback"])),
    ("reset-hard", "git reset --hard", B, "repo", ("deny", DOORS["rollback"])),
    ("global-opts", "git -c core.x=y --no-pager checkout -- f.py", B, "repo", ("deny", DOORS["rollback"])),
    ("dash-C-other-dirty", "git -C {repo} restore f.py", B, "clean", ("deny", DOORS["rollback"])),
    ("clean-fd", "git clean -fd", B, "repo", ("deny", DOORS["rollback"])),
    ("clean-xdf-ignored-only", "git clean -xdf", B, "clean", ("deny", DOORS["rollback"])),
    ("clean-fX-ignored", "git clean -fX", B, "clean", ("deny", DOORS["rollback"])),
    ("stash", "git stash", B, "repo", ("deny", DOORS["rollback"])),
    ("stash-push-scope", "git stash push -- f.py", B, "repo", ("deny", DOORS["rollback"])),
]
MARKERS = [
    ("git-dir-env", "git checkout -- f.py", B, "repo", ("marker", "GIT_DIR")),
    ("git-dir-flag", "git --git-dir=x checkout -- f.py", B, "repo", ("marker", "unresolvable")),
    ("dir-absent", "git -C {scratch}/nope restore f.py", B, "repo", ("marker", "addressed directory absent")),
    ("non-literal-path", "git checkout -- $f", B, "repo", ("marker", "non-literal path")),
]
BIG = "x" * 100_000
ADVERSARIAL = [
    ("100kb-benign", "echo " + BIG, B, "tree", S),
    ("100kb-redirect", "echo " + BIG + " > docs/a.md", B, "tree", ("deny", DOORS["mutation"])),
    ("1mb-payload-over-limit", "python -c \"print('" + "a" * 1_000_000 + "')\"", B, "tree", W),
    ("1mb-redirect", "echo " + "x" * 1_000_000 + " > docs/a.md", B, "tree", ("deny", DOORS["mutation"])),
    ("many-statements", "ls; " * 20_000 + "echo x > docs/a.md", B, "tree", ("deny", DOORS["mutation"])),
    ("65-heredoc-openers", "".join(f"cat > docs/a{i}.md <<E{i}\nbody\nE{i}\n" for i in range(65)), B, "tree", S),
    ("2-heredoc-openers-redirect", "cat > docs/a.md <<A\nx\nA\ncat > docs/b.md <<B\ny\nB\n", B, "tree",
     ("deny", DOORS["mutation"])),
    ("heredoc-inside-quotes", 'echo "<<EOF > docs/a.md"', B, "tree", S),
    ("quotes-inside-heredoc", "cat <<'EOF'\nsay \"hi > docs/a.md\" it's\nEOF", B, "tree", S),
    ("unclosed-quote", "echo 'unterminated > docs/a.md", B, "tree", S),
    ("python-open-many-unclosed", 'python -c "' * 5000, B, "tree", W),
    ("cyrillic-scratch", "echo привет > {scratch}/файл.txt", B, "tree", S),
    ("empty-payload", 'python -c ""', B, "tree", S),
    ("unbalanced-parens", "))) ((( echo x", B, "tree", S),
    ("nul-in-command", "echo a\x00b > docs/a.md", B, "tree", ("deny", DOORS["mutation"])),
]
MU, JO, CDB, CDP, RB = (("deny", DOORS[k]) for k in ("mutation", "journal", "cd_bash", "cd_ps", "rollback"))
# Round 2 (critic t-112 C1): each row was red before its fix.
ROUND2 = [
    # B-1: a comparison is never a redirect; a real redirect after the closing bracket still is
    ("b1-arith-if", "if (( n > 5 )); then echo big; fi", B, "tree", S),
    ("b1-arith-subst", "echo $(( 3 > 2 ))", B, "tree", S),
    ("b1-arith-and", "(( count > 0 )) && echo yes", B, "tree", S),
    ("b1-dbl-bracket", "[[ abc > abb ]] && echo yes", B, "tree", S),
    ("b1-for-arith", "for ((i=10; i > 0; i--)); do echo $i; done", B, "tree", S),
    ("b1-arith-ge", "x=$(( a >= b ? 1 : 0 ))", B, "tree", S),
    ("b1-redirect-after-arith", "(( n > 5 )) && echo x > docs/a.md", B, "tree", MU),
    ("b1-redirect-after-dbl-bracket", "[[ a > b ]] && echo x > docs/a.md", B, "tree", MU),
    ("b1-powershell-row-has-no-regions", "[[ a > docs/a.md ]]", P, "tree", MU),
    # B-2: every rollback shape is measured
    ("b2-clean-then-hard", "git checkout -- docs/d.md && git reset --hard", B, "repo", RB),
    ("b2-status-then-checkout", "git status; git checkout -- f.py", B, "repo", RB),
    ("b2-clean-repo-then-dirty-repo", "git -C {clean} reset --hard && git -C {repo} reset --hard", B, "clean", RB),
    # B-3: a literal cd in a group scopes that group only
    ("b3-subshell-cd-clean-repo", "( cd {clean} && git reset --hard )", B, "repo", S),
    ("b3-subshell-cd-rel-rollback", "( cd sub && git checkout -- s.py )", B, "repo", RB),
    ("b3-subshell-cd-nested", "( cd docs && ( cd .. && git checkout -- f.py ) )", B, "repo", RB),
    ("b3-subshell-cd-journal", "( cd logs/journal && echo x >> dev1.jsonl )", B, "tree", JO),
    ("b3-subshell-cd-redirect", "( cd docs && echo x > a.md )", B, "tree", MU),
    ("b3-subshell-cd-payload", "( cd docs && python -c \"open('a.md','w')\" )", B, "tree", MU),
    ("b3-after-group-closed", "( cd sub && make ); echo x > docs/a.md", B, "tree", MU),
    ("b3-after-substitution-closed", "d=$(cd docs && pwd); echo x > docs/a.md", B, "tree", MU),
    ("b3-nonliteral-cd-rollback", "( cd $d && git reset --hard )", B, "repo", ("marker", "unresolvable")),
    ("b3-nonliteral-cd-redirect", "( cd $d && echo x > f.txt )", B, "tree", S),
    ("b3-nonliteral-cd-journal", "( cd $d && echo x >> dev1.jsonl )", B, "tree", S),
    ("b3-nonliteral-cd-does-not-leak", "( cd $d ); git reset --hard", B, "repo", RB),
    ("b3-absolute-cd-in-group", "( cd /nowhere-zz && cd {tree} && echo x > docs/a.md )", B, "scratch", MU),
    # F-1: tee writes every operand
    ("f1-tee-devnull-first", "printf x | tee /dev/null docs/a.md", B, "tree", MU),
    ("f1-tee-two-files", "printf x | tee {scratch}/x docs/a.md", B, "tree", MU),
    ("f1-tee-journal-second", "printf x | tee /dev/null logs/journal/dev1.jsonl", B, "tree", JO),
    ("f1-tee-no-operand", "printf x | tee", B, "tree", S),
    ("f1-tee-append-null-only", "printf x | tee -a /dev/null", B, "tree", S),
    ("f1-tee-outside-only", "printf x | tee -a {scratch}/x {scratch}/y", B, "tree", S),
    # F-2: aliases and an assignment prefix
    ("f2-sc-alias", "sc docs\\a.md x", P, "tree", MU),
    ("f2-ac-alias-journal", "ac logs\\journal\\dev1.jsonl x", P, "tree", JO),
    ("f2-assign-prefix-cd", "$null = Set-Location docs", P, "tree", CDP),
    ("f2-assign-prefix-write", "$r = Set-Content docs\\a.md x", P, "tree", MU),
    ("f2-assign-prefix-read", "$x = Get-Content docs\\a.md", P, "tree", S),
    # F-3: PowerShell quotes escape with the backtick; a trailing backslash closes the string
    ("f3-ps-trailing-backslash-cd", 'Get-Item "C:\\x\\"; Set-Location docs; "y"', P, "tree", CDP),
    ("f3-ps-trailing-backslash-redirect", 'Get-ChildItem "C:\\QAFactory\\" > docs\\a.md', P, "tree", MU),
    ("f3-ps-trailing-backslash-journal", 'Get-Item "C:\\x\\"; Add-Content logs\\journal\\dev1.jsonl x; "y"', P, "tree", JO),
    ("f3-ps-backtick-escaped-quote", 'Write-Output "a`"b" > docs\\a.md', P, "tree", MU),
    ("f3-ps-quote-doubled", "Write-Output 'it''s > docs\\a.md'", P, "tree", S),
    ("f3-bash-escaped-quote-still-escapes", 'echo "a\\"b > docs/a.md"', B, "tree", S),
    # F-5: an MSYS path is translated before resolution; one that still does not exist is unresolved
    ("f5-msys-git-C", "git -C {repo_msys} reset --hard", B, "scratch", RB),
    ("f5-msys-redirect", "echo x > {tree_msys}/docs/a.md", B, "scratch", MU),
    ("f5-msys-absent-dir", "git -C /c/nonexistent-zz-dir reset --hard", B, "scratch", ("marker", "addressed directory absent")),
    ("f5-msys-absent-redirect", "echo x > /c/nonexistent-zz-dir/a.md", B, "scratch", S),
    # F-6: an alias of open
    ("f6-io-open-alias", "python -c \"from io import open as o; o('docs/a.md','w').write('x')\"", B, "tree", MU),
    # F-7: a colon-bound parameter
    ("f7-path-colon-scratch", "Set-Content -Path:{scratch}\\o.txt hello", P, "tree", S),
    ("f7-path-colon-tree", "Set-Content -Path:docs\\a.md hello", P, "tree", MU),
    ("f7-value-colon-then-path", "Set-Content -Value:hello docs\\a.md", P, "tree", MU),
    # F-8: the journal is logs/journal/*.jsonl and logs/routing-log.jsonl, nothing else
    ("f8-scratch-jsonl-outside", "python -B tools/x.py > {scratch}/logs/out.jsonl", B, "tree", S),
    ("f8-other-jsonl-in-tree", "echo x > logs/out.jsonl", B, "tree", MU),
    ("f8-routing-log-backslash", "echo x >> logs\\routing-log.jsonl", B, "tree", JO),
    ("f8-routing-log-lookalike", "echo x > {scratch}/routing-log.jsonl.bak", B, "tree", S),
    ("f8-journal-subdir-not-journal", "echo x > {scratch}/logs/journal/sub/x.txt", B, "tree", S),
    # F-14: a child shell's payload is a named residual (a data row), not read
    ("f14-bash-c-write", 'bash -c "echo x > docs/a.md"', B, "tree", S),
    ("f14-cmd-c-write", 'cmd /c "echo x > docs\\a.md"', P, "tree", S),
]
ROWS = SILENT + WARN_ONLY + MUTATION + JOURNAL + CD + ROLLBACK + MARKERS + ADVERSARIAL + ROUND2


@pytest.mark.parametrize("name,command,tool,cwd,expect", ROWS, ids=[r[0] for r in ROWS])
def test_decide_table(world, monkeypatch, name, command, tool, cwd, expect):
    paths = {k: v.as_posix() for k, v in world.items()}
    for key, value in paths.items():
        command = command.replace("{" + key + "}", value)
    if name == "git-dir-env":
        monkeypatch.setenv("GIT_DIR", "x")
    code, out = _decide(command, tool, world[cwd])
    assert code == 0
    if expect in (S, W):
        assert _kind(out) == expect, out
        if expect == W:
            assert out["hookSpecificOutput"]["additionalContext"] == hg.WARN_PREFIX + hg.MSG_WARN_PAYLOAD
        return
    kind, text = expect
    assert _kind(out) == ("deny" if kind == "deny" else "marker"), out
    hso = out["hookSpecificOutput"]
    assert text in (hso["permissionDecisionReason"] if kind == "deny" else hso["additionalContext"]), out
    if kind == "deny":
        assert text in hso["additionalContext"] and "hookEventName" in hso


def test_order_when_several_fire(world):
    cmd = f"echo x >> {JNL}; git reset --hard; cd x; echo y > docs/a.md"
    _code, out = _decide(cmd, B, world["repo"])
    hso = out["hookSpecificOutput"]
    assert hso["permissionDecisionReason"] == hg.MSG_JOURNAL_BLOCK
    ctx = hso["additionalContext"]
    positions = [ctx.index(DOORS[k]) for k in ("journal", "rollback", "cd_bash")]
    assert positions == sorted(positions)
    assert "journal target: " + JNL in ctx


def test_refused_command_never_gets_the_warn_as_its_reason(world):
    _code, out = _decide("python -c \"exec('1')\"; echo x > docs/a.md", B, world["tree"])
    hso = out["hookSpecificOutput"]
    assert hso["permissionDecisionReason"] != hg.MSG_WARN_PAYLOAD and hg.MSG_WARN_PAYLOAD in hso["additionalContext"]


def test_rollback_git_status_unmeasurable_passes_with_marker(world, monkeypatch):
    monkeypatch.setattr(gitcmd, "git", lambda *a, **k: (-1, b"git missing"))
    code, out = _decide("git checkout -- f.py", B, world["repo"])
    assert code == 0 and _kind(out) == "marker"
    assert "permissionDecision" not in out["hookSpecificOutput"]
    assert out["hookSpecificOutput"]["additionalContext"] == hg.DENY_PREFIX + "rollback not checked: git status did not run (rc -1)"


def test_rollback_measurement_raising_is_a_marker_never_a_refusal(world, monkeypatch):
    def boom(*a, **k):
        raise OSError("disk on fire")
    monkeypatch.setattr(gitcmd, "git", boom)
    _code, out = _decide("git reset --hard", B, world["repo"])
    assert _kind(out) == "marker" and "OSError" in out["hookSpecificOutput"]["additionalContext"]


def test_classifier_exception_fails_open_with_the_visible_marker(world, monkeypatch):
    def boom(command, tool_name="Bash"):
        raise RuntimeError("bug")
    monkeypatch.setattr(hg, "_collect_signals", boom)
    code, out = _decide("echo x > docs/a.md", B, world["tree"])
    assert code == 0 and "permissionDecision" not in out["hookSpecificOutput"]
    assert out["hookSpecificOutput"]["additionalContext"] == hg.MSG_FAIL_OPEN_TEMPLATE.format(exc_type="RuntimeError")


@pytest.mark.parametrize("payload", [None, [], "x", {}, {"tool_name": "Bash"}, {"tool_name": "Bash", "tool_input": None},
                                     {"tool_name": "Bash", "tool_input": {"command": ""}},
                                     {"tool_name": "Bash", "tool_input": {"command": 5}},
                                     {"tool_name": "Edit", "tool_input": {"command": "cd x && ls"}},
                                     {"tool_name": "Bash", "tool_input": []}])
def test_unreadable_input_is_silent(payload):
    assert hg.decide(payload) == (0, None)


@pytest.mark.parametrize("name", ["MSG_CD_BASH", "MSG_CD_POWERSHELL", "MSG_MUTATION", "MSG_JOURNAL_BLOCK",
                                  "MSG_ROLLBACK", "MSG_WARN_PAYLOAD"])
def test_every_text_is_at_most_350_characters_and_names_a_door(name):
    text = getattr(hg, name)
    assert len(text) <= 350, (name, len(text))
    assert any(verb in text for verb in ("Use ", "Edit/Write", "Reading it", "undo", "use Edit/Write")), name


def test_removed_constants_and_detectors_are_gone():
    for gone in ("MSG_CD_PREFIX", "MSG_CD_NON_ROOT_WARN", "MSG_REDIRECT_STDERR", "MSG_PYTHON_DASH_C",
                 "MSG_PYTHON_DASH_C_OPAQUE", "MSG_PYTHON_DASH_C_BLOCK", "PYC_DENY_ENABLED", "_is_journal_bypass",
                 "_has_write_form", "PRINTF_ECHO_RE", "TEE_RE", "SED_INPLACE_RE", "OPEN_WRITE_MODE_RE",
                 "_PS_WRITE_CMDLET_RE", "_collect_redirect_signal"):
        assert not hasattr(hg, gone), gone


def test_collect_signals_is_pure_and_returns_forms_only(monkeypatch):
    def forbid(*a, **k):
        raise AssertionError("I/O in the pure signal walk")
    for owner, name in ((subprocess, "run"), (subprocess, "Popen"), (gitcmd, "git"), (os.path, "lexists"),
                        (os.path, "exists"), (os.path, "isdir"), (os, "stat"), (os, "getcwd"), (os, "listdir"),
                        (time, "time"), (time, "monotonic")):
        monkeypatch.setattr(owner, name, forbid)
    sig = hg._collect_signals("git checkout -- f.py; echo x > docs/a.md; cd x")
    assert set(sig) == {"cd", "write_targets", "journal", "rollback_forms", "pyc_payload", "payload_uncertain"}
    assert sig["rollback_forms"][0]["shape"] == "checkout -- paths" and sig["write_targets"] == [("redirect", "docs/a.md")]
    assert sig["cd"][0]["verb"] == "cd" and sig["cd"][0]["bare_return"] is False
    hg._collect_signals("( cd sub && ( cd $d && git reset --hard ) ); (( n > 5 )) && echo x > docs/a.md", "PowerShell")


@pytest.mark.parametrize("name,command,targets,uncertain", [
    ("literal-cd-composes", "( cd sub && echo x > f.txt )", [("redirect", "sub/f.txt")], False),
    ("cd-chain", "( cd a && cd b && echo x > f.txt )", [("redirect", "a/b/f.txt")], False),
    ("absolute-target-ignores-cd", "( cd sub && echo x > /abs/f.txt )", [("redirect", "/abs/f.txt")], False),
    ("nonliteral-cd-drops-relative", "( cd $d && echo x > f.txt )", [], False),
    ("nonliteral-cd-keeps-absolute", "( cd $d && echo x > /abs/f.txt )", [("redirect", "/abs/f.txt")], False),
    ("nonliteral-cd-payload-warns", "( cd $d && python -c \"open('f.txt','w')\" )", [], True),
    ("group-closed-restores", "( cd sub ); echo x > f.txt", [("redirect", "f.txt")], False),
    ("inner-group-does-not-leak-into-outer", "( cd a && ( cd b ); echo x > f.txt )", [("redirect", "a/f.txt")], False),
    ("sibling-groups-do-not-share", "( cd a ); ( echo x > f.txt )", [("redirect", "f.txt")], False),
])
def test_cd_scope_per_group(name, command, targets, uncertain):
    sig = hg._collect_signals(command)
    assert sig["write_targets"] == targets and sig["payload_uncertain"] is uncertain


def test_collect_signals_is_split_into_helpers_none_over_60_lines():
    import ast
    tree = ast.parse(Path(hg.__file__).read_text(encoding="utf-8"))
    walker = next((n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "_Walker"), None)
    assert walker is not None
    funcs = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "_collect_signals"]
    funcs += [n for n in walker.body if isinstance(n, ast.FunctionDef)]
    assert len(funcs) >= 10
    assert all(f.end_lineno - f.lineno + 1 <= 60 for f in funcs), [(f.name, f.end_lineno - f.lineno + 1) for f in funcs]


@pytest.mark.parametrize("shell,unit", [("Bash", '"\\'), ("PowerShell", '"`'), ("Bash", "'\""), ("Bash", "\"\\'")])
def test_quote_mask_is_linear_on_64kb_of_escape_pairs(world, shell, unit):
    command = unit * 32768
    t0 = time.perf_counter()
    code, out = hg.decide({"tool_name": shell, "tool_input": {"command": command}, "cwd": str(world["tree"])})
    assert time.perf_counter() - t0 < 1.0 and code == 0 and out is None
    t0 = time.perf_counter()
    hg._classify_pyc_payload("python -c " + command)
    assert time.perf_counter() - t0 < 1.0


def test_formatted_texts_stay_within_350_characters():
    long_path = "d/" * 100 + "file.md"
    assert len(hg.MSG_MUTATION.format(target=hg._clip(long_path))) <= 350
    assert len(hg.MSG_ROLLBACK.format(n=99999, dir=hg._clip("C:\\" + long_path))) <= 350
    assert len(hg._clip(long_path)) == hg.SHOWN_TARGET_CHARS and hg._clip(long_path).endswith("file.md")


def test_long_target_refusal_stays_within_350_characters(world):
    _code, out = _decide("echo x > docs/" + "n" * 200 + "/a.md", B, world["tree"])
    assert all(len(v) <= 350 for v in (out["hookSpecificOutput"]["permissionDecisionReason"],))


def test_chained_rollback_names_the_first_dirty_target(world):
    _code, out = _decide("git -C {} reset --hard && git -C {} reset --hard".format(
        world["clean"].as_posix(), world["repo"].as_posix()), B, world["clean"])
    reason = out["hookSpecificOutput"]["permissionDecisionReason"]
    assert os.sep + "repo" in reason and os.sep + "clean" not in reason


def test_python_dash_c_head_follows_the_payload_interpreter_row():
    assert hg._classify_pyc_payload("python3.12 -c \"open('a','w')\"") == "M"
    assert hg._classify_pyc_payload("python3 -c \"print(1)\"") == "P"


@pytest.mark.parametrize("name", ["bash", "sh", "zsh", "dash", "ksh", "cmd", "node", "perl", "ruby", "pwsh", "powershell"])
def test_every_payload_interpreter_without_a_classifier_is_a_named_row(name):
    row = next((r for r in hg.PAYLOAD_INTERPRETERS if r["name"].match(name)), None)
    assert row is not None and row["payload_classifier"] is None and row["payload_flags"], name


def test_capability_rows_carry_the_quote_and_region_rules():
    assert hg.SHELL_CAPABILITIES["Bash"]["dq_escape"] == "\\" and hg.SHELL_CAPABILITIES["Bash"]["arith_regions"]
    assert hg.SHELL_CAPABILITIES["PowerShell"]["dq_escape"] == "`" and not hg.SHELL_CAPABILITIES["PowerShell"]["arith_regions"]


# --- process level: the reader of stdin ---------------------------------------------------------------------
def _run_hook(raw: bytes, cwd):
    return subprocess.run([sys.executable, str(SCRIPT)], input=raw, capture_output=True, cwd=str(cwd), timeout=60)


def _wire(command, cwd):
    return json.dumps({"tool_name": "Bash", "tool_input": {"command": command}, "cwd": str(cwd)})


@pytest.mark.parametrize("name,raw,denied", [
    ("plain", None, True),
    ("utf8-bom", b"\xef\xbb\xbf", True),
    ("empty", b"", False),
    ("broken-json", b"{not json", False),
    ("binary-garbage", b"\xff\xfe\x00 not json", False),
    ("json-null", b"null", False),
])
def test_process_reader(world, name, raw, denied):
    body = _wire("echo x > docs/a.md", world["tree"]).encode("utf-8")
    data = body if raw is None else (raw + body if raw.startswith(b"\xef") else raw)
    done = _run_hook(data, world["tree"])
    assert done.returncode == 0 and done.stderr == b""
    assert (b'"permissionDecision": "deny"' in done.stdout) is denied
    if not denied:
        assert done.stdout == b""


def test_perf_100kb_1mb_is_roughly_linear(world):
    def best(size, repeats):
        cmd = "echo " + "x" * size + " > docs/a.md; python -c \"print('" + "a" * size + "')\""
        runs = []
        for _ in range(repeats):
            t0 = time.perf_counter()
            hg.decide({"tool_name": "Bash", "tool_input": {"command": cmd}, "cwd": str(world["tree"])})
            runs.append(time.perf_counter() - t0)
        return min(runs)
    small, big = best(100_000, 3), best(1_000_000, 2)
    print(f"hygiene_gate decide: 100KB {small:.4f}s, 1MB {big:.4f}s, ratio {big / max(small, 1e-6):.1f}")
    assert big / max(small, 1e-6) < 40 and big < 30.0

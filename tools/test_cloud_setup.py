"""Tests for the cloud setup script (GM1-8): the staged draft until the move, tools/cloud_setup.sh after it.

The tests pin STEPS (what the script does to a clone and to HOME), never comments or line numbers: node GM1-5 edits
the comment lines of the same script later. HOME is always a temporary directory; the real one is never touched.

A green Windows run does not prove Linux: the bash-running tests here are proved on the batch pipeline (Ubuntu).

Run from the repo root: python -m pytest tools/test_cloud_setup.py -q
"""

import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
LIVE = ROOT / "tools" / "cloud_setup.sh"
DRAFT = ROOT / "docs" / "migration" / "forge-repo" / "cloud-setup.sh"
PATH_LINE = 'export PATH="$HOME/.local/bin:$PATH"'


def script_path() -> Path:
    """tools/cloud_setup.sh when it exists (after the move), otherwise the staged draft; neither: red."""
    for p in (LIVE, DRAFT):
        if p.is_file():
            return p
    pytest.fail("neither tools/cloud_setup.sh nor docs/migration/forge-repo/cloud-setup.sh exists")


def _bash():
    """A bash that can run the script; the WSL launcher is not one (it cannot see Windows paths)."""
    exe = shutil.which("bash")
    if not exe:
        return None
    try:
        r = subprocess.run([exe, "-c", "command -v git >/dev/null && echo ok"], capture_output=True, text=True,
                           timeout=60)
    except (OSError, subprocess.SubprocessError):
        return None
    return exe if r.returncode == 0 and r.stdout.strip() == "ok" else None


BASH = _bash()
needs_bash = pytest.mark.skipif(BASH is None, reason="no usable bash on PATH (Git for Windows bash or Linux bash)")


def test_script_exists_in_one_of_its_two_homes():
    assert script_path().is_file()


def test_script_has_no_carriage_return():
    assert b"\r" not in script_path().read_bytes()


@needs_bash
def test_script_passes_bash_syntax_check():
    r = subprocess.run([BASH, "-n", script_path().as_posix()], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr


def _wrapper(path: Path, target: str):
    path.write_text('#!/bin/sh\nexec "%s" "$@"\n' % Path(target).as_posix(), encoding="utf-8", newline="\n")
    path.chmod(path.stat().st_mode | stat.S_IEXEC)


class Clone:
    """A temporary git clone holding the script, a fake `python3` whose pip does nothing, and a PATH that has no
    `python` (so the script's step 2 branch runs)."""

    def __init__(self, tmp: Path, with_example: bool = True, shallow: str = ""):
        """shallow: "" a plain init; "ok" a depth-1 clone whose origin can be fetched; "broken" one whose origin is gone."""
        self.home = tmp / "home"
        self.home.mkdir()
        self.root = tmp / "clone"
        env = {**os.environ, "HOME": str(self.home)}
        g = ["git", "-c", "user.name=t", "-c", "user.email=t@t"]
        if shallow:
            src = tmp / "origin"
            subprocess.run(["git", "init", "-q", str(src)], check=True, capture_output=True, env=env)
            for i in (1, 2):
                subprocess.run(g + ["-C", str(src), "commit", "-q", "--allow-empty", "-m", "c%d" % i], check=True,
                               capture_output=True, env=env)
            subprocess.run(["git", "clone", "-q", "--depth", "1", src.as_uri(), str(self.root)], check=True,
                           capture_output=True, env=env)
            if shallow == "broken":
                subprocess.run(["git", "-C", str(self.root), "remote", "set-url", "origin", str(tmp / "gone")],
                               check=True, capture_output=True, env=env)
        else:
            subprocess.run(["git", "init", "-q", str(self.root)], check=True, capture_output=True, env=env)
        (self.root / "tools").mkdir(exist_ok=True)
        self.script = self.root / "setup.sh"
        self.script.write_bytes(script_path().read_bytes())
        if with_example:
            (self.root / "tools" / "dev.config.example.yaml").write_text("developer: dev1\n", encoding="utf-8")
        fake = tmp / "fakebin"
        fake.mkdir()
        py3 = fake / "python3"
        # pip does nothing; dev_config.py (the one reader of the dev config) runs on the real interpreter
        py3.write_text('#!/bin/sh\nif [ "$1" = "-m" ] && [ "$2" = "pip" ]; then exit 0; fi\n'
                       'case "$*" in *dev_config.py*) exec "%s" "$@";; esac\n'
                       'echo "Python 3.12.0 (fake)"\n' % Path(sys.executable).as_posix(), encoding="utf-8", newline="\n")
        shutil.copy(ROOT / "tools" / "dev_config.py", self.root / "tools" / "dev_config.py")
        py3.chmod(py3.stat().st_mode | stat.S_IEXEC)
        for tool in ("git", "ln", "mkdir", "cp", "grep", "dirname"):
            found = shutil.which(tool)
            if not found:
                pytest.skip("tool %s not found for the sandbox PATH" % tool)
            _wrapper(fake / tool, found)
        self.fake = fake

    def run(self, **extra):
        env = {"HOME": str(self.home), "PATH": self.fake.as_posix(), "SYSTEMROOT": os.environ.get("SYSTEMROOT", ""),
               **extra}
        return subprocess.run([BASH, self.script.as_posix()], cwd=self.root, env=env, capture_output=True,
                              text=True)

    def state(self):
        """Everything the script may touch, as bytes: git config, bashrc, the dev config, the tools folder list."""
        def b(p: Path):
            return p.read_bytes() if p.is_file() else None
        return (b(self.root / ".git" / "config"), b(self.home / ".bashrc"), b(self.root / "tools" / "dev.config.yaml"),
                sorted(str(p.relative_to(self.root)) for p in (self.root / "tools").rglob("*")))


@needs_bash
def test_setup_sets_hooks_path_and_copies_the_example(tmp_path):
    c = Clone(tmp_path)
    r = c.run()
    assert r.returncode == 0, r.stdout + r.stderr
    cfg = (c.root / ".git" / "config").read_text(encoding="utf-8")
    assert "hooksPath = .githooks" in cfg
    assert (c.root / "tools" / "dev.config.yaml").read_text(encoding="utf-8") == "developer: dev1\n"
    assert "cloud setup done" in r.stdout


@needs_bash
def test_setup_never_overwrites_a_personal_dev_config(tmp_path):
    c = Clone(tmp_path)
    mine = c.root / "tools" / "dev.config.yaml"
    mine.write_text("developer: me\n", encoding="utf-8")
    assert c.run().returncode == 0
    assert mine.read_text(encoding="utf-8") == "developer: me\n"


@needs_bash
def test_setup_without_the_example_creates_no_config_and_still_exits_zero(tmp_path):
    c = Clone(tmp_path, with_example=False)
    assert c.run().returncode == 0
    assert not (c.root / "tools" / "dev.config.yaml").exists()


SECRET = "s3cr3t-value"


@needs_bash
@pytest.mark.parametrize("config,env,expect", [
    # the reader's semantics: no file -> the default name; a file without the key or with a bad name -> a refusal note
    (None, {"GITHUB_TOKEN": SECRET}, "environment variable GITHUB_TOKEN: SET"),
    ("github_token_env: MY_TOK\n", {"GITHUB_TOKEN": SECRET}, "environment variable MY_TOK: NOT SET"),
    ("developer: dev1\n",{"GITHUB_TOKEN": SECRET}, "note: environment variable: none to check"),
    ("github_token_env: my_tok\n", {"GITHUB_TOKEN": SECRET}, "note: dev_config.py refused"),
])
def test_token_step_prints_the_reader_answer_and_never_the_value(tmp_path, config, env, expect):
    c = Clone(tmp_path, with_example=config is not None)
    if config is not None:
        (c.root / "tools" / "dev.config.yaml").write_text(config, encoding="utf-8")
    r = c.run(**env)
    assert r.returncode == 0, r.stdout + r.stderr
    assert len([ln for ln in r.stdout.splitlines() if ln.startswith(expect)]) == 1
    assert SECRET not in r.stdout + r.stderr


@needs_bash
@pytest.mark.parametrize("shallow,fetched,note", [("ok", True, False), ("broken", False, True)])
def test_shallow_clone_is_unshallowed_and_a_failure_is_one_note(tmp_path, shallow, fetched, note):
    c = Clone(tmp_path, shallow=shallow)

    def is_shallow():
        return subprocess.run(["git", "-C", str(c.root), "rev-parse", "--is-shallow-repository"],
                              capture_output=True, text=True).stdout.strip()
    before = is_shallow()
    r = c.run()
    assert r.returncode == 0, r.stdout + r.stderr
    assert (before, is_shallow()) == (("true", "false") if fetched else ("true", "true"))
    assert len([ln for ln in r.stdout.splitlines() if "unshallow" in ln]) == (1 if note else 0)


@needs_bash
@pytest.mark.parametrize("tz,noted", [(None, True), ("", True), ("Europe/Paris", False)])
def test_tz_note_only_when_tz_is_unset_or_empty(tmp_path, tz, noted):
    r = Clone(tmp_path).run(**({} if tz is None else {"TZ": tz}))
    assert r.returncode == 0
    assert len([ln for ln in r.stdout.splitlines() if ln.startswith("note: TZ") and "naive local" in ln]) == int(noted)


@needs_bash
def test_bashrc_gets_the_path_line_once_and_a_second_run_changes_nothing(tmp_path):
    c = Clone(tmp_path)
    assert c.run().returncode == 0
    first = c.state()
    assert (c.home / ".bashrc").read_text(encoding="utf-8").splitlines().count(PATH_LINE) == 1
    r = c.run()
    assert r.returncode == 0, r.stdout + r.stderr
    assert c.state() == first


@needs_bash
def test_the_real_home_is_not_touched(tmp_path):
    real = Path(os.path.expanduser("~")) / ".bashrc"
    before = real.read_bytes() if real.is_file() else None
    Clone(tmp_path).run()
    assert (real.read_bytes() if real.is_file() else None) == before


def test_gitattributes_pins_lf_for_shell_and_workflow_files():
    text = (ROOT / ".gitattributes").read_text(encoding="utf-8")
    for line in ("*.sh text eol=lf", "docs/migration/**/*.yml text eol=lf", ".github/**/*.yml text eol=lf"):
        assert line in text.splitlines()


def test_gitignore_has_the_bundle_pattern():
    assert "*.bundle" in (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()

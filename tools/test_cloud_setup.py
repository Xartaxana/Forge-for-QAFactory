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
    `python` and no `gh` (so the script's step 2 and step 5 branches both run)."""

    def __init__(self, tmp: Path, with_example: bool = True):
        self.home = tmp / "home"
        self.home.mkdir()
        self.root = tmp / "clone"
        (self.root / "tools").mkdir(parents=True)
        self.script = self.root / "setup.sh"
        self.script.write_bytes(script_path().read_bytes())
        if with_example:
            (self.root / "tools" / "dev.config.example.yaml").write_text("developer: dev1\n", encoding="utf-8")
        env = {**os.environ, "HOME": str(self.home)}
        subprocess.run(["git", "init", "-q", str(self.root)], check=True, capture_output=True, env=env)
        fake = tmp / "fakebin"
        fake.mkdir()
        py3 = fake / "python3"
        py3.write_text('#!/bin/sh\nif [ "$1" = "-m" ] && [ "$2" = "pip" ]; then exit 0; fi\n'
                       'echo "Python 3.12.0 (fake)"\n', encoding="utf-8", newline="\n")
        py3.chmod(py3.stat().st_mode | stat.S_IEXEC)
        for tool in ("git", "ln", "mkdir", "cp", "grep", "dirname"):
            found = shutil.which(tool)
            if not found:
                pytest.skip("tool %s not found for the sandbox PATH" % tool)
            _wrapper(fake / tool, found)
        self.fake = fake

    def run(self):
        env = {"HOME": str(self.home), "PATH": self.fake.as_posix(), "SYSTEMROOT": os.environ.get("SYSTEMROOT", "")}
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


@needs_bash
def test_setup_without_gh_says_one_line_and_exits_zero(tmp_path):
    c = Clone(tmp_path)
    r = c.run()
    assert r.returncode == 0
    assert len([ln for ln in r.stdout.splitlines() if "gh CLI missing" in ln]) == 1


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

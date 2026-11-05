"""Tests for tools/factory_rules_index.py — the generated index of the factory building rules."""
import pathlib
import re
import subprocess
import sys

import pytest

TOOLS = pathlib.Path(__file__).resolve().parent
SCRIPT = TOOLS / "factory_rules_index.py"
REAL_SOURCE = TOOLS.parent / "ai-packages" / "qa-factory" / "design" / "factory-rules.md"

GOOD = """# Rules

| Section | Rules |
|---|---|
| A. First | FR-1, FR-3 |
| B. Second | FR-2 |

## A. First

**FR-1 — A refusal says what is wrong.** Body of the rule
over two lines.

**FR-3 — The package is English**, including fixtures; the rest is outside the bold.

## B. Second

**FR-2 — A story's spend is the names
across two lines**
*Why:* something.
"""


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                          capture_output=True, text=True, encoding="utf-8")


def make_source(tmp_path, text=GOOD):
    src = tmp_path / "rules.md"
    src.write_bytes(text.encode("utf-8"))
    return src


def test_small_source_titles_and_layout(tmp_path):
    src, out = make_source(tmp_path), tmp_path / "index.md"
    r = run("--source", src, "--out", out)
    assert r.returncode == 0, r.stderr
    assert "3 rules, 2 sections" in r.stdout
    data = out.read_bytes()
    assert b"\r" not in data and data.endswith(b"\n") and not data.endswith(b"\n\n")
    text = data.decode("utf-8")
    assert "- FR-1 — A refusal says what is wrong\n" in text          # trailing period stripped
    assert "- FR-3 — The package is English\n" in text                 # nothing from outside the bold
    assert "- FR-2 — A story's spend is the names across two lines\n" in text  # multi-line bold
    assert text.index("FR-1") < text.index("FR-3") < text.index("## B. Second")  # file order kept


def source_counts():
    """(rules, sections) counted from the real source by the test's own regexes -- the pin
    follows the source (FR-58, FR-59 were added after this test was written), never a literal."""
    src = REAL_SOURCE.read_text(encoding="utf-8")
    rules = len(re.findall(r"^\*\*FR-\d+ — ", src, re.MULTILINE))
    sections = len(re.findall(r"^## [A-Z]\. ", src, re.MULTILINE))
    assert rules > 0 and sections > 0   # the counting itself must find something
    return rules, sections


def test_real_source(tmp_path):
    n_rules, n_sections = source_counts()
    out = tmp_path / "index.md"
    r = run("--source", REAL_SOURCE, "--out", out)
    assert r.returncode == 0, r.stderr
    assert f"{n_rules} rules, {n_sections} sections" in r.stdout
    text = out.read_text(encoding="utf-8")
    assert "- FR-30 — The package is English\n" in text
    assert "- FR-24 — A story's spend is the sessions its own journal names\n" in text
    assert text.count("\n- FR-") == n_rules and text.count("\n## ") == n_sections


def test_generate_then_check_ok(tmp_path):
    n_rules, _ = source_counts()
    out = tmp_path / "index.md"
    assert run("--source", REAL_SOURCE, "--out", out).returncode == 0
    r = run("--check", "--source", REAL_SOURCE, "--out", out)
    assert r.returncode == 0
    assert r.stdout.strip() == f"factory rules index: up to date ({n_rules} rules)"


def test_check_stale_after_altered_title(tmp_path):
    out = tmp_path / "index.md"
    run("--source", REAL_SOURCE, "--out", out)
    out.write_text(out.read_text(encoding="utf-8").replace("The package is English",
                                                            "The package is Russian"),
                   encoding="utf-8", newline="")
    r = run("--check", "--source", REAL_SOURCE, "--out", out)
    assert r.returncode == 1
    assert "factory rules index is stale: run python tools/factory_rules_index.py" in r.stdout


def test_check_missing_out(tmp_path):
    r = run("--check", "--source", REAL_SOURCE, "--out", tmp_path / "nope.md")
    assert r.returncode == 1
    assert "factory rules index is missing: run python tools/factory_rules_index.py" in r.stdout


def test_check_writes_nothing(tmp_path):
    out = tmp_path / "index.md"
    run("--source", REAL_SOURCE, "--out", out)
    out.write_bytes(out.read_bytes() + b"tampered\n")
    before, mtime = out.read_bytes(), out.stat().st_mtime_ns
    assert run("--check", "--source", REAL_SOURCE, "--out", out).returncode == 1
    assert out.read_bytes() == before and out.stat().st_mtime_ns == mtime
    missing = tmp_path / "absent.md"
    run("--check", "--source", REAL_SOURCE, "--out", missing)
    assert not missing.exists()


def test_duplicate_id(tmp_path):
    src = make_source(tmp_path, GOOD.replace("FR-2 — A story", "FR-1 — A story"))
    out = tmp_path / "index.md"
    r = run("--source", src, "--out", out)
    assert r.returncode == 2 and "duplicate rule id FR-1" in r.stderr
    assert not out.exists()


def test_summary_table_mismatch(tmp_path):
    src = make_source(tmp_path, GOOD.replace("| A. First | FR-1, FR-3 |", "| A. First | FR-1, FR-9 |"))
    out = tmp_path / "index.md"
    r = run("--source", src, "--out", out)
    assert r.returncode == 2
    assert "FR-9" in r.stderr and "FR-3" in r.stderr and "A. First" in r.stderr
    assert not out.exists()


def test_rule_before_any_section(tmp_path):
    text = GOOD.replace("## A. First", "**FR-7 — Early rule.** text\n\n## A. First", 1)
    r = run("--source", make_source(tmp_path, text), "--out", tmp_path / "index.md")
    assert r.returncode == 2 and "before the first" in r.stderr


def test_missing_source(tmp_path):
    out = tmp_path / "index.md"
    r = run("--source", tmp_path / "gone.md", "--out", out)
    assert r.returncode == 2 and "cannot read the source" in r.stderr
    assert not out.exists()


def test_zero_rules(tmp_path):
    r = run("--source", make_source(tmp_path, "# nothing\n\n## A. Empty\n"),
            "--out", tmp_path / "index.md")
    assert r.returncode == 2 and "no rules found" in r.stderr


def test_committed_index_is_current():
    """The index committed in docs/ matches the real source (the same check the hook runs)."""
    r = run("--check")
    assert r.returncode == 0, r.stdout + r.stderr


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))

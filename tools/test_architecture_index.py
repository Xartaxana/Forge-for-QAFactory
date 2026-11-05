"""Tests for tools/architecture_index.py -- the generated index of the factory's AR-n invariants."""
import importlib.util
import pathlib
import re
import shutil
import subprocess
import sys

import pytest

TOOLS = pathlib.Path(__file__).resolve().parent
SCRIPT = TOOLS / "architecture_index.py"
REAL_SOURCE = TOOLS.parent / "ai-packages" / "qa-factory" / "design" / "architecture.md"

_spec = importlib.util.spec_from_file_location("architecture_index_under_test", SCRIPT)
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)

GOOD = """# Architecture

| Section | Invariants |
|---|---|
| A. First | AR-1, AR-3 |
| B. Second | AR-2 |
| C. Third | AR-4 |
| D. Fourth | AR-5 |

## A. First

**AR-1 — A refusal says what is wrong.**
- Invariant: body of the invariant.

**AR-3 — The package is English**, including fixtures; the rest is outside the bold.

## B. Second

**AR-2 — A story's spend is the names.**
- Invariant: AR-9 is only mentioned here, not an opener.

## C. Third

**AR-4 — Third title.**

## D. Fourth

**AR-5 — Fourth title.**

## How a change walks this map

**AR-6 — Never indexed, after the first unlettered heading.**
"""


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                          capture_output=True, text=True, encoding="utf-8")


def make_source(tmp_path, text=GOOD):
    src = tmp_path / "architecture.md"
    src.write_bytes(text.encode("utf-8"))
    return src


def test_small_source_titles_and_layout(tmp_path):
    src, out = make_source(tmp_path), tmp_path / "index.md"
    r = run("--source", src, "--out", out)
    assert r.returncode == 0, r.stderr
    assert "5 invariants, 4 sections" in r.stdout
    data = out.read_bytes()
    assert b"\r" not in data and data.endswith(b"\n") and not data.endswith(b"\n\n")
    text = data.decode("utf-8")
    assert "- AR-1 — A refusal says what is wrong\n" in text            # trailing period stripped
    assert "- AR-3 — The package is English\n" in text                   # nothing from outside the bold
    assert text.index("AR-1") < text.index("AR-3") < text.index("## B. Second")   # file order kept
    assert "AR-6" not in text                                            # the protocol section is not indexed


def source_counts():
    """(invariants, sections) counted from the real source by the test's own regexes -- the pin
    follows the source, never a literal."""
    src = REAL_SOURCE.read_text(encoding="utf-8")
    body = src.split("\n## How a change walks this map")[0]
    invariants = len(re.findall(r"^\*\*AR-\d+ — ", body, re.MULTILINE))
    sections = len(re.findall(r"^## [A-Z]\. ", body, re.MULTILINE))
    assert invariants > 0 and sections == 4
    return invariants, sections


def test_real_source(tmp_path):
    n, sections = source_counts()
    out = tmp_path / "index.md"
    r = run("--source", REAL_SOURCE, "--out", out)
    assert r.returncode == 0, r.stderr
    assert f"{n} invariants, {sections} sections" in r.stdout
    text = out.read_text(encoding="utf-8")
    assert text.count("\n- AR-") == n and text.count("\n## ") == sections
    assert "- AR-22 — Every field read has a producer; every field produced has a reader\n" in text
    assert len(text.encode("utf-8")) <= mod.MAX_BYTES


def test_generate_then_check_ok(tmp_path):
    n, _ = source_counts()
    out = tmp_path / "index.md"
    assert run("--source", REAL_SOURCE, "--out", out).returncode == 0
    r = run("--check", "--source", REAL_SOURCE, "--out", out)
    assert r.returncode == 0
    assert r.stdout.startswith(f"architecture index: up to date ({n} invariants")


def test_check_stale_after_one_byte_edit_restored_by_byte_copy(tmp_path):
    out, keep = tmp_path / "index.md", tmp_path / "index.keep"
    run("--source", REAL_SOURCE, "--out", out)
    shutil.copyfile(out, keep)                                   # the byte copy taken BEFORE the edit
    data = bytearray(out.read_bytes())
    data[-3] ^= 0x01                                             # one byte
    out.write_bytes(bytes(data))
    r = run("--check", "--source", REAL_SOURCE, "--out", out)
    assert r.returncode == 1
    assert "architecture index is stale: run python tools/architecture_index.py" in r.stdout
    shutil.copyfile(keep, out)
    assert out.read_bytes() == keep.read_bytes()
    assert run("--check", "--source", REAL_SOURCE, "--out", out).returncode == 0


def test_check_missing_out(tmp_path):
    r = run("--check", "--source", REAL_SOURCE, "--out", tmp_path / "nope.md")
    assert r.returncode == 1
    assert "architecture index is missing: run python tools/architecture_index.py" in r.stdout


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
    src = make_source(tmp_path, GOOD.replace("AR-2 — A story", "AR-1 — A story"))
    out = tmp_path / "index.md"
    r = run("--source", src, "--out", out)
    assert r.returncode == 2 and "duplicate invariant id AR-1" in r.stderr
    assert not out.exists()


def test_id_missing_from_summary_table(tmp_path):
    src = make_source(tmp_path, GOOD.replace("| A. First | AR-1, AR-3 |", "| A. First | AR-1 |"))
    r = run("--source", src, "--out", tmp_path / "index.md")
    assert r.returncode == 2
    assert "AR-3" in r.stderr and "A. First" in r.stderr and "missing from the summary table" in r.stderr


def test_id_listed_but_not_found(tmp_path):
    src = make_source(tmp_path, GOOD.replace("| A. First | AR-1, AR-3 |", "| A. First | AR-1, AR-3, AR-9 |"))
    r = run("--source", src, "--out", tmp_path / "index.md")
    assert r.returncode == 2 and "AR-9" in r.stderr and "not found under the heading" in r.stderr


@pytest.mark.parametrize("opener", ["**AR-3 — **", "**AR-3 —** x", "**AR-3**", "**AR-3 — never closed"])
def test_opener_without_a_title(tmp_path, opener):
    src = make_source(tmp_path, GOOD.replace("**AR-3 — The package is English**", opener, 1))
    out = tmp_path / "index.md"
    r = run("--source", src, "--out", out)
    assert r.returncode == 2 and "AR-3" in r.stderr and "opener" in r.stderr
    assert not out.exists()


def test_missing_section_d(tmp_path):
    text = GOOD.replace("## D. Fourth", "## How else").replace("| D. Fourth | AR-5 |\n", "")
    r = run("--source", make_source(tmp_path, text), "--out", tmp_path / "index.md")
    assert r.returncode == 2 and "## D." in r.stderr and "missing section" in r.stderr


def test_opener_before_any_section(tmp_path):
    text = GOOD.replace("## A. First", "**AR-7 — Early.** text\n\n## A. First", 1)
    r = run("--source", make_source(tmp_path, text), "--out", tmp_path / "index.md")
    assert r.returncode == 2 and "before the first" in r.stderr


def test_missing_source(tmp_path):
    out = tmp_path / "index.md"
    r = run("--source", tmp_path / "gone.md", "--out", out)
    assert r.returncode == 2 and "cannot read the source" in r.stderr
    assert not out.exists()


def test_zero_invariants(tmp_path):
    text = "\n".join("## %s. S%s" % (c, c) for c in "ABCD") + "\n"
    r = run("--source", make_source(tmp_path, text), "--out", tmp_path / "index.md")
    assert r.returncode == 2 and "no invariants found" in r.stderr


def source_with_openers(count, last_title_padding=0):
    """A valid source: four sections, `count` openers, the last title padded by that many characters."""
    per = [list(range(1, count + 1))[i::4] for i in range(4)]
    rows = "\n".join("| %s. S%s | %s |" % (c, c, ", ".join("AR-%d" % n for n in ids))
                     for c, ids in zip("ABCD", per))
    body = []
    for c, ids in zip("ABCD", per):
        body.append("## %s. S%s\n" % (c, c))
        for n in ids:
            pad = "x" * last_title_padding if n == count else ""
            body.append("**AR-%d — A title of a realistic length, number %d%s.**\n" % (n, n, pad))
    return "# T\n\n| Section | Invariants |\n|---|---|\n" + rows + "\n\n" + "\n".join(body)


def test_cap_30_openers_with_long_titles_is_exit_2(tmp_path):
    r = run("--source", make_source(tmp_path, source_with_openers(30, 1200)), "--out", tmp_path / "index.md")
    assert r.returncode == 2 and "over the 3072-byte cap" in r.stderr
    assert not (tmp_path / "index.md").exists()


def test_entry_limit_30_passes_and_31_is_exit_2(tmp_path):
    out = tmp_path / "index.md"
    r = run("--source", make_source(tmp_path, source_with_openers(mod.MAX_INVARIANTS)), "--out", out)
    assert mod.MAX_INVARIANTS == 30 and r.returncode == 0, r.stderr
    assert "30 invariants" in r.stdout and out.is_file()
    out.unlink()
    r = run("--source", make_source(tmp_path, source_with_openers(mod.MAX_INVARIANTS + 1)), "--out", out)
    assert r.returncode == 2 and "31 invariants" in r.stderr and "30-entry limit" in r.stderr
    assert "step 10" in r.stderr and not out.exists()


def test_entry_limit_60_openers_names_the_limit_first(tmp_path):
    r = run("--source", make_source(tmp_path, source_with_openers(60)), "--out", tmp_path / "index.md")
    assert r.returncode == 2 and "30-entry limit" in r.stderr


def test_ar_0_is_refused(tmp_path):
    r = run("--source", make_source(tmp_path, GOOD.replace("AR-5 — Fourth", "AR-0 — Fourth")),
            "--out", tmp_path / "index.md")
    assert r.returncode == 2 and "AR-0" in r.stderr and "ids start at AR-1" in r.stderr


def test_cap_at_and_beyond_the_limit(tmp_path):
    base = len(mod.build(make_source(tmp_path, source_with_openers(20)))[0])
    assert base < mod.MAX_BYTES
    at = mod.build(make_source(tmp_path, source_with_openers(20, mod.MAX_BYTES - base)))[0]
    assert len(at) == mod.MAX_BYTES                                          # exactly 3072 B passes
    beyond = make_source(tmp_path, source_with_openers(20, mod.MAX_BYTES - base + 1))
    r = run("--source", beyond, "--out", tmp_path / "index.md")
    assert r.returncode == 2 and "3073 bytes" in r.stderr and "3072-byte cap" in r.stderr   # 3073 B fails
    ok = run("--source", make_source(tmp_path, source_with_openers(20, mod.MAX_BYTES - base)),
             "--out", tmp_path / "index.md")
    assert ok.returncode == 0 and (tmp_path / "index.md").stat().st_size == mod.MAX_BYTES


def test_committed_index_is_current():
    """The index committed in docs/ matches the real source (the same check the hook runs)."""
    r = run("--check")
    assert r.returncode == 0, r.stdout + r.stderr


def test_gitattributes_pins_the_index_to_lf():
    """The check is byte-for-byte: a CRLF checkout under core.autocrlf would read as stale forever."""
    lines = (TOOLS.parent / ".gitattributes").read_text(encoding="utf-8").splitlines()
    assert "docs/ARCHITECTURE_INDEX.md text eol=lf" in lines


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))

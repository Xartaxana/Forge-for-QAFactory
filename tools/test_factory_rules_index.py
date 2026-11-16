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


def test_fr_row_byte_identical_to_committed(tmp_path):
    """Row FR: a fresh build equals the committed docs/FACTORY_RULES_INDEX.md byte for byte."""
    out = tmp_path / "index.md"
    assert run("--row", "FR", "--source", REAL_SOURCE, "--out", out).returncode == 0
    assert out.read_bytes() == (TOOLS.parent / "docs" / "FACTORY_RULES_INDEX.md").read_bytes()


# ---- row P: the owner principles index, on fixture sources built in tmp_path ----

PRE = "- P{n} — "
PRE_BYTES = lambda n: len((PRE.format(n=n)).encode("utf-8"))   # noqa: E731


def sentence(total_chars, word="abc"):
    """An ASCII sentence of exactly total_chars chars: words, spaces, one final period."""
    return ((word + " ") * total_chars)[:total_chars - 1] + "."


def bullets(*items):
    """items: (n, text); the source of a principles file."""
    return "# Principles\n\n" + "".join("- **P%d.** %s\n" % (n, t) for n, t in items)


def run_p(tmp_path, source_text, *flags, crlf=False, write_out=False):
    src, out = tmp_path / "p.md", tmp_path / "p_index.md"
    data = source_text.replace("\n", "\r\n") if crlf else source_text
    src.write_bytes(data.encode("utf-8"))
    r = run("--row", "P", "--source", src, "--out", out, *flags)
    return r, out


LONG = "w" + "ord " * 80 + "end. Second sentence."          # first sentence far over 220 bytes
AT = sentence(220 - PRE_BYTES(1))                            # the line is exactly 220 bytes
BEYOND = sentence(220 - PRE_BYTES(1) + 1)                    # one byte beyond the cap

P_LINE_CASES = [
    # id: (source items, expected lines in the index, in order)
    ("first-sentence", [(1, "Code never decides. It reports.")], ["- P1 — Code never decides."]),
    ("gap-in-numbering", [(1, "A."), (3, "B! More"), (7, "C? x")],
     ["- P1 — A.", "- P3 — B!", "- P7 — C?"]),
    ("period-inside-backticks", [(2, "Use `a. b` always. Then more.")],
     ["- P2 — Use `a. b` always."]),
    ("no-sentence-end", [(4, "no end here at all")], ["- P4 — no end here at all"]),
    ("dot-not-followed-by-space", [(5, "version 1.5 stays. next")], ["- P5 — version 1.5 stays."]),
    ("cap-at-limit-passes", [(1, AT)], ["- P1 — " + AT]),
]


@pytest.mark.parametrize("items,expected", [c[1:] for c in P_LINE_CASES],
                         ids=[c[0] for c in P_LINE_CASES])
def test_p_row_lines(tmp_path, items, expected):
    r, out = run_p(tmp_path, bullets(*items))
    assert r.returncode == 0, r.stderr
    lines = out.read_text(encoding="utf-8").splitlines()
    assert lines[0].startswith("# Owner principles") and "do not edit by hand" in lines[2]
    assert lines[3] == "" and lines[4:] == expected


@pytest.mark.parametrize("text", [LONG, BEYOND, " ".join(["é" * 20] * 12) + ".", "é" * 300 + "."],
                         ids=["long-first-sentence", "cap-one-byte-beyond-is-cut",
                              "multibyte-with-spaces", "multibyte-no-whitespace"])
def test_p_row_cut(tmp_path, text):
    r, out = run_p(tmp_path, bullets((19, text)))
    assert r.returncode == 0, r.stderr
    line = out.read_bytes().decode("utf-8").splitlines()[-1]     # decodes: no cut inside a character
    assert len(line.encode("utf-8")) <= 220 and line.startswith("- P19 — ")
    assert line.endswith(" …") and not line.endswith("  …")
    if " " in text:       # cut at whitespace: the kept part is a whole-word prefix of the sentence
        kept = line[len("- P19 — "):-2]
        assert text.startswith(kept) and text[len(kept)] == " "


def test_p_row_crlf_equals_lf(tmp_path):
    items = [(1, "Alpha beta. More"), (2, "Multi line\n  bullet text. Tail")]
    lf, out_lf = run_p(tmp_path, bullets(*items))
    out_lf_bytes = out_lf.read_bytes()
    crlf, out_crlf = run_p(tmp_path, bullets(*items), crlf=True)
    assert lf.returncode == crlf.returncode == 0
    assert out_crlf.read_bytes() == out_lf_bytes and b"\r" not in out_lf_bytes
    assert b"- P2 \xe2\x80\x94 Multi line bullet text." in out_lf_bytes


P_REFUSALS = [
    ("duplicate-id", bullets((1, "A."), (2, "B."), (1, "C.")), ["duplicate id P1", "lines 3 and 5"]),
    ("empty-bullet", "# x\n\n- **P1.** A.\n- **P2.** \n", ["P2", "line 4", "empty bullet"]),
    ("no-bullets", "# nothing here\n", ["no entries found"]),
]


@pytest.mark.parametrize("text,needles", [c[1:] for c in P_REFUSALS], ids=[c[0] for c in P_REFUSALS])
def test_p_row_refusals(tmp_path, text, needles):
    r, out = run_p(tmp_path, text)
    assert r.returncode == 2 and not out.exists()
    for needle in needles:
        assert needle in r.stderr, r.stderr


def _file_sized(target):
    """A source whose index is exactly `target` bytes: filler bullets, the last one padded."""
    sys.path.insert(0, str(TOOLS))
    try:
        import factory_rules_index as mod
    finally:
        sys.path.pop(0)
    base = len((mod.P_HEADER + "\n").encode("utf-8"))
    items, total, n = [], base, 0
    while True:
        n += 1
        room = target - total                              # bytes left, newline of the line included
        chunk = room if room <= 220 else 201
        text = sentence(chunk - 1 - PRE_BYTES(n))          # ASCII: chars == bytes
        items.append((n, text))
        total += chunk
        if total == target:
            return bullets(*items)
        assert total < target and n < 100


def test_p_row_file_cap_at_and_beyond(tmp_path):
    ok, out = run_p(tmp_path, _file_sized(6144))
    assert ok.returncode == 0, ok.stderr
    assert out.stat().st_size == 6144
    (tmp_path / "b").mkdir()
    over, out2 = run_p(tmp_path / "b", _file_sized(6145))
    assert over.returncode == 2 and not out2.exists()
    assert "over the 6144-byte cap" in over.stderr and "three longest lines" in over.stderr
    assert "shorten the first sentence in the source, or raise the cap" in over.stderr
    assert over.stderr.count(" | ") == 2           # exactly three lines named


def test_p_row_check_ok_then_stale(tmp_path):
    src_text = bullets((1, "A."), (2, "B."))
    r, out = run_p(tmp_path, src_text)
    assert r.returncode == 0 and out.is_file()
    assert run_p(tmp_path, src_text, "--check")[0].returncode == 0
    out.write_bytes(out.read_bytes() + b"x\n")
    stale = run_p(tmp_path, src_text, "--check")[0]
    assert stale.returncode == 1 and "stale" in stale.stdout


def test_p_row_temporal_both_worlds(tmp_path):
    # world 1: neither the source nor the index exists -> skip, exit 0, nothing written
    src, out = tmp_path / "OWNER_PRINCIPLES.md", tmp_path / "OWNER_PRINCIPLES_INDEX.md"
    for flags in ((), ("--check",)):
        r = run("--row", "P", "--source", src, "--out", out, *flags)
        assert r.returncode == 0 and "skip:" in r.stdout and "OWNER_PRINCIPLES.md absent" in r.stdout
    assert not out.exists()
    # world 2: the index exists, the source is gone -> exit 2 naming both
    out.write_text("old\n", encoding="utf-8")
    r = run("--row", "P", "--source", src, "--out", out, "--check")
    assert r.returncode == 2
    assert "OWNER_PRINCIPLES_INDEX.md" in r.stderr and "OWNER_PRINCIPLES.md" in r.stderr


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))

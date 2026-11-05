"""The forge's licence files equal the package's, and the QAFactory marketplace draft names what the package reads (GM2-1).

Run from the repo root: python -m pytest tools/test_license_files.py -q
"""
import json
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
PKG = REPO / "ai-packages" / "qa-factory"
DRAFT = REPO / "docs" / "migration" / "qafactory-repo"
sys.path.insert(0, str(PKG / "scripts"))


def read(path):
    return path.read_bytes().decode("utf-8").replace("\r\n", "\n")


def test_root_license_equals_package_license():
    assert read(REPO / "LICENSE") == read(PKG / "LICENSE")


def _draft_or_skip():
    if not DRAFT.is_dir():
        pytest.skip("after the move the QAFactory files live in that repository")


def test_draft_license_equals_package_license():
    _draft_or_skip()
    path = DRAFT / "LICENSE"
    assert path.is_file(), f"missing {path}"
    assert read(path) == read(PKG / "LICENSE")


def test_draft_marketplace_names_the_package_reads():
    _draft_or_skip()
    import hooklib
    path = DRAFT / ".claude-plugin" / "marketplace.json"
    assert path.is_file(), f"missing {path}"
    data = json.loads(read(path))
    assert data["name"] == hooklib.VERSION_MARKETPLACE
    row = [p for p in data["plugins"] if p.get("name") == "qa-factory"]
    assert row and row[0].get("source") == "./qa-factory"

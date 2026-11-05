"""backlog_tree.py: the «Бэклог» pane's data is the piles tree as tools/piles.py reads it, closed work left out."""
import json
import subprocess
import sys
from pathlib import Path

import backlog_tree as BT

ROOT = Path(__file__).resolve().parent.parent


def test_tree_has_open_batches_only_and_counts_match():
    data = BT.tree(ROOT)
    assert data["piles"], "the repository has open piles"
    total = 0
    for pile in data["piles"]:
        assert pile["batches"], "a pile with no open batch is left out"
        for b in pile["batches"]:
            assert not b["status"].startswith("закрыта")
            for n in b["nodes"]:
                assert not n["status"].startswith(BT.DONE_NODE)
                assert n["id"]
            total += len(b["nodes"])
    assert sum(data["counts"].values()) == total


def test_order_piles_by_most_urgent_batch_and_batches_by_priority():
    data = BT.tree(ROOT)
    best = [min(BT._rank(b["prio"]) for b in p["batches"]) for p in data["piles"]]
    assert best == sorted(best), "a pile with a П1 batch stands above one whose best is П2, П3 last"
    for p in data["piles"]:
        ranks = [BT._rank(b["prio"]) for b in p["batches"]]
        assert ranks == sorted(ranks), f"{p['slug']}: batches П1 → П2 → П3"
    assert BT._rank("") == 4      # no priority: last


def test_prio_reads_the_header_word():
    assert BT._prio("П1") == "П1"
    assert BT._prio("приоритет П 3, срочно") == "П3"
    assert BT._prio("") == ""          # empty input: no priority, the pane draws it grey
    assert BT._prio(None) == ""


def test_cli_prints_json():
    out = subprocess.run([sys.executable, "-B", str(ROOT / "tools" / "backlog_tree.py")], capture_output=True, check=True)
    data = json.loads(out.stdout.decode("utf-8"))
    assert set(data) == {"piles", "counts"}

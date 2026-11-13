"""backlog_tree.py -- the piles as one JSON tree for the «Бэклог» pane (a read-only view; the one view of the piles).

Prints {"piles": [{"slug", "title", "batches": [{"n", "title", "status", "prio", "who", "nodes": [...]}]}], "counts": {...}}
built with the ONE parser of the piles, tools/piles.py `load_tree` (AR-13 of the forge: no second reader of the batch files).
A closed batch is left out; a pile with no open batch is left out. Writes nothing.
"""
import collections
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import piles as P  # noqa: E402
import streams  # noqa: E402

PRIO_RE = re.compile(r"П\s*([123])")
CLOSED_WORDS = ("закрыта",)
DONE_NODE = ("принято", "закрыт", "отклонено")


def _prio(text):
    m = PRIO_RE.search(text or "")
    return "П" + m.group(1) if m else ""


def _title(text):
    """The card title without its markdown, for one line of the pane."""
    return re.sub(r"[*`]", "", text or "").strip()


def tree(root=ROOT):
    t = P.load_tree(root, tolerant=True)
    out, counts = [], collections.Counter()
    for slug in sorted(t.piles):
        pile = t.piles[slug]
        batches = []
        for b in sorted(pile.batches, key=lambda x: x.n):
            if (b.status_raw or "").startswith(CLOSED_WORDS):
                continue
            prio = _prio(b.header.get("приоритет", ""))
            nodes = []
            for n in b.nodes:
                status = (n.status_raw or "").strip()
                if status.startswith(DONE_NODE):
                    continue
                nodes.append({"id": n.id, "status": status.split()[0] if status else "", "what": _title(n.what)[:220]})
            counts[prio or "—"] += len(nodes)
            batches.append({"n": b.n, "title": _title(b.title), "status": (b.status_raw or "").split()[0] if b.status_raw else "",
                            "prio": prio, "who": b.who, "nodes": nodes})
        if batches:
            # The owner's order (01.11.2026): inside a pile П1 → П2 → П3; piles by their most urgent batch.
            batches.sort(key=lambda b: (_rank(b["prio"]), b["n"]))
            card_title = _title(pile.card.title) if getattr(pile.card, "title", "") else slug
            out.append({"slug": slug, "title": card_title, "batches": batches})
    out.sort(key=lambda p: (min(_rank(b["prio"]) for b in p["batches"]), p["slug"]))
    return {"piles": out, "counts": dict(counts)}


def _rank(prio):
    """П1 → 1, П2 → 2, П3 → 3; a batch with no priority goes last."""
    return int(prio[1]) if prio else 4


if __name__ == "__main__":
    streams.utf8_stdio()
    print(json.dumps(tree(), ensure_ascii=False))

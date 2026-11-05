#!/usr/bin/env python3
"""The texts the scribe reads BEFORE the work (FR-38, t-109 piece P10): key presence, per file.

The report's counts and statuses are code's (`report_facts.py`); what keeps a role from typing them
again is one sentence in each text it reads. A text nothing tests drifts back to "write the counts
yourself", so this file holds the sentences down:

  * the charter says to run `report_facts.py --task <TICKET> --write` first, to never type a number the
    blocks carry, and to pass `--check` before the handoff - inside the charter cap of 9,000 bytes;
  * `phases/s8.md` names the `--write` / `--check` pair;
  * `phases/s9.md` replaces the old "append Decided at gate B by hand" step with the rebuild, keeps the
    retro's proposals "outside the blocks", and names `state/report-history/`;
  * the gate-B handoff names the sections by their headings, `Decided at gate A` and `Open questions`
    included;
  * the scribe's ahead-card carries every heading of `grammar.REPORT_SECTIONS`, in order.

The keys are quoted verbatim from the task's DoD, written before the first run. A key-presence check
that cannot fail proves nothing, so the last block is the NEGATIVE CONTROL: a key that is in no text is
reported absent, and a copy of the charter with its `never type a number` sentence removed fails the
same check.

Run on its own: `python -B scripts/tests/test_report_texts.py`.
"""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import check, check_eq, check_in, check_not_in  # noqa: E402

sys.path.insert(0, str(harness.SCRIPTS))
import grammar as G  # noqa: E402

PLUGIN = harness.PLUGIN_ROOT
CHARTER = PLUGIN / "agents" / "qa-doc-scribe.md"
S8 = PLUGIN / "skills" / "qa-story" / "phases" / "s8.md"
S9 = PLUGIN / "skills" / "qa-story" / "phases" / "s9.md"
HANDOFF = PLUGIN / "handoffs" / "s8-scribe-to-gate-b.yaml"
CARDS = PLUGIN / "references" / "ahead-cards.json"
CONTRACT = PLUGIN / "references" / "artifact-contract-results.md"
CHARTER_MAX_BYTES = 9000   # builder-rules item 5, measured with `wc -c`
CARD_MAX_BYTES = 1200      # test_ahead_cards.py's own cap for a card

# The keys, verbatim from the DoD of t-195 (rule 11, doc witness: chosen BEFORE the run).
KEYS = {
    "charter": (CHARTER, ["report_facts.py --task <TICKET> --write", "--check", "never type a number"]),
    "s8.md": (S8, ["report_facts.py --task <TICKET> --write", "--check"]),
    "s9.md": (S9, ["report_facts.py --task <TICKET> --write", "state/report-history/", "outside the blocks"]),
    "handoff": (HANDOFF, ["Decided at gate A", "Open questions"]),
}


def flat(text: str) -> str:
    """One line per text: a key broken across two lines of a wrapped paragraph is still in it."""
    return " ".join(text.split())


def present(key: str, text: str) -> bool:
    """The one presence predicate: the real checks and the negative control both go through it."""
    return key in flat(text)


def card_text() -> str:
    data = json.loads(CARDS.read_text(encoding="utf-8"))
    return data["cards"]["qa-doc-scribe"]["text"]


def table_row(text: str, number: int) -> str:
    """The first markdown table row whose first cell is `number` (the scribe's table: `| 0 | ...`)."""
    for line in text.splitlines():
        if line.startswith(f"| {number} |"):
            return line
    return ""


def sections_in_order(text: str, names) -> bool:
    """Every name in `text`, each after the one before it."""
    at = 0
    for name in names:
        found = text.find(name, at)
        if found < 0:
            return False
        at = found + len(name)
    return True


def main() -> None:
    # --- key presence, per file -------------------------------------------------------------
    for label, (path, keys) in KEYS.items():
        text = path.read_text(encoding="utf-8")
        for key in keys:
            check_in(f"{label} holds `{key}`", key, flat(text))

    # --- the charter stays inside its cap (it was over it: 9,239 B) -----------------------------
    charter = CHARTER.read_text(encoding="utf-8")
    size = len(charter.encode("utf-8"))
    check(f"the charter is within {CHARTER_MAX_BYTES} bytes ({size} B)", size <= CHARTER_MAX_BYTES)

    # --- the old instructions are replaced, not kept beside the new one (FR-10) ------------------
    s9 = S9.read_text(encoding="utf-8")
    check_not_in("s9.md no longer tells the conductor to run --close-gate-b", "--close-gate-b", s9)
    check_not_in("s9.md no longer says the old step appends the section", "appends `## Decided at gate B`", s9)
    check_not_in("s9.md no longer re-runs the report validator", "re-runs the report validator", s9)
    check_not_in("the charter no longer counts nine sections", "Nine sections", charter)
    check_not_in("the charter no longer leaves the gate B section to the closure script",
                 "written by the closure script", charter)
    check_in("the scribe's card says eleven sections, not nine", "Eleven sections", card_text())
    check_not_in("and no longer says nine", "Nine sections", card_text())

    # --- the card carries the code's own section list, in order ---------------------------------
    headings = [s[len("## "):] for s in G.REPORT_SECTIONS]
    check_eq("the code names eleven report sections", len(headings), 11)
    card = card_text()
    for heading in headings:
        check_in(f"the card names the section {heading}", heading, card)
    check("the card names the eleven sections in the code's order", sections_in_order(card, headings))
    check("control: the sections listed in another order are not in order",
          not sections_in_order(card, list(reversed(headings))))

    # --- the handoff names the sections by their headings -----------------------------------------
    handoff = HANDOFF.read_text(encoding="utf-8")
    for heading in ("## Product bugs", "## Left with you", "## Not proven"):
        check_in(f"the handoff's source line names {heading}", heading, handoff)

    # --- t-205 (t-202 F4/F2 texts): the code-owned blocks own the counts and the line ----------------
    # Keys quoted from the DoD of t-205, written before the first run: `artifact-contract-results.md` holds
    # `report_facts.py` and does NOT hold `check_delivery.py` in row 0 of the scribe's table (negative check,
    # with its positive control: the same predicate finds `check_delivery.py` elsewhere in that file).
    contract = CONTRACT.read_text(encoding="utf-8")
    row0 = table_row(contract, 0)
    check("the scribe's table has a row 0", bool(row0), contract[:80])
    check("row 0 holds `report_facts.py`", present("report_facts.py", row0))
    check("row 0 does NOT hold `check_delivery.py`", not present("check_delivery.py", row0))
    check("control: the same predicate finds `check_delivery.py` in the file (the ledger section's readers)",
          present("check_delivery.py", contract))
    check("control: and finds a key row 0 does hold, in the row it extracted", present("delivery_ready", row0))
    check("row 0 no longer tells the scribe to type the counts or copy the line",
          not present("verbatim from", row0) and present("you type none of them", row0))
    # the scribe's card likewise, and the card still fits its cap
    card = card_text()
    check("the card does not send the scribe to check_delivery.py for delivery_ready",
          not present("verbatim from check_delivery.py", card) and present("report_facts.py", card))
    check("the card says the line is the block's, and check_delivery.py only feeds it",
          present("`delivery_ready:` line is the block's (check_delivery.py feeds it)", card))
    check(f"the card is within {CARD_MAX_BYTES} bytes ({len(card.encode('utf-8'))} B)",
          len(card.encode("utf-8")) <= CARD_MAX_BYTES)
    # s9.md says what `--write` prints, and no longer promises a line it never prints
    check("s9.md names the line `--write` prints", present("code-owned blocks refreshed", s9))
    check("s9.md says the S8 hook, not `--write`, checks an item's `How:`", present("is checked by the S8 hook, not here", s9))
    check("s9.md no longer promises that `--write` prints an item with no `How:`",
          not present("a problem outside the blocks (an item with no", s9))

    # --- NEGATIVE CONTROL: a check that cannot fail is indistinguishable from a broken one --------
    absent_key = "zz-not-in-the-charter-zz"
    check(f"control: `{absent_key}` is reported absent from the charter", not present(absent_key, charter))
    check("control: and absent from every other owned text",
          not any(present(absent_key, p.read_text(encoding="utf-8")) for p in (S8, S9, HANDOFF, CARDS)))
    tmp = harness.temp_dir("qa-report-texts-")
    try:
        sentence = "never type a number"
        check("control: the sentence to remove is in the charter to begin with", sentence in charter)
        stripped = tmp / "qa-doc-scribe.md"
        stripped.write_text(charter.replace(sentence, ""), encoding="utf-8")
        check(f"control: a copy of the charter without `{sentence}` FAILS the same check",
              not present(sentence, stripped.read_text(encoding="utf-8")))
        check("control: and the real charter passes it", present(sentence, charter))
        # the same for the t-205 keys: put the old words back and the check must fail
        old_row = contract.replace("you type none of them", "the line verbatim from `check_delivery.py`")
        check("control: a contract whose row 0 names `check_delivery.py` again FAILS the row-0 check",
              present("check_delivery.py", table_row(old_row, 0)))
        old_s9 = s9.replace("an item with no `How:` is checked by", "a problem outside the blocks (an item with no `How:`) is checked by")
        check("control: an s9.md with the old promise back FAILS the s9 check",
              present("a problem outside the blocks (an item with no", old_s9))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    harness.finish("test_report_texts")


if __name__ == "__main__":
    main()

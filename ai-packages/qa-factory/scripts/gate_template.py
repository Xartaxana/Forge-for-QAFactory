"""gate_template.py - the one predicate for a true accept site of a gate row (A26, FR-59).

A gate that consumes a verdict word to let something through (reuse a probe, close a review, count a
receipt) asks `acceptable(value, "<gate>.<consumer>")` and nothing else; it never lists the good words
itself. The words, their classes and the consumer's tokens are DATA in references/gate-registry.json
(the row's `words`, `verdict_map`, `accepts`, `promotable`), read only through
`gate_registry.load_registry` (AR-13); this module holds no word list of its own.

THE ERROR DIRECTION is one way: toward NOT acceptable, and nothing here raises. An unknown consumer, an
unreadable registry, a word outside the row's vocabulary (case-exact, no strip), a non-str word, a
record without its field, a row without `words` / `verdict_map` / `accepts` all return False. A word
of class `unknown` or `mismatched` is never acceptable, whatever a consumer lists (FR-59; the registry
check refuses such a token, this is the second wall).

  value     a word (str), or a record (dict) whose word is `value[row["field"]]`
  consumer  `<gate>.<consumer>`, the key of one row's `accepts`
  registry  a dict replaces the file (the seam the tests use); None reads the file once per process

The caller computes the word NOW (`same_test(now, bound)`, `compare_identity(now, before)`) and passes it:
freshness belongs to the producer of the word, which returns "" / "different" / "unknown" (none of them
acceptable here) for a record measured on other bytes.

`registry_problem()` says why the registry cannot be used ("" when it can), for a site that must tell a
person that a reuse was refused because of the registry, not because of the word.

This file writes nothing and has no CLI (FR-45). It is registered as a `library` site of the row
`provenance_acceptance`: its body compares the anchor words `matched` / `person_confirmed`.
"""
import gate_registry

_READ = []        # [(registry, reason)] once per process; a file that could not be read is cached as such


def _file_registry():
    if not _READ:
        _READ.append(gate_registry.load_registry(gate_registry.PLUGIN_ROOT))
    return _READ[0]


def _registry_and_reason(registry):
    if registry is not None:
        return registry, gate_registry.structural_error(registry)
    return _file_registry()


def registry_problem(*, registry=None) -> str:
    """"" when the registry reads and carries `rows`, else the reason (the text of `load_registry` /
    `structural_error`). Never raises."""
    try:
        data, why = _registry_and_reason(registry)
        if why:
            return str(why)
        if data is None:
            return "it is not available"
        return ""
    except Exception as exc:  # noqa: BLE001 - the answer of a reader that must never raise
        return f"it cannot be read ({type(exc).__name__})"


REGISTRY_BLOCK = "gate registry unreadable"   # the dispatch stop's block; the door text of tools/controller-blocks-gen.py:354 is a copy


def registry_why(reason, tail) -> str:
    """THE sentence for "the gate registry cannot be read" (RD1-27, AR-16, P31): ONE head, `reason` is `registry_problem()`'s text,
    `tail` what the site adds: "the gate registry cannot be read (R): a factory defect, <tail>". The dispatch stop opens it with
    `REGISTRY_BLOCK + ": "` (the dispatch stop's block; the door text of `tools/controller-blocks-gen.py:354` is a copy; pinned by tests)."""
    return f"the gate registry cannot be read ({reason}): a factory defect, {tail}"


def acceptable(value, consumer, *, registry=None) -> bool:
    """True only when `consumer` is registered, `value` is an exact word of its row, and the word's class is
    one the consumer's `accepts` tokens take. Every doubt is False; never raises."""
    try:
        data, why = _registry_and_reason(registry)
        if why or not isinstance(data, dict) or not isinstance(consumer, str):
            return False
        row = next((r for r in data["rows"]
                    if isinstance(r, dict) and isinstance(r.get("accepts"), dict) and consumer in r["accepts"]), None)
        if row is None:
            return False
        tokens = row["accepts"][consumer]
        words, vmap = row.get("words"), row.get("verdict_map")
        if not isinstance(tokens, list) or not isinstance(words, list) or not isinstance(vmap, dict):
            return False
        word = value
        if isinstance(value, dict):
            field = row.get("field")
            if not isinstance(field, str) or not field:
                return False
            word = value.get(field)
        if not isinstance(word, str) or word not in words:
            return False
        entry = vmap.get(word)
        if not isinstance(entry, dict):
            return False
        cls, reason = entry.get("class"), entry.get("reason_code")
        if cls == "matched":
            return "matched" in tokens
        if cls == "person_confirmed":
            return "person_confirmed" in tokens and row.get("promotable") is True
        if cls == "not_applicable":
            return "not_applicable" in tokens or (isinstance(reason, str) and bool(reason)
                                                  and f"not_applicable:{reason}" in tokens)
        return False
    except Exception:  # noqa: BLE001 - a malformed registry is "not acceptable", never an error
        return False

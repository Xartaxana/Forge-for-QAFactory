"""The one ASCII line helper of tools/ (FG7-56, FG7-61; AR-15): a hook line or a report line built from a value
this module does not author is cut by ONE body, not by a copy per hook. A leaf: stdlib only, imports nothing
from tools/, so every chain file may import it. Each caller keeps its own profile (keywords of `clip`), and
its bytes stay what they were: strip -> control -> encode -> cut, in that order. No cut marker is added.
"""
import re

CTRL_RE = re.compile(r"[\x00-\x1f\x7f]")  # includes \t \n \r: no injected second line
_ERRORS = ("replace", "backslashreplace", None)


def clip(value, max_len, *, errors="replace", control="", strip=True, none=None) -> str:
    """str(value), stripped, control chars replaced by `control`, non-ASCII by `errors`, then cut to `max_len`.

    max_len has no default: a hook line never loses its cap silently (None = deliberately uncapped).
    `none` replaces a None value (default: the text "None"); `control=None`, `errors=None`, `strip=False`
    switch the step off. A mistyped handler or a negative cap (a TAIL cut by slicing) is a ValueError."""
    if errors not in _ERRORS:
        raise ValueError("errors must be 'replace', 'backslashreplace' or None, got %r" % (errors,))
    if max_len is not None and (not isinstance(max_len, int) or max_len < 0):
        raise ValueError("max_len must be None or an int >= 0, got %r" % (max_len,))
    text = none if (value is None and none is not None) else str(value)
    if strip:
        text = text.strip()
    if control is not None:
        text = CTRL_RE.sub(control, text)
    if errors is not None:
        text = text.encode("ascii", errors).decode("ascii")
    return text if max_len is None else text[:max_len]

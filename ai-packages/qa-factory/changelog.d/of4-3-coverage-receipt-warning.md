- `check_coverage.py` no longer passes silently when the coverage map has no receipt: it prints one warning line saying the
  map-to-receipt binding was not checked and that `check_coverage.py --write` writes the map and its receipt. Exit codes are unchanged.

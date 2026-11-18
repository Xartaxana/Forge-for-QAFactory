- `manifest_from_tests.py` rows now take the same pytest id check as hand rows when `manifest_put.py` stores them (marked
  `node_id_check`, an uncollected id refused with the nearest ids, `not_verified` where no collect answers); `--collect` is no
  longer needed and is accepted with a note; a hand row carrying a copied `generated_from` is checked too (RD1-35).

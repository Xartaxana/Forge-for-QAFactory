- dry walk test layer: the label ledger of a walk group is now one file per group, `fixtures/driver-exits/known_red/<group>.json`
  (an absent file is an empty ledger, so a red row is a new red and never expected); the shared `known_red.json` keeps only the
  `main/*` rows of the main pass; the census (`dry_exits.py --check`) reads every ledger file, refuses a row that names no row of its own
  group (or a `main/*` row in a group file, or a walk row in the shared file) and refuses one id held by two files; the unused
  `dry_exits.py --judge` branch and its `judge` function are removed (one road, `judge_group`); test layer only, no change for a project

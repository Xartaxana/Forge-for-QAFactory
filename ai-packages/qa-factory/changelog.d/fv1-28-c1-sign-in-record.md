- the way in a first look found is kept for later stories: after an accepted first look, `first_look.py record-sign-in --task-root <T>`
  (the driver calls the same `first_look.record_sign_in`) writes it to the project's registry as key `environments.sign_in` (one row per
  stand and surface, source `role`), only when the look was accepted and at least one requirement was not blocked by access; a changed
  way is a new row, the same way again is the existing row, a story that leaves no trace records nothing; the one reader is
  `project_knowledge.sign_in` (the order against the project's config is `project_knowledge.SIGN_IN_PRECEDENCE`: recorded, project,
  factory default); a stale way is taken back with `project_knowledge.py revoke`; `first_look.accepted` is the one reader of "the first
  look was accepted" and `first_look.read` now also returns the record's `stand` (FV1-28)

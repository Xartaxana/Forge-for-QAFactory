- The two test fixtures that stand in for a recorded `environment.access` block are now built from the template's own
  block, so a new template key no longer breaks them by hand-copy drift. The stand's login body field names keep one
  reader (`config_contract.body_fields`), which the manual capture already uses; the steps file carries no body.

- the reuse of an earlier reporter-rehearsal proof now reads the producer's state word through the gate registry
  (`gate_template.acceptable`, consumer `reporter_rehearsal_identity.reuse`) instead of comparing it to `same_command` in
  `gate_preflight._reporter_outcome`: a state that is absent, in another case, not a string, or read while the registry cannot
  be read is never reused and the command is rehearsed again, exactly as an unknown state already was; the two hit checks (the key
  must hit) still come first, and the registry row `reporter_rehearsal_identity` is converted (B-283)

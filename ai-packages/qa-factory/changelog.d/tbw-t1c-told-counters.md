- `stage_joints.py`, `refusal_registry.py`: `stage_joints.audit` judges more of the told-before-work joint data. It reads the check ids of the
  scripts (K2 page leg, K3 and K7 requirement carriers, E4 shape, E7 duplicate ids) and compares the `hand_cards`, `legacy_legs` and
  `unsited` counters of the rows file against their stored ceilings; an unreadable card file or an absent counter is a named problem, never
  zero. `refusal_registry.CHECK_PASSTHROUGH` lists the one wrapper (`exit_gate.own`) whose check id is read through it, so the scan no
  longer reports its argument as unreadable.

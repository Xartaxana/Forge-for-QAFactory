- `handoff_init.py` takes `--purpose <word>`: the handover row a dispatch serves by purpose (S5's plan pair, `s5_plan`) is now reachable
  through the tool, not only through `--contract`. An empty or whitespace-only value reads as none (the stage's usual contract); an
  unknown purpose is refused naming it and the purposes the registry knows for that stage and role (or saying none carries one); a
  value with a space, over 64 characters, or not lowercase letters, digits and `_` is a call refusal; `--contract` still wins and its
  purpose is not judged (OF5-7)

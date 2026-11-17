- dry-world walker: an optional walk-row field `offered_if` names ONE fact of `dry_world.WORLD_FACTS` (today `inventory_unavailable`, read through the
  product's own `source_inventory.completeness`); a row whose answer is offered only under that condition is judged as before when the condition holds,
  is a NOTE `unreached` (never red) when it does not hold, and is refused with `condition named, no world for it` when the world cannot answer it
  (an unknown key is refused naming the known keys and the door); a row with no `offered_if` is judged exactly as before (FV3-17)
  - a row whose condition does not hold but whose token was offered is a FAIL (drift), and a FAIL of the ask-level checks wins over the `unreached` NOTE

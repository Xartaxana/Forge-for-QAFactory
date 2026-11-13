- `scripts/native_context.py` (`stage`): a packet file under the launch's key whose JSON is not an object (a list, a string, a number,
  `null`) is an unreadable packet and takes the road a corrupt one takes (a `ValueError` the hook turns into a refusal naming the
  file), instead of an `AttributeError` that let the launch run without its context; an empty or unparsable file and an empty
  object behave as before
- the refusal of a launch whose packet is still pending now also names a door for a launch that never started: relaunch the role under
  a unique task name; the start of the text is unchanged

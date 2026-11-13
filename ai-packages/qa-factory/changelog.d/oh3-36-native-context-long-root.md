- native role launch (`inject_context.py`, `native_context.py`): a launch whose context cannot be written (for example a
  project folder longer than the supported limit (143 characters after OH6-3) on Windows without long paths) is now refused with
  the cause and the way out, or passed by the person's recorded word, instead of starting the role without its context;
  and a launch receipt or packet record that cannot be written at the child's start no longer stops the context from
  being delivered - it is reported instead (OH3-36)

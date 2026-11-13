- The S5 plan now receives the case critic's concerns, including every request to parametrise cases into one test, whether the
  plan is small or large; on the driver process each S5 window receives the concerns of its own cases. `s5_plan.py --check` adds a
  hint when the plan leaves such cases in separate tests without an `apart_reason`, and the plan critic treats an unanswered one as a
  blocker. Cases the driver's cut puts in two windows still cannot be merged by either window (TQ2-1)

- the test planner can ask an unanswered question again in clearer words from its plan: a plan row's `reword_questions` entries
  (`{"question": "Q<n>", "text": "<clearer words>", "readings": [...] (optional), "why": "<one line>"}`) are executed when S3 closes
  (`planning_contract.project_plan`, new `_reword_plan_entries`) through the register's one writer `question_register.reword` (role
  `qa-test-strategist`); a done entry leaves the row, a refused or malformed one stays on it with a line naming the row and the entry
  (`project_plan(...).notes`), and never stops the other entries or rows; an approved plan executes nothing and says so; a plan with
  no such key reads and writes exactly as before (FV1-9)

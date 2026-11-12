# The permission block - only when asked

When asked why every command needs a confirmation, print this block
to paste into the project's `.claude/settings.json`, and say what it does and does not allow:

```json
{"permissions": {"allow": [
  "Bash(python \"${CLAUDE_PLUGIN_ROOT}/scripts/*.py\":*)",
  "Bash(git status:*)", "Bash(git diff:*)", "Bash(git log:*)", "Bash(git show:*)",
  "Bash(git rev-parse:*)", "Bash(grep:*)", "Bash(find:*)", "Bash(ls:*)"
]}}
```

Reading and the factory's own scripts, nothing else: no commit, push, tracker command or
test framework. It saves wall-clock time, not money. **The human writes that file, not
you**: the factory writes nothing into a project except `qa-factory/` and its own `.gitignore` block.

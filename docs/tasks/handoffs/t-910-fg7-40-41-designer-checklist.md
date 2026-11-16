# t-910 FG7-40 / FG7-41 report

Done: two sentences appended to `.claude/agents/designer.md` (staged, not committed; no commit attempted, so no gate refusal to report).
- FG7-41: end of rule 1's package paragraph.
- FG7-40: end of rule 6 (next to "A residual of this class is a node with owns and a test"). Findings pointed at the rule-1 area but that sentence lives in rule 6.
No rule renumbered or reworded. Size cap: `git grep designer.md -- tools` finds no byte/line cap on designer.md (only anchor pins in test_role_carriers_one_owner.py, test_handoff_rule_anchors.py); role-load.json has no designer entry.

DoD: `python -B -m pytest tools/tests/test_role_carriers_one_owner.py -q -p no:cacheprovider`
Output (verbatim tail):
```
.......................................                                  [100%]
39 passed in 0.78s
```

## Diff of designer.md
Rule 1 paragraph, appended: Commit-line templates the spec prescribes to a builder are given in the gate's own form, and the only carrier of that form is `tools/architecture_gate.py` (point to it, do not copy the grammar); `judgment: none` always carries its ` -- <why>`, and a spec never prescribes it bare.
Rule 6, appended after "Siblings: SIBLING_MAP axis 34.": Every PRODUCER the spec names (a script, a role or a step that must write a field, a file or an output line) is produced by a node or stream with `owns:`; a producer with no owning node is returned as a fork/question, never left implied.

## Gate lines (tools/architecture_gate.py)
Docstring item 6, lines 34-38:
```
6. The `judgment:` line (t-1765 2.4). A package commit also carries at least one own line of
       judgment: none -- <why the change moves no judgment>
       judgment: adds data check <unit> -- <why this is a data check or a guard, not judgment>
       judgment: moves <what> to role -- <why>
       judgment: moves <what> to code -- <why>
```
Code, judgment_form lines 193-196: `if not sep: return None, "the line `judgment: %s` has no ` -- <why>` part"`; `if head == "none": return ("none", None) if why else (None, "`judgment: none --` carries no reason after the dashes")`. Empty text after `--` is refused for every form (lines 201, 205).

## Text for CLAUDE.md, for the Lead
- FG7-40 -> rule 11, five-point checklist point (3) ("given" enumerated and sufficient) / point (4) (writing dispatch): "Every producer the spec names (a script, role or step that must write a field, file or output line) has a node or stream with `owns:` in the dispatch set, or the spec names the existing node that owns it; a producer with no owning node is returned as a fork, not dispatched."
- FG7-41 -> rule 11, five-point checklist point (4) (writing dispatch): "Commit-line templates in a dispatch are given in the gate's own form (`tools/architecture_gate.py` is the only carrier; point to it): `architecture: AR-n -- <how kept>` or `architecture: none -- <reason>`, and `judgment: none -- <why>` (or `adds data check <unit> -- <why>` / `moves <what> to role|code -- <why>`); a bare `judgment: none` is refused."

## Siblings
`git grep -n -i -E "judgment: none|PRODUCER|owns:"` over builder.md and critic.md: no hits. builder.md does not prescribe commit lines (it receives them), critic.md does not draft specs, so neither carries nor needs the lines (report only; builder.md may merit a "use the dispatch's lines as given" note, not queued by me).

## Questions
none

## Needed beyond the manifest
tools/tests/test_role_carriers_one_owner.py, tools/tests/test_handoff_rule_anchors.py (cap search), ai-packages/qa-factory/references/role-load.json

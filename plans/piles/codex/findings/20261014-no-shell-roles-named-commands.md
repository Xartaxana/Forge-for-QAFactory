# Тексты фабрики называют команды оболочки ролям без Bash (брифы, справочники, отказы)

id: — | кучка: `codex` | от: Dev2 (прогон TP2-2406 S4, Codex Desktop), 14.10.2026 | приоритет: П2 | кандидат наверх: нет

Что не так / что сделать: на Codex Desktop каждая роль получает `exec`, и роль без Bash в своём `tools:` (qa-case-designer,
qa-case-critic, qa-test-strategist) послушно выполняет команду, которую ей назвал текст фабрики, а гард роли
(`host_adapter.role_policy`) её отказывает — роль останавливается с нетронутой формой (S4-6/S4-7, 14.10: «FACTORY ROLE:
qa-case-designer may read using rg/Get-Content without shell chaining; arbitrary shell execution is not permitted»).
Промпт запуска починен в t-013 (`story_step._prompt` ветвится по `guard_pre_tool.role_ways`; тест
`test_story_step_prompt.py` прогоняет каждую названную команду каждой роли через настоящий гард). Та же ловушка
остаётся в других носителях (вердикт критика t-013, F-3 и заметки, `docs/tasks/specs/reviews/t-013-handoff-prompt-review.md`):

- (а) `brief_pack.py:85-87` `SLICE_INSTEAD` — дизайнеру и критику S4 выдаётся `manifest_view.py` (бриф, который промпт
  велит прочесть первым); `brief_pack.py:135-141` — карточка инструментов стратега называет `planning_contract.py`
  и `plan_row.py`; `brief_pack.py:89` `NO_SHELL` — мёртвый второй список ролей без оболочки (без стратега).
  Следующий узел той же темы.
- (б) `references/common-rules.md:82-85` и `references/handoffs.md:16-17` — `handoff_check.py --set` каждой роли без
  оговорки о Bash.
- (в) `host_adapter.py:245` — отказ гарда не называет дверь записи для роли без Bash (FR-1); по слову владельца гард
  не трогали.
- (г) `story_step.py:1024-1026` (отказ `finish`) и `guard_pre_tool.py:1773` называют `handoff_help.py` роли, у
  которой может не быть Bash.
- (д) Роли без Bash теряют `.help.yaml`: `finish` должен запускать `handoff_help` при непустом `blocked` (N-4).
- (е) `role_ways` при сомнении отвечает {Edit, Bash} (для гарда верно, для промпта — нет): параметр `doubt=`,
  регулярка `^tools:\s*(.+)$` на пустой строке `tools:` переходит на следующую строку; `role_ways` читает весь файл,
  `role_policy` — только фронтматтер (N-1).
- (з) После t-015 (бриф починен для дизайнера/критика/стратега; вердикт критика t-015,
  `docs/tasks/specs/reviews/t-015-brief-roles-review.md`): `guard_pre_tool.py:1059` — отказ переписи test-plan говорит
  стратегу «меняется plan_row.py, никогда руками», противореча его карточке без оболочки и отказу `:1029`;
  `references/role-commands.json:86-90` — `plan_row.py` разрешён только двум ролям без Bash, дверь мёртвая;
  `audit_factory.py:146` — комментарий о карточке стратега устарел; `brief_pack.py` `TOOLING["qa-test-strategist"]`
  недостижим, пока у стратега нет Bash; на Desktop голова карточки без оболочки называет только целый
  `Get-Content`, хотя гард пускает `rg`/`Select-String` — при плане в 36 КБ «не читать целиком» невыполнимо как
  написано: назвать формы диапазона (`rg -n`, `Get-Content -TotalCount`, `Select-String -Context`); путь
  context-manifest в брифе дизайнера назван дважды (~60 байт); `story_step.py:254` говорит, что бриф «называет
  команды», а бриф без оболочки не называет ни одной; карточки `references/ahead-cards.json` называют проверяющую
  сторону (`critic_rollcall.py`, `planning_contract.py`) — данные, не инструкции, принято как есть; тест пропускает
  их секцию, команда без `.py` в карточке прошла бы незамеченной.
- (ж) Один тест на класс: `test_story_step_prompt` закрывает промпт; брифы и справочники — тем же приёмом
  (отрендерить, выделить команды, прогнать через гард).

Свидетель: роллауты S4-6 (`rollout-2026-10-14T13-47-10-01a13a3c…`, строки 32/58) и S4-7
(`rollout-2026-10-14T14-02-50-01a13a4b…`, строка 93); `work/briefs/S4-qa-case-designer-7.launch.md:9`;
диагноз `docs/tasks/specs/reviews/t-012-s4-handoff-guard-diagnosis.md` (репродукция e1–e5 на копии).

Принципы и правила: P14, P15, FR-1, FR-2, FR-15, FR-17, FR-38, FR-56, FR-57.

Решение владельца нужно: нет.
перенесено из ветки dev2/codex-overhead-fixes (plans/piles/roles-context/findings/20261014-no-shell-roles-named-commands.md), узел: CX1-6

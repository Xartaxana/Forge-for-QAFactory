# Читатели транскриптов вне хуков (CLI) и раскладка workflows — очередь после `tools/transcripts.py` (B-467)

id: — | кучка: `forge` | от: дизайнер t-612 / критик t-615 / Lead, 09.10 | приоритет: П3 | кандидат наверх: нет

Что не так / что сделать: узел B-467 (спека `docs/tasks/specs/t-612-b-467-transcripts.md`, развилка F2 (a)) сводит
в `tools/transcripts.py` только четырёх потребителей-хуков (`dispatch_gate`, `journal_echo`, `tier_echo`,
`agent_budget`); у них направление ошибки «молчать / считать живым». Остальные читатели `agent-*.jsonl` — CLI с
противоположным направлением («не потерять ни строки») — остаются со своими копиями и ждут отдельного узла:
(1) парсеры транскриптов `usage_report.py:299-317` (рекурсивный glob, покрывает и `workflows/`), `warn_density.py:546-556`,
`permission_audit.py:340-342`; (2) близнецы корня проектов `usage_report.py:314`, `warn_density.py:126`,
`permission_audit.py:143` → `transcripts.projects_root`; (3) близнецы слага проекта `exam_runner.project_slug:243` и
`permission_audit._default_project_key:114`; (4) `usage_report.py:291` держит собственный `SKIP_MODELS` (критик t-615) →
`transcripts.SKIP_MODELS`; (5) раскладка `subagents/workflows/wf_*/agent-*.jsonl` (развилка F10): лимит параллельных
воркеров её не считает, `journal_echo` в ней не ищет (`:594-596`), `usage_report` покрывает — решить, считать ли воркеров
workflow живыми для лимита; (6) писатели фикстур транскриптов в тестах (`test_dispatch_gate` `_subagents_home`/`_finish`,
`test_journal_echo` `_write_agent_transcript`, `test_agent_budget` `_assistant`/`_write`, `test_tier_echo`
`_write_transcript`, `hook_liveness_probe:579-581`) — один testkit; (7) `TAIL_BYTES` off-by-one (`agent_budget` :89:
последняя строка ровно 65536 байт теряется; подтверждено пробой t-615) — узел B-467 закрепляет его тестом как есть,
починка здесь. Правило оси 14 (пишет Lead в коммите слияния B-467): новый читатель `agent-*.jsonl` зовёт `transcripts`;
разделитель JSONL — только `\n` (не ось 7).

Свидетель: спека t-612 («Clone groups», F2, F10), вердикт `docs/tasks/specs/reviews/t-615-b-467-plan.md` (п. 5,
«Trail» — 1072 транскрипта на машине, 0 дублей id).

Принципы и правила: правило 9 (класс, не экземпляр), ось 14 SIBLING_MAP (после слияния), бриф критика п. 6.

Решение владельца нужно: нет.

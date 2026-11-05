# Предложения для CX1-11: что сказать про возврат по роллауту в `references/codex-host.md` и `controller-api.md`

id: — | кучка: `driver-hosts` | от: билдер t-971 (узел CX1-3), по критику t-969 F-5 / F-6, 19.10.2026 | приоритет: П2 | кандидат наверх: нет (носитель — узел CX1-11, первый владелец `references/codex-host.md`)

Что не так / что сделать: после CX1-3 расписка `story_step`, чей роллаут кончается чистым `task_complete` этого запуска (не раньше
`bound_at`, старше `dispatch.native_completion_grace_s`, единственный незавершённый кандидат пути), — это `returned` ДО возраста
расписки, и `next` / `recover` закрывают по нему диспатч в `returned_unaccepted`. `references/controller-api.md:28–37` перечисляет
доказательства `state()` и этого не знает; бюджета байтов у файла нет (пачка :195, :204), поэтому правка идёт не туда, а в
`references/codex-host.md` (порядок CX1-11 → CX1-13 → CX1-14). Предлагаемые фразы (английский, для роли и оркестратора):

1. «A `story_step` receipt whose host rollout ends with `task_complete` of this launch, older than
   `dispatch.native_completion_grace_s` (300 s), reads `returned`: the role stopped. Nothing is written to the receipt and no work is
   accepted — `next` closes the dispatch as `returned_unaccepted`, and the checkpoint and `accept` operations are open again.»
2. «Evidence of a rollout that nobody could read (compressed `.jsonl.zst`, cut mid-row) is said as `rollout unreadable: <reason>`;
   it never counts as a return. A worker that completed less than the grace window ago is `alive` ("its stop hooks may still send it back").»
3. Ключ: `dispatch.native_completion_grace_s` (число секунд > 0; умолчание 300; `references/templates/config.json`, `config-keys.json`,
   модульное умолчание `dispatch_liveness.NATIVE_COMPLETION_GRACE_S`).

Свидетель: `references/controller-api.md:28–37` (перечень доказательств `state()` без роллаута); `scripts/dispatch_liveness.py`
(`native_stop`, `NATIVE_COMPLETION_GRACE_S`); `plans/piles/codex/batch-1-overhead-fixes.md` (узел CX1-3, CX1-11).

Принципы и правила: P10, FR-37, FR-44.

Решение владельца нужно: нет

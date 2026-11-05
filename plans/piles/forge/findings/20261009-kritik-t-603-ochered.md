# Очередь критика t-603 (остатки пачки 1): шесть пунктов «в очередь»

id: — | кучка: `forge` | от: критик t-603, 09.10 | приоритет: П3 | кандидат наверх: нет

Что не так / что сделать (вердикт `docs/tasks/specs/reviews/t-603-batch-1-leftovers.md`; F-5 и F-13 ушли в B-472 / узел F2-8):
- F-8 (развилка Lead): два читателя имени переменной токена с противоположным поведением на негодном конфиге —
  `ci_read.token_env_name` откатывается на `GITLAB_TOKEN`, `piles_gitlab.py:633-643` отказывает; оба умеют писать
  (`--apply`, `start`). Один помощник, одно поведение — Lead выбирает (отказ безопаснее для пишущих команд).
- F-9: `skip()` в `scripts/tests/test_critic_rollcall_apply_fixes.py` ключуется на `PYTEST_CURRENT_TEST`, который
  наследуют дочерние процессы pytest-теста; точный сигнал — `"pytest" in sys.modules`. Сегодня таких вызовов нет;
  ложный FAIL, не ложный pass.
- F-10: `forge_metrics.run_check` вырос до 87 строк, `compute` 191; `counts["finding_warnings"]` — список внутри
  словаря счётчиков. Выделить `_findings_check`.
- F-11: одна цепочка декодирования (`decode("utf-8","replace")` + CRLF→LF) скопирована в трёх вызывающих
  `gitcmd` (`forge_metrics`, `r3_integration_check`, `exam_runner`) — текстовый помощник в `gitcmd`.
- F-12: под `--base` красные строки перемаркируются заменой строки («origin/main <sha7>» → «the --base <sha7>»);
  передавать метку в сравнители.
- F-14: `tools/test_piles_close_gate.py:66` `assert code == 2 and A or B` — при истинном B код выхода не проверяется.

Свидетель: `docs/tasks/specs/reviews/t-603-batch-1-leftovers.md`, таблица находок.

Принципы и правила: P10/P12, FR-17, FR-54; бриф критика `docs/tasks/critic-diff-brief.md` п. 6–7.

Решение владельца нужно: нет.

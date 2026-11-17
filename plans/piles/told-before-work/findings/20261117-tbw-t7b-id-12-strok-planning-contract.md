# id 12 строк `planning_contract`

id: — | кучка: `told-before-work` | от: спека «Told before work: finish» (`docs/tasks/specs/20261117-told-before-work-finish-spec.md`), 17.11.2026 | приоритет: П1 | кандидат наверх: нет

Что не так / что сделать: Класс: требование плана S3 названо в строках, сайты отказов id не несут (AR-9, AR-10).

Что именно менять: `planning_contract.py`: 12 id на своих сайтах (`gate_plan_errors`, `validate_plan`, `contradiction_errors`, `_branch_block_lines`, `s3_branch_refusals`, `fence_lines`, `_regression_findings`, `fit_target_block`, `_request_findings`, `_detector_body`); блоки REJECT побайтно прежние. Задачи `regression` идут из `regression_scope.problems`: id на зовущем (EC-2), `regression_scope.py` не правится. Докстринг `_regression_findings` переформулируется (F-W5 (a)). Не трогать `unmarked_revision_errors` (его строка дирижёра — в TBW1-11 (T9c)). Тест `tbw_t7b_sites`.

Карточка: `docs/tasks/specs/20261117-told-before-work-finish-spec.md`, карточка §6 «Card T7b» — читать там, не копировать сюда.

Свидетель: спека wave0 §3a; F-W4 (b), F-W5 (a).

Принципы и правила: AR-9, AR-13, AR-18, AR-29.

Решение владельца нужно: нет.

# BATCH CANON пачки живёт только в прозе: ни скрипта, ни строки CI; рецепт докера — в памяти Lead и CURRENT_CONTEXT

id: — | кучка: `onboarding-forge` | от: скаут t-1205 Q3 (`docs/tasks/handoffs/t-1205-verification-carriers.md`), D-0056 (3) | приоритет: П2 | кандидат наверх: нет

Что не так / что сделать: D-0056 (3) переносит соседей, большие файлы, докер, храповики, аудит и мутационный проход на
один BATCH CANON интегратора, но канон определён только словами (DECISIONS.md:74, PROJECT.md п. 2, builder-rules 7b,
бриф критика); `git ls-files | grep -i canon` пуст, `.gitlab-ci.yml` и RUNBOOK его не называют, рецепт докера на
tar-копии (`MSYS_NO_PATHCONV=1 docker run … tar -C /src …`) есть только в памяти Lead и в CURRENT_CONTEXT.md:95. Каждый
интегратор собирает канон заново руками, свидетель «BATCH CANON» в `accepted` не имеет формы. Что сделать (один узел,
builder): `tools/batch_canon.py <worktree-or-main> --nodes <handoff-files…>` — читает списки тестов и мутаций из
хэндоффов узлов, гоняет соседей и большие файлы в докере python:3.12 на tar-копии (один контейнер), храповики
(`dup_ratchet`, `lint_ratchet`), `selftest.py --limits --lang`, `test_audit_rules.py`, один мутационный проход по
списку каждого узла (мутант на КОПИИ, sha до/после), печатает свидетель в форме для `accepted.witness` («BATCH CANON:
…», файл → результат); RUNBOOK §интеграция и PROJECT.md п. 2 ссылаются на него; CI не трогается (package-fast остаётся
регрессией на пуш). Тест: `tools/tests/test_batch_canon.py` на фикстурном хэндоффе (разбор списков, форма вывода, отказ при
отсутствии докера с дверью «локально по списку»).

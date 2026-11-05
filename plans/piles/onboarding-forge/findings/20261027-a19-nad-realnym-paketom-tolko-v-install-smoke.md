# A19 над реальным пакетом идёт только внутри `install_smoke` (ночь), поэтому роль без обязательного раздела проходит все MR-пайплайны

id: — | кучка: `onboarding-forge` | от: docker-канон релиза 0.10.3, 27.10.2026 | приоритет: П1 | кандидат наверх: нет

Что не так / что сделать: проверка A19 «agents contract» над РЕАЛЬНЫМ пакетом запускается только внутри `install_smoke.py`, то есть в ночном `package-full`. Пайплайны MR (`forge-check`, `package-fast`) её не гоняют, поэтому ролевой файл, потерявший обязательный раздел, проходит все MR. Результат: релиз 0.10.3 ушёл с `agents/qa-code-critic.md` без `## Procedure` (раздел разделён на «On the plan» / «On the code (a window)»), а нашёл это только docker-канон: `A19 agents contract: VIOLATIONS (1) … qa-code-critic.md: missing section(s) ['## Procedure']`.

Что сделать: выполнить A19 (и родственные проверки ролевых файлов реального пакета, A22/A25) в быстром ярусе, который идёт на каждый MR при изменении `ai-packages/qa-factory/agents/`, либо вынести из `install_smoke` в `package-fast` шаг `audit_factory.py` по пакету. Оценить цену времени до решения: измерить, сколько занимает один `audit_factory.py` (FR-26). Класс: проверка, которая ловит дефект, стоит там, где дефект впервые может попасть в `main`; ночная проверка видит его на следующий день.

Свидетель: `D:/ws1/canon-release-0103\out\install_smoke.txt` (хвост), `.gitlab-ci.yml` (`package-fast`, `package-full`), `PROJECT.md` «Как принимается изменение пакета» п. 2.

Принципы и правила: FR-33, FR-54, AR-18, AR-25 (гейт стоит на пути исполнения); дефект пакета — `run-honesty/findings/20261027-regressii-docker-kanona-0-10-3-k11-i-krasnye-selftest-install-smoke.md` (RH1-2).

Решение владельца нужно: нет (цена CI — решение Lead при взятии узла).

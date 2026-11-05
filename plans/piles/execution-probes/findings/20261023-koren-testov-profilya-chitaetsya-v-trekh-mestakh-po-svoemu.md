# Принадлежность пути корню тестов профиля читается в трёх местах по-своему; безымянная строка рядом с именованной под чужим единственным корнем идёт под именованным профилем

id: — | кучка: `execution-probes` | от: Lead пачки hotfix-12586/1 (dev2), 23.10.2026 | приоритет: П2 | кандидат наверх: нет

Узел HF1-3 (EP1-10) свёл выбор профиля по пути к одному читателю `execution_request.profiles_owning(cfg, rel_path)`
(`scripts/execution_request.py:1228`, нормализация `_path_key` — `:1210`: обратные слэши, `./`, `//`, `a/..`, внешние слэши,
регистр на Windows). Он обошёл три соседа того же класса; все три оставлены очередью узла.

(1) `probe_by_code._in_test_root` (`scripts/probe_by_code.py:1108`) — вопрос «лежит ли путь под `roots.test` какого-либо профиля или под
`tests_root`» — нормализует сам: `replace("\\", "/").strip("/")` без `./` и без свёртки регистра. Класс С2 узла (AR-13) в форме
проверки принадлежности, а не выбора; рядом стоит инвариант «дерево продукта не трогается сознательно», поэтому расхождение
нормализаций — не косметика: путь `./tests/x.py` по этой функции вне корня и получает отказ там, где `profiles_owning` его узнает.
Направление ошибки — отказ (безопасное), но гейт и проба расходятся в том, что такое «свой корень».

(2) `gate_preflight.Rehearsal._root_rel` (`scripts/gate_preflight.py:1958`) и `_node_prefix` (`:1967`) — два способа получить «каталог тестов
профиля относительно чего-то» (проект против `tests_root`) с разной обработкой «не лежит внутри»: один возвращает исходную строку, другой
пустую. Класс С7 узла; спека оставила как есть.

(3) Строка манифеста без `profile_id` рядом с именованной, лежащая под корнем, которым владеет только ДРУГОЙ единственный профиль, всё ещё
запускается под именованным профилем: узел закрыл только общий корень двух профилей (отказ с дверью), этот край лежит вне общего корня.

Что сделать: `probe_by_code._in_test_root` использует `execution_request.profiles_owning` / `_path_key` и сохраняет `protected_app_paths`;
`_root_rel`/`_node_prefix` — один помощник с одним ответом на «не внутри»; для (3) — отказ или названная строка отчёта (FR-59),
решение с тестом в `test_profile_shared_root.py`. Мутации: `_path_key` без `normpath` убивает ключ `profiles_owning: tests and ./tests are
one root` (t-055, мутация 1) — для `_in_test_root` нужен свой ключ.

Свидетель: `docs/tasks/handoffs/t-055-hf1-3.md`, «Class sweep (analogs seen, scope not expanded)»: «Queued: `probe_by_code._in_test_root`
(l.1108-1125) has its own root normalisation (no `./`, no case fold) — the same AR-13 class as C2 but a membership test; queue it to use
`_path_key`. An unnamed row beside a named one, under a root only another single profile owns, still runs under the named profile
(outside the shared-root edge). C7 (`_root_rel` vs `_node_prefix`) left as the spec says.» Строки — по дереву пачки, проверены 23.10.2026.

Принципы и правила: FR-17, FR-54, FR-59, AR-3, AR-13, AR-28.

Решение владельца нужно: нет.

# Докстринг `execution_request.path_under` / `profiles_owning` описывает старое чтение `_path_key`, а `profiles_owning` читает `roots.test` сам и может разойтись с `probe_by_code._in_test_root`

id: — | кучка: `onboarding-forge` | от: отчёт узла I B-355 (`wip/b355-i`, t-179/t-186), слова Lead 12.11.2026 («докстринг execution_request и расхождение с `profiles_owning`») | приоритет: П3 | кандидат наверх: нет

## Что наблюдалось

`scripts/execution_request.py` (main): `_path_key` :1605, `path_under` :1616-1622 — докстринг называет `profiles_owning` и `probe_by_code._in_test_root` двумя потребителями «одного сравнения под корнем»; `profiles_owning` :1624-1642 берёт корень сам:
`_path_key((profile.get("roots") or {}).get("test"))` и сравнивает `path_under`.
Узел I B-355 (ветка `wip/b355-i`, в main нет; коммиты 5a7f5e7, 33842e9) переводит `probe_by_code._in_test_root` на чтение корней через `test_locations.is_test_path` (`by == "config"`, источник `roots.test` / `tests_root`): значение, которое читатель игнорирует (`"."`, корень на уровне проекта или выше), игнорируется и там;
`_path_key` и `path_under` в `_in_test_root` остаются только для защищённых путей. Итог после слияния: (1) докстринги `path_under` и `profiles_owning` («the pair `profiles_owning` uses») уже неверны; (2) два читателя `roots.test` — `profiles_owning` (напрямую) и `_in_test_root` (через `test_locations`) — могут давать разные ответы для `"."` и корней на уровне проекта или выше (AR-13). Расхождение именно по этим входам названо отчётом узла I; в main (до I) оба читают через `_path_key` и согласованы.

## Что именно менять

1. `scripts/execution_request.py`: докстринги `_path_key`, `path_under`, `profiles_owning` — назвать фактических потребителей после узла I («`profiles_owning`; для защищённых путей `probe_by_code._in_test_root`»); без изменения поведения.
2. Таблица случаев (`scripts/tests/test_probe_by_code.py` или тест, судящий `profiles_owning`; назвать в спеке узла): корень `roots.test` = `tests`, `./tests/`, `.`, `..`, `../x`, пусто, абсолютный; путь `tests/a.py`, `a.py`, `x/tests/a.py`. Ожидание — из требований (корень `.` и выше корня проекта не владеют ничем — «отказ только в сторону False»), одно на оба читателя.
3. Если таблица покажет расхождение — `profiles_owning` берёт корень тем же правилом игнорирования, что `test_locations` (один читатель, AR-13); решение в узле, расхождение — строкой в отчёте.

Зависит от слияния B-355 I в main (ветка `wip/b355-i`). Принципы и правила: FR-54; AR-13, AR-15, AR-28.

Решение владельца нужно: нет.

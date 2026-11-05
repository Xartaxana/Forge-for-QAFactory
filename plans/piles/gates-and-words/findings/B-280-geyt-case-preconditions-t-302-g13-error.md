# Гейт `case_preconditions` (t-302 G13) — `error` среды считается дефектом фабрики

id: B-280 | кучка: `gates-and-words` | от: новое, 03.10 — после релиза | приоритет: — | кандидат наверх: нет

Что не так / что сделать: **Гейт `case_preconditions` (t-302 G13) — `error` среды считается дефектом фабрики.** `gate_preflight._check_one_precondition`/`check_case_preconditions`: `uncheckable` → карточка человеку (верно); `error` → строка FACTORY_DEFECT и проход в S5 — а ошибка, вызванная средой (HTTP 301-308/401/403 = стена логина, ключ base_url), должна стать неизвестным = вопросом; `planning_contract._unmet_preconditions` гоняет тот же классификатор второй раз (B-255 в). `debt_ref`. [F07]

Свидетель: t-302 R-2 G13; F-cmp2-18/20/26; t-218.

Принципы и правила: FR-19, FR-46, FR-17

Решение владельца нужно: нет (фраза не найдена)

<!-- piles split: plans/BACKLOG.md, раздел 7 «Релизы, приёмки, инфраструктура разработки»; ячейки строки перенесены дословно -->

Строка BACKLOG.md целиком:

```
| B-280 | **Гейт `case_preconditions` (t-302 G13) — `error` среды считается дефектом фабрики.** `gate_preflight._check_one_precondition`/`check_case_preconditions`: `uncheckable` → карточка человеку (верно); `error` → строка FACTORY_DEFECT и проход в S5 — а ошибка, вызванная средой (HTTP 301-308/401/403 = стена логина, ключ base_url), должна стать неизвестным = вопросом; `planning_contract._unmet_preconditions` гоняет тот же классификатор второй раз (B-255 в). `debt_ref`. [F07] | t-302 R-2 G13; F-cmp2-18/20/26; t-218. | новое, 03.10 — после релиза | FR-19, FR-46, FR-17 |
```

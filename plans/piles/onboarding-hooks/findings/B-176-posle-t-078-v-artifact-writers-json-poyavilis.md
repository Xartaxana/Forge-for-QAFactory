# После t-078 в `artifact-writers.json` появились ключи-пути (`work/test-cases/critic-findings.md`,…

id: B-176 | кучка: `onboarding-hooks` | от: новое, 30.09 | приоритет: — | кандидат наверх: нет

Что не так / что сделать: После t-078 в `artifact-writers.json` появились ключи-пути (`work/test-cases/critic-findings.md`, `work/test-code/critic-findings.md`); реестр читают своей логикой ещё четыре места — `guard_pre_tool.py` ~:880, `contract_slices.py:312`, `artifact_supersede.py:163`, `story_run.py:862`. Проверить, что они видят ключи-пути верно (один читатель реестра — FR-17).

Свидетель: Билдер t-078.

Принципы и правила: FR-17, FR-54

Решение владельца нужно: нет (фраза не найдена)

<!-- piles split: plans/BACKLOG.md, раздел 7 «Релизы, приёмки, инфраструктура разработки»; ячейки строки перенесены дословно -->

Строка BACKLOG.md целиком:

```
| B-176 | После t-078 в `artifact-writers.json` появились ключи-пути (`work/test-cases/critic-findings.md`, `work/test-code/critic-findings.md`); реестр читают своей логикой ещё четыре места — `guard_pre_tool.py` ~:880, `contract_slices.py:312`, `artifact_supersede.py:163`, `story_run.py:862`. Проверить, что они видят ключи-пути верно (один читатель реестра — FR-17). | Билдер t-078. | новое, 30.09 | FR-17, FR-54 |
```

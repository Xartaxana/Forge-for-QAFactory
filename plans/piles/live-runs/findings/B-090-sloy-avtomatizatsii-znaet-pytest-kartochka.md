# Слой автоматизации знает pytest (карточка маркеров, `diff_scope`, `execution_fingerprint`,…

id: B-090 | кучка: `live-runs` | от: PLAN-after-run4 P11.6; PLAN-cost-3x C1; PLAN-cost-and-time F7 | приоритет: — | кандидат наверх: нет

Что не так / что сделать: Слой автоматизации знает pytest (карточка маркеров, `diff_scope`, `execution_fingerprint`, `manifest_from_tests` читает только `@pytest.mark.qa`, маркер зашит в `s5_precheck.py:327`) — вынести за `profiles[].adapter_id` и `config.test_marker`.

Свидетель: Фабрика обязана работать на проектах не на pytest.

Принципы и правила: P2

Решение владельца нужно: нет (фраза не найдена)

<!-- piles split: plans/BACKLOG.md, раздел 6 «Универсальность»; ячейки строки перенесены дословно -->

Строка BACKLOG.md целиком:

```
| B-090 | Слой автоматизации знает pytest (карточка маркеров, `diff_scope`, `execution_fingerprint`, `manifest_from_tests` читает только `@pytest.mark.qa`, маркер зашит в `s5_precheck.py:327`) — вынести за `profiles[].adapter_id` и `config.test_marker`. | Фабрика обязана работать на проектах не на pytest. | PLAN-after-run4 P11.6; PLAN-cost-3x C1; PLAN-cost-and-time F7 | P2 |
```

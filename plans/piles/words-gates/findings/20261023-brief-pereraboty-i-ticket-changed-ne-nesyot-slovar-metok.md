# Бриф `ticket_changed`-починки и доработки S3 не несёт списки меток, хотя тем же ролям тот же словарь недоступен

id: — | кучка: `words-gates` | от: Lead пачки hotfix-12586/1 (dev2), 23.10.2026 | приоритет: П2 | кандидат наверх: нет

Что не так: узел HF1-6 (OH3-14) вложил закрытые списки `grounding_labels` и `requirement_grounding_states` в бриф ОКНА 1 стратега S3
(`brief_pack.s3_labelling_vocabulary_lines`, окно определяет `controller.s3_window_of`; строка в голове брифа, которая не сжимается), потому что
гард `guard_pre_tool.py` запрещает роли читать `handoffs/vocabulary.yaml` плагина. Спека ограничила бриф окном 1. Но стратегу списки нужны и там,
где его запускают снова: диспатч-починка `repair_cause == "ticket_changed"` и доработка S3 после reject размечают и затем планируют заново, а драйвер
даёт им ту же `labelling_lines` (`story_run.s3_strategist_lines`, строки `scripts/story_run.py:7775-7776`), которая теперь будет строиться
через общий помощник (см. находку-хвост HF1-6 для `conductor`). Бриф этих диспатчей списков не несёт: на повторе роль может оказаться там же, где
была в прогоне 12586 (окно разметки «impossible»).

Вопрос Lead из отчёта: «extend `s3_labelling_vocabulary_lines` to `repair_cause == "ticket_changed"` and to S3 reworks?». Второй вопрос из
того же отчёта: окну плана (выход) нужны ли слова — `planning_contract.py:393` проверяет `numerator_labels` по `grounding_labels`, а строка
контракта плана `references/artifact-contract-plan.md:92` называет `vocabulary.grounding_labels` без значений (её правит узел HF1-13 пачки
hotfix-12586/1); бриф выходного окна плана значений не несёт.

Что сделать: свип «каждый диспатч стратега S3 (окно 1, выход, ticket_changed, rework) — список меток в брифе или текст роли даёт значения
словами»; помощник `handoff.grounding_vocabulary_line()` зовут все построители; тест: бриф `ticket_changed` и бриф rework содержат
строку `labels: …; requirement states: …`; окно выхода — решение узла (нужны ли слова плану).

Свидетель: `docs/tasks/handoffs/t-058-hf1-6.md`, «Analogs noticed, not fixed» («QUESTION for the Lead: a `ticket_changed` repair dispatch
and an S3 rework label and then plan, and the driver gives them `labelling_lines` (story_run `s3_strategist_lines`). Their brief still
carries no lists. The spec limits the brief to window 1.»; «Exit (plan) window: `planning_contract.py:393` validates `numerator_labels`
against `grounding_labels` ... Whether the plan-writing role needs the words is a Lead question.»).

Принципы и правила: FR-2, FR-15, FR-38, AR-8, AR-10, AR-13.

Решение владельца нужно: нет.

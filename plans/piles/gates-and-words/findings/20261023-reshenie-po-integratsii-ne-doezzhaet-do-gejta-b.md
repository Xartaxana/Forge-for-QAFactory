# Решение человека по пробелу интеграции не доезжает до гейта B: непривязанный `accept` не связан со строкой S5, слово по `INT-*` не переоткрывает перенесённый accept

id: — | кучка: `gates-and-words` | от: Lead пачки hotfix-12586/1 (dev2), 23.10.2026 | приоритет: П2 | кандидат наверх: нет

Два хвоста узла HF1-9 (GW1-13, пробел интеграции назван на гейте A), оба — в одном читателе: `stand_gaps.py` не знает карточек
интеграции. Чинятся одним механизмом (читатель `environment.integrations[]` в `stand_gaps.py`, ключи ответа — id `INT-*` и имена
ключей), поэтому одна находка.

Что не так (1), спека t-051 §8 Q1: непривязанный к кейсу `accept` на `integration missing: <name>` (вопрос уровня истории, когда
`required_by` нельзя связать с кейсом) не сопоставляется с поздней строкой S5 `blocked_by_env` того же кейса, поэтому гейт B может
спросить про этот кейс ещё раз. Нужно: `stand_gaps.gate_b_answers` (`scripts/stand_gaps.py:732`) и `delivery_decisions`
(`scripts/stand_gaps.py:785`) читают waiver как перенесённое решение с ключом «имена ключей интеграции».

Что не так (2), отчёт t-062 («Questions / findings for the Lead», п. 3): позднее слово по гэпу `INT-*` не переоткрывает перенесённый
`accept` гейта A. Эксперимент билдера (scratch `blind.py`): accept и перенос → гейт B читает `accept`; добавить позже
`INT-jira-integration: theirs` → по-прежнему `('accept', '')`. Причина: `stand_gaps.declared_ids` (`scripts/stand_gaps.py:502`), `_c3`
(`:639`) и `_c5` (`:696`) читают только предусловия, которые объявляют файлы кейсов (`declared_preconditions`,
`scripts/stand_gaps.py:162`); id `INT-*` производит `gate_preflight.integration_gap_ids` (`scripts/gate_preflight.py:106`), и
читателя у них в `stand_gaps.py` нет. Новый `INT`-гэп, появившийся после переноса, так же не считается «новым гэпом стенда» для C5.

Что сделать: `declared_preconditions` (или соседний читатель) возвращает ещё и id интеграций из `environment.integrations[]` через
`integration_gap_ids` — один читатель на оба хода; тест: accept → перенос → позднее слово по `INT-*` открывает вопрос заново;
непривязанный accept закрывает позднюю строку S5 того же кейса и не спрашивает дважды. Производитель и читатели меняются одним
коммитом (AR-22).

Свидетель: `docs/tasks/specs/t-051-hf1-9-gw1-13.md` §8 Q1; `docs/tasks/handoffs/t-062-hf1-9.md` («Questions / findings for the Lead», п. 3;
раздел K-AR3 — звено «untied `accept` → waiver → gate B» не построено).

Принципы и правила: P13, FR-7, FR-9, FR-40, AR-22, AR-24.

Решение владельца нужно: нет.

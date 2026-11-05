# Два скраббера адреса рядом с `http_client.safe_url`

id: — | кучка: `execution-report` | от: билдер CX1-4 (t-1004) по критику t-965 (Q5), 19.10.2026 | приоритет: П3 | кандидат наверх: нет

Что не так / что сделать: CX1-4 пропускает каждый адрес, который печатает `env_probe` (строка вердикта, JSON `url`,
деталь `base_url`), через `http_client.safe_url` (userinfo, query и fragment снимаются) и не вводит четвёртого
скраббера. Остались двойники: `stand_access._safe` (`scripts/stand_access.py:54`) и `stand_health._display`
(`scripts/stand_health.py:402`). Свести к `http_client.safe_url`; различия формы вывода — в тестах своих файлов.

Свидетель: `scripts/stand_access.py:54`, `scripts/stand_health.py:402`, `scripts/http_client.py:151`; критик
`docs/tasks/specs/reviews/t-965-t-958-cx1-4-plan.md` M-2, Q5.

Принципы и правила: P10, P12, FR-17, FR-54.

Решение владельца нужно: нет.

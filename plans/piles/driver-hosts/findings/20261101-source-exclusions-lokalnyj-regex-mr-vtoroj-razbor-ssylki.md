# `source_exclusions.py` держит локальный разбор ссылки MR (`re.search(r"/-/merge_requests/(\d+)", fetch)`) рядом с `VCS_URL_RE` и `ticket_light.classify_url` — ещё одна копия «что такое ссылка MR»

id: — | кучка: `driver-hosts` | от: DUPLICATION критика диффа HF8-5 (`docs/tasks/specs/reviews/r0107-hf8-5-diff-critic.md`, стоячие вопросы и F7: «`source_exclusions.py:550` already holds a local regex: queue row»), `docs/tasks/release-0.10.7.md:196`, 01.11.2026 | приоритет: П3 | кандидат наверх: нет

## Что наблюдалось

В слитом дереве `scripts/source_exclusions.py:565` (в дереве критика :550) разбирает номер MR своим регулярным выражением; рядом `VCS_URL_RE` (`source_inventory.py:3538`), разбор по стилям
в `source_exclusions.py:121` и `ticket_light.classify_url` (данные `reference-kinds.json`) — разное понимание «ссылки MR» (критик показал ложные срабатывания: `https://confluence/display/merge_requests/12`,
`?next=/pull/9`). Копия не в диффе HF8-5, поэтому в очередь.

## Что именно менять

1. Один читатель ссылки MR (вид + номер, по пути URL): `source_exclusions.py:565` и :121 читают его, а не свои выражения (AR-1, AR-13); проверка `5a` из `story_run.py:4123-4124` сохраняется.
2. Тест: те же четыре входа (`/-/merge_requests/5`, `/merge_requests/5a`, `confluence/display/merge_requests/12`, `?next=/pull/9`) дают один ответ у всех потребителей. Мутация: вернуть локальное выражение — красит.

## Принципы и правила

AR-1, AR-13, AR-15; FR-54. Связи: HF8-5, ось 19 карты.

Решение владельца нужно: нет.

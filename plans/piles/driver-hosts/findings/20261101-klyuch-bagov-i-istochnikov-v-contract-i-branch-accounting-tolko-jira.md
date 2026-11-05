# Форма ключа `bug:` и `rest:` держится вне `adapter_forms` и знает только Jira: на github/gitlab/ado `bug:#42` и `rest:#42` отказываются

id: — | кучка: `driver-hosts` | от: обзор MR !12 по требованиям (`docs/tasks/specs/reviews/t-1646-mr12-review-requirements.md`, F-1 MAJOR), 01.11.2026 | приоритет: П2 | кандидат наверх: нет | узел: SS1-16

## Что наблюдалось

- `ai-packages/qa-factory/scripts/contract.py:2589` `BUG_TRACKER_ID_RE = re.compile(r"[A-Z][A-Z0-9]*-\d+")`, его читает `derived_from_legal` (:2592); отказывает `validate_artifacts.py:518` («`bug:` takes a bug id (`bug:BUG-12`)»).
- `ai-packages/qa-factory/scripts/branch_accounting.py:62-63` `KEY_RE` внутри `UNIT_TOKEN_RE` (`rest:{KEY_RE}`) — тот же класс, строки `## Source obligations` шаблона реестра.
- Проба критика (`git archive` пакета, `python -I`, цитата из t-1646): `bug:TP1-123 True | bug:#42 False | bug:42 False | bug:owner/repo#42 False`; `rest:PROJ-1 True | rest:#42 False | rest:42 False | rest:LOCAL-3 True`.
- Единственный читатель формы ключа — `references/adapter-forms.json` через `adapter_forms.is_key` / `form_keys` (его примечание: «the ONE reader; no other script holds a key shape»); он знает ключи github/gitlab/ado как `\d+` / `#123`.

Не проверено: старый код вне диффа MR !12 на ту же форму не обходился (оговорка критика).

## Класс

Форма ключа трекера, живущая вне `adapter_forms`. Слово владельца 31.10.2026: трекер не Jira по определению. Дверь отказа («`bug:BUG-12`») толкает роль придумать ключ формы, которой у этого трекера нет, — дверь, которой роль честно воспользоваться не может (FR-2). Для `rest:#42` остаток одного связанного тикета назвать нельзя, и роль откатывается к `rest` на всю стори.

## Что именно менять

Направление выбрано (Lead пачки, 01.11.2026). Пути — от `ai-packages/qa-factory/`.

1. `scripts/contract.py:BUG_TRACKER_ID_RE` / `derived_from_legal`: убрать регулярное выражение; сегмент после `bug:` проверяется `adapter_forms.is_key(seg, cfg)` (или `KeyForm` стори); фабричный черновой ключ `bug:BUG-n` остаётся отдельной формой — строкой данных в `references/adapter-forms.json` (не списком в коде, AR-1), читается тем же `adapter_forms`. Тест: github-kind конфиг принимает `bug:#42`; jira-kind принимает `bug:ABC-1`; черновой `bug:BUG-12` принят в обоих.
2. `scripts/branch_accounting.py:KEY_RE` / `UNIT_TOKEN_RE`: `rest:<ключ>` проверяется тем же `adapter_forms.is_key(seg, cfg)` вместо `KEY_RE`; жёсткий шаблон `UNIT_TOKEN_RE` разбирает только префикс и сегмент, форму сегмента решает читатель. Тест (`scripts/tests/test_branch_accounting.py`): github-kind принимает `rest:#42`, jira-kind принимает `rest:ABC-1`, оба отказывают `rest:` без ключа.
3. `scripts/validate_artifacts.py:518`: дверь отказа называет форму ключа проекта (пример берётся из `adapter_forms` для вида трекера проекта), а не литерал `bug:BUG-12`; для черновой формы дверь остаётся второй строкой. Тест: текст отказа на github-kind содержит `#`-пример, на jira-kind — `ABC-1`-пример (FR-2).
4. Чек-лист соседей: `git grep` по `scripts/` на `[A-Z][A-Z0-9` вне `adapter_forms.py`; каждая найденная форма ключа — переносится на читатель или получает строку «не ключ трекера — почему» в отчёте узла.

Тест-файлы: `scripts/tests/test_adapter_forms.py`, `scripts/tests/test_branch_accounting.py`, `scripts/tests/test_validate_artifacts_report.py` (имя теста контракта — проверить по коду).

## Связи

- SS1-14 (форма ключа трекера, `adapter_forms.key_form`) и SS1-15 (общие правила чтения трекера) — тот же читатель; общий файл `adapter_forms.py`, `references/adapter-forms.json`.
- Второй MINOR того же обзора (F-2, `fallback_kind: "jira"` как знание, а не догадка) в этот узел не входит.

## Принципы и правила

P2, P10; FR-2, FR-13; AR-1, AR-13, AR-15.

Решение владельца нужно: нет (слово 31.10.2026 «трекер — не Jira по определению» уже дано).

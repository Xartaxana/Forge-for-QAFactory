# Два (и больше) разбора env-файла в пакете читают одну и ту же строку по-разному: бриф называет ключи парсером, а вход читает другим (t-561 Ф-9 c)

id: — | кучка: `onboarding-forge` | от: критик t-561, Ф-9 (в) и Ф-12 (`docs/tasks/specs/reviews/t-561-s4-critic.md`), 31.10.2026 | приоритет: П2 | кандидат наверх: нет

## Что наблюдалось

Читателей формата `KEY=VALUE` три, правила у них разные (все читаны в этом дереве):
- `env_probe.parse_env_file` (`env_probe.py:103`): `utf-8`, без `export `, снимает кавычки `strip('"').strip("'")` (кавычки разных видов вперемешку), ключ `=x` с пустым именем сохраняет.
- `manual_capture._env_values` (`manual_capture.py:533`): `utf-8-sig` (BOM), снимает `export `, пропускает пустое имя, снимает ОДНУ пару одинаковых кавычек.
- `stand_health._env_values` (`stand_health.py:431`): берёт `env_probe.parse_env_file`, но читает только `environment.env_file` — файлы `env_files` (список) игнорирует; `gate_preflight.configured_env_files` (:702) и `env_values` (:718) читают список.
`brief_pack._env_file_key_names` (`brief_pack.py:2239`, после Ф-12 через `configured_env_files`) называет ключи `env_probe.parse_env_file`, а вход, которым пользуется роль, читает `manual_capture._env_values`: строка `export USER_X=…` или файл с BOM
в брифе «нет такого ключа» / ключ с BOM-приставкой, а `--as env:K/S` по нему отказывает. Один факт — несколько читателей (AR-13, ось 126 карты).

## Что именно менять

1. Один разбор: `env_probe.parse_env_file` получает правила `manual_capture._env_values` (BOM, `export `, пустое имя, парные кавычки) и становится единственным; `manual_capture._env_values` вызывает его и добавляет только свой обход «позднейший файл побеждает, пустое не стирает» (`_env_files_state`, :551).
2. `stand_health._env_values` берёт список файлов через `gate_preflight.configured_env_files` (как гейт), не один `env_file`.
3. Запрос Lead на скаута перед узлом (критик t-561: «env_file читают ещё `readiness.py`, `project_inventory.py`, `source_inventory.py` и др. — 12 файлов по grep; кто из них решает, какой файл содержит учётку, мимо `configured_env_files`»): таблица читателей с вердиктом «через общий / нет» — первый шаг узла.
4. Тесты (`scripts/tests/test_env_probe.py` или соседний, `test_manual_actor.py:617` расширить): таблица строк `A=1`, `export A=1`, `A="x"`, `A='x'`, `A="x'`, `=x`, `#c`, BOM-первая строка — один и тот же результат у всех читателей (вызовом каждого); `env_files` из двух файлов видят `stand_health` и `brief_pack`. Мутация: вернуть старый `parse_env_file` — красит BOM и `export`.

## Принципы и правила

P2, P14; FR-17, FR-54; AR-13, AR-15. Связи: OH3-40, `findings/20261031-brief-s5-avtomatora-bez-stroki-uchetki.md`.

Решение владельца нужно: нет.

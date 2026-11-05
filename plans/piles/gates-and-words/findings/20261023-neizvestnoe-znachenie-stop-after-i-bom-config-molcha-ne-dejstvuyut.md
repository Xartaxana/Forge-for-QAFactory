# Неизвестное значение `pipeline.stop_after` молча значит «без остановки», а конфиг с BOM `hooklib.load_config` молча не читает

id: — | кучка: `gates-and-words` | от: Lead пачки hotfix-12586/1 (dev2), 23.10.2026 | приоритет: П2 | кандидат наверх: нет

Что не так (1): значение `pipeline.stop_after`, которого нет в закрытом списке (`"gate_a"` вместо `gate_A`, `true`, число), читается как
«остановки нет», без слова человеку: ничто его не проверяет (`config_contract.py`, `readiness`). Слово человека «остановись после
гейта A» пропадает, и фабрика едет дальше. После HF1-8 (GW1-12) `stop_after` — единственная причина остановки дирижёра после гейта,
значит и единственная, которая молча не срабатывает. Единственный читатель — `controller.stop_after` (`scripts/controller.py:5863`;
закрытый список `STOP_VALUES` — `:5858`, перенесён туда узлом HF1-8).

Что не так (2): `hooklib.load_config` читает конфиг как `utf-8`, а не `utf-8-sig` (`scripts/hooklib.py:620`; соседний `read_json`
читает `utf-8-sig`, `scripts/hooklib.py:532`). Проект, у которого `qa-factory/config.json` записан с BOM, молча теряет `stop_after` — и всё
прочее, что читают через `load_config`. Это одно семейство с (1): значение конфига, которое не удалось прочитать, становится
умолчанием, а не отказом (FR-59, AR-28).

Что сделать: `config_contract`/`readiness` называют неизвестное значение `stop_after` с закрытым списком (FR-1) — предупреждение
в репетиции или чек-листе, не остановка (P1); `load_config` читает через тот же читатель, что `read_json` (одна функция
чтения JSON, AR-13); тест: `"gate_a"` даёт строку с допустимыми значениями; конфиг с BOM читается и даёт тот же результат, что без.

Свидетель: `docs/tasks/handoffs/t-061-hf1-8.md` («Deviations, decisions-for-the-record, findings», F-7: «an unknown `pipeline.stop_after`
value (`"gate_a"`, `true`, ...) means no stop, silently; nothing validates it (`config_contract.py`/readiness). Also a BOM-prefixed
config is not read by `hooklib.load_config` (utf-8, not utf-8-sig)»); строки `hooklib.py` — проверены в дереве пачки 23.10.2026.

Принципы и правила: P1, P3, FR-1, FR-41, FR-59, AR-13, AR-28.

Решение владельца нужно: нет.

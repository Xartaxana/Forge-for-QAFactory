# Хвосты узла «Then-остаток человеку»: номер Then читают два приватных читателя, метка ожидающей находки живёт в двух файлах

id: — | кучка: `execution-probes` | от: Lead пачки hotfix-12586/1 (dev2), 23.10.2026 | приоритет: П3 | кандидат наверх: нет

перенос: hotfix-12586/batch-2 (узел HF2-2 (EP1-13), волна 1; слово владельца 25.10.2026 — срочная пачка; узел здесь закрывается её хэшем)

Два хвоста узла HF1-10 (GW1-14), оба — «одно знание в двух носителях» (AR-13, AR-15); чинятся одним узлом в `contract.py`.

(1) Номер Then строки `then_bindings`. `s5_precheck._then_number` (`scripts/s5_precheck.py:783`) читает его и при списке или словаре
возвращает 0 (раньше `int([4])` валил всю проверку: отчёт t-059, п. 2). Ту же операцию делает `judge_code` своим приватным циклом
(`scripts/judge_code.py:125`, `int(row.get("then") or 0)` внутри собственного `try/except (TypeError, ValueError): continue`). РАСХОЖДЕНИЕ
С ОТЧЁТАМИ: отчёты t-059 (п. 2) и t-067 («Observations for the Lead», п. 2) называют `judge_code.py:125` «unguarded»; в дереве пачки
(проверено 23.10.2026, последний коммит файла `02442ef1`) там уже стоит `try/except` — падения нет. Остаётся дубль читателя: оба места
читают испорченное `then` как «нет номера» (0 / `continue`), и если понадобится иначе (отказ с названием строки вместо тихого пропуска
в `judge_code`, где функция судится по меньшему числу клауз), менять придётся в двух местах.

(2) Метка ожидающей находки `then-remainder-unrecorded-` стоит в двух файлах: `s5_precheck.THEN_REMAINDER_WAITS`
(`scripts/s5_precheck.py:916`, строится из `THEN_REMAINDER_TAG`) и `exit_gate.WAITING_FINDING_TAGS` (`scripts/exit_gate.py:1006`); `exit_gate`
не импортирует `s5_precheck`, поэтому равенство держит только пин в `test_then_remainder.py` (комментарий `exit_gate.py:1005`). Единый
дом — `contract.py` (там уже живёт семейство `THEN_HANDED_MATCH_PREFIX`, `then_remainder_rows`, `then_handed_words`).

Что сделать: в `contract.py` — одна функция «номер Then строки» и одна константа метки; `s5_precheck`, `judge_code`, `exit_gate`
читают их; пин превращается в тест «в `exit_gate` нет литерала метки» (по образцу census-ключей узла HF1-5). Тест: строка с
`then: [4]` читается обоими одинаково; удаление константы из `contract.py` ломает оба потребителя. Как читать испорченное значение
(тихо или отказом) — решение узла, с FR-59 как мерой.

Свидетель: `docs/tasks/handoffs/t-059-hf1-10.md` (п. 2 «Deviations»: «Same unguarded `int(row.get("then") or 0)` stands in
`judge_code.py:125` (not mine, reported)»); `docs/tasks/handoffs/t-067-hf1-10-fix-round.md` («pin: `exit_gate.WAITING_FINDING_TAGS ==
(s5_precheck.THEN_REMAINDER_WAITS,)` (the string lives in two files because `s5_precheck` does not import `exit_gate`; a better single
home is `contract.py`, not owned - report line)»). Номера строк и состояние `judge_code.py:125` — прочитаны в дереве пачки 23.10.2026.

Принципы и правила: FR-14, FR-59, AR-13, AR-15, AR-28.

Решение владельца нужно: нет.

# `test_gate_preflight` красный на `main` (982/983): падение на дороге `story_step.py:1283` → `gate_preflight.s5_profiles` — медленный тест, CI `--fast` его не гоняет, ночной прогон не прочитан

id: — | кучка: `conductor` | от: билдер t-868 (замечено), подтвердил критик t-874 на 18e9e6f9 и далее; записал Lead 16.10.2026 07:5x | приоритет: П1 | кандидат наверх: нет

## Что

`python -B scripts/tests/test_gate_preflight.py` на `main` (18e9e6f9 и позже) — 982/983: один сценарий `s5_profiles`/`story_step`
красный. Дифф C3-8/9 части A `story_step.py`/`gate_preflight.py` не трогает — красный пришёл раньше. `test_gate_preflight.py` стоит в
`scripts/slow_tests.json` (26,6 с), поэтому `selftest --fast` в CI на каждый пуш его пропускает; ловит только ночной `package-full`
(F6-18) — его артефакт за последнюю ночь Lead не читал. Последняя правка `story_step.py:1283` — C2-3 core (t-817 WIP → t-827/t-830).

Что сделать (первый ход — диагноз, не починка): прогнать файл на `main`, прочитать падение, найти слияние, которое его внесло
(`git bisect` по `main` между 4a51d7b3 и 18e9e6f9 с одним этим тестом), записать `defect_found` с `ref` на `accepted` того узла;
затем починка узлом той же кучки (или C2-3 «Остатки»); ночной артефакт `package-full` читать каждое утро (память
`slow-tests-proved-on-ci-image`).

## Куда

Строка C4-2 пачки `conductor/batch-4-vhodyashchie-2.md` (D-0044).

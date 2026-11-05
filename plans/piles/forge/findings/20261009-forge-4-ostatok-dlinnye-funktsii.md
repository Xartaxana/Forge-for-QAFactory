# Остаток класса «длинные функции» после B-426: следующие переростки, контекст-объект для помощников, мерилка `--lines/--depth`, литерал 400 рядом с новой константой, G13-пин регистра

id: — | кучка: `forge` | от: критики t-640/t-648/t-655/t-656, Lead, 09.10 | приоритет: П3 | кандидат наверх: нет

Что не так / что сделать: B-426 закрыл свой список из десяти функций, но у класса (B-419) нет носителя для следующих:
(1) верх CRAP после слияний — `Driver.take_answer` (сложность 95, `story_run.py:8934`; C1-1 добавит в него ветку шва),
`gate_brief.render` (92), `Driver.dispatch_action` (81); в тех же файлах — `publish_binding`, `main`, `plan_mutation`,
`run_shape_checks` (`probe_by_code.py`), `render_text` 97 / `main` 73 (`calibration_counts.py`), `carry_environment_properties`
(глубина 6), другие `check_*` с лестницей `if/elif` по слову состояния (`gate_preflight.py`); (2) списки параметров
помощников после разбиений: `_plan` 14, `_new_record` 15, `_run_and_judge` 10, `_repeat_check` 10 (`probe_by_code.py`),
`_reporter_outcome` 12, `_choose_test` 7 (`gate_preflight.py`), `_card` 8, `_short_line` 6 (`gate_brief.py`), `_relay_note` 7
(`story_run.py`) — узел «контекст-объект»; (3) мерилка длины/вложенности в репозитории отсутствует — спека t-625 M живёт
только во временной папке; обещано (t-625 F-2 (b)): `crap_report --lines/--depth`, переиспользуя его L(f) (:36-38, :113-130),
а не второй счётчик; (4) `gate_preflight.py:2474` `names_only(understood)[:400]` — тот же литерал, что D6 свёл в
`report_adapt.UNDERSTOOD_SHOWN`, и его комментарий «at most 400» противоречит `UNDERSTOOD_LIMIT = 2000 "stored"`; (5) регистр
гейтов: удаление сайта из строки регистра видно только по счётчику `--sites --json` (126) — G13-пин атрибуции сайтов по
образцу K-T1.2 G7 (`test_gate_registry.py:242-250`); при B-283 строка `environment_property_cover` держит R7-вызывающих
(`_card_items` через `_environment_cover`, `_reporter_card`), не помощников сравнения.

Свидетель: `docs/tasks/specs/reviews/t-656-forge-4-integration.md` (F-4, F-5, F-6; `crap_report --top 20`: take_answer 95,
render 92, dispatch_action 81); `t-640-b-426-wave-1.md` (F-3), `t-648-b-426-wave-2a.md` (F-2), `t-655-b-426-wave-2b.md`
(F-1, F-2, F-5); спека `docs/tasks/specs/t-625-b-426-long-functions.md` (M, F-2).

Принципы и правила: правило 18 файла критика (КАЧЕСТВО), `docs/tasks/critic-diff-brief.md` п. 7; FR-28 (мерилка — код с
тестом); FR-17.

Решение владельца нужно: нет.

# Дирижёр — пачка 2: находка из прогона чинится классом — весь список за один ход, слово человека во всех носителях одной дверью, фабрика не спрашивает о невозможном

кучка: `conductor` | статус: закрыта | взял: владелец, 13.10.2026 | ветка: `pile/conductor/batch-2` | MR: `e981cb86` | стенд: нужен | приоритет: П1 | issue: https://git.example.com/dev1/yml-text-factory/-/issues/16

очередь: conductor/1 → conductor/2
очередь: conductor/2 → forge/5

Слово владельца 13.10.2026 (прогон cmp3, три раза): «Мы это чиним сейчас? Во всех похожих местах чиним, а не только в
одном где встретили?» (20:58); «Это слово человек может не сказать, так как и так понятно что фабрика не может сделать
недостижимое. Это само собой разумеещееся. Фабрика не должна обещать или пытаться сделать что-то что заранее понятно что
невозможно» (20:58); «подумай где ещё могут быть ошибки похожие на эти все находки (в других этапах? при других
переходах? у других агентах?) Мы должны чинить весь класс таких проблем, а не одно место где мы поймали прицедент»
(20:58); о прогоне 25: «Вызывается роль только для каких-то бюрократических процедур? Это слишком дорого» (20:20).
Носитель классов — отчёт скаута t-718 `docs/tasks/specs/reports/t-718-class-walk-cmp3.md` (K1–K9, 98 строк-сайтов по
S0–S9, гейтам A/B и дирижёру, матрица «Пересчёт», честный список «Не пройдено»). Пачка открыта 13.10 21:20 параллельно с
хвостом `conductor/1` (C1-5b1, C1-5d2, C1-6…C1-8): узлы по `story_run.py` и `controller.py` идут после узлов C1-5…C1-7
по строке `очередь:`; узлы по `exit_gate.py`, `waiver.py`, детекторам и контроллеру проектируются сразу.

Правило готовности: пачка закрыта, когда каждый узел «принято», свидетели узлов — в журнале взявшего, пакетный
свидетель каждого узла — свои тесты, тесты соседей (из `test_story_run_*.py` только те, что судят узел), `python -B
scripts/selftest.py --limits --lang`, `test_audit_rules.py`, проход по FR (A, B, C, E); живые доказательства (FR-33) —
один прогон на копии cmp3 (TP1-13797) с тем же ответом человека, что в cmp3, записанный в кучку «живые прогоны».

Решения владельца: слово 13.10.2026 20:58 (трижды, выше); D-0039 (P22); D-0025 (слово владельца только от владельца).
Решения Lead пачки (13.10 21:20, технические, «решила сама»): (1) K3 «код закрывает стадию без роли» — отдельный узел
C2-8, не расширение d2 (d2 остаётся в границах t-698 §12–§14); (2) расписка S1 — ФАКТ («снимок лежит», ставит код),
не суждение скаута; сокращение длинной `reason` в механическом третьем возобновлении — усечением с пометкой и путём к
полному тексту, слова роли не переписываются; (3) сверка блока с отказом живёт у ПИСАТЕЛЯ (`waiver.py`) — одна дверь
для драйвера, дирижёра и человека; (4) причина молчания `check_s5_toolchain` в cmp3 (K7) — находка в `stand-and-sources`,
не узел этой пачки; (5) три кандидата cmp3, намеченные ранее как §17 узла C1-5d2 (запасной вопрос несёт слово гейта;
токен несёт исходные слова; блок вне отказа отклоняется), идут узлами C2-7, C2-6, C2-5 этой пачки.
Порядок по общим файлам: `story_run.py`: C2-1 → C2-6 → C2-7 → C2-8 → C2-9 → C2-4 → C2-5 (все — после C1-5…C1-7
`conductor/1`); `controller.py`: C2-2 → C2-3; `gate_preflight.py`: C2-2 → C2-3 → C2-9; `s5_precheck.py`: C2-1 → C2-9;
`ticket_adapter.py`: C2-3 → C2-9; `window_record.py`: C2-3 → C2-4; `no_move.py`, `conductor-actions.json`: C2-3 → C2-6 →
C2-7 → C2-8.
Скоуп свидетеля: C2-1 — `test_exit_gate_scope.py`, `test_exit_gate_grounding.py`, `test_s5_precheck.py`,
`test_check_coverage.py`, `test_handoff.py`; C2-2 — `test_controller_gate_decision.py`, `test_controller_state.py`,
`test_gate_preflight.py`, `test_acceptance_semantics.py`; C2-3 — `test_controller_state.py`, `test_story_step.py`,
`test_window_record.py`, `test_source_preflight.py`, `test_conductor_doors.py`; C2-4 — `test_handoff.py`,
`test_story_run_refusals.py`, `test_window_record.py`; C2-5 — `test_waiver_release.py`, `test_person_word_stages.py`,
`test_no_move_seam.py`; C2-6 — `test_story_run_gate_repair.py`, `test_person_words.py`, `test_no_move_seam.py`; C2-7 —
`test_no_move_seam.py`, `test_story_run_gate_repair.py`, `test_human_questions.py`; C2-8 — `test_no_move_seam.py`,
`test_story_run_s0.py`, `test_story_run_refusals.py`; C2-9 — `test_source_inventory.py`, `test_ticket_adapter.py`,
`test_s5_precheck.py`, `test_story_run_s0.py`; всем — `python -B scripts/selftest.py --limits --lang`,
`test_audit_rules.py`. Интегратор — CI `package-fast`.
Общий бриф дизайнерам: раздел своего класса в отчёте t-718 (определение, таблица сайтов с вердиктами, «Уже закрыто»,
строка класса в «Пересчёте» и в «Не пройдено»); спеки `conductor/1` t-698 (§12–§14 — форма шва `exit_limit`, виды
вопроса, `asked.words_file`) и t-699; `docs/SIBLING_MAP.md` ось 5; PROJECT.md P1, P3, P5, P9, P13, P15, P22; FR-1, FR-7,
FR-8, FR-9, FR-42, FR-48, FR-50, FR-57, FR-59; `references/conductor.md`, `conductor-actions.json`,
`human-questions.md`. Критерий узла: КАЖДЫЙ сайт класса из таблицы t-718 получает в спеке вердикт — «чинится этим
узлом (как)» / «не класс (почему)» / «остаётся: <почему это не место класса>»; сайты «Не пройдено» своего класса
дизайнер проходит чтением и даёт им вердикт; вернуть спеку в `docs/tasks/specs/t-nnn-c2-n.md` с развилками наверх;
номера строк t-718 — на `bf9b4806`, перед правкой сверяются с HEAD.

## Бриф

Что сделать: в cmp3 каждая из девяти находок оказалась классом, а не местом — одна и та же ошибка живёт на нескольких
стадиях и у нескольких агентов. Пачка чинит классы: отказ показывает весь список за один ход (K1); одно решение
человека кладётся во все носители одной дверью кода, роль возобновляется только ради суждения (K2, K9); пропуск с
блоком мимо отказа отклоняется (K4); токен-ответ и запасной вопрос несут слова человека и слова сайта (K5, K6);
закрытие стадии кодом без роли получает ход дирижёра (K3); фабрика не спрашивает о заведомо невозможном и не
переспрашивает по экземпляру (K8).
НЕ делать: не расширять узлы `conductor/1` (d2 — границы t-698 §12–§14; b1 — S5-лимит); не трогать сравнение подстрокой
(четыре открытых id в `gates-and-words`) и возобновления-за-прозу (id в `driver-controller`); K7 (тулчейн на гейте A) —
находка `stand-and-sources`; не чинить экземпляр без таблицы класса.
Первые 10 минут: прочитать карточку («Бриф пачки 2», «Входящие»), преамбулу выше, раздел своего класса в t-718; первый
диспатч — дизайнер узла с вопросом «живы ли строки t-718 на HEAD и какие сайты класса d2/b1 уже закрыли».

## Узлы

Исполнитель «designer → critic на план → builder → critic» — узел меняет гейт или семантику решения; статусы:
`ожидает` → `в работе` → `сдано` → `принято` / `отклонено`.

| Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус |
|---|---|---|---|---|---|---|
| C2-1 | П1 | K1 — читатель вердикта детектора берёт весь список: `exit_gate.detector_errors` (:225, `[-3:]`) и `witness_errors` (:87, `[-4:]`) несут все строки находок (счёт «REJECT — N» + N строк; потолок — по байтам с путём к полному выводу, не по строкам); производители печатают каждую находку одной машинно-считаемой строкой (`s5_precheck.report` :1936, `planning_contract` :1706–1732 — `errors`/`conflicts` не числом, `critic_rollcall` :493, `check_coverage` :239/:285 — REJECT не теряется за WARN в другом потоке, `check_witness` :226); тексты возобновления и `Refusal` в `story_run` (:1593/:1617 `[:8]`, :1629 `[:6]`; `exit_gate` :181/:814/:865 `[:10]`) говорят «N находок» и несут все или путь к полному списку; сайты «Не пройдено» K1 (`no_move.py` options, `conductor.md`, `handoff_check.py`, `acceptance.validate_window`) получают вердикт в спеке | designer → builder → critic | `scripts/exit_gate.py`, `scripts/s5_precheck.py`, `scripts/planning_contract.py`, `scripts/critic_rollcall.py`, `scripts/check_coverage.py`, `scripts/check_witness.py`, `scripts/story_run.py` (тексты `handoff`), `scripts/tests/test_exit_gate_scope.py`, `scripts/tests/test_s5_precheck.py`, `scripts/tests/test_check_coverage.py`, `scripts/tests/test_handoff.py` | conductor/1 C1-5 (`story_run.py`) | принято |
| C2-2 | П1 | K1 — контроллер и гейты отказывают одним списком: `controller.py` `decision` (:3409 `problems[0]`), accept-цепочка S5 (:3251–:3385 — `ValueError`/`StateConflict` на первой неудаче; образец — :3243 «EVERY structural gap at once»), `gate_preflight.py:1280` и `acceptance.py:468` (`problems[0]`) собирают все проблемы в один нумерованный отказ; дирижёр и роль видят список целиком; тест: три дефекта одного окна → один отказ с тремя строками | designer → critic на план → builder → critic | `scripts/controller.py`, `scripts/gate_preflight.py`, `scripts/acceptance.py`, `scripts/tests/test_controller_gate_decision.py`, `scripts/tests/test_controller_state.py`, `scripts/tests/test_gate_preflight.py`, `scripts/tests/test_acceptance_semantics.py` | — | принято |
| C2-3 | П1 | K2 — одно решение человека ложится во все носители одним ходом: «кейс отдан человеку» (S5) пишет одна дверь кода из слов человека сразу в манифест `unresolved[]`, completion `unresolved`+`reason` и запись окна `scope_instances` — для кейсов с инстансами и без (`controller.py:3251–3278, 3364–3385`, `story_step.py:814/:985`, `manifest_put.py`, `window_record.py:487–497`); ход дирижёра «записать решение человека» в `conductor-actions.json` — один ход, все носители (FR-9); `stage_complete: false` без названной работы (`controller.py:3155`) закрывается кодом из слов человека (`finish --unresolved`), не возобновлением роли; расписка S1 — факт, который ставит код (`ticket_adapter.py:2306`), `source_inputs` (`controller.py:2347`; вызовы :1573/:2333/:2380/:3171) читает факт и слово человека (`waiver --stage S1` / `accept-gap --point`) одной дверью; двойная запись S3/S4 (`planning_contract.py:1741`, `gate_preflight.py:1406`) — одна запись, которую читают обе стадии; гейт B «отдано человеку» (три носителя, `check_delivery.mark_handed`) — проверить по коду, что слово ложится во все три | designer → critic на план → builder → critic | `scripts/controller.py`, `scripts/story_step.py`, `scripts/manifest_put.py`, `scripts/window_record.py`, `scripts/source_preflight.py`, `scripts/ticket_adapter.py`, `scripts/planning_contract.py`, `scripts/gate_preflight.py`, `references/conductor-actions.json`, `scripts/tests/test_controller_state.py`, `scripts/tests/test_story_step.py`, `scripts/tests/test_window_record.py`, `scripts/tests/test_source_preflight.py`, `scripts/tests/test_conductor_doors.py` | C2-2 (`controller.py`, `gate_preflight.py`) | принято (ядро, t-721 §L-6; C2-3s — conductor/3 C3-3) |
| C2-4 | П1 | K9 — роль возобновляется только ради суждения: механические поля третьего возобновления (`story_run.py:1607–1627` — сокращение `reason`, путь расписки) правит код через `handoff_check.py --set` (усечение с пометкой и путём к полному тексту; слова роли не переписываются); отказы о форме и расписках в `resume_on_refusal` (:3691/:3706) и расписки `review_receipt_ref` (`window_record.py:930`) — сначала дверь кода, роль — только если осталось суждение; флаг `stage_complete` последнего окна решает код по состоянию окна (`completion_for` :9041; маршрутизация `concerns` — id в `driver-controller`, здесь не чинится); роли S6/S9 («Не пройдено» K9) получают вердикт; измерение: число возобновлений ради записи на копии cmp3 до/после | designer → builder → critic | `scripts/story_run.py` (`handoff`, `resume_on_refusal`), `scripts/handoff_check.py`, `scripts/window_record.py`, `scripts/tests/test_handoff.py`, `scripts/tests/test_story_run_refusals.py`, `scripts/tests/test_window_record.py` | C2-3 (`window_record.py`), conductor/1 C1-5 (`story_run.py`) | принято, слито `e981cb86` 17.10 (t-917 по спеке t-908 §L/§L-2, два раунда; критик t-919 `fit_with_fixes`: F-1 должный ремонт S4 выводится из записей диспатчей на любой дороге — не новый платный критик, F-2 лестница режет только при пустой стороне выхода, F-3 причина называет отклонённые кейсы; `handoff_check --shorten`, двери кода раз на ключ; F-8 (`retro_numbers`) — очередь полного Lead; F-6 критика — conductor/3 C3-27; при слиянии строка базы A27 переехала на `Driver.s4_after_critic`) |
| C2-5 | П1 | K4 — пропуск с блоком, которого нет в стоящем отказе, не записывается: `waiver.py run_stage`/`record_refusals` (:362–:431) сверяет `--block` со строками стоящего отказа (`stage_guard.dispatch_errors` и отказ диспатча) и отказывает, перечисляя стоящие строки как закрытые варианты (FR-1, FR-59); «block lifted» (:206–:230) печатается только при совпадении, иначе «ни одна строка не совпала: …»; ветка `take_seam_answer` без `asked.block` (`story_run.py:9269`) ведёт дирижёра к этому отказу, а не к свободному выбору строки; `s0_file_pass` (:4843, «Не пройдено») получает вердикт; сравнение подстрокой и отозванные слова (четыре открытых id в `gates-and-words`) узел не трогает | designer → critic на план → builder → critic | `scripts/waiver.py`, `scripts/story_run.py` (`take_seam_answer` без блока), `scripts/tests/test_waiver_release.py`, `scripts/tests/test_person_word_stages.py`, `scripts/tests/test_no_move_seam.py` | conductor/1 C1-5 (`story_run.py`) | принято (C2-5s t-835: попытка 1 отклонена критиком t-842, попытка 2 — F1 сырой источник строк, F2 `_DOOR_TAIL` сужен (`waiver.py` открыт), F3 `exit_limit` с `lines`, q4, F6; A27 чистый на слитом дереве, 446/446, 223/223; слияние 16.10 04:3x; очередь F4/F5 → C3-10, двойник `running_stage` → C3-9) |
| C2-6 | П1 | K5 — токен-ответ несёт исходные слова человека кодом: `rework`, `restart` и `go on` с блоком (`story_run.py:9260–9271`) исполняются с `--words-file asked.words_file` / `--reason` из файла ИСХОДНЫХ слов, а не из файла токена; состояние `chosen` (:3345) получает `words`, чтобы `words_note` (:3122) строилась; ход `release_and_restart` в `conductor-actions.json` перестаёт обещать «the new session does not see the words»; d2 A7 (`exit_limit`) — та же точка, узел идёт после неё; тест: токен `rework` на гейте B → `rework --reason` содержит слова человека | designer → builder → critic | `scripts/story_run.py` (`take_seam_answer`, `_no_move`), `references/conductor-actions.json`, `scripts/tests/test_story_run_gate_repair.py`, `scripts/tests/test_person_words.py`, `scripts/tests/test_no_move_seam.py` | conductor/1 C1-5d2 (`exit_limit`, A7) | принято, слито `9fcd3acd` (t-856: два воркера, остаток свежим по D-0038; ветка `t-856-c2-6` 9ddac763, 16.10 07:2x; цепочка зелёная, A27 105/105; критик t-873 `fit_with_fixes` 07:49 — F-1 major: `run_release` без окружения драйвера (ось 15, `controller.py` без `console_io`); фикс-раунд 0523cfad/4a3d0496 → **принято, слито `9fcd3acd`** 16.10 09:04; F-1 переоценён — не живой дефект (hooklib ставит UTF-8), ходы оставлены; остатки F-6 и `exit_round` (ось 5) — строки Lead) |
| C2-7 | П1 | K6 — запасной вопрос несёт слова сайта: запасной гейт-вопрос (`GATE_FALLBACK` :269, `no_move` :3317, `last_resort` :3285) предлагает и читает `approve`/`rework`; ветка `offered` (:10109) отдаёт слова гейта в `gate_approval`/`record_by_code` (:9294/:9435); карточки стенд-пробелов читаются и на запасном вопросе (`take_stand_gap_answers`, :10066); `second_delivery` (:3791) несёт `no delivery`; `cap` (:9342) называет слова сайта или явную строку «остаётся»; сайты K6 2–5 закрывают d2 и b1 — узел их не дублирует, а сверяет после слияния | designer → critic на план → builder → critic | `scripts/story_run.py` (`take_answer`, `fallback_person`, `last_resort`), `scripts/no_move.py`, `scripts/tests/test_no_move_seam.py`, `scripts/tests/test_story_run_gate_repair.py`, `scripts/tests/test_human_questions.py` | C2-6, conductor/1 C1-5b1, C1-5d2 | принято, слито `8f91e7fc` 16.10 19:1x (t-884 → 6e18a5c8 16.10 10:4x: `gate_option_rows` одна таблица, пол, `seam_gate_words` + `keep_earlier`, строка `cap`; `test_driver_layers` 51/52 — шесть строк фикстуры вне owns, три мутации не прогнаны; критик t-891 `fit_with_fixes` 11:00 — F-1 второй ответ теряет первый после одного хода, F-2 хвост в разборе карточек (дефект спеки), F-3 потерянный файл слов молча; попытка 1 отклонена, фикс-раунд (попытка 2) с 11:41; воркер умер на сети 12:06, замена с 15:53 в том же worktree наследует дифф → `081c1dd3` 18:0x: F-1…F-7 с пинами, шесть мутаций, docker зелёный, владелец `shown_gaps` в driver-layers → `driver_conductor`; одна развилка возвращена и решена Lead 18:07 — дорога токена `approve` читает только новый ответ (голова до `EARLIER_ANSWER`), запись целиком; раунд 3 `01dce3dc` 18:5x: `approve_by_option` делит файл по `EARLIER_ANSWER`, пин g27_f2, мутация, docker gate_repair 497/497) → принято, слито `8f91e7fc` 16.10 19:11 (Lead: docker human_questions 301/301, conductor_doors 192/192, no_move_seam 518/518, driver_layers 52/52 на слитом дереве; аналоги билдера → conductor/4 C4-14) |
| C2-8 | П1 | K3 — закрытие стадии кодом без роли получает ход: восемь `stage_done … check=True` (`story_run.py:5935` S0; :6847/:6874/:7058 S6; :7303/:7329 S7; :7745/:7758 S9) и `Refusal` :6741 (S5: все окна приняты, стадия открыта), :7357 (S7 передача), :4004 (code-only без свидетельства) идут через шов видом `code_close` с ходами `story_fact` / `go_on_as_is` / `person_does` / `stop_here` и ценой; «возобновить роль» среди вариантов нет — роли нет; форма — как `exit_limit` d2: один шов, другой вид | designer → builder → critic | `scripts/story_run.py` (закрытия S0/S5/S6/S7/S9), `scripts/no_move.py`, `references/conductor-actions.json`, `scripts/tests/test_no_move_seam.py`, `scripts/tests/test_story_run_s0.py`, `scripts/tests/test_story_run_refusals.py` | conductor/1 C1-5d2, C1-6 (S6–S9) | принято, слито `5266d720` 17.10 (t-907: две попытки под критиком t-914, второй воркер — фикс-раунд; остатки — conductor/3 C3-25) |
| C2-9 | П1 | K8 — фабрика не спрашивает о заведомо невозможном и не переспрашивает по экземпляру: `s1_gap_text` (:2916) и `s1_review_text` (:2994) не предлагают дорогу, недоступность которой фабрика установила сама (`ACCESS_CAUSES`: `host_unreachable`, `no_tool`, `too_large` с вердиктом пробы) — такой источник пишется пробелом по умолчанию и строкой отчёта по имени, вопрос остаётся только там, где человек МОЖЕТ дать дорогу (FR-50 «три ответа» при реальной развилке); запись класса причин `accept-gap --cause <класс>` (`ticket_adapter.py:1967/:2226`, по образцу `environment_record.py`) действует на новые экземпляры класса до конца прогона (:1543/:2525 — вопрос не повторяется, FR-7); S5 «has no obligation binding» (`s5_precheck.py:1550–1558`) проходит по слову одним решением класса (по полному списку C2-1); «Не пройдено» K8 (`EXECUTOR_OPTION_IDS` при `stand_authorized`, гейт B/S9/S6) получают вердикт; формулировка принципа — кандидат наверх (находка `gates-and-words/findings/20261013-fabrika-ne-obeshchaet-nevozmozhnogo.md`; DECISIONS.md / уточнение P5 пишет Lead) | designer → critic на план → builder → critic | `scripts/story_run.py` (тексты S1, `handoff` S1_GAP), `scripts/ticket_adapter.py`, `scripts/source_inventory.py`, `scripts/s5_precheck.py`, `scripts/gate_preflight.py` (`executor_question`), `scripts/tests/test_source_inventory.py`, `scripts/tests/test_ticket_adapter.py`, `scripts/tests/test_s5_precheck.py`, `scripts/tests/test_story_run_s0.py` | C2-1 (`s5_precheck.py`), C2-3 (`ticket_adapter.py`, `gate_preflight.py`), conductor/1 C1-3 (тексты S1) | принято, слито `34ba8367` 17.10 (t-906: три воркера — бюджетная остановка, остаток, фикс-раунд под критиком t-916; остатки — conductor/3 C3-26) |

## Ход

- 16.10 19:11 — C2-7 принят и слит (`8f91e7fc`; t-884: попытка 1 отклонена по критику t-891, фикс-раунд и раунд 3 в одном worktree двумя воркерами — первый умер на сети; развилка дороги токена решена Lead 18:07). `story_run.py` свободен. Следующий на SR: C2-8 (своя спека — дизайнер первым; не в этом окне лимита). Аналоги билдера → conductor/4 C4-14.
- 16.10 04:3x — C2-5s принят и слит (t-835: попытка 1 отклонена критиком t-842 по D-0046, попытка 2 свежим воркером в том же
  worktree — F1/F2/F3/q4/F6 по t-722 §L-8; `waiver.py` открыт узлу; A27 на слитом дереве чистый, 105/105 без новых сайтов).
  Строки Lead: `design/state-exits.md` — запись `state/standing-refusal.json`; SIBLING_MAP ось 8 (запись) и ось 17
  (`refusal_lines` в Consumers). Очередь: F4/F5 t-842 → C3-10, двойник `running_stage` → C3-9. Следующий на SR: C2-6 (t-722).
- 13.10 21:20 — пачка собрана Lead по отчёту скаута t-718 (обход классов K1–K9 по S0–S9, гейтам и дирижёру; принят по следу, три точечные проверки) и слову владельца 13.10 20:58; открыта параллельно с хвостом `conductor/1` (строка `очередь:`), четыре развилки скаута решены в преамбуле.
- 13.10 21:51 — пачка взята (`ef34acb8`); дизайнеры t-720 (C2-1/2), t-721 (C2-3/4), t-722 (C2-5/6/7) запущены 21:31.
  **t-722 принята** (`docs/tasks/specs/t-722-c2-5-6-7-words.md`, 38 сайтов, 11 развилок решены в §L: F-6a (b) — вариант
  `rework` несёт `args`, исполняет код). Дополнение owns C2-7 (F-7d): `references/conductor-actions.json`,
  `scripts/tests/test_conductor_doors.py` (ячейка узла заморожена — здесь). Дальше — один критик на план по всей спеке.
- 13.10 22:00 — **t-720 (C2-1/2) и t-721 (C2-3/4) приняты** (`docs/tasks/specs/t-720-c2-1-2-whole-list.md`, 29 сайтов,
  10 развилок в §L; `t-721-c2-3-4-one-door.md`, 35 сайтов, 13 развилок в §L). Дополнения owns (ячейки заморожены):
  C2-1 + `scripts/detector_verdict.py` (new), `scripts/tests/test_detector_verdict.py` (new), `scripts/audit_factory.py`,
  `scripts/check_delivery.py`, находка `findings/` (new); C2-2 + `scripts/tests/test_controller_blocks.py`,
  `tools/controller-blocks-gen.py`, `design/controller-blocks.md`; C2-3 + `scripts/source_inventory.py`,
  `references/conductor.md`, `scripts/guard_pre_tool.py`, тесты по §8 t-721; C2-5 получает пункт очереди из t-721 F-8
  (`waiver --stage S1` по строке источника — отказ писателя). Критики на план: t-724 (t-722), далее t-720 и t-721.
- 13.10 22:36 — критики на план: t-724 (t-722) reject, t-726 (t-720) и t-727 (t-721) fit_with_fixes — вердикты в
  `docs/tasks/specs/reviews/`; переработки дизайнерами t-728 (t-722, принята: §11 закрывает 15 находок, §L-3 решает 7
  развилок), t-730 (t-721), t-731 (t-720). Дополнения owns по §L-3 t-722 и решениям t-727: C2-5 + `skills/qa-story/SKILL.md`,
  `references/conductor.md`, `scripts/tests/test_gate_vocabulary.py`; C2-6 + `scripts/no_move.py`, `references/conductor.md`,
  `scripts/tests/test_conductor_doors.py`; C2-4 + `scripts/retro_numbers.py`, `scripts/tests/test_retro_numbers.py`,
  `scripts/handoff.py`. Очереди внутри пачки: `conductor.md`: C2-5 → C2-6 → C2-3; `test_conductor_doors.py`: C2-2 → C2-3 →
  C2-6 → C2-7; `waiver.py`: C2-5 → C2-3. b1 (`conductor/1`): фикс-раунд t-729 остановлен бюджетом, остаток — t-732.
- 13.10 22:37 — **t-730 (переработка t-721) принята**: §10 закрывает 15 находок t-727, 7 развилок решены в §L-2 t-721;
  очередь внутри пачки `scripts/tests/test_handoff.py`: C2-1 → C2-4. Критики по диффам переработок t-722 и t-721 — следующее
  окно; t-731 (переработка t-720) в работе.
- 13.10 22:41 — **t-731 (переработка t-720) принята**: §10 закрывает 12 находок t-726, 39 сайтов (10 новых), 6 развилок
  решены в §L-2 t-720 (`*` проходит всё, именованное слово — только то, что пропускает производитель). Порядок внутри
  пачки: C2-1 вливается раньше C2-2. Все три спеки conductor/2 переработаны; критики по диффам — следующее окно.
- 13.10 23:38 — три критика только по диффам переработок запущены параллельно: t-734 (t-722, `2451e5cc..c31c4c57`, 15 находок
  t-724), t-735 (t-721, `7e4cb85e..c31c4c57`, 15 находок t-727), t-736 (t-720, `7e4cb85e..c31c4c57`, 12 находок t-726);
  каждый пишет вердикт сам файлом `docs/tasks/specs/reviews/t-73N-<спека>-rework.md` (агент типа builder с моделью opus —
  форма до узла F5-1 кучки `forge`). После вердиктов: дизайнеры C2-8/C2-9, билдеры C2-2 и C2-5 первыми.
- 13.10 23:52 — **три вердикта по диффам: все `fit_with_fixes`**, файлы `reviews/t-734-t-722-rework.md` (14/15 закрыто,
  открыт id 2 — тело отстаёт от §L-3 F-7e; must-fix N1 блок `go on` целой строкой не находит носителя, N2 запись `seam_rework`
  удаляется до регистрации, N9 цикл очередей), `t-735-t-721-rework.md` (13/15; id 1 F-14 и id 3 F-19 — тело отстаёт;
  конфликт §L F-5 (a) ↔ §L-2 F-19), `t-736-t-720-rework.md` (10/12; id 1 F-11 тело и три края, id 3 транспорт составного
  отказа: префикс `story_step: refused - ` и JSON-экранирование). Решения Lead — §L-3 t-721 (исполнитель `open` — дверь C2-3,
  она пишет запись `seam_rework`, исполняет шаг цикла C2-6), §L-4 t-722, §L-3 t-720 (один нормализатор транспорта,
  `unmigrated` только `*`, `predating` первым). **Поправка очередей (N9)**, один ациклический порядок на файл:
  `story_run.py`: C2-1 → C2-5 → C2-6 → C2-7 → C2-8 → C2-9 → C2-4 → C2-3; `conductor.md`: C2-5 → C2-6 → C2-3; `waiver.py`:
  C2-5 → C2-6 → C2-3; owns C2-6 + `scripts/waiver.py`, `scripts/tests/test_waiver_release.py`. Поправка строки 23:38
  (F-15): первыми C2-1 и C2-5 параллельно, C2-2 после слияния C2-1. Фикс-раунды свежими дизайнерами: t-737 (t-721),
  t-738 (t-722), t-739 (t-720); второго прохода критика нет (D-0035 (b)).
- 14.10 07:15 — **фикс-раунды 1 приняты**, каждый вернул вопросы (развилки, не решения — как и положено дизайнеру): t-737
  → §L-4 t-721 (носитель решения `open` — файл решения, запись `seam_rework` создаёт драйвер после принятия D; `cause
  open_work`; `words_file_path` в `person_words.py`; **порядок слияния: C2-6 раньше C2-3 на всех файлах, C2-3 раньше C2-4**
  — `story_run.py`: C2-1 → C2-5 → C2-6 → C2-7 → C2-8 → C2-9 → C2-3 → C2-4; `no_move.py`: C2-6 → C2-7 → C2-3;
  `conductor-actions.json`: C2-6 → C2-3; `test_conductor_doors.py`: C2-2 → C2-6 → C2-7 → C2-3); t-739 → §L-4 t-720 (тег в
  заголовке; машинный тег `WORDS_REFUSED_AT_SOURCE: <id> <cause>` выше `*`; исключение `*` в S5P не меняется); t-738 →
  §L-5 t-722 (ответ `chosen` — `ask_person` с одним вариантом; `purpose` как у `ticket_rework`, `complete=False`; owns C2-5
  + `story_step.py` строка `MODE_SWITCH`, очередь `story_step.py`: C2-2 → C2-5; owns C2-3 + `person_words.py`,
  `test_person_words*.py`). Фикс-раунды 2: t-741 (t-721), t-742 (t-720), t-743 (t-722). Машина спала 00:35–07:10: сторож
  снял t-733 (остаток b1) и скаута t-740 — перезапущены заменой работника.
- 14.10 07:46 — **фикс-раунды 2 приняты** (t-742 → §L-5 t-720, t-743 → §L-6 t-722 — 07:24; t-741 → §L-5 t-721): все три
  спеки закрыты для билдеров. §L-5 t-721: `cause` записи `open_work` = `test_defect`, `cases` = `unresolved` на S4+;
  отметка драйвера `open_work_taken`; `words_file_path` даёт основу имени, метку и `-<n>` добавляет `write_words` (имена
  файлов слов не меняются). **Поправка порядков**: owns C2-3 не содержат `no_move.py` и `waiver.py` — `no_move.py`:
  C2-6 → C2-7 → C2-8; `waiver.py`: C2-5 → C2-6 (строки 07:15 и t-722 §L-6 (в) читаются так). Owns C2-3 +
  `scripts/story_run.py` (две правки: запись `open_work` перед шагом C2-6, обёртка `Driver.words_file`) и
  `scripts/tests/test_story_run_open_work.py` (new); очередь `test_person_words.py`: C2-6 → C2-3. Дальше — дизайнеры C2-8,
  C2-9; билдеры C2-1 и C2-5 первыми.
- 14.10 08:52 — **C2-8: спека t-745 (черновик, 7 развилок) → критик на план t-751 — `rework`** (2 блокера: S0 помечен
  `done` до `stage_done` SR:5918–5923, строка `s0_receipt` SR:190 перехватывает дверь раньше шва; инвариант I3 несовместим
  с M1/M3). Пересмотр формы шва — решение Lead в §L t-745 после компакта; до него — один замер (сайт 8: S9 numbers mode,
  managed story — не кончается ли уже `funnel`); затем свежий дизайнер, попытка 2. По фактам критика: F-2 (a), F-4 (b),
  F-5 (a), F-7 (a). Находка t-745 §2.3 против C2-5 — наполовину (M8): держится для `no accepted controller stage` и `gate
  rehearsal` — в диспатч билдера C2-5. **C2-9**: дизайнер t-752 идёт.
- 14.10 09:32 — **C2-9: спека t-752 (черновик, 16 развилок) → критик на план t-756 — `fit_with_fixes`** (5 обязательных
  правок: носитель id источников для `record_gaps` — `asked` не несёт списка SRC, регулярное выражение возвращает пусто;
  `--revoke` после закрытия S1 блокирует поздние диспатчи C:2362–2364; `driver-layers.json`/`test_driver_layers.py` в owns;
  закрытые классом источники доходят до читателей без слов человека SS:799/GB:340; близнецы K8 в `mr-access-routes.md`,
  `s1.md`, `qa-scout.md`). По фактам: **F-0 — петля есть, порядок C2-3 → C2-9 → C2-4 на всех файлах** (строка
  `source_inventory.py` C2-3 → C2-9 — в «Ход» при §L); §3.5 (S5-блок класса) — отдельный узел после d2 (N7). F-1 (только
  `too_large`), F-5 (какой «отчёт»), F-10 — решения Lead в §L t-752 после компакта; затем свежий дизайнер, попытка 2.
- 14.10 23:45 — **§L t-752 (C2-9) и §L t-745 (C2-8) написаны**, обе попытки 1 — `rejected` (basis critic), попытка 2 — свежие
  дизайнеры своим типом (t-752 attempt 2 идёт; t-745 — после замера сайта 8 t-765). **C2-3 разделён** (t-721 §L-6): C2-3
  (ядро, без `story_run.py`, CA, `conductor.md`) идёт сразу после C2-2 — дверь `decide --hand` снимает блокер гейта B; C2-3s
  (шов и слова + ключ `code_close.role_open`) — узел C3-3 пачки 3. §3.5 t-752 (S5-блок класса) — узел C3-4 (C2-10).
  **Порядки**: `story_run.py`: C1-5d2 → C2-1 → C2-5 → C2-6 → C2-7 → C2-8 → C3-3 → C2-9 → C2-4; `no_move.py`: C2-6 → C2-7 →
  C2-8 → C3-3; `conductor-actions.json`: C2-6 → C3-3; `conductor.md`: C2-5 → C2-6 → C3-3; `test_conductor_doors.py`: C2-2 →
  C2-3 → C2-6 → C2-7 → C2-8; `test_person_words.py`: C2-3 → C2-6; `story_step.py`: C2-2 → C2-3 → C2-5 → C2-9;
  `question-prices.json`: C1-5d2 → C2-8 → C3-3 → C2-9; `source_inventory.py`: C2-3 → C2-9; `driver-layers.json`,
  `test_driver_layers.py`: C1-5d2 → C2-8 → C2-9. Владельцу подсвечено: «строка отчёта по имени» (D-0043) прочитана как пакет
  гейта A в C2-9 + финальный отчёт узлом `report-delivery`. Билдер d2 (t-764) запущен; C2-1 — следующим (часть §3.4 по
  `story_run.py` — после слияния d2, малым раундом), затем C2-5, C2-2 после слияния C2-1, C2-3 после C2-2.
- 15.10 01:42 — **C2-1 (t-766) сдан** (детекторы и `exit_gate` на одном читателе `detector_verdict.py`, теги S5P, контракт-тест;
  §3.4 по `story_run.py` — отложено в C2-1s после d2) → критик t-772 `fit_with_fixes` (M1: пропуск `state/findings/` в
  `_identity` без теста; m1, m3, m5, m7, m8 — в фикс-раунд свежим воркером; m2, m4, m6, m9 — очередь). **Порядок (решение Lead по
  строке критика F-15)**: C2-2 ВЛИВАЕТСЯ после C2-1s (составная голова отказа безопасна только за `route_known`), билдер C2-2
  может начать раньше. Объединённый SR-раунд после слияния d2: C2-1s (§3.4 t-720) + C2-5s (§3.4 t-722, имена констант).
  C2-5 (t-768) — в работе. d2: первый воркер встал по бюджету (~375K), остаток — свежий воркер в том же worktree (t-764,
  замена). F5-3 слит (`6b84e468`): детектор (е) теперь красный на находке без строки пачки.
- 15.10 04:27 — **C2-1 слит** (`eac4ddc7`, без `story_run.py`; ось 17 карты); **C2-5 слит** (писатель K4 без `story_run.py`:
  t-768 → форк §L-7 → фикс t-776 → критик t-782 `fit_with_fixes` → второй отказ на уровне билдера → эскалация по правилу 6,
  фикс t-785 на Opus); **C2-2 принят** (t-779, критик t-786, фикс t-791 с §L-6 — расписки во всех ярусах), слияние — после
  C2-1s (F-15); **C2-1s (t-790) идёт** — голова очереди `story_run.py` после слияния d2 (`fabe133c`). Дальше: слияние C2-2 →
  C2-3 (ядро; снимает блокер гейта B) и C2-5s (носитель стоящего отказа в `no_move`, `refusal_lines` через читатель C2-1,
  стиратели, кросс-узловой пин с `go on` d2 — очередь t-778/t-782); C2-6, C2-7, C2-8, C2-9 — билдеры по порядку SR.
- 15.10 09:10 — **C2-1s слит** (t-790, критик t-806 `fit_with_fixes` → фикс-раунд t-809; ветка `worktree-agent-a2acaf9f13f3282ac`,
  38377e5a…4c599e9f): тексты возобновления/третьего хода/`Refusal` несут `N finding(s)` и каждую строку через
  `detector_verdict.render` (`-handoff/-filled/-collected.txt`), сухой прогон не обещает файла (`Driver.listed` → `(text, cut,
  clause)`), ветви S1 — `Driver.s1_person`, вызываются и после пересчёта лестницы; `route_known` поверх `match_known` для
  списочных отказов; свидетель мутаций — `scripts/tests/mutate_once.py` + спека `fixtures/mutations-c2-1s-fix-round.json`.
  Узел C2-1 — «принято» целиком. Остаток Lead: абсолютный путь указателя в тексте (`detector_verdict.render`, ось 8) → C3-9.
  Следом — слияние C2-2.
- 15.10 09:20 — **C2-2 слит** (t-779, критик t-786 → фикс-раунд t-791 с §L-6; ветка `worktree-agent-ab5ed69a259c86689`,
  c8876eaf…4744918b): `Controller._raise_all` — один отказ на все независимые дефекты (`decision`, завершение S5 ярусами,
  расписки код-ревью первыми в каждом ярусе), GP/ACC без среза `[:8]`, карта блоков 227 (генератор читает пары
  `(класс, сообщение)`). Строки Lead: ось 17 (продюсер `_raise_all`, тексты SR), фрагмент changelog (расписки), C3-11
  (остальные цепочки одиночного `raise`). Очередь `story_run.py` свободна: дальше C1-5b2 (S7), C2-3 (ядро, без SR, после
  C2-2 на `controller.py`/`gate_preflight.py`), фикс F5-7 (фикстуры поверх C2-2) — параллельно.
- 15.10 16:40 — **C2-3 (ядро) слит, «принято»** (t-817: воркер 1 — код, остановлен бюджетом; воркер 2 — тесты и мутации
  (`replaces_worker`); критик t-826 `fit_with_fixes` (0 блокеров) → фикс-раунд t-827; ветка `worktree-agent-a8dd354e6686f5792`,
  fc07dfd6…9d7c1ab4): дверь `story_step.py decide --hand|--open|--close` (слова файлом, пять шагов, запись решения
  `state/decisions/<D>.json`, один читатель `_decision_of`), пара completion для кейсов без инстансов (`_derived_pair`, стражи
  SS:1018/SS:858, дописка к паре вызывающего по §L-2 F-14/§L-3 N1/§L-7), расписка S1 кодом (штамп в `update_inventory`, одна
  сводка `source_inputs`), одна запись S3/S4 (`missing_branch_line`), гейт B через `handed_records` (T12), `person_words.write_words`
  — один писатель `state/words/`, `decide` в двери гарда; `window_record` на правиле контроллера (точные ключи). Остатки критика:
  F4/F7/F9/F10/F11 и аналоги (профильная фикстура `_hand_detail`, вынос дверных тестов в `test_story_decide.py`) → conductor/3
  C3-13; F12 → C3-12. Очереди: `story_run.py` C2-3 → C1-5b2 → C2-3s; `test_conductor_doors.py` C2-3 → C1-5b2; `controller.py`
  C2-3 → F5-11 → C3-12. Живое доказательство гейта B (C3-1) теперь возможно.
- 17.10 00:xx–13:3x — окно без Fable (Opus-координатор, слово владельца «доводи до закрытия обе пачки дирижёра»): C2-8 `5266d720`,
  C2-9 `34ba8367`, C2-4 `e981cb86` слиты; все узлы приняты, остатки — строками непринятой conductor/3 (C3-21…C3-27, D-0044).
  `main` был красным 2 ч после C2-9 (перепись K3 `test_runtime_paths`, `size_limit_of`) — починка `ce88a813`. Закрытие ждёт
  решения владельца по строке «Живых доказательств» (прогон на копии cmp3): прогнать или перенести с подтверждением.

## Живые доказательства

| Что | Стенд / проект | Кто | Статус |
|---|---|---|---|
| один прогон на копии cmp3 (TP1-13797): S1 без вопросов о недостижимом (K8), отказ `s5_precheck` одним списком (K1), «отдано человеку» одним ходом (K2/K9), `waiver --block` мимо отказа отклонён (K4), токен `rework` на гейте B уносит слова человека (K5) | копия `testproject1-dev-fresh`, стенд | — | перенос: live-runs/findings/20261017-conductor-2-zhivoe-dokazatelstvo-cmp3.md \| обоснование: все узлы слиты и доказаны пинами, прогон на стенде — отдельная работа пачки живых прогонов (строка LR1-8) \| подтвердил: владелец, 17.10.2026 |

## Остатки


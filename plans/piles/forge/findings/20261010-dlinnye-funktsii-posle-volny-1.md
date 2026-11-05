# Длинные функции и глубокая вложенность, оставшиеся после волны 1 остатка t-667 (мерилка `crap_report --lines --depth`)

id: — | кучка: `forge` | от: билдеры t-680/t-682/t-683, критик t-686 (Q8), Lead, 10.10 | приоритет: П3 | кандидат наверх: нет

Что не так / что сделать: по решению t-667 §9 F-2 (a) узлы волны 1 резали только список находки; всё остальное выше 60
строк или глубже 3 в тронутых файлах, по новой мерилке, — здесь, одним списком (lines/depth):
`tools/calibration_counts.py`: `load_journal` 16/4. `scripts/probe_by_code.py`: `lex` 63/3, `_probe` 69/2 (дальнейший разрез
двигает последовательность замка R9, которую A8 держит рядом), `_judge_run` 48/4, `_imported_modules` 16/4, `_statements`
12/5, `put_back` 20/4. `scripts/gate_brief.py`: `render_gate_b` 109, `contradiction_questions` 63, `question_effects` 44/5,
`packet_items` 25/4, `story_cases` 27/4, `open_debts` 23/4, `undrafted_discrepancies` 19/4, `_first` 10/5, `selftest` 90.
`scripts/gate_preflight.py`: `check_bug_drafts` 95, `parse_preconditions` 78, `_rehearse_reporter` 75, `check_s5_credentials`
67, `_check_one_precondition` 64, `check_cases` 61, `_loaded_env_files` 39/4, `collect_command` 24/4, `_stray_env_file`
глубина 6, `selftest` 82. Литералы 400 вне D10: GP `[-400:]` в `_reporter_gap_row`, `"; ".join(broken)[:400]` в тексте
стенда, GP:3215, SR:5676, SR:7298. Соседи по классу «контекст-объект»: `_answer_words` (5 параметров, `forms` и `word_of`
порознь). Мелочь из t-686: `_put_fragment` имеет двойников red_sandbox.py:1362 и window_record.py:943; `_probe_verdict`
запускает подпроцесс, а имя этого не говорит; `scripts = Path(rp.__file__)...` считается дважды (`_probe_no_container`,
`_probe_argvs`); test_reporter_rehearsal.py:1880/1889 возвращает `sys.modules["report_adapt"] = held` и при `held is None`;
crap_report.py:11 в докстринге потерян пробел (`--repo PATH`); указатель B-283: BACKLOG.md:232 описывает гейт
`reporter_rehearsal_identity`, а `debt_ref` в gate-registry.json:522 ждёт переноса вызывающих R7 — план, которого нет
(строка в B-283 или новая находка). Узел N-C (`take_answer`, `dispatch_action`, `carry_environment_properties`, `RelayCtx`)
идёт после C1-4b и ДО C1-5/C1-6/C1-7 (t-667 §10). Правило для любого билдера, трогающего регистр (t-686 Q10): пин D13
ключуется по именам функций — перенос тела без сравнений пин не трогает; перенос/переименование/добавление учтённого
сравнения — красный по замыслу, и тот же коммит правит `sites` строки в gate-registry.json, `D13_TRIPLES`, `D13_ITEM_COUNT`
и прикладывает `--sites --json` до/после.

Дополнение по вердикту t-689 (C1-3 узел B, 10.10): `scripts/story_run.py` — `s0_read_word` 70 → 83 строк, `s0_criteria` 77 → 86,
`s0` 158 → 168 (выросли на узле B; кандидаты N-C или отдельного узла). Аналоги вне носителя (t-689 Q-b, t-684 F6): «run the
same command again» в тексте человеку — source_inventory.py:432/:764/:776 и story_run.py:782 (один помощник «повтори
команду» или замена на дверь); копии однострочника слов вердикта SR:2412/:3234/:3311; `build-identity-methods.json:189`
(собственный текст «held on stop» вне `stop_held()`).

Дополнение по вердикту t-696 (N-C, 13.10): список билдера по Q9 пропустил 14 строк `story_run.py` длиннее 60 строк (мера —
`python tools/crap_report.py --paths ai-packages/qa-factory/scripts/story_run.py --top 400 --lines --depth`, перемеряно в worktree
t-697: 393 функции, 33 строки с длиной > 60 или глубиной > 3 — число критика совпало): `assemble_digest` 78, `take_build_answer` 75,
`package_check` 82, `s0_ticket_read_question` 86, `s0_read_word` 73, `stage_S5` 88, `run_role` 74, `take_question_answer` 69,
`conductor` 74, `take_stand_gap_answers` 75, `question_threshold` 61, `gate_text` 77, `s0_criteria` 74, `__init__` 64. Очередь критика
(каждый пункт — отдельный узел, не правка N-C): (1) близнецы stand / stand-login (SR:10236-10241 и :10271-10275) передают слова
человека через `--decision said` и при неудавшемся waiver только печатают, а `take_question_answer` (:2217-2221) и
`take_seam_answer` (:9261-9265) — через `--words-file` и `raise held_question`; нужен один общий помощник, отдельным узлом;
(2) имя `_unread_kept_gate` не отражает, что оно же обслуживает ответы conductor и refusal; (3) `_relay_note` не использует `self`
(сделать `@staticmethod`); (4) дешёвый пин «`Driver.gate` всегда поднимает исключение» (E10 после M2); (5) область переписи в
test_story_run_refusals.py:449-456 (`handled = ...`) — весь файл, а не тело `dispatch_action`; пин самих семи видов сужен до тела в t-697 F1.

Свидетель: отчёты t-680 (`load_journal`), t-682 (шесть имён), t-683 (список) и вердикт t-686 Q6/Q8 (семь функций глубины ≥ 4,
пропущенных t-683; измерено `crap_report --lines --depth` на обоих worktree).

Принципы и правила: FR-54, правило 9 CLAUDE.md, t-625 S6 (≤ 60 / ≤ 3).

Решение владельца нужно: нет.

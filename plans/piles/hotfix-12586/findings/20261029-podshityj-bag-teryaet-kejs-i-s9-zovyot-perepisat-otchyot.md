# Подшитый баг теряет связь с кейсом, и закрытие S9 требует переоткрыть S8 после выпущенного MR

id: — | кучка: `hotfix-12586` | от: прогон TP1-12586 на 0.10.5, `testproject1-dev-010`, 29.10.2026 (владелец: «в самом конце фабрика словила ошибку. Посмотри почему она хотела переоткрывать S8») | приоритет: П1 (0.10.7, решение Lead) | кандидат наверх: нет

## Что наблюдалось

Транскрипт дирижёра `c8b73507-….jsonl`, 17:57–18:00 UTC; `state/events.jsonl`:

1. 18:28 гейт B: «Bug 1: это баг. deliver with known gaps. MR открывай как драфт». 18:31 `qa-bug-reporter` пишет `bugs/BUG-1.md`
   (`confirmation: confirmed_by_person`, `source_draft: work/bug-drafts/ms-teams-move-project-mismatch.json`). 18:44 MR !833 (Draft) открыт
   с отчётом, собранным на S8.
2. 18:57 `story_step finish` S9, затем `stage_done --stage S9` отказывают: «test-report.md: the appendix row `R-6 · TC-004 · Then 1–3` reads
   `ms-teams-move-project-mismatch unconfirmed`, but the trace the run records gives now reads `blocked` (red run, triaged APP_BUG: no reason
   recorded; bug not filed) … the scribe pastes it again (`story_step.py start … --stage S8 --role qa-doc-scribe`)». То же для R-7.
3. Дирижёр спросил владельца «waiver или переоткрыть S8»; владелец дал слово; `waiver.py` дважды ответил «no refusal of S9 is known to this
   command … cannot say the block is lifted» (пришлось подбирать `--block` второй раз), затем S9 закрыт.

## Почему

1. **Новая трасса неверна, а не отчёт устарел.** `traceability.story_bug_records` (`traceability.py:205-221`): когда у бага есть подшитый
   `.md`, кейсы и требования читаются ТОЛЬКО из его шапки; черновик (`"case": "TC-004"`, `"cases": ["TC-004","TC-005"]`) отбрасывается.
   Шапка `BUG-1.md` несёт `found_by: <имя теста>` и `violates: requirement:R-6`, но не id кейса → `cases = []` → `bug_for` (`:474`) не
   находит бага у TC-004 → строка «bug not filed». Проверено вызовом `bug_records.story_bugs` на стенде: у слитой записи BUG-1 нет полей
   `cases`/`requirements`; `traceability.py --render` сейчас печатает для R-6/R-7/R-11 «blocked … bug not filed» при подшитом BUG-1.
   До подшивки (черновик один) приложение было верным (`ms-teams-move-project-mismatch unconfirmed`).
2. **Шапку баг-файла никто не задаёт.** У `qa-bug-reporter` нет контракта выхода (B-183, HF8-21) — поля шапки, которые читает трасса,
   не названы роли до работы (FR-38, FR-11).
3. **Проверка S9 зовёт не ту дверь.** Отчёт после гейта B меняется законно (баг подтверждён и подшит, MR открыт), но сверка отчёта с
   трассой на S9 предлагает роли переписать приложение через переоткрытие S8 — после выпущенного MR, то есть откат стадии ради блока,
   которым владеет код (`report_facts.py --write`, `traceability.py --close-gate-b`). Человека спросили о том, что код должен был сделать
   сам (FR-3, P22: спрашивать только то, что знает человек).
4. **`waiver.py` не видит отказа `stage_done`** без драйвера: слово записано, но «cannot say the block is lifted»; `--block` подбирается
   по тексту отказа вручную.

## Что нужно

1. `story_bug_records`: кейсы и требования подшитого бага — объединение шапки `.md` и его `source_draft`; пустой результат при непустом
   черновике — дефект читателя, а не «bug not filed».
2. Контракт выхода баг-репортёра (HF8-21) называет поля шапки: `case`/`cases`, `requirements`, `source_draft`; `handoff_check` их требует.
3. После гейта B блоки отчёта, которыми владеет код, перестраивает код (`report_facts --write` после подшивки багов, до MR), а сверка S9
   на расхождении в блоке кода перестраивает его сама и отказывает только на противоречии со словами роли; переоткрытие S8 после MR —
   не дверь этой проверки.
4. `waiver.py` находит открытый отказ стадии и при запуске без драйвера (последний отказ `stage_done` из журнала), `--block` — по коду
   отказа, не по подстроке текста.

Решение владельца нужно: нет (решение Lead).
Связи: HF8-16 (подтверждение бага), HF8-17 (отчёт), HF8-21 (контракт баг-репортёра, B-183); B-206 (читатель багов истории); FR-3, FR-10,
FR-38; AR-13, AR-22, AR-27.

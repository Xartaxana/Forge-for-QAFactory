# Текст вопроса `s1_gap` называет человеку скрипт `vcs_evidence.py` — фабрика сама ловит нарушение и спрашивает «как есть»

id: — | кучка: `driver-hosts` | от: C3-7 scout t-841 (тетрадь cmp3 :65, `runs/cmp3-3.log:18-19`) | записал t-843 по приёмке Lead 16.10.2026 | приоритет: П3 | кандидат наверх: нет

Что: на cmp3 15:45 драйвер напечатал «question rules: this text breaks 1 rule(s) of references/human-questions.md — asked anyway, recorded as ours: script_name: `vcs_evidence.py`». Текст берётся из `story_run.py` (~:3098: «the authenticated API (`vcs_evidence.py`) and the local checkouts»). Имя скрипта человеку не показывают (P9, FR-6; B-292 (а) — тот же класс).

Чинить: текст `s1_gap` (и соседи, где драйвер сам ловит свою ошибку — `human_text.problems` уже считает правила на запуске) без имени скрипта; тест, который прогоняет `human_text.problems` по текстам вопросов драйвера (S1/S5/гейты) на фикстурах и красный на любом `script_name`/`flag`/`exit_code`. Сначала проверить, нет ли такого теста.

Куда: C2-9 владеет `s1_gap_text` (`story_run.py`, тексты S1) — одна строка в его спеку вместо отдельного узла; иначе узел ниже.

Повтор 30.10.2026, ночной прогон 14857 (0.10.6): текст `s1_gap` снова называет скрипт `vcs_evidence.py` (`state/driver-questions.jsonl`, RL-2); разбор docs/tasks/specs/reviews/t-1605-14857-night-vs-manual.md #26 (часть про пакет гейта B — новая находка GW1-35).

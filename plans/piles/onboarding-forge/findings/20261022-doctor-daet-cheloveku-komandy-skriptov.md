# Доктор отдаёт человеку шаги фабрики: «сделай вызов shell и Write, перезапусти host_probe.py --check», «project_gitignore.py --write»

id: — | кучка: `onboarding-forge` | от: владелец, 22.10.2026 («Человек не запускает скрипты, только скиллы») | приоритет: П2 | кандидат наверх: нет

Что не так: в отчёте того же первого доктора (0.10.0, копия `testproject1-sdk-fresh010/test-harness`) человеку адресованы действия роли:
- строка хуков (`owner: factory`): «To settle it, make one ordinary shell call and one Write of a temp file in this session. Then re-run
  `host_probe.py --check`» — это `guard_parse.reason` из вывода `host_probe.py --check`, написанный для роли, а доктор пересказал его
  человеку вместо того, чтобы сделать оба вызова сам;
- строка `.gitignore` (`owner: user`): «`project_gitignore.py --write` rewrites the block».

Это противоречит самому уставу доктора (`skills/qa-doctor/SKILL.md`, «Rules of printing»: строка `remedy.owner: factory` шагов не
получает; «Routes the factory can take itself come before anything asked of a person») и P9/FR-6 (текст человеку — по
`human-questions.md`), P3/FR-48: человек вызывает только скиллы (`/qa-factory:…`) и отвечает на вопросы; скрипт, который может запустить
роль, запускает роль, а то, что требует решения человека, приходит вопросом с вариантами («записать блок в .gitignore? да / нет»).

Что сделать: (1) `guard_parse` — доктор сам делает обычный shell-вызов и Write временного файла и перезапускает `--check` (это уже
шаг роли по смыслу `next_action: check_guard_parse`); (2) любая строка отчёта с `remedy.owner: user` называет скилл или вопрос, а не
скрипт; (3) детектор: проверка текста отчёта доктора на имя скрипта в строке, адресованной человеку (эвал `skills/qa-doctor/evals`
— кейс «отчёт без `*.py` в шагах человека»). Сиблинги: тексты человеку у онбординга и `qa-story`, где роль может отдать
`*.py` человеку (ось «текст человеку» карты).

Свидетель: тот же транскрипт, что у находки `20261022-doctor-do-onbordinga-proba-i-huki-v-raznyh-kornyah.md` (финальный отчёт доктора);
скриншоты владельца 22.10.

Принципы и правила: P3, P9, FR-6, FR-48, FR-47, AR-16, AR-9.

Решение владельца нужно: нет.

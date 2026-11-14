# Вызывающие стороны отказов ER/RS остаются голыми (без id) вне узла S-1a: `s6_close_from_state`, `_profile_for`, `find_active_dispatch` и другие

id: — | кучка: `live-run-fvf` | от: отчёт билдера S-1a, `.claude/worktrees/tbw-t1r/docs/tasks/specs/reports/20261114-t1r-sites-s1a-report.md` («Questions for the Lead» 2; «Analogs noticed»: `onboarding_probe.py:278`, прочие помощники с текстовым возвратом); спека `docs/tasks/specs/20261114-told-before-work-t1r-sites-spec.md` §6b п. 4, 8 | приоритет: П3 | кандидат наверх: нет

## Что не так

Класс фабрики: **сайт отказа без литерального id остаётся ВНЕ пути «роль узнаёт требование до работы»** (FR-38, AR-9, AR-22). Билдер S-1a читал B3 буквально для всех помощников с несколькими
вызывающими: id не стоит внутри помощника, он стоит у каждого зовущего (§6b п. 4). Следствие: зовущие вне узла остаются голыми, пока их не обернёт S-1b или другой узел:
- `s6_close_from_state` (отказ «not in the story's approved scope») остаётся голым: помощник зовут `build_mine_request` и `s6_close_dispatch` → `probe_by_code`, и зовущий не отличит этот отказ от других.
  Остаток E4: роль на дороге `probe_by_code --s6-close` встречает этот отказ без строки требования. Сайт `scope` в `build_mine_request` размечен.
- `probe_by_code.py:2686` (`_profile_for`); `probe_by_code.py` около `4755`, `6964`, `7804` и `run_suite.py:3105` (`find_active_dispatch`); `run_suite.py:2877` (`reference_target_problem`).
- `onboarding_probe.py:278` зовёт `ER._command_from_profile` (онбординг-дорога, голая по B3).
- Помощники, возвращающие текст (`_stand_refusal`, `_probe_refusal`, `scope_refusal`, `_no_test_refusal`), обёрнуты на своих сайтах отказа в S-1a; остальные их зовущие (если есть) не размечены.
Критик класса (ключ B3, последний абзац) судил `_profile_for`, `find_active_dispatch` и `_command_from_profile` «не затронутыми», потому что все зовущие спрашивают одно требование; билдер оставил Lead выбор:
ставить id ВНУТРИ этих помощников (три строки правки на помощник) или на каждом зовущем.

## Что именно менять

Узел-классификация (по §6b п. 8, E6): по каждому голому сайту выше назвать, КОД это (ошибка вызывающего, которую роль встретить не может) или РОЛЬ (требование, которое роль может выполнить).
1. Файлы: `ai-packages/qa-factory/scripts/probe_by_code.py`, `ai-packages/qa-factory/scripts/run_suite.py`, `ai-packages/qa-factory/scripts/onboarding_probe.py`,
   `ai-packages/qa-factory/scripts/execution_request.py` (`s6_close_from_state`, `_profile_for`, `find_active_dispatch`, `reference_target_problem`, `_command_from_profile`).
2. Для РОЛЕВЫХ: предложенная строка таблицы 31 id (`execution_request:` / `run_suite:`) с id на зовущем, по правилу §6b п. 4 (id литералом на каждом зовущем многозовного помощника);
   для КОДОВЫХ: пометка «code-only» с причиной, как у E6.
3. Выбор «внутри помощника или на зовущем» Lead делает до сборки (слово билдера S-1a: «если Lead предпочтёт id внутри — три строки правки на помощник»); по умолчанию остаётся §6b п. 4
   (id на зовущем, помощник голый).
4. Тест: строки `T1rs/` в `ai-packages/qa-factory/scripts/tests/test_detector_verdict.py` (быстрый файл по §6b п. 3): сканер id по обоим направлениям (литерал вне 31 строки — красный, строка без литерала — в
   `untold`).

Принципы и правила: FR-38, FR-16; AR-9, AR-22, AR-13.

Решение владельца нужно: нет.

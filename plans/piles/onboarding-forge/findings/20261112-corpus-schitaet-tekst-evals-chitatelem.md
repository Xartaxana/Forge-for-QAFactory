# `install_paths._corpus` считает текст `skills/*/evals/` читателем файла установки

id: — | кучка: `onboarding-forge` | от: критик диффа OH3-9, `docs/tasks/specs/reviews/t-182-oh3-9-diff.md` (очередь Q1), 12.11.2026 | приоритет: П3 | кандидат наверх: нет

## Что наблюдалось

`scripts/install_paths.py`, `_corpus` (:493-510 на main; :507-525 на ветке OH3-9 `pile/onboarding-forge/batch-1`): корпус читателей берёт `CORPUS_DIRS` (включая `skills`, :73) и суффикс `.json`;
исключены только таблица и `install_paths.py` (`CORPUS_EXCLUDED`, :77), а из обхода выброшен только `scripts/tests` (:502 на main). Поэтому `skills/qa-onboarding/evals/evals.json` —
проза оценок — считается «читателем» пути: ловушка, из-за которой пришлось менять формулировку eval 16 (критик t-182 проверил сам). Проверка на main: те же :73, :77, :502 — не исправлено.

## Что именно менять

1. `scripts/install_paths.py`, `_corpus`: в фильтре обхода (там, где отбрасывается `scripts/tests`) отбрасывать и `skills/<любой>/evals/` — одно условие, тем же приёмом.
2. После правки eval 16 в `skills/qa-onboarding/evals/evals.json` снова может называть `qa-factory/state/jira-probe-x.json` (вернуть исходную формулировку, если её поменяли только из-за ловушки).
3. Тест: `scripts/tests/test_install_paths.py` — строка таблицы случаев: строка в `skills/x/evals/evals.json`, называющая путь, не делает путь «имеющим читателя»; тот же путь в `scripts/x.py` — делает.

Связи: узел OH3-9 пачки 1 (ветка `pile/onboarding-forge/batch-1`, не в main — править после слияния). Принципы и правила: FR-12, FR-54; AR-13, AR-22.

Решение владельца нужно: нет.

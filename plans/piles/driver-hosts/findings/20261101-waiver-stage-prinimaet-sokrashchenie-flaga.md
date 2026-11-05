# `waiver.py` принимает сокращённый флаг `--stag S1` как `--stage`: слово человека записывается под сокращением, охранного теста нет

id: — | кучка: `driver-hosts` | от: спека t-303 (`docs/tasks/specs/t-303-R3-question-registry-and-decisions.md`, F3: «N3 closes `waiver.py`'s `--gate` and abbreviated flags (`allow_abbrev=False`; the guard test with `--stag`)»), перепроверено 01.11.2026 | приоритет: П3 | кандидат наверх: нет

Что не так: t-303 F3 требовал закрыть сокращения флагов `waiver.py` (`allow_abbrev=False`) и пинить охранным тестом на `--stag`. На `1afda33f` разборщик создан без `allow_abbrev` (`waiver.py:1511`: `ap = argparse.ArgumentParser(description="record a coverage gap accepted at a gate")`), и `git grep -n "allow_abbrev\|--stag" -- ai-packages/qa-factory/scripts/waiver.py ai-packages/qa-factory/scripts/tests` не находит ни параметра, ни охранного теста (находятся только заметки в фикстурах конфигурации, к флагам не относятся; контроль: `--stage` в `waiver.py:1516` найден тем же поиском). Значит, по умолчанию argparse принимает однозначную приставку `--stag` как `--stage` (по чтению argparse; не прогонялось), и слово человека записывается под сокращением: точное ограничение «слово человека — только идентификатором целиком» (FR-12; GW1-1) на уровне флага не держится. Направление ошибки: слово не пропадает, но принимается форма, которую дверь не печатала и тесты не пинят.

Что именно менять: `ai-packages/qa-factory/scripts/waiver.py:1511`: `argparse.ArgumentParser(description=…, allow_abbrev=False)`; отказ argparse на неизвестный флаг называет флаг (проверить, что текст отказа называет `--stag` и что `--stage` верен, FR-1). Тест `scripts/tests/test_waiver*.py` (имя проверить по коду, `git grep -ln "waiver.py" -- ai-packages/qa-factory/scripts/tests`): `waiver.py --task T --stag S1 --block x --decision y` → выход 2 и отказ с флагом `--stag`, ничего не записано; `--stage S1` — записано; полный флаг рядом с сокращением того же флага (`--stage S1 --stag S2`) — отказ. Соседи: все `argparse.ArgumentParser(` скриптов, что пишут слово человека (`git grep -n "ArgumentParser(" -- ai-packages/qa-factory/scripts` и `allow_abbrev`) — перечислением с вердиктом «закрыт / не пишет слово человека».

Свидетель: `docs/tasks/specs/t-303-R3-question-registry-and-decisions.md` F3; `ai-packages/qa-factory/scripts/waiver.py:1511`, `:1516`.

Принципы и правила: P13; FR-1, FR-12, FR-54; AR-9, AR-18.

Решение владельца нужно: нет.

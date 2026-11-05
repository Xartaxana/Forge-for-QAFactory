# Команда `npx` (и любой `.cmd`-запуск) на Windows не запускается без оболочки: проба гейта и `run_suite` дают WinError 2, хотя `shutil.which` находит запуск

id: — | кучка: `execution-probes` | от: критик диффа S2a2 часть 1 (r0107-s2a2-p1-diff-critic.md, ответ 3), 30.10.2026 | приоритет: П2 | кандидат наверх: нет

Что не так / что сделать: на Windows `npx` — это `npx.CMD`. Запуск без оболочки (`subprocess.run(["npx", "--version"])`) даёт
`FileNotFoundError [WinError 2]`, хотя `shutil.which("npx")` находит `C:\Program Files\nodejs\npx.CMD`. Оба запуска фабрики идут без оболочки и
без разрешения имени: `_probe_reporter` в `gate_preflight.py` (код `launcher_missing`, затем «`npx` is not on this machine», что неверно) и
`run_suite.py` около строки 1780. При этом `gate_preflight.py` около строки 410 использует `shutil.which` и говорит «запуск находится»: два ответа
на одной машине. Следствие: образец в `references/profile-shape.json` и шаг 2 лестницы §7 спеки EP1-22 на Windows не проходят, пока в профиле нет
`npx.cmd`. Лечение — вилка Lead, не решение этой находки: ОДИН разрешатель запуска на оба вызова через `shutil.which` (AR-13, AR-15) и то, как
аргументы цитируются для `.cmd` (кавычки и `^` для оболочки `cmd`); до решения проба отвечает правду («`npx` найден как `npx.CMD`, но фабрика
запускает без оболочки»), а не «нет на этой машине» (FR-41, FR-1).

Свидетель: запуск критика на копии `4f386f51`: `which: C:\Program Files\nodejs\npx.CMD`; `subprocess.run(["npx","--version"])` →
`FileNotFoundError [WinError 2]`; `docs/tasks/specs/reviews/r0107-s2a2-p1-diff-critic.md`, ответ 3. Связь: `20261028-playwright-junit-otchet-ne-chitaetsya.md`
(владелец цитирует `npx` там же); EP1-22.

Принципы и правила: P2, P5; FR-1, FR-41, FR-54; AR-4, AR-13, AR-15.

Решение владельца нужно: нет (вилка Lead: форма разрешателя и цитирование для `.cmd`).

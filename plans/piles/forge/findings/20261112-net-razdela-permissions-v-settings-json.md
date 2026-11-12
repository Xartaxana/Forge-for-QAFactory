# В `.claude/settings.json` нет раздела `permissions`: 2 560 из 2 827 вызовов оболочки без совпадения со списком, каждый просит подтверждения

id: — | кучка: `forge` | от: Lead, калибровка 12.11.2026 (`docs/tasks/specs/reports/calibration-20261112.md`, п. 7), записал builder t-093 | приоритет: П2 | кандидат наверх: нет

## Что не так

Класс: «разрешение команды, нужной каждой сессии, не записано в носитель, который читает хост, и каждая сессия платит запросом
оператору». Причина волны запросов — не форма команд, а отсутствие списка.

Свидетель (часть p3, `docs/tasks/specs/reports/calibration-20261112-p3.md`, проверка 27):
- `python -B -X utf8 tools/permission_audit.py --all --summary`: просмотрено 2827 вызовов Bash/PowerShell, «likely needed confirmation» 2560,
  причина «no allowlist match» — 2560 (1514 билдер, 656 критик, 388 главная, 2 дизайнер).
- `.claude/settings.json`: ключи `model`, `enabledPlugins`, `extraKnownMarketplaces`, `hooks`; ключа `permissions` нет (проверено и лидом
  в записи калибровки: `"permissions"` — 0, `"hooks"` — 12); `.claude/settings.local.json` отсутствует (`ls .claude`).
- пользовательский `~/.claude/settings*.json` не читался (вне корзины и приватен).

## Что именно менять

**Решение владельца нужно (настройка безопасности хоста, правило 11a; `PROJECT.md`: настройки хоста — решение владельца).** Узел исполним
по рекомендации, но запись в `.claude/settings.json` делает только Lead в приёмке и только по слову владельца.

1. Навык `.claude/skills/permission-audit` (читает `tools/permission_audit.py`): запустить на всём окне
   (`python -B -X utf8 tools/permission_audit.py --all --summary`), получить предложенные строки `permissions.allow`; предложение — файл
   `docs/tasks/specs/permission-allow-proposal.md` (строки, по каждой — сколько вызовов закрывает, чем уже). Ожидание: строки узкие
   (`python -B tools/*`, `python -m pytest tools/*`, `git -C * status|diff|log`, чтение репозитория) и без широких масок вроде `Bash(*)`.
2. После слова владельца: Lead вставляет раздел `permissions` (только `allow`, `deny` не трогается) в `.claude/settings.json` и перезапускает
   `permission_audit.py --all --summary`: доля «no allowlist match» падает; число и причина остатков называются.
3. Тест: `python -B tools/permission_audit.py --all --summary` до/после (вывод как свидетель); `python -m pytest tools/test_permission_audit.py -q`
   (если есть) зелёный; ручная проверка на негативе — строка вне списка по-прежнему просит подтверждения.

Края: список не маскирует правило гигиены команд (`cd`, `2>&1`, `python -c` отказывает/предупреждает `hygiene_gate` независимо от
списка); новая строка разрешения не закрывает мутирующие команды (`git push`, `git reset`) — их по-прежнему подтверждает человек.

Исполнитель: builder (предложение) → Lead и владелец (запись в настройки).

## Связи

`../../forge/findings/20261009-b-449-stream-copies-remainder.md` (упоминает `permission_audit`, другая тема);
`20261023-hooki-sessii-privyazany-k-cwd-cd-v-paket-otbivaet-kazhdyj-vyzov.md` (`onboarding-forge`, F6-36: тот же вопрос «лишние запросы»).

Принципы и правила: P25 (настройки хоста — данность проекта; запись — по слову владельца); AR-5.

Решение владельца нужно: да — вопрос простыми словами: «Включить ли в `.claude/settings.json` список разрешённых команд, чтобы сессии
не просили подтверждения на каждый запуск тестов и чтение репозитория? Рекомендация: да; навык `permission-audit` предложит узкие строки,
вы смотрите список до записи; цена — несколько строк в настройках, откат — удалить раздел».

<!-- id выдаёт интегратор при сборке пачки. -->

# Исходники docker-канона, собранные `git archive` на Windows, пришли с CRLF и испортили канон

id: — | кучка: `onboarding-forge` | от: docker BATCH CANON релиза 0.10.3, 27.10.2026 | приоритет: П2 | кандидат наверх: нет

Что не так / что сделать: исходники для docker-канона собраны `git archive` на Windows с `core.autocrlf=true` и пришли с окончаниями CRLF. В Linux `hooks/run-py.cmd` сломался (`Syntax error: end of file unexpected`), первый канон 0.10.3 стал недействительным. Починка в рецепте канона: `git -c core.autocrlf=false archive …` (или `.gitattributes` с `eol=lf` для sh/cmd-файлов пакета; выбирает билдер `tools/batch_canon.py` F6-34 или Lead). Проверка рецепта: в собранной копии нет `\r` в `hooks/*.cmd` и `*.sh` (тест на копии, не на рабочем дереве).

Предыдущий канон `canon-hotfix-b3` (394/436) мог иметь тот же дефект: его красные не читать как поведение без проверки на `\r`.

Свидетель: журнал канона релиза 0.10.3 (`D:/ws1/canon-release-0103\out\`, вне репозитория), рецепт в `docs/RUNBOOK.md`; связь — узел F6-34 (BATCH CANON как скрипт) и `forge/findings/20261021-kanon-pachki-zhivet-tolko-v-proze.md`.

Принципы и правила: FR-31 (красный от среды, не от кода), FR-32, FR-54; AR-4 (ничто не привязано к машине и раскладке).

Решение владельца нужно: нет.

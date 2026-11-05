# `.gitattributes` у пакета нет: свежий клон на Windows с `core.autocrlf=true` кладёт фикстуру…

id: B-409 | кучка: `onboarding-forge` | от: разведка t-460 (C2); отчёт `qa-factory-smoke-failure-report.md` | приоритет: — | кандидат наверх: нет

Что не так / что сделать: `.gitattributes` у пакета нет: свежий клон на Windows с `core.autocrlf=true` кладёт фикстуру `scripts/tests/fixtures/old-generation-project/.gitignore` с CRLF, писатель `project_gitignore.py:113-126` сохраняет CRLF, свежая запись — LF, `compare_trees` (`onboard_apply.py:1391`) видит разные байты → `test_reinstall_equals_fresh` K5 и `install_smoke.py` красные, онбординг не стартует (Максим 05.10, dev2 05.10 = B-386; воспроизведено механизмом на этой машине: worktree CRLF, старый чекаут владельца LF). План: `.gitattributes` в пакете (фикстуры, `*.py`, `*.json` — `text eol=lf`), едет в релизную копию; `compare_trees` печатает первую отличающуюся строку и признак EOL; `install_smoke` называет CRLF-чекаут словами; латки CRLF по месту (`test_case_id_form_sites.py:111`, `test_launcher_argv.py:224/713`, `test_person_words.py:674`, `content_size.py:6`, `test_novelty.py:217`, `driver_golden.py:904`) снимаются. Закрывает B-386. До релиза. [F15]

Свидетель: Любой коллега на Windows получает красный онбординг и ложный вывод «CRLF ни при чём».

Принципы и правила: FR-1, FR-31, FR-54

Решение владельца нужно: нет (фраза не найдена)

<!-- piles split: plans/BACKLOG.md, раздел 12 «Миграция исправлений из legacy-прогона TP2-2406»; ячейки строки перенесены дословно -->

Строка BACKLOG.md целиком:

```
| B-409 | `.gitattributes` у пакета нет: свежий клон на Windows с `core.autocrlf=true` кладёт фикстуру `scripts/tests/fixtures/old-generation-project/.gitignore` с CRLF, писатель `project_gitignore.py:113-126` сохраняет CRLF, свежая запись — LF, `compare_trees` (`onboard_apply.py:1391`) видит разные байты → `test_reinstall_equals_fresh` K5 и `install_smoke.py` красные, онбординг не стартует (Максим 05.10, dev2 05.10 = B-386; воспроизведено механизмом на этой машине: worktree CRLF, старый чекаут владельца LF). План: `.gitattributes` в пакете (фикстуры, `*.py`, `*.json` — `text eol=lf`), едет в релизную копию; `compare_trees` печатает первую отличающуюся строку и признак EOL; `install_smoke` называет CRLF-чекаут словами; латки CRLF по месту (`test_case_id_form_sites.py:111`, `test_launcher_argv.py:224/713`, `test_person_words.py:674`, `content_size.py:6`, `test_novelty.py:217`, `driver_golden.py:904`) снимаются. Закрывает B-386. До релиза. [F15] | Любой коллега на Windows получает красный онбординг и ложный вывод «CRLF ни при чём». | разведка t-460 (C2); отчёт `qa-factory-smoke-failure-report.md` | FR-1, FR-31, FR-54 |
```

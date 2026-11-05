# `execution_fingerprint.py` падает с `TypeError` на спеке ровно той формы, что описывает его собственная справка роли

id: — | кучка: `execution-probes` | от: владелец, 22.10.2026 (S5 окно 1 TP1-12586 на `testproject1-dev-010`, 0.10.0) | приоритет: П1 | кандидат наверх: нет

перенос: hotfix-12586/batch-1 (узел HF1-2; слово владельца 23.10.2026 — срочная отдельная пачка; узел EP1-8 здесь закрывается её хэшем)

Что не так: карточка роли `references/role-commands.json` → `execution_fingerprint.py` (роли `qa-automator`, `qa-runner`) говорит:
`test_files`, `config_files`, `dependency_files` — «each a list of {path, sha256} for files that exist on disk now … a claimed sha256 that does
not match the bytes is refused». Код `scripts/execution_fingerprint.py` `build()` (строки ~51-56) читает каждую запись как строку пути:
`Path(raw).resolve()` — на словаре `{path, sha256}` это `TypeError`, необработанный, а не отказ; заявленный `sha256` `build()` вообще не
сравнивает (сравнение есть только в `verify_files`). Автоматор написал спеку по справке → падение → окно 1 S5 встало до первого теста;
дирижёр записал это как FB-5 в бэклог ПРОЕКТА и переписал спеку списками строк. Деньги окна и диспатч — впустую на каждом прогоне.

Почему это дефект: FR-11 / FR-14 (форма входа скрипта — контракт; инструмент, который роли велено звать, должен принимать то, что ей
описано), FR-1 / AR-9 (отказ говорит, что не так и чего ждут, — не трассировка `TypeError`), AR-13 (одна форма записи файла — один
читатель: `verify_files` и `build` читают одно поле по-разному), FR-19 / AR-27 (ошибка фабрики записана в бэклог проекта — тот же класс,
что OH3-10).

Что сделать: (1) `build()` принимает обе формы — строку пути и `{path, sha256}`; для записи с `sha256` сверяет байты (одна функция
нормализации записи, её зовут `build` и `verify_files`); (2) неверная форма записи — отказ с примером формы, не `TypeError`;
(3) карточка в `role-commands.json` и `--help` (`epilog`) описывают одну и ту же форму, тест сверяет карточку с тем, что `build`
принимает (пример из карточки проходит `build`); (4) тест: спека из справки (`{path, sha256}`) → отпечаток; неверный `sha256` → отказ с
именем файла; словарь без `path` → отказ с формой; (5) свип: другие скрипты из `role-commands.json`, чей пример входа в карточке не
прогоняется тестом (класс «справка расходится с парсером»), — список с вердиктом по каждому; (6) ошибка своего скрипта — находка фабрики,
не строка `factory-backlog.md` проекта (общий узел с OH3-10 по классу).

Свидетель: сообщение дирижёра владельцу 22.10 («The factory's fingerprint script crashes on the spec format its own help text describes.
I logged that as FB-5»); `testproject1-dev-010/testproject1-sdk/test-harness/qa-factory/factory-backlog.md` строка FB-5 («fp-spec.json with
{path,sha256} lists -> TypeError; path-string lists accepted»); `scripts/execution_fingerprint.py:24-60`; `references/role-commands.json`
(`execution_fingerprint.py`).

Принципы и правила: FR-1, FR-11, FR-14, FR-19, AR-9, AR-13, AR-27.

Решение владельца нужно: нет.

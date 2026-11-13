# Перепись выходов драйвера: долги Lead (N-L, путь реестра, ключ keep) и перепись вне пути CI

id: — | кучка: `live-run-fvf` | от: критик кода узла P1-b N1, `docs/tasks/specs/reviews/20261113-p1b-n1-code-critic.md`, строка «F12 — owed by the Lead, not the builder» (и «Топик-вопрос 5, регистрация»); спека `docs/tasks/specs/20261113-p1b-dry-story-spec.md` (N-L R-L1/R-L2, §3.2) | приоритет: П2 | кандидат наверх: нет

## Что не так

Класс фабрики: **обязательства слияния (строки карты, брифа, спеки, ключ `keep`) записаны только в ревью; пока их нет, новый ratchet стоит без правила и вне пути CI (AR-20; FR-44)**.

- N-L R-L1 (строки осей 18, 34 и 17 в `docs/SIBLING_MAP.md`: четыре счёта плюс `raised_by` с семантикой F2) и R-L2 (вопрос 9 в
  `docs/tasks/critic-diff-brief.md`) должны войти вместе со слиянием N1 (изменение AR-20, `architecture.md:222`).
- Путь реестра красных строк `fixtures/driver-exits/known_red.json` записывается в спеку §3.2 одной строкой (P1-a §3.6 оставляет файл спеке P1-b).
- Ключ `keep` для `test_scenario_dry_1.py` (владелец — N3, `test-layers.json`) несёт `covers` += `tests/dry_exits.py`,
  `scripts/tests/fixtures/driver-exits`; строка `keep` ключуется только `test_*.py`, поэтому предложенный билдером ключ `dry_exits_census` неверен по форме.
- Пока файл теста N3 не запускает перепись, `--check`/`--selftest` не стоят ни на одном пути CI: `canon.yml` гоняет только `dry_world.py --spike`.
  Пункт (d) сообщения коммита N1 говорит об этом честно.

## Что именно менять

Узел-документ (исполнитель builder; тексты диктует спека P1-b N-L). Проверить сначала, что из этого уже сделано при слиянии.

1. `docs/SIBLING_MAP.md`: оси 18, 34, 17 — строки R-L1; ось 18 называет четыре счёта (`live_only`, `after`, `unwalked`, `hook_layer`), `raised_by` и
   смысл «каждая запись называет свой счёт; выше — красное, ниже — устаревший кредит» (после фикса F2 критика).
2. `docs/tasks/critic-diff-brief.md`: вопрос 9 — строка R-L2.
3. `docs/tasks/specs/20261113-p1b-dry-story-spec.md` §3.2: путь `fixtures/driver-exits/known_red.json`.
4. `ai-packages/qa-factory/scripts/tests/test-layers.json`: `covers` у `keep`-строки `test_scenario_dry_1.py` (после того, как N3 её создаст).
5. `.github/workflows/canon.yml`: перепись (`dry_exits.py --check`, `--selftest`) на пути CI — либо через тест N3, либо строкой задачи; выбор — Lead пачки.
   Развилка: пока (5) не решён, пункт остаётся называнием «не на пути CI» в отчёте узла.

Свидетель (документ-диспатч): ключи дословно из этого списка до прогона; скрипт в отчёте целиком; отрицательный контроль — один ключ намеренно отсутствует.

Принципы и правила: AR-20, FR-44; `docs/TESTING.md` (ключи `keep`).

Решение владельца нужно: нет.

# Пакет: тесты, Linux, CI (`package-ci`)

приоритет: П1 | фичи: F15 | стенд: не нужен (CI) | зона: `.gitlab-ci.yml`, `ai-packages/qa-factory/scripts/selftest.py`, `scripts/install_smoke.py`, `scripts/onboard_apply.py`, `scripts/project_gitignore.py`, `scripts/stage_done.py`, `scripts/manifest_put.py`, `scripts/stand_lease.py`, `scripts/tests/test_story_run*.py`, `scripts/tests/test_words_doors.py`, `references/gate-registry.json`

## Зачем

Сегодня пакет зелёный на машине владельца и красный на Linux и на второй Windows-машине; часть тестов падает только
под нагрузкой, часть идёт дольше лимита полного прогона. Поэтому ночной полный прогон в CI и релиз не доказывают,
что пакет целый везде, где им пользуются. После первой пачки полный прогон зелёный на Linux и на второй
Windows-машине, тесты стабильны под нагрузкой и укладываются в лимит, а реестры гейтов и тексты не называют того,
чего в коде нет.

## Что не так сегодня (факты)

- Первый полный прогон на Linux 04.10: 11 красных файлов, все зелёные на Windows (`plans/BACKLOG.md:251`); `package-fast` 03.10 — пять красных файлов (`plans/BACKLOG.md:257`).
- `tools/` на Linux: 21 упавший тест, из них 5 — гейты не узнают POSIX-пути, остальные — фикстуры с Windows-путями (`plans/BACKLOG.md:256`).
- `test_story_run` идёт 484 с, `test_words_doors` 177 с (`plans/BACKLOG.md:367`); на 13.10 файла `scripts/tests/test_story_run.py` в дереве нет — он разрезан на семейство `test_story_run_*.py`, цифра 484 с датирована, актуальные времена брать со свежего прогона CI; `test_story_run_freshness` 223–967 с под нагрузкой (`plans/BACKLOG.md:475`); потолок 600 с поднят как временная мера (`plans/BACKLOG.md:247`).
- Вторая Windows-машина (Python 3.13.5, `core.autocrlf=true`): набор проверок 0.8.1 падает, причина по каждой не установлена (`plans/BACKLOG.md:406`).
- 16 открытых строк в пачке 1 и 14 находок (дайджест `docs/tasks/specs/reports/t-712-scout-piles-a.md`, пересчёт 16 из 16 и 14 из 14 на 13.10).

## Пачки

| № | Что изменится для пользователя | Строки | Размер | Статус | Взял | Ветка | MR |
|---|---|---|---|---|---|---|---|
| 1 | полный прогон зелёный на Linux и на второй Windows-машине, тесты не падают под нагрузкой, время тестов в лимите | B-307, B-301, B-302 | M | закрыта | — | — | `855d4e5c` |
| 2 | пины потолков брифа в тестах строятся во время теста, а не берутся из измеренной константы | — (находка 02.11.2026, узел PC2-1) | S | закрыта | dev1, 11.11.2026 | `pile/package-ci/batch-2` | `b592d8a` |
| 3 | потолок брифа «только двери» в тесте ужат до замера CI после PC2-6 | — (находки 12.11.2026, узлы PC3-1, PC3-2) | S | ожидает | — | — | — |

Открытое перенесено 01.11.2026 → words-gates/1, onboarding-forge/1, onboarding-forge/2.

Статусы пачки: `ожидает` → `в работе` → `сдано` → `принято` → `закрыта`. Размер — по узлам: S ≤ 4 узлов,
M 5–9, L 10–15 (больше — две пачки). Взятая пачка заморожена: её файл правит только взявший, новое
по теме — файлом в `findings/`.

## Бриф пачки 1

Начать с PC1-1 (красные файлы на Linux) и PC1-2 (вторая Windows-машина): они дают список, по которому читаются остальные
узлы; PC1-4 и PC1-5 (время тестов) идут после PC1-1 по `selftest.py`. Стенд не нужен — свидетель CI (`package-fast`,
`package-full`) и образ CI; слово владельца не нужно. Подробно — `batch-1-green-ci.md`, раздел «Бриф».

## Дороги

Читать по порядку: эта карточка → `batch-1-green-ci.md` → находки узла (колонка «id / файл» ниже) → строки
`plans/BACKLOG.md` 247, 251, 256, 257, 342, 344, 350, 357, 367, 390, 401, 406, 422, 464, 466, 475 → `.gitlab-ci.yml`
(задачи `forge-check`, `package-fast`, `package-full`) → `ai-packages/qa-factory/scripts/selftest.py` (таблицы
`TEST_TIMEOUTS`, `SLOW_TESTS`) → `plans/builder-rules.md` → `PROJECT.md` «Как принимается изменение пакета» п. 2 (что
гоняет CI, что — машина).
Слова: `plans/features.json` F15 (поле `words`) и сверх них: `TEST_TIMEOUTS`, `SLOW_TEST_TIMEOUT_S`, `SLOW_TESTS`,
`allow_failure`, `package-fast`, `package-full`, `forge-check`, `autocrlf`, `.gitattributes`, `atomic_json`,
`os.replace`, `log_append`, `committed_event`, `stand_lease`, `compare_trees`, `IMPORT_RE`, `gate-registry.json`,
`red_sandbox.verify`, `ticket_freshness`, `PYTEST_CURRENT_TEST`, `MANIFEST.json`, `allowed_patterns`; «Linux»,
«под нагрузкой», «потолок», «воркеры».
Не читать: зоны `conductor` и `driver-controller` (кроме их находок про подпапку git и golden — имена в колонке «связи» ниже),
код стадий (`story_run.py`) вне тестов узла.

## Содержание

Снимок 13.10.2026; пути — от `ai-packages/qa-factory/` (вне пакета — от корня репозитория); суть строк — из `plans/BACKLOG.md`, находок — из дайджеста t-712. При расхождении авторитетна доска `plans/PILES.md`.

| id / файл | вид | суть (≤ 20 слов) | пути | статус | слово владельца | связи |
|---|---|---|---|---|---|---|
| **Пачка 1** | | | | | | |
| B-307 | строка | первый полный прогон на Linux 04.10: 11 красных файлов, все зелёные на Windows; разбор после релиза | `scripts/selftest.py`, `.gitlab-ci.yml` | пачка 1, PC1-1 | отсрочка 03.10 («разбор после релиза») | — |
| B-301 | строка | первый прогон 03.10, `package-fast`: пять красных файлов (а–д); `allow_failure` до починки | `.gitlab-ci.yml` | пачка 1, PC1-1; `pyyaml` в CI уже добавлен по тексту — проверить по коду | нет | — |
| B-302 | строка | `tools/` на Linux: 21 упавший тест; 5 — гейты не узнают POSIX-пути, 9 — фикстуры с Windows-путями | `scripts/selftest.py` | пачка 1, PC1-1 | нет | — |
| B-386 | строка | вторая Windows-машина (Python 3.13.5, `autocrlf=true`): набор 0.8.1 падает, причина по каждой не установлена | `scripts/install_smoke.py`, `scripts/tests/test_ticket_light.py` | пачка 1, PC1-2; `test_archive_task` починен на ветке по тексту — проверить, влито ли | нет | находка B-409 |
| B-446 | строка | остатки `.gitattributes`: `compare_trees` может сказать «одинаково» при JSON `true`/`1` (опасная сторона, FR-59) | `scripts/onboard_apply.py`, `scripts/tests/test_ticket_light.py` | пачка 1, PC1-2 | нет | находка B-409 |
| B-448 | строка | остатки кодировки консоли: три локальных ASCII-запасных варианта, `IMPORT_RE` слеп к `try: import X` | `scripts/stage_done.py`, `scripts/install_smoke.py` | пачка 1, PC1-2 | нет | `live-runs` (кодировка консоли) |
| B-326 | строка | полный `selftest.py` на 4 воркерах на Windows нестабилен: гонка замены файла (M8), таймаут `test_story_run` | `scripts/stand_lease.py`, `scripts/stage_done.py` | пачка 1, PC1-3 | нет | — |
| B-320 | строка | `test_obligation_join.py` падает только под нагрузкой; найти причину, печатать `report["left"]` | `scripts/tests/test_obligation_join.py` | пачка 1, PC1-3 | нет | — |
| B-333 | строка | прямые `os.replace` вне `atomic_json`, та же гонка; `committed_event` и `manifest_put` «projection stale» | `scripts/manifest_put.py`, `scripts/controller.py` | пачка 1, PC1-3 | нет | `driver-controller` (ревизия журнала) |
| B-318 | строка | `log_append` берёт замок журнала внутри замка истории `stage_done`; вложенный замок | `scripts/stage_done.py` | пачка 1, PC1-3 | нет | — |
| B-344 | строка | тесты дольше лимита selftest: `test_story_run` 484 с, `test_words_doors` 177 с; разбить оба | `scripts/tests/test_story_run_*.py`, `scripts/tests/test_words_doors.py` | пачка 1, PC1-4; файла `test_story_run.py` уже нет (разрезан) — актуальные времена по свежему прогону; запас `SLOW_TEST_TIMEOUT_S = 900` — не доказательство | нет | `driver-controller` (медленные тесты) |
| B-381 | строка | у `test_words_doors.py` нет строки в `TEST_TIMEOUTS`: измерить отдельно, задать потолок или разбить | `scripts/selftest.py`, `scripts/tests/test_words_doors.py` | пачка 1, PC1-4 | нет | — |
| B-460 | строка | `test_story_run_freshness.py` 223–967 с под нагрузкой; разрезать по сценариям, снять потолок 600 | `scripts/tests/test_story_run_freshness.py` | пачка 1, PC1-5 | нет | `driver-controller` (свежесть тикета) |
| B-297 | строка | `test_story_run_s0.py` 305 с, `test_story_run_gate_repair.py` 238 с; потолок поднят до 600 как временная мера | `scripts/tests/test_story_run_s0.py`, `scripts/tests/test_story_run_gate_repair.py` | пачка 1, PC1-5 | нет | — |
| B-368 | строка | у `red_sandbox.verify` нет строки в `references/gate-registry.json`, хотя он выносит вердикт | `references/gate-registry.json` | пачка 1, PC1-6 | нет | — |
| B-403 | строка | комментарий и тексты называют несуществующую `story_run.ticket_freshness`; остаётся `phases/s8.md` §2b и три R11-текста | `skills/qa-story/phases/s8.md` | пачка 1, PC1-6; половина `s8.md` сделана узлом по гейту B (по тексту) — проверить по коду | нет | `live-runs` (гейт B) |
| **Зелёный прогон и нагрузка (кандидаты пачки 2)** | | | | | | |
| `findings/B-409-gitattributes-u-paketa-net-svezhiy-klon.md` | находка | `.gitattributes` у пакета нет; CRLF-фикстура краснит `install_smoke`; план `text eol=lf` | `scripts/project_gitignore.py`, `scripts/onboard_apply.py`, `scripts/install_smoke.py` | входит в PC1-2 (закрывает вторую Windows-машину по тексту) | нет | — |
| `findings/B-101-selftest-i-install-smoke-na-posix-ci.md` | находка | `selftest` и `install_smoke` на POSIX: CI или разово на macOS перед релизом; два macOS-дефекта | — | кандидат пачки 2 | нет | — |
| `findings/20261009-check-pod-pytest-ne-padaet.md` | находка | под pytest `check()` только записывает: красная проверка не роняет прогон; поднимать `AssertionError` | `scripts/tests/harness.py`, `scripts/selftest.py` | кандидат пачки 2 | нет | — |
| **Списки-копии и расхождения с кодом** | | | | | | |
| `findings/B-300-spisok-git-khukov-i-ego-kopii-v.md` | находка | список git-хуков и его копии в `tools/`: шесть пунктов (а–е) | `tools/session_context.py`, `tools/test_wiring_check.py`, `tools/agents_md.py` | открыто | нет | — |
| `findings/B-401-rezhim-sliyaniya-tools-journal-validator-py-t.md` | находка | режим слияния `journal_validator` принимает строки MERGE_HEAD без перепроверки; решить, перепроверять ли форму | `tools/journal_validator.py` | открыто | нет (решение Lead) | `forge` |
| `findings/B-402-v-obedinennom-zhurnale-71-sovpadayushchiy-task.md` | находка | в объединённом журнале 71 совпадающий `task_id`; ключевать по (`ts`, `task_id`) или маркеру ветки | `tools/forge_metrics.py` | открыто | нет | `forge` |
| `findings/B-205-design-state-exits-md-69-utverzhdaet-chto.md` | находка | `design/state-exits.md` утверждает доказательство `halts[]`, а тест не утверждает `resolved` | `design/state-exits.md`, `scripts/tests/test_story_run_*.py` | открыто | нет | `driver-controller` |
| `findings/20261009-driver-golden-manifest-hash.md` | находка | `MANIFEST.json` хранит хэши всех файлов пакета: правка любого теста делает golden «чужим» | `experiments/driver-golden/MANIFEST.json` | кандидат пачки 2 | нет | `driver-controller` (golden драйвера) |
| **Универсальность форм (P2: трекер, VCS, монорепо, тестовые пути)** | | | | | | |
| `findings/B-405-forma-klyucha-tiketa-jira-a-z-a-z0-9-d-zashita.md` | находка | форма ключа тикета Jira зашита в шесть мест; нужен один читатель из конфига | `scripts/ticket_light.py`, `scripts/stage_guard.py` | открыто | нет | `live-runs`, `stand-and-sources` |
| `findings/B-406-dostavka-raspoznaetsya-tolko-po-glab-mr.md` | находка | доставка распознаётся только по `glab mr create` / `gh pr create`; формы вынести в `adapters.vcs` | `scripts/stage_guard.py`, `scripts/story_run.py` | открыто | нет | `live-runs`, `stand-and-sources` |
| `findings/B-407-ostalnoy-inventar-odin-yazyk-instrument.md` | находка | остальной инвентарь «один язык / инструмент / проект»: 20 мест по шести осям | `scripts/stage_guard.py`, `scripts/gate_preflight.py` | части A, A-map, B-run, B-report, C, D влиты 07.10 по тексту находки — остаток проверить по коду | нет | `onboarding-hooks`, `execution-probes` |
| `findings/B-412-proekt-v-podpapke-git-repozitoriya-monorepo.md` | находка | проект в подпапке git: три проверки `.git` заменить на `git rev-parse --show-toplevel` | `scripts/story_run.py`, `scripts/hooklib.py` | открыто; остатки ведёт `driver-controller` | нет | `driver-controller` (DC1-7) |
| `findings/B-415-d-0030-mesta-testov-v-repozitorii-prilozheniya.md` | находка | места тестов в репозитории приложения: слово проекта в конфиге, `test-path-markers.json` не гейт | `references/test-path-markers.json`, `scripts/waiver.py` | слово владельца дано 06.10 (D-0030) | дано 06.10 | `onboarding-hooks` |
| `findings/B-125-skripty-otkazyvayut-na-neizvestnom-flage-i.md` | находка | скрипты отказывают на неизвестном флаге: `env_probe.py` молча игнорирует флаг и логинится на стенде | `scripts/env_probe.py` | открыто | нет | — |
| `findings/20261021-test-stand-lease-waited-s-pod-nagruzkoj-fr-31.md` | находка | `test_stand_lease` «a free stand is taken without waiting» краснеет под нагрузкой: `waited_s == 0` меряет часы, не ожидание (FR-31; узел PC1-7) | `scripts/stand_lease.py` | открыто | нет | — |
| `findings/20261030-test-brief-pack-roles-k6-k9-krasnye-na-baze-reliza.md` | находка | `test_brief_pack_roles` K9 (`branch_accounting.py` не на карточке роли) и K6 (хэш `## Commands`) красные на базе 0.10.7 | `scripts/brief_pack.py`, `agents/qa-requirements-tester.md` | пачка 1, PC1-8 | нет | OH3-15; GW1-16 |
| `findings/20261030-a-k9-test-triage-control-perechen-ne-znaet-traceability-i-s7-pretriage.md` | находка | `test_triage_control` A-K9 красный: перепись не знает docstring в `traceability.py` и `s7_pretriage.py` | `scripts/tests/test_triage_control.py` | пачка 1, PC1-9 | нет | HF8-19 N1b |
| `findings/20261030-lint-ratchet-check-21-novyj-na-baze-reliza.md` | находка | `lint_ratchet --check` на базе 0.10.7: 21 новая находка | `tools/lint_ratchet.py`, файлы находок | пачка 1, PC1-10 | нет | SC2-37 фикс-раунд |
| `findings/20261030-test-read-json-380-382-i-p21-main-bolshe-60-strok-krasnye-na-baze.md` | находка | `test_read_json` G5 380/382 и P21 `main()` в 70 строк красные на базе 0.10.7 | `scripts/tests/test_read_json.py`, `scripts/project_decisions.py` | пачка 1, PC1-11 | нет | OH3-23; HF7 |
| `findings/20261101-test-run-suite-mine-pin-vremeni-fazy-flake.md` | находка, id — | `test_run_suite_mine`: пины времени фаз по реальным часам флейкают под нагрузкой (FR-31) | `scripts/tests/test_run_suite_mine.py` | пачка 1, PC1-12 | нет | PC1-7; SC2-45 |
| `findings/20261102-potolki-brief-pack-v-testah-plyvut-s-kazhdym-bajtom-brifa.md` | находка | пины потолков S5 в `test_brief_pack` дрейфуют с каждым байтом брифа: три перемера за вечер | `scripts/tests/test_brief_pack.py` | пачка 2, PC2-1 | нет | t-747, t-755, t-769 |
| `findings/20261104-testy-posle-svertki-changelog-chitayut-ne-svoyu-zapis.md` | находка | три теста после свёртки changelog проверяют непустой `CHANGELOG.md`, а не свою запись релиза | `scripts/tests/test_codex_tool_guidance.py`, `scripts/tests/test_role_policy_reads.py`, `scripts/tests/test_story_step_materialize.py` | пачка 2, PC2-2 | нет | t-1822 |
| `findings/20261105-hvosty-kritika-gm3-2-obshchie-helpery-priemki-s6-i-podpisi-byudzheta.md` | находка | хвосты критика GM3-2: общие хелперы приёмки S6 в тестах, фикстура K3, подписи бюджета брифа | `scripts/tests/story_run_common.py`, `scripts/brief_pack.py` | пачка 2, PC2-3 | нет | t-008, `github-move` GM3-2 |
| `findings/20261111-kanon-krasnyj-probe-by-code-povtor-obhoda-i-raspiska.md` | находка | канон красный: расписка пробы пишется на каждой публикации, повтор отвечает `already_probed`, два ключа без пина | `scripts/probe_by_code.py`, `scripts/tests/test_probe_by_code.py` | пачка 2, PC2-4 | нет | t-033, t-035 |
| `findings/20261111-kanon-krasnyj-freshness-s3-ne-registriruetsya.md` | находка | канон красный: после приёмки S2 диспатч S3 не зарегистрирован, тест падает исключением | `scripts/tests/test_story_run_freshness.py` | пачка 2, PC2-5 | нет | t-034, t-035; PC2-3 |
| `findings/20261111-kanon-krasnyj-brief-pack-brify-vyshe-potolka-6-kb.md` | находка | канон красный: брифы S5 и критика кода выше потолка 6 КБ, срез убирает обход человека и файлы кейсов | `scripts/brief_pack.py`, `scripts/tests/test_brief_pack.py` | пачка 2, PC2-6 | нет | t-034, t-035; PC2-1 |
| `findings/20261111-kanon-krasnyj-no-mr-entry-otvet-o-storone-vyklyuchaet-produkt.md` | находка | канон красный: собственный ответ о стороне выключает продукт по умолчанию | `scripts/story_run.py`, `scripts/tests/test_no_mr_entry.py` | пачка 2, PC2-7 | нет | t-034; `pre-code` PC1-3 |
| `findings/20261112-khrapovik-doors-only-brief-max-posle-pc2-6.md` | находка, id — | храповик `DOORS_ONLY_BRIEF_MAX` ужать до числа `REPORT K7` из лога CI после PC2-6; PC2-1 по дереву уже сделан | `scripts/tests/test_brief_pack_s5_plan.py` | пачка 3, PC3-1 | нет | t-056 N9; PC2-1, PC2-6 |
| `findings/20261112-nochnoj-prohod-krasnyj-probe-by-code-languages-300-s.md` | находка, id — | ночной прогон 43178152997 красный: `test_probe_by_code_languages.py` упёрся в 300 с (канон: 209,2 с); файл режется (N9 td-11c) и идёт «в процессе»; потолок не поднимается | `scripts/tests/test_probe_by_code_languages.py`, `scripts/slow_tests.json` | пачка 3, PC3-2 | нет (слово владельца 12.11.2026, td-11d F2) | td-11c §7 N9; FR-31 |

## Входящие

`findings/` этой кучки; их число и дату последней показывает `plans/PILES.md` (собирает `piles.py board`; карточку код не правит).
По теме в других кучках: `driver-controller/findings/B-214-sosedi-b-155-testovye-fayly-paketa.md` (медленные тесты),
`driver-controller/findings/B-293-golden-drayvera-t-301-n0-t-337.md` (golden драйвера).

## Вопросы владельцу

- нет (основание: «Решение владельца нужно: да» — 0 из 14 находок, дайджест t-712 п. 5; отсрочка B-307 «разбор после релиза» дана 03.10 и сама по себе вопросом не является).

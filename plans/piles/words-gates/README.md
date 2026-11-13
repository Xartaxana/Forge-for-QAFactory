# Слова человека и гейты S2–S4 (`words-gates`)

приоритет: П2 | фичи: F07, F16, F12, F08 | стенд: не нужен (CI + эталоны) | зона: `ai-packages/qa-factory/scripts/gate_preflight.py`, `scripts/gate_brief.py`, `scripts/stage_done.py`, `scripts/stage_guard.py`, `scripts/guard_pre_tool.py`, `scripts/hooklib.py`, `scripts/planning_contract.py`, `scripts/question_register.py`, `scripts/case_versions.py`, `scripts/claim_projector.py`

## Зачем

Человек отвечает фабрике словами на гейтах и в вопросах S2–S4; эти слова должны доходить до каждого читателя без искажения, а карточки гейтов — говорить человеку правду и не отдавать ему выбор, который принадлежит фабрике. Рядом живёт слой гардов: одна оболочка, один разбор команды, ни одного молчаливого прохода мимо охраны. После пачки слова человека читаются одним правилом, карточки гейтов называют причину своими словами, а гард не пропускает обход через оболочку.

## Что не так сегодня (факты)

- Гейт A показывает человеку то, что фабрика чинит сама, и предлагает выбор там, где решать фабрике (находки `findings/20261016-…`, `findings/20261027-…`, `findings/20261028-…`).
- Слова человека на `s1_review` и резюме дирижёра теряются или перефразируются (`findings/20261030-…`).
- Гард читает подстроку команды, а не слово оболочки; сегментаторов несколько (находки `findings/20261019-…`, `findings/20261020-…`).
- Строка плана, версия кейса и триаж S7 читаются несколькими правилами (узлы групп «планирование», «кейсы», «триаж»).
- Состав и источники: `docs/tasks/specs/reports/backlog-audit-20261101/mapping.md` §2 «words-gates/1».

## Пачки

| № | Что изменится для пользователя | Строки | Размер | Статус | Взял | Ветка | MR |
|---|---|---|---|---|---|---|---|
| 1 | слова человека доходят до читателей и не переспрашиваются, карточки гейтов не отдают человеку выбор фабрики, гард знает оболочку, планирование, требования, кейсы и триаж читаются одним правилом | B-365, B-387, B-388, B-292, B-358, B-362, B-278, B-279, B-368, B-403, B-349, B-351, B-433, B-434, B-436, B-453, B-270, B-286 | L+ (41 узел) | ожидает | — | — | — |

Статусы пачки: `ожидает` → `в работе` → `сдано` → `принято` → `закрыта`. Размер — по узлам: S ≤ 4 узлов,
M 5–9, L 10–15 (больше — две пачки). Взятая пачка заморожена: её файл правит только взявший, новое
по теме — файлом в `findings/`. Размер 41 узел — по решению пересборки бэклога 01.11.2026 (D3, 40–55 узлов).

## Бриф пачки 1

Начать с узлов с пометкой «перепроверить» (GW1-4, GW1-53, EP1-5, DC1-18, RD1-5): сверка с кодом сужает остальное. Стенд не нужен. Подробно — `batch-1-slova-i-gejty.md`, раздел «Бриф».

## Дороги

Читать по порядку: эта карточка → `batch-1-slova-i-gejty.md` → находки узла (колонка «id / файл» ниже) → строки `plans/BACKLOG.md` с id из «Строк» → код зоны по функциям из «Слов» → `docs/tasks/specs/reports/backlog-audit-20261101/mapping.md` (§1 строки узлов, §2 состав, §5 края).
Слова: `gate_preflight`, `gate_brief`, `check_stand`, `_choose_test`, `question_register`, `person_words`, `stage_guard`, `_resume_doors`, `hooklib`, `guard_pre_tool`, `planning_contract`, `case_versions`, `claim_projector`, `diff_pass`, `triage_row_for`; «слова человека», «карточка гейта», «сегментатор оболочки».
Не читать: код пакета вне зоны и старые пачки-источники (их закрывает отдельный шаг пересборки).

## Содержание

Снимок 01.11.2026; пути — от `ai-packages/qa-factory/`; суть строк и находок — из карточек пачек-источников. При расхождении авторитетны файлы пачек. Каждый id строки и каждый файл из `findings/` стоит здесь ровно один раз.

| id / файл | вид | суть (≤ 20 слов) | пути | статус | слово владельца | связи |
|---|---|---|---|---|---|---|
| **Гейты и слова** | | | | | | |
| `findings/20261016-gejt-a-pokazan-s-nechinennym-factory-fixable.md` | находка | гейт A показан с «6 вещами, которые фабрика ещё чинит сама» — подкласс вне `--apply-fixes` | `scripts/gate_preflight.py`, `scripts/story_run.py`, `scripts/critic_rollcall.py` | пачка 1, C3-17 | нет | — |
| `findings/20261030-perefraz-dirizhyora-menyaet-slova-cheloveka.md` | находка | резюме дирижёра на гейтах A и B меняет слова человека (TC-001 вместо TC-003) | `scripts/gate_brief.py`, `scripts/story_run.py` | пачка 1, C5-9 | нет | t-1605 #10 |
| `findings/20261030-slova-na-s1-review-ne-perehodyat-v-s1-gap-na-teh-zhe-istochnikah.md` | находка | слова на `s1_review` не доезжают до `s1_gap` об тех же источниках (TP1-10937) | `scripts/story_run.py` | пачка 1, C5-10 | нет | D-0043; t-1605 #12 |
| B-365 | строка | у `stand_identity.py --words` и `source_exclusions.py --revoke --words` нет файлового маршрута слов | `stand_identity.py`, `source_exclusions.py` | пачка 1, GW1-2 | нет | — |
| B-387 | строка | семь дверей в пяти файлах висят в PENDING детектора без строки бэклога | `tests/test_words_doors.py`, `person_words.py` | пачка 1, GW1-2 | нет | — |
| B-388 | строка | `person_words.door(for_person=True)` называет скрипт человеку и не вызывается вне тестов: убрать или переназначить | `person_words.py` | пачка 1, GW1-2 | нет | — |
| B-292 / `findings/B-292-teksty-cheloveku-posle-chasti-a-t-357.md` | строка + находка-остаток | тексты человеку после части A: ~11 подпунктов (а–к); (д) закрыт, (г) решено 03.10 | `stage_done.py`, `story_run.py`, `gate_brief.py`, `gate_preflight.py`, `waiver.py`, `readiness.py` | пачка 1, GW1-4; перепроверить; перечень подпунктов — в находке | (г) дано 03.10 | — |
| B-358 | строка | строка «the fix:» на карточке и инструкция исполнителю `apply` — одно поле `remedy.change`; разделить | `gate_preflight.py`, `gate_brief.py` | пачка 1, GW1-5 | нет | — |
| B-362 | строка | текст двери запуска без читаемого отчёта не предлагает «запустите ещё раз», когда повтор не поможет | `gate_preflight.py` | пачка 1, GW1-5 | нет | — |
| `findings/20261027-gate-check-stand-factory-owned-kak-vybor-cheloveka.md` | находка | `check_stand` превращает `missing` с владельцем `factory` в выбор человека «fix the stand first, or let the stage run» | `scripts/gate_preflight.py` | пачка 1, GW1-24 | нет | t-1365 Q2; FR-3 |
| `findings/20261028-gejt-a-skip-stroka-plana-tehnicheskoj-frazoj.md` | находка | строка плана `skip` (TS-13) подана жаргоном: не названы три непроверенных риска и чем они прикрыты | `scripts/gate_brief.py`, `scripts/gate_preflight.py` | пачка 1, GW1-28 | нет | GW1-29 |
| `findings/20261028-gejt-a-probnyj-test-otchyota-vybor-fabriki-cheloveku.md` | находка | пробный тест отчёта: фабрика отказывается выбирать при общем корне профилей и отдаёт человеку имя ключа конфига | `scripts/gate_preflight.py` (`_choose_test`) | пачка 1, GW1-28 | нет | GW1-24 |
| `findings/20261028-gejt-a-vetka-testov-pravki-fabriki-kak-vybor-cheloveka.md` | находка | две незакоммиченные правки в ветке тестов — собственные файлы фабрики, человеку предложено «закоммитить / спрятать / идти» | `scripts/gate_preflight.py` | пачка 1, GW1-30 | нет | GW1-24 |
| `findings/20261030-accept-po-integracii-ne-dohodit-do-pozdnej-stroki-s5-blocked-by-env.md` | находка | `accept` по пропуску интеграции не доходит до поздней строки S5: нужно поле `integration` на `blocked_by_env` | `scripts/gate_preflight.py`, `scripts/stand_gaps.py` | пачка 1, GW1-36 | да — подтвердить перенос остатка GW1-15 | GW1-15; HF1-9 |
| `findings/20261031-stroka-punkta-gejta-a-id-svobodnye-slova-bez-chitatelya.md` | находка | строка пункта гейта A `vcs-1: <слова>` не читается; свободные слова идут дирижёру под своим пунктом | `scripts/story_run.py`, `scripts/gate_preflight.py` | пачка 1, GW1-45 | нет | GW1-33, GW1-32 |
| `findings/20261031-gejt-a-stroka-voprosa-bez-registra-i-s-drugim-razdelitelem-ne-vidna.md` | находка | бродячая строка вопроса без регистра и с другим разделителем не видна (t-542 F8) | `scripts/question_register.py` | пачка 1, GW1-47 | нет | GW1-34 |
| `findings/20261031-plan-warnings-padaet-na-spiske-v-pole-i-mertvaya-zashchita-note.md` | находка | `plan_warnings` падает на списке в закрытом поле; мёртвый `getattr` (t-542 F12) | `scripts/planning_contract.py`, `scripts/gate_brief.py`, `scripts/story_run.py` | пачка 1, GW1-49 | нет | GW1-29 |
| `findings/20261101-ga-4-dg-2-krasnye-na-baze-ssylki-na-dokumenty.md` | находка | `test_gate_brief_attachments.py` GA-4 и DG-2 красные на базе релиза: ссылка на документ не найдена в карточке гейта A | `scripts/gate_preflight.py`, `scripts/gate_brief.py` | пачка 1, GW1-53; перепроверить по CI | нет | GW1-32 |
| `findings/20261020-slovo-s1-waiver-prohodit-stage-done-no-ne-kontroller-i-p13.md` | находка | слово `waiver.py --stage S1` проходит `stage_done`, но не контроллер; `stage_overrides` с цитатой отказа не доходит ни до кого | `scripts/waiver.py`, `scripts/source_preflight.py`, `scripts/controller.py` | пачка 1, CX2-18 | нет | — |
| B-278 | строка | гейт `collected_ids`: для не-pytest «не проверено» молчит; первая половина закрыта 07.10 по тексту | `gate_preflight.py`, `node_ids.py` | пачка 1, EP1-5; перепроверить | нет | — |
| B-279 | строка | гейт `live_check_demand`: без ключа `novelty` проходит как «не требуется»; нужно «не проверено» в Left with you | `gate_preflight.py` | пачка 1, EP1-5; перепроверить | нет | `report-delivery` |
| B-368 | строка | у `red_sandbox.verify` нет строки в `references/gate-registry.json`, хотя он выносит вердикт | `references/gate-registry.json` | пачка 1, PC1-6 | нет | — |
| B-403 | строка | комментарий и тексты называют несуществующую `story_run.ticket_freshness`; остаётся `phases/s8.md` §2b и три R11-текста | `skills/qa-story/phases/s8.md` | пачка 1, PC1-6; половина `s8.md` сделана узлом по гейту B (по тексту) — проверить по коду | нет | `live-runs` (гейт B) |
| `findings/20261101-odobrenie-gejta-a-ne-svyazyvaet-versii-kejsov.md` | находка | одобрение гейта A не связывает версии кейсов; правка байт одобренного кейса проходит молча (A8) | `scripts/controller.py`, `scripts/case_versions.py` | пачка 1, HF8-26 | нет | HF8-6 |
| **Охрана и сегментатор оболочки** | | | | | | |
| B-349 | строка | жёсткие ссылки обходят охрану границы: создание ссылки и запись по ссылке проходят без разрешения (серьёзность высокая) | `guard_app_under_test.py`, `guard_pre_tool.py` | пачка 1, OH1-1 | нет | — |
| B-351 | строка | `apply_patch` Codex с `Update File`, после которого файл пуст, не распознаётся как удаление (`_empties_existing_file`) | `guard_app_under_test.py` | пачка 1, OH1-1 | нет | — |
| B-433 | строка | shell-индирекция (heredoc, `echo` в `bash`, `eval`, `python -c`, git-алиасы) проходит мимо гейтов запуска и доставки | `hooklib.py`, `stage_guard.py`, `guard_pre_tool.py` | пачка 1, OH1-2 | нет | `stand-and-sources` (остатки форм) |
| B-434 | строка | один токенайзер и сегментатор оболочки для всех гейтов: три сегментатора, `shlex` в пяти местах, разбор `cd` | `hooklib.py`, `stage_guard.py`, `guard_pre_tool.py` | пачка 1, OH1-2 | смена данных — слово Lead | — |
| B-436 | строка | качество кода гарда тестов: `hooklib._scan` 107 строк, `elif`-цепь, мёртвая ветка, не закоммичен скрипт мутантов | `hooklib.py` | пачка 1, OH1-2 | нет | `live-runs` (гард тестов) |
| B-453 | строка | остатки мест тестов: `SHELL_EXPANSION` не знает extglob, `check()` 122 строки, повторный глоб, перезапись эталона | `test_path_grants.py` | пачка 1, OH1-2 | нет | `package-ci` (места тестов) |
| `findings/20261019-odna-tablitsa-shablonov-sekretov-dlya-garda-i-redaktora.md` | находка | шаблоны секретов в двух таблицах — гард записи и редактор сбора; нужно решение Lead о направлении ошибки гарда | `scripts/guard_secrets.py`, `references/collect-redaction.json` | пачка 1, OH1-8 | нет | `collect` (CL1-1) |
| `findings/20261031-resume-doors-mertvaya-dver-i-agent-id-bez-kavychek.md` | находка | `_resume_doors` — копия условий `resume` с мёртвой дверью для записи без агента и контрольной точки; `--agent-id` без кавычек в двух отказах | `scripts/stage_guard.py` | пачка 1, SC5-4 | нет | SC5-4, SC2-17, t-409 F-9c |
| `findings/20261031-strazh-prinimaet-kod-typescript-za-komandu-dostavki.md` | находка | гард принимает код TypeScript в heredoc за команду доставки gitlab: пять отказов; основная правка — OH3-22, здесь фикстуры и дверь | `scripts/stage_guard.py` | пачка 1, SC5-9 | нет | свод п. 7.3, t-1633 строка 18; OH3-22, OH3-32 в `onboarding-hooks/3` |
| `findings/20261031-tekst-otkaza-straza-nesyot-cifry-chuzhogo-tiketa.md` | находка | отказ гарда цитирует «20 rewrites on TP1-13797 cost 8,284 tokens» из `artifact-writers.json`: убрать числа чужого тикета | `references/artifact-writers.json`, `scripts/guard_pre_tool.py` | пачка 1, SC5-10 | нет | свод п. 7.5, t-1633 строка 35 |
| `findings/20261019-prefiltry-vne-scan-skleyka-podstanovki-i-obratnaya-kosaya-v-flage.md` | находка | гард читает подстроку, не слово оболочки: склейка подстановкой, `--p\re`, `find -exec`, метка хоста | `scripts/hooklib.py`, `scripts/stage_guard.py`, `scripts/host_adapter.py` | пачка 1, CX2-14 (частично: SC1-5 speed-cost/1) | нет | — |
| `findings/20261020-obrabotchiki-garda-fail-open-i-str-list-posle-cx1-20.md` | находка | обработчики гарда после CX1-20: fail-open на не-walker исключении, чтения `str(list)`, след одиночной ошибки | `scripts/guard_pre_tool.py`, `scripts/stage_guard.py`, `scripts/host_adapter.py` | пачка 1, CX2-16 | нет | — |
| **Планирование** | | | | | | |
| `findings/20261029-gejt-s3-nahodit-odnu-stroku-v-dva-prohoda.md` | находка | гейт S3 находит проблемы строки TS-2 в два прохода, вторую пишет после принятия: лишний диспатч доработки | `scripts/planning_contract.py`, `scripts/stage_done.py` | пачка 1, DC1-18; перепроверить | нет (П1 0.10.7 — решение Lead) | HF8-24, HF9-1, DC1-9 |
| `findings/20261027-coverage-delta-ne-klyuch-zaplatki-vopros-o-dannykh.md` | находка | `coverage_delta` не выражается ключом заплатки; прочтение, меняющее набор обязательств, оставляет записи старого | `scripts/planning_contract.py`, `references/question-branch-keys.json` | пачка 1, SC2-1 | нет | SC2-1, t-1270 A-3 |
| `findings/20261023-brief-pereraboty-i-ticket-changed-ne-nesyot-slovar-metok.md` | находка | бриф `ticket_changed`-починки и доработки S3 не несёт списки меток, хотя вложены только в окно 1 | `brief_pack.py`, `handoff.py`, `controller.py`, `phases/s3.md` | пачка 1, OH3-18 | нет | OH3-14, t-058 |
| `findings/20261019-zaimstvovaniya-iz-skilla-qa-verify-change.md` | находка | восемь заимствований из скилла qa-verify-change: края G1-2/G2-1/G2-3, узлы G2-6, G2-7, C3-28, два П3 | `ai-packages/qa-factory/handoffs/`, `scripts/planning_contract.py`, `agents/qa-case-designer.md` | пачка 1, G2-6, G2-7, C3-28 | да, 19.10 («класть сейчас») | C3-28 |
| **Требования** | | | | | | |
| `findings/20261027-diff-pass-pechataet-novyj-nomer-u-udalyonnoj-stroki.md` | находка | `diff_pass` нумерует удалённую строку по новому файлу: ссылка `diff:-` читается как старый номер | `scripts/diff_pass.py` | пачка 1, SC2-9 | нет | SC2-9, t-1308 F10 (а) |
| `findings/20261028-kontekst-bag-tiketa-prinyat-za-trebovanie.md` | находка | тестировщик требований принял описание бага (состояние ДО) из Context за требование и поднял блокер R-3 против AC-3 | `agents/qa-requirements-tester.md`, `references/coverage-design.md` | пачка 1, RC1-12 | «не в 0.10.5, в пачки» (28.10.2026) | Dev6 (TP2-2702), t-1553; P20, P23; FR-7 |
| `findings/20261101-claim-projector-chitaet-tolko-implementation-only.md` | находка | проектор читает `implementation_only`, а после F-4 критика S2 строку обязаны иметь и требования `current-code:` | `scripts/claim_projector.py` | пачка 1, G2-18 | нет | G2-12 |
| `findings/20261102-p11-isklyuchenie-pripisano-slovu-cheloveka.md` | находка | исключение скоупа подписано «решение человека», хотя человек правку в корзине не называл; исключение по слову цитирует слова | `scripts/branch_accounting.py`, `agents/qa-requirements-tester.md` | WG1-1 → release-next/1 (П1, слово владельца 02.11.2026) | нет | прогон LOCAL-1, разбор t-1666 П-11 |
| `findings/20261102-pustye-voprosy-gejta-a-i-svoj-propusk-kak-probel-cheloveku.md` | находка | вопрос, где ни один вариант ничего не меняет, не задаётся; свой пропуск фабрики не подаётся человеку как принимаемый пробел | `references/human-questions.md`, `scripts/gate_brief.py`, `scripts/question_register.py` | пачка 1, WG1-2 | нет | RN1-14, RN1-4; t-1671 Н-6, Н-17 |
| `findings/20261102-otvet-primenen-k-flagam-no-tekst-i-sosednie-ekzemplyary-ostalis-otkrytymi.md` | находка | ответ применён к флагам, но тексты в плане, кейсах и отчёте «открыт»; слово о пробеле стенда дошло не до всех экземпляров | `scripts/planning_contract.py`, `scripts/report_facts.py`, `scripts/story_run.py` | пачка 1, WG1-3 | нет | GW1-43, RN1-11; t-1671 Н-13, t-1672 П-12 |
| **Кейсы** | | | | | | |
| `findings/20261019-predusloviya-ruchnogo-keisa-cherez-realnyj-interfejs-testera.md` | находка | предусловие ручного кейса должно создаваться через интерфейс тестировщика: нет рецепта и записи среды — отказ с дверью | `scripts/s5_precheck.py`, `scripts/gate_preflight.py`, `scripts/contract.py`, `agents/qa-case-designer.md` | пачка 1, C3-28 | да, 19.10 («класть сейчас») | G2-6, G2-7 |
| `findings/20261101-sozdanie-versii-kejsa-teryaet-vtoruyu-oblast-s-odinakovymi-bajtami.md` | находка | два файла кейса с одинаковыми байтами в разных областях получают одну запись `create_version`; вторая область не закреплена | `scripts/case_versions.py` | пачка 1, HF8-27 | нет | HF8-6; SC5-15 |
| **Триаж** | | | | | | |
| `findings/20261030-case-defect-net-v-drajvere-verdikt-bez-ispolnitelya.md` | находка | `CASE_DEFECT` нигде не встречается в `story_run.py`: вердикт, требующий хода, без исполнителя на дороге драйвера | `scripts/story_run.py` | пачка 1, DC1-25 | нет | цикл S7 после фикса; критик S5b rest |
| `findings/20261028-s7-round-mozhet-poslat-rework-s5-bez-del.md` | находка | `Driver.s7_round` может отправить доработку S5 без дел и получить отказ контроллера | `scripts/story_run.py` | пачка 1, RH2-6 | нет | RH1-6, DC1-13 |
| B-270 | строка | остатки «один матч триажа»: exact-шаг `triage_row_for`, NEAR через `test`, литерал `MANUAL_BLOCK_MAX`, «manual manual check» | `scripts/contract.py`, `scripts/story_run.py` | пачка 1, RD1-5; перепроверить | нет | — |
| B-286 | строка | `s7-automator-to-analyst` — мёртвый контракт индекса; решить: убрать форму или объявить писателя и читателя | `handoffs/index.yaml` | пачка 1, RD1-5 | нет (решение Lead) | — |
| `findings/20261102-retro-mode-numbers-skip-v-dokumentah-i-retro-mode-words-bez-pisatelya.md` | находка | документы и контракты называют `retro_mode numbers\|skip` текущими; `retro_mode_words` без писателя; F-6 (i)(ii) | `handoffs/*.yaml`, `references/artifact-contract-*.md`, `references/templates/retro.md`, `skills/qa-story/phases/s8.md` | пачка 1, WG1-4 | нет | t-738 m-2, B-2; GW1-3 |
| `findings/20261102-b-306-command-i-change-zhivye-na-karte-gejta.md` | находка | ответы пробы `command` и `change` на карте гейта нежилые; двухходовый поток драйвера | `scripts/story_run.py`, `scripts/probe_answers.py` | пачка 1, WG1-5 | нет | t-701 F-4; RD1-4 |
| `findings/20261104-analogi-kritika-t-1752-f9-claim-readings-i-case-versions.md` | находка | `claim_readings` пишет «say what it was» на стори без диффа; проверка `case_versions` в `controller` не может сработать | `scripts/contract.py`, `scripts/controller.py` | пачка 1, WG1-6 | нет | RN1-11, RN1-20; t-1752 F9 |

## Входящие

`findings/` этой кучки; находку, не названную ни в одной пачке, называет `piles.py check --all` (е).
Каждая новая находка тем же ходом получает строку в пачке этой кучки, которую ещё не взяли, или указатель `перенос: <кучка>/…`
(`piles.py check` (е)); нет такой пачки — открывается следующая со статусом «ожидает».

## Вопросы владельцу

- нет открытых вопросов, перенесённых пересборкой; слово владельца 30.10.2026 о размерах (узел SC5-6) уже дано, подтвердить перенос остатка GW1-15 (узел GW1-36).

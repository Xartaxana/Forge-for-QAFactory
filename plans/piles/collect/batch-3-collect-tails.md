# Collect — пачка 3: хвосты критика пачки 2 (перенос при закрытии collect/2)

кучка: `collect` | статус: закрыта | взял: — | ветка: `pile/collect/batch-3` | MR: `855d4e5c` | стенд: не нужен | приоритет: П3 | issue: —

Открыта 28.10.2026 по D-0044 и слову владельца 28.10.2026 («если там мелкие хвосты, то перенеси их в ещё не взятые»): две строки «Остатков» пачки 2 (очереди критика t-1206 по CL2-1 и CL2-2),
которые в тексте пачки 2 названы «строками для пачки collect/3», перенесены сюда узлами CL3-1, CL3-2 перед закрытием пачки 2 (t-1554). Текст — дословно из «Остатков» пачки 2 (она заморожена).
Слово владельца 21.10.2026: kb-страницы про A14 — законный перенос в кучку kb; остальное — доделать. Пачка НЕ взята.

Правило готовности: пачка закрыта, когда каждый узел «принято», свидетели узлов — в журнале взявшего, живые
доказательства (FR-33) сделаны или переданы строкой в кучку «живые прогоны».

## Бриф

Цель: закрыть мелкие хвосты критика t-1206 — читатели и константы вокруг отпечатка пакета и редактора сбора. Исходные данные — строки «Остатков» `batch-2-collect-leftovers.md`
и находка `findings/20261020-tretij-recept-otpechatka-host-probe-i-a14.md`. CL3-1 касается `release_fingerprint.py`, `factory_manifest.py`, `host_probe.py`: открывать их вместе.

## Узлы

Исполнитель «designer → builder → critic» — кодовый узел; «builder» — узел-документ. Статусы:
`ожидает` → `в работе` → `сдано` → `принято` / `отклонено`.

| Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус |
|---|---|---|---|---|---|---|
| CL3-1 | П3 | Очередь критика t-1206 по CL2-1 (перенос из collect/2 «Остатки», слово владельца 28.10.2026): C1-5 kb-страницы `kb/02-architecture.xhtml:281`, `kb/04-onboarding-doctor.xhtml:308` описывают A14 как проверку штампа (AR-22, читатели вне переписи; страницы пишутся по-английски; kb/2 ведёт другой разработчик — править через кучку kb); C1-6 `factory_manifest.py:45, :53-57` читает текст OSError выжившего по префиксу — атрибут со списком при следующем открытии `release_fingerprint.py` (AR-18); C1-7 идиома «первые 10, потом (+k more)» скопирована дважды в этом диффе поверх шести копий — один выживший `cut_list(names, cap)`; C1-8 литерал `echo QA_FACTORY_PROBE_` пять раз в `host_probe.py` (:60, :105, :109, :164, :169) — одна константа; `skills/qa-doctor/SKILL.md:87` на `unverified` велит «report missing/correlation evidence» — роль отчитается неверно на unread (байтовый бюджет пинит `test_session_identity.py`); аналог фикс-раунда t-1166: строки `verify()` «manifest missing/unreadable» тоже печатаются под `DRIFT` | builder → critic | `scripts/factory_manifest.py`, `scripts/release_fingerprint.py`, `scripts/host_probe.py`, `skills/qa-doctor/SKILL.md`, `kb/02-architecture.xhtml`, `kb/04-onboarding-doctor.xhtml`, их тесты (список — по коду) | — | закрыта: перенесено 01.11.2026 → driver-hosts/2 |
| CL3-2 | П3 | Очередь критика t-1206 по CL2-2 (C2-4; перенос из collect/2 «Остатки», слово владельца 28.10.2026): `test_collect_redact.py` `leaves()`/`sweep()` (P48) — третий читатель листьев; пины начальной позиции для остальных регэкспов данных; строка пачки CL2-2 устарела (оба дефекта были закрыты до узла: (а) 8a1840cf, (б) `_units` с 7fe625b3 — дефект свежести диспетчера, калибровочный случай) | builder → critic | `scripts/tests/test_collect_redact.py`, `scripts/machine_facts.py` (только если пин требует) | — | закрыта: перенесено 01.11.2026 → driver-hosts/2 |
| CL3-3 | П1 | Находка `findings/20261030-sbor-tablica-naborov-ne-pokryvaet-papku-istorii.md` (F1 ревью t-1612): таблица наборов покрывает каждый файл истории, который читает расследование (таблица §2 ревью — перечень), код продукта исключён; тест-связка области `h`. Слово владельца 30.10.2026: «все какие нужно для расследования» | designer → builder → critic | `references/collect-sets.json`, `scripts/collect_pack.py`, их тесты | — | закрыта: перенесено 01.11.2026 → release-next/1 |
| CL3-4 | П1 | Находка `findings/20261030-priem-ne-chitaet-skipped-i-gaps-manifesta.md` (F2): план приёма печатает `skipped` по причинам и каждую строку `gaps` | builder → critic | `tools/collect_intake.py`, `tools/test_collect_intake.py` | — | закрыта: перенесено 01.11.2026 → driver-hosts/1 |
| CL3-5 | П1 | Находка `findings/20261030-sbor-plugin-version-istorii-ne-tam-chitaetsya.md` (F3): `plugin_version` истории из `run_mode.plugin_version`, фикстуры с настоящей формой | builder → critic | `scripts/collect_pack.py`, `scripts/tests/test_collect_pack.py` | — | закрыта: перенесено 01.11.2026 → release-next/1 |
| CL3-6 | П1 | Находка `findings/20261030-priem-chitaet-retro-po-tochnomu-zagolovku.md` (F4): проверка S9 фиксирует заголовок ретро, приём сопоставляет по префиксу, фикстура из настоящего ретро | designer → builder → critic | `tools/collect_intake.py`, `tools/test_collect_intake.py`, шаблон ретро и проверка S9 (список — по коду) | — | закрыта: перенесено 01.11.2026 → driver-hosts/1 |
| CL3-7 | П2 | Находка `findings/20261030-priem-ne-schitaet-kandidatov-po-golomu-imeni-skripta.md` (F5): кандидаты по голому имени скрипта пакета, текст причины | builder → critic | `tools/collect_intake.py`, `tools/test_collect_intake.py` | — | закрыта: перенесено 01.11.2026 → driver-hosts/2 |
| CL3-8 | П2 | Находка `findings/20261030-priem-ne-pechataet-razmeshchennye-elementy-v-plane.md` (F6): строка PLACED на размещённый элемент | builder → critic | `tools/collect_intake.py`, `tools/test_collect_intake.py` | — | закрыта: перенесено 01.11.2026 → driver-hosts/2 |
| CL3-9 | П1 | Находка `findings/20261030-sbor-transkripty-tolko-zavisshih-petli-ne-vidny.md` (F7): сборщик упаковывает транскрипты и историй с петлями (повторные диспатчи роли/стадии, исчерпанный лимит правок/окна, проход лимита словом человека). Слово владельца 30.10.2026: «да, брать»; поправка к D-0052 «только зависших» — запись в DECISIONS.md в очереди Lead | designer → builder → critic | `scripts/collect_stall.py`, `scripts/collect_pack.py`, их тесты | — | закрыта: перенесено 01.11.2026 → release-next/1 |
| CL3-10 | П2 | Находка `findings/20261030-redaktor-korotkij-sekret-raskryvaetsya-metkoj-v-kontekste.md` (F8): короткий секрет не раскрывается меткой в контексте | designer → builder → critic | `references/collect-redaction.json`, `scripts/machine_facts.py`, `scripts/tests/test_collect_redact.py` | — | закрыта: перенесено 01.11.2026 → driver-hosts/1 |
| CL3-11 | П2 | Находка `findings/20261030-sbor-neizvestnye-fajly-vsegda-pod-naborom-a.md` (F9): строка пропуска несёт набор по папке | builder → critic | `scripts/collect_pack.py`, `scripts/tests/test_collect_pack.py` | — | закрыта: перенесено 01.11.2026 → driver-hosts/2 |
| CL3-12 | П2 | Находка `findings/20261030-test-priema-pustoe-utverzhdenie-srez-0.md` (F10): пустое утверждение `[:0]` заменить настоящей проверкой | builder | `tools/test_collect_intake.py` | — | закрыта: перенесено 01.11.2026 → driver-hosts/2 |
| CL3-13 | П2 | Находка `findings/20261030-sbor-manifest-bez-mtime-istochnika.md` (F11): mtime источника в строках `files[]` | builder → critic | `scripts/collect_pack.py`, читатели манифеста (по карте), тесты | — | закрыта: перенесено 01.11.2026 → driver-hosts/2 |

## Ход

Журнал передачи Lead пачки, новые записи в конец: `<дата время> — <что сделано, диспатчи t-nnn, хэши>`.

- 28.10 — пачка открыта: две строки «Остатков» collect/2 положены узлами CL3-1, CL3-2 перед закрытием пачки 2 по слову владельца 28.10.2026 (t-1554).
- 30.10 — по D-0044 в пачку (ещё не взята) положены 11 находок ревью архива сбора (ревью `docs/tasks/specs/reviews/t-1611-qa-collect-archive-review.md`, диспатч t-1612): узлы CL3-3…CL3-13. Приоритет — отображение критичности ревью (major → П1, minor → П2), отображение сделал исполнитель. Слова владельца 30.10.2026 по F1 (CL3-3) и F7 (CL3-9) записаны в находках.
- 01.11 — закрыта по слову владельца 01.11.2026 (пересборка бэклога): открытые узлы → release-next/1, driver-hosts/1, driver-hosts/2

## Живые доказательства

| Что | Где | Статус |
|---|---|---|

## Остатки

# `SendMessage` агенту записи в статусе `incomplete` проходит, хотя контроллер говорит «no agent holds its context»

id: — | кучка: `onboarding-forge` | от: спека S3c релиза 0.10.7 (`docs/tasks/specs/r0107-s3c-sc2-17-19-38.md`, F-S3C-8 «Сосед `incomplete`», строка 294), 31.10.2026 | приоритет: П3 | кандидат наверх: нет

Что не так / что сделать: контроллер называет запись в статусе `incomplete` так: «it stopped with work left, not for a person's answer, so no agent holds its context; continue it with the retry packet `recover` prints» (`controller.py:5602-5604`, `_resume_status_problems`; `RESUMABLE = ("blocked", "paused")`, `:5549`: «`incomplete` is work left ... its agent is gone, its road is the retry»). По спеке S3c `SendMessage` такому агенту проходит гард: две стороны отвечают на один вопрос («можно ли продолжить этого агента») по-разному (AR-15, AR-25: у возвращённого состояния ход один; FR-42). Чего эта находка не знает: какая именно ветка `stage_guard` пропускает (по тексту `stage_guard.py:1152` `RESUMABLE_STOPPED` не содержит `incomplete`, то есть путь пропуска не найден чтением; спека S3c описывает его как факт, воспроизведения в этой находке нет). Что сделать: сначала воспроизведение (один вызов гарда на записи `incomplete` с `agent_id`: проходит или отказан, и какой дверью); затем узел: гард отказывает с дверью `recover` (retry-пакет) в тех же словах, что контроллер, либо контроллер перестаёт называть статус «без агента», если агент у записи есть. Взаимодействие с `--needs-author` и `retry_packets` (вариант (б) спеки S3c: решать в узле N1) оценить в самом узле.

Спека S3c предложила (а) очередь находкой (D-0044) и рекомендовала (а): этот файл и есть эта запись.

Свидетель: `docs/tasks/specs/r0107-s3c-sc2-17-19-38.md:294` (F-S3C-8); `ai-packages/qa-factory/scripts/controller.py:5549`, `:5602-5604` и `ai-packages/qa-factory/scripts/stage_guard.py:1057`, `:1152` на базе `3840246e`.

Принципы и правила: P22; FR-2, FR-42; AR-15, AR-25.

Решение владельца нужно: нет.

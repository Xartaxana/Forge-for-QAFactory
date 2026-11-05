# Измеритель хопов — остатки критика t-812 (FX-6) и двойники чтения транскриптов

id: — | кучка: `forge` | от: критик t-812 (`docs/tasks/specs/reviews/t-812-t-811-f5-2-n2.md`, FX-6 и §L-5 аналоги), записал Lead 15.10.2026 08:05 | приоритет: П3 | кандидат наверх: нет

## Что

После forge/5 F5-2 N2 (`tools/hop_metrics.py`, потоковый `transcripts.iter_lines`, `journal_keys.node_of`) остались:

1. **FX-6 критика t-812** (не блокируют слияние): вложенность > 3 в `hop_metrics._manifest_lines` и `lead_all`; `_count_by` —
   это `collections.Counter`; предупреждения печатают `key[1]` без `@label`; `NODE_RE` принимает хвостовой дефис
   (`forge/5/F5-`) — N3 пинит; пустой журнал читается как «cannot be read»; проба повторных записей в транскриптах воркеров
   (`tier_echo` счёт `=N` — та же переписанная запись под одним `uuid`, что Е32 спеки t-797, но на стороне воркера; не измерено).
2. **Двойники чтения транскриптов (ось 14, §L-5 t-797):** `usage_report.iter_assistant_turns` (`:376-381`: `session:requestId` →
   `uuid` → `session:None`, MAX только output) сводится на `transcripts.request_usages`; два glob-цикла
   `find_agent_transcript`/`find_agent_transcripts` (единичный = пакет из одного).
3. **Ось 13:** `hop_metrics._manifest_lines` повторяет правило остановки `dispatch_manifest._section_paths`.

## Куда

Строка F6-15 пачки `forge/batch-6-vhodyashchie-2.md` (D-0044).

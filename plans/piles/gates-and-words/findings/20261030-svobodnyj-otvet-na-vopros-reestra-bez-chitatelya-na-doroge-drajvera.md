# Свободный ответ на вопрос реестра на гейте A на дороге драйвера не имеет читателя: условные строки плана все уходят в skip, отчёт печатает сырой текст ветки

id: — | кучка: `gates-and-words` | от: ночной прогон 14857 на 0.10.6 (критик t-1605), 30.10.2026 | приоритет: П2 | кандидат наверх: нет

Что не так / что сделать: на гейте A человек ответил на Q3 словами («Q3: not confirmed by the owner - keep … open gaps»), а не буквой.
Читателя такого ответа на дороге драйвера нет: `work/question-answers.jsonl` содержит только Q1 и Q2; в плане строки с условием
«per Q3: a → automate api …; b → skip; not needed → skip» все разрешились в skip (`work/ledger.md` TS-5, TS-6), требование R-7 и
R-8/R-9 потеряны; отчёт называет Q3 «factory recorded no answer» и печатает сырой текст ветки (`test-report.md:71-78`, `:82-83`,
`:240-241`). Слова существовали. Спека узла: свободный ответ читает дирижёр (P22), а не код; код читает только буквы (P2). Когда слова
не буква, вопрос возвращается дирижёру, ответ записывается как буква или остаётся открытым пробелом, и строка плана не уходит
в skip по умолчанию (FR-59). Сторона дороги дирижёра — соседняя находка
`driver-controller/findings/20261030-doroga-dirizhyora-ne-zapisyvaet-otvety-cheloveka-na-voprosy-gejta.md` (DC1-19); учёт веток в плане — TQ1-20
(`test-code-quality/findings/20261029-skvoznoj-uchyot-vetok-ot-s2-do-otchyota.md`). Новое здесь — случай свободного текста на дороге драйвера.

Свидетель: `work/question-answers.jsonl` и `state/words/driver-gateA-1793326086985.txt` ночного прогона (стенд testproject1-dev-010);
`test-report.md:71-78`; `work/ledger.md` TS-5, TS-6; `docs/tasks/specs/reviews/t-1605-14857-night-vs-manual.md` строка #6.

Принципы и правила: P2, P20, P22; FR-8, FR-9, FR-12, FR-59; AR-24, AR-28.

Решение владельца нужно: нет.

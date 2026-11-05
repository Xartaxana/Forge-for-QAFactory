# Изолированный worktree билдера режется от `main`, а не от ветки пачки: каждый билдер пачки начинает с чужой базы и чинит её руками

id: — | кучка: `onboarding-forge` | от: Lead пачки hotfix-12586/1 (dev2), 23.10.2026 | приоритет: П2 | кандидат наверх: нет

Что не так: диспатч с `isolation: "worktree"` на пачку, у которой работа идёт на ветке `pile/<slug>/batch-<N>`, получает дерево `main` (в пачке hotfix-12586/1 —
`93b29079`), а не голову ветки пачки с уже влитыми узлами. Диспатч говорит «worktree вырезан от `pile/hotfix-12586/batch-1`, HF1-6 влит»; это неверно. Билдер
тратит ход на расхождение, а один раз и вовсе дубль патча. Три билдера пачки сообщили это в своих отчётах:

- t-061 (HF1-8): «BASE NOTE (reality differs from the dispatch): this branch was cut from `93b29079`, which is an ANCESTOR of `pile/hotfix-12586/batch-1`
  (`d9415063`), not the batch head ... I did not merge (F-8)»;
- t-062 (HF1-9): «Divergence from the dispatch: the worktree was cut from `main` (93b29079), not from `pile/hotfix-12586/batch-1`, so it did NOT hold HF1-1. I ran
  `git merge --ff-only pile/hotfix-12586/batch-1` ... before any edit»;
- t-065 (HF1-13): «It was cut from `main` ... `git merge --ff-only pile/hotfix-12586/batch-1` was refused by the permission layer ("Modify Shared Resources"); I then ran
  `git cherry-pick 986ba3a1` ... the coordinator merging this branch into the pile branch gets the HF1-6 patch twice (same content, different sha)»;
- t-064 (HF1-12): «the worktree was cut from `main` (93b29079), not from `pile/hotfix-12586/batch-1`; I fast-forwarded it (`git merge --ff-only ...`, tip f02f4e2a)».

Единственная защита сегодня — `tools/dispatch_gate.py:1768` (`push_before_launch_warn`): WARN, когда локальный `main` опережает `origin/main` (worktree режется от `origin/main`). Ветку
пачки она не знает: пачка живёт не в `main`, поэтому предупреждения нет. Обход «первым ходом `git merge --ff-only <ветка пачки>`» держится на дисциплине спеки; в одном случае
(t-065) слияние запретил слой разрешений, и результат — дубль патча.

Что сделать: (а) измерить, от чего режет worktree хост (источник базы: `origin/main` или HEAD главной сессии) — одна команда на пустом диспатче; (б) по результату — либо
`dispatch_gate` предупреждает, когда worktree-диспатч называет ветку `pile/…` (в `given:`/тексте) без строки первого хода «слить ветку пачки», либо ветка пачки
становится базой worktree (если хост позволяет); (в) в шаблон диспатча билдера на пачку — первая строка «`git merge --ff-only pile/<slug>/batch-<N>`» с запасным
ходом при отказе слоя разрешений (сообщить Lead, а не `cherry-pick`). Тест: `tools/test_dispatch_gate*.py` — worktree-диспатч с именем ветки пачки и без строки слияния даёт WARN.

Свидетель: отчёты `docs/tasks/handoffs/t-061-hf1-8.md` (шапка), `t-062-hf1-9.md` (шапка), `t-064-hf1-12.md` (Reality note), `t-065-hf1-13.md` («Spec divergence (reality vs the dispatch)»);
`tools/dispatch_gate.py:1768-1789`.

Принципы и правила: правило 4 `CLAUDE.md` (параллельные специи), PROJECT.md «Командная работа» п. 1 (ветка пачки от `origin/main`), P12.

Решение владельца нужно: нет.

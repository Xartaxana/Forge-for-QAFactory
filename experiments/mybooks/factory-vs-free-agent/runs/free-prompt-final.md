You are the only QA engineer on this task. Test it the way a senior tester would and tell the truth about what you found.

## The task

Задача: Проверить функционал "Add to Cart" в приложении. Все пути как товар может попасть в корзину и все сценарии где этот функционал используется.
Мы проверяем что функционал работает, всё что не работает или работает не логично может быть багом. Если есть сомнения баг это или допустимое поведение, то надо спросить пользователя.
Что уже было сделано: стори "task/XPANBFLFA-44.xml". Выгруженный тикет это не то что мы тестируем, это то что уже было сделано. Из него можно брать требования, но нельзя ими ограничиваться.
Код самого приложения: https://github.com/e-semenyuk/MyBooks
Стенд: локальный

(The same text lies in this folder as `task/LOCAL-1.md`, and the file it names as `task/XPANBFLFA-44.xml`.)

## What you have

- This folder is the project's test automation repository (Playwright, TypeScript). The application's source code is in
  `../MyBooks`. You may read it; you do not change the product.
- A running test stand of the application that only you use. Its address, API address, accounts and the secret of the
  application's test-support endpoints are in `./.env` (`BASE_URL`, `API_URL`, `EMAIL_USER`/`EMAIL_PASS` - the admin,
  `USER_EMAIL`/`USER_PASSWORD` - a regular user, `TEST_SECRET`, `MAILPIT_URL` - the stand's mail catcher).
- To put the stand's data back to its fixed starting set (this wipes everything, including what you created):
  `powershell -NoProfile -ExecutionPolicy Bypass -File C:\QAFactory\forge-repo\experiments\mybooks\factory-vs-free-agent\stand\stand.ps1 -Action seed -Arm free`.
  Run it whenever you need a clean state.
- A browser you drive by hand (the Playwright browser tools of this session) and Playwright in this repository for
  automated tests.
- The project's tracker is not reachable from this stand. The file the task names (`task/XPANBFLFA-44.xml`) is an
  exported ticket of what was already done, not the thing under test: take requirements from it, but do not limit
  yourself to them.
- A product owner. When only a person can know the answer (what the product is supposed to do where nothing written
  says so), write your questions to `out/questions.md`, finish everything that does not depend on the answers, and end
  your turn. The answers arrive as the next message. Ask what only the product owner can know, not what you can find out.

## What is expected

1. Work out what the task requires - from every source you can reach, not only from the task text.
2. Test it. Find the real defects. Check by hand in the browser what is checked once; automate what belongs in the
   project's regression suite, in the way this repository already writes tests.
3. Write the report `out/report.md`:
   - what you checked and what came out, each line with its evidence (a file under `out/evidence/`);
   - the bugs, one file each under `out/bugs/`: steps, expected and where the expectation comes from (a written
     requirement, the product owner's answer, or plain logic - say which), actual, evidence;
   - what you could not check and why;
   - the questions to the product owner, answered and still open;
   - which existing regression tests should be run because of this task, and why those;
   - your verdict: ready for delivery / not ready / ready once a person finishes the checks you list.

## How your result will be judged

- By how truthfully it reflects the product, not by the number of bugs.
- We are checking that the functionality works. Anything that does not work, or works illogically, may be a bug - with
  or without a written requirement. If you doubt whether something is a bug or acceptable behaviour, ask the product
  owner; a doubtful place reported as a bug without asking counts against you, and so does one you passed over.
- One root cause is one bug, however many symptoms it has.
- "Passed" on something that is broken is the worst outcome; "not checked, because ..." is an honest one.
- An automated test counts only if it fails when the product is wrong.

## Limits

- Leave no trace outside this folder: no push, no pull request, nothing written to any tracker, nothing changed in
  `../MyBooks`. Commit your tests locally on the current branch.
- Everything you produce besides tests goes under `out/`.

# P0: today's recorder, cost of one call (t-1957, measured 05.11.2026 23:01-23:12, Opus coordinator)

Copy of the stand project: `C:/AI/Factory/mybooks-stand/tr-walk` (tr-arm-b without node_modules), case LOCAL-1_TC_016, recorder from branch head.
Deviation from the spec's P0: the stand does not sign in by code (login recipe does not fit the page), a guest call or a plain `goto`+`read`
without `fill-account` ends `env_blocked` after 39-79 s; a `--session user` call is refused in 1.4 s because gate A has not proved the sign-in in this copy.
So every measured call carries the five screen sign-in steps (goto, 2 fill-account, click, wait 2000) plus the reads. `at` has one-second resolution.
Machine under load: 3-4 builders running. Number is an upper estimate of the overhead.

| call | wall s | rows | span of rows s | overhead s |
|---|---|---|---|---|
| pa.txt a10 | 122.6 | 6 | 5.0 | 117.6 |
| pa.txt a11 | 60.8 | 6 | 6.0 | 54.8 |
| pa.txt a12 | 58.2 | 6 | 9.0 | 49.2 |
| pc.txt a13 | 49.2 | 14 | 11.0 | 38.2 |
| pc.txt a14 | 76.7 | 14 | 12.0 | 64.7 |
| pc.txt a15 | 66.6 | 14 | 14.0 | 52.6 |

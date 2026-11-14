- the stand sign-in roads keep the stand's recorded norm: `stand_access.py --roads` and `project_decisions.py stand-login` carry `environment.access.unauth_status` (and any key that is
  no sign-in key of the old road) onto the road they write, so the liveness check still reads the project's own "answers 404/405/429, that is alive" codes; the road written is the
  real access, never the display form; a road with no key names takes the stand block's `user_key` / first `secret_keys` entry, as the probe does
- a login answer of 400/422 on the local sign-in that names no body field now reads as an unknown (`unjudged`), not as a refused account; one that names a field it was sent still
  reads as `credentials_refused`; the token-endpoint sign-in keeps its row
- `stand_health.py`: a recorded code that is no HTTP code on an HTTP sign-in contradicts the `ok` outcome (it no longer reads as proved by "the project's login command", which only
  the command road has); the stand question after a search that exited 0 says the recorded way did not sign in when checked again; the onboarding roads run is not triggered by
  `none` / `ui_only`

- project's way of getting more test accounts and walker data (`config.json` `manual.accounts_way`, `manual.data_way`; `config_contract.walk_supply`): the
  person's words about how the project gets more accounts and which records walkers may share or make are kept whole in config, with
  the fields the conductor maps from them (sign-up roles, env-file key names, a lane limit per role, record pools, the data-change
  answer); one reader returns them shape-checked, never raises, drops a secret-looking value without printing it, and reads
  anything but one of the three data-change sentences as `existing_only` and not known; record kinds that differ only in case or
  surrounding spaces are merged into one (their `existing` lists joined, the first request kept); three question prices
  (`s6.walk_supply`, `s6.walk_account`, `s6.data_change`) and three conductor rows (merge on write) carry the way to record them
  (t-2174 TR3-10b)

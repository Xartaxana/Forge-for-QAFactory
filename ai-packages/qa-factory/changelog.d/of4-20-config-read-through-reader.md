- the app card reads the config's `test_data` through `config_contract.test_data_states`: a key recorded as unknown (`unknown`, `TBD`, `?`) is
  named "not set", no longer printed as a value; the scheduler's parallel defaults are read through `read_config_file`, so a config with
  a byte-order mark gives its own parameters instead of silently the defaults, and a config holding a list gives the declared defaults
  instead of a traceback (OF4-20)

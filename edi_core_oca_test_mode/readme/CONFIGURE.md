1. Open *EDI > Configuration > EDI Backend Types* and tick
   *Test Mode Supported* on the types whose transport offers a test
   environment (connector modules usually set this in their data).
2. Open the backend and enable *Test mode*. A warning banner reminds
   you exchanges will use the test configuration.
3. Fill in the transport-specific test parameters (e.g. the *Test
   environment* group provided by `edi_storage_oca_test_mode`).

To extend test mode to your own parameters, whitelist the field names
in `_edi_test_conn_param_fields()` and provide matching `test_<name>`
fields; `get_conn_parameter()` resolves them automatically when test
mode is on, falling back to the live value when empty.

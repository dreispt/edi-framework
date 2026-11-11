Enable *Test mode* on a supported backend: all connection parameters
resolved through `edi.backend.get_conn_parameter()` switch to their
`test_` counterparts. Disable it to return to the live configuration —
nothing is rewritten, so toggling is instant and safe.

Databases restored from a neutralized dump already have test mode
enabled on every backend.

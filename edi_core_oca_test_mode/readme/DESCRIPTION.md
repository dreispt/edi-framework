This module adds a generic **test mode** to `edi.backend`.

When enabled, the backend resolves test-specific connection parameters
instead of the live ones, so exchanges never reach live trading partners
by accident. Support is declared per backend *type* (*Test Mode
Supported* on `edi.backend.type`); the backend form then shows a
*Test mode* toggle and a warning banner while active.

What "test" means is transport-specific: each connector whitelists the
parameters that have a test counterpart (`test_<name>` fields) via
`_edi_test_conn_param_fields()` and resolves them through
`edi.backend.get_conn_parameter()`.

`edi_storage_oca_test_mode` provides the file-storage implementation
(test directories and an alternate test `fs.storage`).

Copied or neutralized databases are safe by default:
`data/neutralize.sql` enables test mode on every backend.

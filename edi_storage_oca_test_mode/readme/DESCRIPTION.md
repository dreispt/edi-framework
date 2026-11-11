Test environment support for file-storage EDI backends
(`edi_storage_oca`), on top of `edi_core_oca_test_mode`.

When *Test mode* is enabled on a backend, every file operation —
polling, directory moves, sends and reads — resolves the test
counterparts instead of the live configuration:

- `test_storage_id` — an alternate `fs.storage` (different host,
  port, credentials)
- `test_input_dir_*` / `test_output_dir_*` — alternate directories,
  each falling back to its live counterpart when empty

The *Test environment* group on the backend Storage page holds these
fields and only appears for backend types with test mode supported.

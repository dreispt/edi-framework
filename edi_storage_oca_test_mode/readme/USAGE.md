With *Test mode* on, incoming files are polled from the test input
directory, outgoing files are written to the test output directory,
and done/error moves use the test directories — all on the test
storage when `test_storage_id` is set. Toggling test mode off restores
the live configuration instantly; nothing is rewritten.

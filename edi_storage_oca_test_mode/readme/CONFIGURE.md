1. Make sure the backend type has *Test Mode Supported* ticked
   (provided by `edi_core_oca_test_mode`).
2. On the backend's Storage page, fill the *Test environment* group:
   - `test_storage_id` — only when test files live on a different
     SFTP/FS account; otherwise leave empty to reuse the live storage
   - `test_*_dir_*` — only the directories that differ from live
     (empty falls back to the live value)
3. Enable *Test mode* on the backend.

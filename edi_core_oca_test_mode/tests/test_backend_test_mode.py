# Copyright 2026 Odoo Community Association (OCA)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.edi_core_oca.tests.common import EDIBackendCommonTestCase


class TestBackendTestMode(EDIBackendCommonTestCase):
    def test_test_mode_supported_from_type(self):
        """Backends expose the test-mode support declared on their type."""
        self.assertFalse(self.backend.test_mode_supported)
        self.backend.backend_type_id.test_mode_supported = True
        self.assertTrue(self.backend.test_mode_supported)

    def test_conn_parameter_returns_live_value(self):
        """Parameters outside the whitelist resolve to live values in test mode."""
        self.backend.test_mode = True
        self.assertEqual(self.backend.get_conn_parameter("name"), self.backend.name)

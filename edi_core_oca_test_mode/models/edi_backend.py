# Copyright 2026 Odoo Community Association (OCA)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class EDIBackend(models.Model):
    _inherit = "edi.backend"

    test_mode = fields.Boolean(
        help="Use this backend's test configuration instead of live partners."
    )
    test_mode_supported = fields.Boolean(
        related="backend_type_id.test_mode_supported",
    )

    def get_conn_parameter(self, name, operation=None):
        """Return the effective value of a connection parameter.

        In test mode, whitelisted fields resolve to their ``test_``
        counterpart when set (``test_<name>``), falling back to the
        live value. Extend ``_edi_test_conn_param_fields`` to whitelist
        more parameters; ``operation`` optionally identifies the
        exchange flow for parameters that differ per operation.
        """
        self.ensure_one()
        test_name = "test_" + name
        if (
            self.test_mode
            and name in self._edi_test_conn_param_fields()
            and test_name in self._fields
        ):
            return self[test_name] or self[name]
        return self[name]

    def _edi_test_conn_param_fields(self):
        """Connection parameter field names eligible for test_ overrides."""
        return []

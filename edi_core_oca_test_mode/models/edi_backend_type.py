# Copyright 2026 Odoo Community Association (OCA)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class EDIBackendType(models.Model):
    _inherit = "edi.backend.type"

    test_mode_supported = fields.Boolean(
        help="Whether backends of this type can run in test mode.",
    )

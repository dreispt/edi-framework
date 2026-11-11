# Copyright 2026 Odoo Community Association (OCA)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "EDI Storage Test Mode",
    "summary": """
    Test environment support for file-storage EDI backends.
    """,
    "version": "19.0.1.0.0",
    "development_status": "Beta",
    "license": "LGPL-3",
    "website": "https://github.com/OCA/edi-framework",
    "author": "Odoo Community Association (OCA)",
    "depends": ["edi_core_oca_test_mode", "edi_storage_oca"],
    "data": [
        "views/edi_backend_views.xml",
    ],
}

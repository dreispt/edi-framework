# Copyright 2026 Odoo Community Association (OCA)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "EDI Backend Test Mode",
    "summary": """
    Run EDI backends against their test environment instead of live partners.
    """,
    "version": "19.0.1.0.0",
    "development_status": "Beta",
    "license": "LGPL-3",
    "website": "https://github.com/OCA/edi-framework",
    "author": "Odoo Community Association (OCA)",
    "depends": ["edi_core_oca"],
    "data": [
        "views/edi_backend_views.xml",
        "views/edi_backend_type_views.xml",
        "data/neutralize.sql",
    ],
    "demo": [
        "demo/edi_backend_demo.xml",
    ],
}

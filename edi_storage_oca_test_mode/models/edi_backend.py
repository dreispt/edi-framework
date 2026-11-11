# Copyright 2026 Odoo Community Association (OCA)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging

from odoo import fields, models

from odoo.addons.edi_storage_oca import utils

_logger = logging.getLogger(__name__)


class EDIBackend(models.Model):
    _inherit = "edi.backend"

    test_storage_id = fields.Many2one(
        string="FS Storage (test)",
        comodel_name="fs.storage",
        help="Storage to use in test mode; falls back to the live storage when empty.",
        ondelete="restrict",
    )
    test_input_dir_pending = fields.Char(
        "Input pending directory (test)",
        help="Path to folder for pending operations in test mode. "
        "Falls back to the live directory when empty.",
    )
    test_input_dir_done = fields.Char(
        "Input done directory (test)",
        help="Path to folder for doneful operations in test mode. "
        "Falls back to the live directory when empty.",
    )
    test_input_dir_error = fields.Char(
        "Input error directory (test)",
        help="Path to folder for error operations in test mode. "
        "Falls back to the live directory when empty.",
    )
    test_output_dir_pending = fields.Char(
        "Output pending directory (test)",
        help="Path to folder for pending operations in test mode. "
        "Falls back to the live directory when empty.",
    )
    test_output_dir_done = fields.Char(
        "Output done directory (test)",
        help="Path to folder for doneful operations in test mode. "
        "Falls back to the live directory when empty.",
    )
    test_output_dir_error = fields.Char(
        "Output error directory (test)",
        help="Path to folder for error operations in test mode. "
        "Falls back to the live directory when empty.",
    )

    def _edi_test_conn_param_fields(self):
        # Whitelist the storage connection params: the FS storage
        # record itself plus all *_dir_* fields.
        return super()._edi_test_conn_param_fields() + [
            "storage_id",
            "input_dir_pending",
            "input_dir_done",
            "input_dir_error",
            "output_dir_pending",
            "output_dir_done",
            "output_dir_error",
        ]

    def _storage_check_pending_input(self, **kw):
        # Resolve storage and dirs through get_conn_parameter so test
        # mode picks the test_* values.
        self.ensure_one()
        if not self.get_conn_parameter("storage_id") or not self.get_conn_parameter(
            "input_dir_pending"
        ):
            _logger.info(
                "%s ignored: no storage and/or input directory specified.", self.name
            )
            return False

        exchange_types = self.env["edi.exchange.type"].search(
            self._storage_exchange_type_pending_input_domain()
        )
        for exchange_type in exchange_types:
            # NOTE: this call might keep hanging the cron
            # if the remote storage is slow (eg: too many files)
            # We should probably run this code in a separate job per exchange type.
            file_names = self._storage_get_input_filenames(exchange_type)
            _logger.info(
                "Processing exchange type '%s': found %s files to process",
                exchange_type.display_name,
                len(file_names),
            )
            for file_name in file_names:
                self._storage_create_record_if_missing(exchange_type, file_name)
        return True

    def _storage_get_input_filenames(self, exchange_type):
        full_input_dir_pending = exchange_type._storage_fullpath(
            self.get_conn_parameter("input_dir_pending")
        ).as_posix()
        if not exchange_type.exchange_filename_pattern:
            # If there is not pattern, return everything
            filenames = [
                x
                for x in utils.list_files(
                    self.get_conn_parameter("storage_id"),
                    full_input_dir_pending,
                )
                if x.strip("/")
            ]
            return filenames

        bits = [exchange_type.exchange_filename_pattern]
        if exchange_type.exchange_file_ext:
            bits.append(r"\." + exchange_type.exchange_file_ext)
        pattern = "".join(bits)
        return [
            x
            for x in utils.find_files(
                self.get_conn_parameter("storage_id"),
                pattern,
                full_input_dir_pending,
            )
            if x.strip("/")
        ]

    def _storage_new_exchange_record_vals(self, file_name):
        return {
            "exchange_filename": file_name,
            "edi_exchange_state": "input_pending",
            "storage_id": self.get_conn_parameter("storage_id").id,
        }

    def _storage_on_edi_exchange_done(self, exchange_record):
        # Same logic as the base implementation, with storage and dirs
        # resolved through get_conn_parameter for test mode.
        self.ensure_one()
        storage = exchange_record.backend_id.get_conn_parameter("storage_id")
        if exchange_record.direction != "input" or not storage:
            return False
        if not self.get_conn_parameter("input_dir_done"):
            return False
        file_name = exchange_record.exchange_filename
        pending_dir = exchange_record.type_id._storage_fullpath(
            self.get_conn_parameter("input_dir_pending")
        ).as_posix()
        done_dir = exchange_record.type_id._storage_fullpath(
            self.get_conn_parameter("input_dir_done")
        ).as_posix()
        error_dir = exchange_record.type_id._storage_fullpath(
            self.get_conn_parameter("input_dir_error")
        ).as_posix()
        res = utils.move_file(storage, pending_dir, done_dir, file_name)
        if not res and self.get_conn_parameter("input_dir_error"):
            res = utils.move_file(storage, error_dir, done_dir, file_name)
        return res

    def _storage_on_edi_exchange_error(self, exchange_record):
        # Same logic as the base implementation, with storage and dirs
        # resolved through get_conn_parameter for test mode.
        self.ensure_one()
        storage = exchange_record.backend_id.get_conn_parameter("storage_id")
        if exchange_record.direction != "input" or not storage:
            return False
        if not self.get_conn_parameter("input_dir_error"):
            return False
        file_name = exchange_record.exchange_filename
        pending_dir = exchange_record.type_id._storage_fullpath(
            self.get_conn_parameter("input_dir_pending")
        ).as_posix()
        error_dir = exchange_record.type_id._storage_fullpath(
            self.get_conn_parameter("input_dir_error")
        ).as_posix()
        return utils.move_file(storage, pending_dir, error_dir, file_name)

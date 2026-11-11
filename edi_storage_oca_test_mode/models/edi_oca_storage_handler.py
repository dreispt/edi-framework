# Copyright 2026 Odoo Community Association (OCA)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging
from pathlib import PurePath

from odoo import models
from odoo.exceptions import UserError

from odoo.addons.edi_storage_oca import utils

_logger = logging.getLogger(__name__)


class EdiOcaStorageHandler(models.AbstractModel):
    _inherit = "edi.oca.storage.handler"

    def send(self, exchange_record):
        # Same logic as the base implementation, with the storage
        # resolved through get_conn_parameter for test mode.
        result = self.check(exchange_record)
        if not result:
            # all good here
            return True
        filedata = exchange_record.exchange_file
        path = self._get_remote_file_path(exchange_record, "pending")
        utils.add_file(
            exchange_record.backend_id.get_conn_parameter("storage_id"),
            path.as_posix(),
            filedata,
        )

    def _dir_by_state(self, backend, direction, state):
        # Same logic as the base implementation, with the directory
        # resolved through get_conn_parameter for test mode.
        assert direction in ("input", "output")
        assert state in ("pending", "done", "error")
        return PurePath(
            (backend.get_conn_parameter(direction + "_dir_" + state) or "")
            .strip()
            .rstrip("/")
        )

    def _get_remote_file(
        self,
        exchange_record,
        state,
        filename=None,
        binary=False,
        raise_if_missing=False,
    ):
        # Same logic as the base implementation, with the storage
        # resolved through get_conn_parameter for test mode.
        path = self._get_remote_file_path(exchange_record, state, filename=filename)
        try:
            # TODO: support match via pattern (eg: filename-prefix-*)
            # otherwise is impossible to retrieve input files and acks
            # (the date will never match)
            return utils.get_file(
                exchange_record.backend_id.get_conn_parameter("storage_id"),
                path.as_posix(),
                binary=binary,
            )
        except FileNotFoundError:
            _logger.info(
                "Ignored FileNotFoundError when trying "
                "to get file %s into path %s for state %s",
                filename,
                path,
                state,
            )
            if raise_if_missing:
                raise
            return None
        except OSError as err:
            _logger.warning(
                "OSError when trying to get file %s into path %s for state %s: %s",
                filename,
                path,
                state,
                err,
            )
            if raise_if_missing:
                raise UserError(
                    self.env._(
                        "Storage error while reading %(path)s: %(error)s",
                        path=path.as_posix(),
                        error=str(err),
                    )
                ) from err
            return None

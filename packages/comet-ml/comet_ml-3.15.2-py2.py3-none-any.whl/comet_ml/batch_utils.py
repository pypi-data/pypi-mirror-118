# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at http://www.comet.ml
#  Copyright (C) 2015-2021 Comet ML INC
#  This file can not be copied and/or distributed
#  without the express permission of Comet ML Inc.
# *******************************************************

import json
import logging

import six

from ._typing import Any, Dict, List, Optional
from .messages import RemoteAssetMessage
from .utils import compact_json_dump, get_time_monotonic

LOGGER = logging.getLogger(__name__)


class Batch(object):

    """
    The Batch object contains a list of anything and manage the size of the batch, isolating the
    logic about the max size and max time for a batch
    """

    def __init__(self, max_batch_size, max_batch_time):
        self.batch = []  # type: List[Any]
        self.on_upload_callbacks = []  # type: List[Any]
        self.last_time_created = get_time_monotonic()

        self.max_batch_size = max_batch_size
        self.max_batch_time = max_batch_time

    def _append(self, batch_item, on_upload=None):
        # type: (Any) -> None
        if len(self.batch) == 0:
            self.last_time_created = get_time_monotonic()

        self.batch.append(batch_item)

        if on_upload is not None:
            self.on_upload_callbacks.append(on_upload)

    def __len__(self):
        return len(self.batch)

    def should_be_uploaded(self):
        # type: () -> bool
        if len(self.batch) == 0:
            return False

        duration_since_last_created = get_time_monotonic() - self.last_time_created

        return (
            len(self.batch) >= self.max_batch_size
            or duration_since_last_created >= self.max_batch_time
        )

    def get_and_clear(self):
        # type: () -> List[Any]
        batch = self.batch
        self.clear()
        return batch

    def clear(self):
        self.batch = []

    def _get_payload(self):
        return self.batch

    def call_on_upload(self, *args, **kwargs):
        for callback in self.on_upload_callbacks:
            try:
                callback(*args, **kwargs)
            except Exception:
                LOGGER.debug(
                    "Error calling on_upload callback from a batch", exc_info=True
                )


class RemoteAssetsBatch(Batch):
    def append(self, remote_asset_message, additional_data=None, on_upload=None):
        # type: (RemoteAssetMessage, Optional[Dict[str, Any]], Any) -> None
        batch_item = {
            "assetId": remote_asset_message.additional_params["assetId"],
            "fileName": remote_asset_message.additional_params["fileName"],
            "link": remote_asset_message.remote_uri,
            "metadata": json.dumps(remote_asset_message.metadata),
            "overwrite": remote_asset_message.additional_params["overwrite"],
        }

        if remote_asset_message.additional_params.get("type") is not None:
            batch_item["type"] = remote_asset_message.additional_params["type"]

        if remote_asset_message.additional_params.get("step") is not None:
            batch_item["step"] = remote_asset_message.additional_params["step"]

        if remote_asset_message.additional_params.get("artifactVersionId") is not None:
            batch_item["artifactVersionId"] = remote_asset_message.additional_params[
                "artifactVersionId"
            ]

        if additional_data is not None:
            batch_item.update(additional_data)

        super(RemoteAssetsBatch, self)._append(batch_item, on_upload=on_upload)

    def get_payload(self):
        # type: (None) -> six.BytestIO
        payload = six.BytesIO()
        compact_json_dump({"remoteAssets": self.batch}, payload)
        return payload

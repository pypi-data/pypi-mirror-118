# encoding: utf-8
from typing import Optional
from labelci.core.index import Index
from labelci.core.client.client import DataHubClient
from labelci.common.exception.labelci_sdk_exception import ClientDoesNotExistError, ResourcesDoesNotExistError
import numpy as np
from PIL import Image
from io import BytesIO


class Tensor:
    def __init__(
            self,
            key: str,
            data: list,
            client: Optional[DataHubClient] = None,
    ):
        self.key = key
        self.data = data or []
        self.client = client
        self.file_cache = None

    def __getitem__(self, item):
        if self.key != "labels":
            if not self.client:
                raise ClientDoesNotExistError
            if not self.data[item]:
                raise ResourcesDoesNotExistError

            response_data = self.client.download_file(self.data[item])
            f = BytesIO(response_data)
            self.file_cache = f
            return self

        return self.data[item]

    def numpy(self):
        """file transform to numpy array format.
        """
        if not self.file_cache:
            return []
        return np.array(Image.open(self.file_cache))

    def bytes(self):
        """return BytesIO object
        """
        if not self.file_cache:
            return b""
        return self.file_cache

    def remove_file_cache(self):
        self.file_cache = None

    def update_labels(self):
        """update labels
        """

        pass

import gzip
import math
import os
from datetime import datetime, timedelta

import zstandard as zstd
from django.utils import timezone

from sentry.nodestore.base import NodeStorage


class FSNodeStorage(NodeStorage):
    compressor = zstd.ZstdCompressor()
    decompressor = zstd.ZstdDecompressor()

    def __init__(self, base_path="/data/nodestore/"):
        self.base_path = base_path

    def _get_path(self, id):
        return os.path.join(self.base_path, id[:2], id[2:4], id[4:])

    def _decompress(self, data):
        if data[:2] == b'\x1f\x8b':
            return gzip.decompress(data)
        return self.decompressor.decompress(data)

    def delete(self, id):
        try:
            os.remove(self._get_path(id))
        except FileNotFoundError:
            pass
        self._delete_cache_item(id)

    def delete_multi(self, id_list):
        for id in id_list:
            try:
                os.remove(self._get_path(id))
            except FileNotFoundError:
                pass
        self._delete_cache_items(id_list)

    def _get_bytes(self, id):
        try:
            with open(self._get_path(id), 'rb') as fp:
                data = fp.read()
            return self._decompress(data)
        except FileNotFoundError:
            return None

    def _set_bytes(self, id, data, ttl=None):
        path = self._get_path(id)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        data = self.compressor.compress(data)
        with open(path, "wb") as f:
            f.write(data)

    def cleanup(self, cutoff_timestamp):
        total_seconds = (timezone.now() - cutoff_timestamp).total_seconds()
        days = math.floor(total_seconds / 86400)

        today = datetime.today()
        for root, directories, files in os.walk(self.base_path, topdown=False):
            for name in files:
                path = os.path.join(root, name)
                if os.path.isfile(path):
                    filetime = os.stat(path).st_mtime
                    if filetime < (today - timedelta(days=days)).timestamp():
                        os.remove(path)

        if self.cache:
            self.cache.clear()

    def bootstrap(self):
        # Nothing for Django backend to do during bootstrap
        pass

import numpy as np

from base_spider import BaseSpider


class DatasetSpider(BaseSpider):

    random_idx = False

    def __init__(self):
        self.random_idx = self.__class__.random_idx
        self.dataset = self.__class__.dataset
        self._idx = 0
        self._gen_ids()

    def _gen_ids(self):
        if self.random_idx:
            self._ids = np.random.choice(len(self.dataset), len(self.dataset), replace=False)
        else:
            self._ids = range(len(self.dataset))

    def get_idx(self):
        if self._idx >= len(self._ids):
            self._gen_ids()
            self._idx = 0
        idx = self._ids[self._idx]
        self._idx += 1
        return idx

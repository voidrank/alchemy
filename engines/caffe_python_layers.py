import os
from multiprocessing import Process
import cPickle
import redis
import time

import config

import caffe

import config

class AlchemyDataLayer(caffe.Layer):

    wait_time = 1
    process_num = 2

    def setup(self, bottom, top):
        assert len(bottom) == 0
        assert len(self.__class__.spider.attr) == len(top)
        self.process_num = self.__class__.process_num
        self.max_cache_item_num = self.__class__.max_cache_item_num
        self.wait_time = self.__class__.wait_time
        self.processes = []

        self.redis = redis.Redis()
        self.redis.delete(config.solver_prototxt)

        for _ in range(self.process_num):
            self.processes.append(Process(target=self.fetch, args=(self.spider(),)))
            self.processes[_].start()
        

    def fetch(self, spider):
        while True:
            item_dict = spider.fetch()
            item = []
            for attr_name in spider.attr:
                item.append(item_dict[attr_name])
            while self.redis.llen(config.solver_prototxt) >= self.max_cache_item_num:
                time.sleep(self.wait_time)
            self.redis.rpush(config.solver_prototxt, cPickle.dumps(item, cPickle.HIGHEST_PROTOCOL))



    def reshape(self, bottom, top):
        while self.redis.llen(config.solver_prototxt) == 0:
            print 'waiting for spider...', self.redis.llen(config.solver_prototxt)
            time.sleep(0.2)

        self.item = cPickle.loads(self.redis.lpop(config.solver_prototxt))
        item = self.item

        for i in range(len(item)):
            top[i].reshape(*item[i].shape)

    def forward(self, bottom, top):
        item = self.item
        for i in range(len(item)):
            top[i].data[...] = item[i]


    def backward(self, bottom, propagate_down, top):
        pass

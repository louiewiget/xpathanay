#encoding: utf-8

import Queue

import logging

from DB import DB
from SchemeEntity import SchemeEntity


class CrawlerLoader(object):

    def loadMap(self, dbCluster, id=None):
        db = DB(dbCluster)
        self.queue = Queue.Queue()

        varsList = SchemeEntity().getVars()
        sql = "select %s from yq_crawler_scheme" % ",".join(varsList)
        if id is not None:
            sql += " where id = %s" % id
        ret, datas = db.query(sql)
        for one in datas:
            scheme = {}
            entity = SchemeEntity()
            tupleLength = len(one)
            for i in xrange(0, tupleLength):
                setattr(entity, varsList[i], one[i])
            self.queue.put(entity)

    def getQueue(self):
        return self.queue


if __name__ == "__main__":
    crawlerLoader = CrawlerLoader()
    crawlerLoader.loadMap()

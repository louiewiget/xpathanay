#encoding: utf-8

import logging
import hashlib
import time
import threading

from DB import DB

from BaseAppender import BaseAppender

class DbAppender(BaseAppender):

    BATCH_CNT = 100

    def __init__(self, DbCluster):
        self.db = DB(DbCluster, False)
        self.cnt = 0
        self.lock = threading.Lock()

    def perform(self, title, url, date, element):
        sign = self.getSign(title, url ,date)
        t = time.time()
        sql = "insert into yq_crawler_store (`site_name`, `category_name`, `title`," + \
              " `url`, `date`, `signature`, `create_time`, `update_time`) " + \
                "values('%s', '%s', '%s', '%s', '%s', '%s', %s, %s)" + \
                "on duplicate key update update_time = values(`update_time`)"
        sql = sql %  (DB.es(element.getSiteName()), DB.es(element.getCategoryName()), \
                 DB.es(title), DB.es(url), date, sign, t, t)
        self.lock.acquire()
        ret, data = self.db.query(sql)

        if ret != False:
            self.db.commit()
            """
            if self.cnt >= BATCH_CNT:
                self.db.commit()
                self.cnt = 0
            """
        else:
            logging.warning("execute db failed sql[%s]" % sql)
        self.lock.release()

    def getSign(self, title, url, date):
        src = title + url + date
        return hashlib.md5(src).hexdigest()

    def finish(self):
        pass
        # self.db.commit()

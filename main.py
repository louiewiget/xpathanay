#encoding: utf-8

"""add by guminli"""

import log

from BaseAppender import BaseAppender
from DbAppender import DbAppender
from CrawlerLoader import CrawlerLoader
from XpathAnaylize import XpathAnaylize


if __name__ == "__main__":
    THREAD_NUM = 10
    DB_CLUSTER = 'cae03'
    log.init_log("./log/news_crawer")
    crawlerLoader = CrawlerLoader()
    crawlerLoader.loadMap(DB_CLUSTER)
    executorList = []
    appender = DbAppender(DB_CLUSTER)
    for i in xrange(0, THREAD_NUM):
        anaylizer = XpathAnaylize(crawlerLoader.getQueue())
        anaylizer.setAppender(appender=appender)
        anaylizer.start()
        executorList.append(anaylizer)
    for executor in executorList:
        executor.join()

#encoding: utf-8

import sys

import log

from BaseAppender import BaseAppender
from DbAppender import DbAppender
from CrawlerLoader import CrawlerLoader
from XpathAnaylize import XpathAnaylize



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print 'plz provide scheme id in database'
        sys.exit(-1)
    debug = False

    if len(sys.argv) >= 3:
        if sys.argv[2] == 'debug':
            debug = True
    DB_CLUSTER = 'cae03'
    log.init_log("./log/debug_crawer")
    crawlerLoader = CrawlerLoader()
    crawlerLoader.loadMap(DB_CLUSTER, sys.argv[1])
    executorList = []
    appender = BaseAppender()
    anaylizer = XpathAnaylize(crawlerLoader.getQueue())
    anaylizer.setDebug(debug)
    anaylizer.setAppender(appender=appender)
    anaylizer.start()

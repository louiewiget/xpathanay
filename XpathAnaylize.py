#encoding: utf-8
import time
import threading
import logging
import Queue
import re
import time
import sys
import urllib
reload(sys)
sys.setdefaultencoding('utf-8')

import traceback

import lxml.html.soupparser as soupparser
import lxml.etree as etree

import BeautifulSoup

from CrawlerLoader import CrawlerLoader
from SchemeEntity import SchemeEntity
from PageLoader import PageLoader

import utils

class XpathAnaylize(threading.Thread):

    def __init__(self, queue):
        """
        print type(queue)
        if isinstance(queue, Queue.Queue):
            raise Exception("not a valid queue type")
        """
        threading.Thread.__init__(self);
        self.queue = queue
        self.debug = False

    def setAppender(self, appender):
        self.appender = appender

    def setDebug(self, value):
        self.debug = value

    def run(self):
        if not hasattr(self, "queue"):
            logging.warning("xpath anaylize queue is not ready")
            raise Exception("xpath anaylize queue is not ready")

        while not self.queue.empty():
            try:
                element = self.queue.get_nowait()
                try:
                    pageContent = PageLoader().loadUrl(element.getCategoryUrl())
                    pageContent = pageContent.decode(element.getEncoding())
                except Exception as e:
                    logging.warning("load page and try decode from [%s] fail[%s]" % (element.getEncoding(), e.message))
                    continue
                try:
                    self.anaylize(pageContent, element)
                except Exception as e:
                    logging.warning("anaylize page fail[%s][%s]" % (e.message, traceback.format_exc()))

            except Exception as e:
                print traceback.format_exc()
                logging.warning("missing a error [%s]" % e.message)
                break
        self.appender.finish()

    def anaylize(self, page, element):
        """ titleXpath 被 ; 号分隔， 第一位元素为 标题的 xpath, 其余待扩展"""
        titleXpath = element.getTitleXpath().split(";")
        """ urlXpath 被 ; 号分隔， 第一位元素为 url 的xpath 路径，第二位为分离 url 的正则表达式， 第三位为组装 url 的规则"""
        urlXpath   = element.getUrlXpath().split(";")
        """ dateXpath  被 ; 号分隔， 第一位元素为 date 的xpath 路径，第二位为 strptime 时间规则"""
        dateXpath  = element.getDateXpath().split(";")
        categoryUrl = element.getCategoryUrl()
        pageNoParam = categoryUrl[0:categoryUrl.find("?")]
        varDict = {"$host":categoryUrl, "$page":categoryUrl, "$pageNoParam": pageNoParam, "$siteUrl": element.getSiteUrl()}
        if self.debug:
            logging.info("DEBUG: prefix[%s] url[%s]" % (element.getXpathPrefix(), element.getCategoryUrl()))
            utils.write_log(urllib.quote_plus(element.getCategoryUrl()), page);
        if len(dateXpath) < 2:
            dateXpath.append("%Y-%m-%d")
        dom = soupparser.fromstring(page, BeautifulSoup.BeautifulSoup)

        try:
            areas = dom.xpath(element.getXpathPrefix())
        except Exception as e:
            logging.warn("xpath failed[%s][%s][%s]" % (element.getCategoryUrl(), element.getXpathPrefix(), e.message))
        if self.debug:
            print "find areas [%s]" % len(areas)
        for area in areas:
            if self.debug:
                print etree.tostring(area)
            titleRet = area.xpath('%s' % (titleXpath[0]))
            if len(titleRet) < 1:
                logging.warning("title xpath has no result[%s]" % titleXpath[0])
                continue
            title = titleRet[0].strip()

            urlRet = area.xpath(urlXpath[0])
            if len(urlRet) < 1:
                logging.warning("url xpath has no result[%s]" % urlXpath[0])
                continue
            url = urlRet[0].strip()

            dateRet = area.xpath(dateXpath[0])
            if len(urlRet) < 1:
                logging.warning("date xpath has no result[%s]" % dateXpath[0])
                continue
            dateRaw = dateRet[0].strip()

            if len(urlXpath) > 1:
                p1 = urlXpath[1]
                pattern = re.compile(p1)
                result = pattern.findall(url)
                if len(result) >= 1:
                    url = result[0]
                varDict["$result"] = url
                if len(urlXpath) > 2:
                    matchString = urlXpath[2]
                    for k, v in varDict.iteritems():
                        matchString = matchString.replace(k, v)
                    url = matchString
            date = time.strptime(dateRaw, dateXpath[1])
            dateStr = "%s-%s-%s" % (date.tm_year, date.tm_mon, date.tm_mday)
            self.appender.perform(title, url, dateStr, element)

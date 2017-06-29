#encoding: utf-8

import requests
import commands
import os
import logging

class PageLoader(object):


    def loadUrl(self, url, loader):
        try:
            funcStr = "loadUrlBy" + loader
            loaderHandler = getattr(self, funcStr)
            return loaderHandler(url)
        except Exception as e:
            logging.warning("loader[%s]  is not exists, using default Requests instead[error:%s]" % (loader, e))
            return self.loadUrlByRequests(url)

    def loadUrlByRequests(self, url):
        headers = { "Accept":"text/html,application/xhtml+xml,application/xml;",
            "Accept-Encoding":"gzip",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
            }
        try:
            r = requests.get(url=url, headers=headers)
            if r.status_code == 200:
                return r.content
        except Exception as e:
            logging.warn("request url[%s] exception, except = [%s]" % (url, e.message))
        return None

    def loadUrlByPhantomjs(self, url):
        if not url.startswith("http"):
            url = "http://%s" % url
        cmd = "phantomjs loadPage.js \"%s\"" % url
        logging.info(cmd)
        pipe = os.popen(cmd, "r")
        output = pipe.read()
        status = pipe.close()
        return output

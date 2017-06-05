#encoding: utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class BaseAppender(object):

    def perform(self, title, url, date, element):
        print ("[%s-%s] %s %s %s" % (element.getSiteName(), element.getCategoryName(), title, url, date))

    def finish(self):
        print 'done'

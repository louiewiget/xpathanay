#encoding: utf-8

class SchemeEntity(object):

    def __init__(self):
        self.site_name = ""
        self.category_name = ""
        self.category_url = ""
        self.xpath_prefix = ""
        self.title_xpath = ""
        self.url_xpath = ""
        self.date_xpath = ""
        self.encoding = ""

    def getSiteName(self):
        return self.site_name

    def getCategoryName(self):
        return self.category_name

    def getCategoryUrl(self):
        return self.category_url

    def getXpathPrefix(self):
        return self.xpath_prefix

    def getTitleXpath(self):
        return self.title_xpath

    def getUrlXpath(self):
        return self.url_xpath

    def getDateXpath(self):
        return self.date_xpath

    def getVars(self):
        return vars(self).keys()

    def getEncoding(self):
        return self.encoding

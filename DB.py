import MySQLdb
import ConfigParser
import logging


class DB(object):
    def __init__(self, cluster, use_transaction=True):
        self.use_transaction = use_transaction
        self.cluster = cluster
        conf = ConfigParser.ConfigParser()
        conf.read("conf/db.conf")
        if conf.has_section(cluster):
            host = conf.get(cluster, 'host')
            user = conf.get(cluster, 'user')
            passwd = conf.get(cluster, 'passwd')
            port = conf.getint(cluster, 'port')
            db = conf.get(cluster, 'database')
            self.conn = MySQLdb.connect(host, user, passwd, db, port, charset="utf8")
            self.cur = self.conn.cursor()
            if use_transaction:
                self.cur.execute('begin')
                self.rollback = False

    def begin(self):
        self.cur.execute('begin')

    def query(self, sql):
        data = ''
        ret = False
        try:
            ret = self.cur.execute(sql)
            data = self.cur.fetchall()
        except Exception as e:
            logging.warning("mysql error:[%s]" % e)
        return ret, data

    def commit(self):
        self.cur.execute("commit")

    def rollback(self):
        self.rollback = True

    @staticmethod
    def es(string):
        return MySQLdb.escape_string(string)

    def __del__(self):
        try:
            if self.use_transaction:
                if self.rollback:
                    self.cur.execute('rollback')
                else:
                    self.cur.execute("commit")
            self.cur.close()
            self.conn.close()
        except Exception as e:
            logging.warning('%s'%e)

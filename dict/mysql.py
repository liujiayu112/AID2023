"""
    数据操作模块
    思路：
        将数据库操作封装一个类
        将 dict_server 需要的数据库操作功能分别写成方法，在 dict_server 中实例化对象，需要什么方法直接调用
"""

import pymysql
import hashlib

SALT = "#&aAid_"  # 盐


class Database:
    def __init__(self,
                 host='192.168.7.220',
                 port=3306,
                 user='root',
                 passwd='Ljy_123.com',
                 charset='utf8',
                 database=None):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.database = database
        self.charset = charset
        self.connect_database()  # 连接数据库

    def connect_database(self):
        """
        连接数据库
        """
        self.db = pymysql.connect(host=self.host,
                                  port=self.port,
                                  user=self.user,
                                  passwd=self.passwd,
                                  database=self.database,
                                  charset=self.charset,
                                  )

    def close(self):
        """
        关闭数据库
        """
        self.db.close()

    def create_cursor(self):
        """
        生成游标
        """
        self.cur = self.db.cursor()

    def register(self, name, passwd):
        """
        注册操作
        :param name: 注册用户名
        :param passwd: 注册用户密码
        :return: True，False
        """
        sql = "select * from user where name='%s'" % name
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            return False  # 用户存在

        # 密码加密存储处理
        hash = hashlib.md5((name + SALT).encode())  # 算法加盐
        hash.update(passwd.encode())
        passwd = hash.hexdigest()

        # 插入数据库
        sql = "insert into user (name,passwd) values (%s,%s)"
        try:
            self.cur.execute(sql, [name, passwd])
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False

    def login(self, name, passwd):
        """
        登录操作
        :param name: 用户名
        :param passwd: 用户密码
        :return: True，False
        """
        hash = hashlib.md5((name + SALT).encode())  # 算法加盐
        hash.update(passwd.encode())
        passwd = hash.hexdigest()

        # 数据库查找
        sql = "select * from user where name='%s' and passwd = '%s'" % (name, passwd)
        self.cur.execute(sql)
        r = self.cur.fetchone()
        # 有数据运行登录
        if r:
            return True
        else:
            return False

    def query(self, word):
        """
        查单词
        :param word: 单词
        :return: 返回单词解释
        """
        sql = "select mean from words where word='%s'" % word
        self.cur.execute(sql)
        r = self.cur.fetchone()
        # 如果找到 r --> (mean)
        if r:
            return r[0]

    def insert_hist(self, name, word):
        """
        插入数据
        :param name: 用户名
        :param word: 单词名称
        """
        sql = "insert into history(name,word) values (%s,%s)"
        try:
            self.cur.execute(sql, [name, word])
            self.db.commit()
        except Exception:
            self.db.rollback()

    def history(self,name):
        """
        历史记录查询
        :param name: 用户名
        :return:
        """
        sql = "select name,word,time from history where name='%s' order by time desc limit 10" % name
        self.cur.execute(sql)
        return self.cur.fetchall()

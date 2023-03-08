"""
    数据操作模块
    思路：
        将数据库操作封装一个类
        将 dict_server 需要的数据库操作功能分别写成方法，在 dict_server 中实例化对象，需要什么方法直接调用
"""

import pymysql


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
        sql = "insert into user (name,passwd) values (%s,%s)"
        try:
            self.cur.execute(sql, [name, passwd])
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False

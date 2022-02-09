import json

import jsonpath
import pymysql
from config.read_ini import ReadIni


class MySQLClient(object):
    conn = None

    # 构造函数
    def __init__(self, host, user, password, db, charset="utf8", port=3306):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.charset = charset
        self.port = port

    # 连接数据库
    def connect(self):
        self.conn = pymysql.connect(host=self.host,
                                    port=self.port,
                                    user=self.user,
                                    password=self.password,
                                    db=self.db,
                                    charset=self.charset)
        # 创建游标
        self.cursor = self.conn.cursor()

    # 关闭数据库连接
    def close(self):
        self.cursor.close()
        self.conn.close()

    # 查询一条记录
    def get_one(self, sql, params=()):
        ret = None
        try:
            self.connect()
            self.cursor.execute(sql, params)
            ret = self.cursor.fetchone()
            self.close()
        except Exception as e:
            print(e)
        return ret

    # 查询所有记录
    def get_all(self, sql, params=()):
        list_data = None
        try:
            self.connect()
            self.cursor.execute(sql, params)
            list_data = self.cursor.fetchall()
            self.close()
        except Exception as e:
            print(e)
        return list_data

    def __edit(self, sql, params):
        count = 0
        try:
            self.connect()
            count = self.cursor.execute(sql, params)
            self.conn.commit()
            self.close()
        except Exception as e:
            print(e)
        return count

    # 插入
    def insert(self, sql, params=()):
        return self.__edit(sql, params)

    # 修改
    def update(self, sql, params=()):
        return self.__edit(sql, params)

    # 删除
    def delete(self, sql, params=()):
        return self.__edit(sql, params)


# if __name__ == '__main__':
#     sql = "select name,age from users;"
#     host = ReadIni("LOCAL_DB", "host")
#     user = ReadIni("LOCAL_DB", "user")
#     password = ReadIni("LOCAL_DB", "password")
#     db = ReadIni("LOCAL_DB", "db")
#     mysql_client = MySQLClient(host=host,user=user,password=password,db=db)
#     result = mysql_client.get_all(sql)
#     print(result)
#     # name = json.loads(result)
#     loc = "0,0"
#     loc = loc.split(',')
#     i = int(loc[0])
#     j = int(loc[1])
#     name = result[i][j]
#     print(name)




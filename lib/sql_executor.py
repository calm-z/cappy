from util.log import Logger
from util.sqlclient import MySQLClient
from config.read_ini import ReadIni


class SqlExecutor:
    def __init__(self, db):
        self.log = Logger().get_logger()
        self.host = ReadIni(db, "host")
        self.user = ReadIni(db, "user")
        self.password = ReadIni(db, "password")
        self.db = ReadIni(db, "db")
        self.mysql_client = MySQLClient(host=self.host, user=self.user, password=self.password, db=self.db)
        self.arg_dict = {}

    def sql_executor(self, dbAssert):

        for value in dbAssert:
            sql = value["sql"]
            result = self.mysql_client.get_all(sql)
            if "placeHolder" in value.keys():
                placeHolder = value["placeHolder"]
                for key, value in placeHolder.items():
                    loc = value.split(',')
                    i = int(loc[0])
                    j = int(loc[1])
                    self.arg_dict[key] = result[i][j]
        return self.arg_dict


# if __name__ == '__main__':
#     dbAssert = [
#         {
#             "sql": "select name,age from users;",
#             "placeHolder": {
#                 "name_0": "0,0",
#                 "name_1": "1,0"
#             }
#         },
#         {
#             "sql": "select name,age from users;",
#             "placeHolder": {
#                 "name_2": "0,0",
#                 "name_3": "1,0"
#             }
#         }
#     ]
#     executor = SqlExecutor("LOCAL_DB")
#     args = executor.sql_executor(dbAssert)
#     print(args)

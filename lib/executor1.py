import json
from util.log import Logger
from lib.re_executor import ReExecutor
from lib.sql_executor import SqlExecutor


class Executor:
    def __init__(self):
        self.log = Logger().get_logger()
        self.arg_dict = {}
        self.re_executor = ReExecutor(self.arg_dict)

    def execute1(self,data):
        try:
            self.log.debug("----------开始执行用例：{}----------".format(data["id"]))

            if "before" in data.keys():

                before = data["before"]
                if "dbAssert" in before:
                    if "database" in data.keys():
                        db = data["database"]
                    else:
                        raise IOError("未指定数据库，请检查用例")
                    sql_executor = SqlExecutor(db)
                    args = sql_executor.sql_executor(before["dbAssert"])
                    for key, value in args.items():
                        self.arg_dict[key] = value
                    self.log.debug("数据库元素记录成功：{0}".format(self.arg_dict))
                if "requests" in before:
                    requests = before["requests"]
                    self.re_executor.re_executor(requests)
            if "requests" in data.keys():
                requests = data["requests"]
                self.re_executor.re_executor(requests)
            else:
                self.log.error("没有找到requests，请检查用例")
            self.log.debug("----------用例{0}执行完毕----------".format(data["id"]))
            return "用例执行成功"

        except Exception as e:
            self.log.error(e)
            return "用例执行失败"

    def execute(self):
        data = json.load(open('casedata/data02.json'))
        print(type(data))
        #
        # print(casedata)
        # data1 = tuple(json.load(open('../casedata/data02.json')))
        # print(type(data1))
        # print(data1)
        try:
            for case in data:
                self.log.debug("----------开始执行用例：{}----------".format(case["id"]))

                if "before" in case.keys():

                    before = case["before"]
                    if "dbAssert" in before:
                        if "database" in case.keys():
                            db = case["database"]
                        else:
                            raise IOError("未指定数据库，请检查用例")
                        sql_executor = SqlExecutor(db)
                        args = sql_executor.sql_executor(before["dbAssert"])
                        for key, value in args.items():
                            self.arg_dict[key] = value
                        self.log.debug("数据库元素记录成功：{0}".format(self.arg_dict))
                    if "requests" in before:
                        requests = before["requests"]
                        self.re_executor.re_executor(requests)
                if "requests" in case.keys():
                    requests = case["requests"]
                    self.re_executor.re_executor(requests)
                else:
                    self.log.error("没有找到requests，请检查用例")
                self.log.debug("----------用例{0}执行完毕----------".format(case["id"]))
                print("一条用例结束后打印用例字典", self.arg_dict)

        except Exception as e:
            return self.log.error(e)


if __name__ == '__main__':
    Executor().execute()

import string

import jsonpath
import re
import pymysql
import json
import yaml


def replace_char(old_string, char1, char2):
    '''
        字符串按索引位置替换字符
        '''
    old_string = str(old_string)
    char2 = "json.load(open('" + char2 + "'))"
    # 新的字符串 = 老字符串[:要替换的索引位置] + 替换成的目标字符 + 老字符串[要替换的索引位置+1:]
    new_string = old_string[:72] + char2 + old_string[80:98] + char1 + old_string[105:]
    return new_string

def read_file():
    file = open("//case.yaml", "r", encoding="utf-8")
    case_file = yaml.load(file, Loader=yaml.FullLoader)
    print(case_file)
    case_data = []
    case_name = []
    for key,value in case_file.items():
        data = json.load(open(value))
        print(data)
        for i in data:
            case_name.append(i["id"])
            case_data.append(i)
    return case_data,case_name

class Viking():
    # def __init__(self):
    #     code = '''
    #         def dynamo(self, arg):
    #             """ dynamo's a dynamic method!
    #             """
    #             self.weight += 1
    #             print(self.weight)
    #             return arg * self.weight
    #         '''
    #     code_other = '''
    #         import pytest
    #         @pytest.mark.parametrize("casedata", casedata)
    #         def test_01(casedata):
    #             Executor().execute1(casedata)
    #         '''
    #     # char = "test_" + "aaa"
    #     code_other_new = replace_char(code_other, "test_" + "aaa","bbb")
    #     print(code_other_new)
    #     # self.weight = 50
    #     # code_new = replace_char(code, "aaa")
    #     # print(code_new)
    #     d = {}
    #     exec(code_other_new.strip(), d)
    #     setattr(self.__class__, 'aaa', d['aaa'])
    def ccc(self):
        code = '''
            def dynamo(self, arg):
                """ dynamo's a dynamic method!
                """
                self.weight += 1
                print(self.weight)
                return arg * self.weight
            '''
        code_other = '''
        import pytest
            @pytest.mark.parametrize("casedata", casedata)
            def test_01(casedata):
                Executor().execute1(casedata)
            '''
        # char = "test_" + "aaa"
        code_other_new = replace_char(code_other, "test_" + "aaa", "bbb")
        print(code_other_new)
        # self.weight = 50
        # code_new = replace_char(code, "aaa")
        # print(code_new)
        d = {}
        exec(code_other_new.strip(), d)
        setattr(self.__class__, 'aaa', d['aaa'])


if __name__ == "__main__":
    # v = Viking().ccc()
    # print(v.aaa(10))
    # print(v.aaa(10))
    # print(v.aaa.__doc__)
    print(read_file())

    # args = {"name": "admin", "openid": "abcdefg", "aaa": "111"}
    #
    # a = '{"code": "200", "msg": "Success Create", "casedata": {"name": "${name}", "openid": "${open_id033}"}, "ip": "61.50.119.242"}'
    # result = jsonpath.jsonpath(a,"$.codeee")
    # print(result)

    # pattern = re.compile(r"[$][{](.*?)[}]", re.S)
    # b = re.findall(pattern, a)
    # # print(b)
    #
    # list_ = re.finditer(pattern, a)
    # # for i in list_:
    # # print(i.group())
    #
    # # re.sub(pattern,args[""])
    #
    # for key, value in args.items():
    #     key_match = "\$\{" + key + "\}"
    #     print(key_match)
    #     a = re.sub(key_match, value, a)
    # print(a)
    #
    # db = pymysql.connect(host="localhost", user="root", password="qwer1234", database="user", charset="utf8mb4",
    #                      port=3306)
    # cursor = db.cursor()
    # select_sql = "select * from users;"
    # insert_sql = "INSERT INTO users(`name`,age,tel) VALUES('李娜',19,17718344206);"
    # update_sql = "UPDATE users SET `name`='李娜娜' WHERE `name`='李娜';"
    # delete_sql = "DELETE FROM users WHERE `name`='李娜娜';"
    # cursor.execute(select_sql)
    # result = cursor.fetchall()
    # print(type(result))
    # print(result)

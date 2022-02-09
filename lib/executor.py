import unittest
import ddt
from util.client.httpclient import HttpClient
import os
import jsonpath
import json

@ddt.ddt
class TestWMS02(unittest.TestCase):
    arg_dict = {}

    @ddt.file_data("../casedata/data01.json")
    def testcase(self, data):
        httpclient = HttpClient()

        for item in data:

            # 处理json数据文件中的格式化字符串
            # 将字典转换成字符串
            item = json.dumps(item)
            item = item % TestWMS02.arg_dict
            item = json.loads(item)
            ret = httpclient.send_request(method=item["method"],
                                    url=item["url"],
                                    params_type=item["params_type"],
                                    data=item["casedata"])
            self.assertEqual(item["assert_info"]["expect"], jsonpath.jsonpath(ret.json(), item["assert_info"]["getnode"])[0])
            #判断数据文件中是否有升级header的字段
            if item.get("updata_header"):
                for header_item in item["updata_header"]:
                    print(header_item)
                    for key, value in header_item.items():
                        # 将token永久加入当前会话的请求头当中，后学接口调用不在需要手动设置token
                        httpclient.session.headers.update({"{}".format(key):
                                                           jsonpath.jsonpath(ret.json(), "{}".format(value))[0]})

            if item.get("set_arg"):
                for arg_item in item["set_arg"]:
                    for key,value in arg_item.items():
                        TestWMS02.arg_dict[key]= jsonpath.jsonpath(ret.json(),
                                                                   value)[0]
            print(TestWMS02.arg_dict)
        httpclient.close_session()


if __name__ == '__main__':
    unittest.main()
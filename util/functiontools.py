import json
import re

import jsonpath
from util.log import Logger


class Tools:
    def __init__(self):
        self.log = Logger().get_logger()

    def AssertListEqual(self, list1, list2):
        return list1.sort() == list2.sort()

    def keysAssert(self, ret_text, assert_data):
        ret_text = json.loads(ret_text)

        for key, expect_value in assert_data.items():
            actual_value = jsonpath.jsonpath(ret_text, key)
            if actual_value:
                if expect_value == actual_value[0]:
                    self.log.debug("{0} 断言成功，{1} == {2}".format(key, expect_value, actual_value[0]))
                else:
                    # self.log.error("断言失败，{0} != {1}".format(expect_value,actual_value[0]))
                    raise AssertionError("断言失败，{0} != {1}".format(expect_value, actual_value[0]))
            else:
                raise AssertionError("断言失败，{0}不存在".format(key))

    def KeysExist(self, ret_text, keys_data):
        ret_text = json.loads(ret_text)

        for key in keys_data:
            actual_keys = jsonpath.jsonpath(ret_text, key)
            if actual_keys:
                self.log.debug("断言成功，{0} 存在".format(key))
            else:
                # self.log.error("断言失败，{0} 不存在".format(key))
                raise AssertionError("断言失败，{0} 不存在".format(key))

    def PlaceHolder(self, ret_text, keys_data):
        args = {}
        ret_text = json.loads(ret_text)
        for key, value in keys_data.items():
            value_1 = jsonpath.jsonpath(ret_text, value)
            if value_1:
                args[key] = value_1[0]
            else:
                raise ValueError("元素记录失败，{0} 不存在".format(key))
        return args

    # def params_replace(self, args, request):
    #     request = json.dumps(request)
    #     for key, value in args.items():
    #         key_match = "\$\{" + key + "\}"
    #         request = re.sub(key_match, str(value), request)
    #     return json.loads(request)

    def params_replace(self, args, request):
        for key, value in args.items():
            request = self.get_dict_allkeys(request, key, value)
        return request

    def get_dict_allkeys(self, dict_a, special_key, special_value):
        if isinstance(dict_a, dict):
            for key, value in dict_a.items():
                if isinstance(value, str):
                    value_ = value[2:-1]
                    if value_ == special_key:
                        dict_a[key] = special_value
                self.get_dict_allkeys(value, special_key, special_value)
        elif isinstance(dict_a, list):
            for k in dict_a:
                if isinstance(k, dict):
                    for key, value in k.items():
                        value_ = value[2:-1]
                        if value_ == special_key:
                            k[key] = special_value
                        self.get_dict_allkeys(value, special_key, special_value)
        return dict_a


if __name__ == '__main__':
    # ret_text = '{"code": "200", "msg": "Success Create", "casedata": {"name": "admin", "openid": "ee05c00110670eb569d9073af06bd1a0"}, "ip": "61.50.119.242"}'
    # body_assert = {'$.code': "200", '$.msg': 'Success Create', '$.casedata.name': 'admin',
    #                '$.casedata.openid': 'ee05c00110670eb569d9073af06bd1a0', '$.ip': '61.50.119.242'}
    tool = Tools()
    # tool.keysAssert(ret_text, body_assert)

    args = {'code': 200, 'msg': 'Success Create', 'name': 'admin', 'openid': 'ee05c00110670eb569d9073af06bd1a0',
            'ip': '61.50.119.242'}
    request = {'url': 'http://39.98.138.157:8008/asn/list/', 'desc': '这是第二个接口，请求接口获取返回值，并记录部分数据', 'method': 'post',
               'headers': {'token': '${openid}', 'code': '${code}'}, 'params': {}, 'body': {'creater': 'admin'},
               'status_code': 200,
               'placeHolder': {'id': '$.id', 'openid': '$.openid', 'asn_code': '$.asn_code', 'bar_code': '$.bar_code',
                               'creater': '$.creater'}, 'Assert': {'$.id': 4554, '$.openid': '${openid}'},
               'KeysExist': ['$.asn_code', '$.supplier', '$.bar_code', '$.asn_status', '$.total_weight'],
               'WaitTime': 1000}
    print(tool.params_replace(args, request))

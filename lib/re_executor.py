from util.client.httpclient import HttpClient
from util.log import Logger
from util.functiontools import Tools
import json
import jsonpath
from time import sleep


class ReExecutor:
    def __init__(self, arg_dict):
        self.log = Logger().get_logger()
        self.tool = Tools()
        self.arg_dict = arg_dict
        self.httpclient = HttpClient()

    def __del__(self):
        self.httpclient.close_session()

    def re_executor(self, re_data):

        for request in re_data:
            request = self.tool.params_replace(args=self.arg_dict, request=request)

            ret = self.httpclient.send_request(url=request["url"], method=request["method"], params_type="json",
                                               data=json.dumps(request["body"]), headers=request["headers"],
                                               params=request["params"])
            self.log.debug(
                "url:{0}，method:{1}，headers:{2}，body:{3}".format(ret.request.url, ret.request.method,
                                                                 ret.request.headers, ret.request.body))
            self.log.debug("response:{}".format(ret.text))
            if "WaitTime" in request.keys():
                self.log.debug("WaitTime：{0}".format(request["WaitTime"]))
                sleep(request["WaitTime"] / 1000)
            if "status_code" in request.keys():
                if ret.status_code == request["status_code"]:
                    self.log.debug("接口状态断言成功，{0} == {1}".format(request["status_code"], ret.status_code))
                else:
                    # self.log.error("接口状态断言失败，{0} != {1}".format(request["status_code"],ret.status_code))
                    raise AssertionError(
                        "接口状态断言失败，{0} != {1}".format(request["status_code"], ret.status_code))
            if "placeHolder" in request.keys():
                args = self.tool.PlaceHolder(ret_text=ret.text, keys_data=request["placeHolder"])
                for key, value in args.items():
                    self.arg_dict[key] = value
                self.log.debug("元素记录成功：{0}".format(self.arg_dict))

            if "Assert" in request.keys():
                self.tool.keysAssert(ret_text=ret.text, assert_data=request["Assert"])

            if "KeysExist" in request.keys():
                self.tool.KeysExist(ret_text=ret.text, keys_data=request["KeysExist"])


if __name__ == '__main__':
    r = [{'url': 'http://39.98.138.157:8008/login/', 'desc': '这是第一个接口，请求接口获取返回值，并记录部分数据', 'method': 'post',
          'headers': {}, 'params': {}, 'body': {'name': 'admin', 'password': '123456'}, 'status_code': 200,
          'placeHolder': {'code': '$.code', 'msg': '$.msg', 'name': '$.casedata.name', 'openid': '$.casedata.openid',
                          'ip': '$.ip'},
          'Assert': {'$.code': '200', '$.msg': 'Success Create', '$.casedata.name': 'admin',
                     '$.casedata.openid': 'ee05c00110670eb569d9073af06bd1a0',
                     '$.ip': '61.50.119.242'},
          'KeysExist': ['$.code', '$.msg', '$.casedata.name', '$.casedata.openid', '$.ip'], 'WaitTime': 1000},
         {'url': 'http://39.98.138.157:8008/asn/list/', 'desc': '这是第二个接口，请求接口获取返回值，并记录部分数据', 'method': 'post',
          'headers': {'token': '${openid}'}, 'params': {}, 'body': {'creater': 'admin'}, 'status_code': 200,
          'placeHolder': {'id': '$.id', 'asn_code': '$.asn_code', 'bar_code': '$.bar_code', 'creater': '$.creater'},
          'Assert': {'$.openid': '${openid}'},
          'KeysExist': ['$.id', '$.asn_code', '$.supplier', '$.bar_code', '$.asn_status', '$.total_weight'],
          'WaitTime': 1000}]
    ReExecutor().re_executor(r)

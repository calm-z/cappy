import requests
import json
from util.log import Logger


class HttpClient:
    """

    """
    def __init__(self):
        self.session = requests.session()

    def send_request(self, method, url, params_type="form", data=None, **kwargs):
        method = method.upper()
        params_type = params_type.upper()

        if isinstance(data, str):
            data = json.loads(data)

        if "GET" == method:
            response = self.session.request(method=method, url=url, data=data, **kwargs)
        elif method == 'POST' or method == 'PUT' or method == 'DELETE':
            if 'FORM' == params_type:
                response = self.session.request(method=method, url=url, data=data, **kwargs)
            elif 'JSON' == params_type:
                response = self.session.request(method=method, url=url, json=data, **kwargs)
        else:
            raise ValueError('request method "{}" error'.format(method))

        return response

    def __call__(self, method, url, params_type="form", data=None, **kwargs):
        return self.send_requests(method, url, params_type, data, **kwargs)

    def close_session(self):
        self.session.close()

if __name__ == '__main__':
    HttpClient().send_request(method="post",url="http://39.98.138.157:8008/login/",params_type='json',data='"name": "admin","password": "123456"')

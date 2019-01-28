# -*- coding = utf-8 -*-

import requests
from collections import OrderedDict


def _set_header_default():
    header_dict = OrderedDict()
    header_dict['Accept'] = '*/*'
    header_dict['Accept-Encoding'] = 'gzip, deflate, br'
    header_dict['Accept-Language'] = 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,en-US;q=0.6'
    header_dict['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    return header_dict

class HttpClient():
    def __init__(self):
        self.initSession()

        pass

    def initSession(self):
        self._s = requests.session()
        self._s.headers.update(_set_header_default())

    def send(self, url, data=None, **kwargs):
        if data:
            method = 'post'
        else:
            method = 'get'
        pass

# -*- coding=utf-8 -*-
import os

class CDNProxy:
    def __init__(self):
        pass

    def open_cdn_file(self):

        cdn = []

        path = os.path.join(os.path.dirname(__file__), './cdn_list')
        try:
            with open(path, "r", encoding="utf-8") as f:
                for i in f.readlines():
                    # print(i.replace("\n", ""))
                    if i and "kyfw.12306.cn:443" not in i:
                        cdn.append(i.replace("\n", ""))
                return cdn
        except Exception:
            with open(path, "r") as f:
                for i in f.readlines():
                    # print(i.replace("\n", ""))
                    if i and "kyfw.12306.cn:443" not in i:
                        cdn.append(i.replace("\n", ""))
                return cdn

if __name__ == '__main__':
    print(CDNProxy().open_cdn_file())

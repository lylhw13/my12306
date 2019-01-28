# -*- coding=utf-8 -*-

from collections import OrderedDict
import requests
from cdn_utils import CDNProxy
import random
from time import sleep


class MyQuery:
    def __init__(self):
        self.from_station = '南京'
        self.to_station = '洛阳'
        self.depart_date = '2019-01-31'
        self.base_url = ''
        self.url_query_by_train_no = 'https://kyfw.12306.cn/otn/czxx/queryByTrainNo'
        self.train_no = ''
        self.start_time_range = []
        self.arrive_time_range = []
        self.initSession()
        pass

    @classmethod
    def set_header_default(self):
        # header_dict = OrderedDict()
        # header_dict['Accept'] = '*/*'
        # header_dict['Accept-Encoding'] = 'gzip, deflate, br'
        # header_dict['Accept-Language'] = 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,en-US;q=0.6'
        # header_dict[
        #     'User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        # return header_dict
        header_dict = OrderedDict()
        # header_dict["Accept"] = "application/json, text/plain, */*"
        header_dict["Accept-Encoding"] = "gzip, deflate"
        header_dict[
            "User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) 12306-electron/1.0.1 Chrome/59.0.3071.115 Electron/1.8.4 Safari/537.36"
        header_dict["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
        #header_dict['Referer'] = 'https://kyfw.12306.cn/otn/leftTicket/init'
        return header_dict

    @classmethod
    def seat_name2num(self, index):
        """
        获取车票对应坐席
        :return:
        """
        seat = {'商务座': 32,
                '一等座': 31,
                '二等座': 30,
                '特等座': 25,
                '软卧': 23,
                '硬卧': 28,
                '硬座': 29,
                '无座': 26,
                '动卧': 33,
                }
        return seat[index]

    def initSession(self):
        self.session = requests.session()
        self.session.headers.update(self.set_header_default())

    def handle_data(self):

        pass


    def send_query(self, url, **kwargs):
        self.session.is_cdn = 1
        self.session.cdn_list = CDNProxy().open_cdn_file()

        if self.session.is_cdn == 1:
            self.session.cdn = self.session.cdn_list[random.randint(0, len(self.session.cdn_list) - 1)]

        url_host = self.session.cdn
        http = 'https'
        method = 'get'

        req_url = '/otn/leftTicket/queryZ?leftTicketDTO.train_date=2019-02-18&leftTicketDTO.from_station=SYQ&leftTicketDTO.to_station=IOQ&purpose_codes=ADULT'

        #response = self.session.request(method=method, url=http + '//' + url_host + req_url)

        self._proxies = None
        allow_redirects = False
        data = None

        num = 0
        #while True:
        try:
            if self.session.is_cdn == 1:
                self.session.cdn = self.session.cdn_list[random.randint(0, len(self.session.cdn_list) - 1)]

            url_host = 'kyfw.12306.cn'

            num += 1
            print("{0} current cdn is {1}".format(num, url_host))
            sleep(random.random() * 3)
            try:
                requests.packages.urllib3.disable_warnings()
            except:
                pass
            response = self.session.request(method=method,
                                            timeout=2,
                                            proxies=self._proxies,
                                            url=http + "://" + url_host + req_url,
                                            data=data,
                                            allow_redirects=allow_redirects,
                                            verify=False,
                                            **kwargs)

            if response.status_code == 200:
                print(response.content.decode('utf-8'))

                with open('response.html', 'w') as f:
                    f.write(response.content.decode('utf-8'))

                result = json.loads(response.content)['data']['result']
                if result:
                    for i in result:
                        ticket_info = i.split('|')
                        print(ticket_info)
                        if ticket_info[11] == "Y" and ticket_info[1] == "预订":  # 筛选未在开始时间内的车次
                            for j in self.seat_name2num:
                                is_ticket_pass = ticket_info[j]
                                if is_ticket_pass != '' and is_ticket_pass != '无' and is_ticket_pass != '*' and self.check_is_need_train(
                                        ticket_info):  # 过滤有效目标车次
                                    train_no = ticket_info[2]
                                    stationTrainCode = ticket_info[3]
                                    from_station_name = ticket_info[6]
                                    to_station_name = ticket_info[7]
                                    train_location = ticket_info[15]
                                    leftTicket = ticket_info[12]
                                    start_time = ticket_info[8]
                                    arrive_time = ticket_info[9]
                                    duration = ticket_info[10]
                                    print(start_time, arrive_time, duration)
                                    seat = j
                                    try:
                                        ticket_num = int(ticket_info[j])
                                    except ValueError:
                                        ticket_num = "有"
                                    print('车次: {0} 始发车站: {1} 终点站: {2} {3}: {4}'.format(ticket_info[3],
                                                                                        self.from_station_h,
                                                                                        self.to_station_h,
                                                                                        seat_conf_2[j],
                                                                                        ticket_num))
        except Exception as e:
            pass




    def query_by_station(self):
        #url = 'https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs=%E5%8D%97%E4%BA%AC,NJH&ts=%E6%B4%9B%E9%98%B3,LYF&date=2019-01-31&flag=N,N,Y'
        base_url = 'https://kyfw.12306.cn/'
        url = base_url + '/otn/leftTicket/queryZ?leftTicketDTO.train_date=2019-02-18&leftTicketDTO.from_station=NJH&leftTicketDTO.to_station=LYF&purpose_codes=ADULT'
        self.send_query(url)
        pass

    def query_by_train(self):
        url = 'https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no=5l000G193220&from_station_telecode=NKH&to_station_telecode=LLF&depart_date=2019-01-31'

        self.send_query(url)
        pass

import json
if __name__ == '__main__':
    MyQuery().query_by_station()
    pass
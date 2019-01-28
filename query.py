# -*- coding=utf-8 -*-

from collections import OrderedDict
import requests
from cdn_utils import CDNProxy
import random
from time import sleep
import matplotlib.pyplot as plt
import numpy as np

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

        #req_url = '/otn/leftTicket/queryZ?leftTicketDTO.train_date=2019-02-18&leftTicketDTO.from_station=SYQ&leftTicketDTO.to_station=IOQ&purpose_codes=ADULT'
        req_url = '/otn/leftTicket/queryZ?leftTicketDTO.train_date=2019-02-18&leftTicketDTO.from_station=NJH&leftTicketDTO.to_station=LYF&purpose_codes=ADULT'

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

                # with open('response.html', 'w') as f:
                #     f.write(response.content.decode('utf-8'))

                result = json.loads(response.content)['data']['result']
                return result
        except Exception as e:
            print(e)
            pass

    @classmethod
    def check_time(self, start_time, arrive_time, time_range=None):
        flag = True
        if not time_range:
            return flag
        for index, local_time in enumerate(time_range):
            if local_time:
                curr_time = start_time if index/2==0 else arrive_time
                curr_res = curr_time >= local_time if index%2==0 else curr_time <= local_time
                flag = curr_res
        return flag

    @classmethod
    def query_by_station(self, from_station, to_station, target_seat=None, time_range=None):
        #url = 'https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs=%E5%8D%97%E4%BA%AC,NJH&ts=%E6%B4%9B%E9%98%B3,LYF&date=2019-01-31&flag=N,N,Y'
        base_url = 'https://kyfw.12306.cn/'
        url = base_url + '/otn/leftTicket/queryZ?leftTicketDTO.train_date=2019-02-18&leftTicketDTO.from_station=NJH&leftTicketDTO.to_station=LYF&purpose_codes=ADULT'
        result = self.send_query(url)

        target_seat = []

        target_trains = []

        remain_ticket_num = 0

        if result:
            for i in result:
                ticket_info = i.split('|')
                if ticket_info[11] == "Y" and ticket_info[1] == "预订":  # 筛选未在开始时间内的车次
                    train_no = ticket_info[2]
                    stationTrainCode = ticket_info[3]
                    from_station_name = ticket_info[6]
                    to_station_name = ticket_info[7]
                    start_time = ticket_info[8]
                    arrive_time = ticket_info[9]
                    duration = ticket_info[10]

                    if time_range:      # check the time range
                        if self.check_time(start_time, arrive_time, time_range):
                            target_trains.append(train_no)
                    else:
                        target_trains.append(train_no)

                    if target_seat:
                        # 查询当前车次的余票信息, 如果有票就返回，无票就展示所有可能的换乘方案
                        for seat_num in target_seat:
                            remain_ticket = ticket_info[seat_num]
                            if remain_ticket not in ['', '无', '*']:
                                try:
                                    remain_ticket_num = int(remain_ticket)
                                except ValueError as e:
                                    print(e)
                                    remain_ticket_num = 100 # 否则是有，则表示票量充足，此时设定值为100

                                # 此时可以提交订单

            # 表面未成功提交订单，尝试所有线路显示
            for target_train in target_trains:
                self.query_by_train(from_station, to_station, target_train)

        #         print(ticket_info)
        #         if ticket_info[11] == "Y" and ticket_info[1] == "预订":  # 筛选未在开始时间内的车次
        #             for j in self.seat_name2num:
        #                 is_ticket_pass = ticket_info[j]
        #                 if is_ticket_pass != '' and is_ticket_pass != '无' and is_ticket_pass != '*' and self.check_is_need_train(
        #                         ticket_info):  # 过滤有效目标车次
        #                     train_no = ticket_info[2]
        #                     stationTrainCode = ticket_info[3]
        #                     from_station_name = ticket_info[6]
        #                     to_station_name = ticket_info[7]
        #                     start_time = ticket_info[8]
        #                     arrive_time = ticket_info[9]
        #                     duration = ticket_info[10]
        #                     # train_location = ticket_info[15]
        #                     # leftTicket = ticket_info[12]
        #                     print(start_time, arrive_time, duration)
        #                     seat = j
        #                     try:
        #                         ticket_num = int(ticket_info[j])
        #                     except ValueError:
        #                         ticket_num = "有"
        #                     print('车次: {0} 始发车站: {1} 终点站: {2} {3}: {4}'.format(ticket_info[3],
        #                                                                        self.from_station_h,
        #                                                                        self.to_station_h,
        #                                                                        #seat_conf_2[j],
        #                                                                        ticket_num))
        # pass


    def time2num(self, str_time):
        if ':' not in str_time:
            return 0
        hour, minute = [int(x) for x in str_time.split(':')]
        minute10 = minute/60
        return hour + minute10


    def query_by_train(self, from_train_name, to_train_name, train_no):
        url = 'https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no=5l000G193220&from_station_telecode=NKH&to_station_telecode=LLF&depart_date=2019-01-31'

        #result = self.send_query(url)
        result = '''
        {"validateMessagesShowId":"_validatorMessage","status":true,"httpstatus":200,
        "data":{
        "data":[
        {"start_station_name":"上海虹桥","arrive_time":"13:44","station_train_code":"G1932","station_name":"上海虹桥","train_class_name":"高速","service_type":"2","start_time":"13:44","stopover_time":"----","end_station_name":"西安北","station_no":"01","isEnabled":false},
        {"arrive_time":"14:07","station_name":"苏州北","start_time":"14:09","stopover_time":"2分钟","station_no":"02","isEnabled":false},
        {"arrive_time":"14:19","station_name":"无锡东","start_time":"14:29","stopover_time":"10分钟","station_no":"03","isEnabled":false},
        {"arrive_time":"14:58","station_name":"镇江南","start_time":"15:12","stopover_time":"14分钟","station_no":"04","isEnabled":false},
        {"arrive_time":"15:30","station_name":"南京南","start_time":"15:32","stopover_time":"2分钟","station_no":"05","isEnabled":true},
        {"arrive_time":"15:50","station_name":"滁州","start_time":"15:52","stopover_time":"2分钟","station_no":"06","isEnabled":true},
        {"arrive_time":"16:55","station_name":"徐州东","start_time":"17:00","stopover_time":"5分钟","station_no":"07","isEnabled":true},
        {"arrive_time":"18:31","station_name":"郑州东","start_time":"18:34","stopover_time":"3分钟","station_no":"08","isEnabled":true},
        {"arrive_time":"19:11","station_name":"洛阳龙门","start_time":"19:13","stopover_time":"2分钟","station_no":"09","isEnabled":true},
        {"arrive_time":"20:31","station_name":"西安北","start_time":"20:31","stopover_time":"----","station_no":"10","isEnabled":false}
        ]},
        "messages":[],"validateMessages":{}
        }
        '''

        #fig, ax = plt.subplots()
        plt.xticks(np.arange(13,21,step=1))
        plt.yticks(np.arange(0,9,step=1))
        plt.axis([13,21,0,9])

        station_infos = []

        data = json.loads(result)['data']['data']
        if data:
            for station_info in data:
                arrive_time_num = self.time2num(station_info['arrive_time'])
                start_time_num = self.time2num(station_info['start_time'])
                plt.scatter([arrive_time_num, start_time_num], [0.1]*2, marker='o')
                plt.plot([arrive_time_num, start_time_num], [0.1]*2)
                station_infos.append([station_info['station_name'], arrive_time_num, start_time_num])


        for length in range(1, len(station_infos)):
            for index, station_info in enumerate(station_infos):
                if length + index < len(station_infos):
                    start_time_num = station_infos[index][2]
                    arrive_time_num = station_infos[index + length][1]
                    plt.plot([arrive_time_num,start_time_num],[length + index * 0.1] * 2)
        plt.show()

        '''
        1, 查询station，忽略余票信息，只关注时间范围，查到合适车次
        2，查询station，标记余票信息，不关注时间范围，查到合适车站
        '''
        # query_by_station()
        pass

import json
if __name__ == '__main__':
    #MyQuery().query_by_station()
    MyQuery().query_by_train(None,None,None)
    pass
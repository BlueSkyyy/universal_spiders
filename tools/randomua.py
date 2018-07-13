# _*_coding:utf-8_*_
# Time : 2018/6/28 15:03
# User : yy-zhangcong2
# Email: zhangcong2@yy.com
# Python: 3.6.4

"""Documentation comments"""
import random
import os
import json


class Ua(object):
    ua_list = []
    path = str(os.path.dirname(os.path.abspath(__file__))) + "/ua.json"
    with open(path, 'r', encoding='utf-8')as file:
        data_json = json.load(file)
        for i in data_json['browsers']['chrome']:
            ua_list.append(i)

        for j in data_json['browsers']['safari']:
            ua_list.append(j)

    def get_ua(self, arg1):
        if isinstance(arg1, dict):
            _u = random.choice(self.ua_list)
            _a = {"User-Agent": _u}
            _a.update(arg1)
            return _a
        else:
            print('ua-参数-错误')

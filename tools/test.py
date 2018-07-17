# _*_coding:utf-8_*_
# Time : 2018/7/3 18:51
# User : yy-zhangcong2
# Email: zhangcong2@yy.com
# Python: 3.6.4

"""Documentation comments"""

# from tools.utils import RPCSESSION
# from tools.utils import MysqlDB
# import requests
# from pb import spiderinput_pb2

# if __name__ == "__main__":
#     # temp_request = spiderinput_pb2.InputAuditVideoRequest()
#     # video_data = temp_request.video_datas.add()
#     # video_data.post_vid = 34662253596250
#     # video_data.vsource_vid = '11_1264021'
#     # send_message = temp_request.SerializeToString()
#     # print(send_message)
#     # s = requests.session()
#     # header = {"Content-Type": "application/protobuf"}
#     # a = s.post(url='http://116.31.122.113:8101/budao.SpiderInputService/InputAuditOfflineVideoData', data=send_message,
#     #            headers=header)
#     # print(a.text)
#     # s.close()
#     # rpc_s = RPCSESSION()
#     # rpc_s.rpc_send(post_vid=34662253596250, vsource_vid='11_1264021')
#     client = MysqlDB()
#     client.data_query('SELECT videourl, vid, vsource_vid FROM video_0 WHERE parse_type = 4 AND state = 2 LIMIT 1')
#     query_data = client.cursor.fetchall()
#     for i in query_data:
#         print(type(i[0]))
#         print(type(i[1]))
#         print(type(i[2]))

from urllib import parse
import time
import random


# params = {
#     "keyword": "699862339",
#     "cursor": "0",
#     "count": "10",
#     "type": "1",
#     "ts": str(round(time.time())),
#     "app_type": "normal",
#     "os_api": "24",
#     "device_platform": "android",
#     "device_type": "BLN-AL40",
#     "iid": str(random.randrange(1000 * 1000 * 10, 1000 * 1000 * 50)),
#     "ssmix": "a",
#     "manifest_version_code": "166",
#     "dpi": "480",
#     "version_code": "166",
#     "app_name": "aweme",
#     "version_name": "1.6.6",
#     "openudid": "60aed8020936b609",
#     "device_id": str(random.randrange(1000 * 1000 * 10, 1000 * 1000 * 50)),
#     "resolution": "1080*1812",
#     "os_version": "7.0",
#     "language": "zh",
#     "device_brand": "HONOR",
#     "ac": "wifi",
#     "update_version_code": "1662",
#     "aid": "1128",
#     "channel": "douyin_tengxun_wzl"
# }

class Safe:
    @staticmethod
    def bytes(s, default_value=b'') -> bytes:
        if isinstance(s, str):
            return s.encode('utf-8')
        elif isinstance(s, bytes):
            return s
        return default_value

    @staticmethod
    def md5_str(s) -> str:
        import hashlib
        m = hashlib.md5()
        m.update(Safe.bytes(s))
        return m.hexdigest()


class DouyinSigHelper:
    key1 = '57218436'
    key2 = '15387264'
    rstr = 'efc84c17'

    debug_ts = None
    debug_rticket = None

    @staticmethod
    def rewrite_params(params, ts, rticket) -> dict:
        """
        :type rticket: int
        :type ts: int
        :type params: dict
        """

        ts = DouyinSigHelper.debug_ts or ts
        rticket = DouyinSigHelper.debug_rticket or rticket

        params.update({
            "ts": ts,
            "_rticket": rticket
        })

        sig_str = DouyinSigHelper.__prepare_sig_str(params)
        md5 = Safe.md5_str(sig_str)
        if ts & 1:
            md5 = Safe.md5_str(md5)

        hex_time = hex(ts)[2:]
        k1 = DouyinSigHelper.__shift(hex_time, DouyinSigHelper.key1)
        k2 = DouyinSigHelper.__shift(hex_time, DouyinSigHelper.key2)
        sig = DouyinSigHelper.__gen_sig(md5, k1, k2)

        params.update({
            "as": sig[:18],
            "cp": sig[18:],
            "ts": ts,
            "_rticket": rticket
        })

        return params

    @staticmethod
    def __prepare_sig_str(params):
        """
        :type params: dict
        """
        r = ''
        params.update({
            "rstr": DouyinSigHelper.rstr
        })
        for k in sorted(params.keys()):
            v = str(params[k])
            v = v.replace('+', 'a').replace(' ', 'a')
            r += v

        return r

    @staticmethod
    def __shift(p1, p2):
        """
        :type p1: str
        :type p2: str
        """
        p = ''
        p += p1[int(p2[0], 10) - 1]
        p += p1[int(p2[1], 10) - 1]
        p += p1[int(p2[2], 10) - 1]
        p += p1[int(p2[3], 10) - 1]
        p += p1[int(p2[4], 10) - 1]
        p += p1[int(p2[5], 10) - 1]
        p += p1[int(p2[6], 10) - 1]
        p += p1[int(p2[7], 10) - 1]
        return p.lower()

    @staticmethod
    def __gen_sig(md5, k1, k2):
        """
        :type md5: str
        :type k1: str
        :type k2: str
        """
        ascp = ['0'] * 36
        ascp[0] = 'a'
        ascp[1] = '1'
        for i in range(0, 8):
            ascp[2 * (i + 1)] = md5[i]
            ascp[2 * i + 3] = k2[i]
            ascp[2 * i + 18] = k1[i]
            ascp[2 * i + 1 + 18] = md5[i + 24]
        ascp[-2] = 'e'
        ascp[-1] = '1'

        return ''.join(ascp)


class Test:
    @staticmethod
    def run(*args):
        for i in args:
            print(i)


if __name__ == '__main__':
    real_user = [{"iid": 30373511894, "device_id": 35781128184},
                 {"iid": 37526064403, "device_id": 37977281220},
                 {"iid": 31717878106, "device_id": 10258085598},
                 {"iid": 34796162101, "device_id": 53478217135},
                 {"iid": 34796457507, "device_id": 51263625018},
                 {"iid": 34797113441, "device_id": 53478839423},
                 {"iid": 34735681415, "device_id": 38194105888},
                 {"iid": 34800082374, "device_id": 49035294445},
                 {"iid": 35747076934, "device_id": 51277347406},
                 {"iid": 1, "device_id": 1}]

    params = {
        "cursor": 0,
        'aweme_id': '6569926925316263176',
        "device_platform": "android",
        "count": 50,
        "iid": 34797113441,
        "version_code": "166",
        "app_name": "aweme",
        "version_name": "1.6.6",
        "device_id": 53478839423,
        "ac": "wifi",
        "aid": 1128,
        "build_number": 16605,
        "comment_style": 2
    }
    a = DouyinSigHelper.rewrite_params(params, round(time.time()), round(time.time() * 1000))
    url = "https://aweme.snssdk.com/aweme/v1/comment/list/?" + parse.urlencode(a)
    print(url)
    import requests

    header = {
        # "Host": "api.amemv.com",
        # "Connection": "keep-alive",
        # "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/3.8.1",
    }

    search_header = {
        "Host": "aweme.snssdk.com",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip",
        "X-SS-REQ-TICKET": str(round(time.time() * 1000)),
        "User-Agent": "com.ss.android.ugc.aweme/190 (Linux; U; Android 7.0; zh_CN_#Hans; BLN-AL40; Build/HONORBLN-AL40; Cronet/58.0.2991.0)"
    }

    s = requests.session()
    b = s.get(url=url, headers=header)
    print(b.text)
    # import random
    # a = [1, 2, 3]
    # print(len(a))
    # print(random.randint(0, len(a)))
    # import json
    #
    # data = json.loads(b.text, encoding='utf-8')
    # if 'status_code' in data.keys() and data['status_code'] == 0:
    #     if 'aweme_list' in data.keys() and data['aweme_list']:
    #         print('*' * 99 + str(len(data['aweme_list'])))
    #         for i in data['aweme_list']:
    #             if 'aweme_id' in i.keys() and i['aweme_id']:
    #                 print(i['aweme_id'])
    #             else:
    #                 print('failed')

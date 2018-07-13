# _*_coding:utf-8_*_
# Time : 2018/7/12 18:22
# User : yy-zhangcong2
# Email: zhangcong2@yy.com
# Python: 3.6.4

"""Documentation comments"""
from tools.utils import Safe
import time


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


class DouyinUserAndParamsHelper:
    # 必须有真实的iid和device_id
    real_user_list = [{"iid": 30373511894, "device_id": 35781128184},
                      {"iid": 37526064403, "device_id": 37977281220},
                      {"iid": 31717878106, "device_id": 10258085598},
                      {"iid": 34796162101, "device_id": 53478217135},
                      {"iid": 34796457507, "device_id": 51263625018},
                      {"iid": 34797113441, "device_id": 53478839423},
                      {"iid": 34735681415, "device_id": 38194105888},
                      {"iid": 34800082374, "device_id": 49035294445},
                      {"iid": 35747076934, "device_id": 51277347406}]

    @staticmethod
    def provide_user():
        import random
        user_dict = DouyinUserAndParamsHelper.real_user_list[
            random.randint(0, len(DouyinUserAndParamsHelper.real_user_list) - 1)]
        return user_dict

    @staticmethod
    def update_params(up_dict):
        from urllib import parse
        real_user = DouyinUserAndParamsHelper.provide_user()
        params = {
            # "max_cursor": 0,
            # 'user_id': '96492921920',
            # "count": 5000,
            "device_platform": "android",
            "iid": real_user['iid'],
            "version_code": "166",
            "app_name": "aweme",
            "version_name": "1.6.6",
            "device_id": real_user['device_id'],
            "ac": "wifi",
            "aid": 1128,
            "build_number": 16605
        }
        params.update(up_dict)
        f_params = DouyinSigHelper.rewrite_params(params, round(time.time()), round(time.time() * 1000))
        return parse.urlencode(f_params)

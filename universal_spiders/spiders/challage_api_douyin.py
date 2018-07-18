# -*- coding: utf-8 -*-
import scrapy
import json
from tools.douyin_helper import DouyinUserAndParamsHelper
from ..items import UniversalSpidersItem


class ChallageApiDouyinSpider(scrapy.Spider):
    name = 'challage_api_douyin'
    allowed_domains = ['api.amemv.com']
    # start_urls = ['http://api.amemv.com/']

    default_header = {
        # "Host": "api.amemv.com",
        # "Connection": "keep-alive",
        # "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/3.8.1"
    }

    challage_dict = {
        # "抖音上的“伪长腿”": ['再也不信你的大长腿了！'],
        # "抖音好看的美腿在这里": ['美腿'],
        # "抖音里的帅boy": ['瞬间变美变帅'],
        "抖音最火歌曲短视频集合": ['热门歌曲', 'shape of you', '全部都是你', 'boom', '纸短情长', '123我爱你'],
        # "抖音热门挑战之全民挑战66舞": ['全民挑战66舞'],
        # "抖音热门挑战之橙子微笑挑战": ['橙子微笑挑战'],
        # "抖音热门挑战之转圈大挑战": ['转圈大挑战'],
        # "抖音热门挑战之你敢挑战撩头发吗": ['你敢挑战掀头发吗'],
        # "抖音热门挑战之疯狂加速器": ['我要挑战疯狂加速器'],
        # "抖音热门挑战之冬奥会冰壶项目": ['我来挑战冬奥会冰壶项目'],
        # "抖音热门挑战之百变背景挑战": ['百变背景挑战'],
        # "抖音表白套路汇总": ['520旅行表白套路', '520，是谁在表白'],
        # "抖音计算器音乐大全": ['计算器音乐'],
        # "抖音神反转": ['音乐神反转'],
        # "抖音尬舞机": ['舞蹈'],
        # "抖音偶遇明星啦": ['偶遇明星'],
        # "抖音里播放超过百万的视频": ['播放数据超过百万次的视频'],
        # "明星们在抖音上拍什么": ['明星']
    }
    try_count = 0

    def start_requests(self):
        for k, v in self.challage_dict.items():
            for i in v:
                meta_dict = {"topic": k, "keyword": i}
                yield scrapy.Request(
                    url='https://api.amemv.com/aweme/v1/challenge/search/?' + DouyinUserAndParamsHelper.update_params(
                        {"keyword": i, "count": 10, "cursor": 0}), dont_filter=True,
                    headers=ChallageApiDouyinSpider.default_header,
                    method='GET',
                    meta=meta_dict, callback=self.parse)

    def parse(self, response):

        if response.status == 200:
            print(str(response.body, encoding='utf-8'))
            data = json.loads(str(response.body, encoding='utf-8'))
            if 'status_code' in data.keys() and data['status_code'] == 0:
                if 'challenge_list' in data.keys() and data['challenge_list']:
                    challage = data['challenge_list'][0]
                    if 'challenge_info' in challage.keys() and challage['challenge_info'] and 'cid' in challage[
                        'challenge_info'].keys() and challage['challenge_info']['cid']:
                        cid = challage['challenge_info']['cid']
                        yield scrapy.Request(
                            url='https://api.amemv.com/aweme/v1/challenge/aweme/?' + DouyinUserAndParamsHelper.update_params(
                                {"ch_id": cid, "count": 20, "cursor": 0}), dont_filter=True,
                            headers=ChallageApiDouyinSpider.default_header,
                            method='GET',
                            meta=response.meta, callback=self.detail_parse)
                    else:
                        print('NO_CID')
            else:
                ChallageApiDouyinSpider.try_count += 1
                if ChallageApiDouyinSpider.try_count > 10:
                    from datetime import datetime
                    with open(str(datetime.now().date().strftime('%Y%m%d')) + 'cid_search_err.txt', 'a',
                              encoding='utf-8')as file:
                        file.write(
                            'keyword:' + str(response.meta['keyword']) + ',topic:' + response.meta['topic'] + '\n')
                else:
                    yield scrapy.Request(
                        url='https://api.amemv.com/aweme/v1/challenge/search/?' + DouyinUserAndParamsHelper.update_params(
                            {"keyword": response.meta['keyword'], "count": 10, "cursor": 0}), dont_filter=True,
                        headers=ChallageApiDouyinSpider.default_header,
                        method='GET',
                        meta=response.meta, callback=self.parse)
        else:
            from datetime import datetime
            with open(str(datetime.now().date().strftime('%Y%m%d')) + '_cid_douyin_parse_!200_err.txt', 'a',
                      encoding='utf-8')as file:
                file.write('keyword:' + str(response.meta['keyword']) + ',topic:' + response.meta['topic'] + '\n')

    def detail_parse(self, response):
        if response.status == 200:
            #print(str(response.body, encoding='utf-8'))
            #data = json.loads(str(response.body, encoding='utf-8'))
            print(response.meta['keyword'])

        else:
            from datetime import datetime
            with open(str(datetime.now().date().strftime('%Y%m%d')) + '_cid_douyin_detail_!200_err.txt', 'a',
                      encoding='utf-8')as file:
                file.write(
                    'keyword:' + str(response.meta['keyword']) + ',topic:' + response.meta['topic'] + ",user_id:" +
                    response.meta['user_id'] + '\n')

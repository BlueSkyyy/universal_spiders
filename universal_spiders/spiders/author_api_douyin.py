# -*- coding: utf-8 -*-
import scrapy
import time
import json
from ..items import UniversalSpidersItem
from tools.douyin_helper import DouyinUserAndParamsHelper


class AuthorApiDouyinSpider(scrapy.Spider):
    name = 'author_api_douyin'
    allowed_domains = ['api.amemv.com', 'aweme.snssdk.com']

    # start_urls = ['http://api.amemv.com/']

    default_header = {
        "Host": "api.amemv.com",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/3.7.0.6"
    }
    search_header = {
        "Host": "aweme.snssdk.com",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip",
        "X-SS-REQ-TICKET": str(round(time.time() * 1000)),
        "User-Agent": "com.ss.android.ugc.aweme/190 (Linux; U; Android 7.0; zh_CN_#Hans; BLN-AL40; Build/HONORBLN-AL40; Cronet/58.0.2991.0)"
    }
    try_count = 0

    def start_requests(self):
        # 获取用户信息
        user_dict = {
            "抖音好看的美腿在这里": ['952454822'],
            "抖音里的帅boy": ['58915999', '11111111ii', '58826496', '19008461'],
            "抖音最美小姐姐": ['IAMCHEESE', '6065536', 'yingtaogongzhu', '9503043', 'babeyuu55'],
            "抖音潮流搭配风": ['839399539', 'juzi90312', '124885918', '14808960'],
            "抖音文化小课堂/抖音让你成为文化人": ['987523062', '1072132481', '98337230', '837222249'],
            "抖音美食炼成术": ['781340612', '633041794', '698550156', '333025213', '576657769'],
            "抖音里的小姐姐好会穿": ['cutie888', 'yanshitou1234'],
            "抖音精致达人会生活": ['291954110', 'mz36', 'shenghuo66'],
            "抖音恋爱tip教学": ['291931910', '7664071', '37881979', '7146328', 'xy9920599'],
            "抖音Ps信手拈来": ['cui2066', 'ymawxb', '867048418', '867048418', 'ps8294'],
            "抖音Excel教学不求人": ['154539259', 'lime0906.', 'dnkt6666', 'excel001', 'excel3'],
            "抖音让你PPT略胜一筹": ['606186051', '346715476', '950779070', 'pptmoban', '991443274'],
            "抖音上的戏精有很多": ['63452991', '14286898', '3518813'],
            "抖音里的烘焙工厂": ['qiyue52718', '169558553', '99494425', '385699400', '21618813'],
            "抖音表白套路汇总": ['a7529235'],
            "抖音计算器音乐大全": ['139759957', '130754538', '849693895', '95069902']
        }
        for k, v in user_dict.items():
            for i in v:
                meta_dict = {"topic": k, "keyword": i}
                yield scrapy.Request(
                    url='https://aweme.snssdk.com/aweme/v1/general/search/?' + DouyinUserAndParamsHelper.update_params(
                        {"keyword": i}), dont_filter=True, headers=AuthorApiDouyinSpider.search_header, method='GET',
                    meta=meta_dict, callback=self.parse)

    def parse(self, response):
        aweme_count = 0
        nickname = ''
        uid = ''
        if response.status == 200:
            data = json.loads(str(response.body, encoding='utf-8'))
            if 'status_code' in data.keys() and data['status_code'] == 0:
                print(str(response.body, encoding='utf-8'))
                if 'user_list' in data.keys() and data['user_list']:
                    u = data['user_list'][0]
                    if 'user_info' in u.keys() and u['user_info']:
                        if 'aweme_count' in u['user_info'].keys() and u['user_info']['aweme_count']:
                            aweme_count = u['user_info']['aweme_count']
                        if 'nickname' in u['user_info'].keys() and u['user_info']['nickname']:
                            nickname = u['user_info']['nickname']
                        else:
                            nickname = 'unknown'
                        if 'uid' in u['user_info'].keys() and u['user_info']['uid']:
                            uid = u['user_info']['uid']
                            response.meta.update({"user_id": uid, "nickname": nickname, "aweme_count": aweme_count})
                            yield scrapy.Request(
                                url='https://api.amemv.com/aweme/v1/aweme/post/?' + DouyinUserAndParamsHelper.update_params(
                                    {"user_id": uid, "count": aweme_count}),
                                dont_filter=True, headers=AuthorApiDouyinSpider.default_header, method='GET',
                                meta=response.meta,
                                callback=self.detail_parse)
                        else:
                            print('NO_USER_ID')
            else:
                AuthorApiDouyinSpider.try_count += 1
                if AuthorApiDouyinSpider.try_count > 10:
                    from datetime import datetime
                    with open(str(datetime.now().date().strftime('%Y%m%d'))+'search_err.txt', 'a',
                              encoding='utf-8')as file:
                        file.write(
                            'keyword:' + str(response.meta['keyword']) + ',topic:' + response.meta['topic'] + '\n')
                else:
                    yield scrapy.Request(
                        url='https://aweme.snssdk.com/aweme/v1/general/search/?' + DouyinUserAndParamsHelper.update_params(
                            {"keyword": response.meta['keyword']}), dont_filter=True,
                        headers=AuthorApiDouyinSpider.search_header,
                        method='GET',
                        meta=response.meta, callback=self.parse)
        else:
            from datetime import datetime
            with open(str(datetime.now().date().strftime('%Y%m%d'))+'douyin_parse_!200_err.txt', 'a',
                      encoding='utf-8')as file:
                file.write('keyword:' + str(response.meta['keyword']) + ',topic:' + response.meta['topic'] + '\n')

    def detail_parse(self, response):
        if response.status == 200:
            # print(str(response.body, encoding='utf-8'))
            # print(response.meta)
            data = json.loads(str(response.body, encoding='utf-8'))
            if 'status_code' in data.keys() and data['status_code'] == 0:
                if 'aweme_list' in data.keys() and data['aweme_list']:
                    for i in data['aweme_list']:
                        item = UniversalSpidersItem()
                        item['source'] = 1
                        if 'aweme_id' in i.keys() and i['aweme_id']:
                            item['vid'] = i['aweme_id']
                        else:
                            item['vid'] = 0
                        item['media_name'] = response.meta['nickname']
                        item['media_id'] = response.meta['user_id']
                        if 'desc' in i.keys() and i['desc']:
                            item['video_title'] = i['desc']
                        else:
                            item['video_title'] = 'unknown'
                        if 'statistics' in i.keys() and 'play_count' in i['statistics'].keys() and i['statistics'][
                            'play_count']:
                            item['play_count'] = i['statistics']['play_count']
                        else:
                            item['play_count'] = 0
                        if 'video' in i.keys() and 'duration' in i['video'].keys() and i['video']['duration']:
                            item['video_duration'] = round((i['video']['duration']) / 1000)
                        else:
                            item['video_duration'] = 0
                        if 'share_url' in i.keys() and i['share_url']:
                            item['share_url'] = i['share_url']
                        else:
                            item['share_url'] = 'unknown'
                        if 'video' in i.keys() and 'origin_cover' in i['video'].keys() and 'url_list' in i['video'][
                            'origin_cover'].keys() and i['video']['origin_cover']['url_list']:
                            item['video_cover'] = i['video']['origin_cover']['url_list'][0]
                        else:
                            item['video_cover'] = 'unknown'
                        if 'video' in i.keys() and 'width' in i['video'].keys() and i['video']['width']:
                            item['video_width'] = i['video']['width']
                        else:
                            item['video_width'] = 0
                        if 'video' in i.keys() and 'height' in i['video'].keys() and i['video']['height']:
                            item['video_height'] = i['video']['height']
                        else:
                            item['video_height'] = 0
                        if 'statistics' in i.keys() and 'digg_count' in i['statistics'].keys() and i['statistics'][
                            'digg_count']:
                            item['praise_count'] = i['statistics']['digg_count']
                        else:
                            item['praise_count'] = 0
                        item['fav_count'] = 0
                        if 'statistics' in i.keys() and 'share_count' in i['statistics'].keys() and i['statistics'][
                            'share_count']:
                            item['share_count'] = i['statistics']['share_count']
                        else:
                            item['share_count'] = 0
                        if 'statistics' in i.keys() and 'comment_count' in i['statistics'].keys() and i['statistics'][
                            'comment_count']:
                            item['comment_count'] = i['statistics']['comment_count']
                        else:
                            item['comment_count'] = 0
                        if 'create_time' in i.keys() and i['create_time']:
                            item['create_time'] = i['create_time']
                        else:
                            item['create_time'] = round(time.time())
                        if 'video' in i.keys() and 'download_addr' in i['video'].keys() and 'url_list' in i['video'][
                            'download_addr'].keys() and i['video']['download_addr']['url_list']:
                            item['video_url'] = i['video']['download_addr']['url_list'][0]
                        else:
                            item['video_url'] = 'unknown'
                        item['topic'] = response.meta['topic']
                        item['parse_type'] = 1
                        yield item
        else:
            from datetime import datetime
            with open(str(datetime.now().date().strftime('%Y%m%d')) + '_douyin_detail_!200_err.txt', 'a',
                      encoding='utf-8')as file:
                file.write('keyword:' + str(response.meta['keyword']) + ',topic:' + response.meta['topic'] + '\n')

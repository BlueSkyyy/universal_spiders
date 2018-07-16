# -*- coding: utf-8 -*-
import scrapy
from tools.utils import MysqlDB
from scrapy import signals
from pydispatch import dispatcher
import time
from tools.douyin_helper import DouyinUserAndParamsHelper
from ..items import DouyinCommentsItem
import json


class CommentsApiDouyinSpider(scrapy.Spider):
    name = 'comments_api_douyin'
    allowed_domains = ['aweme.snssdk.com']

    # start_urls = ['http://aweme.snssdk.com/']

    dedault_header = {
        "Host": "aweme.snssdk.com",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip",
        "X-SS-REQ-TICKET": str(round(time.time() * 1000)),
        "User-Agent": "com.ss.android.ugc.aweme/190 (Linux; U; Android 7.0; zh_CN_#Hans; BLN-AL40; Build/HONORBLN-AL40; Cronet/58.0.2991.0)"
    }

    def __init__(self):
        super(CommentsApiDouyinSpider, self).__init__()
        self.db_client = MysqlDB()
        dispatcher.connect(self.close_client, signals.spider_closed)

    def close_client(self):
        self.db_client.db_close()

    def start_requests(self):
        self.db_client.data_query(
            "SELECT video_id FROM video_data  where DATE_FORMAT(insert_time,'%Y%m%d') = '20180716'")
        query_data = self.db_client.cursor.fetchall()
        # query_data = ['6569926925316263176']
        for i in query_data:
            meta_dict = {"aweme_id": i}
            yield scrapy.Request(
                url='https://aweme.snssdk.com/aweme/v1/comment/list/?' + DouyinUserAndParamsHelper.update_params({
                    "aweme_id": i, "cursor": "0", "count": "20"
                }), dont_filter=True, method='GET', headers=CommentsApiDouyinSpider.dedault_header,
                meta=meta_dict, callback=self.parse)

    def parse(self, response):
        if response.status == 200:
            data = json.loads(str(response.body, encoding='utf-8'))
            if 'status_code' in data.keys() and data['status_code'] == 0:
                if 'comments' in data.keys() and data['comments']:
                    for i in data['comments']:
                        item = DouyinCommentsItem()
                        item['source'] = 1
                        if 'aweme_id' in i.keys() and i['aweme_id']:
                            item['vid'] = i['aweme_id']
                        else:
                            item['vid'] = ''
                        if 'cid' in i.keys() and i['cid']:
                            item['cid'] = i['cid']
                        else:
                            item['cid'] = ''
                        if 'text' in i.keys() and i['text']:
                            item['content'] = i['text']
                        else:
                            item['content'] = ''
                        if 'digg_count' in i.keys() and i['digg_count']:
                            item['favor_num'] = i['digg_count']
                        else:
                            item['favor_num'] = 0
                        if 'user' in i.keys() and i['user'] and 'uid' in i['user'].keys() and i['user']['uid']:
                            item['user_id'] = i['user']['uid']
                        else:
                            item['user_id'] = ''
                        if 'user' in i.keys() and i['user'] and 'nickname' in i['user'].keys() and i['user'][
                            'nickname']:
                            item['user_name'] = i['user']['nickname']
                        else:
                            item['user_name'] = ''
                        if 'user' in i.keys() and i['user'] and 'avatar_thumb' in i['user'].keys() and i['user'][
                            'avatar_thumb'] and 'url_list' in i['user']['avatar_thumb'].keys() and \
                                i['user']['avatar_thumb']['url_list']:
                            item['user_photo'] = i['user']['avatar_thumb']['url_list'][0]
                        else:
                            item['user_photo'] = ''
                        if 'create_time' in i.keys() and i['create_time']:
                            item['create_time'] = i['create_time']
                        else:
                            item['create_time'] = round(time.time())
                        yield item
                if 'has_more' in data.keys() and int(data['has_more']) == 1:
                    print('HAS_MORE_COMMENTS')
                    yield scrapy.Request(
                        url='https://aweme.snssdk.com/aweme/v1/comment/list/?' + DouyinUserAndParamsHelper.update_params(
                            {
                                "aweme_id": response.meta["aweme_id"], "cursor": data["cursor"], "count": "20"
                            }), dont_filter=True, method='GET', headers=CommentsApiDouyinSpider.dedault_header,
                        meta=response.meta, callback=self.parse)
        else:
            from datetime import datetime
            with open(str(datetime.now().date().strftime('%Y%m%d')) + '_douyin_comment_parse!200.txt',
                      encoding='utf-8') as file:
                file.write('aweme_id:' + response.meta['aweme_id'] + '\n')

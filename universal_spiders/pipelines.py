# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from tools.utils import RPCSESSION, DouyinCommentsRPCSession
from scrapy import signals
from pydispatch import dispatcher
import time
from datetime import datetime


class UniversalSpidersPipeline(object):

    def __init__(self):
        super(UniversalSpidersPipeline, self).__init__()
        self.client = RPCSESSION()
        dispatcher.connect(self.client_close, signals.spider_closed)

    def client_close(self):
        self.client.session_close()

    def process_item(self, item, spider):
        if spider.name == 'author_api_douyin':
            time.sleep(0.1)
            if int(item['video_duration']) == 0 or item['video_url'] is None:
                pass
            else:
                self.client.rpc_send(source=item['source'], vid=item['vid'], media_name=item['media_name'],
                                     media_id=item['media_id'], video_title=item['video_title'],
                                     play_count=item['play_count'],
                                     video_duration=item['video_duration'], share_url=item['share_url'], source_type='',
                                     create_time=item['create_time'], channel_id='', question_type='', meta_data='',
                                     video_cover=item['video_cover'], video_width=item['video_width'],
                                     video_height=item['video_height'], praise_count=item['praise_count'],
                                     fav_count=item['fav_count'], share_count=item['share_count'],
                                     comment_count=item['comment_count'], video_url=item['video_url'],
                                     topic=item['topic'],
                                     parse_type=item['parse_type'])

                return item
        else:
            pass


class WriteAwemIdToFile(object):
    def process_item(self, item, spider):
        if spider.name == 'author_api_douyin':
            if int(item['video_duration']) == 0 or item['video_url'] is None:
                with open(str(datetime.now().date().strftime('%Y%m%d')) + 'miss_duration_or_url_awemeid.txt', 'a',
                          encoding='utf-8')as file:
                    file.write(item['vid'] + '\n')
                return item
            else:
                with open(str(datetime.now().date().strftime('%Y%m%d')) + 'succeed_awemeid.txt', 'a',
                          encoding='utf-8')as file:
                    file.write(item['vid'] + '\n')
                return item
        else:
            pass


# *********************************************************************************************************************
# *********************************************************************************************************************

class DouyinCommentsPipline(object):
    def __init__(self):
        super(DouyinCommentsPipline, self)
        self.client = DouyinCommentsRPCSession()
        dispatcher.connect(self.client_close, signals.spider_closed)

    def client_close(self):
        self.client.douyin_com_session_close()

    def process_item(self, item, spider):
        if spider.name == 'comments_api_douyin':
            time.sleep(0.1)
            if item['vid'] is None or item['content'] is None or item['cid'] is None or item['user_id'] is None:
                pass
            else:
                self.client.rpc_send(source=item['source'], vid=item['vid'], cid=item['cid'], content=item['content'],
                                     favor_num=item['favor_num'], user_id=item['user_id'], user_name=item['user_name'],
                                     user_photo=item['user_photo'], reply_num=0, is_hot=False,
                                     create_time=item['create_time'])
                return item
        else:
            pass


if __name__ == "__main__":
    # r = RPCSESSION()
    # r.rpc_send(source=1, vid='t', media_name='t', media_id='t', video_title='t', play_count=0, video_duration=12,
    #            share_url='t', source_type='', create_time=1531372816, channel_id='', question_type='', meta_data='',
    #            video_cover='t', video_width=1, video_height=1, praise_count=1, fav_count=2, share_count=3,
    #            comment_count=4, video_url='t', topic='t', parse_type=1)
    r = DouyinCommentsRPCSession()
    r.rpc_send(source=1, vid='t', cid='t', content='t', favor_num=0, user_id='t', user_name='t', user_photo='t',
               reply_num=999, is_hot=True,
               create_time=1531725183)

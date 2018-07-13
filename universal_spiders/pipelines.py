# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from tools.utils import RPCSESSION
from scrapy import signals
from pydispatch import dispatcher
import time

class UniversalSpidersPipeline(object):

    def __init__(self):
        super(UniversalSpidersPipeline, self).__init__()
        self.client = RPCSESSION()
        dispatcher.connect(self.client_close, signals.spider_closed)

    def client_close(self):
        self.client.session_close()

    def process_item(self, item, spider):
        time.sleep(1)
        self.client.rpc_send(source=item['source'], vid=item['vid'], media_name=item['media_name'],
                             media_id=item['media_id'], video_title=item['video_title'], play_count=item['play_count'],
                             video_duration=item['video_duration'], share_url=item['share_url'], source_type='',
                             create_time=item['create_time'], channel_id='', question_type='', meta_data='',
                             video_cover=item['video_cover'], video_width=item['video_width'],
                             video_height=item['video_height'], praise_count=item['praise_count'],
                             fav_count=item['fav_count'], share_count=item['share_count'],
                             comment_count=item['comment_count'], video_url=item['video_url'], topic=item['topic'],
                             parse_type=item['parse_type'])

        return item


if __name__ == "__main__":
    r = RPCSESSION()
    r.rpc_send(source=1, vid='t', media_name='t', media_id='t', video_title='t', play_count=0, video_duration=12,
               share_url='t', source_type='', create_time=1531372816, channel_id='', question_type='', meta_data='',
               video_cover='t', video_width=1, video_height=1, praise_count=1, fav_count=2, share_count=3,
               comment_count=4, video_url='t', topic='t', parse_type=1)

# _*_coding:utf-8_*_
# Time : 2018/6/28 14:30
# User : yy-zhangcong2
# Email: zhangcong2@yy.com
# Python: 3.6.4

"""Documentation comments"""
import pymysql
import logging
import requests
from pb import spiderinput_pb2
import time

_l = logging.getLogger(__file__)


class MysqlDB:
    '''
    链接发布线上库
    '''

    def __init__(self):
        try:
            self.connect = pymysql.Connect(
                host='221.228.79.244',
                port=8066,
                user='jxz_db@jxz_bd',
                password='xywaD3kfz',
                db='budao',
                charset='utf8mb4'
            )
            # _l.info('db-connect-success')
            print('db-connect-success')
        except Exception as e:
            print(e)
            # _l.info('dn-connect-failed')
            print('dn-connect-failed')
        self.cursor = self.connect.cursor()

    def db_close(self):
        if self.connect and self.cursor:
            self.cursor.close()
            self.connect.close()
            # _l.info('db-close-success')
            print('db-close-success')
        else:
            # _l.info('db-close-failed')
            print('db-close-failed')

    def data_insert(self, sql, data):
        if isinstance(sql, str):
            try:
                self.cursor.execute(sql % data)
                self.connect.commit()
            except Exception as e:
                self.connect.rollback()
                raise e
        else:
            print('params-wrong')

    def data_query(self, sql):
        if isinstance(sql, str):
            self.cursor.execute(sql)
            self.connect.commit()
        else:
            print('params-wrong')

    def query_params(self, sql):
        if isinstance(sql, str):
            self.cursor.execute(sql)
            self.connect.commit()
        else:
            print('params-err')


class RPCDATA(object):
    @staticmethod
    def serialize(source, vid, media_name, media_id, video_title, play_count, video_duration, share_url,
                  video_cover, video_width, video_height, source_type, praise_count, fav_count, share_count,
                  comment_count, create_time, video_url, channel_id, topic, question_type, meta_data, parse_type):
        temp_request = spiderinput_pb2.InputVideoRequest()
        video_data = temp_request.video_datas.add()
        video_data.source = source
        video_data.vid = vid
        video_data.media_name = media_name
        video_data.media_id = media_id
        video_data.video_title = video_title
        video_data.play_count = play_count
        video_data.video_duration = video_duration
        video_data.share_url = share_url
        video_data.video_cover = video_cover
        video_data.video_width = video_width
        video_data.video_height = video_height
        video_data.source_type = source_type
        video_data.praise_count = praise_count
        video_data.fav_count = fav_count
        video_data.share_count = share_count
        video_data.comment_count = comment_count
        video_data.create_time = create_time
        video_data.video_url = video_url
        video_data.channel_id = channel_id
        video_data.topic = topic
        video_data.question_type = question_type
        video_data.meta_data = meta_data
        video_data.parse_type = parse_type

        return temp_request.SerializeToString()


class RPCSESSION(object):
    default_header = {"Content-Type": "application/protobuf"}

    def __init__(self):
        self.s = requests.session()

    def rpc_send(self, source, vid, media_name, media_id, video_title, play_count, video_duration, share_url,
                 video_cover, video_width, video_height, source_type, praise_count, fav_count, share_count,
                 comment_count, create_time, video_url, channel_id, topic, question_type, meta_data, parse_type):
        time.sleep(1)  # 控制并发下的最大链接数
        self.s.post(url='http://116.31.122.113:8101/budao.SpiderInputService/InputVideoData',
                    data=RPCDATA.serialize(source=source
                                           , vid=vid
                                           , media_name=media_name
                                           , media_id=media_id
                                           , video_title=video_title
                                           , play_count=play_count
                                           , video_duration=video_duration
                                           , share_url=share_url
                                           , video_cover=video_cover
                                           , video_width=video_width
                                           , video_height=video_height
                                           , source_type=source_type
                                           , praise_count=praise_count
                                           , fav_count=fav_count
                                           , share_count=share_count
                                           , comment_count=comment_count
                                           , create_time=create_time
                                           , video_url=video_url
                                           , channel_id=channel_id
                                           , topic=topic
                                           , question_type=question_type
                                           , meta_data=meta_data
                                           , parse_type=parse_type), headers=self.default_header)

    def session_close(self):
        self.s.close()
        print('RPC_SESSION_CLOSED')


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

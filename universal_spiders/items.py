# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UniversalSpidersItem(scrapy.Item):
    source = scrapy.Field()  # 来源 0西瓜 1抖音 2快手 3内涵段子 4即刻 5好看 6波波 7秒拍 8美拍 9B站 10 微博 11 梨视频 12 飞碟说 int
    vid = scrapy.Field()  # 视频在源站的id string，具体根据规则来截取
    media_name = scrapy.Field()  # 媒体名 string
    media_id = scrapy.Field()  # 媒体id string
    video_title = scrapy.Field()  # 视频标题 string
    play_count = scrapy.Field()  # 播放总数 int
    video_duration = scrapy.Field()  # 视频时长 int
    share_url = scrapy.Field()  # h5链接 string
    video_cover = scrapy.Field()  # 封面图 string
    video_width = scrapy.Field()  # 宽 int
    video_height = scrapy.Field()  # 高 int
    source_type = scrapy.Field()  # 博哥自定义
    praise_count = scrapy.Field()  # 点赞数 int
    fav_count = scrapy.Field()  # 收藏数 int
    share_count = scrapy.Field()  # 分享数 int
    comment_count = scrapy.Field()  # 评论数 int
    create_time = scrapy.Field()
    video_url = scrapy.Field()  # 播放地址 string
    channel_id = scrapy.Field()  # 频道 string
    topic = scrapy.Field()  # 话题 string
    question_type = scrapy.Field()  # 问答类型
    meta_data = scrapy.Field()  # 元数据 string
    parse_type = scrapy.Field()  # 解析规则 int


class DouyinCommentsItem(scrapy.Item):
    source = scrapy.Field()
    vid = scrapy.Field()
    cid = scrapy.Field()
    content = scrapy.Field()
    favor_num = scrapy.Field()
    user_id = scrapy.Field()
    user_name = scrapy.Field()
    user_photo = scrapy.Field()
    reply_num = scrapy.Field()
    create_time = scrapy.Field()

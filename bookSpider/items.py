# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class NovelItem(scrapy.Item):
    # 书名
    book_name = scrapy.Field()
    # 书名编号
    id_book = scrapy.Field()
    # 封面
    image = scrapy.Field()
    # 类型
    category_id = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 描述
    description = scrapy.Field()
    # 状态
    status = scrapy.Field()
    # 更新时间
    update_time = scrapy.Field()
    # 小说链接地址
    novel_url = scrapy.Field()

class ChapterItem(scrapy.Item):
    # 书编
    novel_id = scrapy.Field()
    # 章节标题
    title = scrapy.Field()
    # 章节链接地址
    chapter_url = scrapy.Field()
    # 章节内容
    content = scrapy.Field()
    # 小说id
    book_id = scrapy.Field()
    # 插入编号
    insert_num = scrapy.Field()

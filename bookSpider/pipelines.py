# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi
from scrapy.log import err
from scrapy.conf import settings
from bookSpider.items import NovelItem, ChapterItem

class BookspiderPipeline(object):
    def __init__(self):
        # self.client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
        # self.db = self.client[settings['MONGO_DB']]  # 获得数据库的句柄
        # self.novel_coll = self.db[settings['MONGO_NOVEL_COLL']]  # 获得collection的句柄
        # self.chapter_coll = self.db[settings['MONGO_CHAPTER_COLL']]  # 获得collection的句柄

        self.conn = MySQLdb.connect(
            host = settings['MYSQL_HOST'],
            db = settings['MYSQL_DBNAME'],
            user = settings['MYSQL_USER'],
            passwd = settings['MYSQL_PASSWD'],
            charset = 'utf8',
            use_unicode=True
        )
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        if isinstance(item, NovelItem):
            # novelItem = dict(item)
            # self.novel_coll.insert(novelItem)
            try:
                self.cursor.execute(
                    """insert into novel_novel(id_book, book_name, author, category_id, status, image, description,
                                   novel_url, update_time) value (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (
                        item['id_book'],
                        item['book_name'],
                        item['author'],
                        item['category_id'],
                        item['status'],
                        item['image'],
                        item['description'],
                        item['novel_url'],
                        item['update_time']
                    )
                )
                self.conn.commit()
            except Exception as e:
                err(e)
        elif isinstance(item, ChapterItem):
            # chapterItem = dict(item)
            # self.chapter_coll.insert(chapterItem)
            try:
                self.cursor.execute(
                    """insert into novel_chapter(title, chapter_url, content, book_id, insert_num) value (%s, %s, %s, %s, %s)""",
                    (
                        item['title'],
                        item['chapter_url'],
                        item['content'],
                        item['book_id'],
                        item['insert_num']
                    )
                )
                self.conn.commit()
            except Exception as e:
                print(e)
        return item

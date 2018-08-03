# -*- coding: utf-8 -*-
import scrapy
from bookSpider.items import NovelItem, ChapterItem

class NovelSpider(scrapy.Spider):
    name = 'novel'
    allowed_domains = ['www.quanshuwang.com']
    sort_dict = {
        1: '玄幻魔法',
        2: '武侠修真',
        3: '纯爱耽美',
        4: '都市言情',
        5: '职场校园',
        6: '穿越重生',
        7: '历史军事',
        8: '网游动漫',
        9: '恐怖灵异',
        10: '科幻小说',
        11: '美文名著'
    }

    start_urls = [
        'http://www.quanshuwang.com/list/1_1.html',
        # 'http://www.quanshuwang.com/list/2_1.html',
        # 'http://www.quanshuwang.com/list/3_1.html',
        # 'http://www.quanshuwang.com/list/4_1.html',
        # 'http://www.quanshuwang.com/list/5_1.html',
        # 'http://www.quanshuwang.com/list/6_1.html',
        # 'http://www.quanshuwang.com/list/7_1.html',
        # 'http://www.quanshuwang.com/list/8_1.html',
        # 'http://www.quanshuwang.com/list/9_1.html',
        # 'http://www.quanshuwang.com/list/10_1.html',
        # 'http://www.quanshuwang.com/list/11_1.html'
    ]

    # 获取分类小说总页数
    def parse(self, response):
        url = response.xpath("//*[@id='pagelink']/a[@class='first']/@href").extract()[0]

        urls = response.xpath("//a[@class='readTo']/@href").extract()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.get_novel_info)
            break
        # 总页数
        page_total = response.xpath("//*[@id='pagestats']/text()").extract()[0]
        page_total = page_total.split('/')
        pages = int(page_total[-1])
        for page in range(2, pages+1):
            link = url.replace('1.html', (str(page) + '.html'))
            yield scrapy.Request(url=link, callback=self.get_novel_url)
            break

    # 获取每页小说url链接
    def get_novel_url(self, response):
        urls = response.xpath("//a[@class='readTo']/@href").extract()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.get_novel_info)
            break

    # 获取小说信息
    def get_novel_info(self, response):
        item = NovelItem()
        # 小说描述
        description = response.xpath("//meta[6]/@content").extract()[0].strip()
        if '<br />' in description:
            description = description[:-6]
        item['description'] = description
        # 封面
        item['image'] = response.xpath("//meta[7]/@content").extract()[0]
        # 分类
        category = response.xpath("//meta[8]/@content").extract()[0]
        for k in self.sort_dict:
            if category in self.sort_dict[k]:
                item['category_id'] = k
        # 作者
        item['author'] = response.xpath("//meta[9]/@content").extract()[0]
        # 书名
        item['book_name'] = response.xpath("//meta[10]/@content").extract()[0]
        # 状态
        item['status'] = response.xpath("//meta[11]/@content").extract()[0]
        # 最后更新时间
        item['update_time'] = response.xpath("//meta[12]/@content").extract()[0]
        # 链接地址
        item['novel_url'] = response.xpath("//meta[16]/@content").extract()[0]
        # 章节链接
        url = response.xpath("//div[@class='b-oper']/a[@class='reader']/@href").extract()[0]
        strs = url.split('/')
        id = strs[-1]
        item['id_book'] = id
        # 保存数据
        yield item
        yield scrapy.Request(url=url, callback=self.get_chapter_info, meta={'id': id})

    # 所有章节
    def get_chapter_info(self, response):
        chapter_list = response.xpath("//div[@class='chapterNum']/ul//a")
        num = 0
        for chapter in chapter_list:
            num += 1
            # 章节标题
            title = chapter.xpath("string(.)").extract()[0]
            # 章节链接
            url = chapter.xpath("@href").extract()[0]

            yield scrapy.Request(url=url, callback=self.get_chapter_content, meta={
                'title': title,
                'url': url,
                'novel_id': response.meta['id'],
                'num': num,
            })

    # 小说章节内容
    def get_chapter_content(self, response):
        item = ChapterItem()
        item['title'] = response.meta['title']
        item['book_id'] = response.meta['novel_id']
        item['chapter_url'] = response.meta['url']
        content = response.xpath("//div[@id='content']/text()").extract()
        item['content'] = ''.join(content)
        item['insert_num'] = response.meta['num']
        # 保存数据
        yield item

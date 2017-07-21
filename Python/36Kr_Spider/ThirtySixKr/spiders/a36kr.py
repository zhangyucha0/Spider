# -*- coding: utf-8 -*-
import scrapy
import json
import time
import re
from ThirtySixKr.items import ThirtysixkrItem


class A36krSpider(scrapy.Spider):
    name = "36kr"
    allowed_domains = [
        "36kr.com",
        "pic.36krcnd.com"
    ]
    start_urls = [
        # 'http://36kr.com/tags/yiliaojiankang'  # url_typeI---from html (just one page)
        'http://36kr.com/api/tag/yiliaojiankang?',  # url_typeII---from api
        'http://36kr.com/api/tag/rengongzhineng?',
    ]

    # ----- 'url_typeII' next_page handle start -----
    def start_requests(self):
        for eachUrl in A36krSpider.start_urls:
            URL_tag = re.search('tag\/(.*?)\?', eachUrl).group(1)
            URL_per_page_num = '20'
            URL_ts = time.time()  # Normal TimeStamp
            for i in range(1, 4):
                time.sleep(1)
                # API example: http://36kr.com/api/tag/yiliaojiankang?page=2&ts=1500286828&per_page=20&_=1500286832385
                nextPage_url = 'http://36kr.com/api/tag/%(tag)s?page=%(page)s&ts=%(ts)s&per_page=%(per_page)s&_=%(_)s' % {
                    'tag': URL_tag,
                    'page': i,
                    'ts': int(round(URL_ts)),
                    'per_page': URL_per_page_num,
                    '_': int(round(time.time() * 1000))  # Microseconds TimeStamp
                }
                print nextPage_url
                yield self.make_requests_from_url(nextPage_url)

    # ----- 'url_typeII' next_page handle end -----


    def parse(self, response):
        print 'Parse crawl：' + str(response.url)
        # jsonOriginal = re.search('"tagArticles\|post":(.*?)},locationnal={', response.body, re.S).group(1)  # url_typeI deal way
        jsonOriginal = re.search('"items":(.*?),"tagText":"', response.body, re.S).group(1)  # url_typeII deal way
        jsonClear = re.sub('<em class=\'highlight\'>|</em>|&nbsp', '', jsonOriginal)
        jsonData = json.loads(jsonClear)
        # print jsonData[0]['tags']
        for each in jsonData:
            item = ThirtysixkrItem()
            item['platform_website'] = '36Kr'
            origin_news_url = 'http://36kr.com/p/' + str(each['url_code']) + '.html'
            item['origin_news_url'] = origin_news_url
            item['origin_cover_img'] = each['img']  # 类型：链接
            item['title'] = each['title']
            item['author'] = each['author']['display_name']  # 类型：数组
            item['time'] = each['published_at']
            item['tags'] = each['tags']  # 类型：数组
            item['summary'] = each['summary']
            yield scrapy.Request(origin_news_url, meta={'item': item}, callback=self.parse_content)

    def parse_content(self, response):
        item = response.meta['item']
        contentOriginal = re.search('"detailArticle\|post":(.*?),"abTest\|abtest"', response.body, re.S).group(1)
        contentClear = re.sub('&nbsp', '', contentOriginal)
        contentData = json.loads(contentClear)
        item['content'] = contentData['content']
        yield item

# -*- coding:utf8 -*-
import requests
import re
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

class spider(object):
    def __init__(self):
        print u'开始爬取内容。。。'

    # getsource用来获取网页源代码
    def getsource(self, url):
        html = requests.get(url)
        return html.text

    # changepage用来生产不同页数的链接
    def changepage(self, url, total_page):
        now_page = int(re.search('latest_(\d+)\.htm', url, re.S).group(1))
        page_group = []
        for i in range(now_page, total_page + 1):
            link = re.sub('latest_(\d+)\.htm', 'latest_%s.htm' % i, url, re.S)
            page_group.append(link)
        return page_group

    # geteveryclass用来抓取每个块的信息
    def geteveryclass(self, source):
        everyclass = re.findall('(<li class="clear">.*?</li>)', source, re.S)
        return everyclass

    # getinfo用来从每个块中提取出我们需要的信息
    def getinfo(self, eachclass):
        info = {}
        info['url'] = re.search('href="(.*?)"', eachclass, re.S).group(1)
        info['title'] = re.search('data-transition="slide">(.*?)</a>', eachclass, re.S).group(1)
        return info

    # saveinfo用来保存结果到news_link.txt文件中
    def saveinfo(self, classinfo):
        f = open('news_link.txt', 'a')
        for each in classinfo:
            f.writelines('title：' + each['title'] + '\n')
            f.writelines('url：' + 'http://m.cnbeta.com' + each['url'] + '\n')
        f.close()

    def getcontentinfo(self, eachclass):
        news = {}
        news['artical_title'] = re.search('<title>(.*?)...............</title>', eachclass, re.S).group(1)
        news['artical_time'] = re.search('<time class="time">(.*?)</time>', eachclass, re.S).group(1)
        news['artical_summ'] = re.search('<div class="article-summ"><b>...</b>(.*?)</div>', eachclass, re.S).group(1)
        news['artical_cont'] = re.search('<div class="articleCont">(.*?)</div>', eachclass, re.S).group(1)
        return news

    def saveinfo2(self, classinfo):
        f = open('news.txt', 'a')
        for each in classinfo:
            f.writelines('title：' + each['artical_title'] + '\n')
            f.writelines('time：' + each['artical_time'] + '\n')
            f.writelines('summ：' + each['artical_summ'] + '\n')
            f.writelines('cont：' + each['artical_cont'] + '\n\n')
        f.close()


if __name__ == '__main__':
    classinfo = []
    classinfo2 = []
    url = 'http://m.cnbeta.com/list/latest_1.htm'
    cnbetaspider = spider()
    all_links = cnbetaspider.changepage(url, 3) #要爬取的页数（从第一页开始）
    for link in all_links:
        print u'正在处理页面：' + link
        html = cnbetaspider.getsource(link)
        everyclass = cnbetaspider.geteveryclass(html)
        for each in everyclass:
            info = cnbetaspider.getinfo(each)
            contentUrl = cnbetaspider.getsource('http://m.cnbeta.com' + info['url'])
            contentinfo = cnbetaspider.getcontentinfo(contentUrl)
            classinfo2.append(contentinfo)
            classinfo.append(info)
    cnbetaspider.saveinfo(classinfo)
    cnbetaspider.saveinfo2(classinfo2)
    print u'爬取完毕'

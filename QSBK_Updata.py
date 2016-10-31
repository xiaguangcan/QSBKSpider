#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import re
import sys


class QSBK:
    def __init__(self):
        self.pageIndex = 1
        self.totalPage = 2
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64)'
        self.headers = {'User-Agent': self.user_agent}

    # 传入某一页的索引获得页面代码
    def getPage(self, pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接糗事百科失败，错误原因", e.reason
                return None

    # 传入某一页代码，返回本页不带图片的段子列表
    def getPageItems(self, pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "页面加载失败。。。"
            return None
        pattern = re.compile(
            '<div class="author clearfix">.*?<h2>(.*?)</h2>.*?"content">.*?<span>(.*?)</span>.*?</div>.*?number">(.*?)</.*?number">(.*?)</.',
            re.S)
        items = re.findall(pattern, pageCode)
        pageStories = []
        for item in items:
            replaceBR = re.compile('<br/>')
            text = re.sub(replaceBR, "\n", item[1])
            pageStories.append([item[0].strip(), text.strip(), item[2].strip(), item[3].strip()])
        return pageStories

    def start(self):
        reload(sys)
        sys.setdefaultencoding('utf8')

        startPage = raw_input("请输入开始抓取的页码 \n")
        endPage = raw_input("请输入结束抓取的页码 \n")

        self.pageIndex = int(startPage)
        self.totalPage = int(endPage) + 1
        for i in range(self.pageIndex, self.totalPage):
            print "正在抓取第%d页……" % i
            pageStories = self.getPageItems(i)
            self.writeToLog(pageStories, i)

    def writeToLog(self, pageStories, page):
        log = open(str(page) + ".txt", "w")
        for story in pageStories:
            storyContent = "第" + str(page) + "页\t发布人:" + story[0] + "\t赞:" + story[2] + "\t评论:" + story[3] + "\n" + \
                           story[1] + "\n\n"
            log.write(storyContent)
        log.close()


spider = QSBK()
spider.start()

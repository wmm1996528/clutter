from lxml import etree
from redis_queue.DataOutput import data
import re
from redis_queue import redis_db
from setting import *
import requests
import json
class HtmlParser(object):
    def __init__(self):
        self.r = redis_db.RedisQueue('new')
    def parser(self, url, htmls):
        '''
        解析网页
        :param page_url: url
        :param html_cont: content
        :return: url 和数据
        '''
        if htmls == None:
            return
        try:
            h = etree.fromstring(htmls)
        except Exception as e :
            h = etree.HTML(htmls)
        if 'item' in url:
            self._get_datas(url, h)
        else:

            self._get_new_urls(url, h)


    def _get_new_urls(self, url, html):
        try:
            new_urls = []

            lis = html.xpath('//*[@id="plist"]/ul/li/div/div[1]/a')
            for i in lis:
                new_urls.append(BASE_URL + i.get('href'))
            if new_urls:
                self.r.put(new_urls)
        except Exception as e:
            logger.debug('error urls %s ' % e)

    def _get_datas(self,url, html):
        print(html)
        # try:
        #     data.output_mongo(datas)
        # except Exception as e :
        #     logger.debug(e, title, url)
if __name__ == '__main__':
    s = HtmlParser()

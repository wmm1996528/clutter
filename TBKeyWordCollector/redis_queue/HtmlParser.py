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

        if KEYS in url:
            self._get_datas(url, htmls)
        else:

            self._get_new_urls(url, htmls)


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

        try:
            a = re.findall('({"pageName":.+"shopcardOff":false}})', html, re.S)[0]
            js = json.loads(a)
        except Exception as e:
            logger.warning(e, url)
        itemlist = js['mods']['itemlist']['data']['auctions']
        print(len(itemlist))
        for item in itemlist:
            tiltle = item['raw_title']
            detail_url = item['detail_url']
            view_price = item['view_price']
            item_loc = item['item_loc']
            reserve_price = item['reserve_price']
            view_sales = re.findall('\d+',item['view_sales'])[0]
            try:
                comment_count = item['comment_count']
            except:
                comment_count = '0'
            nick = item['nick']
            datas = {
                'tiltle': tiltle,
                'detail_url': detail_url,
                'view_price': view_price,
                'item_loc': item_loc,
                'reserve_price': reserve_price,
                'view_sales': view_sales,
                'comment_count': comment_count,
                'nick': nick,
            }
            try:
                data.output_mongo(datas)
            except Exception as e :
                logger.debug(e, url)
if __name__ == '__main__':
    s = HtmlParser()

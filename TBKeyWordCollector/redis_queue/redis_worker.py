from redis_queue import redis_db
from redis_queue.HtmlDownloader import HtmlDownloader
from redis_queue.HtmlParser import HtmlParser
from multiprocessing import Process
from lxml import etree
import re
from setting import  *
import time
class Worker():
    def __init__(self):
        self.salver = SALVER
        self.r = redis_db.RedisQueue('new')
        self.html = HtmlDownloader()
        self.parser = HtmlParser()
        if self.salver:

            start_urls = 'https://s.taobao.com/search?q={}&app=detailproduct&through=1'.format(KEYS)
            self.r.put(start_urls)

            for i in range(1, PAGE_NUM):
                url = 'https://s.taobao.com/search?data-key=s&data-value=88&ajax=true&_ksTS=1526525628728_733&callback=jsonp734&q={}&imgfile=&ie=utf8&app=detailproduct&through=1&bcoffset=4&p4ppushleft=6%2C48&s={}'.format(
                    KEYS, i * 44)
                self.r.put(url)


    def start(self):
        while True:
            url = self.r.get_wait()
            if url == None:
                break
            html = self.html.download(url)
            self.parser.parser(url, html)
            time.sleep(1)






    def process_start(self):
        threads = []
        t1 = time.time()
        for i in range(PROCESS_NUM):
            t = Process(target=self.start, args=())
            threads.append(t)
        for i in range(len(threads)):
            print('线程% running...' % i)
            threads[i].start()

        for i in range(len(threads)):

            threads[i].join()
            print('线程% close...' % i)
        t2 = time.time()
        print(t2-t1)

    def run(self):
        if PROCESS_BOOL:
            logger.debug('多线程启动')
            self.process_start()
        else:
            logger.debug('单线程启动')
            self.start()
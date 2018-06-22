from redis_queue import redis_db
from redis_queue.HtmlDownloader import HtmlDownloader
from redis_queue.HtmlParser import HtmlParser
from multiprocessing import Process
from lxml import etree
from setting import  *
import time
class Worker():
    def __init__(self):
        self.salver = SALVER
        self.r = redis_db.RedisQueue('new')
        self.html = HtmlDownloader()
        self.parser = HtmlParser()
        if self.salver:
            start_urls = ['https://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain'
                          '=100505&from=page_100505_profile&wvr=6&mod=data&is_hot=1&pagebar=1&pl_name=Pl_Of'
                          'ficial_MyProfileFeed__20&id=1005051713926427&script_uri=/p/1005051713926427/home&feed_typ'
                          'e=0&page={}&pre_page=1&domain_op=100505&__rnd=1526295208644'.format(i) for i in range(200)]
            self.r.put(start_urls)
    def start(self):
        while True:
            url = self.r.get_wait()
            if url == None:
                break
            html = self.html.download(url)
            print(html)
            self.parser._get_datas(url, html)






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
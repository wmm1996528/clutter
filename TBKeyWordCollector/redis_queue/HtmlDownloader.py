import requests
from bs4 import BeautifulSoup
from redis_queue.redis_db import RedisQueue
import time
from setting import *
class HtmlDownloader(object):
    def __init__(self):
        self.__db = RedisQueue('old')
        self.bool = IP_PROXY
        if self.bool == True:
            self.proxy = self._get_ip()
        else:
            self.proxy = None

    def _get_ip(self):
        try:
            # url = 'http://tvp.daxiangdaili.com/ip/?tid=556862908033437&num=1&protocol=https'
            url = 'http://127.0.0.1:8080/ip'
            ip = requests.get(url).text
            proxy = {
                'http': ip,
                'https': ip,
            }



            print(proxy)
            time.sleep(1)
        except Exception as e:
            logger.debug(e)
            proxy = None
        return proxy

    def download(self, url):
        self.url = url
        if url is None:
            return None



        # s.cookies['antipas'] = '0197P302a7312G67X8X30'
        while True:
            try:
                res = requests.get(self.url, headers=HEADERS, proxies=self.proxy, timeout=2)
                if res.status_code == 200:
                    self.__db.put_old(url)
                    if len(res.text) > 1000:
                        return res.text
                    else:
                        continue
                else:
                    logger.debug(res.status_code)
                    print(res.url)
            except Exception as e:
                self.proxy = self._get_ip()
                logger.debug(e)


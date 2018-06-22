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

    def get_cookie(self):
        # try:
        #     # url = 'http://tvp.daxiangdaili.com/ip/?tid=556862908033437&num=1&protocol=https'
        #     url = 'http://127.0.0.1:8080/cookie'
        #     ip = requests.get(url).text
        #     time.sleep(1)
        # except Exception as e:
        #     logger.debug(e)
        #     cookie = None
        cookie = {'ALC': 'ac%3D2%26bt%3D1526355964%26cv%3D5.0%26et%3D1557891964%26ic%3D2071432238%26scf%3D%26uid%3D5293962012%26vf%3D0%26vs%3D0%26vt%3D0%26es%3D512607409583f4a7c3fb92817227ec04', 'LT': '1526355964', 'tgc=TGT-NTI5Mzk2MjAxMg=': '-1526355964-tc-AB18B725FE0528CB4020787769C32FA0-1', 'SRF': '1526355964', 'SRT': 'D.QqHBJZ4qQ-bbVrMb4cYGS4uiiFoEdOb95!suTZSHNEYdPdbfidkpMERt4EPKRcsrA4uJPQSTTsVuObicRcS6dbi!KdPIUEEwiOSQNPJnSZSJNCr-5eArS4V-*B.vAflW-P9Rc0lR-ykcDvnJqiQVbiRVPBtS!r3JZPQVqbgVdWiMZ4siOzu4DbmKPWfSEbji!YeS!MoAciCO!yQN4usTr0-i49ndDPIJcYPSrnlMc0kMOEISOMOU3f3S4kwJcM1OFyHMPHJ5mkiOmHII4noINsJ5mkiOmHIO4noN-uJ5mkiODmkJ!noTmHJ5mkoODEIU!noJ8sJ5mkoODEIU!noJ8sa', 'ALF': '1557891964', 'SCF': 'Aun5_3FcjENIR1pYls_Qr6y8x-UN04rYryBXa64Ddm-xiiK5XhtoRDEvP6YKpfxhwupnYdkjmaXQN6_k9sv6SJM.', 'SUB': '_2A253_iesDeRhGeNM4lEY9izMyj6IHXVUih5krDV8PUNbmtANLUvZkW9NSfbfoZSd9eKlQz56WIS0f6LH-6zt4eG6', 'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9WhdYl6HgfDqBcBNOWINukO65JpX5K2hUgL.Fo-E1Ke4Soz7eKz2dJLoIERLxKMLBK-L1--LxKMLBKML1KnLxKML1-2L1hBLxKqL1KnL12-LxKqL1KnL12-_', 'sso_info=v02m6alo5qztKWRk5ylkJOUpY6UlKWRk5ylkJOcpY6ToKWRk5yljpSEpY6DkKWRk5iljpOgpY6ElKWRk5iljpOgpY6ElK2Jp5WpmYO0tYyjpLOOk5iyjIOEsg': '=', 'SSOLoginState': '1526355964', 'SUHB': '03oFymq0CvSjZb', 'wvr': '6', 'login': '13a0857768fc0c0abafd3d70c0f4538a', 'YF-Ugrow-G0': 'ad83bc19c1269e709f753b172bddb094', 'YF-V5-G0': '5468b83cd1a503b6427769425908497c'}
        return cookie
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

        headers = {
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'Accept-Encoding': 'gzip, deflate, br',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
        }

        # s.cookies['antipas'] = '0197P302a7312G67X8X30'
        while True:
            try:
                res = requests.get(self.url, headers=headers, proxies=self.proxy, timeout=2, cookies=self.get_cookie())
                if res.status_code == 200:
                    self.__db.put_old(url)
                    print(res.text)
                    return res.text
                else:
                    logger.debug(res.status_code)
                    print(res.url)
            except Exception as e:
                # self.proxy = self._get_ip()
                logger.debug(e)


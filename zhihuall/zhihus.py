import requests

from pymongo import MongoClient
from multiprocessing import Process
from threading import Thread
import gevent
from termcolor import colored
# requests.adapters.DEFAULT_RETRIES = 5
import random
import threading

requests.packages.urllib3.disable_warnings()
class ZhihuSpider():
    def __init__(self):
        self.headers={
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'

        }
        # self.
        self.conn = MongoClient('mongodb://127.0.0.1:27017')
        self.coll = self.conn['zhihu']
        self.db = self.coll.infos
        # self.conn = pymysql.connect('localhost','root', '123456', 'zhihu')
        # self.cursor = self.conn.cursor()
        # self.cursor.execute('''CREATE TABLE info(
        #                     headline VARCHAR(255),
        #                     url_token VARCHAR(30),
        #                     avatar_url VARCHAR(30),
        #                     name VARCHAR(30),
        #                     message_thread_token VARCHAR(30),
        #                     description VARCHAR(255),
        #                     company VARCHAR(255),
        #                     business VARCHAR(255),
        #                     school VARCHAR(30),
        #                     location VARCHAR(30)
        #                     );
        #                     ''')
        # self.conn.commit()
        self.proxy = self.get_ip()
    def get_ip(self):
        ip = ''
        while ip == '':
            try:
                url = 'http://tvp.daxiangdaili.com/ip/?tid=556862908033437&num=1&protocol=https&category=2'
                ip = requests.get(url, verify=False).text
                proxy = {
                    'http': 'http://' + ip,
                    'https': 'https://' + ip
                }
                url2 = 'http://httpbin.org/ip'

                res = requests.get(url2, proxies=proxy, verify=False)
                origin = res.json()['origin']
                if ip == origin:

                    return proxy
            except:
                pass

    def start(self, n):
        print('--------------------正在爬 %s------------------' % n)
        url = 'https://www.zhihu.com/api/v4/members/kaifulee/followers?include=data%5B%2A%5D.locations%2Cemployments%2Cgender%2Ceducations%2Cbusiness%2Cvoteup_count%2Cthanked_Count%2Cfollower_count%2Cfollowing_count%2Ccover_url%2Cfollowing_topic_count%2Cfollowing_question_count%2Cfollowing_favlists_count%2Cfollowing_columns_count%2Cavatar_hue%2Canswer_count%2Carticles_count%2Cpins_count%2Cquestion_count%2Ccommercial_question_count%2Cfavorite_count%2Cfavorited_count%2Clogs_count%2Cmarked_answers_count%2Cmarked_answers_text%2Cmessage_thread_token%2Caccount_status%2Cis_active%2Cis_force_renamed%2Cis_bind_sina%2Csina_weibo_url%2Csina_weibo_name%2Cshow_sina_weibo%2Cis_blocking%2Cis_blocked%2Cis_following%2Cis_followed%2Cmutual_followees_count%2Cvote_to_count%2Cvote_from_count%2Cthank_to_count%2Cthank_from_count%2Cthanked_count%2Cdescription%2Chosted_live_count%2Cparticipated_live_count%2Callow_message%2Cindustry_category%2Corg_name%2Corg_homepage%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=20&offset={}'
        url = url.format(n)


        # self.session.get('https://www.zhihu.com', headers=self.headers)
        self.session = requests.session()
        while  True:

            try:
                s = [
                    "2|1:0|10:1526288234|4:z_c0|92:Mi4xMnhKOEFBQUFBQUFBc0dfTy1IcUlEU1lBQUFCZ0FsVk5hcDNtV3dEZVh4ajV2cUNfQnJmT25vQkxkc1doc1ZIYzdR|537c48594ee22687834a4c79db6ef9e95414f0e01f1cd44542ef157ad9afca5f"
                ]
                cookie = s.pop()
                cookies = {
                    'z_c0': cookie
                }
                print(self.proxy)
                res = self.session.get(url, headers=self.headers, proxies=self.proxy, cookies=cookies, verify=False)
                data = res.json()
                for i in data['data']:
                    for j, d in i.items():
                        if d == False:
                            i[j] = '无'

                self.db.insert(data['data'])
                print('\033[;33;m %s 成功' % n)
                s.append(cookie)
                break

            except KeyError :
                print('ip错误')
                print(res.text)
                self.proxy = self.get_ip()
            except Exception as e:
                print(colored('错误信息：%s' % e, 'red'))

                print(colored('流量异常','green'))
                self.proxy = self.get_ip()








if __name__ == '__main__':

    count = 1050000
    login = ZhihuSpider()
    class zhihuThread(Process):
        def __init__(self, que):
            Process.__init__(self)
            self.que = que

        def run(self):
            length = len(self.que)
            glen = 20
            num = length // glen
            for i in range(glen+1):
                jobs = []
                if i == 0:
                    l = 0
                else:
                    l = (i - 1) * num
                r = i * num
                for j in self.que[l:r]:
                    jobs.append(gevent.spawn(login.start, j))
                gevent.joinall(jobs)
    TOTALNUM = 1000000// 20
    num = TOTALNUM // 10
    listss = [i * 20 for i in range(TOTALNUM)]
    for i in range(100):
        if i ==0:
            lists = listss[:num]
        elif i==100:
            lists = listss[i*num:]
        else:
            lists = listss[i*num:(i+1)*num]
        thread_list = []
        num2 = num//100
        for i in range(100):
            if i == 0:
                urls = lists[:num2]
            elif i == 100:
                urls = lists[i * num2:]
            else:
                urls = lists[i * num2:(i + 1) * num2]
            thread_list.append(zhihuThread(urls))
        for i in range(len(thread_list)):
            print('------------------------第%s个线程启动了---------------------------------' % i)
            thread_list[i].start()
        for i in range(len(thread_list)):
            thread_list[i].join()


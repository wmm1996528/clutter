import logging
logger = logging.getLogger('module')
#设置是否为生产端
# True 生产
# None 消费者
SALVER = True
if SALVER:
    REDIS_URL = "redis://localhost:6379"
else:
    REDIS_URL = "redis://192.168.2.171:6379"


BASE_URL = 'https:'


DATABASE_NAME ='taobao'
TABLE_NAME = 'detail'
#设置最大线程数
PROCESS_BOOL = False
PROCESS_NUM = 10

#设置是否启用代理ip
IP_PROXY = False

#UA
HEADERS = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
        }
KEYS = 'iphonex'

PAGE_NUM = 50
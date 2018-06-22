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


DATABASE_NAME ='weibo'
TABLE_NAME = 'sina'
#设置最大线程数
PROCESS_BOOL = False
PROCESS_NUM = 10

#设置是否启用代理ip
IP_PROXY = False

#设置是否携带cookie
COOKIE_BOOL= False

import os
from redis_worker import Worker


class work(Worker):
    pass

s = work()
s.run()
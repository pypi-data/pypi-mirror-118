#!/usr/bin/env python 
# coding=utf-8
# @Time : 2021/3/12 11:34 
# @Author : HL 
# @Site :  
# @File : DatabaseRedis.py 
# @Software: PyCharm
import redis

redis_host = '172.20.1.10'


class redisDatabase():

    def __init__(self, host=redis_host, port=6379, password="", db=0):
        '''
        这种连接是连接一次就断了，耗资源.端口默认6379，就不用写
        r = redis.Redis(host='127.0.0.1',port=6379,password='tianxuroot')
        r.set('name','root')
        print(r.get('name').decode('utf8'))
        '''
        '''
        连接池：
        当程序创建数据源实例时，系统会一次性创建多个数据库连接，并把这些数据库连接保存在连接池中，当程序需要进行数据库访问时，
        无需重新新建数据库连接，而是从连接池中取出一个空闲的数据库连接
        '''
        self.pool = redis.ConnectionPool(host=host, port=port, password=password, db=db,
                                         decode_responses=True)  # 实现一个连接池
        # self.redis = redis.Redis(connection_pool=self.pool)
        # r.set('foo', 'bar')
        # print(r.get('foo').decode('utf8'))

    # 已写方法不足是，直接返回一个redis链接
    def get_redis(self):
        r = redis.Redis(connection_pool=self.pool)
        return r

    """String数据类型"""

    def str_set(self, name, value, ex=None, px=None, nx=False, xx=False):
        """
        string类型，像数据库存值
        :param name: key
        :param value: values
        :param ex: 过期时间（秒） 时间结束后，键值就变成None
        :param px: 过期时间（毫秒）时间结束后，键值就变成None
        :param nx: 如果设置为True，则只有name不存在时，当前set操作才执行
        :param xx: 如果设置为True，则只有name存在时，当前set操作才执行
        :return:
        """
        r = redis.Redis(connection_pool=self.pool)
        r.set(name, value, ex=ex, px=px, nx=nx, xx=xx)

    # String数据提取
    def str_get(self, name):
        r = redis.Redis(connection_pool=self.pool)
        r.get(name)

    def str_click_incr(self, name, amount=None):
        """
        应用场景 – 页面点击数 自增
        :param name: 键值
        :param amount: 自增数
        :return:
        """
        r = redis.Redis(connection_pool=self.pool)
        if amount is None:
            r.incr(name)
        else:
            r.incr(name, amount)

    def str_click_descr(self, name, amount=None):
        """
        应用场景 – 页面点击数 自减
        :param name: 键值
        :param amount: 自减数
        :return:
        """
        r = redis.Redis(connection_pool=self.pool)
        if amount is None:
            r.decr(name)
        else:
            r.decr(name, amount)

    # 在redis name对应的值后面追加内容
    def str_append(self, name, value):
        r = redis.Redis(connection_pool=self.pool)
        r.append(name, value)




    """set数据类型"""

    def saveSet(self, setName, value):
        r = redis.Redis(connection_pool=self.pool)
        n = r.sadd(setName, value)
        return n

    def readSet(self, setName):
        r = redis.Redis(connection_pool=self.pool)
        n = r.smembers(setName)
        return n


# if __name__ == '__main__':
#     # redisDatabase().saveSet('redis_data_demo', '实验13')
#     redisDatabase().str_click_num('visit:12306:totals11', 100)

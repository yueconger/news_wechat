# -*- encoding: utf-8 -*-
"""
@File    : proxy_ip_redispool.py
@Time    : 2021/4/15 11:42
@Author  : yuecong
@Email   : yueconger@163.com
@Software: PyCharm
"""
import requests, redis
import pandas
import random

from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
import logging

db_conn = redis.ConnectionPool(host="127.0.0.1", port=6379, password="", db=6)
redis_conn = redis.Redis(connection_pool=db_conn, max_connections=10)


# 删除redis数据库里的ip
def remove_ip(ip, redis_conn):
    redis_conn.zrem("IP", ip)
    print("已删除 %s..." % ip)


# 获取redis数据库里一共有多少ip
def get_ip_num(redis_conn):
    num = redis_conn.zcard("IP")
    return num


# 获取ip的端口
def get_port(ip, redis_conn):
    port = redis_conn.zscore("IP", ip)
    port = str(port).replace(".0", "")
    return port


# 添加ip和端口到数据库里
def add_ip(ip, port, redis_conn):
    # nx: 不要更新已有的元素。总是添加新的元素,只有True，False
    redis_conn.zadd("IP", {ip: port}, nx=55)
    print("已添加 %s %s...ok" % (ip, port))


# 列出所有的ip
def get_all_ip(redis_conn):
    all_ip = redis_conn.zrange("IP", 0, -1)
    return all_ip


# 随机获取一个ip
def get_random_ip(redis_conn):
    end_num = get_ip_num(redis_conn)
    num = random.randint(0, end_num)
    random_ip = redis_conn.zrange("IP", num, num)
    if not random_ip:
        return "", ""
    random_ip = str(random_ip[0]).replace("b", '').replace("'", "")
    port = get_port(random_ip, redis_conn)
    return random_ip, port


# 获取代理ip
def spider_ip(x, redis_conn):
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), x)
    for p in range(1, 20):
        res = pandas.read_html("http://www.89ip.cn/index_{}.html".format(p))
        # print(res)
        # print(type(res[0]))
        for i in range(len(res[0])):
            ip = res[0].iloc[i, 0]
            port = res[0].iloc[i, 1]
            print("ip", ip)
            print("port", port)
            add_ip(str(ip), str(port), redis_conn)


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='log1.txt',
                    filemode='a')


def aps_detection_ip(x, redis_conn):
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), x)
    res = get_random_ip(redis_conn)
    ip = res[0]
    port = res[1]
    try:
        requests.get("http://www.baidu.com", proxies={'https': '{ip}:{port}'.format(ip=ip, port=port)}, timeout=2)
        print("可用", ip, port, res)
    except Exception:
        # ip错误失效就删除
        remove_ip(ip, redis_conn)


scheduler = BlockingScheduler()
scheduler.add_job(func=aps_detection_ip, args=('检测循环任务0', redis_conn), trigger='interval', seconds=1,
                  id='aps_detection_ip_task', max_instances=10)
scheduler.add_job(func=spider_ip, args=('获取循环任务0', redis_conn), trigger='interval', seconds=60 * 60 * 2,
                  id='spider_ip_task', max_instances=10)

scheduler._logger = logging

# scheduler.start()
if __name__ == '__main__':
    # print(get_ip_num())
    spider_ip("获取循环任务", redis_conn)
    scheduler.start()
    # aps_detection_ip("检测循环任务")

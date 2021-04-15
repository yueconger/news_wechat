# -*- coding: utf-8 -*-

import logging.handlers
import logging
import os
import sys
import time

def creat_time_os():
    creat_time = time.strftime("%Y-%m-%d", time.localtime())

    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

    log_path_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    logs_path = os.path.join(log_path_dir, "logs", creat_time)
    if os.path.exists(logs_path):
        # print("日志路径已存在,不需创建")
        return logs_path
    else:
        os.makedirs(logs_path)
        # print("日志路径创建完毕!")
        return logs_path


# 提供日志功能
class logger:
    logs_path = creat_time_os()

    # 日志文件名：由用例脚本的名称，结合日志保存路径，得到日志文件的绝对路径
    logname = os.path.join(logs_path, sys.argv[0].split('/')[-1].split('.')[0]) + '.log'

    # 初始化logger
    log = logging.getLogger()
    # 日志格式，可以根据需要设置
    fmt = logging.Formatter('[%(asctime)s][%(filename)s][line:%(lineno)d][%(levelname)s] %(message)s',
                            '%Y-%m-%d %H:%M:%S')

    # 日志输出到文件，这里用到了上面获取的日志名称，大小，保存个数
    handle1 = logging.handlers.RotatingFileHandler(logname, maxBytes=1024 * 1024 * int(8), encoding='utf-8', backupCount=int(2))
    handle1.setFormatter(fmt)
    # 同时输出到屏幕，便于实施观察
    handle2 = logging.StreamHandler(stream=sys.stdout)
    handle2.setFormatter(fmt)
    log.addHandler(handle1)
    log.addHandler(handle2)

    # 设置日志基本，这里设置为INFO，表示只有INFO级别及以上的会打印
    log.setLevel(logging.INFO)

    # 日志接口，用户只需调用这里的接口即可，这里只定位了INFO, WARNING, ERROR三个级别的日志，可根据需要定义更多接口

# -*- encoding: utf-8 -*-
"""
@File    : get_requests.py
@Time    : 2021/4/13 14:23
@Author  : yuecong
@Email   : yueconger@163.com
@Software: PyCharm
"""
import requests
requests.packages.urllib3.disable_warnings()
from utils.log_custom import logger

log = logger.log


class GetRequests():
    def __init__(self):
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
        }

    # 发送请求
    def req_custom(self, method='GET', url=None, headers=None, params=None, data=None, data_type=None, proxies=None,
                   **kwargs):
        response = None
        # s = requests.session()
        s = requests
        try:
            for i in range(3):
                if method == 'GET':
                    response = s.get(url=url, headers=headers, proxies=proxies, params=params, verify=False)
                if method == 'POST' and data_type == 'json_type':
                    response = s.post(url=url, headers=headers, json=data, proxies=proxies, timeout=30,
                                      verify=False)
                if method == 'POST' and data_type == None:
                    response = s.post(url=url, headers=headers, data=data, proxies=proxies, verify=False)
                if response.status_code == 200:
                    # log.info('第%s次请求成功,返回状态码为：%s' % (i, response.status_code))
                    return response
                elif 200 < response.status_code < 400:
                    # log.warning('第%s次请求网站重定向，返回状态码为：%s' % (i, response.status_code))
                    continue
                elif 400 < response.status_code < 500:
                    # log.warning('第%s次请求网站接口出错，请求返回状态码为：%s' % (i, response.status_code))
                    continue
                elif response.status_code == 500:
                    # log.warning('第%s次请求网站出错，请求返回状态码为：%s' % (i, response.status_code))
                    continue
        except Exception as e:
            log.error(e)
            return ''
# -*- encoding: utf-8 -*-
"""
@File    : get_detail_info.py
@Time    : 2021/4/13 9:08
@Author  : yuecong
@Email   : yueconger@163.com
@Software: PyCharm
"""

import time
from threading import Thread
from queue import Queue
import json
from lxml import etree
from utils.get_requests import GetRequests
from utils.log_custom import logger
from utils.common_process_function import rule_dict_fix, \
    standard_time, elem_2_str, fix_docClob, fix_content_txt, fix_pictures, fix_title
from utils.rules_wechat_article import all_rule_dict

log = logger.log

req_custom = GetRequests().req_custom


class GetWeChatArticle():
    def __init__(self):
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
        }

    def download_item(self):
        pass

    def get_detail(self, url):
        response = req_custom(url=url, headers=self.headers)
        log.info(response.status_code)
        source_code_str = response.content.decode()
        need_item = rule_dict_fix(all_rule_dict, source_code_str)
        item = self.get_item_process(need_item, source_code_str)
        return item

    def get_item_process(self, need_item: dict, source_code_str):
        new_item = need_item
        url = new_item['url']
        new_item['html'] = source_code_str
        for fix_item_key, fix_item_value in need_item.items():
            if fix_item_key == 'detail':
                # 处理正文
                detail = elem_2_str(fix_item_value)
                fix_item_value = fix_docClob(url, detail)
            elif fix_item_key == 'title':
                # 处理标题
                fix_item_value = fix_title(fix_item_value)
            elif fix_item_key == 'content_text':
                # 处理纯文本
                content_text = elem_2_str(fix_item_value)
                fix_item_value = fix_content_txt(content_text)
            elif fix_item_key == 'release_time':
                # 处理日期
                fix_item_value = standard_time(fix_item_value)
            elif fix_item_key == 'pictures':
                # 处理图片
                fix_item_value = fix_pictures(fix_item_value)

            new_item[fix_item_key] = fix_item_value
        return new_item


if __name__ == '__main__':
    get_detail_wechat_article = GetWeChatArticle()
    url = "https://mp.weixin.qq.com/s?__biz=MzAwMTU0MDI5OQ==&amp;mid=2659050665&amp;idx=1&amp;sn=b97f30881bf5baf2f6a007373fddb9c1&amp;chksm=81516d0db626e41b5ca201f882744788c3641c11451c5a3617f81389dc2c76ff8abaa18d7283&amp;scene=27#wechat_redirect"
    get_detail_wechat_article.get_detail(url)

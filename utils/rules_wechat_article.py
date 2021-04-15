# -*- encoding: utf-8 -*-
"""
@File    : rules_wechat_article.py
@Time    : 2021/4/13 16:44
@Author  : yuecong
@Email   : yueconger@163.com
@Software: PyCharm
公众号用
"""
all_rule_dict = {
    'title': {'xpath_1': '//meta[@property="og:title"]/@content'},
    'url': {'xpath_1': '//meta[@property="og:url"]/@content'},
    'digest': {'xpath_1': '//meta[@property="og:description"]/@content'},
    'author': {'xpath_1': '//meta[@property="og:article:author"]/@content'},
    'release_time': {'regex': 'var ct = ["\'](\d{10})["\'];|getXmlValue\(\'ori_create_time\.DATA\'\) : \'(\d{10})\';'},
    'detail': {'xpath_2': '//div[@id="js_content"]'},
    'content_text': {'xpath_2': '//div[@id="js_content"]'},
    'pictures': {'xpath_2': '//div[@id="js_content"]//@data-src'},
    'source_url': {'regex': 'var msg_source_url = ["\'](.*?)["\'];'},
}

if __name__ == '__main__':
    for k, v in all_rule_dict.items():
        print(k, v.keys())
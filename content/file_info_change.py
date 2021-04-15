# -*- encoding: utf-8 -*-
"""
@File    : file_info_change.py
@Time    : 2021/4/13 9:09
@Author  : yuecong
@Email   : yueconger@163.com
@Software: PyCharm
公众号用
"""
from content.get_detail_info import GetWeChatArticle
from utils.common_process_function import datetime_now
from utils.iot_source_info import bid_source_info
import json
import time
from utils.log_custom import logger
log = logger.log
get_detail_wechat_article = GetWeChatArticle()

def search_bid_source(source):
    """
    从查询并匹配公众号名称和唯一id关系
    :param source:
    :return:
    """
    for bid_source in bid_source_info:
        if source == bid_source['nick_name']:
            wechat_id = bid_source['wechat_id']
            bid = bid_source['bid']
            nickname = source
            service_type = bid_source['service_type']
            return nickname, wechat_id, bid, service_type
    else:
        return '', '', '', ''


def get_item(source, wechat_id, fakeid, url, source_url, cover_picture, title, digest, author, nickname, service_type):
    """
    字段处理
    :param source:
    :param wechat_id:
    :param fakeid:
    :param url:
    :param source_url:
    :param cover_picture:
    :param title:
    :param digest:
    :param author:
    :return:
    """
    item = {}
    item['source'] = source
    item['wechat_id'] = wechat_id
    item['fakeid'] = fakeid
    item['url'] = url
    item['source_url'] = source_url
    item['cover_picture'] = cover_picture
    item['title'] = title
    item['digest'] = digest
    item['author'] = author
    item['nickname'] = nickname
    item['service_type'] = service_type
    return item


def get_content_info(content_info_list, source, wechat_id, fakeid, nickname, service_type):
    """
    获取内容
    :param content_info_list:
    :param source:
    :param wechat_id:
    :param fakeid:
    :return: 单个公众号的近期数据 列表形式
    """
    item_list = []
    for content_info in content_info_list:
        if type(content_info) is list:
            for content_info_inner in content_info:
                app_msg_ext_info = content_info_inner.get('app_msg_ext_info')
                url = app_msg_ext_info.get('content_url')
                source_url = app_msg_ext_info.get('source_url')
                cover_picture = app_msg_ext_info.get('cover')
                title = app_msg_ext_info.get('title')
                digest = app_msg_ext_info.get('digest')
                author = app_msg_ext_info.get('author')
                item_first = get_item(source, wechat_id, fakeid, url, source_url, cover_picture, title, digest, author, nickname, service_type)
                item_list.append(item_first)
                if len(app_msg_ext_info.get('multi_app_msg_item_list')) > 0:
                    # 多篇文章
                    multi_app_msg_item_list = app_msg_ext_info.get('multi_app_msg_item_list')
                    for multi_app_msg_item in multi_app_msg_item_list:
                        title = multi_app_msg_item.get('title')
                        digest = multi_app_msg_item.get('digest')
                        url = multi_app_msg_item.get('content_url')
                        source_url = multi_app_msg_item.get('source_url')
                        cover_picture = multi_app_msg_item.get('cover')
                        author = multi_app_msg_item.get('author')
                        item = get_item(source, wechat_id, fakeid, url, source_url, cover_picture, title, digest,
                                        author, nickname, service_type)
                        item_list.append(item)
    return item_list


def file_info(file_path):
    count = 1
    with open(file_path, 'r', encoding='utf-8') as f:
        content_list = f.readlines()

    for i in range(int(len(content_list) / 2)):
        source = content_list[i * 2].strip()
        content_info = content_list[i * 2 + 1].strip()
        nickname, wechat_id, bid, service_type = search_bid_source(source)
        log.info('source="%s", wechat_id="%s", bid="%s"' % (source, wechat_id, bid))
        content_info_list = json.loads(content_info)
        item_list = get_content_info(content_info_list, source, wechat_id, bid, nickname, service_type)
        for wechat_item in item_list:
            url = wechat_item.get('url')
            item = get_detail_wechat_article.get_detail(url)
            wechat_item.update(item)
            create_time = datetime_now()
            wechat_item['create_time'] = create_time
            wechat_item['update_time'] = create_time
            wechat_item['get_way'] = '1'
            wechat_item['website_type_id'] = '3'
            log.info('第%s条数据'% count)
            log.info('当前数据source="%s", url="%s", title="%s", release_time="%s"' % (wechat_item.get('source'),
                wechat_item.get('url'), wechat_item.get('title'), wechat_item.get('release_time')))
            with open(r'E:\projects_online\wechat_articles_spider\docs\result_0414_02.json', 'a+', encoding='utf-8') as wf:
                wf.write(json.dumps(wechat_item, ensure_ascii=False) + '\n')
            count += 1
            time.sleep(0.5)


if __name__ == '__main__':
    file_path = r'E:\projects_online\wechat_articles_spider/test/iot_source_histoty.txt'
    file_info(file_path)

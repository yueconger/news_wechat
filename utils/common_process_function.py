# -*- encoding: utf-8 -*-
"""
@File    : common_process_function.py
@Time    : 2021/4/13 16:20
@Author  : yuecong
@Email   : yueconger@163.com
@Software: PyCharm
"""
import re
import time
from datetime import datetime
from lxml import etree
from utils.Tomd import Tomd
from utils import qcbq, ttomd
from utils.log_custom import logger

log = logger.log


def standard_time(input_time: str):
    """
    时间戳标准化输出
    :param input_time:
    :return:
    """
    result = '1970-01-01 00:00:00'
    if input_time:
        input_time = input_time.strip()
        try:
            result = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(input_time)))
        except TypeError as e:
            pass
    return result


def datetime_now():
    """
    当前时间 %Y-%m-%d %H:%M:%S
    :return:
    """
    datetime_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return datetime_now


def fix_pictures(pictures):
    """
    修复图片问题
    :param pictures:
    :return:
    """
    new_picture_list = []
    if pictures:
        for picture in pictures:
            result = re.findall('/icon', picture)  # |\.gif 微信公众号不能替换掉gif
            if result:
                pass
            else:
                new_picture_list.append(picture)

    return list(tuple(new_picture_list))


def regex_fix(source_code_str: str, pattern: str):
    """
    正则匹配获取, 返回匹配到的第一个值
    :param source_code_str:
    :param pattern:
    :return:
    """
    regex_list = re.findall(pattern, source_code_str)
    if regex_list:
        return regex_list[0]
    else:
        return ''


def xpath_many_fix(html_element, xpath: str):
    """
    xpath结果 返回多个匹配结果
    :param html_element:
    :param xpath:
    :return:
    """
    result_list = html_element.xpath(xpath)
    return result_list


def xpath_fix(html_element, xpath: str):
    """
    xpath匹配, 返回匹配到的第一个值
    :param html_element:
    :param xpath:
    :return:
    """
    result_list = html_element.xpath(xpath)
    if result_list:
        if isinstance(result_list[0], str):
            return result_list[0]
        else:
            return etree.tostring(result_list[0], encoding="utf-8").decode("utf-8")
    else:
        return ''


def elem_2_str(elem):
    if len(elem) > 1:
        elem = ''.join(elem)
    elif len(elem) == 0:
        elem = ''
    else:
        elem = elem[0]
    result = ''
    try:
        result = etree.tostring(elem, encoding="utf-8").decode("utf-8")
    except Exception as e:
        log.error("转化失败 %s" % e)
    return result


def get_html_element(source_code_str: str):
    """
    str型源码, 经 lxml 转为节点内容(element类型)
    :param source_code_str:
    :return:
    """
    html_element = etree.HTML(source_code_str)
    return html_element


def rule_dict_fix(all_rule_dict: dict, source_code_str: str):
    html_element = get_html_element(source_code_str)
    need_item = {}
    for k, v in all_rule_dict.items():
        need_key = k
        if 'xpath_1' in v.keys():
            need_value = xpath_fix(html_element, v.get('xpath_1'))
        elif 'xpath_2' in v.keys():
            need_value = xpath_many_fix(html_element, v.get('xpath_2'))
        elif 'regex' in v.keys():
            need_value = regex_fix(source_code_str, v.get('regex'))
        else:
            need_value = ''
        need_item[need_key] = need_value
    return need_item


# 处理标题
def fix_title(title):
    title = title.strip().replace('\u3000', ' ')
    title = re.sub('\n|\u200b', '', title)
    title = re.sub('\t|\r', '', title)
    title = title.encode("utf-8").decode("utf-8")
    return title


# 处理html标签类型的内容
def fix_docClob(url, docClob):
    if docClob:
        docClob = docClob.encode("utf-8").decode("utf-8")
        docClob = re.sub('<!--[\w\W]*?-->', '', docClob)
        docClob = re.sub('<meta name="ContentEnd[\w\W]*?</table>', '', docClob)
        docClob = re.sub('<iframe[\w\W]*?</iframe>', '', docClob)
        docClob = re.sub('<style[\w\W]*?</style>', '', docClob)
        docClob = re.sub('<video[\w\W]*?</video>', '', docClob)
        docClob = re.sub('<audio[\w\W]*?</audio>', '', docClob)
        docClob = re.sub('<div style="display:none"[\w\W]*?</div>', '', docClob)
        detail = Tomd(url).getMarkdown(docClob).replace('\xa0\n', '').replace('\n\n\n', '\n').replace(
            '\u3000\u3000\n',
            '').replace(
            '\u3000', '')
        # detail = re.sub('/table(?!>)', '/table>', detail)
        # detail = detail.replace('\n', '<br>')
        detail = re.sub('%20', '', detail)
        detail = re.sub('\[关闭\]\(javascript\:void\\\\\(0\\\\\)\)', '', detail)
        return detail
    else:
        detail = ""
        return detail


# 处理纯文本
def fix_content_txt(content_text):
    content_text = content_text.encode("utf-8").decode("utf-8")
    content_text = re.sub('<!--[\w\W]*?-->', '', content_text)
    content_text = re.sub('<script[\w\W]*?</script>', '', content_text)
    content_text = re.sub('<meta name="ContentEnd[\w\W]*?</table>', '', content_text)
    content_text = re.sub('<iframe[\w\W]*?</iframe>', '', content_text)
    content_text = re.sub('<style[\w\W]*?</style>', '', content_text)
    content_text = re.sub('<video[\w\W]*?</video>', '', content_text)
    content_text = re.sub('<audio[\w\W]*?</audio>', '', content_text)
    content_text = re.sub('<o:p>|</o:p>', '', content_text)
    content_text = ttomd.Tomd(content_text).delete_info()
    content_text = qcbq.filterHtmlTag(content_text)
    content_text = re.sub('<!.*?->', '', content_text)
    content_text = content_text.replace('*', '').replace(' \n', '').replace('\n\n', '\n').replace(
        '\u3000\u3000\n', '').replace(
        '\u3000', '')
    content_text = content_text.strip()
    # content_text = re.sub('\n|\t|\r', '', content_text)
    content_text = re.sub('%20', '', content_text)
    return content_text


# 处理临时详情
def fix_detail_tmp(detail):
    detail_tmp = re.sub('\n|\t|\r', '', detail)
    detail_tmp = detail_tmp.strip()
    return detail_tmp


if __name__ == '__main__':
    pass

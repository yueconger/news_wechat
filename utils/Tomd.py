#coding:utf-8
import html2text as ht
from urllib import parse
import re


class Tomd:
    def __init__(self, website):
        self.text_maker = ht.HTML2Text(bodywidth=0)
        self.website = website

    def searchTable(self,detailhtml,Sstr,Estr):
        tPreIndex = []
        tEndIndex = []
        # 文件中的table位置
        tStr = []
        b = []
        for a in re.finditer(Sstr, detailhtml):
            b.append([i for i in a.span()])
        for i in b:
            tPreIndex.append(i[0])
        c = []
        for a in re.finditer(Estr, detailhtml):
            c.append([i for i in a.span()])
        for i in c:
            tEndIndex.append([i[1], 0])
        for i in reversed(tPreIndex):
            for j in range(len(tEndIndex)):
                if i < tEndIndex[j][0] and tEndIndex[j][1] == 0:
                    tStr.append([i, tEndIndex[j][0]])
                    tEndIndex[j][1] = 1
                    break
        # 去除表格内表格
        # for index1 in tStr:
        #     for index2 in tStr:
        #         if index1[0] > index2[0] and index1[1] < index2[1]:
        #             tStr.remove(index1)
        return tStr

    def getMarkdown(self, detailhtml=''):
        #转md忽略表格
        self.text_maker.bypass_tables = True
        t = self.text_maker.handle(detailhtml)
        t = re.sub('(\n)\\1+', "\n\n", t)
        t = re.sub('>+\n$','\n',t)
        #将多余的*删掉
        t = re.sub('(\*)\\1+', "**", t)
        #清除每行开头的空格
        t = '\n'.join([re.sub("^\\s+", "", line) for line in t.split("\n")])
        x = []
        for line in t.split("\n"):
            if len(re.findall("\*+",line)) % 2 != 0:
                x.append(line.replace("*",""))
                continue
            star_labels = re.findall("\*\*(.*?)\*\*",line)
            for label in star_labels:
                line = line.replace(label,re.sub("^\s+|\s+$",'',label))
                line = re.sub("\s+\*+\s+|^\*+\s+|\s+\*+$|^\*+$","",line)
            x.append(line)
        t = '\n'.join(x)
        links = re.findall("\]\((.*?)\)", t)
        # 集合去重
        links = set(links)
        if '' in  links:
            links.remove('')
        for link in links:
            t = t.replace(link, parse.urljoin(self.website,link))

        #获得tablehtml的范围

        tStr = self.searchTable(detailhtml, '<table', '</table>')

        tMdStr = self.searchTable(t, '<table', '</table>')
        for i in range(len(tMdStr)):
            t = t.replace(t[tMdStr[i][0]:tMdStr[i][1]],detailhtml[tStr[i][0]:tStr[i][1]])
        t.encode('utf-8')
        return t

    def set_main_domain(self,url):
        self.website = url


# -*- coding: gbk -*-
import csv
import requests
import re
from lxml import etree
from time import sleep
from selenium import webdriver
from config import model_one


class spider(object):
    def __init__(self):
        self.url = 'https://www.diyifanwen.com/tool/mingrenmingyan/'
        self.index = requests.get(self.url)
        self.hot_urls = {}  # url汇总
        self.urls_classify = {}
        self.urls = {}
        self.author = ''
        self.classify = ''
        self.text = []
        self.ret_dict = {'类别': '', '作者': '', '名言': '', '出处': ''}
        path = r'D:\web_driver\chromedriver.exe'
        self.author_rule = None
        self.driver = webdriver.Chrome(path)
        self.data = []

    def get_url_classify(self):
        """获取分类的url"""
        html = etree.HTML(self.index.content)
        urls = html.xpath('//*[@id="tab_box2"]/ul//li//a/@href')
        classify = html.xpath('//*[@id="tab_box2"]/ul//li//a//text()')
        classify_url = {x: y for x, y in zip(classify, urls)}
        print(classify_url)
        self.urls_classify.update(classify_url)

    def get_hot_url(self):
        """获取热门名人名言url"""
        # self.driver.get(self.url)
        # html = etree.HTML(self.driver.page_source)
        # url = html.xpath('//*[@id="IndexContent"]//div//ul//li/a/@href')
        # author = html.xpath('//*[@id="IndexContent"]//div//ul//li/a//text()')
        # _dict = {f"中国古代名人名言-{x}": y for x, y in zip(author, url)}
        # # print(_dict)
        html = etree.HTML(self.index.content)
        urls = html.xpath('//*[@id="tab_box1"]/ul//li//a/@href')
        classify = html.xpath('//*[@id="tab_box1"]/ul//li//a//text()')
        classify_url = {x: y for x, y in zip(classify, urls)}
        print(classify_url)
        self.hot_urls.update(classify_url)

    def get_url(self):
        """获取精选中的url"""
        html = etree.HTML(self.index.content)
        urls = html.xpath('//*[@id="ListLeft"]//dl//dd//a/@href')
        classify = html.xpath('//*[@id="ListLeft"]//dl//dd//a//text()')
        url = {x: y for x, y in zip(classify, urls)}
        print(url)
        self.urls.update(url)

    def get_data(self, _dict):
        """抓取推荐分类名言数据"""
        # 获取页面源码
        ret = [_dict]
        self.driver.get(r'https:' + self.urls_classify[_dict])
        page = self.driver.page_source
        # print(page)
        html = etree.HTML(page)
        # 标签p的内容
        for i in range(1, 2000):
            temp_data = html.xpath(f'//*[@id="ArtContent"]/p[{i}]//text()')
            temp_data = ''.join(temp_data).replace(' ', '')
            ret.append(temp_data)
        ret = [x for x in ret if x]
        print(ret)
        return ret

    def get_other_data(self, _dict):
        """抓取其它名言数据"""
        # 获取页面源码
        ret = [_dict]
        if _dict in model_one or _dict in self.hot_urls or _dict in ['TT教你学国外名言', '国外名言原来这么简单', '无敌英语名人名言', '功夫熊猫10句电影名人名言']:
            self.driver.get(r'https:' + self.urls[_dict])
            page = self.driver.page_source
            y = 1
        else:
            # page = requests.get(r'https:' + self.urls[_dict]).content
            self.driver.get(r'https:' + self.urls[_dict])
            page = self.driver.page_source
            y = 2
        html = etree.HTML(page)
        if _dict in ['中国谚语', '英国谚语']:
            # 文本存储路径不同
            for j in range(1, 50):
                temp_data = html.xpath(f'//*[@id="ArtContent"]/ol/li[{j}]//text()')
                temp_data = ''.join(temp_data).replace(' ', '')
                ret.append(temp_data)
            ret = [x for x in ret if x]
            print(ret)
            sleep(0.5)
            return ret
        for i in range(y, 200):
            if _dict in ['TT教你学国外名言', '国外名言原来这么简单', '无敌英语名人名言', '功夫熊猫10句电影名人名言']:
                temp_data = html.xpath(f'//*[@id="ArtContent"]/p[{i}]//text()')
                temp_data = ''.join(temp_data)
                ret.append(temp_data)
            else:
                temp_data = html.xpath(f'//*[@id="ArtContent"]/p[{i}]//text()')
                temp_data = ''.join(temp_data).replace(' ', '')
                ret.append(temp_data)
        ret = [x for x in ret if x]
        print(ret)
        sleep(0.5)
        return ret

    def data_format(self, temp_data):
        """数据格式化"""
        if not temp_data:
            return
        ret = []
        # if temp_data[0] in '国外名人名言汇总的名言':
        #     temp_data = self.get_text(temp_data)
        # 正则表达式取出符合条件的文本
        if temp_data[0] in ['名人名言_学习', 'TT教你学国外名言', '国外名言原来这么简单', '无敌英语名人名言', '功夫熊猫10句电影名人名言']:
            for term in temp_data:
                if temp_data.index(term) % 2 == 1 and term != temp_data[-1]:
                    if '.' in term:
                        temp_data[temp_data.index(term)] = term + ''.join(temp_data[temp_data.index(term) + 1])
                    else:
                        temp_data[temp_data.index(term)] = term + temp_data[temp_data.index(term) + 1]
                if '读书名言' in term:
                    temp_data.remove(term)
            for i in range(len(temp_data) - 1, 0, -2):
                temp_data.pop(i)
            print(temp_data)
        if temp_data[0] in model_one:
            temp_data = self.get_text(temp_data)
        for term in temp_data:
            if temp_data.index(term) == 0:
                continue
            # 筛选出作者
            self.author = ''.join(re.findall(self.author_rule, term))
            print(self.author)
            if '作者:' in self.author:
                author_re = self.author.split('作者:')[-1]
                self.ret_dict['作者'] = author_re
            elif '——' in self.author:
                if "——这份爱如此美好" in self.author or "——在你周围最黑暗的时刻显得最亮" in self.author:
                    continue
                author_re = self.author.split('——')[-1]
                self.author = author_re
                self.ret_dict['作者'] = author_re
            # 筛选出类别
            if temp_data[0] in self.urls_classify:
                classify = temp_data[0]
                self.ret_dict['类别'] = classify
            else:
                self.classify = ''.join(re.findall('类别:[\u4e00-\u9fa5a-zA-Z]+', term))
                classify_re = self.classify.split('类别:')[-1]
                self.ret_dict['类别'] = classify_re
            # 筛选出正文
            if temp_data[0] in ['TT教你学国外名言', '国外名言原来这么简单', '无敌英语名人名言', '功夫熊猫10句电影名人名言']:
                list_ = term.split('.')
                text1 = ' '.join(re.findall('[a-zA-Z]+[。，；·:.]|[a-zA-Z]+', list_[0])).replace(self.author, '').replace(self.classify, '') + '.'
                text2 = ''.join(re.findall(
                '\[[\u4e00-\u9fa5]+]|[\u4e00-\u9fa5a-zA-Z]+[。，；,·:.]|[\u4e00-\u9fa5a-zA-Z]+',
                term)).replace(self.author, '').replace(self.classify, '')
                text = text1 + text2
            else:
                text = ''.join(re.findall(
                    '[\u4e00-\u9fa5a-zA-Z]+[。，；·:.]|《[\u4e00-\u9fa5a-zA-Z]+》|作者:[\u4e00-\u9fa5a-zA-Z]+|（[\u4e00-\u9fa5a-zA-Z]+）|[\u4e00-\u9fa5a-zA-Z]+',
                    term)).replace(self.author, '').replace(self.classify, '')
            if '作者' in text:
                text = text.replace(f'作者：{self.ret_dict["作者"]}', '')
            self.ret_dict['名言'] = text
            self.ret_dict['出处'] = temp_data[0]
            ret.append(self.ret_dict)
            print(self.ret_dict)
            # 重置元素
            self.ret_dict = {'类别': '', '作者': '', '名言': '', '出处': ''}
            self.author = ''
            self.classify = ''
        return ret

    def get_author(self, ):
        self.author_rule = '——《[\u4e00-\u9fa5a-zA-Z]+·[\u4e00-\u9fa5a-zA-Z]+·[\u4e00-\u9fa5a-zA-Z]+》|' \
                           '——\S+?[\u4e00-\u9fa5]+|' \
                           '——塞约翰逊，英国作家|' \
                           '——（[\u4e00-\u9fa5a-zA-Z]+）[\u4e00-\u9fa5a-zA-Z]+|' \
                           '——《[\u4e00-\u9fa5a-zA-Z]+》|' \
                           '——[\u4e00-\u9fa5a-zA-Z]+·[\u4e00-\u9fa5a-zA-Z]+·[\u4e00-\u9fa5a-zA-Z]+|' \
                           '——[\u4e00-\u9fa5a-zA-Z]+·[\u4e00-\u9fa5a-zA-Z]+|' \
                           '——《[\u4e00-\u9fa5a-zA-Z]+·[\u4e00-\u9fa5a-zA-Z]+·[\u4e00-\u9fa5a-zA-Z]+》|' \
                           '——（[\u4e00-\u9fa5a-zA-Z]+）[\u4e00-\u9fa5a-zA-Z]+|' \
                           '——《[\u4e00-\u9fa5a-zA-Z]+》|' \
                           '——[\u4e00-\u9fa5a-zA-Z]+·[\u4e00-\u9fa5a-zA-Z]+·[\u4e00-\u9fa5a-zA-Z]+|' \
                           '——[\u4e00-\u9fa5a-zA-Z]+·[\u4e00-\u9fa5a-zA-Z]+|' \
                           '——[\u4e00-\u9fa5a-zA-Z]+|' \
                           '——[a-zA-Z].[a-zA-Z].|' \
                           '作者:[\u4e00-\u9fa5a-zA-Z]+·[\u4e00-\u9fa5a-zA-Z]+|' \
                           '作者:《[\u4e00-\u9fa5a-zA-Z]+》|' \
                           '作者:（[\u4e00-\u9fa5a-zA-Z]+）[\u4e00-\u9fa5a-zA-Z]+|' \
                           '作者:[\u4e00-\u9fa5a-zA-Z]+'

    def get_text(self, list_):
        ret_list = [list_[0]]
        for term in list_:
            if term == list_[0]:
                continue
            # \S+?。[\u4e00-\u9fa5a-zA-Z]+
            text = re.findall('\d+\D+|\S+?类别:[\u4e00-\u9fa5]{2}|\S+?[）]|\S+?》|\S+?●|\S+?[?]|名言：\S+名言|名言\S+。|\D+', term)
            print(text)
            for x in text:
                ret_list.append(x)
        return ret_list

    def write_in_file(self):
        # persons = [('Tom', 20, 180), ('Allen', 21, 182), ('Jerry', 22, 181)]
        for term in self.data:
            for iterm in term:
                if '名言' in iterm['名言'] or '推荐' in iterm['名言']:
                    term.remove(iterm)
        headers = ('名言', '作者', '类别', '出处')
        with open(r'C:\Users\86131\Desktop\名人名言.csv', 'w', encoding='utf-8', newline='') as f:
            write = csv.writer(f)  # 创建writer对象
            write.writerow(headers)
            # 写内容，writerrow 一次只写入一行
            for data_list in self.data:
                for data_dict in data_list:
                    write.writerow((data_dict['名言'], data_dict['作者'], data_dict['类别'], data_dict['出处']))

    def main(self):
        self.get_author()
        # 获取热门名人超链接
        self.get_hot_url()
        # 获取分类名言超链接
        self.get_url_classify()
        # 获取各种精选名言
        self.get_url()
        # # 抓取超链接中的数据并处理
        # for term in self.hot_urls:
        #     temp_data = self.get_other_data(term)
        #     self.data.append(self.data_format(temp_data))
        # for x in self.urls_classify:
        #     temp_data = self.get_data(x)
        #     self.data.append(self.data_format(temp_data))
        for iterm in self.urls:
            temp_data = self.get_other_data(iterm)
            self.data.append(self.data_format(temp_data))
        print(y for y in self.data)
        self.driver.close()
        self.write_in_file()


if __name__ == "__main__":
    spider().main()

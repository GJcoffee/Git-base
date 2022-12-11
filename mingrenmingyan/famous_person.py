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
        self.hot_urls = {}  # url����
        self.urls_classify = {}
        self.urls = {}
        self.author = ''
        self.classify = ''
        self.text = []
        self.ret_dict = {'���': '', '����': '', '����': '', '����': ''}
        path = r'D:\web_driver\chromedriver.exe'
        self.author_rule = None
        self.driver = webdriver.Chrome(path)
        self.data = []

    def get_url_classify(self):
        """��ȡ�����url"""
        html = etree.HTML(self.index.content)
        urls = html.xpath('//*[@id="tab_box2"]/ul//li//a/@href')
        classify = html.xpath('//*[@id="tab_box2"]/ul//li//a//text()')
        classify_url = {x: y for x, y in zip(classify, urls)}
        print(classify_url)
        self.urls_classify.update(classify_url)

    def get_hot_url(self):
        """��ȡ������������url"""
        # self.driver.get(self.url)
        # html = etree.HTML(self.driver.page_source)
        # url = html.xpath('//*[@id="IndexContent"]//div//ul//li/a/@href')
        # author = html.xpath('//*[@id="IndexContent"]//div//ul//li/a//text()')
        # _dict = {f"�й��Ŵ���������-{x}": y for x, y in zip(author, url)}
        # # print(_dict)
        html = etree.HTML(self.index.content)
        urls = html.xpath('//*[@id="tab_box1"]/ul//li//a/@href')
        classify = html.xpath('//*[@id="tab_box1"]/ul//li//a//text()')
        classify_url = {x: y for x, y in zip(classify, urls)}
        print(classify_url)
        self.hot_urls.update(classify_url)

    def get_url(self):
        """��ȡ��ѡ�е�url"""
        html = etree.HTML(self.index.content)
        urls = html.xpath('//*[@id="ListLeft"]//dl//dd//a/@href')
        classify = html.xpath('//*[@id="ListLeft"]//dl//dd//a//text()')
        url = {x: y for x, y in zip(classify, urls)}
        print(url)
        self.urls.update(url)

    def get_data(self, _dict):
        """ץȡ�Ƽ�������������"""
        # ��ȡҳ��Դ��
        ret = [_dict]
        self.driver.get(r'https:' + self.urls_classify[_dict])
        page = self.driver.page_source
        # print(page)
        html = etree.HTML(page)
        # ��ǩp������
        for i in range(1, 2000):
            temp_data = html.xpath(f'//*[@id="ArtContent"]/p[{i}]//text()')
            temp_data = ''.join(temp_data).replace(' ', '')
            ret.append(temp_data)
        ret = [x for x in ret if x]
        print(ret)
        return ret

    def get_other_data(self, _dict):
        """ץȡ������������"""
        # ��ȡҳ��Դ��
        ret = [_dict]
        if _dict in model_one or _dict in self.hot_urls or _dict in ['TT����ѧ��������', '��������ԭ����ô��', '�޵�Ӣ����������', '������è10���Ӱ��������']:
            self.driver.get(r'https:' + self.urls[_dict])
            page = self.driver.page_source
            y = 1
        else:
            # page = requests.get(r'https:' + self.urls[_dict]).content
            self.driver.get(r'https:' + self.urls[_dict])
            page = self.driver.page_source
            y = 2
        html = etree.HTML(page)
        if _dict in ['�й�����', 'Ӣ������']:
            # �ı��洢·����ͬ
            for j in range(1, 50):
                temp_data = html.xpath(f'//*[@id="ArtContent"]/ol/li[{j}]//text()')
                temp_data = ''.join(temp_data).replace(' ', '')
                ret.append(temp_data)
            ret = [x for x in ret if x]
            print(ret)
            sleep(0.5)
            return ret
        for i in range(y, 200):
            if _dict in ['TT����ѧ��������', '��������ԭ����ô��', '�޵�Ӣ����������', '������è10���Ӱ��������']:
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
        """���ݸ�ʽ��"""
        if not temp_data:
            return
        ret = []
        # if temp_data[0] in '�����������Ի��ܵ�����':
        #     temp_data = self.get_text(temp_data)
        # ������ʽȡ�������������ı�
        if temp_data[0] in ['��������_ѧϰ', 'TT����ѧ��������', '��������ԭ����ô��', '�޵�Ӣ����������', '������è10���Ӱ��������']:
            for term in temp_data:
                if temp_data.index(term) % 2 == 1 and term != temp_data[-1]:
                    if '.' in term:
                        temp_data[temp_data.index(term)] = term + ''.join(temp_data[temp_data.index(term) + 1])
                    else:
                        temp_data[temp_data.index(term)] = term + temp_data[temp_data.index(term) + 1]
                if '��������' in term:
                    temp_data.remove(term)
            for i in range(len(temp_data) - 1, 0, -2):
                temp_data.pop(i)
            print(temp_data)
        if temp_data[0] in model_one:
            temp_data = self.get_text(temp_data)
        for term in temp_data:
            if temp_data.index(term) == 0:
                continue
            # ɸѡ������
            self.author = ''.join(re.findall(self.author_rule, term))
            print(self.author)
            if '����:' in self.author:
                author_re = self.author.split('����:')[-1]
                self.ret_dict['����'] = author_re
            elif '����' in self.author:
                if "������ݰ��������" in self.author or "����������Χ��ڰ���ʱ���Ե�����" in self.author:
                    continue
                author_re = self.author.split('����')[-1]
                self.author = author_re
                self.ret_dict['����'] = author_re
            # ɸѡ�����
            if temp_data[0] in self.urls_classify:
                classify = temp_data[0]
                self.ret_dict['���'] = classify
            else:
                self.classify = ''.join(re.findall('���:[\u4e00-\u9fa5a-zA-Z]+', term))
                classify_re = self.classify.split('���:')[-1]
                self.ret_dict['���'] = classify_re
            # ɸѡ������
            if temp_data[0] in ['TT����ѧ��������', '��������ԭ����ô��', '�޵�Ӣ����������', '������è10���Ӱ��������']:
                list_ = term.split('.')
                text1 = ' '.join(re.findall('[a-zA-Z]+[��������:.]|[a-zA-Z]+', list_[0])).replace(self.author, '').replace(self.classify, '') + '.'
                text2 = ''.join(re.findall(
                '\[[\u4e00-\u9fa5]+]|[\u4e00-\u9fa5a-zA-Z]+[������,��:.]|[\u4e00-\u9fa5a-zA-Z]+',
                term)).replace(self.author, '').replace(self.classify, '')
                text = text1 + text2
            else:
                text = ''.join(re.findall(
                    '[\u4e00-\u9fa5a-zA-Z]+[��������:.]|��[\u4e00-\u9fa5a-zA-Z]+��|����:[\u4e00-\u9fa5a-zA-Z]+|��[\u4e00-\u9fa5a-zA-Z]+��|[\u4e00-\u9fa5a-zA-Z]+',
                    term)).replace(self.author, '').replace(self.classify, '')
            if '����' in text:
                text = text.replace(f'���ߣ�{self.ret_dict["����"]}', '')
            self.ret_dict['����'] = text
            self.ret_dict['����'] = temp_data[0]
            ret.append(self.ret_dict)
            print(self.ret_dict)
            # ����Ԫ��
            self.ret_dict = {'���': '', '����': '', '����': '', '����': ''}
            self.author = ''
            self.classify = ''
        return ret

    def get_author(self, ):
        self.author_rule = '������[\u4e00-\u9fa5a-zA-Z]+��[\u4e00-\u9fa5a-zA-Z]+��[\u4e00-\u9fa5a-zA-Z]+��|' \
                           '����\S+?[\u4e00-\u9fa5]+|' \
                           '������Լ��ѷ��Ӣ������|' \
                           '������[\u4e00-\u9fa5a-zA-Z]+��[\u4e00-\u9fa5a-zA-Z]+|' \
                           '������[\u4e00-\u9fa5a-zA-Z]+��|' \
                           '����[\u4e00-\u9fa5a-zA-Z]+��[\u4e00-\u9fa5a-zA-Z]+��[\u4e00-\u9fa5a-zA-Z]+|' \
                           '����[\u4e00-\u9fa5a-zA-Z]+��[\u4e00-\u9fa5a-zA-Z]+|' \
                           '������[\u4e00-\u9fa5a-zA-Z]+��[\u4e00-\u9fa5a-zA-Z]+��[\u4e00-\u9fa5a-zA-Z]+��|' \
                           '������[\u4e00-\u9fa5a-zA-Z]+��[\u4e00-\u9fa5a-zA-Z]+|' \
                           '������[\u4e00-\u9fa5a-zA-Z]+��|' \
                           '����[\u4e00-\u9fa5a-zA-Z]+��[\u4e00-\u9fa5a-zA-Z]+��[\u4e00-\u9fa5a-zA-Z]+|' \
                           '����[\u4e00-\u9fa5a-zA-Z]+��[\u4e00-\u9fa5a-zA-Z]+|' \
                           '����[\u4e00-\u9fa5a-zA-Z]+|' \
                           '����[a-zA-Z].[a-zA-Z].|' \
                           '����:[\u4e00-\u9fa5a-zA-Z]+��[\u4e00-\u9fa5a-zA-Z]+|' \
                           '����:��[\u4e00-\u9fa5a-zA-Z]+��|' \
                           '����:��[\u4e00-\u9fa5a-zA-Z]+��[\u4e00-\u9fa5a-zA-Z]+|' \
                           '����:[\u4e00-\u9fa5a-zA-Z]+'

    def get_text(self, list_):
        ret_list = [list_[0]]
        for term in list_:
            if term == list_[0]:
                continue
            # \S+?��[\u4e00-\u9fa5a-zA-Z]+
            text = re.findall('\d+\D+|\S+?���:[\u4e00-\u9fa5]{2}|\S+?[��]|\S+?��|\S+?��|\S+?[?]|���ԣ�\S+����|����\S+��|\D+', term)
            print(text)
            for x in text:
                ret_list.append(x)
        return ret_list

    def write_in_file(self):
        # persons = [('Tom', 20, 180), ('Allen', 21, 182), ('Jerry', 22, 181)]
        for term in self.data:
            for iterm in term:
                if '����' in iterm['����'] or '�Ƽ�' in iterm['����']:
                    term.remove(iterm)
        headers = ('����', '����', '���', '����')
        with open(r'C:\Users\86131\Desktop\��������.csv', 'w', encoding='utf-8', newline='') as f:
            write = csv.writer(f)  # ����writer����
            write.writerow(headers)
            # д���ݣ�writerrow һ��ֻд��һ��
            for data_list in self.data:
                for data_dict in data_list:
                    write.writerow((data_dict['����'], data_dict['����'], data_dict['���'], data_dict['����']))

    def main(self):
        self.get_author()
        # ��ȡ�������˳�����
        self.get_hot_url()
        # ��ȡ�������Գ�����
        self.get_url_classify()
        # ��ȡ���־�ѡ����
        self.get_url()
        # # ץȡ�������е����ݲ�����
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

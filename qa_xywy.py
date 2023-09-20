# -*- coding: utf-8 -*-            
# @Author : hujingsong
# @Time : 2021/12/15 8:43
# @software : PyCharm

import urllib.request
import urllib.parse
from lxml import etree
from tqdm import tqdm
import pymongo
import re
import json
import time
import sys

class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a",encoding="utf-8")
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
    def flush(self):
        pass
sys.stdout = Logger('worklog.txt')

'''
已解决问题：https://club.xywy.com/list_answer_1.htm  1-1000
全部问题：https://club.xywy.com/list_all_1.htm   1-1000
悬赏问题：https://club.xywy.com/list_score_1.htm  1-1000
热门问题：https://club.xywy.com/list_hot_1.htm  1-1000
'''

class CrimeSpider:
    def __init__(self):
        try:
            self.conn = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
            self.db = self.conn['medical']
            self.col = self.db['qa_data_xywy']
            print(self.db)
            print(self.col)
            print('['+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+']:连接数据库成功')
            # self.db.authenticate("root4","123456")
        except Exception as e:
            print('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ']:连接数据库失败')
            print(e)

    def get_html(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/51.0.2704.63 Safari/537.36'}
        req = urllib.request.Request(url=url, headers=headers)
        res = urllib.request.urlopen(req)
        html = res.read().decode('gbk','ignore')
        return html

    def get_url_list(self):
        print('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ']:开始获取所有问题的url')
        data_url_list = []
        init_url = ['https://club.xywy.com/list_answer_%s.htm','https://club.xywy.com/list_all_%s.htm',
                    'https://club.xywy.com/list_score_%s.htm','https://club.xywy.com/list_hot_%s.htm']
        for url in init_url:
            for page in tqdm(range(1,1001)):
                    basic_url = url%page
                    # 拼接url
                    domain_url = 'https://club.xywy.com'
                    try:
                        question_url = self.question_url_spider(basic_url)
                        # print(question_url)
                        if len(question_url) != 0:
                            for _url in question_url:
                                data_url = domain_url + _url
                                # print(data_url)
                                data_url_list.append(data_url)
                    except Exception as e:
                        print('[' + time.strftime('%Y-%m-%d %H:%M:%S',
                                                  time.localtime(time.time())) + ']:%s问题的url获取失败'%(basic_url))
                        print('失败的url：',basic_url)
                        print(e)
        print('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ']:'+'所有的url:',len(data_url_list))
        print('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ']:所有问题的url获取成功')
        print('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ']:'+'去重后的url:',len(set(data_url_list)))
        return data_url_list

    def spider_main(self):
        url_list = self.get_url_list()
        i = 0
        for url in tqdm(set(url_list)):
            try:
                i += 1
                qa_data = {}
                try:
                    qa_data['question_url'] = url
                    qa_data['qa_data'] = self.qa_data_spider(url)
                    q = self.qa_data_spider(url)
                    # print(q)
                except Exception as e:
                    print(e)
                try:
                    self.col.insert_one(qa_data)
                    qa_data.pop('_id')
                    qa_data['id'] = i
                    with open('qa_data.json', 'a+', encoding='UTF-8') as fp:
                        fp.write(json.dumps(qa_data, indent=2, ensure_ascii=False))
                        fp.write('\n')
                    print('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ']:%s数据保存成功。' % str(i))
                except Exception as e:
                    print('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ']:%s数据保存失败。' % str(i))
                    print(e)

            except Exception as e:
                print(e)

        return

    def question_url_spider(self,url):
        html = self.get_html(url)
        selector = etree.HTML(html)
        question_url = selector.xpath('//div[@class="fl"]/a/@href')
        # print(question_url)
        return question_url

    def qa_data_spider(self,url):
        html = self.get_html(url)
        selector = etree.HTML(html)
        data = {}
        question_data = selector.xpath('//div[@class="clearfix"]/h3/text()')
        question_leibie = selector.xpath('//div[@class="clearfix content menu-Breadcrumb"]/a/text()')
        answer = selector.xpath('//div[@class="replay-item-box clearfix borb js-replay-item"]/div[2]')
        infobox = []
        for p in answer:
            info = p.xpath('string(.)').replace('\r','').replace('\n','').replace('\xa0', '').replace('   ', '').replace('\t','')
            infobox.append(info)
        # print(infobox)
        data['question_leibie'] = question_leibie
        data['question_name'] = question_data
        data['answer'] = infobox
        # print(data)

        return data




if __name__ == '__main__':
    q = CrimeSpider()
    #q.get_url_list()
    q.spider_main()





# -*- coding: utf-8 -*-
# @Author : hujingsong
# @Time : 2021/12/13 15:05
# @software : PyCharm

import urllib.request
import urllib.parse
from lxml import etree
# import pymongo
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



class CrimeSpider:
    def __init__(self):
        pass
        # try:
        #     self.conn = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
        #     self.db = self.conn['medical']
        #     self.col = self.db['disease_data']
        #     print(self.db)
        #     print(self.col)
        #     print('['+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+']:连接数据库成功')
        #     # self.db.authenticate("root4","123456")
        # except Exception as e:
        #     print('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ']:连接数据库成功')
        #     print(e)

    def get_html(self, url):
        url='http://jib.xywy.com/il_sii_1.htm'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/51.0.2704.63 Safari/537.36'}
        req = urllib.request.Request(url=url, headers=headers)
        res = urllib.request.urlopen(req)
        html = res.read().decode('gbk')
        return html



    def spider_main(self):

        for page in range(1, 3):
        #for page in range(1, 10):
            try:
                #//div[@class="jib-kownlege clearfix mt20"]/div[@class="fl jib-common-sense"]/p[@class="clearfix"]/span/text()
                basic_url = 'http://jib.xywy.com/il_sii/gaishu/%s.htm'%page
                cause_url = 'http://jib.xywy.com/il_sii/cause/%s.htm'%page
                prevent_url = 'http://jib.xywy.com/il_sii/prevent/%s.htm'%page
                symptom_url = 'http://jib.xywy.com/il_sii/symptom/%s.htm'%page
                inspect_url = 'http://jib.xywy.com/il_sii/inspect/%s.htm'%page
                treat_url = 'http://jib.xywy.com/il_sii/treat/%s.htm'%page
                food_url = 'http://jib.xywy.com/il_sii/food/%s.htm'%page
                drug_url = 'http://jib.xywy.com/il_sii/drug/%s.htm'%page
                data = {}
                data['url'] = basic_url
                try:
                    data['basic_info'] = self.basicinfo_spider(basic_url)
                    print('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ']:疾病基本信息爬取成功')
                except Exception as e:
                    print('[' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ']:疾病基本信息爬取失败')
                    print('失败url：%s'%basic_url)
                    print('失败原因：%s'%e)

                try:
                    data['cause_info'] =  self.common_spider(cause_url)
                    print('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ']:疾病病因爬取成功')
                except Exception as e:
                    print('[' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ']:疾病病因爬取失败')
                    print('失败url：%s'%cause_url)
                    print('失败原因：%s'%e)

                try:
                    data['prevent_info'] =  self.common_spider(prevent_url)
                    print('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ']:疾病预防信息爬取成功')
                except Exception as e:
                    print('[' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ']:疾病预防信息爬取失败')
                    print('失败url：%s'%prevent_url)
                    print('失败原因：%s'%e)
                try:
                    data['symptom_info'] = self.symptom_spider(symptom_url)
                    print('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ']:疾病症状信息爬取成功')
                except Exception as e:
                    print('[' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ']:疾病症状信息爬取失败')
                    print('失败url：%s'%symptom_url)
                    print('失败原因：%s'%e)

                try:
                    data['inspect_info'] = self.inspect_spider(inspect_url)
                    print('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ']:疾病检查信息爬取成功')
                except Exception as e:
                    print('[' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ']:疾病检查信息爬取失败')
                    print('失败url：%s'%inspect_url)
                    print('失败原因：%s'%e)

                try:
                    data['treat_info'] = self.treat_spider(treat_url)
                    print('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ']:疾病治疗信息爬取成功')
                except Exception as e:
                    print('[' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ']:疾病治疗信息爬取失败')
                    print('失败url：%s'%treat_url)
                    print('失败原因：%s'%e)

                try:
                    data['food_info'] = self.food_spider(food_url)
                    print('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ']:食物信息爬取成功')
                except Exception as e:
                    print('[' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ']:食物信息爬取失败')
                    print('失败url：%s'%food_url)
                    print('失败原因：%s'%e)

                try:
                    data['drug_info'] = self.drug_spider(drug_url)
                    print('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ']:药物信息爬取成功')
                except Exception as e:
                    print('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ']:药物信息爬取失败')
                    print('失败url：%s' %drug_url)
                    print('失败原因：%s' %e)

                print(page, basic_url)
                try:
                    # self.col.insert_one(data)
                    # data.pop('_id')
                    data['id'] = page
                    with open('data2.json', 'a+', encoding='UTF-8') as fp:
                        fp.write(json.dumps(data, indent=2, ensure_ascii=False))
                        fp.write('\n')
                    print('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ']:%s数据保存成功。'%str(page))
                except Exception as e:
                    print('[' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ']:%s数据保存失败。'%str(page))
                    print(e)
            except Exception as e:
                print(e, page)
        return


    def basicinfo_spider(self, url):
        # url='http://jib.xywy.com/il_sii_1.htm'
        html = self.get_html(url)
        selector = etree.HTML(html)
        title = selector.xpath('//title/text()')[0]
        #//div[@class="jib-kownlege clearfix mt20"]/div[@class="fl jib-common-sense"]/p[@class="clearfix"]/span/text()
        category = selector.xpath('//div[@class="wrap mt10 nav-bar"]/a/text()')
        desc = selector.xpath('//div[@class="jib-articl-con jib-lh-articl"]/p/text()')
        ps = selector.xpath('//div[@class="mt20 articl-know"]/p')
        infobox = []
        for p in ps:
            info = p.xpath('string(.)').replace('\r','').replace('\n','').replace('\xa0', '').replace('   ', '').replace('\t','')
            infobox.append(info)
        basic_data = {}
        basic_data['category'] = category
        basic_data['name'] = title.split('的简介')[0]
        basic_data['desc'] = desc
        basic_data['attributes'] = infobox
        return basic_data


    def treat_spider(self, url):
        html = self.get_html(url)
        selector = etree.HTML(html)
        ps = selector.xpath('//div[starts-with(@class,"mt20 articl-know")]/p')
        infobox = []
        for p in ps:
            info = p.xpath('string(.)').replace('\r','').replace('\n','').replace('\xa0', '').replace('   ', '').replace('\t','')
            infobox.append(info)
        return infobox


    def drug_spider(self, url):
        html = self.get_html(url)
        selector = etree.HTML(html)
        drugs = [i.replace('\n','').replace('\t', '').replace(' ','') for i in selector.xpath('//div[@class="fl drug-pic-rec mr30"]/p/a/text()')]
        return drugs


    def food_spider(self, url):
        html = self.get_html(url)
        selector = etree.HTML(html)
        divs = selector.xpath('//div[@class="diet-img clearfix mt20"]')
        try:
            food_data = {}
            food_data['good'] = divs[0].xpath('./div/p/text()')
            food_data['bad'] = divs[1].xpath('./div/p/text()')
            food_data['recommand'] = divs[2].xpath('./div/p/text()')
        except:
            return {}

        return food_data


    def symptom_spider(self, url):
        html = self.get_html(url)
        selector = etree.HTML(html)
        symptoms = selector.xpath('//span[@class="db f12 lh240 mb15 "]/a/text()')
        ps = selector.xpath('//p')
        detail = []
        for p in ps:
            info = p.xpath('string(.)').replace('\r','').replace('\n','').replace('\xa0', '').replace('   ', '').replace('\t','')
            detail.append(info)
        symptoms_data = {}
        symptoms_data['symptoms'] = symptoms
        symptoms_data['symptoms_detail'] = detail
        return symptoms, detail


    def inspect_spider(self, url):
        html = self.get_html(url)
        selector = etree.HTML(html)
        inspects  = selector.xpath('//li[@class="check-item"]/a/@href')
        return inspects


    def common_spider(self, url):
        html = self.get_html(url)
        selector = etree.HTML(html)
        ps = selector.xpath('//p')
        infobox = []
        for p in ps:
            info = p.xpath('string(.)').replace('\r', '').replace('\n', '').replace('\xa0', '').replace('   ','').replace('\t', '')
            if info:
                infobox.append(info)
        return '\n'.join(infobox)



    def inspect_crawl(self):
        for page in range(1, 3685):
        #for page in range(1, 10):
            try:
                url = 'http://jck.xywy.com/jc_%s.html'%page
                html = self.get_html(url)
                selector = etree.HTML(html)
                jc_name = selector.xpath('//div[@class="clearfix"]/strong/text()')
                ps = selector.xpath('//p')
                infobox = []
                for p in ps:
                    info = p.xpath('string(.)').replace('\r', '').replace('\n', '').replace('\xa0', '').replace('   ','').replace('\t', '')
                    if info:
                        infobox.append(info)
                        # print(info)
                data = {}
                data['jc_url']= url
                data['jc_name'] = jc_name
                data['jc_info'] = infobox
                # print(data)
                self.db['jc'].insert_one(data)
                data.pop('_id')
                with open('data.json', 'a+', encoding='UTF-8') as fp:
                    fp.write(json.dumps(data, indent=2, ensure_ascii=False))
                    fp.write('\n')
                print('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ']:%s检查数据保存成功。' % str(page))

            except Exception as e:
                print('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ']:%s检查数据下载失败。' % str(page))

                print(e)

if __name__ == '__main__':
    handler = CrimeSpider()
    # handler.spider_main()
    #handler.inspect_crawl()
    url='http://jib.xywy.com/il_sii_1.htm'
    d=handler.basicinfo_spider(url)
    print(d)
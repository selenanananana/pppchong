### 1.爬虫的目的
爬取医药网站的数据，丰富我们的知识图谱。
### 2.爬虫程序的实现过程
#### 技术：

    1）HTTP 库：如 Requests、urllib 等，能够模拟浏览器发送 HTTP 请求，获取页面内容。
    2）解析库：lxml ，能够解析 HTML 或 XML 格式的页面内容，提取需要的信息。
    3）XPath：了解 XPath 的语法和使用方法，能够进行页面元素的定位和抽取。
    4）正则表达式：能够使用正则表达式进行文本匹配和抽取，对于抓取数据非常有帮助。
    5）数据库：了解关系型数据库  MySQL 和 NoSQL 数据库 MongoDB 等数据存储方式，能够进行数据存储和管理。
    6）编程语言：能够熟练使用至少一种编程语言，如 Python、Java、Ruby、JavaScript 等，进行数据抓取和处理。
#### 工具

    python,urllib.request,lxml,MongoDB,MySQL
#### 爬取的网站
    https://jib.xywy.com/il_sii/gaishu/124.htm    寻医问药网

![img.png](imgs/img.png)

![img_1.png](imgs/img_1.png)

#### 技术难点
    1.Xpath
    2.网络波动，页面返回的问题
    3.分布式爬虫，大规模数据的爬取会用到

### 3.爬取的数据
#### 数据：
![img_2.png](imgs/img_2.png)
![img_3.png](imgs/img_3.png)
### 4.分析和处理爬取的数据
#### 数据的清洗和整理
    1)得到的疾病有11000条数据
    2)经过初步清除之后，有疾病1w条，症状7100条
        disease（疾病）-symptom（症状）
        去除一个字的症状
        AC自动机
    3)数据补充
        39健康网，博禾医生网

#### 问答数据情况：
    1)数据量有8w
    2)为后续任务提供数据支持

### 5.目录结构

    │  data_spider.py          寻医问药网疾病爬虫
    │  json文件读取问题.py  
    │  qa_39.py                39健康网问答数据爬虫
    │  qa_xywy.py              寻医问药网问答数据爬虫
    │  readme.md
    │  数据情况.txt
    │
    ├─processed_data           处理之后的数据
    │      disease.txt         疾病
    │      disease_symptom_data.json  疾病——症状对应
    │      symptom.txt         症状
    │
    └─raw_data                 原始数据
        data.json              寻医问药网疾病数据
        qa_39_data.json        39健康网问答数据
        qa_xywy_data.json      寻医问药网问答数据

文件名称|内容|数量
:----|:-----:|-----:
data.json|知识图谱全部数据|1w
disease_symptom_data.json|疾病_症状数据|9700
disease.txt|所有疾病名称|9700
symptom.txt|所有症状名称|7000
qa_xywy_data.json|寻医问药网 问答数据|6w
qa_39_data.json|39健康网 问答数据|1.5w

data.json保存的字段|        |
:----|--------|
疾病基本信息||
1| 疾病名称   |
  2| 疾病描述   |
  3| 科室     |
  4| 是否医保疾病 |
  5| 患病比例   |
  6| 易感人群   |
  7| 传染方式   |
  8| 并发症    |
  9| 治疗方式   |
  10| 治疗周期   |
  11| 治愈率    |
  12| 常用药品   |
  13| 治疗费用   |
发病原因|
预防方法|
症状信息|
检查信息|
食物|
  1| 宜吃食品   |
  2| 忌吃食品   |
  3| 推荐食谱   |
治疗药品|
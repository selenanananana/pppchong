# -*- coding: utf-8 -*-            
# @Author : hujingsong
# @Time : 2021/12/29 8:35
# @software : PyCharm、
import json
def load_data():
    data_path = r'D:\PycharmProjects\pythonProject\N5\医疗机器人\医疗机器人\doctor_online\bert_serve\spiderpro\raw_data\qa_xywy_data.json'
    data = []
    try:
        data_list = []
        for line in open(data_path, 'r', encoding='utf-8'):
            data_list.append(line.replace("',",'').strip())
            # 将列表合并成一个字符串
            # print(data_list)
        json_str = ''.join(data_list).split('}{')
        # print(len(json_str))
        for i, s in enumerate(json_str):
            if i == 0:
                result = json.loads(s + '}')
                data.append(result)
            elif i == len(json_str) - 1:
                result = json.loads('{' + s)
                data.append(result)
            else:
                result = json.loads('{' + s + '}')
                data.append(result)
    except json.decoder.JSONDecodeError as e:
        print(f'JSON格式错误：{e}')
        # 在发生错误时返回默认值
    return data

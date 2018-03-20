import config
import json

def get_category_from_json(json_file):
    """
    从 json 文件中获取数据
    :param
            - json_file:  json 文件
    :return:
            - category_dict:    category字典
    """
    category_dict = {}

    with open(json_file, 'r') as f:
        data = json.load(f)
        for category in data['items']:
            category_dict[int(category['id'])] = category['snippet']['title']

    return category_dict

json_file = './data/CA_category_id.json'
print(get_category_from_json(json_file))


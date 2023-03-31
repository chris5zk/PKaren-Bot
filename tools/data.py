import json


def get_json():
    with open('data.json', 'r', encoding='utf8') as file:
        return json.load(file)

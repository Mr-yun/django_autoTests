# -*- coding:utf-8 -*-
import os

from json import loads

from auto_tests import AutoTests
from const import CONST
from loggers.logger import log

def get_json():
    list_json = []
    for i in os.listdir(CONST.JSON_PATH):
        if i.endswith('.json'):
            log.info('read json_files files:{}'.format(i))
            with open(os.path.join(CONST.JSON_PATH, i), 'r') as f:
                str_value = f.read()
            list_json.append({'value':loads(str_value),'file_name':i[:-5]})
    return list_json


if __name__ == "__main__":
    list_json = get_json()
    for create_json in list_json:
        obj_auto_tests = AutoTests()
        obj_auto_tests.run(create_json)

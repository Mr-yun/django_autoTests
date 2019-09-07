# -*- coding:utf-8 -*-
import os

from requests import get as req_get

from const import CONST
from loggers.logger import log


class AutoTests(object):
    def __init__(self, new_api=None):
        '''
        :param new_api: 指定更新接口
        '''
        self.str_template = CONST.STR_TEMPLATE
        self.new_api = new_api

    def __add_new_test_function(self, method, keys, add_string):
        '''生成测试方法'''
        self.str_template += '''
                        \n
    def _test_{0}_{1}(self):
        {2}
                    '''.format(method, keys,
                               add_string[9:])

    def __check_get_result(self, dict_url, add_string):
        '''get 操作需要检查参数个数'''
        try:
            rsp = req_get(dict_url.get('full_url')).json()
            for rsp_k, rsp_v in rsp.items():
                if rsp_k != 'result' and rsp_k != 'count':
                    if isinstance(rsp_v, list):
                        dict_rsp_value = rsp_v[0]
                    else:
                        dict_rsp_value = rsp_v

                    if isinstance(dict_rsp_value, dict):
                        # 递归查询字典内
                        for _k in dict_rsp_value.keys():
                            add_string += CONST.ASSERT_NONE.format(_k)
                    else:
                        add_string += CONST.ASSERT_NONE.format(dict_rsp_value)

        except Exception as e:
            log.error('error:{}'.format(dict_url.get('full_url')))

        return add_string

    def __code_get_or_delete(self, keys, method, list_value):
        '''get,delete'''
        add_string = ''
        for dict_url in list_value:
            add_string += CONST.STR_TEMPLATE_CHECK_RESULT.format(method, dict_url.get('url'))
            if method == CONST.METHOD_GET:
                add_string = self.__check_get_result(dict_url, add_string)
                if add_string is None:
                    continue
                else:
                    add_string += '\n'
            log.info('end:{}-{}'.format(method, dict_url.get('url')))
        self.__add_new_test_function(method, keys, add_string)

    def __code_put_or_post(self, keys, method, list_value):
        add_string = ''
        for dict_url in list_value:
            add_string += CONST.STR_TEMPLATE_SENT_BODY_RESULT.format(dict_url.get('url'), dict_url.get('data'), method)
            log.info('end:{}-{}'.format(method, dict_url.get('url')))
        self.__add_new_test_function(method, keys, add_string)

    def create_function(self, dict_get):
        list_method = {}
        for keys, values in dict_get.items():
            if keys not in list_method:
                list_method[keys] = {}

            for method, list_value in values.items():
                if len(list_value) == 0:
                    continue

                add_string = ''
                if method in [CONST.METHOD_GET, CONST.METHOD_DELETE]:
                    self.__code_get_or_delete(keys, method, list_value)
                else:
                    self.__code_put_or_post(keys, method, list_value)
                list_method[keys][method] = 'self._test_{0}_{1}()'.format(method, keys)

        return list_method

    def analysis_url(self, value):
        '''解析postman'''
        dict_url = {}
        parameter_method = 'method'

        for z in value.get('requests'):
            view_url = z.get('url').split('?')[0].split('/')[-1]
            if self.new_api is None or self.new_api == view_url:
                if view_url not in dict_url:
                    dict_url[view_url] = {CONST.METHOD_GET: [], CONST.METHOD_PUT: [], CONST.METHOD_POST: [],
                                          CONST.METHOD_DELETE: []}
                dict_url[view_url][z.get('method').lower()].append({'url': '/' + '/'.join(z.get('url').split('/')[1:]),
                                                                    'full_url': 'http://' + z.get('url'),
                                                                    'method': z.get(parameter_method).lower()})

                if z.get(parameter_method) == CONST.METHOD_POST or z.get(parameter_method) == CONST.METHOD_PUT:
                    # 获取提交数据
                    if z.get('rawModeData'):
                        dict_url[view_url][z.get(parameter_method).lower()][-1]['data'] = z.get('rawModeData').replace(
                            'null',
                            'None')
                    else:
                        dict_url[view_url][z.get(parameter_method).lower()][-1]['data'] = z.get('rawModeData')
        return dict_url

    def __save_files(self, file_name):
        if os.path.exists(CONST.SAVE_DIR) is None:
            os.makedirs(CONST.SAVE_DIR)

        with open(os.path.join(CONST.SAVE_DIR, file_name + '.py'), 'w') as f:
            f.write(self.str_template)

    def __add_test(self, list_method):
        self.str_template += '''
    def test(self):
    '''
        for k, v in list_method.items():
            self.str_template += '''
            #{}\n'''.format(k)
            if v.get(CONST.METHOD_POST):
                self.str_template += '        ' + v.get(CONST.METHOD_POST) + '\n'
            if v.get(CONST.METHOD_GET):
                self.str_template += '        ' + v.get(CONST.METHOD_GET) + '\n'
            if v.get(CONST.METHOD_PUT):
                self.str_template += '        ' + v.get(CONST.METHOD_PUT) + '\n'
            if v.get(CONST.METHOD_DELETE):
                self.str_template += '        ' + v.get(CONST.METHOD_DELETE) + '\n'

    def run(self, create_json):
        dict_url = self.analysis_url(create_json.get('value'))
        list_method = self.create_function(dict_url)
        self.__add_test(list_method)
        self.__save_files(create_json.get('file_name'))

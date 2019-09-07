# -*- coding:utf-8 -*-
class _CONST(object):
    LOCALHOST = 'localhost'

    STR_TEMPLATE = '''
from traceback import print_exc

from django.test import Client
from django.test import TestCase
from json import loads, dumps

class TestDjango(TestCase):
    ip = 'localhost' # 测试服务器ip
    client = Client()
    def sent_date(self, url, data, method='post'):
            try:
                if method == 'post':
                    response = self.client.post(url,
                                       dumps(data),
                                       content_type="application/json_files", **{'HTTP_X_REAL_IP': self.ip})
                else:
                    response = self.client.put(url,
                                       dumps(data),
                                       content_type="application/json_files", **{'HTTP_X_REAL_IP': self.ip})
                return loads(response.content.decode("utf-8"))
            except Exception:
                print_exc()
                return None

    def _loads(self, content):
        return loads(content.decode('utf-8'))

    '''

    METHOD_GET = 'get'
    METHOD_POST = 'post'
    METHOD_PUT = 'put'
    METHOD_DELETE = 'delete'

    STR_TEMPLATE_CHECK_RESULT = '''
        value = self._loads(self.client.{0}('{1}').content)
        assert value.get('result') == 'success' '''
    STR_TEMPLATE_SENT_BODY_RESULT = '''
        value = self.sent_date('{0}',{1},'{2}')
        assert value.get('result') == 'success'
                            '''
    ASSERT_NONE = "\n        assert value.get('{0}') is not None"

    SAVE_DIR = './tests'
    JSON_PATH = './json_files'

CONST = _CONST()

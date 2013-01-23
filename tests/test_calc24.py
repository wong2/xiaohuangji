# -*- coding: utf-8 -*-

"""
Copyright (c) 2013 Moody _"Kuuy"_ Wizmann <mail.kuuy@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
'Software'), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

""" Calc24 plugin test """

__author__ = 'Moody _"Kuuy"_ Wizmann'
__copyright__ = 'Copyright (c) 2013 Wizmann'
__license__ = 'MIT'
__version__ = '0.1'
__maintainer__ = 'Wizmann'
__email__ = 'mail.kuuy@gmail.com'
__status__ = 'development'

from nose.tools import ok_
from nose.tools import eq_
from test_config import *
from ..plugins import calc24

sys.path = [TEST_DIR] + sys.path


class TestCalc24(TestBase):

    def setup(self):
        pass

    def teardown(self):
        pass

    def test_calc24_test_1(self):
        eq_(False, calc24.test({'message': 'Hello World 24'}, None),
            WRONG_KEY_WORD_ERROR)

    def test_calc24_test_2(self):
        eq_(False, calc24.test({'message': 'Hello World 算24点'}, None),
            WRONG_KEY_WORD_ERROR)

    def test_calc24_test_3(self):
        eq_(True, calc24.test({'message': 'Hello World 算24点 [1,2,4,5]'},
            None), WRONG_RESULT_ERROR)

    def test_calc24_handle_1(self):
        result = calc24.handle({'message': 'Hello World 算24点 [1,2,4,5]',
                                'author_id': 'Wizmann'}, None)
        eq_(True, '答案' in result, WRONG_RESULT_FORMAT_ERROR)

    def test_calc24_handle_2(self):
        result = calc24.handle({'message': 'Hello World 算24点 [A,A,A,A]',
                                'author_id': 'Wizmann'}, None)
        eq_(True, '答案' in result, WRONG_RESULT_FORMAT_ERROR)

    def test_calc24_handle_3(self):
        result = calc24.handle({'message': 'Hello World 算24点 [F,U,C,K]',
                                'author_id': 'Kuuy'}, None)
        eq_(True, '没有那种牌' in result, WRONG_RESULT_FORMAT_ERROR)

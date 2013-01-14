# -*- coding: utf-8 -*-

"""
Copyright (c) 2013 Xiangyu Ye<yexiangyu1985@gmail.com>

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

""" QiuBai plugin test
"""

from nose.tools import ok_
from nose.tools import eq_
from test_config import *
from ..plugins import qiubai

sys.path = [TEST_DIR] + sys.path


class TestQiuBai(TestBase):

    def setup(self):
        pass

    def teardown(self):
        pass

    def test_qiubai_test_1(self):
        eq_(False, qiubai.test({'message': '讲个感人的故事吧'}, None), WRONG_KEY_WORD_ERROR)

    def test_qiubai_test_2(self):
        eq_(True, qiubai.test({'message': '给我讲个笑话吧'}, None), WRONG_RESULT_ERROR)

    def test_qiubai_test_3(self):
        eq_(True, qiubai.test({'message': '给我讲个糗百上的故事吧'}, None), WRONG_RESULT_ERROR)

    #TODO: Add better unit test
    def test_qiubai_handle_1(self):
        eq_(True, qiubai.handle({'message': '讲个笑话吧'}, None) != '', WRONG_RESULT_FORMAT_ERROR)

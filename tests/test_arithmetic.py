# -*- coding: utf-8 -*-

"""
Copyright (c) 2013 Pili Hu <hpl1989@gmail.com>

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

""" Arithmetic plugin test

    Test Cases for xiaohuangji Arithmetic plugin
"""

__author__ = 'hupili'
__copyright__ = 'Copyright (c) 2013 hupili'
__license__ = 'MIT'
__version__ = '0.1'
__maintainer__ = 'hupili'
__email__ = 'hpl1989@gmail.com'
__status__ = 'development'

from nose.tools import ok_
from nose.tools import eq_
from test_config import *
from ..plugins import arithmetic

sys.path = [TEST_DIR] + sys.path


class TestArithmetic(TestBase):

    def setup(self):
        pass

    def teardown(self):
        pass

    def test_arithmetic_test(self):
        _ut_test('hello', False)
        _ut_test('2 * 4+ 5/3 = ?', True)
        _ut_test('x *4+ 5/3 =?', True)
        _ut_test('2 * 4+ 5/3= ？', True)
        _ut_test('2 * 4+ 5/3 是多少', True)
        _ut_test('2 * 4+ 5/3 是几', True)
        _ut_test('2 * 4+ 5/3 等于多少', True)
        _ut_test('2 * 4+ 5/3 等于几', True)
        _ut_test('sys.exit(-1)', False)
        _ut_test('sys.exit(-1) = ?', True)
        _ut_test('sin(pi/2)=?', True)
        _ut_test('x^(1+3)=?', True)

    def test_arithmetic_handle_normal_basic(self):
        _ut_handle('2 * 4+ 5/3 = ?', '不就是29/3嘛。啦啦啦……我是计算鸡…… ＼（￣︶￣）／')
        _ut_handle('2 * 4+ 5/3= ？', '不就是29/3嘛。啦啦啦……我是计算鸡…… ＼（￣︶￣）／')
        _ut_handle('2 * 4+ 5/3 是多少', '不就是29/3嘛。啦啦啦……我是计算鸡…… ＼（￣︶￣）／')
        _ut_handle('2 * (4+ 5)/3 是几', '不就是6嘛。啦啦啦……我是计算鸡…… ＼（￣︶￣）／')
        _ut_handle('2 * 4+ 5/(3.0) 是几', '不就是9.66666666666667嘛。啦啦啦……我是计算鸡…… ＼（￣︶￣）／')
        # The matched part is "(-1)" not "sys.exit(-1)"
        _ut_handle('sys.exit(-1) = ?', '好复杂哦，计算鸡也不会了 ╮(︶︿︶)╭')

    def test_arithmetic_handle_normal_advanced(self):
        _ut_handle('sin(pi/2)=?', '不就是1嘛。啦啦啦……我是计算鸡…… ＼（￣︶￣）／')
        _ut_handle('atan(1)=?', '不就是pi/4嘛。啦啦啦……我是计算鸡…… ＼（￣︶￣）／')
        _ut_handle('integrate(x * e ** (-x), x)=?', '不就是-e^(-x)*x/log(e) - e^(-x)/log(e)^2嘛。啦啦啦……我是计算鸡…… ＼（￣︶￣）／')

    def test_arithmetic_handle_with_pre_and_post_process(self):
        # Test the conversion between "^" and "**"
        _ut_handle('x^(1+3)=?', '不就是x^4嘛。啦啦啦……我是计算鸡…… ＼（￣︶￣）／')

    def test_arithmetic_handle_exception(self):
        # Syntax error
        _ut_handle(' *4+ 5/3 =?', '(´･д･`) 这明显有问题嘛！！你确定没写错？')
        # The following is originally Syntax error.
        # After allowing letters in expression, it is no longer syntax error.
        # Also, sympy will retain x as a symbol.
        _ut_handle('x *4+ 5/3 =?', '不就是4*x + 5/3嘛。啦啦啦……我是计算鸡…… ＼（￣︶￣）／')
        # Zero division: error in Python eval; infinity in sympy
        #_ut_handle('2 * 4+ 5/0 是几', '你好笨啊！除零了。跟小鸡学下四则运算吧 （＃￣▽￣＃）')
        _ut_handle('2 * 4+ 5/0 是几', '不就是oo嘛。啦啦啦……我是计算鸡…… ＼（￣︶￣）／')
        # Long input expression
        _ut_handle('1' + ('+1' * (arithmetic.AI_ARITHMETIC_MAX_LEN_EXP / 2 - 1)) + '=?',
                   '不就是%d嘛。啦啦啦……我是计算鸡…… ＼（￣︶￣）／' % (arithmetic.AI_ARITHMETIC_MAX_LEN_EXP / 2))
        _ut_handle('1' + ('+1' * (arithmetic.AI_ARITHMETIC_MAX_LEN_EXP / 2)) + '=?', '太长了……小鸡才不算呢。╮(︶︿︶)╭')
        _ut_handle(('1' * (arithmetic.AI_ARITHMETIC_MAX_LEN_REPLY)) + '=?',
                   '不就是%s嘛。啦啦啦……我是计算鸡…… ＼（￣︶￣）／' % ('1' * (arithmetic.AI_ARITHMETIC_MAX_LEN_REPLY)))
        _ut_handle(('1' * (arithmetic.AI_ARITHMETIC_MAX_LEN_REPLY + 1)) + '=?', '这个数字太长了！鸡才懒得回你呢╮(︶︿︶)╭')

    def test_arithmetic_handle_false_flow(self):
        # The following text will not get True from test(). It will not
        # reach handle(). Verify whether we handle it correctly if this
        # happens due to incorrect configuration.
        _ut_handle('sys.exit(-1)', '好复杂哦，计算鸡也不会了 ╮(︶︿︶)╭ （怎么会这样？）')

    def test_arithmetic_handle_timeout(self):
        _ut_handle('2**' + ('9' * (arithmetic.AI_ARITHMETIC_MAX_LEN_EXP - 3)) + '=?', '太难了，计算鸡半天都算不出来 ╮(︶︿︶)╭')


def _ut_test(exp, ret):
    eq_(ret, arithmetic.test({'message': exp}, None), WRONG_RESULT_ERROR)


def _ut_handle(exp, ret):
    print exp, ': ', ret, '\n'
    eq_(ret, arithmetic.handle({'message': exp}, None), WRONG_RESULT_ERROR)

#!/usr/bin/env python
#-*-coding:utf-8-*-

"""
Copyright (c) 2013 Pili Hu <hpl1989@gmail.com>

Original Author:
        Phili Hu <hpl1989@gmail.com>

Changed By
        Qijiang Fan <fqj1994@gmail.com>
        1. Convert expr to float values if accurate value is too long
        2. Handle TokenError.

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

# Arithmetic Module
#
# Emoji from:
#     http://zh.wikipedia.org/wiki/%E8%A1%A8%E6%83%85%E7%AC%A6%E5%8F%B7

import re
from timeout import timeout, TimeoutException
from sympy.parsing import sympy_parser
from sympy.parsing.sympy_tokenize import TokenError

try:
    from settings import AI_ARITHMETIC_REGEX_TEST
except:
    AI_ARITHMETIC_REGEX_TEST = '([ \(\.\)0-9a-zA-Z,+\-*^/]+)((\s*=\s*(\?|？))|(\s*(是多少|是几|等于几|等于多少)))'

try:
    from settings import AI_ARITHMETIC_REGEX_HANDLE
except:
    AI_ARITHMETIC_REGEX_HANDLE = AI_ARITHMETIC_REGEX_TEST

try:
    from settings import AI_ARITHMETIC_MAX_LEN_EXP
except:
    AI_ARITHMETIC_MAX_LEN_EXP = 120

try:
    from settings import AI_ARITHMETIC_MAX_LEN_REPLY
except:
    AI_ARITHMETIC_MAX_LEN_REPLY = 100

try:
    from settings import AI_ARITHMETIC_EVAL_TIMEOUT
except:
    AI_ARITHMETIC_EVAL_TIMEOUT = 1.0  # Second

REGEX_TEST = re.compile(AI_ARITHMETIC_REGEX_TEST)
REGEX_HANDLE = re.compile(AI_ARITHMETIC_REGEX_HANDLE)


def test(data, bot):
    return True if REGEX_TEST.search(data['message']) else False


def handle(data, bot):
    try:
        exp = REGEX_HANDLE.search(data['message']).groups()[0]
    except:
        # The flow is not supposed to reach here. 'data' is already
        # tested by AI_ARITHMETIC_REGEX_TEST so we should be able to
        # read group()[0]. This is just to prevent your customized
        # regex from causing errors.
        return '好复杂哦，计算鸡也不会了 ╮(︶︿︶)╭ （怎么会这样？）'

    try:
        return cal(exp)
    except TimeoutException:
        return '太难了，计算鸡半天都算不出来 ╮(︶︿︶)╭'


@timeout(AI_ARITHMETIC_EVAL_TIMEOUT)
def cal(exp):
    if len(exp) > AI_ARITHMETIC_MAX_LEN_EXP:
        return '太长了……小鸡才不算呢。╮(︶︿︶)╭'

    try:
        ansexp = sympy_parser.parse_expr(exp.replace('^', '**'))
        ans = str(ansexp).replace('**', '^')
        i = 15
        while len(ans) > AI_ARITHMETIC_MAX_LEN_EXP:
            ans = str(ansexp.evalf(i)).replace('**', '^')
            i = i - 1
            if i <= 0:
                break

        if len(ans) > AI_ARITHMETIC_MAX_LEN_REPLY:
            return '这个数字太长了！鸡才懒得回你呢╮(︶︿︶)╭'
        else:
            return '不就是%s嘛。啦啦啦……我是计算鸡…… ＼（￣︶￣）／' % ans
    except ZeroDivisionError:
        return '你好笨啊！除零了。跟小鸡学下四则运算吧 （＃￣▽￣＃）'
    except SyntaxError:
        return '(´･д･`) 这明显有问题嘛！！你确定没写错？'
    except TokenError:
        return '(´･д･`) 这明显有问题嘛！！你确定没写错？'
    except Exception, e:
        #TODO:
        #    Any logging convention in this project? We should log the
        #    error for further investigation
        #raise e
        return '好复杂哦，计算鸡也不会了 ╮(︶︿︶)╭'

if __name__ == '__main__':
    print "Unit tests are now moved to 'test_arithmetic.py'"
    pass

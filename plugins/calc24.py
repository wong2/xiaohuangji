#coding=utf-8

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

import sys
import re
import os
import sqlite3

reload(sys)
sys.setdefaultencoding('utf-8')


class Calc24db:
    def __init__(self):
        db_path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)),
            'data', 'calc24.sqlite3')
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def search(self, nums):
        SQL = "SELECT `answer` FROM `calc24` WHERE `hashcode`={0}"
        hashcode = reduce(lambda x, y: x * 13 + y, sorted(nums))
        self.cursor.execute(SQL.format(hashcode))
        answer = self.cursor.fetchall()
        if answer:
            return answer[0][0]
        else:
            return None


calc24db = Calc24db()


class Calc24Exception(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


def test(data, bot):
    message = data['message']
    if '算24点' not in message \
            or not re.match('(?:.*\[)(.+)(?:\][.]*)', message):
        return False
    else:
        return True


def solve(nums):
    try:
        s = calc24db.search(nums)
        if(s):
            return s.strip()
        else:
            return None
    except Exception, e:
        return str(e)


def handle(data, bot):
    message = data['message']
    query = re.findall('(?:.*\[)(.+)(?:\][.]*)', message)
    try:
        if len(query) == 0:
            raise Calc24Exception("表达式错误哦~")
        else:
            nums = map(lambda x: x.strip(), query[0].split(','))
            if len(nums) != 4:
                raise Calc24Exception("参数错误哦~")
            else:
                def conv(ch):
                    try:
                        t = int(ch)
                    except:
                        t = ch
                    if(1 <= t <= 10):
                        return t
                    else:
                        conv_dict = {'A': 1, 'J': 11, 'Q': 12, 'K': 13}
                        t = conv_dict.get(t, None)
                        if t:
                            return t
                        else:
                            raise Calc24Exception("明明没有那种牌嘛～")
                nums = map(conv, nums)
                ans = solve(nums)
                return "没有答案哦~" if not ans else '答案是：' + ans
    except Exception, e:
        return str(e)


if(__name__ == '__main__'):
    print test({'message': "@小黄鸡  算24点 不算烧死 [1,2,3,4]你好世界"}, None)
    print test({'message': "@小黄鸡  算24点 不算烧死 [A,A,A,A]你好世界"}, None)
    print test({'message': 'Hello World 算24点'}, None)
    print handle({'message':
                  '@小黄鸡  算24点 不算烧死 [Q,K,A,A]你好世界',
                  'author_id': 'Wizmann'}, None)
    print handle({'message':
                  '@小黄鸡  算24点 不算烧死 [A,A,A,A]你好世界',
                  'author_id': 'Wizmann'}, None)
    print handle({'message': 'Hello World 算24点 [F,U,C,K]',
                 'author_id': 'Kuuy'}, None)

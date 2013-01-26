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
            'data', 'CalcXdb.sqlite3')
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def search(self, ans, nums):
        SQL = "SELECT `formula` FROM `calcx` \
                WHERE `ans`={0} AND `hashcode`={1}"
        hashcode = reduce(lambda x, y: x * 13 + y, sorted(nums))
        self.cursor.execute(SQL.format(ans, hashcode))
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
    if not re.search('算[\d-]+点', message) \
            or not re.search('(?:.*\[)(.+)(?:\][.]*)', message):
        return False
    else:
        return True


def solve(ans, nums):
    try:
        s = calc24db.search(ans, nums)
        if(s):
            return s.strip()
        else:
            return None
    except Exception, e:
        return str(e)


def handle(data, bot):
    message = data['message']
    query = re.findall('(?:.*\[)(.+)(?:\][.]*)', message)
    ans = re.findall('算([\d-]+)点', message)
    try:
        if len(query) == 0 or len(ans) == 0:
            raise Calc24Exception("表达式错误哦~")
        else:
            try:
                ans = int(ans[0])
            except:
                raise Calc24Exception("表达式错误哦~")
            nums = map(lambda x: x.strip(), query[0].split(','))
            if ''.join(nums) == 'FUCK':
                return 'Coded by Wizmann~'
            elif ''.join(nums) == 'SEXY':
                return 'I love SEX!'
            elif len(nums) != 4:
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
                formula = solve(ans, nums)
                return "没有答案哦~" if not formula else '答案是：' + formula
    except Exception, e:
        return str(e)


if(__name__ == '__main__'):
    print test({'message': "@小黄鸡  算24点 不算烧死 [1,2,3,4]你好世界"}, None)
    print test({'message': "@小黄鸡  算24点 不算烧死 [A,A,A,A]你好世界"}, None)
    print test({'message': "@小黄鸡  算16点 不算烧死 [4,4,4,4]你好世界"}, None)
    print test({'message': 'Hello World 算24点'}, None)
    print handle({'message':
                  '@小黄鸡  算24点 不算烧死 [Q,K,A,A]你好世界',
                  'author_id': 'Wizmann'}, None)
    print handle({'message':
                  '@小黄鸡  算24点 不算烧死 [A,A,A,A]你好世界',
                  'author_id': 'Wizmann'}, None)
    print handle({'message':
                  '@小黄鸡  算-2点 不算烧死 [A,A,A,A]你好世界',
                  'author_id': 'Wizmann'}, None)
    print handle({'message':
                  '@小黄鸡  算----------点 不算烧死 [3,3,8,8]你好世界',
                  'author_id': 'Wizmann'}, None)
    print handle({'message':
                  '@小黄鸡  算24点 不算烧死 [3,3,8,8]你好世界',
                  'author_id': 'Wizmann'}, None)
    print handle({'message':
                  '@小黄鸡  算16点 不算烧死 [4,4,4,4]你好世界',
                  'author_id': 'Wizmann'}, None)
    print handle({'message':
                  '@小黄鸡  算256点 不算烧死 [8,8,4,4]你好世界',
                  'author_id': 'Wizmann'}, None)
    print handle({'message':
                  '算132465点 [A,2,Q,K]',
                  'author_id': 'Wizmann'}, None)
    print handle({'message':
                  '算0点 [1,K,Q,K]',
                  'author_id': 'Wizmann'}, None)
    print handle({'message':
                  '算512点 [ZZ,2,Q,K]',
                  'author_id': 'Wizmann'}, None)
    print handle({'message': 'Hello World 算24点 [F,U,C,K]',
                 'author_id': 'Kuuy'}, None)

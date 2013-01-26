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

"""
算X点答案预处理脚本
速度极慢
CPU 2.3G + RAM 4G 用时为6分钟+

生成一个sqlite3数据库，查询速度较快，基本没有延时
没有在大规模并发下进行测试，目测问题不大

在使用CalcX插件前，先要生成答案数据库
而且要删除目录下的CalcXdb.sqlite3文件

由于不是线上代码，所以写的比较屎，见谅

By Moody _"Kuuy"_ Wizmann
"""

from __future__ import division
import sys
import os
import sqlite3

CREATE_SQL = '''
CREATE TABLE IF NOT EXISTS `calcX`
(
    id INTEGER NOT NULL  primary key autoincrement ,
    ans INTEGER NOT NULL,
    hashcode INTEGER NOT NULL,
    formula TEXT NOT NULL
);
'''

INDEX_SQL = '''
CREATE INDEX IF NOT EXISTS idx_ans_hashcode ON `calcX`(`ans`,`hashcode`);
'''


class CalcXdb:
    def __init__(self):
        db_path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'CalcXdb.sqlite3')
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute(CREATE_SQL)
        self.cursor.execute(INDEX_SQL)
        self.visit = set()

    def insert(self, key, values):
        SQL = 'INSERT INTO `calcX` (`ans`,`hashcode`,`formula`)\
                VALUES ({0},{1},"{2}")'
        for ans, formula in values:
            if (ans, key) in self.visit:
                continue
            else:
                self.visit.add((ans, key))
            _SQL = SQL.format(ans, key, formula)
            #print _SQL
            self.cursor.execute(_SQL)

    def commit(self):
        self.conn.commit()


formula_set = (
    '(%d%c%d)%c(%d%c%d)',
    '((%d%c%d)%c%d)%c%d',
    '(%d%c(%d%c%d)%c%d)',
    '%d%c(%d%c(%d%c%d))',
    '%d%c((%d%c%d)%c%d)')


def conv_int(x):
    if abs(x-round(x)) < 1e-8:
        if abs(x) < 1e-8:
            return 0
        else:
            return int(x + (0.5 * (x / abs(x))))
    else:
        return None


def calc(formula, nums, oprs):
    oprs = map(lambda x: {0: '+', 1: '-', 2: '*', 3: '/'}[x], oprs)
    formula = formula % (nums[0], oprs[0],
                         nums[1], oprs[1],
                         nums[2], oprs[2],
                         nums[3])
    try:
        ans = conv_int(eval(formula))
        if ans:
            return (ans, formula)
        else:
            return None
    except Exception, e:
        return None


def slove(a, b, c, d):
    answer = []
    for i in xrange(4):
        for j in xrange(4):
            for k in xrange(4):
                for formula in formula_set:
                    ans = calc(formula, [a, b, c, d], [i, j, k])
                    if ans:
                        answer.append(ans)
    return answer


def main():
    _CalcXdb = CalcXdb()
    for i in xrange(13):
        for j in xrange(13):
            for k in xrange(13):
                for l in xrange(13):
                    nums = [i + 1, j + 1, k + 1, l + 1]
                    print nums
                    hashcode = reduce(lambda x, y: x * 13 + y, sorted(nums))
                    answer = slove(*nums)
                    _CalcXdb.insert(hashcode, answer)
    _CalcXdb.commit()


if __name__ == '__main__':
    main()

#-*-coding:utf-8-*-

"""
Copyright (c) 2012 wong2 <wonderfuly@gmail.com>

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


# 小黄鸡的ai，先自己尝试处理，没结果则交给simsimi

import time
from simsimi import SimSimi

simi = SimSimi()


def my_logic(text):
    # 教学模式: /Q python和ruby哪个好？ /A php最好！
    if '/Q' in text and '/A' in text:
        _, right_part = text.split('/Q', 1)
        question, answer = [s.strip() for s in right_part.split('/A', 1)]
        if question and answer:
            simi.teach(question, answer)
            return '学会啦'

    return None


# some magic here
def magic(text):
    text = text.strip()
    return simi.chat(text).encode('utf-8')

if __name__ == '__main__':
    print magic('/Q 今天天气怎么样？ /A 大雪')

#!/usr/bin/env python
#-*-coding:utf-8-*-

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

# 糗事百科TOP10
import urllib2
import re
import redis
import time
import random

try:
    from settings import REDIS_HOST
except:
    REDIS_HOST = 'localhost'

kv = redis.Redis(REDIS_HOST)

key = time.strftime('%Y-%m-%d')


def test(data, bot):
    return any(w in data['message'] for w in ['糗百', '笑话'])

def handle(data, bot):
    r = kv.lrange(key, 0, -1)
    if r:
        return random.choice(r)
    r = urllib2.urlopen('http://feed.feedsky.com/qiushi', timeout=60)
    p = r.read()
    r = re.findall('&lt;p&gt;([\s]+)([^\t]+)&lt;br/&gt;', p)
    if r:
        for l in r:
            kv.rpush(key, l[1])
        return random.choice(r)[1]
    else:
        raise Exception

if __name__ == '__main__':
    print handle({'message': '糗百'}, None)
    print handle({'message': '笑话'}, None)

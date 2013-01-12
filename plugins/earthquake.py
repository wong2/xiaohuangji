#!/usr/bin/env python
#-*-coding:utf-8-*-

"""
Copyright (c) 2012 Qijiang Fan <fqj1994@gmail.com>

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

# 地震
import StringIO
import time
import urllib2
import re


def test(data, bot):
    return '地震了' in data['message']


def jw(a, b):
    aa = ''
    bb = ''
    if int(a.replace('.', '')) > 0:
        aa = '北纬' + a + '度'
    elif int(a.replace('.', '')) < 0:
        aa = '南纬' + a.replace('-', '') + '度'
    else:
        aa = '赤道附近'
    if int(b.replace('.', '')) > 0:
        bb = '东经' + b + '度'
    elif int(b.replace('.', '')) < 0:
        bb = '西经' + b.replace('-', '') + '度'
    else:
        bb = '本初子午线附近'
    return '，'.join((aa, bb))


def handle(data, bot):
    r = urllib2.urlopen('http://data.earthquake.cn/datashare/globeEarthquake_csn.html',
            timeout=5)
    t = [re.sub('(<[^>]*>|[\r\n])', '', a) for a in r.read().decode('gbk').encode('utf-8').split('\n')[170:178]]
    return '最近一次地震发生在%s（%s），发生时间%s，震级%s，震源深度%s千米，地震类型为%s。' %\
            (t[7], jw(t[2], t[3]), ' '.join(t[0:2]), t[5], t[4], t[6])

if __name__ == '__main__':
    print handle({'message': '地震了吗？'}, None)

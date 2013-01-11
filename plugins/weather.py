#!/usr/bin/env python
#-*-coding:utf-8-*-

"""
Copyright (c) 2013 Qimin Huang <qiminis0801@gmail.com>

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

# 天气
import requests
import json
import cPickle as pickle


def test(data, bot):
    return '天气' in data['message']


def weather(cityid):
    flag = 1
    count = 0  # 尝试进行三次数据获取
    while flag and count < 3:
        try:
            r = requests.get('http://www.weather.com.cn/data/cityinfo/' + cityid + '.html')
            weatherinfo = json.loads(r.text)[u'weatherinfo']
            flag = 0
        except:
            count += 1
    try:
        return (weatherinfo[u'city'] + u', ' + weatherinfo[u'weather'] + u', ' + weatherinfo[u'temp1'] + u' ~ ' + weatherinfo[u'temp2']).encode('utf8')
    except:
        return 0


def handle(data, bot):
    # 加载城市名称和城市id
    cityidDict = pickle.load(file('./cityid', 'r'))
    cityFlag = False
    for city in cityidDict.keys():
        if city.encode('utf8') in data['message']:
            reply = weather(cityidDict[city])
            cityFlag = True
            break
    if not cityFlag:
        reply = '亲爱的'+data['author_id']+'，您想知道哪个城市的天气啊！！！'
    if 0 == reply:
        return '亲爱的'+data['author_id']+'，服务器连接失败， 啊啊啊啊啊啊！！！'
    else:
        return reply

if __name__ == '__main__':
    print test({'message': '天气怎么样'}, None)
    print handle({'message': '天气怎么样', 'author_id': 'HQM'}, None)
    print handle({'message': '北京天气怎么样', 'author_id': 'HQM'}, None)

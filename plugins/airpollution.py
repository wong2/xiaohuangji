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

# 空气污染
import urllib2
import re
import json
import redis
try:
    from settings import REDIS_HOST
except:
    REDIS_HOST = 'localhost'

city = json.loads("""[["\u5317\u4eac", "Beijing"], ["\u5929\u6d25", "Tianjin"], ["\u4e0a\u6d77", "Shanghai"], ["\u91cd\u5e86", "Chongqing"], ["\u77f3\u5bb6\u5e84", "Shijiazhuang"], ["\u5510\u5c71", "Tangshan"], ["\u79e6\u7687\u5c9b", "Qinhuangdao"], ["\u90af\u90f8", "Handan"], ["\u4fdd\u5b9a", "Baoding"], ["\u90a2\u53f0", "Xingtai"], ["\u5f20\u5bb6\u53e3", "Zhangjiakou"], ["\u627f\u5fb7", "Chengde"], ["\u5eca\u574a", "Cangzhou"], ["\u5eca\u574a", "Langfang"], ["\u8861\u6c34", "Hengshui"], ["\u592a\u539f", "Taiyuan"], ["\u5927\u540c", "Datong"], ["\u9633\u6cc9", "Yangquan"], ["\u957f\u6cbb", "Changzhi"], ["\u4e34\u6c7e", "Linfen"], ["\u547c\u548c\u6d69\u7279", "Huhehaote"], ["\u5305\u5934", "Baotou"], ["\u8d64\u5cf0", "Chifeng"], ["\u6c88\u9633", "Shenyang"], ["\u5927\u8fde", "Dalian"], ["\u978d\u5c71", "Anshan"], ["\u629a\u987a", "Fushun"], ["\u672c\u6eaa", "Benxi"], ["\u9526\u5dde", "Jinzhou"], ["\u957f\u6625", "Changchun"], ["\u5409\u6797", "Jilin"], ["\u54c8\u5c14\u6ee8", "Haerbin"], ["\u9f50\u9f50\u54c8\u5c14", "Qiqihaer"], ["\u5927\u5e86", "Daqing"], ["\u7261\u4e39\u6c5f", "Mudanjiang"], ["\u5357\u4eac", "Nanjing"], ["\u65e0\u9521", "Wuxi"], ["\u5f90\u5dde", "Xuzhou"], ["\u5e38\u5dde", "Changzhou"], ["\u82cf\u5dde", "Suzhou"], ["\u5357\u901a", "Nantong"], ["\u8fde\u4e91\u6e2f", "Lianyungang"], ["\u626c\u5dde", "Yangzhou"], ["\u9547\u6c5f", "Zhenjiang"], ["\u6dee\u5b89", "Huaian"], ["\u76d0\u57ce", "Yancheng"], ["\u53f0\u5dde", "Taizhou"], ["\u5bbf\u8fc1", "Suqian"], ["\u676d\u5dde", "Hangzhou"], ["\u5b81\u6ce2", "Ningbo"], ["\u6e29\u5dde", "Wenzhou"], ["\u5609\u5174", "Jiaxing"], ["\u6e56\u5dde", "Huzhou"], ["\u7ecd\u5174", "Shaoxing"], ["\u91d1\u534e", "Jinhua"], ["\u8862\u5dde", "Quzhou"], ["\u821f\u5c71", "Zhoushan"], ["\u4e3d\u6c34", "Lishui"], ["\u5408\u80a5", "Hefei"], ["\u829c\u6e56", "Wuhu"], ["\u9a6c\u978d\u5c71", "Maanshan"], ["\u798f\u5dde", "Fuzhou"], ["\u53a6\u95e8", "Xiamen"], ["\u6cc9\u5dde", "Quanzhou"], ["\u5357\u660c", "Nanchang"], ["\u4e5d\u6c5f", "Jiujiang"], ["\u6d4e\u5357", "Jinan"], ["\u9752\u5c9b", "Qingdao"], ["\u6dc4\u535a", "Zibo"], ["\u67a3\u5e84", "Zaozhuang"], ["\u70df\u53f0", "Yantai"], ["\u6f4d\u574a", "Weifang"], ["\u6d4e\u5b81", "Jining"], ["\u6cf0\u5b89", "Taian"], ["\u5a01\u6d77", "Weihai"], ["\u65e5\u7167", "Rizhao"], ["\u4e1c\u8425", "Dongying"], ["\u83b1\u829c", "Laiwu"], ["\u4e34\u6c82", "Linyi"], ["\u5fb7\u5dde", "Dezhou"], ["\u804a\u57ce", "Liaocheng"], ["\u6ee8\u5dde", "Binzhou"], ["\u83cf\u6cfd", "Heze"], ["\u90d1\u5dde", "Zhengzhou"], ["\u5f00\u5c01", "Kaifeng"], ["\u6d1b\u9633", "Luoyang"], ["\u5e73\u9876\u5c71", "Pingdingshan"], ["\u5b89\u9633", "Anyang"], ["\u7126\u4f5c", "Jiaozuo"], ["\u4e09\u95e8\u5ce1", "Sanmenxia"], ["\u6b66\u6c49", "Wuhan"], ["\u5b9c\u660c", "Yichang"], ["\u8346\u5dde", "Jingzhou"], ["\u957f\u6c99", "Changsha"], ["\u682a\u6d32", "Zhuzhou"], ["\u6e58\u6f6d", "Xiangtan"], ["\u5cb3\u9633", "Yueyang"], ["\u5e38\u5fb7", "Changde"], ["\u5f20\u5bb6\u754c", "Zhangjiajie"], ["\u5e7f\u5dde", "Guangzhou"], ["\u97f6\u5173", "Shaoguan"], ["\u6df1\u5733", "Shenzhen"], ["\u73e0\u6d77", "Zhuhai"], ["\u6c55\u5934", "Shantou"], ["\u4f5b\u5c71", "Foshan"], ["\u6e5b\u6c5f", "Zhanjiang"], ["\u4e2d\u5c71", "Zhongshan"], ["\u6c5f\u95e8", "Jiangmen"], ["\u8087\u5e86", "Zhaoqing"], ["\u4e1c\u839e", "Dongguan"], ["\u60e0\u5dde", "Huizhou"], ["\u987a\u5fb7", "Shunde"], ["\u5357\u5b81", "Nanning"], ["\u67f3\u5dde", "Liuzhou"], ["\u6842\u6797", "Guilin"], ["\u5317\u6d77", "Beihai"], ["\u6d77\u53e3", "Haikou"], ["\u4e09\u4e9a", "Sanya"], ["\u6210\u90fd", "Chengdu"], ["\u81ea\u8d21", "Zigong"], ["\u6500\u679d\u82b1", "Panzhihua"], ["\u6cf8\u5dde", "Luzhou"], ["\u5fb7\u9633", "Deyang"], ["\u7ef5\u9633", "Mianyang"], ["\u5357\u5145", "Nanchong"], ["\u5b9c\u5bbe", "Yibin"], ["\u8d35\u9633", "Guiyang"], ["\u9075\u4e49", "Zunyi"], ["\u6606\u660e", "Kunming"], ["\u66f2\u9756", "Qujing"], ["\u7389\u6eaa", "Yuxi"], ["\u62c9\u8428", "Lhasa"], ["\u897f\u5b89", "Xian"], ["\u94dc\u5ddd", "Tongchuan"], ["\u5b9d\u9e21", "Baoji"], ["\u54b8\u9633", "Xianyang"], ["\u6e2d\u5357", "Weinan"], ["\u5ef6\u5b89", "Yanan"], ["\u5170\u5dde", "Lanzhou"], ["\u91d1\u660c", "Jinchang"], ["\u897f\u5b81", "Xining"], ["\u94f6\u5ddd", "Yinchuan"], ["\u77f3\u5634\u5c71", "Shizuishan"], ["\u4e4c\u9c81\u6728\u9f50", "Wulumuqi"], ["\u514b\u62c9\u739b\u4f9d", "Karamay"]]""")


kv = redis.Redis(REDIS_HOST)


def test(data, bot):
    message = data['message']
    if '空气' not in message:
        return False
    req = filter(lambda p: p[0].encode('utf-8') in message, city)
    return len(req) > 0


def get_desc(cityname, cityshort):
    r = kv.get('airpollution.%s' % (cityshort))
    if r:
        return r
    r = urllib2.urlopen('http://www.aqicn.info/?city=%s&lang=cn' % (cityshort), timeout=60)
    p = r.read()
    m = re.search('%s[^"]*的空气质量([^"]*)' % (cityname), p)
    m_aqiindex = re.search(r'整体空气质量指数为([0-9]*)', p)
    if m and m_aqiindex:
        text = m.group(0).replace('。', '，').replace('.', '') + '，整体AQI指数为：' + m_aqiindex.group(1)
        kv.setex('airpollution.%s' % (cityshort), text, 1800)
        return text
    else:
        raise Exception


def handle(data, bot):
    message = data['message']
    reqs = filter(lambda p: p[0].encode('utf-8') in message, city)
    s = []
    for i in reqs:
        try:
            s.append(get_desc(i[0].encode('utf-8'), i[1].encode('utf-8')))
        except:
            pass
    if s:
        return '，'.join(s) + '。'
    else:
        raise Exception

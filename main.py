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


# 主程序，轮询通知，处理通知

from renren import RenRen
from ntype import NTYPES
from multiprocessing import Pool
from urlparse import urlparse, parse_qsl
from redis import Redis
from pyquery import PyQuery
from rq import Queue
import requests
import time, re
from controller import bots, reply

# 匹配自己名字的正则
self_match_pattern = re.compile('<a.*@小黄鸡.*</a>')

# 消息队列
redis_conn = Redis()
q = Queue(connection=redis_conn)

# 解析一条通知的数据
def parseNotification(notification):
    dom = PyQuery(notification['content'])
    # 回复/@你的用户的首页，回复的资源的地址
    user_link, source_link = [a.get('href') for a in dom.find('a')]
    source_query = urlparse(source_link).query
    source_params = dict(parse_qsl(source_query))

    ntype, source_id = map(int, notification['source'].split('-'))

    return {
        'ntype': ntype,
        'source_id': source_id,
        'owner_id': source_params['id'],
        'doing_id': int(source_params['doingId']),
        'reply_id': int(source_params.get('repliedId', 0))
    }

def handle(bot, notification):
    data = parseNotification(notification)

    print time.strftime('%Y-%m-%d %I:%M:%S',time.localtime(time.time())), data
    ntype = data['ntype']

    if not ntype in NTYPES.values():
        return

    owner_id, doing_id = data['owner_id'], data['doing_id']

    payloads = {
      'owner_id': owner_id,
      'doing_id': doing_id
    }

    content = ''
    if ntype == NTYPES['at_in_status']:
        doing = bot.getDoingById(owner_id, doing_id)
        if doing:
            content = self_match_pattern.sub('', doing['content'].encode('utf-8'))
        else:
            return

    elif ntype == NTYPES['reply_in_status_comment']:
        reply_id = data['reply_id']
        comment = bot.getCommentById(owner_id, doing_id, reply_id)
        if comment:
            payloads.update({
                'author_id': comment['ownerId'],
                'author_name': comment['ubname'],
                'reply_id': reply_id
            })
            content = comment['replyContent']
            content_s = content.split(u'\uff1a', 1)
            if len(content_s) == 1:
                content_s = content.split(': ', 1)
            if len(content_s) == 1:
                content_s = content.split(':', 1)
            content = content_s[-1]
            print content
        else:
            return

    print ''
    # 进入消息队列
    q.enqueue(reply, payloads, content)

# 得到人人上的通知，处理之
def process(bot, just_clear=False):
    notifications = bot.getNotifications()

    for notification in notifications:
        bot.get(notification['rmessagecallback'])

        # 如果已经处理过了，拜拜
        if redis_conn.get(notification['nid']):
            print 'duplicate', notification
            return

        # 如果只是要清理通知，拜拜
        if just_clear:
            print 'clear', notification
            return

        try:
            handle(bot, notification)
            redis_conn.set(notification['nid'], True)
            redis_conn.incr('comment_count')
        except Exception, e:
            print e

        print ''

if __name__ == '__main__':
    while True:
        try:
            map(process, bots)
        except:
            pass

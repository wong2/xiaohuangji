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
from rq import Queue
import requests
import time
import re
import sys
from controller import bots, reply

# 消息队列
redis_conn = Redis()
q = Queue(connection=redis_conn)


def handle(bot, notification):
    print time.strftime('%Y-%m-%d %I:%M:%S', time.localtime(time.time())), 'got notification'
    if int(notification['type']) in NTYPES.values():
        # 进入消息队列
        q.enqueue(reply, notification)


# 得到人人上的通知，处理之
def process(bot, just_clear=False):
    notifications = bot.getNotifications()

    for notification in notifications:
        notify_id = notification['notify_id']

        bot.removeNotification(notify_id)

        # 如果已经处理过了, 或在执行清空消息脚本
        if redis_conn.get(notify_id) or just_clear:
            print 'clear' if just_clear else 'get duplicate notification', notification
            return

        try:
            redis_conn.set(notify_id, True)
            handle(bot, notification)
            redis_conn.incr('comment_count')
        except Exception, e:
            print e

        print ''


def main():
    while True:
        try:
            map(process, bots)
        except KeyboardInterrupt:
            sys.exit()
        except Exception, e:
            print e

if __name__ == '__main__':
    main()

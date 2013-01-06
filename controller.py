#-*-coding:utf-8-*-

"""
Copyright (c) 2012 wong2 <wonderfuly@gmail.com>
Copyright (c) 2012 Qijiang Fan <fqj1994@gmail.com>

Original Author:
    Wong2 <wonderfuly@gmail.com>
Changes Statement:
    Changes made by Qijiang Fan <fqj1994@gmail.com> on
    Jan 6 2013:
        Add keywordfilter bindings.

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


# 小黄鸡们

from renren import RenRen
from ai import magic
from filter_manager import questionfilter, answerfilter
import redis
try:
    from my_accounts import accounts
except:
    from accounts import accounts


def getBots(accounts):
    bots = []
    for account in accounts:
        bot = RenRen()
        bot.login(account[0], account[1])
        print bot.email, 'login'
        bots.append(bot)
    return bots

bots = getBots(accounts)

r = redis.Redis()


# 得到数据，找到答案，发送回复
def reply(data, message):
    # 不要自问自答
    if 'author_name' in data and '小黄鸡' in data['author_name'].encode('utf-8'):
        return

    data['message'] = answerfilter(magic(questionfilter(message)))

    current_bot_index = int(r.get('current_bot_index') or 0)
    bot = bots[current_bot_index]
    result = bot.addComment(data)

    # 如果连续8次遇到 code 1031，则认为被封了，换下一个账号
    if result['code'] == 1031:
        reach_limit_time, MAX_LIMIT_TRY = r.incr('reach_limit_time'), 8
        if int(reach_limit_time) == MAX_LIMIT_TRY:
            r.set('reach_limit_time', 0)
            current_bot_index = r.incr('current_bot_index')
            if int(current_bot_index) >= len(bots):
                r.set('current_bot_index', 0)
                raise Exception('SHIT!!!!!!ALL BOTS ARE DOWN!!!!!!!!!!')
            else:
                raise Exception('bot %s reach comment limit' % bot.email)
        else:
            print 'maybe comment limit', bot.email
    elif result['code'] == 0:
        r.set('reach_limit_time', 0)
    else:
        raise Exception('Error sending comment by bot %s' % bot.email)

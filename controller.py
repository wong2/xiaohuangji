#-*-coding:utf-8-*-

from renren import RenRen
from ai import magic
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
    if 'author_name' in data and  '小黄鸡' in data['author_name'].encode('utf-8'):
        return

    data['message'] = magic(message)

    current_bot_index = int(r.get('current_bot_index') or 0)
    bot = bots[current_bot_index]
    result = bot.addComment(data)

    # 如果连续5次遇到 code 1031，则认为被封了，换下一个账号
    if result['code'] == 1031:
        reach_limit_time, MAX_LIMIT_TRY = r.incr('reach_limit_time'), 5
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


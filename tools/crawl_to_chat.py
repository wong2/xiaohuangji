#-*-coding:utf-8-*-

# 主动聊天

import sys
sys.path.append('..')

import random
from redis import Redis
from renren import RenRen
from my_accounts import accounts
import time
from crawl_info_config import crawl_info_list

kv = Redis(host='localhost')
account = accounts[0]
bot = RenRen(account[0], account[1])

def handle(keyword, responses):
    statuses = bot.searchStatus(keyword, max_length=10)
    for status in statuses:
        user_id, status_id, status_time = status
        status_id_hash = int(str(status_id)[1:])
        if not kv.getbit('status_record', status_id_hash):
            print keyword, user_id, status_id, status_time
            bot.addComment({
                'type': 'status',
                'source_id': status_id,
                'owner_id': user_id,
                'message': random.choice(responses)
            })
            kv.setbit('status_record', status_id_hash, 1)

def main():
    for crawl_info in crawl_info_list:
        for keyword in crawl_info['keywords']:
            try:
                handle(keyword, crawl_info['responses'])
            except Exception, e:
                print e
                continue

if __name__ == '__main__':
    while True:
        print 'fetching...'
        main()
        time.sleep(30)

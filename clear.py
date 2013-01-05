from main import process
from controller import bots
import time

# 用来出错重启前，先清理出错时间段内的通知

while True:
    for bot in bots:
        process(bot, True)
    time.sleep(1)

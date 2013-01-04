from main import process
from controller import bots
import time

while True:
    for bot in bots:
        process(bot, True)
    time.sleep(1)

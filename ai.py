#-*-coding:utf-8-*-

import time
from simsimi import SimSimi

simi = SimSimi()

# some magic here
def magic(text):
    return simi.chat(text).encode('utf-8')

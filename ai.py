#-*-coding:utf-8-*-

# 小黄鸡的ai，先自己尝试处理，没结果则交给simsimi

import time
from simsimi import SimSimi

simi = SimSimi()

def my_logic(text):
    # 教学模式: /Q python和ruby哪个好？ /A php最好！
    if '/Q' in text and '/A' in text:
        _, right_part  = text.split('/Q', 1) 
        question, answer = [s.strip() for s in right_part.split('/A', 1)]
        if question and answer:
            simi.teach(question, answer)
            return '学会啦'

    return None

# some magic here
def magic(text):
    text = text.strip()
    return simi.chat(text).encode('utf-8')

if __name__ == '__main__':
    print magic('/Q 今天天气怎么样？ /A 大雪')

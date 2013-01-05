#-*-coding:utf-8-*-

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

    # 先自己试着处理，否则给simsimi
    try:
        my_result = my_logic(text)
    except:
        my_result = None

    if my_result:
        return my_result
    else:
        return simi.chat(text).encode('utf-8')

if __name__ == '__main__':
    print magic('/Q 今天天气怎么样？ /A 大雪')

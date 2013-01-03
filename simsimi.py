#-*-coding:utf-8-*-

import requests
import cookielib

class SimSimi:

    def __init__(self):
        self.session = requests.Session()
        self.session.get('http://www.simsimi.com/talk.htm')

        self.headers = {
            'Referer':'http://www.simsimi.com/talk.htm' 
        }
        self.url = 'http://www.simsimi.com/func/req?lc=ch&msg=%s'

    def chat(self, message=''):
        if message.strip():
            r = self.session.get(self.url % message.strip(), headers=self.headers)
            try:
                return r.json()['response']
            except:
                return u'呵呵'
        else:
            return u'叫我干嘛'

if __name__ == '__main__':
    simi = SimSimi()
    print simi.chat('最后一个问题')


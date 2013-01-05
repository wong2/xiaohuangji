#-*-coding:utf-8-*-

# 从simsimi读数据

import requests
import cookielib

class SimSimi:

    def __init__(self):
        r = requests.get('http://www.simsimi.com/talk.htm')
        self.chat_cookies = r.cookies

        r = requests.get('http://www.simsimi.com/teach.htm')
        self.teach_cookies = r.cookies

        self.headers = {
            'Referer': 'http://www.simsimi.com/talk.htm'
        }

        self.chat_url = 'http://www.simsimi.com/func/req?lc=ch&msg=%s'
        self.teach_url = 'http://www.simsimi.com/func/teach'

    def chat(self, message=''):
        if message:
            r = requests.get(self.chat_url % message, cookies=self.chat_cookies, headers=self.headers)
            self.chat_cookies = r.cookies
            try:
                return r.json()['response']
            except:
                return u'呵呵'
        else:
            return u'叫我干嘛'

    def teach(self, req, resp):
        data = {
            'req': req,
            'resp': resp,
            'lc': 'ch',
            'snsinfo': '{"sid":"1432328384", "stype":"facebook", "sname":"王大鹏", "stoken":"AAAFRQIFUlkgBAPKP1DkWkDRuhGDpO2mZCbgq38t90ZC9U1VlstKQEH0OUt8sWUzdGBFWoGz4Wegbm0ZA4LyjaBQ6p0OIrZCg1nnp0JiiqPgjVWNwoGoh", "sshare":"off"}'
        }
        r = requests.post(self.teach_url, data, cookies=self.teach_cookies, headers=self.headers)
        print r.text


if __name__ == '__main__':
    simi = SimSimi()
    print simi.chat('最后一个问题')
    #simi.teach('一切的答案', '42')

#-*-coding:utf-8-*-

"""
Copyright (c) 2012 wong2 <wonderfuly@gmail.com>

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


# 从simsimi读数据

import requests
import cookielib
import MySQLdb
import socket
from settings import MYSQL_HOST, MYSQL_USER, MYSQL_PASS, MYSQL_DBNAME
try:
    from settings import SIMSIMI_KEY
except:
    SIMSIMI_KEY = ''

mysqldb = MySQLdb.connect(host=MYSQL_HOST, port=3306, user=MYSQL_USER, passwd=MYSQL_PASS, db=MYSQL_DBNAME, charset='utf8', use_unicode=False)
cursor = mysqldb.cursor()
try:
    workerhostname = socket.gethostname()
except:
    workerhostname = 'unknown'


class SimSimi:

    def __init__(self):

        self.headers = {
            'Referer': 'http://www.simsimi.com/talk.htm'
        }

        self.chat_url = 'http://www.simsimi.com/func/req?lc=ch&msg=%s'
        self.api_url = 'http://api.simsimi.com/request.p?key=%s&lc=ch&ft=1.0&text=%s'

        if not SIMSIMI_KEY:
            self.initSimSimiCookie()

    def initSimSimiCookie(self):
        r = requests.get('http://www.simsimi.com/talk.htm')
        self.chat_cookies = r.cookies

    def getSimSimiResult(self, message, method='normal'):
        if method == 'normal':
            r = requests.get(self.chat_url % message, cookies=self.chat_cookies, headers=self.headers)
            self.chat_cookies = r.cookies
        else:
            url = self.api_url % (SIMSIMI_KEY, message) 
            r = requests.get(url)
        return r

    def chat(self, message=''):
        if message:
            r = self.getSimSimiResult(message, 'normal' if not SIMSIMI_KEY else 'api')
            try:
                answer = r.json()['response']
                sql = "INSERT INTO question_and_answers (question, answer, worker) VALUES(%s, %s, %s)"
                try:
                    cursor.execute(sql, (message, answer, workerhostname))
                except Exception as e:
                    print e
                return answer
            except:
                return u'呵呵'
        else:
            return u'叫我干嘛'

if __name__ == '__main__':
    simi = SimSimi()
    print simi.chat('最后一个问题')

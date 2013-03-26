#-*-coding:utf-8-*-

"""
Copyright (c) 2012 wong2 <wonderfuly@gmail.com>
Copyright (c) 2012 hupili <hpl1989@gmail.com>

Original Author:
    Wong2 <wonderfuly@gmail.com>
Changes Statement:
    Changes made by Pili Hu <hpl1989@gmail.com> on
    Jan 10 2013:
        Support captcha.

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


# 人人各种接口

import requests
import json
import re
import random
from pyquery import PyQuery
from encrypt import encryptString
import os


class RenRen:

    def __init__(self, email=None, pwd=None):
        self.session = requests.Session()
        self.token = {}

        if email and pwd:
            self.login(email, pwd)

    def _loginByCookie(self, cookie_str):
        cookie_dict = dict([v.split('=', 1) for v in cookie_str.strip().split(';')])
        self.session.cookies = requests.utils.cookiejar_from_dict(cookie_dict)

        self.getToken()

    def loginByCookie(self, cookie_path):
        with open(cookie_path) as fp:
            cookie_str = fp.read()

        self._loginByCookie(cookie_str)

    def saveCookie(self, cookie_path):
        with open(cookie_path, 'w') as fp:
            cookie_dict = requests.utils.dict_from_cookiejar(self.session.cookies)
            cookie_str = '; '.join([k + '=' + v for k, v in cookie_dict.iteritems()])
            fp.write(cookie_str)

    def login(self, email, pwd):
        key = self.getEncryptKey()

        if self.getShowCaptcha(email) == 1:
            fn = 'icode.%s.jpg' % os.getpid()
            self.getICode(fn)
            print "Please input the code in file '%s':" % fn
            icode = raw_input().strip()
            os.remove(fn)
        else:
            icode = ''

        data = {
            'email': email,
            'origURL': 'http://www.renren.com/home',
            'icode': icode,
            'domain': 'renren.com',
            'key_id': 1,
            'captcha_type': 'web_login',
            'password': encryptString(key['e'], key['n'], pwd) if key['isEncrypt'] else pwd,
            'rkey': key['rkey']
        }
        print "login data: %s" % data
        url = 'http://www.renren.com/ajaxLogin/login?1=1&uniqueTimestamp=%f' % random.random()
        r = self.post(url, data)
        result = r.json()
        if result['code']:
            print 'login successfully'
            self.email = email
            r = self.get(result['homeUrl'])
            self.getToken(r.text)
        else:
            print 'login error', r.text

    def getICode(self, fn):
        r = self.get("http://icode.renren.com/getcode.do?t=web_login&rnd=%s" % random.random())
        if r.status_code == 200 and r.raw.headers['content-type'] == 'image/jpeg':
            with open(fn, 'wb') as f:
                for chunk in r.iter_content():
                    f.write(chunk)
        else:
            print "get icode failure"

    def getShowCaptcha(self, email=None):
        r = self.post('http://www.renren.com/ajax/ShowCaptcha', data={'email': email})
        return r.json()

    def getEncryptKey(self):
        r = requests.get('http://login.renren.com/ajax/getEncryptKey')
        return r.json()

    def getToken(self, html=''):
        p = re.compile("get_check:'(.*)',get_check_x:'(.*)',env")

        if not html:
            r = self.get('http://www.renren.com')
            html = r.text

        result = p.search(html)
        self.token = {
            'requestToken': result.group(1),
            '_rtk': result.group(2)
        }

    def request(self, url, method, data={}):
        if data:
            data.update(self.token)

        if method == 'get':
            return self.session.get(url, data=data)
        elif method == 'post':
            return self.session.post(url, data=data)

    def get(self, url, data={}):
        return self.request(url, 'get', data)

    def post(self, url, data={}):
        return self.request(url, 'post', data)

    def getUserInfo(self):
        r = self.get('http://notify.renren.com/wpi/getonlinecount.do')
        return r.json()

    def getNotifications(self):
        url = 'http://notify.renren.com/rmessage/get?getbybigtype=1&bigtype=1&limit=50&begin=0&view=17'
        r = self.get(url)
        try:
            result = json.loads(r.text, strict=False)
        except Exception, e:
            print 'error', e
            result = []
        return result

    def removeNotification(self, notify_id):
        self.get('http://notify.renren.com/rmessage/remove?nl=' + str(notify_id))

    def getDoings(self, uid, page=0):
        url = 'http://status.renren.com/GetSomeomeDoingList.do?userId=%s&curpage=%d' % (str(uid), page)
        r = self.get(url)
        return r.json().get('doingArray', [])

    def getDoingById(self, owner_id, doing_id):
        doings = self.getDoings(owner_id)
        doing = filter(lambda doing: doing['id'] == doing_id, doings)
        return doing[0] if doing else None

    def getDoingComments(self, owner_id, doing_id):
        url = 'http://status.renren.com/feedcommentretrieve.do'
        r = self.post(url, {
            'doingId': doing_id,
            'source': doing_id,
            'owner': owner_id,
            't': 3
        })

        return r.json()['replyList']

    def getCommentById(self, owner_id, doing_id, comment_id):
        comments = self.getDoingComments(owner_id, doing_id)
        comment = filter(lambda comment: comment['id'] == int(comment_id), comments)
        return comment[0] if comment else None

    def addComment(self, data):
        return {
            'status': self.addStatusComment,
            'album' : self.addAlbumComment,
            'photo' : self.addPhotoComment,
            'blog'  : self.addBlogComment,
            'share' : self.addShareComment,
            'gossip': self.addGossip
        }[data['type']](data)

    def sendComment(self, url, payloads):
        r = self.post(url, payloads)
        r.raise_for_status()
        try:
            return r.json()
        except:
            return { 'code': 0 }

    # 评论状态
    def addStatusComment(self, data):
        url = 'http://status.renren.com/feedcommentreply.do'

        payloads = {
            't': 3,
            'rpLayer': 0,
            'source': data['source_id'],
            'owner': data['owner_id'],
            'c': data['message']
        }

        if data.get('reply_id', None):
            payloads.update({
                'rpLayer': 1,
                'replyTo': data['author_id'],
                'replyName': data['author_name'],
                'secondaryReplyId': data['reply_id'],
                'c': '回复%s：%s' % (data['author_name'].encode('utf-8'), data['message'])
            })

        return self.sendComment(url, payloads)

    # 回复留言
    def addGossip(self, data):
        url = 'http://gossip.renren.com/gossip.do'
        
        payloads = {
            'id': data['owner_id'], 
            'only_to_me': 1,
            'mode': 'conversation',
            'cc': data['author_id'],
            'body': data['message'],
            'ref':'http://gossip.renren.com/getgossiplist.do'
        }

        return self.sendComment(url, payloads)

    # 回复分享
    def addShareComment(self, data):
        url = 'http://share.renren.com/share/addComment.do'

        if data.get('reply_id', None):
            body = '回复%s：%s' % (data['author_name'].encode('utf-8'), data['message']),
        else:
            body = data['message']
        
        payloads = {
            'comment': body,
            'shareId' : data['source_id'],
            'shareOwner': data['owner_id'],
            'replyToCommentId': data.get('reply_id', 0),
            'repetNo' : data.get('author_id', 0)
        }

        return self.sendComment(url, payloads)

    # 回复日志
    def addBlogComment(self, data):
        url = 'http://blog.renren.com/PostComment.do'
        
        payloads = {
            'body': '回复%s：%s' % (data['author_name'].encode('utf-8'), data['message']),
            'feedComment': 'true',
            'guestName': '小黄鸡', 
            'id' : data['source_id'],
            'only_to_me': 0,
            'owner': data['owner_id'],
            'replyCommentId': data['reply_id'],
            'to': data['author_id']
        }

        return self.sendComment(url, payloads)

    # 回复相册
    def addAlbumComment(self, data):
        url = 'http://photo.renren.com/photo/%d/album-%d/comment' % (data['owner_id'], data['source_id'])
        
        payloads = {
            'id': data['source_id'],
            'only_to_me' : 'false',
            'body': '回复%s：%s' % (data['author_name'].encode('utf-8'), data['message']),
            'feedComment' : 'true', 
            'owner' : data['owner_id'],
            'replyCommentId' : data['reply_id'],
            'to' : data['author_id']
        }

        return self.sendComment(url, payloads)

    def addPhotoComment(self, data):
        url = 'http://photo.renren.com/photo/%d/photo-%d/comment' % (data['owner_id'], data['source_id'])

        if 'author_name' in data:
            body = '回复%s：%s' % (data['author_name'].encode('utf-8'), data['message']),
        else:
            body = data['message']
        
        payloads = {
            'guestName': '小黄鸡',
            'feedComment' : 'true',
            'body': body,
            'owner' : data['owner_id'],
            'realWhisper':'false',
            'replyCommentId' : data.get('reply_id', 0),
            'to' : data.get('author_id', 0)
        }

        return self.sendComment(url, payloads)

    # 访问某人页面
    def visit(self, uid):
        self.get('http://www.renren.com/' + str(uid) + '/profile')

    # 根据关键词搜索最新状态(全站)
    def searchStatus(self, keyword, max_length=20):
        url = 'http://browse.renren.com/s/status?offset=0&sort=1&range=0&q=%s&l=%d' % (keyword, max_length)
        r = self.session.get(url, timeout=5)
        status_elements = PyQuery(r.text)('.list_status .status_content')
        id_pattern  = re.compile("forwardDoing\('(\d+)','(\d+)'\)")
        results = []
        for index, _ in enumerate(status_elements):
            status_element = status_elements.eq(index)

            # 跳过转发的
            if status_element('.status_root_msg'):
                continue

            status_element = status_element('.status_content_footer')
            status_time = status_element('span').text()
            m = id_pattern.search(status_element('.share_status').attr('onclick'))
            status_id, user_id = m.groups()
            results.append( (int(user_id), int(status_id), status_time) )
        return results

if __name__ == '__main__':
    renren = RenRen()
    renren.login('email', 'password')
    info = renren.getUserInfo()
    print 'hello', info['hostname']
    print renren.searchStatus('么么哒')

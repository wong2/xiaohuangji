#coding = utf8

"""
Copyright (c) 2012 yangzhe1991 <ud1937@gmail.com>

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

import urllib2
import urllib


def remove(s):
    ans = ''
    while True:
        i = s.find('<')
        if i < 0:
            ans += s
            return ans
        ans += s[:i]
        s = s[i+1:]
        s = s[s.find('>')+1:]


def wikipedia(title):
    try:
        url = 'http://zh.wikipedia.org/w/index.php?%s' % urllib.urlencode({'title': title, 'printable': 'yes', 'variant': 'zh-cn'})
        req = urllib2.Request(url, headers={'User-Agent': "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_2; en-US) AppleWebKit/533.3 (KHTML, like Gecko) Chrome/5.0.354.0 Safari/533.3"})
        wp = urllib2.urlopen(req, timeout=10)
        html = wp.read()
        #防止404，实际上似乎py会直接在urlopen的时候发现404并抛异常
        if html.find('维基百科目前还没有与上述标题相同的条目') >= 0:
            raise Exception
        i = html.find('mw-content-text')
        if i < 0:
            raise Exception
        html = html[i:]
        html = html[html.find('<p>')+3:html.find('</p>')]
        return remove(html)
    except:
        return None
if __name__ == '__main__':
    print wikipedia('三国')
    print wikipedia('ibm')
    print wikipedia('IBM')

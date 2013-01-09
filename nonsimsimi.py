#-*-coding:utf-8-*-

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

from wikipedia import wikipedia


#关键字过滤，首项为keyword，第二项为对应的函数，依次过滤，直到找到匹配,如添加其他功能也可在此修改
#函数的第一个参数为message全文，第二个参数为所触发的keyword
keywords=[
        ('是什么', wikipedia), 
        ('是谁', wikipedia), 
        ]
    

def filter(message):
    if not message:
        return None
    for pair in keywords:
        if message.find(pair[0]) >= 0:
            return pair[1](message,pair[0])
    return None


if __name__ == '__main__':
    print filter('三国是什么')
    print filter('节操是什么')
    print filter('刘邦是谁')
    print filter('节操是谁')
            


#-*-coding:utf-8-*-

"""
Copyright (c) 2012 Qijiang Fan <fqj1994@gmail.com>

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


import re


# 过滤器基类
class Filter:
    def filter(self, sent):
        pass


# 修改过滤器
class ModificationFilter(Filter):
    def filter(self, sent):
        return sent


# 正则表达式修改过滤器
class RegexModificationFilter(ModificationFilter):
    def __init__(self, search, replacement):
        self.search = search
        self.replacement = replacement

    def filter(self, sent):
        return re.sub(self.search, self.replacement, sent)


# 问题屏蔽器基类
class BlockFilter(Filter):
    def __init__(self, default_text='呵呵'):
        self.default_text = default_text

    def block(self, sent):
        return False

    def filter(self, sent):
        if self.block(sent):
            return self.default_text
        else:
            return sent


# 正则表达式过滤屏蔽器
class RegexBlockFilter(BlockFilter):
    def __init__(self, reg, default_text='呵呵'):
        self.reg = reg
        BlockFilter.__init__(self, default_text)

    def block(self, sent):
        if re.match(self.reg, sent):
            return True
        else:
            return False

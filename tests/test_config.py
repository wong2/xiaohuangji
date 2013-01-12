#-*-coding:utf-8-*-

"""
Copyright (c) 2012 wgx731 <wgx731@gmail.com>

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

""" Nose test config file

    config sys path for testing
"""

import os
import glob
import sys


TEST_DIR = os.path.abspath(os.path.dirname(__file__))
MAIN_CODE_DIR = os.path.abspath(os.path.join(TEST_DIR, os.path.pardir))
PLUGINS_CODE_DIR = os.path.abspath(os.path.join(MAIN_CODE_DIR, "plugins"))

# Result refers to result returned by plugin
WRONG_KEY_WORD_ERROR = "Missing or wrong keyword should not have result."
WRONG_RESULT_ERROR = "Correct keyword should have result."
WRONG_RESULT_FORMAT_ERROR = "Result should have correct format."


class TestBase(object):

    @classmethod
    def clean_up(klass, path, wildcard):
        os.chdir(path)
        for rm_file in glob.glob(wildcard):
            os.unlink(rm_file)

    @classmethod
    def setup_class(klass):
        sys.stderr.write("\nRunning %s\n" % klass)

    @classmethod
    def teardown_class(klass):
        klass.clean_up(TEST_DIR, "*.py?")
        klass.clean_up(PLUGINS_CODE_DIR, "*.py?")
        klass.clean_up(MAIN_CODE_DIR, "*.py?")

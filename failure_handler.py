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


import time
import sys
try:
    from settings import REDIS_HOST
except:
    REDIS_HOST = 'localhost'
try:
    from settings import REST_THRESHOLD
except:
    REST_THRESHOLD = 10
from rq import Worker
import redis

r = redis.Redis(host=REDIS_HOST)

failure_times = last_error_time = continuous_failure_times = 0


# 失败计数器
def job_failure_counter(prefix):
    global failure_times, last_error_time, continuous_failure_times
    n_failure_times = '.'.join([prefix, 'failure_times'])
    n_last_error_time = '.'.join([prefix, 'last_error_time'])
    n_continuous_failure_times = '.'.join([prefix, 'continuous_failure_times'])
    failure_times = int(r.get(n_failure_times) or 0)
    last_error_time = float(r.get(n_last_error_time) or 0)
    continuous_failure_times = int(r.get(n_continuous_failure_times) or 0)
    failure_times += 1
    r.incr(n_failure_times)
    if n_continuous_failure_times >= REST_THRESHOLD or time.time() - last_error_time <= 5:  # 将5s内的两次失败计作连续的失败
        continuous_failure_times += 1
        r.incr(n_continuous_failure_times)
    else:
        continuous_failure_times = 1
        r.set(n_continuous_failure_times, 1)
    last_error_time = time.time()
    r.set(n_last_error_time, last_error_time)
    failure_times = int(r.get(n_failure_times) or 0)
    continuous_failure_times = int(r.get(n_continuous_failure_times) or 0)


# 重置连续错误
def reset_failure(prefix):
    r.set('.'.join([prefix, 'continuous_failure_times']), 0)


# 得到 worker
def get_worker(traceback):
    p = traceback
    while p:
        l = p.tb_frame
        if 'self' in l.f_locals and isinstance(l.f_locals['self'], Worker):
            return l.f_locals['self']
        p = p.tb_next
    return None


# 额外的错误处理
def do_job_failure_handler_have_a_rest(job, exc_type, exc_val, traceback):
    worker = get_worker(traceback)
    if not worker:
        return True
    prefix = '.'.join(worker.name.split('.')[:-1])
    if 'simsimi.com' in str(exc_val):
        print 'count'
        job_failure_counter(prefix)
    if continuous_failure_times >= REST_THRESHOLD:
        print '%d continuous failed jobs. Sleep 60 seconds.' % (REST_THRESHOLD)
        time.sleep(60)
        reset_failure(prefix)
    return True

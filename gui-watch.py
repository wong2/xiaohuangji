#!/usr/bin/env python
#-*-coding:utf-8-*-
#import redis
import MySQLdb
import requests
import sys
import time
import datetime

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from collections import *
from threading import Thread
from Queue import Queue

from settings import *

q = Queue()


class SThread(Thread):
    def __init__(self, func, args):
        self.func = func
        self.args = args
        Thread.__init__(self)
        self.daemon = True

    def run(self):
        self.func(*self.args)


def run_thread(fun, args):
    SThread(fun, args).start()


def update_stat(qlabel):
    while True:
        try:
            m = MySQLdb.connect(host=MYSQL_HOST, port=3306, user=MYSQL_USER, passwd=MYSQL_PASS,
                    db=MYSQL_DBNAME, charset="utf8", use_unicode=False, connect_timeout=5).cursor()
            m.execute("SELECT count(*) FROM `question_and_answers`")
            total = m.fetchone()[0]
            m.execute("SELECT MAX(`time`) FROM `question_and_answers`")
            maxtime = m.fetchone()[0]
            m.execute("SELECT count(*) FROM `question_and_answers` WHERE `time` = %s", (maxtime - datetime.timedelta(0, 1)))
            lastsec = m.fetchone()[0]
            m.execute("SELECT count(*) FROM `question_and_answers` WHERE `time` >= %s AND `time` < %s",
                    (maxtime - datetime.timedelta(0, 3600), maxtime))
            lasthour = m.fetchone()[0]
            m.execute("SELECT count(*) FROM `question_and_answers` WHERE `time` >= %s AND `time` < %s",
                    (maxtime - datetime.timedelta(0, 60), maxtime))
            lastmin = m.fetchone()[0]
            m.execute("SELECT count(*) FROM `question_and_answers` WHERE `time` >= %s AND `time` < %s",
                    (maxtime - datetime.timedelta(0, 3600 * 24), maxtime))
            lastday = m.fetchone()[0]

            q.put((qlabel, u'<center>统计数据</center>' + '<br/>'.join([
                u'最近更新：%s' % (maxtime - datetime.timedelta(0, 1)),
                u'总计：%d次' % total,
                u'最近一天：%d次' % lastday,
                u'最近一小时：%d次' % lasthour,
                u'最近一分钟：%d次' % lastmin,
                u'最近一秒：%d次' % lastsec,
                ])))
        finally:
            time.sleep(2)


def update_queues(qlabel):
    while True:
        try:
            r = requests.get('http://' + REDIS_HOST + ':9181/queues.json', timeout=5)
            j = r.json()
            s = u'<center>队列监控</center><br/>'
            if j[u'queues']:
                s += '<br/>'.join([
                    u'%s: %d' % (i[u'name'], i[u'count']) for i in j[u'queues']
                    ])
            else:
                s += u'所有队列为空'
            q.put((qlabel, s))
        finally:
            time.sleep(2)


def update_workers(qlabel):
    while True:
        try:
            r = requests.get('http://' + REDIS_HOST + ':9181/workers.json', timeout=5)
            j = r.json()
            workers = {}
            for i in j[u'workers']:
                name = '.'.join(i[u'name'].split('.')[:-1])
                if not name in workers:
                    workers[name] = defaultdict(int)
                workers[name][i[u'state']] += 1
            st = u'<center>Workers 状态</center><br/>' + u'<br/>'.join([
                worker + u'：   ' + u'   '.join([
                    u'%d %s(s)' % (workers[worker][state], state) for state in workers[worker]
                    ])
                for worker in workers])
            q.put((qlabel, st))
        finally:
            time.sleep(2)


def update_realtime(qlabel):
    while True:
        try:
            m = MySQLdb.connect(host=MYSQL_HOST, port=3306, user=MYSQL_USER, passwd=MYSQL_PASS,
                    db=MYSQL_DBNAME, charset="utf8", use_unicode=False, connect_timeout=5).cursor()
            m.execute("SELECT * FROM question_and_answers ORDER BY `id` DESC LIMIT 0, 3")
            l = m.fetchall()
            s = u'<center>最近三条问答</center><br/>' + '<br/>'.join([
                ("Q: %s<br/>A: %s<br/>Worker: %s<br/>Time: %s<br/>" % (t[1], t[2], t[3], t[4])).decode('UTF-8')
                for t in l])
            q.put((qlabel, s))
        finally:
            time.sleep(2)


def op(w):
    try:
        l = q.get_nowait()
        while l:
            l[0].setText(l[1])
            l = q.get_nowait()
    except:
        pass


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, windowTitle=u'小黄鸡监控')
        self.setCentralWidget(MainWidget())


class MainWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self, windowTitle=u'小黄鸡监控')
        self.stat_data = QLabel("", parent=self)
        self.queues = QLabel("", parent=self)
        self.workers = QLabel("", parent=self)
        self.realtime = QLabel("", parent=self)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.stat_data)
        self.layout().addWidget(self.queues)
        self.layout().addWidget(self.workers)
        self.layout().addWidget(self.realtime)

        run_thread(update_stat, [self.stat_data])
        run_thread(update_queues, [self.queues])
        run_thread(update_workers, [self.workers])
        run_thread(update_realtime, [self.realtime])

        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: op(self))
        self.timer.start(100)


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())

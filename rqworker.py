#!/usr/bin/env python
import sys
from rq import Queue, Connection, Worker

# Preload libraries
from controller import bots, r

# Provide queue names to listen to as arguments to this script,
# similar to rqworker
with Connection():
    qs = map(Queue, sys.argv[1:]) or [Queue()]

    w = Worker(qs)
    w.work()

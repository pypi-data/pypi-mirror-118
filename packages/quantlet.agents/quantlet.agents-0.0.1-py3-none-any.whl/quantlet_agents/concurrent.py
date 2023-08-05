#
#     QuantLET-agents - Synchronous and asynchronous agents for discrete-event simulation.
#          This is related to the distribution and simulation facets defined as part of
#          the financial language SIGMA.
#
#     Copyright (C) 2006 Jorge M. Faleiro Jr.
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as published
#     by the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.
#
#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import print_function

import logging
import multiprocessing as mp
import time
from threading import Thread, current_thread

from quantlet_streaming.stream import QLet

_manager = mp.Manager()
_endpoints = {}

EOS = '<end-of-stream>'
LOG = logging.getLogger(__name__)


def endpoint(url):
    """
    define an endpoint for url
    """
    if url not in _endpoints:
        _endpoints[url] = _manager.Queue()
    return _endpoints[url]


@QLet
def send(iter, endpoint):
    """
    send point to point
    """
    for i in iter:
        endpoint.put(i, block=False)
    endpoint.put(EOS, block=False)


def recv(endpoint, until=lambda x: x == EOS, timeout=None):
    """
    receive from endpoint until condition is true
    """
    while True:
        i = endpoint.get(block=True, timeout=timeout)
        if until(i):
            break
        yield i


class MultiProcessingPubSub(object):
    def __init__(self):
        self.manager = mp.Manager()
        self.queues = self.manager.dict()

    def publish(self, topic, payload):
        if topic in self.queues:
            for q in self.queues:
                q.put(payload)

    def subscribe(self, topic, f):
        if topic not in self.queues:
            self.queues[topic] = []

        def send(queue):
            while True:
                payload = queue.get(block=True)
                f(payload)

        queue = mp.Queue()
        self.queues[topic].append(queue)
        p = mp.Process(target=send, args=(queue,))
        p.start()


def dispatch(function):
    process = mp.Process(target=function)
    LOG.info("dispatching %s" % process.name)
    process.start()
    return process


def thread_dispatch(function):
    thread = Thread(target=function)
    print("dispatching %s" % thread.name)
    thread.daemon = True
    thread.start()
    return thread


def wait(timeout):
    print("sleeping %s for %ds" % (current_thread().name, timeout))
    time.sleep(timeout)
    print("resuming %s" % current_thread().name)


def parallel(f):
    def wrapper(*args, **kvargs):
        p = mp.Process(target=f, args=args, kwargs=kvargs)
        p.start()
        p.join()
        p.terminate()

    return wrapper

'''
Decorators for simple threadify/processify functions.

@Threadify(threads=10) or @Processify(processes=10)
def function(iterable, *args, **kwargs):
    return iterable (return value)

Decorated function returns list of values or 
concatenated iterables.
'''

import os
from threading import Thread
from multiprocessing import Process, Manager
from functools import wraps
from collections.abc import Iterable
import time


class MyThread(Thread):

    def __init__(self, func, res, iterable, *args, **kwargs):
        Thread.__init__(self)
        self.func = func
        self.res = res
        self.iterable = iterable
        self.args = args
        self.kwargs = kwargs

    def run(self):
        ans = self.func(self.iterable, *self.args, **self.kwargs)
        if ans:
            self.res += list(ans) if not isinstance(ans, str) and \
                        not isinstance(ans, bytes) and \
                        isinstance(ans, Iterable) else [ans]


class Threadify:

    def __init__(self, threads=1):
        self.threads = threads
        self.thrds = []
        self.res = []

    def __call__(self, func, *args, **kwargs):
        @wraps(func)
        def threadified(*args, **kwargs):
            iterable = list(args[0])
            for i in [iterable[i::self.threads] for i in range(self.threads)]:
                t = MyThread(func, self.res, i, *args[1:], **kwargs)
                t.setDaemon(True)
                self.thrds.append(t)
                t.start()
            for t in self.thrds:
                t.join()
            return self.res
        return threadified


class MyProcess(Process):

    def __init__(self, func, res, iterable, *args, **kwargs):
        Process.__init__(self)
        self.func = func
        self.res = res
        self.iterable = iterable
        self.args = args
        self.kwargs = kwargs

    def run(self):
        ans = self.func(self.iterable, *self.args, **self.kwargs)
        if ans:
            self.res += list(ans) if not isinstance(ans, str) and \
                        not isinstance(ans, bytes) and \
                        isinstance(ans, Iterable) else [ans]


class Processify:

    def __init__(self, processes=1):
        self.processes = processes
        self.procs = []
        self.manager = Manager()
        self.res = self.manager.list()

    def __call__(self, func, *args, **kwargs):
        @wraps(func)
        def processified(*args, **kwargs):
            iterable = list(args[0])
            for i in [iterable[i::self.processes] for i in range(self.processes)]:
                p = MyProcess(func, self.res, i, *args[1:], **kwargs)
                p.deamon = True
                self.procs.append(p)
                p.start()
            for p in self.procs:
                p.join()
            return self.res
        return processified

'''
Examples
'''


import urllib.request

@Threadify(threads=10)
def downloader(iterable):
    for url in iterable:
        handle = urllib.request.urlopen(url)
        fname = os.path.basename(url)
        with open(fname, "wb") as f_handler:
            while True:
                chunk = handle.read(1024)
                if not chunk:
                    break
                f_handler.write(chunk)
    return 1

@Processify(processes=10)
def simples(iterable, end='1'):
    return [i for i in iterable 
            if all(i%j!=0 for j in range(2, int(i**.5)+1)) and 
            str(i).endswith(end)]


def main():
    urls = ['http://www.irs.gov/pub/irs-pdf/f1040.pdf',
            'http://www.irs.gov/pub/irs-pdf/f1040a.pdf',
            'http://www.irs.gov/pub/irs-pdf/f1040ez.pdf',
            'http://www.irs.gov/pub/irs-pdf/f1040es.pdf',
            'http://www.irs.gov/pub/irs-pdf/f1040sb.pdf']
    start_time = time.perf_counter()
    return_codes = downloader(urls)
    td = time.perf_counter() - start_time
    print(return_codes, td)

    start_time = time.perf_counter()
    simple_nums = simples(range(10000000), end='6421')
    td = time.perf_counter() - start_time
    print(simple_nums , td)

if __name__ == '__main__':
    main()



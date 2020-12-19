import time
import os
from threading import Thread, Event
import ctypes


frame1 = \
"""
  .---------.
  |.-------.|
  ||>run#  ||
  ||       ||
  |"-------'|etf
.-^---------^-.
| ---~   AMiGA|
"-------------'
"""

frame2 = \
"""
  .---------.
  |.-------.|
  ||>hello#||
  ||       ||
  |"-------'|etf
.-^---------^-.
| ---~   AMiGA|
"-------------'
"""

frame3 = \
"""
  .---------.
  |.-------.|
  ||>world#||
  ||       ||
  |"-------'|etf
.-^---------^-.
| ---~   AMiGA|
"-------------'
"""


def animate(frames):
    while True:
        for f in frames:
            clear_console = 'clear' if os.name == 'posix' else 'CLS'
            os.system(clear_console)
            print(globals()[f])
            time.sleep(.5)

def terminate_thread(thread):
    """Terminates a python thread from another thread.

    :param thread: a threading.Thread instance
    """
    if not thread.is_alive():
        return

    exc = ctypes.py_object(SystemExit)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(thread.ident), exc)
    if res == 0:
        raise ValueError("nonexistent thread id")
    elif res > 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


frames = sorted(i for i in locals() if i.startswith('frame'))

t = Thread(target=animate, args=(frames,))
t.start()

# Do some work
res = 0
for i in range(10):
    res += i
    time.sleep(1)

terminate_thread(t)

print(res)

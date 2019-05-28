import timeit
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


def plot(func, start, end, repeat=1, saveimg=0):
    """
    Function for visualizing the asymptotics of algorithms.

    Usage: asympt.plof("f({N})", start, end, repeats=1, saveimg=0)
    """
    N = np.arange(start, end + 1)
    data = {}
    func_name = func[:func.find('(')]
    for i in N:
        data[i] = timeit.timeit(func.format(
            N=i), "from __main__ import {}".format(func_name), number=repeat)
    n = list(data.keys())
    t = list(data.values())
    fig, ax = plt.subplots()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.plot(n, t)
    ax.set(xlabel='N', ylabel='time (s)', title=func_name + '(N)')
    ax.grid()
    if saveimg:
        fig.savefig(func_name + "_asympt")
    plt.show()

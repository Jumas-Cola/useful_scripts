import timeit
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


def plot(funcs, start, end, step=1, repeat=10):
    """
    Function for visualizing the asymptotics of algorithms.

    Usage: asympt.plof("f({N})", start, end, step=1, repeat=1)
    """
    N = list(range(start, end + 1, step))
    fig, ax = plt.subplots()
    for f in funcs:
        f_name = f[:f.find('(')]
        ax.plot(N, [timeit.timeit(f.format(N=i),
                "from __main__ import {}".format(f_name), number=repeat)
                    for i in N], label=f_name)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.legend()
    ax.set(xlabel='N', ylabel='time (s)')
    ax.grid()
    plt.show()

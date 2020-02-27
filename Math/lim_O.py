import sympy as smp


def sort_by_asympt(funcs, n):
    sorted_funcs = []
    while funcs:
        max_f = funcs[0]
        for func in funcs:
            lim = smp.limit(max_f / func, n, smp.oo)
            if lim == 0:
                max_f = func
        sorted_funcs.append(max_f)
        i = funcs.index(max_f)
        del funcs[i]
    return sorted_funcs[::-1]


n = smp.symbols('n')

funcs = [
    smp.sqrt(n),
    n / smp.log(n, 5),
    smp.log(smp.factorial(n), 2),
    3 ** smp.log(n, 2),
    n ** 2,
    smp.log(smp.log(n, 2)),
    smp.sqrt(smp.log(n, 4)),
    2 ** n,
    4 ** n,
    2 ** (3 * n),
    smp.factorial(n),
    2 ** (2 ** n),
    smp.log(n, 3),
    smp.log(n, 2) ** 2,
    7 ** (smp.log(n, 2)),
    smp.log(n, 2) ** (smp.log(n, 2)),
    n ** (smp.sqrt(n)),
    n ** (smp.log(n, 2)),
]

print(sort_by_asympt(funcs, n))

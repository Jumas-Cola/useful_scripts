from collections.abc import Iterable
from collections import defaultdict


def flatten(lst):
    for el in lst:
        if isinstance(el, Iterable):
            yield from flatten(el)
        else:
            yield el


def abc_solver(B, P):
    code_layers = {}
    ans = defaultdict(str)
    P = [{
        'val': p,
        'order': (i,)
    } for i, p in enumerate(P, 1)]

    q = len(B)
    r = len(P)

    if (q == 2):
        q0 = 2
    else:
        k = r % (q - 1)
        if (k == 0):
            q0 = q - 1
        elif (k == 1):
            q0 = q
        else:
            q0 = k

    while len(P) >= q:
        P.sort(key=lambda x: -x['val'])
        first = P[:-q0]
        last = P[-q0:]

        code_layer = []
        val = 0
        order = tuple()
        for i, b in zip(last, B):
            code_layer += [b]
            val += i['val']
            order += (i['order'],)
            for j in i['order']:
                if (isinstance(j, Iterable)):
                    for m in flatten(j):
                        ans[m] += str(b)
                else:
                    ans[j] += str(b)

        q0 = q

        code_layers[tuple(order)] = code_layer

        P = first + [{'val': val, 'order': order}]

    for i in sorted(dict(ans).items()):
        print(i[0], ' - ', i[1])


abc_solver(
    (0, 1, 2, 3),
    (0.3, 0.25, 0.2, 0.12, 0.08, 0.025, 0.02, 0.005)
)

# abc_solver(
#         (0, 1),
#         (0.1, 0.25, 0.2, 0.01, 0.05, 0.09, 0.15, 0.15)
#         )

import itertools
import re

func = "(a or (b and c)) == (not (not c or d) or r)"

letters = sorted(list(set(re.findall(r'\b\w\b', func))))
repeat = len(letters)
print(*letters, '\t', func)
for i in itertools.product((0,1), repeat=repeat):
    f_copy = func
    for n, l in enumerate(letters):
        f_copy = re.sub(r'\b{}\b'.format(l), str(i[n]), f_copy)
    print(*i, '\t', int(eval(f_copy)))

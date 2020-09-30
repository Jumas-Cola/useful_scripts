import time
from functools import partial
import re


class MNR:
    def __init__(self, tape, prog):
        self.I = []
        self.parser(prog)
        self.R = {n: int(r) for n, r in enumerate(tape.strip(), 1)}
        self.i = 0

    def Z(self, n):
        if n in self.R:
            self.R[n] = 0

    def S(self, n):
        if n in self.R:
            self.R[n] += 1
        else:
            self.R[n] = 1

    def T(self, m, n):
        if m in self.R:
            self.R[n] = self.R[m]
        else:
            self.R[n] = 0

    def J(self, m, n, q):
        if m in self.R and n in self.R:
            if self.R[m] == self.R[n]:
                self.i = q - 2
        elif n in self.R:
            if 0 == self.R[n]:
                self.i = q - 2
        elif m in self.R:
            if self.R[m] == 0:
                self.i = q - 2
        else:
            self.i = q - 2

    def print_field(self):
        print('I:', self.i + 1)
        print('r:', end=' ')
        for k, v in sorted(self.R.items()):
            if k == 1 or k - 1 in self.R:
                print('{: 3}'.format(v), end=' ')
            else:
                print('...', '{: 3}'.format(v), end=' ')
        print()
        print('R:', end=' ')
        for k, v in sorted(self.R.items()):
            if k == 1 or k - 1 in self.R:
                print('{: 3}'.format(k), end=' ')
            else:
                print('...', '{: 3}'.format(k), end=' ')
        print()

    def parser(self, s):
        for row in s.split('\n'):
            row = row.strip()
            if re.match(r'J\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)', row):
                args = map(int, re.findall(r'\d+', row))
                self.I.append(partial(self.J, *args))
            elif re.match(r'T\(\s*\d+\s*,\s*\d+\s*\)', row):
                args = map(int, re.findall(r'\d+', row))
                self.I.append(partial(self.T, *args))
            elif re.match(r'Z\(\s*\d+\s*\)', row):
                args = map(int, re.findall(r'\d+', row))
                self.I.append(partial(self.Z, *args))
            elif re.match(r'S\(\s*\d+\s*\)', row):
                args = map(int, re.findall(r'\d+', row))
                self.I.append(partial(self.S, *args))

    def run(self):
        while self.i < len(self.I):
            self.print_field()
            time.sleep(0.4)
            self.I[self.i]()
            self.i += 1
        self.print_field()


prog = '''
        J(1, 3, 9)
        J(2, 3, 9)
        J(2, 3, 7)
        S(1)
        S(3)
        J(1, 1, 3)
        Z(2)
        Z(3)
        J(1, 1, 100)
        Z(1)
        Z(2)
        J(1, 1, 100)
'''
tape = '34'

m = MNR(tape, prog)
m.run()


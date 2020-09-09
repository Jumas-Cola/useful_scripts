from time import sleep
import argparse


class TM:
    def __init__(self):
        self.state = 'q1'
        self.pos = 0
        self.tape = []


    def print_state(self):
        print(self.state + ':', ' ' * self.pos + 'V')
        print(' ' * len(self.state) + ' ', ''.join(self.tape))


    def execute_line(self, line):
        state_A, sign_A, *other, state_B, sign_B, shift =  line.split()
        if self.state == state_A and self.tape[self.pos] == sign_A:
            self.state = state_B

            if self.pos < 0:
                self.pos = 0
                self.tape.insert(0, sign_B)
            elif self.pos >= len(self.tape):
                self.tape.append(sign_B)
            else:
                self.tape[self.pos] = sign_B

            if shift == 'L':
                self.pos -= 1
            elif shift == 'R':
                self.pos += 1

            if self.pos < 0:
                self.pos = 0
                self.tape.insert(0, '0')
            elif self.pos >= len(self.tape):
                self.tape.append('0')

            return False
        return True


    def execute(self, tape, program, timeout=0.4, verbose=False):
        self.tape = list(tape.strip('0'))
        program = tuple(line.strip() for line in program.split('\n') if line)
        while self.state != 'qz':
            if verbose: self.print_state()
            for line in program:
                executing = self.execute_line(line)
                if not executing:
                    break
            if verbose: sleep(timeout)
        if verbose: self.print_state()
        return ''.join(self.tape).strip('0')


parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='''
    Turing machine interpreter.

    Example program - adding 2 numbers (111*1111):
    q1 * -> qz 0 E
    q1 1 -> q2 0 R
    q2 1 -> q2 1 R
    q2 * -> qz 1 E
    ''')
parser.add_argument('-v', '--verbose', action='store_true')
parser.add_argument('-p', '--program_file', required=True, help='File with Turing machine program.')
parser.add_argument('-t', '--tape', required=True, help='String with start tape configuration.')
args = parser.parse_args()

tm = TM()
print(tm.execute(args.tape, open(args.program_file).read(), verbose=args.verbose))

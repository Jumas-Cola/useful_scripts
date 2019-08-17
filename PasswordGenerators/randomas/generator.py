import random
import dic


class PassGenerator:

    def __init__(self, items=1, nums=3, low=5, up=2, signs=2):
        self.items = items
        self.nums = nums
        self.low = low
        self.up = up
        self.signs = signs

    def __iter__(self):
        for _ in range(self.items):
            yield self.pass_generate()

    def pass_generate(self):
        password = []
        for i in range(self.nums):
            password += random.choice([*'0123456789'])
        for i in range(self.low):
            password += random.choice([chr(i) for i in range(97, 123)])
        for i in range(self.up):
            password += random.choice([chr(i) for i in range(65, 91)])
        for i in range(self.signs):
            password += random.choice([*r'!@#$%^&*_=+-/"[](){}'])
        random.shuffle(password)
        return ''.join(password)


class LoginGenerator:

    def __init__(self, items=1, length=10, dictionary=None):
        if not dictionary:
            dictionary = dic.dic
        self.dictionary = dictionary
        self.items = items
        self.length = length

    def __iter__(self):
        for _ in range(self.items):
            yield self.login_generate()

    @staticmethod
    def leet(string):
        d = {'a': '@', 'b': '8', 'c': '(', 'd': '|)', 'e': '3', 'f': '|=',
             'g': '9', 'h': '#', 'i': '!', 'j': '_|', 'k': '|{', 'l': '1',
             'm': '|\\/|', 'n': '/|/', 'o': '0', 'p': '|D', 'q': '(,)', 'r': '|?',
             's': '$', 't': '7', 'u': '|_|', 'v': '\\/', 'w': '\\|\\|', 'x': '}{',
             'y': '\'/', 'z': '(\\)'}
        string = list(string)
        indexes = list(range(len(string)))
        for _ in range(len(string) // 4):
            if indexes:
                i = random.randint(0, len(indexes) - 1)
                string[indexes[i]] = d[string[indexes[i]]]
                del indexes[i]
        return ''.join(string)

    def login_generate(self):
        login = ''
        while len(login) < self.length:
            login += random.choice(self.dictionary)
        return self.leet(login)

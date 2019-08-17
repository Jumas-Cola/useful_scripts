import sys
import os

try:
    file = sys.argv[1]
except:
    print('\nUsage: py freq_crypto.py <file>\n')
    raise

file_str = ''
with open(file, 'r') as f:
    for string in f:
        for i in '  \n':
            string = string.replace(i, '')
        file_str += string

freq_dict = {}
for ch in set(file_str):
    freq_dict[ch] = file_str.count(ch) / len(file_str) * 100

freq_dict = sorted(freq_dict.items(), key=lambda x: x[1], reverse=1)

counter = 0
res_file = 'freq_crypto_{}.txt'.format(counter)
while os.path.exists(res_file):
    counter += 1
    res_file = 'freq_crypto_{}.txt'.format(counter)

with open(res_file, 'a') as f:
    for i in freq_dict:
        f.write('{} {}\n'.format(i[0], i[1]))

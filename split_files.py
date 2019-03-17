import os
import shutil
import sys


def split_list(l, n):
    return [l[i:i + n] for i in range(0, len(l), n)]


if len(sys.argv) != 3:
    print('\nUsage: python3 {} <directory> <count>\n'.format(
        os.path.split(sys.argv[0])[1]))
    raise ValueError("Missing required positional arguments.")

directory, n = sys.argv[1], int(sys.argv[2])

path, folder = os.path.split(directory)
new_dir = '{}{}{}{}{}'.format(path, os.sep, folder, '_splitted_by_', n)
if not os.path.exists(new_dir):
    os.mkdir(new_dir)
for num, i in enumerate(sorted(split_list(os.listdir(directory), n))):
    res_folder = '{}{}{}'.format(new_dir, os.sep, num)
    if not os.path.exists(res_folder):
        os.mkdir(res_folder)
    for file in i:
        old_file = '{}{}{}'.format(directory, os.sep, file)
        shutil.copy(old_file, res_folder)
print('\nFinished!')

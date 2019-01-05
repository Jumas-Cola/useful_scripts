
import sys
import os
import hashlib

def check_for_duplicates(path):
    hash_dict = {}
    doubles_count = 0
    for item in os.listdir(path):
        with open(path+'\\'+item, "rb") as f:
            hash_dict.update({item: hashlib.sha1(f.read())})
    keys = list(hash_dict.keys())
    for key in keys:
        for key_1 in keys:
            if (key != key_1) and (hash_dict[key].hexdigest() == hash_dict[key_1].hexdigest()):
                print(key, '|**************|',key_1, '\n')
                os.remove(path+'\\'+key_1)
                keys.remove(key_1)
                hash_dict.pop(key_1)
                doubles_count += 1
    return doubles_count


if sys.argv[1:]:
    print('Doubles count: ',check_for_duplicates(sys.argv[1:]))
else:
    print("Please pass the paths to check as parameters to the script")"""

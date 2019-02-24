import random

# count_nums - count of numbers in password
# count_chars - count of small letters in pass
# count_caps - count of large letters in pass
# count_signs - count of signs in pass


def pass_generate(nums=3, chars=5, caps=2, signs=2):
    password = []
    for i in range(nums):
        password += random.choice([*'0123456789'])
    for i in range(chars):
        password += random.choice([chr(i) for i in range(97, 123)])
    for i in range(caps):
        password += random.choice([chr(i) for i in range(65, 91)])
    for i in range(signs):
        password += random.choice([*r'!@#$%^&*_=+-/"'])
    random.shuffle(password)
    return ''.join(password)


print('By default: ' + pass_generate())
print('Only 12 nums: ' + pass_generate(12, 0, 0, 0))
print('8 small and 4 large letters: ' + pass_generate(0, 8, 4, 0))

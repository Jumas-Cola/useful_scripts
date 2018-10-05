"""
    Cкрипт для автоматической постановки ударения в словах
    Источник: https://где-ударение.рф/
"""


from bs4 import BeautifulSoup
import urllib.parse
import requests
import re


def word_accent(word):
    res_array = []
    encoded_word = urllib.parse.quote_plus(word)
    url = 'https://xn----8sbhebeda0a3c5a7a.xn--p1ai/%D0%B2-%D1%81%D0%BB%D0%BE%D0%B2%D0%B5-{}/'.format(encoded_word)
    doc = requests.get(url)
    soup = BeautifulSoup(doc.content, "lxml")
    div_word = soup.find('div', {'class': 'rule'})
    pattern = r'— [^.,]+[.,]'
    words_with_accent = re.findall(pattern, str(div_word))
    for word in words_with_accent:
        word = word[2:-1]
        pattern = r'<b>[^</b>]+</b>'
        for sign in re.findall(pattern, word):
            word = word.replace(sign, sign[3:-4].lower()+'\'')
        res_array.append(word)
    return res_array


def txt_to_list(file_name):
    res_list = []
    with open(file_name) as file:
        for row in file:
            res_list.append(row.rstrip('\n').strip().lower())
    return res_list


def list_to_text(in_list, file_name, type_write):
    f = open(file_name, type_write)
    for string in in_list:
        f.write(string+"\n")
    f.close()


while True:
    try:
        file_name = input('Input file name: ')
        word_list = txt_to_list(file_name)
        break
    except:
        print('File not exist. Try again.')

for word in word_list:
    try:
        list_to_text(word_accent(word), 'words_with_accent.txt', 'a')
    except:
        print('Cant found : {}'.format(word))
"""
    Скрипт для скачивания галерей с deviantart.com
"""

from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from urllib.request import urlretrieve
from selenium import webdriver
import time
import sys
import os
from bs4 import BeautifulSoup


def init_driver(path=r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe'):
    gecko = os.path.normpath(os.path.join(
        os.path.dirname(__file__), 'geckodriver'))
    # ...path to firefox.exe
    binary = FirefoxBinary(path)
    driver = webdriver.Firefox(
        firefox_binary=binary, executable_path=gecko + '.exe')
    driver.wait = WebDriverWait(driver, 5)
    return driver


def devian_authorization(login, password, driver):
    driver.get('https://www.deviantart.com/users/login')
    time.sleep(5)
    try:
        log = driver.wait.until(
            EC.presence_of_element_located((By.NAME, "username")))
        log.send_keys(login)
        pas = driver.wait.until(
            EC.element_to_be_clickable((By.NAME, "password")))
        pas.send_keys(password)
        button = driver.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#login > table > tbody > tr:nth-child(4) > td > input")))
        button.click()
        time.sleep(5)
    except TimeoutException:
        print("Box or Button not found in deviantart.com")

try:
    url = sys.argv[1]
except:
    print("\n--------------------------------------------------")
    print("\nUsage:\npy downl_from_devianart.py <url> <login> <password>")
    exit()
login = sys.argv[2]
password = sys.argv[3]

driver = init_driver()

try:
    devian_authorization(login, password, driver)
except:
    print("\n--------------------------------------------------")
    print('\nCant authorize.')

dir = url.split('/')[-3]
try:
    os.makedirs(dir)
except:
    pass

driver.get(url)
find_set = set()

# scrolling
lastHeight = driver.execute_script("return document.body.scrollHeight")
offset = 1000
pos = 0
while True:
    driver.execute_script(f"window.scrollTo(0, {pos});")
    html = driver.page_source
    soup = BeautifulSoup(html, "html5lib")
    find_list = soup.select('a.torpedo-thumb-link')
    for href in [href.get('href') for href in find_list]:
        find_set.add(href)
    newHeight = driver.execute_script("return document.body.scrollHeight")
    if pos >= lastHeight:
        break
    lastHeight = newHeight
    pos += offset

print('Total imgs count:'+str(len(find_set)))

html = driver.page_source
soup = BeautifulSoup(html, "html5lib")
find_list = soup.select('a.torpedo-thumb-link')
find_list = [href.get('href') for href in find_list]
for href in find_set:
    print(href)
    driver.get(href)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    src = soup.select('img.dev-content-normal')[0].get('src')
    urlretrieve(src, dir+'/'+src.split('/')[-1])

driver.quit()
time.sleep(5)
print("\n--------------------------------------------------")
print("\nFinished!")

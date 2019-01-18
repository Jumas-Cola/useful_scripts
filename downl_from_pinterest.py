"""
    Скрипт для скачивания пинов с pinterest
    Для работы нужен geckodriver.exe
"""

from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from urllib.request import urlretrieve
from selenium import webdriver
import time
import os


def init_driver(path=r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe'):
    gecko = os.path.normpath(os.path.join(
        os.path.dirname(__file__), 'geckodriver'))
    # ...path to firefox.exe
    binary = FirefoxBinary(path)
    driver = webdriver.Firefox(
        firefox_binary=binary, executable_path=gecko + '.exe')
    driver.wait = WebDriverWait(driver, 5)
    return driver


link_file_name = 'list.txt' # список ссылок на пины
dir_name = 'photos' # имя папки для сохранения


browser = init_driver()
try:
    os.mkdir(dir_name)
except:
    pass
with open(link_file_name, 'r') as f:
    for string in f:
        browser.get(string)  # Загружаем страницу
        time.sleep(5)
        place_block = browser.find_element_by_css_selector(
            "div._ub._49._4f._uc._2v > img")
        place_img = place_block.get_attribute('src')
        urlretrieve(place_img, dir_name + '/' + place_img.split('/')[-1])
browser.quit()
time.sleep(5)

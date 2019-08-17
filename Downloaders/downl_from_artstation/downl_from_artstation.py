"""
    Скрипт для скачивания пинов с pinterest
    Для работы нужен geckodriver.exe

    ↓↓↓ JS скрипт для скачивания ссылок на изображения с доски
        (пролистать до низа страницы, уменьшив масштаб, а потом запускать) ↓↓↓

    var items = document.querySelectorAll(".project-image");
    var text = "";
    for (i = 0; i < items.length; i++) {
        text += "https://www.artstation.com"+items[i].getAttribute("href")+"\n";
    }
    var a = document.createElement("a");
    a.setAttribute("href", "data:text/plain;charset=utf-8," + text);
    a.setAttribute("download", "link_list.txt");
    a.click();
"""

from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
import requests
import shutil
import time
import os


def init_driver(path=r'C:\Program Files\Mozilla Firefox\firefox.exe'):
    gecko = os.path.normpath(os.path.join(
        os.path.dirname(__file__), 'geckodriver'))
    # ...path to firefox.exe
    binary = FirefoxBinary(path)
    driver = webdriver.Firefox(
        firefox_binary=binary, executable_path=gecko + '.exe')
    driver.wait = WebDriverWait(driver, 5)
    return driver


link_file_name = 'link_list.txt'  # список ссылок на пины
dir_name = 'davidpan1905'  # имя папки для сохранения


browser = init_driver()
try:
    os.mkdir(dir_name)
except:
    pass
with open(link_file_name, 'r') as f:
    for string in f:
        browser.get(string)  # Загружаем страницу
        time.sleep(5)
        place_blocks = browser.find_elements_by_css_selector(
            "div.artwork-image > img")
        for place_block in place_blocks:
            place_img = place_block.get_attribute('src').rstrip('?0123456789')
            print(place_img)
            # обход запрета на скачивание
            r = requests.get(place_img, stream=True, headers={'User-agent': 'Mozilla/5.0'})
            if r.status_code == 200:
                with open(dir_name + '/' + place_img.split('/')[-1], 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
browser.quit()
time.sleep(5)
print("\n--------------------------------------------------")
print("\nFinished!")

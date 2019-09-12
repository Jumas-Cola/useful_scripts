"""
selenium script for downloading pdf from e.lanbook.com

Usage:
py elan_downl.py -l <login> -p <password> -b <number or url like:> 1111 https://e.lanbook.com/book/2222 https://e.lanbook.com/reader/book/3333/#1
"""


from selenium import webdriver
import time
import os
import codecs
from urllib.parse import urlparse
import shutil
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from PyPDF2 import PdfFileMerger
import sys
import argparse


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--login')
    parser.add_argument('-p', '--password')
    parser.add_argument('-b', '--books', nargs='+')
    return parser


class Downloader:
    def __init__(self, login, password, path=os.getcwd()):
        self.login = login
        self.password = password
        self.browser = webdriver.Chrome()
        self.path = path
        self.svg_dir = os.path.join(self.path, 'svg')
        self.pdf_dir = os.path.join(self.path, 'pdf')

    def signin(self):
        self.browser.get('https://e.lanbook.com/auth/signin')
        time.sleep(5)
        login = self.browser.find_element_by_name('username')
        login.send_keys(self.login)
        password = self.browser.find_element_by_name('password')
        password.send_keys(self.password)
        btn = self.browser.find_element_by_css_selector(
            'body > ebs-root > app-auth-layout > section > app-signin-page > mat-card > app-signin-form > form > mat-card-actions > button')
        btn.click()
        time.sleep(5)

    def get_pages(self, bookpage):
        u = urlparse(bookpage)
        book_num = u.path.strip('/').split('/')[-1]
        self.browser.get(
            'https://e.lanbook.com/reader/book/{}/'.format(book_num))
        time.sleep(5)
        total_pages = int(self.browser.find_element_by_css_selector(
            '#page-navigation > span').text.strip('/'))
        book_name = self.browser.find_element_by_css_selector(
            '#panel-head > div > div > h4').text.replace(' ', '_')
        return book_name, ['https://fs1.e.lanbook.com/api/book/{}/page/{}/img'.format(book_num, i) for i in range(1, total_pages + 1)]

    def download_svg(self, pages):
        not os.path.exists(self.svg_dir) or shutil.rmtree(self.svg_dir)
        os.mkdir(self.svg_dir)
        for url in pages:
            url = url.strip()
            self.browser.get(url)
            file_name = '_'.join(url.split('/')[-3:]) + '.svg'
            file_object = codecs.open(os.path.join(
                self.svg_dir, file_name), 'w', 'utf-8')
            html = self.browser.page_source.replace(
                '<?xml version="1.0" encoding="UTF-8"?>', '')
            file_object.write(html)

    def svg_to_pdf(self):
        not os.path.exists(self.pdf_dir) or shutil.rmtree(self.pdf_dir)
        os.mkdir(self.pdf_dir)
        for svg in os.listdir(self.svg_dir):
            drawing = svg2rlg(os.path.join(self.svg_dir, svg))
            renderPDF.drawToFile(drawing, os.path.join(
                self.pdf_dir, os.path.splitext(svg)[0] + '.pdf'))

    def join_pdf(self, filename='result'):
        pdfs = sorted(os.listdir(self.pdf_dir),
                      key=lambda x: int(x.split('_')[1]))
        merger = PdfFileMerger()
        for pdf in pdfs:
            merger.append(os.path.join(self.pdf_dir, pdf))
        merger.write(os.path.join(os.path.splitext(filename)[0] + '.pdf'))
        merger.close()

    def make_pdf(self, bookpage):
        name, pages = self.get_pages(bookpage)
        self.download_svg(pages)
        self.svg_to_pdf()
        self.join_pdf(name)
        shutil.rmtree(self.pdf_dir)
        shutil.rmtree(self.svg_dir)

    def close(self):
        self.browser.quit()


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])

    if not namespace.login:
        raise Exception('Login required!')
    if not namespace.password:
        raise Exception('Password required!')
    if not namespace.books:
        raise Exception('Books urls required!')

    login = namespace.login
    password = namespace.password
    books = namespace.books

    d = Downloader(login, password)
    d.signin()
    for url in books:
        try:
            d.make_pdf(url)
        except Exception as e:
            print(str(e))
    d.close()
    print('\n____Finished____')

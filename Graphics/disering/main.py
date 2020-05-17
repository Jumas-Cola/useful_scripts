from PIL import Image
from collections.abc import Iterable
from math import log
import numpy as np
import os


def fs_disering(image_file):
    img = Image.open(image_file)
    img_arr = np.asarray(img)
    grayscale_img_arr = [[int(sum(pixel)/len(pixel))
        if isinstance(pixel, Iterable) else pixel
        for pixel in row] for row in img_arr]
    img_rows = len(grayscale_img_arr)
    bw_img_arr = []
    for i, row in enumerate(grayscale_img_arr):
        bw_row = []
        for j, pixel in enumerate(row):
            if abs(pixel - 255) <= pixel:
                bw_row.append(255)
                if i < img_rows - 1:
                    grayscale_img_arr[i + 1][j] -= (255 - pixel) / 16 * 5
                if j < len(row) - 1:
                    grayscale_img_arr[i][j + 1] -= (255 - pixel) / 16 * 7
                if i < img_rows - 1 and j < len(row) - 1:
                    grayscale_img_arr[i + 1][j + 1] -= (255 - pixel) / 16
                if i < img_rows - 1 and j > 0:
                    grayscale_img_arr[i + 1][j - 1] -= (255 - pixel) / 16 * 3
            else:
                bw_row.append(0)
                if i < img_rows - 1:
                    grayscale_img_arr[i + 1][j] += pixel / 16 * 5
                if j < len(row) - 1:
                    grayscale_img_arr[i][j + 1] += pixel / 16 * 7
                if i < img_rows - 1 and j < len(row) - 1:
                    grayscale_img_arr[i + 1][j + 1] += pixel / 16
                if i < img_rows - 1 and j > 0:
                    grayscale_img_arr[i + 1][j - 1] += pixel / 16 * 3
        bw_img_arr.append(bw_row)
    bw_img_arr = np.array(bw_img_arr)
    filename, _ = os.path.splitext(image_file)
    img = Image.fromarray(np.uint8(bw_img_arr))
    img.save('{}_fs_disered.{}'.format(filename, 'bmp'), 'BMP')


def baer_matr(n, f=1):
    if n > 0:
        n -= 1
        a = np.array([[4 * baer_matr(n, 0), 4 * baer_matr(n, 0) + 2],
                      [4 * baer_matr(n, 0) + 3, 4 * baer_matr(n, 0) + 1]])
        if f:
            for _ in range((n+1)*2):
                a = np.hstack(a)
        return a
    else:
        return np.array([[4*n, 4*n + 2], [4*n + 3, 4*n + 1]])


def generate_matr(size=4):
    n = baer_matr(round(log(size, 2) - 1))
    x, y = n.shape
    n = (n + 1)/(x * y)
    return n


def ordered_disering(image_file, size=4):
    index_matrix = generate_matr(size)
    img = Image.open(image_file)
    img_arr = np.asarray(img).tolist()
    index_rows, index_cols = index_matrix.shape
    for i in range(0, len(img_arr), index_rows):
        for j in range(0, len(img_arr[i]), index_cols):
            for m in range(index_rows):
                for n in range(index_cols):
                    row, col  = i + n, j + m
                    if row < len(img_arr) and col < len(img_arr[i]):
                        pixel = img_arr[row][col]
                        img_arr[row][col] = int(sum(pixel)/len(pixel)) if isinstance(pixel, Iterable) else pixel
                        img_arr[row][col] = 0 if img_arr[row][col] < 255 * index_matrix[m][n] else 255
    img_arr = np.array(img_arr)
    filename, _ = os.path.splitext(image_file)
    img = Image.fromarray(np.uint8(img_arr))
    img.save('{}_ordered_disered.{}'.format(filename, 'bmp'), 'BMP')




ordered_disering('img.jpg', size=4)
fs_disering('img.jpg')


import cv2
import os
import numpy as np
from time import time
import sys
from math import log
from functools import partial

usage = """
Usage:
    video_dithering.py video.mp4

Output:
    video_dithered.mp4 (without sound)
"""

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])


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



def matr_func(img_list, index_matrix, index_rows, index_cols, pool_param):
    i, j = pool_param
    for m in range(index_rows):
        for n in range(index_cols):
            row, col  = i + n, j + m
            if row < len(img_list) and col < len(img_list[i]):
                img_list[row][col] = 0 if img_list[row][col] < 255 * index_matrix[m][n] else 255



def ordered_disering(img, size=4):
    index_matrix = generate_matr(size)
    img_list = rgb2gray(img).tolist()
    index_rows, index_cols = index_matrix.shape
    pool_params = ((i, j) for i in range(0, len(img_list), index_rows) for j in range(0, len(img_list[i]), index_cols))
    f = partial(matr_func, img_list, index_matrix, index_rows, index_cols)
    for pool_param in pool_params:
        f(pool_param)
    img_list = np.stack((img_list,)*3, axis=-1)
    return np.uint8(img_list)


def main():
    video_name = sys.argv[1]

    vidcap = cv2.VideoCapture(video_name)
    success, image = vidcap.read()
    count = 1

    height, width, layers = image.shape
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    out_video_name = video_name.split('.')[0] + '_dithered.mp4'
    video = cv2.VideoWriter(out_video_name, cv2.VideoWriter_fourcc(*'MP4V'), fps, (width,height))

    start_time = time()
    while success:
        print('Second: {:.3}'.format(count/fps))
        image = ordered_disering(image)
        video.write(image)
        success, image = vidcap.read()
        count += 1

    print('Total time:', time() - start_time)

    cv2.destroyAllWindows()
    video.release()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(str(e) + '\n\n')
        print(usage)

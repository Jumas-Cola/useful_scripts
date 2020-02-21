from PIL import Image
import numpy as np
import os
import random as rd
import sys


def avg(arr):
    return np.sum(arr) / arr.shape[0]


def color_dist(im_array_1, im_array_2, power=2):
    im_array_1 = im_array_1.astype(np.float32)
    im_array_2 = im_array_2.astype(np.float32)
    return avg(np.array(list(map(lambda x: np.sum(x) ** .5, (im_array_1 - im_array_2) ** power))))


if len(sys.argv) > 1:
    folder = sys.argv[1]
else:
    raise Exception(
        '[Error!] Dir path not entered\nUsage: main.py <path_to_folder>')

imgs = [np.asarray(Image.open(os.path.join(folder, im_name)))
        for im_name in os.listdir(folder)]
rd.shuffle(imgs)

max_height = imgs[0].shape[0]
for i in range(len(imgs)):
    max_height = max(max_height, imgs[i].shape[0])

for n, img in enumerate(imgs):
    if img.shape[0] < max_height:
        zeros = np.zeros((max_height, *img.shape[1:]))
        zeros[:img.shape[0], :img.shape[1], :img.shape[2]] = img
        imgs[n] = zeros

channels = imgs[0].shape[-1]
len_imgs = len(imgs) - 1
for i in range(len(imgs) - 1):
    print(i + 1, '/', len_imgs)
    img_1 = imgs.pop()
    min_dist_img = (float('inf'), 0, '')
    for n, img_2 in enumerate(imgs):
        dist_r = color_dist(
            img_1[:, -1:].reshape(-1, channels), img_2[:, 0:1].reshape(-1, channels))
        dist_l = color_dist(
            img_1[:, 0:1].reshape(-1, channels), img_2[:, -1:].reshape(-1, channels))
        if dist_r < min_dist_img[0]:
            min_dist_img = (dist_r, n, 'r')
        if dist_l < min_dist_img[0]:
            min_dist_img = (dist_l, n, 'l')

    res = []
    for n, row in enumerate(img_1):
        if min_dist_img[2] == 'r':
            res.append(np.concatenate((row, imgs[min_dist_img[1]][n])))
        else:
            res.append(np.concatenate((imgs[min_dist_img[1]][n], row)))

    imgs.pop(min_dist_img[1])
    imgs.append(np.uint8(np.array(res)))

im = Image.fromarray(imgs[0])

if channels == 4:
    im.save('output.png')
elif channels == 3:
    im.save('output.jpg')
else:
    im.save('output.bmp')

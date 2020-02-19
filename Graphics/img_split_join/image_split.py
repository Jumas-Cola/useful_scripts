from PIL import Image
import numpy as np
import os
import random as rd
import sys


def image_split(img_path, lines=20, size=0):
    path = os.path.dirname(img_path)

    img = np.asarray(Image.open(img_path))
    channels = img.shape[-1]

    pixels = list(range(img.shape[1]))
    delims = [0, len(pixels)]

    if size == 0:
        for i in range(lines - 1):
            delims.append(pixels[1:].pop(rd.randint(0, len(pixels) - 1)))
    else:
        delims = pixels[::size] + [len(pixels)]

    delims.sort()

    for i in range(len(delims) - 1):

        im = Image.fromarray(img[:, delims[i]:delims[i + 1]])

        if channels == 4:
            im.save(os.path.join(path, '{}.png'.format(i)))
        elif channels == 3:
            im.save(os.path.join(path, '{}.jpg'.format(i)))
        else:
            im.save(os.path.join(path, '{}.bmp'.format(i)))


if len(sys.argv) == 4:
    img_path = sys.argv[1]
    size = int(sys.argv[2])
    lines = int(sys.argv[3]) - 1 if int(sys.argv[3]) > 0 else 0
elif len(sys.argv) == 3:
    img_path = sys.argv[1]
    size = int(sys.argv[2])
    lines = 20
elif len(sys.argv) == 2:
    img_path = sys.argv[1]
    size = 0
    lines = 20
else:
    raise Exception(
        '[Error!] Image path not entered\nUsage: main.py <path_to_image>')

image_split(img_path, lines=lines, size=size)

from pathlib import Path
import numpy as np
from PIL import Image
import random


def stegano_encoder(img_bytes, string_bytes):
    c = 0
    for i, row in enumerate(img_bytes):
        for j, pixel in enumerate(row):
            r, g, b = pixel
            r_b, g_b, b_b = bin(r)[2:].zfill(8), bin(g)[2:].zfill(8), bin(b)[2:].zfill(8)
            if c < len(string_bytes):
                char_bin = bin(string_bytes[c])[2:].zfill(8)
                r_b = r_b[:-3] + char_bin[:3]
                g_b = g_b[:-3] + char_bin[3:6]
                b_b = b_b[:-2] + char_bin[6:]
            else:
                char_bin = '0' * 8
                r_b = r_b[:-3] + char_bin[:3]
                g_b = g_b[:-3] + char_bin[3:6]
                b_b = b_b[:-2] + char_bin[6:]
                img_bytes[i][j] = np.array([int(r_b, 2), int(g_b, 2), int(b_b, 2)])
                if c < len(string_bytes):
                    raise Exception('Word is too long!')
                else:
                    return img_bytes

            img_bytes[i][j] = np.array([int(r_b, 2), int(g_b, 2), int(b_b, 2)])
            c += 1
    

def stegano_decoder(img_bytes):
    decoded = []
    for i, row in enumerate(img_bytes):
        for j, pixel in enumerate(row):
            r, g, b = pixel
            r_b, g_b, b_b = bin(r)[2:].zfill(8), bin(g)[2:].zfill(8), bin(b)[2:].zfill(8)
            byte = int(r_b[-3:] + g_b[-3:] + b_b[-2:], 2)
            if byte == 0:
                return bytearray(decoded)
            decoded.append(byte)

    return bytearray(decoded)


def rand_stegano_encoder(img_bytes, string_bytes, seed):
    random.seed(seed)
    c = 0

    rand_pixels = [(i, j, pixel) for i, row in enumerate(img_bytes) 
                                 for j, pixel in enumerate(row)]
    random.shuffle(rand_pixels)
 
    for i, j, pixel in rand_pixels:
        r, g, b = pixel
        r_b, g_b, b_b = bin(r)[2:].zfill(8), bin(g)[2:].zfill(8), bin(b)[2:].zfill(8)
        if c < len(string_bytes):
            char_bin = bin(string_bytes[c])[2:].zfill(8)
            r_b = r_b[:-3] + char_bin[:3]
            g_b = g_b[:-3] + char_bin[3:6]
            b_b = b_b[:-2] + char_bin[6:]
        else:
            char_bin = '0' * 8
            r_b = r_b[:-3] + char_bin[:3]
            g_b = g_b[:-3] + char_bin[3:6]
            b_b = b_b[:-2] + char_bin[6:]
            img_bytes[i][j] = np.array([int(r_b, 2), int(g_b, 2), int(b_b, 2)])
            if c < len(string_bytes):
                raise Exception('Word is too long!')
            else:
                return img_bytes

        img_bytes[i][j] = np.array([int(r_b, 2), int(g_b, 2), int(b_b, 2)])
        c += 1
 

def rand_stegano_decoder(img_bytes, seed):
    random.seed(seed)
    decoded = []

    rand_pixels = [(i, j, pixel) for i, row in enumerate(img_bytes) 
                                 for j, pixel in enumerate(row)]
    random.shuffle(rand_pixels)

    for i, j, pixel in rand_pixels:
        r, g, b = pixel
        r_b, g_b, b_b = bin(r)[2:].zfill(8), bin(g)[2:].zfill(8), bin(b)[2:].zfill(8)
        byte = int(r_b[-3:] + g_b[-3:] + b_b[-2:], 2)
        if byte == 0:
            return bytearray(decoded)
        decoded.append(byte)

    return bytearray(decoded)


#!/usr/bin/env python3
from PIL import Image
import base64
import io
from math import sqrt


threshold = 120


def read_image(b):
    f = io.BytesIO(base64.b64decode(b))
    im = Image.open(f)

    sums = [0, 0, 0]
    n = 0
    for x in range(im.size[0]):
        for y in range(im.size[1]):
            pixel = im.getpixel((x, y))
            if pixel[0] < threshold or \
               pixel[1] < threshold or \
               pixel[2] < threshold:
                sums[0] += pixel[0] ** 2
                sums[1] += pixel[1] ** 2
                sums[2] += pixel[2] ** 2
                n = n + 1

    sums = map(lambda x: sqrt(x / n), sums)

    return sums

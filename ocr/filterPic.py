#! /usr/bin/python3
# -*- coding: utf-8 -*-

from PIL import Image

def extractPixels(image,pixelFile):
    with open(pixelFile,'a+') as f:
        for x in range(image.size[0]):
            for y in range(image.size[1]):
                f.write(str(image.getpixel((x,y))))
                f.write("\t")
            f.write("\n")


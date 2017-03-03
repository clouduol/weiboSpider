#! /usr/bin/python3
# -*- coding: utf-8 -*-
# this script can erase dots from the jpg image,
# however, the tesseract result has a little wrong,1==>I,for example

from PIL import Image
import subprocess

# image: image handle  pixelFile:file to store pixel
def storePixels(image,pixelFile):
    with open(pixelFile,'a+') as f:
        for x in range(image.size[0]):
            for y in range(image.size[1]):
                f.write(str(image.getpixel((x,y))))
                f.write("\t")
            f.write("\n")

# erase little dots from the jpg image
# iamgePath:image path filterImagePath:filter image path 
# handle pixThre:threshold filter parameter gridLen:the grid length
def filterImage(imagePath,filterImagePath,pixThre,gridLen):
    imageRead = Image.open(imagePath)
    imageWrite = Image.open(imagePath)
    imageRead = imageRead.point(lambda x:0 if x<pixThre else 255)
    imageWrite = imageWrite.point(lambda x:0 if x<pixThre else 255)
    # grid erase
    imageReadMap = imageRead.load()
    imageWriteMap = imageWrite.load()
    for x in range(imageRead.size[0]-gridLen+1):
        for y in range(imageRead.size[1]-gridLen+1):
            erase = True
            # bug, check the border...
            for i in range(x,x+gridLen):
                for j in range(y,y+gridLen):
                    # add to fix the bug...
                    if i in [x,x+gridLen-1] or j in [y,y+gridLen-1]:
                        if imageReadMap[i,j][0]!=255:
                            erase = False
                            break
                if erase == False:
                    break
            if erase == False:
                continue
            for i in range(x+1,x+gridLen-1):
                for j in range(y+1,y+gridLen-1):
                    if imageReadMap[i,j][0] == 0:
                        imageWriteMap[i,j]=(255,255,255)
    imageWrite.save(filterImagePath)
    
    return (imageRead,imageWrite)

# show pixel in bits
def showBitsPixel(image):
    for x in range(image.size[1]):
        line=str(x)+"\t"
        for y in range(image.size[0]):
            if image.getpixel((y,x))[0] == 0:
                line = line+"0 "
            else:
                line = line+"1 "
        line = line + "\n"
        print(line)


## find the proper parameter
## threshold = 10/20, gridLen = 4
#threshold = 20
#for x in range(3,20):
#    print("---- "+str(x)+" ----")
#    filterImagePath="captcha_filter_"+str(x)+".jpg"
#    ir,iw=filterImage("captcha_initial.jpg",filterImagePath,threshold,x)

threshold = 20
gridLen = 4
imagePath="captcha_initial.jpg"
txtName = "captcha_initial"
filterImagePath = "captcha_filter_4.jpg"
filterBorderImagePath = "captcha_filter_4b.jpg"
txtBorderFilterName = "captcha_filter_4b"

filterImage(imagePath,filterImagePath,threshold,gridLen)

print("--- captcha initial ---")
subprocess.run(['tesseract',imagePath,txtName])
output = open(txtName+".txt",'r')
print(output.read())
output.close()

print("--- captcha border filter ---")
# should add border first, or error will occur
subprocess.run(['convert',filterImagePath,'-bordercolor','Black','-border','1x1',filterBorderImagePath])
subprocess.run(['tesseract',filterBorderImagePath,txtBorderFilterName])
output = open(txtBorderFilterName+".txt",'r')
print(output.read())
output.close()


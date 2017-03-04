#!/usr/bin/python3
# -*- coding: utf-8 -*-
# this script recognizes characters in the captcha,
# and use them to subbmit comment automatically

from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup
import subprocess
import requests
from PIL import Image
from PIL import ImageOps

def cleanImage(imagePath):
    image = Image.open(imagePath)
    image = image.point(lambda x:0 if x<143 else 255)
    borderImage = ImageOps.expand(image, border=20, fill='white')
    borderImage.save(imagePath)

html = urlopen("http://pythonscraping.com/humans-only")
bsObj = BeautifulSoup(html,"lxml")
# collect form data
imageLocation = bsObj.find("img",{"title":"Image CAPTCHA"})['src']
formBuildId = bsObj.find("input",{"name":"form_build_id"})['value']
captchaSid = bsObj.find("input",{"name":"captcha_sid"})['value']
captchaToken = bsObj.find("input",{"name":"captcha_token"})['value']

captchaUrl = "http://pythonscraping.com"+imageLocation
urlretrieve(captchaUrl,"captcha.jpg")
cleanImage("captcha.jpg")
p =\
subprocess.Popen(['tesseract','captcha.jpg','captcha'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
p.wait()
f = open("captcha.txt",'r')

# clean the space the line feed characters
captchaResponse = f.read().replace(" ","").replace("\n","")
print("Captcha solution attempt: "+captchaResponse)

if len(captchaResponse) == 5:
    params = {"captcha_token":captchaToken, "captcha_sid":captchaSid,
              "form_id":"comment_node_page_form","form_build_id":formBuildId,
              "captcha response":captchaResponse,"name":"nicai",
              "subject":"test",
              "comment_body[und][0][value]":"Just a test, don't worry",
              "op":"Save"}
    r = requests.post("http://www.pythonscraping.com/comment/reply/10",
                      data=params)
    responseObj = BeautifulSoup(r.text,"lxml")
    if responseObj.find("div",{"id","messages"}) is not None:
        print(responseObj.find("div",{"id","messages"}).get_text())
else:
    print("There was a problem reading the CAPTCHA correctly!")

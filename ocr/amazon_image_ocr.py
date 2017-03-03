#!/usr/bin/python3
# -*- coding: utf-8 -*-
# this script simulate the browser,
# first, navigate to the book page in amazon;
# then, open the try to read iframe, collect the images url;
# finally, download them, use tesseract to extract the character and display

import time
from urllib.request import urlretrieve
import subprocess
from selenium import webdriver

# book page url,The Complete Sherlock Holmes (2 Volumes)
book_url =\
"https://www.amazon.com/Complete-Sherlock-Holmes-Volumes/dp/0553328255/"

driver = webdriver.Chrome()
driver.get(book_url)
time.sleep(2)

# click the button to try to read
driver.find_element_by_id("sitbLogoImg").click()
imageList = set()

# wait for the page to load completely
time.sleep(5)
# when the right arrow is ready, click it
print("---- get image url -----")
while "pointer" in\
driver.find_element_by_id("sitbReaderRightPageTurner").get_attribute("style"):
    driver.find_element_by_id("sitbReaderRightPageTurner").click()
    time.sleep(2)
    # get the pages
    pages = driver.find_elements_by_xpath("//div[@class='pageImage']/div/img")
    for page in pages:
        image = page.get_attribute("src")
        imageList.add(image)
        print(image)

driver.quit()

# process the image uing tesseract
print("---- retrieve image ------")
for image in sorted(imageList):
    print(">>>>")
    print(image)
    urlretrieve(image,"amazon_page.jpg")
    p = subprocess.Popen(["tesseract","amazon_page.jpg","amazon_page"],
                         stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p.wait()
    f = open("amazon_page.txt","r")
    print(f.read())

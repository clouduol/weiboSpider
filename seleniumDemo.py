#! /usr/bin/python3
# -*- coding: utf-8 -*-

from selenium import webdriver
import time

# client redirection
from selenium.common.exceptions import StaleElementReferenceException

def waitForLoad(driver):
    elem = driver.find_element_by_tag_name("html")
    count = 0
    while True:
        count += 1
        if count > 20:
            print("Timing out after 10 seconds and returning")
            return
        time.sleep(.5)
        try:
            elem = driver.find_element_by_tag_name("html")
        except StaleElementReferenceException:
            return

driver =\
webdriver.PhantomJS(executable_path="/home/guoyunlong/Software/phantomjs-2.1.1-linux-x86_64/bin/phantomjs")
driver.get("http://pythonscraping.com/pages/javascript/redirectDemo1.html")
print("------ before redirect ------")
print(driver.page_source)
waitForLoad(driver)
print("------ after redirect ------")
print(driver.page_source)

## implicit wait
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.wait import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#
#driver =\
#webdriver.PhantomJS(executable_path="/home/guoyunlong/Software/phantomjs-2.1.1-linux-x86_64/bin/phantomjs")
#driver.get("http://pythonscraping.com/pages/javascript/ajaxDemo.html")
#try:
#    element = WebDriverWait(driver, 10).until(
#        EC.presence_of_element_located((By.ID,"loadedButton")))
#finally:
#    print(driver.find_element_by_css_selector("#content").text)
#    driver.close()

## explicit wait
#driver =\
#webdriver.PhantomJS(executable_path='/home/guoyunlong/Software/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
#
#driver.get("http://pythonscraping.com/pages/javascript/ajaxDemo.html")
#print("before ajax")
#print(driver.find_element_by_id('content').text)
#time.sleep(3)
#print("after ajax")
#print(driver.find_element_by_id('content').text)
#driver.close()

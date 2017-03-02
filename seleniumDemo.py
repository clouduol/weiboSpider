#! /usr/bin/python3
# -*- coding: utf-8 -*-

from selenium import webdriver
import time

# simulate login
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# download chromedriver to $PATH
driver = webdriver.Chrome()
driver.get("http://weibo.com")
# wait for redirect
try:
    element=WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.ID,"loginname")))
finally:
    print("Pass Sina Visitor System, Now In Weibo.com")

try:
    username_elem=driver.find_element_by_id("loginname")
    password_elem=driver.find_element_by_xpath("//input[@type='password']")
    print("Input username:")
    username=input()
    print("Input password:")
    password=input()
    username_elem.send_keys(username)
    password_elem.send_keys(password)
    print("Waiting for data from the server...")
    password_elem.send_keys(Keys.RETURN)
    assert "我的首页" in driver.title
    print("Login successful")

    # print the nick name
    name_elem=driver.find_element_by_class_name("nameBox")
    name_elem=name_elem.find_element_by_tag_name("a")
    print("Your nick name is %s" % name_elem.text)
    # after 10 seconds, quit
    print("10 seconds later, the browser will be closed")
    time.sleep(10)
except Exception as e:
    print("Exception found: %s" % e)
# close the browser
finally:
    driver.close()
    driver.quit()

## client redirection
#from selenium.common.exceptions import StaleElementReferenceException
#
#def waitForLoad(driver):
#    elem = driver.find_element_by_tag_name("html")
#    count = 0
#    while True:
#        count += 1
#        if count > 20:
#            print("Timing out after 10 seconds and returning")
#            return
#        time.sleep(.5)
#        try:
#            elem = driver.find_element_by_tag_name("html")
#        except StaleElementReferenceException:
#            return
#
#driver =\
#webdriver.PhantomJS(executable_path="/home/guoyunlong/Software/phantomjs-2.1.1-linux-x86_64/bin/phantomjs")
#driver.get("http://pythonscraping.com/pages/javascript/redirectDemo1.html")
#print("------ before redirect ------")
#print(driver.page_source)
#waitForLoad(driver)
#print("------ after redirect ------")
#print(driver.page_source)

## wait for event presence 
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

## wait a fixed time
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

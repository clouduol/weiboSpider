#!/usr/bin/python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

#
# independent element actions && ActionChains
#
driver = webdriver.PhantomJS()
driver2 = webdriver.PhantomJS()
driver.get("http://pythonscraping.com/pages/files/form.html")
driver2.get("http://pythonscraping.com/pages/files/form.html")

firstnameField = driver.find_element_by_name("firstname")
firstnameField2 = driver2.find_element_by_name("firstname")
lastnameField = driver.find_element_by_name("lastname")
lastnameField2 = driver2.find_element_by_name("lastname")
submitButton = driver.find_element_by_id("submit")
submitButton2 = driver2.find_element_by_id("submit")

firstnameField.send_keys("Hi")
lastnameField.send_keys("Hello")
submitButton.click()

actions = ActionChains(driver2).click(firstnameField2).send_keys("Hi2")\
                                .click(lastnameField2).send_keys("Hello2")\
                                .send_keys(Keys.RETURN)
actions.perform()

# get screen shot
driver.get_screenshot_as_file('/tmp/dirver.png')
driver2.get_screenshot_as_file('/tmp/dirver2.png')

# print 
print(driver.find_element_by_tag_name("body").text)
print(driver2.find_element_by_tag_name("body").text)

driver.close()
driver2.close()

#
# drag and drop
# this func test fail
#
driver = webdriver.PhantomJS()
driver.get("http://pythonscraping.com/pages/javascript/draggableDemo.html")

print(driver.find_element_by_id("message").text)

element = driver.find_element_by_id("draggable")
target = driver.find_element_by_id("div2")
actions = ActionChains(driver)
actions.drag_and_drop(element,target).perform()

print(driver.find_element_by_id("message").text)

driver.close()

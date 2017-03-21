#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import unquote
import re
import random

class TestWikipedia(unittest.TestCase):
    bsObj = None
    url = None

    def setUpClass():
        print("Begin wikipedia test, You can see this sentence once")

    def test_PageProperties(self):
        global bsObj
        global url

        url = "http://en.wikipedia.org/wiki/Football"
        for i in range(100):
            bsObj = BeautifulSoup(urlopen(url),"lxml")
            titles = self.titleMathchesURL()
            self.assertEqual(titles[0],titles[1])
            self.assertTrue(self.contentExists())
            url = self.getNextLink()
        print("Done")

    def titleMathchesURL(self):
        global bsObj
        global url
        pageTitle = bsObj.find("h1").get_text()
        urlTitle = url[(url.index("/wiki/")+6):]
        urlTitle = urlTitle.replace("_"," ")
        urlTitle = unquote(urlTitle)
        return [pageTitle.lower(),urlTitle.lower()]

    def contentExists(self):
        global bsObj
        content = bsObj.find("div",{"id":"mw-content-text"})
        if content is not None:
            return True
        return False

    def getNextLink(self):
        global bsObj
        links = bsObj.find("div",{"id":"bodyContent"}).findAll("a",
                                                               {"href":re.compile(r"^(/wiki/)((?!:).)*$")})
        link = links[random.randint(0,len(links)-1)].attrs['href']
        print("Next link is: "+link)
        return "http://en.wikipedia.org"+link

if __name__ == "__main__":
    unittest.main()


#class TestAddition(unittest.TestCase):
#    def setUp(self):
#        print("Setting up the test")
#
#    def tearDown(self):
#        print("Tearing down the test")
#
#    def test_twoPlusTwo(self):
#        total=2+2
#        self.assertEqual(4,total)
#
#    def test_twoPlusThree(self):
#        total=2+3
#        self.assertEqual(5,total)
#
#    def test_twoPlusFour(self):
#        total=2+2
#        self.assertEqual(6,total)
#
#if __name__ == '__main__':
#    unittest.main()

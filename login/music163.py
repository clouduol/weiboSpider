#!/usr/bin/python3
# -*- coding: utf-8 -*-
# login 163 music
# weibo(https) login

import requests
import re
import sys
import os
from bs4 import BeautifulSoup

class Music163(object):
    # class data
    # session headers
    headers = {"User-Agent":
               "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,\
               like\
               Gecko) Ubuntu Chromium/56.0.2924.76 Chrome/56.0.2924.76\
               Safari/537.36",
               "Upgrade-Insecure-Requests":"1",
               "Accept":"*/*",
               "Accept-Encoding":"gzip, deflate, sdch",
               "Accept-Language":"en-US,en;q=0.8",
               "Connection":"keep-alive"
              }
    cookies = None          # session cookies
    cookie_file = os.path.join(sys.path[0],"qzone_cookie")  # cookie file path
    session = None          # session object
    wb_name = None          # weibo name
    wb_password = None      # weibo password 
    home_url = "http://music.163.com"       # music home url
    # weibo api login url regular exp
    reg_login_url =\
            r"<a.*?href=\"(http://music.163.com/api/sns/authorize\?snsType=2.*?)\".*?</a>"

    # constructor function
    def __init__(self):
        os.chdir(sys.path[0])
        self.session = requests.session()

    # login function,by weibo user name and password
    def login(self,wb_name,wb_password):
        self.wb_name = wb_name
        self.wb_password = wb_password
        # set headers
        self.session.headers = self.headers
        # get login url
        r = self.session.get(self.home_url)
        login_url = re.findall(self.reg_login_url,r.text)
        if len(login_url) == 0:
            print("Cann't get weibo login url.")
            return -1
        r = self.session.get(login_url[0])
        print(r.text)
        print(r.url)
        print(r.history)
        print(r.history[0].headers)
        print(r.headers)


    # login function, by cookie
    def login_by_cookie(self):
        pass

if __name__ == "__main__":
    music163 = Music163()
    music163.login("","")

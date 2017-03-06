#!/usr/bin/python3
# -*- coding: utf-8 -*-
# login the qzone
# http qq+password ajax encryption
# Tencent login encryption flow is complex,
# so use cookie to login
# extra function:get qzone title and shuoshuo in the index page

import requests
import os
import sys
import re
from bs4 import BeautifulSoup

class Qzone(object):
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
    cookies = None          # cookies
    cookie_file = os.path.join(sys.path[0],"qzone_cookie")  # cookie file path
    session = None          # session object
    qq_number = None        # qq number
    qzone_url_pref = "http://user.qzone.qq.com/"     # qzone url prefix
    qzone_url = None                            # qzone url
    qzone_bsOjb = None
    title = None                                # qzone title

    def __init__(self):
        os.chdir(sys.path[0])
        self.session = requests.session()

    def login_by_cookie(self,qq_number):
        self.qq_number = qq_number
        self.qzone_url = self.qzone_url_pref + str(self.qq_number)
        if os.path.exists(self.cookie_file):
            with open(self.cookie_file,'r') as f:
                self.cookies = str(f.read())
            # cookie is a str other than a dict or json, user headers directly
            # headers value must not have no \n
            self.cookies = self.cookies.replace("\n","")
            self.headers['Cookie'] = self.cookies
            self.session.headers = self.headers
            print("Load cookies from %s successfully!" % self.cookie_file)
            r = self.session.get(self.qzone_url)
            print(r.url)
            if r.url == self.qzone_url:
                return 0
            else:
                print("Try to login %s failed. Test blocked" % self.qzone_url)
                return -1
        else:
            print("Can't find %s, please create it first!" % self.cookie_file)
            return -1

    def get_title(self):
        try:
            r = self.session.get(self.qzone_url)
            self.qzone_bsOjb = BeautifulSoup(r.text,"lxml")
            self.title = self.qzone_bsOjb.find("title").get_text().strip()
            return self.title
        except Exception as e:
            print(e)
            return None

    # get shuoshuo in index page, the content may has "查看全文"
    def get_shuoshuo(self):
        try:
            if self.qzone_bsOjb is None:
                r = self.session.get(self.qzone_url)
                self.qzone_bsOjb = BeautifulSoup(r.text,"lxml")
            sslist_tags = self.qzone_bsOjb.findAll("li",{"class":"f-single f-s-s"})
            sslist = []
            for sslist_tag in sslist_tags:
                ssentity = []
                ss_user =\
                sslist_tag.find("div",{"class":"f-nick"}).get_text().strip()
                ss_content =\
                sslist_tag.find("div",{"class":"f-info"}).get_text().strip()
                ssentity.append(ss_user)
                ssentity.append(ss_content)
                sslist.append(ssentity)
            return sslist
        except Exception as e:
            print(e)
            return None

if __name__ == "__main__":
    qzone = Qzone()
    print("Input your QQ number:")
    qq_number = input()
    if qzone.login_by_cookie(qq_number) == 0:
        print("Login successfully!")
    else:
        print("Login failed.")
        sys.exit()
    # get title
    qzone_title = qzone.get_title()
    if qzone_title is None:
        print("Get shuoshuo failed.")
    else:
        print("Your qzone title is: %s" % qzone_title)
    # get shuoshuo 
    qzone_sslist = qzone.get_shuoshuo()
    if qzone_sslist is None:
        print("Get shuoshuo failed.")
    else:
        print("Get shuoshuo successfull!.")
        ssid = 1
        for qzone_ssentity in qzone_sslist:
            print("[%s]" % str(ssid)
                  +qzone_ssentity[0]+":\t\t"+qzone_ssentity[1])
            ssid += 1

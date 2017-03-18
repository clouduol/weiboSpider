#!/usr/bin/python3
# -*- coding: utf-8 -*-
# login zhihu
# https email+password ajax
# extra function: get user nick name
import requests
import re
import time
import json
import os
import sys
import getpass

class Zhihu(object):
    # object data, public
    email = None         # user email
    password = None     # password
    xsrf = None         # xsrf value
    # xsrf regular expression
    reg_xsrf = r"<input.*?name=\"_xsrf\".*?value=\"(.*?)\".*?>"
    data = None         # login post data
    # request header
    # every request should set User-Agent;if user-Agent is requests default, response is 500
    headers={"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64;rv:51.0) Gecko/20100101 Firefox/51.0",
                  "Accept":"*/*",
                  "Accept-Language":"zh,en-US;q=0.7,en;q=0.3",
                  "Accept-Encoding":"gzip, deflate, br",
                  "Connection":"keep-alive"}
    session = None      # requests session
    index_url = "https://www.zhihu.com"                 # zhihu index url
    login_url = "https://www.zhihu.com/login/email"     # zhihu login url
    name = None           # user nick name
    # user name regular expression
    reg_name = r"<span\s+?class=\"name\"[^>]*?>(.*?)</span>"
    cookie_file = os.path.join(sys.path[0],".cookie_zhihu")    # file to store cookie
    cookies = None        # cookies

    def __init__(self):
        # change script directory as working directory
        os.chdir(sys.path[0])
        self.session = requests.session()
        self.session.headers = self.headers

    def login(self,email,password):
        self.email=email
        self.password=password
        self.data={"email":self.email,"password":self.password}
        # find _xsrf value
        r = self.session.get(self.index_url)
        self.xsrf = re.findall(self.reg_xsrf,r.text)
        if len(self.xsrf)==0:
            print("Error! Can't find _xsrf value")
            return -1
        self.xsrf=self.xsrf[0]
        self.data['_xsrf']=self.xsrf
        # time.sleep(5)
        r = self.session.post(self.login_url,data=self.data)
        ret_dict = eval(r.text)
        if ret_dict['r'] == 0:
            print("Congratulations, login successfully!")
            # store cookie, update in time
            self.__store_cookie()
            return 0
        elif ret_dict['errcode'] == 100005:
            print("Email or password error, try again.")
            return -1
        else:
            print("Someting wrong happened, login failed.")
            return -1

    def login_by_cookie(self):
        self.cookies = self.__load_cookie()
        if self.cookies is None:
            print("Load cookies error")
            return -1
        # set session cookie
        self.session.cookies.update(self.cookies)
        print("Load cookies from %s successfully!" % self.cookie_file)
        return 0

    def get_username(self):
        r = self.session.get(self.index_url)
        self.name = re.findall(self.reg_name,r.text)
        if len(self.name) == 0:
            print("Someting wrong happened, get user name failed.")
            return None
        else:
            self.name = self.name[0]
            print("Your nick name is: %s" % self.name)
            return self.name

    # Serialize cookie to file
    def __store_cookie(self):
        with open(self.cookie_file,'w') as f:
            cookies = self.session.cookies.get_dict()
            json.dump(cookies,f)
            print("Cookies stored into %s successfully!" % self.cookie_file)

    # Deserialize cookie from file
    def __load_cookie(self):
        if os.path.exists(self.cookie_file):
            with open(self.cookie_file,'r') as f:
                cookies = json.load(f)
                return cookies
        else:
            return None

    # if exists cookie file
    def find_cookie_file(self):
        if os.path.exists(self.cookie_file):
            return True
        else:
            return False

if __name__ == "__main__":
    zhihu = Zhihu()
    if zhihu.find_cookie_file():
        print("Login by cookie, please guarantee "+
             "it is within the effective period.")
        zhihu.login_by_cookie()
    else:
        print("Email:",end="")
        email = input()
        password = getpass.getpass("Password:")
        zhihu.login(email,password)
    zhihu.get_username()

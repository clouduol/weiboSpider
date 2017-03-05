#!/usr/bin/python3
# -*- coding: utf-8 -*-
# login zhihu
# https email+password
import requests
import re
import time

class Zhihu(object):
    # object data, public
    email = ""         # user email
    password = ""     # password
    xsrf = ""         # xsrf value
    # xsrf regular expression
    reg_xsrf = r"<input.*?name=\"_xsrf\".*?value=\"(.*?)\".*?>"
    data = ""         # login post data
    # request header
    # every request should set User-Agent;if user-Agent is requests default, response is 500
    headers={"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64;rv:51.0) Gecko/20100101 Firefox/51.0",
                  "Accept":"*/*",
                  "Accept-Language":"zh,en-US;q=0.7,en;q=0.3",
                  "Accept-Encoding":"gzip, deflate, br",
                  "Connection":"keep-alive"}
    session = ""      # requests session
    index_url = "https://www.zhihu.com"                 # zhihu index url
    login_url = "https://www.zhihu.com/login/email"     # zhihu login url
    name = ""           # user nick name
    # user name regular expression
    reg_name = r"<span\s+?class=\"name\"[^>]*?>(.*?)</span>"

    def __init__(self,email,password):
        self.email=email
        self.password=password
        self.data={"email":self.email,"password":self.password}
        self.session = requests.session()

    def login(self):
        # find _xsrf value
        r = self.session.get(self.index_url,headers=self.headers)
        print(r.url)
        print(r.request.headers)
        self.xsrf = re.findall(self.reg_xsrf,r.text)
        if len(self.xsrf)==0:
            print("Error! Can't find _xsrf value")
            return -1
        self.xsrf=self.xsrf[0]
        self.data['_xsrf']=self.xsrf
        print(self.data)
        # time.sleep(5)
        r = self.session.post(self.login_url,headers=self.headers,data=self.data)
        print(r.url)
        print(r.request.headers)
        print(r.text.__class__)
        print(r.text)
        ret_dict = eval(r.text)
        if ret_dict['r'] == 0:
            print("Congratulations, login successfully!")
            return 0
        elif ret_dict['errcode'] == 100005:
            print("Email or password error, try again.")
            return -1
        else:
            print("Someting wrong happened, login failed.")
            return -1

    def get_username(self):
        r = self.session.get(self.index_url,headers=self.headers)
        self.name = re.findall(self.reg_name,r.text)
        print(r.url)
        print(r.request.headers)
        print(self.name)
        if len(self.name) == 0:
            print("Someting wrong happened, get user name failed.")
            return None
        else:
            self.name = self.name[0]
            print("User nick name: %s" % self.name)
            return self.name

if __name__ == "__main__":
    print("Input your email:")
    email = input()
    print("Input your password:")
    password = input()
    zhihu = Zhihu(email,password)
    zhihu.login()
    zhihu.get_username()

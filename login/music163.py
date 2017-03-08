#!/usr/bin/python3
# -*- coding: utf-8 -*-
# login 163 music
# weibo(https+ ajax+ username/passowrd+ rsa) login

import requests
import re
import sys
import os
from bs4 import BeautifulSoup
import base64
import rsa
import binascii
import getpass

class Music163(object):
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
    cookie_file = os.path.join(sys.path[0],"music163_cookie")  # cookie file path
    session = None          # session object
    wb_name = None          # weibo name
    wb_password = None      # weibo password 
    home_url = "http://music.163.com"       # music home url

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
        # weibo login Referer, not necessary
        referer = self.getReferer()
        self.session.headers['Referer'] = referer
        # get su:username base64 code
        su = self.getSu(wb_name)
        # get pre login response parameter
        (servertime,nonce,pubkey,rsakv) = self.prelogin(su)
        # get sp:password rsa encryption result
        sp = self.getSp(wb_password,servertime,nonce,pubkey)
        wbapi_login_url =\
        "https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)&openapilogin=qrcode"
        wbapi_login_data = {"entry":"openapi",
                            "gateway":"1",
                            "from":"",
                            "savestate":"0",
                            "useticket":"1",
                            "pagerefer":"http://music.163.com/",
                            "ct":"1800",
                            "s":"1",
                            "vsnf":"1",
                            "vsnval":"",
                            "door":"",
                            "appkey":"u6BYq",
                            "su":su,
                            "service":"miniblog",
                            "servertime":servertime,
                            "nonce":nonce,
                            "pwencode":"rsa2",
                            "rsakv":rsakv,
                            "sp":sp,
                            "sr":"1377*768",
                            "encoding":"UTF-8",
                            "cdult":"2",
                            "domain":"weibo.com",
                            "prelt":"61",
                            "returntype":"TEXT"
                           }
        r = self.session.post(wbapi_login_url,data=wbapi_login_data)
        print(self.session.cookies)
        # retcode is "str"
        print(r.text)
        if eval(r.text)['retcode'] != '0':
            print("Login failed")
            return -1
        else:
            print("Congratulations, Login successfully!")
            r = self.session.get(self.home_url)
            print(r.request.headers)
            return 0
        print(sp)
        print(servertime)
        print(nonce)
        print(pubkey)
        print(rsakv)
        print(su)
        print(referer)

    # get weibo login Referer
    def getReferer(self):
        r = self.session.get(self.home_url)
        # weibo api login url regular exp
        reg_wblogin_url =\
                r"<a.*?href=\"(http://music.163.com/api/sns/authorize\?snsType=2.*?)\".*?</a>"
        wblogin_url = re.findall(reg_wblogin_url,r.text)
        if len(wblogin_url) == 0:
            print("Cann't get weibo login url in home page.")
            sys.exit()
        print(self.session.cookies)
        r = self.session.get(wblogin_url[0])
        print(self.session.cookies)
        return r.url

    # get su: weibo name base64 code
    def getSu(self,wb_name):
        return base64.b64encode(wb_name.encode("utf-8")).decode("utf-8")

    # prelogin
    def prelogin(self,su):
        params = {'checkpin': '1',
                  'entry': 'openapi',
                  'client':'ssologin.js(v1.4.18)',
                  'callback':'sinaSSOController.preloginCallBack',
                  'su': su,
                  'rsakt': 'mod'
                 }
        prelogin_url = \
                "https://login.sina.com.cn/sso/prelogin.php"
        r = self.session.get(prelogin_url,params = params)
        print(self.session.cookies)
        reg_prelogin = r"sinaSSOController\.preloginCallBack\((.*)\)"
        resp_dict = eval(re.findall(reg_prelogin,r.text)[0])
        # the retcode is "int"
        if resp_dict['retcode'] != 0:
            print("Prelogin response error happened")
            sys.exit()
        return (resp_dict['servertime'],resp_dict['nonce'],
                resp_dict['pubkey'],resp_dict['rsakv'])

    # get sp: pasword rsa encryption result
    def getSp(self,wb_password,servertime,nonce,pubkey):
        # set rsa public key
        pubkey = int(pubkey,16)
        # 65537 is the default e
        pubkey = rsa.PublicKey(pubkey,65537)
        # concatenate message to encrypt
        message = str(servertime)+"\t"+str(nonce)+"\n"+str(wb_password)
        # convert message to bytes
        message = message.encode('utf-8')
        sp = rsa.encrypt(message,pubkey)
        # convert to hex
        sp = binascii.b2a_hex(sp)
        return sp


    # login function, by cookie
    def login_by_cookie(self):
        pass

if __name__ == "__main__":
    music163 = Music163()
    print("weibo name: ",end="")
    wb_name = input()
    wb_password = getpass.getpass("weibo password: ")
    music163.login(wb_name,wb_password)

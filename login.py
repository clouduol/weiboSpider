#!/usr/bin/python3
# -*- coding: utf-8 -*-
# login sina weibo
# https + ajax + (username + base64)/(passowrd + rsa)

import requests
import re
import sys
import os
from bs4 import BeautifulSoup
import base64
import rsa
import binascii
import getpass
import json

class Login(object):
    # session headers
    headers = {"User-Agent":
               "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,\
               like\
               Gecko) Ubuntu Chromium/56.0.2924.76 Chrome/56.0.2924.76\
               Safari/537.36",
               "Accept":"*/*",
               "Accept-Encoding":"gzip, deflate, sdch",
               "Accept-Language":"en-US,en;q=0.8",
               "Connection":"keep-alive"
              }
    session = None          # session object
    wb_name = None          # weibo name
    wb_password = None      # weibo password 
    home_url = "https://weibo.com"       # weibo home url
    login_url = "https://login.sina.com.cn/sso/login.php"   # login url
    prelogin_url = "https://login.sina.com.cn/sso/prelogin.php" # prelogin url
    cookies = None          # session cookies
    cookie_file = os.path.join(os.getcwd(),".cookies_weibo")  # cookie file path

    # constructor function
    def __init__(self):
        # os.chdir(sys.path[0])
        self.session = requests.session()
        # set headers
        self.session.headers = self.headers

    # login function,by weibo user name and password
    def login_by_up(self,wb_name,wb_password):
        self.wb_name = wb_name
        self.wb_password = wb_password
        # get su:username base64 code
        su = self.getSu(wb_name)
        # get pre login response parameter
        (servertime,nonce,pubkey,rsakv) = self.prelogin(su)
        # get sp:password rsa encryption result
        sp = self.getSp(wb_password,servertime,nonce,pubkey)
        # weibo login, get ticket
        login_retcode = self.login(su,servertime,nonce,rsakv,sp)
        # print parameters, tuning parameter:0-don't print;other-print
        print_paras = 1
        if print_paras:
            print("================= parameters begin ================")
            print("su:\t"+str(su))
            print("sp:\t"+str(sp))
            print("servertime:\t"+str(servertime))
            print("nonce:\t"+str(nonce))
            print("pubkey:\t"+str(pubkey))
            print("rsakv:\t"+str(rsakv))
            print("cookies:\t"+str(self.session.cookies))
            print("================= parameters end  ================")
        if login_retcode == 0:
            print("Congratulations,Login successfully!")
            self.__store_cookie()
            return 0
        else:
            print("Some errors happened, Login failed.")
            return 1

    # prelogin
    def prelogin(self,su):
        params ={ 'entry': 'account',
                  'client':'ssologin.js(v1.4.15)',
                  'callback':'sinaSSOController.preloginCallBack',
                  'su': su,
                  'rsakt': 'mod'
                 }
        r = self.session.get(self.prelogin_url,params = params)
        print("prelogin")
        print(r.text)
        reg_prelogin = r"sinaSSOController\.preloginCallBack\((.*)\)"
        resp_dict = eval(re.findall(reg_prelogin,r.text)[0])
        # the retcode is "int"
        if resp_dict['retcode'] != 0:
            print("Prelogin response error happened")
            sys.exit()
        print("Weibo prelogin successfully...")
        return (resp_dict['servertime'],resp_dict['nonce'],
                resp_dict['pubkey'],resp_dict['rsakv'])

    # get su: weibo name base64 code
    def getSu(self,wb_name):
        return base64.b64encode(wb_name.encode("utf-8")).decode("utf-8")

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

    # weibo login
    def login(self,su,servertime,nonce,rsakv,sp):
        login_data = {"entry":"account",
                        "gateway":"1",
                        "from":"null",
                        "savestate":"30",
                        "useticket":"0",
                        "pagerefer":"",
                        "vsnf":"1",
                        "su":su,
                        "service":"account",
                        "servertime":servertime,
                        "nonce":nonce,
                        "pwencode":"rsa2",
                        "rsakv":rsakv,
                        "sp":sp,
                        "sr":"1366*768",
                        "encoding":"UTF-8",
                        "cdult":"3",
                        "domain":"sina.com.cn",
                        "prelt":"30",
                        "returntype":"TEXT"
                       }
        login_params = {"client":"ssologin.js(v1.4.15)"}
        r = self.session.post(self.login_url,params=login_params,data=login_data)
        print("login")
        print(r.text)
        # retcode is "str"
        resp_dict = eval(r.text)
        if resp_dict['retcode'] != '0':
            print("Weibo login error happened")
            return -1
        else:
            print("Weibo login successfully...")
            return 0

    # get evidence to confirm login successfully
    def getEvidence(self):
        #self.session.headers['User-Agent'] += 'googlebot'
        r = self.session.get(self.home_url)
        #print(r.text)
        try:
            re_nick = r"$CONFIG['nick']='(.*?)';"
            nick = re.findall(re_nick,r.text)
        except Exception as e:
            print("Exception found: %s " % e)
            return None
        if len(nick) == 1:
            return nick[0]
        else:
            print("Error found")
            return None

    # login function, by cookie
    def login_by_cookie(self):
        self.cookies = self.__load_cookie()
        if self.cookies is None:
            print("Load cookies error")
            return -1
        # set session cookie
        self.session.cookies.update(self.cookies)
        print("Load cookies from %s successfully!" % self.cookie_file)
        return 0

    # Serialize cookie to file
    def __store_cookie(self):
        with open(self.cookie_file,'w') as f:
            cookies = self.session.cookies.get_dict()
            json.dump(cookies,f)
            print("Cookies stored into %s successfully!" % self.cookie_file)

    # deserialize cookie from file
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
    if (len(sys.argv) > 2) or (len(sys.argv) == 2 and sys.argv[1] != "cookie"):
        print("Usage: python3 login.py [cookie]")
    wblogin = Login()
    login_retcode = 1
    if len(sys.argv) == 1:
        print("weibo name: ",end="")
        wb_name = input()
        wb_password = getpass.getpass("weibo password: ")
        login_retcode = wbLogin.login_by_up(wb_name,wb_password)
    else:
        if not wbLogin.find_cookie_file():
            print("Cannot find cookie file: %s" % wbLogin.cookie_file)
            sys.exit() 
        login_retcode=wbLogin.login_by_cookie()
    if login_retcode == 0:
        evidence=wbLogin.getEvidence()
        print("Evidence:")
        print("weibo nick name: %s" % evidence)

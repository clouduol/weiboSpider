#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import re

# urls
index_url = 'http://music.163.com'
login_163_url = ''
login_weibo_url_prefix = 'https://api.weibo.com'

# regular expressions
re_login_163 = \
r'<a.*?href="(http://music.163.com/api/sns/authorize\?snsType=2.*?)".*?</a>'
re_login_weibo = r'\n[^<]*<form.*?action="(.+?)".*?>'
re_login_hidden_input = \
r'<input\s+type="hidden"[^>]+?name="(.+?)"[^>]*?value="(.*?)".*?>'

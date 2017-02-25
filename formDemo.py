# using requests through form

import requests

# basic auth
from requests.auth import HTTPBasicAuth

auth = HTTPBasicAuth('Cloud','password')
r = requests.post("http://pythonscraping.com/pages/auth/login.php",auth=auth)
print(r.text)

## session cookie
#session = requests.session()
#
#params = {'username':'Wind','password':'password'}
#s = session.post("http://pythonscraping.com/pages/cookies/welcome.php",params)
#print("Cookie is set to:")
#print(s.cookies.get_dict())
#print("Headers are:")
#print(s.headers)
#print("------------------")
#print("Going to profile page...")
#s = session.get("http://pythonscraping.com/pages/cookies/profile.php")
#print(s.text)

## cookie 
#params = {'username':'Rain','password':'password'}
#r = \
#requests.post("http://pythonscraping.com/pages/cookies/welcome.php",data=params)
#print("Cookie is set to:")
#print(r.cookies.get_dict())
#print("-----------------")
#print("Going to profile page...")
#r =\
#requests.get("http://pythonscraping.com/pages/cookies/profile.php",cookies=r.cookies)
#print(r.text)

## simple form
#action_url = "http://pythonscraping.com/files/processing.php"
#data={"firstname":"Guo","lastname":"guess"}
#r = requests.post(action_url,data=data)
#print(r)
#print(r.text)

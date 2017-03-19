#!/usr/bin/python3
# -*- coding: utf-8 -*-
# clean data from wikipedia to n-grams format

import string
from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import OrderedDict
import re

# params
wiki_url = "https://en.wikipedia.org/wiki/FC_Barcelona"
grams_count = 2
print_count = 20

# functions

# cleanInput, return list, element:word
def cleanInput(input):
    #input = input.lower()           # avoid case sensitive
    input = re.sub('\n+'," ",input)     #'\n' to space
    input = re.sub('\[[0-9]*\]',"",input)  #delete reference, like [9]
    input = re.sub(' +'," ",input)      #multiple space to one
    input = bytes(input, 'utf-8')
    input = input.decode("ascii","ignore")  #remove unicode characters
    cleanInput = []
    input = input.split(" ")
    for item in input:
        item = item.strip(string.punctuation)   #delete punctuation
        # delete one letter word, except 'i' and 'a'
        if len(item)>1 or (item.lower()=='a' or item.lower()=='i'):
            cleanInput.append(item)
    return cleanInput

# getNparams, return dict, element:n <parames(str),count>
def getNparams(input,n):
    input = cleanInput(input)
    output = dict()
    for i in range(len(input)-n+1):
        ngram = " ".join(input[i:i+n])
        if ngram in output:
            output[ngram]+=1
        else:
            output[ngram]=1
    return output

# main function
html = urlopen(wiki_url)
bsObj = BeautifulSoup(html,"lxml")
content = bsObj.find("div",{"id":"mw-content-text"}).get_text()
ngrams = getNparams(content,grams_count)
# get ordered dict
ngrams = OrderedDict(sorted(ngrams.items(),key=lambda t:t[1], reverse = True))
print("The wiki page is: " + wiki_url)
print(str(grams_count)+"-grams count is: "+str(len(ngrams)))
i = 0
for item in ngrams.items():
    i+=1
    if i <= print_count:
        print(item)
    else:
        break

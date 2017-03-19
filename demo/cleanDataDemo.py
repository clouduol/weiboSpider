#!/usr/bin/python3
# -*- coding: utf-8 -*-
# clean data from wikipedia to n-grams format

import string
from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import OrderedDict
import re

# params
wiki_url = "https://en.wikipedia.org/wiki/Beijing"
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
        # filter common word
        if isCommon(input[i:i+n]):
            continue
        # update dict element
        ngram = " ".join(input[i:i+n])
        if ngram in output:
            output[ngram]+=1
        else:
            output[ngram]=1
    return output

# ngram(list) contains common word or not
def isCommon(ngram):
    commonWords = ["the", "be", "and", "of", "a", "in", "to", "have", "it",
                   "i", "that", "for", "you", "he", "with", "on", "do", "say",
                   "this", "they", "is", "an", "at", "but","we", "his", "from",
                   "that", "not", "by", "she", "or", "as", "what", "go",
                   "their","can", "who", "get", "if", "would", "her", "all",
                   "my", "make", "about", "know", "will","as", "up", "one",
                   "time", "has", "been", "there", "year", "so", "think",
                   "when", "which", "them", "some", "me", "people", "take",
                   "out", "into", "just", "see", "him", "your", "come",
                   "could", "now", "than", "like", "other", "how", "then",
                   "its", "our", "two", "more", "these", "want", "way", "look",
                   "first", "also", "new", "because", "day", "more", "use",
                   "no", "man", "find", "here", "thing", "give", "many",
                   "well","retrieved"]
    for word in ngram:
        if word.lower() in commonWords:
            return True
    return False

# get first sentence that contains ngram(str)
def getFirstSentence(ngram_str,content):
    sentences = content.split(".")
    for sentence in sentences:
        if ngram_str in sentence:
            return sentence
    return ""

# main function
html = urlopen(wiki_url)
bsObj = BeautifulSoup(html,"lxml")
content = bsObj.find("div",{"id":"mw-content-text"}).get_text()
ngrams = getNparams(content,grams_count)
# get sorted list
ngrams = sorted(ngrams.items(),key=lambda t:t[1], reverse = True)
print("The wiki page is: " + wiki_url)
print(str(grams_count)+"-grams count is: "+str(len(ngrams)))
print("Top +"+str(print_count)+" ngrams")
for i in range(print_count):
    print(ngrams[i])
print("Top 5 ngrams and their first sentence")
for i in range(5):
    print(ngrams[i][0]+" : "+getFirstSentence(ngrams[i][0],content))

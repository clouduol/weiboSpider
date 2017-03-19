#!/usr/bin/python3
# -*- coding: utf-8 -*-
# using inaugurationSpeech generate Markov model, then generate word by the
# model

from urllib.request import urlopen
from random import randint

# count word list sum
def wordListSum(wordList):
    sum = 0
    for word,value in wordList.items():
        sum+=value
    return sum

# random select next word by probability
def retrieveRandomWord(wordList):
    randIndex = randint(1,wordListSum(wordList))
    for word,value in wordList.items():
        randIndex -= value
        if randIndex <= 0:
            return word

# build word dict, nested dict
def buildWordDict(text):
    text = text.replace("\n"," ")
    text = text.replace("\"","")

    punctuation = [',','.',';',':']
    for symbol in punctuation:
        text = text.replace(symbol," "+symbol+" ")

    words = text.split(" ")
    words = [word for word in words if word != ""]

    wordDict = {}
    for i in range(1,len(words)):
        if words[i-1] not in wordDict:
            wordDict[words[i-1]] = {}
        if words[i] not in wordDict[words[i-1]]:
            wordDict[words[i-1]][words[i]] = 0
        wordDict[words[i-1]][words[i]] += 1

    return wordDict

# main func
text = \
str(urlopen("http://pythonscraping.com/files/inaugurationSpeech.txt").read(),'utf-8')
wordDict = buildWordDict(text)

length = 100
chain = ""
currentWord = "American"
chain += currentWord+" "
for i in range(length-1):
    currentWord = retrieveRandomWord(wordDict[currentWord])
    chain += currentWord+" "

print(chain)

#!/usr/bin/python3
# -*- coding:utf-8 -*-
# get weibo follow and fans
# use class Login

from login import *

class FollowFans(Login):
    # list unit:{'nick': , 'homeUrl': ,'fansCount': }
    followList = list()     # follow list
    fansList = list()       # fans list
    followCount = 0         # follow count
    fansCount = 0           # fans count
    ffHomeUrl = "https://weibo.cn"  # follow and fans home url

    # get follow
    # return follow count 
    def getFollow(self):
        followUrl = self.ffHomeUrl + "/" + self.wb_uid +"/follow"
        re_followCount = r"粉丝(.*?)人"
        page = 0
        while True:
            page += 1
            params={'page':str(page)}
            r = self.session.get(followUrl,params=params)
            bsObj = BeautifulSoup(r.text,"lxml")
            followTables = bsObj.findAll("table")
            if len(followTables) == 0:
                break
            #print("page"+str(page)+"\tcount:"+str(len(followTables)))
            for followTable in followTables:
                followUnit = dict()
                self.followCount += 1
                targetTag = followTable.find("td").next_sibling
                followUnit['nick'] = targetTag.find("a").get_text()
                followUnit['homeUrl'] = targetTag.find("a").attrs["href"]
                followUnit['fansCount'] = \
                        re.findall(re_followCount,targetTag.get_text())[0]
                self.followList.append(followUnit)
        return self.followCount

    # print follow
    def printFollow(self):
        print("Follow Count:\t" + str(self.followCount))
        for followUnit in self.followList:
            print("%s%s粉丝人数:%s" %(followUnit['nick'].ljust(40),\
                followUnit['homeUrl'].ljust(40),followUnit['fansCount'].ljust(20)))

    # get fans 
    # return fans count 
    def getFans(self):
        fansUrl = self.ffHomeUrl + "/" + self.wb_uid +"/fans"
        re_fansCount = r"粉丝(.*?)人"
        page = 0
        while True:
            page += 1
            params={'page':str(page)}
            r = self.session.get(fansUrl,params=params)
            bsObj = BeautifulSoup(r.text,"lxml")
            fansTables = bsObj.findAll("table")
            if len(fansTables) == 0:
                break
            #print("page"+str(page)+"\tcount:"+str(len(fansTables)))
            for fansTable in fansTables:
                fansUnit = dict()
                self.fansCount += 1
                targetTag = fansTable.find("td").next_sibling
                fansUnit['nick'] = targetTag.find("a").get_text()
                fansUnit['homeUrl'] = targetTag.find("a").attrs["href"]
                fansUnit['fansCount'] = \
                        re.findall(re_fansCount,targetTag.get_text())[0]
                self.fansList.append(fansUnit)
        return self.fansCount

    # print fans
    def printFans(self):
        print("Fans Count:\t" + str(self.fansCount))
        for fansUnit in self.fansList:
            print("%s%s粉丝人数:%s" %(fansUnit['nick'].ljust(40),\
                fansUnit['homeUrl'].ljust(40),fansUnit['fansCount'].ljust(20)))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print("Usage: python3 followFans.py")
        sys.exit()
    wbFF = FollowFans()
    login_retcode = 1
    print("weibo name: ",end="")
    wb_name = input()
    wb_password = getpass.getpass("weibo password: ")
    login_retcode = wbFF.login_by_up(wb_name,wb_password)
    if login_retcode == 0:
        wbFF.getFollow()
        wbFF.getFans()
        wbFF.printFollow()
        wbFF.printFans()

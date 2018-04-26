# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 10:56:58 2018

@author: u1562268


"""
#import packages
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import requests
import re
import time
import csv
import pprint as pp
import datetime
from collections import OrderedDict
import pandas
#############################################################
#first get the dates we are interested in
days = []
d1 = date(2010, 1, 1)  # start date
d2 = date(2017, 5, 31)  # end date

delta = d2 - d1         # timedelta

for i in range(delta.days + 1):
    days.append(d1 + timedelta(days=i))

##############################################################
browser=webdriver.Firefox()

BBC_list = []
DailyMail_list = []

#this function checks the page height, scrolls down, checks the height again and keeps scrolling if the height has increased
def twt_scroller(url):
    browser.get(url)    
    #define initial page height for 'while' loop
    lastHeight = browser.execute_script("return document.body.scrollHeight")    
    while True:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #define how many seconds to wait while dynamic page content loads
        time.sleep(2)
        newHeight = browser.execute_script("return document.body.scrollHeight")        
        if newHeight == lastHeight:
            break
        else:
            lastHeight = newHeight            
    html = browser.page_source
    return html

base_url_bbc = 'https://twitter.com/search?l=&q=from%3ABBCNews%20since%3A'
base_url_dailymail = 'https://twitter.com/search?l=&q=from%3ADailyMailUK%20since%3A'


try:
    for x in range(1,len(days)):
    
        page = base_url_bbc + str(days[x-1]) + '%20until%3A' + str(days[x]) + '&src=typd&lang=en-gb'
        print(x)
        
        soup = BeautifulSoup(twt_scroller(page),"lxml")
        tweets = soup.findAll('li',{"class":'js-stream-item'})
        for tweet in tweets:
            if tweet.find('p',{"class":'tweet-text'}):
                tweet_date= tweet.find('a', title = True, class_ = 'tweet-timestamp')['title']
                tweet_text = tweet.find('p',{"class":'tweet-text'}).text.encode('utf8').strip()
                replies = tweet.find('span',{"class":"ProfileTweet-actionCount"}).text.strip()
                retweets = tweet.find('span', {"class" : "ProfileTweet-action--retweet"}).text.strip()
                tweetdict = {
                "Date" : tweet_date,
                "Text" : tweet_text,
                "No_replies" : replies,
                "No_retweets" : retweets
                }
        
                BBC_list.append(tweetdict)
            else:
                continue
except (AttributeError, TypeError, KeyError, ValueError):
    print("missing_value")

alldates = []
alltexts = []
allreplies = []
allretweets = []
for y in range(len(BBC_list)):
   alldates.append(BBC_list[y]['Date'])
   alltexts.append(BBC_list[y]['Text'])
   allreplies.append(BBC_list[y]['No_replies'])
   allretweets.append(BBC_list[y]['No_retweets'])
   
df = pandas.DataFrame(data={"Dates": alldates, "Texts": alltexts, "Replies": allreplies, "Retweets": allretweets})
df.to_csv("./BBC_data.csv", sep=',',index=False)
        
        
        


try:
    for x in range(1,len(days)):
    
        page = base_url_dailymail + str(days[x-1]) + '%20until%3A' + str(days[x]) + '&src=typd&lang=en-gb'
        print(x)
        
        soup = BeautifulSoup(twt_scroller(page),"lxml")
        tweets = soup.findAll('li',{"class":'js-stream-item'})
        for tweet in tweets:
            if tweet.find('p',{"class":'tweet-text'}):
                tweet_date= tweet.find('a', title = True, class_ = 'tweet-timestamp')['title']
                tweet_text = tweet.find('p',{"class":'tweet-text'}).text.encode('utf8').strip()
                replies = tweet.find('span',{"class":"ProfileTweet-actionCount"}).text.strip()
                retweets = tweet.find('span', {"class" : "ProfileTweet-action--retweet"}).text.strip()
                tweetdict = {
                "Date" : tweet_date,
                "Text" : tweet_text,
                "No_replies" : replies,
                "No_retweets" : retweets
                }
        
                DailyMail_list.append(tweetdict)
            else:
                continue
except (AttributeError, TypeError, KeyError, ValueError):
    print("missing_value")

alldates = []
alltexts = []
allreplies = []
allretweets = []
for y in range(len(DailyMail_list)):
   alldates.append(DailyMail_list[y]['Date'])
   alltexts.append(DailyMail_list[y]['Text'])
   allreplies.append(DailyMail_list[y]['No_replies'])
   allretweets.append(DailyMail_list[y]['No_retweets'])
   
df = pandas.DataFrame(data={"Dates": alldates, "Texts": alltexts, "Replies": allreplies, "Retweets": allretweets})
df.to_csv("./DailyMail_data.csv", sep=',',index=False)































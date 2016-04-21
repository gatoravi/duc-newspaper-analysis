#!/usr/bin/env python

import praw
from bs4 import BeautifulSoup
import newspaper
from random import randint
import re
import requests
import sys

#http://stackoverflow.com/questions/6883049/regex-to-find-urls-in-string-in-python
URL_REGEX = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

def create_date(year, month, day):
    return year + "-" + month + "-" + day

n_days_per_year = 2
n_days = 0
years = ["2015"]
seen_dates = {}
for year in years:
    while n_days < n_days_per_year:
        month = str(randint(1, 12))
        day = str(randint(1, 28))
        date = create_date(year, month, day)
        if date in seen_dates:
            next
        n_days += 1
        seen_dates[date] = 1
        out_file = date + ".txt"
        f_out = open(out_file, "w")
        print("date is " + date)
        url = "http://www.thehindu.com/todays-paper/tp-index/?date=" + date
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")
        tpaper = soup.find_all("div", class_="tpaper")
        tpaper_links = re.findall(URL_REGEX,str(tpaper))
        for count, tpaper_link in enumerate(tpaper_links):
            print "Article number: " + str(count)
            if count == 100:
                break
            article = newspaper.Article(tpaper_link)
            article.download()
            article.parse()
            text = re.sub("\n", " ", article.text)
            text = text + "\n"
            f_out.write(text.encode('utf-8'))

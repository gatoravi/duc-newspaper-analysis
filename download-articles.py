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

years = ["2015"]
for year in years:
    month = str(randint(1, 12))
    day = str(randint(1, 28))
    date = create_date(year, month, day)
    out_file = date + ".txt"
    f_out = open(out_file, "w")
    print("date is " + date)
    url = "http://www.thehindu.com/todays-paper/tp-index/?date=" + date
    r = requests.get(url)
    soup = BeautifulSoup(r.text,"lxml")
    tpaper = soup.find_all("div", class_="tpaper")
    print(tpaper)
    tpaper_links = re.findall(URL_REGEX,str(tpaper))
    for count, tpaper_link in tpaper_links:
        if count == 100:
            break
        print(count)
        print(tpaper_link)
        article = newspaper.Article(tpaper_link)
        article.download()
        article.parse()
        print(article.text)
        f_out.write(str(article.text))

"""
user_agent = "DUC newspaper analysis 1.0"
r = praw.Reddit(user_agent=user_agent)
domain = r.get_domain_listing('thehindu.com', sort='new', limit=1000)
urls = [x.url for x in domain]
print("\nGot {:d} urls\n".format(len(urls)))

print ("Fetching url: {}\n".format(urls[0]))
article = newspaper.Article(urls[0])
article.download()
article.parse()

print ("Here's the raw text:\n")
print(article.text)
"""

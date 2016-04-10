#!/usr/bin/env python

import praw
import newspaper

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

from __future__ import print_function, division
import pprint, os, json, logging, codecs
from datetime import datetime, timedelta

import requests
import newspaper
from lxml import html

pp = pprint.PrettyPrinter(indent=4)
logging.basicConfig(
    format="%(levelname) -10s %(asctime)s %(message)s",
    level=logging.INFO
)

class Downloader(object):
    def __init__(self, root_dump_path="/tmp"):
        self.base_url = 'http://www.thehindu.com'
        self.root_dump_path = root_dump_path
        self.log = logging.getLogger('Downloader.' + __name__)

    def get_paper_index(self, date_time):
        contents = self.fetch_index_page(date_time)
        news_links = self.get_news_links(contents)
        index = self.classify_news_links(news_links)
        return index

    def classify_news_links(self, links):
        data = {}

        for url in links:
            details = url.split('/', 4)[-1]
            organization = details.split('/')
            section = 'front-page'
            subsection = None

            # figure out the proper section/subsection
            if ( len(organization) > 2 ):
                section = organization[0].split('-', 1)[1]
                if section == 'national' or section == 'features':
                    if len(organization) == 4:
                        subsection = organization[1].split('-')[1]
                    else:
                        subsection = 'general'

            # add the url into the proper place in the dictionary
            if section in data:
                if subsection in data[section]:
                    data[section][subsection].append(url)
                else:
                    data[section][subsection] = [url]
            else:
                data[section] = {}
                data[section][subsection] = [url]

        return data

    def get_news_links(self, contents):
        tree = html.fromstring(contents)
        links = tree.xpath('//div[@class="tpaper"]/a/@href')
        #pp.pprint(links)
        return links

    def fetch_index_page(self, date_time):
        url = os.path.join( self.base_url, 'todays-paper/tp-index/')
        date = date_time.strftime("%Y-%m-%d")
        payload = { 'date' : date }
        r = requests.get(url, params=payload)
        if r.status_code != 200:
            msg = ("Got a {} code ".format(r.status_code),
                   "on fetching the index page for date '{}'".format(date))
            self.log.critical(msg)
            sys.exit(' '.join(msg))
        return r.content

    def dump_articles(self,
            start="2016-01-01", end="2016-01-03",
            section="sports", subsection=None):
        self.ensure_path(self.root_dump_path)
        time_range = self.collect_date_range(start, end)

        self.log.info("section: {} | subsection: {}".format(section, subsection))

        for day in time_range:
            self.log.info("Day: {}".format(day.strftime("%Y-%m-%d")))
            news = self.get_section_links(day, section, subsection)
            self.log.info("Got {} news links".format(len(news)))

            i = 1
            for link in news:
                self.log.info("({}) Processing: {}".format(i, link))
                article = self.get_article(link)
                self.dump_article(article, day, section, subsection)
                i += 1

        self.log.info("All Done!")

    def get_section_links(self, day, section, subsection):
        index = self.get_paper_index(day)
        links = index[section][subsection]
        return links

    def get_article(self, link):
        article = newspaper.Article(link)
        article.download()
        article.parse()
        return article

    def dump_article(self, article, day, section, subsection):
        date = day.strftime("%Y-%m-%d")
        location = os.path.join(self.root_dump_path, date, section)
        if subsection is not None:
            location = os.path.join(location, subsection)

        self.ensure_path(location)

        # strip out odd characters in the title
        name = unicode(article.title.encode('utf-8'), errors='ignore')
        name = ''.join(c for c in name if c not in ',./')

        filename = os.path.join(
            location,
            u"{}.json".format(name.replace(' ', '-')).encode('utf-8'),
        )

        data = {
            'date' : date,
            'section' : section,
            'subsection' : subsection,
            'title' : article.title.encode('utf-8'),
            'author' : article.authors,
            'text' : article.text.encode('utf-8'),
        }

        self.log.info("Dumping article to: {}".format(filename))
        with open(filename, 'w') as f:
            f.write(json.dumps(data, indent=4))

    def collect_date_range(self, start, end):
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")

        range = []
        day = start_date
        oneday = timedelta(days=1)

        while day != end_date :
            range.append(day)
            day = day + oneday

        return range

    def ensure_path(self, path):
        if not os.path.exists(path):
            self.log.info("Creating directory: {}".format(path))
            os.makedirs(path)


if __name__ == '__main__':
    d = Downloader("/tmp/duc-newspaper-analysis")
    d.dump_articles(
        start="2016-01-01",
        end="2016-01-03",
        section="sports",
        subsection=None,
    )
#    day = datetime.strptime('2016-01-02', '%Y-%m-%d')
#    index = d.get_paper_index(day)
#    print(json.dumps(index, indent=4))

# http://stackoverflow.com/questions/4531995/getting-attribute-using-xpath

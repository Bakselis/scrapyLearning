# This spider will scrape the data from json files
# found in http://www.trumptwitterarchive.com/archive page
import json
from scrapy import Spider

class JsonSpiderSpider(Spider):
    name = 'json_spider'
    allowed_domains = ['http://www.trumptwitterarchive.com']
    start_urls = [
    'http://www.trumptwitterarchive.com/data/realdonaldtrump/2019.json',
    'http://d5nxcu7vtzvay.cloudfront.net/data/realdonaldtrump/2018.json'
    ]

    def parse(self, response):
        jsonresponse = json.loads(response.body)

        for tweet in jsonresponse:
            yield {
                'Created_at': tweet['created_at'],
                'Text'      : tweet['text']
            }

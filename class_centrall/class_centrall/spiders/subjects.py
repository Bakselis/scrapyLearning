# Programm for scrapping the data from classcentral.com website
# If the specific subject is set, programm will scrape just the courses of the subject that is set
# If the subject is not provided, programm will scrape all subjects

from scrapy import Spider
from scrapy.http import Request

class SubjectsSpider(Spider):
    name = 'subjects'
    allowed_domains = ['classcentral.com']
    start_urls = ['http://classcentral.com/subjects']

    def __init__(self, subject=None):
        self.subject = subject

    def parse(self, response):
        if self.subject:
            # finding the url for specific subject
            self.logger.info("Scrapping {}".format(self.subject))
            url = response.xpath('//*[contains(@title, "{}")]/@href'.format(self.subject)).extract_first()
            yield Request(response.urljoin(url), callback=self.parse_subject)
        else:
            # finding the url for all subjects
            self.logger.info("Scrapping every subject")
            urls = response.xpath('//*[@class="head-3 large-up-head-2 text--bold block"]/../@href').extract()
            for url in urls:
                yield Request(response.urljoin(url), callback=self.parse_subject)


    def parse_subject(self, response):
        subject_title = response.xpath('//title/text()').extract_first().split(" | ")[0]

        courses_block = course_div = response.xpath('//a[contains(@class, "course-name")]')

        for course_block in courses_block:
            url = course_block.xpath('.//@href').extract_first()
            name = course_block.xpath('.//text()').extract_first()

            yield {
                'Course_name' : name,
                'Course_url'  : url,
                'Subject_title': subject_title
            }

        next_page = response.xpath('//*[@rel="next"]/@href').extract_first()

        yield Request(response.urljoin(next_page), callback=self.parse_subject)

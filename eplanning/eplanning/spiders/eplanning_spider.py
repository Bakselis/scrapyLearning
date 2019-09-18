# This is a spider that will go to all categories in page http://www.eplanning.ie/
# Then selects the "Received Applications"
# Then selects 14 days in the form
# Then goes into intem page and checks does the agent button is one the page
# If the button does exist in the page, the data will be scraped
from scrapy import Spider
from scrapy.http import Request, FormRequest

class EpanningSpider(Spider):
    name = 'eplanning_spider'
    allowed_domains = ['eplanning.ie']
    start_urls = ['http://www.eplanning.ie/']

    def parse(self, response):
        urls = response.xpath('//a/@href').extract()
        for url in urls:
            # some a tags have # in them, so they need to be filtered out
            if '#' == url:
                pass
            else:
                yield Request(url, callback=self.parse_app)

    def parse_app(self, response):
        app_url = response.xpath('//*[@class="glyphicon glyphicon-inbox btn-lg"]/following-sibling::a/@href').extract_first()
        yield Request(response.urljoin(app_url), callback=self.parse_form)

    def parse_form(self, response):
        yield FormRequest.from_response(response,
                                        formdata={ 'RdoTimeLimit': '14',},
                                        dont_filter=True,
                                        formxpath='(//form)[2]',
                                        callback=self.parse_pages)
    def parse_pages(self, response):
        rows = response.xpath('.//table/tr')[1:]
        for row in rows:
            url = row.xpath('.//a/@href').extract_first()
            yield Request(response.urljoin(url), callback=self.parse_page)

        next_url = response.xpath('//*[@rel="next"]/@href').extract_first()
        yield Request(response.urljoin(next_url), callback=self.parse_pages)


    def parse_page(self, response):
        agent_btn = response.xpath('//*[@value="Agents"]/@style').extract_first("")
        if 'display: inline;  visibility: visible;' in agent_btn:
            name = response.xpath('//tr[th="Name :"]/td/text()').extract_first()

            address_first = response.xpath('//tr[th="Address :"]/td/text()').extract()
            address_second = response.xpath('//tr[th="Address :"]/following-sibling::tr/td/text()').extract()[0:3]

            address = address_first + address_second

            phone = response.xpath('//tr[th="Phone :"]/td/text()').extract_first()

            fax = response.xpath('//tr[th="Fax :"]/td/text()').extract_first()

            email = response.xpath('//tr[th="e-mail :"]/td/a/text()').extract_first()

            url = response.url

            yield {'name': name,
                   'address': address,
                   'phone': phone,
                   'fax': fax,
                   'email': email,
                   'url': url}
        else:
            self.logger.info('No agent button on the page')

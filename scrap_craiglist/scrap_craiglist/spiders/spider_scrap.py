# -*- coding: utf-8 -*-
import scrapy


class SpiderScrapSpider(scrapy.Spider):
    name = 'spider_scrap'
    allowed_domains = ['sfbay.craigslist.org']
    start_urls = ['https://sfbay.craigslist.org/search/egr']

    def parse(self, response):
        # jobs_postings = response.xpath('//a[@class="result-title hdrlnk"]/text()').extract()
        # for jobs in jobs_postings:
        #     # print (jobs)
        #     yield{'Listing ' : jobs}
        list_items = response.xpath('//li[@class="result-row"]')
        for item in list_items:
            date = item.xpath('.//*[@class="result-date"]/@datetime').extract_first()
            link = item.xpath('.//a[@class="result-title hdrlnk"]/@href').extract_first()
            position = item.xpath('.//a[@class="result-title hdrlnk"]/text()').extract_first()
            # print (date)
            # print (position)
            # print (link)
            yield{'Date' : date,
                  'Position' : position,
                  'Link' : link
            }

        next_page_url = response.xpath('//a[text()="next > "]/@href').extract_first()
        if next_page_url:
            print (response.urljoin(next_page_url))
            yield scrapy.Request(response.urljoin(next_page_url),callback=self.parse)

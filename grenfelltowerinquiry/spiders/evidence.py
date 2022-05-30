from urllib.parse import urljoin
from scrapy.loader import ItemLoader
from grenfelltowerinquiry.items import GrenfellEvidenceItem
import scrapy

class GrenfellEvidenceSpider(scrapy.Spider):
    name = 'evidence'
    allowed_domains = ['www.grenfelltowerinquiry.org.uk']
    start_urls = ['http://www.grenfelltowerinquiry.org.uk/evidence']

    def parse(self, response):
        for hearing_item in response.xpath('//li[@class="hearing-item top-border-box"]'):
            yield scrapy.Request(urljoin(response.url, hearing_item.xpath('.//a/@href').get()), callback=self.parse_hearingitem)

        next_page_url = response.xpath('//li[@class="pager__item pager__item--next"]/a/@href').get()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

    def parse_hearingitem(self, response):
        item_loader = ItemLoader(item=GrenfellEvidenceItem(), response=response)
        item_loader.add_xpath('title', '//h1[@class="page-title"]/span/text()')
        item_loader.add_xpath('date', '//time[@class="datetime"]/text()')
        item_loader.add_xpath('witness', '//span[@class="content-item-label" and contains(text(), \'Witness:\')]/parent::div/text()')
        item_loader.add_xpath('item_type', '//span[@class="content-item-label" and contains(text(), \'Type:\')]/parent::div/text()')
        item_loader.add_xpath('url', '//span[contains(concat(\' \', @class, \' \'), \' file \')]/a/@href')
        return item_loader.load_item()

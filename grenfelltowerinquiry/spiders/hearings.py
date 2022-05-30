"""This module contains a spider for Grenfell hearings."""

from urllib.parse import urljoin
import re
import scrapy
from scrapy.loader import ItemLoader
from grenfelltowerinquiry.items import GrenfellHearingItem

class GrenfellHearingSpider(scrapy.Spider):
    """
    A scrapy spider for Grenfell hearings.
    """
    name = 'hearings'
    allowed_domains = ['www.grenfelltowerinquiry.org.uk']
    start_urls = ['http://www.grenfelltowerinquiry.org.uk/hearings']
    youtube_pattern = re.compile(r'https://www.youtube.com/embed/(...........)')

    def parse(self, response, **kwargs):
        for hearing_url in response.xpath(
                '//li[@class="hearing-item top-border-box"]/a/@href').getall():
            sub_url = urljoin(response.url, hearing_url)
            req = scrapy.Request(sub_url, callback=self.parse_hearingitem)
            yield req

        next_page_url = response.xpath('//li[@class="pager__item pager__item--next"]/a/@href').get()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

    def parse_hearingitem(self, response):
        """
        Parse a hearing item.
        """
        item_loader = ItemLoader(item=GrenfellHearingItem(), response=response)
        item_loader.add_xpath(
                'title',
                '//h1[@class="page-title"]/span/text()'
                )
        item_loader.add_xpath(
                'date',
                '//time[@class="datetime"]/@datetime'
                )
        item_loader.add_xpath(
                'witnesses',
                '//div[contains(text(), \'Witnesses\')]/following-sibling::div/div/a/text()'
                )
        item_loader.add_value(
                'hearing_urls',
                self.parse_videoembed(
                    response.xpath('//div/@data-video-embed-field-lazy')
                    .getall()
                    )
                )
        item_loader.add_xpath(
                'transcript_urls',
                '//div[contains(text(), \'Transcripts\')]' +
                '/following-sibling::div/div/span[contains(concat(\' \', @class, \' \'),' +
                '\' file \')]/a/@href'
                )
        yield item_loader.load_item()

    def parse_videoembed(self, items):
        """
        Parse some data containing youtube urls.
        """
        if items is not None:
            return ["https://youtube.com/watch?v=" +
                    word for word in self.youtube_pattern.findall(''.join(items))]
        return None

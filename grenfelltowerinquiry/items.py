# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from itemloaders.processors import MapCompose
import scrapy

class GrenfellEvidenceItem(scrapy.Item):
    title = scrapy.Field()
    date = scrapy.Field()
    witness = scrapy.Field(input_processor=MapCompose(str.strip))
    item_type = scrapy.Field(input_processor=MapCompose(str.strip))
    url = scrapy.Field()

class GrenfellHearingItem(scrapy.Item):
    page_url = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    witnesses = scrapy.Field(input_processor=MapCompose(str.strip))
    hearing_urls = scrapy.Field()
    transcript_urls = scrapy.Field()

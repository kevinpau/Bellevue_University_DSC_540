# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# class ScrapyspiderItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass

class EmojiSpiderItem(scrapy.Item):
    emoji_handle = scrapy.Field()
    emoji_image = scrapy.Field()
    section = scrapy.Field()


class PythonPackageItem(scrapy.Item):    
    package_name = scrapy.Field()
    version_number = scrapy.Field()
    package_downloads = scrapy.Field()
    package_page = scrapy.Field()
    package_short_description = scrapy.Field()
    home_page = scrapy.Field()
    python_versions = scrapy.Field()
    last_month_downloads = scrapy.Field()

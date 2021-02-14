# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os

from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
import hashlib
from scrapy.utils.python import to_bytes
from image_scraper.settings import IMAGES_STORE


class ImageScraperPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for url in item['image_urls']:
            yield Request(url, meta={'folder': item['folder']})

    def file_path(self, request: Request, response=None, info=None, *, item=None):
        folder = request.meta['folder']
        image_store = os.path.join(IMAGES_STORE, folder)
        if not os.path.exists(image_store):
            os.mkdir(image_store)
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return os.path.join(image_store, image_guid) + '.jpg'


class ImageGeneratorPipeline:

    def process_item(self, item, spider):
        return item

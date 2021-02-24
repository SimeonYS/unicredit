import re

import scrapy

from scrapy.loader import ItemLoader
from ..items import UnicreditItem
from itemloaders.processors import TakeFirst
pattern = r'(\xa0)?'

class UnicreditSpider(scrapy.Spider):
	name = 'unicredit'
	start_urls = ['https://www.unicreditbulbank.bg/bg/blog/?page=1']

	def parse(self, response):
		post_links = response.xpath('//h2[@class="entry-title blog__post__content-title"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//li[@class="page next"]/a/@href').get()
		if next_page:
			yield response.follow(next_page, self.parse)


	def parse_post(self, response):

		date = response.xpath('//ul[@class="blog__inner__layer__header__icons list-inline"]/li/span//text()').get()
		title = response.xpath('//h1[@class="blog__inner__layer__header__title"]/text()').get().strip()
		content = response.xpath('//div[@class="entry-content"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))


		item = ItemLoader(item=UnicreditItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		return item.load_item()

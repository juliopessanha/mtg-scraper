import scrapy
import json
import os

class QuotesSpider(scrapy.Spider):
    name = "mtg_crawler"
    start_urls = [
        'https://scryfall.com/sets',
    ]

    def parse(self, response):
        set_pages = response.css('td.flexbox a::attr(href)').getall()
        
        for set_link in set_pages:
            if set_link is not None:
                yield response.follow(set_link, callback=self.set_parse)
                break
        
    def set_parse(self, response):
        card_links = response.css('div.card-grid-item a::attr(href)').getall()
        for card_page in card_links:
            if card_page is not None:
                yield response.follow(card_page, callback=self.get_card)
                #break

    def get_card(self, response):
        #print("entering")
        card_json = response.css('script::text').getall()[-1]
        yield json.loads(card_json)

    def closed(self, reason):
        # will be called when the crawler process ends
        folder_path = os.path.abspath("./").replace("mtg_scrapper", "")
        os.system('python3 %stransform_mtg_data.py' % folder_path)
    
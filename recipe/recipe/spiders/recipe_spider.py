# -*- coding:utf-8 -*-

import re
from bs4 import BeautifulSoup
from scrapy.spider import Spider
from scrapy.selector import Selector, HtmlXPathSelector
from scrapy.contrib.spiders import SitemapSpider, CrawlSpider
from scrapy.http import Request
from recipe.items import RecipeItem, PageItem



# From mapadelsition: level_1 tipo level_2 receta
# mongo structure idea: entrante/receta.foto/elaboracion/ingredientes


class BaseSpider(Spider):
    allowed_domains = ["www.1080recetas.com"]

    def parse_item(self, response):
        sel = Selector(response)
        item = RecipeItem()
        item["title"] = sel.xpath('//h1[@class="contentheading"]/a/text()').extract() # Cleansing is made on the pipeline
        item['category'] = sel.xpath('//span[@class="article-section"]/a/text()').extract()
        item["link"] = response.url
        item["date"] = sel.xpath('//span[@class="createdate"]/text()').extract()
        item["image_urls"] = [ "http://"+self.allowed_domains[0]+sel.xpath('//div[@class="article-content"]/img/@src').extract()[0] ]
        # In test (and maybe code) check if links ends up with jpg or equivalent
        item["description"] = sel.xpath('//div[@class="article-content"]/p[1]/text()').extract()
        item["ingredients"] = sel.xpath('//div[@class="article-content"]/ul/li//text()').extract() # Unordered
        item["elaboration"] = sel.xpath('//div[@class="article-content"]/ol/li/text()').extract() # Ordered
        item['tips'] = ''.join(sel.xpath('//div[@class="article-content"]/p[strong/text()="Consejos:"]/following-sibling::p[1]//text()').extract()).strip()
        # PENDING IMPORTANT additional texts after Consejos
        # PENDING Facebook commentaries, votes
        return item   

class PageSpider(BaseSpider): # PENDING transform into a Unit test
    name = "one"
    start_urls = ["http://www.1080recetas.com/recetas/entrantes/1362-receta-gratis-cocina-pan-cebolla-pipas-santa-rita-harinas"]

    def parse(self, response):
        sel = Selector(response)
        item = self.parse_item(response)
        return item 

class RecipesSpider(BaseSpider): # PENDING transform into a Unit test
    name = "recipes"
    start_urls = ["http://www.1080recetas.com/mapa-del-sitio"]

    def parse(self, response):
        sel = Selector(response)
        pages = sel.xpath('//ul/li/a/@href').extract()         # FILTER <ul class="level_2"> <li><a href=regex9recetas/.+)>
        for url in pages: # PENDING check filter listing pages like entrantes, ensaladas ...
            if re.match("/recetas/.+/.+", url ) is not None: # parses only recipe pages, not listings pages
                yield Request('http://'+self.allowed_domains[0]+url, callback=self.parse_recipe)
            elif re.match("http://www.1080recetas.com/recetas/.+/.+", url ):
                yield Request(url, callback=self.parse_recipe)

    def parse_recipe(self, response):
        item = self.parse_item(response)
        return item

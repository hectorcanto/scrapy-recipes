# -*- coding:utf-8 -*-

import re
from scrapy import log
from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.selector import Selector
from recipe.items import RecipeItem, PageItem

class BaseSpider(Spider):
    """ 
    Base class for standalone and complete crawling.
    """
    allowed_domains = ["www.1080recetas.com"]

    def parse_item(self, response):
        sel = Selector(response)
        item = RecipeItem()
        item["title"] = sel.xpath('//h1[@class="contentheading"]/a/text()').extract() # Cleansing is made on the pipeline
        item['category'] = sel.xpath('//span[@class="article-section"]/a/text()').extract()
        item["link"] = response.url
        item["date"] = sel.xpath('//span[@class="createdate"]/text()').extract()
        images = sel.xpath('//div[@class="article-content"]//img/@src').extract() # // before image to extract links in and outside <p>
        item["image_urls"] = []

        log.msg("Extracted image links {0}".format(images), level=log.DEBUG)
        for path in images:
            if "stories" in path:
                if "http" in path:
                    item["image_urls"].append(path)
                else:
                    item["image_urls"].append("http://"+self.allowed_domains[0]+path) # PENDING Transform properly
        log.msg("Number of paths:{1} -- Resulting path {0}".format( item["image_urls"], len(item["image_urls"])))
                
        item["description"] = sel.xpath('//div[@class="article-content"]/p[1]/text()').extract()
        item["ingredients"] = sel.xpath('//div[@class="article-content"]/ul/li//text()').extract() # Unordered
        item["elaboration"] = sel.xpath('//div[@class="article-content"]/ol/li/text()').extract() # Ordered
        item['tips'] = ''.join(sel.xpath('//div[@class="article-content"]/p[strong/text()="Consejos:"]/following-sibling::p[1]//text()').extract()).strip() # ISSUE some tips are not retrieved properly
        # PENDING IMPORTANT additional texts after "Consejos"
        # PENDING Facebook commentaries, votes
        return item   

class PageSpider(BaseSpider): 
    """
    Class specially designed for testing by crawling a single page. It could be used as a single page crawler.
    """

    name = "one"
    start_urls = ["http://www.1080recetas.com/recetas/entrantes/1362-receta-gratis-cocina-pan-cebolla-pipas-santa-rita-harinas"]

    # PENDING transform into a Unit test and a one-page crawler script

    def parse(self, response):
        sel = Selector(response)
        item = self.parse_item(response)
        return item 

class RecipesSpider(BaseSpider):
    """
    Spider to crawl over all the recipes in 1080recetas.com.
    """

    name = "recipes"
    start_urls = ["http://www.1080recetas.com/mapa-del-sitio"]

    # PENDING stablish rules to filter links

    def parse(self, response):
        sel = Selector(response)
        pages = sel.xpath('//ul/li/a/@href').extract()  
        for url in pages: 
            if re.match("/recetas/.+/.+", url ) is not None: # Parses only recipe pages, not listings pages
                yield Request('http://'+self.allowed_domains[0]+url, callback=self.parse_recipe) # Ensures absolute link

            elif re.match("http://www.1080recetas.com/recetas/.+/.+", url ):
                yield Request(url, callback=self.parse_recipe)

    def parse_recipe(self, response):
        item = self.parse_item(response) # uses base class method
        return item

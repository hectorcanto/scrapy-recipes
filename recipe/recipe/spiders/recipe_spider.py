from scrapy.spider import Spider
from scrapy.selector import Selector
from recipe.items import RecipeItem, PageItem
from scrapy.contrib.spiders import SitemapSpider, CrawlSpider
from scrapy.http import Request
import re
# From mapadelsition: level_1 tipo level_2 receta
# mongo structure idea: entrante/receta.foto/elaboracion/ingredientes


class FirstSpider(Spider):
    name = "first"
    allowed_domains = ["www.1080recetas.com"]
    start_urls = [
        #"http://www.1080recetas.com/recetas",
        "http://www.1080recetas.com/mapa-del-sitio"
    ]
    
    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//ul/li')
        items = []
        for site in sites:
            #PENDING filter links not in /recetas"
            item = PageItem()
            item['title'] = site.xpath('a/text()').extract()
            item['link'] = site.xpath('a/@href').extract()
            items.append('item')
            #item['desc'] = site.xpath('text()').extract()
            
        print "Scraped",len(items)
        #for item in items:
        #    print item['title'], item.['link']
        return items


class PageSpider(Spider): # PENDING transform into a Unit test
    name = "one"
    allowed_domains = ["www.1080recetas.com"]
    start_urls = ["http://www.1080recetas.com/recetas/entrantes/1362-receta-gratis-cocina-pan-cebolla-pipas-santa-rita-harinas"]

    def parse(self, response):
        sel = Selector(response)
        title = sel.xpath('//h1[@class="contentheading"]/a/text()').extract() # PENDING strip
        item = RecipeItem()
        item["title"] = sel.xpath('//h1[@class="contentheading"]/a/text()').extract() # PENDING strip
        item["link"] = response.url
        item["photo"] = sel.xpath('//div[@class="article-content"]/img/@src').extract() # PENDING extract image instead of relative link
        # In test (and maybe code) check if links ends up with jpg or equivalent
        
        item["description"] = sel.xpath('//div[@class="article-content"]').extract() # PENDING sanitize, order and divide into pieces
        #item["description"] = sel.xpath('//div[@class="article-content"]/p/text()').extract() # PENDING divide into pieces
        return item
        
        #item["ingredients"] = # PENDING stora as an array
        # item["elaboration"] =
        # item["category"] = sel.xpath('//span[@class="article-section"]/a/text()).extract()
        # PENDING fields like commentaries, votes, category ... also date        

        # <span class="createdate">Lunes, 21 de Abril de 2014 00:00</span>
	# <span class="article-section"><a href="/recetas/entrantes">Entrantes</span>
        # div class="article-content">     # <strong>Ingredientes:</strong></p> list
        # <p><strong>Elaboracion:</strong></p> # <p><strong>Consejos:</strong></p>


class RecipeSpider(CrawlSpider):
    name = "recipes"
    allowed_domains = ["www.1080recetas.com"]
    start_urls = ["http://www.1080recetas.com/mapa-del-sitio"]

    def parse(self, response):
        sel = Selector(response)
        pages = sel.xpath('//ul/li/a/@href').extract()         # FILTER <ul class="level_2"> <li><a href=regex9recetas/.+)>
        for url in pages: # PENDING check filter listing pages like entrantes, ensaladas ...
            if re.match("/recetas/.+/.+", url ) is not None: # parses only recipe pages, not listings pages
                yield Request('http://'+self.allowed_domains[0]+url, callback=self.parse_recipe)

    def parse_recipe(self, response):
        sel = Selector(response)
        title = sel.xpath('//h1[@class="contentheading"]/a/text()').extract() # PENDING strip

class MapSpider(SitemapSpider):
    name = "sitemap"
    allowed_domains = ["www.1080recetas.com"]
    sitemap_urls = ["http://www.1080recetas.com/mapa-del-sitio"]
    #sitemap_rules = [ ("/recetas/.+", self.parse_recipe) ]

    def parse(self, response):
        sel = Selector(response)
        for h3 in sel.xpath('//h3').extract():
            yield MyItem(title=h3)

        for url in sel.xpath('//a/@href').extract():
            yield Request(url, callback=self.parse)


    def parse_recipe(self, response):
        sel = Selector(response)
        sites = sel.xpath('//ul/li')
        items = []
        for site in sites:
            #PENDING filter links not in /recetas"
            item = RecipeItem()
            item['title'] = site.xpath('a/text()').extract()
            item['link'] = site.xpath('a/@href').extract()
            items.append('item')
            #item['desc'] = site.xpath('text()').extract()
        print "Scraped",len(items)
        for item in items:
            print item['title'], item['link']

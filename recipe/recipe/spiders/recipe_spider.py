from scrapy.spider import Spider
from scrapy.selector import Selector
from recipe.items import RecipeItem

class RecipeSpider(Spider):
    name = "recipes"
    allowed_domains = ["www.1080recetas.com"]
    start_urls = [
        #"http://www.1080recetas.com/recetas",
        "http://www.1080recetas.com/mapa-del-sitio"
    ]

# From mapadelsition: level_1 tipo level_2 receta
# Estructura mongo: entrante/receta.foto/elaboracion/ingredientes

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
        return items

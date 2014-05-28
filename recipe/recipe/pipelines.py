import PIL as pil
import locale
from datetime import datetime

class RecipePipeline(object):
    def process_item(self, item, spider):
        item = self.clean_fields(item)
        image = self.download_photo(item['photo']) # MAYBE transform into BSON?
        item['photo'] = image
        item = self.transform_date(item)
        return item

    def download_photo(self, link): # Transform into standalone Pipeline class 
        # check type
        # transform into jpg rgb with PIL
        return link
    
    def clean_fields(self, item):
        item['title'] = item['title'][0].strip()
        item['category']= item['category'][0].strip()
        item["date"] = item["date"][0].strip() # PENDING transform into datetime
        return item

    def transform_date(self, item):
        locale.setlocale(locale.LC_ALL, "es_ES.UTF-8")
        item["date"]= datetime.strptime(item["date"], "%A, %d de %B de %Y %H:%M")
        return item

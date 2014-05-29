import locale
from PIL import Image
from os import path
from datetime import datetime
from pymongo import MongoClient
from bson.binary import Binary as BsonBinary

from scrapy import log
from recipe.settings import IMAGES_STORE



class RecipePipeline(object):
    def process_item(self, item, spider):
        item = self.clean_fields(item)
        return item
    
    def clean_fields(self, item):
        item['title'] = item['title'][0].strip()
        item['category']= item['category'][0].strip()
        item['date'] = self.transform_date(item['date'][0].strip())
        return item

    def transform_date(self, date):
        locale.setlocale(locale.LC_ALL, "es_ES.UTF-8")
        dt = datetime.strptime(date.encode('utf8'), "%A, %d de %B de %Y %H:%M") # string encoding to include names with accents
        return dt

class BinaryPipeline(object):

    def process_item(self, item, spider):
        try:
            image_path = path.join(IMAGES_STORE, item['images'][0]['path'])
            jpg = Image.open(image_path)
            jpg.seek(0)
            binary = BsonBinario(jpg.tobytes()) 
            #item["photo"] = binary
            return item
        except:
            return item

class MongoPipeline(object):

    def __init__(self):
        self.connection = MongoClient('localhost', 27017)
        self.database = self.connection['recipes_db']
        self.collection = self.database['recipes']
        
    def process_item(self, item, spider):
        # transform image into binary
        image_path = path.join(IMAGES_STORE, item['images'][0]['path'])
        jpg = Image.open(image_path)
        jpg.seek(0)
        binary = BsonBinary(jpg.tobytes())           
        item["photo"] = binary

        mapped = dict(item)
        for key in ['images', 'image_urls', 'photo']:
            mapped.pop(key)
        mapped['timestamping'] = datetime.utcnow()    
        identifier = self.collection.insert(mapped, continue_on_erro=True)
        log.msg("Element inserted with ID {0}".format(identifier))

        return item

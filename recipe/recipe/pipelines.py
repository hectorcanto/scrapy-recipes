import locale
from os import path
from datetime import datetime

from scrapy import log
from recipe.settings import IMAGES_STORE
from pymongo import MongoClient
import gridfs
from bson.binary import Binary as BsonBinary

class RecipePipeline(object):
    """
    Cleaning the fields for a better visualization and more efficient storage. Also transform fields into proper Python objects if necessary.
    """
    def process_item(self, item, spider):
        item = self.clean_fields(item)
        return item
    
    def clean_fields(self, item):
        item['title'] = item['title'][0].strip()
        item['category']= item['category'][0].strip()
        item['date'] = self.transform_date(item['date'][0].strip())
        # PENDING cleaning paragraphs
        return item

    def transform_date(self, date):

        locale.setlocale(locale.LC_ALL, "es_ES.UTF-8")
        dt = datetime.strptime(date.encode('utf8'), "%A, %d de %B de %Y %H:%M") # string encoding to include names with accents
        return dt

class MongoPipeline(object):
    """
    Adapt the item for MongoDB storing. Adding indexing and key fields.
    """

    def __init__(self):
        self.connection = MongoClient('localhost', 27017)
        self.database = self.connection['recipes_db']
        self.collection = self.database['recipes']
        self.fs = gridfs.GridFS(self.database)
        
    def process_item(self, item, spider):
        """
        Map RecipeItem into a dict with valuable fields and useful information
        _id : link
        number: recipe number, got from the link
        image: gridFS ID for the JPG file
        text_fields: title, description, elaboration, ingredients and tips
        """

        # PENDING store more than one image

        mapped = dict(item)
        for key in ['images', 'image_urls', 'link']:
            mapped.pop(key)
        mapped['timestamp'] = datetime.utcnow() # For updating or duplicate control purposes
        mapped['_id'] = item['link']
        mapped['number'] = int(item['link'].split("/")[5].split("-")[0]) # For an easier manual retrieval

        # Single image storing
        if len(item['images']):
            image_path = path.join(IMAGES_STORE, item['images'][0]['path']) 
            image_data = open(image_path, 'r')
            mapped['image'] = self.fs.put(image_data) # stores image ID in filesystem

        identifier = self.collection.insert(mapped, continue_on_error=True)
        log.msg("Element inserted with ID {0}".format(identifier))
        return item

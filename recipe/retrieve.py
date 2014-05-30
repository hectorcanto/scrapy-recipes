from pymongo import MongoClient
import gridfs
from PIL import Image

class ItemRetriever(object):

    def __init__(self):
        self.connection = MongoClient('localhost', 27017)
        self.database = self.connection['recipes_db']
        self.collection = self.database['recipes']
        self.fs = gridfs.GridFS(self.database)

    def ReturnItemByNumber(self, number):
        """
        Number should be in int, of be valid for an int cast.
        In case there is no match return None.
        """
        cursor = self.collection.find( { u'number':int(number) } )
        item =self.ReturnItem(cursor)
        return item

    def ReturnItemByLink(self, link):
        """
        Links must be in string format starting with with http://www 
        """
        cursor = self.collection.find( { u'_id': link } )
        item =self.ReturnItem(cursor)
        return item
        
    def ReturnItem(self, cursor):
        if not cursor.count():
            return None
        return list(cursor)[0]

    def ShowImageByNumber(self, number):
        item  = self.ReturnItemByNumber(number)
        image_data = self.fs.get(item['image'])
        if image_data:
            image = Image.open(image_data)
            image.show()
        else:
            print "Sorry, no image avaliable"

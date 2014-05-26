# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class PageItem(Item):
    title = Field()
    link = Field()


class RecipeItem(Item):
    title = Field() # title of the page / recipe
    category = Field() # Entrantes ...
    link = Field() # link to the recipe
    photo = Field() # Maybe link to the image first
    votes = Filed() # Number of votes
    qualification = Field() # Vote Average
    description = Field()
    elaboration = Field()
    ingredients = Field() # PENDING array
    commentaries = Field() # PENDING array

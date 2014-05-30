from scrapy.item import Item, Field

class PageItem(Item): # Obsolete, due for removing
    title = Field()
    link = Field()

class RecipeItem(Item):
    title = Field() # title of the page / recipe
    date = Field() # in Spanish in text format, later datetime
    category = Field() # Entrantes, Postres ...
    link = Field() # link to the recipe
    image_urls = Field() # MANDATORY for ImagesPipeline
    images = Field() # MANDATORY for ImagesPipeline
    description = Field()
    elaboration = Field()
    ingredients = Field()
    tips = Field() # PENDING handle missing paragraph

    # PENDING additional, scrap extra text after mandatory fields
    #votes = Field() # Number of votes
    #qualification = Field() # Vote Average
    #commentaries = Field() # PENDING array, if any


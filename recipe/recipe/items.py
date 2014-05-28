from scrapy.item import Item, Field

class PageItem(Item):
    title = Field()
    link = Field()

class RecipeItem(Item):
    title = Field() # title of the page / recipe
    date = Field() # text, later datetime
    category = Field() # Entrantes ...
    link = Field() # link to the recipe
    photo = Field() # link or photo
    description = Field()
    elaboration = Field()
    ingredients = Field()
    tips = Field() # PENDING hanle missing paragraph
    # PENDING additional, scrap extra text after mandatory fields

    #votes = Field() # Number of votes
    #qualification = Field() # Vote Average
    #commentaries = Field() # PENDING array, if any


# Scrapy settings for recipe project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'recipe'

SPIDER_MODULES = ['recipe.spiders']
NEWSPIDER_MODULE = 'recipe.spiders'

ITEM_PIPELINES = {
    'recipe.pipelines.RecipePipeline': 100,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'recipe (+http://www.yourdomain.com)'

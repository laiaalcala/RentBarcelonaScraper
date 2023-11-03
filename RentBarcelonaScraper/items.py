
import scrapy


class RentBarcelonaItem(scrapy.Item):
    
    Price= scrapy.Field()
    Size= scrapy.Field()
    Rooms= scrapy.Field()
    Baths= scrapy.Field()
    Zone=scrapy.Field()
    pass

import scrapy 
import re 
from RentBarcelonaScraper.items import RentBarcelonaItem

class FeatureSpider(scrapy.Spider):
	name= 'features' 
	start_urls= ['https://www.pisos.com/alquiler/pisos-barcelona/'] 


	def parse(self,response):
		items =RentBarcelonaItem()
		
		# Precios
		prices= response.css(".ad-preview__price::text").extract()
		items['Price']= [price.strip() for price in prices if price.strip()]
		
		# Número de habitaciones
		rooms= response.css(".p-sm:nth-child(1)::text").extract()
		items['Rooms']= [re.search(r'\d+', room).group(0) if room else '' for room in rooms] # Guardamos solo el número
		
		# Tamaño
		sizes= response.css(".p-sm:nth-child(3)::text").extract()
		items['Size']= sizes
		
		# Zona
		zonas= response.css(".ad-preview__title+ .p-sm::text").extract()
		items['Zone']= zonas
		
		return items

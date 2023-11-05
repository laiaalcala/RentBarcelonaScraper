import scrapy 
import re 
from RentBarcelonaScraper.items import RentBarcelonaItem
from scrapy.http import TextResponse
import json
import csv
#from selenium import webdriver

class FeatureSpider(scrapy.Spider):
	name= 'features' 
	start_urls= ['https://www.pisos.com/alquiler/pisos-barcelona'] 
	data = []
	def parse(self,response):
		#driver = webdriver.Chrome()
		#items =RentBarcelonaItem()
		#container alquiler
		containers = response.css(".ad-preview").extract()
		next_page = response.css('.pagination__next a::attr(href)').extract_first()
		for container in containers:
			# Encuentra un elemento en la página por su selector CSS (cambia esto por el selector adecuado)
			#elemento = driver.find_element_by_css_selector('.ad-preview')
			#print(elemento)
			# Haz clic en el elemento
			#elemento.click()
			# Crear un objeto de respuesta a partir de la cadena de contenido
			container_response = TextResponse(body=container, url=response.url, encoding='utf-8')
			 # Utiliza una expresión XPath para seleccionar el elemento div con el atributo data-lnk-href
			div_element = container_response.xpath('//div[@data-lnk-href]')

			# Extrae el valor del atributo data-lnk-href
			data_lnk_href = div_element.xpath('@data-lnk-href').extract_first()
			# Si hay un enlace, sigue el enlace para ver la información necesaria, caso contrario extraera la información basica de la pagina principal
			if data_lnk_href:
				yield response.follow(data_lnk_href, callback=self.parse_pagina_vinculada)
			else:
				price = container_response.css(".ad-preview__price::text").extract_first()
				rooms = container_response.css(".ad-preview__info .ad-preview__section:nth-child(3) .p-sm:nth-child(1)::text").extract_first()
				bathrooms = container_response.css(".ad-preview__info .ad-preview__section:nth-child(3) .p-sm:nth-child(2)::text").extract_first()
				size = container_response.css(".ad-preview__info .ad-preview__section:nth-child(3) .p-sm:nth-child(3)::text").extract_first()
				characteristics = container_response.css(".ad-preview__info .ad-preview__section:nth-child(3) .p-sm:nth-child(4)::text").extract_first()
				image = container_response.css(".carousel__main-photo img::attr(src)").extract_first()
				address = container_response.css(".p-sm:nth-child(2)::text").extract_first()
				#Objeto con la información correspondiente
				dataObject = {
					"address": address,
					"price": price,
					#"price_m2": price_m2,
					"bathrooms": bathrooms,
					#"size_construction": size_construction,
					"size": size,
					"rooms": rooms,
					#"description": description,
					#"planta": planta,
					#"exterior": exterior,
					#"preservation": preservation,
					#"floor_type": floor_type,
					#"last_updated": date
				}
				self.data.append(dataObject)



		next_page = response.css('.pagination__next a::attr(href)').extract_first()
		if next_page:
			yield response.follow(next_page, self.parse)

	def parse_pagina_vinculada(self, response):
		date = response.css(".updated-date::text").extract_first()
		owner = response.css(".owner-data-info a::text").extract_first() 
		description = response.css(".description-body::text").extract_first()
		#Datos basicos
		price_m2 = response.css(".basicdata-info .basicdata-item:nth-child(5)::text").extract_first()
		price = response.css(".jsPrecioH1::text").extract_first()
		address = response.css(".position::text").extract_first()
		size_construction = response.css(".charblock-list:nth-child(1) .charblock-element:nth-child(1) span:nth-child(2)::text").extract_first()
		size = response.css(".charblock-list:nth-child(1) .charblock-element:nth-child(2) span:nth-child(2)::text").extract_first()
		rooms = response.css(".charblock-list:nth-child(1) .charblock-element:nth-child(3) span:nth-child(2)::text").extract_first()
		bathrooms = response.css(".charblock-list:nth-child(1) .charblock-element:nth-child(4) span:nth-child(2)::text").extract_first()
		planta = response.css(".charblock-list:nth-child(1) .charblock-element:nth-child(5) span:nth-child(2)::text").extract_first()
		exterior = response.css(".charblock-list:nth-child(1) .charblock-element:nth-child(6) span:nth-child(2)::text").extract_first()
		preservation = response.css(".charblock-list:nth-child(1) .charblock-element:nth-child(7) span:nth-child(2)::text").extract_first()
		# Muebles y acabados
		floor_type = response.css(".charblock-list:nth-child(2) .charblock-element:nth-child(1) span:nth-child(2)::text").extract_first()
		# Gallery images
		#ul = response.css(".gallery-carousel-item").extract()
		#print(ul)
		#images = []
		#for li in ul.css('.gallery-carousel-item'):
		#	img_src = li.css('img::attr(src)').extract_first()
		#	print(img_src)
		#	images.push(img_src)


		dataObject = {
			"owner": owner,
			"address": address,
			"price": price,
			"price_m2": price_m2,
			"bathrooms": bathrooms,
			"size_construction": size_construction,
			"size": size,
			"rooms": rooms,
			"description": description,
			"planta": planta,
			"exterior": exterior,
			"preservation": preservation,
			"floor_type": floor_type,
			"last_updated": date
			#"images": ul
		}
		self.data.append(dataObject)
    
	def closed(self, reason):
	# Escribir el objeto JSON en un archivo externo
		with open('result.json', 'w') as json_file:
			json.dump(self.data, json_file, indent=2)

		# Escritura de los resultados en archivo csv
		# Obrir un arxiu CSV en mode d'escriptura
		with open('result.csv', 'w', newline='') as archivo_csv:
			# Encabezado del csv basado en los keys del json
			encabezados = self.data[0].keys()

			# Crea un objeto csv.DictWriter
			escritor = csv.DictWriter(archivo_csv, fieldnames=encabezados)

			# Escritura de los encabezados
			escritor.writeheader()

			# Escritura de los datos en el csv
			for fila in self.data:
				escritor.writerow(fila)
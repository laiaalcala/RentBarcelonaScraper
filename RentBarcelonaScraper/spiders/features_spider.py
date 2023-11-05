import scrapy 
import re 
from RentBarcelonaScraper.items import RentBarcelonaItem
from scrapy.http import TextResponse
import json
import csv

class FeatureSpider(scrapy.Spider):
	name= 'features' 
	start_urls= ['https://www.pisos.com/alquiler/pisos-barcelona'] 

	data = []
	def parse(self,response):
		#items =RentBarcelonaItem()
		#container alquiler
		containers = response.css(".ad-preview").extract()
		next_page = response.css('.pagination__next a::attr(href)').extract_first()
		for container in containers:
			# Crear un objeto de respuesta a partir de la cadena de contenido
			container_response = TextResponse(body=container, url=response.url, encoding='utf-8')
			price = container_response.css(".ad-preview__price::text").extract_first()
			rooms = container_response.css(".ad-preview__info .ad-preview__section:nth-child(3) .p-sm:nth-child(1)::text").extract_first()
			bathrooms = container_response.css(".ad-preview__info .ad-preview__section:nth-child(3) .p-sm:nth-child(2)::text").extract_first()
			size = container_response.css(".ad-preview__info .ad-preview__section:nth-child(3) .p-sm:nth-child(3)::text").extract_first()
			characteristics = container_response.css(".ad-preview__info .ad-preview__section:nth-child(3) .p-sm:nth-child(4)::text").extract_first()
			image = container_response.css(".carousel__main-photo img::attr(src)").extract_first()
			address = container_response.css(".p-sm:nth-child(2)::text").extract_first()
			#Objeto con la información correspondiente
			mi_lista = {
				"address": address,
				"price": price,
				"bathrooms": bathrooms,
				"size": size,
				"rooms": rooms,
				"characteristics": characteristics,
				"image": image,
				"next_page": next_page,
			}
			self.data.append(mi_lista)

		next_page = response.css('.pagination__next a::attr(href)').extract_first()
		if next_page:
			yield response.follow(next_page, self.parse)

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
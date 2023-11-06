# tipologia-y-ciclo-de-vida-de-los-datos-PRA1
## Integrantes del Grupo
- Laia Alcalà (https://github.com/laiaalcala)
- Fernando Roque (https://github.com/tfrc19)
## Descripción del Repositorio

Este repositorio es un proyecto desarrollado con Scrapy (https://scrapy.org/) en Python. Su principal objetivo es la extracción de datos relacionados con el alquiler de viviendas en la ciudad de Barcelona, y estos datos se obtienen del sitio web https://www.pisos.com.

El proceso de extracción de datos es exhaustivo, ya que abarca la recopilación de información de toda la plataforma web. Como resultado, se generan dos archivos de salida: uno en formato JSON y otro en formato CSV. Estos archivos incluyen una variedad de detalles relevantes sobre las ofertas de alquiler de viviendas, como precios, ubicaciones, características de las propiedades, información del propietario, y mucho más.

## Ejecución
Para ejecutar el proyecto es necesario tener instalado las siguientes librerias (Paquetes):
```python
  import scrapy
  import json
  import csv
```
Comando de ejecución
```bash
  scrapy crawl features
```

La ejecución del proyecto dará como resultado la creación de dos archivos que albergarán de manera completa toda la información recopilada a través del proceso de web scraping. Estos archivos funcionan como una valiosa fuente de datos que captura exhaustivamente los detalles extraídos de la web.

```
result.csv
result.json
```
***Resultado***
```json
  [
    {
        "owner": "Inmuebles LDP",
        "address": "El Camp de l'Arpa del Clot (Distrito Sant Mart\u00ed. Barcelona Capital)",
        "price": "1.550€",
        "price_m2": "30€",
        "bathrooms": "1 Baño",
        "size_construction": ": 40m2",
        "size": "34m2",
        "rooms": "1 Hab",
        "description": "Información relevante",
        "planta": "Planta baja",
        "exterior": "Terraza",
        "preservation": "En buen estado",
        "last_updated": "Actualizado el 05/11/2023"
      }
  ]
```

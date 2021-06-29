# REST_API HTTP SERVER 

### Сервер запускается следующим образом: python3 script.py


* Перед запуском HTTP-сервера необходимо установить зависимости среды: (команда pip install -r requirements.txt).

* Программа работает с базой данных.

* В программе реализованы как основные задания, так и дополнительные.

* Программа включает покрытие тестами.

### По адресу http://127.0.0.1:8000/api/<название_метода> cервер предоставляет REST API сервис, принимающий запросы в формате json и предоставляющий методы:

#### 1. getinfo	- метод, принимающий идентификатор geonameid и возвращающий информацию о локации.

##### Пример:
 ######  Запрос:
	
        {
            "geo_id": 451750
        }
		
######   Ответ:
	
        {
            "geonameid": 451750,
            "name": "Zhitovo",
            "asciiname": "Zhitovo",
            "alternatenames": "",
            "latitude": "57.29693",
            "longitude": "34.41848",
            "feature class": "P",
            "feature_code": "PPL",
            "country_code": "RU",
            "cc2": "",
            "admin1_code": "77",
            "admin2_code": "",
            "admin3_code": "",
            "admin4_code": "",
            "population": 0,
            "elevation": "",
            "dem": 247,
            "timezone": "Europe/Moscow",
            "modification_date": "2011-07-09"
        }

#### 2. getpage - метод, принимающий страницу и количество отображаемых на странице локаций и возвращающий
 Cписок городов с их информацией. Отсчет страниц начинается с 0.

##### Пример:
###### Запрос:
	
        {
            "page":1,
            "items_value":2
        }

######   Ответ:
	
         [
            {
                "geonameid": 451747,
                "name": "Zyabrikovo",
                "asciiname": "Zyabrikovo",
                "alternatenames": "",
                "latitude": "56.84665",
                "longitude": "34.7048",
                "feature class": "P",
                "feature_code": "PPL",
                "country_code": "RU",
                "cc2": "",
                "admin1_code": "77",
                "admin2_code": "",
                "admin3_code": "",
                "admin4_code": "",
                "population": 0,
                "elevation": "",
                "dem": 204,
                "timezone": "Europe/Moscow",
            "modification_date": "2011-07-09"
            },
            {
                "geonameid": 451748,
                "name": "Znamenka",
                "asciiname": "Znamenka",
                "alternatenames": "",
                "latitude": "56.74087",
                "longitude": "34.02323",
                "feature class": "P",
                "feature_code": "PPL",
                "country_code": "RU",
                "cc2": "",
                "admin1_code": "77",
                "admin2_code": "",
                "admin3_code": "",
                "admin4_code": "",
                "population": 0,
                "elevation": "",
                "dem": 215,
                "timezone": "Europe/Moscow",
                "modification_date": "2011-07-09"
            }
        ]

#### 3. getcomparison - метод, принимающий названия двух локаций (на русском языке) и возвращающий:
    1) информацию о найденных городах
    2) название локации, расположенной севернее другой
    3) количество часов, на которое различаются временные зоны

##### Пример:
######  Запрос:
	
        {
            "geo_1":"Озеро Сяркиярви",
            "geo_2":"Явидово"
        }
		
######  Ответ:
	
        {
        "geo_1": {
            "geonameid": 12121691,
            "name": "Ozero Syarkiyarvi",
            "asciiname": "Ozero Syarkiyarvi",
            "alternatenames": [
                "Ozero Sjarkijarvi",
                "Озеро Сяркиярви"
            ],
            "latitude": "61.72219",
            "longitude": "30.51401",
            "feature class": "H",
            "feature_code": "LK",
            "country_code": "RU",
            "cc2": "",
            "admin1_code": "28",
            "admin2_code": "",
            "admin3_code": "",
            "admin4_code": "",
            "population": 0,
            "elevation": "",
            "dem": 78,
            "timezone": "Europe/Moscow",
            "modification_date": "2020-01-11"
        },
        "geo_2": {
            "geonameid": 451769,
            "name": "Yavidovo",
            "asciiname": "Yavidovo",
            "alternatenames": [
                "Javidovo",
                "Явидово"
            ],
            "latitude": "56.87068",
            "longitude": "34.51994",
            "feature class": "P",
            "feature_code": "PPL",
            "country_code": "RU",
            "cc2": "",
            "admin1_code": "77",
            "admin2_code": "",
            "admin3_code": "",
            "admin4_code": "",
            "population": 0,
            "elevation": "",
            "dem": 217,
            "timezone": "Europe/Moscow",
            "modification_date": "2012-01-16"
        },
        "compares": {
            "northern geo": "Ozero Syarkiyarvi",
            "northern latitude": "61.72219",
            "timezones_difference": "0.0"
        }
    }
	
#### 4. hintname - метод принимающий часть названия города и возвращающий ему подсказку с возможными вариантами продолжений

##### Пример:
######    Запрос:
	
        {
            "hint": "Yasnaya"
        }
		
   ###### Ответ:
	
        [
            "Les Yasnaya Polyana",
            "Balka Ryasnaya",
            "Razvaliny Yasnaya Polyana",
            "Stantsiya Yasnaya",
            "Myasnaya",
            "Yasnaya Zor’ka",
            "Bol’shaya Myasnaya",
            "Yasnaya Polyana",
            "Yasnaya Zvezda",
            "Yasnaya-Polyana",
            "Urochishche Sladko-Ryasnaya Plavnya",
            "Yasnaya Zor'ka",
            "Ostanovochnyy Punkt Yasnaya",
            "Ostanovochnyy Punkt Yasnaya Polyana",
            "Pionerlager' Yasnaya Polyana",
            "Lager’ Otdykha Yasnaya Polyana",
            "Detskiy Lager’ Yasnaya Polyana",
            "Yasnaya",
            "Bol'shaya Myasnaya",
            "Gora Yasnaya",
            "Lager' Otdykha Yasnaya Polyana",
            "Stantsiya Yasnaya Polyana",
            "Urochishche Yasnaya Polyana",
            "Pionerlager’ Yasnaya Polyana",
            "Yasnaya Zarya",
            "Detskiy Lager' Yasnaya Polyana"
        ]   

from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)

port = '8000'

app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db_path = 'geo_info_ru.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path

test_db_path = '/tests/geo_info_ru_sample.db'

ru_txt_path = 'db/database_creation/databases_in_txt/RU.txt'
timezones_txt_path = 'db/database_creation/databases_in_txt/timezones.txt'

ru_txt_sample_path = '../tests/test_txt_validation/ru_sample.txt'

request_keys = {
    'geoinfo': ('geo_id',),
    'getpage': ('page', 'items_value'),
    'getcomparison': ('geo_1', 'geo_2'),
    'hintname': ('hint',)
}

response_keys = {
    'geocomparision': ('geo_1', 'geo_2', 'compares'),
    'compares': ('timezones_difference', 'northern latitude', 'northern geo')
}
db = SQLAlchemy(app)

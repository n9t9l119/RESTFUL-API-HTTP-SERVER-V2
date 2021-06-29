import logging

from config import app, port, ru_txt_path, timezones_txt_path
from db.database_creation.DataBaseCreator import DataBaseCreator
from pages import api

if __name__ == '__main__':
    try:
        DataBaseCreator(ru_txt_path, timezones_txt_path).create_database()
    except Exception as e:
        logging.error(f'Database creation failed!\n{e}')
    else:
        api.ApiView.register(app)
        app.run(port=port)

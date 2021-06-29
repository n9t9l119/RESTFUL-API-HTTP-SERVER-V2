import logging

from config import app, port, ru_txt_path, timezones_txt_path
from db.database_creation.DatabaseCreator import DatabaseCreator
from pages import ApiView

if __name__ == '__main__':
    try:
        DatabaseCreator(ru_txt_path, timezones_txt_path).create_database()
    except Exception as e:
        logging.error(f'Database creation failed!\n{e}')
    else:
        ApiView.ApiView.register(app)
        app.run(port=port)

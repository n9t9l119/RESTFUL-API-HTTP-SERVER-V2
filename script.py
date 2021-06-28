from config import app, port, ru_txt_path, timezones_txt_path
from db.DataBaseCreator import DataBaseCreator
from pages import api

if __name__ == '__main__':
    DataBaseCreator(ru_txt_path, timezones_txt_path).create_database()
    api.ApiView.register(app)
    app.run(port=port)

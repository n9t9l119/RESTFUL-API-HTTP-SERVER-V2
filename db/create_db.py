from db.DataBaseCreator import DataBaseCreator
from config import ru_txt_path, timezones_txt_path

if __name__ == '__main__':
    DataBaseCreator(ru_txt_path, timezones_txt_path).generate_db()

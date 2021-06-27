import os.path
from typing import IO, List, Union

from config import db_path, ru_txt_path, timezones_txt_path, db
from db.TimezonesTxtConverter import TimezonesTxtConverter
from db.RuTxtConvertor import RuTxtConvertor
from db.model import GeoInfo, NameId
from db.serializers.Serializer import Serializer


class DataBaseCreator:
    def create_db(self):
        if not os.path.exists('..' + db_path):
            print("Database creation is started")

            ru_txt = open(ru_txt_path, 'r', encoding="utf8")
            timezones_txt = open(timezones_txt_path, 'r', encoding="utf8")

            self.convert_ru_txt_to_db(ru_txt)
            self.add_to_db(TimezonesTxtConverter().convert_timezones_txt_to_db(timezones_txt))

            ru_txt.close()
            timezones_txt.close()

            print("Database creation was completed successfully")
        else:
            print("Database is already exist!")

    def add_to_db(self, items: db.Model):
        db.session.add_all(items)
        db.session.commit()

    def convert_ru_txt_to_db(self, file: IO):
        db.create_all()
        table = []
        for string in file.readlines():
            cells = RuTxtConvertor().make_cells(string)
            table = self.append_str_to_db(table, cells)
        self.add_to_db(table)

    def append_str_to_db(self, table: List[Union[GeoInfo, NameId]], cells: List[str]) -> List[Union[NameId, GeoInfo]]:
        geo_item = RuTxtConvertor().convert_str_to_info(cells)
        geo_item = Serializer().serialize_geo_info(geo_item)
        table.append(geo_item)

        name_id_items = RuTxtConvertor().convert_str_to_nameid(cells, geo_item)
        name_id_items = [Serializer().serialize_name_id(item) for item in name_id_items]
        table.extend(name_id_items)
        return self.block_commit(table)

    def block_commit(self, table: List[Union[NameId, GeoInfo]]) -> List[Union[NameId, GeoInfo]]:
        if len(table) >= 600000:
            self.add_to_db(table)
            print("Database creation is in progress...")
            return []
        return table

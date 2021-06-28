import os.path
from typing import IO, List, Union

from config import db_path, db
from db.TimezonesTxtConverter import TimezonesTxtConverter
from db.RuTxtConvertor import RuTxtConvertor
from db.model import GeoInfo, NameId
from db.serializers.ModelSerializer import ModelSerializer


class DataBaseCreator:
    def __init__(self, ru_txt_path: str, timezones_txt_path: str):
        self.__ru_txt = open(ru_txt_path, 'r', encoding="utf8")
        self.__timezones_txt = open(timezones_txt_path, 'r', encoding="utf8")

        self.__ru_txt_convertor = RuTxtConvertor()

    def generate_db(self) -> None:
        if not os.path.exists('..' + db_path):
            print("Database creation is started")

            self.convert_ru_txt_to_db(self.__ru_txt)
            timezones_dicts = TimezonesTxtConverter().convert_timezones_txt_to_db(self.__timezones_txt)
            self.add_items_to_db(
                [ModelSerializer.deserialize_timezones(timezone) for timezone in timezones_dicts])

            print("Database creation was completed successfully")
        else:
            print("Database is already exist!")

    @staticmethod
    def add_items_to_db(items: db.Model) -> None:
        db.session.add_all(items)
        db.session.commit()

    def block_commit(self, table: List[Union[NameId, GeoInfo]]) -> List[Union[NameId, GeoInfo]]:
        if len(table) >= 600000:
            self.add_items_to_db(table)
            print("Database creation is in progress...")
            return []
        return table

    def convert_ru_txt_to_db(self, file: IO) -> None:
        db.create_all()
        table = []
        for string in file.readlines():
            cells = self.__ru_txt_convertor.make_cells(string)
            table = self.append_cells_to_db(table, cells)
        self.add_items_to_db(table)

    def append_cells_to_db(self, table: List[Union[GeoInfo, NameId]], cells: List[str]) -> List[Union[NameId, GeoInfo]]:
        table = self.add_geo_item_to_list(table, cells)
        table = self.add_nameid_items_to_list(table, cells)

        return self.block_commit(table)

    def add_geo_item_to_list(self, table: List[GeoInfo], cells: List[str]) -> List[GeoInfo]:
        geo_item = self.__ru_txt_convertor.convert_cells_to_info_dict(cells)
        geo_item = ModelSerializer.deserialize_geo_info(geo_item)
        table.append(geo_item)

        return table

    def add_nameid_items_to_list(self, table: List[GeoInfo], cells: List[str]) -> List[GeoInfo]:
        geo_item = table[-1]

        name_id_items = self.__ru_txt_convertor.convert_cells_to_nameid_dct(cells, geo_item)
        name_id_items = [ModelSerializer.deserialize_name_id(item) for item in name_id_items]
        table.extend(name_id_items)

        return table

    def __del__(self) -> None:
        self.__ru_txt.close()
        self.__timezones_txt.close()

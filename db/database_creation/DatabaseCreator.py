import os.path
from typing import IO, List, Union
import logging

from config import db_path, db
from db.database_creation.txt_convertors.TimezonesTxtConverter import TimezonesTxtConverter
from db.database_creation.txt_convertors.RuTxtConvertor import RuTxtConvertor
from db.model import GeoInfo, NameId
from db.serializers.ModelSerializer import ModelSerializer


class DatabaseCreator:
    def __init__(self, ru_txt_path: str, timezones_txt_path: str):
        self.__ru_txt_path = ru_txt_path
        self.__timezones_txt_path = timezones_txt_path

        if os.path.exists(ru_txt_path) and os.path.exists(timezones_txt_path):
            self.__ru_txt = open(ru_txt_path, 'r', encoding='utf8')
            self.__timezones_txt = open(timezones_txt_path, 'r', encoding='utf8')
        else:
            raise FileNotFoundError('Can\'t find database in txt!')

        self.__ru_txt_convertor = RuTxtConvertor()
        self.__timezones_txt_convertor = TimezonesTxtConverter()

        self.__model_serializer = ModelSerializer()

    def create_database(self) -> None:
        logging.basicConfig(level=logging.INFO)
        if not os.path.exists(db_path):
            logging.info('Database creation is started')
            db.create_all()
            self.__fill_database()
            logging.info('Database creation was completed successfully')
        else:
            logging.info(f'Database in directory {db_path} already exist')

    def __fill_database(self) -> None:
        self.__put_ru_txt_in_database(self.__ru_txt)
        timezones_dicts = self.__timezones_txt_convertor.convert_timezones_txt_to_dicts(self.__timezones_txt)
        serialized_timezones = [self.__model_serializer.deserialize_timezones(timezone) for timezone in timezones_dicts]
        self.__add_items_to_database(
            [timezone for timezone in serialized_timezones if timezone])

    def __put_ru_txt_in_database(self, file: IO) -> None:
        table = []
        for string in file:
            cells = self.__ru_txt_convertor.make_cells(string)
            table = self.__insert_items_to_database(table, cells)
        self.__add_items_to_database(table)

    def __insert_items_to_database(self, items_prepared_for_insertion: List[Union[GeoInfo, NameId]],
                                   cells: List[str]) -> List[Union[NameId, GeoInfo]]:

        start_items_count = len(items_prepared_for_insertion)
        items_prepared_for_insertion = self.__prepare_geo_item_to_insertion(items_prepared_for_insertion, cells)

        if start_items_count + 1 == len(items_prepared_for_insertion):
            items_prepared_for_insertion = self.__prepare_nameid_items_to_insertion(items_prepared_for_insertion, cells)
            return self.__commit_block_of_items(items_prepared_for_insertion)

        return items_prepared_for_insertion

    def __prepare_geo_item_to_insertion(self, items_prepared_for_insertion: List[Union[GeoInfo, NameId]],
                                        cells: List[str]) -> List[
        Union[GeoInfo, NameId]]:

        geo_item = self.__ru_txt_convertor.convert_cells_to_info_dict(cells)
        geo_item = self.__model_serializer.deserialize_geo_info(geo_item)
        if geo_item:
            items_prepared_for_insertion.append(geo_item)

        return items_prepared_for_insertion

    def __prepare_nameid_items_to_insertion(self, items_prepared_for_insertion: List[Union[GeoInfo, NameId]],
                                            cells: List[str]) -> List[
        Union[GeoInfo, NameId]]:

        geo_item = items_prepared_for_insertion[-1]

        name_id_items = self.__ru_txt_convertor.convert_cells_to_nameid_dict(cells, geo_item)
        name_id_items = [self.__model_serializer.deserialize_name_id(item) for item in name_id_items]
        items_prepared_for_insertion.extend(name_id_items)

        return items_prepared_for_insertion

    @staticmethod
    def __add_items_to_database(items: db.Model) -> None:
        db.session.add_all(items)
        db.session.commit()

    def __commit_block_of_items(self, table: List[Union[NameId, GeoInfo]]) -> List[Union[NameId, GeoInfo]]:
        if len(table) >= 600000:
            self.__add_items_to_database(table)
            logging.info('Database creation is in progress...')
            return []
        return table

    def __del__(self) -> None:
        if os.path.exists(self.__ru_txt_path) and os.path.exists(self.__timezones_txt_path):
            self.__ru_txt.close()
            self.__timezones_txt.close()

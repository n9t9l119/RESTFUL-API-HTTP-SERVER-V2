from transliterate import translit
from typing import Union, Dict, Any, List

from db.model import GeoInfo, Timezones
from repositories.GeoInfoRepository import GeoInfoRepository
from repositories.NameIdRepository import NameIdRepository
from repositories.TimezonesRepository import TimezonesRepository
from services.GeoInfoService import GeoInfoService


class GeoComparisonService:
    def __init__(self):
        self.geo_info_service = GeoInfoService()
        self.nameid_repository = NameIdRepository()
        self.info_repository = GeoInfoRepository()

    def compare_geo_items(self, geoname_1: str, geoname_2: str) -> Dict[str, Any]:
        geo_item_1, geo_item_2 = self.__get_geo_item_by_name(geoname_1), self.__get_geo_item_by_name(geoname_2)
        return self.make_compare_dict(geo_item_1, geo_item_2)

    def make_compare_dict(self, geo_item_1: GeoInfo, geo_item_2: GeoInfo) -> Dict[str, Any]:
        geo_items_comparison_dict = {'geo_1': self.geo_info_service.make_geoinfo_dict(geo_item_1),
                                     'geo_2': GeoInfoService().make_geoinfo_dict(geo_item_2),
                                     'compares': self.__compare_geo_items(geo_item_1, geo_item_2)}
        return geo_items_comparison_dict

    def __get_geo_item_by_name(self, geoname: str) -> GeoInfo:
        geo_ids = self.__get_all_ids_by_name(geoname)
        geo_items = self.__get_geo_items_by_geoids(geo_ids)
        return self.__choose_geo_item_with_max_population(geo_items)

    def __get_all_ids_by_name(self, translited_geoname: str) -> List[int]:
        ids_for_cyrillic = self.__get_geoids_by_geoname(translited_geoname)
        translited_geoname = translit(translited_geoname, reversed=True)
        ids_for_latin = self.__get_geoids_by_geoname(translited_geoname)

        return list(set(ids_for_latin).union(ids_for_cyrillic))

    def __get_geoids_by_geoname(self, geoname: str) -> List[int]:
        geo_items = self.nameid_repository.get_all_filtered_by_name(geoname)
        geoids = []

        if geo_items:
            for item in geo_items:
                geoids.append(item.geonameid)

        return geoids

    def __get_geo_items_by_geoids(self, ids: List[int]) -> List[GeoInfo]:
        geo_items = []

        if ids:
            for id in ids:
                item = self.info_repository.get_first_by_geonameid(id)
                if item is not None:
                    geo_items.append(item)

        return geo_items

    @staticmethod
    def __choose_geo_item_with_max_population(geo_items: List[GeoInfo]) -> Union[GeoInfo, None]:
        if geo_items:
            chosen_item = geo_items[0]
            for item in geo_items:
                if item.population > chosen_item.population:
                    chosen_item = item
            return chosen_item

        return None

    def __compare_geo_items(self, geo_item_1: GeoInfo, geo_item_2: GeoInfo) -> Union[Dict[str, Any], None]:
        if geo_item_1 is not None and geo_item_2 is not None:
            northern_item = self.__get_geo_item_with_max_latitude(geo_item_1, geo_item_2)
            comparison_dict = {'Northern geo': northern_item.name,
                               'Northern latitude': northern_item.latitude,
                               'Timezones_difference': self.__get_timezones_difference(geo_item_1, geo_item_2)}
            return comparison_dict

        return None

    @staticmethod
    def __get_geo_item_with_max_latitude(geo_item_1: GeoInfo, geo_item_2: GeoInfo) -> GeoInfo:
        if geo_item_1.latitude > geo_item_2.latitude:
            return geo_item_1
        return geo_item_2

    def __get_timezones_difference(self, geo_item_1: GeoInfo, geo_item_2: GeoInfo) -> str:
        if geo_item_1.timezone == geo_item_2.timezone:
            return '0.0'
        return self.__calculate_timezones_difference(self, geo_item_1.timezone, geo_item_2.timezone)

    def __calculate_timezones_difference(self, timezone_name_1: str, timezone_name_2: str) -> str:
        time_1 = self.__get_timezone_offset_by_timezone_name(timezone_name_1)
        time_2 = self.__get_timezone_offset_by_timezone_name(timezone_name_2)
        if not time_1 or not time_2:
            return "Undefinded"
        return str(time_1 - time_2)

    @staticmethod
    def __get_timezone_offset_by_timezone_name(timezone_name: str) -> Union[Timezones, None]:
        if timezone_name == "":
            return None
        else:
            timezone_name = TimezonesRepository().get_first_by_timezone(timezone_name)
            return TimezonesRepository().get_timezone_offset(timezone_name)

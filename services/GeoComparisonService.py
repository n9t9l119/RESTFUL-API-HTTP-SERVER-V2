from transliterate import translit
from flask import Response, jsonify
from typing import Union, Dict, Any, Tuple, List

from db.model import GeoInfo, Timezones
from repositories.InfoRepository import InfoRepository
from repositories.NameIdRepository import NameIdRepository
from repositories.TimezonesRepository import TimezonesRepository
from services.GeoInfoService import GeoInfoService


class GeoComparisonService:
    def compare_geos(self, geo_1: str, geo_2: str) -> Dict[str, Any]:
        geo_1, geo_2 = self.get_obj_by_name(geo_1), self.get_obj_by_name(geo_2)
        return self.make_compare_dict(geo_1, geo_2)

    def make_compare_dict(self, geo_1: GeoInfo, geo_2: GeoInfo) -> Dict[str, Any]:
        lt = {'geo_1': GeoInfoService().make_geoinfo_dict(geo_1), 'geo_2': GeoInfoService().make_geoinfo_dict(geo_2),
              'compares': self.get_comparison(geo_1, geo_2)}
        return lt

    def get_obj_by_name(self, name: str) -> GeoInfo:
        ids = self.find_all_ids(name)
        items = self.get_items_by_ids(ids)
        return self.chose_item(items)

    def find_all_ids(self, name: str) -> List[int]:
        ru_ids = self.get_ids_by_name(name)
        name = translit(name, reversed=True)
        alt_ids = self.get_ids_by_name(name)
        for id in ru_ids:
            if id not in alt_ids:
                alt_ids.append(id)
        return alt_ids

    def get_ids_by_name(self, name: str) -> List[int]:
        items = NameIdRepository().get_all_filtered_by_name(name)
        if items:
            ids = []
            for item in items:
                ids.append(item.geonameid)
            return ids
        return []

    def get_items_by_ids(self, ids: List[int]) -> List[GeoInfo]:
        if ids:
            items = []
            for id in ids:
                item = InfoRepository().get_first_by_geonameid(id)
                if item is not None:
                    items.append(item)
            return items
        return []

    def chose_item(self, items: List[GeoInfo]) -> Union[GeoInfo, None]:
        if items:
            chosen_item = items[0]
            for item in items:
                if item.population > chosen_item.population:
                    chosen_item = item
            return chosen_item
        return None

    def get_comparison(self, geo_1: GeoInfo, geo_2: GeoInfo) -> Union[Dict[str, Any], None]:
        if geo_1 is not None and geo_2 is not None:
            northern_item = self.compare_geo(geo_1, geo_2)
            compare_dct = {'Northern geo': northern_item.name,
                           'Northern latitude': northern_item.latitude,
                           'Timezones_difference': self.compare_timezone(geo_1, geo_2)}
            return compare_dct
        return None

    def compare_geo(self, geo_1: GeoInfo, geo_2: GeoInfo) -> GeoInfo:
        if geo_1.latitude > geo_2.latitude:
            return geo_1
        return geo_2

    def compare_timezone(self, geo_1: GeoInfo, geo_2: GeoInfo) -> str:
        if geo_1.timezone == geo_2.timezone:
            return '0.0'
        return self.timezones_difference(self, geo_1.timezone, geo_2.timezone)

    def timezones_difference(self, timezone_1: str, timezone_2: str) -> str:
        time_1 = self.get_timezone(timezone_1)
        time_2 = self.get_timezone(timezone_2)
        if not time_1 or not time_2:
            return "Undefinded"
        return str(time_1 - time_2)

    def get_timezone(self, timezone: str) -> Union[str, Timezones]:
        if timezone == "":
            return None
        else:
            timezone = TimezonesRepository().get_first_by_timezone(timezone)
            return TimezonesRepository().get_timezone_offset(timezone)

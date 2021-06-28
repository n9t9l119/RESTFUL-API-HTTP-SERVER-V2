from typing import List, Dict, Any

from services.GeoInfoService import GeoInfoService
from repositories.GeoInfoRepository import GeoInfoRepository


class GeoInfoPageService:
    def __init__(self):
        self.__info_repository = GeoInfoRepository()
        self.__geo_info_service = GeoInfoService()

    def get_page(self, page_number: int, items_value: int) -> List[Dict[str, Any]]:
        start_id = items_value * (page_number - 1) + 1
        return self.__make_geoinfo_lst(items_value, start_id)

    def __make_geoinfo_lst(self, items_count: int, start_id: int) -> List[Dict[str, Any]]:
        items = []
        for value in range(items_count):
            items.append(self.__geo_info_service.make_geoinfo_dict(self.__info_repository.get_item_by_id(start_id + value)))
        return items

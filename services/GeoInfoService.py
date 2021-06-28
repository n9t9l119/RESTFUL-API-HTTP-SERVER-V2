from typing import Union, Dict, Any, List

from db.model import GeoInfo, NameId
from db.serializers.ModelSerializer import ModelSerializer
from repositories.GeoInfoRepository import GeoInfoRepository
from repositories.NameIdRepository import NameIdRepository


class GeoInfoService:
    def __init__(self):
        self.__info_repository = GeoInfoRepository()
        self.__nameid_repository = NameIdRepository()

    def get_geoinfo_by_geonameid(self, geonameid: str) -> Union[Dict[str, Any], None]:
        geoitem = self.__info_repository._get_first_by_geonameid(geonameid)

        if geoitem is None:
            return None

        return self.make_geoinfo_dict(geoitem)

    def make_geoinfo_dict(self, geo_item: GeoInfo) -> Union[Dict[str, Any], None]:
        if geo_item is None:
            return None

        alternames = self.__get_geoitem_alternames(str(geo_item.geonameid))

        return ModelSerializer.serialize_geo_info(geo_item, alternames)

    def __get_geoitem_alternames(self, geonameid: str) -> List[str]:
        alternames = self.__nameid_repository.get_all_filtered_by_geonameid(geonameid)
        alternames_list = self.create_geoitem_alternames_list(geonameid, alternames)

        return alternames_list

    def create_geoitem_alternames_list(self, geonameid: str, alternames: List[NameId]) -> List[str]:
        names = []

        for name in alternames:
            names.append(name.name)

        if names:
            names.remove(self.__info_repository.get_geoname_by_geonameid(geonameid))

        return names

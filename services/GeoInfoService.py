from typing import Union, Dict, Any, List

from db.model import GeoInfo, NameId
from repositories.InfoRepository import InfoRepository
from repositories.NameIdRepository import NameIdRepository


class GeoInfoService:
    def get_item_by_geonameid(self, geonameid: str):
        item = InfoRepository().get_first_by_geonameid(geonameid)

        if item is None:
            return None

        return self.make_geoinfo_dict(item)

    def make_geoinfo_dict(self, item: GeoInfo) -> Union[Dict[str, Any], None]:
        if item is None:
            return None

        alternames = self.get_geo_alternames(str(item.geonameid))
        info_in_dict = {'geonameid': item.geonameid, 'name': item.name, 'asciiname': item.asciiname,
                        'alternatenames': alternames if alternames else "", 'latitude': item.latitude,
                        'longitude': item.longitude,
                        'feature class': item.feature_class, 'feature_code': item.feature_code,
                        'country_code': item.country_code, 'cc2': item.cc2, 'admin1_code': item.admin1_code,
                        'admin2_code': item.admin2_code, 'admin3_code': item.admin3_code,
                        'admin4_code': item.admin4_code, 'population': item.population, 'elevation': item.elevation,
                        'dem': item.dem, 'timezone': item.timezone, 'modification_date': item.modification_date}
        return info_in_dict

    def get_geo_alternames(self, geonameid: str) -> Union[str, List[str]]:
        alternames = NameIdRepository().get_all_filtered_by_geonameid(geonameid)
        names = self.create_geo_alternames_lst(geonameid, alternames)
        # if not names:
        #     return ""
        return names

    def create_geo_alternames_lst(self, geonameid: str, alternames: List[NameId]) -> List[str]:
        names = []

        for name in alternames:
            names.append(name.name)

        if names:
            geo = InfoRepository().get_first_by_geonameid(geonameid)
            names.remove(InfoRepository().get_geo_name(geo))

        return names

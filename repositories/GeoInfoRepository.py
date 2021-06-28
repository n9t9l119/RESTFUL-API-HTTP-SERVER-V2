from typing import Union, List

from db.model import GeoInfo
from repositories.AbstractRepositories import AbstractGeoInfoRepository


class GeoInfoRepository(AbstractGeoInfoRepository):
    def get_item_by_id(self, id: int) -> Union[GeoInfo, None]:
        try:
            return GeoInfo.query.get(id)
        except:
            return None

    def get_all(self) -> List[GeoInfo]:
        return GeoInfo.query.all()

    def _get_first_by_geonameid(self, geonameid: int) -> GeoInfo:
        return GeoInfo.query.filter_by(geonameid=geonameid).first()

    def get_geoname_by_geonameid(self, geonameid: int) -> str:
        return self._get_first_by_geonameid(geonameid).name

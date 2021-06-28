from typing import List

from db.model import NameId
from repositories.AbstractRepositories import AbstractNameIdRepository


class NameIdRepository(AbstractNameIdRepository):
    def get_all(self) -> NameId:
        return NameId.query.all()

    def get_all_sorted_by_name(self) -> str:
        return NameId.query.order_by(NameId.name)

    def get_all_filtered_by_name(self, name: str) -> List[NameId]:
        return NameId.query.filter_by(name=name)

    def get_all_filtered_by_geonameid(self, geonameid: int) -> List[NameId]:
        return NameId.query.filter_by(geonameid=geonameid)

    def get_items_by_name_template(self, request: str) -> List[NameId]:
        return NameId.query.filter(NameId.name.ilike(f'%{request}%'))

from typing import List

from repositories.NameIdRepository import NameIdRepository


class GeoNameHintService:
    def __init__(self):
        self.__nameid_repository = NameIdRepository()

    def get_hint(self, request: str) -> List[str]:
        hint_list = self.__nameid_repository.get_items_by_name_template(request)
        hint_list = [hint.name for hint in hint_list]
        return list(set(hint_list))

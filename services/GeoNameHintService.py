from typing import List

from repositories.NameIdRepository import NameIdRepository


class GeoNameHintService:
    def get_hint(self, request: str) -> List[str]:
        return self.make_hint_list(request)

    def make_hint_list(self, request: str) -> List[str]:
        hint_list = NameIdRepository().filter(request)
        hint_list = [hint.name for hint in hint_list]
        return list(set(hint_list))

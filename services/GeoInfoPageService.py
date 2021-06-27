from typing import List, Dict, Any

from services.GeoInfoService import GeoInfoService
from repositories.InfoRepository import InfoRepository


class GeoInfoPageService:
    def get_page(self, page_number: int, items_value: int) -> List[Dict[str, Any]]:
        start_id = items_value * (page_number-1) + 1
        return self.make_geoinfo_lst(items_value, start_id)

    # def input_validation(self, page_number: int, items_value: int) -> Union[bool, Response]:
    #     if re.match(r'[0-9]{1,6}$', str(page_number)) \
    #             and re.match(r'[0-9]{1,6}$', str(items_value)) is not None:
    #         return self.numerical_range_validation(page_number, items_value)
    #     return Response("'Page' and 'Items_value' must be a positive number no less than 1 and no more than 6 digits!",
    #                     status=400, mimetype='text/plain')
    #
    # def numerical_range_validation(self, page_number: int, items_value: int) -> Union[bool, Response]:
    #     max_value = len(InfoRepository().get_all())
    #     if items_value > max_value:
    #         return Response("There is not so many values in database!", status=404, mimetype='text/plain')
    #     if (page_number + 1) * items_value > max_value or items_value == 0:
    #         return Response("That get_page is empty!", status=400, mimetype='text/plain')
    #     return True

    def make_geoinfo_lst(self, items_value: int, start_id: int) -> List[Dict[str, Any]]:
        items = []
        for value in range(items_value):
            items.append(GeoInfoService().make_geoinfo_dict(InfoRepository().get_by_id(start_id + value)))
        return items

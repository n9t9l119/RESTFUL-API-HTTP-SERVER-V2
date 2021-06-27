import pytest

from services import GeoInfoPageService
from db.model import GeoInfo


@pytest.fixture()
def page_items_value_validation():
    max_items_value = len(GeoInfo.query.all())

    def params_lst():
        params = [(3, 2),
                  (0, max_items_value)]
        return params

    return params_lst()


def test_input_validation(page_items_value_validation):
    for tup in page_items_value_validation:
        (page_number, items_value) = tup
        result = GeoInfoPageService.input_validation(page_number, items_value)
        assert result == True

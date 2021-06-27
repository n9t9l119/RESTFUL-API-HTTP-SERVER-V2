import pytest
import re

from services import GeoComparisonService
from db.model import GeoInfo


@pytest.fixture()
def comparison_validation(request):
    (item_1, item_2) = make_items_from_id(request.param)

    def params_list():
        params = [([None, item_2]), ([item_1, item_2])]
        return params

    return params_list()


def make_items_from_id(param):
    (id_1, id_2) = param

    item_1 = GeoInfo.query.filter_by(geonameid=id_1).first()
    item_2 = GeoInfo.query.filter_by(geonameid=id_2).first()
    return item_1, item_2


@pytest.mark.parametrize('comparison_validation', [
    (462339, 11238618),
    (462335, 462339)
], indirect=True)
def test_get_comparison(comparison_validation):
    for tup in comparison_validation:
        (geo_1, geo_2) = tup
        result = GeoComparisonService.get_comparison(geo_1, geo_2)
        assert result is None or re.match(r'[-]?[0-9]{1,2}\.*[0-9]{0,2}$|0|"Undefinded"',
                                          str(result['Timezones_difference'])) and \
               re.match(r'[-]?[0-9]{1,3}\.*[0-9]{0,5}$', str(result['Northern latitude'])) and \
               result['Northern geo'] != "" and result['Northern geo'] is not None


def test_chose_item():
    max_population_id = 1
    result = GeoComparisonService.chose_item(GeoInfo.query.all())
    assert result.id == max_population_id


@pytest.mark.parametrize("input, expected_output", [("Знаменка", [462335, 462336, 462337, 462338, 462339, 462340]),
                                                    ("Отсутствующее название", [])])
def test_find_all_ids(input, expected_output):
    result = GeoComparisonService.find_all_ids(input)
    assert result == expected_output


@pytest.fixture()
def items_by_ids_validation(request):
    (id_1, id_2) = request.param
    (item_1, item_2) = make_items_from_id(request.param)

    def params_list():
        params = [([id_1, id_2], [item_1, item_2]),
                  ([], [])]
        return params

    return params_list()


@pytest.mark.parametrize('items_by_ids_validation', [
    (8456283, 11238618),
    (462335, 462336)
], indirect=True)
def test_get_items_by_id(items_by_ids_validation):
    for tup in items_by_ids_validation:
        (request, expected_output) = tup
        result = GeoComparisonService.get_items_by_ids(request)
        assert result == expected_output

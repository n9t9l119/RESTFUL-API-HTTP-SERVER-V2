from flask_classy import FlaskView, route
from flask import request, Response, jsonify

from BadReuquestResponse import BadRequestResponse
from services.GeoComparisonService import GeoComparisonService
from services.GeoInfoService import GeoInfoService
from services.GeoNameHintService import GeoNameHintService
from services.GeoInfoPageService import GeoInfoPageService
from validators.RequestValidator import RequestValidator


class ApiView(FlaskView):
    __request_validator = RequestValidator()
    __bad_request_response = BadRequestResponse()

    __geo_info_service = GeoInfoService()
    __geo_info_page_service = GeoInfoPageService()
    __geo_comparison_service = GeoComparisonService()
    __geo_name_hint_service = GeoNameHintService()

    @route('/getinfo', methods=["POST"])
    def get_geo_info(self) -> Response:
        expected_keys = 'Geo_id',

        json_request = request.get_json()
        validated_geonameid = self.__request_validator.try_convert_to_positive_int(json_request[expected_keys[0]])

        if validated_geonameid is None:
            return self.__bad_request_response.positive_int_expected(expected_keys)

        geoinfo = self.__geo_info_service.get_item_by_geonameid(json_request[expected_keys[0]])

        if geoinfo is None:
            return Response("Such id does not exist!", status=404, mimetype='text/plain')

        return jsonify(geoinfo)

    @route('/getpage', methods=["POST"])
    def get_page(self) -> Response:
        json_request = request.get_json()

        expected_keys = 'Page', 'Items_value'

        if self.__request_validator.find_keys_in_request(json_request, *expected_keys) is None:
            return self.__bad_request_response.keys_not_found(expected_keys)

        if self.__request_validator.try_convert_request_values_to_positive_int(json_request) is None:
            return self.__bad_request_response.positive_int_expected(expected_keys)

        return jsonify(self.__geo_info_page_service.get_page(json_request[expected_keys[0]], json_request[expected_keys[1]]))

    @route('/getcomparison', methods=["POST"])
    def get_comparison(self) -> Response:
        json_request = request.get_json()

        expected_keys = 'Geo_1', 'Geo_2'

        if self.__request_validator.find_keys_in_request(json_request, *expected_keys) is None:
            return self.__bad_request_response.keys_not_found(expected_keys)

        if self.__request_validator.check_match_request_values_to_pattern(r'[А-Яа-я0-9\s]*$', json_request) is None:
            return self.__bad_request_response.incorrect_symbols(expected_keys)

        return jsonify(
            self.__geo_comparison_service.compare_geos(json_request[expected_keys[0]], json_request[expected_keys[0]]))

    @route('/hintname', methods=["POST"])
    def hint_name(self) -> Response:
        json_request = request.get_json()

        expected_keys = 'Hint',

        validated_hintname = self.__request_validator.check_match_with_pattern(r'[\wА-Яа-я\d]*',
                                                                               json_request[expected_keys[0]])

        if validated_hintname is None:
            return self.__bad_request_response.incorrect_symbols(expected_keys)

        return jsonify(self.__geo_name_hint_service.get_hint(json_request[expected_keys[0]]))

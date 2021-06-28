from flask_classy import FlaskView, route
from flask import request, Response, jsonify

from pages.request_validation.responses.BadReuquestResponse import ClientErrorResponse
from services.GeoComparisonService import GeoComparisonService
from services.GeoInfoService import GeoInfoService
from services.GeoNameHintService import GeoNameHintService
from services.GeoInfoPageService import GeoInfoPageService
from pages.request_validation.RequestValidator import RequestValidator
from config import request_keys


class ApiView(FlaskView):
    __request_validator = RequestValidator()

    __geo_info_service = GeoInfoService()
    __geo_info_page_service = GeoInfoPageService()
    __geo_comparison_service = GeoComparisonService()
    __geo_name_hint_service = GeoNameHintService()

    @route('/getinfo', methods=["POST"])
    def get_geo_info(self) -> Response:
        try:
            json_request = request.get_json()
        except:
            return ClientErrorResponse.unable_parse_request()

        if not json_request:
            return ClientErrorResponse.json_expected()

        if self.__request_validator.find_keys_in_request(json_request, *request_keys['geoinfo']) is None:
            return ClientErrorResponse.keys_not_found(request_keys['geoinfo'])

        validated_geonameid = self.__request_validator.try_convert_to_positive_int(json_request[request_keys['geoinfo'][0]])

        if validated_geonameid is None:
            return ClientErrorResponse.positive_int_expected(request_keys['geoinfo'])

        geoinfo = self.__geo_info_service.get_geoinfo_by_geonameid(json_request[request_keys['geoinfo'][0]])

        if geoinfo is None:
            return ClientErrorResponse.geonameid_does_not_exist()

        return jsonify(geoinfo)

    @route('/getpage', methods=["POST"])
    def get_page(self) -> Response:
        try:
            json_request = request.get_json()
        except:
            return ClientErrorResponse.unable_parse_request()

        if not json_request:
            return ClientErrorResponse.json_expected()

        if self.__request_validator.find_keys_in_request(json_request, *request_keys['getpage']) is None:
            return ClientErrorResponse.keys_not_found(request_keys['getpage'])

        if self.__request_validator.try_convert_request_values_to_positive_int(json_request) is None:
            return ClientErrorResponse.positive_int_expected(request_keys['getpage'])

        return jsonify(
            self.__geo_info_page_service.get_page(json_request[request_keys['getpage'][0]], json_request[request_keys['getpage'][1]]))

    @route('/getcomparison', methods=["POST"])
    def get_comparison(self) -> Response:
        try:
            json_request = request.get_json()
        except:
            return ClientErrorResponse.unable_parse_request()

        if not json_request:
            return ClientErrorResponse.json_expected()

        if self.__request_validator.find_keys_in_request(json_request, *request_keys['getcomparison']) is None:
            return ClientErrorResponse.keys_not_found(request_keys['getcomparison'])

        if self.__request_validator.check_match_request_values_to_pattern(r'[А-Яа-я0-9\s]*$', json_request) is None:
            return ClientErrorResponse.incorrect_symbols(request_keys['getcomparison'])

        return jsonify(
            self.__geo_comparison_service.compare_geo_items(json_request[request_keys['getcomparison'][0]],
                                                            json_request[request_keys['getcomparison'][1]]))

    @route('/hintname', methods=["POST"])
    def hint_name(self) -> Response:
        try:
            json_request = request.get_json()
        except:
            return ClientErrorResponse.unable_parse_request()

        if not json_request:
            return ClientErrorResponse.json_expected()

        if self.__request_validator.find_keys_in_request(json_request, *request_keys['hintname']) is None:
            return ClientErrorResponse.keys_not_found(request_keys['hintname'])

        validated_hintname = self.__request_validator.check_match_with_pattern(r'[\wА-Яа-я\d]*',
                                                                               json_request[request_keys['hintname'][0]])

        if validated_hintname is None:
            return ClientErrorResponse.incorrect_symbols(request_keys['hintname'])

        return jsonify(self.__geo_name_hint_service.get_hint(json_request[request_keys['hintname'][0]]))

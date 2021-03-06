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
        validated_request = self.__validate_json_request(request_keys['geoinfo'])

        if isinstance(validated_request, Response):
            return validated_request

        validated_geonameid = self.__request_validator.try_convert_to_positive_int(
            validated_request[request_keys['geoinfo'][0]])

        if validated_geonameid is None:
            return ClientErrorResponse.positive_int_expected(request_keys['geoinfo'])

        geoinfo = self.__geo_info_service.get_geoinfo_by_geonameid(validated_request[request_keys['geoinfo'][0]])

        if geoinfo is None:
            return ClientErrorResponse.geonameid_does_not_exist()

        return jsonify(geoinfo)

    @route('/getpage', methods=["POST"])
    def get_page(self) -> Response:
        validated_request = self.__validate_json_request(request_keys['getpage'])

        if isinstance(validated_request, Response):
            return validated_request

        if self.__request_validator.try_convert_request_values_to_positive_int(validated_request) is None:
            return ClientErrorResponse.positive_int_expected(request_keys['getpage'])

        return jsonify(
            self.__geo_info_page_service.get_page(validated_request[request_keys['getpage'][0]],
                                                  validated_request[request_keys['getpage'][1]]))

    @route('/getcomparison', methods=["POST"])
    def get_comparison(self) -> Response:
        validated_request = self.__validate_json_request(request_keys['getcomparison'])

        if isinstance(validated_request, Response):
            return validated_request

        if self.__request_validator.check_match_request_values_to_pattern(r'[??-????-??0-9\s]*$',
                                                                          validated_request) is None:
            return ClientErrorResponse.incorrect_symbols(request_keys['getcomparison'])

        return jsonify(
            self.__geo_comparison_service.compare_geo_items(validated_request[request_keys['getcomparison'][0]],
                                                            validated_request[request_keys['getcomparison'][1]]))

    @route('/hintname', methods=["POST"])
    def hint_name(self) -> Response:
        validated_request = self.__validate_json_request(request_keys['hintname'])

        if isinstance(validated_request, Response):
            return validated_request

        validated_hintname = self.__request_validator.check_match_with_pattern(r'[\w??-????-??\d]*',
                                                                               validated_request[
                                                                                   request_keys['hintname'][0]])

        if validated_hintname is None:
            return ClientErrorResponse.incorrect_symbols(request_keys['hintname'])

        return jsonify(self.__geo_name_hint_service.get_hint(validated_request[request_keys['hintname'][0]]))

    def __validate_json_request(self, request_keys):
        try:
            json_request = request.get_json()
        except:
            return ClientErrorResponse.unable_parse_request()

        if not json_request:
            return ClientErrorResponse.json_expected()

        if self.__request_validator.find_keys_in_request(json_request, *request_keys) is None:
            return ClientErrorResponse.keys_not_found(request_keys)

        return json_request

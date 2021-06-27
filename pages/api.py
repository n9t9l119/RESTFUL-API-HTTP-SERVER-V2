from flask_classy import FlaskView, route
from flask import request, Response, jsonify

from services.GeoComparisonService import GeoComparisonService
from services.GeoInfoService import GeoInfoService
from services.GeoNameHintService import GeoNameHintService
from services.GeoInfoPageService import GeoInfoPageService
from RequestValidator import RequestValidator


class ApiView(FlaskView):
    @route('/getinfo', methods=["POST"])
    def get_geo_info(self) -> Response:
        geonameid = request.data.decode("utf-8")
        validated_geonameid = RequestValidator().try_convert_to_positive_int(geonameid)

        if validated_geonameid is None:
            return Response("Incorrect request!\nGeonameid must be positive int",
                            status=500, mimetype='text/plain')

        geoinfo = GeoInfoService().get_item_by_geonameid(validated_geonameid)

        if geoinfo is None:
            return Response("Such id does not exist!", status=404, mimetype='text/plain')

        return jsonify(geoinfo)

    @route('/getpage', methods=["POST"])
    def get_page(self) -> Response:
        json_request = request.get_json()

        expected_keys = ('Page', 'Items_value')

        if RequestValidator().find_keys_in_request(json_request, expected_keys[0], expected_keys[1]) is None:
            return Response(f"Incorrect request!\nIt must be json with keys {', '.join(expected_keys)}!",
                            status=500, mimetype='text/plain')

        if RequestValidator().try_convert_request_values_to_positive_int(json_request) is None:
            return Response(f"Incorrect request!\n{', '.join(expected_keys)} must be positive int",
                            status=500, mimetype='text/plain')

        return jsonify(GeoInfoPageService().get_page(json_request[expected_keys[0]], json_request[expected_keys[1]]))

    @route('/getcomparison', methods=["POST"])
    def get_comparison(self) -> Response:
        json_request = request.get_json()

        expected_keys = ('Geo_1', 'Geo_2')

        if RequestValidator().find_keys_in_request(json_request, expected_keys[0], expected_keys[1]) is None:
            return Response(f"Incorrect request!\nIt must be json with keys {', '.join(expected_keys)}!",
                            status=500, mimetype='text/plain')

        if RequestValidator().check_match_request_values_to_pattern(r'[А-Яа-я0-9\s]*$', json_request) is None:
            return Response(f"Incorrect request!\n{', '.join(expected_keys)} include incorrect symbols!",
                            status=500, mimetype='text/plain')

        return jsonify(GeoComparisonService().compare_geos(json_request[expected_keys[0]], json_request[expected_keys[0]]))

    @route('/hintname', methods=["POST"])
    def hint_name(self) -> Response:
        hintname = request.data.decode("utf-8")

        validated_hintname = RequestValidator().check_match_with_pattern(r'[\wА-Яа-я\d]*', hintname)

        if validated_hintname is None:
            return Response("Incorrect request!\nRequest includes incorrect symbols!",
                            status=500, mimetype='text/plain')

        return jsonify(GeoNameHintService().get_hint(hintname))

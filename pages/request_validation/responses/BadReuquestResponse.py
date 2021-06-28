from flask import Response


class ClientErrorResponse:
    @staticmethod
    def unable_parse_request():
        return Response(f'Incorrect request!\nUnable to parse the request.',
                            status=400, mimetype='text/plain')
    @staticmethod
    def json_expected() -> Response:
        return Response(f'Incorrect request!\nRequest must be in json format.',
                        status=400, mimetype='text/plain')

    @staticmethod
    def positive_int_expected(expected_keys: tuple) -> Response:
        return Response(f'Incorrect request!\n{", ".join(expected_keys)} must be positive int.',
                        status=400, mimetype='text/plain')

    @staticmethod
    def incorrect_symbols(expected_keys: tuple) -> Response:
        return Response(f'Incorrect request!\n{", ".join(expected_keys)} include incorrect symbols!',
                        status=400, mimetype='text/plain')

    @staticmethod
    def keys_not_found(expected_keys: tuple) -> Response:
        return Response(f"Incorrect request!\nIt must be json with keys {', '.join(expected_keys)}!",
                        status=400, mimetype='text/plain')

    @staticmethod
    def geonameid_does_not_exist() -> Response:
        return Response("Such geonameid does not exist!", status=404, mimetype='text/plain')

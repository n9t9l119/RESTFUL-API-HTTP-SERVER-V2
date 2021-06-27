from flask import Response


class BadRequestResponse:
    def positive_int_expected(self, expected_keys: tuple) -> Response:
        return Response(f'Incorrect request!\n{", ".join(expected_keys)} must be positive int',
                        status=500, mimetype='text/plain')

    def incorrect_symbols(self, expected_keys: tuple) -> Response:
        return Response(f'Incorrect request!\n{", ".join(expected_keys)} include incorrect symbols!',
                        status=500, mimetype='text/plain')

    def keys_not_found(self, expected_keys: tuple) -> Response:
        return Response(f"Incorrect request!\nIt must be json with keys {', '.join(expected_keys)}!",
                        status=500, mimetype='text/plain')

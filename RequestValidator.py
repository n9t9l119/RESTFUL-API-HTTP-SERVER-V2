import re


class RequestValidator:
    def check_match_with_pattern(self, pattern, value):
        occurrences = re.match(pattern, value)
        if occurrences is None:
            return None
        return occurrences.group(0) if occurrences.group(0) == value else None

    def check_match_request_values_to_pattern(self, pattern, request):
        for key in request:
            converted_value = self.check_match_with_pattern(pattern, request[key])

            if converted_value is None:
                return None

            request[key] = converted_value
        return request

    def try_convert_to_positive_int(self, geonameid):
        try:
            geonameid = int(geonameid)
        except:
            return None

        return geonameid if geonameid > 0 else None

    def find_keys_in_request(self, request, *keys):
        for key in keys:
            if key not in request:
                return None
            request[key] = request[key]
        return request

    def try_convert_request_values_to_positive_int(self, request):
        for key in request:
            converted_value = self.try_convert_to_positive_int(request[key])

            if converted_value is None:
                return None

            request[key] = converted_value
        return request

import re
from typing import Union, Dict


class RequestValidator:
    @staticmethod
    def find_keys_in_request(json_request: Dict, *keys: str) -> Union[Dict[str, str], None]:
        for key in keys:
            if key not in json_request:
                return None

            json_request[key] = json_request[key]
        return json_request

    @staticmethod
    def check_match_with_pattern(pattern: re, value: str) -> Union[str, None]:
        occurrences = re.match(pattern, value)

        if occurrences is None:
            return None

        return occurrences.group(0) if occurrences.group(0) == value else None

    def check_match_request_values_to_pattern(self, pattern: re, json_request: Dict) -> Union[Dict[str, str], None]:
        for key in json_request:
            converted_value = self.check_match_with_pattern(pattern, json_request[key])

            if converted_value is None:
                return None

            json_request[key] = converted_value
        return json_request

    @staticmethod
    def try_convert_to_positive_int(geonameid: int) -> Union[int, None]:
        return geonameid if geonameid > 0 else None

    def try_convert_request_values_to_positive_int(self, json_request: Dict[str, int]) -> Union[Dict[str, int], None]:
        for key in json_request:
            converted_value = self.try_convert_to_positive_int(json_request[key])

            if converted_value is None:
                return None

            json_request[key] = converted_value
        return json_request

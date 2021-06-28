import re
from typing import Dict


class GeoComparesTemplate:
    __timezones_difference_pattern = r'[-]?[0-9]{1,2}\.*[0-9]{0,2}$|0|"Undefinded"'
    __northern_latitude_pattern = r'[-]?[0-9]{1,3}\.*[0-9]{0,5}$'

    def check_template_matches(self, compares: Dict) -> bool:
        return compares == None or re.match(self.__timezones_difference_pattern,
                                            str(compares['Timezones_difference'])) and \
               re.match(self.__northern_latitude_pattern, str(compares['Northern latitude'])) and \
               compares['Northern geo'] != "" and compares['Northern geo'] is not None

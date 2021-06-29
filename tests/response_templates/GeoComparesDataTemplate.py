import re
from typing import Dict

from tests.response_templates.AbstractDataTemplate import AbstractDataTemplate
from config import response_keys


class GeoComparesDataTemplate(AbstractDataTemplate):
    __timezones_difference_pattern = r'[-]?[0-9]{1,2}\.*[0-9]{0,2}$|0|"Undefinded"'
    __northern_latitude_pattern = r'[-]?[0-9]{1,3}\.*[0-9]{0,5}$'

    def check_template_matches(self, compares: Dict) -> bool:
        compares_key = response_keys['compares']
        return compares == None or re.match(self.__timezones_difference_pattern,
                                            str(compares[compares_key[0]])) and \
               re.match(self.__northern_latitude_pattern, str(compares[compares_key[1]])) and \
               compares[compares_key[2]] != "" and compares[compares_key[2]] is not None

import re
from typing import List


class GeoInfoDataTemplate:
    __data_patterns = [r'[0-9]{6,8}$', '', '', '', r'[-]?[0-9]{1,3}\.*[0-9]{0,5}$', r'[-]?[0-9]{1,3}\.*[0-9]{0,5}$',
                     r'[A-Z]{1,4}$', r'[A-Z\d]{2,5}$', 'RU', '', r'[0-9\w]{2}|^$', '', '', '', r'[0-9]*$', '',
                     r'[-]?[0-9]*$',
                     r'[\w-]*/[\w-]*|^$', r'[0-9]{4}-[0-9]{2}-[0-9]{2}$']

    def check_template_matches(self, cells:List):
        for count in range(len(GeoInfoDataTemplate.__data_patterns)):
            if GeoInfoDataTemplate.__data_patterns[count] != '':
                assert re.match(GeoInfoDataTemplate.__data_patterns[count], str(cells[count]))

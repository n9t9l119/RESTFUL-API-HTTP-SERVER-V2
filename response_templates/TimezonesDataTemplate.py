import re
from typing import List

from response_templates.AbstractDataTemplate import AbstractDataTemplate

class TimezonesDataTemplate(AbstractDataTemplate):
    __data_patterns = [r'([\w-]*\/){1,2}[\w-]*$', r'[-]?[0-9]{1,2}\.[0-9]|0$']

    def check_template_matches(self, cells: List[str]) -> bool:
        if not re.match(self.__data_patterns[0], cells[1]) \
               and re.match(self.__data_patterns[1], cells[3]):
            return False
        return True

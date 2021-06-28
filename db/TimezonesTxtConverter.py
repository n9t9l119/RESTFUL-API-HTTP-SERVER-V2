from typing import List, Union, IO, Dict

from repositories.InfoRepository import InfoRepository


class TimezonesTxtConverter:
    def convert_timezones_txt_to_db(self, timezones_txt: IO) -> List[Dict[str, float]]:
        timezones_db_lst = []
        expected_timezones_names = self.get_timezones()
        for cells in timezones_txt.readlines():
            cells = cells.split('\t')
            timezones_db_lst = self.append_timezone_to_db(expected_timezones_names, timezones_db_lst, cells)
        return timezones_db_lst

    def append_timezone_to_db(self, expected_timezones_names: List[str], timezones_db_list: List[Dict[str, float]],
                              cells: List[Union[str, float]]) -> List[Dict[str, float]]:
        if cells[1] in expected_timezones_names:
            timezones_db_list.append(dict(time_zone=cells[1], offset=cells[3]))
        return timezones_db_list

    def get_timezones(self) -> List[str]:
        timezones_list = []
        for item in InfoRepository().get_all():
            if item.timezone not in timezones_list:
                timezones_list.append(item.timezone)
        return timezones_list

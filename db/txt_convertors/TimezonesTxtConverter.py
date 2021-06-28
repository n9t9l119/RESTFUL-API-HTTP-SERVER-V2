from typing import List, Union, IO, Dict

from repositories.GeoInfoRepository import GeoInfoRepository


class TimezonesTxtConverter:
    def __init__(self):
        self.__geoinfo_repository = GeoInfoRepository()

    def convert_timezones_txt_to_dicts(self, timezones_txt: IO) -> List[Dict[str, float]]:
        timezones_db_lst = []
        expected_timezones_names = self.__get_timezones_required_by_geoinfo()
        for cells in timezones_txt.readlines():
            cells = cells.split('\t')
            timezones_db_lst = self.__append_timezone_dict_to_list(expected_timezones_names, timezones_db_lst, cells)
        return timezones_db_lst

    @staticmethod
    def __append_timezone_dict_to_list(expected_timezones_names: List[str], timezones_list: List[Dict[str, float]],
                                       cells: List[Union[str, float]]) -> List[Dict[str, float]]:
        if cells[1] in expected_timezones_names:
            timezones_list.append(dict(time_zone=cells[1], offset=cells[3]))
        return timezones_list

    def __get_timezones_required_by_geoinfo(self) -> List[str]:
        timezones_list = []
        for geo_item in self.__geoinfo_repository.get_all():
            if geo_item.timezone not in timezones_list:
                timezones_list.append(geo_item.timezone)
        return timezones_list

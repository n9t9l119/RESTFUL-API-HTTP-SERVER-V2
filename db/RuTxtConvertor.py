from typing import List, Union

from db.model import GeoInfo, NameId


class RuTxtConvertor:
    def make_cells(self, string: str) -> List[str]:
        cells = string.split('\t')
        cells[-1] = cells[-1].replace("\n", "")
        return cells

    def convert_str_to_info(self, cells: List[str]):
        info_string = dict(
            geonameid=cells[0],
            name=cells[1],
            asciiname=cells[2],
            alternatenames=cells[3],
            latitude=cells[4],
            longitude=cells[5],
            feature_class=cells[6],
            feature_code=cells[7],
            country_code=cells[8],
            cc2=cells[9],
            admin1_code=cells[10],
            admin2_code=cells[11],
            admin3_code=cells[12],
            admin4_code=cells[13],
            population=cells[14],
            elevation=cells[15],
            dem=cells[16],
            timezone=cells[17],
            modification_date=cells[18])
        return info_string

    def convert_str_to_nameid(self, cells: List[str], item: GeoInfo) -> List[NameId]:
        all_str_names_to_db = []
        names = self.all_names_in_str(cells)
        for name in names:
            all_str_names_to_db.append(NameId(name=name, idlnk=item))
        return all_str_names_to_db

    def all_names_in_str(self, cells: List[str]) -> List[str]:
        names = [cells[1]]
        if names[0] != cells[2]:
            names.append(cells[2])
        if cells[4] != "":
            alternatenames = cells[3].split(',')
            for alternatename in alternatenames:
                if alternatename not in names and alternatename != '':
                    names.append(alternatename)
        return names




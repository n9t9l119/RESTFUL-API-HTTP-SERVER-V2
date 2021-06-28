from abc import ABC, abstractmethod
from typing import List, Union

from db.model import GeoInfo, NameId, Timezones


class AbstractGeoInfoRepository(ABC):
    @abstractmethod
    def get_item_by_id(self, id: int) -> Union[GeoInfo, None]:
        raise NotImplementedError(
            f'Method {self.__class__.get_item_by_id.__name__} not implemented in class {self.__class__.__name__}')

    @abstractmethod
    def get_all(self) -> List[GeoInfo]:
        raise NotImplementedError(
            f'Method {self.__class__.get_all.__name__} not implemented in class {self.__class__.__name__}')

    @abstractmethod
    def _get_first_by_geonameid(self, geonameid: int) -> GeoInfo:
        raise NotImplementedError(
            f'Method {self.__class__._get_first_by_geonameid.__name__} not implemented in class {self.__class__.__name__}')

    @abstractmethod
    def get_geoname_by_geonameid(self, geonameid: int) -> str:
        raise NotImplementedError(
            f'Method {self.__class__.get_geoname_by_geonameid.__name__} not implemented in class {self.__class__.__name__}')


class AbstractNameIdRepository(ABC):
    @abstractmethod
    def get_all(self) -> NameId:
        raise NotImplementedError(
            f'Method {self.__class__.get_all.__name__} not implemented in class {self.__class__.__name__}')

    @abstractmethod
    def get_all_sorted_by_name(self) -> str:
        raise NotImplementedError(
            f'Method {self.__class__.get_all_sorted_by_name.__name__} not implemented in class {self.__class__.__name__}')

    @abstractmethod
    def get_all_filtered_by_name(self, name: str) -> List[NameId]:
        raise NotImplementedError(
            f'Method {self.__class__.get_all_filtered_by_name.__name__} not implemented in class {self.__class__.__name__}')

    @abstractmethod
    def get_all_filtered_by_geonameid(self, geonameid: int)-> List[NameId]:
        raise NotImplementedError(
            f'Method {self.__class__.get_all_filtered_by_geonameid.__name__} not implemented in class {self.__class__.__name__}')

    @abstractmethod
    def get_items_by_name_template(self, request: str) -> List[NameId]:
        raise NotImplementedError(
            f'Method {self.__class__.get_items_by_name_template.__name__} not implemented in class {self.__class__.__name__}')


class AbstractTimezonesRepository(ABC):
    @abstractmethod
    def _get_first_by_timezone(self, timezone_name: str) -> Timezones:
        raise NotImplementedError(
            f'Method {self.__class__._get_first_by_timezone.__name__} not implemented in class {self.__class__.__name__}')

    @abstractmethod
    def get_timezone_offset(self, timezone_name: str)  -> float:
        raise NotImplementedError(
            f'Method {self.__class__.get_timezone_offset.__name__} not implemented in class {self.__class__.__name__}')

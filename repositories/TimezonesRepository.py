from db.model import Timezones
from repositories.AbstractRepositories import AbstractTimezonesRepository


class TimezonesRepository(AbstractTimezonesRepository):
    def _get_first_by_timezone(self, timezone_name: str) -> Timezones:
        return self.query.filter_by(time_zone=timezone_name).first()

    def get_timezone_offset(self, timezone_name: str) -> float:
        return self._get_first_by_timezone(timezone_name).offset

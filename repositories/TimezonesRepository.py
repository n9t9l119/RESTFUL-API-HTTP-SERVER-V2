from db.model import Timezones


class TimezonesRepository:
    def get_first_by_timezone(self, timezone):
        return Timezones.query.filter_by(time_zone=timezone).first()

    def get_timezone_offset(self, timezone: Timezones):
        return timezone.offset

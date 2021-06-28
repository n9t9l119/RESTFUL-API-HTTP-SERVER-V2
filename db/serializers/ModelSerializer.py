from typing import Dict, Any

from db.model import GeoInfo, NameId, Timezones


class ModelSerializer:
    @staticmethod
    def serialize_geo_info(geo_item: GeoInfo, alternames=None) -> Dict[str, Any]:
        return {'geonameid': geo_item.geonameid,
                'name': geo_item.name,
                'asciiname': geo_item.asciiname,
                'alternatenames': alternames if alternames else "", 'latitude': geo_item.latitude,
                'longitude': geo_item.longitude,
                'feature class': geo_item.feature_class,
                'feature_code': geo_item.feature_code,
                'country_code': geo_item.country_code,
                'cc2': geo_item.cc2,
                'admin1_code': geo_item.admin1_code,
                'admin2_code': geo_item.admin2_code,
                'admin3_code': geo_item.admin3_code,
                'admin4_code': geo_item.admin4_code,
                'population': geo_item.population,
                'elevation': geo_item.elevation,
                'dem': geo_item.dem,
                'timezone': geo_item.timezone,
                'modification_date': geo_item.modification_date
                }

    @staticmethod
    def deserialize_geo_info(geo_info) -> GeoInfo:
        return GeoInfo(
            geonameid=geo_info.get('geonameid'),
            name=geo_info.get('name'),
            asciiname=geo_info.get('asciiname'),
            alternatenames=geo_info.get('alternatenames'),
            latitude=geo_info.get('latitude'),
            longitude=geo_info.get('longitude'),
            feature_class=geo_info.get('feature_class'),
            feature_code=geo_info.get('feature_code'),
            country_code=geo_info.get('country_code'),
            cc2=geo_info.get('cc2'),
            admin1_code=geo_info.get('admin1_code'),
            admin2_code=geo_info.get('admin2_code'),
            admin3_code=geo_info.get('admin3_code'),
            admin4_code=geo_info.get('admin4_code'),
            population=geo_info.get('population'),
            elevation=geo_info.get('elevation'),
            dem=geo_info.get('dem'),
            timezone=geo_info.get('timezone'),
            modification_date=geo_info.get('modification_date'))

    @staticmethod
    def deserialize_name_id(name_id) -> NameId:
        return NameId(name=name_id.get('name'), idlnk=name_id.get('idlnk'))

    @staticmethod
    def deserialize_timezones(timezones) -> Timezones:
        return Timezones(time_zone=timezones.get('time_zone'), offset=timezones.get('offset'))

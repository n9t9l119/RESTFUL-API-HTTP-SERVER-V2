from db.model import GeoInfo


class GeoInfoSerializer:
    def serialize(self, json):
        return GeoInfo(
            geonameid=json.get('geonameid'),
            name=json.get('name'),
            asciiname=json.get('asciiname'),
            alternatenames=json.get('alternatenames'),
            latitude=json.get('latitude'),
            longitude=json.get('longitude'),
            feature_class=json.get('feature_class'),
            feature_code=json.get('feature_code'),
            country_code=json.get('country_code'),
            cc2=json.get('cc2'),
            admin1_code=json.get('admin1_code'),
            admin2_code=json.get('admin2_code'),
            admin3_code=json.get('admin3_code'),
            admin4_code=json.get('admin4_code'),
            population=json.get('population'),
            elevation=json.get('elevation'),
            dem=json.get('dem'),
            timezone=json.get('timezone'),
            modification_date=json.get('modification_date'))

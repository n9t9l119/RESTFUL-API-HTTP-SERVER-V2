from db.model import GeoInfo


class InfoRepository:

    def get_by_id(self, id):
        return GeoInfo.query.get(id)

    def get_all(self):
        return GeoInfo.query.all()

    def get_first_by_geonameid(self, geonameid):
        return GeoInfo.query.filter_by(geonameid=geonameid).first()

    def get_geo_name(self, geo):
        return geo.name

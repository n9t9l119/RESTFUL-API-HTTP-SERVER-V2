from db.model import NameId


class NameIdRepository:

    def get_all(self):
        return NameId.query.all()

    def get_all_sorted_by_name(self):
        return NameId.query.order_by(NameId.name)

    def get_all_filtered_by_name(self, name):
        return NameId.query.filter_by(name=name)

    def get_all_filtered_by_geonameid(self, geonameid):
        return NameId.query.filter_by(geonameid=geonameid)

    def filter(self, request):
        return NameId.query.filter(NameId.name.ilike(f'%{request}%'))

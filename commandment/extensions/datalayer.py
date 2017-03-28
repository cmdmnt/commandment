from flask_rest_jsonapi.data_layers.alchemy import SqlalchemyDataLayer
from sqlalchemy.inspection import inspect
from sqlalchemy.orm.exc import NoResultFound


class ExtendedSqlalchemyDataLayer(SqlalchemyDataLayer):

    def __init__(self, *args, **kwargs):
        super(ExtendedSqlalchemyDataLayer, self).__init__(*args, **kwargs)

    def get_object(self, view_kwargs):
        """Retrieve an object through sqlalchemy.
        
        This subclass specifically implements an attribute called `is_singleton` which allows the data layer
        to fetch in instances where there can only be one row that is relevant to the view.

        :params dict view_kwargs: kwargs from the resource view
        :return DeclarativeMeta: an object from sqlalchemy
        """
        self.before_get_object(view_kwargs)

        is_singleton = getattr(self, 'is_singleton', False)
        if not is_singleton:
            id_field = getattr(self, 'id_field', inspect(self.model).primary_key[0].name)
            try:
                filter_field = getattr(self.model, id_field)
            except Exception:
                raise Exception("{} has no attribute {}".format(self.model.__name__, id_field))

            url_field = getattr(self, 'url_field', 'id')
            filter_value = view_kwargs[url_field]

            try:
                obj = self.session.query(self.model).filter(filter_field == filter_value).one()
            except NoResultFound:
                obj = None
        else:
            obj = self.session.query(self.model).first()

        self.after_get_object(obj, view_kwargs)

        return obj


from flask.testing import FlaskClient


class MDMClient(FlaskClient):
    def __init__(self, *args, **kwargs):
        self._private_key = kwargs.get('private_key', None)
        self._certificate = kwargs.get('certificate', None)
        
        super(MDMClient, self).__init__(*args, **kwargs)

from flask import Blueprint, current_app
from uuid import uuid4
import plistlib

omdm_app = Blueprint('omdm_app', __name__)


@omdm_app.route('/')
def omdm():
    faux_command = {
        'CommandUUID': str(uuid4()),
        'RequestType': 'OMAlert',
        'Message': 'Hello World!'
    }

    return plistlib.dumps(faux_command), {'Content-Type': 'text/xml'}
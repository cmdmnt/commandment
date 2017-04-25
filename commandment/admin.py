"""
Copyright (c) 2015 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
"""

from flask import Blueprint, render_template, Response, request, redirect, current_app, abort, make_response
#from .pki.certificateauthority import get_ca
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

from .models import CertificateType, Device
from .models import Certificate as DBCertificate, RSAPrivateKey as DBPrivateKey
from .profiles.models import Profile as DBProfile
from .models import App
from .profiles.restrictions import RestrictionsPayload
from .profiles import Profile
from .mdmcmds import InstallProfile, RemoveProfile, AppInstall
from .push import push_to_device
import uuid
import os
from .utils.app_manifest import pkg_signed, get_pkg_bundle_ids, get_chunked_md5, MD5_CHUNK_SIZE
import tempfile
from shutil import copyfile
from email.parser import Parser
import json
#from .utils.dep import DEP
#from .utils.dep_utils import initial_fetch, mdm_profile, assign_devices
import datetime
from urllib.parse import urlparse
from base64 import b64encode


class FixedLocationResponse(Response):
    # override Werkzeug default behaviour of "fixing up" once-non-compliant
    # relative location headers. now permitted in rfc7231 sect. 7.1.2
    autocorrect_location_header = False


admin_app = Blueprint('admin_app', __name__)


@admin_app.route('/')
def index():
    return render_template('index.html')



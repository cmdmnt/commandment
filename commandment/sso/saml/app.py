
from flask import (
    Flask,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from saml2 import (
    BINDING_HTTP_POST,
    BINDING_HTTP_REDIRECT,
    entity,
)
from saml2.client import Saml2Client
from saml2.config import Config as Saml2Config
import requests

metadata_url_for = {
    # For testing with http://saml.oktadev.com use the following:
    'test': 'http://idp.oktadev.com/metadata',
    # WARNING WARNING WARNING
    #   You MUST remove the testing IdP from a production system,
    #   as the testing IdP will allow ANYBODY to log in as ANY USER!
    # WARNING WARNING WARNING
}



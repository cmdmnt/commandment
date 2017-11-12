from flask import Blueprint, current_app, redirect, url_for, request, flash
from . import oauth2

auth_app = Blueprint('auth_app', __name__)
oauth2.init_app(auth_app)


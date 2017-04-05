"""
This module implements the profile delivery service as described in "Over-The-Air profile delivery".
"""
from flask import Blueprint, send_file, abort, current_app, jsonify

ota = Blueprint('ota', __name__)

from flask import Blueprint
from commandment.mdm.resources import CommandsList, CommandDetail
from commandment.api.app_jsonapi import api

api_app = Blueprint('inventory_api_app', __name__)

# Commands
api.route(CommandsList, 'commands_list', '/v1/commands', '/v1/devices/<int:device_id>/commands')
api.route(CommandDetail, 'command_detail', '/v1/commands/<int:command_id>')

'''
Copyright (c) 2015 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
'''

import datetime
from .dep import DEP, DEP4xxError

from ..models import DEPConfig, Device
import uuid
import collections

FETCH_LIMIT = 100
DEP_CHECK_SECONDS = 5 * 60 # 5m in seconds
# DEP_CHECK_SECONDS = 15 # debug testing
DEP_CURSOR_EXPIRE_DAYS = 7

class ExpiredCursor(DEP4xxError):
    body = 'EXPIRED_CURSOR'

def add_or_modify_device(dep, device_dict):
    ser_no = device_dict.get('serial_number')
    if not ser_no:
        return

    try:
        device = db_session.query(Device).filter(Device.serial_number == ser_no).one()
    except NoResultFound:
        device = Device()
        device.serial_number = ser_no
        device.dep_json = device_dict
        db_session.add(device)

    if isinstance(device.dep_json, collections.Mapping):
        device.dep_json.update(device_dict)
    else:
        device.dep_json = device_dict

    device.dep_config = dep

    db_session.commit()

    print('>>>>> ADD/MODIFY DEP DEVICE:', device_dict.get('serial_number'), device_dict.get('model'))
    print(device_dict)

def dep_configs_needing_updates():
    return db_session.query(DEPConfig).filter(
        and_(DEPConfig.server_token != None,
             or_(DEPConfig.initial_fetch_complete == False,
                 DEPConfig.next_check == None,
                 DEPConfig.next_check <= datetime.datetime.utcnow())))

def dep_cursor_retired():
    return datetime.datetime.utcnow() - datetime.timedelta(days=DEP_CURSOR_EXPIRE_DAYS)

def update_dep_configs(dep_configs):
    for dep_config in dep_configs:
        if not dep_config.initial_fetch_complete:
            initial_fetch(dep_config)
        # cursor can only be used for 7 days
        elif dep_config.device_cursor_recevied and dep_config.device_cursor_recevied <= dep_cursor_retired():
            initial_fetch(dep_config)

        else:
            try:
                update_fetch(dep_config)
            except ExpiredCursor:
                print('WARNING: expired cursor; attempting initial fetch')
                initial_fetch(dep_config)

def next_dep_update_datetime():
    return datetime.datetime.utcnow() + datetime.timedelta(seconds=DEP_CHECK_SECONDS)

def cursor_received_datetime():
    return datetime.datetime.utcnow() 

def handle_devices(dep, devices):
    for device in devices:
        operation = device.get('op_type')
        if operation in ('added', 'modified', None):
            add_or_modify_device(dep, device)
        # TODO:
        # elif operation == 'deleted':
        #     delete_device(device)

def initial_fetch(dep):
    # TODO: implement progress tracking in DB? (for admin progress update?)

    def save_session_token(sess):
        dep.auth_session_token = sess
        db_session.commit()

    dep_api = DEP(dep.server_token,
                  dep.auth_session_token,
                  url_base=dep.url_base,
                  new_session_callback=save_session_token)

    cursor = None
    while True:
        input_dict = {'limit': FETCH_LIMIT}

        if cursor:
            input_dict['cursor'] = cursor

        resp = dep_api.auth_api_request('/server/devices', method='POST', input_dict=input_dict)

        cursor = resp.get('cursor')

        handle_devices(dep, resp.get('devices', []))

        if 'more_to_follow' in resp and resp['more_to_follow'] is False:
            break

    dep.next_check = next_dep_update_datetime()
    dep.device_cursor = cursor
    dep.device_cursor_recevied = cursor_received_datetime()
    dep.initial_fetch_complete = True
    db_session.commit()

    return resp

def update_fetch(dep):
    # TODO: implement progress tracking in DB? (for admin progress update?)

    def save_session_token(sess):
        dep.auth_session_token = sess
        db_session.commit()

    dep_api = DEP(dep.server_token,
                  dep.auth_session_token,
                  url_base=dep.url_base,
                  new_session_callback=save_session_token)

    cursor = dep.device_cursor
    initial_cursor = cursor
    while True:
        input_dict = {'limit': FETCH_LIMIT}

        if cursor:
            input_dict['cursor'] = cursor

        resp = dep_api.auth_api_request('/devices/sync', method='POST', input_dict=input_dict)

        cursor = resp.get('cursor')

        handle_devices(dep, resp.get('devices', []))

        if 'more_to_follow' in resp and resp['more_to_follow'] is False:
            break

    dep.next_check = next_dep_update_datetime()
    if cursor != initial_cursor:
        dep.device_cursor = cursor
        dep.device_cursor_recevied = cursor_received_datetime()
    db_session.commit()

    return resp

def mdm_profile(mdm, **options):
    '''Return the "profile" from an MDMConfig

    Note: Not really a configuration profile. Rather a description of the MDM
    environment for devices to attempt enrollment with.
    '''
    enroll_url = str(mdm.base_url() + '/enroll')

    dep_profile = {
        'url': enroll_url,
        # some defaults for the required params in case not provided
        'profile_name': mdm.mdm_name,
        'org_magic': str(uuid.uuid4()),
    }

    dep_profile.update(options)

    return dep_profile

def unsubmitted_dep_profiles():
    return db_session.query(DEPProfile).filter(DEPProfile.uuid == None)

def submit_dep_profiles(dep_profiles):
    for dep_profile in dep_profiles:
        dep = dep_profile.dep_config

        def save_session_token(sess):
            dep.auth_session_token = sess
            db_session.commit()

        dep_api = DEP(dep.server_token,
                      dep.auth_session_token,
                      url_base=dep.url_base,
                      new_session_callback=save_session_token)

        input_dict = dict(dep_profile.profile_data)
        input_dict['devices'] = []

        resp = dep_api.auth_api_request('/profile', method='POST', input_dict=input_dict)

        if 'profile_uuid' in resp:
            dep_profile.uuid = resp['profile_uuid']
            db_session.commit()
            print('DEP profile id %d received UUID %s' % (dep_profile.id, dep_profile.uuid))

def assign_devices(dep_profile, devices):
    dep = dep_profile.dep_config

    def save_session_token(sess):
        dep.auth_session_token = sess
        db_session.commit()

    dep_api = DEP(dep.server_token,
                  dep.auth_session_token,
                  url_base=dep.url_base,
                  new_session_callback=save_session_token)

    input_dict = {'profile_uuid': dep_profile.uuid}
    input_dict['devices'] = []

    for device in devices:
        input_dict['devices'].append(device.serial_number)
        device.dep_json['profile_uuid'] = dep_profile.uuid

    if len(input_dict['devices']) < 1:
        return

    resp = dep_api.auth_api_request('/profile/devices', method='PUT', input_dict=input_dict)

    # TODO: handle non-updated devices/errors
    # TODO: only update profile_uuid for 'SUCCESSFUL' devices after the request
    # TODO: may not need to update profile_uuid (may get a triggered update on
    # subsequent sync calls?)
    print(resp)

    db_session.commit()

    return

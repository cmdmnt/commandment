'''
Copyright (c) 2015 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
'''

from flask import Blueprint, render_template, Response, request, redirect, current_app, abort, make_response
from .pki.ca import get_ca, PushCertificate
from .pki.m2certs import X509Error, Certificate, RSAPrivateKey, CertificateRequest
from .database import db_session, and_, or_
from .pki.m2certs import Certificate
from .models import CERT_TYPES, profile_group_assoc, device_group_assoc, Device
from .models import Certificate as DBCertificate, PrivateKey as DBPrivateKey, MDMGroup, Profile as DBProfile, MDMConfig
from .models import App, DEPConfig, DEPProfile
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
from M2Crypto import SMIME, BIO
import json
from .utils.dep import DEP
from .utils.dep_utils import initial_fetch, mdm_profile, assign_devices

class FixedLocationResponse(Response):
    # override Werkzeug default behaviour of "fixing up" once-non-compliant
    # relative location headers. now permitted in rfc7231 sect. 7.1.2
    autocorrect_location_header = False

admin_app = Blueprint('admin_app', __name__)

@admin_app.route('/certificates')
def admin_certificates():
    # merely to generate new CA if not exist
    mdm_ca = get_ca()

    # get a list of configured system certificates
    cert_rows = db_session.query(DBCertificate).filter(DBCertificate.cert_type != 'mdm.device')

    # assemble a list of dictionaries to pass to our certificate list template
    installed_certs = []
    cert_output = []
    for cert_row in cert_rows:
        installed_certs.append(cert_row.cert_type)
        row_cert = Certificate.load(str(cert_row.pem_certificate))
        dict_row = {
            'id': cert_row.id,
            'name': cert_row.cert_type,
            'subject': row_cert.get_subject_as_text(),
            'title': CERT_TYPES[cert_row.cert_type]['title'] if CERT_TYPES.get(cert_row.cert_type) else '',
            'description': CERT_TYPES[cert_row.cert_type]['description'] if CERT_TYPES.get(cert_row.cert_type) else '',
            'required': bool(CERT_TYPES[cert_row.cert_type].get('required')) if CERT_TYPES.get(cert_row.cert_type) else False,
        }
        cert_output.append(dict_row)

    # assemble all the other required certificate types we know about as options
    missing = []
    for cert_name in set(CERT_TYPES.keys()).difference(set(installed_certs)):
        if cert_name != 'mdm.device':
            dict_row = {
                'name': cert_name,
                'title': CERT_TYPES[cert_name]['title'],
                'description': CERT_TYPES[cert_name]['description'],
                'required': bool(CERT_TYPES[cert_name].get('required')),
            }
            missing.append(dict_row)

    return render_template('admin/certificates/index.html', certs=cert_output, missing=missing)

@admin_app.route('/certificates/add/<certtype>', methods=['GET', 'POST'])
def admin_certificates_add(certtype):
    if certtype not in CERT_TYPES.keys():
        return 'Invalid certificate type' 
    if request.method == 'POST':
        if not request.form.get('certificate'):
            return 'No certificate supplied!'

        try:
            cert = Certificate.load(str(request.form.get('certificate')))
        except X509Error:
            return 'Invalid X509 Certificate'

        if CERT_TYPES[certtype]['pkey_required'] and not request.form.get('privatekey'):
            return 'No private key supplied (required)'

        pkey = None
        try:
            pkey = RSAPrivateKey.load(str(request.form.get('privatekey')))
        except:
            pkey = None

        if pkey:
            if not cert.belongs_to_key(pkey):
                return 'Private key does not match certificate (RSA modulus mismatch)'

        # save our newly uploaded certificates
        dbc = DBCertificate()
        dbc.cert_type = certtype
        dbc.pem_certificate = str(request.form.get('certificate'))
        db_session.add(dbc)

        # save private key if we have one
        if pkey:
            dbk = DBPrivateKey()
            dbk.pem_key = str(request.form.get('privatekey'))
            db_session.add(dbk)

            dbk.certificates.append(dbc)

        db_session.commit()

        return redirect('/admin/certificates', Response=FixedLocationResponse)
    else:
        return render_template('admin/certificates/add.html', certtype=CERT_TYPES[certtype]['title'])

@admin_app.route('/certificates/new', methods=['GET', 'POST'])
def admin_certificates_new():
    approved_certs = ['mdm.webcrt']

    if request.method == 'POST':
        print 'cert type', request.form['cert_type']
        if 'cert_type' not in request.form.keys() or request.form['cert_type'] not in approved_certs:
            abort(400, 'Invalid cert_type!')

        # all certs must have a CN?
        if 'CN' not in request.form.keys() or not request.form['CN']:
            abort(400, 'No common name!')

        approved_input = ('C', 'CN', 'OU', 'L', 'O', 'ST')

        # get dictionary of any appropriate fields submitted
        subject_names = {}
        for i in request.form.keys():
            if i in approved_input:
                subject_names.update({i: str(request.form[i])})

        print 'Generating test web certificate and CA'
        new_pk = RSAPrivateKey()

        # generate csr
        # XXX: TODO: Great unsanitized input, batman!
        new_csr = CertificateRequest(new_pk, **subject_names)

        # create (and self-sign) the web certificate request
        new_crt = Certificate.cacert_from_req(new_csr)

        # save CA private key in DB
        db_new_pk = DBPrivateKey()
        db_new_pk.pem_key = new_pk.get_pem()

        db_session.add(db_new_pk)

        # save certificate
        db_new_crt = DBCertificate()
        db_new_crt.cert_type = request.form['cert_type']
        db_new_crt.pem_certificate = new_crt.get_pem()

        db_session.add(db_new_crt)

        # add certificate to private key
        db_new_pk.certificates.append(db_new_crt)

        db_session.commit()

        # after successful addition
        return redirect('/admin/certificates', Response=FixedLocationResponse)
    else:
        cert_types = {}
        for i in approved_certs:
            cert_types[i] = CERT_TYPES[i]['title']

        return render_template('admin/certificates/new.html', cert_types=cert_types)

@admin_app.route('/certificates/delete/<int:cert_id>')
def admin_certificates_delete(cert_id):
    certq = db_session.query(DBCertificate).filter(DBCertificate.id == cert_id)
    cert = certq.one()
    db_session.delete(cert)
    db_session.commit()
    return redirect('/admin/certificates', Response=FixedLocationResponse)

@admin_app.route('/groups', methods=['GET', 'POST'])
def admin_groups():
    if request.method == 'POST':
        db_grp = MDMGroup()
        db_grp.group_name = request.form['group_name']
        db_grp.description = request.form['description']
        db_session.add(db_grp)
        db_session.commit()

        return redirect('/admin/groups', Response=FixedLocationResponse)

    groups = db_session.query(MDMGroup)

    return render_template('admin/groups.html', groups=groups)

@admin_app.route('/groups/remove/<int:group_id>')
def admin_groups_remove(group_id):
    q = db_session.query(MDMGroup).filter(MDMGroup.id == group_id).delete(synchronize_session=False)
    db_session.commit()
    return redirect('/admin/groups', Response=FixedLocationResponse)

@admin_app.route('/profiles')
def admin_profiles1():
    profiles = db_session.query(DBProfile)
    return render_template('admin/profiles/index.html', profiles=profiles)

@admin_app.route('/profiles/add', methods=['GET', 'POST'])
def admin_profiles_add1():
    if request.method == 'POST':
        config = db_session.query(MDMConfig).one()

        myrestr = RestrictionsPayload(config.prefix + '.tstRstctPld', allowiTunes=(request.form.get('allowiTunes') == 'checked'))

        # generate us a unique identifier that shouldn't change for this profile
        myidentifier = config.prefix + '.profile.' + str(uuid.uuid4())

        myprofile = Profile(myidentifier, PayloadDisplayName='Test1 Restrictions')

        myprofile.append_payload(myrestr)

        db_prof = DBProfile()

        db_prof.identifier = myidentifier
        db_prof.uuid = myprofile.get_uuid()

        db_prof.profile_data = myprofile.generate_plist()

        db_session.add(db_prof)
        db_session.commit()

        return redirect('/admin/profiles', Response=FixedLocationResponse)
    else:
        return render_template('admin/profiles/add.html')

@admin_app.route('/profiles/edit/<int:profile_id>', methods=['GET', 'POST'])
def admin_profiles_edit1(profile_id):
    # db_session
    if request.method == 'POST':
        db_prof = db_session.query(DBProfile).filter(DBProfile.id == profile_id).one()

        myprofile = Profile.from_plist(db_prof.profile_data)

        # TODO: need an API to *get* a profile out
        # TODO: assuming first payload is ours. bad, bad.
        mypld = myprofile.payloads[0]

        mypld.payload['allowiTunes'] = (request.form.get('allowiTunes') == 'checked')

        # assume changed, reset UUIDs
        myprofile.set_uuid()
        mypld.set_uuid()

        db_prof.uuid = myprofile.set_uuid()

        db_prof.profile_data = myprofile.generate_plist()

        db_session.commit()

        return redirect('/admin/profiles', Response=FixedLocationResponse)
    else:
        db_prof = db_session.query(DBProfile).filter(DBProfile.id == profile_id).one()

        # get all MDMGroups left joining against our assoc. table to see if this profile is in any of those groups
        group_q = db_session.query(MDMGroup, profile_group_assoc.c.profile_id).outerjoin(profile_group_assoc, and_(profile_group_assoc.c.mdm_group_id == MDMGroup.id, profile_group_assoc.c.profile_id == db_prof.id))

        myprofile = Profile.from_plist(db_prof.profile_data)

        # TODO: need an API to *get* a profile out
        # TODO: assuming first payload is ours. bad, bad.
        mypld = myprofile.payloads[0]

        return render_template('admin/profiles/edit.html', identifier=myprofile.get_identifier(), uuid=myprofile.get_uuid(), allowiTunes=mypld.payload['allowiTunes'], id=db_prof.id, groups=group_q)

@admin_app.route('/profiles/groupmod/<int:profile_id>', methods=['POST'])
def admin_profiles_groupmod1(profile_id):
    # get device info
    profile = db_session.query(DBProfile).filter(DBProfile.id == profile_id).one()

    # get all groups
    groups = db_session.query(MDMGroup)

    # get integer list of unique group IDs to be assigned
    new_group_memberships = set([int(g_id) for g_id in request.form.getlist('group_membership')])

    # select the groups that match the new membership ids and assign to profile
    profile.mdm_groups = [g for g in groups if g.id in new_group_memberships]

    # commit our changes
    db_session.commit()

    # TODO: trigger group membership profile commands for the *entire group*

    return redirect('/admin/profiles/edit/%d' % int(profile.id), Response=FixedLocationResponse)


@admin_app.route('/profiles/remove/<int:profile_id>')
def admin_profiles_remove1(profile_id):
    q = db_session.query(DBProfile).filter(DBProfile.id == profile_id).delete(synchronize_session=False)
    db_session.commit()
    return redirect('/admin/profiles', Response=FixedLocationResponse)

@admin_app.route('/devices')
def devices():
    devices = db_session.query(Device)

    for i in devices:
        if i.info_json is None:
            i.info_json = {}

    return render_template('admin/devices.html', devices=devices)

@admin_app.route('/device/<int:device_id>')
def admin_device(device_id):
    device = db_session.query(Device).filter(Device.id == device_id).one()

    # get all MDMGroups left joining against our assoc. table to see if this device is in any of those groups
    group_q = db_session.query(MDMGroup, device_group_assoc.c.device_id).outerjoin(device_group_assoc, and_(device_group_assoc.c.mdm_group_id == MDMGroup.id, device_group_assoc.c.device_id == device.id))

    apps = db_session.query(App.id, App.filename)

    return render_template('admin/device.html', device=device, groups=group_q, apps=apps)

def install_group_profiles_to_device(group, device):
    q = db_session.query(DBProfile.id).join(profile_group_assoc).filter(profile_group_assoc.c.mdm_group_id == group.id)

    # note singular tuple for subject here
    for profile_id, in q:
        new_qc = InstallProfile.new_queued_command(device, {'id': profile_id})
        db_session.add(new_qc)

def remove_group_profiles_from_device(group, device):
    q = db_session.query(DBProfile.identifier).join(profile_group_assoc).filter(profile_group_assoc.c.mdm_group_id == group.id)

    # note singular tuple for subject here
    for profile_identifier, in q:
        print 'Queueing removal of profile identifier:', profile_identifier
        new_qc = RemoveProfile.new_queued_command(device, {'Identifier': profile_identifier})
        db_session.add(new_qc)

@admin_app.route('/device/<int:device_id>/groupmod', methods=['POST'])
def admin_device_groupmod(device_id):
    # get device info
    device = db_session.query(Device).filter(Device.id == device_id).one()

    # get list of unique group IDs to be assigned
    new_group_memberships = set([int(g_id) for g_id in request.form.getlist('group_membership')])

    # get all MDMGroups left joining against our assoc. table to see if this device is in any of those groups
    group_q = db_session.query(MDMGroup, device_group_assoc.c.device_id).outerjoin(device_group_assoc, and_(device_group_assoc.c.mdm_group_id == MDMGroup.id, device_group_assoc.c.device_id == device.id))

    group_additions = []
    group_removals = []
    for group, dev_id in group_q:
        if dev_id:
            # this device is in this group currently
            if group.id not in new_group_memberships:
                # this device is being removed from this group!
                print 'Device %d is being REMOVED from Group %d (%s)!' % (device.id, group.id, group.group_name)
                group_removals.append(group)
            # else:
            #   print 'Device %d is REMAINING in Group %d (%s)!' % (device.id, group.id, group.group_name)
        else:
            # this device is NOT in this group currently
            if group.id in new_group_memberships:
                print 'Device %d is being ADDED to Group %d (%s)!' % (device.id, group.id, group.group_name)
                group_additions.append(group)
            # else:
            #   print 'Device %d is REMAINING out of Group %d (%s)!' % (device.id, group.id, group.group_name)

    # get all groups
    groups = db_session.query(MDMGroup)

    # select the groups that match the new membership ids and assign to device
    device.mdm_groups = [g for g in groups if g.id in new_group_memberships]

    # commit our changes
    db_session.commit()

    for i in group_additions:
        install_group_profiles_to_device(i, device)

    for i in group_removals:
        remove_group_profiles_from_device(i, device)

    if group_removals or group_additions:
        db_session.commit()
        push_to_device(device)

    return redirect('/admin/device/%d' % int(device.id), Response=FixedLocationResponse)

@admin_app.route('/device/<int:device_id>/appinst', methods=['POST'])
def admin_device_appinst(device_id):
    # get device info
    device = db_session.query(Device).filter(Device.id == device_id).one()

    # get app id
    app_id = int(request.form['application'])

    # note singular tuple for subject here
    new_appinst = AppInstall.new_queued_command(device, {'app_id': app_id})
    db_session.add(new_appinst)
    db_session.commit()
    push_to_device(device)

    return redirect('/admin/device/%d' % device_id, Response=FixedLocationResponse)

@admin_app.route('/apps', methods=['GET'])
def admin_app_list():
    apps = db_session.query(App)
    return render_template('admin/apps.html', apps=apps)

@admin_app.route('/app/add', methods=['POST'])
def admin_app_add():

    new_file = request.files['app']

    if not new_file.filename.endswith('.pkg'):
        abort(400, 'Failed: filename does not end with ".pkg". Upload must be an Apple Developer-signed Apple "flat" package installer.')

    # first, save the file to a temporary location. ideally we'd like to read
    # the temporary file it's already contained in but Werkzeug only seems to
    # give us access to the file handle of that (.stream attribute) and not a
    # filename that we need. this implies we'll need to copy the file twice
    # (once out of the temporary stream to this temp file, then once into the
    # uploaded location).
    temp_file_handle, temp_file_path = tempfile.mkstemp()

    new_file.save(temp_file_path)

    if not pkg_signed(temp_file_path):
        os.close(temp_file_handle)
        os.unlink(temp_file_path)
        abort(400, 'Failed: uploaded package not signed. Upload must be an Apple Developer-signed Apple "flat" package installer.')

    # get MD5 and MD5 chunks
    md5, md5s = get_chunked_md5(temp_file_path, chunksize=MD5_CHUNK_SIZE)

    # get bundle and package IDs
    pkg_ids, bundle_ids = get_pkg_bundle_ids(temp_file_path)

    filesize = os.path.getsize(temp_file_path)

    new_app = App()
    new_app.filename = new_file.filename
    new_app.filesize = filesize

    new_app.md5_hash = md5
    new_app.md5_chunk_size = MD5_CHUNK_SIZE
    new_app.md5_chunk_hashes = ':'.join(md5s)

    new_app.pkg_ids_json = pkg_ids
    new_app.bundle_ids_json = bundle_ids

    db_session.add(new_app)
    db_session.commit()

    apps_dir = os.path.join(current_app.root_path, current_app.config['APP_UPLOAD_ROOT'])

    if not os.path.isdir(apps_dir):
        os.mkdir(apps_dir)

    new_file_path = os.path.join(apps_dir, new_app.path_format())

    copyfile(temp_file_path, new_file_path)
    # new_file.save(new_file_path)

    # remove the temp file
    os.close(temp_file_handle)
    os.unlink(temp_file_path)

    return redirect('/admin/apps', Response=FixedLocationResponse)

@admin_app.route('/app/delete/<int:app_id>', methods=['GET'])
def admin_app_delete(app_id):
    app_q = db_session.query(App).filter(App.id == app_id)
    app = app_q.one()

    apps_dir = os.path.join(current_app.root_path, current_app.config['APP_UPLOAD_ROOT'])

    try:
        os.unlink(os.path.join(apps_dir, app.path_format()))
    except OSError:
        # just continue on -- best effort for deletion
        pass

    db_session.delete(app)
    db_session.commit()

    return redirect('/admin/apps', Response=FixedLocationResponse)

@admin_app.route('/config/add', methods=['GET', 'POST'])
def admin_config_add():
    mdm_ca = get_ca()

    if request.method == 'POST':
        push_cert = db_session.query(DBCertificate).filter(DBCertificate.id == int(request.form['push_cert'])).one()

        cert = PushCertificate.load(str(push_cert.pem_certificate))

        topic = cert.get_topic()

        new_config = MDMConfig()

        new_config.topic = topic

        base_url = 'https://' + request.form['hostname']

        if request.form['port']:
            portno = int(request.form['port'])

            if portno < 1 or portno > (2 ** 16):
                abort(400, 'Invalid port number')

            base_url += ':%d' % portno

        new_config.mdm_url = base_url + '/mdm'
        new_config.checkin_url = base_url + '/checkin'

        new_config.mdm_name = request.form['name']
        new_config.description = request.form['description'] if request.form['description'] else None
        new_config.prefix = request.form['prefix'].rstrip('.')

        # TODO: validate this input (but DB constraints should catch it, too)
        new_config.ca_cert_id = int(request.form['ca_cert'])

        new_config.push_cert = push_cert

        db_session.add(new_config)
        db_session.commit()

        return redirect('/admin/config/edit', Response=FixedLocationResponse)
    else:
        # get relevant certificates
        q = db_session.query(DBCertificate).join(DBPrivateKey.certificates).filter(or_(DBCertificate.cert_type == 'mdm.cacert', DBCertificate.cert_type == 'mdm.pushcert'))

        ca_certs = []
        push_certs = []
        for i in q:
            if i.cert_type == 'mdm.pushcert':
                cert = PushCertificate.load(str(i.pem_certificate))
                topic = cert.get_topic()
                i.subject_text = topic
                push_certs.append(i)
            elif i.cert_type == 'mdm.cacert':
                cert = Certificate.load(str(i.pem_certificate))
                i.subject_text = cert.get_subject_as_text()
                ca_certs.append(i)

        if not push_certs or not ca_certs:
            return redirect('/admin/certificates', Response=FixedLocationResponse)

        return render_template('admin/config/add.html', ca_certs=ca_certs, push_certs=push_certs)

@admin_app.route('/config/edit', methods=['GET', 'POST'])
def admin_config():
    config = db_session.query(MDMConfig).first()
    if not config:
        return redirect('/admin/config/add', Response=FixedLocationResponse)
    if request.method == 'POST':
        config.ca_cert_id = int(request.form['ca_cert'])
        config.mdm_name = request.form['name']
        config.description = request.form['description'] if request.form['description'] else None
        db_session.commit()
        return redirect('/admin/config/edit', Response=FixedLocationResponse)
    else:
        ca_certs = db_session.query(DBCertificate).join(DBPrivateKey.certificates).filter(DBCertificate.cert_type == 'mdm.cacert')
        for i in ca_certs:
            cert = Certificate.load(str(i.pem_certificate))
            i.subject_text = cert.get_subject_as_text()
        print type(config.description)
        return render_template('admin/config/edit.html', config=config, ca_certs=ca_certs)

@admin_app.route('/dep/')
@admin_app.route('/dep/index')
def dep_index():
    dep_configs = db_session.query(DEPConfig)
    dep_profiles = db_session.query(DEPProfile)
    return render_template('admin/dep/index.html', dep_configs=dep_configs, dep_profiles=dep_profiles)

@admin_app.route('/dep/add')
def dep_add():

    new_dep = DEPConfig()

    ca_cert = DBCertificate.find_one_by_cert_type('mdm.cacert')

    new_dep.certificate = ca_cert

    db_session.add(new_dep)
    db_session.commit()

    return redirect('/admin/dep/index', Response=FixedLocationResponse)

@admin_app.route('/dep/manage/<int:dep_id>')
def dep_manage(dep_id):
    dep = db_session.query(DEPConfig).filter(DEPConfig.id == dep_id).one()
    return render_template('admin/dep/manage.html', dep_config=dep)

@admin_app.route('/dep/cert/<int:dep_id>/DEP_MDM.crt')
def dep_cert(dep_id):
    dep = db_session.query(DEPConfig).filter(DEPConfig.id == dep_id).one()
    # TODO: better to use a join rather than two queries
    response = make_response(dep.certificate.pem_certificate)
    # TODO: technically we really ought to use a proper MIME type but since
    # some browsers do fancy stuff when downloading properly typed certs for
    # now just use an octet-stream
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = 'attachment; filename=DEP_MDM.crt'
    return response

@admin_app.route('/dep/tokenupload/<int:dep_id>', methods=['POST'])
def dep_tokenupload(dep_id):
    # get DEP config
    dep = db_session.query(DEPConfig).filter(DEPConfig.id == dep_id).one()

    filedata = request.files['server_token_file'].stream.read()

    try:
        smime = filedata

        # load the encrypted file
        p7, data = SMIME.smime_load_pkcs7_bio(BIO.MemoryBuffer(str(smime)))

        # query DB to get cert & key from DB
        q = db_session.query(DBCertificate, DBPrivateKey).join(DBCertificate, DBPrivateKey.certificates).filter(DBCertificate.id == dep.certificate.id)
        cert, pk = q.one()

        # construct SMIME object using cert & key
        decryptor = SMIME.SMIME()
        decryptor.load_key_bio(BIO.MemoryBuffer(str(pk.pem_key)), BIO.MemoryBuffer(str(cert.pem_certificate)))

        # decrypt!
        out = decryptor.decrypt(p7)

        eml = Parser().parsestr(out).get_payload()

        if eml.startswith('-----BEGIN MESSAGE-----\n') and eml.endswith('\n-----END MESSAGE-----\n'):
            myjson = eml[24:-23]
    except SMIME.SMIME_Error:
        # submitted file was not an SMIME encrypted file
        # try to just load the file in the hopes the json parser can read it
        myjson = filedata

    try:
        json_loaded = json.loads(myjson)

        dep.server_token = json_loaded
        db_session.commit()
    except ValueError:
        abort(400, 'Invalid server token supplied')

    return redirect('/admin/dep/index', Response=FixedLocationResponse)

@admin_app.route('/dep/profile/add', methods=['GET', 'POST'])
def dep_profile_add():
    if request.method == 'POST':
        form_bools = ('allow_pairing', 'is_supervised', 'is_multi_user', 'is_mandatory', 'is_mdm_removable')
        form_strs = ('profile_name', 'support_phone_number', 'support_email_address', 'department', 'org_magic')

        profile = {}

        # go through submitted bools and convert to actual bools in the dict
        for form_bool in form_bools:
            if request.form.has_key(form_bool):
                profile[form_bool] = request.form.get(form_bool, type=bool)

        # go through submitted strs and convert to actual bools in the dict
        for form_str in form_strs:
            if request.form.has_key(form_str) and request.form.get(form_str):
                profile[form_str] = request.form.get(form_str)

        if not 'profile_name' in profile:
            raise Exception('DEP profile must have profile_name')

        # gather our skip_setup_items from the form
        if request.form.has_key('skip_setup_items'):
            profile['skip_setup_items'] = request.form.getlist('skip_setup_items')

        # TODO: await_device_configured

        dep = db_session.query(DEPConfig).filter(DEPConfig.id == request.form.get('dep_config_id', type=int)).one()
        mdm = db_session.query(MDMConfig).filter(MDMConfig.id == request.form.get('mdm_config_id', type=int)).one()

        profile['url'] = mdm.base_url() + '/enroll'

        # find and include all mdm.webcrt's
        anchor_certs = []
        q = db_session.query(DBCertificate).filter(DBCertificate.cert_type == 'mdm.webcrt')
        for dbcert in q:
            cert = Certificate.load(str(dbcert.pem_certificate))
            anchor_certs.append(cert.get_der().encode('base64'))

        if anchor_certs:
            profile['anchor_certs'] = anchor_certs

        new_dep_profile = DEPProfile()

        new_dep_profile.mdm_config = mdm
        new_dep_profile.dep_config = dep

        new_dep_profile.profile_data = profile

        # TODO: supervising_host_certs
        # TODO: initial list of devices?

        db_session.add(new_dep_profile)
        db_session.commit()

        return redirect('/admin/dep/index', Response=FixedLocationResponse)

    else:
        mdms = db_session.query(MDMConfig)
        deps = db_session.query(DEPConfig)
        return render_template('admin/dep/add_profile.html', dep_configs=deps, mdm_configs=mdms, initial_magic=uuid.uuid4())

@admin_app.route('/dep/profile/manage/<int:profile_id>', methods=['GET', 'POST'])
def dep_profile_manage(profile_id):
    dep_profile = db_session.query(DEPProfile).filter(DEPProfile.id == profile_id).one()
    if request.method != 'POST':
        return render_template('admin/dep/manage_profile.html', dep_profile=dep_profile)
    else:
        submitted_dev_ids = [int(i) for i in request.form.getlist('devices')]
        if len(submitted_dev_ids):
            devices = db_session.query(Device).filter(and_(Device.dep_config == dep_profile.dep_config, or_(*[Device.id == i for i in submitted_dev_ids])))
            assign_devices(dep_profile, devices)
        return 'tbd'

@admin_app.route('/dep/test1/<int:dep_id>')
def dep_test1(dep_id):
    # get DEP config
    mdm = db_session.query(MDMConfig).one()
    dep = db_session.query(DEPConfig).filter(DEPConfig.id == dep_id).one()

    initial_fetch(dep)

    return 'initial_fetch complete'
    # return '<pre>%s</pre>' % str(mdm_profile(mdm))

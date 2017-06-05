from flask import Blueprint, jsonify

ac2_app = Blueprint('ac2_app', __name__)


@ac2_app.route('/MDMServiceConfig')
def mdm_service_config():
    """Apple Configurator 2 checks this route to figure out which enrollment profile it should use."""
    return jsonify({
        'dep_enrollment_url': 'https://commandment.dev:5443/devicemanagement/mdm/dep_mdm_enroll',
        'dep_anchor_certs_url': '/devicemanagement/mdm/dep_anchor/certs',
        'trust_profile_url': '/mdm/trust_profile'
    })

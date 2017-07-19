from flask import Blueprint, jsonify, current_app

ac2_app = Blueprint('ac2_app', __name__)


@ac2_app.route('/MDMServiceConfig')
def mdm_service_config():
    """Apple Configurator 2 checks this route to figure out which enrollment profile it should use."""
    public_hostname = current_app.config.get('PUBLIC_HOSTNAME', 'localhost')
    port = current_app.config.get('PORT', 443)

    return jsonify({
        'dep_enrollment_url': 'https://{}:{}/dep/profile'.format(public_hostname, port),
        'dep_anchor_certs_url': 'https://{}:{}/dep/anchor_certs'.format(public_hostname, port),
        'trust_profile_url': 'https://{}:{}/enroll/trust.mobileconfig'.format(public_hostname, port)
    })

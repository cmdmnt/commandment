from flask import g, current_app

from commandment.vpp.errors import VPPError
from commandment.vpp.vpp import VPP


def get_vpp() -> VPP:
    vpp = getattr(g, '_vpp', None)

    if vpp is None:
        if 'VPP_STOKEN' not in current_app.config:
            raise VPPError('VPP stoken not configured')

        g._vpp = VPP(current_app.config['VPP_STOKEN'])

    return vpp

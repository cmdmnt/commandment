from flask import g, current_app
from commandment.vpp.vpp import VPP


def get_vpp() -> VPP:
    vpp = getattr(g, '_vpp', None)

    if vpp is None:
        g._vpp = VPP(current_app.config['VPP_STOKEN'])

    return vpp

from flask import g
from commandment.vpp.vpp import VPP


def get_vpp() -> VPP:
    vpp = getattr(g, '_vpp', None)

    if vpp is None:
        return None  # TODO: Finish
import functools

from commandment.vpp.errors import VPPError


def raise_error_replies(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        reply = f(*args, **kwargs)
        if 'status' in reply and reply['status'] == -1:  # VPP Error occurred
            raise VPPError('{} ({})'.format(reply['errorMessage'], reply['errorNumber']))
        return reply

    return wrapper

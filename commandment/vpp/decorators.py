import functools

from commandment.vpp.errors import VPPAPIError


def raise_error_replies(f):
    """Decorator which wraps a function that returns the dict representing a direct response body from the VPP service.

    The reply is checked for VPP errors and, if there are any errors, the error is raised as a VPPAPIError exception.
    """
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        reply = f(*args, **kwargs)
        if reply['status'] == -1:  # VPP Error occurred
            raise VPPAPIError(reply['errorNumber'], reply['errorMessage'])
        return reply

    return wrapper

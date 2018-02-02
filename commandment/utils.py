from flask import current_app
import plistlib


def plistify(*args, **kwargs):
    """Similar to jsonify, which ships with Flask, this function wraps plistlib.dumps and sets up the correct
    mime type for the response."""
    if args and kwargs:
        raise TypeError('plistify() behavior undefined when passed both args and kwargs')
    elif len(args) == 1:  # single args are passed directly to dumps()
        data = args[0]
    else:
        data = args or kwargs

    return current_app.response_class(
        (plistlib.dumps(data), '\n'),
        mimetype=current_app.config['PLISTIFY_MIMETYPE']
    )

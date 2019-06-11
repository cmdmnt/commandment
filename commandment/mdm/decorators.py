from functools import wraps


def handle_error_status(func):
    """This decorator looks at the request for an Error status, then handles the error accordingly:

    """
    @wraps(func)
    def handler(*args, **kwargs):
        return func(*args, **kwargs)
    return handler



from requests import Response, HTTPError


class DEPError(HTTPError):
    """DEPError inherits from request's HTTPError to provide the response and request as part of the exception.

    Additionally, the error tracks information about the body content as this can sometimes be the only way to
    distinguish an error.

    Attributes:
          text (str): The reserved string that was returned in the error body.
    """
    def __init__(self, *args, **kwargs):
        super(DEPError, self).__init__(*args, **kwargs)
        if 'response' in kwargs:
            # Quote characters (") must be stripped, because the body may contain the reason inside double quotes.
            self.text = kwargs.get('response').content.strip("\"\n\r")
        else:
            self.text = "NO_REASON_GIVEN"

    def __str__(self):
        return '{}: {}'.format(self.response.status_code, self.text)

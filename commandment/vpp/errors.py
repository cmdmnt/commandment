class VPPTokenInvalid(Exception):
    """When an invalid token is given to VPP"""
    pass


class VPPTokenExpired(Exception):
    """When an expired token is given to VPP"""
    pass


class VPPRetryAfter(Exception):
    """When the service has a `Retry-After` header"""
    pass


class VPPTransportError(Exception):
    """VPP Service returned a non 2xx code or could not connect to the VPP service."""
    pass


class VPPError(Exception):
    """Generic error used when the service returns an error of any kind"""
    pass

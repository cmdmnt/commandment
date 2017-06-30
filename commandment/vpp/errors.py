class VPPTokenExpired(Exception):
    """When an expired token is given to VPP"""
    pass


class VPPRetryAfter(Exception):
    """When the service has a `Retry-After` header"""
    pass


class VPPTransportError(Exception):
    """VPP Service returned a non 2xx code or could not connect to the VPP service."""
    pass


class VPPServiceError(Exception):
    """When the service returns an errorNumber"""
    pass

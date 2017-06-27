class VPPTokenExpired(Exception):
    """When an expired token is given to VPP"""
    pass


class VPPRetryAfter(Exception):
    """When the service has a `Retry-After` header"""
    pass


class VPPServiceError(Exception):
    """When the service returns an errorNumber"""
    pass

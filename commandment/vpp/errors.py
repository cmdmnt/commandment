from enum import IntEnum


class VPPErrorType(IntEnum):
    """An enumeration representation of all (currently) possible error codes returned by the VPP API."""
    
    MissingArgument = 9600
    LoginRequired = 9601
    InvalidArgument = 9602
    InternalError = 9603
    ResultNotFound = 9604
    AccountStorefrontIncorrect = 9605
    ErrorConstructingToken = 9606
    LicenseIrrevocable = 9607
    EmptyResponseFromSharedData = 9608
    UserNotFound = 9609
    LicenseNotFound = 9610
    AdminNotFound = 9611
    FailedCreatingClaimJob = 9612
    FailedCreatingUnclaimJob = 9613
    InvalidDateFormat = 9614
    OrgCountryNotFound = 9615
    LicenseAlreadyAssigned = 9616
    UserAlreadyRetired = 9618
    LicenseNotAssociated = 9619
    UserAlreadyDeleted = 9620
    TokenExpired = 9621
    InvalidAuthenticationToken = 9622
    InvalidAPNSToken = 9623
    LicenseRefunded = 9624
    STokenRevoked = 9625
    LicenseAlreadyAssignedUser = 9626
    DeviceAssignmentNotAllowed = 9628
    TooManyAssignmentErrors = 9630
    TooManyNoLicenseErrors = 9631
    TooManyDuplicateAssignments = 9632
    DataBatchUnrecoverable = 9633
    Deprecated = 9634
    AppleIDInvalid = 9635
    RegisteredUserNotFound = 9636
    STokenPermissionDenied = 9637
    FacilitatorHasNoManagedID = 9638
    FacilitatorMemberIDNotFound = 9639
    FacilitatorDetailsNotAvailable = 9640
    

class VPPError(Exception):
    """Generic error used when the service returns an error of any kind"""
    pass


class VPPAPIError(VPPError):
    """If the VPP API returns an error code, it is raised using this error class.

    Attributes:
          errno (int): The errorNumber
          message (str): The error message
    """
    def __init__(self, errno, message):
        self.errno = errno
        self.message = message

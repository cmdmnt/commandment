"""
Copyright (c) 2015 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
"""

from enum import IntFlag


class KeyUsage(IntFlag):
    """Intended key usage flag. Used in SCEP payload."""
    Signing = 1
    Encryption = 4
    All = Signing | Encryption

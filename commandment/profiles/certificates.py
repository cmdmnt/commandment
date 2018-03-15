"""
Copyright (c) 2015 Jesse Peterson, 2017 Mosen
Licensed under the MIT license. See the included LICENSE.txt file for details.
"""

from enum import IntFlag
from marshmallow import Schema, fields, post_load, post_dump


class KeyUsage(IntFlag):
    """Intended key usage flag. Used in SCEP payload."""
    Signing = 1
    Encryption = 4
    All = Signing | Encryption

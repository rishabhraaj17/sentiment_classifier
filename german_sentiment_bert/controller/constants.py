# -*- coding: utf-8 -*-

from enum import Enum


class ResponseCode(Enum):
    SYSTEM_AVAILABLE = "SYSTEM_AVAILABLE"
    SYSTEM_CHECK_OK = "SYSTEM_CHECK_OK"
    SYSTEM_CHECK_FAILED = "SYSTEM_CHECK_FAILED"

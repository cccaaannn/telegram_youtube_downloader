from enum import Enum


class AuthorizationMode(Enum):
    DISABLED = "DISABLED"
    ALLOW_SELECTED = "ALLOW_SELECTED"
    BLOCK_SELECTED = "BLOCK_SELECTED"
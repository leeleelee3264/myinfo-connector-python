from enum import unique, Enum

from rest_framework.response import Response


def _remove_none_values(data):
    return {k: v for k, v in data.items() if v is not None}


class APIResponse(Response):
    @unique
    class Code(Enum):
        ALREADY_EXIST = 'ALREADY_EXIST'
        NOT_EXIST = 'NOT_EXIST'
        INVALID_PARAM = 'INVALID_PARAM'
        INVALID_STATE = 'INVALID_STATE'
        TRANSFER_BLOCKED = 'TRANSFER_BLOCKED'
        ORDER_BLOCKED = 'ORDER_BLOCKED'
        INSUFFICIENT_DABS = 'INSUFFICIENT_DABS'
        INSUFFICIENT_FUNDS = 'INSUFFICIENT_FUNDS'
        SUBSCRIPTION_LIMIT_EXCEEDED = 'SUBSCRIPTION_LIMIT_EXCEEDED'
        QUOTA_EXCEEDED = 'QUOTA_EXCEEDED'
        DISAGREED_REQUIRED_TERMS = 'DISAGREED_REQUIRED_TERMS'
        INVALID_DABS_CODE = 'INVALID_DABS_CODE'
        INVALID_VERIFY_CODE = 'INVALID_VERIFY_CODE'
        EXPIRED_VERIFY_LIMIT = 'EXPIRED_VERIFY_LIMIT'
        EXCEED_REQUEST_LIMIT = 'EXCEED_REQUEST_LIMIT'
        IDENTITY_VERIFICATION_ERROR = 'IDENTITY_VERIFICATION_ERROR'
        VERIFIED_TOKEN = 'VERIFIED_TOKEN'
        EXPIRED_TOKEN = 'EXPIRED_TOKEN'
        UNKNOWN_RESOURCE = 'UNKNOWN_RESOURCE'
        INVALID_INDIVIDUAL_INFO = 'INVALID_INDIVIDUAL_INFO'
        INTERNAL_SERVER_ERROR = 'INTERNAL_SERVER_ERROR'

        def __str__(self):
            return self.value

    def __init__(self, status=None, *, message=None, code=None, data=None, headers=None):
        code = code.value if isinstance(code, APIResponse.Code) else code

        payload = {
            'message': message,
            'code': code,
            'data': data,
        }

        super().__init__(_remove_none_values(payload), status=status, headers=headers)
